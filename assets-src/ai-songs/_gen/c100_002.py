# ケルト・フルート100曲「銀の笛と百の夜」002 灯室への階段 Stairway to the Lamp（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 灯室へ、らせん階段を一段ずつ上る。足音（枠太鼓の手のひら1打）は、上るほど間が空いて、やがて消える。波の音は遠くなる。
#       最後に灯室へ着いて、灯りがともる（小さな山1つ）。始め：低い竪琴が一段ずつ上がる／終わり：高めの笛。
# 型: 「一段ずつ上がる4音」（1 2 3 5 → 2 3 4 6 → 3 4 5 7…）。ベースの根音も A B C D と一段ずつ上がる。
# 強さ: 一段目(pp)→らせん1(p)→らせん2(p→mp)→らせん3(mp)→灯室(mf。小さな山)→余韻(pp)
import sys
from c100_common import *

S = Song("C100", "002-lamp-stairs", "灯室への階段", "Stairway to the Lamp", 60, 4, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("一段目", 4, "intro", ["Am", "Bm7", "C", "D"])
S.scene("らせん1", 12, "verse", ["Am", "Bm7", "C", "D", "Em", "G", "Am", "Bm7", "C", "D", "Em", "Am"])
S.scene("らせん2", 12, "verse", ["Am", "C", "D", "Em", "Bm7", "C", "D", "Em", "G", "Em", "D", "Am"])
S.scene("らせん3", 12, "verse", ["C", "D", "Em", "G", "Am", "Bm7", "C", "D", "Em", "G", "D", "Em"])
S.scene("灯室", 16, "chorus", ["Am", "C", "D", "Em", "G", "D", "Em", "Am", "C", "D", "Em", "G", "Bm7", "C", "D", "Am"])
S.scene("余韻", 8, "outro", ["Am", "Am", "G", "Am", "Em", "Am", "Am", "Am"])
NAMES = ["一段目", "らせん1", "らせん2", "らせん3", "灯室", "余韻"]
K = S.key

c = make(S, NAMES,
         [("一段目", 0, 0.72), ("らせん1", 0, 0.68), ("らせん2", 0, 0.74), ("らせん3", 0, 0.82), ("灯室", 0, 0.9), ("灯室", 9, 1.0), ("灯室", 15, 0.9), ("余韻", 0, 0.45), ("余韻", 7, 0.3)],
         {"らせん1": 0.55, "らせん2": 0.55, "らせん3": 0.6, "灯室": 0.62, "余韻": 0.8},
         flute_gain={"らせん1": 1.5, "らせん2": 1.3, "らせん3": 1.2, "灯室": 1.15}, intro="一段目", passing=True)
BELL = S.track("ベル", "bell", patch="glockenspiel", volume=0.035, pan=0.35, reverb=0.7, barGain=c.g())
STEP = S.track("足音（枠太鼓）", "guitar", patch="frameDrum", volume=0.06, pan=-0.2, reverb=0.4, modulate=False)

# ---------- 旋律（A ドリアン。一段ずつ上がる4音） ----------
put_melody(c, "らせん1", [
    ["1:1 2:1 3:1 5:1", "2:1 3:1 4:1 6:1", "3:1 4:1 5:1 7:1", "5:3 R:1"],
    ["R:1 1:1 2:1 3:1", "2:1 3:1 4:1 5:1", "4:1 3:1 2:1 1:1", "1:3 R:1"],
    ["1:1 2:1 3:1 5:1", "3:1 4:1 5:1 6:1", "5:1 4:1 3:1 2:1", "1:4"]], 4)
put_melody(c, "らせん2", [
    ["5,:1 6,:1 7,:1 2:1", "6,:1 7,:1 1:1 3:1", "7,:1 1:1 2:1 3:1", "2:3 R:1"],
    ["R:1 5,:1 6,:1 7,:1", "6,:1 7,:1 1:1 2:1", "1:1 7,:1 6,:1 5,:1", "5,:3 R:1"],
    ["5,:1 7,:1 1:1 3:1", "2:1 1:1 7,:1 6,:1", "7,:1 1:1 2:1 3:1", "1:4"]], 5)
put_melody(c, "らせん3", [
    ["7,:1 1:1 2:1 3:1", "1:1 2:1 3:1 2:1", "7,:1 1:1 2:1 3:1", "3:3 R:1"],
    ["R:1 6,:1 7,:1 1:1", "7,:1 1:1 2:1 3:1", "2:2 1:1 7,:1", "1:3 R:1"],
    ["1:1 2:1 3:1 2:1", "3:2 2:1 1:1", "7,:1 1:1 2:1 3:1", "3:4"]], 5)
put_melody(c, "灯室", [
    ["3:2 2:1 1:1", "2:2 3:2", "1:2 2:1 3:1", "3:4"],
    ["3:1.5 2:0.5 1:1 7,:1", "1:2 2:2", "7,:1 1:1 2:1 3:1", "2:4"],
    ["3:2 2:2", "1:1 2:1 3:2", "2:2 1:1 7,:1", "1:4"],
    ["6,:2 7,:2", "1:2 2:2", "1:3 7,:1", "1:4"]], 5)
put_bars(c, "余韻", ["3:4", "R:4", "2:4", "R:4", "1:2 2:2", "R:4", "3:4", "3:4"], 5)

# ---------- 伴奏 ----------
STAIR = ["A3", "B3", "C4", "D4"]
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6")
    if n == "一段目":
        c.HARP.bar(b, f"{STAIR[i]}:4")                       # 低い竪琴が、一段ずつ上がる
        if i >= 1: c.HARP2.bar(b, f"R:2 {nm(t[-3])}:2")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    elif n == "らせん1":
        c.HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 2)))
        if i >= 4: c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        if i % 4 == 3: c.HARP2.bar(b, f"R:2 {nm(t[-2])}:2")
        STEP.bar(b, "D3:1 R:3")                              # 足音：毎小節の頭に1打
    elif n == "らせん2":
        c.HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 2, 0, 2, 4, 6)))
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i % 4 == 3: BELL.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C6", "C7")[:4]))
        if i % 2 == 0: STEP.bar(b, "D3:1 R:3")              # 足音：2小節に1打。間が空く
    elif n == "らせん3":
        c.HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 6, 4, 2, 4, 6)))
        c.HARP2.bar(b, " ".join(f"{nm(x)}:0.5" for x in [t[-1], t[-2], t[-3], t[-2]] * 2) if i % 2 == 0 else f"{nm(t[-1])}:4")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i % 2 == 1: BELL.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C6", "C7")[:4]))
        if i % 4 == 0: STEP.bar(b, "D3:1 R:3")              # 足音：4小節に1打。遠ざかる
    elif n == "灯室":
        if i < 12:
            c.HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 6, 7, 6, 4, 2)))
            if i % 2 == 0: c.HARP2.bar(b, " ".join(f"{nm(x)}:0.5" for x in [t[-1], t[-2], t[-3], t[-2]] * 2))
        else:   # 灯りがともったあとは、竪琴がゆっくりになり、笛を前に出す
            c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2")
            if i % 2 == 0: c.HARP2.bar(b, f"{nm(t[-1])}:4")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i % 2 == 1 and i < 12: BELL.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C6", "C7")[:4]))
    elif n == "余韻":
        if i % 2 == 0: c.HARP2.bar(b, f"{nm(t[-1])}:2 {nm(t[-3])}:2")
        if i < 6: c.HARP.bar(b, f"{nm(t[0])}:4")
        if i < 6:
            v = voice(ch, 62, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i == 5: BELL.bar(b, f"{nm(tones(ch, 'C6', 'C7')[2])}:4")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の002。灯室へのらせん階段。A ドリアン・60。一段ずつ上がる4音の型。足音は上るほど間があいて消え、最後に灯りがともる。",
       harm_scenes=["らせん2", "らせん3", "灯室"], tail_scene="余韻", tail_keep=6, double=("--double" in sys.argv))
