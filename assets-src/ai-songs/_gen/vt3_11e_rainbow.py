# vt3 11「水まきレインボー」Garden-Hose Rainbow（仮）— ポップな Kawaii future bass。4分の4・100。ニ長調 → 最後のサビから全音上のホ長調。
# 第3弾（0時〜24時の街）の 10時。
#
# v2（2026-11-21）: 人間「11はテンポを100ぐらいでもっとポップな感じにしよう」「11の音は良いね。」
#   → 楽器（音）は v1（`vt3_11d_rainbow.py`・158）のまま。テンポ 100 に合わせて、歌・リズム・構成を書き直した。
#   ポップにするために: キックは1・3拍めの近く、スネアとクラップは2・4拍め。Aメロは1小節に1行（8分と16分）。サビは 3・3・2 のはねる入りで、同じ形を3回くり返して覚えやすく。
#
# コンセプト: 午前10時、庭の水まき。指で口をおさえると霧になり、日がさして小さな虹が出る。夢中になって、びしょぬれで笑う。
# 物語の出来事 → その時の音:
#   蛇口をひねる       → 水滴の音とプラックの駆け上がり（2小節）
#   しぶき（Aメロ）    → はねるベースとベル。行の終わりにベルが答える
#   ひかりがさす       → 和音が1小節ずつ上がる。最後の1拍は無音
#   サビ               → スーパーソウの和音が 3・3・2 で刻む。歌がフック
#   虹が出た（サビのあと）→ 歌なし。ベルが旋律、プラックが7音で駆け上がる（虹）。声のチョップ「き・ら」
#   びしょぬれ         → ドラムとベースが止まり、ベルと声だけ。最後の2拍は無音
#   最後のサビ         → 全音上がる。最後の虹で、ベルが合いことばの節を2回
#   しずく             → ベルと水滴の音で終わる
# この曲だけの物: 「虹」＝7音で駆け上がるプラック。出るたびに高い所から始まる。
# 歌詞: 曲名は歌わない。「みずまき」「にじ」も使わない。声: キュート 1 種類。
from vocalo_lib import *

S = Song("11", "rainbow", "水まきレインボー（仮）", "Garden-Hose Rainbow", 100, 4, "D", "major", "Kawaii future bass・ポップ（ボカロ）")
S.kit = "naked-x"; S.flags = S.flags + " --space room --space-wet 0.1"
K1, K2 = Key("D", "major"), Key("E", "major")


def up2(chs): return [tr_chord(c, 2) for c in chs]


VCH = ["Dmaj7", "Em7", "F#m7", "G", "Dmaj7", "Bm7", "Em7", "A"]
WCH = ["Em7", "F#m7", "G", "A"]
DCH = ["D", "A", "Bm7", "F#m7", "G", "D", "Em7", "A"]
RCH = ["G", "A", "Bm7", "A"]
S.scene("蛇口をひねる", 2, "intro", ["G", "A"])
S.scene("しぶき", 8, "verse", VCH)
S.scene("ひかりがさす", 4, "pre", WCH)
S.scene("サビ1", 8, "chorus", DCH)
S.scene("虹が出た1", 4, "break", RCH)
S.scene("もっと大きく", 4, "verse", VCH[:4])
S.scene("ひかりがさす2", 4, "pre", WCH)
S.scene("サビ2", 8, "chorus", DCH)
S.scene("虹が出た2", 4, "break", RCH)
S.scene("びしょぬれ", 4, "bridge", ["Bm7", "G", "Cmaj7", "B7"])
S.scene("サビ3", 16, "chorus", up2(DCH + DCH))
S.scene("最後の虹", 4, "break", up2(RCH))
S.scene("しずく", 3, "outro", up2(["G", "A", "Dmaj7"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("サビ3")[0]


def KEY(b): return K2 if b >= MOD else K1


V = Voice(S, vol=0.16, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.055, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.6, fx=rack_supersaw()) for i in range(5)]
FMB = S.track("はねるシンセベース", "bass", patch="surgeBassAnalogBassImaged", volume=0.1, pan=0, duck=0.25)
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.055, pan=0, duck=0.4)
BELL = S.track("ベル", "lead", patch="surgeFantasyBell", volume=0.11, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
PLK = S.track("プラック（虹）", "lead", patch="kfbSquarePluck", volume=0.09, pan=-0.3, reverb=0.2, fx=rack_pluck())
PAD = [S.track(f"きらめくパッド{i + 1}", "pad", patch="surgePadSparkly", volume=0.035, pan=0.0, reverb=0.4, fx=[{"type": "widen", "amount": 1.4}]) for i in range(3)]
KFXT = S.track("クラップと指パッチン", "guitar", patch="kawaiiFx", volume=0.05, pan=0.05, reverb=0.15, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
FXT = S.track("効果音（水滴・きらきら）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = D4。サビ3 からは 1 = E4）=================
# Aメロ: 1小節に1行（8音・3拍ぶん歌って1拍休む）
VA = ["3:0.5 5:0.5 5:0.25 6:0.25 5:0.5 3:0.5 2:0.25 3:0.25 R:1", "4:0.5 6:0.5 6:0.25 1':0.25 6:0.5 5:0.5 4:0.25 5:0.25 R:1",
      "5:0.5 1':0.5 1':0.25 2':0.25 1':0.5 6:0.5 5:0.25 6:0.25 R:1", "6:0.5 5:0.5 4:0.25 3:0.25 2:0.5 3:0.5 2:0.25 1:0.25 R:1",
      "3:0.25 3:0.25 5:0.5 6:0.5 5:0.25 5:0.25 3:0.5 5:0.5 R:1", "4:0.25 4:0.25 6:0.5 1':0.5 6:0.25 6:0.25 5:0.5 6:0.5 R:1",
      "1':0.5 2':0.5 1':0.25 6:0.25 5:0.5 6:0.5 1':0.25 6:0.25 R:1", "5:0.5 4:0.5 3:0.25 2:0.25 3:0.5 2:0.5 1:0.25 1:0.25 R:1"]
VW = ["3:0.5 3:0.5 5:0.5 5:0.5 6:0.5 6:0.25 5:0.25 R:1", "4:0.5 4:0.5 6:0.5 6:0.5 1':0.5 1':0.25 6:0.25 R:1", "5:0.5 5:0.5 1':0.5 1':0.5 2':0.5 2':0.25 1':0.25 R:1", "1':0.5 2':0.5 1':0.5 2':0.5 2':1 R:1"]
VC = ["5:0.75 5:0.75 1':0.5 6:1 5:1", "3:0.75 5:2.25 R:1", "6:0.75 6:0.75 2':0.5 1':1 6:1", "5:0.75 6:2.25 R:1", "5:0.75 5:0.75 1':0.5 2':1 1':1", "6:0.75 1':2.25 R:1", "6:0.5 5:0.5 3:1 2:1 3:1", "2:1 1:2 R:1"]
VB = ["3:0.5 2:0.5 1:0.5 2:0.5 3:1 R:1", "5:0.5 3:0.5 2:0.5 3:0.5 5:1 R:1", "6:0.5 5:0.5 6:0.5 1':0.5 2':1 R:1"]
VO = ["1':0.5 6:0.5 5:0.5 3:0.5 5:1 R:1"]
C1 = "きらきらはねて/そらにかかるよ/わたしがつくる/ちいさなはしを"
C2 = "きらきらわらう/しずくのなかに/さかさのまちが/ゆれてひかるよ"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("しぶき", VA, "あおいくだのさき/みずがとびだした/はなもくさのめも/せのびをしている/ゆびでおさえたら/しぶきがひろがる/ひかりがとおれば/なないろがうかぶ")
put("ひかりがさす", VW, "ひかりのほうへ/むきをかえたら/ほらみえてきた/せえのでね")
put("サビ1", VC, C1)
put("もっと大きく", VA[4:], "まだまだおおきく/そらまでかけたい/くつもくつしたも/ぬれているけれど")
put("ひかりがさす2", VW, "もうすこしだけ/たかくあげたら/ほらつながるよ/せえのでね")
put("サビ2", VC, C2)
put("びしょぬれ", VB, "あめみたい/わらえるね/もういちど", bars=S.sc("びしょぬれ")[:3])
put("サビ3", VC + VC, C1 + "/" + C2)
put("しずく", VO, "みえたかな", bars=S.sc("しずく")[:1])


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
def rainbow(b, k=0, pat="........xxxxxxx-"):
    """虹: プラックが7音で駆け上がる。k が大きいほど高い所から"""
    PLK.bar(b, arp16(S.chords[b], pat, tuple(range(k, k + 7)), lo="A4", hi="D7", short=0.25))


def claps(b, pat="R:1 B4:1 R:1 B4:1"): KFXT.bar(b, pat)


GATE = ["x-.x-.x-x-.x-.x-", "x-.x-.x-x---x-..", "x-.x-.x-.x-.x-x-", "x-.x-.x-x-x-....", "x-.x-.x-x-.x-.x-", "x-x-..x-x-.x-.x-", "x-.x-.x-.x-.x-x-", "x-x-x-x-xxxx...."]
BSK = [("x-.x-.x-x-.x-.x-", "rorror"), ("x-.x-.x-x---x-..", "roror"), ("x-.x-.x-.x-.x-x-", "rororo"), ("x-.x-.x-x-x-....", "ror5a"), ("x-.x-.x-x-.x-.x-", "rorror"), ("x-x-..x-x-.x-.x-", "rorror"),
       ("x-.x-.x-.x-.x-x-", "rororo"), ("x-x-x-x-........", "rr55")]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）
POP = [("X.....x.X.......", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X.....x.X..x....", "....X.......X..x", "x.x.xxx.x.x.x.xx")]            # Aメロ: ふつうのポップスの8分
BIG = [("X..x..x.X.....x.", "....X.......X...", "x.xxx.xxx.xxx.xx"), ("X..x....X..x..x.", "....X.......X.xx", "x.xxx.xxx.xxx.x.")]            # サビ: キックがはねる。16分のハイハット


def chorus(b, i):
    saw(b, GATE[i % 8], short=0.5 if i % 8 != 7 else None); p, k = BSK[i % 8]; bs(b, p, k, short=0.5)
    kk, s_, h = BIG[i % 2]; D.set(b, kk, s_, h); claps(b)
    if i % 8 == 0: crash(D, b, "C2", 4)
    if i % 8 == 7: fill_cresc(D, b, 1)
    if i % 2 == 1: BELL.bar(b, steps("........x-x-x-x-", [top(b)[0], top(b)[1], top(b)[-1], top(b)[1]]))        # 歌がのばす後ろで、ベルが答える


def post(b, i, k, motif=False):
    """サビのあと（4小節）: 歌なし。ベルが旋律、プラックの虹、声のチョップ"""
    saw(b, GATE[(i * 2) % 8]); p, kk_ = BSK[(i * 2) % 8]; bs(b, p, kk_, short=0.5)
    kk, s_, h = BIG[i % 2]; D.set(b, kk, s_, h); claps(b)
    if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if motif and i in (0, 1): bell_line(b, MOT[i])
    elif motif and i == 2: bell_line(b, MOT[0])
    elif i in (0, 2): bell_line(b, VC[i])
    if i in (1, 3): rainbow(b, k + (0 if i == 1 else 2)); hat_roll(HATR, b, 1)
    if i == 3: fill_cresc(D, b, 1)


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; t = top(b)
    if n == "蛇口をひねる":                                             # 水滴とプラックの駆け上がり
        if i == 0: FXT.bar(b, fx_bar((0, "drop", 1), (2, "awa", 1)))
        rainbow(b, i * 2, pat="....xxxxxxx-...." if i == 0 else "xxxxxxx-........"); BELL.bar(b, steps("x-x-............" if i == 0 else "........x-x-x---", [t[0], t[1], t[-1]]))
        pad(b); SUB.bar(b, f"{N(root(b))}:4"); claps(b, "R:1 C5:1 R:1 C5:1")
        if i == 1: D.set(b, "................", "........x.x.xxxx", "................")
    elif n in ("しぶき", "もっと大きく"):                               # はねるベースとベル。行の終わり（4拍め）にベルが答える
        two = n == "もっと大きく"; late = i >= 4 or two
        kk, s_, h = POP[i % 2]; D.set(b, kk, s_ if late else "................", h if not last else h[:12] + "....")
        bs(b, "x-..x-x-..x-x---" if not odd else "x-..x-x-x-..x-x-", "rorro" if not odd else "roro5a", short=0.5, sub="x-----------....")
        claps(b, "R:1 C5:1 R:1 C5:1"); pad(b)
        BELL.bar(b, steps("............x-x-" if not odd else "............xxx-", [t[0], t[-1]] if not odd else [t[0], t[1], t[-1]]))
        if two: saw(b, "x-......x-......", short=0.5)
        if last: D.set(b, kk, "....X.......x.xx", h)
    elif n in ("ひかりがさす", "ひかりがさす2"):                         # 和音が1小節ずつ上がる。最後の1拍は無音
        saw(b, ["x-------x-------", "x---x---x---x---", "x-.x-.x-x-.x-.x-", "x-x-x-x-xxxx...."][i])
        SUB.bar(b, f"{N(root(b))}:{3 if last else 4}" + (" R:1" if last else "")); pad(b, "x---------------" if not last else "x-----------....")
        D.set(b, ("X.......X.......", "X...X...X...X...", "X...X...X...X...", "X...X...X.X.....")[i], "................" if i < 2 else ("....X.......X..." if i == 2 else "x.x.x.x.xxxx...."),
              "x.x.x.x.x.x.x.x." if not last else "................")
        if i == 2: hat_roll(HATR, b, 1)
        if last: FXT.bar(b, fx_bar((0, "up", 3)))
    elif n in ("サビ1", "サビ2", "サビ3"): chorus(b, i)
    elif n in ("虹が出た1", "虹が出た2"): post(b, i, 0 if n == "虹が出た1" else 1)
    elif n == "最後の虹": post(b, i, 2, motif=True)
    elif n == "びしょぬれ":                                             # ドラムとベースが止まる。ベルと声だけ。最後の2拍は無音
        if i < 3:
            pad(b); BELL.bar(b, steps("............x-x-", [t[0], t[-1]])); SUB.bar(b, f"{N(root(b))}:4"); claps(b, "R:3 C5:1")
        else:
            v = sorted(voice(S.chords[b], 66, 3)); FXT.bar(b, fx_bar((0, "rev", 2)))
            for q in range(3): PAD[q].bar(b, f"{N(v[q])}:2 R:2")
            rainbow(b, 0, pat="xxxxxxx-........")
    elif n == "しずく":                                                 # ベルと水滴の音で終わる
        pad(b, "x---------------"); SUB.bar(b, f"{N(root(b))}:4")
        if i == 0: crash(D, b, "C2", 4); BELL.bar(b, steps("............x-x-", [t[0], t[-1]]))
        if i == 1: rainbow(b, 2)
        if i == 2: BELL.bar(b, f"{t[-1]}:4"); FXT.bar(b, fx_bar((2, "drop", 1)))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の11（10時）。ポップな Kawaii future bass（100・ニ長調 → ホ長調）。庭の水まきで小さな虹を作る話。"
          "水滴とプラックの駆け上がりで始まる → はねるベースとベルの Aメロ → 和音が上がって無音 → 3・3・2 で刻むスーパーソウのドロップと、7音で駆け上がるプラック（虹）→ サビ → "
          "止まって無音 → 全音上がって最後のサビとドロップ → ベルと水滴で終わる。自作")
finish(S, LY, V, 0, flat=True)                                           # どのドロップも同じ強さで鳴らす（曲全体の山を打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "はねるシンセベース", mid=92, down=12, up=10, seed=11); humanize(path, "ベル", mid=88, down=10, up=12, seed=4)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "bridge": 8, "outro": 8}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("サビ3", 0, None, K2)], vol=0.34)
    bars = {}                                                             # サビのあとの合間に、声のチョップ「き・ら」
    for name, sh in (("虹が出た1", 0), ("虹が出た2", 0), ("最後の虹", 2)):
        sc = S.sc(name); p = lambda q: nm(midi(q) + sh)
        for i in (1, 3): bars[sc[i]] = f"{p('A4')}:0.5:き {p('D5')}:0.5:ら {p('A4')}:0.5:き {p('D5')}:0.5:ら R:2"
    chops(path, S, bars, vol=0.3, pan=0.3)
    voice_by_scene(path, S, {}, default="cute")                           # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
