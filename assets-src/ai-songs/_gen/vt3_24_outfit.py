# vt3 24「明日の服がきまらない」Can't Pick Tomorrow's Outfit（仮）— フレンチポップ。132・4/4。G長調 → 最後のサビは +1（A♭）。 書き出しは全体を+1半音（A♭長調 → 最後は A）。
# 第3弾（0時〜24時の街）の 23時。表は docs/sound/vt3-plan.md。
# 物語: 初デートの前の夜。鏡の前で、服を何度も着がえる。しまのシャツは子どもっぽい、花がらのスカートは少しはでかな。
#   ふとんの上には服の山。時計の針は12時まえ。ベッドに倒れこんで天井を見る。でも、いちばん好きな服に決めた。目覚ましをかけて、おやすみ。
# 場面と強さ: チェンバロの前奏 → イントロ（ストリングスと口笛の節）→ Aメロ1（話すように・中弱）→ Bメロ1 → サビ1（中強）
#   → 間奏（口笛）→ Aメロ2 → Bメロ2 → サビ2 → ベッドに倒れこむ（チェンバロとストリングスだけ・静か）→ ブレイク（1拍止まる）
#   → 最後のサビ（+1・いちばん明るい）→ 目覚まし（目覚ましをかける音）
# 旋律の性格: 軽やかな、話すような節（A3〜D5）。Aメロは同じ音をくり返して話し、サビは5度から跳ねて上がる。
# この曲だけの音: チェンバロ・ストリングス・ウッドベース・ブラシ。口笛のかわりに高い縦笛（tinWhistle）。
#   合いことばの節（3・5・6・5・2＝B・D・E・D・A）は、口笛（イントロと間奏）。
from vt25_lib import *

S = Song("24", "outfit", "明日の服がきまらない（仮）", "Can't Pick Tomorrow's Outfit", 132, 4, "G", "major", "フレンチポップ（ボカロ）")
S.kit = "naked"
S.flags = "--bass rubner " + S.flags + " --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.35
S.drum_scale = 0.85
K = Key("G", "major")          # oct 3 で 1 = G3
KL = Key("Ab", "major")        # 最後のサビ（+1）

A_CH = ["Gmaj7", "Em7", "Am7", "D7", "Bm7", "E7", "Am7", "D7"]
B_CH = ["Cmaj7", "Bm7", "Am7", "D7", "Cmaj7", "Bm7", "Em7", "D7sus4"]
C_CH = ["Gmaj7", "B7", "Em7", "G7", "Cmaj7", "Cm6", "Am7", "D7"]
LAST = [tr_chord(c, 1) for c in C_CH]

S.scene("チェンバロの前奏", 4, "intro", ["Gmaj7", "Em7", "Am7", "D7"])
S.scene("イントロ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ベッドに倒れこむ", 8, "bridge", ["Cmaj7", "Bm7", "Am7", "Gmaj7", "Cmaj7", "Bm7", "Am7", "Eb7"])
S.scene("最後のサビ", 24, "chorus", LAST)
S.scene("目覚まし", 4, "outro", ["Abmaj7", "Fm7", "Bbm7", "Abmaj7"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)   # v2: フルートの音は使わない（人間・2026-11-11）→ 高さの揺れない電子の音に   # v2: BGM の旋律をシンセのはじく音からフルートに（生楽器の曲なのに1つだけ電子の音だった）
HL = S.track("チェンバロ（左手）", "harpsichord", volume=0.12, pan=-0.2, reverb=0.3)
HR = [S.track(f"チェンバロ（右手{j + 1}）", "harpsichord", volume=0.055, pan=0.15 + 0.05 * j, reverb=0.3) for j in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.4 + 0.4 * i, reverb=0.4, sustain=1.2) for i in range(3)]
PIZ = S.track("ピチカート", "strings", patch="pizzicatoStrings", volume=0.06, pan=0.35, reverb=0.3)
WH = S.track("口笛（高い縦笛）", "lead", patch="kfbSineLead", volume=0.07, pan=0.1, reverb=0.35)
BASS = S.track("ウッドベース", "bass", **finger_bass_spec(vol=0.24))
ALM = S.track("目覚まし", "glockenspiel", volume=0.05, pan=0.25, reverb=0.25)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 3:0.5 3:0.5 3:0.5 4:0.5 3:0.5 2:1", "5:1.5 R:2.5", "R:0.5 4:0.5 4:0.5 4:0.5 5:0.5 4:0.5 3:1", "6:1.5 R:2.5",
      "R:0.5 5:0.5 5:0.5 5:0.5 6:0.5 5:0.5 4:0.5 3:0.5", "2:1 3:1 R:2", "R:0.5 2:0.5 3:0.5 4:0.5 5:1 4:0.5 3:0.5", "2:2 R:2"]
A1 = ("あしたのごごに/きみにあうから/かがみのまえでまた/ふくをきがえる/"
      "しまのしゃつだと/こどもみたいで/はながらのすかあと/すこしはでかな")
A2 = ("あかいぼうしは/きどりすぎかな/おきにいりのくつは/あめでぬれそう/"
      "ふとんのうえに/ふくのやまがね/ひとつまたひとつと/たかくつもるよ")
VB = ["R:0.5 1':0.5 7:0.5 6:0.5 5:1 6:1", "7:1 1':1 R:2", "R:0.5 6:0.5 5:0.5 4:0.5 3:1 4:1", "5:2 R:2",
      "R:0.5 1':0.5 7:0.5 6:0.5 5:1 2':1", "1':1 7:1 R:2", "R:0.5 6:0.5 7:0.5 1':0.5 2':1 3':1", "2':2 R:2"]
B1 = "どれもすてきで/えらべないの/きみはどんなの/すきなのかな"
B2 = "とけいのはりは/じゅうにじまえ/はやくきめなきゃ/ねむれないよ"
VC = ["R:0.5 5:0.5 1':0.5 2':0.5 3':1 2':0.5 1':0.5", "2':1 5:1 R:2", "R:0.5 5:0.5 1':0.5 2':0.5 3':1 4':0.5 3':0.5", "2':2 R:2",
      "R:0.5 6:0.5 6:0.5 6:0.5 4':1 3':0.5 2':0.5", "1':1 6:1 R:2", "R:0.5 5:0.5 6:0.5 7:0.5 1':1 2':1", "1':2 R:2"]
C1 = ("あしたのわたしは/なにをきてくの/くるりとまわれば/きまらないの/"
      "かがみのむこうで/ほほえむわたし/きみのすきないろ/さがしてるの")
C2 = ("あしたのわたしは/どきどきしてる/しろいぶらうすに/きめたんだよ/"
      "かがみのむこうで/えがおをつくる/あとはねむるだけ/めをとじるの")
C3 = ("あしたのわたしは/このふくでいく/いちばんすきなの/これにきめた/"
      "かがみのむこうで/ほほえむわたし/きみにあえるまで/あとすこしね/"
      "あしたのわたしは/なにをきてても/たぶんだいじょうぶ/またあしたね")
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC + VC, C1)
put("Aメロ2", K, VA + VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC + VC, C2)
put("最後のサビ", KL, VC + VC + VC, C3)

# ================= チェンバロ・ストリングス・口笛 =================
def harpsi(b, ch, busy=True):
    r = low(ch, "G2"); v = voice(ch, 64, 3)
    # v2: 全体が 7.2〜7.5 で平ら（チェンバロが左手4分・右手3声の裏8分を全場面で鳴らし、シャリシャリが続いていた）
    #     → 左手は根音と5度の2分、右手は「チャッ・チャー」と2回だけ
    HL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    pat = "R:0.5 {0}:0.5 R:1 R:0.5 {0}:1 R:0.5" if busy else "{0}:2 R:2"
    for j in range(3): HR[j].bar(b, pat.format(nm(v[j])))


def strings(b, ch, c=62):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


def pizz(b, ch):
    t = tones(ch, "G4", "G5")
    PIZ.bar(b, f"{nm(t[0])}:0.5 R:0.5 {nm(t[1 % len(t)])}:0.5 R:0.5 {nm(t[2 % len(t)])}:0.5 R:0.5 {nm(t[1 % len(t)])}:0.5 R:0.5")


MOTIF = ["R:1 B5:0.5 D6:0.5 E6:1 D6:0.5 A5:0.5", "G5:3 R:1"]      # 合いことばの節（3・5・6・5・2）
WSOLO = ["R:0.5 D6:0.5 B5:0.5 G5:0.5 A5:1 B5:1", "C6:2 B5:1 R:1", "R:0.5 E6:0.5 D6:0.5 B5:0.5 C6:1 A5:1", "B5:2 A5:1 R:1",
         "R:0.5 D6:0.5 E6:0.5 F#6:0.5 G6:1 E6:1", "D6:2 B5:1 R:1", "R:0.5 C6:0.5 B5:0.5 A5:0.5 B5:1 A5:1", "G5:3 R:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "チェンバロの前奏":
        harpsi(b, ch)
    elif n == "イントロ":
        harpsi(b, ch); strings(b, ch, 64)
        WH.bar(b, MOTIF[i % 2] if i < 4 else WSOLO[i])
    elif n in ("Aメロ1", "Aメロ2"):
        harpsi(b, ch)
        if i >= 8 or n == "Aメロ2": pizz(b, ch)
    elif n in ("Bメロ1", "Bメロ2"):
        harpsi(b, ch); strings(b, ch, 62)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        harpsi(b, ch); strings(b, ch, 67 if n == "最後のサビ" else 65); pizz(b, ch)
        if n == "最後のサビ" and i >= 16 and i % 2 == 1: WH.bar(b, "R:2 C6:0.5 Eb6:0.5 F6:1")
    elif n == "間奏":
        harpsi(b, ch); strings(b, ch, 62); WH.bar(b, MOTIF[i % 2] if i < 2 else WSOLO[i])
    elif n == "ベッドに倒れこむ":
        harpsi(b, ch, busy=False)
        if i >= 2: strings(b, ch, 60)
        if i == 4: WH.bar(b, MOTIF[0])
        if i == 5: WH.bar(b, MOTIF[1])
    elif n == "目覚まし":
        if i < 3: harpsi(b, ch, busy=i < 2); strings(b, ch, 64)

ALM.bar(S.sc("目覚まし")[3], "C7:0.25 R:0.25 C7:0.25 R:0.25 C7:0.25 R:1.25 G6:0.25 R:1.25")    # 目覚ましをかける「ピピッ」→「カチッ」

# ================= ウッドベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "チェンバロの前奏": continue
    if n in ("サビ1", "サビ2", "最後のサビ", "間奏"): BASS.bar(b, bass_line(S, b, "walk", lo="E1")); continue
    if n == "ベッドに倒れこむ":
        BASS.bar(b, f"{nm(r)}:4" if i >= 2 else "R:4"); continue
    if n == "目覚まし":
        if i < 3: BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        continue
    BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 {nm(r + 7)}:1.5 {nm(r + 7)}:0.5")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "C4")

# ================= ドラム（ブラシ）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "チェンバロの前奏": continue
    if n == "ベッドに倒れこむ":
        if i >= 4: D.set(b, "................", "..o...o...o...o.", "................")
        if last: halt(D, b, 1)        # 1拍止まって +1 へ
        continue
    if n == "目覚まし":
        if i < 2: D.set(b, "X.......X.......", "....o.......o...", "x.x.x.x.x.x.x.x.")
        if i == 2: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)
        continue
    if n in ("サビ1", "サビ2", "最後のサビ"):
        D.set(b, "X.....X.X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")
        if i % 8 == 0: crash(D, b, "C2", 6 if n == "最後のサビ" and i == 0 else 4)
    else:
        D.set(b, "X.......X.......", "....o.o.....o.o.", "x.x.x.x.x.x.x.x.")
    if i % 8 == 7 and not last: put_fill(D, b, "small")
    if last and n in ("Bメロ1", "Bメロ2", "間奏", "イントロ"): put_fill(D, b, "snare16")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の24（23時）。フレンチポップ。G長調・132、最後のサビは +1（A♭）。初デートの前の夜、鏡の前で服を何度も着がえる。"
          "チェンバロ・ストリングス・ピチカート・ウッドベース・ブラシ。口笛のかわりに高い縦笛。ベッドに倒れこむ静かな場面と1拍の止まりのあと、+1 の最後のサビ。"
          "合いことばの節は口笛。目覚ましをかける音で終わる。自作")
finish(S, LY, V, 1,
       level={"verse": -0.25}, special={"ベッドに倒れこむ": -0.45, "最後のサビ": 0.35, "目覚まし": -0.2})

# ================= v2（2026-11-12 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後11時・明日の服がきまらない・フレンチポップ）で直すこと:
#   口笛（高い縦笛）とフルートの音をやめ、電子の笛（kfbSineLead）に（人間「フルートの音は指定しない限り使わない」「そこら辺の音は電子って感じの音に」）
#   チェンバロは1音ずつ強さを揺らす。ウッドベースは同じ音を続ける所の穴をなくす
#   歌: Aメロ・Bメロはクリア（鏡の前のひとりごと）、サビはキュート（フレンチポップのかわいさ）、ベッドに倒れこむ所はウィスパー。ハモリは サビ2 の後半と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "チェンバロ", mid=84, down=10, up=8, seed=4)
set_parts(path, "ウッドベース", sustain=1.12)
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "最後のサビ": 22, "bridge": 0, "outro": 0}, scoop=0.3, slash=0.8, vib_min_beats=1.5, vib_start=0.5, auto=0.5, breaths=0.6)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, KL)], vol=0.36, shift=1)
    voice_by_scene(path, S, {"verse": "clear", "pre": "clear", "chorus": "cute", "bridge": "whisper"}, default="clear")
