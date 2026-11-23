# KFB 03A「窓ぎわシャンデリア」Window-seat Chandelier（仮）— Kawaii future bass × ダンス × ロック。4分の4・164・イ長調 → 変ロ長調 → ロ長調。約5分04秒。
#
# 2026-11-23 人間: 「てくてくフラワー」v4 に「明るい曲ってより日常感」「展開が少ない」「前奏の音の途切れ方が不自然で使い物にならない → 最初から作り直し」
#   「ドラムはハイハット主体の16ビートも」「フィルも」「FXも入れて」「高嶺の花って感じの恋愛曲に」「曲名がダサい」「ストーリーも作り直して。5分ぐらいの曲に」「登山的なイメージがついていやだ」
#   → 物語を3つ出したところ「3つ全部作って欲しい」。これは A（窓ぎわの人）。前の曲（kfb_03_tekuteku.py）の旋律・和音・伴奏は使っていない。
# 物語（高嶺の花＝見えていても手が届かない、あこがれの人）: 教室でいちばん遠い席の、みんながあこがれる人。見ているだけの恋だった。落とした消しゴムを拾ってもらった日から、
#   あいさつ → 名前を呼ぶ → 雨の帰り道、と少しずつ近づく。近くで知ったのは、完ぺきに見えるその人が、だれにも誘われずひとりで帰ること。「話しかけてくれた人は初めて」。
#   遠い人だと決めていたのは自分のほうだった、と気づいて「好きです」を言う。最後は「おはよう」をあしたも言わせてね。
# 音: サビのたびに調が半音上がる（気持ちが高まる）。前奏はのばす和音とシンセの旋律がつながって鳴る。ドラムは4つ打ちとハイハット主体の16ビート、形のちがうフィル4種。
#   効果音（当たる音・逆回しのシンバル・きらめき・上がっていく音・ふくらむ和音・ハイハットのロール）。和音を小節の途中で止める形は使わない。
# 歌詞: 曲名の言葉（窓ぎわ・シャンデリア）は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *
import gtr2_lib as G2

S = Song("29", "madogiwa", "窓ぎわシャンデリア（仮）", "Window-seat Chandelier", 164, 4, "A", "major", "カワイイ・フューチャーベース×ダンス×ロック（ボカロ）")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud " + S.flags + " --space room --space-wet 0.08"
KS = (Key("A", "major"), Key("Bb", "major"), Key("B", "major"))      # 和音の表は変ロ長調で書き、全体を半音下げて使う（歌のいちばん高い音を E5 までにするため）





VCH = ["Bb", "Bb/D", "Eb", "F", "Gm7", "Ab", "Eb", "F7sus4"]                       # ベースが I → III → IV → V → VI → ♭VII と登る
PCH = ["Cm7", "Dm7", "Ebmaj7", "F", "Gm7", "Abmaj7", "Bb", "F7sus4"]               # ベースが7段つづけて上がる
CCH = ["Eb", "F", "Dm7", "Gm7", "Eb", "F", "Gm7", "Ab", "Eb", "F", "Dm7", "G7", "Cm7", "Dm7", "Eb", "F"]
SHIFT = {}


def scene(name, n, kind, chs, sh=0, lastch=None):
    b0 = S.nb if hasattr(S, "nb") and S.nb else sum(x for x in getattr(S, "_n", [])); S._n = getattr(S, "_n", []) + [n]
    c = [tr_chord(x, sh - 1) for x in chs]
    if lastch: c[-1] = lastch
    for k in range(n): SHIFT[sum(S._n[:-1]) + k] = sh
    S.scene(name, n, kind, c)


QCH = ["Ebmaj7", "F/Eb", "Dm7", "Gm7", "Cm7", "Dm7", "Ebmaj7", "F7sus4", "Ebmaj7", "F/Eb", "Dm7", "G7", "Cm7", "Dm7", "Ebmaj7", "F7sus4"]
scene("前奏", 8, "intro", VCH)
scene("1番A", 16, "verse", VCH * 2)
scene("1番B", 8, "pre", PCH)
scene("サビ1", 16, "chorus", CCH)
scene("ドロップ1", 8, "break", VCH)
scene("2番A", 16, "verse", VCH * 2)
scene("2番B", 8, "pre", PCH, 0, "F7sus4")                                         # 最後の和音が、半音上の調の V
scene("サビ2", 16, "chorus", CCH, 1)
scene("ドロップ2", 16, "break", VCH * 2, 1)
scene("ギターソロ", 8, "break", PCH, 1)
scene("静かな場面", 16, "bridge", QCH, 1)
scene("落ちサビ", 8, "bridge", CCH[:8], 1)                                        # 和音と歌だけ
scene("立ち上げ", 8, "pre", PCH, 2)
scene("最後のサビ", 16, "chorus", CCH, 2)
scene("大サビ", 16, "chorus", CCH, 2)
scene("最後のドロップ", 16, "break", VCH * 2, 2)
scene("おわり", 8, "outro", ["Eb", "F", "Gm7", "Ab", "Eb", "F", "Bb", "Bb"], 2)
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3


def KEY(b): return KS[SHIFT.get(b, 0)]


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
HOOK = S.track("フックのシンセ", "lead", patch="kfbTranceLead", volume=0.06, mono=True, pan=-0.1, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])
BELL = S.track("ベルの速い動き", "lead", patch="kfbMusicBox", volume=0.05, pan=-0.3, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
FXT = S.track("効果音（当たる音・逆回しのシンバル・きらめき）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
SWELL = [S.track(f"ふくらむ和音{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
FXH = {}


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))


def swell(b):
    v = sorted(voice(S.chords[b], 67, 3))
    for j in range(3): SWELL[j].bar(b, f"{N(v[j])}:4")


D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)


# ================= 歌（度数:長さ。oct 3 で 1 = その調の主音（イ長調なら A3）。サビのいちばん高い音は 4'）=================
def f(pat, pitches):
    it = iter(pitches.split()); return " ".join((next(it) + t[1:]) if t[0] == "x" else t for t in pat.split())


Va, Vb, Vc, Vd = "x:0.5 x:0.5 x:0.5 x:1 x:0.5 x:1", "x:1.5 x:0.5 x:1 R:1", "R:1 x:0.5 x:0.5 x:1 x:1", "x:0.5 x:1 x:0.5 x:0.5 x:1 R:0.5"      # Aメロ: 6音＋3音、4音＋5音（食いこむリズム）
PA = ("5 5 6 5 3 5", "6 5 3", "4 4 5 6", "5 6 5 3 2", "3 3 5 6 6 1'", "2' 1' 6", "6 6 1' 2'", "2' 1' 6 5 5")
PB = ("1' 1' 2' 1' 6 1'", "3' 2' 1'", "6 6 1' 2'", "2' 3' 2' 1' 7", "1' 1' 2' 3' 3' 2'", "2' 2' 6", "6 1' 2' 3'", "3' 2' 1' 2' 2'")
VA = [f((Va, Vb, Vc, Vd)[k % 4], p) for k, p in enumerate(PA)]; VA2 = [f((Va, Vb, Vc, Vd)[k % 4], p) for k, p in enumerate(PB)]
VA4, VA3 = VA2, VA                                                               # 2番: 高い方の形から入る
Pa, Pb, Pc = "R:0.5 x:0.5 x:1 x:1 x:1", "x:1.5 x:1.5 x:1", "x:1 x:0.5 x:0.5 x:1 x:1"
VB = [f(Pa, "4 4 5 6"), f(Pb, "5 5 3"), f(Pa, "5 5 6 1'"), f(Pb, "7 7 5"), f(Pa, "6 6 1' 2'"), f(Pb, "2' 2' 1'"), f(Pc, "1' 2' 3' 2' 3'"), "R:4"]
Ka, Kb, Kc, Kd, Ke = "x:1.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5", "x:1 x:1 x:1.5 R:0.5", "x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:1", "x:1 x:2 R:1", "x:3 R:1"
VC = [f(Ka, "1' 1' 2' 3' 3' 2'"), f(Kb, "2' 3' 2'"), f(Kc, "5 7 2' 3' 2' 7 2'"), f(Kd, "3' 1'"), f(Ka, "1' 1' 2' 3' 4' 3'"), f(Kb, "2' 2' 3'"), f(Kc, "6 1' 2' 3' 2' 1' 2'"), f(Ke, "4'"),
      f(Ka, "3' 3' 2' 1' 2' 3'"), f(Kb, "2' 7 2'"), f(Kc, "7 2' 3' 2' 7 5 7"), f(Kd, "3' 7"), f(Ka, "2' 2' 3' 4' 3' 2'"), f(Kb, "3' 2' 3'"), f(Kc, "1' 2' 3' 4' 3' 2' 3'"), f(Ke, "2'")]   # サビ: 高く、句の終わりをのばす
Qa, Qb, Qc, Qd = "x:0.5 x:0.5 x:1 x:1 x:1", "x:3 R:1", "x:1 x:1 x:1 x:1", "x:3 R:1"
VQ = [f(Qa, "3 4 5 5 6"), f(Qb, "5"), f(Qa, "5 6 7 7 2'"), f(Qb, "1'"), f(Qa, "4 5 6 6 1'"), f(Qb, "7"), f(Qc, "6 1' 2' 3'"), f(Qd, "2'")]
VQ2 = [f(Qa, "5 6 1' 1' 2'"), f(Qb, "1'"), f(Qa, "6 1' 2' 2' 3'"), f(Qb, "2'"), f(Qa, "4 5 6 6 1'"), f(Qb, "2'"), f(Qc, "1' 2' 3' 2'"), f(Qd, "1'")]
OTO = "あなたはしらないの/このむねのおとを"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else KEY(b).mel(x, oct=3) for b, x in zip(bars, lines)]
    for k, sg in enumerate(text.split("/")):
        nn = sum(1 for x in " ".join(lines[k * 2:k * 2 + 2]).split() if not x.startswith("R"))
        assert nn == mora(sg), (name, k, sg, nn, mora(sg))
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("1番A", VA + VA2, "いちばんとおいせき/ひかりのなかのひと/みんながふりむいて/わたしはうつむいた/つりあわないよねと/じぶんにいいきかせ/それでもめがおうの/きらきらするほうを")
put("1番B", VB, "おちたけしゴム/ひろうゆびさき/ありがとのこえ/はじまりだ")
put("サビ1", VC, "てがとどかなくても/すきでいてもいいの/みているだけのこい/きょうでやめにする/おはようのひとこと/それだけでふるえる/" + OTO)
put("2番A", VA4 + VA3, "なまえをよんでみた/ふりむくそのかおが/おもうよりやさしい/なんどもおもいだす/かんぺきにみえても/ひとりでかえるひと/だれもさそわないと/わらうきみがすきだ")
put("2番B", VB, "かさをさしだす/あめのかえりに/かたがふれそう/とまるいき")
put("サビ2", VC, "てがとどかなくても/すきでいてもいいの/となりをあるくだけ/それでいいはずが/さよならのかどまで/ことばがでてこない/" + OTO)
put("静かな場面", VQ + VQ2, "はなしかけて/くれたひとは/はじめてだと/わらうから/とおいひとと/きめてたのは/わたしのほう/きづいたの")
put("落ちサビ", VC[:8], "てがとどかなくても/すきでいてもいいの/そうきいてたこいに/こたえをだすから")
put("最後のサビ", VC, "てをのばせばとどく/ところにきみがいた/みているだけのこい/きょうでやめにする/すきですのひとこと/こえがふるえたけど/あなたがわらうから/なみだがでました")
put("大サビ", VC, "てがとどかないひと/そうよばれてたひと/いまとなりにいるの/ゆめではないよね/おはようのひとこと/あしたもいわせてね/あなたもしらないの/このむねのおとを")
put("おわり", [f("x:0.5 x:0.5 x:1 x:2", "5 1' 2' 1'"), "R:4"], "すきだよ", bars=S.sc("おわり")[6:8])


# ================= 伴奏 =================
def bass(b, pat="r-------r-------"):
    """ベースは音数を少なく（1小節 1〜4 音）。r＝根音、5＝5度、R＝1オクターブ上、-＝のばす、.＝休み"""
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
    """シンセの16分のかけ上がり（和音の音を上がって下がる）。k で形を変える"""
    t = sorted(voice(S.chords[b], 74, 4)); u = t + [t[0] + 12, t[1] + 12]
    o = ([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3], [4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5], [0, 2, 1, 3, 2, 4, 3, 5, 4, 3, 2, 1, -1, -1, -1, -1], [0, 1, 2, 3, -1, -1, 2, 3, 4, 5, -1, -1, 4, 3, 2, 1],
         [0, -1, 2, -1, 1, 3, -1, 2, 4, -1, 3, -1, 2, 4, 5, -1])[k % 5]
    ARP.bar(b, " ".join("R:0.25" if x < 0 else f"{N(u[x])}:0.25" for x in o))


def bell(b, k=0):
    BELL.bar(b, KEY(b).mel(("R:2 5':0.25 3':0.25 2':0.25 1':0.25 6:0.25 5:0.25 3:0.5", "R:2.5 3:0.25 5:0.25 6:0.25 1':0.25 2':0.25 3':0.25", "R:2 3':0.25 5':0.25 3':0.25 2':0.25 1':0.5 R:0.5", "R:3 1':0.25 2':0.25 3':0.25 5':0.25")[k % 4], oct=4))


TR = [None]


def gtr(b, patL=None, patR=None, sung=None, feel=16):
    """左右のギター。左は低い側の形、右はまん中の弦の三和音。歌が鳴っているマスは、間を作る"""
    c = S.chords[b]
    if patL: SL.bar(b, G2.with_space(patL, sung, keep=(0, 8)) if sung else patL, G2.low_shape(c), feel=feel)
    if patR: TR[0] = G2.triad(c, TR[0]); SR.bar(b, G2.with_space(patR, sung, keep=(0, 8)) if sung else patR, TR[0], feel=feel)


GA = ("D.dUd.dUD.dUdUd.", "D.dUdUd.D.dUd.dU", "D.xUd.dUD.dUdUx.", "DUdUd.dUD.xUdUdU")
GB = ("d.dUd.dUd.dUd.dU", "dUd.dUdUd.dUd.d.", "d.dUdUd.dUd.dUdU", "dUdUd.dUd.dUdUd.")
HK = ("1':0.5 2':0.5 3':0.5 5':1 3':0.5 2':0.5 1':0.5", "2':0.5 3':0.5 2':0.5 1':1 6:0.5 1':1", "1':0.5 2':0.5 3':0.5 5':1 6':0.5 5':0.5 3':0.5", "5':1.5 3':0.5 2':1 R:1",
      "1':0.5 2':0.5 3':0.5 5':1 3':0.5 2':0.5 1':0.5", "2':0.5 3':0.5 2':0.5 1':1 6:0.5 1':1", "3':0.5 5':0.5 6':0.5 1'':1 6':0.5 5':0.5 3':0.5", "2':0.5 3':0.5 5':1 1'':2")   # フック（5音だけ）。8小節で1まわり
ANS = ("R:2 3':0.25 5':0.25 3':0.25 2':0.25 1':1", "R:2.5 1':0.25 2':0.25 3':0.5 5':0.5", "R:2 5':0.5 3':0.25 2':0.25 1':0.5 6:0.5", "R:2.5 6:0.25 1':0.25 2':0.25 3':0.25 5':0.5")   # リードギターの返事（歌の切れ目）
SOLO = ("2':1 4':0.5 2':0.25 4':0.25 5':1 4':0.5 2':0.5", "3':0.5 5':0.5 3':0.25 2':0.25 1':0.5 7:0.5 2':0.5 3':1", "4':0.25 5':0.25 6':0.5 5':0.5 4':0.5 2':0.5 4':0.5 5':1", "5':1.5 4':0.25 5':0.25 6':1 5':1",
        "6':0.5 5':0.25 4':0.25 2':0.5 4':0.5 5':0.5 6':0.5 1'':1", "1'':0.5 5':0.5 4':0.25 5':0.25 4':0.5 2':0.5 1':0.5 2':1", "3':0.25 5':0.25 3':0.25 5':0.25 1'':0.5 5':0.5 3':0.5 5':0.5 1'':1", "2'':3 R:1")
FOUR = ("X...X...X...X...", "....X.......X...", "x.x.x.x.x.x.x.x.")          # ドラムは音数を少なく: 4つ打ち、スネアは2・4拍
OFFH = ("X...X...X...X...", "....X.......X...", "..x...x...x...x.")          # サビ: 裏のハイハット（ダンス）
HALFT = ("X.......X.......", "........X.......", "x...x...x...x...")
RUN = ("X.....X.X.....X.", "....X.......X...", "x.x.x.x.x.x.x.x.")           # 2番Aの後半: かけ足


def hook(b, i, gtr_too=False):
    HOOK.bar(b, KEY(b).mel(HK[i % 8], oct=3))
    if gtr_too: LEAD.bar(b, KEY(b).mel(HK[i % 8], oct=3))


H16, H16o = "XxxxXxxxXxxxXxxx", "XxxxXxxxXxxxXxO."                      # ハイハット主体の16ビート（頭を強く。o＝オープン）
K16 = ("X.....X...X.....", "X.........X..X..", "X.....X.....X...", "X..X......X.....")
SN, SNg = "....X.......X...", "....X..o.o..X..."
SAWC = ("x-------x---x---", "x---x---x-------", "x-----x---x-----", "x---x---x-x-x---")     # 和音は小節の中で切らない
SAWD = ("x--x--x---x--x--", "x-----x---x-----", "x--x--x-----x-x-", "x-----x---x-x---")


def fill(b, kind):
    """フィル4種。0: スネア→タムへ下りる2拍／1: スネアだけ1拍／2: スネア2つとタム3つ／3: タムを高い方から低い方へ"""
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; sung = G2.sung_slots(V, S, b)
    head = (i == 0 and (kind in ("chorus", "break") or n == "静かな場面")) or (i == 8 and n in ("2番A", "最後のドロップ", "1番A")) or (i == 4 and n == "前奏")
    if head: fxh(b, 0, "down" if n == "静かな場面" else "impact", 2); (b > 0 and fxh(b - 1, 2, "rev", 2))      # 場面の頭に当たる音、その前に逆回しのシンバル
    if (kind == "pre" and i >= 4) or (n == "静かな場面" and i >= 4): swell(b)
    if (n == "前奏" and i in (0, 2)) or (n == "静かな場面" and i % 2 == 0) or (kind == "chorus" and i in (4, 12)): fxh(b, 1 if kind == "chorus" else 0, "kira", 1)
    if last and kind in ("pre", "chorus"): hat_roll(HATR, b, 1)
    if n == "前奏":                                                      # のばす和音とフックがつながって鳴る → タムのフィル → 全員（16ビート）
        if i < 4:
            saw(b, "x---------------"); bass(b, "r---------------"); hook(b, i); D.set(b, "................", "................", "................")
            if i >= 2: arp(b, 0)
            if odd: bell(b, i // 2)
            if i == 3: fill(b, 0)
        else:
            D.set(b, K16[i % 4], SN, H16o if odd else H16); bass(b, ("r-------r-----5-", "r-----R---r-----")[i % 2]); gtr(b, GA[i % 4], GB[i % 4]); saw(b, "x-------x-------"); hook(b, i, True)
            if i == 4: crash(D, b, "C2", 4)
            if last: fill(b, 2)
    elif n == "1番A":                                                    # 前半: ベースとシンセの細かい音、ギターは裏だけ。後半: 16ビート
        first = i < 8
        if first:
            D.set(b, HALFT[0], HALFT[1], "x.x.x.x.x.x.x.x."); gtr(b, None, "..U...U...U...U.", feel=8); arp(b, 4)
            if i == 7: fill(b, 1)
        else:
            D.set(b, K16[i % 4], SNg, H16o if i % 4 == 3 else H16); gtr(b, GA[i % 4], GB[(i + 2) % 4], sung=sung); arp(b, 2 + i % 2); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
            if i == 8: crash(D, b, "C2", 4)
            if last: fill(b, 3)
        bass(b, ("r-----r---------", "r---------r-----", "r--r------------", "r-------r-----5-")[i % 4])
        if i % 4 == 3: bell(b, i // 4)
    elif n == "2番A":                                                    # 前半: 音を減らし、リードギターが歌に返事。後半: 16ビートでかけ足
        if i < 8:
            D.set(b, "X.........X....." if not odd else "X.......X.......", "............X..." if odd else "................", "x.x.x.x.x.x.x.x."); bass(b, "r-----------5---" if odd else "r---------------")
            gtr(b, "D...............", "D......U........" if odd else "D..............."); saw(b, "x---------------", 60)
            if odd: LEAD.bar(b, KEY(b).mel(ANS[(i // 2) % 4], oct=3))
            if i == 7: fill(b, 2)
        else:
            D.set(b, K16[(i + 1) % 4], SNg, H16o if odd else H16); bass(b, ("r-------r-----5-", "r-----R---r-----", "r---------r---r-", "r---5---r---R---")[i % 4])
            gtr(b, GA[i % 4], GB[i % 4], sung=sung); CLP.bar(b, "R:1 B4:1 R:1 B4:1"); arp(b, i)
            if i == 8: crash(D, b, "C2", 4)
            if last: fill(b, 1)
    elif n in ("1番B", "2番B"):                                          # ベースが1段ずつ上がる。最後はフィルでサビへ
        gtr(b, "D.......d.dUd.dU" if i < 4 else GA[i % 4], GB[i % 4] if i >= 4 else None, sung=sung); saw(b, "x---------------" if i < 4 else "x-------x-------", 62 + i)
        D.set(b, HALFT[0] if i < 4 else FOUR[0], HALFT[1] if i < 4 else SN, "x.x.x.x.x.x.x.x." if i < 4 else H16); bass(b, "r---------------" if i < 4 else "r-----r---------")
        if i >= 4: arp(b, i)
        if i == 3: fill(b, 1)
        if i == 6: FX.bar(b, "C5:4")
        if last: FX.bar(b, "C5:4"); fill(b, 0)
    elif n == "立ち上げ":                                                # 歌なし。もう半音上の調で7段登る。ドラムがだんだん細かくなる
        saw(b, "x-------x-------" if i < 4 else "x---x---x---x---", 62 + i); bass(b, "r---------------" if i < 4 else "r-------r-------"); arp(b, i); gtr(b, GA[i % 4] if i >= 2 else None, GB[i % 4] if i >= 4 else None)
        D.set(b, "X.......X......." if i < 2 else "X...X...X...X...", "................" if i < 2 else ("....x.......x..." if i < 4 else "x...x...x...x..." if i < 6 else "x.x.x.x.x.x.x.x."), "x.x.x.x.x.x.x.x." if i < 4 else H16)
        if i >= 4: HOOK.bar(b, KEY(b).mel(("1':0.5 2':0.5 3':3", "2':0.5 3':0.5 5':3", "3':0.5 5':0.5 6':3", "5':0.5 6':0.5 1'':3")[i - 4], oct=3))
        if i >= 6: FX.bar(b, "C5:4")
        if last: fill(b, 0)
    elif n == "落ちサビ":                                                # のばす和音と歌だけ。後半からベースと細かい音
        saw(b, "x---------------", 65); swell(b); D.set(b, "................", "................", "................")
        if i >= 4: bass(b, "r---------------"); arp(b, 4)
        if i % 4 == 0: fxh(b, 0, "kira", 1)
    elif n in ("サビ1", "サビ2", "最後のサビ", "大サビ"):                          # 前半: 4つ打ちと裏のハイハット（ダンス）。後半: 16ビート
        D.set(b, OFFH[0], OFFH[1] if i % 8 != 6 else "....X.......X.X.", OFFH[2] if i < 8 else (H16o if odd else H16)); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 8 == 0: crash(D, b, "C2", 4)
        bass(b, ("r-------r-----5-", "r-----R---r-----", "r---------r---r-", "r---5---r---R---")[i % 4]); saw(b, SAWC[i % 4])
        gtr(b, GA[i % 4], GB[(i + 1) % 4], sung=sung); arp(b, i)
        if odd and i not in (7, 15): HOOK.bar(b, KEY(b).mel(("R:2.5 3':0.5 5':1", "R:3 2':0.5 3':0.5", "R:2.5 5':0.5 6':1", "R:3 3':0.5 5':0.5")[(i // 2) % 4], oct=3))   # フックのシンセが、句の終わりに短く返事
        if i == 7: fill(b, 3)
        if last: FX.bar(b, "C5:4"); fill(b, 0)
    elif n in ("ドロップ1", "ドロップ2", "最後のドロップ"):              # 歌なし。フックを、シンセとリードギターがいっしょに弾く
        k8 = i % 8; h16 = n == "最後のドロップ" and i >= 8 or n == "ドロップ2"
        D.set(b, OFFH[0], OFFH[1], (H16o if odd else H16) if h16 else OFFH[2]); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if k8 == 0: crash(D, b, "C2", 4)
        bass(b, ("r--r--r---------", "r-------r-----5-", "r--r------r-----", "r-----r-----R---")[i % 4]); saw(b, SAWD[i % 4]); gtr(b, GA[(i + 2) % 4], GB[i % 4])
        hook(b, i, True)
        if n == "最後のドロップ" and i >= 8: arp(b, i)
        if k8 == 3: fill(b, 2 if n != "ドロップ2" else 1)
        if k8 == 7: fill(b, 0 if n != "ドロップ2" else 3)
    elif n == "ギターソロ":
        D.set(b, K16[i % 4], SNg, H16o if odd else H16); bass(b, "r-----r---------" if i < 4 else "r-------r-----5-"); saw(b, "x-------x-------", 62 + i)
        gtr(b, GA[i % 4], GB[i % 4]); LEAD.bar(b, KEY(b).mel(SOLO[i], oct=3))
        if i == 0: crash(D, b, "C2", 4)
        if i == 3: fill(b, 1)
        if last: fill(b, 3)
    elif n == "静かな場面":                                              # 半分の速さ。クリーンのギターと、のばす和音とベース
        gtr(b, "D...d.dUd...d.dU" if not odd else "D.dUd...d.dUd...", "d.dUd...d.dUd.dU" if not odd else "d...d.dUd.dUd...", sung=sung); saw(b, "x---------------", 60); bass(b, "r---------------")
        D.set(b, "X..............." if i >= 4 else "................", "........x......." if i >= 4 else "................", "x...x...x...x...")
        if i == 3: bell(b, 1)
        if last: fill(b, 1)
    elif n == "おわり":                                                  # フックをもう一度。最後は全員で1打、和音はのびたまま
        if i < 6:
            D.set(b, OFFH[0], OFFH[1], H16o if odd else H16); bass(b, "r-------r-----5-"); saw(b, "x-------x-------"); gtr(b, GA[i % 4], GB[i % 4]); hook(b, i, True); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
            if i == 0: crash(D, b, "C2", 4)
            if i == 5: fill(b, 0)
        elif i == 6: D.set(b, "X...............", "................", "................"); crash(D, b, "C2", 4); bass(b, "r---------------"); saw(b, "x---------------"); gtr(b, "D...............", "D...............")
        else: bass(b, "r---------------"); saw(b, "x---------------")

for b_, hs in FXH.items(): FXT.bar(b_, fx_bar(*hs))
SL.end(S.nb); SR.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース×ダンス×ロックの恋の歌（164・イ長調 → 変ロ長調 → ロ長調・約5分）。高嶺の花（見えていても手が届かない、あこがれの人）がコンセプト。"
          "教室でいちばん遠い席の人に、あいさつから少しずつ近づき、最後に好きと言う話。サビのたびに調が半音上がる。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "シンセのかけ上がり（矩形波のプラック）", mid=90, down=12, up=10, seed=29); humanize(path, "リードギター", mid=98, down=10, up=12, seed=3)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("大サビ", 0, None, KS[2])], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in (("1番A", 0.85),):
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    p_["barGain"] = g[:S.nb]
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
