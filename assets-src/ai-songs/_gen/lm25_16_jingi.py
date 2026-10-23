# ラウド26曲 16「喪服と雨」（仮。もとの仮題「仁義の雨」）。2026-10-24 素材から作り直し
# スタイル: 7拍子のグルーヴのあるメタルコア（8分の 3+3+2+3+3 ＝タンゴの刻みを、低い弦の刻みで）＋アコーディオン。G♯ 和声的短音階・116・7/4
# 物語: 雨の中の決闘。二人の男が向かい合い、長いにらみ合い、銃に手をかける一瞬、短い決闘、一発の銃声のあとの無音、アコーディオンの弔い、葬列。
# 形: 決闘の儀式（ほとんどが抑えた緊張。爆発は決闘の一度だけ、短く）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   雨（0）: アコーディオンの嘆きだけ
#   向かい合う（1）: ベースと、低い弦のタンゴの刻み（短く切る）、アコーディオンの切った和音。リードは鋭い短い音
#   にらみ合い（1→2）: 刻みが伸びる音に変わり、リードは長い嘆きの音（息つぎを置く）
#   手をかける（2）: 全員の決め
#   決闘（3）: この曲で一度だけの爆発。短い
#   銃声: 一撃と、1小節の無音
#   弔い（0→1）: アコーディオンの独奏とクリーンのギター
#   葬列（2）: 重いハーフタイムで、抑えて
# 旋律の性格: タンゴの 3+3+2（鋭く切る短い音）と、長い嘆き。2026-10-23 人間「16、サビでドラムのガチャガチャした感じを抑えよう」「ハイハットは繊細に強弱」は引き継ぐ
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 116, 7
bar = Bars(BEATS)
R7 = bar.rest()

FORM = [("rain", 6), ("face", 16), ("stare", 12), ("draw", 4), ("duel", 8), ("shot", 1), ("mourn", 16), ("burial", 8)]
FACE = ["G#m", "G#m", "C#m", "D#7", "G#m", "E", "C#m", "D#7"]
CH = {"rain": ["G#m", "C#m", "D#7", "G#m", "E", "D#7"], "face": FACE * 2, "stare": ["G#m", "A", "G#m", "A", "E", "D#7"] * 2,
      "draw": ["D#7"] * 4, "duel": ["G#5", "A5", "G#5", "A5", "G#5", "A5", "D#5", "G#5"], "shot": ["G#m"],
      "mourn": ["G#m", "C#m", "F#", "B", "E", "C#m", "D#7", "G#m"] * 2, "burial": ["G#m", "E", "C#m", "D#7", "G#m", "E", "D#7", "G#m"]}
song = Song("仁義の雨（仮）",
            "仮: ラウド26曲の16曲目（2026-10-24 素材から作り直し）。7拍子のメタルコア（タンゴの 3+3+2 の刻み）＋アコーディオン。G♯ 和声的短音階・116・7/4。"
            "雨・向かい合う・にらみ合い・手をかける・短い決闘・銃声の無音・弔い・葬列。爆発は決闘の一度だけ。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 雨の中の決闘。長いにらみ合い、短い決闘、一発の銃声のあとの無音、アコーディオンの弔い、葬列。"
song.kinds = {"rain": "intro", "face": "verse", "stare": "pre", "draw": "break", "duel": "chorus", "shot": "break", "mourn": "bridge", "burial": "outro"}
SECS, NB = song.secs, song.nb

LOW = {"G#m": "G#1", "C#m": "C#2", "D#7": "D#2", "E": "E2", "A": "A1", "F#": "F#1", "B": "B1", "G#5": "G#1", "A5": "A1", "D#5": "D#2"}


def tango(ch, cut=True):
    """8分の 3+3+2+3+3（1.5・1.5・1・1.5・1.5拍）の頭を、低い弦で。cut＝短く切る／伸ばす"""
    g = LOW[ch]; o = up(g, 1)
    if cut: return bar(f"{g}:0.25! R:1.25 {g}:0.25! R:1.25 {o}:0.25! {g}:0.25 R:0.5 {g}:0.25! R:1.25 {tr(g, 7)}:0.25! R:1.25")
    return bar(f"{g}:1.5! {g}:1.5 {o}:1 {g}:1.5! {tr(g, 7)}:1.5")


VOICE = {"G#m": ["B3", "D#4", "G#4"], "C#m": ["C#4", "E4", "G#4"], "D#7": ["C#4", "D#4", "G4"], "E": ["B3", "E4", "G#4"], "A": ["C#4", "E4", "A4"],
         "F#": ["C#4", "F#4", "A#4"], "B": ["B3", "D#4", "F#4"]}
# リード: 向かい合う＝鋭い短い音（タンゴの区切りの頭）、にらみ合い＝長い嘆き
FACE_MEL = [bar("D#5:0.25! R:1.25 D#5:0.25! R:1.25 E5:0.5 D#5:0.5 R:3"), bar("R:3 B4:0.25! R:1.25 C#5:0.25 D#5:0.25 R:2"),
            bar("E5:0.25! R:1.25 E5:0.25! R:1.25 G#5:0.5 E5:0.5 R:3"), bar("R:3 G4:0.25! R:1.25 A#4:0.25 C#5:0.25 R:2"),
            bar("D#5:0.25! R:1.25 B4:0.25! R:1.25 G#4:0.5 B4:0.5 R:3"), bar("R:3 E5:0.25! R:1.25 D#5:0.25 B4:0.25 R:2"),
            bar("C#5:0.25! R:1.25 E5:0.25! R:1.25 G#5:0.5 F#5:0.5 R:3"), bar("R:3 F#5:0.25! R:1.25 D#5:0.25 C5:0.25 R:2")]
STARE_MEL = [bar("D#5:3 R:0.5 C#5:0.5 B4:1.5 R:1.5"), bar("C#5:2.5 R:1 E5:1.5 R:2"), bar("B4:3 R:0.5 G#4:0.5 B4:1.5 R:1.5"),
             bar("A4:2.5 R:1 C#5:1.5 R:2"), bar("G#4:1.5 B4:1.5 E5:2.5 R:1.5"), bar("D#5:3 R:4"),
             bar("R:1 G#4:0.5 B4:0.5 D#5:3 R:2"), bar("R:1 A4:0.5 C#5:0.5 E5:3 R:2"), bar("R:1 B4:0.5 D#5:0.5 F#5:3 R:2"),
             bar("R:1 C#5:0.5 E5:0.5 A5:2 R:3"), bar("G#5:1.5 E5:1.5 B4:2 R:2"), bar("A#4:2 G4:2 R:3")]
# アコーディオンの嘆き（雨・弔い）
LAMENT = [bar("R:1.5 D#5:1.5 E5:1 D#5:1.5 B4:1.5"), bar("C#5:3 R:0.5 B4:0.5 E5:1.5 R:1.5"), bar("A#4:1.5 C5:1.5 D#5:1 G4:3"),
          bar("G#4:3 R:4"), bar("R:1.5 B4:1.5 E5:1 G#5:1.5 F#5:1.5"), bar("D#5:3 C5:1 A#4:3")]
MOURN = [bar(x) for x in melody_walk(scale_pcs("G#", "harmonic"), "B4", "G#4", [[-1.5, 1.5, 1, 1.5, 1.5], [3, -0.5, 0.5, 1.5, -1.5], [1.5, 1.5, 1, 3], [2.5, -1, 1.5, -2]], 1,
                                     CH["mourn"], contour=(1, -1, -1, 2, -2, 1), lo="F4", hi="E5", beats=7)]

# 葬列の歌（嘆きを和音に合わせて。息つぎを置く）
BURIAL_MEL = [bar(x) for x in melody_walk(scale_pcs("G#", "harmonic"), "D#5", "G#4", [[3, -0.5, 0.5, 1.5, -1.5], [-1, 0.5, 0.5, 3, -2], [1.5, 1.5, 2.5, -1.5]], 2,
                                          CH["burial"], contour=(-1, -1, 2, -1), lo="F4", hi="E5", beats=7)]

P = {k: [] for k in ["riff", "rhy", "lead", "clean", "amel", "a0", "a1", "a2", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = amel = R7; acc = [R7] * 3
    root = root_note(ch); v = VOICE.get(ch, VOICE["G#m"])
    if name == "rain":
        amel = LAMENT[i]; b = R7
    elif name == "face":
        riff = tango(ch, True); lead = FACE_MEL[i % 8] if i >= 4 else R7
        acc = [bar(f"{x}:0.25! R:1.25 {x}:0.25 R:1.25 {x}:0.25 R:0.75 {x}:0.25 R:1.25 {x}:0.25 R:1.25") for x in v]
        b = bar(f"{root}:1.5 {root}:1.5 {up(root, 1) if False else fifth_of(ch)}:1 {root}:1.5 {fifth_of(ch)}:1.5")
    elif name == "stare":
        riff = rhy = tango(ch, False); lead = STARE_MEL[i]
        acc = [bar(f"{x}:7,") for x in v] if i % 2 == 0 else [R7] * 3
        b = bar(f"{root}:3.5 {root}:3.5")
    elif name == "draw":
        g = LOW[ch]
        riff = rhy = bar(f"{g}:0.5! R:1 {g}:0.5! R:1 {g}:0.5! R:3.5") if i < 3 else bar(f"{g}:0.25! {g}:0.25! {g}:0.25! {g}:0.25! R:6")
        b = unison_low(riff, -1, "B0")
    elif name == "duel":
        g = LOW[ch]
        riff = rhy = bar(" ".join(f"{g}:0.25{'!' if j in (0, 6, 12, 16, 22) else ''}" for j in range(28)))
        DUEL = ["D#5:0.25 E5:0.25 G#5:0.25 E5:0.25 " * 3 + "D#5:0.5 R:3.5", "R:3 B4:0.25 D#5:0.25 F#5:0.5! D#5:0.25 B4:0.25 G#4:0.5 R:2",
                "E5:0.5! D#5:0.25 C5:0.25 R:0.5 A4:0.5 C5:0.25 D#5:0.25 R:4.5", "R:1.5 G#4:0.25 B4:0.25 D#5:0.25 G#5:0.25 R:0.5 G#5:0.5! R:3.5"]
        lead = bar(DUEL[i % 4])
        b = unison_low(riff, -1, "B0")
    elif name == "shot":
        riff = rhy = R7; b = R7                                     # 銃声のあとの無音（一撃はドラムだけ）
    elif name == "mourn":
        amel = MOURN[i]
        tones = (chord_tones(ch, "G#3", "G#4") * 2)[:4]
        clean = bar(" ".join(f"{t}:1.5" if j % 2 == 0 else f"{t}:1" for j, t in enumerate(tones[:3])) + f" {tones[3]}:3") if i >= 4 else R7
        b = bar(f"{root}:7,") if i >= 8 else R7
    else:   # burial
        g = LOW[ch]
        riff = rhy = bar(f"{g}:3! {tr(g, 7)}:2 {g}:2") if i < n - 1 else bar(f"{g}:7!")
        lead = BURIAL_MEL[i] if i < n - 1 else R7
        amel = strip_marks(shift_oct(BURIAL_MEL[i], 0)) if 4 <= i < n - 1 else R7
        b = unison_low(riff, -1, "B0")
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["amel"].append(amel)
    for j in range(3): P[f"a{j}"].append(acc[j])
    P["bass"].append(b)
    if name == "shot": kit.add("X" + "." * 27, "X" + "." * 27, "." * 28, None, "C2:0.5! R:6.5")
    else: kit.add("X" + "." * 11 + "X" + "." * 15, "." * 6 + "X" + "." * 13 + "X" + "." * 7, "".join("x" if j % 2 == 0 else "." for j in range(28)))

J = lambda k: " ".join(P[k])
ACC = dict(reverb=0.35, attack=0.03, release=0.4, fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 1500, "high": 0}, {"type": "plate", "mix": 0.18}])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの和音（弔い）"))
song.add([part(f"アコーディオン（和音{j + 1}）", "accordion", J(f"a{j}"), volume=0.07, pan=-0.2, **ACC) for j in range(3)])
song.add(part("アコーディオン（旋律）", "accordion", J("amel"), volume=0.14, pan=-0.15, phrase=8, **ACC))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "deep-scoop-djent"

from lm25_plans import apply_plan
apply_plan(song, "16")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-16-jingi.json"
    song.write(out)
    check_clash(song)
