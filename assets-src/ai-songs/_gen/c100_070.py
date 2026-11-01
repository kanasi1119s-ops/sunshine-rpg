# ケルト・フルート100曲「銀の笛と百の夜」070 納屋の月明かり Moonlight in the Barn — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第7章の終わり。眠れないエイラが外へ出ると、納屋の戸のすきまから月の光が差しこみ、中で若者たちが小さく踊っている。
#   遠い国から来た旅の楽士のアコーディオンが、2拍目に重みのある、少し異国風の踊りを弾いている。エイラも笛でくるくると加わる。
#   やがて月が雲に隠れ、踊りは静かにほどけていく。
# 調べ: あいだ。形: マズルカ（3/4。2拍目に強勢）。AABB → CCAA（山）→ BBAA → AABB → 雲（A がだんだん薄く）。
# 拍子・速さ: 3/4・♩=100。旋法: A エオリア（トリオの C は C の長調の色）。
# 主役は笛（くるくる回る笛）。伴奏の主役: アコーディオン（2拍目に強い和音、3拍目に軽い和音）。脇: ピチカートの低音（1拍目）。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 2拍目のアクセント（マズルカ）で、少し異国風に回る。旋律も付点で2拍目に重みをかける。
# 始まり: アコーディオンの2拍目 → 終わり: 月が雲に隠れるように静かに。
# 山: 中盤（CCAA）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "070-moonlight-in-the-barn", "納屋の月明かり", "Moonlight in the Barn", 100, 3, "A", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.1})
K = Key("A", "minor", 4)
CA = ["Am", "F", "Am", "E", "Am", "Am", "G", "Am"]; CB = ["F", "G", "C", "F", "Dm", "C", "G", "Am"]; CC = ["C", "F", "C", "Am", "Am", "C", "G", "C"]
SC = [("2拍目", 2, "intro", ["Am", "Am"]), ("踊り1", 32, "verse", CA * 2 + CB * 2), ("踊り2", 32, "chorus", CC * 2 + CA * 2), ("踊り3", 32, "verse", CB * 2 + CA * 2),
      ("踊り4", 32, "verse", CA * 2 + CB * 2), ("雲", 20, "outro", CA * 2 + ["Am"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("2拍目", 0, 0.76), ("踊り1", 0, 0.76), ("踊り2", 0, 0.84), ("踊り2", 31, 0.9), ("踊り3", 0, 0.8), ("踊り4", 0, 0.76), ("雲", 0, 0.7), ("雲", 19, 0.56)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="2拍目", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# アコーディオン（060: 短い2音で笛の約5dB 下）。2拍目だけの始まりは少し大きく
AC = [S.track(f"アコーディオン{j + 1}", "accordion", volume=0.05, pan=0.2 + 0.07 * j, reverb=0.35,
              barGain=[round(x * (1.4 if b < 2 else 1.0), 3) for b, x in enumerate(G)]) for j in range(3)]
PZ = S.track("ピチカートの低音", "strings", patch="pizzicato", volume=0.12, gainDb=5, pan=-0.2, reverb=0.35, barGain=G)

# ---------- 節（1=A4。付点で2拍目に重み） ----------
A = ["5:0.75 4:0.25 3:1 5:1", "1':1.5 7:0.5 6:1", "5:0.75 6:0.25 5:1 4:1", "3:2 2:1", "1:0.75 2:0.25 3:1 4:1", "5:1.5 6:0.5 5:1", "4:0.5 3:0.5 2:1 7,:1", "1:2 R:1"]
Bm = ["1':0.5 7:0.5 6:0.5 7:0.5 1':1", "2':0.5 1':0.5 7:0.5 1':0.5 2':1", "3':1 2':0.5 1':0.5 7:1", "6:2 5:1",
      "4:0.5 5:0.5 6:0.5 5:0.5 4:1", "3:0.5 4:0.5 5:0.5 4:0.5 3:1", "2:0.75 3:0.25 4:1 7,:1", "1:2 R:1"]
Cm = ["3:0.75 4:0.25 5:1 3:1", "6:1.5 5:0.5 4:1", "5:0.75 4:0.25 3:1 2:1", "3:2 5,:1", "3:0.75 4:0.25 5:1 1':1", "7:1.5 6:0.5 5:1", "4:0.5 3:0.5 2:1 4:1", "3:2 R:1"]
PLAN = [("踊り1", A + A + Bm + Bm, 0.3), ("踊り2", Cm + Cm + A + A, 0.45), ("踊り3", Bm + Bm + A + A, 0.35), ("踊り4", A + A + Bm + Bm, 0.3)]
for k, (sc, bars, dens) in enumerate(PLAN):
    play_melody(c, sc, bars, 4, "waltz", key=K, density=dens, seed=7000 + k)
play_melody(c, "雲", A + A[:5] + ["5:3", "R:3", "3:3", "R:3", "R:3", "R:3", "R:3"], 4, "waltz", key=K, density=0.1, seed=7010)    # だんだん薄く

# ---------- アコーディオン（2拍目に強く、3拍目に軽く）とピチカート（1拍目） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    voice = [near(r, 57), near(th, 57), near(fi, 57)]
    fading = (n == "雲" and i >= 16)
    for j, m in enumerate(voice):
        if fading:
            AC[j].bar(b, f"R:1 {nm(m)}:0.8, R:1.2" if i < 19 else "R:3")
        else:
            AC[j].bar(b, f"R:1 {nm(m)}:0.6! R:0.4 {nm(m)}:0.4, R:0.6")
    if n != "2拍目" and not fading:
        PZ.bar(b, f"{nm(near(r, 33 + 12))}:1{'' if i % 2 == 0 else ','} R:2")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の070（第3版）。第7章の終わり、月明かりの納屋で若者たちが小さく踊る。マズルカ（3/4・♩=100）、A エオリア。旅の楽士のアコーディオンが2拍目に強い和音を置き、ピチカートが1拍目の低音。笛は付点で2拍目に重みをかけながら、くるくる回る。AABB → CCAA（トリオの C が山）→ BBAA → AABB。最後は月が雲に隠れるように、節がだんだん薄くなって静かに終わる。",
       harm_scenes=None, tail_scene="雲", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -45, "hp": 200, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air070.json", "w"), ensure_ascii=False)
