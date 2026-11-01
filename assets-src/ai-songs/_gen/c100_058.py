# ケルト・フルート100曲「銀の笛と百の夜」058 霧が晴れる前 Before the Mist Lifts — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 二つの笛が重なったあと、湖の霧はまだ厚い。けれど、ゆっくりと、少しずつ薄くなっていく。
#   にごった空気が澄んでいき、最後は、遠くの岸まで見通せる澄んだ響きになる。
# 調べ: あいだ。形: にごった響きが澄んでいく（弦の和音に、となりあう音のにごりを3つ → 2つ → 1つ → 0 と、場面ごとに1つずつ外す）。
# 拍子・速さ: 4/4・♩=50。旋法: F リディア（B♮ が明るく浮く）。
# 主役は笛（長い音で、場面ごとにゆるく上がる）。伴奏の主役: 弦の和音（にごりの音つき）とナイロン弦ギターの分散和音。
#   竪琴・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: にごりの音が場面ごとに1つずつ外れていき、最後は5度とオクターブだけの澄んだ響きになる。
# 始まり: ギターとにごった弦 → 終わり: 澄んだ5度とオクターブ。
# 山: 中盤に1つ（薄霧）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "058-before-the-mist-lifts", "霧が晴れる前", "Before the Mist Lifts", 50, 4, "F", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.15})
K = Key("F", "lydian", 4)
CH8 = ["F", "G", "Am", "F", "Dm", "G", "Em", "F"]
SC = [("にごり", 4, "intro", ["F", "G", "F", "F"]), ("霧1", 12, "verse", CH8 + CH8[:4]), ("霧2", 12, "verse", CH8[4:] + CH8), ("薄霧", 12, "chorus", CH8 + CH8[:4]),
      ("澄む", 12, "verse", CH8[4:] + CH8), ("晴れ", 4, "outro", ["F"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("にごり", 0, 0.68), ("霧1", 0, 0.68), ("霧2", 0, 0.72), ("薄霧", 0, 0.8), ("薄霧", 8, 0.86), ("澄む", 0, 0.76), ("晴れ", 0, 0.72), ("晴れ", 3, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="にごり", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 弦は声が多い（3〜6声）ので、1声ずつは 004 の値より小さめ。始まり（ギターとにごった弦だけ）は ×1.6
IG = [round(x * (1.6 if b < 4 else 1.0), 3) for b, x in enumerate(G)]
VC = S.track("チェロ（根音）", "strings", patch="cello", volume=0.018, gainDb=2, pan=-0.2, reverb=0.7, release=0.7, barGain=IG)
VA = S.track("ビオラ（5度）", "strings", patch="viola", volume=0.014, pan=0.05, reverb=0.7, release=0.7, barGain=IG)
VN = S.track("バイオリン（3度）", "strings", patch="violin", volume=0.02, gainDb=3, pan=0.25, reverb=0.7, release=0.7, barGain=IG)
CL = [S.track(f"にごりの音{j + 1}", "strings", patch=("viola" if j % 2 else "violin"), volume=(0.013 if j % 2 else 0.018), gainDb=(0 if j % 2 else 3),
              pan=-0.1 + 0.2 * j, reverb=0.7, release=0.7, barGain=IG) for j in range(3)]
OCT = S.track("バイオリン（オクターブ）", "strings", patch="violin", volume=0.02, gainDb=3, pan=0.35, reverb=0.7, release=0.7, barGain=G)
GT = [S.track(f"ギター（分散和音{j + 1}）", "guitar", patch="nylonGuitar", volume=0.011, pan=-0.3 + 0.1 * j, reverb=0.4, barGain=IG) for j in range(2)]

def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
SCALE = [(5 + x) % 12 for x in (0, 2, 4, 6, 7, 9, 11)]          # F リディア
def step_up(m):
    x = m + 1
    while x % 12 not in SCALE: x += 1
    return x

# ---------- 弦の和音（2小節ごとに弓を返す。にごりの音は、和音の音の1つ上の隣の音） ----------
MUD = {"にごり": 3, "霧1": 3, "霧2": 2, "薄霧": 1, "澄む": 0}
for b in range(0, c.s0["晴れ"], 2):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r, th, fi = tri(ch)
    L = f"{2 * B + 0.25}"
    v_r, v_f, v_t = near(r, 41), near(fi, 53), near(th, 60)
    mk = "," if b % 4 else ""
    if n == "澄む":                                            # 澄む：5度とオクターブだけ
        VC.at(b * B, f"{nm(v_r)}:{L}{mk}"); VA.at(round(b * B + 0.05, 3), f"{nm(v_r + 7)}:{L},")
        VN.at(round(b * B + 0.1, 3), f"{nm(v_r + 12 if v_r + 12 >= 53 else v_r + 24)}:{L},"); OCT.at(round(b * B + 0.15, 3), f"{nm(v_r + 19 if v_r + 19 >= 60 else v_r + 31)}:{L},")
        continue
    VC.at(b * B, f"{nm(v_r)}:{L}{mk}"); VA.at(round(b * B + 0.05, 3), f"{nm(v_f)}:{L},"); VN.at(round(b * B + 0.1, 3), f"{nm(v_t)}:{L},")
    for j, base in enumerate((v_f, v_t, v_r + 12)[:MUD[n]]):
        CL[j].at(round(b * B + 0.15 + 0.05 * j, 3), f"{nm(step_up(base))}:{L},")

# ---------- ギター（8分の分散和音。にごりの所は和音の上の隣の音もつまむ） ----------
for b in range(c.s0["晴れ"]):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 40)
    if n == "澄む":
        seq = [lo, lo + 7, lo + 12, lo + 19, lo + 24, lo + 19, lo + 12, lo + 7]
    else:
        t2 = near(th, lo + 12); f2 = near(fi, lo + 12)
        seq = [lo, f2, t2, step_up(t2) if MUD[n] >= 2 else lo + 12, near(r, t2 + 1), t2, f2, step_up(f2) if MUD[n] >= 1 else t2]
    for q, m in enumerate(seq):
        GT[q % 2].at(round(b * B + q * 0.5, 3), f"{nm(m)}:{1.0 if q % 2 == 0 else 0.5}{'' if q == 0 else ','}")

# ---------- 笛（長い音で、場面ごとにゆるく上がる。1=F4。C6 より上には行かない） ----------
MEL = {
    "霧1": ["3:4", "2:2 3:2", "4:4", "3:4", "5:4", "4:2 3:2", "2:4", "3:4", "3:2 5:2", "4:4", "3:2 2:2", "3:4"],
    "霧2": ["5:4", "6:2 5:2", "7:4", "5:4", "6:4", "5:2 4:2", "5:2 6:2", "7:4", "1':4", "7:2 6:2", "5:4", "6:4"],
    "薄霧": ["1':4", "7:2 1':2", "2':4", "1':4", "3':2 2':2", "1':4", "7:2 6:2", "7:4", "1':2 2':2", "3':4", "2':2 1':2", "2':4"],
    "澄む": ["3':4", "4':2 3':2", "5':4", "3':4", "2':2 3':2", "4':4", "5':4", "4':2 3':2", "2':4", "3':2 4':2", "5':4", "5':4"],
}
for k, (sc, bars) in enumerate(MEL.items()):
    play_melody(c, sc, bars, 4, "air", key=K, density=(0.1, 0.15, 0.2, 0.12)[k], seed=5800 + k)
s0 = c.s0["晴れ"]
c.FLUTE.at(s0 * B, "C6:13")
VC.at(s0 * B, "F2:15.5"); VA.at(round(s0 * B + 0.05, 3), "C3:15.4,"); VN.at(round(s0 * B + 0.1, 3), "F4:15.3,"); OCT.at(round(s0 * B + 0.15, 3), "C5:15.2,")
GT[0].at(s0 * B, "F2:6,"); GT[1].at(round(s0 * B + 0.5, 3), "C3:5.5,"); GT[0].at(round(s0 * B + 1.0, 3), "F3:5,"); GT[1].at(round(s0 * B + 1.5, 3), "C4:4.5,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の058（第3版）。湖の厚い霧が、ゆっくり薄くなっていく。4/4・♩=50、F リディア。弦の和音に、和音の音のとなりの音（にごり）を3つ重ね、場面ごとに1つずつ外していく。ギターの分散和音も同じように、にごりの音が外れていく。笛は長い音で、場面ごとにゆるく上がり、中盤の薄霧が山。最後は5度とオクターブだけの澄んだ響きの上で、笛が高い C を長く吹く。",
       harm_scenes=None, tail_scene="晴れ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air058.json", "w"), ensure_ascii=False)
