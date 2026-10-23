# ラウド25曲（第2シリーズ）02「白い螺旋」（仮）。イメージ: ドラッグ（抜け出せないめまい）。F♯ フリジアン・128・7/4（2+2+3）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: シタール（螺旋の動機を最初と間奏で）
# しかけ:
#   - 7拍子を 2+2+3 で数える。看板リフは F♯ の開放のペダルに ♭2（G）がまとわりつく「螺旋」（最後の3拍で上って落ちる）
#   - Aメロは F♯ のペダルの上で和音だけ動く（G/F♯ のめまい）。Bメロで C♯7（和声的短音階の属和音）へ
#   - サビは D から下りる低音（D → C♯ → B → G）に、7小節目の Gmaj7♯11（リディアンの色）で一瞬だけ浮く
#   - 間奏はベースのスラップ（親指・はじく・ゴースト）とシタールの掛け合い。ブリッジはギターのタッピング
#   - ドラム: 7拍子のリニアのフィル、ライドのベルで 2+2+3 を示す、ブレイクダウンは 2+2+3 の一撃
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 128, 7
bar = Bars(BEATS)
R7 = bar.rest()

FORM = [("intro", 6), ("verse", 8), ("pre", 4), ("chorus", 8), ("inter", 6), ("verse2", 4), ("pre2", 4), ("chorus2", 8),
        ("bridge", 8), ("break", 4), ("chorus3", 8), ("outro", 3)]
VERSE = ["F#m7", "G/F#", "F#m", "G/F#", "Bm/F#", "G/F#", "F#m", "C#7"]
PRE = ["Dmaj7", "Em7", "Gmaj7", "C#7sus4"]
CHORUS = ["Dmaj7", "A/C#", "Bm7", "G", "Dmaj7", "A/C#", "Gmaj7#11", "C#7"]
CH = {"intro": ["F#m"] * 5 + ["G"], "verse": VERSE, "pre": PRE, "chorus": CHORUS,
      "inter": ["F#m", "F#m", "G", "G", "F#m", "C#7"], "verse2": VERSE[:4], "pre2": PRE, "chorus2": CHORUS,
      "bridge": ["F#m", "G", "Em", "F#m", "Bm", "C#7", "D", "C#7"], "break": ["F#5"] * 4, "chorus3": CHORUS, "outro": ["F#m", "G", "F#5"]}
song = Song("白い螺旋（仮）",
            "仮: ラウド25曲（第2シリーズ）の2曲目。イメージはドラッグ（抜け出せないめまい）。F♯ フリジアン・128・7/4（2+2+3）。"
            "F♯ のペダルに ♭2 がまとわりつく螺旋のリフ、サビは下りる低音と Gmaj7♯11 で一瞬浮く。間奏はスラップとシタール、ブリッジはタッピング。別の楽器はシタール。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 最初の一口、時間が7拍子にゆがみ、タッピングで高く舞い上がって、落ちる。"
SECS, NB = song.secs, song.nb

# ---------------- 看板リフ（2+2+3） ----------------
RIFF_A = bar("F#2:0.5! F#2:0.5 G2:0.5 F#3:0.5", "F#2:0.5! F#2:0.5 A2:0.5 E3:0.5", "F#2:0.5! C#3:0.5 D3:0.5 C#3:0.5 G2:1")
RIFF_A2 = bar("F#2:0.5! F#2:0.5 G2:0.5 F#3:0.5", "F#2:0.5! F#2:0.5 A2:0.5 E3:0.5", "F#2:0.5! C#3:0.5 D3:0.5 E3:0.5 G3:1")
RIFF_G = bar("G2:0.5! G2:0.5 A2:0.5 G3:0.5", "G2:0.5! G2:0.5 B2:0.5 F#3:0.5", "G2:0.5! D3:0.5 E3:0.5 D3:0.5 A2:1")
RIFF_C = bar("C#2:0.5! C#2:0.5 D2:0.5 C#3:0.5", "C#2:0.5! C#2:0.5 F2:0.5 B2:0.5", "C#2:0.5! G#2:0.5 B2:0.5 G#2:0.5 C#3:1")
RIFFS = {"F#m": [RIFF_A, RIFF_A2], "G": [RIFF_G, RIFF_G], "C#7": [RIFF_C, RIFF_C], "F#5": [RIFF_A, RIFF_A]}

# ---------------- 旋律 ----------------
VERSE_MEL = [
    bar("R:1 C#4:0.5 E4:0.5 F#4:1 A4:1 G4:0.5 F#4:0.5 E4:2"),
    bar("D4:3 R:1 B3:0.5 D4:0.5 G4:2"),
    bar("R:0.5 A4:0.5 C#5:1 B4:0.5 A4:0.5 F#4:2 R:2"),
    bar("R:1 G4:0.5 A4:0.5 B4:1.5 A4:0.5 G4:1 D4:2"),
    bar("F#4:1 B4:1 D5:2 C#5:0.5 B4:0.5 F#4:2"),
    bar("E4:0.5 G4:0.5 B4:1 D5:1.5 E5:0.5 D5:1 B4:2"),
    bar("C#5:2 A4:1 F#4:2 R:2"),
    bar("R:1 F4:0.5 G#4:0.5 B4:1 C#5:2 R:2"),
]
VERSE2_MEL = [   # 2回目は1オクターブ近く上で、リズムを詰める
    bar("R:0.5 C#5:0.5 E5:0.5 F#5:0.5 A5:1 G5:0.5 F#5:0.5 E5:1 C#5:2"),
    bar("D5:2 B4:1 R:1 D5:0.5 G5:0.5 B5:2"),
    bar("R:0.5 A5:0.5 C#6:1 B5:0.5 A5:0.5 F#5:2 R:2"),
    bar("R:1 G5:0.5 A5:0.5 B5:1.5 A5:0.5 G5:1 D5:2"),
]
PRE_MEL = [bar("F#4:1 A4:1 C#5:2 A4:1 F#4:0.5 A4:0.5 R:1"), bar("G4:1 B4:1 D5:2 B4:1 G4:0.5 B4:0.5 R:1"),
           bar("B4:1 D5:1 F#5:2 D5:1 B4:0.5 D5:0.5 R:1"), bar("C#5:1 F#5:1 G#5:3 R:2")]
CHORUS_MEL = [
    bar("R:0.5 F#5:0.5 A5:0.5 C#6:0.5 A5:3 F#5:1 E5:1"),
    bar("E5:2 C#5:1 E5:1 A5:2 R:1"),
    bar("R:0.5 D5:0.5 F#5:0.5 A5:0.5 B5:3 A5:1 F#5:1"),
    bar("G5:2 D5:1 B4:1 D5:2 R:1"),
    bar("R:0.5 F#5:0.5 A5:0.5 C#6:0.5 E6:3! D6:1 C#6:1"),
    bar("C#6:2 A5:1 E5:1 A5:2 R:1"),
    bar("R:0.5 B5:0.5 C#6:0.5 D6:0.5 C#6:3 B5:1 A5:1"),
    bar("G#5:3 F5:1 C#5:3"),
]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("E5:1 A5:1 C#6:2 B5:1 A5:1 R:1")
CHORUS2_MEL[5] = bar("C#6:1 E6:1 C#6:2 A5:2 R:1")
CHORUS3_MEL = [bar("A5:7!"), bar("E5:4 C#5:3"), bar("B5:7!"), bar("G5:4 D5:3")] + CHORUS_MEL[4:]

# シタール: 螺旋の動機（リフの2オクターブ上）と、間奏の答え
SITAR_INTRO = [shift_oct(strip_marks(RIFF_A), 2), shift_oct(strip_marks(RIFF_A2), 2)]
SITAR_INTER = [R7, bar("R:4 F#4:0.5 G4:0.5 A4:0.5 C#5:0.5 F#5:1"), R7, bar("R:4 G4:0.5 A4:0.5 B4:0.5 D5:0.5 G5:1"),
               R7, bar("R:4 F4:0.5 G#4:0.5 B4:0.5 C#5:0.5 G#4:1")]
# タッピング: 和音の3音（低・中・右手の高い音）を6連でくり返し、最後の1拍は高い音を伸ばす
TAP_TRI = {"F#m": ["A4", "C#5", "F#5"], "G": ["B4", "D5", "G5"], "Em": ["G4", "B4", "E5"], "Bm": ["B4", "D5", "F#5"],
           "C#7": ["G#4", "B4", "F5"], "D": ["A4", "D5", "F#5"]}
TAP_PAT = [(2, 1, 0, 1), (2, 0, 1, 0), (2, 1, 0, 1), (0, 1, 2, 1)]

# スラップ（間奏）: T 親指・P はじく・F 5度・S ♭7・g ゴースト（止めた音）。2+2+3 の頭に親指
SLAP = ["T.gP.gT.T.gPTgP.T..gP.gTPgS.", "T.gPTgP.T.gP.gTPT.gP.gTgP.P.", "T.gP.gT.T.gPTgP.T..gP.gTPgS.", "T.gPTgP.T..PTgP.TgP.gT.TPgPg"]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "arp", "lead", "harm", "sitar", "tap", "bass", "pop", "mute"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
RIDE_227 = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5"

def g28(*pos, ch="X", base=None):
    return kit.grid(pos, ch, base)

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    root = root_note(ch)
    groot = root_note(ch, "E2", "D#3")
    base_ch = ch.split("/")[0]

    # ----- リフ -----
    rf = R7
    if name in ("intro", "outro") or (name == "inter" and False):
        if name == "intro" and i < 2: rf = R7
        elif name == "outro" and last: rf = bar("F#2:7!")
        else:
            key = "G" if base_ch == "G" else ("C#7" if base_ch == "C#7" else "F#m")
            rf = RIFFS[key][i % 2]
            if name == "intro" and last: rf = bar("G2:0.5! G2:0.5 A2:0.5 G3:0.5", "G2:0.5! G2:0.5 B2:0.5 F#3:0.5", "G2:3!")
    elif name == "break":
        rf = bar("F#2:2! F#2:2! F#2:3!") if i < n - 1 else bar("F#2:2! G2:2! R:3")
    P["riff"].append(rf)

    # ----- リズムギター（2+2+3 の頭で伸ばす） -----
    s = si = R7
    if name in ("verse", "verse2"):
        s = bar(f"{groot}:2! {groot}:2 {groot}:3") if not last else bar(f"{groot}:4! R:3")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:4! {groot}:3") if not last else bar(f"{groot}:4! R:3")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:7!")
        elif last and name != "chorus3": s = bar(f"{groot}:4! R:3")
        else: s = bar(f"{groot}:2! {groot}:2 {groot}:3")
        si = s if not (name == "chorus3" and i < 4) else R7
    elif name == "bridge":
        s = bar(f"{groot}:7")
    elif name == "break":
        s = si = P["riff"][-1]
    elif name == "inter" and i >= 2:
        s = bar(f"{groot}:4 R:3") if i % 2 == 0 else R7
    P["rhy"].append(s); P["rhy_in"].append(si)

    # ----- 分散和音（サビ2・サビ3の後半） -----
    if (name == "chorus2" or (name == "chorus3" and i >= 4)) and not last:
        t = chord_tones(base_ch, "D4", "D5")[:4]
        pat = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3]
        P["arp"].append(bar(*[f"{t[j % len(t)]}:0.5{'!' if k in (0, 4, 8) else ''}" for k, j in enumerate(pat)]))
    else:
        P["arp"].append(R7)

    # ----- 旋律 -----
    lead = harm = sitar = tapn = R7
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 4: sitar = shift_oct(strip_marks(lead), -1)
    elif name == "intro" and i < 2: sitar = SITAR_INTRO[i]
    elif name == "inter": sitar = SITAR_INTER[i]
    elif name == "bridge":
        tri = TAP_TRI[ch]
        tapn = bar(tap(tri, 6, pattern=TAP_PAT[i % 4]), f"{tri[2]}:1")
    P["lead"].append(lead); P["harm"].append(harm); P["sitar"].append(sitar); P["tap"].append(tapn)

    # ----- ベース -----
    pop = mute = R7
    if name in ("intro", "outro"):
        if name == "intro" and i < 2: b = bar("F#1:4 R:3") if i == 0 else bar("F#1:4 G1:3")
        elif name == "outro" and last: b = bar("F#1:7!")
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name == "inter":
        b, mute = bass_slap_bar(ch, BEATS, SLAP[i % 4])
        # はじく音（P）は別のパートで明るく。親指の音はふつうのベースで
        pt = [];  mt = []
        for t in b.split():
            if t.endswith("'"): pt.append(t); mt.append("R:" + t.split(":")[1].rstrip("'"))
            else: pt.append("R:" + t.split(":")[1].rstrip("!'")); mt.append(t)
        pop = merge_rests(" ".join(pt)); b = merge_rests(" ".join(mt))
    elif name in ("verse", "verse2", "pre", "pre2"):
        r = root
        acc = {0, 4, 8}
        toks = [f"{r}:0.5{'!' if j in acc else ''}" for j in range(14)]
        if not last and name in ("pre", "pre2"):
            toks[-1] = f"{fifth_of(base_ch)}:0.5"
        b = bar(" ".join(toks)) if not last else bar(f"{r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5 {r}:2! R:3")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: b = bar(f"{root}:4! {root}:3")
        elif last and name != "chorus3": b = bar(f"{root}:2! {root}:2 R:3")
        else:
            toks = [f"{root}:0.5{'!' if j in (0, 4, 8) else ''}" for j in range(14)]
            nr = root_note(nxt)
            if nr != root: toks[-1] = f"{fifth_of(base_ch)}:0.5"
            b = bar(" ".join(toks))
    elif name == "bridge":
        b = bar(f"{root}:2! {up(root, 1)}:1 {root}:1 {fifth_of(ch)}:3")
    elif name == "break":
        b = unison_low(P["riff"][-1], -1, "B0")
    else:
        b = R7
    P["bass"].append(b); P["pop"].append(pop); P["mute"].append(mute)

    # ----- ドラム（28マス＝16分×7拍。2+2+3 の頭は 0・8・16） -----
    k = s = h = None; tom = cym = None
    if name in ("intro", "outro"):
        if name == "intro" and i == 0:
            k = g28(0, 16); s = g28(); tom = f"R:4 D3:1 A2:1 A2:1"; cym = RIDE_227
        elif name == "intro" and i == 1:
            k, s, tom = linear_fill(kit, 3, 0); k = g28(0, 8, base=k); cym = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:3"
        elif name == "outro" and last:
            k = g28(0); s = g28(0); cym = f"{CR}:7!"
        else:
            k = g28(0, 2, 8, 10, 16); s = g28(4, 12, 20) ; s = g28(23, ch="o", base=s)
            cym = RIDE_227 if i % 2 else f"{CR}:0.5! " + RIDE_227.split(" ", 1)[1]
            if name == "intro" and last:
                k, s, tom = linear_fill(kit, 3, 1); k = g28(0, 2, 8, 10, base=k); s = g28(4, 12, base=s)
                cym = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:3"
    elif name in ("verse", "verse2"):
        k = [g28(0, 6, 8, 16, 22), g28(0, 8, 14, 16, 26), g28(0, 6, 8, 16, 19, 22), g28(0, 8, 16, 18, 24)][i % 4]
        s = g28(4, 12, 24); s = g28(*[p for p in (7, 15, 21) if k[p] == "."], ch="o", base=s)
        h = "".join("x" if j % 2 == 0 else "." for j in range(28)) if name == "verse" else "".join("x" if j % 2 == 0 else "o" for j in range(28))
        h = "".join("X" if j in (0, 8, 16) else c for j, c in enumerate(h))
        if i == 0: cym = f"{CR2}:1! R:6"
        if last:
            k, s, tom = linear_fill(kit, 3, 2); k = g28(0, 8, base=k); s = g28(4, 12, base=s); h = "x.x.x.x.x.x.x.x............."
    elif name in ("pre", "pre2"):
        k = [g28(0, 8, 16), g28(0, 4, 8, 12, 16, 20, 24), g28(*range(0, 28, 2)), g28(*range(0, 24))][i]
        s = [g28(16), g28(8, 24), g28(4, 12, 20), g28(24, 25, 26, 27)][i]
        if i == 3: k = g28(*range(0, 16)); s = g28(16, 18, 20, 22); tom = "R:6 A2:0.5! A2:0.5!"
        h = "x.x.x.x.x.x.x.x.x.x.x.x.x.x." if i < 3 else None
        if i == 0: cym = f"{CR2}:2! R:5"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! {CHINA}:1 R:3"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = g28(0, 10, 16); s = g28(16)
            cym = f"{CR}:4! {RIDE}:1 {RIDE}:1 {RIDE}:1" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1 {RIDE}:1"
        else:
            k = [g28(0, 3, 8, 11, 16, 19, 22), g28(0, 3, 8, 16, 18, 22, 26), g28(0, 3, 8, 11, 16, 19, 22), g28(0, 8, 10, 16, 20, 24)][i % 4]
            s = g28(4, 12, 20, 24) if i % 4 != 3 else g28(4, 12, 20, 25, 27)
            s = g28(*[p for p in (14, 26) if k[p] == "." and s[p] == "."], ch="o", base=s)
            h = "".join("X" if j % 4 == 0 else ("x" if j % 2 == 0 else ".") for j in range(28)) if i % 8 < 4 else None
            cym = None if i % 8 < 4 else f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 " * 3 + f"{BELL}:0.5! {RIDE}:0.5"
            if cym: cym = cym.strip()
            if i % 4 == 0:
                lead_c = f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! "
                cym = lead_c + (f"{RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 " * 2 + f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5").strip() if i % 8 >= 4 else lead_c + "R:6"
            if name == "chorus2" and i in (4, 5): k = g28(*range(0, 28)); k = "".join("X" if j % 2 == 0 else "x" for j in range(28))
        if last and name != "chorus3":
            k, s, tom = linear_fill(kit, 3, 3); k = g28(0, 8, base=k); s = g28(4, 12, base=s); h = None
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:3"
        if name == "chorus3" and last:
            k = g28(0, 8, 16); s = g28(4, 12, 20); cym = f"{CR}:2! {RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1 {RIDE}:1"
    elif name == "inter":
        # スラップの下: 2+2+3 の頭のキック、スネアのゴースト多め、ハイハットは16分の強弱
        k = g28(0, 8, 16, 22) if i % 2 == 0 else g28(0, 6, 8, 16, 26)
        s = g28(4, 12, 20); s = g28(*[p for p in (2, 7, 10, 15, 18, 23, 25) if k[p] == "."], ch="o", base=s)
        h = "".join("X" if j in (0, 8, 16) else ("x" if j % 2 == 0 else "o") for j in range(28))
        if i == 0: cym = f"{CHINA}:1! R:6"
        if last:
            k, s, tom = linear_fill(kit, 3, 0); k = g28(0, 8, base=k); s = g28(4, 12, base=s); h = "X.x.x.x.X.x.x.x............."
    elif name == "bridge":
        # タッピングの下: ハーフタイム（スネアは5拍目）、ライドで 2+2+3
        k = g28(0, 10, 16) if i % 2 == 0 else g28(0, 8, 18, 24)
        s = g28(16); s = g28(26, ch="o", base=s)
        cym = RIDE_227 if i else f"{CR2}:0.5! " + RIDE_227.split(" ", 1)[1]
        if last:
            tom = "R:4 " + tom_triplets_down(3); s = g28(16); cym = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:3"
    elif name == "break":
        k = g28(0, 8, 16) if i < n - 1 else g28(0, 8)
        s = g28(16) if i < n - 1 else g28()
        cym = f"{CHINA}:2! {CHINA}:2! {CHINA}:3!" if i < n - 1 else f"{CHINA}:2! {CHINA}:2! R:3"
        if i == 0: cym = f"{CR}:2! {CHINA}:2! {CHINA}:3!"
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
song.add(arp_part(J("arp"), vol=0.08, pan=0.2))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(tech_part(J("tap"), role="タッピングのギター", vol=0.11, pan=0.05))
song.add(part("シタール", "sitar", J("sitar"), volume=0.16, pan=-0.25, reverb=0.35, attack=0.005, release=0.8,
              fx=[{"type": "eq", "low": -3, "mid": 1.5, "midHz": 2000, "high": 1}, {"type": "delay", "beats": 0.75, "mix": 0.18, "feedback": 0.3}, {"type": "plate", "mix": 0.2}]))
song.add(bass_part(J("bass")))
song.add(slap_pop_part(J("pop")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "dark-electro-rock"
add_layer(song, "piano", "めまいの中で、遠くの鍵盤が同じ和音をくり返す。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-02-rasen.json"
    song.write(out)
    check_clash(song)
