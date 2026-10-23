# ラウド25曲（第2シリーズ）08「鼓動の前」（仮）。イメージ: 生と死。G 短調・100・7/4（3+2+2）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: バイオリン（柔らかく力強く透き通る。前奏の嘆き・Aメロ2の対旋律・最後のサビの高い線）
# しかけ:
#   - 7拍子を 3+2+2 で数える。キックの「ドクッ」（2つ続けた打ち）が心臓の鼓動。かたまりの頭ごとに鳴る
#   - 看板リフ: G の低い開放から B♭・A と下り、2つ目と3つ目のかたまりで F・E♭（死の側）へ傾く
#   - サビ: E♭ → B♭/D → Cm7 → Gm/B♭ と下りる低音、5小節目に ♭II（A♭。ナポリ）で光、D7 で止める
#   - ブリッジ: ジャズの ii-V（Cm7 → F7 → B♭maj7 …）にウォーキングのベース、ギターはスウィープ
#   - 最後は G 長調の和音で終わる（死から生へ。ピカルディの3度）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 100, 7
bar = Bars(BEATS)
R7 = bar.rest()

FORM = [("intro", 4), ("verse", 6), ("pre", 3), ("chorus", 6), ("inter", 3), ("verse2", 4), ("pre2", 3), ("chorus2", 6),
        ("bridge", 6), ("break", 2), ("chorus3", 8), ("outro", 3)]
VERSE = ["Gm", "Eb", "Gm", "Cm", "Bb/D", "D7"]
PRE = ["Ebmaj7", "Cm7", "D7sus4"]
CHORUS = ["Eb", "Bb/D", "Cm7", "Gm/Bb", "Ab", "D7"]
CH = {"intro": ["Gm", "Gm", "Eb", "D7"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": ["Gm", "Eb", "D7"],
      "verse2": VERSE[:4], "pre2": PRE, "chorus2": CHORUS, "bridge": ["Cm7", "F7", "Bbmaj7", "Ebmaj7", "Am7b5", "D7"],
      "break": ["G5", "G5"], "chorus3": ["Eb", "Bb/D", "Cm7", "Gm/Bb", "Ab", "Fm", "D7sus4", "D7"], "outro": ["Gm", "Eb", "G"]}
song = Song("鼓動の前（仮）",
            "仮: ラウド25曲（第2シリーズ）の8曲目。イメージは生と死。G 短調・100・7/4（3+2+2）。キックの「ドクッ」が心臓の鼓動、G から F・E♭ へ傾く看板リフ、"
            "サビは E♭ から下りる低音と ♭II（A♭）の光。ブリッジはジャズの ii-V とウォーキングのベース、ギターはスウィープ。最後は G 長調で終わる。別の楽器はバイオリン。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 生まれる前と死ぬ前の鼓動。走馬灯（ジャズ）のあと、G 長調で生まれ直す。"
SECS, NB = song.secs, song.nb

RIFF = {"Gm": [bar("G2:0.5! G2:0.5 A#2:0.5 A2:0.5 G2:0.5 D3:0.5", "G2:0.5! F3:0.5 D#3:1", "G2:0.5! D3:0.5 C3:0.5 A#2:0.5"),
               bar("G2:0.5! G2:0.5 A#2:0.5 A2:0.5 G2:0.5 D3:0.5", "G2:0.5! F3:0.5 D#3:1", "D3:0.5! C3:0.5 A#2:0.5 A2:0.5")],
        "Eb": [bar("D#2:0.5! D#2:0.5 G2:0.5 F2:0.5 D#2:0.5 A#2:0.5", "D#2:0.5! D3:0.5 C3:1", "D#2:0.5! A#2:0.5 G2:0.5 F2:0.5")] * 2,
        "D7": [bar("D2:0.5! D2:0.5 F#2:0.5 A2:0.5 D2:0.5 C3:0.5", "D2:0.5! A2:0.5 F#2:1", "D2:1! R:1")] * 2}

VERSE_MEL = [bar("R:1 D4:0.5 G4:0.5 A#4:1", "A4:1 G4:1", "D4:2"), bar("D#4:1.5 G4:0.5 A#4:1", "C5:1 A#4:1", "G4:2"),
             bar("R:0.5 A#4:0.5 D5:0.5 C5:0.5 A#4:1", "A4:2", "G4:2"), bar("C5:1.5 D#5:0.5 G5:1", "F5:1 D#5:1", "C5:2"),
             bar("D5:2 F5:1", "A#4:2", "R:2"), bar("A4:1 C5:1 F#5:1", "D5:2", "R:2")]
VERSE2_MEL = [bar("R:1 G4:0.5 A#4:0.5 D5:1", "C5:1 A#4:1", "G4:2"), bar("G4:1.5 A#4:0.5 D#5:1", "F5:1 D#5:1", "A#4:2"),
              bar("R:0.5 D5:0.5 G5:0.5 F5:0.5 D5:1", "A4:2", "A#4:2"), bar("D#5:1.5 G5:0.5 C6:1", "A#5:1 G5:1", "D#5:2")]
PRE_MEL = [bar("G4:1 A#4:1 D5:1", "D#5:2", "D5:2"), bar("C5:1 D#5:1 G5:1", "A#5:2", "G5:2"), bar("A5:1 G5:1 D5:1", "C5:2", "R:2")]
CHORUS_MEL = [bar("A#5:3!", "G5:1 F5:0.5 D#5:0.5", "G5:2"), bar("F5:2 D5:1", "A#4:2", "F5:2"),
              bar("D#5:3", "G5:1 A#5:1", "C6:2!"), bar("A#5:2 A5:1", "G5:2", "D5:2"),
              bar("D#5:1 G#5:1 C6:1", "D#6:2!", "C6:2"), bar("D6:2 C6:1", "A5:1 F#5:1", "D5:2")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("F5:1 A#5:1 D6:1", "A#5:2", "F5:2")
CHORUS2_MEL[3] = bar("A#5:1 D6:1 A#5:1", "G5:2", "A#5:2")
CHORUS3_MEL = [bar("A#5:7!"), bar("F5:4 D5:3")] + CHORUS_MEL[2:5] + [bar("F5:2 G#5:1", "C6:2", "G#5:2"), bar("G5:3", "A5:2", "D6:2"), bar("F#5:7")]

# バイオリン
VLN_INTRO = [bar("D5:3 C5:1 A#4:1 A4:2"), bar("G4:4 A4:1 A#4:2"), bar("G5:3 F5:1 D#5:3"), bar("C5:3 A4:2 F#4:2")]
VLN_V2 = [bar("R:3 D5:2 A#4:2"), bar("A#4:3 G4:2 R:2"), bar("R:3 G5:2 D5:2"), bar("D#5:3 C5:2 R:2")]
VLN_C3 = {4: bar("C6:3 D#6:2 C6:2"), 5: bar("C6:3 G#5:2 F5:2"), 6: bar("A5:3 C6:2 D6:2"), 7: bar("C6:3 A5:2 F#5:2")}


def walk7(ch, nxt):
    """7拍のウォーキング（根音から和音の音と経過音で上がり、最後の1拍で次の根音へ近づく）"""
    r = root_note(ch)
    tones = chord_tones(ch, r, up(r, 1))
    rr, q, _ = parse_chord(ch)
    mode = {"7": "mixolydian", "m7": "dorian", "m7b5": "locrian", "maj7": "ionian"}.get(q, "aeolian")
    sc = scale_notes(rr, mode, r, up(r, 1), flat="b" in rr)
    line = [r, tones[1], sc[3] if len(sc) > 3 else tones[2], tones[2], sc[5] if len(sc) > 5 else tones[2], tones[-1] if len(tones) > 3 else up(r, 1)]
    return " ".join(f"{x}:1{'!' if j == 0 else ''}" for j, x in enumerate(line)) + f" {approach_note(ch, nxt)}:1"


BRIDGE_SWEEP = {"Cm7": ("G4", "G5"), "F7": ("A4", "A5"), "Bbmaj7": ("F4", "F5"), "Ebmaj7": ("G4", "G5"), "Am7b5": ("G4", "G5"), "D7": ("F#4", "F#5")}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "vln", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
HEADS = (0, 12, 20)


def g28(*pos, ch="X", base=None):
    return kit.grid(pos, ch, base)


def beat_kick(extra=()):
    """鼓動（ドクッ）: かたまりの頭とその16分あと"""
    return g28(*[p for h in HEADS for p in (h, h + 1)], *extra)


RIDE322 = f"{BELL}:1! {RIDE}:1 {RIDE}:1 {BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R7
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: rf = R7
        elif name == "outro" and last: rf = bar("G2:7!")
        else: rf = RIFF[base_ch if base_ch in RIFF else "Gm"][i % 2]
    elif name == "break":
        rf = bar("G2:3! G2:2! G#2:2!") if i < n - 1 else bar("G2:3! G#2:2! R:2")
    P["riff"].append(rf)

    s = si = R7
    if name in ("verse", "verse2") and (i >= 3 or name == "verse2"):
        s = bar(f"{groot}:3 {groot}:2 {groot}:2") if not last else bar(f"{groot}:3! R:4")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:3! {groot}:4") if not last else bar(f"{groot}:3! {groot}:2! R:2")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 2: s = bar(f"{groot}:7!")
        elif last and name != "chorus3": s = bar(f"{groot}:3! R:4")
        else: s = bar(f"{groot}:3! {groot}:2 {groot}:2")
        si = s if not (name == "chorus3" and i < 2) else R7
    elif name == "bridge":
        s = bar(f"{groot}:7")
    elif name == "break":
        s = si = P["riff"][-1]
    elif name == "outro" and last:
        s = si = bar("G2:7!")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tech = vln = R7
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]; vln = VLN_V2[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]; vln = VLN_C3.get(i, R7)
        if i >= 2: harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "intro": vln = VLN_INTRO[i]
    elif name == "outro" and last: vln = bar("B5:7")
    elif name == "bridge":
        lo, hi = BRIDGE_SWEEP[ch]
        top = chord_tones(ch, lo, hi)[-1]
        tech = bar(sweep(ch, lo, hi, 2), sweep(ch, lo, hi, 2), f"{top}:3" if i < n - 1 else f"{top}:2 R:1")
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech); P["vln"].append(vln)

    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: b = bar("G1:3! G1:2 G1:2") if i == 0 else bar("G1:3! A#1:2 D2:2")
        elif name == "outro" and last: b = bar("G1:7!")
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("verse", "verse2", "pre", "pre2") or (name.startswith("chorus") and not (name == "chorus3" and i < 2)):
        if last and name != "chorus3":
            b = bar(f"{root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5 {root}:1! R:4")
        else:
            toks = [f"{root}:0.5{'!' if j in (0, 6, 10) else ''}" for j in range(14)]
            if root_note(nxt) != root: toks[-1] = f"{approach_note(ch, nxt)}:0.5"
            b = bar(" ".join(toks))
    elif name == "chorus3": b = bar(f"{root}:3! {root}:4")
    elif name == "bridge": b = bar(walk7(ch, nxt))
    elif name == "break": b = unison_low(P["riff"][-1], -1, "B0")
    else: b = R7
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2:
            k = beat_kick() if i == 1 else g28(0, 1)
            cym = f"{BELL}:3 {BELL}:2 {BELL}:2" if i == 0 else RIDE322
            if i == 1: tom = "R:5 " + tom_16_down(2)
        elif name == "outro" and last:
            k = g28(0); s = g28(0); cym = f"{CR}:7!"
        else:
            k = beat_kick(); s = g28(8, 16, 24); s = g28(*[p for p in (11, 27) if k[p] == "."], ch="o", base=s)
            cym = RIDE322
            if (name == "intro" and i == 2) or (name == "inter" and i == 0): cym = f"{CR}:1! " + RIDE322.split(" ", 1)[1]
            if last and name != "outro":
                k = beat_kick()[:20] + "........"; s = g28(8, 16); tom = "R:5 " + tom_triplets_down(2)
                cym = f"{BELL}:1! {RIDE}:1 {RIDE}:1 {BELL}:1! {RIDE}:1 R:2"
    elif name in ("verse", "verse2"):
        k = beat_kick((6,)) if i % 2 == 0 else beat_kick((26,))
        s = g28(8, 16, 24); s = g28(*[p for p in (5, 15, 23) if k[p] == "."], ch="o", base=s)
        h = "".join("X" if j in HEADS else ("x" if j % 2 == 0 else ".") for j in range(28)) if name == "verse" else None
        if name == "verse2": cym = RIDE322
        if i == 0: cym = f"{CR2}:1! " + (RIDE322.split(" ", 1)[1] if name == "verse2" else "R:6")
        if last: k = beat_kick()[:20] + "........"; s = g28(8, 16); h = None; tom = "R:5 " + tom_triplets_down(2); cym = None
    elif name in ("pre", "pre2"):
        k = [g28(0, 12, 20), g28(*range(0, 28, 4)), g28(*range(0, 24))][i]
        s = [g28(8, 24), g28(8, 16, 24), g28(24, 25, 26, 27)][i]
        h = [g28(*range(0, 28, 2), ch="x"), g28(*range(0, 28), ch="x"), None][i]
        if i == 0: cym = f"{CR2}:3! R:4"
        if i == 2: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! {CHINA}:1 {CHINA}:1! R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 2
        if half:
            k = g28(0, 1, 12, 13); s = g28(12)
            cym = f"{CR}:7!" if i == 0 else f"{RIDE}:1! {RIDE}:1 {RIDE}:1 {BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        else:
            # 5つずつのかたまり（16分5つ）のキックが小節線をまたぐ。スネアはかたまりの2つ目に
            off = ({"chorus": 0, "chorus2": 6, "chorus3": 12}[name] + i) * 28
            k = "".join("X" if (off + j) % 5 == 0 else ("x" if (off + j) % 5 == 2 else ".") for j in range(28))
            s = g28(8, 16, 24); k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 " * 3 + f"{RIDE}:0.5! {RIDE}:0.5"
            cym = cym.strip()
            if i % 2 == 0: cym = (f"{CR}:1! " if i % 4 == 0 else f"{CR2}:1! ") + f"{BELL}:0.5 {RIDE}:0.5 " * 5 + f"{RIDE}:0.5 {BELL}:0.5"
            cym = cym.strip()
        if last and name != "chorus3":
            k = beat_kick()[:20] + "........"; s = g28(8, 16); tom = "R:5 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1 R:2"
    elif name == "bridge":
        # ジャズの区間: ライドのレガート、キックは弱く、スネアは会話するゴースト
        k = g28(0, 20, ch="o"); s = g28(6, 14, 22, ch="o")
        cym = f"{RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1"
        if i == 0: cym = f"{CR2}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1"
        if last: tom = "R:4 " + tom_triplets_down(3); cym = f"{RIDE}:1! {RIDE}:1 {RIDE}:1 {RIDE}:1 R:3"; s = g28(6, 14, ch="o")
    elif name == "break":
        k = g28(0, 12, 20) if i < n - 1 else g28(0, 12)
        s = g28(12) if i < n - 1 else g28()
        cym = f"{CHINA}:3! {CHINA}:2! {CHINA}:2!" if i < n - 1 else f"{CHINA}:3! {CHINA}:2! R:2"
        if i == 0: cym = f"{CR}:3! {CHINA}:2! {CHINA}:2!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:4 C4:3"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:5 D4:2"))
    else: FX.append(R7)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="スウィープのギター", vol=0.11, pan=0.05))
# バイオリン（banned-sounds 21 の出発点: 2本重ね・柔らかく力強く透き通る）
song.add(part("バイオリン", "strings", J("vln"), patch="violin", volume=0.16, pan=-0.15, reverb=0.5, gainDb=3, bright=-0.15, attack=0.35, release=0.7,
              doubleDetune={"cents": 5, "spread": 0.3}, phrase=8,
              fx=[{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 1, "mix": 0.08, "feedback": 0.2},
                  {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "deep-scoop-djent"
add_layer(song, "synth-arp", "心臓の電気信号のように、細かい音が脈打つ。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-08-kodou.json"
    song.write(out)
    check_clash(song)
