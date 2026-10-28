# ケルト・フルート100曲「銀の笛と百の夜」008 港の別れ Parting at the Pier — 第2版（2026-10-28）
# イメージ: 港で旅立つ人を見送る。はじめは岸の人みんなで手を振っている（全員で始まる）。舟が遠ざかるにつれ、声がひとつ、またひとつ聞こえなくなる
#   （楽器が1つずつ抜けていく）。岬を回る直前、最後に大きく手を振る（やわらかい山）。そして一人の笛だけが残る。
# 形（台帳）: 細くなっていく逆アーチ。4/4・♩=58。A エオリア。始め：見送りの全員／終わり：一人の笛。
# 旋律: 下がって上がる別れの節（A 8小節＋B 8小節）。
# 編曲の表（抜けていく順）:
#   見送り  : 全員（ピアノの和音・弦・竪琴・チェロ・ピチカート）
#   手を振る: ピチカートが抜ける
#   遠ざかる1: 竪琴が抜ける。ピアノは右手だけ
#   遠ざかる2: 弦の上の声が抜け、チェロと低い弦だけ
#   岬      : 最後に大きく手を振る（弦がそっと戻り、笛は高い所で）
#   一人    : 笛だけ（と港の空気）
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "008-parting-at-the-pier", "港の別れ", "Parting at the Pier", 58, 4, "A", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
AC = ["Am", "F", "C", "G", "Am", "F", "G", "Am"]
BC = ["F", "Dm", "G", "C", "Dm", "F", "G", "Am"]
S.scene("見送り", 8, "verse", AC)
S.scene("手を振る", 16, "verse", AC + BC)
S.scene("遠ざかる1", 16, "verse", AC + BC)
S.scene("遠ざかる2", 12, "verse", AC + ["Dm", "F", "G", "Am"])
S.scene("岬", 8, "chorus", BC)
S.scene("一人", 8, "outro", AC)
NAMES = ["見送り", "手を振る", "遠ざかる1", "遠ざかる2", "岬", "一人"]

c = make(S, NAMES,
         [("見送り", 0, 0.78), ("手を振る", 0, 0.74), ("遠ざかる1", 0, 0.68), ("遠ざかる2", 0, 0.62), ("遠ざかる2", 11, 0.6),
          ("岬", 0, 0.66), ("岬", 4, 0.8), ("岬", 7, 0.66), ("一人", 0, 0.6), ("一人", 7, 0.45)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro=None, passing=True, tension=False)
PR = S.track("ピアノ（右手）", "piano", volume=0.2, pan=-0.15, reverb=0.45, barGain=c.g())
PR2 = S.track("ピアノ（右手2）", "piano", volume=0.17, pan=-0.12, reverb=0.45, barGain=c.g())
PL = S.track("ピアノ（左手）", "piano", volume=0.2, pan=-0.2, reverb=0.45, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.2, reverb=0.45, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.055, pan=-0.35, reverb=0.4, barGain=c.g())

TA = ["5:1.5 4:0.5 3:1 2:1", "3:2 1:2", "6,:1 7,:1 1:1 2:1", "3:3 R:1",
      "5:1.5 4:0.5 3:1 5:1", "6:2 5:1 4:1", "3:1 2:1 7,:1 2:1", "1:4"]
TB = ["1':1.5 7:0.5 6:1 5:1", "6:2 4:2", "5:1 6:1 7:1 5:1", "6:4",
      "4:1.5 3:0.5 2:1 3:1", "4:2 6:2", "5:1 3:1 2:1 7,:1", "1:4"]
play_melody(c, "見送り", TA, 4, "air", density=0.6, seed=801)
play_melody(c, "手を振る", TA + TB, 4, "air", density=0.8, seed=802)
play_melody(c, "遠ざかる1", TA + TB, 4, "air", density=0.9, seed=803)
play_melody(c, "遠ざかる2", TA + TB[4:], 4, "air", density=0.8, seed=804)
play_melody(c, "岬", ["1':1.5 7:0.5 6:1 5:1", "6:2 1':2", "2':1 1':1 7:1 5:1", "6:4", "4:1.5 3:0.5 2:1 3:1", "4:2 6:2", "5:1 3:1 2:1 7,:1", "1:4"], 4, "air", density=1.0, seed=805)
play_melody(c, "一人", ["5:1.5 4:0.5 3:1 2:1", "3:2 1:2", "6,:1 7,:1 1:1 2:1", "3:4", "5:1.5 4:0.5 3:1 2:1", "1:4", "R:4", "R:4"], 4, "air", density=0.6, seed=806)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5"); hi = [x for x in range(60, 74) if x % 12 in chord_pcs(ch)]
    lvl = NAMES.index(n)
    if n == "一人": continue
    if lvl <= 1 or n == "岬":
        PL.at(b * B, f"{nm(r)}:2"); PL.at(b * B + 2, f"{nm(r + 7)}:2")
    if lvl <= 2 or n == "岬":
        PR.at(b * B, f"{nm(hi[1])}:2"); PR.at(b * B + 2, f"{nm(hi[2 % len(hi)])}:2")
        PR2.at(b * B, f"{nm(hi[0])}:4")
    if lvl <= 3 or n == "岬":
        CELLO.bar(b, f"{nm(r)}:4")
        v = voice(ch, 52 if lvl == 3 else 57, 3 if lvl < 3 or n == "岬" else 2, spread=True)
        for j in range(len(v)): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if lvl <= 1: c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2])))
    if lvl == 0: PIZZ.bar(b, f"{nm(t[1])}:1 R:1 {nm(t[2])}:1 R:1")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の008（第2版）。港の見送り。4/4・♩=58、A エオリア。全員で始まり、舟が遠ざかるにつれて楽器が1つずつ抜けていく（逆アーチ）。岬を回る前に最後に大きく手を振り、一人の笛が残る。",
       harm_scenes=None, tail_scene="一人", fill=False, pads=True, pad_scenes=["見送り", "手を振る", "岬"])
