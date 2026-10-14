# 『ナイトドリフト』（仮）: フォンク系（ドリフトフォンク風）のインスト。BPM140（ハーフタイムのノリ）・嬰ヘ短調（和声的短音階）、約2分58秒。
# 主役: フォンク定番の「カウベル風」の旋律リフ（fmBell を短く切って金属的に）。低音は 808（sub808。少し歪ませる）。
# ドラム: 3拍目のスネア（ハーフタイム）、ハイハットのロール。声の素材は使わない（既存の録音の流用になるため）。
# 構成（104小節）: イントロ8 → ビルド8 → ドロップ16 → ブレイク8 → ドロップ16（リフB） → ブリッジ8 → ドロップ16 → ドロップ16（リフB・最大） → 終わり8
# 使い方: python3 night-drift.py <出力.json>
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

# ---------------- コード（1小節1つ） ----------------
LOOP = "F#m D Bm C# F#m D Bm C#".split()
SEC = [("intro", LOOP, 0, 0), ("build", LOOP, 0, 0), ("drop", LOOP * 2, 0, 0), ("break", LOOP, 0, 0),
       ("drop", LOOP * 2, 0, 1), ("bridge", LOOP, 0, 0), ("drop", LOOP * 2, 0, 2), ("drop", LOOP * 2, 0, 3), ("outro", LOOP, 0, 0)]
chords = [c for _, pr, _, _ in SEC for c in pr]
GAIN = {"intro": .8, "build": .85, "drop": 1.0, "break": .75, "bridge": .78, "outro": .8}
ARC = []
for si, (s, pr, k, n) in enumerate(SEC):
    g = GAIN[s] + (0.03 if n == 3 else 0)
    ARC += [round(min(1.05, g + (0.12 * i / len(pr) if s == "build" else 0) - (0.2 * i / len(pr) if s == "outro" else 0)), 3) for i in range(len(pr))]

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

# ---------------- カウベル風の旋律 ----------------
RA = ["F#5:0.5 F#5:0.25 A5:0.25 C#6:0.5 A5:0.5 F#5:0.5 G#5:0.5 A5:1", "F#5:0.5 F#5:0.25 A5:0.25 D6:0.5 A5:0.5 F#5:0.5 E5:0.5 D5:1",
      "D5:0.5 D5:0.25 F#5:0.25 B5:0.5 F#5:0.5 D5:0.5 C#5:0.5 B4:1", "C#5:0.5 F5:0.25 G#5:0.25 C#6:0.5 G#5:0.5 F5:0.5 G#5:0.5 C#5:1"]
RB = ["C#6:0.25 C#6:0.25 A5:0.5 F#5:0.25 F#5:0.25 C#6:0.5 B5:0.5 A5:0.5 G#5:0.5 F#5:0.5",
      "D6:0.25 D6:0.25 A5:0.5 F#5:0.25 F#5:0.25 D6:0.5 C#6:0.5 A5:0.5 F#5:0.5 A5:0.5",
      "B5:0.25 B5:0.25 F#5:0.5 D5:0.25 D5:0.25 B5:0.5 A5:0.5 F#5:0.5 D5:0.5 F#5:0.5",
      "C#6:0.25 C#6:0.25 G#5:0.5 F5:0.25 F5:0.25 C#6:0.5 B5:0.5 G#5:0.5 F5:0.5 G#5:0.5"]
RA2 = RA[:2] + ["D5:0.25 F#5:0.25 B5:0.5 D6:0.5 B5:0.5 F#5:0.5 D5:0.5 F#5:1", "C#6:0.5 G#5:0.5 F5:0.5 C#5:0.5 F5:0.5 G#5:0.5 C#6:1"]
RA3 = ["A5:0.5 A5:0.25 C#6:0.25 F#6:0.5 C#6:0.5 A5:0.5 B5:0.5 C#6:1", "A5:0.5 A5:0.25 D6:0.25 F#6:0.5 D6:0.5 A5:0.5 F#5:0.5 D6:1"] + RA2[2:]
RB2 = RB[:2] + RA2[2:]
RS = ["F#5:1 R:1 C#6:1 R:1", "D6:1 R:1 A5:1 R:1", "B5:1 R:1 F#5:1 R:1", "F5:1 R:1 G#5:1 R:1"]   # まばら（ブレイク）
def f_cow(si, s, pr, k, n):
    if s == "intro": return "R:16 " + seq(RA)
    if s == "build": return seq(RS) + " " + seq(RA2)
    if s == "drop": return seq([RA + RA2 + RA + RA3, RB + RB2 + RB + RA3, RA3 + RA2 + RA + RA3, RB + RB2 + RA3 + RB2][n])
    if s == "break": return seq(RS * 2)
    if s == "bridge": return seq(RB + RB2, -12)
    if s == "outro": return seq(RA) + " " + seq(RS)
def f_cow2(si, s, pr, k, n):   # 最後のドロップだけ、3度上に重ねる（短3度・長3度は和音に合わせて）
    if s == "drop" and n == 3:
        out = []
        for x in " ".join(RB * 4).split():
            if x.startswith("R:"): out.append(x); continue
            nn, d = x.split(":"); m = midi(nn)
            out.append(nm(m + (3 if m % 12 in (6, 11, 2) else 4) - 12) + ":" + d)
        return " ".join(out)
    return rest(pr)

# ---------------- 808 ----------------
def f_808(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = 28 + ((chord_pcs(ch)[0] - 28) % 12); a, o = nm(r), nm(r + 12 if r + 12 <= 48 else r + 7)
        if s == "intro": out += [f"{a}:4"]
        elif s in ("break",): out += [f"{a}:4"]
        elif s == "outro": out += [f"{a}:4"] if i < 4 else ["R:4"]
        elif s == "build": out += [f"{a}:2", f"{a}:2"]
        else: out += [f"{a}:1.5", f"{a}:1", f"{o}:0.5", f"{a}:1"]
    return " ".join(out)

# ---------------- 暗いパッド（ブレイク・ブリッジ・イントロ） ----------------
def pad(center, which):
    def f(si, s, pr, k, n):
        return " ".join(f"{nm(voicing(ch, center)[which])}:4" if s in ("break", "bridge", "intro") else "R:4" for ch in pr)
    return f

# ---------------- ドラム ----------------
Z = "................"
def tomtok(tm):
    pit = ["E3", "E3", "C3", "C3", "A2", "A2"]; hits = [j for j, c in enumerate(tm) if c in "xX"]; toks = []; kk = 0
    for c in tm:
        if c in "xX": toks.append(pit[min(5, kk * 6 // len(hits))] + ":0.25" + ("!" if c == "X" else "")); kk += 1
        else: toks.append("R:0.25")
    return toks
KICK, SNARE, HAT, CRASH, TOM = [], [], [], [], []
for si, (s, pr, k, n) in enumerate(SEC):
    kb, sb, hb, cb, tb = [], [], [], [], []
    L = len(pr)
    for b in range(L):
        last = b == L - 1; cr = "R:4"; tm = None
        roll = "x.x.x.x.x.x.xxxx" if b % 2 == 1 else "x.x.x.x.x.x.x.x."
        if s == "intro": kk, sn, hh = Z, Z, (Z if b < 4 else "x.x.x.x.x.x.x.x.")
        elif s == "build":
            kk = "X.......X......."; hh = "xxxxxxxxxxxxxxxx" if b >= 4 else "x.x.x.x.x.x.x.x."
            sn = ["........X.......", "........X.......", "....X.......X...", "....X.......X...", "X...X...X...X...", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XXXXXXXXXXXXXXXX"][b]
        elif s == "drop":
            kk = "X.....X...X....." if b % 4 != 3 else "X.....X...X.X.X."; sn = "........X......."
            hh = roll if n < 3 else ("xxxxxxxxxxxxxxxx" if b % 2 == 0 else "x.xxx.xxx.xxxxxx")
            if b % 8 == 0: cr = "g:X..............."
            if last: sn = "........X...xxXX"; tm = "............xxXX" if n != 3 else None
        elif s == "break": kk, sn, hh = Z, Z, ("x...x...x...x..." if b >= 4 else Z)
        elif s == "bridge":
            kk = "X..............." if b % 2 == 0 else Z; sn = "........X......." if b >= 4 else Z; hh = "x.x.x.x.x.x.x.x."
            if last: sn = "X.X.X.X.XXXXXXXX"
        elif s == "outro":
            kk = "X.....X...X....." if b < 4 else (Z if b > 4 else "X..............."); sn = "........X......." if b < 4 else Z; hh = roll if b < 4 else Z
            if b == 4: cr = "g:X..............."
        if cr != "R:4": hh = "." + hh[1:]
        if tm:
            first = next(j for j, c in enumerate(tm) if c in "xX"); hh = hh[:first] + "." * (16 - first)
        kb.append("g:" + kk); sb.append("g:" + sn); hb.append("g:" + hh); cb.append(cr)
        tb += tomtok(tm) if tm else ["R:4"]
    KICK.append(kb); SNARE.append(sb); HAT.append(hb); CRASH.append(cb); TOM.append(tb)

PARTS = []
def add(inst, role, vol, pan, secs, **kw):
    d = {"instrument": inst, "role": role, "volume": vol, "pan": pan, "notes": cat(secs, role)}; d.update(kw); PARTS.append(d)
A = ARC
add("fmBell", "カウベル風の旋律", 0.24, 0, per(f_cow), barGain=A, reverb=0.18, sustain=0.35, gainDb=2)
add("fmBell", "カウベル風（3度上の重ね）", 0.12, 0.35, per(f_cow2), barGain=A, reverb=0.2, sustain=0.35)
add("pad", "暗いパッド（上）", 0.07, 0.5, per(pad(66, 2)), barGain=A, reverb=0.35, patch="metalPad")
add("pad", "暗いパッド（下）", 0.07, -0.5, per(pad(57, 0)), barGain=A, reverb=0.35, patch="metalPad")
add("sub808", "808", 0.4, 0, per(f_808), barGain=A, amp="fuzz", ampDrive=0.5)
add("kick", "キック", 0.32, 0, KICK, barGain=A)
add("snare", "スネア（ハーフタイム）", 0.28, 0, SNARE, barGain=A, reverb=0.15)
add("hihat", "ハイハット（ロール）", 0.08, 0, HAT, barGain=A)
add("crash", "クラッシュ", 0.09, 0, CRASH, barGain=A)
add("tom", "タム", 0.14, 0, TOM, barGain=A, reverb=0)

song = {"title": "ナイトドリフト（仮）",
        "description": "（仮）フォンク系（ドリフトフォンク風）のインスト。BPM140・ハーフタイム・嬰ヘ短調（和声的短音階）。主役は短く金属的なカウベル風の旋律リフ（fmBell）、低音は少し歪ませた 808、3拍目のスネアとハイハットのロール。声の素材は使わない。入り方: 5（暗いパッドと808の持続音から。リフは5小節目から）。終わり方: 旋律がまばらになって消える。動機: F#5:0.5 F#5:0.25 A5:0.25 C#6:0.5。",
        "bpm": 140, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "pop", "human": 0.15, "dynamics": "natural", "autoAccompaniment": False,
        "parts": PARTS}
json.dump(song, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars", round(len(chords) * 4 * 60 / 140), "sec")
