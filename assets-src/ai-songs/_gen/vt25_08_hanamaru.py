# vt25 08「はなまるリグレット」Hanamaru Regret（仮）— J-POP（ピアノポップ×ブラス）。150・4/4。D 長調。転調なし。
#   （表では J-POP バンド 170・アコギ・グロッケン・ストリングスだったが、第1弾の 08「からっぽのポケットに銀河」と楽器と速さが似るので、
#     ピアノとブラスのポップにして、子どものころの場面だけ おもちゃのピアノ にした）
# 物語: 大人になって、仕事でしっぱいした夕方。電車の窓に泣きそうな顔。かばんの底から、小学校の連絡帳が出てくる。
#   開いたページに、先生の赤いペンの大きな「はなまる」。逆上がりができた、それだけの日に。小さなことでもほめてくれた人。
#   大人になってから、はなまるはもらえない。でも、がんばった自分に、自分でまるをつけよう。ゆがんでいても、わたしの手で。
# 場面と強さ: はなまる（おもちゃのピアノの節 → バンド・中）→ Aメロ1（電車の窓・語る）→ Bメロ1 → サビ1（強）→ 間奏（ブラスのリフ）
#   → Aメロ2（連絡帳＝子どものころ。おもちゃのピアノが入る）→ Bメロ2 → サビ2 → 帰り道（ハーフの重さ・弱。ピアノとおもちゃのピアノ）
#   → Cメロ（自分でほめる）→ 最後のサビ（24小節・いちばん強い）→ ピアノの和音だけ残す
# 旋律の性格: 長いのばしで歌う、わかりやすい旋律（A3〜A4 で語り、サビは A4 → D5 のオクターブの上で、C#5・B4 と歌う）。
# ほかの曲とちがう所（この曲だけの音）: 子どものころの場面（はなまる・Aメロ2・帰り道）だけ、音がおもちゃのピアノになる。
from vt25_lib import *

S = Song("08", "hanamaru", "はなまるリグレット（仮）", "Hanamaru Regret", 150, 4, "D", "major", "J-POP（ピアノポップ×ブラス・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.55
S.keepers = {"Aメロ1": "closed", "Aメロ2": "ride", "サビ2": "open"}
K = Key("D", "major")           # oct 3 で 1 = D3。歌うのは A3〜E5

A_CH = ["D", "A/C#", "Bm7", "F#m7", "Gmaj7", "D/F#", "Em7", "A7sus4"]
B_CH = ["Gmaj7", "A", "Bm7", "Bm7", "Em7", "F#m7", "Gmaj7", "A"]
C_CH = ["D", "A/C#", "Bm7", "Gmaj7", "Em7", "A", "Bm7", "Gmaj7", "D", "A/C#", "Bm7", "Gmaj7", "Em7", "A", "Em7", "D"]
X_CH = ["Gmaj7", "A", "Bm7", "Gmaj7", "Em7", "A", "Gmaj7", "A"]

S.scene("はなまる", 8, "intro", ["D", "Gmaj7", "D", "A", "D", "A/C#", "Bm7", "A7sus4"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 12, "break", ["D", "A/C#", "Bm7", "Gmaj7"] * 3)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("帰り道", 12, "break", ["Gmaj7", "A", "F#m7", "Bm7", "Em7", "A", "D", "D", "Gmaj7", "A", "Gmaj7", "A"])
S.scene("Cメロ", 8, "bridge", X_CH)
S.scene("最後のサビ", 24, "chorus", C_CH + C_CH[8:])
S.scene("和音", 8, "outro", ["Gmaj7", "A", "F#m7", "Bm7", "Em7", "A", "Dmaj9", "Dmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.3, patch="altoSax", low=False)
PL = S.track("ピアノ（左手）", "piano", volume=0.14, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -1, "mid": -2, "midHz": 400, "high": 2}])
PR = S.track("ピアノ（右手）", "piano", volume=0.14, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3.5}])
PR2 = S.track("ピアノ（右手の上）", "piano", volume=0.11, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3.5}])
TOY = S.track("おもちゃのピアノ（子どものころ）", "pad", patch="surgeKeysBellPiano", volume=0.085, pan=0.25, reverb=0.3, sustain=0.6)
BRS = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.075, pan=-0.3 + 0.3 * i, reverb=0.25, sustain=0.8) for i in range(3)]
TPT = S.track("トランペット（ブラスのリフの上）", "brass", patch="trumpet", volume=0.08, pan=0.2, reverb=0.28)
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.21))
STR = [S.track(f"ストリングス{i + 1}（最後のサビ）", "strings", patch="stringEnsemble", volume=0.06, pan=-0.3 + 0.3 * i, reverb=0.4, sustain=1.4) for i in range(3)]
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 1':0.5 2':0.5 3':0.5 3':1 2':1", "7:1.5 6:0.5 5:1 R:1", "R:0.5 6:0.5 7:0.5 1':0.5 1':1 7:1", "6:1.5 5:0.5 6:1 R:1",
      "R:0.5 5:0.5 6:0.5 7:0.5 1':1 5':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 2':0.5 2':0.5 3':0.5 4':1 3':1", "2':2 R:2"]
A1 = "でんしゃのまどにね/なきそうなかおで/きょうもしっぱいだね/ためいきだよ/かばんのそこから/ちいさなてちょうが/でてきたのはなぜ/わからないや"
A2 = "あけたぺーじのね/あかいはなまるが/せんせいのもじで/がんばったねって/さかあがりできた/それだけのひにね/おおきなはなまる/くれたんだね"
VB = ["R:0.5 5':0.5 5':0.5 4':0.5 3':1 2':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 3':0.5 3':0.5 4':0.5 5':1 3':1", "2':1.5 1':0.5 2':1 R:1",
      "R:0.5 2':0.5 3':0.5 4':0.5 5':1 6':1", "5':1.5 4':0.5 3':1 R:1", "R:0.5 3':0.5 4':0.5 5':0.5 6':1 7':1", "6':2 R:2"]
B1 = "ちいさなことでも/ほめてくれたひと/おとなになってから/もらえないね"
B2 = "てすとのまるより/あのはなまるがね/なぜだかいまでも/うれしいんだ"
VC = ["R:0.5 5':0.5 1'':1 7':0.5 6':0.5 5':1", "6':1 7':1 6':1 R:1", "R:0.5 4':0.5 6':1 5':0.5 4':0.5 3':1", "5':2 R:2",
      "R:0.5 2':0.5 6':1 5':0.5 4':0.5 2':1", "3':1 4':1 5':1 R:1", "R:0.5 5':0.5 6':0.5 7':0.5 1'':1 7':1", "6':2 R:2"]
VC2 = VC[:6] + ["R:0.5 3':0.5 4':0.5 5':0.5 6':1 7':1", "1'':2 R:2"]
C1 = "はなまるちょうだい/このわたしに/できなかったことも/ちいさなまる/はなまるのかずを/かぞえないで/がんばったじぶんに/まるつけよう"
C2 = "はなまるちょうだい/つかれたひも/なにもできなかった/それでもまる/あかいぺんのあと/いまもひかる/わすれていたこと/おもいだした"
CL = C1 + "/はなまるのかたち/ゆがんでても/わたしのてでいま/かいてみるよ"
VX = ["R:1 3':1 2':1 1':1", "2':3 R:1", "R:1 3':1 5':1 6':1", "5':3 R:1", "R:1 6':1 5':1 4':1", "3':3 R:1", "R:1 2':1 3':1 4':1", "5':4"]
X1 = "えらいね/ほめてよ/じぶんで/いえるよ"
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)
    return mel


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1); put("Bメロ2", VB, B2)
put("サビ1", VC + VC2, C1); put("サビ2", VC + VC2, C2)
put("Cメロ", VX, X1)
put("最後のサビ", VC + VC2 + VC2, CL)
if VOCAL: put("Aメロ2", VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: TOY.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= おもちゃのピアノ（子どものころの場面） =================
TOYM = ["F#5:1 A5:1 D6:2", "B5:1 A5:1 G5:2", "F#5:1 A5:1 D6:1 E6:1", "C#6:4",
        "F#5:0.5 G5:0.5 A5:1 B5:1 A5:1", "G5:1 F#5:1 E5:2", "D5:1 F#5:1 A5:1 B5:1", "A5:4"]
for i, b in enumerate(S.sc("はなまる")): TOY.bar(b, TOYM[i])
for i, b in enumerate(S.sc("帰り道")): TOY.bar(b, TOYM[i % 8] if i < 8 else "R:4")
if VOCAL:
    for i, b in enumerate(S.sc("Aメロ2")):
        if i % 4 == 3: TOY.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(S.chords[b], "D6", "D7")[:4]))
TOY.bar(S.sc("和音")[-1], "R:1 D6:0.5 F#6:0.5 A6:2")

# ================= ピアノ =================
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C2"); v4 = voice(ch, 66, 4, prev=prev); prev = v4
    if n == "はなまる":
        if i >= 4:
            PL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:0.5 {nm(r)}:2")
            PR.bar(b, f"{nm(v4[0])}:0.75 {nm(v4[1])}:0.75 {nm(v4[2])}:0.5 {nm(v4[3])}:2")
    elif n in ("Aメロ1", "Aメロ2"):
        PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:1 {nm(r + 12)}:1")
        PR.bar(b, f"R:1 {nm(v4[0])}:0.5 {nm(v4[1])}:0.5 R:1 {nm(v4[2])}:0.5 {nm(v4[3])}:0.5")
    elif n in ("Bメロ1", "Bメロ2", "Cメロ"):
        PL.bar(b, " ".join(f"{nm(r if q % 2 == 0 else r + 12)}:0.5" for q in range(8)))
        PR.bar(b, f"{nm(v4[0])}:1 {nm(v4[1])}:1 {nm(v4[2])}:1 {nm(v4[3])}:1")
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏"):
        # ピアノポップの16分の刻み（右手の和音を 16分の裏で）
        PL.bar(b, f"{nm(r)}:0.75 {nm(r + 12)}:0.75 {nm(r)}:0.5 {nm(r + 7)}:0.75 {nm(r + 12)}:0.75 {nm(r + 7)}:0.5")
        PR.bar(b, f"{nm(v4[0])}:0.5 {nm(v4[1])}:0.25 {nm(v4[2])}:0.25 R:0.5 {nm(v4[3])}:0.5 {nm(v4[2])}:0.5 {nm(v4[1])}:0.25 {nm(v4[0])}:0.25 R:0.5 {nm(v4[3])}:0.5")
        if i % 2 == 0: PR2.bar(b, f"{nm(v4[3] + 12)}:1.5 {nm(v4[2] + 12)}:1 {nm(v4[3] + 12)}:1.5")
    elif n == "帰り道":
        PL.bar(b, f"{nm(r)}:4")
        PR.bar(b, f"{nm(v4[0])}:2 {nm(v4[2])}:2" if i % 2 == 0 else f"{nm(v4[1])}:2 {nm(v4[3])}:2")
    elif n == "和音":
        if i < 6:
            PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); PR.bar(b, " ".join(f"{nm(x)}:1" for x in v4))
        elif i == 6:
            PL.bar(b, f"{nm(r)}:8"); PR.bar(b, " ".join(f"{nm(x)}:0.25" for x in v4) + f" {nm(v4[3] + 12)}:7")

# ================= ブラス（間奏のリフ・サビの合いの手） =================
RIFF = ["A5:0.5 A5:0.25 B5:0.25 R:0.5 A5:0.5 F#5:0.5 E5:0.5 D5:1", "R:0.5 C#5:0.5 E5:0.5 A5:0.5 G5:1 F#5:1",
        "B5:0.5 B5:0.25 C#6:0.25 R:0.5 B5:0.5 A5:0.5 F#5:0.5 D5:1", "R:0.5 G5:0.5 F#5:0.5 E5:0.5 D5:1 E5:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; bv = voice(ch, 67, 3)
    if n == "間奏" or (n == "はなまる" and i >= 4):
        TPT.bar(b, RIFF[i % 4])
        for j in range(3): BRS[j].bar(b, f"{nm(bv[j])}:0.5 R:1 {nm(bv[j])}:0.25 R:0.75 {nm(bv[j])}:0.5 R:1")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        if i % 2 == 1:
            for j in range(3): BRS[j].bar(b, f"R:2 {nm(bv[j])}:0.25 R:0.25 {nm(bv[j])}:0.5 R:1")
        if n == "最後のサビ" and i >= 8:
            sv = voice(ch, 62, 3)
            for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    elif n == "和音" and i == 6:
        for j in range(3): BRS[j].bar(b, f"{nm(bv[j])}:6")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "はなまる":
        if i >= 4: BASS.bar(b, bass_line(S, b, "half", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half" if i < 8 else "walk", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2", "Cメロ"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏"): BASS.bar(b, bass_line(S, b, "push" if i % 2 else "oct8", lo="E1"))
    elif n == "帰り道": BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n == "和音" and i < 7: BASS.bar(b, bass_line(S, b, "half" if i < 6 else "long", lo="E1"))
cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "はなまる":
        if i >= 4: vgroove(D, b, "beat8", ghosts=0.2, seed=b)
        if i == 4: crash(D, b)
        if i == 7: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "vrock2", ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "間奏":
        vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if i % 4 == 0: crash(D, b)
        if last: put_fill(D, b, "lift")
    elif n == "帰り道":
        vgroove(D, b, "half", ghosts=0.15, seed=b)
        if i == 0: crash(D, b, "C2", 6)
    elif n == "Cメロ":
        vgroove(D, b, "halfdrive", ghosts=0.25, seed=b)
        if last: put_fill(D, b, "build")
    elif n == "和音":
        if i < 6: vgroove(D, b, "beat8", ghosts=0.2, seed=b)
        if i == 6: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の08。J-POP（ピアノポップ×ブラス）。D 長調・150、転調なし。"
          "大人になってしっぱいした日に、小学校の先生がくれた「はなまる」を思い出す。おもちゃのピアノの節で始まり、ピアノの16分の刻みとブラスのリフ、"
          "子どものころの場面だけ おもちゃのピアノ、ハーフの重さの帰り道、自分でほめる Cメロ、ピアノの和音だけ残して終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.3}, special={"Cメロ": -0.35, "最後のサビ": 0.5})
