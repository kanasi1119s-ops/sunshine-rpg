# ケルト・フルート100曲「銀の笛と百の夜」015 麦のゆりかご Cradle of the Barley — 第2版（2026-10-28）
# イメージ: 麦畑の午後。風にゆれる麦の穂が、ゆりかごのように見える。羊飼いの小屋で、母親が子を寝かしつける子守歌。
#   ゆれはだんだんゆっくりになり、最後は子が眠りに落ちた瞬間に、歌が途中で止まる（最後の小節が2拍だけ）。
# 形（台帳）: 子守歌（主題と小さな変奏）。3/4・♩=56。F イオニア。始め：竪琴／終わり：眠り（途中で止まる）。山なし。
# 編曲の表:
#   ゆれ   : 竪琴のゆりかごのゆれ（低→高→中）だけ
#   歌1    : 笛が子守歌（A 8小節＋B 8小節）＋竪琴＋ナイロンギターのやわらかい和音
#   歌2    : 笛が少し飾って。チェロがやさしく低い所を支える
#   歌3    : 弦がうすく入る。グロッケンが小さく木霊（オルゴールのように）
#   歌4    : 楽器が少しずつ減る（だんだん眠くなる）
#   眠り   : 竪琴のゆれがゆっくりになり、笛の最後の句が途中で止まる
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "015-cradle-of-the-barley", "麦のゆりかご", "Cradle of the Barley", 54, 3, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.3})
AC = ["F", "Bb", "F", "C", "F", "Dm", "C", "F"]
BC = ["Bb", "C", "Dm", "C", "Bb", "F", "C", "F"]
S.scene("ゆれ", 4, "intro", ["F", "F", "Bb", "F"])
S.scene("歌1", 16, "verse", AC + BC)
S.scene("歌2", 16, "verse", AC + BC)
S.scene("歌3", 16, "verse", AC + BC)
S.scene("歌4", 16, "verse", AC + BC)
S.scene("眠り", 6, "outro", ["F", "Bb", "F", "C", "F", "F"])
NAMES = ["ゆれ", "歌1", "歌2", "歌3", "歌4", "眠り"]
S.extra["rit"] = {"bar": 4 + 16 * 4 + 1, "bars": 6, "to": 0.72, "aTempo": False}

c = make(S, NAMES,
         [("ゆれ", 0, 0.6), ("歌1", 0, 0.62), ("歌2", 0, 0.66), ("歌3", 0, 0.68), ("歌3", 15, 0.64), ("歌4", 0, 0.58), ("眠り", 0, 0.5), ("眠り", 5, 0.35)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="ゆれ", passing=True, tension=False)
GT = S.track("ナイロンギター", "guitar", patch="nylonGuitar", volume=0.085, pan=0.35, reverb=0.4, barGain=c.g())
GT2 = S.track("ナイロンギター2", "guitar", patch="nylonGuitar", volume=0.07, pan=0.4, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.15, reverb=0.45, barGain=c.g())
GLOCK = S.track("オルゴールの木霊", "bell", patch="glockenspiel", volume=0.022, pan=0.4, reverb=0.75, barGain=c.g())

LA = ["5:2 3:1", "4:2 2:1", "3:2 1:1", "2:3", "5:2 3:1", "6:2 4:1", "3:1 2:1 7,:1", "1:3"]
LB = ["1':2 6:1", "7:2 5:1", "6:2 4:1", "5:3", "6:1.5 5:0.5 4:1", "3:2 5:1", "4:1 3:1 2:1", "1:3"]
play_melody(c, "歌1", LA + LB, 4, "air", density=0.5, seed=1501)
play_melody(c, "歌2", LA + LB, 4, "air", density=0.9, seed=1502)
play_melody(c, "歌3", LA + LB, 4, "air", density=0.7, seed=1503)
play_melody(c, "歌4", LA + LB[:7] + ["1:3"], 4, "air", density=0.5, seed=1504)
play_melody(c, "眠り", ["5:2 3:1", "4:2 2:1", "3:3", "R:3", "5:2 3:1", "4:2 R:1"], 4, "air", density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "F3", "F5")
    last = (n == "眠り" and i == 5)
    # 竪琴のゆりかご：低→高→中
    c.HARP.bar(b, f"{nm(r)}:1 {nm(t[3 % len(t)])}:1 {nm(t[2])}:1" if not last else f"{nm(r)}:1 {nm(t[2])}:1 R:1")
    if n in ("歌1", "歌2", "歌3") or (n == "歌4" and i < 8):
        GT.bar(b, f"R:1 {nm(t[1])}:2"); GT2.bar(b, f"R:1 {nm(t[2])}:2")
    if n in ("ゆれ", "歌1", "歌2", "歌3", "歌4"): CELLO.bar(b, f"{nm(r)}:3")
    if n == "ゆれ":   # 午後の光：うすい弦と、竪琴の高いゆれ（ゆりかごの上の麦の穂）
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
        c.HARP2.bar(b, f"R:1 {nm(t[2] + 12)}:1 {nm(t[1] + 12)}:1")
    if n in ("歌1", "歌2"):
        v = voice(ch, 53, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:3")
    if n == "歌3":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
        if i % 4 == 3: GLOCK.bar(b, f"R:1 {nm(tones(ch, 'C6', 'C7')[0])}:2")
    if n in ("歌4", "眠り") and not last:
        v = voice(ch, 55, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:3")
# 最後の小節は2拍だけ：3拍目から先は、全部の音を止める
c.SIL.add(c.s0["眠り"] + 5, 2, 3)
rich(c, choir_scenes=["歌3"], pulse_scenes=["歌2", "歌3", "歌4"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の015（第2版）。麦畑の午後の子守歌。3/4・♩=54、F イオニア。竪琴のゆりかごのゆれの上で、主題と小さな変奏。だんだんゆっくりになり、最後は眠りに落ちた所で歌が途中で止まる（最後の小節が2拍だけ）。",
       harm_scenes=None, tail_scene="眠り", fill=False, pads=True, pad_scenes=["歌1", "歌2", "歌3", "歌4"], floor=True)
