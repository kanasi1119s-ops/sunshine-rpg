# ケルト・フルート100曲「銀の笛と百の夜」085 星の降る夜 A Night of Falling Stars — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 稜線をこえた夜、雪の峰の上に、星が一つ、また一つと現れる。エイラが笛で祖父の節を吹くたびに、星が増えていき、
#   最後は空いっぱいの星になる。
# 調べ: 喜び。形: 星の変奏（笛ひとりの主題 → 16小節の主題を9回。変奏ごとに星（グロッケンの音）が1つずつ増える）。
# 拍子・速さ: 笛ひとりは 6/8・付点4分＝60（ゆれを大きく）→ 6/8・付点4分＝80。旋法: A ミクソリディア（G♮）。
# 主役は笛（主題の笛）。伴奏の主役: グロッケン（星）と竪琴（地の分散和音）。脇: 弦（4回目から、だんだん厚く）。
#   ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 変奏ごとに星（グロッケン）が1つずつ増える。それぞれの星は決まった高さと決まった位置でまたたく（1回目は1つ、9回目は9つ）。
# 始まり: 笛ひとり → 終わり: 満天。
# 山: 変奏ごとに密に（最後がいちばん密）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "085-a-night-of-falling-stars", "星の降る夜", "A Night of Falling Stars", 80, 2, "A", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
K = Key("A", "mixolydian", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CT = ["A", "D", "Bm", "A", "A", "D", "A", "A", "A", "Bm", "A", "D", "A", "Bm", "G", "A"]
SC = [("笛ひとり", 8, "intro", CT[:8])] + [(f"星{k + 1}", 16, ("chorus" if k >= 7 else "verse"), CT) for k in range(9)] + [("満天", 4, "outro", ["A"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("笛ひとり", 0, 0.72)] + [(f"星{k + 1}", 0, round(0.7 + 0.025 * k, 3)) for k in range(9)] + [("星9", 15, 0.96), ("満天", 0, 0.9), ("満天", 3, 0.8)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="笛ひとり", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 60}, {"bar": s["星1"] + 1, "bpm": 80, "ramp": 2}]
B = S.beats
G = c.g()
GL = [S.track(f"星（グロッケン{j + 1}）", "bell", patch="glockenspiel", volume=0.03, pan=-0.6 + 0.15 * j, reverb=0.85, barGain=[0.8] * c.NB) for j in range(9)]
HP = [S.track(f"竪琴（地{j + 1}）", "harp", patch="folkHarp", volume=0.06, pan=-0.2 + 0.2 * j, reverb=0.55, sustain=1.4, barGain=G) for j in range(2)]
VC = S.track("チェロ", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.25, reverb=0.7, release=0.7, barGain=G)
VA = S.track("ビオラ", "strings", patch="viola", volume=0.017, pan=0.1, reverb=0.7, release=0.7, barGain=G)
VN = S.track("バイオリン", "strings", patch="violin", volume=0.022, gainDb=3, pan=0.3, reverb=0.75, release=0.7, barGain=G)

# ---------- 主題（16小節。1=A4） ----------
T = ["1:2 3:1 5:3", "6:2 5:1 4:2 3:1", "2:2 3:1 4:3", "5:6", "1':2 7:1 6:2 5:1", "4:2 5:1 6:3", "5:2 4:1 3:2 2:1", "3:6",
     "1:2 3:1 5:3", "6:2 1':1 2':3", "1':2 7:1 6:2 5:1", "4:3 6:3", "5:2 4:1 3:2 1:1", "2:2 3:1 4:3", "3:2 2:1 7,:2 2:1", "1:6"]
play_melody(c, "笛ひとり", e2b(T[:8]), 4, "air", key=K, density=0.15, seed=8500)
for k in range(9):
    play_melody(c, f"星{k + 1}", e2b(T), 4, "jig" if k >= 3 else "air", key=K, density=0.15 + 0.04 * k, seed=8501 + k)
c.FLUTE.at(s["満天"] * B, "A5:7")

# ---------- 星（星 j は、2小節ごとに決まった位置・決まった高さでまたたく） ----------
STAR = [(93, 0.0), (88, 1 + T3), (85, 2 * T3), (90, 2 + 2 * T3), (81, 1.0), (95, 3 + T3), (86, 3.0), (91, 2.0), (83, 3 + 2 * T3)]   # (高さ, 2小節の中の位置)
for k in range(9):
    b0 = s[f"星{k + 1}"]
    for g in range(8):
        for j in range(k + 1):
            m, pos = STAR[j]
            GL[j].at(round((b0 + 2 * g) * B + pos, 4), f"{nm(m)}:1.5{',' if (g + j) % 2 else ''}")
for j in range(9):                                                   # 満天：すべての星が一斉に
    m, pos = STAR[j]
    GL[j].at(round(s["満天"] * B + pos * 0.5, 4), f"{nm(m)}:4")

# ---------- 竪琴の地と弦 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(s["星1"], c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lvl = int(n[1:]) if n.startswith("星") else 10
    seq = (near(r, 45), near(fi, 52), near(th, 57), near(r, 57), near(th, 57), near(fi, 52))
    for q, m in enumerate(seq if n != "満天" else seq[:3]):
        HP[q % 2].at(round(b * B + q * T3, 4), f"{nm(m)}:{round(2 * T3, 4)}{'' if q == 0 else ','}")
    if i % 2 == 0 and lvl >= 4:
        VC.at(b * B, f"{nm(near(r, 40))}:{2 * B + 0.2}{',' if i % 4 else ''}")
        if lvl >= 6: VA.at(round(b * B + 0.05, 3), f"{nm(near(th, 55))}:{2 * B + 0.15},")
        if lvl >= 8: VN.at(round(b * B + 0.1, 3), f"{nm(near(fi, 64))}:{2 * B + 0.1},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の085（第3版）。雪の峰の夜空に、星が一つずつ現れる。6/8、A ミクソリディア。笛ひとりの主題（付点4分＝60）のあと、付点4分＝80 で16小節の主題を9回変奏する。変奏ごとに星（グロッケン）が1つずつ増え、それぞれの星は決まった高さと位置でまたたく。下では竪琴の分散和音、4回目からチェロ、6回目からビオラ、8回目からバイオリン。最後はすべての星が一斉に光る満天。",
       harm_scenes=None, tail_scene="満天", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 3000, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air085.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
