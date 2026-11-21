# vt3 11「雨あがり、とび石」Stepping Stones After the Rain（仮）— Kawaii future bass・ポップ。4分の4・100。ト長調 → 最後のサビから全音上のイ長調。約4分45秒。
# 第3弾（0時〜24時の街）の 10時。
#
# v1（2026-11-21）: 人間「10、11ともに緩急をつけるのと。5分ぐらいの曲で物語も作り直そう。」→ 物語の案から「11はb」。
#   楽器は、人間が「11の音は良いね。」と言った「水まきレインボー」と同じ組み合わせ。旋律・歌詞・和音・構成は新しく書いた。
#
# コンセプト: 10時に雨が上がる。しとしと → 晴れ間 → 水たまりを跳んで渡る → 通り雨 → 大きな晴れ。
# 緩急: 雨の場面はキックもベースもなし（ベルと細かいハイハットだけ）。晴れ間でスーパーソウが開く。山は3つで、だんだん大きく。通り雨で一度いちばん下まで落とす。
# 物語の出来事 → その時の音:
#   しとしと             → 水滴の音と、まばらな16分のハイハット。ベルがぽつぽつ
#   雨（Aメロ）          → ベルと低いベース（のばす）だけ。歌はゆっくり（2小節で1行）
#   雨2                  → パッドと指パッチンが加わる
#   晴れ間               → 和音が1小節ずつ上がる。最後の1拍は無音
#   サビ1（山1）         → スーパーソウの和音が 3・3・2 で刻む。ポップスのビート
#   とび石1              → 歌なし。ベースが「跳ぶ → 休む」をくり返す。跳ぶ回数が小節ごとに増える。プラックが駆け上がる
#   水たまり（Aメロ・速い）→ 1小節で1行。ベースがはねる
#   サビ2（山2）         → 16分のハイハットとベルの合いの手が加わる
#   通り雨               → いちばん下まで落とす。ベルとハイハットと声だけ → 最後の2拍は無音
#   大きな晴れ（山3）    → 全音上がる。16小節。いちばん大きい
#   最後のとび石         → ベルが合いことばの節を2回
#   しずく               → ベルと水滴で終わる
# この曲だけの物: 「とび石」。ベースが跳ぶ回数が 1・2・3・4 と増えていき、最後に大きく跳ぶ（オクターブ）。
# 歌詞: 曲名は歌わない。「あめあがり」「とびいし」も使わない。声: キュート 1 種類。
from vocalo_lib import *

S = Song("11", "rainwalk", "雨あがり、とび石（仮）", "Stepping Stones After the Rain", 100, 4, "G", "major", "Kawaii future bass・ポップ（ボカロ）")
S.kit = "naked-x"; S.flags = S.flags + " --space room --space-wet 0.1"
K1, K2 = Key("G", "major"), Key("A", "major")


def up2(chs): return [tr_chord(c, 2) for c in chs]


RCH = ["Gmaj7", "Em7", "Cmaj7", "D", "Gmaj7", "Em7", "Am7", "D7sus4"]          # 雨
WCH = ["Am7", "Bm7", "Cmaj7", "D"]                                         # 晴れ間
CCH = ["G", "Bm7", "C", "D", "Em7", "Bm7", "C", "D"]                        # サビ
TCH = ["C", "G", "D", "Em7", "C", "G", "D", "D"]                            # とび石
FCH = ["G", "D", "Em7", "C", "G", "D", "Am7", "D"]                          # 水たまり
S.scene("しとしと", 6, "intro", RCH[:4] + ["Gmaj7", "Gmaj7"])
S.scene("雨", 8, "verse", RCH)
S.scene("雨2", 8, "verse", RCH)
S.scene("晴れ間", 4, "pre", WCH)
S.scene("サビ1", 8, "chorus", CCH)
S.scene("とび石1", 8, "break", TCH)
S.scene("水たまり", 8, "verse", FCH)
S.scene("晴れ間2", 4, "pre", WCH)
S.scene("サビ2", 8, "chorus", CCH)
S.scene("とび石2", 8, "break", TCH)
S.scene("通り雨", 16, "bridge", RCH + RCH[:6] + ["Fmaj7", "E7"])
S.scene("大きな晴れ", 16, "chorus", up2(CCH + CCH))
S.scene("最後のとび石", 8, "break", up2(TCH))
S.scene("しずく", 8, "outro", up2(RCH[:4] + ["Gmaj7"] * 4))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("大きな晴れ")[0]


def KEY(b): return K2 if b >= MOD else K1


V = Voice(S, vol=0.16, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.055, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.6, fx=rack_supersaw()) for i in range(5)]
FMB = S.track("跳ぶシンセベース", "bass", patch="surgeBassAnalogBassImaged", volume=0.1, pan=0, duck=0.25)
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.055, pan=0, duck=0.4)
BELL = S.track("ベル", "lead", patch="surgeFantasyBell", volume=0.11, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
PLK = S.track("プラック", "lead", patch="kfbSquarePluck", volume=0.09, pan=-0.3, reverb=0.2, fx=rack_pluck())
PAD = [S.track(f"きらめくパッド{i + 1}", "pad", patch="surgePadSparkly", volume=0.035, pan=0.0, reverb=0.4, fx=[{"type": "widen", "amount": 1.4}]) for i in range(3)]
KFXT = S.track("クラップと指パッチン", "guitar", patch="kawaiiFx", volume=0.05, pan=0.05, reverb=0.15, modulate=False)
HATR = S.track("雨つぶ（細かいハイハット）", "guitar", patch="kawaiiFx", volume=0.045, pan=-0.2, reverb=0.2, modulate=False)
FXT = S.track("効果音（水滴・きらきら）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = G4。大きな晴れからは 1 = A4。高い所は 6 まで）=================
VR = ["3:1 2:0.5 3:1 5:0.5 3:1", "2:1.5 1:1.5 R:1", "3:1 2:0.5 3:1 5:0.5 6:1", "5:1.5 3:1.5 R:1", "6:1 5:0.5 6:1 5:0.5 3:1", "5:1.5 6:1.5 R:1", "5:1 3:0.5 2:1 1:0.5 2:1", "1:3 R:1"]     # 雨: ゆっくり
VF = ["1:0.5 3:0.25 3:0.25 5:0.5 3:0.5 2:0.25 1:0.25 2:0.5 R:1",
      "2:0.25 3:0.25 5:0.5 6:0.25 5:0.25 3:0.5 2:0.5 3:0.5 R:1",
      "3:0.5 5:0.25 6:0.25 5:0.5 6:0.5 5:0.25 3:0.25 5:0.5 R:1",
      "6:0.25 5:0.25 3:0.5 2:0.25 1:0.25 2:0.5 1:0.5 1:0.5 R:1",
      "1:0.5 1:0.25 3:0.25 5:0.5 3:0.5 3:0.25 2:0.25 3:0.5 R:1",
      "2:0.25 2:0.25 5:0.5 6:0.25 5:0.25 5:0.5 3:0.5 5:0.5 R:1",
      "6:0.5 6:0.25 5:0.25 3:0.5 5:0.5 6:0.25 5:0.25 3:0.5 R:1",
      "5:0.25 3:0.25 2:0.5 1:0.25 2:0.25 3:0.5 1:0.5 1:0.5 R:1"]                # 水たまり: 速い（1小節で1行）
VW = ["5,:0.75 1:0.25 2:0.5 3:0.5 3:0.25 5:0.25 3:0.5 R:1", "1:0.75 2:0.25 3:0.5 5:0.5 5:0.25 6:0.25 5:0.5 R:1", "2:0.75 3:0.25 5:0.5 6:0.5 6:0.25 5:0.25 6:0.5 R:1", "5:0.5 6:0.5 5:0.75 6:0.25 6:1 R:1"]
VC = ["3:0.5 3:1 5:0.5 3:1 2:1", "1:1 2:2 R:1", "3:0.5 3:1 5:0.5 6:1 5:1", "3:1 5:2 R:1", "6:0.5 6:1 5:0.5 3:1 5:1", "6:1 5:2 R:1", "3:0.5 2:1 1:0.5 2:1 3:1", "2:1.5 1:1.5 R:1"]
C1 = "みずたまりには/そらがおちてる/とびこえるたび/くもをまたぐよ"
C2 = "ながぐつのおと/しぶきがはねて/ひかりのつぶが/あしにからまる"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("雨", VR, "まどのむこうは/ぎんのすだれで/かさのはなたち/ゆれていたよ")
put("雨2", VR, "のきのしたでは/すずめもだまる/とけいのはりが/とおをさした")
put("晴れ間", VW, "くもがちぎれて/ひかりがさして/みちがかがやく/でかけよう")
put("サビ1", VC, C1)
put("水たまり", VF, "いちばんおおきな/うみをとびこえる/かかとがぬれても/わらえるならいい/むこうのかどまで/あといつつあるよ/かぞえてすすめば/まちがあたらしい")
put("晴れ間2", VW, "かぜがふいたら/しずくがおちて/せなかがぬれる/かまわない")
put("サビ2", VC, C2)
TB = S.sc("通り雨")
put("通り雨", VR, "またふりだした/だけどこんどは/あかるいあめだ/すぐにあがる", bars=TB[:8])
put("通り雨", ["3:1 5:1 6:1 R:1"], "ほらね", bars=TB[14:15])
put("大きな晴れ", VC + VC, C1 + "/" + C2)
put("しずく", VR[6:], "かさをとじた", bars=S.sc("しずく")[:2])


# ================= 伴奏 =================
def root(b): return low(S.chords[b], "E1")


def saw(b, pat, short=None):
    v = wide9(S.chords[b])
    for j in range(5): SAW[j].bar(b, steps(pat, [N(v[j])], short=short))


def pad(b, pat="x-------------.."):
    v = sorted(voice(S.chords[b], 66, 3))
    for j in range(3): PAD[j].bar(b, steps(pat, [N(v[j])]))


def bs(b, pat, kinds, short=None, sub="x-------x-------"):
    r = root(b); nx = low(S.chords[b + 1], "E1") if b + 1 < S.nb else r
    mp = {"r": r, "o": r + 12, "5": r + 7, "a": nx - 1 if nx > r else nx + 1}
    assert onsets(pat) == len(kinds), (pat, kinds)
    FMB.bar(b, steps(pat, [N(mp[c]) for c in kinds], short=short))
    if sub: SUB.bar(b, steps(sub, [N(r)]))


def top(b): return [N(x) for x in tones(S.chords[b], "D5", "D6")]
def bell_line(b, line): BELL.bar(b, KEY(b).mel(line, oct=5))
def run(b, k=0, pat="........xxxxxxx-"): PLK.bar(b, arp16(S.chords[b], pat, tuple(range(k, k + 7)), lo="A4", hi="D7", short=0.25))
def claps(b, pat="R:1 B4:1 R:1 B4:1"): KFXT.bar(b, pat)
def rain(b, k=0):
    """雨つぶ: まばらな16分のハイハット（小節ごとに場所が変わる）"""
    pat = ["x..x.x....x..x.x", ".x...x.x..x....x", "x.x....x.x...x..", "..x.x...x..x.x.."][k % 4]
    HATR.bar(b, " ".join(("C#5" if c == "x" else "R") + ":0.25" for c in pat))


GATE = ["x---x-.x-.x-x---", "x-.x-...x-.x-.x-", "x---x-.x-.x-x-x-", "x-x-..x-..x-....", "x---x-.x-.x-x---", "x-.x-...x-x-x-..", "x---x-.x-.x-x-x-", "x-x-x-x-xxxx...."]
BSK = [("x-x-..x-x-..x-x-", "roroor"), ("x-..x-x-..x-x---", "rroro"), ("x-x-..x-x-..x-x-", "rorro5"), ("x-x-..x-..x-....", "ro5a"), ("x-x-..x-x-..x-x-", "roroor"), ("x-..x-x-..x-x-..", "rroro"),
       ("x-x-..x-x-..x-x-", "ror5oa"), ("x-x-x-x-........", "rr55")]
# とび石: 跳ぶ回数が 1・2・3・4 と増える（跳ぶ＝短い音、あいだは休み）。最後は大きく跳ぶ
STONE = [("x...............", "r"), ("x.......x.......", "ro"), ("x.....x.....x...", "ror"), ("x...x...x...x...", "roro"), ("x.....x.x.....x.", "roro"), ("x...x.x...x.x...", "rorro"), ("x.x.x.x.x.x.x.x.", "rorororo"), ("x-------o-------".replace("o", "x"), "ro")]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）
POP = [("X......xX.......", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X...x....xX.....", "....X.......X..x", "x.x.xxx.x.x.x.xx")]
BIG = [("X.x...X...x..X..", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X.x......xX...x.", "....X.......X.xx", "x.x.x.x.x.x.x.x.")]
BIG16 = [("X.x...X...x..X..", "....X.......X...", "x.xxx.xxx.xxx.xx"), ("X.x......xX...x.", "....X.......X.xx", "x.xxx.xxx.xxx.x.")]


def chorus(b, i, size):
    """サビ。size 1＝山1、2＝山2（16分のハイハットとベル）、3＝山3（さらにパッドとプラック）"""
    saw(b, GATE[i % 8], short=0.5 if i % 8 != 7 else None); p, k = BSK[i % 8]; bs(b, p, k, short=0.5)
    kk, s_, h = (BIG if size == 1 else BIG16)[i % 2]; D.set(b, kk, s_, h); claps(b)
    if i % 8 == 0: crash(D, b, "C2", 4)
    if i % 8 == 7: fill_cresc(D, b, 1)
    if size >= 2 and i % 2 == 1: BELL.bar(b, steps("........x-x-x-x-", [top(b)[0], top(b)[1], top(b)[-1], top(b)[1]]))
    if size >= 3:
        pad(b)
        if i % 4 == 3: run(b, (i // 4) % 3, pat="..........xxxxx-")


def stones(b, i, k, motif=False):
    """とび石（8小節）: 歌なし。ベースが跳ぶ回数が増える。ベルが旋律、プラックが駆け上がる"""
    p, kinds = STONE[i]; bs(b, p, kinds, short=0.5 if i < 7 else None, sub="x-----------....")
    kk, s_, h = BIG[i % 2]; D.set(b, kk if i >= 2 else "X...............", s_, h if i >= 4 else "..x...x...x...x."); claps(b)
    if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if i >= 4: saw(b, "x-......x-......" if i < 6 else GATE[i], short=0.5)
    if motif and i in (0, 1, 4, 5): bell_line(b, MOT[i % 2])
    elif i in (0, 2, 4): bell_line(b, VC[i])
    if i in (1, 3, 5, 7): run(b, k + i // 2)
    if i == 7: fill_cresc(D, b, 1)


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; t = top(b)
    if n == "しとしと":                                                 # 水滴と雨つぶ。ベルがぽつぽつ
        rain(b, i)
        if i == 0: FXT.bar(b, fx_bar((0, "drop", 1)))
        if i >= 2: pad(b)                                                 # v2: 前奏が小さすぎた（−30dB。雨の Aメロより 8dB 下）ので、パッドを足して全体も上げた
        if i >= 1: BELL.bar(b, steps(["x-----------x---", "......x-....x---", "x-----x---x-----", "..x---x---x-x---", "x---x---x-x-x---"][i - 1], [t[q % len(t)] for q in (0, 2, 1, 0, 2)]))
    elif n in ("雨", "雨2", "通り雨"):                                   # キックもベースもなし。ベルと雨つぶと、のばす低い音
        if n == "通り雨" and i == 15:                                   # 最後の2拍は無音
            v = sorted(voice(S.chords[b], 66, 3)); FXT.bar(b, fx_bar((0, "rev", 2))); run(b, 0, pat="xxxxxxx-........")
            for q in range(3): PAD[q].bar(b, f"{N(v[q])}:2 R:2")
            continue
        rain(b, i)
        if n != "雨": SUB.bar(b, f"{N(root(b))}:2 R:2")                    # 雨（1番）は低い音もなし
        BELL.bar(b, steps("x-------....x-x-" if not odd else "........x-x-x---", [t[0], t[-1], t[1]]))
        if n != "雨": pad(b); claps(b, "R:3 C5:1")
        if n == "通り雨" and 8 <= i < 14 and not odd: PLK.bar(b, arp16(S.chords[b], "x-x-x-x-........", (0, 1, 2, 3), lo="A4", hi="A6", short=0.5))      # 雨が細くなっていく
        if n == "雨2" and i >= 4: D.set(b, "x...............", "................", "................")
    elif n in ("晴れ間", "晴れ間2"):                                     # 和音が1小節ずつ上がる。最後の1拍は無音
        saw(b, ["x-------x-------", "x---x---x---x---", "x-.x-.x-x-.x-.x-", "x-x-x-x-xxxx...."][i])
        SUB.bar(b, f"{N(root(b))}:{3 if last else 4}" + (" R:1" if last else "")); pad(b, "x---------------" if not last else "x-----------....")
        D.set(b, ("X.......X.......", "X...X...X...X...", "X...X...X...X...", "X...X...X.X.....")[i], "................" if i < 2 else ("....X.......X..." if i == 2 else "x.x.x.x.xxxx...."),
              "x.x.x.x.x.x.x.x." if not last else "................")
        if i == 2: hat_roll(HATR, b, 1)
        if last: FXT.bar(b, fx_bar((0, "up", 3)))
    elif n == "サビ1": chorus(b, i, 1)
    elif n == "サビ2": chorus(b, i, 2)
    elif n == "大きな晴れ": chorus(b, i, 3)
    elif n in ("とび石1", "とび石2"): stones(b, i, 0 if n == "とび石1" else 1)
    elif n == "最後のとび石": stones(b, i, 2, motif=True)
    elif n == "水たまり":                                               # 速い Aメロ。ベースがはねる。4拍めにベルが答える
        kk, s_, h = POP[i % 2]; D.set(b, kk, s_ if not last else "....X.......x.xx", h)
        bs(b, "x--x-..x-.x-..x-" if not odd else "x--x-..x-.x-x-x-", "rroro" if not odd else "rroo5a", short=0.5, sub="x-----------....")
        claps(b, "R:1 C5:1 R:1 C5:1"); pad(b); BELL.bar(b, steps("............x-x-" if not odd else "............xxx-", [t[0], t[-1]] if not odd else [t[0], t[1], t[-1]]))
    elif n == "しずく":                                                 # ベルと水滴で終わる
        if i < 6: rain(b, i); SUB.bar(b, f"{N(root(b))}:4"); pad(b, "x---------------")
        if i == 0: crash(D, b, "C2", 4)
        if 2 <= i < 6: BELL.bar(b, steps("x-------....x-x-" if not odd else "........x-x-x---", [t[0], t[-1], t[1]]))
        if i == 6: BELL.bar(b, f"{t[-1]}:4"); FXT.bar(b, fx_bar((2, "drop", 1)))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の11（10時）。Kawaii future bass・ポップ（100・ト長調 → イ長調）。雨が上がって、水たまりを跳んで渡る話。"
          "水滴と雨つぶ（まばらなハイハット）で始まる → キックもベースもない雨の Aメロ → 晴れ間でスーパーソウが開く → 山は3つ（だんだん大きく）→ "
          "ベースの跳ぶ回数が増える「とび石」→ 通り雨でいちばん下まで落として無音 → 全音上がって大きな晴れ → ベルと水滴で終わる。自作")
finish(S, LY, V, 0, flat=True)                                           # 山の大きさは、場面ごとの楽器の数で決める（曲全体の山は打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "跳ぶシンセベース", mid=92, down=12, up=10, seed=11); humanize(path, "ベル", mid=88, down=10, up=12, seed=4)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "bridge": 4, "outro": 4}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("大きな晴れ", 0, None, K2)], vol=0.34)
    bars = {}                                                             # とび石で跳ぶたびに、声のチョップ「ぴょ」
    for name, sh in (("とび石1", 0), ("とび石2", 0), ("最後のとび石", 2)):
        sc = S.sc(name); p = lambda q: nm(midi(q) + sh)
        bars[sc[3]] = f"{p('D5')}:0.5:ぴょ R:0.5 {p('D5')}:0.5:ぴょ R:0.5 {p('B4')}:0.5:ぴょ R:0.5 {p('D5')}:0.5:ぴょ R:0.5"
        bars[sc[6]] = f"{p('B4')}:0.5:ぴょ {p('D5')}:0.5:ぴょ {p('B4')}:0.5:ぴょ {p('D5')}:0.5:ぴょ {p('E5')}:1:ぴょ R:1"
    chops(path, S, bars, vol=0.3, pan=0.3)
    voice_by_scene(path, S, {}, default="cute")                           # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0; v["debreathAt"] = [[t + 0.02, 1.2] for t in [76.76, 209.33, 65.33, 52.77]]   # v2: 測って大きかった 4 か所
    save(path, js)
js = load(path); drum_center(js)
# 緩急: 雨の場面は全員が小さく弾く（山との差 8dB 以上）。速い Aメロも少しおさえる
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in (("しとしと", 0.95), ("雨", 0.85), ("雨2", 0.78), ("通り雨", 0.72), ("水たまり", 0.68), ("しずく", 0.75), ("サビ1", 0.88), ("とび石1", 0.88)):
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    p_["barGain"] = g[:S.nb]
save(path, js)
