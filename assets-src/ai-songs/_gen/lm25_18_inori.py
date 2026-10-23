# ラウド26曲 18「Pray Louder」（仮。もとの仮題「祈りの音量」）。2026-10-24 素材から作り直し
# スタイル: フォークメタル（3拍子の行進・バグパイプ・重い刻み）。E ドリアン・90・3/4
# 物語: 霧の戦場に一人のバグパイプ吹き。行進が始まり、戦いになり、倒れた者の上に風だけが吹く。生き残った全員が、バグパイプの旋律を一緒に歌う。
# 形: 霧の独奏 → 行進 → 戦い → 倒れた者 → 全員の歌 → 風。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   霧（0）: バグパイプの独奏（ドローンの上で）
#   行進（2）: 3拍子の行進。強さは一定（行列は叫ばない）。スネアの行進
#   戦い（3）: 速い（倍の感じ）。リードが戦いの断片、バグパイプはドローン
#   倒れた者（0）: ドローンだけ
#   全員の歌（2）: 大きいが荒くない。バグパイプとリードが同じ旋律を、全員で
#   風（0）: ドローンが消える
# 旋律の性格: バグパイプの装飾音（すばやい前打音）のついた民謡風の旋律。跳ばずに音階で動く。3拍子の付点
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 90, 3
bar = Bars(BEATS)
R3 = bar.rest()

TUNE_CH = ["Em", "D", "Em", "A", "Em", "G", "D", "Em"]
FORM = [("mist", 8), ("march", 32), ("battle", 32), ("fallen", 8), ("hymn", 32), ("wind", 8)]
CH = {"mist": ["Em"] * 8, "march": TUNE_CH * 4, "battle": ["Em", "Em", "C", "D"] * 8, "fallen": ["Em"] * 8, "hymn": TUNE_CH * 4, "wind": ["Em"] * 8}
song = Song("祈りの音量（仮）",
            "仮: ラウド26曲の18曲目（2026-10-24 素材から作り直し）。フォークメタル＋バグパイプ。E ドリアン・90・3/4。霧の独奏、3拍子の行進、戦い、倒れた者、"
            "全員でバグパイプの旋律を歌う。旋律は装飾音のついた民謡風（跳ばずに音階で）。自作",
            BPM, BEATS, FORM, CH)
song.flags = "--space hall --space-wet 0.14"
song.desc += " 物語: 霧の戦場に一人のバグパイプ。行進、戦い、倒れた者の上の風、そして生き残った全員がバグパイプの旋律を歌う。"
song.kinds = {"mist": "intro", "march": "verse", "battle": "chorus", "fallen": "bridge", "hymn": "chorus", "wind": "outro"}
SECS, NB = song.secs, song.nb

# 行進の旋律（8小節。装飾音＝16分より短いすばやい前打音）
TUNE = ["B4:0.125 E5:0.875 D5:0.5 B4:0.5 A4:0.75 B4:0.25", "G4:0.125 A4:0.375 B4:0.5 D5:1.5 R:0.5",
        "E5:0.75 F#5:0.25 E5:0.5 D5:0.5 B4:1", "C#5:0.125 D5:0.375 C#5:0.5 A4:1 R:1",
        "B4:0.125 E5:0.875 G5:0.5 F#5:0.5 E5:0.5 D5:0.5", "B4:0.75 D5:0.25 B4:0.5 G4:0.5 A4:0.5 B4:0.5",
        "A4:0.125 D5:0.875 C#5:0.5 A4:0.5 F#4:1", "G4:0.5 E4:0.5 E4:0.125 F#4:0.375 E4:1.5"]
# 行進の旋律の変奏（同じ旋律を、リズムを変えて）
TUNE2 = ["E5:0.5 D5:0.25 B4:0.25 A4:0.5 B4:0.5 D5:1", "B4:0.125 D5:0.375 E5:0.5 F#5:1 E5:0.5 D5:0.5", "E5:1.5 D5:0.5 B4:0.5 A4:0.5",
         "A4:0.125 B4:0.375 A4:0.5 F#4:0.5 E4:0.5 R:1", "B4:0.125 E5:0.375 G5:0.5 E5:0.5 D5:1 R:0.5", "D5:1 B4:0.5 G4:0.5 B4:1",
         "A4:0.125 D5:0.375 F#5:0.5 E5:0.5 C#5:0.5 A4:1", "B4:0.5 G4:0.5 F#4:0.5 E4:1.5"]
# 霧の独奏（自由に。長短を混ぜる）
MIST = ["R:1 B4:0.125 E5:1.875", "D5:0.5 B4:0.5 A4:2", "R:0.5 G4:0.5 A4:0.5 B4:1.5", "D5:0.125 E5:1.375 D5:0.5 B4:1",
        "A4:2 R:1", "R:0.5 B4:0.125 D5:0.875 E5:1.5", "F#5:0.5 E5:0.5 D5:0.5 B4:1.5", "E5:2.5 R:0.5"]
# 戦い: リードの断片（短く鋭い）
FIGHT = ["E5:0.25 D5:0.25 B4:0.25 R:0.25 E5:0.25 G5:0.25 R:1.5", "R:1.5 D5:0.25 E5:0.25 F#5:0.5 D5:0.5",
         "G5:0.5 E5:0.25 C5:0.25 R:1 E4:0.25 G4:0.25 C5:0.5", "R:1 A4:0.25 D5:0.25 F#5:0.5 D5:0.5 A4:0.5"]
# 全員の歌: 行進の旋律を、全員で（2回目は 3度上の線をバグパイプに）
HYMN_TOP = ["G5:0.125 G5:0.875 F#5:0.5 D5:0.5 C#5:0.75 D5:0.25", "B4:0.125 C#5:0.375 D5:0.5 F#5:1.5 R:0.5",
            "G5:0.75 A5:0.25 G5:0.5 F#5:0.5 D5:1", "E5:0.125 F#5:0.375 E5:0.5 C#5:1 R:1",
            "D5:0.125 G5:0.875 A5:0.5 A5:0.5 G5:0.5 F#5:0.5", "D5:0.75 F#5:0.25 D5:0.5 B4:0.5 C#5:0.5 D5:0.5",
            "C#5:0.125 F#5:0.875 E5:0.5 C#5:0.5 A4:1", "B4:0.5 G4:0.5 G4:0.125 A4:0.375 G4:1.5"]

LOW = {"Em": "E2", "D": "D2", "A": "A1", "G": "G1", "C": "C2"}
P = {k: [] for k in ["riff", "rhy", "lead", "pipe", "drone", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = pipe = R3
    g = LOW[ch]; root = root_note(ch)
    drone = bar("E3:3") if name in ("mist", "fallen", "battle") or (name == "wind" and i < 6) else (bar("E3:3,") if name == "march" else R3)
    if name == "mist":
        pipe = bar(MIST[i]); b = R3
    elif name == "march":
        pipe = bar((TUNE2 if 16 <= i < 24 else TUNE)[i % 8]) if i >= 8 else R3
        riff = rhy = bar(f"{g}:1! {g}:0.5 {g}:0.5 {tr(g, 7)}:1") if i >= 4 else R3
        b = bar(f"{root}:1! {root}:1 {fifth_of(ch)}:1")
    elif name == "battle":
        riff = rhy = bar(" ".join(f"{g}:0.25{'!' if j % 3 == 0 else ''}" for j in range(12)))
        lead = bar(FIGHT[i % 4]) if i % 2 == 0 or i >= 16 else R3
        b = unison_low(riff, -1, "B0")
    elif name == "fallen":
        b = bar("E1:3,") if i < 6 else R3
    elif name == "hymn":
        pipe = bar(TUNE[i % 8]) if i < 16 else (bar(HYMN_TOP[i % 8]) if i < 24 else bar(TUNE2[i % 8]))
        lead = bar(strip_marks((TUNE2 if i >= 24 else TUNE)[i % 8])) if i >= 8 else R3
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 {tr(g, 7)}:1")
        b = bar(f"{root}:1.5 {root}:0.5 {fifth_of(ch)}:1")
    else:   # wind
        pipe = bar("E5:3,") if i == 0 else R3
        b = R3
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["pipe"].append(pipe); P["drone"].append(drone); P["bass"].append(b)
    if name == "march":    # 行進のスネア（3拍子。2拍目の裏にロールの粒、3拍目に強く）
        kit.add("X.......X..." if i % 2 == 0 else "X...........", "..o.X.ooX.o." if i % 4 != 3 else "..o.X.ooXoXo", "x...x...x...")
    else:
        kit.add("X" + "." * 11, "....X...X...", "x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("バグパイプ", "bagpipe", J("pipe"), volume=0.13, pan=-0.12, reverb=0.45, attack=0.03, release=0.4,
              fx=[{"type": "eq", "low": -2, "mid": -1.5, "midHz": 2500, "high": -1}, {"type": "reverb", "mix": 0.25}]))
song.add(part("バグパイプ（ドローン）", "bagpipe", J("drone"), volume=0.07, pan=0.12, reverb=0.45, attack=0.2, release=0.6,
              fx=[{"type": "eq", "low": -2, "mid": -2, "midHz": 2500, "high": -2}, {"type": "reverb", "mix": 0.25}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "glossy-jrock"

from lm25_plans import apply_plan
apply_plan(song, "18")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-18-inori.json"
    song.write(out)
    check_clash(song)
