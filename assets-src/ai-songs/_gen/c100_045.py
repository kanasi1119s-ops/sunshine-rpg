# ケルト・フルート100曲「銀の笛と百の夜」045 石段の読み聞かせ Reading on the Steps（2026-10-29）
# イメージ: 塔の石段に腰かけて、祖父の記録を声に出して読む。一文読んでは、ひと息。ページをめくる。
#   ところどころ、胸が熱くなる一節があって、声が少し高くなる（小さな山が2つ）。最後に本をそっと閉じる。
# 形: 語り口の旋律。3小節の「一文」と、1小節の「ひと息（間）」をくり返す。間はピアノの和音が受けとめる。6/8・付点4分＝44。C リディア。小さな山2つ。
# ただひとつ: 句の終わりの「間」で笛は休むが、ピアノが両手の和音で受けとめ、竪琴がページをめくるように上る（音は落ちない）。
# 編曲の表:
#   本を開く : ピアノの大きな和音（両手）、チェロ、うすい弦
#   読む1    : 笛の一文＋ピアノの左手（根音と5度）・右手（和音）＋チェロ
#   読む2    : ＋竪琴・弦3声
#   胸が熱く1: 笛が高い所でつながる。弦の全和音・内声
#   読む3    : 読む1の落ちつき
#   胸が熱く2: いちばん高い所。笛の和声
#   本を閉じる: ピアノの和音で閉じる
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 132   # 8分音符＝132（付点4分＝44）
S = Song("C100", "045-reading-on-the-steps", "石段の読み聞かせ", "Reading on the Steps", BPM, 6, "C", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
U = [["C", "D", "Em", "C"], ["Am", "D", "G", "G"], ["C", "D", "Em", "Am"], ["Em", "D", "C", "G"], ["Am", "Bm", "Em", "Em"], ["G", "D", "C", "C"]]
HOT = ["F", "G", "C", "Am", "F", "D", "G", "C"]
S.scene("本を開く", 3, "intro", ["C", "D", "C"])
S.scene("読む1", 24, "verse", sum(U, []))
S.scene("読む2", 24, "verse", sum(U[3:] + U[:3], []))
S.scene("胸が熱く1", 8, "chorus", HOT)
S.scene("読む3", 16, "verse", sum(U[:4], []))
S.scene("胸が熱く2", 8, "chorus", HOT)
S.scene("本を閉じる", 6, "outro", ["F", "G", "C", "D", "C", "C"])
NAMES = ["本を開く", "読む1", "読む2", "胸が熱く1", "読む3", "胸が熱く2", "本を閉じる"]

c = make(S, NAMES,
         [("本を開く", 0, 0.66), ("読む1", 0, 0.64), ("読む2", 0, 0.68), ("胸が熱く1", 0, 0.78), ("胸が熱く1", 5, 0.85), ("読む3", 0, 0.68),
          ("胸が熱く2", 0, 0.82), ("胸が熱く2", 5, 0.92), ("本を閉じる", 0, 0.7), ("本を閉じる", 5, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="本を開く", passing=True, tension=False)
PL = S.track("ピアノ（左手）", "piano", volume=0.45, pan=-0.18, reverb=0.45, barGain=c.g())
PR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=[0.4, 0.34, 0.3][i], pan=[-0.12, -0.08, -0.04][i], reverb=0.45, barGain=c.g()) for i in range(3)]
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.15, reverb=0.45, barGain=c.g())

P = [["5:3 6:2 5:1", "4:3 3:3", "2:6"], ["3:2 4:1 5:3", "4:3 5:3", "6:6"], ["1':3 7:2 6:1", "5:3 4:3", "3:6"],
     ["2:2 3:1 4:3", "5:3 6:3", "5:6"], ["6:3 7:2 1':1", "2':3 1':3", "7:6"], ["5:2 4:1 3:3", "2:3 7,:3", "1:6"]]
def read(order): return sum([P[k] + ["R:6"] for k in order], [])
HOTM = ["1':3 2':3", "3':6", "2':2 1':1 7:3", "1':6", "6:3 7:3", "1':3 2':3", "7:3 5:3", "5:6"]
play_melody(c, "読む1", read(range(6)), 4, "air", density=0.5, seed=4501)
play_melody(c, "読む2", read([3, 4, 5, 0, 1, 2]), 4, "air", density=0.7, seed=4502)
play_melody(c, "胸が熱く1", HOTM, 4, "air", density=0.8, seed=4503)
play_melody(c, "読む3", read([0, 1, 2, 5]), 4, "air", density=0.6, seed=4504)
play_melody(c, "胸が熱く2", ["1':3 2':3", "3':3 4':3", "3':2 2':1 1':3", "2':6", "1':3 7:3", "6:3 7:3", "1':3 2':3", "1':6"], 4, "air", density=0.9, seed=4505)
play_melody(c, "本を閉じる", ["5:3 4:3", "3:3 2:3", "1:6", "R:6", "R:6", "R:6"], 4, "air", density=0.3, seed=4506)

B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    hi = [x for x in range(60, 77) if x % 12 in chord_pcs(ch)]
    t = tones(ch, "C3", "C6")
    rest = n in ("読む1", "読む2", "読む3") and i % 4 == 3          # 一文のあとの「間」
    big = n in ("本を開く", "本を閉じる") or rest
    if n == "本を閉じる" and i >= 4:
        if i == 4:
            PL.at(b * B, f"{nm(r)}:6"); [PR[j].at(b * B + 0.08 * j, f"{nm(hi[j % len(hi)])}:6") for j in range(3)]
        continue
    if big:   # ピアノが両手の大きな和音（少しずつずらして弾く）で受けとめる
        PL.at(b * B, f"{nm(r)}:6"); PL.at(b * B + 0.05, f"{nm(r + 7)}:6")
        for j in range(3): PR[j].at(b * B + 0.12 + 0.08 * j, f"{nm(hi[j % len(hi)])}:6")
        if rest: c.HARP2.bar(b, "R:3 " + " ".join(f"{nm(x)}:0.5" for x in t[4:10]))   # ページをめくる
    else:     # 語りの下：左手は根音と5度、右手は和音を2回
        PL.at(b * B, f"{nm(r)}:3"); PL.at(b * B + 3, f"{nm(r + 7)}:3")
        PR[0].at(b * B + 1, f"{nm(hi[0])}:2"); PR[1].at(b * B + 1, f"{nm(hi[1])}:2")
        PR[0].at(b * B + 4, f"{nm(hi[0])}:2"); PR[1].at(b * B + 4, f"{nm(hi[2 % len(hi)])}:2")
    CELLO.bar(b, f"{nm(r)}:6")
    nv = 2 if n in ("本を開く", "読む1") else 3
    v = voice(ch, 55 if "胸" not in n else 59, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n in ("読む2", "胸が熱く1", "胸が熱く2") and not rest:
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[5 % len(t)], t[4 % len(t)], t[2])))
rich(c, choir_scenes=["胸が熱く2"], pulse_scenes=["胸が熱く1", "胸が熱く2"], guitar=False, pizz=False, inner=True, choir_vol=0.11)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.33 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の045。塔の石段で、祖父の記録を声に出して読む。6/8・付点4分＝44、C リディア。3小節の一文と1小節のひと息をくり返し、ひと息はピアノの両手の和音と、ページをめくるような竪琴が受けとめる。胸が熱くなる一節で2つの小さな山。最後はピアノの和音で本を閉じる。",
       harm_scenes=None, tail_scene="本を閉じる", fill=False, pads=True, pad_scenes=["読む1", "読む2", "胸が熱く1", "読む3", "胸が熱く2"], floor=True)
air = {"pre": 0.6, "tail": 7.0, "layers": [{"file": "0595", "db": -37, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -28, "rt": 7.0}, "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5}}, "intro_db": 5.0}
json.dump(air, open("/tmp/cel/w/air045.json", "w"), ensure_ascii=False)
