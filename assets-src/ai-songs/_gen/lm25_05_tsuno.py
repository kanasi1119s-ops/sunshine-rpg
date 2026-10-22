# ラウド25曲（第2シリーズ）05「七つの角」（仮）。イメージ: 悪魔。E フリジアン・ドミナント・112・5/4（3+2）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 三味線（鋭い撥で、前奏・間奏・後奏の動機）
# しかけ:
#   - 5拍子を 3+2 で数える。看板リフは E と半音上の F（♭2）、長3度の G♯ が同居する「悪魔の音階」
#   - Aメロは E のペダルの上で F/E・Dm/E とにじむ。サビは A 和声的短音階の側へ開け、低音が G♯→A と半音で上がる
#   - サビ7小節目の B♭（A から見た ♭II）で一瞬だけ別の世界
#   - ブリッジ: クリーンのナチュラルハーモニクス（本物の録音）と三味線だけ。ソロはレガート（ハンマリング・プルオフ）
#   - ドラム: 5拍子、3連のタム、ソロの下はツーバスの16分
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 112, 5
bar = Bars(BEATS)
R5 = bar.rest()

FORM = [("intro", 6), ("verse", 8), ("pre", 4), ("chorus", 8), ("inter", 6), ("verse2", 6), ("pre2", 4), ("chorus2", 8),
        ("bridge", 8), ("solo", 6), ("break", 4), ("chorus3", 8), ("outro", 3)]
VERSE = ["E", "F/E", "E7", "Dm/E", "Am", "G#dim7", "F", "E"]
PRE = ["Dm", "F", "G#dim7", "E"]
CHORUS = ["C", "E/G#", "Am", "F", "C", "E/G#", "Bb", "E"]
CH = {"intro": ["E", "E", "E", "F", "E", "E"], "verse": VERSE, "pre": PRE, "chorus": CHORUS,
      "inter": ["E", "F", "E", "Am", "F", "E"], "verse2": VERSE[:6], "pre2": PRE, "chorus2": CHORUS,
      "bridge": ["Am", "Am", "F", "F", "Dm", "Dm", "E", "E"], "solo": ["E", "F", "Am", "G#dim7", "F", "E"],
      "break": ["E5"] * 4, "chorus3": CHORUS, "outro": ["E", "F", "E5"]}
song = Song("七つの角（仮）",
            "仮: ラウド25曲（第2シリーズ）の5曲目。イメージは悪魔。E フリジアン・ドミナント・112・5/4（3+2）。E と F（♭2）と G♯ が同居する看板リフ、"
            "サビは A の和声的短音階へ開け、G♯→A と半音で上がる低音と B♭ の別世界。ブリッジはナチュラルハーモニクスと三味線、ソロはレガート。別の楽器は三味線。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
SECS, NB = song.secs, song.nb

RIFF = {
    "E": [bar("E2:0.5! F2:0.5 E2:0.5 G#2:0.5 A2:0.5 G#2:0.5", "E2:0.5! E3:0.5 D3:0.5 C3:0.5"),
          bar("E2:0.5! F2:0.5 E2:0.5 G#2:0.5 B2:0.5 C3:0.5", "E2:0.5! D3:0.5 F3:1")],
    "F": [bar("F2:0.5! E2:0.5 F2:0.5 A2:0.5 C3:0.5 A2:0.5", "F2:0.5! F3:0.5 E3:0.5 C3:0.5")] * 2,
    "Am": [bar("A2:0.5! G#2:0.5 A2:0.5 C3:0.5 E3:0.5 C3:0.5", "A2:0.5! A3:0.5 G#3:0.5 E3:0.5")] * 2,
}
SHAMI_INTRO = [shift_oct(strip_marks(RIFF["E"][0]), 2), shift_oct(strip_marks(RIFF["E"][1]), 2)]
SHAMI_INTER = [R5, bar("R:3 F5:0.5 E5:0.5 C5:1"), R5, bar("R:3 C5:0.5 B4:0.5 A4:1"), R5, bar("R:3 G#4:0.5 B4:0.5 D5:1")]

VERSE_MEL = [bar("R:1 B3:0.5 E4:0.5 G#4:1", "F4:0.5 E4:0.5 B3:1"), bar("A4:2 C5:1", "A4:1 R:1"),
             bar("R:0.5 G#4:0.5 B4:0.5 E5:0.5 D5:1", "B4:1 G#4:1"), bar("F4:2 A4:1", "D4:2"),
             bar("R:1 C5:0.5 B4:0.5 A4:1", "E5:2"), bar("D5:1.5 B4:0.5 G#4:1", "F4:2"),
             bar("A4:1 C5:1 F5:1", "E5:0.5 C5:0.5 A4:1"), bar("G#4:3", "R:2")]
VERSE2_MEL = [bar("R:0.5 E4:0.5 G#4:0.5 B4:0.5 E5:1", "F5:0.5 E5:0.5 B4:1"), bar("C5:1 F5:1 A5:1", "F5:1 R:1"),
              bar("R:0.5 B4:0.5 E5:0.5 G#5:0.5 D5:1", "B4:1 G#4:1"), bar("A4:1 D5:1 F5:1", "D5:2"),
              bar("R:0.5 E5:0.5 A5:0.5 C6:0.5 B5:1", "A5:2"), bar("G#5:1.5 F5:0.5 D5:1", "B4:2")]
PRE_MEL = [bar("D5:1 F5:1 A5:1", "F5:1 D5:1"), bar("C5:1 F5:1 A5:2", "F5:1"), bar("G#5:1 F5:1 D5:1", "B4:1 D5:1"), bar("E5:1 G#5:1 B5:1", "R:2")]
CHORUS_MEL = [bar("E5:1 G5:1 C6:1", "D6:0.5 C6:0.5 G5:1"), bar("G#5:2 E5:1", "B4:2"),
              bar("A5:1 C6:1 D6:1", "C6:1 A5:1"), bar("C6:2 A5:1", "F5:2"),
              bar("E5:1 G5:1 C6:1", "D6:1 E6:1!"), bar("D6:2 B5:1", "G#5:2"),
              bar("F5:1 A#5:1 D6:2", "C6:1"), bar("B5:2 G#5:1", "E5:2")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("G#5:1 B5:1 E6:1", "D6:1 B5:1")
CHORUS2_MEL[3] = bar("C6:1 A5:1 F5:1", "A5:2")
CHORUS2_MEL[5] = bar("D6:1 E6:1 D6:1", "B5:2")
CHORUS3_MEL = [bar("C6:5!"), bar("B5:3 G#5:2"), bar("A5:5!"), bar("C6:3 A5:2")] + CHORUS_MEL[4:6] + [bar("D6:1 C6:1 A#5:1", "D6:2!"), CHORUS_MEL[7]]

# ブリッジ: ナチュラルハーモニクス（E・B・G♯ の本物の録音）と三味線の旋律
HARM = [bar("E5:2 B5:3"), bar("E6:5"), bar("G#5:2 E5:3"), bar("B5:5"), bar("E5:2 B5:3"), bar("E6:5"), bar("G#5:2 B5:3"), bar("E6:3 R:2")]
SHAMI_BRIDGE = [bar("A4:1 C5:0.5 E5:0.5 A5:2 E5:1"), bar("E5:3 C5:1 B4:1"), bar("C5:1 F5:1 A5:2 C6:1"), bar("A5:3 F5:1 C5:1"),
                bar("D5:1 F5:0.5 A5:0.5 C6:2 A5:1"), bar("A5:3 F5:1 D5:1"), bar("E5:1 G#5:1 B5:2 G#5:1"), bar("G#5:3 R:2")]


def legato_bar(*pieces):
    return bar(*pieces)


SOLO = [
    legato_bar(legato_run("E", "phrygdom", "E4", "E5", 2), "G#5:1.5 F5:0.5 E5:1"),
    legato_bar(legato_run("E", "phrygdom", "F4", "F5", 2), "A5:2 C6:1"),
    legato_bar(legato_run("E", "phrygdom", "A5", "A4", 2), "C5:0.5 E5:0.5 A5:2"),
    legato_bar(legato_run("E", "phrygdom", "G#4", "G#5", 2), "D6:2 B5:1"),
    legato_bar(legato_run("E", "phrygdom", "C6", "C5", 2), "A5:1 F5:1 C6:1"),
    bar("B5:3^^ R:2"),
]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "shami", "gfx", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
RIDE32 = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5"


def g20(*pos, ch="X", base=None):
    return kit.grid(pos, ch, base)


for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = root_note(ch, "E2", "D#3")

    # ----- リフ -----
    rf = R5
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: rf = R5
        elif name == "outro" and last: rf = bar("E2:5!")
        else:
            key = base_ch if base_ch in RIFF else "E"
            if key == "E7": key = "E"
            rf = RIFF[key][i % 2]
            if name == "intro" and last: rf = bar("E2:0.5! F2:0.5 E2:0.5 G#2:0.5 B2:1", "R:2")
    elif name == "break":
        rf = bar("E2:1.5! E2:1.5!", "F2:2!") if i < n - 1 else bar("E2:1.5! F2:1.5!", "R:2")
    P["riff"].append(rf)

    # ----- リズムギター（3+2 の頭で伸ばす） -----
    s = si = R5
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:3 {groot}:2") if not last else bar(f"{groot}:3! R:2")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:3! {groot}:2") if not last else bar(f"{groot}:3! R:2")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:5!")
        elif last and name != "chorus3": s = bar(f"{groot}:3! R:2")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:2")
        si = s if not (name == "chorus3" and i < 4) else R5
    elif name == "solo":
        s = bar(f"{groot}:5")
    elif name == "break":
        s = si = P["riff"][-1]
    P["rhy"].append(s); P["rhy_in"].append(si)

    # ----- 旋律・技・三味線・ハーモニクス -----
    lead = harm8 = tech = shami = gfx = R5
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "solo": tech = SOLO[i]
    elif name == "intro" and i < 2: shami = SHAMI_INTRO[i]
    elif name == "inter": shami = SHAMI_INTER[i]
    elif name == "outro" and i < 2: shami = shift_oct(strip_marks(RIFF["E" if i == 0 else "F"][0]), 2)
    elif name == "bridge": gfx = HARM[i]; shami = SHAMI_BRIDGE[i]
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech); P["shami"].append(shami); P["gfx"].append(gfx)

    # ----- ベース（コードに沿う。3+2 の頭にアクセント） -----
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: b = bar("E1:3 R:2") if i == 0 else bar("E1:3 F1:2")
        elif name == "outro" and last: b = bar("E1:5!")
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("verse", "verse2", "pre", "pre2", "solo") or (name.startswith("chorus") and not (name == "chorus3" and i < 4)):
        if last and not name.startswith("chorus3"):
            b = bar(f"{root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5 {root}:1! R:2")
        else:
            toks = [f"{root}:0.5{'!' if j in (0, 6) else ''}" for j in range(10)]
            if root_note(nxt) != root:
                toks[-1] = f"{fifth_of(base_ch)}:0.5"
            b = bar(" ".join(toks))
    elif name == "chorus3":
        b = bar(f"{root}:3! {root}:2")
    elif name == "bridge":
        b = bar(f"{root}:5") if i % 2 == 0 else bar(f"{root}:3 {fifth_of(base_ch)}:2")
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R5
    P["bass"].append(b)

    # ----- ドラム（20マス＝16分×5拍。3+2 の頭は 0・12） -----
    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0:
            k = g20(0, 12); cym = RIDE32; tom = "R:3 A2:1 A2:1"
        elif name == "intro" and i == 1:
            k = g20(0, 6, 12); tom = "R:2 " + tom_triplets_down(3); cym = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:3"
        elif name == "outro" and last:
            k = g20(0); s = g20(0); cym = f"{CR}:5!"
        else:
            k = g20(0, 4, 12); s = g20(8, 16); s = g20(*[p for p in (11, 18) if k[p] == "."], ch="o", base=s)
            cym = RIDE32 if i % 2 else f"{CR}:0.5! " + RIDE32.split(" ", 1)[1]
            if name == "intro" and i == 2: cym = f"{CR}:1.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5"
            if last and name != "outro":
                k = g20(0, 4); s = g20(8); tom = "R:2 " + tom_triplets_down(3)
                cym = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:3"
    elif name in ("verse", "verse2"):
        k = [g20(0, 6, 12), g20(0, 3, 12, 14), g20(0, 6, 12, 18), g20(0, 10, 12)][i % 4]
        s = g20(8, 16); s = g20(*[p for p in (5, 15) if k[p] == "."], ch="o", base=s)
        h = "".join("X" if j in (0, 12) else ("x" if j % 2 == 0 else ".") for j in range(20))
        if name == "verse2": h = None; cym = RIDE32
        if i == 0: cym = f"{CR2}:1.5! " + (f"{RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5" if name == "verse2" else "R:3.5")
        if last:
            k = g20(0, 6); s = g20(8); h = None; tom = "R:2 " + tom_triplets_down(3); cym = None
    elif name in ("pre", "pre2"):
        k = [g20(0, 12), g20(0, 6, 12, 16), g20(*range(0, 20, 2)), g20(*range(0, 12))][i]
        s = [g20(8), g20(8, 16), g20(4, 8, 12, 16), g20(12, 14, 16, 17, 18, 19)][i]
        h = [g20(*range(0, 20, 4), ch="x"), g20(*range(0, 20, 2), ch="x"), g20(*range(0, 20), ch="x"), None][i]
        if i == 0: cym = f"{CR2}:3! R:2"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = g20(0, 10); s = g20(12)
            cym = f"{CR}:3! {RIDE}:1 {RIDE}:1" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 {RIDE}:1"
        else:
            k = [g20(0, 3, 6, 12, 14), g20(0, 3, 6, 12, 15, 18)][i % 2]
            s = g20(8, 16) if i % 4 != 3 else g20(8, 16, 18, 19)
            h = "".join("x" if (j % 2 == 0) else "." for j in range(20)) if i % 8 < 4 else None
            cym = None if i % 8 < 4 else RIDE32
            if i % 4 == 0: cym = (f"{CR}:1.5! " if i % 8 == 0 else f"{CR2}:1.5! ") + (f"{RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5" if i % 8 >= 4 else "R:3.5")
            if name == "chorus2" and i in (4, 5): k = "".join("X" if j % 2 == 0 else "x" for j in range(20))
        if last and name != "chorus3":
            k = g20(0, 6); s = g20(8); h = None; tom = "R:2 " + tom_triplets_down(3); cym = None
        if name == "chorus3" and last:
            k = g20(0, 3, 6, 12); s = g20(8, 16); h = None; cym = f"{CR}:2! {RIDE}:1 {RIDE}:1 {RIDE}:1"
    elif name == "bridge":
        k = g20(0) if i % 2 == 0 else g20(0, 12)
        s = None if i < 4 else g20(16, ch="o")
        cym = f"{BELL}:1.5 {RIDE}:1.5 {BELL}:1 {RIDE}:1"
        tom = "R:3 A2:2," if i % 2 == 1 else None
        if i == 0: cym = f"{CR2}:3 {BELL}:1 {RIDE}:1"
        if last: tom = "R:2 " + tom_triplets_down(3); cym = f"{BELL}:1.5 {RIDE}:0.5 R:3"
    elif name == "solo":
        k = "".join("X" if j % 2 == 0 else "x" for j in range(20)); s = g20(8, 16)
        cym = RIDE32
        if i == 0: cym = f"{CR}:0.5! " + RIDE32.split(" ", 1)[1]
        if last: k = g20(0, 4); s = g20(8); tom = "R:2 " + tom_triplets_down(3); cym = f"{RIDE}:1 {RIDE}:1 R:3"
    elif name == "break":
        k = g20(0, 6, 12) if i < n - 1 else g20(0, 6)
        s = g20(12) if i < n - 1 else g20()
        cym = f"{CHINA}:1.5! {CHINA}:1.5! {CHINA}:2!" if i < n - 1 else f"{CHINA}:1.5! {CHINA}:1.5! R:2"
        if i == 0: cym = f"{CR}:1.5! {CHINA}:1.5! {CHINA}:2!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:3 C4:2"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:4 D4:1"))
    else: FX.append(R5)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="レガートのギター", vol=0.12, pan=0.05))
song.add(gfx_part(J("gfx"), vol=0.09, role="ナチュラルハーモニクス"))
song.add(part("三味線", "shamisen", J("shami"), volume=0.17, pan=-0.22, reverb=0.3, attack=0.002, release=0.5,
              fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 1800, "high": 1}, {"type": "delay", "beats": 0.75, "mix": 0.15, "feedback": 0.25}, {"type": "plate", "mix": 0.18}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-05-tsuno.json"
    song.write(out)
    check_clash(song)
