# ラウド26曲 11「Crush Depth」（仮。もとの仮題「深海の時計」）。2026-10-24 素材から作り直し
# スタイル: スラッジ／ドローン（6拍子で波のように揺れる重さが、深くなるほど細り、押しつぶされる）＋琴。F 短調・86 → 48・6/4（3+3）
# 物語: 潜水艇が沈んでいく。海面・100m・300m・700m・1000m。琴の「時計」が、深さとともに遅く、まばらになる。限界深度で、圧壊。
# 形: 沈降（深さごとの5場面。下りるほど遅く・低く・音数が少なく・小さくなる）。最後に一撃だけ。
#      07（落ちるほど密に重く）とは逆で、ここは深くなるほど細く静かに押しつぶされる。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   海面（2）: 明るく揺れる。重い6拍子の揺れと琴の8分の時計
#   100m（2）: リードが長い音で漂う
#   300m（1）: 72。ドラムはハーフ、リフの一撃が減る
#   700m（1→0）: 60。ベースと琴とキックの鼓動だけ。リードは1小節に1〜2音
#   1000m（0）: 48。琴の時計がまばらに、低いうなりだけ
#   圧壊（3）: 一撃だけ。そのあと無音
# 旋律の性格: 伸ばす音だけ（息の長い音と、小節の途中の休み）。深くなるほど音が減り、低くなる
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 86, 6
bar = Bars(BEATS)
R6 = bar.rest()

FORM = [("surface", 8), ("d100", 12), ("d300", 12), ("d700", 10), ("d1000", 8), ("crush", 2)]
CH = {"surface": ["Fm", "Db", "Fm", "Eb", "Fm", "Db", "Bbm", "C"],
      "d100": ["Fm", "Db", "Ab", "Eb", "Fm", "Db", "Bbm", "C", "Fm", "Db", "Bbm", "C"],
      "d300": ["Fm", "Fm", "Db", "Db", "Bbm", "Bbm", "C", "C", "Fm", "Fm", "Db", "C"],
      "d700": ["Fm", "Fm", "Fm", "Db", "Db", "Fm", "Fm", "Bbm", "C", "C"],
      "d1000": ["Fm"] * 8, "crush": ["Fm", "Fm"]}
song = Song("深海の時計（仮）",
            "仮: ラウド26曲の11曲目（2026-10-24 素材から作り直し）。スラッジ／ドローン＋琴。F 短調・6/4（3+3）。海面・100m・300m・700m・1000m と沈み、"
            "86 から 48 へ遅く、低く、音数が少なくなり、最後に圧壊の一撃。旋律は伸ばす音だけで、深くなるほど減る。自作",
            BPM, BEATS, FORM, CH)
song.flags = "--space hall --space-wet 0.16"
song.desc += " 物語: 潜水艇が沈む。琴の時計が深さとともに遅く、まばらになり、限界深度で圧壊する。"
song.kinds = {"surface": "intro", "d100": "chorus", "d300": "verse", "d700": "bridge", "d1000": "outro", "crush": "break"}
SECS, NB = song.secs, song.nb

LOW = {"Fm": "F2", "Db": "C#2", "Eb": "D#2", "Bbm": "A#1", "C": "C2", "Ab": "G#1"}
KOTO = {"Fm": ["F4", "G#4", "C5"], "Db": ["F4", "G#4", "C#5"], "Eb": ["G4", "A#4", "D#5"], "Bbm": ["F4", "A#4", "C#5"], "C": ["E4", "G4", "C5"], "Ab": ["G#4", "C5", "D#5"]}


def koto_clock(ch, density):
    """琴の時計: density＝1 は8分の 3+3、0.5 は4分、0.25 は小節に2つ、0.1 は小節に1つ"""
    a, b_, c = KOTO[ch]
    if density >= 1: return bar(f"{a}:0.5 {b_}:0.5 {c}:0.5 {a}:0.5 {b_}:0.5 {c}:0.5 {a}:0.5 {c}:0.5 {b_}:0.5 {a}:0.5 {b_}:0.5 {c}:0.5")
    if density >= 0.5: return bar(f"{a}:1 {b_}:1 {c}:1 {a}:1 {c}:1 {b_}:1")
    if density >= 0.25: return bar(f"{a}:3 {c}:3")
    return bar(f"{a}:6,")


# 旋律: 伸ばす音（場面ごとに減る）
SURF = [bar("C5:3 R:1 G#4:2"), bar("F4:2 R:1 G#4:3"), bar("C5:3 R:1 D#5:2"), bar("A#4:4 R:2"),
        bar("C5:3 R:1 F5:2"), bar("C#5:2 R:1 G#4:3"), bar("A#4:3 R:1 C#5:2"), bar("C5:4 R:2")]
D100 = [bar("F4:4 R:2"), bar("R:1 G#4:3 F4:2"), bar("C5:4 R:2"), bar("R:1 A#4:5"), bar("G#4:4 R:2"), bar("R:1 F4:3 G#4:2"),
        bar("F4:4 R:2"), bar("R:1 E4:5"), bar("C5:4 R:2"), bar("R:1 C#5:3 G#4:2"), bar("A#4:3 R:3"), bar("G4:5 R:1")]
D300 = [bar("R:1 F4:5"), R6, bar("R:2 F4:4"), R6, bar("R:1 C#4:5"), R6, bar("R:2 E4:4"), R6, bar("R:1 C4:5"), R6, bar("R:3 F4:3"), bar("E4:4 R:2")]
D700 = [R6, bar("R:3 C4:3"), R6, R6, bar("R:2 C#4:4"), R6, R6, bar("R:3 A#3:3"), R6, bar("C4:4 R:2")]

def breathe(b_):
    """小節の終わりまで伸ばさず、最後に息つぎ（8分の休み）を置く"""
    t = b_.split()
    if t and not t[-1].startswith("R"):
        n_, d_ = t[-1].split(":")[0], tok_beats(t[-1])
        if d_ >= 2: t[-1] = f"{n_}:{d_ - 0.5:g}"; t.append("R:0.5")
    return bar(" ".join(t))


SURF, D100, D300, D700 = ([breathe(x) for x in L] for L in (SURF, D100, D300, D700))

P = {k: [] for k in ["riff", "rhy", "lead", "koto", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = R6
    g = LOW[ch]; root = root_note(ch)
    if name == "surface":
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 {g}:1 {tr(g, 7)}:1.5! {g}:0.5 {g}:1")
        koto = koto_clock(ch, 1); lead = SURF[i] if i >= 4 else R6
        b = bar(f"{root}:1.5! {root}:1.5 {fifth_of(ch)}:1.5 {root}:1.5")
    elif name == "d100":
        riff = rhy = bar(f"{g}:2! {g}:1 {tr(g, 7)}:2! {g}:1")
        koto = koto_clock(ch, 1 if i < 6 else 0.5); lead = D100[i]
        b = bar(f"{root}:3! {root}:3")
    elif name == "d300":
        riff = bar(f"{g}:3! R:3") if i % 2 == 0 else R6
        rhy = R6
        koto = koto_clock(ch, 0.5); lead = D300[i]
        b = bar(f"{root}:6")
    elif name == "d700":
        koto = koto_clock(ch, 0.25); lead = D700[i]
        b = bar(f"{root}:6,") if i % 2 == 0 else R6
    elif name == "d1000":
        koto = koto_clock(ch, 0.1) if i % 2 == 0 else R6
        b = bar("F1:6,") if i < 6 else R6
    else:   # crush
        riff = rhy = bar("F2:6!") if i == 0 else R6
        koto = R6 if i == 0 else bar("R:4 F5:2,")                     # 圧壊のあと、時計の最後の一音
        b = bar("F1:6!") if i == 0 else R6
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["koto"].append(koto); P["bass"].append(b)
    kit.add("X" + "." * 23, "." * 12 + "X" + "." * 11, "".join("x" if j % 4 == 0 else "." for j in range(24)))

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("琴", "koto", J("koto"), volume=0.12, pan=-0.25, reverb=0.45, attack=0.002, release=1.0,
              fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 2200, "high": 1}, {"type": "delay", "beats": 1.5, "mix": 0.18, "feedback": 0.3}, {"type": "plate", "mix": 0.22}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "glossy-jrock"

from lm25_plans import apply_plan
apply_plan(song, "11")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-11-shinkai.json"
    song.write(out)
    check_clash(song)
