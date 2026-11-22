# アイドル曲 01「午前0時のアンコール」Encore at Midnight（仮）— アイドルポップ。4分の4・164。イ長調 → 最後のサビから半音上の変ロ長調。約4分。
#
# v4（2026-11-23）: 人間「テトの声をキュートにして一音一音聞こえやすくしてください」→ 声を幼く明るく（フォルマント 1.13→1.16）、子音を強く（1.85→2.2）、音の移り変わりを速く（0.9→0.7）、
#   しゃくりを半分に（0.12→0.06）、声のやまびこを半分に（0.4→0.2）、声を少し大きく（0.16→0.175）、ハモリを小さく（0.26→0.2）。
# v3（2026-11-23）: 1番A・2番Aではないが同じ型のベースで、短く弾き直す所にパチッという音（尖度 57）が出ていたので、弾き直しをやめた。
# v2（2026-11-23）: 歌入りの点が 7.33（サビが 6.2〜6.5）。サビで歌の後ろの音を減らした（ギター 0.11→0.08、ピアノの右手は2・4拍だけ、短いシンセの和音は1小節おき）、サビの歌の強さ 20→15、ハモリ 0.34→0.26。
# v1（2026-11-23）: 人間「テトでアイドルっぽい曲作ろうか cメロも2番に入れよう。ストーリーを入れて。コンセプトはシンデレラにしよう。」→ 物語の案から「Aで」。
#
# コンセプト（シンデレラ。昔話そのものだけを元にする）: いつも後ろの列の子が、今夜だけ代役でまん中に立つ。
#   魔法＝衣装係が直してくれた借り物の衣装／12時＝終演の時刻（衣装を返す）／くつ＝舞台に落とした片方の髪かざり／むかえは待たず、自分で次の日へ行く。
# ジャンルの見本（アイドルポップの定番。くわしい資料は見つからず、知っている定番を見本にした）:
#   サビ頭／だんだん上がるBメロ／手びょうし／落ちサビ／最後の半音上げ。ぜんぶはなぞらない（Cメロで短調に寄せて鐘を数える、鐘で終わる）。
# 物語の出来事 → その時の音:
#   出だし（楽屋の鏡の前）      → 声と、オルゴールのようなベルの分散和音。低いパッド
#   前奏（舞台そでへ）          → ドラムが入り、ギターをかき鳴らす
#   1番A（後ろの列の毎日）      → ピアノとベース。ドラムは細かくきざまない。歌は低め
#   1番B（衣装にそでを通す）    → 手びょうしが入り、1段ずつ上がる。最後の1拍は無音
#   サビ1（幕が開く）           → 4つ打ち、左右のギター、キラキラ
#   2番A・B（まん中からの景色） → はねるビート。ギターが前に出る
#   Cメロ（終演が近づく）       → 小さく落とす。時計の針のハイハットと、電子の鐘を12回数える。短調に寄せる
#   サビ2（時間切れでも歌いきる）→ 鐘が鳴りつづける中で全員
#   落ちサビ（衣装を返した帰り道）→ 声とピアノだけ
#   最後のサビ（自分の足で次の日へ）→ 半音上げ。鐘が今度は始まりの合図
#   おわり                      → 鐘の余韻と、ひとこと
# この曲だけの物: 12回数える鐘。Cメロでは「終わり」、最後のサビでは「始まり」の合図になる。
# 歌詞: 曲名の言葉（ごぜん・れいじ・アンコール）と「シンデレラ」は歌わない。声: キュート 1 種類。オーケストラの楽器・アコーディオン・バンジョーは使わない。
import random as _r
from vocalo_lib import *
import gtr2_lib as G2

S = Song("26", "midnight-encore", "午前0時のアンコール（仮）", "Encore at Midnight", 164, 4, "A", "major", "アイドルポップ（ボカロ）")
S.kit = "electro"; S.flags = S.flags + " --piano salamander --space room --space-wet 0.08"
K1, K2 = Key("A", "major"), Key("Bb", "major")


def up1(chs): return [tr_chord(c, 1) for c in chs]


ACH = ["A", "E", "F#m7", "C#m7", "D", "A", "Bm7", "E"]
BCH = ["F#m7", "C#m7", "D", "E", "F#m7", "C#m7", "Bm7", "E7sus4"]
CCH = ["D", "E", "C#m7", "F#m7", "Bm7", "E", "A", "A7", "D", "E", "C#m7", "F#m7", "Bm7", "E7sus4", "A", "A"]
MCH = ["F#m7", "F#m7", "D", "D", "Bm7", "Bm7", "C#7", "C#7", "F#m7", "F#m7", "D", "D", "Bm7", "E", "E7sus4", "E"]
S.scene("出だし", 8, "intro", CCH[:8])
S.scene("前奏", 8, "intro", ["D", "E", "C#m7", "F#m7", "D", "E", "A", "A"])
S.scene("1番A", 16, "verse", ACH * 2)
S.scene("1番B", 8, "pre", BCH)
S.scene("サビ1", 16, "chorus", CCH)
S.scene("つなぎ", 8, "break", ["D", "E", "A", "A", "D", "E", "A", "A"])
S.scene("2番A", 16, "verse", ACH * 2)
S.scene("2番B", 8, "pre", BCH)
S.scene("Cメロ", 16, "bridge", MCH)
S.scene("サビ2", 16, "chorus", CCH)
S.scene("間奏", 8, "break", ["F#m7", "D", "A", "E", "F#m7", "D", "E", "E"])
S.scene("落ちサビ", 8, "bridge", CCH[:6] + ["A", "F7"])
S.scene("最後のサビ", 16, "chorus", up1(CCH))
S.scene("最後のサビ2", 8, "chorus", up1(CCH[8:]))
S.scene("おわり", 8, "outro", up1(["D", "E", "A", "A", "D", "E", "A", "A"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
MOD = S.sc("最後のサビ")[0]


def KEY(b): return K2 if b >= MOD else K1


V = Voice(S, vol=0.175, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
SUB = S.track("サブベース（のばす）", "bass", patch="kfbSub", volume=0.05, pan=0, duck=0.4, fx=[{"type": "filter", "kind": "highpass", "freq": 32, "q": 0.7}])
RB = S.track("指弾きのベース", "bass", volume=0.13, pan=0, duck=0.2)
STAB = [S.track(f"短いシンセの和音{i + 1}", "lead", patch="kfbSawStab", volume=0.07, pan=0.0, reverb=0.2, duck=0.3, fx=[{"type": "widen", "amount": 1.6}]) for i in range(3)]
PAD = [S.track(f"パッド{i + 1}", "pad", patch="kfbSparklePad", volume=0.05, pan=0.0, reverb=0.35, fx=[{"type": "widen", "amount": 1.4}]) for i in range(3)]
BOX = S.track("オルゴールのようなベル", "lead", patch="kfbBrightBells", volume=0.075, pan=0.2, reverb=0.3)
BELL = S.track("12回の鐘", "lead", patch="surgeFantasyBell", volume=0.11, pan=-0.1, reverb=0.45)
PLK = S.track("キラキラ（プラック）", "lead", patch="surgeNicePluck", volume=0.07, pan=0.35, reverb=0.25, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
PNL = [S.track(f"ピアノ（左手）{i + 1}", "piano", volume=0.06, pan=-0.3, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(3)]
PNR = [S.track(f"ピアノ（右手）{i + 1}", "piano", volume=0.06, pan=0.3, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(3)]
GLT = [S.track(f"左のギター{i + 1}弦め", "guitar", amp="clean", volume=0.08, pan=-0.5, reverb=0.15, chorus=0) for i in range(6)]
GRT = [S.track(f"右のギター{i + 1}弦め", "guitar", amp="clean", volume=0.08, pan=0.5, reverb=0.2, chorus=0) for i in range(6)]
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
SL, SR = G2.Strummer(GLT, S, 12), G2.Strummer(GRT, S, 24)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 3 で 1 = A3、1' = A4、3' = C#5。最後のサビからは半音上）=================
VA = ["1:0.5 1:0.5 2:0.5 3:0.5 3:1 2:1", "3:1 2:1.5 R:1.5", "3:0.5 3:0.5 4:0.5 5:0.5 5:1 3:1", "2:1 3:1.5 R:1.5",
      "1:0.5 1:0.5 2:0.5 3:0.5 5:1 3:1", "2:1 1:1.5 R:1.5", "R:0.5 3:0.5 5:0.5 6:0.5 5:1 3:1", "2:1.5 2:0.5 3:1 R:1"]                    # A: 低めで、ひとりごと
VA2 = VA[:4] + ["5:0.5 5:0.5 6:0.5 5:0.5 3:1 5:1", "6:1 5:1.5 R:1.5", "R:0.5 5:0.5 6:0.5 1':0.5 6:1 5:1", "3:1.5 2:0.5 2:1 R:1"]            # A の後半: 少し上へ
VB = ["3:1 3:0.5 4:0.5 5:1 5:1", "6:2 R:2", "4:1 4:0.5 5:0.5 6:1 6:1", "1':2 R:2", "5:1 5:0.5 6:0.5 1':1 1':1", "2':2 R:2", "1':1 2':1 3':2", "R:4"]   # B: 階段を上がる
VC = ["5:0.5 5:0.5 1':1 2':1 3':1", "2':1.5 1':0.5 1':1 R:1", "6:0.5 6:0.5 1':1 2':1 1':1", "6:1.5 5:0.5 5:1 R:1",
      "4:0.5 5:0.5 6:1 1':1 2':1", "3':1.5 2':0.5 2':1 R:1", "2':1 1':1 6:1 1':1", "1':3 R:1"]                                             # サビ前半: 大きく跳ねて、高い所でのばす
VC2 = VC[:2] + ["6:0.5 6:0.5 1':1 2':1 3':1", "4':1.5 3':0.5 3':1 R:1", "4:0.5 5:0.5 6:1 1':1 3':1", "2':1.5 1':0.5 1':1 R:1", "6:1 7:1 1':1 2':1", "1':3 R:1"]   # サビ後半
VM = ["1:1.5 2:0.5 3:1.5 2:0.5", "1:2.5 R:1.5", "3:1.5 2:0.5 3:1.5 1:0.5", "2:2.5 R:1.5", "1:1.5 3:0.5 5:1.5 3:0.5", "2:2.5 R:1.5", "3:1.5 2:0.5 2:1.5 1:0.5", "3:2.5 R:1.5",
      "3:1.5 5:0.5 6:1.5 5:0.5", "3:2.5 R:1.5", "5:1.5 6:0.5 1':1.5 6:0.5", "5:2.5 R:1.5", "6:1.5 1':0.5 2':1.5 1':0.5", "3':2.5 R:1.5", "2':1 2':1 3':2", "R:4"]    # Cメロ: ゆっくり。後半で上がる
C1 = "かねがなるまえに/いちばんまぶしく/わたしをみつけて/おどらせて/まほうがとけても/うたはきえないよ/はだしでもいいの/はしりだす"
C2 = "はりがかさなれば/ひかりはかえすの/それでもいまだけ/うたわせて/まほうがとけても/こえはわたしだよ/かざりをおとして/わらえたの"
C3 = "かねがなりおえて/あさがくるまえに/わたしがわたしを/むかえるの/まほうがとけても/うたはきえないよ/はだしでもいいの/はしりだす"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=3) for b, x in zip(bars, lines)]
    segs = text.split("/")
    for k, sg in enumerate(segs):                                         # 2小節ごとに、音の数と文字の数が合っているか確かめる
        nn = sum(1 for x in " ".join(lines[k * 2:k * 2 + 2]).split() if not x.startswith("R"))
        assert nn == mora(sg), (name, k, sg, nn, mora(sg))
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("出だし", VC, "/".join(C1.split("/")[:4]))
put("1番A", VA + VA2, "うしろのれつから/せなかをみていた/ふりつけはぜんぶ/おぼえているのに/こんやはかわりに/まんなかにたつの/なまえもしらない/ひとたちのまえで")
put("1番B", VB, "ぬいなおした/かりたどれす/そでをとおす/いくよ")
put("サビ1", VC + VC2, C1)
put("2番A", VA + VA2, "まんなかはひろい/らいとがあついよ/きゃくせきのおくで/だれかがてをふる/まちがえたところ/えがおでごまかす/それでもこのばしょ/てばなしたくない")
put("2番B", VB, "とけいのはり/すすんでいく/あとなんきょく/まだよ")
put("Cメロ", VM, "かねのおと/かぞえてる/じゅうにまで/あとすこし/ぬげていく/きらきらが/それでもね/うたう")
put("サビ2", VC + VC2, C2)
put("落ちサビ", VC, "かえしたどれすに/ありがとうをいう/かたほうだけない/かみかざり")
put("最後のサビ", VC + VC2, C3)
put("最後のサビ2", VC2, "/".join(C1.split("/")[4:]))
put("おわり", ["5:1 6:1 2':1 1':1", "R:4"], "おはよう", bars=S.sc("おわり")[4:6])


# ================= 伴奏 =================
def rlow(b, lo="E1"): return low(S.chords[b], lo)


def seq(b, pat):
    """ベースを16分のマスで。r＝根音、R＝1オクターブ上、5＝5度、3＝3度（長短は和音に合わせる）、.＝休み、-＝のばす"""
    r = rlow(b); third = 3 if "m" in S.chords[b].replace("maj", "") else 4; out = []; i = 0
    while i < 16:
        c = pat[i]; L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if c == "." else f"{N(r + {'r': 0, 'R': 12, '5': 7, '3': third}[c])}:{L * 0.25:g}"); i += L
    RB.bar(b, " ".join(out))


def stab(b, pat, center=67):
    v = sorted(voice(S.chords[b], center, 3))
    for j in range(3): STAB[j].bar(b, steps(pat, [N(v[j])] * pat.count("x"), short=0.5))


def pad(b, lift=0, pat=None):
    v = sorted(voice(S.chords[b], 62 + lift, 3))
    for j in range(3): PAD[j].bar(b, pat.replace("N", N(v[j])) if pat else f"{N(v[j])}:4")


def piano(b, patL=None, patR=None):
    lo = sorted(voice(S.chords[b], 57, 3)); hi = sorted(voice(S.chords[b], 71, 3))
    for j in range(3):
        if patL: PNL[j].bar(b, steps(patL, [N(lo[j])] * patL.count("x"), short=0.5))
        if patR: PNR[j].bar(b, steps(patR, [N(hi[j])] * patR.count("x"), short=0.5))


def box(b, k=0):
    """オルゴールのような分散和音（8分）"""
    v = sorted(voice(S.chords[b], 76, 3)); o = ([0, 1, 2, 1, 0, 2, 1, 2], [2, 1, 0, 1, 2, 0, 1, 0])[k]
    BOX.bar(b, " ".join(f"{N(v[x])}:0.5" for x in o))


def chime(b, beat=0, hi=False):
    """鐘をひとつ。その調の5度（イ長調ならミ）"""
    m = midi("E5") + (1 if b >= MOD else 0) + (5 if hi else 0); BELL.at(S.bar_beat(b) + beat, f"{N(m)}:3.5")


def clap(b, pat="R:1 B4:1 R:1 B4:1"): CLP.bar(b, pat)
def spark(b, k=0): PLK.bar(b, KEY(b).mel(("R:2.5 1':0.5 2':0.5 3':0.5", "R:3 5':0.5 3':0.5", "1':0.5 2':0.5 3':0.5 5':0.5 R:2")[k], oct=4))
def gtr(b, patL=None, patR=None):
    sh = G2.low_shape(S.chords[b])
    if patL: SL.bar(b, patL, sh, feel=8)
    if patR: SR.bar(b, patR, sh, feel=8)


K4 = "X...X...X...X..."
SLOW = [("X.........X.....", "........X.......", "x...x...x...x..."), ("X.....X...X.....", "........X.....x.", "x...x...x...x.x.")]      # A: 細かくきざまない
HOP = [("X..x....X.x.....", "....X.......X...", "x.x.x.x.x.x.x.x."), ("X..x..x...X.....", "....X.......X..x", "x.x.x.x.x.x.x.xx")]      # 2番A: はねる
FOUR = [(K4, "....X.......X...", "..x...x...x...x."), (K4, "....X.......X..x", "..x...x...x..xx.")]                                # サビ1: 4つ打ちと裏のハイハット
FOUR8 = [(K4, "....X.......X...", "x.x.x.x.x.x.x.x."), (K4, "....X.......X.xx", "x.x.x.x.x.x.x.xx")]                               # サビ2・最後: 8分のハイハット
G1, G2P = "D---d-U---U-d-U-", "D-----U-d-U---U-"


def chorus(b, i, size):
    """サビ。size 1＝幕が開く、2＝鐘の中で全員、3＝半音上げていちばん大きい"""
    g = (FOUR if size == 1 else FOUR8)[i % 2]; D.set(b, g[0], g[1] if i % 8 != 7 else "....X.......X.XX", g[2]); clap(b)
    if i % 8 == 0: crash(D, b, "C2", 4)
    seq(b, "r-.r-.R-r-.r-.5-" if i % 2 == 0 else "r-.r-.R-r-R-5-3-"); SUB.bar(b, f"{N(rlow(b))}:4")
    piano(b, "x.....x...x.....", "....x.......x..."); gtr(b, G1 if i % 2 == 0 else G2P, G2P if i % 2 == 0 else G1)   # v2: 歌の後ろをすっきりさせる（右手は2・4拍だけ、ギターは小さめ）
    if i % 4 == 3: spark(b, (i // 4) % 2)
    if size >= 2 and i % 2 == 1: stab(b, "x.....x...x.....")            # v2: 歌の切れ目の小節だけ
    if size == 2 and i % 2 == 0: chime(b, 0)                              # 鐘が鳴りつづける
    if size == 3:
        pad(b)
        if i % 4 == 0: chime(b, 0, hi=True)                               # 始まりの合図


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "出だし":                                                    # 声とオルゴール。低いパッドとのばすベースで、小さくなりすぎないようにする
        box(b, i % 2); pad(b, -5); SUB.bar(b, f"{N(rlow(b))}:4"); piano(b, patL="x...............")
        if last: D.set(b, "................", "........x.x.xxxx", "................")
    elif n == "前奏":                                                    # ドラムが入り、ギターをかき鳴らす
        g = FOUR8[i % 2]; D.set(b, g[0], g[1] if not last else "....X...X.X.XXXX", g[2]); clap(b)
        if i == 0: crash(D, b, "C2", 4)
        seq(b, "r-.r-.R-r-.r-.5-" if not odd else "r-.r-.R-r-R-5-3-"); SUB.bar(b, f"{N(rlow(b))}:4"); gtr(b, G1, G2P); box(b, i % 2); piano(b, "x.....x...x.....")
        if odd: spark(b, 2 if i == 7 else 0)
    elif n == "1番A":                                                    # ピアノとベース。ドラムは細かくきざまない
        g = SLOW[i % 2]; D.set(b, g[0], g[1] if not last else "........X...x.xx", g[2])
        seq(b, "r-----..r---5---" if not odd else "r-------3---5---")      # v3: 短く弾き直す音をやめた（パチッという音が出ていた）; SUB.bar(b, f"{N(rlow(b))}:2.5 R:1.5")
        piano(b, "x.......x.......", "..x..x....x....." if not odd else "..x.....x..x....")
        if i >= 8: gtr(b, patL="D-------d-----U-"); (clap(b, "R:3 B4:1") if odd else None)
    elif n in ("1番B", "2番B"):                                          # 手びょうしが入り、1段ずつ上がる。最後の1拍は無音
        if last:
            pad(b, i * 2, pat="N:3 R:1"); D.set(b, "................", "x.x.x.xxxxxx....", "................"); gtr(b, "D-------d---....", "D-------d---...."); continue
        pad(b, i); clap(b, "R:1 B4:1 R:1 B4:1" if i >= 4 else "R:3 B4:1"); D.set(b, "X.......X......." if i < 4 else K4, "................" if i < 6 else "x...x...x.x.x.x.", "x...x...x...x..." if i < 4 else "x.x.x.x.x.x.x.x.")
        seq(b, "r-------r---5---" if i < 4 else "r-r-r-r-r-r-5-5-"); SUB.bar(b, f"{N(rlow(b))}:4"); piano(b, "x...............", "x...x...x...x..." if i >= 4 else "....x.......x...")
        if n == "2番B": gtr(b, patR="D-------d-----U-")
    elif n == "サビ1": chorus(b, i, 1)
    elif n == "つなぎ":
        g = FOUR8[i % 2]; D.set(b, g[0], g[1] if not last else "....X...X.x.xxXX", g[2]); clap(b); seq(b, "r-.r-.R-r-.r-.5-"); SUB.bar(b, f"{N(rlow(b))}:4"); gtr(b, G1, G2P); box(b, i % 2)
    elif n == "2番A":                                                    # はねるビート。ギターが前に出る
        g = HOP[i % 2]; D.set(b, g[0], g[1] if not last else g[1][:12] + "x.xx", g[2]); clap(b)
        seq(b, "r--R--r-.r-R..5-" if not odd else "r--R--r-r-.3-5-."); SUB.bar(b, f"{N(rlow(b))}:2.5 R:1.5")
        gtr(b, "D---d-U-..U-d-U-" if not odd else "D-U-....d-U-d-U-", "....d-U-d-----U-" if i >= 8 else None); piano(b, patR="..x.....x..x...." if not odd else "..x..x....x.....")
        if odd and i >= 8: spark(b, 1)
    elif n == "Cメロ":                                                   # 小さく落とす。時計の針のハイハットと、鐘を12回
        D.set(b, "X..............." if i < 8 else "X.......X.......", "................" if i < 14 else ("x...x...x...x..." if i == 14 else "x.x.x.xxxxxx...."), "x...x...x...x..." if i < 15 else "................")
        if i < 15: pad(b, -5 + (i - 8 if i >= 8 else 0)); SUB.bar(b, f"{N(rlow(b))}:4"); piano(b, "x...............", "........x...x..." if odd else None)
        if 2 <= i <= 13: chime(b, 0)                                      # 12回（3小節め〜14小節め）
        if i >= 8 and i < 15: seq(b, "r-------r-------")
    elif n == "サビ2": chorus(b, i, 2)
    elif n == "間奏":                                                    # 歌なし。ピアノの右手が旋律、キラキラが答える
        g = FOUR8[i % 2]; D.set(b, g[0], g[1] if not last else "....X...X...XXXX", g[2]); clap(b); seq(b, "r-.r-.R-r-R-5-3-" if odd else "r-R-r-R-r-R-5-R-"); SUB.bar(b, f"{N(rlow(b))}:4")
        gtr(b, G1, G2P); stab(b, "x.....x...x.....")
        PNR[0].bar(b, K1.mel(("3':1 2':0.5 1':0.5 6:1 1':1", "2':1.5 1':0.5 6:2", "5:0.5 6:0.5 1':1 2':1 3':1", "2':3 R:1", "3':1 2':0.5 1':0.5 6:1 1':1", "4':1.5 3':0.5 2':2", "2':1 3':1 4':1 5':1", "5':3 R:1")[i], oct=4))
        if odd: spark(b, 0)
    elif n == "落ちサビ":                                                # 声とピアノだけ
        piano(b, "x.......x.......", "..x.x...x.x.x..." if not odd else "..x.x.....x.x..."); SUB.bar(b, f"{N(rlow(b))}:4"); pad(b, -5)
        if i == 6: box(b, 0)
        if last: D.set(b, "................", "x...x...x.x.xxxx", "................"); gtr(b, "D-------d---....", "D-------d---....")
    elif n in ("最後のサビ", "最後のサビ2"): chorus(b, i, 3)
    elif n == "おわり":                                                  # 鐘の余韻と、ひとこと
        if i < 4:
            g = FOUR8[i % 2]; D.set(b, g[0], g[1] if i < 3 else "....X...X.X.X...", g[2]); clap(b); seq(b, "r-.r-.R-r-.r-.5-"); SUB.bar(b, f"{N(rlow(b))}:4"); gtr(b, G1, G2P); box(b, i % 2); pad(b)
            if i == 0: crash(D, b, "C2", 4)
        else:
            box(b, i % 2) if i < 6 else None; pad(b, -5); SUB.bar(b, f"{N(rlow(b))}:4")
            if i == 4: crash(D, b, "C2", 4); piano(b, "x...............", "x...............")
            if i == 6: chime(b, 0, hi=True)                               # 最後の鐘

SL.end(S.nb); SR.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのアイドルポップ（164・イ長調 → 変ロ長調）。シンデレラがコンセプト。いつも後ろの列の子が、今夜だけ代役でまん中に立つ話。"
          "声とオルゴールのようなベルでサビから始まる → 低めのAメロ → 階段を上がるBメロ → サビ → 2番は A・B のあとに Cメロ（時計の針のハイハットと、鐘を12回数える）→ サビ → "
          "間奏 → 声とピアノだけの落ちサビ → 半音上げた最後のサビ（鐘が始まりの合図になる）→ 鐘の余韻で終わる。自作")
finish(S, LY, V, 0, flat=True)                                           # 山の大きさは、場面ごとの楽器の数で決める（曲全体の山は打ち消す）

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "指弾きのベース", mid=92, down=12, up=10, seed=26); humanize(path, "オルゴールのようなベル", mid=84, down=10, up=10, seed=7)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 14, "chorus": 15, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("最後のサビ", 0, None, K2), ("最後のサビ2", 0, None, K2)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.16, "consonant": 2.2, "glide": 0.7, "legato": 0.0}})   # v4: もっとキュートに、一音一音はっきり                           # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
# 強弱: 場面ごとに全員の弾く強さを少し変える（急に小さくしない。出だしと A は、サビの −2〜−3dB くらい）
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in (("出だし", 0.9), ("1番A", 0.8), ("1番B", 0.88), ("2番A", 0.85), ("2番B", 0.9), ("Cメロ", 0.8), ("落ちサビ", 0.85)):
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    p_["barGain"] = g[:S.nb]
save(path, js)
