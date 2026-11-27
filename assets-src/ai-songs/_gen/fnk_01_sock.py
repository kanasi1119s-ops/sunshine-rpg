# FNK 01「片方だけのソックス」One Sock Left（仮）— ファンク（ボカロ）。4分の4・124・ニ短調（ドリア。ハ長調の度数で書く）。124小節・約4分。
#
# 2026-11-27 人間「ボカロに7色シグナルみたいなリズムで、ファンクな曲を作って」
#   「7色シグナルみたいなリズム」の受け取り方: テンポ 124・4つ打ちに16分のハイハット・歌の「タータータ」（付点8分の 3・3・2）・全員で止まる所。旋律・和音・物語・楽器は別（生のバンドのファンク）。
# 形: くじ（tools/vt3/form_dice.py --skeleton 2701 240 124 --min-chorus 3 --grooves funk16,four,twostep）。始まり＝効果音ひとつ → すぐAメロ／終わり＝だんだん楽器が抜けて、1つだけ残る／
#   リズムの取り方＝主「four（4つ打ち）」・静かな場面「funk16」。骨組みの「ドロップ 8小節」は、スラップベースのソロにした。
# 物語: 夜11時のコインランドリー。乾燥機の丸い窓が回る音に、つま先が勝手にはねる。向かいの人のひざも同じ速さ。声をかける理由がないから、ひざで話しかける。
#   止まったあと、かごの中に知らない色の靴下がひとつ。「これ、きみのかな」。来週も同じ席、同じ時間で。
# この曲だけのもの: 乾燥機の回る音＝フロアタムの「3・3・2」。曲の最初から鳴り、最後はこれだけが残る／最初の効果音はビブラスラップひとつ。
# 歌詞: 曲名の言葉（かたほう・そっくす）は歌わない。声: クリア1種類。歌をなぞるリードは入れない。オーケストラの楽器（ブラスなど）は使わない。
# キックとベースの型は、この曲用に書く（grooves.json の型をそのまま使うと、同じ型の曲とベースが9割同じになる。KFB05 で分かったこと）。
from vocalo_lib import *
import gtr2_lib as G2
from groove_lib import Groove
import re as _re, os

S = Song("36", "sock", "片方だけのソックス（仮）", "One Sock Left", 124, 4, "C", "major", "ファンク（ボカロ）")
S.kit = "crocell-punch"; S.flags = S.flags + " --space room --space-wet 0.06 --bass finger"
KA = Key("C", "major")
CH16 = ["Bbmaj7", "A7", "Dm7", "G7", "Bbmaj7", "A7", "Dm7", "C/E", "Fmaj7", "Em7", "Dm7", "G7", "Bbmaj7", "A7", "Dm7", "Dm7"]     # サビ: ♭VImaj7 → V7 → i → IV7（ドリア）
AC = ["Dm7", "Dm7", "G7", "G7", "Dm7", "Dm7", "Fmaj7", "A7"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("A1", 8, "verse", AC)
scene("立ち上げ1", 8, "pre", ["Dm7", "Dm7", "Dm7", "Dm7", "Em7", "Fmaj7", "G7", "A7"])
scene("フック1", 8, "break", ["Dm7", "G7", "Dm7", "G7", "Bb", "C", "Dm7", "A7"])
scene("サビ別", 8, "chorus", ["Gm7", "C7", "Fmaj7", "Bb", "Gm7", "C7", "A7", "A7"])
scene("フック2", 8, "break", ["Dm7", "G7", "Dm7", "G7", "Bb", "C", "Dm7", "A7"])
scene("サビ1", 16, "chorus", CH16)
scene("B", 8, "bridge", ["Bbmaj7", "Bbmaj7", "Am7", "Am7", "Gm7", "Gm7", "A7", "A7"])
scene("サビ2", 8, "chorus", CH16[:8])
scene("立ち上げ2", 4, "pre", ["Bb", "C", "Dm7", "A7"])
scene("ドロップ", 8, "break", ["Dm7", "Dm7", "G7", "G7", "Dm7", "Dm7", "Bb", "A7"])
scene("A2", 8, "verse", AC)
scene("サビ3", 12, "chorus", ["Bbmaj7", "A7", "Dm7", "Bbmaj7", "A7", "Dm7", "Fmaj7", "Em7", "Dm7", "Bbmaj7", "A7", "Dm7"])
scene("半分", 14, "chorus", ["Bbmaj7", "Bbmaj7", "A7", "A7", "Dm7", "Bbmaj7", "Bbmaj7", "A7", "A7", "Dm7", "Gm7", "A7", "Dm7", "Dm7"])
scene("A3", 6, "outro", ["Dm7", "Dm7", "G7", "G7", "Dm7", "Dm7"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.4

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BASS = S.track("指弾きのベース", "bass", volume=0.22, pan=0, duck=0.05)             # 歌のある場面は指弾き（スラップのままだと、サビの切り出しが 7.4 どまり。指弾きで 7.69）
SLAP = S.track("スラップベース", "slap", volume=0.2, pan=0, duck=0.05)             # フックとソロはスラップ
BT = [BASS]
C39 = lambda v, pn, **k: {"volume": v, "pan": pn, "amp": "crystal", "chorus": 0, "humanPitch": 0, "noScoop": True, **k}  # 見本の39番（クリーン。diGuitar は掛けない）
GL = [S.track(f"Lギター{i + 1}弦め", "guitar", **C39(0.17, -0.55)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "guitar", **C39(0.17, 0.55)) for i in range(6)]
GS = [S.track(f"ソロのギター{i + 1}弦め", "guitar", **C39(0.3, 0.1, reverb=0.15)) for i in range(6)]
SL, SR, LS = G2.Strummer(GL, S, 47), G2.Strummer(GR, S, 68), G2.Strummer(GS, S, 19); SL.gap = SR.gap = 0.0
EP = [S.track(f"FMのピアノ{i + 1}", "fmEpiano", volume=0.07, pan=(-0.2, 0, 0.2, 0.1)[i], reverb=0.15, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(4)]
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.04, pan=(-0.3, 0.3, 0)[i], reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
HOOK = S.track("フックのシンセ（声のようなリード）", "lead", patch="kfbFormantLead", volume=0.065, mono=True, pan=-0.1, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}])
FXT = S.track("効果音（ビブラスラップ）", "guitar", patch="toysFx", volume=0.08, pan=0.15, reverb=0.25, modulate=False)
CLP = S.track("効果音（手びょうし）", "guitar", patch="kawaiiFx", volume=0.05, pan=-0.1, reverb=0.15, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)
mel = lambda s, up=0: KA.mel(s, oct=4 + up)                                          # 1＝C4。歌は 1（C4）〜 3'（E5）

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




# サビの句（2小節）: 「タータータ・タータータ」（付点8分の 3・3・2 を2回）→ のばす
C1 = "2':0.75 2':0.75 1':0.5 6:0.75 6:0.75 1':0.5 | #1':1.5 6:0.5 R:2"                       # B♭maj7 → A7
C2 = "R:0.5 4:0.5 6:0.5 1':0.5 2':0.75 1':0.75 6:0.5 | 7:1.5 5:0.5 R:2"                      # Dm7 → G7
C4 = "R:0.5 4:0.5 6:0.5 1':0.5 2':0.75 3':0.75 2':0.5 | 1':1.5 5:0.5 R:2"                    # Dm7 → C/E
C5 = "3':0.75 3':0.75 1':0.5 6:0.75 6:0.75 1':0.5 | 7:1.5 5:0.5 R:2"                         # Fmaj7 → Em7
put("A1", "R:1.5 2:0.5 4:1 6:1 | 6:2.5 5:1.5 | 4:2.5 2:1.5 | 2:3 R:1 | R:1.5 2:0.5 4:1 6:1 | 1':2.5 6:1.5 | 5:2.5 4:1.5 | 3:3 R:1", ["まるいまどまわる", "あとじゅうはちふん"])          # 4小節のばす長い句
put("サビ別", "b7:0.75 b7:0.75 2':0.5 1':1 R:1 | b7:0.75 b7:0.75 1':0.5 5:1 R:1 | 6:0.75 6:0.75 1':0.5 6:1 R:1 | 4:0.75 4:0.75 6:0.5 b7:1 R:1 | "
              "2':0.75 2':0.75 b7:0.5 2':1 R:1 | 1':0.75 1':0.75 3':0.5 1':1 R:1 | 3':0.75 3':0.75 #1':0.5 6:1 R:1 | 6:1 #1':1 3':2",
    ["ごろんと", "まわるよ", "ひざがね", "うごくの", "となりの", "ひざまで", "おなじだ", "わらう"])                                            # 1小節の短い句をたたみかける
put("サビ1", " | ".join((C1, C2, C1, C4, C5, C2, C1, "R:0.5 4:0.5 6:0.5 1':0.5 2':2 | 2':3 R:1")),
    ["まわれまわれよる", "しゃつもくつしたも", "まわれまわれよる", "つまさきがはねる", "むかいのひとまで", "おなじりずむだよ", "まわれまわれよる", "あとすこし"])   # 2小節の句
put("B", "R:0.5 2:0.5 2:0.5 2:0.5 b7:1.25 6:0.75 | 4:2.5 R:1.5 | R:0.5 1:0.5 1:0.5 1:0.5 6:1.25 5:0.75 | 3:2.5 R:1.5 | R:0.5 2:0.5 2:0.5 2:0.5 b7:1.25 2':0.75 | 1':2.5 R:1.5 | R:0.5 3:0.5 3:0.5 3:0.5 #1':1.25 2':0.75 | 3':3 R:1",
    ["こえをかける", "りゆうがない", "だからひざで", "はなしかける"])                                                                       # 低い音から6度以上跳ぶ
put("サビ2", "2':1.5 1':1.5 6:1 | #1':2.5 6:1.5 | R:1 4:1 6:1 1':1 | 2':2.5 R:1.5 | 2':1.5 1':1.5 6:1 | #1':2.5 3':1.5 | R:1 2':1 1':1 6:1 | 1':3 R:1",
    ["まわれよる", "ゆるりと", "まわれよる", "ふたりで"])                                                                              # 4小節のばす長い句
put("A2", "6:0.5 6:0.5 4:0.5 6:0.75 1':0.75 R:1 | 6:0.5 6:0.5 4:0.5 6:0.75 2:0.75 R:1 | 5:0.5 5:0.5 4:0.5 5:0.75 7:0.75 R:1 | 5:0.5 5:0.5 7:0.5 2':0.75 7:0.75 R:1 | "
          "6:0.5 6:0.5 1':0.5 2':0.75 1':0.75 R:1 | 2':0.5 2':0.5 1':0.5 6:0.75 4:0.75 R:1 | 6:0.5 6:0.5 1':0.5 3':0.75 1':0.75 R:1 | 3':0.5 3':0.5 #1':0.5 6:1.5 R:1",
    ["まどのなか", "しゃつがとぶ", "たおるもね", "はねている", "きみのあし", "わたしのも", "そろうんだ", "おかしい"])                        # 1小節の短い句をたたみかける
put("サビ3", " | ".join((C1, "R:0.5 4:0.5 6:0.5 1':0.5 2':1.5 R:0.5", C1, "R:0.5 2':0.5 1':0.5 6:0.5 4:1.5 R:0.5", C5, "R:0.5 4:0.5 6:0.5 1':0.5 2':1.5 R:0.5", C1, "R:0.5 2':0.5 1':0.5 6:0.5 2':2")),
    ["まわれまわれよる", "とまるな", "まわれまわれよる", "まだだよ", "おわりのおとまで", "おどろう", "まわれまわれよる", "きみとね"])       # 3小節の句
put("半分", "R:2 2':1.5 1':0.5 | 6:3 R:1 | R:1.5 #1':0.5 3':1 2':1 | 1':2.5 6:1.5 | 6:3 R:1 | R:2 2':1.5 3':0.5 | 2':3 R:1 | R:1.5 6:0.5 #1':1 3':1 | 2':2.5 1':1.5 | 2':3 R:1 | "
            "R:1 b7:1 2':1 1':1 | 6:1.5 #1':0.5 3':2 | 2':4 | R:4",
    ["とまる", "しずかになる", "かごに", "しらないいろ", "これきみのかな"])                                                                # 5小節の句（半分の速さ）
put("A3", "2':1 1':0.5 6:0.5 4:1 R:1 | R:0.5 6:0.5 5:0.5 4:0.5 2:1.5 R:0.5 | 2':1 7:0.5 5:0.5 4:1 R:1 | R:0.5 5:0.5 4:0.5 2:0.5 5:1.5 R:0.5 | 2':1.5 1':0.5 6:1 4:1 | 2:3 R:1",
    ["らいしゅう", "このせき", "じかんも", "おなじで", "またあおう"])                                                                      # 高い音から下りてくる
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
    BT[0].bar(b, " ".join(out))


def _ch(tracks, b, pat, center, n, acc=False):
    v = sorted(voice(S.chords[b], center, n))
    for j in range(n):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(v[j])}:{L * 0.25:g}" + ("!" if acc and i % 4 else "")); i += L
        tracks[j].bar(b, " ".join(out))


def ep(b, pat="x-------x-------", center=64): _ch(EP, b, pat, center, 4)
def org(b, center=67): _ch(ORG, b, "x---------------", center, 3)


TRL, TRR = [None], [None]
_ss = sorted(G2.patterns("ファンク"), key=lambda p: (abs(p["テンポ"] - 124), -p["打数"]))
PGL, PGR = [p["id"] for p in _ss[0:4:2]], [p["id"] for p in _ss[1:5:2]]              # かき鳴らしの型: GuitarSet の「ファンク」から、テンポが 124 に近いもの


GST = ("D---..D-....D---", "..D---....D-..D-", "D---....D-..D---", "..D-..D---..D-..")           # 歌のサビの右ギター: まばらな和音（のばして、止める）
GV = os.environ.get("GV", "stab")


def strum(b, i, left=True, right=True, stab=False):
    """ギター39番: 右＝高い所の三和音、左＝少し低い所の三和音。ファンクの型のダウン・アップ・弦をわたる時間をそのまま使う"""
    c = simple(S.chords[b])
    if right and stab and GV == "stab": TRR[0] = G2.triad(c, TRR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))); SR.bar(b, GST[i % 4], TRR[0], feel=16)
    elif right: TRR[0] = G2.triad(c, TRR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))); G2.play(SR, b, PGR[(i // 2) % 2], TRR[0], half=i % 2, human=0.6, single=False)
    if left: TRL[0] = G2.triad(c, TRL[0], top_lo=57, top_hi=66); G2.play(SL, b, PGL[(i // 2) % 2], TRL[0], half=i % 2, human=0.6, single=False)


def clap(b, pat="R:1 B4:1 R:1 B4:1"): CLP.bar(b, pat)
def dryer(b, v=""): D.tom(b, f"D3:0.75{v} D3:0.75 D3:0.5 D3:0.75{v} D3:0.75 D3:0.5")     # 乾燥機の回る音: フロアタムの 3・3・2


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."




# フック（声のようなシンセ）: 16分の食いこみと 3・3・2
HKS = ("R:0.5 2':0.5 R:0.25 2':0.25 1':0.5 6:0.75 1':0.75 2':0.5", "4':0.75 2':0.75 7:0.5 R:2", "R:0.5 2':0.5 R:0.25 2':0.25 1':0.5 6:0.75 1':0.75 2':0.5", "5:0.75 7:0.75 2':0.5 4':1 R:1",
       "b7:0.75 2':0.75 4':0.5 2':1 R:1", "1':0.75 3':0.75 5':0.5 3':1 R:1", "R:0.5 2':0.5 R:0.25 2':0.25 4':0.5 6':0.75 4':0.75 2':0.5", "#1':1 3':1 6:2")
def hook(b, line): HOOK.bar(b, mel(line))

GQ = Groove("funk16")                                                               # はね・ノリ（少しはねる・あと乗り）だけ借りる
NO = "................"
KM = ("X...X...X...X...", "X...X...X..XX...", "X...X...X...X...", "X...X..XX...X.X.")           # キック（主）: 4つ打ち＋食いこみ
SM = ("....X..o.o..X...", "....X.o.....X..o", "....X..o.o..X..o", "....X.o..o..X.o.")           # スネア: 2・4拍＋ゴースト
HM = ("xoOoxoOoxoOoxoOo", "xoOoxoOoxoOoxoxx", "xoOoxoOoxoOoxoOo", "xoOoxoOoxoOoxOxo")           # ハイハット: 16分。8分の裏でオープン
BM = ("r--.R.r..R.r7-R.", "r--.R..r5..R.r..", "r--.R.r..R.r5-7.", "r-.r.R.r7-.rR.5-")           # ベース（主）: 親指の根音と、オクターブ上のはじく音
KQ = ("X.....X...X.....", "X..X......X..X..", "X.....X...X.X...", "X..X.....X.X....")           # キック（静かな場面）
SQ = ("....X.......X..o", "....X..o....X...", "....X.......X.o.", "....X.o.....X..o")
HQ = ("x.x.x.x.x.x.x.xO", "x.xxx.x.x.xxx.x.", "x.x.x.x.x.x.x.xO", "x.xxx.x.x.x.xOx.")
BQ = ("r-----.R..r-.5..", "r--r.....7-r.R..", "r-----.R..r-.3..", "r--r..5-...r.R.7")           # ベース（静かな場面）
BS = ("r.rR.r7.R.r.5R.r", "r-.R.rR.7.5.r.R.", "r.rR.r5.R.r.7R.9", "rR.r.R7-5-.r.R9R")           # ベース（ソロ）: 16分で動く
BH = ("r-------..r---5-", "r---------R-7-5-")                                                   # ベース（半分の速さ）
EC = ("x-..x-....x-..x-", "..x-..x-....x-..", "x-....x-..x-....", "..x-....x-..x-x-")           # エレピの打ち方
SOLO_PH = [p["id"] for p in sorted(G2.phrases(offbeat16=6, min_single=6), key=lambda p: (abs(p["テンポ"] - 124), p["id"]))[2:6]]


def full(b, i, k=0, gl=True, stab=False):
    j = (i + k) % 4; D.set(b, KM[j], SM[j], HM[j]); bass(b, BM[j]); ep(b, EC[j]); strum(b, i + k, left=gl, stab=stab)


def quiet(b, i, k=0, snare=True, gr=False):
    j = (i + k) % 4; D.set(b, KQ[j], SQ[j] if snare else NO, HQ[j]); bass(b, BQ[j]); ep(b, EC[(j + 1) % 4])
    if gr: strum(b, i + k, left=False)


_last = [None]
_cnt = lambda st: sum(len(t.ev) for t in st.tr)
_prev = {}
for b in range(S.nb):
    for st_ in (SL, SR, LS):                                             # 前の小節で弾かなかったギターは、鳴りっぱなしにしない（のばしたままだと、次に弾くまで何十小節も鳴る）
        c_ = _cnt(st_)
        if b and _prev.get(id(st_)) == c_:
            for s_ in list(st_.ring): st_._stop(s_, S.bar_beat(b) - 0.05)
        _prev[id(st_)] = c_
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "A1":                                                        # 効果音ひとつ → すぐAメロ。乾燥機のフロアタム、3小節めからベース、5小節めからエレピとハイハット
        if i == 0: FXT.bar(b, "C5:2 R:2")
        dryer(b, "!"); D.set(b, "X...............", NO, NO if i < 4 else "..x...x...x...x.")
        if i >= 2: bass(b, BQ[i % 4])
        if i >= 4: ep(b, EC[i % 4])
        if last: fill(b, 4)
    elif n == "立ち上げ1":                                               # 右のギター → 左のギターとオルガン → スネアで上げて、最後の半小節を空ける
        quiet(b, i, gr=True)
        if i >= 4: strum(b, i, right=False); org(b, 64 + i)
        if i == 6: D.S[b] = "....X...X...X.X."
        if last: D.set(b, "X...X...........", "x.x.xxXX........", NO)
    elif n in ("フック1", "フック2"):
        BT[0] = SLAP; full(b, i, k=0 if n == "フック1" else 2); clap(b)
        if n == "フック1": hook(b, HKS[i])
        elif i % 2 == 0: _last[0] = G2.play_phrase(LS, b, SOLO_PH[i // 2], [simple(S.chords[b]), simple(S.chords[b + 1])], {0, 2, 4, 5, 7, 9, 11}, start=_last[0], lo=59, hi=79)
        if i == 0: crash(D, b, "C2", 4)
        if i == 3: fill(b, 4)
        if last: fill(b, 2 if n == "フック1" else 3)
        BT[0] = BASS
    elif n == "サビ別":                                                  # 1小節の短い句: ファンクの16分。ベースとエレピと右のギター、手びょうし
        quiet(b, i, k=1, gr=True); clap(b)
        if i == 3: fill(b, 4)
        if last: D.set(b, "X.....X.........", "....X...X.X.XXXX", "x.x.x.x.........")
    elif n in ("サビ1", "サビ3"):
        full(b, i, k=1 if n == "サビ1" else 3, gl=False, stab=True); org(b, 67)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 4 == 3 and not last: fill(b, 4)
        if i >= 8 or n == "サビ3": clap(b)
        if last: fill(b, 3 if n == "サビ1" else 0)
    elif n == "B":                                                       # 静か: キックは少なく、エレピは長い和音、ベースは長い音。乾燥機のフロアタムが戻る
        D.set(b, "X.........X.....", "............X..." if i >= 4 else NO, "x...x...x...x..."); dryer(b); bass(b, BH[i % 2]); ep(b, "x---------x-----"); org(b, 64)
        if last: fill(b, 1)
    elif n == "サビ2":                                                   # 長くのばすサビ: 全員。右のギターだけ
        full(b, i, k=2, gl=False, stab=True); org(b, 67)
        if i == 0: crash(D, b, "C2", 4)
        if i == 3: fill(b, 4)
    elif n == "立ち上げ2":                                               # スネアで上げて、最後の小節の後ろ半分を全員で止める
        D.set(b, "X...X...X...X...", ("....X.......X...", "....X...X...X...", "..X...X...X...X.", "x.x.xxXX........")[i], "x.x.x.x.x.x.x.x." if i < 3 else NO); bass(b, "r-..r-..r-..r-.." if i < 3 else "r-..r-.........."); ep(b, "x-..x-..x-..x-.." if i < 3 else "x-..x-.........."); strum(b, i, left=i >= 2) if i < 3 else None
    elif n == "ドロップ":                                                # スラップベースのソロ: ドラムとベース、右のギター。後半は声のようなシンセが答える
        j = i % 4; D.set(b, KM[j], SM[j], HM[j]); BT[0] = SLAP; bass(b, BS[j]); BT[0] = BASS; strum(b, i + 1, left=False); clap(b)
        if i >= 4: hook(b, HKS[(i - 4) * 2 + 1] if i < 7 else HKS[7])
        if i == 0: crash(D, b, "C2", 4)
        if i == 3: fill(b, 4)
        if last: fill(b, 2)
    elif n == "A2":                                                      # Aメロ: ファンクの16分。乾燥機のフロアタムも
        quiet(b, i, k=2, gr=i >= 4); dryer(b)
        if i == 3: fill(b, 4)
        if last: fill(b, 0)
    elif n == "半分":                                                    # 半分の速さ: 乾燥機が止まる。スネアは3拍め。最後の4小節はうすく
        D.set(b, "X.........X.....", "........X.......", "x...x...x...x..." if i < 10 else NO); bass(b, BH[i % 2] if i < 12 else "r---------------"); ep(b, "x---------x-----" if i < 12 else "x---------------")
        if i < 10: org(b, 65); strum(b, i, left=False) if i >= 5 else None
        if i == 0: crash(D, b, "C2", 4)
        if i == 9: fill(b, 4)
    elif n == "A3":                                                      # だんだん抜ける: ベース＋エレピ＋フロアタム → ベース＋フロアタム → フロアタムだけ
        dryer(b, "!" if i >= 4 else "")
        if i < 4: bass(b, BQ[i % 4])
        if i < 2: ep(b, EC[i % 4]); D.set(b, "X...............", NO, "..x...x...x...x.")

SL.end(S.nb); SR.end(S.nb); LS.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのファンク（124・ニ短調のドリア・約4分）。夜のコインランドリーで、乾燥機の回る音に合わせて、向かいの知らない人とひざでリズムを合わせる歌。スラップベース、クリーンのギターのかき鳴らし、FMのエレピ、オルガン。"
          "場面の並び・長さ・旋律の句の形・始まり方・終わり方・リズムの取り方は、くじ（form_dice.py・種 2701。合わない所は引き直し）で決めた。効果音ひとつで始まり、楽器が抜けてフロアタムだけが残る。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js) + LS.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ3", 0, None, KA)], vol=0.2)
    voice_by_scene(path, S, {}, default="clear")
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
if VOCAL:                                                                           # 歌のサビは、右のギターを 0.5 倍（切り出しで 7.16 → 7.4）
    for p_ in js["parts"]:
        if p_["role"].startswith("Rギター"):
            g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
            for name in ("サビ1", "サビ2", "サビ3", "サビ別"):
                for b in S.sc(name): g[b] = round(g[b] * 0.5, 4)
            p_["barGain"] = g[:S.nb]
js["guitarWobble"] = False                                                          # 39番のギターには diGuitar を掛けない
GQ.apply(js)                                                                        # ノリ: 少しはねる16分・あと乗り。キックとベースは同じだけずらす
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
