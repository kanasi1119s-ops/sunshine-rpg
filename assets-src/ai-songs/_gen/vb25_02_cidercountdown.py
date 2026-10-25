# vb25 02「サイダーカウントダウン」Cider Countdown（仮）— J-POP（疾走ピアノ）。E長調・前奏だけ 80 → 本編 178・4/4。最後のサビは +2（F#長調）
# 物語: 夏祭りの花火まで、残り10分。浴衣で下駄を鳴らして、神社の裏の坂道を駆け上がる。坂の上で息をのんだら、最初の花火が打ち上がる。
# 場面と強さ: 縁側の時計（ピアノだけ・ゆっくり・弱）→ 出発（10から数え下ろすピアノのリフ・全員）→ 下駄の音（Aメロ・語る）→ 坂道（Bメロ・溜め）
#   → あと5分（サビ・強）→ 屋台の灯り（間奏・中）→ 金魚すくい（2番。前半はピアノが歌を受け取る）→ 坂道2 → あと3分（サビ2）
#   → 射的とりんご飴（ピアノのソロ）→ 坂の上（全員の止め・虫の声だけの2小節）→ 見上げる空（Cメロ・Half feel）
#   → 導火線（こもった音・ローパス）→ 1拍の完全な無音 → 打ち上がる最後のサビ（+2・最大）→ 花火のあと（ピアノの1音だけ残す）
# 旋律の性格: 長調の循環の上で、上へ上へ伸びる。Aメロは16分の早口で、2小節ごとに3度ずつ階段のように上がる。
#   サビは同じ音の3連打のフックと、5度・6度の跳躍。最高音 C#6（最後のサビは C#6 で止める）
# 派手な展開: テンポの跳躍（80→178）・全員の止め（坂の上）・Half feel（Cメロ）・最後のサビ前のフィルター・1拍の完全な無音・最後のサビ +2
from vb25_lib import *

S = Song("02", "cidercountdown", "サイダーカウントダウン（仮）", "Cider Countdown", 178, 4, "E", "major", "J-POP（疾走ピアノ・ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
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
S.tempo = [{"bar": 1, "bpm": 80}, {"bar": S.sc("出発")[0] + 1, "bpm": 178}]

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75)
PNFX = [{"type": "eq", "low": -2, "mid": -1.5, "midHz": 350, "high": 1}]
def piano(role, vol): return S.track(role, "piano", volume=vol, pan=-0.12, reverb=0.24, fx=PNFX)
PR = piano("ピアノ（右手・16分の分散和音）", 0.13)
PL = piano("ピアノ（左手・8分のオクターブ）", 0.12)
PM = piano("ピアノ（リフ・歌の受け渡し・ソロ）", 0.17)
PC = [piano(f"ピアノ（和音{i + 1}）", 0.1) for i in range(3)]
MUF = [S.track(f"こもったピアノ{i + 1}（導火線）", "piano", volume=0.13, pan=-0.12, reverb=0.3,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}, {"type": "eq", "low": -2, "mid": 0, "midHz": 500, "high": 0}]) for i in range(2)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.085, pan=0.3, reverb=0.35, sustain=1.6) for i in range(4)]
GT = [S.track(f"ギター（{['根音', '5度'][i]}）", "distGuitar", **rock_gtr_spec(0.09, 0.0)) for i in range(2)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.21))
BUG = S.track("夏の虫の声（パルス波）", "lead", patch="chipPulse12", volume=0.035, pan=0.45, reverb=0.4, mono=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 1200, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.7}])
GLK = S.track("グロッケン（花火のきらめき）", "glockenspiel", volume=0.09, pan=0.25, reverb=0.45)
BOOM = S.track("花火の音（インパクト）", "impactHit", volume=0.1, pan=0.0, reverb=0.4)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役の旋律（E長調の度数。oct=4 で 1 = E4） =================
# Aメロ「下駄の音」: 16分の早口。同じ音の連打で語り、2小節ごとに3度ずつ階段のように上がる
A1 = ["R:0.25 1:0.25 1:0.25 2:0.25 3:0.25 3:0.25 2:0.25 1:0.25 R:0.25 1:0.25 2:0.25 3:0.25 5:0.5 3:0.5",
      "R:0.25 7,:0.25 7,:0.25 1:0.25 2:0.25 2:0.25 1:0.25 7,:0.25 R:0.25 7,:0.25 1:0.25 2:0.25 5:0.5 2:0.5",
      "R:0.25 3:0.25 3:0.25 4:0.25 5:0.25 5:0.25 4:0.25 3:0.25 R:0.25 3:0.25 4:0.25 5:0.25 6:0.5 5:0.5",
      "6:0.5 5:0.25 3:0.25 R:0.5 1:0.25 3:0.25 6:1.5 R:0.5",
      "R:0.25 6,:0.25 1:0.25 1:0.25 2:0.25 1:0.25 6,:0.5 R:0.25 2:0.25 2:0.25 3:0.25 4:0.25 3:0.25 2:0.5",
      "R:0.25 7,:0.25 2:0.25 2:0.25 3:0.25 2:0.25 7,:0.5 R:0.25 3:0.25 3:0.25 4:0.25 5:0.25 4:0.25 3:0.5",
      "R:0.25 1:0.25 3:0.25 3:0.25 4:0.25 3:0.25 1:0.5 R:0.25 4:0.25 4:0.25 5:0.25 6:0.25 5:0.25 4:0.5",
      "5:0.75 4:0.25 5:0.5 6:0.5 7:1 R:1"]
A1b = ["R:0.25 3:0.25 3:0.25 3:0.25 2:0.25 1:0.25 2:0.25 3:0.25 R:0.25 5:0.25 5:0.25 5:0.25 6:0.5 5:0.5",
       "R:0.25 2:0.25 2:0.25 2:0.25 1:0.25 7,:0.25 1:0.25 2:0.25 R:0.25 5:0.25 5:0.25 5:0.25 6:0.5 5:0.25 2:0.25",
       "R:0.25 1:0.25 1:0.25 3:0.25 5:0.25 1':0.25 7:0.25 5:0.25 R:0.25 6:0.25 6:0.25 5:0.25 3:0.5 1:0.5",
       "6:1 5:0.5 3:0.5 4:0.25 3:0.25 1:0.5 R:1",
       "R:0.25 4:0.25 4:0.25 5:0.25 6:0.25 6:0.25 5:0.25 4:0.25 R:0.25 2:0.25 4:0.25 6:0.25 1':0.5 6:0.5",
       "R:0.25 5:0.25 5:0.25 6:0.25 7:0.25 7:0.25 6:0.25 5:0.25 R:0.25 3:0.25 5:0.25 7:0.25 1':0.5 7:0.5",
       "6:0.5 5:0.25 4:0.25 R:0.25 4:0.25 5:0.25 6:0.25 7:1 6:0.5 5:0.5",
       "5:1.5 R:0.5 R:2"]
# 2番「金魚すくい」の後半（歌が戻る所）: 1番より高く、分散和音の16分で急に跳ぶ（歌いにくい所）
A2b = ["R:0.25 5:0.25 5:0.25 5:0.25 6:0.25 5:0.25 3:0.25 1:0.25 R:0.25 3:0.25 5:0.25 1':0.25 7:0.5 5:0.5",
       "R:0.25 5:0.25 5:0.25 5:0.25 4:0.25 2:0.25 7,:0.25 2:0.25 R:0.25 2:0.25 5:0.25 7:0.25 6:0.5 5:0.5",
       "R:0.25 6:0.25 6:0.25 6:0.25 7:0.25 6:0.25 5:0.25 3:0.25 R:0.25 5:0.25 6:0.25 1':0.25 2':0.5 1':0.5",
       "6:0.5 5:0.25 4:0.25 3:0.5 1:0.5 3:0.25 4:0.25 6:1 R:0.5",
       "R:0.25 1:0.25 1:0.25 2:0.25 4:0.25 6:0.25 1':0.25 6:0.25 R:0.25 4:0.25 6:0.25 1':0.25 2':0.5 1':0.5",
       "R:0.25 2:0.25 2:0.25 3:0.25 5:0.25 7:0.25 2':0.25 7:0.25 R:0.25 5:0.25 7:0.25 2':0.25 3':0.5 2':0.5",
       "1':0.75 7:0.25 6:0.5 4:0.5 3:0.25 4:0.25 6:0.5 1':1",
       "7:2 R:2"]
# Bメロ「坂道」: 8分で少しずつ上げて溜める。最後はのばして休む
BM = ["3:1 4:0.5 5:0.5 6:1 5:0.5 4:0.5", "5:1 6:0.5 7:0.5 2':1.5 R:0.5", "7:1 1':0.5 2':0.5 3':1 2':0.5 7:0.5", "1':2 R:0.5 3:0.5 5:0.5 6:0.5",
      "6:1 1':0.5 2':0.5 3':1.5 2':0.5", "2':0.5 1':0.5 7:1 #5:1 7:1", "1':1.5 7:0.5 1':1 3':1", "2':3 R:1"]
BM2 = BM[:4] + ["6:1 1':0.5 3':0.5 4':1.5 3':0.5", "2':0.5 1':0.5 7:0.5 #5:0.5 7:1 2':1", "3':1.5 2':0.5 1':1 3':1", "4':2 2':1 R:1"]
# サビ: 同じ音の3連打のフック（1〜2拍）を2回ずつ、5度・6度の跳躍で上へ。最後の2小節は上がって締める
CH1 = ["R:0.5 3':0.5 3':0.5 3':0.5 2':0.75 1':0.25 3:1", "R:0.5 1':0.5 1':0.5 1':0.5 5':1 3':1",
       "R:0.5 2':0.5 2':0.5 2':0.5 1':0.75 7:0.25 3:1", "R:0.5 5:0.5 3':0.5 2':0.5 1':2",
       "R:0.5 3':0.5 3':0.5 3':0.5 2':0.75 1':0.25 6:1", "R:0.5 1':0.5 1':0.5 1':0.5 5':1 6':1",
       "R:0.5 6':0.5 5':0.5 4':0.5 6:1 1':0.5 2':0.5", "2':1.5 1':0.5 5:1 2':1"]
CH2 = CH1[:3] + ["R:0.5 3:0.5 1':0.5 3':0.5 5':2", "R:0.5 6':0.5 5':0.5 4':0.5 3':1 2':0.5 1':0.5",
                 "R:0.5 5':0.5 3':0.5 7:0.5 3':1 2':0.5 1':0.5", "6:0.5 1':0.5 6':0.5 5':0.5 3':1 1':1", "2':2 #4':1 5':1"]
CHORUS = CH1 + CH2
# 最後のサビ（F#長調）: いちばん高い音は 5'（C#6）で止める
CL1 = [l.replace("6':1", "5':1") for l in CH1]
CL2 = CH2[:3] + ["R:0.5 3:0.5 1':0.5 3':0.5 4':2", CH2[4], CH2[5], "6:0.5 1':0.5 5':0.5 4':0.5 3':1 1':1", "2':2 #4':1 5':1"]
CL3 = CH1[:4] + ["R:0.5 3':0.5 3':0.5 3':0.5 4':0.5 3':0.5 5':1", "R:0.5 5':0.5 5':0.5 5':0.5 4':0.5 3':0.5 1':1",
                 "5':1.5 4':0.5 3':1 2':1", "1':3 R:1"]
CL4 = ["R:0.5 5:0.5 1':0.5 3':0.5 5':2", "4':1 3':1 2':1 4':1", "3':1.5 2':0.5 1':1 2':1", "5':4"]
LAST_L = [l.replace("6':", "5':") for l in CL1 + CL2 + CL3 + CL4] + ["R:4"] * 4

for i, b in enumerate(S.sc("下駄の音")): V.bar(b, K.mel((A1 + A1b)[i], oct=4))
for i, b in enumerate(S.sc("金魚すくい")):
    if i < 8: PM.bar(b, shift_oct(K.mel(A1[i], oct=4), 1))          # 2番の前半は、ピアノが歌を受け取る（1オクターブ上で）
    else: V.bar(b, K.mel(A2b[i - 8], oct=4))
for i, b in enumerate(S.sc("坂道")): V.bar(b, K.mel(BM[i], oct=4))
for i, b in enumerate(S.sc("坂道2")): V.bar(b, K.mel(BM2[i], oct=4))
for name in ("あと5分", "あと3分"):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(CHORUS[i], oct=4))
# Cメロ「見上げる空」: Half feel。長い音で、空を見上げるようにゆっくり上へ
HM = ["1':3 7:0.5 6:0.5", "7:2 5:1 3:1", "6:2 1':1 3':1", "2':3 R:1", "1':2 6:1 1':1", "7:1.5 1':0.5 7:1 5:1", "6:1 7:1 1':1 2':1", "1':4",
      "R:1 3:0.5 5:0.5 1':2", "#5:2 1':1 3':1", "4':2 3':1 1':1", "3':1 1':1 b6:2", "7:2 2':1 3':1", "3':2 1':2", "6:1 1':1 2':1 4':1", "5':4"]
for i, b in enumerate(S.sc("見上げる空")): V.bar(b, K.mel(HM[i], oct=4), low=(i >= 8))
# 導火線: こもった声（1オクターブ下の重ねのパートだけ。ローパス 2kHz）で、元の高さのまま上がっていく
FL = ["3:1 4:1 5:1 6:1", "5:1 6:1 7:1 1':1", "6:2 7:1 1':1", "6:1 b2':1 3':2"]
for i, b in enumerate(S.sc("導火線")): V.low.bar(b, K.mel(FL[i], oct=4))
for i, b in enumerate(S.sc("打ち上げ")): V.bar(b, KF.mel(LAST_L[i], oct=4))
for i, b in enumerate(S.sc("花火のあと")):
    if i < 4: V.bar(b, KF.mel(["3':2 2':2", "1':3 R:1", "2':2 5:2", "1':4"][i], oct=4), low=False)

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
for i, b in enumerate(S.sc("出発")): PM.bar(b, K.mel(RIFF[i], oct=4))
for i, b in enumerate(S.sc("屋台の灯り")): PM.bar(b, K.mel(RIFF[i], oct=4) if i < 4 else shift_oct(K.mel(RIFF[i], oct=4), 1) if i < 7 else K.mel(RIFF[i], oct=4))
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
        PR.bar(b, piano_arp16(ch, "B3", "B5", (0, 2, 1, 2, 3, 2, 1, 2))); PL.bar(b, piano_left8(ch, "E2"))
    elif n in ("下駄の音", "金魚すくい"):
        if i < 8:
            # 前半: 和音の刻み（2拍半の伸ばしと裏）。左手は2分の根音
            for j in range(3): PC[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5")
            r = low(ch, "E2"); PL.bar(b, f"{nm(r)}:2 {nm(r + 12)}:1.5 {nm(r + 7)}:0.5")
        else:
            PR.bar(b, piano_arp16(ch, "B3", "B5")); PL.bar(b, piano_left8(ch, "E2"))
    elif n.startswith("坂道"):
        if i == 7: continue                               # サビ直前の1小節は、ベースと歌の役だけ
        PR.bar(b, piano_arp16(ch, "C#4", "C#6", (0, 1, 2, 3, 4, 3, 2, 1))); PL.bar(b, piano_left8(ch, "E2"))
    elif n in ("あと5分", "あと3分", "打ち上げ"):
        if n == "打ち上げ" and i >= 28: continue
        PR.bar(b, piano_arp16(ch, "C#4", "C#6")); PL.bar(b, piano_left8(ch, "E2"))
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
    if n in ("あと5分", "あと3分", "打ち上げ", "見上げる空", "屋台の灯り") or (n.startswith("坂道") and i < 7):
        if n == "打ち上げ" and i >= 28: continue
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
    if n not in ("あと5分", "あと3分", "射的とりんご飴", "打ち上げ"): continue
    if n == "打ち上げ" and i >= 28: continue
    pw = power(S.chords[b], "E2")
    if n == "射的とりんご飴" and i < 8: pat = "X:1.5! X:1 X:1.5"
    elif i == L - 1 and n != "打ち上げ": pat = "X:0.5! X:0.5 X:0.5 X:0.5 X:2!"
    else: pat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
    for j in range(2): GT[j].bar(b, pat.replace("X", nm(pw[j])))

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in ("縁側の時計", "坂の上"): continue
    if n in ("出発", "屋台の灯り"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n in ("下駄の音", "金魚すくい"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "root8"))
    elif n.startswith("坂道"): BASS.bar(b, bass_line(S, b, "root8") if i < 7 else f"{nm(r)}:3 {nm(r + 12)}:0.5 {nm(r + 10)}:0.5")
    elif n in ("あと5分", "あと3分", "打ち上げ"):
        if n == "打ち上げ" and i >= 28: BASS.bar(b, f"{nm(r)}:4") if i == 28 else None; continue
        BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "射的とりんご飴": BASS.bar(b, bass_line(S, b, "walk" if i < 8 else "oct8"))
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
        vgroove(D, b, "vrock2", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if i == 4: crash(D, b, "G2")
        if n == "屋台の灯り" and 4 <= i < 7:
            D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16                       # ライド
        if last: put_fill(D, b, "tomdown")
    elif n in ("下駄の音", "金魚すくい"):
        if i < 8:
            vgroove(D, b, "beat8", ghosts=0.45, seed=b, h="x.x.x.x.x.x.x.x.")
            if n == "金魚すくい":
                D.cym(b, ("F2:0.5 " if i % 4 == 0 else "D2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        else:
            vgroove(D, b, "vrock2", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("坂道"):
        if i < 4: vgroove(D, b, "half", ghosts=0.3, seed=b)
        elif i < 7: vgroove(D, b, "vrock2", ghosts=0.3, seed=b)
        if i == 0: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "." * 16, "............xXXX", "." * 16)            # サビ直前の1小節は、ベースと歌の役だけ（最後の1拍だけ助走）
    elif n in ("あと5分", "あと3分", "打ち上げ"):
        if n == "打ち上げ" and i >= 28:
            if i == 28: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
            continue
        name = "vrock"
        if n == "あと3分" and i < 8: name = "punk"                         # 2回目のサビの前半は2ビート寄りに入れかえる
        if n == "打ち上げ" and 16 <= i < 24: name = "vrock2"
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomtrip")
        if last and n != "打ち上げ": put_fill(D, b, "tomdown")
    elif n == "射的とりんご飴":
        vgroove(D, b, "vrock2" if i < 8 else "vrock", ghosts=0.4, seed=b)
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
vwrite(S)
