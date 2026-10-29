# ケルト・フルート100曲「銀の笛と百の夜」039 妖精の輪 The Ring of Little Lights — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 夜の森の草地に、小さな光が輪になって舞っている。はじめは輪の外から、遠くの踊りをそっと眺めている（小さく遠い音）。
#   ふと輪の真ん中に招き入れられ、時間がゆっくりになる（エア）。そして今度は輪の中で、一緒に踊る（全員）。虫の声が6拍子の揺れと重なる。
# 形（台帳）: ジグ→エア→ジグの入れ子（輪の外→輪の中）。6/8・付点4分＝78。D ドリア。始め：輪の外（遠く小さく）／終わり：輪の中（全員）。終盤に山。
# 編曲の表:
#   輪の外  : 遠い竪琴と虫の声
#   ジグ1   : 遠くの踊り：笛（小さめ）＋竪琴＋ピチカート。伴奏は少なく
#   エア    : 輪の真ん中：時間がゆっくりになる。笛の長い音、弦、竪琴の倍音
#   ジグ2   : 輪の中で一緒に踊る：全員（ボーランはやわらかく、ギター、弦、笛の和声）。山
#   輪の中  : 全員で和音をのばして止まる
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 234
S = Song("C100", "039-the-ring-of-little-lights", "妖精の輪", "The Ring of Little Lights", BPM, 6, "D", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["Dm", "Dm", "C", "Am", "Dm", "G", "C", "Dm"]; BC = ["F", "C", "G", "Am", "F", "C", "G", "Dm"]
S.scene("輪の外", 4, "intro", ["Dm", "Dm", "C", "Dm"])
S.scene("ジグ1", 64, "verse", (AC * 2 + BC * 2) * 2)
S.scene("エア", 16, "break", ["Dm", "F", "C", "Dm", "G", "Am", "C", "Dm"] * 2)
S.scene("ジグ2", 64, "chorus", (AC * 2 + BC * 2) * 2)
S.scene("輪の中", 8, "outro", ["Dm", "C", "Dm", "Dm", "Dm", "Dm", "Dm", "Dm"])
NAMES = ["輪の外", "ジグ1", "エア", "ジグ2", "輪の中"]

c = make(S, NAMES, [("輪の外", 0, 0.6), ("ジグ1", 0, 0.7), ("ジグ1", 63, 0.74), ("エア", 0, 0.64), ("ジグ2", 0, 0.8), ("ジグ2", 56, 0.95), ("輪の中", 0, 0.86), ("輪の中", 7, 0.5)],
         {}, flute_gain={"輪の外": 1.0, "ジグ1": 1.05, "エア": 1.2, "ジグ2": 1.1, "輪の中": 1.1}, intro="輪の外", passing=True, tension=False)
DRUM = S.track("ボーラン（やわらかく）", "guitar", patch="frameDrum", volume=0.09, pan=-0.15, reverb=0.35, modulate=False, barGain=c.g())
GTR = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.045, pan=0.3 + 0.04 * i, reverb=0.35, barGain=c.g()) for i in range(4)]
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.055, pan=-0.35, reverb=0.4, barGain=c.g())
A = ["1:2 2:1 3:2 4:1", "5:2 3:1 1:3", "2:2 3:1 4:2 5:1", "6:3 5:3", "4:2 5:1 6:2 4:1", "5:2 3:1 1:2 3:1", "2:2 1:1 7,:2 2:1", "1:6"]
Bm = ["5:2 6:1 7:2 1':1", "2':3 1':3", "7:2 6:1 5:2 6:1", "7:3 5:3", "1':2 7:1 6:2 5:1", "4:2 6:1 5:3", "4:2 3:1 2:2 7,:1", "1:6"]
T = A + A + Bm + Bm
play_melody(c, "ジグ1", T + T, 4, "jig", density=0.5, seed=3901)
play_melody(c, "エア", ["5:6", "6:3 5:3", "4:6", "3:6", "2:3 3:3", "4:6", "3:3 2:3", "1:6"] * 2, 4, "air", density=0.6, seed=3902)
play_melody(c, "ジグ2", T + T, 4, "jig", density=1.0, seed=3903)
play_melody(c, "輪の中", ["1:3 5:3", "1':6", "1':6", "R:6", "R:6", "R:6", "R:6", "R:6"], 4, "air", density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5")
    if n == "輪の外":
        c.HARP2.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "D5", "D6")[:3]) + " R:3")
        v = voice(ch, 55, 3, spread=True)   # 夜の草地の空気
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        c.LOW.bar(b, f"{nm(r)}:6")
        if i >= 2: c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:1 {nm(t[4 % len(t)])}:2 {nm(t[2])}:1")
        continue
    if n == "ジグ1":
        c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:1 {nm(t[4 % len(t)])}:2 {nm(t[2])}:1")
        PIZZ.bar(b, f"{nm(r + 12)}:3 {nm(r + 19)}:3")
        bodhran(DRUM, b, B, "jig", var=0, soft=True)                     # 遠くの踊りの足音（やわらかく）
        strum(GTR, b, B, ch, JIG_STRUM_LIGHT)
        v = voice(ch, 53, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        c.LOW.bar(b, f"{nm(r)}:3 {nm(r + 7)}:3")
    if n == "エア":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        c.HARP2.bar(b, f"R:3 {nm(tones(ch, 'D5', 'D6')[1])}:3")
        c.LOW.bar(b, f"{nm(r)}:6")
    if n == "ジグ2":
        bodhran(DRUM, b, B, "jig", var=1 if i % 4 == 3 else 0, soft=False)
        strum(GTR, b, B, ch, JIG_STRUM)
        c.HARP.bar(b, f"{nm(t[0])}:1 {nm(t[2])}:1 {nm(t[4 % len(t)])}:1 {nm(t[2])}:1 {nm(t[4 % len(t)])}:1 {nm(t[2])}:1")
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        c.LOW.bar(b, f"{nm(r)}:3 {nm(r + 7)}:3")
    if n == "輪の中" and i < 6:
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        if i == 0: strum(GTR, b, B, ch, [(0, 6, "d", "!")]); DRUM.bar(b, "D3:3! R:3")
        if i < 3: c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "D4", "D6")[i * 2:i * 2 + 6]))
rich(c, choir_scenes=["ジグ2"], pulse_scenes=["エア", "ジグ2"], guitar=False, pizz=False, inner=True)
thick(c); sparkle(c)   # 2026-10-29: 速い曲の厚さ（023 7.27→7.53・025 7.26→7.66）＋高いきらめき
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.32 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の039（第2版・明るく速めの曲）。夜の草地の、小さな光の輪の踊り。6/8・付点4分＝78、D ドリア。ジグ→エア→ジグ：輪の外から遠くの踊りを眺め（小さく遠い）、輪の真ん中で時間がゆっくりになり、輪の中で一緒に踊る（全員）。虫の声が6拍子と重なる。",
       harm_scenes=None, tail_scene="輪の中", fill=False, pads=True, pad_scenes=["ジグ1", "エア", "ジグ2"], floor=True)
BEAT3 = 3 * 60 / BPM
json.dump({"pre": 1.2, "tail": 7.0, "layers": [{"file": "0425", "db": -36, "hp": 1500, "lp": 9000, "wide": 0.012, "pan": -0.2, "duck": 0.35, "fade": 6}, {"file": "0621", "db": -36, "hp": 120, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 6}],
           "fx": {"glass": {"hz": [293.7, 587.3, 880.0], "db": -29, "rt": 6.0, "start": 3}, "shimmer": {"db": -27, "rt": 8.0}, "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5},
                  "haze": {"db": -27, "rt": 8.0}, "band": {"db": -37, "hz": 7000, "per": 23}}, "intro_db": 8.5}, open("/tmp/cel/w/air039.json", "w"))
