# 『夏色シグナル』（仮）: 夏を感じる爽快なポップ。キュンとする恋の曲。BPM150・ニ長調（最後のサビはホ長調へ転調）。
# 楽器: 生ピアノ（3声）・クリーンギター（2声。コーラスなし・短い高音の刻みはしない＝禁止の音）・弦（2声）・ベース・生ドラム・
#       旋律は笛（lead。synth なし＝フルート）、サビでベル（bell）を重ねてきらめかせる。
# 使い方: python3 summer-signal.py <出力.json>
import json, sys

def fmt(x): return ("%.4f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pcof(s):
    r = PCN[s[0]]
    if len(s) > 1 and s[1] == "#": r += 1
    if len(s) > 1 and s[1] == "b": r -= 1
    return r % 12
def midi(n):  # "F#5" → 78
    i = 2 if len(n) > 2 and n[1] in "#b" else 1
    return pcof(n[:i]) + 12 * (int(n[i:]) + 1)
def tr(tok, k):  # 音名つきのトークンを k 半音ずらす
    if tok.startswith("R:") or k == 0: return tok
    n, rest = tok.split(":", 1)
    return nm(midi(n) + k) + ":" + rest

# ---------------- 構成とコード ----------------
INTRO = "G A F#m Bm".split()
VERSE = "Dmaj7 F#m7 Gmaj7 A Dmaj7 F#m7 Em7 A7".split()
PRE = "Bm F#m G D Em F#m G A".split()
CHO = "Gmaj7 A F#m7 Bm7 G A Dsus4 D".split()
INTER = "D G D A".split()
BRI = "Bm G D A Bm G Em A".split()
CHO_E = "Amaj7 B G#m7 C#m7 A B Esus4 E".split()
OUT_E = "A B E E".split()
SEC = [("intro", INTRO, 0), ("verse", VERSE, 0), ("pre", PRE, 0), ("chorus", CHO, 0), ("inter", INTER, 0),
       ("verse", VERSE, 0), ("pre", PRE, 0), ("chorus", CHO, 0), ("bridge", BRI, 0), ("chorus", CHO_E, 2), ("outro", OUT_E, 2)]
chords = [c for _, pr, _ in SEC for c in pr]
GAIN = {"intro": .8, "verse": .82, "pre": .9, "chorus": 1.0, "inter": .9, "bridge": .74, "outro": .95}
ARC = []
for si, (s, pr, _) in enumerate(SEC):
    g = GAIN[s] + (0.04 if si >= 5 and s != "bridge" else 0)
    ARC += [round(min(1.05, g + (0.03 * k / len(pr) if s == "pre" else 0)), 3) for k in range(len(pr))]

def barsum(toks):
    t = 0
    for x in toks:
        if x.startswith("g:"): assert len(x) == 18, x; t += 4; continue
        d = x.split(":")[1]; t += float("".join(c for c in d if c.isdigit() or c == "."))
    return t
def cat(secs, name):
    out = []
    for (s, pr, _), toks in zip(SEC, secs):
        if isinstance(toks, str): toks = toks.split()
        assert abs(barsum(toks) - 4 * len(pr)) < 1e-6, (name, s, barsum(toks), 4 * len(pr))
        out += toks
    return " ".join(out)
def per(fn): return [fn(si, s, pr, k) for si, (s, pr, k) in enumerate(SEC)]

def triad(ch):
    import re
    c = ch.split("/")[0]; r = pcof(c); m = bool(re.match(r"^[A-G][#b]?m(?!aj)", c))
    return [r, (r + (3 if m else 4)) % 12, (r + 7) % 12]
def voicing(ch, center):
    """3音の和音を、中心の高さに近い並びで返す（低い順）。"""
    pcs = triad(ch); best = None
    for inv in range(3):
        o = pcs[inv:] + pcs[:inv]
        base = center - 7
        v = []; cur = base
        for p in o:
            n = cur + ((p - cur) % 12); v.append(n); cur = n + 1
        sc = abs(sum(v) / 3 - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]
def root_in(ch, lo): r = pcof(ch.split("/")[0]); return lo + ((r - lo) % 12)

# ---------------- 旋律（笛） ----------------
M_A = ["R:0.5 F#4:0.5 A4:0.5 D5:1 C#5:0.5 A4:1", "R:0.5 F#4:0.5 A4:0.5 C#5:1 B4:0.5 A4:1",
       "R:0.5 G4:0.5 B4:0.5 D5:0.5 E5:1 D5:0.5 B4:0.5", "C#5:1.5 A4:0.5 E5:2",
       "R:0.5 F#4:0.5 A4:0.5 D5:1 C#5:0.5 A4:1", "R:0.5 A4:0.5 C#5:0.5 E5:1 D5:0.5 C#5:1",
       "B4:1 G4:0.5 B4:0.5 E5:1 D5:0.5 B4:0.5", "A4:2.5 R:1.5"]
M_B = ["D5:1.5 C#5:0.5 B4:1 F#4:1", "A4:1.5 C#5:0.5 A4:1 F#4:1", "G4:1 B4:1 D5:1 E5:1", "F#5:2.5 E5:0.5 D5:1",
       "E5:1.5 D5:0.5 B4:1 G4:1", "A4:1.5 C#5:0.5 E5:1 F#5:1", "G5:1.5 F#5:0.5 E5:1 D5:1", "E5:2 R:0.5 A4:0.5 B4:0.5 C#5:0.5"]
M_C = ["D5:0.5 B5:1 A5:0.5 G5:1 F#5:0.5 G5:0.5", "A5:1.5 E5:0.5 E5:1 C#5:0.5 D5:0.5",
       "C#5:0.5 F#5:1 E5:0.5 F#5:1 A5:1", "F#5:3 R:0.5 D5:0.5",
       "D5:0.5 B5:1 A5:0.5 G5:1 F#5:0.5 G5:0.5", "A5:1.5 B5:0.5 C#6:1 A5:1",
       "D6:1.5 C#6:0.5 A5:1 F#5:1", "A5:2.5 R:1.5"]
# 2回目のAメロは、後半の旋律を少し変える（同じくり返しにしない）
M_A2 = M_A[:4] + ["R:0.5 F#4:0.5 A4:0.5 D5:1 E5:0.5 F#5:1", "R:0.5 E5:0.5 F#5:0.5 E5:1 C#5:0.5 A4:1",
                  "B4:1 D5:0.5 E5:0.5 G5:1 F#5:0.5 E5:0.5", "E5:2.5 R:1.5"]
M_BR = ["F#4:2 B4:1 D5:1", "D5:1.5 B4:0.5 G4:2", "A4:2 F#4:1 A4:1", "E5:3 R:1",
        "F#5:2 E5:1 D5:1", "D5:1.5 E5:0.5 B4:2", "G5:2 F#5:1 E5:1", "E5:2 R:2"]
M_OUT = ["E5:0.5 C#6:1 B5:0.5 A5:2", "B5:1.5 C#6:0.5 D#6:2", "E6:4", "R:4"]
def f_lead(si, s, pr, k):
    if s == "intro": return " ".join(M_C[:3]) + " F#5:2 R:2"
    if s == "verse": return " ".join(M_A if si < 5 else M_A2)
    if s == "pre": return " ".join(M_B)
    if s == "chorus":
        t = " ".join(M_C).split()
        if k == 2: t = t[:-2] + ["A5:2", "R:2"]  # 最後のサビの終わりは outro へつなぐ
        return " ".join(tr(x, k) for x in t)
    if s == "inter": return "R:16"
    if s == "bridge": return " ".join(M_BR)
    if s == "outro": return " ".join(M_OUT)
# ベル: サビで旋律を同じ高さで重ねる（きらめき）。間奏では短い合いの手。
def f_bell(si, s, pr, k):
    if s == "chorus": return " ".join(tr(x, k) for x in " ".join(M_C).split())
    if s == "inter": return "F#5:0.5 A5:0.5 D6:1 R:2 G5:0.5 B5:0.5 D6:1 R:2 F#5:0.5 A5:0.5 D6:1 R:2 E5:0.5 A5:0.5 C#6:2 R:1"
    if s == "outro": return "R:8 " + " ".join(tr(x, 2) for x in "D6:4 R:4".split())
    return f"R:{fmt(4 * len(pr))}"

# ---------------- ピアノ（3声） ----------------
def piano(voice):
    def f(si, s, pr, k):
        out = []
        for i, ch in enumerate(pr):
            v = voicing(ch, 62)
            if voice == 3: n = nm(root_in(ch, 50))  # 左手（D3〜C#4。ベースと重ねない）
            else: n = nm(v[voice])
            if s == "intro":
                out += [f"{n}:4"] if i < 3 else [f"{n}:2", "R:2"]
            elif s in ("verse",):
                out += ([f"{n}:2", f"{n}:2"] if voice == 3 else ["R:0.5", f"{n}:1", f"{n}:0.5", "R:0.5", f"{n}:1", f"{n}:0.5"])
            elif s == "pre":
                out += ([f"{n}:1.5", f"{n}:0.5", f"{n}:2"] if voice == 3 else [f"{n}:1.5", f"{n}:1", f"{n}:1.5"])
                if i == len(pr) - 1: out[-3:] = [f"{n}:1", f"{n}:1", "R:2"]
            elif s == "chorus":
                out += ([f"{n}:1.5", f"{n}:0.5", f"{n}:1", f"{n}:1"] if voice == 3 else [f"{n}:0.5"] * 8)
            elif s == "inter":
                out += ([f"{n}:2", f"{n}:2"] if voice == 3 else [f"{n}:0.5"] * 8)
            elif s == "bridge":
                out += [f"{n}:4"] if not (i == len(pr) - 1) else [f"{n}:2", "R:2"]
            elif s == "outro":
                out += [f"{n}:4"] if i < 3 else ["R:4"]
        return " ".join(out)
    return f

# ---------------- ギター（2声。長めの音で弾く） ----------------
def guitar(voice):
    def f(si, s, pr, k):
        out = []
        for i, ch in enumerate(pr):
            v = voicing(ch, 54); n = nm(v[voice + 1])
            if s in ("intro", "bridge") or (s == "verse" and si < 5): out += ["R:4"]
            elif s == "verse": out += ["R:1", f"{n}:1.5", f"{n}:1.5"]
            elif s == "pre": out += [f"{n}:2", f"{n}:2"] if i < len(pr) - 1 else [f"{n}:2", "R:2"]
            elif s in ("chorus", "inter"): out += [f"{n}:1.5", f"{n}:1", f"{n}:1.5"]
            elif s == "outro": out += [f"{n}:4"] if i < 3 else ["R:4"]
        return " ".join(out)
    return f

# ---------------- 弦（2声） ----------------
def strings(voice):
    def f(si, s, pr, k):
        out = []
        for i, ch in enumerate(pr):
            v = voicing(ch, 70 if voice == 0 else 55); n = nm(v[2] if voice == 0 else v[0])
            if s in ("pre", "chorus", "bridge") or (s == "verse" and si >= 5 and i >= 4) or (s == "outro" and i < 3):
                out += [f"{n}:4"] if not (s in ("pre", "bridge") and i == len(pr) - 1) else [f"{n}:2", "R:2"]
            else: out += ["R:4"]
        return " ".join(out)
    return f

# ---------------- ベース ----------------
def f_bass(si, s, pr, k):
    out = []
    for i, ch in enumerate(pr):
        r = root_in(ch, 28); nx = pr[i + 1] if i + 1 < len(pr) else ch; rn = root_in(nx, 33)
        a = nm(r); o = nm(r + 12); f5 = nm(r + 7)
        appr = nm(rn - 1 if rn > r else rn + 1) if rn != r else f5  # 次のコードへ半音で寄る
        last = i == len(pr) - 1
        if s == "intro": out += ["R:4"] if i < 2 else [f"{a}:1.5", f"{a}:0.5", f"{f5}:1", f"{o}:1"]
        elif s == "verse": out += [f"{a}:1.5", f"{a}:0.5", f"{f5}:1", f"{o}:0.5", f"{appr}:0.5"]
        elif s == "pre": out += [f"{a}:2", f"{f5}:1", f"{appr}:1"] if not last else [f"{a}:1", f"{a}:1", "R:2"]
        elif s == "chorus": out += [f"{a}:0.5"] * 6 + [f"{o}:0.5", f"{appr}:0.5"]
        elif s == "inter": out += [f"{a}:1.5", f"{a}:0.5", f"{o}:1", f"{f5}:1"]
        elif s == "bridge": out += [f"{a}:4"] if not last else [f"{a}:2", "R:2"]
        elif s == "outro": out += [f"{a}:4"] if i < 3 else ["R:4"]
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
for si, (s, pr, k) in enumerate(SEC):
    kb, sb, hb, cb, tb = [], [], [], [], []
    n = len(pr)
    for b in range(n):
        last = b == n - 1; cr = "R:4"; tm = None
        if s == "intro":
            kk, sn, hh = Z, Z, Z
            if b == 2: kk = "X.....x.X......."; hh = "x.x.x.x.x.x.x.x."; sn = "....x.......x..."
            if b == 3: kk = "X.....x.X......."; sn = "....x...x.xxXXXX"; hh = "x.x.x.x........."; tm = "............xxXX"
        elif s == "verse":
            kk = "X.....x.X......." if b % 2 == 0 else "X.....x.X.x....."; sn = "....X.......X..."
            hh = "x.x.x.x.x.x.x.x." if si < 5 else "x.xxx.x.x.xxx.x."
            if b == 0: cr = "g:X..............."
            if b == 3: sn = "....X.......X.o."
            if last: sn = "....X.......xxXX"; tm = None
        elif s == "pre":
            kk = "X.....x.X.x....."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."
            if b == 0: cr = "g:X..............."
            if b == 6: sn = "....X.x.X.x.X.x."; hh = "x.x.x.x.x.x.x.x."
            if last: kk = "X..............."; sn = "........xxxxXXXX"; hh = "x.x.x.x........."; tm = "............xxXX"
        elif s == "chorus":
            kk = "X...X...X...X..."; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."
            if b % 4 == 0: cr = "g:X..............."
            if b == 3: sn = "....X.......X.xx"
            if last: sn = "....X...x.xxXXXX" if k == 0 else "X..............."; tm = "........xx..xxXX" if k == 0 else None
            if last and k == 2: kk = "X..............."; hh = Z
        elif s == "inter":
            kk = "X.....x.X......."; sn = "....X.......X..."; hh = "xxxxxxxxxxxxxxxx"
            if b == 0: cr = "g:X..............."
            if last: sn = "....X...xxxxXXXX"; tm = "............xxXX"
        elif s == "bridge":
            kk = "X.......X......." if b < 6 else "X.....x.X.x....."; sn = Z if b < 4 else "........X......."; hh = "x...x...x...x..."
            if b == 6: sn = "....X.......X..."
            if last: kk = "X.x.X..........."; sn = "X.x.X..........."; hh = Z; cr = "R:4"
        elif s == "outro":
            kk = "X...X...X...X..." if b < 2 else ("X..............." if b == 2 else Z)
            sn = "....X.......X..." if b < 2 else Z; hh = "x.O.x.O.x.O.x.O." if b < 2 else Z
            if b == 0 or b == 2: cr = "g:X..............."
        if s == "chorus" and k == 2 and b == 0: cr = "g:X..............."
        if cr != "R:4": hh = "." + hh[1:]
        if tm: hh = "".join("." if tm[j] in "xX" or j >= tm.index(next(c for c in tm if c in "xX")) else hh[j] for j in range(16))
        kb.append("g:" + kk); sb.append("g:" + sn); hb.append("g:" + hh); cb.append(cr)
        tb += tomtok(tm) if tm else ["R:4"]
    KICK.append(kb); SNARE.append(sb); HAT.append(hb); CRASH.append(cb); TOM.append(tb)

PARTS = []
def add(inst, role, vol, pan, secs, **kw):
    d = {"instrument": inst, "role": role, "volume": vol, "pan": pan, "notes": cat(secs, role)}; d.update(kw); PARTS.append(d)
A = ARC
add("lead", "旋律（笛）", 0.26, 0, per(f_lead), barGain=A, reverb=0.22, gainDb=2, breath=True)
add("bell", "きらめき（ベル）", 0.09, 0.25, per(f_bell), barGain=A, reverb=0.3)
add("piano", "ピアノ（上）", 0.13, -0.25, per(piano(2)), barGain=A, reverb=0.18)
add("piano", "ピアノ（中）", 0.12, -0.25, per(piano(1)), barGain=A, reverb=0.18)
add("piano", "ピアノ（下）", 0.12, -0.25, per(piano(0)), barGain=A, reverb=0.18)
add("guitar", "ギター（左）", 0.1, -0.8, per(guitar(0)), barGain=A, amp="jpopClean", chorus=0, reverb=0.15)
add("guitar", "ギター（右）", 0.1, 0.8, per(guitar(1)), barGain=A, amp="jpopClean", chorus=0, reverb=0.15, push=0.012)
add("strings", "弦（上）", 0.1, 0.6, per(strings(0)), barGain=A, reverb=0.25)
add("strings", "弦（下）", 0.09, -0.6, per(strings(1)), barGain=A, reverb=0.25)
add("bass", "ベース", 0.3, 0, per(f_bass), barGain=A)
add("kick", "キック", 0.3, 0, KICK, barGain=A)
add("snare", "スネア", 0.26, 0, SNARE, barGain=A, push=0.02)
add("hihat", "ハイハット", 0.09, 0, HAT, barGain=A, push=-0.008)
add("crash", "クラッシュ", 0.1, 0, CRASH, barGain=A)
add("tom", "タム", 0.14, 0, TOM, barGain=A, reverb=0)

song = {"title": "夏色シグナル（仮）",
        "description": "（仮）夏を感じる爽快なポップ。キュンとする恋の曲。BPM150・ニ長調、最後のサビでホ長調へ転調。入り方: 1（サビの旋律をピアノと笛だけで先に聞かせる）。終わり方: クラッシュ一発で止めて余韻。動機: D5:0.5 B5:1 A5:0.5（サビ頭の6度の跳躍）。",
        "bpm": 150, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "pop", "human": 0.3, "dynamics": "natural", "autoAccompaniment": False,
        "parts": PARTS}
json.dump(song, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars")
