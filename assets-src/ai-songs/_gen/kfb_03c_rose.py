# KFB 03C「トゲなしローズ」Thornless Rose（仮）— Kawaii future bass × ファンク。4分の4・130・ヘ長調（1場面だけニ長調）。158小節・約4分52秒。
#
# v3（2026-11-25）: 人間「kawaiiFutureベースでファンキーな曲に一からCを作り直そう。あとテンポは130ぐらいで」→ 全部書き直し（前の 188 の版は kfb_03c_rose_188_old.py。旋律・和音・伴奏は使っていない）。
#   骨組みはくじ（tools/vt3/form_dice.py --skeleton 43173 285 130）: 場面の並び・小節数・旋律の句の形。始まり方と終わり方は、出たものが A と同じ形だったので、次のくじ（種 43174）の
#     「手びょうしと声の切れはしだけ」「歌の最後の音で、後奏なしに終わる」を使った。
#   人が決めた所: 調（ヘ長調。「君の答え」だけ短3度下のニ長調）、和音（A は I7 ⇄ IV7 のファンクの形。サビは IV → III7 → vi → ♭VI → V）、
#     Kawaii future bass の音（食いこむリズムで短く打つ広い和音・はねるシンセベース・16分のかけ上がり・声の切れはし）、ドラム（サビとドロップは4つ打ち＋裏のハイハット、A は食いこむキックとゴースト）、
#     ギター（聞きくらべで人間が選んだファンクのカッティング。録音ギター emily＋内蔵の歪み。全員が鳴る場面だけ）。
#   この曲だけのもの: 「みんなの声」（声の切れはし「き・れ・い」「す・ご・い」「と・お・い」）。「好きです」の場面から先は「す・き」に変わる。
# 物語（高嶺の花と呼ばれる側）: 完ぺきに見せているけれど、となりは空いたまま。すみの席の君だけが、ふつうに「おはよう」と言う。廊下を走って「好きです」。
#   君の答えは「作りものじゃない笑いを見たくてさ」。ふつうの花で、君のそばで咲く。最後は「私からね、おはようを」。
# 歌詞: 曲名の言葉（とげ・ローズ）は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("31", "rose", "トゲなしローズ（仮）", "Thornless Rose", 130, 4, "F", "major", "カワイイ・フューチャーベース×ファンク（ボカロ）")
S.kit = "crocell-punch"; S.flags = S.flags + " --space room --space-wet 0.08"
KFm, KD = Key("F", "major"), Key("D", "major")
AV = ["F7", "F7", "Bb7", "Bb7", "Am7", "D7", "Gm7", "C7sus4"]                     # A: I7 ⇄ IV7 のファンクの形
HV = ["F7", "F7", "Bb7", "Bb7", "Dbmaj7", "Eb", "F7", "C7sus4"]                   # ドロップ・フック
SC = []


def scene(name, n, kind, chs, key=KFm):
    assert len(chs) == n, (name, n, len(chs)); SC.append((name, key)); S.scene(name, n, kind, chs)


scene("合図", 4, "break", ["F7", "F7", "Bb7", "C7sus4"])
scene("みんなの言葉", 6, "bridge", ["Bbmaj7", "Bbmaj7", "Am7", "Am7", "Gm7", "C7sus4"])
scene("A", 16, "verse", AV * 2)
scene("ドロップ", 8, "break", HV)
scene("サビ1", 12, "chorus", ["Bbmaj7", "A7", "Dm7", "Dbmaj7", "C7sus4", "Bbmaj7", "A7", "Dm7", "G7", "Gm7/C", "Dbmaj7", "Eb"])
scene("本当は", 8, "bridge", ["Bbmaj7", "Am7", "Gm7", "C7sus4"] * 2)
scene("サビ別", 12, "chorus", ["Gm7", "C7", "Fmaj7", "D7", "Gm7", "Bbm6", "Am7", "D7", "Gm7", "C7", "Dbmaj7", "Eb"])
scene("走る", 8, "verse", ["F7", "F7", "Bb7", "Bb7", "Am7", "D7", "Gm7", "C7"])
scene("フック1", 8, "break", HV)
scene("早口", 4, "verse", ["Gm7", "C7", "Am7", "D7"])
scene("サビ告白", 8, "chorus", ["Bbmaj7", "A7", "Dm7", "Dbmaj7", "Bbmaj7", "A7", "Dm7", "C7sus4"])
scene("サビ降りる", 8, "chorus", ["Bbmaj7", "A7", "Dm7", "G7", "Gm7", "C7", "Dbmaj7", "Eb"])
scene("君の答え", 16, "bridge", ["Gmaj7", "F#7", "Bm7", "E7", "Gmaj7", "F#7", "Bm7", "A7sus4", "Gmaj7", "F#7", "Bm7", "E7", "Gmaj7", "F#7", "Gm7", "C7"], KD)
scene("サビふつう", 16, "chorus", ["Bbmaj7", "A7", "Dm7", "Bbmaj7", "A7", "Dm7", "Gm7", "C7", "Fmaj7", "Bbmaj7", "A7", "Dm7", "Dbmaj7", "Eb", "F", "F"])
scene("フック2", 16, "break", HV * 2)
scene("おはよう", 8, "outro", ["Bbmaj7", "C/Bb", "Am7", "Dm7", "Gm7", "C7sus4", "F", "F"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3
KEYOF = dict(SC)

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BASS = S.track("はねるシンセベース", "bass", patch="kfbFmBass", volume=0.075, pan=0, duck=0.1)
SUB = S.track("低いベース", "bass", patch="kfbSub", volume=0.045, pan=0, duck=0.12)
GSP = lambda v, p: {**{k: x for k, x in rock_gtr_spec(v, p).items() if k != "guitarTone"}, "release": 0.9}      # B で OK が出た音: 音色プリセットなし（内蔵の歪み）＋録音ギター
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **GSP(0.125, -0.6)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **GSP(0.12, 0.6)) for i in range(6)]
SL, SR = G2.Strummer(GL, S, 33), G2.Strummer(GR, S, 54); SL.gap = SR.gap = 0.0
PF = {"type": "pluckfilter", "freq": 2000, "depth": 0.6, "rate": 30, "hold": 4}
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.07, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
PAD = [S.track(f"きらめくパッド{i + 1}", "pad", patch="surgePadSparkly", volume=0.09, pan=(-0.2, 0.2, 0)[i], reverb=0.3) for i in range(3)]
EP = [S.track(f"エレピ{i + 1}", "lead", patch="surgeKeysDxEp", volume=0.075, pan=(-0.25, 0, 0.25, 0.1)[i], reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(4)]
ARP = S.track("シンセのかけ上がり（矩形波のプラック）", "lead", patch="kfbSquarePluck", volume=0.068, pan=0.2, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HOOK = S.track("フックのシンセ（矩形波のリード）", "lead", patch="kfbSquareLead", volume=0.055, mono=True, pan=-0.1, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
FXT = S.track("効果音（当たる音・逆回しのシンバル・きらめき）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
SWELL = [S.track(f"ふくらむ和音{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); FXH = {}


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))


def mel(b, s, up=0):
    return KEYOF[S.scene_of(b)[0]].mel(s, oct=4 + up)                              # ヘ長調は 1＝F4（いちばん高い音は 7＝E5）、ニ長調は 1＝D4


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


put("みんなの言葉", "R:2 3:1 3:1 | 6:1 5:0.5 3:1.5 R:1 | R:2 2:1 2:1 | 5:1 3:0.5 2:1.5 R:1 | R:2 1:1 1:1 | 4:1 2:0.5 1:1.5 R:1", ["きれいだね", "すごいよね", "とおいよね"])                  # 小節のまん中から入る
FA = lambda p: "R:1 {}:0.5 {}:0.5 {}:0.75 {}:0.75 {}:0.5".format(*p.split())             # 休みから入って最後をのばす（食いこむリズム）
FB = lambda p: "{}:0.5 {}:1 {}:0.5 {}:1.5 R:0.5".format(*p.split())
put("A", " | ".join([FA("1 1 3 5 3"), FB("5 3 1 1"), FA("4 4 6 6 4"), FB("b3 4 6 4"), FA("3 3 5 7 5"), FB("6 5 3 6"), FA("2 2 4 6 4"), FB("5 4 2 5"),
                     FA("3 3 5 b7 5"), FB("5 3 5 3"), FA("6 6 4 6 6"), FB("b3 4 6 6"), FA("5 5 7 5 3"), FB("6 6 5 3"), FA("4 4 6 4 2"), FB("2 4 5 5")]),
    ["まえがみをなおして", "せすじをのばしたら", "わらいかたをきめて", "きょうしつにはいるの", "みんながみちあける", "となりはあいたまま", "おひるもひとりきり", "へいきなふりをする"])
put("サビ1", "6:1.5 6:0.5 5:1 3:1 | 3:1 2:1 3:2 | 5:1.5 5:0.5 6:1 5:1 | b3:2 5:2 | 5:3 R:1 | 6:1.5 6:0.5 7:1 6:1 | 7:1 6:1 #5:2 | 6:1.5 5:0.5 3:1 5:1 | 6:2 #4:2 | 5:3 R:1 | 5:1 5:1 b3:2 | 4:3 R:1",
    ["みてよわたしここにいるのにな", "たかいところはさむいんだよね", "おりたい"])                                                                                      # 5小節の句 ×2 ＋ 2小節
put("本当は", "3:0.5 4:1 6:1 5:1.5 | 5:2.5 3:1 R:0.5 | 2:0.5 4:1 6:1 5:1.5 | 4:2.5 5:1 R:0.5 | 6:0.5 6:1 7:1 6:1.5 | 5:2.5 7:1 R:0.5 | 4:0.5 6:1 5:1 4:1.5 | 2:2.5 1:1 R:0.5",
    ["ほんとうはね", "すきなひとが", "ひとりいるの", "すみのせきに"])                                                                                                  # 2小節の句
put("サビ別", "R:2 2:0.5 4:1.5 | 5:0.5 5:1.5 7:1.5 R:0.5 | R:2 3:0.5 5:1.5 | 6:0.5 5:1.5 3:1.5 R:0.5 | R:2 4:0.5 6:1.5 | 4:0.5 4:1.5 2:1.5 R:0.5 | R:2 5:0.5 7:1.5 | 6:0.5 5:1.5 6:1.5 R:0.5 | "
              "R:2 6:0.5 6:1.5 | 7:0.5 5:1.5 4:1.5 R:0.5 | R:2 5:0.5 b3:1.5 | 4:0.5 2:1.5 4:1.5 R:0.5", ["きみだけが", "ふつうにね", "おはようと", "いうんだよ", "それだけで", "うれしくて"])      # 小節のまん中から入る
put("走る", "1:1 3:1.5 5:1.5 | b7:4 | 6:1 6:1 4:0.5 6:1.5 | 4:3 R:1 | 3:1 5:1.5 7:1.5 | 6:4 | 6:1 4:1 2:0.5 4:1.5 | 5:3 R:1", ["ろうかをはしるのは", "うまれてはじめてよ"])               # 4小節のばす長い句
put("早口", "2:0.5 4:1 6:1.5 R:1 | 5:0.5 7:1 5:1.5 R:1 | 3:0.5 5:1 7:1.5 R:1 | 6:0.5 5:1 3:1.5 R:1", ["いきが", "きれる", "かみも", "みだれ"])                                           # 1小節の短い句
U = lambda a, c, d, b_: f"{a}:0.5 {a}:0.5 {a}:0.5 {a}:0.5 {c}:1 {d}:1 | " + b_                 # 同じ音を連打してから跳ぶ
put("サビ告白", " | ".join([U("3", "6", "5", "3:0.5 2:1.5 3:1.5 R:0.5"), U("5", "6", "5", "5:0.5 b3:1.5 5:1.5 R:0.5"), U("6", "7", "6", "7:0.5 6:1.5 #5:1.5 R:0.5"), U("5", "6", "5", "5:3 R:1")]),
    ["すきですすきですよ", "ながくいえなくてね", "はなじゃなくてわたし", "みていてほしい"])
put("サビ降りる", "7:1 6:0.5 5:1.5 3:1 | 3:0.5 2:1.5 3:1.5 R:0.5 | 6:1 5:0.5 3:1.5 1:1 | 2:0.5 #4:1.5 6:1.5 R:0.5 | 6:1 4:0.5 2:1.5 1:1 | 7,:0.5 2:1.5 5:1.5 R:0.5 | 5:1 b3:0.5 1:1.5 b3:1 | 4:3 R:1",
    ["たかねのはなを", "やめにきたのよ", "きみのところへ", "おりてきた"])                                                                                              # 高い音から下りてくる
NA = lambda p: "{}:0.5 {}:1 {}:1 {}:1.5".format(*p.split())
NB = lambda p: "{}:1 {}:2 R:1".format(*p.split())
put("君の答え", " | ".join([NA("1' 7 6 5"), NB("3 2"), NA("6 5 3 1"), NB("2 #4"), NA("2' 1' 6 4"), NB("3 7"), NA("1' 6 5 3"), NB("2 1"), NA("1' 7 6 4"), NB("3 2"), NA("1' 6 5 3"), NB("#4 6"), NA("2' 1' 7 6"), NB("7 3"), NA("1' b6 4 b3"), NB("4 2")]),
    ["きづいてたよ", "そのえがおの", "むこうがわに", "いるきみをね", "つくりものじゃ", "ないわらいを", "みたくてさと", "きみはいうの"])                                # 高い音から下りてくる（ニ長調）
T3 = lambda a, b_, c: "{}:1.5 {}:0.5 {}:1 {}:1 | ".format(*a.split()) + "{}:0.5 {}:1.5 {}:2 | ".format(*b_.split()) + f"{c}:3 R:1"       # 3小節の句
put("サビふつう", " | ".join([T3("6 6 5 3", "3 2 3", "5"), T3("6 6 7 6", "7 6 #5", "6"), T3("4 4 6 4", "5 7 5", "3"), T3("6 6 7 6", "3 #5 7", "6"), T3("5 5 b3 5", "4 2 4", "5")]) + " | R:4",
    ["ふつうのはなでね", "きみのそばでさく", "たかいとこよりも", "ここがあたたかい", "それがいちばんよ"])
put("おはよう", "R:2 5,:1 3:1 | 6:2 5:1 3:1 | 2:3 R:1 | R:4 | R:2 6,:1 4:1 | 5:2 4:2 | 1:4 | R:4", ["わたしからね", "おはようを"])                                                 # 低い音から6度跳ぶ。歌の最後の音で終わる
assert not BAD, BAD


# ================= 伴奏（Kawaii future bass × ファンク。130 の16分） =================
def bass(b, pat="r---------------", sub=True):
    """はねるシンセベース。r＝根音、5＝5度、7＝短7度、R＝1オクターブ上、-＝のばす、.＝休み。sub＝低いベースで根音をのばす"""
    r = low(S.chords[b], "E1"); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + 12 + {'r': 0, '5': 7, '7': 10, 'R': 12}[pat[i]])}:{L * 0.25:g}"); i += L
    BASS.bar(b, " ".join(out))
    if sub: SUB.bar(b, f"{N(r)}:2.5 R:0.5 {N(r)}:1")


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
def ep(b, pat="x-------x-------", center=65): _ch(EP, b, pat, center, 4)


def swell(b):
    v = sorted(voice(S.chords[b], 68, 3))
    for j in range(3): SWELL[j].bar(b, f"{N(v[j])}:4")


def arp(b, k=0):
    t = sorted(voice(S.chords[b], 75, 4)); u = t + [t[0] + 12, t[1] + 12]
    o = ([0, 2, 1, 3, 2, 4, 3, 5], [4, 3, 2, 1, 0, 1, 2, 3], [0, -1, 2, 3, -1, 4, 3, -1], [0, 1, 2, -1, 4, 5, -1, -1], [5, -1, 4, -1, 3, 2, -1, 0])[k % 5]
    ARP.bar(b, " ".join("R:0.5" if x < 0 else f"{N(u[x])}:0.5" for x in o))


def arp(b, k=0):
    """16分のかけ上がり（人間が気に入った「ピロピロピロピーン」）"""
    t = sorted(voice(S.chords[b], 75, 4)); u = t + [t[0] + 12, t[1] + 12]
    o = ([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3], [4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5], [0, 2, 1, 3, 2, 4, 3, 5, 4, 3, 2, 1, -1, -1, -1, -1], [0, 1, 2, 3, -1, -1, 2, 3, 4, 5, -1, -1, 4, 3, 2, 1],
         [0, -1, -1, 2, -1, -1, 4, -1, 3, -1, -1, 5, -1, -1, 2, -1])[k % 5]
    ARP.bar(b, " ".join("R:0.25" if x < 0 else f"{N(u[x])}:0.25" for x in o))


TR = [None]
CUT16 = ("D.xUx.xU.xD.xUx.", "x.D.xUx.D.xU.xD.", "D.xUx.xUD.x.xUx.", "x.xUD.x.xUx.D.xU")       # ファンクのカッティング（16分で手を振る。x＝左手を浮かせた「チャッ」、和音は弾いてすぐ止める）


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "dim" if ("m7b5" in rest or "dim" in rest) else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


def cutting(b, i):
    """ギター: 右が高い3本の弦でカッティング（7 の音も入れる）、左は根音と5度をキックに合わせて。全員が鳴る場面だけ"""
    TR[0] = G2.triad(S.chords[b].split("/")[0], TR[0], top_lo=66, top_hi=74, groups=((3, 4, 5),)); SR.bar(b, CUT16[i % 4], TR[0], feel=16)
    SL.bar(b, "D-----d---------" if i % 2 == 0 else "D---------d-----", G2.low_shape(simple(S.chords[b]), with_third=False), feel="down")


HK = ("1:0.5 3:0.5 5:0.5 b7:1 5:0.5 3:1", "5:0.75 3:0.75 1:0.5 R:2", "4:0.5 6:0.5 4:0.5 b3:1 4:0.5 6:1", "6:0.75 4:0.75 b3:0.5 R:2", "b3:1 5:0.5 1:0.5 5:2", "4:1 b7:0.5 2:0.5 b7:2", "1:0.5 3:0.5 5:0.5 b7:1 5:0.5 1':1", "2':1 1':1 5:2")
K4, SN, SNg, NO = "X...X...X...X...", "....X.......X...", "....X..o.o..X..o", "................"
HOF, H16, H16o = "..O...O...O...O.", "XxxxXxxxXxxxXxxx", "XxxxXxxxXxxxXxO."          # 裏のハイハット（開く）／16分
KFK = ("X..X..X...X..X..", "X.....X..X....X.", "X..X......X.X...", "X.....X...X..X..")       # A: 食いこむキック
BFK = ("r-.R..r-.R.r7-R.", "r-.R.r..5-.R..7-", "r-.R..r-..R-7-5.", "r..r.R..r-.7-.R.")      # はねるベース（根音・オクターブ・短7度・5度）
B4 = ("r-.R.r.Rr-.R.r.R", "r-.R.r.R5-.R.7.R")                                                 # 4つ打ちの場面: 根音とオクターブが交互
STAB = ("x-..x-....x-..x-", "..x-..x-....x-..", "x-....x-..x-....", "..x-....x-..x-x-")     # 広い和音を、食いこむリズムで短く打つ


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."


def hook(b, line): HOOK.bar(b, mel(b, line, 1))


def full(b, i, k=0, hat=None, stab=None, gtr=True):
    """全員の場面: 4つ打ち、裏のハイハット、手びょうし、はねるベース、広い和音の短い打ち、ギターのカッティング"""
    D.set(b, K4, SNg if i % 2 else SN, hat or HOF); bass(b, B4[(i + k) % 2]); saw(b, stab or STAB[(i + k) % 4]); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
    if gtr: cutting(b, i + k)


def groove(b, i, k=0, ep_on=True):
    """A の場面: 食いこむキック、ゴーストのスネア、16分のハイハット、はねるベース、エレピの合いの手"""
    j = (i + k) % 4; D.set(b, KFK[j], SNg, H16o if i % 2 else H16); bass(b, BFK[j])
    if ep_on: ep(b, STAB[(j + 1) % 4])


CB = {}                                                                             # 声の切れはし: 小節 → 音
KIREI, SUGOI, TOOI, SUKI = "A4:0.25:き A4:0.25:れ A4:0.5:い", "A4:0.25:す A4:0.25:ご A4:0.5:い", "A4:0.25:と A4:0.25:お A4:0.5:い", "C5:0.5:す A4:0.5:き"

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "合図":                                                      # 始まり: 手びょうしと声の切れはしだけ
        CLP.bar(b, "R:1 B4:1 R:1 B4:0.5 B4:0.5" if not last else "R:1 B4:1 B4:0.5 B4:0.5 B4:1"); CB[b] = (KIREI + " R:3", "R:2 " + SUGOI + " R:1", TOOI + " R:1 " + KIREI + " R:1", "R:1 " + SUGOI + " R:2")[i]
        if i >= 2: D.set(b, "X.....X.........", NO, NO)
        if last: fxh(b, 2, "rev", 2)
    elif n == "みんなの言葉":                                            # 静か: パッドとエレピ。みんなの言葉を、彼女がくり返す
        pad(b); ep(b, "x---------------" if not odd else "x-------x-------"); bass(b, "r---------------", sub=True); D.set(b, "X.........X.....", NO, "x...x...x...x...")
        if i == 0: fxh(b, 0, "down", 2)
        if last: fill(b, 4)
    elif n == "A":                                                       # ファンクの A。後半で広い和音の短い打ちと手びょうし
        groove(b, i)
        if i >= 8: saw(b, STAB[i % 4], 62); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i == 0: crash(D, b, "C2", 4)
        if i % 4 == 3 and not last: CB[b] = "R:3 " + (KIREI, SUGOI, TOOI)[(i // 4) % 3]
        if i == 7: fill(b, 2)
        if last: fill(b, 0); FX.bar(b, "C5:4"); fxh(b, 2, "rev", 2)
    elif n in ("ドロップ", "フック1", "フック2"):                        # フックと声の切れはし。フック2 は「す・き」
        full(b, i, k=1 if n != "ドロップ" else 0, hat=H16o if (n == "フック2" and i >= 8) else None); hook(b, HK[i % 8]); arp(b, i % 5) if n != "ドロップ" or i >= 4 else None
        if i % 8 == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i % 2 == 1: CB[b] = ("R:2 " + (KIREI if i % 4 == 1 else SUGOI) + " R:1") if n != "フック2" else ("R:2 " + SUKI + " R:1")
        if i % 8 == 3: fill(b, 4)
        if i % 8 == 7: fill(b, 3 if not last else 0)
        if last and n == "フック2": fxh(b, 2, "rev", 2)
    elif n == "サビ1":                                                   # 全員。5小節の句
        full(b, i); arp(b, i % 5)
        if i in (0, 5): crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 4: fill(b, 4)
        if i == 9: fill(b, 2)
        if last: fill(b, 1)
    elif n == "本当は":                                                  # 静か: パッドとエレピと低いベース
        pad(b); ep(b, ("x-----x---------", "x---------x-----")[i % 2]); SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:4"); D.set(b, "X.........X....." if i >= 4 else NO, NO, "x...x...x...x...")
        if i == 0: fxh(b, 0, "down", 2)
        if i >= 6: FX.bar(b, "C5:4"); swell(b)
        if last: fill(b, 0); fxh(b, 2, "rev", 2)
    elif n == "サビ別":                                                  # 別の和音のサビ: 4つ打ちだがギターなし、エレピが前
        full(b, i, k=2, gtr=False, stab="x---------x-----"); ep(b, STAB[i % 4]); arp(b, 2 + i % 3)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 5: fill(b, 4)
        if last: fill(b, 3)
    elif n == "走る":                                                    # 倍の速さ: キックとスネアが8分で交互。歌は長い音
        D.set(b, "X...X...X...X...", "..X...X...X...X.", H16); bass(b, "r.R.r.R.r.R.r.7."); saw(b, "x-------x-------"); arp(b, i % 2); cutting(b, i)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 3: fill(b, 4)
        if last: fill(b, 0)
    elif n == "早口":                                                    # 息が切れる: ドラムとベースだけ。最後に止まる
        groove(b, i, k=2, ep_on=False)
        if last: D.set(b, "X.....X.........", "....X...X.X.XXXX", NO); FX.bar(b, "C5:4"); fxh(b, 2, "rev", 2)
    elif n in ("サビ告白", "サビ降りる"):
        full(b, i, k=0 if n == "サビ告白" else 1); arp(b, i % 5)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 3: fill(b, 4)
        if last: fill(b, 2 if n == "サビ告白" else 0)
        if last and n == "サビ降りる": fxh(b, 2, "rev", 2)
    elif n == "君の答え":                                                # ニ長調。前半はパッドとエレピだけ。後半でファンクのドラムとベース
        pad(b, 66); ep(b, "x---------------" if i < 8 else STAB[i % 4], 67)
        if i == 0: fxh(b, 0, "kira", 1)
        if i >= 4: SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:4")
        if i >= 8: D.set(b, KFK[i % 4], SNg, H16); bass(b, BFK[i % 4], sub=False); arp(b, 2 + i % 3)
        if i >= 14: FX.bar(b, "C5:4"); swell(b)
        if last: fill(b, 0); fxh(b, 2, "rev", 2)
    elif n == "サビふつう":                                              # 最後のサビ: 全員。3小節の句
        full(b, i, k=1, hat=H16o if odd else HOF); arp(b, i % 5)
        if i in (0, 9): crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i % 3 == 2 and i < 15: fill(b, 4)
        if last: fill(b, 3)
    elif n == "おはよう":                                                # 静か: パッドとエレピ。歌の最後の音で終わる
        if i < 7: pad(b); ep(b, "x---------------")
        if i < 6: SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:4"); D.set(b, "X.........X.....", NO, "x...x...x...x..." if i < 4 else NO)
        if i == 0: fxh(b, 0, "down", 2)

for b_, hs in FXH.items(): FXT.bar(b_, fx_bar(*hs))
SL.end(S.nb); SR.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース×ファンクの恋の歌（130・ヘ長調・約4分52秒）。高嶺の花と呼ばれる側の女の子が、高い所から降りて、好きな人に自分から言いに行く話。"
          "場面の並び・長さ・旋律の句の形は、くじ（form_dice.py・種 43173）で決めた。手びょうしと声の切れはしで始まり、歌の最後の音で終わる。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "シンセのかけ上がり（矩形波のプラック）", mid=90, down=12, up=10, seed=31); humanize(path, "はねるシンセベース", mid=100, down=12, up=14, seed=7)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビふつう", 0, None, KFm)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    chops(path, S, CB, vol=0.3, pan=0.25)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
js["diGuitar"] = "emily"; js["guitarWobble"] = False                               # 録音ギターで鳴らす
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
