# ケルト・フルート100曲「銀の笛と百の夜」007 潮の呼び声 Call of the Tide — 第2版（2026-10-28）
# イメージ: 夕方の砂浜。潮がゆっくり引いていき（旋律が上から下りてくる）、また満ちてくる（下から上がっていく）。
#   それが2回。2回目の満ち潮は、1回目より高い所まで来る。最後は波の音に戻る。
# 形（台帳）: ゆっくりのジグ（6/8・付点4分＝42）。8小節で1つの波（下りる→上がる）。2回の満ち引き＝2つの小さな山。D ドリア。
# 編曲の表:
#   波      : 波の音→ナイロンギターだけ（1本ずつのアルペジオ）
#   引く1   : 笛が上から下りる。ギターはまばら（付点4分2つ）
#   満ちる1 : 笛が下から上がる。ギターは8分で細かく、竪琴が加わる（山1）
#   凪ぎ    : 引き切った浜。笛は低い所で、ギターとチェロだけ
#   引く2   : もう一度下りる。チェロが笛と反対向きに上がる
#   満ちる2 : いちばん高い所まで（山2）。弦と竪琴
#   波に戻る: 笛の短い結びのあと、ギターがゆっくりになり、波の音
import sys
from c100_common import *
from c100_v2 import *

BPM = 126   # 8分音符＝126（付点4分＝42）
S = Song("C100", "007-call-of-the-tide", "潮の呼び声", "Call of the Tide", BPM, 6, "D", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
PC_ = ["Dm", "C", "Am", "Dm", "C", "Am", "G", "Dm", "F", "C", "G", "Am", "Dm", "C", "G", "Dm"]
FC_ = ["Dm", "G", "Am", "C", "Am", "F", "G", "Am", "F", "C", "Dm", "G", "Dm", "G", "C", "Dm"]
S.scene("波", 4, "intro", ["Dm", "Dm", "C", "Dm"])
S.scene("引く1", 16, "verse", PC_)
S.scene("満ちる1", 16, "chorus", FC_)
S.scene("凪ぎ", 8, "break", ["Dm", "C", "Dm", "Am", "Dm", "C", "Dm", "Dm"])
S.scene("引く2", 16, "verse", PC_)
S.scene("満ちる2", 16, "chorus", FC_)
S.scene("波に戻る", 6, "outro", ["Dm", "C", "Dm", "Dm", "Dm", "Dm"])
NAMES = ["波", "引く1", "満ちる1", "凪ぎ", "引く2", "満ちる2", "波に戻る"]

c = make(S, NAMES,
         [("波", 0, 0.6), ("引く1", 0, 0.62), ("引く1", 15, 0.58), ("満ちる1", 0, 0.62), ("満ちる1", 7, 0.78), ("満ちる1", 15, 0.62),
          ("凪ぎ", 0, 0.56), ("引く2", 0, 0.62), ("満ちる2", 0, 0.66), ("満ちる2", 7, 0.88), ("満ちる2", 15, 0.66), ("波に戻る", 0, 0.56), ("波に戻る", 5, 0.34)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="波", passing=True, tension=False)
GT = S.track("ナイロンギター", "guitar", patch="nylonGuitar", volume=0.13, pan=0.3, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.2, reverb=0.45, barGain=c.g())

PULL = ["5':3 4':1 3':2", "2':2 1':1 7:3", "6:3 5:1 4:2", "5:6",
        "4':3 3':1 2':2", "1':2 7:1 6:3", "5:3 4:1 3:2", "4:6",
        "3':3 2':1 1':2", "7:2 6:1 5:3", "4:3 3:1 2:2", "3:6",
        "5:3 6:1 7:2", "1':2 7:1 6:3", "5:2 4:1 3:2 2:1", "1:6"]
FLOW = ["1:3 2:1 3:2", "4:2 5:1 6:3", "5:3 6:1 7:2", "1':6",
        "7:3 1':1 2':2", "3':2 2':1 1':3", "2':3 3':1 4':2", "5':6",
        "4':3 3':1 2':2", "3':2 2':1 1':3", "7:3 6:1 5:2", "6:6",
        "5:3 4:1 3:2", "4:2 3:1 2:3", "3:2 2:1 1:2 7,:1", "1:6"]
FLOW2 = FLOW[:4] + ["1':3 2':1 3':2", "4':2 5':1 6':3", "5':3 6':1 7':2", "6':6"] + FLOW[8:]
play_melody(c, "引く1", PULL, 4, "air", density=0.7, seed=701)
play_melody(c, "満ちる1", FLOW, 4, "air", density=0.9, seed=702)
play_melody(c, "凪ぎ", ["5,:6", "1:3 2:3", "3:6", "2:6", "1:3 7,:3", "1:6", "R:6", "R:6"], 4, "air", density=0.5, seed=703)
play_melody(c, "引く2", PULL, 4, "air", density=0.9, seed=704)
play_melody(c, "満ちる2", FLOW2, 4, "air", density=1.0, seed=705)
play_melody(c, "波に戻る", ["5:3 4:1 3:2", "2:6", "1:6", "1:6", "R:6", "R:6"], 4, "air", density=0.5, seed=706)

B = S.beats; prev = 48
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5")
    if n in ("引く1", "引く2", "凪ぎ") or (n == "波" and i < 2) or (n == "波に戻る" and i >= 3):
        if not (n == "波に戻る" and i >= 5):
            GT.bar(b, f"{nm(t[0])}:1 {nm(t[2])}:1 {nm(t[3])}:1 {nm(t[4 % len(t)])}:3")        # 1本ずつ、最後は長く
    else:
        GT.bar(b, " ".join(f"{nm(t[x % len(t)])}:1" for x in ((0, 2, 3, 4, 3, 2) if i % 2 == 0 else (1, 3, 4, 5, 4, 3))))
    if n in ("波", "凪ぎ", "引く1") or (n == "波に戻る" and i < 5):   # 空間の床：うすい弦（前奏と凪ぎで音が落ちすぎないように）
        v = voice(ch, 52, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n in ("満ちる1", "満ちる2"):
        c.HARP.bar(b, f"{nm(r)}:3 {nm(r + 12)}:3")
        c.HARP2.bar(b, f"R:3 {nm(tones(ch, 'D5', 'D6')[0])}:3") if i % 2 == 1 else None
    if n in ("凪ぎ", "引く2", "満ちる2", "波に戻る") and not (n == "波に戻る" and i >= 5):
        cand = [m for m in range(40, 57) if m % 12 in chord_pcs(ch)]
        a = min(cand, key=lambda m: abs(m - prev)); z = min([m for m in cand if m != a], key=lambda m: abs(m - a))
        CELLO.bar(b, f"{nm(a)}:3 {nm(z)}:3"); prev = z
    if n == "満ちる2" or (n == "満ちる1" and i >= 4):
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の007（第2版）。引き潮と満ち潮の砂浜。ゆっくりのジグ（6/8・付点4分＝42）、D ドリア。8小節で1つの波（旋律が下りる→上がる）を2回。2回目の満ち潮はより高く。ナイロンギターの1本ずつのアルペジオ。",
       harm_scenes=None, tail_scene="波に戻る", fill=False, pads=True, pad_scenes=["引く1", "満ちる1", "凪ぎ", "満ちる2", "引く2"])
