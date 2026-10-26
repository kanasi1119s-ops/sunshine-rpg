# vb25 25「アンコールは流星群」Encore of Meteors（仮）— ロック（ボカロロック×オーケストラ）。F# 短調（サビは平行調の A）・190・4/4。
#   最後のサビで半音ずつ2回上がる（A → B♭ → B）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（ライブの最後の曲。小さな部屋で始めた歌が、たくさんの人に届いた）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を B♭短調から 4半音下げて F#短調にした（書くのは B♭短調／D♭長調の度数のまま、書き出しの前に下げる）。
#   いちばん高い音（F#5）は、最後のさらに +1 のサビに来るようにした。
# 物語: ライブの最後の曲。ふるえる指でマイクをにぎる。小さな部屋から始めた歌が、こんなに大きく響いている。
#   ゆれる光は星空みたい。流星群の夜に、ありがとうを歌に乗せる。支えてくれた人の名前を呼んで、アンコール。「また あしたね」。
# 場面と強さ: オーケストラの一撃 → 前奏（ギターのリフとオーケストラ・強）→ Aメロ（中）→ 空を見上げる（Bメロ・溜め・止め）
#   → 流星群（サビ・強）→ 掛け合い（ギターと弦の間奏）→ 24の灯り（2番。BGM は前半ピアノが歌を受け取る）→ 空を見上げる2（1拍の無音）→ 流星群2
#   → 名前を呼ぶ（Half feel。パワーコードが半音ずつ下りる）→ ギターのソロ → ピアノだけの落ちサビ（いちばん静か）
#   → こもった音（ローパス 800Hz の写し）でだんだん明るく → 1拍の無音 → 最後のサビ（+1）→ 1拍のブレイク → さらに +1（最大）→ 全員でのばして終わる
# 旋律の性格: Aメロは句の頭を休んで8分で語る。サビは5度・6度の跳躍で空へ上がる「りゅうせいぐんのよる」。
# 定番以外の和音: Aメロの Edim（♯iv°）、サビの F7（III7・副属和音）と D♭7（IV への副属和音）、Half feel の半音ずつ下りるパワーコード、
#   最後のサビ前の Em7–A7（半音上の調の ii–V へ飛ぶ）・B♭7（さらに半音上の調の属和音）
from vb25_lib import *

S = Song("25", "encore", "アンコールは流星群（仮）", "Encore of Meteors", 190, 4, "Bb", "minor", "ロック（ボカロロック×オーケストラ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock --orchestra vsco " + S.flags + " --piano salamander"
S.extra.update({"diGuitar": "emily"})
K = S.key                     # B♭ 短調（oct=3 で 1＝B♭3。歌は 2＝C4 から上）
KD = Key("Db", "major")       # サビ
KDD = Key("D", "major")       # 最後のサビ前半（+1）
KE = Key("Eb", "major")       # 最後のサビ後半（さらに +1）


def chk(key, lines, oct, beats=4):
    for l in lines: assert abs(total(key.mel(l, oct=oct)) - beats) < 1e-6, ("拍の数", l)


RIFF_CH = ["Bbm", "Gb", "Ab", "F"]
A_CH = ["Bbm", "Db", "Ab", "Gb", "Bbm", "Db", "Ebm7", "F", "Bbm", "Db", "Ab", "Gb", "Bbm", "Edim", "F", "F7"]
B_CH = ["Gbmaj7", "Ab", "Fm7", "Bbm7", "Ebm7", "Fm7", "Gbmaj7", "Ab7"]
C_CH = ["Bbm", "Gb", "Ab", "Db", "Ab/C", "Bbm", "Gb", "Ab", "Gbmaj7", "F7", "Bbm7", "Db7", "Gbmaj7", "Ab", "Bbm", "Ab"]
HF_CH = ["Bb5", "A5", "Ab5", "G5", "Gb5", "F5", "Gb5", "F5", "Gbmaj7", "Ab", "Fm7", "Bbm", "Gbmaj7", "Ab", "Bbm", "F7"]
FL_CH = ["Gbmaj7", "Ab", "Fm7", "Bbm7", "Gbmaj7", "Ab", "Em7", "A7"]
L1_CH = ["Bm", "G", "A", "D", "A/C#", "Bm", "G", "A", "Gmaj7", "F#7", "Bm7", "D7", "Gmaj7", "A", "Bm", "Bb7"]
L2_CH = ["Cm", "Ab", "Bb", "Eb", "Bb/D", "Cm", "Ab", "Bb", "Abmaj7", "G7", "Cm7", "Eb7", "Abmaj7", "Bb", "Cm", "Bb"]
OUT_CH = ["Abmaj7", "Bb", "Gm7", "Cm7", "Abmaj7", "Bb", "Cm7", "Bb/D", "Abmaj7", "Bb/Ab", "Ebadd9", "Ebadd9"]

S.scene("一撃", 4, "intro", ["Bbm", "Bbm", "Gb", "F"])
S.scene("前奏", 8, "intro", RIFF_CH)
S.scene("集まりはじめる", 16, "verse", A_CH)
S.scene("空を見上げる", 8, "pre", B_CH)
S.scene("流星群", 16, "chorus", C_CH)
S.scene("掛け合い", 16, "interlude", RIFF_CH)
S.scene("24の灯り", 16, "verse", A_CH)
S.scene("空を見上げる2", 8, "pre", B_CH)
S.scene("流星群2", 16, "chorus", C_CH)
S.scene("名前を呼ぶ", 16, "bridge", HF_CH)
S.scene("ギターのソロ", 16, "solo", RIFF_CH)
S.scene("落ちサビ", 8, "break", C_CH[:8])
S.scene("夜明けの手前", 8, "build", FL_CH)
S.scene("アンコール", 16, "chorus", L1_CH)
S.scene("アンコール2", 16, "chorus", L2_CH)
# 2026-10-26 人間「エイトビートもライドで刻むとか、ハイハット以外もつかって曲に合うように変えてほしい。これ重要」:
#   空を見上げる（Bメロ）はライド、掛け合いは裏の開いたハイハット、2回目のサビはライドのカップ、アンコールの後半はクラッシュの4分
S.keepers = {'空を見上げる': 'ride', '空を見上げる2': 'ride', '掛け合い': 'open', '流星群2': 'bell', 'アンコール2': 'wash'}
S.scene("全員でのばす", 12, "outro", OUT_CH)

V = Voice(S, vol=0.23, delay=0.75, patch="horn", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
PIANO_FX = [{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}]
PN = S.track("ピアノ（右手）", "piano", volume=0.12, pan=-0.2, reverb=0.25, fx=PIANO_FX)
PNC = [S.track(f"ピアノ（右手の和音{i + 2}）", "piano", volume=0.1, pan=-0.2, reverb=0.25, fx=PIANO_FX) for i in range(2)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.2, reverb=0.25, fx=PIANO_FX)
PNM = S.track("ピアノ（歌の受け渡し・落ちサビ）", "piano", volume=0.18, pan=-0.2, reverb=0.25, fx=PIANO_FX)
PNF = S.track("ピアノ（こもった写し）", "piano", volume=0.13, pan=-0.2, reverb=0.3,
              fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}, {"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}])
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.11, pan=0.3, reverb=0.35, sustain=1.6) for i in range(3)]
STRM = S.track("ストリングス（対旋律・掛け合い）", "strings", patch="stringEnsemble", volume=0.16, pan=0.3, reverb=0.35, sustain=1.6, mono=True)
TIMP = S.track("ティンパニ", "strings", patch="timpani", volume=0.2, pan=0.0, reverb=0.35)
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.13, pan=-0.3, reverb=0.3, gainDb=2, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 1.5, "midHz": 1500, "high": 0}]) for i in range(2)]
HALO = [S.track(f"合唱風のパッド{i + 1}", "pad", **pad_spec("halo", vol=0.06, pan=0.0, duck=0.25, sustain=2.5)) for i in range(2)]
GT = [S.track(f"ギター（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.09, 0.0)) for i in range(3)]
LG = S.track("リードギター（リフ・ソロ）", "distGuitar", **lead_gtr_spec(0.15, -0.05))
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
STAR = S.track("流れ星（ガラスのプラック）", "pad", patch="glassPluck", volume=0.07, pan=0.5, sustain=1.0, reverb=0.5)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.07, pan=0, modulate=False)
RIDE = S.track("ライド", "crash", **{k: v for k, v in NAKED["crash"].items() if k != "human"})
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（B♭短調／D♭長調の度数。oct=4。書き出しの前に全体を 4半音下げる） =================
VERSE = ["R:1 1:0.5 1:0.5 3:0.5 1:0.5 5:1", "3:1.5 1:0.5 5,:1 R:1", "R:1 7,:0.5 7,:0.5 2:0.5 7,:0.5 4:1", "3:1.5 1:0.5 6,:1 R:1",
         "R:1 5:0.5 5:0.5 3:0.5 1:0.5 5:1", "5:1 3:1 R:2", "R:1 4:0.5 4:0.5 6:0.5 4:0.5 3:1", "2:2 R:2",
         "R:0.5 5:0.5 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "5:1 7:1 R:2", "R:0.5 7:0.5 7:0.5 7:0.5 6:0.5 4:0.5 2:1", "3:1 6:1 R:2",
         "R:0.5 1:0.5 3:0.5 5:0.5 7:1 5:1", "1:1 #4:1 3:1 R:1", "R:0.5 #7,:0.5 2:0.5 5:0.5 #7:1 5:1", "4:2 R:2"]
V1 = "さいごのきょくだよ/ふるえるゆびさき/まいくをにぎる/みんながいる/ちいさなへやから/はじめたうたがね/こんなにおおきく/ひびいてるよ"
V2 = "ゆれるぺんらいと/ほしぞらみたいだ/かおはみえない/けどわかるよ/おなじうたうたう/こえでむすばれる/めのふちのしずく/わらうんだよ"
BM = ["R:1 4:1 6:1 1':1", "7:1.5 5:0.5 2':1 R:1", "R:1 3:1 5:1 7:1", "1':1.5 6:0.5 3':1 R:1",
      "R:0.5 2':0.5 2':0.5 2':0.5 4':1 2':1", "3':1 2':1 7:1 R:1", "R:0.5 4':0.5 4':0.5 3':0.5 1':1 3':1", "5':1 R:3"]
P1 = "みあげたそら/ながれぼしが/ひとつふたつみっつ/ふりそそぐよ"
P2 = "あいことばは/もういちどだ/こえをそろえたら/うたいだそう"
# サビ（D♭長調）: 5度・6度の跳躍で空へ上がる「りゅうせいぐんのよる」
CH = ["R:0.5 6:0.5 1':0.5 3':0.5 3':1 1':1", "4':1 3':1 1':1 6:0.5 R:0.5",
      "R:0.5 5:0.5 7:0.5 2':0.5 2':1 7:1", "1':1 3':1 5':1 R:1",
      "R:0.5 7:0.5 7:0.5 2':0.5 5':1 2':1", "3':1.5 1':0.5 6:1 R:1",
      "R:0.5 4:0.5 6:0.5 1':0.5 4':1 3':1", "2':2 R:2",
      "R:0.5 6:0.5 1':0.5 3':0.5 3':1 4':1", "#5':1 3':1 7:1 R:1",
      "R:0.5 6:0.5 1':0.5 3':0.5 5':1 3':1", "b7:1 1':1 3':1 R:1",
      "R:0.5 4':0.5 4':0.5 3':0.5 1':1 6:1", "5:1 7:1 2':1 R:1",
      "R:0.5 1':0.5 3':0.5 5':0.5 5':1 3':1", "2':3 R:1"]
C1 = "りゅうせいぐんのよる/きみのこえがする/ありがとうをいま/うたにのせて/このしゅんかんをね/まぶたにしまうよ/もういちどうたう/ほしのしたで"
C2 = "りゅうせいぐんのよる/ねがいごとひとつ/このうたがいつか/とどくように/ひとりのよるにも/ほしをとどけたい/なんどだってうたう/きみのために"
HF = ["R:4", "R:4", "R:1 4:1 5:1 7:1", "1:2 R:2", "R:1 6:1 1:1 3:1", "2:2 R:2", "R:1 1:1 3:1 6:1", "5:2 R:2",
      "R:0.5 3:0.5 3:0.5 3:0.5 5:1 3:1", "2:1 4:1 7:1 R:1", "R:0.5 5:0.5 5:0.5 5:0.5 7:1 5:1", "3:1.5 1:0.5 1:1 R:1",
      "R:0.5 1:0.5 3:0.5 5:0.5 6:1 5:1", "4:1 2:1 7,:1 R:1", "R:0.5 5:0.5 5:0.5 5:0.5 7:1 5:1", "#7:2 R:2"]
FL = ["R:4", "R:4", "R:1 3:1 5:1 7:1", "1':2 R:2", "R:1 4:1 6:1 1':1", "2':2 R:2"]
FL_D = ["R:1 2':1 4':1 5':1", "5':2 7:1 R:1"]                      # Em7–A7（D 長調の度数）
L1 = CH[:15] + ["1':3 R:1"]
L2 = CH[:9] + ["3':1 #5:1 7:1 R:1"] + CH[10:]
CL1 = "りゅうせいぐんのよる/もういちどうたう/みんなのこえがね/きこえてるよ/ふりそそぐひかり/ぜんぶうけとめて/このむねにだいて/うたいきるよ"
CL2 = "りゅうせいぐんのよる/このままずっといて/ありがとうきみに/であえたこと/うたぼしになれた/きみがいたからね/またあうひまでね/またあしたね"
OUT = ["R:1 4:1 6:1 1':1", "2':3 R:1", "R:1 3:1 5:1 7:1", "1':3 R:1", "R:1 6:1 1':1 3':1", "2':3 R:1",
       "R:0.5 6:0.5 1':0.5 3':0.5 3':1 2':1", "2':2 5:2", "R:1 3':1 2':1 1':1", "2':4", "1':4", "R:4"]
chk(K, VERSE, 4); chk(KD, BM, 4); chk(KD, CH, 4); chk(K, HF, 4); chk(KD, FL, 4); chk(KDD, FL_D, 4)
chk(KDD, L1, 4); chk(KE, L2, 4); chk(KE, OUT, 4)

LY = Lyrics(S)
def put(name, key, lines, text, low=True, bars=None):
    bars = bars or S.sc(name); ob, om = [], []
    for i, (b, x) in enumerate(zip(bars, lines)):
        if x == "R:4": continue
        m = key.mel(x, oct=4); V.bar(b, m, low=low if not callable(low) else low(i)); ob.append(b); om.append(m)
    LY.flow(ob, om, text, name)
put("集まりはじめる", K, VERSE, V1)
if VOCAL: put("24の灯り", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("24の灯り")):
        if i < 8: PNM.bar(b, K.mel(VERSE[i], oct=5))    # BGM: ピアノが歌を受け取る（1オクターブ上）
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("空を見上げる", KD, BM, P1); put("空を見上げる2", KD, BM, P2)
put("流星群", KD, CH, C1); put("流星群2", KD, CH, C2)
put("名前を呼ぶ", K, HF, "ありがと/ともだち/せんせい/かさになってくれた/なまえをよぶから/きこえていますか/ここにいるよ", low=lambda i: i >= 8)
put("落ちサビ", KD, CH[:8], "りゅうせいぐんのよる/ひとつねがいごと/このよるがながく/つづくように", low=False)
fb, fm = [], []
for i, b in enumerate(S.sc("夜明けの手前")):
    x = FL[i] if i < 6 else FL_D[i - 6]
    if x == "R:4": continue
    m = (KD if i < 6 else KDD).mel(x, oct=4); V.bar(b, m, low=False); fb.append(b); fm.append(m)
LY.flow(fb, fm, "みんなで/うたおう/もういちど", "夜明けの手前")
put("アンコール", KDD, L1, CL1)
put("アンコール2", KE, L2, CL2)
put("全員でのばす", KE, OUT, "ありがと/みんなに/このうた/ぜんぶあげるよ/ありがとう")

# ================= ギターのリフ・ソロと、弦の掛け合い =================
RIFF = ["1':0.5 1':0.25 5:0.25 7:0.5 1':0.5 3':0.5 2':0.25 1':0.25 7:1", "6:0.5 6:0.25 4:0.25 6:0.5 1':0.5 3':0.5 1':0.25 6:0.25 4:1",
        "7:0.5 7:0.25 4:0.25 7:0.5 2':0.5 4':0.5 2':0.25 7:0.25 2':1", "#7:0.5 2':0.5 5':0.5 2':0.5 #7:1 R:1"]
SOLO = ["1':0.5 7:0.25 5:0.25 1':0.5 3':0.5 5':1 3':1", "4':0.5 3':0.25 1':0.25 6:0.5 1':0.5 4':1 3':1",
        "2':0.5 1':0.25 7:0.25 4:0.5 7:0.5 2':1 4':1", "5':1.5 #7:0.5 2':1 R:1",
        "1'':0.25 7':0.25 5':0.25 3':0.25 1'':0.25 7':0.25 5':0.25 3':0.25 1':1 3':1",
        "6':0.25 4':0.25 3':0.25 1':0.25 6':0.25 4':0.25 3':0.25 1':0.25 6:1 1':1",
        "7':0.25 5':0.25 4':0.25 2':0.25 7':0.25 5':0.25 4':0.25 2':0.25 7:1 2':1", "#7':1 5':1 2':1 R:1",
        "5':2 6':1 5':1", "4':2 3':1 1':1", "2':1 4':1 7':1 5':1", "#7':2 R:2",
        "1':0.25 3':0.25 5':0.25 1'':0.25 5':0.25 3':0.25 1':0.25 3':0.25 5':0.5 1'':0.5 5':1",
        "1':0.25 3':0.25 4':0.25 6':0.25 4':0.25 3':0.25 1':0.25 3':0.25 4':0.5 6':0.5 1'':1",
        "2':0.25 4':0.25 5':0.25 7':0.25 5':0.25 4':0.25 2':0.25 4':0.25 5':0.5 7':0.5 1'':1", "#7':3 R:1"]
chk(K, RIFF, 3); chk(K, SOLO, 3)
for name in ("前奏", "掛け合い"):
    for i, b in enumerate(S.sc(name)):
        if name == "掛け合い" and i % 2 == 1: STRM.bar(b, K.mel(RIFF[i % 4], oct=3))     # 弦が1小節ずつ答える
        else: LG.bar(b, K.mel(RIFF[i % 4], oct=3))
# 2026-10-26 人間「どっかでハーモニクスとキーン！ていうチョーキングもあるといいなー」（どこか1曲で。25 に入れる）:
#   ・ソロの入り: いちばん高い所で全音のチョーキング（7''→1'' へ持ち上げて、のばしたまま戻さない＝「キーン！」）。
#   ・ソロの終わり: #6'（G）を全音持ち上げて導音 A（#7'）でのばす。どちらも戻さない（人間「上がって落ちる」は気になる）。ビブラートなし
#   ・名前を呼ぶ（Half feel）の最後の2小節: 本物のナチュラルハーモニクスが和音の音で鳴って、静かにソロへつなぐ
SOLO = ["7'':2!^^ 5':0.5 3':0.5 1':1"] + SOLO[1:15] + ["#6':3!^^ R:1"]
for i, b in enumerate(S.sc("ギターのソロ")): LG.bar(b, K.mel(SOLO[i], oct=3))
HARM = S.track("ギターのハーモニクス", "guitar", patch="guitarFx", volume=0.1, pan=0.3, reverb=0.35, modulate=False,
               fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}, {"type": "plate", "mix": 0.2}])
for k_, b in enumerate(S.sc("名前を呼ぶ")[-2:]):
    t_ = tones(S.chords[b], "E4", "E6")
    pick = [t_[-1], t_[-3], t_[-2], t_[-4]] if len(t_) >= 4 else t_
    HARM.bar(b, " ".join(f"{nm(m)}:1" for m in pick[:4]))
# 弦の対旋律（サビ。歌が長い音のとき動く）
CM_STR = ["3:2 4:1 5:1", "4:2 2:1 1:1", "1:2 2:1 3:1", "5,:4", "3:2 4:1 5:1", "3:2 1:2", "4:2 6:2", "5:4"]
for name, kk in (("流星群", KD), ("流星群2", KD), ("アンコール", KDD), ("アンコール2", KE)):
    # 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 最後の最後（アンコール2の後半）は、弦の対旋律を1オクターブ上へ（空いっぱいに広がる）
    for i, b in enumerate(S.sc(name)): STRM.bar(b, kk.mel(CM_STR[i % 8], oct=5 if (name == "アンコール2" and i >= 8) else 4))

# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 足した工夫:
#   ・合いの手: Aメロで歌が2拍休む所に、1番はリードギターの短い答え、2番の後半は弦の答え（楽器の受け渡し）。弱く（「,」）
#   ・名前を呼ぶ（Half feel）: パワーコードが半音ずつ下りるのに合わせて、弦の1本の線も3度上で半音ずつ下りる（名前を一人ずつ呼ぶように）
ANS = [[(2, 0.5), (1, 0.5), (0, 1)], [(None, 0.5), (0, 0.5), (1, 0.5), (2, 0.5)], [(1, 0.25), (2, 0.25), (3, 0.5), (2, 1)], [(3, 0.5), (2, 0.5), (1, 0.5), (None, 0.5)]]
def answer(tr_, b, k, lo, hi):
    tt = tones(S.chords[b], lo, hi)
    tr_.bar(b, "R:2 " + " ".join(f"R:{L:g}" if q is None else f"{nm(tt[min(q, len(tt) - 1)])}:{L:g}," for q, L in ANS[k % 4]))
for i, b in enumerate(S.sc("集まりはじめる")):
    if i in (5, 9, 11): answer(LG, b, i // 2, "F3", "F4")
for i, b in enumerate(S.sc("24の灯り")):
    if i in (9, 11, 15): answer(STRM, b, i // 2 + 1, "F4", "F5")
for i, b in enumerate(S.sc("名前を呼ぶ")):
    if i < 8: STRM.bar(b, ["Db4:4", "C4:4", "B3:4", "Bb3:4", "A3:4", "Ab3:4", "A3:2 Bb3:2", "Ab3:4"][i])

# ================= 伴奏 =================
def chords(trs, b, ch, pat, center):
    vv = voice(ch, center, len(trs))
    for j, t in enumerate(trs):
        t.bar(b, " ".join(("R:" + x.split(":")[1]) if x.startswith("R") else f"{nm(vv[j])}:{x.split(':')[1]}" for x in pat.split()))


BIG = ("流星群", "流星群2", "アンコール", "アンコール2")
for i, b in enumerate(S.sc("掛け合い")):
    if i >= 8 and i % 2 == 0: chords(BR, b, S.chords[b], "X:0.5 R:1 X:0.5 R:2", 60)     # 後半はブラスも合いの手
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    last = i == L - 1
    # オーケストラ: 弦の和音（サビ・前奏・Half feel）、ブラスの一撃と伸ばし、ティンパニ
    if n in BIG or n in ("前奏", "名前を呼ぶ", "全員でのばす") or n.startswith("空を見上げる"):
        # 2026-10-26: 名前を呼ぶの前半8小節は、弦の和音のかわりに、弦の1本の線が半音ずつ下りる（下の「名前を呼ぶ」。同じ音域を重ねない）
        if not (n == "全員でのばす" and i >= 10) and not (n == "名前を呼ぶ" and i < 8): chords(STR, b, ch, "X:4", 62)
    if n in BIG and i % 4 == 0: chords(BR, b, ch, "X:1.5 X:2.5", 60)
    if n in BIG and i % 8 == 7: TIMP.bar(b, f"R:2 {nm(low(ch, 'F2'))}:0.5 {nm(low(ch, 'F2'))}:0.5 {nm(low(ch, 'F2'))}:1")
    if n == "前奏" and i % 4 == 0: TIMP.bar(b, f"{nm(low(ch, 'F2'))}:2 R:2")
    # 合唱風のパッド
    if n in BIG or n in ("名前を呼ぶ", "夜明けの手前", "全員でのばす") or n.startswith("空を見上げる"):
        vv = voice(ch, 60, 2)
        if not (n == "全員でのばす" and i >= 10):
            for j in range(2): HALO[j].bar(b, f"{nm(vv[j])}:4")
    # ピアノ
    if n in BIG or n.startswith("空を見上げる"):
        PN.bar(b, piano_arp16(ch, "F4", "F6") if n in BIG else piano_arp16(ch, "C4", "C6", (0, 2, 1, 3, 2, 1, 3, 2)))
        PNL.bar(b, piano_left8(ch, "C3" if n in BIG else "C2"))
        if n.startswith("空を見上げる") and last: PN.bar(b, f"{nm(voice(ch, 72, 1)[0])}:2 R:2")
    elif n in ("集まりはじめる", "24の灯り"):
        if n == "24の灯り" and i < 8: PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 12)}:2")
        elif i >= 8 or n == "集まりはじめる":
            chords([PN] + PNC, b, ch, "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if i < 8 else "X:0.75 X:0.75 X:0.5 R:0.5 X:0.75 X:0.75", 66)
            PNL.bar(b, f"{nm(low(ch, 'C2'))}:1.5 {nm(low(ch, 'C2') + 12)}:1 {nm(low(ch, 'C2'))}:1.5")
    elif n == "落ちサビ":
        # ピアノだけ: 左手と右手で和音（歌のすき間に分散和音）
        vv = voice(ch, 64, 3)
        PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 7)}:2")
        chords([PN] + PNC, b, ch, "X:4", 64)
        PNM.bar(b, " ".join(f"{nm(x + 12)}:0.5" for x in [vv[0], vv[1], vv[2], vv[1]] * 2) if i % 2 == 1 else "R:4")
    elif n == "夜明けの手前":
        PNF.bar(b, piano_arp16(ch, "F4", "F6")); PNL.bar(b, f"{nm(low(ch, 'C2'))}:4")
    elif n == "全員でのばす":
        if i < 10: chords([PN] + PNC, b, ch, "X:2 X:2", 66); PNL.bar(b, f"{nm(low(ch, 'C2'))}:4")
        elif i == 10:
            vv = voice("Ebadd9", 68, 3)
            for j, t in enumerate([PN] + PNC): t.bar(b, f"R:{0.25 * j} {nm(vv[j])}:{8 - 0.25 * j}")
            PNL.bar(b, "Eb2:8")
    # ベース（根音。サビは8分のオクターブ）
    if n == "一撃": BASS.bar(b, f"{nm(low(ch, 'E1'))}:4" if i == 0 else "R:4")
    # 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 歌うベース（sing_bass。音域は元と同じ E1 から）を場面ごとに:
    #   サビ: 押す（drive）と、歌が伸ばす4小節目で駆ける（run）。前奏と間奏はリフに合わせてオクターブのまま、ソロの後半は押す／
    #   Aメロの後半: 1番は上る・下りる、2番は歩く（1番と変える）／Bメロ: 前半は根音の8分、後半は上っていって止めへ
    if n in BIG: BASS.bar(b, sing_bass(S, b, "run" if i % 4 == 3 else "drive"))
    elif n == "ギターのソロ" and i >= 8: BASS.bar(b, sing_bass(S, b, "drive" if i % 2 == 0 else "run"))
    elif n in ("前奏", "掛け合い", "ギターのソロ"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n in ("集まりはじめる", "24の灯り"):
        if i < 8: BASS.bar(b, bass_line(S, b, "push"))
        elif n == "集まりはじめる": BASS.bar(b, sing_bass(S, b, "climb" if i % 2 == 0 else "fall"))
        else: BASS.bar(b, sing_bass(S, b, "walk"))
    elif n.startswith("空を見上げる"):
        if last: BASS.bar(b, f"{nm(low(ch, 'E1'))}:2 R:2")
        else: BASS.bar(b, bass_line(S, b, "root8") if i < 4 else sing_bass(S, b, "climb"))
    elif n == "名前を呼ぶ": BASS.bar(b, bass_line(S, b, "half"))
    elif n == "夜明けの手前": BASS.bar(b, bass_line(S, b, "long" if i < 4 else "root8"))
    elif n == "全員でのばす": BASS.bar(b, bass_line(S, b, "oct8" if i < 4 else "half") if i < 10 else ("Eb2:8" if i == 10 else ""))
    # ギター（パワーコード）。Aメロ・落ちサビ・曲の頭では刻まない
    pw = power(ch, "E2")
    pat = None
    if n in ("前奏", "掛け合い", "ギターのソロ"): pat = "X:0.5! X:0.5 X:0.5 X:0.5 X:0.5! X:0.5 X:0.5 X:0.5" if i % 4 != 3 else "X:1.5! X:1.5 X:1!"
    elif n in BIG: pat = "X:0.5! X:0.5 X:0.5 X:0.5 X:0.5! X:0.5 X:0.5 X:0.5" if i % 8 < 6 else "X:1.5! X:1.5 X:1!"
    elif n == "名前を呼ぶ": pat = "X:4!" if i < 8 else "X:2! X:2"
    elif n.startswith("空を見上げる") and i >= 4: pat = "X:1! X:1 X:1! X:1" if not last else "X:2! R:2"
    elif n == "全員でのばす": pat = ("X:0.5! X:0.5 X:0.5 X:0.5 X:0.5! X:0.5 X:0.5 X:0.5" if i < 4 else "X:2! X:2") if i < 10 else ("X:8!" if i == 10 else None)
    if pat:
        for j in range(3): GT[j].bar(b, pat.replace("X", nm(pw[j])))

# オーケストラの一撃（1小節目: 弦・ブラス・ティンパニ・ギター・クラッシュがいっせいに）
# 2026-10-26 人間「後半に行くにつれて曲の始まり方似てない？」→ 一撃はこの曲だけに残す。アルバムの最後らしく、いちばん大きく開ける:
#   ブラスは1拍で切らずに3拍のばし、合唱風のパッド・ピアノの低いオクターブ・弦の高い音（B♭5）も加えて、
#   本物のクラッシュの長い一打（シンバルの効果音 F。8拍のばす）を重ねる。音のない所から全員で客席を開くように
b0 = 0
chords(STR, b0, "Bbm", "X:4", 62); chords(BR, b0, "Bbm", "X:3! R:1", 60); TIMP.bar(b0, "Bb2:0.25 Bb2:0.25 Bb2:0.25 F2:3.25")
for j in range(2): HALO[j].bar(b0, f"{nm(voice('Bbm', 60, 2)[j])}:4")
PNL.bar(b0, "Bb2:4!"); PN.bar(b0, "Bb3:4!"); STRM.bar(b0, "Bb5:4")
CYM.bar(b0, "F4:8")   # インパクトの楽器は MIDI のチャンネルがあふれるので足さない（ティンパニのロールと全員の一打が「ドン」の役）
for j in range(3): GT[j].bar(b0, f"{nm(power('Bbm', 'E2')[j])}:4!")
# 一撃のあと: 流星群が流れ始める（ガラスのプラックが上から下へ）
STARS = ["R:1 Bb5:0.25 F5:0.25 Db5:0.25 Bb4:0.25 R:2", "R:2.5 Ab5:0.25 F5:0.25 Db5:0.5 R:0.5", "R:0.5 Bb5:0.25 Gb5:0.25 Eb5:0.5 R:2.5", "R:3 C6:0.25 A5:0.25 F5:0.5"]
for i, b in enumerate(S.sc("一撃")[1:]): STAR.bar(b, STARS[i])
for name in ("流星群", "流星群2", "アンコール", "アンコール2"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 2: STAR.bar(b, "R:3 C6:0.25 Ab5:0.25 F5:0.25 Db5:0.25" if "アンコール" not in name else "R:3 F#5:0.25 D5:0.25 B4:0.25 F#4:0.25")
riser(FX, S.sc("流星群")[0], 4, "C4"); riser(FX, S.sc("アンコール")[0], 16, "D4")
cym_swell(CYM, S.sc("流星群2")[0], 2, "C4"); cym_swell(CYM, S.sc("アンコール2")[0], 2, "C4"); cym_swell(CYM, S.sc("ギターのソロ")[0], 2, "C4")
CYM.bar(S.sc("全員でのばす")[10], "B4:8")          # ロールのディミヌエンド（のばした和音の下で）
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ この曲の物語でしか出ない音: 客席の手拍子。
#   夜明けの手前（「みんなで うたおう」）で客席が手拍子を始め（1拍の無音で止まる）、最後の和音がのびる所で、アンコールの手拍子が鳴る（終わり方）
season(S, S.sc("夜明けの手前")[2], "手拍子", S.beats * 6, vol=0.07)
season(S, S.sc("全員でのばす")[11], "手拍子", S.beats * 1, vol=0.06)
# 最後の和音（全員でのばす）: 弦とブラスとパッドも
bx = S.sc("全員でのばす")[10]
chords(STR, bx, "Ebadd9", "X:8", 62); chords(BR, bx, "Ebadd9", "X:8", 58)
for j in range(2): HALO[j].bar(bx, f"{nm(voice('Ebadd9', 60, 2)[j])}:8")
TIMP.bar(bx, "Eb2:0.25 Eb2:0.25 Eb2:0.25 Eb2:0.25 Eb2:0.25 Eb2:0.25 Eb2:0.25 Eb2:0.25 Eb2:2 R:4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "一撃":
        if i == 0: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2"); RIDE.bar(b, "G2:4")
        elif i == 3: D.set(b, "." * 16, "........xxxxXXXX", "." * 16)
    elif n in ("前奏", "掛け合い"):
        vgroove(D, b, "vrock", ghosts=0.3, seed=b)
        if i % 4 == 0: crash(D, b, "C2" if i % 8 == 0 else "G2")
        if last: put_fill(D, b, "tomdown")
        elif i % 4 == 3: put_fill(D, b, "small")
    elif n in ("集まりはじめる", "24の灯り"):
        if i < 8: vgroove(D, b, "vrock2", ghosts=0.4, seed=b)
        else:
            vgroove(D, b, "vrock2", ghosts=0.35, seed=b); D.H[b] = "." * 16
            RIDE.bar(b, " ".join(("D2:0.5!" if q % 2 == 0 else "D2:0.5") for q in range(8)))
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomtrip")
    elif n.startswith("空を見上げる"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n in BIG:
        vgroove(D, b, "vrock", ghosts=0.3, seed=b)
        if n == "流星群2" and i < 8: vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)    # 2回目のサビの前半はリズムを入れかえる
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomdown")
        if last: put_fill(D, b, "tomtrip" if n != "アンコール2" else "tomdown")
    elif n == "名前を呼ぶ":
        vgroove(D, b, "half", ghosts=0.5, seed=b, h="................")
        RIDE.bar(b, "D2:1! D2:1 D2:1 D2:1")
        if i in (0, 8): crash(D, b, "C2")
        if i == 7: put_fill(D, b, "tomtrip")
        if last: put_fill(D, b, "build")
    elif n == "ギターのソロ":
        vgroove(D, b, "vrock" if i < 8 else "punk", ghosts=0.35, seed=b)
        if i % 4 == 0: crash(D, b, "C2" if i % 8 == 0 else "B2")
        if i % 4 == 3 and not last: put_fill(D, b, "small")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16)
    elif n == "落ちサビ":
        pass                                                          # ピアノだけ
    elif n == "夜明けの手前":
        D.set(b, "X...X...X...X...", "." * 16 if i < 4 else "....x.......x...", "." * 16 if i < 6 else "x.x.x.x.x.x.x.x.")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X...X...", "x.x.x.x.xxxxXXXX", "." * 16)
    elif n == "全員でのばす":
        if i < 10:
            vgroove(D, b, "vrock" if i < 4 else "half", ghosts=0.3, seed=b)
            if i in (0, 4): crash(D, b)
            if i == 3: put_fill(D, b, "tomdown")
        elif i == 10:
            D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
            D.tom(b, "R:2 C4:0.25 A3:0.25 F3:0.25 D3:0.25 A2:1!")

# 2026-10-26 人間「ドラム強弱、アクセント、余韻も上手く使ってね」:
#   ・Aメロの前半と Bメロの前半は軽く: 強打（X）を4小節の句の頭の1打だけ残して x に（ライドの所は元のまま）
#   ・サビは、2小節ごとの頭のキックと、次の小節へ押し出すスネアの最後の一打を強く
#   ・余韻: クラッシュは次のシンバルまで、最大 8拍のばす（止めのあとも鳴りを残す）
def lighten(b, head):
    for arr in (D.K, D.S):
        arr[b] = "".join(("x" if c == "X" and not (head and j == 0) else c) for j, c in enumerate(arr[b]))
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if (n in ("集まりはじめる", "24の灯り") and i < 8) or (n.startswith("空を見上げる") and i < 4): lighten(b, i % 4 == 0)
    elif n in BIG:
        kk = list(D.K[b]); ss = list(D.S[b])
        if kk[0] in "xX" and i % 2 == 0: kk[0] = "X"
        ls = max([j for j, c in enumerate(ss) if c in "xX"], default=None)
        if ls is not None and i % 2 == 1: ss[ls] = "X"
        D.K[b] = "".join(kk); D.S[b] = "".join(ss)
D.C.ev = [(st, max(L, 8.0), x) for st, L, x in D.C.ev]

# 止め・1拍の無音: Bメロの最後（1回目は止め、2回目は1拍の完全な無音）・最後のサビの前（2回の転調の直前に1拍ずつ）
SIL.add(S.sc("空を見上げる")[-1], 2, 4)
SIL.add(S.sc("空を見上げる2")[-1], 3, 4)
SIL.add(S.sc("夜明けの手前")[-1], 3, 4)
SIL.add(S.sc("アンコール")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の25（アルバムのフィナーレ）。ボカロロック×オーケストラ。F# 短調・190（サビは A、最後のサビで B♭ → B と半音ずつ2回上がる）。"
          "ライブの最後の曲。小さな部屋で始めた歌が、たくさんの人に届いた。オーケストラの一撃から、ギターのリフ、8分で語る Aメロ、跳躍の多いサビ、2番はピアノが歌を受け取り、"
          "パワーコードが半音ずつ下りる Half feel、ギターのソロ、ピアノだけの落ちサビ、ローパスの写しで明るくなって、1拍の無音から +1、さらに +1 の最後のサビ、"
          "全員で Badd9 をのばして終わる。自作")
S.no_depth = True   # 2026-10-25: 深いパッドを足すと MIDI のチャンネルがあふれるので、空間だけ
S.flags += " --space hall --space-wet 0.15"
teto(S, LY, V, transpose=-4, special={"アンコール": 0.5, "アンコール2": 0.6, "名前を呼ぶ": -0.4, "落ちサビ": -0.6, "夜明けの手前": -0.2, "全員でのばす": 0.3})
