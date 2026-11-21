# vt3 10「自動ドアのランウェイ」Sliding-Door Runway（仮）— 明るい K-POP（場面ごとにビートが切りかわるダンスポップ）。4分の4・124。ト長調 → 最後のサビから全音上のイ長調。
# v3（2026-11-21）: 人間「10はもっと明るくした曲調に変えよう」。短調 → 長調、歪んだギター → 左右のピアノの和音、テンポ 120 → 124、和音の進み方も長調で書き直した。
#   v1・v2（短調・歪んだギター）は、歌の入るサビだけ点が低かった（場面ごとに測ると 5.7〜6.3。Aメロは 7.8〜8.0）。
# 第3弾（0時〜24時の街）の 9時。
#
# v1（2026-11-21）: 曲名も物語も新しくして、ゼロから作った。前の 10 は「教科書の落書きたち」（ブルーグラス `vt3_10_doodles.py`、K-POP の試し書き `vt3_10c_doodles.py`）。
#   人間の指示: 「曲自体初めから1011は作り直そう。KPOPとKawaii_future_bassで。全く新しい曲で」→「曲名も物語も新しく」→ 3つの案から「Aで」（2026-11-21）。
#
# コンセプト: 9時。ビルの自動ドアが開くたび、通勤の人がモデルのように歩いて入っていく。自分も胸を張って入る。
# ジャンル: K-POP。決まりごと（出どころは docs/sound/vt3-remake-plan.md）:
#   ・場面ごとに対比をつける（Aメロ → Bメロで持ち上げ → フックのサビ → サビのあとのフック → ダンスブレイク → 最後のサビで転調）
#   ・テンポ 120〜135。808 のキック、シンセの短い和音、声のチョップ、かけ声のフック
#
# 物語の出来事 → その時の音:
#   くつ音             → 右足・左足の「コツ、コツ」（高さのちがう2音）がそのままビートになる
#   歩道               → くつ音とキック、休みの多いシンセベースのリフだけ。音は真ん中に集める
#   ドアの前           → キックが消えて和音が上がる。ドアのチャイム（上がる2音）→ 1拍の無音
#   ドアが開く（サビ） → 音が一気に左右に広がる。4つ打ち、ウラで鳴るベース、左右のピアノ、短いシンセの和音
#   床がひかる         → 歌なしのフック（プラックと声のチョップ「あ・る・け」）
#   鏡の柱             → はねるビートに切りかわり、プラックが合いの手
#   ターン             → 歌なし。ベースの旋律とドラム。プラックが合いことばの節を2回
#   立ち止まる         → 1小節の無音 → 小さな声 → スネアが細かくなる
#   最後のサビ         → 全音上がる
#   ドアが閉まる       → チャイム（下がる2音）と、くつ音で終わる
# この曲だけの物: くつ音のビート。ドアが開くと、真ん中に集めていた音が左右に広がる。
# 合いことばの節（3・5・6・5・2）: ターンで、プラックが2回鳴らす（アルバムの決まり）。
# 歌詞: 曲名は歌わない。「じどうドア」「ランウェイ」も使わない。声: クリア 1 種類。
from vocalo_lib import *

S = Song("10", "runway", "自動ドアのランウェイ（仮）", "Sliding-Door Runway", 124, 4, "G", "major", "明るい K-POP（ボカロ）")
S.kit = "electro"; S.flags = S.flags + " --piano salamander --space room --space-wet 0.08"
K1, K2 = Key("G", "major"), Key("A", "major")


def up2(chs): return [tr_chord(c, 2) for c in chs]


VCH = ["G", "Bm7", "Cmaj7", "D"]
PCH = ["Am7", "Bm7", "Cmaj7", "D", "Am7", "Bm7", "D7sus4", "D7"]
CCH = ["G", "D", "Em7", "Cmaj7", "G", "D", "Am7", "D"]
S.scene("くつ音", 4, "intro", ["G", "G", "Cmaj7", "D"])
S.scene("歩道", 8, "verse", VCH * 2)
S.scene("ガラスの向こう", 8, "verse", VCH * 2)
S.scene("ドアの前", 8, "pre", PCH)
S.scene("ドアが開く1", 8, "chorus", CCH)
S.scene("床がひかる", 8, "break", CCH)
S.scene("鏡の柱", 8, "verse", VCH * 2)
S.scene("ドアの前2", 8, "pre", PCH)
S.scene("ドアが開く2", 8, "chorus", CCH)
S.scene("ターン", 8, "break", ["G", "G", "Cmaj7", "Cmaj7", "Am7", "Am7", "D", "D"])
S.scene("立ち止まる", 4, "bridge", ["Em7", "Cmaj7", "D", "E7"])
S.scene("最後のサビ", 16, "chorus", up2(CCH + CCH[:7] + ["G"]))
S.scene("ドアが閉まる", 6, "outro", up2(["G", "Cmaj7", "G", "Cmaj7", "G", "G"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("最後のサビ")[0]


def KEY(b): return K2 if b >= MOD else K1


PING = [{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}]
V = Voice(S, vol=0.16, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
HEEL = S.track("くつ音（カホンの縁）", "cajon", volume=0.2, pan=0.0, reverb=0.12, fx=[{"type": "boost", "gain": 14}])
SUB = S.track("サブベース（のばす）", "bass", patch="kfbSub", volume=0.05, pan=0, duck=0.4, fx=[{"type": "filter", "kind": "highpass", "freq": 32, "q": 0.7}])
RB = S.track("シンセベースのリフ", "bass", patch="kfbFmBass", volume=0.085, pan=0, duck=0.3, fx=rack_bass())
STAB = [S.track(f"短いシンセの和音{i + 1}", "lead", patch="surgeChordReset", volume=0.1, pan=0.0, reverb=0.2, duck=0.3, fx=[{"type": "widen", "amount": 1.6}]) for i in range(3)]
PAD = [S.track(f"上がっていく和音{i + 1}", "pad", patch="surgePadBright", volume=0.12, pan=0.0, reverb=0.35, fx=[{"type": "boost", "gain": 2}, {"type": "widen", "amount": 1.4}]) for i in range(3)]
PLK = S.track("プラック（フック）", "lead", patch="surgeNicePluck", volume=0.09, pan=0.3, reverb=0.25, fx=PING)
BELL = S.track("ドアのチャイム", "lead", patch="kfbBrightBells", volume=0.1, pan=-0.2, reverb=0.35)
PNL = [S.track(f"左のピアノ{i + 1}", "piano", volume=0.06, pan=-0.55, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(3)]
PNR = [S.track(f"右のピアノ{i + 1}", "piano", volume=0.06, pan=0.55, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(3)]
CLP = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = G4。最後のサビからは 1 = A4）=================
VA = ["1:0.5 1:0.5 R:0.5 3:0.5 1:1 7,:1", "5,:0.5 7,:0.5 1:2 R:1", "1:0.5 1:0.5 R:0.5 3:0.5 4:1 3:1", "2:0.5 4:0.5 2:2 R:1",
      "3:0.5 3:0.5 R:0.5 5:0.5 3:1 1:1", "7,:0.5 1:0.5 3:2 R:1", "4:0.5 4:0.5 R:0.5 5:0.5 4:1 3:1", "2:0.5 2:0.5 2:2 R:1"]
VP = ["3:1 5:1 7:1.5 5:0.5", "4:3 R:1", "2:1 4:1 6:1.5 4:0.5", "3:3 R:1", "3:1 5:1 1':1.5 7:0.5", "2':3 R:1", "1':1 7:1 5:1 R:1", "R:4"]
HK = "5:0.75 5:0.75 3:1.5 R:1"                                             # 3音のフック（あ・る・け）
VC = [HK, "3:0.5 4:0.5 5:1 7:0.5 5:0.5 R:1", HK, "4:0.5 5:0.5 6:1 1':0.5 6:0.5 R:1", "1':1.5 7:0.5 5:1 3:1", "4:0.5 5:0.5 6:1 5:1 R:1", HK, "2:0.5 3:0.5 1:2 R:1"]
VT = ["3:1 2:1 1:1.5 2:0.5", "3:3 R:1"]
C1 = "あるけ/むねをはれ/あるけ/かおあげて/ひかりのまんなか/あるけ/わたし"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("歩道", VA, "くつおとがそろう/あさのほどうでは/だれもかれもみな/まえだけをみてる")
put("ガラスの向こう", VA, "がらすのむこうに/ひかるゆかがある/せすじをのばして/あごをすこしあげ")
put("ドアの前", VP, "あとごほで/せんをこす/いまわたし/ひらけ")
put("ドアが開く1", VC, C1)
put("鏡の柱", VA, "かがみのはしらに/うつるよこがおは/きのうよりすこし/つよくみえるかな")
put("ドアの前2", VP, "もういちど/むねをはり/このさきへ/すすめ")
put("ドアが開く2", VC, C1)
put("立ち止まる", VT, "これでいい", bars=S.sc("立ち止まる")[1:3])
put("最後のサビ", VC + VC, C1 + "/" + C1)


# ================= 伴奏 =================
def rlow(b, lo="E1"): return low(S.chords[b], lo)


def seq(b, pat):
    """シンセベースを16分のマスで。r＝根音、R＝1オクターブ上、5＝5度、7＝短7度、.＝休み、-＝のばす"""
    r = rlow(b); out = []; i = 0
    while i < 16:
        c = pat[i]; L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if c == "." else f"{N(r + {'r': 0, 'R': 12, '5': 7, '7': 9}[c])}:{L * 0.25:g}"); i += L
    RB.bar(b, " ".join(out))


def stab(b, pat, center=67):
    v = sorted(voice(S.chords[b], center, 3))
    for j in range(3): STAB[j].bar(b, steps(pat, [N(v[j])] * pat.count("x"), short=0.5))


def pad(b, lift=0, pat=None):
    v = sorted(voice(S.chords[b], 62 + lift, 3))
    for j in range(3): PAD[j].bar(b, pat.replace("N", N(v[j])) if pat else f"{N(v[j])}:4")


def hook(b, k=0): PLK.bar(b, KEY(b).mel(("5:0.75 5:0.75 3:1.5 R:1", "R:1 7:0.5 5:0.5 3:1 5:1")[k], oct=5))        # フックの音型（歌のフックと同じ 5・5・3）と、その答え
def gtr(b, patL="x..x..x...x.x...", patR="..x..x..x..x..x."):
    """ドアが開いたあとの、左右のピアノの和音（左は低め、右は高め。リズムをずらして左右でかけ合う）"""
    lo = sorted(voice(S.chords[b], 60, 3)); hi = sorted(voice(S.chords[b], 72, 3))
    for j in range(3): PNL[j].bar(b, steps(patL, [N(lo[j])] * patL.count("x"), short=0.5)); PNR[j].bar(b, steps(patR, [N(hi[j])] * patR.count("x"), short=0.5))


def clap(b, pat="R:1 B4:1 R:1 B4:1"): CLP.bar(b, pat)
def heel(b, pat="E3:1 G3:1 E3:1 G3:1"): HEEL.bar(b, pat)                   # 右足・左足


K4 = "X...X...X...X..."
WALK = [("X.........X.....", "................", "................"), ("X.......X..x....", "................", "................")]                      # 歩道: キックだけ（くつ音がビート）
WALK2 = [("X.........X.....", "............X...", "x.x.x.x.x.x.x.x."), ("X.......X..x....", "............X..x", "x.x.x.xxx.x.x.x.")]
TURN = [("X.....X..X......", "....X.......X...", ""), ("X..X.....X..X...", "....X..x....X...", "")]
BOUNCE = [("X.....X...X..X..", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X..X......X...X.", "....X.......X..x", "x.xxx.x.x.xxx.x.")]
FOUR = [(K4, "....X.......X...", "..x...x...x...x."), (K4, "....X.......X..x", "..x...x...x..xx.")]
BRK = ["G1:1 R:0.5 G2:0.5 E2:0.5 D2:0.5 B1:1", "G1:0.5 A1:0.5 B1:0.5 D2:1 E2:0.5 G2:1", "C2:1 R:0.5 C2:0.5 B1:0.5 G1:0.5 E2:1", "C2:0.5 E2:0.5 G2:0.5 A2:1 G2:0.5 E2:1",
       "A1:1 R:0.5 A1:0.5 G1:0.5 E1:0.5 C2:1", "A1:0.5 C2:0.5 D2:0.5 E2:1 G2:0.5 A2:1", "D2:1 R:0.5 D2:0.5 C2:0.5 A1:0.5 F#1:1", "D1:0.5 F#1:0.5 A1:0.5 C2:0.5 D2:2"]
MOT = ["3:1 5:0.5 6:1 5:0.5 R:1", "2:2 R:2"]                               # 合いことばの節（3・5・6・5・2）

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "くつ音":                                                    # くつ音だけ → 低いベース → リフ
        heel(b)
        SUB.bar(b, f"{N(rlow(b))}:4")                                      # くつ音だけだと小さすぎた（−30dB）ので、低いベースは頭から
        if i >= 1: seq(b, "r-.r..7-r-......" if i != 3 else "r-.r..7-R-..5-7-")
        if i == 3: D.set(b, "................", "............x.xx", "................")
    elif n in ("歩道", "ガラスの向こう"):                                # くつ音とキック、休みの多いリフ。真ん中に集める
        late = n == "ガラスの向こう"; g = (WALK2 if late else WALK)[i % 2]; D.set(b, g[0], g[1] if not last else "........x.x.xxxx", g[2])
        heel(b); seq(b, "r-.r..7-r-......" if not odd else "r-.r..7-R-..5-7-"); SUB.bar(b, f"{N(rlow(b))}:2.5 R:1.5")
        stab(b, "......x........." if not odd else "......x..x......", center=64)   # v2: 歌がはだかにならないよう、短い和音は頭から、パッドは後半から
        if late: clap(b, "R:3 B4:1"); pad(b)
    elif n == "鏡の柱":                                                  # はねるビート。プラックが合いの手
        g = BOUNCE[i % 2]; D.set(b, g[0], g[1] if not last else g[1][:12] + "x.xx", g[2]); heel(b, "E3:0.75 G3:0.75 E3:0.5 G3:1 E3:1")
        seq(b, "r--R--r-.r-R..5-" if not odd else "r--R--r-r-.7-R-."); SUB.bar(b, f"{N(rlow(b))}:1.5 R:1 {N(rlow(b))}:1.5"); clap(b); stab(b, "..x.....x..x....")
        if odd: PLK.bar(b, KEY(b).mel(("R:3 1':0.5 7:0.5", "R:2.5 5:0.5 7:0.5 1':0.5")[(i // 2) % 2], oct=5))
    elif n in ("ドアの前", "ドアの前2"):                                 # キックが消え、和音が上がる。チャイム → 1拍の無音
        if last:
            pad(b, i * 2, pat="N:3 R:1"); BELL.bar(b, KEY(b).mel("R:1 5:1 1':1 R:1", oct=5)); D.set(b, "................", "x.x.x.xxxxxx....", "................"); continue
        pad(b, i * 2); heel(b); D.set(b, "................", "................" if i < 4 else ("....x.......x..." if i < 6 else "x...x...x.x.x.x."), "x...x...x...x...")
        if i >= 4: SUB.bar(b, f"{N(rlow(b))}:4")
        if n == "ドアの前2" and not odd: hook(b, 1)
    elif n in ("ドアが開く1", "床がひかる", "ドアが開く2", "最後のサビ"):  # 音が左右に広がる。4つ打ち、ウラで鳴るベース、左右のピアノ
        fin = n == "最後のサビ"; two = n == "ドアが開く2"; post = n == "床がひかる"
        g = FOUR[i % 2]; D.set(b, g[0], g[1] if i % 8 != 7 else "....X.......X.XX", g[2] if not (two or fin) else "x.x.x.x.x.x.x.x."); clap(b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        seq(b, "..r-..r-..R-..r-" if not odd else "..r-..r-..R-.r5-"); SUB.bar(b, f"{N(rlow(b))}:4"); gtr(b)
        stab(b, "x..x..x....x..x." if not odd else "x..x......x..x..")
        if post or (fin and i >= 8): hook(b, i % 2)                       # 歌なしの所と、最後のくり返しでフックの音型
    elif n == "ターン":                                                  # 歌なし。ベースの旋律とドラム。プラックが合いことばの節を2回
        g = TURN[i % 2]; D.set(b, g[0], g[1] if not last else "....X...X...XXXX", "x.xxx.x.x.xxx.xx"); RB.bar(b, BRK[i]); clap(b); SUB.bar(b, f"{N(rlow(b))}:4")
        stab(b, "x.....x...x.....")
        if i in (0, 1, 4, 5): PLK.bar(b, K1.mel(MOT[i % 2], oct=5))
        gtr(b, "x.....x...x.....", "...x.....x...x..")
    elif n == "立ち止まる":                                              # 1小節の無音 → 小さな声 → スネアが細かくなる
        if i in (1, 2): pad(b)
        if i == 3: D.set(b, "X...X...X.X.X.X.", "x...x...x.x.xxxx", "................"); pad(b, 4); seq(b, "r-r-r-r-rrrrRRRR")
    elif n == "ドアが閉まる":                                            # チャイム（下がる2音）と、くつ音で終わる
        if i < 4: heel(b); SUB.bar(b, f"{N(rlow(b))}:4"); hook(b, i % 2)
        if i == 0: crash(D, b, "C2", 4)
        if i == 4: heel(b, "E3:1 G3:1 R:2"); BELL.bar(b, KEY(b).mel("R:2 1':1 5:1", oct=5))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の10（9時）。明るい K-POP（124・ト長調 → イ長調）。ビルの入口を、モデルのように胸を張って歩いて入る話。"
          "くつ音で始まる → くつ音とリフだけの Aメロ → 和音が上がってチャイムと無音 → 音が左右に広がる4つ打ちのサビと3音のフック → はねるビート → "
          "ダンスブレイク → 1小節の無音 → 全音上がって最後のサビ → チャイムとくつ音で終わる。自作")
finish(S, LY, V, 0, flat=True)                                           # どのサビも同じ強さで鳴らす（曲全体の山を打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "シンセベースのリフ", mid=92, down=12, up=10, seed=10); humanize(path, "プラック（フック）", mid=86, down=10, up=12, seed=5)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 14, "chorus": 20, "bridge": 8}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("ドアが開く2", 0, None, K1), ("最後のサビ", 0, None, K2)], vol=0.34)
    bars = {}
    for name in ("床がひかる",):                                          # サビのあと: 声のチョップで「あ・る・け」
        sc = S.sc(name)
        for i in range(8): bars[sc[i]] = "D5:0.75:あ D5:0.75:る B4:1.5:け R:1" if i % 2 == 0 else "R:2 D5:0.5:あ D5:0.5:る B4:1:け"
    chops(path, S, bars, vol=0.3, pan=-0.25)
    voice_by_scene(path, S, {}, default="clear")                          # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
