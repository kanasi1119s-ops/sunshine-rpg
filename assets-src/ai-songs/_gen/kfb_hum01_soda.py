# HUM 01「はんぶんこサイダー」Half-and-Half Soda（仮）— Kawaii future bass のアニソン。4分の4・150・ヘ長調。152小節・約4分3秒。
# v2（2026-11-25）人間「ランダムだけど合わない部分は合うように引き直すようにしようか。あとリズムの取り方も変えれるようにしよう。なんか、グルーブがのっぺりしていて感じられないんだよね」
#   1) 形: くじ（form_dice.py）が、合わない所だけ引き直すようになった。この曲では5か所:
#        最初の「止まる」→「楽器のソロ」8／「にせの立ち上げ」6 →「B」6／「立ち上げ」16 →「ドロップ」4（上げたのに山へ行かず、22小節も歌が出なかった）／2つめの「にせの立ち上げ」8 →「立ち上げ」8（次がフックなので、落とさずに上げる）
#   2) リズムの取り方: くじで「主＝はねる16分（bounce）」「静かな場面＝2ステップ（twostep）」。型は groove_lib.py（中身は tools/vt3/grooves.json）。
#        v1 がのっぺりだった元: サビがずっと「4つ打ち＋2・4拍のスネア＋強さ2段のハイハット」で、キック・ベース・和音が毎小節同じ所。ずれ（はね・あと乗り）も書いていなかった。
#        v2: キックは食いこむ形を4小節で1まわり、ハイハットは強さ3段＋開く音、スネアにゴースト、ベースはキックと同じ所で打つ、16分のウラを少し後ろへ（はね 0.5）、スネアとベースはあと乗り。
#
# 2026-11-25 人間が鼻歌（スマホの録音・78秒）を送ってきた。「これをただ大元にするだけで、あとはアレンジして変えて、曲として成り立つようにしてください。声が低いので2オクターブあげて。
#   曲は4分ぐらいで kawaiiFutureベースのアニソンに。コンセプトは高校生の甘酸っぱい記憶」
#   鼻歌の読み取り: tools/hum/hum_to_melody.py（ホ長調として読めた。音階への合い具合 0.63・テンポはあやしい）。読み取りから、くり返し出てくる動きを種にした:
#     種1「6, 7, 1 —」（下から主音へ上がってのばす。読み取りの 1〜3・28〜30小節め）／種2「4 3 2 1」（2・5〜6・39小節め）／種3「2 2 2 3 | 3 2 7, 5,」（10〜11小節め）／
#     種4「3 4 5 6 —」（順に上がってのばす。13〜14・20・27小節め）／種5「6 4 2 5, 7, 1」（下りて主音に落ち着く。28〜30小節め）
#   リズム・並べ方・和音・歌詞は新しく書いた。2オクターブ上はテトの音域（A3〜E5）を超えるので、歌は1オクターブ上＋半音（ヘ長調。1＝F4）。2オクターブ上の高さは、フックのシンセが弾く。
#   骨組みはくじ（tools/vt3/form_dice.py --skeleton 51430 240 150 --min-chorus 3 --not-start 手びょうし → 種 51433）。サビが1回の形と、前の曲と同じ始まり方は引き直した。
#   人が決めた所: サビの旋律は1つ（毎回同じ出だし）。サビの和音は IV → V/IV → ii → I/3 → IV → V/IV → III7 → vi（最後が短調の和音）。この曲だけのもの＝炭酸の泡の効果音。
# 物語（高校生の甘酸っぱい記憶）: 自転車置き場のかげで、ひとつの缶の炭酸をふたりで飲んだ夏。言おうとして言えなかった「好き」を、泡といっしょに飲みこんだ。今も缶を開けるたび、あの日へ戻る。
# 歌詞: 曲名の言葉（はんぶんこ・サイダー）は歌わない。声: キュート 1 種類。歌をなぞるリードは入れない。オーケストラの楽器・アコーディオン・バンジョーは使わない。
from vocalo_lib import *
import gtr2_lib as G2
from groove_lib import Groove
import re as _re

S = Song("32", "soda", "はんぶんこサイダー（仮）", "Half-and-Half Soda", 150, 4, "F", "major", "カワイイ・フューチャーベースのアニソン（ボカロ）")
S.kit = "crocell-punch"; S.flags = S.flags + " --space room --space-wet 0.08"
KFm = Key("F", "major")
CH = ["Bbmaj7", "C/Bb", "Gm7", "F/A", "Bbmaj7", "C/Bb", "A7", "Dm7", "Gm7", "C7", "Dbmaj7", "Eb"]      # サビ（12小節。8小節の時は前の8つ）
SC = []


def scene(name, n, kind, chs, key=KFm):
    assert len(chs) == n, (name, n, len(chs)); SC.append((name, key)); S.scene(name, n, kind, chs)


scene("始まり", 4, "break", ["Bb", "Bb", "C", "C"])
scene("ソロ", 8, "intro", CH[:8])
scene("サビ1", 12, "chorus", CH)
scene("語り", 16, "verse", ["F", "Am7", "Bb", "Dm7", "C", "Bb", "Gm7", "C7", "F", "Dm7", "Bb", "C", "Bb", "C", "Dm7", "C7sus4"])
scene("サビ2", 12, "chorus", CH)
scene("鐘", 6, "bridge", ["Dm7", "C", "Bb", "Gm7", "C7sus4", "C7"])
scene("止まる2", 2, "bridge", ["F", "F"])
scene("B0", 6, "pre", ["Gm7", "Am7", "Bb", "Dm7", "Gm7", "C7sus4"])
scene("ドロップ", 4, "break", CH[:4])
scene("早口", 8, "verse", ["Gm7", "C7", "Am7", "Dm7", "Gm7", "C7", "Dbmaj7", "Eb"])
scene("フック1", 4, "break", CH[:4])
scene("B1", 6, "pre", ["Gm7", "Gm7", "Am7", "Am7", "Bb", "C7sus4"])
scene("サビ3", 8, "chorus", CH[:8])
scene("B2", 4, "pre", ["Gm7", "Am7", "Bb", "C7sus4"])
scene("立ち上げ", 8, "pre", ["Bb", "Bb", "C", "C", "Db", "Db", "Eb", "Eb"])
scene("フック2", 10, "break", CH[:4] * 2 + ["Gm7", "C7sus4"])
scene("サビ4", 8, "chorus", CH[:8])
scene("A", 10, "verse", ["F", "Am7", "Bb", "Dm7", "C", "Bb", "Gm7", "Am7", "Bb", "C7sus4"])
scene("サビ別", 12, "chorus", ["Dm7", "C/E", "Gm7", "F/A", "Bbmaj7", "C/Bb", "A7", "Dm7", "Gm7", "C7", "Dbmaj7", "Eb"])
scene("もどる", 4, "outro", ["Bb", "C", "F", "F"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3
KEYOF = dict(SC)

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
SUB = S.track("シンセの低いベース", "bass", patch="kfbSub", volume=0.066, pan=0, duck=0.12)
GSP = lambda v, p: {**{k: x for k, x in rock_gtr_spec(v, p).items() if k != "guitarTone"}, "release": 0.9}
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **GSP(0.125, -0.6)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **GSP(0.12, 0.6)) for i in range(6)]
# v3（2026-11-27）人間「1と3も39で」→ ギターを全部、見本の39番（instrument guitar・amp crystal＝透き通るクリーン・コーラスなし）に。録音のギター（diGuitar）は掛けない（掛けると高い音が減って39番の音でなくなる）。
#   大きさは、前の版のギターと同じ位置になるよう、目印の音で測って合わせた（tools/vt3/balance_check.py）
import os as _os
C39 = lambda v, pn, **k: {"volume": v, "pan": pn, "amp": "crystal", "chorus": 0, "humanPitch": 0, "noScoop": True, **k}
for _trs, _pn, _v in ((GL, -0.6, 0.19), (GR, 0.6, 0.17)):      # 大きさ: ベースとの差が前の版と同じになるように（0.125 のままだと、前の版より 2〜4dB 小さかった）
    for _t in _trs: _t.inst = "guitar"; _t.spec.clear(); _t.spec.update(C39(_v, _pn))
SL, SR = G2.Strummer(GL, S, 34), G2.Strummer(GR, S, 55); SL.gap = SR.gap = 0.0
PF = {"type": "pluckfilter", "freq": 2000, "depth": 0.6, "rate": 30, "hold": 4}
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.07, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=[PF] + rack_supersaw(lp=4000, wide=0.5)) for i in range(5)]
PAD = [S.track(f"やわらかいパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.06, pan=(-0.2, 0.2, 0)[i], reverb=0.3) for i in range(3)]
EP = [S.track(f"ピアノ{i + 1}", "piano", volume=0.036, pan=(-0.25, 0, 0.25, 0.1)[i], reverb=0.2, sustain=0.9, fx=rack_piano()) for i in range(4)]
ARP = S.track("シンセのかけ上がり（矩形波のプラック）", "lead", patch="kfbSquarePluck", volume=0.068, pan=0.2, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HOOK = S.track("フックのシンセ（夢のようなリード）", "lead", patch="kfbDreamLead", volume=0.065, mono=True, pan=-0.1, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}])
BELL = S.track("オルゴール", "lead", patch="kfbMusicBox", volume=0.05, pan=-0.3, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}])
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.05, pan=0, reverb=0.3)
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
FXT = S.track("効果音（当たる音・逆回しのシンバル・きらめき・泡）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.25, modulate=False)
HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
SWELL = [S.track(f"ふくらむ和音{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); FXH = {}


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))


def mel(b, s, up=0):
    return KEYOF[S.scene_of(b)[0]].mel(s, oct=4 + up)                              # ヘ長調は 1＝F4。歌は 4,（B♭3）〜 6（D5）


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


# サビの旋律は1つ（鼻歌の種4「順に上がってのばす」→ 種5「下りて主音に落ち着く」→ 種4 → 種2「4 3 2 1」）。出だしは低い音から6度跳ぶ
C8 = "5,:0.5 3:1 4:1 5:1.5 | 6:3 R:1 | 6:1.5 4:0.5 2:1 5,:1 | 7,:1 1:2.5 R:0.5 | 5,:0.5 3:1 4:1 5:1.5 | 6:2 5:1 3:0.5 R:0.5 | 4:1.5 3:0.5 2:1 1:1 | 1:3 R:1"
C4 = "2:0.5 2:1.5 2:1 3:1 | 3:2 2:1 7,:1 | 5,:1.5 1:0.5 b3:1 5:1 | 4:3 R:1"                    # 種3 から。♭VI → ♭VII の上で
put("サビ1", C8 + " | " + C4, ["あのなつの", "あわがきえる", "いえないままで", "のみこんだ", "たんさんよりもしみるのよ"])
G3 = lambda a, b_, c: "R:0.5 {}:0.5 {}:0.5 {}:0.5 {}:1 {}:1 | ".format(*a.split()) + "{}:0.5 {}:0.5 {}:1 {}:1 {}:1 | ".format(*b_.split()) + f"{c}:2 R:2"      # 3小節の句（語り）
put("語り", " | ".join([G3("6, 7, 1 1 2", "2 1 6, 7, 1", "1"), G3("1 2 3 3 4", "4 3 2 1 2", "2"), G3("2 2 2 3 3", "3 2 7, 5, 6,", "6,"), G3("2 3 4 4 3", "2 2 7, 6, 5,", "5,"), G3("6, 1 3 3 4", "5 6 5 3 4", "5")]) + " | R:4",
    ["じてんしゃおきばのかげで", "ひとつのかんをふたりで", "かわりばんこにのんだね", "くちがふれたところだけ", "みないふりしてわらうの"])
put("サビ2", C8 + " | " + C4, ["ゆうだちの", "にじをみたね", "そばにいたのに", "とおいまま", "たんさんよりもはかないね"])
put("鐘", "6:1.5 5:0.5 4:1 3:1 | 2:0.5 1:1.5 2:2 | 3:3 R:1 | 5:1.5 4:0.5 3:1 2:1 | 1:0.5 7,:1.5 1:2 | 1:3 R:1", ["かねがなるまえに", "いおうとしていた"])                       # 高い音から下りてくる
put("B0", "R:3 2:0.5 3:0.5 | 4:1.5 3:0.5 2:1 4:1 | 5:3 R:1 | R:3 4:0.5 5:0.5 | 6:1.5 5:0.5 4:1 3:1 | 2:3 R:1 | R:4", ["のどのおくまで", "しみてくことば"], pre=1)        # 1拍早く食って入る（言えなかった言葉を飲みこむ）
SH = lambda p: "{}:0.5 {}:1 {}:1.5 R:1".format(*p.split())                          # 1小節の短い句をたたみかける
put("早口", " | ".join(SH(p) for p in ("2 2 4", "5 5 7", "3 3 5", "6 5 3", "2 4 6", "5 7 5", "5 5 b3", "4 4 2")), ["いまだ", "いえる", "いえよ", "だめだ", "あとで", "あした", "つぎの", "なつに"])
put("B1", "R:2 5,:1 3:1 | 5:2 4:1 3:1 | 2:3 R:1 | R:2 6,:1 4:1 | 6:2 5:1 4:1 | 5:3 R:1", ["かんのなかで", "ゆれていたの"])                                             # 低い音から6度跳ぶ
put("サビ3", "R:2 5,:1 3:1 | 4:1 5:1 6:1.5 R:0.5 | R:2 6:1 4:1 | 2:1 5,:1 1:1.5 R:0.5 | R:2 5,:1 3:1 | 4:1 5:1 6:1.5 R:0.5 | R:2 4:1 3:1 | 2:1 1:1 1:1.5 R:0.5", ["いまもまだ", "あけるたび", "あのひへと", "もどるのよ"])      # 同じ旋律を、小節のまん中から
put("B2", "6:1.5 5:0.5 4:1 3:1 | 2:2 1:1 R:1 | 5:1.5 4:0.5 3:1 2:1 | 1:3 R:1", ["きえないでね", "あのなつよ"])
put("サビ4", C8, ["あのなつの", "あわはいまも", "むねではじける", "すきでした"])
A3 = lambda a, b_, c: "{}:0.5 {}:1.5 {}:1 {}:1 | ".format(*a.split()) + "{}:1.5 {}:0.5 {}:2 | ".format(*b_.split()) + f"{c}:3 R:1"       # 3小節の句（種1 から）
put("A", " | ".join([A3("6, 7, 1 2", "3 2 1", "1"), A3("1 2 3 4", "5 4 3", "2"), A3("2 3 4 5", "6 5 4", "5")]) + " | R:4", ["おとなになれても", "あのかんのあじは", "だれともわけない"])
put("サビ別", "6:1.5 5:0.5 4:1 3:1 | 5:3 R:1 | 6:1.5 4:0.5 2:1 5,:1 | 7,:1 1:2.5 R:0.5 | 6:1.5 5:0.5 4:1 3:1 | 6:2 5:1 3:0.5 R:0.5 | 4:1.5 3:0.5 2:1 1:1 | 1:3 R:1 | " + C4,
    ["さよならも", "いえないまま", "なつはすぎても", "わすれない", "たんさんよりもやさしいね"])                                                                        # 高い音から下りてくる（後ろ半分はサビと同じ）
assert not BAD, BAD


# ================= 伴奏 =================
def sub(b, pat="r---------------"):
    r = low(S.chords[b], "E1"); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + {'r': 0, '5': 7, '7': 10, 'R': 12}[pat[i]])}:{L * 0.25:g}"); i += L
    SUB.bar(b, " ".join(out))


def _ch(tracks, b, pat, center, n, acc=False):
    """acc: 拍の頭でない所（食いこむ所）で打つ和音を、少し強く（強さの山を作る）"""
    v = sorted(voice(S.chords[b], center, n))
    for j in range(n):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(v[j])}:{L * 0.25:g}" + ("!" if acc and i % 4 else "")); i += L
        tracks[j].bar(b, " ".join(out))


def saw(b, pat="x---------------", center=66): _ch(SAW, b, pat, center, 5, acc=True)
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


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "dim" if ("m7b5" in rest or "dim" in rest) else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."


TR = [None]
G8 = ("D-d-d-D-d-d-D-d-", "D-d-D-d-d-D-d-d-", "D-d-d-D-d-D-d-d-", "D-D-d-d-D-d-d-d-")
G8b = ("D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-", "D-U---U-D-U-D-U-", "D---D-U---U-D-U-")


def strum(b, i):
    """ギター（B で OK が出た音と弾き方）: 8分のかき鳴らし。左は根音と5度、右は高い所の三和音。全員が鳴る場面だけ"""
    c = simple(S.chords[b]); SL.bar(b, G8[i % 4], G2.low_shape(c, with_third=False), feel="down"); TR[0] = G2.triad(c, TR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))); SR.bar(b, G8b[i % 4], TR[0])


def bell(b, k=0):
    BELL.bar(b, mel(b, ("R:2 5:0.5 3:0.5 2:0.5 1:0.5", "R:2 3:0.5 5:0.5 6:0.5 1':0.5", "R:2.5 3:0.5 2:0.5 5,:0.5", "R:3 1:0.5 3:0.5")[k % 4], 1))


HK = ("3:0.5 4:0.5 5:0.5 6:1.5 5:0.5 6:0.5", "6:0.5 4:0.5 2:0.5 5,:0.5 7,:0.5 1:1.5", "3:0.5 4:0.5 5:0.5 6:1 1':0.5 6:0.5 5:0.5", "4:0.5 3:0.5 2:0.5 1:2.5")      # フック: 鼻歌の種4・種5・種2 を、2オクターブ上で
K4, SN, SNg, NO = "X...X...X...X...", "....X.......X...", "....X..o.o..X...", "................"
HOF, H16, H16o, H8 = "..x...x...x...O.", "XoxoXoxoXoxoXoxo", "XoxoXoxoXoxoXxO.", "X.o.x.o.X.o.x.o."        # ハイハットは強さ3段（強・ふつう・弱）
GM, GQ = Groove("bounce"), Groove("twostep")                                        # リズムの取り方: 主＝はねる16分／静かな場面＝2ステップ（くじ）
SOLO = ("R:0.5 6,:0.5 7,:0.5 1:1.5 R:1", "2:0.25 2:0.25 2:0.5 3:1 2:0.5 7,:0.5 5,:1", "R:0.5 3:0.5 4:0.5 5:0.5 6:2", "5:0.75 3:0.75 2:0.5 1:2",
        "R:0.5 6,:0.5 7,:0.5 1:1 3:0.5 5:1", "4:0.75 3:0.75 2:0.5 1:1 R:1", "2:0.5 2:0.5 3:1 5:2", "1:2 R:2")                    # 最初のソロ: 鼻歌の種1・種3・種4 を、はねるリズムで
KB = ("X.....X...X.....", "X..X......X.....", "X.....X..X......", "X.........X..X..")
STAB = ("x-----x---x-----", "x--x------x-----", "x-----x--x------", "x---------x--x--")           # 広い和音は、キックと同じ所で打ってのばす


def hook(b, line): HOOK.bar(b, mel(b, line, 1))                                     # 1＝F5（鼻歌の2オクターブ上の高さ）


def full(b, i, k=0, gtr=True, hat=None):
    """全員の場面（サビ・フック・ドロップ）: はねる16分の型（食いこむキック・ゴーストのスネア・強さ3段のハイハット）、キックと同じ所で打つ低いベース、食いこむ広い和音、ピアノ、手びょうし、ギター"""
    GM.drums(D, b, i + k, hat=hat); sub(b, GM.B[(i + k) % 4]); saw(b, GM.C[(i + k) % 4]); ep(b, ("x-------x-------", "x-----x---x-----")[i % 2]); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
    if gtr: strum(b, i + k)


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n in ("始まり", "もどる"):                                        # 上がっていく音。始まりはいきなり落とす／終わりは同じ音にもどって、最後に和音を1つ
        if n == "もどる" and i >= 2:
            if i == 2: saw(b, "x---------------"); ep(b, "x---------------"); sub(b, "r---------------"); D.set(b, "X...............", NO, NO); crash(D, b, "C2", 4); fxh(b, 0, "awa", 2)
            continue
        FX.bar(b, "C5:4"); saw(b, "x-------x-------" if i < 2 else "x---x---x---x---", 62 + 2 * i); D.set(b, NO, "x...x...x...x..." if i < 2 else ("x.x.x.x.x.x.x.x." if i == 2 else "xxxxxxxxXXXXXXXX"), NO)
        if i >= 2: swell(b)
        if i == 3 or (n == "もどる" and i == 1): hat_roll(HATR, b, 1)
    elif n == "ソロ":                                                    # いきなり落として、フックのシンセのソロ（2ステップ。はじめの2小節は泡とパッドだけ）
        hook(b, SOLO[i]); pad(b)
        if i < 2: fxh(b, 0, "awa", 2); (i == 0 and fxh(b, 2, "kira", 1))
        else: GQ.drums(D, b, i, snare=None if i >= 4 else NO); sub(b, GQ.B[i % 4]); ep(b, GQ.C[i % 4])
        if i >= 4: CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 4 == 3: bell(b, i // 4)
        if last: fill(b, 1); fxh(b, 2, "rev", 2)
    elif n in ("止まる1", "止まる2"):                                    # 止まる: 泡の音とオルゴールだけ
        fxh(b, 0, "awa", 2); fxh(b, 2, "kira" if i == 0 else "awa", 1); bell(b, i)
        if last: D.set(b, NO, NO, NO); fill(b, 1 if n == "止まる1" else 4); fxh(b, 3, "rev", 1)
    elif n in ("サビ1", "サビ2", "サビ4"):
        full(b, i, k=0 if n == "サビ1" else 1); arp(b, i % 5)
        if i in (0, 8): crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 7: fill(b, 4 if L > 8 else 0)
        if last: fill(b, 3 if n == "サビ1" else 2); (n != "サビ4" and fxh(b, 2, "awa", 2))
    elif n == "語り":                                                    # 語り: ピアノと低いベース、食いこむキック。後半で広い和音
        GQ.drums(D, b, i, snare=None if i >= 6 else "............X...", hat=H8 if i < 6 else None); sub(b, GQ.B[i % 4]); ep(b, GQ.C[i % 4] if i % 4 != 3 else "x---------------")
        if i >= 9: saw(b, "x---------------", 62); CLP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 3 == 2: bell(b, i // 3)
        if i == 0: fxh(b, 0, "down", 2)
        if last: fill(b, 0); FX.bar(b, "C5:4"); fxh(b, 2, "rev", 2)
    elif n == "鐘":                                                      # 新しい歌: パッドとピアノとオルゴール
        pad(b); ep(b, "x-------x-------"); sub(b, "r---------------")
        if i % 3 == 2: bell(b, i)
        if i == 0: fxh(b, 0, "down", 2)
    elif n == "ドロップ":                                                # ドロップ: 全員で、はねる型をいちばん強く。歌もフックもなし
        full(b, i, k=2); arp(b, (0, 2, 1, 3)[i]); swell(b)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2); fxh(b, 2, "awa", 2)
        if last: fill(b, 2)
    elif n == "立ち上げ":                                                # 立ち上げ: 2小節ごとに音が増える。♭VI → ♭VII でフックへ
        j = i // 2; saw(b, ("x---------------", "x-------x-------", "x---x---x---x---", "x-x-x-x-x-x-x-x-")[j], 60 + i); sub(b, ("r---------------", "r-------r-------", "r---r---r---r---", "r-r-r-r-r-r-r-r-")[j])
        D.set(b, "X.......X......." if j == 0 else K4, NO if j == 0 else ("....x.......x..." if j == 1 else "x...x...x...x..." if j == 2 else "x.x.x.x.x.x.x.x."), NO if j < 2 else H16)
        if j >= 1: arp(b, i % 2); ep(b, "x-------x-------")
        if j >= 2: FX.bar(b, "C5:4")
        if j == 3: swell(b)
        if last: D.set(b, K4, "xxxxxxxxXXXXXXXX", NO); hat_roll(HATR, b, 1); fxh(b, 2, "rev", 2)
    elif n == "早口":                                                    # 頭だけ打って止まる。手びょうし
        D.set(b, "X.....X.........", "............X...", NO); sub(b, "r----r....r....."); ep(b, "x-----x---------"); CLP.bar(b, "R:1 B4:1 R:1 B4:0.5 B4:0.5")
        if i == 0: crash(D, b, "C2", 4)
        if last: D.set(b, "X...X...X.X.....", "....X...X.X.XXXX", NO); FX.bar(b, "C5:4")
    elif n in ("フック1", "フック2"):                                    # 鼻歌の動きを、シンセが2オクターブ上で
        full(b, i, k=1); arp(b, i % 5)
        if i < 8: hook(b, HK[i % 4])
        else: hook(b, ("3:0.5 4:0.5 5:0.5 6:2.5", "5:3 R:1")[i - 8])
        if i % 4 == 0: crash(D, b, "C2", 4); (i == 0 and fxh(b, 0, "impact", 2))
        if last: fill(b, 3 if n == "フック1" else 0); (n == "フック2" and fxh(b, 2, "rev", 2))
    elif n in ("B0", "B1", "B2"):                                        # B: 半分の速さ。パッドとピアノ。キックは2小節で1まわり、スネアの前にゴースト
        pad(b); ep(b, ("x-----x---------", "x---------x-----")[i % 2]); sub(b, ("r---------r-----", "r------r--r-----")[i % 2]); D.set(b, ("X.........X.....", "X......X..X.....")[i % 2], ("........X.......", "......o.X....o..")[i % 2], H8)
        if n == "B0" and i == 0: fxh(b, 0, "down", 2)
        if last: fill(b, 0); FX.bar(b, "C5:4"); fxh(b, 2, "rev", 2)
    elif n == "サビ3":                                                   # サビを、ギターなしで軽く（まん中から入る）
        full(b, i, k=1, gtr=False, hat=HOF); arp(b, 2 + i % 3)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if last: fill(b, 1)
    elif n == "A":                                                       # A: ピアノと低いベースとオルゴール。ドラムは小さく
        ep(b, ("x---x---x-------", "x-------x---x---")[i % 2]); sub(b, GQ.B[i % 4] if i >= 3 else "r---------------"); pad(b); D.set(b, GQ.K[i % 4] if i >= 3 else "X.........X.....", NO, H8 if i >= 3 else NO)
        if i == 0: fxh(b, 0, "down", 2)
        if i % 3 == 2: bell(b, i // 3)
        if last: fill(b, 0); FX.bar(b, "C5:4"); fxh(b, 2, "rev", 2)
    elif n == "サビ別":                                                  # 別の和音の最後のサビ: 全員
        full(b, i, k=0); arp(b, i % 5)
        if i in (0, 8): crash(D, b, "C2", 4); fxh(b, 0, "impact", 2)
        if i == 7: fill(b, 4)
        if last: fill(b, 0)

for b_, hs in FXH.items(): FXT.bar(b_, fx_bar(*hs))
SL.end(S.nb); SR.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベースのアニソン（150・ヘ長調・約4分3秒）。人間の鼻歌の録音から読み取った動きを種にして、アレンジした曲。高校生の甘酸っぱい記憶がコンセプト。"
          "場面の並び・長さは、くじ（form_dice.py・種 51433。合わない5か所は引き直し）、リズムの取り方もくじ（はねる16分＋2ステップ）。上がっていく音で始まり、同じ音にもどって終わる。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "シンセのかけ上がり（矩形波のプラック）", mid=90, down=12, up=10, seed=32)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ別", 0, None, KFm)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.15, "consonant": 2.0, "glide": 0.7, "legato": 0.0, "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 0], ["peak", 2600, 2.0, 4], ["hshelf", 6500, 0.7, 10]], "deess": -5.0}})
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
if VOCAL:                                                                           # 歌のあるサビは、広い和音とかけ上がりを 0.8 倍（C で分かったこと）
    for p_ in js["parts"]:
        if "広い和音" in p_["role"] or "かけ上がり" in p_["role"]:
            g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
            for name in ("サビ1", "サビ2", "サビ3", "サビ4", "サビ別"):
                for b in S.sc(name): g[b] = round(g[b] * 0.8, 4)
            p_["barGain"] = g[:S.nb]
js["guitarWobble"] = False                                                       # 39番のギターには diGuitar を掛けない
GM.apply(js); js["swing16"] = 0.5                                                   # はね: 16分のウラを 0.5÷12 拍（150 で約17ミリ秒）後ろへ。ノリ: あと乗り（スネア・ベースを少し後ろ）。キックとベースは同じだけずらす
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
