# vb25 16「雨音ステップアップ」Raindrop Step-Up（仮）— ヒップホップ（ローファイ×ドラムンベース）。B長調・88 → 倍テン 176（走り出すから）・4/4。
#   最後のサビは +1（C長調）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（落ちこんだ雨の日、少しずつ足が軽くなる）、歌を人が歌える旋律に、テトの歌の版を足した。
#   倍テンになっても歌は同じ速さ（音の長さを2倍で書く）。速くなるのはドラムとベース＝「足取り」。
#   テトの声に合うよう、曲全体を E♭長調から 4半音下げて B長調にした（書くのは E♭長調の度数のまま、書き出しの前に下げる）。
# 物語: 何もうまくいかなかった雨の日の帰り道。水たまりに映る顔はしかめっつら。傘をくるくる回すと雨粒が飛びちって、ちょっとおかしくなる。
#   雨音がリズムを刻み、足取りがだんだん速くなる。晴れ間がのぞいて傘を閉じて走り出す。にわか雨に軒下で雨宿りしても、もう待てない。晴れた空の下へ。
# 場面と強さ: 雨音とエレピ（小）→ 傘をさして（Aメロ・ゆるい）→ 水たまり（Bメロ）→ くるくる（ローファイのサビ）→ 傘の上の雨粒（ナイロンギター）
#   → 2回目の帰り道（BGM はエレピが歌を受け取る）→ 足取り（1拍の無音）→ 走り出す（倍テンのサビ）→ 晴れ間 → 晴れ間の帰り道（倍テンの Aメロ）
#   → 軒下の雨宿り（Half feel）→ もう待てない（止め）→ 晴れた空のサビ（+1・最大）→ 鳥の声
# 旋律の性格: Aメロは句の頭を休む8分と16分の2つ組。サビは同じ音を3つ置いて下がる「くるくる」。最高音 F#5（最後のサビは F5）。
# ほかの曲とちがう所: テンポが途中で倍になる（歌は同じ速さのまま）。ローファイのエレピ・ナイロンギター・雨粒・鳥の声。
from vb25_lib import *

S = Song("16", "amaoto", "雨音ステップアップ（仮）", "Raindrop Step-Up", 88, 4, "Eb", "major", "ヒップホップ（ローファイ×ドラムンベース・ボカロ）")
S.kit = "naked"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.keep_old_synth = True
S.no_depth = True
K = S.key                    # E♭長調
KE = Key("E", "major")       # 最後のサビ（+1）

A_CH = ["Abmaj7", "Gm7", "Fm7", "Bb7sus4"]
B_CH = ["Cm7", "Cm7/Bb", "Abmaj7", "Bb7"]
C_CH = ["Abmaj7", "G7", "Cm7", "Bbm7", "Eb7", "Abmaj7", "Fm7", "Bb7"]
dbl = lambda xs: [x for c in xs for x in (c, c)]
SUN = ["Ebmaj7", "Ebmaj7", "Bbm7", "Eb7", "Abmaj7", "Abmaj7", "Bb7sus4", "Bb7"]
EAVES = ["Abmaj7", "Abmaj7", "Gm7", "Gm7", "Fm7", "Fm7", "Ebmaj7/G", "Ebmaj7/G",
         "Abmaj7", "Abmaj7", "Bbm7", "Eb7", "Abm6", "Abm6", "Bb7sus4", "Bb7"]
C_E = [tr_chord(c, 1) for c in C_CH]
LAST = dbl(C_E) + dbl(C_E[:7]) + ["B7sus4", "B7"]

S.scene("雨音とエレピ", 4, "intro", A_CH)
S.scene("傘をさして", 8, "verse", A_CH)
S.scene("水たまり", 4, "pre", B_CH)
S.scene("くるくる", 8, "chorus", C_CH)
S.scene("傘の上の雨粒", 4, "interlude", A_CH)
S.scene("2回目の帰り道", 8, "verse", A_CH)
S.scene("足取り", 4, "pre", ["Abmaj7", "Bb", "Bdim7", "Cm7"])
S.scene("走り出す", 16, "chorus", dbl(C_CH))           # ここから倍テン 176
S.scene("晴れ間", 8, "interlude", SUN)
S.scene("早口の帰り道", 16, "verse", dbl(A_CH) * 2)
S.scene("軒下の雨宿り", 16, "bridge", EAVES)
S.scene("もう待てない", 8, "pre", ["Cm7", "Cm7", "Bdim7", "Bdim7", "Abmaj7", "Abmaj7", "Bb7sus4", "B7"])
S.scene("晴れた空", 32, "chorus", LAST)
S.scene("鳥の声", 8, "outro", ["Emaj7", "Emaj7", "Amaj7", "Amaj7", "Emaj7", "Emaj7", "Amaj7", "Emaj9"])
b_run = S.sc("走り出す")[0]
S.tempo = [{"bar": b_run + 1, "bpm": 176}]

V = Voice(S, vol=0.22, delay=0.75, patch="calliope", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
EPS = dict(volume=0.11, pan=-0.3, reverb=0.3, sustain=1.0, fx=[{"type": "eq", "low": -3, "mid": -1.5, "midHz": 400, "high": -0.5},
                                                                   {"type": "tape", "mix": 0.1}])
EP = [S.track(f"エレピの和音{i + 1}", "pad", patch="surgeKeysFmPiano1", **EPS) for i in range(3)]
EPM = S.track("エレピ（歌の受け渡し）", "pad", patch="surgeKeysFmPiano1", **EPS)
NY = S.track("ナイロンギター", "guitar", patch="nylonGuitar", amp="clean", chorus=0, volume=0.13, pan=0.35, reverb=0.25, sustain=1.3,
             humanPitch=0, fx=[{"type": "filter", "kind": "highpass", "freq": 120, "q": 0.7}])
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.2))
DROP = S.track("雨粒（ガラスのような音）", "pad", patch="surgeChordBellSquare2", volume=0.05, pan=0.5, sustain=0.6, reverb=0.45,
               fx=[{"type": "filter", "kind": "highpass", "freq": 600, "q": 0.7}])
BIRD = S.track("鳥の声（ピッコロのさえずり）", "panflute", patch="piccolo", volume=0.06, pan=-0.4, reverb=0.35)
PAD = [S.track(f"晴れ間のパッド{i + 1}", "pad", **pad_spec("surgePadHineVertigo", vol=0.055, pan=0.45, duck=0.3)) for i in range(2)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 最後のサビにだけ足す新しい音: 高いストリングスの対旋律（晴れた空が広がる）。
#   背景なので小さく奥に（パッドの 0.055 と同じくらい）、ナイロンギター（右 0.35）・エレピ（左 0.3）とぶつからない高い音域と少し右に
STRC = S.track("ストリングス（晴れた空の対旋律）", "strings", patch="stringEnsemble", volume=0.06, pan=0.15, reverb=0.4, sustain=1.6)
TR = -4                                   # 書き出しの前に全体を下げる半音（teto の transpose と同じ）
BLO, BHI = 28 - TR, 52 - TR               # 歌うベースの音域（下げたあとで E1〜E3）

# ================= 歌の旋律と歌詞（E♭長調の度数。oct=4 で 1 = E♭4。書き出しの前に全体を 4半音下げる） =================
def stretch(lines):
    """1小節の行を、音の長さを2倍にして2小節に分ける（倍テンでも歌の速さは同じ）"""
    out = []
    for line in lines:
        a, b, t = [], [], 0.0
        for x in line.split():
            nm_, d = x.split(":", 1)
            dd = float(d.rstrip("!,'_~^/\\\\")) * 2
            (a if t < 4 - 1e-6 else b).append(f"{nm_}:{dd:g}"); t += dd
        out += [" ".join(a), " ".join(b)]
    return out
VA = ["R:0.5 3:0.25 4:0.25 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "2:0.5 1:0.5 2:1 R:2",
      "R:0.5 2:0.25 3:0.25 4:0.5 4:0.5 6:0.5 4:0.5 2:1", "5:0.5 4:0.5 5:1 R:2",
      "R:0.5 1':0.25 7:0.25 6:0.5 6:0.5 5:0.5 3:0.5 5:1", "3:0.5 2:0.5 3:1 R:2",
      "R:0.5 4:0.25 4:0.25 6:0.5 1':0.5 7:0.5 6:0.5 5:1", "4:1 5:1 R:2"]
V1 = "あめのひのかえりみち/なにもかもさかさまで/みずたまりにうつったの/くもりがおのぼくだ"
V2 = "かさをくるくるまわす/あまつぶがとびちってく/ちょっとだけおかしくなる/はれあしがうまれる"
V3 = "はれまがのぞくそらだ/かさをとじてかけだす/ぬれたくつでもいいよ/ひかりのほうへいく"
VB = ["R:0.5 6:0.5 6:0.5 7:0.5 1':1 3':1", "2':1 1':1.5 R:1.5", "R:0.5 3':0.5 1':0.5 6:0.5 4:1 1':1", "2':2 7:2"]
VB2 = ["R:0.5 1':0.5 1':0.5 7:0.5 6:1 1':1", "2':1 1':1 2':1 4':0.5 R:0.5", "#5:0.5 7:0.5 2':0.5 4':0.5 2':1 7:1", "1':2 R:2"]
VC = ["R:0.5 5':0.5 5':0.5 5':0.5 4':0.5 3':0.5 1':1", "7:0.5 2':0.5 #5:0.5 2':0.5 7:1.5 R:0.5",
      "R:0.5 3':0.5 3':0.5 3':0.5 5':1 3':1", "4':0.5 2':0.5 b7:0.5 2':0.5 4':1.5 R:0.5",
      "3':0.5 5':0.5 b7:0.5 1':0.5 3':1.5 R:0.5", "R:0.5 4':0.5 4':0.5 4':0.5 3':1 1':0.5 R:0.5",
      "6:0.5 1':0.5 2':0.5 4':0.5 5':1 4':1", "5':1 4':0.5 2':0.5 7:2"]
C1 = "くるくるまわるよかさが/あめつぶをはじいてる/すこしずつ/ふわりうく/くもりがおがほどける"
C2 = "はしりだすよあめのなか/くものすきまにひかり/あしたへと/かけてゆく/みずたまりとびこえて"
VR = stretch(VC)
VRL = [x.replace("5':", "4':") for x in VR] + [x.replace("5':", "4':") for x in VR[:12]] + ["R:1 1':1 2':1 3':1", "4':4", "3':2 2':2", "1':4"]
CL = C2 + "/" + "/".join(C1.split("/")[:4]) + "/そらがはれたよ"
VEAVES = ["5:2 6:1 1':1", "3':3 R:1", "2':2 1':1 7:1", "5:3 R:1", "4:2 6:1 2':1", "1':3 R:1", "7:2 1':1 3':1", "2':3 R:1",
          "4':3 3':1", "1':3 R:1", "b7:2 2':1 4':1", "5':3 R:1", "b6:2 4:1 1':1", "1':3 R:1", "4':2 2':1 1':1", "2':3 R:1"]
VK = ["R:0.5 6:0.5 1':0.5 3':0.5 5':1 3':1", "4':1 3':1 1':1.5 R:0.5", "R:0.5 #5:0.5 7:0.5 2':0.5 4':1 2':1", "#5:2 7:1 R:1",
      "R:0.5 1':0.5 3':0.5 5':0.5 5':2", "4':1 3':1 1':1.5 R:0.5", "R:0.5 4':0.5 4':0.5 4':0.5 5':2", "R:4"]
VOUT = ["3':2 2':1 1':1", "5:3 R:1", "6:2 5:1 3:1", "4:3 R:1", "3:1 5:1 1':2", "R:4", "R:4", "R:4"]
LY = Lyrics(S)
def put(name, key, lines, text, low=True):
    bars = S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("傘をさして", K, VA, V1)
if VOCAL: put("2回目の帰り道", K, VA, V2)
else:
    for i, b in enumerate(S.sc("2回目の帰り道")):
        if i < 4: EPM.bar(b, K.mel(VA[i], oct=4))                  # BGM: 前半はエレピが歌を受け取る
        else: V.bar(b, K.mel(VA[i], oct=4))
put("水たまり", K, VB, "あまおとがほら/りずむをきざむ")
put("足取り", K, VB2, "ひとつふたつあるく/はれあしでいく")
put("くるくる", K, VC, C1)
put("走り出す", K, VR, C2)
put("早口の帰り道", K, stretch(VA), V3)
put("軒下の雨宿り", K, VEAVES, "のきした/まただね/とけいの/はりおす/でもね/そらには/にじがね/みえたよ", low=False)
put("もう待てない", K, VK, "もうまてないんだ/あめあがりへと/あしがうずくの/いまだよ")
put("晴れた空", KE, VRL, CL)
put("鳥の声", KE, VOUT, "とりがね/うたうよ/はれた", low=False)


# ================= ナイロンギター（間奏の主旋律・晴れ間のソロ・伴奏の分散和音） =================
NYS = ["5:0.5 4:0.25 3:0.25 1:0.5 3:0.5 4:1 6:1", "5:0.5 3:0.25 2:0.25 7,:0.5 2:0.5 3:2",
       "1:0.25 2:0.25 4:0.25 6:0.25 1':0.5 6:0.5 4:0.5 2:0.5 1:1", "2:1.5 4:0.5 1:2"]
for i, b in enumerate(S.sc("傘の上の雨粒")): NY.bar(b, K.mel(NYS[i], oct=4))
SUNS = ["3:0.5 5:0.5 1':0.5 3':0.5 2':1 1':1", "5:0.25 6:0.25 5:0.25 3:0.25 1:0.5 3:0.5 5:2",
        "4:0.5 b6:0.5 1':0.5 4':0.5 2':1 b7:1", "5:0.5 b7:0.5 2':0.5 5':0.5 3':2",
        "1':0.25 3':0.25 1':0.25 6:0.25 4:0.5 6:0.5 1':1 3':1", "4':0.5 3':0.5 1':0.5 6:0.5 1':2",
        "2':0.5 1':0.5 5:0.5 4:0.5 2:1 4:1", "5:1 7:1 2':1 4':1"]
for i, b in enumerate(S.sc("晴れ間")): NY.bar(b, K.mel(SUNS[i], oct=4))
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("傘をさして", "くるくる", "早口の帰り道") or (n == "2回目の帰り道" and i >= 4) or (n == "晴れた空" and i >= 16):
        t = tones(S.chords[b], "E3", "E5")
        pat = (0, 2, 1, 3, 2, 4, 3, 1) if n not in ("早口の帰り道", "晴れた空") else (0, 1, 2, 3, 0, 1, 2, 3)
        NY.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in pat))

# ================= エレピ（ローファイの和音・倍テンでは刻み） =================
COMP = ["X:1.5 X:0.5 R:0.5 X:1.5", "R:0.5 X:1 X:1 R:0.5 X:1", "X:0.75 X:0.75 R:0.5 X:2", "R:0.25 X:1.75 X:2"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 63, 3)
    pat = None
    # 2026-10-26 人間「後半に行くにつれて曲の始まり方似てない？」→ 前奏は、雨粒がだんだんエレピの和音に変わっていく:
    #   1小節目＝雨粒だけ／2小節目＝雨粒の落ちる所でエレピが和音の音を1つずつ（下の「雨粒が和音に」）／3小節目＝後ろ半分で和音／4小節目＝和音をのばす
    if n == "雨音とエレピ": pat = None if i < 2 else ("R:2 X:2" if i == 2 else "X:4")
    elif n in ("軒下の雨宿り", "鳥の声"): pat = "X:4"
    elif n in ("傘をさして", "傘の上の雨粒") or (n == "2回目の帰り道" and i >= 4): pat = COMP[i % 4]
    elif n == "2回目の帰り道": pat = "X:2 X:2"
    elif n in ("水たまり", "足取り"): pat = "X:1 X:1 X:1 X:1" if not (n == "足取り" and i == 3) else "X:2 R:2"
    elif n == "くるくる": pat = "X:1.5 X:1 X:1.5"
    elif n in ("走り出す", "晴れた空", "早口の帰り道"): pat = "R:0.5 X:1 X:0.5 R:0.5 X:1.5" if i % 2 == 0 else "X:1.5 X:2.5"
    elif n == "晴れ間": pat = "X:2 X:2"
    elif n == "もう待てない": pat = "X:0.5 " * 8 if i < 7 else "X:2 R:2"
    if pat:
        for j in range(3): EP[j].bar(b, pat.strip().replace("X", nm(v[j])))

# 晴れ間のパッド
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("晴れ間", "晴れた空", "鳥の声", "軒下の雨宿り"):
        v = voice(S.chords[b], 57, 2)
        for j in range(2): PAD[j].bar(b, f"{nm(v[j])}:4")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); r5 = r + 7
    if n == "雨音とエレピ": continue
    if n in ("傘をさして", "2回目の帰り道", "傘の上の雨粒"):
        BASS.bar(b, f"{nm(r)}:1.5! {nm(r)}:0.5 R:0.5 {nm(r5)}:0.5 {nm(r + 12)}:0.5 {nm(r5)}:0.5" if i % 2 == 0 else f"{nm(r)}:2.5! {nm(r5)}:0.5 {nm(r)}:1")
    # 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 歌うベース（音域は下げたあと E1〜E3。音量はそのまま）:
    #   水たまり＝雨音といっしょに上っていく（最後の小節は駆ける）／くるくる＝歌が伸ばす偶数小節で歩く／晴れ間＝ギターのソロにゆったり寄りそう／
    #   倍テン＝4小節目は駆けて次の句へ／もう待てない＝後半で上っていく
    elif n == "水たまり":
        BASS.bar(b, sing_bass(S, b, "climb" if i < 3 else "run", BLO, BHI))
    elif n == "足取り":
        BASS.bar(b, bass_line(S, b, "root8") if i != 3 else f"{nm(r)}:2! R:2")
    elif n == "くるくる":
        BASS.bar(b, bass_line(S, b, "push") if i % 2 == 0 else sing_bass(S, b, "walk", BLO, BHI))
    elif n in ("走り出す", "晴れた空", "早口の帰り道"):
        # ドラムンベース: 1小節目は伸ばし、2小節目は8分で走る
        if i % 2 == 0: BASS.bar(b, f"{nm(r)}:2.5! {nm(r5)}:0.5 {nm(r + 12)}:1")
        elif i % 4 == 3 and i != L - 1: BASS.bar(b, sing_bass(S, b, "run", BLO, BHI))
        else: BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "晴れ間": BASS.bar(b, sing_bass(S, b, "ride" if i % 2 == 0 else "walk", BLO, BHI))
    elif n == "軒下の雨宿り": BASS.bar(b, f"{nm(r)}:4" if i % 2 == 0 or ch != S.chords[b - 1] else "R:4")
    elif n == "もう待てない":
        if i < 4: BASS.bar(b, bass_line(S, b, "root8"))
        elif i < 7: BASS.bar(b, sing_bass(S, b, "climb", BLO, BHI))
        else: BASS.bar(b, f"{nm(r)}:2! R:2")
    elif n == "鳥の声": BASS.bar(b, f"{nm(r)}:4" if i < 7 else f"{nm(r)}:4")

# ================= 雨粒・鳥 =================
rnd = random.Random(16)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "雨音とエレピ":
        # 雨粒が和音に: 1小節目は雨粒6つ、2小節目からは雨粒が減り、そのかわりエレピが同じように落ちる音で和音の音を鳴らす
        ts = tones(S.chords[b], "C5", "C7")
        for j in range((6, 4, 2, 2)[i]):
            DROP.at(S.bar_beat(b) + rnd.choice([x * 0.25 for x in range(16)]), f"{nm(rnd.choice(ts))}:0.25")
        if i == 1: EPM.bar(b, " ".join(f"R:0.5 {nm(m)}:0.5" for m in tones(S.chords[b], "Eb4", "Eb5")[:4]))
        if i == 2: EPM.bar(b, " ".join(f"{nm(m)}:0.5" for m in tones(S.chords[b], "Eb4", "Eb5")[:4]) + " R:2")
        continue
    dens = {"雨音とエレピ": 6, "傘の上の雨粒": 6, "軒下の雨宿り": 4, "傘をさして": 3, "2回目の帰り道": 3, "水たまり": 2, "くるくる": 2, "足取り": 2}.get(n, 0)
    ts = tones(S.chords[b], "C5", "C7")
    for j in range(dens):
        DROP.at(S.bar_beat(b) + rnd.choice([x * 0.25 for x in range(16)]), f"{nm(rnd.choice(ts))}:0.25")
for i, b in enumerate(S.sc("晴れ間") + S.sc("鳥の声")):
    if i % 2 == 0: BIRD.bar(b, f"R:{(i % 3) + 0.5:g} E6:0.125 G6:0.125 E6:0.125 G6:0.25 R:0.375 A6:0.125 C7:0.375")
for i, b in enumerate(S.sc("晴れた空")):
    if i % 8 == 4: BIRD.bar(b, "R:1 G6:0.125 A6:0.125 G6:0.25 R:2.5")

# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ この曲の物語でしか出てこない音と展開:
#   ・傘を開く「バサッ」（Aメロの直前の半拍）。閉じる「シュッ」（倍テンの直前）と対になる
#   ・水たまりを跳びこえる「ぴちゃん」（倍テンのサビの頭と、最後のサビの頭。雨粒の高い音を短く散らす）
#   ・にわか雨: 軒下の雨宿りで、いったんやんだ雨（季節の音）がもう一度降る。もう待てないで、またやむ
#   ・終わり: 鳥の声のあと、軒先から最後のひとしずく
FX.bar(S.sc("傘をさして")[0] - 1, "R:3.5 A4:0.5")
for b in (S.sc("走り出す")[0], S.sc("晴れた空")[0]): DROP.bar(b, "C7:0.125 G6:0.125 E7:0.125 C7:0.25 R:3.375")
DROP.bar(S.sc("鳥の声")[-1], "R:3 G6:1")
season(S, S.sc("軒下の雨宿り")[0], "雨", S.beats * 16, vol=0.032, every=11)   # 2026-10-26 雨の音を ×0.4（雑音で点数が下がっていた。試すと 7.15→7.34）
# 合いの手: Aメロの句の終わり（歌が2拍休む所）にエレピの短い返事。倍テンの Aメロは、歌が1小節まるごと休む所に（書き出しで 4半音下がる）
LICK = {"Gm7": "R:2 D5:0.25 F5:0.25 G5:0.5 Bb5:0.5 G5:0.5"}
LICK2 = {"Gm7": "D5:0.5 F5:0.5 G5:0.5 Bb5:0.5 D6:1 Bb5:1", "Bb7sus4": "F5:0.5 Ab5:0.5 Bb5:0.5 Eb6:0.5 F6:1 Eb6:1"}
for name, idx in (("傘をさして", (1, 5)), ("2回目の帰り道", (5,))):
    for i in idx:
        b = S.sc(name)[i]
        if S.chords[b] in LICK: EPM.bar(b, LICK[S.chords[b]])
for i, b in enumerate(S.sc("早口の帰り道")):
    if i % 4 == 3 and S.chords[b] in LICK2: EPM.bar(b, LICK2[S.chords[b]])
# 最後のサビの対旋律（E長調の音名で書く。2小節で1つの和音）
STRM = ["G#5:3 B5:1", "D6:4", "C#6:3 E6:1", "G#5:4", "A5:3 C#6:1", "E6:2 C#6:2", "D#6:4", "A5:2 B5:2",
        "E6:4", "C#6:4", "C6:3 D#6:1", "F#6:2 D#6:2", "E6:3 C#6:1", "B5:4", "D6:4", "C#6:2 A5:2",
        "B5:3 D6:1", "G#5:4", "A5:2 C#6:2", "E6:4", "C#6:3 A5:1", "E6:2 F#6:2", "E6:4", "D#6:4"]
for i, b in enumerate(S.sc("晴れた空")[8:]): STRC.bar(b, STRM[i])

# 効果音
FX.bar(S.sc("走り出す")[0] - 1, "R:2 A4:1 R:1")                 # 傘を閉じる「シュッ」（無音の直前）
riser(FX, S.sc("晴れた空")[0], 8, "D4")
cym_swell(CYM, S.sc("くるくる")[0], 2, "C4"); cym_swell(CYM, S.sc("晴れ間")[0], 2, "C4")
CYM.bar(S.sc("鳥の声")[-1], "B4:4")                          # 最後はロールのディミヌエンド

# ================= ドラム（素直な生ドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "雨音とエレピ":
        if i == 3: D.set(b, "X.........X.....", "............X...", "x.x.x.x.x.x.x.x.")
    elif n in ("傘をさして", "2回目の帰り道"):
        vgroove(D, b, "boombap", ghosts=0.45, seed=b, k="X.....x...X....." if i % 2 == 0 else "X......xX.....x.", h="x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b, "G2")
        if last: put_fill(D, b, "small")
    elif n in ("水たまり", "足取り"):
        vgroove(D, b, "boombap", ghosts=0.3, seed=b, h="xxxxxxxxxxxxxxxx" if n == "足取り" else "x.x.x.x.x.x.x.x.")
        if n == "足取り" and i == 2: put_fill(D, b, "snare16")
        if n == "足取り" and last: halt(D, b, 2)
        if n == "水たまり" and last: put_fill(D, b, "tomtrip")
    elif n == "くるくる":
        vgroove(D, b, "boombap", ghosts=0.4, seed=b, h="x.xxx.xxx.xxx.xx")
        if i == 0: crash(D, b)
        if i == 4: D.cym(b, "D2:1 D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "small")
    elif n == "傘の上の雨粒":
        vgroove(D, b, "boombap", ghosts=0.5, seed=b, h="x...x...x...x...")
        D.cym(b, "D2:1 D2:1 D2:1 D2:1"); D.H[b] = "." * 16
    elif n in ("走り出す", "晴れた空", "早口の帰り道"):
        # ドラムンベース（倍テン）。2小節で1つの形
        if i % 2 == 0: vgroove(D, b, "dnb", ghosts=0.4, seed=b)
        else: vgroove(D, b, "dnb", ghosts=0.4, seed=b, k="..X.......X.....", s="....X..o.o..X..o")
        if n == "早口の帰り道" and i % 4 < 2:
            D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16                                  # ライドで走る
        if i % 8 == 0 and not (n == "早口の帰り道" and i % 4 < 2): crash(D, b, "C2" if i % 16 == 0 else "G2", 8 if (i == 0 and n != "早口の帰り道") else 4)   # 2026-10-26 無音・止めのあとのサビ頭はシンバルを長く残す
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "snare16")
        if last and n == "走り出す": put_fill(D, b, "small")
        if last and n == "早口の帰り道": put_fill(D, b, "tomdown")
        if last and n == "晴れた空": put_fill(D, b, "snare16")
    elif n == "晴れ間":
        vgroove(D, b, "twostep", ghosts=0.3, seed=b)
        if i == 0: crash(D, b, "B2")
        if last: put_fill(D, b, "build")
    elif n == "軒下の雨宿り":
        # Half feel（176 の上で 88 のノリ）
        if i < 4: D.set(b, "X...............", "." * 16, "x...x...x...x...")
        else: vgroove(D, b, "half", ghosts=0.3, seed=b, h="x.x.x.x.x.x.x.x.")
        if i == 8: D.cym(b, "D2:1 D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "lift")
    elif n == "もう待てない":
        vgroove(D, b, "vrock2", ghosts=0.3, seed=b)
        if i == 0: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n == "鳥の声":
        if i < 4: vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
        if i == 0: crash(D, b, "C2")

# 1拍の完全な無音（倍テンの直前）・止め（もう待てないの最後の2拍）
SIL.add(S.sc("足取り")[-1], 3, 4)
SIL.add(S.sc("もう待てない")[-1], 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の16。ヒップホップ（ローファイ×ドラムンベース）。B長調・88 → 倍テン 176、最後のサビは +1（C）。"
          "落ちこんだ雨の日の帰り道、少しずつ足取りが軽くなる。雨音とエレピで始まり、ゆるい Aメロ、「くるくる」のローファイのサビ、ナイロンギター、1拍の無音から倍テンのサビ"
          "（歌は同じ速さで、ドラムとベースが倍に）、軒下の雨宿りの Half feel、止め、+1 の晴れた空のサビ、鳥の声。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, 0, "雨", S.beats * 10, vol=0.032, every=11)   # 2026-10-26 雨を ×0.4・前奏の10小節だけに（BGM の点数: 40小節 7.34 → 24小節 7.44。雨が少ないほど上がる。軒下の雨宿りでもう一度降る）
season(S, S.nb - 6, "小鳥", S.beats * 6, vol=0.07)
teto(S, LY, V, transpose=-4, level={"verse": -0.3}, special={"晴れた空": 0.55, "軒下の雨宿り": -0.5, "もう待てない": 0.1, "鳥の声": -0.45, "早口の帰り道": -0.1})
