# KFB 02「強面ハーバリウム」Scary-Face Herbarium（仮）— Kawaii future bass ＋ 明るいヒップホップ。4分の4・140（半分の速さに感じるノリ・16分をはねる）・ヘ長調。約4分07秒。
#
# v4（2026-11-23）: v3 は場面の大きさの形はよくなったが、点が 7.45 に落ちた（広い和音を大きくすると点が下がる）→ 和音を v2 と v3 の間にし、上をもう少し丸めた（4.5k → 4kHz）。
# v3（2026-11-23）: v2 は Aメロ −14.6dB がサビ −15.0dB より大きかった → Aメロを少し下げ、サビとドロップの和音を上げ、サビの和音の休みを減らした。
# v2（2026-11-23）: v1 は 歌 7.76・BGM 7.64 だが、場面の大きさがどこも −15〜−16dB で平ら（静かな場面とサビが同じ、ドロップが Aメロより小さい）。
#   ピアノが大きすぎ、頭で開くフィルターを掛けた広い和音が小さすぎた → ピアノを 0.6 倍、広い和音を 1.6 倍、フィルターの閉じた所を 1.5k → 2kHz。
# v1（2026-11-23）: 人間「次はKawaii_future_bassに明るいヒップホップのテイストを混ぜてみようか。コンセプトは美女と野獣」→ 物語の案から「A」。
#
# コンセプト（美女と野獣。昔話そのものだけを元にする）: こわい顔で、だれも話しかけない左の席の同級生。落とした本をひろったら、紙の間にすみれがはさんであった。
#   野獣＝見た目で決めつけられている人／バラ＝はさんだ花／呪いがとける所＝みんなの前で、ふつうに名前を呼ぶ。
# ジャンルの見本（調べたこと）: フューチャーベースはヒップホップやソウルから借りる。ドラムはトラップ寄り（スネアは3拍め・ハイハットを食い気味に、連打）。はねるノリは2つめの音を遅らせる。ベースは長くのばしてすべらせる。
#   明るいヒップホップなので長調で、手びょうしとはねるノリを前に出す。ピアノの和音の合いの手（ジャズ寄りの和音）。
# 物語の出来事 → その時の音:
#   出だし（朝の教室）              → 手びょうしと低いベースと、ピアノの和音だけ
#   Aメロ＝ラップ（だれも話しかけない）→ 音の高さをしぼった、はねるラップ。頭4小節は手びょうしとベースだけ。ハイハットの連打が、紙をめくる音の役
#   Bメロ（こわいのは顔だけ）        → 歌う。ベースを抜く。最後に1拍の無音
#   サビ（見た目で決めるなんて）     → 広い和音を休みを入れて切る。まん中で全員が止まる
#   ドロップ                         → 歌なし。夢のようなリードと「ポッ」という音がかけ合う。4小節ごとに止まる
#   静かな場面（みんなの前で名前を呼ぶ）→ ピアノと歌だけ
#   最後のサビ・ドロップ             → 全員
# この曲だけの物: 紙をめくる音の役のハイハットの連打と、ベースのすべり。サビの終わりの ♭VII → ♭VI から、ドロップの頭の IV に落ちる。
# 歌詞: 曲名の言葉（こわもて・ハーバリウム）と「やじゅう」は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *

S = Song("28", "kowamote", "強面ハーバリウム（仮）", "Scary-Face Herbarium", 140, 4, "F", "major", "カワイイ・フューチャーベース×ヒップホップ（ボカロ）")
S.kit = "electro"; S.flags = S.flags + " --piano salamander --space room --space-wet 0.08"
K1 = Key("F", "major")

# コード進行: ふつうの進行にしない。
#   Aメロ: I → ♭VII → VI → ♭VI と、ベースが全音・半音で下がる（明るいのに少しはみ出す）。終わりは II7 → IIm9・V7sus4
#   Bメロ: IV → IIIm → IIm → #Idim（半音で下からつなぐ）→ IIm → IIIm・VI7 → IV → V7sus4
#   サビ: IV → V/IV → IIIm → VIm → IIm → V7 → I → I7 / IV → IVm6 → IIIm → VI7 → IIm → ♭II7（裏の和音）→ I → ♭VII・♭VI
#   ドロップ: IV → IIIm・VI7 → IIm → ♭II7 → I → ♭VII → ♭VI → V7sus4
VCH = ["Fmaj9", "Ebmaj7", "Dm9", "Dbmaj7", "Fmaj9", "Ebmaj7", "Dm9", "Gm9"]; VH = {6: "G7", 7: "C7sus4"}
PCH = ["Bbmaj7", "Am7", "Gm9", "F#dim7", "Gm9", "Am7", "Bbmaj7", "C7sus4"]; PH = {5: "D7"}
CCH = ["Bbmaj9", "C/Bb", "Am7", "Dm9", "Gm9", "C7", "Fmaj7", "F7", "Bbmaj9", "Bbm6", "Am7", "D7", "Gm9", "Gb7", "Fmaj9", "Ebmaj7"]; CH = {15: "Dbmaj7"}
DCH = ["Bbmaj9", "Am7", "Gm9", "Gb7", "Fmaj9", "Ebmaj7", "Dbmaj7", "C7sus4"]; DH = {1: "D7"}
HALF = {}


def scene(name, n, kind, chs, half=None, rep=1):
    b0 = sum(x[1] for x in getattr(S, "_sc", [])); S._sc = getattr(S, "_sc", []) + [(name, n)]
    S.scene(name, n, kind, chs)
    for k in range(rep):
        for i, c in (half or {}).items():
            if i + k * (n // rep) < n: HALF[b0 + i + k * (n // rep)] = c


scene("出だし", 4, "intro", VCH[:4])
scene("1番A", 16, "verse", VCH * 2, VH, 2)
scene("1番B", 8, "pre", PCH, PH)
scene("サビ1", 16, "chorus", CCH, CH)
scene("ドロップ1", 8, "break", DCH, DH)
scene("2番A", 16, "verse", VCH * 2, VH, 2)
scene("2番B", 8, "pre", PCH, PH)
scene("サビ2", 16, "chorus", CCH, CH)
scene("ドロップ2", 8, "break", DCH, DH)
scene("静かな場面", 8, "bridge", ["Bbmaj9", "C/Bb", "Am7", "Dm9", "Gm9", "Bbm6", "F/A", "C7sus4"])
scene("最後のサビ", 16, "chorus", CCH, CH)
scene("最後のドロップ", 16, "break", DCH * 2, DH, 2)
scene("おわり", 4, "outro", ["Bbmaj9", "Bbm6", "Fmaj9", "Fmaj9"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
SUB = S.track("すべる低いベース", "bass", patch="kfbSub", volume=0.06, pan=0, duck=0.12)
PF = {"type": "pluckfilter", "freq": 2000, "depth": 0.6, "rate": 30, "hold": 4}                                             # 音の頭で開いて、すぐ閉じる（見本の和音の形）
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.066, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
DRP = [S.track(f"ドロップの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.098, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
STB = [S.track(f"和音の頭の明るい一打{i + 1}", "lead", patch="kfbSawStab", volume=0.04, pan=(-0.35, 0, 0.35)[i], reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(3)]
PAD = [S.track(f"やわらかいパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.05, pan=(-0.2, 0.2, 0)[i], reverb=0.3) for i in range(3)]
PNL = [S.track(f"ピアノ（左手）{i + 1}", "piano", volume=0.034, pan=-0.25, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(3)]
PNR = [S.track(f"ピアノ（右手）{i + 1}", "piano", volume=0.036, pan=0.25, reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(4)]
BOO = S.track("ポッという音", "lead", patch="kfbBoops", volume=0.07, pan=0.3, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.3}])
DRM = S.track("夢のようなリード", "lead", patch="kfbDreamLead", volume=0.06, mono=True, pan=-0.15, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = F4。低い 3, = A3、高い 1' = F5）=================
def f(pat, pitches):
    """リズムの型（x:長さ と R:長さ）に、高さを順に当てはめる"""
    it = iter(pitches.split()); return " ".join((next(it) + t[1:]) if t[0] == "x" else t for t in pat.split())


# リズムの型（16分をまぜる。はねるノリで歌う）。あたりつきの型は使わない
Ra, Rb = "x:0.25 x:0.25 x:0.5 R:0.5 x:0.25 x:0.25 x:0.5 x:0.5 R:1", "R:0.5 x:0.5 x:0.25 x:0.25 x:0.5 R:0.25 x:0.25 x:0.5 x:0.5 R:0.5"
Rc, Rd = "x:0.5 x:0.25 x:0.25 R:0.5 x:0.5 x:0.25 x:0.25 x:0.5 R:1", "R:0.25 x:0.25 x:0.5 x:0.5 x:0.25 x:0.25 R:0.5 x:0.5 x:0.5 R:0.5"
Re, Rf, Rg, Rh, Ri = "x:0.75 x:0.25 x:1 R:2", "R:0.5 x:0.5 x:0.5 x:1 R:1.5", "x:0.25 x:0.75 x:1.5 R:1.5", "x:0.25 x:0.25 x:0.5 x:1 R:2", "x:0.5 x:0.5 x:1.5 R:1.5"
RA = [f(Ra, "5, 6, 1 1 1 6, 1"), f(Re, "2 1 6,"), f(Rb, "6, 1 3 3 1 6, 1"), f(Rf, "5, 1 1"),
      f(Rc, "1 1 3 1 3 5 3"), f(Rg, "2 4 2"), f(Rd, "3 3 1 2 2 1 6,"), f(Rh, "2 2 1 5,")]                                   # ラップ（前半）: 高さは3つ4つだけ
RA2 = [f(Rc, "1 3 5 5 5 3 5"), f(Re, "4 2 2"), f(Ra, "3 5 6 5 3 1 3"), f(Rg, "1 5, 1"),
       f(Rb, "5 5 6 5 3 5 6"), f(Rf, "6 4 2"), f(Rd, "5 5 3 2 2 1 2"), f(Ri, "2 4 5")]                                      # ラップ（後半）: 少し歌に寄る
Ba, Bb_, Bc = "x:0.75 x:0.25 x:0.5 R:0.5 x:0.5 x:0.25 x:0.25 R:1", "x:2 R:2", "x:0.5 x:0.25 x:0.25 x:0.5 x:1.5 R:1"
VB = [f(Ba, "3 5 6 6 5 6"), f(Bb_, "5"), f(Ba, "4 5 6 6 5 4"), f(Bb_, "5"), f(Ba, "4 6 6 6 5 6"), f(Bb_, "7"), f(Bc, "6 6 7 6 1'"), "R:4"]
Ca, Cb_ = "x:0.75 x:0.25 x:0.5 x:0.5 R:0.5 x:0.5 x:0.5 x:0.5", "R:0.5 x:0.25 x:0.25 x:0.5 x:0.75 x:0.25 x:0.5 x:1"
Ce, Cf, C2n, C1n = "R:0.25 x:1.25 x:0.5 x:1 R:1", "x:1 R:0.5 x:0.5 x:1 R:1", "x:0.75 x:1.25 R:2", "x:1.5 R:2.5"
VC = [f(Ca, "5 6 7 6 5 3 5"), f(Ce, "6 5 3"), f(Cb_, "3 5 6 5 3 2 3"), f(Cf, "2 1 2"), f(Ca, "2 3 5 6 7 6 5"), f(Ce, "6 5 2"), f(Cb_, "3 5 6 5 3 1 3"), f(C2n, "5 3"),
      f(Ca, "5 6 7 6 5 3 5"), f(Ce, "5 4 2"), f(Cb_, "3 5 7 1' 7 5 7"), f(Cf, "6 5 3"), f(Ca, "2 4 5 6 1' 7 6"), f(Ce, "7 7 4"), f(Cb_, "5 5 3 2 3 5 6"), f(C1n, "5")]
Qa, Qb, Qc = "x:0.5 x:0.5 x:1 R:0.5 x:0.25 x:0.25 x:1", "x:1 x:1 R:2", "x:2.5 R:1.5"
VQ = [f(Qa, "3 2 1 1 2 3"), f(Qb, "5 3"), f(Qa, "5 3 2 2 3 5"), f(Qb, "6 5"), f(Qa, "4 2 1 1 2 4"), f(Qb, "5 4"), f(Qa, "3 5 6 5 6 7"), f(Qc, "1'")]
CB = "のろいなんかじゃないよ/だれもよばないだけだ/なまえをふつうによぶ/それがまほうだよ"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else K1.mel(x, oct=4) for x in lines]
    for k, sg in enumerate(text.split("/")):                              # 2小節ごとに、音の数と文字の数が合っているか確かめる
        nn = sum(1 for x in " ".join(lines[k * 2:k * 2 + 2]).split() if not x.startswith("R"))
        assert nn == mora(sg), (name, k, sg, nn, mora(sg))
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("1番A", RA + RA2, "ひだりのせきのきみは/まゆげがいつもななめ/だれもはなしかけない/ろうかでみちがひらくよ/おとしたほんをひろう/ひらいたかみのあいだ/ちいさなすみれがいた/ていねいなじでなまえ")
put("1番B", VB, "こわいのはかお/それだけなのに/だれもしらない/わたしだけ")
put("サビ1", VC, "みためできめるなんて/そんしてるよみんなは/とげのあるそのおくに/やさしいねがあるの/" + CB)
put("2番A", RA + RA2, "ほうかごかだんのまえ/しゃがんでるおおきなせ/みずやるてがやさしい/みんなとおくでみてるよ/こわくないよといえば/うそだといわれるかな/それでもみていたから/すみれのなまえのじを")
put("2番B", VB, "ゆうきがいるの/きみにじゃなくて/わたしのほうに/いまいるの")
put("サビ2", VC, "みためできめるなんて/そんしてるよみんなは/つちのついたゆびさき/だれよりきれいだよ/" + CB)
put("静かな場面", VQ, "あさのきょうしつで/みんながいるまえ/むねがなるけれど/きみをよんだよ")
put("最後のサビ", VC, "ふりむいたそのかおが/はじめてほどけていく/きょうしつがしんとする/それからざわめいた/" + CB)
put("おわり", [f("x:0.25 x:0.25 x:0.5 x:2 R:1", "5 6 1' 1'"), "R:4"], "あしたも", bars=S.sc("おわり")[2:4])


# ================= 伴奏 =================
def ch2(b): return (S.chords[b], HALF.get(b))


def chords(tr, b, pat="hold", center=65):
    """5声の和音。hold＝のばす（まん中で変わる小節は2拍ずつ）、ほか＝16マスの型（x＝打つ、-＝のばす、.＝休み）。和音を打つたびに、頭にだけ短く明るい一打を重ねる"""
    c1, c2 = ch2(b); v1 = sorted(voice(c1, center, 5)); v2 = sorted(voice(c2, center, 5)) if c2 else v1
    p2 = ("x-------" + ("x-------" if c2 else "--------")) if pat == "hold" else pat
    for j in range(5):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and p2[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if p2[i] == "." else f"{N((v1 if i < 8 else v2)[j])}:{L * 0.25:g}"); i += L
        tr[j].bar(b, " ".join(out))
    for j in range(3):
        STB[j].bar(b, " ".join(f"{N((v1 if i < 8 else v2)[-3 + j])}:0.25" if p2[i] == "x" else "R:0.25" for i in range(16)))


def sub(b, pat, slide=True):
    """サブベースを8分のマスで。x＝根音（前半は前半の和音、後半は後半の和音）、5＝5度、-＝のばす、.＝休み。小節の最後の音は、次の小節の根音へすべらせる"""
    c1, c2 = ch2(b); r1 = low(c1, "D1"); r2 = low(c2, "D1") if c2 else r1; ev = []; i = 0
    while i < 8:
        L = 1
        while i + L < 8 and pat[i + L] == "-": L += 1
        r = r1 if i < 4 else r2
        ev.append(None if pat[i] == "." else (r + (7 if pat[i] == "5" else 0), L * 0.5) if pat[i] != "." else None) if pat[i] != "." else ev.append(("R", L * 0.5)); i += L
    out = []; lastn = max((k for k, e in enumerate(ev) if e[0] != "R"), default=-1)
    nxt = low(S.chords[b + 1], "D1") if b + 1 < S.nb else None
    for k, e in enumerate(ev):
        if e[0] == "R": out.append(f"R:{e[1]:g}")
        elif slide and k == lastn and nxt is not None and nxt != e[0] and abs(nxt - e[0]) <= 7 and e[1] >= 0.5: out.append(f"{N(e[0])}:{e[1]:g}>{N(nxt)}")
        else: out.append(f"{N(e[0])}:{e[1]:g}")
    SUB.bar(b, " ".join(out))


def piano(b, patL=None, patR=None):
    """ピアノ: 左手は低い3声、右手は上の4声（9th や 7th をふくむ）。16マスの型"""
    c1, c2 = ch2(b)
    for tr, pat, cen, n in ((PNL, patL, 55, 3), (PNR, patR, 69, 4)):
        if not pat: continue
        v1 = sorted(voice(c1, cen, n)); v2 = sorted(voice(c2, cen, n)) if c2 else v1
        for j in range(n):
            out = []; i = 0
            while i < 16:
                L = 1
                while i + L < 16 and pat[i + L] == "-": L += 1
                out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N((v1 if i < 8 else v2)[j])}:{L * 0.25:g}{'!' if i % 8 == 0 else ',' if i % 4 == 2 else ''}"); i += L
            tr[j].bar(b, " ".join(out))


def pad(b, lift=0):
    v = sorted(voice(S.chords[b], 62 + lift, 3))
    for j in range(3): PAD[j].bar(b, f"{N(v[j])}:4")


def boop(b, k=0):
    """ポッという音: 和音の音で、歌の切れ目に短い返事"""
    c1, c2 = ch2(b); t = sorted(voice(c2 or c1, 77, 4))
    BOO.bar(b, ("R:2.5 {0}:0.25 R:0.25 {2}:0.5 R:0.5", "R:2 {2}:0.25 {1}:0.25 R:0.5 {3}:0.5 R:0.5", "R:3 {1}:0.25 {2}:0.25 {3}:0.5", "R:2.5 {3}:0.25 R:0.25 {1}:0.25 {0}:0.25 R:0.5")[k % 4].format(*[N(x) for x in t]))


DL = ("5:0.5 R:0.5 6:0.25 7:0.25 R:0.5 5:0.5 R:0.5 3:0.5 5:0.5", "3:0.5 R:0.5 5:0.25 7:0.25 R:0.5 6:0.5 R:0.5 5:0.5 R:0.5",
      "2:0.25 4:0.25 5:0.5 R:0.5 6:0.5 R:0.5 5:0.5 R:0.5 4:0.5", "5:0.25 5:0.25 R:0.5 1':0.5 R:0.5 5:0.5 3:0.5 R:1",
      "5:0.5 R:0.5 3:0.25 5:0.25 R:0.5 2:0.5 R:0.5 1:0.5 2:0.5", "4:0.5 R:0.5 2:0.25 4:0.25 R:0.5 6:0.5 R:0.5 4:0.5 R:0.5")   # ドロップのリード（小節 0・2・4・5 の和音に合わせた音。休みをはさむ）


def clap(b, pat="R:2 B4:1 R:1"): CLP.bar(b, pat)
def gate(k): return ("x-------x---x-..", "x---x-..x-------", "x-------x---x-..", "x---x---x-x-....")[k]      # v3: 休みは小節の終わりだけ（サビが Aメロより小さく測れたので、のばす所を増やした）
# ドラム（半分の速さに感じる: スネアと手びょうしは3拍め）。ハイハットは8分に、16分の連打（紙をめくる音の役）をまぜる
RAP = [("X......X..X.....", "........X.......", "x.x.x.x.x.x.xxxx"), ("X..X......X..X..", "........X.....x.", "x.x.xxx.x.x.x.x."), ("X......X..X.....", "........X.......", "x.x.x.x.xxx.x.x."), ("X..X...X..X.....", "........X...x...", "x.xxx.x.x.x.xxxx")]
CHO = [("X.....X...X.....", "........X.......", "x.x.x.x.x.x.x.x."), ("X..X..X....X..X.", "........X.....X.", "x.x.x.xxx.x.x.x.")]
DRO = [("X..X......X..X..", "........X.......", "x.x.xxx.x.x.x.x."), ("X.....X..X....X.", "........X...X...", "x.xxx.x.x.x.xxxx")]

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "出だし":                                                    # 手びょうしと低いベースと、ピアノの和音
        clap(b); sub(b, "x--...x-" if not odd else "x-----.x"); piano(b, "x...............", "..x...x.....x..."); pad(b, -5)
        D.set(b, "X.........X....." if i >= 2 else "................", "................", "........xxxx...." if odd else "................")
    elif n in ("1番A", "2番A"):                                          # ラップ。頭4小節は手びょうしとベースだけ
        thin = i < 4 and n == "1番A"; g = RAP[i % 4]
        if i == 7: D.set(b, "X......X........", "................", "x.x.x.x.xxxxxxxx")                 # 8小節め: 後半は連打（ページをめくる）だけ
        elif thin: D.set(b, "X.........X.....", "................", "............xxxx" if odd else "................")
        else: D.set(b, g[0], g[1] if not last else "........X...x.xx", g[2])
        clap(b); sub(b, "x--....." if i == 7 else ("x--...x-", "x-.x---.", "x--..x.x", "x-....x-")[(i + (1 if n == "2番A" else 0)) % 4])
        if not thin: piano(b, "x.......x......." if i % 4 != 3 else "x...............", ("..x...x.....x...", "....x.....x.x...", "..x.....x...x...", "..x.x.......x...")[i % 4] if i != 7 else "..x.............")
        if i >= 8: pad(b, -5)
        if i % 4 == 1 and not thin: boop(b, i // 4 + (2 if n == "2番A" else 0))
    elif n in ("1番B", "2番B"):                                          # 歌う。ベースを抜く。最後の1拍は無音
        if last:
            FX.bar(b, "C5:3 R:1"); piano(b, "x---x---x-x-....", "x---x---x-x-...."); D.set(b, "................", "x...x...x.xx....", "................"); continue
        pad(b, i // 2); piano(b, "x...............", "x-------........" if i < 4 else "x-----..x-----..")
        D.set(b, "X..............." if i < 4 else "X.........X.....", "................" if i < 6 else "....x.......x.x.", "x...x...x...x..." if i < 4 else "x.x.x.x.x.x.xxxx"); clap(b, "R:2 B4:1 R:1" if i < 4 else "R:1 B4:1 R:1 B4:1")
        if i == 6: FX.bar(b, "C5:4"); boop(b, 2)
    elif n in ("サビ1", "サビ2", "最後のサビ"):                          # 広い和音を、休みを入れて切る
        g = CHO[i % 2]
        if i == 7:                                                        # まん中: 3〜4拍めは全員が休む（ポッという音だけ）
            D.set(b, "X.....X.........", "................", "x.x.x.x........."); chords(SAW, b, "x-----.........."); sub(b, "x--.....", slide=False); boop(b, 1); continue
        if last:                                                          # 終わり: ♭VII・♭VI を1打ずつ。最後の1拍は全員がだまる
            D.set(b, "X.......X.......", "........X.x.....", "x.x.x.x.x.x....."); chords(SAW, b, "x-----..x---...."); sub(b, "x--.x-..", slide=False); FX.bar(b, "C5:3 R:1"); continue
        D.set(b, g[0], g[1], g[2]); clap(b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        chords(SAW, b, gate(i % 4)); sub(b, ("x--....x", "x-.x--.5", "x--..x..", "x-.x..x-")[i % 4]); piano(b, "x...............")
        if i % 4 == 3: boop(b, i // 4)
    elif n in ("ドロップ1", "ドロップ2", "最後のドロップ"):              # 歌なし。夢のようなリードと、ポッという音がかけ合う。4小節ごとに止まる
        g = DRO[i % 2]; k8 = i % 8
        if k8 == 3:
            D.set(b, "X..X..X.........", "................", "x.x.x.x.xxxxxxxx"); chords(DRP, b, "x--x--x........."); sub(b, "x--x....", slide=False); boop(b, 1); continue
        if k8 == 7:
            D.set(b, "X.X.X.X.XXXX....", "........x.x.....", "x.x.x.x.xxxx...."); chords(DRP, b, "x-x-x-x-xxxx...."); sub(b, "x-x-xx..", slide=False); continue
        D.set(b, g[0], g[1], g[2]); clap(b)
        if k8 == 0: crash(D, b, "C2", 4)
        chords(DRP, b, ("x--x--x-..x--x..", "x-----..x--.x-..", "x--x--x-....x-x-", "x-----..x-x-....")[i % 4]); sub(b, ("x--x..x-", "x--...x-", "x--x...5", "x-..x.x-")[i % 4])
        if k8 in (0, 2, 4): DRM.bar(b, K1.mel(DL[(0, 0, 2, 0, 4)[k8] // 2 + (3 if (i // 8) % 2 else 0)], oct=4))
        elif k8 in (1, 5, 6): boop(b, k8)
    elif n == "静かな場面":                                              # ピアノと歌だけ
        piano(b, "x.......x.......", "..x.x...x.x.x..." if not odd else "..x.x.....x.x..."); pad(b, -5)
        if i == 7: D.set(b, "................", "................", "........xxxxxxxx"); FX.bar(b, "C5:4")
    elif n == "おわり":                                                  # ピアノと、ポッという音。ひとこと
        piano(b, "x...............", "x-------........" if i < 3 else "x---------------"); pad(b, -5)
        if i == 0: crash(D, b, "C2", 4); clap(b)
        if i == 1: boop(b, 0)

S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース×明るいヒップホップ（140・ヘ長調・16分をはねる）。美女と野獣がコンセプト。こわい顔でだれも話しかけない同級生の名前を、みんなの前でふつうに呼ぶ話。"
          "手びょうしとベースの出だし → はねるラップのAメロ → 歌うBメロ（ベース抜き）→ 歌のサビ → 歌なしのドロップ → 2番 → ピアノだけの静かな場面 → 最後のサビ → ドロップ → ひとこと。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ポッという音", mid=92, down=10, up=10, seed=28)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))     # 音どうしの大きさをそろえる（見本は、となりの音との差が 1dB）
    vocal_polish(path, S, {"intro": 8, "verse": 6, "pre": 12, "chorus": 15, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("最後のサビ", 0, None, K1)], vol=0.2)
    cb = {}                                                               # ドロップ: 声のチョップ（和音に合わせた高さ）
    for name in ("ドロップ1", "ドロップ2", "最後のドロップ"):
        for i_, b_ in enumerate(S.sc(name)):
            if i_ % 8 == 1: cb[b_] = "A4:0.25:や R:0.25 A4:0.25:や R:0.25 C5:0.5:は R:0.5 R:2"
            if i_ % 8 == 5: cb[b_] = "G4:0.25:や R:0.25 Bb4:0.25:や R:0.25 D5:0.5:あ R:0.5 R:2"
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    chops(path, S, cb, vol=0.3, pan=0.25)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
js["swing16"] = 0.3                                                       # 16分の裏を遅らせて、はねるノリにする
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in (("静かな場面", 0.9), ("1番A", 0.8), ("2番A", 0.8), ("出だし", 0.85)):
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    p_["barGain"] = g[:S.nb]
if VOCAL:                                                                # 歌と同じ旋律をなぞるリードを消す（人間「歌に合わせたリードの音いらない」）
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
