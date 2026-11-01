# ケルト・フルート100曲「銀の笛と百の夜」087 祖父の最後の曲 Grandfather's Last Tune — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 雪の峰の小屋で、エイラは祖父が最後に書いた曲の楽譜を見つける。曲は途中で終わっていた。
#   エイラは祖父の節を吹き、変奏しながら自分の音にしていき、最後に、祖父が書けなかった終わりの句を、自分の節で吹く。
#   001 で竪琴が呼んだ問いの3音（レ・ミ・ラ）は、ここで初めて、答えの3音（ラ・ミ・レ）になって、D に落ち着く。
# 調べ: 悲しみ。形: 主題と変奏（竪琴の前奏 → 祖父の主題 → 変奏3つ → エイラの終わりの句）。
# 拍子・速さ: 前奏は ♩=46（ゆれを大きく）→ 3/4・♩=60。旋法: E ドリア（最後は同じ音のまま、D に落ち着く）。
# 主役は笛（祖父の節 → エイラの節）。伴奏の主役: 金属弦の竪琴（001 と同じ竪琴の響き：長く鳴らす手と止める手。3度を抜いた和音）。
#   ギター・ピアノ・パッド・弦・打楽器・2本目の笛は使わない。
# この曲だけ: 001 の「問いの3音」（レ・ミ・ラ。上がる）が、ここで初めて「答えの3音」（ラ・ミ・レ。下りる）になる。
#   祖父の主題の中には問いの3音が2回隠れていて、エイラの終わりの句で答えに変わる。
# 始まり: 竪琴の前奏 → 終わり: エイラの新しい終わりの句。
# 山: 終盤（3つ目の変奏）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "087-grandfathers-last-tune", "祖父の最後の曲", "Grandfather's Last Tune", 60, 3, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("E", "dorian", 4)
CT = ["Em", "Em", "D", "A", "A", "Bm", "D", "Em", "Em", "A", "Em", "A", "G", "Em", "D", "Em"]
CE = ["Em", "Em", "A", "D", "A", "D", "Em", "A", "A", "D", "D", "D"]
SC = [("竪琴の前奏", 4, "intro", ["Em", "D", "A", "D"]), ("祖父の主題", 16, "verse", CT), ("変奏1", 16, "verse", CT), ("変奏2", 16, "verse", CT),
      ("変奏3", 16, "chorus", CT), ("エイラの終わり", 12, "outro", CE)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("竪琴の前奏", 0, 0.7), ("祖父の主題", 0, 0.7), ("変奏1", 0, 0.72), ("変奏2", 0, 0.76), ("変奏3", 0, 0.84), ("変奏3", 14, 0.9), ("エイラの終わり", 0, 0.76),
          ("エイラの終わり", 11, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="竪琴の前奏", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 46}, {"bar": s["祖父の主題"] + 1, "bpm": 60, "ramp": 2}]
B = S.beats
G = c.g()
# 001 と同じ金属弦の竪琴（長く鳴らす手・止める手・高い鐘）
HR = S.track("竪琴（響かせる）", "harp", patch="folkHarp", volume=0.13, pan=-0.18, reverb=0.55, sustain=2.6, barGain=G)
HD = S.track("竪琴（止める）", "harp", patch="folkHarp", volume=0.11, pan=-0.05, reverb=0.4, sustain=0.45, barGain=G)
HB = S.track("竪琴（高い鐘）", "harp", patch="folkHarp", volume=0.06, pan=0.35, reverb=0.7, sustain=3.0, barGain=G)
def roll(tr, b, notes, start=0.0, step=0.22, L=3.0, soft=True):
    for k, m in enumerate(notes): tr.at(round(b * B + start + k * step, 3), f"{nm(m)}:{L}{',' if (k and soft) else ''}")

# ---------- 旋律（1=E4。問いの3音「レ・ミ・ラ」＝7,・1・4 が主題に2回隠れている） ----------
Q = "7,:1 1:1 4:1"                          # 問い（上がる）：D4 E4 A4
ANS = "4:1 1:1 7,:1"                        # 答え（下りる）：A4 E4 D4
T = ["1:2 3:1", "5:1 4:1 3:1", "2:2 1:1", Q, "5:2 6:1", "7:1 6:1 5:1", "4:1 3:1 2:1", "3:3",
     "1':2 7:1", "6:1 5:1 4:1", "5:2 3:1", Q, "3:2 4:1", "5:1 3:1 2:1", "1:1 2:1 7,:1", "1:3"]
V3 = ["5:2 1':1", "2':1 1':1 7:1", "6:2 5:1", Q, "1':2 2':1", "3':1 2':1 1':1", "7:1 6:1 5:1", "6:3",
      "2':2 1':1", "7:1 6:1 5:1", "6:2 5:1", Q, "5:2 6:1", "7:1 5:1 4:1", "3:1 2:1 7,:1", "1:3"]       # エイラの変奏（高く）
END = ["5:2 4:1", "3:1 2:1 1:1", ANS, "7,:3", "1':2 6:1", "5:1 4:1 3:1", "2:2 3:1", "4:3", ANS, "7,:3", "7,:3", "R:3"]
play_melody(c, "祖父の主題", T, 4, "air", key=K, density=0.1, seed=8701)
play_melody(c, "変奏1", T, 4, "air", key=K, density=0.3, seed=8702)
play_melody(c, "変奏2", T, 4, "air", key=K, density=0.35, seed=8703)
play_melody(c, "変奏3", V3, 4, "air", key=K, density=0.4, seed=8704)
play_melody(c, "エイラの終わり", END, 4, "air", key=K, density=0.15, seed=8705)

# ---------- 竪琴（3度を抜いた和音。前奏は 001 のように問いの3音で呼ぶ） ----------
OPEN = {"Em": (40, 47, 52, 54), "D": (38, 45, 50, 52), "A": (45, 52, 57, 59), "Bm": (47, 54, 59, 61), "G": (43, 50, 55, 57)}
roll(HR, 0, [38, 45, 50, 52, 57], step=0.3)
HD.bar(1, "D4:1 E4:1 A4:1"); HR.at(1 * B + 2, "A4:3")                       # 問いの3音（001 と同じ）
roll(HR, 2, [45, 52, 57, 59], step=0.35)
roll(HR, 3, [38, 45, 50], step=0.4, soft=False)
for b in range(s["祖父の主題"], c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; d = OPEN[ch]
    if n == "エイラの終わり" and i >= 9:
        if i == 9: roll(HR, b, [38, 45, 50, 57, 62, 69], step=0.45, L=9)      # 最後は D に落ち着く
        continue
    if n == "祖父の主題":
        if i % 2 == 0: roll(HR, b, d[:3], step=0.3)
    elif n == "変奏1":
        roll(HR, b, d[:3], step=0.25); HD.at(round(b * B + 2, 3), f"{nm(d[3] + 12)}:1,")
    elif n == "変奏2":                                                       # 止める手の対旋律（8分で）
        HR.at(b * B, f"{nm(d[0])}:3")
        HD.bar(b, " ".join(f"{nm(x)}:0.5," for x in (d[1] + 12, d[2] + 12, d[3] + 12, d[2] + 12, d[1] + 12, d[2] + 12)))
    elif n == "変奏3":
        roll(HR, b, list(d), step=0.18)
        if i % 4 == 0: HB.at(b * B, f"{nm(d[2] + 24)}:4,")
    else:
        roll(HR, b, d[:3], step=0.35)
        if i in (2, 8): HB.at(b * B, "A6:4,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.32 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の087（第3版）。雪の峰の小屋で、途中で終わった祖父の最後の曲を見つける。E ドリア、3/4。001 と同じ金属弦の竪琴が、001 と同じ問いの3音（レ・ミ・ラ）で呼ぶ前奏（♩=46）。笛が祖父の主題（♩=60。問いの3音が2回隠れている）を吹き、3つの変奏で自分の節にしていく（3つ目が山）。最後に、祖父が書けなかった終わりの句をエイラが吹き、問いの3音が初めて答えの3音（ラ・ミ・レ）になって、D に落ち着く。",
       harm_scenes=None, tail_scene="エイラの終わり", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air087.json", "w"), ensure_ascii=False)
