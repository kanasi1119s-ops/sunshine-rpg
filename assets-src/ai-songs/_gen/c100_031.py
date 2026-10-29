# ケルト・フルート100曲「銀の笛と百の夜」031 森の入口 At the Edge of the Wood — 第2版（2026-10-28）
# イメージ: 古い森の手前で立ち止まる。中は暗く、何がいるのか分からない。笛で「入ってもいい？」と短く問いかけると、
#   森が低い声（チェロと低い弦の暗い和音）で答える。問いかけるたびに、空気は少しずつ暗く、狭くなる（答えの和音が低く、暗くなる）。
#   ためらったあと、意を決して一歩ずつ進み、最後に森の中へ足を踏み入れる。
# 形（台帳）: 問いと森の答え。4/4・♩=54。E ドリア。始め：風／終わり：足を踏み入れる（足音1つと暗い和音）。山なし。
# 編曲の表:
#   風      : 風の音と、ごく弱い低い弦
#   問い1   : 笛が2小節問い、森（低い弦とチェロ）が2小節答える。答えは回ごとに低く
#   問い2   : 問いが少し大胆に（上へ）。チェロが動く
#   ためらい: 笛の長い音と、低いドローンだけ
#   一歩    : 笛がつながった節で歩き出す。ピチカートの足どり、竪琴の低い音
#   森へ    : 足音1つと、暗い和音
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 54
S = Song("C100", "031-at-the-edge-of-the-wood", "森の入口", "At the Edge of the Wood", BPM, 4, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.3})
QC = ["Em", "Em", "C", "Am", "Em", "D", "Bm", "Em", "Em", "Em", "C", "Am", "D", "D", "Bm", "Em"]
S.scene("風", 3, "intro", ["Em", "Em", "Em"])
S.scene("問い1", 16, "verse", QC)
S.scene("問い2", 16, "verse", QC)
S.scene("ためらい", 8, "break", ["Em", "C", "Em", "Am", "Em", "C", "Bm", "Em"])
S.scene("一歩", 16, "verse", ["Em", "D", "C", "D", "Em", "Am", "Bm", "Em", "C", "D", "Em", "Am", "C", "Bm", "Em", "Em"])
S.scene("森へ", 4, "outro", ["Em", "C", "Em", "Em"])
NAMES = ["風", "問い1", "問い2", "ためらい", "一歩", "森へ"]

c = make(S, NAMES,
         [("風", 0, 0.58), ("問い1", 0, 0.62), ("問い2", 0, 0.66), ("ためらい", 0, 0.6), ("一歩", 0, 0.66), ("一歩", 15, 0.72), ("森へ", 0, 0.66), ("森へ", 3, 0.4)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="風", passing=True, tension=False)
CELLO = S.track("チェロ（森の声）", "strings", patch="cello", volume=0.1, pan=0.1, reverb=0.5, barGain=c.g())
PIZZ = S.track("ピチカート（足どり）", "strings", patch="pizzicato", volume=0.07, pan=-0.25, reverb=0.4, barGain=c.g())
STEP = S.track("足音", "guitar", patch="frameDrum", volume=0.07, pan=-0.1, reverb=0.5, modulate=False, barGain=c.g())

Q1 = [("R:1 1:1 2:1 3:1", "5:3 R:1"), ("R:1 3:1 4:1 5:1", "7:2 6:1 5:1"), ("R:1 5:1 4:1 3:1", "2:3 R:1"), ("R:1 1:1 3:1 5:1", "6:3 R:1")]
Q2 = [("R:1 6:1 5:1 4:1", "3:2 4:2"), ("R:1 1':1 7:1 6:1", "5:3 R:1"), ("R:1 4:1 3:1 2:1", "1:3 R:1"), ("R:1 2:1 3:1 5:1", "4:3 R:1")]
def qa(qs): return sum([[a, b, "R:4", "R:4"] for a, b in qs], [])
play_melody(c, "問い1", qa(Q1), 4, "air", density=0.5, seed=3101)
play_melody(c, "問い2", qa(Q2), 4, "air", density=0.7, seed=3102)
play_melody(c, "ためらい", ["5:4", "R:4", "4:2 3:2", "R:4", "2:4", "R:4", "1:4", "R:4"], 4, "air", density=0.4, seed=3103)
play_melody(c, "一歩", ["1:1 2:1 3:1 5:1", "4:2 3:1 2:1", "3:1 4:1 5:2", "6:2 5:2", "5:1 4:1 3:1 2:1", "3:2 1:2", "2:1 3:1 4:1 2:1", "1:4",
                        "3:1 4:1 5:1 7:1", "6:2 5:1 4:1", "5:1 6:1 7:2", "1':4", "7:1 6:1 5:1 3:1", "4:2 2:2", "3:1 2:1 7,:1 2:1", "1:4"], 4, "air", density=0.8, seed=3104)
play_melody(c, "森へ", ["R:4", "R:4", "R:4", "R:4"], 4, "air", density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "風":
        if i >= 1:
            v = voice(ch, 50, 2, spread=True)
            for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:4")
        continue
    if n in ("問い1", "問い2"):
        unit = i // 4; ph = i % 4
        k_ = unit + (4 if n == "問い2" else 0)            # 何回目の答えか（0〜7）
        if ph in (0, 1):   # 問い：うすい弦だけ
            v = voice(ch, 55, 2, spread=True)
            for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:4")
        else:              # 答え：森の声。回ごとに低く、暗く
            v = voice(ch, 55 - 2 * k_, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
            CELLO.bar(b, f"{nm(r)}:4" if ph == 2 else f"{nm(r)}:2 {nm(r - 2 if r - 2 >= 36 else r + 10)}:2")
            if k_ < 3: c.HARP2.bar(b, f"R:2 {nm(tones(ch, 'E5', 'E6')[0])}:2") if ph == 2 else None
    if n == "ためらい":
        CELLO.bar(b, "E2:4")
        v = voice(ch, 47, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "一歩":
        PIZZ.bar(b, f"{nm(r)}:1 R:1 {nm(r + 7)}:1 R:1")
        c.HARP.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        CELLO.bar(b, f"{nm(r)}:4")
        v = voice(ch, 50, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i % 2 == 0: STEP.bar(b, "D3:1, R:3")
    if n == "森へ":
        if i == 1: STEP.bar(b, "D3:1 R:3")
        if i >= 1:
            v = voice(ch, 45, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4" if i < 3 else "R:4")
            CELLO.bar(b, f"{nm(r)}:4" if i < 3 else "R:4")
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の031（第2版）。古い森の入口で立ち止まる。4/4・♩=54、E ドリア。笛が短く問いかけ、森（低い弦とチェロ）が答える。答えは回ごとに低く暗くなる。ためらったあと一歩ずつ進み、森の中へ足を踏み入れる。",
       harm_scenes=None, tail_scene="森へ", fill=False, pads=True, pad_scenes=["問い2", "ためらい", "一歩"])
air = {"pre": 1.5, "tail": 8.0, "layers": [{"file": "0595", "db": -33, "hp": 80, "lp": 4000, "lfo": [37, 0.4], "wide": 0.012, "duck": 0.3, "fade": 6, "end": 140},
                                           {"file": "0905", "db": -35, "hp": 100, "lp": 5000, "wide": 0.016, "duck": 0.3, "start": 60, "fade": 30},
                                           {"file": "0136", "db": -34, "hp": 80, "lp": 3500, "wide": 0.018, "duck": 0.25, "start": 200, "fade": 30}],
       "fx": {"glass": {"hz": [329.6, 659.3, 987.8], "db": -29, "rt": 6.0, "start": 4}, "shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -24, "delay": 0.3, "lp": 2200, "rt": 5.0},
              "haze": {"db": -26, "rt": 9.0}, "band": {"db": -37, "hz": 5500, "per": 23}, "ramp": [0.6, 1.8]}, "intro_db": 8.5}
json.dump(air, open("/tmp/cel/w/air031.json", "w"), ensure_ascii=False)
