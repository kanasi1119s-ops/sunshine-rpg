# ケルト・フルート100曲「銀の笛と百の夜」078 雨宿り Shelter from the Rain — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 泣きつかれたエイラは、灯台守の老婆の小屋で雨宿りをする。老婆がギターで子守歌の伴奏をつま弾き、エイラは小さな笛で合わせる。
#   小屋の中は狭く、音はすぐそばで乾いて聞こえる。外では雨が降り続いているが、とても遠い。やがてふたりの音は、雨音よりも小さくなって消える。
# 調べ: 眠り。形: 小屋の中の子守歌（16小節を4回 → 雨だけの間 → もう1回 → 消える）。
# 拍子・速さ: 6/8・付点4分＝48（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。旋法: G イオニア。
# 主役は笛（小さな笛。D4〜E5）。伴奏の主役: ナイロン弦ギター（揺れる分散和音）。外の雨: グロッケンのまばらな粒（とても遠く、響きだけが多い）。
#   竪琴・ピアノ・パッド・弦・打楽器・2本目の笛は使わない。
# この曲だけ: 部屋の中（笛とギター）は近く乾いた音、外の雨（グロッケンの粒）はとても遠い。最後は部屋の中の音が雨音より小さくなって消える。
# 始まり: ギターの揺れ → 終わり: 雨音より小さく消える。
# 山: なし。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "078-shelter-from-the-rain", "雨宿り", "Shelter from the Rain", 48, 2, "G", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.15})
K = Key("G", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CL = ["G", "D", "G", "G", "C", "G", "D", "G", "C", "G", "D", "G", "C", "Em", "D", "G"]
SC = [("ギターの揺れ", 4, "intro", ["G", "G", "C", "G"]), ("子守歌", 64, "verse", CL * 4), ("雨だけ", 8, "verse", ["G", "C", "G", "D", "G", "C", "G", "G"]),
      ("もう1回", 16, "verse", CL), ("消える", 8, "outro", ["G", "C", "G", "G", "G", "G", "G", "G"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ギターの揺れ", 0, 0.7), ("子守歌", 0, 0.68), ("子守歌", 63, 0.7), ("雨だけ", 0, 0.62), ("もう1回", 0, 0.64), ("消える", 0, 0.56), ("消える", 7, 0.3)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ギターの揺れ", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
c.FLUTE.spec["reverb"] = 0.06                                       # 部屋の中：近く乾いた笛
GB = S.track("ギター（親指）", "guitar", patch="nylonGuitar", volume=0.016, pan=-0.15, reverb=0.06, barGain=[round(x * (1.3 if b < 4 else 1.0), 3) for b, x in enumerate(G)])
GF = [S.track(f"ギター（指{j + 1}）", "guitar", patch="nylonGuitar", volume=0.008, pan=-0.25 + 0.1 * j, reverb=0.06, barGain=G) for j in range(2)]
RAIN = [S.track(f"外の雨（グロッケン{j + 1}）", "bell", patch="glockenspiel", volume=0.014, pan=-0.6 + 1.2 * j, reverb=0.98, barGain=[0.6] * c.NB) for j in range(2)]

# ---------- 子守歌（16小節。1=G4） ----------
M = ["3:3 2:2 1:1", "2:3 5,:3", "1:2 2:1 3:2 4:1", "5:6", "6:3 5:2 4:1", "3:3 2:3", "1:2 3:1 2:2 7,:1", "1:6",
     "5:3 6:2 5:1", "4:3 3:3", "2:2 3:1 4:2 2:1", "3:6", "4:3 3:2 2:1", "1:3 6,:3", "7,:2 1:1 2:2 7,:1", "1:6"]
play_melody(c, "子守歌", e2b(M * 4), 4, "air", key=K, density=0.15, seed=7801)
play_melody(c, "もう1回", e2b(M), 4, "air", key=K, density=0.08, seed=7802)
play_melody(c, "消える", e2b(["3:3 2:3", "1:6", "R:6", "R:6", "R:6", "R:6", "R:6", "R:6"]), 4, "air", key=K, density=0.0)

# ---------- ギターの揺れ（8分6つ：根音・5度・10度・オクターブ・10度・5度） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    if n == "消える" and i >= 4: continue
    lo = near(r, 40)
    seq = [lo, near(fi, lo + 1), near(th, lo + 12), lo + 12, near(th, lo + 12), near(fi, lo + 1)]
    GB.at(b * B, f"{nm(seq[0])}:{2 * T3 * 3}{'' if i % 4 == 0 else ','}")
    for q in range(1, 6):
        GF[q % 2].at(round(b * B + q * T3, 4), f"{nm(seq[q])}:{round(2 * T3, 4)},")
s0 = c.s0["消える"]
GB.at((s0 + 4) * B, "G2:6,"); GF[0].at(round((s0 + 4) * B + 0.5, 3), "D3:5.5,"); GF[1].at(round((s0 + 4) * B + 1.0, 3), "B3:5,")

# ---------- 外の雨（とても遠い。まばらに、最後まで降り続く） ----------
rng = random.Random(7801)
for b in range(c.NB + 1):
    if b >= c.NB: break
    n = S.scene_of(b)[0]
    dens = 0.55 if n in ("雨だけ", "消える") else 0.3
    for q in range(6):
        if rng.random() < dens:
            pcs = tri(S.chords[b])
            RAIN[rng.randrange(2)].at(round(b * B + q * T3 + rng.uniform(0, 0.1), 3), f"{nm(near(rng.choice(pcs), rng.choice((79, 84, 88))))}:1,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.06 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の078（第3版）。泣きつかれたエイラが、灯台守の老婆の小屋で雨宿りをする。6/8・付点4分＝48、G の長調。老婆のナイロン弦ギターが揺れる分散和音を弾き、エイラの小さな笛が16小節の子守歌を合わせる。部屋の中（笛とギター）は近く乾いた音、外の雨（グロッケンのまばらな粒）はとても遠く、響きだけが多い。山はなく、最後は部屋の中の音が雨音より小さくなって消える。",
       harm_scenes=None, tail_scene="消える", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -44, "hp": 200, "lp": 3600, "wide": 0.02, "duck": 0.2, "fade": 7}],
       "fx": {"far": {"db": -30, "delay": 0.1, "lp": 3000, "rt": 1.0}}}
json.dump(air, open("/tmp/cel/w/air078.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
