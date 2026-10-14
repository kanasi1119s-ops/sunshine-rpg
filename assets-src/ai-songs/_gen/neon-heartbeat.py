# 『ネオンハートビート』（仮）: ボカロ曲のようなインスト。BPM186・ロ短調（最後のサビ2回は半音上のハ短調）。
# 歌のかわりにシンセのリード（早口・音域広め・サビで高く。長い音だけビブラート）。16分で走るピアノ、動くベース、
# 歪みギターの刻み（左右）、左右の弦、サビの厚いシンセ（unisonSaw）、サビできらめく FM ベル、生ドラム。
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

# ---------------- 構成とコード ----------------
INTRO = "Gmaj7 A F#m7 Bm Gmaj7 A F#m7 Bm".split()
VERSE = "Bm G D A Bm G Em F#7".split()
PRE = "Em F#m G A Em F#m G A".split()
CHO = "G A F#m Bm G A Bm Bm".split()
INTER = "Bm G D A".split()
BRI = "Em Bm Cmaj7 D Em Bm Cmaj7 G7".split()
CHO_UP = "Ab Bb Gm Cm Ab Bb Cm Cm".split()   # 半音上（ハ短調）
OUT = "Abmaj7 Bb Gm Cm".split()
SEC = [("intro", INTRO, 0, 0), ("verse", VERSE, 0, 0), ("pre", PRE, 0, 0), ("chorus", CHO, 0, 0), ("inter", INTER, 0, 0),
       ("verse", VERSE, 0, 1), ("pre", PRE, 0, 1), ("chorus", CHO, 0, 1), ("bridge", BRI, 0, 0),
       ("chorus", CHO_UP, 1, 2), ("chorus", CHO_UP, 1, 3), ("outro", OUT, 1, 0)]
chords = [c for _, pr, _, _ in SEC for c in pr]
GAIN = {"intro": .82, "verse": .84, "pre": .9, "chorus": 1.0, "inter": .88, "bridge": .9, "outro": .95}
ARC = []
for si, (s, pr, k, n) in enumerate(SEC):
    g = GAIN[s] + (0.03 if n >= 1 and s != "bridge" else 0)
    ARC += [round(min(1.05, g + (0.04 * i / len(pr) if s == "pre" else 0)), 3) for i in range(len(pr))]

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
    c = ch.split("/")[0]
    m = re.match(r"^([A-G][#b]?)(.*)$", c); r = pcof(m.group(1)); q = m.group(2)
    minor = q.startswith("m") and not q.startswith("maj")
    pcs = [r, (r + (3 if minor else 4)) % 12, (r + 7) % 12]
    if "maj7" in q: pcs.append((r + 11) % 12)
    elif "7" in q: pcs.append((r + 10) % 12)
    return pcs
def tones_from(ch, lo):
    """lo 以上で、根音から始まる和音の音を上へ並べる（2オクターブ分）。"""
    pcs = chord_pcs(ch); r = pcs[0]; base = lo + ((r - lo) % 12)
    out = []
    for o in (0, 12):
        for p in pcs: out.append(base + o + ((p - r) % 12))
    return sorted(out)
def voicing(ch, center):
    pcs = chord_pcs(ch)[:3]; best = None
    for inv in range(3):
        o = pcs[inv:] + pcs[:inv]; cur = center - 7; v = []
        for p in o:
            n = cur + ((p - cur) % 12); v.append(n); cur = n + 1
        sc = abs(sum(v) / 3 - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]
def root_in(ch, lo): return lo + ((chord_pcs(ch)[0] - lo) % 12)

# ---------------- 旋律（シンセのリード＝歌の役） ----------------
M_A = ["B4:0.5 B4:0.5 C#5:0.5 D5:0.5 C#5:0.5 B4:0.5 F#4:1", "R:0.5 G4:0.5 A4:0.5 B4:0.5 D5:1 B4:0.5 A4:0.5",
       "A4:0.5 A4:0.25 A4:0.25 B4:0.5 A4:0.5 F#4:0.5 E4:0.5 D4:1", "E4:0.5 F#4:0.5 A4:1 C#5:1.5 R:0.5",
       "B4:0.5 B4:0.5 C#5:0.5 D5:0.5 E5:0.5 D5:0.5 C#5:0.5 B4:0.5", "D5:0.5 B4:0.5 G4:0.5 B4:0.5 D5:1 E5:0.5 F#5:0.5",
       "G5:1 F#5:0.5 E5:0.5 D5:0.5 B4:0.5 G4:0.5 B4:0.5", "A#4:1.5 C#5:0.5 F#5:1.5 R:0.5"]
# 2番のAメロ: 前半はそのまま、後半を高く
M_A2 = M_A[:4] + ["B4:0.5 D5:0.5 F#5:0.5 E5:0.5 D5:0.5 C#5:0.5 B4:0.5 D5:0.5", "G5:0.5 F#5:0.5 D5:0.5 B4:0.5 D5:1 E5:0.5 F#5:0.5",
                  "G5:0.5 A5:0.5 G5:0.5 F#5:0.5 E5:0.5 D5:0.5 B4:0.5 E5:0.5", "F#5:1.5 E5:0.5 C#5:1.5 R:0.5"]
M_B = ["E5:1 D5:0.5 E5:0.5 G5:1 E5:1", "F#5:1 E5:0.5 C#5:0.5 A4:1 C#5:1", "D5:0.5 D5:0.5 E5:0.5 F#5:0.5 G5:1 A5:1",
       "A5:2 R:1 E5:0.5 F#5:0.5", "G5:1 F#5:0.5 E5:0.5 B4:1 E5:1", "A5:1 G#5:0.5 F#5:0.5 C#5:1 F#5:1",
       "B5:1 A5:0.5 G5:0.5 D5:0.5 G5:0.5 A5:0.5 B5:0.5", "C#6:2.5 R:1.5"]
M_C = ["B5:0.5 A5:0.5 B5:0.5 D6:1 B5:0.5 A5:0.5 G5:0.5", "A5:1 E5:0.5 F#5:0.5 A5:0.5 C#6:1 A5:0.5",
       "C#6:0.5 B5:0.5 A5:0.5 F#5:1 E5:0.5 F#5:0.5 A5:0.5", "B5:2.5~ R:0.5 F#5:0.5 A5:0.5",
       "B5:0.5 A5:0.5 B5:0.5 D6:1 B5:0.5 A5:0.5 G5:0.5", "A5:1 B5:0.5 C#6:0.5 E6:1 C#6:0.5 A5:0.5",
       "D6:1 C#6:0.5 B5:0.5 A5:0.5 F#5:0.5 A5:0.5 B5:0.5", "B5:3~ R:1"]
M_C_LAST = M_C[:6] + ["D6:1 E6:0.5 F#6:0.5 E6:1 D6:1", "B5:4~"]   # 最後のサビの終わりは高く
M_BR = ["E5:0.25 F#5:0.25 G5:0.25 B5:0.25 E6:1 D6:0.5 B5:0.5 G5:1", "F#5:0.5 D5:0.5 B4:0.5 D5:0.5 F#5:1 B5:1",
        "G5:0.25 A5:0.25 B5:0.25 C6:0.25 E6:1 D6:0.5 C6:0.5 B5:1", "A5:0.5 F#5:0.5 D5:0.5 F#5:0.5 A5:1 D6:1",
        "E6:1 D6:0.5 B5:0.5 G5:0.5 B5:0.5 E5:1", "D6:1 B5:0.5 F#5:0.5 D5:1 F#5:1",
        "E6:0.5 D6:0.5 C6:0.5 B5:0.5 G5:0.5 E5:0.5 G5:0.5 B5:0.5", "B5:1 D6:1 F6:1 G6:0.5 R:0.5"]
def f_lead(si, s, pr, k, n):
    if s == "intro": return "R:16 " + " ".join(M_C[:3]) + " B5:2~ R:2"
    if s == "verse": return " ".join(M_A if n == 0 else M_A2)
    if s == "pre": return " ".join(M_B)
    if s == "chorus":
        src = M_C_LAST if n == 3 else M_C
        return " ".join(tr(x, k) for x in " ".join(src).split())
    if s == "bridge": return " ".join(M_BR)
    return rest(pr)
def f_bell(si, s, pr, k, n):
    if s == "chorus":
        src = M_C_LAST if n == 3 else M_C
        return " ".join(tr(x.replace("~", ""), k) for x in " ".join(src).split())
    return rest(pr)

# ---------------- ピアノ（16分で走る分散和音） ----------------
PAT = [0, 2, 1, 3, 4, 3, 2, 1, 0, 2, 1, 3, 4, 5, 4, 3]
def f_piano(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        t = tones_from(ch, 55)
        last = i == len(pr) - 1
        if s == "pre" and last: out += [f"{nm(t[0])}:0.25", f"{nm(t[2])}:0.25", f"{nm(t[4])}:0.5", "R:3"]
        elif s == "bridge" and i < 4: out += [f"{nm(t[j % len(t)])}:0.5" for j in (0, 2, 4, 2, 0, 2, 4, 2)]
        elif s == "outro" and last: out += [f"{nm(t[0])}:4"]
        else: out += [f"{nm(t[j % len(t)])}:0.25" for j in PAT]
    return " ".join(out)

# ---------------- ギター（歪み・8分の刻み。左右） ----------------
def guitar(side):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            r = nm(root_in(ch, 40))
            last = i == len(pr) - 1
            if s in ("intro",) and i < 4: out += ["R:4"]
            elif s == "verse" and n == 0: out += ["R:4"]
            elif s == "verse": out += [f"{r}:1.5", f"{r}:0.5", f"{r}:1", f"{r}:1"]
            elif s in ("pre", "chorus", "intro", "bridge"):
                if (s == "pre" and last): out += [f"{r}:1", "R:3"]
                else: out += [f"{r}:0.5"] * 8
            elif s == "inter": out += [f"{r}:2", f"{r}:2"]
            elif s == "outro": out += [f"{r}:0.5"] * 8 if not last else [f"{r}:4"]
        return " ".join(out)
    return f

# ---------------- 弦・厚いシンセ（2声） ----------------
def pad(center, which, sections):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            if s in sections and not (s == "pre" and i == len(pr) - 1):
                out.append(f"{nm(voicing(ch, center)[which])}:4")
            elif s == "pre" and s in sections: out += [f"{nm(voicing(ch, center)[which])}:1", "R:3"]
            else: out.append("R:4")
        return " ".join(out)
    return f

# ---------------- ベース（動く8分＋オクターブ） ----------------
def f_bass(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = root_in(ch, 28); a, o, f5 = nm(r), nm(r + 12), nm(r + 7)
        nx = pr[i + 1] if i + 1 < len(pr) else ch; rn = root_in(nx, 28)
        ap = nm(rn - 1 if rn > r else rn + 1) if rn != r else f5
        last = i == len(pr) - 1
        if s == "intro" and i < 4: out += ["R:4"]
        elif s == "pre" and last: out += [f"{a}:1", "R:3"]
        elif s in ("chorus", "intro"):
            out += [a + ":0.5", a + ":0.5", o + ":0.5", a + ":0.5", a + ":0.5", o + ":0.5", f5 + ":0.5", ap + ":0.5"] if i % 4 != 3 else \
                   [a + ":0.5", o + ":0.5", a + ":0.5", o + ":0.5", f5 + ":0.25", o + ":0.25", f5 + ":0.25", a + ":0.25", ap + ":1"]
        elif s == "bridge": out += [a + ":1.5", a + ":0.5", o + ":1", ap + ":1"]
        elif s == "outro": out += [a + ":0.5"] * 8 if not last else [a + ":4"]
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
KICK, SNARE, HAT, CRASH, TOM, RIDE = [], [], [], [], [], []
for si, (s, pr, k, n) in enumerate(SEC):
    kb, sb, hb, cb, tb, rb = [], [], [], [], [], []
    L = len(pr)
    for b in range(L):
        last = b == L - 1; cr = "R:4"; rd = "R:4"; tm = None
        if s == "intro":
            if b < 4: kk, sn, hh = Z, Z, Z
            else:
                kk = "X..x..X...x.X..."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.O."
                if b == 4: cr = "g:X..............."
                if last: sn = "....X...xxxxXXXX"; tm = "............xxXX"
            if b == 3: sn = "........x.x.xxXX"
        elif s == "verse":
            kk = "X..x..X...x.X..." if b % 2 == 0 else "X..x..X...X..x.."; sn = "....X.......X..."
            hh = "x.x.x.x.x.x.x.O." if n == 0 else "xxx.xxx.xxx.xxO."
            if b == 0: cr = "g:X..............."
            if b == 3: sn = "....X.......X.o."
            if last: sn = "....X.......xxXX"
        elif s == "pre":
            kk = "X...X..xX...X..x"; sn = "....X..o....X..o"; hh = "xxxxxxxxxxxxxxxx"
            if b == 0: cr = "g:X..............."
            if b == 6: sn = "....X.x.X.x.XxXx"
            if last: kk = "X..............."; sn = Z; hh = Z; cr = "g:X..............."
        elif s == "chorus":
            kk = "X..xX..xX..xX..x" if b % 2 == 0 else "X..xX...X..xX.x."; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."
            if b % 4 == 0: cr = "g:X..............."
            if b == 3: sn = "....X.......X.xx"
            if n >= 2 and b in (1, 2, 5, 6): hh = Z; rd = "g:x.x.x.x.x.x.x.x."   # 最後のサビはライドで広げる
            if last: sn = "....X...xxxxXXXX" if n != 3 else "X..............."; tm = "........xx..xxXX" if n != 3 else None
            if last and n == 3: kk = "X..............."; hh = Z; rd = "R:4"
        elif s == "inter":
            kk = "X.......X.x....."; sn = Z if b < 2 else "....X.......X..."; hh = "xxxxxxxxxxxxxxxx"
            if b == 0: cr = "g:X..............."
            if last: sn = "....X...xxxxXXXX"; tm = "............xxXX"
        elif s == "bridge":
            if b < 4: kk = "X.......X......."; sn = "........X......."; hh = "x...x...x...x..."; rd = "R:4"
            else: kk = "X..xX..xX..xX..x"; sn = "....X.......X..."; hh = Z; rd = "g:x.x.x.x.x.x.x.x."
            if b == 0 or b == 4: cr = "g:X..............."
            if b == 6: sn = "....X...X...X.x."
            if last: kk = "X...X...X...X..."; sn = "xxxxxxxxXXXXXXXX"; hh = Z; rd = "R:4"; tm = None
        elif s == "outro":
            kk = "X..xX..xX..xX..x" if b < 2 else ("X..............." if b == 2 else Z)
            sn = "....X.......X..." if b < 2 else Z; hh = "x.O.x.O.x.O.x.O." if b < 2 else Z
            if b == 0 or b == 2: cr = "g:X..............."
        if cr != "R:4": hh = "." + hh[1:]
        if tm:
            first = next(j for j, c in enumerate(tm) if c in "xX")
            hh = hh[:first] + "." * (16 - first)
        kb.append("g:" + kk); sb.append("g:" + sn); hb.append("g:" + hh); cb.append(cr); rb.append(rd)
        tb += tomtok(tm) if tm else ["R:4"]
    KICK.append(kb); SNARE.append(sb); HAT.append(hb); CRASH.append(cb); TOM.append(tb); RIDE.append(rb)
RIDE_N = [[("D2:4" if x == "R:4" else x) for x in sec] for sec in RIDE]
# ライドは crash の楽器で D2（ライド）を鳴らす: グリッドのままでは高さが選べないので、8分の D2 にする
def ride_notes(sec_list):
    out = []
    for x in sec_list:
        out += ["D2:0.5"] * 8 if x.startswith("g:") else ["R:4"]
    return out
RIDE2 = [ride_notes(sec) for sec in RIDE]

PARTS = []
def add(inst, role, vol, pan, secs, **kw):
    d = {"instrument": inst, "role": role, "volume": vol, "pan": pan, "notes": cat(secs, role)}; d.update(kw); PARTS.append(d)
A = ARC
add("lead", "歌の役（シンセのリード）", 0.26, 0, per(f_lead), barGain=A, reverb=0.2, gainDb=2, breath=True)
add("fmBell", "きらめき（FMベル）", 0.07, 0.3, per(f_bell), barGain=A, reverb=0.3)
add("piano", "ピアノ（16分）", 0.15, -0.3, per(f_piano), barGain=A, reverb=0.15)
add("distGuitar", "ギター（左）", 0.07, -0.85, per(guitar(0)), barGain=A, amp="hardrock", ampDrive=0.9, ampTone=-3, chorus=0, reverb=0.1)
add("distGuitar", "ギター（右）", 0.07, 0.85, per(guitar(1)), barGain=A, amp="hardrock", ampDrive=0.9, ampTone=-3, chorus=0, reverb=0.1, push=0.008)
add("strings", "弦（上）", 0.09, 0.6, per(pad(70, 2, ("pre", "chorus", "bridge"))), barGain=A, reverb=0.25)
add("strings", "弦（下）", 0.08, -0.6, per(pad(58, 0, ("pre", "chorus", "bridge"))), barGain=A, reverb=0.25)
add("unisonSaw", "厚いシンセ（上）", 0.06, 0.45, per(pad(66, 1, ("chorus",))), barGain=A, reverb=0.2)
add("unisonSaw", "厚いシンセ（下）", 0.06, -0.45, per(pad(62, 0, ("chorus",))), barGain=A, reverb=0.2)
add("bass", "ベース", 0.32, 0, per(f_bass), barGain=A)
add("kick", "キック", 0.3, 0, KICK, barGain=A)
add("snare", "スネア", 0.26, 0, SNARE, barGain=A, push=0.02)
add("hihat", "ハイハット", 0.08, 0, HAT, barGain=A, push=-0.008)
add("crash", "クラッシュ", 0.1, 0, CRASH, barGain=A)
add("crash", "ライド", 0.07, 0.2, RIDE2, barGain=A)
add("tom", "タム", 0.14, 0, TOM, barGain=A, reverb=0)

song = {"title": "ネオンハートビート（仮）",
        "description": "（仮）ボカロ曲のようなインスト。BPM186・ロ短調、最後のサビ2回は半音上のハ短調。歌の役はシンセのリード。16分のピアノ・動くベース・歪みギター・左右の弦・サビの厚いシンセ。入り方: 2（ピアノの16分だけで4小節）→全員でサビの旋律。終わり方: 全員で一発止め。動機: B5:0.5 A5:0.5 B5:0.5 D6:1（サビ頭）。",
        "bpm": 186, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "vocaloid", "synth": True, "human": 0.25, "dynamics": "natural", "autoAccompaniment": False,
        "parts": PARTS}
json.dump(song, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars")
