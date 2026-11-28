# UG 05「ねえ、好きな人だれ？」（仮）Hey, Who Do You Like? — インスト。ヒップホップ × Kawaii future bass。4分の4・160・イ長調。
#
# 2026-11-28 人間「ブルーアーカイブの最初の曲みたいなテンポで間を使った、ヒップホップでkawaiifutureベースの曲。キーボード、シンセ、FXで。緩急間合い、楽器交互のきざみ。
#   テンポは160ぐらいで。コンセプトはあなたの好きな人は誰？」
#   参考の曲は「テンポと間の使い方」だけ（旋律・和音・音はまねしない。CLAUDE.md 1-1）。
#   楽器: キーボード（エレピ kfbGlassEp・オルゴール kfbMusicBox）／シンセ（低い正弦波のベース・スーパーソウ・ふくらむスーパーソウ・矩形波のプラック・夢のようなリード）／効果音（kawaiiFx）。
#   kfbSawStab は使わない。歌の指定がないのでインスト。
# 形: くじ（tools/vt3/form_dice.py --skeleton 7316 200 160 --min-chorus 2 --not-start ベース/ピアノ/静か/ドラム --not-groove four/twobeat/laid）。
#   始まり＝歌なしのフックを全員で／終わり＝くじは「新しい旋律で終わる」だったが UG04 と同じなので、物語に合わせて「解決しない和音で問いかけのまま止まる」に変えた。
#   リズム＝3・3・2（主）に 16分のはね（swing16 0.6）を足したヒップホップ／静かな場面と A は前のめりの8ビートをまばらに。
# 物語: 放課後、ふいに聞かれた「好きな人だれ？」。はぐらかしたり、答えかけたり。最後は答えを言わずに、問いかけのまま終わる。
# この曲だけのもの: 語尾が上がる2音の「だれ？」の動機（短い音 → 4度上の長い音）。キーボード・プラック・オルゴール・リードが曲のあちこちで投げ合う。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("41", "suki", "ねえ、好きな人だれ？（仮）", "Hey, Who Do You Like?", 160, 4, "A", "major", "インスト（ヒップホップ × Kawaii future bass）")
S.flags = S.flags + " --space room --space-wet 0.1"
KA = Key("A", "major")
CH = ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "E/G#", "Amaj7", "A7"]                       # サビ: IV → V → iii → vi ／ ii → V/3 → I → I7（次の IV へ寄りかかる）
CHQ = ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "Dm6"]                                       # 終わり: 最後は iv6（Dm6）で止まる＝問いかけ
AA = ["A", "A", "F#m7", "F#m7", "Dmaj7", "Dmaj7", "E", "E", "A", "C#7", "F#m7", "E"]
BB = ["Bm7", "C#m7", "Dmaj7", "E", "Bm7", "C#m7", "Dmaj7", "E/D"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("サビ0", 8, "chorus", CH)
scene("早口1", 8, "verse", ["F#m7", "F#m7", "Dmaj7", "Dmaj7", "A", "A", "E", "E"])
scene("ソロ1", 4, "break", ["Dmaj7", "E", "C#m7", "F#m7"])
scene("A1", 12, "verse", AA)
scene("サビ半", 8, "chorus", CH)
scene("ドロップ", 6, "break", ["F#m7", "F#m7", "Dmaj7", "Dmaj7", "E", "E"])
scene("静か", 8, "bridge", ["Dmaj7", "Dmaj7", "C#m7", "C#m7", "Bm7", "Bm7", "Esus4", "E"])
scene("B1", 8, "bridge", BB)
scene("A2", 8, "verse", AA[:8])
scene("サビ1", 16, "chorus", CH * 2)
scene("B2", 12, "bridge", BB + ["Bm7", "C#m7", "Dmaj7", "E"])
scene("フック", 8, "break", CH)
scene("ソロ2", 12, "break", ["F#m7", "Dmaj7", "A", "E", "F#m7", "Dmaj7", "A", "E", "Bm7", "C#m7", "Dmaj7", "E"])
scene("A3", 8, "verse", AA[:8])
scene("ソロ3", 8, "break", ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "C#m7", "Dmaj7", "E"])
scene("サビ2", 6, "outro", CHQ)
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

KB = [S.track(f"エレピ（和音）{i + 1}", "keys", patch="kfbGlassEp", volume=0.11, pan=(-0.22, 0.0, 0.18, -0.08)[i], reverb=0.15,
              fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(4)]
KM = S.track("エレピ（右手の句）", "keys", patch="kfbGlassEp", volume=0.2, pan=-0.12, reverb=0.16, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}])
MB = S.track("オルゴール", "keys", patch="kfbMusicBox", volume=0.06, pan=0.3, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.21, pan=0, gainDb=-5)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.065, pan=(-0.4, 0.4, -0.15, 0.15)[i], reverb=0.2, duck=0.4,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(4)]
SWL = S.track("ふくらむスーパーソウ", "pad", patch="kfbSupersawSwell", volume=0.06, pan=0, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
PLK = S.track("矩形波のプラック", "lead", patch="kfbSquarePluck", volume=0.085, pan=0.28, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
LEAD = S.track("夢のようなリード", "lead", patch="kfbDreamLead", volume=0.14, mono=True, pan=0.06, reverb=0.26, fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.6}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}])
FX = lambda name, v, pn=0.0: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=0.08, modulate=False)
FK, FSN, FCL, FH, FRM = FX("効果音（キック）", 0.13), FX("効果音（スネア）", 0.08, 0.04), FX("効果音（手びょうし）", 0.06, -0.06), FX("効果音（ハイハット）", 0.04, 0.22), FX("効果音（リム）", 0.05, -0.22)
FKW = FX("効果音（かわいい音: あわ・きらめき・きゅっ・ぽよん）", 0.045, 0.3)
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


def cutp(pat, stop):
    k = int(stop * 4); return pat[:k] + "." * (16 - k)


# 3・3・2 のヒップホップ（キックは 3・3・2、スネアは2と4、ハイハットは16分のはね）
KP = ("X..X..X.....X...", "X..X..X...X.....", "X..X..X.....X..x", "X..X......X.X...")
def hop(b, i, hat=True, clap=False, stop=None, sparse=False):
    k = KP[i % 4] if not sparse else "X.........X....."; sn = "....X.......X..." if not sparse else "........X......."
    hp = ("x.xxx.x.x.xxx.x.", "x.x.x.xxx.x.x.x.")[i % 2]
    if stop is not None: k, sn, hp = cutp(k, stop), cutp(sn, stop), cutp(hp, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, sn, "A#4")
    if clap: grid(FCL, b, sn, "B4")
    if hat: grid(FH, b, hp, "C#5")
def kawaii(b, pat, key="C4"): grid(FKW, b, pat, key)


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


BK = ("r..r..r.....r-..", "r..r..5...R.....", "r..r..r.....5-..", "r..r......r.R...")                     # ベース（キックにそろえる）
def bass(b, pat):
    ch = S.chords[b]; r = low(ch, "E1"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 7
    off = {"r": 0, "3": t3, "5": 7, "7": 10, "R": 12}; out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + off[pat[i]])}:{L * 0.25:g}"); i += L
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


KP2 = ("x..x......x.....", "..x..x....x..x..", "x.....x...x.....", "x..x..x.........")                    # エレピの刻み（間をあける）
def keys(b, k, center=64, pat=None): _ch(KB, b, pat or KP2[k % 4], center, 4, short=0.5)
def saw(b, pat="x..x..x.....x...", center=66, short=0.5): _ch(SAW, b, pat, center, 4, short=short)


def one(tr, b, pat, center=79, k=0):
    """和音の音を1つずつ、型の x の所に置く"""
    t = sorted(voice(S.chords[b], center, 4)); out = []; i = 0; c = k
    while i < 16:
        if pat[i] == "x": out.append(f"{N(t[c % 4])}:0.25"); c += 1; i += 1
        else:
            L = 1
            while i + L < 16 and pat[i + L] != "x": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    tr.bar(b, " ".join(out))


def trade(b, k):
    """楽器の交互の刻み: エレピ（表の16分）→ プラック → オルゴール の順に回す。3拍めのあとは休んで間をあける"""
    E = ("x...x.......x...", "x.......x...x...")[k % 2]; P = ("..x...x.........", "..x.......x.....")[k % 2]; M = (".x...x....x.....", "....x.x.......x.")[k % 2]
    _ch(KB, b, E, 64, 4, short=0.25); one(PLK, b, P, 76, k); one(MB, b, M, 84, k + 1)


DARE = "R:2 5:0.5 1':1.5"                                                             # 「だれ？」の動機: 短い音 → 4度上の長い音（語尾が上がる）
def dare(tr, b, up=1): tr.bar(b, KA.mel(DARE, oct=3 + up))


def theme(name, lines, tr=None, up=1, start=0):
    bars = S.sc(name)[start:]; ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) <= len(bars), (name, len(ls), len(bars))
    for b, l in zip(bars, ls):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l != "R:4": (tr or LEAD).bar(b, KA.mel(l, oct=3 + up))


# ---- 旋律（夢のようなリード。1＝A4）。付点と16分の食いこみ。長い音は和音の音 ----
C0 = ["R:2 3:0.75 5:0.75 6:0.5", "5:1.5 R:2.5", "R:2 3:0.75 5:0.75 1':0.5", "7:1.5 R:1 5:0.5 1':1", "R:2 4:0.75 6:0.75 1':0.5", "2':1.5 R:2.5", "R:2 3':0.75 2':0.75 1':0.5", "1':1.5 R:2.5"]
F1 = ["R:1 6:0.75 1':0.75 3':1.5", "R:4", "R:1 4:0.75 6:0.75 1':1.5", "R:4", "R:1 3:0.75 5:0.75 1':1.5", "R:4", "R:1 5:0.75 7:0.75 2':1.5", "5:1 R:1 5:0.5 1':1.5"]   # 休みから入って最後をのばす（最後に「だれ？」）
A1L = ["1:0.25 1:0.25 1:0.25 R:0.25 5:0.75 3:1.25 R:1", "R:4", "6:0.25 6:0.25 6:0.25 R:0.25 3':0.75 1':1.25 R:1", "R:4", "4:0.25 4:0.25 4:0.25 R:0.25 1':0.75 6:1.25 R:1", "R:2 5:0.5 1':1.5",
       "5:0.25 5:0.25 5:0.25 R:0.25 2':0.75 7:1.25 R:1", "R:4", "1:0.25 1:0.25 1:0.25 R:0.25 5:0.75 3:1.25 R:1", "R:4", "6:0.25 6:0.25 6:0.25 R:0.25 3':0.75 1':1.25 R:1", "R:2 5:0.5 1':1.5"]
CH3 = ["R:1 3':0.75 2':0.75 1':1.5", "6:2 R:2", "R:1 1':0.75 7:0.75 5:1.5",                                                    # 3小節の句
       "R:1 3':0.75 2':0.75 1':1.5", "4':2 R:2", "R:1 3':0.75 1':0.75 2':1.5", "R:4", "R:4"]
QL = ["3':0.25 3':0.25 3':0.25 R:0.25 6':3", "R:4", "1':0.25 1':0.25 1':0.25 R:0.25 5':3", "R:4", "6:0.25 6:0.25 6:0.25 R:0.25 4':3", "R:4", "5:0.25 5:0.25 5:0.25 R:0.25 4':3", "R:2 5:0.5 1':1.5"]
B1L = ["4:0.5 6:0.5 1':1 R:2", "3:0.5 5:0.5 7:1 R:2", "4:0.5 6:0.5 3':1 R:2", "5:0.5 7:0.5 2':1 R:2", "4:0.5 6:0.5 1':1 R:2", "5:0.5 7:0.5 3':1 R:2", "6:0.5 1':0.5 4':1 R:2", "R:2 5:0.5 1':1.5"]
CH1 = ["R:3 3':1", "6':1.5 5':0.5 3':1 R:1", "R:3 1':1", "5':1.5 3':0.5 1':1 R:1", "R:3 2':1", "4':1.5 3':0.5 2':1 R:1", "R:3 3':1", "1':2 R:1 5:0.5 1':0.5"]   # 1拍早く食って入る
B2L = ["R:2 4:0.75 6:0.75 1':0.5", "7:1.5 R:2.5", "R:2 6:0.75 1':0.75 3':0.5", "2':1.5 R:2.5", "R:2 4:0.75 6:0.75 2':0.5", "1':1.5 R:2.5", "R:2 5:0.75 7:0.75 2':0.5", "3':1.5 R:2.5",
       "R:2 4:0.75 6:0.75 1':0.5", "7:1.5 R:2.5", "R:2 6:0.75 1':0.75 4':0.5", "R:2 5:0.5 1':1.5"]
HOOK = ["R:0.5 3':0.5 R:0.25 3':0.25 5':0.5 R:0.5 3':0.5 2':1", "R:0.5 7:0.5 R:0.25 7:0.25 2':0.5 R:0.5 3':0.5 5':1", "R:0.5 3':0.5 R:0.25 3':0.25 5':0.5 R:0.5 6':0.5 5':1", "3':1.5 R:2.5"]
A3L = ["R:1 1':0.75 3':0.75 5':1.5", "3':2 R:2", "R:1 6:0.75 1':0.75 3':1.5", "R:1 4:0.75 6:0.75 2':1.5", "1':2 R:2", "R:1 5:0.75 7:0.75 2':1.5", "R:4", "R:2 5:0.5 1':1.5"]
CHE = ["R:2 3:0.75 5:0.75 6:0.5", "5:1.5 R:2.5", "R:2 3:0.75 5:0.75 1':0.5", "7:1.5 R:2.5", "R:2 4:0.75 6:0.75 1':0.5", "R:2 5:0.5 1':1.5"]                     # 終わり: 最後は「だれ？」（Dm6 の上で D・… 解決しない）

theme("サビ0", C0); theme("早口1", F1); theme("A1", A1L); theme("サビ半", CH3); theme("静か", QL); theme("B1", B1L); theme("A2", A1L[:8])
theme("サビ1", CH1 * 2); theme("B2", B2L); theme("フック", HOOK * 2); theme("A3", A3L); theme("サビ2", CHE)
SOLO = ["0+:0.5 R:0.25 2:0.25 3:0.5 R:0.5 0+:0.25 1+:0.25 2+:0.5 R:1", "2+:1 R:0.5 1+:0.25 0+:0.25 3:1 R:1", "3:0.25 0+:0.25 1+:0.25 2+:0.25 R:1 3+:1 R:1", "2+:1.5 1+:0.5 0+:1 R:1"]


def ct(tr, b, cell, center=72):
    v = sorted(voice(S.chords[b], center, 4)); out = []
    for x in cell.split():
        a, L = x.split(":")
        if a == "R": out.append(x); continue
        out.append(f"{N(v[int(a[0])] + 12 * (a.count('+') - a.count('-')))}:{L}")
    assert abs(sum(float(x.split(':')[1]) for x in out) - 4) < 1e-6, cell
    tr.bar(b, " ".join(out))


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n in ("サビ0", "サビ1", "フック"):                                 # 全員。4小節ごとに 刻み → 間 の緩急。8小節めは2拍半で止める
        ph = i % 4; stop = 2.5 if i % 8 == 7 else None
        hop(b, i, clap=True, stop=stop); bass(b, cutp(BK[i % 4], stop) if stop else BK[i % 4])
        if ph == 2: saw(b, "xxx.xxx.xx......", short=0.25); keys(b, i, pat="x.......x.......")       # 16分で刻む → あとは間
        else: saw(b, cutp("x..x..x.....x...", stop) if stop else "x..x..x.....x..."); keys(b, i, pat=cutp(KP2[i % 4], stop) if stop else None)
        if ph == 1: one(MB, b, "..........x.x.x.", 84, i)
        if i == 0: fxh(b, 0, "impact", 2)
        if stop: kawaii(b, "............x...", "E4")
    elif n in ("早口1", "A1", "A2", "A3"):                                # 楽器の交互の刻み。ドラムはまばら
        hop(b, i, sparse=n != "早口1"); bass(b, BK[i % 4]); trade(b, i)
        if last: fxh(b, 0, "riser", 4)
    elif n in ("ソロ1", "ソロ3"):
        hop(b, i, clap=True); bass(b, BK[i % 4]); keys(b, i); ct(KM, b, SOLO[i % 4], 74)
        if last: fxh(b, 0, "rev", 4)
    elif n == "ソロ2":                                                   # シンセ（リード）とエレピのかけ合い: 1小節ずつ交代
        hop(b, i, clap=True); bass(b, BK[i % 4]); saw(b, "x.......x.......", short=1.0)
        ct(LEAD if i % 2 == 0 else KM, b, SOLO[i % 4], 74 if i % 2 == 0 else 72)
        if i % 4 == 3: kawaii(b, "........x.x.x.x.", "F4")
        if last: fxh(b, 0, "riser", 4)
    elif n == "サビ半":                                                  # 半分の速さ
        grid(FK, b, "X.........X.....", "A4"); grid(FSN, b, "........X.......", "A#4"); bass(b, "r.........r.....")
        SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4"); keys(b, i, pat="x.........x.....")
        if last: fxh(b, 0, "riser", 4)
    elif n == "ドロップ":
        hop(b, i, clap=True); bass(b, "r.rr.rr.r.rr.R.R"); saw(b, ("xxxxxxxx........", "x..x..x...x..x..")[i % 2], short=0.25); one(PLK, b, "x.x.x.x.x.x.x.x.", 76, i)
        if i == 0: fxh(b, 0, "subdrop", 4)
        if last: fxh(b, 0, "down", 4)
    elif n == "静か":                                                    # エレピとオルゴールだけ
        keys(b, i, pat="x---------------"); one(MB, b, "x...x...x...x..." if i % 2 else "x.......x.......", 84, i)
        if last: fxh(b, 2, "rev", 2)
    elif n in ("B1", "B2"):                                              # 1小節ずつ: 刻む小節と、間をあける小節
        if i % 2 == 0: hop(b, i); bass(b, BK[i % 4]); trade(b, i)
        else: hop(b, i, hat=False, sparse=True); bass(b, "r..............."); keys(b, i, pat="x...............")
        if last: fxh(b, 0, "riser", 4)
    elif n == "サビ2":                                                   # 終わり: 最後の Dm6 で全部止まり、オルゴールが「だれ？」をもう一度
        if not last: hop(b, i, clap=True); bass(b, BK[i % 4]); saw(b); keys(b, i)
        else:
            grid(FK, b, "X...............", "A4"); _ch(KB, b, "x---------------", 64, 4); SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:2 R:2")
            dare(MB, b, up=2); kawaii(b, "x...............", "D4")

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: ヒップホップ × Kawaii future bass のインスト（160・イ長調）。放課後、ふいに聞かれた「好きな人だれ？」。はぐらかしたり、答えかけたり、最後は問いかけのまま終わる。"
          "エレピ・プラック・オルゴールの交互の刻み、間をあける緩急。形は、くじ（form_dice.py・種 7316）で決めた。全員のフックで始まり、解決しない和音で止まる。自作")
V = Voice(S, vol=0.0, delay=0.0, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead" and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "tight"; js["human"] = 0.35; js["swing16"] = 0.6
save(path, js)
