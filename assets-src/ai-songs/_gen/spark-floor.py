# 『スパーク・フロア』（仮）: ダンス × ロック のインスト。BPM126・ト短調・120小節（約3分49秒）。2026-10-15、人間の指示「ダンスとロックを融合した曲を」。
# ダンスの側: 4つ打ちのキック、裏拍のオープンハイハット、オクターブで跳ねるベース、キックに合わせて沈むシンセの厚い和音（ダッキング）、
#   16分の FM エレピのアルペジオ（ピンポンディレイ）、ブレイクとせり上げ（スネアの連打）。
# ロックの側: 左右の歪みギター（Aメロは付点4分のシンコペ、サビは8分で押す）、サビの旋律はリードギター（warm-lead-b。ビブラート・チョーキングなし）、
#   バンドの生ドラムの音色で叩く2・4拍目。サビはリードギターに FM ベル（1オクターブ上）を重ねる。Bメロの旋律はピアノ。
# 構成: イントロ8 → ビルド8 → Aメロ16 → Bメロ8 → サビ16 → ブレイク8 → Aメロ8 → Bメロ8 → サビ16 → ブリッジ8（ブレイクダウン）→ 最後のサビ16（一発で終わる）
# 使い方: python3 spark-floor.py <出力.json>
# 書き出し: node tools/composer/song.mjs build assets-src/ai-songs/spark-floor.json --wav --edition modern --bass pick --piano salamander --guitar emily --master-preset edm --master -13.5（点数 8.14）
import json, os, sys
KARAOKE = os.environ.get("KARAOKE") == "1"   # 1 なら重音テトの歌入り版の伴奏（spark-floor-vocal.py）

def fmt(x): return ("%.4f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FL = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
def md(n):
    for f, s in FL.items(): n = n.replace(f, s) if n.startswith(f) else n
    i = 2 if len(n) > 2 and n[1] == "#" else 1
    return N.index(n[:i]) + 12 * (int(n[i:]) + 1)
def split_ch(ch):
    r = ch[:2] if len(ch) > 1 and ch[1] in "#b" else ch[:1]
    return N.index(FL.get(r, r)), ch[len(r):]
def chord_pcs(ch):
    r, q = split_ch(ch)
    if q.startswith("maj7"): iv = [0, 4, 7, 11]
    elif q.startswith("m7"): iv = [0, 3, 7, 10]
    elif q.startswith("m"): iv = [0, 3, 7]
    elif q.startswith("7"): iv = [0, 4, 7, 10]
    else: iv = [0, 4, 7]
    return [(r + x) % 12 for x in iv]
def root_in(ch, lo): return lo + ((chord_pcs(ch)[0] - lo) % 12)
def tones_from(ch, lo):
    pcs = chord_pcs(ch)[:3]; r = pcs[0]; base = lo + ((r - lo) % 12)
    return sorted(base + o + ((p - r) % 12) for o in (0, 12) for p in pcs)
def voicing(ch, center):
    pcs = chord_pcs(ch); pcs = pcs[1:] if len(pcs) == 4 else pcs   # 4和音は根音を抜いて 3度・5度・7度
    best = None
    for inv in range(3):
        o = pcs[inv:] + pcs[:inv]; cur = center - 7; v = []
        for p in o:
            x = cur + ((p - cur) % 12); v.append(x); cur = x + 1
        sc = abs(sum(v) / 3 - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]
def sh(tok, k):
    if tok.startswith("R:") or k == 0: return tok
    n, rest = tok.split(":", 1); return nm(md(n) + k) + ":" + rest

VERSE = "Gm Gm Ebmaj7 F Gm Gm Cm D7".split()
PRE = "Cm D Eb F Cm D Eb D7".split()
CHO = "Eb F Dm Gm Eb F Gm Gm".split()
BRI = "Ebmaj7 Ebmaj7 Dm7 Dm7 Cm7 Cm7 D D7".split()
SEC = [("intro", VERSE, 0), ("build", VERSE, 0), ("verse", VERSE, 0), ("verse", VERSE, 1), ("pre", PRE, 0),
       ("chorus", CHO, 0), ("chorus", CHO, 1), ("break", VERSE, 0), ("verse", VERSE, 2), ("pre", PRE, 1),
       ("chorus", CHO, 0), ("chorus", CHO, 1), ("bridge", BRI, 0), ("chorus", CHO, 2), ("chorus", CHO, 3)]
bars = []
for si, (s, pr, n) in enumerate(SEC):
    for i, c in enumerate(pr): bars.append(dict(kind=s, chord=c, i=i, n=n, si=si, L=len(pr)))
NB = len(bars); assert NB == 120

# ---- 旋律（オリジナル）----
M_V = ["R:0.5 D5:0.5 D5:0.5 Bb4:0.5 C5:1 Bb4:0.5 G4:0.5", "A4:1 Bb4:0.5 A4:0.5 G4:2", "R:0.5 G4:0.5 Bb4:0.5 D5:0.5 Eb5:1 D5:0.5 Bb4:0.5",
       "C5:1.5 A4:0.5 F4:2", "R:0.5 D5:0.5 D5:0.5 F5:0.5 G5:1 F5:0.5 D5:0.5", "F5:1 D5:0.5 C5:0.5 Bb4:2",
       "C5:0.5 Eb5:0.5 G5:1 F5:0.5 Eb5:0.5 C5:1", "D5:2 F#4:1 A4:1"]
M_P = ["G4:1 G4:0.5 C5:0.5 Eb5:2", "F#4:1 A4:0.5 D5:0.5 F#5:2", "G5:1 F5:0.5 Eb5:0.5 Bb4:2", "A4:1 C5:0.5 F5:0.5 A5:2",
       "G5:1 Eb5:0.5 G5:0.5 C6:2", "A5:1 F#5:0.5 A5:0.5 D6:2", "Bb5:2 G5:2", "F#5:2 A5:1 R:1"]
M_C = ["G5:1.5 F5:0.5 Eb5:1 G5:1", "A5:1.5 G5:0.5 F5:1 C5:1", "D5:1 F5:1 A5:1 F5:1", "G5:3 R:1",
       "Bb5:1.5 A5:0.5 G5:1 Eb5:1", "F5:1.5 G5:0.5 A5:1 C6:1", "Bb5:2 A5:1 F5:1", "G5:3 R:1"]
M_C2 = M_C[:6] + ["Bb5:1 A5:1 G5:1 F5:1", "G5:4"]
M_B = ["G5:4", "Bb5:2 A5:2", "F5:4", "A5:4", "Eb5:4", "G5:2 F5:2", "F#5:4", "A5:2 C6:2"]
for m in (M_V, M_P, M_C, M_C2, M_B):
    for x in m: assert abs(sum(float(t.split(":")[1]) for t in x.split()) - 4) < 1e-9, x

PARTS, ORDER = {}, []
def part(key, inst, role, vol, pan, **kw):
    PARTS[key] = dict(meta=dict(instrument=inst, role=role, volume=vol, pan=pan, **kw), bars=[None] * NB); ORDER.append(key)
def put(key, bi, toks):
    if isinstance(toks, str): toks = toks.split()
    t = 0.0
    for x in toks:
        if x.startswith("g:"): assert len(x) == 18, x; t += 4; continue
        d = x.split(":")[1]; t += float("".join(c for c in d if c.isdigit() or c == "."))
    assert abs(t - 4) < 1e-6, (key, bi, bars[bi]["kind"], toks)
    PARTS[key]["bars"][bi] = " ".join(toks)

DR = -6
part("lead", "leadGuitar", "旋律（リードギター）", 0.16, 0.08, gainDb=3, guitarTone="warm-lead-b", humanPitch=0, autoScoop=False)
part("pmel", "piano", "旋律（ピアノ・Bメロ）", 0.2, -0.05, reverb=0.2, gainDb=2)
part("bell", "fmBell", "きらめき（FMベル）", 0.07, 0.3, reverb=0.35)
part("arp", "fmEpiano", "アルペジオ（FMエレピ）", 0.1, -0.35, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.22, "feedback": 0.3}])
part("gl", "distGuitar", "ギター（左）", 0.07, -0.85, amp="hardrock", ampDrive=0.8, ampTone=-3, chorus=0, reverb=0.1)
part("gr", "distGuitar", "ギター（右）", 0.07, 0.85, amp="hardrock", ampDrive=0.8, ampTone=-3, chorus=0, reverb=0.1, push=0.008)
part("sawh", "unisonSaw", "厚いシンセ（上）", 0.06, 0.5, reverb=0.2, duck=0.4)
part("sawl", "unisonSaw", "厚いシンセ（下）", 0.06, -0.5, reverb=0.2, duck=0.4)
part("ph", "piano", "ピアノ和音（上）", 0.09, 0.25, reverb=0.25)
part("pl", "piano", "ピアノ和音（下）", 0.09, -0.25, reverb=0.25)
part("bass", "bass", "ベース（オクターブ）", 0.3, 0, duck=0.25)
part("kick", "kick", "キック（4つ打ち）", 0.3, 0, gainDb=DR)
part("snare", "snare", "スネア", 0.26, 0, push=0.015, gainDb=DR)
part("hihat", "hihat", "ハイハット", 0.09, 0, push=-0.008, gainDb=DR)
part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=DR)
part("tom", "tom", "タム", 0.14, 0, reverb=0, gainDb=DR)
R4 = "R:4"
Z = "................"
FOUR = "X...X...X...X..."

def tomtok(tm, pit=("E3", "E3", "C3", "C3", "A2", "A2")):
    hits = [j for j, c in enumerate(tm) if c in "xX"]; toks = []; k = 0
    for c in tm:
        if c in "xX": toks.append(pit[min(len(pit) - 1, k * len(pit) // max(1, len(hits)))] + ":0.25" + ("!" if c == "X" else "")); k += 1
        else: toks.append("R:0.25")
    return toks

def drums(b):
    s, i, L, n = b["kind"], b["i"], b["L"], b["n"]; last = i == L - 1
    kk, sn, hh, crash, tm = Z, Z, Z, False, None
    if s == "intro":
        kk = FOUR; hh = "..o...o...o...o." if i >= 4 else Z
        if i == 7: sn = "........x.x.xxXX"
    elif s == "build":
        kk = FOUR; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."; crash = i == 0
        if last: sn = "x.x.x.x.xxxxXXXX"; hh = Z
    elif s == "verse":
        kk = FOUR; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O." if n != 0 or i >= 8 else "..O...O...O...O."
        crash = i == 0
        if i % 8 == 7 and not last: sn = "....X.......X.oX"
        if last and n != 1: sn = "....X...o.x.X.XX"
    elif s == "pre":
        kk = FOUR if i < 6 else ("X.X.X.X.X.X.X.X." if i == 6 else "XXXXXXXXXXXXXXXX")
        sn = "....X.......X..." if i < 4 else ("x.x.x.x.x.x.x.x." if i < 6 else "xxxxxxxxXXXXXXXX")
        hh = "xxxxxxxxxxxxxxxx" if i < 4 else Z; crash = i == 0
        if last: kk = "X.X.X.X.X.X....."
    elif s == "chorus":
        kk = FOUR; sn = "....X.......X..."; hh = "xxOxxxOxxxOxxxOx"; crash = i % 4 == 0
        if i % 8 == 7 and not last: sn = "....X.......xxXX"; hh = hh[:12] + "...."
        if last and n in (1,) and b["si"] < 12: sn = "....X...xxxxXXXX"; tm = "............XXXX"
        if last and n == 3: kk = "X..............."; sn = Z; hh = Z; crash = True
    elif s == "break":
        kk = Z if i < 4 else FOUR; hh = "..O...O...O...O."; crash = i == 4
        if last: sn = "....X...o.x.X.XX"
    elif s == "bridge":
        kk = Z if i < 6 else FOUR; hh = Z if i < 4 else "..o...o...o...o."
        if i == 6: sn = "x.x.x.x.x.x.x.x."
        if i == 7: sn = "xxxxxxxxXXXXXXXX"; kk = "XXXXXXXXXXXXXXXX"; hh = Z
        crash = i == 0
    if tm:
        first = next(j for j, c in enumerate(tm) if c in "xX")
        sn = sn[:first] + "".join("." if tm[first + j] in "xX" else c for j, c in enumerate(sn[first:])); hh = hh[:first] + "." * (16 - first)
    if crash: hh = "." + hh[1:]
    return kk, sn, hh, crash, tm

ARC = []
for b in bars:
    s, i, L, n = b["kind"], b["i"], b["L"], b["n"]; f = i / max(1, L - 1)
    g = {"intro": 0.72 + 0.1 * f, "build": 0.82 + 0.1 * f, "verse": 0.86, "pre": 0.88 + 0.12 * f, "chorus": [1.0, 1.0, 1.04, 1.06][n],
         "break": 0.8, "bridge": 0.72 + 0.2 * f}[s]
    ARC.append(round(g, 3))

for bi, b in enumerate(bars):
    s, ch, i, n, L = b["kind"], b["chord"], b["i"], b["n"], b["L"]; last = i == L - 1
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB else ch
    final = s == "chorus" and n == 3 and last
    # 旋律
    if KARAOKE:   # 歌入り版の伴奏: 歌のある所（Aメロ・Bメロ・サビ）は旋律の楽器を鳴らさない。ブレイクはリードギターが Aメロの旋律を弾く
        put("lead", bi, M_V[i].split() if s == "break" else [R4]); put("pmel", bi, [R4])
        put("bell", bi, M_B[i] if s == "bridge" else [R4])
    else:
     if s == "verse": put("lead", bi, M_V[i % 8].split() if not (n == 0 and i < 8) else [R4])
     elif s == "chorus":
        mel = (M_C2 if n % 2 == 1 else M_C)[i]
        put("lead", bi, mel.split() if not final else ["G5:4"])
     else: put("lead", bi, [R4])
     if s == "verse" and n == 0 and i < 8: put("pmel", bi, M_V[i])        # 1回目のAメロの前半はピアノ
     elif s == "pre": put("pmel", bi, M_P[i])
     else: put("pmel", bi, [R4])
     if s == "chorus": put("bell", bi, [sh(x, 12) for x in (M_C2 if n % 2 == 1 else M_C)[i].split()] if not final else "G6:4")   # ベルは1オクターブ上
     elif s == "bridge": put("bell", bi, M_B[i])
     else: put("bell", bi, [R4])
    # アルペジオ（16分）
    t = tones_from(ch, 62)
    arp_on = s in ("intro", "build", "verse", "chorus", "break") or (s == "bridge" and i >= 2)
    if arp_on and not final:
        pat = [0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 1, 3, 5, 4]
        put("arp", bi, [f"{nm(t[j % len(t)])}:0.25" for j in pat])
    elif final: put("arp", bi, [f"{nm(t[0])}:4"])
    else: put("arp", bi, [R4])
    # 歪みギター
    r = nm(root_in(ch, 40))
    if s == "build": g = [f"{r}:0.5"] * 8 if i >= 4 else [R4]
    elif s == "verse": g = [f"{r}:1.5", f"{r}:1.5", f"{r}:1"] if not (n == 0 and i < 8) else [R4]
    elif s == "pre": g = [f"{r}:1.5", f"{r}:1.5", f"{r}:1"] if i < 4 else [f"{r}:0.5"] * 8
    elif s == "chorus": g = [f"{r}:0.5"] * 8 if not final else [f"{r}:4"]
    elif s == "break": g = [f"{r}:4"] if i >= 4 else [R4]
    elif s == "bridge": g = [f"{r}:4"] if i >= 6 else [R4]
    else: g = [R4]
    put("gl", bi, g); put("gr", bi, g if not (s == "build") else [R4])
    # シンセの厚い和音・ピアノの和音
    v = voicing(ch, 66)
    saw = s in ("pre", "chorus", "bridge") and not (s == "pre" and i < 4)
    put("sawh", bi, [f"{nm(v[2])}:4"] if saw else [R4]); put("sawl", bi, [f"{nm(v[0])}:4"] if saw else [R4])
    pv = voicing(ch, 60)
    if s in ("bridge", "break") or (s == "pre" and i < 4): pp = (f"{nm(pv[2])}:2 {nm(pv[2])}:2", f"{nm(pv[0])}:2 {nm(pv[0])}:2")
    elif final: pp = (f"{nm(pv[2])}:4", f"{nm(pv[0])}:4")
    else: pp = (R4, R4)
    put("ph", bi, pp[0]); put("pl", bi, pp[1])
    # ベース（オクターブで跳ねる）
    lo = root_in(ch, 28); a, o = nm(lo), nm(lo + 12)
    rn = root_in(nxt, 28); ap = nm(rn - 1 if rn > lo else rn + 1) if rn != lo else nm(lo + 7)
    if final: bs = [f"{a}:4"]
    elif s in ("chorus", "build") or (s == "pre" and i >= 4): bs = [a + ":0.5", o + ":0.5"] * 3 + [a + ":0.5", ap + ":0.5"] if (s != "build" or i >= 4) else [a + ":4"]
    elif s == "verse": bs = [a + ":0.75", a + ":0.25", o + ":0.5", a + ":0.5", a + ":0.75", a + ":0.25", o + ":0.5", ap + ":0.5"]
    elif s == "pre": bs = [f"{a}:1.5", f"{a}:1.5", f"{a}:1"]
    elif s == "break": bs = [f"{a}:4"] if i < 4 else [a + ":0.5", o + ":0.5"] * 4
    elif s == "bridge": bs = [f"{a}:4"] if i < 6 else [a + ":0.5"] * 8
    elif s == "intro": bs = [f"{a}:4"] if i >= 4 else [R4]
    else: bs = [R4]
    if s == "build" and i < 4: bs = [R4]
    put("bass", bi, bs)
    kk, sn, hh, crash, tm = drums(b)
    put("kick", bi, ["g:" + kk]); put("snare", bi, ["g:" + sn]); put("hihat", bi, ["g:" + hh])
    put("crash", bi, ["g:X..............."] if crash else [R4])
    put("tom", bi, tomtok(tm) if tm else [R4])

parts = []
for key in ORDER:
    p = PARTS[key]; assert all(x is not None for x in p["bars"]), key
    d = dict(p["meta"]); d["notes"] = " ".join(p["bars"]); d["barGain"] = ARC; parts.append(d)
song = {"title": "スパーク・フロア（歌入り版の伴奏・仮）" if KARAOKE else "スパーク・フロア（仮）",
        "description": "（仮）ダンスとロックを混ぜたインスト。BPM126・ト短調・約3分49秒。4つ打ちのキック・裏拍のオープンハイハット・オクターブで跳ねるベース・"
                       "キックに合わせて沈むシンセの和音・16分のFMエレピのアルペジオに、左右の歪みギターとリードギターの旋律（ビブラート・チョーキングなし）。"
                       "入り方: キックとアルペジオだけ → ギター → 全員。終わり方: 最後のサビの終わりで全員一発、のばして消える。",
        "bpm": 126, "beats": 4, "chords": " ".join(b["chord"] for b in bars), "barsPerChord": 1, "repeats": 1,
        "tone": "rock", "feel": "dance", "human": 0.2, "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False,
        "parts": parts}
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/spark-floor.json"
json.dump({"guitarWobble": False, **song}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(parts), "parts", NB, "bars", round(NB * 4 * 60 / 126), "sec")
