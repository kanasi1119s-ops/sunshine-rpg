# ケルト・フルート100曲「銀の笛と百の夜」093 村人たちの待つ朝 The Morning the Village Waited — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 海を渡って、ついに故郷の島へ帰る朝。港では、エイラの帰りを待つ村人たちが、夜明けの呼び声の曲で迎える。
#   村の笛吹きの娘が、エイラの笛と3度で重なって吹き、小太鼓と大太鼓が行列をはずませる。
# 調べ: 喜び。形: 夜明けの呼び声（ガリシアのアルボラーダ風）＋2本の笛の3度。呼び声 → AABB を6回 → 太鼓の間をはさむ → 全員で止める。
# 拍子・速さ: 2/4・♩=104。旋法: D イオニア。
# 主役は笛（2本。エイラの笛が上、村の娘の笛が3度下・6度下で平行に）。伴奏の主役: 小太鼓（枠太鼓の小さい太鼓の細かい刻み）と大太鼓（録音のタム）。
#   竪琴・ギター・ピアノ・パッド・弦・アコーディオンは使わない。
# この曲だけ: 2本の笛が3度・6度で平行に歌う（A は3度下、B は6度下。イベリアのケルトの色）。
# 始まり: 呼び声の笛 → 終わり: 全員で止める。
# 山: 終盤。
import sys, json, re
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia

S = Song("C100", "093-the-morning-the-village-waited", "村人たちの待つ朝", "The Morning the Village Waited", 104, 2, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("D", "major", 4)
CA = ["D", "D", "G", "D", "D", "D", "A", "D"]; CB = ["G", "D", "G", "D", "G", "A", "G", "D"]
T = CA * 2 + CB * 2
SC = [("呼び声", 8, "intro", ["D", "G", "A", "D", "D", "G", "A", "D"])] + [(f"行列{k + 1}", 32, ("chorus" if k >= 4 else "verse"), T) for k in range(3)] + \
     [("太鼓の間", 8, "verse", ["D"] * 8)] + [(f"行列{k + 4}", 32, ("chorus" if k >= 1 else "verse"), T) for k in range(3)] + [("止める", 1, "outro", ["D"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("呼び声", 0, 0.74), ("行列1", 0, 0.76), ("行列2", 0, 0.8), ("行列3", 0, 0.82), ("太鼓の間", 0, 0.8), ("行列4", 0, 0.84), ("行列5", 0, 0.88), ("行列6", 0, 0.92),
          ("行列6", 31, 0.98), ("止める", 0, 0.98)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="呼び声", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 80}, {"bar": s["行列1"] + 1, "bpm": 104, "ramp": 1}]
B = S.beats
G = c.g()
F2 = S.track("村の娘の笛", "panflute", patch="flute", volume=0.075, bright=-0.4, pan=0.35, reverb=0.45, breath=False, barGain=G)
SN = [S.track(f"小太鼓{j + 1}", "guitar", patch="frameDrum", volume=0.3, gainDb=18, pan=0.15 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]
BD = S.track("大太鼓", "strings", patch="inchTom", volume=0.12, gainDb=12, pan=-0.1, reverb=0.35, barGain=G)

# ---------- 呼び声と行列の節（8分＝0.5。1=D4。F♯4 より下には行かない：3度下・6度下も D4 より上に） ----------
CALL = ["5:2", "1':2", "7:1 6:1", "5:2", "3':2", "2':1 1':1", "7:1 5:1", "5:2"]
A = ["5:0.5 6:0.25 5:0.25 3:0.5 5:0.5", "1':0.5 7:0.25 6:0.25 5:1", "6:0.5 5:0.5 4:0.5 3:0.5", "4:0.5 5:0.5 3:1",
     "5:0.5 6:0.25 5:0.25 3:0.5 5:0.5", "1':0.5 2':0.5 3':1", "2':0.5 1':0.5 7:0.5 6:0.5", "5:1 R:1"]
Bm = ["1':1 7:0.5 6:0.5", "5:0.5 6:0.5 5:1", "4:0.5 5:0.5 6:0.5 4:0.5", "3:1 5:1", "1':1 7:0.5 6:0.5", "5:0.5 6:0.5 7:1", "6:0.5 5:0.5 4:0.5 3:0.5", "3:2"]
def put(b0, bars, dens, seed, second=None):
    ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (b0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 104, "reel", B, density=dens, seed=seed))
    if second is not None:
        play(F2, [(t, L, (_dia(K, m, second) if _dia(K, m, second) >= 62 else _dia(K, m, -2)), "") for t, L, m in ev])      # D4 より下になるときは3度下に
put(s["呼び声"], CALL, 0.3, 9300)
for k in range(6):
    b0 = s[f"行列{k + 1}"]
    put(b0, A + A, (0.3, 0.35, 0.4, 0.4, 0.45, 0.5)[k], 9310 + k, second=(-2 if k >= 1 else None))           # A：3度下（1回目は笛ひとり）
    put(b0 + 16, Bm + Bm, (0.3, 0.35, 0.4, 0.4, 0.45, 0.5)[k], 9320 + k, second=(-5 if k >= 1 else None))    # B：6度下
c.FLUTE.at(s["止める"] * B, "A5:0.6!"); F2.at(s["止める"] * B, "F#5:0.6!")

# ---------- 小太鼓（細かい刻み）と大太鼓 ----------
for b in range(s["行列1"], s["止める"]):
    n, i, Lb, k = S.scene_of(b); sn = SN[b % 2]
    fill = (i % 8 == 7)
    if n == "太鼓の間":
        sn.bar(b, "E3:0.25! E3:0.25, E3:0.25, E3:0.25, E3:0.5! E3:0.25, E3:0.25,"); BD.bar(b, "F2:0.5! R:0.5 F2:0.5 F2:0.5,"); continue
    sn.bar(b, "E3:0.5! E3:0.25, E3:0.25, E3:0.5 E3:0.25, E3:0.25," if not fill else "E3:0.25! E3:0.25, E3:0.25, E3:0.25, E3:0.25! E3:0.25! E3:0.5!")
    BD.bar(b, "F2:0.5! R:1.5" if i % 2 == 0 else "F2:0.5 R:0.5 F2:0.5, R:0.5")
s0 = s["止める"]; SN[0].at(s0 * B, "E3:0.5!"); BD.at(s0 * B, "F2:0.6!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.2 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の093（第3版）。故郷の島に帰る朝、港で待つ村人たちの夜明けの呼び声（ガリシアのアルボラーダ風）。2/4・♩=104、D の長調。笛ひとりの呼び声で始まり、小太鼓の細かい刻みと大太鼓に乗って行列の節を6回。2回目からは村の娘の笛が加わり、A は3度下、B は6度下で平行に歌う（イベリアのケルトの色）。途中に太鼓だけの間。山は終盤で、最後は全員で止める。",
       harm_scenes=None, tail_scene="止める", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.15, "lp": 3000, "rt": 1.8}}}
json.dump(air, open("/tmp/cel/w/air093.json", "w"), ensure_ascii=False)
