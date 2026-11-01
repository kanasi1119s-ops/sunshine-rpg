# ケルト・フルート100曲「銀の笛と百の夜」032 木漏れ日 Dappled Light — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 森の奥へ進むと、高い木々のすきまから日が差しこみ、足もとに光と影のまだら模様がゆれている。
#   エイラは光の上を跳ねるように歩き、笛も光る。ときどき雲がかかって森が暗くなり（影）、また光が戻る。
# 調べ: 喜び。形: スリップ・ジグ（9/8。A・B 8小節ずつ）を4回（2回目と3回目のあいだに「影」）。
# 拍子・速さ: 9/8・付点4分＝100。1拍＝付点4分、1小節＝3拍で書き、8分は 1/3 拍（011 と同じ）。旋法: D ミクソリディア。
# 主役は笛（光る笛）。伴奏の主役: 竪琴の割り重ね（ウェールズの三重ハープのように、同じ音を左の手と右の手で2回ずつはじく）。
#   ギター・ピアノ・弦・パッド・打楽器・2本目の笛は使わない（011 のギターのスリップ・ジグとは、楽器も旋律の形もちがう）。
# この曲だけ: 竪琴の同じ音の連打（左・右）で、光がちらつく。影の場面では、ちらつきが止まって1回ずつになる。
# 始まり: 竪琴の揺らぎ（左右の同じ音）→ 終わり: 最後の音（主音）を伸ばす。
# 山: 2つ（2回目と4回目）。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 100
S = Song("C100", "032-dappled-light", "木漏れ日", "Dappled Light", BPM, 3, "D", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("D", "mixolydian", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["D", "C", "G", "D", "D", "C", "G", "D"]
CB = ["D", "Am", "C", "G", "D", "Am", "C", "D"]
AB = CA + CA + CB + CB
SC = [("ゆらぎ", 4, "intro", ["D", "C", "D", "D"]), ("1回目", 32, "verse", AB), ("2回目", 32, "chorus", AB), ("影", 16, "verse", CA + CB),
      ("3回目", 32, "verse", AB), ("4回目", 32, "chorus", AB), ("のばす", 2, "outro", ["D", "D"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ゆらぎ", 0, 0.68), ("1回目", 0, 0.72), ("2回目", 0, 0.84), ("2回目", 31, 0.88), ("影", 0, 0.66), ("3回目", 0, 0.74),
          ("4回目", 0, 0.86), ("4回目", 31, 0.92), ("のばす", 0, 0.8)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ゆらぎ", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 左右の竪琴（0.06）は笛と同じくらい → 0.04（笛が主役）。低い根音は笛より約8dB 小さい → 0.1
HL = [S.track(f"竪琴（左の手{j + 1}）", "harp", patch="folkHarp", volume=0.04, pan=-0.45, reverb=0.5, sustain=1.6, barGain=G) for j in range(2)]
HR = [S.track(f"竪琴（右の手{j + 1}）", "harp", patch="folkHarp", volume=0.04, pan=0.45, reverb=0.5, sustain=1.6, barGain=G) for j in range(2)]
HB = S.track("竪琴（低い根音）", "harp", patch="folkHarp", volume=0.1, pan=0.0, reverb=0.5, sustain=2.2, barGain=G)

# ---------- スリップ・ジグ（D ミクソリディア。1=D4。8分＝1、1小節＝9） ----------
A = ["5:2 3:1 1:2 3:1 5:2 6:1", "7:2 6:1 5:2 4:1 3:3", "2:2 4:1 6:2 4:1 2:2 7,:1", "1:2 3:1 5:3 R:3",
     "5:2 3:1 1:2 3:1 5:2 1':1", "7:2 1':1 2':2 1':1 7:2 5:1", "6:2 4:1 2:2 7,:1 2:3", "1:3 3:3 1:3"]
Bm = ["1':2 2':1 3':2 2':1 1':2 7:1", "6:2 7:1 1':2 6:1 4:3", "5:2 6:1 7:2 5:1 3:2 5:1", "4:2 3:1 2:2 7,:1 1:3",
      "1':2 2':1 3':2 4':1 3':2 2':1", "1':2 7:1 6:2 5:1 4:3", "3:2 5:1 1':2 5:1 3:2 2:1", "1:6 R:3"]
SHADOW = ["5:9", "3:6 2:3", "1:9", "7,:6 1:3", "2:9", "3:6 5:3", "4:6 3:3", "2:9",
          "1':9", "7:6 5:3", "6:9", "5:6 3:3", "4:9", "3:6 2:3", "2:6 7,:3", "1:9"]
DENS = {"1回目": 0.35, "2回目": 0.55, "3回目": 0.4, "4回目": 0.6}
for n in ("1回目", "2回目", "3回目", "4回目"):
    play_melody(c, n, e2b(A + A + Bm + Bm), 4, "march", key=K, density=DENS[n], seed=3200 + len(n) * 3 + int(n[0]))
play_melody(c, "影", e2b(SHADOW), 4, "air", key=K, density=0.2, seed=3210)
play_melody(c, "のばす", e2b(["1:9", "1:6 R:3"]), 4, "air", key=K, density=0.0)

# ---------- 竪琴の割り重ね（同じ音を左→右で2回ずつ。8分9つ） ----------
def tones(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return sorted(62 + (p - 62) % 12 for p in (r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12))
ROOT = {"D": 38, "C": 36, "G": 43, "Am": 45}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    tn = tones(ch); seq = [tn[0], tn[1], tn[2], tn[1] + 0, tn[2], tn[0] + 12]
    if n == "のばす":
        if i == 0:
            for j, x in enumerate(tn): (HL if j % 2 else HR)[0].at(round(b * B + 0.05 * j, 3), f"{nm(x)}:6,")
            HB.at(b * B, f"{nm(ROOT[ch])}:6")
        continue
    if n == "影":                                                     # 影：ちらつきが止まり、1音ずつ（左だけ）
        HL[b % 2].bar(b, " ".join(f"{nm(seq[q])}:1," for q in (0, 1, 2)))
        if i % 4 == 0: HB.at(b * B, f"{nm(ROOT[ch])}:{2 * B}")
        continue
    # 9つの8分：同じ音を左・右で2回ずつ（左右に光が跳ねる）
    pos = 0
    for q in range(9):
        note = seq[(q // 2) % len(seq)]
        tr = (HL if q % 2 == 0 else HR)[b % 2]
        mk = "" if q % 2 == 0 else ","
        tr.at(round(b * B + q * T3, 4), f"{nm(note)}:{round(T3, 4)}{mk}")
    if n != "ゆらぎ" and i % 2 == 0: HB.at(b * B, f"{nm(ROOT[ch])}:{2 * B},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の032（第3版）。森の木々のすきまから差す木漏れ日。スリップ・ジグ（9/8・付点4分＝100）、D ミクソリディア。竪琴が同じ音を左の手と右の手で2回ずつはじき（三重ハープの割り重ね）、光がちらつく。2回目のあとに雲がかかる「影」の場面ではちらつきが止まり、また光が戻る。山は2回目と4回目、最後は主音を伸ばす。",
       harm_scenes=None, tail_scene="のばす", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.22, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air032.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
