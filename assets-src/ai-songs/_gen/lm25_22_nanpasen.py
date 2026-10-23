# ラウド25曲（第2シリーズ）22「難破船の歌」（仮）。イメージ: 海（船乗りの歌と難破）。E 短調・96・6/4（3+3 と 2+2+2）。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: フィドル（民謡風のバイオリン。船乗りの歌・ジグ・生き残った者の歌）
# 物語: 甲板で船乗りたちが歌う（3+3 の舟歌）→ 嵐（2+2+2 の重いヘミオラ）→ 難破（ほぼ無音、低い一撃だけ）→ 生き残った者がフィドルでゆっくり歌う
#   → 最後のサビで全員がもう一度歌い、フィドルの舟歌で終わる。
# 形（ほかの曲と変える）: 6拍子の数え方そのものが場面で変わる（舟歌は 3+3、嵐は 2+2+2）。難破の場面はほぼ無音
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 96, 6
bar = Bars(BEATS)
R6 = bar.rest()

FORM = [("intro", 4), ("verse", 6), ("chorus", 6), ("jig", 2), ("verse2", 4), ("chorus2", 6), ("storm", 8), ("wreck", 4), ("survivor", 4),
        ("chorus3", 8), ("outro", 4)]
CHORUS = ["G", "D/F#", "Em", "C", "F", "B7"]
CH = {"intro": ["Em", "D", "C", "B7"], "verse": ["Em", "D", "Em", "Bm", "C", "B7"], "chorus": CHORUS, "jig": ["Em", "B7"],
      "verse2": ["Em", "D", "C", "B7"], "chorus2": CHORUS, "storm": ["Em", "Em", "C", "C", "Am", "Am", "B7", "B7"],
      "wreck": ["E5", "E5", "C", "B7"], "survivor": ["Em", "D", "C", "B7"], "chorus3": CHORUS[:5] + ["Em/B", "Am7", "B7"], "outro": ["Em", "D", "C", "Em"]}
song = Song("難破船の歌（仮）",
            "仮: ラウド25曲（第2シリーズ）の22曲目。イメージは海（船乗りの歌と難破）。E 短調・96・6/4。舟歌は 3+3、嵐は 2+2+2 の重いヘミオラと、6拍子の数え方が場面で変わる。"
            "フィドルの舟歌とジグ、難破はほぼ無音、生き残った者のフィドル、最後のサビで全員がもう一度歌う。サビは F（♭Ⅱ）の光。別の楽器はフィドル。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 甲板で歌う船乗りたち、嵐、難破、生き残った者の歌、そして全員でもう一度。"
song.kinds = {"jig": "interlude", "storm": "bridge", "wreck": "break", "survivor": "interlude"}
song.flags = "--space hall --space-wet 0.15"
SECS, NB = song.secs, song.nb

RIFF33 = {"Em": bar("E2:1.5! B2:0.5 E3:0.5 D3:0.5", "E2:1.5! G2:0.5 A2:0.5 B2:0.5"), "D": bar("D2:1.5! A2:0.5 D3:0.5 C#3:0.5", "D2:1.5! F#2:0.5 G2:0.5 A2:0.5"),
          "C": bar("C2:1.5! G2:0.5 C3:0.5 B2:0.5", "C2:1.5! E2:0.5 F#2:0.5 G2:0.5"), "B7": bar("B1:1.5! F#2:0.5 B2:0.5 A2:0.5", "B1:1.5! D#2:0.5 F#2:0.5 A2:0.5")}
RIFF222 = {"Em": bar("E2:1! E3:1", "D3:1! B2:1", "C3:1! B2:0.5 G2:0.5"), "C": bar("C2:1! C3:1", "G2:1! E2:1", "G2:1! E2:0.5 D2:0.5"),
           "Am": bar("A1:1! A2:1", "G2:1! E2:1", "C3:1! B2:0.5 G2:0.5"), "B7": bar("B1:1! B2:1", "A2:1! F#2:1", "D#2:1! F#2:0.5 A2:0.5")}

FID_SHANTY = [bar("E5:1 F#5:0.5 G5:0.5 E5:1", "B4:1.5 D5:0.5 E5:1"), bar("F#5:1 E5:0.5 D5:0.5 A4:1", "D5:1.5 E5:0.5 F#5:1"),
              bar("G5:1 F#5:0.5 E5:0.5 C5:1", "E5:1.5 D5:0.5 C5:1"), bar("B4:1 D#5:0.5 F#5:0.5 A5:1", "F#5:3")]
FID_JIG = [bar("E5:0.5 F#5:0.5 G5:0.5 F#5:0.5 E5:0.5 D5:0.5", "B4:0.5 D5:0.5 E5:0.5 G5:0.5 B5:1"),
           bar("A5:0.5 G5:0.5 F#5:0.5 E5:0.5 D#5:0.5 E5:0.5", "F#5:0.5 B4:0.5 D#5:0.5 F#5:0.5 B5:1")]
FID_SURV = [bar("E5:3", "B4:1.5 D5:0.5 E5:1"), bar("F#5:3", "D5:3"), bar("G5:2 E5:1", "C5:3"), bar("B4:1.5 D#5:0.5 F#5:1", "B4:3")]
VERSE_MEL = [bar("R:1 B4:1 E5:1", "D5:1.5 B4:0.5 G4:1"), bar("A4:1.5 B4:0.5 D5:1", "F#4:3"), bar("R:1 G4:1 B4:1", "E5:2 D5:1"),
             bar("B4:1.5 A4:0.5 F#4:1", "D4:3"), bar("R:1 E4:1 G4:1", "C5:2 E5:1"), bar("A4:1 F#4:1 D#4:1", "B3:3")]
VERSE2_MEL = [bar("R:1 E5:1 G5:1", "F#5:1.5 E5:0.5 B4:1"), bar("D5:1.5 E5:0.5 F#5:1", "A5:3"), bar("R:1 C5:1 E5:1", "G5:2 E5:1"), bar("D#5:1 F#5:1 A5:1", "B5:3")]
CHORUS_MEL = [bar("D5:1 G5:1 B5:1", "D6:2! B5:1"), bar("A5:3", "F#5:1.5 E5:0.5 D5:1"), bar("E5:1 G5:1 B5:1", "E6:3!"),
              bar("C6:2 E6:1", "G5:3"), bar("A5:1.5 C6:0.5 A5:1", "F5:3"), bar("D#6:2 B5:1", "F#5:2 R:1")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[1] = bar("A5:1 D6:1 A5:1", "F#5:3")
CHORUS2_MEL[3] = bar("C6:1 E6:1 C6:1", "G5:3")
CHORUS3_MEL = CHORUS_MEL[:5] + [bar("B5:1 E6:1 B5:1", "G5:3"), bar("C6:1.5 B5:0.5 A5:1", "E5:3"), bar("D#5:1 F#5:1 A5:1", "B5:3!")]
VERSE_BASS = [bar("E1:1.5! B1:0.5 E2:1", "G2:1.5 F#2:0.5 E2:1"), bar("D2:1.5 A1:0.5 D2:1", "F#2:1.5 E2:0.5 D2:1"), bar("E2:1.5 G2:0.5 B2:1", "E2:3"),
              bar("B1:1.5 D2:0.5 F#2:1", "B1:3"), bar("C2:1.5 E2:0.5 G2:1", "C2:1.5 D2:0.5 E2:1"), bar("B1:1.5 D#2:0.5 F#2:1", "A2:1.5 F#2:0.5 D#2:1")]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "fid", "clean", "bass"]}
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

    rf = R6
    if name in ("intro", "outro") and i >= 2 and not (name == "outro" and last) and base_ch in RIFF33: rf = RIFF33[base_ch]
    elif name == "verse2" and base_ch in RIFF33: rf = RIFF33[base_ch]
    elif name == "storm": rf = RIFF222[base_ch]
    elif name == "wreck": rf = bar("E1:6!".replace("E1", "E2")) if i == 0 else (bar("C2:6!") if i == 2 else R6)
    elif name == "outro" and last: rf = bar("E2:6!")
    P["riff"].append(rf)

    s = si = R6
    if name == "verse" and i >= 3:
        s = bar(f"{groot}:3 {groot}:3") if not last else bar(f"{groot}:3! R:3")
    elif name.startswith("chorus"):
        s = bar(f"{groot}:3! {groot}:1.5 {groot}:1.5") if not (last and name != "chorus3") else bar(f"{groot}:3! R:3")
        si = s
    elif name == "storm":
        s = si = bar(f"{groot}:2! {groot}:2 {groot}:2")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = fid = clean = R6
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
        fid = [bar("A4:3 C5:3"), bar("B4:3 G4:3"), bar("C5:3 E5:3"), bar("D#5:3 F#5:3")][i - 4] if i >= 4 else R6  # 全員で歌う所: フィドルが下で長い対旋律
    elif name == "intro": fid = FID_SHANTY[i]
    elif name == "jig": fid = FID_JIG[i]
    elif name == "survivor":
        fid = FID_SURV[i]
        t = chord_tones(base_ch, "E3", "E5"); clean = bar(" ".join(f"{t[j % len(t)]}:1" for j in (0, 2, 4, 3, 2, 1)))
    elif name == "outro": fid = FID_SHANTY[i] if not last else bar("E5:6")
    elif name == "storm" and i >= 4: lead = [bar("A5:2! C6:2 E6:2"), bar("E6:2 C6:2 A5:2"), bar("B5:2! D#6:2 F#6:2".replace("F#6", "B5")), bar("A5:2 F#5:2 D#5:2")][i - 4]
    P["lead"].append(lead); P["harm8"].append(harm8); P["fid"].append(fid); P["clean"].append(clean)

    if name == "intro": b = R6 if i < 2 else unison_low(P["riff"][-1], -1, "B0")
    elif name == "verse": b = VERSE_BASS[i]
    elif name == "verse2": b = unison_low(P["riff"][-1], -1, "B0")
    elif name.startswith("chorus"):
        if last and name != "chorus3": b = bar(f"{root}:3! R:3")
        else: b = bar(f"{root}:1.5! {root}:0.5 {up(root, 1)}:1 {fifth_of(base_ch)}:1.5 {root}:0.5 {approach_note(ch, nxt)}:1")
    elif name == "jig": b = bar(f"{root}:1.5! {fifth_of(base_ch)}:1.5 {root}:1.5! {fifth_of(base_ch)}:1.5")
    elif name == "storm": b = unison_low(P["riff"][-1], -1, "B0")
    elif name == "wreck": b = bar("E1:6!") if i == 0 else (bar("C1:6!".replace("C1", "C2")) if i == 2 else R6)
    elif name == "survivor": b = bar(f"{root}:6")
    elif name == "outro": b = unison_low(P["riff"][-1], -1, "B0") if P["riff"][-1] != R6 else (bar("E1:6!") if last else bar(f"{root}:6"))
    else: b = R6
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name in ("intro", "outro", "jig"):
        # 舟歌: 3+3 の足踏み（キック1・4拍目、スネア3・6拍目の裏）
        if name == "intro" and i < 2: k = g24(0, 12); s = g24(8, 20, ch="o")
        elif name == "outro" and last: k = g24(0); s = g24(0); cym = f"{CR}:6!"
        else:
            k = g24(0, 12, 18); s = g24(8, 20); h = g24(*range(0, 24, 2), ch="x")
            if (name == "intro" and i == 2) or (name == "jig" and i == 0): cym = f"{CR}:1.5! R:4.5"; h = g24(*range(6, 24, 2), ch="x")
            if name == "jig": cym = f"{BELL}:1.5! {RIDE}:1.5 {BELL}:1.5! {RIDE}:1.5"; h = None
    elif name in ("verse", "verse2"):
        k = g24(0, 12) if i % 2 == 0 else g24(0, 10, 12)
        s = g24(8, 20); s = g24(*[p for p in (5, 17, 23) if k[p] == "."], ch="o", base=s)
        h = g24(*range(0, 24, 2), ch="x") if name == "verse" else None
        if name == "verse2": cym = f"{RIDE}:1.5! {BELL}:1.5 {RIDE}:1.5! {BELL}:1.5"
        if i == 0: cym = f"{CR2}:1.5! " + ("R:4.5" if name == "verse" else f"{BELL}:1.5 {RIDE}:1.5! {BELL}:1.5"); h = h and g24(*range(6, 24, 2), ch="x")
        if last: k = g24(0, 6); s = g24(); tom = "R:3 " + tom_triplets_down(3); h = None; cym = None
    elif name.startswith("chorus"):
        k = g24(0, 3, 6, 12, 15, 18); s = g24(8, 20)
        h = "".join("X" if j in (0, 12) else ("x" if j % 2 == 0 else ".") for j in range(24)); h = "".join("." if s[j] == "X" else c for j, c in enumerate(h))
        if i % 2 == 0: cym = (f"{CR}:1.5! " if i % 4 == 0 else f"{CR2}:1.5! ") + "R:4.5"; h = "......" + h[6:]
        if name == "chorus3" and i >= 4: k = "".join("X" if j % 2 == 0 else "x" for j in range(24)); k = "".join("." if s[j] != "." else c for j, c in enumerate(k)); h = None; cym = cym or f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
        if last and name != "chorus3": k = g24(0, 6); s = g24(); tom = "R:3 " + tom_triplets_down(3); h = None; cym = None
        if name == "chorus3" and last: k = g24(0, 12); s = g24(8); h = None; cym = f"{CR}:6!"
    elif name == "storm":
        # 嵐: 2+2+2（ヘミオラ）。ツーバスとチャイナが2拍ごと
        k = "".join("X" if j % 2 == 0 else "x" for j in range(24)); s = g24(4, 12, 20)
        k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = f"{CHINA}:2! {CHINA}:2! {CHINA}:2!" if i % 2 == 0 else f"{RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1 {RIDE}:1! {BELL}:1"
        if i == 0: cym = f"{CR}:2! {CHINA}:2! {CHINA}:2!"
        if last: k = "".join("X" for _ in range(16)) + "........"; s = g24(16, 18, 20, 22); cym = None
    elif name == "wreck":
        # 難破: ほぼ無音。低い一撃だけ
        if i in (0, 2): k = g24(0); tom = "A2:6!"; cym = f"{CR}:6!" if i == 0 else None
    elif name == "survivor":
        cym = f"{RIDE}:3, {RIDE}:3," if i >= 2 else None
        if last: tom = "R:3 " + tom_16_down(3)
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx.startswith("chorus"): FX.append(bar("R:3 C4:3"))
    elif name == "storm" and i == 6: FX.append(bar("E4:6"))
    elif name == "wreck" and i == 1: FX.append(bar("R:2 D4:4"))
    else: FX.append(R6)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(clean_part(J("clean"), vol=0.09, pan=0.25, role="クリーンの分散和音（生き残った者）"))
song.add(part("フィドル", "fiddle", J("fid"), volume=0.16, pan=-0.15, reverb=0.5, gainDb=3, bright=-0.15, attack=0.35, release=0.7,
              doubleDetune={"cents": 5, "spread": 0.3}, phrase=8,
              fx=[{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 1, "mix": 0.08, "feedback": 0.2},
                  {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "glossy-jrock"
add_layer(song, "choir", "沈んだ船乗りたちの声が、海の底から歌う。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-22-nanpasen.json"
    song.write(out)
    check_clash(song)
