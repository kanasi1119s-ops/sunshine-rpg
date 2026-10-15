# 『焚き火のポルカ』（仮）: ケルト音楽5曲の5曲目。「ポルカ」（2/4、速くて明るい踊りの曲。アイルランド南西部のスタイル）。
# BPM138・ニ長調 → 最後の1回だけ1音上のホ長調に上がる。伴奏は「ブン・チャッ」（1拍目に低い音、裏に和音）。
# 形: 前奏4（アコギとボーラン）→ 1回目 AABB（笛）→ 2回目（フィドルと笛・バンジョー）→ 3回目（生ドラム）→ 間奏8（ボーランの見せ場とタム）
#   → 4回目（ホ長調に上がって全員・フィドルの下のハモり）→ 一発で終わる。
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

DMAJ = [2, 4, 6, 7, 9, 11, 1]
A = ["A5:2 F#5:2 A5:2 F#5:2", "A5:1 B5:1 A5:1 F#5:1 D5:4", "G5:2 E5:2 G5:2 E5:2", "G5:1 A5:1 G5:1 E5:1 C#5:4",
     "A5:2 F#5:2 A5:2 D6:2", "B5:1 A5:1 G5:1 B5:1 D6:4", "C#6:1 B5:1 A5:1 G5:1 F#5:2 E5:2", "D5:2 A4:2 D5:4"]
B = ["B5:2 D6:2 B5:2 G5:2", "A5:2 F#5:2 D5:4", "E5:1 F#5:1 G5:1 A5:1 C#6:2 A5:2", "D6:4 A5:4",
     "B5:2 D6:2 B5:2 G5:2", "A5:1 B5:1 A5:1 F#5:1 D5:2 F#5:2", "E5:2 C#5:2 E5:2 A5:2", "D5:2 A4:2 D5:4"]
CA = "D D A A D G A D".split(); CB = "G D A D G D A D".split()
plan = [("intro", 0, "-", i) for i in range(4)]
for rnd in (1, 2, 3):
    for p in "AABB": plan += [("tune", rnd, p, i) for i in range(8)]
plan += [("break", 0, "-", i) for i in range(8)]
for p in "AABB": plan += [("tune", 4, p, i) for i in range(8)]
plan += [("end", 0, "-", i) for i in range(2)]
S = Song(2, 4, len(plan), DMAJ); S.check(A, B); S.G = 0.1   # BPM138 で約43ms
UP = {"D": "E", "A": "B", "G": "A"}
def chord_of(k, rnd, p, i):
    if k == "intro": return ["D", "A", "D", "A"][i]
    if k == "break": return ["D", "A", "D", "A", "D", "A", "B", "B"][i]
    if k == "end": return "E"
    c = (CA if p == "A" else CB)[i]
    return UP[c] if rnd == 4 else c
chords = [chord_of(*x) for x in plan]
CH = {"D": [38, 50, 54, 57, 62], "A": [33, 45, 49, 52, 57], "G": [31, 43, 47, 50, 55], "E": [40, 52, 56, 59, 64], "B": [35, 47, 51, 54, 59]}

S.part("flute", "panflute", "笛（旋律）", 0.2, 0.22, patch="flute", reverb=0.32, gainDb=2)
S.part("fiddle", "fiddle", "フィドル（旋律）", 0.19, -0.2, patch="violin", reverb=0.3, gainDb=2)
S.part("harm", "fiddle", "フィドル2（下のハモり）", 0.1, -0.45, patch="violin", reverb=0.3)
S.part("banjo", "banjo", "バンジョー", 0.11, 0.45, reverb=0.2)
for k, pan in (("g1", -0.5), ("g2", -0.45), ("g3", -0.4), ("g4", -0.35)):
    S.part(k, "guitar", f"アコギ（{k[1]}本目）", 0.085, pan, amp="crystal", chorus=0, sustain=0.8, reverb=0.2, autoScoop=False, push=0.006 * int(k[1]))
S.part("sth", "strings", "弦（上・のばす）", 0.055, 0.6, reverb=0.32)
S.part("stl", "strings", "弦（下・のばす）", 0.055, -0.6, reverb=0.32)
S.part("bass", "bass", "ベース", 0.27, 0)
S.part("bodhran", "tom", "ボーラン風の刻み", 0.13, 0.1, reverb=0, gainDb=-8)
S.part("kick", "kick", "キック", 0.3, 0, gainDb=-8)
S.part("snare", "snare", "スネア", 0.22, 0, push=0.01, gainDb=-8)
S.part("hihat", "hihat", "ハイハット", 0.08, 0, gainDb=-8)
S.part("ride", "crash", "ライド", 0.05, 0.2, gainDb=-8)
S.part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=-8)
S.part("tom", "tom", "タム（フィル）", 0.13, 0, reverb=0, gainDb=-8)
BOD = {"X": "A2", "x": "C3,", "o": "C3,,"}

def fill(tm):
    cnt = sum(1 for c in tm if c != "."); toks = []; j = 0; q = 0
    while j < 8:
        c = tm[j]; e = j + 1
        while e < 8 and tm[e] == ".": e += 1
        d = fmt((e - j) / 4)
        if c == ".": toks.append(f"R:{d}")
        else: toks.append(f"{['E3', 'C3', 'A2'][min(2, q * 3 // cnt)]}:{d}" + ("!" if c == "X" else "")); q += 1
        j = e
    return toks

arc = []
for bi, (k, rnd, p, i) in enumerate(plan):
    ch = chords[bi]; v = CH[ch]; last = k == "end" and i == 1
    sh = 2 if rnd == 4 or k == "end" else 0
    sq = S.seq((A if p == "A" else B)[i]) if k == "tune" else None
    if k == "tune":
        S.put("flute", bi, S.ornament(sq, "cut", bi * 3 + rnd, shift=sh, dens=0.6, legato=False))
        if rnd >= 2: S.put("fiddle", bi, S.ornament(sq, "plain", 0, shift=sh, legato=False))
        if rnd in (2, 4) and p == "B" or rnd == 3 and p == "A": S.put("banjo", bi, S.plain(sq, shift=sh - 12, legato=False))
        if rnd == 4:
            pcs = {x % 12 for x in v}; h = []
            for n, kk in sq:
                m = md(n) + sh; c = m - 3
                while c % 12 not in pcs: c -= 1
                h.append((nm(c), kk))
            S.put("harm", bi, S.ornament(h, "plain", 0, legato=False))
    if k == "end" and i == 0: S.put("flute", bi, ["E6:0.5", "B5:0.5", "E6:0.5", "B5:0.5"]); S.put("fiddle", bi, ["E5:0.5", "B4:0.5", "E5:0.5", "B4:0.5"])
    if last: S.put("flute", bi, ["E6:0.5", "R:1.5"]); S.put("fiddle", bi, ["E5:0.5", "R:1.5"]); S.put("harm", bi, ["B4:0.5", "R:1.5"]); S.put("banjo", bi, ["E5:0.5", "R:1.5"])
    # アコギ（ブン・チャッ: 1拍目に低い弦、裏拍に和音）
    for gi, g in enumerate(("g1", "g2", "g3", "g4")):
        if last: S.put(g, bi, [f"{nm(v[gi + 1] if gi else (v[0] + 12 if v[0] < 40 else v[0]))}:0.5!", "R:1.5"]); continue
        if gi == 0:   # 低い弦（ギターの音域 E2 より下にならないように1オクターブ上げる）
            lo = v[0] + 12 if v[0] < 40 else v[0]
            alt = lo + 7 if i % 2 else lo
            S.put(g, bi, [f"{nm(lo)}:0.5!", "R:0.5", f"{nm(alt)}:0.5", "R:0.5"])
        else: S.put(g, bi, ["R:0.5", f"{nm(v[gi + 1])}:0.5!", "R:0.5", f"{nm(v[gi + 1])}:0.5,"])
    # 弦（3回目のBと4回目）
    if (k == "tune" and (rnd == 4 or (rnd == 3 and p == "B"))) or k == "end":
        S.put("sth", bi, [f"{nm(v[3] + 12)}:2"]); S.put("stl", bi, [f"{nm(v[2])}:2"])
    # ベース（1拍目に根音、2拍目に5度。裏で次へ）
    r = v[0] - 12 if v[0] >= 40 else v[0]
    if last: S.put("bass", bi, [f"{nm(r)}:0.5", "R:1.5"])
    elif k in ("tune", "end") and (rnd >= 2 or k == "end") or (k == "break" and i >= 4):
        S.put("bass", bi, [f"{nm(r)}:0.75", f"{nm(r)}:0.25", f"{nm(r + 7)}:1"])
    # ボーラン
    if (k == "tune" and rnd >= 2) or k in ("intro", "end") and not last:
        S.put("bodhran", bi, S.pgrid("X.x.X.xo" if i % 4 != 3 else "X.x.Xxxx", BOD))
    if k == "break":
        S.put("bodhran", bi, S.pgrid(["X.x.X.x.", "X.xoX.xo", "X.x.Xoxo", "XxxoX.xo", "X.x.X.x.", "XoxoXoxo", "XxxxXxxx", "X...X..."][i], BOD))
    if last: S.put("bodhran", bi, S.pgrid("X.......", {"X": "A2"}))
    # 生ドラム（3・4回目）。ポルカ: キックは表、スネアは裏
    kk = sn = hh = "........"; ride = crash = False; tm = None
    if k == "tune" and rnd >= 3:
        kk = "X...X..."; sn = "..x...x." if i % 2 == 0 else "..x...xx"
        if p == "B" and rnd == 4: ride = True
        else: hh = "x.x.x.x."
        crash = i == 0
        if i == 7 and p == "B": tm = "....xxXX"
    elif k == "break" and i >= 4:
        kk = "X...X..."; sn = "..x...x."; hh = "x.x.x.x." if i < 6 else "........"
        if i == 6: tm = "xxxxXxxx"
        if i == 7: tm = "X...X.XX"; kk = "X...X..."
    elif k == "end" and i == 0: kk = "X...X..."; sn = "..x.XxXX"
    if last: kk = "X......."; sn = "X......."; crash = True
    if tm:
        f0 = next(j for j, c in enumerate(tm) if c != "."); sn = sn[:f0] + "." * (8 - f0); hh = hh[:f0] + "." * (8 - f0); ride = False
    if crash: hh = "." + hh[1:]
    S.put("kick", bi, S.grid(kk)); S.put("snare", bi, S.grid(sn)); S.put("hihat", bi, S.grid(hh))
    if crash: S.put("crash", bi, S.grid("X......."))
    if ride: S.put("ride", bi, S.grid("x.x.x.x." if i % 2 else "x.xxx.x.", "D2"))
    if tm: S.put("tom", bi, fill(tm))
    arc.append({"intro": 0.8, "break": 0.88, "end": 1.05}[k] if k != "tune" else {1: 0.84, 2: 0.92, 3: 0.98, 4: 1.04}[rnd])

out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-polka-bonfire.json"
S.dump(out, "焚き火のポルカ（仮）",
       "（仮）ケルト音楽5曲の5曲目。速くて明るい踊りの曲「ポルカ」（2/4）。BPM138・ニ長調、最後の1回はホ長調に上がる・約2分。"
       "アコギの「ブン・チャッ」とボーランで始まり、笛・フィドル・バンジョー・生ドラム、ボーランの見せ場の間奏をはさんで、1音上がって全員で盛り上がって終わる。",
       138, chords, arc)
