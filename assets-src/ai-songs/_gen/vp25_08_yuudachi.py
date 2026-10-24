# vp25 08「夕立とスニーカー」Sneakers in a Summer Shower（仮）— ダンス（UKガラージ／2ステップ）。A♭長調・132・4/4。主役の楽器: カリンバ
# 物語: 夏の夕方、新しいスニーカーで走っていたら、急に夕立。駄菓子屋の軒先で雨宿り。雨粒を数えながら待つうちに小降りになり、
#   雲が切れて虹が出る。水たまりを跳びこえて、虹の下を走り出す。
# 形: 走る→雨が降り出す→雨宿り（やむのを待つ）→小降り→虹の下を走り出す
# 場面と強さ: 走る＝跳ねる中くらい／雨宿り＝雨音だけの静けさ（ドラムなし。雨が強まって、また弱まる）／虹＝最大／虹の向こう＝フェードアウト
# 旋律の性格: はねる付点と休符の多い短い句（2ステップの跳ねに合わせる）。雨宿りでは長く下る旋律
# 崩す所: 雨宿りの間（約1分）、2ステップの命のリズム（ドラム）を止める
from vp25_lib import *

S = Song("08", "yuudachi", "夕立とスニーカー（仮）", "Sneakers in a Summer Shower", 132, 4, "Ab", "major", "ダンス（2ステップ）")
K = S.key
RUN = ["Dbmaj7", "Cm7", "Bbm7", "Eb7sus4"]
RAIN = ["Fm7", "Dbmaj7", "Bbm9", "C7"]
SHELTER = ["Fm9", "Dbmaj7", "Gb", "Fm9", "Db", "Bbm7", "Eb7sus4", "Eb7"]
RAINBOW = ["Abmaj7", "Eb/G", "Fm7", "Ab7", "Dbmaj7", "Eb", "Cm7", "F7"]
S.scene("走る", 32, "verse", RUN)
S.scene("降り出す", 8, "pre", RAIN)
S.scene("雨宿り", 40, "bridge", SHELTER)
S.scene("小降り", 8, "pre", ["Bbm7", "Cm7", "Dbmaj7", "Eb7sus4"])
S.scene("虹", 32, "chorus", RAINBOW)
S.scene("虹の向こう", 16, "outro", ["Abmaj7", "Dbmaj7"] * 8)
S.extra["swing16"] = 0.22

KA = S.track("主役: カリンバ", "kalimba", volume=0.25, pan=-0.1, reverb=0.32, sustain=1.6, gainDb=5,
             fx=[{"type": "eq", "low": -3, "mid": 2.5, "midHz": 2200, "high": 1}, {"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("calliope", vol=0.19, pan=0.05, delay=0.75))
DROP = S.track("雨粒", "pad", patch="glassPluck", volume=0.07, pan=0.5, sustain=0.6, reverb=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 800, "q": 0.7}, {"type": "pingpong", "beats": 0.5, "mix": 0.3, "feedback": 0.35}])
DROP2 = S.track("雨粒（左）", "pad", patch="glassPluck", volume=0.06, pan=-0.55, sustain=0.6, reverb=0.5,
                fx=[{"type": "filter", "kind": "highpass", "freq": 900, "q": 0.7}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.22, duck=0.25))
SUB = S.track("808（重低音）", "sub808", **sub_spec(0.18))
EP = [S.track(f"エレピの和音{i + 1}", "fmEpiano", volume=0.09, pan=[-0.4, 0.4, 0, 0.15][i], reverb=0.2, sustain=0.8) for i in range(4)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.55, 0.55, 0][i], duck=0.25)) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 歌の役: はねる付点と休符の多い短い句 ----------
RA = ["R:0.5 5:0.75 6:0.25 R:0.5 1':0.75 6:0.25 5:1", "R:0.5 3:0.75 5:0.25 R:0.5 4:1 3:0.5 R:0.5", "R:0.5 2:0.75 4:0.25 R:0.5 6:0.75 5:0.25 4:1", "5:1.5 R:2.5",
      "R:0.5 5:0.75 6:0.25 R:0.5 2':0.75 1':0.25 6:1", "R:0.5 5:0.75 3:0.25 R:0.5 2:1 3:0.5 R:0.5", "R:0.5 4:0.75 6:0.25 1':0.5 b7:0.75 6:0.25 5:1", "5:1 4:0.5 2:0.5 R:2"]
RA2 = ["R:0.5 1':0.75 2':0.25 R:0.5 3':0.75 2':0.25 1':1", "R:0.5 7:0.75 1':0.25 R:0.5 2':1 7:0.5 R:0.5", "R:0.5 6:0.75 1':0.25 R:0.5 2':0.75 1':0.25 6:1", "5:2 R:2",
       "R:0.5 3':0.75 2':0.25 R:0.5 1':0.75 6:0.25 5:1", "R:0.5 6:0.75 5:0.25 R:0.5 3:1 2:0.5 R:0.5", "R:0.5 4:0.75 5:0.25 6:0.5 1':0.75 2':0.25 b7:1", "5:3 R:1"]
for i, b in enumerate(S.sc("走る")):
    if i < 8: continue
    LEAD.bar(b, K.mel((RA if i < 16 else RA2 if i < 24 else RA)[i % 8], oct=4))
# 降り出す: 句が下へ（雨が落ちる）
for i, b in enumerate(S.sc("降り出す")):
    LEAD.bar(b, K.mel(["6:1 5:1 3:1 2:1", "1:2 R:2", "4:1 3:1 1:1 6,:1", "#5,:2 R:2"][i % 4], oct=5 if i < 4 else 4))
# 雨宿り: 長く下る旋律（リードは前半だけ、後半はカリンバが受けつぐ）
SH = ["5':4", "4':2 3':2", "b3':3 2':1", "1':4", "1':4", "7:2 6:2", "5:2 4:2", "5:4"]
for i, b in enumerate(S.sc("雨宿り")):
    if 8 <= i < 24: LEAD.bar(b, K.mel(SH[i % 8], oct=4))
# 虹: 走るの句を高く、はねる
RB = ["R:0.5 1':0.75 2':0.25 R:0.5 3':1 5':1", "R:0.5 5':0.75 4':0.25 R:0.5 3':1 2':1", "R:0.5 1':0.75 2':0.25 R:0.5 4':1 3':1", "1':2 R:1 b7:0.5 1':0.5",
      "R:0.5 2':0.75 3':0.25 R:0.5 4':1 6':1", "5':2 R:0.5 3':0.75 2':0.25", "R:0.5 1':0.75 7:0.25 R:0.5 6:1 1':1", "#4':2 R:2"]
for i, b in enumerate(S.sc("虹")):
    LEAD.bar(b, K.mel(RB[i % 8] if i < 24 else seq_up(RB[i % 8], K, 0), oct=4))
for i, b in enumerate(S.sc("虹の向こう")):
    if i < 8: LEAD.bar(b, K.mel(["3':4", "2':4", "1':4", "R:4", "5:4", "6:4", "5:4", "R:4"][i], oct=4))

# ---------- カリンバ: 走る（分散和音）・雨宿り（主役の旋律）・虹（合いの手） ----------
def kal_arp(b, pat):
    t = tones(S.chords[b], "Ab4", "Ab6")
    return " ".join(f"{nm(t[q % len(t)], True)}:0.5" if q >= 0 else "R:0.5" for q in pat)


for i, b in enumerate(S.sc("走る")):
    KA.bar(b, kal_arp(b, [0, 2, 4, 2, 1, 3, 5, 3] if i % 2 == 0 else [4, 2, 0, -1, 1, 3, 4, -1]))
for i, b in enumerate(S.sc("降り出す")):
    KA.bar(b, kal_arp(b, [6, 5, 4, 3, 2, 1, 0, -1]))
# 雨宿りの旋律（カリンバが主役）: 雨粒を数えるような、ひと粒ずつの音から旋律に
KM = ["5:1 R:1 5:1 R:1", "3:1 R:1 2:1 R:1", "R:1 1:0.5 2:0.5 3:1 R:1", "5:3 R:1",
      "R:0.5 6:0.5 5:0.5 3:0.5 2:1 1:1", "R:0.5 2:0.5 3:0.5 5:0.5 6:2", "R:0.5 1':0.5 b7:0.5 5:0.5 4:1 2:1", "1:4",
      "5:0.5 6:0.5 1':1 6:0.5 5:0.5 3:1", "2:0.5 3:0.5 5:1 3:0.5 2:0.5 1:1", "R:0.5 4:0.5 6:0.5 1':0.5 2':1 1':1", "6:2 5:2",
      "1':0.5 2':0.5 3':1 2':0.5 1':0.5 6:1", "5:0.5 6:0.5 1':1 2':2", "R:0.5 3':0.5 2':0.5 1':0.5 6:1 5:1", "5:4"]
for i, b in enumerate(S.sc("雨宿り")):
    if i < 8: KA.bar(b, K.mel(KM[i], oct=5))
    elif i < 24: KA.bar(b, kal_arp(b, [0, -1, 2, -1, 4, -1, 2, -1]))
    else: KA.bar(b, K.mel(KM[8 + (i - 24) % 8], oct=5))
for i, b in enumerate(S.sc("小降り")): KA.bar(b, kal_arp(b, [0, 2, 4, 6, 4, 2, 1, 3]))
for i, b in enumerate(S.sc("虹")):
    # 歌の休む所（各小節の頭の半拍・4拍目）に合いの手
    t = tones(S.chords[b], "Ab5", "Ab6")
    KA.bar(b, f"{nm(t[0], True)}:0.25 {nm(t[1], True)}:0.25 R:2.5 {nm(t[2], True)}:0.5 {nm(t[1], True)}:0.5" if i % 2 == 0 else
           f"R:3 {nm(t[-1], True)}:0.5 {nm(t[-2], True)}:0.5")
for i, b in enumerate(S.sc("虹の向こう")): KA.bar(b, kal_arp(b, [0, 2, 4, 2, 1, 3, 5, 3]) if i < 12 else (kal_arp(b, [0, -1, -1, -1, 2, -1, -1, -1]) if i < 15 else "R:4"))

# ---------- 雨粒（雨宿りの間、強くなって弱くなる） ----------
rnd = random.Random(8)
for i, b in enumerate(S.sc("降り出す") + S.sc("雨宿り") + S.sc("小降り")):
    dens = min(1.0, 0.2 + i * 0.05) if i < 20 else max(0.1, 1.0 - (i - 20) * 0.03)
    t = tones(S.chords[b], "C6", "C8")
    for tr_, side in ((DROP, 0), (DROP2, 1)):
        toks = []
        for q in range(16):
            toks.append(f"{nm(rnd.choice(t), True)}:0.25" if rnd.random() < dens * 0.45 else "R:0.25")
        tr_.bar(b, merge_rests(" ".join(toks)))

# ---------- 低音 ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in ("走る", "虹", "小降り"):
        if n == "走る" and i < 4: continue
        BASS.bar(b, f"{nm(r)}:0.75! R:0.25 {nm(r)}:0.5 R:1 {nm(r + 12)}:0.5 {nm(r)}:0.5 R:0.25 {nm(r + 7)}:0.25")
        if n == "虹": SUB.bar(b, f"{nm(r)}:1.5 R:1 {nm(r)}:1 R:0.5")
    elif n == "降り出す": BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    elif n == "雨宿り": BASS.bar(b, f"{nm(r)}:4" if i % 2 == 0 or i >= 24 else "R:4")
    elif n == "虹の向こう" and i < 12: BASS.bar(b, f"{nm(r)}:0.75! R:0.25 {nm(r)}:0.5 R:2.5")

# ---------- 和音 ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 63, 4)
    if n in ("走る", "虹", "小降り"):
        pat = "R:0.5 X:0.75 R:0.75 X:0.5 R:1 X:0.5" if i % 2 == 0 else "R:0.5 X:0.25 R:0.25 X:0.5 R:1 X:0.75 R:0.75"
        for j in range(4): EP[j].bar(b, pat.replace("X", nm(v[j], True)))
    pv = voice(S.chords[b], 57, 3)
    if n in ("雨宿り", "降り出す", "虹の向こう") or (n == "虹" and i >= 16):
        for j in range(3): PAD[j].bar(b, f"{nm(pv[j], True)}:4")
riser(FX, S.sc("虹")[0], 8, "D4"); cym_swell(CYM, S.sc("虹")[0], 2, "C4")
cym_swell(CYM, S.sc("小降り")[0], 4, "E4")

# ---------- ドラム（2ステップ: キックは1拍目と2拍目の裏の裏、スネアは2・4、ハットははねる16分） ----------
GK = ["X.........X.....", "X.......X.x.....", "X.........X...x.", "X.......x.X....."]
GH = ["x.xox.xox.xox.xo", "x.x.xox.x.xox.x.", "..xo..xo..xo..xo", "x.xox.xox.xoxxxo"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("走る", "虹"):
        if n == "走る" and i < 2: D.set(b, h=GH[0]); continue
        put_groove(D, b, (GK[i % 4], "....X.......X...", GH[i % 4]), ghosts=0.6, seed=b, hat_vary=False)
        if n == "虹" and i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if n == "走る" and i == 8: crash(D, b, "A2", 2)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "tomdown")
        continue
    if n == "降り出す":
        put_groove(D, b, ("X...............", "....X.......X...", "x.x.x.x.x.x.x.x."), seed=b, hat_vary=False)
        if last: D.set(b, "X" + "." * 15, "." * 16, "." * 16)
        continue
    if n == "小降り":
        D.set(b, "." * 16, "." * 16, GH[2] if i < 4 else GH[0])
        if last: put_fill(D, b, "build")
        continue
    if n == "虹の向こう":
        if i < 12: put_groove(D, b, (GK[0], "....X.......X..." if i < 8 else "." * 16, GH[2]), seed=b, hat_vary=False)

S.fade_out = 14
S.flags += " --space room --space-wet 0.12"
S.desc = ("仮: ボカロ曲のインスト25曲の08。UKガラージ（2ステップ）。A♭長調・132。主役の楽器はカリンバ。夏の夕立。"
          "新しいスニーカーで走る（はねる2ステップ）→降り出す→軒先の雨宿り（約1分、ドラムなし。雨粒が強まって弱まり、カリンバが雨粒を数える旋律）→小降り→虹の下を走り出す（最大）→フェードアウト。自作")
S.write()
