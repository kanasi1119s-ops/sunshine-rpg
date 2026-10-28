# ケルト・フルート100曲「銀の笛と百の夜」004 嵐の前の凪 Calm Before the Gale（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 風が止まった夕空。船乗りが息をひそめて空を見る。曲のまんなかで、すべての楽器が1小節ぶん息を止め（波の響きだけが残る）、
#       そのあとまた、ほとんど動かない長い音が続く。静止の長い呼吸。始め：弦の持続／終わり：何もない1小節→波。山なし。
# 型: ほとんど動かない長音と、ごく短い揺らぎ（2音を行き来する）。笛は低めの音域（C5〜C6のやわらかい所）。
# 強さ: 弦の息(pp)→凪1(pp)→凪2(p)→静止(休み)→凪3(p→pp)→終わり(ppp→無)
import sys
from c100_common import *

S = Song("C100", "004-calm-before-gale", "嵐の前の凪", "Calm Before the Gale", 48, 4, "F", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("弦の息", 4, "intro", ["Fmaj7", "Fmaj7", "Am7", "Fmaj7"])
S.scene("凪1", 12, "verse", ["Fmaj7", "G", "Am7", "Fmaj7", "Dm7", "Am7", "G", "Fmaj7", "Em7", "Am7", "G", "Fmaj7"])
S.scene("凪2", 12, "verse", ["Dm7", "Fmaj7", "G", "Am7", "Fmaj7", "C", "G", "Fmaj7", "Am7", "Dm7", "G", "Fmaj7"])
S.scene("静止", 1, "break", ["Fmaj7"])
S.scene("凪3", 12, "verse", ["Fmaj7", "Am7", "G", "Fmaj7", "Dm7", "G", "Am7", "Fmaj7", "Em7", "Am7", "G", "Fmaj7"])
S.scene("終わり", 8, "outro", ["Fmaj7", "Fmaj7", "Am7", "Fmaj7", "Fmaj7", "Fmaj7", "Fmaj7", "Fmaj7"])
NAMES = ["弦の息", "凪1", "凪2", "静止", "凪3", "終わり"]

c = make(S, NAMES,
         [("弦の息", 0, 0.72), ("凪1", 0, 0.62), ("凪2", 0, 0.7), ("凪2", 11, 0.74), ("静止", 0, 0.6), ("凪3", 0, 0.66), ("凪3", 11, 0.55), ("終わり", 0, 0.5), ("終わり", 7, 0.3)],
         {"凪1": 0.6, "凪2": 0.6, "凪3": 0.62, "終わり": 0.8},
         flute_gain={"凪1": 1.4, "凪2": 1.3, "凪3": 1.3, "終わり": 1.1}, intro="弦の息", passing=True)
BELL = S.track("ベル", "bell", patch="glockenspiel", volume=0.03, pan=0.35, reverb=0.7, barGain=c.g())

# ---------- 旋律（F リディア。長音と、ごく短い揺らぎ） ----------
put_melody(c, "凪1", [
    ["1:4", "R:2 5,:2", "1:3 2:0.5 1:0.5", "R:4"],
    ["5,:4", "6,:3 5,:0.5 6,:0.5", "R:2 1:2", "1:4"],
    ["3:4", "R:2 2:1 1:1", "5,:4", "R:4"]], 5)
put_melody(c, "凪2", [
    ["1:2 3:2", "4:4", "3:3 2:0.5 3:0.5", "R:4"],
    ["5:4", "4:2 3:2", "2:3 1:1", "R:4"],
    ["1:4", "3:3 R:1", "2:4", "R:4"]], 5)
put_melody(c, "凪3", [
    ["R:2 5,:2", "1:4", "2:3 1:0.5 2:0.5", "1:4"],
    ["6,:4", "5,:3 6,:0.5 5,:0.5", "1:4", "R:4"],
    ["3:4", "2:4", "1:3 7,:1", "1:4"]], 5)
put_bars(c, "終わり", ["R:4", "1:4", "R:4", "5,:4", "R:4", "1:4", "R:4", "R:4"], 5)

# ---------- 伴奏（動かない。長い和音と、ひとつずつの音） ----------
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6")
    if n == "静止": continue                                   # 全パートが1小節ぶん息を止める
    if n == "弦の息":
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        if i >= 2: c.HARP.bar(b, f"{nm(t[0])}:4")
    elif n in ("凪1", "凪2", "凪3"):
        c.HARP.bar(b, f"{nm(t[0])}:4" if i % 2 == 0 else f"{nm(t[2])}:2 R:2")
        if i % 4 == 3: c.HARP2.bar(b, f"R:2 {nm(t[-2])}:2")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 62, 3, spread=True)
        if n != "凪1" or i >= 4:
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if n == "凪2" and i % 4 == 2: BELL.bar(b, f"{nm(tones(ch, 'C6', 'C7')[1])}:4")
    elif n == "終わり":
        if i in (0, 3): c.HARP.bar(b, f"{nm(t[0])}:4")
        if i < 6:
            v = voice(ch, 62, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i == 4: BELL.bar(b, f"{nm(tones(ch, 'C6', 'C7')[2])}:4")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の004。風が止まった夕空。F リディア・48。ほとんど動かない長音と短い揺らぎ。曲のまんなかで全パートが1小節ぶん息を止める。",
       harm_scenes=["凪2", "凪3"], tail_scene="終わり", tail_keep=6, skip_scenes=["静止"])
