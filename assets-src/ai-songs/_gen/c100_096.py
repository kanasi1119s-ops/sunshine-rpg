# ケルト・フルート100曲「銀の笛と百の夜」096 夜明けの前奏 Prelude to Dawn — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 鐘の倍音が島に広がると、夜明け前の家々で、ひとり、またひとりと目をさます。エイラが鐘楼で同じ短い節を吹き続けると、
#   目をさました人たちが、それぞれの楽器で加わっていく。空が白むにつれて音は大きくなり、日がのぼる瞬間、同じ節が長調になる。
# 調べ: あいだ。形: アン・ドロ型（ブルターニュの輪踊り。6小節の短い節を16回くり返し、夜明けの楽器が少しずつ加わる）。
# 拍子・速さ: 4/4・♩=92。旋法: E エオリア → 最後の1回だけ E イオニア。
# 主役は笛（同じ節を吹き続ける）。伴奏: 回ごとに少しずつ（低い弦 → ギター → ボーラン → 高い弦 → 全員）。
#   竪琴・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 16回くり返す同じ節が、最後の1回だけ長調になる（日がのぼる瞬間）。
# 始まり: ひとつの節（笛ひとり）→ 終わり: 同じ節が長調に。
# 山: だんだん大きく（最後がいちばん大きい）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "096-prelude-to-dawn", "夜明けの前奏", "Prelude to Dawn", 92, 4, "E", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
KM, KJ = Key("E", "minor", 4), Key("E", "major", 4)
CMI = ["Em", "Am", "G", "Am", "D", "Em"]; CMA = ["E", "A", "B", "A", "B", "E"]
SC = [(f"{k + 1}回目", 6, ("chorus" if k == 15 else "verse"), CMA if k == 15 else CMI) for k in range(16)] + [("日の出", 2, "outro", ["E", "E"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [(f"{k + 1}回目", 0, round(0.68 + 0.017 * k, 3)) for k in range(16)] + [("16回目", 5, 0.96), ("日の出", 0, 0.92), ("日の出", 1, 0.8)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="1回目", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
VC = S.track("低い弦（チェロ）", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.25, reverb=0.6, release=0.6, barGain=G)
CB_ = S.track("低い弦（コントラバス）", "strings", patch="contrabass", volume=0.025, gainDb=3, pan=-0.1, reverb=0.6, release=0.6, barGain=G)
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=0.25 - 0.08 * i, reverb=0.3, barGain=G) for i in range(5)]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]
VN = S.track("高い弦（バイオリン）", "strings", patch="violin", volume=0.024, gainDb=3, pan=0.3, reverb=0.65, release=0.6, barGain=G)
VA = S.track("高い弦（ビオラ）", "strings", patch="viola", volume=0.017, pan=0.15, reverb=0.65, release=0.6, barGain=G)

# ---------- 同じ節（6小節。1=E4） ----------
P = ["1:0.5 2:0.5 3:1 3:0.5 4:0.5 5:1", "4:0.5 3:0.5 2:1 1:2", "5:0.5 6:0.5 7:1 7:0.5 6:0.5 5:1", "4:0.5 5:0.5 6:1 5:2",
     "3:0.5 4:0.5 5:0.5 3:0.5 2:1 7,:1", "1:1 2:1 1:2"]
for k in range(16):
    play_melody(c, f"{k + 1}回目", P, 4, "reel", key=(KJ if k == 15 else KM), density=min(0.5, 0.15 + 0.025 * k), seed=9600 + k)
c.FLUTE.at(c.s0["日の出"] * B, "E5:7")

# ---------- 夜明けの楽器（加わったら残る） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
DRO = [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 1, "d", ",")]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lvl = int(n.replace("回目", "")) if n.endswith("回目") else 17
    if n == "日の出":
        if i == 0:
            VC.at(b * B, "E2:7"); CB_.at(b * B, "E1:7,"); VA.at(b * B, "B3:7,"); VN.at(b * B, "G#4:7,"); strum(GT, b, B, "E", [(0, 6, "d", "!")]); DR[0].at(b * B, "C3:1!")
        continue
    if lvl >= 2:
        VC.at(b * B, f"{nm(near(r, 40))}:{B + 0.1}{'' if i == 0 else ','}")
        if lvl >= 3: CB_.at(b * B, f"{nm(near(r, 28))}:{B + 0.1},")
    if lvl >= 4:
        strum(GT, b, B, ch, DRO if lvl >= 13 else [(0, 2, "d", ","), (2, 2, "d", ",")])
    if lvl >= 7:
        d = DR[b % 2]
        d.bar(b, "C3:1! E3:0.5, E3:0.5, C3:1 E3:1," if lvl < 13 else "C3:0.5! E3:0.5, C3:0.5 E3:0.5, C3:0.5! E3:0.5, C3:0.5 E3:0.25, E3:0.25,")
    if lvl >= 10:
        VN.at(round(b * B + 0.05, 3), f"{nm(near(th, 64))}:{B},")
        if lvl >= 12: VA.at(round(b * B + 0.08, 3), f"{nm(near(fi, 57))}:{B - 0.05},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の096（第3版）。鐘の倍音が島に広がり、夜明け前の家々で人が目をさます。アン・ドロ型（4/4・♩=92）、E エオリア。笛が6小節の同じ短い節を16回くり返し、回ごとに夜明けの楽器が少しずつ加わる（2回目 チェロ、3回目 コントラバス、4回目 ギター、7回目 ボーラン、10回目 バイオリン、12回目 ビオラ、13回目から全員が細かく）。だんだん大きくなり、日がのぼる16回目だけ、同じ節が E の長調になる。",
       harm_scenes=None, tail_scene="日の出", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 3000, "rt": 3.0}}}
json.dump(air, open("/tmp/cel/w/air096.json", "w"), ensure_ascii=False)
