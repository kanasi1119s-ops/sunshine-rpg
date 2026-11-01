# ケルト・フルート100曲「銀の笛と百の夜」094 鐘楼への階段 The Stairs to the Belfry — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 島の灯台の上に、止まったままの鐘がある。エイラは鐘楼へ続く古い石の階段を登る。段の高さはばらばらで、
#   足どりは「いち・に・さん、いち・に」とつまずくような5拍子になる。一段ずつ（一回りずつ）高くなり、最後に鐘楼の扉が開く。
# 調べ: あいだ。形: 5拍子の上り（コーンウォールふうの5拍子の踊り。16小節の節を5回、回ごとに全音ずつ高く：C → D → E → F → G）。
# 拍子・速さ: 5/4・♩=96（3＋2）。旋法: C ミクソリディア（回ごとに主音が上がる）。
# 主役は笛（一段ずつ）。伴奏の主役: 竪琴（3＋2 の分散和音）とピチカート（足音。1拍目と4拍目）。
#   ギター・ピアノ・パッド・弓の弦・打楽器・2本目の笛は使わない。
# この曲だけ: 5拍子のつまずく足どり（3＋2）。回るたびに全音ずつ高くなる階段。
# 始まり: 足音 → 終わり: 鐘楼の扉の和音。
# 山: 階段（回ごとに一段ずつ）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "094-the-stairs-to-the-belfry", "鐘楼への階段", "The Stairs to the Belfry", 96, 5, "C", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
NOTE = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
def tp(ch, k):
    m = re.match(r"^([A-G][#b]?)(.*)$", ch); return NOTE[(PC[m.group(1)] + k) % 12] + m.group(2)
CA = ["C", "F", "C", "F", "F", "F", "Gm", "C"]; CB = ["C", "Bb", "C", "Dm", "Bb", "F", "C", "C"]
UP = [0, 2, 4, 5, 7]                                                     # C → D → E → F → G
SC = [("足音", 2, "intro", ["C", "C"])] + [(f"段{k + 1}", 16, ("chorus" if k == 4 else "verse"), [tp(x, UP[k]) for x in CA + CB]) for k in range(5)] + \
     [("扉", 4, "outro", ["G"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("足音", 0, 0.76)] + [(f"段{k + 1}", 0, round(0.72 + 0.04 * k, 3)) for k in range(5)] + [("段5", 15, 0.94), ("扉", 0, 0.9), ("扉", 3, 0.76)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="足音", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
PZ = [S.track(f"ピチカート（足音{j + 1}）", "strings", patch="pizzicato", volume=0.12, gainDb=(12 if j == 2 else 5), pan=-0.2 + 0.2 * j, reverb=0.35,
              barGain=(G if j < 2 else [0.8] * c.NB)) for j in range(3)]           # 3本目は足音だけの所（始まり）用に大きく
HP = [S.track(f"竪琴{j + 1}", "harp", patch="folkHarp", volume=0.065, pan=0.15 + 0.12 * j, reverb=0.5, sustain=1.4, barGain=G) for j in range(3)]

# ---------- 節（5/4。1=主音4。回ごとに全音ずつ上がる） ----------
A = ["1:1 2:1 3:1 5:2", "4:1 3:1 2:1 1:2", "3:1 4:1 5:1 7:2", "6:1 5:1 4:1 5:2", "1':1 7:1 6:1 5:2", "4:1 5:1 6:1 4:2", "3:1 2:1 1:1 2:2", "1:5"]
Bm = ["5:1 6:1 7:1 1':2", "7:1 6:1 5:1 4:2", "5:1 6:1 5:1 3:2", "4:3 2:2", "1':1 2':1 1':1 7:2", "6:1 7:1 6:1 5:2", "4:1 3:1 2:1 3:2", "1:5"]
for k in range(5):
    Kk = Key(NOTE[UP[k]], "mixolydian", 4)
    play_melody(c, f"段{k + 1}", A + Bm, 4, "march", key=Kk, density=0.25 + 0.05 * k, seed=9400 + k)
c.FLUTE.at(c.s0["扉"] * B, "G5:12")

# ---------- 足音（ピチカート：1拍目と4拍目に、3＋2）と竪琴（3＋2 の分散和音） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 43)
    if n == "足音":
        PZ[2].bar(b, f"{nm(lo)}:1! R:2 {nm(lo + 7)}:1 R:1"); continue
    if n == "扉":
        if i == 0:
            for q, m in enumerate((43, 50, 55, 59, 62, 67, 69, 74)): HP[q % 3].at(round(b * B + 0.2 * q, 3), f"{nm(m)}:{round(18 - 0.2 * q, 2)}{'' if q == 0 else ','}")
            PZ[0].at(b * B, "G2:2!"); PZ[1].at(b * B, "D3:2!")
        continue
    PZ[0].bar(b, f"{nm(lo)}:1! R:2 {nm(lo + 7)}:1 R:1")
    PZ[1].bar(b, f"R:1 {nm(near(th, 55))}:1, R:2 {nm(near(fi, 55))}:1,")
    seq = [near(r, 55), near(fi, 55), near(th, 60), near(r, 67), near(th, 60)]
    for q, m in enumerate(seq):
        HP[q % 3].at(round(b * B + q, 3), f"{nm(m)}:{'1.5' if q in (0, 3) else '1'}{'' if q in (0, 3) else ','}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の094（第3版）。灯台の上の、止まったままの鐘へ続く古い石の階段。5/4・♩=96（3＋2）、C ミクソリディア。ピチカートの足音（1拍目と4拍目）で始まり、竪琴の 3＋2 の分散和音に乗って、笛がつまずくような5拍子で一段ずつ登る。16小節の節を5回、回ごとに全音ずつ高く（C → D → E → F → G）なる階段。最後に鐘楼の扉が開く和音。",
       harm_scenes=None, tail_scene="扉", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 200, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 2800, "rt": 3.2}}}
json.dump(air, open("/tmp/cel/w/air094.json", "w"), ensure_ascii=False)
