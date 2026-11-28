# UG 03「サンライズ・ステップ」（仮）Sunrise Step — インスト。Kawaii future bass。4分の4・190（ハーフで体感95のヒップホップのノリ）・ニ長調。
#
# 2026-11-28 人間「テンポ190ピアノはヒップホップみたいに。シンセ、FXを入れて。kawaiifutureベースで。間をしっかり開けて。細かい空間を開けたらそこにシンセを入れて
#   交互の刻みも1部入れる。コンセプトは新しい始まり、太陽に向かって。」
#   楽器: ピアノ（ヒップホップの刻み。はねて、短く、間をあける）／シンセ（低い正弦波のベース・うなるベース・スーパーソウの和音・ふくらむスーパーソウ・矩形波のプラック・夢のようなリード・グロッケン）／効果音（kawaiiFx）。
#   ピアノのすき間（16分で3マス以上の休み）に、シンセの粒（プラック）を1つ入れる。A1・A3・ソロ2は、ピアノ（表）とシンセ（裏）の交互の刻み。
#   kfbSawStab は使わない（入れるだけで曲全体の音が変わる。UG02 で分かった）。
# 形: くじ（tools/vt3/form_dice.py --skeleton 5211 220 190 --min-chorus 2 --not-start ピアノだけ）。始まり＝曲のいちばん静かな場面から／終わり＝フックをくり返しながら消えていく。
#   リズム: くじは twobeat だったが、UG02 と同じになるので、ヒップホップのあと乗りのハーフ（16分のはね）を自分で書いた。
# 物語: 夜明け前の暗さから、一歩ずつ太陽に向かって歩き出す。サビ4で朝日が昇りきる。
# この曲だけのもの: 1小節ごとに半音ずつ上がる「日の出のスイープ」（ふくらむスーパーソウ）。曲の中で2回だけ（サビ4の前・終わりのフックの前）。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("39", "sunrise", "サンライズ・ステップ（仮）", "Sunrise Step", 190, 4, "D", "major", "インスト（Kawaii future bass）")
S.flags = S.flags + " --space room --space-wet 0.12"
KA = Key("D", "major")
CH = ["Gmaj7", "A/G", "F#m7", "Bm7", "Em7", "C", "Asus4", "A"]                         # サビ: IV → V/IV → iii → vi ／ ii → ♭VII → Vsus4 → V
CH4 = ["Gmaj7", "A/G", "F#m7", "Bm7", "Em7", "C", "D", "D"]                              # サビ4（日の出）: 最後に主和音へ着く
AA = ["D", "D/F#", "Gmaj7", "Gmaj7", "Em7", "Em7", "Asus4", "A"]
QQ = ["Bm7", "Bm7", "Gmaj7", "Gmaj7", "Em7", "Em7", "Asus4", "A"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("ソロ0", 12, "intro", ["Bm7", "Bm7", "Gmaj7", "Gmaj7", "Em7", "Em7", "Asus4", "A", "Bm7", "Gmaj7", "Asus4", "A"])
scene("にせ", 6, "pre", ["Em7", "Em7", "F#m7", "F#m7", "Asus4", "A"])
scene("新1", 6, "verse", ["D", "D/F#", "Gmaj7", "Em7", "Asus4", "A"])
scene("A1", 8, "verse", AA)
scene("ソロ1", 8, "break", ["Bm7", "Gmaj7", "D", "A", "Bm7", "Gmaj7", "Em7", "A"])
scene("新2", 4, "pre", ["Gmaj7", "A", "Bm7", "A"])
scene("A2", 16, "verse", AA + ["Bm7", "Bm7", "F#m7", "F#m7", "Gmaj7", "Gmaj7", "Asus4", "A"])
scene("止1", 2, "bridge", ["A", "A"])
scene("早口1", 16, "verse", ["Bm7", "Bm7", "Gmaj7", "Gmaj7", "D", "D", "A/C#", "A/C#", "Bm7", "Bm7", "Gmaj7", "Gmaj7", "Em7", "Em7", "Asus4", "A"])
scene("サビ1", 8, "chorus", CH)
scene("A3", 16, "verse", AA * 2)
scene("サビ2", 8, "chorus", CH)
scene("静か1", 8, "bridge", QQ)
scene("止2", 1, "bridge", ["A"])
scene("サビ3", 10, "chorus", CH + ["Asus4", "A"])
scene("ソロ2", 8, "break", ["Bm7", "Gmaj7", "D", "A", "Bm7", "Gmaj7", "C", "A"])
scene("サビ4", 8, "chorus", CH4)
scene("フック1", 6, "break", ["Gmaj7", "A", "F#m7", "Bm7", "Em7", "A"])
scene("早口2", 8, "verse", ["Bm7", "Bm7", "Gmaj7", "Gmaj7", "D", "D", "Asus4", "A"])
scene("静か2", 8, "bridge", QQ)
scene("A4", 6, "verse", ["D", "D/F#", "Gmaj7", "Em7", "Asus4", "A"])
scene("フック2", 8, "outro", ["Gmaj7", "A", "F#m7", "Bm7", "Gmaj7", "A", "F#m7", "D"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

PN = [S.track(f"ピアノ（ヒップホップの刻み）{i + 1}", "piano", volume=0.15, pan=(-0.18, 0.0, 0.14, -0.06)[i], reverb=0.12,
              fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(4)]
PM = S.track("ピアノ（右手の短い句）", "piano", volume=0.3, pan=-0.1, reverb=0.14)
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.2, pan=0, gainDb=-6)
GRW = S.track("シンセのベース（うなる）", "bass", patch="kfbGrowlBass", volume=0.09, pan=0, gainDb=-8, fx=[{"type": "filter", "kind": "lowpass", "freq": 3000, "q": 0.6}])
BT = [SUB]
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.075, pan=(-0.4, 0.4, -0.15, 0.15)[i], reverb=0.2, duck=0.35,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(4)]
SWL = S.track("ふくらむスーパーソウ（日の出のスイープ）", "pad", patch="kfbSupersawSwell", volume=0.07, pan=0, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
PLK = S.track("矩形波のプラック（すき間の粒・交互の刻み）", "lead", patch="kfbSquarePluck", volume=0.085, pan=0.28, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
LEAD = S.track("夢のようなリード", "lead", patch="kfbDreamLead", volume=0.16, mono=True, pan=0.08, reverb=0.28, fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}])
GLK = S.track("グロッケン", "keys", patch="kfbGlocken", volume=0.05, pan=0.35, reverb=0.4, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
FX = lambda name, v, pn=0.0: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=0.08, modulate=False)
FK, FSN, FCL, FH, FSH = FX("効果音（キック）", 0.13), FX("効果音（スネア）", 0.08, 0.04), FX("効果音（手びょうし）", 0.06, -0.06), FX("効果音（ハイハット）", 0.04, 0.22), FX("効果音（シェイカー）", 0.03, -0.25)
FKW = FX("効果音（かわいい音: あわ・きらめき・きゅっ）", 0.045, 0.3)
FXT = S.track("効果音（上がる音・下がる音・逆回しのシンバル・当たる音・低く落ちる音・針の音）", "guitar", patch="kawaiiFx", volume=0.065, pan=0.1, reverb=0.3, modulate=False)
N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "down": "G4", "rev": "G#4", "impact": "G5", "subdrop": "G#5", "vinyl": "A#5", "spark": "D4", "drop": "C#4"}
def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))
mel = lambda s, up=1: KA.mel(s, oct=3 + up)                                           # リード: 1＝D4


def grid(tr, b, pat, key):
    out = []; i = 0; pat = pat.replace(" ", ""); assert len(pat) == 16, pat
    while i < 16:
        if pat[i] in "Xx": out.append(f"{key}:0.25" + ("!" if pat[i] == "X" else "")); i += 1
        else:
            L = 1
            while i + L < 16 and pat[i + L] not in "Xx": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    tr.bar(b, " ".join(out))


# ヒップホップのハーフ（キックはずらし、スネアは3拍め、ハイハットは8分）。はねは js["swing16"] で
KP = ("X......X..X.....", "X.........X..X..", "X......X..X...x.", "X..X......X.....")
def hh(b, i, hat=True, clap=False, shaker=False, roll=False):
    grid(FK, b, KP[i % 4], "A4")
    grid(FSN, b, "........X......." if not roll else "........X.x.xxxx", "A#4")
    if clap: grid(FCL, b, "........X.......", "B4")
    if hat: grid(FH, b, ("x.x.x.x.x.x.x.xx", "x.x.x.x.x.x.x.x.")[i % 2], "C#5")
    if shaker: grid(FSH, b, ".x.x.x.x.x.x.x.x", "C6")
def kawaii(b, pat, key="C4"): grid(FKW, b, pat, key)


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


BK = {0: "r-----.r..r-....", 1: "r---------r--5-.", 2: "r------r..r---7-", 3: "r--R------r-...."}           # ベースはキックにそろえる
def bass(b, pat):
    ch = S.chords[b]; r = low(ch, "E1"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 7
    off = {"r": 0, "3": t3, "5": 7, "7": 10, "R": 12}; out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + off[pat[i]])}:{L * 0.25:g}" + ("!" if i % 8 == 0 else "")); i += L
    BT[0].bar(b, " ".join(out))


def _ch(tracks, b, pat, center, n, short=None):
    """和音を型で鳴らす（x＝鳴らす・-＝のばす・.＝休み）。short があれば、1つの音を short 拍までにする"""
    v = sorted(voice(S.chords[b], center, n))
    for j in range(n):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            if pat[i] == ".": out.append(f"R:{L * 0.25:g}")
            else:
                d = L * 0.25 if short is None else min(L * 0.25, short)
                out.append(f"{N(v[j])}:{d:g}");
                if L * 0.25 - d > 1e-6: out.append(f"R:{L * 0.25 - d:g}")
            i += L
        tracks[j].bar(b, " ".join(out))


# ---- ヒップホップのピアノ: 短く刻んで、間をあける。16分で3マス以上あいた所の1つに、シンセの粒を入れる ----
HP = ("x--x--x.........", "x-----..x--x....", "..x--x......x-..", "x--x.......x-...")
def hip(b, k, center=62, fill=True):
    pat = HP[k % 4]; _ch(PN, b, pat, center, 4, short=0.5)
    if not fill: return
    t = sorted(voice(S.chords[b], 79, 4)); gaps = []; i = 0
    while i < 16:
        if pat[i] == ".":
            j = i
            while j < 16 and pat[j] == ".": j += 1
            if j - i >= 3: gaps.append((i + 1, j - i - 1))
            i = j
        else: i += 1
    if not gaps: return
    at, room = gaps[(k + b) % len(gaps)]; nt = t[(k + b) % 4]; out = []
    if at: out.append(f"R:{at * 0.25:g}")
    out.append(f"{N(nt)}:0.25"); rest = 16 - at - 1
    if room >= 3 and (b % 2): out.append(f"{N(t[(k + b + 1) % 4])}:0.25"); rest -= 1     # 広いすき間には2つ
    if rest: out.append(f"R:{rest * 0.25:g}")
    PLK.bar(b, " ".join(out))


def alt(b, k=0, center=62):
    """交互の刻み: ピアノは表の8分、シンセのプラックは裏の8分（3拍めのあとは休んで間をあける）"""
    pp = ("x.......x.......", "x...x...x.......", "x.......x...x...", "x...x.......x...")[k % 4]
    sp = ("..x...x...x.....", "..x...x...x...x.", "..x...x...x.....", "..x.......x...x.")[k % 4]
    _ch(PN, b, pp, center, 4, short=0.25)
    t = sorted(voice(S.chords[b], 79, 4)); out = []; i = 0; c = 0
    while i < 16:
        if sp[i] == "x": out.append(f"{N(t[c % 4])}:0.25"); c += 1; i += 1
        else:
            L = 1
            while i + L < 16 and sp[i + L] != "x": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    PLK.bar(b, " ".join(out))


def saw(b, pat="x..x..x...x..x..", center=66): _ch(SAW, b, pat, center, 4, short=0.5)       # future bass の和音の刻み（キックでへこむ）
def glk(b): GLK.bar(b, " ".join(f"{N(x)}:0.5" for x in sorted(voice(S.chords[b], 86, 4)) * 2))


def ct(tr, b, cell, center=72, up=0):
    v = sorted(voice(S.chords[b], center, 4)); out = []
    for x in cell.split():
        a, L = x.split(":")
        if a == "R": out.append(x); continue
        out.append(f"{N(v[int(a[0])] + 12 * (a.count('+') - a.count('-')) + up)}:{L}")
    assert abs(sum(float(x.split(':')[1]) for x in out) - 4) < 1e-6, cell
    tr.bar(b, " ".join(out))


def theme(name, lines, tr=None, up=1, start=0):
    bars = S.sc(name)[start:]; ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) <= len(bars), (name, len(ls), len(bars))
    for b, l in zip(bars, ls):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l != "R:4": (tr or LEAD).bar(b, mel(l, up))


# ---- 旋律（夢のようなリード。1＝D4）。長い音は和音の音、明るく上へ ----
NEW1 = ["R:2 3:0.75 5:0.75 1':0.5", "3':2 2':1 R:1", "R:1 5:0.5 1':0.5 3':2", "R:4", "R:2 4:0.75 6:0.75 1':0.5", "7:2 R:2"]                          # 3小節の句
A1L = ["3:0.25 3:0.25 3:0.25 R:0.25 1':1 7:1 R:1", "R:4", "5:0.25 5:0.25 5:0.25 R:0.25 3':1 2':1 R:1", "R:4",
       "2:0.25 2:0.25 2:0.25 R:0.25 7:1 6:1 R:1", "R:4", "4:0.25 4:0.25 4:0.25 R:0.25 2':1 1':1 R:1", "R:4"]                                     # 同じ音を連打してから跳ぶ
NEW2 = ["R:2 5:0.75 6:0.75 7:0.5", "1':1.5 R:2.5", "R:2 3':0.75 2':0.75 1':0.5", "7:2 5:1 R:1"]                                                      # 小節のまん中から
A2L = ["R:1 1:0.5 3:0.5 5:1 1':1", "3':2 R:2", "R:1 5:0.5 7:0.5 2':1 3':1", "2':2 7:2", "1':3 R:1",                                                 # 5小節の句
       "R:1 3:0.5 5:0.5 1':1 3':1", "5':2 4':1 3':1", "R:1 2':0.5 3':0.5 2':1 7:1", "1':2 7:1 6:1", "7:3 R:1",
       "R:1 4:0.5 6:0.5 1':1 3':1", "2':2 R:2", "R:1 5:0.5 7:0.5 2':1 4':1", "3':2 2':2", "5:2 6:1 7:1", "R:4"]
FAST = ["R:3 3:0.5 5:0.5", "1':0.75 7:0.75 5:0.5 R:2", "R:3 5:0.5 7:0.5", "2':0.75 1':0.75 7:0.5 R:2"]                                              # 1拍早く食って入る
CHO1 = ["R:2 5:0.5 1':0.5 3':1", "2':1.5 1':1 R:1.5", "R:2 3':0.5 5':0.5 3':1", "2':2 R:2", "R:2 2':0.5 3':0.5 5':1", "3':1.5 1':1 R:1.5", "R:2 1':0.5 2':0.5 4':1", "3':3 R:1"]   # 小節のまん中から
CHO2 = ["1':1 3':1 5':1.5 3':0.5", "2':2 R:2", "3':1 5':1 7':1.5 5':0.5", "4':2 R:2", "2':1 3':1 5':1.5 1'':0.5", "7':2 R:2", "1':1 2':1 4':1.5 2':0.5", "3':4"]      # 2小節の句
A3L = ["R:1 3:0.5 5:0.5 1':2", "7:1 5:1 R:2", "R:1 4:0.5 6:0.5 1':1 3':1",                                                                         # 3小節の句
       "R:1 5:0.5 7:0.5 2':2", "1':1 6:1 R:2", "R:1 2':0.5 3':0.5 4':1 2':1",
       "R:1 3:0.5 5:0.5 1':2", "7:1 5:1 R:2", "R:1 4:0.5 6:0.5 1':1 3':1",
       "R:1 5:0.5 7:0.5 2':2", "1':1 6:1 R:2", "R:1 2':0.5 3':0.5 5':1 3':1", "R:4", "R:4", "R:4", "R:4"]
QUIET1 = ["3:1 1':3", "R:4", "3:1 2':3", "R:4", "2:1 1':3", "R:4", "1:1 7:3", "R:4"]                                                                 # 低い音から6度以上跳ぶ
CHO3 = ["3':0.5 3':0.5 3':0.5 R:0.5 5':1 3':1", "2':2 R:2", "5':0.5 5':0.5 5':0.5 R:0.5 1'':1 7':1", "5':2 R:2",
        "4':0.5 4':0.5 4':0.5 R:0.5 1'':1 7':1", "5':2 R:2", "4':0.5 4':0.5 4':0.5 R:0.5 6':1 5':1", "R:4", "2':0.5 2':0.5 2':0.5 R:0.5 5':1 4':1", "3':3 R:1"]   # 連打して跳ぶ
CHO4 = ["1':0.5 3':0.5 5':1 R:2", "2':0.5 4':0.5 6':1 R:2", "3':0.5 5':0.5 7':1 R:2", "4':0.5 6':0.5 1'':1 R:2",                                      # 1小節の短い句をたたみかける（日の出）
        "5':0.5 7':0.5 2'':1 R:2", "5':0.5 1'':0.5 3'':1 R:2", "3'':2 2'':1 1'':1", "1'':4"]
HOOK = ["5':0.5 R:0.25 5':0.25 R:0.5 3':0.5 R:0.5 5':0.5 R:1", "6':0.5 R:0.25 6':0.25 R:0.5 5':0.5 3':1 R:1",
        "5':0.5 R:0.25 5':0.25 R:0.5 3':0.5 R:0.5 2':0.5 R:1", "3':0.5 R:0.25 2':0.25 R:0.5 1':0.5 R:2", "2':0.5 R:0.25 2':0.25 R:0.5 3':0.5 5':1 R:1", "6':0.5 5':0.5 7':2 R:1"]
QUIET2 = ["3':4", "2':2 1':2", "7:4", "R:4", "3':4", "5':2 3':2", "4':4", "3':2 R:2"]                                                                  # 4小節のばす長い句
FAST2 = ["R:3 3:0.25 3:0.25 3:0.25 5:0.25", "1':1 7:1 R:2", "R:3 5:0.25 5:0.25 5:0.25 1':0.25", "3':1 2':1 R:2",
         "R:3 1:0.25 1:0.25 1:0.25 5:0.25", "1':1 7:1 R:2", "R:3 2:0.25 2:0.25 2:0.25 4:0.25", "3':2 R:2"]
A4L = ["R:3 3:0.5 5:0.5", "1':2 7:1 R:1", "R:3 5:0.5 7:0.5", "2':2 1':1 R:1", "R:3 2':0.5 3':0.5", "2':2 R:2"]

theme("新1", NEW1); theme("A1", A1L); theme("新2", NEW2); theme("A2", A2L); theme("早口1", FAST * 4); theme("サビ1", CHO1); theme("A3", A3L)
theme("サビ2", CHO2); theme("静か1", QUIET1); theme("サビ3", CHO3); theme("サビ4", CHO4); theme("フック1", HOOK); theme("早口2", FAST2); theme("静か2", QUIET2)
theme("A4", A4L); theme("フック2", HOOK + HOOK[:2])
SOLO = ["0+:0.5 R:0.25 2:0.25 3:0.5 R:0.5 0+:0.5 1+:0.5 R:1", "2+:1 R:0.5 1+:0.25 0+:0.25 3:1 R:1", "3:0.25 0+:0.25 1+:0.25 2+:0.25 R:1 3+:1 R:1", "2+:1.5 1+:0.5 0+:1 R:1"]
PMC = ["R:2 0:0.25 1:0.25 2:0.5 R:1", "R:4", "R:2 1:0.25 2:0.25 3:0.5 R:1", "R:4"]                                     # ピアノの右手: 短い答え（リードの休みの所で）
SWEEP_N = []


def sweep(b0, n=4):
    """日の出のスイープ: ふくらむスーパーソウを、1小節ごとに半音ずつ上げてのばす（A4 → B♭4 → B4 → C5。次の場面で D の和音へ着く）"""
    for k in range(n): SWL.bar(b0 + k, f"{N(69 + k)}:4")


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "ソロ0":                                                     # いちばん静か: ヒップホップのピアノだけ（はねて・短く・間をあけて）＋針の音。すき間にシンセの粒
        hip(b, i, fill=i >= 2)
        if i == 0: fxh(b, 0, "vinyl", 4)
        if i >= 4: grid(FH, b, "x.x.x.x.x.x.x.x." if i >= 8 else "x...x...x...x...", "C#5")        # v2: 前奏が -24dB と小さすぎたので、4小節めからハイハット、6小節めからベースとキック
        if i >= 6: bass(b, BK[i % 4]); grid(FK, b, KP[i % 4], "A4")
        if i >= 8: grid(FSN, b, "........X.......", "A#4")
        if last: fxh(b, 0, "riser", 4)
    elif n == "にせ":                                                    # 上げる → 最後の2小節で静かに落とす
        if i < 4: hip(b, i); hh(b, i, roll=i == 3); bass(b, BK[i % 4]); SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 7)}:4")
        else: hip(b, i, fill=False); kawaii(b, "..........x.....", "D4")
        if i == 3: fxh(b, 0, "riser", 4)
    elif n in ("新1", "新2", "A2", "早口1", "早口2", "A4"):
        hh(b, i, hat=n != "新1" or i >= 2, shaker=n in ("A2", "早口2")); bass(b, BK[i % 4]); hip(b, i)
        if n in ("A2", "早口1") and i >= 8: saw(b, "x.......x.......")
        if n == "早口2" and i % 4 == 3: kawaii(b, "............x.x.", "E4")
        if last: fxh(b, 0, "riser", 4)
    elif n in ("A1", "A3"):                                              # 交互の刻み（ピアノ＝表、シンセ＝裏）
        hh(b, i, hat=False); bass(b, BK[i % 4]); alt(b, i)
        if n == "A3" and i >= 12: ct(PM, b, PMC[i % 4], center=74)
        if i % 4 == 2: kawaii(b, "..............x.", "C4")
        if last: fxh(b, 0, "riser", 4)
    elif n in ("ソロ1", "ソロ2"):                                        # ソロ1＝リードのソロ／ソロ2＝ピアノとリードのかけ合い（交互）
        hh(b, i, clap=True); bass(b, BK[i % 4]); saw(b, "x.......x..x....")
        if n == "ソロ1": ct(LEAD, b, SOLO[i % 4], center=74); hip(b, i, fill=False)
        else:
            if i % 2 == 0: ct(LEAD, b, SOLO[i % 4], center=74)
            else: ct(PM, b, SOLO[(i + 1) % 4], center=74)
            alt(b, i) if i % 2 else hip(b, i, fill=False)
        if i == 0: fxh(b, 0, "impact", 2)
        if last: fxh(b, 0, "rev", 4)
    elif n in ("止1", "止2"):                                            # 全部止まる。最後に「きゅっ」とひとつ
        kawaii(b, "............x...", "E4")
        if last: fxh(b, 0, "rev", 4) if n == "止1" else None
    elif n in ("サビ1", "サビ2", "サビ3", "サビ4"):
        hot = n in ("サビ3", "サビ4"); hh(b, i, clap=True, shaker=hot); BT[0] = GRW if n == "サビ4" else SUB; bass(b, BK[i % 4]); BT[0] = SUB
        if n == "サビ4": SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:4")
        saw(b); hip(b, i, center=60, fill=False)
        if hot or i >= 4: glk(b) if i % 2 else None
        if i == 0: fxh(b, 0, "impact", 2)
        if last and n != "サビ4": fxh(b, 0, "down", 4)
    elif n in ("静か1", "静か2"):                                        # 静か: ピアノの刻みは減らし、パッドのようにスーパーソウをのばす
        hip(b, i, fill=i % 2 == 1); _ch(SAW, b, "x---------------", 64, 4) if n == "静か2" else None
        if n == "静か1" and i >= 4: grid(FH, b, "x...x...x...x...", "C#5")
        if last: fxh(b, 2, "rev", 2)
    elif n in ("フック1", "フック2"):
        out = n == "フック2"; hh(b, i, clap=True, hat=not (out and i >= 6), shaker=not out); bass(b, BK[i % 4]); saw(b, "x..x..x...x..x..")
        hip(b, i, center=60)
        if i == 0: fxh(b, 0, "impact", 2)
        if n == "フック1" and last: fxh(b, 0, "riser", 4)

sweep(S.sc("ソロ2")[-4])           # サビ4の前の4小節
sweep(S.sc("A4")[-4])                                                    # 終わりのフックの前の4小節

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 8
S.desc = ("仮: Kawaii future bass のインスト（190・ニ長調・ハーフのヒップホップのノリ）。夜明け前から、一歩ずつ太陽に向かって歩き出す曲。ヒップホップのピアノが間をあけて刻み、"
          "すき間にシンセの粒が入る。ピアノとシンセの交互の刻みも。形は、くじ（form_dice.py・種 5211）で決めた。いちばん静かな場面から始まり、フックをくり返しながら消えていく。自作")
V = Voice(S, vol=0.0, delay=0.0, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead" and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "laidback"; js["human"] = 0.4; js["swing16"] = 0.9                   # ヒップホップのはね（16分のウラを後ろへ）とあと乗り
save(path, js)
