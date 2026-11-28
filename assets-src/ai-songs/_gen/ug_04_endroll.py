# UG 04「エンドロールは踊りながら」（仮）Dancing Through the End Credits — インスト。ダンスポップ × Kawaii future bass。4分の4・120・ヘ長調 → 最後のドロップからト長調。
#
# 2026-11-28 人間「次はダンスポップ。kawaiifutureベースで、ピアノ、シンセ、FX、テンポ120。コンセプト、ハッピーエンド。」
#   楽器: ピアノ（ハウスふうの和音の刻み・右手の短い句）／シンセ（低い正弦波のベース・スーパーソウの和音・ふくらむスーパーソウ・矩形波のリード・矩形波のプラック・グロッケン）／効果音（kawaiiFx）。
#   kfbSawStab は使わない（入れるだけで曲全体の音が変わる。UG02 で分かった）。歌の指定がないのでインスト。
# 形: くじ（tools/vt3/form_dice.py --skeleton 6120 210 120 --min-chorus 3 --not-start ベース --not-start ピアノ --not-start 静か --not-groove twobeat --not-groove laid）。
#   始まり＝ドラムだけ（4小節を足した）／終わり＝新しい旋律を最後に1回だけ鳴らして終わる／リズム＝まっすぐ4つ打ち（主）・3・3・2（静かな場面）
# 物語: 長い物語のハッピーエンド。エンドロールが流れはじめても、みんな踊りやめない。最後のドロップで調が1音上がる。
# この曲だけのもの: 最後のドロップでの1音上の転調／サビの D7（II7）と A♭maj7（♭VI）の明るい寄り道。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("40", "endroll", "エンドロールは踊りながら（仮）", "Dancing Through the End Credits", 120, 4, "F", "major", "インスト（ダンスポップ）")
S.flags = S.flags + " --space room --space-wet 0.1"
KF = Key("F", "major"); KG = Key("G", "major")
CH = ["Bbmaj7", "C/Bb", "Am7", "D7", "Gm7", "Abmaj7", "C/Bb", "F"]                      # サビ: IV → V/IV → iii → II7 ／ ii → ♭VI → V/IV → I
CHE = ["Dm7", "Dm7", "Bbmaj7", "Bbmaj7", "F", "F", "C", "C", "Gm7", "Abmaj7", "Bb", "C"]     # 新1
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("ドラム", 4, "intro", ["F"] * 4)
scene("新1", 12, "verse", CHE)
scene("立ち上げ1", 8, "pre", ["Gm7", "Gm7", "Am7", "Am7", "Bbmaj7", "Bbmaj7", "C", "C"])
scene("フック1", 6, "break", ["Bbmaj7", "C", "Am7", "Dm7", "Gm7", "C"])
scene("サビ別", 10, "chorus", ["Dm7", "C", "Bbmaj7", "C", "Dm7", "C", "Bbmaj7", "Abmaj7", "Bb", "C"])
scene("立ち上げ2", 8, "pre", ["Gm7", "Gm7", "Am7", "Am7", "Bbmaj7", "Bbmaj7", "C", "C"])
scene("サビ1", 16, "chorus", CH * 2)
scene("ドロップ1", 6, "break", ["F", "F", "Dm7", "Dm7", "Bbmaj7", "C"])
scene("サビ半", 8, "chorus", CH)
scene("A", 6, "verse", ["F", "C/E", "Dm7", "Bbmaj7", "Gm7", "C"])
scene("静か", 4, "bridge", ["Bbmaj7", "Bbmaj7", "Gm7", "D7"])                                # 最後の D7 が、次のト長調への入口
scene("ドロップ2", 12, "break", ["G", "G", "Em7", "Em7", "Cmaj7", "D", "G", "G", "Em7", "Em7", "Cmaj7", "D"])
scene("語り", 7, "outro", ["Cmaj7", "D/C", "Bm7", "E7", "Am7", "D", "G"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

PN = [S.track(f"ピアノ（ハウスの刻み）{i + 1}", "piano", volume=0.15, pan=(-0.2, 0.0, 0.16, -0.08)[i], reverb=0.12) for i in range(4)]
PL = S.track("ピアノ（左手の根音）", "piano", volume=0.16, pan=-0.05, reverb=0.1)
PM = S.track("ピアノ（右手の短い句）", "piano", volume=0.28, pan=-0.12, reverb=0.14)
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.21, pan=0, gainDb=-5)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.07, pan=(-0.4, 0.4, -0.15, 0.15)[i], reverb=0.2, duck=0.4,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(4)]
SWL = S.track("ふくらむスーパーソウ", "pad", patch="kfbSupersawSwell", volume=0.065, pan=0, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
LEAD = S.track("矩形波のリード", "lead", patch="kfbSquareLead", volume=0.11, mono=True, pan=0.06, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 3800, "q": 0.6}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}])
PLK = S.track("矩形波のプラック", "lead", patch="kfbSquarePluck", volume=0.085, pan=0.28, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
GLK = S.track("グロッケン", "keys", patch="kfbGlocken", volume=0.05, pan=0.35, reverb=0.4, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
FX = lambda name, v, pn=0.0: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=0.08, modulate=False)
FK, FCL, FSN, FOH, FSH = FX("効果音（キック）", 0.14), FX("効果音（手びょうし）", 0.075, 0.05), FX("効果音（スネア）", 0.06, -0.04), FX("効果音（開いたハイハット）", 0.04, 0.22), FX("効果音（シェイカー）", 0.03, -0.25)
FKW = FX("効果音（かわいい音: あわ・きらめき）", 0.045, 0.3)
FXT = S.track("効果音（上がる音・下がる音・逆回しのシンバル・当たる音・低く落ちる音）", "guitar", patch="kawaiiFx", volume=0.065, pan=0.1, reverb=0.3, modulate=False)
N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "down": "G4", "rev": "G#4", "impact": "G5", "subdrop": "G#5", "spark": "D4"}
def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))


def grid(tr, b, pat, key):
    out = []; i = 0; pat = pat.replace(" ", ""); assert len(pat) == 16, pat
    while i < 16:
        if pat[i] in "Xx": out.append(f"{key}:0.25" + ("!" if pat[i] == "X" else "")); i += 1
        else:
            L = 1
            while i + L < 16 and pat[i + L] not in "Xx": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    tr.bar(b, " ".join(out))


def four(b, i, clap=True, oh=True, sh=True, roll=None):
    grid(FK, b, "X...X...X...X...", "A4")
    if clap: grid(FCL, b, "....X.......X...", "B4")
    if oh: grid(FOH, b, "..x...x...x...x.", "D5")
    if sh: grid(FSH, b, ("x.xxx.xxx.xxx.xx", "x.xxx.xxx.xxx.x.")[i % 2], "C6")
    if roll: grid(FSN, b, roll, "A#4")
def tres(b, i):                                                         # 静かな場面: 3・3・2
    grid(FK, b, "X..X..X.........", "A4"); grid(FCL, b, "............X...", "B4"); grid(FSH, b, "x.x.x.x.x.x.x.x.", "C6")
def kawaii(b, pat, key="C4"): grid(FKW, b, pat, key)


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


BH = ("r..r..r.r..r..R.", "r..r..5.r..r..R.", "r..r..r.r..5..R.", "r..r..R.r..r.5R.")                  # ハウスのベース（キックをよけて、はねる）
def bass(b, pat):
    ch = S.chords[b]; r = low(ch, "E1"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 7
    off = {"r": 0, "3": t3, "5": 7, "7": 10, "R": 12}; out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + off[pat[i]])}:{min(L * 0.25, 0.5):g}" + (f" R:{L * 0.25 - 0.5:g}" if L * 0.25 > 0.5 else "") + ("" if True else "")); i += L
    SUB.bar(b, " ".join(out))


def _ch(tracks, b, pat, center, n, short=None):
    v = sorted(voice(S.chords[b], center, n))
    for j in range(n):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            if pat[i] == ".": out.append(f"R:{L * 0.25:g}")
            else:
                d = L * 0.25 if short is None else min(L * 0.25, short)
                out.append(f"{N(v[j])}:{d:g}")
                if L * 0.25 - d > 1e-6: out.append(f"R:{L * 0.25 - d:g}")
            i += L
        tracks[j].bar(b, " ".join(out))


HP = ("x..x..x...x..x..", "x..x..x...x.x...", "x..x..x...x..x..", "..x..x..x...x...")              # ハウスのピアノの刻み
def piano(b, k, center=64, root=True):
    _ch(PN, b, HP[k % 4], center, 4, short=0.25)
    if root: PL.bar(b, f"{N(low(S.chords[b], 'E2') + 12)}:0.5 R:1.5 {N(low(S.chords[b], 'E2') + 12)}:0.5 R:1.5")
def saw(b, pat="x...x...x...x...", center=67): _ch(SAW, b, pat, center, 4, short=0.75)            # キックでへこむ（ポンプ）
def glk(b): GLK.bar(b, " ".join(f"{N(x)}:0.5" for x in sorted(voice(S.chords[b], 86, 4)) * 2))
def arp(b, k=0):
    t = sorted(voice(S.chords[b], 76, 4)); up = [t[0], t[1], t[2], t[3], t[0] + 12, t[1] + 12, t[2] + 12, t[3] + 12]
    PLK.bar(b, ("R:2 " if k % 2 else "") + " ".join(f"{N(x)}:0.25" for x in up) + (" R:2" if not k % 2 else ""))


def theme(name, lines, key=KF, tr=None, up=1):
    bars = S.sc(name); ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) <= len(bars), (name, len(ls), len(bars))
    for b, l in zip(bars, ls):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l != "R:4":
            (tr or LEAD).bar(b, key.mel(l, oct=3 + up))
            if tr is None: PM.bar(b, key.mel(l, oct=3 + up))                       # v2: 旋律をピアノでも重ねる（矩形波だけだと細く、点が低かった）


# ---- 旋律（1＝F4。G の場面は 1＝G4）。長い音は和音の音、明るく ----
NEW1 = ["5':0.75 3':0.75 2':0.5 1':0.75 6:1.25", "R:0.5 5:1.5 R:2", "4':0.75 3':0.75 1':0.5 6:0.75 5:1.25", "R:0.5 3:1.5 R:2", "5':0.75 4':0.75 3':0.5 1':0.75 5:1.25", "R:0.5 6:1.5 R:2",
        "4':0.75 3':0.75 2':0.5 7:0.75 5:1.25", "R:0.5 1':1.5 R:2", "4':0.75 3':0.75 2':0.5 1':0.75 6:1.25", "R:0.5 b3':1.5 R:2", "4':0.75 2':0.75 1':0.5 6:0.75 4:1.25", "R:0.5 5:3.5"]
HOOK = ["R:0.25 3':0.5 R:0.25 5':0.5 R:0.5 3':0.5 2':1.5", "R:0.25 5:0.5 R:0.25 7:0.5 R:0.5 2':0.5 3':1.5", "R:0.25 1':0.5 R:0.25 3':0.5 R:0.5 5':0.5 6':1.5",
        "5':0.75 4':0.75 3':2.5", "R:0.25 2':0.5 R:0.25 4':0.5 R:0.5 6':0.5 5':1.5", "5':2.5 R:1.5"]
CHA = ["R:0.25 6:0.25 1':0.5 2':1 R:2", "R:0.25 3':0.25 5':0.5 5':1 R:2", "R:0.25 4':0.25 3':0.5 1':1 R:2", "R:0.25 7:0.25 2':0.5 5':1 R:2", "R:0.25 6:0.25 1':0.5 3':1 R:2",
       "R:0.25 3':0.25 5':0.5 6':1 R:2", "R:0.25 5':0.25 4':0.5 2':1 R:2", "R:0.25 b3':0.25 4':0.5 b3':1 R:2", "2':0.75 1':0.75 2':0.5 4':2", "5':4"]
CHO = ["R:1.5 3':0.75 5':0.75 6':1", "6':1.5 5':2.5", "R:1.5 1':0.75 3':0.75 4':1", "#4':3.5 R:0.5", "R:1.5 2':0.75 4':0.75 5':1", "b3':1.5 1':2.5", "R:1.5 2':0.75 3':0.75 5':1", "1':3.5 R:0.5"]                              # 休みから入って最後をのばす
CHH = ["R:2.5 3':0.75 4':0.75", "5':3.5 R:0.5", "R:2.5 1':0.75 3':0.75", "#4':3.5 R:0.5", "R:2.5 4':0.75 5':0.75", "b3':3.5 R:0.5", "R:2.5 3':0.75 2':0.75", "1':3.5 R:0.5"]                                       # 半分の速さ: 小節のまん中から
AL = ["1':0.75 3':0.75 5':0.5 3':2", "2':1.5 R:2.5", "6:0.75 1':0.75 3':0.5 2':2", "1':1.5 R:2.5", "4:0.75 6:0.75 2':0.5 1':2", "7:1.5 R:2.5"]                               # 2小節の句
QL = ["R:2.5 3':0.75 5':0.75", "6':3.5 R:0.5", "R:2.5 4':0.75 2':0.75", "#1':3.5 R:0.5"]                                                                                            # 静か（D7 の上で C# ＝ 3度）
DR2 = ["R:1.5 5:0.25 1':0.25 3':2", "5':1.5 R:2.5", "R:1.5 5:0.25 7:0.25 2':2", "3':1.5 R:2.5", "R:1.5 3':0.25 5':0.25 1'':2", "7':1.5 R:2.5"]                              # ドロップ2（ト長調）
FIN = ["R:0.5 3':0.5 3':0.5 5':0.5 R:0.5 1'':1.5", "7':2 R:2", "R:0.5 2':0.5 2':0.5 4':0.5 R:0.5 6':1.5", "#5':2 R:2", "R:0.5 1':0.5 1':0.5 3':0.5 R:0.5 6':1.5", "5':2 6':1 7':1", "1'':4"]  # 新しい旋律（1回だけ）

theme("新1", NEW1); theme("フック1", HOOK); theme("サビ別", CHA); theme("サビ1", CHO * 2); theme("サビ半", CHH); theme("A", AL); theme("静か", QL)
theme("ドロップ2", DR2 * 2, key=KG); theme("語り", FIN, key=KG)

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "ドラム":                                                    # ドラムだけ。3小節めから手びょうし・4小節めにかわいい音
        four(b, i, clap=i >= 2, oh=i >= 1, sh=i >= 3)
        if i == 3: kawaii(b, "............x.x.", "D4"); fxh(b, 2, "rev", 2)
    elif n == "新1":
        four(b, i, sh=i >= 4); bass(b, BH[i % 4]); piano(b, i)
        if i >= 8: arp(b, i)
        if last: fxh(b, 0, "riser", 4)
    elif n in ("立ち上げ1", "立ち上げ2"):                                # 上がっていく: スネアの連打が細かくなり、ふくらむスーパーソウ
        roll = ("X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XXXXXXXXXXXXXXXX")[i // 2]
        four(b, i, clap=i < 6, sh=False, roll=roll); bass(b, BH[i % 4] if i < 6 else "r.......r......."); piano(b, i)
        SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12 + 7)}:4")
        if i == 4: fxh(b, 0, "riser", 4)
        if last: kawaii(b, "x.x.x.x.xxxxxxxx", "D4")
    elif n in ("フック1", "ドロップ1"):
        four(b, i); bass(b, BH[i % 4]); piano(b, i, center=60); saw(b, "x..x..x...x..x..")
        if n == "ドロップ1": arp(b, i)
        if i == 0: fxh(b, 0, "impact" if n == "フック1" else "subdrop", 2 if n == "フック1" else 4)
        if last: fxh(b, 0, "down", 4)
    elif n in ("サビ別", "サビ1"):
        four(b, i); bass(b, BH[i % 4]); piano(b, i); saw(b)
        if i % 2 == 1: glk(b)
        if n == "サビ1" and i >= 8: arp(b, i)
        if i == 0: fxh(b, 0, "impact", 2)
        if i % 4 == 3: kawaii(b, "..............x.", "C4")
        if last and n == "サビ別": fxh(b, 0, "down", 4)
    elif n == "サビ半":                                                  # 半分の速さ: キックは1と3、手びょうしは3
        grid(FK, b, "X.......X.......", "A4"); grid(FCL, b, "........X.......", "B4"); grid(FOH, b, "..x...x...x...x.", "D5")
        bass(b, "r.......r......."); SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4"); piano(b, i, root=False)   # v2: のばすスーパーソウの和音（5.63）をやめ、ふくらむ音1つに
        if last: fxh(b, 0, "riser", 4)
    elif n == "A":                                                       # 3・3・2 の場面
        tres(b, i); bass(b, "r..r..r.r..r..r."); piano(b, i)
        if last: kawaii(b, "........x.x.x.x.", "D4")
    elif n == "静か":                                                    # ピアノとふくらむスーパーソウだけ。最後の D7 で、ト長調への入口
        _ch(PN, b, "x---------------", 62, 4); SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4")
        if last: fxh(b, 0, "riser", 4)
    elif n == "ドロップ2":                                               # ハッピーエンド: 1音上がって、全員
        four(b, i); bass(b, BH[i % 4]); piano(b, i); saw(b); arp(b, i)
        if i % 2 == 1: glk(b)
        if i in (0, 6): fxh(b, 0, "impact", 2); kawaii(b, "x...............", "D4")
    elif n == "語り":                                                    # 新しい旋律を1回だけ。最後の小節で全員1打して、きらめきだけ残る
        if not last: four(b, i); bass(b, BH[i % 4]); piano(b, i); saw(b)
        else:
            grid(FK, b, "X...............", "A4"); grid(FCL, b, "X...............", "B4"); _ch(PN, b, "x---------------", 64, 4); SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:2 R:2")
            _ch(SAW, b, "x-------........", 67, 4); GLK.bar(b, " ".join(f"{N(x)}:0.5" for x in sorted(voice(S.chords[b], 86, 4))) + " R:2"); fxh(b, 0, "impact", 2)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: ダンスポップ × Kawaii future bass のインスト（120・ヘ長調 → 最後のドロップからト長調）。長い物語のハッピーエンド。エンドロールが流れても踊りやめない。"
          "ハウスふうのピアノの刻み、スーパーソウの和音。形は、くじ（form_dice.py・種 6120）で決めた。ドラムだけで始まり、新しい旋律を1回だけ鳴らして終わる。自作")
V = Voice(S, vol=0.0, delay=0.0, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead" and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "tight"; js["human"] = 0.3
save(path, js)
