# vt3 10「教科書の落書きたち」Doodles in the Textbook（仮）— バンジョーとフィドルのブルーグラス（ギターなし）。126・4/4（16分のロール）。G長調。
# 第3弾（0時〜24時の街）の 9時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-13）: ゼロから作り直し（人間「全ての曲を1みたいにこだわって作って」「このレベル（02 v7）まで詰めて曲作って」）。
#   v1〜v3 は 160 のブルーグラス（アコースティックギターの伴奏）。ギターは使わない（ギターに聞こえない音は使わない決まり）。
#   伴奏は、バンジョーのロール（16分）、もう1本のバンジョーの裏打ち（マンドリンの「チョップ」の役）、ベースのドン・ドン、ブラシのようなスネアの裏打ち。
#
# 物語: 9時の算数の授業。ねむくなって、教科書のすみに描いた落書き（棒人間・星・小さなねこ）。ぱらぱらめくると、動き出した。
#   棒人間が口笛でふくのは、けさ街に流れていた鼻歌（3・5・6・5・2）。数字もいっしょに踊り出す。先生がふりむくと、ぴたりと止まる。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: たいくつな式が踊り出し、ねむたい授業が冒険になる。
#
# 曲を決める表（書く前に similar_check.py --plan で確かめる）:
#   形: バンジョーのロールだけ → フィドルの節 → Aメロ1（ベースとバンジョー・後半フィドルの合いの手）→ Bメロ（先生は黒板へ・止め）
#       → サビ1（「ぱらぱらめくれば」）→ ソロ回し（バンジョー → フィドルが合いことばの節）→ Aメロ2 → Bメロ2 → サビ2
#       → 先生がふりむく（全員止まる。木の音の「カチ・カチ」だけ）→ ソロ回し2（フィドルとバンジョーのかけ合い）→ 最後のサビ → 2つの音のチャイム
#   旋律: Aメロ＝8分の弱起から7音 → 5音（七・五ではずむ）。Bメロ＝4分から始めてだんだんつめる。
#         サビ＝「ぱ・ら・ぱ・ら・め・く・れ・ば」を8分8つ（同じ2音を行き来する＝ページをめくる動き）→ 5音で答える
#   和音: I・IV・vi・II7・V7（素朴な3つの和音に、II7 をひとつ）。サビの後半だけ III7 → vi
#   ベース: 1拍目と3拍目のドン・ドン（根音と5度）。句の終わりは歩いて次の和音へ
#   この曲だけ: ①バンジョーの16分のロールが最初から最後まで走る ②サビの旋律がページをめくる動き ③先生がふりむくと全員止まる
#
# ブルーグラスの作り方（2026-11-13。作曲ソフトの手引きと、これまでの調べ）: ドラムを主役にしない。ベースが1・3拍、マンドリンのチョップが2・4拍で、これがドラムの代わり。
#   バンジョーは3本指のロール（3・3・2 の16分）。ソロは楽器が順番に回す。フィドルは歌のすき間で答える。
from vt25_lib import *

S = Song("10", "doodles", "教科書の落書きたち（仮）", "Doodles in the Textbook", 126, 4, "G", "major", "バンジョーとフィドルのブルーグラス（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
S.keepers = {}
K = Key("G", "major")          # oct 4 で 1 = G4

A_CH = ["G", "G", "C", "G", "G", "Em", "A7", "D7"]
B_CH = ["C", "G", "C", "G", "Am7", "A7", "D7sus4", "D7"]
C_CH = ["G", "C", "G", "D", "Em", "C", "G", "D7", "G", "C", "G", "B7", "Em", "C", "D7", "G"]

S.scene("バンジョー", 4, "intro", ["G", "G", "C", "D7"])
S.scene("フィドル", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("ソロ回し", 8, "solo", A_CH)
S.scene("Aメロ2", 16, "verse", A_CH + A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ふりむく", 4, "bridge", ["Em", "Em", "A7", "D7"])
S.scene("ソロ回し2", 8, "solo", A_CH)
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("チャイム", 4, "outro", ["G", "C", "G", "G"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
BJ = S.track("バンジョー（ロール）", "banjo", volume=0.17, pan=0.3, reverb=0.15)
BJC = [S.track(f"バンジョー（裏打ち{i + 1}）", "banjo", volume=0.06, pan=-0.35, reverb=0.15, sustain=0.3) for i in range(2)]
FID = S.track("フィドル", "fiddle", volume=0.11, pan=-0.15, reverb=0.3)
FID2 = S.track("フィドル（下の音）", "fiddle", volume=0.07, pan=-0.3, reverb=0.3)
BASS = S.track("ベース（指弾き・丸い音）", "bass", sustain=0.8, **dict(finger_bass_spec(vol=0.21), fx=[{"type": "eq", "low": 1, "mid": 0, "midHz": 800, "high": -4}, {"type": "filter", "kind": "lowpass", "freq": 1300, "q": 0.6}]))
WB = S.track("木の音（時計）", "lead", patch="marimba", volume=0.08, pan=0.1, reverb=0.2)
GLK = S.track("チャイム（鉄琴）", "glockenspiel", volume=0.09, pan=0.2, reverb=0.4)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.04, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5,:0.5 1:0.5 1:0.5 3:0.5 1:0.5 3:0.5 5:0.5", "5:0.75 3:0.75 1:0.5 3:0.5 1:0.5 R:1",
      "R:0.5 6,:0.5 1:0.5 1:0.5 4:0.5 1:0.5 4:0.5 6:0.5", "5:0.75 3:0.75 1:0.5 5,:0.5 1:0.5 R:1",
      "R:0.5 3:0.5 3:0.5 5:0.5 5:0.5 3:0.5 5:0.5 6:0.5", "5:0.75 3:0.75 7,:0.5 3:0.5 3:0.5 R:1",
      "R:0.5 2:0.5 2:0.5 #4:0.5 6:0.5 #4:0.5 2:0.5 6:0.5", "5:0.75 4:0.75 2:0.5 7,:0.5 2:0.5 R:1"]
A1 = ("くじのさんすうねむくなる/きょうかしょのすみらくがきだ/ぼうにんげんとほしひとつ/ちいさなねこもかいてみた/"
      "せんせいのこえとおくなる/まぶたがおもいそのときに/ぺーじのすみでなにかがね/もぞもぞうごくきがしたの")
A2 = ("ぼうにんげんがくちぶえで/どこかできいたあのふしを/けさのまちでもながれてた/あのはなうただきがついた/"
      "すうじのさんがとびはねて/はちはくるくるまわりだす/たいくつなしきおどりだす/のーとのうえはおおさわぎ")
VB = ["4:1 6:1 6:0.5 5:0.5 4:1", "3:1 5:1 R:2", "4:1 6:1 6:0.5 7:0.5 6:1", "5:1 3:1 R:2",
      "2:0.5 2:0.5 4:0.5 4:0.5 6:1 4:1", "#4:1 6:1 R:2", "5:0.5 5:0.5 5:0.5 5:0.5 6:1 7:1", "7:2 R:2"]
B1 = "せんせいはいま/こくばんむいた/いまのうちだよね/でておいでよー"
B2 = "せんせいがほら/ふりむきそうだ/いきをひそめてね/しずかにしてー"
# サビ: 「ぱらぱらめくれば」＝同じ2つの音を行き来する8分8つ（ページをめくる動き）→ 5音で答える
FLIP = "3:0.5 5:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 5:0.5"
FLIP2 = "3:0.5 5:0.5 3:0.5 5:0.5 7:0.5 5:0.5 3:0.5 5:0.5"
VC = [FLIP, "6:0.75 6:0.75 5:0.5 4:0.5 6:0.5 R:1", FLIP2, "7:0.75 7:0.75 5:0.5 2:0.5 5:0.5 R:1",
      "3:1 5:1 6:1 5:1", "4:1 6:1 5:0.5 4:0.5 R:1", "3:1 5:1 3:1 2:1", "2:2 R:2",
      FLIP, "6:0.75 6:0.75 5:0.5 4:0.5 6:0.5 R:1", FLIP2, "7:0.75 7:0.75 5:0.5 #2:0.5 7:0.5 R:1",
      "3:1 5:1 6:1 7:1", "6:1.5 5:0.5 4:1 R:1", "7:1 6:1 5:1 2:1", "1:3 R:1"]
C1 = ("ぱらぱらめくればうごきだす/ぱらぱらめくればはしりだす/ぼうにんげんたち/れつをくむ/"
      "ぱらぱらめくればとびだした/ぱらぱらめくればほしがとぶ/すうじもおどる/ぱれーどだ")
C2 = ("ぱらぱらめくればうたいだす/ぱらぱらめくればあのふしを/ちいさなねこまで/くちぶえで/"
      "ぱらぱらめくればきょうしつは/ぱらぱらめくればおまつりだ/まどのそとまで/つづいてく")
C3 = ("ぱらぱらめくればここにいる/ぱらぱらめくればともだちが/ねむたいじゅぎょうも/ぼうけんだ/"
      "ぱらぱらめくればうごきだす/ぱらぱらめくればはしりだす/ぺーじのすみっこ/ぱれーどだ")
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA + VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("最後のサビ", VC, C3)

# ================= バンジョー・フィドル =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]
ROLL_A = (0, 1, 2, 0, 1, 2, 0, 1, 0, 1, 2, 0, 1, 2, 0, 2)      # 3・3・2 のロール
ROLL_B = (2, 1, 0, 2, 1, 0, 2, 1, 0, 1, 2, 0, 2, 1, 0, 2)      # うしろ向きのロール
ROLL_S = (0, 2, 0, 2, 0, 2, 0, 2)                              # 8分だけ（静かな所）


def roll(b, pat=ROLL_A, lo="G3", hi="E5", pick=(0, 2, 3)):
    tn = tones(root(b), lo, hi); tn = [tn[q % len(tn)] for q in pick]
    L = 4 / len(pat); BJ.bar(b, " ".join(f"{nm(tn[q])}:{L:g}" for q in pat))


def chop(b, pat="R:1 x:0.5 R:1.5 x:0.5 R:0.5"):
    v = sorted(voice(root(b), 67, 3))
    for j in range(2): BJC[j].bar(b, " ".join(t.replace("x", nm(v[j + 1])) for t in pat.split()))


def fid_long(b, c=71):
    v = sorted(voice(root(b), c, 3)); FID.bar(b, f"{nm(v[2])}:4"); FID2.bar(b, f"{nm(v[0])}:4")


def fid_fill(b, order=(1, 2), lead="R:3"):
    tn = tones(root(b), "D5", "D6"); FID.bar(b, lead + " " + " ".join(f"{nm(tn[q % len(tn)])}:0.5" for q in order))


TUNE = ["D5:0.5 G5:0.5 B5:0.5 G5:0.5 A5:0.5 G5:0.5 E5:0.5 D5:0.5", "B4:0.5 D5:0.5 G5:1 D5:0.5 B4:0.5 G4:1",
        "E5:0.5 G5:0.5 C6:0.5 G5:0.5 E5:0.5 G5:0.5 E5:0.5 C5:0.5", "D5:0.5 B4:0.5 G4:0.5 B4:0.5 D5:1 R:1",
        "G5:0.5 B5:0.5 D6:0.5 B5:0.5 G5:0.5 B5:0.5 A5:0.5 G5:0.5", "E5:0.5 G5:0.5 B5:1 G5:0.5 E5:0.5 B4:1",
        "C#5:0.5 E5:0.5 A5:0.5 E5:0.5 G5:0.5 E5:0.5 C#5:0.5 A4:0.5", "D5:0.5 F#5:0.5 A5:0.5 C6:0.5 D6:1 R:1"]
MOTIF = "R:1 B4:0.5 D5:0.5 E5:1 D5:0.5 A4:0.5"                 # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "バンジョー":
        roll(b, ROLL_A if i % 2 == 0 else ROLL_B)
        if i >= 2: chop(b)                                       # v5: 出だしが小さすぎた（−27dB。次の場面は −17dB）→ バンジョーを大きく、後半から裏打ちとベース
    elif n == "フィドル":
        roll(b, ROLL_A if i % 2 == 0 else ROLL_B); chop(b); FID.bar(b, TUNE[i])
    elif n == "Aメロ1":
        roll(b, ROLL_A if i % 2 == 0 else ROLL_B)       # v5: 歌が入る所で 3.1dB 下がっていた（前半を8分だけにしていた）→ 頭から16分のロールと軽いキック
        chop(b)
        if i >= 8 and i % 2 == 1: fid_fill(b, (1, 2) if i % 4 == 1 else (3, 2))
    elif n == "Aメロ2":
        roll(b, ROLL_B if i % 2 == 0 else ROLL_A); chop(b, "R:1 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 R:0.5" if i >= 8 else "R:1 x:0.5 R:1.5 x:0.5 R:0.5")
        if i % 2 == 1: fid_fill(b, (2, 3, 2) if i >= 8 else (2, 1), lead="R:2.5" if i >= 8 else "R:3")
        if i >= 8: FID2.bar(b, f"{nm(tones(root(b), 'G4', 'G5')[0])}:4")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6: roll(b, ROLL_S); fid_long(b, 66 + i)
        elif i == 6: roll(b, ROLL_A); fid_long(b, 72)
        else: BJ.bar(b, f"{nm(tones(root(b), 'D4', 'D5')[-1])}:1 R:3"); FID.bar(b, "A5:2 R:2")
        if i < 7: chop(b, "R:1 x:0.5 R:1.5 x:0.5 R:0.5")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        roll(b, ROLL_A if i % 2 == 0 else ROLL_B, hi="G5", pick=(0, 2, 3) if n == "サビ1" else (1, 3, 4))
        chop(b, "R:1 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 R:0.5" if n != "サビ1" else "R:1 x:0.5 R:1.5 x:0.5 R:0.5")
        # フィドル: サビ1 は長い音。サビ2 は歌の答えのあと（偶数の小節の4拍目）に合いの手。最後のサビは長い音＋合いの手
        if n == "サビ1": fid_long(b, 71)
        else:
            if i in (1, 3, 9, 11): fid_fill(b, (2, 3), lead="R:3")
            elif i in (7, 15): FID.bar(b, TUNE[7] if i == 7 else TUNE[3])
            else: fid_long(b, 74 if n == "最後のサビ" else 71)
    elif n == "ソロ回し":                                          # バンジョーが4小節 → フィドルが4小節（合いことばの節から）
        chop(b)
        if i < 4: roll(b, ROLL_B if i % 2 == 0 else ROLL_A, lo="D4", hi="D6", pick=(1, 3, 4))
        else: roll(b, ROLL_S); FID.bar(b, [MOTIF, TUNE[5], TUNE[6], TUNE[7]][i - 4])
    elif n == "ふりむく":                                          # 全員止まる。木の音の「カチ・カチ」だけ → 最後の小節でバンジョーがそっともどる
        WB.bar(b, "E6:1 B5:1 E6:1 B5:1")
        if i == 3: roll(b, (0, 1, 2, 0, 1, 2, 0, 1), lo="D4", hi="D6", pick=(0, 1, 2)); FID.bar(b, "R:2 A5:0.5 C6:0.5 D6:1")
    elif n == "ソロ回し2":                                         # フィドルとバンジョーが2小節ずつかけ合う
        chop(b, "R:1 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 R:0.5")
        if i in (0, 1, 4, 5): roll(b, ROLL_S); FID.bar(b, TUNE[i])
        elif i < 6: roll(b, ROLL_A if i % 2 == 0 else ROLL_B, lo="D4", hi="D6", pick=(1, 3, 4))
        else: roll(b, ROLL_A if i % 2 == 0 else ROLL_B); FID.bar(b, TUNE[i])
    elif n == "チャイム":
        if i < 2: roll(b, ROLL_A if i == 0 else ROLL_B); chop(b); FID.bar(b, TUNE[i * 2])
        elif i == 2: BJ.bar(b, "G3:0.5 B3:0.5 D4:0.5 G4:0.5 B4:1 R:1"); FID.bar(b, "G5:1 R:3"); GLK.bar(b, "R:2 D6:1 G6:1")      # 2つの音のチャイム
        else: GLK.bar(b, "R:4")

# ================= ベース（1拍目と3拍目のドン・ドン。句の終わりは歩く。共通の部品 bass_line は使わない）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t3 = next((m for m in up if (m - r) in (3, 4)), r + 4)
    lo5 = t5 - 12 if t5 - 12 >= 28 else t5
    d = rn - r; w1, w2 = (r + 2, r + 4) if d > 0 else ((r - 1, r - 3) if d < 0 else (t3, t5))
    boom = f"{nm(r)}:1 R:1 {nm(lo5)}:1 R:1"
    boom2 = f"{nm(r)}:1 R:1 {nm(lo5)}:1 {nm(t3)}:0.5 {nm(r)}:0.5"
    walk = f"{nm(r)}:1 R:1 {nm(w1)}:1 {nm(w2)}:1"
    drive = f"{nm(r)}:1 {nm(t5)}:0.5 {nm(r)}:0.5 {nm(lo5)}:1 {nm(w1)}:0.5 {nm(w2)}:0.5"
    if n == "バンジョー" and i >= 2: BASS.bar(b, boom if i == 2 else walk)
    elif n in ("フィドル", "Aメロ1", "ソロ回し", "ソロ回し2"): BASS.bar(b, walk if (rn != r and i % 2 == 1) else (boom if i % 4 != 2 else boom2))
    elif n == "Aメロ2": BASS.bar(b, walk if rn != r else (boom2 if i % 2 == 0 else boom))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, f"{nm(r)}:2 {nm(lo5)}:2" if i < 6 else (walk if i == 6 else f"{nm(r)}:1 R:3"))
    elif n == "サビ1": BASS.bar(b, walk if rn != r and i % 2 == 1 else boom)
    elif n in ("サビ2", "最後のサビ"): BASS.bar(b, drive if i % 4 == 3 else (walk if rn != r and i % 2 == 1 else boom2))
    elif n == "チャイム" and i < 3: BASS.bar(b, boom if i < 2 else f"{nm(r)}:1 R:3")

# ================= ドラム（主役にしない。スネアの裏打ちと軽いキックだけ）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "フィドル": D.set(b, "X.......X.......", "....x.......x...", "................")
    elif n == "Aメロ1":
        D.set(b, "X.......X.......", "....x.......x...", "................" if i < 8 else "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "small")
    elif n in ("Aメロ2", "ソロ回し", "ソロ回し2"):
        D.set(b, "X.......X.......", "....x.......x..." if i % 4 != 3 else "....x.......x.x.", "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6: D.set(b, "X.......X.......", "................", "x...x...x...x...")
        elif i == 6: D.set(b, "X...X...X...X...", "....X...X.X.XXXX", "................")
        else: D.set(b, "X...............", "X...............", "................")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.......X.....x." if i % 2 == 0 else "X.......X.......", s="....X.......X...", h="x.x.x.x.x.x.x.x.", vary=False)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i == 7: put_fill(D, b, "small")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "チャイム":
        if i < 2: D.set(b, "X.......X.......", "....x.......x...", "x.x.x.x.x.x.x.x.")
        elif i == 2: D.set(b, "X...............", "X...............", "................")

# 止め: Bメロ の8小節目は、頭の2拍のあと全員休み
for nme in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(nme)[-1], 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の10（9時）。バンジョーとフィドルのブルーグラス（ギターなし）。G・126。教科書の落書きが、ぱらぱらめくると動き出す。"
          "サビは「ぱらぱらめくれば」。バンジョーの16分のロール、裏打ち、フィドル、ベースのドン・ドン。先生がふりむくと全員止まる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"ふりむく": -0.4, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "バンジョー（ロール", mid=84, down=12, up=8, seed=3); humanize(path, "フィドル", mid=86, down=8, up=8, seed=5)
# v4 を測ると、最後のサビ（−14.9）が サビ2（−14.1）より小さかった → 山を最後に
final_gain(path, {"バンジョー": 2.0, "サビ2": -0.2, "最後のサビ": 1.6, "チャイム": 0.8})
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 20, "最後のサビ": 24}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
