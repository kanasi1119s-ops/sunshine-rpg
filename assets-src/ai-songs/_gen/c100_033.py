# ケルト・フルート100曲「銀の笛と百の夜」033 梟の問い The Owl's Question — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 日が暮れて、森の古い樫の木の上から、大きな梟が問いかける。「ホウ、ホウ、ホー？」（おまえはだれだ）。
#   エイラは笛で答えるが、梟は毎回同じ問いをくり返す。エイラは答え方を変え、高さを変え、何度も答える。
#   問答がいちばん熱くなったあと、エイラの答えは静かになり、最後は梟の問いだけが森に残る（答えは自分で見つけなさい）。
# 調べ: あいだ。形: 問いと答え（梟の1小節の問い → エイラの3小節の答え）を何度も。
# 拍子・速さ: 4/4・♩=60。旋法: F♯ エオリア。
# 主役は笛（問う・答える笛）。伴奏の主役: ファゴット（梟の声）と低い弦（チェロとコントラバスの持続）。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 梟の問いはいつも同じ高さ（同じ3音）。エイラの答えは、毎回ちがう高さから始まる。
# 始まり: 梟（ファゴット）の問い → 終わり: 梟の声だけが残る。
# 山: 中盤に1つ（問答2。梟が答えを待たずに問いを重ね、エイラの答えが高く速くなる）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "033-the-owls-question", "梟の問い", "The Owl's Question", 60, 4, "F#", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
K = Key("F#", "minor", 4)
U = ["F#m", "D", "Bm", "C#m", "F#m", "A", "D", "C#m"]
SC = [("問答1", 24, "verse"), ("問答2", 16, "chorus"), ("問答3", 20, "verse"), ("梟だけ", 6, "outro")]
CH = []
for n, L, kd in SC:
    ch = [U[(len(CH) + q) // 4 % 8] for q in range(L)]
    S.scene(n, L, kd, ch); CH += ch
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("問答1", 0, 0.7), ("問答1", 23, 0.74), ("問答2", 0, 0.82), ("問答2", 12, 0.9), ("問答3", 0, 0.72), ("問答3", 19, 0.68), ("梟だけ", 0, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="問答1", passing=False, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 梟（ファゴット 0.15）は笛と同じくらい（問答の相手として丁度よい）。チェロは笛より約7dB、コントラバスは約10dB 小さい（低い持続として丁度よい）
OWL = S.track("ファゴット（梟の声）", "strings", patch="bassoon", volume=0.15, pan=-0.3, reverb=0.7, barGain=[round(x * 1.3, 3) for x in G])
VC = [S.track(f"チェロ（低い持続{j + 1}）", "strings", patch="cello", volume=0.014, gainDb=1, pan=0.2, reverb=0.65, release=0.5, barGain=[round(x * 1.4, 3) for x in G]) for j in range(2)]
CB = S.track("コントラバス（低い持続）", "strings", patch="contrabass", volume=0.05, pan=0.05, reverb=0.6, release=0.6, barGain=G)

QUESTION = "F#3:1 F#3:0.5 A3:2 R:0.5"                   # ホウ、ホウ、ホー？（いつも同じ高さ）
def ask(b, late=0.0):
    OWL.at(round(b * B + late, 3), QUESTION.replace("R:0.5", f"R:{round(0.5 - late, 3)}") if late else QUESTION)

# エイラの答え（3小節）。始まりの音を毎回変える（度数）
ANS = {1: ["1:1 3:1 2:1 1:1", "7,:2 1:1 3:1", "2:4"], 3: ["3:1.5 4:0.5 5:1 3:1", "2:1 1:1 7,:2", "1:4"],
       5: ["5:2 4:1 3:1", "4:1 6:1 5:2", "3:4"], 2: ["2:1 4:1 3:1 2:1", "1:1 3:1 5:2", "4:2 3:2"],
       4: ["4:1 3:1 4:1 6:1", "5:2 3:2", "2:4"], 7: ["7:2 6:1 5:1", "4:1 5:1 6:2", "5:4"],
       6: ["6:1.5 5:0.5 4:1 3:1", "4:1 2:1 7,:2", "1:4"], 8: ["1':2 7:1 6:1", "5:1 7:1 1':2", "2':2 1':2"]}
def answer(b, deg, dens, seed, up=0):
    ev = []
    for j, s_ in enumerate(ANS[deg]):
        ev += mel_events(K, s_, 4 + up, (b + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 60, "air", B, density=dens, seed=seed))

# 問答1：梟が問い、エイラが答える（答えの始まり：1・3・5・2・4・7）
s0 = c.s0["問答1"]
for q, d in enumerate((1, 3, 5, 2, 4, 7)):
    ask(s0 + 4 * q); answer(s0 + 4 * q + 1, d, 0.25, 3300 + q)
# 問答2（山）：梟は答えの途中で問いを重ねる（2小節ごと）。エイラの答えは高く、装飾が多く
s0 = c.s0["問答2"]
for q, d in enumerate((6, 8, 7, 8)):
    ask(s0 + 4 * q); ask(s0 + 4 * q + 2, late=0.5)
    answer(s0 + 4 * q + 1, d, 0.5, 3310 + q)
# 問答3：エイラの答えは低く静かに（最後は答えずに、問いを聞くだけ）
s0 = c.s0["問答3"]
for q, d in enumerate((5, 3, 2, 1, None)):
    ask(s0 + 4 * q)
    if d: answer(s0 + 4 * q + 1, d, 0.15, 3320 + q)
s0 = c.s0["梟だけ"]
ask(s0); ask(s0 + 2); ask(s0 + 4)

# 低い弦：4小節ごとに和音の根音（コントラバス）と3度（チェロ）。梟だけの所では止める
ROOT = {"F#m": 42, "D": 38, "Bm": 47, "C#m": 49, "A": 45}
for b in range(0, c.NB, 4):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r = ROOT[ch]
    if n == "梟だけ":
        CB.at(b * B, f"{nm(42 - 12 if 42 - 12 >= 28 else 42)}:{2 * B}"); break
    th = r + (3 if ch.endswith("m") else 4)
    CB.at(b * B, f"{nm(r - 12 if r - 12 >= 28 else r)}:{4 * B},")
    VC[(b // 4) % 2].at(round(b * B + 0.1, 3), f"{nm(th + 12 if th + 12 <= 62 else th)}:{4 * B - 0.1},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の033（第3版）。日暮れの森で、古い樫の木の上の梟が問いかける。問いと答え（4/4・♩=60）、F♯ エオリア。梟（ファゴット）の問いはいつも同じ3音の高さで、エイラの笛の答えは毎回ちがう高さから始まる。中盤で梟が答えを待たずに問いを重ねて問答が熱くなり、そのあとエイラの答えは静かになって、最後は梟の問いだけが森に残る。",
       harm_scenes=None, tail_scene="梟だけ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air033.json", "w"), ensure_ascii=False)
