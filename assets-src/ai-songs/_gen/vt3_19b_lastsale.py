# vt3 19「商店街ラストセール」Last Sale on Shopping Street（仮）— 街を歩く楽隊のブラスバンド・ファンク（4分の4・102）。B♭ → B → C → D♭。
# 第3弾（0時〜24時の街）の 18時。表は docs/sound/vt3-plan.md。
#
# v3（2026-11-19）: ゼロから作り直し。v1・v2 はサンバ（ホイッスルを仕上げで 12dB 持ち上げていた）。
#   人間の指示: 「18からは1曲ずつコンセプトとかジャンルをしっかり決めて作って行こうか。つまり作り直そう」（2026-11-19）。下の表を見せて「良い」をもらってから作った。
#
# コンセプト: 閉店セールの日なのに、商店街がいちばんにぎやかになる。さみしい日を、お祭りに書きかえる。
# ジャンル: ニューオーリンズ風のブラスバンド・ファンク（街を歩きながら演奏する楽隊）。作る前に調べた決まりごと:
#   ・ベースの役はスーザフォン（チューバ）。曲はスーザフォンのくり返しの型から始まることが多い
#   ・小太鼓（こまかい連打とアクセント）と大太鼓（食いこむ型。2小節めの4拍めを強く＝「ビッグ・フォー」）は別べつの人がたたく。大太鼓についた小さいシンバルが裏拍
#   ・管楽器は短い節（リフ）を呼びかけと返事で回す。トロンボーンはすき間に下から合いの手。ピアノとギターはいない
#   ・リズムはきっちりの16分と、はねた16分の「あいだ」
#   ・終わりは3拍めで止める
# 音の地図の場所: 生の楽器の側・にぎやかな側。18（生の楽器・静か）とも、16・17（まん中）ともちがう。電子の音・ギター・ピアノ・ドラムセットの形のたたき方は使わない。
#
# 曲を決める表:
#   形: 楽隊が来る（太鼓 → スーザフォン → トランペットの合図）→ テーマ（管のリフ）→ 呼びこみ1（声2小節・管の返事2小節）→ 歌1 → 「まけた！」（全員止まる・調が上がる）
#       → サビ1（B）→ 呼びこみ2 → 歌2 → 「まけた！」→ サビ2（C）→ 楽隊の番（トロンボーン → トランペットとサックスのかけ合い → 全員のキメ）
#       → しずかな通り（スーザフォンと手拍子と声だけ）→ 「まけた！」→ 最後のサビ（D♭・全員）→ 手じめ（手拍子と声だけ → 3拍めで全員1発）
#   場面と強さ: 楽隊が来る 中弱 → 中／テーマ 中強／呼びこみ 中／歌 中弱／サビ1 中強／サビ2 強／楽隊の番 強／しずかな通り 弱／最後のサビ 最強／手じめ 中（手拍子）
#   旋律: 呼びこみは 5・6 の音のまわりで短くはずむ。歌は下の音域（1〜6）で、1行ごとに2拍の休み（そこへ管が合いの手）。いちばん高い音（3'）はサビにとっておく。
#   和音: 歌は B♭・Gm・E♭・F7・D7。テーマと呼びこみは 7 の和音（B♭7・E♭7）で、管はブルースの音（♭3・♭7）を使う。
#   ベース: スーザフォン。根音・5度・7度のくり返しの型（場面ごとに型を変える）。
#   ドラム: 小太鼓と大太鼓。入り方は「太鼓だけで始まる」。サビは2小節ひとまとまり（2小節めの4拍めが強い）。
#   この曲だけ: ①「まけた！」のたびに全員が止まり、調が1つ上がる（3回）。値段が下がるほど曲は上がる ②最後は楽器なしの手じめ
#   声: キュート 1 種類で最後まで。
#   ほかの曲とのちがい: 04（ホーン隊のスカ・176・裏打ちのギター）は速いバンドの曲。こちらはギターもピアノもなく、スーザフォンがベース、太鼓が2人、102 のはねるリズム。13（ファンク）はエレキベースとドラムセット。
from vt25_lib import *

S = Song("19", "lastsale", "商店街ラストセール（仮）", "Last Sale on Shopping Street", 102, 4, "Bb", "major", "ブラスバンド・ファンク（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.keepers = {}
KEYS = [Key("Bb", "major"), Key("B", "major"), Key("C", "major"), Key("Db", "major")]
BASE = [3, 3, 4, 4]                       # 歌の高さ: その調の 1 が B♭3・B3・C4・D♭4
up = lambda L, n: [tr_chord(c, n) for c in L]

TH = ["Bb7", "Bb7", "Eb7", "Bb7", "Gm", "C7", "F7", "Bb7"]
CALL = ["Bb7", "Bb7", "Bb7", "Bb7", "Eb7", "Eb7", "Bb7", "F7"]
VCH = ["Bb", "Gm", "Eb", "F7", "Bb", "D7", "Eb", "F7"]
CH = ["Eb", "Bb", "Eb", "Bb", "Gm", "C7", "F7", "Bb"]
SOLO = ["Bb7", "Bb7", "Eb7", "Bb7", "Bb7", "Bb7", "Eb7", "Bb7", "Gm", "C7", "F7", "Bb7"]

PLAN = [("楽隊が来る", 4, "intro", ["Bb7"] * 4, 0), ("テーマ", 8, "solo", TH, 0), ("呼びこみ1", 8, "verse", CALL, 0), ("歌1", 8, "verse", VCH, 0),
        ("まけた1", 2, "bridge", ["F7", "F#7"], 0), ("サビ1", 8, "chorus", up(CH, 1), 1), ("呼びこみ2", 8, "verse", up(CALL, 1), 1), ("歌2", 8, "verse", up(VCH, 1), 1),
        ("まけた2", 2, "bridge", ["F#7", "G7"], 1), ("サビ2", 8, "chorus", up(CH, 2), 2), ("楽隊の番", 12, "solo", up(SOLO, 2), 2), ("しずかな通り", 8, "bridge", up(VCH, 2), 2),
        ("まけた3", 2, "bridge", ["G7", "Ab7"], 2), ("最後のサビ", 16, "chorus", up(CH + CH, 3), 3), ("手じめ", 6, "outro", ["Db"] * 6, 3)]
KI = []
for name, n, kind, ch, ki in PLAN:
    S.scene(name, n, kind, ch)
    KI += [ki, ki + 1] if name.startswith("まけた") else [ki] * n      # 「まけた」の2小節めは、もう次の調

V = Voice(S, vol=0.2, delay=0.25, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit()


def km(b, line, rel=0):
    """その小節の調で、度数の節を音名に。rel: 歌の高さからのオクターブ（管は 0 か −1）"""
    return KEYS[KI[b]].mel(line, oct=BASE[KI[b]] + rel)


# ================= 歌 =================
# 呼びこみ（声2小節 → 管の返事2小節）
CA = ["5:0.5 5:0.5 6:0.5 5:0.5 3:0.5 5:0.5 6:0.5 5:0.5", "R:0.5 5:0.5 5:0.5 3:0.5 2:0.5 1:1.5", "R:4", "R:4",
      "3:0.5 5:0.5 6:0.5 5:1 6:0.5 5:0.5 3:0.5", "R:0.5 5:0.5 6:0.5 1':0.5 6:0.5 5:1.5", "R:4", "R:4"]
TC1 = "さあさあおいでよ/きょうかぎり/さかなもはなも/はんがくだ"
TC2 = "さあさあおいでよ/まだまける/やさいもほんも/まだやすい"
# 歌（1行＝2小節。うしろの2拍は休み＝管の合いの手）
P7a = ["1:0.5 2:0.5 3:0.5 5:1 3:0.5 2:1", "3:2 R:2"]
P7b = ["3:0.5 3:0.5 5:0.5 6:1 5:0.5 3:1", "2:2 R:2"]
P8 = ["R:0.5 1:0.5 2:0.5 3:0.5 5:1 6:0.5 5:0.5", "3:1 2:1.5 R:1.5"]
P8b = ["1:0.5 2:0.5 3:0.5 5:0.5 5:0.5 3:0.5 2:1", "3:2 R:2"]
P7c = ["6:0.5 5:0.5 3:1 2:0.5 1:0.5 2:1", "2:2.5 R:1.5"]
P5 = ["R:1 3:0.5 5:0.5 6:1 5:1", "5:2.5 R:1.5"]
TV1 = "ろくじゅうねんの/のれんがゆれる/はりがみのもじを/かぜによませて"
TV2 = "だがしやのまえに/むかしのわたし/らじおのあのふし/みんなでうたう"
TQ = "まちのあかりが/ひとつずつきえて/それでもうたは/きえないよ"
# サビ（いちばん高い音 3' はここだけ）
C1 = ["5:0.5 1':0.5 1':0.5 2':1 1':0.5 6:0.5 6:0.5", "5:2 R:2"]
C2 = ["6:0.5 1':0.5 2':0.5 3':1 2':0.5 1':0.5 6:0.5", "1':2 R:2"]
C3 = ["5:0.5 1':0.5 1':0.5 2':1 1':0.5 2':0.5 3':0.5", "2':2 R:2"]
C4 = ["R:0.5 5:0.5 6:0.5 1':1 2':1.5", "1':3 R:1"]
C4E = ["R:0.5 6:0.5 1':0.5 2':1 2':1.5", "3':3 R:1"]            # 最後だけ上で終わる
TS1 = "さいごのひだから/いちばんにぎやか/なみだはおまけに/つけとくよ"
TS2 = "さいごのひだから/いちばんわらおう/おもいでみんなに/くばろうよ"
# 「まけた！」: 1小節めは止まった中で声だけ。2小節めはもう次の調
MK = [("まけた/もうひとこえ", "R:0.5 5:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 R:0.5"),
      ("まけた/まだまだいける", "5:0.5 5:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 R:0.5"),
      ("まけた/ぜんぶあげるよ", "5:0.5 5:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 R:0.5")]
# 手じめ（声と手拍子だけ。さいごの句は合いことばの節 3・5・6・5・2 から 1 へ）
TJ = ["5:0.5 5:0.5 6:0.5 5:0.5 3:1 R:1", "R:4", "6:0.5 6:0.5 1':0.5 6:0.5 5:1 R:1", "R:4", "R:0.5 3:0.5 5:0.5 6:0.5 5:0.5 2:0.5 1:1", "R:4"]
LY = Lyrics(S)


def put(name, lines, text):
    bars = S.sc(name); mel = [km(b, x) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars[:len(mel)], mel, text, name)


put("呼びこみ1", CA, TC1); put("歌1", P7a + P7b + P8 + P7c, TV1)
put("サビ1", C1 + C2 + C3 + C4, TS1)
put("呼びこみ2", CA, TC2); put("歌2", P8b + P7b + P8 + P7c, TV2)
put("サビ2", C1 + C2 + C3 + C4, TS2)
put("しずかな通り", P7a + P8 + P7b + P5, TQ)
put("最後のサビ", C1 + C2 + C3 + C4 + C1 + C2 + C3 + C4E, TS1 + "/" + TS2)
put("手じめ", TJ, "ありがとう/ありがとう/またどこかで")
for k, (txt, line2) in enumerate(MK): put(f"まけた{k + 1}", ["5:0.5 5:0.5 1':1 R:2", line2], txt)

# ================= 楽器（音量は最初から最後まで同じ。仕上げで持ち上げない）=================
# 1 回めの書き出しを、曲から分けて測った（tools/vt3/part_balance.py）: 太鼓 −21dB・管ぜんぶ −37dB・スーザフォン −43dB。管がほとんど聞こえず、太鼓だけの曲になっていた（BGM 7.05）。
#   2 回め: 管 −30dB（まだ太鼓より 8dB 小さい）→ boost をさらに +8。
#   → 管とスーザフォンを volume 0.5（上のかぎり）＋ boost で上げ、手拍子も上げる。太鼓は少し下げる
BST = lambda g: [{"type": "boost", "gain": g}]
TP = S.track("トランペット", "brass", patch="trumpet", volume=0.5, pan=0.18, reverb=0.22, fx=BST(11.5))
AS = S.track("アルトサックス", "brass", patch="altoSax", volume=0.5, pan=-0.3, reverb=0.22, fx=BST(9.5))
SX = S.track("テナーサックス", "brass", patch="tenorSax", volume=0.5, pan=0.35, reverb=0.22, fx=BST(9.5))
TB = S.track("トロンボーン", "brass", patch="trombone", volume=0.5, pan=-0.15, reverb=0.22, fx=BST(11.5))
TU = S.track("スーザフォン（チューバ）", "bass", patch="tuba", volume=0.5, pan=0.0, reverb=0.12, sustain=0.9, fx=BST(8))
from vb25_lib import season
CL = season(S, 0, "手拍子", 1, vol=0.3); CL.ev = []

root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def horns(b, line, tp=True, lows=True, alto=False):
    """管のリフ（トランペットは歌の高さ、テナーとトロンボーンは1オクターブ下）"""
    if tp: TP.bar(b, km(b, line, 0))
    if alto: AS.bar(b, km(b, line, 0))
    if lows: SX.bar(b, km(b, line, -1)); TB.bar(b, km(b, line, -1))


def stab(b, pat, c=62, alto=True):
    """短い和音の合いの手（トロンボーン・テナー・アルト）。pat: 'R:1.5 x:0.5 R:1.5 x:0.5' の x の所で鳴らす"""
    v = sorted(voice(root(b), c, 3))
    for tr, m in ((TB, v[0]), (SX, v[1])) + (((AS, v[2]),) if alto else ()):
        tr.bar(b, " ".join(t if t.startswith("R") else f"{nm(m)}:{t.split(':')[1]}" for t in pat.split()))


def tuba(b, kind):
    r = low(S.chords[b], "G1"); ch = root(b); seven = ch.endswith("7"); minor = "m" in ch and not ch.endswith("maj7")
    f5 = r + 7; t7 = r + 10 if (seven or minor) else r + 9; o8 = r + 12
    nx = low(S.chords[b + 1], "G1") if b + 1 < S.nb else r; ap = nx - 1 if nx != r else f5
    R_, F, T, O, A = nm(r), nm(f5), nm(t7), nm(o8), nm(ap)
    pats = {"funkA": f"{R_}:0.75 R:0.75 {R_}:0.5 {T}:0.5 {O}:0.5 R:0.5 {F}:0.5",
            "funkB": f"{R_}:0.75 R:0.25 {O}:0.5 R:0.5 {T}:0.5 {F}:0.5 {R_}:0.5 {A}:0.5",
            "funkC": f"{R_}:0.5 {R_}:0.5 R:0.5 {F}:0.5 R:0.5 {T}:0.5 {O}:0.5 {F}:0.5",
            "walk": f"{R_}:1 {F}:1 {T}:1 {A}:1",
            "light": f"{R_}:1.5 {R_}:0.5 R:1 {F}:1",
            "lightB": f"{R_}:1.5 {F}:0.5 R:1 {R_}:0.5 {A}:0.5",
            "two": f"{R_}:1.5 R:0.5 {F}:1.5 R:0.5",
            "long": f"{R_}:3 R:1", "hit": f"{R_}:0.5 R:3.5"}
    TU.bar(b, pats[kind])


def clap(b, beats=(1, 3), L=0.5):
    for q in beats: CL.at(b * 4 + q, f"B4:{L:g}")


# 太鼓の型（大太鼓, 小太鼓, 大太鼓についた小さいシンバル）。X 強・x ふつう・o ごく弱い
ST_A = ("X.....x...x.....", "o.xo.oX.o.xoX.o.", "..x...x...x...x.")
ST_B = ("X.....x.....X...", "o.xo.oX.oox.X.xx", "..x...x...x...X.")       # 4拍めを強く（ビッグ・フォー）
LT_A = ("X.........x.....", "..o.x..o..o.x.o.", "..x...x...x...x.")       # 歌の軽い型
LT_B = ("X.....x.....x...", "..o.x.o...o.x.oo", "..x...x...x...x.")
CH_A = ("X.....x...x..x..", "o.o.X.oxo.o.X.xo", "..x...x...x...x.")
CH_B = ("X..x..x.....X...", "o.o.X.oxo.x.X.XX", "..x...x...x...X.")
SO_A = ("X..x..x...x..x..", "..o.X..o.o..X.oo", "x.x.x.x.x.x.x.x.")
SO_B = ("X..x..x.....X...", "..o.X..o.ox.X.xX", "x.x.x.x.x.x.x.X.")
ROLL = ("X...............", "ooooooooxxxxXXXX", "................")       # 止まったあとの連打（だんだん強く）

# テーマ（管のリフ。B♭7 の上でブルースの音）
THEME = ["R:0.5 5:0.5 b7:0.5 1':1 b7:0.5 5:1", "b3:0.25 3:0.75 1:1 R:2", "R:0.5 4:0.5 6:0.5 1':1 6:0.5 4:1", "5:0.5 3:0.5 1:1 R:2",
         "R:0.5 6:0.5 1':0.5 3':1 1':0.5 6:1", "2':1.5 1':0.5 6:1 #4:1", "5:0.5 5:0.5 R:0.5 5:0.5 6:0.5 7:0.5 2':1", "1':1 R:3"]
TAIL = ["R:4", "R:2 5:0.5 6:0.5 b7:0.5 1':0.5", "R:4", "R:2 1:0.5 2:0.5 b3:0.25 3:0.75", "R:4", "R:4", "R:4", "R:1.5 5:0.5 b7:0.5 6:0.5 5:0.5 3:0.5"]   # トロンボーンの合いの手（すき間に下から）
ANS1 = ["R:0.5 5:0.5 b7:0.5 1':1 b7:0.5 5:1", "b3:0.25 3:0.75 1:1 R:2"]
ANS2 = ["1':0.5 1':0.5 R:0.5 b7:0.5 5:1 3:1", "5:0.5 6:0.5 7:0.5 2':1.5 R:1"]
FILL = ["R:2 6:0.5 1':0.5 3':0.5 2':0.5", "R:2 2':0.5 1':0.5 6:0.5 5:0.5", "R:2.5 3':0.5 2':0.5 7:0.5", "R:1.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5"]     # 歌の行のあとの合いの手
CANS = {1: "R:2.5 3:0.5 5:0.5 6:0.5", 3: "R:2 3':0.5 1':0.5 6:0.5 5:0.5", 5: "R:2 6:0.5 1':0.5 2':0.5 #4:0.5", 7: "R:3 5:0.25 6:0.25 7:0.5"}          # サビの、歌の休みに入るトランペット
OBB = ["3:1 5:1 6:1 5:1", "R:0.5 3:0.5 5:0.5 6:0.5 5:1 3:1", "4:1 6:1 1':1 6:1", "R:0.5 5:0.5 6:0.5 1':0.5 6:1 5:1"]                                  # 最後のサビのアルトサックス（ゆっくり動く線）
TSOLO = ["1:1 b3:0.25 3:0.75 5:0.5 6:0.5 5:1", "b7:1.5 5:0.5 3:0.5 1:0.5 R:1", "4:0.5 6:0.5 1':1 b3':0.5 1':0.5 6:1", "5:1.5 b3:0.25 3:0.25 1:2"]
TRADE = [("TP", "R:0.5 5:0.5 b7:0.5 1':0.5 3':1 1':1"), ("AS", "3':0.5 1':0.5 b7:0.5 5:0.5 b7:0.5 5:0.5 3:1"), ("TP", "R:0.5 6:0.5 1':0.5 b3':0.5 4':1 b3':0.5 1':0.5"), ("AS", "5:0.5 6:0.5 b7:0.5 1':0.5 3':2")]
SHOUT = ["6:0.5 6:0.5 R:0.5 1':0.5 R:0.5 3':0.5 1':1", "2':0.5 2':0.5 R:0.5 1':0.5 R:0.5 6:0.5 #4:1", "5:0.5 5:0.5 R:0.5 7:0.5 R:0.5 2':0.5 4':1", "3':1 1':0.5 b7:0.5 5:1 R:1"]
OFF = "R:1.5 x:0.5 R:1.5 x:0.5"; OFF2 = "R:0.5 x:0.5 R:1 x:0.5 R:1 x:0.5"; LONG = "x:3 R:1"

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "楽隊が来る":                                         # 太鼓だけ → スーザフォン → トランペットの合図 → 全員「ヘイ」
        D.set(b, *(ST_A if i % 2 == 0 else ST_B))
        if i >= 1: tuba(b, "funkA" if i % 2 else "funkB")
        if i == 2: TP.bar(b, km(b, "R:1 5:0.5 1':0.5 3':2"))
        if i == 3: TP.bar(b, km(b, "5':0.5 3':0.5 1':1 R:2")); stab(b, "R:2 x:0.5 R:1.5", 62)
    elif n == "テーマ":
        D.set(b, *(ST_A if i % 2 == 0 else ST_B)); tuba(b, ("funkA", "funkB", "funkA", "funkC")[i % 4] if not last else "walk")
        TP.bar(b, km(b, THEME[i])); SX.bar(b, km(b, THEME[i], -1)); AS.bar(b, km(b, THEME[i]) if i >= 4 else "R:4")
        TB.bar(b, km(b, TAIL[i], -1) if TAIL[i] != "R:4" else km(b, THEME[i], -1))
    elif n.startswith("呼びこみ"):                                 # 声2小節（太鼓とスーザフォンだけ）→ 管の返事2小節
        two = n.endswith("2")
        D.set(b, *(LT_A if i % 4 == 0 else LT_B if i % 4 == 1 else ST_A if i % 4 == 2 else ST_B)); tuba(b, ("light", "lightB", "funkA", "funkB")[i % 4])
        clap(b)
        if i in (2, 3): horns(b, ANS1[i - 2], alto=two)
        if i in (6, 7): horns(b, ANS2[i - 6], alto=two)
        if i in (0, 4) and two: stab(b, OFF, 60, alto=False)
    elif n.startswith("歌"):                                       # 歌。行のうしろの2拍に合いの手（1番 アルト・2番 トロンボーン）
        two = n.endswith("2")
        D.set(b, *(LT_A if i % 2 == 0 else LT_B)); tuba(b, ("light", "lightB", "two", "lightB")[i % 4] if not last else "walk")
        if i % 2 == 1:
            f = FILL[i // 2] if not two else FILL[(i // 2 + 2) % 4]
            (TB if two else AS).bar(b, km(b, f, -1 if two else 0))
        elif two: stab(b, OFF, 60, alto=False)
        if last: D.set(b, LT_B[0], "..o.x.o...xxXXXX", LT_B[2])
    elif n.startswith("まけた"):                                   # 1小節め: 頭の1発で全員止まり、声だけ。2小節め: 小太鼓の連打と、次の調へのぼる管
        if i == 0:
            D.set(b, "X...............", "X...............", "................"); tuba(b, "hit"); stab(b, "x:0.5 R:3.5", 62); TP.bar(b, f"{nm(sorted(voice(root(b), 70, 3))[2])}:0.5 R:3.5")
        else:
            D.set(b, *ROLL); r = low(S.chords[b], "G1"); TU.bar(b, f"R:2 {nm(r)}:0.5 {nm(r + 2)}:0.5 {nm(r + 4)}:0.5 {nm(r + 6)}:0.5")
            stab(b, "R:2 x:2", 62); TP.bar(b, f"R:2 {nm(sorted(voice(root(b), 72, 3))[2])}:2")
    elif n.startswith("サビ") or n == "最後のサビ":
        lv = {"サビ1": 1, "サビ2": 2, "最後のサビ": 3}[n]; j = i % 8
        D.set(b, *(CH_A if i % 2 == 0 else CH_B)); tuba(b, ("funkA", "funkB", "funkC", "funkB")[i % 4] if j != 7 else ("walk" if not last else "long"))
        if j in CANS: TP.bar(b, km(b, CANS[j]))
        if j % 2 == 0: stab(b, OFF2 if lv >= 2 else OFF, 62, alto=lv < 3)
        else: stab(b, LONG if j != 7 else "x:1 R:3", 62, alto=lv < 3)
        if lv >= 2: clap(b)
        if lv == 3: AS.bar(b, km(b, OBB[i % 4]))                    # 最後だけ、アルトサックスが別の線で歌う（みんなが同時に別のことを吹く）
        if lv == 3 and i >= 8 and j % 2 == 0: TP.bar(b, km(b, "R:1 1':0.5 R:0.5 1':0.5 R:0.5 2':0.5 R:0.5"))   # 2回めは、トランペットが歌の下で短く打つ
        if j == 7 and not last: D.set(b, CH_B[0], "o.o.X.oxooxxXXXX", CH_B[2])
    elif n == "楽隊の番":
        D.set(b, *(SO_A if i % 2 == 0 else SO_B)); tuba(b, ("funkC", "funkB", "funkA", "funkB")[i % 4] if i < 11 else "walk"); clap(b)
        if i < 4: TB.bar(b, km(b, TSOLO[i], 0 if i != 2 else -1)); SX.bar(b, "R:4")
        elif i < 8:
            who, line = TRADE[i - 4]; (TP if who == "TP" else AS).bar(b, km(b, line)); stab(b, OFF, 58, alto=False)
        else:
            horns(b, SHOUT[i - 8], alto=True)
            if i == 11: D.set(b, SO_B[0], "X...X.x.X...XXXX", "................")
    elif n == "しずかな通り":                                     # スーザフォンと手拍子と声だけ
        tuba(b, "two" if i % 2 == 0 else "light"); clap(b)
        if i >= 6: D.set(b, "X...............", "................" if i == 6 else "........ooooxxxx", "................")
    elif n == "手じめ":                                           # 楽器なし。声と手拍子 → 3拍めで全員1発
        if i in (0, 2, 4): clap(b)
        if i in (1, 3): clap(b, (0, 0.5, 1, 2, 2.5, 3), 0.5)
        if i == 5:
            clap(b, (0, 0.5, 1), 0.5); D.set(b, "........X.......", "........X.......", "................")
            v = sorted(voice(root(b), 65, 3)); TU.bar(b, f"R:2 {nm(low(S.chords[b], 'G1'))}:1.5 R:0.5")
            for tr, m in ((TB, v[0] - 12), (SX, v[1] - 12), (AS, v[2]), (TP, v[2] + 5)): tr.bar(b, f"R:2 {nm(m)}:1.5 R:0.5")

S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の19（18時）。街を歩く楽隊のブラスバンド・ファンク（102）。B♭→B→C→D♭。閉店セールの日、商店街がいちばんにぎやかになる。"
          "「まけた！」のたびに全員が止まって調が上がる。トランペット・アルトとテナーのサックス・トロンボーン・スーザフォン・小太鼓と大太鼓・手拍子。ギター・ピアノ・電子の音はなし。自作")
finish(S, LY, V, 0)

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "トランペット", mid=88, down=10, up=8, seed=3); humanize(path, "サックス", mid=84, down=10, up=8, seed=5); humanize(path, "トロンボーン", mid=86, down=10, up=8, seed=7); humanize(path, "スーザフォン", mid=88, down=8, up=8, seed=9)
set_parts(path, "キック", volume=0.16); set_parts(path, "スネア", swing16=0.12, volume=0.09)   # 3 回め: テーマで太鼓 −23.7・管 −26.5 → 太鼓を 2dB 下げ、管を 1.5dB 上げる; set_parts(path, "ハイハット", swing16=0.12)      # きっちりと、はねたリズムの「あいだ」
final_gain(path, {"最後のサビ": 1.0})   # 3 回め: 最後のサビ −14.3 が サビ2 −14.1 より小さかった（上げるのは 1.5dB まで）
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 10, "bridge": 10, "chorus": 20, "最後のサビ": 24, "outro": 10}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, KEYS[2]), ("最後のサビ", 0, None, KEYS[3]), ("手じめ", 0, None, KEYS[3])], vol=0.34)
    voice_by_scene(path, S, {}, default="cute")       # 1 曲 1 種類の声（2026-11-17 人間）
    sing_ends(path, S, max_len=2.0, throw=0.2)
    js = load(path)
    for v in js.get("vocals", []):
        v["debreath"] = 0.5; v["softCons"] = 0.3
        v["debreathAt"] = [[t + 0.03, 1.2] for t in [179.09, 108.75, 115.16, 120.46, 113.47, 185.25]]   # 息の点検（tools/vt3/breath_check.py）が「音の中」と言った所だけ、追加で息の音を下げる
    save(path, js)
