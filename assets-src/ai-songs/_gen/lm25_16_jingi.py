# ラウド25曲（第2シリーズ）16「仁義の雨」（仮）。イメージ: マフィア×嵐（雨の中の果たし合い）。G♯ 和声的短音階・116・7/4（2+2+3）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: アコーディオン（タンゴのような刻みの和音・ギターとの掛け合い・弔いの独奏）
# 物語: 雨の中の果たし合い。間奏のジャズは男たちの昔話。ブリッジの掛け合いで裏切りが明かされ、アコーディオンだけの弔いのあと、最後のサビ。
# 形（ほかの曲と変える）: 7拍子のタンゴ風。ブレイクダウンのかわりに「弔い」（アコーディオンとベースだけ）。
# しかけ:
#   - 2+2+3 の最後の3拍で、和声的短音階の導音（G＝F♯♯）へ上がる看板リフ
#   - 雨: Aメロのハイハットは弱い16分（雨粒）
#   - サビ: E から B/D♯・C♯m と下りる低音、5小節目の A（ナポリの ♭Ⅱ）で光
#   - ブリッジ: ギターのレガート（和声的短音階の速い上り下り）とアコーディオンの掛け合い
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 116, 7
bar = Bars(BEATS)
R7 = bar.rest()

FORM = [("intro", 4), ("verse", 6), ("pre", 3), ("chorus", 6), ("inter", 4), ("verse2", 4), ("pre2", 3), ("chorus2", 6),
        ("bridge", 6), ("funeral", 4), ("chorus3", 8), ("outro", 3)]
VERSE = ["G#m", "C#m/G#", "G#m", "D#7", "E", "D#7"]
PRE = ["C#m7", "A", "D#7sus4"]
CHORUS = ["E", "B/D#", "C#m", "G#m/B", "A", "D#7"]
CH = {"intro": ["G#m", "G#m", "A", "D#7"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": ["C#m7", "F#7", "Bmaj7", "Emaj7"],
      "verse2": VERSE[:4], "pre2": PRE, "chorus2": CHORUS, "bridge": ["G#m", "E", "C#m", "D#7", "G#m", "A"], "funeral": ["G#m", "E", "A", "D#7"],
      "chorus3": ["E", "B/D#", "C#m", "G#m/B", "A", "E", "D#7sus4", "D#7"], "outro": ["G#m", "A", "G#m"]}
song = Song("仁義の雨（仮）",
            "仮: ラウド25曲（第2シリーズ）の16曲目。イメージはマフィア×嵐（雨の中の果たし合い）。G♯ 和声的短音階・116・7/4（2+2+3）。最後の3拍で導音へ上がるタンゴ風の看板リフ、"
            "雨粒のハイハット、サビは E から下りる低音と A（♭Ⅱ）の光。間奏はジャズ、ブリッジはレガートとアコーディオンの掛け合い、アコーディオンだけの弔い。別の楽器はアコーディオン。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 雨の中の果たし合い。昔話（ジャズ）、裏切り（掛け合い）、弔い、そして最後のサビ。"
song.kinds = {"funeral": "break"}
SECS, NB = song.secs, song.nb

RIFF = {"G#m": [bar("G#1:1! G#1:0.5 A1:0.5", "G#1:1! D#2:0.5 E2:0.5", "G#1:0.5! B1:0.5 C#2:0.5 D#2:0.5 G2:0.5 G#2:0.5"),
                bar("G#1:1! G#1:0.5 A1:0.5", "G#1:1! D#2:0.5 B1:0.5", "G#1:0.5! D#2:0.5 E2:0.5 D#2:0.5 C#2:0.5 B1:0.5")],
        "A": [bar("A1:1! A1:0.5 B1:0.5", "A1:1! E2:0.5 C#2:0.5", "A1:0.5! C#2:0.5 E2:0.5 G#2:0.5 A2:1")] * 2,
        "D#7": [bar("D#2:1! D#2:0.5 E2:0.5", "D#2:1! A#2:0.5 G2:0.5", "D#2:0.5! G2:0.5 A#2:0.5 C#3:0.5 D#3:1")] * 2}

VERSE_MEL = [bar("R:1 D#4:0.5 G#4:0.5", "B4:1 A#4:1", "G#4:3"), bar("C#5:1.5 E5:0.5", "D#5:1 C#5:1", "G#4:3"),
             bar("R:0.5 B4:0.5 D#5:0.5 C#5:0.5", "B4:2", "A#4:1 G#4:2"), bar("G4:1 A#4:1", "C#5:2", "D#5:3"),
             bar("E5:1 F#5:1", "B4:2", "G#4:3"), bar("G4:2", "A#4:1 C#5:1", "D#5:1 R:2")]
VERSE2_MEL = [bar("R:1 G#4:0.5 B4:0.5", "D#5:1 C#5:1", "B4:3"), bar("E5:1.5 G#5:0.5", "F#5:1 E5:1", "C#5:3"),
              bar("R:0.5 D#5:0.5 G#5:0.5 F#5:0.5", "D#5:2", "C#5:1 B4:2"), bar("A#4:1 C#5:1", "D#5:2", "G5:3")]
PRE_MEL = [bar("E5:1 G#5:1", "B5:2", "G#5:3"), bar("A5:1 E5:1", "C#5:2", "E5:3"), bar("G#5:2", "A#5:2", "R:3")]
CHORUS_MEL = [bar("B5:2!", "G#5:1 E5:1", "B5:3"), bar("D#6:2", "B5:1 F#5:1", "D#5:3"), bar("E5:1 G#5:1", "C#6:2!", "B5:1 G#5:2"),
              bar("D#6:2", "B5:1 G#5:1", "D#5:3"), bar("C#6:1 E6:1!", "C#6:2", "A5:3"), bar("D#6:2", "A#5:1 G5:1", "D#5:3")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("D#6:1 F#6:1".replace("F#6", "B5"), "F#5:1 D#5:1", "B4:3")
CHORUS2_MEL[3] = bar("B5:1 D#6:1", "G#5:2", "B5:3")
CHORUS3_MEL = [bar("B5:7!"), bar("D#6:4 B5:3")] + CHORUS_MEL[2:5] + [bar("G#5:2", "B5:2", "E6:3!"), bar("G#5:4 A#5:3"), bar("G5:4 A#5:3")]

ACC_V = {"G#m": ["B3", "D#4", "G#4"], "C#m/G#": ["C#4", "E4", "G#4"], "D#7": ["C#4", "G4", "A#4"], "E": ["B3", "E4", "G#4"], "A": ["C#4", "E4", "A4"],
         "C#m7": ["B3", "E4", "G#4"], "D#7sus4": ["C#4", "G#4", "A#4"], "B/D#": ["B3", "D#4", "F#4"], "C#m": ["C#4", "E4", "G#4"], "G#m/B": ["B3", "D#4", "G#4"]}
TANGO = "{v}:0.5! R:0.5 {v}:0.5 R:0.5 {v}:0.5! R:0.5 {v}:0.5 R:0.5 {v}:0.5! R:0.25 {v}:0.25 R:0.5 {v}:1.5"   # 2+2+3 のマルカート
ACC_INTER = [bar("G#4:1 B4:1 E5:2 D#5:1 C#5:1 B4:1"), bar("A#4:2 C#5:1 E5:1 D#5:3"), bar("D#5:1 F#5:1 A#5:2 G#5:1 F#5:1 D#5:1"), bar("D#5:3 B4:1 G#4:3")]
ACC_FUNERAL = [bar("D#5:3 B4:1 G#4:3"), bar("G#4:2 B4:1 E5:4"), bar("E5:2 C#5:1 A4:4"), bar("G4:3 A#4:1 D#5:3")]
ACC_BRIDGE = [R7, bar("R:4 B4:0.5 E5:0.5 G#5:0.5 B5:0.5 E5:1"), R7, bar("R:4 G5:0.5 A#5:0.5 D#5:1 C#5:1"), R7, bar("R:4 C#5:0.5 E5:0.5 A5:0.5 C#6:0.5 A5:1")]
BRIDGE_GTR = [bar(legato_run("G#", "harmonic", "G#4", "G#5", 2), "B5:2", "D#6:3"), R7,
              bar(legato_run("G#", "harmonic", "C#5", "C#6", 2), "E6:2", "C#6:3"), R7,
              bar(legato_run("G#", "harmonic", "D#6", "D#5", 2), legato_run("G#", "harmonic", "D#5", "D#6", 2), "G#5:3"), R7]


def walk7(ch, nxt):
    r = root_note(ch)
    rr, q, _ = parse_chord(ch)
    mode = {"7": "mixolydian", "m7": "dorian", "maj7": "ionian"}.get(q, "aeolian")
    sc = scale_notes(rr, mode, r, up(r, 1), flat="b" in rr)
    tones = chord_tones(ch, r, up(r, 1))
    line = [r, tones[1], sc[3], tones[2], sc[5], tones[-1] if len(tones) > 3 else up(r, 1)]
    return bar(" ".join(f"{x}:1{'!' if j == 0 else ''}" for j, x in enumerate(line)) + f" {approach_note(ch, nxt)}:1")


P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "a0", "a1", "a2", "amel", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
HEADS = (0, 8, 16)


def g28(*pos, ch="X", base=None):
    return kit.grid(pos, ch, base)


RIDE223 = f"{BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 {RIDE}:1"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R7
    if name in ("intro", "outro"):
        if name == "intro" and i == 0: rf = R7
        elif name == "outro" and last: rf = bar("G#1:7!")
        else: rf = RIFF[base_ch if base_ch in RIFF else "G#m"][i % 2]
    P["riff"].append(rf)

    s = si = R7
    if name in ("verse", "verse2") and (i >= 3 or name == "verse2"):
        s = bar(f"{groot}:2 {groot}:2 {groot}:3") if not last else bar(f"{groot}:4! R:3")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:4! {groot}:3") if not last else bar(f"{groot}:4! R:3")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 2: s = bar(f"{groot}:7!")
        elif last and name != "chorus3": s = bar(f"{groot}:4! R:3")
        else: s = bar(f"{groot}:2! {groot}:2 {groot}:3")
        si = s if not (name == "chorus3" and i < 2) else R7
    elif name == "bridge":
        s = bar(f"{groot}:7")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tech = amel = R7; av = [R7, R7, R7]
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 2: harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "bridge": tech = BRIDGE_GTR[i]; amel = ACC_BRIDGE[i]
    elif name == "inter": amel = ACC_INTER[i]
    elif name == "funeral": amel = ACC_FUNERAL[i]
    if name in ("intro", "verse", "chorus2") or (name == "outro" and not last):
        v = ACC_V.get(ch)
        if v: av = [bar(TANGO.format(v=x)) for x in v]
    elif name == "outro" and last:
        av = [bar(f"{x}:7") for x in ACC_V["G#m"]]
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech); P["amel"].append(amel)
    for j in range(3): P[f"a{j}"].append(av[j])

    if name in ("intro", "outro"):
        if name == "intro" and i == 0: b = bar("G#1:4 G#1:3")
        elif name == "outro" and last: b = bar("G#1:7!")
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("verse", "verse2", "pre", "pre2") or (name.startswith("chorus") and not (name == "chorus3" and i < 2)):
        if last and name != "chorus3": b = bar(f"{root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5 {root}:1! R:4")
        else:
            toks = [f"{root}:0.5{'!' if j in (0, 4, 8) else ''}" for j in range(14)]
            if root_note(nxt) != root: toks[-1] = f"{approach_note(ch, nxt)}:0.5"
            b = bar(" ".join(toks))
    elif name == "chorus3": b = bar(f"{root}:4! {root}:3")
    elif name == "inter": b = walk7(ch, nxt)
    elif name == "bridge": b = bar(f"{root}:2! {up(root, 1)}:1 {root}:1 {fifth_of(base_ch)}:3")
    elif name == "funeral": b = bar(f"{root}:7")
    else: b = R7
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    RAIN = "".join("o" if j % 2 == 0 else "." for j in range(28))
    if name in ("intro", "outro"):
        if name == "intro" and i == 0:
            h = RAIN; k = g28(0, 8, 16)
        elif name == "outro" and last:
            k = g28(0); s = g28(0); cym = f"{CR}:7!"
        else:
            k = g28(0, 8, 16, 18); s = g28(4, 12, 22); cym = RIDE223
            if name == "intro" and i == 1: cym = f"{CR}:1! " + RIDE223.split(" ", 1)[1]
            if name == "intro" and last: k = g28(0, 8); s = g28(4, 12); tom = "R:4 " + tom_triplets_down(3); cym = f"{BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 R:3"
    elif name in ("verse", "verse2"):
        k = g28(0, 8, 16, 22) if i % 2 == 0 else g28(0, 6, 8, 16)
        s = g28(4, 12, 24); s = g28(*[p for p in (10, 19, 27) if k[p] == "."], ch="o", base=s)
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j in HEADS else "o") for j in range(28)) if name == "verse" else None
        if name == "verse2": cym = RIDE223
        if i == 0: cym = f"{CR2}:1! " + (RIDE223.split(" ", 1)[1] if name == "verse2" else "R:6"); h = h and ("...." + h[4:])
        if last: k, s, tom = linear_fill(kit, 3, i); k = g28(0, 8, base=k); s = g28(4, 12, base=s); h = None; cym = None
    elif name in ("pre", "pre2"):
        k = [g28(0, 8, 16), g28(*range(0, 28, 4)), g28(*range(0, 24))][i]
        s = [g28(4, 12, 24), g28(4, 12, 20, 24), g28(24, 25, 26, 27)][i]
        h = [g28(*range(0, 28, 2), ch="x"), g28(*range(0, 28), ch="x"), None][i]
        if i == 0: cym = f"{CR2}:2! R:5"
        if i == 2: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! {CHINA}:1 {CHINA}:1! R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 2
        if half:
            k = g28(0, 16); s = g28(16)
            cym = f"{CR}:7!" if i == 0 else f"{RIDE}:1! {RIDE}:1 {RIDE}:1 {RIDE}:1 {BELL}:1! {RIDE}:1 {RIDE}:1"
        else:
            k = [g28(0, 3, 8, 11, 16, 19, 22), g28(0, 3, 8, 16, 18, 22, 26)][i % 2]
            s = g28(4, 12, 20, 24)
            h = "".join("X" if j in HEADS else ("x" if j % 2 == 0 else ".") for j in range(28))
            h = "".join("." if s[j] == "X" else c for j, c in enumerate(h))
            if i % 2 == 0: cym = (f"{CR}:1! " if i % 4 == 0 else f"{CR2}:1! ") + "R:6"; h = "...." + h[4:]
            if name == "chorus2" and i == 3: k = "".join("X" if j % 2 == 0 else "x" for j in range(28)); h = None; cym = RIDE223
        if last and name != "chorus3":
            k, s, tom = linear_fill(kit, 3, 1); k = g28(0, 8, base=k); s = g28(4, 12, base=s); h = None; cym = None
        if name == "chorus3" and last:
            k = g28(0, 8, 16); s = g28(4, 12, 20); h = None; cym = f"{CR}:2! {RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1"
    elif name == "inter":
        # 昔話（ジャズ）: ライドのレガート、スネアのゴースト
        k = g28(0, 16, ch="o"); s = g28(6, 14, 22, ch="o")
        cym = f"{RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1"
        if i == 0: cym = f"{CR2}:1! " + cym.split(" ", 1)[1]
        if last: tom = "R:4 " + tom_triplets_down(3); cym = f"{RIDE}:1! {RIDE}:1 {RIDE}:1 {RIDE}:1 R:3"; s = g28(6, 14, ch="o")
    elif name == "bridge":
        k = "".join("X" if j % 2 == 0 else "x" for j in range(28)) if i % 2 == 0 else g28(0, 8, 16, 18)
        s = g28(4, 12, 20, 24) if i % 2 == 0 else g28(4, 12, 22)
        k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = RIDE223
        if i == 0: cym = f"{CR}:1! " + RIDE223.split(" ", 1)[1]
        if last: k, s, tom = linear_fill(kit, 3, 2); k = g28(0, 8, base=k); s = g28(4, 12, base=s); cym = None
    elif name == "funeral":
        # 弔い: 雨（弱い16分のハイハット）だけ
        h = RAIN if i < 3 else "".join("o" if j % 2 == 0 and j < 16 else "." for j in range(28))
        if last: tom = "R:4 " + tom_triplets_down(3)
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("chorus", "chorus2", "chorus3"): FX.append(bar("R:4 C4:3"))
    elif name == "funeral" and i == 1: FX.append(bar("R:1 E4:6"))
    else: FX.append(R7)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="レガートのギター", vol=0.11, pan=0.05))
ACC = dict(reverb=0.35, attack=0.03, release=0.4, fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 1500, "high": 0}, {"type": "plate", "mix": 0.18}])
song.add([part(f"アコーディオン（和音{j + 1}）", "accordion", J(f"a{j}"), volume=0.07, pan=-0.2, **ACC) for j in range(3)])
song.add(part("アコーディオン（旋律）", "accordion", J("amel"), volume=0.14, pan=-0.15, phrase=8, **ACC))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "deep-scoop-djent"
add_layer(song, "strings", "雨の果たし合いを見守る、タンゴの弦。")

# 展開の型（2026-10-23 人間「展開が全曲同じ」「4分から5分」）。lm25_plans.py
from lm25_plans import apply_plan
apply_plan(song, "16")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-16-jingi.json"
    song.write(out)
    check_clash(song)
