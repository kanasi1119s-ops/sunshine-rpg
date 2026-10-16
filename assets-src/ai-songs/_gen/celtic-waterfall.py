# 『霧ふる滝の祈り』（仮）: 滝の流れを感じる、神秘的なケルト音楽（2026-10-16、人間の依頼「ケルト曲で滝の流れを感じる神秘な感じの曲を4~4分半で作って」）。
# 4/4・BPM78・ロ短調のドリアン（G# が明るく神秘的）→ 山場で全音上の嬰ハ短調ドリアン → 戻る。86小節・約4分25秒。
# 滝の表し方: ハープが和音の音を高い所から低い所へ16分で「流れ落ちる」（1小節に2回）。鉄琴の「しずく」にピンポンディレイ。
#   急流の所では、フィドルが音階を16分で駆け下り、和音を駆け上がる。
# 形と、だれが鳴るか:
#   霧6（パッドと低い弦の持続、鉄琴のしずく、ハープの流れ落ち）
#   → 主題A16（ロー・ホイッスル風の笛。ピアノは左手の8分の転がしと右手の和音。チェロ。後半からボーラン）
#   → B16（フィドルが高く歌う。アコーディオンが和音をのばし、弦が入る。後半の頭はナポリの C で神秘的に）
#   → 滝つぼ8（静かに。笛の断片・鉄琴・ピアノの和音・パッド。最後に大太鼓のロールでふくらむ）
#   → 急流16（笛が主題A、フィドルが16分で駆け回る。キック・ボーラン・ライド・大太鼓のフィル）
#   → 山場16（全音上で B の旋律。フィドルと笛のオクターブ、ホルンの長い音、全員）
#   → 霧に戻る8（主題の頭だけ。最後は Bsus2 で解決しないまま消える）
# 人間の指示（2026-10-16）: FX を使う／ピアノは左手と右手で（右手は和音を同時に）／定番から外したコード進行。
#   進行: Bm Bm/A E/G#（ドリアンの IV）Gmaj7 …、B の後半は C（ナポリ）Gmaj7/B A D/F# … F#7、滝つぼは Gmaj7 C/G（♭II をゆらす）、終わりは Bsus2。
# MIDI のチャンネルは（ドラム以外で）15まで。
# 既存の曲のメロディは使わない（CLAUDE.md 1-1）。旋律はすべてこの曲のために書いたもの。
# 使い方: python3 celtic-waterfall.py <出力.json>
# 書き出し: --drums muldjord --bass finger --orchestra vsco --piano salamander --guitar shiny-acoustic --master-preset rock-clean --master -13.5（点数 8.08）
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

# ---------------- 音階（B を主音とした値。山場は +2）----------------
BDOR = [11, 1, 2, 4, 6, 8, 9]
BNEA = [11, 0, 2, 4, 6, 7, 9]      # C（ナポリ）・C/G の上
BHM = [11, 1, 2, 4, 6, 7, 10]      # F#7 の上（和声的短音階）
BAEO = [11, 1, 2, 4, 6, 7, 9]      # Gmaj7・Em7 の上（G を使う）
def scale_of(ch, shift=0):
    c = ch.split("/")[0]
    if c.startswith("C") and not c.startswith("C#"): sc = BNEA
    elif c.startswith("F#7"): sc = BHM
    elif c.startswith("G") or c.startswith("Em"): sc = BAEO
    else: sc = BDOR
    return [(x + shift) % 12 for x in sc]

# ---------------- 旋律（1小節＝16分音符16個）----------------
A1 = ["F#5:6 E5:2 D5:4 B4:4", "A4:8 B4:4 D5:4", "E5:6 G#5:2 F#5:4 E5:4", "D5:4 B4:4 F#5:8",
      "A5:6 G5:2 F#5:4 D5:4", "E5:4 G5:4 B5:6 A5:2", "B5:4 F#5:4 C#5:8", "C#5:12 R:4"]
A2 = ["F#5:6 E5:2 D5:4 B4:4", "A4:4 B4:4 D5:4 F#5:4", "G#5:6 A5:2 B5:8", "A5:4 F#5:4 D5:8",
      "C#6:6 B5:2 A5:4 F#5:4", "G5:4 B5:4 E5:8", "E5:4 F#5:2 G5:2 A5:4 C#5:4", "B4:16"]
B1 = ["D6:6 B5:2 F#5:8", "E5:4 A5:4 C#6:8", "D6:4 C#6:4 A5:4 F#5:4", "B5:12 F#5:4",
      "G5:6 B5:2 E6:8", "C#6:6 A5:2 F#5:8", "D6:4 B5:4 G5:4 F#5:4", "E5:12 R:4"]
B2 = ["E6:6 C6:2 G5:8", "D6:6 B5:2 F#5:8", "C#6:4 E6:4 A5:8", "F#5:4 A5:4 D6:8",
      "B5:6 A5:2 G5:4 F#5:4", "E5:4 G5:4 B5:8", "A#5:6 C#6:2 E6:8", "D6:4 C#6:4 B5:8"]
POOL = ["B4:8 D5:4 F#5:4", "E5:12 R:4", "D5:8 F#5:4 A5:4", "G5:12 R:4",
        "B5:8 G5:4 E5:4", "F#5:8 C#5:4 A4:4", "B4:4 D5:4 F#5:8", "E5:12 R:4"]
CODA = A1[:4] + ["F#5:8 E5:8", "D5:16", "R:16", "R:16"]
CA1 = "Bm Bm/A E/G# Gmaj7 D/F# Em7 F#sus4 F#m".split()
CA2 = "Bm Bm/A E/G# Gmaj7 Dmaj7/A Em7 A Bm".split()
CB1 = "Gmaj7 A D/F# Bm Em7 F#m7 Gmaj7 Asus4".split()
CB2 = "C Gmaj7/B A D/F# Gmaj7 Em7 F#7 Bm".split()
CPOOL = "Gmaj7 C/G Gmaj7 C/G Em7 F#m7 Gmaj7 F#7sus4".split()
CMIST = "Bm Bm/A Gmaj7 E/G# Bm Bm/A".split()
CCODA = "Bm Bm/A E/G# Gmaj7 Bm Bm/A Gmaj7 Bsus2".split()

def up2(seq): return " ".join(x if x.startswith("R:") else f"{nm(md(x.split(':')[0]) + 2)}:{x.split(':')[1]}" for x in seq.split())
def upc(ch):
    F = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]; PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    def one(x):
        m = re.match(r"^([A-G])([#b]?)(.*)$", x); r = (PC[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0) + 2) % 12
        return F[r] + m.group(3)
    return "/".join(one(x) for x in ch.split("/"))

plan = []
def sec(name, chords, mel=None, shift=0):
    for i, c in enumerate(chords):
        plan.append(dict(k=name, i=i, orig=c, ch=(upc(c) if shift else c), mel=(up2(mel[i]) if (mel and shift) else (mel[i] if mel else None)), shift=shift))
sec("mist", CMIST)
sec("A", CA1 + CA2, A1 + A2)
sec("B", CB1 + CB2, B1 + B2)
sec("pool", CPOOL, POOL)
sec("rapid", CA1 + CA2, A1 + A2)
sec("peak", CB1 + CB2, B1 + B2, shift=2)
sec("coda", CCODA, CODA)
NB = len(plan)
chords = [p["ch"] for p in plan]
S = Song(4, 4, NB, BDOR); S.check(A1, A2, B1, B2, POOL); S.G = 0.08

# ---------------- 和音 ----------------
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(s): return (PCN[s[0]] + (1 if len(s) > 1 and s[1] == "#" else -1 if len(s) > 1 and s[1] == "b" else 0)) % 12
def chord_pcs(ch):
    m = re.match(r"^([A-G][#b]?)(.*)$", ch.split("/")[0]); r = pc(m.group(1)); q = m.group(2)
    if "sus4" in q: pcs = [r, (r + 5) % 12, (r + 7) % 12]
    elif "sus2" in q: pcs = [r, (r + 2) % 12, (r + 7) % 12]
    elif q.startswith("m") and not q.startswith("maj"): pcs = [r, (r + 3) % 12, (r + 7) % 12]
    else: pcs = [r, (r + 4) % 12, (r + 7) % 12]
    if "maj7" in q: pcs.append((r + 11) % 12)
    elif "7" in q: pcs.append((r + 10) % 12)
    return pcs
def bass_pc(ch): return pc(ch.split("/")[1]) if "/" in ch else chord_pcs(ch)[0]
def low(x, lo): return lo + ((x - lo) % 12)
def step(m, k, sc):
    d = 1 if k > 0 else -1
    for _ in range(abs(k)):
        m += d
        while m % 12 not in sc: m += d
    return m
def tones_in(pcs, lo, hi): return [m for m in range(lo, hi + 1) if m % 12 in pcs]

# ---------------- パート（チャンネル: 笛・フィドル・アコーディオン・鉄琴・ハープ・ピアノ・チェロ・コントラバス・弦上・弦下・パッド・ホルン・大太鼓＝13）----------------
S.part("flute", "panflute", "笛（ロー・ホイッスル風の旋律）", 0.21, 0.12, reverb=0.42, gainDb=2, breath=True,
       fx=[{"type": "delay", "beats": 0.75, "mix": 0.14, "feedback": 0.3}, {"type": "plate", "mix": 0.12}])
S.part("fiddle", "fiddle", "フィドル（旋律・急流の駆け回り）", 0.19, -0.18, patch="violin", reverb=0.38, gainDb=1, fx=[{"type": "plate", "mix": 0.14}])
S.part("acc", "accordion", "アコーディオン（和音をのばす）", 0.1, 0.3, reverb=0.3, fx=[{"type": "room", "mix": 0.12}])
S.part("glock", "glockenspiel", "鉄琴（しずく）", 0.07, 0.45, reverb=0.45, sustain=4, release=0.8,
       fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.4}])
S.part("harp", "harp", "ハープ（流れ落ちる16分）", 0.11, -0.35, reverb=0.4, bright=-0.4, sustain=3, release=0.8,
       fx=[{"type": "pingpong", "beats": 0.5, "mix": 0.1, "feedback": 0.2}])
for _k in ("pno1", "pno2", "pno3"):
    S.part(_k, "piano", f"ピアノ右手（和音・{_k[3]}）", 0.09, 0.08, reverb=0.32, sustain=1.6, fx=[{"type": "plate", "mix": 0.16}])
S.part("pnoL", "piano", "ピアノ左手（低音の転がし）", 0.12, 0.08, reverb=0.32, sustain=1.4, fx=[{"type": "plate", "mix": 0.16}])
for _k, _pan in (("g1", -0.5), ("g2", 0.5), ("g3", -0.5), ("g4", 0.5)):   # アコギ（B・急流・山場の刻み）
    S.part(_k, "guitar", f"アコギ（{_k[1]}本目）", 0.08, _pan, amp="crystal", chorus=0, sustain=1.0, reverb=0.24, autoScoop=False, humanPitch=0, push=0.008 * int(_k[1]),
           fx=[{"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.01, "release": 0.12}])
S.part("cello", "strings", "チェロ", 0.13, -0.3, patch="cello", reverb=0.36, release=0.5,
       fx=[{"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.01, "release": 0.15}])
S.part("cb", "strings", "コントラバス", 0.14, 0, patch="contrabass", reverb=0.3)
S.part("sth", "strings", "弦（上・のばす）", 0.07, 0.55, patch="slowStrings", reverb=0.42, release=0.6)
S.part("stl", "strings", "弦（下・のばす）", 0.07, -0.55, patch="slowStrings", reverb=0.42, release=0.6)
S.part("pad", "pad", "パッド（霧）", 0.07, 0, patch="warmPad", reverb=0.5, sustain=2, fx=[{"type": "chorus", "mix": 0.2}])
S.part("horn", "brass", "ホルン（山場の長い音）", 0.12, -0.1, patch="horn", reverb=0.38, breath=True, release=0.5, fx=[{"type": "reverb", "mix": 0.15}])
S.part("big", "inchTom", "大太鼓（滝の響き）", 0.13, 0, patch="inchTom", reverb=0.15, gainDb=-9)
S.part("bodhran", "tom", "ボーラン風の刻み", 0.12, 0.1, reverb=0, gainDb=-8, bright=-0.4)
S.part("kick", "kick", "キック", 0.26, 0, gainDb=-8)
S.part("snare", "snare", "スネア", 0.17, 0, push=0.01, gainDb=-10)
S.part("ride", "crash", "ライド", 0.05, 0.2, gainDb=-9)
S.part("crash", "crash", "クラッシュ", 0.09, 0, gainDb=-8)

GAIN = {"mist": (0.6, 0.72), "A": (0.74, 0.84), "B": (0.84, 0.94), "pool": (0.72, 0.82), "rapid": (0.92, 1.0), "peak": (1.0, 1.05), "coda": (0.8, 0.6)}
LEN = {}
for p in plan: LEN[p["k"]] = LEN.get(p["k"], 0) + 1
arc = []
BOD = {"X": "A2!", "x": "C3", "o": "C3,,"}
BIG = {"X": "E2!", "x": "A2", "o": "C3,"}

for bi, p in enumerate(plan):
    k, i, ch, mel, sh = p["k"], p["i"], p["ch"], p["mel"], p["shift"]
    a, z = GAIN[k]; arc.append(round(a + (z - a) * i / max(1, LEN[k] - 1), 3))
    sc = scale_of(p["orig"], sh); S.scale = sc
    pcs = chord_pcs(ch); br = bass_pc(ch)
    # ---- 旋律 ----
    if k == "A": S.put("flute", bi, S.ornament(S.seq(mel), "cut", bi, dens=0.35, legato=True))
    if k == "B": S.put("fiddle", bi, S.ornament(S.seq(mel), "roll", bi, dens=0.4, legato=True))
    if k == "pool" and mel: S.put("flute", bi, S.ornament(S.seq(mel), "cut", bi, dens=0.25, legato=True))
    if k == "rapid":
        S.put("flute", bi, S.ornament(S.seq(mel), "cut", bi + 5, dens=0.45, legato=True))
        # フィドルの急流: 前半は和音の高い音から音階を16分で駆け下り、後半は和音を駆け上がる
        top = max(tones_in(pcs, 76, 86)); run = [top]
        for _ in range(7): run.append(step(run[-1], -1, sc))
        ups = tones_in(pcs, 59, 100)[:8]
        S.put("fiddle", bi, [f"{nm(m)}:0.25" + ("" if j % 4 == 0 else ",") + ("_" if j < 15 else "") for j, m in enumerate(run + ups)])
    if k == "peak":
        S.put("fiddle", bi, S.ornament(S.seq(mel), "roll", bi, dens=0.45, legato=True))
        S.put("flute", bi, S.plain(S.seq(" ".join(x if x.startswith("R:") else f"{nm(md(x.split(':')[0]) - 12)}:{x.split(':')[1]}" for x in mel.split())), legato=True))
        S.put("horn", bi, [f"{nm(low(pcs[2], 55))}:4"] if i % 2 == 0 else [f"{nm(low(pcs[1], 55))}:4"])
    if k == "coda" and mel and mel != "R:16": S.put("flute", bi, S.ornament(S.seq(mel), "cut", bi, dens=0.25, legato=True))
    # ---- 鉄琴（しずく）: 霧・滝つぼ・終わり、A の偶数小節 ----
    if k in ("mist", "pool", "coda") or (k == "A" and i % 2 == 1):
        hi = tones_in(pcs, 84, 100)
        t1, t2 = hi[(bi * 3) % len(hi)], hi[(bi * 5 + 2) % len(hi)]
        S.put("glock", bi, ["R:1", f"{nm(t1)}:1.5", f"{nm(t2)}:1.5"] if bi % 2 == 0 else [f"R:0.5", f"{nm(t2)}:2", f"{nm(t1)}:1.5"])
    if k == "peak" and i % 4 == 0: S.put("glock", bi, [f"{nm(x)}:1" for x in tones_in(pcs, 86, 100)[-4:][::-1]])
    # ---- ハープ（流れ落ちる16分。1小節に2回、和音の音を高い所から低い所へ）----
    if k != "pool" or i >= 4:
        fall = sorted(tones_in(pcs, 50, 88), reverse=True)[:8]
        if k == "coda" and i == 7: S.put("harp", bi, [f"{nm(m)}:0.25" for m in sorted(tones_in(pcs, 59, 90))[:8]] + [f"{nm(sorted(tones_in(pcs, 59, 90))[8])}:2"])
        elif k == "coda" and i == 6: S.put("harp", bi, [f"{nm(m)}:0.5" for m in fall])
        else: S.put("harp", bi, [f"{nm(m)}:0.25" + ("" if j % 8 == 0 else ",") for j, m in enumerate(fall + fall)])
    # ---- ピアノ（左手と右手）----
    pv = sorted(low(x, 59) for x in pcs[:3]); lr = low(br, 40)
    if k in ("A", "B", "rapid", "peak"):
        for vi, g in enumerate(("pno1", "pno2", "pno3")):
            S.put(g, bi, [f"{nm(pv[vi])}:2", f"{nm(pv[vi])}:2,"] if k in ("A", "B") else [f"{nm(pv[vi])}:1.5!", f"{nm(pv[vi])}:1,", f"{nm(pv[vi])}:1.5"])
        fifth = lr + ((pcs[2] - br) % 12)
        S.put("pnoL", bi, [f"{nm(x)}:0.5" + ("!" if j == 0 else ("," if j % 2 else "")) for j, x in enumerate((lr, fifth, lr + 12, fifth + 12 if fifth + 12 < 60 else fifth, lr + 12, fifth, lr + 12, fifth))])
    if k in ("pool", "coda") or (k == "mist" and i >= 2):
        for vi, g in enumerate(("pno1", "pno2", "pno3")): S.put(g, bi, [f"{nm(pv[vi])}:4,"])
        S.put("pnoL", bi, [f"{nm(lr)}:4,"])
    # ---- アコギ（低い2本はのばし、高い2本は8分で「ダウン・ダウン・アップ」）----
    if k in ("B", "rapid", "peak") or (k == "A" and i >= 8):
        g0 = low(pcs[0], 45)
        v = [low(br, 40), g0 + ((pcs[2] - pcs[0]) % 12), g0 + 12, g0 + 12 + ((pcs[1] - pcs[0]) % 12)]
        for gi, g in enumerate(("g1", "g2", "g3", "g4")):
            if gi < 2 or k == "A": S.put(g, bi, [f"{nm(v[gi])}:4" + ("!" if gi < 2 else ",")]); continue
            n0 = nm(v[gi])
            S.put(g, bi, [f"{n0}:1!", f"{n0}:0.5,", f"{n0}:1", f"{n0}:0.5,", f"{n0}:0.5", f"{n0}:0.5,"])
    # ---- アコーディオン ----
    if k == "B" or k == "pool" or k == "peak": S.put("acc", bi, [f"{nm(low(pcs[1], 57))}:4"])
    # ---- 低音 ----
    if k in ("mist", "A", "pool", "coda", "B"):
        S.put("cello", bi, [f"{nm(low(br, 43) + 12 if k == 'B' else low(br, 43))}:4"])
        if k != "A" or i >= 8: S.put("cb", bi, [f"{nm(low(br, 31))}:4"])
    if k in ("rapid", "peak"):
        r3 = low(br, 43)
        S.put("cello", bi, [f"{nm(r3)}:0.5" + ("!" if j % 4 == 0 else ",") for j in range(8)])
        S.put("cb", bi, [f"{nm(low(br, 31))}:4"])
    # ---- 弦・パッド ----
    if k in ("B", "rapid", "peak") or (k == "coda" and i < 4) or (k == "A" and i >= 12):
        S.put("sth", bi, [f"{nm(low(pcs[1], 66))}:4"]); S.put("stl", bi, [f"{nm(low(pcs[2], 57))}:4"])
    if k in ("mist", "pool", "coda") or (k == "A" and i < 8):
        S.put("pad", bi, [f"{nm(low(pcs[0], 50))}:4"])
    # ---- 打楽器 ----
    if k == "A" and i >= 8: S.put("bodhran", bi, S.pgrid("X.......x...o..." if i % 4 != 3 else "X.......x.o.xoxx", BOD))
    if k == "B":
        S.put("bodhran", bi, S.pgrid("X..ox...x..ox.o." if i % 4 != 3 else "X..ox...xoxoXxXx", BOD))
        if i % 2 == 0: S.put("kick", bi, S.grid("X..............."))
        if i == 8: S.put("crash", bi, S.grid("x..............."))
    if k == "pool" and i >= 6: S.put("big", bi, S.pgrid("o...o...o.o.oooo" if i == 6 else "o.o.oooxxxxxXXXX", BIG))
    if k in ("rapid", "peak"):
        last4 = i % 4 == 3
        S.put("bodhran", bi, S.pgrid("X.ox.xo.X.ox.xox" if not last4 else "X.ox.xo.X.ox....", BOD))
        S.put("kick", bi, S.grid("X.....x...X....." if not last4 else "X.....x...X.X.X."))
        S.put("snare", bi, S.grid("....X.......X..." if not last4 else "....X.......XxXX"))
        if not last4: S.put("ride", bi, ["D2:0.5"] * 8)
        if i % 8 == 0: S.put("crash", bi, S.grid("X..............."))
        if k == "peak" and i % 2 == 0: S.put("big", bi, S.pgrid("X.......x.......", BIG))
        if k == "rapid" and i % 8 == 7: S.put("big", bi, S.pgrid("........X.x.XxXx", BIG))
    if k == "coda" and i == 0: S.put("crash", bi, S.grid("x..............."))
    if k == "coda" and i == 7: S.put("big", bi, S.pgrid("o...............", BIG))

out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-waterfall.json"
S.dump(out, "霧ふる滝の祈り（仮）",
       "（仮）滝の流れを感じる、神秘的なケルト音楽。4/4・BPM78・ロ短調のドリアン、山場は全音上、約4分25秒。"
       "ハープが和音の音を16分で流れ落ち、鉄琴のしずくにピンポンディレイ。霧 → 笛の主題 → フィドルが高く歌う → 滝つぼ（静か）→ "
       "急流（フィドルが16分で駆け回り、ボーラン・ライド・大太鼓）→ 全音上の山場（ホルン・全員）→ 霧に戻り Bsus2 で解決せずに消える。"
       "ピアノは左手の8分の転がしと右手の和音。FX: 笛のディレイ、鉄琴とハープのピンポンディレイ、パッドのコーラス、フィドルのプレート、チェロのコンプ。"
       "進行: ドリアンの IV（E/G#）、ナポリの C、C/G のゆらぎ、F#7sus4、Bsus2。入り方: 5（パッドと低い弦の持続の上に、しずくと流れ）。終わり方: 余韻を残して消える。",
       78, chords, arc, extra={"guitarWobble": False})

# ---- 仕上げ: のばす楽器の同じ高さの弾き直しをつなぐ（弾き直すと音が切れてプチッと鳴る）----
def _merge(notes, legato):
    out_ = []
    for t in notes.split():
        n_, d = t.split(":", 1); mark = "".join(c for c in d if not (c.isdigit() or c == ".")); dv = float(d[:len(d) - len(mark)])
        if out_ and n_ != "R" and out_[-1][0] == n_ and dv >= 1 and out_[-1][1] >= 1 and "!" not in mark:
            out_[-1][1] += dv; out_[-1][2] = out_[-1][2].replace("_", ""); continue
        out_.append([n_, dv, mark.replace("_", "") if legato else mark])
    res = []
    for j, (n_, dv, mark) in enumerate(out_):
        nxt = out_[j + 1][0] if j + 1 < len(out_) else "R"
        lg = "_" if legato and n_ != "R" and nxt not in ("R", n_) and dv >= 1 else ""
        res.append(f"{n_}:{fmt(dv)}{mark}{lg}")
    return " ".join(res)
_song = json.load(open(out, encoding="utf-8"))
for _p in _song["parts"]:
    r = _p["role"]
    if r.startswith(("弦（", "チェロ", "コントラバス", "アコーディオン", "パッド", "ホルン")):
        _p["notes"] = _merge(_p["notes"], legato=r.startswith(("弦（", "パッド")))
json.dump(_song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
