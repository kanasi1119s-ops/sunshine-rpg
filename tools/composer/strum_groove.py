"""曲に合わせて決めたかき鳴らしの型に、本物のギタリストの「揺れ方」をのせる（グルーヴのひな形。2026-11-07）。

人間「和音になったけど曲として成立してないよ」:
  前夜祭では、人の演奏データ（GuitarSet）をそのまま場面に当てはめたので、元の曲のコードの変わり目・句・速さのまま鳴り、
  この曲のアクセントやドラムとそろわなかった。プロは「どこで弾くか」を曲に合わせて決め、人の演奏からは揺れ方だけをもらう。
  ここでは:
    - 型（16分の16文字）で、打つ場所・向き・強さ・止める所を曲に合わせて決める
    - 1打ごとに、同じ場所（16分の何番目か）・同じ向きで本物のギタリストが弾いた打ちを1つ選び、
      その「ずれ（拍）・弦から弦への速さ（秒）・強さ・鳴らした弦の数」だけを借りる
型の文字:
  D 強いダウン（全部の弦）／d ふつうのダウン（低い弦を1本外すこともある）／U アップ（高い弦3〜4本）／u 弱いアップ（高い弦2〜3本）
  x ミュートの「チャッ」（短く・弱く）／P 次の小節のコードを先取りする強いダウン／- 前の打ちをのばす／. 止める（鳴っている弦を止める）
使い方:
  g = Groove(seed=1)
  ev = g.bar(bar_index, "D-d-dUd-D-d-dUdU", voicing_of_bar, next_voicing, bpm, vel=1.0)   → 弦ごとの [拍, 長さ, 音名, 強さ]
  （ev を弦ごとにためて、merge_lane() で notes 文字列にする）
"""
import math, random
from gset_to_parts import load

TAKES = ["00_Rock3-117-Bb_comp", "01_Rock3-117-Bb_comp", "00_Rock3-148-C_comp", "04_Rock3-148-C_comp", "01_Rock3-148-C_comp", "02_Rock3-148-C_comp",
         "03_Rock3-148-C_comp", "02_Rock3-117-Bb_comp", "03_Rock3-117-Bb_comp", "05_Rock3-148-C_comp"]


class Groove:
    def __init__(self, seed=1, takes=None, amount=1.0):
        self.rnd = random.Random(seed); self.amount = amount
        self.lib = {}   # (16分の位置の偶奇, 上か下か) → [(ずれ[拍], 速さ[秒/弦], 強さ, 弦の数)]
        for t in (takes or TAKES):
            try:
                strums, bpm = load(t)
            except Exception:
                continue
            for s in strums:
                slot = round(s["beat"] * 4); dev = s["beat"] - slot / 4
                if abs(dev) > 0.12: continue
                ns = len(s["notes"])
                spread = (max(x[1] for x in s["notes"]) / max(1, ns - 1)) if ns > 1 else 0.012
                self.lib.setdefault((slot % 2, s["up"]), []).append((dev, min(0.03, max(0.004, spread)), s["vel"], ns))
        for k in list(self.lib): self.lib[k].sort()

    def pick(self, odd, up):
        L = self.lib.get((odd, up)) or self.lib.get((odd, not up)) or [(0.0, 0.012, 100, 4)]
        return L[self.rnd.randrange(len(L))]

    def bar(self, bi, pat, vo, vo_next, bpm, vel=1.0):
        """1小節（16分×16）。vo: 6本ぶんの音名（低い弦から。鳴らさない弦は None）"""
        sp = 60.0 / bpm; out = []; held = {}   # 弦 → 鳴っている事件
        def stop(t):
            for st, e in list(held.items()):
                e[1] = max(0.05, t - e[0] - 0.01); del held[st]
        for i, c in enumerate(pat):
            t0 = bi * 4 + i * 0.25
            if c == '-': continue
            if c == '.': stop(t0); continue
            up = c in 'Uu'
            dev, spd, v, ns = self.pick(i % 2, up)
            dev *= self.amount
            v = 100 + (v - 100) * 0.6 * self.amount    # 強さの揺れは6割（型で決めた強弱を崩しすぎない）
            v *= {'D': 1.12, 'P': 1.15, 'd': 0.97, 'U': 0.86, 'u': 0.72, 'x': 0.5}[c] * vel
            voc = vo_next if c == 'P' else vo
            strs = [k for k in range(6) if voc[k] is not None]
            if c in 'Uu':
                n = max(2, min(len(strs), (4 if c == 'U' else 3) - (1 if ns <= 2 else 0)))
                strs = strs[-n:][::-1]
            elif c == 'd' and ns <= 3 and len(strs) > 4 and self.rnd.random() < 0.5:
                strs = strs[1:]
            t = max(0.0, t0 + dev)
            stop(t)
            for k, st in enumerate(strs):
                tt = t + k * spd / sp
                e = [tt, 0.0, voc[st], int(max(35, min(140, v * (0.94 if k and not up else 1.0))))]
                if c == 'x':
                    e[1] = 0.07
                else:
                    held[st] = e
                out.append((st, e))
        return out, held


class Lanes:
    """弦ごとの事件をためて、小節をまたいでのばす（次の打ちか「.」まで鳴らす）"""
    def __init__(self):
        self.ev = [[] for _ in range(6)]; self.held = {}

    def add(self, res):
        out, held = res
        # 前の小節からのばしていた弦は、この小節の最初の打ち（どの弦でも）で止める
        if out:
            first = min(e[0] for _, e in out)
            for st, e in list(self.held.items()):
                e[1] = max(0.05, min(first - e[0] - 0.01, 8.0))   # 間が空いたときは、のばすのは最大2小節
            self.held = {}
        for st, e in out: self.ev[st].append(e)
        for st, e in held.items():
            self.held[st] = e
        # 小節の終わりまでの長さを仮に入れておく（次の小節で上書き）
        for st, e in held.items():
            if e[1] <= 0: e[1] = max(0.05, (math.floor(e[0] / 4) + 1) * 4 - e[0] - 0.01)

    def stop_at(self, t):
        for st, e in list(self.held.items()):
            e[1] = max(0.05, min(t - e[0] - 0.01, 8.0))
        self.held = {}

    def notes(self, total):
        res = []
        for lane in self.ev:
            lane.sort(key=lambda e: e[0]); toks = []; cur = 0.0
            for i, (t, d, n, v) in enumerate(lane):
                if t < cur - 1e-6: continue
                nxt = lane[i + 1][0] if i + 1 < len(lane) else total
                d = max(0.04, min(d if d > 0 else min(3.0, nxt - t), nxt - t - 0.01, total - t))   # 長さ未定（単音の分散和音）は、次の音まで（最大3拍）
                if t > cur + 1e-4:
                    r = t - cur
                    while r > 16 + 1e-6: toks.append('R:16'); r -= 16
                    toks.append(f'R:{r:.4f}')
                toks.append(f'{n}:{d:.4f}%{v}'); cur = t + d
            r = total - cur
            while r > 16 + 1e-6: toks.append('R:16'); r -= 16
            if r > 1e-4: toks.append(f'R:{r:.4f}')
            res.append(' '.join(toks) if lane else None)
        return res
