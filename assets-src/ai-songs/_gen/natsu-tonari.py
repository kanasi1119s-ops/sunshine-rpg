# 『あの夏のとなり』（仮）: 夏を感じる、甘酸っぱい恋にたどり着くようなボカロ風の曲（歌なし）。BPM115・イ長調、約4分44秒。
# 甘酸っぱさ: 長7度の和音（maj7）と、F#m へ引き寄せる C#7（3度の属七）を多めに。最後のサビは半音上（変ロ長調）。
# 旋律: A・Bメロ・ブリッジ・落ちサビはエレピ（keys）、サビ・間奏・ソロ・終わりはリードギター（音色プリセット warm-lead-a）。
# 伴奏: 生ピアノの分散和音（Aメロ8分・サビ16分）、クリーンギター（コーラスなし・長めの音のアルペジオ）、左右の弦、ベル、ベース、生ドラム（-10dB）。
# 構成（136小節）: イントロ8 → Aメロ16 → Bメロ8 → サビ16 → 間奏8 → Aメロ8 → Bメロ8 → サビ16 → ブリッジ8 → ソロ8 → 落ちサビ8 → 転調サビ16 → 終わり8
# 使い方: python3 natsu-tonari.py <出力.json>
import json, re, sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import drumkit

def fmt(x): return ("%.4f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pcof(s):
    r = PCN[s[0]]
    if len(s) > 1 and s[1] == "#": r += 1
    if len(s) > 1 and s[1] == "b": r -= 1
    return r % 12
def midi(n):
    i = 2 if len(n) > 2 and n[1] in "#b" else 1
    return pcof(n[:i]) + 12 * (int(n[i:]) + 1)
def tr(tok, k):
    if tok.startswith("R:") or k == 0: return tok
    n, rest = tok.split(":", 1)
    return nm(midi(n) + k) + ":" + rest
def fold(tok, hi=88):  # リードギターの音域（〜E6）を超える音は1オクターブ下げる
    if tok.startswith("R:"): return tok
    n_, rest_ = tok.split(":", 1); m = midi(n_)
    return nm(m - 12 if m > hi else m) + ":" + rest_
def seq(lst, k=0, f=lambda x: x): return " ".join(f(tr(x, k)) for x in " ".join(lst).split())
def up(chs, k):  # コード名を k 半音上げる（フラット表記）
    F = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    out = []
    for c in chs:
        parts = []
        for x in c.split("/"):
            m = re.match(r"^([A-G][#b]?)(.*)$", x); parts.append(F[(pcof(m.group(1)) + k) % 12] + m.group(2))
        out.append("/".join(parts))
    return out

# ---------------- コード ----------------
INTRO = "Dmaj7 E C#m7 F#m7 Dmaj7 E Amaj7 Amaj7".split()
VERSE = "Amaj7 E/G# F#m7 C#m7 Dmaj7 A/C# Bm7 E".split()
VERSE2 = "Amaj7 E/G# F#m7 C#m7 Dmaj7 C#7 F#m7 E".split()
PRE = "Dmaj7 E C#m7 F#m7 Bm7 C#m7 Dmaj7 E".split()
CHO1 = "Dmaj7 C#7 F#m7 E/G# Dmaj7 C#7 F#m7 A7".split()
CHO2 = "Dmaj7 C#7 F#m7 E Bm7 E Amaj7 Amaj7".split()
BRI = "F#m7 Dmaj7 E C#m7 Bm7 C#m7 Dmaj7 E".split()
SEC = [("intro", INTRO, 0, 0),
       ("verse", VERSE, 0, 0), ("verse", VERSE2, 0, 1), ("pre", PRE, 0, 0), ("chorus", CHO1, 0, 0), ("chorus", CHO2, 0, 1),
       ("inter", INTRO, 0, 0),
       ("verse", VERSE2, 0, 2), ("pre", PRE, 0, 1), ("chorus", CHO1, 0, 0), ("chorus", CHO2, 0, 1),
       ("bridge", BRI, 0, 0), ("solo", CHO1, 0, 0), ("otosabi", CHO1, 0, 0),
       ("chorus", up(CHO1, 1), 1, 2), ("chorus", up(CHO2, 1), 1, 3),
       ("outro", up(INTRO, 1), 1, 0)]
chords = [c for _, pr, _, _ in SEC for c in pr]
GAIN = {"intro": .8, "verse": .8, "pre": .88, "chorus": 1.0, "inter": .88, "bridge": .82, "solo": .96, "otosabi": .68, "outro": .9}
ARC = []
for si, (s, pr, k, n) in enumerate(SEC):
    g = GAIN[s] + (0.03 if si >= 7 and s not in ("otosabi", "bridge") else 0)
    ARC += [round(min(1.05, g + (0.06 * i / len(pr) if s in ("pre", "otosabi") else 0)), 3) for i in range(len(pr))]

def barsum(toks):
    t = 0
    for x in toks:
        if x.startswith("g:"): assert len(x) == 18, x; t += 4; continue
        d = x.split(":")[1]; t += float("".join(c for c in d if c.isdigit() or c == "."))
    return t
def cat(secs, name):
    out = []
    for (s, pr, _, _), toks in zip(SEC, secs):
        if isinstance(toks, str): toks = toks.split()
        assert abs(barsum(toks) - 4 * len(pr)) < 1e-6, (name, s, barsum(toks), 4 * len(pr))
        out += toks
    return " ".join(out)
def per(fn): return [fn(si, s, pr, k, n) for si, (s, pr, k, n) in enumerate(SEC)]
def rest(pr): return f"R:{fmt(4 * len(pr))}"

def chord_pcs(ch):
    m = re.match(r"^([A-G][#b]?)(.*)$", ch.split("/")[0]); r = pcof(m.group(1)); q = m.group(2)
    minor = q.startswith("m") and not q.startswith("maj")
    pcs = [r, (r + (3 if minor else 4)) % 12, (r + 7) % 12]
    if "maj7" in q: pcs.append((r + 11) % 12)
    elif "7" in q: pcs.append((r + 10) % 12)
    return pcs
def bass_pc(ch): return pcof(re.match(r"^([A-G][#b]?)", ch.split("/")[1]).group(1)) if "/" in ch else chord_pcs(ch)[0]
def tones_from(ch, lo):
    pcs = chord_pcs(ch); r = pcs[0]; base = lo + ((r - lo) % 12)
    return sorted(base + o + ((p - r) % 12) for o in (0, 12) for p in pcs)
def voicing(ch, center):
    pcs = chord_pcs(ch)[:3]; best = None
    for inv in range(3):
        o = pcs[inv:] + pcs[:inv]; cur = center - 7; v = []
        for p in o:
            x = cur + ((p - cur) % 12); v.append(x); cur = x + 1
        sc = abs(sum(v) / 3 - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]

# ---------------- 旋律 ----------------
M_I = ["A5:0.5 C#6:0.5 E6:0.5 C#6:0.5 A5:1 F#5:1", "G#5:0.5 B5:0.5 E6:0.5 B5:0.5 G#5:1 E5:1",
       "E5:0.5 G#5:0.5 B5:0.5 G#5:0.5 E5:1 C#5:1", "C#6:2 A5:2",
       "A5:0.5 C#6:0.5 E6:0.5 C#6:0.5 A5:1 F#5:1", "G#5:0.5 B5:0.5 E6:0.5 B5:0.5 G#5:1 E5:1",
       "C#6:0.5 E6:0.5 G#5:0.5 A5:0.5 E5:2", "A5:3 R:1"]
M_A = ["R:0.5 E4:0.5 A4:0.5 B4:0.5 C#5:1 B4:0.5 A4:0.5", "B4:1.5 G#4:0.5 E4:1 R:1",
       "R:0.5 F#4:0.5 A4:0.5 C#5:0.5 E5:1 C#5:0.5 B4:0.5", "C#5:1.5 B4:0.5 G#4:1 R:1",
       "R:0.5 D5:0.5 C#5:0.5 D5:0.5 F#5:1 E5:0.5 D5:0.5", "C#5:1 A4:0.5 C#5:0.5 E5:1 C#5:1",
       "D5:0.5 C#5:0.5 B4:0.5 A4:0.5 B4:1 F#4:1", "G#4:2 E4:1 R:1"]
M_A2 = M_A[:2] + ["R:0.5 F#4:0.5 A4:0.5 C#5:0.5 F#5:1 E5:0.5 C#5:0.5", M_A[3],
                  "R:0.5 F#5:0.5 E5:0.5 D5:0.5 C#5:1 A4:0.5 F#4:0.5", "G#4:1 F4:0.5 G#4:0.5 B4:1 C#5:1",
                  "A4:0.5 C#5:0.5 E5:0.5 F#5:0.5 E5:1 C#5:1", "B4:2.5 R:1.5"]
# 2番の Aメロは出だしを変える
M_A3 = ["R:0.5 C#5:0.5 E5:0.5 F#5:0.5 E5:1 C#5:0.5 A4:0.5", "B4:1 E5:0.5 B4:0.5 G#4:1 R:1",
        "R:0.5 A4:0.5 C#5:0.5 E5:0.5 F#5:1 E5:0.5 C#5:0.5", "E5:1.5 C#5:0.5 G#4:1 R:1"] + M_A2[4:]
M_B = ["F#5:1 E5:0.5 D5:0.5 C#5:1 A4:1", "B4:1 G#4:0.5 B4:0.5 E5:2", "E5:0.5 F#5:0.5 G#5:1 E5:1 C#5:1",
       "C#5:1.5 E5:0.5 A5:2", "A5:1 F#5:0.5 D5:0.5 F#5:1 A5:1", "G#5:1 E5:0.5 C#5:0.5 E5:1 G#5:1",
       "A5:1.5 F#5:0.5 A5:2", "B5:2 R:1 G#5:0.5 A5:0.5"]
M_B2 = ["A5:1 F#5:0.5 E5:0.5 D5:1 C#5:1", "B4:0.5 E5:0.5 G#5:0.5 B5:0.5 G#5:2", "E5:0.5 G#5:0.5 B5:1 G#5:1 E5:1",
        "F#5:1.5 E5:0.5 C#5:2"] + M_B[4:]
M_C1 = ["A5:1 F#5:0.5 A5:0.5 C#6:1 A5:0.5 F#5:0.5", "G#5:1.5 F5:0.5 G#5:1 B5:1",
        "A5:1 C#6:0.5 B5:0.5 A5:1 E5:1", "G#5:1.5 E5:0.5 B5:1.5 R:0.5",
        "A5:1 F#5:0.5 A5:0.5 C#6:1 E6:1", "B5:1 G#5:0.5 F5:0.5 G#5:1 C#6:1",
        "C#6:1.5 B5:0.5 A5:1 F#5:1", "E5:1 G5:1 C#6:1.5 R:0.5"]
M_C2 = ["A5:1 F#5:0.5 A5:0.5 C#6:1 A5:0.5 F#5:0.5", "G#5:1.5 F5:0.5 G#5:1 C#6:1",
        "C#6:1 E6:1 C#6:0.5 B5:0.5 A5:1", "B5:1.5 G#5:0.5 E5:2",
        "D6:1 C#6:0.5 B5:0.5 A5:1 F#5:1", "G#5:1 B5:1 E6:1 D6:1", "C#6:3 B5:0.5 A5:0.5", "A5:3 R:1"]
M_BR = ["C#5:2 A4:1 C#5:1", "F#5:2 E5:1 C#5:1", "B4:1.5 G#4:0.5 B4:1 E5:1", "E5:3 R:1",
        "D5:1 F#5:1 A5:1 F#5:1", "E5:1 G#5:1 B5:1 G#5:1", "A5:2 F#5:1 A5:1", "B5:2 R:2"]
SOLO = ["F#5:0.5 A5:0.5 C#6:0.5 E6:0.5 C#6:1 A5:1", "G#5:0.5 B5:0.5 C#6:1 B5:0.5 G#5:0.5 F5:1",
        "E5:0.5 F#5:0.5 A5:0.5 C#6:0.5 E6:1 C#6:1", "B5:2 G#5:1 E5:1",
        "A5:0.25 B5:0.25 C#6:0.25 E6:0.25 D6:1 C#6:0.5 A5:0.5 F#5:1", "F5:0.5 G#5:0.5 B5:0.5 C#6:0.5 B5:1 G#5:1",
        "A5:1 C#6:1 E6:1.5 C#6:0.5", "C#6:2 R:2"]

def f_keys(si, s, pr, k, n):   # エレピの旋律
    if s == "verse": return " ".join([M_A, M_A2, M_A3][n])
    if s == "pre": return " ".join(M_B if n == 0 else M_B2)
    if s == "bridge": return " ".join(M_BR)
    return rest(pr)
def f_piano_mel(si, s, pr, k, n):   # 落ちサビの旋律は生ピアノ（エレピの音域を超えるため）
    if s == "otosabi": return " ".join(M_C1)
    return rest(pr)
def f_lead(si, s, pr, k, n):   # リードギター（warm-lead-a）
    if s == "chorus": return seq(M_C1 if n in (0, 2) else M_C2, k, fold)
    if s == "inter": return seq(M_I, k, fold)
    if s == "solo": return seq(SOLO, k, fold)
    if s == "outro": return seq(M_I[:6] + ["C#6:0.5 E6:0.5 G#5:0.5 A5:0.5 E5:2", "A5:4"], k, fold)
    return rest(pr)
def f_bell(si, s, pr, k, n):
    if s == "intro": return "R:8 " + seq(M_I[2:], k)
    if s == "chorus": return seq(M_C1 if n in (0, 2) else M_C2, k)
    if s == "otosabi": return " ".join(["R:4"] * 4) + " " + seq(M_C1[4:], k)
    return rest(pr)

# ---------------- ピアノ（分散和音） ----------------
P8 = [0, 2, 4, 2, 1, 3, 4, 3]
P16 = [0, 2, 1, 3, 4, 3, 2, 1, 0, 2, 1, 3, 4, 5, 4, 3]
def f_piano(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        t = tones_from(ch, 52); last = i == len(pr) - 1
        if s == "pre" and last: out += [f"{nm(t[0])}:1", f"{nm(t[2])}:1", "R:2"]
        elif s in ("chorus", "solo", "inter") or (s == "pre" and n == 1 and i >= 4): out += [f"{nm(t[j % len(t)])}:0.25" for j in P16]
        elif s in ("bridge", "otosabi"): out += [f"{nm(t[j % len(t)])}:1" for j in (0, 2, 4, 2)]
        elif s == "outro" and last: out += [f"{nm(t[0])}:4"]
        elif s == "intro" and i < 2: out += ["R:4"]
        else: out += [f"{nm(t[j % len(t)])}:0.5" for j in P8]
    return " ".join(out)

# ---------------- クリーンギター（アルペジオ。長めの音） ----------------
def f_clean(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        v = voicing(ch, 60); last = i == len(pr) - 1
        if s == "otosabi" or (s == "verse" and n == 0): out += ["R:4"]
        elif s == "pre" and last: out += [f"{nm(v[0])}:2", "R:2"]
        elif s == "outro" and last: out += [f"{nm(v[1])}:4"]
        else: out += [f"{nm(v[0])}:1", f"{nm(v[1])}:1", f"{nm(v[2])}:1", f"{nm(v[1])}:1"]
    return " ".join(out)

# ---------------- 弦（2声） ----------------
def strings(center, which):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            on = s in ("pre", "chorus", "bridge", "otosabi", "solo", "outro") or (s == "verse" and n >= 1 and i >= 4)
            v = nm(voicing(ch, center)[which])
            if not on: out.append("R:4")
            elif s == "pre" and i == len(pr) - 1: out += [f"{v}:2", "R:2"]
            else: out.append(f"{v}:4")
        return " ".join(out)
    return f

# ---------------- ベース（分数コードは分母の音） ----------------
def f_bass(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = 28 + ((bass_pc(ch) - 28) % 12); a, o, f5 = nm(r), nm(r + 12 if r + 12 <= 50 else r + 7), nm(r + 7)
        nx = pr[i + 1] if i + 1 < len(pr) else ch; rn = 28 + ((bass_pc(nx) - 28) % 12)
        ap = nm(rn - 1 if rn > r else rn + 1) if rn != r else f5
        last = i == len(pr) - 1
        if s == "intro" and i < 4: out += ["R:4"] if i < 2 else [f"{a}:4"]
        elif s == "pre" and last: out += [f"{a}:2", "R:2"]
        elif s == "otosabi": out += [f"{a}:4"]
        elif s == "outro" and last: out += [f"{a}:4"]
        elif s in ("chorus", "solo", "inter"): out += [a + ":1", a + ":0.5", o + ":0.5", a + ":0.5", f5 + ":0.5", a + ":0.5", ap + ":0.5"]
        elif s == "bridge": out += [a + ":2", f5 + ":1", ap + ":1"]
        else: out += [a + ":1.5", a + ":0.5", o + ":1", ap + ":1"]
    return " ".join(out)

# ---------------- ドラム（drumkit.py: 強弱・アクセント・フィル） ----------------
Z = drumkit.Z
def groove(s, n, b, L):
    ride = False; crash = b == 0 and s not in ("intro", "otosabi", "bridge")
    if s == "intro":
        if b < 4: return Z, Z, Z, False, False
        return "X.......X.x.....", "....x.......x...", "X.x.X.x.X.x.X.x.", False, b == 4
    if s == "verse":
        kk = ["X.....x...x.....", "X.....x.X......."][b % 2]
        return kk, "....X......oX..o", ("X.x.X.x.X.x.X.x." if n == 0 else "X.xoX.xoX.xoX.xo"), False, crash
    if s == "pre":
        sn = "....X..oX.o.X.oo" if b == 6 else "....X..o....X..o"
        return "X.....x.X.x.....", sn, ("X.x.X.x.X.x.X.x." if b < 4 else "XxxxXxxxXxxxXxxx"), False, crash
    if s in ("chorus", "solo"):
        kk = ["X...X.x.X...X...", "X...X.x.X.x.X..."][b % 2]; hh = "X.O.X.O.X.O.X.O."
        return kk, "....X......oX..o", hh, ride, crash
    if s == "inter": return "X.....x.X.......", "....X......oX...", "XxxxXxxxXxxxXxxx", False, crash
    if s == "bridge":
        if b < 4: return "X.......X.......", "........X.......", Z, True, b == 0
        return "X.....x.X.......", "....X......oX..o", Z, True, b == 4
    if s == "otosabi":
        if b < 4: return Z, Z, Z, False, False
        if b < 6: return "X.......X.......", Z, "x...x...x...x...", False, False
        return "X...X...X...X...", "....X.......X...", "X.x.X.x.X.x.X.x.", False, b == 6
    if s == "outro":
        if b < 6: return "X.......X.x.....", "....x.......x...", "X.x.X.x.X.x.X.x.", False, b == 0
        if b == 6: return "X...............", Z, Z, False, True
        return Z, Z, Z, False, False
    return Z, Z, Z, False, False
# 転調したサビ（k=1）ではライドで広げる: groove が k を見られるよう、SEC を回しながら k を渡す
_cur = {"k": 0}
def groove_k(s, n, b, L):
    kk, sn, hh, ride, crash = groove(s, n, b, L)
    if s == "chorus" and _cur["k"] == 1 and b in (1, 2, 5, 6): hh, ride = Z, True
    return kk, sn, hh, ride, crash
KICK, SNARE, HAT, CRASH, TOM, RIDE = [], [], [], [], [], []
for _sec in SEC:
    _cur["k"] = _sec[2]
    parts_ = drumkit.build([_sec], groove_k, stops={("solo", 0)}, fills_off={"outro"})
    for acc, got in zip((KICK, SNARE, HAT, CRASH, TOM, RIDE), parts_): acc += got
DG = drumkit.drum_gain(SEC, {"intro": (0.75, 0.85), "verse": (0.78, 0.9), "pre": (0.85, 1.02), "chorus": (0.95, 1.0), "inter": (0.9, 0.95),
                             "bridge": (0.7, 0.85), "solo": (0.95, 1.02), "otosabi": (0.55, 1.0), "outro": (0.9, 0.7)})


# ---------------- カッティング（guitarcut.py。4弦の和音のストローク） ----------------
import guitarcut
def cut_pat(s, n, b):
    if s == "verse" and n >= 1: return "D.xU.UxUD.xU.UxU" if b % 2 == 0 else "D.xU.UxUD.xUxUD."
    if s == "pre": return "D.......--------" if b == 7 else "D.xUD.xUD.xUD.xU"
    if s in ("chorus", "solo"): return "D...xU.UD...xU.U" if b != 7 else "D.xU.UxUD.......".replace("D.......", "D.------")
    if s == "inter": return "D.xU.UxUD.xU.UxU"
    return None
CUT = guitarcut.cut_parts(SEC, chord_pcs, nm, cut_pat)

PARTS = []
def add(inst, role, vol, pan, secs, **kw):
    d = {"instrument": inst, "role": role, "volume": vol, "pan": pan, "notes": cat(secs, role)}; d.update(kw); PARTS.append(d)
A = ARC
DR = -6   # ドラムは -6dB（2026-10-15: 「全体的に少し小さく」の指示で -4 から下げた）
add("keys", "旋律（エレピ）", 0.24, -0.05, per(f_keys), barGain=A, reverb=0.25, gainDb=2)
ACOUSTIC = _os.environ.get("ACOUSTIC") == "1"   # アコギ版（2026-10-15、人間の指示）。旋律のギターを生のアコギにし、1オクターブ下げて弾く
def _oct_down(text): return " ".join(t if t.startswith("R:") else tr(t, -12) for t in text.split())
if ACOUSTIC:
    add("guitar", "旋律（アコギ）", 0.2, 0.08, [_oct_down(x) for x in per(f_lead)], barGain=A, gainDb=5, amp="clean", chorus=0, humanPitch=0, noRestrike=True,
        reverb=0.26, fx=[{"type": "plate", "mix": 0.12}])
else:
    add("leadGuitar", "旋律（リードギター）", 0.16, 0.08, per(f_lead), barGain=A, gainDb=5, guitarTone="warm-lead-a")
add("piano", "旋律（ピアノ・落ちサビ）", 0.2, -0.05, per(f_piano_mel), barGain=A, reverb=0.25, gainDb=2)
add("bell", "きらめき（ベル）", 0.07, 0.35, per(f_bell), barGain=A, reverb=0.32)
add("piano", "ピアノ（分散和音）", 0.15, -0.35, per(f_piano), barGain=A, reverb=0.18)
add("guitar", "アコギ（アルペジオ）" if ACOUSTIC else "クリーンギター", 0.1, 0.65, per(f_clean), barGain=A, amp="clean" if ACOUSTIC else "jpopClean", chorus=0, reverb=0.2, humanPitch=0)
add("strings", "弦（上）", 0.09, 0.55, per(strings(72, 2)), barGain=A, reverb=0.28)
add("strings", "弦（下）", 0.08, -0.55, per(strings(57, 0)), barGain=A, reverb=0.28)
for _i, _name in enumerate(["低", "中低", "中高", "高"]):
    add("guitar", f"カッティング（{_name}い弦）", 0.07, -0.6, CUT[_i], barGain=A, amp="clean" if ACOUSTIC else "jpopClean", chorus=0, reverb=0.12, humanPitch=0, push=round(0.008 * _i, 3))
add("bass", "ベース", 0.3, 0, per(f_bass), barGain=A)
add("kick", "キック", 0.3, 0, KICK, barGain=DG, gainDb=DR)
add("snare", "スネア", 0.26, 0, SNARE, barGain=DG, push=0.02, gainDb=DR)
add("hihat", "ハイハット", 0.08, 0, HAT, barGain=DG, push=-0.008, gainDb=DR)
add("crash", "クラッシュ", 0.1, 0, CRASH, barGain=DG, gainDb=DR)
add("crash", "ライド", 0.07, 0.2, RIDE, barGain=DG, gainDb=DR)
add("tom", "タム", 0.16, 0, TOM, barGain=DG, reverb=0, gainDb=DR)

song = {"title": ("（アコギ版）" if ACOUSTIC else "") + "あの夏のとなり（仮）",
        "description": "（仮）夏を感じる、甘酸っぱい恋にたどり着くようなボカロ風の曲（歌なし）。BPM115・イ長調、最後のサビは半音上の変ロ長調。長7度の和音と C#7 で甘酸っぱく。旋律は Aメロ・Bメロ・ブリッジ・落ちサビがエレピ、サビ・間奏・ソロがリードギター（warm-lead-a）。入り方: 3（クリーンギターのアルペジオだけで2小節→ピアノとベルが入る→5小節目からドラムとベース）。終わり方: 長い和音で静かに。動機: A5:1 F#5:0.5 A5:0.5 C#6:1（サビ頭）。",
        "bpm": 115, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "vocaloid", "human": 0.3, "dynamics": "natural", "autoAccompaniment": False, **({"autoScoop": False} if ACOUSTIC else {}),
        "parts": PARTS}
json.dump({"guitarWobble": False, **song}, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars", round(len(chords) * 4 * 60 / 115), "sec")
