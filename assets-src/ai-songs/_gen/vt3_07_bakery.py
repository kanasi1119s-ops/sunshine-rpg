# vt3 07「焼きたてのオーブン」Fresh Out of the Oven（仮）— ピアノのボサノバ → ピアノハウス（ギターなし）。118・4/4。A長調。
# 第3弾（0時〜24時の街）の 6時。表は docs/sound/vt3-plan.md。
#
# v5（2026-11-13）: ゼロから作り直し（人間「全ての曲を1みたいにこだわって作って」「このレベル（02 v7）まで詰めて曲作って」）。
#   v1〜v4 はナイロンギターのボサノバとフルート。ギターは使わず（ギターに聞こえない音は使わない決まり）、フルートも使わない（指定がない限り使わない決まり）。
#   ボサノバの弾き方は、ピアノの左手（低い音）と右手（ずらした和音）に分けて弾く。合いの手はマリンバとカリンバ。
#
# 物語: 町のパン屋の朝。まだ暗い店で、ゆうべ寝かせた生地がふくらんでいる。となりのラジオの小さな鼻歌（1時の節）をまねしながら生地をこねる。
#   オーブンの「チン」。いちばん最初のパンが焼ける。ランドセルの子が窓をのぞいて手をふる。扉を開けて、今日のはじまりを手わたす。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: 生地がふくらむのといっしょに、町じゅうの朝がふくらむ。手のひらの下で朝が育つ。
#
# 曲を決める表（書く前に similar_check.py --plan で確かめた: いちばん近い曲でも近さ 29%）:
#   形: オーブンの「チン」→ ピアノだけのボサノバ → Aメロ1（ピアノ・縁をたたく音・細かいハイハット。後半からマリンバ）→ Bメロ（のぼる）
#       → サビ1（「チン」と同時に4つ打ちのハウスに入れかわる）→ 間奏（マリンバが合いことばの節）→ Aメロ2（ボサノバにもどる・カリンバ）→ Bメロ2 → サビ2
#       → 寝かせる（カリンバと声だけ。「待つのも仕事だ」）→ 間奏2（ハウスのピアノの上でマリンバが歌う）→ 最後のサビ → ドアベル（2つの音）
#   旋律: Aメロ＝句の頭を1拍半おくらせる、ささやく7音の句。Bメロ＝8分の弱起から4分でのぼる。
#         サビ＝「ふ・く・ら・めー」を同じ形で2回（和音に合わせて下がる）→ 高い所で長い句。サビは ii の和音から始まる
#   和音: Aメロ I △7 → ii → V7。Bメロ IV → iii → ii → iii。サビ ii → V7 → I → VI7（ii へもどる回り方）、最後は IV → #IVdim → Vsus → V7 で宙に浮く
#   ベース: Aメロはピアノの左手（1拍目と3拍目、その前に短い音）。サビだけベースが入り、キックのない裏拍で鳴る
#   この曲だけ: ①オーブンの「チン」が曲を切りかえる合図 ②同じピアノがボサノバからハウスへ変わる ③「寝かせる」場面 ④ドアベルで終わる
#
# ボサノバの作り方（2026-11-13 に調べた。ujam.com / beatkey / soundbrenner.com / pianogroove.com / thejazzpianosite.com）:
#   ボサノバは「低い音の型・ずらした和音の型・旋律」の3つの層でできている。低い音はまっすぐ（1拍目と3拍目）、和音はその間にずらして入れ、少し前に食う。
#   縁をたたく音（クロススティック）が2小節の型（ボサノバのクラーベ）を打ち、ハイハットかシェイカーがまっすぐ刻む。和音は 7th・9th を使う。
#   ギターの弾き方をまねるときは、低い音と和音を別のパートに分ける（1つの和音をまとめて鳴らすと、かき鳴らしに聞こえる）。
from vt25_lib import *

S = Song("07", "bakery", "焼きたてのオーブン（仮）", "Fresh Out of the Oven", 118, 4, "A", "major", "ピアノのボサノバ・ハウス（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
S.keepers = {}
K = Key("A", "major")          # oct 3 で 1 = A3

A_CH = ["Amaj7", "Amaj7", "Bm7", "E7", "Amaj7", "F#m7", "Bm7", "E7"]
B_CH = ["Dmaj7", "C#m7", "Bm7", "C#m7", "Dmaj7", "C#m7", "Bm7", "E7sus4"]
C_CH = ["Bm7", "E7", "Amaj7", "F#7", "Bm7", "E7", "C#m7", "F#m7", "Bm7", "E7", "Amaj7", "F#7", "Dmaj7", "D#dim", "E7sus4", "E7"]

S.scene("チン", 8, "intro", ["Amaj7", "Amaj7"] + A_CH[2:])
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 4, "break", ["Amaj7", "F#m7", "Bm7", "E7"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("寝かせる", 8, "bridge", ["F#m7", "F#m7", "Dmaj7", "Dmaj7", "Bm7", "Bm7", "E7sus4", "E7"])
S.scene("間奏2", 8, "solo", C_CH[:8])
S.scene("最後のサビ", 24, "chorus", C_CH + C_CH[8:])
S.scene("ドアベル", 4, "outro", ["Amaj7", "Dmaj7", "Amaj7", "Amaj7"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)
PL = S.track("ピアノ（左手の低い音）", "piano", volume=0.13, pan=-0.1, reverb=0.2, sustain=0.9)
PR = [S.track(f"ピアノ（右手の和音{i + 1}）", "piano", volume=0.085, pan=-0.1, reverb=0.22, sustain=0.6,
              fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 900, "high": 1}]) for i in range(3)]
MAR = S.track("マリンバ", "lead", patch="marimba", volume=0.1, pan=0.35, reverb=0.3)
KAL = S.track("カリンバ", "lead", patch="kalimbaReal", volume=0.085, pan=-0.4, reverb=0.4, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])
GLK = S.track("オーブンのチン・ドアベル（鉄琴）", "glockenspiel", volume=0.1, pan=0.15, reverb=0.4)
STR = [S.track(f"弦{i + 1}", "strings", patch="stringEnsemble", volume=0.04, pan=-0.4 + 0.8 * i, reverb=0.4, sustain=1.4) for i in range(2)]
BASS = S.track("ベース（指弾き・丸い音）", "bass", sustain=0.8, **dict(finger_bass_spec(vol=0.2), fx=[{"type": "eq", "low": 1, "mid": 1, "midHz": 800, "high": -3}, {"type": "filter", "kind": "lowpass", "freq": 1500, "q": 0.6}]))
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.03, pan=0, duck=0.5)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# Aメロ（前半）: 句の頭を1拍半おくらせる。7つの音でささやく
VA = ["R:1.5 3:0.5 5:0.5 5:1 3:0.5", "5:0.5 6:1 5:1.5 R:1", "R:1.5 4:0.5 6:0.5 6:1 4:0.5", "4:0.5 5:1 2:1.5 R:1",
      "R:1.5 5:0.5 1':0.5 1':1 7:0.5", "6:0.5 1':1 6:1.5 R:1", "R:1.5 2:0.5 4:0.5 6:1 4:0.5", "2:0.5 4:1 5:1.5 R:1"]
# Aメロ（後半）: 1拍おくれて5つ → 長い音2つ
VA2 = ["R:1 3:0.5 5:0.5 5:1 6:0.5 5:0.5", "3:1 5:1.5 R:1.5", "R:1 4:0.5 6:0.5 6:1 1':0.5 6:0.5", "5:1 7:1.5 R:1.5",
       "R:1 5:0.5 1':0.5 1':1 2':0.5 1':0.5", "6:1 1':1.5 R:1.5", "R:1.5 6:0.5 4:0.5 2:1 4:0.5", "5:0.5 7:1 2':1.5 R:1"]
A1 = ("まだくらいみせ/こむぎのにおい/ゆうべのきじが/ふくらんでいる/"
      "えぷろんしめて/こなをはたいて/となりのらじお/ちいさくうたう")
A2 = "はなうたまねて/きじをこねれば/てのひらのした/あさがそだつよ"
VB = ["R:0.5 6:0.5 6:0.5 1':0.5 1':1 6:1", "5:1 7:1 5:1 R:1", "R:0.5 4:0.5 4:0.5 6:0.5 6:1 4:1", "5:1 7:1 2':1 R:1",
      "R:0.5 6:0.5 6:0.5 1':0.5 3':1 1':1", "2':1 7:1 5:1 R:1", "R:0.5 4:0.5 6:0.5 1':0.5 2':1 1':1", "2':3 R:1"]
B1 = "いちばんさいしょの/ぱんがやけるまで/まだねむるまちを/かおりでよぶ"
B2 = "らんどせるのこが/まどをのぞいてく/ちいさなてをふる/うれしくなる"
# サビ: 「ふくらめ」を同じ形で2回（和音に合わせて下がる）→ 高い所の長い句
VC = ["2':0.5 2':0.5 1':0.5 6:1.5 R:1", "2':0.5 2':0.5 1':0.5 7:1.5 R:1", "R:1 3':0.5 3':0.5 2':0.5 3':1 2':0.5", "6:1 #1':1 3':1 R:1",
      "2':0.5 2':0.5 4':0.5 2':1.5 R:1", "2':0.5 2':0.5 5':0.5 4':1.5 R:1", "R:1 3':0.5 3':0.5 5':0.5 3':1 2':0.5", "1':1 3':1 1':1 R:1",
      "2':0.5 2':0.5 1':0.5 6:1.5 R:1", "2':0.5 2':0.5 1':0.5 7:1.5 R:1", "R:1 3':0.5 3':0.5 2':0.5 3':1 2':0.5", "6:1 #1':1 3':1 R:1",
      "R:0.5 6:0.5 1':0.5 3':0.5 4':1 3':1", "6:1 1':1 1':1.5 R:0.5", "2':0.5 2':0.5 1':0.5 2':1.5 R:1", "R:4"]
C1 = "ふくらめ/ふくらめ/きょうがやきあがる/もうすぐ/もうすぐ/まちじゅうのあさが/ふくらめ/ふくらめ/ゆげがまどをぬけ/あまいかぜになる/ふくらめ"
C2 = "ふくらめ/ふくらめ/ちいさなゆめたち/やけたよ/やけたよ/ひとつずつどうぞ/ふくらめ/ふくらめ/てのひらのうえで/ぬくもりがのこる/ふくらめ"
C3 = ("ふくらめ/ふくらめ/とびらをひらけば/やけたよ/やけたよ/あさのひかりごと/ふくらめ/ふくらめ/はなうたまぜこみ/こんがりやけたよ/ふくらめ/"
      "ふくらめ/ふくらめ/きょうのはじまりを/てわたしにいこう/ふくらめ")
VBR = ["R:2 6:1 1':1", "3':2 1':1 R:1", "R:2 4:1 6:1", "1':2 6:1 R:1", "R:2 2:1 4:1", "6:2 4:1 R:1", "R:1 2':1 1':1 2':1", "2':3 R:1"]
CB = "しずかに/ねかせて/まつのも/しごとだ"
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA2, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA2, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("寝かせる", VBR, CB)
put("最後のサビ", VC + VC[8:], C3)

# ================= ピアノ（左手の低い音と、右手のずらした和音を分ける）=================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]
BOSSA_A = "x:0.5 R:1 x:0.5 R:0.5 x:0.5 R:1"                 # 右手: 1拍目・2拍目の裏・3拍目の裏
BOSSA_B = "R:0.5 x:0.5 R:0.5 x:0.5 R:1 x:0.5 R:0.5"         # 右手: 裏・裏・4拍目
HOUSE_A = "x:0.75 x:0.75 x:1 x:0.5 x:1"                     # ハウスのピアノ（3・3・4・2・4 の16分）
HOUSE_B = "R:0.5 x:0.75 x:0.75 x:0.5 R:0.5 x:1"
LONG = "x:4"


def rh(b, pat, c=64):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): PR[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def lh(b, style="bossa"):
    r = low(S.chords[b], "E2"); up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7)
    PL.bar(b, {"bossa": f"{nm(r)}:1.5 {nm(r)}:0.5 {nm(t5)}:1.5 {nm(t5)}:0.5",     # 1拍目と3拍目、その前に短い音
               "one": f"{nm(r)}:3.5 R:0.5", "two": f"{nm(r)}:2 {nm(t5)}:2"}[style])


def strs(b, c=69):
    v = sorted(voice(root(b), c, 3)); STR[0].bar(b, f"{nm(v[0])}:4"); STR[1].bar(b, f"{nm(v[2])}:4")


def mar(b, order, lo="E4", hi="E6", L=0.5, lead="R:2"):
    tn = tones(root(b), lo, hi); MAR.bar(b, lead + " " + " ".join(f"{nm(tn[q % len(tn)])}:{L:g}" for q in order))


MOTIF = "R:1 C#5:0.5 E5:0.5 F#5:1 E5:0.5 B4:0.5"            # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "チン":
        if i == 0: GLK.bar(b, "A6:4")                                     # オーブンの「チン」
        if i >= 2: lh(b); rh(b, BOSSA_A if i % 2 == 0 else BOSSA_B)
        elif i == 1: rh(b, "R:2 x:2")
        if i == 7: mar(b, (0, 1, 2, 3))
    elif n in ("Aメロ1", "Aメロ2"):
        lh(b); rh(b, BOSSA_A if i % 2 == 0 else BOSSA_B)
        if n == "Aメロ1" and i >= 8 and i % 2 == 1: mar(b, (2, 3, 4, 3) if i % 4 == 1 else (4, 3, 2, 1), lead="R:2")      # 後半: 句の終わりにマリンバが答える
        if n == "Aメロ2":
            tn = tones(root(b), "A4", "A6"); KAL.bar(b, f"R:0.5 {nm(tn[1])}:0.5 R:1 {nm(tn[3])}:0.5 {nm(tn[2])}:0.5 R:1" if i % 2 == 0 else f"R:2.5 {nm(tn[2])}:0.5 {nm(tn[4 % len(tn)])}:1")
    elif n in ("Bメロ1", "Bメロ2"):
        lh(b, "two"); rh(b, BOSSA_A if i < 6 else ("x:1 x:1 x:1 x:1" if i == 6 else "x:2 R:2"), 64 + i)
        strs(b, 66 + i)
        if n == "Bメロ2" and i % 2 == 1 and i < 7: mar(b, (1, 2, 3, 4))
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        j = i if i < 16 else i - 8
        rh(b, HOUSE_A if j % 2 == 0 else HOUSE_B, 66)
        if i == 0: GLK.bar(b, "A6:4")                                     # 「チン」と同時にハウスへ
        if n != "サビ1" or j >= 8: strs(b, 71)
        # マリンバ: 歌が休む所（「ふくらめ」のあとの1拍）で答える。サビ2 からは長い句のあとにも
        if j in (0, 1, 4, 5, 8, 9, 14): mar(b, (3, 4), lead="R:3")
        elif n != "サビ1" and j in (3, 7, 11): mar(b, (4, 5), lead="R:3")
        if j == 15: mar(b, (0, 1, 2, 3, 4, 5, 6, 7), lead="")              # サビの最後の小節: マリンバがかけ上がる
        if n == "最後のサビ":
            tn = tones(root(b), "A5", "A6"); KAL.bar(b, f"{nm(tn[0])}:1 {nm(tn[-1])}:1 {nm(tn[1 % len(tn)])}:1 {nm(tn[-1])}:1")
    elif n == "間奏":
        lh(b); rh(b, BOSSA_A if i % 2 == 0 else BOSSA_B)
        MAR.bar(b, [MOTIF, "R:2 A4:0.5 C#5:0.5 E5:1", "R:1 D5:0.5 F#5:0.5 A5:1 F#5:0.5 D5:0.5", "E5:1 G#5:1 B5:2"][i])
    elif n == "寝かせる":                                                  # カリンバと、ピアノの長い音だけ
        lh(b, "one")
        tn = tones(root(b), "A4", "A6"); KAL.bar(b, " ".join(f"{nm(tn[q % len(tn)])}:0.5" for q in ((0, 2, 4, 2) if i % 2 == 0 else (1, 3, 5, 3))) + " R:2")
        if i >= 6: rh(b, LONG, 64 + i); strs(b, 62 + i)
    elif n == "間奏2":                                                    # ハウスのピアノの上で、マリンバが歌う
        rh(b, HOUSE_A if i % 2 == 0 else HOUSE_B, 66); strs(b, 69)
        MAR.bar(b, ["B4:0.5 D5:0.5 F#5:1 E5:0.5 D5:0.5 B4:1", "G#4:0.5 B4:0.5 E5:1 D5:1 B4:1", "C#5:0.5 E5:0.5 A5:1 G#5:0.5 E5:0.5 C#5:1", "A#4:0.5 C#5:0.5 E5:0.5 F#5:0.5 A#5:1 R:1",
                    "F#5:0.5 D5:0.5 B4:0.5 D5:0.5 F#5:0.5 A5:0.5 F#5:1", "E5:0.5 G#5:0.5 B5:1 G#5:1 E5:1", "C#5:0.5 E5:0.5 G#5:0.5 B5:0.5 G#5:1 E5:1", "F#5:0.5 A5:0.5 C#6:1 A5:1 R:1"][i])
    elif n == "ドアベル":
        if i < 2: lh(b); rh(b, BOSSA_A if i == 0 else BOSSA_B)
        elif i == 2: lh(b, "one"); rh(b, LONG, 64); GLK.bar(b, "R:1 E6:1.5 C#6:1.5")       # ドアベル（2つの音）
        else: rh(b, "x:2 R:2", 69)

# ================= ベース（サビだけ。キックのない裏拍で鳴る。共通の部品 bass_line は使わない）=================
def bl(b, style):
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t3 = next((m for m in up if (m - r) in (3, 4)), r + 4)
    o = r + 12; ap = t5 if rn == r else (rn - 1 if rn > r else rn + 1)
    N = nm
    return {"off": f"R:0.5 {N(r)}:0.5 R:0.5 {N(r)}:0.5 R:0.5 {N(r)}:0.5 R:0.5 {N(t5)}:0.5",
            "off_b": f"R:0.5 {N(r)}:0.5 R:0.5 {N(o)}:0.5 R:0.5 {N(r)}:0.5 {N(t3)}:0.25 {N(t5)}:0.25 {N(ap)}:0.5",
            "off_c": f"{N(r)}:0.5 {N(r)}:0.5 R:0.5 {N(o)}:0.5 R:0.5 {N(t5)}:0.5 R:0.5 {N(ap)}:0.5",
            "long": f"{N(r)}:3.5 R:0.5"}[style]


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "サビ1": BASS.bar(b, bl(b, "off" if i % 2 == 0 else "off_b"))
    elif n in ("サビ2", "間奏2"): BASS.bar(b, bl(b, "off_c" if i % 4 == 2 else ("off" if i % 2 == 0 else "off_b")))
    elif n == "最後のサビ": BASS.bar(b, bl(b, "off_c" if i % 2 == 0 else "off_b"))
    elif n == "寝かせる" and i >= 6: BASS.bar(b, bl(b, "long"))
    if n in ("サビ2", "間奏2", "最後のサビ"): SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:0.5 R:3.5")

# ================= ドラム（Aメロ＝ボサノバ: 縁をたたく音の2小節の型。サビ＝4つ打ちのハウス）=================
CLAVE = ("x.....x.....x...", "....x.....x.....")     # ボサノバのクラーベ（3 つ ＋ 2 つ）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "チン":
        if i >= 4: D.set(b, "................", CLAVE[i % 2], "x.x.x.x.x.x.x.x.")
    elif n == "Aメロ1":
        D.set(b, "................" if i < 8 else "X.....x.X.....x.", CLAVE[i % 2], "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "small")
    elif n in ("Aメロ2", "間奏"):
        D.set(b, "X.....x.X.....x.", CLAVE[i % 2], "x.xxx.xxx.xxx.xx" if n == "Aメロ2" else "x.x.x.x.x.x.x.x.")
        if last and n == "Aメロ2": put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6: D.set(b, "X.......X......." if i < 4 else "X...X...X...X...", CLAVE[i % 2], "x.x.x.x.x.x.x.x.")
        elif i == 6: D.set(b, "X...X...X...X...", "....X...X.X.XXXX", "................")
        else: halt(D, b, 2); D.K[b] = "X...X..........."; D.S[b] = "X...X..........."
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏2"):
        hh = "..X...X...X...X." if n == "サビ1" else "xxXxxxXxxxXxxxXx"                 # サビ1 は裏拍だけ、サビ2 からシェイカーのように16分
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X...X...X...X...", s="....X.......X..." if i % 4 != 3 else "....X.......X.x.", h=hh, vary=False)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if last and n in ("サビ1", "サビ2"): put_fill(D, b, "small")
        if last and n == "間奏2": halt(D, b, 3)
    elif n == "寝かせる":
        if i >= 4: D.set(b, "................", CLAVE[i % 2] if i < 7 else "....x...x.x.xxxx", "................")
    elif n == "ドアベル":
        if i < 2: D.set(b, "X.....x.X.....x.", CLAVE[i % 2], "x.x.x.x.x.x.x.x.")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# 止め: Bメロ の8小節目は、頭の2拍のあと全員休み → サビの頭の「チン」
for nme in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(nme)[-1], 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の07（6時）。ピアノのボサノバ → ピアノハウス（ギターなし）。A・118。町のパン屋の朝、いちばん最初のパンが焼ける。"
          "オーブンの「チン」でボサノバから4つ打ちのハウスに入れかわる。ピアノ・マリンバ・カリンバ・鉄琴。ドアベルで終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"寝かせる": -0.5, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ピアノ（右手", mid=82, down=10, up=8, seed=3); humanize(path, "マリンバ", mid=84, down=8, up=8, seed=5); humanize(path, "カリンバ", mid=82, down=8, up=8, seed=7)
set_parts(path, "ハイハット", swing16=0.12)
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 22, "最後のサビ": 26, "bridge": 6}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 8, None, K)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.3
    save(path, js)
