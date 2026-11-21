# vt3 11「ひなたの猫会議」Sunny-Spot Assembly（仮）— Kawaii future bass。4分の4・150（半分の速さで感じる）。変ホ長調 → 最後のサビから全音上のヘ長調。
# 第3弾（0時〜24時の街）の 10時。
#
# v1（2026-11-21）: 曲名も物語も新しくして、ゼロから作った。前の 11 は「洗濯日和のステップ」（ケルトのジグ `vt3_11_laundry.py`、Kawaii future bass の試し書き `vt3_11b_laundry.py`）。
#   人間の指示: 「曲自体初めから1011は作り直そう。KPOPとKawaii_future_bassで。全く新しい曲で」→ 聞くと「曲名も物語も新しく」（2026-11-21）。
#
# コンセプト: 午前10時。駐車場のひなたに1匹ずつ集まって、何も決めずに解散する。
# ジャンル: Kawaii future bass。決まりごと（出どころは docs/sound/vt3-remake-plan.md）:
#   ・キックにあわせて沈むスーパーソウの和音がドロップの主役 ・ベルやプラックのかわいい旋律 ・声のチョップのかけ合い ・半分の速さのドラム
#
# 物語の出来事 → その時の音:
#   1匹め                → ベル1つと低いベースだけ
#   集まってくる         → 4小節ごとに楽器が1つ増える（プラック → パッド → ハイハットとキック）
#   ぽかぽか（のびの前） → 和音が上がる。最後の1拍は無音
#   のび（ドロップ）     → スーパーソウの和音がゆっくりふくらんで沈む。声のチョップ「にゃ」が左右でかけ合う
#   サビ                 → 和音を短く切って歌を前に。プラックの駆け上がりが合いの手
#   雲がかかる           → ドラムとベースが止まり、ベルと声だけ。最後の2拍は無音
#   サビ3・最後ののび    → 全音上がる。ベルが合いことばの節を2回
#   解散                 → 入った順の逆に、楽器が1つずつ抜ける。最後は「にゃ」ひとこと
# この曲だけの物: 集まった数だけ音が増えて、帰る数だけ減る。「にゃ」のかけ合い。
# 合いことばの節（3・5・6・5・2）: 最後ののびで、ベルが2回鳴らす（アルバムの決まり）。
# 歌詞: 曲名は歌わない。「ねこ」「かいぎ」も使わない。声: キュート 1 種類。
from vocalo_lib import *

S = Song("11", "catmeeting", "ひなたの猫会議（仮）", "Sunny-Spot Assembly", 150, 4, "Eb", "major", "Kawaii future bass（ボカロ）")
S.kit = "naked-x"; S.flags = S.flags + " --space room --space-wet 0.1"
K1, K2 = Key("Eb", "major"), Key("F", "major")


def up2(chs): return [tr_chord(c, 2) for c in chs]


VCH = ["Ebmaj7", "Gm7", "Abmaj7", "Bb", "Cm7", "Gm7", "Abmaj7", "Bb7sus4"]
WCH = ["Abmaj7", "Bb", "Gm7", "Cm7", "Fm7", "Fm7", "Bb7sus4", "Bb"]
DCH = ["Abmaj7", "Gm7", "Fm7", "Bb", "Abmaj7", "Gm7", "Cm7", "Bb7sus4"]
S.scene("1匹め", 4, "intro", ["Ebmaj7", "Ebmaj7", "Abmaj7", "Bb7sus4"])
S.scene("集まってくる", 16, "verse", VCH * 2)
S.scene("ぽかぽか", 8, "pre", WCH)
S.scene("のび1", 8, "break", DCH)
S.scene("サビ1", 8, "chorus", DCH)
S.scene("議題はない", 16, "verse", VCH * 2)
S.scene("ぽかぽか2", 8, "pre", WCH)
S.scene("のび2", 8, "break", DCH)
S.scene("サビ2", 8, "chorus", DCH)
S.scene("雲がかかる", 8, "bridge", ["Cm7", "Abmaj7", "Fm7", "Bb", "Cm7", "Abmaj7", "Dbmaj7", "C7"])
S.scene("サビ3", 8, "chorus", up2(DCH))
S.scene("最後ののび", 8, "break", up2(DCH))
S.scene("解散", 8, "outro", up2(["Abmaj7", "Gm7", "Fm7", "Bb", "Ebmaj7", "Ebmaj7", "Ebmaj7", "Ebmaj7"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("サビ3")[0]


def KEY(b): return K2 if b >= MOD else K1


V = Voice(S, vol=0.16, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.03, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.7, fx=rack_supersaw()) for i in range(5)]
FMB = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.09, pan=0, duck=0.25, fx=rack_bass())
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.06, pan=0, duck=0.4)
BELL = S.track("ベル", "lead", patch="kfbMusicBox", volume=0.09, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
PLK = S.track("プラック", "lead", patch="surgeNicePluck", volume=0.06, pan=-0.3, reverb=0.2, fx=rack_pluck())
PAD = [S.track(f"やわらかいパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.1, pan=0.0, reverb=0.4, fx=[{"type": "boost", "gain": 7}, {"type": "widen", "amount": 1.4}]) for i in range(3)]
KFXT = S.track("クラップ", "guitar", patch="kawaiiFx", volume=0.08, pan=0.05, reverb=0.15, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
FXT = S.track("効果音（きらきら）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = Eb4。サビ3 からは 1 = F4）。ゆっくり大きく動く =================
VA = ["1:1 3:0.5 5:1.5 3:0.5 5:0.5", "6:1.5 5:1 R:1.5", "2:1 4:0.5 6:1.5 4:0.5 6:0.5", "5:1.5 3:1 R:1.5",
      "3:1 5:0.5 1':1.5 7:0.5 6:0.5", "5:1.5 6:1 R:1.5", "4:1 3:1 2:1 7,:1", "1:2.5 R:1.5"]
VW = ["5:1 6:1 1':1.5 6:0.5", "5:2.5 R:1.5", "6:1 1':1 2':1.5 1':0.5", "6:2.5 R:1.5", "5:1 1':1 2':1 1':1", "2':3 R:1", "R:4", "R:4"]
VC = ["5:1.5 1':1.5 7:1", "6:0.5 5:2.5 R:1", "4:1.5 6:1.5 5:1", "3:0.5 5:2.5 R:1", "6:1.5 2':1.5 1':1", "7:0.5 1':2.5 R:1", "6:1 5:0.5 3:1.5 2:1", "1:3 R:1"]
VB = ["3:1 2:1 1:1.5 2:0.5", "3:2.5 R:1.5", "5:1 3:1 2:1.5 3:0.5", "5:2.5 R:1.5", "6:1 5:1 6:1.5 1':0.5", "2':2.5 R:1.5"]
VO = ["3:1 5:1 6:1.5 5:0.5", "3:2.5 R:1.5"]
C1 = "なにもない/それがいい/おひさまの/したでいい"
C2 = "きめないで/ここにいる/まるいせな/ならべてる"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("集まってくる", VA + VA, "ひなたのすみに/ひとりめがくる/あくびをひとつ/まるくなる/へいのうえから/ふたりめがくる/ひげをそろえて/すわりこむ")
put("ぽかぽか", VW, "ぽかぽかと/ねむくなる/せをのばす")
put("サビ1", VC, C1)
put("議題はない", VA + VA, "けさのぎだいは/とくにないけど/かぜのにおいを/たしかめる/だれもなかずに/みみだけうごく/それでぜんぶが/つたわるの")
put("ぽかぽか2", VW, "ぬくもりが/しみてくる/もういちど")
put("サビ2", VC, C2)
put("雲がかかる", VB, "くもがきて/ひえてきた/でもすぐに", bars=S.sc("雲がかかる")[:6])
put("サビ3", VC, C1)
put("解散", VO, "またあした", bars=S.sc("解散")[:2])


# ================= 伴奏 =================
def root(b): return low(S.chords[b], "F1")


def saw(b, pat, short=None):
    v = wide9(S.chords[b])
    for j in range(5): SAW[j].bar(b, steps(pat, [N(v[j])], short=short))


def pad(b, pat="x-------------.."):
    v = sorted(voice(S.chords[b], 64, 3))
    for j in range(3): PAD[j].bar(b, steps(pat, [N(v[j])]))


def bs(b, pat, kinds, short=None, sub="x-------x-------"):
    r = root(b); nx = low(S.chords[b + 1], "F1") if b + 1 < S.nb else r
    mp = {"r": r, "o": r + 12, "5": r + 7, "a": nx - 1 if nx > r else nx + 1}
    assert onsets(pat) == len(kinds), (pat, kinds)
    FMB.bar(b, steps(pat, [N(mp[c]) for c in kinds], short=short))
    if sub: SUB.bar(b, steps(sub, [N(r)]))


def top(b): return [N(x) for x in tones(S.chords[b], "C5", "C6")]
def bell_line(b, line): BELL.bar(b, KEY(b).mel(line, oct=5))
def bell_ans(b, t, odd): BELL.bar(b, steps("x-----....x-x---" if not odd else "x---....x-x-x---", [t[0], t[1], t[-1], t[1]]))
def pluck_ans(b): PLK.bar(b, arp16(S.chords[b], "........x.x.xxx-", (0, 2, 1, 3, 4), lo="A4", hi="A6", short=0.25))
def sub1(b): SUB.bar(b, f"{N(root(b))}:3 R:1")


# のび: 和音がゆっくりふくらんで沈む（長い音。小節ごとに打つ場所がちがう）
SWELL = ["x---------------", "x-------x-------", "x-----------x---", "x-----x-----x-x-", "x---------------", "x-------x-----x-", "x-----x-----x---", "x---x---x-x-...."]
BSP = [("x---------x-x---", "r5o"), ("x-----x---------", "ro"), ("x---------x---x-", "rro"), ("x-----x-----x-x-", "rr5a"), ("x---------x-x---", "ro5"), ("x-----x---------", "r5"),
       ("x---------x---x-", "ro5"), ("x---x---x-x-....", "rr5o")]
SOFT = ["x---....x---....", "x---x---....x---", "x---....x-x-....", "x---x---x---....", "x---....x---x---", "x---x---....x---", "x---....x-x-x---", "x---x---x-------"]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）
HALF = [("X.....x...x.....", "........X.......", "x...x...x.x.x..."), ("X.........x..x..", "........X.......", "x.x.x...x...x.xx")]
LAZY = [("X.........x.....", "................", "x...x.x.x...x..."), ("X......x........", "..............x.", "x...x...x.x.x.x.")]


def drop(b, i, full=True, motif=False):
    """ドロップの1小節。full＝和音を長く（歌のないドロップ）、False＝短く切って歌を前に（サビ）"""
    saw(b, SWELL[i] if full else SOFT[i], short=None if full else 0.5); bs(b, *BSP[i])
    k, s, h = HALF[i % 2]; D.set(b, k, s, h); KFXT.bar(b, "R:2 B4:1 R:1")
    if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if i == 3: hat_roll(HATR, b, 1)
    if i == 7: fill_cresc(D, b, 2)
    if full:
        if motif and i in (0, 1, 4, 5): bell_line(b, MOT[i % 2])
        elif i in (0, 1, 4, 5): bell_line(b, VC[i])                       # ベルが、あとで歌う旋律を先に鳴らす
    elif i % 2 == 1: PLK.bar(b, arp16(S.chords[b], "..........xxxxx-", (0, 1, 2, 3, 4), lo="A4", hi="A6", short=0.25))


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; t = top(b)
    if n == "1匹め":                                                     # ベル1つと低いベースだけ。音が1つずつ増える
        BELL.bar(b, steps(["x---------------", "x-------x-------", "x-----x---x-----", "x---x---x-------"][i], [t[q % len(t)] for q in ((0,), (0, 2), (1, 0, 2), (0, 1, 2))[i]]))
        SUB.bar(b, f"{N(root(b))}:4")
    elif n == "集まってくる":                                           # 4小節ごとに1つ増える: ベル＋ベース → プラック → パッド → ハイハットとキック
        g = i // 4; SUB.bar(b, f"{N(root(b))}:4"); bell_ans(b, t, odd)
        if g >= 1 and odd: pluck_ans(b)
        if g >= 2: pad(b)
        if g >= 3: k, s, h = LAZY[i % 2]; D.set(b, k, "................", h); KFXT.bar(b, "R:2 C5:1 R:1")
    elif n == "議題はない":                                             # 全員そろっている。ベースがゆっくりはねる
        pad(b); bs(b, "x-----x-..x-x---" if not odd else "x-----x-x-....x-", "rro5" if not odd else "rroa", sub="x-----------....")
        k, s, h = LAZY[i % 2]; D.set(b, k, s, h); KFXT.bar(b, "R:2 C5:1 R:1")
        if odd: pluck_ans(b)
        elif i >= 8: bell_ans(b, t, False)
    elif n in ("ぽかぽか", "ぽかぽか2"):                                 # 和音が上がる。最後の1拍は無音
        if not last: pad(b, "x---------------"); SUB.bar(b, f"{N(root(b))}:4")
        if i >= 2: saw(b, ["x-------........", "x-------x-------", "x---x---x---x---", "x---x---x-x-x-x-", "x-x-x-x-x-x-x-x-", "x-x-x-x-xxxx...."][i - 2])
        D.set(b, ("X...............", "X.......x.......", "X...x...X...x...", "X...X...X...X...")[i // 2], "................" if i < 6 else ("....X.......X..." if i == 6 else "x.x.x.x.xxxx...."),
              "x...x...x...x..." if i < 4 else "x.x.x.x.x.x.x.x." if not last else "................")
        if i == 5: hat_roll(HATR, b, 1)
        if last: FXT.bar(b, fx_bar((0, "up", 3))); SUB.bar(b, f"{N(root(b))}:3 R:1")
    elif n in ("のび1", "のび2"): drop(b, i, full=True)
    elif n in ("サビ1", "サビ2", "サビ3"): drop(b, i, full=False)
    elif n == "最後ののび": drop(b, i, full=True, motif=True)
    elif n == "雲がかかる":                                             # ドラムとベースが止まる。ベルと声だけ。最後の2拍は無音
        if i < 7:
            pad(b); BELL.bar(b, steps("x---....x-x-----" if not odd else "........x---x---", [t[0], t[-1], t[1]]))
            if i >= 4: SUB.bar(b, f"{N(root(b))}:4")
        else:
            v = sorted(voice(S.chords[b], 64, 3)); FXT.bar(b, fx_bar((0, "rev", 2)))
            for q in range(3): PAD[q].bar(b, f"{N(v[q])}:2 R:2")
            BELL.bar(b, steps("x-x-x-x-........", [t[0], t[1], t[2 % len(t)], t[-1]]))
    elif n == "解散":                                                   # 入った順の逆に、1つずつ抜ける: ハイハット → パッド → プラック → ベース → ベルの1音
        g = i // 2
        if i < 7: bell_ans(b, t, odd) if i < 6 else BELL.bar(b, f"{t[0]}:4")
        if g <= 2: sub1(b)
        if g <= 1 and odd: pluck_ans(b)
        if g <= 1: pad(b)
        if g == 0: k, s, h = LAZY[i % 2]; D.set(b, k, "................", h); KFXT.bar(b, "R:2 C5:1 R:1")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の11（10時）。Kawaii future bass（150・半分の速さ・変ホ長調 → ヘ長調）。ひなたに1匹ずつ集まって、何も決めずに解散する話。"
          "ベル1つで始まる → 4小節ごとに楽器が1つ増える → スーパーソウの和音がゆっくりふくらむドロップと「にゃ」のかけ合い → サビ → "
          "雲がかかって無音 → 全音上がって最後のサビとドロップ → 楽器が1つずつ抜けて終わる。自作")
finish(S, LY, V, 0, flat=True)                                           # どのドロップも同じ強さで鳴らす（曲全体の山を打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "FM のベース", mid=92, down=12, up=10, seed=11); humanize(path, "ベル", mid=88, down=10, up=12, seed=4)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "bridge": 8, "outro": 8}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("サビ3", 0, None, K2)], vol=0.34)
    L_, R_ = {}, {}                                                       # のびの合間に、声のチョップ「にゃ」が左右でかけ合う
    for name, sh in (("のび1", 0), ("のび2", 0), ("最後ののび", 2)):
        sc = S.sc(name); p = lambda x: nm(midi(x) + sh)
        for i in (2, 6): L_[sc[i]] = f"R:1 {p('Bb4')}:0.5:にゃ R:0.5 {p('Bb4')}:0.5:にゃ R:1.5"; R_[sc[i]] = f"R:2.5 {p('Eb5')}:0.5:にゃ R:0.5 {p('C5')}:0.5:にゃ"
        for i in (3, 7): R_[sc[i]] = f"R:1 {p('C5')}:0.5:にゃ {p('Eb5')}:1:にゃ R:1.5"
    R_[S.sc("解散")[7]] = f"{nm(midi('C5'))}:1.5:にゃ R:2.5"                    # 最後のひとこと
    chops(path, S, L_, vol=0.3, pan=-0.35); chops(path, S, R_, vol=0.3, pan=0.35)
    voice_by_scene(path, S, {}, default="cute")                           # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
