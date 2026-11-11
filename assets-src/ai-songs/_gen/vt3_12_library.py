# vt3 12「図書館ではお静かに」Quiet in the Library（仮）— ジャズ（ピアノトリオ）。100（スウィング）・4/4。F長調（転調なし）。書き出しは全体を2半音下げる（テトの声に入れるため・E♭長調）。
# 第3弾（0時〜24時の街）の 11時。表は docs/sound/vt3-plan.md。
# 物語: 11時の図書館。窓の光の中で本の背をたどる指が、同じ本の上で、知らない人の指と重なる。声は出せない。
#   「先にどうぞ」と小さなメモを渡すと、返ってきたメモには、音符で書かれた5つの音（合いことばの節）。
#   ささやき声さえ響いてしまう部屋で、ページの音とまなざしだけの内緒話。貸し出しの期限は1週間後。
# 場面と強さ: ページ（ページをめくる音とピアノ・とても弱い）→ イントロ（トリオ）→ Aメロ1（ささやく・ブラシ・弱）→ Bメロ1
#   → サビ1（中）→ ピアノソロ（スティックに持ちかえ・いちばん強い・山）→ Aメロ2 → Bメロ2 → サビ2 → エンディング（本を閉じる）
# 旋律の性格: ささやくような細かい旋律（半音・小さな上り下り）、スウィングの8分。C4〜E5。
# この曲だけの音: ジャズのピアノトリオ（録音のピアノ・ウッドベースの指弾き・Naked Drums のブラシ）。歌はいちばん小さく、
#   山は歌ではなくピアノソロにある。ジャズの決まり（電子音を使わない・やわらかい音・ライドは長く鋭く）を守る。
#   合いことばの節（3・5・6・5・2＝A・C・D・C・G）は、ピアノソロの頭の右手。
from vt25_lib import *
import re as _re

S = Song("12", "library", "図書館ではお静かに（仮）", "Quiet in the Library", 100, 4, "F", "major", "ジャズ（ピアノトリオ・ボカロ）")
S.kit = "naked"
S.flags = "--bass rubner " + S.flags + " --piano salamander --space room --space-wet 0.2"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.35
S.drum_scale = 0.8
K = Key("F", "major")          # oct 4 で 1 = F4

_T = _re.compile(r"^([^:]+):([0-9.]+)(.*)$")


def warp(t):
    b = int(t + 1e-9); f = t - b
    return b + (f * 4 / 3 if f <= 0.5 + 1e-9 else 2 / 3 + (f - 0.5) * 2 / 3)


def swing(s):
    """まっすぐ書いた8分を、3連の跳ねる長さに直す（1小節）"""
    out, t = [], 0.0
    for x in s.split():
        m = _T.match(x); n, L, mk = m.group(1), float(m.group(2)), m.group(3)
        a, z = warp(t), warp(t + L)
        out.append(f"{n}:{z - a:.4f}{mk}"); t += L
    return " ".join(out)


A_CH = ["Fmaj7", "Dm9", "Gm9", "C13", "Am7", "D7b9", "Gm9", "C7sus4"]
B_CH = ["Bbmaj7", "Bbm6", "Am7", "Abdim7", "Gm9", "C7b9", "Fmaj7", "D7b9"]
C_CH = ["Bbmaj7", "Am7", "Gm9", "Fmaj7", "Ebmaj7#11", "D7b9", "Gm9", "C7sus4", "Bbmaj7", "Am7", "Dm9", "G13", "Gm9", "C13", "Fmaj7", "Fmaj7"]

S.scene("ページ", 2, "intro", ["Fmaj7", "Fmaj7"])
S.scene("イントロ", 4, "intro", ["Bbmaj7", "Am7", "Gm9", "C7sus4"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("ピアノソロ", 16, "solo", C_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("エンディング", 6, "outro", ["Bbmaj7", "Am7", "Gm9", "C7sus4", "Fmaj7", "Fmaj7"])

V = Voice(S, vol=0.19, delay=0.75, bright=-0.3, patch="mutedTrumpet", low=False)
PL = S.track("ピアノ（左手）", "piano", volume=0.1, pan=-0.2, reverb=0.25, fx=[{"type": "eq", "low": -2, "mid": -1, "midHz": 400, "high": -1}])
PR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.075, pan=-0.2, reverb=0.25, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": -1}]) for i in range(3)]
PS = S.track("ピアノ（ソロ）", "piano", volume=0.13, pan=-0.1, reverb=0.25, fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 800, "high": -1}])
BASS = S.track("ウッドベース", "bass", **finger_bass_spec(vol=0.24))
PAGE = S.track("ページの音（カホンの縁）", "cajon", volume=0.05, pan=0.3, reverb=0.15)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌（ささやく。スウィングの8分）=================
VA = ["R:1 3:0.5 2:0.5 3:0.5 5:0.5 3:1", "2:1.5 R:2.5", "R:1 2:0.5 1:0.5 2:0.5 4:0.5 3:1", "1:1.5 R:2.5",
      "R:1 6:0.5 5:0.5 6:0.5 1':0.5 6:1", "5:1.5 R:2.5", "R:1 4:0.5 3:0.5 2:0.5 3:0.5 4:0.5 5:0.5", "3:2 R:2"]
A1 = "しずかなへや/まどのひかり/ほんのせなか/ゆびでたどるの/おなじほんに/ふたつのゆび/めとめがあう/こえはだせない"
A2 = "めもをかいて/そっとわたすの/さきにどうぞ/ちいさなもじで"
VB = ["R:0.5 4:0.5 5:0.5 6:0.5 1':1 6:1", "5:1 4:1 2:1 R:1", "R:0.5 3:0.5 4:0.5 5:0.5 7:1 5:1", "4:1 3:1 1:1 R:1",
      "R:0.5 4:0.5 5:0.5 6:0.5 1':1 2':1", "1':1 7:1 6:1 R:1", "R:0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5", "6:2 R:2"]
B1 = "ささやきごえでも/ひびいてしまうの/ぺーじのおとだけ/こたえのかわりに"
B2 = "かえってきためもに/ちいさなはなうた/おんぷでかかれて/いつつのおとだけ"
VC = ["R:0.5 1':0.5 1':0.5 7:0.5 6:1 5:1", "6:1.5 4:0.5 4:1 R:1", "R:0.5 5:0.5 5:0.5 4:0.5 3:1 2:1", "3:2 R:2",
      "R:0.5 b7:0.5 b7:0.5 6:0.5 5:1 3:1", "#1:1.5 6:0.5 6:1 R:1", "R:0.5 5:0.5 4:0.5 3:0.5 4:1 6:1", "5:2 R:2",
      "R:0.5 1':0.5 1':0.5 7:0.5 6:1 5:1", "6:1.5 1':0.5 1':1 R:1", "R:0.5 2':0.5 2':0.5 1':0.5 6:1 5:1", "7:2 R:2",
      "R:0.5 4:0.5 5:0.5 6:0.5 1':1 2':1", "1':1.5 7:0.5 6:1 R:1", "R:0.5 6:0.5 5:0.5 3:0.5 2:1 3:1", "1:3 R:1"]
C1 = "としょかんだからね/こえはだめよ/まなざしでかたる/ないしょばなし/ほんだなのあいだ/ひかるほこり/ふたりのことばは/しずかなおと"
C2 = "としょかんだからね/こえはだめよ/めもようしのはし/えがおひとつ/かえすのはいつに/しようかなって/かしだしのきげん/いっしゅうかんご"
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [swing(K.mel(x, oct=o)) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
if VOCAL: put("エンディング", ["R:4", "R:4", "R:1 3:1 2:1 1:1", "R:4", "R:4", "R:4"], "またね")

# ================= ピアノ（左手は低い根音と7度、右手は3音のやわらかい和音）=================
def comp(b, ch, style):
    r = low(ch, "F2"); v = voice(ch, 64, 3)
    if style == "long":
        PL.bar(b, f"{nm(r)}:4")
        for j in range(3): PR[j].bar(b, f"{nm(v[j])}:4")
    elif style == "charleston":    # 1拍目と2拍目の裏（チャールストン）
        PL.bar(b, swing(f"{nm(r)}:1.5 R:2.5"))
        for j in range(3): PR[j].bar(b, swing(f"{nm(v[j])}:1.5 {nm(v[j])}:0.5 R:2"))
    else:                          # 2拍目と4拍目の裏をふむ
        PL.bar(b, swing(f"{nm(r)}:2 {nm(r + 7)}:2"))
        for j in range(3): PR[j].bar(b, swing(f"R:1.5 {nm(v[j])}:1 R:1 {nm(v[j])}:0.5"))


SOLO = ["R:1 A5:0.5 C6:0.5 D6:1 C6:0.5 G5:0.5", "A5:2 R:1 C5:0.5 D5:0.5",                                   # 合いことばの節
        "F5:0.5 G5:0.5 A5:0.5 Bb5:0.5 D6:1 C6:1", "A5:1.5 F5:0.5 E5:1 R:1",
        "G5:0.5 Bb5:0.5 D6:0.5 F6:0.5 E6:1 D6:1", "C6:0.5 A5:0.5 F#5:0.5 Eb5:0.5 D5:1 R:1",
        "Bb4:0.5 D5:0.5 F5:0.5 A5:0.5 G5:1 F5:0.5 E5:0.5", "F5:3 R:1",
        "D6:0.5 C6:0.5 A5:0.5 F5:0.5 G5:1 A5:1", "C6:1.5 A5:0.5 G5:1 R:1",
        "F5:0.5 A5:0.5 C6:0.5 E6:0.5 D6:1 A5:1", "B5:0.5 A5:0.5 G5:0.5 F5:0.5 E5:1 R:1",
        "Bb5:0.5 A5:0.5 G5:0.5 F5:0.5 D5:1 F5:1", "E5:0.5 G5:0.5 Bb5:0.5 D6:0.5 C6:1 Bb5:1", "A5:1 F5:1 C5:1 E5:1", "F5:3 R:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "ページ":
        if i == 1: comp(b, ch, "long")
    elif n == "イントロ": comp(b, ch, "push")
    elif n in ("Aメロ1", "Aメロ2"): comp(b, ch, "charleston" if i % 2 == 0 else "long")
    elif n in ("Bメロ1", "Bメロ2", "サビ1", "サビ2"): comp(b, ch, "push")
    elif n == "ピアノソロ":
        PS.bar(b, swing(SOLO[i]))
        r = low(ch, "F2"); v = voice(ch, 60, 3)
        PL.bar(b, swing(f"R:1 {nm(v[0])}:0.5 R:1.5 {nm(v[1])}:1"))
    elif n == "エンディング":
        comp(b, ch, "long" if i >= 4 else "push")

PAGE.bar(S.sc("ページ")[0], "F3:0.5 R:0.25 G3:0.25 R:3")           # ページをめくる
PAGE.bar(S.sc("エンディング")[5], "R:2 A2:1 R:1")                    # 本を閉じる（低い「ぽん」）

# ================= ウッドベース（歩く4分）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "ページ": continue
    if n == "Aメロ1" and i < 4: BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    elif n == "エンディング": BASS.bar(b, bass_line(S, b, "walk", lo="E1") if i < 4 else f"{nm(r)}:4")
    else: BASS.bar(b, bass_line(S, b, "walk", lo="E1"))

# ================= ドラム（ブラシ → ソロはスティックのライド）=================
RIDE = "D2:1 D2:0.6667 D2:0.3333 D2:1 D2:0.6667 D2:0.3333"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ページ": continue
    if n == "ピアノソロ":
        D.set(b, "X.........X.....", "......o.....o...", "....x.......x...")
        D.R.bar(b, RIDE)
        if i == 0: crash(D, b)
        if i == 15: put_fill(D, b, "small")
    elif n in ("サビ1", "サビ2"):
        D.set(b, "X.......X.......", "....o.......o...", "....x.......x...")
        D.R.bar(b, RIDE)
        if i == 0: crash(D, b)
    elif n == "エンディング":
        if i < 4: D.set(b, "X...............", "....o.......o...", "....x.......x..."); D.R.bar(b, RIDE)
        elif i == 4: crash(D, b, "C2", 8)
    else:   # ブラシのような弱いスネアとハイハット
        D.set(b, "X...............", "..o...o...o...o.", "....x.......x...")
        if n in ("Bメロ1", "Bメロ2"): D.R.bar(b, RIDE)

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の12（11時）。ジャズのピアノトリオ。F長調・100（スウィング）。"
          "図書館で同じ本に手をのばした二人の、声に出せない会話。録音のピアノ・ウッドベース・Naked Drums のブラシとライド。"
          "山は歌ではなくピアノソロ。合いことばの節はピアノソロの頭。ページをめくる音で始まり、本を閉じる音で終わる。自作")
finish(S, LY, V, -2,
       level={"verse": -0.4, "chorus": 0.1}, special={"ピアノソロ": 0.2, "エンディング": -0.3})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午前11時・図書館・ジャズのピアノトリオ）で直すこと:
#   ジャズの決まり（電子の音は使わない・録音の楽器だけ）なので、音は足さない。ピアノは1音ずつ強さを揺らす（左手は重く、右手は軽く、ソロは抑揚を大きく）。
#   ウッドベースは同じ音を続ける所の穴をなくす
#   歌: 図書館なので、Aメロはウィスパー（ひそひそ声）、Bメロとサビはクリア。揺れは浅く、長い音の後ろだけ。ハモリなし（トリオの静けさを残す）
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ピアノ（右手", mid=78, down=14, up=10, seed=4); humanize(path, "ピアノ（左手", mid=84, down=8, up=8, seed=5); humanize(path, "ピアノ（ソロ", mid=84, down=16, up=14, seed=6)
set_parts(path, "ウッドベース", sustain=1.12)
final_gain(path, {"ページ": 6, "ピアノソロ": -0.8, "サビ2": 1.0})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5, minlen=1.0))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 20, "outro": 8}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.55, auto=0.7, breaths=0.7)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "clear", "outro": "whisper"}, default="clear")
