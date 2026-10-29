# ケルト・フルート100曲「銀の笛と百の夜」029 水が教える道 The Way the Water Goes — 第2版（2026-10-28）
# イメージ: 道に迷ったエイラが、小川の流れについていく。水はいつも低い方へ、下りながら道を教えてくれる（下りていく旋律が道になる）。
#   流れはひと回りごとに水が増えて太くなり（楽器が増える）、最後に全音上がって、遠くに海の気配がする。
# 形（台帳）: 9/8 のゆっくりした流れ（スリップ・ジグの3つ組）。1周ごとに水が増え、最後に全音上がる。付点4分＝54。E ドリア。
#   始め：小さな流れ（ギター）／終わり：海の予感（広い和音と波）。終盤に小さな山。（007 の 6/8・D ドリアと重ならないように 9/8・E にした）
# 編曲の表:
#   流れ   : ナイロンギターの流れだけ
#   1周目  : 笛（下りる道の節）＋ギター
#   2周目  : ＋竪琴
#   3周目  : ＋弦とチェロ
#   4周目  : F# ドリアへ全音上がる。＋笛の和声（小さな山）
#   海の予感: 広い和音、波の音
import sys, json
from c100_common import *
from c100_v2 import *
from lm25_lib import tr_chord

BPM = 162
S = Song("C100", "029-the-way-the-water-goes", "水が教える道", "The Way the Water Goes", BPM, 9, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
RC = ["Em", "D", "Em", "A", "G", "D", "Em", "Em", "G", "D", "A", "Em", "C", "D", "Bm", "Em"]
S.scene("流れ", 2, "intro", ["Em", "Em"])
for k in range(1, 4): S.scene(f"{k}周目", 16, "verse", RC)
S.scene("4周目", 16, "chorus", [tr_chord(x, 2) for x in RC])
S.scene("海の予感", 8, "outro", ["F#m", "E", "F#m", "D", "F#m", "F#m", "F#m", "F#m"])
NAMES = ["流れ", "1周目", "2周目", "3周目", "4周目", "海の予感"]

c = make(S, NAMES,
         [("流れ", 0, 0.6), ("1周目", 0, 0.62), ("2周目", 0, 0.66), ("3周目", 0, 0.7), ("4周目", 0, 0.78), ("4周目", 12, 0.88), ("海の予感", 0, 0.72), ("海の予感", 7, 0.4)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="流れ", passing=True, tension=False)
GT = S.track("ナイロンギター（流れ）", "guitar", patch="nylonGuitar", volume=0.1, pan=0.3, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.15, reverb=0.45, barGain=c.g())

D1 = ["5:3 4:2 3:1 2:3", "3:2 2:1 1:3 7,:3", "1:3 2:2 3:1 4:3", "5:6 3:3",
      "1':3 7:2 6:1 5:3", "6:2 5:1 4:3 3:3", "4:3 3:2 2:1 7,:3", "1:9"]
D2 = ["3:3 5:2 6:1 7:3", "1':6 7:3", "6:3 5:2 4:1 3:3", "4:6 2:3",
      "5:3 4:2 3:1 2:3", "3:2 2:1 1:3 7,:3", "2:3 1:2 7,:1 6,:3", "1:9"]
play_melody(c, "1周目", D1 + D2, 4, "air", density=0.5, seed=2901)
play_melody(c, "2周目", D1 + D2, 4, "air", density=0.7, seed=2902)
play_melody(c, "3周目", D2 + D1, 4, "air", density=0.9, seed=2903)
play_melody(c, "4周目", D1 + D2, 4, "air", density=1.0, seed=2904, lift=2)
play_melody(c, "海の予感", ["5:6 4:3", "3:9", "2:6 1:3", "1:9", "R:9", "R:9", "R:9", "R:9"], 4, "air", density=0.3, seed=2905, lift=2)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5")
    lv = NAMES.index(n)
    if n != "海の予感" or i < 6:
        GT.bar(b, " ".join(f"{nm(t[x % len(t)])}:1" for x in ((0, 2, 3, 4, 3, 2, 1, 2, 3) if i % 2 == 0 else (1, 3, 4, 5, 4, 3, 2, 3, 4))))
    if lv >= 2 and n != "海の予感": c.HARP.bar(b, f"{nm(r)}:3 {nm(t[2])}:3 {nm(t[4 % len(t)])}:3")
    if lv <= 2:   # 森の空気と、流れの下の深さ：うすい弦2声とチェロ
        v = voice(ch, 50, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:9")
        if lv >= 1: CELLO.bar(b, f"{nm(r)}:9")
    if lv >= 3 or n == "海の予感":
        if not (n == "海の予感" and i == 7):
            v = voice(ch, 55 if n != "海の予感" else 60, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
            CELLO.bar(b, f"{nm(r)}:9")
rich(c, choir_scenes=["4周目"], pulse_scenes=["2周目", "3周目"], guitar=False, pizz=False, inner=True)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の029（第2版）。迷ったエイラが小川の流れについていく。9/8・付点4分＝54、E ドリア→F# ドリア。下りていく旋律が道になり、ひと回りごとに水が増えて楽器が増え、最後に全音上がって海の気配。",
       harm_scenes=None, tail_scene="海の予感", fill=False, pads=True, pad_scenes=["1周目", "2周目", "3周目", "4周目", "海の予感"])
BAR = 9 * 60 / BPM
air = {"pre": 1.0, "tail": 8.0, "layers": [{"file": "0213", "db": -34, "hp": 200, "lp": 8000, "wide": 0.014, "duck": 0.3, "fade": 6, "end": round(c.s0["3周目"] * BAR, 1)},
                                           {"file": "0864", "db": -33, "hp": 150, "lp": 7000, "wide": 0.016, "duck": 0.3, "start": round(c.s0["2周目"] * BAR, 1), "fade": 20},
                                           {"file": "0698", "db": -32, "hp": 100, "lp": 4500, "lfo": [11, 0.4], "wide": 0.016, "duck": 0.2, "start": round(c.s0["海の予感"] * BAR - 6, 1), "fade": 10}],
       "fx": {"glass": {"hz": [329.6, 659.3, 987.8], "db": -28, "rt": 6.0, "start": 4}, "shimmer": {"db": -27, "rt": 8.0}, "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5},
              "haze": {"db": -27, "rt": 8.0}, "band": {"db": -37, "hz": 6500, "per": 23}}, "intro_db": 8.5}
json.dump(air, open("/tmp/cel/w/air029.json", "w"), ensure_ascii=False)
