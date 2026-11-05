# vt3 04「新聞配達スプリンター」Newspaper Sprinter（仮）— スカパンク。196・4/4。B♭長調 → 最後のサビは +1（B）。
# 第3弾（0時〜24時の街）の 3時。表は docs/sound/vt3-plan.md。
# 物語: 午前3時。まだ真っ暗な町を、かごいっぱいの新聞をのせた自転車で走る「わたし」。だれも知らない、町でいちばんの早起き。
#   角の家では犬がほえ、坂の上には赤いポスト。信号はまだ眠っていて、黄色だけが点めつしている。
#   どこかの窓から、聞いたことのある鼻歌（1時のラジオの節）が聞こえた。最後の1軒を配り終えると、東の空がうす青くなる。
# 場面と強さ: ホーン（いきなりの一撃・強）→ イントロ（スカの裏打ち・中強）→ Aメロ1（スカ・中）→ Bメロ1（ためる）→ サビ1（パンク・強）
#   → 掛け声 → 間奏（ホーン隊の節）→ Aメロ2 → Bメロ2 → サビ2 → 掛け声 → トランペットのソロ → Cメロ（信号待ち・ハーフ・弱）
#   → 最後のサビ（+1・いちばん強い）→ 掛け声 → 自転車のベル
# 旋律の性格: 裏打ちに乗る短い句（4分と8分）、Bメロは1段ずつ上がる呼びかけ、サビは4分で駆けるパンクの節。B♭3〜E♭5。
# この曲だけの音: Aメロはスカの裏打ち（ギターとオルガンが拍の裏だけ）、サビで一気にパンクの8分の刻みへ切りかわる。最後は自転車のベル。
#   合いことばの節（3・5・6・5・2）は、間奏でホーン隊が速く吹く。
from vt25_lib import *

S = Song("04", "paperboy", "新聞配達スプリンター（仮）", "Newspaper Sprinter", 196, 4, "Bb", "major", "スカパンク（ボカロ）")
S.kit = "naked-x"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --space room --space-wet 0.1"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.55
S.drum_scale = 0.85
S.keepers = {"Aメロ1": "closed", "Aメロ2": "ride", "サビ2": "open", "最後のサビ": "open"}
K = Key("Bb", "major")          # oct 3 で 1 = B♭3
KL = Key("B", "major")          # 最後のサビ（+1）

INTRO = ["Bb", "Gm7", "Eb", "F7"]
A_CH = ["Bb", "Bb", "Gm7", "Gm7", "Eb", "F", "Bb", "F7"]
B_CH = ["Eb", "F", "Dm7", "Gm7", "Eb", "F", "Cm7", "F7sus4"]
C_CH = ["Bb", "F/A", "Gm7", "Eb", "Bb", "F/A", "Eb", "F", "Gm7", "Dm7", "Eb", "Bb", "Cm7", "F/A", "Eb", "F7"]
CHANT = ["Eb", "F", "Dm7", "Gm7", "Eb", "F", "Bb", "Bb"]
LAST = [tr_chord(c, 1) for c in C_CH]

S.scene("ホーン", 4, "intro", ["Bb", "Bb", "Eb", "F7"])
S.scene("イントロ", 20, "intro", INTRO)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("掛け声1", 8, "break", CHANT)
S.scene("間奏", 8, "break", INTRO)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("掛け声2", 8, "break", CHANT)
S.scene("トランペットのソロ", 16, "solo", INTRO)
S.scene("Cメロ", 16, "bridge", ["Gm7", "Eb", "Bb", "F", "Gm7", "Eb", "Cm7", "F", "Gm7", "Eb", "Bb", "F", "Gm7", "Eb", "Cm7", "F#7"])    # 最後の小節は B への入り口
S.scene("最後のサビ", 24, "chorus", LAST + LAST[:8])
S.scene("掛け声3", 8, "break", [tr_chord(c, 1) for c in CHANT])
S.scene("ベル", 6, "outro", ["E", "F#", "G#m7", "E", "B", "B"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="trumpet", low=False)
SKA = [S.track(f"スカのギター{i + 1}", "guitar", amp="jpopClean", volume=0.05, pan=-0.5, reverb=0.12, chorus=0, sustain=0.25) for i in range(3)]
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.045, pan=0.5, reverb=0.2, sustain=0.3) for i in range(3)]
GL = [S.track(f"Lギター（刻み{i + 1}）", "distGuitar", **rock_gtr_spec(0.045, -0.55, drive=0.5)) for i in range(3)]
GR = [S.track(f"Rギター（刻み{i + 1}）", "distGuitar", **rock_gtr_spec(0.042, 0.55, drive=0.5)) for i in range(3)]
TP = S.track("トランペット", "brass", patch="trumpet", volume=0.11, pan=0.15, reverb=0.25)
TB = S.track("トロンボーン", "brass", patch="trombone", volume=0.1, pan=-0.15, reverb=0.25)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.23))
BELL = S.track("自転車のベル", "bell", volume=0.07, pan=0.3, reverb=0.25)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "2:0.5 3:0.5 5:1 R:2", "R:1 5:0.5 5:0.5 6:0.5 5:0.5 1':1", "7:0.5 6:0.5 5:1 R:2",
      "R:1 6:0.5 6:0.5 1':0.5 6:0.5 5:1", "3:0.5 2:0.5 3:1 R:2", "R:1 2:0.5 3:0.5 5:0.5 3:0.5 2:1", "1:2 R:2"]
A1 = ("くらいまちかどを/じてんしゃでかける/かごいっぱいのあさ/ずっしりおもい/"
      "いっけんめはかどの/いぬがほえるいえ/さかのうえのいえ/あかいぽすと")
A2 = ("だれもしらないの/わたしのはやおき/さんじのまちかど/いちばんのり/"
      "ぺだるをふみこむ/しろいいきがでる/どこかのまどから/きいたふしだ")
VB = ["R:1 3:1 4:1 5:1", "6:1 5:1 4:1 R:1", "R:1 4:1 5:1 6:1", "7:1 6:1 5:1 R:1",
      "R:1 5:1 6:1 7:1", "1':1 7:1 6:1 R:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 3':1", "2':3 R:1"]
B1 = "みてないけど/まちはまってる/けさのしらせ/とどけにいくよ"
B2 = "ねむるまどべ/おきるまえに/ぽすとのなか/あさをいれとく"
VC = ["1':1 1':1 7:1 6:1", "5:2 6:1 R:1", "5:1 5:1 6:1 5:1", "3:2 R:2",
      "4:1 4:1 5:1 6:1", "7:2 6:1 R:1", "5:1 6:1 7:1 1':1", "2':3 R:1",
      "3':1 3':1 2':1 1':1", "2':2 1':1 R:1", "6:1 6:1 7:1 1':1", "5:2 R:2",
      "4':1 3':1 2':1 1':1", "7:2 1':1 R:1", "2':1 1':1 7:1 6:1", "1':3 R:1"]
C1 = "はしれはしれ/よあけまえ/さかをくだれ/かぜになれ/だれよりさき/まちのあさ/ひとつひとつ/くばるんだ"
C2 = "はしれはしれ/しんごうも/まだねむってる/きいろだけ/てんめつして/わたしだけ/みちをてらす/あおになれ"
C3 = ("はしれはしれ/よがあける/さいごのいえ/のこりいち/あさひのぼる/まちおきる/かごはからっぽ/ただいまだ/"
      "はしれはしれ/あしたもね/しらなくても/あさはくる")
VCH = ["5:1 5:1 6:1 5:1", "3:2 R:2", "6:1 6:1 1':1 6:1", "5:2 R:2", "5:1 5:1 6:1 5:1", "3:2 R:2", "2:1 3:1 5:1 3:1", "1:2 R:2"]
CH = "おーおーお/おーおーお/とどけるよ/まちじゅうへ"
VBR = ["R:1 3:1 5:1 6:1", "5:2 3:1 R:1", "R:1 3:1 5:1 1':1", "7:2 6:1 R:1",
       "R:1 6:1 6:1 5:1", "3:2 2:1 R:1", "R:1 2:1 3:1 5:1", "5:3 R:1"]
CB = "とまるあし/そらをみる/ひがしがわ/うすあお/みちのさき/とりがなく/もうすこし/あといち"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("掛け声1", K, VCH, CH)
put("Aメロ2", K, VA + VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
put("掛け声2", K, VCH, CH)
put("Cメロ", K, VBR + VBR, CB)
put("最後のサビ", KL, VC + VC[:8], C3)
put("掛け声3", KL, VCH, CH)

# ================= 和音の楽器 =================
def skank(b, ch, tracks, center=64, every="R:0.5 x:0.5"):
    v = voice(ch, center, 3)
    for j in range(3): tracks[j].bar(b, " ".join([every.replace("x", nm(v[j]))] * 4))


def punk8(b, ch, accent_last=False):
    """パンクの8分の刻み（ジャジャジャジャ）。左は根音・5度・オクターブ（E2〜C3あたり）、右は C3〜B4 の中の和音"""
    pw = power(ch, "E2")
    r = low(ch, "C3"); up = [x for x in tones(ch, nm(r + 1), nm(r + 12))][:2]
    while len(up) < 2: up.append(r + 12)
    rv = [r] + up
    for j in range(3):
        GL[j].bar(b, " ".join(f"{nm(pw[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))
        GR[j].bar(b, " ".join(f"{nm(rv[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))


def horn_hit(b, ch, pat):
    v = voice(ch, 65, 2)
    TP.bar(b, pat.replace("x", nm(v[1]))); TB.bar(b, pat.replace("x", nm(v[0] - 12 if v[0] > 60 else v[0])))


RIFF = ["F4:0.5 D4:0.5 F4:0.5 G4:0.5 Bb4:1 R:1", "A4:0.5 G4:0.5 F4:0.5 D4:0.5 F4:1 R:1",
        "G4:0.5 F4:0.5 G4:0.5 A4:0.5 Bb4:0.5 C5:0.5 D5:1", "C5:1 A4:1 F4:1 R:1"]
MOTIF = ["R:2 D5:0.5 F5:0.5 G5:0.5 F5:0.5", "C5:1 R:3"]           # 合いことばの節（3・5・6・5・2）を速く
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "ホーン":
        horn_hit(b, ch, ["x:0.5! R:0.5 x:0.5! R:2.5", "x:0.5! R:0.5 x:0.5! R:0.5 x:2", "R:4", "x:0.5 x:0.5 x:0.5 x:0.5 x:2"][i])
        punk8(b, ch) if i >= 2 else None
    elif n in ("イントロ", "間奏"):
        skank(b, ch, SKA); skank(b, ch, ORG, 60)
        TP.bar(b, RIFF[i % 4]); TB.bar(b, shift_oct(RIFF[i % 4], -1))
        if n == "間奏" and i in (4, 5): TP.bar(b, MOTIF[i - 4]); TB.bar(b, shift_oct(MOTIF[i - 4], -1))
    elif n in ("Aメロ1", "Aメロ2"):
        skank(b, ch, SKA)
        if n == "Aメロ2" or i >= 8: skank(b, ch, ORG, 60)
        if i % 8 == 7: horn_hit(b, ch, "R:2.5 x:0.5 x:0.5 x:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        skank(b, ch, ORG, 62, "R:0.5 x:0.25 x:0.25")
        punk8(b, ch) if i >= 4 else skank(b, ch, SKA)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        punk8(b, ch)
        if i % 4 == 3: horn_hit(b, ch, "R:1 x:0.5 x:0.5 x:1 R:1")
        if i % 8 == 0: skank(b, ch, ORG, 62, "x:1")
    elif n in ("掛け声1", "掛け声2", "掛け声3"):
        punk8(b, ch); skank(b, ch, ORG, 62, "R:0.5 x:0.5")
        horn_hit(b, ch, "x:1 R:1 x:1 R:1" if i % 2 == 0 else "x:2 R:2")
    elif n == "トランペットのソロ":
        skank(b, ch, SKA); skank(b, ch, ORG, 60)
        SOLO = ["R:1 F4:0.5 G4:0.5 Bb4:1 D5:1", "C5:0.5 Bb4:0.5 G4:1 F4:2", "R:1 Eb5:0.5 D5:0.5 C5:1 Bb4:1", "A4:1 C5:1 F5:2",
                "R:0.5 F5:0.5 F5:0.5 Eb5:0.5 D5:1 Bb4:1", "C5:1 D5:0.5 C5:0.5 Bb4:1 G4:1", "R:0.5 Bb4:0.5 C5:0.5 D5:0.5 Eb5:1 G5:1", "F5:3 R:1",
                "D5:0.5 F5:0.5 D5:0.5 Bb4:0.5 D5:0.5 F5:0.5 Bb5:1", "A5:1 G5:1 F5:2", "Eb5:0.5 G5:0.5 Eb5:0.5 C5:0.5 Eb5:0.5 G5:0.5 C6:1", "Bb5:1 A5:1 F5:2",
                "G5:1 F5:1 D5:1 Bb4:1", "C5:1 Eb5:1 G5:1 A5:1", "Bb5:0.5 A5:0.5 G5:0.5 F5:0.5 D5:1 C5:1", "Bb4:3 R:1"]
        TP.bar(b, SOLO[i])
        if i >= 8: punk8(b, ch)
    elif n == "Cメロ":
        skank(b, ch, ORG, 60, "x:2 R:2" if i < 8 else "R:0.5 x:0.5")
        if i >= 14: punk8(b, ch)
    elif n == "ベル":
        if i < 5: horn_hit(b, ch, "x:4" if i < 4 else "x:0.5! R:3.5"); punk8(b, ch) if i < 4 else None
        BELL.bar(b, ["R:4", "R:4", "R:4", "R:4", "R:2 E6:0.25 R:0.25 E6:0.25 R:1.25", "E6:0.25 R:0.25 E6:0.25 R:3.25"][i])

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("イントロ", "間奏", "Aメロ1", "Aメロ2", "トランペットのソロ"):
        BASS.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1 {nm(r + 12)}:1 {nm(r + 7)}:0.5 {nm(r + 4 if 'm' not in ch.split('/')[0] else r + 3)}:0.5" if i % 2 == 0 else bass_line(S, b, "walk", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n in ("サビ1", "サビ2", "最後のサビ", "掛け声1", "掛け声2", "掛け声3", "ホーン"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n == "Cメロ": BASS.bar(b, f"{nm(r)}:2 R:2" if i < 8 else (f"{nm(r)}:1 R:1 {nm(r)}:1 R:1" if i < 14 else bass_line(S, b, "root8", lo="E1")))
    elif n == "ベル" and i < 4: BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n == "ベル" and i == 4: BASS.bar(b, f"{nm(r)}:0.5 R:3.5")

riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("最後のサビ")[0], 4, "C4")
cym_swell(CYM, S.sc("サビ2")[0], 2, "C4")

# ================= ドラム =================
SKA_K, SKA_S, SKA_H = "X.......X.......", "....X.......X...", "..x...x...x...x."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ホーン":
        if i < 2: D.set(b, "X.......X.......", "X.......X.......", "................")
        else: vgroove(D, b, "punk", ghosts=0.1, seed=b)
        if i == 0: crash(D, b)
        if i == 3: put_fill(D, b, "snare16")
    elif n in ("イントロ", "間奏", "Aメロ1", "Aメロ2", "トランペットのソロ"):
        if n == "トランペットのソロ" and i >= 8: vgroove(D, b, "punk", ghosts=0.15, seed=b)
        else: vgroove(D, b, "beat8", ghosts=0.35, seed=b, k=SKA_K, s=SKA_S, h=SKA_H)
        if i == 0 and n != "Aメロ1": crash(D, b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.......X.X.....", s=SKA_S, h="x.x.x.x.x.x.x.x.") if i < 4 else vgroove(D, b, "punk", ghosts=0.15, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ", "掛け声1", "掛け声2", "掛け声3"):
        vgroove(D, b, "punk" if "掛け声" not in n else "vrock", ghosts=0.15, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        if last and n != "掛け声3": put_fill(D, b, "snare16")
    elif n == "Cメロ":
        if i < 14: vgroove(D, b, "half", ghosts=0.2, seed=b)
        elif i == 14: put_fill(D, b, "build")
        else: D.set(b, "X.X.X.X.X.X.X.X.", "....X...XXXXXXXX", "................")
    elif n == "ベル":
        if i < 3: vgroove(D, b, "punk", ghosts=0.15, seed=b)
        if i == 0: crash(D, b, "C2", 6)
        elif i == 3: D.set(b, "X.......X.......", "....X...X.X.XXXX", "x.x.x.x.........")
        elif i == 4: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)

SIL.add(S.sc("Bメロ1")[-1], 1, 4); SIL.add(S.sc("Bメロ2")[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の04（3時）。スカパンク。B♭・196、最後のサビは +1（B）。まだ暗い町で、自転車で新聞を配る。"
          "Aメロはスカの裏打ち（ギター・オルガン）、サビはパンクの8分の刻み。トランペット・トロンボーン。合いことばの節は間奏のホーン隊。自転車のベルで終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"Cメロ": -0.5, "最後のサビ": 0.4, "ベル": 0.0})
