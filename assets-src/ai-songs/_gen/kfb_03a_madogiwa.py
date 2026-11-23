# KFB 03A「窓ぎわシャンデリア」Window-seat Chandelier（仮）— Kawaii future bass × ダンス × ロック。4分の4・180・イ長調 ⇄ ハ長調。224小節・約4分59秒。
#
# v4（2026-11-23）: 曲を全部書き直した（旋律・和音・場面の並び・伴奏）。v1〜v3（164・前奏 → A → B → サビ…の型）は使っていない。
#   人間: 「曲調もだしメロディ全てよくある感じ」「場面展開も今までと全部同じ感じに聞こえる。場面展開を学習してくると良い」→ docs/sound/scene-development-study.md
#         「決め事というより、そこをランダムにした方が同じにならないんじゃないかな」→ tools/vt3/form_dice.py（形のくじ）を作った
#         「骨組みだけ。あとそこにプラスオリジナリティを入れる用に。」
#   骨組みはくじ（種 27011・1回めをそのまま）: 始まり方・場面の並び・小節数・旋律の句の形・終わり方。テンポ 180 もくじ。
#   人が決めた所: 調（A・静かな場面＝イ長調、サビ・ドロップ＝短3度上のハ長調）、和音、ドラム、厚み、物語の当てはめ。
#   この曲だけのもの: 「胸の音」のキック（トク、トク）。静かな場面で鳴り、話が進むほど速くなり、最後はサビのキックになる。歌詞の「このおとを」はこの音。
# 物語（高嶺の花＝見えていても手が届かない、あこがれの人。登山の言葉は使わない）: 教室でいちばん遠い席の人。落ちた消しゴムを拾ってもらう → 名前を呼ぶ → 完ぺきに見えるその人は
#   ひとりで帰る → 雨の帰り道 → 言おうとして言えない →「話しかけてくれた人は初めて」→ 遠くしていたのは自分だった →「好きです」→ 返事「わたしもだよ」→ おはようを、あしたも。
# 歌詞: 曲名の言葉（窓ぎわ・シャンデリア）は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *
import gtr2_lib as G2

S = Song("29", "madogiwa", "窓ぎわシャンデリア（仮）", "Window-seat Chandelier", 180, 4, "A", "major", "カワイイ・フューチャーベース×ダンス×ロック（ボカロ）")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud " + S.flags + " --space room --space-wet 0.08"
KA, KC = Key("A", "major"), Key("C", "major")
CC = ["F", "G/F", "Em7", "A7", "Dm7", "Fm6", "C/G", "G7sus4"]                     # サビ（ハ長調）: IV → V/IV → iii → V/ii → ii → iv6 → I/5 → V
QA = ["Dmaj7", "E/D", "C#m7", "F#m7", "Bm7", "E7sus4", "Amaj7", "A7", "Dmaj7", "Dm6", "A/C#", "E7sus4"]      # 静かな場面（イ長調）
DA = ["A", "A/G", "D/F#", "Dm/F", "A/E", "F#m7", "Bm7", "E7sus4"]                 # Aメロ（イ長調）: ベースが半音と全音で下りていく
SC = []                                                                           # (名前, 調)


def scene(name, n, kind, chs, key):
    assert len(chs) == n, (name, n, len(chs)); SC.append((name, key)); S.scene(name, n, kind, chs)


scene("サビ1", 8, "chorus", CC, KC)
scene("遠い席", 12, "bridge", QA, KA)
scene("消しゴム", 12, "pre", ["F#m7", "F#m7/E", "D#m7b5", "Dmaj7", "C#m7", "F#7", "Bm7", "C#m7", "Dmaj7", "E", "G", "G"], KA)
scene("ドロップ1", 6, "break", ["F", "G/F", "Em7", "Am7", "Dm7", "G7sus4"], KC)
scene("早口1", 4, "verse", ["Am7", "Am7/G", "F#m7b5", "Fmaj7"], KC)
scene("フック", 8, "break", CC[:7] + ["E7sus4"], KC)
scene("名前", 12, "bridge", QA, KA)
scene("ひとりで帰る", 16, "verse", DA + DA[:7] + ["G"], KA)
scene("サビ2", 12, "chorus", CC + ["Dm7", "Em7", "Fmaj7", "G7sus4"], KC)
scene("ソロ1", 4, "solo", ["Am7", "F", "G", "E7"], KC)
scene("雨", 12, "verse", DA + ["Dmaj7", "Dm6", "A/C#", "G"], KA)
scene("ソロ2", 10, "solo", CC + ["Dm7", "E7sus4"], KC)
scene("にせの立ち上げ", 8, "pre", ["Bm7", "C#m7", "Dmaj7", "E", "Bm7", "C#m7", "Dmaj7", "E7sus4"], KA)
scene("初めて", 16, "verse", DA + DA, KA)
scene("早口2", 4, "verse", ["F#m7", "F#m7/E", "D#m7b5", "Dmaj7"], KA)
scene("止まる", 2, "bridge", ["G", "G"], KA)
scene("サビ3", 10, "chorus", CC + ["Fm6", "G7sus4"], KC)
scene("ソロ3", 6, "solo", ["Am7", "F", "C/E", "Dm7", "F", "E7sus4"], KC)
scene("返事を待つ", 8, "bridge", ["Dmaj7", "E/D", "C#m7", "F#m7", "Bm7", "Dm6", "A/C#", "E7sus4"], KA)
scene("倍の速さ", 8, "verse", DA[:7] + ["G"], KA)
scene("ドロップ2", 16, "break", CC + CC, KC)
scene("聞こえていた", 4, "bridge", ["Fmaj7", "Fm6", "C/E", "G7sus4"], KC)
scene("サビ4", 16, "chorus", CC + CC, KC)
scene("あしたも", 8, "pre", ["Fmaj7", "G/F", "Em7", "Am7", "Dm7", "Fm6", "C", "C"], KC)
scene("もどる", 2, "outro", ["C", "C"], KC)
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3
KEYOF = dict(SC)

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BSPEC = rock_bass_spec(0.165); BSPEC["ampDrive"] = 0.25                           # 人間「ベースの歪みがちょっと強いかも」→ 0.55 → 0.25
BSPEC["fx"] = [{"type": "eq", "low": 0, "mid": 4, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 1.5, "midHz": 2200, "high": 1}]
BASS = S.track("指弾きのベース", "bass", **BSPEC)
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.085, -0.6, tone="marshall-mid", drive=0.4)) for i in range(6)]      # v7: 0.04 → 0.085（測ったらギターはほかの音より 11〜17dB 小さく、ほぼ聞こえていなかった）。人間「クリーン系の和音が微妙」→ 浅い歪み
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.08, 0.6, tone="marshall-mid", drive=0.35)) for i in range(6)]
GM = [S.track(f"Lギター（ミュートの刻み）{i + 1}", "distGuitar", **{**rock_gtr_spec(0.04, -0.6, tone="marshall-mid", drive=0.4), "palmMute": "light"}) for i in range(3)]
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.14, 0.1))
SL, SR = G2.Strummer(GL, S, 29), G2.Strummer(GR, S, 47)
PF = {"type": "pluckfilter", "freq": 2000, "depth": 0.6, "rate": 30, "hold": 4}
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.055, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
ARP = S.track("シンセのかけ上がり（矩形波のプラック）", "lead", patch="kfbSquarePluck", volume=0.07, pan=0.2, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HOOK = S.track("フックのシンセ", "lead", patch="kfbTranceLead", volume=0.06, mono=True, pan=-0.1, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])
BELL = S.track("ベルの速い動き", "lead", patch="kfbMusicBox", volume=0.05, pan=-0.3, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
FXT = S.track("効果音（当たる音・逆回しのシンバル・きらめき）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
SWELL = [S.track(f"ふくらむ和音{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); FXH = {}


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))


def mel(b, s, up=0):
    """度数の旋律を、その場面の調の音名に。イ長調は 1＝A3、ハ長調は 1＝C4（up で1オクターブ上）"""
    k = KEYOF[S.scene_of(b)[0]]; return k.mel(s, oct=(3 if k is KA else 4) + up)


# ================= 歌（句ごとに、小節を | で区切って書く。句の形はくじで決まったもの）=================
BAD = []


def put(name, phrases):
    bars = S.sc(name); lines = []; texts = []
    for m, t in phrases:
        bl = [x.strip() for x in m.split("|")]; nn = sum(1 for x in " ".join(bl).split() if not x.startswith("R"))
        if t and nn != mora(t): BAD.append((name, t, nn, mora(t)))
        for x in bl: assert abs(sum(float(y.split(":")[1]) for y in x.split()) - 4) < 1e-6, (name, x)
        lines += bl
        if t: texts.append(t)
    assert len(lines) == len(bars), (name, len(lines), len(bars))
    ml = [x if x == "R:4" else mel(b, x) for b, x in zip(bars, lines)]
    for b, m in zip(bars, ml): V.bar(b, m)
    LY.flow(bars, ml, "/".join(texts), name)


P1 = "5:1 3':1.5 2':0.5 1':1 | 2':1 2':1 3':1.5 R:0.5"                            # サビ: 低い音から6度跳ぶ
P2 = "5:1 2':1.5 1':0.5 7:1 | 1':1 6:1 5:1.5 R:0.5"
P3 = "5:1 3':1.5 2':0.5 1':1 | 2':1 1':1 6:1.5 R:0.5"
P4 = "5:0.5 1':1.5 2':1 3':1 | 2':3.5 R:0.5"
put("サビ1", [(P1, "とどかなくても"), (P2, "すきでいさせて"), (P3, "きみはしらない"), (P4, "このおとを")])
put("遠い席", [("3':1.5 2':0.5 1':1 6:1 | 5:1 3:1 5:2 | R:4", "いちばんとおい"), ("2':1.5 1':0.5 6:1 5:1 | 3:1 2:1 3:2 | R:4", "せきにいるひと"),          # 高い音から下りてくる・3小節の句
               ("4':1.5 3':0.5 2':1 1':1 | 6:1 1':1 2':2 | R:4", "みんなふりむく"), ("3':1.5 2':0.5 1':1 6:1 | 5:1 6:1 1':2 | R:4", "わたしうつむく")])
put("消しゴム", [("R:3 3:1 | 5:1.5 5:0.5 6:1 5:1 | 3:1 2:2 R:1", "おちたけしゴム"), ("R:3 5:1 | 6:1.5 6:0.5 1':1 6:1 | 5:1 3:2 R:1", "ひろうゆびさき"),          # 1拍早く食って入る
                ("R:3 6:1 | 1':1.5 1':0.5 2':1 1':1 | 6:1 5:2 R:1", "ありがとのこえ"), ("R:3 1':1 | 2':1.5 2':0.5 3':1 2':1 | 2':3 R:1", "はじまるおと")])
RAP = lambda a, c: f"{a}:0.5 {a}:0.5 {a}:0.5 {a}:0.5 {a}:0.5 {a}:0.5 {c}:0.5 R:0.5"         # 同じ音を連打してから跳ぶ
put("早口1", [(RAP("5", "1'"), "なにかいわなきゃ"), (RAP("6", "2'"), "ことばがでない"), (RAP("6", "3'"), "かおがあついよ"), ("5:0.5 5:0.5 5:0.5 5:0.5 3':2", "ばれちゃうよ")])
put("名前", [("R:1.5 1:0.5 2:1 3:1 | 5:2 3:1 2:1 | 3:3 R:1", "なまえをよんだ"), ("R:1.5 2:0.5 3:1 5:1 | 6:2 5:1 3:1 | 5:3 R:1", "ふりむくかおが"),                    # 3小節の句（上がっていく）
             ("R:1.5 3:0.5 5:1 6:1 | 1':2 6:1 5:1 | 6:3 R:1", "おもいのほかに"), ("R:1.5 5:0.5 6:1 1':1 | 2':2 1':1 6:1 | 1':3 R:1", "やさしくわらう")])
T = lambda a, b_, c: f"{a[0]}:1.5 {a[1]}:0.5 {a[2]}:1 {a[3]}:1 | {b_[0]}:0.5 {b_[1]}:1.5 {b_[2]}:2 | {c}:2.5 R:1.5"
put("ひとりで帰る", [(T(("5", "5", "6", "5"), ("3", "5", "6"), "5"), "かんぺきなひとは"), (T(("6", "6", "1'", "6"), ("5", "6", "1'"), "2'"), "ひとりきりかえる"),      # 3小節の句 ×4 ＋ 4小節の句
                    (T(("1'", "1'", "2'", "1'"), ("6", "1'", "2'"), "3'"), "だれもさそわない"), (T(("3'", "2'", "1'", "6"), ("1'", "2'", "1'"), "6"), "そういいわらうの"),
                    ("5:1 6:0.5 1':1.5 2':1 | 3':2.5 2':1.5 | 1':1 2':1 3':2 | 2':3 R:1", "そのえがおがすきだよ")])
put("サビ2", [(P1, "とどかなくても"), (P2, "となりあるくの"), (P3, "きみはしらない"), (P4, "このおとを"), ("R:3 5:1 | 3':2 2':1 1':1 | 2':1 3':3 | R:4", "きこえないで")])
U = lambda a, b_, c, d: f"{a[0]}:1.5 {a[1]}:0.5 {a[2]}:2 | {b_}:4 | {c[0]}:0.5 {c[1]}:1.5 {c[2]}:2 | {d}:3 R:1"       # 4小節のばす長い句
put("雨", [(U(("3", "5", "6"), "5", ("6", "1'", "2'"), "1'"), "あめのかえりみち"), (U(("5", "6", "1'"), "2'", ("1'", "2'", "3'"), "2'"), "かさをさしだした"),
           (U(("6", "1'", "2'"), "3'", ("3'", "2'", "1'"), "2'"), "かたがふれそうで")])
W = lambda a, b_, c, d: f"{a[0]}:2 {a[1]}:1.5 {a[2]}:0.5 | {b_}:4 | {c[0]}:1 {c[1]}:0.5 {c[2]}:1.5 {c[3]}:1 | {d}:3 R:1"
put("初めて", [(W(("3'", "2'", "1'"), "6", ("5", "6", "1'", "2'"), "1'"), "はなしかけてくれた"), (W(("2'", "1'", "6"), "5", ("3", "5", "6", "1'"), "6"), "ひとははじめてだと"),
               (W(("3'", "2'", "1'"), "2'", ("6", "1'", "2'", "3'"), "2'"), "わらうきみをみてた"), (W(("1'", "2'", "3'"), "3'", ("3'", "2'", "1'", "2'"), "1'"), "とおいのはわたしだ")])
put("早口2", [(RAP("5", "1'"), "いまならいえる"), (RAP("6", "2'"), "のどまできてる"), (RAP("1'", "3'"), "あとひとことだ"), ("2':0.5 2':0.5 2':0.5 2':0.5 3':2", "いうんだよ")])
C_ = lambda a, b_: f"R:1 {a[0]}:1 {a[1]}:1 {a[2]}:1 | {b_[0]}:0.5 {b_[1]}:0.5 {b_[2]}:1 {b_[3]}:2"              # 休みから入って最後をのばす
put("サビ3", [(C_(("5", "3'", "2'"), ("1'", "1'", "2'", "3'")), "とどかなくても"), (C_(("5", "2'", "1'"), ("7", "7", "1'", "5")), "すきといわせて"),
              (C_(("5", "3'", "2'"), ("1'", "1'", "2'", "6")), "きみにきこえる"), (C_(("5", "1'", "2'"), ("3'", "3'", "2'", "2'")), "くらいのおとで"),
              ("R:1 1':1 1':1 2':1 | 2':3 R:1", "すきです")])
put("返事を待つ", [("R:2 1:1 6:1 | 5:2 3:1 5:1 | 6:4 | R:4", "へんじをまつ"), ("R:2 2:1 1':1 | 6:2 5:1 6:1 | 1':4 | R:4", "ときがとまる")])                      # 低い音から6度以上跳ぶ
put("倍の速さ", [("5:0.5 5:0.5 6:1 5:0.5 3:0.5 5:1 | 6:1 1':1 2':2 | 3':0.5 3':0.5 2':1 1':0.5 2':0.5 3':1 | 2':0.5 1':0.5 5:1 1':2 | 2':3 R:1", "きみのくちがうごくわたしもだよときこえた"),   # 5小節の句
                ("6:1 1':1 2':1 3':1 | 3':1 2':1 1':2 | 2':3 R:1", "おとがうるさいよ")])
put("聞こえていた", [("R:1 5:1 6:1 1':1 | 2':2 1':1 6:1 | 1':3 R:1 | R:4", "きこえていたの")])
SH = lambda p: "{}:1 {}:0.5 {}:1.5 R:1".format(*p.split())                      # 1小節の短い句をたたみかける
put("サビ4", [(SH("5 6 1'"), "とどく"), (SH("6 1' 2'"), "とどく"), (SH("7 2' 3'"), "きみに"), (SH("2' 3' 2'"), "とどく"), (SH("5 6 1'"), "すきが"), (SH("5 1' 2'"), "すきが"), (SH("1' 2' 3'"), "いまね"), (SH("3' 3' 2'"), "とどく"),
              (P1, "とどいたんだね"), (P2, "すきでいるから"), (P3, "いまはふたつの"), (P4, "むねのおと")])
Z = lambda a, b_, c, d: f"{a[0]}:0.5 {a[1]}:1.5 {a[2]}:2 | {b_}:4 | {c[0]}:1.5 {c[1]}:0.5 {c[2]}:1 {c[3]}:1 | {d}:3 R:1"
put("あしたも", [(Z(("5", "1'", "2'"), "3'", ("2'", "1'", "6", "1'"), "2'"), "おはようをあしたも"), (Z(("6", "1'", "2'"), "2'", ("3'", "2'", "1'", "2'"), "1'"), "いわせてねとなりで")])
put("もどる", [(P1, "とどいたよいま")])                                             # 始まりと同じ音にもどる（言葉を1つ変える）
assert not BAD, BAD


# ================= 伴奏 =================
def bass(b, pat="r---------------"):
    r = low(S.chords[b], "E1"); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + {'r': 0, '5': 7, 'R': 12}[pat[i]])}:{L * 0.25:g}"); i += L
    BASS.bar(b, " ".join(out))


def saw(b, pat="x---------------", center=65):
    v = sorted(voice(S.chords[b], center, 5))
    for j in range(5):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(v[j])}:{L * 0.25:g}"); i += L
        SAW[j].bar(b, " ".join(out))


def swell(b):
    v = sorted(voice(S.chords[b], 67, 3))
    for j in range(3): SWELL[j].bar(b, f"{N(v[j])}:4")


def arp(b, k=0):
    """シンセのかけ上がり。テンポ 180 なので 8分（k が 5 以上のときだけ 16分）"""
    t = sorted(voice(S.chords[b], 74, 4)); u = t + [t[0] + 12, t[1] + 12]
    if k >= 5:
        o = ([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3], [4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5])[k % 2]; ARP.bar(b, " ".join(f"{N(u[x])}:0.25" for x in o)); return
    o = ([0, 2, 1, 3, 2, 4, 3, 5], [4, 3, 2, 1, 0, 1, 2, 3], [0, -1, 2, 3, -1, 4, 3, -1], [0, 1, 2, -1, 4, 5, -1, -1], [5, -1, 4, -1, 3, 2, -1, 0])[k % 5]
    ARP.bar(b, " ".join("R:0.5" if x < 0 else f"{N(u[x])}:0.5" for x in o))


def bell(b, k=0):
    BELL.bar(b, mel(b, ("R:2 5':0.5 3':0.5 2':0.5 1':0.5", "R:2 3:0.5 5:0.5 6:0.5 1':0.5", "R:2.5 3':0.5 2':0.5 5:0.5", "R:3 1':0.5 3':0.5")[k % 4], 1))


TR = [None]


def gtr(b, patL=None, patR=None, sung=None, feel=8, feelL="down"):
    """左＝低い側の形（8分をぜんぶダウン）、右＝まん中の弦の三和音（8分で下・上）。型の - は鳴らしたまま、. は止める"""
    c = S.chords[b]
    if patL: SL.bar(b, G2.with_space(patL, sung, keep=(0, 8)) if sung else patL, G2.low_shape(c), feel=feelL)
    if patR: TR[0] = G2.triad(c, TR[0]); SR.bar(b, G2.with_space(patR, sung, keep=(0, 8)) if sung else patR, TR[0], feel=feel)


def riff(b, k=0):
    """左のギターの単音リフ（根音・5度・オクターブ）。歌の下で和音を鳴らしつづけない場面で使う"""
    r = low(S.chords[b], "E1") + 12; f5, o8 = N(r + 7), N(r + 12); r = N(r)
    SL.line(0, S.bar_beat(b), (f"{r}:0.5! {r}:0.5 {f5}:0.5 {r}:0.5 {o8}:1! {f5}:0.5 {r}:0.5", f"{r}:1! {f5}:0.5 {o8}:0.5 {f5}:0.5 {r}:0.5 {f5}:1", f"{r}:0.5! {r}:0.5 {o8}:1! {f5}:0.5 {r}:0.5 {r}:1", f"{r}:1.5! {f5}:0.5 {o8}:0.5 {f5}:0.5 {r}:1")[k % 4])


def garp(b, k=0):
    """右のギターのアルペジオ（三和音を1本ずつ。鳴らしたまま）"""
    TR[0] = G2.triad(S.chords[b], TR[0]); G2.arp(SR, b, ("0---1---2---1---", "0---2---1---2---", "0-1-2---1---2---")[k % 3], TR[0])


import random as _r
RNG = _r.Random(29)


def deco(b):
    """コードの飾り（見本の7）: 右のギターの三和音の3度を、2拍めで4度に上げ、3拍めで戻す（sus4 → 3度）"""
    third = G2.chord_info(S.chords[b])[1]; sh = sorted(TR[0])
    for k, (st_, m) in enumerate(sh):
        if third is not None and m % 12 == third:
            up = m + (1 if (m - G2.chord_info(S.chords[b])[0]) % 12 == 4 else 2); SR.hammer(b, 4, k, up); SR.hammer(b, 8, k, m); return


def octs(b, line):
    """オクターブ奏法（見本の4）: 右のギターが、旋律を1オクターブはなれた2本の弦で弾く"""
    G2.octaves(SR, 2, 4, S, b, mel(b, line, -1))


def stops2(b):
    """2本の弦の合いの手（見本の8）: 小節の後半に、三和音の上2本を短く2回"""
    for st_, m in sorted(TR[0], key=lambda x: x[1])[-2:]: SR.line(st_, S.bar_beat(b) + 2, f"{N(m)}:0.5! R:0.5 {N(m)}:0.5 {N(m)}:0.5")


def palm8(b, pat="M-m-m-m-M-m-m-m-"):
    """ミュートの刻み（見本の3）: 左の低い弦（やわらかめのミュート）"""
    G2.palm(GM, S, b, pat, G2.low_shape(S.chords[b]), RNG)


# v7（2026-11-24）: 人間「ギターの音ちゃんと出てる？」→ ギターだけ／ギターぬきを書き出して測ったら、ほぼ聞こえていなかった（音量を約2倍に、のばす和音を少し下げた）。
#   人間「ギターの弾き方1ぐらいのシンプルなのを上手く使えばいいんじゃないかな」→ 全場面を見本の1（8分のかき鳴らし）に。場面で変えるのは、型の回し方・歌のあいだの間・白玉・キメだけ。
# v6（2026-11-23 夜）: 人間「ギターの弾き方別の良いのないかな？あった気がするんだが」→ 11月19日に学んだ弾き方の見本（docs/sound/guitar-playing-study.md）を場面ごとに使い分ける。
#   人間「2つめ（16分のカッティング）以外は使えるから。使って」→ 1 かき鳴らし・3 ミュートの刻みと白玉・4 オクターブ奏法・5 単音リフとキメ・6 アルペジオ・7 コードの飾り・8 裏打ちと合いの手 を場面ごとに使う。
#   v5 までの型は「D...D.U.」のように . （止める）で書いていて、弾くたびに音を止めていた。- （鳴らしたまま）に直した。
G8 = ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-", "D-d-d-D-d-D-d-d-", "D-D-d-d-D-d-d-d-")          # 左: 8分をぜんぶダウン（強い所が 3・3・2 など）
G8b = ("D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-", "D-U---U-D-U-D-U-", "D---D-U---U-D-U-")         # 右: 8分で下・上（空振りでノリを作る）
OFFB = "--U.--U.--U.--U."                                                                     # 右: 裏打ち（「と」だけ短く）
HKC = ("3':1.5 2':0.5 1':1 5:1", "2':1.5 1':0.5 7:1 5:1", "7:0.5 2':0.5 3':1 5':2", "3':1 5':1 3':2", "4':1.5 3':0.5 2':1 6:1", "4':1 2':1 1':2", "3':0.5 5':0.5 3':1 2':1 1':1", "2':3 R:1")
HKC2 = ("5':1 3':0.5 2':0.5 1':2", "5':1 2':0.5 1':0.5 7:2", "5':0.5 3':0.5 2':0.5 7:0.5 2':2", "5':1 3':1 6':2", "6':1 4':0.5 2':0.5 6:2", "4':1 2':1 4':2", "5':0.5 3':0.5 1':1 3':1 5':1", "5':3 R:1")
SOLO1 = ("6:1 1':0.5 3':0.5 5':2", "4':0.5 3':0.5 1':1 6:2", "2':1 5':1 4':1 2':1", "3':3 R:1")
SOLO3 = ("3':1.5 2':0.5 1':1 6:1", "6:0.5 1':0.5 4':1 3':2", "5':1 3':0.5 1':0.5 5:2", "4':1.5 2':0.5 6:1 2':1", "6':1 5':0.5 4':0.5 1':2", "3':3 R:1")
H16, H16o, H8, H8o = "XxxxXxxxXxxxXxxx", "XxxxXxxxXxxxXxO.", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.O."
FOURK, SN, SNg = "X...X...X...X...", "....X.......X...", "....X..o.o..X..."
HB1, HB2, HB3 = "X..X............", "X..X....X..X....", "X..X..X..X..X..X"       # 胸の音（トク、トク）: ゆっくり → 速く → もっと速く
NO = "................"


def fill(b, kind):
    """フィル 5種。0: スネア→タム2拍／1: スネア1拍／2: スネア2つとタム3つ／3: タムを高い方から／4: 小節まるごとタム回し"""
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.set(b, "X.......X.......", "x.x.X...........", NO); D.tom(b, "R:1.5 C4:0.5 C4:0.5 A3:0.5 A3:0.5! F3:0.25! F3:0.25! D3:0.5!")


def hook(b, line, gtr_too=False, up=0):
    HOOK.bar(b, mel(b, line, up))
    if gtr_too: LEAD.bar(b, mel(b, line, up))


def full(b, i, hat=H16, kick=FOURK, sn=SN, sung=None, sawp="x-------x-------", clap=True, k=0, offb=False):
    """全員の場面の土台"""
    D.set(b, kick, sn, hat); bass(b, ("r-------r-----5-", "r-----R---r-----", "r---------r---r-", "r---5---r---R---")[(i + k) % 4]); saw(b, sawp); gtr(b, G8[(i + k) % 4], G8b[(i + k) % 4], sung=sung)
    if clap: CLP.bar(b, "R:1 B4:1 R:1 B4:1")


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1; sung = G2.sung_slots(V, S, b)
    if n == "サビ1":                                                     # 始まり: 伴奏なしで歌1句（2小節）→ 全員
        if i < 2:
            if i == 1: D.set(b, NO, NO, NO); fill(b, 0); fxh(b, 2, "rev", 2)
            continue
        full(b, i, H16o if odd else H16, sung=sung); arp(b, i)
        if i == 2: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 3)
    elif n == "遠い席":                                                  # 静か: のばす和音とベル、胸の音（ゆっくり）
        saw(b, "x---------------", 62); D.set(b, HB1 if i % 2 == 0 else NO, NO, NO)
        if i == 0: fxh(b, 0, "down", 2)
        if i % 3 == 2: bell(b, i // 3)
        if i >= 6: bass(b, "r---------------")
        if i >= 9: arp(b, 2)
    elif n == "消しゴム":                                                # 半分の速さ → 4つ打ち。最後はフィルでドロップへ
        saw(b, "x---------------" if i < 6 else "x-------x-------", 62 + i // 2); bass(b, "r---------------" if i < 6 else "r-------r-------")
        D.set(b, "X.......X......." if i < 6 else FOURK, "........X......." if i < 6 else SN, H8 if i < 6 else H16)
        if i >= 6: gtr(b, "D-------D-------", G8b[i % 4], sung=sung); arp(b, i % 2)      # 左は白玉、右はかき鳴らし＋コードの飾り
        if i == 5: fill(b, 1)
        if i >= 10: FX.bar(b, "C5:4"); swell(b)
        if last: fill(b, 4); fxh(b, 2, "rev", 2)
    elif n == "ドロップ1":                                               # フックをシンセとリードギターで
        full(b, i, H8o if odd else H8, sawp=("x--x--x---x--x--", "x-----x---x-----")[i % 2], offb=True); hook(b, (HKC[0], HKC[1], HKC[2], "3':1 1':1 6:2", HKC[4], "2':3 R:1")[i], True)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 2)
    elif n in ("早口1", "早口2"):                                        # 頭だけ打って止まる。手びょうしとプラック
        D.set(b, "X.....X........." if not last else "X...X...X.X.....", "............X..." if not last else "....X...X.X.XXXX", NO); bass(b, "r-----r---------"); CLP.bar(b, "R:1 B4:1 R:1 B4:0.5 B4:0.5"); arp(b, 3)
        gtr(b, "D---------------", "D---------------")
        if last: FX.bar(b, "C5:4")
    elif n == "フック":                                                  # シンセだけのフック、16分のハイハット。最後の和音でイ長調へ戻る
        D.set(b, FOURK, SNg, H16o if odd else H16); bass(b, ("r--r--r---------", "r-------r-----5-")[i % 2]); saw(b, "x-------x-------"); arp(b, 5 + i % 2); hook(b, HKC[i] if i < 7 else "3':3 R:1"); gtr(b, G8[i % 4], G8b[i % 4])      # 左は白玉、右はオクターブ奏法でフック
        if i == 0: crash(D, b, "C2", 4)
        if last: fill(b, 1)
    elif n == "名前":                                                    # 静か: 胸の音が毎小節に
        saw(b, "x---------------", 62); D.set(b, HB1, NO, NO if i < 6 else "....x.......x..."); bass(b, "r---------------")
        if i == 0: fxh(b, 0, "kira", 1)
        if i % 3 == 2: bell(b, i // 3 + 1)
        if i >= 6: arp(b, 3)
        if last: fill(b, 2)
    elif n == "ひとりで帰る":                                            # バンドのAメロ: ベースが下りていく。ギターは歌の間をあける
        D.set(b, ("X.....X...X.....", "X.........X..X..", "X.....X.....X...", "X..X......X.....")[i % 4], SNg, H8o if i % 4 == 3 else H8); bass(b, ("r-------r-----5-", "r---------r-----", "r-----r---------", "r-------r---R---")[i % 4])
        gtr(b, G8[i % 4], G8b[(i + 2) % 4], sung=sung)      # 左は単音リフ、右は三和音のかき鳴らし（歌のあいだは間）
        if i >= 8: saw(b, "x---------------", 62); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i == 0: crash(D, b, "C2", 4)
        if i == 7: fill(b, 1)
        if i >= 14: FX.bar(b, "C5:4")
        if last: fill(b, 0); fxh(b, 2, "rev", 2)
    elif n in ("サビ2", "サビ3"):
        ext = i >= 8
        full(b, i, H16o if odd else H16, sung=sung, sawp="x-------x-------" if not ext else "x---------------", k=1 if n == "サビ3" else 0); arp(b, 5 + i % 2 if n == "サビ3" else i)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 7 and L > 8: fill(b, 3 if n == "サビ2" else 1)
        if last: fill(b, 0 if n == "サビ2" else 4)
    elif n == "ソロ1":
        full(b, i, H8, kick="X.....X...X.....", sn=SNg, k=2); LEAD.bar(b, mel(b, SOLO1[i]))
        if i == 0: crash(D, b, "C2", 4)
        if last: fill(b, 2)
    elif n == "雨":                                                      # 長い句: 半分の速さ。のばす和音と、ぽつぽつのプラック
        D.set(b, "X.......X.......", "........X.......", H8); bass(b, "r-----------r---"); saw(b, "x---------------", 64); arp(b, 2 + i % 3)
        if i % 4 == 3: bell(b, i // 4)
        if i >= 4: gtr(b, None, "D-------D-U-----", sung=sung)                                    # 右のギターのアルペジオ
        if last: fill(b, 3); fxh(b, 2, "rev", 2)
    elif n == "ソロ2":                                                   # シンセのソロ（フックの別の形）。最後の2小節で静かに
        if i < 8:
            D.set(b, FOURK, SN, "..x...x...x...x."); bass(b, ("r--r--r---------", "r-------r-----5-")[i % 2]); saw(b, "x--x--x---x--x--" if not odd else "x-----x---x-----"); gtr(b, G8[i % 4], G8b[(i + 1) % 4]); hook(b, HKC2[i]); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
            if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
            if i == 7: fill(b, 1)
        else: saw(b, "x---------------", 62); bass(b, "r---------------"); hook(b, ("4':1 2':1 6:1 2':1", "3':3 R:1")[i - 8]); D.set(b, HB2, NO, NO)
    elif n == "にせの立ち上げ":                                          # 盛り上げて…落とす（言おうとして、言えない）
        saw(b, "x-------x-------" if i < 4 else "x---x---x---x---", 62 + i); bass(b, "r-------r-------"); arp(b, i % 2 if i < 4 else 5 + i % 2); gtr(b, G8[i % 4] if i >= 2 else None, G8b[i % 4] if i >= 4 else None)
        D.set(b, "X.......X......." if i < 2 else FOURK, NO if i < 2 else ("....x.......x..." if i < 4 else "x...x...x...x..." if i < 6 else "x.x.x.x.x.x.x.x."), H8 if i < 4 else H16)
        if i >= 4: FX.bar(b, "C5:4"); swell(b)
        if last: D.set(b, "X.X.X.X.X.X.X.X.", "xxxxxxxxXXXXXXXX", NO); hat_roll(HATR, b, 1)
    elif n == "初めて":                                                  # 落ちる: 前半は和音と歌と胸の音だけ。後半でベースとドラム（半分の速さ）
        saw(b, "x---------------", 62)
        if i == 0: fxh(b, 0, "down", 2)
        if i < 8: D.set(b, HB2, NO, NO); (i % 4 == 3 and bell(b, i // 4))
        else: D.set(b, "X.......X.....X.", "........X.......", H8); bass(b, "r-----------r---"); arp(b, 2 + i % 3); gtr(b, None, "D-------D-U-----", sung=sung)
        if last: fill(b, 1)
    elif n == "止まる":                                                  # 和音を1回。あとは胸の音だけ（速い）
        D.set(b, HB3, NO, NO)
        if i == 0: saw(b, "x---------------", 62); bass(b, "r---------------"); gtr(b, "D---------------", "D---------------"); fxh(b, 0, "sub", 2)
        else: fxh(b, 2, "rev", 2)
    elif n == "ソロ3":
        full(b, i, H16, kick=FOURK, sn=SNg, k=1); LEAD.bar(b, mel(b, SOLO3[i]))
        if i == 0: crash(D, b, "C2", 4)
        if last: D.set(b, "X...............", NO, NO)
    elif n == "返事を待つ":                                              # いちばん静か: 和音と胸の音
        saw(b, "x---------------", 60); D.set(b, HB2 if i < 4 else HB3, NO, NO)
        if i == 0: fxh(b, 0, "down", 2)
        if i >= 4: bass(b, "r---------------"); swell(b)
        if i % 4 == 3: bell(b, 2 + i // 4)
        if last: FX.bar(b, "C5:4"); fxh(b, 2, "rev", 2)
    elif n == "倍の速さ":                                                # キックとスネアが倍の速さで交互に
        D.set(b, "X...X...X...X...", "..X...X...X...X.", H16); bass(b, "r---r---r---r---" if not odd else "r---r---r-5-R---"); saw(b, "x-------x-------"); gtr(b, "D-D-D-D-D-D-D-D-", G8b[i % 4], sung=sung)                  # 左は8分をぜんぶ強いダウン、右は裏打ち; arp(b, 5 + i % 2)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 4); fxh(b, 2, "rev", 2)
    elif n == "ドロップ2":                                               # 前半: フック。後半: 形を変える（半分の速さの重いドラム・フックは別の形で1オクターブ上）
        if i < 8:
            full(b, i, H16o if odd else H16, sawp=("x--x--x---x--x--", "x-----x---x-----")[i % 2], offb=True); hook(b, HKC[i], True)
            if i == 7: fill(b, 3)
        else:
            D.set(b, "X.....X.X.......", "........X.......", "X...x...X...x.O."); bass(b, "r--r--r---------" if not odd else "r-----------R-5-"); saw(b, "x---------------" if not odd else "x-------x-x-x---"); gtr(b, "D-------D-d-D---", "D---D-U-----D-U-")
            hook(b, HKC2[i - 8], True); arp(b, 5 + i % 2); CLP.bar(b, "R:2 B4:1 R:1")
            if last: D.set(b, "X...............", NO, NO)
        if i in (0, 8): crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
    elif n == "聞こえていた":
        saw(b, "x---------------", 62); swell(b); D.set(b, HB3, NO, NO)
        if i == 0: fxh(b, 0, "kira", 1)
        if last: fill(b, 0); FX.bar(b, "C5:4"); fxh(b, 2, "rev", 2)
    elif n == "サビ4":                                                   # 前半: 短い句に全員が合いの手（3拍打って1拍あける）。キックは胸の音の形。後半: 全員
        if i < 8:
            D.set(b, HB3, "....X.......X...", "x.x.x.x.x.x....."); bass(b, "r---r---r---...."); saw(b, "x---x---x---...."); gtr(b, "D---D---D---....", "D---D---D---...."); arp(b, 3)
            if i == 7: D.set(b, HB3, "....X...X.X.....", NO); fill(b, 0)
        else:
            full(b, i, H16o if odd else H16, kick="X..X..X..X..X..X" if not odd else FOURK, sung=sung); arp(b, 5 + i % 2); (odd and i != 15 and hook(b, ("R:2.5 3':0.5 5':1", "R:3 2':0.5 3':0.5", "R:2.5 5':0.5 6':1")[(i // 2) % 3]))
            if last: fill(b, 2)
        if i in (0, 8): crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
    elif n == "あしたも":                                                # 長い句: 全員 → 少しずつ抜ける
        saw(b, "x-------x-------" if i < 4 else "x---------------"); bass(b, "r-------r-----5-" if i < 4 else "r---------------")
        D.set(b, FOURK if i < 4 else ("X.......X......." if i < 6 else HB1), SN if i < 4 else ("........X......." if i < 6 else NO), H8 if i < 6 else NO)
        if i < 4: gtr(b, G8[i % 4], G8b[i % 4], sung=sung); arp(b, i)
        if i == 0: crash(D, b, "C2", 4)
        if i in (5, 7): bell(b, i)
    elif n == "もどる":                                                  # 始まりと同じ: 伴奏なしで歌1句。胸の音だけ
        D.set(b, HB1, NO, NO)
        if i == 1: fxh(b, 2, "kira", 1)

for b_, hs in FXH.items(): FXT.bar(b_, fx_bar(*hs))
SL.end(S.nb); SR.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース×ダンス×ロックの恋の歌（180・イ長調 ⇄ ハ長調・約5分）。高嶺の花（見えていても手が届かない、あこがれの人）がコンセプト。"
          "場面の並び・長さ・旋律の句の形・始まり方・終わり方は、くじ（form_dice.py・種 27011）で決めた。伴奏なしの歌1句で始まり、同じ1句で終わる。胸の音のキックが、話が進むほど速くなる。自作")
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
    harmony(path, S, [("サビ4", 8, None, KC)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
# 静かな場面を本当に静かにする（v4 の1回めは、静かな場面もサビも -15〜-16dB で横ならびだった）。伴奏だけ下げる。歌は下げない
QUIET = {"遠い席": 0.6, "名前": 0.65, "初めて": 0.62, "止まる": 0.7, "返事を待つ": 0.55, "聞こえていた": 0.65, "雨": 0.8, "あしたも": 0.85, "もどる": 0.6}
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in QUIET.items():
        for j, b in enumerate(S.sc(name)):
            if name == "初めて" and j >= 8: k = 0.8
            g[b] = round(min(g[b], 1.0) * k, 4)
    p_["barGain"] = g[:S.nb]
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
