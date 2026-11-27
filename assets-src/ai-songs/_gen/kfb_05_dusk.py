# KFB 05「釣瓶落としのベーカリー」Bakery at Early Dusk（仮）— Kawaii future bass（ボカロ）。4分の4・120・ト長調（短調寄りの和音）。122小節・約4分。
#
# 2026-11-27 人間「次秋の夕暮れの寂しさを感じながら恋する物語。kawaiifutureベースで、ベースは18ギターは11で、FXは種類入れて。テンポは120で。ギターソロ、アルペジオ、入れてください」
#   ギター＝見本の11番（distGuitar・guitarTone electro-rock・ampGate 0.5・diGuitar emily）／ベース＝見本の18番（--bass finger ＋ bassSplit アンプ 歪み 0.3）
#   効果音6種類: 上がっていく音（最初だけ）・レコードの針の音・きらめき（下がる＝落ち葉）・下がっていく音（店が閉まる）・逆回しのシンバル・ギターのハーモニクス（一番星）
# 形: くじ（tools/vt3/form_dice.py --skeleton 2512 240 120 --min-chorus 3 --not-groove break --not-start フック --not-start サビ → 種 2514）。
#   始まり＝立ち上げ（上がっていく音）から始めて、いきなり落とす（2小節を足した）／終わり＝フックをくり返しながら消えていく／リズムの取り方＝主「bounce（はねる16分）」・静かな場面「twostep」。
#   骨組みの「ドロップ 8小節」は、ギターソロにした（人間の指定）。
# 物語: 日が短くなった秋の夕方。商店街のパン屋で働く人に恋をしている。閉店の6時に間に合うよう早足で歩くと、長くのびた影だけが先に店先へ着く。自分は角の手前で息を止めるだけ。
#   鏡の前で練習した言葉は、店の明かりの下で口が閉じる。最後の日、日が落ちる前に踏み出して、影より先に自分の足で着き、「こんばんは」だけが言えた。
# この曲だけのもの: 落ち葉のように「下りながら遅くなる」ガラスのプラック（KFB04 のかけ上がりの逆）／サビは vi → ♭VImaj7 → V（Em7 → E♭maj7 → D）で、最後は V/vi で解決しないまま止まる／一番星＝ギターのハーモニクス。
# 歌詞: 曲名の言葉（つるべおとし・べーかりー）は歌わない。声: クリア1種類。歌をなぞるリードは入れない。オーケストラの楽器は使わない。スーパーソウは使わない。
from vocalo_lib import *
import gtr2_lib as G2
from groove_lib import Groove
import re as _re

S = Song("35", "dusk", "釣瓶落としのベーカリー（仮）", "Bakery at Early Dusk", 120, 4, "G", "major", "カワイイ・フューチャーベース（ボカロ）")
S.kit = "crocell-punch"; S.flags = S.flags + " --space room --space-wet 0.08 --bass finger"
KA = Key("G", "major")
CX = ["Em7", "Ebmaj7", "D", "Bm7", "Cmaj7", "Em7", "Ebmaj7", "D", "F", "Cmaj7", "Am7", "B7"]          # サビ（5小節の句×2＋2小節）: vi → ♭VImaj7 → V → iii → IV ／ … → ♭VII → IV ／ ii → V/vi（解決しない）
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("立ち上げ", 2, "intro", ["Cmaj7", "B7"])
scene("夕暮れ", 16, "bridge", ["Cmaj7", "Cmaj7", "Bm7", "Bm7", "Am7", "Am7", "B7sus4", "B7", "Cmaj7", "Cmaj7", "Bm7", "Em7", "Am7", "Am7", "D7sus4", "D7"])
scene("サビ1", 12, "chorus", CX)
scene("金木犀", 12, "verse", ["G", "G", "Bm7", "Bm7", "C", "C", "Cm", "Cm", "G", "B7", "Em7", "A7"])
scene("サビ2", 10, "chorus", CX[:10])
scene("商店街", 16, "verse", ["Em7", "Em7", "Cmaj7", "Cmaj7", "Am7", "Am7", "D", "D", "Em7", "G/B", "Cmaj7", "A7", "Am7", "Am7", "B7sus4", "B7"])
scene("ソロ", 8, "break", ["Cmaj7", "D", "Bm7", "Em7", "Cmaj7", "D", "Am7", "B7"])
scene("フックA", 6, "break", ["Em7", "Ebmaj7", "D", "Bm7", "Cmaj7", "B7"])
scene("サビ3", 12, "chorus", CX)
scene("早口", 8, "verse", ["Am7", "Am7", "Bm7", "Bm7", "Cmaj7", "Cmaj7", "D7sus4", "D7"])
scene("日が落ちる", 6, "bridge", ["Cmaj7", "Cmaj7", "Cm", "Cm", "G", "B7"])
scene("サビ4", 8, "chorus", ["Em7", "Ebmaj7", "D", "Bm7", "Cmaj7", "Em7", "F", "Cmaj7"])
scene("フックB", 6, "outro", ["Em7", "Ebmaj7", "D", "Bm7", "Cmaj7", "Cmaj7"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BASS = S.track("指弾きのベース", "bass", volume=0.22, pan=0, duck=0.1, gainDb=-9, amp="bassSplit", ampDrive=0.3, fx=[{"type": "eq", "low": 0, "mid": 4, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}])   # 見本の18番
T11 = lambda v, pn, **k: {"volume": v, "pan": pn, "guitarTone": "electro-rock", "ampGate": 0.5, "chorus": 0, "humanPitch": 0, "noScoop": True, **k}    # 見本の11番
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **T11(0.06, -0.55, gainDb=-11)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **T11(0.06, 0.55, gainDb=-10)) for i in range(6)]
GA = [S.track(f"Rギター（静か）{i + 1}弦め", "distGuitar", **T11(0.015, 0.55, ampDrive=0.2, release=0.3)) for i in range(6)]   # 静かな場面のアルペジオ: 同じ11番で、歪みを浅く（むき出しで鳴ると音質の点が 6.8 まで落ちた。浅くして 7.67）
GS = [S.track(f"ソロのギター{i + 1}弦め", "distGuitar", **T11(0.17, 0.1, reverb=0.18)) for i in range(6)]
SL, SR, LS = G2.Strummer(GL, S, 43), G2.Strummer(GR, S, 66), G2.Strummer(GS, S, 17); SA = G2.Strummer(GA, S, 71); SL.gap = SR.gap = 0.0
PF = {"type": "pluckfilter", "freq": 2200, "depth": 0.6, "rate": 30, "hold": 4}
STAB = [S.track(f"ガラスの和音{i + 1}", "keys", patch="kfbGlassEp", volume=0.075, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.22, duck=0.15, fx=[{"type": "filter", "kind": "highpass", "freq": 180, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(5)]
PAD = [S.track(f"パッド{i + 1}", "pad", patch="modernPad", volume=0.06, pan=(-0.25, 0.25, 0)[i], reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}]) for i in range(3)]
EP = [S.track(f"FMのピアノ{i + 1}", "fmEpiano", volume=0.055, pan=(-0.2, 0, 0.2, 0.1)[i], reverb=0.22, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(4)]
LEAF = S.track("落ち葉（ガラスのプラック）", "lead", patch="glassPluck", volume=0.075, pan=0.2, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HOOK = S.track("フックのシンセ（やわらかい電子のリード）", "lead", patch="kfbDreamLead", volume=0.065, mono=True, pan=-0.1, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}])
FXT = S.track("効果音（上がる音・針の音・きらめき・下がる音・逆回しのシンバル）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.3, modulate=False)
HRM = S.track("効果音（ギターのハーモニクス）", "guitar", patch="guitarFx", volume=0.09, pan=-0.2, reverb=0.35, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "vinyl": "A#5", "leaf": "D#4", "down": "G4", "rev": "G#4"}


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))
def star(b, notes="B4:2 F#5:2"): HRM.bar(b, notes)
mel = lambda s, up=0: KA.mel(s, oct=3 + up)                                          # 1＝G3。歌は 1（G3）〜 4'（C5）

# ================= 歌 =================
BAD = []


def put(name, bars_s, segs, pre=0):
    b0 = S.sc(name)[0] - pre; lines = [x.strip() for x in bars_s.split("|")]; bars = list(range(b0, b0 + len(lines)))
    assert len(lines) == len(S.sc(name)) + pre, (name, len(lines))
    for x in lines: assert abs(sum(float(y.split(":")[1]) for y in x.split()) - 4) < 1e-6, (name, x)
    nn = sum(1 for x in " ".join(lines).split() if not x.startswith("R")); mm = sum(mora(t) for t in segs)
    if nn != mm: BAD.append((name, nn, mm, [mora(t) for t in segs]))
    ml = [x if x == "R:4" else mel(x) for x in lines]
    for b, m in zip(bars, ml):
        if m != "R:4": V.bar(b, m)
    LY.flow(bars, ml, "/".join(segs), name)



# サビ X（5小節の句×2＋2小節。サビ1・サビ3）／サビ Y（高い音から下りてくる2小節の句。サビ2・サビ4）
CXM = ("R:1 6:0.5 7:0.5 1':1 3':1 | 2':1.5 1':0.5 b7:1 R:1 | R:0.5 5:0.5 6:0.5 7:0.5 2':1 1':1 | 7:1.5 6:0.5 5:2 | 6:3 R:1 | "
       "R:1 6:0.5 7:0.5 1':1 3':1 | 4':1.5 b3':0.5 2':1 R:1 | R:0.5 2':0.5 3':0.5 2':0.5 1':1 7:1 | 2':1.5 1':0.5 b7:2 | 5:3 R:1 | "
       "R:1.5 6:0.5 1':1 2':1 | 7:1.5 #5:0.5 7:2")
CY6 = ("3':1.5 2':0.5 1':0.5 7:1 6:0.5 | b7:1.5 5:0.5 b7:1.5 R:0.5 | 2':1.5 1':0.5 7:0.5 6:1 5:0.5 | 7:1.5 6:0.5 3:1.5 R:0.5 | 1':1.5 7:0.5 6:0.5 5:1 3:0.5 | 6:1.5 5:0.5 6:1.5 R:0.5")
put("夕暮れ", "R:2.5 3:0.5 5:1 | 6:2.5 5:1.5 | 3:2.5 2:1.5 | 3:3 R:1 | R:2.5 3:0.5 5:1 | 7:2.5 6:1.5 | 5:2.5 3:1.5 | 2:3 R:1 | R:2.5 6:0.5 7:1 | 1':2.5 7:1.5 | 6:2.5 5:1.5 | 6:3 R:1 | R:2.5 5:0.5 6:1 | 3':2.5 2':1.5 | 7:2.5 5:1.5 | 6:4",
    ["かねがなるまち", "かげがのびてく", "ひがみじかくて", "いそぐあしおと"])                                                               # 4小節のばす長い句
put("サビ1", CXM, ["かげだけさきに", "あのみせさきにつく", "わたしはまだね", "かどのむこうがわで", "いきをとめる"])                            # 5小節の句
put("金木犀", "R:1 3:0.5 3:0.5 1':1.5 7:0.5 | 5:2.5 R:1.5 | R:1 2:0.5 2:0.5 7:1.5 6:0.5 | 5:2.5 R:1.5 | R:1 3:0.5 3:0.5 2':1.5 1':0.5 | 6:2.5 R:1.5 | R:1 b3:0.5 b3:0.5 1':1.5 b7:0.5 | b6:2.5 R:1.5 | "
              "R:1 3:0.5 3:0.5 2':1.5 7:0.5 | #5:1.5 7:1.5 R:1 | R:1 3:0.5 3:0.5 3':1.5 2':0.5 | #1':3 R:1",
    ["はがおちる", "ほどうには", "なまえさえ", "しらないの", "それでもまた", "ここにいる"])                                                   # 低い音から6度以上跳ぶ
put("サビ2", CY6 + " | 4':1.5 b3':0.5 2':0.5 b7:1 5:0.5 | 2':1.5 1':0.5 7:1.5 R:0.5 | 2':1.5 1':0.5 b7:1.5 6:0.5 | 5:3 R:1",
    ["あまいかぜのなか", "しろいまえかけが", "ぱんをならべてる", "それだけのことに", "むねがなる"])                                          # 高い音から下りてくる
put("商店街", "R:0.5 3:0.5 3:0.5 3:0.5 3:1 1':1 | 7:0.5 6:1.5 R:2 | R:0.5 5:0.5 5:0.5 5:0.5 5:1 1':1 | 7:0.5 5:1.5 R:2 | R:0.5 2:0.5 2:0.5 2:0.5 2:1 1':1 | 6:0.5 5:1.5 R:2 | R:0.5 5:0.5 5:0.5 5:0.5 5:1 2':1 | 1':0.5 7:1.5 R:2 | "
              "R:0.5 3:0.5 3:0.5 3:0.5 3:1 2':1 | 1':0.5 7:1.5 R:2 | R:0.5 5:0.5 5:0.5 5:0.5 5:1 3':1 | 2':0.5 #1':1.5 R:2 | R:0.5 1':0.5 1':0.5 1':0.5 1':1 3':1 | 2':1 1':1 6:2 | 7:3 R:1 | R:4",
    ["しょうてんがいの", "あかりがつくと", "ぱんやのまどが", "きんいろになる", "ろくじにしまる", "ふだがゆれてる", "まにあうようにいく"])   # 同じ音を連打してから跳ぶ
put("サビ3", CXM, ["ゆうひがせなか", "おしてくれてるのに", "ことばはいつも", "のどのおくでまよう", "かげがゆれる"])                            # 5小節の句（骨組みは3小節の句。サビの旋律を2つにしぼるため、サビ1と同じにした）
put("早口", "R:0.5 6:0.5 6:0.5 1':0.5 6:0.5 5:0.5 6:1 | R:0.5 6:0.5 6:0.5 1':0.5 2':0.5 1':0.5 6:1 | R:0.5 7:0.5 7:0.5 2':0.5 7:0.5 6:0.5 7:1 | R:0.5 7:0.5 7:0.5 2':0.5 3':0.5 2':0.5 7:1 | "
            "R:0.5 1':0.5 1':0.5 3':0.5 1':0.5 7:0.5 1':1 | R:0.5 1':0.5 1':0.5 3':0.5 4':0.5 3':0.5 1':1 | R:0.5 2':0.5 2':0.5 4':0.5 2':0.5 1':0.5 2':1 | R:1 6:1 7:2",
    ["こんばんはも", "おいしいねも", "れんしゅうした", "かがみのまえ", "なのにみせの", "あかりのした", "くちがとじる", "また"])               # 1小節の短い句をたたみかける
put("日が落ちる", "R:1.5 3':1 2':0.5 1':1 | 7:2.5 5:0.5 R:1 | R:1.5 b3':1 2':0.5 1':1 | b6:2.5 5:0.5 R:1 | R:1.5 2':1 1':0.5 7:1 | 7:3 R:1",
    ["ひがおちる", "そのまえに", "ふみだす"])                                                                                              # 高い音から下りてくる
put("サビ4", CY6 + " | 2':1.5 1':0.5 b7:1.5 6:0.5 | 5:4", ["かげよりもさきに", "このあしでついた", "こんばんはだけが", "いえたよる"])              # 2小節の句
assert not BAD, BAD


# ================= 伴奏 =================
def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "dim" if ("m7b5" in rest or "dim" in rest) else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


def bass(b, pat="r---------------"):
    """フレットレスのベース。r 根音・3＝3度・5＝5度・7＝7度（短7）・R＝1オクターブ上・9＝1オクターブ上の2度・- のばす・. 休み。分数の和音（E/D など）は下の音が根音"""
    ch = S.chords[b]; r = low(ch, "E1"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 7
    off = {"r": 0, "3": t3, "5": 7, "7": 10, "R": 12, "9": 14}; out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + off[pat[i]])}:{L * 0.25:g}" + ("!" if i % 8 == 0 else "")); i += L
    BASS.bar(b, " ".join(out))


def _ch(tracks, b, pat, center, n, acc=False):
    v = sorted(voice(S.chords[b], center, n))
    for j in range(n):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(v[j])}:{L * 0.25:g}" + ("!" if acc and i % 4 else "")); i += L
        tracks[j].bar(b, " ".join(out))


def stab(b, pat="x---------------", center=66): _ch(STAB, b, pat, center, 5, acc=True)
def pad(b, center=64): _ch(PAD, b, "x---------------", center, 3)
def ep(b, pat="x-------x-------", center=65): _ch(EP, b, pat, center, 4)


def leaf(b, k=0):
    """落ち葉: 高い所から下りながら遅くなる（16分→8分→4分）。この曲だけの音"""
    t = sorted(voice(S.chords[b], 74, 4)); u = [t[3] + 12, t[2] + 12, t[3], t[2], t[1], t[0]]
    p = ("0:0.25 1:0.25 2:0.25 3:0.25 4:0.5 5:0.5 4:1 R:1", "R:1 1:0.25 2:0.25 3:0.25 4:0.25 5:0.5 4:0.5 5:1", "0:0.25 2:0.25 1:0.25 3:0.25 2:0.5 4:0.5 3:1 5:1", "R:2 2:0.25 3:0.25 4:0.5 5:1")[k % 4]
    LEAF.bar(b, " ".join(x if x[0] == "R" else f"{N(u[int(x[0])])}:{x[2:]}" for x in p.split()))


TR = [None]
_ss = sorted(G2.patterns("ロック"), key=lambda p: (abs(p["テンポ"] - 120), -p["打数"]))
PGL, PGR = [p["id"] for p in _ss[0:4:2]], [p["id"] for p in _ss[1:5:2]]              # かき鳴らしの型: GuitarSet の「ロック」から、テンポが 120 に近いもの
GARP = ("0-1-2-1-2-1-0-1-", "0-2-1-2-0-2-1-2-", "0---1-2---1-2---", "2-1-0-1-2---1---")   # アルペジオ（8分が中心）
_tri = lambda b: G2.triad(simple(S.chords[b]), TR[0], top_lo=62, top_hi=69, groups=((2, 3, 4), (3, 4, 5)))


def strum(b, i, both=False):
    """ギター11番: 左＝3度入りの低い形をかき鳴らす。both のとき（ソロ・フック）は右も高い三和音でかき鳴らす"""
    c = simple(S.chords[b]); G2.play(SL, b, PGL[(i // 2) % 2], G2.low_shape(c, with_third=True), half=i % 2, human=0.6, single=False)
    if both: TR[0] = _tri(b); G2.play(SR, b, PGR[(i // 2) % 2], TR[0], half=i % 2, human=0.6, single=False)


def garp(b, i, quiet=False):
    TR[0] = _tri(b); G2.arp(SA if quiet else SR, b, GARP[i % 4], TR[0])


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."



# フック: 落ちていく形（付点でのばして、16分で2つ下りる）
HK = ("3':1.5 2':0.25 1':0.25 7:1 R:1", "4':1.5 b3':0.25 2':0.25 b7:1 R:1", "2':1 R:0.5 1':0.5 7:0.5 6:0.5 5:1", "7:2 R:1 6:0.5 7:0.5", "1':1.5 7:0.5 5:2", "#5:1 7:1 3':2")
HKB = HK[:4] + ("1':1.5 7:0.5 5:2", "6:4")
def hook(b, line): HOOK.bar(b, mel(line, 1))                                        # 1＝G4

GM, GQ = Groove("bounce"), Groove("twostep")                                        # リズムの取り方: 主＝はねる16分／静かな場面＝2ステップ（くじ）
NO = "................"
KM = ("X......X..X.....", "X.....X....X....", "X......X..X..X..", "X..X.......X....")           # キック（主）: この曲の型
BM = ("r------r..r-5-R-", "r-----r-.3.r----", "r------r..r-.r7-", "r-.r---5...r-R-5")           # ベース（主）: キックの所で根音、すき間で5度・3度・オクターブ
KQ = ("X.......X.X.....", "X....X....X.....", "X.......X..X....", "X....X......X...")           # キック（静かな場面）
BQ = ("r-------r.r---5-", "r----r-...r-3-5-", "r-------r..r--R-", "r----r-.5---r---")           # ベース（静かな場面）
BL = ("r---------------", "r-------5-------", "r-----------R---", "r-------5---3---")           # ベース（静か）
SOLO_PH = [p["id"] for p in sorted(G2.phrases(offbeat16=6, min_single=6), key=lambda p: (abs(p["テンポ"] - 120), p["id"]))[:4]]


def full(b, i, k=0, both=False, arp=True):
    """全員の場面: はねる16分のドラム、キックと同じ所で動くベース、ガラスの和音、左のかき鳴らし、右のアルペジオ"""
    GM.drums(D, b, i + k, kick=KM[(i + k) % 4]); bass(b, BM[(i + k) % 4]); stab(b, GM.C[(i + k) % 4]); strum(b, i + k, both=both)
    if arp and not both: garp(b, i + k)


_last = [None]
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "立ち上げ":                                                  # 針の音と上がっていく音だけ → 2小節めの最後を空けて、いきなり落とす
        fxh(b, 0, "vinyl", 4) if i == 0 else fxh(b, 0, "riser", 3)
        pad(b, 62 + 4 * i)
        if i == 1: D.set(b, NO, "x.x.x.x.xxxxX...", NO)
    elif n == "夕暮れ":                                                  # 静か: アルペジオとパッドだけ → 9小節めからベースとドラム
        pad(b, 64); garp(b, i, quiet=True)
        if i == 0: star(b)
        if i == 4: fxh(b, 2, "leaf", 2)
        if i >= 8: bass(b, BL[i % 4]); D.set(b, "X.........X.....", NO, "..x...x...x...x.")
        if i >= 12: ep(b, "x-----x---x-----"); D.set(b, "X.....X...X.....", "....x.......x...", "x.xXx.xXx.xXx.xX")
        if last: fill(b, 3); fxh(b, 2, "rev", 2)
    elif n in ("サビ1", "サビ2", "サビ3", "サビ4"):
        k = SC.index(n) % 4; full(b, i, k=k); leaf(b, i + k)
        if i in (0, 5): crash(D, b, "C2", 4)
        if i == 0 and n in ("サビ2", "サビ4"): fxh(b, 0, "leaf", 2)
        if i == 4: fill(b, 4)
        if i == 9 and L > 10: fill(b, 2)
        if last and n == "サビ1": D.set(b, "X.....X.........", "....X...X.X.XXXX", "x.x.x.x.........")
        if last and n == "サビ2": fill(b, 4)
        if last and n == "サビ3": D.set(b, "X.......X.......", "....X.......X...", NO); fxh(b, 0, "down", 4)        # 店が閉まる
        if last and n == "サビ4": fill(b, 3)
    elif n == "金木犀":                                                  # 新しい歌の場面: 2ステップ。ベースとFMのピアノ、5小節めからアルペジオ
        GQ.drums(D, b, i, kick=KQ[i % 4], snare="....X.......X..." if i >= 4 else "............X..."); bass(b, BQ[i % 4]); ep(b, GQ.C[i % 4])
        if i == 0: fxh(b, 0, "leaf", 2)
        if i >= 4: garp(b, i + 2)
        if i >= 8: pad(b, 64)
        if i in (3, 7): fill(b, 4)
        if last: fill(b, 0); fxh(b, 2, "rev", 2)
    elif n == "商店街":                                                  # A: 前半はベースとピアノ、後半（9小節めから）アルペジオとパッド
        GQ.drums(D, b, i + 1, kick=KQ[(i + 1) % 4], snare=None if i >= 4 else "............X..."); bass(b, BQ[(i + 1) % 4]); ep(b, GQ.C[(i + 1) % 4])
        if i >= 8: garp(b, i + 1); pad(b, 64)
        if i == 8: star(b, "E5:2 B5:2")
        if i in (7, 11): fill(b, 4)
        if last: D.set(b, NO, NO, NO); fill_cresc(D, b, 2, True); fxh(b, 2, "rev", 2)
    elif n == "ソロ":                                                    # ギターソロ（11番）: 左右はかき鳴らし。型は外から入れたもの、音の高さはこの曲の和音と音階
        full(b, i, k=2, both=True)
        if i % 2 == 0: _last[0] = G2.play_phrase(LS, b, SOLO_PH[i // 2], [simple(S.chords[b]), simple(S.chords[b + 1])], {7, 9, 11, 0, 2, 4, 6}, start=_last[0], lo=59, hi=79)
        if i % 4 == 0: crash(D, b, "C2", 4)
        if i == 3: fill(b, 4)
        if last: fill(b, 2)
    elif n in ("フックA", "フックB"):
        full(b, i, k=1 if n == "フックA" else 3, arp=True); hook(b, (HK if n == "フックA" else HKB)[i]); pad(b, 66)
        if i == 0: crash(D, b, "C2", 4); fxh(b, 0, "leaf", 2)
        if i == 3: fill(b, 4)
        if last and n == "フックA": fill(b, 3)
    elif n == "早口":                                                    # 語り・早口: 2ステップ。ベースとFMのピアノ。5小節めからアルペジオ
        GQ.drums(D, b, i + 2, kick=KQ[(i + 2) % 4]); bass(b, BQ[(i + 2) % 4]); ep(b, GQ.C[(i + 2) % 4])
        if i >= 4: garp(b, i)
        if i == 3: fill(b, 4)
        if last: D.set(b, "X...............", "X...............", NO)
    elif n == "日が落ちる":                                              # 静か: パッドとアルペジオとベース。一番星。最後に逆回しのシンバルでサビへ
        pad(b, 64); garp(b, i + 3, quiet=True); bass(b, BL[i % 4])
        if i == 0: star(b, "D5:2 B5:2")
        if i >= 4: D.set(b, "X...X...X...X...", "........" + ("x.x.xxXX" if last else "....x..."), NO)
        if last: fxh(b, 2, "rev", 2)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
SL.end(S.nb); SR.end(S.nb); LS.end(S.nb); SA.end(S.nb)
S.fade_out = 11
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース（120・ト長調・約4分）。日が短くなった秋の夕方、商店街のパン屋で働く人に恋をして、影だけが先に店先へ着く歌。ギターは乾いた浅い歪み、ベースは指弾き。"
          "場面の並び・長さ・旋律の句の形・始まり方・終わり方・リズムの取り方は、くじ（form_dice.py・種 2514。合わない所は引き直し）で決めた。上がっていく音から落として始まり、フックをくり返しながら消える。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "落ち葉（ガラスのプラック）", mid=90, down=12, up=10, seed=35)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js) + LS.velocity(js) + SA.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ3", 5, None, KA), ("サビ4", 0, None, KA)], vol=0.2)
    voice_by_scene(path, S, {}, default="clear")
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
if VOCAL:                                                                           # 歌のあるサビは、ガラスの和音と落ち葉を 0.8 倍
    for p_ in js["parts"]:
        k_ = 0.8 if "ガラスの和音" in p_["role"] else 0.6 if (p_["role"].startswith("Lギター") or p_["role"].startswith("Rギター")) and "静か" not in p_["role"] else None   # 歪んだギターは、歌のサビで 0.6 倍（切り出しで 7.38 → 7.89）
        if k_:
            g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
            for name in ("サビ1", "サビ2", "サビ3", "サビ4"):
                for b in S.sc(name): g[b] = round(g[b] * k_, 4)
            p_["barGain"] = g[:S.nb]
for p_ in js["parts"]:
    if "（静か）" in p_["role"]: p_.pop("barGain", None)                             # 静かなアルペジオは、自動の持ち上げをしない
js["diGuitar"] = "emily"; js["guitarWobble"] = False                                # 11番のギターは録音のギター（emily）を通す
GM.apply(js)                                                                        # ノリ: はねる16分・あと乗り。キックとベースは同じだけずらす
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
