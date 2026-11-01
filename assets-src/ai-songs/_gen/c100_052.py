# ケルト・フルート100曲「銀の笛と百の夜」052 舟を押す Pushing Off — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 湖のほとりに、古い小舟がつないである。エイラは浅瀬に入り、「せーの」で舟を押す。三度目で舟が水に乗る。
#   漕ぎ出して岸を離れる瞬間、景色がひらける（調が一音上がる）。最後は櫂を3回強くかいて、舟がすべりだす。
# 調べ: 喜び。形: スリップ・ジグ（9/8）2曲のセット。1曲目（D）AABB×2 → 岸を離れる2小節 → 2曲目（E）AABB×2 → 最後の A。
# 拍子・速さ: 9/8・付点4分＝100（1拍＝付点4分、1小節＝3拍。8分は 1/3 拍）。旋法: D イオニア → E イオニア。
# 主役は笛（漕ぐ笛）。伴奏: ボーラン（枠太鼓）・ナイロン弦ギターのストローク・コントラバスのピチカート（打つ伴奏だけ）。
#   竪琴・ピアノ・パッド・ほかの弦・2本目の笛は使わない。
# この曲だけ: 全員の「せーの」の3回の打ちで始まり、岸を離れる瞬間に調が一音上がる（D → E）。終わりは櫂の3回の打ち（始まりと鏡）。
# 041（立つ石）もスリップ・ジグだが、あちらは1曲を遅い → 速いへ。こちらは速さが一定で、2曲のセットと転調。
# 山: 1曲目の2周目と、最後の A。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 100
S = Song("C100", "052-pushing-off", "舟を押す", "Pushing Off", BPM, 3, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K1, K2 = Key("D", "major", 4), Key("E", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA1 = ["D", "G", "D", "A", "D", "G", "A", "D"]; CB1 = ["D", "Em", "D", "A", "D", "G", "A", "D"]
CA2 = ["E", "A", "E", "B", "E", "A", "B", "E"]; CB2 = ["E", "A", "F#m", "B", "E", "A", "B", "E"]
T1 = CA1 * 2 + CB1 * 2; T2 = CA2 * 2 + CB2 * 2
SC = [("押す", 3, "intro", ["D"] * 3), ("1曲目", 32, "verse", T1), ("1曲目2", 32, "chorus", T1), ("岸を離れる", 2, "verse", ["D", "B"]),
      ("2曲目", 32, "verse", T2), ("2曲目2", 32, "verse", T2), ("最後のA", 16, "chorus", CA2 * 2), ("櫂", 3, "outro", ["E"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("押す", 0, 0.8), ("1曲目", 0, 0.74), ("1曲目2", 0, 0.84), ("1曲目2", 31, 0.9), ("岸を離れる", 0, 0.76), ("2曲目", 0, 0.78), ("2曲目2", 0, 0.82),
          ("最後のA", 0, 0.9), ("最後のA", 15, 0.96), ("櫂", 0, 0.94)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="押す", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.1 + 0.2 * j, reverb=0.3, barGain=G) for j in range(2)]
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=-0.3 - 0.05 * i, reverb=0.3, barGain=G) for i in range(5)]
BS = S.track("コントラバス（ピチカート）", "strings", patch="pizzicato", volume=0.12, gainDb=5, pan=-0.05, reverb=0.3, barGain=G)

# ---------- 2曲の旋律（8分＝1、1小節＝9） ----------
A1 = ["3:2 1:1 3:2 5:1 6:2 5:1", "4:2 2:1 4:2 6:1 5:2 4:1", "3:2 1:1 3:2 5:1 1':2 7:1", "6:2 5:1 4:2 2:1 7,:3",
      "3:2 1:1 3:2 5:1 6:2 5:1", "4:2 6:1 1':2 6:1 5:2 4:1", "3:2 5:1 4:2 2:1 7,:2 2:1", "1:3 3:3 1:3"]
B1 = ["5:2 1':1 3':2 1':1 5:2 1':1", "6:2 2':1 4':2 2':1 6:2 2':1", "5:2 1':1 3':2 2':1 1':2 7:1", "6:2 7:1 1':2 6:1 5:3",
      "5:2 1':1 3':2 1':1 5:2 1':1", "4:2 6:1 2':2 1':1 7:2 6:1", "5:2 3:1 4:2 2:1 7,:2 2:1", "1:3 5,:3 1:3"]
A2 = ["5:1 4:1 3:1 2:2 3:1 5:2 3:1", "6:2 5:1 4:2 3:1 2:3", "5:1 4:1 3:1 2:2 3:1 5:2 1':1", "7:2 5:1 6:2 4:1 5:3",
      "5:1 4:1 3:1 2:2 3:1 5:2 3:1", "6:2 1':1 2':2 1':1 6:3", "5:2 3:1 2:2 3:1 7,:2 2:1", "1:6 5,:3"]
B2 = ["1':3 7:2 6:1 5:3", "6:2 5:1 4:2 6:1 1':3", "2':3 1':2 7:1 6:3", "5:2 6:1 7:2 5:1 2':3",
      "3':3 2':2 1':1 7:3", "6:2 7:1 1':2 6:1 4:3", "5:2 3:1 4:2 2:1 7,:2 2:1", "1:9"]
play_melody(c, "押す", e2b(["R:9", "R:9", "R:7 1:1 2:1"]), 4, "march", key=K1, density=0.0)          # 三度目で舟が浮く：笛の弱起
play_melody(c, "1曲目", e2b(A1 + A1 + B1 + B1), 4, "march", key=K1, density=0.35, seed=5201)
play_melody(c, "1曲目2", e2b(A1 + A1 + B1 + B1), 4, "march", key=K1, density=0.55, seed=5202)
play_melody(c, "岸を離れる", e2b(["1:9", "R:3 7,:3 1:1 2:1 R:1"]), 4, "march", key=K1, density=0.0)    # D を長く → E への弱起（C♯・D♯…）
play_melody(c, "2曲目", e2b(A2 + A2 + B2 + B2), 4, "march", key=K2, density=0.4, seed=5203)
play_melody(c, "2曲目2", e2b(A2 + A2 + B2 + B2), 4, "march", key=K2, density=0.5, seed=5204)
play_melody(c, "最後のA", e2b(A2 + A2), 4, "march", key=K2, density=0.6, seed=5205)
s0 = c.s0["櫂"]
c.FLUTE.at(s0 * B, "E5:1!"); c.FLUTE.at((s0 + 1) * B, "B5:1!"); c.FLUTE.at((s0 + 2) * B, "E6:2!")

# ---------- 全員の打ち（押す・櫂） ----------
def hit(b, ch, big=True):
    DR[0].at(b * B, "C3:1!"); DR[1].at(round(b * B + 0.01, 3), "E3:0.5!")
    strum(GT, b, B, ch, [(0, 2, "d", "!")])
    BS.at(b * B, f"{nm(38 + (PC[ch[0]] - 2) % 12)}:1!")
for b in range(3): hit(b, "D")
for k in range(3): hit(c.s0["櫂"] + k, "E")

# ---------- ボーラン・ギター・コントラバス（場面ごとに変える） ----------
R = lambda x: round(x * T3, 4)
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; d = DR[b % 2]
    if n in ("押す", "櫂"): continue
    root = 38 + (PC[re.match(r"^([A-G][#b]?)", ch).group(1)] - 2) % 12
    fifth = root + 7 if root + 7 <= 50 else root - 5
    part_b = (i % 32) >= 16                               # B の部分
    if n == "岸を離れる":                                  # 打ちをやめ、ボーランの小刻み（舟が水に乗る）→ E へ
        d.bar(b, " ".join(f"{'C3' if q % 3 == 0 else 'E3'}:{R(1)}{'!' if q == 0 else ','}" for q in range(9)))
        strum(GT, b, B, ch, [(0, 3, "d", ",")])
        BS.at(b * B, f"{nm(root)}:1,")
        continue
    # ボーラン
    if n == "1曲目" and i < 8:
        d.bar(b, f"C3:1! E3:1, C3:1,")                                     # 最初の A：拍だけ（軽く）
    elif n in ("1曲目2", "最後のA") or (n == "2曲目2" and part_b):
        fill = (i % 8 == 7)
        pat = [("C3", "!"), ("E3", ","), ("E3", ","), ("C3", ""), ("E3", ","), ("C3", ","), ("C3", "!"), ("E3", ","), ("E3", ",")] if not fill else \
              [("C3", "!"), ("E3", ","), ("C3", ","), ("C3", "!"), ("E3", ","), ("E3", ","), ("C3", "!"), ("C3", "!"), ("C3", "!")]
        d.bar(b, " ".join(f"{x}:{R(1)}{mk}" for x, mk in pat))
    else:
        d.bar(b, f"C3:{R(2)}! E3:{R(1)}, C3:{R(2)} E3:{R(1)}, C3:{R(2)} E3:{R(1)},")
    # ギター（1曲目の最初の A は休み。B は長いストローク、A は1拍ごと）
    if not (n == "1曲目" and i < 8):
        if n == "1曲目" and i < 16:
            pat = [(0, 3, "d", ",")]
        elif part_b:
            pat = [(0, 1.5, "d", "!"), (1.5, 0.5, "u", ","), (2, 1, "d", "")]
        else:
            pat = [(0, R(2), "d", "!"), (R(2), R(1), "u", ","), (1, R(2), "d", ""), (1 + R(2), R(1), "u", ","), (2, R(2), "d", ""), (2 + R(2), R(1), "u", ",")]
        strum(GT, b, B, ch, pat)
    # コントラバス（根音と5度。山では8分で歩く）
    if n in ("1曲目2", "最後のA") and not part_b:
        BS.bar(b, f"{nm(root)}:{R(2)}! {nm(root)}:{R(1)}, {nm(fifth)}:{R(2)} {nm(root + 12 if root + 12 <= 52 else root)}:{R(1)}, {nm(fifth)}:{R(2)} {nm(root)}:{R(1)},")
    else:
        BS.bar(b, f"{nm(root)}:1! R:1 {nm(fifth)}:1,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の052（第3版）。湖のほとりで、古い小舟を押して漕ぎ出す。スリップ・ジグ（9/8・付点4分＝100）2曲のセット。全員の「せーの」の3回の打ち（ボーラン・ギター・コントラバス）で舟を押し、三度目で舟が浮いて笛が走りだす。1曲目は D、岸を離れる2小節で調が一音上がり、2曲目は E。最後は櫂の3回の打ちで止まる（始まりと鏡）。伴奏は打つ楽器だけ（ボーラン・ギターのストローク・コントラバスのピチカート）。",
       harm_scenes=None, tail_scene="櫂", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.2}}}
json.dump(air, open("/tmp/cel/w/air052.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
