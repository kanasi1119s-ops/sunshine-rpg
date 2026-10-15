# 『ヘルタースケルター』（仮）: リズム&ブルース × ロック のインスト。BPM138・シャッフル（swing 0.55）・イ長調（ブルース）→ 最後の3回は全音上のロ長調。約3分57秒（136小節）。
# 2026-10-15、人間の指示「リズム&ブルースとロックを融合した曲でヘルタースケルターという曲を。4分ぐらい」。
# 曲名は同じ名前の有名な曲があるが、旋律・リフ・進行・構成はすべてこの曲のために作ったオリジナル（既存曲の旋律やリフは使っていない）。
# R&B の側: 12小節のブルースの形、ドローバーオルガンの旋律、ホーン隊（ブラス2本・オクターブ）の合いの手とキメ、ピアノの裏拍の和音、
#   ブギのベース（1・3・5・6・♭7）、ストップタイム（1拍目だけ全員で鳴らし、すきまをギターが埋める）。
# ロックの側: 左右の歪みギターのパワーコードのリフ、サビはリードギター（warm-lead-b。ビブラート・チョーキングなし）、ギターソロ24小節、強いバックビート。
# 構成: イントロ8 → Aメロ12 → サビ8 → Aメロ12（ホーン）→ サビ8 → ストップタイム8 → ギターソロ24 → ピアノソロ12 →
#   ブリッジ8（短調のハーフタイム）→ 全音上のAメロ12 → サビ8 → サビ8 → 終わり8（全員で一発）
# 使い方: python3 helter-skelter-rb.py <出力.json>
# 書き出し: node tools/composer/song.mjs build assets-src/ai-songs/helter-skelter-rb.json --wav --drums muldjord --bass finger
#   --piano salamander --orchestra vsco --guitar emily --master-preset rock-clean
import json, sys

def fmt(x): return ("%.4f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
def md(n):
    i = 2 if len(n) > 2 and n[1] == "#" else 1
    return N.index(n[:i]) + 12 * (int(n[i:]) + 1)
def croot(ch): return N.index(ch[:2]) if len(ch) > 1 and ch[1] == "#" else N.index(ch[0])
def cqual(ch): return ch[2:] if len(ch) > 1 and ch[1] == "#" else ch[1:]
def up(ch, k): return N[(croot(ch) + k) % 12] + cqual(ch)
def chord_pcs(ch):
    r = croot(ch); q = cqual(ch); minor = q.startswith("m")
    return [r, (r + (3 if minor else 4)) % 12, (r + 7) % 12] + ([(r + 10) % 12] if "7" in q else [])
def root_in(ch, lo): return lo + ((croot(ch) - lo) % 12)
def voicing(ch, center, n=3):
    pcs = chord_pcs(ch)
    pcs = [pcs[1], pcs[3], pcs[2]] if len(pcs) == 4 and n == 3 else pcs[:n]   # 7th の和音は 3度・7度・5度（根音はベースにまかせる）
    best = None
    for inv in range(len(pcs)):
        o = pcs[inv:] + pcs[:inv]; cur = center - 7; v = []
        for p in o:
            x = cur + ((p - cur) % 12); v.append(x); cur = x + 1
        sc = abs(sum(v) / len(v) - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]
def tr(tok, k):
    if tok.startswith("R:") or k == 0: return tok
    n, rest = tok.split(":", 1)
    return nm(md(n) + k) + ":" + rest

BLUES = "A7 A7 A7 A7 D7 D7 A7 A7 E7 D7 A7 E7".split()
CHO = "D7 D7 A7 A7 C7 D7 E7 E7".split()
BRI = "F#m7 Bm7 C#m7 F#m7 Bm7 C#m7 D7 F#7".split()
# (種類, コード, 転調の半音, 何回目)
SEC = [("intro", "A7 A7 A7 A7 A7 A7 E7 E7".split(), 0, 0),
       ("verse", BLUES, 0, 0), ("chorus", CHO, 0, 0), ("verse", BLUES, 0, 1), ("chorus", CHO, 0, 1),
       ("stop", "A7 A7 A7 A7 A7 A7 D7 E7".split(), 0, 0), ("gsolo", BLUES * 2, 0, 0), ("psolo", BLUES, 0, 0),
       ("bridge", BRI, 0, 0), ("verse", BLUES, 2, 2), ("chorus", CHO, 2, 2), ("chorus", CHO, 2, 3),
       ("outro", "A7 A7 A7 A7 D7 D7 A7 A7".split(), 2, 0)]
bars = []
for s, pr, k, n in SEC:
    for i, c in enumerate(pr): bars.append(dict(kind=s, chord=up(c, k), base=c, k=k, n=n, i=i, L=len(pr)))
NB = len(bars); assert NB == 136, NB

# ---- 旋律（オリジナル）----
VERSE_MEL = ["R:0.5 E5:0.5 G5:0.5 A5:1 G5:0.5 E5:1", "C5:0.5 C#5:0.5 A4:2 R:1", "R:0.5 A4:0.5 C5:0.5 D5:0.5 D#5:0.5 E5:1.5",
             "G5:0.5 E5:0.5 D5:0.5 C5:0.5 A4:2", "R:0.5 A5:0.5 C6:0.5 A5:1 F#5:0.5 A5:1", "F5:0.5 F#5:0.5 D5:2 R:1",
             "R:0.5 E5:0.5 G5:0.5 A5:1 G5:0.5 E5:1", "C#5:0.5 A4:0.5 G4:0.5 A4:2.5", "B4:0.5 D5:0.5 E5:0.5 G#5:1 B5:1.5",
             "A5:0.5 F#5:0.5 D5:0.5 C5:0.5 A4:1 F#4:1", "E5:0.5 C#5:0.5 A4:3", "R:2 E5:0.5 D5:0.5 B4:1"]
HOOK = ["A5:1 A5:0.5 F#5:0.5 A5:1 C6:1", "D6:1.5 C6:0.5 A5:2", "E5:1 E5:0.5 G5:0.5 A5:1 C#6:1", "E6:1.5 C#6:0.5 A5:2",
        "G5:1 G5:0.5 E5:0.5 G5:1 A#5:1", "A5:1 F#5:0.5 A5:0.5 C6:2", "B5:1 G#5:0.5 B5:0.5 D6:1 B5:1", "G#5:2 B5:1 R:1"]
BRI_MEL = ["C#5:2 E5:1 F#5:1", "D5:2 B4:1 A4:1", "G#4:2 B4:1 C#5:1", "A4:3 R:1",
           "F#5:2 E5:1 D5:1", "E5:2 C#5:1 B4:1", "A4:1 C5:1 D5:1 F#5:1", "A#4:2 C#5:2"]
# ホーンの合いの手（旋律の休みに入る。音と音は _ でつなぐ。根音からの半音、拍）
HORN_ANS = [(16, 0.5), (19, 0.5), (22, 1)]   # 3度 → 5度 → ♭7（下から駆け上がる）

def toks_sum(toks):
    t = 0.0
    for x in toks:
        if x.startswith("g:"): assert len(x) == 18, x; t += 4; continue
        d = x.split(":")[1]; t += float("".join(c for c in d if c.isdigit() or c == "."))
    return t

PARTS, ORDER = {}, []
def part(key, inst, role, vol, pan, **kw):
    PARTS[key] = dict(meta=dict(instrument=inst, role=role, volume=vol, pan=pan, **kw), bars=[None] * NB); ORDER.append(key)
def put(key, bi, toks):
    if isinstance(toks, str): toks = toks.split()
    assert abs(toks_sum(toks) - 4) < 1e-6, (key, bi, bars[bi]["kind"], toks)
    PARTS[key]["bars"][bi] = " ".join(toks)
def legato(toks):
    """休みに挟まれていない音どうしを _ でつなぐ（ブラスを1音ずつ切って「ポンポン」にしない。banned-sounds 14）。"""
    out = []
    for j, x in enumerate(toks):
        nxt = toks[j + 1] if j + 1 < len(toks) else "R"
        out.append(x + "_" if not x.startswith("R") and not nxt.startswith("R") and not x.endswith("_") else x)
    return out

DR = -5
part("organ", "drawbarOrgan", "旋律（オルガン）", 0.2, -0.1, reverb=0.2, gainDb=1)
part("lead", "leadGuitar", "サビ・ソロ・合いの手（リードギター）", 0.16, 0.12, gainDb=3, guitarTone="warm-lead-b", humanPitch=0, autoScoop=False)
part("hornh", "brass", "ホーン（上）", 0.13, 0.3, reverb=0.18)
part("hornl", "brass", "ホーン（下・オクターブ）", 0.11, -0.3, reverb=0.18)
part("p1", "piano", "ピアノ（和音・上）", 0.1, 0.2, reverb=0.12, pedal="chord")
part("p2", "piano", "ピアノ（和音・中）", 0.1, 0.2, reverb=0.12, pedal="chord")
part("p3", "piano", "ピアノ（和音・下）", 0.09, 0.2, reverb=0.12, pedal="chord")
part("psolo", "piano", "ピアノソロ", 0.2, 0.05, reverb=0.15, gainDb=2)
part("o1", "drawbarOrgan", "オルガン（和音・上）", 0.06, 0.45, reverb=0.2)
part("o2", "drawbarOrgan", "オルガン（和音・下）", 0.06, -0.45, reverb=0.2)
part("gl", "distGuitar", "ギター（左）", 0.07, -0.85, amp="hardrock", ampDrive=0.7, ampTone=-3, chorus=0, reverb=0.1)
part("gr", "distGuitar", "ギター（右）", 0.07, 0.85, amp="hardrock", ampDrive=0.7, ampTone=-3, chorus=0, reverb=0.1, push=0.008)
part("bass", "bass", "ベース（ブギ）", 0.3, 0)
part("kick", "kick", "キック", 0.3, 0, gainDb=DR)
part("snare", "snare", "スネア", 0.26, 0, push=0.02, gainDb=DR)
part("hihat", "hihat", "ハイハット", 0.09, 0, push=-0.008, gainDb=DR)
part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=DR)
part("ride", "crash", "ライド", 0.07, 0.2, gainDb=DR)
part("tom", "tom", "タム", 0.14, 0, reverb=0, gainDb=DR)
R4 = "R:4"

def fit4(ev):
    s = sum(d for _, d in ev)
    if s < 4: ev[-1] = (ev[-1][0], ev[-1][1] + 4 - s)
    elif s > 4:
        out, acc = [], 0.0
        for x, d in ev:
            if acc + d >= 4 - 1e-9: out.append((x, 4 - acc)); break
            out.append((x, d)); acc += d
        ev = out
    return [f"{nm(x)}:{fmt(d)}" for x, d in ev]
def to_chord_tone(x, ch):
    while x % 12 not in chord_pcs(ch): x -= 1
    return x

# ---- ギターソロ（ペンタトニック＋ブルーノート。チョーキング・ビブラートなし。長い音は和音の音）----
GL = [[(12, 0.5), (15, 0.5), (16, 0.5), (19, 0.5), (22, 1), (19, 1)],
      [(24, 1.5), (22, 0.5), (19, 0.5), (16, 0.5), (15, 0.5), (12, 0.5)],
      [(19, 0.5), (22, 0.5), (24, 0.5), (22, 0.5), (19, 0.5), (16, 0.5), (19, 1)],
      [(12, 0.25), (15, 0.25), (16, 0.25), (19, 0.25), (22, 0.25), (24, 0.25), (27, 0.25), (28, 0.25), (24, 2)],
      [(28, 1), (27, 0.5), (24, 0.5), (22, 0.5), (19, 0.5), (16, 1)],
      [(16, 0.5), (19, 0.5), (16, 0.5), (19, 0.5), (22, 0.5), (24, 0.5), (22, 1)]]
def gsolo_bar(b):
    i, ch = b["i"], b["chord"]; r = root_in(ch, 57)
    lick = GL[(i + (i // 12) * 3) % len(GL)]
    lift = 12 if (i >= 12 and i % 12 >= 8) else 0           # 2周目の終わりは1オクターブ上で山をつくる
    ev = [(r + o + lift, d) for o, d in lick]
    ev = [(x - 12 if x > 88 else x, d) for x, d in ev]
    if i == 23: ev = [(r + 12, 1), (r + 16, 1), (r + 19, 2)]   # E7 の上で終わり、ピアノへ渡す
    return fit4([(to_chord_tone(x, ch) if d >= 0.75 else x, d) for x, d in ev])

# ---- ピアノソロ（右手の8分のブギ。シャッフルで跳ねる）----
PL = [[7, 10, 12, 15, 16, 15, 12, 10], [12, 16, 19, 16, 12, 10, 7, 4], [15, 16, 19, 22, 24, 22, 19, 16], [24, 19, 16, 12]]
def psolo_bar(b):
    i, ch = b["i"], b["chord"]; r = root_in(ch, 60)
    if i == 11: return fit4([(r + 7, 1), (r + 4, 1), (r, 2)])
    lick = PL[i % 4]
    if len(lick) == 4: return fit4([(to_chord_tone(r + lick[0], ch), 2), (r + lick[1], 1), (r + lick[2], 1)])
    return fit4([(r + o, 0.5) for o in lick])

# ---- ドラム（1文字＝16分。8分の裏は swing で跳ねる）----
Z = "................"
def tomtok(tm, pit=("E3", "E3", "C3", "C3", "A2", "A2")):
    hits = [j for j, c in enumerate(tm) if c in "xX"]; toks = []; k = 0
    for c in tm:
        if c in "xX": toks.append(pit[min(len(pit) - 1, k * len(pit) // max(1, len(hits)))] + ":0.25" + ("!" if c == "X" else "")); k += 1
        else: toks.append("R:0.25")
    return toks
FILL_SMALL = ("....X.....o.X.XX", None)
FILL_TOM = ("....X...........", "........x.x.X.X.")
FILL_BIG = ("....X...o.x.X.X.", "............X.XX")
def drums(b, nxtkind):
    kind, i, L, n = b["kind"], b["i"], b["L"], b["n"]; last = i == L - 1
    kk, sn, hh, ride, crash, tm, fill = Z, Z, Z, False, False, None, None
    SH_K = ["X.....x.X.......", "X.....x.X.....x."]
    if kind == "intro":
        if i >= 4: kk = SH_K[i % 2]; sn = "....X.......X..."; hh = "X.x.X.x.X.x.X.x."; crash = i == 4
        if i == 3: sn = "........x.x.X.X."
    elif kind == "verse":
        kk = SH_K[i % 2]; sn = "....X.o.....X.o." if n >= 1 else "....X.......X..."
        hh = "X.x.X.x.X.x.X.x." if n == 0 else "X.x.X.x.X.x.X.O."
        crash = i == 0
    elif kind == "chorus":
        kk = "X...X.x.X...X.x." if i % 2 == 0 else "X.....x.X...X.x."; sn = "....X.......X..."; ride = True; crash = i % 4 == 0
    elif kind == "stop":
        if i < 6: kk = "X..............."; hh = "....o...o...o..."; crash = i % 2 == 0
        else: kk = SH_K[i % 2]; sn = "....X.......X..."; hh = "X.x.X.x.X.x.X.x."
    elif kind == "gsolo":
        kk = SH_K[i % 2] if i < 12 else "X...X.x.X...X.x."; sn = "....X.o.....X.o."
        if i < 12: hh = "X.x.X.x.X.x.X.O."
        else: ride = True
        crash = i % 12 == 0
    elif kind == "psolo":
        kk = "X.......X......."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."; crash = i == 0
    elif kind == "bridge":
        kk = "X.......X.....x."; sn = "........X......."; ride = True; crash = i in (0, 4)
        if i == 7: kk = "X...X...X...X..."; sn = "X.X.X.X.X.X.XXXX"; ride = False
    elif kind == "outro":
        if i < 6: kk = "X...X.x.X...X.x."; sn = "....X.......X..."; ride = True; crash = i % 4 == 0
        elif i == 6: kk = "X...X...X...X..."; sn = "....X...X.X.X.X."
        else: kk = "X..............."; crash = True
    busy = kind in ("verse", "chorus", "gsolo", "psolo") or (kind == "intro" and i >= 4) or (kind == "stop" and i >= 6) or (kind == "outro" and i < 6)
    if busy:
        if last and kind != "outro": fill = FILL_BIG
        elif kind == "outro" and i == 5: fill = FILL_TOM
        elif i % 4 == 3 and kind != "stop": fill = FILL_SMALL if i % 8 != 7 else FILL_TOM
    if kind == "outro" and i == 6: tm = "........x.x.X.X."
    if fill:
        fs, ft = fill
        sn = "".join(f if f != "." else sn[j] for j, f in enumerate(fs))
        if ft: tm = ft; ride = False
        hh = hh[:8] + "........" if ft else hh[:12] + "...."
    if tm:
        first = next(j for j, c in enumerate(tm) if c in "xX")
        sn = sn[:first] + "".join("." if tm[first + j] in "xX" else c for j, c in enumerate(sn[first:]))
        hh = hh[:first] + "." * (16 - first)
    if crash: hh = "." + hh[1:]
    return kk, sn, hh, ride, crash, tm

ARC = []
for b in bars:
    s, i, L, n = b["kind"], b["i"], b["L"], b["n"]; f = i / max(1, L - 1)
    g = {"intro": 0.8 + 0.1 * f, "verse": [0.82, 0.88, 0.95][min(n, 2)], "chorus": [1.0, 1.0, 1.03, 1.06][n], "stop": 0.86 + 0.1 * f,
         "gsolo": 0.92 + 0.1 * f, "psolo": 0.86, "bridge": 0.75 + 0.15 * f, "outro": 1.04}[s]
    ARC.append(round(min(1.06, g), 3))

for bi, b in enumerate(bars):
    s, ch, k, n, i, L = b["kind"], b["chord"], b["k"], b["n"], b["i"], b["L"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB else ch
    nxtkind = bars[bi + 1]["kind"] if bi + 1 < NB else None
    last = i == L - 1
    r = root_in(ch, 57)
    # 旋律（オルガン）: Aメロ
    put("organ", bi, [tr(x, k) for x in VERSE_MEL[i].split()] if s == "verse" else [R4])
    # リードギター: サビ・ストップタイムの合いの手・ソロ・ブリッジの終わり・イントロ後半
    if s == "chorus":
        put("lead", bi, [tr(x, k - 12) for x in HOOK[i].split()])   # ホーン（上）と同じ高さで重ねる（ギター＋ホーンのユニゾン。刺さる高音を避ける）
    elif s == "stop" and i < 6:
        rr = root_in(ch, 57) + 12
        lick = [(rr + 3, 0.5), (rr + 4, 0.5), (rr + 7, 0.5), (rr + 10, 0.5), (rr + 12, 1)] if i % 2 == 0 else [(rr + 10, 0.5), (rr + 7, 0.5), (rr + 4, 0.5), (rr, 0.5), (rr + 7, 1)]
        put("lead", bi, ["R:1"] + [f"{nm(x)}:{fmt(d)}" for x, d in lick])
    elif s == "gsolo": put("lead", bi, gsolo_bar(b))
    elif s == "intro" and i >= 4: put("lead", bi, [f"{nm(r + 12)}:2", f"{nm(r + 16)}:1", f"{nm(r + 19)}:1"] if i < 7 else [f"{nm(r + 7)}:4"])
    else: put("lead", bi, [R4])
    # ホーン（上と、その1オクターブ下）
    hr = root_in(ch, 60)
    if s == "verse" and n >= 1 and i in (1, 3, 5, 7, 11):
        hs = ["R:2"] + legato([f"{nm(hr + o if hr + o <= md('C6') else hr + o - 12)}:{fmt(d)}" for o, d in (HORN_ANS if i != 11 else [(7, 0.5), (10, 0.5), (12, 0.5), (16, 0.5)])])
    elif s == "chorus":
        mel = [tr(x, k - 12) for x in HOOK[i].split()]
        hs = legato(mel)
    elif s == "stop" and i < 6: hs = [f"{nm(to_chord_tone(hr + 4, ch))}:2", "R:2"]
    elif s == "stop": hs = legato([f"{nm(hr + 4)}:2", f"{nm(hr + 7)}:2"])
    elif s == "bridge": hs = [f"{nm(voicing(ch, 64)[1])}:4"] if i >= 4 else [R4]
    elif s == "outro" and i == 7: hs = [f"{nm(hr + 4)}:4"]
    elif s == "intro" and i >= 6: hs = legato([f"{nm(hr + 4)}:2", f"{nm(hr + 7)}:2"])
    else: hs = [R4]
    assert abs(toks_sum(hs) - 4) < 1e-6, (bi, hs)
    put("hornh", bi, hs)
    put("hornl", bi, [x if x.startswith("R") else nm(md(x.split(":")[0]) - 12) + ":" + x.split(":", 1)[1] for x in hs])
    # ピアノの和音（2拍目・4拍目と、その前の裏拍。シャッフルで跳ねる）
    pv = voicing(ch, 64)
    comp = s in ("verse", "chorus", "gsolo") or (s == "intro" and i >= 4) or (s == "stop" and i >= 6) or (s == "outro" and i < 7)
    for key, v in zip(("p1", "p2", "p3"), sorted(pv, reverse=True)):
        if comp: put(key, bi, ["R:1", f"{nm(v)}:1", "R:0.5", f"{nm(v)}:0.5", f"{nm(v)}:1"])
        elif s == "stop": put(key, bi, [f"{nm(v)}:2", "R:2"])
        elif s == "bridge": put(key, bi, [f"{nm(v)}:2", f"{nm(v)}:2"])
        elif s == "outro" and i == 7: put(key, bi, [f"{nm(v)}:4"])
        else: put(key, bi, [R4])
    put("psolo", bi, psolo_bar(b) if s == "psolo" else [R4])
    # オルガンの和音（のばす）
    ov = voicing(ch, 60)
    org = s in ("chorus", "psolo", "bridge", "gsolo") or (s == "verse" and n >= 1) or (s == "intro" and i >= 4) or (s == "outro")
    put("o1", bi, [f"{nm(ov[2])}:4"] if org else [R4])
    put("o2", bi, [f"{nm(ov[0])}:4"] if org else [R4])
    # 歪みギター（パワーコードのリフ。根音だけ書く＝5度とオクターブは自動で重なる）
    gr = root_in(ch, 40)
    if s in ("verse", "gsolo") or (s == "intro") or (s == "outro" and i < 6) or (s == "stop" and i >= 6):
        g = [(gr, 1), (gr, 0.5), (gr + 3, 0.5), (gr + 5, 1), (gr + 3, 0.5), (gr, 0.5)] if i % 2 == 0 else [(gr, 1.5), (gr, 0.5), (gr + 7, 0.5), (gr + 5, 0.5), (gr + 3, 0.5), (gr, 0.5)]
        if s == "verse" and last: g = [(gr, 4)]
        g = [f"{nm(x)}:{fmt(d)}" for x, d in g]
    elif s == "chorus": g = [f"{nm(gr)}:2", f"{nm(gr)}:1.5", f"{nm(gr)}:0.5"]
    elif s == "stop": g = [f"{nm(gr)}:2", "R:2"]
    elif s == "bridge" and i >= 4: g = [f"{nm(gr)}:4"]
    elif s == "psolo" and i % 4 == 0: g = [f"{nm(gr)}:4"]
    elif s == "outro": g = [f"{nm(gr)}:4"] if i == 7 else [f"{nm(gr)}:2", f"{nm(gr)}:2"]
    else: g = [R4]
    if s == "intro" and i < 4: g = [f"{nm(x)}:{fmt(d)}" for x, d in ([(gr, 1), (gr, 0.5), (gr + 3, 0.5), (gr + 5, 1), (gr + 3, 0.5), (gr, 0.5)] if i % 2 == 0 else [(gr, 1.5), (gr, 0.5), (gr + 7, 0.5), (gr + 5, 0.5), (gr + 3, 0.5), (gr, 0.5)])]
    put("gl", bi, g); put("gr", bi, g if not (s == "intro" and i < 2) else [R4])   # 最初の2小節は左のギターだけ
    # ベース（ブギ: 1・3・5・6・♭7・6・5・3）
    br = root_in(ch, 28) if croot(ch) not in (2, 3, 0, 1) else root_in(ch, 36)
    minor = cqual(ch).startswith("m"); t3 = 3 if minor else 4
    boogie = [0, t3, 7, 9, 10, 9, 7, t3]
    if s in ("verse", "gsolo", "psolo") or (s == "intro" and i >= 4) or (s == "stop" and i >= 6) or (s == "outro" and i < 6):
        bs = [f"{nm(br + o)}:0.5" for o in boogie]
        if last and s == "verse": bs = [f"{nm(br)}:2", f"{nm(br + 7)}:1", f"{nm(br + 10)}:1"]
    elif s == "chorus":
        rn = root_in(nxt, 28) if croot(nxt) not in (2, 3, 0, 1) else root_in(nxt, 36)
        ap = rn - 1 if rn > br else (rn + 1 if rn < br else br + 7)
        bs = [f"{nm(x)}:0.5" for x in (br, br, br + 12, br, br, br + 12, br + 7, ap)]
    elif s == "stop": bs = [f"{nm(br)}:2", "R:2"]
    elif s == "bridge": bs = [f"{nm(br)}:2", f"{nm(br)}:1", f"{nm(br + 7)}:1"]
    elif s == "outro": bs = [f"{nm(br)}:2", f"{nm(br)}:2"] if i == 6 else [f"{nm(br)}:4"]
    else: bs = [R4]
    put("bass", bi, bs)
    # ドラム
    kk, sn, hh, ride, crash, tm = drums(b, nxtkind)
    put("kick", bi, ["g:" + kk]); put("snare", bi, ["g:" + sn]); put("hihat", bi, ["g:" + hh])
    put("crash", bi, ["g:X..............."] if crash else [R4])
    put("ride", bi, ["D2:0.5"] * 8 if ride else [R4])
    put("tom", bi, tomtok(tm) if tm else [R4])

parts = []
for key in ORDER:
    p = PARTS[key]; assert all(x is not None for x in p["bars"]), key
    d = dict(p["meta"]); d["notes"] = " ".join(p["bars"]); d["barGain"] = ARC; parts.append(d)
song = {"title": "ヘルタースケルター（仮）",
        "description": "（仮）リズム&ブルースとロックを混ぜたインスト。BPM138・シャッフル・イ長調のブルース（最後の3回は全音上のロ長調）・約4分。"
                       "R&B の側: 12小節ブルース、オルガンの旋律、ホーン隊の合いの手とキメ、ピアノの裏拍、ブギのベース、ストップタイム。"
                       "ロックの側: 左右の歪みギターのリフ、サビとソロはリードギター（ビブラート・チョーキングなし）、強いバックビート。"
                       "同じ名前の有名な曲があるが、旋律・リフ・進行はすべてオリジナル。入り方: 左のギターのリフだけ2小節 → 右が重なる → 全員。終わり方: 全員で一発、のばして消える。",
        "bpm": 138, "beats": 4, "chords": " ".join(b["chord"] for b in bars), "barsPerChord": 1, "repeats": 1,
        "tone": "rock", "feel": "rock", "swing": 0.55, "human": 0.3, "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False,
        "parts": parts}
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/helter-skelter-rb.json"
json.dump(song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(parts), "parts", NB, "bars", round(NB * 4 * 60 / 138), "sec")
