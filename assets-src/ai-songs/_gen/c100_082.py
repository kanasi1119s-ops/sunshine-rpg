# ケルト・フルート100曲「銀の笛と百の夜」082 足跡 Footprints — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 峠をこえた雪原に、古い足跡がてんてんと続いている。祖父の足跡かもしれない。エイラはそれをたどって歩くが、
#   降りつづく雪が、足跡をひとつ、またひとつと消していく。最後には、自分の吐く白い息のような、笛の1音だけが残る。
# 調べ: 悲しみ。形: 足跡が雪に消えていく（8小節の節を8回。回ごとに、句の頭の音が1つずつ欠ける）。
# 拍子・速さ: 3/4・♩=52。旋法: A エオリア。
# 主役は笛（細い笛。E4〜E5）。伴奏の主役: チェロ独奏（前奏と、笛の下の歌う低音）。
#   竪琴・ギター・ピアノ・パッド・ほかの弦・打楽器・2本目の笛は使わない。
# この曲だけ: 各小節の頭の音（足跡）が、回るたびに1つずつ欠けて休符になる（1回目は全部、8回目は最後の小節の頭だけが残る）。
# 始まり: チェロ → 終わり: 笛の最後の1音だけ。
# 山: 前半（2〜3回目）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "082-footprints", "足跡", "Footprints", 52, 3, "A", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("A", "minor", 4)
CH8 = ["Am", "Em", "Am", "G", "Am", "F", "Dm", "Am"]
SC = [("チェロ", 4, "intro", ["Am", "Em", "F", "Am"]), ("足跡", 64, "verse", CH8 * 8), ("最後の1音", 4, "outro", ["Am"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("チェロ", 0, 0.72), ("足跡", 0, 0.74), ("足跡", 12, 0.84), ("足跡", 24, 0.8), ("足跡", 63, 0.62), ("最後の1音", 0, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="チェロ", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# チェロの旋律（043: 0.025・gainDb 4・×1.4 で笛と同じくらい）。ここは笛の下で歌うので ×1.2
VC = S.track("チェロ独奏", "strings", patch="cello", volume=0.025, gainDb=4, pan=-0.15, reverb=0.65, release=0.5, barGain=[round(x * (1.4 if b < 4 else 1.2), 3) for b, x in enumerate(G)])

# ---------- 足跡の節（8小節。1=A4。小節の頭の音が「足跡」） ----------
M = ["1:1 2:1 3:1", "5:2 4:1", "3:1 2:1 1:1", "7,:3", "1:1 3:1 5:1", "6:2 5:1", "4:1 3:1 2:1", "1:3"]
s0 = c.s0["足跡"]
for k in range(8):
    bars = []
    for j, s_ in enumerate(M):
        toks = s_.split()
        if j < k:                                                    # 頭の音が消える
            toks[0] = "R:" + toks[0].split(":")[1]
        bars.append(" ".join(toks))
    play_melody(c, "足跡", ["R:3"] * (8 * k) + bars + ["R:3"] * (8 * (7 - k)), 4, "air", key=K, density=max(0.0, 0.15 - 0.015 * k), seed=8200 + k)
c.FLUTE.at((c.s0["最後の1音"]) * B, "A4:9")

# ---------- チェロ独奏（前奏の歌と、笛の下の歌う低音） ----------
CI = ["A2:2 C3:1", "B2:2 G2:1", "F2:2 A2:1", "A2:3"]
for j, s_ in enumerate(CI): VC.bar(j, s_)
ROOT = {"Am": 45, "Em": 40, "G": 43, "F": 41, "Dm": 38}
for b in range(s0, s0 + 64):
    ch = S.chords[b]; r = ROOT[ch]; th = r + (3 if ch.endswith("m") else 4)
    i = b - s0
    VC.bar(b, f"{nm(r)}:2{'' if i % 8 == 0 else ','} {nm(th)}:1," if (i // 8) % 2 == 0 else f"{nm(r)}:1, {nm(r + 7)}:1, {nm(th + 12 if th + 12 <= 57 else th)}:1,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の082（第3版）。峠をこえた雪原に、古い足跡がてんてんと続く。3/4・♩=52、A エオリア。チェロ独奏の前奏のあと、細い笛が8小節の節を8回吹く。チェロは笛の下で歌う低音。回るたびに、各小節の頭の音（足跡）が1つずつ欠けて休符になり、降る雪が足跡を消していくように、節がまばらになっていく。山は前半。最後は笛の1音だけが残る。",
       harm_scenes=None, tail_scene="最後の1音", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -44, "hp": 180, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2600, "rt": 4.2}}}
json.dump(air, open("/tmp/cel/w/air082.json", "w"), ensure_ascii=False)
