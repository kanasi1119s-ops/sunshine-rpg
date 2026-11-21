# vt3 11「水まきレインボー」Garden-Hose Rainbow（仮）— 明るい Kawaii future bass。4分の4・158。ニ長調 → 最後のサビから全音上のホ長調。
# 第3弾（0時〜24時の街）の 10時。
#
# v1（2026-11-21）: ゼロから作り直し。人間「11、Kawaii_future_bassで明るい曲を一から作り直しましょう」。
#   その前の「ひなたの猫会議」（`vt3_11c_catmeeting.py`・半分の速さでゆっくり）は不採用。さらに前は「洗濯日和のステップ」。
#   明るくするために変えたこと: 半分の速さをやめて、クラップを2拍め・4拍めに。キックははねる型。歌は8分で細かく動く。和音は 3・3・2 で刻む。
#
# コンセプト: 午前10時、庭の水まき。指で口をおさえると霧になり、日がさして小さな虹が出る。もっと大きい虹を作ろうと夢中になって、びしょぬれで笑う。
# 物語の出来事 → その時の音:
#   蛇口をひねる       → 水滴の音とプラックの駆け上がり（2小節だけ）
#   はじめのサビ       → いきなりサビを歌う。ベルとパッドとはねるベースだけ
#   しぶき（Aメロ）    → はねるベースとベル。クラップは2拍め・4拍め
#   ひかりがさす       → 和音が1小節ずつ上がる。ハイハットのロール。最後の1拍は無音
#   虹が出た（ドロップ）→ 歌なし。スーパーソウの和音が 3・3・2 で刻む。ベルが旋律。小節の終わりに、プラックが7音で駆け上がる（虹）。声のチョップ「き・ら」
#   サビ               → ベルと同じ旋律を歌う
#   びしょぬれ         → ドラムとベースが止まり、ベルと声だけ。最後の2拍は無音
#   最後の虹           → 全音上がる。ベルが合いことばの節を2回
#   しずく             → ベルと水滴の音で終わる
# この曲だけの物: 「虹」＝7音で駆け上がるプラック。出るたびに1音ずつ高い所から始まる。
# 合いことばの節（3・5・6・5・2）: 最後の虹で、ベルが2回鳴らす（アルバムの決まり）。
# 歌詞: 曲名は歌わない。「みずまき」「にじ」も使わない。声: キュート 1 種類。
from vocalo_lib import *

S = Song("11", "rainbow", "水まきレインボー（仮）", "Garden-Hose Rainbow", 158, 4, "D", "major", "Kawaii future bass（ボカロ）")
S.kit = "naked-x"; S.flags = S.flags + " --space room --space-wet 0.1"
K1, K2 = Key("D", "major"), Key("E", "major")


def up2(chs): return [tr_chord(c, 2) for c in chs]


VCH = ["Dmaj7", "Em7", "F#m7", "G", "Dmaj7", "Bm7", "Em7", "A"]
WCH = ["Em7", "F#m7", "G", "A", "Em7", "F#m7", "G", "A"]
DCH = ["D", "A", "Bm7", "F#m7", "G", "D", "Em7", "A"]
S.scene("蛇口をひねる", 2, "intro", ["G", "A"])
S.scene("はじめのサビ", 8, "chorus", DCH)
S.scene("しぶき", 16, "verse", VCH * 2)
S.scene("ひかりがさす", 8, "pre", WCH)
S.scene("虹が出た1", 8, "break", DCH)
S.scene("サビ1", 8, "chorus", DCH)
S.scene("もっと大きく", 8, "verse", VCH)
S.scene("ひかりがさす2", 8, "pre", WCH)
S.scene("虹が出た2", 8, "break", DCH)
S.scene("サビ2", 8, "chorus", DCH)
S.scene("びしょぬれ", 8, "bridge", ["Bm7", "G", "Em7", "A", "Bm7", "G", "Cmaj7", "B7"])
S.scene("サビ3", 8, "chorus", up2(DCH))
S.scene("最後の虹", 8, "break", up2(DCH))
S.scene("しずく", 6, "outro", up2(["G", "A", "Dmaj7", "Dmaj7", "Dmaj7", "Dmaj7"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("サビ3")[0]
S.drum_gain = {"kick": {"gainDb": -3}, "snare": {"gainDb": -2}}             # 測るとドラムだけが大きかった（シンセより 6〜10dB 上）


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

# ================= 歌（度数:長さ。oct 4 で 1 = D4。サビ3 からは 1 = E4）。8分で細かく、明るく =================
VA = ["3:0.5 5:0.5 5:1 6:0.5 5:1.5", "3:0.5 2:0.5 3:1.5 R:1.5", "4:0.5 6:0.5 6:1 1':0.5 6:1.5", "5:0.5 4:0.5 5:1.5 R:1.5",
      "5:1 1':0.5 1':0.5 2':1 1':1", "6:0.5 5:0.5 6:1.5 R:1.5", "6:0.5 5:0.5 4:0.5 3:0.5 2:1 3:1", "2:1 1:1.5 R:1.5"]
VW = ["3:1 3:0.5 5:1 5:0.5 6:1", "6:1 5:1.5 R:1.5", "4:1 4:0.5 6:1 6:0.5 1':1", "1':1 6:1.5 R:1.5", "5:1 5:0.5 1':1 1':0.5 2':1", "2':1 1':1.5 R:1.5", "1':1 2':1 1':1 2':1", "2':2 R:2"]
VC = ["5:0.5 5:0.5 1':1 6:1 5:1", "3:1 5:1.5 R:1.5", "6:0.5 6:0.5 2':1 1':1 6:1", "5:1 6:1.5 R:1.5", "5:0.5 5:0.5 1':1 2':1 1':1", "6:1 1':1.5 R:1.5", "6:0.5 5:0.5 3:1 2:1 3:1", "2:1 1:2 R:1"]
VB = ["3:1.5 2:0.5 1:1 2:1", "3:2.5 R:1.5", "5:1.5 3:0.5 2:1 3:1", "5:2.5 R:1.5", "6:1.5 5:0.5 6:1 1':1", "2':2.5 R:1.5"]
VO = ["1':1 6:1 5:1.5 3:0.5", "5:3 R:1"]
C1 = "きらきらはねて/そらにかかるよ/わたしがつくる/ちいさなはしを"
C2 = "きらきらわらう/しずくのなかに/さかさのまちが/ゆれてひかるよ"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("はじめのサビ", VC, C1)
put("しぶき", VA + VA, "あおいくだのさき/みずがとびだした/はなもくさのめも/せのびをしている/ゆびでおさえたら/しぶきがひろがる/ひかりがとおれば/なないろがうかぶ")
put("ひかりがさす", VW, "ひかりのほうへ/むきをかえたら/ほらみえてきた/せえのでね")
put("サビ1", VC, C1)
put("もっと大きく", VA, "まだまだおおきく/そらまでかけたい/くつもくつしたも/ぬれているけれど")
put("ひかりがさす2", VW, "もうすこしだけ/たかくあげたら/ほらつながるよ/せえのでね")
put("サビ2", VC, C2)
put("びしょぬれ", VB, "あめみたい/わらえるね/もういちど", bars=S.sc("びしょぬれ")[:6])
put("サビ3", VC, C1)
put("しずく", VO, "みえたかな", bars=S.sc("しずく")[:2])


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
def rainbow(b, k=0):
    """虹: 小節の後ろ半分で、プラックが7音で駆け上がる。k が大きいほど高い所から"""
    PLK.bar(b, arp16(S.chords[b], "........xxxxxxx-", tuple(range(k, k + 7)), lo="A4", hi="D7", short=0.25))


def claps(b, pat="R:1 B4:1 R:1 B4:1"): KFXT.bar(b, pat)


# ドロップ: 和音を 3・3・2 で刻む（小節ごとに形を変える）。ベースは1オクターブを行き来してはねる
GATE = ["x-.x-.x-x-.x-.x-", "x-.x-.x-x---....", "x-.x-.x-.x-.x-x-", "x-.x-.x-........", "x-.x-.x-x-.x-.x-", "x-x-..x-x-.x-...", "x-.x-.x-.x-.x-x-", "x-x-x-x-xxxx...."]
BSP = [("x-.o-.r-o-.r-.o-", "rorororo"[:6]), ("x-.o-.r-r---....", "rorr"), ("x-.o-.r-.o-.r-o-", "rororo"), ("x-.o-.r-..5-o-a-", "ror5oa"), ("x-.o-.r-o-.r-.o-", "rororo"), ("x-o-..r-o-.r-...", "rorro"[:5]),
       ("x-.o-.r-.o-.r-o-", "rororo"), ("x-x-x-x-........", "rr55")]
SOFT = ["x-....x-..x-....", "x-.x-...x-......", "x-....x-..x-.x-.", "x-.x-.x-........", "x-....x-..x-....", "x-.x-...x-..x-..", "x-....x-..x-.x-.", "x-x-x-x-........"]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）
HOP = [("X..X..X...X.....", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X..X......X..X..", "....X.......X..x", "x.xxx.x.x.x.x.xx")]            # ドロップ: はねるキック。クラップは2・4拍め
SKIP = [("X.....x...X.....", "................", "..x...x...x...x."), ("X.....x...X..x..", "................", "..x...x...x..xx.")]            # Aメロ: 軽く。ウラのハイハット


def fix(pat): return pat.replace("o", "x").replace("r", "x")


def drop(b, i, full=True, motif=False, n_th=0):
    """ドロップの1小節。full＝歌のないドロップ、False＝和音を短く切って歌を前に（サビ）"""
    saw(b, GATE[i] if full else SOFT[i], short=0.5 if not full else None); p, k = BSP[i]; bs(b, fix(p), k[:onsets(fix(p))], short=0.5)
    kk, s, h = HOP[i % 2]; D.set(b, kk, s, h); claps(b)
    if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if i == 7: fill_cresc(D, b, 2)
    if full:
        if i in (3, 7): rainbow(b, n_th + (0 if i == 3 else 2)); hat_roll(HATR, b, 1)
        if motif and i in (0, 1, 4, 5): bell_line(b, MOT[i % 2])
        elif i in (0, 1, 2, 4, 5, 6): bell_line(b, VC[i])                 # ベルが、あとで歌う旋律を先に鳴らす
    elif i % 2 == 1: BELL.bar(b, steps("..........x-x-x-", [top(b)[0], top(b)[1], top(b)[-1]]))


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; t = top(b)
    if n == "蛇口をひねる":                                             # 水滴 → プラックの駆け上がり → ベル
        if i == 0: FXT.bar(b, fx_bar((0, "drop", 1), (2, "awa", 1)))
        rainbow(b, i * 2); BELL.bar(b, steps("x-x-x---........", [t[0], t[1], t[-1]]))
        pad(b); SUB.bar(b, f"{N(root(b))}:4"); claps(b, "R:1 C5:1 R:1 C5:1")
        if i == 1: D.set(b, "................", "........x.x.xxxx", "................")
    elif n == "はじめのサビ":                                           # いきなり歌う。ベルとパッドとはねるベースだけ（スーパーソウはドロップまで取っておく）
        kk, s_, h = SKIP[i % 2]; D.set(b, kk, s_ if not last else "........x.x.xxxx", h); claps(b); pad(b)
        bs(b, "x-..x-x-..x-x---" if not odd else "x-..x-x-x-..x-x-", "rorro" if not odd else "roro5a", short=0.5, sub="x-----------....")
        if odd: BELL.bar(b, steps("..........x-x-x-", [t[0], t[1], t[-1]]))
        if i == 0: crash(D, b, "C2", 4)
    elif n in ("しぶき", "もっと大きく"):                               # はねるベースとベル。クラップは2拍め・4拍め
        two = n == "もっと大きく"; late = i >= 8 or two
        kk, s, h = SKIP[i % 2]; D.set(b, kk if not two else "X..X..x...X.....", s if not last else "........x.x.xxxx", h if not late else "x.x.x.x.x.x.x.x.")
        bs(b, "x-..x-x-..x-x---" if not odd else "x-..x-x-x-..x-x-", "rorro" if not odd else "roro5a", short=0.5, sub="x-----------....")
        claps(b, "R:1 C5:1 R:1 C5:1" if not late else "R:1 B4:1 R:1 B4:1"); pad(b)
        if odd: BELL.bar(b, steps("........x-x-x-x-", [t[0], t[1], t[2 % len(t)], t[-1]]))             # 歌の行の終わりに、ベルが答える
        if two and not odd: PLK.bar(b, arp16(S.chords[b], "..........xxxxx-", (0, 2, 1, 3, 4), lo="A4", hi="A6", short=0.25))
    elif n in ("ひかりがさす", "ひかりがさす2"):                         # 和音が1小節ずつ上がる。最後の1拍は無音
        saw(b, ["x-------........", "x-------x-------", "x---x---x---x---", "x---x---x-x-x-x-", "x-.x-.x-x-.x-.x-", "x-.x-.x-x-.x-.x-", "x-x-x-x-x-x-x-x-", "xxxxxxxxxxxx...."][i])
        SUB.bar(b, f"{N(root(b))}:{3 if last else 4}" + (" R:1" if last else "")); pad(b, "x---------------" if not last else "x-----------....")
        D.set(b, ("X.......x.......", "X...x...X...x...", "X...X...X...X...", "X...X...X...X...")[i // 2], "................" if i < 4 else ("....X.......X..." if i < 7 else "x.x.x.x.xxxx...."),
              "..x...x...x...x." if i < 4 else "x.x.x.x.x.x.x.x." if not last else "................")
        if i in (3, 5): hat_roll(HATR, b, 1)
        if last: FXT.bar(b, fx_bar((0, "up", 3)))
    elif n in ("虹が出た1", "虹が出た2"): drop(b, i, full=True, n_th=0 if n == "虹が出た1" else 1)
    elif n in ("サビ1", "サビ2", "サビ3"): drop(b, i, full=False)
    elif n == "最後の虹": drop(b, i, full=True, motif=True, n_th=2)
    elif n == "びしょぬれ":                                             # ドラムとベースが止まる。ベルと声だけ。最後の2拍は無音
        if i < 7:
            pad(b); BELL.bar(b, steps("x---....x-x-----" if not odd else "........x---x---", [t[0], t[-1], t[1]]))
            if i >= 4: SUB.bar(b, f"{N(root(b))}:4"); claps(b, "R:3 C5:1")
        else:
            v = sorted(voice(S.chords[b], 66, 3)); FXT.bar(b, fx_bar((0, "rev", 2)))
            for q in range(3): PAD[q].bar(b, f"{N(v[q])}:2 R:2")
            PLK.bar(b, arp16(S.chords[b], "xxxxxxx-........", tuple(range(7)), lo="A4", hi="D7", short=0.25))
    elif n == "しずく":                                                 # ベルと水滴の音で終わる
        if i < 5: pad(b, "x---------------")
        if i < 4: SUB.bar(b, f"{N(root(b))}:4"); claps(b, "R:1 C5:1 R:1 C5:1")
        if i in (2, 3): BELL.bar(b, steps("x-x-x---x-x-----" if i == 2 else "x---x-----------", [t[0], t[1], t[2 % len(t)], t[-1], t[1]]))
        if i == 3: rainbow(b, 2)
        if i == 4: BELL.bar(b, f"{t[-1]}:4"); FXT.bar(b, fx_bar((2, "drop", 1)))
        if i == 0: crash(D, b, "C2", 4)

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の11（10時）。明るい Kawaii future bass（158・ニ長調 → ホ長調）。庭の水まきで小さな虹を作る話。"
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
    bars = {}                                                             # ドロップの合間に、声のチョップ「き・ら」
    for name, sh in (("虹が出た1", 0), ("虹が出た2", 0), ("最後の虹", 2)):
        sc = S.sc(name); p = lambda x: nm(midi(x) + sh)
        for i in (3, 7): bars[sc[i]] = f"{p('A4')}:0.5:き {p('D5')}:0.5:ら R:0.5 {p('A4')}:0.5:き {p('D5')}:1:ら R:1"
    chops(path, S, bars, vol=0.3, pan=0.3)
    voice_by_scene(path, S, {}, default="cute")                           # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
