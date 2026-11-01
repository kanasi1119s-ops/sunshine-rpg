# ケルト・フルート100曲「銀の笛と百の夜」080 朝の水たまり Morning Puddles — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第8章の終わり。嵐の去った朝、岬の道はあちこち水たまりだらけ。泣いたあとのエイラは、子どものように水たまりを跳んで歩く。
#   小さな水たまりはひょいと跳び、大きな水たまりの所だけは、思いきり2歩ぶん跳んで、着地のあとに一瞬止まる。
# 調べ: 喜び。形: 跳ねるジグ2曲のセット（1曲目 AABB×3 → 2曲目 AABB×3 → 1曲目 AABBAA）。
# 拍子・速さ: 6/8・付点4分＝116（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。旋法: D イオニア。
# 主役は笛（跳ねる笛）。伴奏の主役: マリンバ（8分で跳ねる低音と和音）と竪琴（裏の和音）。打楽器はボーラン。
#   ギター・ピアノ・パッド・弦・2本目の笛は使わない。
# この曲だけ: 大きな水たまりの所（2曲目の B の5〜7小節目）だけ、2小節ぶん大きく跳んで、1小節まるごと全員が休む。
# 始まり: 水たまりの1跳び（笛の1音とボーランの1打）→ 終わり: 全員でジャン。
# 山: 2周目。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 116
S = Song("C100", "080-morning-puddles", "朝の水たまり", "Morning Puddles", BPM, 2, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("D", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
C1A = ["D", "G", "D", "A", "D", "G", "A", "D"]; C1B = C1A
C2A = ["D", "Em", "D", "A", "D", "G", "A", "D"]; C2B = ["D", "G", "D", "G", "D", "A", "A", "D"]
T1 = C1A * 2 + C1B * 2; T2 = C2A * 2 + C2B * 2
SC = [("1跳び", 2, "intro", ["D", "D"])] + [(f"1曲目{k + 1}", 32, ("chorus" if k == 1 else "verse"), T1) for k in range(3)] + \
     [(f"2曲目{k + 1}", 32, ("chorus" if k == 1 else "verse"), T2) for k in range(3)] + [("1曲目もう一度", 48, "chorus", T1 + C1A * 2), ("ジャン", 1, "outro", ["D"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("1跳び", 0, 0.8), ("1曲目1", 0, 0.76), ("1曲目2", 0, 0.88), ("1曲目3", 0, 0.8), ("2曲目1", 0, 0.8), ("2曲目2", 0, 0.9), ("2曲目3", 0, 0.82),
          ("1曲目もう一度", 0, 0.86), ("1曲目もう一度", 47, 0.96), ("ジャン", 0, 0.96)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="1跳び", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# マリンバ 0.05 で笛の約5dB 下（049）。8分で跳ねるので少し小さく
MR = [S.track(f"マリンバ{j + 1}", "strings", patch="marimba", volume=0.045, pan=-0.25 + 0.15 * j, reverb=0.35, barGain=G) for j in range(2)]
HP = [S.track(f"竪琴（裏の和音{j + 1}）", "harp", patch="folkHarp", volume=0.05, pan=0.2 + 0.1 * j, reverb=0.45, sustain=1.0, barGain=G) for j in range(3)]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]

# ---------- 2つのジグ（8分＝1、1小節＝6。1=D4） ----------
A1 = ["1:2 3:1 5:2 3:1", "4:2 6:1 5:2 3:1", "1:2 3:1 5:2 1':1", "7:2 5:1 6:3", "1:2 3:1 5:2 3:1", "4:2 6:1 5:2 3:1", "2:2 4:1 3:2 7,:1", "1:3 1:3"]
B1 = ["1':2 7:1 1':2 5:1", "6:2 5:1 6:2 2':1", "1':2 7:1 1':2 3':1", "2':3 1':3", "1':2 7:1 1':2 5:1", "6:2 1':1 5:2 3:1", "4:2 6:1 3:2 7,:1", "1:3 1:3"]
A2 = ["5:1 4:1 3:1 2:2 1:1", "2:2 3:1 4:3", "5:1 4:1 3:1 2:2 1:1", "7,:2 1:1 2:3", "5:1 4:1 3:1 2:2 1:1", "2:2 3:1 4:2 6:1", "5:2 4:1 3:2 2:1", "1:6"]
B2 = ["1':3 5:2 3:1", "4:2 5:1 6:3", "1':3 5:2 3:1", "2:2 3:1 4:3", "1:2 5:1 1':2 3':1", "5':3 R:3", "R:6", "5:1 3:1 2:1 1:3"]      # 5〜7小節目：大きな水たまり
for k in range(3):
    play_melody(c, f"1曲目{k + 1}", e2b(A1 + A1 + B1 + B1), 4, "jig", key=K, density=(0.35, 0.5, 0.4)[k], seed=8000 + k)
    play_melody(c, f"2曲目{k + 1}", e2b(A2 + A2 + B2 + B2), 4, "jig", key=K, density=(0.4, 0.5, 0.45)[k], seed=8010 + k)
play_melody(c, "1曲目もう一度", e2b(A1 + A1 + B1 + B1 + A1 + A1), 4, "jig", key=K, density=0.55, seed=8020)
play_melody(c, "1跳び", e2b(["R:3 5:1 R:2", "R:6"]), 4, "jig", key=K, density=0.0)
s0 = c.s0["ジャン"]
c.FLUTE.at(s0 * B, "D5:0.6!")

# ---------- 伴奏（大きな水たまりの休みの小節は全員休む） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
R3 = round(T3, 4)
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    d = DR[b % 2]
    if n == "1跳び":
        if i == 0: DR[0].at(1.0, "C3:0.5!")
        continue
    if n == "ジャン":
        DR[0].at(b * B, "C3:0.6!"); MR[0].at(b * B, "D3:0.6!"); MR[1].at(b * B, "A3:0.6!")
        for j, m in enumerate((62, 66, 69)): HP[j].at(b * B, f"{nm(m)}:0.6!")
        continue
    in_puddle = n.startswith("2曲目") and (i % 32) in (22, 30)                     # B の7小節目（休み）
    jump = n.startswith("2曲目") and (i % 32) in (20, 21, 28, 29)                  # B の5・6小節目（大きく跳ぶ）
    if in_puddle: continue
    lo = near(r, 50)
    if jump:                                                                       # 跳ぶ所：伴奏も大きく上へ
        MR[0].bar(b, f"{nm(lo)}:{R3}! {nm(lo + 7)}:{R3}, {nm(lo + 12)}:{R3}, {nm(lo + 19)}:{R3}! {nm(lo + 24)}:{R3}, {nm(lo + 19)}:{R3},")
        d.bar(b, f"C3:{R3}! E3:{R3}, E3:{R3}, C3:{R3}! C3:{R3}! C3:{R3}!")
        continue
    MR[0].bar(b, f"{nm(lo)}:{R3}! {nm(near(fi, lo + 1))}:{R3}, {nm(lo + 12)}:{R3}, {nm(lo)}:{R3} {nm(near(fi, lo + 1))}:{R3}, {nm(near(th, lo + 12))}:{R3},")
    if n.endswith("2") or n == "1曲目もう一度":                                   # 2周目と最後：マリンバの2本目も
        MR[1].bar(b, f"R:{R3} {nm(near(th, 62))}:{R3}, R:{R3} R:{R3} {nm(near(fi, 62))}:{R3}, R:{R3}")
    for j, m in enumerate((near(r, 62), near(th, 62), near(fi, 62))):
        HP[j].at(round(b * B + 2 * T3, 4), f"{nm(m)}:{R3},"); HP[j].at(round(b * B + 1 + 2 * T3, 4), f"{nm(m)}:{R3},")
    fill = (i % 8 == 7)
    d.bar(b, f"C3:{R3}! E3:{R3}, C3:{R3}, C3:{R3}! E3:{R3}, C3:{R3}," if not fill else f"C3:{R3}! E3:{R3}, C3:{R3}, C3:{R3}! C3:{R3}! C3:{R3}!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の080（第3版）。第8章の終わり、嵐の去った朝の岬の道で、水たまりを跳んで歩く。跳ねるジグ（6/8・付点4分＝116）2曲のセット、D の長調。笛の1音とボーランの1打（水たまりの1跳び）で始まり、マリンバの跳ねる8分、竪琴の裏の和音、ボーランに乗って笛が跳ねる。2曲目の B の大きな水たまりの所だけ、2小節ぶん大きく跳んで、1小節まるごと全員が休む。山は2周目。最後は全員でジャン。",
       harm_scenes=None, tail_scene="ジャン", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.15, "lp": 3000, "rt": 1.8}}}
json.dump(air, open("/tmp/cel/w/air080.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
