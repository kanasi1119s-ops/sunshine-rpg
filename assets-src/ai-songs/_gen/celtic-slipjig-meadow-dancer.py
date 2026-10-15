# 『草原の踊り子』（仮）: ケルト音楽5曲の2曲目。踊りの曲「スリップジグ」（9/8。1小節に3拍、1拍を3つに分ける。「4分＋8分」が3つ続く、はずむ型）。
# BPM116（付点4分）・ト長調。形: 8小節の A と高い B を AABB で3回。
#   前奏4（ハープとドローンの上で笛が A の頭をゆっくり）→ 1回目（笛ひとり・ハープ・アコギ）→ 2回目（フィドルと笛・ボーラン・ベース）
#   → 間奏4（ハープとボーラン）→ 3回目（生ドラム・弦。フィドルは3度下のハモり）→ 一発で終わる。
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

GMAJ = [7, 9, 11, 0, 2, 4, 6]
A = ["D5:2 B4:1 D5:2 G5:1 B5:2 G5:1", "A5:2 G5:1 F#5:2 G5:1 E5:3",
     "E5:2 C5:1 E5:2 G5:1 C6:2 G5:1", "B5:2 A5:1 G5:1 F#5:1 E5:1 D5:3",
     "D5:2 B4:1 D5:2 G5:1 B5:2 D6:1", "E6:2 D6:1 B5:2 G5:1 E5:3",
     "C5:1 E5:1 G5:1 C6:2 B5:1 A5:2 G5:1", "F#5:2 A5:1 D5:2 F#5:1 G5:3"]
B = ["B5:2 E6:1 D6:2 B5:1 G5:2 B5:1", "A5:2 D6:1 C6:2 A5:1 F#5:2 A5:1",
     "G5:2 C6:1 E6:2 C6:1 G5:2 E5:1", "F#5:1 G5:1 A5:1 D6:3 C6:2 A5:1",
     "B5:2 E6:1 D6:2 B5:1 D6:2 E6:1", "C6:2 G5:1 E5:2 G5:1 C6:3",
     "A5:2 C6:1 B5:2 A5:1 F#5:2 D5:1", "G5:1 F#5:1 E5:1 D5:2 B4:1 G4:3"]
CA = "G G C D G Em C G".split(); CB = "Em D7 C D Em C Am7 G".split()
plan = [("intro", 0, "-", i) for i in range(4)]
for rnd in (1, 2):
    for p in "AABB": plan += [("tune", rnd, p, i) for i in range(8)]
plan += [("break", 0, "-", i) for i in range(4)]
for p in "AABB": plan += [("tune", 3, p, i) for i in range(8)]
plan += [("end", 0, "-", 0)]
S = Song(3, 3, len(plan), GMAJ); S.check(A, B); S.G = 0.09   # 飾り 約45ms
chords = [("G" if k in ("intro", "end") else ["G", "C", "G", "D"][i] if k == "break" else (CA if p == "A" else CB)[i]) for k, rnd, p, i in plan]
CH = {"G": [43, 50, 55, 59, 62], "C": [48, 52, 55, 60, 64], "D": [50, 54, 57, 62, 66], "D7": [50, 54, 57, 60, 66], "Em": [40, 47, 52, 55, 59],
      "Am7": [45, 52, 55, 60, 64]}
ROOT = {"G": 31, "C": 36, "D": 38, "D7": 38, "Em": 40, "Am7": 33}

S.part("flute", "panflute", "笛（旋律）", 0.2, 0.2, patch="flute", reverb=0.38, gainDb=2)
S.part("fiddle", "fiddle", "フィドル（旋律）", 0.19, -0.2, patch="violin", reverb=0.36, gainDb=2)
S.part("harm", "fiddle", "フィドル2（3度下のハモり）", 0.1, -0.45, patch="violin", reverb=0.36)
S.part("harp", "harp", "ハープ（3連の分散和音）", 0.12, 0.45, reverb=0.35, bright=-0.4)
S.part("pipe", "bagpipe", "バグパイプのドローン（G）", 0.045, -0.3, reverb=0.35)
S.part("pipe5", "bagpipe", "バグパイプのドローン（D）", 0.04, 0.3, reverb=0.35)
for k, pan in (("g1", -0.55), ("g2", -0.5), ("g3", -0.45), ("g4", -0.4)):
    S.part(k, "guitar", f"アコギ（{k[1]}本目）", 0.085, pan, amp="crystal", chorus=0, sustain=1.0, reverb=0.22, autoScoop=False, push=0.008 * int(k[1]))
S.part("sth", "strings", "弦（上・のばす）", 0.06, 0.6, reverb=0.35)
S.part("stl", "strings", "弦（下・のばす）", 0.06, -0.6, reverb=0.35)
S.part("bass", "bass", "ベース", 0.27, 0)
S.part("bodhran", "tom", "ボーラン風の刻み", 0.13, 0.1, reverb=0, gainDb=-8)
S.part("kick", "kick", "キック", 0.3, 0, gainDb=-8)
S.part("snare", "snare", "スネア", 0.22, 0, push=0.01, gainDb=-8)
S.part("hihat", "hihat", "ハイハット", 0.08, 0, gainDb=-8)
S.part("ride", "crash", "ライド", 0.05, 0.2, gainDb=-8)
S.part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=-8)
S.part("tom", "tom", "タム（フィル）", 0.13, 0, reverb=0, gainDb=-8)
U3 = fmt(1 / 3)

def fill(tm):
    cnt = sum(1 for c in tm if c != "."); toks = []; j = 0; q = 0
    while j < 9:
        c = tm[j]; e = j + 1
        while e < 9 and tm[e] == ".": e += 1
        d = fmt((e - j) / 3)
        if c == ".": toks.append(f"R:{d}")
        else: toks.append(f"{['E3', 'C3', 'A2'][min(2, q * 3 // cnt)]}:{d}" + ("!" if c == "X" else "")); q += 1
        j = e
    return toks

arc = []
for bi, (k, rnd, p, i) in enumerate(plan):
    ch = chords[bi]; v = CH[ch]; nxt = chords[bi + 1] if bi + 1 < len(plan) else ch; last = k == "end"
    sq = S.seq((A if p == "A" else B)[i]) if k == "tune" else None
    # 旋律
    if k == "intro" and i >= 1:
        S.put("flute", bi, S.plain(S.seq(["D5:3 G5:3 B5:3", "A5:6 G5:3", "F#5:3 E5:3 D5:3"][i - 1])))
    if k == "tune":
        S.put("flute", bi, S.ornament(sq, "roll" if rnd >= 2 else "cut", bi * 13 + rnd, dens=0.8 + 0.2 * (rnd > 1)))
        if rnd >= 2: S.put("fiddle", bi, S.ornament(sq, "plain", 0, legato=False))   # フィドルは飾りなしで弓を返す（短い飾りの音で録音音源がプチッと鳴った）。飾りは笛が受け持つ
        if rnd == 3:
            h = []
            for n, kk in sq:
                if n == "R": h.append((n, kk)); continue
                m = md(n); h.append((nm(S.nb(S.nb(m, -1), -1)), kk))
            S.put("harm", bi, S.ornament(h, "plain", 0, legato=False))
    if last: S.put("flute", bi, ["G5:3"]); S.put("fiddle", bi, ["D5:3"]); S.put("harm", bi, ["B4:3"])
    # ドローン
    if k in ("intro", "end", "break") or (k == "tune" and rnd == 3 and p == "B"):
        S.put("pipe", bi, ["G3:3" if False else "G4:3"]); S.put("pipe5", bi, ["D4:3"] if k != "tune" else ["R:3"])
    # ハープ（前奏・1回目・間奏）
    arp = [x + 12 for x in v[1:]] + [v[1] + 24]
    if k in ("intro", "break") or (k == "tune" and rnd == 1):
        pat = [0, 1, 2, 3, 4, 3, 2, 1, 0] if i % 2 == 0 else [1, 2, 3, 4, 3, 2, 1, 2, 3]
        S.put("harp", bi, [f"{nm(arp[j])}:{U3}" for j in pat])
    if last: S.put("harp", bi, [f"{nm(x)}:{U3}" for x in arp[:4]] + [f"{nm(arp[4])}:{fmt(3 - 4 / 3)}"])
    # アコギ（各拍: ダウン2/3・アップ1/3。低い2本はのばす）
    if k == "tune" or (k == "break" and i >= 2) or last:
        for gi, g in enumerate(("g1", "g2", "g3", "g4")):
            n0 = v[gi + 1] if gi < 3 else v[4]
            if last: S.put(g, bi, [f"{nm(n0)}:3!"]); continue
            if gi < 2: S.put(g, bi, [f"{nm(n0)}:3!"]); continue
            toks = []
            for beat in range(3):
                acc = "!" if beat == 0 else ""
                toks += [f"{nm(n0)}:{fmt(2 / 3)}{acc}", f"{nm(n0)}:{U3},"]
            S.put(g, bi, toks)
    # 弦
    if (k == "tune" and (rnd == 3 or (rnd == 2 and p == "B"))) or last:
        S.put("sth", bi, [f"{nm(v[3] + 12)}:3"]); S.put("stl", bi, [f"{nm(v[2])}:3"])
    # ベース
    r = ROOT[ch]; f5 = r + 7; rn = ROOT[nxt]; ap = rn - 1 if rn > r else (rn + 1 if rn < r else f5)
    if last: S.put("bass", bi, [f"{nm(r)}:3"])
    elif k == "tune" and rnd >= 2: S.put("bass", bi, [f"{nm(r)}:1", f"{nm(r)}:{fmt(2 / 3)}", f"{nm(r)}:{U3}", f"{nm(ap)}:1"])
    elif k == "break" and i >= 2: S.put("bass", bi, [f"{nm(r)}:3"])
    # ボーラン（強・弱・中を3拍）
    bod = None
    if k == "tune" and rnd >= 2: bod = "XoxXoxXox" if i % 4 != 3 else "XoxXoxXxx"
    elif k == "break": bod = ["X..X..X..", "XoxX..X..", "XoxXoxXox", "XoxXxxXXX"][i]
    elif k == "intro" and i == 3: bod = "......XoX"
    if bod: S.put("bodhran", bi, S.pgrid(bod, {"X": "A2", "x": "C3,", "o": "C3,,"}))
    if last: S.put("bodhran", bi, S.pgrid("X........", {"X": "A2!"}))
    # 生ドラム（3回目）
    kk = sn = hh = "........."; ride = crash = False; tm = None
    if k == "tune" and rnd == 3:
        kk = "X.....X.." if i % 2 == 0 else "X..x..X.."; sn = "...X.....".replace(".....", "....X" if False else ".....")
        sn = "...X....." if i % 2 == 0 else "...X....x"
        if p == "B": ride = True
        else: hh = "x.xx.xx.x"
        crash = i == 0
        if i == 7: sn = "...X..xxX"; tm = None if p == "A" else "......xxX"
    if last: kk = "X........"; sn = "X........"; crash = True
    if tm:
        f0 = next(j for j, c in enumerate(tm) if c != "."); sn = sn[:f0] + "." * (9 - f0); hh = hh[:f0] + "." * (9 - f0); ride = False
    if crash: hh = "." + hh[1:]
    S.put("kick", bi, S.grid(kk)); S.put("snare", bi, S.grid(sn)); S.put("hihat", bi, S.grid(hh))
    if crash: S.put("crash", bi, S.grid("X........"))
    if ride: S.put("ride", bi, S.grid("x.xx.xx.x" if i % 2 else "x.xx.xxxx", "D2"))
    if tm: S.put("tom", bi, fill(tm))
    arc.append({"intro": 0.72, "break": 0.82, "end": 1.0}[k] if k != "tune" else {1: 0.8 if p == "A" else 0.86, 2: 0.92, 3: 1.0}[rnd])

out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-slipjig-meadow-dancer.json"
S.dump(out, "草原の踊り子（仮）",
       "（仮）ケルト音楽5曲の2曲目。踊りの曲「スリップジグ」（9/8・1小節に3拍、各拍を3つに分けるはずむ型）。BPM116・ト長調・約2分43秒。"
       "AABB の形を3回。笛ひとりとハープで始まり、フィドル・ボーラン・ベース、3回目に生ドラムと弦、フィドルの3度下のハモりが入る。飾りは笛にカット、フィドルにロール。",
       116, chords, arc)
