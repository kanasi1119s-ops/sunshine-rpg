# ラウド26曲 02「PALE ORBIT」（仮。もとの仮題「白い螺旋」）。2026-10-24 素材から作り直し
# スタイル: ジェント（7拍子 2+2+3 の上で、16分3+3+2 の低い刻みがずれていく）＋シタール。F♯ フリジアン・128・7/4
# 物語: 抜け出せないめまい。同じ景色（16小節）を、半音ずつ高い所で4周する。3周目で意識が飛ぶ（全部消える）。
# 形: 螺旋（サビという区切りがない。同じ骨組みの16小節が、半音ずつ上がって4周）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   前奏（0）: シタールの螺旋の動機だけ
#   1周目 F♯（1）: 刻みは弱く短く、シタールが主役。リードはまだ出ない（めまいの入り口）
#   2周目 G（2）: リードが同じ音のくり返しと半音の落下で歌う。バンド全員だが、まだ抑えている
#   3周目 A♭: はじめの4小節は意識が飛ぶ（0。低い脈とキックの心拍だけ）→ 残り12小節で少しずつ戻る（1→2）
#   4周目 A（3）: この曲で一度だけの全開。リードとシタールが同じ旋律、最後の4小節はタッピングが螺旋を描く
#   終わり（1）: ドラムとシタールだけが残り、フェードアウト
# 旋律の性格: 同じ音のくり返し（めまい）と、半音で落ちる短い動機。2+2+3 の拍の区切りに沿って句を置く（長く伸ばさない）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 128, 7
bar = Bars(BEATS)
R7 = bar.rest()

LAP = ["F#m", "F#m", "G", "F#m", "F#m", "F#m", "Em", "G", "D", "D", "Em", "F#m", "D", "Em", "G", "F#m"]
FORM = [("intro", 4), ("lap1", 16), ("lap2", 16), ("lap3", 16), ("lap4", 16), ("outro", 8)]
CH = {"intro": ["F#m"] * 4, "lap1": LAP, "lap2": LAP, "lap3": LAP, "lap4": LAP, "outro": ["F#m", "F#m", "G", "F#m", "F#m", "G", "F#m", "F#m"]}
song = Song("白い螺旋（仮）",
            "仮: ラウド26曲の2曲目（2026-10-24 素材から作り直し）。ジェント・F♯ フリジアン・128・7/4（2+2+3）。同じ16小節を半音ずつ上げて4周する螺旋。"
            "3周目で全部消え、4周目で全開。旋律は同じ音のくり返しと半音の落下。別の楽器はシタール。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 抜け出せないめまい。同じ景色を半音ずつ高い所で4周し、3周目で意識が飛び、4周目で螺旋の頂上へ。"
song.kinds = {"intro": "intro", "lap1": "verse", "lap2": "chorus", "lap3": "bridge", "lap4": "chorus", "outro": "outro"}
SECS, NB = song.secs, song.nb

LOW = {"F#m": ("F#1", "G1", "C#2", "B1"), "G": ("G1", "A1", "D2", "C2"), "Em": ("E2", "F#2", "B2", "A2"), "D": ("D2", "E2", "A2", "G2")}


def djent(ch, var=0):
    """16分 3+3+2 の刻み（2+2+3 の拍とずれていく）。var で最後のまとまりを変える"""
    r, n2, f5, f4 = LOW[ch]
    ends = [f"{f5}:0.5 {f4}:0.5 {r}:0.25 {r}:0.25 R:1", f"{r}:0.25 {r}:0.25 {n2}:0.5 R:0.5 {f5}:0.5! R:0.5", f"{r}:0.75! {r}:0.75 R:1"]
    return bar(f"{r}:0.75! {r}:0.75 {r}:0.5! {n2}:0.25 {r}:0.25 R:0.5 {r}:0.75! {r}:0.75 " + ends[var % 3])


def pulse(ch):
    """1周目: 刻みを短く弱く（頭と3つ目の拍だけ）"""
    r = LOW[ch][0]
    return bar(f"{r}:0.5, R:1.5 {r}:0.5, R:1.5 {r}:0.75, R:2.25")


# シタールの螺旋の動機（2+2+3）。和音ごとに最後の音を変える
SITAR = {"F#m": bar("F#4:0.25 G4:0.25 A4:0.5 G4:0.5 F#4:0.5 C#5:0.5 D5:0.5 C#5:0.5 A4:0.5 G4:0.5 F#4:0.5 E4:0.5 F#4:1.5"),
         "G": bar("G4:0.25 A4:0.25 B4:0.5 A4:0.5 G4:0.5 D5:0.5 E5:0.5 D5:0.5 B4:0.5 A4:0.5 G4:0.5 F#4:0.5 G4:1.5"),
         "Em": bar("E4:0.25 F#4:0.25 G4:0.5 F#4:0.5 E4:0.5 B4:0.5 C5:0.5 B4:0.5 G4:0.5 F#4:0.5 E4:0.5 D4:0.5 E4:1.5"),
         "D": bar("D4:0.25 E4:0.25 F#4:0.5 E4:0.5 D4:0.5 A4:0.5 B4:0.5 A4:0.5 F#4:0.5 E4:0.5 D4:0.5 C#4:0.5 D4:1.5")}

# 2周目の旋律: 同じ音のくり返し → 半音の落下（2+2+3 の区切りに沿う）
LAP2 = [
    bar("C#5:0.5 C#5:0.5 C#5:0.5 D5:0.5 C#5:1 R:1 A4:0.5 G4:0.5 F#4:1 R:1"),
    bar("R:1 C#5:0.5 C#5:0.5 C#5:0.5 C5:0.5 R:1 A4:0.5 A4:0.5 G#4:0.5 R:1.5"),
    bar("D5:0.5 D5:0.5 D5:0.5 E5:0.5 D5:1 R:1 B4:0.5 A4:0.5 G4:1 R:1"),
    bar("R:2 F#4:0.5 G4:0.5 A4:0.5 R:0.5 C#5:0.5 C5:0.5 B4:0.5 R:1.5"),
    bar("C#5:0.5 C#5:0.5 E5:0.5 C#5:0.5 R:0.5 C#5:0.5 C#5:0.5 C5:0.5 A4:1 R:2"),
    bar("R:1 F#4:0.5 A4:0.5 C#5:1 R:0.5 B4:0.5 A#4:0.5 A4:0.5 F#4:1 R:1"),
    bar("B4:0.5 B4:0.5 B4:0.5 C5:0.5 B4:1 R:1 G4:0.5 F#4:0.5 E4:1 R:1"),
    bar("R:1 D5:0.5 D5:0.5 B4:0.5 R:0.5 D5:0.5 C#5:0.5 C5:0.5 B4:0.5 R:2"),
    bar("A4:0.5 A4:0.5 A4:0.5 B4:0.5 A4:1 R:1 F#4:0.5 E4:0.5 D4:1 R:1"),
    bar("R:1 F#4:0.5 F#4:0.5 A4:0.5 R:0.5 D5:0.5 C#5:0.5 C5:0.5 A4:0.5 R:2"),
    bar("G4:0.5 G4:0.5 B4:0.5 B4:0.5 E5:1 R:1 D5:0.5 C#5:0.5 B4:1 R:1"),
    bar("R:2 C#5:0.5 C#5:0.5 C#5:0.5 C5:0.5 A4:1 R:2"),
    bar("F#4:0.5 A4:0.5 D5:0.5 F#4:0.5 R:0.5 A4:0.5 D5:0.5 C#5:0.5 A4:1 R:2"),
    bar("R:1 G4:0.5 B4:0.5 E5:0.5 R:0.5 E5:0.5 D#5:0.5 D5:0.5 B4:0.5 R:2"),
    bar("D5:0.5 D5:0.5 D5:0.5 C#5:0.5 B4:1 R:1 A4:0.5 G4:0.5 D5:1 R:1"),
    bar("C#5:0.5 C#5:0.5 C#5:0.5 C5:0.5 B4:0.5 A#4:0.5 A4:1.5 R:2.5"),
]
# 3周目の後半（戻ってくる）: 同じ動機を上下さかさまに、まばらに
LAP3 = [R7] * 8 + [
    bar("R:2 C#5:0.5 B4:0.5 A4:0.5 R:3.5"), bar("R:4 A4:0.5 A#4:0.5 B4:1 R:1"),
    bar("R:2 D5:0.5 C#5:0.5 B4:0.5 R:3.5"), bar("R:4 B4:0.5 C5:0.5 C#5:1 R:1"),
    bar("R:2 F#4:0.5 F#4:0.5 F#4:0.5 G4:0.5 A4:3"), bar("R:2 E4:0.5 E4:0.5 G4:0.5 B4:0.5 E5:3"),
    bar("D5:0.5 D5:0.5 D5:0.5 D#5:0.5 E5:1 R:1 G4:0.5 A4:0.5 B4:1 R:1"), bar("C#5:0.5 C#5:0.5 C#5:0.5 D5:0.5 C#5:1 R:4")]
# 4周目（頂上）: 2周目の動機を、跳躍で広げる
LAP4 = [
    bar("C#5:0.5 C#5:0.5 E5:0.5 C#5:0.5 C#5:1 R:1 A4:0.5 G4:0.5 F#4:1 R:1"),
    bar("R:1 C#5:0.5 E5:0.5 C#5:0.5 C5:0.5 R:1 A4:0.5 C5:0.5 B4:0.5 R:1.5"),
    bar("D5:0.5 D5:0.5 D5:0.5 E5:0.5 E5:1 R:1 D5:0.5 B4:0.5 G4:1 R:1"),
    bar("R:2 F#4:0.5 A4:0.5 C#5:0.5 R:0.5 E5:0.5 E5:0.5 C#5:0.5 R:1.5"),
    bar("C#5:0.5 E5:0.5 E5:0.5 E5:0.5 R:0.5 C#5:0.5 C#5:0.5 C5:0.5 A4:1 R:2"),
    bar("R:1 F#4:0.5 A4:0.5 C#5:1 R:0.5 E5:0.5 D#5:0.5 D5:0.5 C#5:1 R:1"),
    bar("B4:0.5 B4:0.5 E5:0.5 B4:0.5 G4:1 R:1 B4:0.5 A#4:0.5 A4:1 R:1"),
    bar("R:1 D5:0.5 B4:0.5 G4:0.5 R:0.5 D5:0.5 E5:0.5 E5:0.5 D5:0.5 R:2"),
    bar("A4:0.5 A4:0.5 D5:0.5 A4:0.5 F#4:1 R:1 A4:0.5 B4:0.5 D5:1 R:1"),
    bar("R:1 F#4:0.5 A4:0.5 D5:0.5 R:0.5 E5:0.5 E5:0.5 D5:0.5 A4:0.5 R:2"),
    bar("G4:0.5 B4:0.5 E5:0.5 B4:0.5 G4:1 R:1 E5:0.5 D#5:0.5 D5:1 R:1"),
    bar("R:2 C#5:0.5 E5:0.5 E5:0.5 F5:0.5 E5:1 R:2"),
] + [R7] * 4          # 最後の4小節はタッピングに渡す

TAP_TRI = {"D": ("D5", "F#5", "A5"), "Em": ("E5", "G5", "B5"), "G": ("D5", "G5", "B5"), "F#m": ("C#5", "F#5", "A5")}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "sitar", "tap", "bass", "mute"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]; last = i == n - 1
    riff = rhy = lead = sitar = tap_ = mute = R7
    r = LOW[ch][0]; root = root_note(ch)
    if name == "intro":
        sitar = SITAR[ch] if i % 2 == 0 else bar("R:4 " + " ".join(SITAR[ch].split()[-4:]))
        b = R7 if i < 2 else bar(f"{root}:7,")
    elif name == "lap1":
        riff = pulse(ch); sitar = SITAR[ch]
        b = bar(f"{root}:2, R:2 {root}:3,")
    elif name == "lap2":
        riff = rhy = djent(ch, i); lead = LAP2[i]; sitar = SITAR[ch] if i % 4 == 3 else R7
        b = unison_low(riff, -1, "B0")
        mute = bar("R:4 F#2:0.25, R:2.75") if i % 2 == 1 else R7
    elif name == "lap3":
        if i < 4:
            b = bar(f"{root}:7,")                                # 意識が飛ぶ: 低い脈だけ
        else:
            sitar = SITAR[ch] if i >= 4 else R7
            riff = pulse(ch) if i >= 8 else R7
            rhy = djent(ch, i) if i >= 12 else R7
            lead = LAP3[i]
            b = bar(f"{root}:2, R:2 {root}:3,") if i < 12 else unison_low(djent(ch, i), -1, "B0")
    elif name == "lap4":
        riff = rhy = djent(ch, i + 1); lead = LAP4[i]
        sitar = strip_marks(lead) if 4 <= i < 12 else (SITAR[ch] if i < 4 else R7)
        if i >= 12: tap_ = bar(tap(TAP_TRI[ch], 4, 0.25) + " " + tap(TAP_TRI[ch], 3, 1 / 6))
        b = unison_low(riff, -1, "B0")
    else:   # outro
        sitar = SITAR[ch] if i < 6 else (bar("F#4:7") if i == 6 else R7)
        b = bar(f"{root}:7,") if i < 6 else R7
    P["riff"].append(riff); P["rhy"].append(rhy); P["rhy_in"].append(rhy); P["lead"].append(lead); P["sitar"].append(sitar)
    P["tap"].append(tap_); P["bass"].append(b); P["mute"].append(mute)
    kit.add("X" + "." * 27, "." * 16 + "X" + "." * 11, "".join("x" if j % 4 == 0 else "." for j in range(28)))

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(tech_part(J("tap"), role="タッピングのギター（螺旋の頂上）", vol=0.11, pan=0.05))
song.add(part("シタール", "sitar", J("sitar"), volume=0.16, pan=-0.25, reverb=0.35, attack=0.005, release=0.8,
              fx=[{"type": "eq", "low": -3, "mid": 1.5, "midHz": 2000, "high": 1}, {"type": "delay", "beats": 0.75, "mix": 0.18, "feedback": 0.3}, {"type": "plate", "mix": 0.2}]))
song.add(bass_part(J("bass")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "dark-electro-rock"
song.dance_air = True

from lm25_plans import apply_plan
apply_plan(song, "02")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-02-rasen.json"
    song.write(out)
    check_clash(song)
