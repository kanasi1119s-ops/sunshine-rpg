# ラウド25曲（第2シリーズ）10「成層圏の手紙」（仮）。イメージ: 空。A ミクソリディアン・132・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 馬頭琴の代わり（無料の馬頭琴の録音が見つからないため、チェロの録音を馬頭琴風に。
#   すべり＝スライド・長い音・低い弦の伸ばし＝ドローン。人間「馬頭琴もあったら入れてほしいかも」）
# しかけ:
#   - ミクソリディアン（♭7＝G）の開けた明るさ。看板リフは A のペダルの上で高い弦が鳴り続ける分散和音
#   - ベースは旋律（Aメロで歌の下をもう一本の線で動く）
#   - サビ16小節: D から開け、7小節目に ♭Ⅲ（F）で空の色が変わる。主和音 A は16小節目まで取っておく
#   - ブリッジ: 馬の駆け足（ギャロップ）のドラムに、馬頭琴風のチェロの旋律とドローン
#   - ソロはレガート（ハンマリング・プルオフの速い上り下り）。ドラムは16分のリニアのハイハット
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 132, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 4), ("chorus", 16), ("inter", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 16),
        ("bridge", 8), ("solo", 8), ("break", 4), ("chorus3", 16), ("outro", 4)]
VERSE = ["A", "G/A", "D/A", "A", "F#m7", "G", "D", "E7sus4"]
PRE = ["Bm7", "D", "Em7", "G"]
CHORUS = ["D", "A/C#", "Bm7", "G", "D", "A/C#", "F", "G", "D", "A/C#", "Bm7", "G", "Em7", "F#m7", "G", "A"]
RIFFCH = ["A", "G/A", "D/A", "A", "A", "G/A", "D/A", "E7sus4"]
CH = {"intro": RIFFCH, "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": RIFFCH, "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS,
      "bridge": ["A", "G/A", "A", "G/A", "D/A", "Em/A", "G/A", "A"], "solo": VERSE, "break": ["A5"] * 4, "chorus3": CHORUS, "outro": ["A", "G/A", "D/A", "A"]}
song = Song("成層圏の手紙（仮）",
            "仮: ラウド25曲（第2シリーズ）の10曲目。イメージは空。A ミクソリディアン・132。A のペダルの上で高い弦が鳴り続ける看板リフ、ベースは旋律、"
            "サビは D から開けて ♭Ⅲ（F）で空の色が変わる。ブリッジは馬の駆け足のドラムと馬頭琴風の旋律、ソロはレガート。別の楽器は馬頭琴の代わり（チェロの録音）。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
SECS, NB = song.secs, song.nb

RIFF = {"A": bar("A2:0.5! E3:0.5 A3:0.5 B3:0.5 C#4:0.5 B3:0.5 A3:0.5 E3:0.5"),
        "G/A": bar("A2:0.5! D3:0.5 G3:0.5 A3:0.5 B3:0.5 A3:0.5 G3:0.5 D3:0.5"),
        "D/A": bar("A2:0.5! F#3:0.5 A3:0.5 D4:0.5 C#4:0.5 A3:0.5 F#3:0.5 D3:0.5"),
        "E7sus4": bar("E2:0.5! B2:0.5 E3:0.5 A3:0.5 B3:0.5 D4:1 R:0.5")}

VERSE_MEL = [bar("R:1 E4:0.5 A4:0.5 C#5:1 B4:0.5 A4:0.5"), bar("G4:2 B4:1 D5:1"), bar("F#4:1 A4:1 D5:1.5 C#5:0.5"), bar("C#5:1 E5:1 A4:2"),
             bar("R:0.5 A4:0.5 C#5:0.5 F#5:0.5 E5:1.5 C#5:0.5"), bar("D5:1 B4:0.5 G4:0.5 B4:2"), bar("A4:1 D5:1 F#5:2"), bar("E5:1 D5:1 B4:1 R:1")]
VERSE2_MEL = [bar("R:0.5 A4:0.5 C#5:0.5 E5:0.5 A5:1 G5:0.5 E5:0.5"), bar("D5:1.5 G5:0.5 B5:2"), bar("A5:1 F#5:1 D5:1.5 E5:0.5"), bar("E5:1 C#5:1 A4:2"),
              bar("R:0.5 C#5:0.5 F#5:0.5 A5:0.5 E5:1.5 F#5:0.5"), bar("G5:1 D5:0.5 B4:0.5 D5:2"), bar("F#5:1 A5:1 D6:2"), bar("B5:1 A5:1 E5:1 R:1")]
PRE_MEL = [bar("B4:1 D5:1 F#5:2"), bar("A4:1 D5:1 F#5:1 A5:1"), bar("B4:1 E5:1 G5:2"), bar("B5:1 G5:1 D5:1 R:1")]
CHORUS_MEL = [bar("R:0.5 A4:0.5 D5:0.5 F#5:0.5 A5:2!"), bar("E5:1 C#5:0.5 E5:0.5 A5:2"), bar("R:0.5 B4:0.5 D5:0.5 F#5:0.5 B5:2"), bar("A5:1 G5:0.5 D5:0.5 G5:2"),
              bar("R:0.5 A4:0.5 D5:0.5 F#5:0.5 D6:2!"), bar("C#6:1 B5:0.5 A5:0.5 E5:2"), bar("R:0.5 C5:0.5 F5:0.5 A5:0.5 C6:2!"), bar("B5:2 D6:1 R:1"),
              bar("R:0.5 F#5:0.5 A5:0.5 D6:0.5 E6:2!"), bar("C#6:1 A5:0.5 E5:0.5 A5:2"), bar("R:0.5 D5:0.5 F#5:0.5 A5:0.5 B5:2"), bar("G5:1 B5:0.5 D6:0.5 B5:2"),
              bar("R:0.5 E5:0.5 G5:0.5 B5:0.5 D6:2"), bar("C#6:1 A5:0.5 F#5:0.5 E5:2"), bar("D5:1 G5:1 B5:2"), bar("C#6:2 A5:1 R:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("E5:1 A5:0.5 C#6:0.5 A5:2")
CHORUS2_MEL[5] = bar("C#6:1 E6:0.5 C#6:0.5 A5:2")
CHORUS2_MEL[9] = bar("C#6:1 E6:0.5 C#6:0.5 E5:2")
CHORUS2_MEL[13] = bar("C#6:1 E6:0.5 C#6:0.5 A5:2")
CHORUS3_MEL = [bar("A5:4!"), bar("E5:2 C#6:2"), bar("B5:4!"), bar("D6:2 G5:2")] + CHORUS_MEL[4:9] + [bar("E6:1 C#6:0.5 A5:0.5 E6:2")] + CHORUS_MEL[10:14] + [bar("D6:1 B5:1 G5:2"), bar("A5:4!")]

# 馬頭琴風（チェロの録音）: スライド＝">"、長い音、低い弦のドローン
MORIN = [bar("E4:1.5 F#4:0.5 A4:2"), bar("B4:1>D5 D5:1 B4:1 G4:1"), bar("A4:3 E4:1"), bar("G4:1 A4:1 B4:1>D5 D5:1"),
         bar("F#5:2 E5:1 D5:1"), bar("E5:1>G5 G5:1 E5:1 B4:1"), bar("D5:2 B4:1 G4:1"), bar("A4:4")]
MORIN_INTRO = [bar("E4:4/"), bar("A4:2>B4 B4:1 A4:1")]
MORIN_OUTRO = [bar("A4:2 B4:1 C#5:1"), bar("D5:2 B4:2"), bar("A4:4"), bar("A4:4")]

SOLO = [bar(legato_run("A", "mixolydian", "A4", "A5", 2), "C#6:2"), bar(legato_run("A", "mixolydian", "G4", "G5", 2), "B5:2"),
        bar(legato_run("A", "mixolydian", "D6", "D5", 2), "F#5:2"), bar("E5:0.5 A5:0.5 C#6:1 E6:2^^"),
        bar(legato_run("A", "mixolydian", "F#4", "F#5", 2), "A5:2"), bar(legato_run("A", "mixolydian", "G4", "G5", 2), "D6:2"),
        bar(legato_run("A", "mixolydian", "D6", "D5", 2), "A5:2"), bar("E6:2^^ R:2")]
VERSE_BASS = [bar("A1:1.5! E2:0.5 A2:1 C#3:1"), bar("A1:1 G2:1 B2:1 D3:1"), bar("A1:1.5 D2:0.5 F#2:1 A2:1"), bar("C#3:1 B2:1 A2:1 E2:1"),
              bar("F#1:1.5 C#2:0.5 E2:1 F#2:1"), bar("G1:1 D2:1 G2:1 B2:1"), bar("D2:1 F#2:1 A2:1 F#2:1"), bar("E2:1 D2:1 B1:1 A1:1")]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "morin", "drone", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R4
    if name in ("intro", "outro") or (name == "inter" and i < 4):
        if name == "intro" and i < 2: rf = bar("A2:4!") if i == 0 else R4
        elif name == "outro" and last: rf = bar("A2:4!")
        else: rf = RIFF[ch if ch in RIFF else "A"]
    elif name == "break":
        rf = bar("A2:0.75! A2:0.75! A2:2.5!") if i < n - 1 else bar("A2:0.75! G2:0.75! A2:0.5! R:2")
    P["riff"].append(rf)

    s = si = R4
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:2! {groot}:1! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:4!")
        elif i in (7,) or (i == 15 and name != "chorus3"): s = bar(f"{groot}:2! R:2")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1")
        si = s if not (name == "chorus3" and i < 4) else R4
    elif (name == "inter" and i >= 4) or name == "solo":
        s = bar(f"{groot}:4")
    elif name == "break":
        s = si = P["riff"][-1]
    elif name == "outro" and last:
        s = si = bar("A2:4!")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tech = morin = drone = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "solo": tech = SOLO[i]
    elif name == "inter" and i >= 4: tech = SOLO[i - 4] if i < 7 else bar("C#6:2 E6:2")
    elif name == "bridge": morin = MORIN[i]; drone = bar("A2:4")
    elif name == "intro" and i < 2: morin = MORIN_INTRO[i]; drone = bar("A2:4")
    elif name == "outro": morin = MORIN_OUTRO[i]; drone = bar("A2:4") if not last else bar("A2:4!")
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech); P["morin"].append(morin); P["drone"].append(drone)

    if name in ("intro", "outro") or (name == "inter" and i < 4):
        if name == "intro" and i < 2: b = bar("A1:4!") if i == 0 else bar("A1:2 A1:1 G1:1")
        elif name == "outro" and last: b = bar("A1:4!")
        else: b = bass_root8(ch, BEATS, nxt)
    elif name == "verse": b = VERSE_BASS[i]
    elif name in ("verse2", "pre", "pre2", "inter", "solo"):
        b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:3! {root}:1")
        elif i == 7 or (i == 15 and name != "chorus3"): b = bar(f"{root}:1.5! {root}:0.5 R:2")
        elif i % 4 == 3:
            # 4小節ごとに旋律ぎみの埋め（上がって次の根音へ）
            r = root; b = bar(f"{r}:0.5! {r}:0.5 {r}:0.5 {up(r, 1)}:0.5 {fifth_of(base_ch)}:0.5 {up(r, 1)}:0.5 {fifth_of(base_ch)}:0.5 {approach_note(ch, nxt)}:0.5")
        else: b = bass_root8(ch, BEATS, nxt)
    elif name == "bridge":
        b = bar("A1:0.5! A1:0.25 A1:0.25 A1:0.5 A1:0.25 A1:0.25 A1:0.5! A1:0.25 A1:0.25 A1:0.5 A1:0.25 A1:0.25")   # 駆け足
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R4
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("intro", "outro") or (name == "inter" and i < 4):
        if name == "intro" and i == 0:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "intro" and i == 1:
            k = "X.xxX.xxX.xxX..."; tom = "R:3 " + tom_16_down(1); cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 R:1"
        elif name == "outro" and last:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        else:
            k = "X.....X.X.....X." if i % 2 == 0 else "X.....X.X..X...."
            s = "....X.......X..."
            h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(16))   # リニア
            if (name == "intro" and i == 2) or (name == "inter" and i == 0) or (name == "outro" and i == 0): cym = f"{CR}:1! R:3"; h = "...." + h[4:]
            if last and name != "outro":
                k, s, tom = linear_fill(kit, 2, i); k = "X.....X." + k[8:]; s = "....X..." + s[8:]; h = "..o.x.o........."
    elif name in ("verse", "verse2"):
        k = ["X.....X...X.....", "X..x......X..x..", "X.....X...X..x..", "X..x....X.x....."][i % 4]
        s = "....X.......X..."
        s = "".join("o" if (j in (7, 15) and k[j] == ".") else c for j, c in enumerate(s))
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(16))
        if name == "verse2": h = None; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"
        if i == 0: cym = f"{CR2}:1! " + (f"{RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5" if name == "verse2" else "R:3"); h = ("...." + h[4:]) if h else None
        if last:
            k, s, tom = linear_fill(kit, 2, 2); k = "X.....X." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
    elif name in ("pre", "pre2"):
        k = ["X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XxXxXxXxXxXx...."][i]
        s = ["........X.......", "....X.......X...", "....X.......X...", "..X...X...X....."][i]
        h = ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", None][i]
        if i == 0: cym = f"{CR2}:2! R:2"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! R:1"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = "X.......X.x....."; s = "........X......."
            cym = f"{CR}:2! {RIDE}:1 {RIDE}:1" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        else:
            k = ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2]
            s = "....X.......X..." if i % 4 != 3 else "....X.......X.oo"
            h = "O.x.O.x.O.x.O.x." if i % 8 < 4 else "x.X.x.X.x.X.x.X."
            if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + "R:3"; h = "..x." + h[4:]
            if i == 6: cym = f"{CHINA}:1! R:3"; h = "..x." + h[4:]
            if name == "chorus2" and i in (12, 13): k = "XxXxXxXxXxXxXxXx"; h = None; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i == 7 or (i == 15 and name != "chorus3"):
            k = "X.x...X........."; s = "....X..........."; h = None; tom = "R:2 " + tom_16_down(2); cym = None
        if name == "chorus3" and i == 15:
            k = "X..............."; s = "X..............."; h = None; cym = f"{CR}:4!"; tom = None
    elif (name == "inter" and i >= 4) or name == "solo":
        k = "XxXxXxXxXxXxXxXx"; s = "....X.......X..."
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i in (0, 4): cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k = "X.x...X........."; s = "....X..........."; tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 R:2"
    elif name == "bridge":
        # 馬の駆け足（ギャロップ: 8分＋16分2つ）をキックとフロアタムで
        k = "X.XXX.XXX.XXX.XX" if i >= 4 else "X.X.X.X.X.X.X.X."
        s = "........X......." if i < 4 else "....X.......X..."
        cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1" if i < 4 else f"{RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {BELL}:0.5"
        if i == 0: cym = f"{CR2}:2 {RIDE}:1 {RIDE}:1"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 R:2"; k = "X.XXX.XX........"; s = None
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
    elif name == "chorus3" and i == 3: FX.append(bar("R:2 C4:2"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="レガートのギター", vol=0.11, pan=0.05))
MORIN_FX = [{"type": "eq", "low": -1, "mid": 2.5, "midHz": 1200, "high": 0.5}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}, {"type": "reverb", "mix": 0.3}]
song.add(part("馬頭琴の代わり（チェロの録音）", "strings", J("morin"), patch="cello", volume=0.19, pan=-0.12, reverb=0.5, attack=0.12, release=0.7, phrase=8, fx=MORIN_FX))
song.add(part("馬頭琴の代わり（低い弦のドローン）", "strings", J("drone"), patch="cello", volume=0.08, pan=-0.12, reverb=0.5, attack=0.3, release=0.9, fx=MORIN_FX))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-10-seisouken.json"
    song.write(out)
    check_clash(song)
