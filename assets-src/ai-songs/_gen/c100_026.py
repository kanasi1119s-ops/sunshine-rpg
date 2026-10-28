# ケルト・フルート100曲「銀の笛と百の夜」026 小さな滝の祈り Prayer at the Falls — 第2版（2026-10-28）
# イメージ: 森の小さな滝の前で、エイラが手を合わせる。弦の和音が、祈りの歌（コラール）のように静かに動く。
#   笛は少しずつ上がっては止まる祈りの節。途中で、笛の音が滝の音の中に溶けて聞こえなくなり（祈りが水に吸いこまれる）、
#   やがて水の中から、澄んだ長い音が浮かび上がる。
# 形（台帳）: 祈りのコラール（弦の和音が半小節ずつ動く上で、上がって止まる旋律）。4/4・♩=54。B ドリア。始め：水の音／終わり：澄んだ長い音。中盤に山。
# 編曲の表:
#   水       : 滝の音→弦がそっと入る
#   祈り1    : 弦のコラール＋チェロ＋笛
#   祈り2    : ＋竪琴のゆっくりした分散和音。中盤の山（笛がいちばん高く、弦が広がる）
#   溶ける   : 滝の音が大きくなり、笛はだんだん小さく、聞こえなくなる。弦だけが残る
#   澄んだ音 : 水の中から、笛の澄んだ長い音
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 54
S = Song("C100", "026-prayer-at-the-falls", "小さな滝の祈り", "Prayer at the Falls", BPM, 4, "B", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.25})
C1 = ["Bm|A", "D|E", "Bm|F#m", "G|A", "D|A", "Bm|E", "A|F#m", "Bm|Bm", "G|D", "A|E", "Bm|F#m", "G|A", "D|G", "Bm|A", "E|F#m", "Bm|Bm"]
S.scene("水", 2, "intro", ["Bm", "Bm"])
S.scene("祈り1", 16, "verse", C1)
S.scene("祈り2", 16, "chorus", C1)
S.scene("溶ける", 8, "break", ["Bm|A", "G|A", "Bm|E", "Bm|Bm", "G|D", "A|E", "Bm|A", "Bm|Bm"])
S.scene("澄んだ音", 12, "outro", ["Bm", "E", "Bm", "A", "Bm", "E", "Bm", "Bm", "Bm", "Bm", "Bm", "Bm"])
NAMES = ["水", "祈り1", "祈り2", "溶ける", "澄んだ音"]

c = make(S, NAMES,
         [("水", 0, 0.6), ("祈り1", 0, 0.64), ("祈り1", 15, 0.68), ("祈り2", 0, 0.72), ("祈り2", 11, 0.9), ("祈り2", 15, 0.74), ("溶ける", 0, 0.7),
          ("澄んだ音", 0, 0.62), ("澄んだ音", 11, 0.36)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="水", passing=True, tension=False)
# 溶ける：笛がだんだん小さく、聞こえなくなる
s0 = c.s0["溶ける"]
c.FLUTE.spec["barGain"] = [round(x * (max(0.15, 1 - 0.2 * (b - s0)) if s0 <= b < s0 + 8 else 1.0), 3) for b, x in enumerate(c.FLUTE.spec["barGain"])]
CELLO = S.track("チェロ（コラールの低い声）", "strings", patch="cello", volume=0.09, pan=0.1, reverb=0.5, barGain=c.g())

P1 = ["5,:1 6,:1 7,:2", "1:1 2:1 3:2", "2:4", "R:4", "3:1 4:1 5:2", "6:1 7:1 1':2", "7:4", "R:4",
      "4:1 5:1 6:2", "7:2 6:2", "5:4", "R:4", "3:1 4:1 5:1 6:1", "5:2 3:2", "1:4", "R:4"]
P2 = ["3:1 4:1 5:2", "6:1 7:1 1':2", "7:4", "R:4", "5:1 6:1 7:2", "1':2 7:1 6:1", "5:4", "R:4",
      "6:1 7:1 1':2", "1':4", "7:2 6:2", "5:4", "4:1 5:1 6:1 5:1", "4:2 2:2", "1:4", "R:4"]
play_melody(c, "祈り1", P1, 4, "air", density=0.6, seed=2601)
play_melody(c, "祈り2", P2, 4, "air", density=0.8, seed=2602)
play_melody(c, "溶ける", ["3:1 4:1 5:2", "6:1 7:1 1':2", "7:4", "6:4", "5:4", "4:4", "3:4", "R:4"], 4, "air", density=0.4, seed=2603)
play_melody(c, "澄んだ音", ["R:4", "R:2 5:2", "1':4", "1':4", "7:2 6:2", "5:4", "1:4", "1:4", "R:4", "R:4", "R:4", "R:4"], 4, "air", density=0.3, seed=2604)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); chs = S.chords[b].split("|")
    if n == "水" and i == 0: continue
    for h, ch in enumerate(chs if len(chs) == 2 else chs * 2):
        v = voice(ch, 55 if n != "祈り2" or i < 8 else 59, 3, spread=True)
        for j in range(3): c.STR[j].at(b * B + 2 * h, f"{nm(v[j])}:2")
        r = low(ch, "C2"); r = r + 12 if r < 40 else r
        if n != "水" and not (n == "澄んだ音" and i >= 10): CELLO.at(b * B + 2 * h, f"{nm(r)}:2")
    if n == "祈り2" or (n == "澄んだ音" and 2 <= i < 8):
        t = tones(chs[0], "D3", "D5"); c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2])))
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の026（第2版）。森の小さな滝の前の祈り。4/4・♩=54、B ドリア。弦のコラールの上で、少しずつ上がっては止まる祈りの節。途中で笛が滝の音の中に溶けて聞こえなくなり、やがて水の中から澄んだ長い音が浮かび上がる。",
       harm_scenes=None, tail_scene="澄んだ音", fill=False, pads=True, pad_scenes=["祈り1", "祈り2", "溶ける", "澄んだ音"])
BAR = 4 * 60 / BPM; t_melt = c.s0["溶ける"] * BAR
air = {"pre": 2.5, "tail": 8.0, "layers": [{"file": "0219", "db": -30, "hp": 120, "lp": 8000, "wide": 0.016, "duck": 0.3, "fade": 6},
                                           {"file": "0219", "db": -22, "hp": 120, "lp": 9000, "wide": 0.02, "duck": 0.0, "start": round(t_melt, 1), "end": round(t_melt + 8 * BAR, 1), "fade": 9, "pan": 0.1}],
       "fx": {"glass": {"hz": [493.9, 987.8, 1480.0], "db": -27, "rt": 7.0, "start": 4}, "shimmer": {"db": -26, "rt": 9.0}, "far": {"db": -25, "delay": 0.3, "lp": 2600, "rt": 5.0},
              "haze": {"db": -26, "rt": 9.0}, "band": {"db": -37, "hz": 6500, "per": 23}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air026.json", "w"), ensure_ascii=False)
