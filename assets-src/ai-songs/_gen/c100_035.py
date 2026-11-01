# ケルト・フルート100曲「銀の笛と百の夜」035 光る茸 Foxfire — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 真夜中、苔の上で目をさますと、まわりの茸がぽう、ぽう、と青く光っている。光は鬼火のように、ふっと消えては別の所にともる。
#   エイラは笛を吹きながら光を追いかけるが、光の跳ね方は笛の拍と合わず、どこにともるか分からない。
#   やがて夜明けが近づき、光は1つずつ消え、最後は笛だけが暗い森に残る。
# 調べ: 喜び（不思議）。形: 鬼火の追いかけっこ（ポリリズム）。笛は 6/8 のジグで追い、光は付点8分（2拍子の4つ）でともる＝拍がつかめない。
# 拍子・速さ: 6/8・付点4分＝120（1拍＝付点4分、1小節＝2拍で書く。笛の8分は 1/3 拍、光の付点8分は 0.5 拍）。旋法: B エオリア。
# 主役は笛（追う笛）。伴奏の主役: マリンバ（光る茸の点。左右のあちこちに、決まった順でなくともる）と、2回目の灯からピチカート。
#   脇: 暗闇の低い持続（チェロとコントラバス）。竪琴・ギター・ピアノ・パッド・打楽器は使わない。
#   014「迷い羊」（ピチカートが左右に順に跳ね、笛が 2+2+2 で追う）とは、光の拍（付点8分＝4対3）と、ともる場所（ばらばら）を変えた。
# この曲だけ: 6/8 の上に、付点8分の点（2拍子の4つ）が重なり、拍がつかめない。最後は光が1つずつ消える。
# 始まり: 暗闇の低い持続 → 終わり: 灯が消えて笛だけ。
# 山: 中盤（灯2）。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

BPM = 120
S = Song("C100", "035-foxfire", "光る茸", "Foxfire", BPM, 2, "B", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("B", "minor", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Bm", "Bm", "Em", "F#m", "Bm", "G", "Em", "Bm"]
CB = ["G", "D", "A", "Bm", "Em", "F#m", "G", "Bm"]
AB = CA + CA + CB + CB
SC = [("闇", 8, "intro", ["Bm"] * 8), ("灯1", 64, "verse", AB * 2), ("灯2", 64, "chorus", AB * 2), ("迷う", 32, "verse", AB),
      ("灯3", 64, "verse", AB * 2), ("消える", 24, "outro", (CA + CB + CA))]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("闇", 0, 0.64), ("灯1", 0, 0.72), ("灯2", 0, 0.82), ("灯2", 48, 0.9), ("迷う", 0, 0.7), ("灯3", 0, 0.78), ("消える", 0, 0.72), ("消える", 23, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="闇", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: マリンバ（0.07）は笛より少し大きい → 0.05。ピチカート（gainDb 5）は笛より約2dB、チェロは約5dB 小さい
MR = [S.track(f"マリンバ（光る茸{j + 1}）", "strings", patch="marimba", volume=0.05, pan=p, reverb=0.6, barGain=G) for j, p in enumerate((-0.7, -0.25, 0.25, 0.7))]
PZ = [S.track(f"ピチカート（光{j + 1}）", "strings", patch="pizzicato", volume=0.1, gainDb=5, pan=p, reverb=0.55, barGain=G) for j, p in enumerate((-0.5, 0.5))]
VC = [S.track(f"チェロ（闇{j + 1}）", "strings", patch="cello", volume=0.014, gainDb=1, pan=-0.1, reverb=0.7, release=0.6, barGain=[round(x * 1.4, 3) for x in G]) for j in range(2)]
CBS = S.track("コントラバス（闇）", "strings", patch="contrabass", volume=0.05, pan=0.1, reverb=0.65, release=0.6, barGain=G)

# ---------- 笛のジグ（B エオリア。1=B4。8分＝1、1小節＝6） ----------
A = ["5:1 4:1 3:1 1:3", "2:1 3:1 4:1 5:3", "6:2 5:1 4:2 3:1", "2:3 5,:3",
     "5:1 4:1 3:1 1:2 3:1", "2:2 4:1 7:3", "1':2 7:1 6:2 5:1", "4:2 2:1 1:3"]
Bm = ["1':3 7:2 6:1", "5:2 6:1 7:3", "1':1 7:1 1':1 7:2 5:1", "6:3 4:3",
      "3:2 4:1 5:2 6:1", "7:2 6:1 5:3", "4:2 3:1 2:2 7,:1", "1:3 R:3"]
for n, d in (("灯1", 0.3), ("灯2", 0.55), ("灯3", 0.45)):
    play_melody(c, n, e2b((A + A + Bm + Bm) * 2), 4, "march", key=K, density=d, seed=3500 + len(n) + int(n[1]))
LOST = ["5:6", "4:3 3:3", "2:6", "1:6", "3:6", "2:3 7,:3", "1:6", "5,:6"] * 4                # 迷う：長い音で、光を見失う
play_melody(c, "迷う", e2b(LOST), 4, "air", key=K, density=0.2, seed=3510)
play_melody(c, "消える", e2b((A + Bm)[:16] + ["1:6", "3:6", "1:6", "R:6", "5:6", "1:6", "1:6", "R:6"]), 4, "march", key=K, density=0.25, seed=3511)

# ---------- 光る茸（付点8分＝0.5拍の点。ともる場所も高さも、決まった順でない） ----------
LIGHT = [71, 74, 76, 78, 81, 83, 86]                  # B ミナー・ペンタトニックの高い所
rng = random.Random(3535)
PROB = {"闇": 0.12, "灯1": 0.45, "灯2": 0.7, "迷う": 0.25, "灯3": 0.55}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b)
    p = PROB.get(n, 0.55 * (1 - i / 24))              # 消える：だんだん少なく（光が1つずつ消える）
    if n == "消える" and i >= 20: p = 0.0
    for q in range(4):                                # 1小節に付点8分が4つ（笛の 6/8 と合わない）
        if rng.random() < p:
            m = rng.choice(LIGHT); tr = rng.choice(MR)
            tr.at(round(b * B + 0.5 * q, 3), f"{nm(m)}:0.5{'' if q == 0 else ','}")
            if n in ("灯2", "灯3") and rng.random() < 0.35:
                rng.choice(PZ).at(round(b * B + 0.5 * q + 0.02, 3), f"{nm(m - 12)}:0.5,")

# ---------- 暗闇の低い持続（B と F♯。消える の途中で止まり、笛だけが残る） ----------
end = (c.s0["消える"] + 16) * B
st, k = 0.0, 0
while st < end - 0.01:
    en = min(end, st + 8.2)
    VC[k % 2].at(round(st, 3), f"F#3:{round(en - st, 3)}{',' if st else ''}")
    CBS.at(round(st, 3), f"B1:{round(min(8, en - st), 3)},") if k % 2 == 0 else None
    st += 8; k += 1

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.25 --side-hpf 200",
       "ケルト・フルート100曲の035（第3版）。真夜中、苔の上の茸が鬼火のように青く光る。6/8・付点4分＝120、B エオリア。笛はジグで光を追うが、マリンバの光は付点8分（2拍子の4つ）でともり、左右のあちこちに決まった順でなく現れるので、拍がつかめない。山は中盤、2回目の灯ではピチカートの光も加わる。夜明けが近づくと光は1つずつ消え、最後は笛だけが暗い森に残る。",
       harm_scenes=None, tail_scene="消える", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.26, "lp": 2800, "rt": 3.0}}}
json.dump(air, open("/tmp/cel/w/air035.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
