# ケルト・フルート100曲「銀の笛と百の夜」038 夜露 Night Dew — 第2版（2026-10-28）
# イメージ: 夜の森。葉の先にたまった雫が、ぽとん、ぽとんと落ちる。その間隔が、そのまま曲の拍になる。
#   笛は雫の拍の上で、ゆっくり歌う。雫は増えも減りもせず、ただ同じ間隔で落ち続け、最後の一滴で終わる。
# 形（台帳）: 雫が拍を刻むスロー・エア（雫の間隔＝拍。雫の音は竪琴の高いハーモニクスとピチカートの「ぽとん」で作る）。
#   4/4・♩=60。E ミクソリディア。始め：一滴／終わり：一滴。山なし。
# 編曲の表:
#   一滴   : 雫の音1つ
#   雫     : 雫が1拍ごとに（高い竪琴とピチカートが交互）。弦のごく弱い持続
#   歌1    : 笛のスロー・エア A A'
#   歌2    : 笛 B A'。チェロ、パッド
#   静けさ : 笛が休み、雫と弦だけ
#   一滴   : 雫が1つずつ間をあけて、最後の一滴
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "038-night-dew", "夜露", "Night Dew", 57, 4, "E", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.25})
AC = ["E", "D", "A", "E", "E", "D", "B", "E"]; BC = ["A", "E", "D", "A", "C#m", "D", "B", "E"]
S.scene("一滴", 2, "intro", ["E", "E"])
S.scene("雫", 4, "intro", ["E", "E", "D", "E"])
S.scene("歌1", 16, "verse", AC * 2)
S.scene("歌2", 16, "verse", BC + AC)
S.scene("静けさ", 8, "break", AC)
S.scene("歌3", 8, "verse", AC)
S.scene("最後の一滴", 4, "outro", ["A", "E", "E", "E"])
NAMES = ["一滴", "雫", "歌1", "歌2", "静けさ", "歌3", "最後の一滴"]

c = make(S, NAMES, [("一滴", 0, 0.62), ("歌1", 0, 0.62), ("歌2", 0, 0.66), ("静けさ", 0, 0.6), ("歌3", 0, 0.62), ("最後の一滴", 0, 0.56), ("最後の一滴", 3, 0.45)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro=None, passing=True, tension=False)
DROPH = S.track("雫（竪琴の高い音）", "harp", patch="folkHarp", volume=0.08, pan=0.3, reverb=0.75, barGain=c.g())
DROPP = S.track("雫（ピチカート）", "strings", patch="pizzicato", volume=0.06, pan=-0.3, reverb=0.7, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.1, reverb=0.5, barGain=c.g())

A1 = ["R:2 5:2", "6:3 5:1", "4:2 3:2", "2:4", "R:2 3:2", "4:2 5:1 6:1", "5:3 4:1", "3:4"]
A2 = ["R:2 5:2", "6:3 5:1", "4:2 3:2", "2:4", "R:2 3:2", "2:2 7,:1 2:1", "1:3 7,:1", "1:4"]
B1 = ["R:2 1':2", "7:3 6:1", "5:2 6:2", "4:4", "R:2 3:2", "4:2 6:2", "5:3 4:1", "5:4"]
play_melody(c, "歌1", A1 + A2, 4, "air", density=0.6, seed=3801)
play_melody(c, "歌2", B1 + A2, 4, "air", density=0.8, seed=3802)
play_melody(c, "歌3", A2, 4, "air", density=0.6, seed=3803)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    hi = tones(ch, "E5", "E6")
    if n == "一滴":
        if i == 0: DROPH.bar(b, f"R:2 {nm(hi[0])}:2")
        if i == 1: DROPH.bar(b, f"R:1 {nm(hi[1])}:1 R:1 {nm(hi[2])}:1")
        v = voice(ch, 52, 3, spread=True)        # 夜の森の空気：低い弦とチェロ（はじまりが小さすぎないように）
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        CELLO.bar(b, f"{nm(r)}:4")
        continue
    if n == "最後の一滴":
        if i in (0, 1, 3): DROPH.bar(b, f"{nm(hi[i % len(hi)])}:2 R:2")
        if i < 3:
            v = voice(ch, 55, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
            CELLO.bar(b, f"{nm(r)}:4")
        continue
    # 雫：1拍ごとに、竪琴とピチカートが交互（雫の間隔＝拍）
    DROPH.bar(b, f"{nm(hi[(b) % len(hi)])}:1 R:1 {nm(hi[(b + 1) % len(hi)])}:1 R:1")
    DROPP.bar(b, f"R:1 {nm(hi[(b + 2) % len(hi)] - 12)}:1 R:1 {nm(hi[(b + 1) % len(hi)] - 12)}:1")
    v = voice(ch, 55, 3 if n in ("歌2", "歌3") else 2, spread=True)
    for j in range(len(v)): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n in ("雫", "歌1", "歌2", "静けさ", "歌3"): CELLO.bar(b, f"{nm(r)}:4")
play_melody(c, "最後の一滴", ["3:2 2:2", "1:4", "R:4", "R:4"], 4, "air", density=0.2, seed=3804)
rich(c, choir_scenes=["歌2"], pulse_scenes=["歌2", "静けさ", "歌3"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の038（第2版）。夜の森の葉先の雫。4/4・♩=57、E ミクソリディア。雫の音（高い竪琴とピチカートが交互）が1拍ごとに落ち、その間隔がそのまま曲の拍になる。笛はその上でゆっくり歌い、最後の一滴で終わる。",
       harm_scenes=None, tail_scene="最後の一滴", fill=False, pads=True, pad_scenes=["雫", "歌1", "歌2", "静けさ", "歌3", "最後の一滴"], floor=True)
json.dump({"pre": 1.5, "tail": 8.0, "layers": [{"file": "0621", "db": -33, "hp": 120, "lp": 6000, "wide": 0.014, "duck": 0.3, "fade": 6}],
           "fx": {"glass": {"hz": [329.6, 659.3, 987.8], "db": -28, "rt": 7.0, "start": 4}, "shimmer": {"db": -26, "rt": 9.0}, "far": {"db": -24, "delay": 0.3, "lp": 2400, "rt": 5.0},
                  "haze": {"db": -26, "rt": 9.0}, "band": {"db": -38, "hz": 6500, "per": 29}}, "intro_db": 8.5}, open("/tmp/cel/w/air038.json", "w"))
