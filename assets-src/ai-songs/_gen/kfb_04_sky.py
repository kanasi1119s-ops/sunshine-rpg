# KFB 04「透過率100%」Transparency 100%（仮）— Kawaii future bass（ボカロ）。4分の4・130・イ長調。130小節・約4分。
#
# 2026-11-27 人間「空が透き通るようなkawaiifutureベースの曲を作ってください。ギターは39ベースは22を使ってください。FXも4種類ほど入れてください。テンポは130で。物語仕立てにしてください」
#   ギター＝見本の39番（instrument guitar・amp crystal・コーラスなし。diGuitar は掛けない）／ベース＝見本の22番（patch fretlessBass。歌うように動かす）
#   効果音4種類: しずく（kawaiiFx drop）・きらめき（kawaiiFx sparkle-up）・逆回しのシンバル（kawaiiFx revcym）・ウインドチャイム（toysFx）。手びょうし・上がっていく音などは入れない。
# 形: くじ（tools/vt3/form_dice.py --skeleton 2403 240 130 --min-chorus 3 …）。始まり＝歌なしのフックを全員で（「いきなり全員でサビ」は最初の場面と合わず引き直し）／終わり＝テンポを落として終わる／
#   リズムの取り方＝主「break（ブレイクビート）」・静かな場面「tresillo（3・3・2）」。骨組みの12場面の前に、始まりのフック4小節を足した。
# 物語: 何日も続いた雨が上がった朝。窓を開けると、雨にみがかれた青。水たまりを飛びこえて土手へ走り、凧を上げる。糸がぴんと張って胸まで引かれる。
#   雨の日に書いた手紙を糸に通すと、風に運ばれて昇っていく。夕方、糸を巻くてのひらに、青がまだ残っている。
# この曲だけのもの: 凧のはためき（16分の細かいゆれ）で始まるフックの旋律／雨のしずくの効果音は曲の最初（立ち上げ）だけ鳴り、あとは二度と出てこない／旋律に ♯4（リディアの色）。
# 歌詞: 曲名の言葉（とうかりつ・ひゃくぱーせんと）は歌わない。声: キュート1種類。歌をなぞるリードは入れない。オーケストラの楽器は使わない。
from vocalo_lib import *
import gtr2_lib as G2
from groove_lib import Groove
import re as _re

S = Song("34", "sky", "透過率100%（仮）", "Transparency 100%", 130, 4, "A", "major", "カワイイ・フューチャーベース（ボカロ）")
S.kit = "crocell-punch"; S.flags = S.flags + " --space room --space-wet 0.08"
KA = Key("A", "major")
CHS = ["Dmaj7", "E/D", "C#m7", "F#m7", "B7", "E7sus4", "Dmaj7", "E/D", "C#m7", "Bm7", "Dm", "A"]          # サビ（3小節の句×4）: IVmaj7 → V/IV → iii ／ vi → II7 → Vsus4 ／ … ／ ii → iv → I
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("フック0", 4, "intro", ["Dmaj7", "E/D", "C#m7", "F#m7"])
scene("雨", 6, "pre", ["Bm7", "Bm7", "C#m7", "C#m7", "E7sus4", "E7"])
scene("サビ1", 12, "chorus", CHS)
scene("数える", 6, "bridge", ["F#m7", "F#m7", "Dmaj7", "Dmaj7", "Bm7", "E7sus4"])
scene("走る", 16, "verse", ["A", "C#m7", "D", "F#m7", "Bm7", "E", "A", "E/G#", "F#m7", "C#m7", "D", "A/C#", "Bm7", "B7", "E7sus4", "E7"])
scene("ソロ1", 12, "break", CHS)
scene("風", 10, "verse", ["A", "A", "F#m7", "F#m7", "D", "D", "Bm7", "E", "D", "E7sus4"])
scene("上がる", 6, "pre", ["Dmaj7", "E", "F", "G", "Asus4", "A"])
scene("サビ2", 12, "chorus", CHS)
scene("サビ別", 8, "chorus", ["F#m7", "E/G#", "A", "B7", "Dmaj7", "E", "F", "G"])
scene("手紙", 16, "verse", ["A", "A", "F#m7", "F#m7", "D", "D", "E", "E", "A", "C#m7", "D", "B7", "Bm7", "Bm7", "E7sus4", "E7"])
scene("フック1", 12, "break", CHS)
scene("夕方", 10, "outro", ["Dmaj7", "Dmaj7", "C#m7", "C#m7", "Bm7", "Bm7", "Dm", "Dm", "A", "A"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BASS = S.track("フレットレスのベース", "bass", patch="fretlessBass", volume=0.2, pan=0, duck=0.1, gainDb=2)                       # 見本の22番。大きさ: サビで測ると 0.2 では +15.7（ギター +15〜17・ドラム +19）で、ほかの曲のベース（+20.8）より 5dB 小さかった。volume を 0.32 にしても +0.2dB しか変わらないので、gainDb 5 で上げる（+20.0）
C39 = lambda v, pn, **k: {"volume": v, "pan": pn, "amp": "crystal", "chorus": 0, "humanPitch": 0, "noScoop": True, **k}  # 見本の39番
GL = [S.track(f"Lギター{i + 1}弦め", "guitar", **C39(0.175, -0.55)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "guitar", **C39(0.17, 0.55)) for i in range(6)]
GS = [S.track(f"ソロのギター{i + 1}弦め", "guitar", **C39(0.3, 0.1, reverb=0.18)) for i in range(6)]
SL, SR, LS = G2.Strummer(GL, S, 41), G2.Strummer(GR, S, 62), G2.Strummer(GS, S, 13); SL.gap = SR.gap = 0.0
PF = {"type": "pluckfilter", "freq": 2200, "depth": 0.6, "rate": 30, "hold": 4}
SAW = [S.track(f"広い和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.065, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.22, duck=0.15, fx=[PF] + rack_supersaw(lp=4200, wide=0.5)) for i in range(5)]
PAD = [S.track(f"きらめくパッド{i + 1}", "pad", patch="kfbSparklePad", volume=0.065, pan=(-0.25, 0.25, 0)[i], reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(3)]
EP = [S.track(f"ベルの混ざったピアノ{i + 1}", "keys", patch="surgeKeysBellPiano", volume=0.055, pan=(-0.2, 0, 0.2, 0.1)[i], reverb=0.22, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(4)]
ARP = S.track("シンセのかけ上がり（矩形波のプラック）", "lead", patch="kfbSquarePluck", volume=0.062, pan=0.2, reverb=0.22, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
HOOK = S.track("フックのシンセ（明るく抜けるリード）", "lead", patch="surgeTropics", volume=0.06, mono=True, pan=-0.1, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}])
SWELL = [S.track(f"ふくらむ和音{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
FXT = S.track("効果音（しずく・きらめき・逆回しのシンバル）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.3, modulate=False)
WCH = S.track("効果音（ウインドチャイム）", "guitar", patch="toysFx", volume=0.05, pan=-0.2, reverb=0.3, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); FXH = {}
FXK = {"drop": "C#4", "kira": "D4", "rev": "G#4"}                                   # 効果音は4種類だけ（この3つ＋ウインドチャイム）


def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))
def chime(b, at=0, down=False): WCH.bar(b, (f"R:{at:g} " if at else "") + f"{'D5' if down else 'C#5'}:{4 - at:g}")
mel = lambda s, up=0: KA.mel(s, oct=3 + up)                                          # 1＝A3。歌は 1（A3）〜 5'（E5）

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


R4 = lambda d: " ".join(f"{d}:0.5" for _ in range(4))
# サビの旋律は1つ（3小節の句×4）。休みから入り、上へ跳んで、♯4（Dmaj7 の上の G♯・B7 の上の D♯）を通り、最後をのばす
CA = "R:0.5 5:0.5 1':1 7:0.5 5:1.5 | R:0.5 5:0.5 2':1 1':0.5 7:1.5 | 7:1.5 5:0.5 3:2"
CB = "R:0.5 6:0.5 1':1 7:0.5 6:1.5 | R:0.5 6:0.5 2':1 #4':0.5 2':1.5 | 2':1.5 1':0.5 2':1 R:1"
CC = "R:0.5 5:0.5 1':1 7:0.5 5:1.5 | R:0.5 5:0.5 2':1 1':0.5 7:1.5 | 7:1.5 1':0.5 3':2"
CD = "R:0.5 4:0.5 6:1 2':0.5 1':1.5 | R:0.5 4:0.5 b6:1 1':0.5 b6:1.5 | 3:1 5:1 1':2"
CHO = " | ".join((CA, CB, CC, CD))
put("サビ1", CHO, ["ほらみて", "まどのむこうに", "あめたち", "みがいたあおが", "どこまで", "つづいているの", "きょうなら", "とどくきがする"])            # 3小節の句
put("数える", "R:2 1:1 3:1 | 5:3 R:1 | R:2 4:1 6:1 | 6:3 R:1 | R:2 2:1 4:1 | 5:4", ["あめの", "おとを", "かぞえ"])                               # 休みから入って最後をのばす
put("走る", "1':0.5 7:0.5 6:0.5 5:0.5 6:0.5 5:0.5 3:1 | 5:0.5 3:0.5 2:0.5 1:0.5 2:1 R:1 | 6:0.5 5:0.5 4:0.5 3:0.5 4:0.5 3:0.5 1:1 | 3:1 1:1 R:2 | "
            "2':0.5 1':0.5 7:0.5 6:0.5 7:0.5 6:0.5 4:1 | 5:0.5 4:0.5 3:0.5 2:0.5 2:1 R:1 | 1':0.5 7:0.5 6:0.5 5:0.5 6:0.5 5:0.5 3:1 | 2:1 5:1 R:2 | "
            "3':0.5 2':0.5 1':0.5 7:0.5 1':0.5 7:0.5 6:1 | 7:0.5 6:0.5 5:0.5 3:0.5 5:1 R:1 | 1':0.5 7:0.5 6:0.5 4:0.5 6:0.5 4:0.5 2:1 | 3:1 5:1 R:2 | "
            "2':0.5 1':0.5 7:0.5 6:0.5 4:1 6:1 | #4:1 6:1 2':2 | 2':1.5 1':0.5 2':2 | R:4",
    ["みずたまりとびこえながら", "かかえたたこゆれる", "あめあがりのみちのにおい", "くつしたまでしみる", "どてはかぜのとおりみちだ", "だれもいないあさだ", "いきをきらしみあげたさき"])   # 高い音から下りてくる
put("風", f"R:1 {R4(3)} 6:1 | 5:1.5 3:0.5 R:2 | R:1 {R4(1)} 5:1 | 3:1.5 1:0.5 R:2 | R:1 {R4(4)} 1':1 | 6:1.5 4:0.5 R:2 | R:1 {R4(2)} 6:1 | 5:1.5 7:0.5 R:2 | R:1 4:0.5 4:0.5 6:0.5 6:0.5 1':1 | 2':3 R:1",
    ["かぜをまつゆび", "いとまきにぎる", "くさがゆれたら", "それがあいずだ", "かけだしたら"])                                                  # 同じ音を連打してから跳ぶ
put("サビ2", CHO, ["いとがね", "ぴんとはるたび", "むねまで", "ひかれるみたい", "ちいさな", "わたしのかけら", "あおさに", "とけていくんだ"])            # 休みから入って最後をのばす
put("サビ別", f"{R4(6)} 1':1 3':1 | 2':2 R:2 | {R4(5)} 1':1 3':1 | #4':2 R:2 | {R4(6)} 2':1 4':1 | 3':1 2':1 7:2 | {R4('b6')} 1':1 b3':1 | 2':3 R:1",
    ["うえへうえへと", "かぜがよんでる", "ゆびさきからひとつつながるいとだ"])                                                                  # 同じ音を連打してから跳ぶ（山の上の山）
put("手紙", "1:0.5 1:0.5 6:1.5 5:0.5 3:1 | 5:2 R:2 | 1:0.5 1:0.5 6:1.5 5:0.5 6:1 | 1':2 R:2 | 2:0.5 2:0.5 1':1.5 6:0.5 4:1 | 6:2 R:2 | 2:0.5 2:0.5 7:1.5 5:0.5 7:1 | 2':2 R:2 | "
            "1:0.5 1:0.5 6:1.5 5:0.5 3:1 | 5:1.5 3:0.5 R:2 | 2:0.5 2:0.5 1':1.5 6:0.5 4:1 | #4:2 6:1 R:1 | 2:0.5 2:0.5 2':1.5 1':0.5 6:1 | 4:1 6:1 2':2 | 2':3 R:1 | R:4",
    ["ちいさくなる", "あのひしがた", "あめのひのじ", "おりたたんで", "いとにとおせば", "かぜがはこぶよ", "するりのぼるてがみ"])                 # 低い音から6度以上跳ぶ
put("夕方", "R:2 6:1 5:1 | 3:1.5 4:0.5 5:2 | R:1 5:1 3:1 2:1 | 3:3 R:1 | R:1 2:1 4:1 6:1 | 6:1.5 5:0.5 4:2 | R:1 4:1 b6:1 1':1 | 1':1 b6:1 4:2 | R:4 | R:4",
    ["ゆうやけに", "いとまく", "てのひらには", "あおがのこる"])                                                                              # 5小節の句。iv の上で止まり、解決は楽器にまかせる
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


def saw(b, pat="x---------------", center=66): _ch(SAW, b, pat, center, 5, acc=True)
def pad(b, center=66): _ch(PAD, b, "x---------------", center, 3)
def ep(b, pat="x-------x-------", center=66): _ch(EP, b, pat, center, 4)


def swell(b):
    v = sorted(voice(S.chords[b], 68, 3))
    for j in range(3): SWELL[j].bar(b, f"{N(v[j])}:4")


def arp(b, k=0):
    """16分のかけ上がり（人間が気に入った「ピロピロピロピーン」）"""
    t = sorted(voice(S.chords[b], 75, 4)); u = t + [t[0] + 12, t[1] + 12]
    o = ([0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3], [4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5], [0, 2, 1, 3, 2, 4, 3, 5, 4, 3, 2, 1, -1, -1, -1, -1], [0, 1, 2, 3, -1, -1, 2, 3, 4, 5, -1, -1, 4, 3, 2, 1],
         [0, -1, -1, 2, -1, -1, 4, -1, 3, -1, -1, 5, -1, -1, 2, -1])[k % 5]
    ARP.bar(b, " ".join("R:0.25" if x < 0 else f"{N(u[x])}:0.25" for x in o))


TR = [None]
_ss = sorted(G2.patterns("弾き語り風"), key=lambda p: (abs(p["テンポ"] - 130), -p["打数"]))
PGL, PGR = [p["id"] for p in _ss[0:4:2]], [p["id"] for p in _ss[1:5:2]]              # ギターの型: GuitarSet の「弾き語り風」から、テンポが 130 に近いものを左右に2つずつ
GARP = ("0---1---2---1---", "0---2---1---2---", "0-1-2---1---2---", "2---1---0---1---")


def strum(b, i):
    """ギター39番: 左＝3度入りの低い形、右＝高い所の三和音。型のダウン・アップ・弦をわたる時間をそのまま使う。全員が鳴る場面だけ"""
    c = simple(S.chords[b]); G2.play(SL, b, PGL[(i // 2) % 2], G2.low_shape(c, with_third=True), half=i % 2, human=0.6, single=False)
    TR[0] = G2.triad(c, TR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))); G2.play(SR, b, PGR[(i // 2) % 2], TR[0], half=i % 2, human=0.6, single=False)


def garp(b, i):
    TR[0] = G2.triad(simple(S.chords[b]), TR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))); G2.arp(SR, b, GARP[i % 4], TR[0])


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."


# フック: 凧のはためき（16分の細かいゆれ）で始まる旋律。歌のサビとは別の形
HK = ("5:0.25 6:0.25 5:0.5 1':1 R:0.5 7:0.5 5:1", "5:0.25 6:0.25 5:0.5 2':1 R:0.5 1':0.5 7:1", "3:0.25 5:0.25 7:0.5 3':1.5 2':0.5 1':1", "6:2 R:0.5 5:0.5 6:0.5 1':0.5")
HK2 = ("6:0.25 7:0.25 6:0.5 1':1 R:0.5 7:0.5 6:1", "6:0.25 7:0.25 6:0.5 2':1 R:0.5 #4':0.5 2':1", "2':1.5 1':0.5 2':2", "R:4")                 # II7 の上（♯4）
HK3 = ("4:0.25 6:0.25 4:0.5 2':1 R:0.5 1':0.5 6:1", "4:0.25 b6:0.25 4:0.5 1':1 R:0.5 b6:0.5 4:1", "3:0.5 5:0.5 1':1 3':2", "R:4")              # ii → iv → I
HOOK12 = HK[:3] + HK2[:3] + HK[:3] + HK3[:3]
def hook(b, line): HOOK.bar(b, mel(line, 1))                                        # 1＝A4

GM, GQ = Groove("break"), Groove("tresillo")                                        # リズムの取り方: 主＝ブレイクビート／静かな場面＝3・3・2（くじ）
NO = "................"
BM = ("r-----..r-5-R---", "r-r-..5---r--3-5", "r-----..r-5-R-9-", "r-..r-3-5-R-7-5-")           # ベース（主）: キックの所で根音、すき間で5度・オクターブ・3度へ歌う
BQ = ("r--r--5-r--R--5-", "r--3--5-R-----5-", "r--r--5-r--R--3-", "r--5--R-9--R-5-3")           # ベース（3・3・2）
BL = ("r-------5---R---", "r-----3-5-------", "r-------R---5-3-", "r---5---R-9-R-5-")           # ベース（静か）: 長い音でなめらかに
SOLO_PH = [p["id"] for p in sorted(G2.phrases(offbeat16=6, min_single=6), key=lambda p: (abs(p["テンポ"] - 130), p["id"]))[:6]]    # ソロの型: テンポが 130 に近い「単音まじりの型」を6つ


def full(b, i, k=0, gtr=True):
    """全員の場面: ブレイクビート、キックと同じ所から歌うベース、食いこむ広い和音、ベルのピアノ、ギター"""
    GM.drums(D, b, i + k); bass(b, BM[(i + k) % 4]); saw(b, GM.C[(i + k) % 4]); ep(b, ("x-------x-------", "x-----x---x-----")[i % 2])
    if gtr: strum(b, i + k)


_last = [None]
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "フック0":                                                   # 歌なしのフックを全員で（凧のはためき）
        full(b, i); hook(b, HK[i]); arp(b, i)
        if i == 0: crash(D, b, "C2", 4); chime(b)
        if last: fill(b, 3)
    elif n == "雨":                                                      # 雨の音が遠ざかる: しずく（ここだけ）とパッド → だんだん増える → 逆回しのシンバルでサビへ
        pad(b, 62 + i); bass(b, BL[i % 4] if i >= 2 else "r---------------")
        FXH[b] = [(0, "drop", 0.5), (1.5, "drop", 0.5), (2.75, "drop", 0.5)] if i < 2 else [(0, "drop", 0.5), (2.5, "drop", 0.5)] if i < 4 else [(0.5, "drop", 0.5)] if i == 4 else []
        if i >= 2: garp(b, i); D.set(b, "X.........X.....", NO, "..x...x...x...x.")
        if i >= 4: ep(b, "x---x---x---x---"); D.set(b, "X...X...X...X...", "....x.......x..." if i == 4 else "x...x...x.x.xxXX", NO); swell(b)
        if last: fxh(b, 2, "rev", 2)
    elif n in ("サビ1", "サビ2"):
        full(b, i, k=0 if n == "サビ1" else 1); arp(b, i if i % 3 != 2 else 4)
        if i % 3 == 0: crash(D, b, "C2", 4)
        if i == 0: fxh(b, 0, "kira", 1); chime(b, 1)
        if i in (5, 8): fill(b, 4)
        if i == 2 and n == "サビ2": fill(b, 4)
        if last: fill(b, 2 if n == "サビ1" else 0); (n == "サビ2" and fxh(b, 2, "rev", 2))
    elif n == "数える":                                                  # 静かな場面: パッドとギターの分散和音とベースだけ
        pad(b, 64); garp(b, i); bass(b, BL[i % 4])
        if i >= 2: D.set(b, "X.........X.....", NO, "..x...x...x...x.")
        if last: fill_cresc(D, b, 1, False)
    elif n == "走る":                                                    # 語り・早口: 3・3・2。前半はベースとピアノ、後半（9小節めから）は右ギターも
        GQ.drums(D, b, i, snare=None if i >= 4 else "........X......."); bass(b, BQ[i % 4]); ep(b, GQ.C[i % 4] if i % 4 != 3 else "x---------------")
        if i >= 8: garp(b, i)
        if i >= 12: pad(b, 66)
        if i in (3, 7, 11): fill(b, 4)
        if last: D.set(b, NO, NO, NO); fill_cresc(D, b, 2, True); fxh(b, 2, "rev", 2)
    elif n == "ソロ1":                                                   # 楽器のソロ: 39番のギター（外から入れた型で、音の高さはこの曲の和音と音階）
        full(b, i, k=2)
        if i % 2 == 0: _last[0] = G2.play_phrase(LS, b, SOLO_PH[i // 2], [simple(S.chords[b]), simple(S.chords[b + 1])], {9, 11, 1, 2, 4, 6, 8}, start=_last[0], lo=57, hi=78)
        if i % 3 == 0: crash(D, b, "C2", 4)
        if i == 0: fxh(b, 0, "kira", 1)
        if i == 5: fill(b, 4)
        if last: fill(b, 3)
    elif n == "風":                                                      # A: 風を待つ。ベースが歌い、ギターは分散和音。ドラムは軽く
        GQ.drums(D, b, i, snare="........X.......", hat="X.x.x.X.x.x.X.x."); bass(b, BQ[(i + 1) % 4] if i >= 4 else BL[i % 4]); garp(b, i + 1); pad(b, 64)
        if i >= 6: ep(b, GQ.C[i % 4])
        if last: fill(b, 1)
    elif n == "上がる":                                                  # 楽器のソロ（短い）: 凧が上がる。フックのシンセが上がっていく和音の上で
        hook(b, ("5:0.25 6:0.25 5:0.5 1':1 2':1 3':1", "5:0.25 7:0.25 5:0.5 2':1 3':1 2':1", "b6:0.25 1':0.25 b6:0.5 b3':1 4':1 b3':1", "b7:0.25 2':0.25 b7:0.5 2':1 4':1 2':1", "2':1 3':1 4':2", "3':3 R:1")[i])
        bass(b, ("r-------r-------", "r-------r---5---", "r---r---r---R---", "r---r---r-5-R-9-", "r-r-r-r-r-r-r-r-", "r-r-r-r-R-R-R-R-")[i]); saw(b, ("x---------------", "x-------x-------", "x---x---x---x---", "x---x---x-x-x-x-", "x-x-x-x-x-x-x-x-", "x-x-x-x-x-x-x-x-")[i], 62 + i)
        D.set(b, "X.......X......." if i < 2 else "X...X...X...X...", NO if i < 2 else ("....x.......x..." if i < 4 else "x.x.x.x.x.x.x.x." if i == 4 else "xxxxxxxxXXXXXXXX"), "..x...x...x...x." if i < 4 else NO)
        if i >= 3: swell(b)
        if i == 4: chime(b)
        if last: fxh(b, 2, "rev", 2)
    elif n == "サビ別":                                                  # サビ（別の和音）: 山の上の山。かけ上がりは休まず
        full(b, i, k=2); arp(b, i % 2)
        if i % 4 == 0: crash(D, b, "C2", 4)
        if i == 0: fxh(b, 0, "kira", 1)
        if i == 3: fill(b, 4)
        if last: fill(b, 3); chime(b, 2, down=True)
    elif n == "手紙":                                                    # A: 小さくなる凧。前半は静か、9小節めから3・3・2で動き出す
        if i < 8:
            pad(b, 64); garp(b, i); bass(b, BL[(i + 2) % 4])
            if i >= 4: D.set(b, "X.........X.....", NO, "..x...x...x...x.")
        else:
            GQ.drums(D, b, i); bass(b, BQ[i % 4]); garp(b, i); ep(b, GQ.C[i % 4])
            if i >= 12: pad(b, 66); swell(b)
            if i == 11: fill(b, 4)
        if i == 7: fill(b, 1)
        if last: D.set(b, "X...X...X...X...", "x.x.x.x.xxxxXXXX", NO); fxh(b, 2, "rev", 2)
    elif n == "フック1":                                                 # 歌なしのフック: 手紙が昇っていく
        full(b, i, k=1); hook(b, HOOK12[i]); arp(b, i if i % 3 != 2 else 4)
        if i % 3 == 0: crash(D, b, "C2", 4)
        if i == 0: fxh(b, 0, "kira", 1); chime(b, 1)
        if i in (2, 8): fill(b, 4)
        if i == 5: fill(b, 2)
        if last: D.set(b, "X...............", "X...............", NO); chime(b, 1, down=True)
    elif n == "夕方":                                                    # 静かな場面: パッドとギターの分散和音とベース。最後の2小節でテンポを落として、主和音に落ち着く
        pad(b, 64); bass(b, BL[i % 4] if i < 8 else "r---------------")
        if i < 8: garp(b, i)
        else: ep(b, "x---------------", 64); c_ = simple(S.chords[b]); (i == 8 and SR.bar(b, "D---------------", G2.triad(c_, TR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))), feel="down"))
        if i == 8: fxh(b, 0, "kira", 1)
        if i == 9: chime(b, 0)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
SL.end(S.nb); SR.end(S.nb); LS.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース（130・イ長調・約4分）。雨上がりの朝に凧を上げ、雨の日に書いた手紙を糸に通して空へ送る歌。ギターは透き通るクリーン、ベースはフレットレス。"
          "場面の並び・長さ・旋律の句の形・始まり方・終わり方・リズムの取り方は、くじ（form_dice.py・種 2403。合わない所は引き直し）で決めた。歌なしのフックで始まり、テンポを落として終わる。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "シンセのかけ上がり（矩形波のプラック）", mid=90, down=12, up=10, seed=34)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js) + LS.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 6, None, KA), ("サビ別", 0, None, KA)], vol=0.2)
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
            for name in ("サビ1", "サビ2", "サビ別"):
                for b in S.sc(name): g[b] = round(g[b] * 0.8, 4)
            p_["barGain"] = g[:S.nb]
js["guitarWobble"] = False                                                          # 39番のギターには diGuitar を掛けない
GM.apply(js)                                                                        # ノリ: 前のめり（ブレイクビート）。キックとベースは同じだけずらす
js["rit"] = {"bar": S.nb - 1, "bars": 2, "to": 0.6, "aTempo": False}                # 終わり方: 最後の2小節でテンポを落とす（歌は その前に終わっている）
if VOCAL:
    n0 = len(js["parts"]); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead"]; print("  歌をなぞるリードを消した:", n0 - len(js["parts"]), "パート")
save(path, js)
