# vt3 14「工事中ステップ」Under-Construction Step（仮）— K-POP（Kawaii future bass の音）。104・4/4。G短調 → 最後の「別のサビ」は A短調。
# 第3弾（0時〜24時の街）の 13時。表は docs/sound/vt3-plan.md。
#
# v2（2026-11-15）: ゼロから作り直し。人間の指示（2026-11-15）: 6ジャンル（この曲は K-POP）・構成を今までと変える・電子音は Kawaii future bass。v1 はアフロビーツだった。
#
# 構成（Aメロ→Bメロ→サビ の形を使わない。K-POP の形）:
#   かけ声 → サビ（いきなり）→ ダンスの場面（歌なし。金づちのリズムが主役）→ ラップ調の語り（半分の速さのビート）→ のぼる（4小節）→ サビ
#   → ダンスの場面 → 休けい（やわらかい声と鼻歌）→ 別のサビ（新しい節・A短調・長い音で歌い上げる）→ ダンスの場面で終わり、最後に全員の1打
#
# 物語: ビルの工事現場。ヘルメットをかぶって、右を見て左を見て、前進よし。クレーンが空をつかみ、ミキサー車が歌う。ドリルはベース、槌はドラム、足場はステージ。
#   昼の休けいに、だれかが口笛でふく、あの節。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: 「うるさい」と言われる音が町の音楽になる。「工事中」のままが好き ── 作っている今がいちばんいい。
#
# 曲を決める表:
#   旋律: サビ＝「と・ん・て・ん・か・ん」（同じ音を2つずつ、3段のぼる）→ 裏から入る5音の返事。ラップ調＝ほぼ1つの高さで16分を刻む8音 → 6音。
#         別のサビ＝2分と4分の長い音（3音ずつ）で歌い上げる
#   和音: サビ i → VI → III → VII。ラップ調 i → iv → V7。別のサビは A短調で i → VI → III → VII
#   ベース: サブベースの長い音と、FM のベースの 3・3・2。ラップ調は半分の速さで、1拍目と「2拍目の裏」だけ
#   この曲だけ: ①金づちのリズム（トン・テン・カン）が歌にもダンスの場面にも出る ②歌のないダンスの場面 ③ラップ調の語り ④最後に別のサビ
#   音色（Kawaii future bass）: kfbSub・kfbFmBass・kfbSawStab・kfbSupersaw・kfbSquarePluck・kfbGlocken（金づち）・kfbBrightBells・kfbSparklePad
from vt25_lib import *

S = Song("14", "construction", "工事中ステップ（仮）", "Under-Construction Step", 104, 4, "G", "minor", "K-POP（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.1"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.45
S.keepers = {}
K = Key("G", "minor")          # oct 4 で 1 = G4
KA = Key("A", "minor")         # 別のサビ（+2）

C8a = ["Gm", "Eb", "Bb", "F", "Gm", "Eb", "F", "D7"]
C8b = ["Gm", "Eb", "Bb", "F", "Gm", "Eb", "F", "Gm"]
DN = ["Gm", "Eb", "Bb", "F", "Gm", "Eb", "Bb", "F"]
RAP = ["Gm", "Gm", "Cm", "D7"] * 4
S.scene("かけ声", 4, "intro", ["Gm", "Gm", "Gm", "D7"])
S.scene("サビ1", 16, "chorus", C8a + C8b)
S.scene("ダンス1", 8, "break", DN)
S.scene("ラップ", 16, "verse", RAP)
S.scene("のぼる", 4, "pre", ["Eb", "F", "Gm", "D7"])
S.scene("サビ2", 16, "chorus", C8a + C8b)
S.scene("ダンス2", 8, "break", DN)
S.scene("休けい", 8, "bridge", ["Ebmaj7", "F", "Dm7", "Gm", "Ebmaj7", "F", "D7sus4", "E7"])
S.scene("別のサビ", 16, "chorus", ["Am", "F", "C", "G", "Am", "F", "C", "G", "Am", "F", "C", "G", "Am", "F", "G", "Am"])
S.scene("ダンス3", 10, "outro", ["Am", "F", "C", "G", "Am", "F", "C", "G", "Am", "Am"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
HAM = S.track("金づち（鉄琴の音）", "lead", patch="kfbGlocken", volume=0.085, pan=0.3, reverb=0.25)
FMB = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.09, pan=0, duck=0.25)
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.04, pan=0, duck=0.4)
STAB = [S.track(f"電子の短い和音{i + 1}", "lead", patch="kfbSawStab", volume=0.036, pan=0.45 - 0.45 * i, reverb=0.2, duck=0.4,
                fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}]) for i in range(3)]
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersaw", volume=0.03, pan=-0.5 + 0.5 * i, reverb=0.25, duck=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(3)]
PLK = S.track("プラック", "lead", patch="kfbSquarePluck", volume=0.05, pan=-0.35, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
PAD = [S.track(f"きらめくパッド{i + 1}", "lead", patch="kfbSparklePad", volume=0.034, pan=-0.4 + 0.4 * i, reverb=0.45) for i in range(3)]
BELL = S.track("ベル", "lead", patch="kfbBrightBells", volume=0.07, pan=0.25, reverb=0.4)
KDR = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
H1 = "1:0.5 1:0.5 3:0.5 3:0.5 5:0.5 5:1 R:0.5"          # と・ん・て・ん・か・ん
H2 = "3:0.5 3:0.5 5:0.5 5:0.5 7:0.5 7:1 R:0.5"
VC = [H1, "R:0.5 6:0.5 5:0.5 3:0.5 5:0.75 3:0.75 R:0.5", H2, "R:0.5 7:0.5 5:0.5 4:0.5 5:0.75 4:0.75 R:0.5",
      "5:1 7:0.5 5:0.5 3:1 5:1", "6:1.5 5:0.5 3:1 R:1", "4:0.5 4:0.5 5:0.5 7:0.5 7:1 5:1", "5:2 R:2",
      H1, "R:0.5 6:0.5 5:0.5 3:0.5 5:0.75 3:0.75 R:0.5", H2, "R:0.5 7:0.5 5:0.5 4:0.5 5:0.75 4:0.75 R:0.5",
      "5:1 7:0.5 5:0.5 3:1 5:1", "6:1.5 5:0.5 3:1 R:1", "7:0.5 7:0.5 5:0.5 4:0.5 5:1 7:1", "5:2 R:2"]
C1 = ("とんてんかん/ひびくおと/とんてんかん/そらたかく/なにもないばしょに/あしたをたてる/"
      "とんてんかん/はしらたち/とんてんかん/のびていく/きのうよりたかく/くもまでとどけ")
C2 = ("とんてんかん/うるさいと/とんてんかん/いわれても/これはおんがくだ/まちのたいこだ/"
      "とんてんかん/あせひかる/とんてんかん/こえあわせ/みんなのてのひら/みらいをつくる")
RA = "R:0.5 1:0.25 1:0.25 1:0.5 1:0.25 3:0.25 1:0.5 5,:0.5 1:1"
RB = "R:0.5 3:0.5 3:0.25 3:0.25 1:0.5 3:0.5 4:0.5 R:1"
RAc = "R:0.5 4:0.25 4:0.25 4:0.5 4:0.25 6:0.25 4:0.5 1:0.5 4:1"
RBd = "R:0.5 5:0.5 5:0.25 5:0.25 #7:0.5 5:0.5 2:0.5 R:1"
VRAP = [RA, RB, RAc, RBd] * 4
RT = ("へるめっとをかぶり/あんぜんよし/みぎをみてひだり/ぜんしんよし/くれーんがまわる/そらをつかむ/みきさーしゃうたう/ぐるぐるりと/"
      "どりるがべーすで/つちはどらむ/あしばがすてーじ/みんなおどれ/ひるのきゅうけいに/だれかがふく/くちぶえあのふし/またきこえた")
VP = ["6:1 6:0.5 5:0.5 3:1 5:1", "7:1 7:0.5 5:0.5 4:1 5:0.5 R:0.5", "5:0.5 5:0.5 7:0.5 7:0.5 5:1 3:1", "5:2 R:2"]
PT = "うるさいだけじゃないよ/みみをすませて"
VBR = ["R:2 5,:0.5 7,:0.5 1:1", "7,:0.5 4,:1.5 R:2", "R:1 5,:1 7,:1 2:1", "3:2 1:1 R:1",
       "R:2 5,:0.5 7,:0.5 1:1", "7,:0.5 4,:1.5 R:2", "R:1 5:1 4:1 5:1", "5:3 R:1"]
BT = "ららららら/ひとやすみ/ららららら/いこうか"
VF = ["1:2 3:1 5:1", "6:1.5 5:0.5 3:1 R:1", "3:2 5:1 5:1", "4:1.5 2:0.5 2:1 R:1",
      "1:1 3:1 5:1 6:1", "6:1.5 5:0.5 3:1 1:0.5 R:0.5", "3:1 5:1 5:2", "4:3 R:1",
      "1:2 3:1 5:1", "6:1.5 5:0.5 3:1 R:1", "3:2 5:1 5:1", "4:1.5 2:0.5 2:1 R:1",
      "1:1 3:1 5:1 6:1", "6:1.5 5:0.5 3:1 1:0.5 R:0.5", "2:1 4:1 5:2", "5:3 R:1"]
FT = ("たちあがるよ/あたらしいひ/こうじちゅうのまま/すすもう/できあがりは/まだとおくて/つくってるいまがね/だいすき")
LY = Lyrics(S)


def put(name, lines, text, key=K, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("サビ1", VC, C1)
put("ラップ", VRAP, RT)
put("のぼる", VP, PT)
put("サビ2", VC, C2)
put("休けい", VBR, BT)
put("別のサビ", VF, FT, key=KA)

# ================= 伴奏 =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def tr_line(line, semi):
    return " ".join(t if t.startswith("R") else f"{nm(midi(t.split(':')[0]) + semi)}:{t.split(':')[1]}" for t in line.split())


def ch3(tracks, b, pat, c=64):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): tracks[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def bass(b, style):
    ch = S.chords[b]; r = low(ch, "F1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "F1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); o = r + 12
    ap = t5 if rn == r else (rn - 2 if rn > r else rn + 2); N = nm
    pat = {"t332": f"{N(r)}:0.75 {N(r)}:0.75 {N(o)}:0.5 R:0.5 {N(r)}:0.5 {N(t5)}:0.5 {N(ap)}:0.5",
           "half": f"{N(r)}:1 R:0.5 {N(r)}:0.5 R:1.5 {N(o)}:0.25 {N(t5)}:0.25",              # ラップ調: 1拍目と2拍目の裏
           "dance": f"{N(r)}:0.5 R:0.25 {N(r)}:0.25 R:0.5 {N(o)}:0.5 {N(r)}:0.5 R:0.5 {N(t5)}:0.5 {N(ap)}:0.5",
           "long": f"{N(r)}:3.5 R:0.5", "hit": f"{N(r)}:1 R:3"}[style]
    FMB.bar(b, pat)


def sub(b, pat="x:1.5 R:0.5 x:1.5 R:0.5"):
    r = low(S.chords[b], "F1"); SUB.bar(b, pat.replace("x", nm(r)))


HAMMER = ["G5:0.5 G5:0.5 Bb5:0.5 Bb5:0.5 D6:0.5 D6:1 R:0.5", "R:0.5 Eb6:0.5 D6:0.5 Bb5:0.5 D6:0.75 Bb5:0.75 R:0.5",
          "Bb5:0.5 Bb5:0.5 D6:0.5 D6:0.5 F6:0.5 F6:1 R:0.5", "R:0.5 F6:0.5 D6:0.5 C6:0.5 D6:0.75 C6:0.75 R:0.5"]
ST_A = "x:0.75 x:0.75 x:0.5 R:1 x:0.5 x:0.5"
ST_B = "R:0.5 x:0.5 R:0.5 x:0.5 R:1 x:0.5 x:0.5"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "かけ声":
        HAM.bar(b, "G5:1 R:1 G5:1 R:1" if i < 2 else ("G5:0.5 G5:0.5 R:1 G5:0.5 G5:0.5 R:1" if i == 2 else "D6:0.5 D6:0.5 D6:0.5 D6:0.5 D6:0.25 D6:0.25 D6:0.25 D6:0.25 D6:1"))
        if i >= 2: bass(b, "hit")
    elif n in ("サビ1", "サビ2"):
        j = i % 8
        bass(b, "t332"); sub(b); ch3(SAW, b, "x:1.5 x:1.5 x:1" if j % 2 == 0 else "x:1 x:1.5 x:1.5", 65)
        if n == "サビ2" or i >= 8: ch3(PAD, b, "x:4", 70)
        if j in (0, 2): HAM.bar(b, "R:3.5 D6:0.25 D6:0.25")               # 「とんてんかん」のあとに金づちが2つ
        if j == 7: HAM.bar(b, HAMMER[0] if i < 8 else HAMMER[2])           # 歌が休む小節で金づちが歌う
        if n == "サビ2" and j in (1, 3): PLK.bar(b, "R:3 " + " ".join(f"{nm(m)}:0.25" for m in tones(root(b), "G5", "G6")[:4]))
    elif n.startswith("ダンス"):                                           # 歌なし。金づちの節と、電子の和音のシンコペーション
        semi = 2 if n == "ダンス3" else 0
        if n == "ダンス3" and i >= 8:
            if i == 8: ch3(STAB, b, "x:1 R:3", 72); bass(b, "hit"); sub(b, "x:1 R:3"); HAM.bar(b, "A6:1 R:3")       # 全員の1打
            continue
        HAM.bar(b, tr_line(HAMMER[i % 4], semi)); bass(b, "dance"); sub(b, "x:1 R:1.5 x:0.5 R:1")
        ch3(STAB, b, ST_A if i % 2 == 0 else ST_B, 67)
        if n != "ダンス1": ch3(SAW, b, "x:4", 62); PLK.bar(b, " ".join(f"{nm(m)}:0.25" for m in (tones(root(b), "G4", "G6") * 3)[:16]))
    elif n == "ラップ":                                                    # 半分の速さ。ベースと金づちの「カン」だけ → 後半からプラック
        bass(b, "half"); sub(b, "x:3 R:1")
        if i % 4 == 3: HAM.bar(b, "R:3 D6:0.5 D6:0.5")
        if i >= 8: PLK.bar(b, " ".join(f"{nm(m)}:0.5" for m in [tones(root(b), "G4", "G6")[q] for q in (0, 2, 3, 2, 4, 2, 3, 2)]))
        if i >= 12: ch3(PAD, b, "x:4", 67)
    elif n == "のぼる":
        ch3(PAD, b, "x:4", 67 + i); ch3(SAW, b, "x:4" if i < 3 else "x:2 R:2", 62 + i); bass(b, "long" if i < 3 else "hit"); sub(b, "x:3.5 R:0.5" if i < 3 else "x:1 R:3")
    elif n == "休けい":
        ch3(PAD, b, "x:4", 65); bass(b, "long")
        if i in (1, 5): BELL.bar(b, "R:2.5 D6:1.5")
        if i == 7: ch3(SAW, b, "x:3 R:1", 68)
    elif n == "別のサビ":
        j = i % 8
        bass(b, "t332"); sub(b); ch3(SAW, b, "x:1.5 x:1.5 x:1" if j % 2 == 0 else "x:1 x:1.5 x:1.5", 67); ch3(PAD, b, "x:4", 72)
        PLK.bar(b, " ".join(f"{nm(m)}:0.5" for m in [tones(root(b), "A4", "A6")[q] for q in (0, 2, 3, 4, 3, 2, 3, 2)]))
        if j in (3, 7): HAM.bar(b, "R:2 E6:0.5 E6:0.5 A6:1" if j == 3 else tr_line(HAMMER[0], 2))
        if i >= 8: BELL.bar(b, f"{nm(tones(root(b), 'A5', 'A6')[1])}:2 {nm(tones(root(b), 'A5', 'A6')[2])}:2")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "かけ声":
        if i >= 2: D.set(b, "X.......X.......", "................" if i == 2 else "X...X...X.X.XXXX", "................")
    elif n in ("サビ1", "サビ2", "別のサビ"):
        vgroove(D, b, "beat8", ghosts=0.2 if n != "別のサビ" else 0.3, seed=b, k="X..X..X...X....." if i % 2 == 0 else "X..X......X..X..", s="....X.......X..." if i % 4 != 3 else "....X.......X.X.", h="x.x.x.x.x.x.x.x." if n == "サビ1" else "x.xxx.xxx.xxx.xx", vary=False)
        KDR.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 8 == 0: crash(D, b, "C2", 6 if n == "別のサビ" else 4)
        if last: put_fill(D, b, "tomtrip")
        elif i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("ダンス"):
        if n == "ダンス3" and i >= 8:
            if i == 8: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)
            continue
        D.set(b, "X..X..X.X..X..X.", "....X.......X..." if i % 4 != 3 else "....X..X.X..X.XX", "x.x.x.x.x.x.x.x.")       # キックが金づちのように打つ
        KDR.bar(b, "R:1 B4:1 R:1 B4:0.5 B4:0.5" if i % 2 == 1 else "R:1 B4:1 R:1 B4:1")
        if i == 0: crash(D, b, "C2", 4)
    elif n == "ラップ":                                                    # 半分の速さ（スネアは3拍目）。ハイハットは16分と細かい刻み
        D.set(b, "X.....X........." if i % 2 == 0 else "X.....X...x.....", "........X.......", "x.x.x.xxx.x.xxxx" if i % 2 == 1 else "x.x.x.x.x.xxx.x.")
        if last: put_fill(D, b, "snare16")
    elif n == "のぼる":
        D.set(b, "X...X...X...X...", ["x...x...x...x...", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", "X...X..........."][i], "................")
        if i == 3: halt(D, b, 2); D.K[b] = "X...X..........."; D.S[b] = "X...X..........."
    elif n == "休けい":
        if i >= 4: D.set(b, "X...............", "........x......." if i < 7 else "....X...X.X.XXXX", "x...x...x...x..." if i < 7 else "................")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("別のサビ")[0], 4, "E4")
SIL.add(S.sc("のぼる")[-1], 2, 4); SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の14（13時）。K-POP（Kawaii future bass の音）。Gm→Am・104。工事現場の音が町の音楽になる。"
          "サビ「とんてんかん」から始まり、歌のないダンスの場面、ラップ調の語り、最後に別のサビ。金づちのリズム・サブベース・電子の和音。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"休けい": -0.5, "別のサビ": 0.5})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
set_parts(path, "ハイハット", swing16=0.1)
humanize(path, "プラック", mid=80, down=10, up=8, seed=3)
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 4, "pre": 12, "chorus": 20, "別のサビ": 26, "bridge": 6}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 8, None, K), ("別のサビ", 0, None, KA)], vol=0.36)
    # ダンスの場面のかけ声（テトの短い声）
    cb = {}
    for nme, semi in (("ダンス1", 0), ("ダンス2", 0), ("ダンス3", 2)):
        for q, b in enumerate(S.sc(nme)[:8]):
            if q % 2 == 1: cb[b] = f"R:3 {nm(74 + semi)}:0.25:え {nm(74 + semi)}:0.75:い"
    chops(path, S, cb, vol=0.3, pan=-0.2)
    voice_by_scene(path, S, {"ラップ": "cute", "休けい": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
