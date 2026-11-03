# vt25 06「トーキョー・カラーパレット」Tokyo Color Palette（仮）— K-POP（アフロビーツ・ポップ）。108・4/4。F# の短調（サビは A の明るい所）→ 最後のサビは +1。
#   （表では K-POP ダンスポップ 126 だったが、第1弾の 22「7色シグナル」（K-POP ダンスポップ 124・色の話）と似るので、
#     アフロビーツのリズム（3・3・2 で揺れる打楽器、ハイライフふうのギター）にした）
# 物語: 地方から東京へ出てきた春。駅の出口で迷子になる。ネオンの色がまぶしすぎて、ふるさとの空の緑と青しか知らない「わたし」は、
#   ここが何色なのか分からない。服を変えても、髪を染めても、鏡の中のわたしは誰？ ワンルームの夜、目を閉じると、自分の色が見えた。
#   パレットのすみっこでもいい。まざった色も嫌いじゃない。わたしはわたし。
# 場面と強さ: 短いサビから（いきなり「カラーパレットの」）→ Aメロ1（迷子・語る・中）→ Bメロ1 → サビ1（赤・マリンバの色・強）→ 間奏
#   → Aメロ2 → Bメロ2 → サビ2（青・ガラスのプラック・ハーフの重さ）→ ワンルームの夜（とても弱い）→ 最後のサビ（+1・金・ブラスが加わる）
#   → 1色だけ残る和音
# 旋律の性格: 短いフックのくり返し（「カラーパレットの」の6音がサビの頭に毎回）。Aメロは低め（C#4〜A4）で語り、サビで C#5〜E5 まで。
# ほかの曲とちがう所（この曲だけの音）: サビごとに、旋律の合いの手の音色が「色」を変える（サビ1 マリンバ → サビ2 ガラスのプラック → 最後 ブラス）。
#   3・3・2 で揺れるアフロビーツの打楽器と、ハイライフふうのギターのつまびき。
from vt25_lib import *

S = Song("06", "colorpalette", "トーキョー・カラーパレット（仮）", "Tokyo Color Palette", 108, 4, "F#", "minor", "K-POP（アフロビーツ・ポップ・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.15"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.5
K = Key("F#", "minor")          # oct 3 で 1 = F#3。歌うのは C#4〜E5
KL = Key("G", "minor")          # 最後のサビ（+1）

A_CH = ["F#m7", "Dmaj7", "Bm7", "C#m7"]
B_CH = ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "C#m7", "Dmaj7", "E"]
C_CH = ["Dmaj7", "E", "C#m7", "Bm7", "Dmaj7", "E", "C#m7", "F#m7"]
C_CH2 = C_CH[:7] + ["A"]
X_CH = ["Bm7", "C#m7", "Dmaj7", "E", "Bm7", "C#m7", "Dmaj7", "Esus4"]
LAST = [tr_chord(c, 1) for c in C_CH + C_CH2]

S.scene("短いサビ", 8, "intro", C_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("間奏", 4, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH + C_CH2)
S.scene("ワンルームの夜", 8, "bridge", X_CH[:7] + ["F7"])          # 最後の小節は +1 への入り口
S.scene("最後のサビ", 16, "chorus", LAST)
S.scene("1色だけ", 4, "outro", ["Ebmaj7", "F", "Bbmaj9", "Bbmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="voiceLeadModern", low=True)
GTR = S.track("ギター（ハイライフのつまびき）", "guitar", amp="jpopClean", volume=0.1, pan=0.35, reverb=0.25, chorus=0, sustain=0.6)
GTR2 = S.track("ギター（和音のミュートなしの刻み）", "guitar", amp="jpopClean", volume=0.07, pan=-0.4, reverb=0.25, chorus=0, sustain=0.5)
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.21))
LOG = S.track("ログドラム（音程のある低い太鼓）", "rotoTom", patch="rotoTom", volume=0.13, pan=0.0, reverb=0.15)
PERC = S.track("打楽器（カホン）", "cajon", volume=0.09, pan=-0.25, reverb=0.12)
SHK = S.track("打楽器（フレームドラム）", "guitar", patch="frameDrum", volume=0.12, pan=0.3, reverb=0.15, gainDb=10)
MAR = S.track("色1 マリンバ（サビ1の合いの手）", "strings", patch="marimba", volume=0.12, pan=-0.3, reverb=0.25)
GLS = S.track("色2 ガラスのプラック（サビ2の合いの手）", "pad", patch="glassPluck", volume=0.07, pan=0.3, reverb=0.35, sustain=1.0)
BRS = [S.track(f"色3 ブラス（最後のサビ）{i + 1}", "brass", patch="brassSection", volume=0.06, pan=-0.25 + 0.25 * i, reverb=0.3, sustain=0.8) for i in range(3)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("surgePadBright", vol=0.035, pan=-0.35 + 0.35 * i, duck=0.35, sustain=1.4)) for i in range(3)]
GLK = S.track("グロッケン（ネオン）", "glockenspiel", patch="glockenspiel", volume=0.05, pan=0.45, reverb=0.4)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.5 1':0.5 1':0.5 3':0.5 1':0.5 7:1", "1':1.5 R:2.5", "R:0.5 5:0.5 1':0.5 1':0.5 4':0.5 3':0.5 2':1", "1':1.5 R:2.5"]
A1 = "えきのでぐちで/まいごになるの/ねおんのいろが/まぶしすぎるよ/ふるさとのそら/みどりとあおで/ここはなんいろ/わからないんだ"
A2 = "ふくをかえても/かみをそめても/かがみのなかの/わたしはだあれ"
VB = ["R:0.5 3':0.5 3':0.5 2':0.5 1':1 3':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 3':0.5 3':0.5 4':0.5 5':1 4':1", "3':1.5 2':0.5 1':1 R:1",
      "R:0.5 4':0.5 4':0.5 5':0.5 6':1 5':1", "4':1.5 3':0.5 2':1 R:1", "R:0.5 3':0.5 4':0.5 5':0.5 6':1 7':1", "5':2 R:2"]
B1 = "このまちのいろを/ぜんぶまぜたらね/どんないろになる/おしえてよね"
B2 = "まどからみえるの/とうきょうたわーの/あかいひかりがね/またたいてる"
VC = ["R:0.5 3':0.5 5':0.5 6':0.5 7':1 6':1", "5':1 4':1 R:2", "R:0.5 3':0.5 5':0.5 6':0.5 7':1 5':1", "6':1 5':1 3':1 R:1",
      "R:0.5 3':0.5 5':0.5 6':0.5 7':1 6':1", "5':1 4':1 R:2", "R:0.5 2':0.5 3':0.5 4':0.5 5':1 4':1", "3':2 R:2"]
C0 = "からーぱれっとの/まんなかにたつよ/どのいろよりも/あかくなれる"
C1 = C0 + "/からーぱれっとの/ちいさくてもいい/わたしのいろで/ぬりたいんだ"
C2 = "からーぱれっとの/あおいところにね/ふるさとのそら/とけていくよ/からーぱれっとの/まざりあういろも/きらいじゃないよ/すきになれた"
CL = "からーぱれっとの/まんなかにたつよ/わたしのいろを/みつけたんだ/からーぱれっとの/どこにいてもいい/わたしはわたし/それでいいの"
VX = ["R:1 1':1 2':1 3':1", "5':2 4':2", "R:1 3':1 4':1 5':1", "6':3 R:1", "R:1 1':1 2':1 3':1", "5':2 4':2", "R:1 3':1 5':1 7':1", "6':4"]
X1 = "わんるーむ/しずかだ/めをとじる/みえるよ"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("短いサビ", K, VC, C0)
put("Aメロ1", K, VA * 4, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC + VC, C1); put("サビ2", K, VC + VC, C2)
put("ワンルームの夜", K, VX, X1)
put("最後のサビ", KL, VC + VC, CL)
if VOCAL: put("Aメロ2", K, VA * 2, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA * 2)): MAR.bar(b, K.mel(l, oct=4))

# ================= ギター（ハイライフのつまびき: 3・3・2 の位置に、和音の上の音を細かく） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; t = tones(ch, "E4", "E6"); v = voice(ch, 64, 3)
    if n in ("ワンルームの夜",):
        if i % 2 == 0: GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3)) + " R:2")
        continue
    if n == "1色だけ":
        if i == 2: GTR.bar(b, " ".join(f"{nm(x)}:0.25" for x in t[:4]) + f" {nm(t[4 % len(t)])}:7")
        continue
    GTR.bar(b, f"{nm(t[2])}:0.25 {nm(t[1])}:0.25 R:0.25 {nm(t[3])}:0.25 {nm(t[2])}:0.25 R:0.25 {nm(t[4 % len(t)])}:0.5 "
               f"{nm(t[2])}:0.25 {nm(t[1])}:0.25 R:0.25 {nm(t[3])}:0.25 {nm(t[2])}:0.5 {nm(t[0])}:0.5")
    if n not in ("Aメロ1",) or i >= 8:
        for j in range(3): pass
        GTR2.bar(b, " ".join(f"R:0.5 {nm(v[1])}:0.25 R:0.25" for _ in range(4)))

# ================= ベースとログドラム（3・3・2） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "ワンルームの夜":
        if i % 2 == 0: BASS.bar(b, f"{nm(r)}:4")
        continue
    if n == "1色だけ":
        if i < 3: BASS.bar(b, f"{nm(r)}:4")
        continue
    BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:1.5 {nm(r + 7)}:1" if n != "サビ2" else f"{nm(r)}:3 {nm(r + 7)}:1")
    lg = low(ch, "F2")
    LOG.bar(b, f"{nm(lg)}:0.75 R:0.75 {nm(lg)}:0.5 {nm(lg + 5 if lg + 5 <= 60 else lg)}:0.5 R:0.5 {nm(lg)}:0.5 {nm(lg + 7 if lg + 7 <= 60 else lg)}:0.5"
          if n.startswith(("サビ", "最後", "短い")) else f"{nm(lg)}:1.5 {nm(lg)}:1.5 R:1")

# ================= 打楽器（カホンとフレームドラムで 3・3・2） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("ワンルームの夜", "1色だけ"): continue
    PERC.bar(b, "R:0.75 E3:0.25, R:0.5 E3:0.25! R:0.5 E3:0.25, R:0.5 E3:0.25 R:0.25 E3:0.25! R:0.25")
    SHK.bar(b, " ".join(f"C3:0.25{'!' if q in (0, 6, 12) else ','}" for q in range(16)))

# ================= 色の合いの手（サビごとに音色が変わる）・パッド・グロッケン =================
FILL = ["R:2 C#6:0.25 E6:0.25 F#6:0.5 A6:0.5 F#6:0.5", "R:2 B5:0.25 D6:0.25 E6:0.5 F#6:0.5 E6:0.5"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 62, 3)
    if n in ("サビ1", "短いサビ"):
        if i % 2 == 1: MAR.bar(b, FILL[(i // 2) % 2])
    elif n == "サビ2":
        if i % 2 == 1: GLS.bar(b, FILL[(i // 2) % 2])
    elif n == "最後のサビ":
        bv = voice(ch, 67, 3)
        for j in range(3): BRS[j].bar(b, f"R:0.75 {nm(bv[j])}:0.25 R:0.5 {nm(bv[j])}:0.5 R:2" if i % 2 == 0 else f"R:2 {nm(bv[j])}:0.5 {nm(bv[j])}:0.5 R:1")
        if i % 2 == 1: MAR.bar(b, " ".join(f"{nm(midi(x.split(':')[0]) + 1)}:{x.split(':')[1]}" if not x.startswith("R") else x for x in FILL[(i // 2) % 2].split()))
    if n.startswith(("サビ", "最後", "短い")) or n.startswith("Bメロ") or n == "ワンルームの夜":
        for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")
    if n == "1色だけ":
        if i < 3:
            for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4" if i < 2 else f"{nm(v[j])}:8")
        if i == 3: GLK.bar(b, "D6:4")
    if n in ("Aメロ1", "Aメロ2") and i % 4 == 3:
        GLK.bar(b, "R:3 " + " ".join(f"{nm(x)}:0.25" for x in tones(ch, "C6", "C7")[:4]))

# ================= ドラム（アフロビーツ: キックは 3・3・2、スネアはリムのような軽い音） =================
AF_K = "X.....X...X....."; AF_S = "...o..X.....X..o"; AF_H = "x.xx.xx.x.xx.xx."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "短いサビ":
        vgroove(D, b, "four", ghosts=0.2, seed=b, k=AF_K, s=AF_S, h=AF_H, vary=False)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "four", ghosts=0.15, seed=b, k=AF_K, s="......X.......X." if i < 8 else AF_S, h=AF_H, vary=False)
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.25, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "最後のサビ"):
        vgroove(D, b, "four", ghosts=0.25, seed=b, k=AF_K, s=AF_S, h="xxxxxxxxxxxxxxxx", vary=False)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
    elif n == "サビ2":
        vgroove(D, b, "half", ghosts=0.2, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown")
    elif n == "間奏":
        vgroove(D, b, "four", ghosts=0.1, seed=b, k=AF_K, s="................", h=AF_H, vary=False)
    elif n == "ワンルームの夜":
        if i == 7: put_fill(D, b, "build")
    elif n == "1色だけ" and i < 2:
        vgroove(D, b, "four", ghosts=0.0, seed=b, k=AF_K, s=AF_S, h=AF_H, vary=False)
cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の06。K-POP（アフロビーツ・ポップ）。F# の短調（サビは A）・108、最後のサビは +1。"
          "地方から上京した子が、色の多すぎる街で自分の色を探す。短いサビから始まり、3・3・2 で揺れる打楽器とハイライフふうのギター、"
          "サビごとに合いの手の色が変わる（マリンバ → ガラスのプラック → ブラス）。ワンルームの夜の静けさ、1色だけ残る和音で終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.25}, special={"ワンルームの夜": -0.6, "最後のサビ": 0.5, "短いサビ": 0.1})
