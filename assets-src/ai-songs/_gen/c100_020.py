# ケルト・フルート100曲「銀の笛と百の夜」020 星の草原 Meadow of Stars — 第2版（2026-10-28）
# イメージ: 夜の草原に寝ころぶ。風がやみ、まわりの虫たちが、ゆっくりと拍を刻みはじめる。その拍に合わせて、笛が空に向かって歌う。
#   拍を刻むのは、楽器ではなく虫の声だけ。最後は、空いっぱいの星（高いグロッケン）が見えて終わる。
# 形（台帳）: スロー・エア AABA（虫の声が拍を刻む）。4/4・♩=52。D リディア（G♯の夜の浮遊感）。始め：風／終わり：星。山なし。
# 編曲の表:
#   風     : 夜の風→弦のごくうすい持続
#   空1    : 笛＋弦のうすい持続＋チェロの低い D。拍は虫の声だけ（空気の層で作る）
#   空2    : B から竪琴がときどき1音、笛の和声が少し
#   星     : 高いグロッケンが一つずつ、空いっぱいに
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 52
S = Song("C100", "020-meadow-of-stars", "星の草原", "Meadow of Stars", BPM, 4, "D", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.3})
AC = ["D", "E/D", "D", "Bm", "G", "A", "G", "A"]
A2C = ["D", "E/D", "D", "Bm", "G", "Em", "A", "D"]
BC = ["G", "A", "F#m", "Bm", "G", "E/D", "A", "A"]
S.scene("風", 2, "intro", ["D", "D"])
S.scene("空1", 32, "verse", AC + A2C + BC + A2C)
S.scene("空2", 16, "verse", BC + A2C)
S.scene("星", 8, "outro", ["D", "E/D", "D", "D", "D", "D", "D", "D"])
NAMES = ["風", "空1", "空2", "星"]

c = make(S, NAMES,
         [("風", 0, 0.58), ("空1", 0, 0.62), ("空1", 20, 0.7), ("空1", 31, 0.64), ("空2", 0, 0.68), ("空2", 15, 0.62), ("星", 0, 0.6), ("星", 7, 0.36)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="風", passing=True, tension=False)
CELLO = S.track("チェロ（低い D）", "strings", patch="cello", volume=0.07, pan=0.0, reverb=0.5, barGain=c.g())
GLOCK = S.track("星（グロッケン）", "bell", patch="glockenspiel", volume=0.03, pan=0.35, reverb=0.8, barGain=c.g())

A = ["R:2 5:2", "1':3 7:1", "6:2 5:1 4:1", "5:4", "R:2 3:2", "4:3 5:1", "3:1.5 2:0.5 1:2", "2:4"]
A2 = ["R:2 5:2", "1':3 7:1", "6:2 5:1 4:1", "5:4", "R:2 3:2", "2:3 3:1", "2:1.5 1:0.5 7,:2", "1:4"]
BM = ["R:2 3':2", "2':3 1':1", "7:2 6:1 5:1", "6:4", "R:2 5:2", "4:3 3:1", "2:2 3:2", "5:4"]
play_melody(c, "空1", A + A2 + BM + A2, 4, "air", density=0.7, seed=2001)
play_melody(c, "空2", BM + A2, 4, "air", density=0.9, seed=2002)
play_melody(c, "星", ["5:4", "1':4", "R:4", "R:4", "R:4", "R:4", "R:4", "R:4"], 4, "air", density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b].split("/")[0]
    if n == "風" and i == 0: continue
    if not (n == "星" and i >= 7):
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n in ("空1", "空2") or (n == "星" and i < 5): CELLO.bar(b, "D2:4")
    if n == "空2" and i % 4 == 1: c.HARP.bar(b, f"R:2 {nm(tones(ch, 'D5', 'D6')[1])}:2")
    if n == "星":
        hi = tones(ch, "C6", "C7")
        GLOCK.bar(b, " ".join(f"{nm(hi[(i + q) % len(hi)])}:1" for q in range(min(4, i + 1))) + (" R:" + str(4 - min(4, i + 1)) if i < 3 else ""))
rich(c, choir_scenes=["空2"], pulse_scenes=[], guitar=False, pizz=False, inner=False, choir_vol=0.1)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の020（第2版）。夜の草原に寝ころぶ。4/4・♩=52、D リディア。スロー・エア AABA。拍を刻むのは虫の声だけ（楽器の打楽器はなし）。最後は空いっぱいの星（高いグロッケン）。",
       harm_scenes=None, tail_scene="星", fill=False, pads=True, pad_scenes=["空1", "空2", "星"])
BEAT = 60 / BPM; t0 = c.s0["空1"] * 4 * BEAT; t1 = c.s0["星"] * 4 * BEAT + 3 * 4 * BEAT
air = {"pre": 2.0, "tail": 7.0, "layers": [{"file": "0114", "db": -33, "hp": 150, "lp": 7000, "wide": 0.012, "duck": 0.3, "fade": 10},
                                           {"file": "0908", "db": -40, "hp": 150, "lp": 5000, "wide": 0.014, "pan": 0.25, "duck": 0.3, "fade": 6, "end": 20}],
       "events": [{"t": 0, "pulse": {"from": round(t0, 2), "to": round(t1, 2), "every": round(BEAT, 4), "hz": 4400, "burst": 0.04, "n": 3, "db": -29, "pan": 0.45}}],
       "fx": {"glass": {"hz": [293.7, 587.3, 880.0], "db": -27, "rt": 7.0, "start": 4}, "shimmer": {"db": -26, "rt": 9.0}, "far": {"db": -25, "delay": 0.3, "lp": 2400, "rt": 5.0},
              "haze": {"db": -26, "rt": 9.0}, "band": {"db": -37, "hz": 7000, "per": 29}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air020.json", "w"), ensure_ascii=False)
