# UG 02「ログインの春」（仮）Login Spring — インスト。ピアノとシンセと効果音だけ。4分の4・200・ホ長調（はじめ210、人間の指示で200に）。196小節・約3分55秒。
#
# 2026-11-28 人間「ピアノとシンセとFXでインスト曲。テンポ210。コンセプトはデジタルワールドで新しい恋」
#   楽器: ピアノ（右手の旋律・左手の和音）／シンセ（ベース2種・パッド・矩形波のプラック・声のようなリード・グロッケン）／効果音（kawaiiFx）。ドラムセット・ギター・エレキベースは使わない。
#   打楽器の役は効果音でやる（やわらかいキック A4・スネア A#4・ハイハット C#5/D5・リム D#5・レーザー A5・グリッチ D#6）。UG01 の硬いキック・手びょうし・指パッチンは使わない。
# 形: くじ（tools/vt3/form_dice.py --skeleton 4127 225 210 --min-chorus 2 --not-groove pogo --not-groove laid --not-start ベース）。
#   始まり＝いきなり歌（伴奏なしで1句）→ インストなので、ピアノだけで1句／終わり＝テンポを落として終わる／リズム＝2ビート（ドッタン・ドッタン、前のめり）
# 物語: デジタルの世界。ピアノの子（彼女）と、声のようなシンセのリードの子が出会う。はじめは通信が1拍おくれて、リードはピアノの旋律を1拍あとからまねする。
#   場面が進むほど遅れが短くなり（1拍→半拍）、最後の B で2人の旋律がぴったり重なる（つながる）。そのあとテンポが落ちて、静かにログアウトせずに終わる。
# この曲だけのもの: 1拍ずれの追いかけっこが最後にぴったり重なる／♭III（G）と ♭VI（C）へ、画面が切りかわるように飛ぶ和音。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("38", "login", "ログインの春（仮）", "Login Spring", 200, 4, "E", "major", "インスト（ピアノとシンセ）")
S.flags = S.flags + " --space room --space-wet 0.1"
KA = Key("E", "major")
CH = ["Amaj7", "B/A", "G#m7", "C#m7", "F#m9", "D", "Esus4", "E"]                        # サビ: IV → V/IV → iii → vi ／ ii → ♭VII → Isus4 → I
CHB = ["Amaj7", "B/A", "G#m7", "C#m7", "Cmaj7", "D", "Esus4", "E"]                      # サビ2・B: ii の所を ♭VI（C）へ飛ばす
SE = ["C#m7", "C#m7", "Cmaj7", "Cmaj7", "Amaj7", "Amaj7", "Bsus4", "B", "C#m7", "C#m7", "Gmaj7", "Gmaj7", "Amaj7", "F#m9", "Bsus4", "B"]   # 出会い（サビ別）
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("起動", 10, "intro", ["E", "E", "Amaj7", "Amaj7", "G#m7", "C#m7", "F#m9", "F#m9", "Bsus4", "B"])
scene("出会い", 16, "chorus", SE)
scene("ネットの中", 16, "verse", ["E", "E", "B/D#", "B/D#", "C#m7", "C#m7", "Gmaj7", "Gmaj7", "Amaj7", "Amaj7", "E/G#", "E/G#", "F#m9", "F#m9", "Bsus4", "B"])
scene("A1", 4, "verse", ["Amaj7", "Amaj7", "Bsus4", "B"])
scene("サビ1", 8, "chorus", CH)
scene("サビ半", 8, "chorus", CH)
scene("迷子", 8, "bridge", ["C#m7", "C#m7", "Cmaj7", "Cmaj7", "Amaj7", "Amaj7", "Bsus4", "B"])
scene("ドロップ", 10, "break", ["C#m7", "C#m7", "Amaj7", "Amaj7", "E", "E", "B", "B", "C#m7", "B"])
scene("フック", 4, "break", ["Amaj7", "B", "C#m7", "Cmaj7"])
scene("近づく", 16, "pre", ["E", "E", "G#m7", "G#m7", "Amaj7", "Amaj7", "E", "E", "C#m7", "C#m7", "D", "D", "Amaj7", "F#m9", "Bsus4", "B"])
scene("A2", 16, "verse", ["E", "E", "B/D#", "B/D#", "C#m7", "C#m7", "Gmaj7", "Gmaj7", "Amaj7", "Amaj7", "E/G#", "E/G#", "F#m9", "F#m9", "Bsus4", "B"])
scene("サビ2", 8, "chorus", CHB)
scene("早口1", 10, "verse", ["C#m7", "C#m7", "Amaj7", "Amaj7", "E", "E", "B", "B", "Cmaj7", "D"])
scene("静か", 6, "bridge", ["Amaj7", "Amaj7", "G#m7", "G#m7", "Bsus4", "B"])
scene("早口2", 16, "verse", ["C#m7", "C#m7", "Amaj7", "Amaj7", "E", "E", "B", "B", "C#m7", "C#m7", "Gmaj7", "Gmaj7", "Amaj7", "Amaj7", "Bsus4", "B"])
scene("A3", 16, "verse", ["E", "E", "B/D#", "B/D#", "C#m7", "C#m7", "Gmaj7", "Gmaj7", "Amaj7", "Amaj7", "E/G#", "E/G#", "F#m9", "F#m9", "Bsus4", "B"])
scene("ソロ", 8, "break", ["C#m7", "Amaj7", "E", "B", "C#m7", "Amaj7", "Cmaj7", "D"])
scene("B", 16, "outro", CHB + ["Amaj7", "B/A", "G#m7", "C#m7", "Cmaj7", "D", "Esus4", "E"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

# v10（人間「テンポ200にしましょう。あとピアノにデジタルエフェクトかけましょう」）: ピアノに、ビットを落とした音（bitcrusher）と左右に跳ねるやまびこ（pingpong・3/4拍）をかける
DFX = lambda bits, mix: [{"type": "bitcrusher", "bits": bits}, {"type": "pingpong", "beats": 0.75, "mix": mix, "feedback": 0.3}, {"type": "filter", "kind": "lowpass", "freq": 7500, "q": 0.6}]
PR = S.track("ピアノ（右手・旋律）", "piano", volume=0.4, pan=-0.12, reverb=0.16, fx=DFX(8, 0.18))
PR2 = S.track("ピアノ（右手・速弾き）", "piano", volume=0.22, pan=0.1, reverb=0.16, fx=DFX(7, 0.22))
PL = [S.track(f"ピアノ（左手・和音）{i + 1}", "piano", volume=0.15, pan=(-0.2, -0.08, -0.14)[i], reverb=0.16, fx=[{"type": "bitcrusher", "bits": 9}]) for i in range(3)]
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.2, pan=0, gainDb=-6)
GRW = S.track("シンセのベース（うなる）", "bass", patch="kfbGrowlBass", volume=0.1, pan=0, gainDb=-8, fx=[{"type": "filter", "kind": "lowpass", "freq": 3000, "q": 0.6}])
BT = [SUB]
PAD = [S.track(f"パッド（結晶）{i + 1}", "pad", patch="surgePadCrystals", volume=0.12, pan=(-0.35, 0.35, 0)[i], reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(3)]
ARP = S.track("矩形波のプラック（駆け上がり）", "lead", patch="kfbSquarePluck", volume=0.1, pan=0.25, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.35}])
LEAD = S.track("声のようなリード", "lead", patch="kfbFormantLead", volume=0.17, mono=True, pan=0.12, reverb=0.28, fx=[{"type": "filter", "kind": "lowpass", "freq": 5200, "q": 0.6}, {"type": "delay", "beats": 0.5, "mix": 0.12, "feedback": 0.25}])
LEADF = S.track("声のようなリード（遅れてまねする影）", "lead", patch="kfbFormantLead", volume=0.075, mono=True, pan=0.3, reverb=0.4, fx=[{"type": "filter", "kind": "lowpass", "freq": 3400, "q": 0.6}])   # 遅れてまねする所は、影のように小さく・やわらかく（1拍ずれの重なりで濁らないように）
# ---- v4（2026-11-28 人間「もっと歯切れをよく。地下の曲みたいなデジタル感で、テクノポップみたいな感じ。高音を入れて、浮き沈みと緩急、休符も」「始まりの部分が主に」）----
DIRT = S.track("シンセのベース（汚れて太い・はじまり）", "bass", patch="surgeBassModernDirtyFat", volume=0.11, pan=0, gainDb=-7, fx=[{"type": "filter", "kind": "lowpass", "freq": 2600, "q": 0.6}])
# kfbSawStab は、入れるだけで曲全体の音が明るく・低音が細くなり点が 7.6 → 6.4 に下がった（使わない）
STAB = [S.track(f"短い和音（デジタルのプラック）{i + 1}", "keys", patch="modernPluck", volume=0.055, pan=(-0.3, 0.3, 0)[i], reverb=0.15, fx=[{"type": "filter", "kind": "lowpass", "freq": 5200, "q": 0.6}]) for i in range(3)]
DPLK = S.track("デジタルのプラック（はじまり）", "lead", patch="modernPluck", volume=0.1, pan=-0.3, reverb=0.2, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.22, "feedback": 0.3}])
HI = S.track("高いきらめきのリード", "lead", patch="kfbSquareLead", volume=0.05, mono=True, pan=0.2, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6800, "q": 0.6}, {"type": "pingpong", "beats": 0.5, "mix": 0.2, "feedback": 0.25}])
GLK = S.track("グロッケン（きらめき）", "keys", patch="kfbGlocken", volume=0.06, pan=0.35, reverb=0.4, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
FX = lambda name, v, pn=0.0: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=0.08, modulate=False)
FK, FSN, FH, FR, FL = FX("効果音（やわらかいキック）", 0.13), FX("効果音（スネア）", 0.08, 0.04), FX("効果音（ハイハット）", 0.045, 0.22), FX("効果音（リム）", 0.05, -0.2), FX("効果音（レーザーとグリッチ）", 0.035, -0.3)
FCL, FHC, FGL = FX("効果音（手びょうし）", 0.075, 0.06), FX("効果音（閉じたハイハット）", 0.035, -0.22), FX("効果音（グリッチ）", 0.045, 0.3)
# 始まりの2場面は、別のトラックで鳴らす（同じトラックに足すと、トラックごとの大きさの自動調整が曲全体で変わり、後ろの場面まで音が明るく・低音が細くなった。v4・v5 で 7.63 → 6.38）
INTRO = dict(FK=FX("効果音（やわらかいキック・はじまり）", 0.13), FSN=FX("効果音（スネア・はじまり）", 0.08, 0.04), FH=FX("効果音（ハイハット・はじまり）", 0.045, 0.22),
             SUB=S.track("シンセのベース（低い正弦波・はじまり）", "bass", patch="kfbSub", volume=0.2, pan=0, gainDb=-6),
             PAD=[S.track(f"パッド（結晶・はじまり）{i + 1}", "pad", patch="surgePadCrystals", volume=0.12, pan=(-0.35, 0.35, 0)[i], reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6}]) for i in range(3)],
             ARP=S.track("矩形波のプラック（はじまり）", "lead", patch="kfbSquarePluck", volume=0.1, pan=0.25, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.35}]),
             PR=S.track("ピアノ（右手・旋律・はじまり）", "piano", volume=0.4, pan=-0.12, reverb=0.07, fx=DFX(8, 0.15)),
             LEADF=S.track("声のようなリード（遅れてまねする影・はじまり）", "lead", patch="kfbFormantLead", volume=0.075, mono=True, pan=0.3, reverb=0.4, fx=[{"type": "filter", "kind": "lowpass", "freq": 3400, "q": 0.6}]),
             FXT=S.track("効果音（はじまりの上がる音・当たる音・きらめき）", "guitar", patch="kawaiiFx", volume=0.065, pan=0.1, reverb=0.3, modulate=False))
MAIN = {}
def use(intro):
    """始まりの場面を書くときだけ、トラックを差しかえる"""
    global FK, FSN, FH, SUB, PAD, ARP, PR, LEADF, FXT
    if intro:
        if not MAIN: MAIN.update(FK=FK, FSN=FSN, FH=FH, SUB=SUB, PAD=PAD, ARP=ARP, PR=PR, LEADF=LEADF, FXT=FXT)
        FK, FSN, FH, SUB, PAD, ARP, PR, LEADF, FXT = (INTRO[k] for k in ("FK", "FSN", "FH", "SUB", "PAD", "ARP", "PR", "LEADF", "FXT"))
    elif MAIN:
        FK, FSN, FH, SUB, PAD, ARP, PR, LEADF, FXT = (MAIN[k] for k in ("FK", "FSN", "FH", "SUB", "PAD", "ARP", "PR", "LEADF", "FXT"))
    BT[0] = SUB
FXT = S.track("効果音（上がる音・下がる音・逆回しのシンバル・当たる音・低く落ちる音・きらめき）", "guitar", patch="kawaiiFx", volume=0.065, pan=0.1, reverb=0.3, modulate=False)
N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "down": "G4", "rev": "G#4", "impact": "G5", "subdrop": "G#5", "spark": "D4", "drop": "C#4"}
def fxh(b, at, name, L): FXH.setdefault(b, []).append((at, name, L))
mel = lambda s, up=0: KA.mel(s, oct=3 + up)                                          # 1＝E3。ピアノの旋律は 5（B3）〜 5''（B5）


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


def perc(b, k=None, s=None, h=None, r=None, l=None, oh=False):
    if k: grid(FK, b, k, "A4")
    if s: grid(FSN, b, s, "A#4")
    if h: grid(FH, b, h, "D5" if oh else "C#5")
    if r: grid(FR, b, r, "D#5")
    if l: grid(FL, b, l, "A5")


# 2ビート（ドッタン・ドッタン）。前のめり（pushed）にするため、4小節めは3拍めのキックを半拍前に食う
def two(b, i, hat=True, ghost=False):
    k = ("X.......X.......", "X.......X.......", "X.......X.......", "X.....X.X.......")[i % 4]
    s = ("....X.......X...", "....X.......X..x" if ghost else "....X.......X...")[i % 2]
    perc(b, k, s, "..x...x...x...x." if hat else None, oh=(i % 8 == 7))
def tp(b, i, stop=None):
    """テクノポップの4つ打ち: キック4分・手びょうし2と4・開いたハイハットは裏・閉じたハイハットは16分の弱い所。stop＝その拍から休む（休符のブレイク）"""
    k = ("X...X...X...X...", "X...X...X...X..x", "X...X...X...X...", "X...X...X.x.X...")[i % 4]
    c = "....X.......X..."; oh = "..x...x...x...x."; ch = ".x...x...x...x.x"
    if stop is not None:
        cut = int(stop * 4); k, c, oh, ch = (x[:cut] + "." * (16 - cut) for x in (k, c, oh, ch))
    grid(FK, b, k, "A4"); grid(FCL, b, c, "B4"); grid(FH, b, oh, "D5"); grid(FHC, b, ch, "C#5")
def glitch(b, pat): grid(FGL, b, pat, "D#6")
def octb(b, i, stop=None, dirt=True):
    """オクターブを8分で行き来する短いベース（テクノポップ）。stop＝その拍から休む"""
    p = ("r.R.r.R.r.R.r.R.", "r.R.r.R.5.R.r.R.", "r.R.r.R.r.R.7.R.", "r.R.r.RRr.R.5.R.")[i % 4]
    if stop is not None: p = p[:int(stop * 4)] + "." * (16 - int(stop * 4))
    bass(b, p)
    if dirt: BT[0] = DIRT; bass(b, p); BT[0] = SUB
def stab(b, pat="..x...x...x...x.", center=70): _ch(STAB, b, pat, center, 3)
def gpad(b, pat="x-.x-.x-.x-.x-.."): _ch(PAD, b, pat, 64, 3)                       # 切りきざんだパッド（ゲート）
def hi(b, cell): ct(HI, b, cell, center=88)
def stac(lines, f=0.5):
    """1拍以下の音を短く切って、あとを休符にする（歯切れ）"""
    out = []
    for l in lines:
        toks = []
        for x in l.split():
            a, L = x.split(":"); L = float(L)
            if a != "R" and L <= 1.0 + 1e-6: toks += [f"{a}:{L * f:g}", f"R:{L * (1 - f):g}"]
            else: toks.append(x)
        out.append(" ".join(toks))
    return out
def half(b, i):                                                         # 静かな場面: キックとリムだけ（半分の速さ）
    perc(b, "X...............", None, None, "........x.......")

# ================= 伴奏 =================
def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "dim" if ("m7b5" in rest or "dim" in rest) else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


def bass(b, pat="r---------------"):
    """r 根音・3＝3度・5＝5度・7＝7度（短7）・R＝1オクターブ上・- のばす・. 休み。分数の和音は下の音が根音"""
    ch = S.chords[b]; r = low(ch, "E1"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 7
    off = {"r": 0, "3": t3, "5": 7, "7": 10, "R": 12}; out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + off[pat[i]])}:{L * 0.25:g}" + ("!" if i % 8 == 0 else "")); i += L
    BT[0].bar(b, " ".join(out))


def _ch(tracks, b, pat, center, n):
    v = sorted(voice(S.chords[b], center, n))
    for j in range(n):
        out = []; i = 0
        while i < 16:
            L = 1
            while i + L < 16 and pat[i + L] == "-": L += 1
            out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(v[j])}:{L * 0.25:g}"); i += L
        tracks[j].bar(b, " ".join(out))


def pad(b, center=64): _ch(PAD, b, "x---------------", center, 3)
def crisp(pat):
    """左手の和音を歯切れよく: 1つの音は8分（2マス）まで、残りは休み"""
    out = list(pat)
    for i, c in enumerate(pat):
        if c == "-" and not (i >= 1 and pat[i - 1] in "xX"): out[i] = "."
    return "".join(out)
def lh(b, pat="x-------x-------", center=55):
    _ch(PL, b, pat if S.scene_of(b)[0] == "静か" else crisp(pat), center, 3)        # v10（人間「ピアノは歯切れよく」）: 静かな場面のほかは短く


def ct(tr, b, cell, center=66, up=0):
    """和音の音で書く句。0〜3＝その小節の和音の音（低い方から）、+ で1オクターブ上、- で下"""
    v = sorted(voice(S.chords[b], center, 4)); out = []
    for x in cell.split():
        a, L = x.split(":")
        if a == "R": out.append(x); continue
        out.append(f"{N(v[int(a[0])] + 12 * (a.count('+') - a.count('-')) + up)}:{L}")
    assert abs(sum(float(x.split(':')[1].rstrip('!')) for x in out) - 4) < 1e-6, cell
    tr.bar(b, " ".join(out))


def arp(b, k=0):
    """矩形波のプラックで和音を16分で駆け上がる（最後の音はやまびこで残る）"""
    t = sorted(voice(S.chords[b], 74, 4)); up = [t[0], t[1], t[2], t[3], t[0] + 12, t[1] + 12, t[2] + 12, t[3] + 12]
    ARP.bar(b, ("R:2 " if k % 2 else "") + " ".join(f"{N(x)}:0.25" for x in up) + (" R:2" if not k % 2 else ""))


# ---- 旋律: ピアノ（彼女）の句を書き、リード（相手）は D 拍おくれてまねする ----
def _split(line):
    return [(x.split(":")[0], float(x.split(":")[1])) for x in line.split()]


def shift(bars_lines, d):
    """句の列（1小節ずつ）を d 拍おくらせる。最後の小節からはみ出た分は切る"""
    ev = []
    for l in bars_lines: ev += _split(l)
    tot = 4 * len(bars_lines); out = [("R", d)] if d else []; t = d
    for nm_, L in ev:
        if t >= tot - 1e-6: break
        L = min(L, tot - t); out.append((nm_, L)); t += L
    res = []; cur = []; acc = 0.0
    for nm_, L in out:
        while L > 1e-6:
            take = min(L, 4 - acc); cur.append((nm_, take)); acc += take; L -= take
            if acc >= 4 - 1e-6: res.append(" ".join(f"{a}:{x:g}" for a, x in cur)); cur = []; acc = 0.0
    if cur: cur.append(("R", 4 - acc)); res.append(" ".join(f"{a}:{x:g}" for a, x in cur))
    while len(res) < len(bars_lines): res.append("R:4")
    return res


def theme(name, lines, follow=None, up=0, lead_up=1, start=0, tr=None):
    """lines を場面の start 小節めから。follow＝リードがまねする遅れ（拍）。0 ならぴったり重なる。None ならまねしない"""
    bars = S.sc(name)[start:]; ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) <= len(bars), (name, len(ls), len(bars))
    if name not in ("静か", "起動", "出会い"): ls = stac(ls, 0.5)                    # v10: ピアノの旋律は、1拍以下の音を半分にして歯切れよく（起動・出会いはもう短い）
    for b, l in zip(bars, ls):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l != "R:4": (tr or PR).bar(b, mel(l, up))
    if follow is not None:
        for b, l in zip(bars, shift(ls, follow)):
            if l.replace("R:4", "").strip(): (LEAD if follow == 0 else LEADF).bar(b, mel(l, lead_up))


# 起動: ピアノだけの1句（伴奏なし）。同じ音を2つ打って、6度上へ跳ぶ「呼びかけ」
CALL = ["R:1 1:0.5 3:0.5 5:1.5 1':0.5", "3':1 2':0.5 1':0.5 5:2"]
# 出会い（サビ別）: 同じ音を連打してから跳ぶ。2小節ずつ
SEL = ["3:0.25 3:0.25 3:0.25 R:0.25 6:0.75 1':0.75 3':1.5", "3':0.75 1':0.75 6:0.5 R:2", "5:0.25 5:0.25 5:0.25 R:0.25 b3':0.75 5':0.75 b3':1.5", "5':3 R:1",
       "1:0.25 1:0.25 1:0.25 R:0.25 4:0.75 6:0.75 1':1.5", "3':0.75 4':0.75 3':0.5 R:2", "5:0.25 5:0.25 5:0.25 R:0.25 1':0.75 2':0.75 5':1.5", "7:0.75 2':0.75 5':1.5 R:1"]   # v8: Cmaj7・Gmaj7・Bsus4 の上でぶつかる音（G#・A#・D#・E）をやめた
# ネットの中: 小節のまん中から入る
NET = ["R:2 3:0.75 5:0.75 1':0.5", "3':1.5 1':1 R:1.5", "R:2 2:0.75 5:0.75 7:0.5", "2':2.5 R:1.5", "R:2 3:0.75 6:0.75 1':0.5", "3':0.75 1':0.75 6:0.5 R:2", "R:2 5:0.75 b3':0.75 5':0.5", "2':3 R:1",
       "R:2 1':0.75 3':0.75 4':0.5", "6':1.5 4':1 R:1.5", "R:2 3:0.75 5:0.75 1':0.5", "5':2.5 R:1.5", "R:2 6:0.75 1':0.75 3':0.5", "2':0.75 1':0.75 6:0.5 R:2", "R:2 1':0.75 2':0.75 5':0.5", "2':0.75 7:0.75 5:2 R:0.5"]
A1L = ["R:2 6:1 1':1", "3':4", "R:2 1':1 2':1", "5':4"]                                   # 休みから入って最後をのばす
# サビ: 4小節のばす長い句（上へ跳んで、高い所でのばす）
SB = ["R:1 1':1 3':1 5':1", "6':2 5':2", "R:1 3':1 5':1 7':1", "1'':4", "R:1 1':1 5':1 1'':1", "4':2 2':2", "R:1 1':1 4':1 5':1", "5':4"]
SBH = ["3':2 5':2", "5':4", "3':2 5':2", "6':2 1'':2", "6':2 1'':2", "4':4", "4':2 5':2", "3':4"]  # 半分の速さ（2小節の句）
MAY = ["5':0.75 3':0.75 1':0.5 6:0.75 3:1.25", "R:4", "5':0.75 b3':0.75 1':0.5 5:0.75 b3:1.25", "R:4", "3':0.75 1':0.75 6:0.5 4:0.75 3:1.25", "R:4", "5':0.75 2':0.75 1':0.5 5:0.75 2:1.25", "R:4"]   # 迷子: 高い音から下りる
NEAR = ["R:1 1:0.5 3:0.5 5:1 1':1", "3':1.5 2':0.5 1':2", "R:1 3:0.5 5:0.5 7:1 3':1", "2':1.5 7:0.5 5:2", "3':4",
        "R:1 1':0.5 3':0.5 4':1 6':1", "5':1.5 3':0.5 1':2", "R:1 3':0.5 5':0.5 3':1 1':1", "6:1.5 1':0.5 3':2", "1'':4",
        "R:1 2':0.5 4':0.5 2':1 4':1", "4':4", "R:1 1':0.5 3':0.5 6':1 1'':1", "6':1.5 4':0.5 1':2", "5':2 4':1 5':1", "R:4"]
A2L = ["3:0.5 5:0.25 1':0.25 R:0.5 3':0.5 5':2", "3':0.75 1':0.75 5:2.5", "2:0.5 5:0.25 7:0.25 R:0.5 2':0.5 5':2", "2':0.75 7:0.75 5:2.5", "3:0.5 6:0.25 1':0.25 R:0.5 3':0.5 6':2", "3':0.75 1':0.75 6:2.5", "5:0.5 b3':0.25 5':0.25 R:0.5 2':0.5 5':2", "R:4",
       "1':0.5 3':0.25 4':0.25 R:0.5 6':0.5 1'':2", "6':0.75 3':0.75 1':2.5", "3:0.5 5:0.25 1':0.25 R:0.5 3':0.5 5':2", "3':0.75 1':0.75 5:2.5", "4:0.5 6:0.25 1':0.25 R:0.5 3':0.5 4':2", "3':0.75 1':0.75 6:2.5", "5:0.5 1':0.25 2':0.25 R:0.5 5':0.5 4':2", "7:3 R:1"]
FAST = ["0+:0.25 3:0.25 2:0.25 1:0.25 0:0.25 1:0.25 2:0.25 3:0.25 0+:0.5 1+:0.5 2+:1", "1+:0.25 0+:0.25 3:0.25 2:0.25 1:0.25 2:0.25 3:0.25 0+:0.25 1+:1 R:1",
        "2:0.25 3:0.25 0+:0.25 1+:0.25 2+:0.25 1+:0.25 0+:0.25 3:0.25 2:1 R:1", "3:0.25 2:0.25 1:0.25 0:0.25 1:0.25 2:0.25 3:0.25 0+:0.25 2+:2"]
FAST2 = ["3:0.25 0+:0.25 1+:0.25 2+:0.25 3+:0.5 2+:0.5 1+:0.5 0+:0.5 R:1", "R:3 2:1", "0+:0.5 3:0.25 2:0.25 1:0.5 2:0.5 3:1 R:1", "R:3 1:1"]   # 1拍早く食って入る（前の小節の4拍めから）
QUIET = ["3':0.5 3':0.5 6':3", "R:4", "3':0.5 3':0.5 7':3", "R:4", "1':0.5 1':0.5 5':3", "R:4"]
A3L = ["R:1 1':0.5 3':0.5 5':1 3':1", "1':2 5:2", "R:1 7:0.5 2':0.5 5':1 2':1", "7:2 5:2", "3':4",
       "R:1 6:0.5 1':0.5 3':1 6':1", "5':2 2':2", "R:1 5:0.5 b3':0.5 5':1 2':1", "1':2 3':2", "6':4",
       "R:1 3':0.5 5':0.5 1'':1 5':1", "3':2 1':1 5:1", "R:1 4:0.5 6:0.5 1':1 3':1", "6':2 4':2", "5':2 4':1 2':1", "7:4"]
SOLO = ["0+:0.75 3:0.75 2:0.5 3:0.75 0+:0.75 1+:0.5", "2+:1.5 1+:0.25 0+:0.25 3:2", "2+:0.25 1+:0.25 0+:0.25 3:0.25 2:0.75 3:0.75 0+:0.5 2+:1", "3+:3 R:1"]
HOOK = ["1':0.5 R:0.5 1':0.5 3':0.5 R:0.5 1':0.5 5':1", "5':0.5 2':0.5 7:1 R:2", "3':0.5 R:0.5 3':0.5 6':0.5 R:0.5 3':0.5 1'':1", "5':0.5 b3':0.5 1':1 5':2"]
BPT = ("r-..r-....5-r-..", "r-..r-..5-..r-R-", "r-....r-5-..r-..", "r-..r-..5-r-R-..")           # ベース（2ビートに合わせて）
BQT = ("r---------------", "r-----------5---", "r-------........", "r-------5-------")           # ベース（静か）
BDR = ("r-r-R-..r-..7-R-", "r-r-R-..5-r-..R-", "r-r-R-..r-..5-7-", "r-..R-r-7-..R-5-")           # ドロップ: うなるベースの16分


def full(b, i, k=0, growl=False, ar=True, ghost=False):
    two(b, i + k, ghost=ghost); BT[0] = GRW if growl else SUB; bass(b, (BDR if growl else BPT)[(i + k) % 4]); BT[0] = SUB
    if growl: SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:4")
    if ar: arp(b, i + k)


use(True)
# v8（人間「最初のピアノの旋律の余韻を短め」「不協和の音になってる」）: 5〜6小節めの句が G#m7・C#m7 の上で A・A# を鳴らしてぶつかっていた → 和音の音だけの句に。音は短く（0.35）、響きも少なく
CALL2 = ["R:1 3:0.5 5:0.5 7:1.5 5:0.5", "1':1 7:0.5 6:0.5 3':2"]
theme("起動", stac(CALL[:2], 0.35), up=1)                                             # 高い所で短く「呼びかけ」
theme("起動", stac(CALL2, 0.35), up=1, start=4)
theme("出会い", stac(SEL[:6] + ["R:4", "R:4"] + SEL[:6] + SEL[6:], 0.5), follow=1.0, up=1)   # 1オクターブ上で歯切れよく。8小節めは休む
use(False)                                                   # リードは1拍おくれてまねする
theme("ネットの中", NET)
theme("A1", A1L)
theme("サビ1", SB, follow=1.0, lead_up=0)
theme("サビ半", SBH)
theme("迷子", MAY)
theme("近づく", NEAR, follow=0.5)                                                     # 遅れが半拍に
theme("A2", A2L)
theme("サビ2", SB, follow=0.5, up=0)
theme("静か", QUIET)
theme("A3", A3L)
theme("B", SB + SB, follow=0, lead_up=1)                                              # つながる: リードがピアノの1オクターブ上で、ぴったり同時に
PIC = {}

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    use(n in ("起動", "出会い"))
    if n == "起動":
        # 浮き沈み: 0-1 ピアノだけ（高い・短い）＋グリッチ → 2-3 オクターブのベースと短い和音 → 4 半分で休む → 5-7 4つ打ち・プラック → 8 ブレイク（グリッチだけ）→ 9 立ち上げ
        if i < 2: glitch(b, ("..........x.x...", "......x.....xxxx")[i])
        elif i < 4: octb(b, i); stab(b); glitch(b, "............x...")
        elif i == 4: octb(b, 0, stop=2); stab(b, "..x...x........."); perc(b, "X...X..........."); glitch(b, "..........x.xxxx")
        elif i < 8: tp(b, i); octb(b, i); stab(b); ct(DPLK, b, ("0+:0.25 R:0.25 2:0.25 R:0.25 1+:0.25 R:0.75 3:0.25 R:0.25 0+:0.25 R:0.25 2+:0.5 R:0.5", "R:0.5 2:0.25 R:0.25 0+:0.25 R:0.25 3:0.25 R:0.75 1+:0.25 R:0.25 2+:0.5 R:0.5")[i % 2], center=74); hi(b, ("R:3 3:0.5 R:0.5", "R:2 2:0.25 R:0.25 3:0.5 R:1", "R:3 0+:0.5 R:0.5")[i - 5])
        elif i == 8: glitch(b, "x.x.x.x.xxxxxxxx"); fxh(b, 0, "rev", 4)
        else: perc(b, "X..............."); bass(b, "r..............."); fxh(b, 0, "riser", 4); glitch(b, "........x.x.xxxx")
        if i == 0: fxh(b, 0, "spark", 2)
    elif n == "出会い":
        # テクノポップ: 4つ打ち・オクターブのベース・裏の短い和音・ゲートのパッド。7小節めは2拍めで止めて休む／10-11小節めは沈む（キックだけ）／最後は3拍めで止める
        if i == 7: tp(b, i, stop=1); octb(b, i, stop=1); stab(b, "x..............."); glitch(b, "........x.x.xxxx")
        elif i in (10, 11): perc(b, "X.......X......."); bass(b, "r-------........"); gpad(b, "x---------------")
        elif last: tp(b, i, stop=2); octb(b, i, stop=2); stab(b, "..x...x........."); fxh(b, 2, "rev", 2)
        else:
            tp(b, i); octb(b, i, dirt=i >= 4); stab(b); gpad(b)
            if i >= 12: arp(b, i)
            if i in (2, 5, 13): glitch(b, "..............xx")
        if i not in (10, 11): hi(b, ("R:3 3:0.5 R:0.5", "R:1 2:0.25 R:0.25 3:0.5 R:2", "R:3 0+:0.25 R:0.25 1+:0.5", "R:4")[i % 4]) if i >= 4 else None
        if i == 0: fxh(b, 0, "impact", 2)
        if i == 12: fxh(b, 0, "impact", 2)
    elif n in ("ネットの中", "A2", "A3"):
        two(b, i, hat=i >= 4 or n != "ネットの中", ghost=n == "A3"); bass(b, BPT[i % 4] if n != "ネットの中" or i >= 8 else BQT[i % 4]); lh(b, "x-------..x-----" if i % 2 == 0 else "..x-------x-----")
        if i >= 8: pad(b)
        if n == "A3" and i >= 4: arp(b, i)
        if n == "A2" and i % 2 == 1: perc(b, None, None, None, None, "...........x....")   # たまにレーザー
        if last: fxh(b, 0, "riser", 4)
    elif n == "A1":                                                      # 休み: パッドとピアノとリムだけ
        pad(b, 60); lh(b, "x---------------"); half(b, i)
        if last: fxh(b, 0, "riser", 4)
    elif n in ("サビ1", "サビ2"):
        full(b, i, k=SC.index(n) % 4, ghost=n == "サビ2"); lh(b, "x-----x---x-----" if i % 2 == 0 else "x---x-----x---x-"); pad(b)
        if i == 0: fxh(b, 0, "impact", 2)
        if n == "サビ2" and i % 2 == 1: GLK.bar(b, " ".join(f"{N(x)}:0.5" for x in sorted(voice(S.chords[b], 86, 4)) * 2))
        if last: fxh(b, 0, "down", 4)
    elif n == "サビ半":                                                  # 半分の速さ: キックは1小節に1つ、スネアは3拍め
        perc(b, "X...............", "........X.......", "x...x...x...x..."); bass(b, BQT[i % 4]); lh(b, "x---------------"); pad(b); arp(b, i)
        if last: perc(b, "X...X...X.X.X.XX", "....X...X.X.XXXX"); fxh(b, 0, "riser", 4)
    elif n == "迷子":                                                    # パッドとピアノ。リムとグリッチだけ
        pad(b, 60); lh(b, "x-------x-------"); perc(b, None, None, None, "....x.......x...", "..............x.")
        if last: fxh(b, 0, "riser", 4)
    elif n == "ドロップ":
        full(b, i, k=2, growl=True, ar=False); pad(b, 60); lh(b, "x-..x-....x-..x-" if i % 2 == 0 else "..x-..x-....x-..", 57)
        ct(PR, b, ("0+:0.75 3:0.75 2:0.5 R:2", "R:1 1:0.75 2:0.75 3:1.5", "1+:0.75 0+:0.75 3:0.5 R:2", "R:1 3:0.75 0+:0.75 2+:1.5")[i % 4])
        if i % 2 == 1: perc(b, None, None, None, None, "x.x.......x.x...")
        if i == 0: fxh(b, 0, "subdrop", 4)
        if last: fxh(b, 0, "riser", 4)
    elif n == "フック":
        full(b, i, k=3); LEAD.bar(b, mel(HOOK[i], 0)); PR.bar(b, mel(HOOK[i], 1)) if i >= 2 else None; pad(b); lh(b, "x-----x---x-----")
        if i == 0: fxh(b, 0, "impact", 2)
        if last: fxh(b, 0, "down", 4)
    elif n == "近づく":                                                  # 前半はハーフ、後半から全員
        lh(b, "x-------x-------"); pad(b)
        if i < 8: perc(b, "X.......X.......", None, "..x...x...x...x."); bass(b, BQT[i % 4])
        else: full(b, i, ar=i >= 12)
        if last: perc(b, "X...X...X.X.X.XX", "....X...X.X.XXXX"); fxh(b, 0, "riser", 4)
    elif n in ("早口1", "早口2"):                                        # ピアノの速弾き（和音の音で16分）
        full(b, i, k=1, ar=False, ghost=True); lh(b, "x---x---x---x---", 52); pad(b) if i >= 4 else None
        if n == "早口1": ct(PR2, b, FAST[i % 4], center=68)
        else: ct(PR2, b, FAST2[i % 4], center=68)
        if i % 4 == 3: perc(b, None, None, None, None, "............x.x.")
        if last: fxh(b, 0, "riser" if n == "早口2" else "down", 4)
    elif n == "静か":                                                    # パッドとピアノだけ
        pad(b, 60); lh(b, "x---------------", 53)
        if last: fxh(b, 2, "rev", 2)
    elif n == "ソロ":                                                    # リードのソロ（和音の音で8分）
        full(b, i, k=1); ct(LEAD, b, SOLO[i % 4], center=72); lh(b, "x---x---x---x---"); pad(b)
        if i == 0: fxh(b, 0, "impact", 2)
        if last: perc(b, "X...X...X.X.XXXX", "x.x.x.x.xxxxXXXX"); fxh(b, 0, "riser", 4)
    elif n == "B":                                                       # つながる: 全員。最後の4小節は打楽器が抜けて、テンポが落ちる
        if i < 12:
            full(b, i, ghost=True); lh(b, "x-----x---x-----" if i % 2 == 0 else "x---x-----x---x-"); pad(b)
            if i % 2 == 1: GLK.bar(b, " ".join(f"{N(x)}:0.5" for x in sorted(voice(S.chords[b], 86, 4)) * 2))
            if i in (0, 8): fxh(b, 0, "impact", 2)
        else:
            pad(b); lh(b, "x---------------"); bass(b, "r---------------")
            if i == 12: fxh(b, 0, "spark", 2)
            if last: GLK.bar(b, f"{N(76)}:0.5 {N(80)}:0.5 {N(83)}:0.5 {N(88)}:2.5")

use(False)
FXHI = {b: h for b, h in FXH.items() if S.scene_of(b)[0] in ("起動", "出会い")}
for b, hits in FXH.items():
    FXT_ = INTRO["FXT"] if b in FXHI else FXT
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT_.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: ピアノとシンセと効果音だけのインスト（200・ホ長調・約3分55秒）。デジタルの世界で、ピアノの子と声のようなシンセの子が出会う。はじめはリードが1拍おくれてまねし、"
          "遅れが半拍になり、最後の場面でぴったり重なる。形は、くじ（form_dice.py・種 4127）で決めた。ピアノだけで始まり、テンポを落として終わる。自作")
V = Voice(S, vol=0.0, delay=0.0, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead" and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "pushed"; js["human"] = 0.3
js["rit"] = {"bar": S.nb - 4, "bars": 4, "to": 0.55, "aTempo": False}                # 終わり方: 最後の4小節でテンポを落とす
save(path, js)
