# 『ネオンハートビート』（仮）: ボカロ曲のようなインスト。約5分。BPM172・ロ短調（最後のサビ4回分は半音上のハ短調）。
# 2026-10-15 改訂: シンセのリードは外した（人間の指示）。旋律は A・Bメロ・落ちサビがピアノ、サビ・間奏・ブリッジ・ソロがリードギター
#   （distortion アンプ。ビブラートなし・チョーキングは少しだけ）。サビは FM ベルを重ねてきらめかせる。
# 伴奏: 16分で走るピアノ、動くベース、歪みギターの刻み（左右）、左右の弦、サビの厚いシンセ（unisonSaw）、生ドラム（-7dB）。
# 構成（216小節）: イントロ8 → リフ8 → Aメロ16 → Bメロ8 → サビ16 → リフ8 → Aメロ16 → Bメロ8 → サビ16 → リフ8 →
#   ブリッジ16 → ギターソロ16 → 落ちサビ16 → Bメロ8（最後に G7 で転調の準備）→ 半音上のサビ32 → リフ8 → 終わり8
# 使い方: python3 neon-heartbeat.py <出力.json>
import json, re, sys

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
def fold(tok, hi=88):  # リードギターの音域（〜E6）を超える音は1オクターブ下げる。ビブラート（~）は付けない
    if tok.startswith("R:"): return tok
    n_, rest_ = tok.split(":", 1); m = midi(n_)
    return nm(m - 12 if m > hi else m) + ":" + rest_.replace("~", "")
def seq(lst, k=0, f=lambda x: x): return " ".join(f(tr(x, k)) for x in " ".join(lst).split())

# ---------------- コード ----------------
INTRO = "Gmaj7 A F#m7 Bm Gmaj7 A F#m7 Bm".split()
INTRO_UP = "Abmaj7 Bb Gm7 Cm Abmaj7 Bb Gm7 Cm".split()
VERSE = "Bm G D A Bm G Em F#7".split()
PRE = "Em F#m G A Em F#m G A".split()
PRE_UP = "Em F#m G A Em F#m G G7".split()    # 最後の Bメロ: G7 で半音上（ハ短調）へ
CHO = "G A F#m Bm G A Bm Bm".split()
CHO_UP = "Ab Bb Gm Cm Ab Bb Cm Cm".split()
BRI0 = "Em Bm Cmaj7 D Em Bm Cmaj7 D".split()
BRI1 = "Em Bm Cmaj7 D Em Bm Cmaj7 F#7".split()
OUT = "Abmaj7 Bb Gm Cm Abmaj7 Bb Gm Cm".split()
# (名前, コード, 転調の半音, 何回目か)
SEC = [("intro", INTRO, 0, 0), ("riff", INTRO, 0, 0),
       ("verse", VERSE, 0, 0), ("verse", VERSE, 0, 1), ("pre", PRE, 0, 0), ("chorus", CHO, 0, 0), ("chorus", CHO, 0, 1),
       ("riff", INTRO, 0, 1),
       ("verse", VERSE, 0, 2), ("verse", VERSE, 0, 3), ("pre", PRE, 0, 1), ("chorus", CHO, 0, 0), ("chorus", CHO, 0, 1),
       ("riff", INTRO, 0, 2),
       ("bridge", BRI0, 0, 0), ("bridge", BRI1, 0, 1), ("solo", VERSE, 0, 0), ("solo", VERSE, 0, 1),
       ("otosabi", CHO, 0, 0), ("otosabi", CHO, 0, 1), ("pre", PRE_UP, 0, 2),
       ("chorus", CHO_UP, 1, 2), ("chorus", CHO_UP, 1, 1), ("chorus", CHO_UP, 1, 2), ("chorus", CHO_UP, 1, 3),
       ("riff", INTRO_UP, 1, 3), ("outro", OUT, 1, 0)]
chords = [c for _, pr, _, _ in SEC for c in pr]
GAIN = {"intro": .8, "riff": .92, "verse": .82, "pre": .9, "chorus": 1.0, "bridge": .88, "solo": .97, "otosabi": .7, "outro": .95}
ARC = []
for si, (s, pr, k, n) in enumerate(SEC):
    g = GAIN[s] + (0.03 if si >= 8 and s not in ("otosabi", "bridge") else 0) + (0.12 if s == "otosabi" and n == 1 else 0)
    ARC += [round(min(1.05, g + (0.05 * i / len(pr) if s in ("pre",) or (s == "otosabi" and n == 1) else 0)), 3) for i in range(len(pr))]

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
def root_in(ch, lo): return lo + ((chord_pcs(ch)[0] - lo) % 12)

# ---------------- 旋律 ----------------
M_A = ["B4:0.5 B4:0.5 C#5:0.5 D5:0.5 C#5:0.5 B4:0.5 F#4:1", "R:0.5 G4:0.5 A4:0.5 B4:0.5 D5:1 B4:0.5 A4:0.5",
       "A4:0.5 A4:0.25 A4:0.25 B4:0.5 A4:0.5 F#4:0.5 E4:0.5 D4:1", "E4:0.5 F#4:0.5 A4:1 C#5:1.5 R:0.5",
       "B4:0.5 B4:0.5 C#5:0.5 D5:0.5 E5:0.5 D5:0.5 C#5:0.5 B4:0.5", "D5:0.5 B4:0.5 G4:0.5 B4:0.5 D5:1 E5:0.5 F#5:0.5",
       "G5:1 F#5:0.5 E5:0.5 D5:0.5 B4:0.5 G4:0.5 B4:0.5", "A#4:1.5 C#5:0.5 F#5:1.5 R:0.5"]
M_A2 = M_A[:4] + ["B4:0.5 D5:0.5 F#5:0.5 E5:0.5 D5:0.5 C#5:0.5 B4:0.5 D5:0.5", "G5:0.5 F#5:0.5 D5:0.5 B4:0.5 D5:1 E5:0.5 F#5:0.5",
                  "G5:0.5 A5:0.5 G5:0.5 F#5:0.5 E5:0.5 D5:0.5 B4:0.5 E5:0.5", "F#5:1.5 E5:0.5 C#5:1.5 R:0.5"]
# 2番の A メロは出だしを変える
M_A3 = ["F#5:0.5 F#5:0.5 E5:0.5 D5:0.5 C#5:0.5 B4:0.5 C#5:1", "R:0.5 B4:0.5 D5:0.5 G5:0.5 F#5:1 D5:0.5 B4:0.5",
        "A4:0.5 D5:0.5 F#5:0.5 E5:0.5 D5:0.5 A4:0.5 F#4:1", "E4:0.5 A4:0.5 C#5:1 E5:1.5 R:0.5"] + M_A[4:]
M_B = ["E5:1 D5:0.5 E5:0.5 G5:1 E5:1", "F#5:1 E5:0.5 C#5:0.5 A4:1 C#5:1", "D5:0.5 D5:0.5 E5:0.5 F#5:0.5 G5:1 A5:1",
       "A5:2 R:1 E5:0.5 F#5:0.5", "G5:1 F#5:0.5 E5:0.5 B4:1 E5:1", "A5:1 G#5:0.5 F#5:0.5 C#5:1 F#5:1",
       "B5:1 A5:0.5 G5:0.5 D5:0.5 G5:0.5 A5:0.5 B5:0.5", "C#6:2.5 R:1.5"]
M_B_UP = ["E5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5 E5:1", "F#5:0.5 A5:0.5 C#6:1 B5:0.5 A5:0.5 F#5:1",
          "G5:0.5 B5:0.5 D6:0.5 B5:0.5 A5:1 B5:1", "C#6:2 R:1 A5:0.5 B5:0.5"] + M_B[4:7] + ["D6:2.5 R:1.5"]   # 3回目の Bメロ（最後は G7 の上）
M_C = ["B5:0.5 A5:0.5 B5:0.5 D6:1 B5:0.5 A5:0.5 G5:0.5", "A5:1 E5:0.5 F#5:0.5 A5:0.5 C#6:1 A5:0.5",
       "C#6:0.5 B5:0.5 A5:0.5 F#5:1 E5:0.5 F#5:0.5 A5:0.5", "B5:2.5 R:0.5 F#5:0.5 A5:0.5",
       "B5:0.5 A5:0.5 B5:0.5 D6:1 B5:0.5 A5:0.5 G5:0.5", "A5:1 B5:0.5 C#6:0.5 E6:1 C#6:0.5 A5:0.5",
       "D6:1 C#6:0.5 B5:0.5 A5:0.5 F#5:0.5 A5:0.5 B5:0.5", "B5:3 R:1"]
M_C2 = ["B5:0.5 A5:0.5 B5:0.5 D6:0.5 E6:0.5 D6:0.5 B5:0.5 G5:0.5", "A5:1 E5:0.5 F#5:0.5 A5:0.5 C#6:0.5 E6:0.5 C#6:0.5",
        M_C[2], "B5:2 R:1 D6:0.5 C#6:0.5"] + M_C[4:6] + ["D6:1 C#6:0.5 D6:0.5 E6:1 C#6:1", "B5:4"]   # サビ後半（前半を少し変える）
M_C_LAST = M_C2[:4] + M_C[4:6] + ["D6:1 E6:0.5 F#6:0.5 E6:1 D6:1", "B5:4"]
RIFF = ["B5:0.5 D6:0.5 B5:0.5 A5:0.5 G5:1 A5:0.5 B5:0.5", "C#6:0.5 A5:0.5 E5:0.5 A5:0.5 C#6:1 E6:1",
        "C#6:0.5 A5:0.5 F#5:0.5 A5:0.5 C#6:1 B5:0.5 A5:0.5", "B5:2 F#5:1 D5:1",
        "B5:0.5 D6:0.5 B5:0.5 A5:0.5 G5:1 A5:0.5 B5:0.5", "C#6:0.5 A5:0.5 E5:0.5 A5:0.5 C#6:1 E6:1",
        "C#6:0.5 E6:0.5 D6:0.5 C#6:0.5 B5:1 A5:0.5 F#5:0.5", "B5:3 R:1"]
M_BR0 = ["E5:0.25 F#5:0.25 G5:0.25 B5:0.25 E6:1 D6:0.5 B5:0.5 G5:1", "F#5:0.5 D5:0.5 B4:0.5 D5:0.5 F#5:1 B5:1",
         "G5:0.25 A5:0.25 B5:0.25 C6:0.25 E6:1 D6:0.5 C6:0.5 B5:1", "A5:0.5 F#5:0.5 D5:0.5 F#5:0.5 A5:1 D6:1",
         "E6:1 D6:0.5 B5:0.5 G5:0.5 B5:0.5 E5:1", "D6:1 B5:0.5 F#5:0.5 D5:1 F#5:1",
         "E6:0.5 D6:0.5 C6:0.5 B5:0.5 G5:0.5 E5:0.5 G5:0.5 B5:0.5", "A5:0.5 D6:0.5 F#5:0.5 A5:0.5 D6:2"]
M_BR1 = ["G5:0.5 B5:0.5 E6:1 D6:0.5 B5:0.5 G5:1", "F#5:1 B5:0.5 D6:0.5 C#6:1 B5:1",
         "E5:0.5 G5:0.5 C6:0.5 E6:0.5 D6:1 C6:1", "A5:1.5 F#5:0.5 D6:2",
         "E6:0.5 D6:0.5 B5:0.5 G5:0.5 E5:0.5 G5:0.5 B5:0.5 D6:0.5", "D6:1 C#6:0.5 B5:0.5 F#5:1 B5:1",
         "C6:0.5 B5:0.5 G5:0.5 E5:0.5 G5:0.5 C6:0.5 E6:1", "C#6:1 A#5:1 F#5:1 R:1"]
SOLO0 = ["F#5:0.5 B5:0.5 D6:0.5 B5:0.5 A5:1^^ F#5:1", "G5:0.25 A5:0.25 B5:0.25 D6:0.25 E6:1 D6:0.5 B5:0.5 G5:1",
         "F#5:0.5 A5:0.5 D6:1 C#6:0.5 A5:0.5 F#5:1", "E5:0.5 A5:0.5 C#6:0.5 E6:0.5 B5:1^^ C#6:1",
         "B5:0.25 C#6:0.25 D6:0.25 E6:0.25 D6:0.5 B5:0.5 F#5:1 B5:1", "D6:0.5 B5:0.5 G5:0.5 B5:0.5 D6:1 E6:1",
         "E6:0.5 D6:0.5 B5:0.5 G5:0.5 E5:0.25 G5:0.25 B5:0.25 E6:0.25 D6:1", "C#6:1.5 A#5:0.5 F#5:2"]
SOLO1 = ["B5:2^^ A5:0.5 F#5:0.5 D5:1", "D5:0.5 G5:0.5 B5:0.5 D6:0.5 E6:2",
         "D6:0.5 C#6:0.5 A5:0.5 F#5:0.5 A5:0.5 D6:0.5 F#5:1", "E5:0.25 F#5:0.25 A5:0.25 C#6:0.25 E6:3",
         "D6:1 C#6:0.5 B5:0.5 F#5:0.5 B5:0.5 D6:1", "E6:0.5 D6:0.5 B5:0.5 G5:0.5 B5:1 D6:1",
         "G5:0.5 B5:0.5 E6:1 D6:0.5 B5:0.5 G5:1", "A#5:1 C#6:1 E6:1 R:1"]

RIFF_B = RIFF[:4] + ["D6:0.5 B5:0.5 G5:0.5 B5:0.5 D6:1 E6:1", "E6:0.5 C#6:0.5 A5:0.5 C#6:0.5 E6:1 C#6:1",
                     "A5:0.5 C#6:0.5 F#5:0.5 A5:0.5 C#6:1 B5:0.5 A5:0.5", "B5:2 D6:1 B5:1"]   # 3回目のリフは後半を変える
def f_piano_mel(si, s, pr, k, n):
    if s == "intro": return "R:16 " + " ".join(M_C[:3]) + " B5:2 R:2"
    if s == "verse": return " ".join([M_A, M_A2, M_A3, M_A3[:4] + M_A2[4:]][n])
    if s == "pre": return " ".join(M_B_UP if n == 2 else M_B)
    if s == "otosabi": return " ".join(M_C if n == 0 else M_C2)
    return rest(pr)
def f_gtr_mel(si, s, pr, k, n):
    if s == "chorus": return seq([M_C, M_C2, M_C, M_C_LAST][n], k, fold)
    if s == "riff": return seq(RIFF_B if n == 2 else RIFF, k, fold) if n != 1 else " ".join(["R:4"] * 4) + " " + seq(RIFF[4:], k, fold)
    if s == "bridge": return seq(M_BR0 if n == 0 else M_BR1, 0, fold)
    if s == "solo": return seq(SOLO0 if n == 0 else SOLO1, 0, fold)
    if s == "outro": return seq(["C6:4", "D6:4", "D6:4", "C6:4", "R:16"], 0, fold)
    return rest(pr)
def f_bell(si, s, pr, k, n):
    if s == "chorus": return seq([M_C, M_C2, M_C, M_C_LAST][n], k)
    if s == "otosabi" and n == 1: return seq(M_C2, k)
    if s == "intro": return "R:16 " + " ".join(M_C[:3]) + " B5:2 R:2"
    return rest(pr)

# ---------------- ピアノ（16分の分散和音） ----------------
PAT = [0, 2, 1, 3, 4, 3, 2, 1, 0, 2, 1, 3, 4, 5, 4, 3]
def f_piano(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        t = tones_from(ch, 55); last = i == len(pr) - 1
        if s == "pre" and last: out += [f"{nm(t[0])}:0.25", f"{nm(t[2])}:0.25", f"{nm(t[4])}:0.5", "R:3"]
        elif s == "bridge" and n == 0 and i < 4: out += [f"{nm(t[j % len(t)])}:0.5" for j in (0, 2, 4, 2, 0, 2, 4, 2)]
        elif s == "otosabi" and n == 0: out += [f"{nm(t[j % len(t)])}:1" for j in (0, 2, 4, 2)]
        elif s == "outro" and i >= 4: out += [f"{nm(t[0])}:4"] if i < 7 else ["R:4"]
        else: out += [f"{nm(t[j % len(t)])}:0.25" for j in PAT]
    return " ".join(out)

# ---------------- ギターの刻み（歪み・左右） ----------------
def f_rhythm(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = nm(root_in(ch, 40)); last = i == len(pr) - 1
        if s == "intro" and i < 4: out += ["R:4"]
        elif (s == "verse" and n in (0, 1)) or s == "otosabi" and n == 0: out += ["R:4"]
        elif s == "verse": out += [f"{r}:1.5", f"{r}:0.5", f"{r}:1", f"{r}:1"]
        elif s == "otosabi": out += [f"{r}:2", f"{r}:2"]
        elif s == "pre" and last: out += [f"{r}:1", "R:3"]
        elif s == "outro" and i >= 4: out += [f"{r}:4"] if i < 7 else ["R:4"]
        else: out += [f"{r}:0.5"] * 8
    return " ".join(out)

# ---------------- 弦・厚いシンセ（2声） ----------------
def pad(center, which, sections):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            if s in sections:
                v = nm(voicing(ch, center)[which])
                out += [f"{v}:1", "R:3"] if (s == "pre" and i == len(pr) - 1) else ([f"{v}:4"] if not (s == "outro" and i == 7) else ["R:4"])
            else: out.append("R:4")
        return " ".join(out)
    return f

# ---------------- ベース ----------------
def f_bass(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = root_in(ch, 28); a, o, f5 = nm(r), nm(r + 12), nm(r + 7)
        nx = pr[i + 1] if i + 1 < len(pr) else ch; rn = root_in(nx, 28)
        ap = nm(rn - 1 if rn > r else rn + 1) if rn != r else f5
        last = i == len(pr) - 1
        if s == "intro" and i < 4: out += ["R:4"]
        elif s == "pre" and last: out += [f"{a}:1", "R:3"]
        elif s == "otosabi" and n == 0: out += [f"{a}:4"]
        elif s == "outro" and i >= 4: out += [f"{a}:4"] if i < 7 else ["R:4"]
        elif s in ("chorus", "intro", "riff", "solo"):
            out += [a + ":0.5", a + ":0.5", o + ":0.5", a + ":0.5", a + ":0.5", o + ":0.5", f5 + ":0.5", ap + ":0.5"] if i % 4 != 3 else \
                   [a + ":0.5", o + ":0.5", a + ":0.5", o + ":0.5", f5 + ":0.25", o + ":0.25", f5 + ":0.25", a + ":0.25", ap + ":1"]
        elif s == "bridge": out += [a + ":1.5", a + ":0.5", o + ":1", ap + ":1"]
        else: out += [a + ":0.75", a + ":0.75", o + ":0.5", a + ":0.5", f5 + ":0.5", o + ":0.5", ap + ":0.5"]
    return " ".join(out)

# ---------------- ドラム ----------------
Z = "................"
def tomtok(tm):
    pit = ["E3", "E3", "C3", "C3", "A2", "A2"]; hits = [j for j, c in enumerate(tm) if c in "xX"]; toks = []; kk = 0
    for c in tm:
        if c in "xX": toks.append(pit[min(5, kk * 6 // len(hits))] + ":0.25" + ("!" if c == "X" else "")); kk += 1
        else: toks.append("R:0.25")
    return toks
CHO_K = ["X..xX..xX..xX..x", "X..xX...X..xX.x."]
KICK, SNARE, HAT, CRASH, TOM, RIDE = [], [], [], [], [], []
for si, (s, pr, k, n) in enumerate(SEC):
    kb, sb, hb, cb, tb, rb = [], [], [], [], [], []
    L = len(pr)
    for b in range(L):
        last = b == L - 1; cr = "R:4"; ride = False; tm = None
        if s == "intro":
            if b < 4: kk, sn, hh = Z, Z, Z
            else:
                kk = "X..x..X...x.X..."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.O."
                if b == 4: cr = "g:X..............."
                if last: sn = "....X...xxxxXXXX"; tm = "............xxXX"
            if b == 3: sn = "........x.x.xxXX"
        elif s == "riff":
            kk = CHO_K[b % 2]; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O." if n != 1 else "x.x.x.x.x.x.x.x."
            if n == 1 and b < 4: kk = "X.......X.x....."; sn = Z if b < 2 else "....X.......X..."; hh = "xxxxxxxxxxxxxxxx"
            if b % 4 == 0: cr = "g:X..............."
            if last: sn = "....X...xxxxXXXX"; tm = "............xxXX"
        elif s == "verse":
            kk = "X..x..X...x.X..." if b % 2 == 0 else "X..x..X...X..x.."; sn = "....X.......X..."
            hh = "x.x.x.x.x.x.x.O." if n in (0, 1) else "xxx.xxx.xxx.xxO."
            if b == 0 and n in (0, 2): cr = "g:X..............."
            if b == 3: sn = "....X.......X.o."
            if last: sn = "....X.......xxXX" if n in (1, 3) else "....X.......X.o."
        elif s == "pre":
            kk = "X...X..xX...X..x"; sn = "....X..o....X..o"; hh = "xxxxxxxxxxxxxxxx"
            if b == 0: cr = "g:X..............."
            if b == 6: sn = "....X.x.X.x.XxXx"
            if last: kk = "X..............."; sn = Z; hh = Z; cr = "g:X..............."
        elif s == "chorus":
            kk = CHO_K[b % 2]; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."
            if b % 4 == 0: cr = "g:X..............."
            if b == 3: sn = "....X.......X.xx"
            if k == 1 and b in (1, 2, 5, 6): hh = Z; ride = True     # 半音上のサビはライドで広げる
            if last: sn = "....X...xxxxXXXX"; tm = "........xx..xxXX"
            if last and n == 1 and si in (6, 12): sn = "....X...xxxxXXXX"
        elif s == "bridge":
            if n == 0 and b < 4: kk = "X.......X......."; sn = "........X......."; hh = "x...x...x...x..."
            else: kk = CHO_K[b % 2]; sn = "....X.......X..."; hh = Z; ride = True
            if b in (0, 4): cr = "g:X..............."
            if last and n == 1: kk = "X...X...X...X..."; sn = "xxxxxxxxXXXXXXXX"; hh = Z; ride = False
        elif s == "solo":
            kk = CHO_K[b % 2]; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."
            if b % 4 == 0: cr = "g:X..............."
            if last: sn = "....X...xxxxXXXX"; tm = "........xx..xxXX"
            if last and n == 1: kk = "X..............."; sn = "X..............."; hh = Z; tm = None   # 落ちサビの前で止める
        elif s == "otosabi":
            if n == 0: kk, sn, hh = Z, Z, Z
            else:
                kk = "X.......X......." if b < 4 else "X...X...X...X..."; sn = Z if b < 4 else "....X.......X..."
                hh = "x...x...x...x..." if b < 4 else "x.x.x.x.x.x.x.x."
                if b == 6: sn = "....X...x.x.x.x."
                if last: sn = "x.x.x.x.xxxxXXXX"; tm = "............xxXX"
        elif s == "outro":
            if b < 4: kk = CHO_K[b % 2]; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."
            elif b < 7: kk = "X..............." if b == 4 else Z; sn = Z; hh = Z
            else: kk, sn, hh = Z, Z, Z
            if b in (0, 4): cr = "g:X..............."
        if cr != "R:4": hh = "." + hh[1:]
        if tm:
            first = next(j for j, c in enumerate(tm) if c in "xX")
            hh = hh[:first] + "." * (16 - first)
        kb.append("g:" + kk); sb.append("g:" + sn); hb.append("g:" + hh); cb.append(cr)
        rb += ["D2:0.5"] * 8 if ride else ["R:4"]
        tb += tomtok(tm) if tm else ["R:4"]
    KICK.append(kb); SNARE.append(sb); HAT.append(hb); CRASH.append(cb); TOM.append(tb); RIDE.append(rb)

PARTS = []
def add(inst, role, vol, pan, secs, **kw):
    d = {"instrument": inst, "role": role, "volume": vol, "pan": pan, "notes": cat(secs, role)}; d.update(kw); PARTS.append(d)
A = ARC
DR = -7   # ドラムは -7dB（点数の試行で決めた。docs/sound/listening-toolkit.md）
add("piano", "旋律（ピアノ）", 0.22, -0.05, per(f_piano_mel), barGain=A, reverb=0.18, gainDb=2)
add("leadGuitar", "旋律（リードギター）", 0.16, 0.08, per(f_gtr_mel), barGain=A, amp="distortion", ampDrive=0.8, chorus=0, reverb=0.18, gainDb=3,
    fx=[{"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}])
add("fmBell", "きらめき（FMベル）", 0.07, 0.3, per(f_bell), barGain=A, reverb=0.3)
add("piano", "ピアノ（16分）", 0.15, -0.3, per(f_piano), barGain=A, reverb=0.15)
add("distGuitar", "ギター（左）", 0.07, -0.85, per(f_rhythm), barGain=A, amp="hardrock", ampDrive=0.9, ampTone=-3, chorus=0, reverb=0.1)
add("distGuitar", "ギター（右）", 0.07, 0.85, per(f_rhythm), barGain=A, amp="hardrock", ampDrive=0.9, ampTone=-3, chorus=0, reverb=0.1, push=0.008)
STR = ("pre", "chorus", "bridge", "otosabi", "solo", "outro")
add("strings", "弦（上）", 0.09, 0.6, per(pad(70, 2, STR)), barGain=A, reverb=0.25)
add("strings", "弦（下）", 0.08, -0.6, per(pad(58, 0, STR)), barGain=A, reverb=0.25)
add("unisonSaw", "厚いシンセ（上）", 0.06, 0.45, per(pad(66, 1, ("chorus", "riff"))), barGain=A, reverb=0.2)
add("unisonSaw", "厚いシンセ（下）", 0.06, -0.45, per(pad(62, 0, ("chorus", "riff"))), barGain=A, reverb=0.2)
add("bass", "ベース", 0.32, 0, per(f_bass), barGain=A)
add("kick", "キック", 0.3, 0, KICK, barGain=A, gainDb=DR)
add("snare", "スネア", 0.26, 0, SNARE, barGain=A, push=0.02, gainDb=DR)
add("hihat", "ハイハット", 0.08, 0, HAT, barGain=A, push=-0.008, gainDb=DR)
add("crash", "クラッシュ", 0.1, 0, CRASH, barGain=A, gainDb=DR)
add("crash", "ライド", 0.07, 0.2, RIDE, barGain=A, gainDb=DR)
add("tom", "タム", 0.14, 0, TOM, barGain=A, reverb=0, gainDb=DR)

song = {"title": "ネオンハートビート（仮）",
        "description": "（仮）ボカロ曲のようなインスト。約5分・BPM172・ロ短調、最後のサビ4回分は半音上のハ短調。旋律は A・Bメロ・落ちサビがピアノ、サビ・リフ・ブリッジ・ソロがリードギター（ビブラートなし）。16分のピアノ・動くベース・歪みギター・左右の弦・サビの厚いシンセ・FMベル。入り方: 2（ピアノの16分だけで4小節）。終わり方: 全員で一発止め＋長い和音。動機: B5:0.5 A5:0.5 B5:0.5 D6:1（サビ頭）。",
        "bpm": 172, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "vocaloid", "human": 0.25, "dynamics": "natural", "autoAccompaniment": False,
        "parts": PARTS}
json.dump(song, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars", round(len(chords) * 4 * 60 / 172), "sec")
