# 『ひのわのそらへ』（仮）: リングライト・クロニクルのオープニング曲（重音テトの歌つき。歌は hinowa-op-vocal.py）。
# 2026-10-16 改訂（人間の指摘「ケルト感ないかな。ケルトちょっと勉強してきて」）。調べて分かった、アイルランドの伝統音楽の決まりを入れて作り直した:
#  - 拍子: 踊りの曲「ジグ」（6/8。1拍を3つに分け、「4分＋8分」と「8分3つ」の型）。作曲ソフトでは 4/4・BPM120 の1拍を3連符で書く（12/8 と同じ）。
#  - 形: 8小節の部分 A（tune）と、高い音域の部分 B（turn）。曲の頭は A をまるごと、最後に B。
#  - 音階: ニ長調にミクソリディアン（C の音。D と C の和音を行き来する「ダブル・トニック」）。
#  - 飾り（オーナメント）: 付点4分の音に「ロール」（主音→上の音を一瞬→主音→下の音を一瞬→主音）、同じ音が続く所や長い音の頭に「カット」（上の音を一瞬）。
#  - 楽器: 笛（ティン・ホイッスル代わりに VSCO のフルート）とフィドル（VSCO のバイオリン）のユニゾン、フィドルの開放弦のドローン（重音）、
#    ボーラン（枠太鼓）の「強・弱・中」のジグの刻み（低いタムで、強い拍は A2、ほかは C3 で手の押さえの高さを変える）、
#    アコギは DADGAD 風（開放の D と A を鳴らし続ける3度の薄い和音）で、各拍「ダウン（2）・アップ（1）」のジグのストローク、ハープの3連の分散和音、バグパイプのドローン。
#  - 冒険のワクワク: サビは生ドラムの 12/8 のバックビート、笛が歌の1オクターブ上を重ねる。
# 構成（44小節・88秒、1小節＝2秒）: 前奏4（ドローンと笛のゆっくりした歌）→ ジグ A 8 → Aメロ8 → Bメロ4 → サビ16 → ジグ B 4（最後に全員で一発）
# 使い方: python3 hinowa-op.py <出力.json>
# 書き出し: node tools/composer/song.mjs build assets-src/ai-songs/hinowa-op.json --wav --drums muldjord --bass finger --orchestra vsco --guitar shiny-acoustic --master-preset rock-clean --master -13.5
import json, os, sys, random, importlib.util

def fmt(x): return ("%.6f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
def md(n):
    i = 2 if len(n) > 2 and n[1] == "#" else 1
    return N.index(n[:i]) + 12 * (int(n[i:]) + 1)
MIXO = [2, 4, 6, 7, 9, 11, 0]   # D ミクソリディアン
def nb(m, d):   # 音階の上（d=+1）か下（-1）のとなりの音
    x = m + d
    while x % 12 not in MIXO: x += d
    return x

CH = {"D": [50, 57, 62, 69], "C": [48, 55, 62, 64], "G": [50, 55, 59, 62], "A": [52, 57, 61, 64], "Em": [52, 59, 62, 64],
      "Bm": [54, 59, 62, 66]}   # DADGAD 風（開放の D・A を残す）。低い弦から高い弦へ
ROOT = {"D": 38, "C": 36, "G": 43, "A": 45, "Em": 40, "Bm": 47}
SEC = [("intro", "D D D D"), ("tuneA", "D C D A D C C D"), ("verse", "D C G D D C A A"), ("pre", "Em G A A"),
       ("chorus", "D C G D Bm G A A D C G D G A D D"), ("tuneB", "D C D D")]
bars = []
for s, pr in SEC:
    for i, c in enumerate(pr.split()): bars.append(dict(kind=s, chord=c, i=i))
NB = len(bars); assert NB == 44

AIR = ["R:12", "A4:3 D5:3 E5:3 F#5:3", "E5:6 D5:3 B4:3", "A4:12"]
TA = ["A5:2 F#5:1 A5:1 B5:1 A5:1 F#5:2 D5:1 E5:1 F#5:1 D5:1", "G5:2 E5:1 G5:1 A5:1 G5:1 E5:2 C5:1 D5:1 E5:1 C5:1",
      "A5:2 F#5:1 A5:1 B5:1 A5:1 D6:2 B5:1 A5:1 F#5:1 D5:1", "G5:1 A5:1 B5:1 A5:2 F#5:1 E5:3 D5:1 E5:1 F#5:1",
      "A5:2 F#5:1 A5:1 B5:1 A5:1 F#5:2 D5:1 E5:1 F#5:1 D5:1", "G5:2 E5:1 G5:1 A5:1 G5:1 E5:2 C5:1 D5:1 E5:1 C5:1",
      "A5:1 B5:1 C6:1 D6:2 A5:1 B5:1 A5:1 G5:1 E5:1 D5:1 C5:1", "D5:1 F#5:1 E5:1 D5:1 C5:1 A4:1 D5:3 R:3"]
TB = ["D6:2 A5:1 D6:1 E6:1 D6:1 C6:2 A5:1 G5:1 A5:1 C6:1", "C6:2 G5:1 C6:1 D6:1 C6:1 B5:2 G5:1 E5:1 G5:1 C6:1",
      "D6:2 A5:1 F#5:1 A5:1 D6:1 E6:2 D6:1 C6:1 A5:1 G5:1", "F#5:1 E5:1 C5:1 D5:3 D5:6"]
def tri(s):
    out = [(t.rsplit(":", 1)[0], int(t.rsplit(":", 1)[1])) for t in s.split()]
    assert sum(k for _, k in out) == 12, s
    return out
for m in AIR + TA + TB: tri(m)

G = 0.06   # 飾りの一瞬の音（拍。BPM120 で 30ms）
def ornament(seq, style, seed):
    """seq: [(音名, 8分の数)]。style="roll"（フィドル）か "cut"（笛）。返り値: 拍のトークン（休みに挟まれていない音は _ でつなぐ）"""
    r = random.Random(seed); ev = []
    for j, (n, k) in enumerate(seq):
        d = k / 3
        if n == "R": ev.append(("R", d)); continue
        m = md(n); prev = seq[j - 1][0] if j else None
        if k == 3 and style == "roll" and j < len(seq) - 1:
            ev += [(m, 1 / 3), (nb(m, 1), G), (m, 1 / 3 - G), (nb(m, -1), G), (m, 1 / 3 - G)]
        elif k >= 2 and (prev == n or r.random() < (0.5 if style == "cut" else 0.25)):
            ev += [(nb(m, 1), G), (m, d - G)]
        else: ev.append((m, d))
    toks = []
    for j, (m, d) in enumerate(ev):
        if m == "R": toks.append(f"R:{fmt(d)}"); continue
        nxt = ev[j + 1][0] if j + 1 < len(ev) else "R"
        toks.append(f"{nm(m)}:{fmt(d)}" + ("_" if nxt != "R" else ""))
    return toks
def plain(seq, shift=0, legato=True):
    toks = []
    for j, (n, k) in enumerate(seq):
        if n == "R": toks.append(f"R:{fmt(k / 3)}"); continue
        nxt = seq[j + 1][0] if j + 1 < len(seq) else "R"
        toks.append(f"{nm(md(n) + shift)}:{fmt(k / 3)}" + ("_" if legato and nxt != "R" else ""))
    return toks

PARTS, ORDER = {}, []
def part(key, inst, role, vol, pan, **kw):
    PARTS[key] = dict(meta=dict(instrument=inst, role=role, volume=vol, pan=pan, **kw), bars=[None] * NB); ORDER.append(key)
def put(key, bi, toks):
    if isinstance(toks, str): toks = toks.split()
    t = sum(float("".join(c for c in x.split(":")[1] if c.isdigit() or c == ".")) for x in toks)
    assert abs(t - 4) < 1e-4, (key, bi, bars[bi]["kind"], t, toks)
    PARTS[key]["bars"][bi] = " ".join(toks)
def grid(s, note="x"):
    """12文字（1文字＝3連の8分）。X 強・x ふつう・o 弱・. 休み。音程つきは note を "A2" などに"""
    assert len(s) == 12, s
    toks = []; i = 0
    while i < 12:
        c = s[i]; j = i + 1
        while j < 12 and s[j] == ".": j += 1
        d = fmt((j - i) / 3)
        if c == ".": toks.append(f"R:{d}")
        else: toks.append(f"{note}:{d}" + ("!" if c == "X" else ("," if c == "o" else "")))
        i = j
    return toks

DR = -6
part("flute", "panflute", "笛（ジグの旋律・前奏の歌）", 0.2, 0.2, patch="flute", reverb=0.25, gainDb=2)
part("fiddle", "fiddle", "フィドル（ジグの旋律・対旋律）", 0.2, -0.2, patch="violin", reverb=0.2, gainDb=2)
part("fdrone", "fiddle", "フィドルの開放弦（重音のドローン）", 0.08, -0.25, patch="violin", reverb=0.2)
part("pipe1", "bagpipe", "バグパイプのドローン（D）", 0.05, -0.35, reverb=0.3)
part("pipe2", "bagpipe", "バグパイプのドローン（A）", 0.04, 0.35, reverb=0.3)
part("harp", "harp", "ハープ（3連の分散和音）", 0.12, 0.45, reverb=0.3, bright=-0.4)
for k, pan in (("g1", -0.55), ("g2", -0.5), ("g3", -0.45), ("g4", -0.4)):
    part(k, "guitar", f"アコギ DADGAD 風（{k[1]}本目）", 0.09, pan, amp="crystal", chorus=0, sustain=1.6, reverb=0.15, autoScoop=False,
         push={"g1": 0, "g2": 0.01, "g3": 0.02, "g4": 0.03}[k])
part("sth", "strings", "弦（上）", 0.07, 0.6, reverb=0.3)
part("stl", "strings", "弦（下）", 0.07, -0.6, reverb=0.3)
part("bass", "bass", "ベース", 0.28, 0)
part("bodhran", "tom", "ボーラン風のジグの刻み", 0.13, 0.1, reverb=0, gainDb=DR)
part("kick", "kick", "キック", 0.3, 0, gainDb=DR)
part("snare", "snare", "スネア", 0.24, 0, push=0.02, gainDb=DR)
part("hihat", "hihat", "ハイハット", 0.08, 0, gainDb=DR)
part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=DR)
part("ride", "crash", "ライド", 0.07, 0.2, gainDb=DR)
part("tom", "tom", "タム（フィル）", 0.13, 0, reverb=0, gainDb=DR)
R4 = "R:4"

_sp = importlib.util.spec_from_file_location("v", os.path.join(os.path.dirname(os.path.abspath(__file__)), "hinowa-op-vocal.py"))
vmod = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(vmod)
VB = vmod.bars()   # 歌の小節（笛が1オクターブ上で重ねるため）

ARC = []
for b in bars:
    s, i = b["kind"], b["i"]
    ARC.append({"intro": 0.72, "tuneA": 0.9 if i < 4 else 0.97, "verse": 0.8, "pre": 0.85 + 0.04 * i, "chorus": 1.0 if i < 8 else 1.05, "tuneB": 1.04}[s])

for bi, b in enumerate(bars):
    s, ch, i = b["kind"], b["chord"], b["i"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB else ch
    last = bi == NB - 1
    # 笛
    if s == "intro": put("flute", bi, plain(tri(AIR[i])) if i else [R4])
    elif s == "tuneA": put("flute", bi, ornament(tri(TA[i]), "cut", bi))
    elif s == "tuneB": put("flute", bi, ornament(tri(TB[i]), "cut", bi))
    elif s == "chorus" and 8 <= i <= 14 and VB[bi] != "R:4":   # サビの後半は、歌の1オクターブ上を重ねる
        toks = []
        for t in VB[bi].split():
            if t.startswith("R:"): toks.append(t); continue
            _, p, d = t.split(":"); toks.append(f"{nm(md(p) + 12)}:{d}")
        put("flute", bi, [x + ("_" if j + 1 < len(toks) and not toks[j + 1].startswith("R") and not x.startswith("R") else "") for j, x in enumerate(toks)])
    else: put("flute", bi, [R4])
    # フィドル
    if s == "tuneA" and i >= 2: put("fiddle", bi, ornament(tri(TA[i]), "roll", bi + 100))
    elif s == "tuneB": put("fiddle", bi, ornament(tri(TB[i]), "roll", bi + 100))
    elif s == "chorus" and i < 8:   # 歌の上に長い音の対旋律（和音の音）
        v = sorted(CH[ch])
        hi = max(x + 12 for x in v if x + 12 <= 81)
        lo2 = nb(hi, -1); lo2 = lo2 if lo2 % 12 in [p % 12 for p in v] else hi
        put("fiddle", bi, [f"{nm(hi)}:2_", f"{nm(lo2)}:2"])
    else: put("fiddle", bi, [R4])
    # フィドルの開放弦のドローン（ジグの部分）
    put("fdrone", bi, ["A4:4"] if s in ("tuneA", "tuneB") and not last and not (s == "tuneA" and i < 2) else [R4])
    # バグパイプのドローン
    drone = s == "intro" or (s == "tuneB") or (s == "chorus" and i >= 12)
    put("pipe1", bi, ["D4:4"] if drone else [R4]); put("pipe2", bi, ["A4:4"] if drone and s != "chorus" else [R4])
    # ハープ（3連の分散和音）
    v = CH[ch]; arp = [v[0] + 12, v[1] + 12, v[2] + 12, v[3] + 12]
    if s in ("intro", "verse", "pre"):
        pat = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1]
        put("harp", bi, [f"{nm(arp[j])}:{fmt(1 / 3)}" for j in pat])
    elif last: put("harp", bi, [f"{nm(x)}:{fmt(1 / 3)}" for x in arp + [x + 12 for x in arp]] + [f"{nm(arp[0] + 24)}:{fmt(4 - 8 / 3)}"])
    else: put("harp", bi, [R4])
    # アコギ（各拍: ダウン 2/3 拍・アップ 1/3 拍。アップは上の2本だけ。低い弦はのばす）
    strum = s in ("tuneA", "chorus", "tuneB", "verse", "pre")
    for gi, k in enumerate(("g1", "g2", "g3", "g4")):
        if not strum or (s == "tuneA" and i < 2): put(k, bi, [R4]); continue
        if last: put(k, bi, [f"{nm(v[gi])}:4!"]); continue
        if s == "verse":   # Aメロは1拍にダウン1回（軽く）
            put(k, bi, [f"{nm(v[gi])}:1" + ("!" if j % 2 == 0 else ",") for j in range(4)]); continue
        toks = []
        for beat in range(4):
            acc = "!" if beat % 2 == 0 else ""
            if gi >= 2: toks += [f"{nm(v[gi])}:{fmt(2 / 3)}{acc}", f"{nm(v[gi])}:{fmt(1 / 3)},"]
            else: toks += [f"{nm(v[gi])}:1{acc}"]
        put(k, bi, toks)
    # 弦
    st = s in ("pre", "chorus")
    put("sth", bi, [f"{nm(v[3] + 12)}:4"] if st else [R4]); put("stl", bi, [f"{nm(v[1])}:4"] if st else [R4])
    # ベース
    r = ROOT[ch]; r = r - 12 if r >= 45 else r; f5 = r + 7; rn = ROOT[nxt]; rn = rn - 12 if rn >= 45 else rn
    ap = rn - 1 if rn > r else (rn + 1 if rn < r else f5)
    if last: bs = [f"{nm(r)}:4"]
    elif s == "tuneA" and i < 4: bs = [f"{nm(r)}:4"] if i >= 2 else [R4]
    elif s in ("tuneA", "chorus", "tuneB"): bs = [f"{nm(r)}:1", f"{nm(r)}:{fmt(2 / 3)}", f"{nm(r)}:{fmt(1 / 3)}", f"{nm(f5)}:1", f"{nm(ap)}:1"]
    elif s == "verse": bs = [f"{nm(r)}:2", f"{nm(f5)}:1", f"{nm(ap)}:1"]
    elif s == "pre": bs = [f"{nm(r)}:1"] * 3 + [f"{nm(ap)}:1"]
    else: bs = [R4]
    put("bass", bi, bs)
    # ボーラン（各拍: 強 A2・弱 C3・中 C3。Aメロは軽く）
    if s == "intro": bod = "........XoxX" if i == 3 else None
    elif s == "verse": bod = "X.xX.xX.xX.x" if i % 2 == 0 else "X.xX.xX.xXox"
    elif s in ("tuneA", "chorus", "tuneB", "pre"): bod = "XoxXoxXoxXox" if not last else "X..........."
    else: bod = None
    if bod:
        toks = []; j = 0
        while j < 12:
            c = bod[j]; k = j + 1
            while k < 12 and bod[k] == ".": k += 1
            d = fmt((k - j) / 3)
            toks.append(f"R:{d}" if c == "." else (f"A2:{d}!" if c == "X" else f"C3:{d}" + ("," if c == "o" else "")))
            j = k
        put("bodhran", bi, toks)
    else: put("bodhran", bi, [R4])
    # ドラム（12/8: 1文字＝3連の8分）
    kk = sn = hh = "............"; ride = crash = False; tm = None
    if s == "tuneA" and i >= 4:
        kk = "X.....X....."; sn = "...X.....X.."; hh = "x.xx.xx.xx.x"; crash = i == 4
        if i == 7: sn = "...X.....xxX"
    elif s == "verse":
        kk = "X.....X....."; sn = "...o.....o.." if i < 4 else "...X.....X.."; hh = "x.xx.xx.xx.x"; crash = i == 0
    elif s == "pre":
        kk = "X..X..X..X.."; sn = "...X.....X.." if i < 2 else ("...X..X..XxX" if i == 2 else "XxxXxxXxxXXX"); crash = i == 0
        if i == 3: tm = "......xxXxxX"
    elif s == "chorus":
        kk = "X.....X..X.."; sn = "...X.....X.."; crash = i % 4 == 0
        if i < 8: ride = True
        else: hh = "x.Xx.Xx.Xx.X"
        if i == 7: sn = "...X......xX"; tm = "......xxXxxX"
        if i == 15: sn = "...X..xxXxxX"
    elif s == "tuneB":
        kk = "X.....X..X.."; sn = "...X.....X.."; hh = "x.xx.xx.xx.x"; crash = i == 0
        if last: kk = "X..........."; sn = "X..........."; hh = "............"; crash = True
    if tm:
        f0 = next(j for j, c in enumerate(tm) if c != ".")
        sn = sn[:f0] + "".join("." if tm[f0 + j] != "." else c for j, c in enumerate(sn[f0:])); hh = hh[:f0] + "." * (12 - f0); ride = False
    if crash: hh = "." + hh[1:]
    put("kick", bi, grid(kk)); put("snare", bi, grid(sn)); put("hihat", bi, grid(hh))
    put("crash", bi, grid("X...........") if crash else [R4])
    put("ride", bi, grid("x.xx.xx.xx.x", "D2") if ride else [R4])
    if tm:
        toks = []; pit = ["E3", "C3", "A2"]; cnt = sum(1 for c in tm if c != "."); kq = 0; j = 0
        while j < 12:
            c = tm[j]; k = j + 1
            while k < 12 and tm[k] == ".": k += 1
            d = fmt((k - j) / 3)
            if c == ".": toks.append(f"R:{d}")
            else: toks.append(f"{pit[min(2, kq * 3 // cnt)]}:{d}" + ("!" if c == "X" else "")); kq += 1
            j = k
        put("tom", bi, toks)
    else: put("tom", bi, [R4])

parts = []
for key in ORDER:
    p = PARTS[key]; assert all(x is not None for x in p["bars"]), key
    d = dict(p["meta"]); d["notes"] = " ".join(p["bars"]); d["barGain"] = ARC; parts.append(d)
song = {"title": "ひのわのそらへ（伴奏・仮）",
        "description": "（仮）リングライト・クロニクルのオープニング曲の伴奏（歌は重音テト）。アイルランドの踊りの曲「ジグ」（6/8）で書いた、冒険に出るワクワクの曲。"
                       "BPM120（付点4分）・ニ長調（ミクソリディアン）・88秒。笛とフィドルのユニゾンにロールとカットの飾り、フィドルの開放弦のドローン、ボーランの刻み、"
                       "DADGAD 風のアコギ、ハープ、バグパイプのドローン。入り方: ドローンとハープの上で笛がゆっくり歌う → ジグ。終わり方: 高い音域のジグ B のあと全員で一発。",
        "bpm": 120, "beats": 4, "chords": " ".join(b["chord"] for b in bars), "barsPerChord": 1, "repeats": 1,
        "tone": "rock", "feel": "rock", "human": 0.2, "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False,
        "parts": parts}
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/hinowa-op.json"
json.dump({"guitarWobble": False, **song}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(parts), "parts", NB, "bars", NB * 2, "sec")
