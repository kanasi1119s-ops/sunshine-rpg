# ケルト・フルート100曲「銀の笛と百の夜」090 山頂の静寂 The Silence of the Summit — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第9章の終わり。吹雪をぬけて、エイラは北の峰の頂に立つ。風もなく、音もない。世界とあの世の境目が薄くなる場所。
#   エイラは長い1音ずつ、ゆっくり笛を吹く。1音吹くたびに、まわりの静けさがもどってくる。最後は笛の息が消える。
# 調べ: あいだ。形: 薄い場所（ほとんど音のない頂）。長い1音（3拍）と、1拍の完全な無音をくり返す。
# 拍子・速さ: 4/4・♩=50（ゆれを少し）。旋法: C イオニア（3度の E を抜く：C・D・F・G・A）。
# 主役は笛（長い1音ずつ）。伴奏: 弦合奏のとても弱いドローン（笛の音と同じ長さだけ鳴る。開いた5度だけ）。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 旋律の音と音の間に、1拍の完全な無音がある（弦も笛と一緒に止まる。息をそろえて休む）。
# 始まり: 無音のあとの笛の1音 → 終わり: 笛の息が消える。
# 山: なし。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "090-the-silence-of-the-summit", "山頂の静寂", "The Silence of the Summit", 50, 4, "C", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.2, "rubato": 0.1})
K = Key("C", "major", 5)
SEQ = [5, 6, 5, 4, 2, 1, 2, 4, 5, 8, 6, 5, 4, 5, 6, 8, 9, 8, 6, 5, 4, 2, 1, 2, 4, 5, 6, 8, 6, 5, 4, 2, 4, 5, 2, 1,
       5, 4, 5, 6, 5, 4, 2, 1, 2, 1, 5, 1]                          # 1 音1小節（度数。8＝1オクターブ上の 1、9＝その上の 2）
N = len(SEQ)
SC = [("無音", 1, "intro", ["C"]), ("頂", N, "verse", ["C"] * N), ("息が消える", 3, "outro", ["C"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("無音", 0, 0.66), ("頂", 0, 0.68), ("頂", N // 2, 0.72), ("頂", N - 1, 0.66), ("息が消える", 0, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="無音", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# とても弱いドローン（004 の長い弦の値の約半分）
VC = S.track("弦（とても弱いドローン・チェロ）", "strings", patch="cello", volume=0.012, gainDb=2, pan=-0.25, reverb=0.8, release=0.35, barGain=G)
VA = S.track("弦（とても弱いドローン・ビオラ）", "strings", patch="viola", volume=0.01, pan=0.2, reverb=0.8, release=0.35, barGain=G)
VN = S.track("弦（とても弱いドローン・バイオリン）", "strings", patch="violin", volume=0.012, gainDb=2, pan=0.35, reverb=0.85, release=0.35, barGain=G)

DEG = {1: 0, 2: 2, 4: 5, 5: 7, 6: 9, 8: 12, 9: 14}
ROOT = {1: 48, 2: 50, 4: 53, 5: 55, 6: 57, 8: 48, 9: 50}               # 笛の音の下に置く開いた5度の根音（3度なし）
s0 = c.s0["頂"]
for q, d in enumerate(SEQ):
    t = (s0 + q) * B
    m = 72 + DEG[d] - (12 if 72 + DEG[d] > 84 else 0)
    last = (q == N - 1)
    L = 3 if not last else 3 + 3 * B
    c.FLUTE.at(t, f"{nm(m)}:{L}{',' if q % 3 == 2 else ''}")            # 長い1音（3拍）→ 1拍の完全な無音
    r = ROOT[d] if d not in (6,) else 53
    VC.at(round(t + 0.05, 3), f"{nm(r - 12)}:{L - 0.15},"); VA.at(round(t + 0.1, 3), f"{nm(r - 5)}:{L - 0.2},")
    if q % 4 in (1, 2): VN.at(round(t + 0.15, 3), f"{nm(r + 7)}:{L - 0.25},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の090（第3版）。第9章の終わり、北の峰の頂。風もなく、音もない。4/4・♩=50、C の長調から3度の E を抜いた5音。1小節の無音のあと、笛が長い1音（3拍）を吹き、続く1拍は弦も一緒に止まる完全な無音。これを48回くり返す。下には、笛の音と同じ長さだけ鳴る、とても弱い弦の開いた5度。山はなく、最後は笛の息が消えていく。",
       harm_scenes=None, tail_scene="息が消える", double=False, fill=False, pads=False, silences=())
air = {"pre": 0.5, "tail": 6.0, "layers": [{"file": "0595", "db": -50, "hp": 220, "lp": 3400, "wide": 0.012, "duck": 0.6, "fade": 7}],
       "fx": {"far": {"db": -28, "delay": 0.34, "lp": 2600, "rt": 4.2}}}
json.dump(air, open("/tmp/cel/w/air090.json", "w"), ensure_ascii=False)
