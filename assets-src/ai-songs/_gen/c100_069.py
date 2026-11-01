# ケルト・フルート100曲「銀の笛と百の夜」069 寝息 Sleeping Breath — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 祭りの前の夜もふけ、村の家々は眠りにつく。エイラが泊めてもらった家の窓から、静かな寝息が聞こえる。
#   エイラは小さく笛で子守歌を吹く。吹くたびに節は少しずつ細くなり、最後は自分もまどろんで、節の途中で笛が止まる。
# 調べ: 眠り。形: 眠りの調べ（8小節の同じ節を8回。回ごとに音が少しずつ抜けて細くなり、8回目は途中で消える）。
# 拍子・速さ: 3/4・♩=48。旋法: F イオニア。
# 主役は笛（ささやく笛）。伴奏の主役: リードオルガンの和音（寝息のように、強弱がゆっくり呼吸する）。脇: 竪琴の高い倍音（チェレスタのかわり）。
#   ギター・ピアノ・パッド・弦・打楽器・2本目の笛は使わない。
# この曲だけ: 家々の寝息のように、オルガンの和音の強弱がゆっくり呼吸する（2小節で吸って、2小節で吐く）。
# 始まり: オルガンの和音 → 終わり: 旋律の途中で消える（そのあと寝息の和音だけが少し続く）。
# 山: なし。
import sys, json, re, math
from c100_common import *
from c100_v2 import *

S = Song("C100", "069-sleeping-breath", "寝息", "Sleeping Breath", 48, 3, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.25, "rubato": 0.15})
K = Key("F", "major", 4)
CH8 = ["F", "F", "Dm", "F", "Bb", "C", "C", "F"]
SC = [("オルガン", 2, "intro", ["F", "F"]), ("子守歌", 61, "verse", CH8 * 7 + CH8[:5]), ("寝息だけ", 3, "outro", ["F"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("オルガン", 0, 0.68), ("子守歌", 0, 0.68), ("子守歌", 60, 0.62), ("寝息だけ", 0, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="オルガン", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# リードオルガン: 和音（3音）でも笛より約14dB 小さい → gainDb 6、オルガンだけの所は gainDb 12（015）
BREATH = [round(0.75 + 0.25 * math.sin(2 * math.pi * (b - 1) / 4), 3) for b in range(c.NB)]       # 4小節でひと呼吸
OR = [S.track(f"リードオルガン（寝息{j + 1}）", "pad", patch="reedOrgan", volume=0.1, gainDb=6, pan=-0.15 + 0.15 * j, reverb=0.6,
              barGain=[round(G[b] * BREATH[b], 3) for b in range(c.NB)]) for j in range(3)]
ORI = [S.track(f"リードオルガン（オルガンだけ{j + 1}）", "pad", patch="reedOrgan", volume=0.1, gainDb=12, pan=-0.15 + 0.15 * j, reverb=0.6,
               barGain=[round(0.7 * BREATH[b], 3) for b in range(c.NB)]) for j in range(3)]
HP = S.track("竪琴（高い倍音）", "harp", patch="folkHarp", volume=0.04, pan=0.35, reverb=0.75, sustain=2.0, barGain=G)

# ---------- 子守歌（8小節。1=F4。回ごとに音が抜けて細くなる） ----------
M = ["3:2 2:1", "1:2 5,:1", "6,:1 1:1 2:1", "3:3", "4:2 3:1", "2:2 1:1", "2:1 3:1 2:1", "1:3"]
THIN = [(6, "2:3"), (2, "1:3"), (4, "4:3"), (0, "3:3"), (5, "1:3"), (1, "1:2 R:1"), (3, "3:2 R:1")]
cur = list(M)
s0 = c.s0["子守歌"]
for k in range(8):
    if k >= 1: i, v = THIN[k - 1]; cur[i] = v
    bars = list(cur) if k < 7 else cur[:4] + ["4:1 R:2"]             # 8回目は5小節目の途中で消える
    ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (s0 + 8 * k + j) * B)
    play(c.FLUTE, ornament([[round(t, 4), L, m] for t, L, m in ev], K, 48, "air", B, density=max(0.0, 0.15 - 0.02 * k), seed=6900 + k))

# ---------- オルガンの寝息（1小節ごとに打ちなおす。吸うときは少し強く、吐くときは弱く）と竪琴の倍音 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r, th, fi = tri(ch)
    trs = ORI if n in ("オルガン", "寝息だけ") else OR
    inhale = BREATH[b] >= 0.75
    for j, m in enumerate((near(r, 53), near(th, 57), near(fi, 60))):
        trs[j].at(round(b * B + 0.04 * j, 3), f"{nm(m)}:{B + 0.3}{'' if inhale else ','}")
    if n == "子守歌" and b % 2 == 1:
        HP.at(round(b * B + 1.0, 3), f"{nm(near(fi, 84))}:2,"); HP.at(round(b * B + 2.0, 3), f"{nm(near(th, 88))}:2,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の069（第3版）。祭りの前の夜がふけ、村の家々が眠りにつく。3/4・♩=48、F の長調。リードオルガンの和音が、寝息のように4小節でひと呼吸（2小節で吸って、2小節で吐く）、強弱をゆっくりくり返す。笛はささやくように8小節の子守歌を8回吹き、回ごとに音が少しずつ抜けて細くなる。上には竪琴の高い倍音がまばらに。8回目、笛は節の途中で止まり、寝息の和音だけが少し続いて終わる。",
       harm_scenes=None, tail_scene="寝息だけ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2600, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air069.json", "w"), ensure_ascii=False)
