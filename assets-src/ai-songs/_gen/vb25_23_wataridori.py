# vb25 23「ドキドキ渡り鳥」Heartbeat Migration（仮）— K-POP（ハウス×ジャージークラブ）。A 長調・150・4/4。最後のサビは +2（B）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（生まれた町を出て、大きな町へ旅立つ）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を E長調から 7半音下げて A長調にした（書くのは E長調の度数のまま、書き出しの前に下げる）。
# 物語: 春の風の駅前、みんなが見送りに来てくれた。笑っているけど、ほんとは泣きそう。夜の電車の窓から海が見える。
#   手紙の最後の「またね」がおまもり。雲の中で迷っても、風が道を教えてくれる。雲を抜けると、新しい町。「ここからだ」。
# 場面と強さ: 羽ばたき（効果音だけ）→ 出発（プラックのフック・中）→ Aメロ → 風に乗る（Bメロ・高くのびる・止め）
#   → 島が見える？（サビ・強。ハウスの4つ打ち）→ 夜の海（2番。BGM は前半プラックが歌を受け取る）→ サビ2（ジャージークラブに入れかえ）
#   → 渡りの途中（プラックのソロ）→ 1拍の完全な無音 → 雲の中（ドラムなし・パッドとしずくだけ・弱）
#   → 雲を抜ける（だんだん強く）→ 1拍のブレイク → 島が見えた（+2 の最後のサビ・最大）→ 島に着く → 波の音とフェードアウト
# 旋律の性格: Aメロは句の頭を休んで8分で語る。サビは「どき・どき」の2つの短い呼びかけから下りてくる「わたりどり」。最高音 E5（+2 のサビは F#5）。
# 定番以外の和音: Aメロの G#7（vi への副属和音）、雲を抜ける所の C#7（新しい調の属和音へ）
from vb25_lib import *

S = Song("23", "wataridori", "ドキドキ渡り鳥（仮）", "Heartbeat Migration", 150, 4, "E", "major", "K-POP（ハウス×ジャージークラブ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # E 長調（oct=4 で 1＝E4）
KF = Key("F#", "major")      # 最後のサビ（+2）


def chk(key, lines, beats=4):
    for l in lines: assert abs(total(key.mel(l, oct=4)) - beats) < 1e-6, ("拍の数", l)


A_CH = ["C#m7", "A", "B", "G#7"]
B_CH = ["Amaj7", "B", "G#m7", "C#m7", "F#m7", "E/G#", "A", "Bsus4"]
C_CH = ["A", "B", "G#m7", "C#m", "A", "B", "G#7", "C#m", "F#m7", "G#m7", "A", "B", "A", "B", "Bsus4", "E"]
CLOUD_CH = ["Amaj7", "G#m7", "F#m7", "E/G#", "Amaj7", "G#m7", "F#m7", "Bsus4"]
UP_CH = ["C#m7", "A", "B", "G#7", "C#m7", "A", "B", "C#7"]
LAST_CH = ["B", "C#", "A#m7", "D#m", "B", "C#", "A#7", "D#m", "G#m7", "A#m7", "B", "C#", "B", "C#", "C#sus4", "F#"]

S.scene("羽ばたき", 2, "intro", ["E", "E"])
S.scene("出発", 8, "intro", ["Amaj7", "B", "G#m7", "C#m7"])
S.scene("群れのおしゃべり", 16, "verse", A_CH)
S.scene("風に乗る", 8, "pre", B_CH)
S.scene("島が見える？", 16, "chorus", C_CH)
S.scene("夜の海", 16, "verse", A_CH)
S.scene("風に乗る2", 8, "pre", B_CH)
S.scene("島が見える？2", 16, "chorus", C_CH)
S.scene("渡りの途中", 8, "solo", ["Amaj7", "B", "G#m7", "C#m7", "F#m7", "G#m7", "A", "B"])
S.scene("雲の中", 16, "break", CLOUD_CH)
S.scene("雲を抜ける", 8, "build", UP_CH)
S.scene("島が見えた", 16, "chorus", LAST_CH)
S.scene("島に着く", 8, "outro", ["B", "C#", "D#m7", "F#", "B", "C#", "F#", "F#"])
# 2026-10-26 点数 7.5 を目指す: ベースを録音の指弾きに（7.22→7.60）・プラックを素直で明るい音色に（+0.12）
S.live_bass = True
S.patch_swap = {"modernPluck": "surgeNicePluck"}
S.scene("波", 8, "outro", ["F#maj7"] * 8)

V = Voice(S, vol=0.22, delay=0.75, patch="viola", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
PLK = S.track("プラック（群れ）", "pad", **pluck_spec("pluckSynth", vol=0.08, pan=0.4, delay=0.75, sustain=0.5))
PLM = S.track("プラック（歌の受け渡し・ソロ）", "pad", **pluck_spec("pluckSynth", vol=0.15, pan=0.4, delay=0.75, sustain=0.5))
DROP = S.track("しずく（ガラスのプラック）", "pad", patch="glassPluck", volume=0.08, pan=-0.45, sustain=1.0, reverb=0.5)
PN = [S.track(f"ハウスのピアノ{i + 1}", "piano", volume=0.1, pan=-0.2, reverb=0.2, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}]) for i in range(3)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.1, pan=-0.2, reverb=0.2, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.23, duck=0.3))
PAD = [S.track(f"空のパッド{i + 1}", "pad", **pad_spec("halo", vol=0.055, pan=0.0, duck=0.25, sustain=2.5)) for i in range(3)]
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.045, pan=0.0, duck=0.45, sustain=0.9)) for i in range(2)]
PERC = S.track("パーカッション（カホン）", "cajon", volume=0.14, pan=0.3, reverb=0.2)
FX = S.track("効果音（羽ばたき・ライザー）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
WAVE = S.track("波の音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.45, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（E長調の度数。oct=4 で 1 = E4。書き出しの前に全体を 7半音下げる） =================
VERSE = ["R:1 3:0.5 3:0.5 6:0.5 5:0.5 3:1", "4:1 3:1 1:1 R:1", "R:1 2:0.5 2:0.5 5:0.5 4:0.5 2:1", "3:1.5 2:0.5 R:2",
         "R:1 6:0.5 6:0.5 1':0.5 7:0.5 6:1", "4:1 6:1 R:2", "R:1 5:0.5 5:0.5 4:0.5 2:0.5 5:1", "#5:2 R:2",
         "R:0.5 3:0.5 3:0.5 3:0.5 1:0.5 3:0.5 6:1", "6:1 4:1 R:2", "R:0.5 2:0.5 2:0.5 2:0.5 4:0.5 5:0.5 7:1", "7:1 #5:1 R:2",
         "R:0.5 1':0.5 1':0.5 1':0.5 7:0.5 6:0.5 5:1", "6:1 1':1 4:1 R:1", "R:0.5 2:0.5 4:0.5 5:0.5 7:1 5:1", "#5:2 R:2"]
V1 = "えきまえのべんち/みんながきてる/はるかぜのなか/わらってるけど/このまちをでてく/おおきなまちへと/はねをためしにゆく/わたりどりさ"
V2 = "よるのでんしゃから/うみがみえたよ/まどのわたしは/あめふりがお/てがみのさいごに/またねってかいてた/むねにだきしめてる/おまもりだよ"
BM = ["R:1 6:1 1':1 3':1", "2':3 R:1", "R:1 5:1 7:1 2':1", "3':3 R:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':1 4':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 4':0.5 4':0.5 3':0.5 2':1 1':1", "2':1 R:3"]
P1 = "はばたけ/とおくへ/なみだはおあずけ/まえをむいて"
P2 = "そらまで/とどけと/かぜがせなかおす/ふりかえらず"
# サビ: 「どき・どき」の短い呼びかけから下りてくる「わたりどり」
DK = "R:0.5 1':0.5 3':0.5 R:0.5 R:0.5 1':0.5 3':0.5 R:0.5"
WT = "5':0.5 4':0.5 3':0.5 2':0.5 2':1 R:1"
CH = [DK, WT, "R:0.5 7:0.5 7:0.5 7:0.5 3':1 2':1", "1':1.5 6:0.5 R:2",
      DK, WT, "R:0.5 #5:0.5 7:0.5 2':0.5 3':1 2':1", "1':2 R:2",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':0.5 2':0.5 4':1", "3':1 2':1 7:1 R:1", "R:0.5 4':0.5 4':0.5 4':0.5 3':0.5 1':0.5 3':1", "2':2 R:2",
      DK, WT, "R:0.5 2':0.5 4':0.5 5':0.5 4':1 2':1", "1':3 R:1"]
C1 = "どき/どき/わたりどり/はじめてのそら/どき/どき/わたりどり/まだみぬまち/ふるさとにてをふって/またかえるから/どき/どき/わたりどり/とんでゆくよ"
C2 = "どき/どき/わたりどり/ほしぞらのした/どき/どき/わたりどり/はねがうずく/かぜのちずのさきに/なにがあるかな/どき/どき/わたりどり/むねがおどる"
C3 = "どき/どき/わたりどり/あたらしいまち/どき/どき/わたりどり/まいおりるよ/とどけげんきだよって/ここにすをはる/どき/どき/わたりどり/はじまりだよ"
CLOUD = ["R:1 3':1 2':1 1':1", "7:3 R:1", "R:1 6:1 1':1 2':1", "1':3 R:1", "R:1 3':1 4':1 5':1", "5':3 R:1", "R:1 4':1 3':1 2':1", "2':3 R:1"]
UP = ["R:0.5 6:0.5 6:0.5 1':0.5 3':1 1':1", "6:2 R:2", "R:0.5 5:0.5 5:0.5 7:0.5 2':1 7:1", "#5:2 R:2",
      "R:0.5 3':0.5 3':0.5 1':0.5 6:1 1':1", "4':2 R:2", "R:0.5 5:0.5 7:0.5 2':0.5 4':1 5':1", "#2':1 3':1 5':1 R:1"]
TAG = [DK, WT, "R:1 6:1 1':1 3':1", "1':4", "R:4", "R:4", "R:4", "R:4"]
chk(K, VERSE); chk(K, BM); chk(K, CH); chk(K, CLOUD); chk(K, UP); chk(KF, CH); chk(KF, TAG)

LY = Lyrics(S)
def put(name, key, lines, text, low=True, bars=None):
    bars = bars or S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    ob, om = [], []
    for i, (b, m) in enumerate(zip(bars, mel)):
        if lines[i] == "R:4": continue
        V.bar(b, m, low=low if not callable(low) else low(i)); ob.append(b); om.append(m)
    LY.flow(ob, om, text, name)
put("群れのおしゃべり", K, VERSE, V1)
if VOCAL: put("夜の海", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("夜の海")):
        if i < 8: PLM.bar(b, K.mel(VERSE[i], oct=5))   # BGM: プラックが歌を受け取る（1オクターブ上）
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("風に乗る", K, BM, P1); put("風に乗る2", K, BM, P2)
put("島が見える？", K, CH, C1); put("島が見える？2", K, CH, C2)
put("雲の中", K, CLOUD, "まいごの/とりにも/かぜがね/おしえる", bars=S.sc("雲の中")[4:12], low=False)
put("雲を抜ける", K, UP, "くもをぬけて/ひかりのなか/みおろしたら/あたらしいまちだ")
put("島が見えた", KF, CH, C3)
put("島に着く", KF, TAG, "どき/どき/わたりどり/はばたけ")

# ================= プラックのフックとソロ =================
HOOK = ["1':0.5 3':0.25 1':0.25 5:0.5 1':0.5 R:0.5 7:0.25 1':0.25 3':1", "2':0.5 4':0.25 2':0.25 7:0.5 2':0.5 R:0.5 1':0.25 2':0.25 4':1",
        "3':0.5 2':0.25 7:0.25 5:0.5 7:0.5 R:0.5 2':0.25 3':0.25 5':1", "4':1 3':0.5 2':0.5 1':2"]
chk(K, HOOK)
for i, b in enumerate(S.sc("出発")): PLM.bar(b, K.mel(HOOK[i % 4], oct=4) if i >= 2 else "")
SOLO = ["1':0.25 3':0.25 5':0.25 3':0.25 1':0.25 5:0.25 3:0.25 5:0.25 1':0.5 3':0.5 5':1",
        "2':0.25 4':0.25 5':0.25 4':0.25 2':0.25 7:0.25 5:0.25 7:0.25 2':0.5 4':0.5 5':1",
        "7:0.25 2':0.25 3':0.25 5':0.25 4':0.5 3':0.5 2':0.5 7:0.5 5:1",
        "6:0.25 1':0.25 3':0.25 5':0.25 4':0.5 3':0.5 1':2",
        "6:0.5 1':0.5 4':0.5 5':0.5 4':1 1':1", "7:0.5 2':0.5 3':0.5 5':0.5 3':1 7:1",
        "1':0.25 1':0.25 1':0.25 1':0.25 3':0.25 3':0.25 3':0.25 3':0.25 4':1 3':1", "2':2 R:2"]
chk(K, SOLO)
for i, b in enumerate(S.sc("渡りの途中")): PLM.bar(b, K.mel(SOLO[i], oct=4))

# ================= 伴奏 =================
def chords3(trs, b, ch, pat, center=64):
    vv = voice(ch, center, len(trs))
    for j, t in enumerate(trs):
        t.bar(b, " ".join(("R:" + x.split(":")[1]) if x.startswith("R") else f"{nm(vv[j])}:{x.split(':')[1]}" for x in pat.split()))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "羽ばたき": continue
    # ハウスのピアノ（裏の和音・付点）と左手
    if n == "出発" and i >= 4: chords3(PN, b, ch, "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5")
    elif n in ("群れのおしゃべり", "夜の海") and i >= 8: chords3(PN, b, ch, "X:0.75 X:0.75 X:0.5 R:0.5 X:0.75 X:0.75")
    elif n.startswith("風に乗る"): chords3(PN, b, ch, "X:2 X:2" if i < L - 1 else "X:2 R:2")
    elif n.startswith("島が見え"):
        chords3(PN, b, ch, "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if (n != "島が見える？2" or i >= 8) else "X:0.75 X:0.75 X:0.5 X:0.75 X:0.75 X:0.5")
        # 2026-10-26 人間「ミックスのバランスをよくするのが大事」: ピアノの左手が書き出しで F1〜E2 まで下がってベースとにごっていた（低音のにごり 48%）。
        #   G2 から数えて、鳴る高さを C2〜B2 に上げる（ベースの居場所を空ける）
        r = low(ch, "G2"); PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:1 {nm(r)}:1.5")
    elif n == "渡りの途中": chords3(PN, b, ch, "X:0.75 X:0.75 X:0.5 R:0.5 X:0.75 X:0.75")
    elif n == "雲を抜ける": chords3(PN, b, ch, "X:1 X:1 X:1 X:1" if i < 4 else "X:0.5 X:0.5 X:0.5 X:0.5 X:0.5 X:0.5 X:0.5 X:0.5")
    elif n == "島に着く": chords3(PN, b, ch, "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if i < 6 else ("X:8" if i == 6 else ""))
    # ベース（根音。サビはオクターブ、Aメロはハウスの裏）
    # 2026-10-26 人間「ミックスのバランスをよくするのが大事」: 書き出しで 7半音下がるため、E1 から数えたベースは A0〜G#1 になり、
    #   出ない音（A0・A#0）と自然な音域より低い音が 264 個あった（低音が抜ける）。B1 から数えて、鳴る高さを E1〜D#2 にする（LB）
    # 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 歌うベース（sing_bass。lo=35・hi=59 で書く＝鳴る高さ E1〜E3）を場面ごとに:
    #   Aメロ後半は、歌が休む小節で歩き（walk）、語る小節は押す（push）／Bメロ後半は上っていく／サビ1は前半オクターブのまま、後半から押す・駆ける／
    #   サビ2（ジャージークラブ）は付点で弾む ride／最後のサビは全部押す・駆ける／ソロは上って下りる／雲を抜ける所の後半は上っていく
    LB = "B1"; SB_ = lambda st: sing_bass(S, b, st, lo=35, hi=59)
    if n == "出発": BASS.bar(b, bass_line(S, b, "house", lo=LB) if i >= 4 else "R:4")
    elif n in ("群れのおしゃべり", "夜の海"):
        if i < 8: BASS.bar(b, bass_line(S, b, "house", lo=LB))
        else: BASS.bar(b, SB_("walk") if i % 2 == 1 else bass_line(S, b, "push", lo=LB))
    elif n.startswith("風に乗る"):
        if i < 4: BASS.bar(b, bass_line(S, b, "long", lo=LB))
        elif i < L - 1: BASS.bar(b, SB_("climb"))
        else: BASS.bar(b, f"{nm(low(ch, LB))}:2 R:2")
    elif n == "島が見える？": BASS.bar(b, bass_line(S, b, "oct8", lo=LB) if i < 8 else SB_("run" if i % 2 == 1 else "drive"))
    elif n == "島が見える？2": BASS.bar(b, SB_("run" if i % 4 == 3 else "ride"))
    elif n == "島が見えた": BASS.bar(b, SB_("run" if i % 2 == 1 else "drive"))
    elif n == "渡りの途中": BASS.bar(b, SB_("climb" if i % 2 == 0 else "fall"))
    elif n == "雲の中" and i >= 8: BASS.bar(b, bass_line(S, b, "long", lo=LB))
    elif n == "雲を抜ける": BASS.bar(b, bass_line(S, b, "root8", lo=LB) if i < 4 else SB_("climb"))
    elif n == "島に着く" and i < 7: BASS.bar(b, bass_line(S, b, "half" if i < 6 else "long", lo=LB))
    # パッド（空）
    if n in ("雲の中", "風に乗る", "風に乗る2", "雲を抜ける", "波", "出発") or n.startswith("島が見え") or n == "島に着く":
        vv = voice(ch, 58, 3)
        if n == "波": vv = voice("F#maj7", 58, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(vv[j])}:4")
    if n.startswith("島が見え"):
        vv = voice(ch, 66, 2)
        for j in range(2): SAW[j].bar(b, f"{nm(vv[j])}:1.5 {nm(vv[j])}:1 {nm(vv[j])}:1.5")
    # プラック（群れ: 8分の和音の音。サビは16分）
    t = tones(ch, "E4", "B5")
    if n in ("群れのおしゃべり",) or (n == "夜の海" and i >= 8):
        PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
    elif n.startswith("島が見え"):
        PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 6, 4, 3, 1)))
    # しずく（雲の中・波）
    if n == "雲の中":
        tt = tones(ch, "E5", "B5")
        DROP.bar(b, f"R:{[0.5, 1.5, 2.5, 1][i % 4]} {nm(tt[i % len(tt)])}:1 R:{4 - 1 - [0.5, 1.5, 2.5, 1][i % 4]}")
    if n == "波" and i < 6:
        DROP.bar(b, ["R:1 A#5:2 R:1", "R:2.5 C#5:1.5", "R:0.5 F5:2 R:1.5", "R:3 A#5:1", "R:1.5 F#5:2.5", "R:4"][i])

# パーカッション（カホン: 南の島へ近づくほど増える）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("群れのおしゃべり", "夜の海"): PERC.bar(b, "R:0.5 E3:0.25 R:0.25 R:1 R:0.5 E3:0.25 E3:0.25 D3:1" if i >= 8 else "R:4")
    elif n.startswith("島が見え") or n == "渡りの途中": PERC.bar(b, "R:0.5 E3:0.25 R:0.25 D3:0.5 E3:0.25 R:0.25 R:0.5 E3:0.25 E3:0.25 D3:0.5 G3:0.5")
    elif n == "島が見えた" or n == "島に着く": PERC.bar(b, "D3:0.25 E3:0.25 R:0.25 E3:0.25 D3:0.5 E3:0.25 R:0.25 R:0.5 E3:0.25 E3:0.25 D3:0.5 G3:0.5")
# 羽ばたき（ホワイトノイズのシュッを短く、ばさっ、ばさっ）
# 2026-10-26 人間「後半に行くにつれて曲の始まり方似てない？」→ 物の音を重ねるだけにしない: 羽ばたきのリズムが、そのまま曲のリズムになっていく。
#   羽ばたきは 3・3・2 の割り（16分で 0・3・6 の所＝ジャージークラブのキックと同じ形）。1小節目は羽だけ、2小節目はカホンが同じ所を打ち、
#   出発の前半4小節はキックが羽ばたきの形を受けついで（羽の音は小さくなって消える）、5小節目で 4つ打ちのハウスへ羽ばたいていく
FLAP = "A4:0.5 R:0.25 A4:0.5 R:0.25 A4:0.5 A4:0.5 R:0.25 A4:0.5 R:0.25 A4:0.5"
FX.bar(0, FLAP); FX.bar(1, FLAP); FX.bar(S.sc("出発")[0], FLAP.replace("A4:0.5", "A4:0.5,"))
PERC.bar(1, "A2:0.75 D3:0.75, D3:0.5, A2:0.75 D3:0.75, A2:0.25 A2:0.25")
riser(FX, S.sc("島が見える？")[0], 4, "C4"); riser(FX, S.sc("島が見えた")[0], 8, "D4")
cym_swell(CYM, S.sc("島が見える？2")[0], 2, "C4"); cym_swell(CYM, S.sc("島が見えた")[0], 2, "C4"); cym_swell(CYM, S.sc("雲を抜ける")[0], 4, "E4")
for b in S.sc("波"): WAVE.bar(b, "A4:4")
for b in S.sc("島に着く")[4:]: WAVE.bar(b, "A4:4")

# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ この曲の物語でしか出ない音:
#   ・駅前の発車のチャイム（作った短い旋律。しずくのガラスのプラックで）を、羽ばたきの上に（旅立ちの駅）
#   ・夜の電車の「ガタン、ゴトン」（カホンのトーンと低音を弱く）を、2番の前半（夜の電車の窓から海が見える）に
#   ・雲の中の胸の音「ドクン」（キックを弱く）が、迷っている間に少しずつ速くなる（下のドラム）
#   ・島に着いたら、波の音に小鳥の声（群れが降り立つ）
DROP.bar(0, K.mel("R:1 3':0.5 5':0.5 1'':1 6':1", oct=4)); DROP.bar(1, K.mel("5':1.5 3':0.5 2':2", oct=4))
for i, b in enumerate(S.sc("夜の海")):
    if i < 8: PERC.bar(b, "D3:0.25, D3:0.25 R:1.5 A2:0.25, A2:0.25 R:1.5" if i % 4 != 3 else "D3:0.25, D3:0.25 R:0.75 D3:0.25, A2:0.25, A2:0.25 R:0.75 A2:0.25, D3:0.5,")
season(S, S.sc("波")[0], "小鳥", S.beats * 8, vol=0.06, pan=-0.3, every=16)   # 右にプラック・カホンが多いので左に
# 合いの手: Bメロで歌が3拍のばす小節に、プラックが風のように上る（1回目）・下りる（2回目）。弱く
for name, pat in (("風に乗る", "R:1.5 3':0.25, 5':0.25, 6':0.5, 1'':0.5, R:1"), ("風に乗る2", "R:1.5 1'':0.25, 6':0.25, 5':0.5, 3':0.5, R:1")):
    for i, b in enumerate(S.sc(name)):
        if i in (1, 3): PLM.bar(b, K.mel(pat, oct=4))
# 最後のサビ: 歌が伸ばす・休む所に、しずく（ガラスのプラック）の高い答え（新しい音）。2拍の答えと、1拍の「きらっ」
for i, b in enumerate(S.sc("島が見えた")):
    if i in (3, 7, 11): DROP.bar(b, KF.mel(["R:2 3':0.5 5':0.5 1'':1", "R:2 2':0.5 3':0.5 5':1", "R:2 6':0.5 5':0.5 3':1"][i // 4], oct=4))
    elif i in (1, 5, 13): DROP.bar(b, KF.mel("R:3 5':0.5 1'':0.5", oct=4))
# 出発: ドラムが入る小節（5小節目）の前にライザー、頭に「ドン」。+2 の最後のサビの頭（1拍のブレイクのあと）にも「ドン」。音量 0.08
IMP = S.track("インパクト（ドン）", "impactHit", volume=0.08, pan=0.0, reverb=0.4)
riser(FX, S.sc("出発")[4], 4, "C4")
IMP.bar(S.sc("出発")[4], "D2:4"); IMP.bar(S.sc("島が見えた")[0], "D2:4")
# 2026-10-26 人間「ミックスのバランスをよくするのが大事」: カホンは書き出しで 7半音下がるので、もとの D3（トーン）が G2 になって鳴っていなかった
#   （カホンは鍵盤で打ち方を選ぶ楽器）。全部を +7 半音で書き直して、書き出しのあとに書いたとおりの打ち方（A2〜C#3 低音・D3 トーン・E3〜G3 スラップ）になるようにする
PERC.ev = [(st, L, nm(midi(x.split(":")[0]) + 7) + ":" + x.split(":", 1)[1]) for st, L, x in PERC.ev]

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "出発":
        vgroove(D, b, "four" if i >= 4 else "none", seed=b)
        # 2026-10-26: 前半4小節のキックは、羽ばたきの 3・3・2 の形（弱く始めて、句の頭だけ強く）。3・4小節目は手拍子のようなスネアとハイハットが加わる
        if i < 4: D.set(b, ("X" if i % 2 == 0 else "x") + "..x..x.x..x..x.", "." * 16 if i < 2 else "....o.......x...", "." * 16 if i < 2 else "..x...x...x...x.")
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n in ("群れのおしゃべり", "夜の海"):
        vgroove(D, b, "four" if i < 8 else "four16", ghosts=0.3, seed=b)
        if n == "夜の海" and i < 8: D.set(b, "X.......X.......", "....x.......x...", "x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomdown")
    elif n.startswith("風に乗る"):
        vgroove(D, b, "half" if i < 4 else "four", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n == "島が見える？" or n == "島が見えた":
        vgroove(D, b, "four16", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last: put_fill(D, b, "tomdown" if n == "島が見える？" else "tomtrip")
    elif n == "島が見える？2":
        vgroove(D, b, "jersey", ghosts=0.3, seed=b)                    # サビごとにリズムを入れかえる（ジャージークラブ）
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n == "渡りの途中":
        vgroove(D, b, "four16", ghosts=0.4, seed=b)
        if i == 0: crash(D, b, "B2")
        if i == 3: put_fill(D, b, "small")
        if last: put_fill(D, b, "build")
    elif n == "雲の中":
        # 2026-10-26: 迷っている胸の音「ドクン」が、ベースが入る所（9小節目）から弱く鳴り、少しずつ速くなって、4つ打ちへつながる
        if 8 <= i < 12: D.set(b, "x..o............" if i < 10 else "x..o....x..o....", "." * 16, "." * 16)
        elif i >= 12: D.set(b, "X...X...X...X..." if i >= 14 else "X..x....X..x....", "." * 16, "." * 16)
    elif n == "雲を抜ける":
        D.set(b, "X...X...X...X...", "....X.......X..." if i >= 2 else "." * 16, "x.x.x.x.x.x.x.x." if i >= 4 else "." * 16)
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X...X...", "x.x.x.x.xxxxXXXX", "." * 16)
    elif n == "島に着く":
        vgroove(D, b, "four" if i < 6 else "none", seed=b)
        if i == 0: crash(D, b)
        if i == 6: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 8)

# 2026-10-26 人間「ドラム強弱、アクセント、余韻も上手く使ってね」:
#   ・Aメロ1番の前半（4つ打ち）と Bメロの前半（Half feel）は軽く: 強打（X）を4小節の句の頭の1打だけ残して x に
#   ・サビは、2小節ごとの頭のキックと、次の小節へ押し出すスネアの最後の一打を強く
#   ・余韻: クラッシュは次のシンバルまで、最大 8拍のばす
def lighten(b, head):
    for arr in (D.K, D.S):
        arr[b] = "".join(("x" if c == "X" and not (head and j == 0) else c) for j, c in enumerate(arr[b]))
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if (n == "群れのおしゃべり" and i < 8) or (n.startswith("風に乗る") and i < 4): lighten(b, i % 4 == 0)
    elif n.startswith("島が見え"):
        kk = list(D.K[b]); ss = list(D.S[b])
        if kk[0] in "xX" and i % 2 == 0: kk[0] = "X"
        ls = max([j for j, c in enumerate(ss) if c in "xX"], default=None)
        if ls is not None and i % 2 == 1: ss[ls] = "X"
        D.K[b] = "".join(kk); D.S[b] = "".join(ss)
D.C.ev = [(st, max(L, 8.0), x) for st, L, x in D.C.ev]

# 1拍の完全な無音（雲に入る所）・Bメロの最後の止め・+2 の直前の1拍のブレイク
SIL.add(S.sc("雲の中")[0] - 1, 3, 4)
for name in ("風に乗る", "風に乗る2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("雲を抜ける")[-1], 3, 4)
SIL.apply()

S.fade_out = 12
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の23。K-POP（ハウス×ジャージークラブ）。A 長調・150（最後のサビは +2 の B）。生まれた町を出て、大きな町へ旅立つ。"
          "羽ばたきの音から、プラックのフック、8分で語る Aメロ、高くのびる Bメロ、「どき・どき」のサビ（2回目はジャージークラブ）、プラックのソロ、"
          "1拍の無音から雲の中（ドラムなし）、雲を抜けて +2 の最後のサビ、島に着いて波の音とフェードアウト。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
# 2026-10-26: そよ風は曲の頭から外して（羽ばたきとチャイムだけで始める）、雲の中「かぜがね おしえる」の所へ移した
season(S, S.sc("雲の中")[4], "そよ風", S.beats * 8, vol=0.07)
season(S, S.nb - 10, "波", S.beats * 10, vol=0.09, every=14)
S.no_depth = True
teto(S, LY, V, transpose=-7, special={"島が見えた": 0.55, "雲の中": -0.55, "雲を抜ける": 0.1, "島に着く": 0.1})
