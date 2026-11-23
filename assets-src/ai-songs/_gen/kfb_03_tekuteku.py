# KFB 03「てくてくフラワー」Step by Step Flower（仮。はじめの名前は「てっぺんまで、あと三歩」。人間「曲名もっと可愛くしよう」）— Kawaii future bass × ダンス × ロック。4分の4・156・変ロ長調。約4分10秒。
#
# v3（2026-11-23）: v2 は静かな場面が −16.2dB で、こんどは大きすぎた（サビと同じ）→ ベースとかけ上がりを外し、和音は後半だけ。Aメロをもう少し下げてサビとの差を広げる。
# v2（2026-11-23）: 人間「曲名もっと可愛くしよう」「高嶺の花の意味を調べて。それで進めて。」
#   調べた意味: 高い峰に咲く花は、見えても取りに行けない → 見ているだけで手が届かない、あこがれの人や物。ほめ言葉。そう呼ばれる人は、近寄りがたく思われて、声をかけられにくい。
#   → 物語はそのまま合っている（みんな見上げるだけ・だれも近づかない・花の方はひとりでゆれている）。曲名を「てくてくフラワー」に。
#   v1 は 歌 7.76・BGM 7.76。静かな場面が −28.5dB で小さすぎ（サビより 12dB 下）、サビが Aメロより 1.5dB しか大きくなかった → 静かな場面に左右のギター・和音・ベースを足す。サビの和音とかけ上がりを上げる。ソロのギターを少し下げる。
# v1（2026-11-23）: 人間「次kawaiiFutureベースにダンスとロックを混ぜて。コンセプトは高嶺の花。ドラムとベース以外は音数多めで緩急をつけて。明るい曲でお願い。」
#
# 物語（高嶺の花）: みんなが遠くから見上げるだけの人。「高いなら登ればいい」と、朝のあいさつを一歩めにして、毎日一歩ずつ近づく。
#   近くで見たら、花は風の強い高い所でひとりでゆれていた。「ここまで来た人は初めて」と言われ、最後はならんで同じ景色を見る。
# まぜ方: ダンス＝4つ打ちのキックと手びょうし・シンセの16分のかけ上がり／ロック＝左右のギターの16分のかき鳴らし・リードギター・指弾きのベース／
#   フューチャーベース＝頭で開く広い和音・歌なしのドロップ・全員が止まる休符。
# 人間の指定: ドラムとベースは音数を少なく（ドラムは4つ打ち中心、ベースは1小節 2〜4 音）。ほかは音数を多く、緩急をつける。明るい曲。
# コード進行（「登る」を和音で表す）:
#   Aメロ: I → Iaug → I6 → I7（中の音が半音ずつ上がる）→ IVmaj7 → #IVdim7 → I/V → V7sus4（ベースも半音ずつ上がる）
#   Bメロ: IIm7 → IIIm7 → IVmaj7 → V → VIm7 → ♭VIImaj7 → I → V7sus4（ベースが7段つづけて上がる）
#   サビ: IV → V/IV → IIIm7 → VI7 → IIm7 → #IIdim7 → IIIm7 → VI7 / IIm7 → III7 → VIm7 → I7 → IVmaj7 → #IVdim7 → V7sus4 → V
# 物語の出来事 → その時の音:
#   前奏（ふもとから見上げる）   → ギターの細かい音だけ → ドラムが入る
#   Aメロ（見ているだけの人たち）→ 前半はギターとキックだけ、後半でシンセのかけ上がり
#   Bメロ（一歩め、二歩め）      → ベースが1段ずつ上がる。最後の1拍は無音
#   サビ（高いなら登ろう）       → 全員。細かい音がびっしり。まん中で2拍止まる
#   ドロップ（登っていく）       → 歌なし。リードギターとシンセがかけ合う
#   2番（高い所は風が強い）      → ギター1本から
#   ギターソロ → 静かな場面（ここまで来た人は初めて）→ クリーンのギターと歌だけ
#   最後のサビ・ドロップ（ならんで同じ景色）→ 全員
# この曲だけの物: 半音ずつ登っていく和音と、7段つづけて上がるベース。
# 歌詞: 曲名の言葉（てくてく・フラワー）は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *
import gtr2_lib as G2

S = Song("29", "tekuteku", "てくてくフラワー（仮）", "Step by Step Flower", 156, 4, "Bb", "major", "カワイイ・フューチャーベース×ダンス×ロック（ボカロ）")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud " + S.flags + " --space room --space-wet 0.08"
K1 = Key("Bb", "major")

VCH = ["Bb", "Bbaug", "Bb6", "Bb7", "Ebmaj7", "Edim7", "Bb/F", "F7sus4"]
PCH = ["Cm7", "Dm7", "Ebmaj7", "F", "Gm7", "Abmaj7", "Bb", "F7sus4"]
CCH = ["Eb", "F/Eb", "Dm7", "G7", "Cm7", "C#dim7", "Dm7", "G7", "Cm7", "D7", "Gm7", "Bb7", "Ebmaj7", "Edim7", "F7sus4", "F"]
S.scene("前奏", 8, "intro", VCH)
S.scene("1番A", 16, "verse", VCH * 2)
S.scene("1番B", 8, "pre", PCH)
S.scene("サビ1", 16, "chorus", CCH)
S.scene("ドロップ1", 8, "break", VCH)
S.scene("2番A", 16, "verse", VCH * 2)
S.scene("2番B", 8, "pre", PCH)
S.scene("サビ2", 16, "chorus", CCH)
S.scene("ドロップ2", 8, "break", VCH)
S.scene("ギターソロ", 8, "break", PCH)
S.scene("静かな場面", 8, "bridge", ["Ebmaj7", "F/Eb", "Dm7", "Gm7", "Cm7", "Dm7", "Ebmaj7", "F7sus4"])
S.scene("最後のサビ", 16, "chorus", CCH)
S.scene("最後のドロップ", 16, "break", VCH * 2)
S.scene("おわり", 8, "outro", ["Ebmaj7", "Edim7", "Bb/F", "Bb", "Ebmaj7", "Edim7", "Bb/F", "Bb"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BASS = S.track("指弾きのベース", "bass", **rock_bass_spec(0.15))
CLEAN = dict(di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12, chorus=0, humanPitch=0, noScoop=True, powerChord=False, sustain=1.3, release=0.5)
GFX = [{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7}, {"type": "eq", "low": -1, "mid": 1.5, "midHz": 1800, "high": 0}, {"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}, {"type": "room", "mix": 0.1}]
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", volume=0.06, pan=-0.6, fx=GFX, **CLEAN) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", volume=0.06, pan=0.6, fx=GFX, **CLEAN) for i in range(6)]
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.095, 0.1))
SL, SR = G2.Strummer(GL, S, 29), G2.Strummer(GR, S, 47)
PF = {"type": "pluckfilter", "freq": 2000, "depth": 0.6, "rate": 30, "hold": 4}
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.066, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
ARP = S.track("シンセのかけ上がり（矩形波のプラック）", "lead", patch="kfbSquarePluck", volume=0.07, pan=0.2, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
BELL = S.track("ベルの速い動き", "lead", patch="kfbMusicBox", volume=0.05, pan=-0.3, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)


# ================= 歌（度数:長さ。oct 3 で 1 = Bb3。低い 7, = A3、高い 5' = F5）=================
def f(pat, pitches):
    it = iter(pitches.split()); return " ".join((next(it) + t[1:]) if t[0] == "x" else t for t in pat.split())


Va, Vb, Vc, Vd = "R:1 x:0.5 x:0.5 x:1 x:0.5 x:0.5", "x:1 x:0.5 x:0.5 x:1 R:1", "x:0.5 x:0.5 x:0.5 x:0.5 x:1 R:1", "R:0.5 x:0.5 x:0.5 x:0.5 x:1.5 R:0.5"
VA = [f(Va, "1 2 3 3 2"), f(Vb, "3 3 2 1"), f(Vc, "3 5 6 5 3"), f(Vd, "5 5 3 1"), f(Va, "3 4 5 5 6"), f(Vb, "6 1' 1' 6"), f(Vc, "5 6 1' 6 5"), f(Vd, "2 4 5 5")]
VA2 = [f(Va, "3 5 5 6 5"), f(Vb, "3 3 2 3"), f(Vc, "5 6 1' 6 5"), f(Vd, "1' 1' 5 3"), f(Va, "6 1' 2' 2' 1'"), f(Vb, "1' 1' 6 6"), f(Vc, "5 6 1' 2' 3'"), f(Vd, "2' 2' 1' 2'")]
VA3 = [f(Vc, "3 5 5 6 5"), f(Vd, "3 3 2 3"), f(Va, "5 6 1' 6 5"), f(Vb, "1' 1' 5 3"), f(Vc, "6 1' 2' 2' 1'"), f(Vd, "1' 1' 6 6"), f(Va, "5 6 1' 2' 3'"), f(Vb, "2' 2' 1' 2'")]   # 2番: 型を入れかえる
Pa, Pb, Pc = "x:1.5 x:0.5 x:1 x:1", "x:1 x:1 x:1 R:1", "x:0.5 x:0.5 x:0.5 x:0.5 x:2"
VB = [f(Pa, "4 4 5 6"), f(Pb, "5 5 3"), f(Pa, "5 5 6 1'"), f(Pb, "7 7 5"), f(Pa, "6 6 1' 2'"), f(Pb, "2' 2' 1'"), f(Pc, "1' 2' 3' 2' 3'"), "R:4"]
Ka, Kb, Kc, Kd, Ke = "x:1 x:0.5 x:0.5 x:0.5 x:1 x:0.5", "x:1.5 x:0.5 x:1 R:1", "R:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5", "x:2 x:1 R:1", "x:3 R:1"
VC = [f(Ka, "1' 2' 3' 3' 2' 1'"), f(Kb, "2' 7 2'"), f(Kc, "5 6 7 2' 7 6 5"), f(Kd, "6 7"), f(Ka, "2' 2' 3' 4' 3' 2'"), f(Kb, "1' 6 1'"), f(Kc, "6 7 2' 3' 2' 7 2'"), f(Ke, "3'"),
      f(Ka, "4' 3' 2' 2' 3' 4'"), f(Kb, "3' 2' 3'"), f(Kc, "1' 2' 3' 4' 3' 2' 1'"), f(Kd, "5' 3'"), f(Ka, "2' 3' 4' 4' 3' 2'"), f(Kb, "1' 6 1'"), f(Kc, "1' 2' 2' 4' 2' 1' 2'"), f(Ke, "2'")]
Qa, Qb, Qc, Qd = "x:1 x:1 x:0.5 x:0.5 x:1", "x:2 R:2", "x:1 x:1 x:1 x:1", "x:3 R:1"
VQ = [f(Qa, "3 4 5 5 6"), f(Qb, "5"), f(Qa, "5 6 7 7 2'"), f(Qb, "1'"), f(Qa, "4 5 6 6 1'"), f(Qb, "7"), f(Qc, "6 1' 2' 3'"), f(Qd, "2'")]
CB = "ひとあしずつでいい/くもをぬけるまでは/みあげてたそのめで/となりをみたいの"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else K1.mel(x, oct=3) for x in lines]
    for k, sg in enumerate(text.split("/")):
        nn = sum(1 for x in " ".join(lines[k * 2:k * 2 + 2]).split() if not x.startswith("R"))
        assert nn == mora(sg), (name, k, sg, nn, mora(sg))
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("1番A", VA + VA2, "みんなみあげるはな/とおくてきれいだね/うわさだけがとどく/だれもちかづかない/ながめてるだけなら/ふもとのままだから/くつひもをむすんで/きょうからのぼるんだ")
put("1番B", VB, "あさのあいさつ/それがひとあし/なまえをいえた/ふたあしめ")
put("サビ1", VC, "たかいならのぼろう/いきがきれてもいい/とどかないときめた/ひとはだれですか/" + CB)
VA4 = [f(Vc, "1 2 3 3 2"), f(Vd, "3 3 2 1"), f(Va, "3 5 6 5 3"), f(Vb, "5 5 3 1"), f(Vc, "3 4 5 5 6"), f(Vd, "6 1' 1' 6"), f(Va, "5 6 1' 6 5"), f(Vb, "2 4 5 5")]
put("2番A", VA4 + VA3, "ちかづいてわかるの/かぜがつよいところ/たかいところのはな/ひとりでゆれていた/こえをかけたそのひ/おどろいたかおした/だれもこないからと/わらうのがへたなの")
put("2番B", VB, "ならんでかえる/それがみあしめ/わらいごえきく/よあしめだ")
put("サビ2", VC, "たかいならのぼろう/いきがきれてもいい/さむいならいくから/うごかないでいて/" + CB)
put("静かな場面", VQ, "ここまできた/ひとはきみが/はじめてだと/いうんだよ")
put("最後のサビ", VC, "たかいからみえるの/まちもくももぜんぶ/ふたりぶんのかげが/ならんでのびるよ/ひとあしずつでいい/くもをぬけたさきで/みあげてたそのめで/となりをみている")
put("おわり", [f("x:0.5 x:0.5 x:1 x:2", "5 1' 2' 1'"), "R:4"], "ついたよ", bars=S.sc("おわり")[6:8])


# ================= 伴奏 =================
def bass(b, pat="r-------r-------"):
    """ベースは音数を少なく（1小節 2〜4 音）。r＝根音、5＝5度、R＝1オクターブ上、-＝のばす、.＝休み"""
    r = low(S.chords[b], "E1"); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + {'r': 0, '5': 7, 'R': 12}[pat[i]])}:{L * 0.25:g}"); i += L
    BASS.bar(b, " ".join(out))


def saw(b, pat="x-------x-------", center=65):
    v = sorted(voice(S.chords[b], center, 5))
    for j in range(5):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(v[j])}:{L * 0.25:g}"); i += L
        SAW[j].bar(b, " ".join(out))


def arp(b, k=0):
    """シンセの16分のかけ上がり（和音の音を上がって下がる）。k で形を変える。小節の終わりに休みを入れる形もある"""
    t = sorted(voice(S.chords[b], 74, 4)); u = t + [t[0] + 12, t[1] + 12]
    o = ([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3], [4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5], [0, 2, 1, 3, 2, 4, 3, 5, 4, 3, 2, 1, -1, -1, -1, -1], [0, 1, 2, 3, -1, -1, 2, 3, 4, 5, -1, -1, 4, 3, 2, 1])[k % 4]
    ARP.bar(b, " ".join("R:0.25" if x < 0 else f"{N(u[x])}:0.25" for x in o))


def bell(b, k=0):
    """ベルの速い動き: 歌の切れ目（小節の後半）に、音階をかけ下りる・かけ上がる"""
    BELL.bar(b, K1.mel(("R:2 5':0.25 3':0.25 2':0.25 1':0.25 6:0.25 5:0.25 3:0.5", "R:2.5 3:0.25 5:0.25 6:0.25 1':0.25 2':0.25 3':0.25", "R:2 3':0.25 5':0.25 3':0.25 2':0.25 1':0.5 R:0.5", "R:3 1':0.25 2':0.25 3':0.25 5':0.25")[k % 4], oct=4))


def gtr(b, patL=None, patR=None, sung=None):
    """左右のギター: 16分で振る。左は低い側の形、右はまん中の弦の三和音（高さがちがうので厚くなる）。歌が鳴っているマスは、間を作る"""
    c = S.chords[b]
    if patL: SL.bar(b, G2.with_space(patL, sung, keep=(0, 8)) if sung else patL, G2.low_shape(c), feel=16)
    if patR: TR[0] = G2.triad(c, TR[0]); SR.bar(b, G2.with_space(patR, sung, keep=(0, 8)) if sung else patR, TR[0], feel=16)


TR = [None]
GA = ("D.dUd.dUD.dUdUd.", "D.dUdUd.D.dUd.dU", "D.xUd.dUD.dUdUx.", "DUdUd.dUD.xUdUdU")          # 16分のかき鳴らし（音数多め）
GB = ("d.dUd.dUd.dUd.dU", "dUd.dUdUd.dUd.d.", "d.dUdUd.dUd.dUdU", "dUdUd.dUd.dUdUd.")
LD = ("3':0.5 5':0.25 3':0.25 2':0.5 1':0.25 2':0.25 3':0.5 R:0.5 1':0.25 2':0.25 3':0.25 5':0.25", "3':0.25 3':0.25 R:0.5 1':0.25 2':0.25 3':0.5 2':0.25 1':0.25 6:0.5 1':1",
      "5':0.5 3':0.25 5':0.25 6':0.5 5':0.25 3':0.25 5':0.5 R:0.5 3':0.25 2':0.25 1':0.5", "1':0.25 2':0.25 3':0.25 5':0.25 3':0.5 R:0.5 1':0.25 6:0.25 1':0.5 R:1")      # リードギター（ドロップ。Bb・Bb6・Ebmaj7・Bb/F の小節）
SOLO = ("2':1 4':0.5 2':0.25 4':0.25 5':1 4':0.5 2':0.5", "3':0.5 5':0.5 3':0.25 2':0.25 1':0.5 7:0.5 2':0.5 3':1", "4':0.25 5':0.25 6':0.5 5':0.5 4':0.5 2':0.5 4':0.5 5':1", "5':1.5 4':0.25 5':0.25 6':1 5':1",
        "6':0.5 5':0.25 4':0.25 2':0.5 4':0.5 5':0.5 6':0.5 1'':1", "1'':0.5 5':0.5 4':0.25 5':0.25 4':0.5 2':0.5 1':0.5 2':1", "3':0.25 5':0.25 3':0.25 5':0.25 1'':0.5 5':0.5 3':0.5 5':0.5 1'':1", "2'':3 R:1")   # ギターソロ（1段ずつ上がる和音の上で）
FOUR = ("X...X...X...X...", "....X.......X...", "x.x.x.x.x.x.x.x.")                                   # ドラムは音数を少なく: 4つ打ちとスネア2・4拍、8分のハイハット
HALFT = ("X.......X.......", "........X.......", "x...x...x...x...")

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; sung = G2.sung_slots(V, S, b)
    if n == "前奏":                                                      # ギターの細かい音だけ → 5小節めからドラム
        gtr(b, GA[i % 4], GB[i % 4] if i >= 2 else None)
        if i >= 4: D.set(b, FOUR[0], "................" if i < 6 else FOUR[1], FOUR[2] if i >= 6 else "................"); bass(b, "r---------------"); arp(b, i)
        if last: D.set(b, "X...X...X...X...", "....X...X.X.XXXX", "x.x.x.x.x.x.x.x.")
        if i == 4: crash(D, b, "C2", 4)
    elif n in ("1番A", "2番A"):                                          # 前半はギターとキックだけ。後半でシンセのかけ上がり
        first = i < 8 and n == "1番A"; solo1 = n == "2番A" and i < 4      # 2番の頭4小節は、ギター1本だけ（緩急）
        if solo1: gtr(b, G2.with_space(GA[i % 4], sung, keep=(0, 8))); D.set(b, "X...............", "................", "................")
        else:
            gtr(b, GA[i % 4], GB[i % 4] if not first or i >= 4 else None, sung=sung)
            g = HALFT if first else FOUR; D.set(b, g[0], g[1] if not last else "....X.......X.XX", g[2]); bass(b, ("r-----r---------", "r---------r-----", "r--r------------", "r-------..r---5-")[i % 4])
        if not first and not solo1 and odd: arp(b, 2 + i // 2)
        if i % 4 == 3 and not solo1: bell(b, i // 4)
        if not first and not solo1: clap(b) if False else CLP.bar(b, "R:1 B4:1 R:1 B4:1")
    elif n in ("1番B", "2番B"):                                          # ベースが1段ずつ上がる。最後の1拍は無音
        if last:
            FX.bar(b, "C5:3 R:1"); gtr(b, "D...D...D.D.....", "D...D...D.D....."); saw(b, "x---x---x-x-...."); bass(b, "r---r---r-r-...."); D.set(b, "X...X...X.X.....", "....X...X.X.....", "................"); continue
        gtr(b, "D.......d.dUd.dU" if i < 4 else GA[i % 4], GB[i % 4] if i >= 4 else None, sung=sung); saw(b, "x---------------" if i < 4 else "x-------x-------", 62 + i)
        D.set(b, HALFT[0] if i < 4 else FOUR[0], HALFT[1] if i < 4 else ("....X.......X..." if i < 6 else "....X...X.X.X.XX"), HALFT[2] if i < 4 else FOUR[2]); bass(b, "r---------------" if i < 4 else "r-----r---------")
        if i >= 4: arp(b, i)
        if i == 6: FX.bar(b, "C5:4")
    elif n in ("サビ1", "サビ2", "最後のサビ"):                          # 全員。細かい音がびっしり。まん中（8小節め）の後半は全員が止まる
        if i == 7:
            D.set(b, "X...X...........", "....X...........", "x.x.x.x........."); saw(b, "x-----.........."); bass(b, "r-----.........."); gtr(b, "D.dUd.d.........", "d.dUd.d........."); bell(b, 1); continue
        if last:
            D.set(b, "X...X...X.......", "....X...X.X.....", "x.x.x.x.x.x....."); saw(b, "x---x---x-x-...."); bass(b, "r---r---r-r-...."); gtr(b, "D...D...D.D.....", "D...D...D.D....."); FX.bar(b, "C5:3 R:1"); continue
        D.set(b, FOUR[0], FOUR[1] if i % 8 != 6 else "....X.......X.X.", FOUR[2]); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 8 == 0: crash(D, b, "C2", 4)
        bass(b, ("r-----r---r-----", "r---r-----r---R-", "r-----r-----r---", "r---r---..r-r---")[i % 4]); saw(b, ("x-------x---x-..", "x---x-..x-------", "x-------x---x-..", "x---x---x-x-....")[i % 4])
        gtr(b, GA[i % 4], GB[(i + 1) % 4], sung=sung); arp(b, i)
        if i % 4 == 3: bell(b, i // 4 + 2)
    elif n in ("ドロップ1", "ドロップ2", "最後のドロップ"):              # 歌なし。リードギターとシンセがかけ合う。4小節ごとに止まる
        k8 = i % 8
        if k8 == 3:
            D.set(b, "X...X...........", "....X...........", "x.x.x.x........."); saw(b, "x--x--x........."); bass(b, "r-----.........."); gtr(b, "D.dUd.d.........", "d.dUd.d........."); arp(b, 3); continue
        if k8 == 7:
            D.set(b, "X.X.X.X.XXXX....", "....X...X.X.....", "x.x.x.x.xxxx...."); saw(b, "x-x-x-x-xxxx...."); bass(b, "r-r-r-r-rr......"); gtr(b, "D.D.D.D.DUDU....", "D.D.D.D.DUDU...."); continue
        D.set(b, FOUR[0], FOUR[1], FOUR[2]); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if k8 == 0: crash(D, b, "C2", 4)
        bass(b, ("r--r--r---------", "r-----r---r-----", "r--r------r-----", "r-----r-----R---")[i % 4]); saw(b, ("x--x--x-..x--x..", "x-----..x--.x-..", "x--x--x-....x-x-", "x-----..x-x-....")[i % 4]); gtr(b, GA[(i + 2) % 4], GB[i % 4])
        if k8 in (0, 2, 4, 6): LEAD.bar(b, K1.mel(LD[k8 // 2], oct=3))
        else: arp(b, k8)
    elif n == "ギターソロ":                                              # リードギターが歌う。下は1段ずつ上がる和音
        D.set(b, FOUR[0], FOUR[1] if not last else "....X...X.X.XXXX", FOUR[2]); bass(b, "r-----r---------" if i < 4 else "r-----r---r-----"); saw(b, "x-------x-------", 62 + i)
        gtr(b, GA[i % 4], GB[i % 4]); LEAD.bar(b, K1.mel(SOLO[i], oct=3))
        if i == 0: crash(D, b, "C2", 4)
    elif n == "静かな場面":                                              # クリーンのギターと歌だけ
        gtr(b, "D...d.dUd...d.dU" if not odd else "D.dUd...d.dUd...", "d.dUd...d.dUd.dU" if not odd else "d...d.dUd.dUd...", sung=sung); saw(b, "x---------------", 60); bass(b, "r---------------")      # v4: 和音とのばすベースを入れる（v3 は −29dB で小さすぎ、v2 は −16dB で大きすぎた）
        if i == 7: FX.bar(b, "C5:4"); D.set(b, "................", "........x.x.xxxx", "................")
    elif n == "おわり":                                                  # 半音ずつ登って、いちばん上の和音で終わる
        gtr(b, "D.dUd.dUD.dUdUd." if i < 7 else "D...............", "d.dUd.dUd.dUd.dU" if i < 7 and i >= 4 else ("D..............." if i == 7 else None)); saw(b, "x---------------"); bass(b, "r---------------")
        if i < 6: arp(b, i)
        if i < 4: D.set(b, FOUR[0], FOUR[1], FOUR[2])
        if i in (0, 4): crash(D, b, "C2", 4)
        if i == 7: crash(D, b, "C2", 4); D.set(b, "X...............", "................", "................")

SL.end(S.nb); SR.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース×ダンス×ロック（156・変ロ長調）。高嶺の花（見えていても手が届かない、あこがれの人）がコンセプト。みんなが見上げるだけの人に、一歩ずつ登っていく話。"
          "ドラムとベースは音数を少なく、左右のギターの16分・シンセのかけ上がり・ベル・リードギターは音数を多く。半音ずつ登る和音と、7段つづけて上がるベース。"
          "ギターだけの前奏 → Aメロ → Bメロ → サビ → 歌なしのドロップ → 短い2番 → サビ → ドロップ → ギターソロ → 静かな場面 → 最後のサビ → ドロップ → ひとこと。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "シンセのかけ上がり（矩形波のプラック）", mid=90, down=12, up=10, seed=29); humanize(path, "リードギター", mid=98, down=10, up=12, seed=3)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 15, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("最後のサビ", 0, None, K1)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in (("1番A", 0.8), ("2番A", 0.8)):
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    p_["barGain"] = g[:S.nb]
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
