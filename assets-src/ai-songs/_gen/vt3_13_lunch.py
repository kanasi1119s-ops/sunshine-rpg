# vt3 13「お弁当交換条約」Lunchbox Treaty（仮）— ニュージャックスウィング。106・4/4。B♭長調 → 最後のサビは +1（B）。
# 第3弾（0時〜24時の街）の 12時。表は docs/sound/vt3-plan.md。
# 物語: 昼休み。机を寄せて、お弁当のふたを開ける。卵焼きはきみ、わたしはたこさんウインナー。目で会議、交渉会がはじまる。
#   条件は同じ数ずつ。でも、からあげは特別だから2個分。最後に残ったからあげひとつに、同時にはしがのびる。
#   けっきょく半分こ。おはしとおはしを重ねて「成立しました」。次の会議は、おやつの3時に（16「おやつ宣戦布告」へ）。
# 場面と強さ: いただきます（手拍子と一言）→ イントロ（跳ねるドラムとオルガンのヒット・中）→ Aメロ1（かけ合い・中）→ Bメロ1（まじめな顔・止め）
#   → サビ1（強）→ 間奏（シンセのヒット・節）→ Aメロ2 → Bメロ2 → サビ2 → からあげ（最後のひとつ・止めと緊張）
#   → 最後のサビ（+1・いちばん強い）→ ごちそうさま
# 旋律の性格: 跳ねるリズムの短い句をかけ合いのように置く（B♭3〜F5）。サビは高い F5 から降りてくる歌いだし。
# この曲だけの音: ニュージャックスウィングの跳ねるドラム（強いスネア・3連寄りのハイハット）と、オルガン・ブラスの短いヒット。
#   合いことばの節（3・5・6・5・2＝D・F・G・F・C）は、間奏のシンセのヒット（ブラス）。
from vt25_lib import *

S = Song("13", "lunch", "お弁当交換条約（仮）", "Lunchbox Treaty", 106, 4, "Bb", "major", "ニュージャックスウィング（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --space room --space-wet 0.1"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.5
K = Key("Bb", "major")          # oct 3 で 1 = B♭3
KL = Key("B", "major")          # 最後のサビ（+1）

A_CH = ["Gm9", "Ebmaj7", "Cm9", "D7#9"]
B_CH = ["Ebmaj7", "F", "Dm7", "Gm7", "Ebmaj7", "F", "Cm7", "F7sus4"]
C_CH = ["Ebmaj7", "Dm7", "Cm7", "F7", "Bbmaj7", "Gm7", "Cm9", "F7sus4"]

S.scene("いただきます", 2, "intro", ["Bbmaj7", "Bbmaj7"])
S.scene("イントロ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("からあげ", 4, "bridge", ["Cm9", "D7#9", "Ebmaj7", "F#7"])      # 最後は B への入り口
S.scene("最後のサビ", 16, "chorus", [tr_chord(c, 1) for c in C_CH])
S.scene("ごちそうさま", 2, "outro", ["Bmaj7", "Bmaj7"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.1, patch="brightLead", low=False)
KEY = [S.track(f"FMの鍵盤{i + 1}", "keys", patch="surgeKeysFmPiano1", volume=0.06, pan=-0.35, reverb=0.2, sustain=0.6) for i in range(3)]
ORG = [S.track(f"オルガンのヒット{i + 1}", "drawbarOrgan", volume=0.05, pan=0.35, reverb=0.2, sustain=0.3) for i in range(3)]
BRS = [S.track(f"ブラスのヒット{i + 1}", "brass", patch="brassSection", volume=0.055, pan=0.15, reverb=0.25, sustain=0.35) for i in range(3)]
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassPop", vol=0.22, duck=0.2))
CLAP = S.track("手拍子", "pad", patch="seasonFx", volume=0.08, pan=0, reverb=0.15, modulate=False)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.05, pan=0, reverb=0.3)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 5:0.25 5:0.5 6:0.5 5:0.5 3:0.5 R:1", "R:0.5 1':0.25 1':0.25 7:0.5 6:0.5 5:1 R:1",
      "R:0.5 5:0.25 5:0.25 5:0.5 6:0.5 1':0.5 6:0.5 R:1", "R:0.5 2':0.25 2':0.25 1':0.5 6:0.5 5:1 R:1",
      "R:0.5 3':0.25 3':0.25 2':0.5 1':0.5 6:0.5 5:0.5 R:1", "R:0.5 6:0.25 6:0.25 5:0.5 3:0.5 2:1 R:1",
      "R:0.5 3:0.5 4:0.5 5:0.5 6:0.5 5:0.5 4:0.5 3:0.5", "2:2 R:2"]
A1 = ("おひるやすみ/つくえよせ/おべんとうの/ふたあけて/たまごやきだ/きみのほう/こっちはたこさんだ/"
      "うぃんなーだよ/めでかいぎ/こうしょうかい/はじまりだ/じょうけんはね/ひとつずつ/おなじかずだけね")
A2 = "でもちょっとまって/からあげは/とくべつなの/にこぶんだ/かわりにこれ/ぷちとまと/それじゃたりないって"
VB = ["R:1 6:0.5 6:0.5 5:0.5 6:0.5 1':1", "6:1 5:1 R:2", "R:1 5:0.5 5:0.5 4:0.5 5:0.5 6:1", "5:1 3:1 R:2",
      "R:1 6:0.5 6:0.5 1':0.5 2':0.5 3':1", "2':1 1':1 R:2", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 3':1", "2':2 R:2"]
B1 = "まじめなかおで/はなしあうのは/おかずのことよ/せかいへいわ"
B2 = "さいごにのこる/からあげひとつ/はしがのびたの/どうじにだよ"
VC = ["R:0.5 5':0.5 5':0.5 4':0.5 3':0.5 4':0.5 3':0.5 1':0.5", "2':1.5 1':0.5 6:1 R:1",
      "R:0.5 4':0.5 4':0.5 3':0.5 2':0.5 3':0.5 2':0.5 7:0.5", "1':2 R:2",
      "R:0.5 3':0.5 3':0.5 2':0.5 1':0.5 2':0.5 1':0.5 6:0.5", "5:1.5 6:0.5 1':1 R:1",
      "R:0.5 6:0.5 1':0.5 2':0.5 3':0.5 2':0.5 1':0.5 2':0.5", "2':2 R:2"]
C1 = ("おべんとうのじょうやく/ここにむすぼうよ/たまごやきとたこさん/いっこずつこうかん/"
      "おべんとうのじょうやく/はんこのかわりに/おはしとおはしかさね/せいりつしました")
C2 = ("おべんとうのじょうやく/ここにむすぼうよ/からあげのぶんかつは/はんぶんこしよう/"
      "おべんとうのじょうやく/だいいちじょうはね/なかよくわけあうこと/ずっとかわらないね")
C3 = ("おべんとうのじょうやく/あしたもあるよね/きみのすきなおかずを/わたしはしってるよ/"
      "おべんとうのじょうやく/ごちそうさまでね/つぎのかいぎはおやつ/さんじにしようね")
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC + VC, C1)
put("Aメロ2", K, VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC + VC, C2)
put("最後のサビ", KL, VC + VC, C3)
if VOCAL:
    put("いただきます", K, ["R:4", "R:1 5:0.5 5:0.5 5:0.5 6:0.5 5:0.5 3:0.5"], "いただきます")
    put("ごちそうさま", KL, ["R:1 5:0.5 5:0.5 6:0.5 5:0.5 3:0.5 1:0.5", "R:4"], "ごちそうさま")

# ================= 鍵盤・ヒット =================
def keys(b, ch, pat):
    v = voice(ch, 64, 3)
    for j in range(3): KEY[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def hit(tracks, b, ch, pat, c=67):
    v = voice(ch, c, 3)
    for j in range(3): tracks[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


SWING_KEYS = "x:0.75 R:0.25 x:0.5 R:1 x:0.5 x:0.5 R:0.5"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        keys(b, ch, SWING_KEYS)
        hit(ORG, b, ch, "x:0.5! R:1 x:0.25 R:2.25" if i % 2 == 0 else "R:2 x:0.25 R:0.25 x:0.5 R:1")
    elif n in ("Aメロ1", "Aメロ2"):
        keys(b, ch, SWING_KEYS if (n == "Aメロ2" or i >= 4) else "x:2 R:2")
        if i % 4 == 3: hit(ORG, b, ch, "R:3 x:0.25 R:0.25 x:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        keys(b, ch, "x:1 x:1 x:1 x:1")
        if i % 2 == 1: hit(BRS, b, ch, "R:2.5 x:0.5 R:1")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        keys(b, ch, SWING_KEYS)
        hit(BRS, b, ch, "x:0.5! R:3.5" if i % 4 == 0 else ("R:2.5 x:0.25 R:0.25 x:0.5 R:0.5" if i % 2 == 1 else "R:4"))
        if i % 2 == 0: hit(ORG, b, ch, "R:1.5 x:0.25 R:2.25")
    elif n == "間奏":
        keys(b, ch, SWING_KEYS)
        MOT = ["R:1 D5:0.5 F5:0.5 G5:1 F5:0.5 C5:0.5", "Bb4:3 R:1"]   # 合いことばの節（3・5・6・5・2）
        if i in (2, 3):
            for j in range(3): BRS[j].bar(b, shift_oct(MOT[i - 2], 0) if j == 2 else shift_oct(MOT[i - 2], -1) if j == 1 else "R:4")
        else: hit(ORG, b, ch, "x:0.5! R:1 x:0.25 R:2.25" if i % 2 == 0 else "R:2 x:0.25 R:0.25 x:0.5 R:1")
    elif n == "からあげ":
        hit(ORG, b, ch, "x:0.25! R:3.75" if i < 3 else "x:0.25 R:0.25 x:0.25 R:0.25 x:0.25 R:0.25 x:0.25 R:0.25 x:1 R:1")
    elif n in ("いただきます", "ごちそうさま"):
        if n == "ごちそうさま" and i == 1: keys(b, ch, "x:3 R:1"); hit(BRS, b, ch, "x:0.5! R:3.5")

for b in S.sc("いただきます"): CLAP.bar(b, "B4:1 B4:1 R:2" if b == S.sc("いただきます")[0] else "R:4")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("イントロ", "Aメロ1", "Aメロ2", "サビ1", "サビ2", "最後のサビ", "間奏"):
        BASS.bar(b, f"{nm(r)}:0.75 R:0.25 {nm(r)}:0.5 R:0.5 {nm(r + 12)}:0.25 R:0.25 {nm(r + 10)}:0.5 {nm(r + 7)}:0.5 {nm(r)}:0.5")
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "push", lo="E1"))
    elif n == "からあげ": BASS.bar(b, f"{nm(r)}:0.25 R:3.75")
    elif n == "ごちそうさま" and i == 1: BASS.bar(b, f"{nm(r)}:0.5 R:3.5")

riser(FX, S.sc("最後のサビ")[0], 4, "C4")

# ================= ドラム（ニュージャックスウィング: 強いスネア・跳ねるハイハット）=================
NK, NS, NH = "X.....X...X..X..", "....X.......X...", "x.xx.xx.x.xx.xx."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("いただきます", "ごちそうさま"):
        if n == "ごちそうさま" and i == 1: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)
        continue
    if n == "からあげ":
        D.set(b, "X...............", "X...............", "................") if i < 3 else D.set(b, "X.X.X.X.X.......", "....X.X.XXXXXXXX", "................")
        continue
    if n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.......X.X.....", s=NS, h="x.x.x.x.x.x.x.x.")
        if i == 7: put_fill(D, b, "snare16")
        continue
    vgroove(D, b, "beat8", ghosts=0.4, seed=b, k=NK, s=NS, h=NH)
    if n in ("サビ1", "サビ2", "最後のサビ") and i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
    if i % 8 == 7 and not last: put_fill(D, b, "small")
    if last and n in ("サビ1", "サビ2", "Aメロ1", "Aメロ2", "間奏", "イントロ"): put_fill(D, b, "snare16")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の13（12時）。ニュージャックスウィング。B♭・106、最後のサビは +1。昼休みにお弁当のおかずの交換を、まじめに話し合う。"
          "跳ねるドラム・オルガンとブラスのヒット・FMの鍵盤・シンセベース。合いことばの節は間奏のブラスのヒット。「いただきます」で始まり「ごちそうさま」で終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"からあげ": -0.3, "最後のサビ": 0.4})
