# ケルト・フルート100曲「銀の笛と百の夜」026 小さな滝の祈り Prayer at the Little Falls — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 小川の上流、岩のあいだから細い滝が落ちる所に、古い聖なる泉がある。村の人は泉のまわりを3周まわって祈る。
#   エイラも笛で同じ祈りの節を3回吹く。1周ごとに、泉に集まる気配（オルガン → 竪琴 → 低い響き）が増え、
#   3周目、節の中の1つの音だけが明るくなる（浄め）。最後は、滝つぼに小石が1つ落ちる音。
# 調べ: 悲しみ（祈り）。形: 聖なる泉の「巡り」（同じ32小節の旋律を3周。周ごとに楽器が増える）。
# 拍子・速さ: 前奏は自由（笛ひとりの祈り）→ 3/4・♩=72。旋法: A エオリア → 3周目だけ A ドリア（6度の F が F♯ になる＝浄め）。
# 主役は笛（祈る笛）。伴奏の主役: 小さなパイプオルガン（1周目から）→ ＋竪琴（2周目）→ ＋低いドローン（3周目。チェロの A と E）。
#   ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 3周目で旋法の1音（6度）だけが明るくなる。オルガンの和音も F が D に変わる。
# 始まり: 笛ひとり → 終わり: 小石が落ちるような竪琴の1音。
# 山: 3周目。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "026-prayer-at-the-little-falls", "小さな滝の祈り", "Prayer at the Little Falls", 72, 3, "A", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
KA, KD = Key("A", "minor", 4), Key("A", "dorian", 4)
CH8 = ["Am", "Am", "F", "G", "Am", "F", "G", "Am"]
CH8D = [x.replace("F", "D") for x in CH8]
SC = [("祈り", 8, "intro", ["Am"] * 8), ("1周目", 32, "verse", CH8 * 4), ("2周目", 32, "verse", CH8 * 4), ("3周目", 32, "chorus", CH8D * 4),
      ("小石", 4, "outro", ["Am"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("祈り", 0, 0.64), ("1周目", 0, 0.66), ("1周目", 31, 0.7), ("2周目", 0, 0.72), ("2周目", 31, 0.78), ("3周目", 0, 0.82),
          ("3周目", 24, 0.9), ("3周目", 31, 0.84), ("小石", 0, 0.7)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="祈り", passing=True, tension=False)
S.fix_avoid = lambda t: 0
S.tempo = [{"bar": 1, "bpm": 60}, {"bar": 9, "bpm": 72}]
S.extra.update({"rubato": 0.35})
B = S.beats
G = c.g()
# 試し書き出し: オルガンの和音（3音）は笛より約6dB 小さい（小さなオルガンとして丁度よい）。竪琴は約3dB、低いドローンは笛と同じくらい
ORG = [S.track(f"小さなパイプオルガン{j + 1}", "pad", patch="churchOrgan", volume=0.05, pan=-0.15 + 0.15 * j, reverb=0.65, barGain=G) for j in range(3)]
HP = S.track("竪琴（泉の水）", "harp", patch="folkHarp", volume=0.07, pan=0.3, reverb=0.6, sustain=2.0, barGain=G)
DRN = [S.track(f"低いドローン（チェロ{x}）", "strings", patch="cello", volume=0.1, gainDb=5, pan=-0.05 + 0.1 * j, reverb=0.6, barGain=[round(v * 1.5, 3) for v in G])
       for j, x in enumerate(("A", "E"))]
PEB = S.track("小石（竪琴の1音）", "harp", patch="folkHarp", volume=0.1, pan=0.2, reverb=0.85, sustain=3.0, barGain=G)

# ---------- 祈りの節（A エオリア。1=A4。32小節） ----------
TUNE = ["1:2 3:1", "5:2 4:1", "3:1 2:1 1:1", "7,:3", "1:1 3:1 5:1", "6:2 5:1", "4:1 3:1 2:1", "3:3",
        "5:2 6:1", "7:2 6:1", "5:1 4:1 3:1", "2:3", "3:1 4:1 5:1", "6:1 5:1 4:1", "3:2 2:1", "1:3",
        "6:2 5:1", "4:2 3:1", "6:1 7:1 1':1", "7:3", "6:1 5:1 4:1", "3:2 4:1", "5:1 6:1 5:1", "5:3",
        "1':2 7:1", "6:2 5:1", "4:1 6:1 5:1", "3:3", "2:1 3:1 4:1", "6,:2 7,:1", "1:2 7,:1", "1:3"]
PRAY = ["1:3", "R:1 3:2", "2:1 1:1 7,:1", "1:3", "5,:2 6,:1", "7,:1 1:2", "2:3", "1:3"]       # 祈り：笛ひとり、自由に
play_melody(c, "祈り", PRAY, 4, "air", key=KA, density=0.2, seed=2601)
play_melody(c, "1周目", TUNE, 4, "air", key=KA, density=0.15, seed=2602)
play_melody(c, "2周目", TUNE, 4, "air", key=KA, density=0.25, seed=2603)
play_melody(c, "3周目", TUNE, 4, "air", key=KD, density=0.35, seed=2604)                   # 3周目：F が F♯ に（浄め）

# ---------- 伴奏（周ごとに増える） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, sorted(57 + (p - 57) % 12 for p in (r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12))
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r, tones = tri(ch)
    if n in ("1周目", "2周目", "3周目"):
        if i % 2 == 0 or ch != S.chords[b - 1]:
            L = 6 if (i % 2 == 0 and b + 1 < c.NB and S.chords[b + 1] == ch) else 3
            for j, t in enumerate(tones): ORG[j].at(round(b * B + 0.02 * j, 3), f"{nm(t)}:{L},")
    if n in ("2周目", "3周目"):                                       # 竪琴：泉の水のように、上がって下りる分散和音
        lo = 45 + (r - 45) % 12
        HP.bar(b, " ".join(f"{nm(x)}:0.5{',' if q else ''}" for q, x in enumerate((lo, lo + 7, tones[1] + 12, tones[2] + 12, tones[1] + 12, lo + 7))))
    if n == "3周目" and i % 4 == 0:                                   # 低いドローン（A と E。4小節ずつ弓を返す）
        DRN[0].at(round(b * B + (0.05 if i else 0), 3), "A2:12,"); DRN[1].at(round(b * B + (0.05 if i else 0), 3), "E3:12,")
s0 = c.s0["小石"]
for j, t in enumerate(tri("Am")[1]): ORG[j].at(s0 * B, f"{nm(t)}:6,")
PEB.at(round(s0 * B + 4.5, 3), "A5:4")                                # 小石がひとつ、滝つぼに

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の026（第3版）。小川の上流、細い滝の落ちる聖なる泉で、エイラが祈りの節を3回吹く（泉のまわりを3周する「巡り」）。3/4・♩=72、A エオリア。1周ごとに、小さなパイプオルガン → 竪琴 → 低いドローンと気配が増え、3周目は旋法の1音（F）だけが F♯ に明るくなる（浄め）。最後は滝つぼに小石が1つ落ちる音。",
       harm_scenes=None, tail_scene="小石", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air026.json", "w"), ensure_ascii=False)
