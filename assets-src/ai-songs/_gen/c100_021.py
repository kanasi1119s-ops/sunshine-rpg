# ケルト・フルート100曲「銀の笛と百の夜」021 小川のはじまり Where the Brook Begins — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第3章のはじまり。草原を抜けた山すその岩場で、苔から水が一滴ずつ落ちている。滴はだんだん間を詰め、
#   いつのまにか細い流れになり、流れは小川になって、ひらけた谷へ走りだす。エイラは流れについて歩きだす。
# 調べ: 喜び。形: 一滴から流れへ（拍のない滴 → リールの流れ）。
# 拍子・速さ: 4/4・♩=104（滴の場面は拍を感じさせない：音と音の間が 4拍 → 3.5 → … → 0.5拍 と詰まっていき、気づくとリールの8分になっている）。
# 旋法: D ミクソリディア。
# 主役は笛（滴では1音ずつ → 流れからはなめらかに）。伴奏の主役: 竪琴（folkHarp）。滴のあいだは高い1音ずつ、流れからは8分の分散和音。
#   開ける所でだけ、竪琴の低い根音。ギター・ピアノ・弦・パッド・打楽器は使わない。
# この曲だけ: 滴の間隔がだんだん詰まって、気づくとリールの8分になっている。
# 始まり: 竪琴の高い1音 → 終わり: 流れたまま遠ざかる（笛が先に遠ざかり、竪琴の8分が細くなっていく）。
# 山: 平原（落ち着いた流れ）→ 急に開ける（谷が見える）。最初が大きく、だんだん小さくなる形にはしない。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "021-where-the-brook-begins", "小川のはじまり", "Where the Brook Begins", 104, 4, "D", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("D", "mixolydian", 4)
CA = ["D", "C", "D", "Am", "D", "C", "G", "D"]
CB = ["G", "D", "C", "D", "G", "D", "Am", "D"]
SC = [("滴", 16, "intro", ["D"] * 16), ("流れ", 32, "verse", CA + CA + CB + CB), ("平原", 16, "verse", CA + CB),
      ("開ける", 32, "chorus", CA + CA + CB + CB), ("遠ざかる", 16, "outro", CA + CB)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("滴", 0, 0.64), ("滴", 15, 0.7), ("流れ", 0, 0.74), ("流れ", 31, 0.78), ("平原", 0, 0.72), ("平原", 15, 0.72),
          ("開ける", 0, 0.9), ("開ける", 31, 0.88), ("遠ざかる", 0, 0.8), ("遠ざかる", 15, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="滴", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 滴の1音（高い音・強さ 1.4）は笛より約 8dB 大きい → 0.12→0.06。流れの8分（上）は笛と同じくらい → 0.075→0.055
DROP = [S.track(f"竪琴（滴{j + 1}）", "harp", patch="folkHarp", volume=0.06, pan=[-0.4, 0.35, -0.1][j], reverb=0.75, sustain=2.4,
                barGain=[round(x * (1.8 if b < 16 else 1.0), 3) for b, x in enumerate(G)]) for j in range(3)]
ARP = S.track("竪琴（流れの8分）", "harp", patch="folkHarp", volume=0.055, pan=0.2, reverb=0.45, sustain=1.2, barGain=G)
ARP2 = S.track("竪琴（流れの8分・低い方）", "harp", patch="folkHarp", volume=0.07, pan=-0.2, reverb=0.45, sustain=1.2, barGain=G)
LOW = S.track("竪琴（開ける谷の根音）", "harp", patch="folkHarp", volume=0.1, pan=0.0, reverb=0.55, sustain=2.4, barGain=G)

# ---------- 滴（拍のない1音ずつ。間隔が 4拍 → 0.5拍 へ詰まる） ----------
# 滴の音（D ミクソリディアの高い所）。竪琴と笛が交互に落とす。後半は笛が多くなり、最後の2小節は8分でリールの頭につながる
DROP_NOTES = [81, 76, 79, 74, 78, 72, 76, 69, 74, 71, 72, 67, 69, 74, 72, 71, 69, 67, 66, 67, 69, 71, 72, 74, 76, 74, 72, 71, 69, 67, 69, 71]
t = 0.0; gap = 4.0; k = 0; end_drop = 16 * B
while t < end_drop - 0.01:
    m = DROP_NOTES[k % len(DROP_NOTES)]
    if k % 3 == 2 or gap <= 1.0:                     # 笛の滴（後半ほど多い）
        if m > 79: m -= 12
        c.FLUTE.at(round(t, 3), f"{nm(m)}:{round(min(gap, 2.0) * (0.6 if gap > 1 else 0.95), 3)}")
    else:
        DROP[k % 3].at(round(t, 3), f"{nm(m)}:{round(min(gap, 3.0), 3)}")
    t += gap; k += 1
    gap = max(0.5, gap * 0.86)                        # 間隔がだんだん詰まる（最後は8分＝0.5拍）
    if t + gap > end_drop: gap = max(0.5, end_drop - t)

# ---------- リール（D ミクソリディア。1=D4。A・B 8小節） ----------
A = ["1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "7,:0.5 2:0.5 4:0.5 2:0.5 7:0.5 4:0.5 2:0.5 4:0.5",
     "1:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:0.5 3:0.5", "5,:0.5 1:0.5 2:0.5 1:0.5 6,:0.5 1:0.5 5,:1",
     "1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 2':0.5 1':0.5 6:0.5", "7,:0.5 2:0.5 4:0.5 6:0.5 7:0.5 6:0.5 4:0.5 2:0.5",
     "4:0.5 6:0.5 1':0.5 6:0.5 5:0.5 3:0.5 2:0.5 7,:0.5", "1:1 5:0.5 3:0.5 1:1 R:1"]
Bp = ["4:0.5 5:0.5 6:0.5 1':0.5 2':0.5 1':0.5 6:0.5 4:0.5", "1':0.5 6:0.5 5:0.5 3:0.5 1:0.5 3:0.5 5:0.5 1':0.5",
      "7:0.5 1':0.5 2':0.5 7:0.5 6:0.5 5:0.5 4:0.5 2:0.5", "3:0.5 5:0.5 1':0.5 5:0.5 3:1 1:1",
      "4:0.5 5:0.5 6:0.5 1':0.5 2':0.5 3':0.5 2':0.5 1':0.5", "6:0.5 1':0.5 5:0.5 1':0.5 4:0.5 1':0.5 3:0.5 1':0.5",
      "5:0.5 4:0.5 6,:0.5 1:0.5 2:0.5 4:0.5 6:0.5 7:0.5", "1':1 5:0.5 3:0.5 1:1 R:1"]
play_melody(c, "流れ", A + A + Bp + Bp, 4, "reel", key=K, density=0.3, seed=2101)
PL = ["1:2 3:2", "7,:2 2:2", "1:1 3:1 5:2", "1:4", "4:2 6:2", "1':2 5:2", "6,:1 1:1 2:2", "1:4",
      "3:2 5:2", "4:2 2:2", "3:1 5:1 1':2", "5:4", "4:2 6:2", "5:2 3:2", "2:1 1:1 7,:2", "1:4"]
play_melody(c, "平原", PL, 4, "air", key=K, density=0.25, seed=2102)                 # 平原：流れが広く遅く見える（笛は長い音で）
play_melody(c, "開ける", A + A + Bp + Bp, 4, "reel", key=K, density=0.5, seed=2103)
play_melody(c, "遠ざかる", A + Bp[:6] + ["1:4", "R:4"], 4, "reel", key=K, density=0.35, seed=2104)

# ---------- 竪琴の流れ（8分の分散和音。上と下の2本でかみ合わせる） ----------
ROOT = {"D": 50, "C": 48, "G": 43, "Am": 45}
def tones(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return [r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12]
for b in range(16, c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    pcs = tones(ch)
    up = [62 + (p - 62) % 12 for p in pcs] + [74 + (pcs[0] - 74) % 12]
    up.sort()
    if n == "平原":                                                # 平原：4分でゆったり
        ARP.bar(b, " ".join(f"{nm(up[q])}:1{',' if q else ''}" for q in (0, 2, 1, 3)))
        ARP2.bar(b, f"{nm(r)}:2, {nm(r + 7)}:2,")
        continue
    thin = n == "遠ざかる" and i >= 8                            # 遠ざかる：後半は上の8分だけ、だんだん細く
    ARP.bar(b, " ".join(f"{nm(up[q])}:0.5{',' if q % 2 else ''}" for q in (0, 1, 2, 3, 2, 1, 2, 3)))
    if not thin:
        ARP2.bar(b, " ".join(f"{nm(x)}:0.5," for x in (r, r + 7, r + 12, r + 7, r, r + 7, r + 12, r + 7)))
    if n == "開ける":
        LOW.bar(b, f"{nm(r - 12 if r - 12 >= 38 else r)}:4")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の021（第3版）。第3章のはじまり、山すその岩場で苔から水が一滴ずつ落ちる。滴の間隔がだんだん詰まり、気づくとリール（4/4・♩=104）の8分の流れになっている。D ミクソリディア。伴奏は竪琴（滴の高い1音 → 8分の分散和音）。平原で一度ゆったりし、谷が見える所で急に開けて、最後は流れたまま遠ざかる。",
       harm_scenes=None, tail_scene="遠ざかる", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -28, "delay": 0.24, "lp": 3000, "rt": 2.8}}}
json.dump(air, open("/tmp/cel/w/air021.json", "w"), ensure_ascii=False)
