# UG 01「地下三階、午前二時」B3F, 2 A.M.（仮）— インスト。ピアノとシンセと効果音だけ。4分の4・190・ヘ短調（変イ長調の度数で書く）。186小節・約3分55秒。
#
# 2026-11-27 人間「ピアノとシンセとFXだけでインスト曲をテンポ190で作って。コンセプトはアンダーグラウンドで」
#   楽器: ピアノ（右手の旋律・左手の和音）／シンセ（ベース2種・パッド・プラック・リード）／効果音（kawaiiFx）。ドラムセット・ギター・エレキベースは使わない。
#   打楽器の役は、効果音（硬いキック・手びょうし・指パッチン・グリッチ）でやる。
# 形: くじ（tools/vt3/form_dice.py --skeleton 2803 230 190 --min-chorus 2 --not-groove four --not-start フック --not-start サビ）。始まり＝ベースだけ（4小節を足した）／終わり＝全員で1打して止まる／
#   リズムの取り方＝主「pogo（4分キックのたてノリ）」・静かな場面「laid（あと乗りのハーフ）」。歌の場面は、ピアノの右手が歌う。
# 物語: 終電のあとの地下。使われていない改札の奥から、低い音が聞こえる。階段を下りるほど音が増える。扉の向こうは、だれも知らないフロア。夜明け前、最後の一打で明かりが落ちる。
# この曲だけのもの: 打楽器がぜんぶ効果音／ベースだけで始まる／ナポリの和音（G♭）で地下の暗さ。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("37", "b3f", "地下三階、午前二時（仮）", "B3F, 2 A.M.", 190, 4, "Ab", "major", "インスト（ピアノとシンセ）")
S.flags = S.flags + " --space room --space-wet 0.08"
KA = Key("Ab", "major")
CH8 = ["Fm", "Dbmaj7", "Bbm7", "C7", "Fm", "Db", "Gb", "C7"]                          # サビ: i → VI → iv → V ／ i → VI → ♭II（ナポリ）→ V
A16 = ["Fm", "Fm", "Eb", "Eb", "Dbmaj7", "Dbmaj7", "C7", "C7", "Fm", "Fm", "Bbm7", "Bbm7", "Db", "Db", "C7sus4", "C7"]
DR8 = ["Fm", "Fm", "Gb", "Gb", "Fm", "Fm", "Db", "C7"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("地下へ", 4, "intro", ["Fm"] * 4)
scene("サビ1", 8, "chorus", CH8)
scene("静か", 4, "bridge", ["Dbmaj7", "Dbmaj7", "C7sus4", "C7"])
scene("A1", 16, "verse", A16)
scene("ソロ", 10, "break", ["Fm", "Fm", "Db", "Db", "Bbm7", "Bbm7", "Eb", "Eb", "C7", "C7"])
scene("サビ2", 8, "chorus", CH8)
scene("A2", 16, "verse", A16)
scene("ドロップ1", 8, "break", DR8)
scene("B", 8, "bridge", ["Bbm7", "Bbm7", "Eb", "Eb", "Abmaj7", "Abmaj7", "Gb", "C7"])
scene("フック1", 8, "break", DR8)
scene("A3", 12, "verse", A16[:8] + ["Bbm7", "Bbm7", "C7sus4", "C7"])
scene("サビ3", 16, "chorus", CH8 * 2)
scene("新1", 6, "bridge", ["Dbmaj7", "Dbmaj7", "Bbm7", "Bbm7", "C7sus4", "C7"])
scene("サビ4", 8, "chorus", CH8)
scene("語り1", 8, "verse", ["Fm", "Fm", "Eb", "Eb", "Db", "Db", "C7", "C7"])
scene("サビ別", 8, "chorus", ["Dbmaj7", "Eb", "Fm", "Fm", "Dbmaj7", "Eb", "C7", "C7"])
scene("ドロップ2", 8, "break", DR8)
scene("新2", 16, "pre", ["Abmaj7", "Abmaj7", "Eb", "Eb", "Fm", "Fm", "Dbmaj7", "Dbmaj7", "Bbm7", "Bbm7", "Gb", "Gb", "C7sus4", "C7sus4", "C7", "C7"])
scene("フック2", 10, "break", DR8 + ["Fm", "Fm"])
scene("語り2", 4, "outro", ["Fm", "Gb", "C7", "Fm"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

PR = S.track("ピアノ（右手・旋律）", "piano", volume=0.42, pan=0.05, reverb=0.18)
PR2 = S.track("ピアノ（右手・オクターブ上）", "piano", volume=0.2, pan=0.15, reverb=0.18)
PL = [S.track(f"ピアノ（左手・和音）{i + 1}", "piano", volume=0.16, pan=(-0.15, -0.05, -0.1)[i], reverb=0.15) for i in range(3)]
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.2, pan=0, gainDb=-6)
DIRT = S.track("シンセのベース（汚れて太い）", "bass", patch="surgeBassModernDirtyFat", volume=0.13, pan=0, gainDb=-6, fx=[{"type": "filter", "kind": "lowpass", "freq": 2500, "q": 0.6}])
BT = [SUB]
PAD = [S.track(f"パッド{i + 1}", "pad", patch="modernPad", volume=0.13, pan=(-0.3, 0.3, 0)[i], reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}]) for i in range(3)]
PLK = S.track("シンセのプラック", "lead", patch="modernPluck", volume=0.13, pan=0.3, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
LEAD = S.track("シンセのリード", "lead", patch="modernLead", volume=0.2, mono=True, pan=-0.1, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}])
FX = lambda name, v, pn=0.0: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=0.08, modulate=False)
FK, FC, FS, FG = FX("効果音（硬いキック）", 0.12), FX("効果音（手びょうし）", 0.09, 0.05), FX("効果音（指パッチン）", 0.06, -0.25), FX("効果音（グリッチ）", 0.045, 0.3)
FXT = S.track("効果音（針の音・上がる音・下がる音・逆回しのシンバル・当たる音・低く落ちる音）", "guitar", patch="kawaiiFx", volume=0.07, pan=0.1, reverb=0.3, modulate=False)
N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "down": "G4", "rev": "G#4", "impact": "G5", "subdrop": "G#5", "vinyl": "A#5"}
def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))
mel = lambda s, up=0: KA.mel(s, oct=3 + up)                                          # 1＝A♭3、6＝F4


def grid(tr, b, pat, key):
    """16マスの型で効果音を打つ（X・x＝打つ、.＝休み）"""
    out = []; i = 0; pat = pat.replace(" ", ""); assert len(pat) == 16, pat
    while i < 16:
        if pat[i] in "Xx": out.append(f"{key}:0.25" + ("!" if pat[i] == "X" else "")); i += 1
        else:
            L = 1
            while i + L < 16 and pat[i + L] not in "Xx": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    tr.bar(b, " ".join(out))


def perc(b, k=None, c=None, s=None, g=None):
    if k: grid(FK, b, k, "F#5")
    if c: grid(FC, b, c, "B4")
    if s: grid(FS, b, s, "C5")
    if g: grid(FG, b, g, "D#6")


def pogo(b, i, hat=True): perc(b, ("X...X...X...X...", "X...X...X...X.X.")[i % 4 == 3], "....X.......X...", "..x...x...x...x." if hat else None, "..........x....." if i % 2 else None)
def laid(b, i, snap=True): perc(b, ("X.........X.....", "X.......X.X.....")[i % 4 == 3], "........X.......", "....x.......x..." if snap else None)

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



def pad(b, center=63): _ch(PAD, b, "x---------------", center, 3)
def lh(b, pat="x-------x-------", center=53): _ch(PL, b, pat, center, 3)


def ct(tr, b, cell, center=65, up=0):
    """和音の音で書く句。0〜3＝その小節の和音の音（低い方から）、+ で1オクターブ上、- で下。例 "0:0.5 0:0.5 2:1 3+:1 R:1" """
    v = sorted(voice(S.chords[b], center, 4)); out = []
    for x in cell.split():
        a, L = x.split(":")
        if a == "R": out.append(x); continue
        out.append(f"{N(v[int(a[0])] + 12 * (a.count('+') - a.count('-')) + up)}:{L}")
    assert abs(sum(float(x.split(':')[1].rstrip('!')) for x in out) - 4) < 1e-6, cell
    tr.bar(b, " ".join(out))


def theme(name, lines, dbl=False):
    bars = S.sc(name); ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) == len(bars), (name, len(ls), len(bars))
    for b, l in zip(bars, ls):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l != "R:4":
            PR.bar(b, mel(l))
            if dbl: PR2.bar(b, mel(l, 1))


def plk(b, k=0):
    t = sorted(voice(S.chords[b], 72, 4)); o = ([0, -1, 2, -1, 3, -1, 2, 1], [3, -1, 1, 2, -1, 0, 2, -1], [0, 2, -1, 3, -1, 2, -1, 1], [-1, 3, 2, -1, 1, -1, 0, 2])[k % 4]
    PLK.bar(b, " ".join("R:0.5" if x < 0 else f"{N(t[x])}:0.5" for x in o))


# サビの旋律（ピアノ）: X＝2小節の句／Y＝高い音から下りてくる／Z＝同じ音を2つ打ってから跳ぶ／W＝サビ（別の和音）
X = ["6:1 1':0.5 3':1.5 2':1 | 1':1.5 6:0.5 R:2", "4:1 6:0.5 2':1.5 1':1 | #5:1.5 3:0.5 R:2", "6:1 1':0.5 3':1.5 4':1 | 3':1.5 1':0.5 R:2", "b7:1 2':0.5 4':1.5 2':1 | 3':2 #5:1 3:1"]
Y = ["6':1 5':0.5 3':1.5 1':1 | 6:2 R:2", "4':1 3':0.5 2':1.5 6:1 | #5:2 R:2", "6':1 5':0.5 3':1.5 4':1 | 3':2 R:2", "4':1 2':0.5 b7:1.5 4:1 | 3:1 #5:1 3':2"]
Z = ["6:0.5 6:0.5 4':2 3':1 | 1':2 R:2", "4:0.5 4:0.5 2':2 1':1 | #5:2 R:2", "6:0.5 6:0.5 6':2 5':1 | 3':2 R:2", "b7:0.5 b7:0.5 4':2 2':1 | 3':3 R:1"]
W = ["4:0.5 6:0.5 1':1 3':2 | 2':0.5 5:0.5 7:1 2':2 | 1':1 6:1 1':2 | R:4", "4:0.5 6:0.5 1':1 4':2 | 5':0.5 2':0.5 7:1 5:2 | 3':0.5 1':0.5 #5:1 3:2 | 3:2 R:2"]
theme("サビ1", X); theme("サビ2", Y); theme("サビ3", X + Z); theme("サビ4", Y, dbl=True); theme("サビ別", W)
theme("B", ["R:2 4:1 6:1 | 2':3 R:1", "R:2 5:1 7:1 | 3':3 R:1", "R:2 3:1 5:1 | 1':2 3':2", "R:2 b7:1 2':1 | #5:3 R:1"])                      # 休みから入って最後をのばす
theme("新1", ["R:4 | R:2 3':1 1':1", "4':2 2':1 6:1 | 4:3 R:1", "R:1 4:1 5:1 1':1 | #5:4"])
# A（ピアノ）: 和音の音で書く。同じ音を連打してから跳ぶ（A1）／低い音から跳ぶ（A2）／2小節の句（A3）
AC1 = ("0:0.5 0:0.5 0:0.5 0:0.5 1:1 2:1", "3:2 R:2", "0:0.5 0:0.5 0:0.5 0:0.5 2:1 3:1", "1+:2 R:2")
AC2 = ("0:1 R:0.5 2+:1.5 1+:1", "3:1.5 2:0.5 R:2", "0:1 R:0.5 3+:1.5 2+:1", "0+:1.5 3:0.5 R:2")
AC3 = ("R:0.5 1:0.5 2:0.5 3:0.5 2:1 0+:1", "3:1 2:1 R:2", "R:0.5 2:0.5 3:0.5 0+:0.5 3:1 1+:1", "0+:1 3:0.5 2:0.5 1:2")
SOLO = ("0+:0.5 3:0.5 2:0.5 3:0.5 0+:0.5 1+:0.5 0+:0.5 3:0.5", "2:0.5 3:0.5 0+:1 R:0.5 1+:0.5 2+:1", "2+:0.5 1+:0.5 0+:0.5 3:0.5 2:0.5 3:0.5 0+:0.5 1+:0.5", "2+:1.5 1+:0.5 0+:2")
HK = ("6:0.5 R:0.5 6:0.5 1':0.5 R:0.5 6:0.5 3':1", "2':0.5 1':0.5 6:1 R:2", "b7:0.5 R:0.5 b7:0.5 2':0.5 R:0.5 b7:0.5 4':1", "2':0.5 1':0.5 b7:1 R:2",
      "6:0.5 R:0.5 6:0.5 1':0.5 R:0.5 3':0.5 6':1", "5':0.5 3':0.5 1':1 R:2", "4':0.5 R:0.5 4':0.5 1':0.5 R:0.5 6:0.5 4:1", "3:0.5 #5:0.5 7:1 2':2", "6:1 1':1 3':2", "6':4")
BPG = ("r-..r-..r-R-..r-", "r-..r-r-..5-R-..", "r-..r-..r-R-..7-", "r-r-..r-5-..R-r-")           # ベース（主）
BLD = ("r-------....r---", "r-----------5---", "r-------....R---", "r---------7-5---")           # ベース（静か）
BDR = ("r-r-R-..r-..7-R-", "r-r-R-..5-r-..R-", "r-r-R-..r-..5-7-", "r-..R-r-7-..R-5-")           # ベース（ドロップ）: 汚れたシンセで16分
NO = "................"


def full(b, i, k=0, dirt=False, plk_=True):
    pogo(b, i + k); BT[0] = DIRT if dirt else SUB; bass(b, (BDR if dirt else BPG)[(i + k) % 4]); BT[0] = SUB
    if dirt: SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:4")
    if plk_: plk(b, i + k)


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "地下へ":                                                    # ベースだけ（針の音が小さく鳴っている）。3小節めから汚れたベースが重なる
        bass(b, BLD[i % 4])
        if i == 0: fxh(b, 0, "vinyl", 4)
        if i >= 2: BT[0] = DIRT; bass(b, ("r-..r-..r-R-..r-", "r-..r-r-r-rRrRrR")[i - 2]); BT[0] = SUB
    elif n in ("サビ1", "サビ2", "サビ3", "サビ4", "サビ別"):
        hot = n in ("サビ3", "サビ4"); full(b, i, k=SC.index(n) % 4, plk_=n != "サビ1"); lh(b, "x-----x---x-----" if i % 2 == 0 else "x---x-----x---x-"); pad(b) if n != "サビ1" or i >= 4 else None
        if i == 0: fxh(b, 0, "impact", 2)
        if hot and i % 8 == 0 and i: fxh(b, 0, "impact", 2)
        if last and n in ("サビ1", "サビ3"): fxh(b, 0, "down", 4)
        if last and n == "サビ2": perc(b, "X...X...X.X.X.XX", "....X...X.X.XXXX")
    elif n == "静か":                                                    # 左手の和音とパッドだけ
        lh(b, "x---------------"); pad(b, 60)
        if last: fxh(b, 2, "rev", 2)
    elif n in ("A1", "A2", "A3"):
        cells = {"A1": AC1, "A2": AC2, "A3": AC3}[n]; ct(PR, b, cells[i % 4]); laid(b, i, snap=i >= 4); bass(b, BLD[i % 4]); lh(b, "x-------..x-----" if i % 2 == 0 else "..x-------x-----")
        if n != "A1" and i >= 4: plk(b, i)
        if i >= 8: pad(b)
        if n == "A3" and i >= 8: perc(b, "X...X...X...X...", "....X.......X..." if i < 11 else "x.x.x.x.xxxxXXXX")
        if last: fxh(b, 0, "riser", 4)
    elif n == "ソロ":                                                    # シンセのリードのソロ（和音の音で、8分で走る）
        full(b, i, k=1); ct(LEAD, b, SOLO[i % 4], center=70); lh(b, "x---x---x---x---"); pad(b)
        if i == 0: fxh(b, 0, "impact", 2)
        if last: fxh(b, 0, "rev", 4)
    elif n in ("ドロップ1", "ドロップ2"):                                # ドロップ: 汚れたベースの16分、効果音の打楽器、ピアノは低い所で短く打つ
        full(b, i, k=2, dirt=True); pad(b, 60); lh(b, "x-..x-....x-..x-" if i % 2 == 0 else "..x-..x-....x-..", 58); ct(PR, b, ("R:2 2:0.5 3:0.5 0+:1", "3:1 2:1 R:2", "R:2 3:0.5 0+:0.5 1+:1", "0+:1 3:1 R:2")[i % 4])
        if i == 0: fxh(b, 0, "subdrop", 4)
        if n == "ドロップ2" and i % 2 == 1: LEAD.bar(b, mel(HK[i]))
        if last: fxh(b, 0, "riser", 4)
    elif n == "B":                                                       # パッドとピアノ。前半は打楽器なし、後半からキック
        pad(b); lh(b, "x---------x-----"); bass(b, "r---------------")
        if i >= 4: perc(b, "X.......X.......", None, "....x.......x...")
        if i == 6: fxh(b, 0, "riser", 4)
        if last: perc(b, "X...X...X.X.XXXX", "x.x.x.x.xxxxXXXX")
    elif n in ("フック1", "フック2"):
        full(b, i, k=3 if n == "フック1" else 1); LEAD.bar(b, mel(HK[i])); pad(b); lh(b, "x-----x---x-----")
        if n == "フック2" and HK[i] != "6':4": PR.bar(b, mel(HK[i], 1 if i < 8 else 0))
        if i == 0: fxh(b, 0, "impact", 2)
        if last and n == "フック1": fxh(b, 0, "down", 4)
    elif n == "新1":                                                     # ピアノとパッドだけ（階段の踊り場）
        pad(b, 60); lh(b, "x-------x-------", 55)
        if last: fxh(b, 2, "rev", 2)
    elif n == "語り1":                                                   # ベースと効果音の打楽器。ピアノは休みから入って短く答える
        pogo(b, i, hat=i >= 4); bass(b, BPG[i % 4]); ct(PR, b, ("R:2 2:0.5 3:0.5 0+:1", "3:2 R:2")[i % 2])
        if i >= 4: BT[0] = DIRT; bass(b, BPG[(i + 1) % 4]); BT[0] = SUB
        if last: fxh(b, 0, "riser", 4)
    elif n == "新2":                                                     # 階段を下りきる: 前半はハーフ、後半から全員。ピアノは高い音から下りてくる
        ct(PR, b, ("3+:1 2+:1 1+:1 0+:1", "3:2 R:2", "2+:1 1+:1 0+:1 3:1", "2:2 R:2")[i % 4]); lh(b, "x-------x-------"); pad(b)
        if i < 8: laid(b, i); bass(b, BLD[i % 4])
        else: full(b, i)
        if i >= 12: BT[0] = DIRT; bass(b, BPG[i % 4]); BT[0] = SUB
        if last: perc(b, "X...X...X.X.XXXX", "x.x.x.x.xxxxXXXX"); fxh(b, 0, "riser", 4)
    elif n == "語り2":                                                   # 終わり: 3小節たたみかけて、全員で1打して止まる
        if i < 3: full(b, i, dirt=True, plk_=False); ct(PR, b, "0:0.5 0:0.5 2:0.5 3:0.5 0+:1 R:1"); lh(b, "x-..x-....x-....")
        else:
            perc(b, "X...............", "X..............."); SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:1 R:3"); DIRT.bar(b, f"{N(low(S.chords[b], 'E1') + 12)}:1 R:3"); ct(PR, b, "0:1 R:3"); lh(b, "x---............"); fxh(b, 0, "impact", 2)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: ピアノとシンセと効果音だけのインスト（190・ヘ短調・約3分55秒）。終電のあとの地下で、使われていない改札の奥から聞こえる低い音をたどって、だれも知らないフロアへ下りていく曲。"
          "打楽器の役は効果音（硬いキック・手びょうし・指パッチン・グリッチ）。形は、くじ（form_dice.py・種 2803）で決めた。ベースだけで始まり、全員で1打して止まる。自作")
V = Voice(S, vol=0.0, delay=0.0, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead" and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "tight"; js["human"] = 0.3
save(path, js)
