# ラウド26曲 17「Q.E.D. (Fallen)」（仮。もとの仮題「堕天の証明」）。2026-10-24 素材から作り直し
# スタイル: プログレッシブメタル（2つの主題を別々に示し、戦わせ、最後に同時に重ねる対位法）＋合唱。F♯ 短調（悪魔）↔ F♯ 長調（天使）・120・4/4
# 物語: 「天使は堕ちる」ことの証明。天使の空から始まり、悪魔の主題（命題1）、天使の主題（命題2）、二つの戦い（スウィープ）、天使の墜落。
#       証明の終わり（Q.E.D.）で、悪魔の主題が長調に変わって、天使の主題と同時に鳴る。二つは一つだった。ピタッと止める。
# 形: 証明（主題A・主題B・展開・墜落・AとBを同時に重ねる）。13（言い合いの間が縮む）とは違い、ここは2つの旋律を最後に同時に鳴らす。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   前奏（0→1）: 合唱だけ → 低い音と薄いドラム → リフが入って空間がいっぱいに（2026-10-23 人間「ピロピロやめて空間がだんだん広がるように」）
#   悪魔（2）: 重いハーフタイム。悪魔の主題は低く、短く刻む半音
#   天使（1→2）: 長調。合唱と、高く広く跳ぶ天使の主題
#   戦い（3）: 悪魔の主題がスウィープに砕ける（2026-10-23 人間「17のギターの速弾きをスイープなどに」）。倍の速さの感じ
#   墜落（0→1）: 天使の主題が下りながら遅くなる（合唱だけ）
#   証明終わり（3）: 悪魔の主題（長調に変わる）と天使の主題が同時に。最後はピタッと止める
# 旋律の性格: 悪魔＝低い16分の半音の刻み。天使＝高く跳ぶ長い音と息つぎ。最後に同時
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 120, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 12), ("devil", 24), ("angel", 24), ("war", 24), ("fall", 12), ("qed", 32)]
DEV = ["F#m", "F#m", "D", "C#7"]
ANG = ["F#", "D#m", "B", "C#"]
CH = {"intro": ["F#"] * 4 + ["F#", "D#m", "B", "C#"] + ["F#m"] * 4, "devil": DEV * 6, "angel": ANG * 6,
      "war": ["F#m", "G", "F#m", "C#7"] * 6, "fall": ["F#", "D#m", "B", "C#", "B", "A#m", "G#m", "C#"] + ["F#"] * 4, "qed": ANG * 8}
song = Song("堕天の証明（仮）",
            "仮: ラウド26曲の17曲目（2026-10-24 素材から作り直し）。プログレッシブメタル＋合唱。F♯ 短調（悪魔）と F♯ 長調（天使）・120。"
            "悪魔の主題と天使の主題を別々に示し、スウィープの戦い、天使の墜落、最後に悪魔の主題が長調に変わって天使の主題と同時に鳴る（対位法）。ピタッと止める。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 天使は堕ちることの証明。二つの主題が戦い、天使が落ち、最後に二つが同時に鳴って一つだったとわかる。"
song.kinds = {"intro": "intro", "devil": "verse", "angel": "chorus", "war": "solo", "fall": "bridge", "qed": "chorus"}
SECS, NB = song.secs, song.nb

# 悪魔の主題（2小節。低い16分の半音の刻み）と、天使の主題（4小節。高く跳ぶ）
DEVIL = ["F#3:0.25! G3:0.25 F#3:0.25 R:0.25 C#4:0.25! C4:0.25 R:0.5 F#3:0.25 A3:0.25 G#3:0.25 G3:0.25 F#3:0.5! R:0.5",
         "R:0.5 A3:0.25 B3:0.25 C4:0.5! B3:0.25 A3:0.25 G#3:0.5 R:0.5 F#3:0.5! R:0.5"]
DEVIL_D = ["D3:0.25! D#3:0.25 D3:0.25 R:0.25 A3:0.25! G#3:0.25 R:0.5 D3:0.25 F#3:0.25 E3:0.25 D#3:0.25 D3:0.5! R:0.5",
           "R:0.5 G#3:0.25 A3:0.25 B3:0.5! A3:0.25 G#3:0.25 F3:0.5 R:0.5 C#3:0.5! R:0.5"]
ANGEL = ["C#5:1.5 R:0.5 F#4:0.5 A#4:0.5 C#5:0.5 F#5:0.5", "D#5:1 C#5:0.5 A#4:0.5 R:1 F#4:1",
         "D#5:1.5 R:0.5 B4:0.5 D#5:0.5 F#5:0.5 D#5:0.5", "C#5:1 F5:0.5 G#5:0.5 R:2"]
# 長調に変わった悪魔の主題（Q.E.D.）: 半音を全音に、短3度を長3度に
DEVIL_MAJ = ["F#3:0.25! G#3:0.25 F#3:0.25 R:0.25 C#4:0.25! B3:0.25 R:0.5 F#3:0.25 A#3:0.25 G#3:0.25 F#3:0.25 F#3:0.5! R:0.5",
             "R:0.5 A#3:0.25 B3:0.25 C#4:0.5! B3:0.25 A#3:0.25 G#3:0.5 R:0.5 F#3:0.5! R:0.5"]
# 戦い: 悪魔の主題を1オクターブ上で、ずらしたり縮めたりする（同じ形を続けない）
WAR_LEAD = [shift_oct(DEVIL[0], 1), shift_oct(DEVIL[1], 1),
            "R:0.5 F#4:0.25! G4:0.25 F#4:0.25 R:0.25 C#5:0.5! C5:0.25 B4:0.25 A4:0.5 G#4:0.25 G4:0.25 F#4:0.5",
            "C#5:0.25! C5:0.25 B4:0.25 A#4:0.25 A4:0.5! G#4:0.5 R:0.5 F#4:0.25 G4:0.25 A4:0.5 F#4:0.5!"]
# 墜落: 天使の主題が下りて、長くなる
FALL = ["C#5:1.5 A#4:2.5", "F#4:2 R:0.5 D#4:1.5", "D#5:3 B4:1", "G#4:2.5 C#4:1.5", "B4:3.5 R:0.5", "A#4:1 R:1 A#4:2", "G#4:4", "R:1 F4:3", "F#4:2.5 R:1.5", "C#4:3 R:1", "F#3:2 R:2", "R:4"]

P = {k: [] for k in ["riff", "rhy", "lead", "tech", "q0", "q1", "q2", "bass"]}
kit = Kit(BEATS)
QV = {"F#": ["F#4", "A#4", "C#5"], "D#m": ["F#4", "A#4", "D#5"], "B": ["F#4", "B4", "D#5"], "C#": ["F4", "G#4", "C#5"], "F#m": ["F#4", "A4", "C#5"],
      "A#m": ["F4", "A#4", "C#5"], "G#m": ["D#4", "G#4", "B4"], "D": ["F#4", "A4", "D5"], "C#7": ["F4", "G#4", "B4"], "G": ["G4", "B4", "D5"]}
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = tech = R4; q = [R4] * 3
    root = root_note(ch); v = QV.get(ch, QV["F#"])
    if name == "intro":
        q = [bar(f"{x}:4") for x in v]
        if i >= 4: b = bar(f"{root}:4,")
        else: b = R4
        if i >= 8: riff = rhy = bar(f"{root_note(ch, 'F#1', 'F2')}:2! {root_note(ch, 'F#1', 'F2')}:1 {tr(root_note(ch, 'F#1', 'F2'), 7)}:1")
    elif name == "devil":
        dv = DEVIL if ch in ("F#m", "C#7") else DEVIL_D
        riff = rhy = bar(shift_oct(dv[i % 2], -1)) if ch != "C#7" else bar("C#2:1! R:0.5 C#2:0.5 G#2:1! C2:1")
        lead = bar(dv[i % 2]) if i >= 8 else R4
        b = unison_low(riff, -1, "B0")
    elif name == "angel":
        q = [bar(f"{x}:4") for x in v] if i % 2 == 0 else [bar(f"{x}:2 R:2") for x in v]
        lead = bar(ANGEL[i % 4]) if i >= 4 else R4
        g = root_note(ch, "F#1", "F2")
        riff = rhy = bar(f"{g}:2! {tr(g, 7)}:2") if i >= 8 else R4
        b = bar(f"{root}:2 {fifth_of(ch)}:2")
    elif name == "war":
        g = root_note(ch, "F#1", "F2")
        riff = rhy = bar(" ".join(f"{g}:0.25{'!' if j % 4 == 0 else ''}" for j in range(16)))
        if i % 4 in (1, 3): tech = bar(sweep(ch.replace("7", ""), "F#3", "F#5", 4, 1 / 6))
        else: lead = bar(WAR_LEAD[(i // 2) % 4])
        b = unison_low(riff, -1, "B0")
    elif name == "fall":
        lead = bar(FALL[i]); q = [bar(f"{x}:4,") for x in v] if i < 10 else [R4] * 3
        b = bar(f"{root}:4,") if i < 8 else R4
    else:   # qed
        lead = bar(ANGEL[i % 4])
        riff = rhy = bar(shift_oct(DEVIL_MAJ[i % 2], -1)) if i < n - 1 else bar("F#2:0.5! R:3.5")
        if i == n - 1: lead = bar("F#5:0.5! R:3.5")
        q = [bar(f"{x}:4") for x in v] if i >= 8 and i < n - 1 else ([bar(f"{x}:0.5! R:3.5") for x in v] if i == n - 1 else [R4] * 3)
        b = unison_low(riff, -1, "B0")
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["tech"].append(tech)
    for j in range(3): P[f"q{j}"].append(q[j])
    P["bass"].append(b)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(tech_part(J("tech"), role="スウィープのギター（戦い）", vol=0.11, pan=0.05))
song.add([part(f"合唱（{['上', '中', '下'][j]}）", "choir", J(f"q{j}"), volume=0.07, pan=[-0.3, 0.3, 0][j], reverb=0.55, attack=0.25, release=0.9,
               fx=[{"type": "eq", "low": -4, "mid": -1, "midHz": 700, "high": 0}, {"type": "reverb", "mix": 0.3}]) for j in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [12 + 24 + 24 + 23]        # 戦いの最後（天使が落ちる瞬間）に一度だけ
song.ref_tone = "wide-dark-wall"

from lm25_plans import apply_plan
apply_plan(song, "17")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-17-daten.json"
    song.write(out)
    check_clash(song)
