# 『ミッドナイト・ベルベット』（仮）: 大人っぽく少し色っぽい、ポップなボカロ風の曲（歌なし）。BPM110・ハ短調、約3分56秒。
# 雰囲気とジャンルの参考だけ（既存曲の旋律・進行・決まったフレーズは使わない。CLAUDE.md 1-1）。
# ノリ: 16分の裏打ちのグルーブ、跳ねるスラップベース、エレピ（keys）の裏打ちの和音（2声）、サビは左右の弦。
# 色っぽさ: 7th の和音中心。G7 では ♭9（A♭）の緊張音（わざと。半音のぶつかりの注意は出る）。旋律はサビ・間奏がリードギター（warm-lead-b）、Aメロ・Bメロ・ブリッジは FM エレピ。
# 構成（108小節）: イントロ4 → Aメロ16 → Bメロ8 → サビ16 → 間奏4 → Aメロ8 → Bメロ8 → サビ16 → ブリッジ8 → サビ16 → 終わり4
# 使い方: python3 midnight-velvet.py <出力.json>
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

# ---------------- コード ----------------
INTRO = "Abmaj7 G7 Cm7 Cm7".split()
VERSE = "Cm7 Fm7 Bb7 Ebmaj7 Abmaj7 Fm7 G7 G7".split()
PRE = "Abmaj7 Bb Gm7 Cm7 Fm7 Gm7 Abmaj7 G7".split()
CHO = "Abmaj7 G7 Cm7 Bb7 Ebmaj7 Abmaj7 Fm7 G7".split()
CHO_END = "Abmaj7 G7 Cm7 Bb7 Ebmaj7 Abmaj7 G7 Cm7".split()
BRI = "Fm7 Gm7 Abmaj7 Bb Fm7 Gm7 Abmaj7 Ab7".split()   # 最後の Ab7 で半音上（嬰ハ短調）へ
SEC = [("intro", INTRO, 0, 0), ("verse", VERSE, 0, 0), ("verse", VERSE, 0, 1), ("pre", PRE, 0, 0),
       ("chorus", CHO, 0, 0), ("chorus", CHO, 0, 1), ("inter", INTRO, 0, 0),
       ("verse", VERSE, 0, 2), ("pre", PRE, 0, 1), ("chorus", CHO, 0, 0), ("chorus", CHO, 0, 1),
       ("bridge", BRI, 0, 0), ("chorus", up(CHO, 1), 1, 2), ("chorus", up(CHO_END, 1), 1, 3), ("outro", up(INTRO, 1), 1, 0)]
chords = [c for _, pr, _, _ in SEC for c in pr]
GAIN = {"intro": .82, "verse": .82, "pre": .9, "chorus": 1.0, "inter": .9, "bridge": .75, "outro": .9}
ARC = []
for si, (s, pr, k, n) in enumerate(SEC):
    g = GAIN[s] + (0.03 if si >= 7 and s != "bridge" else 0)
    ARC += [round(min(1.05, g + (0.05 * i / len(pr) if s in ("pre", "bridge") else 0)), 3) for i in range(len(pr))]

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
M_V = ["R:0.5 G4:0.25 Bb4:0.25 C5:0.5 Eb5:0.5 D5:0.5 C5:0.5 Bb4:1", "Ab4:0.75 G4:0.25 F4:0.5 Ab4:0.5 C5:1 R:1",
       "R:0.5 F4:0.25 Ab4:0.25 Bb4:0.5 D5:0.5 C5:0.5 Bb4:0.5 Ab4:1", "G4:1.5 Bb4:0.5 D5:1 R:1",
       "R:0.5 C5:0.25 Eb5:0.25 G5:0.5 F5:0.5 Eb5:0.5 C5:0.5 Ab4:1", "Ab4:0.5 C5:0.5 Eb5:0.75 D5:0.25 C5:1 R:1",
       "B4:1 D5:0.5 F5:0.5 Ab5:1 G5:1", "F5:0.5 D5:0.5 B4:1 G4:1 R:1"]
M_V2 = ["R:0.5 Eb5:0.25 D5:0.25 C5:0.5 G4:0.5 Bb4:0.5 C5:0.5 Eb5:1", "F5:0.75 Eb5:0.25 C5:0.5 Ab4:0.5 C5:1 R:1",
        M_V[2], M_V[3], "R:0.5 Eb5:0.25 G5:0.25 C6:0.5 Bb5:0.5 G5:0.5 Eb5:0.5 C5:1", M_V[5], M_V[6], "G5:2 R:2"]
M_V3 = ["Eb5:0.5 D5:0.5 C5:0.5 Bb4:0.5 C5:0.75 Eb5:0.25 G5:1", "F5:1 Eb5:0.5 C5:0.5 Ab4:1 R:1"] + M_V2[2:]
M_P = ["C5:1 Eb5:1 G5:1.5 F5:0.5", "F5:1 D5:1 Bb4:2", "Bb4:1 D5:1 F5:1.5 Eb5:0.5", "Eb5:2 R:1 C5:0.5 D5:0.5",
       "Eb5:1 F5:0.5 Ab5:0.5 C6:1.5 Bb5:0.5", "Bb5:1 G5:0.5 F5:0.5 D5:1 F5:1", "G5:1.5 Ab5:0.5 C6:2", "B5:2 R:1 G5:0.5 Ab5:0.5"]
M_P2 = ["Eb5:0.5 G5:0.5 C6:1 Bb5:1 G5:1", "F5:0.5 Bb5:0.5 C6:1 Bb5:1 F5:1", "Bb5:1 G5:1 F5:1.5 D5:0.5", "Eb5:2 R:1 C5:0.5 D5:0.5"] + M_P[4:]
M_C = ["G5:0.75 Ab5:0.25 G5:0.5 Eb5:0.5 C5:1 Eb5:1", "D5:0.75 Eb5:0.25 D5:0.5 B4:0.5 G4:1 F5:1",
       "Eb5:0.5 G5:0.5 Bb5:0.75 G5:0.25 C6:1 Bb5:1", "Ab5:1.5 F5:0.5 D5:1 R:1",
       "G5:0.5 Bb5:0.5 D6:1 C6:0.5 Bb5:0.5 G5:1", "C6:0.75 Bb5:0.25 Ab5:0.5 G5:0.5 Eb5:1 C5:1",
       "Ab5:0.5 G5:0.5 F5:0.5 Eb5:0.5 F5:1 Ab5:1", "B5:1.5 Ab5:0.5 G5:1 R:1"]
M_C2 = ["C6:0.75 Bb5:0.25 G5:0.5 Eb5:0.5 G5:1 C6:1", "B5:0.75 C6:0.25 B5:0.5 G5:0.5 D5:1 F5:1",
        "Eb5:0.5 G5:0.5 C6:0.75 Bb5:0.25 G5:1 Eb5:1", "F5:1.5 Ab5:0.5 Bb5:1 R:1",
        "Bb5:0.5 D6:0.5 Eb6:1 D6:0.5 Bb5:0.5 G5:1", "Eb6:0.75 D6:0.25 C6:0.5 Bb5:0.5 G5:1 Eb5:1"] + \
       ["Ab5:0.5 C6:0.5 Eb6:0.5 C6:0.5 Ab5:1 F5:1", "G5:2 R:1 G5:0.5 Ab5:0.5"]
M_C_END = M_C2[:6] + ["B5:1 D6:1 B5:1 G5:1", "C6:3 R:1"]
M_BR = ["C5:2 Ab4:2", "D5:2 Bb4:2", "Eb5:1.5 G5:0.5 C6:2", "D5:2 F5:2", "Ab5:2 F5:2", "Bb5:2 G5:2", "C6:1.5 Bb5:0.5 G5:2", "C6:2 R:2"]
HOOK = ["G5:0.75 Ab5:0.25 G5:0.5 Eb5:0.5 C5:1 Eb5:1", "D5:0.75 Eb5:0.25 D5:0.5 B4:0.5 G4:1 F5:1", "Eb5:2 C5:2", "R:4"]
def f_piano_mel(si, s, pr, k, n):
    if s == "verse": return " ".join([M_V, M_V2, M_V3][n])
    if s == "pre": return " ".join(M_P if n == 0 else M_P2)
    if s == "bridge": return " ".join(M_BR)
    return rest(pr)
def f_lead(si, s, pr, k, n):
    if s == "chorus": return seq([M_C, M_C2, M_C, M_C_END][n], k, fold)
    if s == "inter": return seq(HOOK, k, fold)
    if s == "outro": return seq(HOOK[:2] + ["C5:4", "R:4"], k, fold)
    return rest(pr)

# ---------------- エレピ（裏打ちの和音・2声。3度と7度） ----------------
def shell(ch, which):
    pcs = chord_pcs(ch); third = pcs[1]; sev = pcs[3] if len(pcs) > 3 else pcs[2]
    lo = 58
    t = lo + ((third - lo) % 12); s7 = t + ((sev - t) % 12)
    return [t, s7][which]
def keys(which):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            x = nm(shell(ch, which)); last = i == len(pr) - 1
            if s == "intro" and i < 2: out += ["R:4"]
            elif s == "bridge": out += [f"{x}:4"]
            elif s == "pre" and last: out += [f"{x}:1", "R:3"]
            elif s == "outro" and last: out += [f"{x}:4"]
            else: out += ["R:0.5", f"{x}:1", f"{x}:0.5", "R:0.5", f"{x}:0.75", f"{x}:0.75"]
        return " ".join(out)
    return f

# ---------------- 弦（サビとブリッジ） ----------------
def strings(center, which):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            v = nm(voicing(ch, center)[which])
            out.append(f"{v}:4" if s in ("chorus", "bridge") else "R:4")
        return " ".join(out)
    return f

# ---------------- スラップベース（跳ねる16分） ----------------
def f_bass(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = 28 + ((bass_pc(ch) - 28) % 12); a, o, f5 = nm(r), nm(r + 12 if r + 12 <= 50 else r + 7), nm(r + 7)
        b7 = nm(r + 10 if r + 10 <= 50 else r - 2)
        last = i == len(pr) - 1
        if s == "bridge": out += [f"{a}:2", f"{f5}:1", f"{a}:1"]
        elif s == "pre" and last: out += [f"{a}:1", "R:3"]
        elif s == "outro" and last: out += [f"{a}:4"]
        elif s == "intro" and i < 2: out += ["R:4"]
        else: out += [f"{a}:0.5", f"{a}:0.25", f"{o}:0.25", "R:0.5", f"{a}:0.5", f"{f5}:0.25", f"{o}:0.25", f"{a}:0.5", f"{b7}:0.5", f"{o}:0.5"]
    return " ".join(out)

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
        if s == "intro":
            kk, sn, hh = "X..X..X...X..X..", "....X..o.o..X...", "xxXxxxXxxxXxxxXx"
            if last: sn = "....X..o.o..xxXX"
        elif s == "verse":
            kk = "X..X..X...X..X.." if b % 2 == 0 else "X..X......X..X.."; sn = "....X..o.o..X..o"
            hh = "x.x.x.x.x.x.x.x." if n == 0 else "xxXxxxXxxxXxxxXx"
            if b == 0: cr = "g:X..............."
            if last: sn = "....X..o.o..xxXX"
        elif s == "pre":
            kk = "X.....X.X.....X."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."
            if b == 0: cr = "g:X..............."
            if b == 6: sn = "....X...x.x.X.x."
            if last: kk = "X..............."; sn = "........xxxxXXXX"; hh = Z
        elif s == "chorus":
            kk = "X..X..X...X..X.." if b % 2 == 0 else "X..X..X.X.X..X.."; sn = "....X..o.o..X..o"; hh = "x.O.x.O.x.O.x.O."
            if b % 4 == 0: cr = "g:X..............."
            if last: sn = "....X...xxxxXXXX" if n != 3 else "X..............."; tm = "........xx..xxXX" if n != 3 else None
            if last and n == 3: kk = "X..............."; hh = Z
        elif s == "inter":
            kk = "X..X..X...X..X.."; sn = "....X..o.o..X..o"; hh = "xxXxxxXxxxXxxxXx"
            if b == 0: cr = "g:X..............."
            if last: sn = "....X...xxxxXXXX"; tm = "............xxXX"
        elif s == "bridge":
            kk = "X.......X......." if b < 4 else "X..X..X...X..X.."; sn = "........X......." if b < 4 else "....X..o.o..X..o"; hh = "x...x...x...x..." if b < 4 else "x.x.x.x.x.x.x.x."
            if b == 0: cr = "g:X..............."
            if last: kk = "X..............."; sn = "X..............."; hh = Z   # 最後のサビの前で止める
        elif s == "outro":
            kk = "X..X..X...X..X.." if b < 2 else ("X..............." if b == 2 else Z); sn = "....X..o.o..X..o" if b < 2 else Z
            hh = "xxXxxxXxxxXxxxXx" if b < 2 else Z
            if b in (0, 2): cr = "g:X..............."
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
DR = -6
add("fmEpiano", "旋律（FMエレピ）", 0.22, -0.05, per(f_piano_mel), barGain=A, reverb=0.22, gainDb=2)
add("leadGuitar", "旋律（リードギター）", 0.16, 0.08, per(f_lead), barGain=A, gainDb=3, guitarTone="warm-lead-b")
add("keys", "エレピ（3度）", 0.12, -0.45, per(keys(0)), barGain=A, reverb=0.2)
add("keys", "エレピ（7度）", 0.11, 0.45, per(keys(1)), barGain=A, reverb=0.2)
add("strings", "弦（上）", 0.08, 0.6, per(strings(72, 2)), barGain=A, reverb=0.28)
add("strings", "弦（下）", 0.07, -0.6, per(strings(57, 0)), barGain=A, reverb=0.28)
add("slap", "スラップベース", 0.3, 0, per(f_bass), barGain=A)
add("kick", "キック", 0.3, 0, KICK, barGain=A, gainDb=DR)
add("snare", "スネア", 0.26, 0, SNARE, barGain=A, push=0.025, gainDb=DR)
add("hihat", "ハイハット", 0.08, 0, HAT, barGain=A, push=-0.008, gainDb=DR)
add("crash", "クラッシュ", 0.1, 0, CRASH, barGain=A, gainDb=DR)
add("tom", "タム", 0.14, 0, TOM, barGain=A, reverb=0, gainDb=DR)

song = {"title": "ミッドナイト・ベルベット（仮）",
        "description": "（仮）大人っぽく少し色っぽい、ポップなボカロ風の曲（歌なし）。BPM110・ハ短調。16分の裏打ち・スラップベース・エレピの裏打ちの和音。7th 中心で G7 に ♭9。旋律はサビがリードギター（warm-lead-b）、Aメロ・Bメロ・ブリッジが FM エレピ。入り方: 6（ドラムのグルーブだけで2小節→ベースとエレピ）。最後のサビ2回は半音上（嬰ハ短調）。終わり方: サビの頭の動機で終わる。動機: G5:0.75 Ab5:0.25 G5:0.5 Eb5:0.5（サビ頭）。",
        "bpm": 110, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "pop", "human": 0.3, "dynamics": "natural", "autoAccompaniment": False,
        "parts": PARTS}
json.dump(song, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars", round(len(chords) * 4 * 60 / 110), "sec")
