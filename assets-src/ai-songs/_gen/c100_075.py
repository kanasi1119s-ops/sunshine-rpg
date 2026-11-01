# ケルト・フルート100曲「銀の笛と百の夜」075 迷いの雨 Rain of Doubt — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 祖父が鐘を止めたと知ったエイラは、雨の中を歩きながら迷う。祖父を信じるか、信じないか。鐘を鳴らすか、このままにするか。
#   心は2つのあいだを行ったり来たりして、どちらにも決められない。雨はやまず、答えの出ないまま、足だけが進む。
# 調べ: あいだ。形: 二重主音（D と C の和音を2小節ずつ行き来し、どちらにも決めない）。歌（A B A）を3回、あいだにギターだけの間。
# 拍子・速さ: 4/4・♩=90。旋法: D ミクソリディア（C♮）。
# 主役は笛（迷う笛。句の終わりが D になったり C になったりする）。伴奏の主役: ブズーキ風のギター（開いた5度とオクターブの和音を、3＋3＋2 で刻む）。
#   脇: コントラバス（3＋3＋2 の低音）。竪琴・ピアノ・パッド・打楽器・弦の弓・2本目の笛は使わない。
# この曲だけ: 和音が全音（D と C）で行き来し続け、どちらにも決めない。最後は C のまま終わる（D に戻らない）。
# 始まり: ギターの D と C → 終わり: C のまま終わる。
# 山: 2つ（2回目と3回目の歌の終わり）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "075-rain-of-doubt", "迷いの雨", "Rain of Doubt", 90, 4, "D", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("D", "mixolydian", 4)
DC = ["D", "D", "C", "C"]
SC = [("ギター", 4, "intro", DC), ("歌1", 24, "verse", DC * 6), ("歌2", 24, "chorus", DC * 6), ("間", 8, "verse", DC * 2), ("歌3", 24, "chorus", DC * 6),
      ("C のまま", 6, "outro", ["D", "D", "C", "C", "C", "C"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ギター", 0, 0.78), ("歌1", 0, 0.74), ("歌2", 0, 0.78), ("歌2", 23, 0.9), ("間", 0, 0.72), ("歌3", 0, 0.8), ("歌3", 23, 0.94), ("C のまま", 0, 0.78), ("C のまま", 5, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ギター", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# ギター1本 0.008（044。5本重なる）。始まり（ギターだけ）は少し強く
GT = [S.track(f"ブズーキ風ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=0.25 - 0.1 * i, reverb=0.3,
              barGain=[round(x * (1.4 if S.scene_of(b)[0] in ("ギター", "間") else 1.0), 3) for b, x in enumerate(G)]) for i in range(5)]
CB_ = S.track("コントラバス", "strings", patch="contrabass", volume=0.03, gainDb=3, pan=-0.15, reverb=0.35, release=0.3, barGain=G)

# ---------- 歌（1=D4。句の終わりが D になったり C になったり） ----------
A = ["5:1 6:1 5:1 3:1", "2:2 1:2", "7,:1 2:1 4:1 3:1", "7,:4", "1:1 3:1 5:1 1':1", "7:2 6:2", "5:1 4:1 2:1 4:1", "3:2 2:2"]
Bm = ["1':1 2':1 1':1 6:1", "5:2 3:2", "4:1 5:1 7:1 5:1", "4:4", "3:1 5:1 1':1 5:1", "6:2 5:2", "4:1 2:1 7,:1 2:1", "7,:4"]
for k, sc in enumerate(("歌1", "歌2", "歌3")):
    play_melody(c, sc, A + Bm + A, 4, "reel", key=K, density=(0.3, 0.4, 0.45)[k], seed=7500 + k)
s0 = c.s0["C のまま"]
play_melody(c, "C のまま", ["5:2 6:2", "5:4", "4:2 3:2", "7:4", "7:4", "R:4"], 4, "air", key=K, density=0.0)    # 最後は C5 で止まる

# ---------- ブズーキ風のギター（3＋3＋2 の刻み）とコントラバス ----------
P332 = [(0, 0.75, "d", "!"), (0.75, 0.25, "u", ","), (1.5, 0.5, "d", "!"), (2, 0.5, "u", ","), (2.5, 0.5, "d", ""), (3, 0.5, "d", "!"), (3.5, 0.5, "u", ",")]
P_SOFT = [(0, 1.5, "d", ","), (1.5, 1.5, "d", ","), (3, 1, "d", ",")]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    if n == "C のまま" and i >= 4:
        if i == 4: strum(GT, b, B, "C", [(0, 7.5, "d", "")])
        continue
    strum(GT, b, B, ch, P_SOFT if n == "間" else P332)
    root = 38 if ch == "D" else 36
    if n != "間":
        CB_.bar(b, f"{nm(root)}:1.2! R:0.3 {nm(root)}:1, R:0.5 {nm(root + 7)}:0.8, R:0.2")
s0 = c.s0["C のまま"]
CB_.at((s0 + 4) * B, "C2:7")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の075（第3版）。祖父が鐘を止めたと知り、雨の中で迷う。4/4・♩=90、D ミクソリディア。ブズーキ風のギター（開いた5度とオクターブの和音を 3＋3＋2 で刻む）とコントラバスの上で、和音は D と C を2小節ずつ行き来し続け、どちらにも決めない。笛の句の終わりも D になったり C になったりする。歌を3回、あいだにギターだけの間。山は2回目と3回目の終わり。最後は D に戻らず、C のまま終わる。",
       harm_scenes=None, tail_scene="C のまま", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 2800, "rt": 2.8}}}
json.dump(air, open("/tmp/cel/w/air075.json", "w"), ensure_ascii=False)
