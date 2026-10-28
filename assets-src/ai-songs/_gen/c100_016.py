# ケルト・フルート100曲「銀の笛と百の夜」016 石垣の道 The Stone Wall Path — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 古い石垣に沿って、はずむ足どりで歩く。石垣の上を猫が走り、風が気持ちいい。道の曲がり角では、ふっと立ち止まって景色を見る。
#   ＝はねるホーンパイプ。1周ごとに、曲がり角で一瞬止まる。最後の曲がり角で、ほんとうに止まって終わる。
# 形（台帳）: ホーンパイプ（付点ではねる）AABB。4/4・♩=96。D ミクソリディア→3周目は E へ上がる。始め：足取り（打楽器）／終わり：曲がり角で止まる。終盤に山。
# 編曲の表:
#   足取り : ボーラン（ホーンパイプの「下（休）上」）だけ
#   1周目  : 笛＋ボーラン＋ギターのストローク
#   曲がり角: 全員が止まり、足音が1つ
#   2周目  : ＋竪琴の3音オスティナート＋チェロ。笛の装飾が増える
#   曲がり角: もう一度
#   3周目  : E へ上がる。＋弦。山
#   終わり : 「4分・4分・4分」で止まって、足音が1つ
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "016-stone-wall-path", "石垣の道", "The Stone Wall Path", 96, 4, "D", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["D", "D", "G", "A", "D", "D", "C", "D"]
BC = ["G", "G", "C", "D", "G", "G", "C", "D"]
S.scene("足取り", 4, "intro", ["D"] * 4)
S.scene("1周目", 32, "verse", AC * 2 + BC * 2)
S.scene("角1", 1, "break", ["D"])
S.scene("2周目", 32, "verse", AC * 2 + BC * 2)
S.scene("角2", 1, "break", ["D"])
S.scene("3周目", 32, "chorus", ["E", "E", "A", "B", "E", "E", "D", "E"] * 2 + ["A", "A", "D", "E", "A", "A", "D", "E"] * 2)   # 全音上（E）
S.scene("終わり", 3, "outro", ["E", "E", "E"])
NAMES = ["足取り", "1周目", "角1", "2周目", "角2", "3周目", "終わり"]

c = make(S, NAMES,
         [("足取り", 0, 0.64), ("1周目", 0, 0.68), ("1周目", 31, 0.72), ("角1", 0, 0.6), ("2周目", 0, 0.74), ("2周目", 31, 0.8), ("角2", 0, 0.62),
          ("3周目", 0, 0.84), ("3周目", 24, 0.94), ("3周目", 31, 0.9), ("終わり", 0, 0.88), ("終わり", 2, 0.5)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="足取り", passing=True, tension=False)
DRUM = S.track("ボーラン", "guitar", patch="frameDrum", volume=0.075, pan=-0.15, reverb=0.3, modulate=False, barGain=c.g())
GTR = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.05, pan=0.35 + 0.04 * i, reverb=0.35, barGain=c.g()) for i in range(5)]
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.2, reverb=0.4, barGain=c.g())

A = ["1:0.5 3:0.5 5:0.5 3:0.5 4:0.5 6:0.5 5:0.5 4:0.5", "3:0.5 5:0.5 1':0.5 5:0.5 6:1 5:1",
     "4:0.5 6:0.5 5:0.5 4:0.5 3:0.5 5:0.5 4:0.5 3:0.5", "2:0.5 3:0.5 4:0.5 2:0.5 7,:1 5,:1",
     "1:0.5 3:0.5 5:0.5 3:0.5 4:0.5 6:0.5 5:0.5 4:0.5", "3:0.5 5:0.5 1':0.5 5:0.5 6:0.5 7:0.5 1':1",
     "7:0.5 5:0.5 6:0.5 4:0.5 5:0.5 3:0.5 2:0.5 7,:0.5", "1:1 1:1 1:1 R:1"]
Bm = ["5:0.5 1':0.5 2':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5", "4':1 3':0.5 2':0.5 1':1 5:1",
      "6:0.5 1':0.5 7:0.5 6:0.5 5:0.5 7:0.5 6:0.5 5:0.5", "4:0.5 5:0.5 6:0.5 4:0.5 5:1 2:1",
      "5:0.5 1':0.5 2':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5", "4':1 3':0.5 2':0.5 1':0.5 7:0.5 1':1",
      "7:0.5 5:0.5 6:0.5 4:0.5 5:0.5 3:0.5 2:0.5 7,:0.5", "1:1 1:1 1:1 R:1"]
play_melody(c, "1周目", A + A + Bm + Bm, 4, "hornpipe", density=0.5, seed=1601)
play_melody(c, "2周目", A + A + Bm + Bm, 4, "hornpipe", density=0.9, seed=1602)
play_melody(c, "3周目", A + A + Bm + Bm, 4, "hornpipe", density=1.0, seed=1603, lift=2)
play_melody(c, "終わり", ["1:1 1:1 1:1 R:1", "R:4", "R:4"], 4, "air", density=0, lift=2)

B = S.beats
HP = [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 0.5, "d", ","), (3.5, 0.5, "u", ",")]
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = [x for x in range(36, 48) if x % 12 == PC[ch[0] if len(ch) == 1 or ch[1] not in "#b" else ch[:2]]][0]
    if n == "足取り":
        bodhran(DRUM, b, B, "hornpipe"); continue
    if n in ("角1", "角2"):
        DRUM.bar(b, "R:2 D3:1, R:1"); continue          # 曲がり角：全員止まって、足音が1つ
    if n == "終わり":
        if i == 0:
            strum(GTR, b, B, ch, [(0, 1, "d", "!"), (1, 1, "d", "!"), (2, 1.5, "d", "!")])
            DRUM.bar(b, "D3:1! D3:1! D3:1! R:1"); CELLO.bar(b, f"{nm(r + 12)}:1 {nm(r + 12)}:1 {nm(r + 12)}:2")
        if i == 1: DRUM.bar(b, "R:2 D3:1, R:1")
        continue
    bodhran(DRUM, b, B, "hornpipe")
    strum(GTR, b, B, ch, HP if n != "1周目" else [(0, 1, "d", "!"), (2, 1, "d", ",")])
    if n in ("2周目", "3周目"):
        harp_ostinato(c.HARP, b, B, tones(ch, "D4", "D5")[:3])
        CELLO.bar(b, f"{nm(r + 12)}:1.5 R:0.5 {nm(r + 19)}:1.5 R:0.5")
    if n == "3周目":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
rich(c, choir_scenes=["3周目"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.28 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の016（第2版・明るく速めの曲）。古い石垣に沿ってはずむ足どり。ホーンパイプ（付点ではねる）AABB、4/4・♩=96、D ミクソリディア→E。1周ごとに曲がり角で一瞬止まり、最後の曲がり角でほんとうに止まる。",
       harm_scenes=None, tail_scene="終わり", fill=False, pads=False)
