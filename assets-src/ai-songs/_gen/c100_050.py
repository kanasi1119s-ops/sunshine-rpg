# ケルト・フルート100曲「銀の笛と百の夜」050 石に眠る歌 The Song Asleep in the Stone — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第5章の終わり。蔦の部屋の床の石に、祖父が刻んだ溝がある。指でたたくと、溝のリズムが歌のリズムだと分かる。
#   エイラはまず石をたたいてリズムだけを鳴らし、そこに笛で音をつけていく。眠っていた歌が目をさまし、最後は全員で歌って止まる。
# 調べ: 喜び。形: 打音が先にリズムを刻み、そこに音がつく（A：打音だけ → 打音と笛 → B：打音だけ → 打音と笛 → 全員）。
# 拍子・速さ: 4/4・♩=96。旋法: G エオリア。
# 主役は笛（刻む笛）。伴奏の主役: 枠太鼓の縁の打音（石をたたく音。カホンのような乾いた音）。音がついてから、チェロのピチカートの低音、全員の歌で竪琴。
#   ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 旋律のリズムを、音のない打音が先に刻む（打音のリズムと笛のリズムが、1音残らず同じ）。
# 始まり: 石をたたく律動だけ → 終わり: 全員の歌で止まる。
# 山: 終盤に1つ（全員の歌）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "050-the-song-asleep-in-the-stone", "石に眠る歌", "The Song Asleep in the Stone", 96, 4, "G", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("G", "minor", 4)
CA = ["Gm", "Cm", "Gm", "D", "Gm", "Cm", "D", "Gm"]
CB = ["Bb", "Eb", "Cm", "D", "Bb", "F", "D", "Gm"]
SC = [("Aの律動", 8, "intro", CA), ("Aの歌", 16, "verse", CA * 2), ("Bの律動", 8, "verse", CB), ("Bの歌", 16, "verse", CB * 2),
      ("Aの歌2", 16, "verse", CA * 2), ("全員の歌", 32, "chorus", (CA + CB) * 2), ("止まる", 2, "outro", ["Gm", "Gm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("Aの律動", 0, 0.7), ("Aの歌", 0, 0.72), ("Bの律動", 0, 0.72), ("Bの歌", 0, 0.76), ("Aの歌2", 0, 0.78), ("全員の歌", 0, 0.86), ("全員の歌", 31, 0.94),
          ("止まる", 0, 0.94)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="Aの律動", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
ST = [S.track(f"石の打音{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.12 + 0.24 * j, reverb=0.3,
              barGain=[round(x * (2.0 if S.scene_of(b)[0].endswith("律動") else 1.0), 3) for b, x in enumerate(G)]) for j in range(2)]
VP = S.track("チェロ（ピチカートの低音）", "strings", patch="pizzicato", volume=0.12, gainDb=5, pan=-0.2, reverb=0.35, barGain=G)
HP = S.track("竪琴（全員の歌）", "harp", patch="folkHarp", volume=0.06, pan=0.3, reverb=0.5, sustain=1.6, barGain=G)

A = ["1:0.5 1:0.5 3:1 1:0.5 5:1.5", "4:0.5 3:0.5 2:1 1:1 7,:1", "1:0.5 1:0.5 3:1 5:0.5 6:1.5", "5:1 4:0.5 3:0.5 2:2",
     "1:0.5 1:0.5 3:1 1:0.5 5:1.5", "6:0.5 5:0.5 4:1 3:1 2:1", "3:0.5 2:0.5 1:1 7,:0.5 2:1.5", "1:2 R:2"]
Bm = ["5:1 5:0.5 6:0.5 7:1 5:1", "1':1.5 7:0.5 6:2", "4:1 4:0.5 5:0.5 6:1 4:1", "5:1.5 4:0.5 3:2",
      "5:1 5:0.5 6:0.5 7:1 1':1", "2':1.5 1':0.5 7:1 5:1", "6:0.5 5:0.5 4:0.5 3:0.5 2:1 7,:1", "1:2 R:2"]

def knock(bars, b0, both=False):
    """旋律のリズムを、音のない打音で（長い音は大きい太鼓 C3、短い音は小さい太鼓 E3）"""
    for j, s_ in enumerate(bars):
        t = (b0 + j) * B; q = 0
        for tok in s_.split():
            d, L = tok.split(":"); L = float(L)
            if d != "R":
                x = "C3" if L >= 1 else "E3"                     # 1回目（7.74）: C#3・F#3 はほとんど鳴らず、打音だけの所が -44dB だった → C3・E3 に
                mk = "!" if abs(t % 2) < 1e-6 else ("" if L >= 1 else ",")
                ST[(b0 + j) % 2].at(round(t, 3), f"{x}:{min(L, 1.0)}{mk}")
                if both: ST[(b0 + j + 1) % 2].at(round(t + 0.012, 3), f"{x}:{min(L, 1.0)}{mk}")     # 打音だけの所は2つ重ねる（試し書き出しで笛より約18dB 小さかった）
            t += L; q += 1
for sc, mel in (("Aの律動", A), ("Aの歌", A + A), ("Bの律動", Bm), ("Bの歌", Bm + Bm), ("Aの歌2", A + A), ("全員の歌", A + Bm + A + Bm)):
    knock(mel, c.s0[sc], both=sc.endswith("律動"))
play_melody(c, "Aの歌", A + A, 4, "march", key=K, density=0.25, seed=5001)
play_melody(c, "Bの歌", Bm + Bm, 4, "march", key=K, density=0.3, seed=5002)
play_melody(c, "Aの歌2", A + A, 4, "march", key=K, density=0.35, seed=5003)
play_melody(c, "全員の歌", A + Bm + A + Bm, 4, "march", key=K, density=0.45, seed=5004)
s0 = c.s0["止まる"]
c.FLUTE.at(s0 * B, "G5:2!"); ST[0].at(s0 * B, "C3:1!"); VP.at(s0 * B, "G2:1!"); HP.at(s0 * B, "G3:3!")

# ---------- チェロのピチカート（音がついてから）と竪琴（全員の歌） ----------
ROOT = {"Gm": 43, "Cm": 48, "D": 50, "Bb": 46, "Eb": 51, "F": 41}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    if n.endswith("律動") or n == "止まる": continue
    VP.bar(b, f"{nm(r - 12 if r - 12 >= 36 else r)}:1 R:1 {nm(r - 5 if r - 5 >= 36 else r + 7)}:1, R:1")
    if n == "全員の歌":
        th = r + (3 if ch.endswith("m") else 4)
        HP.bar(b, " ".join(f"{nm(x)}:0.5{',' if q % 2 else ''}" for q, x in enumerate((r + 12, r + 19, th + 24, r + 24, th + 24, r + 19, r + 12, r + 19))))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の050（第3版）。第5章の終わり、床の石に刻まれた溝のリズム。4/4・♩=96、G エオリア。まず石をたたく乾いた打音（枠太鼓）が歌のリズムだけを刻み、そこに笛が同じリズムで音をつける（打音と笛のリズムは1音残らず同じ）。A と B をそれぞれ打音だけ → 打音と笛の順に鳴らし、チェロのピチカートと竪琴が加わって、最後は全員の歌で止まる。",
       harm_scenes=None, tail_scene="止まる", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.4}}}
json.dump(air, open("/tmp/cel/w/air050.json", "w"), ensure_ascii=False)
