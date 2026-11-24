# KFB 03C「トゲなしローズ」Thornless Rose（仮）— Kawaii future bass × ダンス × ロック。4分の4・188・ニ長調（1場面だけヘ長調）。237小節・約5分03秒。
#
# 2026-11-25 人間「3曲目行こう」→ 高嶺の花の恋の歌 3曲のうち C（高嶺の花と呼ばれる側）。A（kfb_03a_madogiwa.py）・B（kfb_03b_glass.py）とは別の曲として、旋律・和音・ノリ・音色を新しく書いた。
#   骨組みはくじ（tools/vt3/form_dice.py --skeleton 36767 290・1回めをそのまま）: 始まり方（ベースだけ）・場面の並び・小節数・旋律の句の形・終わり方（フックをくり返しながら消える）・テンポ 188。
#   人が決めた所: 調（ニ長調。「君の答え」だけ短3度上のヘ長調）、和音（サビは I → ♭III → ♭VII → IV → vi → II7 → IV → V）、ノリ（キックが食う細かいドラム）、低音（エレキベース）、
#     ギター（B で人間が OK を出した音＝録音ギター emily＋内蔵の歪み。全員が鳴る場面だけ。8分のかき鳴らし）。
#   この曲だけのもの: 「みんなの声」。まわりが彼女に貼る言葉「き・れ・い」を、切った声で合いの手に入れる。「好きです」と言う場面から先は出てこない。
# 物語（高嶺の花＝見えていても手が届かない、あこがれの人。その「呼ばれる側」の歌）: 完ぺきに見せているけれど、だれも近くに来ない。すみの席の君だけが、ふつうの声で「おはよう」と言う。
#   なんでもできるのに、声をかけることだけができない。高嶺の花をやめに、君のところへ降りていく。廊下を走って「好きです」。君の答えは「作りものじゃないほうの笑顔を待ってた」。
# 歌詞: 曲名の言葉（とげ・ローズ）は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("31", "rose", "トゲなしローズ（仮）", "Thornless Rose", 188, 4, "D", "major", "カワイイ・フューチャーベース×ダンス×ロック（ボカロ）")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud " + S.flags + " --space room --space-wet 0.08"
KD, KF = Key("D", "major"), Key("F", "major")
CH = ["D", "F", "C", "G", "Bm7", "E7", "G", "A7sus4"]                             # サビ
CR = ["Bm7", "Bb", "F#m7", "G", "Em7", "A7", "Dmaj7", "D7"]                       # サビ（別の和音）
AV = ["Bm7", "Bm7", "G", "G", "Em7", "Em7", "A7sus4", "A7"]                       # A
RP = ["Em7", "A7", "F#m7", "B7", "Em7", "A7", "Dmaj7", "G", "Em7", "A7", "F#m7", "B7", "G", "G", "A7sus4", "A7"]      # 早口
SC = []


def scene(name, n, kind, chs, key=KD):
    assert len(chs) == n, (name, n, len(chs)); SC.append((name, key)); S.scene(name, n, kind, chs)


scene("ベース", 2, "break", ["D", "D"])
scene("サビ1", 16, "chorus", CH * 2)
scene("サビ別1", 8, "chorus", CR)
scene("サビ短", 8, "chorus", CH)
scene("立ち上げ1", 4, "pre", ["G", "A", "Bb", "C"])
scene("早口1", 16, "verse", RP)
scene("ドロップ1", 4, "break", CH[:4])
scene("サビ中", 8, "chorus", CH)
scene("サビ半分", 10, "chorus", CH + ["G", "A"])
scene("A1", 16, "verse", AV * 2)
scene("早口2", 8, "verse", ["Em7", "A7", "F#m7", "B7", "Em7", "A7", "A7sus4", "A7"])
scene("A2", 4, "pre", ["Bm7", "G", "Em7", "A7"])
scene("サビ降", 8, "chorus", CH)
scene("A倍", 4, "verse", ["Bm7", "G", "Em7", "A7"])
scene("早口3", 16, "verse", RP)
scene("サビ連", 8, "chorus", CH[:7] + ["C7"])                                     # 最後の和音がヘ長調の V
scene("新歌1", 16, "bridge", ["Bbmaj7", "C/Bb", "Am7", "Dm7", "Gm7", "C7", "F", "F7", "Bbmaj7", "C/Bb", "Am7", "Dm7", "Gm7", "C7", "A7sus4", "A7"], KF)
scene("A短", 10, "verse", AV + ["G", "A"])
scene("サビ別2", 16, "chorus", CR + CR[:7] + ["D"])
scene("ソロ1", 12, "solo", CH + CH[:4])
scene("A3", 8, "verse", AV)
scene("ソロ2", 8, "solo", CH)
scene("立ち上げ2", 8, "pre", ["G", "G", "A", "A", "Bb", "Bb", "C", "C"])
scene("新歌2", 11, "bridge", ["Gmaj7", "A/G", "F#m7", "Bm7", "Em7", "A7", "D", "D", "Gmaj7", "A/G", "D"])
scene("消えていく", 8, "outro", CH[:4] * 2)
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3
KEYOF = dict(SC)

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BSPEC = rock_bass_spec(0.165); BSPEC["ampDrive"] = 0.25
BSPEC["fx"] = [{"type": "eq", "low": 0, "mid": 4, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 1.5, "midHz": 2200, "high": 1}]
BASS = S.track("指弾きのベース", "bass", **BSPEC)
GSP = lambda v, p: {**{k: x for k, x in rock_gtr_spec(v, p).items() if k != "guitarTone"}, "release": 0.9}      # B で OK が出た音: 音色プリセットなし（内蔵の歪み）＋録音ギター
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **GSP(0.125, -0.6)) for i in range(6)]
import os as _os
CUT = int(_os.environ.get("KFB_CUT", "1"))      # v2: 聞きくらべで人間が選んだのは 1（「最初のカッティング以外は使えない」）                                         # ギターの弾き方の切りかえ（聞きくらべ用）: 0＝8分のかき鳴らし、1＝ファンクのカッティング、2＝同じ弾き方でクリーンの音、3＝間の多いカッティング（左は弾かない）・クリーン
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **({**GSP(0.2, 0.6), "amp": "jpopClean", "ampDrive": 0.12} if CUT >= 2 else GSP(0.12, 0.6))) for i in range(6)]
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.14, 0.1))
SL, SR = G2.Strummer(GL, S, 32), G2.Strummer(GR, S, 53); SL.gap = SR.gap = 0.0
PF = {"type": "pluckfilter", "freq": 2000, "depth": 0.6, "rate": 30, "hold": 4}
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.055, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
PAD = [S.track(f"きらめくパッド{i + 1}", "pad", patch="surgePadSparkly", volume=0.09, pan=(-0.2, 0.2, 0)[i], reverb=0.3) for i in range(3)]
EP = [S.track(f"エレピ{i + 1}", "lead", patch="surgeKeysDxEp", volume=0.075, pan=(-0.25, 0, 0.25, 0.1)[i], reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(4)]
ARP = S.track("はじくシンセのかけ上がり", "lead", patch="surgeNicePluck", volume=0.07, pan=0.2, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HOOK = S.track("フックのシンセ（矩形波のリード）", "lead", patch="kfbSquareLead", volume=0.055, mono=True, pan=-0.1, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
FXT = S.track("効果音（当たる音・逆回しのシンバル・きらめき）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
SWELL = [S.track(f"ふくらむ和音{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); FXH = {}


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))


def mel(b, s, up=0):
    return KEYOF[S.scene_of(b)[0]].mel(s, oct=4 + up)                              # ニ長調は 1＝D4、ヘ長調は 1＝F4


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


X = "5,:0.5 3:1.5 3:0.5 5:1.5 | 5:1 5:0.5 1':2 R:0.5 | 2:0.5 5:1.5 4:0.5 2:1.5 | 4:1 6:0.5 5:2 R:0.5 | 6,:0.5 5:1.5 5:0.5 6:1.5 | 6:1 #4:0.5 6:2 R:0.5 | 4:0.5 6:1 1':1 6:1.5 | 5:3 R:1"      # サビ: 低い音から6度以上跳ぶ
put("サビ1", X + " | " + X, ["たかねのはなと", "よばれるたびに", "ほほえむだけの", "くせがつく", "ほんとはちがう", "ふつうのおんな", "のこでいたいと", "いえなくて"])
put("サビ別1", "3:0.5 3:1 5:1 6:1.5 | 5:2.5 1:1 R:0.5 | 3:0.5 3:1 5:1 7:1.5 | 6:2.5 4:1 R:0.5 | 2:0.5 2:1 4:1 6:1.5 | 5:2.5 2:1 R:0.5 | 3:0.5 5:1 7:1 6:1.5 | 5:3 R:1", ["だれもこない", "つくえのそば", "まぶしいよと", "いわれても"])      # 2小節の句
SH = lambda p: "{}:0.5 {}:1 {}:1.5 R:1".format(*p.split())                          # 1小節の短い句
put("サビ短", " | ".join(SH(p) for p in ("1 3 5", "5 5 1'", "2 4 5", "4 6 1'", "6 6 1'", "6 #4 6", "4 6 1'", "5 5 2'")), ["みてよ", "ここよ", "ここに", "いるの", "とおく", "ないの", "てなら", "とどく"])
RA = lambda p: "R:0.5 {}:0.5 {}:1 {}:0.5 {}:1.5".format(*p.split())                      # 休みから入って最後をのばす
RB = lambda p: "{}:0.5 {}:0.5 {}:1 {}:1.5 R:0.5".format(*p.split())
put("早口1", " | ".join([RA("2 2 4 5"), RB("5 4 3 2"), RA("3 3 5 6"), RB("6 5 5 3"), RA("4 4 5 6"), RB("7 6 5 5"), RA("5 5 7 1'"), RB("1' 6 4 6"), RA("2 2 4 6"), RB("5 5 7 5"), RA("5 5 6 1'"), RB("6 6 5 6"), RA("6 6 1' 2'"), RB("1' 6 4 6"), RA("5 5 1' 2'"), RB("2' 1' 7 5")]),
    ["まえがみなおして", "せすじものばして", "わらいかたきめて", "きょうしつにはいる", "みんなみちあける", "となりあいたまま", "ひるもひとりきり", "へいきなふりする"])
put("サビ中", "R:2 3:0.5 5:1.5 | 5:0.5 5:1.5 1':1.5 R:0.5 | R:2 2:0.5 4:1.5 | 6:0.5 5:1.5 4:1.5 R:0.5 | R:2 5:0.5 6:1.5 | 6:0.5 #4:1.5 6:1.5 R:0.5 | R:2 6:0.5 1':1.5 | 2':0.5 1':1.5 2':1.5 R:0.5", ["はなだもの", "かぜがふく", "さむいひは", "ふるえてる"])      # 小節のまん中から入る
put("サビ半分", "3:2 5:2 | 5:2 1':1 5:1 | 4:3 R:1 | 4:2 6:2 | 6:2 5:1 3:1 | 2:3 R:1 | 6:2 1':2 | 2':2 1':1 5:1 | 6:3 R:1 | R:3 6:1", ["ほんとうはね", "すきなひとが", "ひとりいるの", "す"])      # 3小節の句。最後の「す」は次の句の頭（1拍早く食って入る）
put("A1", "6:1.5 5:0.5 3:2 | 3:0.5 5:1.5 6:0.5 R:0.5 6:1 | 1':1.5 6:0.5 5:2 | 4:0.5 5:1.5 6:0.5 R:0.5 5:1 | 5:1.5 4:0.5 2:2 | 2:0.5 4:1.5 5:0.5 R:0.5 6:1 | 5:1.5 5:0.5 4:2 | 2:0.5 2:1.5 5:0.5 R:0.5 1':1 | "
          "1':1.5 6:0.5 5:2 | 3:0.5 5:1.5 6:0.5 R:0.5 1':1 | 2':1.5 1':0.5 6:2 | 4:0.5 6:1.5 1':0.5 R:0.5 6:1 | 6:1.5 5:0.5 4:2 | 2:0.5 4:1.5 6:0.5 R:0.5 5:1 | 5:1.5 4:0.5 2:2 | 5:3 R:1",
    ["みのせきでは", "わらいごえして", "だれとでもすぐ", "なかよくなれる", "そのきみだけが", "ふつうのこえで", "おはようという", "わたしにも"])
HA = lambda p: "{}:0.5 {}:1 {}:1 {}:1.5".format(*p.split())                              # 高い音から下りてくる
put("早口2", " | ".join([HA("2' 1' 6 5"), RB("5 4 2 2"), HA("1' 7 5 3"), RB("3 3 5 6"), HA("2' 1' 6 4"), RB("5 5 7 5"), HA("2' 1' 5 4"), RB("2 2 5 5")]), ["こえかけたいのに", "あしがうごかない", "なんでもできても", "これだけできない"])
put("A2", "1':2 6:1 5:1 | 4:2 6:1 5:1 | 4:1 2:1 4:1 5:1 | 5:3 R:1", ["だからきょうこそいうんだ"])
put("サビ降", "1':1 6:0.5 5:1.5 3:1 | 5:0.5 5:1.5 1:1.5 R:0.5 | 1':1 5:0.5 4:1.5 2:1 | 4:0.5 6:1.5 5:1.5 R:0.5 | 1':1 6:0.5 5:1.5 3:1 | 2:0.5 #4:1.5 6:1.5 R:0.5 | 2':1 1':0.5 6:1.5 4:1 | 5:3 R:1", ["たかねのはなを", "やめにいくのよ", "きみのところへ", "おりていく"])
put("A倍", "R:1 3:0.5 3:0.5 5:1 6:1 | 6:0.5 5:0.5 4:1 6:1.5 R:0.5 | R:1 2:0.5 2:0.5 4:1 5:1 | 5:0.5 5:0.5 7:1 2':2", ["ろうかをはしるの", "はじめてのことよ"])
put("早口3", " | ".join([HA("2' 1' 6 5"), RB("4 4 2 5"), HA("1' 7 5 3"), RB("3 3 5 6"), HA("2' 6 5 4"), RB("5 5 7 5"), HA("1' 7 5 3"), RB("4 4 6 1'"), HA("2' 1' 6 4"), RB("5 5 2 5"), HA("1' 6 5 3"), RB("6 6 5 6"), HA("2' 1' 6 4"), RB("6 6 1' 6"), HA("2' 1' 5 4"), RB("5 5 7 2'")]),
    ["みんなふりかえる", "かみもみだれてる", "えがおわすれてる", "でもとまれないの", "きみのまえにたつ", "めをまるくしてる", "いきはきれたまま", "いまいわなきゃだめ"])
U = lambda a, c, d, b_: f"{a}:0.5 {a}:0.5 {a}:0.5 {a}:0.5 {c}:1 {d}:1 | " + b_         # 同じ音を連打してから跳ぶ
put("サビ連", " | ".join([U("3", "1'", "6", "5:0.5 5:1.5 1':1.5 R:0.5"), U("2", "5", "4", "4:0.5 6:1.5 5:1.5 R:0.5"), U("3", "1'", "6", "6:0.5 #4:1.5 6:1.5 R:0.5"), U("4", "2'", "1'", "5:3 R:1")]),
    ["すきですすきですよ", "ながくいえなくてね", "はなじゃなくてわたし", "みていてほしい"])
NS = lambda a, b_: "R:2.5 {}:0.5 {}:1 | ".format(*a.split()) + "{}:1.5 {}:0.5 {}:1.5 R:0.5".format(*b_.split())       # 小節のまん中から入る（新しい歌）
put("新歌1", " | ".join([NS("3 5", "5 5 2"), NS("3 5", "6 5 6"), NS("2 4", "5 4 2"), NS("1 3", "5 3 5"), NS("5 6", "7 5 5"), NS("5 7", "6 5 6"), NS("4 6", "5 4 5"), NS("3 6", "7 7 3")]),
    ["わかるよと", "きみがいう", "まいあさの", "そのえがお", "つくりもの", "じゃないほう", "みたくてさ", "まちわびた"])
put("A短", " | ".join(SH(p) for p in ("6 6 5", "3 3 5", "4 4 6", "6 6 1'", "2 2 4", "4 4 6", "5 5 1'", "2' 2' 7", "6 6 1'", "1' 1' 2'")), ["たかい", "ところ", "じゃなく", "きみの", "となり", "ここで", "さくと", "きめた", "いまね", "きめた"])
LG = lambda a, b_, c, d: "{}:1 {}:1.5 {}:1.5 | ".format(*a.split()) + f"{b_}:4 | " + "{}:1 {}:1 {}:0.5 {}:1.5 | ".format(*c.split()) + f"{d}:3 R:1"      # 4小節のばす長い句
put("サビ別2", " | ".join([LG("3 5 6", "5", "5 3 5 7", "6"), LG("2 4 5", "7", "7 5 3 5", "5"), LG("6 1' 2'", "1'", "1' 7 5 7", "6"), LG("4 6 1'", "2'", "7 5 7 2'", "1'")]),
    ["たかねのはなじゃない", "きみのとなりにさく", "ふつうのはなでいい", "それがいちばんいい"])
put("A3", "R:3 6:1 | 6:1.5 5:0.5 3:2 | 3:0.5 5:1.5 6:0.5 R:0.5 1':1 | 1':1.5 6:0.5 5:2 | 4:0.5 6:1.5 1':0.5 R:0.5 6:1 | 6:1.5 5:0.5 4:2 | 2:0.5 4:1.5 6:0.5 R:0.5 5:1 | 5:1.5 4:0.5 2:2 | 5:3 R:1",
    ["あしたのあさは", "わたしのほうが", "さきにいうから", "おはようと"], pre=1)
put("新歌2", " | ".join([NS("3 5", "5 5 2"), NS("3 5", "6 5 6"), NS("2 4", "5 4 2"), NS("1 3", "5 3 5"), NS("5 6", "7 5 5")]) + " | R:4", ["あしたから", "となりにね", "すわるから", "わらいかた", "おしえてね"])
assert not BAD, BAD


# ================= 伴奏（ファンキーに: 188 を「94 の16分」として感じるノリ。スネアは各小節の3拍め＝94 の2・4拍） =================
def bass(b, pat="r---------------"):
    """ベース。r＝根音、5＝5度、7＝短7度、R＝1オクターブ上、-＝のばす、.＝休み（短く切る）"""
    r = low(S.chords[b], "E1"); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + {'r': 0, '5': 7, '7': 10, 'R': 12}[pat[i]])}:{L * 0.25:g}"); i += L
    BASS.bar(b, " ".join(out))


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


TR = [None]
G8 = ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-", "D-d-d-D-d-D-d-d-", "D-D-d-d-D-d-d-d-")
G8b = ("D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-", "D-U---U-D-U-D-U-", "D---D-U---U-D-U-")


CUTA = ("D.x.x.U.x.U.x.x.", "x.U.x.U.D.x.x.U.", "D.x.x.U.x.x.D.x.", "x.U.x.x.D.x.x.U.")
CUTB = ("D---x.U.....x.U.", "x.U---x.D...x.x.", "D...x.U.x...D---", "..U...x.D.x...U.")


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "dim" if ("m7b5" in rest or "dim" in rest) else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


def strum(b, i):
    """ギター（B で OK が出た弾き方）: 8分のかき鳴らし。左は根音と5度、右は高い所の三和音。全員が鳴る場面だけ"""
    c = simple(S.chords[b])
    if CUT == 0: SL.bar(b, G8[i % 4], G2.low_shape(c, with_third=False), feel="down"); TR[0] = G2.triad(c, TR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))); SR.bar(b, G8b[i % 4], TR[0]); return
    # ファンクのカッティング（188 の8分＝94 の16分で手を振る。x＝左手を浮かせた「チャッ」、和音は弾いてすぐ止める）。右のギターが高い3本の弦で、7 の音も入れる
    TR[0] = G2.triad(S.chords[b].split("/")[0], TR[0], top_lo=66, top_hi=74, groups=((3, 4, 5),)); SR.bar(b, (CUTA if CUT < 3 else CUTB)[i % 4], TR[0], feel=8)
    if CUT < 3: SL.bar(b, "D-----d---------" if i % 2 == 0 else "D---------d-----", G2.low_shape(c, with_third=False), feel="down")


HK = ("1':1 5:0.5 3:0.5 5:1 1':1", "1':1 5:0.5 b3:0.5 5:1 1':1", "2':1 5:0.5 4:0.5 5:1 2':1", "1':0.5 6:0.5 4:1 6:2", "3':1 1':0.5 6:0.5 1':1 3':1", "2':1 6:0.5 #4:0.5 6:1 2':1", "1':0.5 6:0.5 4:1 6:1 1':1", "2':3 R:1")
SOLO = ("5:1.5 3:0.5 5:1 1':1", "1':1 5:0.5 b3:0.5 1:2", "2:0.5 4:0.5 5:1 2':2", "1':1 6:0.5 4:0.5 6:2", "3':1.5 1':0.5 6:1 1':1", "2':1 6:0.5 #4:0.5 2:2", "4:0.5 6:0.5 1':1 2':1 1':1", "2':3 R:1")
# ファンクのドラム（2小節で1まわり）: キックは食う。スネアは3拍め。ゴースト（o）。ハイハットは8分（＝94 の16分）で、ときどき開く
KF = ("X.....X.........", "X..X......X.....", "X.....X......X..", "X.X.......X.....")
SF = ("..o.....X....o..", "........X..o....", "..o.....X.......", "........X..o.o..")
HF, HFo, NO = "X.x.X.x.X.x.X.x.", "X.x.X.x.X.x.X.O.", "................"
BF = ("r-.r..R-..7-.r..", "r-....r-.5-.R-..", "r-.r..R-..5-.7-.", "r-..R-....r-.5-.")       # ファンクのベース: 根音・オクターブ・短7度・5度。休符で切る
BF2 = ("r-..r-.R..r-....", "r-.5-.r-....R-.7", "r-..R-..r-.5-...", "r-.r-...R-.7-.5-")
STB = ("....x-....x-....", "..x-......x-.x-.", "....x-..x-......", "..x-....x-..x-..")       # 和音の合いの手（裏）


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."


def hook(b, line, gtr_too=False):
    HOOK.bar(b, mel(b, line))
    if gtr_too: LEAD.bar(b, mel(b, line, -1))


def funk(b, i, k=0, st=False, sawp=None, clap=True, bf=BF, hat=None):
    """ファンクの土台: ドラム、ベース、エレピの合いの手。st＝全員（広い和音とギターも）"""
    j = (i + k) % 4; D.set(b, KF[j], SF[j], hat or (HFo if i % 2 else HF)); bass(b, bf[j]); ep(b, STB[j])
    if st: saw(b, sawp or ("x-----x---x-----", "x--x------x-----")[i % 2]); strum(b, i + k)
    if clap: CLP.bar(b, "R:2 B4:1 R:1")


CB = {}                                                                             # みんなの声（声のチョップ）: 小節 → 音
KIREI, SUGOI = "A4:0.25:き A4:0.25:れ A4:0.5:い", "A4:0.25:す A4:0.25:ご A4:0.5:い"

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "ベース":                                                    # 始まり: ベースだけ（2小節）
        BASS.bar(b, ("D2:1 D2:0.5 R:0.5 D3:0.5 R:0.5 A2:0.5 C3:0.5", "D2:0.5 R:0.5 F2:0.5 G2:0.5 R:0.5 A2:0.5 C3:0.5 D3:0.5")[i])
        if last: D.set(b, NO, "............x.xX", NO); fxh(b, 2, "rev", 2)
    elif n == "サビ1":
        funk(b, i, st=True); arp(b, i % 5)
        if i % 8 == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i % 8 == 7: CB[b] = "R:3 " + KIREI; fill(b, 4 if i == 7 else 1)
    elif n == "サビ別1":                                                 # 静かに: エレピとベースとパッド。キックだけ
        pad(b); ep(b, ("x-----x---------", "x---------x-----")[i % 2]); bass(b, "r---------..r-.."); D.set(b, "X.........X.....", NO, "x...x...x...x...")
        if i == 0: fxh(b, 0, "down", 2)
        if last: fill(b, 1)
    elif n == "サビ短":                                                  # 短い句と「みんなの声」のかけ合い
        funk(b, i, k=1, st=True, sawp="x---x---x---....")
        if odd: CB[b] = "R:3 " + (KIREI if i % 4 == 1 else SUGOI)
        if i == 0: crash(D, b, "C2", 4)
        if last: fill(b, 3)
    elif n in ("立ち上げ1", "立ち上げ2"):
        two = n == "立ち上げ2"; h = L // 2
        saw(b, "x-------x-------" if i < h else "x---x---x---x---", 62 + i); bass(b, "r---r---r---r---"); arp(b, i % 2); FX.bar(b, "C5:4")
        D.set(b, "X.......X.......", "x...x...x...x..." if i < h else "x.x.x.x.x.x.x.x.", NO)
        if i >= h: swell(b)
        if last: D.set(b, "X.X.X.X.X.......", "xxxxxxxxXXXX....", NO); hat_roll(HATR, b, 1); fxh(b, 2, "rev", 2)
    elif n in ("早口1", "早口2", "早口3"):                               # 早口: ドラムとベースが主役。あとから細かい音が増える
        funk(b, i, k=2, bf=BF2, clap=i >= 8)
        if i >= 8: arp(b, 2 + i % 3)
        if i >= 12 or (n == "早口2" and i >= 4): saw(b, "x---------------", 62)
        if i % 4 == 3 and not last: fill(b, 4)
        if last: D.set(b, "X.....X.........", "........X.X.XXXX", NO); FX.bar(b, "C5:4")
    elif n == "ドロップ1":                                               # フックと「みんなの声」
        funk(b, i, k=1, st=True); hook(b, HK[i], True); CB[b] = (KIREI + " R:1 " + SUGOI + " R:1") if not odd else ("R:2 " + KIREI + " R:1")
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 2)
    elif n == "サビ中":
        funk(b, i, k=3, st=True); arp(b, i % 5)
        if not odd: CB[b] = KIREI + " R:3"
        if i == 0: crash(D, b, "C2", 4)
        if last: D.set(b, "X...............", "........X.......", NO)
    elif n == "サビ半分":                                                # もっとゆっくりに感じる: キックは小節の頭だけ、スネアは2小節に1回
        pad(b); saw(b, "x---------------", 62); bass(b, "r-----------..r-" if not odd else "r---------------"); D.set(b, "X...............", "........X......." if odd else NO, "x...x...x...x...")
        if i == 0: fxh(b, 0, "down", 2)
        if i % 3 == 2: arp(b, 3)
        if last: fill(b, 1)
    elif n in ("A1", "A3"):                                              # A: ベースとドラムとエレピ。後半で広い和音
        funk(b, i, k=0, bf=BF if i < 8 else BF2, clap=False)
        if i >= 8: saw(b, "x---------------", 62); CLP.bar(b, "R:2 B4:1 R:1")
        if i == 0: crash(D, b, "C2", 4)
        if i == 7 and L > 8: fill(b, 2)
        if last: fill(b, 1); (n == "A3" and fxh(b, 2, "rev", 2))
    elif n == "A2":                                                      # 「だから今日こそ」: 音を減らして、上がっていく
        pad(b); ep(b, "x-------x-------"); bass(b, "r-------r-------"); D.set(b, "X.......X.......", NO if i < 2 else "x...x...x...x...", NO); FX.bar(b, "C5:4"); swell(b)
        if last: fill(b, 0); fxh(b, 2, "rev", 2)
    elif n in ("サビ降", "サビ連"):
        funk(b, i, k=2 if n == "サビ降" else 0, st=True); arp(b, i % 5)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 3 if n == "サビ降" else 0)
    elif n == "A倍":                                                     # 倍の速さ: キックとスネアが交互（走っている）
        D.set(b, "X...X...X...X...", "..X...X...X...X.", HF); bass(b, "r-r-r-r-r-R-r-5-"); saw(b, "x---x---x---x---"); ep(b, STB[i % 4]); arp(b, i % 2)
        if i == 0: crash(D, b, "C2", 4)
        if last: fill(b, 4)
    elif n == "新歌1":                                                   # ヘ長調。君の答え: 前半はパッドとエレピだけ。後半でドラムとベース
        pad(b, 66); ep(b, "x---------------" if i < 8 else STB[i % 4], 68)
        if i == 0: fxh(b, 0, "kira", 1)
        if i >= 4: bass(b, "r---------------" if i < 8 else BF[i % 4])
        if i >= 8: D.set(b, KF[i % 4], SF[i % 4], HF); arp(b, 2 + i % 3)
        if i >= 14: FX.bar(b, "C5:4"); swell(b)
        if last: fill(b, 0); fxh(b, 2, "rev", 2)
    elif n == "A短":                                                     # 短い句: 全員で3拍打って1拍あける
        D.set(b, "X.....X.........", "........X.......", "X.x.X.x.X.x....."); bass(b, "r-.r..R-..r-...."); ep(b, "x---x---x---...."); saw(b, "x---x---x---....")
        if i == 0: crash(D, b, "C2", 4)
        if i >= 8: FX.bar(b, "C5:4")
        if last: fill(b, 0)
    elif n == "サビ別2":                                                 # 別の和音のサビ: 今度は全員で。長い句
        funk(b, i, k=1, st=True, sawp="x---------x-----"); arp(b, i % 5)
        if i % 8 == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 7: fill(b, 2)
        if last: fill(b, 3)
    elif n == "ソロ1":                                                   # リードギターのソロ8小節 → シンセのフック4小節
        funk(b, i, k=3, st=True); arp(b, i % 5)
        if i < 8: LEAD.bar(b, mel(b, SOLO[i], -1))
        else: hook(b, HK[i - 8])
        if i in (0, 8): crash(D, b, "C2", 4)
        if i == 7: fill(b, 4)
        if last: D.set(b, "X...............", "........X.......", NO)
    elif n == "ソロ2":                                                   # フックをシンセとリードギターで
        funk(b, i, k=1, st=True); hook(b, HK[i], True); arp(b, i % 5)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 2)
    elif n == "新歌2":                                                   # 新しい歌をニ長調で、全員で。最後の3小節で音が減る
        if i < 8: funk(b, i, k=0, st=True, sawp="x---------x-----"); arp(b, i % 5)
        else: pad(b); ep(b, "x---------------"); bass(b, "r---------------"); D.set(b, "X.........X.....", "........X.......", "x...x...x...x...")
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 1)
    elif n == "消えていく":                                              # フックをくり返しながら消えていく
        funk(b, i, k=2, sawp="x---------------"); saw(b, "x---------------", 64); hook(b, HK[i % 4]); arp(b, i % 5)
        if i == 0: crash(D, b, "C2", 4)

for b_, hs in FXH.items(): FXT.bar(b_, fx_bar(*hs))
SL.end(S.nb); SR.end(S.nb)
S.fade_out = 9
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース×ファンク×ロックの恋の歌（188・ニ長調・約5分）。高嶺の花と呼ばれる側の女の子が、高い所から降りて、好きな人に自分から言いに行く話。"
          "場面の並び・長さ・旋律の句の形・始まり方・終わり方は、くじ（form_dice.py・種 36767）で決めた。ベースだけで始まり、フックをくり返しながら消える。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "はじくシンセのかけ上がり", mid=90, down=12, up=10, seed=31); humanize(path, "リードギター", mid=98, down=10, up=12, seed=5); humanize(path, "指弾きのベース", mid=100, down=12, up=14, seed=7)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ別2", 0, None, KD)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    chops(path, S, CB, vol=0.3, pan=0.25)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
js["diGuitar"] = "emily"; js["guitarWobble"] = False                               # 録音ギターで鳴らす（B で分かったこと: これを書かないと、合成のギターになることがある）
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
