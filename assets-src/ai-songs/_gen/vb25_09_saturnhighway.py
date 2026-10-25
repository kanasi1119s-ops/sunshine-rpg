# vb25 09「ゴーゴー土星ハイウェイ」Go-Go Saturn Highway（仮）— ロック（ポップパンク）。A長調・208・4/4。最後のサビは +2（B長調）
# 物語: 自転車にロケットをつけて、友だちと土星の輪っかを一周する。
# 場面と強さ: 秒読み（歌の役が数える・小）→ 発射（全員・強）→ 大気圏をぬける（Aメロ・語る・中）→ 加速（Bメロ・溜め・止め）
#   → 輪っかに入る（サビ1・8ビート・強）→ 掛け声（短い句の言い合い）→ 無重力（間奏・オルガン）→ 2周目（オルガンが歌を受け取る）
#   → 輪っか2（サビ2・Half feel にリズムを入れかえ）→ 掛け声2 → 宇宙の無音2拍 → ただよう（Cメロ・静か→ Half feel で上がる）
#   → ギターソロ → 再突入 → 1拍の完全な無音 → 輪っかを抜ける（最後のサビ +2・2ビート・最大）→ 着陸（急に止める）
# 旋律の性格: 跳ねる8分と、合いの手の掛け声のような短い句。Aメロは16分の早口で跳ねる。サビは同じ音の3連打の「呼びかけ」。最高音 D6
# 派手な展開: 1拍の完全な無音・宇宙の無音2拍・サビごとのリズムの入れかえ（8ビート→Half feel→2ビート）・最後のサビ +2・止め2回
from vb25_lib import *

S = Song("09", "saturnhighway", "ゴーゴー土星ハイウェイ（仮）", "Go-Go Saturn Highway", 208, 4, "A", "major", "ポップパンク（ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
S.extra.update({"tone": "rock"})
K = S.key
K2 = K.up(2)           # 最後のサビ（B長調）

RIFF_CH = ["A", "C#m", "D", "Dm"]                                       # Dm＝同主調から借りた iv
V_CH = ["A", "C#m", "D", "E", "A", "C#m", "Bm7", "E7"]
B_CH = ["D", "E", "F#m", "C#m", "D", "E", "Bm7", "Eaug"]                 # Eaug＝増三和音（定番以外）
C_CH = ["D", "E", "C#m7", "F#m", "D", "E", "A", "A"]
C_CH2 = ["D", "E", "C#7", "F#m", "Bm7", "D/E", "A", "E/G#"]              # C#7＝vi への副属和音
SHOUT = ["A", "G", "D", "A", "A", "G", "D", "E"]                          # G＝♭VII
FLOAT = ["F#m", "D", "A/C#", "Dmaj7", "Bm7", "C#m7", "Dmaj7", "E7sus4",
         "F#m", "F#m/E", "Dmaj7", "C#7", "Bm7", "E/G#", "Dmaj7", "E"]
LAST3 = ["D", "E", "F#m", "G", "D", "E", "A", "A"]
up2 = lambda cs: [tr_chord(c, 2) for c in cs]

S.scene("秒読み", 4, "intro", ["A", "A", "E", "E"])
S.scene("発射", 12, "intro", RIFF_CH)
S.scene("大気圏", 16, "verse", V_CH)
S.scene("加速", 8, "pre", B_CH)
S.scene("輪っか", 16, "chorus", C_CH + C_CH2)
S.scene("掛け声", 8, "interlude", SHOUT)
S.scene("無重力", 16, "interlude", RIFF_CH)
S.scene("大気圏2", 16, "verse", V_CH)
S.scene("加速2", 8, "pre", B_CH)
S.scene("輪っか2", 16, "chorus", C_CH + C_CH2)
S.scene("掛け声2", 8, "interlude", SHOUT)
S.scene("ただよう", 16, "bridge", FLOAT)
S.scene("ギターソロ", 16, "solo", RIFF_CH)
S.scene("再突入", 8, "build", ["D", "E", "F#m", "D", "Bm7", "C#m7", "D", "E"])
S.scene("輪っかを抜ける", 24, "chorus", up2(C_CH + C_CH2 + LAST3))
S.scene("掛け声3", 8, "interlude", up2(SHOUT))
S.scene("着陸", 12, "outro", up2(SHOUT + SHOUT[:4]))

V = Voice(S, vol=0.22, delay=0.5, patch="voiceLeadModern")   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
GL = [S.track(f"ギター左（{['根音', '5度'][i]}）", "distGuitar", **rock_gtr_spec(0.085, -0.6)) for i in range(2)]
GR = [S.track(f"ギター右（{['根音', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.085, 0.6)) for i in range(2)]
LG = S.track("リードギター（リフ・ソロ）", "distGuitar", **lead_gtr_spec(0.14, -0.08))
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.21))
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.08, pan=0.3, reverb=0.25, sustain=1.0,
               fx=[{"type": "filter", "kind": "highpass", "freq": 180, "q": 0.7}, {"type": "rotary", "mix": 0.35}]) for i in range(3)]
ORGM = S.track("オルガン（歌の受け渡し）", "drawbarOrgan", volume=0.13, pan=0.0, reverb=0.25, sustain=1.0, mono=True,
               fx=[{"type": "filter", "kind": "highpass", "freq": 180, "q": 0.7}, {"type": "rotary", "mix": 0.35}])
CLAP = S.track("手拍子（カホンのスラップ）", "cajon", volume=0.13, pan=-0.2, reverb=0.3)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役 =================
# 秒読み: 5・4・3・2・1、ゴー
CD = ["5:0.5' R:1.5 4:0.5' R:1.5", "3:0.5' R:1.5 2:0.5' R:1.5", "1:0.5' R:1.5 5,:0.5' R:1.5", "R:1 1:0.5 3:0.5 5:0.5 1':1.5"]
for i, b in enumerate(S.sc("秒読み")): V.bar(b, K.mel(CD[i], oct=4), low=(i == 3))
# Aメロ: 16分の早口で跳ねる
A1 = ["R:0.5 5,:0.25 5,:0.25 1:0.5 1:0.25 3:0.25 R:0.25 2:0.25 1:0.25 5,:0.25 1:0.5 R:0.5",
      "R:0.25 3:0.25 3:0.25 3:0.25 5:0.5 3:0.5 R:0.25 2:0.25 3:0.25 2:0.25 7,:0.5 R:0.5",
      "R:0.5 4:0.25 4:0.25 6:0.5 4:0.25 3:0.25 2:0.25 3:0.25 4:0.25 6:0.25 5:1",
      "5:0.5 R:0.25 5:0.25 7,:0.5 2:0.5 R:0.5 5,:0.25 6,:0.25 7,:1",
      "R:0.5 1:0.25 1:0.25 3:0.5 1:0.25 5:0.25 R:0.25 4:0.25 3:0.25 1:0.25 3:0.5 R:0.5",
      "R:0.25 5:0.25 5:0.25 5:0.25 6:0.5 5:0.5 R:0.25 3:0.25 5:0.25 3:0.25 1:0.5 R:0.5",
      "R:0.5 4:0.25 4:0.25 2:0.5 4:0.25 5:0.25 6:0.25 5:0.25 4:0.25 2:0.25 4:1",
      "2:0.5 R:0.25 2:0.25 5:0.5 7:0.5 R:2"]
A1b = ["R:0.5 5,:0.25 5,:0.25 1:0.5 1:0.25 3:0.25 R:0.25 5:0.25 4:0.25 3:0.25 2:0.5 R:0.5",
       "R:0.25 3:0.25 3:0.25 3:0.25 5:0.5 1':0.5 R:0.25 7:0.25 5:0.25 3:0.25 5:0.5 R:0.5",
       "R:0.5 6:0.25 6:0.25 4:0.5 6:0.25 5:0.25 4:0.25 3:0.25 2:0.25 3:0.25 4:1",
       "5:0.5 R:0.25 4:0.25 3:0.5 2:0.5 R:0.5 7,:0.25 1:0.25 2:1",
       A1[4],
       "R:0.25 1':0.25 1':0.25 1':0.25 7:0.5 5:0.5 R:0.25 3:0.25 5:0.25 7:0.25 1':0.5 R:0.5",
       "R:0.5 6:0.25 6:0.25 4:0.5 2:0.25 4:0.25 6:0.25 5:0.25 4:0.25 2:0.25 2:1",
       "7,:0.5 1:0.5 2:0.5 3:0.5 5:2"]
A2b = ["R:0.5 3:0.25 3:0.25 5:0.5 3:0.25 1:0.25 R:0.25 2:0.25 3:0.25 5:0.25 6:0.5 R:0.5",
       "R:0.25 7:0.25 7:0.25 7:0.25 5:0.5 3:0.5 R:0.25 2:0.25 3:0.25 5:0.25 3:0.5 R:0.5",
       "R:0.5 6:0.25 6:0.25 1':0.5 6:0.25 4:0.25 2:0.25 4:0.25 6:0.25 1':0.25 6:1",
       "5:0.5 R:0.25 5:0.25 7,:0.5 2:0.5 R:0.5 5:0.25 4:0.25 2:1",
       "R:0.5 1:0.25 3:0.25 5:0.5 3:0.25 1:0.25 R:0.25 5,:0.25 1:0.25 3:0.25 5:0.5 R:0.5",
       "R:0.25 3:0.25 5:0.25 3:0.25 2:0.5 3:0.5 R:0.25 5:0.25 6:0.25 7:0.25 1':0.5 R:0.5",
       "R:0.5 2':0.25 1':0.25 6:0.5 4:0.25 2:0.25 4:0.25 6:0.25 1':0.25 6:0.25 4:1",
       "5:0.5 4:0.5 3:0.5 2:0.5 5:2"]
# Bメロ: 音階の段で上へずらして溜める。最後は止め
BM = ["4:1 6:0.5 1':0.5 6:1 4:1", "5:1 7:0.5 2':0.5 7:1 5:1", "6:0.5 6:0.5 6:0.5 7:0.5 1':1 6:1", "5:2 R:1 3:0.5 5:0.5",
      "6:0.5 6:0.5 6:0.5 1':0.5 2':1 1':1", "7:1 5:1 7:1 2':1", "1':1 2':1 6:1 4:1", "7:2 R:2"]
BM2 = BM[:5] + ["7:0.5 7:0.5 7:0.5 2':0.5 3':1 2':1", "2':1 1':1 6:0.5 4:0.5 6:1", "7:1 #5:1 R:2"]
# サビ: 同じ音の3連打の呼びかけ（休符で区切って「掛け声」のように）
CH1 = ["R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 R:0.5 7:0.5 5:1",
       "R:0.5 3:0.5 5:0.5 1':0.5 7:1 5:1", "6:1.5 5:0.5 6:2",
       "R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 3':1 2':1",
       "1':1 7:0.5 6:0.5 5:1 3:1", "5:3 R:1"]
CH1b = ["R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 R:0.5 7:0.5 5:1",
        "R:0.5 #5:0.5 #5:0.5 #5:0.5 3':1 #5:1", "6:1 1':1 3':2",
        "2':1 1':0.5 6:0.5 4:1 6:1", "5:1 7:1 2':1 1':0.5 7:0.5", "1':2 3':1 2':1", "1':2 R:2"]
CH2 = CH1[:6] + ["1':0.5 2':0.5 1':0.5 6:0.5 5:1 6:1", "5:2 3:1 5:1"]
CH2b = CH1b[:4] + ["2':1 1':0.5 6:0.5 2':1 4':1", "3':1 2':1 7:1 5:1", "6:1 1':1 2':1 3':1", "1':2 R:2"]
# 最後のサビ（B長調。最高音は C#6〜D#6 にならないよう、上の音を組みかえる）
CHL = ["R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 R:0.5 7:0.5 5:1",
       "R:0.5 3:0.5 5:0.5 1':0.5 7:1 5:1", "6:1.5 5:0.5 6:2",
       "R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 1':1 7:1",
       "1':1 7:0.5 6:0.5 5:1 3:1", "5:3 R:1",
       "R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 R:0.5 7:0.5 5:1",
       "R:0.5 #5:0.5 #5:0.5 #5:0.5 7:1 #5:1", "3:1 6:1 1':2",
       "2':1 1':0.5 6:0.5 4:1 6:1", "5:1 7:1 2':1 1':0.5 7:0.5", "1':2 2':1 1':1", "1':2 R:2",
       "R:0.5 1':0.5 1':0.5 1':0.5 2':1 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 1':1 7:1", "6:1 1':1 2':2", "b7:1 1':1 2':2",
       "R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "2':1 1':1 7:1 5:1", "1':4", "R:4"]
# 掛け声（♭VII の明るい句の言い合い）
SH = ["1':0.5 R:0.5 1':0.5 R:0.5 5:0.5 6:0.5 1':1", "b7:0.5 R:0.5 b7:0.5 R:0.5 4:0.5 5:0.5 b7:1",
      "6:0.5 R:0.5 6:0.5 R:0.5 4:0.5 2:0.5 4:1", "5:2 R:2",
      "1':0.5 R:0.5 1':0.5 R:0.5 2':0.5 1':0.5 5:1", "b7:0.5 R:0.5 b7:0.5 R:0.5 2':0.5 1':0.5 b7:1",
      "6:0.5 R:0.5 1':0.5 R:0.5 2':1 1':1", "7:2 R:2"]

for name, lines in (("大気圏", A1 + A1b), ("大気圏2", A1 + A2b)):
    for i, b in enumerate(S.sc(name)):
        line = K.mel(lines[i], oct=4)
        if name == "大気圏2" and i < 8: ORGM.bar(b, line)          # 2番の前半は、オルガンが歌を受け取る
        else: V.bar(b, line)
for name, lines in (("加速", BM), ("加速2", BM2)):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(lines[i], oct=4))
for name, lines in (("輪っか", CH1 + CH1b), ("輪っか2", CH2 + CH2b)):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(lines[i], oct=4))
for i, b in enumerate(S.sc("輪っかを抜ける")): V.bar(b, K2.mel(CHL[i], oct=4))
for name in ("掛け声", "掛け声2"):
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 0: V.bar(b, K.mel(SH[i], oct=4))
        else: ORGM.bar(b, K.mel(SH[i], oct=4))               # 歌の役とオルガンが言い合う
# ただよう（Cメロ）: 前半はささやき（重ねなし）、後半は Half feel で高い所へ（D6 への跳躍＝歌いにくい所）
FL = ["R:2 3:1 5:1", "6:3 R:1", "5:2 3:1 1:1", "2:3 R:1", "4:1 5:1 6:1 1':1", "7:2 5:2", "6:1 5:1 4:1 6:1", "5:4",
      "6:1 1':1 3':2", "2':2 1':2", "6:1 1':1 2':1 4':1", "3':3 R:1", "2':1 1':1 6:1 4:1", "5:2 7:2", "1':1 2':1 3':2", "2':3 R:1"]
for i, b in enumerate(S.sc("ただよう")): V.bar(b, K.mel(FL[i], oct=4), low=(i >= 8))
RE = ["4:1 6:1 1':2", "7:1 5:1 7:2", "6:1 1':1 3':2", "1':4", "2':1 1':1 6:1 4:1", "5:2 7:2", "6:1 1':1 2':1 3':1", "2':2 R:2"]
for i, b in enumerate(S.sc("再突入")): V.bar(b, K.mel(RE[i], oct=4))
for i, b in enumerate(S.sc("掛け声3")): V.bar(b, K2.mel(SH[i], oct=4))      # 最後は全員で言い合わずに声をそろえる
LAND = ["5:2 3:2", "2:4", "1:2 3:1 5:1", "5:4", "1':2 7:1 5:1", "b7:3 R:1", "6:1 4:1 6:1 1':1", "2':4",
        "1':0.5 R:0.5 1':0.5 R:0.5 5:0.5 6:0.5 1':1", "b7:0.5 R:0.5 b7:0.5 R:0.5 2':0.5 1':0.5 b7:1", "6:0.5 R:0.5 1':0.5 R:0.5 2':1 1':1", "1':1! R:3"]
for i, b in enumerate(S.sc("着陸")): V.bar(b, K2.mel(LAND[i], oct=4), low=(i >= 8))
# 無重力の後半: オルガンのソロ（主旋律の受け渡し）
OS = ["5:0.5 3:0.5 5:0.5 1':0.5 7:1 5:1", "3:0.5 5:0.5 7:0.5 2':0.5 3':1 7:1", "6:0.5 4:0.5 6:0.5 1':0.5 2':1 1':1", "b6:1 4:1 2:1 7,:1",
      "1':0.25 7:0.25 6:0.25 5:0.25 3:0.5 5:0.5 1':2", "3':0.25 2':0.25 1':0.25 7:0.25 5:0.5 7:0.5 3':2", "4':0.5 2':0.5 1':0.5 6:0.5 4:0.5 6:0.5 1':1", "b6:2 5:2"]
for i, b in enumerate(S.sc("無重力")):
    if i >= 8: ORGM.bar(b, K.mel(OS[i - 8], oct=4))

# ================= リードギター =================
RIFF = ["1':0.5 5:0.5 1':0.5 3':0.5 2':0.5 1':0.5 5:0.5 3:0.5", "3':0.5 7:0.5 3':0.5 5:0.5 3':0.5 2':0.5 1':0.5 7:0.5",
        "4':0.5 1':0.5 6:0.5 4:0.5 6:0.5 1':0.5 2':0.5 4':0.5", "4':0.75 1':0.25 b6:0.5 4:0.5 b6:0.5 1':0.5 5:1"]
for name in ("発射", "無重力"):
    for i, b in enumerate(S.sc(name)):
        if name == "無重力" and i >= 8: break
        LG.bar(b, K.mel(RIFF[i % 4] if not (name == "発射" and i >= 8) else seq_up(RIFF[i % 4], K, 2), oct=3))
SOLO = ["5:0.5 1':0.5 3':0.5 5':0.5 3':1 1':1", "3':0.5 5':0.5 7':0.5 5':0.5 3':2", "6':1 4':0.5 1':0.5 6:1 1':1", "4':0.75 3':0.25 b3':0.5 1':0.5 7:2",
        "1':0.25 2':0.25 3':0.25 5':0.25 3':0.25 2':0.25 1':0.5 5:0.5 1':0.5 3':1", "5':1.5 3':0.5 5':1 7':1", "1'':2 6':1 4':1", "b6':1 4':1 1':1 7:1",
        "5':0.5 5':0.5 6':0.5 5':0.5 3':0.5 5':0.5 1'':1", "7':0.5 7':0.5 1'':0.5 7':0.5 5':0.5 3':0.5 5':1", "6':0.5 1'':0.5 6':0.5 4':0.5 1':0.5 4':0.5 6':1", "4':2 b3':1 1':1",
        " ".join(["1'':0.125"] * 8) + " " + " ".join(["7':0.125"] * 8) + " 5':1 3':1", "3':1 5':1 7':1 1'':1", "6':1 1'':1 6':1 5':1", "5':4"]
for i, b in enumerate(S.sc("ギターソロ")): LG.bar(b, K.mel(SOLO[i], oct=3))

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    pw = power(ch, "E2")
    v = voice(ch, 64, 3)
    # 歪みのギター（パワーコード。ポップパンクの8分）
    gpat = None
    if n in ("発射", "無重力"): gpat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
    elif n.startswith("大気圏"): gpat = "X:1! R:1 X:1! R:1" if i < 8 else "X:1.5! X:0.5 X:1 X:1"
    elif n.startswith("加速"): gpat = ("X:0.5! X:0.5 " * 4).strip() if i < 7 else "X:2! R:2"
    elif n in ("輪っか", "輪っかを抜ける"): gpat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
    elif n == "輪っか2": gpat = "X:2! X:1.5 X:0.5"                       # Half feel: のばす和音
    elif n.startswith("掛け声") or (n == "着陸" and i >= 8): gpat = "X:0.5! R:0.5 X:0.5! R:0.5 X:0.5 X:0.5 X:1"
    elif n == "ただよう" and i >= 8: gpat = "X:4!"
    elif n == "ギターソロ": gpat = "X:1.5! X:1 X:1.5"
    elif n == "再突入": gpat = "X:2! X:2" if i < 4 else ("X:0.5 " * 8).strip()
    elif n == "着陸": gpat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
    if n == "着陸" and i == L - 1: gpat = "X:1! R:3"
    if gpat:
        for j in range(2):
            GL[j].bar(b, gpat.replace("X", nm(pw[j])))
            GR[j].bar(b, gpat.replace("X", nm([pw[0], pw[2]][j])))
    # オルガン（裏のスタブ・のばす和音）
    opat = None
    if n.startswith("大気圏"): opat = "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if i >= 4 else None
    elif n.startswith("加速"): opat = "X:4" if i < 7 else "X:2 R:2"
    elif n in ("輪っか", "輪っか2", "輪っかを抜ける"): opat = "X:2 X:2" if n != "輪っか2" else "X:4"
    elif n == "無重力": opat = "X:4" if i < 8 else None
    elif n == "ただよう": opat = "X:4"
    elif n == "再突入": opat = "X:4"
    if opat:
        if n.startswith("大気圏2") and i < 8: opat = None          # オルガンが歌を受け取る所は和音を休む
    if opat:
        for j in range(3): ORG[j].bar(b, opat.replace("X", nm(v[j])))
    # ベース（根音に沿わせる。サビは8分のオクターブ）
    r = low(ch, "E1")
    if n == "秒読み": BASS.bar(b, f"{nm(r)}:4" if i == 3 else "R:4")
    elif n in ("発射", "無重力"): BASS.bar(b, bass_line(S, b, "root8"))
    elif n.startswith("大気圏"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "root8"))
    elif n.startswith("加速"): BASS.bar(b, bass_line(S, b, "root8") if i < 7 else f"{nm(r)}:2 R:2")
    elif n in ("輪っか", "輪っかを抜ける"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "輪っか2": BASS.bar(b, bass_line(S, b, "half"))
    elif n.startswith("掛け声"): BASS.bar(b, f"{nm(r)}:0.5 R:0.5 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5 {nm(r)}:0.5 {nm(r + 12)}:1")
    elif n == "ただよう": BASS.bar(b, bass_line(S, b, "long") if i < 8 else bass_line(S, b, "half"))
    elif n == "ギターソロ": BASS.bar(b, bass_line(S, b, "root8"))
    elif n == "再突入": BASS.bar(b, bass_line(S, b, "long" if i < 4 else "root8"))
    elif n == "着陸": BASS.bar(b, bass_line(S, b, "root8") if i < L - 1 else f"{nm(r)}:1 R:3")
    # 手拍子（2拍・4拍。掛け声の所は細かく）
    if n.startswith("掛け声"): CLAP.bar(b, "R:1 G3:1 R:1 F3:0.5 E3:0.5" if i % 2 else "R:1 G3:1 R:1 G3:0.5 F3:0.5")
    elif n in ("輪っか", "輪っかを抜ける") and i % 8 >= 4: CLAP.bar(b, "R:1 G3:1 R:1 G3:1")
    elif n == "発射" and i >= 4: CLAP.bar(b, "R:1 G3:1 R:1 G3:1")
    elif n == "秒読み" and i == 3: CLAP.bar(b, "R:2 E3:0.5 F3:0.5 G3:0.5 G3:0.5")

riser(FX, S.sc("輪っか")[0], 4, "C4"); riser(FX, S.sc("輪っかを抜ける")[0], 16, "D4")
FX.bar(S.sc("ただよう")[0], "G4:4")                         # 宇宙に出た「ドーン」（サブドロップ）
cym_swell(CYM, S.sc("発射")[0], 2, "C4"); cym_swell(CYM, S.sc("無重力")[0], 2, "C4"); cym_swell(CYM, S.sc("輪っか2")[0], 2, "C4"); cym_swell(CYM, S.sc("ギターソロ")[0], 4, "E4")

# ================= ドラム =================
def ride8(b, first="C2"):
    D.cym(b, f"{first}:0.5 " + "D2:0.5 " * 7); D.H[b] = "." * 16


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "秒読み":
        D.set(b, "." * 16, "." * 16, "x.......x......." if i < 3 else "x.x.x.x.x.x.x.x.")
        if i == 3: D.set(b, "X.......X.X.X.X.", "........XXXXXXXX", "." * 16)
    elif n in ("発射", "無重力"):
        vgroove(D, b, "punk" if n == "発射" else "beat8", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if n == "無重力" and i >= 4: ride8(b, "C2" if i == 4 else "D2")
        if last: put_fill(D, b, "tomdown")
    elif n.startswith("大気圏"):
        vgroove(D, b, "beat8" if i < 8 else "vrock2", ghosts=0.4, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("加速"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 4: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1); D.cym(b, "C2:1")
    elif n == "輪っか":                            # 1回目: 8ビート
        vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if i == 7 else "tomdown")
    elif n == "輪っか2":                           # 2回目: Half feel（サビごとにリズムを入れかえる）
        vgroove(D, b, "halfdrive", ghosts=0.45, seed=b)
        if 4 <= i < 12: D.cym(b, ("C2:1 " if i == 4 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "B2")
        if i % 8 == 7: put_fill(D, b, "tomtrip" if i == 7 else "tomdown")
    elif n.startswith("掛け声"):
        vgroove(D, b, "punk", ghosts=0.2, seed=b, s="....X.......X.X.")
        if i == 0: crash(D, b)
        if last and n == "掛け声": put_fill(D, b, "small")
    elif n == "ただよう":
        if i < 8: D.set(b, "." * 16, "." * 16, "." * 16 if i < 4 else "x...x...x...x...")
        else:
            vgroove(D, b, "half", ghosts=0.4, seed=b, h="x...x...x...x...")
            if not last: D.cym(b, ("C2:1 " if i == 8 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "lift")
    elif n == "ギターソロ":
        vgroove(D, b, "vrock2", ghosts=0.35, seed=b)
        if i % 8 == 0: crash(D, b)
        if i % 4 == 3: put_fill(D, b, "small" if i % 8 == 3 else "tomdown")
    elif n == "再突入":
        D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")
        if i >= 4: D.set(b, "X...X...X...X...", "....X.......X...", "xxxxxxxxxxxxxxxx")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X.......", "xxxxXXXXXXXX....", "." * 16)
    elif n == "輪っかを抜ける":                     # 最後: 2ビート（ポップパンク）
        vgroove(D, b, "punk", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if 8 <= i < 16: ride8(b, "D2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomdown")
        if last: put_fill(D, b, "snare16")
    elif n == "着陸":
        vgroove(D, b, "punk", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if last: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16)

# 止め・宇宙の無音2拍・1拍の完全な無音・急停止
SIL.add(S.sc("加速")[-1], 1, 4); SIL.add(S.sc("加速2")[-1], 1, 4)
SIL.add(S.sc("掛け声2")[-1], 2, 4)                 # 宇宙の無音（2拍）
SIL.add(S.sc("再突入")[-1], 3, 4)                  # 1拍の完全な無音（転調の直前）
SIL.add(S.sc("着陸")[-1], 1, 4)                    # 急に止める
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の09。ポップパンク。A長調・208（最後のサビは B長調 +2）。自転車にロケットをつけて、友だちと土星の輪っかを一周する。"
          "歌の役の秒読みで始まり、ギターのリフで発射、16分で跳ねる Aメロ、増三和音で止める Bメロ、同じ音の3連打で呼びかけるサビ（1回目8ビート・2回目 Half feel・最後は2ビート）、"
          "♭VII の掛け声、オルガンが歌を受け取る2番、宇宙の無音2拍からただよう Cメロ、ギターソロ、1拍の無音のあと +2 の最後のサビ、急に止めて終わる。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
