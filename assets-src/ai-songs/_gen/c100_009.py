# ケルト・フルート100曲「銀の笛と百の夜」009 星を数える Counting the Stars — 第2版（2026-10-28）
# イメージ: 甲板に寝ころんで夜空を見上げる。ひとつ、またひとつ星が見えてくる。最初の星（ひとつの音）から、満天の星まで。
#   見えた星は消えずに残り、またたき続ける＝同じ節を、楽器が2小節ずつ遅れて順に歌い出す（輪唱）。最後に全部が静止する。
# 形（台帳）: 輪唱（笛→グロッケン→竪琴の倍音→ピチカート→笛の和声）。9/8（付点4分＝48）。C リディア（F♯のきらめき）。山なし・音数だけが増える。
# 編曲の表:
#   一つ目 : グロッケンの1音だけ（最初の星）
#   星1    : 笛が節を歌う（低い C の持続がうすく支える）
#   星2    : ＋グロッケンが2小節遅れて同じ節（1オクターブ上）
#   星3    : ＋竪琴の倍音（高い音）が、さらに2小節遅れて
#   星4    : ＋ピチカートが低い所で
#   満天   : ＋笛の和声と弦の高い持続。すべての星がまたたく
#   静止   : すべてが1つの和音で止まり、消えていく
import sys
from c100_common import *
from c100_v2 import *

BPM = 144   # 8分音符＝144（付点4分＝48）
S = Song("C100", "009-counting-the-stars", "星を数える", "Counting the Stars", BPM, 9, "C", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
CH12 = (["Cmaj7", "Cmaj7", "D/C", "D/C"] * 3)
S.scene("一つ目", 2, "intro", ["Cmaj7", "Cmaj7"])
S.scene("星1", 12, "verse", CH12)
S.scene("星2", 12, "verse", CH12)
S.scene("星3", 12, "verse", CH12)
S.scene("星4", 12, "verse", CH12)
S.scene("満天", 12, "chorus", CH12)
S.scene("静止", 4, "outro", ["Cmaj7"] * 4)
NAMES = ["一つ目", "星1", "星2", "星3", "星4", "満天", "静止"]

c = make(S, NAMES,
         [("一つ目", 0, 0.6), ("星1", 0, 0.62), ("星2", 0, 0.64), ("星3", 0, 0.67), ("星4", 0, 0.7), ("満天", 0, 0.74), ("満天", 11, 0.74),
          ("静止", 0, 0.62), ("静止", 3, 0.4)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="一つ目", passing=True, tension=False)
GLOCK = S.track("星（グロッケン）", "bell", patch="glockenspiel", volume=0.032, pan=0.4, reverb=0.75, barGain=c.g())
PIZZ = S.track("星（ピチカート）", "strings", patch="pizzicato", volume=0.06, pan=-0.4, reverb=0.5, barGain=c.g())
CELLO = S.track("低い C", "strings", patch="cello", volume=0.07, pan=0.0, reverb=0.5, barGain=c.g())

TH = ["1:2 2:1 3:2 5:1 6:3", "5:2 3:1 2:3 1:3", "3:2 5:1 7:2 6:1 5:3", "4:2 5:1 3:3 2:3",
      "1':2 7:1 5:2 3:1 5:3", "6:2 5:1 4:3 2:3", "3:2 4:1 5:2 7:1 1':3", "7:3 5:3 3:3"]
s_start = c.s0["星1"]; s_end = c.s0["静止"]
def canon(track, entry_bar, oct_, key=None, octup=0):
    """entry_bar から、節（8小節）をくり返して静止の前まで置く"""
    key = key or S.key; B = S.beats; b = entry_bar; j = 0
    while b < s_end:
        for t, L, m in mel_events(key, TH[j % 8], oct_, b * B):
            m = m + 12 * octup
            track.at(round(t, 3), f"{nm(m)}:{L}")
        b += 1; j += 1
# 笛（主役）：装飾つきで、星1から満天まで
play_melody(c, "星1", TH + TH[:4], 5, "air", density=0.5, seed=901)
play_melody(c, "星2", TH[4:] + TH, 5, "air", density=0.7, seed=902)
play_melody(c, "星3", TH + TH[:4], 5, "air", density=0.7, seed=903)
play_melody(c, "星4", TH[4:] + TH, 5, "air", density=0.8, seed=904)
play_melody(c, "満天", TH + ["1':3 7:3 5:3", "3:9", "R:9", "R:9"], 5, "air", density=0.9, seed=905)
canon(GLOCK, c.s0["星2"] + 2, 6)
canon(c.HARP2, c.s0["星3"] + 4, 5)
canon(PIZZ, c.s0["星4"] + 6, 4)
GLOCK.bar(c.s0["一つ目"], "G6:9")          # 最初の星

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    if n == "一つ目": continue
    CELLO.bar(b, "C2:9" if n != "静止" or i < 3 else "R:9")
    if n in ("満天", "静止"):
        v = voice(ch.split("/")[0] if "/" not in ch else "D", 67, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9" if not (n == "静止" and i == 3) else "R:9")
    if n == "静止" and i == 0:
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (48, 55, 60, 64, 67, 71, 74, 76, 79)))
rich(c, choir_scenes=["満天"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.25 --side-hpf 220",
       "ケルト・フルート100曲の009（第2版）。甲板で星を数える。9/8・付点4分＝48、C リディア。輪唱：同じ節を、笛→グロッケン→竪琴の倍音→ピチカートが2小節ずつ遅れて順に歌い出し、満天の星になって静止する。",
       harm_scenes=None, tail_scene="静止", fill=False, pads=True, pad_scenes=["星3", "星4", "満天"])
