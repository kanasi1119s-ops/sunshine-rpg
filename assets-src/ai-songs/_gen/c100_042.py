# ケルト・フルート100曲「銀の笛と百の夜」042 風の刻んだ文字 Letters Cut by Wind（2026-10-29）
# イメージ: 石の輪の中の一つに、古い文字が刻まれている。長い年月の風で、ところどころ欠けて読めない。
#   エイラは指でなぞりながら、欠けた所を想像でつないでいく。何度もなぞるうちに、文がひと続きに読めるようになる。
# 形: 欠けた旋律が、回るたびに埋まっていく（1回目は半分の音が休み、2回目は4分の1、3回目で完成、最後は和声つき）。3/4・♩=52。G ドリア。山なし。
# ただひとつ: 同じ16小節の旋律の「欠け（休符）」が、回るたびに埋まる。欠けた所はギターの指弾きが和音で受けとめる（音は落とさない）。
# 編曲の表:
#   なぞる  : ナイロンギターの指弾きの分散和音＋チェロ＋うすい弦（はじまりから厚く）
#   欠け1   : 笛（音の半分が休み）。休みの所は竪琴の高い音が「かすれた文字」のように1音
#   欠け2   : 笛（4分の1が休み）。弦が3声に
#   読める  : 笛が完成した旋律
#   読めた  : 完成した旋律＋笛の和声＋内声の動き。いちばん豊か
#   息      : 最後の句を、ギターと笛だけでやさしく
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 52
S = Song("C100", "042-letters-cut-by-wind", "風の刻んだ文字", "Letters Cut by Wind", BPM, 3, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
C16 = ["Gm", "Dm", "Gm", "Am", "C", "F", "Bb", "C", "Dm", "Gm", "C", "Dm", "Bb", "C", "F", "Gm"]
S.scene("なぞる", 4, "intro", ["Gm", "Dm", "Gm", "Gm"])
for nm_ in ("欠け1", "欠け2", "読める", "読めた"): S.scene(nm_, 16, "verse" if nm_ != "読めた" else "chorus", C16)
S.scene("息", 4, "outro", ["Bb", "F", "Gm", "Gm"])
NAMES = ["なぞる", "欠け1", "欠け2", "読める", "読めた", "息"]

c = make(S, NAMES,
         [("なぞる", 0, 0.64), ("欠け1", 0, 0.64), ("欠け2", 0, 0.67), ("読める", 0, 0.7), ("読めた", 0, 0.75), ("読めた", 15, 0.72), ("息", 0, 0.66), ("息", 3, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="なぞる", passing=True, tension=False)
G1 = S.track("ナイロンギター（指弾き・低）", "guitar", patch="nylonGuitar", volume=0.1, pan=0.25, reverb=0.4, barGain=c.g())
G2 = S.track("ナイロンギター（指弾き・高）", "guitar", patch="nylonGuitar", volume=0.08, pan=0.38, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.12, reverb=0.45, barGain=c.g())

M = ["1:1 2:1 3:1", "5:2 4:1", "3:1 2:1 1:1", "2:3", "4:1 5:1 6:1", "7:2 6:1", "5:1 4:1 3:1", "4:3",
     "5:1 6:1 7:1", "1':2 7:1", "6:1 5:1 4:1", "5:3", "3:1 4:1 5:1", "4:2 3:1", "2:1 7,:1 2:1", "1:3"]
def worn(bars, every, off=0):
    """欠けた碑文：every 個に1つの音を、休みに変える（every=2 で半分が欠ける）"""
    out = []; k = off
    for s in bars:
        toks = []
        for t in s.split():
            d, L = t.split(":")
            toks.append(f"R:{L}" if k % every == 0 else t); k += 1
        out.append(" ".join(toks))
    return out
play_melody(c, "欠け1", worn(M, 2, 1), 4, "air", density=0.2, seed=4201)
play_melody(c, "欠け2", worn(M, 4, 3), 4, "air", density=0.4, seed=4202)
play_melody(c, "読める", M, 4, "air", density=0.6, seed=4203)
play_melody(c, "読めた", M, 4, "air", density=0.8, seed=4204)
play_melody(c, "息", ["3:1 4:1 5:1", "4:2 3:1", "2:1 7,:1 2:1", "1:3"], 4, "air", density=0.3, seed=4205)

B = S.beats
# 欠けた所（笛が休む拍）に、竪琴の高い音を1つ（かすれた文字）
rest_at = set()
for sc in ("欠け1", "欠け2"):
    b0 = c.s0[sc]; src = worn(M, 2, 1) if sc == "欠け1" else worn(M, 4, 3)
    for j, s in enumerate(src):
        t = 0.0
        for tok in s.split():
            d, L = tok.split(":"); L = float(L)
            if d == "R": rest_at.add(round((b0 + j) * B + t, 3))
            t += L
for st in sorted(rest_at):
    b = int(st // B); hi = tones(S.chords[b], "G5", "G6")
    c.HARP2.at(st, f"{nm(hi[int(st * 2) % len(hi)])}:1")

for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "G2", "G5")
    # ギターの指弾き：低い声部（根音→5度）と高い声部（3音の分散）を分けて
    G1.bar(b, f"{nm(r)}:1 {nm(r + 7)}:2" if not (n == "息" and i == 3) else f"{nm(r)}:3")
    G2.bar(b, " ".join(f"{nm(t[x % len(t)] + 12 if t[x % len(t)] < 55 else t[x % len(t)])}:0.5" for x in ((2, 3, 4, 3, 2, 3) if i % 2 == 0 else (3, 4, 5, 4, 3, 4))))
    CELLO.bar(b, f"{nm(r)}:3")
    nv = 2 if n in ("なぞる", "欠け1") else 3
    v = voice(ch, 55, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:3")
rich(c, choir_scenes=["読めた"], pulse_scenes=["欠け2", "読める", "読めた"], guitar=False, pizz=False, inner=True, choir_vol=0.11)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.33 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の042。風で欠けた碑文を、指でなぞって読む。3/4・♩=52、G ドリア。同じ旋律が、1回目は半分の音が欠け（休み）、2回目は4分の1、3回目で完成し、最後は和声つきでひと続きに読める。欠けた所は竪琴の高い音がかすれた文字のように鳴る。",
       harm_scenes=None, tail_scene="息", fill=False, pads=True, pad_scenes=["欠け1", "欠け2", "読める", "読めた", "息"], floor=True)
air = {"pre": 0.8, "tail": 6.0, "layers": [{"file": "0595", "db": -35, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -28, "rt": 7.0}, "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air042.json", "w"), ensure_ascii=False)
