# ボカロ曲のインスト・アルバム25曲（vp25）の部品（2026-10-25）。設計は docs/sound/vp25-plan.md。
# ラウド26曲（lm25_lib）の音の高さ・和音の道具を借り、電子音・ポップ向けに、
#   ・曲を「場面（scene）」の並びで組み、パートは拍の位置に音を置いていく（小節線をまたぐ長い音も書ける）
#   ・旋律は調の中の度数（1〜7）で書く（転調・移調が楽）
#   ・ドラムは場面ごとの型＋フィル＋ゴースト＋クラッシュ（毎小節同じにしない）
# をまとめる。歌はなし（歌の役はシンセのリードなど）。声の音色は使わない。
import sys, os, json, re, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lm25_lib import (midi, nm, tr, PC, SHARP, FLAT, total, tok_beats, tok_note, merge_rests, fix_len, parse_chord, chord_pcs, QUAL,
                      shift_oct, transpose, strip_marks, scale_pcs, tr_chord, simple_chord)

DRUM_INST = ("kick", "snare", "hihat", "tom", "crash")
NAKED = {p["instrument"]: {k: v for k, v in p.items() if k not in ("notes", "role", "instrument")}
         for p in json.load(open(os.path.join(HERE, "..", "drum-refs", "prog100-naked.json")))["parts"]}

# ---------------- 調と度数 ----------------
MODE_STEPS = {"major": (0, 2, 4, 5, 7, 9, 11), "minor": (0, 2, 3, 5, 7, 8, 10), "dorian": (0, 2, 3, 5, 7, 9, 10),
              "lydian": (0, 2, 4, 6, 7, 9, 11), "mixolydian": (0, 2, 4, 5, 7, 9, 10), "harmonic": (0, 2, 3, 5, 7, 8, 11)}
FLAT_KEYS = {"F", "Bb", "Eb", "Ab", "Db", "Gb", "Dm", "Gm", "Cm", "Fm", "Bbm", "Ebm"}


class Key:
    """調（主音と旋法）。deg('5') → 音名。度数は 1〜7、#/b で半音、' で1オクターブ上、, で1オクターブ下"""
    def __init__(self, tonic, mode="major", oct=5):
        self.tonic, self.mode, self.oct = tonic, mode, oct
        self.flat = tonic in FLAT_KEYS or (len(tonic) > 1 and tonic[1] == "b")
        self.steps = MODE_STEPS[mode]
        self.t = PC[tonic]

    def up(self, semi):
        k = Key(SHARP[(self.t + semi) % 12] if not self.flat else FLAT[(self.t + semi) % 12], self.mode, self.oct)
        k.flat = self.flat
        return k

    def deg(self, d, oct=None):
        oct = self.oct if oct is None else oct
        m = re.match(r"^([#b]*)(\d)(['´,]*)$", d)
        assert m, ("度数が読めない", d)
        acc = m.group(1).count("#") - m.group(1).count("b")
        n = int(m.group(2))
        o = m.group(3).count("'") + m.group(3).count("´") - m.group(3).count(",")
        semi = self.steps[(n - 1) % 7] + 12 * ((n - 1) // 7) + acc
        return nm(self.t + semi + 12 * (oct + 1 + o), self.flat)

    def mel(self, s, oct=None):
        """度数の旋律 → 音名の旋律。'5:0.5 1´:1! -:1 R:1'。休みは R か -"""
        out = []
        for t in s.split():
            d, v = t.split(":", 1)
            if d in ("R", "-"): out.append("R:" + v); continue
            out.append(self.deg(d, oct) + ":" + v)
        return " ".join(out)

    def chord(self, roman):
        """'1' '4' '6m' '5/7' '2m7' のような度数の和音 → 'F' 'Bb' 'Dm' 'C/E' など"""
        base = None
        if "/" in roman: roman, base = roman.split("/")
        m = re.match(r"^([#b]?)(\d)(.*)$", roman)
        acc = (1 if m.group(1) == "#" else -1 if m.group(1) == "b" else 0)
        n = int(m.group(2)); q = m.group(3)
        pc = (self.t + MODE_STEPS["major" if self.mode in ("major", "lydian", "mixolydian") else "minor"][n - 1] + acc) % 12
        name = (FLAT if self.flat else SHARP)[pc] + q
        if base:
            mb = re.match(r"^([#b]?)(\d)$", base)
            acc2 = (1 if mb.group(1) == "#" else -1 if mb.group(1) == "b" else 0)
            pc2 = (self.t + MODE_STEPS["major" if self.mode in ("major", "lydian", "mixolydian") else "minor"][int(mb.group(2)) - 1] + acc2) % 12
            name += "/" + (FLAT if self.flat else SHARP)[pc2]
        return name

    def prog(self, s):
        return [self.chord(x) for x in s.split()]


# ---------------- 和音の音 ----------------
def ch_root(ch):
    return parse_chord(ch.split("|")[0])[0]


def tones(ch, lo, hi):
    """和音の音（lo〜hi の MIDI 番号）"""
    pcs = chord_pcs(ch.split("|")[0])
    return [m for m in range(midi(lo), midi(hi) + 1) if m % 12 in pcs]


def bass_pc(ch):
    r, q, b = parse_chord(ch.split("|")[0])
    return PC[b] % 12


def low(ch, lo="E1"):
    """和音のベースの音（lo から1オクターブの中）"""
    pc = bass_pc(ch)
    m = midi(lo)
    while m % 12 != pc: m += 1
    return m


def voice(ch, center, n=3, prev=None, spread=False):
    """和音を center（MIDI）のまわりに n 音で。prev があれば、なるべく近い動き（声部のつなぎ）。spread で開いた配置"""
    r, q, b = parse_chord(ch.split("|")[0])
    ivs = QUAL[q]
    pcs = [(PC[r] + i) % 12 for i in ivs]
    # 音の選び方: 3度・7度を優先、根音と5度は余れば
    order = [pcs[1] if len(pcs) > 1 else pcs[0]] + ([pcs[3]] if len(pcs) > 3 else []) + [pcs[0]] + ([pcs[2]] if len(pcs) > 2 else []) + pcs[4:]
    use = []
    for p in order:
        if p not in use: use.append(p)
    use = use[:n] if len(use) >= n else (use + use)[:n]
    best = None
    import itertools
    for perm in set(itertools.permutations(use)):
        cur = center - 8; v = []
        for p in perm:
            x = cur + ((p - cur) % 12)
            if spread and v: x += 12 if (x - v[-1]) < 5 else 0
            v.append(x); cur = x + 1
        sc = abs(sum(v) / len(v) - center)
        if prev: sc = sum(abs(a - b_) for a, b_ in zip(sorted(v), sorted(prev))) * 0.6 + sc * 0.4
        if best is None or sc < best[0]: best = (sc, v)
    return sorted(best[1])


# ---------------- 曲 ----------------
class Track:
    def __init__(self, song, role, inst, spec):
        self.song, self.role, self.inst, self.spec = song, role, inst, spec
        self.ev = []          # (拍の位置, 長さ, 文字の音) 。ドラムのグリッドは別
        self.on = True

    def at(self, beat, s):
        """beat（拍）から s（音の並び）を置く"""
        t = float(beat)
        for x in s.split():
            L = tok_beats(x)
            if not (x.startswith("R") or x.startswith("-")): self.ev.append((t, L, x))
            t += L
        return t

    def bar(self, b, s, off=0.0):
        return self.at(self.song.bar_beat(b) + off, s)

    def render(self, total_beats):
        ev = sorted(self.ev, key=lambda e: e[0])
        out, t = [], 0.0
        for st, L, x in ev:
            if st < t - 1e-6:
                # 重なり: 前の音を短くする（1つのパートは同時に1音）
                pst, pL, px = out[-1]
                newL = st - pst
                if newL <= 1e-6:
                    out.pop(); t = pst
                else:
                    out[-1] = (pst, newL, px); t = st
            if st > t + 1e-6: out.append((t, st - t, None))
            out.append((st, L, x)); t = st + L
        if t > total_beats + 1e-6:
            # はみ出しは切る
            keep = []
            for st, L, x in out:
                if st >= total_beats - 1e-6: break
                keep.append((st, min(L, total_beats - st), x))
            out = keep; t = total_beats
        if t < total_beats - 1e-6: out.append((t, total_beats - t, None))
        toks = []
        for st, L, x in out:
            if x is None: toks.append(f"R:{L:.4f}".rstrip("0").rstrip("."))
            else:
                n, v = x.split(":", 1)
                mk = re.match(r"^[0-9.]+", v)
                toks.append(f"{n}:{L:.4f}".rstrip("0").rstrip(".") + v[mk.end():])
        s = merge_rests(" ".join(toks))
        # 長い休み（64拍より長い）は読めないので 32拍ずつに分ける
        out2 = []
        for x in s.split():
            if x.startswith("R:") and tok_beats(x) > 32:
                L = tok_beats(x)
                while L > 32 + 1e-9: out2.append("R:32"); L -= 32
                out2.append(f"R:{L:.4f}".rstrip("0").rstrip("."))
            else: out2.append(x)
        return fix_len(" ".join(out2), total_beats)


class Drums:
    """ドラム（キック・スネア・ハイハットは小節ごとの16分グリッド、タム・シンバルは音）"""
    def __init__(self, song):
        self.song = song
        B = song.beats
        self.n = B * 4
        self.K = ["." * self.n for _ in range(song.nb)]; self.S = list(self.K); self.H = list(self.K)
        self.T = Track(song, "タム", "tom", {}); self.C = Track(song, "シンバル", "crash", {})
        self.P = Track(song, "パーカッション", "tom", {})
        self.R = Track(song, "ライド", "crash", {})   # 2026-10-26 刻み用のライド・シンバル（クラッシュの鳴りを止めないよう別パート）

    def set(self, b, k=None, s=None, h=None):
        for g, arr in ((k, self.K), (s, self.S), (h, self.H)):
            if g is None: continue
            assert len(g) == self.n, ("ドラムの文字数", g, self.n)
            arr[b] = g

    def over(self, b, k=None, s=None, h=None):
        """今のグリッドに上書き（. 以外の文字だけ）"""
        for g, arr in ((k, self.K), (s, self.S), (h, self.H)):
            if g is None: continue
            arr[b] = "".join(c if c != " " else arr[b][i] for i, c in enumerate(g.ljust(self.n, " ")))

    def cym(self, b, s, off=0.0): self.C.bar(b, s, off)
    def tom(self, b, s, off=0.0): self.T.bar(b, s, off)


class Song:
    def __init__(self, no, slug, title, en, bpm, beats=4, key="C", mode="major", genre="", desc=""):
        self.no, self.slug, self.title, self.en, self.bpm, self.beats = no, slug, title, en, bpm, beats
        self.key = Key(key, mode)
        self.genre, self.desc = genre, desc
        self.scenes = []           # (名前, 開始小節, 小節数, 区間の種類)
        self.chords = []           # 小節ごとの和音
        self.tracks = []
        self.tempo = []
        self.flags = "--master -13.5 --widen 1.0"
        self.fade_in = 0; self.fade_out = 0
        self.extra = {}
        self.drums = None
        self.kit = "electro"

    # 場面
    def scene(self, name, bars, kind, chords):
        if isinstance(chords, str): chords = chords.split()
        b0 = len(self.chords)
        self.scenes.append((name, b0, bars, kind))
        for i in range(bars): self.chords.append(chords[i % len(chords)])
        return range(b0, b0 + bars)

    @property
    def nb(self): return len(self.chords)

    def bar_beat(self, b): return b * self.beats

    def sc(self, name):
        """場面の名前（同じ名前が複数あれば、その全部）→ 小節番号のリスト"""
        out = []
        for n, b0, L, k in self.scenes:
            if n == name: out += list(range(b0, b0 + L))
        assert out, ("場面がない", name)
        return out

    def scene_of(self, b):
        for n, b0, L, k in self.scenes:
            if b0 <= b < b0 + L: return n, b - b0, L, k
        raise IndexError(b)

    def track(self, role, inst, **spec):
        t = Track(self, role, inst, spec)
        self.tracks.append(t)
        return t

    def drumkit(self):
        self.drums = Drums(self)
        return self.drums

    def seconds(self):
        sec, bpm, bi = 0.0, self.bpm, 0
        tmap = {e["bar"] - 1: e for e in self.tempo}
        for b in range(self.nb):
            if b in tmap: bpm = tmap[b]["bpm"]
            sec += self.beats * 60 / bpm
        return sec

    def fix_avoid(self, t):
        """強い拍（1・3拍目）か1拍以上の音が、和音の音の半音上でぶつかるとき、半音下の和音の音へ（アヴォイドノート）"""
        n = 0
        B = self.beats
        for k, (st, L, x) in enumerate(t.ev):
            nt, v = x.split(":", 1)
            if nt in ("R", "-"): continue
            bar = min(int(st // B + 1e-6), self.nb - 1)
            ch = self.chords[bar].split("|")[0]
            pcs = chord_pcs(ch)
            m = midi(nt); pc = m % 12
            pos = st - bar * B
            strong = L >= 1 - 1e-6 or abs(pos) < 1e-6 or abs(pos - 2) < 1e-6
            if strong and pc not in pcs and (pc - 1) % 12 in pcs:
                t.ev[k] = (st, L, nm(m - 1, "b" in nt[1:2]) + ":" + v); n += 1
        return n

    def to_json(self):
        TB = self.nb * self.beats
        fixed = sum(self.fix_avoid(t) for t in self.tracks if "リード" in t.role or "歌" in t.role or "旋律" in t.role or t.spec.get("mono"))
        if fixed: print(f"  アヴォイドノートを直した: {fixed}か所")
        parts = []
        for t in self.tracks:
            if not t.ev: continue
            d = {"role": t.role, "instrument": t.inst, "notes": t.render(TB)}
            d.update(t.spec)
            parts.append(d)
        if self.drums:
            D = self.drums
            spec = NAKED if self.kit == "naked" else {k: {kk: vv for kk, vv in v.items() if kk not in ("human",)} for k, v in NAKED.items()}
            dg = getattr(self, "drum_gain", None)
            if dg is None:
                # 電子ドラムのキックは低い所が大きい（01: 40〜100Hz が全体の7割）ので、少し下げる
                dg = {"kick": {"gainDb": -7}} if self.kit == "electro" else {}
            def ds(inst, **kw):
                s_ = dict(spec[inst]); s_.update(dg.get(inst, {})); s_.update(kw); return s_
            parts.append({"role": "キック", "instrument": "kick", "notes": "g:" + "".join(D.K), **ds("kick")})
            parts.append({"role": "スネア", "instrument": "snare", "notes": "g:" + "".join(D.S), **ds("snare")})
            parts.append({"role": "ハイハット", "instrument": "hihat", "notes": "g:" + "".join(D.H), **ds("hihat")})
            if D.T.ev: parts.append({"role": "タム", "instrument": "tom", "notes": D.T.render(TB), **ds("tom")})
            if D.C.ev: parts.append({"role": "シンバル", "instrument": "crash", "notes": D.C.render(TB), **ds("crash")})
            if D.R.ev: parts.append({"role": "ライド（刻み）", "instrument": "crash", "notes": D.R.render(TB),
                                     **ds("crash", volume=getattr(self, "ride_vol", 0.05), pan=0.22)})
        sections = [{"kind": k, "bars": L} for n, b0, L, k in self.scenes]
        song = {"title": self.title, "description": self.desc, "bpm": self.bpm, "beats": self.beats,
                "chords": " ".join(simple_chord(c.split("|")[0]) for c in self.chords), "barsPerChord": 1, "repeats": 1,
                "autoAccompaniment": False, "feel": "vocaloid", "tone": "rock", "dynamics": "natural",
                "human": 0.35, "humanProfile": "role", "humanDist": "triangle", "autoScoop": False, "guitarWobble": False,
                "drumMix": {"kick": {"level": 1.0}, "crash": {"level": 0.8}, "snare": {"level": 0.95}, "hat": {"level": 0.85}},
                "sections": sections, "parts": parts}
        if self.tempo: song["tempo"] = self.tempo
        song.update(self.extra)
        return song

    def write(self, path=None):
        path = path or (sys.argv[1] if len(sys.argv) > 1 else f"/tmp/vp25/vp25-{self.no}-{self.slug}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        js = self.to_json()
        nch = len({(p["instrument"], p.get("patch")) for p in js["parts"] if p["instrument"] not in DRUM_INST})
        json.dump(js, open(path, "w"), ensure_ascii=False)
        drums = {"electro": "--drums electro", "naked": "--drums naked", "jpop": "--drums jpop"}.get(self.kit, "")
        open(path + ".flags", "w").write(f"{drums} {self.flags}".strip())
        open(path + ".fade", "w").write(f"{self.fade_in} {self.fade_out}")
        open(path + ".meta", "w").write(json.dumps({"no": self.no, "title": self.title, "en": self.en}, ensure_ascii=False))
        sec = self.seconds()
        print(f"{self.no} {self.title}: {self.nb}小節・{int(sec // 60)}分{int(sec % 60):02d}秒・楽器{nch}種 → {path}")
        if not (240 <= sec <= 300): print(f"  注意: 長さが 4〜5分の外です（{sec:.0f}秒）")


# ---------------- 音色（パートの設定） ----------------
def P(**kw): return kw

# 歌の役のリード（粒が立って透き通る高音。人間「リードの高音の部分がもう少し粒が立って透き通るように」）
def lead_spec(patch="squareLead", vol=0.2, pan=0.0, delay=0.75, bright=0.0, extra_fx=()):
    # 2026-10-25: 切り抜きで測ると、高い所を持ち上げたぎらつくリードは PQ を 0.4 下げた（sawLead）。
    #   7kHz から上を切り、900Hz の鼻にかかる所を少し引いた、やわらかいリードにする（03 の切り抜き: 7.28 → 7.67）
    fx = [{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7},
          {"type": "filter", "kind": "lowpass", "freq": 7000 + 1500 * bright, "q": 0.7},
          {"type": "eq", "low": 0, "mid": -2.5, "midHz": 900, "high": -1 + bright},
          *extra_fx,
          {"type": "pingpong", "beats": delay, "mix": 0.12, "feedback": 0.25},
          {"type": "plate", "mix": 0.18}]
    return P(patch=patch, volume=vol, pan=pan, phrase=8, reverb=0.18, noRestrike=True, mono=True, gainDb=2, fx=fx)


def pad_spec(patch="warmPad", vol=0.09, pan=0.0, duck=0.0, sustain=2.0):
    return P(patch=patch, volume=vol, pan=pan, reverb=0.4, sustain=sustain, duck=duck,
             fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "eq", "low": 0, "mid": -3, "midHz": 450, "high": -1}])


def pluck_spec(patch="pluckSynth", vol=0.11, pan=0.3, delay=0.75, sustain=0.6):
    return P(patch=patch, volume=vol, pan=pan, sustain=sustain, reverb=0.25,
             fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "pingpong", "beats": delay, "mix": 0.18, "feedback": 0.3}])


def synth_bass_spec(patch="synthBass1", vol=0.22, duck=0.25, bright=0.0):
    # こもらせない: 600〜1500Hz のうなりと 1.5〜3kHz の粒（制作指示書 4）。2026-10-25: 01 で 40〜100Hz が全体の7割になったので、
    #   いちばん下を削り（40Hz より下を切り、低い棚を -4dB）、音量を 0.8 倍に
    return P(patch=patch, volume=round(vol * 0.8, 3), pan=0, duck=duck, sustain=0.9,
             fx=[{"type": "filter", "kind": "highpass", "freq": 40, "q": 0.7}, {"type": "eq", "low": -4, "mid": 4, "midHz": 900, "high": 0},
                 {"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 1.5 + bright}])


def finger_bass_spec(vol=0.2, duck=0.15):
    return P(volume=vol, pan=0, amp="bassSplit", ampDrive=0.45, duck=duck,
             fx=[{"type": "eq", "low": 0, "mid": 3, "midHz": 1000, "high": 0}, {"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}])


def sub_spec(vol=0.26):
    return P(volume=vol, pan=0, sustain=1.0)


def piano_spec(vol=0.15, pan=-0.2, reverb=0.25):
    return P(volume=vol, pan=pan, reverb=reverb, fx=[{"type": "eq", "low": -2, "mid": -1.5, "midHz": 350, "high": 1}])


def clean_gtr_spec(vol=0.12, pan=0.45):
    # コーラスなし（人間「きゅいんきゅいん」は嫌い）
    return P(volume=vol, pan=pan, amp="jpopClean", chorus=0, reverb=0.2, humanPitch=0, sustain=1.4,
             fx=[{"type": "filter", "kind": "highpass", "freq": 150, "q": 0.7}])


def strings_spec(vol=0.09, pan=0.5):
    return P(volume=vol, pan=pan, reverb=0.35, sustain=1.6)


def riser(track, b, beats=4, kind="C4"):
    """ライザー（fxRiser C4＝4秒 D4＝8秒）を b 小節の前に置く（音の終わりが b の頭）"""
    s = track.song
    track.at(s.bar_beat(b) - beats, f"{kind}:{beats:g}")


def cym_swell(track, b, beats=2, kind="C4"):
    """本物のシンバルの効果音（C＝逆再生クラッシュ・E＝スウェル）。音の終わりが b の頭"""
    s = track.song
    track.at(s.bar_beat(b) - beats, f"{kind}:{beats:g}")


# ---------------- 伴奏の型 ----------------
def chord_voices(song, bars, center=60, n=3, spread=False):
    """小節ごとの和音の配置（なめらかにつなぐ）→ {小節: [MIDI...]}"""
    out, prev = {}, None
    for b in bars:
        v = voice(song.chords[b], center, n, prev, spread)
        out[b] = v; prev = v
    return out


def pat_notes(pattern, pitches, step=0.25, marks=None):
    """pattern: 文字列（数字＝pitches の何番目・. ＝休み・- ＝前の音を伸ばす）。1文字＝step 拍"""
    toks = []
    for i, c in enumerate(pattern):
        if c == ".": toks.append(["R", step]); continue
        if c == "-" and toks: toks[-1][1] += step; continue
        idx = int(c) if c.isdigit() else "abcdefghij".index(c) + 10
        toks.append([nm(pitches[idx % len(pitches)] + 12 * (idx // len(pitches))), step, (marks or {}).get(i, "")])
    return " ".join(f"{t[0]}:{t[1]:g}{t[2] if len(t) > 2 else ''}" if t[0] != "R" else f"R:{t[1]:g}" for t in toks)


def bass_line(song, b, style="root8", nxt=None, lo="E1"):
    """ベースの小節の型。style: root8（8分の根音）・oct8（オクターブ）・house（裏）・disco（オクターブの16分）・long（伸ばす）・
    walk（4分のつなぎ）・push（キックに合わせたシンコペ）・half（2分）"""
    ch = song.chords[b]
    r = low(ch, lo)
    B = song.beats
    nx = song.chords[b + 1] if b + 1 < song.nb else ch
    rn = low(nx, lo)
    ap = rn - 1 if rn > r else (rn + 1 if rn < r else r + 7)
    f5 = r + 7
    N = lambda m, L, mk="": f"{nm(m)}:{L:g}{mk}"
    if B != 4:
        if style == "long": return f"{nm(r)}:{B}"
        return " ".join(N(r, 1, "!" if i == 0 else "") for i in range(B))
    if style == "root8": return " ".join(N(r, 0.5, "!" if i == 0 else "") for i in range(7)) + " " + N(ap, 0.5)
    if style == "oct8": return " ".join(N(r + (12 if i % 2 else 0), 0.5) for i in range(7)) + " " + N(ap, 0.5)
    if style == "house": return " ".join(f"R:0.5 {N(r + (12 if i == 3 else 0), 0.5)}" for i in range(4))
    if style == "disco": return " ".join(N(r + (12 if i % 2 else 0), 0.25) for i in range(14)) + " " + N(ap, 0.25) + " " + N(ap + 12, 0.25)
    if style == "long": return N(r, 4)
    if style == "half": return N(r, 2) + " " + N(f5, 1.5) + " " + N(ap, 0.5)
    if style == "walk": return N(r, 1) + " " + N(r + 4 if "m" not in ch.split("/")[0][1:3] else r + 3, 1) + " " + N(f5, 1) + " " + N(ap, 1)
    if style == "push": return N(r, 0.75, "!") + " " + N(r, 0.75) + " " + N(r + 12, 0.5) + " R:0.5 " + N(r, 0.75) + " " + N(ap, 0.75)
    if style == "pulse": return " ".join(N(r, 0.25, "!" if i % 4 == 0 else ",") for i in range(16))
    raise ValueError(style)


# ---------------- ドラムの型 ----------------
def g(s, n=16):
    s = s.replace(" ", "")
    assert len(s) == n, (s, len(s), n)
    return s


GROOVE = {
    # 名前: (キック, スネア, ハイハット)
    "four": ("X...X...X...X...", "....X.......X...", "..x...x...x...x."),
    "four16": ("X...X...X...X...", "....X.......X...", "xoxOxoxOxoxOxoxO".replace("O", "x")),
    "fourOpen": ("X...X...X...X...", "....X.......X...", "..O...O...O...O."),
    "pop16": ("X.....x...X.....", "....X......oX...", "XoxoXoxoXoxoXoxo"),
    "pop8": ("X.....x.X.......", "....X.......X...", "X.x.X.x.X.x.X.x."),
    "vocarock": ("X.x...x.X.x.....", "....X..o....X..o", "X.x.X.x.X.x.X.x."),
    "drive": ("X.X...X.X.X...X.", "....X.......X...", "X.x.X.x.X.x.X.x."),
    "half": ("X.........x.....", "........X.......", "X.x.X.x.X.x.X.x."),
    "twostep": ("X.......x.x.....", "....X.......X...", "x.xox.x.x.xox.x."),
    "boombap": ("X.....x...X..x..", "....X.......X...", "x.x.x.x.x.x.x.x."),
    "trap": ("X.........X.....", "........X.......", "x.x.x.x.x.x.x.x."),
    "disco": ("X...X...X...X...", "....X.......X...", "xxOxxxOxxxOxxxOx".replace("O", "x")),
    "march": ("X.......X.......", "....X..xx...X.xx", "x...x...x...x..."),
    "shuffleish": ("X.....x...X.....", "....X.......X...", "x..xx..xx..xx..x"),
    "sparse": ("X...............", "................", "x...x...x...x..."),
    "none": ("................", "................", "................"),
}


def fill_bar(kind, n=16, beats=4):
    """フィルの形（スネア, タムの音, ハイハットを残す長さ）。kind: small・snare16・tomdown・build・lift・flam"""
    if kind == "small": return ("....X.......oxXX", None, 12)
    if kind == "snare16": return ("....X...ooxxXXXX", None, 8)
    if kind == "tomdown": return ("....X...........", "R:2 C4:0.25 C4:0.25 A3:0.25 A3:0.25 F3:0.25 F3:0.25 D3:0.25! A2:0.25!", 8)
    if kind == "tomtrip": return ("....X...........", "R:2 C4:0.3333 A3:0.3333 F3:0.3334 D3:0.3333 A2:0.3333 A2:0.3334!", 8)
    if kind == "build": return ("x.x.x.x.xxxxXXXX", None, 0)
    if kind == "lift": return ("o.o.x.x.xxxxXXXX", "R:3 D3:0.25 D3:0.25 A2:0.25! A2:0.25!", 0)
    if kind == "kickfill": return ("....X.......X...", None, 12)
    raise ValueError(kind)


def put_groove(D, b, name, k=None, s=None, h=None, ghosts=0.0, seed=0, hat_vary=True):
    """型を置く（k/s/h で一部を差しかえ）。ghosts: スネアのゴーストを入れる量（0〜1）。hat_vary: 4小節ごとにハットの強弱を変える"""
    gk, gs, gh = GROOVE[name] if isinstance(name, str) else name
    gk, gs, gh = k or gk, s or gs, h or gh
    n = D.n
    if n != 16:
        gk, gs, gh = (x[:n] if len(x) >= n else (x * (n // 16 + 1))[:n] for x in (gk, gs, gh))
    rnd = random.Random(seed * 131 + b)
    if ghosts > 0:
        sl = list(gs)
        for i in range(n):
            if sl[i] == "." and i % 2 == 1 and rnd.random() < ghosts * 0.35 and not (i in (3, 11) and sl[(i + 1) % n] == "X"):
                sl[i] = "o"
        gs = "".join(sl)
    if hat_vary and "x" in gh:
        hl = list(gh)
        # 拍の頭を強く、2拍目と4拍目の裏をたまに開く
        for i in range(0, n, 4):
            if hl[i] == "x": hl[i] = "X"
        if (b % 4) == 3 and hl[n - 2] in "xX": hl[n - 2] = "O"
        gh = "".join(hl)
    D.set(b, gk, gs, gh)


def put_fill(D, b, kind):
    fs, tomn, keep = fill_bar(kind, D.n, D.song.beats)
    sn = D.S[b]
    sn = "".join(f if f != "." else (sn[j] if j < (keep if keep else D.n) else ".") for j, f in enumerate(fs[:D.n]))
    hh = D.H[b][:keep] + "." * (D.n - keep) if keep else "." * D.n
    kk = D.K[b]
    if tomn:
        kk = kk[:8] + "".join("X" if j % 4 == 0 else "." for j in range(D.n - 8))
        D.tom(b, tomn)
    D.S[b] = sn; D.H[b] = hh; D.K[b] = kk


def crash(D, b, which="C2", L=4):
    D.cym(b, f"{which}:{L:g}")
    D.H[b] = "." + D.H[b][1:]


def stop(D, b, at=1):
    """止め: at 拍目だけ叩いてあとは休む"""
    n = D.n
    D.set(b, "X" + "." * (n - 1), "X" + "." * (n - 1) if at else "." * n, "." * n)


# ---------------- 旋律の道具 ----------------
def seq_up(s, k: Key, steps):
    """度数の旋律を、音階の段で steps 段ずらす（ゼクエンツ）"""
    out = []
    for t in s.split():
        d, v = t.split(":", 1)
        if d in ("R", "-"): out.append(t); continue
        m = re.match(r"^([#b]*)(\d)(['´,]*)$", d)
        n = int(m.group(2)) - 1 + steps
        o = m.group(3).count("'") - m.group(3).count(",") + n // 7
        n = n % 7 + 1
        out.append(f"{m.group(1)}{n}{chr(39) * o if o > 0 else ',' * (-o)}:{v}")
    return " ".join(out)


def retro(s):
    """逆から（逆行形）"""
    toks = s.split()
    return " ".join(reversed(toks))


def invert(s, k: Key, axis="5"):
    """上下を逆に（反行形）。音階の段で axis を軸に"""
    def idx(d):
        m = re.match(r"^([#b]*)(\d)(['´,]*)$", d)
        return int(m.group(2)) - 1 + 7 * (m.group(3).count("'") - m.group(3).count(","))
    a = idx(axis)
    out = []
    for t in s.split():
        d, v = t.split(":", 1)
        if d in ("R", "-"): out.append(t); continue
        i = 2 * a - idx(d)
        o, n = divmod(i, 7)
        out.append(f"{n + 1}{chr(39) * o if o > 0 else ',' * (-o)}:{v}")
    return " ".join(out)


def beats_of(s): return total(s)


# ---------------- ロックの音色（ボカロロック） ----------------
def rock_gtr_spec(vol=0.12, pan=0.0, tone="jpop-rock-drive", drive=None):
    """歪みのバッキング（浅め・コードが聞こえる。左右は double で別テイク）。ローの持ち上げはしない（+4dB 以内の決まり）"""
    d = P(volume=vol, pan=pan, guitarTone=tone, powerChord=False, sustain=1.3, release=0.5, chorus=0, humanPitch=0, noScoop=True,
          fx=[{"type": "filter", "kind": "highpass", "freq": 90, "q": 0.7}, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 1500, "high": 0},
              {"type": "eq", "low": 0, "mid": 1.5, "midHz": 3500, "high": 1}, {"type": "room", "mix": 0.08}])
    if drive is not None: d["ampDrive"] = drive
    return d


def lead_gtr_spec(vol=0.14, pan=-0.05):
    """リードギター（浅い歪み・中域が太い。高音は鋭いが優しく）。ビブラートは控えめ"""
    return P(volume=vol, pan=pan, guitarTone="warm-lead-a", phrase=8, noRestrike=True, mono=True, chorus=0, humanPitch=0, gainDb=2,
             fx=[{"type": "eq", "low": -2, "mid": 2, "midHz": 1500, "high": 1}, {"type": "eq", "low": 0, "mid": 1.5, "midHz": 3000, "high": 0},
                 {"type": "room", "mix": 0.12}])


def rock_bass_spec(vol=0.19):
    # 指弾き（--bass bnb-loud）。600〜1500Hz のうなりと 1.5〜3kHz の粒を出す
    return P(volume=vol, pan=0, amp="bassSplit", ampDrive=0.55, duck=0.12,
             fx=[{"type": "eq", "low": 0, "mid": 4, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}])


def power(ch, lo="E2"):
    """パワーコードの根音と5度とオクターブ（MIDI）"""
    r = low(ch, lo)
    return [r, r + 7, r + 12]


# ---------------- 旋律の自動の下書き（和音に沿って、start から end へ） ----------------
RHY_LIB = {
    "walk8": [[0.5] * 8, [1, 0.5, 0.5, 1, 1], [0.5, 0.5, 1, 0.5, 0.5, 1], [1.5, 0.5, 1, 1]],
    "song": [[-0.5, 0.5, 0.5, 0.5, 1, 1], [1.5, 0.5, 2], [-0.5, 0.5, 1, 0.5, 0.5, 1], [2, 1, 1], [0.75, 0.25, 0.5, 0.5, 2]],
    "long": [[2, 2], [3, 1], [4], [1, 1, 2]],
}


def gen_phrase(song, bars, start, end, rhy="song", seed=0, key=None, lo="C4", hi="C6", last_long=True, arch=5):
    """和音に沿った旋律の下書き（小節ごとの文字列のリスト）。start・end は MIDI。強い拍と長い音は和音の音、そのほかは音階の音で、
    start から end へ少しずつ寄っていく。最後の音は end を長く"""
    key = key or song.key
    sc = sorted({(key.t + s_) % 12 for s_ in key.steps})
    pool = [m for m in range(midi(lo), midi(hi) + 1) if m % 12 in sc]
    rnd = random.Random(seed)
    lib = RHY_LIB[rhy]
    nbars = len(bars)
    out = []
    cur = start
    total_notes = 0
    plan = []
    for k, b in enumerate(bars):
        r = list(lib[(seed + k) % len(lib)])
        if k == nbars - 1 and last_long: r = [x for x in r[:2] if True] + [song.beats - sum(abs(x) for x in r[:2])] if sum(abs(x) for x in r[:2]) < song.beats else [song.beats]
        plan.append(r); total_notes += sum(1 for x in r if x > 0)
    j = 0
    for k, b in enumerate(bars):
        ch = song.chords[b].split("|")[0]
        pcs = chord_pcs(ch)
        toks, t = [], 0.0
        for idx, d in enumerate(plan[k]):
            if d < 0: toks.append(f"R:{-d:g}"); t += -d; continue
            frac = j / max(1, total_notes - 1)
            target = start + (end - start) * frac + arch * math.sin(math.pi * frac) + 2.5 * math.sin(2 * math.pi * j / 5 + seed)
            strong = abs(t % 2) < 1e-6 or d >= 1
            cands = [m for m in pool if 0 < abs(m - cur) <= (4 if not strong else 9)] or [cur]
            if strong: cands = [m for m in cands if m % 12 in pcs] or [m for m in pool if m % 12 in pcs and abs(m - cur) <= 12]
            # 目標へ寄せつつ、少し揺らす（同じ音が続きすぎない）
            m = min(cands, key=lambda x: abs(x - target) + (2.5 if x == cur else 0) + rnd.random() * 2.0)
            if k == nbars - 1 and idx == len(plan[k]) - 1: m = end
            toks.append(f"{nm(m, key.flat)}:{d:g}"); cur = m; j += 1; t += d
        out.append(" ".join(toks))
    return out
