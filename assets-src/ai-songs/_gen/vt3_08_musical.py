# vt3 08「満員電車ミュージカル」Rush-Hour Musical（仮）— ミュージカルのワルツ（3拍子）。156・3/4。C長調 → 最後のサビは D。
# 第3弾（0時〜24時の街）の 7時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-13）: ゼロから作り直し（人間「全ての曲を1みたいにこだわって作って」「このレベル（02 v7）まで詰めて曲作って」）。
#   v1〜v3 は 4拍子・168 の2ビートのショーチューン（ブラスの合いの手）。04（ホーン隊のスカ・176）と速さも主役の音も近くなるので、曲そのものを変える。
#   → ゆれる電車を「ワルツ」に見立てて、3拍子にする（このアルバムで 3/4 はこの曲だけ）。主役はクラリネットとピチカートの弦と鉄琴。
#
# 物語: 朝7時のぎゅうぎゅうの電車。ひじが当たり、つま先立ちで、だれかの肩を借りている。目をとじると、レールの音が三拍子に聞こえてくる。
#   となりの人の鼻歌（1時のラジオの節 3・5・6・5・2）。もしもここが大きな舞台なら ── 目をあけると、みんなが踊り子だった。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: つり革がシャンデリアに、ため息がコーラスに、ドアが開くのがカーテンコールになる。
#
# 曲を決める表（書く前に similar_check.py --plan で確かめた: いちばん近い曲でも近さ 21%）:
#   形: 発車のチャイム（鉄琴）→ ワルツの前奏 → Aメロ1（ピアノのズン・チャッ・チャッと語るような歌）→ Bメロ（「もしもね」・長い音）
#       → サビ1（「いち・に・さん」）→ 間奏 → Aメロ2（ピチカートの弦が加わる）→ Bメロ2 → サビ2 → ダンス（クラリネットのソロ）
#       → つり革（とても静か・弦だけ）→ 最後のサビ（D に上がる・いちばん大きい）→ カーテンコール（発車のチャイムで終わる）
#   旋律: Aメロ＝1拍おいて8分4つ → 次の小節で4分2つ（語るような「ぼやき」）。Bメロ＝4分でのぼって長い音。
#         サビ＝「いち・に・さん」をそのまま拍にのせる（8分2つ・4分・8分2つ）。同じ形を和音に合わせて2回 → 長い句で答える
#   和音: Aメロ I → VI7 → ii → V7 → I → III7 → vi → II7 V7（ショーチューンの回り方）。サビ IV → V7 → I → vi → ii → V7 → I → I7
#   ベース: 1拍目だけ（ズン）。偶数の小節は5度、句の終わりだけ3拍目で次の和音へ歩く
#   この曲だけ: ①3拍子（ゆれる電車＝ワルツ）②サビの「いち・に・さん」③クラリネットが歌のすき間で答える ④発車のチャイムで始まり、同じチャイムで終わる
#
# ミュージカルの編曲（2026-11-13 に調べた。musicalwriters.com「Orchestrating a New Musical」、supremetracks.com、alanbelkinmusic.com）:
#   木管は「色」＝歌の旋律のすき間に入る対旋律と合いの手として使う。歌と伴奏のあいだにすき間を作り、そこに小さな旋律を出し入れする。
#   ピチカートの弦は「音程のある打楽器」と考える。よく動くパートほど目立つので、うしろに置くパートは動かさない。場面の変わり目は編成を変えて区切る。
from vt25_lib import *

S = Song("08", "musical", "満員電車ミュージカル（仮）", "Rush-Hour Musical", 156, 3, "C", "major", "ミュージカルのワルツ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
S.keepers = {}
K = Key("C", "major")          # oct 4 で 1 = C4
KD = Key("D", "major")         # 最後のサビ（+2）

A_CH = ["C", "C", "A7", "A7", "Dm7", "Dm7", "G7", "G7", "C", "C", "E7", "E7", "Am", "Am", "D7", "G7"]
B_CH = ["Am", "Am", "Em", "Em", "F", "F", "G7sus4", "G7"]
C16 = ["F", "G7", "C", "Am", "Dm7", "G7", "C", "C7", "F", "G7", "Em7", "A7", "Dm7", "G7", "C", "C"]
C_CH = C16 + C16
LAST = [tr_chord(c, 2) for c in C_CH + C16]

S.scene("発車", 12, "intro", ["C", "C", "G7", "G7"] + ["C", "Am", "Dm7", "G7", "C", "Am", "Dm7", "G7"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 32, "chorus", C_CH)
S.scene("間奏", 8, "break", ["C", "Am", "Dm7", "G7", "C", "Am", "Dm7", "G7"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 32, "chorus", C_CH)
S.scene("ダンス", 16, "solo", C16)
S.scene("つり革", 16, "bridge", ["Am", "Am", "F", "F", "C", "C", "G7", "G7", "Am", "Am", "F", "F", "Dm7", "Dm7", "G7", "A7"])
S.scene("最後のサビ", 48, "chorus", LAST)
S.scene("カーテンコール", 8, "outro", ["D", "Bm", "Em7", "A7", "D", "D", "D", "D"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead" if VOCAL else "clarinet", low=False)
PL = S.track("ピアノ（左手・ズン）", "piano", volume=0.13, pan=-0.1, reverb=0.2, sustain=0.9)
PR = [S.track(f"ピアノ（右手・チャッチャッ{i + 1}）", "piano", volume=0.08, pan=-0.1, reverb=0.22, sustain=0.5) for i in range(3)]
PZ = [S.track(f"ピチカートの弦{i + 1}", "strings", patch="pizzicato", volume=0.07, pan=0.3 - 0.3 * i, reverb=0.3) for i in range(2)]
CL = S.track("クラリネット（合いの手）", "lead", patch="clarinet", volume=0.1, pan=0.25, reverb=0.3)
GLK = S.track("発車のチャイム（鉄琴）", "glockenspiel", volume=0.085, pan=0.3, reverb=0.4)
STR = [S.track(f"弦{i + 1}", "strings", patch="stringEnsemble", volume=0.045, pan=-0.45 + 0.45 * i, reverb=0.4, sustain=1.4) for i in range(3)]
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.05, pan=0.4 - 0.4 * i, reverb=0.3) for i in range(2)]
TIMP = S.track("ティンパニ", "lead", patch="timpani", volume=0.1, pan=-0.2, reverb=0.4)
BASS = S.track("ベース（指弾き・丸い音）", "bass", sustain=0.9, **dict(finger_bass_spec(vol=0.2), fx=[{"type": "eq", "low": 1, "mid": 0, "midHz": 800, "high": -4}, {"type": "filter", "kind": "lowpass", "freq": 1200, "q": 0.6}]))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# Aメロ: 1拍おいて8分4つ → 次の小節で4分2つ（語るような「ぼやき」）
VA = ["R:1 5:0.5 5:0.5 6:0.5 5:0.5", "3:0.5 5:1.5 R:1", "R:1 6:0.5 6:0.5 7:0.5 6:0.5", "#1:0.5 3:1.5 R:1",
      "R:1 4:0.5 4:0.5 6:0.5 4:0.5", "2:0.5 4:1.5 R:1", "R:1 5:0.5 7:0.5 2':0.5 7:0.5", "5:2.5 R:0.5",
      "R:1 1':0.5 1':0.5 2':0.5 1':0.5", "5:0.5 1':1.5 R:1", "R:1 7:0.5 7:0.5 2':0.5 7:0.5", "#5:0.5 7:1.5 R:1",
      "R:1 6:0.5 1':0.5 3':0.5 1':0.5", "6:0.5 1':1.5 R:1", "2:0.5 #4:0.5 6:1 1':1", "7:2.5 R:0.5"]
A1 = "あさのほーむ/ひとのなみだ/どあがしまる/ぎゅうぎゅうだ/ひじがあたる/つまさきだち/だれかのかた/かりている"
A2 = "めをとじたら/きこえてくる/れーるのおと/さんびょうし/となりのひと/はなうたして/あのふしだと/きがついた"
VB = ["6:1.5 1':0.5 3':1", "3':2.5 R:0.5", "5:1.5 7:0.5 2':1", "2':2.5 R:0.5", "4:0.5 6:0.5 1':1 1':1", "2':1 1':1 6:1 R:0", "2':1.5 2':0.5 2':1", "2':2.5 R:0.5"]
VB[5] = "2':1 1':1 6:0.5 R:0.5"
B1 = "もしもね/ここがね/おおきなぶたい/ならばね"
B2 = "めをあけ/みわたす/みんなおどりこ/なんだね"
# サビ（32小節）: 「いち・に・さん」を拍にのせる。同じ形を2回（和音に合わせて1段上）→ 長い句で答える
H1 = ["4:0.5 6:0.5 1':1 6:0.5 4:0.5", "5:0.5 7:0.5 2':1 7:0.5 5:0.5"]
H2 = ["6:0.5 1':0.5 3':1 1':0.5 6:0.5", "7:0.5 2':0.5 3':1 2':0.5 7:0.5"]
VC = (H1 + ["3':1 3':0.5 2':0.5 1':1", "6:0.5 1':1.5 R:1", "4:1.5 6:0.5 2':1", "7:1 2':0.5 1':0.5 7:1", "1':2.5 R:0.5", "R:3"]
      + H2 + ["3':1 2':0.5 7:0.5 5:1", "6:0.5 #1':1.5 R:1", "4:1.5 6:0.5 2':1", "2':1 7:0.5 5:0.5 7:1", "1':2.5 R:0.5", "R:3"]
      + H1 + ["3':1 3':0.5 2':0.5 1':1", "6:0.5 1':1.5 R:1", "4:1.5 6:0.5 2':1", "7:1 2':0.5 1':0.5 7:1", "1':2.5 R:0.5", "R:3"]
      + H1 + ["3':1.5 2':0.5 1':1", "#1':0.5 3':1.5 R:1", "4:1.5 6:0.5 2':1", "3':1.5 2':0.5 7:1", "1':2.5 R:0.5", "R:3"])
C1 = ("いちにさんいちにさんゆれるしゃない/ぶとうかいのよう/いちにさんいちにさんつりかわたち/しゃんでりあになる/"
      "いちにさんいちにさんかばんのなか/ゆめがおどりだす/いちにさんいちにさんどのひとも/みんながしゅやく")
C2 = ("いちにさんいちにさんおされるたび/あしなみがそろう/いちにさんいちにさんためいきまで/こーらすにかわる/"
      "いちにさんいちにさんつぎのえきで/まくがあがるから/いちにさんいちにさんかおあげて/すぽっとらいとへ")
C3 = ("いちにさんいちにさんどあがひらく/かーてんこーるだ/いちにさんいちにさんはくしゅのなか/それぞれのまちへ/"
      "いちにさんいちにさんはなうたまで/かばんにしのばせ/いちにさんいちにさんいってきます/きょうのぶたいへ/"
      "いちにさんいちにさんまんいんでも/わるくないあさだ/いちにさんいちにさんまたあした/おなじしゃりょうで")
# つり革（とても静か）: 長い音でのぼる
VBR = ["R:1.5 6:0.5 1':1", "3':3", "2':1.5 1':0.5 6:1", "1':2.5 R:0.5", "R:1.5 5:0.5 1':1", "3':3", "2':1.5 7:0.5 5:1", "7:2.5 R:0.5",
       "R:1.5 6:0.5 1':1", "3':3", "2':1.5 1':0.5 6:1", "1':2.5 R:0.5", "R:1.5 4:0.5 6:1", "2':3", "2':1.5 7:0.5 2':1", "3':2.5 R:0.5"]
CB = "つりかわゆれる/まどにあさひが/しらないだれか/おなじあさだね"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
put("つり革", K, VBR, CB)
put("最後のサビ", KD, VC + VC[16:], C3)

# ================= ワルツの伴奏（左手ズン・右手チャッチャッ）=================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]
OOM = "R:1 x:1 x:1"                     # チャッ・チャッ
OOM2 = "R:1 x:0.5 x:0.5 x:1"            # チャチャ・チャッ（サビ）
OOM3 = "R:1 x:1 x:0.5 x:0.5"


def rh(b, pat, c=64, tracks=None):
    v = sorted(voice(root(b), c, 3)); tr = tracks or PR
    for j in range(len(tr)): tr[j].bar(b, " ".join(t.replace("x", nm(v[j + (3 - len(tr))])) for t in pat.split()))


def lh(b, i, walk=False):
    r = low(S.chords[b], "E2"); up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7)
    PL.bar(b, f"{nm(r if i % 2 == 0 else t5)}:1 R:2" if not walk else f"{nm(r)}:1 R:1 {nm(t5)}:1")


def strs(b, c=67, L=3):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:{L:g}" + ("" if L == 3 else f" R:{3 - L:g}"))


def brass(b, pat, c=65):
    v = sorted(voice(root(b), c, 3)); BR[0].bar(b, pat.replace("x", nm(v[2]))); BR[1].bar(b, pat.replace("x", nm(v[0])))


def cl_fill(b, order, lo="G4", hi="G5", lead="R:1"):
    tn = tones(root(b), lo, hi); CL.bar(b, (lead + " " if lead else "") + " ".join(f"{nm(tn[q % len(tn)])}:0.5" for q in order))


def tr_line(line, semi):
    return " ".join(t if t.startswith("R") else f"{nm(midi(t.split(':')[0]) + semi)}:{t.split(':')[1]}" for t in line.split())


CHIME = ["E6:1 C6:1 G5:1", "C6:2 R:1", "D6:1 B5:1 G5:1", "D6:2 R:1"]        # 発車のチャイム
# クラリネットのソロ（ダンス）。11〜12小節目に合いことばの節（3・5・6・5・2 ＝ ミ・ソ・ラ・ソ・レ）
SOLO = ["A4:1 C5:1 F5:1", "D5:0.5 F5:0.5 G5:1 F5:0.5 D5:0.5", "E5:1.5 G5:0.5 C6:1", "A5:1 E5:1 C5:1",
        "D5:0.5 F5:0.5 A5:1 F5:1", "G5:1 B5:0.5 A5:0.5 G5:1", "E5:2 G5:1", "E5:0.5 G5:0.5 Bb5:1 G5:1",
        "A5:1 C6:1 A5:0.5 F5:0.5", "G5:0.5 B5:0.5 D6:1 B5:1", "R:1 E5:0.5 G5:0.5 A5:1", "G5:0.5 D5:1.5 R:1",
        "F5:1 A5:1 D6:1", "B5:0.5 A5:0.5 G5:1 F5:1", "E5:1 G5:1 C6:1", "C6:2 R:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "発車":
        if i < 4: GLK.bar(b, CHIME[i])
        else:
            lh(b, i); rh(b, OOM)
            if i >= 8: rh(b, OOM, 67, PZ); CL.bar(b, ["G5:1.5 E5:0.5 C5:1", "E5:1 A5:1 G5:1", "F5:1.5 D5:0.5 A4:1", "B4:1 D5:1 G5:1"][i - 8])
    elif n in ("Aメロ1", "Aメロ2"):
        lh(b, i, walk=(i % 4 == 3)); rh(b, OOM)
        if n == "Aメロ2": rh(b, OOM, 67, PZ)
        # クラリネットは、歌の句の終わり（4小節ごとの4小節目）の3拍目から、次の小節へ橋をかける
        if i % 4 == 3: cl_fill(b, (2, 3), lead="R:2")
        elif n == "Aメロ2" and i % 4 == 1: cl_fill(b, (3, 2), lead="R:2")
    elif n in ("Bメロ1", "Bメロ2"):
        lh(b, i); strs(b, 64 + i)
        if i < 6: rh(b, OOM if n == "Bメロ1" else OOM3)
        elif i == 6: rh(b, "x:1 x:1 x:1", 67); brass(b, "x:1 x:1 x:1", 67)
        else: rh(b, "x:1 R:2", 69); brass(b, "x:1 R:2", 69)
        if i == 7: TIMP.bar(b, "R:1 G2:0.5 G2:0.5 G2:0.25 G2:0.25 G2:0.25 G2:0.25")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        j = i % 16; big = n == "最後のサビ"
        lh(b, i, walk=(j % 4 == 3)); rh(b, OOM2 if j % 2 == 0 else OOM3, 66 if big else 64); rh(b, OOM, 69 if big else 67, PZ)
        if n != "サビ1" or i >= 16: strs(b, 71 if big else 69)
        # ブラス: 「いち・に・さん」の小節の頭にひとつ。サビ2 と最後のサビは答えの句の終わりにも
        if j in (0, 1, 8, 9): brass(b, "x:1 R:2", 67 if not big else 69)
        elif n != "サビ1" and j in (6, 14): brass(b, "R:1 x:0.5 x:0.5 x:1", 67 if not big else 69)
        # クラリネット: 歌が休む小節（8小節目・16小節目）で答える。4小節目の終わりにも短く
        if j == 7: cl_fill(b, (0, 1, 2, 3, 4, 5), lead="")
        elif j == 15: cl_fill(b, (5, 4, 3, 2, 1, 0), lead="")
        elif j in (3, 11) and n != "サビ1": cl_fill(b, (3, 4), lead="R:2")
        if j in (0, 8): GLK.bar(b, f"{nm(tones(root(b), 'C6', 'C7')[0])}:1 R:2")       # 鉄琴が1拍目にきらり
        if big and i >= 32 and j % 2 == 0: GLK.bar(b, f"{nm(tones(root(b), 'D6', 'D7')[0])}:1 {nm(tones(root(b), 'D6', 'D7')[1])}:1 R:1")
    elif n == "間奏":
        lh(b, i); rh(b, OOM); rh(b, OOM, 67, PZ)
        CL.bar(b, ["G5:1.5 E5:0.5 C5:1", "E5:1 A5:1 G5:1", "F5:1.5 D5:0.5 A4:1", "B4:1 D5:1 G5:1", "E5:1 G5:1 C6:1", "A5:1.5 G5:0.5 E5:1", "F5:0.5 A5:0.5 D6:1 A5:1", "G5:2 R:1"][i])
    elif n == "ダンス":
        lh(b, i, walk=(i % 4 == 3)); rh(b, OOM2 if i % 2 == 0 else OOM3); rh(b, OOM, 67, PZ)
        CL.bar(b, SOLO[i])
        if i >= 8: strs(b, 69)
        if i == 15: TIMP.bar(b, "C3:1 R:2")
    elif n == "つり革":                                           # 弦の長い音と、ピチカートが1拍目だけ
        strs(b, 62 + i // 4)
        PZ[1].bar(b, f"{nm(low(S.chords[b], 'C3'))}:1 R:2")
        if i >= 8 and i % 2 == 1: GLK.bar(b, f"R:1 {nm(tones(root(b), 'C6', 'C7')[1])}:2")
        if i == 14: brass(b, "x:3", 64)
        if i == 15: brass(b, "x:2 R:1", 66); TIMP.bar(b, "A2:0.5 A2:0.5 A2:0.25 A2:0.25 A2:0.25 A2:0.25 R:1")
    elif n == "カーテンコール":
        if i < 4:
            lh(b, i); rh(b, OOM2, 66); rh(b, OOM, 69, PZ); strs(b, 71)
            CL.bar(b, tr_line(["G5:1.5 E5:0.5 C5:1", "E5:1 A5:1 G5:1", "F5:1.5 D5:0.5 A4:1", "B4:1 D5:1 G5:1"][i], 2))
        elif i < 6: GLK.bar(b, tr_line(CHIME[i - 4], 2)); strs(b, 66)
        elif i == 6: rh(b, "x:1 R:2", 69); brass(b, "x:1 R:2", 69); lh(b, 0); TIMP.bar(b, "D3:1 R:2")

# ================= ベース（1拍目だけ。句の終わりは3拍目で次の和音へ歩く）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7)
    ap = t5 if rn == r else (rn - 1 if rn > r else rn + 1)
    t3 = next((m for m in up if (m - r) in (3, 4)), r + 4)
    one = f"{nm(r)}:1 R:0.5 {nm(t5)}:0.5 {nm(t3 + 12)}:1" if i % 4 == 0 else f"{nm(r)}:1 R:1 {nm(t3)}:0.5 {nm(t5)}:0.5"          # ズン・（ン）ズ・ター: 1拍目のあと、2拍目の裏から5度へ
    walk = f"{nm(r)}:1.5 {nm(t3)}:0.5 {nm(ap)}:1"                # 句の終わりは歩いて次の和音へ
    alt = f"{nm(t5)}:1 R:1 {nm(r)}:0.5 {nm(t3)}:0.5"
    if n == "Aメロ2" or (n == "Aメロ1" and i >= 8): BASS.bar(b, walk if i % 4 == 3 else one)
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, f"{nm(r)}:2 {nm(t5)}:1" if i < 7 else f"{nm(r)}:1 R:2")
    elif n in ("サビ1", "サビ2", "最後のサビ", "ダンス", "間奏"): BASS.bar(b, walk if i % 4 == 3 else (one if i % 2 == 0 else alt))
    elif n == "発車" and i >= 8: BASS.bar(b, one)
    elif n == "つり革" and i >= 8: BASS.bar(b, f"{nm(r)}:2.5 R:0.5")
    elif n == "カーテンコール" and i < 4: BASS.bar(b, walk if i == 3 else one)
    elif n == "カーテンコール" and i == 6: BASS.bar(b, f"{nm(r)}:1 R:2")

# ================= ドラム（3拍子・12マス。Aメロは軽く、サビは2・3拍目のスネア）=================
W_SOFT = ("X...........", "....x...x...", "x...x...x...")
W_MID = ("X...........", "....x...x...", "x.x.x.x.x.x.")
W_BIG = ("X.........x.", "....X...X...", "x.x.x.x.x.x.")
W_FILL = ("X...........", "....X.X.XXXX", "x...........")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "発車" and i >= 4: D.set(b, *(W_SOFT if i < 11 else W_FILL))
    elif n == "Aメロ1": D.set(b, *(("............", "....x...x...", "............") if i < 8 else W_SOFT))
    elif n in ("Aメロ2", "間奏"): D.set(b, *(W_FILL if (last and n == "間奏") else W_MID))
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6: D.set(b, "X...........", "............", "x...x...x...")
        elif i == 6: D.set(b, "X...X...X...", "X...X...X.X.", "............")
        else: D.set(b, "X...........", "X...........", "............")
    elif n in ("サビ1", "サビ2", "最後のサビ", "ダンス"):
        j = i % 16
        D.set(b, *(W_FILL if (j == 15 and not last) or (last and n != "最後のサビ") else (W_BIG if (n != "サビ1" or i >= 16) else W_MID)))
        if j == 0: crash(D, b, "C2", 6 if n == "最後のサビ" else 3)
    elif n == "カーテンコール":
        if i < 4: D.set(b, *(W_BIG if i < 3 else W_FILL))
        if i == 0: crash(D, b, "C2", 3)
        if i == 6: D.set(b, "X...........", "X...........", "............"); crash(D, b, "C2", 6)

cym_swell(CYM, S.sc("サビ1")[0], 3, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 3, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 3, "E4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の08（7時）。ミュージカルのワルツ（3拍子）。C→D・156。ぎゅうぎゅうの電車のゆれがワルツになり、車内が舞台になる。"
          "サビは「いち・に・さん」。ピアノのズン・チャッ・チャッ、ピチカートの弦、クラリネット、鉄琴、ブラス、ティンパニ。発車のチャイムで始まり、同じチャイムで終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"つり革": -0.5, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ピアノ（右手", mid=82, down=10, up=8, seed=3); humanize(path, "ピチカート", mid=84, down=8, up=8, seed=5); humanize(path, "クラリネット", mid=86, down=8, up=8, seed=7)
# v4 を測ると、最後のサビ（−14.6）が サビ2（−14.3）より小さかった → 山を最後に
final_gain(path, {"サビ2": -0.2, "最後のサビ": 1.4, "カーテンコール": 0.8})
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 14, "chorus": 22, "最後のサビ": 26, "bridge": 8}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 16, None, K), ("最後のサビ", 16, None, KD)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
