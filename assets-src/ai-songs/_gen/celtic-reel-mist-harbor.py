# 『霧の港のリール』（仮）: ケルト音楽5曲の1曲目。アイルランドの踊りの曲「リール」（4/4、8分音符が流れつづける速い曲）。
# BPM200・ホ短調（Eドリアン: C# の音が明るい）・Em と D の和音を行き来する（ダブル・トニック）。
# 形: 8小節の A と、高い音域の B を AABB で、4回くり返す。回ごとに楽器を足していく:
#   前奏4（バグパイプのドローン・ボーラン・ギター）→ 1回目（フィドルひとり、B から笛）→ 2回目（笛とフィドルのユニゾン・バンジョー・ベース）
#   → 間奏4（ボーランとタム）→ 3回目（生ドラムが入る。フィドルは3度上のハモり）→ 最後の AB（全員）→ 一発で終わる。
# 使い方: python3 celtic-reel-mist-harbor.py <出力.json>
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

EDOR = [4, 6, 7, 9, 11, 1, 2]
A = ["E5:2 B4:1 E5:1 G5:1 E5:1 B4:1 E5:1", "D5:3 A4:1 D5:1 E5:1 F#5:1 D5:1",
     "E5:2 B4:1 E5:1 G5:1 A5:1 B5:1 G5:1", "A5:1 F#5:1 D5:1 F#5:1 A5:1 B5:1 A5:1 F#5:1",
     "E5:2 B4:1 E5:1 G5:1 E5:1 B4:1 E5:1", "D5:3 E5:1 F#5:1 A5:1 F#5:1 D5:1",
     "B4:1 D5:1 F#5:1 D5:1 A5:1 F#5:1 D5:1 B4:1", "B4:1 A4:1 F#4:1 A4:1 B4:1 E4:1 E4:2"]
B = ["B5:2 G5:1 B5:1 E6:1 B5:1 G5:1 B5:1", "D6:2 B5:1 D6:1 G5:1 B5:1 D6:1 B5:1",
     "A5:3 F#5:1 A5:1 B5:1 A5:1 F#5:1", "E5:1 F#5:1 A5:1 C#6:1 E6:2 C#6:1 A5:1",
     "B5:2 E6:1 B5:1 G5:1 B5:1 D6:1 E6:1", "D6:1 B5:1 G5:1 B5:1 D6:3 B5:1",
     "A5:1 F#5:1 D5:1 F#5:1 A5:1 D6:1 C#6:1 A5:1", "B5:1 A5:1 F#5:1 D5:1 E5:2 E5:2"]
CA = "Em D Em D Em D Bm7 Em".split(); CB = "Em G D A7 Em G Dsus4 Em".split()

# 小節の並び（kind, 回, 部分, 何小節目）
plan = [("intro", 0, "-", i) for i in range(4)]
for rnd in (1, 2):
    for p in "AABB": plan += [("tune", rnd, p, i) for i in range(8)]
plan += [("break", 0, "-", i) for i in range(4)]
for p in "AABB": plan += [("tune", 3, p, i) for i in range(8)]
for p in "AB": plan += [("tune", 4, p, i) for i in range(8)]
plan += [("end", 0, "-", 0)]
S = Song(4, 2, len(plan), EDOR); S.check(A, B)
S.G = 0.15   # 飾りの一瞬の音（BPM200 で45ms。短いとフィドルの録音音源がプチッと鳴った）
chords = []
for k, rnd, p, i in plan:
    chords.append({"intro": "Em", "break": ["Em", "D", "Em", "D"][i] if k == "break" else "Em", "end": "Em"}.get(k) if k != "tune" else (CA if p == "A" else CB)[i])

CH = {"Em": [40, 47, 52, 55, 59], "D": [38, 45, 50, 54, 57], "G": [43, 47, 50, 55, 59], "A": [45, 52, 57, 61, 64], "Bm": [47, 54, 59, 62, 66], "Bm7": [47, 54, 57, 62, 66], "A7": [45, 52, 55, 61, 64], "Dsus4": [38, 45, 50, 55, 57]}
ROOT = {"Em": 40, "D": 38, "G": 43, "A": 45, "Bm": 47, "Bm7": 47, "A7": 45, "Dsus4": 38}

S.part("fiddle", "fiddle", "フィドル（旋律）", 0.2, -0.2, patch="violin", reverb=0.36, gainDb=2)
S.part("flute", "panflute", "笛（旋律）", 0.19, 0.22, patch="flute", reverb=0.38, gainDb=2)
S.part("harm", "fiddle", "フィドル2（3度上のハモり）", 0.11, -0.45, patch="violin", reverb=0.34)
S.part("banjo", "banjo", "バンジョー（旋律をなぞる）", 0.1, 0.45, reverb=0.22)
S.part("pipe", "bagpipe", "バグパイプのドローン（E）", 0.05, -0.3, reverb=0.3)
S.part("pipe5", "bagpipe", "バグパイプのドローン（B）", 0.04, 0.3, reverb=0.3)
for k, pan in (("g1", -0.55), ("g2", -0.5), ("g3", -0.45), ("g4", -0.4), ("g5", -0.35)):
    S.part(k, "guitar", f"アコギ（{k[1]}本目）", 0.085, pan, amp="crystal", chorus=0, sustain=0.9, reverb=0.22, autoScoop=False, push=0.008 * int(k[1]))
S.part("sth", "strings", "弦（上・のばす）", 0.06, 0.6, reverb=0.35)
S.part("stl", "strings", "弦（下・のばす）", 0.06, -0.6, reverb=0.35)
S.part("bass", "bass", "ベース", 0.27, 0)
S.part("bodhran", "tom", "ボーラン風の刻み", 0.13, 0.1, reverb=0, gainDb=-8, bright=-0.4)
S.part("kick", "kick", "キック", 0.3, 0, gainDb=-8)
S.part("snare", "snare", "スネア", 0.23, 0, push=0.01, gainDb=-8)
S.part("hihat", "hihat", "ハイハット", 0.08, 0, gainDb=-8)
S.part("ride", "crash", "ライド", 0.05, 0.2, gainDb=-8)
S.part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=-8)
S.part("tom", "tom", "タム（フィル）", 0.13, 0, reverb=0, gainDb=-8)

def mel(p, i): return S.seq((A if p == "A" else B)[i])
arc = []
for bi, (k, rnd, p, i) in enumerate(plan):
    ch = chords[bi]; v = CH[ch]; nxt = chords[bi + 1] if bi + 1 < len(plan) else ch
    last = k == "end"
    first_of_part = k == "tune" and i == 0
    # ── 旋律 ──
    if k == "tune":
        sq = mel(p, i)
        fid = rnd in (1, 2, 3) or rnd == 4
        if fid: S.put("fiddle", bi, S.ornament(sq, "roll", bi * 7 + rnd, dens=0.6 + 0.2 * rnd, legato=False))   # フィドルは弓を1音ずつ返す（つなぐと音源がプチッと鳴った）
        if (rnd == 1 and p == "B") or rnd >= 2: S.put("flute", bi, S.ornament(sq, "cut", bi * 11 + rnd))
        if rnd == 2 and p == "B": S.put("banjo", bi, S.plain(sq, legato=False))
        if rnd >= 3:   # 3度上のハモり（音階の上で2つ上）
            h = []
            for n, kk in sq:
                if n == "R": h.append((n, kk)); continue
                m = md(n); m2 = S.nb(S.nb(m, 1), 1)
                h.append((nm(m2 if m2 <= 88 else m - 12 + (m2 - m)), kk))
            S.put("harm", bi, S.ornament(h, "plain", 0) if (rnd == 3 and p == "B") or rnd == 4 else [f"R:4"])
    if last:
        S.put("fiddle", bi, ["E5:4"]); S.put("flute", bi, ["E6:4"]); S.put("harm", bi, ["B5:4"])
    # ── ドローン ──
    drone = k in ("intro", "end") or (k == "tune" and rnd == 1 and p == "A") or (k == "tune" and rnd == 4 and p == "B")
    if drone: S.put("pipe", bi, ["E4:4"]); S.put("pipe5", bi, ["B4:4"] if k != "tune" else ["R:4"])
    # ── ギター（8分のストローク。1・3拍目を強く。低い2本はのばす） ──
    gtr = k in ("intro", "break") or k == "tune" or last
    for gi, g in enumerate(("g1", "g2", "g3", "g4", "g5")):
        if not gtr or (k == "intro" and i < 2): continue
        if last: S.put(g, bi, [f"{nm(v[gi])}:4!"]); continue
        if gi < 2: S.put(g, bi, [f"{nm(v[gi])}:2!", f"{nm(v[gi])}:2"]); continue
        toks = []
        for e in range(8):
            acc = "!" if e in (0, 4) else ("," if e % 2 else "")
            if k == "tune" and rnd == 1 and p == "A" and e % 2: toks.append("R:0.5"); continue
            toks.append(f"{nm(v[gi])}:0.5{acc}")
        S.put(g, bi, toks)
    # ── 弦（2回目のBから。和音をのばして広がりを出す） ──
    if (k == "tune" and (rnd >= 3 or (rnd == 2 and p == "B"))) or k == "break" or last:
        S.put("sth", bi, [f"{nm(v[3] + 12)}:4"]); S.put("stl", bi, [f"{nm(v[2])}:4"])
    # ── ベース ──
    r = ROOT[ch] - 12; f5 = r + 7; rn = ROOT[nxt] - 12
    ap = rn - 1 if rn > r else (rn + 1 if rn < r else f5)
    if last: S.put("bass", bi, [f"{nm(r)}:4"])
    elif k == "tune" and rnd >= 2 or k == "break" and i >= 2:
        S.put("bass", bi, [f"{nm(r)}:1", f"{nm(r)}:0.5", f"{nm(r)}:0.5", f"{nm(f5)}:1", f"{nm(ap)}:1"])
    elif k == "tune" and rnd == 1 and p == "B": S.put("bass", bi, [f"{nm(r)}:2", f"{nm(f5)}:2"])
    # ── ボーラン（リール: 1・3拍目が強い。8分で流し、ところどころ3連の装飾） ──
    if k in ("intro", "break") or k == "tune":
        if k == "intro": pat = "X...X..." if i < 2 else "XoxoXoxo"
        elif k == "break": pat = ["XoxoXoxo", "XoxxXoxo", "XoxoXoxx", "XxxxXxXX"][i]
        elif rnd == 1 and p == "A": pat = "X...X.xo" if i % 2 else "X...X..."
        else: pat = "XoxoXoxo" if i % 4 != 3 else "XoxoXxxo"
        S.put("bodhran", bi, S.pgrid(pat, {"X": "A2", "x": "C3,", "o": "C3,,"}))
    if last: S.put("bodhran", bi, S.pgrid("X.......", {"X": "A2"}))
    # ── 生ドラム（3回目から） ──
    kk = sn = hh = "........"; ride = crash = False; tm = None
    if k == "tune" and rnd >= 3:
        kk = "X...X.x." if i % 2 == 0 else "X..xX..."; sn = "..X...X."
        if p == "B": ride = True
        else: hh = "xoxoxoxo"
        crash = i == 0
        if i == 7: sn = "..X..xXX" if p == "A" else "..X.xxxx"; tm = None if p == "A" else "....xxXX"
    elif k == "break" and i >= 2:
        kk = "X...X..."; sn = "..X...X." if i == 2 else "..X.XxXX"; hh = "xoxoxoxo" if i == 2 else "xoxo...."
        if i == 3: tm = "....xxXX"
    if last: kk = "X......."; sn = "X......."; crash = True
    if tm:
        f0 = next(j for j, c in enumerate(tm) if c != ".")
        sn = sn[:f0] + "." * (8 - f0); hh = hh[:f0] + "." * (8 - f0); ride = False
    if crash: hh = "." + hh[1:]
    S.put("kick", bi, S.grid(kk)); S.put("snare", bi, S.grid(sn)); S.put("hihat", bi, S.grid(hh))
    if crash: S.put("crash", bi, S.grid("X......."))
    if ride: S.put("ride", bi, S.grid("x.x.x.x." if i % 2 else "x.xxx.x.", "D2"))
    if tm:
        cnt = sum(1 for c in tm if c != "."); toks = []; j = 0; q = 0
        while j < 8:
            c = tm[j]; e = j + 1
            while e < 8 and tm[e] == ".": e += 1
            d = fmt((e - j) / 2)
            if c == ".": toks.append(f"R:{d}")
            else: toks.append(f"{['E3', 'C3', 'A2'][min(2, q * 3 // cnt)]}:{d}" + ("!" if c == "X" else "")); q += 1
            j = e
        S.put("tom", bi, toks)
    arc.append({"intro": 0.75, "break": 0.85, "end": 1.05}.get(k, {1: 0.82, 2: 0.92, 3: 1.0, 4: 1.04}.get(rnd, 1)) if k != "tune" else {1: 0.82 if p == "A" else 0.88, 2: 0.94, 3: 1.0, 4: 1.04}[rnd])

out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-reel-mist-harbor.json"
S.dump(out, "霧の港のリール（仮）",
       "（仮）ケルト音楽5曲の1曲目。アイルランドの踊りの曲「リール」（4/4・8分音符が流れつづける速い曲）。BPM200・ホ短調（Eドリアン）・約2分25秒。"
       "Em と D を行き来する和音、AABB の形を4回。フィドルひとりで始まり、笛・バンジョー・ベース・生ドラム・3度上のハモりと、回ごとに楽器が増える。"
       "飾りはフィドルにロール、笛にカット。ボーランの8分の刻み、DADGAD 風のアコギのストローク、バグパイプのドローン。",
       200, chords, arc)
