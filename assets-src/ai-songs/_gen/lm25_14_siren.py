# ラウド25曲（第2シリーズ）14「裏通りのサイレン」（仮）。イメージ: 裏通り×嵐（追跡劇）。E 短調・140・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: ミュートのトランペット（ハーマンミュートの録音。隠れている路地の場面）
# 物語: 逃げる者と追う者。サイレン（タッピング）が近づき、路地に隠れ、見つかり、最後は突然の無音で終わる。
# 形（ほかの曲と変える）: Bメロなし。サイレン → 走るリフ → Aメロ → 走る Aメロ（倍のノリ）→ サビ … 隠れる（静）→ サイレン → タッピングのソロ → サビ → 突然の無音
# しかけ:
#   - 曲の頭からタッピングのサイレン（上がって下がる）。ドラムは3小節目から追いかけてくる
#   - 走るリフ: 8分の単音で、開放の E とオクターブ上と下りる線（刻まない）
#   - サビ12小節: C から開け、5小節目の F（フリジアンの ♭Ⅱ）で一瞬目がくらむ
#   - 隠れる: ミュートのトランペットとクリーンの和音、キックの心拍だけ
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 140, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 4), ("inter", 8), ("verse", 8), ("run", 8), ("chorus", 12), ("inter2", 8), ("verse2", 8), ("chorus2", 12),
        ("bridge", 12), ("siren", 4), ("solo", 12), ("chorus3", 12), ("outro", 2)]
VERSE = ["Em", "Em", "C", "D", "Em", "Em", "Am", "B7"]
RUN = ["C", "D", "Em", "Em", "C", "D", "B7sus4", "B7"]
CHORUS = ["C", "G/B", "Am", "Em/G", "F", "C", "D", "B7", "C", "D7", "Em", "Em"]
RIFFCH = ["Em", "Em", "C", "D", "Em", "Em", "C", "B7"]
CH = {"intro": ["Em", "Em", "C", "B7"], "inter": RIFFCH, "verse": VERSE, "run": RUN, "chorus": CHORUS, "inter2": RIFFCH, "verse2": VERSE,
      "chorus2": CHORUS, "bridge": ["Am7", "Em7", "Am7", "Em7", "Cmaj7", "Bm7", "Am7", "B7sus4", "Am7", "Em7", "Cmaj7", "B7"],
      "siren": ["Em", "Em", "C", "B7"], "solo": ["Em", "C", "D", "B7"] * 3, "chorus3": CHORUS, "outro": ["E5", "E5"]}
song = Song("裏通りのサイレン（仮）",
            "仮: ラウド25曲（第2シリーズ）の14曲目。イメージは裏通りの追跡劇。E 短調・140。遠くの空気から空間が広がって盛大に始まり、8分の単音で走るリフ、倍のノリの Aメロ、"
            "サビは C から開け F（♭Ⅱ）で目がくらむ。路地に隠れる場面はミュートのトランペット。最後は突然の無音。別の楽器はミュートのトランペット。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 逃げる者と追う者。サイレンが近づき、路地に隠れ、見つかり、最後は突然の無音。"
song.kinds = {"run": "pre", "inter2": "interlude", "siren": "break"}
SECS, NB = song.secs, song.nb
song.pickups = ['V1', 'V2']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"Em": [bar("E2:0.5! E3:0.5 D3:0.5 B2:0.5 G2:0.5 A2:0.5 B2:0.5 D3:0.5"), bar("E2:0.5! E3:0.5 D3:0.5 B2:0.5 G2:0.5 B2:0.5 E3:0.5 F#3:0.5")],
        "C": [bar("C2:0.5! C3:0.5 B2:0.5 G2:0.5 E2:0.5 G2:0.5 B2:0.5 C3:0.5")] * 2,
        "D": [bar("D2:0.5! D3:0.5 C3:0.5 A2:0.5 F#2:0.5 A2:0.5 C3:0.5 D3:0.5")] * 2,
        "B7": [bar("B1:0.5! B2:0.5 A2:0.5 F#2:0.5 D#2:0.5 F#2:0.5 A2:0.5 B2:0.5")] * 2}
# サイレン（タッピング）: 上がる小節と下がる小節
SIREN = {"Em": [["B4", "E5", "G5"], ["E5", "G5", "B5"]], "C": [["C5", "E5", "G5"], ["G4", "C5", "E5"]], "B7": [["D#5", "F#5", "A5"], ["A4", "D#5", "F#5"]],
         "D": [["D5", "F#5", "A5"], ["A4", "D5", "F#5"]]}

# 2026-10-24 旋律を作り直し（人間「似た曲を作らない」。前の旋律は「4分4分2分」など、シリーズの多くの曲と同じリズムだった）:
#   インダストリアルの合唱のような、裏拍の短い突き（16分2つ＋休み）と、オクターブの跳躍。小節の終わりは休む
STAB = [[-0.5, 0.25, 0.25, -0.5, 0.5, -0.25, 0.25, 0.5, -1], [0.25, 0.25, -0.5, 0.25, 0.25, -0.5, 0.75, -1.25],
        [-0.25, 0.25, 0.25, 0.25, -0.5, 0.5, 0.5, -0.5, 0.25, 0.25, -0.5], [-1, 0.25, 0.25, 0.5, -0.5, 0.25, 0.25, 0.5, -0.5]]
EMIN = scale_pcs("E", "aeolian")
VERSE_MEL = [bar(x) for x in melody_walk(EMIN, "B4", "E4", STAB, 1, CH["verse"], contour=(0, 0, 2, -2, 1, -1, 4, -4), lo="D4", hi="D5")]
VERSE2_MEL = [bar(x) for x in melody_walk(EMIN, "E5", "G4", STAB, 2, CH["verse2"], contour=(0, 0, -2, 2, -1, 1, -4, 4), lo="E4", hi="E5")]
RUN_MEL = [bar(x) for x in melody_walk(EMIN, "G4", "D5", STAB, 3, CH["run"], contour=(0, 1, 1, -1, 2, 0), lo="E4", hi="E5")]
CHORUS_MEL = [bar("R:0.5 E5:0.25 E5:0.25 R:0.5 G5:0.5 R:0.25 E5:0.25 D5:0.5 R:1"), bar("R:0.5 D5:0.25 D5:0.25 R:0.5 B4:0.75 R:0.25 G4:0.5 R:1"),
              bar("R:0.5 C5:0.25 C5:0.25 R:0.5 E5:0.5 R:0.25 C5:0.25 A4:0.5 R:1"), bar("B4:0.25 B4:0.25 R:0.5 G4:0.25 B4:0.25 R:0.5 E5:0.75 R:1.25"),
              bar("R:0.5 C5:0.25 C5:0.25 R:0.5 F5:0.5 R:0.25 C5:0.25 A4:0.5 R:1"), bar("E5:0.25 E5:0.25 R:0.5 C5:0.25 E5:0.25 R:0.5 G4:0.75 R:1.25"),
              bar("R:0.5 F#5:0.25 F#5:0.25 R:0.5 D5:0.5 R:0.25 A4:0.25 D5:0.5 R:1"), bar("D#5:0.25 D#5:0.25 R:0.5 F#4:0.25 B4:0.25 R:0.5 D#5:0.75 R:1.25"),
              bar("R:0.5 E5:0.25 E5:0.25 R:0.5 G5:0.5 R:0.25 E5:0.25 C5:0.5 R:1"), bar("R:0.5 F#5:0.25 F#5:0.25 R:0.5 C5:0.5 R:0.25 A4:0.25 F#4:0.5 R:1"),
              bar("R:0.5 E5:0.25 E5:0.25 R:0.5 B4:0.5 R:0.25 G4:0.25 E4:0.5 R:1"), bar("E5:0.25 R:0.25 E4:0.25 R:3.25")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("R:0.5 D5:0.25 D5:0.25 R:0.25 G5:0.25 D5:0.5 R:0.25 B4:0.25 G4:0.5 R:1")
CHORUS2_MEL[3] = bar("B4:0.25 B4:0.25 R:0.25 E5:0.25 G4:0.25 B4:0.25 R:0.5 E5:0.75 R:1.25")
CHORUS2_MEL[10] = bar("R:0.5 E5:0.25 E5:0.25 R:0.25 B4:0.25 E5:0.5 R:0.25 G4:0.25 E4:0.5 R:1")
CHORUS3_MEL = list(CHORUS2_MEL)
CHORUS3_MEL[0] = bar("E5:0.25 E5:0.25 R:0.25 E5:0.25 R:0.5 G5:0.5 R:0.25 E5:0.25 D5:0.5 R:1")
CHORUS3_MEL[8] = bar("E5:0.25 E5:0.25 R:0.25 E5:0.25 R:0.5 G5:0.5 R:0.25 E5:0.25 C5:0.5 R:1")
CHORUS3_MEL[11] = bar("E5:0.5! R:0.5 E4:0.5! R:2.5")
# 隠れる路地: ミュートのトランペット（2026-10-24 リズムを作り直し: 小節の終わりで伸ばさず、裏から入って途中で切る）
TRUMPET = [bar("R:1 E4:0.5 G4:0.25 C5:1.25 R:1"), bar("B4:0.75 G4:0.25 R:0.5 E4:0.5 G4:1 R:1"), bar("R:0.5 A4:0.25 C5:0.25 E5:0.5 R:0.25 G4:1.25 R:1"),
           bar("F#4:0.5 G4:0.5 R:0.5 B4:1.5 R:1"), bar("R:1.5 B4:0.25 G4:0.25 E4:1 R:1"), bar("F#4:0.75 R:0.25 A4:0.5 D5:1 R:1.5"), bar("C5:1.5 B4:0.5 R:2"),
           bar("R:0.5 E4:0.5 F#4:0.5 G4:0.5 R:2"), bar("R:1 C5:0.25 E5:0.25 G4:1.5 R:1"), bar("B4:2.5 R:1.5"), bar("R:0.5 E4:0.25 G4:0.25 B4:0.5 E5:1 R:1.5"), bar("D#5:1.5 R:2.5")]
VOICE = {"Am7": ["E3", "G3", "C4"], "Em7": ["D3", "G3", "B3"], "Cmaj7": ["E3", "G3", "B3"], "Bm7": ["D3", "F#3", "A3"], "B7sus4": ["E3", "F#3", "A3"], "B7": ["D#3", "F#3", "A3"]}
SOLO_MEL = {3: bar("D#5:0.5 F#5:0.5 A5:0.5 B5:0.5 D#6:2"), 7: bar("B5:2^^ R:2"), 11: bar("F#5:0.5 A5:0.5 B5:1 D#6:2")}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tap", "tp", "c0", "c1", "c2", "bass"]}
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
    riffkey = {"Em": "Em", "C": "C", "D": "D", "B7": "B7"}.get(base_ch, "Em")

    rf = R4
    if name in ("inter", "inter2"):
        rf = RIFF[riffkey][i % 2]
    elif name == "outro":
        rf = bar("E2:0.5! R:3.5") if i == 0 else R4
    P["riff"].append(rf)

    s = si = R4
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:2 {groot}:2") if not last else bar(f"{groot}:2! R:2")
    elif name == "run":
        s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1") if not last else bar(f"{groot}:2! {groot}:1! R:1")
    elif name.startswith("chorus"):
        s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1") if i != n - 1 else bar(f"{groot}:2! R:2")
        si = s
    elif name in ("solo", "siren") and name == "solo":
        s = bar(f"{groot}:4")
    elif name == "outro" and i == 0:
        s = si = bar("E2:0.5! R:3.5")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tapn = tp = R4; cv = [R4, R4, R4]
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name == "run": lead = RUN_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]
    elif name == "chorus3": lead = CHORUS3_MEL[i]
    elif name in ("intro", "siren"):
        tri = SIREN[{"Em": "Em", "C": "C", "B7": "B7"}[base_ch]][i % 2]
        tapn = bar(tap(tri, 4, pattern=(0, 1, 2, 1) if i % 2 == 0 else (2, 1, 0, 1)))
    elif name == "solo":
        if i in SOLO_MEL: lead = SOLO_MEL[i]
        else:
            tri = SIREN[{"Em": "Em", "C": "C", "D": "D", "B7": "B7"}[base_ch]][i % 2]
            tapn = bar(tap(tri, 3, pattern=(2, 1, 0, 1)), f"{tri[2]}:1")
    elif name == "bridge":
        tp = TRUMPET[i]
        v = VOICE[ch]
        cv = [bar(f"R:0.5 {x}:1.5 R:0.5 {x}:1.5") if not last else bar(f"{x}:2 R:2") for x in v]
    P["lead"].append(lead); P["harm8"].append(harm8); P["tap"].append(tapn); P["tp"].append(tp)
    for j in range(3): P[f"c{j}"].append(cv[j])

    if name in ("inter", "inter2"):
        b = unison_low(P["riff"][-1], -1, "B0")
    elif name == "intro":
        b = R4 if i < 2 else bar(f"{root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5 {root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5")
    elif name in ("verse", "verse2", "run", "solo", "siren"):
        b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name.startswith("chorus"):
        b = bass_root8(ch, BEATS, nxt) if i != n - 1 else bar(f"{root}:1.5! {root}:0.5 R:2")
    elif name == "bridge":
        b = bar(f"{root}:2 R:2") if i % 2 == 0 else bar(f"{root}:4")
    elif name == "outro":
        b = bar("E1:0.5! R:3.5") if i == 0 else R4
    else:
        b = R4
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    LINEAR = ["X..x..X...x..x..", "X.....X..x..x...", "X..x..X...x.....", "X..x....X.x..x.."]
    if name == "intro":
        if i == 2: k = "X.X.X.X.X.X.X.X."
        if i == 3: k = "XXXXXXXXXXXX...."; s = "............XXXX"; cym = f"R:3 {CHINA}:1!"
    elif name in ("inter", "inter2", "verse", "verse2"):
        # 速いリニアの16分（手と足が重ならない）
        k = LINEAR[i % 4]; s = "....X.......X..."
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(16))
        if i == 0: cym = (f"{CR}:1! R:3" if name in ("inter", "inter2") else f"{CR2}:1! R:3"); h = "...." + h[4:]
        if last:
            k, s, tom = linear_fill(kit, 2, i + idx); k = LINEAR[0][:8] + k[8:]; s = "....X..." + s[8:]; h = "..x.....o.......".replace("o", ".")
    elif name == "run":
        # 倍のノリ: スネアを毎拍、キックは8分
        k = "X.X.X.X.X.X.X.X."; s = "....X...X...X..."
        s = "X...X...X...X..."; k = "".join("." if s[j] != "." else c for j, c in enumerate(k)); k = "X" + k[1:]; s = "." + s[1:]
        cym = f"{RIDE}:0.5! {BELL}:0.5 {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {BELL}:0.5 {RIDE}:0.5 {BELL}:0.5"
        if i == 0: cym = f"{CR2}:1! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {BELL}:0.5 {RIDE}:0.5 {BELL}:0.5"
        if last: k = "XXXXXXXX........"; s = "........XXXXXXXX"; cym = f"R:3 {CHINA}:1!"
    elif name.startswith("chorus"):
        k = ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2] if not (name == "chorus3" and 8 <= i < 11) else "XxXxXxXxXxXxXxXx"
        s = "....X.......X..."
        h = "x.X.x.X.x.X.x.X." if not (name == "chorus3" and 8 <= i < 11) else None
        if name == "chorus3" and 8 <= i < 11: cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + "R:3"; h = h and "..X." + h[4:]
        if i == 4: cym = f"{CHINA}:1! R:3"; h = "..X." + h[4:]
        if i == n - 1:
            k, s, tom = linear_fill(kit, 2, 1); k = "X.x...X." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
    elif name == "bridge":
        # 隠れる: キックの心拍だけ、ライドを小さく
        k = "X.x............." if i % 2 == 0 else "X.x.......X.x..."
        cym = f"{RIDE}:1, {RIDE}:1, {RIDE}:1, {RIDE}:1," if i >= 4 else None
        if last: k = "X.x.X.x.X.x.X.x."; s = "........o.o.oxXX"; cym = None
    elif name == "siren":
        k = "X...X...X...X..." if i < 2 else "X.X.X.X.X.X.X.X."
        if i == 3: k = "XXXXXXXXXXXX...."; s = "............XXXX"; cym = f"R:3 {CHINA}:1!"
    elif name == "solo":
        k = "XxXxXxXxXxXxXxXx"; s = "....X.......X..."
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i % 4 == 0: cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k, s, tom = linear_fill(kit, 2, 2); k = "XxXxXxXx" + k[8:]; s = "....X..." + s[8:]; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 R:2"
    elif name == "outro":
        if i == 0: k = "X..............."; s = "X..............."; cym = f"{CR}:0.5! R:3.5"   # 一撃のあと突然の無音（シンバルも止める）
        if i == 0: cym = f"C#2:0.5! R:3.5"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and (nx.startswith("chorus") or nx == "run"): FX.append(bar("R:2 C4:2"))
    elif name == "intro" and i == 1: FX.append(bar("R:2 C4:2"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tap"), role="タッピングのギター（サイレン）", vol=0.11, pan=0.05))
song.add(part("ミュートのトランペット", "brass", J("tp"), patch="mutedTrumpet", volume=0.14, pan=0.12, reverb=0.4, phrase=8, attack=0.03, release=0.4,
              fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 1500, "high": 0}, {"type": "delay", "beats": 0.75, "mix": 0.15, "feedback": 0.3}, {"type": "plate", "mix": 0.22}]))
song.add([clean_part(J(f"c{j}"), vol=0.07, pan=[-0.3, 0.3, 0.05][j], role=f"クリーンの和音（{j + 1}）") for j in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 前奏の空気（2026-10-23 人間「だんだん小さい音が空間を広げて大きくなって盛大にスタートする感じ。ピロピロはいらない」）:
#   うねって広がるパッドが、1つの和音ごとにゆっくりふくらみ（attack 長め）、ガラスのようなプラックが左右に散って空間を広げる。前奏の小節だけで鳴る
INTRO_PAD = [["E3", "E3", "C3", "B2"], ["G3", "B3", "G3", "F#3"], ["B3", "E4", "E4", "D#4"]]
INTRO_GLASS = ["R:2 B5:1 R:1", "R:1 E6:1 R:0.5 B5:0.5 R:1", "R:0.5 G5:0.5 R:0.5 E6:0.5 R:0.5 B5:0.5 R:1", "R:0.5 D#6:0.5 B5:0.5 F#5:0.5 R:0.5 A5:0.5 F#6:0.5 R:0.5"]
for v in range(3):
    seq = [bar(f"{INTRO_PAD[v][i]}:4") if name == "intro" else R4 for name, i in SECS]
    song.add(part(f"追加の楽器: 前奏の空気（{v + 1}）", "pad", " ".join(seq), patch="sweep", volume=0.06, pan=0, reverb=0.6, attack=1.2, release=2.0, sustain=1.0))
song.add(part("追加の楽器: 前奏のきらめき", "pad", " ".join(bar(INTRO_GLASS[i]) if name == "intro" else R4 for name, i in SECS), patch="glassPluck", volume=0.05, pan=0.2, reverb=0.5,
              fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.3, "feedback": 0.4}]))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "dark-electro-rock"
add_layer(song, "synthpad", "サイレンの残響が、街の空気をふるわせる。")

# 展開の型（2026-10-23 人間「展開が全曲同じ」「4分から5分」）。lm25_plans.py
from lm25_plans import apply_plan
apply_plan(song, "14")
song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False    # 2026-10-24: 型（自動のハモリ・オクターブ上・空気の層）は使わない

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-14-siren.json"
    song.write(out)
    check_clash(song)
