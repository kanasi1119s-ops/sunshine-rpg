# ケルト・フルート100曲「銀の笛と百の夜」030 水車の夜明け Mill at First Light — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 夜明け前の暗い水車小屋。水車は回り続けている（3拍子のワルツ＝水車の回転）。空が白みはじめると、
#   同じ節が、暗い短調から明るいリディアの長調に生まれ変わる。朝日が差しこむ所で、いちばん明るい山。
# 形（台帳）: 速いワルツ（3/4・♩=132）。同じ旋律が、暗（E エオリア）→明（G リディア）。始め：暗い（低い短調）／終わり：光（明るい和音）。
# 編曲の表:
#   暗い     : 低いピアノのワルツ（ズン・チャ・チャ）だけ
#   夜の回転 : 笛（E エオリア）＋ピアノ＋ピチカート
#   白む     : 和音が G へ動きはじめる。弦が入り、笛は高い所で長い音
#   朝の回転 : 同じ節を G リディア（C♯の光）で。＋竪琴＋グロッケン
#   光1・光2 : 全員（明るい山）。笛の和声
#   朝      : 明るい和音で止まる
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "030-mill-at-first-light", "水車の夜明け", "Mill at First Light", 132, 3, "E", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
NC = ["Em", "Em", "Am", "Em", "Em", "C", "D", "Em", "Em", "Em", "Am", "Em", "C", "D", "B7", "Em",
      "C", "C", "D", "Bm", "C", "Am", "B7", "Em", "C", "C", "D", "Bm", "C", "Am", "B7", "Em"]
LC = ["G", "G", "A", "G", "G", "Em", "D", "G", "G", "G", "A", "G", "Em", "D", "D", "G",
      "Em", "Em", "D", "G", "Em", "A", "D", "G", "Em", "Em", "D", "G", "Em", "A", "D", "G"]
S.scene("暗い", 8, "intro", ["Em", "Em", "Am", "Em", "C", "D", "B7", "Em"])
S.scene("夜の回転", 32, "verse", NC)
S.scene("白む", 32, "verse", ["Em", "C", "G", "D"] * 4 + ["C", "G", "D", "D"] * 4)
S.scene("朝の回転", 32, "verse", LC)
S.scene("光1", 32, "chorus", LC)
S.scene("光2", 32, "chorus", LC)
S.scene("朝", 8, "outro", ["G", "A", "G", "G", "G", "G", "G", "G"])
NAMES = ["暗い", "夜の回転", "白む", "朝の回転", "光1", "光2", "朝"]

c = make(S, NAMES,
         [("暗い", 0, 0.62), ("夜の回転", 0, 0.66), ("白む", 0, 0.68), ("白む", 31, 0.76), ("朝の回転", 0, 0.78), ("光1", 0, 0.84), ("光2", 0, 0.9), ("光2", 28, 0.95),
          ("朝", 0, 0.86), ("朝", 7, 0.5)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="暗い", passing=True, tension=False)
PL = S.track("ピアノ（拍頭の低音）", "piano", volume=0.5, pan=-0.2, reverb=0.4, barGain=c.g())
PR = S.track("ピアノ（裏拍の和音）", "piano", volume=0.37, pan=-0.12, reverb=0.4, barGain=c.g())
PR2 = S.track("ピアノ（裏拍の和音2）", "piano", volume=0.32, pan=-0.08, reverb=0.4, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.055, pan=0.35, reverb=0.35, barGain=c.g())
DRUM = S.track("ボーラン（水車の軸）", "guitar", patch="frameDrum", volume=0.09, pan=-0.15, reverb=0.3, modulate=False, barGain=c.g())
GLOCK = S.track("グロッケン（朝の光）", "bell", patch="glockenspiel", volume=0.026, pan=0.35, reverb=0.65, barGain=c.g())

A1 = ["1:1 3:1 5:1", "6:2 5:1", "4:1 3:1 2:1", "3:3", "1:1 3:1 5:1", "1':2 7:1", "6:1 5:1 4:1", "5:3"]
A2 = A1[:6] + ["4:1 3:1 2:1", "1:3"]
B1 = ["5:1 6:1 7:1", "1':2 5:1", "6:1 7:1 1':1", "2':3", "1':1 7:1 6:1", "5:2 3:1", "4:1 3:1 2:1", "1:3"]
TUNE = A1 + A2 + B1 + B1
KL = S.key.__class__("G", "lydian", 4)
play_melody(c, "夜の回転", TUNE, 4, "jig", density=0.5, seed=3001)
play_melody(c, "白む", ["5:3", "5:3", "1':3", "7:3", "6:3", "5:3", "6:3", "7:3"] * 2 + ["1':3", "1':3", "2':3", "7:3", "1':3", "6:3", "7:3", "7:3"] * 2, 4, "air", density=0.4, seed=3002)
play_melody(c, "朝の回転", TUNE, 4, "jig", key=KL, density=0.7, seed=3003)
play_melody(c, "光1", TUNE, 4, "jig", key=KL, density=1.0, seed=3004)
play_melody(c, "光2", TUNE, 4, "jig", key=KL, density=1.1, seed=3005)
play_melody(c, "朝", ["1':3", "2':3", "1':3", "1':3", "R:3", "R:3", "R:3", "R:3"], 4, "air", key=KL, density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    hi = [x for x in range(57, 72) if x % 12 in chord_pcs(ch)]
    if n == "朝" and i >= 5: continue
    PL.at(b * B, f"{nm(r if n in ('暗い', '夜の回転') else r + 12)}:1")
    PR.at(b * B + 1, f"{nm(hi[0])}:1'"); PR.at(b * B + 2, f"{nm(hi[0])}:1'")
    PR2.at(b * B + 1, f"{nm(hi[1])}:1'"); PR2.at(b * B + 2, f"{nm(hi[1])}:1'")
    if n != "暗い" and n != "朝": bodhran(DRUM, b, B, "waltz") if n in ("朝の回転", "光1", "光2") else DRUM.bar(b, "D3:1, R:2")
    if n in ("暗い", "夜の回転"):   # 夜の小屋の空気：低い弦とチェロ
        v = voice(ch, 50, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:3")
        c.LOW.bar(b, f"{nm(r)}:3")
    if n in ("夜の回転", "光1", "光2"): PIZZ.bar(b, f"{nm(r + 12)}:1 R:2")
    if n in ("白む", "朝の回転", "光1", "光2", "朝"):
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
        c.LOW.bar(b, f"{nm(r)}:3")
    if n in ("朝の回転", "光1", "光2"):
        t = tones(ch, "G4", "G6"); c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in t[:6]))
        if i % 4 == 0: GLOCK.bar(b, f"{nm(tones(ch, 'C6', 'C7')[0])}:3")
rich(c, choir_scenes=["朝の回転", "光1", "光2"], pulse_scenes=["夜の回転", "白む", "朝の回転", "光1", "光2"], guitar=True, pizz=False, inner=True)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の030（第2版・明るく速めの曲）。夜明けの水車。速いワルツ（3/4・♩=132）。水車の回転＝ズン・チャ・チャ。同じ節が暗い E エオリアから、空が白んで G リディアの明るい長調に生まれ変わり、朝日の山へ。",
       harm_scenes=None, tail_scene="朝", fill=False, pads=True, pad_scenes=["夜の回転", "白む", "朝の回転", "光1", "光2"])
import json
d = {"pre": 1.0, "tail": 6.0, "layers": [{"file": "0864", "db": -35, "hp": 150, "lp": 7000, "wide": 0.014, "duck": 0.4, "fade": 6},
                                         {"file": "0222", "db": -36, "hp": 400, "lp": 9000, "wide": 0.012, "pan": 0.25, "duck": 0.4, "start": 95, "fade": 25}],
     "fx": {"glass": {"hz": [392.0, 784.0, 1174.7], "db": -29, "rt": 5.0, "start": 4}, "shimmer": {"db": -28, "rt": 7.0}, "far": {"db": -26, "delay": 0.2, "lp": 3000, "rt": 3.5},
            "haze": {"db": -28, "rt": 7.0}}, "intro_db": 8.5}
json.dump(d, open("/tmp/cel/w/air030.json", "w"))
