# vb25 02「サイダーカウントダウン」Cider Countdown（仮）— J-POP（疾走ピアノ・バンド）。E長調・前奏だけ 80 → 本編 178・4/4。最後のサビは +2（F#長調）
# 2026-10-25 作り直し（人間「２５曲も進めて。伴奏のみのBGMも含めてね」）: 物語を人の気持ちの話に、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
# 物語: 夏祭りの花火まで、あと少し。となりで空を見ている幼なじみに「好き」と言えるか。サイダーの泡がはじけるたびに、胸の中で数える。
#   小さいころ「ゆびきり」をした歌を思い出し、大人になるのがこわい自分にも気づく。最後は、打ち上がった花火の音に声がかき消されても、
#   君が笑ってうなずいてくれる。
# 場面と強さ: 縁側の時計（ピアノだけ・ゆっくり・弱）→ 出発（数え下ろすピアノのリフ・全員）→ となりの君（Aメロ・語る）→ 数える（Bメロ・数え歌で溜める）
#   → さん、にい、いち（サビ・強）→ 屋台の灯り（間奏）→ りんご飴（2番。BGM はピアノが歌を受け取る）→ 数える2 → 言えるかな（サビ2）
#   → ピアノのソロ → 坂の上（全員の止め・虫の声だけ）→ もしも（Cメロ・Half feel）→ 導火線（こもった音）→ 1拍の無音 → 打ち上げ（+2・最大）→ 花火のあと（ピアノ1音）
# 旋律の性格: Aメロは低め（C#4〜E5）で語り、2小節で1つの句。Bメロは「じゅう、きゅう、はち」の数え歌で上がる。
#   サビは「さん、にい、いち」の同じ音の3連のあと、「すきだよ　すきだよ」を2回（2回目は下がる）。最高音は E5、最後のサビ（F#）で F#5。
# 01（テクノポップ・シンセ中心・胸の音で始まり止まって終わる）とちがう所: 生のピアノ・ギター・ベース・ストリングスのバンド、テンポの跳躍で始まり、ピアノ1音で終わる。
from vb25_lib import *

S = Song("02", "cidercountdown", "サイダーカウントダウン（仮）", "Cider Countdown", 178, 4, "E", "major", "J-POP（疾走ピアノ・ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.extra.update({"diGuitar": "emily"})
K = S.key                    # E 長調
KF = Key("F#", "major")      # 最後のサビ（+2）

INTRO = ["Aadd9", "E/G#", "F#m7", "B7sus4"]
RIFF_CH = ["E", "B/D#", "C#m7", "A", "E", "B/D#", "Amaj7", "B"]
A_CH = ["E", "B/D#", "C#m7", "A", "F#m7", "G#m7", "Amaj7", "B"]
B_CH = ["Amaj7", "B", "G#m7", "C#m7", "F#m7", "G#7", "C#m7", "B7sus4"]          # G#7 = vi への副属和音
C_CH = ["A", "E", "B", "C#m", "A", "E/G#", "F#m7", "B", "A", "E", "B", "C#m", "F#m7", "G#m7", "A", "B"]
HALF_CH = ["C#m7", "G#m7", "Amaj7", "E/G#", "F#m7", "E/G#", "Asus2", "B7sus4",
           "E", "Eaug", "A/E", "Am/E", "G#m7", "C#m7", "F#m7", "B7sus4"]          # 増三和音と、同主短調の iv（Am）
FUSE = ["Amaj7", "B", "C#sus4", "C#"]                                             # C# は F# 長調の V（転調のつなぎ）
LAST_CH = [tr_chord(c, 2) for c in C_CH]
OUT_CH = ["B", "F#/A#", "G#m7", "F#"]

S.scene("縁側の時計", 4, "intro", INTRO)
S.scene("出発", 8, "intro", RIFF_CH)
S.scene("下駄の音", 16, "verse", A_CH)
S.scene("坂道", 8, "pre", B_CH)
S.scene("あと5分", 16, "chorus", C_CH)
S.scene("屋台の灯り", 8, "interlude", RIFF_CH)
S.scene("金魚すくい", 16, "verse", A_CH)
S.scene("坂道2", 8, "pre", B_CH)
S.scene("あと3分", 16, "chorus", C_CH)
S.scene("射的とりんご飴", 16, "solo", RIFF_CH + C_CH[8:])
S.scene("坂の上", 2, "break", ["B7sus4", "B7sus4"])
S.scene("見上げる空", 16, "bridge", HALF_CH)
S.scene("導火線", 4, "build", FUSE)
S.scene("打ち上げ", 32, "chorus", LAST_CH + LAST_CH)
S.scene("花火のあと", 9, "outro", OUT_CH + OUT_CH + ["F#"])
# 2026-10-26 人間「エイトビートもライドで刻むとか、ハイハット以外もつかって曲に合うように変えてほしい。これ重要」:
#   下駄の音（Aメロ）は4分に減らして歌と下駄の音を聞かせ、坂道は裏の開いたハイハットで前へ、2回目のサビはライドのカップで明るく、最後の打ち上げはクラッシュの4分（花火）。数え歌のように、刻みがだんだん大きくなる
S.keepers = {'下駄の音': 'quarter', '坂道': 'open', '坂道2': 'open', 'あと3分': 'bell', '打ち上げ': 'wash'}
S.tempo = [{"bar": 1, "bpm": 80}, {"bar": S.sc("出発")[0] + 1, "bpm": 178}]

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75, patch="surgeTropics", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
# 2026-10-26 人間（02）「ピアノの音もっと表に出していいと思う」→ ピアノ全部を 1.2 倍、3.2kHz を +2dB（打鍵の輪郭）、残響を少し減らして手前に
PNFX = [{"type": "eq", "low": -2, "mid": -1.5, "midHz": 350, "high": 1}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3200, "high": 0}]
def piano(role, vol): return S.track(role, "piano", volume=round(vol * 1.2, 4), pan=-0.12, reverb=0.2, fx=PNFX)
# 2026-10-26 人間（02）「ピアノの音ももっと大きくていい」→ ピアノ全部を 1.25 倍
PR = piano("ピアノ（右手・分散和音）", 0.138)
PL = piano("ピアノ（左手・8分のオクターブ）", 0.15)
PM = piano("ピアノ（歌の受け渡し・ソロ）", 0.212)
PMR = piano("ピアノ（数え下ろすリフ）", 0.198)
PC = [piano(f"ピアノ（和音{i + 1}）", 0.125) for i in range(3)]
MUF = [S.track(f"こもったピアノ{i + 1}（導火線）", "piano", volume=0.13, pan=-0.12, reverb=0.3,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}, {"type": "eq", "low": -2, "mid": 0, "midHz": 500, "high": 0}]) for i in range(2)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.085, pan=0.3, reverb=0.35, sustain=1.6) for i in range(4)]
GT = [S.track(f"ギター（{['根音', '5度'][i]}・中域の太い乾いた歪み）", "distGuitar", **{**rock_gtr_spec(0.072, 0.0, tone="electro-rock"), "ampGate": 8}) for i in range(2)]
# 2026-10-26 人間「ギターも途切れて前半聞こえるからちょっと聞きづらい」: ノイズゲートを浅くして（25 → 8）音の終わりを切らない
# 2026-10-25 人間「ドラム、ギターはブンブンサテライツにしよう」→ 中域の太い乾いた歪み（electro-rock）と、拍で刻んだ加工ギターの層（味付け・小さく）
# 2026-10-26 人間（02）「リフギターほんの本当にほんの少し気持ち程度に音量大きく」→ 0.070→0.072（1.03倍）
# 2026-10-26 人間（02）「リフ少し音を小さく。ほんの少し」→ 歪みギター 0.074→0.070、ピアノのリフ 0.17→0.158（別のパートに分けた）
GTG = S.track("ギター（拍で刻んだ加工の層）", "distGuitar", **rock_gtr_spec(0.045, 0.25, tone="electro-rock-gated"))
# 2026-10-26 人間（02）「ギターのリフ音でかいかな」→ 歪みギター 0.095→0.074。「バックの電子音ほんの少しだけ大きくてもいい」→ 加工の層 0.035→0.045
# 2026-10-26 人間（02）「ベースもメロディ入れてもう少し大きい音で」→ 0.21→0.24（リフギターの曲の 1.2 倍がさらに掛かる）。下の「ベース」で歌うベースに
BASS = S.track("ベース（指弾き・歌うベース）", "bass", **rock_bass_spec(0.24))
BUG = S.track("夏の虫の声（パルス波）", "lead", patch="chipPulse12", volume=0.035, pan=0.45, reverb=0.4, mono=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 1200, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.7}])
GLK = S.track("グロッケン（花火のきらめき）", "glockenspiel", volume=0.09, pan=0.25, reverb=0.45)
BOOM = S.track("花火の音（インパクト）", "impactHit", volume=0.1, pan=0.0, reverb=0.4)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律（E長調の度数。oct=4 で 1 = E4）と歌詞 =================
# Aメロ: 2小節で1つの句（前の小節に4〜5音、後ろの小節に1〜2音をのばして息つぎ）
# 2026-10-25 人間「歌い方とか既読メトロノームみたいな感じの歌い方にしようか」→ 句の頭を16分の2つで弾ませて入る（01 と同じ歌い方）。
VERSE = ["R:1 3:0.5 3:0.5 3:0.5 2:0.5 1:1", "2:2 R:2",
         "R:0.5 3:0.5 4:0.5 5:0.5 5:0.5 6:0.5 5:1", "3:2 R:2",
         "R:0.5 1:0.5 1:0.5 1:0.5 2:0.5 3:0.5 2:1", "7,:2 R:2",
         "R:0.5 6,:0.5 7,:0.5 1:0.5 2:0.5 3:0.5 4:1", "3:2 R:2",
         "R:0.5 3:0.5 3:0.5 3:0.5 4:0.5 5:0.5 6:1", "5:2 R:2",
         "R:0.5 5:0.5 6:0.5 1':0.5 7:0.5 6:0.5 5:1", "6:2 R:2",
         "R:1 4:0.5 3:0.5 2:1 4:1", "3:2 R:2",
         "R:1 4:0.5 3:0.5 2:0.5 2:0.5 3:1", "7,:2 R:2"]
V1 = "あとすこしで/はなびがあがる/ゆかたのそでを/ゆびでつまんだ/となりのきみは/そらをみている/いえるかな/のみこむかな"
V2 = "りんごあめを/ふたりでわけた/ちいさいころの/ゆびきりのうた/せのびしたかげ/すこしこわくて/いまならば/いえそうなの"
# Bメロ: 「じゅう、きゅう、はち」の数え歌で上がっていく。最後は sus4 の上で止まる
BM = ["R:1 3:0.5 4:0.5 5:1 5:1", "5:3 R:1", "R:1 5:0.5 6:0.5 7:1 7:1", "1':3 R:1",
      "R:1 2':0.5 2':0.5 1':0.5 1':0.5 7:0.5 7:0.5", "R:1 6:0.5 6:0.5 5:0.5 5:0.5 #4:1", "R:1 4:0.5 5:0.5 6:1 7:1", "1':2 R:2"]
P1 = ["かぞえて", "る", "むねのな", "か", "じゅうきゅうはち", "ななろくご", "とまらな", "い"]
P2 = ["ほんとう", "は", "きみのこ", "と", "いつからかな", "わからない", "とまらな", "い"]
# サビ（最高音は 1'＝E5。最後のサビの F# で F#5）。句の頭は16分の2つで弾ませる（01 の歌い方）
# 2026-10-26 人間（02）「曲調はいいのに歌詞、歌がスムーズに聞こえない」: サビの句の最後の1音（「いいち|で」「きみに|ね」「おとに|に」「ように|に」）の前に
#   半拍の休みがあり、言葉の途中で息つぎしていた → 休みをなくして、前の音を半拍のばしてつなぐ
CH = ["5:0.5 5:0.5 5:0.5 6:0.5 1':0.5 7:1.5", "1':2 R:2",
      "6:0.5 6:0.5 6:0.5 5:0.5 3:0.5 5:1.5", "6:2 R:2",
      "5:0.5 5:0.5 5:0.5 6:0.5 1':0.5 7:1.5", "6:2 R:2",
      "6:0.5 5:0.5 4:0.5 3:0.5 4:0.5 5:1.5", "7:2 R:2",
      "R:0.5 1':0.5 1':0.5 7:0.5 1':2", "R:0.5 1':0.5 1':0.5 7:0.5 6:2",
      "R:0.5 6:0.5 6:0.5 6:0.5 7:0.5 1':0.5 7:1", "6:2 R:2",   # 「すきだよ」のあとに息つぎ（半拍）
      "5:0.5 5:0.5 6:0.5 5:0.5 3:0.5 5:0.5 6:1", "5:2 R:2",
      "4:0.5 5:0.5 6:0.5 1':0.5 1':0.5 7:1.5", "7:2 R:2"]
CH_END = CH[:14] + ["5:0.5 5:0.5 6:0.5 1':0.5 1':0.5 7:0.5 6:1", "7:0.5 6:0.5 1':3"]
C1 = "さんにいいちで/いうよきみにね/はなびのおとに/まけないように/すきだよ/すきだよ/とどけそらまで/はじけるさいだー/このむねのおと"
C2 = "あわことばをね/むかしからだよ/ゆびきりのうた/こゆびのおくに/すきだよ/すきだよ/とどけほしまで/はじけるさいだー/このむねのおと"
C3 = "さんにいいちで/いうよいまなら/はなびのおとに/かきけされても/すきだよ/すきだよ/ちゃんととどいた/きみがわらうから/このむねのおと"
C4 = "さんにいいちで/はなびがさいた/ふたりのそらに/ひかりのはなが/すきだよ/すきだよ/あわことばでね/はじけるさいだー/なつのかうんとだうん"
# Cメロ「もしも」: Half feel。長い音で、空を見上げるように（最高音 2'＝F#5 は「わすれない」の1回だけ）
HM = ["R:1 3:1 5:1 6:1", "5:3 R:1", "R:0.5 6:0.5 6:0.5 1':0.5 2':1 1':1", "6:1 5:2 R:1",
      "R:1 4:1 5:1 6:1", "1':1 7:2 R:1", "R:1 6:1 7:1 1':1", "1':1 2':2 R:1",
      "R:0.5 3:0.5 3:0.5 5:0.5 1':1 7:1", "6:1 5:2 R:1", "R:0.5 4:0.5 4:0.5 6:0.5 1':1 2':1", "1':1 6:2 R:1",
      "R:1 6:1 7:1 1':1", "2':1 1':2 R:1", "R:1 1':1 7:1 6:1", "6:1 7:2 R:1"]
HV = ["もしも", "ね", "とどかなく", "ても", "このな", "つを", "わすれ", "ない",
      "きみのとな", "りで", "みあげたそ", "らは", "いつま", "でも", "ひかる", "から"]
LY = Lyrics(S)
def put(name, key, lines, text, low=True):
    bars = S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("下駄の音", K, VERSE, V1)
if VOCAL: put("金魚すくい", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("金魚すくい")):
        if i < 8: PM.bar(b, shift_oct(K.mel(VERSE[i], oct=4), 1))   # BGM: 2番の前半は、ピアノが歌を受け取る（1オクターブ上で）
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("坂道", K, BM, "".join(P1)); put("坂道2", K, BM, "".join(P2))
put("あと5分", K, CH, C1); put("あと3分", K, CH, C2)
put("見上げる空", K, HM, "".join(HV), low=False)
# 導火線: こもった声（1オクターブ下の重ねのパートだけ。ローパス 2kHz）で、元の高さのまま上がっていく（BGM では消える）
FL = ["3:1 4:1 5:1 6:1", "5:1 6:1 7:1 1':1", "6:2 7:1 1':1", "6:1 b2':1 3':2"]
for i, b in enumerate(S.sc("導火線")): V.low.bar(b, K.mel(FL[i], oct=4))
bars = S.sc("打ち上げ"); mel = [KF.mel(x, oct=4) for x in CH + CH_END]
for b, m in zip(bars, mel): V.bar(b, m)
LY.flow(bars, mel, C3 + "/" + C4, "打ち上げ")

# ================= ピアノ =================
# 出発: 10 から数え下ろすリフ（8分の下行 → 最後に跳ね上がる）
RIFF = ["5':0.5 4':0.5 3':0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5", "4:0.5 3:0.5 R:0.5 3:0.25 5:0.25 7:0.5 2':0.5 5':1",
        "3':0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5 3:0.5 1:0.5", "6:0.5 1':0.5 3':0.5 6':0.5 5':1.5 R:0.5",
        "5':0.5 4':0.5 3':0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5", "4:0.5 3:0.5 R:0.5 3:0.25 5:0.25 7:0.5 2':0.5 5':1",
        "3':0.5 4':0.5 3':0.5 1':0.5 6:0.5 1':0.5 3':0.5 6':0.5", "5':2 #4':1 R:1"]
# 射的とりんご飴: ピアノのソロ（16分で跳ねる。後半は右手のオクターブで歌う）
SOLO = ["1':0.25 3':0.25 5':0.25 3':0.25 1':0.25 3':0.25 5':0.25 1'':0.25 7':0.5 5':0.5 3':1",
        "2':0.25 4':0.25 7':0.25 4':0.25 2':0.25 4':0.25 7':0.25 2'':0.25 1'':0.5 7':0.5 5':1",
        "3':0.5 5':0.25 3':0.25 1':0.5 3':0.5 6':0.25 5':0.25 3':0.25 1':0.25 7:1",
        "6:0.25 1':0.25 4':0.25 6':0.25 5':0.25 4':0.25 3':0.25 1':0.25 6:1 R:1",
        "3':0.75 3':0.25 3':0.5 5':0.5 6':0.5 5':0.5 3':1", "2':0.75 2':0.25 2':0.5 4':0.5 5':0.5 4':0.5 2':1",
        "1':0.25 2':0.25 3':0.25 5':0.25 6':0.5 5':0.5 4':0.25 3':0.25 2':0.25 1':0.25 6:1", "7:0.5 2':0.5 5':0.5 7':0.5 6':1 5':1",
        "3'':1 2'':0.5 1'':0.5 6':1 5':1", "1'':1 7':0.5 5':0.5 3':2", "2'':1 1'':0.5 7':0.5 5':1 2':1", "3':0.5 5':0.5 1'':0.5 3'':0.5 2'':2",
        "4'':1 3'':0.5 2'':0.5 1'':1 6':1", "5':0.5 6':0.5 7':0.5 1'':0.5 2'':1 1'':1", "1'':1.5 7':0.5 6':1 1'':1", "7':2 R:2"]
for i, b in enumerate(S.sc("出発")): PMR.bar(b, K.mel(RIFF[i], oct=4))
for i, b in enumerate(S.sc("屋台の灯り")): PMR.bar(b, K.mel(RIFF[i], oct=4) if i < 4 else shift_oct(K.mel(RIFF[i], oct=4), 1) if i < 7 else K.mel(RIFF[i], oct=4))
for i, b in enumerate(S.sc("射的とりんご飴")): PM.bar(b, K.mel(SOLO[i], oct=4))
# 縁側の時計: ゆっくりのピアノだけ。サビのフックを先に少し（伸ばして）
INM = ["R:1 3':1 3':0.5 3':0.5 2':0.5 1':0.5", "7:2 3:1 5:1", "R:1 1':1 1':0.5 1':0.5 5':1", "4':2 2':1 R:1"]
for i, b in enumerate(S.sc("縁側の時計")):
    PM.bar(b, K.mel(INM[i], oct=4))
    t = tones(S.chords[b], "B3", "B4"); PR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 1, 2, 1, 3, 2, 1, 2)))
    PL.bar(b, f"{nm(low(S.chords[b], 'E2'))}:2 {nm(low(S.chords[b], 'E2') + 7)}:2")

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "縁側の時計": continue
    v = voice(ch, 66, 3)
    if n in ("出発", "屋台の灯り"):
        t = tones(ch, "B4", "B5"); PR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 1, 3, 2))); PL.bar(b, piano_left8(ch, "E2"))
    elif n in ("下駄の音", "金魚すくい"):
        if i < 8:
            # 前半: 和音の刻み（2拍半の伸ばしと裏）。左手は2分の根音
            for j in range(3): PC[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5")
            r = low(ch, "E2"); PL.bar(b, f"{nm(r)}:2 {nm(r + 12)}:1.5 {nm(r + 7)}:0.5")
        else:
            t = tones(ch, "B4", "B5"); PR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 1, 2, 1, 3, 2, 1, 2))); PL.bar(b, f"{nm(low(ch, 'E2'))}:2 {nm(low(ch, 'E2') + 12)}:2")
    elif n.startswith("坂道"):
        if i == 7: continue                               # サビ直前の1小節は、ベースと歌の役だけ
        t = tones(ch, "C#5", "C#6"); PR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 1, 2, 3, 2, 1, 2, 3))); PL.bar(b, piano_left8(ch, "E2"))
    elif n in ("あと5分", "あと3分", "打ち上げ"):
        if n == "打ち上げ" and i >= 28: continue
        t = tones(ch, "E5", "E6"); PR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 0, 2, 1, 3))); PL.bar(b, f"{nm(low(ch, 'E2'))}:1.5 {nm(low(ch, 'E2') + 12)}:1 {nm(low(ch, 'E2') + 7)}:1.5")
    elif n == "射的とりんご飴":
        r = low(ch, "E2"); PL.bar(b, f"{nm(r)}:0.5 {nm(r + 12)}:0.5 R:0.5 {nm(r)}:0.5 {nm(r + 7)}:0.5 {nm(r + 12)}:0.5 R:0.5 {nm(r)}:0.5")
        for j in range(3): PC[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:1 R:0.5 {nm(v[j])}:0.5 R:1")
    elif n == "見上げる空":
        # Half feel: 左手は全音符の根音、右手は和音の伸ばしと8分のゆっくりした分散
        r = low(ch, "E2"); PL.bar(b, f"{nm(r)}:4")
        vv = voice(ch, 64, 4)
        for j in range(3): PC[j].bar(b, f"{nm(vv[j + 1])}:4")
        t = tones(ch, "E5", "E6"); PR.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 1, 3)))
    elif n == "導火線":
        MUF[0].bar(b, piano_arp16(ch, "B3", "B5")); MUF[1].bar(b, piano_left8(ch, "E2"))
    elif n == "花火のあと":
        if i < 4:
            PR.bar(b, " ".join(f"{nm(x)}:0.5" for x in [tones(ch, 'C#4', 'C#6')[q % 6] for q in (0, 2, 4, 3, 5, 3, 2, 1)]))
            PL.bar(b, f"{nm(low(ch, 'E2'))}:4")
        elif i < 8:
            t = tones(ch, "C#4", "C#6"); PR.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 2)) if i < 7 else f"{nm(t[2])}:2 {nm(t[4])}:2")
            PL.bar(b, f"{nm(low(ch, 'E2'))}:4")
# 最後: ピアノの1音だけ残す（F#5 を伸ばしきる）
PM.bar(S.sc("花火のあと")[-1], "F#5:4")

# ================= ストリングス =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    if n in ("あと5分", "あと3分", "打ち上げ", "見上げる空") or (n.startswith("坂道") and i < 7):
        if n == "打ち上げ" and i >= 28: continue
        if n in ("あと5分", "あと3分") and i < 8: continue        # 「伴奏が聞きにくい」→ サビの前半は弦なし（重ねすぎない）
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "下駄の音" and i >= 8:
        for j in range(2): STR[j].bar(b, f"{nm(v[j + 1])}:4")
# 最後のサビの対旋律（ストリングスの高い所。歌が伸ばす所で動く）
CM = ["1'':2 7':1 6':1", "5':4", "7':2 1'':1 2'':1", "1'':4", "6':2 5':1 3':1", "4':2 3':2", "4':1 5':1 6':1 7':1", "1'':4"]
for i, b in enumerate(S.sc("打ち上げ")):
    if 8 <= i < 28: STR[3].bar(b, KF.mel(CM[i % 8], oct=3))

# ================= ギター（サビとソロだけ。明るいパワーコード） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n not in ("あと5分", "あと3分", "射的とりんご飴", "打ち上げ", "出発", "屋台の灯り", "下駄の音", "金魚すくい", "坂道", "坂道2"): continue
    if n == "打ち上げ" and i >= 28: continue
    if n in ("下駄の音", "金魚すくい") and i < 8: continue
    if n.startswith("坂道") and i == 7: continue
    pw = power(S.chords[b], "E2")
    # ビッグビートのギター: 刻んで止める（休みで弾む）。Aメロ・Bメロは短く刺すだけ
    # 2026-10-26: 刻んで止める形は途切れて聞こえたので、Aメロ・Bメロはのばして響かせ、サビも休みを入れずに8分でつなぐ
    # 2026-10-26 人間「ギター刻むなら刻む、伸ばすなら伸ばすにした方がいいかも」: 場面ごとにどちらか1つに決める
    #   のばす＝Aメロ・Bメロ・ソロの前半（全音符で響かせる）／刻む＝前奏・間奏・サビ・ソロの後半（8分を休みなく。拍の頭だけ強く）
    if n in ("下駄の音", "金魚すくい") or n.startswith("坂道") or (n == "射的とりんご飴" and i < 8): pat = "X:4!"
    else: pat = "X:0.5! X:0.5 X:0.5! X:0.5 X:0.5! X:0.5 X:0.5! X:0.5"
    if n in ("出発", "屋台の灯り") or (n == "射的とりんご飴" and i >= 8): GTG.bar(b, f"{nm(pw[0] + 12)}:4")   # 拍で刻んだ加工の層（前奏・間奏・ソロの後半）
    for j in range(2): GT[j].bar(b, pat.replace("X", nm(pw[j])))

# ================= ベース（歌うベース） =================
# 2026-10-26: 根音の8分だけだったのを、場面ごとに旋律のあるベースに。歌が伸ばす所・休む所でベースが動き、歌が細かい所では支える
#   出発・屋台（リフ）: 数え下ろすピアノに対して、ベースは上って押し返す（climb / drive、4小節目と8小節目は駆ける）
#   Aメロ: 前半は歩く（walk）で語りに寄りそう／後半は上る。Bメロ: 数え歌といっしょに上っていく
#   サビ: 歌が「すきだよ」で伸ばす偶数小節で駆ける（run）、ほかは押す（drive）。ソロ: 前半 walk・後半 drive。Cメロ: Half feel のまま
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in ("縁側の時計", "坂の上"): continue
    if n in ("出発", "屋台の灯り"): BASS.bar(b, sing_bass(S, b, "run" if i % 4 == 3 else ("climb" if i % 2 == 0 else "drive")))
    elif n in ("下駄の音", "金魚すくい"):
        if i < 8: BASS.bar(b, sing_bass(S, b, "walk") if i % 2 == 1 else bass_line(S, b, "push"))
        else: BASS.bar(b, sing_bass(S, b, "climb" if i % 2 == 0 else "fall"))
    elif n.startswith("坂道"): BASS.bar(b, sing_bass(S, b, "climb") if i < 7 else f"{nm(r)}:3 {nm(r + 12)}:0.5 {nm(r + 10)}:0.5")
    elif n in ("あと5分", "あと3分", "打ち上げ"):
        if n == "打ち上げ" and i >= 28: BASS.bar(b, f"{nm(r)}:4") if i == 28 else None; continue
        BASS.bar(b, sing_bass(S, b, "run" if i % 2 == 1 else "drive"))
    elif n == "射的とりんご飴": BASS.bar(b, sing_bass(S, b, "walk" if i < 8 else ("drive" if i % 2 == 0 else "run")))
    elif n == "見上げる空": BASS.bar(b, bass_line(S, b, "half"))
    elif n == "導火線": BASS.bar(b, f"{nm(r)}:4" if i < 3 else bass_line(S, b, "pulse"))
    elif n == "花火のあと" and i < 4: BASS.bar(b, f"{nm(r)}:4")

# ================= 虫の声・きらめき・花火・効果音 =================
def bugs(b, beats=4, pitch=("A6", "G#6")):
    """虫の声: 32分の3回の鳴きと休みを、高さを少し変えてくり返す"""
    out = []
    for q in range(int(beats)):
        p = pitch[q % 2]
        out.append(" ".join([f"{p}:0.125,"] * 3) + " R:0.625")
    BUG.bar(b, " ".join(out))
for b in S.sc("縁側の時計"): bugs(b)
for b in S.sc("坂の上"): bugs(b, 4, ("B6", "A6"))
for b in S.sc("花火のあと")[4:8]: bugs(b)
# 花火: 最後のサビの頭と、8小節ごとに「ドン」。グロッケンが光の粒を散らす
for i, b in enumerate(S.sc("打ち上げ")):
    if i in (0, 8, 16, 24): BOOM.bar(b, "C2:4")
    if i % 4 == 2 and i < 28: GLK.bar(b, KF.mel("R:2 5'':0.5 3'':0.5 1'':0.5 5':0.5", oct=4))
for i, b in enumerate(S.sc("あと5分") + S.sc("あと3分")):
    if i % 8 == 7: GLK.bar(b, K.mel("R:3 5':0.25 1'':0.25 3'':0.5", oct=4))
GLK.bar(S.sc("花火のあと")[3], KF.mel("R:2 1'':1 5':1", oct=4))
BOOM.bar(S.sc("出発")[0], "C2:4"); riser(FX, S.sc("出発")[0], 4, "C4")   # 前奏の勢い: 走り出しに「ドン」
riser(FX, S.sc("あと5分")[0], 4, "C4"); riser(FX, S.sc("あと3分")[0], 4, "C4")
riser(FX, S.sc("打ち上げ")[0] - 0.25, 8, "D4")                    # 導火線の音（終わりは1拍の無音の前）
cym_swell(CYM, S.sc("出発")[0], 2, "C4"); cym_swell(CYM, S.sc("射的とりんご飴")[0], 2, "C4")
cym_swell(CYM, S.sc("見上げる空")[0], 2, "E4")

# ================= ドラム（TRiDENT の音・crocell-punch） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "縁側の時計":
        if last: D.set(b, "." * 16, "........x.x.XXXX", "." * 16)          # 本編へのつなぎ（80 のまま、スネアの助走）
        continue
    if n in ("出発", "屋台の灯り"):
        # 2026-10-26 人間（02）「前奏もうちょい勢いあるといい」→ 出発はビッグビート（4つ打ち寄り）で走り出す
        vgroove(D, b, "bigbeat" if n == "出発" else "break1", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if i == 4: crash(D, b, "G2")
        if n == "屋台の灯り" and 4 <= i < 7:
            D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16                       # ライド
        if last: put_fill(D, b, "tomdown")
    elif n in ("下駄の音", "金魚すくい"):
        if i < 8:
            vgroove(D, b, "break2", ghosts=0.45, seed=b)
            if n == "金魚すくい":
                D.cym(b, ("F2:0.5 " if i % 4 == 0 else "D2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        else:
            vgroove(D, b, "break1", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("坂道"):
        if i < 4: vgroove(D, b, "half", ghosts=0.3, seed=b)
        elif i < 7: vgroove(D, b, "break1", ghosts=0.3, seed=b)
        if i == 0: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last:
            # 2026-10-26 人間（02）「さびに入る前のアクションとかも入れてほしい」→ サビ直前の1小節に、全員の「キメ」:
            #   1拍目・2拍目の裏・3拍目の裏で全員が「ジャン、ジャ、ジャン」とそろえて打ち、4拍目はスネアの16分で駆け上がってサビへ。
            #   キメのたびにクラッシュ（鳴りは伸ばす）。下の「サビ前のキメ」でギター・ベース・ピアノも同じ所を弾く
            D.set(b, "X.....X...X.....", "X.....X...X.xxXX", "." * 16)
            D.cym(b, "C2:1.5! G2:1! C2:1.5!")
    elif n in ("あと5分", "あと3分", "打ち上げ"):
        if n == "打ち上げ" and i >= 28:
            if i == 28: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
            continue
        name = "bigbeat"
        if n == "あと3分" and i < 8: name = "break2"                       # 2回目のサビの前半はブレイクビーツに入れかえる
        if n == "打ち上げ" and 16 <= i < 24: name = "break1"
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomtrip")
        if last and n != "打ち上げ": put_fill(D, b, "tomdown")
    elif n == "射的とりんご飴":
        vgroove(D, b, "break1" if i < 8 else "bigbeat", ghosts=0.4, seed=b)
        if i in (0, 8): crash(D, b)
        if 4 <= i < 8: D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16
        if i == 7: put_fill(D, b, "tomtrip")
        if last: put_fill(D, b, "snare16")
    elif n == "坂の上":
        if i == 0: halt(D, b, 1); crash(D, b, "C2", 8)                       # 全員の止め（1拍目だけ。シンバルは伸ばす）
        else: D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "見上げる空":
        vgroove(D, b, "half", ghosts=0.25, seed=b, h="." * 16)
        D.cym(b, ("E2:1 " if i % 4 else "C2:1 ") + "E2:1 E2:1 E2:1")
        if i == 7: put_fill(D, b, "tomtrip")
        if last: put_fill(D, b, "build")
    elif n == "導火線":
        D.set(b, "X...X...X...X...", "." * 16, "." * 16)
        if i == 3: D.set(b, "X...X...X.X.XXXX", "." * 16, "." * 16)
    elif n == "花火のあと":
        if i < 4:
            vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
            if i == 0: crash(D, b, "C2", 8)
        elif i == 4: D.cym(b, "E2:4")

# サビ前のキメ（坂道・坂道2 の最後の小節。ドラムは上のドラムの所で書いた）: 全員で「ジャン（1拍目）、ジャ（2拍目の裏）、ジャン（3拍目の裏）」
S.keep_drums = set()
for name in ("坂道", "坂道2"):
    b = S.sc(name)[-1]; S.keep_drums.add(b)
    ch = S.chords[b]; pw = power(ch, "E2"); r = low(ch, "E1"); vv = voice(ch, 66, 3)
    KIME = "X:1.5! X:1! X:1.5!"
    for j in range(2): GT[j].bar(b, KIME.replace("X", nm(pw[j])))
    BASS.ev = [e for e in BASS.ev if not (b * 4 - 1e-6 <= e[0] < (b + 1) * 4)]
    BASS.bar(b, KIME.replace("X", nm(r)))
    for j in range(3): PC[j].bar(b, KIME.replace("X", nm(vv[j])))
    PL.bar(b, KIME.replace("X", nm(low(ch, "E2"))))
cym_swell(CYM, S.sc("あと5分")[0], 1, "C4"); cym_swell(CYM, S.sc("あと3分")[0], 1, "C4")   # 逆再生のシンバルがサビの頭に吸いこまれる
# 坂の上: 1拍目のあとは全員休み（虫の声だけ残す）
SIL.add(S.sc("坂の上")[0], 1, 4)
# 導火線の最後の1拍は、完全な無音（虫の声も、何もかも）
SIL.add(S.sc("導火線")[-1], 3, 4)
# 坂の上の虫の声は消さない（止めの間に鳴らす）ので、止めの消去から外して後で戻す
keep_bug = [e for e in BUG.ev if S.sc("坂の上")[0] * 4 <= e[0] < (S.sc("坂の上")[-1] + 1) * 4]
SIL.apply()
BUG.ev += keep_bug

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の02。J-POP（疾走ピアノ）。E長調・前奏だけ 80、本編 178。最後のサビは +2（F#）。"
          "夏祭りの花火まで残り10分、浴衣で坂道を駆け上がる。ゆっくりのピアノと虫の声で始まり、10 から数え下ろすピアノのリフ、16分の早口で階段のように上がる Aメロ、"
          "同じ音の3連打のサビ、ピアノのソロ、坂の上の全員の止め、Half feel の Cメロ、こもった導火線と1拍の無音、+2 の最後のサビ（花火の音とグロッケン）、"
          "ピアノの1音だけ残して終わる。歌の役は声のように聞こえるシンセ。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, 0, "夕方の蝉", S.beats * 4, vol=0.08)
season(S, S.nb - 4, "鈴虫", S.beats * 4, vol=0.08)
S.no_depth = True   # 2026-10-25: 深いパッドを足すと MIDI のチャンネルがあふれるので、空間だけ
S.flags += " --space hall --space-wet 0.15"
S.flags = S.flags.replace("--master -13.5", "--master -11")
S.drum_scale = 0.97   # 2026-10-26 人間（02）「ドラムの音もほん、ほんの少しだけ気持ち程度に下げよう」→ ドラム全体を 0.97 倍   # 2026-10-26 人間「全体の音が小さいかな」
# 2026-10-26 人間（02）「一音一音しっかりした言葉で聞きたい。始まり何言ってるかよく分からない」→ Aメロとサビの16分を8分に（178 では1音 84ms で速すぎた）、
#   子音 1.5→2.0、つなぎの重ね 0.04→0.02、音の移りを少し速く（glide 1.5→1.15）、Aメロを少し強く（明るく）
# 2026-10-26 人間（02）「歌がスムーズに聞こえない」→ 子音 2.0→1.75・つなぎの重ね 0.02→0.035・音の移り 1.15→1.3（はっきりさとなめらかさの間）
# 2026-10-26 人間（02）「もっと歌詞がはっきりと聞こえるといい」→ 歌の版で: 歌を少し前に（0.6→0.68・約 +1dB）、子音 1.75→1.9、
#   ピアノ（1.25 倍にしたので歌とぶつかる）の言葉の聞こえる帯域 2.5kHz を −2.5dB へこませる
if VOCAL:
    for t_ in [PR, PL, PM, PMR] + PC:
        t_.spec["fx"] = list(t_.spec.get("fx", [])) + [{"type": "eq", "low": 0, "mid": -1.5, "midHz": 2500, "high": 0}]   # 歌の版: 歌の通り道を少しあける（ピアノを前に出したので −2.5 → −1.5）
teto(S, LY, V, vocal_level=0.68, settings={"legato": 0.035, "glide": 1.3, "gainSmooth": 0.07, "consonant": 1.9}, special={"打ち上げ": 0.55, "見上げる空": -0.5, "下駄の音": 0.3, "金魚すくい": 0.3})   # 2026-10-25「伴奏が聞きにくい」「声が圧倒的に大きい」→ 既定（0.6）で歌を下げる
