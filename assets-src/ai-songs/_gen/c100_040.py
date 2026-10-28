# ケルト・フルート100曲「銀の笛と百の夜」040 暁の森 Dawn in the Forest — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 長い夜が明ける森。はじめは、夜の名残の静かな節（梟との問答の節を思い出すように）。一羽、また一羽と鳥が目を覚まし、
#   そのたびに楽器が1つずつ加わって、リールの拍が立ち上がる。最後は鳥の大合唱と、明るい朝の和音。
# 形（台帳）: リズムから積み上げるリール（鳥の声が増えるのと一緒に楽器が増える）・夜の旋律の明るい返し。4/4・♩=100。A イオニア。
#   始め：静か（笛ひとり、夜の旋律）／終わり：鳥の合唱。終盤に明るい山。
# 編曲の表:
#   夜の名残 : 笛ひとり（夜の節をゆっくり。長調に返して）
#   目覚め   : ボーランがやわらかくリールの拍を刻みはじめる
#   1周目    : ＋ギターのストローク。笛のリール
#   2周目    : ＋竪琴の3音オスティナート＋チェロ
#   3周目    : ＋弦＋笛の和声（明るい山）
#   鳥の合唱 : 明るい和音、鳥の声がいっぱいに
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "040-dawn-in-the-forest", "暁の森", "Dawn in the Forest", 100, 4, "A", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["A", "D", "A", "E", "A", "D", "E", "A"]; BC = ["D", "A", "D", "E", "D", "Bm", "E", "A"]
S.scene("夜の名残", 8, "intro", ["A", "D", "A", "E", "D", "A", "E", "A"])
S.scene("目覚め", 4, "intro", ["A", "A", "D", "E"])
for k in range(1, 4): S.scene(f"{k}周目", 32, "verse" if k < 3 else "chorus", AC * 2 + BC * 2)
S.scene("鳥の合唱", 8, "outro", ["A", "D", "A", "A", "A", "A", "A", "A"])
NAMES = ["夜の名残", "目覚め", "1周目", "2周目", "3周目", "鳥の合唱"]

c = make(S, NAMES, [("夜の名残", 0, 0.6), ("目覚め", 0, 0.64), ("1周目", 0, 0.68), ("2周目", 0, 0.76), ("3周目", 0, 0.86), ("3周目", 28, 0.96), ("鳥の合唱", 0, 0.86), ("鳥の合唱", 7, 0.5)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="夜の名残", passing=True, tension=False)
DRUM = S.track("ボーラン", "guitar", patch="frameDrum", volume=0.07, pan=-0.15, reverb=0.3, modulate=False, barGain=c.g())
GTR = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.05, pan=0.3 + 0.04 * i, reverb=0.3, barGain=c.g()) for i in range(5)]
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.2, reverb=0.4, barGain=c.g())

NIGHT = ["3:1 4:1 5:2", "6:2 5:2", "4:3 R:1", "5:4", "1':1 7:1 6:2", "5:2 4:1 3:1", "2:3 R:1", "1:4"]
A = ["1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "6:0.5 4:0.5 2:0.5 4:0.5 6:1 5:1",
     "4:0.5 3:0.5 2:0.5 3:0.5 4:0.5 5:0.5 6:0.5 7:0.5", "1':1 7:0.5 6:0.5 5:2",
     "1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "6:0.5 1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5",
     "3:0.5 5:0.5 4:0.5 2:0.5 7,:0.5 2:0.5 5,:0.5 7,:0.5", "1:2 1:1 5,:1"]
Bm = ["1':0.5 7:0.5 6:0.5 7:0.5 1':1 5:1", "2':0.5 1':0.5 7:0.5 1':0.5 2':1 7:1",
      "1':0.5 7:0.5 6:0.5 7:0.5 1':0.5 2':0.5 1':0.5 6:0.5", "7:1 6:0.5 5:0.5 6:2",
      "1':0.5 7:0.5 6:0.5 7:0.5 1':1 5:1", "2':0.5 1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5",
      "3:0.5 5:0.5 4:0.5 2:0.5 7,:0.5 2:0.5 5,:0.5 7,:0.5", "1:2 1:1 5,:1"]
T = A + A + Bm + Bm
play_melody(c, "夜の名残", NIGHT, 4, "air", density=0.5, seed=4001)
play_melody(c, "目覚め", ["R:4", "R:4", "R:4", "R:2 5,:1 7,:1"], 4, "air", density=0)
for k in range(1, 4): play_melody(c, f"{k}周目", T, 4, "reel", density=0.4 + 0.3 * k, seed=4001 + k)
play_melody(c, "鳥の合唱", ["1':4", "2':2 1':2", "1':4", "R:4", "R:4", "R:4", "R:4", "R:4"], 4, "air", density=0)

B = S.beats
REEL = [(0, 0.5, "d", "!"), (0.5, 0.5, "u", ","), (1, 0.5, "d", ""), (1.5, 0.5, "u", "!"), (2, 0.5, "d", "!"), (2.5, 0.5, "u", ","), (3, 0.5, "d", ""), (3.5, 0.5, "u", "!")]
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "夜の名残":
        v = voice(ch, 52, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:4")
        continue
    if n == "目覚め": bodhran(DRUM, b, B, "reel", soft=True); continue
    if n == "鳥の合唱":
        if i == 0: strum(GTR, b, B, ch, [(0, 4, "d", "!")]); DRUM.bar(b, "D3:1! R:3")
        if i < 6:
            v = voice(ch, 60, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
            if i < 3: c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "A3", "A6")[i * 3:i * 3 + 8]))
        continue
    bodhran(DRUM, b, B, "reel", var=i % 2)
    strum(GTR, b, B, ch, REEL if n != "1周目" else [(0, 1, "d", "!"), (2, 1, "d", "")])
    if n in ("2周目", "3周目"):
        harp_ostinato(c.HARP, b, B, tones(ch, "E4", "E5")[:3])
        CELLO.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    if n == "3周目":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
rich(c, choir_scenes=["3周目"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.28 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の040（第2版・明るく速めの曲）。長い夜が明ける森。リズムから積み上げるリール（4/4・♩=100）、A イオニア。夜の名残の静かな節→鳥が目を覚ますたびに楽器が1つずつ加わり、最後は鳥の大合唱と明るい朝の和音。",
       harm_scenes=None, tail_scene="鳥の合唱", fill=False, pads=False)
BAR = 4 * 60 / 100
json.dump({"pre": 1.0, "tail": 8.0, "layers": [{"file": "0621", "db": -36, "hp": 120, "lp": 6000, "wide": 0.014, "duck": 0.3, "fade": 6, "end": round(14 * BAR, 1)},
                                               {"file": "0935", "db": -35, "hp": 400, "lp": 9500, "wide": 0.014, "duck": 0.35, "start": round(8 * BAR, 1), "fade": 20},
                                               {"file": "0999", "db": -33, "hp": 400, "lp": 9500, "wide": 0.016, "pan": 0.2, "duck": 0.3, "start": round(44 * BAR, 1), "fade": 30},
                                               {"file": "0222", "db": -31, "hp": 400, "lp": 9500, "wide": 0.016, "pan": -0.2, "duck": 0.2, "start": round(76 * BAR, 1), "fade": 30}],
           "fx": {"glass": {"hz": [440.0, 880.0, 1318.5], "db": -30, "rt": 5.0, "start": 4}, "shimmer": {"db": -28, "rt": 6.5}, "far": {"db": -26, "delay": 0.2, "lp": 3000, "rt": 3.5},
                  "haze": {"db": -29, "rt": 6.0}}, "intro_db": 8.5}, open("/tmp/cel/w/air040.json", "w"))
