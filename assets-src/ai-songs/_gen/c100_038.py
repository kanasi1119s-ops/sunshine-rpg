# ケルト・フルート100曲「銀の笛と百の夜」038 夜露 Night Dew — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 森の主に認められた夜。エイラは大きな羊歯の下で休む。葉の先から夜露が1粒、また1粒と落ちる。
#   落ちる間合いはばらばらで、ときどき2粒つづけて落ちる。笛はささやくように子守歌を吹き、最後の1粒が落ちて夜が明ける。
# 調べ: 眠り。形: エア（16小節の歌を3回。あいだに「夜更け」）。
# 拍子・速さ: 3/4・♩=50。旋法: G イオニアの5音（G・A・B・D・E）。
# 主役は笛（ささやく。G4〜E5 が中心、装飾はごく少し）。伴奏の主役: カリンバ（指ピアノ）の点（夜露）。
#   脇: 2小節ごとに、カリンバの低い1音（葉の下の水たまり）。竪琴・ギター・ピアノ・弦・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: カリンバの粒が、拍に合わせず、葉の先から落ちるように不規則な間合いで落ちる（ときどき2粒つづけて）。
# 始まり: カリンバの1音 → 終わり: 最後の1粒。
# 山: なし。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "038-night-dew", "夜露", "Night Dew", 50, 3, "G", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
K = Key("G", "major", 4)
VA = ["G", "Em", "D", "G", "C", "G", "Em", "D", "G", "C", "G", "D", "Em", "C", "D", "G"]
SC = [("一粒", 4, "intro", ["G"] * 4), ("歌1", 16, "verse", VA), ("歌2", 16, "verse", VA), ("夜更け", 8, "verse", ["Em", "D", "C", "G"] * 2),
      ("歌3", 16, "verse", VA), ("歌4", 16, "verse", VA), ("最後の一粒", 4, "outro", ["G"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("一粒", 0, 0.64), ("歌1", 0, 0.66), ("歌2", 0, 0.68), ("夜更け", 0, 0.64), ("歌3", 0, 0.68), ("歌4", 0, 0.66), ("最後の一粒", 0, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="一粒", passing=True, tension=False)
B = S.beats
G = c.g()
# 試し書き出し: 夜露の粒（0.09）は笛より 5〜15dB 小さい → 0.14。水たまりの低い1音は笛と同じくらいで、すぐ減衰する
DEW = [S.track(f"カリンバ（夜露{j + 1}）", "kalimba", volume=0.14, pan=p, reverb=0.6, sustain=2.4, barGain=G) for j, p in enumerate((-0.5, -0.1, 0.3, 0.6))]
# 1回目（7.38）: カリンバだけの始まり（約14秒）が -56〜-72dB とほぼ無音だった → 始まりは別のパート（gainDb 14）で、粒を多めに
DEWI = [S.track(f"カリンバ（始まりの夜露{j + 1}）", "kalimba", volume=0.14, gainDb=14, pan=p, reverb=0.6, sustain=2.4, barGain=G) for j, p in enumerate((-0.4, 0.4))]
POOL = S.track("カリンバ（葉の下の水たまり）", "kalimba", volume=0.1, pan=0.0, reverb=0.5, sustain=2.6, barGain=G)

# ---------- 歌（G の5音。1=G4） ----------
SONG = ["3:2 2:1", "1:2 6,:1", "5,:2 6,:1", "1:3", "2:1 3:1 5:1", "3:2 2:1", "1:1 2:1 3:1", "2:3",
        "3:2 5:1", "6:2 5:1", "3:1 2:1 1:1", "2:3", "3:1 2:1 1:1", "6,:2 5,:1", "6,:1 1:1 2:1", "1:3"]
SONG2 = ["5:2 6:1", "1':2 6:1", "5:2 3:1", "2:3", "3:1 5:1 6:1", "5:2 3:1", "2:1 1:1 2:1", "3:3",
         "5:2 3:1", "2:2 1:1", "6,:1 1:1 2:1", "3:3", "2:1 1:1 6,:1", "5,:2 6,:1", "1:1 2:1 6,:1", "1:3"]
play_melody(c, "歌1", SONG, 4, "air", key=K, density=0.1, seed=3801)
play_melody(c, "歌2", SONG2, 4, "air", key=K, density=0.15, seed=3802)
play_melody(c, "夜更け", ["3:3", "2:3", "1:3", "R:3", "5,:3", "6,:3", "1:3", "R:3"], 4, "air", key=K, density=0.0)
play_melody(c, "歌3", SONG2, 4, "air", key=K, density=0.15, seed=3803)
play_melody(c, "歌4", SONG, 4, "air", key=K, density=0.1, seed=3804)
play_melody(c, "最後の一粒", ["3:3", "1:3", "R:3", "R:3"], 4, "air", key=K, density=0.0)

# ---------- 夜露（拍に合わせない、ばらばらの間合い） ----------
DROPS = [79, 81, 83, 86, 88, 91]                     # G5〜G6（5音）
rng = random.Random(3838)
t = 0.0
end = (c.s0["最後の一粒"] + 2) * B
used = {i: -9.0 for i in range(4)}
while t < end:
    n = S.scene_of(int(t // B))[0]
    gap = rng.expovariate(1 / (2.4 if n in ("歌1", "歌2", "歌3", "歌4") else 1.6))
    t += max(0.45, gap)
    if t >= end: break
    j = rng.randrange(4)
    if t < 4 * B:                                     # 始まり：大きいパートで
        if t - used.get(10 + j % 2, -9) >= 0.5:
            DEWI[j % 2].at(round(t, 3), f"{nm(rng.choice(DROPS))}:1"); used[10 + j % 2] = t + 1
        continue
    if t - used[j] < 0.5: continue
    m = rng.choice(DROPS)
    DEW[j].at(round(t, 3), f"{nm(m)}:1{',' if rng.random() < 0.5 else ''}"); used[j] = t + 1
    if rng.random() < 0.18:                         # ときどき2粒つづけて
        j2 = (j + 1) % 4
        if t + 0.22 - used[j2] >= 0.5:
            DEW[j2].at(round(t + 0.22, 3), f"{nm(rng.choice(DROPS))}:1,"); used[j2] = t + 1.22
DEW[1].at(round((c.NB - 2) * B + 1.3, 3), "D6:2")                   # 最後の1粒
# 葉の下の水たまり：2小節ごとに低い1音
ROOT = {"G": 55, "Em": 52, "D": 50, "C": 48}
for b in range(0, c.NB - 2, 2):
    POOL.at(b * B, f"{nm(ROOT[S.chords[b]] + 12 if ROOT[S.chords[b]] < 60 else ROOT[S.chords[b]])}:{2 * B},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の038（第3版）。大きな羊歯の下で休む夜、葉の先から夜露が落ちる。エア（3/4・♩=50）、G の5音。カリンバの粒が、拍に合わせずばらばらの間合いで（ときどき2粒つづけて）落ち、笛はささやくように子守歌を吹く。始まりはカリンバの1音、最後の1粒が落ちて夜が明ける。",
       harm_scenes=None, tail_scene="最後の一粒", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air038.json", "w"), ensure_ascii=False)
