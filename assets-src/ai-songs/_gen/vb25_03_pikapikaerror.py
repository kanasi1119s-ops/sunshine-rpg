# vb25 03「ぴかぴかエラーコード」Pika-Pika Error Code（仮）— テクノポップ（中速ダンス）。A短調（サビは平行調の C長調）・146・4/4。転調なし
# 物語: 商店街のすみの、しゃべる自動販売機。まちがえて覚えた言葉（「いらっしゃいまセン」「ありがとうござい、ました？」）で、
#   道行く人をつい笑わせてしまう。朝は通勤の人、昼は子どもたち、夕方には商店街じゅうがいっしょに歌い出す。夜、ひとりで明かりをともして、
#   次の日のための言葉をこっそり練習する。
# 場面と強さ: ピッ（電子音1つ）→ 朝の商店街（Aメロ・語る・中）→ 言いまちがいがふくらむ（Bメロ・溜め → 止め）→ 笑い声のサビ（4つ打ち・強）
#   → おつりのダンス（間奏・カウベル）→ 昼の子どもたち（2番。前半は FM ベルが歌を受け取る）→ Bメロ2（1拍の完全な無音）
#   → 商店街じゅうが歌い出す2サビ（ジャージークラブ・いちばん強い山）→ 故障中（チップのソロ・スタッター）
#   → 夜の自販機の明かり（静けさ・Half feel）→ 朝の点検（こもった音・ローパス）→ 新しい言葉のサビ（2ステップ → 4つ打ち）
#   → 「ありがとう」の和音で切る
# 旋律の性格: 同じ音の16分の連打が、ときどき半音や1音「言いまちがい」でずれる。リズムも16分ずつずれていく（同じ句が1つ遅れて入る）。
#   サビは同じ音の3連打のフックが、最後の1回だけ半音ずれる（F→F#、A→A♭）。最高音 C6
# 派手な展開: サビごとのリズムの入れかえ（4つ打ち→ジャージークラブ→2ステップ）・全員の止め3回（うち1回は1拍の完全な無音）・最後のサビ前のフィルター
from vb25_lib import *

S = Song("03", "pikapikaerror", "ぴかぴかエラーコード（仮）", "Pika-Pika Error Code", 146, 4, "A", "minor", "テクノポップ（ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # A 短調
KC = Key("C", "major")       # サビ（平行調）

A_CH = ["Am9", "Fmaj7", "G", "Em7", "Am9", "Fmaj7", "G", "E7"]
B_CH = ["Dm9", "G", "Cmaj7", "A7", "Dm9", "Em7", "Fmaj7", "E7"]                  # A7 = ii（Dm）への副属和音
C_CH = ["Fmaj7", "G7", "Em7", "Am7", "Dm7", "G7", "Cmaj7", "C7",
        "Fmaj7", "G7", "E7/G#", "Am7", "Dm7", "Fm6", "Em7", "E7"]                 # C7＝IV への副属和音、Fm6＝同主短調から借りた iv
NIGHT = ["Fmaj7", "Em7", "Dm9", "Cmaj7", "Bbmaj7", "Am9", "Dm7/G", "G",
         "Fmaj7", "Em7", "Dm9", "Cmaj7", "Bbmaj7", "Am9", "Bm7b5", "E7"]          # Bbmaj7＝♭II
CHECK = ["Am9", "Fmaj7", "Dm9", "E7sus4"]

S.scene("ピッ", 8, "intro", ["Am9", "Am9", "Fmaj7", "E7sus4", "Am9", "Fmaj7", "G", "E7"])
S.scene("朝の商店街", 16, "verse", A_CH)
S.scene("言いまちがい", 8, "pre", B_CH)
S.scene("笑い声のサビ", 16, "chorus", C_CH)
S.scene("おつりのダンス", 8, "interlude", A_CH)
S.scene("昼の子どもたち", 16, "verse", A_CH)
S.scene("言いまちがい2", 8, "pre", B_CH)
S.scene("商店街じゅうが歌う", 24, "chorus", C_CH + C_CH[:8])
S.scene("故障中", 8, "solo", A_CH)
S.scene("夜の自販機", 16, "bridge", NIGHT)
S.scene("朝の点検", 4, "build", CHECK)
S.scene("新しい言葉のサビ", 20, "chorus", C_CH + ["Fmaj7", "G7", "Cmaj7", "C7"])
S.scene("ありがとう", 6, "outro", ["Fmaj7", "G7", "Em7", "Am7", "Fmaj9", "Fmaj9"])

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75)
VOCO_FX = [{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7},
           {"type": "eq", "low": 0, "mid": 5, "midHz": 800, "high": 0}, {"type": "eq", "low": 0, "mid": 4, "midHz": 1600, "high": -2},
           {"type": "filter", "kind": "lowpass", "freq": 4500, "q": 0.8}, {"type": "plate", "mix": 0.25}]
VOCO = [S.track(f"ボコーダー風パッド{i + 1}", "pad", patch="polysynth", volume=0.06, pan=0.0, reverb=0.3, sustain=1.2, duck=0.3, fx=VOCO_FX) for i in range(3)]
MUF = [S.track(f"こもったパッド{i + 1}（朝の点検）", "pad", patch="polysynth", volume=0.07, pan=0.0, reverb=0.35, sustain=1.5,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}]) for i in range(3)]
COIN = S.track("FMベル（自販機の電子音・コイン）", "fmBell", volume=0.1, pan=0.25, reverb=0.35, sustain=0.6, gainDb=1)
COW = S.track("カウベル風（FMベルを短く）", "fmBell", volume=0.075, pan=-0.3, reverb=0.12, sustain=0.12,
              fx=[{"type": "eq", "low": -6, "mid": 5, "midHz": 820, "high": -2}])
CHIP = S.track("チップのリード（矩形波 25%）", "lead", patch="chipPulse25", volume=0.12, pan=-0.15, reverb=0.12, mono=True, gainDb=1, breath=True,
               fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.7},
                   {"type": "pingpong", "beats": 0.75, "mix": 0.12, "feedback": 0.2}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass2", vol=0.23, duck=0.25))
ARP = S.track("プラック", "pad", **pluck_spec("pluckSynth", vol=0.075, pan=0.35, delay=0.75, sustain=0.5))
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.05, pan=0.0, duck=0.45, sustain=0.9)) for i in range(3)]
PNFX = [{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}]
PN = [S.track(f"ピアノ（和音{i + 1}）", "piano", volume=0.1, pan=-0.15, reverb=0.22, fx=PNFX) for i in range(3)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.1, pan=-0.15, reverb=0.22, fx=PNFX)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役（A短調の度数。oct=4 で 1 = A4） =================
# Aメロ: 同じ音の16分の連打が「言いまちがい」でずれる（b2＝B♭、1つ上の音）。後半は同じ句が16分ずつ遅れて入る
A1 = ["1:0.25 1:0.25 1:0.25 1:0.25 1:0.25 1:0.25 1:0.25 b2:0.25 1:0.5 R:0.25 5,:0.25 7,:0.25 1:0.25 3:0.5",
      "R:0.25 6,:0.25 6,:0.25 6,:0.25 6,:0.25 6,:0.25 6,:0.25 7,:0.25 6,:0.5 R:0.25 3,:0.25 5,:0.25 6,:0.25 1:0.5",
      "R:0.5 7,:0.25 7,:0.25 7,:0.25 7,:0.25 7,:0.25 1:0.25 2:0.25 2:0.25 2:0.25 2:0.25 4:0.5 2:0.5",
      "3:0.5 2:0.25 1:0.25 7,:0.5 5,:0.5 R:0.25 5,:0.25 7,:0.25 2:0.25 3:1",
      "R:0.25 3:0.25 3:0.25 3:0.25 3:0.25 3:0.25 4:0.25 3:0.25 2:0.5 1:0.5 R:0.25 7,:0.25 1:0.25 2:0.25",
      "R:0.25 1:0.25 1:0.25 1:0.25 1:0.25 1:0.25 b2:0.25 1:0.25 6,:0.5 5,:0.5 R:0.25 6,:0.25 1:0.25 3:0.25",
      "2:0.25 2:0.25 2:0.25 2:0.25 R:0.25 2:0.25 2:0.25 2:0.25 R:0.5 2:0.25 2:0.25 4:0.5 5:0.5",
      "#7,:0.25 #7,:0.25 #7,:0.25 #7,:0.25 2:0.5 4:0.5 3:0.5 2:0.5 #7,:1"]
A1b = ["1:0.25 1:0.25 1:0.25 1:0.25 3:0.25 3:0.25 3:0.25 3:0.25 5:0.25 5:0.25 5:0.25 4:0.25 5:0.5 3:0.5",
       "R:0.25 3:0.25 3:0.25 3:0.25 1:0.25 6,:0.25 5,:0.25 6,:0.25 R:0.25 1:0.25 1:0.25 1:0.25 3:0.5 1:0.5",
       "R:0.25 2:0.25 2:0.25 2:0.25 7,:0.25 5,:0.25 4,:0.25 5,:0.25 R:0.25 7,:0.25 7,:0.25 1:0.25 2:0.5 4:0.5",
       "5:0.25 4:0.25 3:0.25 2:0.25 1:0.25 7,:0.25 5,:0.25 7,:0.25 3:1 R:1",
       "R:0.25 1:0.25 3:0.25 5:0.25 R:0.25 1:0.25 3:0.25 5:0.25 R:0.25 R:0.25 1:0.25 3:0.25 5:0.25 7:0.25 5:0.5",
       "R:0.25 6,:0.25 1:0.25 3:0.25 R:0.25 6,:0.25 1:0.25 3:0.25 R:0.25 R:0.25 6,:0.25 1:0.25 3:0.25 5:0.25 3:0.5",
       "2:0.25 2:0.25 2:0.25 2:0.25 2:0.25 3:0.25 2:0.5 R:0.5 4:0.5 2:0.5 7,:0.5",
       "#7,:1.5 R:0.5 R:2"]
# 2番の後半（歌が戻る所）: 1オクターブの跳びを16分で（歌いにくい所）
A2b = ["1:0.25 1':0.25 1:0.25 1:0.25 3:0.25 3:0.25 1':0.25 3:0.25 5:0.25 5:0.25 1':0.25 5:0.25 7:0.5 5:0.5",
       "R:0.25 6,:0.25 6:0.25 6,:0.25 1:0.25 1:0.25 6:0.25 1:0.25 3:0.25 3:0.25 6:0.25 3:0.25 5:0.5 3:0.5",
       "R:0.25 7,:0.25 7,:0.25 7,:0.25 2:0.25 2:0.25 2:0.25 #2:0.25 2:0.5 R:0.25 2:0.25 4:0.25 5:0.25 7:0.5",
       "5:0.75 4:0.25 3:0.5 2:0.5 3:1 R:1",
       A1b[4], A1b[5],
       "2:0.25 2:0.25 2:0.25 2:0.25 2:0.25 2:0.25 #2:0.25 2:0.25 4:0.5 5:0.5 7:0.5 5:0.5",
       "#7,:1 2:0.5 4:0.5 #7:2"]
# Bメロ: 8分で言いまちがいがふくらんでいく（同じ形を1段ずつ上げる）。最後は伸ばして止め
BM = ["4:0.5 4:0.5 6:0.5 4:0.5 3:1 1:1", "2:0.5 2:0.5 4:0.5 2:0.5 7,:1 R:1", "3:0.5 3:0.5 5:0.5 7:0.5 5:1 3:0.5 5:0.5",
      "#3:1 5:0.5 7:0.5 1':1.5 R:0.5", "6:0.5 6:0.5 1':0.5 6:0.5 4:1 6:1", "5:0.5 5:0.5 7:0.5 5:0.5 3:1 5:1",
      "6:0.5 7:0.5 1':1 7:0.5 6:0.5 5:1", "#7:3 R:1"]
BM2 = BM[:5] + ["7:0.5 7:0.5 2':0.5 7:0.5 5:1 7:1", "1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5 #7,:0.5", "#7:2 2':1 R:1"]
# サビ（C長調の度数。oct=4 で 1 = C4）: 同じ音の3連打のフック。最後の1回だけ半音ずれる
CH = ["R:0.5 3':0.5 3':0.5 3':0.5 2':0.5 1':0.5 3:1", "R:0.5 2':0.5 2':0.5 2':0.5 7:0.5 5:0.5 2':1",
      "R:0.5 7:0.5 7:0.5 7:0.5 5':1 3':1", "1':0.5 3':0.5 6':1 5':1 3':1",
      "R:0.5 4':0.5 4':0.5 4':0.5 3':0.5 2':0.5 6:1", "R:0.5 4':0.5 4':0.5 #4':0.5 5':1 2':1",
      "R:0.5 3':0.5 3':0.5 3':0.5 1'':1 7':1", "b7':1 5':0.5 3':0.5 1':2",
      "R:0.5 3':0.5 3':0.5 3':0.5 2':0.5 1':0.5 6:1", "R:0.5 2':0.5 2':0.5 2':0.5 1':0.5 7:0.5 5:1",
      "R:0.5 #5:0.5 #5:0.5 7:0.5 3':1 2':1", "1':0.5 3':0.5 6':1 5':1 3':1",
      "R:0.5 6':0.5 6':0.5 6':0.5 4':0.5 2':0.5 6:1", "R:0.5 b6':0.5 b6':0.5 b6':0.5 4':1 1':1",
      "R:0.5 5':0.5 1':0.5 2':0.5 5:1 7:1", "#5:1 7:1 2':1 3':1"]
# 2サビの後ろ8小節（商店街じゅうが歌う）: 呼びかけと答え。短い句を4回、いちばん高い C6 へ
CH2X = ["R:0.5 5':0.5 5':0.5 5':0.5 R:0.5 1':0.5 1':0.5 1':0.5", "R:0.5 5':0.5 5':0.5 5':0.5 6':1 5':1",
        "R:0.5 4':0.5 4':0.5 4':0.5 R:0.5 6:0.5 6:0.5 6:0.5", "R:0.5 4':0.5 4':0.5 4':0.5 5':1 7:1",
        "R:0.5 3':0.5 3':0.5 3':0.5 R:0.5 6:0.5 1':0.5 3':0.5", "6':1.5 5':0.5 4':1 3':1",
        "R:0.5 1'':0.5 1'':0.5 1'':0.5 7':0.5 5':0.5 2':1", "1'':2 7':1 R:1"]
LASTX = ["R:0.5 3':0.5 3':0.5 3':0.5 4':0.5 3':0.5 6:1", "R:0.5 2':0.5 2':0.5 2':0.5 4':0.5 5':0.5 7':1", "1'':3 R:1", "R:0.5 5':0.5 3':0.5 1':0.5 b7':2"]
for name, lines in (("朝の商店街", A1 + A1b), ("昼の子どもたち", None)):
    for i, b in enumerate(S.sc(name)):
        if lines: V.bar(b, K.mel(lines[i], oct=4)); continue
        if i < 8: COIN.bar(b, shift_oct(K.mel(A1[i], oct=4), 1))          # 2番の前半は、FM ベル（自販機の声）が歌を受け取る
        else: V.bar(b, K.mel(A2b[i - 8], oct=4))
for i, b in enumerate(S.sc("言いまちがい")): V.bar(b, K.mel(BM[i], oct=4))
for i, b in enumerate(S.sc("言いまちがい2")): V.bar(b, K.mel(BM2[i], oct=4))
for i, b in enumerate(S.sc("笑い声のサビ")): V.bar(b, KC.mel(CH[i], oct=4))
for i, b in enumerate(S.sc("商店街じゅうが歌う")): V.bar(b, KC.mel((CH + CH2X)[i], oct=4))
for i, b in enumerate(S.sc("新しい言葉のサビ")): V.bar(b, KC.mel((CH + LASTX)[i], oct=4))
# 夜の自販機: 長い音で、ひとりごとのように（重ねなし）。後半は少し高く
NM = ["R:1 1:1 3:1 5:1", "5:3 R:1", "4:1 3:1 1:1 3:1", "2:3 R:1", "b2:2 4:1 6:1", "5:2 7:2", "6:2 4:1 2:1", "2:4",
      "R:0.5 3:0.5 5:0.5 1':0.5 7:2", "5:2 7:1 2':1", "1':2 6:1 4:1", "5:3 3:1", "4:1 6:1 b2':1 6:1", "5:2 R:1 3:1", "2:1 4:1 6:1 1':1", "#7:4"]
for i, b in enumerate(S.sc("夜の自販機")): V.bar(b, K.mel(NM[i], oct=4), low=(i >= 8))
# 朝の点検: こもった声（1オクターブ下の重ねのパートに元の高さで）
for i, b in enumerate(S.sc("朝の点検")): V.low.bar(b, K.mel(["1:1 1:1 1:0.5 b2:0.5 1:1", "3:1 3:1 3:0.5 4:0.5 3:1", "4:1 4:1 6:1 1':1", "#7:4"][i], oct=4))
# ありがとう: 「あ・り・が・と・う」の5つの音で、最後の和音へ
AR = ["R:0.5 3':0.5 3':0.5 3':0.5 2':0.5 1':0.5 6:1", "R:0.5 2':0.5 2':0.5 2':0.5 1':0.5 7:0.5 5:1", "R:0.5 7:0.5 7:0.5 7:0.5 5':1 3':1",
      "1':0.5 3':0.5 6':1 5':2", "3':0.5 3':0.5 4':0.5 3':0.5 1':1 R:1"]
for i, b in enumerate(S.sc("ありがとう")[:5]): V.bar(b, KC.mel(AR[i], oct=4))

# ================= 自販機の電子音・コイン・カウベル =================
B0 = S.sc("ピッ")[0]
COIN.bar(B0, "E6:0.5 R:3.5")                                        # 電子音1つ「ピッ」
COIN.bar(B0 + 1, "R:2 B5:0.25 E6:1.75")                             # コインが落ちる「チャリン」
COIN.bar(B0 + 3, "R:3 E6:0.25 E6:0.25 B5:0.5")
def coin(b, off=3.0): COIN.bar(b, "B5:0.25 E6:0.75", off)
for name in ("笑い声のサビ", "商店街じゅうが歌う", "新しい言葉のサビ"):
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 3: coin(b, 3.0)
for b in S.sc("ピッ")[4:] + S.sc("故障中"): coin(b, 3.0) if (b % 4 == 1) else None
# カウベル（おつりのダンスと2サビの全部、新しい言葉のサビの後半）
COWP = ["R:0.5 G#5:0.5 R:0.5 G#5:0.25 G#5:0.25 R:0.5 G#5:0.5 R:0.5 C#6:0.5", "R:0.5 G#5:0.5 R:0.5 G#5:0.5 R:0.5 G#5:0.5 G#5:0.25 C#6:0.25 C#6:0.5"]
for i, b in enumerate(S.sc("おつりのダンス") + S.sc("商店街じゅうが歌う") + S.sc("新しい言葉のサビ")[8:16]): COW.bar(b, COWP[i % 2])

# ================= チップのリード（イントロのフック・おつりのダンス・故障中のソロ） =================
HOOK = ["1:0.25 1:0.25 1:0.25 b2:0.25 1:0.5 5:0.5 3:0.25 3:0.25 3:0.25 4:0.25 3:0.5 1:0.5",
        "6,:0.25 6,:0.25 6,:0.25 7,:0.25 6,:0.5 3:0.5 1:0.25 1:0.25 1:0.25 2:0.25 1:0.5 6,:0.5",
        "7,:0.25 7,:0.25 7,:0.25 1:0.25 7,:0.5 4:0.5 2:0.25 2:0.25 2:0.25 3:0.25 2:0.5 7,:0.5",
        "#7,:0.5 2:0.5 4:0.5 #7:0.5 R:2"]
for i, b in enumerate(S.sc("ピッ")[4:]): CHIP.bar(b, K.mel(HOOK[i], oct=4))
for i, b in enumerate(S.sc("おつりのダンス")): CHIP.bar(b, K.mel(HOOK[i % 4], oct=4) if i < 7 else K.mel("#7,:0.5 2:0.5 4:0.5 #7:0.5 1':2", oct=4))
SOLO = ["5:0.25 1':0.25 3':0.25 1':0.25 5:0.25 1':0.25 3':0.25 5':0.25 4':0.5 3':0.5 1':1",
        "3:0.25 6:0.25 1':0.25 6:0.25 3:0.25 6:0.25 1':0.25 3':0.25 2':0.5 1':0.5 6:1",
        "2':0.25 2':0.25 2':0.25 2':0.25 " * 2 + "4':0.25 4':0.25 4':0.25 4':0.25 5':1",
        "3':0.5 2':0.25 1':0.25 7:0.5 5:0.5 #7:2",
        "1':0.25 3':0.25 5':0.25 1'':0.25 5':0.25 3':0.25 1':0.25 5:0.25 1':0.5 b2':0.5 1':1",
        "6:0.5 1':0.5 3':0.5 6':0.5 5':1 3':1",
        "5:0.125 " * 8 + "4:0.125 " * 8 + "5:0.5 7:0.5 2':1",              # スタッター（同じ音の32分の連打）
        "#7:0.125 " * 8 + "2':0.125 " * 8 + "#7':2"]                       # スタッター
for i, b in enumerate(S.sc("故障中")): CHIP.bar(b, K.mel(SOLO[i].strip(), oct=4))

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    chorus = n in ("笑い声のサビ", "商店街じゅうが歌う", "新しい言葉のサビ")
    # ボコーダー風パッド: 和音の刻み（16分の裏を感じる「タ・タン」）。夜は伸ばす
    if n == "ピッ" and i >= 1: [VOCO[j].bar(b, f"{nm(v[j])}:4") for j in range(3)]
    elif n in ("朝の商店街", "昼の子どもたち", "おつりのダンス") or n.startswith("言いまちがい"):
        if n.startswith("言いまちがい") and i == 7: pass
        else: [VOCO[j].bar(b, f"R:0.5 {nm(v[j])}:1 R:0.5 {nm(v[j])}:0.75 {nm(v[j])}:1.25") for j in range(3)]
    elif chorus or n == "故障中":
        if n == "新しい言葉のサビ" and i >= 16 and i == L - 1: pass
        [VOCO[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5") for j in range(3)]
    elif n == "夜の自販機":
        vv = voice(ch, 60, 3); [VOCO[j].bar(b, f"{nm(vv[j])}:4") for j in range(3)]
    elif n == "朝の点検":
        [MUF[j].bar(b, f"{nm(v[j])}:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1 {nm(v[j])}:1.5") for j in range(3)]
    elif n == "ありがとう" and i < 4:
        [VOCO[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5") for j in range(3)]
    # 厚い和音（サビだけ）
    if chorus:
        for j in range(3): SAW[j].bar(b, f"{nm(v[j] + 12 if v[j] < 60 else v[j])}:4")
    # ピアノ（サビと Bメロの和音の刻み・左手）
    if chorus or n.startswith("言いまちがい"):
        if not (n.startswith("言いまちがい") and i == 7):
            vp = voice(ch, 67, 3)
            for j in range(3): PN[j].bar(b, " ".join(f"{nm(vp[j])}:0.5" + ("" if q % 2 == 0 else ",") for q in range(8)))
            r = low(ch, "C2"); PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:1 {nm(r)}:1.5")
    if n == "夜の自販機" and i >= 8:
        t = tones(ch, "A4", "A5"); PN[0].bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 1, 3)))
    # プラック（Aメロの後半・故障中・サビの後半）
    if (n in ("朝の商店街", "昼の子どもたち") and i >= 8) or n == "故障中" or (chorus and i >= 8):
        t = tones(ch, "A3", "A5"); ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" + ("," if q % 4 else "") for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 6, 5, 3, 2, 1)))
    # ベース
    if n == "ピッ": BASS.bar(b, bass_line(S, b, "house")) if i >= 4 else None
    elif n in ("朝の商店街", "昼の子どもたち"): BASS.bar(b, bass_line(S, b, "house" if i < 8 else "oct8"))
    elif n.startswith("言いまちがい"): BASS.bar(b, bass_line(S, b, "push") if i < 7 else f"{nm(low(ch, 'E1'))}:2")
    elif n == "笑い声のサビ" or n == "新しい言葉のサビ": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "商店街じゅうが歌う": BASS.bar(b, bass_line(S, b, "push" if i % 2 == 0 else "oct8"))
    elif n in ("おつりのダンス", "故障中"): BASS.bar(b, bass_line(S, b, "disco"))
    elif n == "夜の自販機": BASS.bar(b, bass_line(S, b, "long") if i < 8 else bass_line(S, b, "half"))
    elif n == "朝の点検": BASS.bar(b, f"{nm(low(ch, 'E1'))}:4")
    elif n == "ありがとう" and i < 4: BASS.bar(b, bass_line(S, b, "oct8"))

# 「ありがとう」の和音: Fmaj9 を1回だけ短く（全員）。そのあとは何も鳴らさない
BEND = S.sc("ありがとう")[5]
vF = voice("Fmaj9", 64, 4)
for j in range(3): VOCO[j].bar(BEND, f"{nm(vF[j + 1])}:1"); SAW[j].bar(BEND, f"{nm(vF[j + 1])}:1"); PN[j].bar(BEND, f"{nm(vF[j] + 12)}:1!")
PNL.bar(BEND, "F2:2"); BASS.bar(BEND, "F1:1"); COIN.bar(BEND, "C7:2")
V.bar(BEND, KC.mel("3':1", oct=4), low=False)

riser(FX, S.sc("笑い声のサビ")[0], 4, "C4"); riser(FX, S.sc("商店街じゅうが歌う")[0], 8, "D4")
FX.bar(S.sc("故障中")[0], "E4:4")                                   # 故障の「プシュー」（ダウンリフター）
FX.bar(S.sc("夜の自販機")[0], "G4:4")                               # サブドロップ（夜になる）
cym_swell(CYM, S.sc("新しい言葉のサビ")[0], 4, "E4")
cym_swell(CYM, S.sc("おつりのダンス")[0], 2, "C4")

# ================= ドラム（電子のドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ピッ":
        if i == 3: D.set(b, "." * 16, "........x.x.xxXX", "." * 16)
        elif i >= 4: vgroove(D, b, "four", seed=b); crash(D, b) if i == 4 else None
        if i == 7: put_fill(D, b, "small")
    elif n in ("朝の商店街", "昼の子どもたち"):
        if n == "昼の子どもたち" and i < 8: vgroove(D, b, "twostep", ghosts=0.3, seed=b)
        elif i < 8: vgroove(D, b, "four", seed=b, s="............X...")
        else: vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("言いまちがい"):
        if i < 4: vgroove(D, b, "half", ghosts=0.3, seed=b)
        elif i < 7: vgroove(D, b, "four16", seed=b)
        if i == 6: put_fill(D, b, "build")
        if last:
            if n == "言いまちがい": halt(D, b, 2)                          # 止め（1回目）: 後ろ2拍は全員休み
            else: vgroove(D, b, "four", seed=b)                             # 2回目は最後の1拍を完全な無音に（下の SIL）
    elif n == "笑い声のサビ":
        vgroove(D, b, "four", seed=b)                                      # 1サビは4つ打ち
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if not last else "tomdown")
    elif n == "商店街じゅうが歌う":
        vgroove(D, b, "jersey", ghosts=0.3, seed=b)                        # 2サビはジャージークラブ
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last: put_fill(D, b, "build")
    elif n == "おつりのダンス":
        vgroove(D, b, "disco", seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n == "故障中":
        vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b, "B2")
        if i >= 6: D.set(b, "X.X.X.X.XXXXXXXX", "....X.......X.XX", "x.x.x.x.x.x.x.x.")
    elif n == "夜の自販機":
        if i < 8: D.set(b, "." * 16, "." * 16, "x.......x......." if i >= 4 else "." * 16)
        else:
            vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
            if i == 8: crash(D, b, "C2", 8)
        if last: put_fill(D, b, "build")
    elif n == "朝の点検":
        D.set(b, "X...X...X...X...", "." * 16, "." * 16)
        if last: D.set(b, "X...X...X.X.XXXX", "............XXXX", "." * 16)
    elif n == "新しい言葉のサビ":
        vgroove(D, b, "twostep" if i < 8 else "four16", ghosts=0.3, seed=b)   # 3回目は2ステップ → 4つ打ち
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i < 16 else "tomtrip")
        if last: put_fill(D, b, "snare16")
    elif n == "ありがとう":
        if i < 4:
            vgroove(D, b, "four", seed=b)
            if i == 0: crash(D, b)
        elif i == 4: halt(D, b, 1); crash(D, b, "G2", 4)                    # 止め（3回目）: 1拍目だけ
        else: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)

SIL.add(S.sc("言いまちがい")[-1], 2, 4)                # 止め1: 後ろ2拍は全員休み
SIL.add(S.sc("言いまちがい2")[-1], 3, 4)               # 止め2: 1拍の完全な無音
SIL.add(S.sc("ありがとう")[4], 3, 4)                    # 止め3: 「ありがとう」の和音の前の1拍
SIL.add(S.sc("ありがとう")[5], 2, 4)                    # 和音のあとは何も鳴らさない（シンバルの余韻だけ）
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の03。テクノポップ（中速ダンス）。A短調（サビは C長調）・146・転調なし。"
          "しゃべる自動販売機が、まちがえて覚えた言葉で商店街の人を笑わせる。自販機の電子音1つで始まり、同じ音の16分の連打が半音ずれていく Aメロ、"
          "4つ打ちの1サビ、カウベルのおつりのダンス、ジャージークラブで商店街じゅうが歌う2サビ（いちばんの山）、チップのソロとスタッター、"
          "夜の自販機の静けさ、こもった朝の点検、2ステップから4つ打ちの最後のサビ、「ありがとう」の和音で切る。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
