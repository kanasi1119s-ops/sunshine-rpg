# ケルト・フルート100曲「銀の笛と百の夜」056 祖父の幻 The Grandfather's Phantom — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 雨のあとの湖に、霧の向こうから角笛の音が聞こえる。祖父が若い日に吹いた節だ。エイラは1小節遅れて、同じ節を追いかける。
#   追いかけるうちに、祖父の音は少しずつ遠くなり、最後は消えてしまう。エイラはひとりで、残りの句を吹き終える。
# 調べ: 悲しみ。形: 1小節遅れのカノン（祖父のホルンが先に吹き、笛が1小節遅れて同じ節を1オクターブ上で追う）。
# 拍子・速さ: 4/4・♩=56。旋法: F♯ エオリア。
# 主役は笛（追う笛）。伴奏の主役: 遠いホルン（祖父の節。響きが多く、少し左の遠く）。脇: 低い弦のドローン（F♯ と C♯）。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 祖父のホルンが先に消え（最後の回は4小節で途切れる）、笛だけが残りの句を吹き終える。最後の音は5度（C♯5）。
# 始まり: 低いドローン → 終わり: 笛だけが最後の句を吹き、5度で止まる。
# 山: 2つの小さな山（2回目と3回目の終わり）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "056-the-grandfathers-phantom", "祖父の幻", "The Grandfather's Phantom", 56, 4, "F#", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("F#", "minor", 4); KH = Key("F#", "minor", 3)
SC = [("ドローン", 3, "intro", ["F#m"] * 3), ("幻1", 16, "verse", ["F#m"] * 16), ("幻2", 16, "verse", ["F#m"] * 16), ("幻3", 16, "chorus", ["F#m"] * 16),
      ("消える", 8, "verse", ["F#m"] * 8), ("五度", 2, "outro", ["F#m"] * 2)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ドローン", 0, 0.66), ("幻1", 0, 0.68), ("幻2", 0, 0.72), ("幻2", 14, 0.8), ("幻3", 0, 0.72), ("幻3", 14, 0.84), ("消える", 0, 0.72), ("五度", 0, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ドローン", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# ホルン（0.12〜0.15・gainDb 6）は笛と同じくらい（037・048）。祖父は遠く: 0.1 で響きを多く。回ごとに遠ざかる
FAR = {"幻1": 1.15, "幻2": 1.05, "幻3": 0.95, "消える": 0.8}
HN = S.track("祖父のホルン", "brass", patch="horn", volume=0.1, gainDb=6, pan=-0.35, reverb=0.9, barGain=[round(x * FAR.get(S.scene_of(b)[0], 1.0), 3) for b, x in enumerate(G)])
# ドローン: チェロ 0.02・gainDb 2、ビオラ 0.017 で笛の約5dB 下（004）。始まりだけは別のパートで大きく（047）
DR = [S.track(f"ドローン（{x}）", "strings", patch=p, volume=v, gainDb=gd, pan=pn, reverb=0.7, release=0.8, barGain=[round(x_ * 1.3, 3) for x_ in G])
      for x, p, v, gd, pn in (("チェロ F♯2", "cello", 0.02, 2, -0.15), ("ビオラ C♯4", "viola", 0.017, 0, 0.2), ("チェロ F♯2・弓返し", "cello", 0.02, 2, -0.15),
                              ("ビオラ C♯4・弓返し", "viola", 0.017, 0, 0.2))]
DRI = [S.track("ドローン（始まりのコントラバス）", "strings", patch="contrabass", volume=0.07, gainDb=8, pan=-0.1, reverb=0.7, release=1.2),
       S.track("ドローン（始まりのチェロ）", "strings", patch="cello", volume=0.03, gainDb=8, pan=0.1, reverb=0.7, release=1.2)]

# ---------- 祖父の節（16小節。1=F♯） ----------
M = ["1:2 3:2", "5:3 4:1", "3:2 2:1 1:1", "2:4", "3:2 5:2", "6:3 5:1", "4:2 3:2", "5:4",
     "6:2 1':2", "7:3 6:1", "5:2 6:1 5:1", "4:4", "3:2 4:1 3:1", "2:2 7,:2", "1:2 2:2", "1:4"]
def put(track, key, bars, b0, dens, seed, orn=True, oct_=4):
    ev = []
    for j, s_ in enumerate(bars): ev += mel_events(key, s_, oct_, (b0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    if orn: play(track, ornament(ev, key, 56, "air", B, density=dens, seed=seed))
    else: play(track, [(t, L, m, "") for t, L, m in ev])
for r, sc in enumerate(("幻1", "幻2", "幻3")):
    s0 = c.s0[sc]
    put(HN, KH, M, s0, 0, 0, orn=False, oct_=3)                                # 祖父：飾りなし
    put(c.FLUTE, K, M, s0 + 1, (0.12, 0.2, 0.28)[r], 5600 + r)        # 笛：1小節遅れ、1オクターブ上
s0 = c.s0["消える"]
put(HN, KH, M[:4], s0, 0, 0, orn=False, oct_=3)                                # 祖父は4小節で途切れる
put(c.FLUTE, K, M[:7], s0 + 1, 0.1, 5610)                              # 笛だけが残りを吹き終える
c.FLUTE.at(c.s0["五度"] * B + 0, "C#5:7")                               # 最後は5度で止まる

# ---------- ドローン（2小節ごとに弓を返す。消える所で薄れ、五度では笛だけ） ----------
DRI[0].at(0, "F#2:12.6"); DRI[1].at(0.05, "C#3:12.5,")
k = 0
for b in range(3, c.s0["消える"] + 4, 2):
    L = 2 * 4 + 0.3 if b + 2 <= c.s0["消える"] + 4 else 4
    DR[2 * (k % 2)].at(b * B, f"F#2:{L}{',' if k else ''}"); DR[1 + 2 * (k % 2)].at(round(b * B + 0.06, 3), f"C#4:{L - 0.06},")
    k += 1

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.38 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の056（第3版）。雨のあとの湖、霧の向こうから祖父の角笛の節が聞こえる。4/4・♩=56、F♯ エオリア。遠いホルン（祖父）が先に吹き、笛が1小節遅れて同じ節を1オクターブ上で追う（カノン）。下には F♯ と C♯ の低い弦のドローン。16小節の節を3回、2回目と3回目の終わりに小さな山。4回目、祖父のホルンは4小節で途切れ、ドローンも薄れて、笛だけが残りの句を吹き終え、5度（C♯）で止まる。",
       harm_scenes=None, tail_scene="五度", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2600, "rt": 4.4}}}
json.dump(air, open("/tmp/cel/w/air056.json", "w"), ensure_ascii=False)
