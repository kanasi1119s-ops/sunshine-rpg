# vb25 15「フライパン・オーケストラ」Frying Pan Orchestra（仮）— ヒップホップ（トラップ）。Gm（サビは B♭）・104（ハーフの型。倍の 208 で感じる）・4/4。
#   最後のサビは +2（Am／C）
# 物語: 夕方の台所。包丁のリズムで下ごしらえが始まり、鍋とフライパンたちが晩ごはんのために演奏会を開く。
#   お湯がわくまで、みんなでじっと待つ。わいたら一気に全員そろって大合唱。最後は「いただきます」の和音。
# 場面と強さ: 包丁（打楽器だけ・小→中）→ 下ごしらえ（Aメロ・語る）→ 火をつける（Bメロ・溜め・止め）→ 鍋がそろう（サビ・強）
#   → お湯がわくまで（静けさ）→ 2品目（ピッツィカートが歌を受け取る）→ 火を強く（Bメロ）→ 強火（2回目のサビ・倍のノリに入れかえ）
#   → 鍋のソロ（大小の鍋が旋律を叩く）→ 1拍の無音 → 全部の鍋の大サビ（+2・最大）→ いただきます（和音）
# 旋律の性格: Aメロは低め（D4〜E♭5）で、16分と16分の3連が跳ねる早口。サビは「タタタン」の同じ音の連打のフックと、5度の跳躍
# 派手な展開: トラップのハット・サビごとのリズムの入れかえ（トラップ → 倍のノリ）・最後のサビ +2・止め2回・1拍の完全な無音
# 定番以外のコード: A♭（♭II）・B♭aug（増三和音）・G7（ii への副属和音）
from vb25_lib import *

S = Song("15", "frypan", "フライパン・オーケストラ（仮）", "Frying Pan Orchestra", 104, 4, "G", "minor", "ヒップホップ（トラップ・ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # G の短調
KB = Key("Bb", "major")      # サビ（平行調）
KC = Key("C", "major")       # 最後のサビ（+2）
KAm = Key("A", "minor")

A_CH = ["Gm", "F", "Ebmaj7", "Ab"]
B_CH = ["Cm7", "D7", "Ebmaj7", "F", "Cm7", "D7", "Ebmaj7", "D7"]
C_CH = ["Ebmaj7", "F", "Dm7", "Gm7", "Ebmaj7", "F", "Bb", "Bbaug"]
C_CH2 = ["Ebmaj7", "F/A", "Bb", "G7", "Cm7", "F7", "Bb", "D7"]
WAIT = ["Gm7", "Ebmaj7", "Cm7", "D7sus4", "Gm7", "Ebmaj7", "Abmaj7", "D7"]
LAST = [tr_chord(c, 2) for c in C_CH] + [tr_chord(c, 2) for c in C_CH2[:6]] + ["Dm7", "G7"]

S.scene("包丁", 8, "intro", A_CH)
S.scene("下ごしらえ", 16, "verse", A_CH)
S.scene("火をつける", 8, "pre", B_CH)
S.scene("鍋がそろう", 16, "chorus", C_CH + C_CH2)
S.scene("お湯がわくまで", 8, "break", WAIT)
S.scene("2品目", 8, "verse", A_CH)
S.scene("火を強く", 8, "pre", B_CH)
S.scene("強火", 16, "chorus", C_CH + C_CH2)
S.scene("鍋のソロ", 8, "solo", A_CH[:3] + ["D7"])
S.scene("全部の鍋", 16, "chorus", LAST)
S.scene("盛りつけ", 4, "outro", ["Fmaj7", "G", "Em7", "Am7"])
S.scene("いただきます", 2, "outro", ["Cmaj9", "Cmaj9"])

V = Voice(S, vol=0.22, delay=0.75)
PZS = dict(patch="pizzicato", volume=0.12, pan=0.35, reverb=0.3, sustain=0.6)
PZ = [S.track(f"ピッツィカート{i + 1}", "strings", **PZS) for i in range(2)]
PZM = S.track("ピッツィカート（歌の受け渡し）", "strings", **PZS)
B808 = S.track("808", "sub808", volume=0.2, pan=0, sustain=1.0, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7},
                                                                        {"type": "eq", "low": -2, "mid": 3, "midHz": 900, "high": 0}])
KNIFE = S.track("包丁とまな板（カホン）", "cajon", volume=0.14, pan=-0.3, reverb=0.12)
POT = S.track("鍋（大小のロートタム）", "rotoTom", patch="rotoTom", volume=0.13, pan=0.15, reverb=0.2)
LID = S.track("鍋のふた（短い FM ベル）", "fmBell", volume=0.05, pan=-0.45, reverb=0.15, sustain=0.25,
              fx=[{"type": "filter", "kind": "highpass", "freq": 900, "q": 0.7}])
GLS = S.track("グラスの音（泡）", "bell", patch="glassPluck", volume=0.06, pan=0.5, sustain=0.6, reverb=0.45,
              fx=[{"type": "filter", "kind": "highpass", "freq": 600, "q": 0.7}])
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.05, pan=-0.5, duck=0.4, sustain=0.9)) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役 =================
# Aメロ（G の短調・oct 4）: 16分と16分の3連（0.1667）の早口。A♭ の小節は ♭2（A♭）
VA = ["1:0.25 1:0.25 1:0.25 R:0.25 3:0.25 1:0.25 R:0.25 5,:0.25 1:0.1667 1:0.1667 1:0.1666 3:0.5 4:0.25 3:0.25 1:0.5",
      "R:0.25 2:0.25 2:0.25 2:0.25 4:0.25 2:0.25 7,:0.5 R:0.25 7,:0.25 2:0.25 4:0.25 5:0.5 4:0.5",
      "3:0.25 3:0.25 1:0.25 6,:0.25 R:0.25 6,:0.25 1:0.25 3:0.25 5:0.333 3:0.333 1:0.334 3:0.5 R:0.5",
      "b2:0.25 b2:0.25 4:0.25 6:0.25 R:0.25 6:0.25 4:0.25 b2:0.25 1:1 R:0.5 5,:0.25 7,:0.25",
      "R:0.25 1:0.25 3:0.25 5:0.25 1':0.5 5:0.25 3:0.25 R:0.25 3:0.25 4:0.25 3:0.25 1:0.5 R:0.5",
      "7,:0.1667 1:0.1667 2:0.1666 4:0.5 2:0.25 7,:0.25 R:0.5 2:0.25 4:0.25 5:0.25 4:0.25 2:0.5 R:0.5",
      "R:0.25 5:0.25 5:0.25 5:0.25 3:0.25 5:0.25 7:0.5 5:0.25 3:0.25 1:0.25 3:0.25 5:1",
      "4:0.25 4:0.25 b2:0.25 6,:0.25 R:0.25 b2:0.25 4:0.25 6:0.25 5:0.333 4:0.333 b2:0.334 1:1",
      "1:0.333 3:0.333 5:0.334 R:0.25 5:0.25 4:0.25 3:0.25 1:0.25 1:0.25 R:0.25 5,:0.25 1:0.5 3:0.5",
      "2:0.333 4:0.333 6:0.334 R:0.25 6:0.25 5:0.25 4:0.25 2:0.25 2:0.25 R:0.25 7,:0.25 2:0.5 4:0.5",
      "R:0.25 3:0.25 3:0.25 3:0.25 5:0.25 3:0.25 1:0.25 6,:0.25 R:0.5 1:0.25 3:0.25 5:0.5 7:0.5",
      "1':0.25 7:0.25 6:0.25 4:0.25 b2:0.5 6,:0.5 R:0.25 b2:0.25 4:0.25 6:0.25 6:1",
      "5:0.25 5:0.25 5:0.25 R:0.25 4:0.25 3:0.25 R:0.25 1:0.25 3:0.1667 4:0.1667 3:0.1666 1:0.5 5,:0.5 R:0.5",
      "R:0.25 7,:0.25 2:0.25 4:0.25 R:0.25 4:0.25 5:0.25 7:0.25 6:0.5 4:0.5 2:1",
      "3:0.25 5:0.25 7:0.25 5:0.25 3:0.25 1:0.25 6,:0.5 R:0.25 6,:0.25 1:0.25 3:0.25 5:1",
      "4:0.5 b2:0.5 6,:0.5 b2:0.5 4:1 R:1"]
VA2 = ["R:0.25 5,:0.25 1:0.25 3:0.25 5:0.25 R:0.25 4:0.25 3:0.25 1:0.1667 3:0.1667 1:0.1666 5,:0.5 1:1",
       "R:0.25 7,:0.25 2:0.25 4:0.25 6:0.25 R:0.25 5:0.25 4:0.25 2:0.1667 4:0.1667 2:0.1666 7,:0.5 2:1",
       "3:0.25 3:0.25 5:0.25 3:0.25 1':0.5 R:0.25 7:0.25 6:0.25 5:0.25 3:0.25 1:0.25 3:1",
       "b2:0.25 4:0.25 6:0.25 1':0.25 R:0.5 6:0.25 4:0.25 b2:0.5 1:0.5 R:1"]
# Bメロ: 8分で上へ（火をつける）。最後は止め
VB = ["4:0.5 4:0.5 6:0.5 4:0.5 R:0.5 1':0.5 7:0.5 6:0.5", "5:1 #7:0.5 2':0.5 #7:1 R:1",
      "6:0.5 6:0.5 1':0.5 6:0.5 R:0.5 3':0.5 2':0.5 1':0.5", "2':1.5 1':0.5 7:1 R:1",
      "4':0.5 4':0.5 3':0.5 1':0.5 R:0.5 6:0.5 1':0.5 3':0.5", "2':1 #7:0.5 2':0.5 5:1 #7:1",
      "3':0.5 2':0.5 1':0.5 6:0.5 1':0.5 3':0.5 2':0.5 1':0.5", "#7:1 R:3"]
VB2 = ["4:0.25 4:0.25 4:0.5 6:0.5 4:0.5 R:0.5 1':0.5 7:0.25 6:0.25 5:0.5", VB[1],
       "6:0.25 6:0.25 6:0.5 1':0.5 6:0.5 R:0.5 3':0.5 2':0.25 1':0.25 7:0.5", VB[3], VB[4], VB[5],
       "3':0.25 2':0.25 1':0.25 6:0.25 1':0.25 3':0.25 2':0.25 1':0.25 #7:0.5 2':0.5 3':0.5 #7:0.5", "2':1 R:3"]
# サビ（B♭長調・oct 4）: 「タタタン」の同じ音の連打 → 5度の跳躍 → C6
VC = ["5:0.25 5:0.25 5:0.5 R:0.5 5:0.5 6:0.5 1':0.5 6:1", "5:0.25 5:0.25 5:0.5 R:0.5 5:0.5 2':1.5 R:0.5",
      "3:0.25 3:0.25 3:0.5 R:0.5 3:0.5 4:0.5 6:0.5 5:1", "6:1 5:0.5 4:0.5 3:0.5 2:0.5 1:1",
      "5:0.25 5:0.25 5:0.5 R:0.5 5:0.5 6:0.5 1':0.5 6:1", "5:0.25 5:0.25 5:0.5 R:0.5 1':0.5 2':1.5 R:0.5",
      "1':0.5 2':0.5 1':0.5 6:0.5 5:1 3:1", "#5:1 3:1 #5:1 1':1",
      "5:0.25 5:0.25 5:0.5 R:0.5 5:0.5 6:0.5 1':0.5 6:1", "5:0.25 5:0.25 5:0.5 R:0.5 5:0.5 2':1.5 R:0.5",
      "3:0.25 3:0.25 3:0.5 R:0.5 3:0.5 5:0.5 1':1 R:0.5", "3:0.5 #1':0.5 6:0.5 5:0.5 #1':1 6:1",
      "2':0.25 2':0.25 2':0.5 R:0.5 1':0.5 6:0.5 4:0.5 2:1", "5:0.5 6:0.5 4:0.5 5:0.5 1':1 7:1",
      "1':1.5 6:0.5 5:1 3:1", "#5:1 7:1 #5:1 R:1"]
# 2回目のサビ（倍のノリ）: 連打を16分の3連にして、もっと速く
T3 = "5:0.1667 5:0.1667 5:0.1666 5:0.5"
VC2 = [f"{T3} R:0.5 5:0.5 6:0.5 1':0.5 6:1", f"{T3} R:0.5 1':0.5 2':1.5 R:0.5"] + VC[2:4] + \
      [f"{T3} R:0.5 5:0.5 6:0.5 1':0.5 6:1", f"{T3} R:0.5 1':0.25 2':0.25 3':0.5 2':1 R:0.5"] + VC[6:12] + \
      ["2':0.1667 2':0.1667 2':0.1666 2':0.5 R:0.5 1':0.5 6:0.5 4:0.5 2:1"] + VC[13:]
# 最後のサビ（C長調）: 最高音 D6
VCL = VC[:14] + ["6:1 1':1 2':2", "2':1 7:1 5:2"]
VTAG = ["3:1 5:1 6:2", "7:1 5:1 2':2", "1':1.5 7:0.5 5:1 3:1", "6:4"]

for i, b in enumerate(S.sc("下ごしらえ")): V.bar(b, K.mel(VA[i], oct=4))
for i, b in enumerate(S.sc("2品目")):
    if i < 4: PZM.bar(b, K.mel(VA[i], oct=5))            # 前半はピッツィカートが歌を受け取る
    else: V.bar(b, K.mel(VA2[i - 4], oct=4))
for i, b in enumerate(S.sc("火をつける")): V.bar(b, K.mel(VB[i], oct=4))
for i, b in enumerate(S.sc("火を強く")): V.bar(b, K.mel(VB2[i], oct=4))
for i, b in enumerate(S.sc("鍋がそろう")): V.bar(b, KB.mel(VC[i], oct=4))
for i, b in enumerate(S.sc("強火")): V.bar(b, KB.mel(VC2[i], oct=4))
for i, b in enumerate(S.sc("全部の鍋")): V.bar(b, KC.mel(VCL[i], oct=5))
for i, b in enumerate(S.sc("盛りつけ")): V.bar(b, KC.mel(VTAG[i], oct=5))
V.bar(S.sc("いただきます")[0], KC.mel("1':6", oct=5))
# お湯がわくまで: 長い音でそっと（重ねなし）
VW = ["5:3 4:1", "3:4", "4:2 6:2", "5:4", "1':3 7:1", "5:4", "b2':2 1':1 6:1", "#7:2 R:2"]
for i, b in enumerate(S.sc("お湯がわくまで")): V.bar(b, K.mel(VW[i], oct=4), low=False)

# ================= 鍋のソロ（大小の鍋＝ロートタムが旋律を叩く） =================
POTS = {"大": "F2", "中": "A2", "小": "C3", "ちび": "D#3", "片手": "F3", "ミルク": "A3"}
PS = ["F2:0.5! C3:0.25 C3:0.25 A2:0.5 F3:0.25 F3:0.25 D#3:0.5 C3:0.5 A3:0.5 F3:0.5",
      "A2:0.5! D#3:0.25 D#3:0.25 C3:0.5 A3:0.25 A3:0.25 F3:0.5 D#3:0.25 C3:0.25 A2:0.5 F2:0.5",
      "F2:0.25! F2:0.25 C3:0.25 F3:0.25 A3:0.25 F3:0.25 C3:0.25 F2:0.25 F2:0.25 A2:0.25 D#3:0.25 A3:0.25 F3:0.5 C3:0.5",
      "A3:0.25! A3:0.25 F3:0.25 F3:0.25 D#3:0.25 D#3:0.25 C3:0.25 C3:0.25 A2:0.25 A2:0.25 F2:0.25 F2:0.25 F2:1"]
for i, b in enumerate(S.sc("鍋のソロ")): POT.bar(b, PS[i % 4] if i < 7 else PS[3])
# 鍋は、サビの合いの手（4小節目ごと）と、包丁の場面にも
for name in ("鍋がそろう", "強火", "全部の鍋"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: POT.bar(b, "R:2.5 A3:0.25 F3:0.25 D#3:0.25 C3:0.25 A2:0.5")
for i, b in enumerate(S.sc("包丁")):
    if i == 7: POT.bar(b, "R:2 F3:0.5 D#3:0.5 C3:0.5 F2:0.5")

# 包丁とまな板（カホンのスラップと胴）
KN = ["E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! F3:0.25, D3:0.25 F3:0.25, E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! E3:0.25 D3:0.5",
      "E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! R:0.25 D3:0.25 F3:0.25, E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! F3:0.25 E3:0.25 E3:0.25"]
for i, b in enumerate(S.sc("包丁")): KNIFE.bar(b, KN[i % 2] if i < 6 else ("A2:1! " + KN[1].split(" ", 4)[-1] if i == 6 else KN[0]))
for name in ("下ごしらえ", "2品目"):
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 0: KNIFE.bar(b, "R:3 E3:0.25! F3:0.25, E3:0.25 E3:0.25")
# 鍋のふた（短い FM ベル）: サビの裏拍
for name in ("鍋がそろう", "全部の鍋", "鍋のソロ"):
    for i, b in enumerate(S.sc(name)):
        LID.bar(b, "R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.75 G6:0.25" if i % 2 else "R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.5 D6:0.5")

# グラスの音（お湯の泡がだんだん増える）
rnd = random.Random(15)
for i, b in enumerate(S.sc("お湯がわくまで")):
    ts = tones(S.chords[b], "C6", "C7")
    n_ = 1 + i
    for j in range(n_):
        st = rnd.choice([x * 0.5 for x in range(8)])
        GLS.at(S.bar_beat(b) + st, f"{nm(rnd.choice(ts))}:0.5")
for i, b in enumerate(S.sc("鍋がそろう") + S.sc("全部の鍋")):
    if i % 8 == 7: GLS.bar(b, " ".join(f"{nm(m)}:0.25" for m in tones(S.chords[b], "C6", "C7")[:4]) + " R:3")

# ================= ピッツィカート（和音の分散） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "包丁" and i < 2: continue
    if n in ("いただきます",): continue
    t = tones(ch, "G3", "G5")
    if n in ("包丁", "下ごしらえ", "鍋のソロ") or (n == "2品目" and i >= 4):
        seq = [t[q % len(t)] for q in (0, 2, 1, 3, 2, 4, 3, 1)]
        PZ[0].bar(b, " ".join(f"{nm(m)}:0.5" for m in seq))
    elif n.startswith("火を"):
        v = voice(ch, 64, 2)
        for j in range(2): PZ[j].bar(b, " ".join(f"{nm(v[j])}:0.5" for _ in range(8)) if i < 7 else f"{nm(v[j])}:1 R:3")
    elif n == "お湯がわくまで":
        PZ[0].bar(b, f"{nm(t[0])}:1 R:1 {nm(t[2 % len(t)])}:1 R:1")
    elif n == "2品目":
        v = voice(ch, 60, 2)
        for j in range(2): PZ[j].bar(b, f"{nm(v[j])}:1 R:1 {nm(v[j])}:0.5 R:1.5")
    elif n in ("鍋がそろう", "強火", "全部の鍋", "盛りつけ"):
        seq = [t[q % len(t)] for q in (0, 1, 2, 3, 2, 1, 3, 4)]
        PZ[0].bar(b, " ".join(f"{nm(m)}:0.25" for m in seq) + " " + " ".join(f"{nm(m)}:0.5" for m in seq[:4]))

# 厚い和音（サビだけ）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("鍋がそろう", "強火", "全部の鍋", "盛りつけ", "いただきます"):
        v = voice(S.chords[b], 62, 3)
        if n == "いただきます":
            if i == 0:
                for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:6")
            continue
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5" if n != "強火" else f"{nm(v[j])}:4")

# ================= 808（キックの位置から長く鳴る） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C1")
    if r < midi("D1"): r += 12
    if n == "包丁":
        if i >= 4: B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:1 {nm(r)}:1.5")
    elif n in ("下ごしらえ", "2品目", "鍋のソロ"):
        B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r)}:1.5" if i % 2 == 0 else f"{nm(r)}:2.5! {nm(r + 7)}:0.5 {nm(r)}:1")
    elif n.startswith("火を"):
        B808.bar(b, f"{nm(r)}:2! {nm(r)}:2" if i < 7 else f"{nm(r)}:1! R:3")
    elif n in ("鍋がそろう", "全部の鍋", "盛りつけ"):
        B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:0.5 {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r)}:1")
    elif n == "強火":
        B808.bar(b, " ".join(f"{nm(r + (12 if q % 2 else 0))}:0.5" for q in range(8)))       # 倍のノリ: 8分のオクターブ
    elif n == "お湯がわくまで":
        if i % 2 == 0: B808.bar(b, f"{nm(r)}:4")
    elif n == "いただきます" and i == 0:
        B808.bar(b, f"{nm(low('C', 'C1') + 12)}:6")

# 効果音
riser(FX, S.sc("鍋がそろう")[0], 4, "C4"); riser(FX, S.sc("強火")[0], 4, "C4")
FX.bar(S.sc("お湯がわくまで")[0], "G4:4")                    # 火を止めた「ドーン」
cym_swell(CYM, S.sc("全部の鍋")[0], 4, "E4"); cym_swell(CYM, S.sc("鍋のソロ")[0], 2, "C4")

# ================= ドラム（電子のドラム・トラップ） =================
TRAPH = ["xxxxxxxxxxxxXxXx", "x.x.xxxxx.x.XXXX", "xxxxx.x.xxxxx.xx", "x.x.x.x.xxxxXXXX"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "包丁":
        if i >= 4: vgroove(D, b, "trap", ghosts=0, seed=b, h=TRAPH[i % 4], vary=False)
        if i == 4: crash(D, b, "G2")
    elif n in ("下ごしらえ", "2品目"):
        vgroove(D, b, "trap", ghosts=0.2, seed=b, h=TRAPH[i % 4], vary=False,
                k="X.......X.X....." if i % 2 == 0 else "X.....X...X..X..")
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("火を"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("鍋がそろう", "全部の鍋"):
        vgroove(D, b, "trap", ghosts=0.2, seed=b, h=TRAPH[(i + 1) % 4], vary=False,
                k="X.......X.X....." if i % 4 != 3 else "X.....X.X...X.X.")
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown")
        if last and n == "鍋がそろう": D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.....")
    elif n == "強火":
        # サビごとのリズムの入れかえ: 倍のノリ（208 で感じるドラムンベース型）
        vgroove(D, b, "dnb", ghosts=0.35, seed=b, s="....X..o.o..X...")
        if i % 8 == 0: crash(D, b, "C2")
        if i % 4 == 3 and not last: put_fill(D, b, "snare16")
        if last: D.set(b, "X...............", "X...............", "................")
    elif n == "お湯がわくまで":
        D.set(b, "X......." * 2 if i >= 4 else "X" + "." * 15, "." * 16, "x...x...x...x..." if i >= 2 else "." * 16)
        if last: put_fill(D, b, "lift")
    elif n == "鍋のソロ":
        vgroove(D, b, "trap", ghosts=0.3, seed=b, h="x.x.x.x.x.x.x.x.", vary=False)
        D.cym(b, ("B2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16      # ライド
        if last: put_fill(D, b, "tomtrip")
    elif n == "盛りつけ":
        vgroove(D, b, "trap", ghosts=0.2, seed=b, h=TRAPH[i % 4], vary=False)
        if i == 0: crash(D, b, "G2")
        if last: put_fill(D, b, "snare16")
    elif n == "いただきます":
        if i == 0: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)

# 止め: 火をつける・火を強くの最後の小節（1拍だけ叩いて全員休み）。1拍の完全な無音: 最後のサビの直前
for name in ("火をつける", "火を強く"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("全部の鍋")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の15。ヒップホップ（トラップ）。Gm（サビは B♭）・104（倍の 208 で感じる）・最後のサビ +2。"
          "台所の鍋とフライパンの演奏会。包丁（カホン）のリズムで始まり、16分と16分の3連の早口の Aメロ、「タタタン」の連打のサビ、"
          "お湯がわくまでの静けさ（グラスの泡）、2回目のサビは倍のノリに入れかえ、大小の鍋（ロートタム）のソロ、1拍の無音から +2 の大サビ、"
          "最後は「いただきます」の和音。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
