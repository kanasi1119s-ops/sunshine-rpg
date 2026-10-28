# ケルト・フルート100曲「銀の笛と百の夜」006 夜の灯台守 The Keeper of the Night Light（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 日が落ちた岬。灯台守が螺旋を上り、灯りを一つずつともしていく。灯りが増えるたびに、高い鈴（グロッケン）の点が一つ増える。
#       中盤に1つ山（灯りがいっぱいに強くなる）→静まり、最後は竪琴の上昇アルペジオで光が遠くまで届く。
# 型: ゆっくり開く和音の上の長い旋律。始め：低い弦／終わり：高いベル。灯りの数＝鈴の点の数（場面ごとに 1→2→3→4→満ちる）。
# 強さ: 低い弦(pp)→灯り1(p)→灯り2(mp, 山)→静まり(p)→灯りが満ちる(mp→p)→余韻(pp)
import sys
from c100_common import *

S = Song("C100", "006-night-light-keeper", "夜の灯台守", "The Keeper of the Night Light", 56, 4, "B", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("暗い海", 4, "intro", ["Bm7", "Bm7", "Em", "Bm7"])
S.scene("灯り1", 12, "verse", ["Bm7", "Em", "D", "Bm7", "F#m7", "Em", "A", "Bm7", "D", "A", "Em", "Bm7"])
S.scene("灯り2", 12, "chorus", ["D", "A", "Bm7", "Em", "D", "A", "F#m7", "Bm7", "Em", "D", "A", "Bm7"])
S.scene("静まり", 12, "verse", ["Bm7", "Em", "Bm7", "F#m7", "Em", "D", "A", "Bm7", "C#m7", "Em", "A", "Bm7"])
S.scene("灯りが満ちる", 12, "chorus", ["D", "Em", "A", "Bm7", "D", "A", "Em", "F#m7", "Em", "A", "D", "Bm7"])
S.scene("余韻", 8, "outro", ["Bm7", "Em", "D", "A", "Bm7", "Bm7", "Bm7", "Bm7"])
NAMES = ["暗い海", "灯り1", "灯り2", "静まり", "灯りが満ちる", "余韻"]

c = make(S, NAMES,
         [("暗い海", 0, 0.7), ("灯り1", 0, 0.62), ("灯り1", 11, 0.7), ("灯り2", 0, 0.76), ("灯り2", 8, 0.9), ("灯り2", 11, 0.7),
          ("静まり", 0, 0.6), ("静まり", 11, 0.64), ("灯りが満ちる", 0, 0.72), ("灯りが満ちる", 8, 0.84), ("灯りが満ちる", 11, 0.62),
          ("余韻", 0, 0.5), ("余韻", 7, 0.3)],
         {"灯り1": 0.6, "灯り2": 0.65, "静まり": 0.6, "灯りが満ちる": 0.65, "余韻": 0.8},
         flute_gain={"灯り1": 1.3, "灯り2": 1.2, "静まり": 1.3, "灯りが満ちる": 1.2, "余韻": 1.1}, intro="暗い海", passing=True, tension=True)
BELL = S.track("灯りの鈴", "bell", patch="glockenspiel", volume=0.032, pan=0.35, reverb=0.7, barGain=c.g())
BELL2 = S.track("灯りの鈴（遠い）", "bell", patch="glockenspiel", volume=0.022, pan=-0.4, reverb=0.8, barGain=c.g())

# ---------- 旋律（B ドリア。001と同じく、一つ一つの音を4分音符で弾いてなめらかにつなぐ。フレーズの終わりだけ長く） ----------
put_melody(c, "灯り1", [
    ["R:1 1:1 2:1 3:1", "5:3 R:1", "4:1 3:1 2:1 3:1", "1:3 R:1"],
    ["1:1 2:1 3:1 5:1", "6:3 R:1", "5:1 4:1 3:1 2:1", "3:3 R:1"],
    ["3:1 5:1 6:1 7:1", "1':2 7:1 6:1", "5:1 4:1 3:1 2:1", "1:3 R:1"]], 4)
put_melody(c, "灯り2", [
    ["5:1 6:1 7:1 1':1", "7:3 R:1", "6:1 7:1 1':1 6:1", "5:3 R:1"],
    ["3:1 5:1 6:1 7:1", "1':2 7:1 6:1", "7:1 1':1 7:1 5:1", "6:3 R:1"],
    ["6:1 5:1 4:1 3:1", "2:1 3:1 4:2", "3:1 2:1 1:1 7,:1", "1:3 R:1"]], 4)
put_melody(c, "静まり", [
    ["R:1 3:1 2:1 1:1", "5,:3 R:1", "6,:1 7,:1 1:1 2:1", "3:3 R:1"],
    ["2:1 3:1 5:1 3:1", "2:3 R:1", "1:1 2:1 3:1 2:1", "7,:3 R:1"],
    ["6,:1 7,:1 1:1 3:1", "2:1.5 1:0.5 7,:2", "6,:1 7,:1 2:1 7,:1", "1:3 R:1"]], 4)
put_melody(c, "灯りが満ちる", [
    ["3:1 5:1 6:1 5:1", "7:3 R:1", "6:1 5:1 3:1 5:1", "6:3 R:1"],
    ["1':1 7:0.5 6:0.5 5:1 3:1", "4:1.5 5:0.5 6:2", "7:1 6:1 5:1 4:1", "5:3 R:1"],
    ["5:1 6:1 7:1 1':1", "7:1 6:1 5:1 3:1", "2:1 3:1 4:1 2:1", "1:4"]], 4)
put_bars(c, "余韻", ["3:1 2:1 1:2", "R:4", "2:1 1:1 7,:2", "R:4", "1:4", "R:4", "R:4", "R:4"], 4)
put_bars(c, "暗い海", ["R:4", "R:4", "R:4", "R:4"], 4)

# ---------- 伴奏 ----------
LIGHTS = {"灯り1": 1, "灯り2": 2, "静まり": 3, "灯りが満ちる": 4}
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6"); hi = tones(ch, "C6", "C7")
    if n == "暗い海":   # 始まり：低いチェロだけが、一音ずつ（灯りの消えた海）。最後の小節で最初の灯り
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4" if i % 2 == 0 else f"R:2 {nm((lo + 12 if lo < 40 else lo) + 7)}:2")
        if i == 3: BELL.bar(b, f"R:2 {nm(hi[0])}:2")
        continue
    if n == "暗い海":
        v = voice(ch, 58, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        if i == 3: BELL.bar(b, f"R:2 {nm(hi[0])}:2")          # 最初の灯り
    elif n in LIGHTS:
        c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2" if i % 2 == 0 else f"{nm(t[1])}:2 {nm(t[3])}:2")
        if i % 4 == 3: c.HARP2.bar(b, f"R:2 {nm(t[-2])}:2")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 58, 3, spread=True)
        if n != "灯り1" or i >= 4:
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        # 灯りの鈴：場面が進むほど点が増える（灯り1=4小節に1回、…）
        step = {1: 4, 2: 3, 3: 2, 4: 2}[LIGHTS[n]]
        if i % step == step - 1: BELL.bar(b, f"{nm(hi[(i // step) % 3])}:4")
        if LIGHTS[n] >= 3 and i % 2 == 0: BELL2.bar(b, f"R:2 {nm(hi[(i // 2 + 1) % 3])}:2")
    elif n == "余韻":
        if i < 6:
            v = voice(ch, 58, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        # 竪琴の上昇アルペジオ：光が遠くへ
        if i in (0, 2, 4):
            a = tones(ch, "D3", "D6")
            c.HARP.bar(b, f"{nm(a[0])}:1 {nm(a[1])}:1 {nm(a[2])}:1 {nm(a[3])}:1")
        if i in (1, 3, 5): BELL.bar(b, f"{nm(hi[(i // 2) % 3])}:4")
        if i == 6: BELL.bar(b, f"{nm(hi[2])}:4")

rich(c, choir_scenes=["灯り2", "灯りが満ちる"], pulse_scenes=["灯り1", "灯り2", "静まり", "灯りが満ちる"])

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の006。夜の岬で灯台守が灯りを一つずつともす。B ドリア・56。灯りの数だけ鈴の点が増え、中盤に山、最後は竪琴の上昇アルペジオ。",
       harm_scenes=["灯り1", "灯り2", "静まり", "灯りが満ちる"], tail_scene="余韻")
