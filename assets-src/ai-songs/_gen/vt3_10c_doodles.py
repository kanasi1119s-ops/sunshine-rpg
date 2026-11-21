# vt3 10「教科書の落書きたち」Doodles in the Textbook（仮）— K-POP（場面ごとにビートが切りかわるダンスポップ）。4分の4・122。ホ短調 → 最後のサビから全音上の嬰ヘ短調。
# 第3弾（0時〜24時の街）の 9時。
#
# v8（2026-11-21）: ゼロから作り直し。v1〜v7 はブルーグラス（バンジョーとフィドル → v6・v7 でアコギとクリーンのギターに入れかえ）で `vt3_10_doodles.py`。
#   人間の指示: 「10と11は曲を最初から作り直しましょう。KPOPとKawaii_future_bassにしましょう」（2026-11-21）。表と「物語 → 音」を見せた。
#
# コンセプト: 授業中、ノートのすみの絵が動きだして踊りはじめる。退屈な1時間を、机の上のステージに書きかえる。
# ジャンル: K-POP。作る前に調べた決まりごと（出どころは docs/sound/vt3-remake-plan.md の 10 v8）:
#   ・場面ごとに対比をつける組み立て（Aメロ → Bメロで持ち上げ → 大きなフックのサビ → サビのあとのフック → ブリッジ／ビートの切りかえ → ダンスブレイク → 最後のサビで転調）
#   ・テンポ 120〜135。808 のキック、細かいハイハット、シンセの短い和音、声のチョップ、かけ声のフック
#   ・いちばん覚えやすい数拍（フック）に向けて、ほかの全部を組み立てる
#
# 物語の出来事 → その時の音:
#   えんぴつの音（机をたたくリズム）   → えんぴつの「コツコツ」と、フックの音型（プラック）で始まる
#   1ページめ（絵が目をさます）        → 半分の速さの重いビート＋低いベース。歌は低く語るように
#   めくる（線が立ちあがる）           → キックが消え、和音が上がっていく。最後に1拍の無音
#   サビ1（机の上で踊りだす）          → 4つ打ち＋3音のくり返しのフック。歪みのギターが入る。後半は歌なしのフック
#   2ページめ（仲間がふえる）          → はねるビートに切りかわり、プラックが合いの手
#   めくる2・サビ2（余白がステージ）   → ハモリが加わる
#   ダンスブレイク（全員で踊る）       → 歌なし。ベースの旋律とドラムと、合いことばの節（プラック）
#   先生がふりむく（ぴたっと止まる）   → 1小節の無音 → 小さな声だけ → スネアが細かくなる
#   最後のサビ（チャイムまで踊る）     → 全音上がり、全部が重なる
#   チャイム（絵が紙に戻る）           → 前奏と同じ、えんぴつとフックの音型に戻って終わる
# この曲だけの物: 「ページをめくる」。めくるたびにビートが別物になる（半分の速さ → 4つ打ち → はねるビート）。
# 合いことばの節（3・5・6・5・2）: ダンスブレイクで、プラックが2回鳴らす（アルバムの決まり）。
# 歌詞: 曲名は歌わない。「教科書」「落書き」も使わない。声: クリア 1 種類。
from vocalo_lib import *
import gtr2_lib as G2

S = Song("10", "doodles", "教科書の落書きたち（仮）", "Doodles in the Textbook", 122, 4, "E", "minor", "K-POP（ボカロ）")
S.kit = "electro"; S.flags = S.flags + " --space room --space-wet 0.08"
K1, K2 = Key("E", "minor"), Key("F#", "minor")


def up2(chs): return [tr_chord(c, 2) for c in chs]


VCH = ["Em", "Em", "Am7", "B7"]
PCH = ["Cmaj7", "D", "Bm7", "Em", "Cmaj7", "D", "B7sus4", "B7"]
CCH = ["Em", "G", "A", "C", "Em", "G", "A", "B7"]
S.scene("えんぴつの音", 4, "intro", ["Em", "Em", "Em", "Em"])
S.scene("1ページめ", 16, "verse", VCH * 4)
S.scene("めくる", 8, "pre", PCH)
S.scene("サビ1", 16, "chorus", CCH + CCH)
S.scene("2ページめ", 16, "verse", VCH * 4)
S.scene("めくる2", 8, "pre", PCH)
S.scene("サビ2", 16, "chorus", CCH + CCH)
S.scene("ダンスブレイク", 8, "break", ["Em", "Em", "C", "C", "Am7", "Am7", "B7", "B7"])
S.scene("先生がふりむく", 4, "bridge", ["Em", "Cmaj7", "D", "C#7"])
S.scene("最後のサビ", 24, "chorus", up2(CCH + CCH + CCH[:7] + ["Em"]))
S.scene("チャイム", 6, "outro", up2(["Em"] * 6))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("最後のサビ")[0]


def KEY(b): return K2 if b >= MOD else K1
def SCALE(b): return {(KEY(b).t + x) % 12 for x in (0, 2, 3, 5, 7, 8, 10)}


PING = [{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}]
V = Voice(S, vol=0.16, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
TAP = S.track("えんぴつのコツコツ（カホンの縁）", "cajon", volume=0.2, pan=0.15, reverb=0.1, fx=[{"type": "boost", "gain": 17}])
SUB = S.track("サブベース（のばす）", "bass", patch="kfbSub", volume=0.05, pan=0, duck=0.4, fx=[{"type": "filter", "kind": "highpass", "freq": 32, "q": 0.7}])
RB = S.track("うなるシンセベース", "bass", patch="surgeBassAnalogBassImaged", volume=0.11, pan=0, duck=0.3)
STAB = [S.track(f"短いシンセの和音{i + 1}", "lead", patch="surgeChordReset", volume=0.1, pan=0.0, reverb=0.2, duck=0.3, fx=[{"type": "widen", "amount": 1.5}]) for i in range(3)]
PAD = [S.track(f"上がっていく和音{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.12, pan=0.0, reverb=0.35, fx=[{"type": "boost", "gain": 9}, {"type": "widen", "amount": 1.4}]) for i in range(3)]
PLK = S.track("矩形波のプラック（フック）", "lead", patch="kfbSquarePluck", volume=0.09, pan=0.3, reverb=0.25, fx=PING)
GLT = [S.track(f"左の歪みのギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.06, -0.5, tone="nu-metal-wall")) for i in range(6)]
GRT = [S.track(f"右の歪みのギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.06, 0.5, tone="nu-metal-wall")) for i in range(6)]
CLP = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)
SL, SR = G2.Strummer(GLT, S, 10), G2.Strummer(GRT, S, 11); TR = [None]

# ================= 歌（度数:長さ。oct 4 で 1 = E4。最後のサビからは 1 = F#4）=================
VA = ["R:0.5 1:0.5 1:0.5 3:1 1:0.5 7,:1", "1:0.5 3:1.5 R:2", "R:0.5 4:0.5 4:0.5 5:1 4:0.5 3:1", "2:0.5 2:1.5 R:2",
      "R:0.5 3:0.5 3:0.5 5:1 3:0.5 1:1", "3:0.5 5:1.5 R:2", "R:0.5 4:0.5 5:0.5 6:1 5:0.5 4:1", "5:0.5 5:1.5 R:2"]
VP = ["5:1.5 6:0.5 7:1 5:1", "4:2.5 R:1.5", "4:1.5 5:0.5 7:1 5:1", "3:2.5 R:1.5", "5:1.5 6:0.5 7:1 1':1", "2':2.5 R:1.5", "1':1.5 5:0.5 5:1 1':1", "5:2 R:2"]
HK = "3:0.5 5:0.5 3:1 3:0.5 5:0.5 3:1"                                    # 3音のくり返しのフック（お・ど・れ）
VC = [HK, "5:1 7:0.5 5:1.5 R:1", HK, "6:1 1':0.5 6:1.5 R:1", "1':1.5 7:0.5 5:1 3:1", "4:0.5 5:0.5 6:1 5:1 R:1", HK, "5:0.5 2:0.5 5:2 R:1"]
VCE = VC[:7] + ["5:0.5 3:0.5 1:2 R:1"]                                    # いちばん最後は主音でとまる
VT = ["R:4", "5:1.5 6:0.5 7:1 5:1", "4:2.5 R:1.5", "R:4"]
C1 = "おどれおどれいまだ/まわれまわれそこだ/ちゃいむがなるまで/おどれおどれぼくら"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("1ページめ", VA + VA, "のーとのすみで/だれかがのびた/えんぴつのせん/あくびをひとつ/まるとぼうだけ/それでもうごく/よはくのひろば/あしぶみをする")
put("めくる", VP, "たちあがる/せんのあし/ひらりとね/めくるたび")
put("サビ1", VC, C1, bars=S.sc("サビ1")[:8])
put("2ページめ", VA + VA, "となりのぺーじ/ねこがとびだす/ひげのせんせい/くるりとまわる/けしごむのかす/ゆきになるから/だれもけせない/ぼくらのおどり")
put("めくる2", VP, "せんせいの/こえはまだ/とおくから/ひびいてる")
put("サビ2", VC, C1, bars=S.sc("サビ2")[:8])
put("先生がふりむく", VT[1:3], "ばれたかな", bars=S.sc("先生がふりむく")[1:3])
LC = S.sc("最後のサビ")
put("最後のサビ", VC + VCE, C1 + "/" + C1, bars=LC[:8] + LC[16:])


# ================= 伴奏 =================
def rlow(b, lo="E1"): return low(S.chords[b], lo)


def seq(b, pat, tr=None):
    """シンセベースを16分のマスで。r＝根音、R＝1オクターブ上、5＝5度、7＝短7度、.＝休み、-＝のばす"""
    r = rlow(b); out = []; i = 0
    while i < 16:
        c = pat[i]; L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if c == "." else f"{N(r + {'r': 0, 'R': 12, '5': 7, '7': 10}[c])}:{L * 0.25:g}"); i += L
    (tr or RB).bar(b, " ".join(out))


def stab(b, pat, center=67):
    v = sorted(voice(S.chords[b], center, 3))
    for j in range(3): STAB[j].bar(b, steps(pat, [N(v[j])] * pat.count("x"), short=0.5))


def pad(b, lift=0):
    v = sorted(voice(S.chords[b], 62 + lift, 3))
    for j in range(3): PAD[j].bar(b, f"{N(v[j])}:4")


def hook(b, k=0):
    """フックの音型（歌のフックと同じ 3・5・3）をプラックで"""
    PLK.bar(b, KEY(b).mel(HK if k == 0 else "5:0.5 7:0.5 5:1 5:0.5 7:0.5 5:1", oct=5))


def gtr(b, patL="D-d-d-D-d-d-D-d-", patR="D---d-U---U-d-U-"):
    c = S.chords[b]; TR[0] = G2.triad(c, TR[0]); SL.bar(b, patL, G2.low_shape(c, with_third=False)[:3], feel="down"); SR.bar(b, patR, TR[0], feel=8)


def clap(b, pat="R:1 B4:1 R:1 B4:1"): CLP.bar(b, pat)
def tap(b, pat="E3:0.5 E3:0.5 R:0.5 E3:0.5 E3:1 R:1"): TAP.bar(b, pat)


K4 = "X...X...X...X..."
HALF = [("X.........X.....", "........X.......", "x.x.x.x.x.x.x.x."), ("X......X..X.....", "........X.......", "x.x.x.xxx.x.xxxx")]         # 半分の速さの重いビート
BOUNCE = [("X..X..X...X..X..", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X..X..X..XX..X..", "....X.......X..x", "x.xxx.x.x.xxx.x.")]       # はねるビート（3・3・2）
FOUR = [(K4, "....X.......X...", "..x...x...x...x."), (K4, "....X.......X..x", "..x...x...x..xx.")]                                      # 4つ打ち
BRK = ["E2:0.75 E2:0.75 G2:0.5 B2:1 A2:0.5 G2:0.5", "E2:0.75 D2:0.75 E2:0.5 G2:0.5 A2:0.5 B2:1", "C2:0.75 C2:0.75 E2:0.5 G2:1 F#2:0.5 E2:0.5", "C2:0.75 D2:0.75 E2:0.5 G2:0.5 B2:0.5 C3:1",
       "A1:0.75 A1:0.75 C2:0.5 E2:1 D2:0.5 C2:0.5", "A1:0.75 B1:0.75 C2:0.5 E2:0.5 G2:0.5 A2:1", "B1:0.75 B1:0.75 D#2:0.5 F#2:1 E2:0.5 D#2:0.5", "B1:0.5 C#2:0.5 D#2:0.5 F#2:0.5 B2:2"]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "えんぴつの音":                                               # えんぴつのコツコツ → 3小節めからフックの音型
        tap(b); hook(b, i % 2)                                             # えんぴつとフックの音型で始まり、3小節めから低いベースが入る
        if i >= 2: SUB.bar(b, f"{N(rlow(b))}:4")
        if i == 3: D.set(b, "................", "........x.x.xxxx", "................")
    elif n in ("1ページめ", "2ページめ"):
        two = n == "2ページめ"; late = i >= 8
        g = (BOUNCE if two else HALF)[i % 2]; D.set(b, g[0], g[1] if not last else g[1][:12] + "x.xx", g[2])
        if two:                                                           # はねるビート: ベースも 3・3・2
            seq(b, "r--r--r-..r-R-r-" if not odd else "r--r--R-r--r-5-7"); clap(b, "R:1 B4:1 R:1 B4:1")
            if odd: PLK.bar(b, KEY(b).mel(("R:2.5 5:0.5 7:0.5 5:0.5", "R:2.5 3:0.5 5:0.5 6:0.5")[(i // 2) % 2], oct=5))      # 歌の行の終わりに、プラックの合いの手
            SUB.bar(b, f"{N(rlow(b))}:1.5 R:1 {N(rlow(b))}:1.5"); stab(b, "..x.....x..x...." if late else "..x.....x.......")
        else:                                                             # 半分の速さ: 低いベースをのばす
            SUB.bar(b, f"{N(rlow(b))}:2.5 R:0.5 {N(rlow(b))}:1"); tap(b, "R:1 E3:0.5 R:0.5 R:1 E3:0.5 E3:0.5")
            if late: seq(b, "r---........r-R-"); stab(b, "........x......." if not odd else "........x..x....")
    elif n in ("めくる", "めくる2"):                                     # キックが消え、和音が上がっていく。最後の1拍は無音
        if last:
            v = sorted(voice(S.chords[b], 62 + i * 2, 3)); D.set(b, "................", "x.x.x.xxxxxx....", "................")
            for j in range(3): PAD[j].bar(b, f"{N(v[j])}:3 R:1")
            continue
        pad(b, i * 2); tap(b, "E3:0.5 R:0.5 E3:0.5 E3:0.5 R:1 E3:0.5 E3:0.5"); D.set(b, "................", "................" if i < 4 else ("....x.......x..." if i < 6 else "x...x...x.x.x.x."), "x...x...x...x...")
        if i >= 4: SUB.bar(b, f"{N(rlow(b))}:4")
        if n == "めくる2" and not odd: hook(b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        fin = n == "最後のサビ"; two = n == "サビ2"; post = (i >= 8) if not fin else (8 <= i < 16); end = fin and last
        g = FOUR[i % 2]; D.set(b, g[0], g[1] if i % 8 != 7 else "....X.......X.XX", g[2] if not (two or fin) else "x.x.x.x.x.x.x.x."); clap(b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        seq(b, "r-r-R-r-r-r-R-5-" if not odd else "r-r-R-r-r-R-5-7-"); SUB.bar(b, f"{N(rlow(b))}:4"); gtr(b)
        stab(b, "x.....x..x....x." if not odd else "x..x.....x..x...")
        if post or fin: hook(b, i % 2)                                    # サビのあと: 歌なしでフックの音型（歌の版では声のチョップも）
    elif n == "ダンスブレイク":                                          # 歌なし。ベースの旋律とドラム。プラックが合いことばの節を2回
        g = HALF[i % 2]; D.set(b, g[0], g[1] if not last else "........X...XXXX", "x.xxx.x.x.xxx.xx"); RB.bar(b, BRK[i]); clap(b, "R:2 B4:1 R:1")
        if i in (0, 1, 4, 5): PLK.bar(b, K1.mel(MOT[i % 2], oct=5))
        stab(b, "x..x..x...x..x.."); SUB.bar(b, f"{N(rlow(b))}:4")
        c = S.chords[b]; TR[0] = G2.triad(c, TR[0]); SL.bar(b, "D--U--D---D--U--", G2.low_shape(c, with_third=False)[:3], feel=16); SR.bar(b, "D--U--D---D--U--", TR[0], feel=16)
    elif n == "先生がふりむく":                                          # 1小節の無音 → 小さな声だけ → スネアが細かくなる
        if i in (1, 2): pad(b)
        if i == 3: D.set(b, "X...X...X.X.X.X.", "x...x...x.x.xxxx", "................"); pad(b, 4); seq(b, "r-r-r-r-rrrrRRRR")
    elif n == "チャイム":                                                # 前奏と同じ音に戻って終わる
        if i < 4: tap(b); hook(b, i % 2)                                   # 前奏と同じ「えんぴつとフックの音型」に戻る（えんぴつだけにすると、仕上げで音量が 3.7dB 下がったため）
        elif i == 4: tap(b, "E3:0.5 E3:0.5 R:3"); PLK.bar(b, KEY(b).mel("1:2 R:2", oct=5))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の10（9時）。K-POP（122・ホ短調 → 嬰ヘ短調）。授業中、ノートのすみの絵が動きだして踊る話。"
          "えんぴつのコツコツで始まる → 半分の速さの重いビート → キックが消えて和音が上がる → 4つ打ちのサビと3音のフック → はねるビート → "
          "ダンスブレイク → 1小節の無音 → 全音上がって最後のサビ → えんぴつの音だけで終わる。ページをめくるたびにビートが切りかわる。自作")
SL.end(S.nb); SR.end(S.nb)
finish(S, LY, V, 0, flat=True)                                           # どのサビも同じ強さで鳴らす（曲全体の山を打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "うなるシンセベース", mid=92, down=12, up=10, seed=10); humanize(path, "矩形波のプラック", mid=86, down=10, up=12, seed=5)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 14, "chorus": 20, "bridge": 8}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("最後のサビ", 0, None, K2)], vol=0.34)
    c1, c2, c3 = S.sc("サビ1"), S.sc("サビ2"), S.sc("最後のサビ")
    CH = {0: "G4:0.5:お B4:0.5:ど G4:1:れ R:2", 1: "R:2 G4:0.5:お B4:0.5:ど G4:1:れ"}
    bars = {}
    for sc_, rng, sh in ((c1, range(8, 16), 0), (c2, range(8, 16), 0), (c3, range(8, 16), 2)):
        for i in rng: bars[sc_[i]] = " ".join(x if x.startswith("R") else f"{nm(midi(x.split(':')[0]) + sh)}:{x.split(':')[1]}:{x.split(':')[2]}" for x in CH[i % 2].split())
    chops(path, S, bars, vol=0.3, pan=-0.25)                              # サビのあと: 声のチョップで「お・ど・れ」
    voice_by_scene(path, S, {}, default="clear")                          # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0; v["debreathAt"] = [[t + 0.02, 1.2] for t in [98.58, 21.11, 102.75, 35.87, 45.11, 94.61, 129.75, 47.14, 139.56]]   # 測って息の音が大きかった 9 か所
    save(path, js)
js = load(path); drum_center(js); save(path, js)
final_gain(path, {"めくる2": 0.7})                                       # v9: 2ページめ → めくる2 で仕上げの音量が 1.7dB 下がっていたのを、1.5dB より小さくする
