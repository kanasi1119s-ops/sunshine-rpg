# ケルト・フルート100曲「銀の笛と百の夜」081 雪の峠 The Snowy Pass — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第9章のはじまり。祖父の約束を胸に、エイラは鐘のある北の峰へ向かう。雪の積もった峠道を、一歩ずつ、決意をこめて登る。
#   峠に着いた瞬間、目の前に広がるのは、誰もいない白い世界。明るい決意の行進は、さびしい短調に変わる。
# 調べ: あいだ。形: 一歩ずつ登る行進（16小節の節を3回、回ごとに伴奏が増える）→ 峠に着いて、さびしい短調の歌（24小節）。
# 拍子・速さ: 4/4・♩=76。旋法: D イオニア → B エオリア。
# 主役は笛（決意の笛 → さびしい笛）。伴奏の主役: ティンパニ（一歩ずつの足取り）と弦。脇: ブズーキ風のギター（2回目から）。
#   竪琴・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 峠に着いた瞬間、長調から短調へ（D の長調の行進 → B の短調。ギターと太鼓は止まり、弦と笛だけになる）。
# 始まり: 太鼓だけ → 終わり: 頂でさびしい短調。
# 山: 頂で1つ（着いた瞬間）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "081-the-snowy-pass", "雪の峠", "The Snowy Pass", 76, 4, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
KD, KB = Key("D", "major", 4), Key("B", "minor", 3)
CA = ["D", "G", "D", "A", "D", "G", "A", "D"]; CB = ["D", "Em", "A", "A", "G", "D", "A", "D"]
CS = ["Bm", "A", "G", "Bm", "Em", "Bm", "A", "Bm", "G", "Em", "D", "F#m", "G", "D", "A", "Bm"]
SC = [("太鼓", 2, "intro", ["D", "D"]), ("登り1", 16, "verse", CA + CB), ("登り2", 16, "verse", CA + CB), ("登り3", 16, "verse", CA + CB),
      ("頂", 24, "chorus", CS + CS[:8]), ("白い世界", 4, "outro", ["Bm"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("太鼓", 0, 0.78), ("登り1", 0, 0.74), ("登り2", 0, 0.78), ("登り3", 0, 0.84), ("登り3", 15, 0.9), ("頂", 0, 0.94), ("頂", 4, 0.78), ("頂", 23, 0.7),
          ("白い世界", 0, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="太鼓", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# ティンパニは E2 より上で（071: D3・A2 の 0.12 で笛とほぼ同じ）→ 足取りなので 0.09
# ティンパニ（timpani）は鳴らない（071 で分かった）→ 録音のタム（inchTom）。0.12・gainDb 12 で（071）
TP = S.track("大太鼓（足取り）", "strings", patch="inchTom", volume=0.1, gainDb=12, pan=0, reverb=0.45, barGain=[round(x * (1.4 if b < 2 else 1.0), 3) for b, x in enumerate(G)])
GT = [S.track(f"ブズーキ風ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=0.25 - 0.1 * i, reverb=0.3, barGain=G) for i in range(5)]
VC = S.track("チェロ", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.25, reverb=0.65, release=0.7, barGain=G)
VA = S.track("ビオラ", "strings", patch="viola", volume=0.017, pan=0.05, reverb=0.65, release=0.7, barGain=G)
VN = S.track("バイオリン", "strings", patch="violin", volume=0.025, gainDb=3, pan=0.3, reverb=0.7, release=0.7, barGain=G)

# ---------- 行進（1=D4）と、頂の短調の歌（1=B3。C♯4 より下には行かない） ----------
A = ["1:1 1:0.5 2:0.5 3:1 5:1", "4:1 3:0.5 2:0.5 3:2", "1:1 1:0.5 2:0.5 3:1 6:1", "5:2 4:1 3:1",
     "6:1 5:0.5 4:0.5 3:1 1:1", "2:1 3:0.5 4:0.5 5:2", "4:1 3:1 2:1 7,:1", "1:4"]
Bm = ["5:1 5:0.5 6:0.5 7:1 1':1", "2':1 1':0.5 7:0.5 6:2", "5:1 6:0.5 7:0.5 1':1 3':1", "2':4",
      "1':1 7:0.5 6:0.5 5:1 3:1", "4:1 5:0.5 6:0.5 5:2", "3:1 2:1 1:1 7,:1", "1:4"]
SUM = ["5:2 4:1 3:1", "4:2 2:2", "3:1 4:1 5:1 6:1", "5:4", "1':2 7:1 6:1", "5:2 4:2", "3:1 4:1 2:2", "1':4",
       "3':2 2':1 1':1", "7:2 6:2", "5:1 6:1 7:1 1':1", "2':4", "3':2 2':1 1':1", "7:2 5:2", "6:1 5:1 4:1 2:1", "1':4"]
for k in range(3):
    play_melody(c, f"登り{k + 1}", A + Bm, 4, "march", key=KD, density=(0.25, 0.35, 0.45)[k], seed=8100 + k)
play_melody(c, "頂", SUM + SUM[:8], 3, "air", key=KB, density=0.2, seed=8110)
c.FLUTE.at(c.s0["白い世界"] * B, "F#4:12")

# ---------- 伴奏 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
MARCH = [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 0.5, "d", ","), (3.5, 0.5, "u", ",")]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    if n == "太鼓" or n.startswith("登り"):
        TP.bar(b, "F2:1! A2:1, F2:1 A2:1," if ch != "A" else "G2:1! C3:1, G2:1 C3:1,")
    if n.startswith("登り"):
        lvl = int(n[-1])
        if lvl >= 2: strum(GT, b, B, ch, MARCH)
        if i % 2 == 0:
            VC.at(b * B, f"{nm(near(r, 38))}:{2 * B + 0.2}{',' if i % 4 else ''}")
            if lvl >= 2: VA.at(round(b * B + 0.05, 3), f"{nm(near(th, 54))}:{2 * B + 0.15},")
            if lvl >= 3: VN.at(round(b * B + 0.1, 3), f"{nm(near(fi, 64))}:{2 * B + 0.1},")
    elif n in ("頂", "白い世界"):                                       # 頂：ギターと太鼓は止まり、弦だけがさびしく
        if n == "頂" and i == 0:
            TP.at(b * B, "F2:4!")                                       # 着いた瞬間の1打
        if i % 2 == 0:
            L = 2 * B + 0.2 if n == "頂" else 4 * B
            VC.at(b * B, f"{nm(near(r, 35))}:{L}"); VA.at(round(b * B + 0.05, 3), f"{nm(near(th, 54))}:{L - 0.05},")
            if n == "頂" and i < 16: VN.at(round(b * B + 0.1, 3), f"{nm(near(fi, 66))}:{L - 0.1},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の081（第3版）。第9章のはじまり、祖父の約束を胸に、雪の峠道を一歩ずつ登る。4/4・♩=76。ティンパニの足取りだけで始まり、D の長調の決意の行進を3回、回ごとにブズーキ風のギターと弦が増える。峠に着いた瞬間（ティンパニの1打。山）、長調は B の短調に変わり、ギターと太鼓は止まって、弦と笛だけのさびしい歌になる。最後は誰もいない白い世界。",
       harm_scenes=None, tail_scene="白い世界", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air081.json", "w"), ensure_ascii=False)
