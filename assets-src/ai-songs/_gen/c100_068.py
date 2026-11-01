# ケルト・フルート100曲「銀の笛と百の夜」068 笛を聴く夜 The Night They Listened — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 祭りの前の夜がふけ、村人たちに頼まれて、エイラが初めて村で笛を吹く。祖父に教わったエア。はじめは笛ひとり。
#   聴いていた村人が、ひとり、またひとりと、そっと自分の楽器で音を足していく（ギター → フィドル → アコーディオン）。
#   最後は全員で同じ節を歌い、静かな和音で終わる。
# 調べ: 悲しみ。形: エア（16小節）を5回。回ごとに村人の楽器が1つずつ加わる（無伴奏 → ギター → フィドル → アコーディオン → 全員）。
# 拍子・速さ: 3/4・♩=60（ゆれを大きく）。旋法: G エオリア。
# 主役は笛（独奏の笛）。伴奏: 無伴奏 → 村人の楽器が1つずつ（ナイロン弦ギター・フィドル・アコーディオン）。
#   竪琴・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 聴いていた村人が1人ずつ、そっと音を足していく（前の回の楽器は残ったまま、次の楽器が加わる）。
# 始まり: 笛ひとり → 終わり: 全員の静かな和音。
# 山: 終盤（全員）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "068-the-night-they-listened", "笛を聴く夜", "The Night They Listened", 60, 3, "G", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.3})
K = Key("G", "minor", 4)
CH16 = ["Gm", "Gm", "Gm", "Dm", "Eb", "Cm", "Bb", "F", "Gm", "F", "F", "Bb", "Cm", "Gm", "F", "Gm"]
SC = [("笛ひとり", 16, "intro", CH16), ("ギター", 16, "verse", CH16), ("フィドル", 16, "verse", CH16), ("アコーディオン", 16, "verse", CH16),
      ("全員", 16, "chorus", CH16), ("静かな和音", 4, "outro", ["Gm"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("笛ひとり", 0, 0.72), ("ギター", 0, 0.7), ("フィドル", 0, 0.72), ("アコーディオン", 0, 0.76), ("全員", 0, 0.82), ("全員", 12, 0.9), ("静かな和音", 0, 0.7)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="笛ひとり", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
B = S.beats
G = c.g()
JOIN = {"ギター": 1, "フィドル": 2, "アコーディオン": 3, "全員": 4, "静かな和音": 4}
GB = S.track("ギター（低音）", "guitar", patch="nylonGuitar", volume=0.014, pan=-0.3, reverb=0.35, barGain=G)
GF = [S.track(f"ギター（指{j + 1}）", "guitar", patch="nylonGuitar", volume=0.007, pan=-0.35 + 0.1 * j, reverb=0.35, barGain=G) for j in range(2)]
FD = S.track("フィドル（長い音）", "strings", patch="violin", volume=0.03, gainDb=3, pan=0.3, reverb=0.55, release=0.6, barGain=G)
AC = [S.track(f"アコーディオン{j + 1}", "accordion", volume=0.05, pan=0.12 + 0.06 * j, reverb=0.45, barGain=[round(x * 0.45, 3) for x in G]) for j in range(3)]

# ---------- エア（16小節。1=G4） ----------
M = ["5:2 4:1", "3:2 2:1", "1:1 2:1 3:1", "5:3", "6:2 5:1", "4:1 3:1 2:1", "3:3", "2:3",
     "5:2 6:1", "7:2 1':1", "2':2 1':1", "7:1 6:1 5:1", "4:2 5:1", "3:1 2:1 1:1", "2:2 7,:1", "1:3"]
for k, sc in enumerate(("笛ひとり", "ギター", "フィドル", "アコーディオン", "全員")):
    play_melody(c, sc, M, 4, "air", key=K, density=(0.35, 0.25, 0.25, 0.3, 0.4)[k], seed=6800 + k)
s0 = s["静かな和音"]
c.FLUTE.at(s0 * B, "D5:10")

# ---------- 村人の楽器（加わったら残る） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(s["ギター"], s["静かな和音"]):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    j_ = JOIN[n]
    lo = near(r, 38)
    GB.at(b * B, f"{nm(lo)}:2{'' if i % 4 == 0 else ','}")
    for q, m in enumerate((near(fi, lo + 1), near(th, lo + 12), near(fi, lo + 12), near(r, lo + 13), near(th, lo + 12))):
        GF[q % 2].at(round(b * B + 0.5 * (q + 1), 3), f"{nm(m)}:0.5,")
    if j_ >= 2 and i % 2 == 0:                                 # フィドル：2小節ごとに、和音の3度を長く（全員では1オクターブ上も）
        FD.at(round(b * B + 0.1, 3), f"{nm(near(th, 62))}:{2 * B - 0.2},")
    if j_ >= 3 and i % 2 == 0:                                 # アコーディオン：2小節ごとに長い和音（そっと）
        for q, m in enumerate((near(r, 55), near(th, 55), near(fi, 55))):
            AC[q].at(round(b * B + 0.05 * q, 3), f"{nm(m)}:{2 * B - 0.1},")
    if j_ >= 4 and i % 2 == 1:
        FD.at(round(b * B + 0.1, 3), f"{nm(near(fi, 67))}:{B - 0.2},")
# 静かな和音（G・D・B♭・A）
for q, (tr, m) in enumerate(((GB, "G2"), (GF[0], "D3"), (GF[1], "Bb3"), (AC[0], "G3"), (AC[1], "Bb3"), (AC[2], "D4"), (FD, "A4"))):
    tr.at(round(s0 * B + 0.12 * q, 3), f"{m}:{round(11.5 - 0.12 * q, 2)}{'' if q == 0 else ','}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.28 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の068（第3版）。祭りの前の夜、エイラが村で初めて笛を吹く。3/4・♩=60、G エオリア。祖父に教わった16小節のエアを5回。はじめは笛ひとり（無伴奏）。聴いていた村人が、回ごとにひとりずつ、そっと楽器を足していく（ナイロン弦ギター → フィドルの長い音 → アコーディオンの長い和音 → 全員）。終盤の全員が山で、最後は全員の静かな和音。",
       harm_scenes=None, tail_scene="静かな和音", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.2}}}
json.dump(air, open("/tmp/cel/w/air068.json", "w"), ensure_ascii=False)
