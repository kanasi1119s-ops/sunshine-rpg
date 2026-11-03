# vt25 13「ビー玉の中の夏」Summer Inside a Marble（仮）— エレクトロニカ（IDM・ブレイクビート×和の音）。132・4/4。E 長調。転調なし。
#   （第1弾の 13「まばたきプリズム」（グリッチポップ・ガラスの音・高い跳躍）と似ないように、祖母の家の夏の音（風鈴・蝉・琴・カリンバ）と、
#     息の長い、句の終わりで少し下がる旋律にした）
# 物語: 今年の夏、祖母の家の縁側。ビー玉をひとつのぞくと、青い中に去年の夏がゆれていた。いとこと、すいかの種を飛ばした庭。
#   蝉の声と笑い声。祖母がうちわであおいでくれた。今年は、もう祖母はいない。ころがるビー玉、まだ止まらないで、もう少しだけ見ていたい。
#   ビー玉の中では夏が続く。来年もまた、ここに来るね。
# 場面と強さ: ビー玉（ころがる音・風鈴・蝉）→ Aメロ1（弱）→ Bメロ1 → サビ1（去年の夏に入る・強）→ 風鈴だけ（とても弱い）
#   → Aメロ2 → Bメロ2 → サビ2 → ソロ（琴とマリンバ）→ 落ちサビ（ゆがむ・逆さの音）→ 最後のサビ → ビー玉が止まる
# 旋律の性格: 息の長い、句の終わりで少し下がる旋律（B3〜E5）。サビは B4 → E5 と5度上がってから、ゆっくり降りる。
# ほかの曲とちがう所（この曲だけの音）: 風鈴の音がそのまま和音になる（高いグロッケンの3つの音が、和音の音で鳴る）。
#   ビー玉がころがる音（木琴の細かい下がり）で始まり、止まる音で終わる。
from vt25_lib import *

S = Song("13", "biidama", "ビー玉の中の夏（仮）", "Summer Inside a Marble", 132, 4, "E", "major", "エレクトロニカ（IDM・ブレイクビート×和の音・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.18"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.5
K = Key("E", "major")           # oct 3 で 1 = E3。歌うのは B3〜E5

A_CH = ["Emaj7", "G#m7", "C#m7", "Amaj7", "F#m7", "B", "Emaj7", "B/D#"]
B_CH = ["C#m7", "A", "B", "G#m7", "C#m7", "F#m7", "A", "B7sus4"]
C_CH = ["Amaj7", "B", "G#m7", "C#m7", "F#m7", "B", "Emaj7", "Emaj7"]
C_CH2 = ["Amaj7", "B", "G#m7", "C#m7", "F#m7", "B", "Amaj7", "E"]

S.scene("ビー玉", 8, "intro", ["Emaj7", "Amaj7", "Emaj7", "Amaj7", "Emaj7", "G#m7", "Amaj7", "B"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("風鈴だけ", 6, "break", ["Emaj7", "Amaj7", "Emaj7", "Amaj7", "F#m7", "B"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH + C_CH2)
S.scene("ソロ", 8, "solo", A_CH)
S.scene("落ちサビ", 8, "bridge", C_CH)
S.scene("最後のサビ", 16, "chorus", C_CH + C_CH2)
S.scene("ビー玉が止まる", 8, "outro", ["Amaj7", "B", "G#m7", "C#m7", "Amaj7", "B", "Emaj9", "Emaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=-0.3, patch="shakuhachi", low=False)
MAR = S.track("マリンバ（分散和音）", "strings", patch="marimba", volume=0.11, pan=-0.3, reverb=0.3)
KOTO = S.track("琴", "koto", volume=0.11, pan=0.3, reverb=0.35, sustain=1.2)
KAL = S.track("カリンバ（光のつぶ）", "kalimba", volume=0.08, pan=0.45, reverb=0.35, sustain=1.0)
CHIME = [S.track(f"風鈴の和音（グロッケン）{i + 1}", "glockenspiel", patch="glockenspiel", volume=0.045, pan=-0.4 + 0.4 * i, reverb=0.5) for i in range(3)]
ROLL = S.track("ビー玉がころがる（木琴）", "xylophone", volume=0.07, pan=-0.2, reverb=0.3)
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.09, pan=-0.1, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 2}]) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.055, pan=-0.3 + 0.3 * i, reverb=0.45, sustain=1.5) for i in range(3)]
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.19))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5:0.5 1':0.5 3':2", "2':1 7:1 5:1.5 R:0.5", "R:1 6:0.5 1':0.5 3':2", "2':1 1':1 6:1.5 R:0.5",
      "R:1 6:0.5 1':0.5 4':2", "3':1 2':1 7:1.5 R:0.5", "R:1 5:0.5 7:0.5 2':2", "7:3 R:1"]
A1 = "そぼのいえの/えんがわでね/びーだまをね/のぞいた/あおいなかに/ゆれていたの/きょねんのなつ/いとこと"
A2 = "すいかのたね/とばしたにわ/せみのこえと/ゆかたで/おばあちゃんが/うちわあおぐ/ことしはもう/いないの"
VB = ["R:0.5 3':0.5 3':0.5 4':0.5 5':1 3':1", "2':1.5 1':0.5 2':1 R:1", "R:0.5 2':0.5 2':0.5 3':0.5 5':1 4':1", "3':1.5 2':0.5 7:1 R:1",
      "R:0.5 3':0.5 3':0.5 4':0.5 5':1 6':1", "5':1.5 4':0.5 3':1 R:1", "R:0.5 4':0.5 5':0.5 6':0.5 1'':1 7':1", "6':2 R:2"]
B1 = "めをほそめたらね/なつがきこえたの/せみとふうりんと/わらうこえも"
B2 = "ころがるびーだま/まだとまらないで/もうすこしだけね/みていたいの"
VC = ["R:0.5 5':0.5 1'':1 7':1 5':1", "6':1.5 5':0.5 3':1 R:1", "R:0.5 3':0.5 7':1 5':1 3':1", "6':1.5 5':0.5 3':1 R:1",
      "R:0.5 4':0.5 6':1 5':1 4':1", "3':1.5 2':0.5 2':1 R:1", "R:0.5 3':0.5 5':0.5 6':0.5 7':1 6':1", "5':2 R:2"]
VC2 = VC[:6] + ["R:0.5 3':0.5 5':0.5 6':0.5 5':1 3':1", "1':2 R:2"]
C1 = "びーだまのなか/なつがゆれてる/あのひのそらは/みずいろだね/びーだまのなか/みんながいるよ/なくさないよう/にぎりしめる"
C2 = "びーだまのなか/ひかるおがわも/ゆうだちのあと/にじのはしも/びーだまのなか/ひるねのいぬも/ぜんぶそのまま/きえないでね"
CL = "びーだまのなか/なつがつづくよ/らいねんもまた/ここにくるね/びーだまのなか/そぼのえがおが/わらっているから/わすれないよ"
CO = "びーだまのなか/しずかなかぜが/ふうりんならす/ちりんちりん"
LY = Lyrics(S)


def put(name, lines, text):
    bars = S.sc(name); mel = [K.mel(x, oct=3) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1); put("Bメロ2", VB, B2)
put("サビ1", VC + VC2, C1); put("サビ2", VC + VC2, C2); put("最後のサビ", VC + VC2, CL)
put("落ちサビ", VC, CO)
if VOCAL: put("Aメロ2", VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: KOTO.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= 風鈴の和音（高いグロッケンの3つの音を、和音の音で、少しずつずらして） =================
rnd = random.Random(1313)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    t = tones(S.chords[b], "G#5", "E7")
    if n in ("ビー玉", "風鈴だけ", "ビー玉が止まる") or (n.startswith(("サビ", "最後")) and i % 2 == 1) or (n.startswith("Aメロ") and i % 4 == 3):
        for j in range(3):
            st = rnd.choice([0, 0.25, 0.5, 1.5, 2, 2.75])
            CHIME[j].at(S.bar_beat(b) + st, f"{nm(rnd.choice(t))}:2")

# ================= マリンバ・琴・カリンバ・ピアノ・ストリングス =================
KOTOS = ["B4:0.5 E5:0.5 F#5:1 G#5:0.5 F#5:0.5 E5:1", "C#5:0.5 E5:0.5 G#5:2 R:1", "A4:0.5 C#5:0.5 E5:1 F#5:0.5 E5:0.5 C#5:1", "B4:3 R:1",
         "F#4:0.5 A4:0.5 C#5:1 E5:0.5 C#5:0.5 B4:1", "D#5:1.5 C#5:0.5 B4:2", "G#4:0.5 B4:0.5 E5:1 F#5:0.5 G#5:0.5 B5:1", "A5:2 F#5:2"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; t = tones(ch, "E4", "E6"); v = voice(ch, 64, 3)
    if n == "ビー玉" and i < 2: continue
    if n in ("Aメロ1", "Aメロ2", "ソロ", "ビー玉") or n.startswith(("サビ", "最後")):
        if not (n == "Aメロ2" and not VOCAL and i < 8):
            MAR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 2)))
    if n == "ソロ": KOTO.bar(b, KOTOS[i])
    if n.startswith(("サビ", "最後")) and i % 2 == 0: KAL.bar(b, "R:2 " + " ".join(f"{nm(x + 12)}:0.5" for x in t[2:6]))
    if n in ("Bメロ1", "Bメロ2", "落ちサビ") or n.startswith(("サビ", "最後")):
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2" if not n.startswith("Bメロ") else f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1")
    if n.startswith(("サビ", "最後")) or n in ("Bメロ2", "ソロ"):
        sv = voice(ch, 60, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if n == "ビー玉が止まる":
        if i < 6:
            for j in range(3): PN[j].bar(b, f"{nm(v[j])}:4")
        elif i == 6:
            for j in range(3): STR[j].bar(b, f"{nm(voice(ch, 60, 3)[j])}:8")
            KAL.bar(b, " ".join(f"{nm(x)}:0.5" for x in t[:4]) + f" {nm(t[4 % len(t)])}:2")

# ================= ビー玉がころがる（木琴の細かい下がり。止まるときはゆっくりになる） =================
ROLL.bar(S.sc("ビー玉")[0], " ".join(f"{nm(x)}:0.125" for x in range(88, 72, -1)) + " R:2")
ROLL.bar(S.sc("ビー玉")[1], "R:1 " + " ".join(f"{nm(x)}:0.125" for x in range(86, 74, -1)) + " R:1.5")
ROLL.bar(S.sc("Aメロ2")[0] - 1, "R:2 " + " ".join(f"{nm(x)}:0.125" for x in range(86, 78, -1)) + " R:1")
bs = S.sc("ビー玉が止まる")
ROLL.bar(bs[6], "R:2 E6:0.25 D#6:0.25 C#6:0.5 B5:0.5 G#5:0.5")
ROLL.bar(bs[7], "E5:1 R:0.5 E5:2.5")                                     # 最後に1つ、こつん（止まる）

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ビー玉" and i >= 4: BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2", "ソロ"): BASS.bar(b, bass_line(S, b, "push" if n == "ソロ" else "root8", lo="E1"))
    elif n.startswith(("サビ", "最後")): BASS.bar(b, bass_line(S, b, "push" if i % 2 else "half", lo="E1"))
    elif n == "落ちサビ" and i >= 4: BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n == "ビー玉が止まる" and i < 7: BASS.bar(b, bass_line(S, b, "long", lo="E1"))

# ================= 季節の音: 蝉と風鈴 =================
season(S, S.sc("ビー玉")[0], "蝉", beats=32, vol=0.05, every=16)
season(S, S.sc("ビー玉")[2], "風鈴", beats=24, vol=0.06, every=8)
season(S, S.sc("風鈴だけ")[0], "風鈴", beats=24, vol=0.07, every=8)
season(S, S.sc("ビー玉が止まる")[4], "夕方の蝉", beats=16, vol=0.05, every=16)
cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "C4")

# ================= ドラム（IDM のブレイク: 細かいゴーストと、ずれたキック） =================
IDM = [("X.....x..X......", "....X..o.o..X..o", "x.xox.x.xxx.x.xo"), ("X..x......X.x...", "....X.o....oX.oo", "xx.x.x.xx.x.x.x.")]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ビー玉":
        if i >= 4: vgroove(D, b, "none", ghosts=0, seed=b, k="X.........X.....", s="................", h="x...x...x...x...", vary=False)
        if i == 7: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        kk, ss, hh = IDM[i % 2]
        vgroove(D, b, "none", ghosts=0.3, seed=b, k=kk, s=ss if i >= 4 else "....X.......X...", h=hh, vary=False)
        if i == 0: crash(D, b, "C2", 3)
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
    elif n.startswith(("サビ", "最後")):
        kk, ss, hh = IDM[i % 2]
        vgroove(D, b, "none", ghosts=0.35, seed=b, k=kk, s=ss, h="x.x.x.x.x.x.x.x.", vary=True)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
    elif n == "ソロ":
        kk, ss, hh = IDM[(i + 1) % 2]
        vgroove(D, b, "none", ghosts=0.4, seed=b, k=kk, s=ss, h=hh, vary=False)
        if last: put_fill(D, b, "lift")
    elif n == "落ちサビ":
        if i >= 4: D.set(b, "X.........X.....", "................", "x...x...x...x...")
    elif n == "ビー玉が止まる":
        if i < 4: vgroove(D, b, "none", ghosts=0.2, seed=b, k="X.........X.....", s="....X.......X...", h="x.x.x.x.x.x.x.x.", vary=False)

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の13。エレクトロニカ（IDM・ブレイクビート×和の音）。E 長調・132、転調なし。"
          "祖母の家の縁側で、ビー玉の中に去年の夏を見る。ビー玉がころがる木琴の音・風鈴・蝉で始まり、風鈴の音がそのまま和音になるグロッケン、琴とマリンバのソロ、"
          "落ちサビは音がゆがんで逆さに、最後はビー玉が止まる「こつん」で終わる。自作")
finish(S, LY, V, 0, fx=[{"type": "reverse", "scene": "落ちサビ", "bars": [7, 8], "bpm": 132}],
       level={"verse": -0.35}, special={"落ちサビ": -0.5, "最後のサビ": 0.4})
