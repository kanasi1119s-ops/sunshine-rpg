# ラウド25曲（第2シリーズ）21「群青の滑走路」（仮）。イメージ: 空（滑走路から雲の上へ）。D 長調 → E♭ → E・140・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: バイオリン（柔らかく力強く透き通る。滑走路の朝・雲の上の独奏・最後の空）
# 物語: 滑走路で待つ → 走り出す（Bメロの加速）→ 離陸（サビ）→ 雲の中（スウィープ）→ 雲の上（バイオリン）→ さらに高く（調が上がる）。
# 形（ほかの曲と変える）: 転調を重ねて上がり続ける。1回目のサビ D → 2回目 E♭（半音上）→ 雲の上とソロも E♭ → 3回目のサビと後奏は E（さらに半音上）。
#   長調の曲。ブレイクダウンなし
# しかけ:
#   - サビ7小節目の B♭（♭Ⅵ）で機体が浮く。サビは G から開け、主和音 D は4小節目まで取っておく
#   - ドラム: アクセントの位置が小節ごとにずれていく（ずらしたアクセントの疾走）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 140, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 8), ("chorus", 16), ("cloud", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 16),
        ("above", 8), ("solo", 8), ("chorus3", 16), ("outro", 8)]
OFF = {"intro": 0, "verse": 0, "pre": 0, "chorus": 0, "cloud": 0, "verse2": 0, "pre2": 0, "chorus2": 1, "above": 1, "solo": 1, "chorus3": 2, "outro": 2}
VERSE = ["D", "A/C#", "Bm", "G", "D", "A/C#", "Em7", "A"]
PRE = ["Em7", "F#m7", "Gmaj7", "A", "Bm7", "C", "G", "A"]
CHORUS = ["G", "D/F#", "Em7", "D", "G", "A/C#", "Bb", "A", "G", "D/F#", "Em7", "D/F#", "Gmaj7", "A", "F#m7", "Bm"]
BASE = {"intro": ["D", "D", "Bm", "A", "D", "D", "G", "A"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "cloud": ["Bm", "G", "D", "A", "Bm", "G", "Em", "A"],
        "verse2": VERSE, "pre2": PRE[4:], "chorus2": CHORUS, "above": ["Gmaj7", "A", "F#m7", "Bm7", "Em7", "F#m7", "Gmaj7", "A7sus4"],
        "solo": ["Bm", "G", "D", "A", "Bm", "G", "Em", "A"], "chorus3": CHORUS[:15] + ["D"], "outro": ["D", "A/C#", "Bm", "G", "D", "G", "A", "D"]}
CH = {k: [tr_chord(c, OFF[k]) for c in v] for k, v in BASE.items()}
song = Song("群青の滑走路（仮）",
            "仮: ラウド25曲（第2シリーズ）の21曲目。イメージは空（滑走路から雲の上へ）。D 長調・140。転調を重ねて上がり続ける形: 1回目のサビ D、2回目 E♭、3回目と後奏は E。"
            "サビは G から開け、♭Ⅵ（B♭）で機体が浮く。雲の中はスウィープ、雲の上はバイオリンの独奏。アクセントが小節ごとにずれる疾走のドラム。別の楽器はバイオリン。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 滑走路で待ち、走り出し、離陸し、雲の中を抜け、雲の上へ、さらに高く。"
song.kinds = {"cloud": "interlude", "above": "bridge"}
SECS, NB = song.secs, song.nb

RIFF = {"D": bar("D2:0.5! A2:0.5 D3:0.5 E3:0.5 F#3:0.5 E3:0.5 D3:0.5 A2:0.5"), "Bm": bar("B1:0.5! F#2:0.5 B2:0.5 C#3:0.5 D3:0.5 C#3:0.5 B2:0.5 F#2:0.5"),
        "A": bar("A1:0.5! E2:0.5 A2:0.5 B2:0.5 C#3:0.5 B2:0.5 A2:0.5 E2:0.5"), "G": bar("G1:0.5! D2:0.5 G2:0.5 A2:0.5 B2:0.5 A2:0.5 G2:0.5 D2:0.5"),
        "Em": bar("E2:0.5! B2:0.5 E3:0.5 F#3:0.5 G3:0.5 F#3:0.5 E3:0.5 B2:0.5")}
VERSE_MEL = [bar("R:1 F#4:0.5 A4:0.5 D5:1 C#5:1"), bar("B4:1 C#5:1 E5:2"), bar("R:0.5 D5:0.5 F#5:0.5 E5:0.5 D5:2"), bar("B4:1 D5:1 G4:2"),
             bar("R:1 A4:0.5 D5:0.5 F#5:1.5 E5:0.5"), bar("E5:2 A4:2"), bar("G4:1 B4:1 D5:2"), bar("C#5:2 E5:1 R:1")]
VERSE2_MEL = [bar("R:1 A4:0.5 D5:0.5 F#5:1 E5:1"), bar("C#5:1 E5:1 A5:2"), bar("R:0.5 F#5:0.5 B5:0.5 A5:0.5 F#5:2"), bar("D5:1 G5:1 B5:2"),
              bar("R:1 D5:0.5 F#5:0.5 A5:1.5 G5:0.5"), bar("A5:2 E5:2"), bar("B4:1 E5:1 G5:2"), bar("E5:2 C#5:1 R:1")]
PRE_MEL = [bar("E5:1 G5:1 B4:2"), bar("F#5:1 A5:1 C#5:2"), bar("G5:1 B5:1 F#5:2"), bar("A5:2 E5:2"),
           bar("B5:1 D6:1 F#5:2"), bar("C6:1 G5:1 E5:2"), bar("B5:1 D6:1 G5:2"), bar("A5:2 C#6:1 R:1")]
CHORUS_MEL = [bar("R:0.5 D5:0.5 G5:0.5 B5:0.5 D6:2!"), bar("C#6:1 A5:1 F#5:2"), bar("R:0.5 E5:0.5 G5:0.5 B5:0.5 D6:2"), bar("A5:1 F#5:1 D5:2"),
              bar("R:0.5 D5:0.5 G5:0.5 B5:0.5 E6:2!"), bar("C#6:1 A5:1 E5:2"), bar("F5:1 A#5:1 D6:2!"), bar("C#6:2 A5:1 R:1"),
              bar("B5:1 D6:1 B5:2"), bar("A5:1 F#5:1 D6:2"), bar("G5:1 B5:1 E6:2"), bar("D6:2 A5:2"),
              bar("R:0.5 D5:0.5 F#5:0.5 B5:0.5 D6:2"), bar("E6:2! C#6:1 A5:1"), bar("C#6:1 A5:1 E5:2"), bar("D6:2 B5:1 R:1")]


def top_ok(s, top="E6"):
    """ギターの出ない高さ（E6 より上）は1オクターブ下げる"""
    return " ".join(t if t.startswith("R") or midi(tok_note(t)) <= midi(top) else up(tok_note(t), -1) + ":" + t.split(":", 1)[1] for t in s.split())


CHORUS2_MEL = [top_ok(transpose(x, 1)) for x in CHORUS_MEL]
CHORUS2_MEL[4] = bar("R:0.5 D#5:0.5 G#5:0.5 C6:0.5 D#6:2!")
CHORUS2_MEL[13] = bar("D6:2! A#5:1 F5:1")
CHORUS3_MEL = [top_ok(transpose(x, 2)) for x in CHORUS_MEL]
CHORUS3_MEL[0] = bar("R:0.5 E5:0.5 A5:0.5 C#6:0.5 E6:2!")
CHORUS3_MEL[4] = bar("R:0.5 E5:0.5 A5:0.5 C#6:0.5 E6:2!")
CHORUS3_MEL[10] = bar("A5:1 C#6:1 E6:2")
CHORUS3_MEL[13] = bar("D#6:2! B5:1 F#5:1")
CHORUS3_MEL[15] = bar("E6:4!")
# バイオリン
VLN_INTRO = [bar("A5:4"), bar("F#5:2 A5:2"), bar("B5:4"), bar("A5:2 E5:2"), bar("D6:4"), bar("D6:2 A5:2"), bar("B5:3 D6:1"), bar("C#6:4")]
VLN_ABOVE = [bar("R:1 B5:1 D6:1 F#6:1"), bar("E6:3 C#6:1"), bar("A5:2 C#6:1 E6:1"), bar("D6:4"), bar("R:1 G5:1 B5:1 D6:1"), bar("C#6:2 A5:1 C#6:1"), bar("B5:1 D6:1 F#6:2"), bar("E6:4")]
VLN_OUTRO = [bar("A5:2 D6:2"), bar("C#6:2 E6:2"), bar("F#6:4"), bar("D6:2 B5:2"), bar("A5:2 F#6:2"), bar("G6:2 D6:2"), bar("E6:2 C#6:2"), bar("D6:4")]
VLN_C3 = [bar("D6:4"), bar("D6:2 A5:2"), bar("B5:2 E6:2"), bar("F#6:4"), bar("F#6:2 D6:2"), bar("E6:4"), bar("C#6:4"), bar("D6:4")]
SWEEP_R = {"Bm": ("D4", "B5"), "G": ("D4", "B5"), "D": ("D4", "A5"), "A": ("C#4", "A5"), "Em": ("E4", "B5")}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "tech", "vln", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    off = OFF[name]
    bch = BASE[name][i]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)
    T = lambda s: transpose(s, off) if off else s

    rf = R4
    if name in ("intro", "cloud") or (name == "outro" and not last):
        key = {"D": "D", "Bm": "Bm", "A": "A", "G": "G", "Em": "Em", "A/C#": "A"}.get(bch, "D")
        rf = T(RIFF[key]) if not (name == "intro" and i < 2) else R4
    elif name == "outro" and last:
        rf = bar(f"{groot}:4!")
    P["riff"].append(rf)

    s = si = R4
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:2! {groot}:1! R:1")
    elif name.startswith("chorus"):
        s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1") if not (last and name != "chorus3") else bar(f"{groot}:2! R:2")
        if name == "chorus3" and last: s = bar(f"{groot}:4!")
        si = s
    elif name in ("solo", "above"):
        s = bar(f"{groot}:4")
    elif name == "outro" and last:
        si = bar(f"{groot}:4!")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = tech = vln = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name == "pre": lead = PRE_MEL[i]
    elif name == "pre2": lead = PRE_MEL[4 + i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
        if i >= 8: vln = transpose(VLN_C3[i - 8], 2)
    elif name in ("cloud", "solo"):
        lo, hi = SWEEP_R[{"A/C#": "A"}.get(bch, bch)]
        lo2, hi2 = tr(lo, off), tr(hi, off)
        if name == "cloud" and i < 4: tech = R4
        elif i in (3, 7): tech = T(bar("C#5:0.5 E5:0.5 A5:0.5 C#6:0.5 A5:2")) if i == 7 else T(bar("A5:2^^ C#6:2"))
        else: tech = bar(sweep(ch, lo2, hi2, 2), sweep(ch, lo2, hi2, 2))
    elif name == "intro": vln = VLN_INTRO[i]
    elif name == "above": vln = transpose(VLN_ABOVE[i], 1)
    elif name == "outro": vln = transpose(VLN_OUTRO[i], 2)
    P["lead"].append(lead); P["harm8"].append(harm8); P["tech"].append(tech); P["vln"].append(vln)

    if name in ("intro", "cloud") or (name == "outro" and not last):
        b = unison_low(P["riff"][-1], -1, "B0") if P["riff"][-1] != R4 else bar(f"{root}:4")
    elif name in ("verse", "verse2", "pre", "pre2", "solo"):
        b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name.startswith("chorus"):
        b = bass_root8(ch, BEATS, nxt) if not (last and name != "chorus3") else bar(f"{root}:1.5! {root}:0.5 R:2")
        if name == "chorus3" and last: b = bar(f"{root}:4!")
    elif name == "above": b = bar(f"{root}:2 {fifth_of(base_ch)}:2")
    elif name == "outro": b = bar(f"{root}:4!")
    else: b = R4
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    # ずらしたアクセント: 小節ごとに、キックとクラッシュ（ベル）のアクセントの位置が16分ずつずれていく
    SHIFT = [0, 3, 6, 9, 12, 15, 2, 5]
    if name in ("intro", "cloud") or (name == "outro" and not last):
        if name == "intro" and i < 2:
            tom = " ".join(f"A2:0.25{',' if j % 4 else ''}" for j in range(16)) if i == 1 else "A2:1 A2:1, A2:1, A2:1,"
            cym = f"{BELL}:1 {BELL}:1 {BELL}:1 {BELL}:1"
        else:
            a = SHIFT[i % 8]
            k = kit.grid((0, 8, a), "X"); s = "....X.......X..."
            k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
            h = "".join("." if (k[j] != "." or s[j] != ".") else ("X" if j == a else ("x" if j % 2 == 0 else ".")) for j in range(16))
            if name == "cloud" and i >= 4: k = "XxXxXxXxXxXxXxXx"; k = "".join("." if s[j] != "." else c for j, c in enumerate(k)); h = None; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
            if (name == "intro" and i == 2) or (name in ("cloud", "outro") and i == 0): cym = f"{CR}:1! R:3"; h = h and "...." + h[4:]
            if last and name != "outro": k, s, tom = linear_fill(kit, 2, i); k = "X......." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
    elif name in ("verse", "verse2"):
        a = SHIFT[i % 8]
        k = kit.grid((0, 10, a), "X"); s = "....X.......X..."; k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        h = "".join("." if s[j] != "." else ("X" if j == a else ("x" if j % 2 == 0 else ".")) for j in range(16))
        if name == "verse2": h = None; cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"
        if i == 0: cym = f"{CR2}:1! " + ("R:3" if name == "verse" else f"{RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"); h = h and "...." + h[4:]
        if last: k, s, tom = linear_fill(kit, 2, 2); k = "X......." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
    elif name in ("pre", "pre2"):
        j = i if name == "pre" else 4 + i
        k = ["X.......X.......", "X.......X.......", "X...X...X...X...", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "X.X.X.X.X.X.X.X.", "XxXxXxXxXxXxXxXx", "XxXxXxXx........"][j]
        s = ["........X.......", "........X.......", "....X.......X...", "....X.......X...", "....X.......X...", "....X.......X...", "....X.......X...", "........X.X.XXXX"][j]
        k = "".join("." if s[q] != "." else c for q, c in enumerate(k))
        h = ["x.x.x.x.x.x.x.x."] * 4 + ["xxxxxxxxxxxxxxxx"] * 2 + [None, None]
        h = h[j]
        if j == 0: cym = f"{CR2}:2! R:2"
    elif name.startswith("chorus"):
        a = SHIFT[i % 8]
        k = kit.grid((0, 2, 6, 8, 10, a), "X") if i % 2 == 0 else kit.grid((0, 2, 6, 8, 12, 14, a), "X")
        s = "....X.......X..."; k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        h = "".join("." if s[j] != "." else ("X" if j == a else "x") if j % 2 == 0 or j == a else "." for j in range(16))
        if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + "R:3"; h = "...." + h[4:]
        if i == 6: cym = f"{CR}:1! R:3"; h = "...." + h[4:]
        if name == "chorus3" and i >= 12: k = "XxXxXxXxXxXxXxXx"; k = "".join("." if s[j] != "." else c for j, c in enumerate(k)); h = None; cym = cym or f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last and name != "chorus3": k, s, tom = linear_fill(kit, 2, 3); k = "X.X...X." + k[8:]; s = "....X..." + s[8:]; h = None; cym = None
        if name == "chorus3" and last: k = "X..............."; s = "X..............."; h = None; cym = f"{CR}:4!"
    elif name == "above":
        # 雲の上: ハーフタイム、ライド、キックは小さく
        k = "X.........X....." if i % 2 == 0 else "X.......X......."
        s = "........X......."
        cym = f"{RIDE}:1 {BELL}:1 {RIDE}:1 {BELL}:1"
        if i == 0: cym = f"{CR}:2 {RIDE}:1 {BELL}:1"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {BELL}:1 R:2"
    elif name == "solo":
        k = "XxXxXxXxXxXxXxXx"; s = "....X.......X..."; k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i % 4 == 0: cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k, s, tom = linear_fill(kit, 2, 0); k = "XxXxXx.." + k[8:]; s = "....X..." + s[8:]; cym = None
    elif name == "outro" and last:
        k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx.startswith("chorus"): FX.append(bar("R:2 C4:2"))
    elif name == "pre" and i == 4: FX.append(bar("E4:4"))
    elif name == "above" and i == 0: FX.append(R4)
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tech"), role="スウィープのギター", vol=0.11, pan=0.05))
song.add(part("バイオリン", "strings", J("vln"), patch="violin", volume=0.15, pan=-0.18, reverb=0.5, gainDb=3, bright=-0.15, attack=0.35, release=0.7,
              doubleDetune={"cents": 5, "spread": 0.3}, phrase=8,
              fx=[{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 1, "mix": 0.08, "feedback": 0.2},
                  {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-21-kassouro.json"
    song.write(out)
    check_clash(song)
