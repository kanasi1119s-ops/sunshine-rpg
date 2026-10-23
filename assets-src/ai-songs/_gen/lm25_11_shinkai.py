# ラウド25曲（第2シリーズ）11「深海の時計」（仮）。イメージ: 海（光の届かない深さで時を刻むもの）。F 短調・86・6/4（3+3）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 琴（時計の音のような8分の分散和音と、ブリッジの旋律）
# しかけ:
#   - 6拍子を 3+3 で数える。看板リフは引き波のように F から A♭・G と寄せては返す。重く、刻まない
#   - 時計: Aメロはハイハットが4分で正確に時を刻み、琴が8分で同じ形をくり返す
#   - ベースは旋律（スライドで、フレットレスのように歌う）
#   - サビ: D♭ から下りる低音（D♭→C→B♭→A♭）と、5小節目の G♭（ナポリの ♭II）で水面の光
#   - 空間: 曲全体をホールの残響に通す（人間「自然を感じる曲は、その空間が感じられるように」）。フロアタムのうねりとシンバルのスウェル
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 86, 6
bar = Bars(BEATS)
R6 = bar.rest()

FORM = [("intro", 4), ("verse", 6), ("pre", 2), ("chorus", 6), ("inter", 3), ("verse2", 4), ("pre2", 2), ("chorus2", 6),
        ("bridge", 5), ("break", 2), ("chorus3", 8), ("outro", 3)]
VERSE = ["Fm", "Dbmaj7", "Bbm7", "C7sus4", "Abmaj7", "C7"]
PRE = ["Bbm7", "C7sus4"]
CHORUS = ["Db", "Ab/C", "Bbm7", "Fm/Ab", "Gb", "C7"]
CH = {"intro": ["Fm", "Fm", "Db", "C7"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": ["Fm", "Db", "C7"],
      "verse2": VERSE[:4], "pre2": PRE, "chorus2": CHORUS, "bridge": ["Fm", "Fm/Eb", "Dbmaj7", "Bbm7", "C7sus4"],
      "break": ["F5", "F5"], "chorus3": ["Db", "Ab/C", "Bbm7", "Fm/Ab", "Gb", "Eb7", "C7sus4", "C7"], "outro": ["Fm", "Db", "Fm"]}
song = Song("深海の時計（仮）",
            "仮: ラウド25曲（第2シリーズ）の11曲目。イメージは海（光の届かない深さで時を刻むもの）。F 短調・86・6/4（3+3）。引き波のような看板リフ、"
            "Aメロはハイハットと琴が時を刻み、ベースはスライドで歌う。サビは D♭ から下りる低音と G♭ の光。ホールの残響で深さを出す。別の楽器は琴。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.flags = "--space hall --space-wet 0.16"
song.desc += " 物語: 沈んだ船の中で止まった時計が、もう一度だけ時を刻み、ゆっくり止まる。"
SECS, NB = song.secs, song.nb

RIFF = {"Fm": [bar("F2:1.5! F2:0.5 G#2:0.5 G2:0.5", "F2:1.5! C3:0.5 C#3:1"), bar("F2:1.5! F2:0.5 G#2:0.5 A#2:0.5", "C3:1.5! A#2:0.5 G#2:0.5 G2:0.5")],
        "Db": [bar("C#2:1.5! C#2:0.5 F2:0.5 D#2:0.5", "C#2:1.5! G#2:0.5 A#2:1")] * 2,
        "C7": [bar("C2:1.5! C2:0.5 E2:0.5 F2:0.5", "C2:1.5! G2:0.5 A#2:1")] * 2}

VERSE_MEL = [bar("R:1 C4:0.5 F4:0.5 G#4:1", "G4:1 F4:1 C4:1"), bar("C#4:2 F4:1", "C5:2 G#4:1"),
             bar("R:0.5 A#4:0.5 C#5:0.5 C5:0.5 A#4:1", "G#4:2 F4:1"), bar("G4:3", "F4:1 G4:1 R:1"),
             bar("D#4:1 G#4:1 C5:1", "A#4:1 G4:1 D#4:1"), bar("E4:2 G4:1", "A#4:2 R:1")]
VERSE2_MEL = [bar("R:1 F4:0.5 G#4:0.5 C5:1", "A#4:1 G#4:1 F4:1"), bar("F4:2 G#4:1", "C5:2 F5:1"),
              bar("R:0.5 C#5:0.5 F5:0.5 D#5:0.5 C#5:1", "C5:2 A#4:1"), bar("C5:3", "A#4:1 C5:1 R:1")]
PRE_MEL = [bar("C#5:1 F5:1 G#5:1", "F5:1 C#5:1 A#4:1"), bar("C5:1 F5:1 G5:1", "A#5:2 R:1")]
CHORUS_MEL = [bar("F5:3!", "G#5:1 F5:1 C#5:1"), bar("D#5:2 C5:1", "G#4:2 D#5:1"), bar("C#5:3", "F5:1 G#5:1 A#5:1!"),
              bar("G#5:2 G5:1", "F5:2 C5:1"), bar("A#4:1 C#5:1 F#5:1", "A#5:2 C#6:1!"), bar("C6:2 A#5:1", "G5:1 E5:1 C5:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("D#5:1 G#5:1 C6:1", "G#5:2 D#5:1")
CHORUS2_MEL[3] = bar("G#5:1 C6:1 G#5:1", "F5:3")
CHORUS3_MEL = [bar("G#5:6!"), bar("D#5:3 G#5:3")] + CHORUS_MEL[2:5] + [bar("G5:1 A#5:1 D#6:1", "C#6:2 A#5:1"), bar("C6:3", "A#5:3"), bar("G5:3 E5:3")]

KOTO_CLOCK = {"Fm": "C5 G#4 F4", "Db": "C#5 G#4 F4", "C7": "C5 G4 E4", "Fm/Eb": "C5 G#4 D#4", "Dbmaj7": "C5 G#4 F4", "Bbm7": "C#5 A#4 F4", "C7sus4": "C5 G4 F4"}
def koto_clock(ch):
    a, b, c = KOTO_CLOCK[ch].split()
    return bar(" ".join(f"{x}:0.5{'!' if j % 6 == 0 else ''}" for j, x in enumerate([a, b, c] * 4)))
KOTO_BRIDGE = [bar("C5:1.5 D#5:0.5 F5:1", "D#5:1 C5:1 G#4:1"), bar("C5:3", "G#4:1 F4:1 D#4:1"), bar("F4:1.5 G#4:0.5 C5:1", "D#5:2 C5:1"),
               bar("C#5:3", "F5:2 G#5:1"), bar("G5:3", "F5:1 C5:1 A#4:1")]
# ベースの旋律（スライドで歌う）
VERSE_BASS = [bar("F1:1.5! C2:0.5 F2:1", "G#2:1 G2:1 F2:1"), bar("C#2:2 F2:1", "G#2:1>C3 C3:1 G#2:1"), bar("A#1:1.5 F2:0.5 A#2:1", "G#2:1 F2:1 C#2:1"),
              bar("C2:3", "F2:1 G2:1 A#2:1"), bar("G#1:1.5 D#2:0.5 G#2:1", "G2:1 D#2:1 C2:1"), bar("C2:2 E2:1", "G2:1>A#2 A#2:1 G2:1")]
BRIDGE_BASS = [bar("F2:3 G#2:1>C3 C3:2"), bar("D#2:3 G2:1 G#2:2"), bar("C#2:3 F2:1>G#2 G#2:2"), bar("A#1:3 C#2:1 F2:2"), bar("C2:6")]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "koto", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"


def g24(*pos, ch="X", base=None):
    return kit.grid(pos, ch, base)


SWELL = " ".join(f"A2:0.25{',' if j < 8 else ('' if j < 16 else '!')}" for j in range(24))   # フロアタムのうねり（弱→強）

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R6
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: rf = R6
        elif name == "outro" and last: rf = R6
        else: rf = RIFF[base_ch if base_ch in RIFF else "Fm"][i % 2]
    elif name == "break":
        rf = bar("F2:1.5! F2:1.5!", "F#2:3!") if i < n - 1 else bar("F2:1.5! F#2:1.5!", "R:3")
    P["riff"].append(rf)

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

    lead = harm8 = koto = R6
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        if i >= 2: harm8 = shift_oct(strip_marks(lead), -1)
    if (name == "intro") or (name == "verse" and i < 4) or (name == "outro" and not last):
        kc = base_ch if base_ch in KOTO_CLOCK else ("C7" if base_ch.startswith("C") else "Fm")
        koto = koto_clock(kc)
    elif name == "bridge":
        koto = KOTO_BRIDGE[i]
    elif name == "outro" and last:
        koto = bar("C5:1 G#4:1 F4:1.5 C4:2.5")          # 時計がゆっくりになって止まる
    P["lead"].append(lead); P["harm8"].append(harm8); P["koto"].append(koto)

    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2: b = bar("F1:6") if i == 0 else bar("F1:3 G#1:1.5 G1:1.5")
        elif name == "outro" and last: b = R6
        else: b = unison_low(P["riff"][-1], -1, "B0")
    elif name == "verse": b = VERSE_BASS[i]
    elif name == "verse2": b = VERSE_BASS[i] if i < 3 else bar("C2:3 F2:1 G2:1 A#2:1")
    elif name in ("pre", "pre2"):
        b = bar(f"{root}:1.5! {root}:1.5 {root}:1.5! {fifth_of(base_ch)}:1.5") if not last else bar(f"{root}:3! {root}:2! R:1")
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 2: b = bar(f"{root}:6!")
        elif last and name != "chorus3": b = bar(f"{root}:3! R:3")
        else: b = bar(f"{root}:1.5! {root}:0.5 {up(root, 1)}:1 {fifth_of(base_ch)}:1.5 {root}:0.5 {approach_note(ch, nxt)}:1")
    elif name == "bridge": b = BRIDGE_BASS[i]
    elif name == "break": b = unison_low(P["riff"][-1], -1, "B0")
    else: b = R6
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("intro", "inter", "outro"):
        if name == "intro" and i < 2:
            # 深い所の時計: ハイハットだけが4分で刻み、フロアタムがうねる
            h = g24(*range(0, 24, 4), ch="x"); tom = SWELL if i == 1 else None
            if i == 0: k = g24(0)
        elif name == "outro" and last:
            h = g24(0, 6, 14, ch="x")                       # 時計の音だけが間をあけて残る
        else:
            k = g24(0, 6, 12, 18) if i % 2 == 0 else g24(0, 6, 12, 16, 18)
            s = g24(12); s = g24(*[p for p in (9, 21) if k[p] == "."], ch="o", base=s)
            cym = f"{RIDE}:1! {RIDE}:1 {BELL}:1 {RIDE}:1! {RIDE}:1 {BELL}:1"
            if (name == "intro" and i == 2) or (name == "inter" and i == 0): cym = f"{CR}:3! {RIDE}:1! {RIDE}:1 {BELL}:1"
            if last and name != "outro":
                k = g24(0, 6); s = g24(12); tom = "R:4 " + tom_16_down(2); cym = f"{RIDE}:1! {RIDE}:1 {BELL}:1 R:3"
    elif name in ("verse", "verse2"):
        k = g24(0, 10, 12) if i % 2 == 0 else g24(0, 6, 12, 22)
        s = g24(12); s = g24(*[p for p in (9, 21) if k[p] == "."], ch="o", base=s)
        h = g24(*range(0, 24, 4), ch="X") if name == "verse" else None
        if name == "verse2": cym = f"{RIDE}:1! {RIDE}:1 {BELL}:1 {RIDE}:1! {RIDE}:1 {BELL}:1"
        if i == 0: cym = f"{CR2}:3! " + (f"{RIDE}:1! {RIDE}:1 {BELL}:1" if name == "verse2" else "R:3"); h = h and ("...." * 3 + h[12:])
        if last: k = g24(0, 6); s = g24(); tom = "R:3 " + tom_triplets_down(3); h = None; cym = None
    elif name in ("pre", "pre2"):
        k = g24(*range(0, 24, 3)) if i == 0 else g24(*range(0, 16))
        s = g24(12) if i == 0 else g24(16, 18, 20, 22)
        tom = SWELL if i == 0 else None
        if i == 0: cym = f"{CR2}:3! R:3"
        else: cym = f"{CHINA}:1! {CHINA}:1 {CHINA}:1! {CHINA}:1 R:2"
    elif name.startswith("chorus"):
        half = name == "chorus3" and i < 2
        if half:
            k = g24(0, 12); s = g24(12)
            cym = f"{CR}:6!" if i == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1 R:3"
            if i == 1: tom = "R:3 " + tom_triplets_down(3)
        else:
            k = [g24(0, 3, 6, 12, 15, 18), g24(0, 6, 9, 12, 18, 21)][i % 2]
            s = g24(8, 20)
            cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5"
            if i % 2 == 0: cym = (f"{CR}:1.5! " if i % 4 == 0 else f"{CR2}:1.5! ") + f"{RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5 {RIDE}:0.5 {RIDE}:0.5 {BELL}:0.5"
            if name == "chorus2" and i == 3: k = "".join("X" if j % 2 == 0 else "x" for j in range(24))
        if last and name != "chorus3":
            k = g24(0, 6); s = g24(8); tom = "R:3 " + tom_triplets_down(3); cym = f"{RIDE}:1 {RIDE}:1 {RIDE}:1 R:3"
        if name == "chorus3" and last:
            k = g24(0, 6, 12); s = g24(8); cym = f"{CR}:3! {RIDE}:1 {RIDE}:1 {RIDE}:1"
    elif name == "bridge":
        # 時計と潮: ハイハットの4分、フロアタムのうねり
        h = g24(*range(0, 24, 4), ch="x"); k = g24(0) if i % 2 == 0 else g24(0, 12)
        tom = SWELL if i % 2 == 1 else None
        if i == 0: cym = f"{CR2}:6"; h = g24(*range(12, 24, 4), ch="x")
        if last: tom = "R:3 " + tom_triplets_down(3); h = g24(0, 4, 8, ch="x")
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
    if name == "intro" and i == 1: FX.append(bar("R:2 E4:4"))                 # 深みから上がるスウェル
    elif i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:2 E4:4"))
    elif i == n - 1 and nx == "break": FX.append(bar("R:4 D4:2"))
    elif name == "bridge" and i == 3: FX.append(bar("R:2 E4:4"))
    elif name == "outro" and i == n - 1: FX.append(bar("R:1 B4:5"))
    else: FX.append(R6)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(part("琴", "koto", J("koto"), volume=0.12, pan=-0.25, reverb=0.45, attack=0.002, release=1.0,
              fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 2200, "high": 1}, {"type": "delay", "beats": 1.5, "mix": 0.18, "feedback": 0.3}, {"type": "plate", "mix": 0.22}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "glossy-jrock"
add_layer(song, "synthpad", "深い海の水圧のような、厚い和音。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-11-shinkai.json"
    song.write(out)
    check_clash(song)
