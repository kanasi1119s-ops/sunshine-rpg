# ケルト・フルート100曲「銀の笛と百の夜」089 吹雪を越えて Through the Blizzard — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 北の峰の最後の登り。猛烈な吹雪が、うしろから追いかけてくる。エイラは風に逆らって走るように進む。
#   平原をぬけ、急な崖を登りきった瞬間、吹雪がうそのように晴れ、真っ青な空の下に、笛の音だけが残る。
# 調べ: あいだ。形: 追われるような速いジグ（弦の8分のオスティナートで駆ける）。平原（AABB×3）→ 急な崖（AABB×3。太鼓が加わり、刻みが厚く）→ 晴れ間（笛ひとり）。
# 拍子・速さ: 6/8・付点4分＝126（晴れ間は 60）。旋法: C エオリア。
# 主役は笛（風に抗う笛）。伴奏の主役: 弦の速い刻み（バイオリンとビオラの8分のオスティナート）。打楽器はボーランと大太鼓（崖から）。
#   竪琴・ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 吹雪が晴れた瞬間に全員が抜けて、笛だけが青空に残る（晴れ間はテンポも半分になり、笛ひとり）。
# 始まり: 弦の刻み → 終わり: 急に静かな晴れ間。
# 山: 平原 → 急な崖（崖がいちばん激しい）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "089-through-the-blizzard", "吹雪を越えて", "Through the Blizzard", 126, 2, "C", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
K = Key("C", "minor", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Cm", "Fm", "Cm", "Ab", "Cm", "Fm", "Bb", "Cm"]; CB = ["Cm", "Fm", "Cm", "Bb", "Ab", "Cm", "Bb", "Cm"]
T = CA * 2 + CB * 2
SC = [("刻み", 4, "intro", ["Cm"] * 4), ("平原", 96, "verse", T * 3), ("急な崖", 96, "chorus", T * 3), ("晴れ間", 24, "outro", CA * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("刻み", 0, 0.78), ("平原", 0, 0.76), ("平原", 95, 0.82), ("急な崖", 0, 0.86), ("急な崖", 95, 0.98), ("晴れ間", 0, 0.76), ("晴れ間", 23, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="刻み", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 126}, {"bar": s["晴れ間"] + 1, "bpm": 60}]
B = S.beats
G = c.g()
OS = [S.track(f"弦の刻み（{x}）", "strings", patch=p, volume=v, pan=pn, reverb=0.3, barGain=[round(y * (1.4 if b < 4 else 1.0), 3) for b, y in enumerate(G)])
      for x, p, v, pn in (("バイオリン", "violin", 0.012, 0.35), ("ビオラ", "viola", 0.01, -0.35), ("チェロ", "cello", 0.016, -0.15))]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]
BD = S.track("大太鼓（崖）", "strings", patch="inchTom", volume=0.12, gainDb=12, pan=0, reverb=0.4, barGain=G)       # ティンパニは鳴らないので録音のタム（071）

# ---------- 速いジグ（8分＝1、1小節＝6。1=C4。C4 より下には行かない） ----------
A = ["1:1 3:1 5:1 1':1 5:1 3:1", "4:1 6:1 1':1 6:1 4:1 2:1", "1:1 3:1 5:1 7:2 5:1", "6:1 5:1 4:1 3:3",
     "1:1 3:1 5:1 1':1 5:1 3:1", "4:1 6:1 1':1 2':2 1':1", "7:1 5:1 3:1 4:1 3:1 2:1", "1:3 1:3"]
Bm = ["5:2 1':1 1':2 7:1", "6:2 1':1 7:2 5:1", "5:2 1':1 1':1 2':1 3':1", "2':3 7:3",
      "1':2 5:1 6:2 4:1", "5:2 3:1 4:2 2:1", "3:1 4:1 5:1 2:1 3:1 2:1", "1:3 1:3"]
TUNE = A + A + Bm + Bm
play_melody(c, "平原", e2b(TUNE * 3), 4, "jig", key=K, density=0.4, seed=8901)
play_melody(c, "急な崖", e2b(TUNE * 3), 4, "jig", key=K, density=0.55, seed=8902)
AIR = ["5:6", "4:3 3:3", "5:3 1':3", "7:6", "1':6", "2':3 1':3", "7:3 6:3", "5:6"] * 3
play_melody(c, "晴れ間", e2b(AIR[:22] + ["5:6", "R:6"]), 5, "air", key=K, density=0.15, seed=8903)     # 青空に笛だけ（1オクターブ上で、長く）

# ---------- 弦の刻み（8分のオスティナート）・ボーラン・大太鼓 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
R3 = round(T3, 4)
for b in range(s["晴れ間"]):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 60)
    OS[0].bar(b, " ".join(f"{nm(x)}:{R3}{'!' if q == 0 else ','}" for q, x in enumerate((lo, near(fi, lo), lo + 12, near(fi, lo), near(th, lo), near(fi, lo)))))
    if n != "刻み" or i >= 2:
        OS[1].bar(b, " ".join(f"{nm(x)}:{R3}," for x in (near(th, 55), near(fi, 55), near(th, 55), near(r, 55), near(th, 55), near(fi, 55))))
    if n == "急な崖":
        OS[2].bar(b, f"{nm(near(r, 36))}:{R3}! {nm(near(r, 36))}:{R3}, {nm(near(fi, 36))}:{R3}, {nm(near(r, 36))}:{R3} {nm(near(r, 36))}:{R3}, {nm(near(fi, 36))}:{R3},")
        BD.bar(b, "F2:1! A2:1," if i % 4 != 3 else "F2:0.3333! F2:0.3333! F2:0.3333! F2:1!")
    if n == "刻み": continue
    d = DR[b % 2]; fill = (i % 8 == 7)
    d.bar(b, f"C3:{R3}! E3:{R3}, C3:{R3}, C3:{R3}! E3:{R3}, C3:{R3}," if not fill else f"C3:{R3}! E3:{R3}, C3:{R3}, C3:{R3}! C3:{R3}! C3:{R3}!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の089（第3版）。北の峰の最後の登りで、吹雪に追われる。速いジグ（6/8・付点4分＝126）、C エオリア。弦の8分のオスティナートの刻みで始まり、ボーランに乗って笛が風に逆らって駆ける。平原（AABB×3）から急な崖（AABB×3。チェロの刻みと大太鼓が加わっていちばん激しい）へ。登りきった瞬間に吹雪が晴れ、全員が抜けて、テンポも半分になり、笛だけが青空に長く残る。",
       harm_scenes=None, tail_scene="晴れ間", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 3000, "rt": 4.4}}}
json.dump(air, open("/tmp/cel/w/air089.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
