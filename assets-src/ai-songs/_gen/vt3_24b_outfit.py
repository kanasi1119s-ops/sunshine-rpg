# vt3 24「明日の服がきまらない」Can't Pick Tomorrow's Outfit（仮）— ディスコ・ポップ（4分の4・116・はねない）。ヘ長調。転調なし。
# 第3弾（0時〜24時の街）の 23時。
#
# v4（2026-11-21）: ゼロから作り直し。v1〜v3 はフレンチポップ（132・ト長調・チェンバロ）で `vt3_24_outfit.py`。
#   人間の指示: 「18からは1曲ずつコンセプトとかジャンルをしっかり決めて作って行こうか。つまり作り直そう」。表と「物語 → 音」を見せて「24行こう」（2026-11-21）。
#
# コンセプト: 寝る前に、あしたの服を鏡の前で何度も着がえる。迷う時間を、ひとりだけのファッションショーに書きかえる。
# ジャンル: ディスコ・ポップ。作る前に調べた決まりごと（出どころは docs/sound/vt3-remake-plan.md の 24 v4）:
#   ・テンポ 110〜130。4つ打ちのキック、2・4拍のスネアか手拍子、裏拍のオープン・ハイハット、両手の16分のハイハット。ドラムは響きを足さない
#   ・ベースは食いこみの多い線と、根音とオクターブの行き来
#   ・「1つ入ったら1つ出る」: ギターが16分で刻むあいだ、鍵盤は長い和音。弦が弾くあいだ、ほかは引く
#
# 物語の出来事 → その時の音:
#   サビから始まる（もう30分たっている） → 前奏なし。1拍めから歌と全員
#   1着め（まず無難な服）                 → 左のギターの16分のカッティング＋オクターブのベース。エレピは長い和音
#   鏡の前（鏡を見て止まる）              → 2小節ごとに全員が1発で止まり、すき間に声と手拍子だけ
#   サビ1（ちがう、これじゃない）         → 弦の合いの手。落ち着かない和音（C7sus4）で終わる
#   ハンガーの音（次の服をさがす）        → カッティングと、右のギターのオクターブの節
#   2着め（派手な服）                     → 右のギターがオクターブ奏法の旋律に変わり、エレピが刻む（左のカッティングは休む）
#   鏡の前2・サビ2（まだちがう）          → 止まる所が増える。サビ2 はハモリ
#   床いっぱいの服（部屋じゅうに散らかる）→ 右のギター（2本の弦）と弦が、2小節ずつかけ合い
#   全部ぬいだ（ふりだしに戻る）          → ベースの旋律と声だけ
#   最後のサビ（これだ）                  → 弦が高い線を弾き、最後の小節で初めて主和音（Fmaj9）に着く
#   きまった（明かりを消す）              → 3小節ゆらして、全員が1発そろえて、ぴたっと止まる
# この曲だけの物: 「きまらない和音」。Aメロもサビも主和音（F）に一度も着かない。最後のサビの終わりで初めて着く ＝ 服がきまる。
# 歌詞: 曲名は歌わない。「服」「きまらない」「あした」も使わない。
# 声: キュート 1 種類。
from vocalo_lib import *
from lm25_lib import QUAL, PC, parse_chord
import gtr2_lib as G2
import random as _r

S = Song("24", "outfit", "明日の服がきまらない（仮）", "Can't Pick Tomorrow's Outfit", 116, 4, "F", "major", "ディスコ・ポップ（ボカロ）")
S.kit = "naked"; S.flags = "--bass bnb --piano salamander --space room --space-wet 0.06 " + S.flags
K = Key("F", "major"); SCALE = {(5 + x) % 12 for x in (0, 2, 4, 5, 7, 9, 11)}

CCH = ["Bbmaj7", "Am7", "Gm7", "C7sus4", "Bbmaj7", "Am7", "Dm7", "C7sus4"]
VCH = ["Gm7", "C9", "Gm7", "C9", "Am7", "Dm7", "Gm7", "C7sus4"]
PCH = ["Bbmaj7", "Bbmaj7", "Am7", "Am7", "Gm7", "Gm7", "C7sus4", "C7"]
S.scene("サビから始まる", 8, "chorus", CCH)
S.scene("1着め", 16, "verse", VCH * 2)
S.scene("鏡の前", 8, "pre", PCH)
S.scene("サビ1", 8, "chorus", CCH)
S.scene("ハンガーの音", 8, "break", ["Gm7", "C9", "Gm7", "C9", "Am7", "Dm7", "Gm7", "C7sus4"])
S.scene("2着め", 16, "verse", VCH * 2)
S.scene("鏡の前2", 8, "pre", PCH)
S.scene("サビ2", 8, "chorus", CCH)
S.scene("床いっぱいの服", 8, "solo", ["Dm7", "Dm7", "Bbmaj7", "Bbmaj7", "Gm7", "Gm7", "C7sus4", "C7"])
S.scene("全部ぬいだ", 8, "bridge", ["Bbmaj7", "Am7", "Gm7", "C7sus4"] * 2)
S.scene("最後のサビ", 16, "chorus", CCH + ["Bbmaj7", "Am7", "Gm7", "C7sus4", "Bbmaj7", "Am7", "Gm7|C7", "Fmaj9"])
S.scene("きまった", 6, "outro", ["Fmaj9", "Bbmaj7", "Fmaj9", "Bbmaj7", "Fmaj9", "Fmaj9"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
S.drum_gain = {"kick": {"gainDb": -4}, "snare": {"gainDb": -5}, "hihat": {"gainDb": -5}, "crash": {"gainDb": -4}}     # 22 で測った: naked のドラムは、ほかより 10dB 以上大きい

V = Voice(S, vol=0.16, delay=0.3, bright=0.0, patch="surgeHappySaws", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(2424)

# ================= 歌（度数。oct=4 で 1 = F4）=================
H1, H2 = "x-x---x-x---x---", "x-------........"                                       # あれ・でも・ない（短い・長いがまざる）
H3, H4 = "..x-x-x-x---x-x-", "x-----------...."
H5, H6 = "x-x---x-x-x---x-", "x---------......"
Va, Vb, Vc, Vd = "..x-x-x---x-x---", "x-x-----........", "x-x---x-x-x-..x-", "x-----.........."
Pa, Pb = "....x-x---x-x-x-", "x-----x---......"
Za, Zb = "x---x---x-x-x---", "x-------........"
CP = [H1, H2, H1, H2, H3, H4, H5, H6]
CD = ["3 3 5 5 6", "5", "4 4 6 6 1'", "6", "5 6 5 3 5 6", "5", "6 5 3 2 3 5", "6"]
CDE = CD[:6] + ["6 5 4 3 2 2", "1"]                                                  # 最後だけ、下がって主音で言い切る
VP_ = [Va, Vb, Vc, Vd] * 4
VD = ["2 2 4 2 4", "4 2", "2 4 5 4 2 4", "5", "3 3 5 3 5", "6 5", "4 5 6 5 4 2", "2",
      "2 2 4 5 4", "4 2", "2 4 5 6 5 4", "5", "3 5 6 5 3", "6 5", "4 5 6 1' 6 5", "6"]
PP = [Pa, Pb] * 4
PD = ["6 6 5 3 5", "6 5", "5 5 3 2 3", "5 3", "4 4 2 1 2", "4 2", "5 5 6 5 6", "6 7"]
ZP = [Za, Zb] * 4
ZD = ["3 5 6 5 3", "5", "2 4 5 4 2", "1", "3 5 6 1' 6", "5", "4 5 6 5 4", "6"]
C0 = ["あれでもない", "これでもない", "とけいのはりが", "おいこしていく"]
C1 = ["あれでもない", "これでもない", "かがみのなかで", "くびをかしげる"]
C2 = ["あれでもない", "これでもない", "はんがーたちが", "ゆれているだけ"]
C3 = ["あれでもない", "これでもない", "かがみのなかで", "えがおがひとつ", "あれじゃなくて", "これがいいな", "いちばんすきな", "いろにきめたよ"]
A1 = ["しろいしゃつなら", "まちがいないね", "でもなんとなく", "きのうとおなじ", "くろいずぼんは", "まじめすぎるし", "ひきだしのおく", "ねむるきいろを"]
A2 = ["あかいすかーと", "くるりとまわる", "すこしはでかな", "きらいじゃないな", "みどりのぼうし", "のせてみたなら", "しらないひとが", "わらいかけてる"]
B1 = ["みぎをむいても", "ひだりむいても", "なにかたりない", "なにがたりない"]
B2 = ["まえからみても", "うしろをみても", "わるくないけど", "これじゃないんだ"]
Z1 = ["ゆかのうえに", "いろのうみが", "ひろがるよる", "ふりだしだね"]


def put(name, pats, degs, phrases):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [K.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("サビから始まる", CP, CD, C0); put("1着め", VP_, VD, A1); put("鏡の前", PP, PD, B1); put("サビ1", CP, CD, C1)
put("2着め", VP_, VD, A2); put("鏡の前2", PP, PD, B2); put("サビ2", CP, CD, C2); put("全部ぬいだ", ZP, ZD, Z1); put("最後のサビ", CP + CP, CD + CDE, C3)


# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


EP = [S.track(f"エレピ{i + 1}", "keys", volume=0.2, pan=0.1, reverb=0.18, sustain=1.2, fx=[{"type": "boost", "gain": 6}]) for i in range(4)]
BASS = S.track("ベース（指弾き）", "bass", volume=0.2, pan=0, duck=0.08, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7}, {"type": "boost", "gain": 7}])
GLT = [S.track(f"左のギター{i + 1}弦め", "guitar", amp="clean", volume=0.13, pan=-0.4, reverb=0.15, chorus=0) for i in range(6)]
GRT = [S.track(f"右のギター{i + 1}弦め", "guitar", amp="clean", volume=0.13, pan=0.4, reverb=0.2, chorus=0) for i in range(6)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.12, pan=0.0, reverb=0.3, sustain=1.0, fx=[{"type": "widen", "amount": 1.4}]) for i in range(3)]
CLP = S.track("手拍子", "guitar", patch="kawaiiFx", volume=0.06, pan=0.05, reverb=0.15, modulate=False)
SL, SR = G2.Strummer(GLT, S, 24), G2.Strummer(GRT, S, 42); EPV = [None]; TL = [None]


def ep_voicing(ch):
    r, q, _ = parse_chord(ch); root = PC[r]; ivs = [i % 12 for i in QUAL[q] if i % 12 != 0]
    rank = {3: 0, 4: 0, 5: 0, 10: 1, 11: 1, 9: 1, 2: 2, 7: 3}
    pcs = [(root + i) % 12 for i in sorted(dict.fromkeys(ivs), key=lambda i: rank.get(i, 4))][:4]
    if len(pcs) < 4: pcs.append((root + 7) % 12 if (root + 7) % 12 not in pcs else root)
    c = sum(EPV[0]) / 4 if EPV[0] else 64; out = []
    for p in pcs:
        cand = [m for m in range(55, 76) if m % 12 == p and m not in out]; out.append(min(cand, key=lambda m: abs(m - c)))
    EPV[0] = sorted(out); return EPV[0]


def ep(b, pat, short=None, nv=4):
    c1, c2 = halves(b); v1 = list(ep_voicing(c1)); v2 = list(ep_voicing(c2)) if c2 != c1 else v1; pos = [i for i, c in enumerate(pat) if c == "x"]
    for j in range(4 - nv, 4): EP[j].bar(b, steps(pat, [N((v2 if p >= 8 else v1)[j]) for p in pos], **({"short": short} if short else {})))


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SCALE, lo=28))


def strs(b, pat, center=72, short=0.5):
    """弦の合いの手（短く切る）"""
    c1, c2 = halves(b); v1, v2 = sorted(voice(c1, center, 3)), sorted(voice(c2, center, 3)); pos = [i for i, c in enumerate(pat) if c == "x"]
    for j in range(3): STR[j].bar(b, steps(pat, [N((v2 if p >= 8 else v1)[j]) for p in pos], short=short))


def strline(b, top):
    """弦の高い線（のばす）: 上の声が旋律、下の2つは和音"""
    v = sorted(voice(halves(b)[0], 67, 2)); STR[0].bar(b, top); STR[1].bar(b, f"{N(v[1])}:4"); STR[2].bar(b, f"{N(v[0])}:4")


def cut(b, pat):
    """左のギター: 16分のカッティング（短く切る和音と、音程のないブラッシング）"""
    c1, c2 = halves(b); a = TL[0] = G2.triad(c1, TL[0]); z = None
    if c2 != c1: z = TL[0] = G2.triad(c2, a)
    SL.bar(b, pat, a, z, feel=16)


def dia(m, k):
    sc = [p for p in range(40, 96) if p % 12 in SCALE]; i = min(range(len(sc)), key=lambda j: abs(sc[j] - m)); return sc[i + k]


FIG = [(0, 1, 0), (0, -1, -2), (0, 1, 2), (2, 1, 0), (0, 2, 1), (-1, 0, 1), (0, 1, 2, 4), (4, 2, 1, 0)]


def dstop(b, slot, k, sixth=False, center=70):
    """右のギターの合いの手: 2本の弦で、同じ形のまま音階を動く（上の音と、その3度下か6度下）"""
    ch = halves(b)[1 if slot >= 8 else 0]; r, third, fifth, sev, _ = G2.chord_info(ch)
    t0 = min((m for m in range(center - 6, center + 7) if m % 12 in {third if third is not None else r, fifth} and m % 12 in SCALE), key=lambda m: abs(m - center), default=center)
    fig = FIG[k % len(FIG)]; n_ = (16 - slot) // 2
    Ls = {2: [0.5, 0.5], 4: [0.5, 0.5, 1.0], 8: [0.5, 1.0, 0.5, 2.0]}.get(n_, [0.5, 0.5, 1.0])[:len(fig)]
    top = [dia(t0, f) for f in fig[:len(Ls)]]; lowv = [dia(m, -5 if sixth else -2) for m in top]; t = S.bar_beat(b) + slot * 0.25
    SR.line(5, t, " ".join(f"{N(m)}:{L:g}" for m, L in zip(top, Ls)), strong=100, mid=90); SR.line(3 if sixth else 4, t, " ".join(f"{N(m)}:{L:g}" for m, L in zip(lowv, Ls)), strong=94, mid=84)


def clap(b, pat="R:1 B4:1 R:1 B4:1"): CLP.bar(b, pat)


def hit(b):
    """全員が1拍めに1発そろえて、止まる"""
    c = halves(b)[0]; r = low(c, "E1"); D.set(b, "X...............", "X...............", "................"); BASS.bar(b, f"{N(r)}:0.5 R:3.5")
    ep(b, "x...............", short=0.5); SL.bar(b, "D...............", TL[0] or G2.triad(c, None), feel=16); strs(b, "x...............")


K4 = "X...X...X...X..."; SN = "....X.......X..."
H8 = "x.O.x.O.x.O.x.O."; H16 = "xxOxx.Oxxxxxx.Ox"; H16B = "xxOxx.OxxxOxx.Ox"                 # 裏拍のオープン。スネアと同じ位置は打たない（両手で刻むため）
CUT = ("D.xUd.xUD.xxdUx.", "D.xxdUx.D.xUd.xU")
BV = [("x-x-x-x-x-x-x-x-", "18181858"), ("x-x-x-x-x-x-xx-x", "1818185da")]                    # 根音とオクターブの行き来
BC = [("x-x-x-xxx-x-x-x-", "181851818"), ("x-x-x-x-x-xxx-x-", "1818158da")]
OCT = ["R:2 D4:0.5 F4:0.5 G4:1", "R:2 G4:0.5 F4:0.5 D4:1", "R:2 E4:0.5 G4:0.5 A4:1", "R:2 A4:0.5 G4:0.5 E4:0.5 D4:0.5",
       "R:2 D4:0.5 F4:0.5 A4:1", "R:2 Bb4:0.5 A4:0.5 G4:1", "R:2 C4:0.5 E4:0.5 G4:1", "R:1.5 F4:0.5 G4:0.5 A4:0.5 C5:1"]      # 2着め: 歌の行の終わり（3〜4拍め）に、オクターブの節
HANG = ["D4:0.75 D4:0.75 F4:0.5 G4:1 R:1", "R:1 G4:0.5 A4:0.5 Bb4:0.75 A4:0.75 G4:0.5", "D4:0.75 D4:0.75 F4:0.5 G4:1 R:1", "R:1 E4:0.5 G4:0.5 A4:1 C5:1",
        "E4:0.75 E4:0.75 G4:0.5 A4:1 R:1", "R:1 A4:0.5 C5:0.5 D5:0.75 C5:0.75 A4:0.5", "D4:0.75 D4:0.75 F4:0.5 G4:1 R:1", "R:1 C4:0.5 D4:0.5 E4:0.5 G4:0.5 Bb4:1"]
BMEL = ["Bb1:1 D2:0.5 F2:0.5 A2:1 G2:0.5 F2:0.5", "A1:1 C2:0.5 E2:0.5 G2:1.5 E2:0.5", "G1:1 Bb1:0.5 D2:0.5 F2:1 D2:0.5 Bb1:0.5", "C2:1.5 G1:0.5 C2:0.5 D2:0.5 E2:0.5 G2:0.5",
        "Bb1:1 F2:0.5 A2:0.5 D3:1 C3:0.5 A2:0.5", "A1:1 E2:0.5 G2:0.5 C3:1.5 A2:0.5", "G1:1 D2:0.5 F2:0.5 Bb2:1 A2:0.5 G2:0.5", "C2:1 C2:0.5 D2:0.5 E2:0.5 G2:0.5 Bb2:0.5 C3:0.5"]
TOP = ["D6:3 C6:1", "C6:2 E6:2", "D6:2 Bb5:2", "C6:3 D6:1", "F6:3 D6:1", "E6:2 C6:2", "D6:2 A5:2", "G5:2 Bb5:1 C6:1",
       "D6:3 C6:1", "C6:2 E6:2", "D6:2 Bb5:2", "C6:3 D6:1", "F6:3 D6:1", "E6:2 G6:2", "F6:2 E6:2", "F6:4"]                 # 最後のサビの弦の高い線

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; sung = G2.sung_slots(V, S, b)
    if n in ("サビから始まる", "サビ1", "サビ2", "最後のサビ"):
        first, two, fin = n == "サビから始まる", n == "サビ2", n == "最後のサビ"; end = fin and last
        D.set(b, K4, SN if not (i % 8 == 7 and not end) else "....X.......X.xX", H16 if not odd else H16B); clap(b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        bass(b, *BC[i % 2]); ep(b, "x---------x-----" if not odd else "x-----x---------")       # ギターが刻むあいだ、エレピは長い和音
        cut(b, G2.with_space(CUT[i % 2], sung, keep=(0, 8)))
        if fin:
            strline(b, TOP[i])
            if not odd: SR.bar(b, G2.with_space("D---d-U---U-d-U-", sung, keep=(0,)), G2.low_shape(halves(b)[0]), feel=8)      # 最後のサビだけ、右のギターも和音をかき鳴らす
        elif odd: strs(b, "........x..x..x." if i % 4 == 1 else "..........x.x.xx")              # 歌の行の終わりに、弦の合いの手
        if (two or fin) and odd and not end: dstop(b, 12, i // 2)
    elif n in ("1着め", "2着め"):
        two = n == "2着め"; late = i >= 8
        D.set(b, K4, SN if not (last or i == 7) else "....X.......X.xX", H8 if not late else H16); bass(b, *BV[i % 2])
        if not two:                                                                              # 1着め: 左のカッティング。エレピは長い和音。後半から手拍子
            cut(b, G2.with_space(CUT[i % 2], sung, keep=(0, 8))); ep(b, "x---------------")
            if late: clap(b)
        else:                                                                                    # 2着め: 右のギターがオクターブの旋律。エレピが刻む。左は休む
            ep(b, "x.....x...x....." if not odd else "..x.....x...x...", short=0.5, nv=2); clap(b)      # 1回め、4つの音で5回刻むと 2着め（−12.0）がサビ1（−13.4）より大きくなった → 上の2つの音で3回に
            if odd: G2.octaves(SR, 2, 4, S, b, OCT[(i // 2) % 8])
            elif late: cut(b, "D...............")
    elif n in ("鏡の前", "鏡の前2"):
        two = n == "鏡の前2"
        if not odd or (two and i >= 4):                                                          # 全員が1発で止まり、すき間は声と手拍子だけ（2回めは後半ずっと止まる）
            hit(b); clap(b, "R:1 B4:1 R:1 B4:1" if not odd else "R:1 B4:0.5 B4:0.5 R:1 B4:1")
        else:
            D.set(b, K4, SN, H8); bass(b, *BV[1]); ep(b, "x---------------"); cut(b, CUT[1]); clap(b)
        if last: D.set(b, "X...........X.X.", "X.......x.x.XXXX", "................")
    elif n == "ハンガーの音":                                                                   # カッティングと、右のギターのオクターブの節
        D.set(b, K4, SN if not last else "....X.......XXXX", H16 if not odd else H16B); bass(b, *BC[i % 2]); ep(b, "x---------------"); cut(b, CUT[i % 2]); clap(b)
        G2.octaves(SR, 2, 4, S, b, HANG[i])
    elif n == "床いっぱいの服":                                                                 # 右のギター（2本の弦）と弦が、2小節ずつかけ合い
        D.set(b, K4, SN if not last else "....X...X.X.XXXX", H16 if not odd else H16B); bass(b, *BC[i % 2]); ep(b, "x---------x-----"); cut(b, CUT[i % 2]); clap(b)
        if (i // 2) % 2 == 0: dstop(b, 0 if not odd else 8, 6 + i % 2 if not odd else i, sixth=odd)
        else: strs(b, "x..x..x...x.x..." if not odd else "x.x...x..x..x.xx", center=74)
        if i == 0: crash(D, b, "C2", 4)
    elif n == "全部ぬいだ":                                                                     # ベースの旋律と声だけ（後半、弱いハイハットと手拍子）
        BASS.bar(b, BMEL[i])
        if i >= 4: D.set(b, "................", "................", "x...x...x...x..."); clap(b, "R:1 B4:1 R:1 B4:1")
        if last: D.set(b, "............X.X.", "........x.x.XXXX", "x...x...........")
    elif n == "きまった":                                                                       # 3小節ゆらして、全員が1発そろえて止まる
        if i < L - 1:
            D.set(b, K4, SN if i < L - 2 else "....X.......X.XX", H16); clap(b); bass(b, *BC[i % 2]); ep(b, "x---------x-----"); cut(b, CUT[i % 2])
            if i == 0: crash(D, b, "C2", 4)
            if odd: dstop(b, 8, 3 + i)
            strs(b, "........x..x..x.")
        else:
            hit(b); crash(D, b, "C2", 4); CLP.bar(b, "B4:1 R:3")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の24（23時）。ディスコ・ポップ（116・ヘ長調）。寝る前に、鏡の前で何度も着がえる話。"
          "前奏なしでサビから始まる → 着がえるたびにギターの弾き方が変わる（16分のカッティング → オクターブ奏法 → 2本の弦）→ 鏡の前で全員が止まる → "
          "ベースの旋律と声だけ → 最後のサビの終わりで初めて主和音に着く → 1発そろえて止まる。自作")
SL.end(S.nb); SR.end(S.nb)
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=92, down=12, up=10, seed=24); humanize(path, "エレピ", mid=82, down=12, up=10, seed=7); humanize(path, "ストリングス", mid=86, down=10, up=12, seed=3)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 8, "pre": 10, "chorus": 20, "bridge": 10}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K), ("最後のサビ", 0, None, K)], vol=0.34)
    voice_by_scene(path, S, {}, default="cute")                          # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
# 1回めを測った（LUFS）: サビから始まる −15.1・サビ1 −13.3・サビ2 −12.2・最後のサビ −12.8（始まりが小さく、最後がサビ2 より小さい）
final_gain(path, {"サビから始まる": 1.5, "1着め": 1.0, "鏡の前": 0.5, "最後のサビ": 1.0, "きまった": 1.0})
