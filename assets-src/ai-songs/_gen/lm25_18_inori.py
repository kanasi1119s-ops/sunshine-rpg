# ラウド25曲（第2シリーズ）18「祈りの音量」（仮）。イメージ: 宗教×戦争（戦場で鳴るバグパイプ）。E ドリアン・90・3/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: バグパイプ（本物の録音。バグパイプの指の音階＝E ドリアンに合わせた）
# 物語: 霧の戦場に一人のバグパイプ。行進が始まり、戦いの中で祈りに変わり、最後は全員がバグパイプの旋律を一緒に歌う。
# 形（ほかの曲と変える）: 3拍子。前奏はバグパイプとスネアの行進だけ。ブレイクダウンもソロもなく、見せ場は「バグパイプの嘆き」と、最後のサビでバグパイプが旋律を一緒に吹くこと
# しかけ:
#   - ヘミオラ: サビのドラムは2拍ずつのかたまり（2小節で3つ）で、3拍子の上に大きな2拍子が重なる
#   - ドリアンの長三和音（A）で明るく、サビは G から開ける
#   - 祈り（ブリッジ）は C・Am（バグパイプの出ない音）で、バグパイプを休ませる
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 90, 3
bar = Bars(BEATS)
R3 = bar.rest()

FORM = [("intro", 8), ("verse", 16), ("pre", 8), ("chorus", 16), ("lament", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 16),
        ("prayer", 8), ("chorus3", 16), ("outro", 4)]
VERSE = ["Em", "Em", "D", "D", "A", "A", "Em", "Em", "Em", "Em", "G", "G", "D", "D", "Bm", "Bm"]
PRE = ["C", "C", "D", "D", "Bm", "Bm", "A", "A"]
CHORUS = ["G", "G", "D", "D", "A", "A", "Bm", "Bm", "G", "G", "D", "D", "A", "A", "Em", "Em"]
CH = {"intro": ["Em", "Em", "D", "D", "Em", "Em", "A", "Em"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "lament": ["Em", "Em", "Em", "D", "Em", "G", "D", "Em"],
      "verse2": VERSE[8:], "pre2": PRE[4:], "chorus2": CHORUS, "prayer": ["C", "G/B", "Am", "Em", "C", "D", "Bsus4", "B"], "chorus3": CHORUS,
      "outro": ["Em", "D", "Em", "Em"]}
song = Song("祈りの音量（仮）",
            "仮: ラウド25曲（第2シリーズ）の18曲目。イメージは宗教×戦争（戦場で鳴るバグパイプ）。E ドリアン・90・3/4。バグパイプとスネアの行進から始まり、サビはヘミオラ（2拍ずつのかたまり）で"
            "3拍子の上に大きな2拍子が重なる。バグパイプの嘆き、祈りのブリッジ、最後のサビでバグパイプが旋律を一緒に吹く。別の楽器はバグパイプ。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 霧の戦場に一人のバグパイプ。行進が始まり、戦いの中で祈りに変わり、最後は全員がバグパイプと一緒に歌う。"
song.kinds = {"lament": "interlude", "prayer": "bridge"}
song.flags = "--space hall --space-wet 0.14"
SECS, NB = song.secs, song.nb

RIFF = {"Em": [bar("E2:1! B2:0.5 E3:0.5 D3:0.5 B2:0.5"), bar("E2:1! G2:0.5 A2:0.5 B2:1")],
        "D": [bar("D2:1! A2:0.5 D3:0.5 C#3:0.5 A2:0.5"), bar("D2:1! F#2:0.5 G2:0.5 A2:1")],
        "A": [bar("A1:1! E2:0.5 A2:0.5 G2:0.5 E2:0.5")] * 2}

PIPE_MARCH = [bar("E4:1 F#4:0.5 G4:0.5 A4:1"), bar("B4:2 A4:1"), bar("A4:1 F#4:0.5 E4:0.5 D4:1"), bar("F#4:2 A4:1"),
              bar("B4:1 D5:0.5 B4:0.5 A4:1"), bar("G4:2 E4:1"), bar("C#5:1 B4:0.5 A4:0.5 E4:1"), bar("E4:3")]
PIPE_LAMENT = [bar("E4:1 F#4:1 G4:1"), bar("B4:2 A4:1"), bar("G4:1 F#4:1 E4:1"), bar("D4:3"),
               bar("E4:1 G4:1 B4:1"), bar("D5:2 B4:1"), bar("A4:1 G4:1 F#4:1"), bar("E4:3")]
VERSE_MEL = [bar("R:1 B3:1 E4:1"), bar("G4:2 F#4:1"), bar("A4:2 F#4:1"), bar("D4:3"), bar("C#5:1 B4:1 A4:1"), bar("E4:3"), bar("G4:1 A4:1 B4:1"), bar("E4:3"),
             bar("R:1 E4:1 G4:1"), bar("B4:2 A4:1"), bar("D5:2 B4:1"), bar("G4:3"), bar("F#4:1 A4:1 D5:1"), bar("D5:2 A4:1"), bar("B4:2 A4:1"), bar("F#4:3")]
PRE_MEL = [bar("E5:2 C5:1"), bar("G4:3"), bar("F#4:1 A4:1 D5:1"), bar("A4:3"), bar("D5:2 B4:1"), bar("F#5:3"), bar("E5:1 C#5:1 A4:1"), bar("E5:2 R:1")]
CHORUS_MEL = [bar("B4:1 D5:1 G5:1"), bar("B5:3!"), bar("A5:2 F#5:1"), bar("D5:3"), bar("C#5:1 E5:1 A5:1"), bar("C#6:2 B5:1"), bar("B5:2 F#5:1"), bar("D5:3"),
              bar("B4:1 D5:1 G5:1"), bar("D6:3!"), bar("D6:2 A5:1"), bar("F#5:3"), bar("E5:1 A5:1 C#6:1"), bar("E6:2! C#6:1"), bar("B5:2 G5:1"), bar("E5:3")]
CHORUS2_MEL = list(CHORUS_MEL)
CHORUS2_MEL[3] = bar("D5:1 F#5:1 A5:1")
CHORUS2_MEL[11] = bar("F#5:1 A5:1 D6:1")
CHORUS2_MEL[9] = bar("A5:1 D6:2")
CHORUS3_MEL = list(CHORUS_MEL)
CHORUS3_MEL[15] = bar("E5:3!")
CHORUS3_MEL[5] = bar("C#6:1 E6:1 C#6:1")
CHORUS3_MEL[6] = bar("D6:2 B5:1")
CHORUS3_MEL[8] = bar("D5:1 G5:1 B5:1")
PRAYER_MEL = [bar("E5:3"), bar("D5:2 B4:1"), bar("C5:3"), bar("B4:2 G4:1"), bar("G4:1 C5:1 E5:1"), bar("F#5:2 D5:1"), bar("E5:2 F#5:1"), bar("D#5:3")]
PRAYER_BASS = [bar("C2:2 E2:1"), bar("B1:2 D2:1"), bar("A1:2 C2:1"), bar("E2:2 G2:1"), bar("C2:2 G2:1"), bar("D2:2 A2:1"), bar("B1:2 E2:1"), bar("B1:2 D#2:1")]

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm8", "pipe", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
PIPE_SNARE = ["o.o.xoo.X.o.", "xox.o.x.XxX."]    # パイプバンドのスネア

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)

    rf = R3
    if name in ("verse", "verse2") and i % 8 < 4 and base_ch in RIFF:
        rf = RIFF[base_ch][i % 2]
    elif name == "outro":
        rf = RIFF["Em" if base_ch == "Em" else "D"][i % 2] if not last else bar("E2:3!")
    P["riff"].append(rf)

    s = si = R3
    if name in ("verse", "verse2") and i % 8 >= 4:
        s = bar(f"{groot}:3") if not last else bar(f"{groot}:2! R:1")
    elif name in ("pre", "pre2"):
        s = bar(f"{groot}:3!") if i % 2 == 0 else bar(f"{groot}:2 {groot}:1")
        if last: s = bar(f"{groot}:2! R:1")
    elif name.startswith("chorus"):
        s = bar(f"{groot}:2! {groot}:1") if i % 2 == 0 else bar(f"{groot}:1 {groot}:2!")     # ヘミオラに合わせた伸ばし
        if last and name != "chorus3": s = bar(f"{groot}:2! R:1")
        si = s
    elif name == "lament":
        s = bar(f"{groot}:3") if i >= 4 else R3
    elif name == "outro" and last:
        s = si = bar("E2:3!")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm8 = pipe = R3
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = shift_oct(strip_marks(VERSE_MEL[8 + i]), 1) if i < 6 else VERSE_MEL[8 + i]
    elif name in ("pre", "pre2"): lead = PRE_MEL[i if name == "pre" else 4 + i]
    elif name == "chorus": lead = CHORUS_MEL[i]
    elif name == "chorus2": lead = CHORUS2_MEL[i]; harm8 = shift_oct(strip_marks(lead), -1)
    elif name == "chorus3":
        lead = CHORUS3_MEL[i]
        pipe = shift_oct(strip_marks(lead), -1)          # 見せ場: バグパイプが旋律を一緒に吹く
    elif name == "prayer": lead = PRAYER_MEL[i]
    elif name == "intro": pipe = PIPE_MARCH[i]
    elif name == "lament": pipe = PIPE_LAMENT[i]
    elif name == "outro": pipe = [PIPE_MARCH[4], PIPE_MARCH[2], PIPE_MARCH[5]][i] if not last else bar("E4:3")
    P["lead"].append(lead); P["harm8"].append(harm8); P["pipe"].append(pipe)

    if name in ("verse", "verse2") and i % 8 < 4 and base_ch in RIFF: b = unison_low(P["riff"][-1], -1, "B0")
    elif name in ("verse", "verse2", "pre", "pre2"):
        b = bar(f"{root}:1! {root}:1 {fifth_of(base_ch)}:1") if not last else bar(f"{root}:2! R:1")
    elif name.startswith("chorus"):
        b = bar(f"{root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5! {root}:0.5 {root}:0.5") if i % 2 == 0 else bar(f"{root}:0.5 {root}:0.5! {root}:0.5 {root}:0.5 {root}:0.5! {approach_note(ch, nxt)}:0.5")
        if last and name != "chorus3": b = bar(f"{root}:2! R:1")
    elif name == "lament": b = bar(f"{root}:3") if i >= 2 else R3
    elif name == "prayer": b = PRAYER_BASS[i]
    elif name == "intro": b = bar("E1:3") if i >= 4 else R3
    elif name == "outro": b = unison_low(P["riff"][-1], -1, "B0") if not last else bar("E1:3!")
    else: b = R3
    P["bass"].append(b)

    k = s = h = None; tom = cym = None
    if name == "intro":
        # パイプバンドの行進: スネアと大太鼓だけ
        s = PIPE_SNARE[i % 2]; k = "X.....X....." if i >= 2 else "X..........."
        if last: s = "xoxoxoxXXXXX"
    elif name in ("verse", "verse2"):
        # 重い3拍子: キックは1拍目、スネアは3拍目、2拍目はゴースト
        k = "X.....x....." if i % 2 == 0 else "X...x......."
        s = "....o...X..."
        h = "x.x.x.x.x.x." if name == "verse" else None
        if name == "verse2": cym = f"{RIDE}:1! {BELL}:1 {RIDE}:1"
        if i % 8 == 0: cym = f"{CR2}:1! " + ("R:2" if name == "verse" else f"{BELL}:1 {RIDE}:1"); h = h and "..x." + h[4:]
        if last: tom = "R:1 " + tom_triplets_down(2); k = "X..........."; s = "............"; h = None; cym = None
    elif name in ("pre", "pre2"):
        k = "X...X...X..." if i % 2 == 0 else "X.X.X.X.X.X."
        s = "....X...X..." if i < 6 else "xxxxxxxxXXXX"
        if i == 0: cym = f"{CR2}:3!"
        if last: s = "xoxoxoxXXXXX"; k = "X...X......."; cym = f"{CHINA}:1! R:2"
    elif name.startswith("chorus"):
        # ヘミオラ: 2拍ずつのかたまり（2小節で3つ）。キックとクラッシュ／チャイナが2拍ごと
        if i % 2 == 0:
            k = "X.x.....X.x."; s = "....X......."; cym = f"{CR if i % 4 == 0 else CHINA}:2! {RIDE}:1!"
        else:
            k = "....X.x....."; s = "X.......X..."; cym = f"{RIDE}:1 {CHINA}:2!"
        if name == "chorus3" and i >= 8: k = "XxXxXxXxXxXx"; s = "....X.......".replace("X", "X")
        if last and name != "chorus3": k = "X..........."; s = "....xoxoXXXX"; cym = f"{CR}:1! R:2"
        if name == "chorus3" and last: k = "X..........."; s = "X..........."; cym = f"{CR}:3!"
    elif name == "lament":
        s = PIPE_SNARE[i % 2] if i >= 4 else None
        k = "X..........." if i >= 2 else None
        if i == 0: cym = f"{CR2}:3"
    elif name == "prayer":
        # 祈り: ヘミオラをフロアタムとライドで小さく
        tom = "A2:2, A2:1," if i % 2 == 0 else "R:1 A2:2,"
        cym = f"{RIDE}:1, {RIDE}:1, {RIDE}:1,"
        if last: tom = "R:1 " + tom_16_down(2); cym = None
    elif name == "outro":
        k = "X.....x....." ; s = "....o...X..." if not last else None
        if last: k = "X..........."; s = "X..........."; cym = f"{CR}:3!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("chorus", "chorus2", "chorus3"): FX.append(bar("R:1 C4:2"))
    elif name == "intro" and i == 0: FX.append(bar("E4:3"))
    elif name == "prayer" and i == 5: FX.append(bar("E4:3"))
    else: FX.append(R3)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm8"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))
song.add(part("バグパイプ", "bagpipe", J("pipe"), volume=0.13, pan=-0.12, reverb=0.45, attack=0.03, release=0.4,
              fx=[{"type": "eq", "low": -2, "mid": -1.5, "midHz": 2500, "high": -1}, {"type": "reverb", "mix": 0.25}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "glossy-jrock"
add_layer(song, "choir", "戦場のバグパイプに、祈りの声が加わる。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-18-inori.json"
    song.write(out)
    check_clash(song)
