# KFB 03B「ガラスごしブーケ」Bouquet Behind the Glass（仮）— Kawaii future bass × ダンス × ロック。4分の4・144・ホ長調（1場面だけト長調）。173小節・約4分48秒。
#
# 2026-11-24 人間「次作ろうか」→ 高嶺の花の恋の歌 3曲のうち B（ショーケースの花）。A（kfb_03a_madogiwa.py）とは別の曲として、旋律・和音・ノリ・音色を新しく書いた。
#   骨組みはくじ（tools/vt3/form_dice.py --skeleton 11672 285・1回めをそのまま）: 始まり方・場面の並び・小節数・旋律の句の形・終わり方・テンポ 144。
#   人が決めた所: 調（ホ長調。「その人の言葉」だけ短3度上のト長調）、和音（サビは I → II/I → IV → iv6 → iii → VI7 → II7 → V。2つめの和音が明るく浮く）、
#     ノリ（キックが食いこむ形。4つ打ちはドロップだけ）、低音（シンセの低いベースだけ）、ギター（サビ・ドロップ・立ち上げだけ。8分のかき鳴らし）。
#   この曲だけのもの: ガラスを「コン、コン」とたたくベルの2音。2人のあいだにガラスがある間だけ鳴り、その人が声をかけた所（サビ2の頭）で割れる音がして、あとは鳴らない。
# 物語（高嶺の花＝見えていても手が届かない、あこがれの人）: お店のいちばん高い棚の花のような人。「見るだけ」と決めて毎日通う。言いわけが増えるほど好きが大きくなる。
#   ある日、その人のほうから声をかけてくる。「だれも来ないのと、上から見ていた。君を待ちながら」。届かないのは花ではなくて、伸ばさずにいた自分の手だった。
#   最後は「またあした来るね。今度は——」で、言いかけたまま終わる。
# 歌詞: 曲名の言葉（ガラス・ブーケ）は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *
import gtr2_lib as G2

S = Song("30", "glass", "ガラスごしブーケ（仮）", "Bouquet Behind the Glass", 144, 4, "E", "major", "カワイイ・フューチャーベース×ダンス×ロック（ボカロ）")
S.kit = "crocell-punch"; S.flags = S.flags + " --space room --space-wet 0.08"
KE, KG = Key("E", "major"), Key("G", "major")
CM = ["E", "F#/E", "Amaj7", "Am6", "G#m7", "C#7", "F#7", "B7sus4"]                # サビ
CR = ["C#m7", "A#m7b5", "Amaj7", "G#7", "C#m7", "F#7", "Amaj7", "B7sus4"]         # サビ（別の和音）: 同じ旋律に別の和音
UP = ["A", "A", "B", "B", "C", "C", "D", "D"]                                     # 立ち上げ: IV → V → ♭VI → ♭VII
SC = []


def scene(name, n, kind, chs, key=KE):
    assert len(chs) == n, (name, n, len(chs)); SC.append((name, key)); S.scene(name, n, kind, chs)


scene("合図", 2, "break", ["E", "B7sus4"])
scene("高い棚", 10, "bridge", ["Amaj7", "Amaj7", "G#m7", "G#m7", "F#m7", "F#m7", "Emaj7", "Emaj7", "A/B", "A/B"])
scene("見るだけ", 6, "verse", ["C#m7", "C#m7/B", "A#m7b5", "A", "G#m7", "B7sus4"])
scene("言いわけ", 12, "verse", ["C#m7", "B", "A", "G#7"] * 2 + ["C#m7", "B", "A", "B7sus4"])
scene("目が合う", 4, "bridge", ["Amaj7", "Am6", "E/G#", "B7sus4"])
scene("ドロップ1", 10, "break", CM + ["A/B", "B7sus4"])
scene("サビ0", 8, "chorus", CR)
scene("サビ1", 16, "chorus", CM + CM)
scene("立ち上げ1", 8, "pre", UP)
scene("サビ2", 8, "chorus", CM)
scene("声", 12, "verse", ["E", "G#m7/D#", "C#m7", "A", "B/A", "G#m7", "F#m7", "G#m7", "A", "A/B", "B", "B7"])
scene("その人の言葉", 10, "bridge", ["Cmaj7", "D/C", "Bm7", "Em7", "A7", "D", "Cmaj7", "Cm6", "G/B", "B7"], KG)
scene("この手", 8, "verse", ["E", "G#m7/D#", "C#m7", "B", "A", "G#m7", "F#m7", "B7sus4"])
scene("サビ3", 8, "chorus", CR)
scene("ソロ", 4, "solo", ["C#m7", "A", "E/G#", "B"])
scene("ドロップ2", 16, "break", CM + CR)
scene("立ち上げ2", 8, "pre", UP)
scene("にせの立ち上げ", 10, "pre", UP + ["Amaj7", "Am6"])
scene("サビ4", 8, "chorus", CM)
scene("またあした", 5, "outro", ["Amaj7", "B/A", "G#m7", "C#m7", "F#m7"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3
KEYOF = dict(SC)

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
SUB = S.track("シンセの低いベース", "bass", patch="kfbSub", volume=0.066, pan=0, duck=0.12)
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **{**rock_gtr_spec(0.24, -0.6, tone="marshall-mid", drive=0.18), "sustain": 3.0, "release": 0.8}) for i in range(6)]      # v3: 歪みを浅く（0.4 → 0.18）、音が次の一打まで残るように（のび 1.3 → 3.0 秒）
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **{**rock_gtr_spec(0.23, 0.6, tone="marshall-mid", drive=0.15), "sustain": 3.0, "release": 0.8}) for i in range(6)]
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.14, 0.1))
# v4（2026-11-24）: 聞きくらべ（tools/vt3/gtr_tone_ab.py）で、人間が「1 と 3 が使える」と選んだ。1＝浅い歪みで和音と同じリズム、3＝つやのあるロックの音（glossy-jrock）で8分のかき鳴らし。
#   浅い歪みは同じ音量設定でも約 13dB 小さく出ると分かったので、1 の音量を上げた（0.095 → 0.24）。3 はサビとドロップ、1 はそのほかのバンドの場面。
GL3 = [S.track(f"Lギター（かき鳴らし）{i + 1}弦め", "distGuitar", **{k: v for k, v in rock_gtr_spec(0.125, -0.6).items() if k != "guitarTone"}) for i in range(6)]      # 音色プリセットなし（内蔵の歪み）＋録音ギター。聞きくらべで合っていた音
GR3 = [S.track(f"Rギター（かき鳴らし）{i + 1}弦め", "distGuitar", **{k: v for k, v in rock_gtr_spec(0.12, 0.6).items() if k != "guitarTone"}) for i in range(6)]
SL, SR = G2.Strummer(GL, S, 30), G2.Strummer(GR, S, 51); SL3, SR3 = G2.Strummer(GL3, S, 31), G2.Strummer(GR3, S, 52)
# v5（2026-11-24）: 聞きくらべを聞いた人間「音が切れて和音がにごるかな」。
#   切れる → 和音が変わる時に弦を少し前で止めていたのをやめ（gap 0）、音の消え方を長く（release 0.5 → 0.9）。
#   にごる → 歪んだギターで 7 や 6 の音まで弾き、左右とも低い所（E3〜C#4）で鳴らしていた。左は根音と5度だけ（パワーコード）、右は三和音だけを高い所（G3〜B4）で弾く。
import re as _re
for _st in (SL, SR, SL3, SR3): _st.gap = 0.0
for _t in GL + GR + GL3 + GR3: _t.spec["release"] = 0.9


def simple(ch):
    """歪んだギター用に、和音を三和音にする（7・6・9 を落とす。sus4 と dim は残す）"""
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "dim" if ("m7b5" in rest or "dim" in rest) else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


def shapes(b, prev):
    c = S.chords[b]; return G2.low_shape(simple(c), with_third=False), G2.triad(simple(c), prev, top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5)))
PF = {"type": "pluckfilter", "freq": 2000, "depth": 0.6, "rate": 30, "hold": 4}
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.055, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
PAD = [S.track(f"水晶のパッド{i + 1}", "pad", patch="surgePadCrystals", volume=0.11, pan=(-0.2, 0.2, 0)[i], reverb=0.3) for i in range(3)]
PN = [S.track(f"ガラスのピアノ{i + 1}", "lead", patch="surgeKeysAliasGlassPiano2", volume=0.085, pan=(-0.25, 0, 0.25, 0.1)[i], reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(4)]
ARP = S.track("シンセのかけ上がり（矩形波のプラック）", "lead", patch="kfbSquarePluck", volume=0.068, pan=0.2, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HOOK = S.track("フックのシンセ（声のようなリード）", "lead", patch="kfbFormantLead", volume=0.06, mono=True, pan=-0.1, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}])
KNOCK = S.track("ガラスをたたくベル", "lead", patch="surgeFantasyBell", volume=0.08, pan=-0.3, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}])
BOO = S.track("鉄琴の合いの手", "lead", patch="kfbGlocken", volume=0.05, pan=0.3, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.3}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
FXT = S.track("効果音（当たる音・逆回しのシンバル・きらめき）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
SWELL = [S.track(f"ふくらむ和音{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); FXH = {}


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))


def mel(b, s, up=0):
    return KEYOF[S.scene_of(b)[0]].mel(s, oct=4 + up)                              # ホ長調は 1＝E4、ト長調は 1＝G4


# ================= 歌 =================
BAD = []


def put(name, bars_s, segs, pre=0):
    """bars_s: 小節を | で区切った旋律。segs: 句ごとの歌詞。pre: 前の場面の最後の小節から歌い始める数（食って入る句）"""
    b0 = S.sc(name)[0] - pre; lines = [x.strip() for x in bars_s.split("|")]; bars = list(range(b0, b0 + len(lines)))
    assert len(lines) == len(S.sc(name)) + pre, (name, len(lines))
    for x in lines: assert abs(sum(float(y.split(":")[1]) for y in x.split()) - 4) < 1e-6, (name, x)
    nn = sum(1 for x in " ".join(lines).split() if not x.startswith("R")); mm = sum(mora(t) for t in segs)
    if nn != mm: BAD.append((name, nn, mm, [mora(t) for t in segs]))
    ml = [x if x == "R:4" else mel(b, x) for b, x in zip(bars, lines)]
    for b, m in zip(bars, ml):
        if m != "R:4": V.bar(b, m)
    LY.flow(bars, ml, "/".join(segs), name)


put("高い棚", "R:1 3:1 5:1 6:1 | 5:4 | 3:1 5:1 7:2 | 5:3 R:1 | R:1 2:1 3:1 5:1 | 6:4 | 5:1 3:1 2:2 | 3:3 R:1 | R:4 | R:4", ["おみせのいちばん", "たかいたなのはな"])                    # 4小節のばす長い句
put("見るだけ", "5:1 5:0.5 3:1.5 R:1 | 5:1 5:0.5 6:1.5 R:1 | 6:1 6:0.5 #4:1.5 R:1 | 6:1 6:0.5 1':1.5 R:1 | 7:1 7:0.5 5:1.5 R:1 | 5:1 5:0.5 2:1.5 R:1", ["みてる", "だけで", "いいの", "さわる", "なんて", "むりよ"])      # 1小節の短い句
RA = lambda p: "R:1 {}:0.5 {}:0.5 {}:0.5 {}:0.5 {}:1".format(*p.split())             # 休みから入って最後をのばす
RB = lambda p: "{}:0.5 {}:0.5 {}:0.5 {}:0.5 {}:1.5 R:0.5".format(*p.split())
put("言いわけ", " | ".join([RA("3 3 3 5 3"), RB("2 2 2 3 2"), RA("1 1 1 3 1"), RB("3 2 3 2 3"), RA("5 5 5 6 5"), RB("5 5 2 3 2"), RA("6 6 6 1' 6"), RB("3 3 2 2 3"), RA("5 5 6 1' 6"), RB("7 7 5 7 5"), RA("6 6 1' 1' 6"), RB("5 5 6 5 5")]),
    ["だれもがみてるひとよ", "わたしのばんはこない", "ねだんもきけずかえる", "それでもまたきちゃうの", "いいわけふえるほどに", "すきがおおきくなるの"])
put("目が合う", "R:2 3:1 5:1 | 2:1 1:1 2:2 | R:1 3:1 5:1 7:1 | 5:3 R:1", ["たしかにめがあうの"])
put("サビ0", "R:3 1':1 | 7:1.5 5:0.5 3:2 | #4:1 6:1 6:0.5 R:0.5 7:1 | 6:1.5 5:0.5 3:2 | 3:1 2:1 3:0.5 R:0.5 1':1 | 7:1.5 5:0.5 7:2 | 6:1 5:1 3:0.5 R:0.5 6:1 | 5:1.5 3:0.5 2:2 | 2:3 R:1",
    ["ひかりのなかの", "いちばんうえの", "なまえもしらぬ", "そのひとに"], pre=1)                                                                                         # 1拍早く食って入る
M = "1':1.5 7:1 5:0.5 3:1 | #4:0.5 5:1.5 6:1.5 R:0.5 | 7:1.5 6:1 5:0.5 3:1 | 1:0.5 2:1.5 1:1.5 R:0.5 | 1':1 7:0.5 5:1.5 7:1 | 6:0.5 5:1.5 3:1.5 R:0.5 | 6:1.5 5:0.5 #4:1.5 3:0.5 | 2:3.5 R:0.5"        # サビ: 高い音から下りてくる
put("サビ1", M + " | " + M, ["みているだけで", "いいときめてた", "とどかぬはなに", "こいをした", "ふれたらすぐに", "こわれそうでね", "きれいなままで", "いてほしい"])
put("サビ2", "R:3 1':1 | 7:1.5 5:0.5 3:2 | #4:1 5:1 6:0.5 R:0.5 7:1 | 6:1.5 5:0.5 3:2 | 1:1 2:1 1:0.5 R:0.5 1':1 | 7:1.5 5:0.5 7:2 | 6:1 5:1 3:0.5 R:0.5 6:1 | 5:1.5 #4:0.5 3:2 | 2:3 R:1",
    ["こえをかけたの", "きみのほうから", "ゆめかとおもう", "ひるさがり"], pre=1)
T3 = lambda a, b_, c: "{}:1 {}:1 {}:0.5 {}:1.5 | ".format(*a.split()) + "{}:1 {}:0.5 {}:0.5 {}:2 | ".format(*b_.split()) + f"{c}:2.5 R:1.5"                          # 3小節の句
put("声", " | ".join([T3("3 5 5 6", "5 3 2 3", "5"), T3("6 1' 1' 6", "7 6 5 7", "5"), T3("2 3 3 5", "5 3 5 7", "6"), T3("6 5 5 2", "2 3 5 7", "5")]), ["そのひとがわらうの", "まいにちくるよねと", "きづかれていたんだ", "かおからひがでそう"])
G3 = lambda a, b_, c: "R:1 {}:1 {}:1 {}:1 | ".format(*a.split()) + "{}:1.5 {}:0.5 {}:1 {}:1 | ".format(*b_.split()) + f"{c}:3 R:1"
put("その人の言葉", " | ".join([G3("3 5 6", "6 5 3 2", "3"), G3("3 5 6", "6 5 6 5", "2"), G3("5 6 6", "5 5 2 1", "3")]) + " | R:3 3:1", ["だれもこないのと", "うえからみていた", "きみをまちながら", "と"])
put("この手", "5:1.5 3:0.5 1:2 | 7,:1 2:1 3:0.5 R:0.5 3:1 | 5:1.5 3:0.5 5:2 | 5:1 6:1 7:0.5 R:0.5 1':1 | 1':1.5 6:0.5 5:2 | 7:1 5:1 3:0.5 R:0.5 2:1 | 3:1.5 2:0.5 1:2 | 2:3 R:1",
    ["どかないのは", "はなではなくて", "のばさずにいた", "このてだね"])                                                                                                  # 「と」は前の場面の最後の拍（1拍早く食って入る）
O = "R:2 1':1 7:1 | 6:1 6:0.5 #4:0.5 6:1 3:1 | R:2 7:1 6:1 | 3:1 3:0.5 2:0.5 3:1 2:1 | R:2 1':1 7:1 | 6:1 6:0.5 5:0.5 #4:1 3:1 | R:2 6:1 5:1 | 2:1 1:1 2:2"                   # 小節のまん中から入る
put("サビ3", O, ["こわれやしない", "あなたのこえが", "こんなにちかく", "きこえるの"])
F4 = lambda a, c, d, b_: f"{a}:0.5 {a}:0.5 {a}:0.5 {a}:0.5 {c}:1 {d}:1 | " + b_                                                                                        # 同じ音を連打してから跳ぶ
put("サビ4", " | ".join([F4("5", "1'", "7", "#4:1 5:1 6:1.5 R:0.5"), F4("6", "1'", "7", "2:1 2:1 1:1.5 R:0.5"), F4("7", "1'", "7", "6:1 5:1 3:1.5 R:0.5"), F4("6", "5", "#4", "2:3 R:1")]),
    ["みてるだけじゃなくて", "となりでさいていて", "かれてもそばにいる", "それがこいでしょ"])
put("またあした", "R:2 5,:1 3:1 | 5:2 6:1 5:1 | 7:1.5 5:0.5 3:1.5 R:0.5 | R:2 5,:1 5:1 | 6:1 1':1 R:2", ["またあしたくるね", "こんどは"])                                  # 低い音から6度跳ぶ。言いかけて切れる
assert not BAD, BAD


# ================= 伴奏 =================
def sub(b, pat="r---------------"):
    """シンセの低いベース。r＝根音、5＝5度、R＝1オクターブ上、-＝のばす、.＝休み"""
    r = low(S.chords[b], "E1"); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + {'r': 0, '5': 7, 'R': 12}[pat[i]])}:{L * 0.25:g}"); i += L
    SUB.bar(b, " ".join(out))


def _ch(tracks, b, pat, center, n):
    v = sorted(voice(S.chords[b], center, n))
    for j in range(n):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(v[j])}:{L * 0.25:g}"); i += L
        tracks[j].bar(b, " ".join(out))


def saw(b, pat="x---------------", center=66): _ch(SAW, b, pat, center, 5)
def pad(b, center=64): _ch(PAD, b, "x---------------", center, 3)
def piano(b, pat="x-------x-------", center=66): _ch(PN, b, pat, center, 4)


def swell(b):
    v = sorted(voice(S.chords[b], 68, 3))
    for j in range(3): SWELL[j].bar(b, f"{N(v[j])}:4")


def arp(b, k=0):
    t = sorted(voice(S.chords[b], 75, 4)); u = t + [t[0] + 12, t[1] + 12]
    o = ([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3], [4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5], [0, 2, 1, 3, 2, 4, 3, 5, 4, 3, 2, 1, -1, -1, -1, -1], [0, 1, 2, 3, -1, -1, 2, 3, 4, 5, -1, -1, 4, 3, 2, 1],
         [0, -1, -1, 2, -1, -1, 4, -1, 3, -1, -1, 5, -1, -1, 2, -1])[k % 5]
    ARP.bar(b, " ".join("R:0.25" if x < 0 else f"{N(u[x])}:0.25" for x in o))


def knock(b, twice=False):
    """ガラスをたたく「コン、コン」。和音の5度の高い音を2回"""
    m = low(S.chords[b], "E1") + 7 + 48
    KNOCK.bar(b, f"{N(m)}:0.5 {N(m)}:0.5 R:3" if not twice else f"{N(m)}:0.5 {N(m)}:0.5 R:1 {N(m)}:0.5 {N(m)}:0.5 R:1")


def boo(b, k=0):
    t = sorted(voice(S.chords[b], 79, 3)); BOO.bar(b, ("R:1.5 {0}:0.5 R:1 {1}:0.5 {2}:0.5", "R:0.5 {2}:0.5 R:2 {0}:0.5 {1}:0.5", "{0}:0.5 R:1 {1}:0.5 R:1.5 {2}:0.5")[k % 3].format(*[N(x) for x in t]))


TR = [None]


def gtr(b, pat):
    """v3（2026-11-24 人間「弾き方が曲にあってないというか交わってない」「途切れる感じが自然じゃない」）:
    ギターは、シンセの和音（またはピアノ）と同じリズムで弾く。8分をずっと刻むのをやめ、和音が鳴る所でいっしょに鳴らして、次の一打まで鳴らしたままにする。
    pat は和音の型（x＝鳴らす、-＝のばす、.＝止める）。表のマスはダウン、ウラのマスはアップにする。歌のあいだも止めない"""
    g = "".join(("D" if i == 0 else "d" if i % 2 == 0 else "U") if c == "x" else c for i, c in enumerate(pat)); lo, TR[0] = shapes(b, TR[0])
    SL.bar(b, g, lo, feel=16); SR.bar(b, g, TR[0], feel=16)


TR3 = [None]
G8 = ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-", "D-d-d-D-d-D-d-d-", "D-D-d-d-D-d-d-d-")
G8b = ("D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-", "D-U---U-D-U-D-U-", "D---D-U---U-D-U-")


def strum(b, i):
    """聞きくらべの 3: つやのあるロックの音で、8分のかき鳴らし（左はぜんぶダウン、右は下・上）"""
    lo, TR3[0] = shapes(b, TR3[0]); SL3.bar(b, G8[i % 4], lo, feel="down"); SR3.bar(b, G8b[i % 4], TR3[0])


HK = ("3':1 1':0.5 7:0.5 5:1 7:0.5 1':0.5", "#4:0.5 6:0.5 1':1 2':1 1':1", "3':1 1':0.5 6:0.5 5:1 6:0.5 1':0.5", "2':1 1':1 2':2", "7:0.5 2':0.5 3':1 5':1 3':1", "3':1 2':1 6:2", "#4:0.5 6:0.5 1':0.5 3':0.5 2':1 #4:1", "2':3 R:1")
HK2 = ("1':1.5 7:0.5 5:2", "#4:1 6:1 3':2", "3':1.5 1':0.5 6:2", "3':1 2':1 3':2", "1':1.5 7:0.5 3':2", "6:1 #4:1 3':2", "6:0.5 1':0.5 3':1 5':2", "2':3 R:1")
SOLO = ("3':1.5 2':0.5 1':1 6:1", "6:0.5 1':0.5 3':1 1':2", "5':1 3':0.5 1':0.5 7:2", "2':3 R:1")
K2 = ("X.....X...X.....", "X..X......X.....", "X.....X..X......", "X.........X..X..")       # キックが食いこむ形（4つ打ちではない）
SN, SNg = "....X.......X...", "....X..o.o..X..."
H16, H16o, H8, FOURK, NO = "XxxxXxxxXxxxXxxx", "XxxxXxxxXxxxXxO.", "x.x.x.x.x.x.x.x.", "X...X...X...X...", "................"


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."


def hook(b, line, gtr_too=False):
    HOOK.bar(b, mel(b, line))
    if gtr_too: LEAD.bar(b, mel(b, line, -1))


def band(b, i, sung=None, hat=None, kick=None, k=0, sawp="x-------x-------", clap=True, st=False):
    """サビの土台: 食いこむキック、16分のハイハット、低いベース、広い和音、左右のギター"""
    D.set(b, kick or K2[(i + k) % 4], SNg if i % 2 else SN, hat or (H16o if i % 2 else H16)); sub(b, ("r-------..r-..r-", "r--r--r-........", "r-----..r--r----", "r-..r-....r--R--")[(i + k) % 4]); saw(b, sawp)
    if st: strum(b, i + k)      # v6: ギターは「全員が鳴っている場面」だけ（聞きくらべで、人間が「③＝全部そろった時だけ合っている」）。うすい場面では弾かない
    if clap: CLP.bar(b, "R:1 B4:1 R:1 B4:1")


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; sung = G2.sung_slots(V, S, b)
    if n == "合図":                                                      # 始まり: 歌なしのフックを全員で（2小節）
        band(b, i, kick=FOURK, sawp="x--x--x---x--x--" if i == 0 else "x-----------....", st=i == 0); (i == 0 and arp(b, 0)); hook(b, (HK[0], "2':3 R:1")[i], True)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        else: fill(b, 3)
    elif n == "高い棚":                                                  # 静か: パッドとピアノ。ガラスをたたく音
        pad(b); piano(b, "x---------------" if i < 8 else "x-------x-------")
        if i % 2 == 0: knock(b)
        if i == 0: fxh(b, 0, "down", 2)
        if i >= 4: sub(b, "r---------..r---")
        if i >= 8: D.set(b, "X.........X.....", NO, H8); arp(b, 4)
    elif n == "見るだけ":                                                # 短い句: 句のあいだに「コン、コン」。食いこむキックだけ
        pad(b); piano(b, "x-----x---------"); sub(b, "r----r----------"); D.set(b, K2[i % 4], "............X...", H8); knock(b); boo(b, i)
        if last: fill(b, 1)
    elif n == "言いわけ":                                                # 早口: ドラムとベースが主役。4小節ごとに音が増える
        D.set(b, K2[i % 4], SNg, H16o if i % 4 == 3 else H16); sub(b, ("r-------..r-..r-", "r--r--r-........", "r-----..r--r----", "r-..r-....r--R--")[i % 4]); piano(b, ("x--x--x---------", "x-----x---x-----")[i % 2])
        if i >= 4: arp(b, 2 + i % 2); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i >= 8: saw(b, "x---------------", 62); boo(b, i)
        if i == 0: crash(D, b, "C2", 4)
        if i in (3, 7): fill(b, 4)
        if last: D.set(b, "X.........X.....", "....X...........", NO); FX.bar(b, "C5:4")
    elif n == "目が合う":                                                # 止まったように静か。ガラスの音が2回ずつ
        pad(b); knock(b, twice=True)
        if i >= 2: sub(b, "r---------..r---"); swell(b)
        if last: D.set(b, NO, NO, NO); fill(b, 0); fxh(b, 2, "rev", 2)
    elif n == "ドロップ1":                                               # フックをシンセとリードギターで。4つ打ち
        if i < 8:
            band(b, i, kick=FOURK, hat="..x...x...x...x.", sawp=("x--x--x---x--x--", "x-----x---x-----")[i % 2], st=True); hook(b, HK[i], True)
            if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
            if i == 7: fill(b, 2)
        else: pad(b); sub(b, "r---------..r---"); D.set(b, "X.........X.....", NO, H8); knock(b)       # 最後の2小節は落として、歌が食って入る
    elif n == "サビ0":                                                   # 別の和音の、静かなサビ。ピアノとベースと「コン、コン」
        pad(b); piano(b, ("x-----x---x-----", "x---x-----x-----")[i % 2]); sub(b, "r----r----------"); D.set(b, K2[i % 4], "............X...", H8)
        if i % 2 == 0: knock(b)
        if i >= 4: arp(b, 4)
        if i >= 6: FX.bar(b, "C5:4"); swell(b)
        if last: fill(b, 0); fxh(b, 2, "rev", 2)
    elif n == "サビ1":
        band(b, i, sung=sung, k=0, st=True); arp(b, i % 2)
        if i % 8 == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i >= 8 and i % 2 == 0: boo(b, i // 2)
        if i == 7: fill(b, 3)
        if last: fill(b, 1)
    elif n in ("立ち上げ1", "立ち上げ2"):                                # IV → V → ♭VI → ♭VII と上がる。スネアが細かくなる
        two = n == "立ち上げ2"
        saw(b, "x-------x-------" if i < 4 else "x---x---x---x---", 62 + i); sub(b, "r-----r-r-------" if i < 4 else "r--r--r-r--r--r-"); None
        D.set(b, "X.......X......." if i < 2 else FOURK, NO if i < 2 else ("....x.......x..." if i < 4 else "x...x...x...x..." if i < 6 else "x.x.x.x.x.x.x.x."), H8 if i < 4 else H16)
        if two: hook(b, ("1':1 2':1 3':2", "2':1 3':1 5':2")[i % 2])
        elif i >= 4: arp(b, i % 2)
        if i >= 4: FX.bar(b, "C5:4"); swell(b)
        if last:
            hat_roll(HATR, b, 1); fxh(b, 2, "rev", 2)
            if not two: D.set(b, "X.X.X.X.X.......", "x.x.x.x.X.......", NO); saw(b, "x---x---x---....", 69); sub(b, "r---r---r---....")      # 最後の1拍は歌だけ
    elif n == "サビ2":                                                   # ガラスが割れる。ここから「コン、コン」は鳴らない
        band(b, i, sung=sung, k=1, st=True); arp(b, 2 + i % 2); boo(b, i)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2); fxh(b, 2, "kira", 1); fxh(b, 3, "kira", 1)
        if last: fill(b, 2)
    elif n == "声":                                                      # A: 3小節の句。ピアノが前、ギターは右だけ
        D.set(b, K2[i % 4], SN, H8 if i < 6 else H16); sub(b, ("r----r----------", "r---------r-----", "r--r------------")[i % 3]); piano(b, ("x--x--x---x-----", "x-----x---x--x--", "x---------------")[i % 3])
        if i >= 6: arp(b, 4)
        if i == 0: crash(D, b, "C2", 4)
        if i % 3 == 2: boo(b, i // 3)
        if last: fill(b, 1)
    elif n == "その人の言葉":                                            # ト長調。その人が話す: ドラムなし、パッドとピアノとかけ上がり
        pad(b, 66); piano(b, "x---------------" if i % 3 != 2 else "x-------x-------", 68)
        if i == 0: fxh(b, 0, "kira", 1)
        if i >= 3: sub(b, "r---------..r---"); arp(b, 4)
        if i >= 6: swell(b); D.set(b, "X.........X.....", NO, NO)
        if last: FX.bar(b, "C5:4"); D.set(b, NO, NO, NO); fill(b, 1)
    elif n == "この手":                                                  # A: 全員。ギターは歌のあいだに間を作る
        band(b, i, sung=sung, k=2, sawp="x---------------", hat=H8 if i < 4 else None, st=i >= 4)
        if i == 0: crash(D, b, "C2", 4)
        if i >= 4: arp(b, i % 2)
        if last: fill(b, 0)
    elif n == "サビ3":                                                   # 別の和音のサビ: 今度は全員で。キックは半分の速さ
        band(b, i, sung=sung, kick="X.........X.....", k=3, sawp="x-----x---x-----", st=True); arp(b, 3)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 3)
    elif n == "ソロ":
        band(b, i, k=1, st=True); arp(b, i % 2); LEAD.bar(b, mel(b, SOLO[i], -1))
        if i == 0: crash(D, b, "C2", 4)
        if last: fill(b, 2)
    elif n == "ドロップ2":                                               # 前半: フック（4つ打ち）。後半: 別の和音・別のフック・食いこむキックにもどる
        if i < 8:
            band(b, i, kick=FOURK, hat="..x...x...x...x.", sawp=("x--x--x---x--x--", "x-----x---x-----")[i % 2], st=True); hook(b, HK[i], True)
            if i == 7: fill(b, 3)
        else:
            band(b, i, k=2, sawp=("x-----x--x------", "x--x------x-----")[i % 2], st=True); hook(b, HK2[i - 8], True); arp(b, i % 2); boo(b, i)
            if last: D.set(b, "X...............", NO, NO)
        if i in (0, 8): crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
    elif n == "にせの立ち上げ":                                          # もう一度上がって…落とす（最後の2小節はパッドだけ）
        if i < 8:
            saw(b, "x---x---x---x---", 62 + i); sub(b, "r--r--r-r--r--r-"); arp(b, i % 2); FX.bar(b, "C5:4")
            D.set(b, FOURK, "x...x...x...x..." if i < 4 else ("x.x.x.x.x.x.x.x." if i < 7 else "xxxxxxxxXXXXXXXX"), H16 if i < 7 else NO)
            if i == 0: crash(D, b, "C2", 4)
            if i == 7: hat_roll(HATR, b, 1)
        else:
            pad(b); piano(b, "x---------------")
            if i == 8: fxh(b, 0, "down", 2)
            if last: D.set(b, NO, NO, NO); fill(b, 0); fxh(b, 2, "rev", 2)
    elif n == "サビ4":
        band(b, i, sung=sung, kick=FOURK if odd else K2[i % 4], st=True); arp(b, i % 2); boo(b, i)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 1)
    elif n == "またあした":                                              # 静か: パッドとピアノ。最後は言いかけて、全部いっしょに切れる
        if not last: pad(b); piano(b, "x-------x-------"); sub(b, "r---------..r---"); D.set(b, "X.........X.....", NO, H8 if i >= 2 else NO)
        else: PAD[0].bar(b, f"{N(sorted(voice(S.chords[b], 64, 3))[0])}:2 R:2"); piano(b, "x-------........"); sub(b, "r-------........"); D.set(b, "X.......", NO, NO) if False else D.set(b, "X...............", NO, NO)
        if i == 0: fxh(b, 0, "down", 2)

for b_, hs in FXH.items(): FXT.bar(b_, fx_bar(*hs))
SL.end(S.nb); SR.end(S.nb); SL3.end(S.nb); SR3.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース×ダンス×ロックの恋の歌（144・ホ長調・約4分48秒）。高嶺の花（見えていても手が届かない、あこがれの人）がコンセプト。お店のいちばん高い棚の花のような人に、見るだけと決めて通う話。"
          "場面の並び・長さ・旋律の句の形・始まり方・終わり方は、くじ（form_dice.py・種 11672）で決めた。ガラスをたたくベルの2音が、その人が声をかけた所で消える。言いかけたまま終わる。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "シンセのかけ上がり（矩形波のプラック）", mid=90, down=12, up=10, seed=30); humanize(path, "リードギター", mid=98, down=10, up=12, seed=4)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js) + SL3.velocity(js) + SR3.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ4", 0, None, KE)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
# v7: ギターを全員の場面だけにしたら、ギターの無い場面が 4〜6dB 小さくなり（-22〜-27dB）、点数も 6.5 に落ちた。ギターの無い場面の伴奏を持ち上げて、段差を小さくする
QUIET = {"見るだけ": 1.2, "言いわけ": 1.2, "目が合う": 1.3, "立ち上げ1": 1.15, "立ち上げ2": 1.15, "声": 1.2, "にせの立ち上げ": 1.2}
# v8（2026-11-25）: 見つけたまちがい。「glossy-jrock」はギターの音色の名前ではなかった（仕上げの参考の音の名前）。作曲ソフトは知らない名前を無視し、
#   ほかに録音ギター（DI）を使う音色のパートが1つでもあれば曲全体を録音ギターで鳴らし、無ければ合成のギターで鳴らす。
#   人間が「合っている」と言った聞きくらべは録音ギターで鳴っていて、v6・v7 は浅い歪みのパートを消したせいで合成のギター（1〜6kHz ばかりの細い音）に変わっていた（点数 6.5）。
#   → 曲に「録音ギター（emily）を使う」と書いて、どの場面でも同じ音で鳴るようにする。
js["diGuitar"] = "emily"; js["guitarWobble"] = False
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in QUIET.items():
        for b in S.sc(name): g[b] = round(min(g[b], 1.0) * k, 4)
    p_["barGain"] = g[:S.nb]
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
