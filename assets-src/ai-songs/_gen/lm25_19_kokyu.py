# ラウド25曲（第2シリーズ）19「最後の呼吸」（仮）。イメージ: 生と死。B 短調・104・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 弦楽合奏（録音 VSCO 2 CE。回想の和音・子どもの頃のピチカートと旋律・最後の一息）
# 物語: 最期の瞬間（サビの頂点）から始まり、人生を巻き戻す。大人の日々（ジャズ）→ 若い頃（速いレガート）→ 子どもの頃（弦だけの D 長調）
#   → もう一度いまへ戻り、最後のサビのあと、弦の和音が消えて「最後の一息」の無音で終わる。
# 形（ほかの曲と変える）: 逆回し。曲の頭がいきなりサビの頂点。Aメロ・Bメロという区切りではなく、人生の時代ごとに音が変わる。最後は無音
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 104, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("climax", 8), ("breath", 2), ("adult", 12), ("adult2", 8), ("youth", 16), ("child", 8), ("return", 8), ("climax2", 16), ("last", 4)]
CLIMAX = ["G", "D/F#", "Em7", "Bm/D", "Cmaj7", "A", "F#7sus4", "F#7"]
CH = {"climax": CLIMAX, "breath": ["Bm9", "Bm9"],
      "adult": ["Bm7", "E9", "Am7", "D9", "Gmaj7", "Cmaj7", "F#7b9", "Bm7", "Em9", "A7", "Dmaj7", "F#7"],
      "adult2": ["G", "A", "Bm", "D/A", "Gmaj7", "A", "F#7sus4", "F#7"],
      "youth": ["Bm", "Bm", "G", "A", "Bm", "Bm", "G", "F#", "Em", "Em", "G", "A", "Bm", "G", "F#7", "F#7"],
      "child": ["D", "A/C#", "Bm", "F#m", "G", "D/F#", "Em", "A"],
      "return": ["Bm", "G", "D", "A", "Bm", "G", "Em", "F#7"],
      "climax2": CLIMAX + ["G", "D/F#", "Em7", "Bm/D", "Cmaj7", "A", "Bsus4", "B"], "last": ["Bm9", "Bm9", "Bm9", "Bm9"]}
song = Song("最後の呼吸（仮）",
            "仮: ラウド25曲（第2シリーズ）の19曲目。イメージは生と死。B 短調・104。逆回しの形: 曲の頭がいきなりサビの頂点（最期の瞬間）、大人の日々（ジャズの和音）、"
            "若い頃（速いレガート）、子どもの頃（弦楽合奏だけの D 長調・ピチカート）と巻き戻り、もう一度いまへ戻って最後のサビ、弦が消えて無音の一息で終わる。別の楽器は弦楽合奏。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 最期の瞬間から始まり、人生を巻き戻し、もう一度いまへ戻って、最後の一息で終わる。"
song.kinds = {"climax": "chorus", "breath": "break", "adult": "verse", "adult2": "pre", "youth": "solo", "child": "bridge", "return": "pre", "climax2": "chorus", "last": "outro"}
SECS, NB = song.secs, song.nb

CLIMAX_MEL = [bar("B5:2! A5:1 G5:1"), bar("F#5:3 D5:1"), bar("G5:1 B5:1 D6:2!"), bar("B5:3 F#5:1"),
              bar("E6:2! D6:1 B5:1"), bar("C#6:2 A5:1 E5:1"), bar("B5:2 C#6:2"), bar("A#5:4")]
CLIMAX2_MEL = [bar("R:0.5 D5:0.5 G5:0.5 A5:0.5 B5:2!"), bar("A5:1 F#5:1 D5:2"), bar("R:0.5 E5:0.5 G5:0.5 B5:0.5 D6:2!"), bar("C#6:1 B5:1 F#5:2"),
               bar("E6:2! D6:1 B5:1"), bar("C#6:2 E6:1 A5:1"), bar("B5:2 C#6:2"), bar("A#5:2 C#6:2"),
               bar("B5:2! D6:1 B5:1"), bar("A5:2 F#5:2"), bar("G5:1 B5:1 E6:2!"), bar("D6:2 B5:2"),
               bar("E6:2 G5:1 B5:1"), bar("C#6:2 A5:2"), bar("B5:2 E5:2"), bar("D#6:4!")]
ADULT_MEL = [bar("R:1 F#4:0.5 A4:0.5 D5:1 C#5:1"), bar("B4:1.5 G#4:0.5 D5:2"), bar("R:1 E4:0.5 G4:0.5 C5:1 B4:1"), bar("A4:1.5 F#4:0.5 C5:2"),
             bar("R:0.5 B4:0.5 D5:0.5 F#5:0.5 E5:1.5 D5:0.5"), bar("G5:1 E5:1 B4:2"), bar("A#4:1 C#5:1 E5:2"), bar("F#5:2 D5:1 R:1"),
             bar("R:1 G4:0.5 B4:0.5 F#5:2"), bar("E5:1 C#5:1 G5:2"), bar("F#5:1.5 E5:0.5 C#5:2"), bar("A#4:2 C#5:1 R:1")]
ADULT2_MEL = [bar("B4:1 D5:1 G5:2"), bar("C#5:1 E5:1 A5:2"), bar("D5:1 F#5:1 B5:2"), bar("A5:2 F#5:2"),
              bar("F#5:1 B5:1 D6:2"), bar("C#6:1 A5:1 E5:2"), bar("B5:2 C#6:2"), bar("A#5:2 R:2")]
CHILD_MEL = [bar("F#5:1 A5:1 D6:2"), bar("E5:1 A5:1 C#6:2"), bar("D6:1.5 C#6:0.5 B5:2"), bar("A5:2 F#5:2"),
             bar("B5:1 D6:1 G5:2"), bar("A5:1 F#5:1 D5:2"), bar("G5:1 B5:1 E6:2"), bar("A5:2 R:2")]
RETURN_MEL = [bar("B4:4"), bar("D5:2 B4:2"), bar("F#5:4"), bar("E5:2 C#5:2"), bar("D5:2 F#5:2"), bar("G5:4"), bar("E5:2 G5:2"), bar("F#5:2 A#5:2")]
YOUTH_TECH = {}
for j, c in enumerate(CH["youth"]):
    if j % 2 == 0:
        base = {"Bm": ("B4", "B5"), "G": ("G4", "G5"), "Em": ("E5", "E6"), "F#7": ("F#5", "F#4")}.get(c)
        if base:
            YOUTH_TECH[j] = bar(legato_run("B", "aeolian" if c != "F#7" else "harmonic", base[0], base[1], 2), f"{base[1]}:2")
YOUTH_LEAD = {1: bar("D5:1 F#5:1 B5:2"), 3: bar("C#5:1 E5:1 A5:2"), 5: bar("F#5:2 D5:1 B4:1"), 7: bar("A#4:1 C#5:1 F#5:2"),
              9: bar("G5:1 B5:1 E5:2"), 11: bar("E5:1 A5:1 C#6:2"), 13: bar("B5:2 G5:2"), 15: bar("A#5:2 R:2")}

STR_V = {"G": ["B3", "D4", "G4"], "D/F#": ["A3", "D4", "F#4"], "Em7": ["B3", "D4", "G4"], "Bm/D": ["B3", "D4", "F#4"], "Cmaj7": ["B3", "E4", "G4"],
         "A": ["A3", "C#4", "E4"], "F#7sus4": ["B3", "C#4", "E4"], "F#7": ["A#3", "C#4", "E4"], "Bm9": ["C#4", "D4", "F#4"], "Bm": ["B3", "D4", "F#4"],
         "D": ["A3", "D4", "F#4"], "Bsus4": ["B3", "E4", "F#4"], "B": ["B3", "D#4", "F#4"], "A/C#": ["A3", "C#4", "E4"], "F#m": ["A3", "C#4", "F#4"]}


def pizz(ch):
    t = chord_tones(ch.split("/")[0], "D3", "D5")
    return bar(" ".join(f"{t[j % len(t)]}:0.5{'!' if j == 0 else ''}" for j in (0, 2, 4, 2, 1, 3, 5, 3)))


P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "s0", "s1", "s2", "smel", "pizz", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
YRIFF = {"Bm": bar("B1:0.5! F#2:0.5 B2:0.5 A2:0.5 F#2:0.5 D2:0.5 E2:0.5 F#2:0.5"), "G": bar("G1:0.5! D2:0.5 G2:0.5 F#2:0.5 D2:0.5 B1:0.5 C2:0.5 D2:0.5"),
         "A": bar("A1:0.5! E2:0.5 A2:0.5 G2:0.5 E2:0.5 C#2:0.5 D2:0.5 E2:0.5"), "F#": bar("F#1:0.5! C#2:0.5 F#2:0.5 E2:0.5 C#2:0.5 A#1:0.5 B1:0.5 C#2:0.5"),
         "Em": bar("E2:0.5! B2:0.5 E3:0.5 D3:0.5 B2:0.5 G2:0.5 A2:0.5 B2:0.5"), "F#7": bar("F#1:0.5! C#2:0.5 F#2:0.5 E2:0.5 C#2:0.5 A#1:0.5 B1:0.5 C#2:0.5")}

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = YRIFF[ch] if name == "youth" and ch in YRIFF else R4
    P["riff"].append(rf)

    s = si = R4
    if name in ("climax", "climax2"):
        s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1") if not (name == "climax" and last) else bar(f"{groot}:2! R:2")
        if name == "climax2" and last: s = bar(f"{groot}:4!")
        si = s
    elif name in ("adult2", "return") or (name == "adult" and i >= 8):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
    elif name == "youth":
        s = bar(f"{groot}:2 {groot}:2")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tech = smel = pz = R4; sv = [R4, R4, R4]
    if name == "climax": lead = CLIMAX_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "climax2": lead = CLIMAX2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "adult": lead = ADULT_MEL[i]
    elif name == "adult2": lead = ADULT2_MEL[i]
    elif name == "youth": tech = YOUTH_TECH.get(i, R4); lead = YOUTH_LEAD.get(i, R4)
    elif name == "child": smel = CHILD_MEL[i]; pz = pizz(ch)
    elif name == "return": lead = RETURN_MEL[i]
    elif name == "last": lead = bar("B5:4") if i == 0 else R4
    if name in ("climax", "breath", "return", "climax2", "child") or (name == "adult" and i % 4 == 0) or (name == "last" and i < 3):
        v = STR_V.get(ch)
        if v:
            if name == "last": sv = [bar(f"{x}:4") if i < 2 else bar(f"{x}:2 R:2") for x in v]
            elif name == "adult": sv = [bar(f"{x}:4") for x in v]
            else: sv = [bar(f"{x}:4") for x in v]
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech); P["smel"].append(smel); P["pizz"].append(pz)
    for j in range(3): P[f"s{j}"].append(sv[j])

    if name in ("climax", "climax2"):
        b = bass_root8(ch, BEATS, nxt) if not (last and name == "climax") else bar(f"{root}:1.5! {root}:0.5 R:2")
        if name == "climax2" and last: b = bar(f"{root}:4!")
    elif name == "breath": b = R4
    elif name == "adult":
        rr, q, _ = parse_chord(ch)
        tones = chord_tones(ch, root, up(root, 1))
        b = bar(f"{root}:1! {tones[1]}:1 {tones[2]}:1 {approach_note(ch, nxt)}:1")      # 大人の日々: ジャズの4分
    elif name in ("adult2", "return"): b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name == "youth": b = unison_low(P["riff"][-1], -1, "B0") if P["riff"][-1] != R4 else bass_root8(ch, BEATS, nxt)
    elif name == "child": b = bar(f"{root_note(ch, 'D2', 'C#3')}:2 {root_note(ch, 'D2', 'C#3')}:2,")
    elif name == "last": b = bar("B1:4") if i < 2 else R4
    else: b = R4
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("climax", "climax2"):
        # 頂点: 頭からツーバスとクラッシュ
        k = "XxXxXxXxXxXxXxXx" if (name == "climax" or i >= 8) else ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2]
        s = "....X.......X..."; k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i % 2 == 0: cym = (f"{CR}:1! " if i % 4 == 0 else f"{CR2}:1! ") + f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if name == "climax" and last: k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        if name == "climax2" and last: k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
    elif name == "adult":
        k = "o.......o......." ; s = ["..o....o.o....o.", "....o..o..o....o", "..o..o.....o..o.", "o......o.o..o..."][i % 4]
        cym = f"{RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25"
        if i >= 8: k = "X.....X...X....."; s = "....X.......X..."; s = "".join("o" if (j in (7, 14) and k[j] == ".") else c for j, c in enumerate(s))
        if last: tom = "R:2 " + tom_triplets_down(2); s = "....X..........."
    elif name == "adult2":
        k = ["X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XxXxXxXx........"][i % 4]
        s = ["........X.......", "....X.......X...", "....X.......X...", "........X.X.XXXX"][i % 4]
        h = ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", None][i % 4]
        if i % 4 == 0: cym = f"{CR2}:2! R:2"
    elif name == "youth":
        LIN = ["X..x..X...x..x..", "X.....X..x..x...", "X..x..X...x.....", "X..x....X.x..x.."]
        k = LIN[i % 4]; s = "....X.......X..."
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(16))
        if i % 4 == 0: cym = f"{CR}:1! R:3"; h = "...." + h[4:]
        if last: k, s, tom = linear_fill(kit, 2, 1); k = LIN[0][:8] + k[8:]; s = "....X..." + s[8:]; h = None
    elif name == "return":
        # いまへ戻る: キックの鼓動から、少しずつ
        k = "X.x.............X" [:16] if i < 4 else "X.x.....X.x....."
        s = None if i < 4 else "........X......."
        cym = f"{RIDE}:1, {RIDE}:1, {RIDE}:1, {RIDE}:1," if i >= 2 else None
        if last: k = "X.x.X.x.X.x.X.x."; s = "........xoxoXXXX"; cym = None
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if name == "breath" and i == 0: FX.append(bar("R:2 C4:2"))          # 逆再生のシンバル＝時間が巻き戻る
    elif name == "child" and i == 6: FX.append(bar("E4:4"))
    elif i == n - 1 and nx in ("climax2", "youth"): FX.append(bar("R:2 C4:2"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="レガートのギター（若い頃）", vol=0.11, pan=0.05))
STR = dict(reverb=0.5, attack=0.3, release=0.9, fx=[{"type": "eq", "low": 0, "mid": -1.5, "midHz": 2500, "high": 0}, {"type": "reverb", "mix": 0.25}])
song.add([part(f"弦楽合奏（{['下', '中', '上'][j]}）", "strings", J(f"s{j}"), patch="stringEnsemble", volume=0.09, pan=[-0.3, 0.3, 0][j], **STR) for j in range(3)])
song.add(part("弦楽合奏（旋律）", "strings", J("smel"), patch="stringEnsemble", volume=0.14, pan=0, phrase=8, **STR))
song.add(part("弦のピチカート", "strings", J("pizz"), patch="pizzicato", volume=0.12, pan=0.2, reverb=0.4))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-19-kokyu.json"
    song.write(out)
    check_clash(song)
