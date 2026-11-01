# ケルト・フルート100曲「銀の笛と百の夜」071 岬への道 The Road to the Cape — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第8章のはじまり。祭りのあと、エイラは祖父の日記の最後のページに書かれた岬を目ざす。重い足取りで、海沿いの坂を登っていく。
#   坂が急になるほど、足取りは遅く重くなる。登りきると、足音だけが残る。
# 調べ: あいだ。形: 行進（重い足取りの 6/8 マーチ。16小節の節 AB を4回。4回目は急な坂でテンポが落ちる）。
# 拍子・速さ: 6/8・付点4分＝88 → 70（急な坂）。旋法: D エオリア。
# 主役は笛（進む笛）。伴奏の主役: ティンパニ（足取り。1拍目が重い）とコントラバス（1拍目に重く）。脇: ホルン（2回目から、長い支え）。
#   竪琴・ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 一歩ごとに1拍目が重く、坂が急になるとテンポが落ちる（♩.=88 → 70）。
# 始まり: 太鼓の足取り → 終わり: 足取りだけ。
# 山: 終盤（急な坂の終わり）。そのあと、登りきって海が見える24小節（ゆっくりのまま）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "071-the-road-to-the-cape", "岬への道", "The Road to the Cape", 88, 2, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
K = Key("D", "minor", 4)
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Dm", "Dm", "C", "Am", "Dm", "Bb", "C", "Dm"]; CB = ["Dm", "C", "Bb", "F", "Bb", "F", "C", "Dm"]
T = CA * 2 + CB * 2
SC = [("足取り", 4, "intro", ["Dm"] * 4), ("道1", 32, "verse", T), ("道2", 32, "verse", T), ("道3", 32, "verse", T), ("急な坂", 32, "chorus", T),
      ("海が見える", 24, "verse", CB * 2 + CA), ("足取りだけ", 8, "outro", ["Dm"] * 8)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("足取り", 0, 0.76), ("道1", 0, 0.72), ("道2", 0, 0.76), ("道3", 0, 0.8), ("急な坂", 0, 0.84), ("急な坂", 31, 0.94), ("海が見える", 0, 0.78), ("足取りだけ", 0, 0.76), ("足取りだけ", 7, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="足取り", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 88}, {"bar": s["急な坂"] + 1, "bpm": 70, "ramp": 16}]
B = S.beats
G = c.g()
TP = S.track("ティンパニ（足取り）", "strings", patch="timpani", volume=0.12, pan=0, reverb=0.4, barGain=[round(x * (1.3 if S.scene_of(b)[0].startswith("足取り") else 1.0), 3) for b, x in enumerate(G)])
CB_ = S.track("コントラバス（1拍目）", "strings", patch="contrabass", volume=0.03, gainDb=3, pan=-0.15, reverb=0.45, release=0.3, barGain=G)
HN = S.track("ホルン（長い支え）", "brass", patch="horn", volume=0.11, gainDb=6, pan=0.25, reverb=0.6, barGain=G)

# ---------- 行進の節（8分＝1、1小節＝6。1=D4） ----------
A = ["1:3 1:2 2:1", "3:3 5:3", "4:2 3:1 2:2 1:1", "2:6", "1:3 1:2 2:1", "3:3 6:3", "5:2 4:1 3:2 2:1", "1:6"]
Bm = ["5:3 5:2 6:1", "7:3 1':3", "6:2 5:1 4:2 3:1", "5:6", "1':3 7:2 6:1", "5:3 4:2 3:1", "2:2 3:1 4:2 2:1", "1:6"]
for k, sc in enumerate(("道1", "道2", "道3", "急な坂")):
    play_melody(c, sc, e2b(A + A + Bm + Bm), 4, "march", key=K, density=(0.2, 0.3, 0.35, 0.45)[k], seed=7100 + k)
play_melody(c, "海が見える", e2b(Bm + Bm + A), 4, "air", key=K, density=0.25, seed=7110)            # 登りきって、海が見える

# ---------- 足取り（ティンパニ：1拍目が重く、2拍目は軽く）とコントラバス、ホルン ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    last = (n == "足取りだけ" and i >= 6)
    TP.bar(b, "D3:1! A2:1," if not last else ("D3:1, R:1" if i == 6 else "A2:1, R:1"))      # 試し書き出し: D2・A1 はティンパニの音域の外で鳴らなかった
    if n.startswith("足取り"): continue
    CB_.bar(b, f"{nm(near(r, 38))}:0.6! R:0.4 {nm(near(r, 38))}:0.3, R:0.7")
    if n != "道1" and i % 2 == 0:
        HN.at(b * B, f"{nm(near(th, 53))}:{2 * B - 0.1}{',' if i % 4 else ''}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の071（第3版）。第8章のはじまり、祖父の日記の最後に書かれた岬へ、海沿いの坂を登る。重い足取りの 6/8 マーチ（付点4分＝88）、D エオリア。ティンパニの足取り（1拍目が重く、2拍目は軽い）とコントラバスに乗って、笛が16小節の節を4回進む。2回目からホルンの長い支え。4回目は坂が急になり、テンポが 70 まで落ちて重くなる（山）。最後は足取りだけが残る。",
       harm_scenes=None, tail_scene="足取りだけ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 2800, "rt": 2.8}}}
json.dump(air, open("/tmp/cel/w/air071.json", "w"), ensure_ascii=False)
