# ケルト・フルート100曲「銀の笛と百の夜」066 山羊の乳搾り Milking the Goats — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 村の朝早く、納屋で娘が山羊の乳をしぼっている。両手が交互に動く一定の音にあわせて、エイラは低い笛で仕事歌を吹く。
#   乳しぼりの拍は最後まで少しも変わらない。節だけが、ひとふしごとに少しずつ変わっていき、最後はもとの節に戻る。
#   乳しぼりが終わっても、拍だけがしばらく続いて、やむ。
# 調べ: 眠り。形: 仕事歌（一定の手の拍の上で、8小節の節を13回。毎回1か所ずつ節が変わり、最後の回でもとに戻る）。
# 拍子・速さ: 6/8・付点4分＝54（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。旋法: B♭ ミクソリディア（A♭）。
# 主役は笛（低め・くり返す。F4〜F5）。伴奏の主役: ビオラのピチカート（乳しぼりの拍。B♭ と F を交互に、ずっと同じ形）。脇: チェロの長い低音。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 乳しぼりの拍は最初から最後までまったく同じで、旋律だけが少しずつ変わる。
# 始まり: ピチカートの拍 → 終わり: 拍だけが残る。
# 山: なし。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "066-milking-the-goats", "山羊の乳搾り", "Milking the Goats", 54, 2, "Bb", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.25})
K = Key("Bb", "mixolydian", 4)
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CH8 = ["Bb", "Bb", "Bb", "Bb", "Ab", "Ab", "F", "Bb"]
SC = [("拍", 2, "intro", ["Bb", "Bb"]), ("仕事歌", 104, "verse", CH8 * 13), ("拍だけ", 6, "outro", ["Bb"] * 6)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("拍", 0, 0.7), ("仕事歌", 0, 0.68), ("仕事歌", 52, 0.72), ("仕事歌", 103, 0.68), ("拍だけ", 0, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="拍", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# ピチカート（0.12・gainDb 5）は笛の約6dB 下（052）。拍だけの所（始まりと終わり）は別のパートで大きく（057 と同じ gainDb 12）
PZ = [S.track(f"ビオラのピチカート（{x}の手）", "strings", patch="pizzicato", volume=0.1, gainDb=5, pan=p, reverb=0.35, barGain=[0.7] * c.NB) for x, p in (("右", 0.2), ("左", -0.05))]
PZI = [S.track(f"ビオラのピチカート（拍だけの{x}の手）", "strings", patch="pizzicato", volume=0.1, gainDb=12, pan=p, reverb=0.35, barGain=[0.7] * c.NB) for x, p in (("右", 0.2), ("左", -0.05))]
VC = S.track("チェロ（長い低音）", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.25, reverb=0.65, release=0.7, barGain=G)

# ---------- 乳しぼりの拍（ずっと同じ。右手 B♭3 が 8分の1・4つ目、左手 F4 が 3・6つ目） ----------
for b in range(c.NB):
    n = S.scene_of(b)[0]
    r, l = PZI if n in ("拍", "拍だけ") else PZ
    r.bar(b, "Bb3:0.3333 R:0.6667 Bb3:0.3333 R:0.6667")
    l.bar(b, "R:0.6667 F4:0.3333, R:0.6667 F4:0.3333,")

# ---------- 仕事歌（8小節の節。毎回1か所ずつ変わり、最後はもとに戻る） ----------
P = ["1:3 7,:2 1:1", "2:3 1:3", "5,:2 6,:1 7,:2 1:1", "1:6", "3:3 2:2 1:1", "2:2 3:1 4:3", "3:2 2:1 7,:2 5,:1", "1:6"]
MUT = [(3, "1:3 2:3"), (1, "2:2 3:1 1:3"), (5, "2:2 3:1 5:3"), (4, "3:2 4:1 2:2 1:1"), (7, "1:3 5,:3"), (0, "1:2 2:1 7,:2 1:1"),
       (2, "5,:2 7,:1 1:2 2:1"), (6, "3:2 4:1 2:2 7,:1"), (5, "4:2 3:1 5:3"), (3, "2:3 3:3"), (7, "1:6"), (4, "5:3 4:2 3:1")]
s0 = c.s0["仕事歌"]
cur = list(P)
for k in range(13):
    if 1 <= k <= 11:
        i, v = MUT[k - 1]; cur[i] = v
    bars = list(P) if k == 12 else list(cur)
    ev = []
    for j, s_ in enumerate(e2b(bars)): ev += mel_events(K, s_, 4, (s0 + 8 * k + j) * B)
    play(c.FLUTE, ornament([[round(t, 4), L, m] for t, L, m in ev], K, 54, "air", B, density=0.12, seed=6600 + k))

# ---------- チェロの長い低音（B♭ 4小節 → A♭ 2小節 → F → B♭） ----------
for b in range(s0, s0 + 104):
    i = (b - s0) % 8
    if i == 0: VC.at(b * B, f"Bb2:{4 * B + 0.2}")
    elif i == 4: VC.at(b * B, f"Ab2:{2 * B + 0.2},")
    elif i == 6: VC.at(b * B, f"F2:{B + 0.2},")
    elif i == 7: VC.at(b * B, f"Bb2:{B + 0.2},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の066（第3版）。朝の納屋で、娘が山羊の乳をしぼる。6/8・付点4分＝54、B♭ ミクソリディア。ビオラのピチカートが両手の交互の動き（B♭ と F）を、最初から最後までまったく同じ形で刻む。その上で低めの笛が8小節の仕事歌を13回くり返し、毎回1か所ずつ節が変わって、最後の回でもとの節に戻る。下にチェロの長い低音。山はなく、最後は乳しぼりの拍だけが残る。",
       harm_scenes=None, tail_scene="拍だけ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.25, "lp": 2800, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air066.json", "w"), ensure_ascii=False)
