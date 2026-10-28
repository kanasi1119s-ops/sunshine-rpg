# ケルト・フルート100曲「銀の笛と百の夜」021 小川のはじまり Where the Brook Begins — 第2版（2026-10-28）
# イメージ: 森の奥の岩のすき間から、水が一滴、また一滴と落ちる。滴がだんだん増えて、つながり、細い流れになって走り出す。小川の生まれる所。
# 形（台帳）: リズムから積み上げる。ぽつんとした水滴の音（竪琴・グロッケンの高い1音）が、だんだん連なって流れになる。
#   笛も、はじめは1音ずつ間をあけて置かれ、2音・3音とつながり、最後はなめらかな旋律として流れる。6/8・付点4分＝44。A ミクソリディア。山なし。
# 編曲の表:
#   一滴   : 竪琴とグロッケンの高い1音だけが、ぽつり、ぽつり（約10秒）
#   滴     : 笛も1音ずつ。滴がふえる。低い弦がごくうすく
#   連なる : 笛が2〜3音ずつつながる。竪琴は2音ずつ
#   流れ1  : 笛のなめらかな旋律。竪琴が流れる分散和音（8分）。チェロ
#   流れ2  : ＋弦の持続＋ピチカート
#   流れ3  : ＋笛の和声。流れがいちばん豊か
#   小川   : 笛が抜け、竪琴の流れと小川の音が残る
import sys, random
from c100_common import *
from c100_v2 import *

BPM = 132
S = Song("C100", "021-where-the-brook-begins", "小川のはじまり", "Where the Brook Begins", BPM, 6, "A", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
FC = ["A", "D", "G", "A", "D", "G", "D", "A", "A", "G", "D", "A", "D", "G", "E", "A"]
S.scene("一滴", 4, "intro", ["A"] * 4)
S.scene("滴", 12, "verse", ["A", "A", "G", "A", "A", "D", "A", "A", "G", "G", "A", "A"])
S.scene("連なる", 16, "verse", FC)
S.scene("流れ1", 16, "verse", FC)
S.scene("流れ2", 16, "chorus", FC)
S.scene("流れ3", 16, "chorus", FC)
S.scene("小川", 8, "outro", ["A", "G", "A", "A", "D", "G", "A", "A"])
NAMES = ["一滴", "滴", "連なる", "流れ1", "流れ2", "流れ3", "小川"]

c = make(S, NAMES,
         [("一滴", 0, 0.6), ("滴", 0, 0.6), ("連なる", 0, 0.64), ("流れ1", 0, 0.68), ("流れ2", 0, 0.72), ("流れ3", 0, 0.76), ("流れ3", 15, 0.72),
          ("小川", 0, 0.64), ("小川", 7, 0.36)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="一滴", passing=True, tension=False)
DROP = S.track("滴（グロッケン）", "bell", patch="glockenspiel", volume=0.06, pan=0.3, reverb=0.75, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.15, reverb=0.45, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.05, pan=-0.35, reverb=0.4, barGain=c.g())

rg = random.Random(21)
def drops(n_):   # 1小節に n_ 個の滴（和音の高い音を、ばらばらの場所に）
    pos = sorted(rg.sample(range(6), min(n_, 6))); out = []; t = 0
    return pos
B = S.beats
# 滴と、連なる：笛は1音ずつ→2〜3音ずつ
DRIP = ["R:2 5:1 R:3", "R:4 3:1 R:1", "1':1 R:5", "R:3 6:1 R:2", "R:1 5:1 R:4", "R:4 2:1 R:1", "3:1 R:5", "R:2 1:1 R:3",
        "R:3 4:1 R:2", "R:1 6:1 R:2 5:1 R:1", "R:2 3:1 R:3", "1:1 R:5"]
LINK = ["5:1 6:1 R:4", "R:3 1':1 7:1 6:1", "5:2 R:4", "R:3 3:1 4:1 5:1", "4:1 3:1 R:4", "R:3 2:1 3:1 1:1", "7,:2 R:4", "R:3 1:1 2:1 3:1",
        "5:1 6:1 5:1 R:3", "R:3 4:1 3:1 2:1", "3:2 R:4", "R:2 5:1 6:1 7:1 R:1", "1':2 R:1 6:1 5:1 R:1", "R:3 4:1 5:1 6:1", "5:3 R:3", "1:3 R:3"]
F1 = ["1:2 2:1 3:2 5:1", "4:2 3:1 2:3", "3:2 4:1 5:2 6:1", "5:3 3:3", "4:2 5:1 6:2 1':1", "7:2 6:1 5:3", "4:2 3:1 2:2 7,:1", "1:6"]
F2 = ["5:2 6:1 7:2 1':1", "2':2 1':1 7:3", "6:2 7:1 1':2 6:1", "5:6", "4:2 5:1 6:2 4:1", "3:2 2:1 1:3", "2:2 3:1 4:2 2:1", "1:6"]
play_melody(c, "滴", DRIP, 4, "air", density=0)
play_melody(c, "連なる", LINK, 4, "air", density=0.3, seed=2101)
play_melody(c, "流れ1", F1 + F2, 4, "air", density=0.7, seed=2102)
play_melody(c, "流れ2", F1 + F2, 4, "air", density=0.9, seed=2103)
play_melody(c, "流れ3", F2 + F1, 4, "air", density=1.0, seed=2104)
play_melody(c, "小川", ["5:3 3:3", "2:6", "3:2 4:1 5:3", "1:6", "4:3 3:3", "2:6", "1:6", "R:6"], 4, "air", density=0.4, seed=2105)

for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    hi = tones(ch, "A5", "A6"); t = tones(ch, "A3", "A5")
    if n in ("一滴", "滴", "連なる"):
        cnt = {"一滴": 1 + (i % 2), "滴": 2 + i // 4, "連なる": 4}[n]
        pos = sorted(rg.sample(range(6), min(cnt, 6)))
        tr = DROP if n == "一滴" and i % 2 == 0 else c.HARP2
        s, t0 = [], 0
        for p in pos:
            if p > t0: s.append(f"R:{p - t0}")
            s.append(f"{nm(hi[rg.randrange(len(hi))])}:1"); t0 = p + 1
        if t0 < 6: s.append(f"R:{6 - t0}")
        tr.bar(b, " ".join(s))
        v = voice(ch, 52 if n != "一滴" else 57, 3, spread=True)   # 森の奥の空気（岩のすき間の、ひんやりした響き）
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        CELLO.bar(b, f"{nm(r)}:6")
        if n == "連なる": c.HARP.bar(b, " ".join(f"{nm(t[x % len(t)])}:1" for x in (0, 2)) + " R:1 " + " ".join(f"{nm(t[x % len(t)])}:1" for x in (1, 3)) + " R:1")
    if n in ("流れ1", "流れ2", "流れ3") or (n == "小川" and i < 7):
        c.HARP.bar(b, " ".join(f"{nm(t[x % len(t)])}:1" for x in ((0, 2, 4, 5, 4, 2) if i % 2 == 0 else (1, 3, 5, 3, 4, 2))))
        CELLO.bar(b, f"{nm(r)}:6")
        if n == "小川":
            v = voice(ch, 55, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n in ("流れ2", "流れ3"):
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        if i % 2 == 1: PIZZ.bar(b, f"R:3 {nm(t[1])}:1 {nm(t[2])}:1 R:1")
    if n in ("流れ3",) and i % 4 == 0: DROP.bar(b, f"{nm(hi[0])}:3 R:3")
rich(c, choir_scenes=["流れ3"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の021（第2版）。湧き水から小川が生まれる。6/8・付点4分＝44、A ミクソリディア。ぽつんとした水滴の音（竪琴・グロッケン）がだんだん連なり、笛も1音ずつ→2〜3音→なめらかな旋律へ。流れになって走り出す。",
       harm_scenes=None, tail_scene="小川", fill=False, pads=True, pad_scenes=["滴", "連なる", "流れ1", "流れ2", "流れ3", "小川"])
