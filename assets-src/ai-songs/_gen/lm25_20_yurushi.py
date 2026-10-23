# ラウド26曲 20「Clowns Don't Apologize」（仮。もとの仮題「赦しの値段」）。2026-10-24 素材から作り直し
# スタイル: アヴァンギャルドなサーカスメタル（5拍子の跳ねる刻み・急なテンポの切りかえ・半音のおどけ）＋木琴。A 短調・5/4（3+2）
# 物語: 「赦し」を売る見世物小屋。呼びこみの口上、綱渡り、道化のおどけ、空中ぶらんこ、猛獣使い、大団円、幕。
# 形: 演目の並び（場面ごとに速さと感じが変わる: 120・96・144・108・132）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   口上（1）: 木琴の呼びこみ
#   綱渡り（2）: 3+2 の跳ねる刻み。リードと木琴が、半音でよろけながら綱を渡る
#   道化（0→1）: 急に小さく、96。木琴とベースの短い音でおどける。笑い声のような3連
#   空中ぶらんこ（3）: 144 の速い3連の揺れ
#   猛獣使い（3）: 108。タムの太鼓と、低くうなるリード
#   大団円（3）: 132、半音上で全員。リードと木琴が同じ旋律
#   幕（1）: 木琴の笑い声で、ぷつりと切れる
# 旋律の性格: 半音でよろける（隣の音へ寄り道してから着く）・はねる3連・短く切る音。場面ごとに速さと形が変わる
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 120, 5
bar = Bars(BEATS)
R5 = bar.rest()

FORM = [("barker", 6), ("rope", 20), ("clown", 12), ("trapeze", 20), ("beasts", 16), ("finale", 20), ("curtain", 4)]
CH = {"barker": ["Am", "E7", "Am", "E7", "Am", "E7"], "rope": ["Am", "Dm", "E7", "Am"] * 5, "clown": ["C", "G7", "C", "G7", "F", "C", "G7", "C"] + ["Am", "E7", "Am", "E7"],
      "trapeze": ["Am", "F", "Dm", "E7"] * 5, "beasts": ["Am", "Am", "Bb", "Bb"] * 4, "finale": ["Am", "Dm", "G", "C", "F", "Dm", "E7", "Am"] * 2 + ["Am", "Dm", "E7", "Am"],
      "curtain": ["Am", "Am", "E7", "Am"]}
song = Song("赦しの値段（仮）",
            "仮: ラウド26曲の20曲目（2026-10-24 素材から作り直し）。サーカスメタル＋木琴。A 短調・5/4（3+2）。口上・綱渡り・道化（96）・空中ぶらんこ（144）・猛獣使い（108）・"
            "大団円（132・半音上）・幕。旋律は半音でよろけ、3連ではね、短く切る。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 「赦し」を売る見世物小屋の演目。最後は木琴の笑い声で幕。"
song.kinds = {"barker": "intro", "rope": "verse", "clown": "bridge", "trapeze": "chorus", "beasts": "break", "finale": "chorus", "curtain": "outro"}
SECS, NB = song.secs, song.nb
AH = scale_pcs("A", "harmonic")
CHROM = set(range(12))

RH_ROPE = [[-0.5, 0.25, 0.25, 0.5, 0.5, 0.5, -0.5, 0.5, 0.5, -1], [0.5, 0.25, 0.25, 1, -0.5, 0.25, 0.25, 0.5, 0.5, -1], [-1, 0.3333, 0.3333, 0.3334, 0.5, 0.5, 0.5, 0.5, -1]]
RH_TRAP = [[0.3333, 0.3333, 0.3334] * 3 + [1, -1], [1, 0.3333, 0.3333, 0.3334, 1, 0.3333, 0.3333, 0.3334, -1], [-1] + [0.3333, 0.3333, 0.3334] * 2 + [1, 1]]
RH_BEAST = [[1.5, -0.5, 0.5, 0.5, 1, -1], [0.75, 0.25, -1, 1.5, -1.5], [-0.5, 1, 0.5, 0.5, 1.5, -1]]
RH_FIN = [[0.5, 0.5, 1, 0.5, 0.5, 1, -1], [-0.5, 0.5, 0.3333, 0.3333, 0.3334, 1, 1, -1], [1, 0.5, 0.5, 0.5, 0.5, 1, -1]]
ROPE = [bar(x) for x in melody_walk(AH, "E4", "A4", RH_ROPE, 1, CH["rope"], contour=(1, -1, 2, -1, -1, 1), lo="C4", hi="E5", beats=5)]
TRAP = [bar(x) for x in melody_walk(AH, "A4", "E5", RH_TRAP, 2, CH["trapeze"], contour=(1, 1, -2, 2, -1), lo="E4", hi="F#5", beats=5)]
BEAST = [bar(x) for x in melody_walk(AH, "E4", "A3", RH_BEAST, 3, CH["beasts"], contour=(-1, 1, -2, 1), lo="E3", hi="E4", beats=5)]
FIN = [bar(x) for x in melody_walk(AH, "C5", "A4", RH_FIN, 4, CH["finale"], contour=(1, 2, -1, -1, 2, -2), lo="E4", hi="E5", beats=5)]
# 口上（木琴）と、道化の笑い（半音のよろけ＋3連）
BARKER = ["A5:0.5! G#5:0.25 A5:0.25 E5:0.5 R:0.5 C5:0.5 B4:0.5 A4:0.5 R:1.5", "R:2 B4:0.25 C5:0.25 D5:0.5 E5:0.5 G#5:0.5 R:1",
          "A5:0.5! R:0.5 A5:0.25 G#5:0.25 G5:0.25 F#5:0.25 F5:0.5 E5:0.5 R:2", "R:1 D#5:0.25 E5:0.75 R:0.5 B4:0.5 G#4:0.5 E4:0.5 R:1",
          "A4:0.3333 C5:0.3333 E5:0.3334 A5:1 R:1 E5:0.3333 F5:0.3333 E5:0.3334 R:1", "D#5:0.25 E5:0.25 R:0.5 G#4:0.5 B4:0.5 E5:0.5 R:2.5"]
CLOWN = ["C5:0.25 B4:0.25 C5:0.5 R:1 E5:0.3333 D#5:0.3333 E5:0.3334 R:2", "R:1 F5:0.25 E5:0.25 D5:0.5 R:0.5 B4:0.25 C5:0.25 D5:0.5 R:1.5",
         "G4:0.5 G#4:0.5 A4:0.5 R:0.5 C5:0.3333 B4:0.3333 A#4:0.3334 A4:1 R:1", "R:2 D5:0.25 C#5:0.25 D5:0.5 G4:0.5 R:1.5",
         "A4:0.25 G#4:0.25 A4:0.5 R:0.5 C5:0.25 B4:0.25 C5:0.5 R:0.5 F5:0.5 R:1.5", "E5:0.3333 D#5:0.3333 E5:0.3334 G5:0.5 R:1 C5:0.5 R:2",
         "R:1 B4:0.25 A#4:0.25 B4:0.5 R:0.5 F4:0.5 G4:0.5 R:1.5", "C5:0.5 R:0.5 E4:0.25 F4:0.25 G4:0.5 C5:0.5 R:2.5"]

LOW = {"Am": "A1", "E7": "E2", "Dm": "D2", "C": "C2", "G7": "G1", "F": "F2", "Bb": "A#1", "G": "G1"}
P = {k: [] for k in ["riff", "rhy", "lead", "xylo", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = xylo = R5
    g = LOW[ch]; root = root_note(ch)
    hop = bar(f"{g}:0.5! R:0.5 {g}:0.25 {g}:0.25 {tr(g, 7)}:0.5! R:0.5 {up(g, 1)}:0.5 {tr(g, 6)}:0.5 {g}:0.5! R:1")   # 3+2 の跳ね
    if name == "barker":
        xylo = bar(BARKER[i]); b = bar(f"{root}:1.5, R:1.5 {fifth_of(ch)}:1, R:1") if i >= 2 else R5
    elif name == "rope":
        riff = rhy = hop if i >= 4 else bar(f"{g}:0.5! R:2.5 {g}:0.5! R:1.5")
        lead = ROPE[i]
        xylo = bar(strip_marks(ROPE[i])) if i % 4 >= 2 else R5
        b = unison_low(hop, -1, "B0")
    elif name == "clown":
        xylo = bar(CLOWN[i % 8]) if i < 8 else R5
        lead = bar(CLOWN[i % 8]).replace("5:", "4:") if False else (R5 if i < 8 else ROPE[i])
        b = bar(f"{root}:0.5 R:1 {fifth_of(ch)}:0.5 R:1 {root}:0.5 R:1.5") if i < 8 else unison_low(hop, -1, "B0")
        if i >= 8: riff = hop
    elif name == "trapeze":
        riff = rhy = bar(" ".join(f"{g}:{1/3 if j % 3 != 2 else 1/3 + 1e-4:.4f}{'!' if j % 3 == 0 else ''}" for j in range(15)))
        lead = TRAP[i]
        xylo = bar(strip_marks(TRAP[i])) if i >= 10 else R5
        b = bar(f"{root}:1 {root}:1 {fifth_of(ch)}:1 {root}:1 {fifth_of(ch)}:1")
    elif name == "beasts":
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 R:0.5 {g}:0.5! {tr(g, 1)}:0.25 R:0.75 {g}:1!")
        lead = BEAST[i]
        b = unison_low(riff, -1, "B0")
    elif name == "finale":
        riff = rhy = hop
        lead = FIN[i]; xylo = bar(strip_marks(FIN[i]))
        b = unison_low(hop, -1, "B0")
    else:   # curtain
        xylo = bar("A5:0.3333 G#5:0.3333 A5:0.3334 E5:0.3333 D#5:0.3333 E5:0.3334 C5:0.3333 B4:0.3333 C5:0.3334 A4:0.5! R:1.5") if i == 0 else (bar("R:1 E5:0.25 A5:0.25 R:3.5") if i == 2 else R5)
        riff = rhy = bar("A1:0.5! R:4.5") if i == 3 else R5
        b = bar("A1:0.5! R:4.5") if i == 3 else R5
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["xylo"].append(xylo); P["bass"].append(b)
    kit.add("X.....X.....X.......", "....X.......X.......", "x.x.x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("木琴", "xylophone", J("xylo"), volume=0.14, pan=-0.25, reverb=0.3, attack=0.002, release=0.4,
              fx=[{"type": "eq", "low": 0, "mid": 1, "midHz": 2500, "high": -1}, {"type": "plate", "mix": 0.18}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "deep-scoop-djent"

from lm25_plans import apply_plan
apply_plan(song, "20")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-20-yurushi.json"
    song.write(out)
    check_clash(song)
