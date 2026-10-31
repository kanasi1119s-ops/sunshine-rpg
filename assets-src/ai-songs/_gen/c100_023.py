# ケルト・フルート100曲「銀の笛と百の夜」023 水面の光 Light on the Water — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 水車が回りだした昼。小川の水面に日の光がちらちらと跳ねる。エイラが笛を吹きながら川岸を歩くうちに、
#   日は傾き、光は水面から少しずつ水の中へ、さらに川底の石へと沈んでいく。最後は、川底で揺れる低い光だけが残る。
# 調べ: 喜び。形: リール AABB を3周（あいだに「水の中」の8小節）。装飾音の雨（ロールとカットが多い）。
# 拍子・速さ: 4/4・♩=104。旋法: E ミクソリディア。
# 主役は笛（ロールとカット多め）。伴奏の主役: ブズーキ風の開いた和音のギター（ナイロン弦で、高い所の開放弦の響きをかき鳴らす）と、ボーラン。
#   脇: 1周目だけ、ティン・ホイッスルが笛の上で短い光の粒を足す。竪琴・ピアノ・弦・パッドは使わない。
# この曲だけ: 周ごとに全員の音域が下がり、光が川底へ沈む（ギターの和音は 高→中→低、笛は3周目だけ低い所で吹く B 部、ホイッスルは1周目だけ）。
# 始まり: 高い音のきらめき（ホイッスルと高い和音）→ 終わり: 低い音（ギターの低い E と笛の低い E）。
# 山: 2周目と最後（3周目の後半）。最初が大きく、だんだん小さくなる形にはしない。
import sys, json, re
from c100_common import *
from c100_v2 import *
import c100_v2 as _v2

S = Song("C100", "023-light-on-the-water", "水面の光", "Light on the Water", 104, 4, "E", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("E", "mixolydian", 4)
CA = ["E", "D", "E", "A", "E", "D", "A", "E"]
CB = ["A", "E", "D", "E", "A", "E", "D", "E"]
SC = [("きらめき", 4, "intro", ["E", "D", "A", "E"])]
for r in (1, 2):
    SC.append((f"{r}周目", 32, "chorus" if r == 2 else "verse", CA + CA + CB + CB))
SC += [("水の中", 8, "verse", ["A", "E", "D", "E"] * 2), ("3周目", 32, "chorus", CA + CA + CB + CB), ("川底", 4, "outro", ["E", "D", "E", "E"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("きらめき", 0, 0.68), ("1周目", 0, 0.74), ("1周目", 31, 0.78), ("2周目", 0, 0.84), ("2周目", 31, 0.9), ("水の中", 0, 0.7),
          ("3周目", 0, 0.76), ("3周目", 16, 0.84), ("3周目", 31, 0.92), ("川底", 0, 0.82), ("川底", 3, 0.72)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="きらめき", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: ギターの和音（3音）は笛より約5dB 大きい → 0.045→0.022（5音になるので少し多めに下げる）。ホイッスルの粒も笛より大きい → 0.025。ボーランは笛と同じくらい
GU = [S.track(f"ブズーキ風ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.022, pan=0.28 + 0.05 * i, reverb=0.3, barGain=G) for i in range(5)]
WH = S.track("ティン・ホイッスル（光の粒）", "panflute", patch="tinWhistle", volume=0.025, pan=-0.35, reverb=0.5, barGain=G)
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.1 + 0.08 * j, reverb=0.3, barGain=G) for j in range(2)]

# ---------- リール（E ミクソリディア。1=E4） ----------
A = ["5:0.5 3:0.5 1:0.5 3:0.5 5:1 6:0.5 5:0.5", "4:0.5 2:0.5 7,:0.5 2:0.5 4:1 5:0.5 4:0.5",
     "3:0.5 4:0.5 5:0.5 6:0.5 7:0.5 6:0.5 5:0.5 3:0.5", "2:0.5 3:0.5 4:0.5 2:0.5 1:1 R:0.5 6,:0.5",
     "5:0.5 3:0.5 1:0.5 3:0.5 5:1 6:0.5 5:0.5", "6:0.5 4:0.5 2:0.5 4:0.5 6:1 7:0.5 1':0.5",
     "2':0.5 1':0.5 7:0.5 5:0.5 6:0.5 4:0.5 3:0.5 2:0.5", "1:1 3:0.5 2:0.5 1:1 R:1"]
Bh = ["1':1 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5 5:0.5", "6:1 5:0.5 6:0.5 7:0.5 6:0.5 5:0.5 3:0.5",
      "4:0.5 5:0.5 6:0.5 4:0.5 5:0.5 6:0.5 7:0.5 5:0.5", "1':1 5:0.5 3:0.5 5:1 R:1",
      "1':1 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5 5:0.5", "6:1 5:0.5 6:0.5 7:0.5 6:0.5 5:0.5 3:0.5",
      "4:0.5 6:0.5 5:0.5 3:0.5 2:0.5 4:0.5 3:0.5 1:0.5", "7,:0.5 2:0.5 6,:0.5 7,:0.5 1:1 R:1"]
Bl = ["1:1 7,:0.5 1:0.5 2:0.5 1:0.5 7,:0.5 6,:0.5", "6,:1 7,:0.5 6,:0.5 7,:0.5 1:0.5 2:0.5 3:0.5",            # 3周目の B：低い所で（川底）
      "4:0.5 3:0.5 2:0.5 4:0.5 3:0.5 2:0.5 1:0.5 7,:0.5", "1:1 6,:0.5 7,:0.5 1:1 R:1",
      "1:1 7,:0.5 1:0.5 2:0.5 1:0.5 7,:0.5 6,:0.5", "6,:1 7,:0.5 6,:0.5 7,:0.5 1:0.5 2:0.5 3:0.5",
      "4:0.5 6:0.5 5:0.5 3:0.5 2:0.5 4:0.5 3:0.5 1:0.5", "7,:0.5 2:0.5 6,:0.5 7,:0.5 1:2"]
SPK = ["R:2 5':0.25 6':0.25 5':0.5 R:1", "R:1 3':0.25 4':0.25 3':0.5 R:2", "R:3 2':0.25 3':0.25 2':0.5", "R:0.5 1':0.25 2':0.25 1':0.5 R:2.5"]
play_melody(c, "きらめき", SPK, 4, "reel", key=K, density=0.0, seed=2300)
nb = play_melody(c, "1周目", A + A + Bh + Bh, 4, "reel", key=K, density=0.55, seed=2301)
for st, L, m, mk in nb:                                       # 1周目：ホイッスルが1オクターブ上で、ところどころ光の粒を
    if L <= 0.6 and int(st * 4) % 7 == 0: WH.at(round(st + 0.01, 3), f"{nm(m + 12 if m + 12 <= 93 else m)}:{round(min(L, 0.4), 3)}")
play_melody(c, "2周目", A + A + Bh + Bh, 4, "reel", key=K, density=0.65, seed=2302)
WATER = ["5:2 3:2", "4:2 2:2", "3:1 4:1 5:2", "1:4", "6,:2 1:2", "2:2 7,:2", "1:1 2:1 3:2", "1:4"]       # 水の中：長い音でゆらぐ
play_melody(c, "水の中", WATER, 4, "air", key=K, density=0.3, seed=2303)
play_melody(c, "3周目", A + A + Bl + Bl, 4, "reel", key=K, density=0.55, seed=2304)
play_melody(c, "川底", ["5:1 3:1 2:1 7,:1", "1:4", "1:4", "R:4"], 4, "air", key=K, density=0.1, seed=2305)
# きらめき：ホイッスルの粒
s0 = c.s0["きらめき"]
for j, s_ in enumerate(["R:1 5':0.25 6':0.25 5':0.5 R:2", "R:2.5 3':0.25 4':0.25 3':1", "R:0.5 6':0.25 5':0.25 6':0.5 R:2.5", "R:3 5':0.5 R:0.5"]):
    for t, L, m in mel_events(K, s_, 5, (s0 + j) * B):
        if m <= 93: WH.at(round(t, 3), f"{nm(m)}:{L}")

# ---------- ブズーキ風ギター（周ごとに和音の高さが下がる） ----------
REEL = [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 0.5, "d", ","), (3.5, 0.5, "u", ",")]
RANGE = {"きらめき": (64, 88), "1周目": (59, 83), "2周目": (52, 76), "水の中": (47, 71), "3周目": (40, 66), "川底": (40, 64)}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    lo, hi = RANGE[n]
    v = _v2.open_chord(ch, lo, hi)
    trs = GU[:len(v)]
    if n == "きらめき":
        for q, x in enumerate(v[-3:]): GU[q].at(round(b * B + 0.08 * q, 3), f"{nm(x)}:4,")
        continue
    if n == "水の中":
        for q, x in enumerate(v[:4]): GU[q].at(round(b * B + 0.12 * q, 3), f"{nm(x)}:4,")      # 水の中：ゆっくり1回だけ鳴らす
        continue
    if n == "川底":
        if i == 0:
            for q, x in enumerate(v[:3]): GU[q].at(round(b * B + 0.1 * q, 3), f"{nm(x)}:4,")
        elif i == 1: GU[0].at(b * B, "E2:8")                              # 最後は低い E
        continue
    for pos, L, d, mk in REEL:
        order = list(range(len(v))) if d == "d" else list(reversed(range(len(v))))
        for j, q in enumerate(order):
            if q < len(GU): GU[q].at(round(b * B + pos + 0.018 * j, 4), f"{nm(v[q])}:{L}{mk}")

# ---------- ボーラン（2周目から。3周目の後半はいちばん密に） ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); tr = DR[b % 2]
    if n in ("2周目", "3周目"):
        bodhran(tr, b, B, "reel", var=(i % 8 == 7 or (n == "3周目" and i >= 16 and i % 2)), soft=(n == "3周目" and i < 16))
    elif n == "1周目" and i >= 16:
        tr.bar(b, "C3:1! R:1 C3:1, R:1")
    elif n == "川底" and i == 0:
        tr.bar(b, "C3:1! R:3")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の023（第3版）。水車が回りだした昼、小川の水面に光が跳ねる。リール（4/4・♩=104）AABB を3周、E ミクソリディア。笛はロールとカットの多い装飾音の雨。伴奏はブズーキ風の開いた和音のギターとボーラン。周ごとに全員の音域が下がり、光が水面から水の中、川底の石へと沈んでいく。始まりは高いきらめき、終わりは低い E。",
       harm_scenes=None, tail_scene="川底", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.5, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.4}}}
json.dump(air, open("/tmp/cel/w/air023.json", "w"), ensure_ascii=False)
