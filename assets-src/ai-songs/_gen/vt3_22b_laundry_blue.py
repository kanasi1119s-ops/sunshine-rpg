# vt3 22「コインランドリー・ブルー」Coin Laundry Blue（仮）— ネオソウル（4分の4・88・16分が少しはねる）。変ホ長調 → 「乾く」場面で短3度上の変ト長調。
# 第3弾（0時〜24時の街）の 21時。
#
# v4（2026-11-20）: ゼロから作り直し。v1〜v3 はトリップホップ（86・ハ短調）で `vt3_22_laundry_blue.py`。
#   人間の指示: 「18からは1曲ずつコンセプトとかジャンルをしっかり決めて作って行こうか。つまり作り直そう」。表と「物語の出来事 → その時の音」を見せて「良い」（2026-11-20）。
#
# コンセプト: 夜ふけにひとりで待つ時間。回る青い服が、だんだん海に見えてくる。となりの機械も回りだし、最後は2台の回る速さがそろう。さみしい待ち時間を、あたたかい時間に書きかえる。
# ジャンル: ネオソウル。作る前に調べた決まりごと（出どころは docs/sound/vt3-remake-plan.md の 22 v4）:
#   ・テンポ 70〜95。16分の裏を 58〜62% にはねさせる。スネアは少し後ろ、ゴーストノートを入れる。ドラムには響きをほとんど足さない
#   ・和音は 9度・11度・13度まで入れ、エレピの右手は根音を弾かない（根音はベースにまかせる）
#   ・ベースは根音だけでなく旋律で動き、ドラムに「返事」をする。すき間を残す
#   ・ギターは2本の弦の和音（3度・6度）、ハンマリングの飾り、歌のすき間の合いの手
#
# 物語の出来事 → その時の音:
#   しずかな店（まだ回っていない） → 声から始まる。2小節めにエレピの和音だけ。リズムなし
#   回りはじめる（機械が動きだす）   → 左に「回る音」（8分3つでひと回り。4拍子とずれつづける）。ハイハットから入り、3小節めでドラムとベースがそろう
#   待つ（丸い窓を見ている）         → 歌のすき間に、ベースとギター（2本の弦）が代わりばんこに返事
#   映る（窓に自分が映る）           → 弱いスネアとハイハットだけ。和音が1段ずつ上がる
#   サビ1（青が海に見える）          → 和音が広がり、歌がいちばん上へ。回る音は続く
#   となりの機械（だれかが来る）     → 右に、別の周期（8分5つ）の回る音。左とずれてからみ合う
#   待つ2・サビ2（ひとりではない）   → ギターの合いの手が増える。サビ2 はライドで刻む
#   乾く（あたたかくなる）           → 調が短3度上がる。クリーンのギターのソロ（歪みなし）
#   最後のサビ（2台がそろう）        → 2つの回る音が、初めて同じ周期（8分4つ）になる
#   止まる（機械が止まる）           → 回る音の間がだんだん長くなって止まる。声とエレピのあたたかい和音で終わる
# 歌詞: 曲名は歌わない。「洗濯」「コインランドリー」も使わない。
# 声: ウィスパー 1 種類。
from vocalo_lib import *
from lm25_lib import QUAL, PC, parse_chord, tr_chord
import gtr2_lib as G2
import random as _r

S = Song("22", "laundryblue", "コインランドリー・ブルー（仮）", "Coin Laundry Blue", 88, 4, "Eb", "major", "ネオソウル（ボカロ）")
S.kit = "naked"; S.flags = "--bass bnb --piano salamander --space room --space-wet 0.06 " + S.flags
K1, K2 = Key("Eb", "major"), Key("Gb", "major")


def up3(chs): return [("|".join(tr_chord(x, 3) for x in c.split("|"))) for c in chs]


VCH = ["Abmaj9", "Gm7", "Cm9", "Cm9", "Abmaj9", "Gm7", "Fm9", "Bb7sus4"]
PCH = ["Fm9", "Gm7", "Abmaj9", "Bb7sus4"]
CCH = ["Ebmaj9", "Gm7", "Cm9", "Bbm7|Eb9", "Abmaj9", "Abm6", "Gm7|Cm9", "Fm9|Bb7sus4"]
S.scene("しずかな店", 4, "verse", ["Abmaj9", "Abmaj9", "Gm7", "Cm9"])
S.scene("回りはじめる", 4, "intro", ["Abmaj9", "Gm7", "Fm9", "Bb7sus4"])
S.scene("待つ", 8, "verse", VCH)
S.scene("映る", 4, "pre", PCH)
S.scene("サビ1", 8, "chorus", CCH)
S.scene("となりの機械", 8, "break", ["Cm9", "Cm9", "Abmaj9", "Abmaj9", "Cm9", "Cm9", "Fm9", "Bb13"])
S.scene("待つ2", 8, "verse", VCH)
S.scene("映る2", 4, "pre", PCH)
S.scene("サビ2", 8, "chorus", CCH)
S.scene("乾く", 12, "solo", ["Ebmaj9", "Cm9", "Abm7", "Db9"] + up3(["Ebmaj9", "Cm9", "Abmaj9", "Bb13", "Ebmaj9", "Gm7", "Fm9", "Bb7sus4"]))
S.scene("最後のサビ", 16, "chorus", up3(CCH + CCH[:7] + ["Fm9|Ebmaj9"]))
S.scene("止まる", 8, "outro", up3(["Abmaj9", "Gm7", "Fm9", "Bb7sus4", "Abmaj9", "Gm7", "Ebmaj9", "Ebmaj9"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
# 1回め（BGM）を分けて測ると、ドラム −22.5 に対して ベース −35・エレピ −34 と、主役のエレピが 12dB 小さかった。volume は 0.2 で頭打ちなので、ドラムを下げ、エレピとベースは boost で上げる
S.drum_gain = {"kick": {"gainDb": -4}, "snare": {"gainDb": -5}, "hihat": {"gainDb": -5}, "crash": {"gainDb": -4}}
MOD = S.sc("乾く")[4]                                   # ここから変ト長調


def KEY(b): return K2 if b >= MOD else K1
def SCALE(b): return {(KEY(b).t + x) % 12 for x in (0, 2, 4, 5, 7, 9, 11)}


V = Voice(S, vol=0.16, delay=0.3, bright=0.0, patch="surgeFormantPulse", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(2222)

# ================= 歌（度数。oct=4 で 1 = E♭4）=================
I1, I2, I3, I4 = "x-x---x-x-x---x-", "x-----------....", "..x-x-x-x---x---", "x-----------...."
A1, A2, A3, A4 = "..x---x-x---x-x-", "x-x-----........", "x-x---x-x---x-x-", "x-------........"       # おくれて入り、行の終わりは2拍あける（返事の場所）
B1, B2 = "x-x---x---x-x-x-", "x-----x-----...."
C1p, C2p, C3p, C4p = "x-----x-x-x---x-", "x-x---------....", "x-x-x---x---x-x-", "x-----------...."; C5p = "..x-x-x---x-x-x-"       # サビ: 頭の音をのばしてから動く
IP = [I1, I2, I3, I4]; ID = ["1 1 2 3 2 1", "6,", "2 3 5 5 3", "3"]
IL = ["よるのかたすみ", "まるいまどべ"]
AP = [A1, A2, A3, A4] * 2
AD1 = ["3 3 5 3 2", "2 3", "1 2 3 5 6 5", "3", "5 5 6 5 3", "2 2", "3 2 1 6, 1 2", "1"]
AD2 = ["3 3 5 6 5", "3 2", "1 2 3 5 6 5", "3", "5 5 6 1' 6", "5 5", "3 2 1 6, 1 2", "1"]
AL1 = ["ぐるぐるまわる", "あおいうずまき", "かぞえるほどに", "よるがのびてく"]
AL2 = ["となりのどあが", "ひらいてとじる", "おなじりずむで", "まわりはじめる"]
BP = [B1, B2] * 2; BD = ["4 4 5 6 6 5", "5 5", "6 6 7 1' 1' 7", "6 5"]
BL1 = ["まどにうつるのは", "ねむたげなわたし"]; BL2 = ["ことばよりさきに", "はなうたがもれた"]
CP = [C1p, C2p, C3p, C4p, C1p, C2p, C5p, C4p]
CD = ["6 5 3 5 6", "5 3", "3 5 6 7 6 5", "5", "6 5 4 5 6", "5 4", "3 2 3 5 3 2", "1"]
CDH = ["7 6 5 6 7", "6 5", "5 6 7 7 6 7", "5", "6 5 4 5 6", "5 4", "3 2 3 5 3 2", "1"]           # 最後のサビの後半: いちばん高い音（7）をのばす
CL1 = ["うみになるまど", "なみうつしゃつは", "およいでるのは", "きのうのわたし"]
CL2 = ["うみになるまど", "ふたつならんで", "しらないひとの", "うたがきこえる"]
CL3 = ["うみになるまど", "なみがそろえば", "おなじはやさで", "よるがほどける"]
CL4 = ["うみになるまど", "あたたかいかぜ", "かわいたそでに", "あさのにおいが"]
OP = [A1, A2, A3, A4]; OD = ["3 3 2 1 2", "1 6,", "1 2 3 3 2 1", "3"]
OL = ["ぬくもりたたむ", "まだあたたかい"]


def put(name, pats, degs, phrases, bars=None):
    lines, text = song_phrases(pats, degs, phrases); bars = bars or S.sc(name); mel = [KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("しずかな店", IP, ID, IL); put("待つ", AP, AD1, AL1); put("映る", BP, BD, BL1); put("サビ1", CP, CD, CL1)
put("待つ2", AP, AD2, AL2); put("映る2", BP, BD, BL2); put("サビ2", CP, CD, CL2); put("最後のサビ", CP + CP, CD + CDH, CL3 + CL4)
put("止まる", OP, OD, OL, bars=S.sc("止まる")[4:])


# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


EP = [S.track(f"エレピ{i + 1}", "keys", volume=0.2, pan=-0.12, reverb=0.2, sustain=1.3, fx=[{"type": "tremolo", "rate": 4.2, "depth": 0.22}, {"type": "boost", "gain": 8}]) for i in range(5)]      # 5本め＝右手の節
BASS = S.track("ベース（指弾き）", "bass", volume=0.2, pan=0, duck=0.08, fx=[{"type": "boost", "gain": 7}])
GC = [S.track(f"クリーンのギター{i + 1}弦め", "guitar", amp="clean", volume=0.12, pan=0.35, reverb=0.25, chorus=0) for i in range(6)]
SPL = S.track("回る音（左の機械）", "lead", patch="surgeConvex", volume=0.09, pan=-0.5, reverb=0.2)
SPR = S.track("回る音（右の機械）", "lead", patch="surgeWoody", volume=0.09, pan=0.5, reverb=0.2)
PAD = [S.track(f"うすいパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.05, pan=0.0, reverb=0.3, sustain=2.0, fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "widen", "amount": 1.3}]) for i in range(3)]
SC = G2.Strummer(GC, S, 22); EPV = [None]; TRI = [None]


def ep_voicing(ch):
    """エレピの右手: 根音を弾かない4つの音（3度・7度・9度・5度…）。前の形にいちばん近い高さへ動く"""
    r, q, _ = parse_chord(ch); root = PC[r]; ivs = [i % 12 for i in QUAL[q] if i % 12 != 0]
    rank = {3: 0, 4: 0, 5: 0, 10: 1, 11: 1, 9: 1, 2: 2, 7: 3, 6: 3, 8: 3}
    pcs = [(root + i) % 12 for i in sorted(dict.fromkeys(ivs), key=lambda i: rank.get(i, 4))][:4]
    if len(pcs) < 4: pcs.append((root + 7) % 12 if (root + 7) % 12 not in pcs else root)
    c = sum(EPV[0]) / 4 if EPV[0] else 63.5; out = []
    for p in pcs:
        cand = [m for m in range(55, 75) if m % 12 == p and m not in out]; out.append(min(cand, key=lambda m: abs(m - c)))
    EPV[0] = sorted(out); return EPV[0]


def ep(b, pat):
    """エレピの和音（16分のマス）。小節のうしろ半分は、うしろの和音。最後の8分（マス 14）は、次の小節の和音を先に弾く（食い）"""
    c1, c2 = halves(b); v1 = list(ep_voicing(c1)); v2 = list(ep_voicing(c2)) if c2 != c1 else v1; pos = [i for i, c in enumerate(pat) if c == "x"]
    vn = list(ep_voicing(nxt(b))) if any(p >= 14 for p in pos) and nxt(b) != c2 else None
    for j in range(4): EP[j].bar(b, steps(pat, [N((vn if vn and p >= 14 else v2 if p >= 8 else v1)[j]) for p in pos]))


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SCALE(b), lo=27))


def pad(b):
    c1, c2 = halves(b); v, v2 = sorted(voice(c1, 66, 3)), sorted(voice(c2, 66, 3))
    for j in range(3): PAD[j].bar(b, f"{N(v[j])}:4" if c1 == c2 else f"{N(v[j])}:2 {N(v2[j])}:2")


def dia(m, k, b):
    sc = [p for p in range(40, 96) if p % 12 in SCALE(b)]; i = min(range(len(sc)), key=lambda j: abs(sc[j] - m)); return sc[i + k]


FIG = [(0, 1, 0), (0, -1, -2), (0, 1, 2), (2, 1, 0), (0, 2, 1), (-1, 0, 1)]


def dstop(b, slot, k, sixth=False, center=70):
    """ギターの合いの手: 2本の弦で、同じ形のまま音階を動く（上の音と、その3度下か6度下）"""
    ch = halves(b)[1 if slot >= 8 else 0]; r, third, fifth, sev, _ = G2.chord_info(ch)
    t0 = min((m for m in range(center - 6, center + 7) if m % 12 in {third if third is not None else r, fifth} and m % 12 in SCALE(b)), key=lambda m: abs(m - center), default=center)
    fig = FIG[k % len(FIG)]; Ls = [0.5, 0.5, 1.0] if slot <= 8 else [0.5, 0.5]; top = [dia(t0, f, b) for f in fig[:len(Ls)]]; lowv = [dia(m, -5 if sixth else -2, b) for m in top]
    t = S.bar_beat(b) + slot * 0.25
    SC.line(5, t, " ".join(f"{N(m)}:{L:g}" for m, L in zip(top, Ls)), strong=98, mid=88); SC.line(3 if sixth else 4, t, " ".join(f"{N(m)}:{L:g}" for m, L in zip(lowv, Ls)), strong=92, mid=82)


def gtr(b, pat, feel=8):
    c1, c2 = halves(b); a = TRI[0] = G2.triad(c1, TRI[0]); z = None
    if c2 != c1: z = TRI[0] = G2.triad(c2, a)
    SC.bar(b, pat, a, z, feel=feel)


def garp(b, pat):
    a = TRI[0] = G2.triad(halves(b)[0], TRI[0]); SC.arp(b, pat, a)


# ---- 回る音: 8分で回る短い音型。左は3つ、右は5つでひと回り（4拍子とずれつづける）。最後のサビで、どちらも4つになってそろう ----
def spin_cell(b, half, center):
    v = sorted(voice(halves(b)[half], center, 3)); return v


def spin():
    b0, bR, bF, bE = S.sc("回りはじめる")[0], S.sc("となりの機械")[0], S.sc("最後のサビ")[0], S.sc("止まる")[0]
    for tr, start, cyc, order, center in ((SPL, b0, 3, (0, 2, 1), 79), (SPR, bR, 5, (0, 1, 2, 1, 2), 72)):
        k = 0
        for e in range(start * 8, bE * 8):
            b = e // 8; half = 1 if e % 8 >= 4 else 0
            if b == bF and e % 8 == 0: k = 0
            cy, od = (4, (0, 2, 1, 2)) if b >= bF else (cyc, order)
            v = spin_cell(b, half, center); tr.at(e * 0.5, f"{N(v[od[k % cy]])}:0.5" + ("!" if k % cy == 0 else "")); k += 1
    # 止まる: 間がだんだん長くなる（8分 → 4分 → 付点4分 → 2分 …）。左右で同じ音
    t = bE * 4.0; gaps = [0.5, 0.5, 1.0, 1.0, 1.5, 2.0, 3.0, 4.0]; k = 0
    for g_ in gaps:
        b = int(t // 4)
        if b >= bE + 4: break
        v = spin_cell(b, 0, 79); w = spin_cell(b, 0, 72); L = min(g_, 1.5)
        SPL.at(t, f"{N(v[(0, 2, 1, 2)[k % 4]])}:{L:g}"); SPR.at(t, f"{N(w[(0, 2, 1, 2)[k % 4]])}:{L:g}"); t += g_; k += 1


spin()

# ---- 型 ----
EPA = ("x---------x-----", "x-----x-........", "..x-------x---x-", "x---x---........")            # 歌の場面: 行の終わりはあける
EPC = ("x-----x---x-----", "x-----x-----x---", "x---x-----x---x-", "x-----x---x-----")            # サビ
BA = ("x-----x-x-------", "115")                                                                   # 歌っている小節
BANS = [("x-------x-x-x-xx", "18653a"), ("x-----x---x-x-x-", "11356"), ("x-------x-xx--x-", "1568d")]      # ベースの返事（歌のすき間）
BCH = [("x-----x-x---x-x-", "1185d"), ("x---x-----x-x-x-", "1535a"), ("x-----x-x-----x-", "115d"), ("x-----x---x-xx-x", "11586a")]
DV = [("X.........x..x..", "....X..o....X..o", "x.x.x.x.x.x.x.x."), ("X......x..x.....", "....X.....o.X...", "x.x.x.x.x.x.xxx.")]      # 歌の場面: ゴーストを少し
DP = ("X.......x.......", "....o.......o...", "x...x...x...x...")                                                                       # 映る: 弱いスネアとハイハットだけ
DC = [("X..x......x..x..", "....X..o.o..X...", "x.x.x.x.x.x.x.x."), ("X.....x...x.....", "....X....o..X..o", "x.x.x.x.x.x.x.O.")]      # サビ
RIDE = ("D2:0.5 " * 8).strip(); RIDE2 = "D2:0.5 D2:0.5 D2:0.5 D2:0.25 D2:0.25 D2:0.5 D2:0.5 D2:0.5 D2:0.5"
LICK = ["R:2.5 Bb4:0.5 C5:0.5 Eb5:0.5", "D5:1.5 Bb4:0.5 R:2", "R:2.5 C5:0.5 Eb5:0.5 F5:0.5", "G5:1 F5:0.5 Eb5:0.5 C5:1 R:1"]            # エレピの右手の節（回りはじめる）
LICK2 = ["R:1 G5:0.5 Eb5:0.5 D5:1 Bb4:1", "R:2 C5:0.5 D5:0.5 Eb5:1", "R:1 Eb5:0.5 C5:0.5 Bb4:1 G4:1", "R:2.5 Ab4:0.5 Bb4:0.5 C5:0.5"]   # となりの機械
SOLO = ["R:1 Bb4:0.5 Db5:0.5 Eb5:1.5 Db5:0.5", "Bb4:1 Ab4:0.5 Gb4:0.5 Ab4:2", "R:0.5 Eb5:0.5 Gb5:0.5 Ab5:0.5 Gb5:1 Eb5:1", "Db5:1.5 Eb5:0.5 Db5:0.5 Bb4:0.5 Ab4:1",
        "R:1 Bb4:0.5 Db5:0.5 Gb5:1 F5:0.5 Eb5:0.5", "Db5:1 Bb4:0.5 Db5:0.5 Eb5:2", "R:0.5 Gb5:0.5 Ab5:0.5 Bb5:1 Ab5:0.5 Gb5:0.5 Eb5:0.5", "Db5:1 Ab4:1 Bb4:2"]


def drums(b, g, fill=False):
    k, s, h = g
    if fill: s = s[:12] + "X.oX"; h = h[:12] + "x..."
    D.set(b, k, s, h)


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; sung = G2.sung_slots(V, S, b)
    if n == "しずかな店":                                              # 声から始まる。2小節めにエレピの和音だけ
        if i >= 1: ep(b, "x---------------")
        if i == 3: EP[4].bar(b, "R:2.5 G4:0.5 Bb4:0.5 C5:0.5")
    elif n == "回りはじめる":                                          # 機械が動きだす: 回る音 → ハイハット → 3小節めでドラムとベースがそろう
        ep(b, EPC[i % 4]); EP[4].bar(b, LICK[i])
        if i < 2: D.set(b, "X..............." if i == 0 else "X.........x.....", "................" if i == 0 else "..............oo", "x.x.x.x.x.x.x.x."); bass(b, "x---------------", "1")
        else: drums(b, DV[i % 2], fill=last); bass(b, *BCH[i % 4])
    elif n in ("待つ", "待つ2"):
        two = n == "待つ2"; drums(b, DV[i % 2], fill=last)
        ep(b, EPA[i % 4])
        if odd and i % 4 == 1: bass(b, *BANS[(i // 4) % 3])            # 行の終わりの2拍: ベースの返事
        else: bass(b, *BA)
        if odd and i % 4 == 3: dstop(b, 8, i // 4 + (2 if two else 0), sixth=two)      # 次の行の終わりは、ギターの返事（2本の弦）
        if two:
            if odd and i % 4 == 1: dstop(b, 12, i // 4 + 4)
            if not odd: garp(b, "0---2---1---2---")
    elif n in ("映る", "映る2"):
        D.set(b, *DP); ep(b, "x-------x-------"); bass(b, "x-------x-------", "15") if not last else bass(b, "x-----x-x-x-x-x-", "11235a")
        if n == "映る2": garp(b, ("0-1-2-1-", "0-2-1-2-")[i % 2] * 2)
        if last: D.set(b, DP[0], "....o.......o.oX", "x...x...x...x.x.")
    elif n in ("サビ1", "サビ2"):
        two = n == "サビ2"; ep(b, EPC[i % 4]); bass(b, *BCH[i % 4]); pad(b)
        if two: D.set(b, DC[i % 2][0], DC[i % 2][1], "................"); D.R.bar(b, RIDE if not odd else RIDE2)
        else: drums(b, DC[i % 2])
        if last: D.S[b] = D.S[b][:12] + "X.oX"
        if i == 0 and two: crash(D, b, "C2", 4)
        gtr(b, G2.with_space(("d---d-u---u-d-u-", "d-u-d-u---u-d---")[i % 2], sung, keep=(0,)))
        if two and odd: dstop(b, 12, i // 2, sixth=i % 4 == 3)
    elif n == "となりの機械":                                          # 右にも回る音。前半はエレピの節、後半はギター（2本の弦）が返す
        drums(b, DV[i % 2], fill=last); ep(b, EPA[(i + 2) % 4] if i < 4 else EPC[i % 4]); bass(b, *(BCH[i % 4] if i % 4 != 3 else BANS[i // 4]))
        if i < 4: EP[4].bar(b, LICK2[i])
        else: dstop(b, 4 if i % 2 == 0 else 8, i, sixth=i % 2 == 1)
    elif n == "乾く":                                                  # 4小節で調を上げ、8小節のギターのソロ（クリーン）
        ep(b, EPC[i % 4]); bass(b, *BCH[i % 4]); pad(b)
        if i < 4: drums(b, DV[i % 2], fill=last); garp(b, "0---1---2---1---")
        else:
            j = i - 4; D.set(b, DC[j % 2][0], DC[j % 2][1], "................"); D.R.bar(b, RIDE if j % 2 == 0 else RIDE2)
            SC.line(5, S.bar_beat(b), SOLO[j], strong=104, mid=94)
            if j in (1, 5, 7): t0 = S.bar_beat(b) + 2; m = midi(SOLO[j].split()[-1].split(":")[0]); SC.note(4, t0, 2.0, N(dia(m, -2, b)), 80)      # のばす音に、3度下を重ねる
            if last: D.S[b] = D.S[b][:10] + "o.X.oX"
        if i == 4: crash(D, b, "C2", 4)
    elif n == "最後のサビ":                                            # 2台がそろう: 回る音が同じ周期。ライドで刻み、ギターはかき鳴らしと合いの手
        end = i == L - 1; ep(b, EPC[i % 4]); bass(b, *BCH[i % 4]); pad(b)
        D.set(b, DC[i % 2][0], DC[i % 2][1], "................"); D.R.bar(b, RIDE if not odd else RIDE2)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not end: D.S[b] = D.S[b][:10] + "o.X.oX"
        gtr(b, G2.with_space(("D---d-u---u-d-u-", "d-u-D-u---u-d-u-")[i % 2], sung, keep=(0,)))
        if odd and not end: dstop(b, 12, i // 2 + 1, sixth=i % 4 == 3)
    elif n == "止まる":                                                # 機械が止まる → 声とエレピだけ
        if i == 0: D.set(b, "X...............", "................", "x.x.x...x......."); bass(b, "x---------------", "1"); ep(b, "x---------------")
        elif i < 4: ep(b, "x---------------"); bass(b, "x---------------", "1") if i == 1 else None
        elif i < 7: ep(b, EPA[(i - 4) % 2 * 3] if i < 6 else "x---------------")
        if i == 7: [EP[j].bar(b, f"{N(m)}:4") for j, m in enumerate(ep_voicing(halves(b)[0]))]; EP[4].bar(b, "R:1 Bb5:3")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の22（21時）。ネオソウル（88・16分が少しはねる）。変ホ長調 → 変ト長調。夜ふけの待ち時間の話。"
          "声から始まる → 回る音（8分3つの周期）→ となりの機械（8分5つの周期）→ 調が上がってギターのソロ → 最後のサビで2つの周期がそろう → 回る音が止まり、声とエレピで終わる。自作")
SC.end(S.nb)
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=86, down=12, up=10, seed=22); humanize(path, "エレピ", mid=80, down=12, up=10, seed=7); humanize(path, "回る音", mid=74, down=10, up=14, seed=9)
js = load(path); print("  ギターの強さ:", SC.velocity(js), "音", SC.count)
js["swing16"] = 0.45                                                   # 16分の裏を約 57.5% に（ネオソウルの 58〜62% の手前。歌は8分の位置にしか置いていないので、ずれない）
for p in js["parts"]:
    r = p.get("role", "")
    if r == "スネア": p["pushMs"] = 14                                 # スネアは少し後ろ
    elif r.startswith("ベース"): p["pushMs"] = 8
    elif r.startswith("エレピ"): p["pushMs"] = 6
save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 10, "pre": 14, "chorus": 22, "outro": 12}, scoop=0.15, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K1), ("最後のサビ", 0, None, K2)], vol=0.34)
    voice_by_scene(path, S, {}, default="whisper")                     # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
# 1回めを測った（tools/vt3/level_curve.py。LUFS）: しずかな店 −23.9・回りはじめる −18.9・待つ −17.0・サビ1 −14.6・サビ2 −13.3・乾く −14.2・最後のサビ −13.4・止まる −21.7
#   → 声とエレピだけの始まりと終わりが小さい。最後のサビがサビ2 と同じ。エレピは鳴りつづけるので、場面のあいだの差は 1.5dB 以内で段をつける
final_gain(path, {"しずかな店": 2.5, "回りはじめる": 1.8, "待つ": 0.8, "乾く": 0.5, "最後のサビ": 1.0, "止まる": 2.5})
