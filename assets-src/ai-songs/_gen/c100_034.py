# ケルト・フルート100曲「銀の笛と百の夜」034 苔の絨毯 Carpet of Moss — 第2版（2026-10-28）
# イメージ: 倒れた古木をおおう、厚い苔の絨毯。座りこむと、体がゆっくり沈んでいくように柔らかい。音も、ゆっくりと低い方へ沈んでいく。
#   最後は、笛のいちばん低い音と、コントラバスのいちばん低い音が、苔の下の土のように鳴る。
# 形（台帳）: スロー・エア（いちばん低い音域まで沈む）。3/4・♩=42。F♯ エオリア。始め：低音／終わり：低音。山なし。
# 編曲の表:
#   低音   : コントラバスとチェロの低い F♯
#   沈む1  : 笛（中くらいの高さ）＋チェロ＋低い弦
#   沈む2  : 笛がだんだん低く。竪琴の低い分散和音
#   苔     : 笛は低い所だけ。弦の暗い和音、パッド
#   土     : 笛のいちばん低い音、コントラバス
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "034-carpet-of-moss", "苔の絨毯", "Carpet of Moss", 42, 3, "F#", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.35})
C8 = ["F#m", "D", "Bm", "C#m", "F#m", "A", "E", "F#m"]
S.scene("低音", 2, "intro", ["F#m", "F#m"])
S.scene("沈む1", 16, "verse", C8 * 2)
S.scene("沈む2", 24, "verse", C8 * 3)
S.scene("苔", 16, "verse", ["F#m", "D", "F#m", "C#m", "D", "Bm", "C#m", "F#m"] * 2)
S.scene("土", 4, "outro", ["F#m"] * 4)
NAMES = ["低音", "沈む1", "沈む2", "苔", "土"]

c = make(S, NAMES,
         [("低音", 0, 0.62), ("沈む1", 0, 0.64), ("沈む2", 0, 0.66), ("苔", 0, 0.66), ("土", 0, 0.6), ("土", 3, 0.38)],
         {}, flute_gain={n: 1.25 for n in NAMES}, intro="低音", passing=True, tension=False)
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.11, pan=0.0, reverb=0.45, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.09, pan=0.15, reverb=0.45, barGain=c.g())

H = ["5:2 4:1", "3:1.5 2:0.5 1:1", "2:2 3:1", "4:3", "5:2 6:1", "5:1.5 4:0.5 3:1", "2:2 1:1", "1:3"]          # F♯4〜C♯5 あたり
M = ["3:2 2:1", "1:1.5 7,:0.5 6,:1", "7,:2 1:1", "2:3", "3:2 1:1", "7,:1.5 6,:0.5 5,:1", "6,:2 7,:1", "1:3"]   # 低く
L_ = ["1:2 7,:1", "6,:3", "5,:2 6,:1", "7,:3", "1:2 6,:1", "5,:3", "6,:2 7,:1", "5,:3"]                         # いちばん低い所（C♯4 まで）
play_melody(c, "沈む1", H + H[:7] + ["1:3"], 4, "air", density=0.5, seed=3401)
play_melody(c, "沈む2", M + H[:4] + M[4:] + M, 4, "air", density=0.6, seed=3402)
play_melody(c, "苔", L_ + L_, 4, "air", density=0.4, seed=3403)
play_melody(c, "土", ["5,:3", "5,:3", "R:3", "R:3"], 4, "air", density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2")
    CB.bar(b, f"{nm(r if r >= 28 else r + 12)}:3" if not (n == "土" and i == 3) else "R:3")
    if n != "低音" and not (n == "土" and i >= 2): CELLO.bar(b, f"{nm(r + 12)}:3")
    if n in ("沈む1", "沈む2", "苔"):
        v = voice(ch, 52 if n != "苔" else 48, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
    if n in ("沈む2", "苔"): c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "F#2", "F#4")[:3]))
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の034（第2版）。倒木をおおう苔の絨毯。3/4・♩=42、F♯ エオリア。スロー・エアの旋律が、ゆっくり低い方へ沈んでいき、最後は笛のいちばん低い音とコントラバスが苔の下の土のように鳴る。",
       harm_scenes=None, tail_scene="土", fill=False, pads=True, pad_scenes=["沈む2", "苔"])
json.dump({"pre": 1.0, "tail": 8.0, "layers": [{"file": "0136", "db": -34, "hp": 80, "lp": 4000, "wide": 0.016, "duck": 0.3, "fade": 8}],
           "fx": {"glass": {"hz": [185.0, 370.0, 554.4], "db": -29, "rt": 7.0, "start": 4}, "shimmer": {"db": -28, "rt": 9.0}, "far": {"db": -24, "delay": 0.3, "lp": 2000, "rt": 5.0},
                  "haze": {"db": -25, "rt": 9.0}, "band": {"db": -38, "hz": 5000, "per": 31}}, "intro_db": 8.5}, open("/tmp/cel/w/air034.json", "w"))
