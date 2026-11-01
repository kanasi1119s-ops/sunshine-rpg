# ケルト・フルート100曲「銀の笛と百の夜」031 森の入口 The Edge of the Old Wood — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第4章のはじまり。山の上の泉をめざすエイラは、古い森の入口に立つ。ここは「薄い場所」（この世とあの世の境が薄い所）。
#   風がやみ、鳥も鳴かない。一歩ふみこむごとに、足もとの低い響きが一段ずつ沈み、木々の上では高い響きがずっと鳴っている。
# 調べ: あいだ。形: 薄い場所の静けさ（ほとんど動かない旋律）。8小節の段を7つ。
# 拍子・速さ: 4/4・♩=54。旋法: C リディア（F♯ が浮いた感じ）。
# 主役は笛（長い音。2〜3音のあいだをゆっくり行き来するだけ）。
# 伴奏の主役: ビオラの高い持続（G5。木々の上の響き）と、チェロの低い持続（段ごとに全音ずつ下がる。6小節鳴らして2小節あける）。
#   始まりだけ、弦合奏の風のようなふくらみ。竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 森に入る一歩（段）ごとに、低い弦が半音でなく全音ずつ下がる（C → B♭ → A♭ → F♯ → E → D → C の全音音階）。
# 始まり: 風のような弦 → 終わり: 弦だけが残る（笛は最後の段の途中で止まる）。
# 山: なし。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "031-the-edge-of-the-old-wood", "森の入口", "The Edge of the Old Wood", 54, 4, "C", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.25})
K = Key("C", "lydian", 4)
STEP = [60, 58, 56, 54, 52, 50, 48]                         # C4 B♭3 A♭3 F♯3 E3 D3 C3（全音ずつ下がる）
CHN = {60: "C", 58: "Bb", 56: "Ab", 54: "F#", 52: "E", 50: "D", 48: "C"}
SC = [("風", 4, "intro", ["C"] * 4)] + [(f"{k + 1}歩目", 8, "verse", [CHN[STEP[k]]] * 8) for k in range(7)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("風", 0, 0.66)] + [(f"{k + 1}歩目", 0, 0.7) for k in range(7)] + [("7歩目", 7, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="風", passing=False, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: ビオラ（0.022）は笛と同じくらい。チェロ（0.022・gainDb 3）は笛より約8dB 大きい → 0.011・gainDb 0。弦合奏も大きい → 0.025
# 長い弦（004 で笛と並べて測った値）：チェロ 0.02・gainDb 2、ビオラ 0.017 で笛の約5dB 下。ここではビオラが主役なので少し大きく
VA = [S.track(f"ビオラ（高い持続{j + 1}）", "strings", patch="viola", volume=0.022, pan=0.25, reverb=0.75, release=0.4, barGain=[round(x * 1.4, 3) for x in G]) for j in range(2)]
VC = [S.track(f"チェロ（低い持続{j + 1}）", "strings", patch="cello", volume=0.011, gainDb=0, pan=-0.2, reverb=0.7, release=0.6, barGain=[round(x * 1.4, 3) for x in G]) for j in range(2)]
WIND = [S.track(f"弦合奏（風{j + 1}）", "strings", patch="stringEnsemble", volume=0.04, pan=-0.3 + 0.6 * j, reverb=0.8, release=1.0,
                barGain=[0.9, 1.4, 1.9, 1.6] + [0.0] * (c.NB - 4)) for j in range(2)]   # 1回目（7.77）は風が -35〜-41dB と本編より約12dB 小さかった

# 風：弦合奏が C と G をふくらませる
for j, m in enumerate((60, 67)):
    WIND[j].at(0.0, f"{nm(m)}:16,")
# ビオラの高い G5：2小節ごとに2本で交互に弓を返す（最後まで切らない）
st, k = 0.0, 0
while st < c.NB * B - 0.01:
    en = min(c.NB * B, st + 8.3)
    VA[k % 2].at(round(st, 3), f"G5:{round(en - st, 3)}{',' if st else ''}")
    st += 8; k += 1
# チェロの低い持続：段ごとに全音下がる。6小節鳴らして2小節あける（森の静けさ）
for kk in range(7):
    b0 = c.s0[f"{kk + 1}歩目"]
    VC[kk % 2].at(b0 * B, f"{nm(STEP[kk])}:{6 * B}")

# ---------- 笛（C リディア。1=C5 にすると高いので 1=C4・オクターブ4。2〜3音のあいだをゆっくり） ----------
P = [["R:2 5:2", "5:4", "4:2 5:2", "5:4", "3:4", "3:2 4:2", "5:4", "R:4"],
     ["R:2 3:2", "3:4", "4:4", "3:4", "2:4", "2:2 3:2", "3:4", "R:4"],
     ["R:2 6:2", "6:4", "5:4", "4:4", "5:4", "5:2 4:2", "3:4", "R:4"],
     ["R:2 3:2", "4:4", "4:4", "3:4", "2:4", "3:4", "2:4", "R:4"],
     ["R:2 5:2", "4:4", "3:4", "4:4", "5:4", "6:4", "5:4", "R:4"],
     ["R:2 3:2", "2:4", "1:4", "2:4", "3:4", "2:4", "1:4", "R:4"],
     ["R:2 5:2", "6:4", "7:4", "1':4", "1':4", "R:4", "R:4", "R:4"]]          # 最後の段：上の C へ登って、笛は止まる。弦だけが残る
for kk in range(7):
    play_melody(c, f"{kk + 1}歩目", P[kk], 4 if kk != 6 else 4, "air", key=K, density=0.15, seed=3100 + kk)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の031（第3版）。第4章のはじまり、古い森の入口の「薄い場所」。4/4・♩=54、C リディア。風のような弦のふくらみのあと、ビオラの高い G がずっと鳴り続け、笛は2〜3音のあいだをゆっくり行き来するだけ。森に一歩ふみこむごとに、チェロの低い持続が全音ずつ（C → B♭ → A♭ → F♯ → E → D → C）沈んでいく。最後は笛が止まり、弦だけが残る。",
       harm_scenes=None, tail_scene="7歩目", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -46, "hp": 180, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.32, "lp": 2600, "rt": 4.2}}}
json.dump(air, open("/tmp/cel/w/air031.json", "w"), ensure_ascii=False)
