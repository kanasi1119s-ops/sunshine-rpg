# vt25 10「ゆびきりアルゴリズム」Pinky-Promise Algorithm（仮）— テクノポップ。178・4/4。E の短調（サビは G 長調）→ 最後のサビは +1（A♭）。
# 物語: 指切りの数をかぞえるのがくせの「わたし」。きのうで108。ぜんぶ守った。数がふえるたび安心していた。
#   でも、寝坊した109番目の約束だけが「ばつ」のまま。駅の時計の下で、きみはひとりで待っていた。ごめんのメールも送れないまま、数をかぞえて指が痛い。
#   きみは「かぞえなくていいよ」と笑う。数をかぞえるのをやめた日、約束のルールを変える。できなかった時はごめんねと言って、何度でも結びなおす。
# 場面と強さ: 手拍子（数をかぞえる手拍子 → バンド）→ Aメロ1（かぞえる・語る）→ Bメロ1 → サビ1（強）→ 間奏（スタッター）→ Aメロ2（109番目）
#   → Bメロ2 → サビ2（24小節）→ 間奏2 → Cメロ（数をかぞえるのをやめる・ハーフ・弱。最後に1拍の無音）→ 落ちサビ（とても弱い）
#   → 最後のサビ（+1・24小節）→ やくそく（和音で切る）
# 旋律の性格: Aメロは同じ音の連打で「かぞえる」（E4 を4回 → F#4 → G4）。サビは G 長調の三和音で跳ぶ（G4 → B4 → D5）。
# ほかの曲とちがう所（この曲だけの音）: 指切りの「ちょん」（小さな高いはじく音）が、サビの小節の頭ごとに入る。手拍子のカウント。
#   01（テクノポップ）とは音色を変えた: フォルマントのパルス・ベルの矩形波の和音・ピアノのスタブ・手拍子。
from vt25_lib import *

S = Song("10", "yubikiri", "ゆびきりアルゴリズム（仮）", "Pinky-Promise Algorithm", 178, 4, "E", "minor", "テクノポップ（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space sky --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.55
K = Key("E", "minor")           # Aメロ（oct 3 で 1 = E3。歌うのは B3〜E5）
KG = Key("G", "major")          # Bメロ以外のサビ（oct 4 で 1 = G4）
KL = Key("Ab", "major")         # 最後のサビ（+1）

A_CH = ["Em7", "Cmaj7", "G", "D/F#"]
B_CH = ["Am7", "Bm7", "Cmaj7", "D", "Am7", "Bm7", "Cmaj7", "D7"]
C_CH = ["G", "D/F#", "Em7", "Cmaj7", "G", "D", "Am7", "D7"]
C_CH2 = C_CH[:6] + ["Am7", "G"]
X_CH = ["Cmaj7", "D", "Bm7", "Em7"] * 2 + ["Am7", "Bm7", "Cmaj7", "D"] * 2
LAST = [tr_chord(c, 1) for c in C_CH + C_CH2 + C_CH2]

S.scene("手拍子", 12, "intro", ["Em7"] * 4 + A_CH * 2)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("間奏", 12, "break", A_CH * 3)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 24, "chorus", C_CH + C_CH2 + C_CH2)
S.scene("間奏2", 12, "solo", A_CH * 3)
S.scene("Cメロ", 16, "bridge", X_CH)
S.scene("落ちサビ", 8, "bridge", C_CH[:7] + ["Eb7"])          # 最後の小節は A♭ への入り口
S.scene("最後のサビ", 24, "chorus", LAST)
S.scene("やくそく", 10, "outro", [tr_chord(c, 1) for c in ["Cmaj7", "D", "Bm7", "Em7", "Am7", "D", "G", "G"]] + ["Ab", "Ab"])

V = Voice(S, vol=0.21, delay=0.75, bright=1.0, patch="surgeFormantPulse", low=True)
PULSE = S.track("フォルマントのパルス（かぞえる音）", "lead", patch="surgeFormantPulse", volume=0.055, pan=-0.3, reverb=0.2, mono=True,
                fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}])
BSQ = [S.track(f"ベルの矩形波の和音{i + 1}", "pad", patch="surgeChordBellSquare2", volume=0.045, pan=-0.3 + 0.3 * i, reverb=0.3, sustain=0.5) for i in range(3)]
PST = [S.track(f"ピアノのスタブ{i + 1}", "piano", volume=0.1, pan=0.15, reverb=0.2, fx=[{"type": "eq", "low": -4, "mid": -1, "midHz": 400, "high": 3}]) for i in range(3)]
STUT = [S.track(f"スタッター{i + 1}", "pad", **pad_spec("surgeHappySaws", vol=0.04, pan=-0.35 + 0.35 * i, duck=0.3, sustain=0.2)) for i in range(3)]
SAW = [S.track(f"サビの和音{i + 1}", "pad", **pad_spec("surgeChordEldorado", vol=0.04, pan=-0.4 + 0.4 * i, duck=0.45, sustain=0.9)) for i in range(3)]
CHON = S.track("指切りの「ちょん」", "pad", patch="surgeNicePluck", volume=0.06, pan=0.35, reverb=0.3, sustain=0.3,
               fx=[{"type": "filter", "kind": "highpass", "freq": 900, "q": 0.7}])
BASS = S.track("シンセベース（オクターブ）", "bass", **synth_bass_spec("synthBass2", vol=0.22, duck=0.3))
CLAP = S.track("手拍子（カホンの縁）", "cajon", volume=0.1, pan=-0.15, reverb=0.2)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.065, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 1':0.5 1':0.5 1':0.5 1':0.5 2':0.5 3':1", "2':1 1':1 R:2", "R:0.5 3':0.5 3':0.5 3':0.5 3':0.5 4':0.5 5':1", "4':1 2':1 R:2"]
A1 = "ゆびきりのかずを/かぞえるのがくせ/きのうでひゃくはち/ぜんぶまもったんだ/あしたもあおうね/ゆびきりげんまん/かずがふえるたび/あんしんしてたの"
A2 = "だけどきのうはね/ねぼうしちゃったんだ/えきのとけいだけ/きみはまっていたの/ひゃくきゅうばんめの/やくそくだけがね/ばつになってるんだ/かぞえられないよ"
VB = ["R:0.5 4':0.5 4':0.5 5':0.5 6':1 5':1", "4':1.5 3':0.5 2':1 R:1", "R:0.5 3':0.5 3':0.5 4':0.5 5':1 7':1", "6':1.5 5':0.5 4':1 R:1",
      "R:0.5 4':0.5 4':0.5 5':0.5 6':1 1'':1", "7':1.5 6':0.5 5':1 R:1", "R:0.5 5':0.5 6':0.5 7':0.5 1'':1 7':1", "6':2 R:2"]
B1 = "ゆびきりのうたは/ちょっぴりこわいうた/はりせんぼんのむ/のめないよね"
B2 = "ごめんのめーるも/おくれないままで/かずをかぞえてる/ゆびがいたい"
VC = ["R:0.5 1:0.5 3:0.5 5:1 3:0.5 5:1", "6:1 5:1 3:1 R:1", "R:0.5 1:0.5 3:0.5 5:1 6:0.5 5:1", "3:2 R:2",
      "R:0.5 1:0.5 3:0.5 5:1 3:0.5 6:1", "5:1 3:1 2:1 R:1", "R:0.5 6:0.5 5:0.5 3:0.5 2:1 1:1", "2:2 R:2"]
VC2 = VC[:6] + ["R:0.5 3:0.5 5:0.5 6:0.5 5:1 3:1", "1:2 R:2"]
C1 = "ゆびきりのるーる/かぞえなくて/いいんだよってきみ/わらってくれた/かぞえたかずより/だいじなこと/まもれなかったひも/そばにいたい"
C2 = ("ゆびきりのるーる/かえてみよう/できなかったときは/ごめんねいう/ゆびきりやくそく/むすびなおす/なんかいでもいい/またあしたね/"
      "かぞえるかわりに/てをつなごう/ゆびのぬくもりを/おぼえておく")
CL = ("ゆびきりのるーる/あたらしいの/かぞえないかわり/まいにちいう/ゆびきりげんまん/うそじゃないよ/ばつがついたひも/やりなおそう/"
      "やくそくしようね/ゆびをだして/かぞえなくていい/きみとならね")
CO = "ゆびきりのるーる/ちいさなこえ/まだこわいけれど/ゆびをだすよ"
VX = ["R:1 3:1 2:1 1:1", "2:3 R:1", "R:1 3:1 5:1 6:1", "5:3 R:1", "R:1 6:1 5:1 3:1", "2:3 R:1", "R:1 1:1 2:1 3:1", "1:3 R:1"]
VX2 = VX[:7] + ["2:3 R:1"]
X1 = "ひゃくはち/ひゃくきゅう/ひゃくじゅう/やめたよ/かずより/きみのて/あたたか/いいよね"
LY = Lyrics(S)


def put(name, key, lines, text, o):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA * 4, A1, 3)
put("Bメロ1", K, VB, B1, 3); put("Bメロ2", K, VB, B2, 3)
put("サビ1", KG, VC + VC2, C1, 4); put("サビ2", KG, VC + VC2 + VC2, C2, 4)
put("Cメロ", KG, VX + VX2, X1, 4)
put("落ちサビ", KG, VC, CO, 4)
put("最後のサビ", KL, VC + VC2 + VC2, CL, 4)
put("やくそく", KL, ["R:4"] * 6 + ["R:1 1:0.5 2:0.5 3:1 5:1", "R:4", "R:4", "R:4"], "やくそく", 4)
if VOCAL: put("Aメロ2", K, VA * 4, A2, 3)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA * 4)):
        if i < 8: PULSE.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 66, 3); t = tones(ch, "B4", "B6")
    if n == "手拍子" and i < 4: continue
    if n in ("Aメロ1", "Aメロ2", "手拍子", "間奏"):
        if not (n == "Aメロ2" and not VOCAL and i < 8):          # BGM の Aメロ2 の前半は、パルスが歌を受け取る
            PULSE.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 0, 2, 0, 1, 0, 3, 2)))
        for j in range(3): BSQ[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:1 {nm(v[j])}:0.25 R:0.75 {nm(v[j])}:0.5 R:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        for j in range(3): PST[j].bar(b, f"{nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5")
        if i == 7:
            for j in range(3): STUT[j].bar(b, " ".join(f"{nm(v[j])}:0.125" for _ in range(32)))      # スタッター（サビの前）
    elif n.startswith(("サビ", "最後", "落ちサビ")):
        sv = voice(ch, 64, 3)
        if n != "落ちサビ":
            for j in range(3): SAW[j].bar(b, f"{nm(sv[j])}:1.5 {nm(sv[j])}:1 {nm(sv[j])}:1.5")
            for j in range(3): PST[j].bar(b, f"R:0.5 {nm(v[j])}:0.25 R:1.25 {nm(v[j])}:0.25 R:0.75 {nm(v[j])}:0.25 R:0.75")
            PULSE.bar(b, piano_arp16(ch, "B4", "B6", pat=(0, 2, 1, 3, 2, 4, 3, 5)))
        else:
            for j in range(3): BSQ[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2")
        CHON.bar(b, f"{nm(t[-1])}:0.25 R:3.75")                              # 指切りの「ちょん」（小節の頭）
    elif n == "間奏2":
        for j in range(3): STUT[j].bar(b, " ".join(f"{nm(v[j])}:0.25" if q % 4 != 3 else "R:0.25" for q in range(16)) if i % 4 < 3
                                       else " ".join(f"{nm(v[j])}:0.125" for _ in range(32)))
        PULSE.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 1, 3, 5, 3)))
    elif n == "Cメロ":
        for j in range(3): BSQ[j].bar(b, f"{nm(v[j])}:4")
    elif n == "やくそく":
        if i < 6:
            for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:4")
        elif i == 8:
            for j in range(3): PST[j].bar(b, f"{nm(v[j])}:0.5! R:3.5")
            CHON.bar(b, f"{nm(t[-1])}:0.25 R:3.75")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "手拍子":
        if i >= 4: BASS.bar(b, bass_line(S, b, "oct8", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half" if i < 8 else "oct8", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "pulse", lo="E1"))
    elif n.startswith(("サビ", "最後")) or n.startswith("間奏"): BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "disco", lo="E1"))
    elif n == "Cメロ": BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n == "やくそく" and i < 8: BASS.bar(b, bass_line(S, b, "oct8" if i < 6 else "long", lo="E1"))

# ================= 手拍子（数をかぞえる） =================
for i, b in enumerate(S.sc("手拍子")):
    if i < 4: CLAP.bar(b, ["G3:1! R:3", "G3:1! R:1 G3:1! R:1", "G3:1! G3:1! G3:1! R:1", "G3:1! G3:1! G3:1! G3:1!"][i])
for name in ("Aメロ1", "Aメロ2"):
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 1: CLAP.bar(b, "R:1 G3:1 R:1 G3:1")
riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("最後のサビ")[0], 4, "C4")
cym_swell(CYM, S.sc("サビ2")[0], 2, "C4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "手拍子":
        if i >= 4: vgroove(D, b, "four", ghosts=0.2, seed=b)
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "half" if i < 8 else "vrock2", ghosts=0.25, seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X.......X.......", "........XXXXXXXX", "................")
    elif n.startswith(("サビ", "最後")):
        vgroove(D, b, "four16", ghosts=0.2, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
    elif n in ("間奏", "間奏2"):
        vgroove(D, b, "four" if n == "間奏" else "vrock", ghosts=0.25, seed=b)
        if i % 4 == 0: crash(D, b)
        if last: put_fill(D, b, "lift")
    elif n == "Cメロ":
        vgroove(D, b, "half", ghosts=0.15, seed=b)
        if i == 15: put_fill(D, b, "build")
    elif n == "落ちサビ":
        if i >= 4: D.set(b, "X...X...X...X...", "................", "................")
    elif n == "やくそく":
        if i < 6: vgroove(D, b, "four16", ghosts=0.2, seed=b)
        if i == 8: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 6)

# 1拍の完全な無音: Cメロの最後（数をかぞえるのをやめる）と、最後のサビの直前
SIL.add(S.sc("Cメロ")[-1], 3, 4); SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の10。テクノポップ。E の短調（サビは G）・178、最後のサビは +1（A♭）。"
          "指切りの数をかぞえるのがくせの子が、守れなかった約束に向き合う。数をかぞえる手拍子で始まり、同じ音の連打の Aメロ、サビの小節の頭ごとの指切りの「ちょん」、"
          "スタッター、数をかぞえるのをやめる1拍の無音、「やくそく」の和音で切る。自作")
finish(S, LY, V, 0, level={"verse": -0.25}, special={"Cメロ": -0.45, "落ちサビ": -0.6, "最後のサビ": 0.5})
