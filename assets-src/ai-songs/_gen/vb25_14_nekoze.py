# vb25 14「猫背のパレード」Hunchback Parade（仮）— ヒップホップ（ブームバップ）。Dm（サビは平行調の F）・96（ハーフの型。ハットは倍で感じる）・4/4。転調なし
# 2026-10-25 作り直し: 物語を人の気持ちの話に（前は猫たちのパレード）、歌を人が歌える旋律（ラップのような8分と16分の2つ組）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を Fm から 3半音下げて Dm にした（書くのは Fm の度数のまま、書き出しの前に下げる）。
# 物語: うまくいかなかった日の帰り道。猫背でため息をこぼして歩いていると、となりの人も、うしろの人も猫背。なんだかおかしくなって、
#   知らない人とくすりと笑い合う。重いかばんはがんばりを詰めたから。カラスが鳴いても止まらない。月の下、同じ帰り道の猫背のパレード。
# 場面と強さ: 路地の入口（ベースだけ）→ 帰り道（Aメロ・ラップのように語る）→ 集まってくる（Bメロ・溜め・止め）→ 猫背のパレード（サビ）
#   → 塀の上（ブラスとスクラッチの間奏）→ 2番（BGM はエレピが歌を受け取る）→ Bメロ2 → サビ2（ハーフのトラップ寄り）→ カラス（止め・静けさ）
#   → 大合唱（最大）→ 夜明け前（フェードアウト）
# 旋律の性格: Aメロは低め（A3〜A4）で、8分と16分の2つ組で語る。サビは同じ音を3つ置いてから上がる「ねこぜのぱれーど」。最高音 D5。
# ほかの曲とちがう所: いちばんゆっくりで低い。生ドラムのブームバップ、エレピ、ブラス、スクラッチ。
from vb25_lib import *

S = Song("14", "nekoze", "猫背のパレード（仮）", "Hunchback Parade", 96, 4, "F", "minor", "ヒップホップ（ブームバップ・ボカロ）")
S.kit = "naked"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.keep_old_synth = True
S.no_depth = True
K = S.key                    # F の短調
KA = Key("Ab", "major")      # サビ（平行調）

A_CH = ["Fm9", "Dbmaj7", "Bbm7", "C7"]
B_CH = ["Dbmaj7", "Eb", "Cm7", "Fm7", "Dbmaj7", "Eb", "Edim7", "Fm7"]
C_CH = ["Dbmaj7", "C7", "Fm7", "Ab7", "Dbmaj7", "Gbmaj7", "C7sus4", "C7"]
C_CH2 = ["Dbmaj7", "C7", "Fm7", "Ab7", "Bbm7", "Gbmaj7", "Eb7sus4", "Eb7"]
LAST2 = ["Dbmaj7", "C7", "Fm7", "Ab7", "Bbm7", "Gbmaj7", "Ab/Eb", "Eb7"]
CROW = ["Bbm7", "C7", "Dbmaj7", "Edim7", "Fm7", "Gbmaj7", "C7sus4", "C7"]

S.scene("路地の入口", 8, "intro", A_CH)
S.scene("ぶらぶら", 16, "verse", A_CH)
S.scene("集まってくる", 8, "pre", B_CH)
S.scene("屋根へ", 16, "chorus", C_CH + C_CH2)
S.scene("塀の上", 4, "interlude", A_CH)
S.scene("2周目", 8, "verse", A_CH)
S.scene("集まってくる2", 8, "pre", B_CH)
S.scene("2回目の屋根", 16, "chorus", C_CH + C_CH2)
S.scene("カラス", 8, "bridge", CROW)
S.scene("屋根の上の大合唱", 16, "chorus", C_CH + LAST2)
S.scene("夜明け前", 6, "outro", ["Fm9", "Dbmaj7", "Bbm7", "C7sus4", "Fm9", "Fm9"])

V = Voice(S, vol=0.22, delay=0.75, patch="trumpet", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
EPS = dict(volume=0.11, pan=-0.25, reverb=0.25, sustain=0.9, fx=[{"type": "eq", "low": -3, "mid": -1.5, "midHz": 400, "high": 0.5}])
EP = [S.track(f"エレピの和音{i + 1}", "pad", patch="surgeKeysDxTonez", **EPS) for i in range(3)]
EPM = S.track("エレピ（歌の受け渡し）", "pad", patch="surgeKeysDxTonez", **EPS)
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.12, pan=0.3, reverb=0.25, gainDb=2,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1600, "high": 0}]) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.2))
SCR = S.track("スクラッチ風の音", "guitar", patch="guitarFx", volume=0.07, pan=0.15, reverb=0.1, modulate=False)
PAD = [S.track(f"月のパッド{i + 1}", "pad", **pad_spec("surgePadStringPad", vol=0.055, pan=-0.5, duck=0.25)) for i in range(2)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（F の短調の度数・oct 4 で 1 = F4。サビは A♭長調。書き出しの前に全体を 3半音下げる） =================
PA1 = ["R:0.5 1:0.5 1:0.25 1:0.25 3:0.5 1:0.5 7,:0.5 1:1", "3:0.5 4:0.5 3:1 R:2"]
PA2 = ["R:0.5 3:0.5 3:0.25 3:0.25 5:0.5 3:0.5 1:0.5 3:1", "4:0.5 3:0.5 1:1 R:2"]
PB1 = ["R:0.5 4:0.5 4:0.25 4:0.25 6:0.5 4:0.5 3:0.5 4:1", "5:0.5 #7,:0.5 5,:1 R:2"]
PB2 = ["R:0.5 6:0.5 6:0.25 6:0.25 4:0.5 6:0.5 5:0.5 4:1", "#7,:0.5 2:0.5 5:1 R:2"]
VA = PA1 + PB1 + PA2 + PB2 + PA1 + PB2 + PA2 + PB1
V1 = "ねこぜでかえるよみち/きょうもからぶりばかり/ためいきぐもをこぼす/かげぼうしながくなる/となりのひともねこぜ/うしろのひともねこぜ/なんだかほっぺがゆるむ/くすりとわらいあうよ"
V2 = "かばんがおもいのはね/がんばりつめたからだ/ねこぜでもいいじゃない/つきがみてるぼくらを"
VB = ["R:0.5 3:0.5 3:0.5 4:0.5 5:1 6:1", "5:1 4:1.5 R:1.5", "R:0.5 5:0.5 5:0.5 6:0.5 7:1 1':1", "1':1 5:1.5 R:1.5",
      "R:0.5 6:0.5 6:0.5 5:0.5 4:1 3:1", "4:1 5:1.5 R:1.5", "R:0.5 #7,:0.5 2:0.5 4:0.5 6:1 R:1", "1:1.5 R:2.5"]
P1 = "ひとりふたりと/あつまってくるよ/しおれたかおで/あるいてく"
P2 = "ねこぜなかまと/あしなみそろう/ふしぎなよるに/むねをはる"
VC = ["R:0.5 5:0.5 5:0.5 5:0.5 6:1 1':1", "7:0.5 #5:0.5 7:0.5 6:0.5 5:1.5 R:0.5",
      "R:0.5 1':0.5 1':0.5 1':0.5 7:1 6:1", "5:0.5 3:0.5 1:0.5 3:0.5 5:0.5 b7:0.5 1':1",
      "R:0.5 5:0.5 5:0.5 5:0.5 6:1 1':1", "b7:1 6:0.5 4:0.5 2:1 4:0.5 R:0.5",
      "4:0.5 5:0.5 6:0.5 5:0.5 4:1 3:1", "3:1 #5:1 7:1 R:1",
      "R:0.5 5:0.5 5:0.5 5:0.5 6:1 1':1", "7:0.5 #5:0.5 7:0.5 6:0.5 5:1.5 R:0.5",
      "R:0.5 1':0.5 1':0.5 1':0.5 7:1 6:1", "5:0.5 b7:0.5 1':0.5 b7:0.5 6:1 5:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 4:0.5 2:0.5 4:1", "b7:0.5 6:0.5 4:0.5 6:0.5 1':1.5 R:0.5",
      "1':1 6:0.5 4:0.5 5:1 4:1", "5:1.5 2:0.5 5:2"]
VCL = VC[:12] + ["R:0.5 1':0.5 1':0.5 1':0.5 7:0.5 6:0.5 5:1", "6:1 5:1 3:1.5 R:0.5", "5:1 6:1 1':2", "7:1.5 6:0.5 5:2"]
C1 = "ねこぜのぱれーどだよ/つきのしたならんであるく/くつさきみててもいい/つまさきはまえむき/ねこぜのぱれーどだよ/おなじかえりみちのうえ/かげぼうしかさなるから/むねをはろうよね"
C2 = "ねこぜのぱれーどだよ/おもいかばんもいっしょにだよ/まっすぐじゃなくてもいい/ゆっくりでもいいから/ねこぜのぱれーどだよ/おなじかえりみちのうえ/かげぼうしかさなるから/むねをはろうよね"
CL = "/".join(C1.split("/")[:6]) + "/あしたもまたここで/またあおうね"
VCR = ["R:4", "R:4", "5:2 6:1 1':1", "#7:3 R:1", "1':2.5 7:0.5 5:1", "b2':2 1':1 6:1", "4:1 5:1 1':2", "#7:2 R:2"]
VOUT = ["R:0.5 1:0.5 3:0.5 5:0.5 1':2", "6:1.5 5:0.5 3:2", "4:1 3:1 1:2", "5,:4", "R:4", "R:4"]
LY = Lyrics(S)
def put(name, key, lines, text, low=True):
    bars = S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("ぶらぶら", K, VA, V1)
if VOCAL: put("2周目", K, VA[:8], V2)
else:
    for i, b in enumerate(S.sc("2周目")):
        if i < 4: EPM.bar(b, K.mel(VA[i], oct=4))                 # BGM: 前半はエレピが歌を受け取る
        else: V.bar(b, K.mel(VA[i], oct=4))
put("集まってくる", K, VB, P1); put("集まってくる2", K, VB, P2)
put("屋根へ", KA, VC, C1); put("2回目の屋根", KA, VC, C2)
put("カラス", K, VCR, "からすが/ないてもとまらないよ", low=False)
put("屋根の上の大合唱", KA, VCL, CL)
put("夜明け前", K, VOUT, "あしたへとかえってゆこう", low=False)


# ================= ブラス（塀の上の主旋律・サビの合いの手・カラスの一撃） =================
HOOK = ["1':0.5 1':0.25 7:0.25 5:0.5 R:0.5 3:0.25 4:0.25 5:0.5 R:1", "6:0.5 6:0.25 5:0.25 3:0.5 R:0.5 1:0.25 3:0.25 1:0.5 R:1",
        "4:0.5 4:0.25 6:0.25 1':0.5 R:0.5 6:0.25 1':0.25 2':0.5 R:0.5 1':0.5", "#7:1 2':0.5 #7:0.5 5:2"]
for i, b in enumerate(S.sc("塀の上")):
    m = K.mel(HOOK[i], oct=4)
    BR[0].bar(b, m); BR[1].bar(b, K.mel(seq_up(HOOK[i], K, -2), oct=4))
for name in ("屋根へ", "2回目の屋根", "屋根の上の大合唱"):
    for i, b in enumerate(S.sc(name)):
        v = voice(S.chords[b], 66, 3)
        if i % 4 == 3:                                    # 歌のすき間に「パッ・パッ」
            for j in range(3): BR[j].bar(b, f"R:2.5 {nm(v[j])}:0.25' R:0.25 {nm(v[j])}:1")
        elif name == "屋根の上の大合唱" and i % 2 == 0:
            for j in range(3): BR[j].bar(b, f"{nm(v[j])}:0.5! R:3.5")
b_crow = S.sc("カラス")[0]
for j, m in enumerate(voice("Edim7", 66, 3)): BR[j].bar(b_crow, f"{nm(m)}:0.5! R:3.5")      # カラスの一声（とがった和音）

# ================= エレピ（ブームバップの和音） =================
COMP = ["R:0.5 X:1.5 R:0.75 X:1.25", "X:0.75 X:0.75 R:1 X:1.5", "R:0.5 X:1 R:0.5 X:0.5 X:1.5", "X:1.5 R:0.5 X:0.75 X:1.25"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    pat = None
    if n == "路地の入口" and i >= 4: pat = "X:4"
    elif n in ("ぶらぶら", "2周目", "夜明け前"): pat = COMP[i % 4]
    elif n.startswith("集まってくる"): pat = "X:1 X:1 X:1 X:1" if i < 7 else "X:1.5 R:2.5"
    elif n in ("屋根へ", "2回目の屋根", "屋根の上の大合唱"): pat = "X:0.5 R:0.25 X:0.75 X:0.5 R:0.5 X:1.5" if i % 2 == 0 else "R:0.5 X:1.5 X:0.5 X:1.5"
    elif n == "塀の上": pat = "X:0.75 X:0.75 R:2.5"
    elif n == "カラス": pat = None if i < 1 else "X:4"
    if n == "2周目" and i < 4: pat = "X:2 X:2"            # エレピが歌うときは、和音は長く
    if pat:
        for j in range(3): EP[j].bar(b, pat.replace("X", nm(v[j])))

# 月のパッド（サビの後ろ・カラス）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("屋根へ", "2回目の屋根", "屋根の上の大合唱", "カラス") and not (n == "カラス" and i == 0):
        v = voice(S.chords[b], 57, 2)
        for j in range(2): PAD[j].bar(b, f"{nm(v[j])}:4")

# ================= ベース（ブームバップの歌うベース） =================
BRIFF = {"Fm9": "F1:0.75! F1:0.25 R:0.5 Ab1:0.5 C2:0.75 F2:0.25 Eb2:0.5 C2:0.5",
         "Dbmaj7": "Db2:0.75! Db2:0.25 R:0.5 F2:0.5 Ab1:0.75 Db2:0.25 C2:0.5 Ab1:0.5",
         "Bbm7": "Bb1:0.75! Bb1:0.25 R:0.5 Db2:0.5 F2:0.75 Bb1:0.25 Ab1:0.5 F1:0.5",
         "C7": "C2:0.75! C2:0.25 R:0.5 E2:0.5 G2:0.75 C2:0.25 Bb1:0.5 E1:0.5"}
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("路地の入口", "ぶらぶら", "2周目", "塀の上") and ch in BRIFF:
        BASS.bar(b, BRIFF[ch] if not (n == "ぶらぶら" and i % 8 == 7) else "C2:0.75! C2:0.25 R:0.5 G1:0.5 Bb1:0.5 C2:0.5 E2:0.5 G2:0.5")
    elif n.startswith("集まってくる"):
        BASS.bar(b, bass_line(S, b, "half") if i < 7 else f"{nm(r)}:1.5! R:2.5")
    elif n in ("屋根へ", "屋根の上の大合唱"):
        BASS.bar(b, bass_line(S, b, "push") if i % 4 != 3 else bass_line(S, b, "walk"))
    elif n == "2回目の屋根":
        BASS.bar(b, f"{nm(r)}:2.5! {nm(r + 12)}:0.5 {nm(r + 7)}:1")     # ハーフのリズム: 長く伸ばす 808 風
    elif n == "カラス":
        if i >= 2: BASS.bar(b, f"{nm(r)}:4")
    elif n == "夜明け前":
        BASS.bar(b, BRIFF.get(ch, f"{nm(r)}:4") if i < 4 else f"{nm(r)}:4")

# ================= スクラッチ風の音（ピックで弦をこする短い音） =================
def scratch(b, at=3.0, kind="a"):
    s = {"a": "F2:0.25 G2:0.25 R:0.25 F2:0.25", "b": "F2:0.125 F2:0.125 G2:0.25 F2:0.125 F2:0.125 G2:0.25"}[kind]
    SCR.bar(b, f"R:{at:g} " + s)
scratch(S.sc("路地の入口")[7], 3.0, "b")
for name in ("ぶらぶら", "2周目"):
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 7: scratch(b, 3.0, "a" if name == "ぶらぶら" else "b")
for i, b in enumerate(S.sc("塀の上")): scratch(b, 2.0 if i % 2 else 3.0, "b" if i % 2 else "a")
scratch(S.sc("屋根の上の大合唱")[15], 3.0, "b")

# 効果音
riser(FX, S.sc("屋根へ")[0], 4, "C4"); riser(FX, S.sc("屋根の上の大合唱")[0], 8, "D4")
FX.bar(b_crow, "A4:1 R:3")                                   # カラスの羽ばたき（シュッ）
cym_swell(CYM, S.sc("2回目の屋根")[0], 2, "C4"); cym_swell(CYM, S.sc("屋根の上の大合唱")[0], 4, "E4")

# ================= ドラム（素直な生ドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "路地の入口":
        if i < 4: continue
        vgroove(D, b, "boombap", ghosts=0.4, seed=b)
        if i == 4: crash(D, b, "G2")
        if last: put_fill(D, b, "small")
    elif n in ("ぶらぶら", "2周目"):
        vgroove(D, b, "boombap", ghosts=0.45, seed=b, k="X.....x...X..x.." if i % 2 == 0 else "X.x...x...X.....")
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "tomtrip" if i == 15 else "small")
    elif n.startswith("集まってくる"):
        vgroove(D, b, "boombap", ghosts=0.3, seed=b, h="x.x.x.x.x.x.x.x." if i < 4 else "xxxxxxxxxxxxxxxx")
        if i == 6: put_fill(D, b, "snare16")
        if last: halt(D, b, 1.5)                             # 止め（1拍半だけ叩いて全員休み）
    elif n in ("屋根へ", "屋根の上の大合唱"):
        # 倍のハット（16分）。最後のサビは8小節目からライド
        vgroove(D, b, "boombap", ghosts=0.35, seed=b, h="XxxxXxxxXxxxXxxx")
        if n == "屋根の上の大合唱" and 9 <= i < 15:
            D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i == 7 else "snare16")
        if last and n == "屋根へ": put_fill(D, b, "small")
        if last and n == "屋根の上の大合唱": put_fill(D, b, "tomdown")
    elif n == "塀の上":
        vgroove(D, b, "boombap", ghosts=0.5, seed=b, h="x.x.x.x.x.x.x.x.")
        D.cym(b, ("B2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16      # ライドで歩く
        if last: put_fill(D, b, "small")
    elif n == "2回目の屋根":
        # サビごとのリズムの入れかえ: ハーフのトラップ寄り（スネアは3拍目、ハットの細かい連打）
        vgroove(D, b, "trap", ghosts=0.2, seed=b)
        if i % 8 == 0: crash(D, b, "C2")
        if i % 4 == 3 and not last: D.over(b, h="            XXXX")
        if last: put_fill(D, b, "build")
    elif n == "カラス":
        if i == 0: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "B2", 4)
        elif i < 4: D.set(b, "." * 16, "." * 16, "x...x...x...x...")
        else:
            vgroove(D, b, "half", ghosts=0.3, seed=b, h="x.x.x.x.x.x.x.x.")
            if i == 4: D.cym(b, "D2:1 D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "lift")
    elif n == "夜明け前":
        vgroove(D, b, "boombap", ghosts=0.4, seed=b) if i < 4 else D.set(b, "X.........X.....", "................", "x...x...x...x...")
        if i == 0: crash(D, b, "G2")

# 止め（Bメロの終わり2回は VB の休みとドラムの halt）。1拍の完全な無音: 2回目のサビの4拍目。カラスの一撃のあとは全員休み
for name in ("集まってくる", "集まってくる2"): SIL.add(S.sc(name)[-1], 1.5, 4)
SIL.add(S.sc("2回目の屋根")[-1], 3, 4)
SIL.add(b_crow, 1, 4)
SIL.apply()

S.fade_out = 12
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の14。ヒップホップ（ブームバップ）。Dm（サビは F）・96。"
          "うまくいかなかった日の帰り道、猫背の人どうしがくすりと笑い合い、月の下でパレードになる。ベースだけで始まり、語るような Aメロ、止めのある Bメロ、"
          "「ねこぜのぱれーど」のサビ、ブラスとスクラッチの間奏、ハーフの2サビ、カラスの止め、大合唱、夜明け前のフェードアウト。生ドラム・ベース・エレピ・ブラス。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, S.nb - 8, "コオロギ", S.beats * 8, vol=0.06)
teto(S, LY, V, transpose=-3, level={"verse": -0.2}, special={"屋根の上の大合唱": 0.5, "カラス": -0.5, "夜明け前": -0.45})
