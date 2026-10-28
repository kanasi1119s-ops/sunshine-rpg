# ケルト・フルート100曲「銀の笛と百の夜」032 木漏れ日 Dappled Light — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 昼の森。風が梢をゆらすと、木の葉のすき間から日の光がちらちら揺れて落ちてくる。揺れるたびに、高い所で光が1つ瞬く。
#   ふっと風がやむと、光も一瞬止まる（全員が1つの和音で静止）。また風が吹いて、揺れがもどる。
# 形（台帳）: スリップ・ジグ（9/8・揺れる3つ組）AABB。付点4分＝90。A ドリア。始め：ゆらぎ（竪琴）／終わり：ゆらぎ。2周目と最後に山。
# 編曲の表:
#   ゆらぎ  : 竪琴の3音のゆれだけ
#   1周目   : 笛＋竪琴＋ピチカート。グロッケンが小節のどこかで1つ瞬く
#   2周目   : ＋弦＋チェロ。笛の装飾が増える（山）
#   静止    : 全員が1つの和音で止まる（風がやむ）
#   3周目   : 揺れがもどる。笛の和声（山）
#   ゆらぎ  : 竪琴と瞬きだけに戻る
import sys, random
from c100_common import *
from c100_v2 import *

BPM = 270
S = Song("C100", "032-dappled-light", "木漏れ日", "Dappled Light", BPM, 9, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["Am", "D", "Am", "G", "Am", "D", "G", "Am"]
BC = ["C", "G", "Am", "Em", "C", "G", "G", "Am"]
S.scene("ゆらぎ", 4, "intro", ["Am", "Am", "G", "Am"])
S.scene("1周目", 32, "verse", AC * 2 + BC * 2)
S.scene("2周目", 32, "chorus", AC * 2 + BC * 2)
S.scene("静止", 4, "break", ["D", "D", "D", "D"])
S.scene("3周目", 32, "chorus", AC * 2 + BC * 2)
S.scene("ゆらぎ2", 16, "outro", ["Am", "D", "Am", "G", "Am", "D", "G", "Am", "Am", "Am", "G", "Am", "Am", "Am", "Am", "Am"])
NAMES = ["ゆらぎ", "1周目", "2周目", "静止", "3周目", "ゆらぎ2"]

c = make(S, NAMES,
         [("ゆらぎ", 0, 0.64), ("1周目", 0, 0.68), ("2周目", 0, 0.76), ("2周目", 28, 0.9), ("静止", 0, 0.72), ("3周目", 0, 0.8), ("3周目", 28, 0.92),
          ("ゆらぎ2", 0, 0.7), ("ゆらぎ2", 15, 0.4)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="ゆらぎ", passing=True, tension=False)
GLOCK = S.track("光の瞬き（グロッケン）", "bell", patch="glockenspiel", volume=0.03, pan=0.3, reverb=0.7, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.06, pan=-0.35, reverb=0.35, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.15, reverb=0.4, barGain=c.g())

A = ["5:2 3:1 1:2 3:1 5:3", "6:2 5:1 4:2 6:1 5:3", "3:2 5:1 1':2 7:1 6:2 5:1", "4:2 3:1 2:3 5,:3",
     "5:2 3:1 1:2 3:1 5:3", "6:2 7:1 1':2 6:1 5:3", "4:2 6:1 5:2 3:1 2:2 7,:1", "1:3 3:2 1:1 5,:3"]
Bm = ["1':2 7:1 6:2 7:1 1':3", "2':2 1':1 7:2 5:1 6:3", "5:2 6:1 7:2 1':1 2':3", "1':2 7:1 6:3 5:3",
      "1':2 7:1 6:2 7:1 1':3", "2':2 3':1 2':2 1':1 7:3", "4:2 6:1 5:2 3:1 2:2 7,:1", "1:3 3:2 1:1 5,:3"]
TUNE = A + A + Bm + Bm
play_melody(c, "1周目", TUNE, 4, "jig", density=0.5, seed=3201)
play_melody(c, "2周目", TUNE, 4, "jig", density=1.0, seed=3202)
play_melody(c, "静止", ["6:9", "6:9", "R:9", "R:9"], 4, "air", density=0)
play_melody(c, "3周目", TUNE, 4, "jig", density=1.1, seed=3203)
play_melody(c, "ゆらぎ2", ["5:3 3:3 1:3", "6:6 5:3", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9", "R:9"], 4, "air", density=0.3, seed=3204)

rg = random.Random(32); B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t3 = tones(ch, "E4", "E5")[:3]
    if n == "静止":   # 風がやむ：全員が1つの和音で止まる
        if i < 2:
            v = voice(ch, 57, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
            CELLO.bar(b, f"{nm(r)}:9"); c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, 'D4', 'D6')[:6]) + " R:6")
        continue
    if not (n == "ゆらぎ2" and i >= 14):
        c.HARP.bar(b, " ".join(f"{nm(t3[q % 3])}:1" for q in range(9)))
    # 光の瞬き：小節のどこかで1つ（揺れるたびに）
    if n != "ゆらぎ" or i >= 2:
        if not (n == "ゆらぎ2" and i >= 13):
            p = rg.choice([2, 4, 5, 7]); hi = tones(ch, "C6", "C7")
            GLOCK.bar(b, f"R:{p} {nm(rg.choice(hi))}:1 R:{8 - p}")
    if n in ("1周目", "2周目", "3周目"): PIZZ.bar(b, f"{nm(r + 12)}:3 R:3 {nm(r + 19)}:3")
    if n in ("2周目", "3周目"):
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
        CELLO.bar(b, f"{nm(r)}:9")
rich(c, choir_scenes=["3周目"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の032（第2版・明るく速めの曲）。昼の森の木漏れ日。スリップ・ジグ（9/8・付点4分＝90）AABB、A ドリア。光が揺れるたびに高い所で1つ瞬き（グロッケン）、風がやむと全員が1つの和音で静止する。",
       harm_scenes=None, tail_scene="ゆらぎ2", fill=False, pads=False)
import json
json.dump({"pre": 0.6, "tail": 6.0, "layers": [{"file": "0905", "db": -36, "hp": 150, "lp": 7000, "wide": 0.016, "duck": 0.4, "fade": 6}, {"file": "0935", "db": -38, "hp": 400, "lp": 9000, "wide": 0.012, "pan": 0.25, "duck": 0.45, "fade": 8}],
           "fx": {"glass": {"hz": [440.0, 880.0, 1318.5], "db": -30, "rt": 5.0, "start": 3}, "shimmer": {"db": -28, "rt": 6.5}, "far": {"db": -26, "delay": 0.2, "lp": 3000, "rt": 3.5},
                  "haze": {"db": -29, "rt": 6.0}, "band": {"db": -37, "hz": 7000, "per": 17}}, "intro_db": 6.0}, open("/tmp/cel/w/air032.json", "w"))
