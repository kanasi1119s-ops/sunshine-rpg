# ケルト・フルート100曲「銀の笛と百の夜」004 嵐の前の凪 Calm Before the Gale — 第2版（2026-10-28）
# イメージ: 風がぴたりと止まった夕空。海も鳥も息をひそめる。空の色だけが、少しずつ変わっていく（明るい凪→くもり→暗い影）。
#   そして、すべての音が3秒だけ消える（嵐の前の、ほんとうの無音）。そのあと、また静かな凪が戻り、最後は波の音だけ。
# 形（台帳）: ドローンの瞑想。低い F の持続の上で、和音はほとんど変えず、旋法だけを変える（F リディア→ミクソリディア→エオリア→リディア）。
#   4/4・♩=48。始め：弦の持続／終わり：何も無い1拍→波。山なし。
# 編曲の表:
#   弦の息 : 弦の持続（F と C、上に高い倍音）とチェロの低い F
#   凪1    : ＋笛。竪琴がときどき1音（水面のきらめき）。リディア（明るく浮かぶ B♮）
#   凪2    : ミクソリディア（E♭が混ざり、空がくもる）。竪琴がゆっくりした分散和音
#   翳り   : エオリア（A♭・D♭、影が落ちる）。チェロが低い所で動く
#   無音   : 3秒だけ、すべての音が消える
#   凪3    : リディアに戻る。笛はやさしく、だんだん少なくなる
#   終わり : 弦の持続だけが消えていき、最後は波の音
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "004-calm-before-gale", "嵐の前の凪", "Calm Before the Gale", 48, 4, "F", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"rubato": 0.3, "human": 0.4})
S.scene("弦の息", 4, "intro", ["F", "F", "G/F", "F"])
S.scene("凪1", 16, "verse", ["F", "F", "G/F", "F", "F", "Am/F", "G/F", "F", "F", "Em/F", "G/F", "F", "F", "G/F", "F", "F"])
S.scene("凪2", 12, "verse", ["F", "Eb/F", "F", "Eb/F", "Bb/F", "F", "Eb/F", "F", "F", "Gm/F", "Eb/F", "F"])
S.scene("翳り", 8, "chorus", ["Fm", "Db/F", "Fm", "Eb/F", "Fm", "Db/F", "Eb/F", "Fm"])
S.scene("無音", 1, "break", ["Fm"])
S.scene("凪3", 12, "verse", ["F", "F", "G/F", "F", "F", "Am/F", "G/F", "F", "F", "F", "F", "F"])
S.scene("終わり", 4, "outro", ["F", "F", "F", "F"])
NAMES = ["弦の息", "凪1", "凪2", "翳り", "無音", "凪3", "終わり"]

c = make(S, NAMES,
         [("弦の息", 0, 0.62), ("凪1", 0, 0.62), ("凪1", 15, 0.66), ("凪2", 0, 0.66), ("凪2", 11, 0.7), ("翳り", 0, 0.72), ("翳り", 7, 0.74),
          ("無音", 0, 0.6), ("凪3", 0, 0.6), ("凪3", 11, 0.5), ("終わり", 0, 0.48), ("終わり", 3, 0.3)],
         {}, flute_gain={n: 1.25 for n in NAMES}, intro="弦の息", passing=True, tension=False)
CELLO = S.track("チェロ（低い F）", "strings", patch="cello", volume=0.1, pan=0.1, reverb=0.5, barGain=c.g())

K = S.key; KM = K.__class__("F", "mixolydian", 5); KA = K.__class__("F", "minor", 5)
play_melody(c, "凪1", ["R:2 5:2", "3:4", "4:2 3:1 2:1", "3:4", "R:2 5:2", "6:3 5:1", "4:2 5:1 6:1", "5:4",
                       "R:2 1':2", "7:3 6:1", "5:2 4:1 3:1", "2:4", "R:2 3:1 4:1", "5:3 4:1", "3:2 2:1 1:1", "1:4"], 4, "air", density=0.7, seed=401)
play_melody(c, "凪2", ["R:2 1:1 2:1", "3:3 4:1", "5:4", "7:2 6:1 5:1", "4:2 5:1 6:1", "7:4", "6:2 5:1 4:1", "5:4",
                       "R:2 3:1 4:1", "5:2 7:2", "6:3 4:1", "5:4"], 4, "air", key=KM, density=0.8, seed=402)
play_melody(c, "翳り", ["R:2 5:2", "6:3 5:1", "4:2 3:2", "2:4", "R:2 1:1 2:1", "3:3 2:1", "7,:2 1:2", "1:4"], 4, "air", key=KA, density=0.8, seed=403)
play_melody(c, "凪3", ["R:2 5:2", "3:4", "4:3 3:1", "2:4", "R:2 5:2", "6:2 5:2", "4:3 2:1", "1:4", "R:4", "5,:2 1:2", "1:4", "R:4"], 4, "air", density=0.6, seed=404)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b].split("/")[0]
    if n == "無音": continue
    hold = not (n == "終わり" and i == 3)
    if hold:
        v = voice(ch, 60, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        CELLO.bar(b, "F2:4")
    if n == "凪1" and i % 4 == 2: c.HARP.bar(b, f"R:2 {nm(tones(ch, 'C5', 'C6')[1])}:2")
    if n == "凪2": c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "F3", "F5")[:4]))
    if n == "翳り":
        CELLO.bar(b, f"{nm(tones(ch, 'C3', 'C4')[0])}:2 {nm(tones(ch, 'C3', 'C4')[1])}:2")
        c.HARP.bar(b, f"{nm(tones(ch, 'F3', 'F4')[0])}:4")
    if n == "凪3" and i % 4 == 0: c.HARP.bar(b, f"R:2 {nm(tones(ch, 'C5', 'C6')[2])}:2")
# 無音：前の小節から鳴っている音も、無音の小節の頭で止める（3秒＝2.4拍）。その後は弦がそっと戻る
SB = c.s0["無音"]
c.SIL.add(SB, 0, 2.4)
v = voice("F", 60, 3, spread=True)
for j in range(3): c.STR[j].at(SB * B + 2.4, f"{nm(v[j])}:1.6")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.25 --side-hpf 220",
       "ケルト・フルート100曲の004（第2版）。風が止まった夕空。低い F の持続の上で旋法だけが変わる（リディア→ミクソリディア→エオリア→リディア）。4/4・♩=48。途中で3秒だけ、すべての音が消える。最後は波の音。",
       harm_scenes=None, tail_scene="終わり", fill=False, pads=True, pad_scenes=["凪1", "凪2", "翳り", "凪3"])
