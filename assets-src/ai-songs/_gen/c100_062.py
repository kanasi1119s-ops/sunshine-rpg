# ケルト・フルート100曲「銀の笛と百の夜」062 炉辺の灯 By the Hearth — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 村の小さな家に招かれたエイラ。炉ばたで、家の主人がギターをつま弾き、エイラは祖父の旅の話を、笛で語って聞かせる。
#   話が終わると、主人が小さなワルツを弾きだし、エイラもそっと合わせる。夜がふけ、炉の火がぱちりとはぜる。
# 調べ: 眠り。形: 炉ばたの語り（自由なゆれのエア 32小節 → 小さなワルツ 64小節）。
# 拍子・速さ: 3/4・♩=56（ゆれを大きく）→ ♩=76 のワルツ。旋法: D イオニア。
# 主役は笛（語る笛）。伴奏の主役: ナイロン弦ギター（語りではまばらな和音、ワルツでは低音と2・3拍目の和音）。
#   竪琴・ピアノ・パッド・弦・2本目の笛は使わない。最後だけ、火がはぜる小さな音（枠太鼓の縁をごく弱く）。
# この曲だけ: 部屋の響きが小さく近い（ほかの曲より残響を短く、乾いた音）。
# 始まり: ギターの1音 → 終わり: 火がはぜるような小さな音。
# 山: 前半（語りの2回目）。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "062-by-the-hearth", "炉辺の灯", "By the Hearth", 76, 3, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.3})
K = Key("D", "major", 4)
L1C = ["D", "Bm", "A", "D", "G", "A", "Bm", "D", "D", "G", "D", "Bm", "Em", "A", "D", "D"]
L2C = ["D", "A", "G", "D", "D", "Bm", "A", "D", "G", "D", "A", "A", "D", "Bm", "A", "D"]
WAC = ["D", "G", "Em", "D", "A", "A", "A", "D"]; WBC = ["A", "D", "G", "D", "G", "D", "A", "D"]
WORDER = ["A", "A", "B", "B", "A", "A", "B", "A"]
SC = [("ギターの1音", 1, "intro", ["D"]), ("語り1", 16, "verse", L1C), ("語り2", 16, "chorus", L2C),
      ("ワルツ", 64, "verse", sum([WAC if x == "A" else WBC for x in WORDER], [])), ("火がはぜる", 3, "outro", ["D"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ギターの1音", 0, 0.7), ("語り1", 0, 0.7), ("語り2", 0, 0.78), ("語り2", 10, 0.86), ("ワルツ", 0, 0.72), ("ワルツ", 63, 0.7), ("火がはぜる", 0, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ギターの1音", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 56}, {"bar": s["ワルツ"] + 1, "bpm": 76, "ramp": 2}]
B = S.beats
G = c.g()
# ギター: 親指 0.014・指 0.007 で笛より少し小さい（051）。部屋が小さいので残響は少なく
GB = S.track("ギター（低音）", "guitar", patch="nylonGuitar", volume=0.016, pan=-0.15, reverb=0.12, barGain=G)
GC = [S.track(f"ギター（和音{j + 1}）", "guitar", patch="nylonGuitar", volume=0.008, pan=-0.25 + 0.08 * j, reverb=0.12, barGain=G) for j in range(3)]
GI = S.track("ギター（始まりの1音）", "guitar", patch="nylonGuitar", volume=0.04, pan=-0.15, reverb=0.15)
FIRE = S.track("炉の火（枠太鼓の縁）", "guitar", patch="frameDrum", volume=0.2, gainDb=8, pan=0.25, reverb=0.1)

def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12

# ---------- 笛 ----------
L1 = ["5:3", "6:1 5:1 3:1", "2:2 3:1", "5:3", "6:2 1':1", "7:1 6:1 5:1", "6:3", "5:3",
      "3:2 5:1", "6:3", "1':2 7:1", "6:1 5:1 3:1", "2:2 1:1", "2:3", "3:1 2:1 1:1", "1:3"]
L2 = ["1':3", "2':1 1':1 7:1", "6:2 7:1", "1':3", "3':2 2':1", "1':1 7:1 6:1", "7:3", "5:3",
      "6:2 7:1", "1':3", "2':2 1':1", "7:1 6:1 5:1", "3:2 2:1", "3:3", "2:1 1:1 7,:1", "1:3"]
WA = ["3:1 4:1 5:1", "6:2 5:1", "4:1 3:1 2:1", "3:3", "2:1 3:1 4:1", "5:2 4:1", "3:1 2:1 7,:1", "1:3"]
WB = ["5:1 6:1 7:1", "1':2 7:1", "6:1 5:1 4:1", "5:3", "6:1 5:1 4:1", "3:2 4:1", "2:1 3:1 2:1", "1:3"]
play_melody(c, "語り1", L1, 4, "air", key=K, density=0.25, seed=6201)
play_melody(c, "語り2", L2, 4, "air", key=K, density=0.35, seed=6202)
play_melody(c, "ワルツ", sum([WA if x == "A" else WB for x in WORDER], []), 4, "waltz", key=K, density=0.25, seed=6203)

# ---------- ギター ----------
GI.at(0, "D3:3")
for b in range(s["語り1"], s["火がはぜる"]):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 38); up = [near(fi, 50), near(th, 54), near(r, 57)]
    if n.startswith("語り"):                                   # 語り：小節の頭に低音、2小節に1回だけ和音をゆっくりつまむ
        GB.at(b * B, f"{nm(lo)}:3{'' if i % 4 == 0 else ','}")
        if i % 2 == 0:
            for j, m in enumerate(up): GC[j].at(round(b * B + 0.35 + 0.25 * j, 3), f"{nm(m)}:{round(2.6 - 0.25 * j, 2)},")
    else:                                                      # ワルツ：1拍目に低音、2・3拍目に和音
        GB.at(b * B, f"{nm(lo if i % 2 == 0 else near(fi, 38))}:1{'!' if i % 8 == 0 else ''}")
        for q in (1, 2):
            for j, m in enumerate(up): GC[j].at(round(b * B + q + 0.015 * j, 3), f"{nm(m)}:0.8,")
s0 = s["火がはぜる"]
GB.at(s0 * B, "D2:6,"); GC[0].at(round(s0 * B + 0.4, 3), "A3:5.5,"); GC[1].at(round(s0 * B + 0.8, 3), "D4:5,"); GC[2].at(round(s0 * B + 1.2, 3), "F#4:4.5,")
c.FLUTE.at(s0 * B, "D5:5")

# ---------- 火がはぜる（最後の3小節に、ぱちっ、ぱち…と小さく） ----------
rng = random.Random(6201)
for t in (s0 * B + 2.3, s0 * B + 4.1, s0 * B + 4.35, s0 * B + 6.6, s0 * B + 7.9, s0 * B + 8.05):
    FIRE.at(round(t, 3), f"E3:0.25{',' if rng.random() < 0.6 else ''}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.08 --master -15 --widen 1.05 --side-hpf 200",
       "ケルト・フルート100曲の062（第3版）。村の小さな家の炉ばた。家の主人のナイロン弦ギターのそばで、エイラが祖父の旅の話を笛で語る（3/4・♩=56、ゆれを大きく。2回目の語りが山）。話が終わると、主人が小さなワルツ（♩=76）を弾きだし、エイラもそっと合わせる。D の長調。部屋の響きは小さく近く、ほかの曲より乾いた音。ギターの1音で始まり、最後は炉の火がぱちりとはぜる小さな音。",
       harm_scenes=None, tail_scene="火がはぜる", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -48, "hp": 200, "lp": 3600, "wide": 0.008, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -34, "delay": 0.08, "lp": 3200, "rt": 0.7}}}
json.dump(air, open("/tmp/cel/w/air062.json", "w"), ensure_ascii=False)
