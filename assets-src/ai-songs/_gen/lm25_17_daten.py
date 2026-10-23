# ラウド25曲（第2シリーズ）17「堕天の証明」（仮）。イメージ: 悪魔×天使。F♯ 短調（悪魔）↔ F♯ 長調（天使）・136・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 合唱（天使の場面の和音と、最後に一つになる場面）
# 物語: 悪魔（F♯ 短調・スウィープ・スラップ）と天使（F♯ 長調・タッピング・合唱）が言い争い、戦い、天使が落ち、最後に二つが一つになる。
# 形（ほかの曲と変える）: 2つの主題が交互に出る（悪魔のAメロ → 天使のAメロ → 悪魔のサビ → 天使のサビ …）。
#   見せ場の「戦い」は24小節: 2小節ごとにスウィープ（悪魔）とタッピング（天使）が入れ替わる。最後の「一つになる」は長調のサビの下で悪魔のリフが鳴る
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 136, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("demon", 8), ("angel", 8), ("dchorus", 8), ("achorus", 8), ("demon2", 8), ("angel2", 8),
        ("battle", 24), ("fall", 8), ("merge", 16), ("outro", 4)]
DEMON = ["F#m", "F#m", "D", "C#7", "F#m", "F#m", "G", "C#7"]
ANGEL = ["F#", "D#m7", "Bmaj7", "C#", "F#", "A#m7", "Bmaj7", "C#sus4"]
DCH = ["D", "E", "F#m", "C#7", "D", "E", "G", "C#7"]
ACH = ["B", "C#", "A#m7", "D#m", "B", "C#", "D", "C#"]
BATTLE = ["F#m", "F#m", "F#", "F#", "Bm", "Bm", "B", "B", "D", "D", "D#m", "D#m", "G", "G", "C#", "C#", "F#m", "G", "F#", "B", "C#7", "C#7", "C#", "C#"]
CH = {"intro": ["F#", "F#", "F#m", "F#m", "F#m", "F#m", "G", "C#7"], "demon": DEMON, "angel": ANGEL, "dchorus": DCH, "achorus": ACH,
      "demon2": DEMON, "angel2": ANGEL, "battle": BATTLE, "fall": ["Bmaj7", "A#m7", "G#m7", "F#", "Emaj7", "D#m7", "D", "C#"],
      "merge": ACH + ACH[:7] + ["F#"], "outro": ["F#", "F#", "F#", "F#"]}
song = Song("堕天の証明（仮）",
            "仮: ラウド25曲（第2シリーズ）の17曲目。イメージは悪魔×天使。F♯ 短調（悪魔: スウィープ・スラップ・♭Ⅱ の G）と F♯ 長調（天使: タッピング・合唱）の2つの主題が交互に出て、"
            "24小節の戦い（2小節ごとにスウィープとタッピングが入れ替わる）、天使の墜落、最後は長調のサビの下で悪魔のリフが鳴り一つになる。別の楽器は合唱。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 悪魔と天使が言い争い、戦い、天使が落ち、最後に二つが一つになる。"
song.kinds = {"demon": "verse", "angel": "verse", "dchorus": "chorus", "achorus": "chorus", "demon2": "verse", "angel2": "verse",
              "battle": "solo", "fall": "bridge", "merge": "chorus"}
SECS, NB = song.secs, song.nb
song.pickups = ['V3', 'V5']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

D_RIFF = {"F#m": [bar("F#2:0.5! A2:0.5 G2:0.5 F#2:0.5 C#3:0.5 D3:0.5 C#3:0.5 G2:0.5"), bar("F#2:0.5! A2:0.5 G2:0.5 F#2:0.5 E3:0.5 D3:0.5 C#3:0.5 A2:0.5")],
          "G": [bar("G2:0.5! B2:0.5 A2:0.5 G2:0.5 D3:0.5 E3:0.5 D3:0.5 A2:0.5")] * 2,
          "C#7": [bar("C#2:0.5! F2:0.5 G#2:0.5 B2:0.5 C#3:0.5 B2:0.5 G#2:0.5 F2:0.5")] * 2,
          "D": [bar("D2:0.5! F#2:0.5 E2:0.5 D2:0.5 A2:0.5 B2:0.5 A2:0.5 F#2:0.5")] * 2}
U_RIFF = [bar("F#2:0.5! A#2:0.5 G#2:0.5 F#2:0.5 C#3:0.5 D#3:0.5 C#3:0.5 G#2:0.5"), bar("F#2:0.5! A#2:0.5 G#2:0.5 F#2:0.5 F3:0.5 D#3:0.5 C#3:0.5 A#2:0.5")]
def shape_riff(ch):
    """悪魔のリフの形（根音・3度・2度・根音・5度・6度・5度・2度）を、その和音の長調／短調で"""
    rr, q, _ = parse_chord(ch)
    r = root_note(ch, "E2", "D#3")
    mode = "aeolian" if q.startswith("m") else "ionian"
    sc = scale_notes(rr, mode, r, up(r, 1), flat="b" in rr)
    seq = [sc[0], sc[2], sc[1], sc[0], sc[4], sc[5], sc[4], sc[1]]
    return bar(" ".join(f"{x}:0.5{'!' if j == 0 else ''}" for j, x in enumerate(seq)))


A_RIFF = bar("F#2:0.5! C#3:0.5 F#3:0.5 A#3:0.5 C#4:0.5 A#3:0.5 F#3:0.5 C#3:0.5")

DEMON_MEL = [bar("R:0.5 C#4:0.5 F#4:0.5 A4:0.5 G#4:1 F#4:1"), bar("C#5:2 A4:1 R:1"), bar("D4:1 F#4:1 A4:1.5 G4:0.5"), bar("G#4:2 B4:1 R:1"),
             bar("R:0.5 F#4:0.5 A4:0.5 C#5:0.5 E5:1 D5:1"), bar("C#5:2 R:2"), bar("B4:1 G4:1 D5:2"), bar("C#5:1 F5:1 G#5:1 R:1")]
DEMON2_MEL = [bar("R:0.5 F#4:0.5 A4:0.5 C#5:0.5 B4:1 A4:1"), bar("F#5:2 C#5:1 R:1"), bar("F#4:1 A4:1 D5:1.5 C#5:0.5"), bar("B4:2 G#4:1 R:1"),
              bar("R:0.5 A4:0.5 C#5:0.5 F#5:0.5 A5:1 G#5:1"), bar("F#5:2 R:2"), bar("D5:1 B4:1 G5:2"), bar("F5:1 G#5:1 B5:1 R:1")]
ANGEL_MEL = [bar("R:1 A#4:1 C#5:2"), bar("D#5:3 C#5:1"), bar("R:1 B4:1 D#5:2"), bar("F5:2 G#5:2"),
             bar("R:1 A#4:1 F#5:2"), bar("C#5:3 A#4:1"), bar("D#5:2 F#5:2"), bar("F#5:2 G#5:2")]
ANGEL2_MEL = [bar("R:1 C#5:1 F#5:2"), bar("F#5:3 D#5:1"), bar("R:1 D#5:1 F#5:2"), bar("G#5:2 F5:2"),
              bar("R:1 C#5:1 A#5:2"), bar("G#5:3 F5:1"), bar("F#5:2 A#5:2"), bar("G#5:2 C#6:2")]
DCH_MEL = [bar("R:0.5 A4:0.5 D5:0.5 F#5:0.5 A5:2!"), bar("G#5:1 E5:1 B4:2"), bar("A5:1.5 F#5:0.5 C#6:2"), bar("B5:1 G#5:1 F5:2"),
           bar("R:0.5 F#5:0.5 A5:0.5 D6:0.5 A5:2"), bar("B5:1 G#5:1 E6:2!"), bar("D6:1 B5:1 G5:2"), bar("F5:2 C#5:1 R:1")]
ACH_MEL = [bar("R:0.5 D#5:0.5 F#5:0.5 B5:0.5 D#6:2!"), bar("C#6:1 G#5:1 F5:2"), bar("C#6:1.5 A#5:0.5 G#5:2"), bar("F#5:1 A#5:1 D#6:2"),
           bar("R:0.5 F#5:0.5 B5:0.5 D#6:0.5 B5:2"), bar("C#6:1 F5:1 G#5:2"), bar("D6:1 A5:1 F#5:2"), bar("F5:2 G#5:1 R:1")]
MERGE_MEL = ACH_MEL[:7] + [bar("F5:2 G#5:2")] + [bar("D#6:4!"), bar("C#6:2 G#5:2"), bar("C#6:2 A#5:2"), bar("A#5:1 C#6:1 D#6:2"),
                                                   bar("R:0.5 F#5:0.5 B5:0.5 D#6:0.5 F#5:2"), bar("C#6:1 F5:1 G#5:2"), bar("D6:2 A5:2"), bar("A#5:4!")]
FALL_MEL = [bar("D#5:4"), bar("C#5:2 A#4:2"), bar("B4:4"), bar("A#4:2 F#4:2"), bar("G#4:4"), bar("F#4:2 D#4:2"), bar("D4:2 F#4:2"), bar("F4:4")]

CHOIR_V = {"F#": ["F#4", "A#4", "C#5"], "D#m7": ["F#4", "A#4", "C#5"], "Bmaj7": ["F#4", "A#4", "D#5"], "C#": ["F4", "G#4", "C#5"], "A#m7": ["F4", "G#4", "C#5"],
           "C#sus4": ["F#4", "G#4", "C#5"], "B": ["F#4", "B4", "D#5"], "D#m": ["F#4", "A#4", "D#5"], "D": ["F#4", "A4", "D5"], "G#m7": ["F#4", "B4", "D#5"],
           "Emaj7": ["G#4", "B4", "D#5"]}
SWEEP_R = {"F#m": ("F#4", "F#5"), "Bm": ("F#4", "D5"), "D": ("F#4", "F#5"), "G": ("G4", "G5"), "C#7": ("F4", "F5")}
TAP_T = {"F#": ["A#4", "C#5", "F#5"], "B": ["B4", "D#5", "F#5"], "D#m": ["A#4", "D#5", "F#5"], "C#": ["G#4", "C#5", "F5"]}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "q0", "q1", "q2", "bass", "pop", "mute"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
SLAP = ["T..gP.T.gTP.T.gP", "T.gP..TgP.T.gPT.", "T..gP.T.gTP.FgP.", "T.gPT.gP.TgP.T.g"]
DEMONISH = ("demon", "dchorus", "demon2")


def split_slap(b):
    pt, mt = [], []
    for t in b.split():
        if t.endswith("'"): pt.append(t); mt.append("R:" + t.split(":")[1].rstrip("'"))
        else: pt.append("R:" + t.split(":")[1].rstrip("!'")); mt.append(t)
    return merge_rests(" ".join(mt)), merge_rests(" ".join(pt))


for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)
    minor = base_ch in ("F#m", "G", "C#7", "D", "Bm")

    rf = R4
    if name == "intro" and i >= 2: rf = D_RIFF[base_ch if base_ch in D_RIFF else "F#m"][i % 2]
    elif name in ("demon", "demon2") and i % 4 < 2: rf = D_RIFF[base_ch if base_ch in D_RIFF else "F#m"][i % 2]
    elif name == "merge": rf = shape_riff(ch) if i < 15 else bar("F#2:4!")    # 一つになる: 悪魔のリフの形のまま長調に（A→A♯・G→G♯）
    elif name == "outro" and i == 0: rf = A_RIFF
    P["riff"].append(rf)

    s = si = R4
    if name in ("dchorus", "achorus") or name == "merge":
        s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1") if not (last and name != "merge") else bar(f"{groot}:2! R:2")
        si = s
    elif name in ("demon", "demon2") and i % 4 >= 2:
        s = bar(f"{groot}:2 {groot}:2")
    elif name in ("angel", "angel2"):
        s = bar(f"{groot}:4") if name == "angel2" else R4
    elif name == "battle":
        s = bar(f"{groot}:4")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tech = R4; qv = [R4, R4, R4]
    if name == "demon": lead = DEMON_MEL[i]
    elif name == "demon2": lead = DEMON2_MEL[i]
    elif name == "angel": lead = ANGEL_MEL[i]
    elif name == "angel2": lead = ANGEL2_MEL[i]
    elif name == "dchorus": lead = DCH_MEL[i]
    elif name == "achorus": lead = ACH_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "merge": lead = MERGE_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "fall": lead = FALL_MEL[i]
    elif name == "battle":
        if minor:
            lo, hi = SWEEP_R[base_ch]
            tech = bar(sweep(ch, lo, hi, 2), sweep(ch, lo, hi, 2)) if i % 2 == 0 else bar(sweep(ch, lo, hi, 2), f"{chord_tones(ch, lo, hi)[-1]}:2")
        else:
            tri = TAP_T[base_ch]
            tech = bar(tap(tri, 3, pattern=(2, 1, 0, 1)), f"{tri[2]}:1")
        if i >= 20: tech = bar(tap(TAP_T["C#"], 2, pattern=(2, 1, 0, 1)), sweep("C#7", "F4", "F5", 2)) if i < 23 else bar("C#6:4!")
    elif name in ("intro",) and i < 2: tech = bar(tap(TAP_T["F#"], 4, pattern=(0, 1, 2, 1)))
    if (name in ("angel", "angel2", "achorus", "fall", "merge", "outro")) or (name == "intro" and i < 2):
        v = CHOIR_V.get(base_ch)
        if v: qv = [bar(f"{x}:3.5 R:0.5") if i % 2 == 1 else bar(f"{x}:4") for x in v]
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech)
    for j in range(3): P[f"q{j}"].append(qv[j])

    pop = mute = R4
    if name == "intro":
        b = R4 if i < 2 else unison_low(P["riff"][-1], -1, "B0")
    elif name in ("demon", "demon2"):
        if i % 4 < 2: b = unison_low(P["riff"][-1], -1, "B0")
        else: b, mute = bass_slap_bar(ch, BEATS, SLAP[i % 4]); b, pop = split_slap(b)
    elif name in ("angel", "angel2", "fall"):
        b = bar(f"{root}:2 {fifth_of(base_ch)}:2") if name != "fall" else bar(f"{root}:4")
    elif name in ("dchorus", "achorus", "battle"):
        b = bass_root8(ch, BEATS, nxt) if not (last and name != "battle") else bar(f"{root}:1.5! {root}:0.5 R:2")
    elif name == "merge":
        b = unison_low(P["riff"][-1], -1, "B0") if i < 15 else bar("F#1:4!")
    elif name == "outro":
        b = bar("F#1:4") if i < 3 else bar("F#1:4!")
    else:
        b = R4
    P["bass"].append(b); P["pop"].append(pop); P["mute"].append(mute)

    k = s = h = None; tom = cym = None
    if name == "intro":
        if i < 2: cym = f"{BELL}:1 {BELL}:1, {BELL}:1, {BELL}:1," if i == 0 else f"{RIDE}:1 {RIDE}:1 {RIDE}:1 R:1"
        if i == 1: tom = "R:3 " + tom_16_down(1)
        if i >= 2:
            k = "X.X...X.X.X...X."; s = "....X.......X..."; h = "x.X.x.X.x.X.x.X."
            if i == 2: cym = f"{CHINA}:1! R:3"; h = "..X." + h[4:]       # 悪魔が割りこむ
            if last: k, s, tom = linear_fill(kit, 2, 0); k = "X.X...X." + k[8:]; s = "....X..." + s[8:]; h = None
    elif name in ("demon", "demon2", "dchorus"):
        k = ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2] if name != "dchorus" else "XxXxXxXxXxXxXxXx"
        s = "....X.......X..."
        k = "".join("." if s[j] != "." else c for j, c in enumerate(k)) if name == "dchorus" else k
        h = "x.X.x.X.x.X.x.X." if name != "dchorus" else None
        cym = f"{CHINA}:0.5! {RIDE}:0.5 {CHINA}:0.5 {RIDE}:0.5 {CHINA}:0.5! {RIDE}:0.5 {CHINA}:0.5 {RIDE}:0.5" if name == "dchorus" else None
        if i == 0: cym = f"{CR}:1! " + ("R:3" if name != "dchorus" else f"{RIDE}:0.5 {CHINA}:0.5 {RIDE}:0.5 {CHINA}:0.5! {RIDE}:0.5 {CHINA}:0.5"); h = h and "..X." + h[4:]
        if last: k, s, tom = linear_fill(kit, 2, i + idx); k = "X.x...X." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
    elif name in ("angel", "angel2", "achorus"):
        # 天使: ハーフタイムで浮く、ライドとベル
        k = "X.......X......." if name != "achorus" else "X.....X.X......."
        s = "........X......."
        cym = f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
        if i == 0: cym = f"{CR2}:2! {RIDE}:1! {BELL}:1"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1! {BELL}:1 R:2"; s = "........X......."
    elif name == "battle":
        # 戦い: 悪魔の2小節はツーバス、天使の2小節はハーフ
        if minor:
            k = "XxXxXxXxXxXxXxXx"; s = "....X.......X..."; k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
            cym = f"{CHINA}:0.5! {RIDE}:0.5 {CHINA}:0.5 {RIDE}:0.5 {CHINA}:0.5! {RIDE}:0.5 {CHINA}:0.5 {RIDE}:0.5"
        else:
            k = "X.......X.x....."; s = "........X......."; cym = f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
        if i % 2 == 0: cym = (f"{CHINA}:1! " if minor else f"{CR}:1! ") + " ".join(cym.split()[2:]) if False else cym
        if i % 2 == 0: cym = (f"{CHINA}:1! " if minor else f"{CR}:1! ") + ("R:3" if not minor else f"{CHINA}:0.5! {RIDE}:0.5 {CHINA}:0.5 {RIDE}:0.5 {CHINA}:0.5! {RIDE}:0.5")
        if last: k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
    elif name == "fall":
        k = "X..............." if i % 2 == 0 else "X.......X......."
        cym = f"{RIDE}:1, {RIDE}:1, {RIDE}:1, {RIDE}:1,"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1, {RIDE}:1, R:2"
    elif name == "merge":
        k = ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2] if i < 8 else "XxXxXxXxXxXxXxXx"
        s = "....X.......X..."; k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        h = "x.X.x.X.x.X.x.X." if i < 8 else None
        cym = None if i < 8 else f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + ("R:3" if i < 8 else f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"); h = h and "..X." + h[4:]
        if i == 7: k, s, tom = linear_fill(kit, 2, 3); k = "X.x...X." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
        if last: k = "X..............."; s = "X..............."; h = None; cym = f"{CR}:4!"
    elif name == "outro":
        cym = f"{BELL}:1 {BELL}:1, {BELL}:1, {BELL}:1," if i < 3 else None
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("dchorus", "achorus", "merge", "battle"): FX.append(bar("R:2 C4:2"))
    elif name == "fall" and i == 5: FX.append(bar("E4:4"))
    elif name == "outro" and i == 0: FX.append(bar("R:1 B4:3"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="スウィープとタッピングのギター", vol=0.11, pan=0.05))
song.add([part(f"合唱（{['上', '中', '下'][j]}）", "choir", J(f"q{j}"), volume=0.07, pan=[-0.3, 0.3, 0][j], reverb=0.55, attack=0.25, release=0.9,
               fx=[{"type": "eq", "low": -4, "mid": -1, "midHz": 700, "high": 0}, {"type": "reverb", "mix": 0.3}]) for j in range(3)])
song.add(bass_part(J("bass")))
song.add(slap_pop_part(J("pop")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "wide-dark-wall"
add_layer(song, "organ", "堕ちる天使の背後で、大聖堂のオルガンが鳴る。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-17-daten.json"
    song.write(out)
    check_clash(song)
