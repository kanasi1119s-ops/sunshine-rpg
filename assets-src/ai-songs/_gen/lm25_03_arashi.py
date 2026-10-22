# ラウド25曲（第2シリーズ）03「嵐の背骨」（仮）。イメージ: 嵐。D 自然的短音階・138・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: チェロ（嵐のうなり＝低いトレモロ、目の中の静けさ＝ブリッジの旋律）
# しかけ:
#   - 曲の頭: 全員の一撃 → タムの16分の雷鳴 → 開放 D のペダルが波のように上下する看板リフ（刻みではなく8分の単音）
#   - Bメロで ♭II（E♭）を一瞬見せ、サビは B♭ → F/A → Gm と下りる低音。サビ13小節目に E♭ で光を差す
#   - 間奏とソロはスウィープ（和音の音を1本ずつ）。ブリッジは嵐の目: チェロの旋律とクリーンの分散和音だけ
#   - ドラム: Bメロは16分のタム回し、サビの後半だけツーバス、ソロの前半はツーバスの16分
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 138, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 8), ("chorus", 16), ("inter", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 16),
        ("bridge", 8), ("solo", 8), ("break", 4), ("chorus3", 16), ("outro", 4)]
VERSE = ["Dm", "Dm", "C/D", "C/D", "Bb", "Bb", "A7", "A7"]
PRE = ["Gm", "Gm", "Bb", "Bb", "Eb", "Eb", "A7sus4", "A7"]
CHORUS = ["Bb", "Bb", "F/A", "F/A", "Gm", "Gm", "Dm", "Dm", "Bb", "Bb", "C", "C", "Eb", "Ebmaj7", "A7", "A7"]
CH = {"intro": ["Dm"] * 6 + ["Bb", "C"], "verse": VERSE, "pre": PRE, "chorus": CHORUS,
      "inter": ["Dm", "Dm", "Bb", "C", "Dm", "Dm", "Gm", "A7"], "verse2": VERSE, "pre2": PRE[4:], "chorus2": CHORUS,
      "bridge": ["Bbmaj7", "Am7", "Gm7", "Dm", "Bbmaj7", "Am7", "Gm7", "A7sus4"],
      "solo": ["Dm", "Bb", "Gm", "A7", "Dm", "Bb", "Eb", "A7"], "break": ["D5"] * 4, "chorus3": CHORUS, "outro": ["Dm", "Dm", "Bb", "D5"]}
song = Song("嵐の背骨（仮）",
            "仮: ラウド25曲（第2シリーズ）の3曲目。イメージは嵐。D 自然的短音階・138。開放 D のペダルが波のように上下する看板リフ、サビは B♭→F/A→Gm と下りる低音と ♭II の光。"
            "間奏とソロはスウィープ、ブリッジは嵐の目（チェロの旋律）。別の楽器はチェロ。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
SECS, NB = song.secs, song.nb

RIFF = {
    "Dm": [bar("D2:0.5! D3:0.5 D2:0.5 C3:0.5 D2:0.5! A2:0.5 A#2:0.5 A2:0.5"), bar("D2:0.5! D3:0.5 D2:0.5 F3:0.5 E3:0.5 D3:0.5 A2:0.5 C3:0.5")],
    "Bb": [bar("A#1:0.5! A#2:0.5 A#1:0.5 A2:0.5 A#1:0.5! F2:0.5 G2:0.5 F2:0.5")] * 2,
    "C": [bar("C2:0.5! C3:0.5 C2:0.5 A#2:0.5 C2:0.5! G2:0.5 A2:0.5 G2:0.5")] * 2,
    "Gm": [bar("G1:0.5! G2:0.5 G1:0.5 F2:0.5 G1:0.5! D2:0.5 D#2:0.5 D2:0.5")] * 2,
    "A7": [bar("A1:0.5! A2:0.5 A1:0.5 G2:0.5 A1:0.5! C#3:0.5 E3:0.5 C#3:0.5")] * 2,
}

VERSE_MEL = [bar("R:0.5 D4:0.5 F4:0.5 A4:0.5 D5:1.5 C5:0.5"), bar("A4:2 R:1 F4:0.5 G4:0.5"),
             bar("E4:1 G4:1 C5:1.5 A#4:0.5"), bar("G4:2 R:2"),
             bar("R:0.5 F4:0.5 A#4:0.5 D5:0.5 F5:1.5 D5:0.5"), bar("C5:1 A#4:1 F4:2"),
             bar("E4:1 G4:1 C#5:1.5 E5:0.5"), bar("C#5:2 R:2")]
VERSE2_MEL = [bar("R:0.5 A4:0.5 D5:0.5 F5:0.5 A5:1.5 G5:0.5"), bar("F5:1 E5:0.5 D5:0.5 A4:1 R:1"),
              bar("E5:1 G5:1 C6:1.5 A#5:0.5"), bar("G5:1 E5:1 C5:1 R:1"),
              bar("R:0.5 F5:0.5 A#5:0.5 D6:0.5 C6:1.5 A#5:0.5"), bar("C6:1 A#5:1 F5:2"),
              bar("E5:1 G5:1 A5:1.5 C#6:0.5"), bar("C#6:1 A5:1 R:2")]
PRE_MEL = [bar("D5:1 A#4:0.5 G4:0.5 D5:2"), bar("R:2 G4:0.5 A4:0.5 A#4:1"), bar("F5:1 D5:0.5 A#4:0.5 F5:2"), bar("R:2 A#4:0.5 C5:0.5 D5:1"),
           bar("G5:1 D#5:0.5 A#4:0.5 G5:2"), bar("R:2 A#4:0.5 D5:0.5 D#5:1"), bar("D5:2 E5:2"), bar("C#5:1 E5:1 R:2")]
CHORUS_MEL = [bar("R:0.5 F5:0.5 A#5:0.5 C6:0.5 D6:2!"), bar("C6:1 A#5:1 F5:2"),
              bar("R:0.5 E5:0.5 F5:0.5 A5:0.5 C6:2"), bar("A5:1 G5:1 F5:2"),
              bar("R:0.5 D5:0.5 G5:0.5 A#5:0.5 D6:2!"), bar("C6:1 A#5:1 G5:2"),
              bar("A5:3 F5:1"), bar("D5:2 R:2"),
              bar("R:0.5 F5:0.5 A#5:0.5 C6:0.5 D6:2!"), bar("C6:1 A#5:1 F5:2"),
              bar("R:0.5 E5:0.5 G5:0.5 C6:0.5 E6:2!"), bar("D6:1 C6:1 G5:2"),
              bar("G5:1.5 A#5:0.5 D#6:2!"), bar("D6:1 A#5:1 G5:2"),
              bar("E5:1 G5:1 A5:1.5 C#6:0.5"), bar("C#6:2 R:2")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("C6:1 D6:1 A#5:2")
CHORUS2_MEL[9] = bar("C6:0.5 D6:0.5 C6:0.5 A#5:0.5 F5:2")
CHORUS2_MEL[5] = bar("C6:0.5 D6:0.5 C6:0.5 A#5:0.5 G5:2")
CHORUS2_MEL[13] = bar("G5:1 A#5:1 D6:2")
CHORUS2_MEL[14] = bar("C#6:1 A5:1 E5:1.5 G5:0.5")
CHORUS3_MEL = [bar("D6:4!"), bar("C6:2 A#5:2"), bar("C6:4!"), bar("A5:2 F5:2")] + CHORUS_MEL[4:6] + [bar("A5:2 D6:2"), CHORUS_MEL[7]] + \
    [bar("D6:1 C6:0.5 A#5:0.5 D6:2!"), bar("F5:1 A#5:1 D6:2"), bar("R:0.5 G5:0.5 C6:0.5 D6:0.5 E6:2!"), bar("E6:1 D6:1 C6:2")] + CHORUS_MEL[12:14] + [bar("E5:0.5 G5:0.5 A5:0.5 C#6:0.5 E6:2!"), CHORUS_MEL[15]]

CELLO_BRIDGE = [bar("D4:2 F4:1 A4:1"), bar("G4:3 E4:1"), bar("F4:2 D4:1 A#3:1"), bar("A3:4"),
                bar("D4:1 F4:1 A4:1 C5:1"), bar("C5:3 A4:1"), bar("A#4:2 G4:1 F4:1"), bar("E4:2 D4:2")]
# サビ3の後半: チェロの対旋律（2分音符で下りる）
CELLO_C3 = {8: bar("D3:2 F3:2"), 9: bar("D3:2 C3:2"), 10: bar("E3:2 G3:2"), 11: bar("E3:2 C3:2"),
            12: bar("D#3:2 G3:2"), 13: bar("A#3:2 G3:2"), 14: bar("E3:2 G3:2"), 15: bar("C#3:4")}


def sweep_bar(ch, lo, hi, plan):
    """plan: 2拍ずつの指定（'s'=スウィープ・それ以外は音符の列）"""
    out = []
    for p in plan:
        out.append(sweep(ch, lo, hi, 2) if p == "s" else p)
    return bar(*out)


SOLO = [
    sweep_bar("Dm", "D4", "A5", ["s", "s"]),
    sweep_bar("Bb", "D4", "A#5", ["s", "A#5:2"]),
    sweep_bar("Gm", "D4", "G5", ["s", "s"]),
    bar("E5:0.5 F5:0.5 G5:0.5 A5:0.5 C#6:2"),
    sweep_bar("Dm", "F4", "D6", ["s", "s"]),
    sweep_bar("Bb", "F4", "D6", ["s", "D6:2"]),
    sweep_bar("Eb", "G4", "D#6", ["s", "s"]),
    bar("G5:2^^ R:2"),
]
INTER_SWEEP = {4: sweep_bar("Dm", "D4", "A5", ["s", "s"]), 5: sweep_bar("Dm", "F4", "D6", ["s", "D6:2"]),
               6: sweep_bar("Gm", "D4", "G5", ["s", "s"]), 7: bar("C#5:0.5 E5:0.5 G5:0.5 A5:0.5 C#6:2")}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm", "tech", "cello", "clean", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
HH8 = "X.x.x.x.X.x.x.x."
HH16 = "XxxxXxxxXxxxXxxx"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch, "D1", "C#2")
    groot = up(root, 1)

    # ----- リフ -----
    rf = R4
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0: rf = bar("D2:4!")
        elif name == "intro" and i == 1: rf = R4
        elif name == "outro" and last: rf = bar("D2:4!")
        else:
            key = {"Dm": "Dm", "Bb": "Bb", "C": "C", "Gm": "Gm", "A7": "A7"}[base_ch]
            rf = RIFF[key][i % 2]
            if name == "inter" and i >= 4: rf = R4 if i < 7 else bar("A1:2! R:2")
    elif name == "break":
        rf = bar("D2:1.5! D2:1.5! D2:1!") if i < n - 1 else bar("D2:1.5! D2:0.5! R:2")
    P["riff"].append(rf)

    # ----- リズムギター -----
    s = si = R4
    if name in ("verse", "verse2"):
        s = bar(f"{groot}:4") if i % 2 == 0 else bar(f"{groot}:2 {groot}:2")
        if last: s = bar(f"{groot}:2! R:2")
        if name == "verse2": si = s
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1") if not last else bar(f"{groot}:1! {groot}:1! R:2")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:4!")
        elif last and name != "chorus3": s = bar(f"{groot}:2! R:2")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1")
        si = s if not (name == "chorus3" and i < 4) else R4
    elif name == "solo":
        s = bar(f"{groot}:4")
    elif name == "inter" and i >= 4:
        s = bar(f"{groot}:4") if i < 7 else bar(f"{groot}:2! R:2")
    elif name == "break":
        s = si = P["riff"][-1]
    P["rhy"].append(s); P["rhy_in"].append(si)

    # ----- 旋律・技・チェロ -----
    lead = harm = tech = cello = clean = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name == "pre": lead = PRE_MEL[i]
    elif name == "pre2": lead = PRE_MEL[4 + i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]; cello = CELLO_C3.get(i, R4)
        if i >= 4: harm = shift_oct(strip_marks(lead), -1)
    elif name == "solo": tech = SOLO[i]
    elif name == "inter": tech = INTER_SWEEP.get(i, R4)
    elif name == "bridge":
        cello = CELLO_BRIDGE[i]
        t = chord_tones(base_ch, "D3", "D5")
        pat = [0, 2, 4, 2, 1, 3, 5, 3]
        clean = bar(*[f"{t[j % len(t)]}:0.5" for j in pat])
    elif name == "intro" and i < 2:
        cello = bar(" ".join(["D2:0.25" + ("!" if k % 4 == 0 else ",") for k in range(16)]))   # 嵐のうなり（トレモロ）
    P["lead"].append(lead); P["harm"].append(harm); P["tech"].append(tech); P["cello"].append(cello); P["clean"].append(clean)

    # ----- ベース（コードに沿う8分） -----
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0: b = bar("D1:4!")
        elif name == "intro" and i == 1: b = bar("D1:4")
        elif name == "outro" and last: b = bar("D1:4!")
        elif name == "inter" and i >= 4: b = bass_root8(ch, BEATS, nxt, lo="D1", hi="C#2") if i < 7 else bar("A1:2! R:2")
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("verse", "verse2", "pre", "pre2", "solo"):
        b = bass_root8(ch, BEATS, nxt, lo="D1", hi="C#2") if not last else bar(f"{root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5 {root}:1! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:3! {root}:1")
        elif last and name != "chorus3": b = bar(f"{root}:1.5! {root}:0.5 R:2")
        else: b = bass_root8(ch, BEATS, nxt, lo="D1", hi="C#2")
    elif name == "bridge":
        b = bar(f"{root}:4") if i % 2 == 0 else bar(f"{root}:2 {fifth_of(base_ch, 'D1', 'C#2')}:2")
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R4
    P["bass"].append(b)

    # ----- ドラム -----
    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "intro" and i == 1:
            tom = " ".join(f"{['A2', 'A2', 'D3', 'A2'][j % 4]}:0.25{'!' if j % 4 == 0 else ','}" for j in range(12)) + " " + tom_16_down(1)
            k = "X...X...X...XXXX"
        elif name == "outro" and last:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "inter" and i >= 4:
            # スウィープの下: ツーバスの16分＋スネア2・4、ライド
            k = "XxXxXxXxXxXxXxXx"; s = "....X.......X..."
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"
            if i == 4: cym = f"{CHINA}:1! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"
            if last: k, s, tom = linear_fill(kit, 2, 1); k = "X.X.X.X." + k[8:]; s = "....X..." + s[8:]; cym = f"{RIDE}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:2"
        else:
            # 波のリフ: ペダルの所にキック、2・4にスネア、8分のハイハット（強弱）
            k = "X...X.x.X...X.x." if i % 2 == 0 else "X...X.x.X.x.X..."
            s = "....X.......X..."
            h = HH8
            if (name == "intro" and i == 2) or (name == "inter" and i == 0): cym = f"{CR}:1! R:3"; h = "..x.x.x.X.x.x.x."
            if name == "intro" and last:
                k, s, tom = linear_fill(kit, 2, 0); k = "X...X.x." + k[8:]; s = "....X..." + s[8:]; h = "x.x.x.x........."
    elif name in ("verse", "verse2"):
        k = ["X.....X.X.......", "X.x...X...X.....", "X.....X.X..x....", "X.x.....X.x....."][i % 4]
        s = "....X.......X..."; s = "".join("o" if (j in (7, 14) and k[j] == ".") else c for j, c in enumerate(s))
        h = "".join("." if s[j] == "X" else ("X" if j % 4 == 0 else ("x" if j % 2 == 0 else "o")) for j in range(16))
        if name == "verse2": h = None; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 " * 2; cym = cym.strip()
        if i == 0: cym = f"{CR2}:1! " + (f"{RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5" if name == "verse2" else "R:3")
        if last:
            k = "X.x...X........."; s = "....X..........."; h = None; tom = "R:2 " + tom_triplets_down(2)
            cym = f"{RIDE}:1! {RIDE}:1 R:2" if name == "verse2" else None
    elif name in ("pre", "pre2"):
        # 16分のタム回し: フロアとスネアで16分のうねり、キックは4分
        k = "X...X...X...X..."
        s = "....X.......X..."
        tom = " ".join(f"{['A2', 'D3', 'A2', 'F3'][j % 4]}:0.25{'!' if j % 8 == 0 else ''}" for j in range(4)) + " R:0.25 " + \
              " ".join(f"{['D3', 'A2', 'D3'][j % 3]}:0.25" for j in range(3)) + " " + \
              " ".join(f"{['A2', 'D3', 'A2', 'F3'][j % 4]}:0.25" for j in range(4)) + " R:0.25 " + " ".join(f"{['D3', 'A2', 'D3'][j % 3]}:0.25" for j in range(3))
        if i == 0: cym = f"{CR2}:1! R:3"
        if last:
            k = "XXXXXXXXXXXX...."; s = "................"; tom = "R:3 " + tom_16_down(1)[:-1] if False else "R:3 A2:0.25! A2:0.25! A2:0.25! A2:0.25!"
            cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! R:1"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = "X.......X.x....."; s = "........X......."
            cym = f"{CR}:2! {RIDE}:1 {RIDE}:1" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        else:
            two = i in (8, 9, 10, 11) or (name == "chorus2" and i in (12, 13))
            k = "XxXxXxXxXxXxXxXx" if two else ["X.X...X.X.X...X.", "X.X...X.X...X.X."][i % 2]
            s = "....X.......X..."
            h = None if two else "x.X.x.X.x.X.x.X."
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5" if two else None
            if i % 4 == 0:
                c0 = f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! "
                cym = c0 + (f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5" if two else "R:3")
            if i == 12: cym = f"{CHINA}:1! {CR2}:1! R:2"
            if i % 8 == 7 and not last:
                k = "X.X...X........."; s = "....X..........."; h = None; tom = "R:2 " + tom_16_down(2)
                cym = f"{RIDE}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:2" if two else None
        if last and name != "chorus3":
            k = "X.X...X........."; s = "....X..........."; h = None; tom = "R:2 " + tom_triplets_down(2)
            cym = None
        if name == "chorus3" and last:
            k = "X.X...X.X.X...X."; s = "....X.......X..."; h = None; cym = f"{CR}:1! {RIDE}:1 {RIDE}:1 {RIDE}:1"
    elif name == "bridge":
        # 嵐の目: ライドとフロアタム、キックは小さく
        k = "X.......o......." if i % 2 == 0 else "X.....o........."
        s = "................" if i < 4 else "........o......."
        cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1" if i < 4 else f"{BELL}:1! {RIDE}:1 {RIDE}:1 {RIDE}:1"
        tom = "R:3 A2:1," if i % 2 == 1 else None
        if i == 0: cym = f"{CR2}:2 {RIDE}:1 {RIDE}:1"
        if last: tom = "R:1 " + tom_triplets_down(2) + " R:1"; cym = f"{RIDE}:1 R:3"
    elif name == "solo":
        if i < 4:
            k = "XxXxXxXxXxXxXxXx"; s = "....X.......X..."
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
            if i == 0: cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        else:
            # 後半は5つずつのかたまり（16分5つ）で小節線をまたぐ
            off = (i - 4) * 16
            k = "".join("X" if (off + j) % 5 == 0 else "." for j in range(16))
            s = "".join("X" if (off + j) % 5 == 3 else "." for j in range(16))
            h = "".join("x" if (k[j] == "." and s[j] == "." and j % 2 == 0) else "." for j in range(16))
            if i == 4: cym = f"{CR2}:1! R:3"; h = "...." + h[4:]
        if last:
            k = "X..............."; s = "................"; h = None; tom = "R:1 " + tom_triplets_down(2) + " R:1"; cym = None
    elif name == "break":
        k = "X.....X.....X..." if i < n - 1 else "X.....X........."
        s = "........X......." if i < n - 1 else "................"
        cym = f"{CHINA}:1.5! {CHINA}:1.5! {CHINA}:1!" if i < n - 1 else f"{CHINA}:1.5! {CHINA}:0.5! R:2"
        if i == 0: cym = f"{CR}:1.5! {CHINA}:1.5! {CHINA}:1!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if name == "intro" and i == 0: FX.append(R4)
    elif name == "intro" and i == 1: FX.append(bar("R:1 E4:3"))          # 雷鳴の前のスウェル
    elif i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:2 C4:2"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:3 D4:1"))
    elif name == "outro" and i == n - 1: FX.append(bar("R:1 B4:3"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="スウィープのギター", vol=0.11, pan=0.05))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの分散和音"))
song.add(part("チェロ", "strings", J("cello"), patch="cello", volume=0.18, pan=-0.2, reverb=0.45, attack=0.1, release=0.6, phrase=8,
              fx=[{"type": "eq", "low": 1, "mid": -1.5, "midHz": 2500, "high": 0}, {"type": "reverb", "mix": 0.2}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-03-arashi.json"
    song.write(out)
    check_clash(song)
