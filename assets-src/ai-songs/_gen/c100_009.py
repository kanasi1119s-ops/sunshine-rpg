# ケルト・フルート100曲「銀の笛と百の夜」009 星を数える Counting the Stars（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 甲板に寝ころんで夜空を見上げ、星を一つずつ数える。最初は一つ、だんだん増えて、最後は満天の星。そして全部が静止する。
# 型: 笛は001と同じく、一つ一つの音を4分音符で弾いてなめらかにつなぐ。星＝グロッケンと竪琴の高い音の点。点の数だけが場面ごとに増える（山なし）。
# 強さ: 一つ目の星(pp)→数える1(p)→数える2(p)→数える3(p→mp)→満天(mp)→静止(pp)
import sys
from c100_common import *

S = Song("C100", "009-counting-the-stars", "星を数える", "Counting the Stars", 50, 4, "C", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("一つ目の星", 4, "intro", ["Cmaj7", "D", "Cmaj7", "Cmaj7"])
S.scene("数える1", 12, "verse", ["Cmaj7", "D", "Em7", "Cmaj7", "Am7", "D", "G", "Cmaj7", "Em7", "D", "Am7", "Cmaj7"])
S.scene("数える2", 12, "verse", ["Am7", "Em7", "D", "G", "Cmaj7", "Bm7", "Em7", "D", "Am7", "D", "G", "Cmaj7"])
S.scene("数える3", 12, "chorus", ["Cmaj7", "D", "Em7", "Am7", "D", "G", "Cmaj7", "D", "Em7", "D", "G", "Cmaj7"])
S.scene("満天", 8, "chorus", ["Cmaj7", "D", "Em7", "D", "Cmaj7", "D", "Cmaj7", "Cmaj7"])
S.scene("静止", 4, "outro", ["Cmaj7", "Cmaj7", "Cmaj7", "Cmaj7"])
NAMES = ["一つ目の星", "数える1", "数える2", "数える3", "満天", "静止"]

c = make(S, NAMES,
         [("一つ目の星", 0, 0.62), ("数える1", 0, 0.6), ("数える2", 0, 0.64), ("数える3", 0, 0.68), ("数える3", 11, 0.76),
          ("満天", 0, 0.8), ("満天", 7, 0.7), ("静止", 0, 0.5), ("静止", 3, 0.3)],
         {"数える1": 0.62, "数える2": 0.62, "数える3": 0.66, "満天": 0.7, "静止": 0.7},
         flute_gain={"数える1": 1.3, "数える2": 1.25, "数える3": 1.2, "満天": 1.15}, intro="一つ目の星", passing=True, tension=True)
STAR = S.track("星（グロッケン）", "bell", patch="glockenspiel", volume=0.03, pan=0.4, reverb=0.75, barGain=c.g())
STAR2 = S.track("星（遠いグロッケン）", "bell", patch="glockenspiel", volume=0.02, pan=-0.45, reverb=0.85, barGain=c.g())

# ---------- 旋律（C リディア） ----------
put_melody(c, "数える1", [
    ["R:1 3:1 5:1 7:1", "6:3 R:1", "5:1 3:1 2:1 3:1", "1:3 R:1"],
    ["1:1 3:1 5:1 6:1", "4:3 R:1", "5:1 6:1 5:1 4:1", "3:3 R:1"],
    ["5:1 7:1 1':1 7:1", "6:3 R:1", "5:1 3:1 6:1 5:1", "3:3 R:1"]], 5)
put_melody(c, "数える2", [
    ["3:1 5:1 6:1 1':1", "7:3 R:1", "6:1 5:1 4:1 6:1", "5:3 R:1"],
    ["3:1 4:1 5:1 7:1", "6:1 5:1 4:2", "5:1 6:1 7:1 5:1", "6:3 R:1"],
    ["1':1 7:0.5 6:0.5 5:1 3:1", "4:1.5 5:0.5 6:2", "7:1 6:1 5:1 4:1", "3:3 R:1"]], 5)
put_melody(c, "数える3", [
    ["5:1 6:1 7:1 1':1", "6:1 4:1 2:1 4:1", "5:1 7:1 6:1 5:1", "3:3 R:1"],
    ["4:1 5:1 6:1 4:1", "5:1 7:1 6:1 5:1", "3:1 5:1 7:1 5:1", "6:3 R:1"],
    ["7:1 6:1 5:1 3:1", "2:1 4:1 6:1 4:1", "5:1 4:1 2:1 7,:1", "1:3 R:1"]], 5)
put_melody(c, "満天", [
    ["3:1 5:1 7:1 6:1", "4:3 R:1", "5:1 3:1 2:1 3:1", "4:3 R:1"],
    ["3:1 5:1 7:1 5:1", "6:3 R:1", "5:4", "R:4"]], 5)

# ---------- 伴奏（星の点だけが増える） ----------
DENS = {"数える1": 1, "数える2": 2, "数える3": 3, "満天": 4}
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6"); hi = tones(ch, "C6", "C7")
    if n == "一つ目の星":
        v = voice(ch, 60, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2")
        if i == 2: STAR.bar(b, f"R:2 {nm(hi[1])}:2")          # 一つ目の星
    elif n in DENS:
        d = DENS[n]
        c.HARP.bar(b, f"{nm(t[0])}:1 {nm(t[1])}:1 {nm(t[2])}:1 {nm(t[1])}:1" if i % 2 == 0 else f"{nm(t[1])}:2 {nm(t[2])}:2")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 60, 3, spread=True)
        if n != "数える1" or i >= 4:
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        # 星の点：数える1=2小節に1つ、数える2=1小節に1つ、数える3=1小節に2つ、満天=1小節に3〜4つ
        if d == 1 and i % 2 == 1: STAR.bar(b, f"R:2 {nm(hi[i % 3])}:2")
        if d == 2: STAR.bar(b, f"R:1 {nm(hi[i % 3])}:3")
        if d == 3:
            STAR.bar(b, f"R:1 {nm(hi[i % 3])}:2 {nm(hi[(i + 1) % 3])}:1")
            if i % 2 == 0: c.HARP2.bar(b, f"R:2 {nm(hi[(i + 2) % 3] - 12)}:2")
        if d == 4:
            STAR.bar(b, f"R:0.5 {nm(hi[0])}:1 {nm(hi[2])}:1 {nm(hi[1])}:1.5")
            STAR2.bar(b, f"R:1.5 {nm(hi[1])}:1 {nm(hi[0])}:1.5")
            c.HARP2.bar(b, f"R:1 {nm(hi[2] - 12)}:3")
    elif n == "静止":
        if i == 0:
            v = voice(ch, 60, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
            STAR.bar(b, f"{nm(hi[2])}:4")
        if i == 1: c.HARP.bar(b, f"{nm(t[2])}:4")

rich(c, choir_scenes=["数える2", "数える3", "満天"], pulse_scenes=["数える1", "数える2", "数える3", "満天"])

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の009。甲板で星を一つずつ数える。C リディア・50。星（グロッケンと竪琴の高い音）の点だけが場面ごとに増え、最後に静止する。",
       harm_scenes=["数える1", "数える2", "数える3"], tail_scene="静止")
