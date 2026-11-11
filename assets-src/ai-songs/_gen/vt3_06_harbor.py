# vt3 06「朝焼け漁港」Dawn at the Fishing Port（仮）— 和ロック。166・4/4。E短調（民謡ふうのペンタトニック）→ 最後のサビは +2（F#m）。
# 書き出しは全体を2半音下げる（テトの声に入れるため。鳴るのは D短調 → 最後のサビは E短調）。
# 第3弾（0時〜24時の街）の 5時。表は docs/sound/vt3-plan.md。
# 物語: 朝焼けの港。じいちゃんの漁船に、はじめて乗せてもらう孫の「わたし」。エンジンの音が胸にひびき、かもめが鳴く。
#   沖へ出て、重い網をいっしょに引く。網の中で銀色の魚がはねる。じいちゃんがふいに口ずさんだのは、夜のラジオで聞いたという鼻歌。
#   わたしもまねして歌いながら、船いっぱいの魚をのせて港へ帰る。いつかこの船を、わたしが動かす。
# 場面と強さ: 太鼓（大きな一打・強）→ イントロ（三味線のリフとバンド）→ Aメロ1（太く語る・中）→ Bメロ1（沖へ・ためる）→ サビ1（網を引く・強）
#   → 掛け声（三味線とバンド）→ 間奏 → Aメロ2 → Bメロ2 → サビ2 → 太鼓のソロ → 波（波の音と尺八だけ・とても弱い）
#   → 最後のサビ（+2・いちばん強い）→ 汽笛
# 旋律の性格: 民謡ふうの5音（ミ・ソ・ラ・シ・レ）、句の終わりに小さなこぶし（16分の回し）。サビは長くのばす太い節。
# この曲だけの音: 和太鼓の大きな一打とソロ、三味線の速いリフ、尺八。サビの「そーれ」の掛け声。
#   合いことばの節（3・5・6・5・2）は、「波」の場面で尺八が吹く（G長調として B・D・E・D・A）。
from vt25_lib import *

S = Song("06", "harbor", "朝焼け漁港（仮）", "Dawn at the Fishing Port", 166, 4, "E", "minor", "和ロック（ボカロ）")
S.kit = "naked-x"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --space hall --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.55
S.drum_scale = 0.85
S.keepers = {"Aメロ2": "ride", "サビ2": "open", "最後のサビ": "open"}
K = Key("E", "minor")           # oct 4 で 1 = E4
KL = Key("F#", "minor")         # 最後のサビ（+2）

INTRO = ["Em", "Em", "C", "D"]
A_CH = ["Em", "Em", "Am7", "Em", "C", "D", "Em", "Em"]
B_CH = ["Am7", "Bm7", "C", "D", "Am7", "Bm7", "C", "B7"]
C_CH = ["Em", "D", "C", "D", "Em", "D", "C", "B7", "Em", "D", "C", "G", "Am7", "Bm7", "C", "B7"]
CALL = ["Em", "D", "C", "B7"]
LAST = [tr_chord(c, 2) for c in C_CH]

S.scene("太鼓", 4, "intro", ["Em", "Em", "Em", "Em"])
S.scene("イントロ", 16, "intro", INTRO)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("掛け声", 8, "break", CALL)
S.scene("間奏", 12, "break", INTRO)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("太鼓のソロ", 8, "solo", ["Em", "Em", "Em", "Em", "Em", "Em", "Em", "B7"])
S.scene("波", 8, "bridge", ["Em", "C", "G", "D", "Em", "C", "Am7", "C#7"])    # 最後の小節は F#m への入り口
S.scene("最後のサビ", 24, "chorus", LAST + LAST[:8])
S.scene("汽笛", 10, "outro", ["F#m", "E", "D", "E", "F#m", "E", "D", "C#7", "F#m", "F#m"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞる音は、フルートの音をやめて高さの揺れない電子の音に
SHAM = S.track("三味線（リフ）", "shamisen", volume=0.13, pan=0.25, reverb=0.2)
SHK = S.track("尺八", "shakuhachi", volume=0.12, pan=-0.1, reverb=0.45)
KOTO = S.track("琴（アルペジオ）", "koto", volume=0.08, pan=-0.45, reverb=0.3)
TAI = S.track("和太鼓", "inchTom", volume=0.16, pan=0, reverb=0.35)
GL = [S.track(f"Lギター（刻み{i + 1}）", "distGuitar", **rock_gtr_spec(0.042, -0.55, drive=0.5)) for i in range(3)]
GR = [S.track(f"Rギター（刻み{i + 1}）", "distGuitar", **rock_gtr_spec(0.04, 0.55, drive=0.5)) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.045, pan=-0.5 + 0.5 * i, reverb=0.4, sustain=1.4) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.23))
HORN = S.track("汽笛（低い金管）", "brass", patch="tuba", volume=0.09, pan=0, reverb=0.5)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5,:0.5 7,:0.5 1:1 1:1", "3:0.5 1:0.5 7,:1 1:1 R:1", "R:1 1:0.5 3:0.5 4:1 4:1", "5:0.5 4:0.5 3:1 4:1 R:1",
      "R:1 5:0.5 7:0.5 5:1 4:1", "3:0.5 4:0.5 3:0.5 1:0.5 3:1 R:1", "R:1 7,:0.5 1:0.5 3:0.5 1:0.5 7,:1", "1:3 R:1"]
A1 = ("ごじのあさやけに/ふねがめをさます/じいちゃんのふといて/なわをにぎる/"
      "はじめてのりこむ/ゆれるかんぱんで/しおのにおいがする/そらはあかい")
A2 = ("えんじんのおとが/むねにひびいてる/かもめがないている/みなとのそら/"
      "じいちゃんがふいに/はなうたをうたう/どこでおぼえたのか/よるのらじお")
VB = ["R:0.5 4:0.5 5:0.5 7:0.5 5:1 4:1", "3:2 1:1 R:1", "R:0.5 4:0.5 5:0.5 7:0.5 1':1 7:1", "5:2 4:1 R:1",
      "R:0.5 5:0.5 7:0.5 1':0.5 2':1 1':1", "7:2 5:1 R:1", "R:0.5 4:0.5 5:0.5 4:0.5 3:0.5 4:0.5 5:1", "5:3 R:1"]
B1 = "おきへおきへと/なみをこえてく/ちいさなからだ/ふんばるあしで"
B2 = "あみをなげれば/うみがひかるよ/うろこのぎんが/あさひにはねる"
VC = ["1':1.5 7:0.5 5:1 7:1", "1':2 R:2", "5:1.5 4:0.5 3:1 4:1", "5:2 R:2",
      "7:1.5 5:0.5 7:1 1':1", "2':1 1':0.5 7:0.5 1':1 R:1", "5:1 4:0.5 3:0.5 1:1 3:1", "4:3 R:1",
      "1':1.5 7:0.5 5:1 7:1", "1':1 2':1 1':1 R:1", "5:1.5 7:0.5 1':1 2':1", "2':2 R:2",
      "1':1 7:0.5 5:0.5 4:1 5:1", "7:2 5:1 R:1", "4:1 3:0.5 1:0.5 3:1 4:1", "1:3 R:1"]
C1 = "そーれひけ/あさのうみ/おもいあみをひけ/そらがもえる/じいちゃんのよこ/わたしもね/うみのこになる/そーれそーれ"
C2 = "そーれひけ/なみのうえ/ぎんいろがはねる/あみのなかで/ちいさなてにも/まめひとつ/きょうのしょうこだ/そーれそーれ"
C3 = ("そーれひけ/みなとまで/ふねいっぱいのせて/かえりみちだ/あのはなうたを/わたしもね/まねしてうたう/そーれそーれ/"
      "そーれひけ/あさのうみ/いつかこのふねを/うごかすんだ")
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA + VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
put("最後のサビ", KL, VC + VC[:8], C3)

# ================= 和楽器・ギター =================
def gtr8(b, ch, n=3):
    pw = power(ch, "E2")
    r = low(ch, "C3"); up = [x for x in tones(ch, nm(r + 1), nm(r + 12))][:2]
    while len(up) < 2: up.append(r + 12)
    rv = [r] + up
    for j in range(n):
        GL[j].bar(b, " ".join(f"{nm(pw[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))
        GR[j].bar(b, " ".join(f"{nm(rv[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))


def strings(b, ch, c=67):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


SHRIFF = ["E4:0.25 E4:0.25 G4:0.5 A4:0.5 B4:0.25 A4:0.25 G4:0.5 E4:0.5 D4:0.5 E4:0.5",
          "E4:0.25 E4:0.25 G4:0.5 A4:0.5 B4:0.5 D5:0.5 B4:0.5 A4:0.5 G4:0.5",
          "E5:0.5 D5:0.25 B4:0.25 A4:0.5 G4:0.5 A4:0.25 G4:0.25 E4:0.5 D4:0.5 E4:0.5",
          "D4:0.5 E4:0.5 G4:0.5 A4:0.5 B4:1 R:1"]
MOTIF = "R:1 B4:0.5 D5:0.5 E5:1 D5:0.5 A4:0.5"   # 合いことばの節（G長調で 3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        SHAM.bar(b, SHRIFF[i % 4])
        if i >= 4: gtr8(b, ch)
        if i in (8, 12): SHK.bar(b, "E5:2 D5:1 B4:1")
        if i in (9, 13): SHK.bar(b, "A4:3 R:1")
    elif n in ("Aメロ1", "Aメロ2"):
        t = tones(ch, "E4", "E5")
        KOTO.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 1, 0, 2)))
        if n == "Aメロ2" or i >= 8: gtr8(b, ch, 2)
        if i % 4 == 3: SHAM.bar(b, "R:2 E4:0.25 G4:0.25 A4:0.5 B4:0.5 A4:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        gtr8(b, ch); strings(b, ch, 64)
        if i % 2 == 1: SHAM.bar(b, "R:2.5 B4:0.25 A4:0.25 G4:0.5 E4:0.5")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        gtr8(b, ch); strings(b, ch, 70)
        if i % 4 == 3: SHAM.bar(b, "R:2 E5:0.25 D5:0.25 B4:0.5 A4:0.5 G4:0.5")
    elif n in ("掛け声", "間奏"):
        gtr8(b, ch); SHAM.bar(b, SHRIFF[i % 4])
        if n == "間奏" and i >= 4:
            SOLO = ["E5:1 D5:0.5 B4:0.5 A4:1 B4:1", "D5:2 B4:1 A4:1", "G4:1 A4:1 B4:0.5 D5:0.5 E5:1", "D5:3 R:1",
                    "B4:1 D5:1 E5:1 G5:1", "E5:1.5 D5:0.5 B4:1 A4:1", "G4:1 E4:1 G4:1 A4:1", "B4:3 R:1"]
            SHK.bar(b, SOLO[i - 4])
    elif n == "太鼓のソロ":
        if i == 7: gtr8(b, ch)
    elif n == "波":
        strings(b, ch, 62)
        SHK.bar(b, MOTIF if i == 1 else ("R:1 E5:2 D5:1" if i == 4 else ("B4:3 R:1" if i == 5 else "R:4")))
        if i >= 6: gtr8(b, ch, 1)
    elif n == "汽笛":
        if i < 8: gtr8(b, ch); strings(b, ch, 66)
        if i < 8 and i % 4 == 3: SHAM.bar(b, "R:2 F#4:0.25 A4:0.25 B4:0.5 C#5:0.5 B4:0.5")
        if i == 8: strings(b, ch, 66)
        HORN.bar(b, "F#2:4" if i == 8 else ("R:4" if i < 9 else "F#2:3 R:1"))

# ================= 和太鼓 =================
TAI.bar(S.sc("太鼓")[0], "F1:4"); TAI.bar(S.sc("太鼓")[1], "R:2 F1:2")
TAI.bar(S.sc("太鼓")[2], "F1:1 F1:1 A1:0.5 A1:0.5 F1:1"); TAI.bar(S.sc("太鼓")[3], "A1:0.5 A1:0.5 F1:0.5 F1:0.5 F1:2")
TSOLO = ["F1:1 A1:0.5 A1:0.5 F1:1 A1:1", "F1:0.5 F1:0.5 A1:0.5 C2:0.5 A1:1 F1:1", "F1:1 R:0.5 F1:0.5 A1:0.5 A1:0.5 C2:1",
         "C2:0.25 C2:0.25 A1:0.25 A1:0.25 F1:0.5 F1:0.5 F1:2", "F1:1 A1:1 F1:1 A1:1", "F1:0.5 A1:0.5 C2:0.5 A1:0.5 F1:0.5 A1:0.5 C2:1",
         "F1:0.25 F1:0.25 F1:0.25 F1:0.25 A1:0.25 A1:0.25 A1:0.25 A1:0.25 C2:0.25 C2:0.25 C2:0.25 C2:0.25 F1:1", "F1:4"]
for i, b in enumerate(S.sc("太鼓のソロ")): TAI.bar(b, TSOLO[i])
for name in ("サビ1", "サビ2", "最後のサビ"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 0: TAI.bar(b, "F1:2 R:2")
TAI.bar(S.sc("汽笛")[8], "F1:4")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("イントロ", "掛け声", "間奏") and (n != "イントロ" or i >= 4): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 {nm(r + 7)}:1 {nm(r + 10)}:1")
    elif n in ("Bメロ1", "Bメロ2", "サビ1", "サビ2", "最後のサビ"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n == "波" and i >= 6: BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n == "汽笛" and i < 9: BASS.bar(b, bass_line(S, b, "root8" if i < 8 else "long", lo="E1"))

for name in ("サビ1", "最後のサビ"): cym_swell(CYM, S.sc(name)[0], 2, "C4")
season(S, S.sc("波")[0], "波", beats=32, vol=0.07, every=8)
season(S, S.sc("Aメロ2")[0], "波", beats=8, vol=0.05)

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "太鼓":
        if i == 0: crash(D, b, "C2", 6)
    elif n in ("イントロ", "掛け声", "間奏"):
        if n == "イントロ" and i < 4: continue
        vgroove(D, b, "vrock", ghosts=0.2, seed=b)
        if i % 8 == 4 or (n != "イントロ" and i == 0): crash(D, b)
        if last: put_fill(D, b, "tomdown")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b) if (n == "Aメロ2" or i >= 8) else D.set(b, "X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.25, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "vrock2", ghosts=0.2, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "太鼓のソロ":
        if i == 7: put_fill(D, b, "lift")
    elif n == "波":
        if i == 7: put_fill(D, b, "build")
    elif n == "汽笛":
        if i < 8: vgroove(D, b, "vrock", ghosts=0.2, seed=b)
        if i == 0: crash(D, b, "C2", 6)
        if i == 7: put_fill(D, b, "tomdown")
        if i == 8: crash(D, b, "C2", 8)

SIL.add(S.sc("Bメロ1")[-1], 1, 4); SIL.add(S.sc("Bメロ2")[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の06（5時）。和ロック。E短調（民謡ふうの5音）・166、最後のサビは +2。書き出しは全体を2半音下げる。"
          "朝焼けの港で、じいちゃんの漁船にはじめて乗る孫。和太鼓・三味線・尺八・琴とバンド。合いことばの節は「波」の尺八。汽笛で終わる。自作")
finish(S, LY, V, -2,
       level={"verse": -0.15}, special={"波": -0.6, "最後のサビ": 0.4, "太鼓のソロ": 0.1})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午前5時・朝焼けの漁港・和ロック）で直すこと:
#   ギター: 全部同じ強さの8分をやめる。左＝下ろしで押す（1・3拍を強く、4小節ごとに後半をたたみかける）、右＝祭りばやしのような「タン・タタ」（8分＋16分2つ）の刻み。
#          刻みが終わる小節は最後を伸ばして止める。音色（TRiDENT の音）はそのまま
#   歌: Aメロ・Bメロ・サビはクリア（力強く）、掛け声はキュート、波（静かな所）はウィスパー。サビは句の頭をすくい、のばす音の後ろを揺らす（こぶしのかわり）。ハモリは サビ2 の後半と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
pl = restrum(path, S, "Lギター（刻み", -0.55, lambda n, i, end, b: "D.d.d.d.D.d.D---" if end else ("D.d.d.d.D.D.DDD." if i % 4 == 3 else "D.d.d.d.D.d.d.d."), seed=2)
pr = restrum(path, S, "Rギター（刻み", 0.55, lambda n, i, end, b: "D.ddD.d.D.d.D---" if end else ("D.ddD.ddD.D.DuDu" if i % 4 == 3 else ("D.ddD.ddD.ddD.d." if i % 2 == 0 else "D.d.D.ddD.d.D.dd")), seed=9)
add_parts(path, pl + pr, drop=lambda p: p.get("role", "").startswith("Lギター（刻み") and not p.get("notes", "").count("%") or p.get("role", "").startswith("Rギター（刻み") and not p.get("notes", "").count("%"))
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=4, minlen=0.75))
    vocal_polish(path, S, {"verse": 10, "pre": 16, "chorus": 26, "最後のサビ": 30, "bridge": 8, "break": 0, "outro": 0}, scoop=0.4, slash=0.9, vib_min_beats=1.5, vib_start=0.45, auto=0.5, breaths=0.5)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, KL)], vol=0.36, shift=-2)
    voice_by_scene(path, S, {"verse": "clear", "pre": "clear", "chorus": "clear", "break": "cute", "bridge": "whisper"}, default="clear")
