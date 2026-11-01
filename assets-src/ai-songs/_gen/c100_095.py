# ケルト・フルート100曲「銀の笛と百の夜」095 眠りを壊さない鐘 The Bell That Does Not Wake — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 鐘楼に着いたのは真夜中。島じゅうが眠っている。祖父の約束は「眠りを壊さずに、鐘を目覚めさせること」。
#   エイラは鐘を強く打たず、鐘のふちをそっと笛の息でなでるように、いちばん小さな音で鳴らす。聞こえるのは、鐘の高い倍音だけ。
# 調べ: 眠り。形: 眠りの調べ（16小節の子守歌を4回。4小節ごとに、鐘の高い倍音だけがそっと響く）。
# 拍子・速さ: 3/4・♩=50。旋法: F イオニアの5音（F・G・A・C・D）。
# 主役は笛（とても小さな笛）。伴奏の主役: 竪琴（低いやわらかな分散和音）とグロッケン（鐘の倍音だけ）。
#   ギター・ピアノ・パッド・弦・打楽器・2本目の笛は使わない。
# この曲だけ: 鐘の音（いちばん低い基音 F3・F4）を一度も鳴らさず、高い倍音（C6・F6・A6）だけで鐘を表す。
# 始まり: 竪琴の1音 → 終わり: 鐘の倍音だけ。
# 山: なし。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "095-the-bell-that-does-not-wake", "眠りを壊さない鐘", "The Bell That Does Not Wake", 50, 3, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.25, "rubato": 0.15})
K = Key("F", "major", 4)
CH16 = ["F", "F", "C", "F", "Dm", "F", "F", "C", "F", "F", "C", "F", "C", "C", "Dm", "F"]
SC = [("竪琴の1音", 2, "intro", ["F", "F"]), ("子守歌", 64, "verse", CH16 * 4), ("倍音だけ", 4, "outro", ["F"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("竪琴の1音", 0, 0.66), ("子守歌", 0, 0.64), ("子守歌", 32, 0.66), ("子守歌", 63, 0.6), ("倍音だけ", 0, 0.58)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="竪琴の1音", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
HP = [S.track(f"竪琴（低くやわらかく{j + 1}）", "harp", patch="folkHarp", volume=0.06, pan=-0.25 + 0.15 * j, reverb=0.6, sustain=1.8, barGain=G) for j in range(2)]
HPI = S.track("竪琴（始まりの1音）", "harp", patch="folkHarp", volume=0.14, pan=-0.2, reverb=0.65, sustain=2.4)
BELL = [S.track(f"鐘の倍音（グロッケン{j + 1}）", "bell", patch="glockenspiel", volume=0.022, pan=-0.3 + 0.3 * j, reverb=0.92, barGain=[0.7] * c.NB) for j in range(3)]

# ---------- 子守歌（16小節。1=F4。F・G・A・C・D だけ） ----------
M = ["5:2 3:1", "2:2 1:1", "2:1 3:1 5:1", "3:3", "6:2 5:1", "3:2 2:1", "1:1 2:1 3:1", "2:3",
     "5:2 6:1", "1':2 6:1", "5:1 3:1 2:1", "3:3", "2:2 3:1", "5:1 3:1 2:1", "1:2 6,:1", "1:3"]
play_melody(c, "子守歌", M * 4, 4, "air", key=K, density=0.1, seed=9501)

# ---------- 竪琴（低くやわらかな分散和音）と、鐘の倍音（基音は鳴らさない） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
HPI.at(0, "F3:6")
for b in range(c.s0["子守歌"], c.s0["倍音だけ"]):
    ch = S.chords[b]; r, th, fi = tri(ch)
    for q, m in enumerate((near(r, 41), near(fi, 48), near(th, 53))):
        HP[q % 2].at(round(b * B + q, 3), f"{nm(m)}:2{'' if q == 0 else ','}")
PART = [("C6", 0.0), ("F6", 0.35), ("A6", 0.8)]                             # 鐘の高い倍音（5度・オクターブ・3度）
for b in range(c.s0["子守歌"], c.s0["倍音だけ"], 4):
    for j, (m, dt) in enumerate(PART):
        BELL[j].at(round(b * B + dt, 3), f"{m}:6{',' if j else ''}")
s0 = c.s0["倍音だけ"]
for j, (m, dt) in enumerate(PART + [("C7", 1.4)]):
    BELL[j % 3].at(round(s0 * B + dt, 3), f"{m}:9{',' if j else ''}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の095（第3版）。真夜中の鐘楼。眠りを壊さずに鐘を目覚めさせる。3/4・♩=50、F の長調の5音。竪琴の1音で始まり、竪琴の低くやわらかな分散和音の上で、とても小さな笛が16小節の子守歌を4回。4小節ごとに、鐘の高い倍音（C6・F6・A6）だけがグロッケンでそっと響く。鐘の基音は一度も鳴らさない。山はなく、最後は鐘の倍音だけが残る。",
       harm_scenes=None, tail_scene="倍音だけ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 7.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 3000, "rt": 4.6}}}
json.dump(air, open("/tmp/cel/w/air095.json", "w"), ensure_ascii=False)
