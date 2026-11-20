# vt3 23「くらげの夜間飛行」Jellyfish Night Flight（仮）— テクノポップ（4分の4・126・はねない）。イのリディアン（ホ長調の音階で、中心がイ）。転調なし。
# 第3弾（0時〜24時の街）の 22時。
#
# v3（2026-11-20）: ゼロから作り直し。v1〜v2 はポストロック（104・ニ長調・水族館の話）で `vt3_23_jellyfish.py`。
#   人間の指示: 「18からは1曲ずつコンセプトとかジャンルをしっかり決めて作って行こうか。つまり作り直そう」。はじめリキッド・ドラムンベースの案を出し、
#   「ジャンル、テクノポップで良いと思う」→ 表を直して見せ、「良い」（2026-11-20）。
#
# コンセプト: 眠れない夜。天井が水面に見えてきて、体が透きとおって浮き、街の上をただよう。眠れない時間を、空をただよう時間に書きかえる。
# ジャンル: テクノポップ。作る前に調べた決まりごと（出どころは docs/sound/vt3-remake-plan.md の 23 v3）:
#   ・4つ打ちのキック、ドラムマシン、くり返す音型（シーケンス）。16分で進むシンセベース、同じ音をオクターブで行き来する型
#   ・パッドが全体をつなぐ。キックに合わせてパッドとベースを引っこめる（ダッキング）
#   ・おぼえやすい音型を1つ決め、Aメロは音を少なくし、サビで開く
#
# 物語の出来事 → その時の音:
#   ねむれない部屋（目がさえている） → 壁のむこうで鳴っているような、こもったキックだけで始まる。5小節めから低い声
#   浮きあがる（体が軽くなる）       → キックのこもりが3段で晴れ、シンセベースが4分 → 8分 → 16分 → オクターブへとせり上がる
#   街の上（屋根の上をただよう）     → キック＋16分のシンセベース＋裏のハイハット。後半からクラップと短い和音
#   雲の中（何も見えなくなる）       → キックが消える。息をするパッドと声と、遠いプラックだけ
#   サビ1（雲をぬける）              → 全部が戻る。プラックが和音を駆け上がる（街の灯）。歌は長い音で浮かぶ
#   風に流される（風に運ばれる）     → ベースの音型が旋律に変わり、スネアの連打で次へ
#   街の上2・サビ2（もっと遠くへ）   → ガラスのエレピの音型が1つ増え、ハモリが入る
#   いちばん高い所（空気がうすい）   → 声とパッドだけ（4小節）→ スネアがだんだん細かくなって最後のサビへ
#   最後のサビ（街ぜんぶが光る）     → ハイハットが16分になり、プラックが左右で追いかけ合う
#   おりる（朝が近づき、布団へ戻る） → キックがまた3段でこもっていき、始まりと同じキックだけになって終わる
# この曲だけの物: 息をするパッド（2小節でふくらんで縮む。4つの声が1拍ずつおくれて入り、1拍ずつ先に消える）。機械の音型の中で、これだけが生き物のように動く。
# 歌詞: 曲名は歌わない。「くらげ」「飛行」「飛ぶ」も使わない。
# 声: クリア 1 種類。
from vocalo_lib import *

S = Song("23", "jellyfish", "くらげの夜間飛行（仮）", "Jellyfish Night Flight", 126, 4, "E", "major", "テクノポップ（ボカロ）")
S.kit = "electro"; S.flags = S.flags + " --space hall --space-wet 0.1"
K = Key("E", "major")          # 音階はホ長調。中心はイ（4番め）＝イのリディアン。oct 4 で 1 = E4、4 = A4、7 = D#5
SCALE = {(4 + x) % 12 for x in (0, 2, 4, 5, 7, 9, 11)}

VCH = ["Amaj7", "B/A", "C#m7", "B", "Amaj7", "B/A", "F#m7", "G#m7"]
PCH = ["F#m7", "F#m7", "G#m7", "G#m7", "Amaj7", "Amaj7", "B", "B"]
# 1回めのサビ（A・B・G#m・C#m…）は、よくある進み方（4→5→3→6）で、前の曲と和音の進み方が 74% 重なった → 4→5→6→2 と 2→5→3→6 に変えた
CCH = ["Amaj7", "B", "C#m7", "F#m7", "Amaj7", "B", "C#m7", "E", "F#m7", "B", "G#m7", "C#m7", "F#m7", "G#m7", "Amaj7", "B"]
S.scene("ねむれない部屋", 8, "verse", ["Amaj7"] * 8)
S.scene("浮きあがる", 8, "intro", ["Amaj7", "Amaj7", "B/A", "B/A", "Amaj7", "Amaj7", "B/A", "B"])
S.scene("街の上", 16, "verse", VCH * 2)
S.scene("雲の中", 8, "pre", PCH)
S.scene("サビ1", 16, "chorus", CCH)
S.scene("風に流される", 8, "break", ["C#m7", "C#m7", "Amaj7", "Amaj7", "F#m7", "F#m7", "B", "B"])
S.scene("街の上2", 8, "verse", VCH)
S.scene("雲の中2", 8, "pre", PCH)
S.scene("サビ2", 16, "chorus", CCH)
S.scene("いちばん高い所", 8, "bridge", ["Amaj7", "Amaj7", "B/A", "B/A", "F#m7", "G#m7", "Amaj7", "B"])
S.scene("最後のサビ", 16, "chorus", CCH[:12] + ["F#m7", "G#m7", "Amaj7", "Amaj7"])
S.scene("おりる", 12, "outro", ["Amaj7", "B/A"] * 4 + ["Amaj7"] * 4)
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35

PING = [{"type": "pingpong", "beats": 0.75, "mix": 0.22, "feedback": 0.32}]


def lp(f): return [{"type": "filter", "kind": "highpass", "freq": 35, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": f, "q": 0.7}]


V = Voice(S, vol=0.16, delay=0.5, bright=0.0, patch="surgeFriendly", low=False)
KM = [S.track(f"壁のむこうのキック（{f}Hz より上を切る）", "kick", volume=0.2, pan=0, fx=lp(f)) for f in (220, 520, 1300)]
FMB = S.track("16分のシンセベース", "bass", patch="surgeBassAnalogBassImaged", volume=0.11, pan=0, duck=0.3)
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.034, pan=0, duck=0.5, fx=[{"type": "filter", "kind": "highpass", "freq": 32, "q": 0.7}])
PAD = [S.track(f"息をするパッド{i + 1}", "lead", patch="surgePadClassicStrings", volume=0.16, pan=0.0, reverb=0.45, duck=0.3, fx=[{"type": "widen", "amount": 1.4}]) for i in range(4)]
STAB = [S.track(f"短い和音のシンセ{i + 1}", "lead", patch="surgeChordReset", volume=0.1, pan=0.0, reverb=0.2, duck=0.3,
                fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "widen", "amount": 1.5}]) for i in range(3)]
PL = S.track("プラック（左・街の灯）", "lead", patch="kfbSquarePluck", volume=0.05, pan=-0.4, reverb=0.3, fx=PING)
PR = S.track("プラック（右・街の灯）", "lead", patch="kfbSquarePluck", volume=0.05, pan=0.4, reverb=0.3, fx=PING)
FAR = S.track("遠いプラック", "lead", patch="kfbSquarePluck", volume=0.045, pan=0.2, reverb=0.6, fx=PING)
GEP = S.track("ガラスのエレピの音型", "lead", patch="surgeKeysDxTonez", volume=0.04, pan=0.25, reverb=0.25)
CLP = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.05, pan=-0.05, reverb=0.1, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = E4。「,」は下のオクターブ）=================
LO5 = ["R:1 4,:0.5 6,:0.5 1:1.5 7,:0.5", "6,:2 R:2"]                   # 低い声の5音
LO6 = ["R:1 4,:0.5 6,:0.5 1:0.5 2:1 3:0.5", "2:3 R:1"]                 # 低い声の6音
VA = ["R:1.5 4:0.5 6:1.5 5:0.5", "3:1.5 5:0.5 4:1 R:1", "R:0.5 3:0.5 6:1 5:0.5 7:1.5", "5:3 R:1",
      "R:1.5 4:0.5 6:1.5 1':0.5", "7:1.5 5:0.5 6:1 R:1", "R:0.5 2:0.5 6:1 4:0.5 5:1.5", "3:3 R:1"]
VB = ["R:1.5 6:0.5 1':1.5 7:0.5", "5:1.5 6:0.5 4:1 R:1", "R:0.5 3:0.5 5:1 6:0.5 5:1.5", "7:3 R:1",
      "R:1.5 4:0.5 6:1.5 1':0.5", "2':1.5 1':0.5 6:1 R:1", "R:0.5 6:0.5 5:1 3:0.5 2:1.5", "3:3 R:1"]
VP = ["R:1.5 2:1 4:0.5 6:1", "5:2.5 4:0.5 R:1", "R:1.5 3:1 5:0.5 7:1", "6:2.5 5:0.5 R:1", "R:1.5 4:1 6:0.5 1':1", "7:2.5 6:0.5 R:1", "R:1.5 5:1 6:0.5 7:1", "2':2.5 7:0.5 R:1"]
VC = ["1:2.5 7:0.5 6:1", "5:0.5 6:1 7:0.5 5:1 R:1", "R:1 3:1.5 5:0.5 6:0.5 7:0.5", "6:3 R:1",
      "1:2.5 1':0.5 7:1", "6:0.5 5:1 6:0.5 7:1 R:1", "R:1 5:1.5 6:0.5 7:0.5 1':0.5", "1':3 R:1",
      "4:2.5 1':0.5 7:1", "6:0.5 6:1 5:0.5 7:1 R:1", "R:1 3:1.5 5:0.5 6:0.5 7:0.5", "1':3 R:1",
      "2:2.5 6:0.5 5:1", "3:0.5 5:1 6:0.5 7:1 R:1", "R:1 6:1.5 7:0.5 1':0.5 7:0.5", "6:3 R:1"]
VCE = VC[:15] + ["1':3 R:1"]                                           # 最後のサビ: 終わりはイの和音の5度（E）でとまる
VH = ["R:1.5 4:1 6:0.5 1':1", "7:2.5 6:0.5 R:1", "R:1.5 5:1 6:0.5 7:1", "2':2.5 7:0.5 R:1"]


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [K.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("ねむれない部屋", LO5 + LO6, "てんじょうが/みなもになる", bars=S.sc("ねむれない部屋")[4:])
put("街の上", VA + VB, "ゆびさきから/すけていく/おもさぬいで/うきあがる/やねのうえを/ただよえば/まちのあかり/ふかいそこ")
put("雲の中", VP, "しろいやみ/こえもない/むねのおと/だけがする")
put("サビ1", VC, "とうめいなかさ/ひらいたら/よるがわたしを/はこんでく/ねむらなくても/いいんだよ/ゆめよりとおく/いけるから")
put("街の上2", VB, "かぜのうわさ/きいている/だれもいない/そらのみち")
put("雲の中2", VP, "なにもない/うえもした/めをとじて/のぼりゆく")
put("サビ2", VC, "とうめいなかさ/ゆらしたら/ひかりのつぶが/ついてくる/ひとりのよるも/わるくない/ゆめよりとおく/いけるから")
put("いちばん高い所", VH, "おとがない/ほしがある", bars=S.sc("いちばん高い所")[:4])
put("最後のサビ", VCE, "とうめいなかさ/ふくらんで/まちじゅうのひが/またたいた/ねむらなくても/いいんだよ/あさがくるまで/ういている")
put("おりる", LO6 + LO5, "まぶたのうら/あさのいろ", bars=S.sc("おりる")[:4])


# ================= 伴奏 =================
def root_of(b): return S.chords[b].split("/")[-1] if "/" in S.chords[b] else S.chords[b]
def chord_of(b): return S.chords[b].split("/")[0]
def rlow(b): return low(root_of(b), "E1")


def seq(b, pat):
    """16分のシンセベース。r＝根音、R＝1オクターブ上、5＝5度、.＝休み、-＝前の音をのばす"""
    r = rlow(b); out = []; i = 0
    while i < 16:
        c = pat[i]; L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if c == "." else f"{N(r + {'r': 0, 'R': 12, '5': 7}[c])}:{L * 0.25:g}"); i += L
    FMB.bar(b, " ".join(out))


def sub(b): SUB.bar(b, f"{N(rlow(b))}:4")


def breathe(b, i):
    """息をするパッド: 2小節でひと息。4つの声が1拍ずつおくれて入り、1拍ずつ先に消える（低い声がいちばん長い）"""
    v = sorted(voice(chord_of(b), 64, 3)); v = v + [v[0] + 12]
    for j in range(4):
        if j == 0: PAD[j].bar(b, f"{N(v[j])}:4")
        elif i % 2 == 0: PAD[j].bar(b, f"R:{j} {N(v[j])}:{4 - j}")
        else: PAD[j].bar(b, f"{N(v[j])}:{4 - j} R:{j}")


def stab(b, pat):
    v = sorted(voice(chord_of(b), 67, 3))
    for j in range(3): STAB[j].bar(b, steps(pat, [N(v[j])] * pat.count("x"), short=0.6))


def run(tr, b, up=True, start=0.0, center=72):
    """プラックが和音を16分で駆け上がり（下り）、最後の音がやまびこで残る"""
    v = sorted(voice(chord_of(b), center, 3)); seqn = [v[0], v[1], v[2], v[0] + 12, v[1] + 12, v[2] + 12, v[0] + 24]
    if not up: seqn = seqn[::-1]
    rest = 4 - start - 1.5
    tr.bar(b, (f"R:{start:g} " if start else "") + " ".join(f"{N(m)}:0.25" for m in seqn[:6]) + f" {N(seqn[6])}:{rest:g}")


def far(b, i):
    v = sorted(voice(chord_of(b), 84, 3)); FAR.bar(b, f"R:2 {N(v[(i * 2) % 3])}:2" if i % 2 == 0 else f"R:3 {N(v[(i + 1) % 3])}:1")


def gep(b, i):
    v = sorted(voice(chord_of(b), 76, 3)); o = [(0, 2, 1, 2, 0, 2, 1, 2), (0, 1, 2, 1, 0, 2, 1, 0)][i % 2]
    GEP.bar(b, " ".join(f"{N(v[k])}:0.5" for k in o))


def clap(b, extra=False): CLP.bar(b, "R:1 B4:1 R:1 B4:1" if not extra else "R:1 B4:1 R:1 B4:0.5 B4:0.5")


def muffled(b, k, pat="x:1 x:1 x:1 x:1"): KM[k].bar(b, pat)


K4 = "X...X...X...X..."
SB = {  # シンセベースの型
    "v1": ("r.rR.r.rr.rR.rR.", "r.rR.rr.r.rR.r5R"), "v2": ("r.rRr.rRr.rRr.5R", "rrrR.rrRr.rRrR5R"),
    "c": ("rrRrrrRrrrRrrRRr", "rrRrrRrrrrRrr5RR"),
}
BMEL = ["C#2:0.75 C#2:0.75 E2:0.5 G#2:1 F#2:0.5 E2:0.5", "C#2:0.75 B1:0.75 C#2:0.5 E2:0.5 F#2:0.5 G#2:1", "A1:0.75 A1:0.75 C#2:0.5 E2:1 D#2:0.5 C#2:0.5", "A1:0.75 B1:0.75 C#2:0.5 E2:0.5 G#2:0.5 A2:1",
        "F#1:0.75 F#1:0.75 A1:0.5 C#2:1 B1:0.5 A1:0.5", "F#1:0.75 G#1:0.75 A1:0.5 C#2:0.5 E2:0.5 F#2:1", "B1:0.75 B1:0.75 D#2:0.5 F#2:1 E2:0.5 D#2:0.5", "B1:0.5 C#2:0.5 D#2:0.5 F#2:0.5 B2:2"]

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "ねむれない部屋":                                            # こもったキックだけ → 5小節めから低い声と、息をするパッド
        muffled(b, 0)
        if i >= 4: breathe(b, i)
    elif n == "浮きあがる":                                              # こもりが3段で晴れ、ベースがせり上がる
        breathe(b, i)
        if i < 2: muffled(b, 0); seq(b, "r---........r---")
        elif i < 4: muffled(b, 1); seq(b, "r-..r-..r-..r-R-")
        elif i < 6: muffled(b, 2); seq(b, "r.r.r.r.r.rRr.r."); D.set(b, "................", "................", "..x...x...x...x.")
        else:
            D.set(b, K4, "................" if not last else "..........x.x.xx", "..x...x...x...x."); seq(b, SB["v2"][i % 2] if not last else "r.rRr.rR5.5RR5RR")
            if last: run(PL, b, start=2.0)
    elif n in ("街の上", "街の上2"):
        two = n == "街の上2"; late = two or i >= 8
        D.set(b, K4, "................" if not (last and late) else "............x.xx", "..x...x...x...x." if not late else "o.x.o.x.o.x.o.x.")
        seq(b, SB["v2" if late else "v1"][i % 2]); breathe(b, i)
        if late: clap(b, extra=i % 4 == 3); stab(b, "x..x..x...x..x.." if not odd else "..x..x..x...x...")
        if two: gep(b, i)
    elif n in ("雲の中", "雲の中2"):                                     # キックが消える
        breathe(b, i); far(b, i)
        if i >= 6: D.set(b, "................", "................" if not last else "....x...x.x.xxxx", "..x...x...x...x.")
        if last: run(PR, b, start=2.0, center=76)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        fin = n == "最後のサビ"; two = n == "サビ2"
        hat = "x.xx..xxx.xx..xx" if fin else ("o.x.o.x.o.x.o.x." if not two else "x.x.x.x.x.x.x.x.")
        D.set(b, K4, "....X.......X..." if not (i % 8 == 7) else "....X.......X.xx", hat); clap(b, extra=i % 8 == 7)
        seq(b, SB["c"][i % 2]); sub(b); breathe(b, i); stab(b, "x.....x..x....x." if not odd else "x..x.....x..x...")
        if i % 8 == 0: crash(D, b, "C2", 4)
        if fin:                                                          # 左右で追いかけ合う: 左が上り、右が半拍おくれて下り
            run(PL, b, up=True) if not odd else run(PR, b, up=False, start=0.5, center=76)
            if i % 4 == 2: gep(b, i)
        elif not odd: run(PL if (i // 2) % 2 == 0 or not two else PR, b, up=True, center=72 if not two else 74)
        if two and odd: gep(b, i)
    elif n == "風に流される":                                            # ベースの音型が旋律に変わる。スネアの連打で次へ
        FMB.bar(b, BMEL[i]); breathe(b, i)
        D.set(b, "X.....X...X....." if not odd else "X.....X.....X...", "....X.......X..." if i < 6 else ("....X...X.X.X.X." if i == 6 else "X.X.X.XXXXXXXXXX"), "o.x.o.x.o.x.o.x.")
        if i % 2 == 0: run(PR, b, up=False, start=1.0, center=76)
        if i >= 4: stab(b, "x..x..x...x..x..")
    elif n == "いちばん高い所":                                          # 声とパッドだけ → スネアが細かくなって最後のサビへ
        breathe(b, i)
        if i >= 4:
            D.set(b, "................" if i < 6 else K4, ("....x.......x...", "x...x...x...x...", "x.x.x.x.x.x.x.x.", "x.x.xxxxxxxxXXXX")[i - 4], "................"); seq(b, ("r---............", "r---....r---....", "r-r-r-r-r-r-r-r-", "rrrrrrrrRRRRRRRR")[i - 4])
            if i == 7: run(PL, b, start=2.0)
    elif n == "おりる":                                                  # キックがまたこもっていく → キックだけで終わる
        if i < 4: D.set(b, K4, "................", "..x...x...x...x."); seq(b, SB["v1"][i % 2]); breathe(b, i)
        elif i < 6: muffled(b, 2); seq(b, "r-..r-..r-..r-.."); breathe(b, i)
        elif i < 8: muffled(b, 1); seq(b, "r---........r---"); breathe(b, i)
        elif i < 11: muffled(b, 0)
        else: muffled(b, 0, "x:1 x:1 x:1 R:1")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の23（22時）。テクノポップ（126・イのリディアン）。眠れない夜に、体が透きとおって街の上をただよう話。"
          "こもったキックだけで始まる → こもりが晴れてシンセベースがせり上がる → 雲の中でキックが消える → サビでプラックが和音を駆け上がる → "
          "声とパッドだけの4小節 → 最後のサビでプラックが左右で追いかけ合う → キックがまたこもって終わる。息をするパッド（2小節でふくらんで縮む）がずっと鳴る。自作")
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "16分のシンセベース", mid=92, down=14, up=10, seed=23); humanize(path, "プラック", mid=84, down=10, up=14, seed=5)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 10, "pre": 12, "chorus": 24, "bridge": 10, "outro": 10}, scoop=0.12, slash=0.4, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K), ("最後のサビ", 0, None, K)], vol=0.34)
    voice_by_scene(path, S, {}, default="clear")                        # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
# 1回めを測った（LUFS）: サビ1 −12.3・サビ2 −11.3・最後のサビ −11.8（最後がサビ2 より小さい）。街の上2 は歌が伴奏より −8.2dB（エレピの音型が大きい → 0.06 を 0.04 に）
final_gain(path, {"最後のサビ": 1.0, "おりる": 0.5})
