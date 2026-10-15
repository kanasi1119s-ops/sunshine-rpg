# 『市場のホーンパイプ』（仮）: ケルト音楽5曲の4曲目。「ホーンパイプ」（4/4、8分音符を「タッカ」とはねる、ゆったり重い足取りの踊りの曲）。
# BPM104・イ（Aミクソリディアン: G の音が素朴）・swing 0.6。A と B の終わりは、ホーンパイプのお決まりの「3つの4分音符」で止まる。
# 形: 前奏2（バンジョーの呼び込み）→ 1回目 AABB（フィドル・アコギ・ベース）→ 2回目 AABB（笛が加わる・バンジョー・ボーラン）
#   → 3回目 AB（生ドラム・弦・フィドルは下のハモり）→ 一発で終わる。
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

AMIX = [9, 11, 1, 2, 4, 6, 7]
A = ["A4:1 C#5:1 E5:1 A5:1 G5:1 E5:1 C#5:1 E5:1", "D5:1 G5:1 B5:1 G5:1 D5:1 B4:1 G4:2",
     "A4:1 C#5:1 E5:1 A5:1 B5:1 A5:1 G5:1 E5:1", "F#5:1 A5:1 F#5:1 D5:1 E5:1 D5:1 C#5:1 B4:1",
     "A4:1 C#5:1 E5:1 A5:1 G5:1 E5:1 C#5:1 E5:1", "D5:1 G5:1 B5:1 D6:1 B5:1 G5:1 E5:1 D5:1",
     "F#5:1 A5:1 D6:1 A5:1 G5:1 F#5:1 E5:1 D5:1", "C#5:1 E5:1 A4:2 A4:2 A4:2"]
B = ["C#6:1 A5:1 E5:1 A5:1 C#6:1 E6:1 D6:1 C#6:1", "B5:1 G5:1 D5:1 G5:1 B5:1 D6:1 B5:1 G5:1",
     "A5:1 C#6:1 E6:1 C#6:1 A5:1 E5:1 C#5:1 E5:1", "F#5:1 B5:1 D6:1 B5:1 F#5:1 D5:1 B4:1 D5:1",
     "C#6:1 A5:1 E5:1 A5:1 C#6:1 E6:1 D6:1 C#6:1", "D6:1 B5:1 G5:1 B5:1 D6:1 E6:1 D6:1 B5:1",
     "A5:1 F#5:1 D5:1 F#5:1 A5:1 G5:1 F#5:1 E5:1", "A5:2 E5:2 A4:2 R:2"]
CA = "A G A D A G D A".split(); CB = "A G A Bm A G D A".split()
plan = [("intro", 0, "-", i) for i in range(2)]
for rnd in (1, 2):
    for p in "AABB": plan += [("tune", rnd, p, i) for i in range(8)]
for p in "AB": plan += [("tune", 3, p, i) for i in range(8)]
plan += [("end", 0, "-", 0)]
S = Song(4, 2, len(plan), AMIX); S.check(A, B); S.G = 0.08   # BPM104 で約46ms
chords = [("A" if k in ("intro", "end") else (CA if p == "A" else CB)[i]) for k, rnd, p, i in plan]
CH = {"A": [45, 52, 57, 61, 64], "G": [43, 50, 55, 59, 62], "D": [50, 54, 57, 62, 66], "Bm": [47, 54, 59, 62, 66]}
ROOT = {"A": 33, "G": 31, "D": 38, "Bm": 35}

S.part("fiddle", "fiddle", "フィドル（旋律）", 0.2, -0.2, patch="violin", reverb=0.34, gainDb=2)
S.part("flute", "panflute", "笛（旋律）", 0.18, 0.22, patch="flute", reverb=0.36, gainDb=1)
S.part("harm", "fiddle", "フィドル2（下のハモり）", 0.1, -0.45, patch="violin", reverb=0.34)
S.part("banjo", "banjo", "バンジョー", 0.11, 0.45, reverb=0.2)
for k, pan in (("g1", -0.55), ("g2", -0.5), ("g3", -0.45), ("g4", -0.4)):
    S.part(k, "guitar", f"アコギ（{k[1]}本目）", 0.085, pan, amp="crystal", chorus=0, sustain=0.9, reverb=0.22, autoScoop=False, push=0.008 * int(k[1]))
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
BOD = {"X": "A2", "x": "C3,", "o": "C3,,"}

def fill(tm):
    cnt = sum(1 for c in tm if c != "."); toks = []; j = 0; q = 0
    while j < 8:
        c = tm[j]; e = j + 1
        while e < 8 and tm[e] == ".": e += 1
        d = fmt((e - j) / 2)
        if c == ".": toks.append(f"R:{d}")
        else: toks.append(f"{['E3', 'C3', 'A2'][min(2, q * 3 // cnt)]}:{d}" + ("!" if c == "X" else "")); q += 1
        j = e
    return toks

arc = []
for bi, (k, rnd, p, i) in enumerate(plan):
    ch = chords[bi]; v = CH[ch]; nxt = chords[bi + 1] if bi + 1 < len(plan) else ch; last = k == "end"
    sq = S.seq((A if p == "A" else B)[i]) if k == "tune" else None
    if k == "intro":   # バンジョーの呼び込み（2小節）
        S.put("banjo", bi, ["A4:0.5", "C#5:0.5", "E5:0.5", "A5:0.5", "G5:0.5", "E5:0.5", "C#5:0.5", "E5:0.5"] if i == 0 else ["D5:0.5", "E5:0.5", "F#5:0.5", "G5:0.5", "A5:1", "E5:1"])
    if k == "tune":
        S.put("fiddle", bi, S.ornament(sq, "cut", bi * 5 + rnd, dens=0.6, legato=False))
        if rnd >= 2: S.put("flute", bi, S.ornament(sq, "cut", bi * 11 + rnd, dens=0.8, legato=False))
        if rnd == 2 and p == "B" or rnd == 3: S.put("banjo", bi, S.plain(sq, legato=False))
        if rnd == 3:
            pcs = {x % 12 for x in v}; h = []
            for n, kk in sq:
                if n == "R": h.append((n, kk)); continue
                m = md(n); c = m - 3
                while c % 12 not in pcs: c -= 1
                h.append((nm(c), kk))
            S.put("harm", bi, S.ornament(h, "plain", 0, legato=False))
    if last: S.put("fiddle", bi, ["A4:2", "R:2"]); S.put("flute", bi, ["A5:2", "R:2"]); S.put("harm", bi, ["E4:2", "R:2"]); S.put("banjo", bi, ["A4:1", "R:3"])
    # アコギ（はねる8分。1・3拍目は低い弦のベース音、2・4拍目に和音＝「ブン・チャッ」）
    if k == "tune" or last:
        for gi, g in enumerate(("g1", "g2", "g3", "g4")):
            n0 = v[gi + 1]
            if last: S.put(g, bi, [f"{nm(n0)}:4!"]); continue
            if gi == 0: S.put(g, bi, [f"{nm(v[0])}:1!", "R:1", f"{nm(v[0] + 7 if v[0] + 7 < 57 else v[0])}:1", "R:1"]); continue
            S.put(g, bi, ["R:1", f"{nm(n0)}:0.5!", f"{nm(n0)}:0.5,", "R:1", f"{nm(n0)}:0.5!", f"{nm(n0)}:0.5,"])
    # 弦
    if (k == "tune" and (rnd == 3 or (rnd == 2 and p == "B"))) or last:
        S.put("sth", bi, [f"{nm(v[3] + 12)}:4"]); S.put("stl", bi, [f"{nm(v[2])}:4"])
    # ベース（1・3拍目、次の和音へのつなぎ）
    r = ROOT[ch]; f5 = r + 7; rn = ROOT[nxt]; ap = rn - 1 if rn > r else (rn + 1 if rn < r else f5)
    if last: S.put("bass", bi, [f"{nm(r)}:2", "R:2"])
    elif k == "tune": S.put("bass", bi, [f"{nm(r)}:1.5", f"{nm(r)}:0.5", f"{nm(f5)}:1.5", f"{nm(ap)}:0.5"])
    # ボーラン（2回目から）
    if k == "tune" and rnd >= 2:
        S.put("bodhran", bi, S.pgrid("X.xoX.xo" if i % 4 != 3 else "X.xoXxxx", BOD))
    if last: S.put("bodhran", bi, S.pgrid("X.......", {"X": "A2"}))
    # 生ドラム（3回目）
    kk = sn = hh = "........"; ride = crash = False; tm = None
    if k == "tune" and rnd == 3:
        kk = "X...X..." if i % 2 == 0 else "X..xX..."; sn = "..X...X."
        if p == "B": ride = True
        else: hh = "x.x.x.x."
        crash = i == 0
        if i == 7 and p == "A": sn = "..X..xXX"
        if i == 6 and p == "B": tm = "....xxXX"
    if last: kk = "X......."; sn = "X......."; crash = True
    if tm:
        f0 = next(j for j, c in enumerate(tm) if c != "."); sn = sn[:f0] + "." * (8 - f0); hh = hh[:f0] + "." * (8 - f0); ride = False
    if crash: hh = "." + hh[1:]
    S.put("kick", bi, S.grid(kk)); S.put("snare", bi, S.grid(sn)); S.put("hihat", bi, S.grid(hh))
    if crash: S.put("crash", bi, S.grid("X......."))
    if ride: S.put("ride", bi, S.grid("x.x.x.x." if i % 2 else "x.xxx.x.", "D2"))
    if tm: S.put("tom", bi, fill(tm))
    arc.append({"intro": 0.78, "end": 1.0}[k] if k != "tune" else {1: 0.84, 2: 0.93, 3: 1.0}[rnd])

out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-hornpipe-market.json"
S.dump(out, "市場のホーンパイプ（仮）",
       "（仮）ケルト音楽5曲の4曲目。8分音符を「タッカ」とはねる踊りの曲「ホーンパイプ」。BPM104・イ（Aミクソリディアン）・swing 0.6・約2分40秒。"
       "A と B の終わりは3つの4分音符で止まるお決まりの形。バンジョーの呼び込みから、フィドル・笛・ボーラン、3回目は生ドラムと弦、フィドルの下のハモり。アコギは「ブン・チャッ」の刻み。",
       104, chords, arc, extra={"swing": 0.6})
