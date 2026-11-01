# ケルト・フルート100曲「銀の笛と百の夜」061 煙突の煙 Chimney Smoke — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第7章のはじまり。対岸の村に着くと、家々の煙突から煙が立ちのぼり、どこかの家から速い踊りの曲が聞こえてくる。
#   戸口をのぞくと、2人のフィドル弾きがオクターブで同じ節を弾いていて、エイラも笛で加わる。
# 調べ: 喜び。形: スライド（12/8）2曲のセット。1曲目 AABB×2 → 2曲目 AABB×2 → 1曲目 AABB。
# 拍子・速さ: 12/8・付点4分＝150（1拍＝付点4分、1小節＝4拍。8分は 1/3 拍）。旋法: G イオニア。
# 主役は笛（軽く速い笛）。伴奏の主役: フィドル2本のオクターブ重ね（ケリー地方の弾き方。低いフィドルは笛の1オクターブ下、
#   高いフィドルは笛と同じ高さでごく小さく）。打楽器はボーラン（長・短の付点のゆれ）。竪琴・ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 1曲に2回だけ、強い音（小節の頭の音）をわざと8分1つ遅らせて、ボーランの足拍子とずらす。
# 始まり: フィドルの開放弦のドローン（G と D）→ 終わり: 全員で切る。
# 山: 波（回ごとに大きく・小さくをくり返す）。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 150
S = Song("C100", "061-chimney-smoke", "煙突の煙", "Chimney Smoke", BPM, 4, "G", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("G", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA1 = ["G", "D", "G", "D", "G", "C", "D", "G"]; CB1 = ["G", "D", "G", "C", "G", "D", "D", "G"]
CA2 = ["G", "Em", "G", "D", "G", "G", "D", "G"]; CB2 = ["C", "Em", "C", "G", "C", "Em", "D", "G"]
T1 = CA1 * 2 + CB1 * 2; T2 = CA2 * 2 + CB2 * 2
SC = [("ドローン", 2, "intro", ["G", "G"]), ("1曲目", 32, "verse", T1), ("1曲目2", 32, "chorus", T1), ("2曲目", 32, "verse", T2), ("2曲目2", 32, "chorus", T2),
      ("1曲目3", 32, "chorus", T1), ("切る", 1, "outro", ["G"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ドローン", 0, 0.78), ("1曲目", 0, 0.74), ("1曲目2", 0, 0.86), ("2曲目", 0, 0.76), ("2曲目2", 0, 0.88), ("1曲目3", 0, 0.8), ("1曲目3", 31, 0.96), ("切る", 0, 0.96)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ドローン", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# フィドルの短い音は大きい（044: 0.1 で笛より約8dB 大きい → 0.04 で旋律を一緒に）。ここは伴奏なので、低いフィドル 0.03、高いフィドル 0.012
FL = S.track("フィドル（低い・1オクターブ下）", "strings", patch="violin", volume=0.03, pan=-0.3, reverb=0.3, barGain=G)
FH = S.track("フィドル（高い・笛と同じ高さ）", "strings", patch="violin", volume=0.012, pan=0.3, reverb=0.3, barGain=G)
FD = [S.track(f"フィドル（開放弦のドローン{j + 1}）", "strings", patch="violin", volume=0.03, pan=-0.3 + 0.6 * j, reverb=0.35, barGain=[1.4] * c.NB) for j in range(2)]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]

# ---------- 2曲の旋律（8分＝1、1小節＝12。1=G4） ----------
A1 = ["5:2 3:1 5:2 6:1 5:2 3:1 1:3", "2:2 3:1 4:2 2:1 7,:3 5,:3", "5:2 3:1 5:2 6:1 1':2 7:1 6:3", "5:2 4:1 3:3 2:6",
      "5:2 3:1 5:2 6:1 5:2 3:1 1:3", "2:2 3:1 4:2 5:1 6:3 4:3", "5:2 3:1 2:2 3:1 7,:3 2:3", "1:3 5,:3 1:6"]
B1 = ["1':3 7:2 1':1 2':3 1':3", "7:2 5:1 6:2 7:1 1':3 5:3", "1':3 7:2 1':1 2':2 3':1 2':3", "1':2 7:1 6:3 5:6",
      "1':3 7:2 1':1 2':3 1':3", "7:2 5:1 6:2 7:1 1':2 7:1 6:3", "5:2 3:1 2:2 3:1 7,:3 2:3", "1:3 5,:3 1:6"]
A2 = ["3:2 2:1 1:2 2:1 3:2 5:1 6:3", "5:2 3:1 5:2 1':1 6:3 5:3", "3:2 2:1 1:2 2:1 3:2 5:1 3:3", "2:2 1:1 2:3 5,:6",
      "3:2 2:1 1:2 2:1 3:2 5:1 6:3", "5:2 3:1 5:2 1':1 2':3 1':3", "6:2 5:1 3:2 2:1 1:2 2:1 3:3", "1:3 5,:3 1:6"]
B2 = ["6:2 5:1 6:2 1':1 2':3 1':3", "6:2 5:1 3:3 5:6", "6:2 5:1 6:2 1':1 2':2 3':1 2':3", "1':3 6:3 5:6",
      "6:2 5:1 6:2 1':1 2':3 1':3", "6:2 5:1 3:2 5:1 6:3 1':3", "2':2 1':1 6:2 5:1 3:3 2:3", "1:3 5,:3 1:6"]
LATE = {("1曲目2", 27), ("2曲目2", 10)}                 # 強い音を遅らせる2か所（場面, 小節）
PLAN = [("1曲目", A1 + A1 + B1 + B1, 0.35), ("1曲目2", A1 + A1 + B1 + B1, 0.5), ("2曲目", A2 + A2 + B2 + B2, 0.4), ("2曲目2", A2 + A2 + B2 + B2, 0.5),
        ("1曲目3", A1 + A1 + B1 + B1, 0.55)]
for k, (sc, bars, dens) in enumerate(PLAN):
    s0 = c.s0[sc]; ev = []
    for j, s_ in enumerate(e2b(bars)): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    for (lsc, lb) in LATE:                                   # 小節の頭の音を8分1つ遅らせ、前の音をのばす
        if lsc != sc: continue
        t0 = (s0 + lb) * B
        for q, e in enumerate(ev):
            if abs(e[0] - t0) < 1e-6 and q > 0:
                e[0] = round(t0 + T3, 4); e[1] = round(e[1] - T3, 4); ev[q - 1][1] = round(ev[q - 1][1] + T3, 4)
    play(c.FLUTE, ornament(ev, K, BPM, "jig", B, density=dens, seed=6100 + k))
    play(FL, [(t, L, (m - 12 if m - 12 >= 55 else m), ("!" if abs(t % B) < 1e-6 else ",")) for t, L, m in ev])
    if sc.endswith("2") or sc.endswith("3"):
        play(FH, [(t, L, m, ",") for t, L, m in ev])
s0 = c.s0["切る"]
c.FLUTE.at(s0 * B, "G5:0.5!"); FL.at(s0 * B, "G3:0.5!"); FH.at(s0 * B, "D4:0.5!"); DR[0].at(s0 * B, "C3:0.5!"); DR[1].at(s0 * B, "E3:0.5!")

# ---------- ドローン（フィドルの開放弦 G と D。始まりの2小節） ----------
FD[0].at(0, "G3:8"); FD[1].at(0.05, "D4:7.95,")

# ---------- ボーラン（ケリー式：1拍＝長・短。1・3拍目に強く。B の終わりで詰める） ----------
for b in range(c.s0["1曲目"], c.s0["切る"]):
    n, i, Lb, k = S.scene_of(b); d = DR[b % 2]
    fill = (i % 16 == 15)
    beats = []
    for q in range(4):
        acc = "!" if q in (0, 2) else ""
        if fill and q == 3:
            beats.append(f"C3:{round(T3, 4)}! C3:{round(T3, 4)}! C3:{round(T3, 4)}!")
        else:
            beats.append(f"C3:{round(2 * T3, 4)}{acc} E3:{round(T3, 4)},")
    d.bar(b, " ".join(beats))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.2 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の061（第3版）。第7章のはじまり、対岸の村の煙突の煙と、戸口から聞こえる速い踊りの曲。スライド（12/8・付点4分＝150）2曲のセット、G の長調。フィドルの開放弦のドローンで始まり、2本のフィドルがケリー地方の弾き方でオクターブに重ねて節を弾き、笛が軽く速く加わる。ボーランは長・短の付点のゆれ。曲の中で2回だけ、小節の頭の強い音をわざと8分1つ遅らせて、足拍子とずらす。回ごとに大きく・小さくの波があり、最後は全員で切る。",
       harm_scenes=None, tail_scene="切る", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.0}}}
json.dump(air, open("/tmp/cel/w/air061.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
