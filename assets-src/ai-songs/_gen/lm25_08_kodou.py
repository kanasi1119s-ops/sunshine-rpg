# ラウド26曲 08「心拍、加速、停止」（仮。もとの仮題「鼓動の前」）。2026-10-24 素材から作り直し
# スタイル: マスコア（3+3+2 でずれる刻み・急な止め・速さの変化）＋バイオリン。G 短調・80 → 160 → 停止 → 60・7/4（3+2+2）
# 物語: 心臓の鼓動がだんだん速くなり、限界で止まる。心電図の平らな音。そして、ゆっくり動き出す。
# 形: 速さそのものが物語（80・96・120・144・160 と上がり、停止、60 で蘇る）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   鼓動（0→1）: キックの心音とバイオリンの「ドクン」だけ
#   早まる（1→2）: バンドが入る。刻みはまばら
#   走る（2）: リードが「ドクン」を細かくした線で
#   動悸（3）: 3+3+2 の刻みが拍とずれて暴れる
#   限界（3）: いちばん速い。最後の拍で止まる
#   停止: 心電図の平らな音（バイオリンの高い1音）と無音
#   蘇生（1→3）: 60 の重いハーフタイム。「ドクン」が長い歌になり、この曲でいちばん大きな歌になる
#   脈（3）: 全員で「ドクン」を4回たたき、最後の一打で切れる（静かに消えない）
# 旋律の性格: 「短い・長い」の2音（ドクン）が核。場面ごとに細かく（8分 → 16分）、最後は長く歌う
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 80, 7
bar = Bars(BEATS)
R7 = bar.rest()

FORM = [("pulse", 6), ("quicken", 12), ("race", 12), ("panic", 12), ("peak", 8), ("flat", 2), ("revive", 10), ("beat", 4)]
CH = {"pulse": ["Gm"] * 6, "quicken": ["Gm", "Gm", "Eb", "D7"] * 3, "race": ["Gm", "Eb", "Cm", "D7"] * 3,
      "panic": ["Gm", "Ab", "Gm", "Ab", "Eb", "D7"] * 2, "peak": ["Gm", "Ab", "Gm", "Ab", "Gm", "Ab", "D7", "D7"],
      "flat": ["Gm", "Gm"], "revive": ["Gm", "Eb", "Bb", "F", "Cm", "Eb", "D7", "D7", "Gm", "Gm"], "beat": ["Gm"] * 4}
song = Song("鼓動の前（仮）",
            "仮: ラウド26曲の8曲目（2026-10-24 素材から作り直し）。マスコア＋バイオリン。G 短調・7/4（3+2+2）。80 から 160 まで速くなり、止まり、60 で蘇る。"
            "旋律は「ドクン」の2音が核で、場面ごとに細かくなり、最後は長く歌う。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 鼓動がだんだん速くなり、限界で止まり、心電図の平らな音のあと、ゆっくり動き出す。"
song.kinds = {"pulse": "intro", "quicken": "verse", "race": "pre", "panic": "chorus", "peak": "break", "flat": "interlude", "revive": "chorus", "beat": "break"}
SECS, NB = song.secs, song.nb

LOW = {"Gm": "G1", "Eb": "D#2", "Cm": "C2", "D7": "D2", "Ab": "G#1", "Bb": "A#1", "F": "F2"}
DUB = {"Gm": ("G4", "D5"), "Eb": ("G4", "D#5"), "Cm": ("G4", "C5"), "D7": ("F#4", "D5"), "Ab": ("G#4", "D#5"), "Bb": ("F4", "D5"), "F": ("F4", "C5")}


def math_riff(ch, var):
    """16分の 3+3+2・3+3+2・3+3+2・4（7拍＝28）で、拍とずれて当たる"""
    r = LOW[ch]; grp = [3, 3, 2, 3, 3, 2, 3, 3, 2, 4] if var % 2 == 0 else [2, 3, 3, 2, 3, 3, 4, 3, 3, 2]
    notes = [r, r, tr(r, 6), r, r, tr(r, 1), r, tr(r, 7), r, r]
    toks = []
    for j, g in enumerate(grp):
        hit = min(g, 2) * 0.25
        toks.append(f"{notes[j]}:{hit:g}!");
        if g * 0.25 - hit > 1e-9: toks.append(f"R:{g * 0.25 - hit:g}")
    return bar(" ".join(toks))


def dub(ch, unit, pattern_seed):
    """「ドクン」: 短い・長い の2音を unit の細かさでくり返す（休みも入れる）"""
    a, b = DUB[ch]
    if unit == 1:      # 4分の短い＋2分の長い（ゆっくりの心臓）
        return bar(f"{a}:0.5! {b}:1 R:1.5 {a}:0.5! {b}:1 R:2.5")
    if unit == 0.5:
        return bar(f"{a}:0.25! {b}:0.75 R:0.5 {a}:0.25! {b}:0.75 R:1 {a}:0.25! {b}:0.75 {up(a, 1) if pattern_seed % 2 else b}:0.5 R:2")
    pats = [f"{a}:0.25! {b}:0.5 R:0.25 {a}:0.25! {b}:0.5 R:0.25 {a}:0.25 {b}:0.25 {a}:0.25 {b}:0.5 R:0.25 {a}:0.25! {b}:0.5 R:0.25 {a}:0.25 {b}:0.25 {up(a, 1)}:0.5 R:1.5",
            f"R:0.5 {a}:0.25! {b}:0.5 {a}:0.25 {b}:0.5 R:0.5 {b}:0.25 {a}:0.25 {b}:0.5! R:0.5 {a}:0.25 {b}:0.25 {a}:0.25 {b}:0.75 R:1.5"]
    return bar(pats[pattern_seed % 2])


# 蘇生: 「ドクン」が長い歌になる（10小節）
REVIVE = [bar("G4:1 D5:2 R:1 D5:0.5 C5:0.5 A#4:2"), bar("G4:1 D#5:2 R:1 D5:0.5 C5:0.5 G4:2"),
          bar("F4:1 D5:2 R:1 C5:0.5 A#4:0.5 F4:2"), bar("A4:1 C5:2 R:1 D5:1 F5:2"),
          bar("G4:1 D#5:2 R:0.5 D5:0.5 C5:1 G4:2"), bar("G4:1 A#4:1 D#5:2 R:1 C5:1 A#4:1"),
          bar("A4:1 F#4:2 R:1 A4:1 C5:2"), bar("D5:3 R:4"),
          bar("G4:1 D5:2 R:1 G5:1 F5:1 D5:1"), bar("D5:3 R:4")]

P = {k: [] for k in ["riff", "rhy", "lead", "vln", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = vln = R7
    root = root_note(ch)
    if name == "pulse":
        vln = dub(ch, 1, i) if i >= 2 else R7
        b = R7
    elif name == "quicken":
        vln = dub(ch, 0.5, i)
        riff = bar(f"{LOW[ch]}:0.5! R:2.5 {LOW[ch]}:0.5! R:1.5 {LOW[ch]}:0.5! R:1.5") if i < 6 else math_riff(ch, i)
        b = bar(f"{root}:0.5! R:2.5 {root}:0.5! R:1.5 {root}:0.5! R:1.5")
    elif name == "race":
        riff = rhy = math_riff(ch, i); lead = dub(ch, 0.25, i)
        vln = bar(f"{DUB[ch][1]}:3 {DUB[ch][0]}:4") if i % 2 == 0 else bar(f"{up(DUB[ch][0], 1)}:4 {DUB[ch][1]}:3")   # 1小節おきに消えていた（途中で小さくなる）
        b = unison_low(riff, -1, "B0")
    elif name == "panic":
        riff = rhy = math_riff(ch, i + 1); lead = dub(ch, 0.25, i + 1)
        vln = shift_oct(strip_marks(lead), 1) if i >= 6 else bar(f"{up(DUB[ch][1], 1)}:7")
        b = unison_low(riff, -1, "B0")
    elif name == "peak":
        r = LOW[ch]
        riff = rhy = bar(" ".join(f"{r}:0.25{'!' if j % 4 == 0 else ''}" for j in range(28))) if i < n - 1 else bar(f"{r}:0.5! R:6.5")
        lead = dub(ch, 0.25, i) if i < n - 1 else R7
        b = unison_low(riff, -1, "B0")
    elif name == "flat":
        vln = bar("A6:7") if i == 0 else bar("A6:3 R:4")              # 心電図の平らな音
        b = R7
    elif name == "revive":
        lead = REVIVE[i]
        # 2026-10-24 人間「08 は途中でバイオリンの音が小さくなるから、そこが少しこもって聞こえる」: 1オクターブ下（G3〜F4）で
        #   歪んだギターの帯域に埋もれていた。蘇生の歌は1オクターブ上で、透き通るように重ねる
        vln = shift_oct(strip_marks(REVIVE[i]), 1) if i >= 2 else R7
        if i >= 2:
            r = LOW[ch]; riff = rhy = bar(f"{r}:1.5! R:0.5 {r}:1 {r}:2! R:2") if i % 2 == 0 else bar(f"{r}:3! {tr(r, 7)}:2 R:2")
        b = bar(f"{root}:3 {root}:4") if i >= 1 else R7
    else:   # beat: 全員で「ドクン」
        r = LOW[ch]
        riff = rhy = bar(f"{r}:0.5! {r}:1! R:5.5") if i < n - 1 else bar(f"{r}:0.5! R:6.5")
        lead = bar("G4:0.5! D5:1! R:5.5") if i < n - 1 else bar("G5:0.5! R:6.5")
        vln = strip_marks(lead)
        b = unison_low(riff, -1, "B0")
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["vln"].append(vln); P["bass"].append(b)
    # 心音（ドクン）: 鼓動・蘇生のはじめ・脈の場面のキック
    if name in ("pulse", "beat") or (name == "revive" and i < 2):
        kit.add("X..X........................" [:28], "." * 28, "." * 28)
    else:
        kit.add("X" + "." * 11 + "X" + "." * 15, "." * 12 + "X" + "." * 15, "".join("x" if j % 4 == 0 else "." for j in range(28)))

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("バイオリン", "strings", J("vln"), patch="violin", volume=0.16, pan=-0.15, reverb=0.5, gainDb=3, bright=0.0, attack=0.08, release=0.7,
              doubleDetune={"cents": 5, "spread": 0.3}, phrase=8,
              fx=[{"type": "eq", "low": -1, "mid": 1.5, "midHz": 3200, "high": 0.5}, {"type": "delay", "beats": 1, "mix": 0.08, "feedback": 0.2},
                  {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "deep-scoop-djent"

from lm25_plans import apply_plan
apply_plan(song, "08")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-08-kodou.json"
    song.write(out)
    check_clash(song)
