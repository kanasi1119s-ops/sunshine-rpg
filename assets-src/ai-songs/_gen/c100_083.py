# ケルト・フルート100曲「銀の笛と百の夜」083 氷の吐息 Breath of Ice — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 春を迎える祭りの前夜（インボルグ前夜）。雪原の小屋で、エイラは旅の娘と出会う。ふたりは凍える息を白く吐きながら、
#   2本の笛で古い歌を吹く。2つの節は、編み物の糸のように、上になり下になりして交差していく。
# 調べ: あいだ。形: 2声が編むようにからむ（8小節の対の節 A・B を、場面ごとに組みかえて）。
# 拍子・速さ: 3/4・♩=63。旋法: E イオニア（高い音を少なく。E4〜E5 が中心）。
# 主役は笛（2本。エイラの笛と、旅の娘の笛。どちらも主旋律で、2小節ごとに上下が入れかわる）。
#   伴奏の主役: 高い弦（バイオリンの高い持続。チェロのハーモニクスのような細い音）。低音・竪琴・ギター・ピアノ・パッド・打楽器は使わない。
# この曲だけ: 2本の笛が編み物のように交差する（2小節ごとに、上の笛と下の笛が入れかわる）。
# 始まり: 2本の笛 → 終わり: 2本の笛。
# 山: 中盤。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "083-breath-of-ice", "氷の吐息", "Breath of Ice", 63, 3, "E", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.15})
K = Key("E", "major", 4)
CA = ["E", "B", "E", "E", "A", "A", "B", "E"]; CB = ["A", "E", "B", "B", "A", "E", "B", "E"]
SC = [("2本の笛", 4, "intro", ["E", "B", "A", "E"]), ("編む1", 24, "verse", CA + CB + CA), ("編む2", 24, "chorus", CB + CA + CB),
      ("編む3", 28, "verse", CA + CB + CA + ["A", "E", "B", "E"]), ("2本の笛だけ", 8, "outro", CA)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("2本の笛", 0, 0.72), ("編む1", 0, 0.72), ("編む2", 0, 0.8), ("編む2", 14, 0.88), ("編む3", 0, 0.74), ("2本の笛だけ", 0, 0.7), ("2本の笛だけ", 7, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="2本の笛", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 2本目の笛（0.1）は笛と同じくらい（047）→ ふたりとも主役なので 0.09
F2 = S.track("旅の娘の笛", "panflute", patch="flute", volume=0.09, bright=-0.5, pan=0.35, reverb=0.55, breath=True, barGain=G)
VN = [S.track(f"高い弦（細い持続{j + 1}）", "strings", patch="violin", volume=0.016, gainDb=2, pan=-0.3 + 0.6 * j, reverb=0.85, release=1.0,
              barGain=[round(x * (1.3 if S.scene_of(b)[0] == "編む2" else 1.0), 3) for b, x in enumerate(G)]) for j in range(2)]

# ---------- 2本の糸（1=E4。2小節ごとに上下が入れかわる） ----------
LA = ["5:2 4:1", "3:2 2:1", "1:2 2:1", "3:3", "4:2 5:1", "6:2 5:1", "5:2 4:1", "3:3"]
FA = ["1:2 2:1", "3:2 4:1", "5:2 4:1", "5:3", "2:2 3:1", "4:2 3:1", "2:2 1:1", "1:3"]
LB = ["1':2 7:1", "6:2 5:1", "4:2 3:1", "2:3", "3:2 4:1", "5:2 6:1", "5:2 4:1", "3:3"]
FB = ["3:2 4:1", "5:2 6:1", "7:2 1':1", "7:3", "6:2 5:1", "4:2 3:1", "2:2 1:1", "1:3"]
def weave(sc, order, b0=None, dens=0.15, seed=0, cut=None):
    b0 = c.s0[sc] if b0 is None else b0
    L_, F_ = [], []
    for x in order:
        L_ += LA if x == "A" else LB; F_ += FA if x == "A" else FB
    if cut: L_, F_ = L_[:cut], F_[:cut]
    for track, bars, sd in ((c.FLUTE, L_, seed), (F2, F_, seed + 50)):
        ev = []
        for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (b0 + j) * B)
        play(track, ornament([[round(t, 4), L, m] for t, L, m in ev], K, 63, "air", B, density=dens, seed=sd))
weave("2本の笛", ["B"], dens=0.1, seed=8300, cut=4)              # 前奏は B の前半4小節だけ
weave("編む1", ["A", "B", "A"], dens=0.15, seed=8301)
weave("編む2", ["B", "A", "B"], dens=0.3, seed=8302)
weave("編む3", ["A", "B", "A", "B"], dens=0.15, seed=8303, cut=28)
weave("2本の笛だけ", ["A"], dens=0.05, seed=8304)

# ---------- 高い弦（細い持続。2小節ごと） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.s0["編む1"], c.s0["2本の笛だけ"], 2):
    ch = S.chords[b]; r, th, fi = tri(ch)
    VN[0].at(b * B, f"{nm(near(fi, 83))}:{2 * B + 0.3}{',' if b % 4 else ''}"); VN[1].at(round(b * B + 0.08, 3), f"{nm(near(th, 88))}:{2 * B + 0.2},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の083（第3版）。春を迎える祭りの前夜、雪原の小屋で、エイラと旅の娘が2本の笛で古い歌を吹く。3/4・♩=63、E の長調（高い音を少なく）。2つの節は、2小節ごとに上の笛と下の笛が入れかわり、編み物の糸のように交差していく。伴奏は高い弦の細い持続だけで、低い音はない。山は中盤。2本の笛で始まり、2本の笛で終わる。",
       harm_scenes=None, tail_scene="2本の笛だけ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 220, "lp": 4200, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 3200, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air083.json", "w"), ensure_ascii=False)
