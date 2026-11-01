# ケルト・フルート100曲「銀の笛と百の夜」086 雪洞の炎 The Fire in the Snow Cave — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 吹雪の夜、エイラは雪洞を掘って、小さな火をおこす。火は風にゆれて、大きくなったり小さくなったりする。
#   その炎を見つめながら、エイラは低い笛で、同じ小さな歌を何度もくり返す。やがて眠りにつき、炎の音だけが残る。
# 調べ: 眠り。形: 小さな炎の歌（8小節の同じ歌を12回。ときどき笛は休み、炎だけがゆれる）。
# 拍子・速さ: 6/8・付点4分＝52（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。旋法: D イオニア。
# 主役は笛（温かい低音域。D4〜B4）。伴奏の主役: リードオルガン（炎のゆらぎ。強弱が不規則にゆっくり変わる）とナイロン弦ギター（揺れる同じ音型）。
#   竪琴・ピアノ・パッド・弦・打楽器・2本目の笛は使わない。
# この曲だけ: オルガンの和音が炎のようにゆっくり強弱する（069 の規則正しい寝息とちがい、炎のゆらぎは不規則）。
# 始まり: ギターの1音 → 終わり: オルガンの和音。
# 山: なし。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "086-the-fire-in-the-snow-cave", "雪洞の炎", "The Fire in the Snow Cave", 52, 2, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.15})
K = Key("D", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CH8 = ["D", "A", "D", "G", "D", "Em", "A", "D"]
SC = [("ギターの1音", 2, "intro", ["D", "D"]), ("炎の歌", 96, "verse", CH8 * 12), ("オルガンの和音", 6, "outro", ["D", "G", "D", "D", "D", "D"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("ギターの1音", 0, 0.7), ("炎の歌", 0, 0.68), ("炎の歌", 48, 0.72), ("炎の歌", 95, 0.64), ("オルガンの和音", 0, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ギターの1音", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 炎のゆらぎ：不規則な強弱（ゆっくりなめらかに）
rng = random.Random(8601)
raw = [rng.uniform(0.5, 1.0) for _ in range(c.NB + 3)]
FLAME = [round((raw[b] + raw[b + 1] + raw[b + 2]) / 3, 3) for b in range(c.NB)]
# リードオルガン: 和音でも笛より約14dB 小さい → gainDb 6、オルガンだけの所は gainDb 12（015・069）
OR = [S.track(f"リードオルガン（炎{j + 1}）", "pad", patch="reedOrgan", volume=0.1, gainDb=6, pan=-0.15 + 0.15 * j, reverb=0.5,
              barGain=[round(G[b] * FLAME[b], 3) for b in range(c.NB)]) for j in range(3)]
ORE = [S.track(f"リードオルガン（終わりの和音{j + 1}）", "pad", patch="reedOrgan", volume=0.1, gainDb=12, pan=-0.15 + 0.15 * j, reverb=0.55,
               barGain=[round(0.7 * FLAME[b], 3) for b in range(c.NB)]) for j in range(3)]
GB = S.track("ギター（親指）", "guitar", patch="nylonGuitar", volume=0.016, pan=-0.25, reverb=0.3, barGain=[round(x * (1.6 if b < 2 else 1.0), 3) for b, x in enumerate(G)])
GF = [S.track(f"ギター（指{j + 1}）", "guitar", patch="nylonGuitar", volume=0.008, pan=-0.35 + 0.1 * j, reverb=0.3, barGain=G) for j in range(2)]

# ---------- 炎の歌（8小節。1=D4。低く温かく。5回目と10回目は笛が休み、炎だけがゆれる） ----------
M = ["3:3 2:2 1:1", "2:3 1:3", "3:2 4:1 5:3", "4:3 3:3", "3:3 2:2 3:1", "4:3 2:3", "3:2 2:1 7,:2 2:1", "1:6"]
REST = {4, 9}
bars = []
for k in range(12):
    bars += ["R:6"] * 8 if k in REST else M
play_melody(c, "炎の歌", e2b(bars), 4, "air", key=K, density=0.12, seed=8601)

# ---------- 伴奏 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
GB.at(0, "D3:6")
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    if n == "ギターの1音": continue
    v = [near(r, 50), near(th, 54), near(fi, 57)]
    trs = ORE if n == "オルガンの和音" else OR
    if n == "オルガンの和音" and i > 0 and i < 3: pass
    for j, m in enumerate(v):
        trs[j].at(round(b * B + 0.04 * j, 3), f"{nm(m)}:{B + 0.3}{'' if FLAME[b] > 0.75 else ','}")
    if n == "炎の歌":                                                      # 揺れる同じ音型（根音・5度・10度・5度・10度・5度）
        lo = near(r, 38)
        seq = [lo, near(fi, lo + 1), near(th, lo + 12), near(fi, lo + 1), near(th, lo + 12), near(fi, lo + 1)]
        GB.at(b * B, f"{nm(seq[0])}:2{'' if i % 8 == 0 else ','}")
        for q in range(1, 6):
            GF[q % 2].at(round(b * B + q * T3, 4), f"{nm(seq[q])}:{round(2 * T3, 4)},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の086（第3版）。吹雪の夜、雪洞の小さな火。6/8・付点4分＝52、D の長調。ギターの1音で始まり、ナイロン弦ギターの揺れる同じ音型と、リードオルガンの和音（炎のように、強弱が不規則にゆっくり変わる）の上で、笛が低く温かい音域で8小節の小さな歌を12回くり返す。ときどき笛は休み、炎だけがゆれる。山はなく、最後はオルガンの和音だけが残る。",
       harm_scenes=None, tail_scene="オルガンの和音", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 2600, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air086.json", "w"), ensure_ascii=False)
