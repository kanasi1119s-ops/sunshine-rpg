# UG 08「ゼロ番地のラブコール」（仮）Love Call from Address Zero — テトの歌（クリアの声）。Kawaii future bass × テクノポップ × ヒップホップのダンス。
#   4分の4・180・ハ短調 → 変ホ長調。124小節・約2分45秒（Instagram 用に3分以内）。
#
# 2026-11-28 人間「kawaiifutureベースでインスタ用のボカロ曲を作ります。kawaiifutureベースでテクノポップとヒップホップにダンスを融合して世界を感じる空間系に。
#   キーボード、シンセ、FXを入れて。深みをだして。テンポは180。間と緩急を入れ、交互の刻みも入れましょう。コンセプトは世界の中心で愛を叫ぶ」
#   楽器: キーボード（エレピ kfbGlassEp・ピアノ）／シンセ（低い正弦波のベース kfbSub・スーパーソウ・ふくらむスーパーソウ・きらめくパッド・矩形波のプラック・
#         明るく抜けるリード surgeTropics＝歌のないフックだけ）／FX（kawaiiFx の電子ドラム・上がる音・逆回しのシンバル・当たる音・低く落ちる音・グリッチ）。
#   使わない: kfbSawStab・kfbBrightBells・モノのスーパーソウのリード・kfbDreamLead（音の頭が持ち上がる）・歌をなぞるリード（歌の版ではパートごと外す）。
# 形: くじ（tools/vt3/form_dice.py --skeleton 1129 170 180 --min-chorus 2 --not-start サビ --not-groove laid）。始まり＝伴奏なしの歌1句。終わり＝歌の最後の音で後奏なし。
#   リズム＝4分キックのたてノリ（主・サビとドロップ）／ブレイクビート（語りとフック＝ヒップホップ）／まっすぐ4つ打ち（静かな A）。
# 物語: 地球のまん中（ゼロ番地）で、ひとりが呼びかける。声が空へ広がり、街を見下ろし、夜の底で数え、最後に「ここがまん中になる」と気づいて、
#   いちばん大きな声で言い切ったところで世界が止まる。
# この曲だけのもの: 伴奏なしの1句で始まり、歌の最後の音で全部が同時に止まる／Abmaj7 → Abm6 → Bb7sus4 → Ebmaj9（最後だけ iv6 を通る）。
from vocalo_lib import *
import gtr2_lib as G2
import re as _re

S = Song("44", "zero", "ゼロ番地のラブコール（仮）", "Love Call from Address Zero", 180, 4, "Eb", "major", "ボカロ（Kawaii future bass × テクノポップ × ヒップホップ）")
S.flags = S.flags + " --space hall --space-wet 0.16"
KG = Key("Eb", "major")
CH = ["Abmaj7", "Bb", "Gm7", "Cm9", "Gbmaj7", "Fm9", "Bb7sus4", "Ebmaj9"]
RAP = ["Cm9", "Cm9", "Abmaj7", "Bbsus4"]
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("呼びかけ", 8, "verse", ["Cm9", "Cm9", "Abmaj7", "Abmaj7", "Fm9", "Fm9", "Gsus4", "G7"])
scene("サビ1", 8, "chorus", CH)
scene("立ち上げ", 8, "pre", ["Abmaj7", "Abmaj7", "Bb", "Bb", "Cm9", "Cm9", "Dbmaj7", "Bbsus4"])
scene("サビ2", 16, "chorus", CH + CH)
scene("フック1", 4, "break", RAP)
scene("語り1", 4, "verse", RAP)
scene("フック2", 4, "break", RAP)
scene("語り2", 8, "verse", RAP + RAP)
scene("サビ半", 8, "chorus", CH)
scene("A", 16, "verse", ["Cm9", "Abmaj7", "Gm7", "Fm9", "Cm9", "Abmaj7", "Dbmaj7", "Bbsus4", "Cm9", "Abmaj7", "Gm7", "Fm9", "Gbmaj7", "Abmaj7", "Bbsus4", "Bb7"])
scene("フック3", 10, "break", RAP + RAP + ["Bbsus4", "Bb7"])
scene("ドロップ", 10, "drop", ["Abmaj7", "Bb", "Gm7", "Cm9", "Abmaj7", "Bb", "Gm7", "Cm9", "Bbsus4", "Bb7"])
scene("サビ別", 8, "chorus", ["Fm9", "Gm7", "Abmaj7", "Bbsus4", "Cm9", "Gbmaj7", "Abmaj7", "Bb7sus4"])
scene("まん中", 12, "outro", ["Ebmaj9", "Gm7", "Abmaj7", "Cm9", "Bbsus4", "Gbmaj7", "Fm9", "Gm7", "Abmaj7", "Abm6", "Bb7sus4", "Ebmaj9"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}

LP = lambda f: {"type": "filter", "kind": "lowpass", "freq": f, "q": 0.6}
EPC = [S.track(f"エレピ（和音）{i + 1}", "keys", patch="kfbGlassEp", volume=0.09, pan=(-0.24, 0.0, 0.2, -0.1)[i], reverb=0.22, fx=[LP(6200)]) for i in range(4)]
PNO = S.track("ピアノ（短く切る和音の刻み）", "piano", volume=0.11, pan=0.12, reverb=0.16)
PLK = S.track("矩形波のプラック（交互の刻み）", "keys", patch="kfbSquarePluck", volume=0.05, pan=0.3, reverb=0.25, fx=[LP(5200), {"type": "delay", "beats": 0.75, "mix": 0.2, "feedback": 0.32}])
EPX = S.track("エレピ（交互の刻み）", "keys", patch="kfbGlassEp", volume=0.11, pan=-0.3, reverb=0.2, fx=[LP(6500)])
SUB = S.track("シンセのベース（低い正弦波）", "bass", patch="kfbSub", volume=0.22, pan=0, gainDb=-5)
SAW = [S.track(f"スーパーソウの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.05, pan=(-0.45, 0.45, -0.18, 0.18)[i], reverb=0.26, duck=0.45, fx=[LP(5600)]) for i in range(4)]
SWL = S.track("ふくらむスーパーソウ", "pad", patch="kfbSupersawSwell", volume=0.05, pan=0, reverb=0.4, fx=[LP(6000)])
SPD = S.track("きらめくパッド（空間）", "pad", patch="kfbSparklePad", volume=0.045, pan=0, reverb=0.5, fx=[LP(7000)])
LEAD = S.track("明るく抜けるリード（歌のないフック）", "lead", patch="surgeTropics", volume=0.1, mono=True, pan=0.08, reverb=0.3,
               fx=[LP(5200), {"type": "delay", "beats": 0.75, "mix": 0.16, "feedback": 0.3}])
FX = lambda name, v, pn=0.0, rv=0.08: S.track(name, "guitar", patch="kawaiiFx", volume=v, pan=pn, reverb=rv, modulate=False)
FK, FK2, FSN, FCL, FH, FOH, FRM = (FX("効果音（キック）", 0.14), FX("効果音（重いキック）", 0.08), FX("効果音（スネア）", 0.08, 0.04), FX("効果音（手びょうし）", 0.06, -0.06),
                                   FX("効果音（ハイハット）", 0.035, 0.22), FX("効果音（開いたハイハット）", 0.032, -0.22), FX("効果音（リム）", 0.05, 0.15))
FXT = S.track("効果音（上がる音・下がる音・逆回しのシンバル・当たる音・低く落ちる音・グリッチ）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.35, modulate=False)
V = Voice(S, vol=0.12, delay=0.75, bright=0.0, patch="surgeTropics", low=False); LY = Lyrics(S)        # 歌なし版の旋律だけ。歌の版ではパートごと外す（音量0は0.2で鳴るため）
N = lambda m: nm(m); FXH = {}
FXK = {"riser": "F#4", "down": "G4", "rev": "G#4", "impact": "G5", "subdrop": "G#5", "glitch": "D#6", "spark": "D4"}
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


# ---- ドラム ----
def pogo(b, i, stop=None, heavy=False):
    """4分キックのたてノリ: キック4つ・手びょうし2と4・開いたハイハットは裏・閉じたハイハットは16分のすき間に少し"""
    k, c, oh, h = "x...x...x...x...", "....x.......x...", "..x...x...x...x.", ("x.x.....x.x.....", "x.......x.x...x.")[i % 2]
    if i % 4 == 3: k, c = "x...x...x...x.x.", "....x.......x.xx"
    if stop is not None: k, c, oh, h = cutp(k, stop), cutp(c, stop), cutp(oh, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FCL, b, c, "B4"); grid(FSN, b, c, "A#4"); grid(FOH, b, oh, "D5"); grid(FH, b, h, "C#5")
    if heavy: grid(FK2, b, cutp("x.......x.......", stop) if stop is not None else "x.......x.......", "F#5")
BK_ = ("x.........x.....", "x.....x...x.....", "x.........x..x..", "x.x.......x.....")
def brk(b, i, stop=None):
    """ブレイクビート（ヒップホップ）: キックは1と3のうら、スネアは2拍めのうらと4（半分の速さに感じる）・ゴーストのリム"""
    k = BK_[i % 4]; s = "........X......."; r = ("....x.......x...", "......x.....x..x")[i % 2]; h = "x.x.x.x.x.x.x.x."
    if stop is not None: k, s, r, h = cutp(k, stop), cutp(s, stop), cutp(r, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FRM, b, r, "D#5"); grid(FH, b, h, "C#5")
def four(b, i, hats=True):
    grid(FK, b, "x...x...x...x...", "A4")
    if hats: grid(FOH, b, "..x...x...x...x.", "D5")
def build(b, i, n):
    """立ち上げのスネア: 4分 → 8分 → 16分"""
    s = ("x...x...x...x...", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx")[min(2, n)]
    grid(FSN, b, s, "A#4"); grid(FK, b, "x...x...x...x...", "A4")
def halftime(b, i, stop=None):
    k, s, h = "x.....x.........", "........x.......", "x...x...x...x..."
    if stop is not None: k, s, h = cutp(k, stop), cutp(s, stop), cutp(h, stop)
    grid(FK, b, k, "A4"); grid(FSN, b, s, "A#4"); grid(FCL, b, s, "B4"); grid(FH, b, h, "C#5")


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


# ベース（キックにそろえる・同じ音の連打はしない）。r=根音 5=5度 7=7度 R=1オクターブ上 3=3度
BP_ = {"pogo": ("r-..r-.5r-..r-.R", "r-..r-..5-..r-.3", "r-..r-.5r-..7-..", "r-..r-..R-..5-.."),
       "brk": ("r-------..r-....", "r-----5-..r-....", "r-------..r-..7.", "r-----..5---r..."),
       "half": ("r-----r---------", "r-----5---------", "r-----r-------7-", "r---------5-----")}
def bass(b, pat, stop=None):
    if stop is not None: pat = cutp(pat, stop)
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


def ep(b, pat="x---------x-----", center=63, short=None): _ch(EPC, b, pat, center, 4, short=short)
def saw(b, pat="x..x..x...x..x..", center=67, short=0.45): _ch(SAW, b, pat, center, 4, short=short)
def swell(b): SWL.bar(b, f"{N(low(S.chords[b], 'E3') + 12)}:4")
def pad(b): SPD.bar(b, f"{N(low(S.chords[b], 'G4'))}:4")


def alt(b, pat, rot=(EPX, PLK, PNO), center=72, step=0.25, stop=None):
    """交互の刻み: 16分（step=0.125 なら32分）の x を、エレピ → プラック → ピアノ の順に回す。音は和音の音を上から下へ順に"""
    if stop is not None: pat = cutp(pat, stop) if step == 0.25 else pat[:int(stop / step)] + "." * (len(pat) - int(stop / step))
    tones = sorted(voice(S.chords[b], center, 4), reverse=True); n = len(pat)
    outs = {id(t): [] for t in rot}; tm = {id(t): 0.0 for t in rot}; k = 0
    for s in range(n):
        if pat[s] != "x": continue
        tr = rot[k % len(rot)]; at = s * step
        if at - tm[id(tr)] > 1e-6: outs[id(tr)].append(f"R:{at - tm[id(tr)]:g}")
        outs[id(tr)].append(f"{N(tones[k % 4])}:{step * (1.6 if step < 0.25 else 0.9):g}"); tm[id(tr)] = at + step * (1.6 if step < 0.25 else 0.9); k += 1
    for tr in rot:
        o = outs[id(tr)]
        if not o: continue
        if 4 - tm[id(tr)] > 1e-6: o.append(f"R:{4 - tm[id(tr)]:g}")
        tr.bar(b, " ".join(o))


def piano_stab(b, pat="x..x..x.x..x..x.", center=60):
    """テクノポップのピアノ: 短く切る和音（3音を1本で順に重ねられないので、根音と5度を短く）"""
    v = sorted(voice(S.chords[b], center, 3)); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] != "x": L += 1
        out.append(f"{N(v[(i // 2) % 3])}:0.2 R:{L * 0.25 - 0.2:g}" if pat[i] == "x" else f"R:{L * 0.25:g}"); i += L
    PNO.bar(b, " ".join(out))


# ---- 歌のないフックの旋律（明るく抜けるリード。1＝Eb4）: 休みと8分の跳ね。歌の旋律はなぞらない ----
HOOKL = ["R:0.5 6:0.5 1':0.5 R:0.5 3':0.75 2':0.75 1':0.5", "6:1.5 R:2.5", "R:0.5 1':0.5 3':0.5 R:0.5 5':0.75 4':0.75 3':0.5", "2':2 R:2"]
def hook(name):
    for k, b in enumerate(S.sc(name)):
        LEAD.bar(b, KG.mel(HOOKL[k % 4], oct=4))


# ---- 歌（1＝Eb3。テトが歌いやすい Bb3〜Eb5。最高は F5 を一度だけ） ----
#   歌詞: 地球のまん中（へそ）から呼びかける。曲名の言葉・「世界の中心」は使わない。直接の「すき」はサビと最後だけ
VS = {
 "呼びかけ": (["x-x-x-x---------", "x-x-x-x---------", "x-x-x-x-x-x-----", "x-x-x-x-x-------", "x-x-x-x-x-x-----", "x-x-x-x-x-------", "x-x-x-x-x-------", "x-x-x-----------"],
          ["6' 5' 3' 5'", "3' 2' 1' 6", "1' 1' 3' 4' 3' 1'", "6 1' 3' 2' 1'", "2' 2' 1' 2' 4' 3'", "3' 2' 1' 6 1'", "3' 3' 6' 7' 6'", "2' 7 3'"],
          ["きこえる", "ここだよ", "ほしのへそで", "てをふるよ", "かぜのむきが", "ゆらいでも", "このこえは", "とどく"]),
 "サビ1": (["........x-x-x-x-", "x---x-x-x-x-----", "......x-x-x-x-x-", "x---x---x-x-x---", "........x-x-x-x-", "x-x-x-x-x-------", "......x-x-x-x-x-", "x-------x-------"],
          ["1' 3' 5' 6'", "1'' 7' 6' 5' 6'", "5' 5' 6' 7' 1''", "1'' 7' 6' 5' 6'", "5' 5' b7' 5'", "6' 5' 4' 2' 1'", "1' 2' 4' 5' 6'", "1'' 5'"],
          ["ねえきみ", "すきなんだ", "そらのはて", "までとどけ", "ひかりが", "ゆれるたび", "なんどでも", "よぶ"]),
 "サビ2": (["x-x-x-x-x-x-x---", "x-------x-------", "x-x-x-x-x-x-----", "x-------x-------",
          "x-x-x-x-x-x-x---", "x-------x-------", "x-x-x-x-x-x-x-x-", "x---x-----------",
          "x-x-x-x-x-x-x---", "x---x---x-------", "x-x-x-x-x-x-----", "x---x---x-------",
          "x-x-x-x-x-x-x---", "x-------x-------", "x-x-x-x-x-x-x-x-", "x-------x-------"],
          ["1' 3' 5' 6' 5' 3' 1'", "2' 4'", "5' 6' 5' 3' 2' 1'", "3' 6",
           "b3' 5' b7' 5' 2' 5' b7'", "6' 4'", "4' 5' 6' 5' 4' 2' 4' 5'", "5' 3'",
           "1' 3' 5' 1'' 7' 6' 5'", "4' 5' 6'", "7' 6' 5' 3' 5' 6'", "1'' 7' 6'",
           "5' 5' b7' 1'' b7' 5' b3'", "4' 6'", "4' 5' 6' 1'' 2'' 1'' 6' 5'", "1'' 5'"],
          ["ちずにないみち", "でも", "まよわないよ", "ほら",
           "ほしのひかりが", "いま", "ふたりをてらして", "ゆく",
           "このむねのおと", "ならす", "このほしごと", "ゆらせ",
           "きみのなまえを", "いま", "なんどもなんども", "よぶ"]),
 "語り1": (["x-x-x-x-x-x-x-x-", "x-x-x-x-x-x-----", "x-x-x-x-x-x-x---", "x-x-x-x-x-x-----"],
          ["1'' 7' 6' 5' 4' 3' 2' 1'", "6' 5' 4' 3' 2' 1'", "6' 5' 4' 3' 2' 1' 7", "1' 2' 3' 2' 1' 6"],
          ["てんぼうだいから", "みおろすまち", "くるまもひとも", "ちいさなてん"]),
 "語り2": (["..x-x-x-x-x-x-x-", "x---x---x-------", "..x-x-x-x-x-x-x-", "x-x-x-x-x-------",
          "..x-x-x-x-x-x-x-", "x---x---x-------", "..x-x-x-x-x-x---", "x---x---x-------"],
          ["5' 5' 6' 5' 3' 5' 6'", "5' 3' 1'", "6' 6' 5' 6' 1'' 6' 5'", "5' 3' 2' 3' 1'",
           "3' 5' 6' 1'' 6' 5' 3'", "2' 3' 5'", "6' 6' 5' 4' 3' 2'", "1' 2' 1'"],
          ["そのまんなかで", "なまえ", "だれもしらない", "あいことば",
           "ほしのはしまで", "とばせ", "このおもいを", "ぜんぶ"]),
 "サビ半": (["x---x---x---x-x-", "x---x---x-------", "x---x---x-x-x-x-", "x-------x-------", "x---x---x-x-x-x-", "x---x---x-------", "x---x---x-x-x-x-", "x---x---x-------"],
          ["5' 6' 5' 3' 5'", "6' 5' 3'", "3' 5' 6' 1'' 7' 6'", "5' 6'", "6' 5' 3' 5' 6' 1''", "7' 6' 5'", "4' 3' 2' 3' 5' 6'", "5' 6' 5'"],
          ["このほしで", "ひとつ", "かけがえない", "こえ", "きこえるまで", "うたう", "いつかきみに", "とどけ"]),
 "A": (["....x-x-x-x-x-x-", "x-------x---x---", "......x-x-x-x-x-", "x-------x-------",
        "....x-x-x-x-x-x-", "x-------x---x---", "....x-x-x-x-x-x-", "x-x-x-x---------",
        "......x-x-x-x-x-", "x-------x-------", "....x-x-x-x-x-x-", "x---x---x-------",
        "......x-x-x-x-x-", "x---x---x-------", "......x-x-x-x-x-", "x-------x-------"],
       ["6 1' 3' 2' 1' 6", "1' 7 6", "6 1' 3' 5' 4'", "3' 2'",
        "6 1' 3' 2' 1' 6", "1' 2' 3'", "4' 3' 2' 1' 7 6", "7 1' 2' 1'",
        "6 1' 3' 5' 6'", "5' 3'", "3' 5' 6' 1'' 7' 6'", "5' 3' 5'",
        "5' b7' 5' 2' 5'", "1'' 7' 6'", "4' 5' 6' 5' 4'", "4' 5'"],
       ["よるのそこで", "ひとり", "かぞえてた", "ほし",
        "なまえのない", "きもち", "むねのおくに", "かくした",
        "でもいまは", "ねえ", "ちへいせんの", "むこう",
        "こえにして", "みるよ", "いまここで", "ほら"]),
 "サビ別": (["..x-x-x-x-x-x-x-", "x-------x---x---", "..x-x-x-x-x-x---", "x---x---x-------", "..x-x-x-x-x-x-x-", "x---x---x-------", "..x-x-x-x-x-x-x-", "x-------x-------"],
          ["1' 2' 3' 4' 5' 6' 5'", "6' 5' 6'", "5' 6' 1'' 6' 5' 3'", "2' 3' 5'", "6' 6' 5' 6' 1'' 7' 6'", "5' 2' 5'", "1'' 1'' 7' 6' 5' 6' 1''", "2'' 1''"],
          ["せかいのはてに", "とどく", "あいのうたを", "うたう", "とおくのきみに", "とどけ", "すきだよきみが", "いま"]),
 "まん中": (["x-x-x-x-x-x-x---", "x-x-x-x-x-x-....", "x---x---x-------", "x-x-x-x-x-x-x---", "x-x-x-x-x-------", "x---x---x-------",
           "x-x-x-x-x-x-x-x-", "x-x-x-x-x-------", "x---x---x-------", "x---x---x---x-x-", "x---x---x-------", "x-------x-------"],
          ["1' 3' 5' 5' 6' 5' 3'", "2' 3' 5' 3' 2' 1'", "2' 3' 1'", "5' 5' 6' 1'' 7' 6' 5'", "3' 5' 6' 5' 4'", "5' 2' b3'",
           "4' 4' 3' 2' 1' 2' 3' 4'", "5' 6' 5' 3' 2'", "1' 3' 6'", "1'' 1'' b6' 4' 1''", "2'' 1'' 2''", "2'' 1''"],
          ["このほしのうえ", "どこにいても", "ここが", "まんなかになる", "きみのいる", "ところ",
           "だからいまここで", "こえにして", "よぶよ", "あいしてる", "きみが", "すき"]),
}


def put(name):
    pats, degs, words = VS[name]
    lines, text = song_lines(list(zip(pats, degs, words))); bars = S.sc(name); ml = [KG.mel(x, oct=3) for x in lines]
    for b, m in zip(bars, ml):
        if m.replace("R:4", "").strip(): V.bar(b, m)
    LY.flow(bars[:len(ml)], ml, text, name)


for nm_ in VS: put(nm_)
for h_ in ("フック1", "フック2", "フック3"): hook(h_)

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); last = i == L - 1
    if n == "呼びかけ":                                   # 2小節は伴奏なしの歌だけ → エレピとベースとパッド → 5小節めから4つ打ち → 最後は2拍で止める（間）
        if i < 2: continue
        ep(b, "x---------------" if i < 4 else "x-------x-------", 63); pad(b)
        if i >= 3: bass(b, "r---------------" if i < 6 else "r-------r-------")
        if i >= 4: four(b, i, hats=i >= 6)
        if i == 2: fxh(b, 0, "rev", 2)
        if last: grid(FK, b, cutp("x...x...x...x...", 2.0), "A4"); fxh(b, 0, "riser", 2)
    elif n in ("サビ1", "サビ2", "サビ別"):               # たてノリ。サビ2 は4小節めと12小節めを3拍で止める
        stop = 3.0 if (n == "サビ2" and i in (3, 11)) else (2.0 if (n == "サビ別" and i == 7) else None)
        pogo(b, i, stop=stop, heavy=True); bass(b, BP_["pogo"][i % 4], stop)
        saw(b, cutp("x..x..x...x..x..", stop) if stop else "x..x..x...x..x.."); swell(b); piano_stab(b, cutp("x..x..x.x..x..x.", stop) if stop else "x..x..x.x..x..x.")
        pad(b)                                             # v4: サビ1 にもパッド（パッドを外すと点が 7.42 → 7.03 に下がった）
        if i == 0: fxh(b, 0, "impact", 2)
        if stop: fxh(b, 3.0 if stop == 3.0 else 2.0, "glitch", 0.5)
        if n == "サビ2" and i == 7: fxh(b, 2, "rev", 2)
    elif n == "立ち上げ":                                  # 交互の刻み（エレピ・プラック・ピアノ）→ スネアが増える → 最後の小節の後半は何も鳴らさない（間）
        ep(b, "x---------------", 63, short=2); pad(b)
        alt(b, ("x.x.x.x.x.x.x.x.", "xx.xx.x.xx.xx.x.")[i % 2] if i < 7 else "x.x.x.x.........")
        if i >= 2: bass(b, BP_["half"][i % 4] if i < 7 else "r-------........")
        if i >= 4: build(b, i, (i - 4) // 1 if i < 7 else 2) if i < 7 else grid(FSN, b, "xxxxxxxx........", "A#4")
        if i == 4: fxh(b, 0, "riser", 4)
    elif n in ("フック1", "フック2", "フック3"):           # ヒップホップのブレイクビート＋交互の刻み＋リード（歌はない）
        stop = 2.0 if (n == "フック3" and i == 9) else None
        if n == "フック3" and i >= 8:                      # 最後の2小節はスネアが増えて、2拍で止める（間）→ ドロップ
            grid(FSN, b, "x.x.x.x.xxxxxxxx" if i == 8 else "xxxxxxxx........", "A#4"); grid(FK, b, "x...x...x...x..." if i == 8 else "x...x...........", "A4")
            if i == 8: fxh(b, 0, "riser", 4)
        else:
            brk(b, i, stop)
        bass(b, BP_["brk"][i % 4], stop); ep(b, "x.....x.........", 63, short=1.0)
        alt(b, "..x.x...x.x..x.x", stop=stop)
    elif n in ("語り1", "語り2"):                          # 早口の語り: ブレイクビートとベースとエレピだけ（すき間を空ける）
        brk(b, i); bass(b, BP_["brk"][(i + 1) % 4]); ep(b, "x-------........", 63, short=1.5)
        if i % 4 == 3: fxh(b, 3.5, "glitch", 0.5)
    elif n == "サビ半":                                    # 半分の速さ: 深いパッドとふくらむスーパーソウ。スネアは3拍めだけ
        halftime(b, i, stop=2.0 if last else None); bass(b, BP_["half"][i % 4], 2.0 if last else None); swell(b); pad(b)
        ep(b, "x-------x-------", 63)
        if i == 0: fxh(b, 0, "subdrop", 2)
        if last: fxh(b, 2, "rev", 2)
    elif n == "A":                                         # 静か: きらめくパッドとエレピ。後半からまっすぐ4つ打ち
        pad(b); ep(b, "x---------------" if i < 8 else "x-------x-------", 60)
        if i >= 4: bass(b, "r---------------" if i < 8 else "r-------r-------")
        if i >= 8: four(b, i, hats=i >= 12)
        if last: fxh(b, 0, "riser", 4)
    elif n == "ドロップ":                                  # Kawaii future bass のドロップ: スーパーソウの刻み・重いキック・5小節めと9小節めに32分の高速の交互刻み
        stop = 2.0 if last else None
        pogo(b, i, stop=stop, heavy=True); bass(b, BP_["pogo"][(i + 2) % 4], stop)
        saw(b, cutp("x.xx.x.xx.x.x.x.", stop) if stop else "x.xx.x.xx.x.x.x.", short=0.2); swell(b); pad(b)
        if i in (4, 8): alt(b, "x" * 16 + "." * 16, step=0.125, center=74)
        elif not last: alt(b, "x..x..x...x..x..", rot=(PLK, EPX), center=76)
        if i == 0: fxh(b, 0, "impact", 2)
        if last: fxh(b, 2, "glitch", 0.5)
    elif n == "まん中":                                    # 最後: 大きくふくらんで、歌の最後の音（最後の小節の頭）で全部が止まる
        if i < 11:
            pogo(b, i, heavy=i >= 6); bass(b, BP_["pogo"][i % 4]); saw(b); swell(b); pad(b); piano_stab(b) if i >= 6 else None
            if i == 6: fxh(b, 0, "impact", 2)
            if i == 10: fxh(b, 2, "rev", 2)
        else:                                              # 最後の小節: 和音を一度だけ鳴らして、歌の「すき」と同時に切れる
            ep(b, "x-------........", 63); saw(b, "x-------........", short=2.0); bass(b, "r-------........"); grid(FK, b, "x...............", "A4"); grid(FK2, b, "x...............", "F#5")
            fxh(b, 0, "impact", 2)

for b, hits in FXH.items():
    out, t = [], 0.0
    for at, name, L_ in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{FXK[name]}:{L_:g}"); t = at + L_
    if 4 - t > 1e-6: out.append(f"R:{4 - t:g}")
    if hits: FXT.bar(b, " ".join(out))
S.fade_out = 0
S.desc = ("仮: Kawaii future bass × テクノポップ × ヒップホップのダンスの歌（180・ハ短調→変ホ長調・約2分45秒）。地球のまん中で、ひとりが呼びかける。"
          "伴奏なしの1句で始まり、交互の刻み・ブレイクビートの語り・半分の速さのサビ・32分の交互刻みのドロップを通って、歌の最後の音で全部が止まる。自作")
finish(S, LY, V, 0, flat=True)  # v2 で2半音下げたら点が下がった（7.42 → 7.24）のでもどした

from vt3x_lib import *
path = sys.argv[1]
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"verse": 8, "bridge": 6, "chorus": 14, "outro": 12, "pre": 8, "break": 8, "drop": 8}, scoop=0.05, slash=0.2, vib_min_beats=2.0, vib_start=0.45, auto=0.5, breaths=0.0)
    voice_by_scene(path, S, {}, default="smooth")                                       # 1曲1種類の声: なめらか（v3。サビ2 だけで比べると クリア 6.85・ウィスパー 6.92・キュート 6.71・なめらか 7.37）
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path)
keep = (lambda p_: not p_.get("role", "").startswith("歌の役")) if VOCAL else (lambda p_: True)   # 歌の版: 歌をなぞるリードはパートごと外す
js["parts"] = [p_ for p_ in js["parts"] if keep(p_) and p_.get("notes", "").replace("R:", "").strip()]
js["grooveFeel"] = "tight"; js["human"] = 0.3
save(path, js)
# v5: 測ると、サビが A や語りより 1〜1.5 LU 小さかった（4つ打ちのキックで仕上げのリミッターが強くかかる）。サビ・ドロップを上げ、静かな A と語りを少し下げて、
#   サビ1 < サビ2 < サビ別 < まん中 の山にする。変わり目で下がるのは 1.5dB 未満
final_gain(path, {"サビ1": 0.8, "サビ2": 1.0, "ドロップ": 1.0, "サビ別": 1.2, "まん中": 1.8, "A": -1.0, "語り1": -0.6, "語り2": -0.6,
                  "フック1": -0.3, "フック2": -0.3, "立ち上げ": -0.3})
