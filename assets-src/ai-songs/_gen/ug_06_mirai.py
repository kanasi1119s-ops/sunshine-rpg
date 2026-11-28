# UG 06「ミライ行きのスタートダッシュ」（仮）Start Dash to the Future — インスト。テクノポップ × Kawaii future bass。4分の4・170・変ホ長調。
#
# 2026-11-28 人間「BGM系は3分以内の曲にしましょうか」→ 3分以内（v2 で 152 → 126小節）。
# 2026-11-28 人間「次、kawaiifutureベースで間を主体にしたテクノポップ。緩急が大事。疾走感もありゆっくりな感じもあり。キーボード、シンセの重ねがけ、FX、
#   コンセプトは挑戦する先に未来が待っている。テンポ170」「手数多めの部分や少なめの部分あり」
#   楽器: キーボード（ピアノ・オルゴール）／シンセ（低い正弦波のベース・スーパーソウ・ふくらむスーパーソウ・矩形波のリード・ベル・矩形波のプラック）／効果音（kawaiiFx）。
#   v4: 重ね3（グロッケン）は、サビ3だけに（ほかで重ねると点が 6.9 に下がった）。
#   シンセの重ねがけ: 旋律を「声のようなリード＋ピアノ＋1オクターブ上の小さなグロッケン」で重ね、場面が進むほど重ねる数を増やす（layer 1〜3）。
#   kfbSawStab は使わない。歌の指定がないのでインスト。
# 形: くじ（tools/vt3/form_dice.py --skeleton 8417 215 170 --min-chorus 3 --not-start ベース/ピアノ/静か/ドラム/フック --not-groove tresillo/twobeat）。
#   始まり＝最後のサビの旋律を別の楽器（オルゴールとピアノ）で先に聞かせる／終わり＝全員で1打して止まる／リズム＝ブレイクビート（疾走）・あと乗りのハーフ（ゆっくり）
# 手数: 早口・ドロップ・フック2 は手数多め（16分の刻みとプラックの細かい分散）／静か・B・A2の前半は手数少なめ（1小節に数音だけ。間を主体に）。
# 物語: こわくても一歩をふみ出す。走って、つまずいて、ひと息ついて、また走る。その先で、未来が手をふって待っている。
# この曲だけのもの: 小節ごとに全音ずつ上がる「階段」の和音（Cm → Dm → E♭ → F → G…。挑戦の坂）。立ち上げとサビ3の頭で鳴る。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("42", "mirai", "ミライ行きのスタートダッシュ（仮）", "Start Dash to the Future", 170, 4, "Eb", "major", "インスト（テクノポップ × Kawaii future bass）")
S.flags = S.flags + " --space room --space-wet 0.1"
KE = Key("Eb", "major")
CH = ["Abmaj7", "Bb/Ab", "Gm7", "Cm7", "Fm7", "Bb", "Ebmaj7", "Eb"]                       # サビ: IV → V/IV → iii → vi ／ ii → V → I
CHE = ["Cm7", "Cm7", "Abmaj7", "Abmaj7", "Ebmaj7", "Ebmaj7", "Bbsus4", "Bb", "Fm7", "Gm7", "Abmaj7", "Bb"]
STAIR = ["Cm7", "Dm7", "Ebmaj7", "Fm7", "Gm7", "Abmaj7", "Bbsus4", "Bb"]                 # 階段（だいたい全音ずつ上がる）
AA = ["Eb", "Eb", "Bb/D", "Bb/D", "Cm7", "Cm7", "Abmaj7", "Bb"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("予告", 8, "intro", ["Cm7", "Dm7", "Ebmaj7", "Fm7", "Gm7", "Abmaj7", "Eb", "Bb"])   # 最後のサビ（サビ3）と同じ階段の和音
scene("サビ別", 8, "chorus", CHE[:8])
scene("止1", 2, "bridge", ["Bb", "Bb"])
scene("A1", 4, "verse", ["Eb", "Bb/D", "Cm7", "Bb"])
scene("静か1", 4, "bridge", ["Abmaj7", "Abmaj7", "Fm7", "Bb"])
scene("立ち上げ", 8, "pre", STAIR)
scene("フック1", 8, "break", CH)
scene("B", 8, "bridge", ["Abmaj7", "Abmaj7", "Gm7", "Gm7", "Fm7", "Fm7", "Bbsus4", "Bb"])
scene("早口", 8, "verse", AA)
scene("静か2", 8, "bridge", ["Cm7", "Cm7", "Abmaj7", "Abmaj7", "Ebmaj7", "Ebmaj7", "Bbsus4", "Bb"])
scene("A2", 12, "verse", AA[:4] + ["Cm7", "Gm7", "Abmaj7", "Ebmaj7", "Fm7", "Gm7", "Abmaj7", "Bb"])
scene("フック2", 6, "break", CH[:6])
scene("ドロップ", 6, "break", ["Cm7", "Cm7", "Abmaj7", "Abmaj7", "Bb", "Bb"])
scene("サビ1", 10, "chorus", CH + ["Bbsus4", "Bb"])
scene("止2", 1, "bridge", ["Bb"])
scene("サビ2", 10, "chorus", CH + ["Bbsus4", "Bb"])
scene("静か3", 8, "bridge", ["Abmaj7", "Abmaj7", "Gm7", "Gm7", "Fm7", "Fm7", "Bbsus4", "Bb"])
scene("サビ3", 7, "outro", ["Cm7", "Dm7", "Ebmaj7", "Fm7", "Gm7", "Abmaj7", "Eb"])          # 未来: 階段を上りきって、主和音で1打
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

PN = [S.track(f"ピアノ（和音）{i + 1}", "piano", volume=0.14, pan=(-0.2, 0.0, 0.16, -0.08)[i], reverb=0.14) for i in range(4)]
PM = S.track("ピアノ（右手の旋律）", "piano", volume=0.26, pan=-0.12, reverb=0.16)
MB = S.track("オルゴール", "keys", patch="kfbMusicBox", volume=0.07, pan=0.3, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.21, pan=0, gainDb=-5)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.065, pan=(-0.4, 0.4, -0.15, 0.15)[i], reverb=0.2, duck=0.4,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}]) for i in range(4)]
SWL = S.track("ふくらむスーパーソウ", "pad", patch="kfbSupersawSwell", volume=0.06, pan=0, reverb=0.35, fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}])
# v6（人間「このピコ系の音別のにしよう」）: 矩形波のリードとプラックをやめ、声のようなリードと、やわらかいデジタルのプラックに
LEAD = S.track("声のようなリード（重ね1）", "lead", patch="kfbFormantLead", volume=0.13, mono=True, pan=0.05, reverb=0.24, fx=[{"type": "filter", "kind": "lowpass", "freq": 3800, "q": 0.6}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}])
BEL = S.track("グロッケン（重ね3）", "keys", patch="kfbGlocken", volume=0.025, pan=-0.2, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}])
SAWL = S.track("オルゴール（重ね3・1オクターブ上）", "keys", patch="kfbMusicBox", volume=0.045, pan=0.2, reverb=0.3, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}])   # v2: kfbBrightBells とモノのスーパーソウは、入れるだけで点が 7.4 → 6.9 に下がった
PLK = S.track("デジタルのプラック", "lead", patch="modernPluck", volume=0.085, pan=0.28, reverb=0.25, fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
FX = lambda name, v, pn=0.0: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=0.08, modulate=False)
FK, FSN, FCL, FH, FOH = FX("効果音（キック）", 0.13), FX("効果音（スネア）", 0.07, 0.04), FX("効果音（手びょうし）", 0.06, -0.06), FX("効果音（ハイハット）", 0.03, 0.22), FX("効果音（開いたハイハット）", 0.035, -0.22)
FKW = FX("効果音（かわいい音: あわ・きらめき・レーザー）", 0.045, 0.3)
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


# 疾走: ブレイクビート／ゆっくり: あと乗りのハーフ
BKK = ("X.X.......X.....", "X.........X..X..", "X.X.......X.X...", "X.....X...X.....")
BKS = ("....X.......X...", "....X.......X...", "....X.......X...", "....X.......X.X.")   # v3: ゴーストを外した（ブレイクの細かいスネアで点が下がった）
def run(b, i, many=False, stop=None, clap=False):
    k, s, h = BKK[i % 4], BKS[i % 4], ("x.x.x.x.x.x.x.x." if not many else "x.xxx.xxx.xxx.xx")
    if stop is not None: k, s, h = cutp(k, stop), cutp(s, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FH, b, h, "C#5")
    if clap: grid(FCL, b, cutp("....X.......X...", stop) if stop else "....X.......X...", "B4")
    if i % 4 == 3 and stop is None: grid(FOH, b, "..............x.", "D5")
def slow(b, i, hat=True):
    grid(FK, b, ("X.........X.....", "X......X..X.....")[i % 2], "A4"); grid(FSN, b, "........X.......", "A#4")
    if hat: grid(FH, b, "x...x...x...x...", "C#5")
def kawaii(b, pat, key="C4"): grid(FKW, b, pat, key)


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


BR = ("r.r.......r..r..", "r.........r..5..", "r.r.......r.R...", "r.....r...r..R..")                # ブレイクビートのキックにそろえる
BM = ("r.rRr.rRr.rRr.rR", "r.rRr.r5r.rRr.rR")                                                    # 手数多め（16分）
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


def keys(b, pat="x..x......x.....", center=62): _ch(PN, b, pat, center, 4, short=0.5)
def saw(b, pat="x..x..x...x..x..", center=66, short=0.5): _ch(SAW, b, pat, center, 4, short=short)


def one(tr, b, pat, center=79, k=0):
    t = sorted(voice(S.chords[b], center, 4)); out = []; i = 0; c = k
    while i < 16:
        if pat[i] == "x": out.append(f"{N(t[c % 4])}:0.25"); c += 1; i += 1
        else:
            L = 1
            while i + L < 16 and pat[i + L] != "x": L += 1
            out.append(f"R:{L * 0.25:g}"); i += L
    tr.bar(b, " ".join(out))


def theme(name, lines, layer=1, start=0, trs=None):
    """旋律を重ねがけで: layer 1＝矩形波のリード／2＝＋ベル／3＝＋1オクターブ上のスーパーソウ。trs で楽器を指定（予告のオルゴールなど）"""
    bars = S.sc(name)[start:]; ls = [x.strip() for x in " | ".join(lines).split("|")]; assert len(ls) <= len(bars), (name, len(ls), len(bars))
    for b, l in zip(bars, ls):
        assert abs(sum(float(y.split(":")[1]) for y in l.split()) - 4) < 1e-6, (name, l)
        if l == "R:4": continue
        for tr, up in (trs or [(LEAD, 1), (PM, 1), (BEL, 2)][:layer]): tr.bar(b, KE.mel(l, oct=3 + up))   # v3: 重ね2＝ピアノ、重ね3＝小さなグロッケン（オルゴールの1オクターブ上の重ねは外した）


# ---- 旋律（1＝E♭4）----
FINAL = ["1':0.75 2':0.75 3':1 R:1.5", "2':0.75 3':0.75 4':1 R:1.5", "3':0.75 4':0.75 5':1 R:1.5", "4':0.75 5':0.75 6':1 R:1.5", "5':0.75 6':0.75 7':1 R:1.5", "6':0.75 7':0.75 1'':1 R:1.5", "1'':4"]   # サビ3（1小節の短い句をたたみかける。付点で前へ）
PRE = ["R:2 5:0.5 1':0.5 3':1", "2':2 R:2", "R:2 3:0.5 5:0.5 1':1", "7:2 R:2", "R:2 4:0.5 6:0.5 1':1", "6:2 R:2", "R:2 5:0.5 7:0.5 2':1", "3':2 R:2"]   # 予告（サビの旋律をゆっくり）
SBE = ["R:3 5:0.5 6:0.5", "1':0.75 3':0.75 5':0.5 3':2", "R:3 3:0.5 5:0.5", "6:0.75 1':0.75 3':0.5 1':2", "R:3 2:0.5 3:0.5", "5:0.75 7:0.75 2':0.5 1':2",          # 1拍早く食って入る
       "R:3 3:0.5 4:0.5", "5:0.75 4:0.75 2:0.5 5:2", "R:3 5:0.5 4:0.5", "6:0.75 1':0.75 2':0.5 3':2", "R:3 5':0.5 4':0.5", "3':0.75 2':0.75 1':0.5 2':2"]
A1L = ["R:3 5:0.5 1':0.5", "3':1.5 2':0.5 1':1 R:1", "R:3 6:0.5 7:0.5", "5:2 R:2"]
Q1 = ["R:2 3':1 1':1", "R:4", "R:2 6:1 4:1", "5:2 R:2"]                                                                                     # 静か1（小節のまん中から。手数少なめ）
HOOK = ["R:0.5 5:0.5 R:0.5 1':0.5 3':0.75 2':0.75 1':0.5", "R:0.5 5:0.5 R:0.5 2':0.5 4':0.75 3':0.75 2':0.5", "R:0.5 3':0.5 R:0.5 5':0.5 6':1 5':1", "3':2 R:2"]
BL = ["3':4", "1':2 7:2", "2':4", "R:4", "6:4", "5:2 4:2", "5:4", "R:4", "3':4", "4':2 3':2", "2':4", "R:4"]                               # 4小節のばす長い句（手数少なめ）
FL = ["5:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "1':0.5 6:0.5 5:1 R:2", "R:4",                                                               # 早口: 3小節の句（手数多め）
      "6:0.5 7:0.5 2':0.5 3':0.5 4':1 3':1", "2':0.5 7:0.5 5:1 R:2", "R:4",
      "5:0.5 6:0.5 1':0.5 2':0.5 3':1 5':1", "3':0.5 2':0.5 1':1 R:2", "R:4",
      "4:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "1':0.5 7:0.5 5:1 R:2", "R:4",
      "5:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "1':0.5 6:0.5 5:1 R:2", "R:4", "R:4"]
Q2 = ["R:4", "R:1 5:1 1':2", "R:4", "R:4", "R:1 3:1 7:2", "R:4", "R:4", "R:1 6:1 2':2", "R:4", "R:4", "R:1 4:1 1':2", "R:4"]               # 静か2: 休みから入って最後をのばす（とても少なく）
A2L = ["5':1 4':1 3':2", "R:4", "4':1 3':1 1':2", "R:4", "3':1 2':1 7:2", "R:4", "4':1 3':1 2':2", "R:4",                                  # 高い音から下りてくる（前半はゆっくり・まばら）
       "5':0.5 4':0.5 3':0.5 2':0.5 1':1 5:1", "3':0.5 2':0.5 1':0.5 7:0.5 5:2", "4':0.5 3':0.5 1':0.5 7:0.5 6:1 1':1", "5':0.5 4':0.5 3':0.5 1':0.5 3':2",
       "6':0.5 5':0.5 4':0.5 3':0.5 1':1 6:1", "5':0.5 4':0.5 3':0.5 2':0.5 7:2", "4':0.5 3':0.5 1':0.5 6:0.5 4':1 3':1", "2':4"]
S3 = ["R:1 3:0.75 6:0.75 1':1.5", "7:2 5:2", "R:1 4:0.75 6:0.75 1':1.5", "R:1 5:0.75 7:0.75 3':1.5", "2':2 7:2", "R:1 6:0.75 1':0.75 4':1.5", "R:1 3':0.75 2':0.75 1':1.5", "5:2 R:2", "R:2 5:1 7:1", "1':4"]   # 3小節の句
SR = ["3':0.25 3':0.25 3':0.25 R:0.25 6':1 5':2", "R:4", "1':0.25 1':0.25 1':0.25 R:0.25 5':1 3':2", "R:4", "6:0.25 6:0.25 6:0.25 R:0.25 4':1 3':2", "R:4",   # 連打して跳ぶ
      "1':0.25 1':0.25 1':0.25 R:0.25 6':1 5':2", "R:4", "4':0.25 4':0.25 4':0.25 R:0.25 2':1 1':2", "5:4"]
Q3 = ["5':2 3':2", "R:4", "4':2 2':2", "R:4", "3':2 1':2", "R:4", "2':2 7:2", "R:4"]                                                        # 高い音から下りてくる（少なめ）

theme("予告", FINAL + ["R:4"], trs=[(MB, 2), (PM, 1)])                                 # 最後のサビの旋律を、オルゴールとピアノで先に; theme("サビ別", SBE[:8], 1); theme("A1", A1L, 1); theme("静か1", Q1, trs=[(PM, 1)])
theme("フック1", HOOK * 2, 2); theme("B", BL[:8], trs=[(BEL, 2), (PM, 1)]); theme("早口", FL[:8], 2); theme("静か2", Q2[:8], trs=[(PM, 1), (MB, 2)])
theme("A2", A2L[:4] + A2L[8:], 2); theme("フック2", (HOOK * 2)[:6], 2); theme("サビ1", S3, 2); theme("サビ2", SR, 2); theme("静か3", Q3, trs=[(MB, 2)]); theme("サビ3", FINAL, 3)

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "予告":                                                      # 最後のサビの旋律を、オルゴールとピアノだけで（ゆっくり・間をあけて）
        keys(b, "x...............", 60)
        if i >= 4: SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4")
        if last: fxh(b, 0, "riser", 4)
    elif n in ("サビ別", "サビ1", "サビ2", "フック1", "フック2"):         # 疾走（ブレイクビート）。4小節ごとの最後は2拍半で止める
        stop = 2.5 if i % 4 == 3 else None; many = n == "フック2"
        run(b, i, many=many, stop=stop, clap=True); bass(b, cutp((BM if many else BR)[i % (2 if many else 4)], stop) if stop else (BM if many else BR)[i % (2 if many else 4)])
        saw(b, cutp("x..x..x...x..x..", stop) if stop else "x..x..x...x..x.."); keys(b, cutp("x..x......x.....", stop) if stop else "x..x......x.....")
        if many: one(PLK, b, "x.xxx.xxx.xxx.xx", 76, i)
        elif i % 2: one(PLK, b, "..x...x.......x.", 76, i)
        if i == 0: fxh(b, 0, "impact", 2)
        if stop: kawaii(b, "............x...", "A5")
        if last and n in ("サビ別",): fxh(b, 0, "down", 4)
    elif n in ("止1", "止2"):
        kawaii(b, "............x...", "D4")
        if last: fxh(b, 0, "rev", 4)
    elif n == "A1":
        run(b, i); bass(b, BR[i % 4]); keys(b)
        if last: fxh(b, 0, "down", 4)
    elif n in ("静か1", "静か3"):                                        # ゆっくり・手数少なめ
        keys(b, "x---------------", 60); SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4") if i % 2 == 0 else None
        if n == "静か3" and i >= 4: slow(b, i, hat=False)
        if last: fxh(b, 0, "riser", 4)
    elif n == "立ち上げ":                                                # 階段の和音（全音ずつ上がる）。ゆっくり → 疾走へ
        if i < 4: slow(b, i)
        else: run(b, i, many=i >= 6)
        saw(b, "x---------------" if i < 4 else "x.x.x.x.x.x.x.x.", short=4 if i < 4 else 0.25); bass(b, "r..............." if i < 4 else BR[i % 4])
        if i == 4: fxh(b, 0, "riser", 4)
        if last: kawaii(b, "x.x.x.x.xxxxxxxx", "D4")
    elif n == "B":                                                       # ゆっくり（ハーフ）・手数少なめ
        slow(b, i); bass(b, "r.........r....."); keys(b, "x.........x.....", 62)
        if i % 4 == 2: one(MB, b, "..........x.....", 84, i)
        if last: fxh(b, 0, "riser", 4)
    elif n == "早口":                                                    # 疾走・手数多め
        run(b, i, many=True); bass(b, BM[i % 2]); keys(b, "x.xx..x.x.xx..x."); one(PLK, b, "x.x.x.x.x.x.x.x.", 76, i)
        if last: fxh(b, 0, "down", 4)
    elif n == "静か2":                                                   # とても少ない
        keys(b, "x---------------" if i % 2 == 0 else "................", 60)
        if last: fxh(b, 0, "riser", 4)
    elif n == "A2":                                                      # 前半はゆっくり・まばら → 後半は疾走・手数多め
        if i < 4: slow(b, i, hat=i >= 2); bass(b, "r.........r....."); keys(b, "x.........x.....")
        else: run(b, i, many=i >= 8); bass(b, BR[i % 4]); keys(b, "x..x..x...x..x.."); one(PLK, b, "x.x.x.x.x.x.x.x." if i >= 8 else "..x...x...x...x.", 76, i)
        if i == 4: fxh(b, 0, "impact", 2)
        if last: fxh(b, 0, "riser", 4)
    elif n == "ドロップ":                                                # 手数多め
        run(b, i, many=True, clap=True); bass(b, BM[i % 2]); saw(b, "xxx.xxx.xxx.x.x.", short=0.25); one(PLK, b, "xxxxxxxxxxxxxxxx", 76, i)
        if i == 0: fxh(b, 0, "subdrop", 4)
        if last: fxh(b, 0, "riser", 4)
    elif n == "サビ3":                                                   # 未来: 階段を上って、最後に全員で1打
        if not last:
            run(b, i, many=True, clap=True); bass(b, BM[i % 2]); saw(b); keys(b); one(PLK, b, "x.x.x.x.x.x.x.x.", 76, i)
            if i == 0: fxh(b, 0, "impact", 2)
        else:
            grid(FK, b, "X...............", "A4"); grid(FCL, b, "X...............", "B4"); _ch(PN, b, "x---------------", 62, 4); _ch(SAW, b, "x-------........", 66, 4)
            SUB.bar(b, f"{N(low(S.chords[b], 'E1'))}:2 R:2"); fxh(b, 0, "impact", 2)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: テクノポップ × Kawaii future bass のインスト（170・変ホ長調）。こわくても一歩をふみ出し、走って、ひと息ついて、また走る。その先で未来が待っている。"
          "疾走（ブレイクビート）とゆっくり（ハーフ）、手数多めと少なめが交互に来る。旋律はシンセの重ねがけ。形は、くじ（form_dice.py・種 8417）で決めた。"
          "最後のサビの旋律を先に聞かせて始まり、全員で1打して止まる。自作")
V = Voice(S, vol=0.0, delay=0.0, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
js = load(path); js["parts"] = [p_ for p_ in js["parts"] if p_.get("patch") != "kfbSineLead" and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "pushed"; js["human"] = 0.3
save(path, js)
