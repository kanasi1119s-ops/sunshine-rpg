# ケルト・フルート100曲「銀の笛と百の夜」023 水面の光 Light on the Water — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 昼の川面に、日の光が細かくきらめく。きらめきは、笛の細かい装飾音（カット・ロール）の雨になって降る。
#   はじめは高い所でちらちら光り、だんだん深い所へ光がしずんでいって、最後は川底の低い音で終わる。
# 形（台帳）: リール（装飾音の雨）AABB。4/4・♩=100。E ミクソリディア（D♮）。始め：高い音のきらめき／終わり：低い音。2周目と最後に山。
# 編曲の表:
#   きらめき: グロッケンと竪琴の高い音の粒だけ
#   1周目  : 笛（A は高い所、B は少し低く）＋竪琴の3音オスティナート＋ピチカート
#   2周目  : ＋弦＋チェロ。笛の装飾がいちばん多い（山）
#   3周目  : 笛が低い所へ。竪琴も低くなり、光が川底へ沈む（最後の山）
#   川底   : 低い長い音で終わる
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "023-light-on-the-water", "水面の光", "Light on the Water", 100, 4, "E", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["E", "E", "A", "D", "E", "E", "D", "E"]
BC = ["A", "A", "D", "E", "A", "A", "D", "E"]
S.scene("きらめき", 4, "intro", ["E", "E", "D", "E"])
S.scene("1周目", 32, "verse", AC * 2 + BC * 2)
S.scene("2周目", 32, "chorus", AC * 2 + BC * 2)
S.scene("3周目", 32, "verse", AC * 2 + BC * 2)
S.scene("川底", 4, "outro", ["E", "D", "E", "E"])
NAMES = ["きらめき", "1周目", "2周目", "3周目", "川底"]

c = make(S, NAMES,
         [("きらめき", 0, 0.62), ("1周目", 0, 0.68), ("2周目", 0, 0.78), ("2周目", 28, 0.92), ("3周目", 0, 0.78), ("3周目", 28, 0.88), ("川底", 0, 0.7), ("川底", 3, 0.45)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="きらめき", passing=True, tension=False)
GLOCK = S.track("きらめき（グロッケン）", "bell", patch="glockenspiel", volume=0.028, pan=0.35, reverb=0.7, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.06, pan=-0.35, reverb=0.35, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.2, reverb=0.4, barGain=c.g())

A = ["5:0.5 1':0.5 2':0.5 1':0.5 7:0.5 5:0.5 6:0.5 7:0.5", "1':0.5 5:0.5 3:0.5 5:0.5 1':0.5 2':0.5 3':1",
     "2':0.5 1':0.5 7:0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5", "6:0.5 4:0.5 2:0.5 4:0.5 6:1 5:1",
     "5:0.5 1':0.5 2':0.5 1':0.5 7:0.5 5:0.5 6:0.5 7:0.5", "1':0.5 5:0.5 3:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5",
     "3':0.5 2':0.5 1':0.5 7:0.5 6:0.5 4:0.5 2:0.5 7,:0.5", "1:1 5,:0.5 7,:0.5 1:2"]
Bp = ["3:0.5 4:0.5 5:0.5 3:0.5 2:0.5 3:0.5 4:0.5 2:0.5", "1:0.5 2:0.5 3:0.5 1:0.5 7,:1 5,:1",
      "6,:0.5 7,:0.5 1:0.5 2:0.5 3:0.5 4:0.5 5:0.5 6:0.5", "7:0.5 6:0.5 5:0.5 4:0.5 5:1 2:1",
      "3:0.5 4:0.5 5:0.5 3:0.5 2:0.5 3:0.5 4:0.5 2:0.5", "1:0.5 2:0.5 3:0.5 1:0.5 7,:1 5,:1",
      "3':0.5 2':0.5 1':0.5 7:0.5 6:0.5 4:0.5 2:0.5 7,:0.5", "1:1 5,:0.5 7,:0.5 1:2"]
play_melody(c, "1周目", A + A + Bp + Bp, 4, "reel", density=0.7, seed=2301)
play_melody(c, "2周目", A + A + Bp + Bp, 4, "reel", density=1.3, seed=2302)
# 3周目：光が沈む＝A を低い所で（1オクターブ下げても笛の低い所に収まる形に）
Alow = [x.replace("3':", "3:").replace("2':", "2:").replace("1':", "1:") for x in A]
play_melody(c, "3周目", A[:4] + Alow[4:] + Bp + Bp, 4, "reel", density=1.0, seed=2303)
play_melody(c, "川底", ["1:4", "7,:2 6,:2", "5,:4", "R:4"], 4, "air", density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "きらめき":
        hi = tones(ch, "E5", "E7")
        GLOCK.bar(b, " ".join(f"{nm(hi[(i * 3 + q) % len(hi)])}:0.5" for q in (0, 2, 4)) + " R:2.5")
        c.HARP2.bar(b, "R:1.5 " + " ".join(f"{nm(hi[(i + q) % len(hi)] - 12)}:0.5" for q in (1, 3, 5)) + " R:1")
        continue
    if n == "川底":
        c.HARP.bar(b, f"{nm(r)}:4"); CELLO.bar(b, f"{nm(r)}:4" if i < 3 else "R:4")
        v = voice(ch, 50, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4" if i < 3 else "R:4")
        continue
    lowp = (n == "3周目" and i >= 4)
    base = "E3" if lowp else "E4"
    harp_ostinato(c.HARP, b, B, tones(ch, base, "E6")[:3])
    PIZZ.bar(b, f"{nm(r + 12)}:0.5 R:0.5 {nm(r + 19)}:0.5 R:0.5 {nm(r + 12)}:0.5 R:0.5 {nm(r + 19)}:0.5 R:0.5")
    if n in ("2周目", "3周目"):
        v = voice(ch, 52 if lowp else 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        CELLO.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    if n == "2周目" and i % 4 == 0: GLOCK.bar(b, f"{nm(tones(ch, 'E6', 'E7')[0])}:1 R:3")
rich(c, choir_scenes=["2周目"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の023（第2版・明るく速めの曲）。昼の川面のきらめき。リール AABB、4/4・♩=100、E ミクソリディア。笛の細かい装飾音（カット・ロール）が光の雨になり、高い所から川底の低い音へ沈んでいく。",
       harm_scenes=None, tail_scene="川底", fill=False, pads=False)
