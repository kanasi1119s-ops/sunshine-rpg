# ラウド25曲（第2シリーズ）07「羽の落ちる速さ」（仮）。イメージ: 天使。E リディアン・120・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: ハープ（3オクターブの分散和音。前奏・ブリッジ・最後のサビのきらめき）
# しかけ:
#   - リディアン（♯4＝A♯）の浮く明るさ。Aメロは E の上で F♯/E（Ⅱの長三和音）が揺れる
#   - 看板リフ: 低い E のペダルから、高い弦の音が羽のように下りてくる（刻まない）
#   - Aメロのベースはスラップ（親指・はじく・ゴースト）。ドラムは 4つの中に3つ（付点8分のキックとベル）のポリリズム
#   - サビ: Ⅳ（A）から開け、F♯/A♯（リディアンのⅡ）で持ち上げ、7小節目に ♭Ⅲ（Gmaj7。半音下の別の光）。主和音 E は16小節目まで取っておく
#   - 間奏とソロはタッピング（右手で高い音を叩き、左手の2音へ引っかける6連）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 120, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 4), ("chorus", 16), ("inter", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 16),
        ("bridge", 8), ("solo", 8), ("break", 4), ("chorus3", 16), ("outro", 4)]
VERSE = ["E", "F#/E", "E", "F#/E", "C#m", "G#m", "A", "B"]
PRE = ["C#m", "B/D#", "E", "F#"]
CHORUS = ["A", "B", "G#m", "C#m", "F#/A#", "B", "Gmaj7", "B", "A", "B", "G#m", "C#m", "Amaj7", "B", "Gmaj7", "E"]
RIFFCH = ["E", "F#/E", "E", "F#/E", "C#m", "B", "A", "B"]
CH = {"intro": RIFFCH, "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": RIFFCH, "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS,
      "bridge": ["Emaj7", "F#/E", "Emaj7", "F#/E", "C#m7", "G#m7", "Amaj7", "B"], "solo": RIFFCH, "break": ["E5"] * 4,
      "chorus3": CHORUS, "outro": ["E", "F#/E", "E", "E5"]}
song = Song("羽の落ちる速さ（仮）",
            "仮: ラウド25曲（第2シリーズ）の7曲目。イメージは天使。E リディアン・120。低い E のペダルから高い音が羽のように下りる看板リフ、Aメロはスラップのベースと"
            "4つの中に3つのポリリズム、サビは A から開けて F♯/A♯ で持ち上げ、Gmaj7 で別の光。間奏とソロはタッピング。別の楽器はハープ。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.extra["modulate"] = {"at": "lastChorus", "semitones": 1}   # 見せ場: 最後のサビで半音上へ（天へ上がる）
song.desc += " 物語: 天使が地上へ落ち、タッピングで再び飛び立ち、最後のサビで半音上の空へ。"
SECS, NB = song.secs, song.nb
song.pickups = ['V3', 'V0', 'V2']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"E": bar("E2:0.5! B3:0.5 A#3:0.5 F#3:0.5 E2:0.5! G#3:0.5 F#3:0.5 D#3:0.5"),
        "F#/E": bar("E2:0.5! C#4:0.5 A#3:0.5 F#3:0.5 E2:0.5! A#3:0.5 G#3:0.5 F#3:0.5"),
        "C#m": bar("C#2:0.5! G#3:0.5 E3:0.5 C#3:0.5 C#2:0.5! B3:0.5 G#3:0.5 E3:0.5"),
        "B": bar("B1:0.5! F#3:0.5 D#3:0.5 B2:0.5 B1:0.5! C#3:0.5 D#3:0.5 F#3:0.5"),
        "A": bar("A1:0.5! E3:0.5 C#3:0.5 A2:0.5 A1:0.5! B2:0.5 C#3:0.5 E3:0.5")}

VERSE_MEL = [bar("R:1 B3:0.5 E4:0.5 G#4:1 A#4:0.5 B4:0.5"), bar("A#4:2 F#4:1 R:1"),
             bar("R:0.5 G#4:0.5 B4:0.5 D#5:0.5 C#5:1.5 B4:0.5"), bar("C#5:1 A#4:1 F#4:2"),
             bar("R:1 E4:0.5 G#4:0.5 C#5:2"), bar("B4:1 D#5:1 G#4:2"),
             bar("C#5:1.5 B4:0.5 A4:1 E4:1"), bar("D#4:1 F#4:1 B4:1 R:1")]
VERSE2_MEL = [bar("R:0.5 E5:0.5 G#5:0.5 B5:0.5 A#5:1 G#5:0.5 F#5:0.5"), bar("A#5:1.5 C#6:0.5 A#5:2"),
              bar("R:0.5 B4:0.5 E5:0.5 G#5:0.5 C#6:1.5 B5:0.5"), bar("C#6:1 A#5:1 F#5:2"),
              bar("R:0.5 E5:0.5 G#5:0.5 C#6:0.5 E5:2"), bar("D#5:1 F#5:1 B5:2"),
              bar("C#6:1.5 B5:0.5 A5:1 E5:1"), bar("D#5:1 F#5:1 B5:1 R:1")]
PRE_MEL = [bar("E4:1 G#4:1 C#5:2"), bar("F#4:1 B4:1 D#5:2"), bar("G#4:1 B4:1 E5:2"), bar("A#4:1 C#5:1 F#5:1 R:1")]
CHORUS_MEL = [bar("R:0.5 C#5:0.5 E5:0.5 A5:0.5 B5:2"), bar("F#5:1 D#5:0.5 F#5:0.5 B5:2"),
              bar("R:0.5 D#5:0.5 G#5:0.5 B5:0.5 D#6:2"), bar("C#6:1 B5:0.5 G#5:0.5 E5:2"),
              bar("R:0.5 C#5:0.5 F#5:0.5 A#5:0.5 C#6:2"), bar("D#6:1 C#6:0.5 B5:0.5 F#5:2"),
              bar("R:0.5 D5:0.5 G5:0.5 B5:0.5 D6:2!"), bar("D#6:2 C#6:1 R:1"),
              bar("R:0.5 E5:0.5 A5:0.5 C#6:0.5 E6:2!"), bar("D#6:1 C#6:0.5 B5:0.5 F#5:2"),
              bar("R:0.5 B4:0.5 D#5:0.5 G#5:0.5 B5:2"), bar("G#5:1 E5:0.5 C#5:0.5 E5:2"),
              bar("R:0.5 C#5:0.5 E5:0.5 G#5:0.5 C#6:2"), bar("B5:1 A#5:0.5 F#5:0.5 D#5:2"),
              bar("D6:1.5 B5:0.5 F#5:2"), bar("E5:2 G#5:1 R:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("F#5:1 B5:0.5 D#6:0.5 B5:2")
CHORUS2_MEL[9] = bar("D#6:1 B5:0.5 F#5:0.5 D#5:2")
CHORUS2_MEL[5] = bar("D#6:1 C#6:1 D#6:2")
CHORUS2_MEL[11] = bar("G#5:1 C#6:0.5 G#5:0.5 E5:2")
CHORUS2_MEL[13] = bar("B5:1 D#6:0.5 B5:0.5 F#5:2")
CHORUS3_MEL = [bar("C#6:4!"), bar("B5:2 D#6:2"), bar("D#6:4!"), bar("E6:2 C#6:2")] + CHORUS_MEL[4:6] + [bar("B5:1 D6:1 G5:2!"), CHORUS_MEL[7]] + CHORUS_MEL[8:10] + [bar("R:0.5 D#5:0.5 G#5:0.5 B5:0.5 D#6:2"), CHORUS_MEL[11], bar("E6:1.5 C#6:0.5 G#5:2")] + CHORUS_MEL[13:]

TAP = {"E": ["G#4", "B4", "E5"], "F#/E": ["A#4", "C#5", "F#5"], "C#m": ["G#4", "C#5", "E5"], "B": ["F#4", "B4", "D#5"], "A": ["E4", "A4", "C#5"]}
TAP_PAT = [(2, 1, 0, 1), (2, 0, 1, 0), (2, 1, 0, 1), (0, 1, 2, 1)]
SOLO_MEL = [bar("R:0.5 E5:0.5 G#5:0.5 B5:0.5 C#6:2^^"), bar("D#6:1 B5:1 F#5:2"), bar("R:0.5 A5:0.5 C#6:0.5 E6:0.5 C#6:2"), bar("B5:2^^ R:2")]

# スラップ（Aメロ）: T 親指・P はじく・F 5度・S ♭7（ここでは長7）・g ゴースト
SLAP = ["T..gP.T.gTP.T.gP", "T.gP..TgP.T.gPT.", "T..gP.T.gTP.FgP.", "T.gPT.gP.TgP.T.g"]

# ハープ: 3オクターブの分散和音（下から上へ、上で折り返す）
def harp_bar(ch, lo="A2", hi="E6", step=0.25):
    t = chord_tones(ch.split("/")[0], lo, hi)
    seq = (t + t[-2:0:-1])
    n = int(BEATS / step)
    return bar(" ".join(f"{seq[i % len(seq)]}:{step}{'!' if i == 0 else ''}" for i in range(n)))


P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tap", "harp", "bass", "pop", "mute"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
POLY_BELL = f"{BELL}:0.75! {RIDE}:0.75 {BELL}:0.75 {RIDE}:0.75 {BELL}:0.75 {RIDE}:0.25"   # 付点8分（3つの16分）のベル

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
    if name in ("intro", "outro") or (name == "inter" and i < 4):
        if name == "intro" and i < 2: rf = bar("E2:4!") if i == 0 else R4
        elif name == "outro" and last: rf = bar("E2:4!")
        else:
            rf = RIFF[ch if ch in RIFF else "E"]
            if name == "intro" and last: rf = bar("B1:0.5! F#3:0.5 D#3:0.5 B2:0.5 B1:2!")
    elif name == "break":
        rf = bar("E2:0.75! E2:0.75! E2:2.5!") if i < n - 1 else bar("E2:0.75! E2:0.75! A#2:0.5! R:2")
    P["riff"].append(rf)

    # ----- リズムギター -----
    s = si = R4
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:2! {groot}:1! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:4!")
        elif i in (7, 15) and not (name == "chorus3" and i == 15): s = bar(f"{groot}:2! R:2")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1")
        si = s if not (name == "chorus3" and i < 4) else R4
    elif name in ("inter", "solo") and (i >= 4 or name == "solo"):
        s = bar(f"{groot}:4")
    elif name == "break":
        s = si = P["riff"][-1]
    P["rhy"].append(s); P["rhy_in"].append(si)

    # ----- 旋律・タッピング・ハープ -----
    lead = harm8 = tapn = harp = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm8 = shift_oct(strip_marks(lead), -1)
        if i >= 12: harp = harp_bar(ch, "E4", "E6", 0.25)
    elif (name == "inter" and i >= 4) or (name == "solo" and i < 4) or (name == "intro" and i == 1):
        tri = TAP[ch if ch in TAP else "E"]
        tapn = bar(tap(tri, 3, pattern=TAP_PAT[i % 4]), f"{tri[2]}:1")
    elif name == "solo": lead = SOLO_MEL[i - 4]
    if (name == "intro" and i == 0) or name == "bridge":
        harp = harp_bar(ch)
    P["lead"].append(lead); P["harm8"].append(harm8); P["tap"].append(tapn); P["harp"].append(harp)

    # ----- ベース -----
    pop = mute = R4
    if name in ("intro", "outro") or (name == "inter" and i < 4):
        if name == "intro" and i < 2: b = bar("E1:4!") if i == 0 else bar("E1:4")
        elif name == "outro" and last: b = bar("E1:4!")
        else: b = bass_root8(ch, BEATS, nxt)
    elif name == "verse":
        if last: b = bar(f"{root}:1! {root}:1 R:2")
        else:
            b, mute = bass_slap_bar(ch, BEATS, SLAP[i % 4])
            pt, mt = [], []
            for t in b.split():
                if t.endswith("'"): pt.append(t); mt.append("R:" + t.split(":")[1].rstrip("'"))
                else: pt.append("R:" + t.split(":")[1].rstrip("!'")); mt.append(t)
            pop = merge_rests(" ".join(pt)); b = merge_rests(" ".join(mt))
    elif name in ("verse2", "pre", "pre2", "inter", "solo"):
        b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:3! {root}:1")
        elif i in (7, 15) and not (name == "chorus3" and i == 15): b = bar(f"{root}:1.5! {root}:0.5 R:2")
        elif name == "chorus3" and i == 15: b = bar(f"{root}:4!")
        else: b = bass_root8(ch, BEATS, nxt)
    elif name == "bridge":
        b = bar(f"{root}:2 {fifth_of(base_ch)}:2") if i % 2 else bar(f"{root}:4")
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R4
    P["bass"].append(b); P["pop"].append(pop); P["mute"].append(mute)

    # ----- ドラム -----
    k = s = h = None; tom = cym = None
    if name in ("intro", "outro") or (name == "inter" and i < 4):
        if name == "intro" and i == 0:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "intro" and i == 1:
            cym = f"{BELL}:0.75 {BELL}:0.75 {BELL}:0.75 {BELL}:0.75 R:1"; k = "X.....X........."; tom = "R:3 " + tom_16_down(1)
        elif name == "outro" and last:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        else:
            # 4つの中に3つ: キックとベルは付点8分、スネアは2・4
            k = "X..X..X..X..X..."; s = "....X.......X..."
            k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
            cym = POLY_BELL
            if (name == "intro" and i == 2) or (name == "inter" and i == 0): cym = f"{CR}:0.75! " + POLY_BELL.split(" ", 1)[1]
            if last and name == "intro":
                k = "X..X..X........."; s = "....X..........."; tom = "R:2 " + tom_triplets_down(2); cym = f"{BELL}:0.75! {RIDE}:0.75 {BELL}:0.5 R:2"
    elif name == "verse":
        # スラップの下: リニアの16分（手と足が重ならない）、スネアのゴースト
        k = ["X..x......X.....", "X.....X..x......", "X..x......X..x..", "X.....X...x....."][i % 4]
        s = "....X.......X..."
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(16))
        if i == 0: cym = f"{CR2}:1! R:3"; h = "...." + h[4:]
        if last:
            k = "X..x....X......."; s = "....X..........."; h = None; tom = "R:2 " + tom_triplets_down(2)
    elif name == "verse2":
        k = "X..X..X..X..X..."; s = "....X.......X..."
        k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = POLY_BELL
        if i == 0: cym = f"{CR2}:0.75! " + POLY_BELL.split(" ", 1)[1]
        if last: k = "X..X..X........."; s = "....X..........."; tom = "R:2 " + tom_triplets_down(2); cym = f"{BELL}:0.75! {RIDE}:0.75 {BELL}:0.5 R:2"
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
        elif 8 <= i < 12:
            # サビの後半の頭: 4つの中に3つのベルで浮かせる
            k = "X..X..X..X..X..."; s = "....X.......X..."
            k = "".join("." if s[j] != "." else c for j, c in enumerate(k)); cym = POLY_BELL
            if i == 8: cym = f"{CR}:0.75! " + POLY_BELL.split(" ", 1)[1]
        else:
            k = ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2]
            s = "....X.......X..." if i % 4 != 3 else "....X.......X.oo"
            h = "x.X.x.X.x.X.x.X."
            if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + "R:3"
            if name == "chorus2" and i in (12, 13): k = "XxXxXxXxXxXxXxXx"; h = None; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5" if i == 13 else f"{CR2}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i in (7, 15) and not (name == "chorus3" and i == 15):
            k = "X.x...X........."; s = "....X..........."; h = None; tom = "R:2 " + tom_triplets_down(2); cym = None
        if name == "chorus3" and i == 15:
            k = "X..............."; s = "X..............."; h = None; cym = f"{CR}:4!"
    elif name == "inter" or name == "solo":
        # タッピングの下: ツーバスの16分＋ライド
        k = "XxXxXxXxXxXxXxXx"; s = "....X.......X..."
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if (name == "inter" and i == 4) or (name == "solo" and i in (0, 4)): cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if name == "solo" and i >= 4:
            k = "X..X..X..X..X..."; k = "".join("." if j in (4, 12) else c for j, c in enumerate(k)); cym = POLY_BELL if i != 4 else f"{CR}:0.75! " + POLY_BELL.split(" ", 1)[1]
        if last: k = "X..X..X........."; s = "....X..........."; tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 R:2"
    elif name == "bridge":
        k = "X.........X....." if i % 2 == 0 else "X.....X........."
        s = "................" if i < 4 else "....o.......o..."
        cym = f"{RIDE}:0.75 {RIDE}:0.75 {BELL}:0.75 {RIDE}:0.75 {RIDE}:0.75 {RIDE}:0.25"
        if i == 0: cym = f"{CR2}:1.5 {RIDE}:0.75 {RIDE}:0.75 {RIDE}:0.75 {RIDE}:0.25"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 R:2"
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
    elif name == "intro" and i == 0: FX.append(R4)
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tap"), role="タッピングのギター", vol=0.11, pan=0.05))
song.add(part("ハープ", "harp", J("harp"), volume=0.13, pan=-0.3, reverb=0.45, attack=0.002, release=1.2,
              fx=[{"type": "eq", "low": -4, "mid": 0, "midHz": 1500, "high": 1.5}, {"type": "delay", "beats": 0.75, "mix": 0.15, "feedback": 0.3}, {"type": "plate", "mix": 0.25}]))
song.add(bass_part(J("bass")))
song.add(slap_pop_part(J("pop")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-07-hane.json"
    song.write(out)
    check_clash(song)
