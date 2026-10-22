# ラウド25曲（第2シリーズ）13「闇市の値札」（仮）。イメージ: 闇市（値切りと裏取引）。B♭ 短調・108・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: バリトンサックス（低いうなり。リフのユニゾン、間奏の掛け合い、ブリッジの独奏）
# しかけ:
#   - 看板リフ: 16分の休みとシンコペーションで「値札をめくる」ような単音（♭5＝E のブルーノートが一瞬）。ギターとバリトンサックスのユニゾン
#   - ベースはスラップ（Aメロ・間奏）と、ブリッジのジャズのウォーキング
#   - ドラム: ゴーストノートの多い16分のノリ（ファンク寄りのプログレ）。区間の終わりはリニアのフィル
#   - サビ: G♭maj7 から開け、7小節目に ♭Ⅱ（B＝C♭）で一瞬だけ表通りの光、F7 で引き戻す
#   - ブリッジ: E♭m7 → A♭7 → D♭maj7 のジャズ。バリトンサックスの独奏
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 108, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 4), ("chorus", 8), ("inter", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 8),
        ("bridge", 8), ("solo", 8), ("break", 4), ("chorus3", 12), ("outro", 4)]
VERSE = ["Bbm7", "Eb9", "Bbm7", "Eb9", "Gbmaj7", "F7", "Bbm7", "F7#9"]
PRE = ["Ebm7", "Ab7", "Dbmaj7", "F7sus4"]
CHORUS = ["Gbmaj7", "Ab", "Fm7", "Bbm7", "Gbmaj7", "Ab", "B", "F7"]
RIFFCH = ["Bbm7", "Bbm7", "Eb9", "Bbm7", "Gb7", "F7#9", "Bbm7", "F7#9"]
CH = {"intro": RIFFCH, "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": RIFFCH, "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS,
      "bridge": ["Ebm7", "Ab7", "Dbmaj7", "Gbmaj7", "Cm7b5", "F7", "Bbm7", "F7"], "solo": VERSE, "break": ["Bb5"] * 4,
      "chorus3": CHORUS + ["Gbmaj7", "Ab", "Fm7", "Bbm7"], "outro": ["Bbm7", "Eb9", "Bbm7", "Bbm7"]}
song = Song("闇市の値札（仮）",
            "仮: ラウド25曲（第2シリーズ）の13曲目。イメージは闇市（値切りと裏取引）。B♭ 短調・108。16分の休みとシンコペーションの看板リフをギターとバリトンサックスで、"
            "ベースはスラップとジャズのウォーキング、ドラムはゴーストノートの多いノリ。サビは G♭maj7 から開け、♭Ⅱ（B）で一瞬表通りの光。別の楽器はバリトンサックス。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 闇市で値札をめぐる駆け引き。売り手（サックス）と買い手（ベース）が言い合う。"
SECS, NB = song.secs, song.nb
song.pickups = ['V5', 'V1']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"Bbm7": [bar("A#2:0.5! R:0.25 A#2:0.25 C#3:0.5 D#3:0.25 E3:0.25 F3:0.5 R:0.5 G#3:0.25 F3:0.25 A#3:0.5"),
                 bar("A#2:0.5! R:0.25 A#2:0.25 C#3:0.5 D#3:0.25 F3:0.25 G#3:0.5 F3:0.5 D#3:0.25 C#3:0.25 A#2:0.5")],
        "Eb9": [bar("D#2:0.5! R:0.25 D#2:0.25 G2:0.5 A#2:0.25 C#3:0.25 F3:0.5 R:0.5 C#3:0.25 A#2:0.25 G2:0.5")] * 2,
        "Gb7": [bar("F#2:0.5! R:0.25 F#2:0.25 A#2:0.5 C#3:0.25 E3:0.25 F#3:0.5 R:0.5 E3:0.25 C#3:0.25 A#2:0.5")] * 2,
        "F7#9": [bar("F2:0.5! R:0.25 F2:0.25 A2:0.5 C3:0.25 D#3:0.25 G#3:0.5 R:0.5 A3:0.25 G#3:0.25 F3:0.5")] * 2}

VERSE_MEL = [bar("R:0.5 F4:0.5 G#4:0.5 A#4:0.5 C#5:1 A#4:1"), bar("C#5:0.5 C5:0.5 A#4:1 G4:2"), bar("R:1 G#4:0.5 F4:0.5 C#4:1 F4:1"), bar("G4:2 F4:1 R:1"),
             bar("R:0.5 A#4:0.5 C#5:0.5 F5:0.5 D#5:1.5 C#5:0.5"), bar("C5:1 A4:1 D#5:2"), bar("C#5:1.5 C5:0.5 A#4:1 F4:1"), bar("G#4:1 A4:1 R:2")]
VERSE2_MEL = [bar("R:0.5 A#4:0.5 C#5:0.5 F5:0.5 G#5:1 F5:1"), bar("F5:0.5 D#5:0.5 C#5:1 A#4:2"), bar("R:1 C#5:0.5 A#4:0.5 F4:1 G#4:1"), bar("A#4:2 G4:1 R:1"),
              bar("R:0.5 C#5:0.5 F5:0.5 A#5:0.5 G#5:1.5 F5:0.5"), bar("F5:1 C5:1 A5:2"), bar("G#5:1.5 F5:0.5 C#5:1 A#4:1"), bar("G#4:1 A4:1 R:2")]
PRE_MEL = [bar("F#4:1 A#4:1 C#5:2"), bar("C5:1 D#5:1 F#5:2"), bar("F5:1 G#5:1 C5:2"), bar("A#5:1 F5:1 C5:1 R:1")]
CHORUS_MEL = [bar("R:0.5 C#5:0.5 F5:0.5 G#5:0.5 A#5:2!"), bar("G#5:1 D#5:0.5 C5:0.5 D#5:2"), bar("R:0.5 C5:0.5 D#5:0.5 G#5:0.5 C6:2"), bar("A#5:1 F5:0.5 C#5:0.5 F5:2"),
              bar("R:0.5 C#5:0.5 F5:0.5 A#5:0.5 C#6:2!"), bar("C6:1 G#5:0.5 D#5:0.5 G#5:2"), bar("R:0.5 B4:0.5 D#5:0.5 F#5:0.5 B5:2!"), bar("A5:1 C6:1 D#6:1 R:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("G#5:1 C6:0.5 G#5:0.5 D#5:2")
CHORUS2_MEL[5] = bar("C6:1 D#6:0.5 C6:0.5 G#5:2")
CHORUS3_MEL = [bar("A#5:4!"), bar("G#5:2 D#5:2"), bar("C6:4!"), bar("A#5:2 F5:2")] + CHORUS_MEL[4:8] + \
    [bar("R:0.5 F5:0.5 A#5:0.5 C#6:0.5 D#6:2!"), bar("C6:1 G#5:0.5 D#5:0.5 C6:2"), bar("G#5:1 C6:1 D#6:2"), bar("C#6:2 A#5:2!")]

SAX_BRIDGE = [bar("F#3:0.5 A#3:0.5 C#4:0.5 D#4:0.5 F4:1.5 C#4:0.5"), bar("C4:1 D#4:0.5 F#4:0.5 F4:2"), bar("F4:1.5 D#4:0.5 C4:1 G#3:1"), bar("A#3:2 C#4:1 F4:1"),
              bar("D#4:1 F#4:1 C4:2"), bar("A3:1 C4:1 D#4:2"), bar("C#4:1.5 C4:0.5 A#3:1 F3:1"), bar("A3:2 R:2")]
SAX_V2 = [R4, bar("R:2 G3:0.5 A#3:0.5 C#4:1"), R4, bar("R:2 F3:0.5 G3:0.5 A#3:1"), R4, bar("R:2 A3:0.5 C4:0.5 D#4:1"), R4, bar("R:2 G#3:0.5 A3:0.5 C4:1")]
SOLO = [bar("F5:0.5 G#5:0.5 A#5:3^^"), bar("C#6:1 A#5:0.5 G5:0.5 F5:2"), bar("R:0.5 C#5:0.5 F5:0.5 G#5:0.5 A#5:2"), bar("G5:2^^ R:2"),
        bar("F5:0.5 A#5:0.5 C#6:1 D#6:2"), bar("C6:1 A5:1 F5:2"), bar("A#5:1.5 G#5:0.5 F5:1 C#5:1"), bar("A4:1 C5:1 D#5:1 G#5:1")]
SLAP = ["T..gP.T.gTP.T.gP", "T.gP..TgP.T.gPT.", "T..gP.TgS.P.T.gP", "T.gPT.gP.TgP.T.g"]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "sax", "bass", "pop", "mute"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"


def split_slap(b):
    pt, mt = [], []
    for t in b.split():
        if t.endswith("'"): pt.append(t); mt.append("R:" + t.split(":")[1].rstrip("'"))
        else: pt.append("R:" + t.split(":")[1].rstrip("!'")); mt.append(t)
    return merge_rests(" ".join(mt)), merge_rests(" ".join(pt))


def walk4(ch, nxt):
    r = root_note(ch)
    rr, q, _ = parse_chord(ch)
    mode = {"7": "mixolydian", "m7": "dorian", "m7b5": "locrian", "maj7": "ionian", "9": "mixolydian"}.get(q, "aeolian")
    sc = scale_notes(rr, mode, r, up(r, 1), flat="b" in rr)
    tones = chord_tones(ch, r, up(r, 1))
    return bar(f"{r}:1! {sc[1] if len(sc) > 1 else tones[1]}:1 {tones[1]}:1 {approach_note(ch, nxt)}:1")


for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R4
    if name in ("intro", "outro") or (name == "inter" and i >= 4):
        if name == "intro" and i == 0: rf = bar("A#2:0.5! R:3.5")
        elif name == "outro" and last: rf = bar("A#2:4!")
        else:
            rf = RIFF[ch if ch in RIFF else "Bbm7"][i % 2]
    elif name == "break":
        rf = bar("A#2:0.5! R:0.25 A#2:0.25 A#2:0.5! R:0.5 B2:2!") if i < n - 1 else bar("A#2:0.5! R:0.25 A#2:0.25 B2:1! R:2")
    P["riff"].append(rf)

    s = si = R4
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"R:0.5 {groot}:1.5 R:0.5 {groot}:1.5") if not last else bar(f"{groot}:2! R:2")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:2! {groot}:1! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:4!")
        elif last and name != "chorus3": s = bar(f"{groot}:2! R:2")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1")
        si = s if not (name == "chorus3" and i < 4) else R4
    elif name == "solo":
        s = bar(f"{groot}:4")
    elif name == "break":
        s = si = P["riff"][-1]
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = sax = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]; sax = SAX_V2[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "solo": lead = SOLO[i]
    elif name == "bridge": sax = SAX_BRIDGE[i]
    if name in ("intro", "outro") or (name == "inter" and i >= 4):
        sax = P["riff"][-1] if not (name == "outro" and last) else bar("A#2:4!")
    elif name == "inter" and i < 4:
        sax = [bar("R:2 A#2:0.5! C#3:0.5 F3:1"), bar("R:2 G#2:0.5 F2:0.5 A#2:1"), bar("R:2 C#3:0.5! D#3:0.5 G3:1"), bar("R:2 F3:0.5 E3:0.5 D#3:1")][i]
    P["lead"].append(lead); P["harm8"].append(harm8); P["sax"].append(sax)

    pop = mute = R4
    if name in ("intro", "outro") or (name == "inter" and i >= 4):
        if name == "intro" and i == 0: b = bar("A#1:0.5! R:3.5")
        elif name == "outro" and last: b = bar("A#1:4!")
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("verse", "inter") and not last:
        b, mute = bass_slap_bar(ch, BEATS, SLAP[i % 4]); b, pop = split_slap(b)
    elif name in ("verse2", "pre", "pre2", "solo") or (name in ("verse", "inter") and last):
        b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
        if name == "verse2" and not last: mute = bar("R:0.25 " + f"{root}:0.25, R:1.5 {root}:0.25, R:1.75")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:3! {root}:1")
        elif last and name != "chorus3": b = bar(f"{root}:1.5! {root}:0.5 R:2")
        elif name == "chorus3" and last: b = bar(f"{root}:4!")
        else: b = bass_root8(ch, BEATS, nxt)
    elif name == "bridge":
        b = walk4(ch, nxt)
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R4
    P["bass"].append(b); P["pop"].append(pop); P["mute"].append(mute)

    k = s = h = None; tom = cym = None
    GH = "..o..o.o..o..o.o"   # スネアのゴーストの位置
    if name in ("intro", "outro") or (name == "inter" and i >= 4):
        if name == "intro" and i == 0:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "outro" and last:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        else:
            k = "X..x....X.x....." if i % 2 == 0 else "X..x...x..X..x.."
            s = "....X.......X..."
            s = "".join("o" if (GH[j] == "o" and k[j] == "." and c == ".") else c for j, c in enumerate(s))
            h = "".join("X" if j % 4 == 0 else ("x" if j % 2 == 0 else "o") for j in range(16))
            h = "".join("." if s[j] == "X" else c for j, c in enumerate(h))
            if (name == "intro" and i == 1) or (name == "inter" and i == 4) or (name == "outro" and i == 0): cym = f"{CR2}:1! R:3"; h = "...." + h[4:]
            if last and name != "outro":
                k, s, tom = linear_fill(kit, 2, i); k = "X..x...." + k[8:]; s = "....X..." + s[8:]; h = "..o.....o......."
    elif name in ("verse", "inter"):
        k = ["X......x..X.....", "X..x......X..x..", "X......x..X..x..", "X..x....X......."][i % 4]
        s = "....X.......X..."
        s = "".join("o" if (GH[j] == "o" and k[j] == "." and c == ".") else c for j, c in enumerate(s))
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(16))
        if i == 0: cym = f"{CR2}:1! R:3"; h = "...." + h[4:]
        if last:
            k, s, tom = linear_fill(kit, 2, 3); k = "X......x" + k[8:]; s = "....X..." + s[8:]; h = None
    elif name == "verse2":
        k = "X......x..X....." if i % 2 == 0 else "X..x......X..x.."
        s = "....X.......X..."; s = "".join("o" if (GH[j] == "o" and k[j] == "." and c == ".") else c for j, c in enumerate(s))
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"
        if i == 0: cym = f"{CR2}:1! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"
        if last: k, s, tom = linear_fill(kit, 2, 1); k = "X......x" + k[8:]; s = "....X..." + s[8:]; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 R:2"
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
            s = "....X.......X..." if i % 4 != 3 else "....X..o....X.oo"
            h = "x.X.x.X.x.X.x.X."
            if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + "R:3"; h = "..X." + h[4:]
            if i == 6: cym = f"{CR}:1! R:3"; h = "..X." + h[4:]
        if last and name != "chorus3":
            k, s, tom = linear_fill(kit, 2, 2); k = "X.x...X." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
        if name == "chorus3" and last:
            k = "X..............."; s = "X..............."; h = None; cym = f"{CR}:4!"
    elif name == "bridge":
        # ジャズ: ライドのレガート、スネアは会話するゴースト、キックは羽のように
        k = "o.......o......." ; s = ["..o....o.o....o.", "....o..o..o....o", "..o..o.....o..o.", "o......o.o..o..."][i % 4]
        cym = f"{RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25"
        if i == 0: cym = f"{CR2}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1! {RIDE}:1 R:2"; s = "..o....o........"
    elif name == "solo":
        k = ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2] if i < 4 else "X..x....X.x..x.."
        s = "....X.......X..."; s = "".join("o" if (GH[j] == "o" and k[j] == "." and c == ".") else c for j, c in enumerate(s))
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i in (0, 4): cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k, s, tom = linear_fill(kit, 2, 0); k = "X.x...X." + k[8:]; s = "....X..." + s[8:]; cym = f"{RIDE}:1 {RIDE}:1 R:2"
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
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(part("バリトンサックス", "brass", J("sax"), patch="bariSax", volume=0.14, pan=0.15, reverb=0.25, phrase=8, attack=0.02, release=0.3,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 900, "high": 1}, {"type": "plate", "mix": 0.14}]))
song.add(bass_part(J("bass")))
song.add(slap_pop_part(J("pop")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-13-yamiichi.json"
    song.write(out)
    check_clash(song)
