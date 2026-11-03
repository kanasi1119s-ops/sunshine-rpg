# vt25 05「ペンギン・ブレイクビーツ」Penguin Breakbeats（仮）— ヒップホップ（ブレイクビーツ）。98・4/4。G の短調（サビは E♭→F の明るい所）。転調なし。
#   （表では エレピ・スクラッチ・ブラスだったが、第1弾の 14「猫背のパレード」（ブームバップ 96・エレピ・ブラス・スクラッチ）と似るので、
#     チューバのよちよちベース・マリンバ・ピッコロに変えた）
# 物語: 体育のダンスの授業がにがて。右手と右足がいっしょに前に出てしまう。鏡の中のわたしはペンギンみたいで、みんなが笑う。
#   先生が「好きに踊って」と言った日、みんなの前で固まってしまう。しーん。でも、ふるえる足で、よちよち歩いてみたら、それがわたしのリズムだった。
#   へたっぴでもいい。最後はみんなもいっしょに、よちよちステップ。
# 場面と強さ: ブレイク（ドラムだけ → チューバとマリンバ）→ Aメロ1（語る・中）→ Bメロ1（止め）→ サビ1（ハットが倍に・強）→ よちよち1（合いの手）
#   → Aメロ2 → Bメロ2（止め）→ サビ2 → よちよち2 → ペンギンのソロ（マリンバとピッコロ）→ 固まる（Cメロ・止め・とても弱い）
#   → Bメロ3 → サビ3（16小節・いちばん強い）→ 足音（だんだん減って、足音1つで終わる）
# 旋律の性格: 語るような8分（C4〜B♭4）。句の頭だけ16分で跳ねる。サビは D4 → G4 → B♭4 → D5 と和音をかけ上がる。
# ほかの曲とちがう所（この曲だけの音）: 拍の裏にずれる「よちよち」のリズム（チューバと足音が、4分の頭を少しずつ外して歩く）。
#   チューバがベースを吹く。止め3回（Bメロ1・Bメロ2・固まる）。
from vt25_lib import *

S = Song("05", "penguin", "ペンギン・ブレイクビーツ（仮）", "Penguin Breakbeats", 98, 4, "G", "minor", "ヒップホップ（ブレイクビーツ・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.55
K = Key("G", "minor")           # oct 3 で 1 = G3。歌うのは C4〜D5

A_CH = ["Gm7", "Cm7", "F", "Ebmaj7"]
B_CH = ["Cm7", "Gm7", "Ebmaj7", "F"]
C_CH = ["Ebmaj7", "F", "Cm7", "D7", "Ebmaj7", "F", "Cm7", "Gm7"]
X_CH = ["Gm7", "Cm7", "Ebmaj7", "F", "Gm7", "Cm7", "Ebmaj7", "D7"]

S.scene("ブレイク", 8, "intro", A_CH * 2)
S.scene("Aメロ1", 8, "verse", A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("よちよち1", 4, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("よちよち2", 4, "break", A_CH)
S.scene("ペンギンのソロ", 8, "solo", A_CH)
S.scene("固まる", 8, "bridge", X_CH)
S.scene("Bメロ3", 4, "pre", B_CH)
S.scene("サビ3", 16, "chorus", C_CH * 2)
S.scene("足音", 8, "outro", A_CH + ["Gm7", "Cm7", "Gm7", "Gm7"])

V = Voice(S, vol=0.22, delay=0.75, bright=0.0, patch="clarinet", low=False)
TUBA = S.track("チューバ（よちよちのベース）", "brass", patch="tuba", volume=0.2, pan=0.0, reverb=0.18, gainDb=3)
BASS = S.track("ベース（チューバの下の支え）", "bass", **finger_bass_spec(vol=0.13))
MAR = S.track("マリンバ", "strings", patch="marimba", volume=0.12, pan=-0.3, reverb=0.25)
MAR2 = S.track("マリンバ（和音）", "strings", patch="marimba", volume=0.08, pan=0.3, reverb=0.25)
PIC = S.track("ピッコロ（氷の上の口笛）", "panflute", patch="piccolo", volume=0.07, pan=0.35, reverb=0.35)
PN = [S.track(f"ピアノ（和音{i + 1}）", "piano", volume=0.09, pan=-0.1, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": 2}]) for i in range(3)]
STAB = [S.track(f"弦のスタッカート{i + 1}", "strings", patch="stringEnsemble", volume=0.06, pan=-0.3 + 0.3 * i, reverb=0.3, sustain=0.3) for i in range(3)]
STEP = S.track("足音（カホンの胴）", "cajon", volume=0.11, pan=0.15, reverb=0.12)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 1':0.25 1':0.25 1':0.5 7:0.5 1':0.5 5:0.5 R:0.5 5:0.5", "6:0.5 5:0.5 4:1 R:2",
      "R:0.5 3':0.25 3':0.25 3':0.5 2':0.5 1':0.5 7:0.5 R:0.5 7:0.5", "1':1 5:1 R:2"]
A1 = "たいいくのだんすがね/ほんとににがてなの/みぎてとみぎあしがね/いっしょにまえにでちゃう"
A2 = "かがみのまえのわたし/ぺんぎんみたいだね/よちよちあるいてるの/みんなわらっちゃうでしょ"
VB = ["R:0.5 3':0.5 3':0.5 4':0.5 5':1 4':1", "3':1 2':1 1':1 R:1", "R:0.5 5':0.5 5':0.5 4':0.5 3':1 4':1", "5':2 R:2"]
B1 = "みんなのまえでね/どきどきする"
B2 = "せんせいがいうの/すきにおどれ"
B3 = "ふるえるあしでも/いいんだよね"
VC = ["R:0.5 5:0.5 1':0.5 3':0.5 5':1 3':1", "4':0.5 3':0.5 2':1 R:2", "R:0.5 5:0.5 1':0.5 3':0.5 5':1 6':1", "5':2 R:2",
      "R:0.5 5:0.5 1':0.5 3':0.5 5':1 3':1", "4':0.5 3':0.5 2':1 R:2", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 3':1", "1':2 R:2"]
C1 = "ぺんぎんすてっぷで/おどるんだよ/よちよちのりずむ/わたしのもの"
C2 = "ぺんぎんすてっぷで/くるりまわる/へたっぴでもいいの/これがわたし"
C3 = "ぺんぎんすてっぷで/とびだしてく/みんなもいっしょにね/よちよちだよ/ぺんぎんすてっぷで/わらいあうの/じぶんのあしでね/それでいいの"
VX = ["R:2 5:1 1':1", "7:3 R:1", "R:2 6:1 5:1", "4:3 R:1", "R:2 5:1 1':1", "7:3 R:1", "R:2 6:1 5:1", "5:4"]
X1 = "とまる/しーん/みてる/こわい"
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1); put("Bメロ2", VB, B2); put("Bメロ3", VB, B3)
put("サビ1", VC, C1); put("サビ2", VC, C2); put("サビ3", VC + VC, C3)
put("固まる", VX, X1)
if VOCAL: put("Aメロ2", VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 4: MAR.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= チューバ（よちよち: 拍の頭を少し外して歩く） =================
def waddle(r, f5):
    # 0・0.75・1.5・2.5・3.25 拍に置く（左・右・左…と体が揺れて、少し遅れて足が出る）
    return f"{nm(r)}:0.75! {nm(f5)}:0.75 {nm(r)}:1 {nm(r + 12)}:0.75 {nm(f5)}:0.75"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "F1"); f5 = r + 7
    if n == "ブレイク" and i < 4: continue
    if n in ("固まる",):
        if i % 2 == 0: TUBA.bar(b, f"{nm(r)}:4")
        continue
    if n == "足音":
        if i < 4: TUBA.bar(b, waddle(r, f5))
        elif i < 6: TUBA.bar(b, f"{nm(r)}:0.75! R:1.25 {nm(r)}:0.75 R:1.25")
        elif i == 6: TUBA.bar(b, f"{nm(r)}:0.75! R:3.25")
        continue
    if n in ("Bメロ1", "Bメロ2", "Bメロ3"):
        TUBA.bar(b, f"{nm(r)}:1 {nm(r)}:1 {nm(f5)}:1 {nm(r + 12)}:1"); continue
    TUBA.bar(b, waddle(r, f5))
    BASS.bar(b, f"{nm(r)}:0.75 R:0.75 {nm(r)}:1 R:0.75 {nm(r)}:0.75" if n.startswith("サビ") else f"{nm(r)}:2 R:2")

# ================= マリンバ・ピアノ・弦 =================
HOOK = ["G5:0.75 Bb5:0.75 D6:1 C6:0.75 Bb5:0.75", "A5:0.75 C6:0.75 F6:1 Eb6:0.75 D6:0.75", "Eb6:0.75 D6:0.75 C6:1 Bb5:0.75 A5:0.75", "Bb5:1.5 A5:0.5 G5:2"]
SOLO = ["G5:0.5 Bb5:0.25 D6:0.25 G6:0.5 F6:0.5 D6:0.5 C6:0.5 Bb5:1", "C6:0.5 Eb6:0.25 G6:0.25 C7:0.5 Bb6:0.5 G6:1 R:1",
        "F6:0.5 A6:0.5 C7:0.5 A6:0.5 F6:0.5 Eb6:0.5 D6:1", "Eb6:0.75 D6:0.75 Bb5:1 G5:0.75 Bb5:0.75",
        "D6:0.25 C6:0.25 Bb5:0.25 A5:0.25 G5:0.5 D6:0.5 G6:1 R:1", "Eb6:0.5 G6:0.5 C7:1 Bb6:0.5 G6:0.5 Eb6:1", "F6:1 Eb6:0.5 D6:0.5 C6:1 A5:1", "Bb5:0.75 A5:0.75 G5:2.5"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 65, 3); t = tones(ch, "G4", "G6")
    if n == "ブレイク" and i >= 4: MAR.bar(b, HOOK[i % 4])
    elif n in ("よちよち1", "よちよち2"):
        MAR.bar(b, HOOK[i % 4]); PIC.bar(b, shift_oct(HOOK[i % 4], 0) if i >= 2 else "R:4")
    elif n == "ペンギンのソロ":
        MAR.bar(b, SOLO[i]); PIC.bar(b, "R:4" if i < 4 else SOLO[i])
    elif n in ("Aメロ1", "Aメロ2"):
        MAR2.bar(b, f"R:0.75 {nm(t[1])}:0.75 R:1 {nm(t[2])}:0.75 {nm(t[3 % len(t)])}:0.75")
    if n in ("サビ1", "サビ2", "サビ3"):
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 R:0.5 {nm(v[j])}:1 R:1")
        for j in range(3): STAB[j].bar(b, f"R:1 {nm(v[j] + 12)}:0.25 R:0.75 R:1 {nm(v[j] + 12)}:0.25 R:0.75")
        MAR2.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2)) + " R:3")
        if i % 4 == 3: PIC.bar(b, "R:2 " + " ".join(f"{nm(x + 12)}:0.25" for x in t[2:6]) + " R:1")
    elif n in ("Bメロ1", "Bメロ2", "Bメロ3"):
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1")
    elif n == "固まる":
        PN[0].bar(b, f"{nm(v[1])}:4" if i % 2 == 0 else "R:4")
    elif n == "足音" and i < 4:
        MAR.bar(b, HOOK[i % 4])

# ================= 足音（カホンの胴: よちよちと同じ、拍の頭を外した歩き） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("よちよち1", "よちよち2", "サビ3") or (n == "ブレイク" and i >= 4):
        STEP.bar(b, "A2:0.75 R:0.75 B2:0.75 R:1 A2:0.75")
    elif n == "足音":
        STEP.bar(b, "A2:0.75 R:0.75 B2:0.75 R:1 A2:0.75" if i < 4 else ("A2:0.75 R:1.25 B2:0.75 R:1.25" if i < 6 else ("A2:0.75 R:3.25" if i == 6 else "R:3 B2:1")))

# ================= ドラム（ブレイクビーツ。サビはハットが倍） =================
BRK_H2 = "xxxxxxxxxxxxxxxO"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ブレイク":
        vgroove(D, b, "break1" if i % 2 == 0 else "break2", ghosts=0.35, seed=b)
        if i == 3: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "break1" if i % 2 == 0 else "break2", ghosts=0.3, seed=b)
        if i == 0: crash(D, b, "C2", 3)
    elif n in ("Bメロ1", "Bメロ2", "Bメロ3"):
        vgroove(D, b, "boombap", ghosts=0.3, seed=b)
        if i == 2: put_fill(D, b, "small")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "サビ3"):
        vgroove(D, b, "break1" if i % 2 == 0 else "break2", ghosts=0.3, seed=b, h=BRK_H2)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
    elif n in ("よちよち1", "よちよち2"):
        vgroove(D, b, "boombap", ghosts=0.2, seed=b)
    elif n == "ペンギンのソロ":
        vgroove(D, b, "break2", ghosts=0.4, seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "lift")
    elif n == "固まる":
        if i >= 4: D.set(b, "X" + "." * 15, "." * 16, "x...x...x...x...")
    elif n == "足音":
        if i < 4: vgroove(D, b, "break1", ghosts=0.2, seed=b)
cym_swell(CYM, S.sc("サビ3")[0], 2, "C4")

# 止め3回: Bメロ1・Bメロ2 の最後と、固まるの頭（1拍だけ叩いて全員休み＝しーん）
for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("固まる")[0], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の05。ヒップホップ（ブレイクビーツ）。G の短調・98、転調なし。"
          "ダンスがにがての子が、自分のよちよち歩きのリズムでいいと気づく。ブレイクビーツのドラムだけで始まり、チューバが拍の頭を外して歩くベース、"
          "マリンバとピッコロの合いの手、みんなの前で固まる止め、ハットが倍になるサビ、足音1つで終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.2}, special={"固まる": -0.65, "サビ3": 0.45})
