# gtr2_lib — ギターの和音の弾き方を、一から作り直した部品（2026-11-19）
#
# 人間の言葉（21 v5 を聞いて）: 「ギター和音で弾いてないよね？弾くとしたら今までの和音の弾き方を忘れて、一から作り直して欲しい」
# 調べて分かった、今までの部品（vocalo_lib.gtr_strum / gtr_shape）の悪い所:
#   ・strings=3 だと 根音・5度・オクターブ だけで、3度（長調か短調かを決める音）が入らない ＝ 和音に聞こえない
#   ・押さえ方が式で決めた1つの形だけ（どの和音も同じならび）。左右のギターが同じ形
#   ・どの弦も「次のストロークまで」で切っていた（本物は、弾かれなかった弦は鳴りつづける）
#   ・アップは「高い弦から2〜3本」を乱数で決めていて、手の動き（ダウンとアップが交互）と結びついていなかった
#
# 作り直した考え方（調べた事。docs/sound/guitar-chords-v2.md に出どころ）:
#   1. 押さえ方は、指板の上で実際に押さえられる形をさがす（6本の弦・フレット・指のとどく幅）。式で決めない
#   2. 歪んだ音では、6本全部の和音はにごる。小さい形（となり合う3本の弦の三和音・2〜4本）を使う
#   3. 左右のギターは別の形を弾く（低い側＝根音が下の形、高い側＝まん中の弦の三和音の転回形）。ひろがりも出る
#   4. 三和音は、前の和音からいちばん近い形へ動く（指が少ししか動かない＝本物の動き）
#   5. かき鳴らしは、手がずっと下・上に振れている。16分の 1・3 番めはダウン、2・4 番めはアップ。型は D/d（ダウン）と U/u（アップ）で書く
#   6. ダウンは低い弦から、アップは高い弦から。アップは高い側の弦だけ当たる。1回のストロークが弦をわたる時間は 12〜28 ミリ秒（強いほど速い）
#   7. 弦ごとに鳴りつづける: その弦が次に弾かれるか、和音が変わるか、手で止める（.）まで
from vp25_lib import parse_chord, QUAL, PC, nm, midi
import random as _r

TUNING = [40, 45, 50, 55, 59, 64]      # 6弦（低い）→ 1弦。E2 A2 D3 G3 B3 E4


def chord_info(ch):
    """和音の名前 → (根音のピッチクラス, 3度の役の音, 5度, 7度（あれば）, ベースの音)。sus は 3度のかわりに 2度か4度"""
    r, q, b = parse_chord(ch.split("|")[0]); ivs = QUAL[q]; root = PC[r]
    third = next((i for i in ivs if i in (3, 4)), None) or next((i for i in ivs if i in (2, 5)), None)
    fifth = next((i for i in ivs if i in (6, 7, 8)), 7); sev = next((i for i in ivs if i in (10, 11)), None)
    return root, (root + third) % 12 if third is not None else None, (root + fifth) % 12, (root + sev) % 12 if sev is not None else None, PC[b] if b else root


def _shapes(pcs, strings, lo_fret, hi_fret, span, allow_open):
    """strings（となり合う弦）の上で、pcs の音だけを使う押さえ方をぜんぶ出す。フレットの幅は span まで"""
    opts = []
    for s in strings:
        o = [f for f in range(0 if allow_open else max(1, lo_fret), hi_fret + 1) if (TUNING[s] + f) % 12 in pcs and (f == 0 or f >= lo_fret)]
        if not o: return []
        opts.append(o)
    out = []

    def rec(i, cur):
        if i == len(strings):
            fr = [f for f in cur if f > 0]
            if fr and max(fr) - min(fr) > span: return
            out.append(tuple(cur)); return
        for f in opts[i]:
            fr = [x for x in cur + [f] if x > 0]
            if fr and max(fr) - min(fr) > span: continue
            rec(i + 1, cur + [f])
    rec(0, [])
    return out


def triad(ch, prev=None, top_lo=59, top_hi=66, groups=((1, 2, 3), (2, 3, 4))):
    """まん中の弦の三和音（3本）。根音・3度・5度を1つずつ（7 の和音は 5度のかわりに7度でもよい）。前の形にいちばん近い転回形をえらぶ。
    返すのは [(弦, MIDI), …]（低い弦から）"""
    root, third, fifth, sev, _ = chord_info(ch); best = None
    need = [{root, third, fifth}] + ([{third, sev, root}, {third, sev, fifth}] if sev is not None else [])
    for g in groups:
        for want in need:
            for sh in _shapes(want, g, 2, 14, 3, False):
                notes = [TUNING[s] + f for s, f in zip(g, sh)]
                if {n % 12 for n in notes} != want: continue                      # 3つの音がそろっていること
                if not top_lo <= notes[-1] <= top_hi: continue
                move = sum(abs(a - b) for a, b in zip(notes, [m for _, m in prev])) if prev else abs(notes[-1] - (top_lo + top_hi) / 2)
                cost = move + (0.5 if want is not need[0] else 0) + (1.0 if prev and g != tuple(s for s, _ in prev) else 0)
                if best is None or cost < best[0]: best = (cost, list(zip(g, notes)))
    assert best, f"三和音の形が見つからない: {ch}"
    return best[1]


def low_shape(ch, with_third=True):
    """低い側の形: いちばん下が根音。根音・5度・オクターブ（＋ 1オクターブ上の3度＝10度。はなれているので歪んでもにごりにくい）。返すのは [(弦, MIDI), …]"""
    root, third, fifth, sev, _ = chord_info(ch); best = None
    for base in (0, 1):                                   # 根音が6弦か5弦
        for f in range(0, 10):
            r = TUNING[base] + f
            if r % 12 != root: continue
            g = tuple(range(base, base + (4 if with_third and third is not None else 3)))
            want = [{root}, {fifth}, {root, sev} if sev is not None else {root}] + ([{third}] if len(g) == 4 else [])
            sh = []
            for s, w in zip(g, want):
                c = [x for x in range(max(0, f - 1), f + 4) if (TUNING[s] + x) % 12 in w and (x > 0 or f <= 2)]
                if not c: sh = None; break
                sh.append(min(c, key=lambda x: abs(x - (f + 2 if s > base else f))))
            if sh is None: continue
            fr = [x for x in sh if x > 0]
            if fr and max(fr) - min(fr) > 3: continue
            cost = abs(r - 45) * 0.3                                # A2 のあたりがいちばん締まる
            if best is None or cost < best[0]: best = (cost, [(s, TUNING[s] + x) for s, x in zip(g, sh)])
    assert best, f"低い形が見つからない: {ch}"
    return best[1]


def open_shape(ch):
    """生のギター用: 開放弦も使う、4〜6本の形（ローポジション）。いちばん下が根音で、3度が入っていること。返すのは [(弦, MIDI), …]"""
    root, third, fifth, sev, _ = chord_info(ch); pcs = {root, fifth} | ({third} if third is not None else set()) | ({sev} if sev is not None else set()); best = None
    for base in (0, 1, 2):
        g = tuple(range(base, 6))
        for sh in _shapes(pcs, g, 1, 5, 3, True):
            notes = [TUNING[s] + f for s, f in zip(g, sh)]
            if notes[0] % 12 != root: continue
            have = {n % 12 for n in notes}
            if third is not None and third not in have: continue
            if sev is not None and sev not in have: continue
            cost = -2.0 * len(g) + 0.4 * sum(sh) + (3 if fifth not in have else 0) + (1.5 if sum(1 for n in notes if n % 12 == (third if third is not None else -1)) > 1 else 0) + 3.0 * (len(notes) - len(set(notes)))      # 同じ高さの音が2本あるのは不自然
            if best is None or cost < best[0]: best = (cost, list(zip(g, notes)))
    assert best, f"開放弦の形が見つからない: {ch}"
    return best[1]


class Strummer:
    """1本のギターを弾く手。tracks は同じ設定のパートを6本（弦1本ずつ＝弦ごとに鳴りつづけるため）。
    型は16分のマス: D＝強いダウン、d＝ふつうのダウン、U＝強めのアップ、u＝軽いアップ、-＝そのまま鳴らす、.＝手で止める
    きまり: マスの 0・2 番め（拍の頭と「と」）はダウン、1・3 番め（16分のウラ）はアップ（手はいつも下・上に振れている）。ちがう向きを書くとまちがいとして止まる"""

    def __init__(self, tracks, S, seed=1, bright=1.0):
        self.tr, self.S, self.rng, self.bright = tracks, S, _r.Random(seed), bright
        self.ring = {}                      # 弦 → (鳴りはじめの拍, MIDI, 強さ)
        self.last = None                    # さいごに弾いた小節
        self.vel = {i: [] for i in range(len(tracks))}      # 弦ごとの、音の強さの並び（JSON にしたあと velocity() で付ける）
        self.count = {"down": 0, "up": 0, "notes": 0}

    def _stop(self, s, t):
        if s in self.ring:
            t0, m, v = self.ring.pop(s); L = max(0.1, t - t0)
            self.tr[s].ev.append((t0, L, f"{nm(m)}:{L:.3f}")); self.vel[s].append(v); self.count["notes"] += 1

    def bar(self, b, pat, shape, shape2=None, up_strings=None):
        """b 小節めに、型 pat で shape（[(弦, MIDI), …]）を弾く。shape2 があれば、小節の後半（3拍めから）はその形。up_strings: アップで当たる弦の数（既定は 高い側の 2〜3本）"""
        S = self.S; pat = pat.replace(" ", ""); assert len(pat) == 16, pat; t0 = S.bar_beat(b); spb = 60.0 / S.bpm
        if self.last is not None and self.last != b - 1:                 # 弾かない小節をはさんだ: 前に弾いた小節の終わりで止まっている
            for s in list(self.ring): self._stop(s, S.bar_beat(self.last + 1))
        self.last = b

        def change(sh, t):                                               # 和音が変わる: 形に無い弦と、音が変わる弦は、指をはなすので少し前で止まる
            p = dict(sh)
            for s in list(self.ring):
                if s not in p or p[s] != self.ring[s][1]: self._stop(s, t - 0.04)
            return [s for s, _ in sh], p
        strings, pitch = change(shape, t0)
        for i, c in enumerate(pat):
            t = t0 + i * 0.25
            if i == 8 and shape2 is not None: strings, pitch = change(shape2, t)
            if c == "-": continue
            if c == ".":
                for s in list(self.ring): self._stop(s, t)
                continue
            down = c in "Dd"; assert c in "DdUu", c
            assert down == (i % 2 == 0), f"{b + 1}小節め {i} マスめ: {'ダウン' if down else 'アップ'}は、このマスでは手の向きが合わない（{pat}）"
            strong = c in "DU"
            if down: hit = strings if strong or len(strings) <= 3 else (strings if self.rng.random() < 0.6 else strings[:-1] if self.rng.random() < 0.5 else strings[1:])
            else:
                k = up_strings or (3 if strong else 2); hit = strings[-min(k, len(strings)):][::-1]
            spread = (self.rng.uniform(12, 18) if strong else self.rng.uniform(18, 28)) / 1000 / spb          # 弦をわたる時間（拍）
            late = self.rng.uniform(-0.004, 0.006) / spb + (0.003 / spb if not down else 0)                    # 手のゆれ。アップはほんの少しおくれる
            base = (self.rng.uniform(100, 110) if c == "D" else self.rng.uniform(84, 94) if c == "d" else self.rng.uniform(86, 96) if c == "U" else self.rng.uniform(66, 78))
            for k_, s in enumerate(hit):
                tt = t + late + spread * k_ / max(1, len(hit) - 1) if len(hit) > 1 else t + late
                v = base - 1.5 * k_ * (1 if down else 0.6) + self.rng.uniform(-3, 3) + (3 if down and k_ == 0 else 0)      # 最初に当たる弦がいちばん強い
                self._stop(s, tt - 0.005); self.ring[s] = (max(t0, tt), pitch[s], int(max(40, min(120, v * self.bright))))
            self.count["down" if down else "up"] += 1

    def end(self, b_end):
        """曲の終わり（または長い休みの前）で、鳴っている弦を止める"""
        for s in list(self.ring): self._stop(s, self.S.bar_beat(b_end))


    def velocity(self, js):
        """JSON にしたあとで、弦ごとの音に強さ（%数字）を付ける"""
        n = 0
        for s, tr in enumerate(self.tr):
            want = self.vel[s]
            if not want: continue
            for p in js["parts"]:
                if p.get("role") != tr.role: continue
                out, k = [], 0
                for t in p["notes"].split():
                    if t.startswith("R") or "%" in t or k >= len(want): out.append(t); continue
                    out.append(f"{t}%{want[k]}"); k += 1; n += 1
                assert k == len(want), (tr.role, k, len(want))
                p["notes"] = " ".join(out)
        return n
