# ラウド25曲（第2シリーズ）09「罰の階段」（仮）。イメージ: 罪と罰。C 短調・92・4/4（重いハーフタイム）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: チェンバロ（法廷の古い音。16分の分散和音と左手の階段）
# しかけ:
#   - 低音が半音ずつ一段ずつ下りる「階段」（C → B → B♭ → A → A♭ → G）。Aメロもサビも、低音は必ず下りる
#   - 看板リフ: C のペダルと、半音で下りる上の音が交互に鳴る（刻まない）
#   - ドラム: 重いハーフタイム（スネア3拍目）。サビの3・4・7小節目は、タムの4分の3連（2拍に3つ）で 3対2 のポリリズム
#   - サビ5小節目の D♭（ナポリの ♭II）で光、G7 の導音 B で止める
#   - ブリッジ: チェンバロの16分の分散和音と、ベースの階段だけ（ギターなし）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 92, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 4), ("chorus", 8), ("inter", 4), ("verse2", 8), ("pre2", 4), ("chorus2", 8),
        ("bridge", 8), ("solo", 8), ("break", 4), ("chorus3", 8), ("outro", 4)]
VERSE = ["Cm", "Cm/B", "Cm/Bb", "Am7b5", "Abmaj7", "G7", "Cm", "G7"]
PRE = ["Fm7", "Bb7", "Ebmaj7", "G7"]
CHORUS = ["Ab", "Eb/G", "Fm", "Cm/Eb", "Db", "Bb", "G7sus4", "G7"]
CH = {"intro": ["Cm", "Cm", "Cm", "Cm", "Ab", "Ab", "G7", "G7"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": ["Cm", "Cm", "Ab", "G7"],
      "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS, "bridge": ["Cm", "G/B", "Eb/Bb", "F/A", "Fm/Ab", "Cm/G", "D7/F#", "G"],
      "solo": VERSE, "break": ["C5"] * 4, "chorus3": CHORUS, "outro": ["Cm", "Cm", "Ab", "C5"]}
song = Song("罰の階段（仮）",
            "仮: ラウド25曲（第2シリーズ）の9曲目。イメージは罪と罰。C 短調・92（重いハーフタイム）。低音が半音ずつ下りる「階段」、C のペダルと下りる上の音が交互の看板リフ、"
            "サビはタムの3連で 3対2 のポリリズムと D♭（♭II）の光。ブリッジはチェンバロの分散和音とベースの階段。別の楽器はチェンバロ。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 絞首台へ一段ずつ下りる。法廷のチェンバロ、最後は無音のあとの最後の一段。"
SECS, NB = song.secs, song.nb
song.pickups = ['V5']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

RIFF = {"Cm": [bar("C2:0.5! C3:0.5 B2:0.5 C3:0.5 A#2:0.5 C3:0.5 A2:0.5 G#2:0.5"), bar("C2:0.5! C3:0.5 B2:0.5 C3:0.5 A#2:0.5 C3:0.5 D3:0.5 D#3:0.5")],
        "Ab": [bar("G#1:0.5! G#2:0.5 G2:0.5 G#2:0.5 F2:0.5 G#2:0.5 D#2:0.5 C2:0.5")] * 2,
        "G7": [bar("G1:0.5! G2:0.5 G#2:0.5 G2:0.5 F2:0.5 G2:0.5 D2:0.5 B1:0.5")] * 2}

VERSE_MEL = [bar("R:1 G4:0.5 D#4:0.5 C4:1 D4:0.5 D#4:0.5"), bar("G4:1.5 F4:0.5 D4:2"),
             bar("R:0.5 D#4:0.5 G4:0.5 A#4:0.5 C5:1.5 A#4:0.5"), bar("A4:1 C5:1 D#5:2"),
             bar("R:1 C5:0.5 D#5:0.5 G5:1.5 F5:0.5"), bar("F5:1 D5:1 B4:2"),
             bar("C5:1.5 D5:0.5 D#5:1 G4:1"), bar("B4:2 R:2")]
VERSE2_MEL = [bar("R:0.5 C5:0.5 D#5:0.5 G5:0.5 C6:1 A#5:0.5 G5:0.5"), bar("G5:1.5 F5:0.5 D5:2"),
              bar("R:0.5 G5:0.5 A#5:0.5 C6:0.5 D#6:1.5 D6:0.5"), bar("C6:1 A5:1 D#5:2"),
              bar("R:1 D#5:0.5 G5:0.5 C6:1.5 A#5:0.5"), bar("B5:1 G5:1 D5:2"),
              bar("D#5:1.5 F5:0.5 G5:1 C5:1"), bar("B4:2 R:2")]
PRE_MEL = [bar("G#4:1 C5:1 D#5:2"), bar("D5:1 F5:1 G#5:2"), bar("D#5:1 G5:1 A#5:2"), bar("B5:1 G5:1 D5:1 R:1")]
CHORUS_MEL = [bar("R:0.5 C5:0.5 D#5:0.5 G#5:0.5 C6:2"), bar("A#5:1 G5:0.5 D#5:0.5 G5:2"),
              bar("R:0.5 C5:0.5 F5:0.5 G#5:0.5 C6:2"), bar("G5:1 D#5:0.5 C5:0.5 D#5:2"),
              bar("R:0.5 C#5:0.5 F5:0.5 G#5:0.5 C#6:2!"), bar("D6:1 C6:0.5 A#5:0.5 F5:2"),
              bar("C6:2 D6:1 G5:1"), bar("B5:2 R:2")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("A#5:1 D#6:0.5 A#5:0.5 G5:2")
CHORUS2_MEL[3] = bar("G5:1 C6:0.5 G5:0.5 D#5:2")
CHORUS2_MEL[5] = bar("D6:1 C6:0.5 D6:0.5 A#5:2")
CHORUS2_MEL[6] = bar("C6:1 A#5:1 G5:2")
CHORUS2_MEL[7] = bar("B5:1 D6:1 R:2")
CHORUS3_MEL = [bar("C6:4!"), bar("A#5:2 G5:2"), bar("C6:4!"), bar("D#6:2 C6:2")] + CHORUS_MEL[4:6] + [bar("C6:1 D6:1 G5:2"), bar("G5:2 B5:2")]
SOLO = [bar("D#5:0.5 G5:0.5 C6:3^^"), bar("D6:1 C6:0.5 B5:0.5 G5:2"), bar("A#5:1.5 G5:0.5 D#5:1 C5:1"), bar("A5:1 C6:1 D#6:2"),
        bar("C6:1.5 A#5:0.5 G5:2"), bar("F5:1 G5:0.5 G#5:0.5 B5:2"), bar("C6:1 G5:1 D#6:2"), bar("D6:2^^ R:2")]


def hpsi_bar(ch, lo="C4", hi="C6"):
    """チェンバロの右手（16分の分散和音: 低・高・中・高 の形をくり返す）"""
    t = chord_tones(ch.split("/")[0], lo, hi)
    a, b, c, d = t[0], t[min(3, len(t) - 1)], t[1], t[2]
    pat = [a, d, c, d, b, d, c, d] * 2
    return bar(" ".join(f"{x}:0.25{'!' if j % 8 == 0 else ''}" for j, x in enumerate(pat)))


P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "hr", "hl", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
TRIP = "A2:0.6667! D3:0.6667 F3:0.6667 A2:0.6667! D3:0.6667 F3:0.6662"     # 4分の3連（2拍に3つ）

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R4
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: rf = bar("C2:4!") if i == 0 else R4
        elif name == "outro" and last: rf = bar("R:2 C2:2!")
        else: rf = RIFF[base_ch if base_ch in RIFF else "Cm"][i % 2]
    elif name == "break":
        rf = bar("C2:1.5! C2:1.5! C#2:1!") if i < n - 1 else bar("C2:1.5! C#2:0.5! R:2")
    P["riff"].append(rf)

    s = si = R4
    if name in ("verse", "verse2") and (i >= 4 or name == "verse2"):
        s = bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")
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

    lead = harm8 = hr = hl = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "solo": lead = SOLO[i]
    if (name == "intro" and i < 2) or name == "bridge" or (name == "outro" and i < 3) or (name == "inter" and i >= 2):
        hr = hpsi_bar(ch)
        hl = bar(f"{root_note(ch, 'C3', 'B3')}:2 {root_note(ch, 'C3', 'B3')}:2") if name != "bridge" else bar(f"{root_note(ch, 'C3', 'B3')}:4")
    P["lead"].append(lead); P["harm8"].append(harm8); P["hr"].append(hr); P["hl"].append(hl)

    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: b = bar("C1:4!") if i == 0 else bar("C1:4")
        elif name == "outro" and last: b = bar("R:2 C1:2!")
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("verse", "verse2", "solo"):
        # 階段: 1小節に1段、4分で押す
        b = bar(f"{root}:1! {root}:1 {root}:1 {root}:1") if not last else bar(f"{root}:1! {root}:1 R:2")
        if name == "verse2" or name == "solo": b = bass_root8(ch, BEATS, nxt) if not last else b
    elif name in ("pre", "pre2"):
        b = bass_root8(ch, BEATS, nxt) if not last else bar(f"{root}:1! {root}:1 R:2")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:3! {root}:1")
        elif last and name != "chorus3": b = bar(f"{root}:1.5! {root}:0.5 R:2")
        else: b = bass_root8(ch, BEATS, nxt)
    elif name == "bridge":
        b = bar(f"{root}:2 {root}:1 {up(root, 1)}:1") if i < n - 1 else bar(f"{root}:4")
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R4
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0:
            k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
        elif name == "intro" and i == 1:
            cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 R:1"; tom = "R:2 " + tom_triplets_down(2)
        elif name == "outro" and last:
            k = "........X......."; s = "........X......."; cym = f"R:2 {CHINA}:2!"
        else:
            k = "X.....X.X......." if i % 2 == 0 else "X.....X.X.x....."
            s = "........X......."
            h = "x.x.x.x.x.x.x.x."
            if (name == "intro" and i == 2) or (name == "inter" and i == 0): cym = f"{CR}:1! R:3"; h = "....x.x.x.x.x.x."
            if last and name != "outro":
                k = "X.....X........."; s = "........"; s += "........"; h = None; tom = "R:2 " + tom_triplets_down(2)
    elif name in ("verse", "verse2"):
        k = ["X...X...X...X...", "X...X.x.X...X...", "X...X...X..xX...", "X...X.x.X...X..x"][i % 4] if name == "verse" else ["X..x..X.X.......", "X.....X.X..x...."][i % 2]
        s = "........X......."
        s = "".join("o" if j in (6, 14) and k[j] == "." else c for j, c in enumerate(s))
        h = "x.x.x.x.x.x.x.x." if name == "verse" else None
        if name == "verse2": cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5"
        if i == 0: cym = f"{CR2}:1! " + (f"{RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5" if name == "verse2" else "R:3")
        if last: k = "X.....X........."; s = "........"; s += "X.X.XXXX"; h = None; cym = None
    elif name in ("pre", "pre2"):
        k = ["X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XxXxXxXxXxXx...."][i]
        s = ["........X.......", "....X.......X...", "....X.......X...", "..X...X...X....."][i]
        h = ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", None][i]
        if i == 0: cym = f"{CR2}:2! R:2"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! R:1"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = "X.........X....."; s = "........X......."
            cym = f"{CR}:4!" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        else:
            k = ["X..x....X.X.....", "X..x..X...X....."][i % 2]
            s = "........X......."
            if i in (2, 3, 6):
                # 3対2: タムの4分の3連（2拍に3つ）を、ハーフタイムのキックとスネアの上に
                tom = TRIP; h = None; cym = None
                s = "........X......."
            else:
                cym = f"{CHINA}:1! {RIDE}:1 {CHINA}:1! {RIDE}:1" if i % 2 else f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
                if i % 4 == 0: cym = (f"{CR}:2! " if i % 8 == 0 else f"{CR2}:2! ") + f"{RIDE}:1! {BELL}:1"
            if name == "chorus2" and i == 5: k = "XxXxXxXx" + "X..x...."
        if last and name != "chorus3":
            k = "X..x............"; s = "........X.X.X..X"; cym = f"{RIDE}:1! {RIDE}:1 R:2"; h = None; tom = None
        if name == "chorus3" and last:
            k = "X..x....X.X....."; s = "........X......."; cym = f"{CR}:2! {RIDE}:1 {RIDE}:1"; tom = None
    elif name == "bridge":
        k = "X.......X......." if i % 2 == 0 else "X..............."
        s = "....o.......o..." if i >= 4 else None
        cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1"
        if i == 0: cym = f"{CR2}:2 {RIDE}:1 {RIDE}:1"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 R:2"; s = None
    elif name == "solo":
        k = ["X.x...X.X.x.....", "X.x...X.X...X.x."][i % 2] if i < 4 else "XxXxXxXxXxXxXxXx"
        s = "....X.......X..."
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i in (0, 4): cym = f"{CR}:1! {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k = "X.x...X........."; s = "....X..........."; tom = "R:2 " + tom_triplets_down(2); cym = f"{RIDE}:1 {RIDE}:1 R:2"
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
    if i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:2 C4:2"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:3 D4:1"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
HPS = dict(reverb=0.35, attack=0.002, release=0.5, fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 1500, "high": 0}, {"type": "plate", "mix": 0.2}])
song.add(part("チェンバロ（右手）", "harpsichord", J("hr"), volume=0.12, pan=-0.2, **HPS))
song.add(part("チェンバロ（左手）", "harpsichord", J("hl"), volume=0.1, pan=-0.1, **HPS))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "dark-electro-rock"
add_layer(song, "synth-arp", "螺旋階段を下りる足音のように、音が回り続ける。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-09-kaidan.json"
    song.write(out)
    check_clash(song)
