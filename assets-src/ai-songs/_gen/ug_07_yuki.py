# UG 07「ふたりぶんの足あと」（仮）Two Sets of Footprints — インスト。ヒップホップ × Kawaii future bass。4分の4・110・ト長調。80小節・約2分55秒。
#
# 2026-11-28 人間「次始まりが緩急あるサビからスタート。Kawaii_future_bassのヒップホップ。キーボード、シンセ、DJ、FX。テンポ110。コンセプト、雪とクリスマスとあなたと私」
#   楽器: キーボード（エレピ kfbGlassEp・ピアノ・オルゴール kfbMusicBox）／シンセ（低い正弦波のベース・スーパーソウ・ふくらむスーパーソウ・夢のようなリード）／
#         DJ（スクラッチ2種・テープストップ・巻きもどし・レコードのパチパチ。kawaiiFx に足した E6〜G6）／効果音（そりの鈴 G#6・雪のきらめき A6 ほか）。
#   kfbSawStab・kfbBrightBells・モノのスーパーソウのリードは使わない。BGM なので3分以内。歌の指定がないのでインスト。
# 形: くじ（tools/vt3/form_dice.py --skeleton 1225 174 110 --min-chorus 3 ... 種 1237）。始まり＝人間の指定で「緩急のあるサビ」から（くじの「手びょうしと声の切れはし」は使わない）。
#   終わり＝くじは「始まりと同じ音にもどる」だったが UG06 と同じになるので、DJ の「テープストップ」でゆっくり止まって終わる（物語: ふたりの夜が終わる）。
#   リズム＝ファンクの16分（主・はね 0.12・あと乗り）／はねる16分（静かな場面）。
# 物語: 雪の降るクリスマスの夜。「あなた」（エレピ）と「私」（夢のようなリード）が、かけ合いながら並んで歩く。最後のサビでだけ、ふたりの旋律が3度はなれて重なる。
# この曲だけのもの: 1小節ずつ交代するふたりの旋律と、最後のサビでの3度の重なり／冬の和音 C → Cm6（IV → iv）。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("43", "yuki", "ふたりぶんの足あと（仮）", "Two Sets of Footprints", 110, 4, "G", "major", "インスト（ヒップホップ × Kawaii future bass）")
S.flags = S.flags + " --space room --space-wet 0.14"
KG = Key("G", "major")
CH = ["Cmaj7", "Cm6", "Bm7", "Em7", "Am7", "D7sus4", "Gmaj7", "G7"]                       # サビ: IV → iv6（冬の和音）→ iii → vi ／ ii → V7sus4 → I
CHE = ["Em7", "Cmaj7", "Am7", "D7sus4", "Em7", "Cm6", "Gmaj7", "D"]                       # サビ別（いきなりサビ）
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("サビ別", 8, "chorus", CHE)
scene("立ち上げ1", 8, "pre", ["Am7", "Am7", "Bm7", "Bm7", "Cmaj7", "Cmaj7", "D7sus4", "D"])
scene("フック1", 8, "break", CH)
scene("B1", 4, "bridge", ["Cmaj7", "Bm7", "Am7", "D7sus4"])
scene("サビ", 8, "chorus", CH)
scene("立ち上げ2", 8, "pre", ["Em7", "Em7", "Cmaj7", "Cmaj7", "Am7", "Am7", "D7sus4", "D"])
scene("新", 12, "verse", ["Gmaj7", "Bm7", "Cmaj7", "Cm6", "Gmaj7", "Em7", "Am7", "D7sus4", "Bm7", "Em7", "Cmaj7", "D"])
scene("フック2", 8, "break", CH)
scene("A", 8, "verse", ["Gmaj7", "Gmaj7", "Em7", "Em7", "Cmaj7", "Cm6", "Am7", "D7sus4"])
scene("B2", 8, "outro", ["Cmaj7", "Cm6", "Bm7", "Em7", "Am7", "D7sus4", "Gmaj7", "Gmaj7"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

EPC = [S.track(f"エレピ（和音）{i + 1}", "keys", patch="kfbGlassEp", volume=0.1, pan=(-0.22, 0.0, 0.18, -0.08)[i], reverb=0.18,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(4)]
YOU = S.track("エレピ（あなたの旋律）", "keys", patch="kfbGlassEp", volume=0.22, pan=-0.15, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}])
ME = S.track("電子のサックス（私の旋律）", "lead", patch="kfbFutureSax",  # v7（人間「まだヒョイある」）: kfbDreamLead は音の頭が下から持ち上がる（測って確かめた）ので替えた
           volume=0.13, mono=True, pan=0.15, reverb=0.28, fx=[{"type": "filter", "kind": "lowpass", "freq": 4500, "q": 0.6}, {"type": "delay", "beats": 0.75, "mix": 0.14, "feedback": 0.28}])
PNO = S.track("ピアノ（低い和音）", "piano", volume=0.12, pan=-0.05, reverb=0.16)
MB = S.track("オルゴール（雪）", "keys", patch="kfbMusicBox", volume=0.05, pan=0.3, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}])
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.21, pan=0, gainDb=-5)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.055, pan=(-0.4, 0.4, -0.15, 0.15)[i], reverb=0.22, duck=0.4,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.6}]) for i in range(4)]
SWL = S.track("ふくらむスーパーソウ", "pad", patch="kfbSupersawSwell", volume=0.055, pan=0, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}])
FX = lambda name, v, pn=0.0, rv=0.08: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=rv, modulate=False)
FK, FSN, FCL, FH, FOH = FX("効果音（キック）", 0.13), FX("効果音（スネア）", 0.08, 0.04), FX("効果音（手びょうし）", 0.055, -0.06), FX("効果音（ハイハット）", 0.035, 0.22), FX("効果音（開いたハイハット）", 0.03, -0.22)
DJ = FX("DJ（スクラッチ・テープストップ・巻きもどし）", 0.06, 0.0, 0.05)
BELL = FX("そりの鈴", 0.04, 0.3, 0.2); SNOW = FX("雪のきらめき", 0.05, -0.25, 0.4); VIN = FX("レコードのパチパチ", 0.04, 0.0, 0.0)
V = Voice(S, vol=0.0, delay=0.0,  # v8（人間「歌ありにある、最初からある。ヒョイ」）: 歌をなぞる正弦波のシンセ（しゃくりで持ち上がる）を鳴らさない
           bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
FXT = S.track("効果音（上がる音・下がる音・逆回しのシンバル・当たる音）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.3, modulate=False)
N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "down": "G4", "rev": "G#4", "impact": "G5", "subdrop": "G#5", "spark": "D4"}
def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))
DJK = {"baby": "E6", "chirp": "F6", "stop": "F#6", "rewind": "G6"}


def grid(tr, b, pat, key):
    out = []; i = 0; pat = pat.replace(" ", ""); assert len(pat) == 16, pat
    while i < 16:
        if pat[i] in "Xx": out.append(f"{key}:0.25" + ("!" if pat[i] == "X" else "")); i += 1
        else:
            L = 1
            while i + L < 16 and pat[i + L] not in "Xx": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    tr.bar(b, " ".join(out))


def dj(b, at, kind, L=1.0):
    """DJ の音を at 拍めから（L 拍）"""
    if kind in ("baby", "chirp", "rewind"):  # v4: スクラッチ2種をなくす／v6（人間「まだヒョイあるぞ、わりと序盤から」）: 上がっていく巻きもどしもなくす
        return
    out = ([f"R:{at:g}"] if at else []) + [f"{DJK[kind]}:{L:g}"] + ([f"R:{4 - at - L:g}"] if 4 - at - L > 1e-6 else [])
    DJ.bar(b, " ".join(out))


def cutp(pat, stop):
    k = int(stop * 4); return pat[:k] + "." * (16 - k)


# ファンクの16分（はね・あと乗り）。キックは1と「3のうら」、スネアは2と4
KF = ("X.....X...X.....", "X..X......X.....", "X.....X...X..X..", "X.X.......X.....")
def funk(b, i, stop=None, clap=False, bell=False):
    k = KF[i % 4]; s = "....X.......X..."; h = ("x.xxx.x.x.xxx.x.", "x.x.x.xxx.x.x.xx")[i % 2]
    if stop is not None: k, s, h = cutp(k, stop), cutp(s, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FH, b, h, "C#5")
    if clap: grid(FCL, b, s, "B4")
    if bell: grid(BELL, b, cutp("....x.......x...", stop) if stop else "....x.......x...", "G#6")
    if i % 4 == 3 and stop is None: grid(FOH, b, "..............x.", "D5")
def bounce(b, i):                                                        # 静か: はねる16分（キックとリムとハイハットだけ）
    grid(FK, b, "X.........X.....", "A4"); grid(FSN, b, "........X.......", "A#4"); grid(FH, b, "..x...x...x...x.", "C#5")


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


BK = ("r--...r.r--.....", "r--.....5-.r..R.", "r--...r.r--...7.", "r--..R..5-.r....")   # はじめの型は KFB03 と 56% 同じだったので書きかえた                  # キックにそろえる
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


def ep(b, pat="x..x......x.....", center=64, short=0.75): _ch(EPC, b, pat, center, 4, short=short)
def saw(b, pat="x..x..x...x..x..", center=66, short=0.5): _ch(SAW, b, pat, center, 4, short=short)
def swell(b): SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4")
def low_pn(b): PNO.bar(b, f"{N(low(S.chords[b], 'E2') + 12)}:2 R:2")
def snow(b): SNOW.bar(b, "A6:4")  # v5（人間「きらめきは戻そうか」）: v3で消した雪のきらめきを戻す（ヒョイヒョイはスクラッチだった）
def mbox(b, pat="x...x...x...x..."):
    t = sorted(voice(S.chords[b], 86, 4)); out = []; i = 0; c = b
    while i < 16:
        if pat[i] == "x": out.append(f"{N(t[c % 4])}:0.25"); c += 1; i += 1
        else:
            L = 1
            while i + L < 16 and pat[i + L] != "x": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    MB.bar(b, " ".join(out))


def duet(name, lines, both=False, start=0):
    """ふたりの旋律: 偶数の小節は「あなた」（エレピ）、奇数の小節は「私」（リード）。both なら同じ小節を、私は3度上で重ねる（最後のサビだけ）"""
    bars = S.sc(name)[start:]; ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) <= len(bars), (name, len(ls), len(bars))
    for k, (b, l) in enumerate(zip(bars, ls)):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l == "R:4": continue
        if both:
            YOU.bar(b, KG.mel(l, oct=4)); ME.bar(b, KG.mel(" ".join(third(x) for x in l.split()), oct=4))
        else:
            (YOU if k % 2 == 0 else ME).bar(b, KG.mel(l, oct=4))


def third(tok):
    """音階で3度上（5 → 7・6 → 1' など）。休みはそのまま"""
    a, L = tok.split(":")
    if a == "R": return tok
    m = _re.match(r"([#b]?)(\d)('*)", a); acc, d, q = m[1], int(m[2]), len(m[3])
    d2 = d + 2; q2 = q + (1 if d2 > 7 else 0); d2 = d2 - 7 if d2 > 7 else d2
    return f"{d2}{chr(39) * q2}:{L}"


# ---- 旋律（1＝G4）。高い音から下りてくる／4小節のばす／3小節の句／休みから入る ----
SBE = ["5':0.75 3':0.75 2':0.5 1':0.75 6:1.25", "R:1 5:0.75 6:0.75 7:1.5", "1'':0.75 6':0.75 5':0.5 3':0.75 2':1.25", "R:4",
       "5':0.75 4':0.75 2':0.5 7:0.75 6:1.25", "R:1 3:0.75 5:0.75 6:1.5", "4':0.75 3':0.75 2':0.5 1':2", "R:4"]
HOOK = ["R:0.5 3':0.5 5':0.5 R:0.5 6':0.75 5':0.75 3':0.5", "2':2 R:2", "R:0.5 1':0.5 3':0.5 R:0.5 5':0.75 3':0.75 2':0.5", "6:2 R:2",
        "R:0.5 6:0.5 1':0.5 R:0.5 2':0.75 1':0.75 6:0.5", "5:2 R:2", "R:0.5 7:0.5 2':0.5 R:0.5 4':0.75 3':0.75 2':0.5", "1':2 R:2"]
B1L = ["3':0.5 5':0.5 7':1 R:2", "2':0.5 4':0.5 6':1 R:2", "1':0.5 3':0.5 5':1 R:2", "2':0.5 5':0.5 4':1 R:2"]
CHO = ["R:1 3':1 5':2", "b6':4", "R:1 3':1 2':2", "5:4", "R:1 1':1 3':2", "4':4", "R:1 3':1 2':2", "1':2 R:2"]        # 4小節のばす長い句（Cm6 の上で ♭6＝E♭）
NEW = ["R:1 5:0.5 7:0.5 2':2", "1':1 7:1 R:2", "R:1 3:0.5 5:0.5 1':2",
       "R:1 5:0.5 7:0.5 3':2", "2':1 1':1 R:2", "R:1 6:0.5 1':0.5 3':2",
       "R:1 2':0.5 3':0.5 5':2", "4':1 3':1 R:2", "R:1 1':0.5 2':0.5 4':2",
       "R:1 3':0.5 2':0.5 1':2", "7:1 6:1 R:2", "R:1 4:0.5 6:0.5 1':2"]
AL = ["R:2 3':1 5':1", "7':4", "R:2 1':1 3':1", "5':4", "R:2 3':1 5':1", "b6':4", "R:2 1':1 3':1", "2':4"]
B2L = ["R:1 3':1 5':2", "b6':4", "R:1 3':1 2':2", "5:4", "R:1 1':1 3':2", "4':4", "R:1 3':1 2':2", "1':4"]

# ---- 歌（2026-11-28 人間「この曲テトに歌わせて」）。VB_VOCAL=1 のときだけ。1＝G3（テトが歌いやすい G3〜D5）。歌の旋律をなぞる楽器は鳴らさない ----
#   歌詞: 雪の夜、ふたりで歩く。曲名の言葉はそのまま使わない。言葉は少し比喩で（息がほどける・指切り・リボンをほどく など）
VS = {
 "サビ別": (["x-x-x-x-x-------", "..x-x-x-x-x-x---", "x-x-x-x-x-x-----", "x-x-x-x-----....", "x-x-x-x-x-x-----", "x-x-x-x-x-------", "..x-x-x-x-x-x---", "x-x-x-x-----...."],
          ["3' 2' 1' 7 6", "1' 7 6 5 6 3", "6 1' 2' 1' 6 5", "5 6 5 4", "3' 2' 1' 7 6 5", "4 b6 1' 2' 1'", "3 5 7 1' 7 5", "5 6 7 5"],
          ["ゆきがふる", "まちのあかり", "てぶくろごし", "ぬくもり", "しろいいきが", "ほどけてく", "きみのとなり", "うたうよ"]),
 "B1": (["x-x-x-x-x-x-....", "x-x-x-x-x-......", "x-x-x-x-x-......", "x-x-x-x-x-......"],
        ["3 5 1' 5 4 3", "2 3 5 3 2", "3 2 3 5 3", "5 6 1' 6 5"],
        ["ねえきこえる", "すずのおと", "ゆきのおと", "きみのこえ"]),
 "サビ": (["..x-x-x-x-x-x-x-", "x---------------", "..x-x-x-x-x-x---", "x-------x-------", "..x-x-x-x-x-x---", "x-------x-------", "..x-x-x-x-x-----", "x---------------"],
         ["3 3 5 6 5 3 5", "b6", "5 5 3 2 3 5", "5 3", "1' 1' 7 6 7 1'", "2' 1'", "5 3 2 3 5", "1'"],
         ["あしあとならべ", "て", "しろいみちを", "ゆく", "そらがひかる", "まで", "いつまでも", "ね"]),
 "新": (["x-x-x-x-x-x-....", "x-x-x-x-x-......", "x-x-x-----......", "x-x-x-x-x-x-....", "x-x-x-x-x-x-....", "x-x-x-----......",
        "x-x-x-x-x-x-....", "x-x-x-x-x-x-....", "x-x-x-----......", "x-x-x-x-x-x-....", "x-x-x-x-x-x-....", "x-x-x-----......"],
       ["3 2 3 5 3 2", "3 5 6 5 3", "5 3 3", "4 b6 1' b6 4 5", "3 5 7 5 3 2", "5 3 3", "6 1' 2' 1' 6 5", "5 6 1' 6 5 4", "5 3 2", "3' 2' 1' 7 6 5", "3 5 6 5 3 5", "2 3 5"],
       ["まどのそとで", "ろうそくが", "ゆれた", "ちいさなはこ", "あけるまえに", "わらう", "あかいりぼん", "きみのゆびが", "ほどく", "ゆきのおとが", "ふたりだけの", "よるに"]),
 "A": (["........x-x-x-x-", "x---x-----------", "......x-x-x-x-x-", "x---------------", "......x-x-x-x-x-", "x-------x-------", "......x-x-x-x-x-", "x---------------"],
       ["3 5 6 5", "3 2", "3 5 6 5 3", "6", "5 3 5 6 5", "b6 4", "6 1' 2' 1' 6", "5"],
       ["ことしの", "ゆき", "きみがいる", "の", "ゆびきりを", "した", "あしたまで", "ね"]),
 "B2": (["..x-x-x-x-x-x-x-", "x---------------", "..x-x-x-x-x-x---", "x-------x-------", "..x-x-x-x-x-x---", "x-------x-------"],
        ["3 3 5 6 5 3 5", "b6", "5 5 3 2 3 5", "5 3", "1' 1' 7 6 7 1'", "2' 1'"],
        ["おなじそらをみ", "て", "あるいてゆく", "よる", "ゆきがとける", "まで"]),
}


def put(name):
    pats, degs, words = VS[name]
    lines, text = song_lines(list(zip(pats, degs, words))); bars = S.sc(name); ml = [KG.mel(x, oct=3) for x in lines]
    for b, m in zip(bars, ml):
        if m.replace("R:4", "").strip(): V.bar(b, m)
    LY.flow(bars[:len(ml)], ml, text, name)


if VOCAL:
    for nm_ in VS: put(nm_)
    duet("フック1", HOOK); duet("フック2", HOOK)                                     # フックは楽器だけ（歌はない）
else:
    duet("サビ別", SBE); duet("フック1", HOOK); duet("B1", B1L); duet("サビ", CHO); duet("新", NEW); duet("フック2", HOOK); duet("A", AL); duet("B2", B2L, both=True)

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "サビ別":                                                    # いきなりサビ。緩急: 全員 → 3小節めは2拍で止めてスクラッチ → 全員 → 7小節めは半分の速さ → 最後に巻きもどし
        if i == 0: VIN.bar(b, "A#5:4")
        if i in (2, 6):
            funk(b, i, stop=2.0, clap=True); bass(b, cutp(BK[i % 4], 2.0)); saw(b, cutp("x..x..x...x..x..", 2.0)); ep(b, cutp("x..x......x.....", 2.0)); dj(b, 2.5, "baby" if i == 2 else "chirp", 1.0)
        else:
            funk(b, i, clap=True, bell=True); bass(b, BK[i % 4]); saw(b); ep(b)
        if i == 0: fxh(b, 0, "impact", 2)
        if last: dj(b, 3.0, "rewind", 1.0)
    elif n in ("立ち上げ1", "立ち上げ2"):                                # だんだん増える: 前半はエレピとオルゴールと雪、後半からドラム
        ep(b, "x.........x.....", 62, short=1.0); swell(b)
        if i < 4: snow(b) if i % 2 == 0 else None; mbox(b, "x.......x.......")
        else: funk(b, i, stop=None if i < 7 else 3.0); bass(b, BK[i % 4]); mbox(b)
        if i == 4: fxh(b, 0, "riser", 4)
        if last: dj(b, 3.0, "chirp", 1.0)
    elif n in ("フック1", "フック2", "サビ"):                              # 全員＋そりの鈴。4小節ごとの最後は3拍で止めてスクラッチ
        stop = 3.0 if i % 4 == 3 else None
        funk(b, i, stop=stop, clap=True, bell=True); bass(b, cutp(BK[i % 4], stop) if stop else BK[i % 4])
        saw(b, cutp("x..x..x...x..x..", stop) if stop else "x..x..x...x..x.."); ep(b, cutp("x..x......x.....", stop) if stop else "x..x......x.....")
        if n == "サビ": swell(b); mbox(b, "..x...x...x...x.")
        if stop: dj(b, 3.0, "baby" if i % 8 == 3 else "chirp", 1.0)
        if i == 0: fxh(b, 0, "impact", 2)
        if last and n == "フック2": fxh(b, 0, "down", 4)
    elif n == "B1":                                                      # 1小節の短い句（ふたりが交代）。ドラムはまばら
        bounce(b, i); bass(b, "r-........r-...."); ep(b, "x.......x.......", 62); low_pn(b)
        if last: dj(b, 3.0, "rewind", 1.0)
    elif n == "新":                                                      # 3小節の句。ファンクだが和音は少なめ
        funk(b, i); bass(b, BK[i % 4]); ep(b, "x.........x.....", 62); low_pn(b) if i % 3 == 0 else None
        if i >= 6: saw(b, "x.......x.......", short=1.0)
        if last: fxh(b, 0, "riser", 4)
    elif n == "A":                                                       # 静か: 雪のきらめきとオルゴールとエレピ
        bounce(b, i) if i >= 4 else None; ep(b, "x---------------", 62, short=4); snow(b) if i % 2 == 0 else None; mbox(b, "x.......x.......")
        if last: fxh(b, 0, "riser", 4)
    elif n == "B2":                                                      # 終わり: ふたりが3度で重なり、最後の2小節でテープストップ
        if i < 6: funk(b, i, clap=True, bell=True); bass(b, BK[i % 4]); ep(b); swell(b)
        elif i == 6: ep(b, "x---------------", 62, short=4); bass(b, "r---------------"); dj(b, 2.0, "stop", 2.0)
        else: snow(b)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: ヒップホップ × Kawaii future bass のインスト（110・ト長調・約2分55秒）。雪の降るクリスマスの夜、「あなた」（エレピ）と「私」（夢のようなリード）が1小節ずつかけ合いながら歩き、"
          "最後のサビでだけ3度で重なる。DJ のスクラッチ・巻きもどし・テープストップ、そりの鈴と雪のきらめき。いきなり緩急のあるサビから始まり、テープストップで止まって終わる。自作")
finish(S, LY, V, 0, flat=True, lead_vol=0.0)  # v8: 歌の版でも歌をなぞるシンセは鳴らさない（「ヒョイ」の音）

from vt3x_lib import *
path = sys.argv[1]
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"verse": 8, "bridge": 6, "chorus": 14, "outro": 10}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("B2", 0, None, KG)], vol=0.25)                                 # 最後の場面だけ、ふたりの声（下の3度）が重なる
    voice_by_scene(path, S, {}, default="cute")                                        # 1曲1種類の声: キュート
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path)
keep = (lambda p_: p_.get("patch") != "kfbSineLead") if not VOCAL else (lambda p_: True)
js["parts"] = [p_ for p_ in js["parts"] if keep(p_) and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "laidback"; js["human"] = 0.35; js["swing16"] = 0.62
save(path, js)
