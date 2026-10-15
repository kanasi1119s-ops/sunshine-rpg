# 『ひのわのそらへ』（仮）: リングライト・クロニクルのオープニング曲（重音テトの歌つき。歌は hinowa-op-vocal.py）。
# 2026-10-16、人間の指示「冒険に出るのがワクワクで楽しみなケルト感あるやつ」。BPM160・ニ長調（リフはミクソリディアンの ♭VII＝C）・56小節（1分24秒）。
# ケルトの側: フィドル（VSCO のバイオリン）と笛（VSCO のフルート）のユニゾンのリフ、バグパイプのドローン（D と A）、ハープの分散和音、
#   アコギのストローク（Shiny のマイク録音）、低いタムで叩くボーラン（枠太鼓）風の刻み。
# 冒険・ワクワクの側: 生ドラムのバックビート、サビはライドと裏拍のオープンハイハット、サビの上でフィドルの対旋律、最後に全員で一発。
# 構成: 前奏8（ドローン→笛が動機をゆっくり）→ リフ8 → Aメロ8 → Bメロ8 → サビ16 → 後奏8（リフ4 → 全員で一発・のばす）
# 使い方: python3 hinowa-op.py <出力.json>
# 書き出し: node tools/composer/song.mjs build assets-src/ai-songs/hinowa-op.json --wav --drums muldjord --bass finger --orchestra vsco --guitar shiny-acoustic --master-preset rock-clean
import json, os, sys, importlib.util

def fmt(x): return ("%.4f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
def md(n):
    i = 2 if len(n) > 2 and n[1] == "#" else 1
    return N.index(n[:i]) + 12 * (int(n[i:]) + 1)
def chord_pcs(ch):
    r = N.index(ch[:2]) if len(ch) > 1 and ch[1] == "#" else N.index(ch[0]); q = ch[2:] if len(ch) > 1 and ch[1] == "#" else ch[1:]
    iv = [0, 3, 7] if q.startswith("m") else [0, 4, 7]
    if "7" in q: iv.append(10)
    return [(r + x) % 12 for x in iv]
def root_in(ch, lo): return lo + ((chord_pcs(ch)[0] - lo) % 12)
def voicing(ch, center):
    pcs = chord_pcs(ch)[:3]; best = None
    for inv in range(3):
        o = pcs[inv:] + pcs[:inv]; cur = center - 7; v = []
        for p in o:
            x = cur + ((p - cur) % 12); v.append(x); cur = x + 1
        sc = abs(sum(v) / 3 - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]

SEC = [("pre0", "D D G D D D A A"), ("riff", "D C G D D C G A"), ("A", "D G D A Bm G A A"), ("B", "Em G A D Em G A A"),
       ("C", "D A Bm G D A G A"), ("C", "D A Bm G Em A D D"), ("out", "D C G D D D D D")]
bars = []
for si, (s, pr) in enumerate(SEC):
    for i, c in enumerate(pr.split()): bars.append(dict(kind=s, chord=c, i=i, si=si, n=sum(1 for x in SEC[:si] if x[0] == s)))
NB = len(bars); assert NB == 56

HOOK = ["D5:0.5 F#5:0.5 A5:0.5 F#5:0.5 D6:1 A5:0.5 F#5:0.5", "G5:0.5 E5:0.5 C5:0.5 E5:0.5 G5:1 E5:1",
        "D5:0.5 G5:0.5 B5:0.5 G5:0.5 D6:0.5 B5:0.5 A5:0.5 G5:0.5", "F#5:0.5 E5:0.5 D5:0.5 E5:0.5 F#5:2",
        "D5:0.5 F#5:0.5 A5:0.5 F#5:0.5 D6:1 A5:0.5 F#5:0.5", "G5:0.5 A5:0.5 G5:0.5 E5:0.5 C6:1 B5:0.5 A5:0.5",
        "B5:0.5 A5:0.5 G5:0.5 B5:0.5 D6:0.5 B5:0.5 G5:0.5 B5:0.5", "A5:1 E5:0.5 C#5:0.5 A5:2"]
SLOW = ["D5:1 F#5:1 A5:2", "G5:1 E5:1 D5:2", "A5:1 F#5:1 E5:2", "C#5:2 A4:2"]   # 前奏の後半、笛がゆっくり動機を吹く
for h in HOOK + SLOW: assert abs(sum(float(t.split(":")[1]) for t in h.split()) - 4) < 1e-9, h

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
def legato(toks):   # 息・弦の旋律は、休みに挟まれていない音をつなぐ（1音ずつ切って「ポンポン」にしない）
    out = []
    for j, x in enumerate(toks):
        nxt = toks[j + 1] if j + 1 < len(toks) else "R"
        out.append(x + "_" if not x.startswith("R") and not nxt.startswith("R") else x)
    return out

DR = -6
part("fiddle", "fiddle", "フィドル（リフ・対旋律）", 0.2, -0.2, patch="violin", reverb=0.22, gainDb=2)
part("flute", "panflute", "笛（リフ・前奏の動機）", 0.18, 0.22, patch="flute", reverb=0.28, gainDb=2)
part("pipe1", "bagpipe", "バグパイプのドローン（D）", 0.06, -0.35, reverb=0.3)
part("pipe2", "bagpipe", "バグパイプのドローン（A）", 0.05, 0.35, reverb=0.3)
part("harp", "harp", "ハープ（分散和音）", 0.13, 0.45, reverb=0.3, bright=-0.4)   # 高い音の弾いた瞬間の鋭さを少し丸める（雑音の検知でプチッ扱いになった）
for k, pan in (("g1", -0.55), ("g2", -0.5), ("g3", -0.45), ("g4", -0.4)):
    part(k, "guitar", f"アコギのストローク（{k[1]}弦目）", 0.1, pan, amp="crystal", chorus=0, sustain=1.6, reverb=0.15, autoScoop=False, push={"g1": 0, "g2": 0.012, "g3": 0.024, "g4": 0.036}[k])
part("sth", "strings", "弦（上）", 0.08, 0.6, reverb=0.3)
part("stl", "strings", "弦（下）", 0.08, -0.6, reverb=0.3)
part("bass", "bass", "ベース", 0.3, 0)
part("bodhran", "tom", "ボーラン風の刻み（低いタム）", 0.12, 0.1, reverb=0, gainDb=DR)
part("kick", "kick", "キック", 0.3, 0, gainDb=DR)
part("snare", "snare", "スネア", 0.26, 0, push=0.02, gainDb=DR)
part("hihat", "hihat", "ハイハット", 0.08, 0, push=-0.008, gainDb=DR)
part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=DR)
part("ride", "crash", "ライド", 0.07, 0.2, gainDb=DR)
part("tom", "tom", "タム（フィル）", 0.14, 0, reverb=0, gainDb=DR)
R4 = "R:4"; Z = "................"

def tomtok(tm, pit=("E3", "E3", "C3", "C3", "A2", "A2")):
    hits = [j for j, c in enumerate(tm) if c in "xX"]; toks = []; k = 0
    for c in tm:
        if c in "xX": toks.append(pit[min(len(pit) - 1, k * len(pit) // max(1, len(hits)))] + ":0.25" + ("!" if c == "X" else "")); k += 1
        else: toks.append("R:0.25")
    return toks

ARC = []
for b in bars:
    s, i, n = b["kind"], b["i"], b["n"]
    g = {"pre0": 0.7 + 0.02 * i, "riff": 0.95, "A": 0.82, "B": 0.86 + 0.02 * i, "C": 1.0 if n == 0 else 1.04, "out": 1.02}[s]
    ARC.append(round(g, 3))

STRUM = {"full": [(0, "D"), (1, "D"), (1.5, "U"), (2.5, "U"), (3, "D"), (3.5, "U")],
         "light": [(0, "D"), (2, "D"), (3, "U")], "eights": [(x * 0.5, "D") for x in range(8)]}

for bi, b in enumerate(bars):
    s, ch, i, n = b["kind"], b["chord"], b["i"], b["n"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB else ch
    final = s == "out" and i >= 4
    # フィドル
    if s in ("riff",) or (s == "out" and i < 4): put("fiddle", bi, legato(HOOK[i % 8].split()))
    elif s == "C":
        v = voicing(ch, 79)
        put("fiddle", bi, legato([f"{nm(v[2])}:2", f"{nm(v[1])}:2"]) if i % 2 == 0 else [f"{nm(v[2])}:4"])
    elif final: put("fiddle", bi, ["D5:4"] if i == 4 else [R4])
    else: put("fiddle", bi, [R4])
    # 笛
    if s == "pre0" and i >= 4: put("flute", bi, legato(SLOW[i - 4].split()))
    elif s == "riff" or (s == "out" and i < 4): put("flute", bi, legato(HOOK[i % 8].split()))
    elif s == "C" and n == 1 and i >= 6: put("flute", bi, ["A5:4"] if i == 6 else [R4])
    elif final: put("flute", bi, ["A5:4"] if i == 4 else [R4])
    else: put("flute", bi, [R4])
    # バグパイプのドローン
    drone = s == "pre0" or final
    put("pipe1", bi, ["D4:4"] if drone and not (final and i == 7) else [R4])
    put("pipe2", bi, ["A4:4"] if drone and not (final and i == 7) else [R4])
    # ハープ（8分の分散和音）
    t = sorted(voicing(ch, 62) + [x + 12 for x in voicing(ch, 62)])
    if s in ("pre0", "A", "B") or (s == "C"):
        pat = [0, 2, 4, 2, 1, 3, 5, 3] if s != "pre0" or i >= 0 else []
        put("harp", bi, [f"{nm(t[j])}:0.5" for j in pat])
    elif final and i == 4: put("harp", bi, [f"{nm(x)}:0.25" for x in (t + t[::-1])[:12]] + [f"{nm(t[-1])}:1"])
    else: put("harp", bi, [R4])
    # アコギのストローク
    sty = None
    if s in ("riff", "C") or (s == "out" and i < 4): sty = "full"
    elif s == "A": sty = "light"
    elif s == "B": sty = "eights" if i >= 4 else "light"
    elif final and i == 4: sty = "hit"
    low = root_in(ch, 40); v = voicing(ch, 55)   # 歌とぶつからないよう、C3〜G4 に
    notes = {"g1": low, "g2": v[0], "g3": v[1], "g4": v[2]}
    for k in ("g1", "g2", "g3", "g4"):
        if sty is None: put(k, bi, [R4]); continue
        if sty == "hit": put(k, bi, [f"{nm(notes[k])}:4!"]); continue
        hits = STRUM[sty]; toks = []
        lead_rest = hits[0][0]
        if lead_rest > 0: toks.append(f"R:{fmt(lead_rest)}")
        for j, (pos, d) in enumerate(hits):
            end = hits[j + 1][0] if j + 1 < len(hits) else 4
            plays = d == "D" or k in ("g3", "g4")
            if plays: toks.append(f"{nm(notes[k])}:{fmt(end - pos)}" + ("!" if pos in (0, 2) and d == "D" else ("," if d == "U" else "")))
            else:
                if toks and not toks[-1].startswith("R"):   # 上の弦だけのアップのあいだ、低い弦は前の音をのばす（すぐ止めない）
                    nn, dd = toks[-1].split(":", 1); num = float("".join(c for c in dd if c.isdigit() or c == ".")); suf = dd[len(fmt(num)):] if dd.startswith(fmt(num)) else ""
                    toks[-1] = f"{nn}:{fmt(num + end - pos)}{suf}"
                else: toks.append(f"R:{fmt(end - pos)}")
        put(k, bi, toks)
    # 弦
    st = s in ("B", "C") or final and i == 4
    put("sth", bi, [f"{nm(voicing(ch, 72)[2])}:4"] if st and not (final and i > 4) else [R4])
    put("stl", bi, [f"{nm(voicing(ch, 60)[0])}:4"] if st and not (final and i > 4) else [R4])
    # ベース
    a = root_in(ch, 28); f5 = a + 7; o = a + 12; rn = root_in(nxt, 28)
    ap = rn - 1 if rn > a else (rn + 1 if rn < a else f5)
    if s in ("riff", "C") or (s == "out" and i < 4): bs = [(a, 1), (a, 0.5), (f5, 0.5), (o, 1), (f5, 0.5), (ap, 0.5)]
    elif s == "A": bs = [(a, 2), (f5, 1), (ap, 1)]
    elif s == "B": bs = [(a, 1), (a, 1), (a, 1), (ap, 1)] if i < 4 else [(a, 0.5)] * 8
    elif final and i == 4: bs = [(a, 4)]
    else: bs = None
    put("bass", bi, [f"{nm(x)}:{fmt(d)}" for x, d in bs] if bs else [R4])
    # ボーラン風の刻み（前奏の後半から。サビと後奏）
    if (s == "pre0" and i >= 4) or s in ("riff", "C") or (s == "out" and i < 4):
        put("bodhran", bi, ["A2:0.5!", "A2:0.5,", "A2:0.5", "A2:0.5,", "A2:0.5!", "A2:0.5,", "A2:0.5", "A2:0.5,"] if not (s == "pre0" and i < 6) else ["A2:1!", "A2:1,", "A2:1!", "A2:1,"])
    else: put("bodhran", bi, [R4])
    # ドラム
    kk = sn = hh = Z; ride = crash = False; tm = None
    if s == "pre0" and i == 7: sn = "........o.o.xxXX"
    elif s == "riff" or (s == "out" and i < 4):
        kk = "X...X.x.X...X.x."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."; crash = i % 4 == 0
        if i == 7: sn = "....X...xxxxXXXX"; tm = "............XXXX"
    elif s == "A":
        kk = "X.......X.x....."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."; crash = i == 0
        if i == 3: sn = "....X.......X.oX"
        if i == 7: sn = "....X...o.x.X.XX"
    elif s == "B":
        kk = "X...X...X...X..."; sn = "....X.......X..." if i < 4 else ("x.x.x.x.x.x.x.x." if i < 6 else "xxxxxxxxxxxxxxxx")
        hh = "x.x.x.x.x.x.x.x." if i < 4 else Z; crash = i == 0
        if i == 7: sn = "xxxxxxxxXXXXXXXX"; tm = "............XXXX"
    elif s == "C":
        kk = "X...X.x.X...X.x."; sn = "....X.......X..."; crash = i % 4 == 0
        if n == 0: ride = True
        else: hh = "x.O.x.O.x.O.x.O."
        if i == 3: sn = "....X.......xxXX"
        if i == 7: sn = "....X...........";  tm = "........xxXXxxXX"
    elif final:
        if i == 4: kk = "X..............."; crash = True
    if tm:
        first = next(j for j, c in enumerate(tm) if c in "xX")
        sn = sn[:first] + "".join("." if tm[first + j] in "xX" else c for j, c in enumerate(sn[first:])); hh = hh[:first] + "." * (16 - first); ride = False
    if crash: hh = "." + hh[1:]
    put("kick", bi, ["g:" + kk]); put("snare", bi, ["g:" + sn]); put("hihat", bi, ["g:" + hh])
    put("crash", bi, ["g:X..............."] if crash else [R4])
    put("ride", bi, ["D2:0.5"] * 8 if ride else [R4])
    put("tom", bi, tomtok(tm) if tm else [R4])

parts = []
for key in ORDER:
    p = PARTS[key]; assert all(x is not None for x in p["bars"]), key
    d = dict(p["meta"]); d["notes"] = " ".join(p["bars"]); d["barGain"] = ARC; parts.append(d)
song = {"title": "ひのわのそらへ（伴奏・仮）",
        "description": "（仮）リングライト・クロニクルのオープニング曲の伴奏（歌は重音テト）。冒険に出るワクワクを、ケルトの楽器で。BPM160・ニ長調・1分24秒。"
                       "フィドルと笛のユニゾンのリフ、バグパイプのドローン、ハープ、アコギのストローク、低いタムのボーラン風の刻み、生ドラム。"
                       "入り方: バグパイプのドローンとハープ → 笛がゆっくり動機。終わり方: 全員で一発、ドローンとハープがのびて消える。",
        "bpm": 160, "beats": 4, "chords": " ".join(b["chord"] for b in bars), "barsPerChord": 1, "repeats": 1,
        "tone": "rock", "feel": "rock", "human": 0.25, "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False,
        "parts": parts}
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/hinowa-op.json"
json.dump(song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(parts), "parts", NB, "bars", round(NB * 4 * 60 / 160), "sec")
