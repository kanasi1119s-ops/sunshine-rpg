# ラウド25曲（第2シリーズ）01「路地裏の灯」（仮）。イメージ: 裏通り。C♯ ドリアン・96・4/4。インスト（歌は後日）
# 設計表: docs/sound/lm25-plan.md。別の楽器: アルトサックス（人間「一つだけ別の楽器を」）
# しかけ:
#   - 曲の頭: 1拍目に全員の一撃 → ライドのベルとウォーキングのベースだけで路地へ入る → 3小節目から看板リフ
#   - 看板リフ: 16分のシンコペーションで「忍び足」。開放の C♯ とオクターブ上・ドリアンの F♯（長三和音）の色
#   - Aメロ1: ジャズのウォーキングベース＋ライドのレガート＋スネアのゴースト、クリーンのギターが和音を置く（刻まない）
#   - サビ: ♭VI（A）から開け、7小節目に ♭II（D）で一瞬だけ違う光。主和音（C♯m）は4小節目まで取っておく
#   - ブリッジ: E 長調の ii-V-I へ寄り道（ジャズ）→ サックスの独奏 → ブレイクダウン → ラストサビ
# 書き出し: node tools/composer/song.mjs build <json> --wav --drums naked --bass bnb-loud --master -13.5 --widen 1.0
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 96, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("verse", 8), ("pre", 4), ("chorus", 8), ("inter", 4), ("verse2", 8), ("pre2", 4), ("chorus2", 8),
        ("bridge", 8), ("solo", 8), ("break", 4), ("chorus3", 8), ("outro", 4)]
VERSE = ["C#m9", "F#9", "C#m9", "F#9", "Amaj7", "B6", "G#7sus4", "G#7"]
PRE = ["Amaj7/C#", "B/C#", "C#m", "D#m7/C#"]
CHORUS = ["Amaj7", "B", "G#m7", "C#m7", "Amaj7", "B", "Dmaj7", "G#7sus4"]
CH = {
    "intro": ["C#m9", "C#m9", "C#m9", "C#m9", "F#9", "F#9", "C#m9", "F#9"],
    "verse": VERSE, "pre": PRE, "chorus": CHORUS,
    "inter": ["C#m9", "C#m9", "F#9", "G#7"],
    "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS,
    "bridge": ["F#m9", "B9", "Emaj7", "Amaj7", "D#m7b5", "G#7", "C#m9", "C#m9"],
    "solo": VERSE,
    "break": ["C#5", "C#5", "C#5", "C#5"],
    "chorus3": CHORUS,
    "outro": ["C#m9", "C#m9", "F#9", "C#m9"],
}
song = Song("路地裏の灯（仮）",
            "仮: ラウド25曲（第2シリーズ）の1曲目。イメージは裏通り。C♯ ドリアン・96。16分のシンコペーションの看板リフ、Aメロはジャズのウォーキングベース、"
            "サビは ♭VI から開けて ♭II で一瞬違う光。別の楽器はアルトサックス（Aメロ2の合いの手と、ブリッジの独奏）。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 夜の路地に迷いこんだ旅人が、裏口でサックス吹きに出会い、追われ、窓に朝の光を見る。"
SECS = song.secs
song.pickups = ['V3', 'V1']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）
NB = song.nb

# ---------------- 看板リフ ----------------
# 1小節＝16分の位置: 低い C♯ のアクセント（0・8）、オクターブ上（3）、下りる（4・6）、高い弦の短い音（10）
RIFF_A = bar("C#2:0.5! R:0.25 C#3:0.25 B2:0.5 G#2:0.5 C#2:0.25! C#2:0.25 E3:0.5 D#3:0.25 C#3:0.25 R:0.5")
RIFF_A2 = bar("C#2:0.5! R:0.25 C#3:0.25 B2:0.5 G#2:0.5 C#2:0.25! C#2:0.25 E3:0.25 F#3:0.25 G#3:0.5 R:0.5")
RIFF_B = bar("F#2:0.5! R:0.25 F#3:0.25 E3:0.5 C#3:0.5 F#2:0.25! F#2:0.25 A#3:0.5 G#3:0.25 F#3:0.25 R:0.5")
RIFF_G = bar("G#2:0.5! R:0.25 G#3:0.25 F#3:0.5 D#3:0.5 G#2:0.25! G#2:0.25 C4:0.5 B3:0.25 G#3:0.25 R:0.5")
RIFF_END = bar("C#2:0.5! R:0.25 C#3:0.25 B2:0.5 G#2:0.5 C#2:2!")

# ---------------- 旋律（リード＝歌の代わり） ----------------
VERSE_MEL = [
    bar("R:1 G#4:0.5 B4:0.5 C#5:1 B4:0.5 G#4:0.5"),
    bar("A#4:2 R:2"),
    bar("R:0.5 E4:0.5 G#4:0.5 B4:0.5 D#5:1.5 C#5:0.5"),
    bar("C#5:1 A#4:1 R:2"),
    bar("R:1 E5:0.5 C#5:0.5 G#4:2"),
    bar("F#4:0.5 G#4:0.5 B4:1 D#5:2"),
    bar("C#5:1.5 B4:0.5 G#4:2"),
    bar("R:1 C5:0.5 D#5:0.5 F#5:2"),
]
# Aメロ2: 同じ形を少し上で、リズムを詰める（1回目と変える）
VERSE2_MEL = [
    bar("R:0.5 G#4:0.5 B4:0.5 C#5:0.5 E5:1 D#5:0.5 C#5:0.5"),
    bar("A#4:1.5 C#5:0.5 R:2"),
    bar("R:0.5 G#4:0.5 B4:0.5 D#5:0.5 E5:1.5 D#5:0.5"),
    bar("C#5:1 A#4:0.5 G#4:0.5 R:2"),
    bar("R:0.5 E5:0.5 G#5:0.5 E5:0.5 C#5:2"),
    bar("D#5:0.5 F#5:0.5 G#5:1 F#5:2"),
    bar("G#5:1.5 F#5:0.5 C#5:2"),
    bar("R:1 C5:0.5 D#5:0.5 G#5:2"),
]
PRE_MEL = [bar("E5:1 C#5:0.5 E5:0.5 G#5:2"), bar("F#5:1 D#5:0.5 F#5:0.5 B5:2"), bar("G#5:1.5 E5:0.5 G#5:2"), bar("A#5:1.5 F#5:0.5 D#5:1 R:1")]
CHORUS_MEL = [
    bar("R:0.5 C#5:0.5 E5:0.5 G#5:0.5 B5:2!"),
    bar("F#5:1 D#5:0.5 E5:0.5 F#5:2"),
    bar("R:0.5 B4:0.5 D#5:0.5 F#5:0.5 A#5:2!"),
    bar("G#5:1 E5:0.5 D#5:0.5 E5:2"),
    bar("R:0.5 C#5:0.5 E5:0.5 G#5:0.5 C#6:2!"),
    bar("B5:1 A#5:0.5 F#5:0.5 D#5:2"),
    bar("F#5:1.5 E5:0.5 A5:2!"),
    bar("G#5:2 F#5:1 R:1"),
]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("F#5:1 D#5:0.5 F#5:0.5 B5:2")         # 2回目はフックの返しを上へ
CHORUS2_MEL[5] = bar("B5:1 A#5:0.5 B5:0.5 D#6:2!")        # 山をひとつ上に（2回目だけ）
CHORUS3_MEL = [bar("B5:4!"), bar("F#5:2 D#5:2"), bar("A#5:4!"), bar("G#5:2 E5:2")] + CHORUS_MEL[4:7] + [bar("G#5:4")]
BRIDGE_MEL = [bar("R:1 A4:1 G#4:2"), bar("R:0.5 A4:0.5 C#5:0.5 D#5:0.5 F#5:2"), bar("G#5:3 D#5:1"), bar("C#5:4"),
              bar("R:1 A4:1 C#5:1 F#5:1"), bar("F#5:1 D#5:1 C5:2"), bar("R:2 E5:1 D#5:1"), bar("C#5:2 R:2")]
# サックスの独奏（Aメロの和音の上。チョーキングの代わりに、しゃくり上げ / を山の音にだけ）
SAX_SOLO = [
    bar("G#4:0.5 B4:0.5 C#5:0.5 E5:0.5 G#5:1.5 F#5:0.5"),
    bar("A#4:2/ R:0.5 C#5:0.5 E5:0.5 F#5:0.5"),
    bar("R:0.5 E5:0.25 F#5:0.25 G#5:0.5 F#5:0.5 D#5:1.5 C#5:0.5"),
    bar("A#4:2 F#4:1 R:1"),
    bar("E5:0.5 G#5:0.5 B4:1 G#4:2"),
    bar("F#5:1.5/ D#5:0.5 B4:0.5 D#5:0.5 F#5:1"),
    bar("C#5:0.5 D#5:0.5 F#5:0.5 A#5:0.5 G#5:2"),
    bar("C5:1 G#4:1 F#4:1 D#4:1"),
]
# サックスの合いの手（Aメロ2: 旋律の休みに答える）
SAX_FILL = [R4, bar("R:2 C#5:0.5 E5:0.5 F#5:1"), R4, bar("R:2 C#5:0.5 E5:0.5 F#5:1"),
            R4, R4, R4, bar("R:2 G#4:0.5 C5:0.5 D#5:1")]

# ---------------- クリーンの和音（3本に分けて同時に鳴らす。刻まず、裏から伸ばす） ----------------
VOICE = {
    "C#m9": ["E3", "B3", "D#4"], "F#9": ["A#3", "E4", "G#4"], "Amaj7": ["G#3", "C#4", "E4"], "B6": ["F#3", "G#3", "D#4"],
    "G#7sus4": ["F#3", "C#4", "D#4"], "G#7": ["F#3", "C4", "D#4"], "F#m9": ["A3", "E4", "G#4"], "B9": ["D#3", "A3", "C#4"],
    "Emaj7": ["G#3", "D#4", "F#4"], "D#m7b5": ["F#3", "A3", "C#4"],
}
COMP = ["R:1.5 {}:1 R:0.5 {}:1", "R:0.5 {}:1.5 R:0.5 {}:1.5", "R:1.5 {}:2.5", "{}:1 R:0.5 {}:2.5"]


def comp(ch, i, voice):
    v = VOICE[ch][voice]
    pat = COMP[i % 4]
    return bar(pat.format(*([v] * pat.count("{}"))))


# ---------------- 組み立て ----------------
P = {k: [] for k in ["riff", "rhy", "rhy_in", "arp", "lead", "harm", "sax", "bass", "mute", "c0", "c1", "c2"]}
kit = Kit(BEATS)
RIDE = "D2"; BELL = "F2"; CR = "C2"; CR2 = "G2"; CHINA = "B2"

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    root = root_note(ch)
    groot = root_note(ch, "E2", "D#3")

    # ----- リフ -----
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2:
            rf = bar("C#2:4!") if i == 0 else R4                    # 1拍目の一撃のあと、ギターは休む（路地へ入る）
        elif name == "outro" and last:
            rf = bar("C#2:4!")
        else:
            rf = {"C#m9": RIFF_A if i % 2 == 0 else RIFF_A2, "F#9": RIFF_B, "G#7": RIFF_G}[ch]
            if name == "intro" and last: rf = bar("F#2:0.5! R:0.25 F#3:0.25 E3:0.5 C#3:0.5 F#2:2!")   # 前ぶれ: 伸ばしてAメロへ
        P["riff"].append(rf)
    elif name == "break":
        P["riff"].append(bar("C#2:0.75! C#3:0.75 C#2:2.5!") if i < n - 1 else bar("C#2:0.75! C#3:0.75 G#2:0.5! R:2"))
    else:
        P["riff"].append(R4)

    # ----- リズムギター（伸ばす。サビとAメロ2・ブリッジ以外は休む） -----
    if name.startswith("chorus"):
        if name == "chorus3" and i < 4: s = bar(f"{groot}:4!")
        elif last: s = bar(f"{groot}:2! R:2") if name != "chorus3" else bar(f"{groot}:4!")
        else: s = bar(f"{groot}:1.5! {groot}:1.5 {groot}:1")
        P["rhy"].append(s); P["rhy_in"].append(s if not (name == "chorus3" and i < 4) else R4)
    elif name == "verse2":
        P["rhy"].append(bar(f"{groot}:4") if not last else bar(f"{groot}:2! R:2")); P["rhy_in"].append(R4)
    elif name in ("pre", "pre2"):
        P["rhy"].append(bar(f"C#3:2! C#3:2") if not last else bar("C#3:2! C#3:1! R:1")); P["rhy_in"].append(R4)
    elif name == "break":
        P["rhy"].append(P["riff"][-1]); P["rhy_in"].append(P["riff"][-1])
    elif name == "solo" and i >= 4:
        P["rhy"].append(bar(f"{groot}:4")); P["rhy_in"].append(R4)
    else:
        P["rhy"].append(R4); P["rhy_in"].append(R4)

    # ----- 分散和音（Bメロ2 とサビ2 の後半だけ。動きを足す） -----
    if (name == "pre2") or (name == "chorus2" and i >= 4 and not last):
        t = chord_tones(ch.split("/")[0], "B3", "B4")[:5]
        while len(t) < 5: t.append(up(t[len(t) - 3], 1))
        pat = [[0, 1, 2, 3, 4, 3, 2, 1], [0, 2, 1, 3, 2, 4, 3, 1]][i % 2]
        P["arp"].append(bar(*[f"{t[j]}:0.5{'!' if k % 4 == 0 else ''}" for k, j in enumerate(pat)]))
    else:
        P["arp"].append(R4)

    # ----- クリーンの和音（Aメロ1・ブリッジ） -----
    for v in range(3):
        if (name == "verse" and not last) or (name == "bridge" and ch in VOICE):
            P[f"c{v}"].append(comp(ch, i, v))
        elif name == "verse" and last:
            P[f"c{v}"].append(bar(f"{VOICE[ch][v]}:2 R:2"))
        else:
            P[f"c{v}"].append(R4)

    # ----- 旋律 -----
    lead = harm = sax = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]; sax = SAX_FILL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2":
        lead = CHORUS2_MEL[i]; harm = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]; harm = shift_oct(strip_marks(lead), -1) if i >= 4 else R4
    elif name == "bridge": sax = BRIDGE_MEL[i]
    elif name == "solo": sax = SAX_SOLO[i]
    P["lead"].append(lead); P["harm"].append(harm); P["sax"].append(sax)

    # ----- ベース -----
    mute = R4
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0: b = bar("C#1:1! R:1 C#1:1 E1:1")          # 一撃のあと、ウォーキングで路地へ
        elif name == "intro" and i == 1: b = bar("F#1:1 G#1:1 B1:1 C2:1")
        elif name == "outro" and last: b = bar("C#1:4!")
        else: b = unison_low(P["riff"][-1], -1, "B0")
        P["bass"].append(b)
    elif name == "verse":
        P["bass"].append(bass_walk(ch, nxt, BEATS) if not last else bar("G#1:1! D#2:1 C2:1 G#1:1"))
    elif name == "verse2":
        # 2回目は8分で押す（オクターブを混ぜた旋律ぎみの線）
        r = root
        P["bass"].append(bar(f"{r}:0.5! {r}:0.5 {up(r,1)}:0.5 {r}:0.5 {fifth_of(ch)}:0.5 {r}:0.5 {up(r,1)}:0.5 {fifth_of(ch)}:0.5") if not last else bar(f"{r}:1! {r}:1 R:2"))
        mute = bar("R:0.25 C#2:0.25, R:3.5") if i % 2 == 0 else R4
    elif name in ("pre", "pre2"):
        P["bass"].append(bar(" ".join(f"C#2:0.5{'!' if j % 2 == 0 else ''}" for j in range(8))) if not last else bar("C#2:0.5! C#2:0.5 C#2:0.5 C#2:0.5 C#2:1! R:1"))
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4: P["bass"].append(bar(f"{root}:3! {root}:1"))
        elif last: P["bass"].append(bar(f"{root}:1.5! {root}:0.5 R:2") if name != "chorus3" else bar(f"{root}:4!"))
        else: P["bass"].append(bass_root8(ch, BEATS, nxt))
    elif name == "bridge":
        P["bass"].append(bass_walk(ch, nxt, BEATS))
    elif name == "solo":
        P["bass"].append(bass_walk(ch, nxt, BEATS) if i < 4 else bass_root8(ch, BEATS, nxt))
    elif name == "break":
        P["bass"].append(unison_low(P["riff"][-1], -1, "B0"))
    else:
        P["bass"].append(R4)
    P["mute"].append(mute)

    # ----- ドラム -----
    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i == 0:
            k = "X..............."; s = "X.....o.......o."; cym = f"{CR}:1! {BELL}:0.75 {BELL}:0.75 {BELL}:0.5 {BELL}:1"
        elif name == "intro" and i == 1:
            k, s, tom = linear_fill(kit, 2, 1)
            k = "X.......x" + k[9:]; cym = f"{BELL}:0.75 {BELL}:0.75 {BELL}:0.5 R:2"
        else:
            # リフに合わせる: 低い C♯ の所にキック、2・4拍にスネアとゴースト、ライドのベルは 3・3・2
            k = "X.....x.Xx......"; s = "....X..o....X.o."
            cym = f"{BELL}:0.75! {RIDE}:0.75 {BELL}:0.5 {RIDE}:0.5 {BELL}:0.75 {RIDE}:0.75"
            if i == 2 and name == "intro": cym = f"{CR}:1.5! {RIDE}:0.75 {BELL}:0.5 {RIDE}:0.5 {BELL}:0.75"
            if name == "inter" and i == 0: cym = f"{CHINA}:1.5! {RIDE}:0.75 {BELL}:0.5 {RIDE}:0.5 {BELL}:0.75"
            if last and name != "outro":
                k = "X.....x........."; s = "....X..........."
                tom = tom_triplets_down(2, 2); cym = f"{BELL}:0.75! {RIDE}:0.75 {BELL}:0.5 R:2"
            if name == "outro" and last:
                k = "X..............."; s = "X..............."; cym = f"{CR}:4!"
    elif name == "verse":
        # ジャズ寄り: ライドのレガート（4分＋付点のはね）、キックは弱く、スネアは会話するゴースト
        k = "o.......o.....o." if i % 2 == 0 else "o.....o.....o..."
        s = ["..o....o.o....o.", "....o..o..o....o", "..o..o.....o..o.", "o......o.o..o..."][i % 4]
        cym = f"{RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25"
        if i == 0: cym = f"{CR2}:1! {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25"
        if last:
            k = "X.....x........."; s = "....X..........."
            tom = tom_triplets_down(2, 2); cym = f"{RIDE}:1! {RIDE}:1 R:2"
    elif name == "verse2":
        # 手と足が重ならないリニアのハイハット（16分）
        k = ["X..x..X...x.....", "X.....X..x..x...", "X..x..X...x..x..", "X.....X.x...x..."][i % 4]
        s = "....X.......X..." if i % 4 != 3 else "....X..o.o..X..o"
        h = "".join("." if (k[j] != "." or s[j] != ".") else ("x" if j % 2 == 0 else "o") for j in range(16))
        if i == 0: cym = f"{CR}:1! R:3"
        if last:
            k, s, tom = linear_fill(kit, 2, 2)
            k = "X..x..X." + k[8:]; s = "....X..." + s[8:]; h = "x.x.x.x........."
    elif name in ("pre", "pre2"):
        # 積み上げ: 2分 → 4分 → 8分 → 16分のキック、最後の1拍は全員休む
        k = ["X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "XxXxXxXxXxXx...."][i]
        s = ["........X.......", "....X.......X...", "....X.......X...", "..X...X...X....."][i]
        h = ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", "................"][i]
        if i == 0: cym = f"{CR2}:2! R:2"
        if i == 3: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! R:1"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 4
        if half:
            k = "X.......X.x....."; s = "........X......."
            cym = f"{CR}:2! {RIDE}:1 {RIDE}:1" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        else:
            kp = ["X..x..X.X.x.....", "X..x..X.X...X.x.", "X..x..X.X.x...x.", "X...X.X.X.x.X..."]
            k = kp[i % 4]
            s = "....X.......X..." if i % 4 != 3 else "....X..o....X.oo"
            h = "x.X.x.X.x.X.x.X." if i % 8 < 4 else "................"
            cym = R4 if i % 8 < 4 else f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
            if i % 4 == 0: cym = (f"{CR}:1! " if i % 8 == 0 else f"{CR2}:1! ") + (f"{RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5" if i % 8 >= 4 else "R:3")
            if name == "chorus2" and i in (4, 5): k = "XxXxXxXxXxXxXxXx"      # 2回目だけ2小節ツーバス
            if name == "chorus3" and i in (4, 5): k = "XxXxXxXxXxXxXxXx"
        if last and not (name == "chorus3"):
            k = "X.x...X........."; s = "....X..........."; h = "................"
            tom = "R:2 " + tom_triplets_down(2)
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 R:2"
        if name == "chorus3" and last:
            k = "X.....X..x......"; s = "....X.......X..."; cym = f"{CR}:1! {RIDE}:1 {RIDE}:1 {RIDE}:1"
    elif name == "bridge":
        # ジャズの区間: ライドのレガート、キックは羽のように、スネアはゴーストとクロスのように薄く
        k = "o.......o......." if i % 2 == 0 else "o.....o........."
        s = ["..o.....o.o.....", "....o.....o..o..", "..o..o....o.....", ".o......o...o..."][i % 4]
        cym = f"{RIDE}:1 {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1 {RIDE}:0.75 {RIDE}:0.25"
        if i == 0: cym = f"{CR2}:2 {RIDE}:1 {RIDE}:1"
        if last:
            tom = "R:1 " + tom_16_down(2) + " R:1"; k = "X..............."; s = "................"
    elif name == "solo":
        # 独奏の下: 前半はライドのはね、後半は5つずつのかたまり（16分5つ）で小節線をまたぐ
        if i < 4:
            k = "X.....x...X....." if i % 2 == 0 else "X.....x.....x..."
            s = "....X..o....X..o"; cym = f"{RIDE}:1! {RIDE}:0.75 {RIDE}:0.25 {BELL}:1! {RIDE}:0.75 {RIDE}:0.25"
        else:
            off = (i - 4) * 16
            k = "".join("X" if (off + j) % 5 == 0 else "." for j in range(16))
            s = "....X.......X..."
            s = "".join("." if k[j] != "." else s[j] for j in range(16))
            cym = f"{BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5"
        if i == 4: cym = f"{CR}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5 {RIDE}:0.5"
        if last:
            k = "X..............."; s = "................"; cym = f"{RIDE}:1 R:3"
            tom = "R:1 " + tom_triplets_down(2) + " R:1"
    elif name == "break":
        # ブレイクダウン: ハーフタイム、キックとギターをそろえる、最後は2拍休む
        k = "X..X..X........." if i < n - 1 else "X..X..X.X......."
        s = "........X......." if i < n - 1 else "........X......."
        cym = f"{CHINA}:0.75! {CHINA}:0.75 {CHINA}:2.5!" if i < n - 1 else f"{CHINA}:0.75! {CHINA}:0.75 {CHINA}:0.5! R:2"
        if i == 0: cym = f"{CR}:0.75! {CHINA}:0.75 {CHINA}:2.5!"
    kit.add(k, s, h, tom, cym)

# 区間の頭の前ぶれ: サビの前の2拍にシンバルのスウェル（本物の録音）
FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nxt_name = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nxt_name in ("chorus", "chorus2") : FX.append(bar("R:2 C4:2"))
    elif i == n - 1 and nxt_name == "break": FX.append(bar("R:3 D4:1"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(arp_part(J("arp"), vol=0.08))
song.add([clean_part(J(f"c{v}"), vol=0.075, pan=[-0.35, 0.35, 0.05][v], role=f"クリーンの和音（{v + 1}）") for v in range(3)])
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
# アルトサックス（録音の音源）: 息の長い音、強い音は山だけ。部屋の響きを少し
song.add(part("アルトサックス", "brass", J("sax"), patch="altoSax", volume=0.16, pan=0.12, reverb=0.3, phrase=8, attack=0.03, release=0.35,
              fx=[{"type": "eq", "low": -2, "mid": 1, "midHz": 1500, "high": 0}, {"type": "delay", "beats": 0.75, "mix": 0.1, "feedback": 0.2}, {"type": "plate", "mix": 0.18}]))
song.add(bass_part(J("bass")))
if any(m != R4 for m in P["mute"]): song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "bright-nu-wall"
add_layer(song, "piano", "裏口の酒場で、古いピアノが旅人を迎える。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-01-rojiura.json"
    song.write(out)
    check_clash(song)
