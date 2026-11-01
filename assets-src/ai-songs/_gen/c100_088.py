# ケルト・フルート100曲「銀の笛と百の夜」088 氷柱 Icicles — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 吹雪がやみ、朝日が雪洞の入口の氷柱を照らす。氷柱の先から、ぽつん、と1粒のしずく。日が高くなるにつれて、
#   しずくの落ちる間がだんだん詰まり、ぽつ、ぽつ、ぽつぽつぽつ…と速くなる。エイラはそのしずくに合わせて、小さく踊るように笛を吹く。
# 調べ: 喜び。形: 小さな踊り（8小節の A・B。AABB を4回 → 溶けていく B の変奏）。しずくの間はずっと詰まり続ける。
# 拍子・速さ: 2/4・♩=108。旋法: F リディア（B♮ が明るい）。
# 主役は笛（短く澄んだ音）。伴奏の主役: 木琴のしずくと、ピチカート（低音と裏の和音）。
#   竪琴・ギター・ピアノ・パッド・弓の弦・打楽器・2本目の笛は使わない。
# この曲だけ: 氷柱が溶けて、しずく（木琴の高い1音）の間隔が、4拍 → 2拍 → 1拍 → 半拍 → 4分の1拍 と、曲を通してだんだん詰まる。
# 始まり: しずくの1音 → 終わり: しずくの1音。
# 山: 中盤（2〜3回目）。
import sys, json, re, math
from c100_common import *
from c100_v2 import *

S = Song("C100", "088-icicles", "氷柱", "Icicles", 108, 2, "F", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
K = Key("F", "lydian", 4)
CA = ["F", "C", "F", "C", "F", "C", "G", "F"]; CB = ["F", "F", "C", "C", "Dm", "G", "G", "F"]
T = CA * 2 + CB * 2
SC = [("しずく", 2, "intro", ["F", "F"])] + [(f"踊り{k + 1}", 32, ("chorus" if k in (1, 2) else "verse"), T) for k in range(4)] + \
     [("溶ける", 80, "verse", CB * 10), ("最後のしずく", 4, "outro", ["F"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("しずく", 0, 0.76), ("踊り1", 0, 0.74), ("踊り2", 0, 0.84), ("踊り3", 0, 0.88), ("踊り4", 0, 0.8), ("溶ける", 0, 0.78), ("溶ける", 79, 0.7), ("最後のしずく", 0, 0.7)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="しずく", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
XY = [S.track(f"しずく（木琴{j + 1}）", "xylophone", volume=0.06, pan=-0.3 + 0.6 * j, reverb=0.55, barGain=[0.8] * c.NB) for j in range(2)]
PZ = [S.track(f"ピチカート（{x}）", "strings", patch="pizzicato", volume=v, gainDb=5, pan=p, reverb=0.35, barGain=G) for x, v, p in (("低音", 0.12, -0.2), ("裏の和音", 0.08, 0.15))]

# ---------- 小さな踊り（8分＝0.5。1=F4） ----------
A = ["5:0.5 3:0.5 5:0.5 1':0.5", "7:0.5 5:0.5 4:1", "3:0.5 4:0.5 5:0.5 3:0.5", "2:0.5 1:0.5 2:1",
     "5:0.5 3:0.5 5:0.5 1':0.5", "2':0.5 1':0.5 7:1", "6:0.5 5:0.5 4:0.5 3:0.5", "1:1 R:1"]
Bm = ["1':0.5 7:0.5 1':0.5 2':0.5", "3':1 1':1", "7:0.5 6:0.5 7:0.5 1':0.5", "2':1 5:1",
      "6:0.5 7:0.5 1':0.5 6:0.5", "5:0.5 4:0.5 3:1", "2:0.5 3:0.5 4:0.5 2:0.5", "1:1 R:1"]
for k in range(4):
    play_melody(c, f"踊り{k + 1}", A + A + Bm + Bm, 4, "reel", key=K, density=(0.25, 0.4, 0.45, 0.3)[k], seed=8800 + k)
BV = ["1':0.5 7:0.5 1':0.5 2':0.5", "3':1 1':1", "7:0.5 6:0.5 7:0.5 1':0.5", "2':1 5:1", "6:0.5 7:0.5 1':0.5 6:0.5", "5:0.5 4:0.5 3:1", "2:0.5 3:0.5 4:0.5 2:0.5", "1:2"]
melt = []
for q in range(10):                                                    # 溶ける：B を10回。だんだん音を減らす
    melt += BV if q < 6 else [x if j % (2 if q < 8 else 3) == 0 else "R:2" for j, x in enumerate(BV)]
play_melody(c, "溶ける", melt, 4, "reel", key=K, density=0.25, seed=8810)

# ---------- しずく（間隔が4拍から 1/4 拍まで、だんだん詰まる） ----------
t = 0.5; t_end = c.s0["最後のしずく"] * B
total = t_end - t
k = 0
while t < t_end - 0.01:
    x = (t - 0.5) / total                                              # 0 → 1
    gap = 4.0 * (1 / 16) ** x                                          # 4拍 → 1/4拍（指数で）
    m = (93, 89, 91, 88, 96, 86)[k % 6]
    XY[k % 2].at(round(t, 3), f"{nm(m)}:0.25{',' if k % 3 else ''}")
    t += gap; k += 1
XY[0].at(round((c.s0["最後のしずく"] + 2) * B, 3), "A6:1")                 # 最後のしずく（1粒）
c.FLUTE.at(c.s0["最後のしずく"] * B, "F5:2!")

# ---------- ピチカート（低音は1・2拍目、裏の和音は裏拍） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.s0["踊り1"], c.s0["最後のしずく"]):
    n, i, Lb, kk = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 41)
    PZ[0].bar(b, f"{nm(lo)}:0.5{'' if i % 2 == 0 else ','} R:0.5 {nm(near(fi, lo + 1))}:0.5, R:0.5")
    if n in ("踊り2", "踊り3") or i % 2 == 0:
        PZ[1].bar(b, f"R:0.5 {nm(near(th, 60))}:0.25, R:0.75 {nm(near(fi, 60))}:0.25, R:0.25")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の088（第3版）。吹雪がやみ、朝日の中で氷柱が溶けはじめる。2/4・♩=108、F リディア。木琴のしずくの1音で始まり、ピチカートの低音と裏の和音に乗って、笛が短く澄んだ音で小さく踊る（AABB を4回。2〜3回目が山）。しずくの間隔は、4拍 → 2拍 → 1拍 → 半拍 → 4分の1拍と、曲を通してだんだん詰まっていく。最後は笛の音がまばらになり、しずくの1音で終わる。",
       harm_scenes=None, tail_scene="最後のしずく", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4200, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3200, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air088.json", "w"), ensure_ascii=False)
