# vt3 11「洗濯日和のステップ」Laundry Day Steps（仮）— Kawaii future bass。4分の4・150（半分の速さで感じる）。ヘ長調 → 最後のサビから全音上のト長調。
# 第3弾（0時〜24時の街）の 10時。
#
# v11（2026-11-21）: ゼロから作り直し。v1〜v10 はケルトのジグ（8分の6・フィドルとアコーディオン → v10 でナイロン弦のギターなどに入れかえ）で `vt3_11_laundry.py`。
#   人間の指示: 「10と11は曲を最初から作り直しましょう。KPOPとKawaii_future_bassにしましょう」（2026-11-21）。表と「物語 → 音」を見せた。
#
# コンセプト: 晴れた朝。窓をあけて干していると、風が来て布が踊りだす。つられて自分も踊る。風がやみ、乾いた布を取りこむ。
# ジャンル: Kawaii future bass。作る前に調べた決まりごと（出どころは docs/sound/vt3-remake-plan.md の 11 v11）:
#   ・キックにあわせて沈む（サイドチェイン）スーパーソウの和音が、ドロップの主役
#   ・ベルやプラックのかわいい旋律、声のチョップのかけ合い、泡やきらきらの効果音
#   ・半分の速さのドラム（キックは1拍め、スネアとクラップは3拍め）。2回めのドロップで全音上げる手もある
#
# 物語の出来事 → その時の音:
#   窓をあける（朝の光）           → 水滴の音ひとつ → ベルが上がっていく → プラックの駆け上がり
#   干す（ぱちんとはさむ）         → ベルと低いベースだけ。スネアの場所で「ぱちん」（指パッチンの音）
#   風が来る（すそがまう）         → スーパーソウの和音が「3小節・3小節・2小節」の風のかたまりで吹く。かたまりの終わりは16分でひらひら
#   ドロップ1（布が踊る）          → 歌なし。和音が沈んでは吹く。ベルが旋律、声のチョップが合いの手
#   サビ1（つられて踊る）          → ベルと同じ旋律を、こんどは歌う
#   干す2（くつ下がならぶ）        → ベースがはねる。プラックが合いの手
#   風がやむ（しずかになる）       → ドラムもベースも止まり、ベルと声だけ。最後の2拍は無音
#   サビ3・最後のドロップ           → 全音上がる。最後のドロップで、ベルが合いことばの節を2回
#   とりこむ（おひさまのにおい）   → ベルとパッドだけ。ひとことで終わる
# この曲だけの物: 「風のかたまり」。和音が4小節ずつではなく 3・3・2 で吹き、終わりがひらひらする。スネアのかわりの「ぱちん」。
# 合いことばの節（3・5・6・5・2）: 最後のドロップで、ベルが2回鳴らす（アルバムの決まり）。
# 歌詞: 曲名は歌わない。「洗濯」「ステップ」も使わない。声: キュート 1 種類。
from vocalo_lib import *

S = Song("11", "laundry", "洗濯日和のステップ（仮）", "Laundry Day Steps", 150, 4, "F", "major", "Kawaii future bass（ボカロ）")
S.kit = "naked-x"; S.flags = S.flags + " --space room --space-wet 0.1"
K1, K2 = Key("F", "major"), Key("G", "major")


def up2(chs): return [tr_chord(c, 2) for c in chs]


VCH = ["Fmaj7", "Am7", "Bbmaj7", "Gm7", "Fmaj7", "Dm7", "Gm7", "C7sus4"]
WCH = ["Bbmaj7", "Bbmaj7", "Bbmaj7", "Gm7", "Gm7", "Gm7", "C7sus4", "C"]          # 風のかたまり: 3・3・2
DCH = ["Bbmaj7", "C", "Dm7", "Dm7", "Gm7", "Am7", "Bbmaj7", "C"]                  # ドロップも 3（上がる）・3・2 で和音が動く
S.scene("窓をあける", 4, "intro", ["Fmaj7", "Fmaj7", "Bbmaj7", "C7sus4"])
S.scene("干す", 16, "verse", VCH * 2)
S.scene("風が来る", 8, "pre", WCH)
S.scene("ドロップ1", 8, "break", DCH)
S.scene("サビ1", 8, "chorus", DCH)
S.scene("干す2", 16, "verse", VCH * 2)
S.scene("風が来る2", 8, "pre", WCH)
S.scene("ドロップ2", 8, "break", DCH)
S.scene("サビ2", 8, "chorus", DCH)
S.scene("風がやむ", 8, "bridge", ["Dm7", "Bbmaj7", "Gm7", "C", "Dm7", "Bbmaj7", "Ebmaj7", "D7"])
S.scene("サビ3", 8, "chorus", up2(DCH))
S.scene("最後のドロップ", 8, "break", up2(DCH))
S.scene("とりこむ", 6, "outro", up2(["Bbmaj7", "C", "Fmaj7", "Fmaj7", "Fmaj7", "Fmaj7"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("サビ3")[0]


def KEY(b): return K2 if b >= MOD else K1


V = Voice(S, vol=0.16, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.03, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.65, fx=rack_supersaw()) for i in range(5)]
FMB = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.09, pan=0, duck=0.25, fx=rack_bass())
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.045, pan=0, duck=0.4)
BELL = S.track("ベル", "lead", patch="surgeFantasyBell", volume=0.09, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
PLK = S.track("プラック", "lead", patch="surgeNicePluck", volume=0.06, pan=-0.3, reverb=0.2, fx=rack_pluck())
PAD = [S.track(f"やわらかいパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.1, pan=0.0, reverb=0.4, fx=[{"type": "boost", "gain": 7}, {"type": "widen", "amount": 1.4}]) for i in range(3)]
KFXT = S.track("ぱちん（指パッチン）とクラップ", "guitar", patch="kawaiiFx", volume=0.08, pan=0.05, reverb=0.15, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
FXT = S.track("効果音（水滴・きらきら）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = F4。サビ3 からは 1 = G4）=================
VA = ["3:1 5:0.5 5:1 6:0.5 5:1", "3:1 2:1.5 R:1.5", "4:1 6:0.5 6:1 1':0.5 6:1", "5:1 5:1.5 R:1.5",
      "3:1 5:0.5 5:1 6:0.5 1':1", "2':1 1':1.5 R:1.5", "6:0.5 6:0.5 5:1 4:0.5 3:0.5 2:1", "2:1 1:2 R:1"]
VW = ["R:1 5:0.5 6:0.5 1':1 6:1", "5:2.5 R:1.5", "R:4", "R:1 6:0.5 1':0.5 2':1 1':1", "6:2.5 R:1.5", "R:4", "5:1 6:1 1':1 6:1", "1':2 R:2"]
VC = ["5:0.75 5:0.75 3:0.5 5:1 6:1", "5:1.5 3:1.5 R:1", "6:0.75 6:0.75 5:0.5 6:1 1':1", "6:1.5 5:1.5 R:1",
      "4:0.75 4:0.75 5:0.5 6:1 1':1", "2':1.5 1':1.5 R:1", "6:0.5 5:0.5 3:1 2:1 3:1", "2:1 1:2 R:1"]
VB = ["3:1 2:1 1:1 2:1", "3:2.5 R:1.5", "5:1 3:1 2:1 3:1", "5:2.5 R:1.5", "6:1 5:1 6:1 1':1", "6:2.5 R:1.5"]
VO = ["3:1 3:0.5 5:1 6:0.5 5:1", "3:1 2:1 1:2"]
C1 = "ひらひらゆれる/かぜのてをとる/つまさきたてて/そらまでまわる"
C2 = "はたはたわらう/ひだまりのなか/かかとをならし/くもまでとどけ"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("干す", VA + VA, "まどをあけたら/ひかりのにおい/しろいたおるが/あくびをしてるよ/ぱちんとはさむ/そでがてをふる/あわのなごりが/そらへとんでいく")
put("風が来る", VW, "かぜがくる/すそがまう/おどろうよ")
put("サビ1", VC, C1)
put("干す2", VA + VA, "くつしたならぶ/みぎとひだりで/かたほうだけが/いつもまいごだね/ひろげたぬのは/ふねのほになる/ひなたのくにへ/わたしものせてよ")
put("風が来る2", VW, "またくるよ/せのびして/つかまえて")
put("サビ2", VC, C2)
put("風がやむ", VB, "かぜがやむ/しずかだね/かわいたよ", bars=S.sc("風がやむ")[:6])
put("サビ3", VC, C1)
put("とりこむ", VO, "おひさまのにおい", bars=S.sc("とりこむ")[:2])


# ================= 伴奏 =================
def root(b): return low(S.chords[b], "F1")


def saw(b, pat, short=None, lift=0):
    v = [x + lift for x in wide9(S.chords[b])]
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
def snap(b, pat="R:2 C5:1 R:1"): KFXT.bar(b, pat)                          # 「ぱちん」


# 風のかたまり（3・3・2）: 吹きはじめはのびて、終わりは16分でひらひら
GUST = ["x-------x-----x-", "x---x---x-x-x-x-", "x-x-x-x-xxxxxxxx", "x-----x-----x---", "x-.x-.x-x-.x-.x-", "x.x.xxx.x.xxxxxx", "x-------x---x-x-", "xxxxxxxxx-------"]
BSP = [("x--x--x-x-------", "rror"), ("x--x--x-x--x--x-", "rrorr5"), ("x-x---x-x--x--x-", "rorr5a"), ("x--x--x-x-------", "rror"), ("x--x--x-x--x--x-", "rr5ro5"), ("x-x---x-x--x--x-", "roro5a"),
       ("x-----x-x--x--x-", "rrr5o"), ("x--x--x-x-------", "ro5r")]
SOFT = ["x---x---x-------", "x---....x---x---", "x-x-....x-------", "x---x---x---....", "x---....x-x-x---", "x---x---....x---", "x-------x---x---", "x---x---x-------"]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）
HALF = [("X.........x.....", "........X.......", "x...x.x.x...x.x."), ("X......x..x.....", "........X.......", "x.x.x...x.x.x.xx")]
HOP = [("X..x......X.....", "........X.......", "x.xxx.x.x.xxx.x."), ("X..x...x..X.....", "........X.....x.", "x.x.x.xxx.x.x.x.")]


def drop(b, i, full=True, bell=True, motif=False):
    """ドロップの1小節。full＝和音を長く・大きく（歌のないドロップ）、False＝短く切って歌を前に（サビ）"""
    g = GUST[i] if full else SOFT[i]; saw(b, g, short=None if full else 0.5); bs(b, *BSP[i])
    k, s, h = HALF[i % 2]; D.set(b, k, s, h); KFXT.bar(b, "R:2 B4:1 R:1")
    if i == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
    if i in (2, 5): hat_roll(HATR, b, 1)                                  # 風のかたまりの終わり
    if i == 7: fill_cresc(D, b, 2)
    if full and bell:
        if motif and i in (0, 1, 3, 4): bell_line(b, MOT[0 if i in (0, 3) else 1])
        elif i in (0, 1): bell_line(b, VC[i])                             # ベルが、あとで歌う旋律を先に鳴らす
        elif i in (3, 4): bell_line(b, VC[i - 1])
        elif i in (6, 7): bell_line(b, VC[i])
    if not full and i % 2 == 1: PLK.bar(b, arp16(S.chords[b], "..........xxxxx-", (0, 1, 2, 3, 4), lo="A4", hi="A6", short=0.25))       # 歌の行の終わりに、プラックの駆け上がり


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; t = top(b)
    if n == "窓をあける":                                               # 水滴ひとつ → ベルが上がる → パッド → プラックの駆け上がり
        if i == 0: FXT.bar(b, fx_bar((0, "drop", 1), (2, "awa", 1)))
        BELL.bar(b, steps(["....x---x---x---", "x---x-----x-----", "x---x---x-x-----", "x-------........"][i], [t[q % len(t)] for q in ((0, 1, 2), (1, 2, 0), (0, 1, 2, 1), (2,))[i]]))
        pad(b); SUB.bar(b, f"{N(root(b))}:4")
        if i == 3: PLK.bar(b, arp16(S.chords[b], "....xxxxxxxxx---", (0, 1, 2, 3, 4, 5, 6, 7, 8), lo="A4", hi="A6", short=0.25)); FXT.bar(b, fx_bar((2, "kira", 2)))
    elif n in ("干す", "干す2"):
        two = n == "干す2"; late = i >= 8
        pad(b)
        if two:                                                           # ベースがはねる。プラックが合いの手
            bs(b, "x--x--x-..x-x---" if not odd else "x--x--x-x-..x-x-", "rroro" if not odd else "rro5ra", short=0.5, sub="x---........x---")
            k, s, h = HOP[i % 2]; D.set(b, k, "................", h); snap(b, "R:2 C5:1 R:1" if not last else "R:2 C5:0.5 C5:0.5 C5:0.5 C5:0.5")
            if odd: PLK.bar(b, arp16(S.chords[b], "........x.x.xxx-", (0, 2, 1, 3, 4), lo="A4", hi="A6", short=0.25))
            if late and not odd: BELL.bar(b, steps("..........x-x---", [t[1], t[-1]]))
        else:                                                             # ベルと低いベース。スネアの場所で「ぱちん」
            SUB.bar(b, f"{N(root(b))}:3 R:1"); snap(b)
            D.set(b, "x...............", "................", "................" if not late else "x...x...x...x.x.")
            if odd: BELL.bar(b, steps("........x.x.x-x-", [t[0], t[1], t[2 % len(t)], t[-1]]))             # 歌がのばす後ろで、ベルが答える
            if late: bs(b, "x-------..x-x---", "r5o", sub=None)
    elif n in ("風が来る", "風が来る2"):                                 # 風のかたまり 3・3・2。吹くたびに和音が高くなる
        g = (0, 0, 0, 1, 1, 1, 2, 2)[i]; j = (0, 1, 2, 0, 1, 2, 0, 1)[i]
        if g < 2: saw(b, ["x-------........", "x-------x---x---", "x---x---x-x-xxxx"][j], lift=0); pad(b, "x---------------"); SUB.bar(b, f"{N(root(b))}:4")
        else: saw(b, ["x-x-x-x-x-x-x-x-", "xxxxxxxxxxxx...."][j]); SUB.bar(b, f"{N(root(b))}:{4 if j == 0 else 3} " + ("" if j == 0 else "R:1"))
        D.set(b, ("X...............", "X.......x.......", "X...x...X...x...")[g] if not last else "X...X...X...X...", "................" if g < 2 else ("....X.......X..." if j == 0 else "x.x.x.x.xxxx...."),
              "x...x...x...x..." if g == 0 else "x.x.x.x.x.x.x.x." if not last else "................")
        if j == 2: hat_roll(HATR, b, 1)
        if g == 1 and j == 0: snap(b, "R:2 B4:1 R:1")
        if last: FXT.bar(b, fx_bar((0, "up", 3)))                          # 最後の1拍は無音
    elif n in ("ドロップ1", "ドロップ2"): drop(b, i, full=True)
    elif n in ("サビ1", "サビ2", "サビ3"): drop(b, i, full=False)
    elif n == "最後のドロップ": drop(b, i, full=True, motif=True)
    elif n == "風がやむ":                                               # ドラムもベースも止まる。ベルと声だけ。最後の2拍は無音
        if i < 6:
            pad(b); BELL.bar(b, steps("x---....x-x-----" if not odd else "........x---x---", [t[0], t[-1], t[1]]))
            if i >= 4: SUB.bar(b, f"{N(root(b))}:4")
        elif i == 6: pad(b); BELL.bar(b, steps("x---x---x---x---", [t[0], t[1], t[2 % len(t)], t[-1]])); SUB.bar(b, f"{N(root(b))}:4")
        else:
            v = sorted(voice(S.chords[b], 64, 3)); FXT.bar(b, fx_bar((0, "rev", 2)))
            for q in range(3): PAD[q].bar(b, f"{N(v[q])}:2 R:2")
            BELL.bar(b, steps("x-x-x-x-........", [t[0], t[1], t[2 % len(t)], t[-1]]))
    elif n == "とりこむ":                                               # ベルとパッドだけ。ひとことで終わる
        if i < 5: pad(b, "x---------------")
        if i in (2, 3): BELL.bar(b, steps("x---x---x-x-----" if i == 2 else "x---x-----------", [t[0], t[1], t[2 % len(t)], t[-1]]))
        if i == 4: BELL.bar(b, f"{t[-1]}:4"); FXT.bar(b, fx_bar((0, "kira2", 2)))
        if i < 4: SUB.bar(b, f"{N(root(b))}:4")
        if i == 0: crash(D, b, "C2", 4)

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の11（10時）。Kawaii future bass（150・半分の速さ・ヘ長調 → ト長調）。晴れた朝に干していると、風が来て布が踊りだし、つられて踊る話。"
          "水滴とベルで始まる → 「ぱちん」とはさむ音がスネアのかわり → スーパーソウの和音が 3・3・2 小節の風のかたまりで吹く → 歌なしのドロップ → サビ → "
          "風がやんで無音 → 全音上がって最後のサビとドロップ → ベルとひとことで終わる。自作")
finish(S, LY, V, 0, flat=True)                                           # どのドロップも同じ強さで鳴らす（曲全体の山を打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "FM のベース", mid=92, down=12, up=10, seed=11); humanize(path, "ベル", mid=88, down=10, up=12, seed=4)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "bridge": 8, "outro": 8}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("サビ3", 0, None, K2)], vol=0.34)
    CH = "R:2 C5:0.5:ひ C5:0.5:ら A4:0.5:ひ C5:0.5:ら"                    # 風のかたまりの終わりに、声のチョップ「ひらひら」
    bars = {}
    for name, sh in (("ドロップ1", 0), ("ドロップ2", 0), ("最後のドロップ", 2)):
        for i in (2, 5): bars[S.sc(name)[i]] = " ".join(x if x.startswith("R") else f"{nm(midi(x.split(':')[0]) + sh + (2 if i == 5 else 0))}:{x.split(':')[1]}:{x.split(':')[2]}" for x in CH.split())
    chops(path, S, bars, vol=0.3, pan=-0.25)
    voice_by_scene(path, S, {}, default="cute")                           # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
