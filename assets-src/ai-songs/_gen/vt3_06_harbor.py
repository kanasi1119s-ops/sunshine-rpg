# vt3 06「朝焼け漁港」Dawn at the Fishing Port（仮）— 和太鼓と三味線の祭りビート（ギターなし）。152・4/4。E短調（民謡の5音）→ 最後は E の長い和音で朝になる。
# 第3弾（0時〜24時の街）の 5時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-13）: ゼロから作り直し（人間「全ての曲を1みたいにこだわって作って」「このレベル（02 v7）まで詰めて曲作って」）。
#   v1〜v3 は和ロック（ひずんだギターの8分の刻み）。ギターに聞こえないギターの音は使わない決まりなので、この曲はギターを使わず、
#   和太鼓（地打ちと表打ち）・三味線・琴を主役にして、サビだけ電子の和音とサブベースで押す。尺八は使わない（笛の音は指定がない限り使わない決まり）。
#
# 物語: 朝焼けの港。じいちゃんの漁船に、はじめて乗せてもらう孫の「わたし」。エンジンの音が胸にひびき、かもめが先に沖へ行く。
#   重い網をいっしょに引く。網の中で銀色の魚がはねる。じいちゃんが口ずさんだのは、夜のラジオで聞いたという鼻歌（3・5・6・5・2）。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: 手のひらのまめが「勲章」になり、波が手拍子を打ち、かもめがいっしょに歌いだす。
#
# 曲を決める表（書く前に similar_check.py --plan で確かめる）:
#   形: 和太鼓だけ（ドン……ドン……ドドン）→ 三味線のリフ → Aメロ1（太鼓の地打ちと琴・三味線は合いの手だけ）→ Bメロ（沖へ。和音がのぼる）
#       → サビ1（「あみをひけ」）→ かけ声（三味線のリフと「それ」）→ Aメロ2（ベースが歩く・三味線が刻む）→ Bメロ2 → サビ2
#       → 太鼓のソロ → 波（琴と声だけ・鼻歌）→ 最後のサビ（2回り・いちばん強い）→ E の長い和音（朝）と太鼓の一打
#   旋律: 民謡の5音（ミ・ソ・ラ・シ・レ）。Aメロ＝七・五の語り（8分で7つ、次の小節で5つ）。Bメロ＝8分で7つずつ、1段ずつ上へ。
#         サビ＝「あ・み・を・ひ・け」を長い音で呼び、次の小節で返事。後半は7つの8分で押して、長い音でしめる
#   和音: Aメロ i → VII → VI → VII。Bメロ VI → VII → v → i → VI → VII → V7。サビ VI → VII → i → III（明るい方へ開く）
#   ベース: Aメロ1 はなし（太鼓の低い音が土台）。2番から。サビは 8分で根音を押して、小節の終わりに5音でかけ上がる
#   この曲だけ: ①和太鼓の地打ち（ドンドコ）がドラムの代わりに曲を運ぶ ②三味線のリフ ③サビの「それ」のかけ声 ④最後だけ長調の和音（朝焼け）
#
# 和風の曲の作り方（2026-11-13 に調べた。tetsu7017.com「和風楽曲の作り方」ほか）: 和太鼓には、曲の土台になる「地打ち」と、それに合わせる「表打ち」がある。
#   → 低い太鼓がずっと同じ型（地打ち）を打ち、高い太鼓が場面の変わり目と合いの手で変化をつける（表打ち）。旋律は民謡の5音。
from vt25_lib import *

S = Song("06", "harbor", "朝焼け漁港（仮）", "Dawn at the Fishing Port", 152, 4, "E", "minor", "和太鼓と三味線の祭りビート（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space hall --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
S.keepers = {}
K = Key("E", "minor")          # oct 4 で 1 = E4。民謡の5音は 1・3・4・5・7

RIFF_CH = ["Em", "Em", "D", "Em", "Em", "Em", "D", "Em"]
A_CH = ["Em", "D", "C", "D", "Em", "D", "C", "Bsus4"]
B_CH = ["C", "D", "Bm7", "Em", "C", "D", "B7", "B7"]
C_CH = ["C", "D", "Em", "G", "C", "D", "Em", "Em", "C", "D", "Em", "G", "C", "D", "Em", "Em"]

S.scene("太鼓", 4, "intro", ["Em", "Em", "Em", "Em"])
S.scene("リフ", 8, "intro", RIFF_CH)
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("かけ声", 8, "break", RIFF_CH)
S.scene("Aメロ2", 16, "verse", A_CH + A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("太鼓のソロ", 8, "solo", ["Em", "Em", "Em", "Em", "Em", "Em", "Em", "B7"])
S.scene("波", 8, "bridge", ["G", "D", "Em", "Em", "G", "D", "C", "B7"])
S.scene("最後のサビ", 32, "chorus", C_CH + C_CH)
S.scene("朝", 6, "outro", ["C", "D", "E", "E", "E", "E"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
SHAM = S.track("三味線", "shamisen", volume=0.2, pan=0.25, reverb=0.2)
KOTO = S.track("琴（分散和音）", "koto", volume=0.13, pan=-0.4, reverb=0.3, sustain=1.6)
KOTO2 = S.track("琴（上の線）", "koto", volume=0.09, pan=0.4, reverb=0.35, sustain=1.6)
TLO = S.track("和太鼓（地打ち・低い太鼓）", "inchTom", volume=0.3, pan=-0.1, reverb=0.3)
THI = S.track("和太鼓（表打ち・高い太鼓）", "inchTom", volume=0.2, pan=0.2, reverb=0.3)
SAW = [S.track(f"電子の和音{i + 1}", "lead", patch="kfbSupersaw", volume=0.026, pan=-0.5 + 0.5 * i, reverb=0.25, duck=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(3)]
STR = [S.track(f"弦{i + 1}", "strings", patch="stringEnsemble", volume=0.04, pan=-0.4 + 0.8 * i, reverb=0.4, sustain=1.4) for i in range(2)]
BASS = S.track("ベース（指弾き）", "bass", sustain=0.9, **finger_bass_spec(vol=0.2))
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.03, pan=0, duck=0.5)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# Aメロ: 七・五の語り（2小節で1行）
VA = ["1:0.75 1:0.75 3:0.5 4:0.5 5:0.5 4:0.5 5:0.5", "7:0.75 7:0.75 5:0.5 4:0.5 5:1 R:0.5",
      "5:0.75 5:0.75 4:0.5 3:0.5 4:0.5 3:0.5 1:0.5", "7,:0.75 1:0.75 3:0.5 4:0.5 4:1 R:0.5",
      "1:0.75 3:0.75 4:0.5 5:0.5 7:0.5 5:0.5 7:0.5", "1':0.75 1':0.75 7:0.5 5:0.5 7:1 R:0.5",
      "5:0.75 7:0.75 5:0.5 4:0.5 3:0.5 4:0.5 5:0.5", "4:0.75 3:0.75 1:0.5 7,:0.5 1:1 R:0.5"]
A1 = ("ごじのみなとはあかねいろ/じいちゃんのふねめをさます/ふといゆびさきなわをとく/はじめてのるよこのふねに/"
      "えんじんのおとむねをうつ/かもめがさきにおきへゆく/しおのにおいとあさのかぜ/ちいさなあしでふみしめる")
A2 = ("あみをなげればうみひかる/うろこのぎんがはねている/てのひらのまめひとつでき/じいちゃんわらうくんしょうだ/"
      "ふいにきこえたはなうたは/よるのらじおできいたふし/わたしもまねてくちずさむ/なみがてびょうしくれている")
# Bメロ: 8分で7つずつ、1段ずつ上へ。最後は V7 の上で長い音
VB = ["3:0.75 3:0.75 5:0.5 5:0.5 7:0.5 5:0.25 7:0.25 R:0.5", "1':0.75 1':0.75 7:0.5 5:0.5 7:0.5 1':0.25 7:0.25 R:0.5",
      "5:0.75 5:0.75 7:0.5 7:0.5 2':0.5 7:0.25 5:0.25 R:0.5", "1':0.75 7:0.75 5:0.5 4:0.5 5:1 R:0.5",
      "5:0.75 5:0.75 7:0.5 7:0.5 1':0.5 7:0.25 1':0.25 R:0.5", "2':0.75 2':0.75 1':0.5 7:0.5 1':0.5 2':0.25 1':0.25 R:0.5",
      "5:1 #7:1 2':1 2':1", "2':2 R:2"]
B1 = "おきへおきへと/なみをこえてく/しぶきをあびて/むねをはる/あさひがのぼる/まんなかめざし/ふねはゆく"
B2 = "ちからあわせて/こえをあわせて/おもたいあみを/たぐりよせ/うみのめぐみが/きらきらはねて/あがるんだ"
# サビ: 「あみをひけ」（呼びかけ）→ 返事。2回目は終わりが上がる。後半は8分で7つ押して、長い音でしめる
HOOK = "5:1 5:0.5 7:0.5 1':1 1':0.5 R:0.5"
HOOK2 = "5:1 5:0.5 7:0.5 1':1 2':0.5 R:0.5"
VC = [HOOK, "R:0.5 7:0.5 7:0.5 5:0.5 7:1 5:0.5 R:0.5", HOOK2, "R:0.5 2':0.5 2':0.5 1':0.5 7:1 5:0.5 R:0.5",
      "3:0.75 5:0.75 5:0.5 5:0.5 7:0.5 5:0.25 3:0.25 R:0.5", "4:0.75 4:0.75 5:0.5 7:0.5 7:1 R:0.5", "1':1.5 7:0.5 5:1 7:1", "1':3 R:1",
      HOOK, "R:0.5 7:0.5 7:0.5 5:0.5 7:1 5:0.5 R:0.5", HOOK2, "R:0.5 2':0.5 2':0.5 1':0.5 7:1 5:0.5 R:0.5",
      "5:0.75 7:0.75 7:0.5 7:0.5 1':0.5 7:0.25 5:0.25 R:0.5", "7:0.75 7:0.75 1':0.5 2':0.5 2':1 R:0.5", "1':1.5 2':0.5 1':1 7:1", "1':3 R:1"]
C1 = ("あみをひけ/あさのうみ/あみをひけ/そらがもえ/じいちゃんのよこ/ならんでね/うみのこだ/"
      "あみをひけ/なみのうえ/あみをひけ/こえあわせ/ぎんのさかなが/あさひあび/はねあがる")
C2 = ("あみをひけ/おもくても/あみをひけ/はなさない/ちいさなこのて/にぎるのは/あしたまで/"
      "あみをひけ/もういちど/あみをひけ/そらたかく/かもめもいっしょに/うたいだす/あさがくる")
C3 = ("あみをひけ/みなとまで/あみをひけ/かえりみち/ふねいっぱいのせ/あのふしを/ふたりして/"
      "あみをひけ/いつのひか/あみをひけ/このふねを/わたしのてでね/うごかすよ/じいちゃんと/"
      "あみをひけ/あさやけに/あみをひけ/そまるほほ/まめだらけのて/ほこらしい/うみのこだ/"
      "あみをひけ/あさのうみ/あみをひけ/こえあわせ/ぎんのさかなが/あさひあび/はねあがる")
# 波: 鼻歌（合いことばの節。ト長調で 3・5・6・5・2 ＝ シ・レ・ミ・レ・ラ）→ ひとこと
VBR = ["R:2 5:0.5 7:0.5 1':1", "7:0.5 4:1.5 R:2", "R:1 3:1 4:1 5:1", "7:2 5:1 R:1",
       "R:2 5:0.5 7:0.5 1':1", "7:0.5 4:1.5 R:2", "R:1 5:1 7:1 1':1", "2':3 R:1"]
CB = "ららららら/なみのうえ/ららららら/ひびいた"
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
put("波", VBR, CB)
put("最後のサビ", VC + VC, C3)

# ================= 三味線・琴・和音 =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]
RIFF = ["E4:0.5 E4:0.25 G4:0.25 A4:0.5 B4:0.5 D5:0.5 B4:0.25 A4:0.25 G4:0.5 E4:0.5",
        "E4:0.5 E4:0.25 G4:0.25 A4:0.5 B4:0.5 E5:1 D5:0.5 B4:0.5",
        "D4:0.5 D4:0.25 F#4:0.25 A4:0.5 B4:0.5 D5:0.5 B4:0.25 A4:0.25 F#4:0.5 D4:0.5",
        "E4:0.5 G4:0.5 A4:0.5 B4:0.5 E5:1 R:1"]


def koto_arp(b, order=(0, 2, 3, 4, 5, 4, 3, 2), lo="E3", hi="E5", tr=None):
    tn = tones(root(b), lo, hi); (tr or KOTO).bar(b, " ".join(f"{nm(tn[q % len(tn)])}:0.5" for q in order))


def saw(b, pat="x:4", c=64):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): SAW[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def strs(b, c=67):
    v = sorted(voice(root(b), c, 3)); STR[0].bar(b, f"{nm(v[0])}:4"); STR[1].bar(b, f"{nm(v[2])}:4")


def sham_stab(b, pat):
    """三味線の合いの手（その和音の音を2つ、短く）"""
    tn = tones(root(b), "B3", "B4"); SHAM.bar(b, " ".join(t.replace("x", nm(tn[-1])).replace("y", nm(tn[-2])) for t in pat.split()))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "太鼓":
        if i == 3: SHAM.bar(b, "R:2 B3:0.25 D4:0.25 E4:0.5 G4:0.25 A4:0.25 B4:0.5")       # 三味線がかけ上がってリフへ
    elif n in ("リフ", "かけ声"):
        SHAM.bar(b, RIFF[i % 4])       # v8（2026-11-13 人間「三味線の音が前奏ちょっとしたら小さくなる」）: 前奏の後半で琴・ベース・キックが入ると三味線がうもれた → 前奏は琴なし、ベースは軽い型、三味線を大きく
        if n == "かけ声" and i >= 4: koto_arp(b)
        if n == "かけ声": saw(b, "x:0.5 R:1 x:0.5 R:2" if i % 2 == 0 else "R:4")
    elif n == "Aメロ1":
        koto_arp(b, (0, 2, 3, 4, 3, 2, 3, 4) if i % 2 == 0 else (0, 2, 3, 4, 5, 4, 3, 2))
        if i % 2 == 1 and i >= 8: sham_stab(b, "R:3 y:0.25 x:0.25 x:0.5")                  # 行の終わりに三味線が答える（後半から）
        if i >= 8: strs(b, 64)
    elif n == "Aメロ2":
        if i < 8:                                                # 2番の前半: 三味線が8分で刻み、琴は休み
            tn = tones(root(b), "E3", "E4"); SHAM.bar(b, " ".join(f"{nm(tn[q % len(tn)])}:0.5" for q in ((0, 0, 2, 0, 1, 0, 2, 1) if i % 2 == 0 else (0, 0, 2, 0, 1, 2, 3, 2))))
        else:
            koto_arp(b, (0, 2, 3, 4, 5, 4, 3, 2)); strs(b, 64)
            if i % 2 == 1: sham_stab(b, "R:2.5 y:0.5 x:0.25 x:0.25 x:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6:
            koto_arp(b, (0, 1, 2, 3, 4, 3, 2, 1) if i % 2 == 0 else (1, 2, 3, 4, 5, 4, 3, 2)); strs(b, 62 + i)
            if n == "Bメロ2": saw(b, "x:4", 60 + i)
        elif i == 6:
            strs(b, 69); saw(b, "x:1 x:1 x:1 x:1", 66); SHAM.bar(b, "B3:0.5 D#4:0.5 F#4:0.5 A4:0.5 B4:0.5 D#5:0.5 F#5:0.5 A5:0.5")
        else:
            saw(b, "x:2 R:2", 68); SHAM.bar(b, "B4:0.5 R:0.5 B4:1 R:2")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        j = i % 16
        big = n == "最後のサビ" and i >= 16
        saw(b, "x:1.5 x:1.5 x:1" if j % 2 == 0 else "x:1 x:1 x:1.5 R:0.5", 64 if n == "サビ1" else 66)
        if n != "サビ1" or j >= 8: strs(b, 69)
        koto_arp(b, (0, 2, 3, 4, 5, 4, 3, 2), "E4", "E6", KOTO2) if (n != "サビ1" and j % 2 == 1) else None
        # 三味線: 歌の返事のあと（偶数の小節の終わり）に短く答える。最後の2回り目はリフを重ねる
        if big and j in (6, 7, 14, 15): SHAM.bar(b, RIFF[1] if j % 2 == 0 else RIFF[3])
        elif j in (1, 3, 9, 11): sham_stab(b, "R:3 y:0.25 x:0.25 x:0.5")
        elif j in (7, 15): SHAM.bar(b, RIFF[3])
    elif n == "太鼓のソロ":
        if i >= 4: SHAM.bar(b, RIFF[i % 4] if i < 7 else "B3:0.5 D#4:0.5 F#4:0.5 A4:0.5 B4:1 R:1")
    elif n == "波":                                               # 琴だけ。波のように上がって下がる
        koto_arp(b, (0, 1, 2, 3, 4, 3, 2, 1), "G3", "G5")
        if i >= 4: KOTO2.bar(b, f"R:2 {nm(tones(root(b), 'B4', 'B5')[-1])}:2")
        if i == 7: strs(b, 66)
    elif n == "朝":
        if i < 2: saw(b, "x:4", 66); strs(b, 69); koto_arp(b)
        elif i < 5: saw(b, "x:4", 68); strs(b, 71); koto_arp(b, (0, 1, 2, 3, 4, 5, 6, 7), "E3", "E6") if i == 2 else None
        if i == 4: SHAM.bar(b, "E4:0.5 G#4:0.5 B4:0.5 E5:2.5")

# ================= 和太鼓（地打ち＝低い太鼓がずっと同じ型、表打ち＝高い太鼓が変化をつける）=================
LO, HI = "F1", "C2"
JI_A = f"{LO}:1 {LO}:0.5 {LO}:0.5 {LO}:1 {LO}:0.5 {LO}:0.5"          # ドン・ドコ・ドン・ドコ
JI_B = f"{LO}:0.5 {LO}:0.5 {LO}:0.5 {LO}:0.5 {LO}:1 {LO}:1"          # ドコドコ・ドン・ドン
JI_S = f"{LO}:1.5 {LO}:0.5 {LO}:1 {LO}:1"                             # 静かな所: ドーン・ド・ドン・ドン
OM_A = f"R:1.5 {HI}:0.5 R:1.5 {HI}:0.25 {HI}:0.25"                    # 表打ち: 裏に入る
OM_B = f"R:0.5 {HI}:0.5 R:1 {HI}:0.5 {HI}:0.5 R:0.5 {HI}:0.5"
OM_F = f"{HI}:0.25 {HI}:0.25 {HI}:0.5 {HI}:0.25 {HI}:0.25 {HI}:0.5 {LO}:0.5 {LO}:0.5 {HI}:0.25 {HI}:0.25 {HI}:0.25 {HI}:0.25"     # 場面の変わり目
TSOLO = [f"{LO}:1 {LO}:1 {HI}:0.5 {HI}:0.5 {LO}:1", f"{HI}:0.5 {HI}:0.25 {HI}:0.25 {LO}:1 {HI}:0.5 {HI}:0.25 {HI}:0.25 {LO}:1",
         f"{LO}:0.5 {HI}:0.5 {LO}:0.5 {HI}:0.5 {LO}:0.25 {LO}:0.25 {HI}:0.5 {LO}:0.25 {LO}:0.25 {HI}:0.5", f"{HI}:0.25 {HI}:0.25 {HI}:0.25 {HI}:0.25 {LO}:1 R:1 {LO}:1",
         JI_A, JI_B, JI_A, OM_F]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "太鼓": TLO.bar(b, [f"{LO}:4", f"R:2 {LO}:2", f"{LO}:1 {LO}:1 {HI}:0.5 {HI}:0.5 {LO}:1", f"{HI}:0.5 {HI}:0.5 {LO}:0.5 {LO}:0.5 {LO}:2"][i])
    elif n in ("リフ", "かけ声"):
        TLO.bar(b, JI_A if i % 2 == 0 else JI_B); THI.bar(b, OM_F if (last and n == "かけ声") else (OM_A if i % 2 == 0 else OM_B))
    elif n == "Aメロ1":
        TLO.bar(b, JI_A if i % 2 == 0 else JI_B)        # v7: 歌が入る所で 4.7dB 下がっていた（静かな地打ちにしていた）→ リフと同じ地打ちのまま歌に入る
        if i >= 8: THI.bar(b, OM_F if last else OM_A)
        elif i % 2 == 1: THI.bar(b, OM_A)
    elif n == "Aメロ2":
        TLO.bar(b, JI_A if i % 2 == 0 else JI_B); THI.bar(b, OM_F if last else (OM_A if i < 8 else OM_B))
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6: TLO.bar(b, JI_S if i < 4 else JI_A)
        elif i == 6: TLO.bar(b, f"{LO}:1 {LO}:1 {LO}:1 {LO}:1"); THI.bar(b, f"{HI}:0.5 {HI}:0.5 {HI}:0.5 {HI}:0.5 {HI}:0.25 {HI}:0.25 {HI}:0.25 {HI}:0.25 {HI}:0.25 {HI}:0.25 {HI}:0.25 {HI}:0.25")
        else: TLO.bar(b, f"{LO}:0.5 R:0.5 {LO}:1 R:2")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        TLO.bar(b, JI_A if i % 2 == 0 else JI_B)
        if n != "サビ1" or i >= 8: THI.bar(b, OM_F if (i % 8 == 7 and not last) else (OM_A if i % 2 == 0 else OM_B))
    elif n == "太鼓のソロ": TLO.bar(b, TSOLO[i])
    elif n == "波" and i >= 6: TLO.bar(b, f"{LO}:4" if i == 6 else f"{LO}:1 {LO}:1 {LO}:0.5 {LO}:0.5 {LO}:0.25 {LO}:0.25 {LO}:0.25 {LO}:0.25")
    elif n == "朝": TLO.bar(b, [JI_A, JI_B, f"{LO}:4", "R:4", f"{LO}:1 R:3", "R:4"][i])

# ================= ベース（この曲のために書く。共通の部品 bass_line は使わない）=================
PENTA = [40, 43, 45, 47, 50, 52, 55, 57, 59]     # ミ・ソ・ラ・シ・レ（E2 から）


def bl(b, style):
    ch = S.chords[b]; r = low(ch, "E1"); o = r + 12
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7)
    pn = [m - 12 for m in PENTA if r < m - 12 <= r + 12] or [t5]      # かけ上がりは民謡の5音で
    N = nm
    run = " ".join(f"{N(m)}:0.5" for m in (pn + pn)[:4])
    return {"push": f"{N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {N(t5)}:0.5 {N(o)}:0.5",
            "push_run": f"{N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {N(r)}:0.5 {run}",
            "step": f"{N(r)}:1 {N(t5)}:1 {N(o)}:1 {N(t5)}:1",
            "don": f"{N(r)}:1.5 {N(r)}:0.5 {N(t5)}:1 {N(r)}:1",                   # 太鼓の地打ち（静かな型）といっしょに
            "long": f"{N(r)}:3.5 R:0.5", "hit": f"{N(r)}:0.5 R:0.5 {N(r)}:1 R:2"}[style]


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "かけ声": BASS.bar(b, bl(b, "push_run" if i % 4 == 3 else "push"))
    elif n == "Aメロ2": BASS.bar(b, bl(b, "step" if i % 2 == 0 else "don"))
    elif n == "Aメロ1": BASS.bar(b, bl(b, "long" if i < 8 else "don"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bl(b, "don" if i < 6 else ("push" if i == 6 else "hit")))
    elif n in ("サビ1", "サビ2", "最後のサビ"): BASS.bar(b, bl(b, "push_run" if i % 4 == 3 else ("push" if (n != "サビ1" or i % 2 == 0) else "don")))
    elif n == "太鼓のソロ" and i >= 4: BASS.bar(b, bl(b, "don" if i < 7 else "hit"))
    elif n == "朝" and i < 3: BASS.bar(b, bl(b, "push" if i < 2 else "long"))
    if n in ("サビ2", "最後のサビ") or (n == "朝" and i < 3): SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:3.5 R:0.5")

# ================= ドラム（太鼓が主役なので、キックとスネアは サビ だけ。Aメロは手拍子のような縁の音）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("リフ", "かけ声"):
        D.set(b, "X.......X......." if n == "かけ声" else "................", "....x.......x...", "................")
    elif n == "Aメロ1" and i >= 8: D.set(b, "................", "....x.......x...", "................")
    elif n == "Aメロ2": D.set(b, "X.......X.......", "....x.......x...", "..x...x...x...x." if i >= 8 else "................")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6: D.set(b, "X.......X......." if i >= 4 else "................", "................", "x.x.x.x.x.x.x.x." if n == "Bメロ2" else "................")
        elif i == 6: D.set(b, "X...X...X...X...", "X.X.X.X.XXXXXXXX", "................")
        else: halt(D, b, 2); D.K[b] = "X...X..........."; D.S[b] = "X...X..........."
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.....x.X......." if i % 2 == 0 else "X.......X.x.....", s="....X.......X...", h="x.x.x.x.x.x.x.x.", vary=False)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i in (0, 16)) else 4)
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "朝":
        if i < 2: vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.....x.X.......", s="....X.......X...", h="x.x.x.x.x.x.x.x.", vary=False)
        if i == 2: crash(D, b, "C2", 8); D.set(b, "X...............", "X...............", "................")
        if i == 4: D.set(b, "X...............", "................", "................")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# 止め: Bメロ の8小節目は、頭の2拍のあと全員休み（サビの「あみをひけ」を大きく聞かせる）
for nme in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(nme)[-1], 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の06（5時）。和太鼓と三味線の祭りビート（ギターなし）。Em・152。朝焼けの港で、じいちゃんの漁船にはじめて乗る孫。"
          "和太鼓の地打ちと表打ち・三味線のリフ・琴、サビは電子の和音とサブベース。最後だけ長調の和音で朝になる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"波": -0.6, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "琴", mid=82, down=10, up=8, seed=3); humanize(path, "三味線", mid=86, down=8, up=8, seed=5); humanize(path, "和太鼓", mid=88, down=10, up=10, seed=7)
# v5 を測ると 太鼓 −34・リフ −21〜−25・Aメロ1 −22〜−24・波 −24〜−35（サビは −14）で、和楽器だけの場面が小さすぎた。サビ2（−13.6）が最後のサビ（−14.1）より大きかった。
#   → 和太鼓を2倍、三味線と琴を大きくして、和楽器だけの場面は伴奏そのものを大きく弾かせる。山は最後のサビに
# v9: v8 を測ると、太鼓だけの出だし（×2.0）からリフ（×1.5）に入る所で全体が 3dB 下がり、リフの後半でキックとベースが入るとさらに 2〜3dB うもれていた。
#   → 出だし・リフ・Aメロ1 を同じ大きさにし、リフの間はキックとベースを入れない（三味線と太鼓だけで通す）
scene_gain(path, S, {"太鼓": 1.7, "リフ": 1.7, "Aメロ1": 1.7, "波": 1.5}, only=lambda p: "三味線" not in p.get("role", ""))
# v8: 三味線は、出だしのかけ上がり（×2.0）からリフ（×1.5）に入る所で 2.5dB 下がっていた（人間「三味線の音が前奏ちょっとしたら小さくなる」）→ 出だしからリフの終わりまで同じ大きさ
scene_gain(path, S, {"太鼓": 2.0, "リフ": 2.0, "Aメロ1": 2.0}, only=lambda p: "三味線" in p.get("role", ""))
final_gain(path, {"Aメロ1": -0.8, "サビ1": 1.0, "サビ2": 0.3, "最後のサビ": 1.3})   # v7 を測ると サビ1（−15.5）が Aメロ1（−15.3）より小さかった → サビを山に
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 14, "chorus": 22, "最後のサビ": 26, "bridge": 6}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 16, None, K)], vol=0.36)
    # かけ声: 「かけ声」の場面で、三味線のリフのすき間にテトの「それ」
    kb = S.sc("かけ声")
    chops(path, S, {kb[1]: "R:3 B4:0.5:そ B4:0.5:れ", kb[3]: "R:3 B4:0.5:そ E5:0.5:れ", kb[5]: "R:3 B4:0.5:そ B4:0.5:れ", kb[7]: "R:2 B4:0.5:そ B4:0.5:れ E5:1:や"}, vol=0.3, pan=-0.2)
    voice_by_scene(path, S, {}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.3
    save(path, js)
