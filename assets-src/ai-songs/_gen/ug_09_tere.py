# UG 09「照れたら負け」（仮）Blush and You Lose — インスト。Kawaii future bass × J-POP。4分の4・160・変ロ長調 → ハ長調。110小節・約2分45秒（3分以内）。
#
# 2026-11-29 人間「次は始まりから心掴むような感じで行こう。kawaiifutureベースでjpopテンポ160。ピアノ、シンセ、FXを入れて。緩急と間を入れる。アルペジオも入れる。コンセプトは愛してるゲーム」
#   歌の指定がないのでインスト。楽器: ピアノ（和音・左手の分散和音・旋律・速いアルペジオのソロ）／シンセ（低い正弦波のベース・スーパーソウ・ふくらむスーパーソウ・
#   矩形波のプラックの駆け上がるアルペジオ・すっきりしたポップなリード popLeadClear）／FX（kawaiiFx の電子ドラム・上がる音・逆回しのシンバル・当たる音・グリッチ）。
#   使わない: kfbSawStab・kfbBrightBells・モノのスーパーソウのリード・音の頭が持ち上がる／すべるリード（kfbDreamLead・kfbTranceLead・brightLead・surgeHappySaws。測って確かめた）。
# 形: くじ（tools/vt3/form_dice.py --skeleton 1601 165 160 --min-chorus 2 --not-start 伴奏なし --not-groove pogo）。
#   始まり＝くじは「手びょうしと声の切れはし」。歌がないので「手びょうしと、サビの旋律の切れはし（ピアノのアルペジオ）」にして、1拍の間をあけてから入る（心をつかむ）。
#   終わり＝全員で1打して止まる。リズム＝2ビート（主・ドッタン、前のめり）／ブレイクビート（静かな場面）。
# 物語（愛してるゲーム）: 「愛してる」と言い合って、先に照れたほうが負け。ピアノ（ぼく）とリード（きみ）が旋律を言い合い、だんだん交代が速くなり（4拍 → 2拍 → 1拍）、
#   最後はふたり同時に言って引き分け。1小節の「止まる」は、照れて言葉が出なくなる間。最後は1つ上の調（ハ長調）で、全員の1打＝「負けました」。
# この曲だけのもの: 交代がだんだん速くなるかけ合い（B）と、ピアノの32分のアルペジオのソロ／Ebmaj7 → Ebm6（照れの iv6）。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("45", "tere", "照れたら負け（仮）", "Blush and You Lose", 160, 4, "Bb", "major", "インスト（Kawaii future bass × J-POP）")
S.flags = S.flags + " --space room --space-wet 0.12"
KB = Key("Bb", "major"); KC = Key("C", "major")
CHA = ["Ebmaj7", "F", "Dm7", "Gm9", "Cm9", "F7sus4", "Bbmaj9", "D7"]
CHB = ["Ebmaj7", "F", "Dm7", "Gm9", "Ebmaj7", "Ebm6", "Bbmaj9", "Bbmaj9"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("つかみ", 8, "intro", ["Gm9", "Gm9", "Ebmaj7", "Ebmaj7", "Cm9", "Cm9", "F7sus4", "F"])
scene("サビ1", 16, "chorus", CHA + CHB)
scene("ドロップ1", 8, "drop", ["Ebmaj7", "F", "Dm7", "Gm9", "Ebmaj7", "F", "Gm9", "Gm9"])
scene("ソロ", 4, "solo", ["Cm9", "Dm7", "Ebmaj7", "F7sus4"])
scene("サビ半", 12, "chorus", CHA + ["Ebmaj7", "Ebm6", "Bbmaj9", "F7sus4"])
scene("静か", 12, "verse", ["Gm9", "Dm7", "Ebmaj7", "Bbmaj7", "Cm9", "Gm9", "Abmaj7", "F7sus4", "Gm9", "Dm7", "Ebmaj7", "F"])
scene("止まる", 1, "break", ["F"])
scene("言い合い", 12, "verse", ["Bbmaj9", "Dm7", "Ebmaj7", "F", "Gm9", "Dm7", "Cm9", "F7sus4", "Bbmaj9", "Dm7", "Ebmaj7", "Ebm6"])
scene("B", 16, "bridge", ["Cm9", "Dm7", "Ebmaj7", "F", "Cm9", "Dm7", "Gm9", "Gm9", "Ebmaj7", "F", "Dm7", "Gm9", "Cm9", "Dm7", "Ebmaj7", "F7sus4"])
scene("立ち上げ", 6, "pre", ["Ebmaj7", "Ebmaj7", "F", "F", "Gsus4", "G7"])
scene("ドロップ2", 6, "drop", ["Fmaj7", "G", "Em7", "Am9", "Fmaj7", "G"])
scene("A", 9, "outro", ["Fmaj7", "G", "Em7", "Am9", "Dm9", "G7sus4", "Cmaj9", "Cmaj9", "C"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

LP = lambda f: {"type": "filter", "kind": "lowpass", "freq": f, "q": 0.6}
PC = [S.track(f"ピアノ（右手の和音）{i + 1}", "piano", volume=0.09, pan=(-0.12, 0.04, 0.16)[i], reverb=0.16) for i in range(3)]
PL = S.track("ピアノ（左手の分散和音）", "piano", volume=0.12, pan=-0.18, reverb=0.16)
PM = S.track("ピアノ（ぼくの旋律）", "piano", volume=0.17, pan=-0.08, reverb=0.18)
PA = S.track("ピアノ（速いアルペジオ）", "piano", volume=0.11, pan=0.2, reverb=0.22)
LEAD = S.track("ポップなリード（きみの旋律）", "lead", patch="popLeadClear", volume=0.11, mono=True, pan=0.1, reverb=0.24,
               fx=[LP(5600), {"type": "delay", "beats": 0.75, "mix": 0.14, "feedback": 0.28}])
PLK = S.track("矩形波のプラック（駆け上がるアルペジオ）", "keys", patch="kfbSquarePluck", volume=0.05, pan=0.28, reverb=0.25,
              fx=[LP(5400), {"type": "delay", "beats": 0.75, "mix": 0.24, "feedback": 0.36}])
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.22, pan=0, gainDb=-5)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.05, pan=(-0.42, 0.42, -0.16, 0.16)[i], reverb=0.24, duck=0.42, fx=[LP(5600)]) for i in range(4)]
SWL = S.track("空気感のあるスーパーソウ（のばす和音の根）", "pad", patch="kfbSupersawWide", volume=0.05, pan=0, reverb=0.38, fx=[LP(6000)])
PAD = S.track("やわらかいパッド", "pad", patch="modernPad", volume=0.05, pan=0, reverb=0.45, fx=[LP(6500)])
FX = lambda name, v, pn=0.0, rv=0.08: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=rv, modulate=False)
FK, FK2, FSN, FCL, FH, FOH, FRM, FTM = (FX("効果音（キック）", 0.14), FX("効果音（重いキック）", 0.07), FX("効果音（スネア）", 0.085, 0.04), FX("効果音（手びょうし）", 0.07, -0.06),
                                        FX("効果音（ハイハット）", 0.035, 0.22), FX("効果音（開いたハイハット）", 0.03, -0.22), FX("効果音（リム）", 0.05, 0.15), FX("効果音（タム）", 0.06, -0.1))
FXT = S.track("効果音（上がる音・逆回しのシンバル・当たる音・グリッチ）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.35, modulate=False)
V = Voice(S, vol=0.1, delay=0.0, bright=0.0, patch="popLeadClear", low=False); LY = Lyrics(S)        # 歌はない（音符を置かないので書き出されない）
N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "down": "G4", "rev": "G#4", "impact": "G5", "subdrop": "G#5", "glitch": "D#6"}
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
    if stop is None: return pat
    k = int(stop * 4); return pat[:k] + "." * (16 - k)


# ---- ドラム ----
def twobeat(b, i, stop=None, heavy=False, crash=False):
    """2ビート（ドッタン・ドッタン）。4小節めは前のめり（4拍めのうらにキック）。手びょうしはスネアに重ねる"""
    k = ("X.......X.......", "X.......X.....x.", "X.......X.x.....", "X.....x.X.....x.")[i % 4]; s = "....X.......X..."
    h = "x.x.x.x.x.x.x.x."; oh = "..............x." if i % 2 else "................"
    k, s, h, oh = cutp(k, stop), cutp(s, stop), cutp(h, stop), cutp(oh, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FCL, b, s, "B4"); grid(FH, b, h, "C#5")
    if "x" in oh: grid(FOH, b, oh, "D5")
    if heavy: grid(FK2, b, cutp("x.......x.......", stop), "F#5")
def brk(b, i, stop=None):
    k = ("x.........x.....", "x.....x...x.....")[i % 2]; s = "....x.......x..."; r = ("......x.......x.", "..x.......x.....")[i % 2]; h = "x.x.x.x.x.x.x.x."
    k, s, r, h = cutp(k, stop), cutp(s, stop), cutp(r, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FRM, b, r, "D#5"); grid(FH, b, h, "C#5")
def halftime(b, i, stop=None):
    k, s, h = "x.....x...x.....", "........X.......", "x...x...x...x..."
    k, s, h = cutp(k, stop), cutp(s, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FCL, b, s, "B4"); grid(FH, b, h, "C#5"); grid(FK2, b, cutp("x...............", stop), "F#5")
def fill(b, kind="tom"):
    """カッコいいフィル（アクセントのあるタムの下り）。4拍めだけ"""
    grid(FTM, b, "............x.x.", "E5"); grid(FSN, b, "............X..X", "A#4")


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


# ベース。r=根音 5=5度 7=7度 R=1オクターブ上 3=3度（同じ音の連打はしない）
BP_ = {"two": ("r-----r-5---r-.R", "r---5---r-----3-", "r-----r-R---5---", "r---r-..5---7-.."),
       "brk": ("r-------..r-....", "r-----5-..r-..7."),
       "half": ("r-----r---------", "r-----5---------"),
       "drop": ("r-.r-.r-.r-.r-r-", "r-.r-.5-.r-.R-r-")}
def bass(b, pat, stop=None):
    pat = cutp(pat, stop)
    ch = S.chords[b]; r = low(ch, "E1"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 5
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


def pch(b, pat="x--.x--.x---x---", center=64, short=None): _ch(PC, b, pat, center, 3, short=short)
def saw(b, pat="x..x..x...x..x..", center=67, short=0.45): _ch(SAW, b, pat, center, 4, short=short)
def swell(b): pass   # v2: 空気感のスーパーソウ（kfbSupersawWide）は外すと点が上がった（ドロップ 7.17 → 7.61）ので鳴らさない
def pad(b): PAD.bar(b, f"{N(low(S.chords[b], 'G3'))}:4")


def lh(b, pat="x.x.x.x.x.x.x.x.", stop=None):
    """左手の分散和音（8分で 根音・5度・オクターブ・3度…）"""
    pat = cutp(pat, stop)
    ch = S.chords[b]; r = low(ch, "C3"); root, third, fifth, sev, _ = G2.chord_info(simple(ch)); t3 = ((third - root) % 12) if third is not None else 5
    seq = [0, 7, 12, 12 + t3, 19, 12 + t3, 12, 7]; out = []; i = 0; k = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] != "x": L += 1
        if pat[i] == "x": out.append(f"{N(r + seq[k % 8])}:{L * 0.25:g}"); k += 1
        else: out.append(f"R:{L * 0.25:g}")
        i += L
    PL.bar(b, " ".join(out))


def run_up(b, at=3.0, beats=1.0, center=72, tr=None):
    """矩形波のプラックの駆け上がり（16分で和音を上へ。やまびこで最後の音が残る＝人間が気に入った「ピロピロピーン」）"""
    tr = tr or PLK; t = sorted(voice(S.chords[b], center, 4)); n = int(beats * 4); seq = (t + [x + 12 for x in t])[:n]
    out = ([f"R:{at:g}"] if at else []) + [f"{N(m)}:0.25" for m in seq[:-1]] + [f"{N(seq[-1])}:{0.25 + 4 - at - beats:g}"]
    tr.bar(b, " ".join(out))


def arp32(b, beats=4.0, center=72, tr=None, start=0.0):
    """ピアノの32分のアルペジオ（上がって下がる）"""
    tr = tr or PA; t = sorted(voice(S.chords[b], center, 4)); up = t + [x + 12 for x in t]; seq = up + up[::-1][1:-1]
    n = int(beats * 8); out = ([f"R:{start:g}"] if start else []) + [f"{N(seq[k % len(seq)])}:0.125" for k in range(n)]
    rest = 4 - start - beats
    if rest > 1e-6: out.append(f"R:{rest:g}")
    tr.bar(b, " ".join(out))


def tease(b, n):
    """つかみ: サビの旋律の「切れはし」をピアノの16分の分散和音でちらっと（2拍で切る）"""
    t = sorted(voice(S.chords[b], 74, 4)); seq = [t[3], t[2], t[1], t[2], t[3], t[2] + 12 if n % 2 else t[1], t[3], t[2]]
    PA.bar(b, " ".join(f"{N(m)}:0.25" for m in seq) + " R:2")


# ---- 旋律（1＝Bb3・oct=3。ピアノ＝ぼく、リード＝きみ） ----
INTRO = {4: "R:2 6:0.5 1':0.5 2':0.5 4':0.5", 5: "3':1.5 2':0.5 1':2", 6: "R:2 5:0.5 1':0.5 2':0.5 4':0.5", 7: "5':2 R:2"}
CHO = ["3':0.75 3':0.25 3':0.5 3':0.5 6':1.5 5':0.5", "4':0.75 3':0.75 2':0.5 1':1 R:1", "2':0.75 2':0.25 2':0.5 2':0.5 5':1.5 3':0.5", "2':1 1':1 6:1.5 R:0.5",
       "4':0.75 4':0.25 4':0.5 4':0.5 1'':1.5 7':0.5", "6':0.75 5':0.75 4':1.5 R:1", "3':0.5 3':0.25 3':0.25 3':0.5 5':0.5 1'':2", "2'':0.75 7':0.75 #5':2.5",
       "3':0.25 3':0.25 3':0.5 3':0.5 3':0.5 6':1 5':1", "4':0.75 3':0.75 2':0.5 1':2", "2':0.75 2':0.25 2':0.5 2':0.5 6':1.5 5':0.5", "3':1 2':0.5 1':2.5",
       "5':0.75 5':0.25 5':0.5 5':0.5 1'':1.5 7':0.5", "1'':1.5 b6':0.5 5':2", "3':0.75 2':0.75 1':2.5", "R:4"]        # 2026-11-29: はじめの形は旋律のリズムが過去の曲と 62% 同じだったので、付点とタイで書きかえた
HALF = ["3':1 3':1 6':2", "5':4", "2':1 2':1 5':2", "3':4", "4':1 4':1 1'':2", "6':4", "3':1 3':1 5':2", "#5':4", "5':1 5':1 1'':2", "b6':4", "5':4", "R:4"]
QUIET = ["R:2 6:1 1':1", "2':2 R:2", "R:2 5:1 6:1", "1':2 R:2", "R:2 4':1 3':1", "2':2 R:2", "R:2 b7:1 1':1", "4':2 R:2", "R:2 6:0.5 1':0.5 2':1", "3':2 R:2", "R:2 5':1 3':1", "2':2 R:2"]
SAY = [("P", "1':0.5 2':0.5 3':1 5':1 3':1"), ("P", "2':2 R:2"), ("L", "R:1 5:0.5 6:0.5 1':1 3':1"), ("L", "2':2 R:2"),
       ("P", "6':0.5 5':0.5 3':1 2':1 1':1"), ("P", "5:2 R:2"), ("L", "R:1 4':0.5 3':0.5 2':1 1':1"), ("L", "4':2 R:2"),
       ("B", "1':0.5 2':0.5 3':1 5':1 6':1"), ("B", "5':2 R:2"), ("B", "5':0.5 6':0.5 5':0.5 3':0.5 2':1 1':1"), ("B", "b6':2 R:2")]
BL = ["2':0.5 4':0.5 6':0.5 4':0.5 2':1 1':1", "3':0.5 5':0.5 6':0.5 5':0.5 3':1 2':1", "4':0.5 5':0.5 6':0.5 5':0.5 4':1 3':1", "5':0.5 6':0.5 1'':0.5 6':0.5 5':2",
      "4':1 2':1 1':2", "3':0.5 3':0.5 5':0.5 3':0.5 2':0.5 3':0.5 5':1", "6':0.5 6':0.5 5':0.5 3':0.5 2':1 1':1", "6:0.5 1':0.5 2':0.5 3':0.5 5':1 6':1",
      "5':0.5 5':0.5 6':0.5 5':0.5 3':0.5 2':0.5 3':1", "1'':0.5 6':0.5 5':0.5 6':0.5 5':2", "3':0.5 5':0.5 3':0.5 5':0.5 3':0.5 5':0.5 6':1", "1'':0.5 6':0.5 1'':0.5 6':0.5 5':0.5 6':0.5 1'':1",
      "2'':0.5 1'':0.5 6':0.5 4':0.5 2'':0.5 1'':0.5 6':0.5 4':0.5", "3'':0.5 1'':0.5 6':0.5 5':0.5 3':0.5 1'':0.5 6':0.5 5':0.5", "5':1 6':1 1'':1 2'':1", "1'':2 R:2"]
AEND = ["1'':0.5 7':0.5 6':0.5 5':0.5 3':2", "2'':0.5 1'':0.5 7':0.5 5':0.5 2':2", "7':0.5 6':0.5 5':0.5 3':0.5 2':2", "1'':0.5 7':0.5 6':0.5 5':0.5 6':2",
        "6':0.5 5':0.5 4':0.5 2':0.5 3':2", "5':0.5 4':0.5 2':0.5 1':0.5 2':2", "3':1 5':1 7':2", "1'':4", "1'':0.5 R:3.5"]


def split_owner(line, chunk, start_owner=0):
    """1小節の旋律を chunk 拍ごとに ぼく（ピアノ）／きみ（リード）で交代させる。返すのは (ピアノの行, リードの行)"""
    toks = line.split(); outs = ([], []); t = 0.0; cur = [0.0, 0.0]
    for tok in toks:
        a, L = tok.split(":"); L = float(L); who = (int(t // chunk) + start_owner) % 2
        if a != "R":
            if t - cur[who] > 1e-6: outs[who].append(f"R:{t - cur[who]:g}")
            outs[who].append(f"{a}:{L:g}"); cur[who] = t + L
        t += L
    for w in (0, 1):
        if 4 - cur[w] > 1e-6: outs[w].append(f"R:{4 - cur[w]:g}")
    return " ".join(outs[0]), " ".join(outs[1])


def put(tr, b, line, K=KB, oct=3):
    if line.replace("R:4", "").strip(): tr.bar(b, K.mel(line, oct=oct))


for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "つかみ":                                   # 手びょうし＋旋律の切れはし（4小節）→ 1拍の間 → リードの旋律・ベース・2ビート
        if i < 4:
            grid(FCL, b, ("....x.......x...", "....x.......x.x.", "....x..x....x...", "....x.......x...")[i], "B4"); tease(b, i)
            if i == 3: PLK.bar(b, "R:2 " + " ".join(f"{N(m)}:0.25" for m in sorted(voice(S.chords[b], 76, 4))[:3]) + f" {N(sorted(voice(S.chords[b], 76, 4))[3])}:1.25")
        else:
            put(LEAD, b, INTRO[i]); pch(b, "x-------x-------", 62); lh(b); bass(b, "r---------------" if i < 6 else BP_["two"][i % 4]); pad(b)
            if i >= 6: twobeat(b, i, stop=None if i < 7 else 3.0)
            if i == 4: fxh(b, 0, "rev", 1)
            if i == 6: fxh(b, 0, "riser", 8)
    elif n == "サビ1":                                  # 2ビート。旋律＝ピアノとリードが同時（ふたりで声をそろえる）。8小節めと16小節めの後半で止める（間）
        stop = 2.0 if i in (7, 15) else None
        twobeat(b, i, stop, heavy=i >= 8); bass(b, BP_["two"][i % 4], stop); pch(b, cutp("x--.x--.x---x---", stop), 64); lh(b, stop=stop); saw(b, cutp("x..x..x...x..x..", stop)); swell(b)
        put(LEAD, b, CHO[i]); put(PM, b, CHO[i], oct=3)
        if i in (3, 11): run_up(b, 3.0, 1.0)
        if i == 0: fxh(b, 0, "impact", 2)
        if i == 7: fxh(b, 2, "glitch", 0.5)
        if i == 14: fxh(b, 0, "rev", 4)
    elif n in ("ドロップ1", "ドロップ2"):                # Kawaii future bass のドロップ: 半分の速さ・スーパーソウの刻み・プラックの駆け上がり・リードの短い合いの手
        K = KC if n == "ドロップ2" else KB; stop = 2.0 if (n == "ドロップ1" and last) else None
        halftime(b, i, stop); bass(b, BP_["drop"][i % 2], stop); pch(b, cutp("x.xx.x.xx.x.x.x.", stop), 67, short=0.2); pad(b)   # v2: スーパーソウの刻み → ピアノの和音の刻み（スーパーソウを外すと 7.17 → 7.55）
        if not last and i % 2 == 1: run_up(b, 2.0, 2.0)
        if i % 2 == 0: put(LEAD, b, "R:0.5 3':0.25 R:0.25 3':0.25 R:0.25 6':0.5 R:2", K)
        if i == 0: fxh(b, 0, "impact", 2)
        if stop: fxh(b, 2, "glitch", 0.5)
    elif n == "ソロ":                                    # ピアノのソロ: 32分のアルペジオで上がって下がる（ぼくの「愛してる」の早口）。ドラムはリムとキックだけ
        arp32(b, 4.0 if i < 3 else 3.0, 70 + i * 2); grid(FK, b, "x.......x.......", "A4"); grid(FRM, b, "....x.......x...", "D#5"); bass(b, "r-------r-------")
        if last: fill(b)
    elif n == "サビ半":                                  # 半分の速さ: 長い音の旋律（リード）と、ピアノの左手と深いパッド
        stop = 2.0 if last else None
        halftime(b, i, stop); bass(b, BP_["half"][i % 2], stop); lh(b, "x...x...x...x...", stop); pad(b); swell(b)
        put(LEAD, b, HALF[i])
        if i in (3, 7): run_up(b, 3.0, 1.0)
        if i == 0: fxh(b, 0, "subdrop", 2)
    elif n == "静か":                                    # 静か: ピアノの旋律（ぼくのひとりごと）とパッド。後半からブレイクビート
        put(PM, b, QUIET[i]); pch(b, "x---------------", 60); pad(b)
        if i >= 4: bass(b, "r---------------")
        if i >= 6: brk(b, i)
        if last: fxh(b, 2, "rev", 2)
    elif n == "止まる":                                  # 照れて言葉が出ない1小節（何も鳴らさない）
        pass
    elif n == "言い合い":                                 # 2小節ずつ ぼく（ピアノ）→ きみ（リード）。最後の4小節はふたり同時
        who, line = SAY[i]
        if who in ("P", "B"): put(PM, b, line)
        if who in ("L", "B"): put(LEAD, b, line)
        twobeat(b, i, heavy=i >= 8); bass(b, BP_["two"][i % 4]); pch(b, "x--.x--.x---x---", 62); lh(b); swell(b) if i >= 8 else None
        if i == 0: fxh(b, 0, "impact", 2)
        if i in (3, 7): run_up(b, 3.0, 1.0)
    elif n == "B":                                       # 交代がだんだん速くなる: 1〜5小節は1小節ごと、6〜10小節は2拍ごと、11〜14小節は1拍ごと、最後の2小節はふたり同時（引き分け）
        line = BL[i]
        if i >= 14: put(PM, b, line); put(LEAD, b, line)
        else:
            chunk = 4.0 if i < 5 else (2.0 if i < 10 else 1.0)
            p_, l_ = split_owner(line, chunk, start_owner=(i % 2 if i < 5 else 0)); put(PM, b, p_); put(LEAD, b, l_)
        twobeat(b, i, stop=2.0 if last else None, heavy=i >= 10); bass(b, BP_["two"][i % 4], 2.0 if last else None); lh(b, stop=2.0 if last else None); saw(b, cutp("x..x..x...x..x..", 2.0 if last else None)) if i >= 10 else None
        if i == 9: fill(b)
        if last: fxh(b, 2, "glitch", 0.5)
    elif n == "立ち上げ":                                 # スネアが増え、ピアノの32分のアルペジオが上へ。G7 で ハ長調 へ
        s = ("x...x...x...x...", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxx", "xxxxxxxx........")[i]
        grid(FSN, b, s, "A#4"); grid(FK, b, "x...x...x...x..." if i < 5 else "x...x...........", "A4"); bass(b, "r-------r-------" if i < 5 else "r-------........")
        arp32(b, 4.0 if i < 5 else 2.0, 66 + i * 2); swell(b); pad(b)
        if i == 2: fxh(b, 0, "riser", 12)
    elif n == "A":                                       # 最後: 高い音から下りてくる旋律（ピアノとリード）→ 全員で1打して止まる
        if not last:
            twobeat(b, i, heavy=True); bass(b, BP_["two"][i % 4]); pch(b, "x--.x--.x---x---", 64); lh(b); saw(b); swell(b); pad(b)
            put(LEAD, b, AEND[i], KC); put(PM, b, AEND[i], KC)
            if i == 0: fxh(b, 0, "impact", 2)
            if i == 7: fxh(b, 2, "rev", 2)
        else:
            put(LEAD, b, AEND[i], KC); put(PM, b, AEND[i], KC); pch(b, "x...............", 64, short=0.5); saw(b, "x...............", short=0.5)
            bass(b, "r..............."); grid(FK, b, "X...............", "A4"); grid(FK2, b, "x...............", "F#5"); grid(FCL, b, "x...............", "B4"); fxh(b, 0, "impact", 2)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{min(L_, 4 - at):g}"); t = at + min(L_, 4 - at)
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: Kawaii future bass × J-POP のインスト（160・変ロ長調→ハ長調・約2分45秒）。愛してるゲーム: ピアノ（ぼく）とリード（きみ）が旋律を言い合い、"
          "交代がだんだん速くなって最後は同時に。手びょうしと旋律の切れはしで始まり、1小節の「止まる」をはさみ、全員の1打で終わる。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path)
js["parts"] = [p_ for p_ in js["parts"] if p_.get("notes", "").replace("R:", "").strip() and not p_.get("role", "").startswith("歌の役")]
js["grooveFeel"] = "pushed"; js["human"] = 0.3
save(path, js)
# v3: 測ると、ドロップが前のサビより 1.5〜2 LU 小さかった（半分の速さで音が少ない）。ドロップを山にする（ほかはそのまま）
final_gain(path, {"ドロップ1": 1.5, "ドロップ2": 2.0, "A": 0.5})
