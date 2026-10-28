# ケルト・フルート100曲「銀の笛と百の夜」002 灯室への階段 Stairway to the Lamp — 第2版（2026-10-28）
# イメージ: 笛を手に、灯台のらせん階段を上っていく。同じ景色が、ひと回りごとに少し高い所から見える。
#   ＝同じ節を3回。ひと回りごとに全音ずつ上がる（A→B→C#）。足音は枠太鼓の手のひら。最上階の灯室に着くと、足音が止み、高い笛が残る。
# 形（台帳）: 1周ごとに全音上がるらせん。3/4・♩=60。A ドリア→B ドリア→C# ドリア。始め：低い竪琴／終わり：高い笛。終盤に小さな山。
# 旋律: 段を上る動機「1 2 3 → 5」「2 3 4 → 6」。8小節の型 a b a' c、続けて b' c'（前半は2度で開き、後半は主音で閉じる）。
# 編曲の表:
#   前置き  : 低い竪琴のオスティナート（根音・5度・オクターブ）＋足音
#   1周目   : 笛＋低い竪琴＋足音（毎小節1打）
#   上り1   : 竪琴が音階を駆け上がり、調が全音上がる
#   2周目   : ＋チェロの対旋律（笛と反対向き）＋ピチカート。足音は1小節に2打（急ぎ足）
#   上り2   : 同じく全音上がる
#   3周目   : ＋弦の持続＋グロッケン。足音は1小節に3打。後半で小さな山、最後は高い音で止まる
#   灯室    : 足音が止み、高い笛の長い音と竪琴の倍音だけ
import sys
from c100_common import *
from c100_v2 import *
from lm25_lib import tr_chord

S = Song("C100", "002-lamp-stairs", "灯室への階段", "Stairway to the Lamp", 60, 3, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
RC = ["Am", "Am", "D", "D", "G", "Em", "Am", "Em", "Am", "Am", "Em", "D", "D", "G", "Em", "Am",
      "G", "Em", "D", "Em", "D", "G", "Em", "Am"]
S.scene("前置き", 4, "intro", ["Am"] * 4)
S.scene("1周目", 24, "verse", RC)
S.scene("上り1", 2, "break", ["D", "E"])
S.scene("2周目", 24, "verse", [tr_chord(x, 2) for x in RC])
S.scene("上り2", 2, "break", ["E", "F#"])
S.scene("3周目", 24, "chorus", [tr_chord(x, 4) for x in RC])
S.scene("灯室", 4, "outro", ["C#m"] * 4)
NAMES = ["前置き", "1周目", "上り1", "2周目", "上り2", "3周目", "灯室"]

c = make(S, NAMES,
         [("前置き", 0, 0.6), ("1周目", 0, 0.62), ("1周目", 23, 0.66), ("上り1", 0, 0.66), ("2周目", 0, 0.68), ("2周目", 23, 0.74),
          ("上り2", 0, 0.74), ("3周目", 0, 0.76), ("3周目", 16, 0.88), ("3周目", 23, 0.74), ("灯室", 0, 0.62), ("灯室", 3, 0.42)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="前置き", passing=True, tension=False)
STEP = S.track("足音（枠太鼓の手のひら）", "guitar", patch="frameDrum", volume=0.07, pan=-0.2, reverb=0.45, modulate=False, barGain=c.g())
CELLO = S.track("チェロ（対旋律）", "strings", patch="cello", volume=0.085, pan=0.25, reverb=0.45, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.055, pan=-0.35, reverb=0.4, barGain=c.g())
GLOCK = S.track("グロッケン", "bell", patch="glockenspiel", volume=0.026, pan=0.35, reverb=0.65, barGain=c.g())

a  = ["1:1 2:1 3:1", "5:2 3:1", "2:1 3:1 4:1", "6:2 5:1"]
b  = ["4:1 5:1 6:1", "7:2 6:1", "5:1 4:1 3:1", "2:3"]
a2 = ["1:1 2:1 3:1", "5:2 6:1", "7:1 6:1 5:1", "6:2 4:1"]
cc = ["5:1 4:1 3:1", "2:1 3:1 4:1", "3:1.5 2:0.5 7,:1", "1:3"]
b2 = ["4:1 5:1 6:1", "1':2 7:1", "6:1 5:1 4:1", "5:3"]
c2 = ["6:1 5:1 4:1", "3:1 4:1 5:1", "4:1.5 3:0.5 2:1", "1:3"]
top = ["4:1 5:1 6:1", "7:1 6:1 5:1", "6:1.5 7:0.5 6:1", "5:3"]           # 3周目の最後：高い所で止まる
play_melody(c, "1周目", a + b + a2 + cc + b2 + c2, 4, "air", density=0.7, seed=201)
play_melody(c, "2周目", a + b + a2 + cc + b2 + c2, 4, "air", density=0.9, seed=202, lift=2)
play_melody(c, "3周目", a + b + a2 + cc + b2 + top, 4, "air", density=1.0, seed=203, lift=4)
play_melody(c, "灯室", ["5:3", "5:3", "R:3", "R:3"], 4, "air", density=0, lift=4)

B = S.beats; prev = 48
for b_ in range(c.NB):
    n, i, L, k = S.scene_of(b_); ch = S.chords[b_]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "E3", "E5")
    if n in ("前置き", "1周目", "2周目", "3周目"):
        c.HARP.bar(b_, f"{nm(r)}:1 {nm(r + 7)}:1 {nm(r + 12)}:1")      # 低い竪琴：根音・5度・オクターブ（段を踏む形）
    if n in ("前置き", "1周目"): STEP.bar(b_, "D3:1 R:2")
    if n == "2周目": STEP.bar(b_, "D3:1 R:1 D3:1,")
    if n == "3周目": STEP.bar(b_, "D3:1 D3:1, D3:1,")
    if n in ("2周目", "3周目"):
        cand = [m for m in range(43, 60) if m % 12 in chord_pcs(ch)]
        a_ = min(cand, key=lambda m: abs(m - prev)); z = min([m for m in cand if m != a_], key=lambda m: abs(m - a_))
        CELLO.bar(b_, f"{nm(a_)}:2 {nm(z)}:1"); prev = z
        if i % 2 == 1: PIZZ.bar(b_, f"R:1 {nm(t[1])}:1 {nm(t[2])}:1")
    if n == "3周目":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b_, f"{nm(v[j])}:3")
        if i % 4 == 0: GLOCK.bar(b_, f"{nm(tones(ch, 'C6', 'C7')[0])}:3")
    if n in ("上り1", "上り2"):    # 竪琴が音階を駆け上がる（次の調の入口へ）
        base = 45 + (2 if n == "上り1" else 4) + (2 if i == 1 else 0)
        sc = [base + x for x in (0, 2, 3, 5, 7, 9)]
        c.HARP.bar(b_, " ".join(f"{nm(x)}:0.5" for x in sc))
        STEP.bar(b_, "D3:1 R:2" if i == 0 else "D3:1 D3:1, R:1")
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b_, f"{nm(v[j])}:3")
    if n == "灯室":
        v = voice(ch, 61, 3, spread=True)
        for j in range(3): c.STR[j].bar(b_, f"{nm(v[j])}:3")
        c.HARP2.bar(b_, " ".join(f"{nm(x)}:1" for x in tones(ch, "C5", "C7")[i:i + 3]))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の002（第2版）。灯台のらせん階段を上る。3/4・♩=60。同じ節を3回、ひと回りごとに全音上がる（A→B→C# ドリア）。足音は枠太鼓の手のひら。灯室に着くと足音が止み、高い笛が残る。",
       harm_scenes=None, tail_scene="灯室", fill=False, pads=True, pad_scenes=["2周目", "3周目", "灯室"])
