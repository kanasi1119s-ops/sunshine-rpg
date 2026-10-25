# vb25 25「アンコールは流星群」Encore of Meteors（仮）— ロック（ボカロロック×オーケストラ）。B♭ 短調（サビは平行調の D♭）・190・4/4。
#   最後のサビで半音ずつ2回上がる（D♭ → D → E♭）
# 物語: アルバムのフィナーレ。これまでの24曲の登場人物たち（小さなロボット、カセットデッキ、渡り鳥、信号機、流れ星……）が、流星群の夜に丘の上へ集まってくる。
# 場面と強さ: オーケストラの一撃 → 前奏（ギターのリフとオーケストラ・強）→ 集まりはじめる（Aメロ・早口・中）→ 空を見上げる（Bメロ・溜め・止め）
#   → 流星群（サビ・強）→ 掛け合い（ギターと弦の間奏）→ 24の灯り（2番。前半はピアノが歌を受け取る）→ 空を見上げる2（1拍の無音）→ 流星群2
#   → ひとつずつ名前を呼ぶ（Half feel。パワーコードが半音ずつ下りる）→ ギターのソロ → ピアノだけの落ちサビ（いちばん静か）
#   → こもった音（ローパス 800Hz の写し）でだんだん明るく → 1拍の無音 → 最後のサビ（+1 の D）→ 1拍のブレイク → さらに +1 の E♭（最大）→ 全員でのばして終わる
# 旋律の性格: アルバムの中でいちばん高い（最後のサビで D6）。サビは 5度・6度・オクターブ近い跳躍が多い。Aメロは C4〜G5 の16分の早口で、16分の分散和音の跳躍（歌いにくい所）
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
S.scene("全員でのばす", 12, "outro", OUT_CH)

V = Voice(S, vol=0.23, delay=0.75, patch="voiceLeadModern")   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
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

# ================= 旋律 =================
# Aメロ（B♭短調・oct=3）: 16分の早口。12小節目は16分の分散和音で G♭5 まで跳ぶ（歌いにくい所）
A = ["R:0.25 5:0.25 5:0.25 5:0.25 6:0.25 5:0.25 3:0.25 5:0.25 R:0.25 1':0.25 7:0.25 5:0.25 6:0.5 5:0.5",
     "R:0.25 3:0.25 3:0.25 3:0.25 5:0.25 3:0.25 2:0.25 3:0.25 R:0.25 6:0.25 5:0.25 3:0.25 5:1",
     "R:0.25 7:0.25 7:0.25 1':0.25 2':0.25 1':0.25 7:0.25 4:0.25 R:0.25 2':0.25 1':0.25 7:0.25 2':0.5 1':0.5",
     "7:0.5 6:0.25 4:0.25 R:0.5 2:0.25 4:0.25 6:1.5 R:0.5",
     "R:0.25 1':0.25 1':0.25 1':0.25 2':0.25 1':0.25 7:0.25 5:0.25 R:0.25 3:0.25 5:0.25 1':0.25 3':0.5 2':0.5",
     "R:0.25 3':0.25 3':0.25 3':0.25 1':0.25 6:0.25 5:0.25 3:0.25 R:0.25 5:0.25 1':0.25 3':0.25 5':1",
     "4':0.5 3':0.25 1':0.25 R:0.5 6:0.25 1':0.25 4':1 3':1",
     "2':0.5 #7:0.5 5:0.5 2:0.5 5:2",
     "1':0.25 1':0.25 R:0.25 1':0.25 3':0.25 1':0.25 R:0.25 7:0.25 1':0.25 5:0.25 R:0.25 3:0.25 5:1",
     "7:0.25 7:0.25 R:0.25 7:0.25 1':0.25 7:0.25 R:0.25 5:0.25 7:0.25 3:0.25 R:0.25 2:0.25 3:1",
     "2':0.25 2':0.25 R:0.25 2':0.25 4':0.25 2':0.25 R:0.25 7:0.25 2':0.25 7:0.25 4:0.25 7:0.25 1':1",
     "6:0.25 1':0.25 3':0.25 6':0.25 5':0.5 3':0.5 1':2",
     "R:0.25 5':0.25 5':0.25 5':0.25 4':0.25 3':0.25 1':0.25 3':0.25 R:0.25 1':0.25 5:0.25 1':0.25 3':1",
     "R:0.25 #4':0.25 #4':0.25 #4':0.25 1':0.25 #6:0.25 1':0.25 #4':0.25 #6':1 R:1",
     "5':0.75 2':0.25 #7:0.5 5:0.5 R:0.5 2':1.5",
     "#7:0.5 2':0.5 4':0.5 5':0.5 R:2"]
# 2番（24の灯り）の後半: 同じ音の連打を2音ずつ上へずらしていく
A2b = ["R:0.25 3:0.25 3:0.25 R:0.25 5:0.25 5:0.25 R:0.25 1':0.25 1':0.25 R:0.25 3':0.25 1':0.25 5:1",
       "R:0.25 3:0.25 3:0.25 R:0.25 5:0.25 5:0.25 R:0.25 7:0.25 7:0.25 R:0.25 1':0.25 7:0.25 5:1",
       "R:0.25 4:0.25 4:0.25 R:0.25 7:0.25 7:0.25 R:0.25 2':0.25 2':0.25 R:0.25 4':0.25 2':0.25 1':1",
       "6:0.25 1':0.25 3':0.25 6':0.25 5':0.25 3':0.25 1':0.25 6:0.25 4':2"] + A[12:]
BM = ["6:1 7:0.5 1':0.5 3':1.5 1':0.5", "7:1 1':0.5 2':0.5 3':1 2':1", "1':1 2':0.5 3':0.5 5':1.5 3':0.5", "4':2 3':1 1':1",
      "2':1.5 4':0.5 6':1 5':0.5 4':0.5", "3':1.5 5':0.5 7':1 6':0.5 5':0.5", "6':1.5 5':0.5 4':1 3':1", "5':2 R:2"]
CH = ["R:0.5 6:0.5 3':0.5 3':0.25 3':0.75 6':1 3':0.5", "2':0.5 1':0.5 R:0.5 4:0.5 1':1.5 R:0.5", "R:0.5 5:0.5 2':0.5 2':0.25 2':0.75 5':1.5", "1':1.5 4:0.5 1':2",
      "R:0.5 3':0.25 3':0.25 3':0.5 R:0.25 7':0.75 5':1.5", "6':0.5 5':0.5 R:0.5 3':0.5 6':1 1':1", "4':0.75 3':0.75 2':0.5 6:1.5 2':0.5", "7:2 R:2",
      "R:0.5 6:0.5 3':0.5 3':0.25 3':0.75 6':0.5 5':1", "7':1 #5':0.5 3':0.5 2':1 7:1", "6':0.5 6':0.25 6':0.75 R:0.5 3':1.5 1':0.5", "5:0.5 1':0.5 3':0.5 5':0.5 b7':1 5':1",
      "R:0.5 4':0.25 4':0.25 4':0.5 R:0.25 6':0.75 3':1.5", "5':1.5 3':0.5 2':1 5:1", "6:0.5 1':0.5 3':0.5 6':0.5 7':1 6':1", "5':3 R:1"]
CH2 = CH[:12] + ["R:0.5 4':0.25 4':0.25 4':0.5 R:0.25 6':0.75 7':1.5", "1'':2 6':1 5':1", "4':1 3':1 2':1 1':1", "2':2 R:2"]
HF = ["R:4", "R:4", "1':2 2':1 1':1", "2':3 R:1", "3':2 1':2", "2':2 5:2", "3':1 4':1 6':2", "5':4",
      "4':2 3':1 1':1", "2':3 R:1", "7:1 2':1 4':1 5':1", "5':3 R:1", "6':2 5':1 4':1", "4':1.5 3':0.5 2':2", "1':1 3':1 5':1 1'':1", "#7':2 R:2"]
FL = ["R:4", "R:4", "1:1 2:1 3:1 5:1", "6:2 5:2", "4:1 5:1 6:1 1':1", "2':2 3':2"]
FL_D = ["2':1 4':1 5':2", "5':2 7:1 R:1"]                      # Em7–A7（D 長調の度数）
L1 = CH[:14] + ["6:0.5 1':0.5 3':0.5 6':0.5 7':1 1'':1", "1'':3 R:1"]
L2 = CH[:14] + ["6:0.5 1':0.5 3':0.5 6':0.5 7':2", "6':3 R:1"]
OUT = ["R:0.5 3':0.25 3':0.25 3':0.5 6':1.5 5':1", "5':1.5 3':0.5 2':1 5:1", "R:0.5 1':0.5 3':0.5 5':0.5 6':1 5':1", "5':3 R:1",
       "5':2 3':2", "2':4", "3':2 2':2", "5':4", "1':2 3':2", "2':4", "1':4", "1':4"]
chk(K, A, 3); chk(K, A2b, 3); chk(KD, BM, 4); chk(KD, CH, 4); chk(KD, CH2, 4); chk(K, HF, 3); chk(KD, FL, 4); chk(KDD, FL_D, 4)
chk(KDD, L1, 4); chk(KE, L2, 4); chk(KE, OUT, 4)

for i, b in enumerate(S.sc("集まりはじめる")): V.bar(b, K.mel(A[i], oct=3))
for i, b in enumerate(S.sc("24の灯り")):
    if i < 8: PNM.bar(b, K.mel(A[i], oct=4) if i % 4 != 3 else K.mel(A[i], oct=3))    # ピアノが歌を受け取る
    else: V.bar(b, K.mel(A2b[i - 8], oct=3))
for name in ("空を見上げる", "空を見上げる2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, KD.mel(BM[i], oct=4))
for i, b in enumerate(S.sc("流星群")): V.bar(b, KD.mel(CH[i], oct=4))
for i, b in enumerate(S.sc("流星群2")): V.bar(b, KD.mel(CH2[i], oct=4))
for i, b in enumerate(S.sc("名前を呼ぶ")): V.bar(b, K.mel(HF[i], oct=3), low=i >= 8)
for i, b in enumerate(S.sc("落ちサビ")): V.bar(b, KD.mel(CH[i], oct=4), low=False)
for i, b in enumerate(S.sc("夜明けの手前")):
    V.bar(b, KD.mel(FL[i], oct=4) if i < 6 else KDD.mel(FL_D[i - 6], oct=4), low=False)
for i, b in enumerate(S.sc("アンコール")): V.bar(b, KDD.mel(L1[i], oct=4))
for i, b in enumerate(S.sc("アンコール2")): V.bar(b, KE.mel(L2[i], oct=4))
for i, b in enumerate(S.sc("全員でのばす")):
    if i < 11: V.bar(b, KE.mel(OUT[i], oct=4) if i < 10 else KE.mel("1':8", oct=4))

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
for i, b in enumerate(S.sc("ギターのソロ")): LG.bar(b, K.mel(SOLO[i], oct=3))
# 弦の対旋律（サビ。歌が長い音のとき動く）
CM_STR = ["3:2 4:1 5:1", "4:2 2:1 1:1", "1:2 2:1 3:1", "5,:4", "3:2 4:1 5:1", "3:2 1:2", "4:2 6:2", "5:4"]
for name, kk in (("流星群", KD), ("流星群2", KD), ("アンコール", KDD), ("アンコール2", KE)):
    for i, b in enumerate(S.sc(name)): STRM.bar(b, kk.mel(CM_STR[i % 8], oct=4))

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
        if not (n == "全員でのばす" and i >= 10): chords(STR, b, ch, "X:4", 62)
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
    elif n in ("前奏", "掛け合い", "ギターのソロ") or n in BIG: BASS.bar(b, bass_line(S, b, "oct8"))
    elif n in ("集まりはじめる", "24の灯り"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "root8"))
    elif n.startswith("空を見上げる"): BASS.bar(b, bass_line(S, b, "root8") if not last else f"{nm(low(ch, 'E1'))}:2 R:2")
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
b0 = 0
chords(STR, b0, "Bbm", "X:4", 62); chords(BR, b0, "Bbm", "X:1 R:3", 60); TIMP.bar(b0, "Bb2:0.25 Bb2:0.25 Bb2:0.25 F2:3.25")
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

# 止め・1拍の無音: Bメロの最後（1回目は止め、2回目は1拍の完全な無音）・最後のサビの前（2回の転調の直前に1拍ずつ）
SIL.add(S.sc("空を見上げる")[-1], 2, 4)
SIL.add(S.sc("空を見上げる2")[-1], 3, 4)
SIL.add(S.sc("夜明けの手前")[-1], 3, 4)
SIL.add(S.sc("アンコール")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の25（アルバムのフィナーレ）。ボカロロック×オーケストラ。B♭ 短調・190（サビは D♭、最後のサビで D → E♭ と半音ずつ2回上がる）。"
          "24曲の登場人物たちが流星群の夜に集まる。オーケストラの一撃から、ギターのリフ、16分の早口の Aメロ、跳躍の多いサビ、2番はピアノが歌を受け取り、"
          "パワーコードが半音ずつ下りる Half feel、ギターのソロ、ピアノだけの落ちサビ、ローパスの写しで明るくなって、1拍の無音から +1、さらに +1 の最後のサビ（D6）、"
          "全員で E♭add9 をのばして終わる。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
