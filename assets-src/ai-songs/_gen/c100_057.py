# ケルト・フルート100曲「銀の笛と百の夜」057 二つの笛 Two Flutes — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 祖父の幻が消えたあと、エイラは祖父の笛の節を、自分の笛でくり返す。すると、もう一つの笛（祖父の思い出）が後を追ってくる。
#   はじめは2小節遅れ、次は1小節、次は1拍。回るたびに、ふたりの息は近づき、最後はぴったり同時に吹いて、一斉に止まる。
# 調べ: 喜び。形: ずれが縮んでいくカノン（2小節 → 1小節 → 1拍 → 同時）。
# 拍子・速さ: 3/4・♩=58。旋法: G ドリアの5音（G・A・C・D・E。どこで重なってもにごらない）。
# 主役は笛（2本。エイラの笛が主、思い出の笛は右から少し小さく）。伴奏の主役: ピチカート（低い根音と、上の5度）。同時の所で竪琴。
#   ギター・ピアノ・パッド・打楽器・弓の弦は使わない。
# この曲だけ: 2本の笛のずれが、回るたびに縮む（2小節 → 1小節 → 1拍 → 同時）。同時になった所で、2本目は5音の1つ下の音で重なる。
# 始まり: ピチカートだけ → 終わり: 全員で一斉に止める。
# 山: 合わさる所（同時）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "057-two-flutes", "二つの笛", "Two Flutes", 58, 3, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
K = Key("G", "dorian", 4)
CH16 = ["G", "G", "C", "G", "C", "G", "D", "G", "C", "D", "Am", "G", "C", "G", "D", "G"]
SC = [("ピチカート", 4, "intro", ["G", "C", "D", "G"]), ("2小節遅れ", 18, "verse", CH16 + ["G", "G"]), ("1小節遅れ", 17, "verse", CH16 + ["G"]),
      ("1拍遅れ", 17, "verse", CH16 + ["G"]), ("同時", 32, "chorus", CH16 * 2), ("一斉に止める", 1, "outro", ["G"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ピチカート", 0, 0.7), ("2小節遅れ", 0, 0.7), ("1小節遅れ", 0, 0.74), ("1拍遅れ", 0, 0.78), ("同時", 0, 0.84), ("同時", 31, 0.94), ("一斉に止める", 0, 0.94)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ピチカート", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 2本目の笛（0.1）は笛と同じくらい（047）→ 少し小さく 0.075。ピチカート（0.12・gainDb 5）は笛の約6dB 下（052 で測った値）
F2 = S.track("思い出の笛", "panflute", patch="flute", volume=0.075, bright=-0.3, pan=0.4, reverb=0.6, breath=False, barGain=G)
PZ = [S.track(f"ピチカート（{x}）", "strings", patch="pizzicato", volume=v, gainDb=5, pan=p, reverb=0.4, barGain=G) for x, v, p in (("低い根音", 0.12, -0.2), ("上の5度", 0.09, 0.15))]
PZI = [S.track(f"ピチカート（始まりの{x}）", "strings", patch="pizzicato", volume=v, gainDb=12, pan=p, reverb=0.4) for x, v, p in (("根音", 0.12, -0.2), ("5度", 0.09, 0.15))]
HP = S.track("竪琴（同時の所）", "harp", patch="folkHarp", volume=0.06, pan=0.3, reverb=0.55, sustain=1.4, barGain=G)

# ---------- 節（16小節。1=G4。使う音は 1・2・4・5・6 だけ＝G・A・C・D・E） ----------
M = ["1:1 2:1 4:1", "5:2 4:1", "6:1 5:1 4:1", "5:3", "6:1 1':1 6:1", "5:2 4:1", "2:1 4:1 2:1", "1:3",
     "5:1 6:1 1':1", "2':2 1':1", "6:1 1':1 6:1", "5:3", "4:1 5:1 6:1", "5:2 4:1", "2:1 1:1 2:1", "1:3"]
PENT = [0, 2, 5, 7, 9]                                       # G を 0 とした5音
def pent_down(m):
    """5音の中で1つ下の音"""
    x = m - 1
    while (x - 67) % 12 not in PENT: x -= 1
    return x
def events(bars, b0, shift_beats=0.0):
    ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (b0 + j) * B + shift_beats)
    return [[round(t, 4), L, m] for t, L, m in ev]
STAGE = [("2小節遅れ", 2 * B, 0.15), ("1小節遅れ", 1 * B, 0.2), ("1拍遅れ", 1.0, 0.25)]
for k, (sc, lag, dens) in enumerate(STAGE):
    s0 = c.s0[sc]
    ev = events(M, s0)
    play(c.FLUTE, ornament(ev, K, 58, "air", B, density=dens, seed=5700 + k))
    play(F2, [(t, L, m, ",") for t, L, m in events(M, s0, lag)])
s0 = c.s0["同時"]
for h in range(2):
    ev = events(M, s0 + 16 * h)
    play(c.FLUTE, ornament(ev, K, 58, "air", B, density=0.3, seed=5710 + h))
    play(F2, [(t, L, (m if h == 0 else pent_down(m)), "") for t, L, m in ev])          # 前半は同じ音、後半は5音の1つ下で
s0 = c.s0["一斉に止める"]
c.FLUTE.at(s0 * B, "G5:1!"); F2.at(s0 * B, "D5:1!")

# ---------- ピチカート（低い根音は1拍目、上の5度は2・3拍目。同時では8分で弾む） ----------
ROOT = {"G": 43, "C": 48, "D": 50, "Am": 45}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); r = ROOT[S.chords[b]]
    lo, hi = (PZI if n == "ピチカート" else PZ)
    if n == "一斉に止める":
        lo.bar(b, "G2:1! R:2"); hi.bar(b, "D3:1! R:2"); HP.bar(b, "G3:1! R:2"); continue
    lo.bar(b, f"{nm(r)}:1{'!' if i % 4 == 0 else ''} R:2")
    if n == "同時":
        hi.bar(b, f"R:1 {nm(r + 7)}:0.5 {nm(r + 12)}:0.5, {nm(r + 7)}:0.5 {nm(r + 14)}:0.5,")
        HP.bar(b, " ".join(f"{nm(x)}:0.5{',' if q % 2 else ''}" for q, x in enumerate((r + 19, r + 24, r + 26, r + 24, r + 19, r + 14))))
    else:
        hi.bar(b, f"R:1 {nm(r + 7)}:1, {nm(r + 12)}:1,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.28 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の057（第3版）。祖父の幻が消えたあと、エイラの笛を、もう一つの笛（祖父の思い出）が追いかける。3/4・♩=58、G ドリアの5音（G・A・C・D・E）。16小節の同じ節を、2本の笛が2小節遅れ → 1小節遅れ → 1拍遅れ → 同時と、回るたびにずれを縮めて吹く。同時になった所が山で、後半は2本目が5音の1つ下で重なる。伴奏はピチカート（低い根音と上の5度）と、同時の所の竪琴。最後は全員で一斉に止める。",
       harm_scenes=None, tail_scene="一斉に止める", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 3000, "rt": 2.8}}}
json.dump(air, open("/tmp/cel/w/air057.json", "w"), ensure_ascii=False)
