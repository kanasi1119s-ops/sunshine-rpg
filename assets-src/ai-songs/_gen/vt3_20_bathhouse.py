# vt3 20「湯けむりスウィング」Steam-Bath Swing（仮）— ジャズ（ビッグバンド）。176（スウィング）・4/4。B♭長調（転調なし）。
# 第3弾（0時〜24時の街）の 19時。表は docs/sound/vt3-plan.md。
# 物語: 夜7時の町の銭湯。のれんをくぐると、湯気のむこうに大きな富士の絵。桶の「カコーン」が天井にひびく。
#   となりの知らないおじいが鼻歌をうたっている。その節なら、わたしも知ってる。声を重ねたら、ほかの人まで ── 湯船が舞台になる。
#   のぼせそうでも止まらない。一日の疲れはお湯にとけて流れていく。湯上がりはコーヒー牛乳。番台さんも笑ってくれる。
# 場面と強さ: 桶（カコーン・響き）→ イントロ（ビッグバンド・強）→ Aメロ1（ブラシ・中）→ Bメロ1 → サビ1（ブラスのかけ合い・強）
#   → サックスのソリ → Aメロ2 → Bメロ2 → サビ2 → ドラムソロ → トロンボーンのソロ（節）→ 湯船に沈む（ベースとブラシだけ・とても静か）
#   → シャウトコーラス（全員・いちばん強い）→ エンディング（ブラス全員のキメ）
# 旋律の性格: 歌いあげるスウィングの節（F4〜F5）、句の終わりは長く伸ばす。
# この曲だけの音: ビッグバンド（トランペット・トロンボーン・アルトとバリトンのサックス）、ウッドベースの指弾き、ライドの長い鳴り（ジャズの決まり）。
#   歌の山のあとに、ブラス全員の「シャウトコーラス」。合いことばの節（3・5・6・5・2＝D・F・G・F・C）は、トロンボーンのソロの頭。
from vt25_lib import *
import re as _re

S = Song("20", "bathhouse", "湯けむりスウィング（仮）", "Steam-Bath Swing", 176, 4, "Bb", "major", "ジャズ（ビッグバンド・ボカロ）")
S.kit = "naked"
S.flags = "--bass rubner " + S.flags + " --piano salamander --space hall --space-wet 0.16"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.4
S.drum_scale = 0.85
K = Key("Bb", "major")          # oct 3 で 1 = B♭3

_T = _re.compile(r"^([^:]+):([0-9.]+)(.*)$")


def warp(t):
    b = int(t + 1e-9); f = t - b
    return b + (f * 4 / 3 if f <= 0.5 + 1e-9 else 2 / 3 + (f - 0.5) * 2 / 3)


def swing(s):
    out, t = [], 0.0
    for x in s.split():
        m = _T.match(x); n, L, mk = m.group(1), float(m.group(2)), m.group(3)
        a, z = warp(t), warp(t + L); out.append(f"{n}:{z - a:.4f}{mk}"); t += L
    return " ".join(out)


A_CH = ["Bb6", "Bdim7", "Cm7", "F7", "Dm7", "G7", "Cm7", "F7"]
B_CH = ["Ebmaj7", "Ebm6", "Bb/D", "G7", "Cm7", "F7", "Bb6", "F7"]
C_CH = ["Ebmaj7", "Ab7", "Dm7", "G7", "Cm7", "F7", "Bb6", "Bb6"]

S.scene("桶", 2, "intro", ["Bb6", "Bb6"])
S.scene("イントロ", 16, "intro", C_CH + A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 24, "chorus", C_CH)
S.scene("サックスのソリ", 16, "solo", C_CH)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 24, "chorus", C_CH)
S.scene("ドラムソロ", 8, "solo", ["Bb6"] * 8)
S.scene("トロンボーンのソロ", 8, "solo", A_CH)
S.scene("湯船に沈む", 8, "bridge", ["Ebmaj7", "Ebm6", "Bb/D", "G7", "Cm7", "F7", "Cm7", "F7"])
S.scene("シャウトコーラス", 16, "chorus", C_CH)
S.scene("エンディング", 10, "outro", ["Ebmaj7", "Ab7", "Dm7", "G7", "Cm7", "F7", "Bb6", "Bb6", "Bb6", "Bb6"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="clarinet", low=False)   # v2: BGM の旋律はクラリネット（サックスの伴奏と同じ音色でぶつかっていた）
TPS = [S.track(f"トランペット{i + 1}", "brass", patch="trumpet", volume=0.055, pan=0.35, reverb=0.3) for i in range(3)]
TBS = [S.track(f"トロンボーン{i + 1}", "brass", patch="trombone", volume=0.055, pan=-0.35, reverb=0.3) for i in range(3)]
TBL = S.track("トロンボーン（ソロ）", "brass", patch="trombone", volume=0.11, pan=-0.1, reverb=0.3)
AS = [S.track(f"アルトサックス{i + 1}", "brass", patch="altoSax", volume=0.06, pan=0.1 - 0.2 * i, reverb=0.28) for i in range(2)]
BS = S.track("バリトンサックス", "brass", patch="bariSax", volume=0.07, pan=0.0, reverb=0.25)
PL = S.track("ピアノ（左手）", "piano", volume=0.09, pan=-0.15, reverb=0.25, fx=[{"type": "eq", "low": -2, "mid": -1, "midHz": 400, "high": -1}])
PR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.065, pan=-0.15, reverb=0.25, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": -1}]) for i in range(3)]
BASS = S.track("ウッドベース", "bass", **finger_bass_spec(vol=0.24))
OKE = S.track("桶（カホン）", "cajon", volume=0.09, pan=0.25, reverb=0.6)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5:0.5 6:0.5 1':1 6:1", "5:1.5 3:0.5 5:2", "R:1 4:0.5 5:0.5 6:1 5:1", "3:1.5 2:0.5 1:2",
      "R:1 5:0.5 6:0.5 1':1 3':1", "2':1.5 1':0.5 6:2", "R:0.5 5:0.5 6:0.5 5:0.5 4:0.5 3:0.5 4:0.5 2:0.5", "1:3 R:1"]
A1 = "まちのせんとう/のれんくぐれば/ゆげのむこうに/おおきなふじのえ/おけがかこーん/ひびくてんじょう/しらないおじい/はなうたうたってる"
A2 = "そのふしならば/わたしもしってる/こえかさねたら/ほかのひとまでも/ゆぶねがぶたい/たいるがきらり/いっきょくおわれば/はくしゅがわれるよ"
VB = ["R:1 3:0.5 4:0.5 5:1 1':1", "1':2 b6:1 R:1", "R:1 3:0.5 4:0.5 5:1 1':1", "#1':2 6:1 R:1",
      "R:1 4:0.5 5:0.5 6:1 2':1", "2':2 1':1 R:1", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 3':1", "2':3 R:1"]
B1 = "のぼせそうだ/とまらないの/ゆげのなかで/みんなわらう"
B2 = "きょういちにち/つかれさえも/おゆにとけて/ながれてゆく"
VC = ["1':1 1':0.5 2':0.5 3':1 1':1", "b7:0.5 1':0.5 b7:1 R:2", "3':1 3':0.5 2':0.5 1':1 3':1", "3':0.5 #1':0.5 6:1 R:2",
      "2':1 2':0.5 3':0.5 4':1 2':1", "5:0.5 3:0.5 5:1 R:2", "R:0.5 5:0.5 6:0.5 1':0.5 3':1 2':1", "1':3 R:1"]
VCL = VC[:6] + ["R:0.5 5:0.5 6:0.5 1':0.5 5':1 3':1", "1':3 R:1"]
HOOK = "ゆけむりすいんぐ"
C1 = (f"{HOOK}/みんなでゆれよう/おけでりずむとり/ゆにつかろう/{HOOK}/しらないどうしで/おなじおゆのなか/なかまだよね/"
      f"{HOOK}/てぬぐいあたまに/のせてごきげんに/ぽかぽかだね")
C2 = (f"{HOOK}/ほおがあかくなる/あまいぎゅうにゅうを/ごくごくのむ/{HOOK}/あしたもくるかい/ばんだいさんがね/わらうからね/"
      f"{HOOK}/おふろあがりには/いちごのぎゅうにゅう/それもいいね")
C3 = f"{HOOK}/またあしたここで/あのふしうたおう/いいゆだなあ/{HOOK}/のれんをくぐれば/よかぜがすずしい/おやすみだね"
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [swing(K.mel(x, oct=o)) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC + VC + VC[:8], C1)
put("Aメロ2", VA + VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC + VC + VC, C2)
put("シャウトコーラス", VC + VCL, C3)

# ================= ビッグバンド =================
def sec(tracks, b, ch, pat, c):
    v = voice(ch, c, len(tracks))
    for j, t in enumerate(tracks): t.bar(b, swing(" ".join(x.replace("x", nm(v[j])) for x in pat.split())))


def comp(b, ch):
    r = low(ch, "F2"); v = voice(ch, 62, 3)
    PL.bar(b, swing(f"{nm(r)}:1.5 R:2.5"))
    for j in range(3): PR[j].bar(b, swing(f"R:1.5 {nm(v[j])}:0.5 R:1.5 {nm(v[j])}:0.5"))


SOLI = ["D5:0.5 F5:0.5 G5:0.5 Bb5:0.5 A5:1 G5:1", "F5:0.5 Eb5:0.5 C5:0.5 A4:0.5 Bb4:1 R:1", "F5:0.5 D5:0.5 F5:0.5 A5:0.5 C6:1 A5:1", "G5:1.5 F5:0.5 D5:1 R:1",
        "Eb5:0.5 G5:0.5 Bb5:0.5 G5:0.5 C6:1 Bb5:1", "A5:0.5 F5:0.5 Eb5:0.5 C5:0.5 D5:1 F5:1", "D5:0.5 C5:0.5 Bb4:0.5 C5:0.5 D5:1 F5:1", "Bb4:3 R:1"]
MOTIF = ["R:1 D4:0.5 F4:0.5 G4:1 F4:0.5 C4:0.5", "Bb3:3 R:1"]      # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        comp(b, ch)
        sec(TPS, b, ch, "x:1.5! x:0.5 R:2" if i % 2 == 0 else "R:2 x:0.5 x:0.5 x:1", 72)
        sec(TBS, b, ch, "x:2 x:2", 58)
        if i >= 8: sec(AS + [BS], b, ch, "R:1 x:1 R:1 x:1", 62)
    elif n in ("Aメロ1", "Aメロ2"):
        comp(b, ch)
        if n == "Aメロ2" or i >= 8: sec(TBS, b, ch, "x:4", 56)
        if i % 4 == 3: sec(TPS, b, ch, "R:2.5 x:0.5 x:1", 70)
    elif n in ("Bメロ1", "Bメロ2"):
        comp(b, ch); sec(AS + [BS], b, ch, "x:2 x:2", 60)
    elif n in ("サビ1", "サビ2"):
        comp(b, ch)
        # v2: サビが 7.0〜7.2（サックスが毎小節2拍4拍に刻み、ブラスのかけ合いも毎小節で、歌のまわりが埋まっていた）
        #     → サックスはのばす和音（下じき）、トランペットのかけ合いは4小節に1回、トロンボーンは2小節に1回
        sec(TPS, b, ch, "R:2.5 x:0.5! x:1" if i % 4 == 3 else "R:4", 72)
        sec(TBS, b, ch, "x:1.5 x:0.5 R:2" if i % 4 == 1 else "R:4", 56)
        sec(AS + [BS], b, ch, "x:4", 58)
    elif n == "サックスのソリ":
        comp(b, ch)
        AS[0].bar(b, swing(SOLI[i % 8]))
        AS[1].bar(b, swing(shift_oct(SOLI[i % 8], -1)))
        BS.bar(b, swing(shift_oct(SOLI[i % 8], -2)))
        if i >= 8: sec(TBS, b, ch, "x:4", 56)
    elif n == "ドラムソロ":
        # v3: ドラムだけの8小節が 6.9（いちばん低い）→ 2小節ずつ「ブラス全員 ⇄ ドラム」のかけ合い（トレード）にする
        if i % 4 < 2:
            comp(b, ch)
            sec(TPS, b, ch, ["x:1.5! x:0.5 R:0.5 x:0.5 x:1", "R:1 x:0.5 x:0.5! R:1 x:1"][i % 2], 72)
            sec(TBS, b, ch, ["x:1.5 x:0.5 R:0.5 x:0.5 x:1", "R:1 x:0.5 x:0.5 R:1 x:1"][i % 2], 58)
            sec(AS + [BS], b, ch, "x:2 x:2", 62)
        if i == 7: sec(TPS + TBS, b, ch, "R:3 x:1!", 64)
    elif n == "トロンボーンのソロ":
        comp(b, ch)
        TBL.bar(b, swing(MOTIF[i] if i < 2 else ["F3:0.5 G3:0.5 Bb3:0.5 D4:0.5 F4:1 D4:1", "Eb4:1 C4:1 A3:2", "Bb3:0.5 D4:0.5 F4:0.5 A4:0.5 G4:1 F4:1",
                                                    "D4:1.5 C4:0.5 Bb3:1 R:1", "Eb4:0.5 F4:0.5 G4:0.5 A4:0.5 Bb4:2", "A4:1 F4:1 C4:2"][i - 2]))
    elif n == "湯船に沈む":
        v = voice(ch, 60, 3)
        for j in range(3): PR[j].bar(b, f"{nm(v[j])}:4" if i % 2 == 0 else "R:4")
    elif n == "シャウトコーラス":
        comp(b, ch)
        sec(TPS, b, ch, "x:1.5! x:0.5 R:0.5 x:0.5 x:1" if i % 2 == 0 else "R:1 x:0.5 x:0.5! R:1 x:1", 74)
        sec(TBS, b, ch, "x:1.5 x:0.5 R:0.5 x:0.5 x:1" if i % 2 == 0 else "R:1 x:0.5 x:0.5 R:1 x:1", 58)
        sec(AS + [BS], b, ch, "x:1 x:1 x:1 x:1", 63)
    elif n == "エンディング":
        if i < 6:
            comp(b, ch); sec(TPS, b, ch, "x:2 x:2", 72); sec(TBS, b, ch, "x:4", 58); sec(AS + [BS], b, ch, "x:2 x:2", 62)
        elif i == 6:
            sec(TPS, b, ch, "x:0.5! R:0.5 x:0.5! R:0.5 x:2!", 74); sec(TBS, b, ch, "x:0.5! R:0.5 x:0.5! R:0.5 x:2!", 58); sec(AS + [BS], b, ch, "x:0.5! R:0.5 x:0.5! R:0.5 x:2!", 63)
        elif i == 7:
            sec(TPS, b, ch, "x:4", 74); sec(TBS, b, ch, "x:4", 58); sec(AS + [BS], b, ch, "x:4", 63)
        elif i == 8:
            sec(TPS, b, ch, "x:0.5! R:3.5", 76); sec(TBS, b, ch, "x:0.5! R:3.5", 58); sec(AS + [BS], b, ch, "x:0.5! R:3.5", 63)

OKE.bar(S.sc("桶")[0], "A2:2 R:2"); OKE.bar(S.sc("湯船に沈む")[0], "A2:2 R:2")

# ================= ウッドベース（歩く4分）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "桶" or (n == "ドラムソロ" and i % 4 >= 2): continue
    if n == "湯船に沈む": BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); continue
    if n == "エンディング":
        if i < 6: BASS.bar(b, bass_line(S, b, "walk", lo="E1"))
        elif i in (6, 7): BASS.bar(b, f"{nm(r)}:4")
        elif i == 8: BASS.bar(b, f"{nm(r)}:0.5 R:3.5")
        continue
    BASS.bar(b, bass_line(S, b, "walk", lo="E1"))

# ================= ドラム（ライドの長い鳴り・ブラシ）=================
RIDE = "D2:1 D2:0.6667 D2:0.3333 D2:1 D2:0.6667 D2:0.3333"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "桶": continue
    if n == "湯船に沈む":
        D.set(b, "................", "..o...o...o...o.", "....x.......x..."); continue
    if n == "ドラムソロ" and i % 4 < 2:
        D.set(b, "X.........X.....", "......o.....o...", "....x.......x..."); D.R.bar(b, RIDE)
        if i % 4 == 0: crash(D, b, "C2", 6)
        continue
    if n == "ドラムソロ":
        D.set(b, "X..X..X.X..X....", "....X.xX.X..XxXx" if i % 2 == 0 else "X.x.X.xxX.x.XXXX", "................")
        if i % 4 == 0: crash(D, b, "C2", 6)
        if i == 7: D.set(b, "X...............", "X.x.X.x.XXXXXXXX", "................")
        continue
    if n == "エンディング":
        if i < 6: D.set(b, "X.........X.....", "......o.....o...", "....x.......x..."); D.R.bar(b, RIDE)
        elif i == 6: D.set(b, "X...X...X.......", "X...X...X.......", "................")
        elif i == 8: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 8)
        continue
    if n in ("Aメロ1",) and i < 8:
        D.set(b, "X...............", "..o...o...o...o.", "....x.......x..."); D.R.bar(b, RIDE); continue
    D.set(b, "X.........X.....", "......o.....o...", "....x.......x...")
    D.R.bar(b, RIDE)
    if n in ("サビ1", "サビ2", "シャウトコーラス", "イントロ") and i % 8 == 0: crash(D, b, "C2", 6)
    if i % 8 == 7 and not last: put_fill(D, b, "small")
    if last and n in ("Bメロ1", "Bメロ2", "サックスのソリ", "サビ2", "トロンボーンのソロ"): put_fill(D, b, "snare16")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の20（19時）。ジャズのビッグバンド。B♭長調・176（スウィング）。町の銭湯で、知らない人たちと歌い出す。"
          "トランペット・トロンボーン・アルトとバリトンのサックス・ウッドベース・ライドの長い鳴り。サックスのソリとドラムソロ、最後はブラス全員のシャウトコーラス。"
          "合いことばの節はトロンボーンのソロの頭。桶の「カコーン」で始まる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"湯船に沈む": -0.6, "シャウトコーラス": 0.4, "ドラムソロ": 0.1})
