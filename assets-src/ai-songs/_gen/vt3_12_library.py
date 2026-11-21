# vt3 12「図書館ではお静かに」Quiet in the Library（仮）— テクノポップ（Kawaii future bass の音）。112・4/4。F長調。
# 第3弾（0時〜24時の街）の 11時。表は docs/sound/vt3-plan.md。
#
# v2（2026-11-15）: ゼロから作り直し。人間の指示（2026-11-15）:「ボカロ系の曲は、ロック、テクノポップ、ファンク、KPOP、ダンス、ケルトで」
#   「曲の構成も11から既存の作り方とは違う構成に」「電子音はkawaiiFutureベースで」→ この曲はテクノポップ。v1 はジャズのピアノトリオだった。
#
# 構成（Aメロ・Bメロ・サビの形を使わない）: くり返しのない「積み上げ」。8小節ごとに音が1つずつ増え、歌の節は毎回新しい。
#   そのあいだに、鼻歌（合いことばの節 3・5・6・5・2）が3回はさまる。鼻歌は 1人 → 2人 → 3人 と増える。
#   ページ（時計の刻みと低い音）→ こごえ（歌1）→ 鼻歌1 → となり（歌2）→ 鼻歌2 → ひろがる（歌3）→ 鼻歌3 → 司書さん（ぐっと静かに・歌4）
#   → みんな（歌5・のぼっていく）→ 大合唱（この曲でただ1回の大きな場面。鼻歌の節が主役になる）→ おしずかに（すっと静かにもどる）
#
# 物語: 11時の図書館。聞こえるのはページの音だけ。となりの席から、聞こえるかどうかの小さな鼻歌 ── あの節だ。本だなをとびこえ、窓ぎわにもうつる。
#   知らない人どうし、目と目が合う。司書さんがこっちを見た。しかられる、と思ったら、司書さんまで歌い出した。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: 「お静かに」の決まりが、声をひそめたままの大合唱になる。
#
# 曲を決める表:
#   旋律: 歌1＝低い所でぽつぽつ（1拍おいて4音 → 2音）。歌2＝8分の弱起で5音 → 3音。歌3＝付点のはねる9音。歌4＝2拍おいて長い音2つ。歌5＝4分でのぼる。
#         大合唱＝鼻歌の節（るるるるる）→ 言葉の返事、を3回
#   和音: 場面ごとにちがう進み方（同じ4つをくり返さない）。大合唱だけ I → V → vi → IV
#   ベース: FM のベースの短い8分（根音とオクターブ上）。司書さんの場面は1拍目だけ
#   この曲だけ: ①くり返しなしの積み上げ ②合いことばの節がこの曲では主役 ③大きい場面は1回だけで、最後は静かにもどる
#   音色（Kawaii future bass）: kfbFmBass・kfbSquarePluck・kfbGlassEp・kfbSparklePad・kfbSupersaw・kfbSawStab・kfbBrightBells・kfbGlocken・kfbSineLead・kfbSub
from vt25_lib import *

S = Song("12", "library", "図書館ではお静かに（仮）", "Quiet in the Library", 112, 4, "F", "major", "テクノポップ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.4
S.drum_scale = 0.85
S.keepers = {}
K = Key("F", "major")          # oct 4 で 1 = F4

HUM_CH = ["F", "C/E", "Dm", "Bb", "F", "C/E", "Bb", "C"]
S.scene("ページ", 8, "intro", ["F", "F", "Dm", "Dm", "Bb", "Bb", "C", "C"])
S.scene("こごえ", 8, "verse", ["F", "Am", "Bb", "C", "F", "Am", "Bb", "C"])
S.scene("鼻歌1", 8, "break", HUM_CH)
S.scene("となり", 8, "verse", ["Dm", "Bb", "F", "C", "Dm", "Bb", "Gm7", "C"])
S.scene("鼻歌2", 8, "break", HUM_CH)
S.scene("ひろがる", 8, "pre", ["Bb", "C", "Am", "Dm", "Bb", "C", "F", "F"])
S.scene("鼻歌3", 8, "break", HUM_CH)
S.scene("司書さん", 8, "bridge", ["Dm", "Dm", "Bb", "Bb", "Gm7", "Gm7", "C7sus4", "C7"])
S.scene("みんな", 16, "pre", ["Bb", "C", "Dm", "F/A", "Bb", "C", "Dm", "C", "Bb", "Bb", "C", "C", "Dm", "Dm", "C7sus4", "C7"])
S.scene("大合唱", 24, "chorus", HUM_CH * 3)
S.scene("おしずかに", 9, "outro", ["F", "C/E", "Dm", "Bb", "F", "F", "F", "F", "F"])

PING = [{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}]
V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)
TICK = S.track("時計の刻み（鉄琴の高い音）", "lead", patch="kfbGlocken", volume=0.075, pan=0.35, reverb=0.2)
FMB = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.085, pan=0, duck=0.3)
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.034, pan=0, duck=0.5)
PLK = S.track("プラックの分散和音", "lead", patch="kfbSquarePluck", volume=0.05, pan=-0.35, reverb=0.3, fx=PING)
EP = [S.track(f"ガラスのエレピ{i + 1}", "lead", patch="kfbGlassEp", volume=0.06, pan=0.3 - 0.2 * i, reverb=0.25) for i in range(3)]
PAD = [S.track(f"きらめくパッド{i + 1}", "lead", patch="kfbSparklePad", volume=0.034, pan=-0.4 + 0.4 * i, reverb=0.45) for i in range(3)]
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersaw", volume=0.03, pan=-0.5 + 0.5 * i, reverb=0.25, duck=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(3)]
BELL = S.track("ベル（鼻歌への返事）", "lead", patch="kfbBrightBells", volume=0.075, pan=0.25, reverb=0.4)
LEAD = S.track("サイン波のリード", "lead", patch="kfbSineLead", volume=0.06, pan=-0.1, reverb=0.35)
KDR = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()

# ================= 歌（節は場面ごとに新しい）=================
HUM = ["R:1.5 3:0.5 5:0.5 6:1.5", "5:1 2:2 R:1"]                         # 合いことばの節（3・5・6・5・2）
HUM_B = ["R:1.5 5:0.5 1':0.5 1':1.5", "7:1 5:2 R:1"]                     # 返しの節（上の形）
REST2 = ["R:4", "R:4"]
L1 = ["R:1 1:0.5 1:0.5 2:1 1:1", "5,:1 1:1 R:2", "R:1 4:0.5 4:0.5 5:1 4:1", "2:2 R:2",
      "R:1 1:0.5 2:0.5 3:1 1:1", "3:1 5:1 R:2", "R:1 4:0.5 5:0.5 6:1 4:1", "5:2 R:2"]
L2 = ["R:0.5 6,:0.5 1:0.5 3:0.5 3:1 1:1", "4:0.5 4:0.5 1:1 R:2", "R:0.5 1:0.5 3:0.5 5:0.5 5:1 3:1", "2:0.5 2:0.5 5,:1 R:2",
      "R:0.5 3:0.5 3:0.5 6:0.5 6:1 3:1", "4:0.5 6:0.5 4:1 R:2", "R:0.5 2:0.5 4:0.5 6:0.5 6:1 4:1", "5:0.5 5:0.5 5:1 R:2"]
L3 = ["4:0.75 6:0.75 1':0.5 6:1 4:1", "5:0.75 7:0.75 5:0.5 3:1 R:1", "3:0.75 5:0.75 7:0.5 5:1 3:1", "6:0.75 6:0.75 3:0.5 1:1 R:1",
      "4:0.75 6:0.75 1':0.5 1':1 6:1", "7:0.75 5:0.75 5:0.5 7:1 R:1", "1':1 6:0.5 5:0.5 3:1 5:1", "1:2 R:2"]
L4 = ["R:2 6,:1 1:1", "3:2 1:1 R:1", "R:2 1:1 4:1", "6:2 4:1 R:1", "R:2 2:1 4:1", "6:2 4:1 R:1", "R:1 5:1 4:1 5:1", "5:3 R:1"]
L5 = ["R:1 4:1 6:1 1':1", "7:1.5 5:0.5 5:1 R:1", "R:1 6:1 1':1 6:1", "5:1.5 3:0.5 3:1 R:1",
      "R:1 4:1 6:1 1':1", "1':1.5 7:0.5 5:1 R:1", "R:1 6:1 1':1 1':1", "7:1.5 5:0.5 7:1 R:1",
      "4:2 6:2", "1':3 R:1", "5:2 7:2", "7:3 R:1", "6:2 6:2", "1':3 R:1", "5:2 7:2", "1':2 R:2"]
ANS1 = ["R:1 6:0.5 6:0.5 1':1 6:1", "4:1 6:1 R:2"]
ANS2 = ["R:1 4:0.5 6:0.5 1':1 6:1", "5:2 R:2"]
BIG8 = HUM + ANS1 + HUM_B + ANS2
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("こごえ", L1, "ほんのもりは/しずかだよ/ぺーじのおと/だけがする")
put("鼻歌1", HUM + REST2 + HUM + REST2, "るるるるる/るるるるる")
put("となり", L2, "となりのせきから/ちいさなはなうた/みみをすましたら/あのふしがしたよ")
put("鼻歌2", HUM + REST2 + HUM_B + REST2, "るるるるる/るるるるる")
put("ひろがる", L3, "ほんだなをとびこえ/まどぎわにもうつる/しらないひとどうし/めとめがあう")
put("鼻歌3", HUM + REST2 + HUM_B + REST2, "るるるるる/るるるるる")
put("司書さん", L4, "ししょさん/こっちみた/まずいな/とおもった")
put("みんな", L5, "あのひとまで/うたいだした/たなのむこう/かいだんまで/みんな/こえを/ひそめ/ながら")
put("大合唱", BIG8 * 3, ("るるるるる/しずかなうた/るるるるる/ひびいてる/るるるるる/こえはなくて/るるるるる/つたわるよ/"
                        "るるるるる/ほんのもりが/るるるるる/うたになる"))
put("おしずかに", HUM + ["R:1 6:0.5 6:0.5 5:1 3:1", "4:1 3:1 R:2"] + REST2 + REST2 + ["R:4"], "るるるるる/おしずかにね")

# ================= 伴奏（8小節ごとに1つずつ増える）=================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def tick(b, dense=False):
    TICK.bar(b, "C7:0.5 R:0.5 G6:0.5 R:0.5 C7:0.5 R:0.5 G6:0.5 R:0.5" if not dense else "C7:0.5 G6:0.5 C7:0.5 G6:0.5 C7:0.5 G6:0.5 C7:0.5 G6:0.5")


def fmb(b, style):
    ch = S.chords[b]; r = low(ch, "F1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "F1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); o = r + 12
    ap = t5 if rn == r else (rn - 2 if rn > r else rn + 2); N = nm
    FMB.bar(b, {"one": f"{N(r)}:1 R:3", "two": f"{N(r)}:0.5 R:1.5 {N(r)}:0.5 R:1 {N(t5)}:0.5",
                "oct": f"{N(r)}:0.5 R:0.5 {N(o)}:0.5 {N(r)}:0.5 R:0.5 {N(r)}:0.5 {N(o)}:0.5 {N(t5)}:0.5",
                "run": f"{N(r)}:0.5 {N(o)}:0.5 {N(r)}:0.5 {N(o)}:0.5 {N(t5)}:0.5 {N(o)}:0.5 {N(t5)}:0.5 {N(ap)}:0.5",
                "pulse": f"{N(r)}:0.5 {N(r)}:0.5 R:0.5 {N(r)}:0.5 {N(o)}:0.5 R:0.5 {N(t5)}:0.5 {N(ap)}:0.5"}[style])


def plk(b, order, lo="F4", hi="F6", L=0.25):
    tn = tones(root(b), lo, hi); PLK.bar(b, " ".join(f"{nm(tn[q % len(tn)])}:{L:g}" for q in order))


P16 = (0, 2, 3, 2, 4, 2, 3, 2, 0, 2, 3, 2, 4, 3, 2, 1)
P8 = (0, 2, 3, 4, 3, 2, 3, 2)


def ep(b, pat, c=65):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): EP[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def pad(b, n_=3, c=69):
    v = sorted(voice(root(b), c, 3))
    for j in range(n_): PAD[j].bar(b, f"{nm(v[j])}:4")


def saw(b, pat="x:1.5 x:1.5 x:1", c=65):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): SAW[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


BELL_ANS = ["R:1.5 A5:0.5 C6:0.5 D6:1.5", "C6:1 G5:2 R:1"]              # ベルが鼻歌をまねして返す
EP_A = "R:0.5 x:0.5 R:1 x:0.5 R:0.5 x:1"
EP_B = "x:1 R:0.5 x:0.5 R:1 x:0.5 R:0.5"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ページ":
        tick(b)                                                         # v7（2026-11-21）: 仕上げの持ち上げ（+8dB → 次の場面で戻す）をやめた。出だしが −33 と小さすぎるので、ベースとパッドを2小節ずつ早く入れ、時計の刻みを少し大きくする
        if i >= 2: fmb(b, "one" if i < 6 else "two")
        if i >= 4: pad(b, 1)
    elif n == "こごえ":
        tick(b); fmb(b, "two"); pad(b, 1)
    elif n.startswith("鼻歌"):
        lv = int(n[-1])
        tick(b, lv >= 2); pad(b, lv); fmb(b, "two" if lv == 1 else "oct")
        if i in (2, 3, 6, 7): BELL.bar(b, BELL_ANS[i % 2])
        if lv >= 2: plk(b, P8, L=0.5)
        if lv >= 3: ep(b, EP_A if i % 2 == 0 else EP_B)
    elif n == "となり":
        tick(b); fmb(b, "oct"); plk(b, P8, L=0.5); pad(b, 1)
    elif n == "ひろがる":
        tick(b, True); fmb(b, "oct" if i % 2 == 0 else "pulse"); plk(b, P16); ep(b, EP_A if i % 2 == 0 else EP_B)
    elif n == "司書さん":
        tick(b); fmb(b, "one"); pad(b, 2, 65)
        if i >= 6: plk(b, P8, L=0.5)
    elif n == "みんな":
        tick(b, True); fmb(b, "pulse" if i < 8 else "run"); plk(b, P16); ep(b, EP_A if i % 2 == 0 else EP_B); pad(b, 3)
        if i >= 8: saw(b, "x:4", 62 + (i - 8) // 2)
    elif n == "大合唱":
        j = i % 8
        tick(b, True); fmb(b, "run" if j % 2 == 1 else "pulse"); plk(b, P16, hi="F6"); pad(b, 3); saw(b, "x:1.5 x:1.5 x:1" if j % 2 == 0 else "x:1 x:1.5 x:1.5", 65 if i < 16 else 69)
        ep(b, EP_B if j % 2 == 0 else EP_A, 70)
        if j in (0, 1): LEAD.bar(b, K.mel(HUM[j], oct=5))                 # リードが鼻歌の節を上で重ねる
        if j in (4, 5): LEAD.bar(b, K.mel(HUM_B[j - 4], oct=5)) if i >= 8 else None
        if j in (3, 7): BELL.bar(b, "R:2 C6:0.5 F6:0.5 A6:1" if j == 3 else "R:2 E6:0.5 G6:0.5 C7:1")
    elif n == "おしずかに":
        tick(b)
        if i < 4: pad(b, 1); fmb(b, "one")
        if i in (2, 3): pass
        if i == 5: BELL.bar(b, "R:2 A5:0.5 C6:0.5 D6:1")
        if i == 6: BELL.bar(b, "C6:0.5 G5:1.5 R:2")
        if i == 7: TICK.bar(b, "C7:1 R:3")
    if n == "大合唱" or (n == "みんな" and i >= 8): SUB.bar(b, f"{nm(low(S.chords[b], 'F1'))}:3.5 R:0.5")

# ================= ドラム（少しずつ増える。大きいのは大合唱だけ）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "こごえ": D.set(b, "X.......X.......", "................", "................")
    elif n == "鼻歌1": D.set(b, "X.......X.......", "................", "..x...x...x...x.")
    elif n == "となり":
        D.set(b, "X...X...X...X...", "................", "..x...x...x...x."); KDR.bar(b, "R:1 B4:1 R:1 B4:1")
    elif n == "鼻歌2":
        D.set(b, "X...X...X...X...", "................", "..x...x...x...x."); KDR.bar(b, "R:1 B4:1 R:1 B4:1")
        if last: put_fill(D, b, "small")
    elif n in ("ひろがる", "鼻歌3"):
        D.set(b, "X...X...X...X...", "....x.......x..." if i % 4 != 3 else "....x.......x.x.", "x.x.x.x.x.x.x.x." if n == "ひろがる" else "x.xxx.xxx.xxx.xx"); KDR.bar(b, "R:1 B4:1 R:1 B4:1")
        if last and n == "鼻歌3": halt(D, b, 3)
    elif n == "司書さん": D.set(b, "X...............", "................", "................" if i < 6 else "x...x...x...x...")
    elif n == "みんな":
        if i < 8: D.set(b, "X...X...X...X...", "....x.......x...", "x.x.x.x.x.x.x.x."); KDR.bar(b, "R:1 B4:1 R:1 B4:1")
        elif i < 14: D.set(b, "X...X...X...X...", "x...x...x...x..." if i < 12 else "x.x.x.x.x.x.x.x.", "................")
        else: D.set(b, "X...X...X...X...", "xxxxxxxxxxxxxxxx" if i == 14 else "XXXXXXXXXXXX....", "................")
    elif n == "大合唱":
        vgroove(D, b, "beat8", ghosts=0.15, seed=b, k="X...X...X...X...", s="....X.......X..." if i % 4 != 3 else "....X.......X.X.", h="x.xxx.xxx.xxx.xx", vary=False)
        KDR.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 8 == 0: crash(D, b, "C2", 6 if i == 0 else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: halt(D, b, 3)

cym_swell(CYM, S.sc("大合唱")[0], 4, "E4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の12（11時）。テクノポップ（Kawaii future bass の音）。F・112。静かな図書館で、小さな鼻歌が人から人へうつっていく。"
          "くり返しのない積み上げの形で、8小節ごとに音が1つずつ増え、大きい場面は「大合唱」の1回だけ。合いことばの節（るるるるる）が主役。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"司書さん": -0.5, "大合唱": 0.5, "おしずかに": -0.5})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "プラック", mid=80, down=10, up=8, seed=3); humanize(path, "ガラスのエレピ", mid=82, down=8, up=8, seed=5)
set_parts(path, "ハイハット", swing16=0.1)
# v5 を測ると、出だしの「ページ」が −30〜−32dB で小さすぎた（次の場面は −18）→ 仕上げで持ち上げる。最後の「おしずかに」も少し
final_gain(path, {"ページ": 1.5, "こごえ": 1.0, "鼻歌1": 0.5, "みんな": -0.6, "大合唱": 1.6, "おしずかに": 5.0})   # 大合唱（−14.4）が みんな（−14.1）より小さかった → ただ1回の大きい場面をいちばん大きく
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "break": 10, "chorus": 22, "bridge": 6, "outro": 6}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    # 鼻歌が増える: 鼻歌2 は2人、鼻歌3 は3人、大合唱は全員（ハモリを足す）
    harmony(path, S, [("鼻歌2", 0, None, K), ("鼻歌3", 0, None, K), ("大合唱", 0, None, K)], vol=0.4)
    voice_by_scene(path, S, {"こごえ": "cute", "司書さん": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
