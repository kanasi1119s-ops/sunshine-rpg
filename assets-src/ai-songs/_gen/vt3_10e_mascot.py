# vt3 10「着ぐるみの中は38度」38 Degrees Inside the Suit（仮）— 明るい K-POP。4分の4・124。ホ長調 → 最後のサビから全音上の嬰ヘ長調。約4分50秒。
# 第3弾（0時〜24時の街）の 9時。
#
# v1（2026-11-21）: 人間「10は最初から作り直そう。10、11ともに緩急をつけるのと。5分ぐらいの曲で物語も作り直そう。」→ 物語の案から「10はa」。
#   前の 10（自動ドアのランウェイ・教科書の落書きたち）は使わない。旋律・歌詞・和音・構成はすべて新しく書いた。
#
# コンセプト: 駅前で風船を配る着ぐるみ。外では元気に踊り、中では汗だくで息を整える。
# 緩急: 「外」＝明るい音が全部鳴る／「中」＝音がこもって、心臓の音のようなキックと小さな声だけ。これを行き来する。山は3つで、3つとも形を変える。
# 物語の出来事 → その時の音:
#   中（はじまり）       → こもったキックが「ドッ・ドッ」。低いパッドだけ
#   外に出る             → プラックのフックと手びょうしが入って、音がひらく
#   外1（風船を配る）    → ポップスのビート、はねるベース、右のピアノ
#   中1（のぞき窓）      → こもったキックと低いパッド。歌は低く、ゆっくり
#   かけ声               → キックが消えて和音が上がる。最後の1拍は無音
#   サビ1（山1）         → 4つ打ち、左右のピアノ、短いシンセの和音。後半は歌なしのフックと声のチョップ
#   中2（あとすこし）    → もう一度こもる
#   外2（みんなが笑う）  → はねるビートに切りかわる
#   サビ2（山2）         → 16分のハイハットとベルの合いの手が加わる
#   ダンスブレイク       → 歌なし。ベースの旋律。プラックが合いことばの節を2回
#   中3（風船がひとつ飛ぶ）→ いちばん長い静けさ。ピアノと声だけ → 1小節の無音
#   最後のサビ（山3）    → 全音上がる。24小節。いちばん大きい
#   中（おわり）         → こもったキックと、ひとこと
# この曲だけの物: 「外」と「中」。中の場面は、キックもパッドも高い音を切った別のパートで鳴らす。
# 合いことばの節（3・5・6・5・2）: ダンスブレイクで、プラックが2回鳴らす（アルバムの決まり）。
# 歌詞: 曲名は歌わない。「きぐるみ」「38」も使わない。声: クリア 1 種類。
from vocalo_lib import *

S = Song("10", "mascot", "着ぐるみの中は38度（仮）", "38 Degrees Inside the Suit", 124, 4, "E", "major", "明るい K-POP（ボカロ）")
S.kit = "electro"; S.flags = S.flags + " --piano salamander --space room --space-wet 0.08"
K1, K2 = Key("E", "major"), Key("F#", "major")


def up2(chs): return [tr_chord(c, 2) for c in chs]


OCH = ["E", "C#m7", "A", "B"]                                              # 外
ICH = ["C#m7", "C#m7", "Amaj7", "Amaj7", "F#m7", "F#m7", "B7sus4", "B7sus4"]    # 中
PCH = ["Amaj7", "B", "G#m7", "C#m7", "Amaj7", "B", "B7sus4", "B"]
CCH = ["A", "B", "E", "C#m7", "A", "B", "G#m7", "C#m7", "A", "B", "E", "C#m7", "F#m7", "B", "E", "E"]
S.scene("中", 4, "intro", ICH[:4])
S.scene("外に出る", 4, "intro", ["A", "B", "A", "B"])
S.scene("外1", 16, "verse", OCH * 4)
S.scene("中1", 8, "bridge", ICH)
S.scene("かけ声", 8, "pre", PCH)
S.scene("サビ1", 8, "chorus", CCH[:8])
S.scene("フック1", 8, "break", CCH[8:])
S.scene("中2", 8, "bridge", ICH)
S.scene("外2", 8, "verse", OCH * 2)
S.scene("かけ声2", 8, "pre", PCH)
S.scene("サビ2", 8, "chorus", CCH[:8])
S.scene("フック2", 8, "break", CCH[8:])
S.scene("ダンスブレイク", 8, "break", ["E", "E", "A", "A", "C#m7", "C#m7", "B", "B"])
S.scene("中3", 16, "bridge", ICH + ICH[:6] + ["B7sus4", "C#7"])
S.scene("最後のサビ", 16, "chorus", up2(CCH[:8] + CCH[:8]))
S.scene("最後のフック", 8, "break", up2(CCH[8:]))
S.scene("中（おわり）", 6, "outro", up2(["Amaj7", "Amaj7", "E", "E", "E", "E"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("最後のサビ")[0]


def KEY(b): return K2 if b >= MOD else K1
def lp(f): return [{"type": "filter", "kind": "highpass", "freq": 35, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": f, "q": 0.7}]


PING = [{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}]
V = Voice(S, vol=0.16, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
KM = S.track("こもったキック（心臓の音）", "kick", volume=0.11, pan=0, fx=lp(240))
PADM = [S.track(f"こもったパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.07, pan=0.0, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 700, "q": 0.7}]) for i in range(3)]
SUB = S.track("サブベース（のばす）", "bass", patch="kfbSub", volume=0.05, pan=0, duck=0.4, fx=[{"type": "filter", "kind": "highpass", "freq": 32, "q": 0.7}])
RB = S.track("はねるシンセベース", "bass", patch="surgeBassAnalogBassImaged", volume=0.1, pan=0, duck=0.3)
STAB = [S.track(f"短いシンセの和音{i + 1}", "lead", patch="surgeChordReset", volume=0.1, pan=0.0, reverb=0.2, duck=0.3, fx=[{"type": "widen", "amount": 1.6}]) for i in range(3)]
PAD = [S.track(f"上がっていく和音{i + 1}", "pad", patch="surgePadSparkly", volume=0.04, pan=0.0, reverb=0.35, fx=[{"type": "boost", "gain": 2}, {"type": "widen", "amount": 1.4}]) for i in range(3)]
PLK = S.track("プラック（フック）", "lead", patch="kfbSquarePluck", volume=0.07, pan=0.3, reverb=0.25, fx=PING)
BELL = S.track("ベルの合いの手", "lead", patch="kfbBrightBells", volume=0.09, pan=-0.25, reverb=0.3)
PNL = [S.track(f"左のピアノ{i + 1}", "piano", volume=0.06, pan=-0.55, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(3)]
PNR = [S.track(f"右のピアノ{i + 1}", "piano", volume=0.06, pan=0.55, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(3)]
CLP = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = E4。最後のサビからは 1 = F#4）=================
VO_ = ["5:0.5 5:0.5 6:0.5 5:0.5 3:1 5:1", "6:1 5:1.5 R:1.5", "5:0.5 5:0.5 6:0.5 5:0.5 3:1 2:1", "3:1 1:1.5 R:1.5",
       "6:0.5 6:0.5 1':0.5 6:0.5 5:1 6:1", "1':1 6:1.5 R:1.5", "5:0.5 6:0.5 5:0.5 3:0.5 2:1 3:1", "2:1 1:1.5 R:1.5"]             # 外: はねる
VI = ["1:1.5 2:0.5 3:1.5 2:0.5", "1:2.5 R:1.5", "3:1.5 2:0.5 1:1.5 6,:0.5", "7,:2.5 R:1.5", "1:1.5 3:0.5 5:1.5 3:0.5", "2:2.5 R:1.5", "3:1.5 2:0.5 1:1.5 7,:0.5", "1:2.5 R:1.5"]    # 中: 低く、ゆっくり
VP = ["3:1.5 3:0.5 5:1.5 5:0.5", "6:2.5 R:1.5", "4:1.5 4:0.5 6:1.5 6:0.5", "1':2.5 R:1.5", "5:1.5 6:0.5 1':1.5 6:0.5", "1':2.5 R:1.5", "6:1.5 6:0.5 1':1 R:1", "R:4"]
HK = "3:0.5 5:0.5 6:1 R:0.5 3:0.5 5:0.5 6:0.5"                             # フック（ふ・わ・り を2回）
VC = [HK, "1':1 6:1 5:1 R:1", HK, "1':1 1':1 6:1 R:1", "5:1 5:0.5 6:1 6:0.5 1':1", "6:1 5:1 3:1 R:1", HK, "5:1 3:1 1:1 R:1"]
C1 = "ふわりふわりとぶよ/ふわりふわりわらう/なかはひみつだよ/ふわりふわりきみへ"
C2 = "ふわりふわりゆれる/ふわりふわりとどく/いろをわけあおう/ふわりふわりきみへ"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("外1", VO_ + VO_, "えきまえひろばで/てをふるくまさん/あかあおきいろの/ふうせんくばるよ/こどもがかけより/だきついてくるよ/おおきなあたまを/かしげてこたえる")
put("中1", VI, "のぞきまど/ひたいから/あせがおち/いきをする")
put("かけ声", VP, "さあいこう/てをひろげ/とびだして/いまだ")
put("サビ1", VC, C1)
put("中2", VI, "あとすこし/がんばれと/じぶんにね/いいきかす")
put("外2", VO_, "みぎてをあげれば/みんながわらうよ/くるりとまわれば/かめらがならぶよ")
put("かけ声2", VP, "もういちど/えがおだけ/とどけたい/いまだ")
put("サビ2", VC, C2)
put("中3", VI + VI[:4], "ふうせんが/ひとつだけ/そらへゆく/なくこには/ぼくのぶん/わたそうか", bars=S.sc("中3")[:12])
put("最後のサビ", VC + VC, C1 + "/" + C2)
put("中（おわり）", VI[:2], "またあとで", bars=S.sc("中（おわり）")[:2])


# ================= 伴奏 =================
def rlow(b, lo="E1"): return low(S.chords[b], lo)


def seq(b, pat):
    """シンセベースを16分のマスで。r＝根音、R＝1オクターブ上、5＝5度、6＝6度、.＝休み、-＝のばす"""
    r = rlow(b); out = []; i = 0
    while i < 16:
        c = pat[i]; L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if c == "." else f"{N(r + {'r': 0, 'R': 12, '5': 7, '6': 9}[c])}:{L * 0.25:g}"); i += L
    RB.bar(b, " ".join(out))


def stab(b, pat, center=67):
    v = sorted(voice(S.chords[b], center, 3))
    for j in range(3): STAB[j].bar(b, steps(pat, [N(v[j])] * pat.count("x"), short=0.5))


def pad(b, lift=0, pat=None, tr=None):
    v = sorted(voice(S.chords[b], (62 if tr is None else 55) + lift, 3))
    for j in range(3): (tr or PAD)[j].bar(b, pat.replace("N", N(v[j])) if pat else f"{N(v[j])}:4")


def piano(b, patL=None, patR=None):
    lo = sorted(voice(S.chords[b], 60, 3)); hi = sorted(voice(S.chords[b], 72, 3))
    for j in range(3):
        if patL: PNL[j].bar(b, steps(patL, [N(lo[j])] * patL.count("x"), short=0.5))
        if patR: PNR[j].bar(b, steps(patR, [N(hi[j])] * patR.count("x"), short=0.5))


def hook(b, k=0): PLK.bar(b, KEY(b).mel((HK, "R:1 1':0.5 6:0.5 5:1 6:1")[k], oct=5))
def clap(b, pat="R:1 B4:1 R:1 B4:1"): CLP.bar(b, pat)
def heart(b, pat="x:0.5 x:1.5 R:2"): KM.bar(b, pat)                        # ドッ・ドッ


def inside(b, i, L, piano_too=False):
    """中: こもったキックと低いパッド。歌は低く、ゆっくり"""
    heart(b, "x:0.5 x:1.5 R:2" if i % 2 == 0 else "x:0.5 x:1.5 x:0.5 x:1.5"); pad(b, tr=PADM); SUB.bar(b, f"{N(rlow(b))}:4")
    if piano_too and i % 2 == 1: piano(b, patR="........x...x...")


K4 = "X...X...X...X..."
POP = [("X.....x.X.......", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X.....x.X..x....", "....X.......X..x", "x.x.x.x.x.x.x.xx")]
HOPB = [("X..x....X.x.....", "....X.......X...", "x.xxx.x.x.xxx.x."), ("X..x..x...X..x..", "....X..x....X...", "x.x.xxx.x.x.xxx.")]
FOUR = [(K4, "....X.......X...", "..x...x...x...x."), (K4, "....X.......X..x", "..x...x...x..xx.")]
FOUR16 = [(K4, "....X.......X...", "x.xxx.xxx.xxx.xx"), (K4, "....X.......X.xx", "x.xxx.xxx.xxx.x.")]
TURN = [("X.....X..X......", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X..X.....X..X...", "....X..x....X...", "x.xxx.x.x.xxx.xx")]
BRK = ["E2:1 R:0.5 E2:0.5 C#2:0.5 B1:0.5 G#1:1", "E1:0.5 F#1:0.5 G#1:0.5 B1:1 C#2:0.5 E2:1", "A1:1 R:0.5 A1:0.5 G#1:0.5 E1:0.5 C#2:1", "A1:0.5 C#2:0.5 E2:0.5 F#2:1 E2:0.5 C#2:1",
       "C#2:1 R:0.5 C#2:0.5 B1:0.5 G#1:0.5 E2:1", "C#2:0.5 E2:0.5 F#2:0.5 G#2:1 B2:0.5 C#3:1", "B1:1 R:0.5 B1:0.5 A1:0.5 F#1:0.5 D#2:1", "B1:0.5 D#2:0.5 F#2:0.5 A2:0.5 B2:2"]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）


def chorus(b, i, size):
    """サビとフック。size 1＝山1、2＝山2（16分のハイハットとベル）、3＝山3（さらにパッド）"""
    g = (FOUR if size == 1 else FOUR16)[i % 2]; D.set(b, g[0], g[1] if i % 8 != 7 else "....X.......X.XX", g[2]); clap(b)
    if i % 8 == 0: crash(D, b, "C2", 4)
    seq(b, "r-.r-.R-r-.r-.R-" if i % 2 == 0 else "r-.r-.R-r-R-5-6-"); SUB.bar(b, f"{N(rlow(b))}:4")
    piano(b, "x..x..x...x.x...", "..x..x..x..x..x."); stab(b, "x..x..x....x..x." if i % 2 == 0 else "x..x......x..x..")
    if size >= 2 and i % 2 == 1: BELL.bar(b, KEY(b).mel("R:2.5 1':0.5 2':0.5 3':0.5", oct=5))
    if size >= 3: pad(b)


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "中":                                                        # こもったキックと低いパッドだけ
        inside(b, i, L)
    elif n == "外に出る":                                                # プラックのフックと手びょうしで、音がひらく
        heart(b, "x:1 x:1 x:1 x:1"); hook(b, i % 2); clap(b); SUB.bar(b, f"{N(rlow(b))}:4"); pad(b, i * 2)
        if i >= 2: seq(b, "r-.r-.R-........" if i == 2 else "r-.r-.R-r-R-5-6-")
        if last: D.set(b, "................", "........x.x.xxxx", "................")
    elif n in ("外1", "外2"):
        two = n == "外2"; late = i >= 8
        g = (HOPB if two else POP)[i % 2]; D.set(b, g[0], g[1] if not last else g[1][:12] + "x.xx", g[2]); clap(b)
        seq(b, ("r-..r-R-..r-R-5-" if not odd else "r-..r-R-r-..5-6-") if not two else ("r--R--r-.r-R..5-" if not odd else "r--R--r-r-.6-R-.")); SUB.bar(b, f"{N(rlow(b))}:2.5 R:1.5")
        piano(b, patR="..x.....x..x...." if not odd else "..x..x....x.....")
        if late or two: stab(b, "......x...x....." if not odd else "......x..x......", center=64)
        if odd and (late or two): PLK.bar(b, KEY(b).mel(("R:3 5:0.5 6:0.5", "R:2.5 6:0.5 1':0.5 6:0.5")[(i // 2) % 2], oct=5))
    elif n in ("中1", "中2"): inside(b, i, L)
    elif n == "中3":                                                     # いちばん長い静けさ。ピアノと声だけ → 1小節の無音
        if i < 12: inside(b, i, L, piano_too=True)
        elif i < 15: pad(b, tr=PADM, lift=(i - 12) * 2); pad(b, (i - 12) * 2); heart(b, "x:1 x:1 x:1 x:1" if i == 14 else "x:0.5 x:1.5 x:0.5 x:1.5")
        if i == 14: D.set(b, "................", "x...x...x.x.xxxx", "................")
    elif n in ("かけ声", "かけ声2"):                                     # キックが消え、和音が上がる。最後の1拍は無音
        if last:
            pad(b, i * 2, pat="N:3 R:1"); D.set(b, "................", "x.x.x.xxxxxx....", "................"); continue
        pad(b, i * 2); clap(b, "R:1 B4:1 R:1 B4:1" if i >= 4 else "R:3 B4:1"); D.set(b, "................", "................" if i < 6 else "x...x...x.x.x.x.", "x...x...x...x..." if i < 4 else "x.x.x.x.x.x.x.x.")
        SUB.bar(b, f"{N(rlow(b))}:4")
        if i >= 4: piano(b, patR="x...x...x...x...")
        if n == "かけ声2" and not odd: hook(b, 1)
    elif n in ("サビ1", "フック1"): chorus(b, i, 1); (hook(b, i % 2) if n == "フック1" else None)
    elif n in ("サビ2", "フック2"): chorus(b, i, 2); (hook(b, i % 2) if n == "フック2" else None)
    elif n in ("最後のサビ", "最後のフック"): chorus(b, i, 3); (hook(b, i % 2) if n == "最後のフック" or i >= 8 else None)
    elif n == "ダンスブレイク":                                          # 歌なし。ベースの旋律。プラックが合いことばの節を2回
        g = TURN[i % 2]; D.set(b, g[0], g[1] if not last else "....X...X...XXXX", g[2]); RB.bar(b, BRK[i]); clap(b); SUB.bar(b, f"{N(rlow(b))}:4")
        stab(b, "x.....x...x....."); piano(b, "x.....x...x.....", "...x.....x...x..")
        if i in (0, 1, 4, 5): PLK.bar(b, K1.mel(MOT[i % 2], oct=5))
    elif n == "中（おわり）":                                            # こもったキックと、ひとこと
        if i < 5: inside(b, i, L)
        else: heart(b, "x:0.5 x:1.5 R:2")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の10（9時）。明るい K-POP（124・ホ長調 → 嬰ヘ長調）。駅前で風船を配る、かぶりものの中の人の話。"
          "こもったキックで始まる → 音がひらく → 外（明るいビート）と中（こもった音と小さな声）を行き来する → 山は3つ（4つ打ち → 16分のハイハットとベル → 全音上げて24小節）→ "
          "いちばん長い静けさと1小節の無音 → こもったキックで終わる。自作")
finish(S, LY, V, 0, flat=True)                                           # 山の大きさは、場面ごとの楽器の数で決める（曲全体の山は打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "はねるシンセベース", mid=92, down=12, up=10, seed=10); humanize(path, "プラック（フック）", mid=86, down=10, up=12, seed=5)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 20, "bridge": 4, "outro": 4}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("最後のサビ", 0, None, K2)], vol=0.34)
    bars = {}
    for name, sh in (("フック1", 0), ("フック2", 0), ("最後のフック", 2)):  # サビのあと: 声のチョップで「ふ・わ・り」
        sc = S.sc(name); p = lambda q: nm(midi(q) + sh)
        for i in range(8): bars[sc[i]] = f"{p('G#4')}:0.5:ふ {p('B4')}:0.5:わ {p('C#5')}:1:り R:2" if i % 2 == 0 else f"R:2 {p('G#4')}:0.5:ふ {p('B4')}:0.5:わ {p('C#5')}:1:り"
    chops(path, S, bars, vol=0.3, pan=-0.25)
    voice_by_scene(path, S, {}, default="clear")                          # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
# 緩急: 外（Aメロ）は全員が少しおさえて弾く（−3dB）。山との差を楽器の数だけに頼らない
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in (("外に出る", 0.78), ("外1", 0.7), ("外2", 0.7), ("中", 0.8), ("中1", 0.8), ("中2", 0.8), ("中3", 0.8), ("中（おわり）", 0.8)):   # 中は、さらに小さく（山との差 8dB 以上）
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    p_["barGain"] = g[:S.nb]
save(path, js)
