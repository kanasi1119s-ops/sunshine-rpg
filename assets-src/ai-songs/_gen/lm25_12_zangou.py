# ラウド25曲（第2シリーズ）12「塹壕の朝」（仮）。イメージ: 戦争（夜明けの塹壕）。D フリジアン・124・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: ブラス（金管の録音 VSCO 2 CE。前奏のラッパの合図と、ブリッジの金管の聖歌）
# しかけ:
#   - 前奏: スネアのロール（行進）とラッパの合図 → 全員の一撃 → 看板リフ
#   - 看板リフ: D と半音上の E♭（フリジアン）を、伸ばす音と単音で。ギターは刻まない（人間「刻みは聞きにくい」）。
#     駆け足（ギャロップ）はベースとキックが受け持つ
#   - サビ16小節: B♭ から開け、後半14小節目に C（E の長3度）、15小節目に D 長調（夜明け）で光が差す
#   - ブリッジ: 金管3本の聖歌と、行進のスネア。ソロはスウィープ
#   - 最後は D 長調の和音で終わる（朝が来る）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 124, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 4), ("chorus", 16), ("inter", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 16),
        ("bridge", 8), ("solo", 8), ("break", 4), ("chorus3", 16), ("outro", 4)]
VERSE = ["Dm", "Eb", "Dm", "Eb", "Gm", "F", "Eb", "A7"]
PRE = ["Bb", "C", "Gm7", "A7"]
CHORUS = ["Bb", "F/A", "Gm", "Dm/F", "Eb", "Bb/D", "C", "A7", "Bb", "F/A", "Gm", "Dm/F", "Ebmaj7", "C", "D", "A7sus4"]
RIFFCH = ["Dm", "Eb/D", "Dm", "Eb/D", "Dm", "C/D", "Bb", "A7"]
CH = {"intro": RIFFCH, "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": RIFFCH, "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS,
      "bridge": ["Gm", "Dm", "Eb", "Bb", "Cm", "Gm", "Eb", "A7"], "solo": ["Dm", "Eb", "Gm", "A7", "Dm", "Eb", "Bb", "A7"],
      "break": ["D5"] * 4, "chorus3": CHORUS, "outro": ["Dm", "Eb/D", "Dm", "D"]}
song = Song("塹壕の朝（仮）",
            "仮: ラウド25曲（第2シリーズ）の12曲目。イメージは戦争（夜明けの塹壕）。D フリジアン・124。スネアのロールとラッパの合図から、D と E♭ の看板リフ、"
            "駆け足はベースとキック。サビは B♭ から開け、後半で C と D 長調の夜明け。ブリッジは金管の聖歌、ソロはスウィープ。最後は D 長調。別の楽器はブラス（金管の録音）。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 夜の塹壕、ラッパの合図、突撃、そして夜明け（D 長調）。"
SECS, NB = song.secs, song.nb
song.pickups = ['V2']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"Dm": [bar("D2:1! D#2:0.5 D2:0.5 A2:1 A#2:0.5 A2:0.5"), bar("D2:1! F2:0.5 G2:0.5 A2:1 C3:0.5 A#2:0.5")],
        "Eb/D": [bar("D2:1! D#2:0.5 G2:0.5 A#2:1 A2:0.5 G2:0.5")] * 2,
        "C/D": [bar("D2:1! E2:0.5 G2:0.5 C3:1 A#2:0.5 G2:0.5")] * 2,
        "Bb": [bar("A#1:1! C2:0.5 D2:0.5 F2:1 D2:0.5 C2:0.5")] * 2,
        "A7": [bar("A1:1! A#1:0.5 C#2:0.5 E2:1 G2:0.5 E2:0.5")] * 2}
TRUMPET_CALL = [bar("D4:0.5! D4:0.25 D4:0.25 A4:1.5 D4:0.5 F4:0.5 A4:0.5"), bar("D5:2! C5:0.5 A#4:0.5 A4:1")]
TRUMPET_INTER = [R4, bar("R:2 D5:0.5! D5:0.25 D5:0.25 A4:1"), R4, bar("R:2 D#5:0.5! D5:0.25 C5:0.25 A#4:1"),
                 R4, bar("R:2 C5:0.5! C5:0.25 C5:0.25 G4:1"), R4, bar("R:2 C#5:0.5! E5:0.5 A4:1")]

VERSE_MEL = [bar("R:1 A3:0.5 D4:0.5 F4:1 D#4:0.5 D4:0.5"), bar("G4:2 A#4:1 R:1"), bar("R:0.5 F4:0.5 A4:0.5 C5:0.5 A4:1.5 F4:0.5"), bar("G4:1 D#4:1 A#3:2"),
             bar("R:1 D4:0.5 G4:0.5 A#4:1.5 A4:0.5"), bar("A4:1 C5:1 F4:2"), bar("G4:1.5 A#4:0.5 D#5:2"), bar("C#5:2 E5:1 R:1")]
VERSE2_MEL = [bar("R:0.5 D5:0.5 F5:0.5 A5:0.5 D5:1 D#5:0.5 D5:0.5"), bar("A#4:1 D#5:1 G5:1 R:1"), bar("R:0.5 A4:0.5 C5:0.5 F5:0.5 C5:1.5 A4:0.5"),
              bar("A#4:1 G4:1 D#5:2"), bar("R:1 G4:0.5 A#4:0.5 D5:1.5 C5:0.5"), bar("C5:1 F5:1 A4:2"), bar("A#4:1.5 D#5:0.5 G5:2"), bar("E5:2 C#5:1 R:1")]
PRE_MEL = [bar("D5:1 F5:1 A#4:2"), bar("E5:1 G5:1 C5:2"), bar("F5:1 A#5:1 D5:2"), bar("E5:1 C#5:1 A4:1 R:1")]
CHORUS_MEL = [bar("R:0.5 F5:0.5 A#5:0.5 C6:0.5 D6:2!"), bar("C6:1 A5:0.5 F5:0.5 A5:2"), bar("R:0.5 D5:0.5 G5:0.5 A5:0.5 A#5:2"), bar("A5:1 F5:0.5 D5:0.5 F5:2"),
              bar("R:0.5 G5:0.5 A#5:0.5 C6:0.5 D#6:2!"), bar("D6:1 C6:0.5 A#5:0.5 F5:2"), bar("E5:1 G5:1 C6:2"), bar("C#6:2 A5:1 R:1"),
              bar("R:0.5 F5:0.5 A#5:0.5 D6:0.5 C6:2!"), bar("A5:1 C6:0.5 A5:0.5 F5:2"), bar("R:0.5 A#5:0.5 A5:0.5 G5:0.5 D6:2"), bar("C6:1 A5:0.5 F5:0.5 D5:2"),
              bar("G5:1 A#5:1 D6:2"), bar("E6:2! C6:1 G5:1"), bar("F#5:1 A5:1 D6:2!"), bar("A5:2 D6:1 R:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("C6:1 F6:0.5 C6:0.5 A5:2".replace("F6", "D6"))
CHORUS2_MEL[5] = bar("D6:1 F6:0.5 D6:0.5 A#5:2".replace("F6", "D#6"))
CHORUS2_MEL[9] = bar("A5:1 F5:0.5 A5:0.5 C6:2")
CHORUS2_MEL[13] = bar("E6:1 G6:0.5 E6:0.5 C6:2".replace("G6", "D6"))
CHORUS3_MEL = [bar("D6:4!"), bar("C6:2 A5:2"), bar("A#5:4!"), bar("A5:2 F5:2")] + CHORUS_MEL[4:10] + [bar("R:0.5 D6:0.5 C6:0.5 A#5:0.5 G5:2"), CHORUS_MEL[11], bar("D#6:1 D6:1 A#5:2")] + CHORUS_MEL[13:15] + [bar("D6:4!")]

BRASS_CHORALE = {"Gm": ["A#4", "G4", "D4"], "Dm": ["A4", "F4", "D4"], "Eb": ["A#4", "G4", "D#4"], "Bb": ["D5", "A#4", "F4"],
                 "Cm": ["C5", "G4", "D#4"], "A7": ["C#5", "G4", "E4"]}
SWEEP_RANGE = {"Dm": ("D4", "A5"), "Eb": ("D#4", "A#5"), "Gm": ("D4", "G5"), "A7": ("C#4", "A5"), "Bb": ("D4", "A#5")}
SOLO = []
for j, c in enumerate(CH["solo"]):
    lo, hi = SWEEP_RANGE[c]
    if j in (3, 7): SOLO.append(bar("C#5:0.5 E5:0.5 G5:0.5 A5:0.5 C#6:2") if j == 3 else bar("A5:2^^ R:2"))
    else: SOLO.append(bar(sweep(c, lo, hi, 2), sweep(c, lo, hi, 2)) if j % 2 == 0 else bar(sweep(c, lo, hi, 2), f"{chord_tones(c, lo, hi)[-1]}:2"))

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "tp", "b0", "b1", "b2", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
ROLL = "o.o.oooxxxxXXXXX"            # スネアのロール（弱→強）
GALLOP = "X.xxX.xxX.xxX.xx"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R4
    if name in ("intro", "outro") or (name == "inter"):
        if name == "intro" and i < 2: rf = R4
        elif name == "intro" and i == 2: rf = bar("D2:4!")
        elif name == "outro" and last: rf = bar("D2:4!")
        else: rf = RIFF[ch if ch in RIFF else "Dm"][i % 2]
    elif name == "break":
        rf = bar("D2:0.75! D2:0.75! D#2:2.5!") if i < n - 1 else bar("D2:0.75! D#2:0.75! D2:0.5! R:2")
    P["riff"].append(rf)

    s = si = R4
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:2! {groot}:1! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:4!")
        elif i == 7 or (i == 15 and name != "chorus3"): s = bar(f"{groot}:2! R:2")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1")
        si = s if not (name == "chorus3" and i < 4) else R4
    elif name == "solo":
        s = bar(f"{groot}:4")
    elif name == "break":
        s = si = P["riff"][-1]
    elif name == "outro" and last:
        s = si = bar("D3:4!")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tech = tp = R4; bc = [R4, R4, R4]
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm8 = shift_oct(strip_marks(lead), -1)
        if i in (12, 13, 14): bc = [bar(f"{x}:4") for x in {"Ebmaj7": ["D5", "A#4", "G4"], "C": ["E5", "C5", "G4"], "D": ["F#5", "D5", "A4"]}[ch]]
    elif name == "solo": tech = SOLO[i]
    elif name == "intro" and i < 2: tp = TRUMPET_CALL[i]
    elif name == "inter": tp = TRUMPET_INTER[i]
    elif name == "bridge": bc = [bar(f"{x}:3.5 R:0.5") if i < n - 1 else bar(f"{x}:2 R:2") for x in BRASS_CHORALE[ch]]
    elif name == "outro" and last: bc = [bar("F#5:4!"), bar("D5:4!"), bar("A4:4!")]
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech); P["tp"].append(tp)
    for j in range(3): P[f"b{j}"].append(bc[j])

    if name in ("intro", "outro", "inter"):
        if name == "intro" and i < 2: b = R4 if i == 0 else bar("D1:4")
        elif name == "intro" and i == 2: b = bar("D1:4!")
        elif name == "outro" and last: b = bar("D1:4!")
        else:
            # 駆け足（8分＋16分2つ）で根音
            r = root; b = bar(f"{r}:0.5! {r}:0.25 {r}:0.25 {r}:0.5 {r}:0.25 {r}:0.25 {r}:0.5! {r}:0.25 {r}:0.25 {r}:0.5 {r}:0.25 {r}:0.25")
    elif name in ("verse", "verse2", "pre", "pre2", "solo"):
        b = bass_root8(ch, BEATS, nxt, lo="D1", hi="C#2") if not last else bar(f"{root}:1! {root}:1 R:2")
        if name == "verse2" and not last:
            r = root_note(ch, "D1", "C#2"); b = bar(f"{r}:0.5! {r}:0.25 {r}:0.25 {r}:0.5 {r}:0.25 {r}:0.25 {r}:0.5! {r}:0.25 {r}:0.25 {r}:0.5 {r}:0.25 {r}:0.25")
    elif name.startswith("chorus"):
        r = root_note(ch, "D1", "C#2")
        if name == "chorus3" and i < 4: b = bar(f"{r}:3! {r}:1")
        elif i == 7 or (i == 15 and name != "chorus3"): b = bar(f"{r}:1.5! {r}:0.5 R:2")
        elif name == "chorus3" and i == 15: b = bar(f"{r}:4!")
        else: b = bass_root8(ch, BEATS, nxt, lo="D1", hi="C#2")
    elif name == "bridge":
        b = bar(f"{root_note(ch, 'D1', 'C#2')}:4")
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R4
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("intro", "outro", "inter"):
        if name == "intro" and i < 2:
            s = "o.o.o.o.o.o.o.o." if i == 0 else ROLL; k = "X..............." if i == 1 else None
        elif name == "intro" and i == 2:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "outro" and last:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        else:
            k = GALLOP; s = "....X.......X..."
            k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
            if name == "inter" and i == 0: cym = f"{CHINA}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
            if last and name != "outro": k = "X.xxX.xx........"; s = "....X..." + ROLL[8:]; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 R:2"
    elif name in ("verse", "verse2"):
        # 行進: スネアのゴーストの連打と、キックは2・4の裏
        k = "X.....X.X......." if i % 2 == 0 else "X.....X...X....."
        s = "o.o.X.o.o.o.X.o." if name == "verse" else "....X.......X..."
        s = "".join("." if k[j] != "." else c for j, c in enumerate(s))
        h = None if name == "verse" else None
        cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1" if name == "verse" else None
        if name == "verse2": k = GALLOP; k = "".join("." if s[j] != "." else c for j, c in enumerate(k)); cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i == 0: cym = f"{CR2}:1! " + (f"{RIDE}:1 {RIDE}:1 {RIDE}:1" if name == "verse" else f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5")
        if last: k = "X.....X........."; s = "....X..." + ROLL[8:]; cym = None
    elif name in ("pre", "pre2"):
        k = ["X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XxXxXxXx........"][i]
        s = ["........X.......", "....X.......X...", "....X.......X...", "........" + ROLL[8:]][i]
        h = ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", None][i]
        if i == 0: cym = f"{CR2}:2! R:2"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = "X.......X.x....."; s = "........X......."
            cym = f"{CR}:2! {RIDE}:1 {RIDE}:1" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        else:
            two = 4 <= i < 6 or 12 <= i < 15
            k = GALLOP if two else ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2]
            s = "....X.......X..."
            k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
            h = None if two else "x.X.x.X.x.X.x.X."
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5" if two else None
            if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + (f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5" if two else "R:3")
            if i == 14: cym = f"{CR}:1! {CR2}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5"     # 夜明け
        if i == 7 or (i == 15 and name != "chorus3"):
            k = "X.x...X........."; s = "....X..." + ROLL[8:]; h = None; cym = None
        if name == "chorus3" and i == 15:
            k = "X..............."; s = "X..............."; h = None; cym = f"{CR}:4!"
    elif name == "bridge":
        # 金管の聖歌の下: 行進のスネア（弱いゴーストの連打）と、フロアタム
        s = "o..oo..oo..oo..o" if i < 4 else "o.ooX.ooo.ooX.oo"
        k = "X.......X......." if i >= 4 else "X..............."
        tom = "A2:1 R:3" if i < 4 else None
        if i == 0: cym = f"{CR2}:4"; tom = None
        if last: s = "....X..." + ROLL[8:]; tom = None
    elif name == "solo":
        k = "XxXxXxXxXxXxXxXx" if i < 4 else GALLOP; s = "....X.......X..."
        k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i in (0, 4): cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k = "X.x...X........."; s = "....X..." + ROLL[8:]; cym = f"{RIDE}:1 {RIDE}:1 R:2"
    elif name == "break":
        k = "X..X..X........." if i < n - 1 else "X..X..X........."
        s = "........X......." if i < n - 1 else "................"
        cym = f"{CHINA}:0.75! {CHINA}:0.75! {CHINA}:2.5!" if i < n - 1 else f"{CHINA}:0.75! {CHINA}:0.75! {CHINA}:0.5! R:2"
        if i == 0: cym = f"{CR}:0.75! {CHINA}:0.75! {CHINA}:2.5!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:2 C4:2"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:3 D4:1"))
    elif name == "intro" and i == 1: FX.append(bar("R:2 C4:2"))
    elif name == "chorus3" and i == 13: FX.append(bar("R:2 C4:2"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="スウィープのギター", vol=0.11, pan=0.05))
BR = dict(reverb=0.45, attack=0.05, release=0.5, fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 1500, "high": 0}, {"type": "reverb", "mix": 0.25}])
song.add(part("トランペット（合図）", "brass", J("tp"), patch="trumpet", volume=0.13, pan=0.15, phrase=4, **BR))
song.add([part(f"金管（{['上', '中', '下'][j]}）", "brass", J(f"b{j}"), patch="brassSection" if j < 2 else "horn", volume=0.1, pan=[-0.2, 0.2, 0][j], **BR) for j in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "wide-dark-wall"
add_layer(song, "strings", "塹壕の夜、ラッパのあとに弦が弔う。")

# 展開の型（2026-10-23 人間「展開が全曲同じ」「4分から5分」）。lm25_plans.py
from lm25_plans import apply_plan
apply_plan(song, "12")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-12-zangou.json"
    song.write(out)
    check_clash(song)
