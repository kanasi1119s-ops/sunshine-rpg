# 『夏空ストローク』（仮）: カッティングが主役の、疾走感のある夏の青春ソング（ボカロ風・歌なし）。BPM178・ホ長調、約5分2秒（224小節）。最後のサビ4回分は半音上（ヘ長調）。
# カッティング: 左右に型のちがう2本（左＝まっすぐの16分、右＝裏から入るシンコペ）。4弦のクローズ・ボイシング（guitarcut.py）。ほぼ全編。
#   2回目の間奏はカッティングとドラムだけの見せ場。
# 旋律: Aメロ・Bメロ・ブリッジ・落ちサビは生ピアノ、サビ・リフ・ソロはリードギター（warm-lead-a）。サビはベルを重ねる。ギターのしゃくり・ビブラートなし。
# ドラム: drumkit.py（強弱・アクセント・フィル）。
# 構成: イントロ8 → リフ8 → Aメロ16 → Bメロ8 → サビ16 → リフ8 → Aメロ16 → Bメロ8 → サビ16 → 間奏（カッティング）16 →
#   ブリッジ8 → ソロ16 → 落ちサビ16 → Bメロ8（転調へ） → 半音上のサビ32 → リフ8 → 終わり8
# 使い方: python3 natsuzora-stroke.py <出力.json>（書き出し: --drums jpop --bass finger --piano salamander --orchestra vsco --guitar gretsch --master-preset jpop-band。点数 7.82）
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

import guitarcut, drumkit
# ---------------- コード ----------------
RIFFC = "A B G#m C#m A B E E".split()
VERSE = "E B/D# C#m A E B/D# A B".split()
VERSE2 = "C#m G#m A E F#m G#m A B".split()
PRE = "A B G#m C#m F#m G#m A B".split()
PRE_UP = "A B G#m C#m F#m G#m A C7".split()     # 最後の Bメロ: C7 で半音上（ヘ長調）へ
CHO1 = "A B G#m C#m F#m B E E".split()
CHO2 = "A B G#m C#m F#m G#m A B".split()
BRI = "C#m A E B C#m A F#m B".split()
SEC = [("intro", RIFFC, 0, 0), ("riff", RIFFC, 0, 0),
       ("verse", VERSE, 0, 0), ("verse", VERSE2, 0, 1), ("pre", PRE, 0, 0), ("chorus", CHO1, 0, 0), ("chorus", CHO2, 0, 1),
       ("riff", RIFFC, 0, 1),
       ("verse", VERSE, 0, 2), ("verse", VERSE2, 0, 3), ("pre", PRE, 0, 1), ("chorus", CHO1, 0, 0), ("chorus", CHO2, 0, 1),
       ("cutbreak", RIFFC, 0, 0), ("cutbreak", VERSE, 0, 1),
       ("bridge", BRI, 0, 0), ("solo", VERSE, 0, 0), ("solo", VERSE2, 0, 1),
       ("otosabi", CHO1, 0, 0), ("otosabi", CHO2, 0, 1), ("pre", PRE_UP, 0, 2),
       ("chorus", up(CHO1, 1), 1, 0), ("chorus", up(CHO2, 1), 1, 1), ("chorus", up(CHO1, 1), 1, 2), ("chorus", up(CHO1, 1), 1, 3),
       ("riff", up(RIFFC, 1), 1, 2), ("outro", up(RIFFC, 1), 1, 0)]
chords = [c for _, pr, _, _ in SEC for c in pr]
GAIN = {"intro": .82, "riff": .95, "verse": .84, "pre": .9, "chorus": 1.0, "cutbreak": .92, "bridge": .78, "solo": .98, "otosabi": .7, "outro": .92}
ARC = []
for si, (s, pr, k, n) in enumerate(SEC):
    g = GAIN[s] + (0.03 if si >= 8 and s not in ("otosabi", "bridge") else 0)
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
M_A = ["B4:0.5 G#4:0.5 B4:0.5 E5:0.5 D#5:0.5 B4:0.5 G#4:1", "F#4:0.5 F#4:0.5 G#4:0.5 B4:0.5 D#5:1 B4:1",
       "C#5:0.5 C#5:0.25 C#5:0.25 E5:0.5 C#5:0.5 B4:0.5 G#4:0.5 E4:1", "C#5:1.5 B4:0.5 A4:1 R:1",
       "B4:0.5 E5:0.5 G#5:0.5 F#5:0.5 E5:0.5 B4:0.5 G#4:1", "F#5:0.5 D#5:0.5 B4:0.5 D#5:0.5 F#5:1 D#5:1",
       "C#5:0.5 E5:0.5 A5:1 G#5:0.5 F#5:0.5 E5:1", "F#5:2.5 R:1.5"]
M_A2 = ["E5:0.5 E5:0.5 D#5:0.5 C#5:0.5 G#4:1 C#5:1", "B4:0.5 B4:0.5 C#5:0.5 D#5:0.5 F#5:1 D#5:1",
        "C#5:0.5 E5:0.5 C#5:0.5 A4:0.5 E5:1 C#5:1", "B4:2 G#4:1 R:1",
        "A4:0.5 C#5:0.5 F#5:0.5 E5:0.5 C#5:1 A4:1", "B4:0.5 D#5:0.5 G#5:0.5 F#5:0.5 D#5:1 B4:1",
        "C#5:0.5 E5:0.5 A5:0.5 G#5:0.5 F#5:0.5 E5:0.5 C#5:1", "D#5:2 F#5:1.5 R:0.5"]
M_A3 = ["G#5:0.5 F#5:0.5 E5:0.5 B4:0.5 E5:0.5 F#5:0.5 G#5:1", "F#5:1 D#5:0.5 B4:0.5 F#4:1 R:1",
        "E5:0.5 G#5:0.5 E5:0.5 C#5:0.5 B4:0.5 C#5:0.5 E5:1", "E5:1.5 C#5:0.5 A4:1 R:1"] + M_A[4:]
M_A4 = ["G#5:0.5 G#5:0.5 F#5:0.5 E5:0.5 C#5:1 E5:1", "D#5:0.5 D#5:0.5 E5:0.5 F#5:0.5 B5:1 F#5:1"] + M_A2[2:]
M_P = ["A4:1 C#5:1 E5:1.5 F#5:0.5", "F#5:1 D#5:1 B4:2", "B4:1 D#5:1 G#5:1.5 F#5:0.5", "E5:2 R:1 C#5:0.5 D#5:0.5",
       "E5:1 F#5:0.5 A5:0.5 C#6:1.5 B5:0.5", "B5:1 G#5:0.5 F#5:0.5 D#5:1 F#5:1", "E5:0.5 F#5:0.5 A5:0.5 B5:0.5 C#6:2", "D#6:2 R:1 B5:0.5 C#6:0.5"]
M_P2 = ["C#5:0.5 E5:0.5 A5:1 G#5:1 E5:1", "D#5:0.5 F#5:0.5 B5:1 A5:1 F#5:1", "G#5:1 B5:1 D#6:1.5 C#6:0.5", "C#6:2 R:1 C#5:0.5 D#5:0.5"] + M_P[4:]
M_P_UP = M_P2[:7] + ["E6:2.5 R:1.5"]   # C7 の上（E は C7 の3度）
K1 = ["E6:0.5 C#6:0.5 B5:0.5 A5:0.5 C#6:1 E6:1", "D#6:0.5 C#6:0.5 B5:0.5 F#5:0.5 B5:1 D#6:1",
      "D#6:0.5 B5:0.5 G#5:0.5 B5:0.5 D#6:1 E6:0.5 D#6:0.5", "C#6:2 B5:0.5 G#5:0.5 E5:1",
      "C#6:0.5 A5:0.5 F#5:0.5 A5:0.5 C#6:1 E6:1", "D#6:1 C#6:0.5 B5:0.5 F#5:1 A5:1",
      "G#5:1 B5:0.5 E6:0.5 D#6:1 B5:1", "E6:3 R:1"]
K2 = ["E6:0.5 C#6:0.5 B5:0.5 A5:0.5 E5:1 A5:1", "B5:0.5 C#6:0.5 D#6:0.5 C#6:0.5 B5:1 F#5:1",
      "G#5:0.5 B5:0.5 D#6:0.5 B5:0.5 G#5:1 B5:1", "C#6:1.5 B5:0.5 G#5:1 E5:1",
      "F#5:0.5 A5:0.5 C#6:0.5 E6:0.5 C#6:1 A5:1", "B5:0.5 D#6:0.5 B5:0.5 G#5:0.5 D#6:1 B5:1",
      "C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 C#6:0.5 E6:0.5 C#6:1", "D#6:3 R:1"]
K3 = ["C#6:1 B5:0.5 A5:0.5 E6:1 C#6:1", "B5:1 A5:0.5 F#5:0.5 D#6:1 B5:1"] + K1[2:]   # 3回目は出だしを変える
K_END = K2[:4] + K1[4:7] + ["E6:4"]
RIFF = ["C#6:0.5 B5:0.5 A5:0.5 E5:0.5 A5:0.5 B5:0.5 C#6:1", "D#6:0.5 C#6:0.5 B5:0.5 F#5:0.5 B5:0.5 C#6:0.5 D#6:1",
        "D#6:0.5 C#6:0.5 B5:0.5 G#5:0.5 B5:1 D#6:1", "C#6:2 G#5:1 B5:1",
        "C#6:0.5 B5:0.5 A5:0.5 E5:0.5 A5:0.5 B5:0.5 C#6:1", "D#6:0.5 C#6:0.5 B5:0.5 F#5:0.5 B5:0.5 C#6:0.5 D#6:1",
        "B5:0.5 E6:0.5 D#6:0.5 B5:0.5 G#5:0.5 B5:0.5 E5:1", "E5:3 R:1"]
RIFF_B = RIFF[:4] + ["A5:0.5 C#6:0.5 E6:1 C#6:0.5 A5:0.5 E5:1", "B5:0.5 D#6:0.5 B5:0.5 F#5:0.5 D#6:1 B5:1",
                     "G#5:0.5 B5:0.5 E6:0.5 B5:0.5 G#5:1 B5:1", "E6:3 R:1"]
M_BR = ["G#4:2 C#5:2", "E5:2 C#5:1 A4:1", "B4:1.5 G#4:0.5 E5:2", "D#5:3 R:1", "E5:2 G#5:2", "A5:2 E5:1 C#5:1", "C#5:1 F#5:1 A5:1 F#5:1", "F#5:2 D#5:1 B4:1"]
SOLO1 = ["B5:0.25 C#6:0.25 B5:0.25 G#5:0.25 E5:1 G#5:0.5 B5:0.5 E6:1", "D#6:1 B5:0.5 F#5:0.5 D#6:1 F#5:1",
         "E5:0.5 G#5:0.5 C#6:0.5 E6:0.5 C#6:1 G#5:1", "A5:0.5 C#6:0.5 E6:1 C#6:0.5 A5:0.5 E5:1",
         "G#5:0.25 A5:0.25 B5:0.25 E6:0.25 D#6:0.5 B5:0.5 G#5:1 E5:1", "F#5:0.5 B5:0.5 D#6:1 B5:0.5 F#5:0.5 D#5:1",
         "C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 E5:0.5 A5:0.5 C#6:1", "D#6:2 R:2"]
SOLO2 = ["E6:1 C#6:1 G#5:1 C#6:1", "D#6:0.5 B5:0.5 G#5:0.5 B5:0.5 D#6:2", "C#6:0.5 B5:0.5 A5:0.5 E5:0.5 A5:1 C#6:1", "B5:2 G#5:2",
         "A5:0.5 C#6:0.5 F#5:0.5 A5:0.5 C#6:0.5 E6:0.5 C#6:1", "B5:0.5 D#6:0.5 B5:0.5 G#5:0.5 D#6:2", "C#6:1 A5:1 E5:1 A5:1", "B5:2 R:2"]

def f_piano_mel(si, s, pr, k, n):
    if s == "verse": return " ".join([M_A, M_A2, M_A3, M_A4][n])
    if s == "pre": return " ".join([M_P, M_P2, M_P_UP][n])
    if s == "bridge": return " ".join(M_BR)
    if s == "otosabi": return " ".join(K1 if n == 0 else K2)
    return rest(pr)
def f_lead(si, s, pr, k, n):
    if s == "chorus": return seq(([K1, K2] if k == 0 else [K1, K2, K3, K_END])[n], k, fold)
    if s == "riff": return seq([RIFF, RIFF_B, RIFF][n], k, fold) if n != 1 else " ".join(["R:4"] * 4) + " " + seq(RIFF_B[4:], k, fold)
    if s == "intro": return " ".join(["R:4"] * 2) + " " + seq(RIFF[2:], k, fold)
    if s == "solo": return seq(SOLO1 if n == 0 else SOLO2, k, fold)
    if s == "outro": return seq(RIFF_B[:6] + ["E6:4", "R:4"], k, fold)
    return rest(pr)
def f_bell(si, s, pr, k, n):
    if s == "chorus": return seq(([K1, K2] if k == 0 else [K1, K2, K3, K_END])[n], k)
    if s == "otosabi" and n == 1: return seq(K2, k)
    return rest(pr)

# ---------------- ピアノ（8分の分散和音） ----------------
P8 = [0, 2, 4, 2, 1, 3, 4, 3]
def f_piano(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        t = tones_from(ch, 52); last = i == len(pr) - 1
        if s in ("intro",) and i < 2: out += ["R:4"]
        elif s == "cutbreak": out += ["R:4"]
        elif s == "pre" and last: out += [f"{nm(t[0])}:1", f"{nm(t[2])}:1", "R:2"]
        elif s in ("bridge", "otosabi"): out += [f"{nm(t[j % len(t)])}:1" for j in (0, 2, 4, 2)]
        elif s == "outro" and i >= 6: out += [f"{nm(t[0])}:4"] if i == 6 else ["R:4"]
        else: out += [f"{nm(t[j % len(t)])}:0.5" for j in P8]
    return " ".join(out)

# ---------------- 弦（2声） ----------------
def strings(center, which):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            v = nm(voicing(ch, center)[which])
            on = s in ("pre", "chorus", "bridge", "otosabi", "solo")
            if not on: out.append("R:4")
            elif s == "pre" and i == len(pr) - 1: out += [f"{v}:2", "R:2"]
            else: out.append(f"{v}:4")
        return " ".join(out)
    return f

# ---------------- ベース（ピック。走る8分） ----------------
def f_bass(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = 28 + ((bass_pc(ch) - 28) % 12); a, o, f5 = nm(r), nm(r + 12 if r + 12 <= 50 else r + 7), nm(r + 7)
        nx = pr[i + 1] if i + 1 < len(pr) else ch; rn = 28 + ((bass_pc(nx) - 28) % 12)
        ap = nm(rn - 1 if rn > r else rn + 1) if rn != r else f5
        last = i == len(pr) - 1
        if s == "intro" and i < 2: out += ["R:4"]
        elif s == "pre" and last: out += [f"{a}:1", "R:3"]
        elif s == "otosabi" and n == 0: out += [f"{a}:4"]
        elif s == "bridge": out += [a + ":2", f5 + ":1", ap + ":1"]
        elif s == "outro" and i >= 6: out += [f"{a}:4"] if i == 6 else ["R:4"]
        elif s in ("chorus", "riff", "solo", "cutbreak"): out += [a + ":0.5"] * 3 + [o + ":0.5"] + [a + ":0.5"] * 2 + [f5 + ":0.5", ap + ":0.5"]
        else: out += [a + ":0.5", a + ":0.5", a + ":0.5", a + ":0.5", o + ":0.5", a + ":0.5", f5 + ":0.5", ap + ":0.5"]
    return " ".join(out)

# ---------------- カッティング（左右2本） ----------------
def cut_L(s, n, b):
    last = b == 7
    if s == "intro": return "D.xUxUD.xUxUD.xU" if b < 7 else "D.xUD.xUD.------"
    if s in ("verse",): return "D.xUxUD.xUxUD.xU" if not last else "D.xUxUD.xUD.----"
    if s == "pre": return "D.......--------" if last else "DxUxDxUxDxUxDxUx"
    if s in ("chorus", "riff", "solo"): return "D.xUD.xUD.xUD.xU" if not last else "D.xUD.xUD.------"
    if s == "cutbreak": return ["DxxUxxDxxUDxUxDx", "D.xUxUD.xUxUD.xU"][b % 2] if not last else "DxUxDxUxD.------"
    if s == "bridge": return "D.......D......."
    if s == "otosabi": return None if n == 0 else ("D.......D......." if b < 6 else "D.xUD.xUD.xUD.xU")
    if s == "outro": return "D.xUD.xUD.xUD.xU" if b < 6 else ("D..............." if b == 6 else None)
    return None
def cut_R(s, n, b):
    last = b == 7
    if s == "intro": return None
    if s == "verse": return ("--D.--D.--D.--D." if n in (0, 2) else "xxD.xxD.xxD.xxDx") if not last else "--D.--D.D.------"
    if s == "pre": return "D.......--------" if last else "xD.UxD.UxD.UxD.U"
    if s in ("chorus", "riff", "solo"): return "xxDxxDxxDxxDxxDx" if not last else "xxDxxDxxD.------"
    if s == "cutbreak": return ["xxDxxDxxDxxDxxDx", "--D.--D.--D.--D."][b % 2] if not last else "xxDxxDxxD.------"
    if s == "otosabi": return None if n == 0 else (None if b < 6 else "xxDxxDxxDxxDxxDx")
    if s == "outro": return "xxDxxDxxDxxDxxDx" if b < 6 else ("D..............." if b == 6 else None)
    return None
CUT_L = guitarcut.cut_parts(SEC, chord_pcs, nm, cut_L)
CUT_R = guitarcut.cut_parts(SEC, chord_pcs, nm, cut_R, lo=60)   # 右は1段高い形（C4〜B4）で、左と聞き分けやすく

# ---------------- ドラム（drumkit.py） ----------------
Z = drumkit.Z
_cur = {"k": 0}
def groove(s, n, b, L):
    crash = b == 0 and s not in ("intro", "otosabi", "bridge")
    if s == "intro":
        if b < 2: return Z, Z, Z, False, False
        return "X..X..X...X.X...", "....X......oX...", "X.x.X.x.X.x.X.x.", False, b == 2
    if s == "verse":
        kk = ["X..X..X...X.X...", "X..X..X.X...X..."][b % 2]
        return kk, "....X......oX...", ("X.x.X.x.X.x.X.x." if n in (0, 1) else "XxxxXxxxXxxxXxxx"), False, crash and n in (0, 2)
    if s == "pre": return "X...X...X...X...", "....X.......X..o", ("X.x.X.x.X.x.X.x." if b < 4 else "XxxxXxxxXxxxXxxx"), False, crash
    if s in ("chorus", "riff", "solo"):
        kk = ["X..X..X...X.X...", "X..X..X.X.X.X..."][b % 2]; hh = "X.O.X.O.X.O.X.O."; ride = False
        if (s == "chorus" and _cur["k"] == 1 and b in (1, 2, 5, 6)) or (s == "solo" and b % 2 == 1): hh, ride = Z, True
        return kk, "....X......oX...", hh, ride, crash
    if s == "cutbreak": return "X..X..X...X.X...", "....X......oX...", "XxxxXxxxXxxxXxxx", False, crash
    if s == "bridge":
        if b < 4: return "X.......X.......", "........X.......", Z, True, b == 0
        return "X..X..X...X.X...", "....X......oX...", Z, True, b == 4
    if s == "otosabi":
        if n == 0: return Z, Z, Z, False, False
        if b < 4: return "X.......X.......", Z, "x...x...x...x...", False, b == 0
        return "X...X...X...X...", "....X.......X...", "X.x.X.x.X.x.X.x.", False, False
    if s == "outro":
        if b < 6: return "X..X..X...X.X...", "....X......oX...", "X.O.X.O.X.O.X.O.", False, b == 0
        if b == 6: return "X...............", "X...............", Z, False, True
        return Z, Z, Z, False, False
    return Z, Z, Z, False, False
KICK, SNARE, HAT, CRASH, TOM, RIDE = [], [], [], [], [], []
for _sec in SEC:
    _cur["k"] = _sec[2]
    got = drumkit.build([_sec], groove, stops={("solo", 1)} , fills_off={"outro"})
    for acc, g in zip((KICK, SNARE, HAT, CRASH, TOM, RIDE), got): acc += g
DG = drumkit.drum_gain(SEC, {"intro": (0.8, 0.9), "riff": (0.95, 1.0), "verse": (0.8, 0.9), "pre": (0.85, 1.03), "chorus": (0.95, 1.0),
                             "cutbreak": (0.9, 1.0), "bridge": (0.7, 0.85), "solo": (0.95, 1.02), "otosabi": (0.55, 0.95), "outro": (0.9, 0.75)})

PARTS = []
def add(inst, role, vol, pan, secs, **kw):
    d = {"instrument": inst, "role": role, "volume": vol, "pan": pan, "notes": cat(secs, role)}; d.update(kw); PARTS.append(d)
A = ARC
DR = -8   # ドラムは -8dB（点数の試行で決めた）
add("piano", "旋律（ピアノ）", 0.22, -0.05, per(f_piano_mel), barGain=A, reverb=0.2, gainDb=2)
add("leadGuitar", "旋律（リードギター）", 0.16, 0.08, per(f_lead), barGain=A, gainDb=7, guitarTone="warm-lead-a")
add("bell", "きらめき（ベル）", 0.06, 0.3, per(f_bell), barGain=A, reverb=0.3)
add("piano", "ピアノ（分散和音）", 0.13, -0.3, per(f_piano), barGain=A, reverb=0.15)
for _i, _name in enumerate(["低", "中低", "中高", "高"]):
    add("guitar", f"カッティング左（{_name}い弦）", 0.08, -0.75, CUT_L[_i], barGain=A, amp="jpopClean", chorus=0, reverb=0.1, humanPitch=0, push=round(0.008 * _i, 3))
for _i, _name in enumerate(["低", "中低", "中高", "高"]):
    add("guitar", f"カッティング右（{_name}い弦）", 0.075, 0.75, CUT_R[_i], barGain=A, amp="jpopClean", chorus=0, reverb=0.1, humanPitch=0, push=round(0.006 + 0.008 * _i, 3))
add("strings", "弦（上）", 0.08, 0.55, per(strings(72, 2)), barGain=A, reverb=0.26)
add("strings", "弦（下）", 0.07, -0.55, per(strings(57, 0)), barGain=A, reverb=0.26)
add("bass", "ベース（ピック）", 0.3, 0, per(f_bass), barGain=A)
add("kick", "キック", 0.3, 0, KICK, barGain=DG, gainDb=DR)
add("snare", "スネア", 0.26, 0, SNARE, barGain=DG, push=0.015, gainDb=DR)
add("hihat", "ハイハット", 0.08, 0, HAT, barGain=DG, push=-0.008, gainDb=DR)
add("crash", "クラッシュ", 0.1, 0, CRASH, barGain=DG, gainDb=DR)
add("crash", "ライド", 0.07, 0.2, RIDE, barGain=DG, gainDb=DR)
add("tom", "タム", 0.16, 0, TOM, barGain=DG, reverb=0, gainDb=DR)

song = {"title": "夏空ストローク（仮）",
        "description": "（仮）カッティングが主役の、疾走感のある夏の青春ソング（ボカロ風・歌なし）。BPM178・ホ長調、最後のサビ4回分は半音上のヘ長調。カッティングは左右に型のちがう2本（4弦のクローズ・ボイシング）で、2回目の間奏はカッティングとドラムだけの見せ場。旋律は Aメロ・Bメロ・ブリッジ・落ちサビが生ピアノ、サビ・リフ・ソロがリードギター（warm-lead-a）。ドラムは強弱・アクセント・フィル（drumkit.py）。入り方: 2（左のカッティングだけで2小節→全員でリフ）。終わり方: 全員で一発止め。動機: E6:0.5 C#6:0.5 B5:0.5 A5:0.5 C#6:1（サビ頭）。",
        "bpm": 178, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "vocaloid", "human": 0.25, "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False,
        "parts": PARTS}
json.dump(song, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars", round(len(chords) * 4 * 60 / 178), "sec")
