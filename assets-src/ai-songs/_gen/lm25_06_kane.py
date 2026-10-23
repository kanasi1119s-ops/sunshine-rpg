# ラウド25曲（第2シリーズ）06「鐘と偶像」（仮）。イメージ: 宗教（祈りと偶像）。B 短調・84・6/4（3+3）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: オルガン（教会のパイプオルガンの録音 VSCO 2 CE。和音の伸ばしと、ブリッジの聖歌のような4声）
# しかけ:
#   - 6拍子を 3+3 で数える。前奏は全員の一撃とオルガンの和音 → 大きなタムの行進 → 看板リフ
#   - 看板リフ: B の低い開放から、C♯・D・G・C（ナポリの ♭II）へ。重く、刻まない
#   - ベースは旋律（Aメロでもう一本の歌）。サビの低音は G → F♯ → E → D → C と下りて F♯7 で止まる
#   - サビ5小節目の Cmaj7（♭II）で光。最後のサビだけ A → F♯7sus4 → F♯7 と延ばす
#   - ブリッジ: オルガンの4声の聖歌とベースの旋律、ライドのベルが鐘のように
#   - ドラム: 大きなタム（フロア）の行進、ライドのベル、3+3 の頭
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 84, 6
bar = Bars(BEATS)
R6 = bar.rest()

FORM = [("intro", 4), ("verse", 6), ("pre", 2), ("chorus", 6), ("inter", 3), ("verse2", 4), ("pre2", 2), ("chorus2", 6),
        ("bridge", 5), ("break", 2), ("chorus3", 8), ("outro", 2)]
VERSE = ["Bm", "Gmaj7", "Em", "Bm/F#", "Cmaj7", "F#7"]
PRE = ["Em", "F#7sus4"]
CHORUS = ["G", "D/F#", "Em", "Bm/D", "Cmaj7", "F#7"]
CH = {"intro": ["Bm", "Bm", "G", "Bm"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": ["Bm", "G", "F#7"],
      "verse2": VERSE[:4], "pre2": PRE, "chorus2": CHORUS, "bridge": ["Em", "Bm", "C", "G", "F#7sus4"],
      "break": ["B5", "B5"], "chorus3": ["G", "D/F#", "Em", "Bm/D", "Cmaj7", "A", "F#7sus4", "F#7"], "outro": ["Bm", "B5"]}
song = Song("鐘と偶像（仮）",
            "仮: ラウド25曲（第2シリーズ）の6曲目。イメージは宗教（祈りと偶像）。B 短調・84・6/4（3+3）。全員の一撃とオルガンの和音、大きなタムの行進、"
            "B の低い開放からナポリの ♭II（C）へ動く看板リフ。ベースは旋律、サビは G から C へ下りる低音と Cmaj7 の光、ブリッジはオルガンの聖歌。別の楽器はオルガン。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 巡礼者が偶像の前で祈り、偶像が崩れ、最後は鐘とオルガンだけが残る。"
SECS, NB = song.secs, song.nb
song.pickups = ['V4']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"Bm": [bar("B1:1.5! B1:0.5 D2:0.5 C#2:0.5", "B1:1.5! F#2:0.5 G2:1"), bar("B1:1.5! B1:0.5 D2:0.5 E2:0.5", "F#2:1.5! E2:0.5 D2:0.5 C#2:0.5")],
        "G": [bar("G1:1.5! G1:0.5 B1:0.5 A1:0.5", "G1:1.5! D2:0.5 E2:1")] * 2,
        "F#7": [bar("F#1:1.5! F#1:0.5 A#1:0.5 C#2:0.5", "F#1:1.5! E2:0.5 C#2:1")] * 2}

VERSE_MEL = [bar("R:1 F#4:0.5 D4:0.5 B3:1", "C#4:1 D4:1 F#4:1"), bar("B4:2 A4:1", "D4:3"),
             bar("R:1 G4:0.5 B4:0.5 E5:1", "D5:1 B4:1 G4:1"), bar("F#4:3", "R:1 D4:0.5 E4:0.5 F#4:1"),
             bar("G4:1 B4:1 E5:1", "D5:0.5 C5:0.5 B4:2"), bar("A#4:2 C#5:1", "E5:2 R:1")]
VERSE2_MEL = [bar("R:0.5 B4:0.5 D5:0.5 F#5:0.5 B5:1", "A5:1 F#5:1 D5:1"), bar("G5:2 F#5:1", "D5:2 B4:1"),
              bar("R:0.5 E5:0.5 G5:0.5 B5:0.5 E6:1", "D6:1 B5:1 G5:1"), bar("F#5:3", "R:1 D5:0.5 E5:0.5 F#5:1")]
PRE_MEL = [bar("E5:1 G5:1 B5:1", "A5:1 G5:1 E5:1"), bar("F#5:2 E5:1", "B4:1 C#5:1 R:1")]
CHORUS_MEL = [bar("R:0.5 D5:0.5 G5:0.5 B5:0.5 D6:2!", "B5:1 A5:0.5 G5:0.5"), bar("A5:3", "F#5:1 E5:1 D5:1"),
              bar("R:0.5 E5:0.5 G5:0.5 B5:0.5 E6:2!", "D6:1 B5:1"), bar("B5:3", "A5:1 F#5:1 D5:1"),
              bar("E5:1 G5:1 B5:1", "C6:2 B5:1"), bar("A#5:3", "C#6:1 A#5:1 F#5:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("A5:1 D6:1 B5:1", "A5:1 F#5:1 D5:1")
CHORUS2_MEL[3] = bar("B5:1 D6:1 B5:1", "F#5:3")
CHORUS3_MEL = [bar("D6:6!"), bar("B5:3 A5:3")] + CHORUS_MEL[2:5] + [bar("E5:1 A5:1 C#6:1", "B5:3"), bar("B5:3 C#6:3"), bar("A#5:6!")]

VERSE_BASS = [bar("B1:2 D2:1", "F#2:1 E2:1 D2:1"), bar("G1:2 B1:1", "D2:2 F#2:1"), bar("E2:2 G2:1", "B2:1 A2:1 G2:1"),
              bar("F#1:3", "F#1:1 A1:1 C#2:1"), bar("C2:2 E2:1", "G2:1 E2:1 C2:1"), bar("F#1:2 A#1:1", "C#2:1 E2:1 F#2:1")]
BRIDGE_BASS = [bar("E2:3 G2:1.5 F#2:0.5 E2:1"), bar("D2:3 F#2:1.5 E2:0.5 D2:1"), bar("C2:3 E2:1.5 D2:0.5 C2:1"),
               bar("B1:3 D2:1.5 C2:0.5 B1:1"), bar("F#1:6")]
# オルガンの4声（ソプラノ・アルト・テノール）＋ベースの旋律
CHORALE = [[bar("G4:3 B4:3"), bar("E4:6"), bar("B3:6")],
           [bar("D5:3 B4:3"), bar("F#4:6"), bar("D4:6")],
           [bar("C5:3 E5:3"), bar("G4:6"), bar("E4:6")],
           [bar("D5:3 B4:3"), bar("G4:6"), bar("D4:6")],
           [bar("C#5:6"), bar("B4:6"), bar("E4:6")]]
ORG = {"Bm": ["F#4", "B4", "D5"], "G": ["G4", "B4", "D5"], "Gmaj7": ["G4", "B4", "D5"], "Em": ["G4", "B4", "E5"], "Bm/F#": ["F#4", "B4", "D5"], "Cmaj7": ["G4", "B4", "E5"],
       "F#7": ["E4", "A#4", "C#5"], "D/F#": ["F#4", "A4", "D5"], "Bm/D": ["F#4", "B4", "D5"], "A": ["E4", "A4", "C#5"], "F#7sus4": ["E4", "B4", "C#5"]}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "o0", "o1", "o2", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"


def g24(*pos, ch="X", base=None):
    return kit.grid(pos, ch, base)


for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    # ----- リフ -----
    rf = R6
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0: rf = bar("B1:6!")
        elif name == "intro" and i == 1: rf = R6
        elif name == "outro" and last: rf = R6
        else:
            key = base_ch if base_ch in RIFF else "Bm"
            rf = RIFF[key][i % 2]
    elif name == "break":
        rf = bar("B1:1.5! B1:1.5!", "C2:3!") if i < n - 1 else bar("B1:1.5! C2:1.5!", "R:3")
    P["riff"].append(rf)

    # ----- リズムギター -----
    s = si = R6
    if name in ("verse", "verse2") and (i >= 3 or name == "verse2"):
        s = bar(f"{groot}:3 {groot}:3") if not last else bar(f"{groot}:3! R:3")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:3! {groot}:3") if not last else bar(f"{groot}:3! {groot}:2! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 2: s = bar(f"{groot}:6!")
        elif last and name != "chorus3": s = bar(f"{groot}:3! R:3")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1.5! {groot}:1.5")
        si = s if not (name == "chorus3" and i < 2) else R6
    elif name == "break":
        s = si = P["riff"][-1]
    P["rhy"].append(s); P["rhy_in"].append(si)

    # ----- 旋律 -----
    lead = harm8 = R6
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 2: harm8 = shift_oct(strip_marks(lead), -1)
    P["lead"].append(lead); P["harm8"].append(harm8)

    # ----- オルガン -----
    ov = [R6, R6, R6]
    if name == "bridge":
        ov = CHORALE[i]
    elif name == "outro" and last:
        ov = [bar("F#4:6"), bar("B4:6"), bar("D5:6")]
    elif (name == "intro" and i < 2) or name in ("chorus", "chorus2", "chorus3") or (name == "verse" and i < 3):
        v = ORG.get(ch)
        if v:
            if name == "intro" and i == 1: ov = [bar(f"{x}:6") for x in v]
            elif name == "intro": ov = [bar(f"{x}:6!") for x in v]
            elif last and name in ("chorus", "chorus2"): ov = [bar(f"{x}:3 R:3") for x in v]
            else: ov = [bar(f"{x}:6") for x in v]
    for j in range(3): P[f"o{j}"].append(ov[j])

    # ----- ベース（旋律） -----
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: b = bar("B0:6!") if i == 0 else bar("B0:3 B0:1.5 F#1:1.5")
        elif name == "outro" and last: b = R6
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name == "verse": b = VERSE_BASS[i]
    elif name == "verse2": b = VERSE_BASS[i] if i < 3 else bar("F#1:3 F#1:1 A1:1 C#2:1")
    elif name in ("pre", "pre2"):
        b = bar(f"{root}:1.5! {root}:1.5 {root}:1.5! {fifth_of(base_ch)}:1.5") if not last else bar(f"{root}:3! {root}:2! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 2: b = bar(f"{root}:6!")
        elif last and name != "chorus3": b = bar(f"{root}:3! R:3")
        else:
            ap = approach_note(ch, nxt)
            b = bar(f"{root}:1.5! {root}:0.5 {up(root, 1)}:1 {fifth_of(base_ch)}:1.5 {root}:0.5 {ap}:1")
    elif name == "bridge": b = BRIDGE_BASS[i]
    elif name == "break": b = unison_low(P["riff"][-1], -1, "B0")
    else: b = R6
    P["bass"].append(b)

    # ----- ドラム（24マス。3+3 の頭は 0・12） -----
    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0:
            k = g24(0); s = g24(0); cym = f"{CR}:6!"; tom = "R:3 A2:1 A2:1 A2:1!"
        elif name == "intro" and i == 1:
            # 大きなタムの行進（フロア2つ）
            tom = "A2:1! D3:0.5 A2:0.5 A2:1 A2:1! D3:0.5 A2:0.5 " + tom_16_down(1)
            k = g24(0, 12); cym = f"{BELL}:1 {BELL}:1 {BELL}:1 {BELL}:1 R:2"
        elif name == "outro" and last:
            cym = f"{BELL}:1.5 {BELL}:1.5, {BELL}:1.5, {BELL}:1.5,"      # 見せ場の後: バンドが抜け、鐘とオルガンだけ
        else:
            k = g24(0, 6, 12, 18) if i % 2 == 0 else g24(0, 6, 12, 16, 18)
            s = g24(8, 20); s = g24(*[p for p in (11, 23) if k[p] == "."], ch="o", base=s)
            cym = f"{BELL}:1! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:1 {BELL}:1! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:1"
            if (name == "intro" and i == 2) or (name == "inter" and i == 0): cym = f"{CR}:1! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:1 {BELL}:1! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:1"
            if last and name != "outro":
                k = g24(0, 6); s = g24(8); tom = "R:3 " + tom_triplets_down(3)
                cym = f"{BELL}:1! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:1 R:3"
    elif name in ("verse", "verse2"):
        # 行進: フロアタムを3+3の頭、キックは付点4分、スネアは4拍目（ハーフ）
        k = g24(0, 6, 12, 18)
        s = g24(12) if i % 2 == 0 else g24(12, 21, ch="X"); s = s if i % 2 == 0 else g24(21, ch="o", base=g24(12))
        tom = "A2:1! R:1 A2:1 R:3" if name == "verse" else None
        cym = f"{BELL}:1 {RIDE}:1 {RIDE}:1 {BELL}:1 {RIDE}:1 {RIDE}:1" if name == "verse" else None
        h = None if name == "verse" else "".join("X" if j in (0, 12) else ("x" if j % 2 == 0 else ".") for j in range(24))
        if i == 0: cym = f"{CR2}:1! {RIDE}:1 {RIDE}:1 {BELL}:1 {RIDE}:1 {RIDE}:1" if name == "verse" else f"{CR2}:1! R:5"
        if last:
            k = g24(0, 6); s = g24(); tom = "R:3 " + tom_triplets_down(3); h = None
            cym = f"{BELL}:1 {RIDE}:1 {RIDE}:1 R:3"
    elif name in ("pre", "pre2"):
        k = g24(*range(0, 24, 2)) if i == 0 else g24(*range(0, 16))
        s = g24(8, 20) if i == 0 else g24(16, 18, 20, 22)
        h = g24(*range(0, 24, 2), ch="x") if i == 0 else None
        if i == 0: cym = f"{CR2}:3! R:3"
        else: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! {CHINA}:1 R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 2
        if half:
            k = g24(0, 12); s = g24(12)
            cym = f"{CR}:6!" if i == 0 else f"{BELL}:1! {RIDE}:1 {RIDE}:1 R:3"
            tom = "R:3 A2:1 A2:1 A2:1!" if i == 1 else None
            if i == 1: s = g24()
        else:
            k = [g24(0, 3, 6, 12, 15, 18), g24(0, 6, 9, 12, 18, 21)][i % 2]
            s = g24(8, 20)
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5"
            if i % 2 == 0: cym = (f"{CR}:1.5! " if i % 4 == 0 else f"{CR2}:1.5! ") + f"{RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5"
            if name == "chorus2" and i == 3: k = "".join("X" if j % 2 == 0 else "x" for j in range(24))
        if last and name != "chorus3":
            k = g24(0, 6); s = g24(8); tom = "R:3 " + tom_triplets_down(3); cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 R:3"
        if name == "chorus3" and last:
            k = g24(0); s = g24(0); cym = f"{CR}:6!"; tom = None
    elif name == "bridge":
        # 鐘: ライドのベルを1拍ずつ、フロアタムの心拍
        k = g24(0) if i % 2 == 0 else g24(0, 12)
        cym = f"{BELL}:1 {BELL}:1, {BELL}:1, {BELL}:1 {BELL}:1, {BELL}:1,"
        tom = "R:3 A2:3," if i % 2 == 1 else None
        if i == 0: cym = f"{CR2}:3 {BELL}:1 {BELL}:1, {BELL}:1,"
        if last: tom = "R:3 " + tom_triplets_down(3); cym = f"{BELL}:1 {BELL}:1, {BELL}:1, R:3"
    elif name == "break":
        k = g24(0, 6, 12) if i < n - 1 else g24(0, 6)
        s = g24(12) if i < n - 1 else g24()
        cym = f"{CHINA}:1.5! {CHINA}:1.5! {CHINA}:3!" if i < n - 1 else f"{CHINA}:1.5! {CHINA}:1.5! R:3"
        if i == 0: cym = f"{CR}:1.5! {CHINA}:1.5! {CHINA}:3!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:3 C4:3"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:4 D4:2"))
    elif name == "outro" and last: FX.append(bar("R:1 B4:5"))
    else: FX.append(R6)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add([part(f"オルガン（{['上', '中', '下'][j]}）", "keys", J(f"o{j}"), patch="churchOrgan", volume=0.07, pan=[-0.25, 0.25, 0][j], reverb=0.4, attack=0.06, release=0.6,
               fx=[{"type": "eq", "low": -4, "mid": -1, "midHz": 600, "high": 0}, {"type": "reverb", "mix": 0.25}]) for j in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "wide-dark-wall"
add_layer(song, "choir", "鐘の下で、巡礼者たちの声が重なる。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-06-kane.json"
    song.write(out)
    check_clash(song)
