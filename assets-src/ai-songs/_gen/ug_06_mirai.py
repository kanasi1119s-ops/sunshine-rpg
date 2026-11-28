# UG 06（作り直し）「未来はガラスの向こう」（仮）The Future Behind the Glass — インスト。テクノポップ × Kawaii future bass。4分の4・170・ハ長調。125小節・約2分56秒。
#
# 2026-11-28 人間「kawaiifutureベースで間を主体にしたテクノポップ。緩急が大事。疾走感もありゆっくりな感じもあり。キーボード、シンセの重ねがけ、FX、
#   コンセプトは挑戦する先に未来が待っている。テンポ170」「手数多めの部分や少なめの部分あり」「BGM系は3分以内」
#   → はじめの版（ug_06_mirai_old.py）に「このピコ系の音別のにしよう」「これはダメかな。一から作り直しましょう」。形・リズム・音を全部変えて作り直した。
#   楽器: キーボード（ピアノ・エレピ kfbGlassEp）／シンセ（低い正弦波のベース・うなるベース・スーパーソウ・ふくらむスーパーソウ・声のようなリード）／効果音（kawaiiFx）。
#   ピコ系（矩形波のリードとプラック・オルゴール・グロッケン・レーザー）は使わない。kfbBrightBells・kfbSawStab・モノのスーパーソウのリードも使わない（点が下がる）。
#   シンセの重ねがけ: 旋律＝声のようなリード＋ピアノ（同じ高さ）。和音＝スーパーソウ＋ふくらむスーパーソウ＋エレピ。
# 形: くじ（tools/vt3/form_dice.py --skeleton 9025 176 170 ... 種 9026）。始まり＝効果音ひとつ → すぐピアノ／終わり＝始まりと同じ音にもどって終わる。
#   リズム: くじはブレイクビートだったが、はじめの版と同じになるので、疾走＝8ビートのドライブ、ゆっくり＝あと乗りのハーフにした。
# 物語: 小さな「カチッ」（スイッチを入れる音）から挑戦が始まる。迷って、立ち止まって、走って、最後にもう一度「カチッ」。それは未来の扉が開く音。
# この曲だけのもの: 最初と最後の「カチッ」（指パッチン C5 ＋ きらめき）と、そのあとピアノが鳴らす3つの音の動機（ド・ソ・ミ↑。最後は1オクターブ上で答える）。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("42", "mirai", "未来はガラスの向こう（仮）", "The Future Behind the Glass", 170, 4, "C", "major", "インスト（テクノポップ × Kawaii future bass）")
S.flags = S.flags + " --space room --space-wet 0.1"
KC = Key("C", "major")
CH = ["Fmaj7", "G/F", "Em7", "Am7", "Dm7", "Bb", "Csus2", "C"]                          # サビ: IV → V/IV → iii → vi ／ ii → ♭VII → I
CHB = ["Am7", "Am7", "Fmaj7", "Fmaj7", "C/E", "C/E", "Dm7", "G", "Am7", "Am7", "Fmaj7", "Fmaj7", "Bb", "Bb", "Gsus4", "G"]
SL = ["Fmaj7", "Fmaj7", "Em7", "Em7", "Dm7", "Dm7", "Gsus4", "G"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("ソロ", 10, "intro", ["C", "C", "Am7", "Am7", "Fmaj7", "Fmaj7", "Dm7", "Dm7", "Gsus4", "G"])
scene("フック", 6, "break", ["Fmaj7", "G", "Em7", "Am7", "Dm7", "G"])
scene("サビ別", 16, "chorus", CHB)
scene("ドロップ", 8, "break", ["Am7", "Am7", "Fmaj7", "Fmaj7", "C", "C", "G", "G"])
scene("早口", 8, "verse", ["Am7", "Am7", "Fmaj7", "Fmaj7", "C", "C", "Gsus4", "G"])
scene("サビ半", 8, "chorus", SL)
scene("新1", 12, "verse", ["C", "C/E", "Fmaj7", "Fmaj7", "Am7", "Em7", "Fmaj7", "G", "C", "C/E", "Dm7", "G"])
scene("立ち上げ", 8, "pre", ["Dm7", "Dm7", "Em7", "Em7", "Fmaj7", "Fmaj7", "Gsus4", "G"])
scene("サビ", 8, "chorus", CH)
scene("新2", 16, "verse", ["Am7", "Fmaj7", "C", "G", "Am7", "Fmaj7", "C", "G", "Dm7", "Em7", "Fmaj7", "Fmaj7", "Bb", "Bb", "Gsus4", "G"])
scene("B", 9, "bridge", ["Fmaj7", "Fmaj7", "Em7", "Em7", "Dm7", "Dm7", "Bb", "Gsus4", "G"])
scene("新3", 16, "outro", CH + ["Fmaj7", "G/F", "Em7", "Am7", "Dm7", "Bb", "Csus2", "C"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

PN = [S.track(f"ピアノ（和音）{i + 1}", "piano", volume=0.14, pan=(-0.2, 0.0, 0.16, -0.08)[i], reverb=0.14) for i in range(4)]
PM = S.track("ピアノ（右手の旋律）", "piano", volume=0.3, pan=-0.12, reverb=0.16)
EP = [S.track(f"エレピ（和音）{i + 1}", "keys", patch="kfbGlassEp", volume=0.08, pan=(-0.3, 0.3, 0.0)[i], reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(3)]
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.21, pan=0, gainDb=-5)
GRW = S.track("シンセのベース（うなる）", "bass", patch="kfbGrowlBass", volume=0.08, pan=0, gainDb=-8, fx=[{"type": "filter", "kind": "lowpass", "freq": 2800, "q": 0.6}])
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.06, pan=(-0.4, 0.4, -0.15, 0.15)[i], reverb=0.2, duck=0.4,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(4)]
SWL = S.track("ふくらむスーパーソウ", "pad", patch="kfbSupersawSwell", volume=0.055, pan=0, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}])
LEAD = S.track("声のようなリード", "lead", patch="kfbFormantLead", volume=0.13, mono=True, pan=0.06, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 4200, "q": 0.6}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}])
FX = lambda name, v, pn=0.0: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=0.08, modulate=False)
FK, FSN, FCL, FH, FOH, FSP = FX("効果音（キック）", 0.13), FX("効果音（スネア）", 0.07, 0.04), FX("効果音（手びょうし）", 0.055, -0.06), FX("効果音（ハイハット）", 0.03, 0.22), FX("効果音（開いたハイハット）", 0.03, -0.22), FX("効果音（指パッチン）", 0.07, 0.1)
FXT = S.track("効果音（上がる音・下がる音・逆回しのシンバル・当たる音・低く落ちる音・きらめき）", "guitar", patch="kawaiiFx", volume=0.065, pan=0.1, reverb=0.3, modulate=False)
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


# 疾走: 8ビートのドライブ（キックは表とすこし食う、スネア2と4、ハイハット8分。手数多めは16分）
DK = ("X.......X.X.....", "X.....X...X.....", "X.......X.X...X.", "X.....X.X.......")
def drive(b, i, many=False, stop=None, clap=False):
    k = DK[i % 4]; s = "....X.......X..."; h = "x.x.x.x.x.x.x.x." if not many else "xxx.xxx.xxx.xxx."
    if stop is not None: k, s, h = cutp(k, stop), cutp(s, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FH, b, h, "C#5")
    if clap: grid(FCL, b, s, "B4")
    if i % 4 == 3 and stop is None: grid(FOH, b, "..............x.", "D5")
# ゆっくり: あと乗りのハーフ
def half(b, i, hat=True):
    grid(FK, b, ("X.........X.....", "X......X........")[i % 2], "A4"); grid(FSN, b, "........X.......", "A#4")
    if hat: grid(FH, b, "x...x...x...x...", "C#5")
def click(b, at=0):                                                    # 「カチッ」: 指パッチン＋きらめき
    grid(FSP, b, "." * (at * 4) + "X" + "." * (15 - at * 4), "C5"); fxh(b, at, "spark", 1)


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


BD = ("r.......r.r.....", "r.....r...r.....", "r.......r.r...R.", "r.....r.r.......")                  # キックにそろえる
BM = ("r.rRr.rRr.rRr.rR", "r.rRr.r5r.rRr.r5")                                                    # 手数多め
def bass(b, pat, tr=None):
    ch = S.chords[b]; r = low(ch, "E1"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 7
    off = {"r": 0, "3": t3, "5": 7, "7": 10, "R": 12}; out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + off[pat[i]])}:{L * 0.25:g}"); i += L
    (tr or SUB).bar(b, " ".join(out))


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


def keys(b, pat="x..x......x.....", center=62, short=0.5): _ch(PN, b, pat, center, 4, short=short)
def ep(b, pat="..x...x...x...x.", center=67): _ch(EP, b, pat, center, 3, short=0.5)
def saw(b, pat="x..x..x...x..x..", center=66, short=0.5): _ch(SAW, b, pat, center, 4, short=short)
def swell(b): SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4")


def theme(name, lines, lead=True, piano=True, up=1, start=0):
    """旋律の重ねがけ: 声のようなリード＋ピアノ（同じ高さ）"""
    bars = S.sc(name)[start:]; ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) <= len(bars), (name, len(ls), len(bars))
    for b, l in zip(bars, ls):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l == "R:4": continue
        if lead: LEAD.bar(b, KC.mel(l, oct=3 + up))
        if piano: PM.bar(b, KC.mel(l, oct=3 + up))


# ---- 旋律（1＝C4）。付点8分（0.75）で前へ、休符で間をあける ----
MOTIF = "1:0.5 5:0.5 3':1 R:2"                                                         # 「カチッ」のあとの3つの音（ド・ソ・ミ↑）
SOLO = [MOTIF, "R:4", "R:1 6:0.5 1':0.5 3':1 R:1", "R:4", "R:1 4:0.75 6:0.75 1':0.5 R:1", "R:4", "R:1 2':0.75 1':0.75 6:0.5 R:1", "R:4", "R:1 5:0.75 7:0.75 2':1.5", "R:4"]
HOOK = ["3':0.75 2':0.75 1':0.5 R:0.5 5:0.5 1':1", "2':0.75 1':0.75 7:0.5 R:2", "3':0.75 2':0.75 1':0.5 R:0.5 6:0.5 1':1", "1':0.75 7:0.75 6:0.5 R:2", "2':0.75 1':0.75 6:0.5 R:0.5 4:0.5 6:1", "7:2 R:2"]
SBE = ["3:0.5 R:0.25 1':0.25 R:0.5 3':1.5 R:1", "2':0.75 1':0.75 7:0.5 R:2", "1:0.5 R:0.25 6:0.25 R:0.5 1':1.5 R:1", "7:0.75 6:0.75 5:0.5 R:2",   # 低い音から6度以上跳ぶ
       "1:0.5 R:0.25 5:0.25 R:0.5 3':1.5 R:1", "2':0.75 3':0.75 2':0.5 R:2", "2:0.5 R:0.25 4:0.25 R:0.5 6:1.5 R:1", "7:2 R:2",
       "3:0.5 R:0.25 1':0.25 R:0.5 5':1.5 R:1", "3':0.75 2':0.75 1':0.5 R:2", "1:0.5 R:0.25 6:0.25 R:0.5 3':1.5 R:1", "2':0.75 1':0.75 6:0.5 R:2",
       "b7:0.5 R:0.25 2':0.25 R:0.5 4':1.5 R:1", "2':0.75 1':0.75 b7:0.5 R:2", "5:0.5 R:0.25 2':0.25 R:0.5 4':1.5 R:1", "2':3 R:1"]
FAST = ["R:3 3:0.5 5:0.5", "1':0.75 R:3.25", "R:3 1:0.5 3:0.5", "6:0.75 R:3.25", "R:3 5:0.5 1':0.5", "3':0.75 R:3.25", "R:3 2:0.5 4:0.5", "5:2 R:2"]   # 1拍早く食う。短い答えだけ（手数少なめ）
HALF = ["3':0.5 1':0.5 R:3", "R:4", "2':0.5 7:0.5 R:3", "R:4", "1':0.5 6:0.5 R:3", "R:4", "2':0.5 5:0.5 R:1 4':0.5 2':0.5 R:1", "R:4"]   # 1小節の短い句（ゆっくり・少なめ）
NEW1 = ["R:3 5:1", "1':2 R:2", "R:3 6:1", "1':1.5 7:0.5 6:2", "R:3 3':1", "2':2 R:2", "R:3 1':1", "2':1.5 1':0.5 7:2",
        "R:3 5:0.5 6:0.5", "1':1 3':1 5':1 R:1", "R:3 4':0.5 3':0.5", "2':3 R:1"]
CHO = ["3:0.5 R:0.25 1':0.25 R:0.5 3':1 5':1.5", "4':1.5 3':0.5 2':2", "3:0.5 R:0.25 7:0.25 R:0.5 2':1 3':1.5", "1':4",
       "2:0.5 R:0.25 6:0.25 R:0.5 2':1 4':1.5", "4':1.5 3':0.5 2':2", "1:0.5 R:0.25 5:0.25 R:0.5 2':1 3':1.5", "1':4"]
NEW2 = ["R:2 3:0.75 5:0.75 1':0.5", "R:4", "R:2 5:0.75 1':0.75 3':0.5", "2':2 R:2", "R:2 3:0.75 5:0.75 1':0.5", "R:4", "R:2 5:0.75 1':0.75 5':0.5", "4':2 R:2",
        "R:2 2':0.75 4':0.75 6':0.5", "5':2 R:2", "R:2 1':0.75 3':0.75 5':0.5", "3':2 R:2", "R:2 b7:0.75 2':0.75 4':0.5", "2':2 R:2", "R:2 5:0.75 7:0.75 2':0.5", "R:4"]
BL = ["3':0.5 R:3.5", "R:4", "2':0.5 R:3.5", "R:4", "1':0.5 R:3.5", "R:4", "2':0.5 R:1.5 4':0.5 R:1.5", "R:4", MOTIF]               # とても少ない（最後に動機）
NEW3 = ["3':1.5 2':0.5 1':2", "R:1 5:0.5 1':0.5 3':2", "2':1.5 1':0.5 7:2", "R:1 3:0.5 6:0.5 1':2",                                     # 2小節の句
        "2':1.5 1':0.5 6:2", "R:1 4:0.5 6:0.5 2':2", "3':1.5 2':0.5 1':2", "R:4",
        "5':1.5 4':0.5 3':2", "R:1 3':0.5 5':0.5 1'':2", "7':1.5 6':0.5 5':2", "R:1 3':0.5 6':0.5 1'':2",
        "R:4", "R:4", "R:4", "R:4"]

theme("ソロ", SOLO, lead=False); theme("フック", HOOK); theme("サビ別", SBE); theme("早口", FAST, lead=False); theme("サビ半", HALF)
theme("新1", NEW1); theme("サビ", CHO); theme("新2", NEW2); theme("B", BL, lead=False); theme("新3", NEW3)

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "ソロ":                                                      # 効果音ひとつ（カチッ）→ すぐピアノ。間が主役。後半からエレピとふくらむ音
        if i == 0: click(b)
        keys(b, ("x...............", "........x.......")[i % 2], 55, short=1.0)
        if i >= 4: ep(b, "........x.......")
        if i >= 6: swell(b); grid(FH, b, "x...x...x...x...", "C#5")
        if last: fxh(b, 0, "riser", 4)
    elif n in ("フック", "サビ別", "サビ"):                                # 疾走・手数多め。4小節ごとの最後は2拍半で止める（緩急）
        stop = 2.5 if i % 4 == 3 else None; many = n != "フック"
        drive(b, i, many=many and i % 4 in (1, 2), stop=stop, clap=True)
        bass(b, cutp(BD[i % 4], stop) if stop else BD[i % 4]); saw(b, cutp("x..x..x...x..x..", stop) if stop else "x..x..x...x..x..")
        keys(b, cutp("x..x......x.....", stop) if stop else "x..x......x....."); ep(b, cutp("..x...x...x...x.", stop) if stop else "..x...x...x...x.")
        if i == 0: fxh(b, 0, "impact", 2)
        if last and n == "サビ別": fxh(b, 0, "down", 4)
    elif n == "ドロップ":                                                # 手数とても多い: 16分の刻み（スーパーソウとピアノを交互）＋うなるベース
        drive(b, i, many=True, clap=True); bass(b, BM[i % 2]); bass(b, BM[i % 2], tr=GRW)
        saw(b, "x.x.x.x.x.x.x.x.", short=0.25); keys(b, ".x.x.x.x.x.x.x.x", 64, short=0.25)
        if i == 0: fxh(b, 0, "subdrop", 4)
        if last: fxh(b, 0, "down", 4)
    elif n == "早口":                                                    # 疾走だが手数少なめ: ドラムとベースと短い答えだけ
        drive(b, i); bass(b, BD[i % 4])
        if i % 2 == 1: ep(b, "x...............")
        if last: fxh(b, 0, "rev", 4)
    elif n == "サビ半":                                                  # ゆっくり（ハーフ）・少なめ
        half(b, i); bass(b, "r.........r....."); swell(b); keys(b, "x.........x.....", 60)
        if last: fxh(b, 0, "riser", 4)
    elif n == "新1":                                                     # 前半ゆっくり・少なめ → 後半疾走
        if i < 6: half(b, i, hat=i >= 2); bass(b, "r.........r....."); keys(b, "x.........x.....", 60); ep(b, "....x.......x...")
        else: drive(b, i, clap=True); bass(b, BD[i % 4]); keys(b); ep(b); saw(b, "x.......x.......")
        if i == 6: fxh(b, 0, "impact", 2)
        if last: fxh(b, 0, "riser", 4)
    elif n == "立ち上げ":                                                # だんだん速く・増えていく
        if i < 4: half(b, i)
        else: drive(b, i, many=i >= 6)
        bass(b, "r.........r....." if i < 4 else BD[i % 4]); swell(b); keys(b, ("x.........x.....", "x...x...x...x...", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx")[i // 2], 60, short=0.25)
        if i == 4: fxh(b, 0, "riser", 4)
    elif n == "新2":                                                     # 疾走・ふつう。小節のまん中から入る旋律のすき間にエレピ
        drive(b, i, clap=i >= 8); bass(b, BD[i % 4]); keys(b, "x.........x....."); ep(b, "..x...x.........")
        if i >= 8: saw(b, "x.......x.......")
        if last: fxh(b, 0, "rev", 4)
    elif n == "B":                                                       # とても少ない
        keys(b, "x---------------" if i % 2 == 0 else "................", 57); swell(b) if i % 4 == 0 else None
        if last: click(b, 0); fxh(b, 0, "riser", 4)
    elif n == "新3":                                                     # 疾走・多い → 最後の4小節で止まり、始まりと同じ「カチッ」とピアノの動機（1オクターブ上）で終わる
        if i < 12:
            drive(b, i, many=i >= 4, clap=True); bass(b, BD[i % 4] if i < 4 else BM[i % 2]); saw(b); keys(b); ep(b)
            if i in (0, 8): fxh(b, 0, "impact", 2)
        elif i == 12: grid(FK, b, "X...............", "A4"); _ch(PN, b, "x---------------", 60, 4); swell(b)
        elif i == 14: click(b); PM.bar(b, KC.mel(MOTIF, oct=5))
        elif i == 15: _ch(PN, b, "x---------------", 60, 4)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: テクノポップ × Kawaii future bass のインスト（170・ハ長調・約2分56秒）。小さな「カチッ」から挑戦が始まり、迷って、止まって、走って、最後にもう一度「カチッ」と未来の扉が開く。"
          "疾走（8ビートのドライブ）とゆっくり（ハーフ）、手数多めと少なめが交互に来る。旋律は声のようなリードとピアノの重ねがけ。形は、くじ（form_dice.py・種 9026）で決めた。自作")
V = Voice(S, vol=0.0, delay=0.0, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead" and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "pushed"; js["human"] = 0.3
save(path, js)
