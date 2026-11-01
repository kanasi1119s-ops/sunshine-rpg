# ケルト・フルート100曲「銀の笛と百の夜」076 岬の灯台 The Lighthouse on the Cape — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 迷いながら、エイラは小舟をこいで岬の灯台へ渡る。祖父がよく通った道すじ。オールを引く重い一打と、戻す軽い一打。
#   波のせいで漕ぐ間合いはそろわず、ときどき、ひとかきが長くのびる。灯台に着くと、はじめの節に戻って、波の音に消える。
# 調べ: 悲しみ。形: 舟こぎのピーブロック（主題 → 変奏4つ。変奏ごとに音が密になる → 主題に戻って消える）。
# 拍子・速さ: 6/8・付点4分＝72（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。ときどき1小節だけ遅くなって、1拍のびる。旋法: G エオリア。
# 主役は笛（低い笛。G4〜D5 が中心）。伴奏の主役: 低い弦（チェロとコントラバスの G と D）と枠太鼓（オールを引く大きく低い1打と、戻す軽い1打）。
#   竪琴・ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: オールを引く重い拍と戻す軽い拍が不ぞろいで（軽い拍が早まったり遅れたりする）、ときどき1拍のびる。
# 始まり: 太鼓の重い1打 → 終わり: 主題に戻って消える。
# 山: 変奏ごとに密に（変奏4がいちばん密）。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "076-the-lighthouse-on-the-cape", "岬の灯台", "The Lighthouse on the Cape", 72, 2, "G", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
K = Key("G", "minor", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CH8 = ["Gm", "F", "Gm", "Gm", "Bb", "Gm", "F", "Gm"]
SC = [("重い1打", 2, "intro", ["Gm", "Gm"]), ("主題", 24, "verse", CH8 * 3), ("変奏1", 24, "verse", CH8 * 3), ("変奏2", 24, "verse", CH8 * 3),
      ("変奏3", 24, "verse", CH8 * 3), ("変奏4", 24, "chorus", CH8 * 3), ("主題に戻る", 24, "outro", CH8 * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("重い1打", 0, 0.76), ("主題", 0, 0.7), ("変奏1", 0, 0.72), ("変奏2", 0, 0.76), ("変奏3", 0, 0.8), ("変奏4", 0, 0.86), ("変奏4", 23, 0.92),
          ("主題に戻る", 0, 0.72), ("主題に戻る", 23, 0.56)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="重い1打", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
# ときどき1拍のびる：その小節だけ ♩.=48（1.5倍の長さ＝1拍ぶん長い）
rng = random.Random(7601)
LONG = sorted(rng.sample(range(s["主題"] + 3, s["主題に戻る"] - 2, 1), 9))
LONG = [b for k, b in enumerate(LONG) if k == 0 or b - LONG[k - 1] > 4]
S.tempo = [{"bar": 1, "bpm": 72}]
for b in LONG: S.tempo += [{"bar": b + 1, "bpm": 48}, {"bar": b + 2, "bpm": 72}]
B = S.beats
G = c.g()
VC = S.track("チェロ（G と D）", "strings", patch="cello", volume=0.03, gainDb=6, pan=-0.2, reverb=0.65, release=0.8, barGain=G)
CB_ = S.track("コントラバス（G）", "strings", patch="contrabass", volume=0.04, gainDb=6, pan=-0.05, reverb=0.65, release=0.8, barGain=G)
DR = S.track("枠太鼓（オール）", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=0.1, reverb=0.45, barGain=[round(x * 1.4, 3) for x in G])

# ---------- 主題と変奏（8分＝1、1小節＝6。1=G4） ----------
TH = ["1:4 7,:2", "1:3 3:3", "4:4 3:2", "2:6", "3:4 2:2", "1:3 5,:3", "7,:4 2:2", "1:6"]
PAIR = [("1", "7,"), ("1", "3"), ("4", "3"), ("2", "2"), ("3", "2"), ("1", "5,"), ("7,", "2"), ("1", "1")]
def var(level):
    out = []
    for a, b in PAIR:
        if level == 1: out.append(f"{a}:2 5,:1 {b}:2 5,:1")                                   # 歩む：旋律の音と低い D をかわるがわる
        elif level == 2: out.append(f"{a}:1 5,:1 {a}:1 {b}:1 5,:1 {b}:1")
        elif level == 3: out.append(f"{a}:1 5,:0.5 1:0.5 {a}:1 {b}:1 5,:0.5 1:0.5 {b}:1")      # 細かい飾りの音を入れて密に
        else: out.append(f"{a}:0.5 5,:0.5 1:0.5 {a}:0.5 3:0.5 {a}:0.5 {b}:0.5 5,:0.5 1:0.5 {b}:0.5 3:0.5 {b}:0.5")
    return out
play_melody(c, "主題", e2b(TH * 3), 4, "air", key=K, density=0.15, seed=7601)
for lv in range(1, 5):
    play_melody(c, f"変奏{lv}", e2b(var(lv) * 3), 4, "air" if lv < 3 else "march", key=K, density=0.1, seed=7601 + lv)
play_melody(c, "主題に戻る", e2b(TH * 2 + TH[:6] + ["1:6", "R:6"]), 4, "air", key=K, density=0.1, seed=7606)

# ---------- 低い弦（G と D の持続）と、オールの太鼓（重い拍と、不ぞろいな軽い拍） ----------
for b in range(0, c.NB, 2):
    n = S.scene_of(b)[0]
    VC.at(b * B, f"G2:{2 * B + 0.3}{',' if b % 4 else ''}"); VC.at(round(b * B + 0.05, 3), f"D3:{2 * B + 0.25},")
    if n != "主題に戻る" or b < s["主題に戻る"] + 16: CB_.at(b * B, f"G1:{2 * B + 0.3},")
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b)
    if n == "重い1打":
        if i == 0: DR.at(0, "C3:2!")
        continue
    if n == "主題に戻る" and i >= 18: continue
    light = round(1 + rng.choice((-0.15, 0, 0, 0.12, 0.2)), 3)          # 戻す軽い拍は早まったり遅れたり
    DR.at(b * B, "C3:1!"); DR.at(b * B + light, "E3:0.5,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.32 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の076（第3版）。迷いながら、小舟をこいで岬の灯台へ渡る。舟こぎのピーブロック（6/8・付点4分＝72、G エオリア）。低い笛の主題（G4〜D5）を、変奏4つでだんだん密にしていく（旋律の音と低い D をかわるがわる → 細かい飾りの音）。伴奏はチェロとコントラバスの G と D の持続、枠太鼓のオールを引く重い1打と、戻す軽い1打（不ぞろいで、早まったり遅れたりする）。ときどき1小節だけ遅くなって、ひとかきが1拍のびる。最後は主題に戻って消える。",
       harm_scenes=None, tail_scene="主題に戻る", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -44, "hp": 150, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2600, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air076.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
