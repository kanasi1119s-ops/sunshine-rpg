# ラウド25曲（第2シリーズ）04「沈黙の掟」（仮）。イメージ: マフィア。A 和声的短音階・88・4/4（ハーフタイム）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: ピアノ（左手のオクターブと右手の和音。前奏と後奏は忍び寄る単音の動機）
# しかけ:
#   - 前奏: ピアノの低い動機（A・E・C・B・A・G♯）だけ → 3小節目に全員の一撃でハーフタイムのリフへ
#   - 看板リフ: A の開放のペダルから G♯・F（和声的短音階の増2度・半音）でにじり寄る。刻まない
#   - ベースは旋律（対旋律）: Aメロでギターの代わりに歌の下でもう一本の線を弾く
#   - サビの低音: F → G♯（E7/G♯）→ A → G → F → E と下り、7小節目に ♭II（B♭maj7）で一瞬の救い
#   - ドラム: ハーフタイム（スネア3拍目）と、ずらしたスネア（2拍目の裏・4拍目の裏）。ブリッジはピアノとベースの二重奏
#   - リードはスライドと全音のチョーキング（保つ）。速弾きはしない
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 88, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 4), ("chorus", 8), ("inter", 4), ("verse2", 8), ("pre2", 4), ("chorus2", 8),
        ("bridge", 8), ("solo", 6), ("break", 4), ("chorus3", 8), ("outro", 4)]
VERSE = ["Am", "Am", "Dm/A", "Am", "Fmaj7", "Dm", "E7b9", "E7"]
PRE = ["F", "G#dim7", "Am/E", "E7"]
CHORUS = ["F", "E7/G#", "Am", "C/G", "Dm/F", "E7", "Bbmaj7", "E7"]
CH = {"intro": ["Am", "Am", "Am", "Am", "Dm", "E7b9", "Am", "E7"], "verse": VERSE, "pre": PRE, "chorus": CHORUS,
      "inter": ["Am", "Am", "Dm", "E7b9"], "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS,
      "bridge": ["Dm", "Am", "Bbmaj7", "E7", "Dm", "Am", "F", "E7sus4"], "solo": ["Am", "F", "Dm", "E7b9", "Am", "E7"],
      "break": ["A5"] * 4, "chorus3": CHORUS, "outro": ["Am", "Am", "Dm", "Am"]}
song = Song("沈黙の掟（仮）",
            "仮: ラウド25曲（第2シリーズ）の4曲目。イメージはマフィア。A 和声的短音階・88（ハーフタイム）。ピアノの忍び寄る動機から全員の一撃、"
            "G♯・F でにじり寄る看板リフ、ベースは歌の下の対旋律、サビは F→G♯→A→G→F→E と動く低音と ♭II の救い。別の楽器はピアノ。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 掟を破った男の告白。ピアノは組織の長、ベースは告白する男。"
SECS, NB = song.secs, song.nb
song.pickups = ['V1']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"Am": [bar("A1:1.5! G#2:0.5 A2:0.5 C3:0.5 B2:0.5 G#2:0.5"), bar("A1:1.5! E2:0.5 F2:1.5 E2:0.5")],
        "Dm": [bar("D2:1.5! F2:0.5 A2:0.5 C3:0.5 A2:0.5 F2:0.5")] * 2,
        "E7b9": [bar("E2:1.5! G#2:0.5 B2:1 D3:0.5 F3:0.5")] * 2,
        "E7": [bar("E2:1.5! G#2:0.5 B2:1 D3:0.5 B2:0.5")] * 2}

# ピアノの忍び寄る動機（右手）と左手のオクターブ
PNO_MOTIF = {"Am": bar("A3:0.5! E4:0.5 C4:0.5 B3:0.5 A3:0.5 G#3:0.5 A3:0.5 E3:0.5"),
             "Dm": bar("D4:0.5! A4:0.5 F4:0.5 E4:0.5 D4:0.5 C#4:0.5 D4:0.5 A3:0.5"),
             "E7b9": bar("E4:0.5! B4:0.5 G#4:0.5 F4:0.5 E4:0.5 D4:0.5 E4:0.5 B3:0.5"),
             "E7": bar("E4:0.5! B4:0.5 G#4:0.5 D4:0.5 E4:0.5 D4:0.5 B3:0.5 G#3:0.5")}
# 右手の和音（3本に分ける）
PV = {"Am": ["E4", "A4", "C5"], "Dm/A": ["F4", "A4", "D5"], "Fmaj7": ["E4", "A4", "C5"], "Dm": ["F4", "A4", "D5"], "E7b9": ["D4", "F4", "G#4"],
      "E7": ["D4", "G#4", "B4"], "F": ["F4", "A4", "C5"], "G#dim7": ["F4", "G#4", "D5"], "Am/E": ["E4", "A4", "C5"], "E7/G#": ["D4", "G#4", "B4"],
      "C/G": ["E4", "G4", "C5"], "Dm/F": ["F4", "A4", "D5"], "Bbmaj7": ["D4", "F4", "A4"], "E7sus4": ["D4", "A4", "B4"]}

VERSE_MEL = [bar("R:1 E4:0.5 A4:0.5 C5:1 B4:0.5 A4:0.5"), bar("B4:1 A4:0.5 G#4:0.5 A4:2"),
             bar("R:1 F4:0.5 A4:0.5 D5:1.5 C5:0.5"), bar("C5:1 B4:0.5 A4:0.5 E4:2"),
             bar("R:0.5 A4:0.5 C5:0.5 F5:0.5 E5:1.5 C5:0.5"), bar("D5:1 C5:0.5 A4:0.5 F4:2"),
             bar("E4:0.5 G#4:0.5 B4:0.5 D5:0.5 E5:1.5 D5:0.5"), bar("G#4:2 R:2")]
VERSE2_MEL = [bar("R:0.5 A4:0.5 C5:0.5 E5:0.5 A5:1 G#5:0.5 E5:0.5"), bar("E5:1 D5:0.5 B4:0.5 C5:2"),
              bar("R:0.5 D5:0.5 F5:0.5 A5:0.5 D6:1.5 C6:0.5"), bar("C6:1 B5:0.5 A5:0.5 E5:2"),
              bar("R:0.5 C5:0.5 F5:0.5 A5:0.5 E5:1.5 C5:0.5"), bar("D5:1 F5:0.5 A5:0.5 F5:2"),
              bar("E5:0.5 G#5:0.5 B5:0.5 D6:0.5 B5:1.5 G#5:0.5"), bar("G#5:2 R:2")]
PRE_MEL = [bar("A4:1 C5:1 F5:2"), bar("G#4:1 B4:1 F5:2"), bar("C5:1 E5:1 A5:2"), bar("G#5:1.5 E5:0.5 B4:1 R:1")]
CHORUS_MEL = [bar("R:0.5 C5:0.5 F5:0.5 A5:0.5 C6:2!"), bar("B5:1 G#5:0.5 E5:0.5 D6:2"),
              bar("C6:1.5 B5:0.5 A5:2"), bar("R:1 G5:0.5 E5:0.5 C5:2"),
              bar("R:0.5 D5:0.5 F5:0.5 A5:0.5 D6:2!"), bar("B5:1 G#5:0.5 E5:0.5 G#5:2"),
              bar("A5:1.5 F5:0.5 D6:2!"), bar("E6:2 D6:1 R:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[3] = bar("R:1 C6:0.5 G5:0.5 E5:2")
CHORUS2_MEL[5] = bar("B5:1 D6:0.5 B5:0.5 G#5:2^^")       # 全音のチョーキング（G♯→A♯ではなく、保ったまま）
CHORUS3_MEL = [bar("C6:4!"), bar("B5:2 G#5:2"), bar("A5:4!"), bar("G5:2 E5:2")] + CHORUS_MEL[4:]
# リードのソロ（スライドと全音のチョーキング。速弾きしない）
SOLO = [bar("E5:1>A5 A5:1 C6:1 B5:0.5 A5:0.5"), bar("A5:2^^ R:1 F5:0.5 A5:0.5"),
        bar("D5:1>F5 F5:1 A5:1 D6:1"), bar("D6:1.5 C6:0.5 B5:1 G#5:1"),
        bar("A5:0.5 C6:0.5 E6:1 D6:0.5 C6:0.5 A5:1"), bar("G#5:2^^ R:2")]
# ブリッジ: ベースの旋律（高めの音域）とピアノ
BASS_BRIDGE = [bar("D2:1.5 F2:0.5 A2:1 C3:1"), bar("C3:1 B2:0.5 A2:0.5 E2:2"), bar("D2:1 F2:1 A2:1 F2:1"), bar("G#2:2 B2:1 D3:1"),
               bar("D3:1.5 C3:0.5 A2:1 F2:1"), bar("E2:1 C2:0.5 E2:0.5 A2:2"), bar("A2:1 C3:1 F2:2"), bar("E2:2 D2:1 B1:1")]
VERSE_BASS = [bar("A1:1.5! E2:0.5 A2:1 G#2:1"), bar("A2:1 E2:1 C2:1 B1:1"), bar("A1:1.5 D2:0.5 F2:1 A2:1"), bar("C3:1 B2:1 A2:1 E2:1"),
              bar("F1:1.5 C2:0.5 E2:1 F2:1"), bar("D2:1 F2:1 A2:1 C3:1"), bar("E2:1 G#2:1 B2:1 D3:1"), bar("E2:1 D2:1 B1:1 G#1:1")]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm", "bass", "pl", "pr", "p0", "p1", "p2"]}
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

    # ----- リフ -----
    rf = R4
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: rf = R4
        elif name == "intro" and i == 2: rf = bar("A1:4!")
        elif name == "outro" and last: rf = bar("A1:4!")
        else:
            key = base_ch if base_ch in RIFF else "Am"
            rf = RIFF[key][i % 2]
            if name == "intro" and last: rf = bar("E2:1.5! G#2:0.5 B2:1 R:1")
    elif name == "break":
        rf = bar("A1:1.5! A1:1.5! A1:1!") if i < n - 1 else bar("A1:1.5! A#1:0.5! R:2")
    P["riff"].append(rf)

    # ----- リズムギター -----
    s = si = R4
    if name == "verse2" or (name == "verse" and i >= 4):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:2! R:2")
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

    # ----- 旋律 -----
    lead = harm = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm = shift_oct(strip_marks(lead), -1)
    elif name == "solo": lead = SOLO[i]
    P["lead"].append(lead); P["harm"].append(harm)

    # ----- ピアノ（左手・右手の単音・右手の和音） -----
    pl = pr = R4; pc = [R4, R4, R4]
    if name in ("intro", "outro"):
        key = base_ch if base_ch in PNO_MOTIF else "Am"
        if not (name == "outro" and last):
            pr = PNO_MOTIF[key]
            pl = bar(f"{root_note(ch, 'A1', 'G#2')}:2! {root_note(ch, 'A1', 'G#2')}:2,") if i >= 2 or name == "outro" else bar(f"{root_note(ch, 'A1', 'G#2')}:4")
        else:
            pl = bar("A1:4!"); pc = [bar("E4:4"), bar("A4:4"), bar("C5:4")]
    elif name == "verse2" and ch in PV:
        # 右手の和音を裏拍に置く（2拍目の裏・4拍目）。左手は1拍目の低いオクターブ
        pc = [bar(f"R:1.5 {v}:1 R:0.5 {v}:1,") for v in PV[ch]] if not last else [bar(f"{v}:2 R:2") for v in PV[ch]]
        pl = bar(f"{root_note(ch, 'A1', 'G#2')}:2! R:2")
    elif name == "bridge" and ch in PV:
        pc = [bar(f"{v}:2 {v}:2,") for v in PV[ch]]
        pl = bar(f"{root_note(ch, 'A1', 'G#2')}:4")
        if i % 2 == 1: pr = bar(f"R:2 {up(PV[ch][2], 1)}:1 {up(PV[ch][1], 1)}:1")
    elif name == "chorus3" and i < 4 and ch in PV:
        pc = [bar(f"{v}:4") for v in PV[ch]]
        pl = bar(f"{root_note(ch, 'A1', 'G#2')}:4!")
    P["pl"].append(pl); P["pr"].append(pr)
    for v in range(3): P[f"p{v}"].append(pc[v])

    # ----- ベース（旋律を弾く） -----
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: b = R4
        elif name == "intro" and i == 2: b = bar("A1:4!")
        elif name == "outro" and last: b = bar("A1:4!")
        else: b = unison_low(P["riff"][-1], -1, "B0") if not (name == "intro" and last) else bar("E1:1.5! G#1:0.5 B1:1 R:1")
    elif name == "verse": b = VERSE_BASS[i]
    elif name == "verse2": b = bass_root8(ch, BEATS, nxt) if not last else bar("E1:1! E2:1 R:2")
    elif name in ("pre", "pre2"):
        b = bar(" ".join(f"{root}:0.5{'!' if j % 4 == 0 else ''}" for j in range(8))) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:3! {root}:1")
        elif last and name != "chorus3": b = bar(f"{root}:1.5! {root}:0.5 R:2")
        else: b = bass_root8(ch, BEATS, nxt)
    elif name == "bridge": b = BASS_BRIDGE[i]
    elif name == "solo": b = bass_root8(ch, BEATS, nxt)
    elif name == "break": b = unison_low(P["riff"][-1], -1, "B0")
    else: b = R4
    P["bass"].append(b)

    # ----- ドラム（ハーフタイム中心、ずらしたスネア） -----
    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2:
            # ピアノの下: ライドのベルと、フロアタムの心拍
            k = "X.......X......." if i == 0 else "X.......X...X.X."
            cym = f"{BELL}:1 {RIDE}:1 {BELL}:1 {RIDE}:1"
            tom = "R:3 A2:1," if i == 0 else "R:2 A2:0.5 A2:0.5 D3:0.5 A2:0.5"
        elif name == "intro" and i == 2:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "outro" and last:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        else:
            k = "X.....x.X.....x." if i % 2 == 0 else "X.....x.X..x...."
            s = "........X......."
            s = "".join("o" if j in (6, 14) and k[j] == "." else c for j, c in enumerate(s))
            h = "x.x.x.x.x.x.x.x."
            if name == "inter" and i == 0: cym = f"{CHINA}:1! R:3"; h = "..x.x.x.x.x.x.x."
            if last and name != "outro":
                k = "X.....x........."; s = "........"; s = s + "X.X.XXXX"; h = None; tom = "R:2 F3:0.25 F3:0.25 D3:0.25 D3:0.25 A2:0.25 A2:0.25 A2:0.25! A2:0.25!"
                s = "................"
    elif name in ("verse", "verse2"):
        # ずらしたスネア: 3拍目（ハーフタイム）と、ときどき2拍目の裏・4拍目の裏
        k = ["X..x....X.......", "X.....x...X.....", "X..x....X..x....", "X.....x.X......."][i % 4]
        s = ["........X......o", "......X.........X"[:16], "........X.....X.", ".......X....X..."][i % 4]
        h = "x.x.x.x.x.x.x.x." if name == "verse" else None
        if name == "verse2": cym = f"{RIDE}:1! {BELL}:0.5 {RIDE}:0.5 {RIDE}:1! {BELL}:0.5 {RIDE}:0.5"
        if i == 0: cym = f"{CR2}:2! " + (f"{RIDE}:1! {BELL}:0.5 {RIDE}:0.5" if name == "verse2" else "R:2")
        if last:
            k = "X..x............"; s = "........X..X.XXX"; h = None; cym = f"{RIDE}:1 {RIDE}:1 R:2" if name == "verse2" else None
    elif name in ("pre", "pre2"):
        k = ["X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XxXxXxXx........"][i]
        s = ["........X.......", "....X.......X...", "....X.......X...", "........X.X.X.X."][i]
        h = ["x...x...x...x...", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", None][i]
        if i == 0: cym = f"{CR2}:2! R:2"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = "X.........X....."; s = "........X......."
            cym = f"{CR}:4!" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        else:
            # サビはハーフタイムのまま、キックで押す。4・8小節目だけフルのノリ
            if i % 4 == 3 and not last:
                k = "X.X...X.X.X...X."; s = "....X.......X..X"; h = None
            else:
                k = ["X..x....X.X.....", "X..x..X...X.....", "X..x....X.X...x.", "X......XX......."][i % 4]
                s = "........X......."
                s = "".join("o" if j in (11, 15) and k[j] == "." else c for j, c in enumerate(s))
            cym = f"{CHINA}:1! {RIDE}:1 {CHINA}:1! {RIDE}:1" if i % 8 >= 4 else f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
            if i % 4 == 0: cym = (f"{CR}:2! " if i % 8 == 0 else f"{CR2}:2! ") + (f"{CHINA}:1! {RIDE}:1" if i % 8 >= 4 else f"{RIDE}:1! {BELL}:1")
            if name == "chorus2" and i in (4, 5): k = "XxXxXxXx" + "X..x...."     # 2回目だけツーバスの半小節
        if last and name != "chorus3":
            k = "X..x............"; s = "........"; s += "X.X.X.XX"; cym = f"{RIDE}:1! {RIDE}:1 R:2"; h = None
            tom = "R:2 F3:0.25 F3:0.25 R:0.25 D3:0.25 R:0.25 A2:0.25 R:0.5"
            s = "........X.X.X..X"
        if name == "chorus3" and last:
            k = "X..x....X.X....."; s = "........X......."; cym = f"{CR}:2! {RIDE}:1 {RIDE}:1"
    elif name == "bridge":
        # 二重奏: ブラシのようなライド、キックは弱く、フロアタムで呼吸
        k = "o.......o......." ; s = "................" if i < 4 else "........o......."
        cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1"
        tom = "R:3 A2:1," if i % 2 == 1 else None
        if i == 0: cym = f"{CR2}:2 {RIDE}:1 {RIDE}:1"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 R:2"
    elif name == "solo":
        k = ["X..x....X.X.....", "X..x..X...X....."][i % 2]
        s = "........X......."
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 " * 2
        cym = cym.strip()
        if i == 0: cym = f"{CR}:1! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k = "X..x............"; s = "........"; s += "X.XX.XXX"; cym = f"{RIDE}:1 {RIDE}:1 R:2"
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
    if name == "intro" and i == 1: FX.append(bar("R:2 C4:2"))
    elif i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:2 C4:2"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:3 D4:1"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
PIANO = dict(volume=0.13, reverb=0.3, fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}, {"type": "plate", "mix": 0.15}])
song.add(part("ピアノ（左手）", "piano", J("pl"), pan=-0.1, **{**PIANO, "volume": 0.14}))
song.add(part("ピアノ（右手の動機）", "piano", J("pr"), pan=0.05, **PIANO))
song.add([part(f"ピアノ（右手の和音{v + 1}）", "piano", J(f"p{v}"), pan=0.1, **{**PIANO, "volume": 0.09}) for v in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "bright-nu-wall"
add_layer(song, "strings", "告白のあと、弔いの弦が静かに掟を語る。")

# 展開の型（2026-10-23 人間「展開が全曲同じ」「4分から5分」）。lm25_plans.py
from lm25_plans import apply_plan
apply_plan(song, "04")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-04-okite.json"
    song.write(out)
    check_clash(song)
