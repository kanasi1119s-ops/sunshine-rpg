# ケルト・フルート100曲「銀の笛と百の夜」045 石段の読み聞かせ The Reading on the Tower Stair — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 鐘守は、塔の石段に腰かけて、祖父が若いころに書き残した日記を読んでくれる。昔のお屋敷で、祖父が領主の娘のために
#   一曲を捧げた日のこと。エイラは笛で、その献呈の曲（プランクスティ）を吹く。最後に鐘守が日記をぱたんと閉じる。
# 調べ: 喜び。形: 宮廷的な2部形式（献呈曲プランクスティ。A 16小節・B 16小節を、それぞれくり返して2周）。
# 拍子・速さ: 3/4・♩=88。旋法: D イオニア。
# 主役は笛（歌う笛・分散和音で跳ぶ）。伴奏の主役: チェンバロ（左手が4分で歩く低音、右手が8分の分散和音。バロック風に和声が進む）。
#   竪琴・ギター・ピアノ・弦・パッド・打楽器・2本目の笛は使わない（036 のチェンバロの「迷う歩み」とは、和声の進み方と右手の8分がちがう）。
# この曲だけ: バロック風の進む和声（5度ずつ巡る）と、跳ねる分散和音の旋律（オカロラン型）。
# 始まり: チェンバロの和音 → 終わり: 本を閉じる和音（ぱたん、と1回）。
# 山: 2つ（1周目と2周目の B）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "045-the-reading-on-the-tower-stair", "石段の読み聞かせ", "The Reading on the Tower Stair", 88, 3, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("D", "major", 4)
CA = ["D", "A", "Bm", "F#m", "G", "D", "Em", "A", "D", "Bm", "G", "A", "D", "G", "A", "D"]
CB = ["Bm", "F#m", "G", "D", "Em", "Bm", "A", "A", "D", "G", "Em", "A", "Bm", "G", "A", "D"]
SC = [("和音", 1, "intro", ["D"])]
for r in (1, 2):
    SC += [(f"{r}周目A", 32, "verse", CA * 2), (f"{r}周目B", 32, "chorus", CB * 2)]
SC.append(("本を閉じる", 2, "outro", ["D", "D"]))
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("和音", 0, 0.7), ("1周目A", 0, 0.72), ("1周目B", 0, 0.8), ("1周目B", 24, 0.86), ("2周目A", 0, 0.74), ("2周目B", 0, 0.84), ("2周目B", 28, 0.9),
          ("本を閉じる", 0, 0.82)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="和音", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 左手（0.14）・右手（0.08）とも笛より 3〜5dB 小さい（丁度よい）
HL = S.track("チェンバロ（左手の歩く低音）", "harpsichord", volume=0.14, pan=-0.2, reverb=0.35, barGain=G)
HR = S.track("チェンバロ（右手の分散和音）", "harpsichord", volume=0.08, pan=0.18, reverb=0.35, barGain=G)
HC = [S.track(f"チェンバロ（和音{j + 1}）", "harpsichord", volume=0.07, pan=-0.1 + 0.1 * j, reverb=0.4, barGain=G) for j in range(3)]

# ---------- 旋律（D イオニア。1=D4。分散和音で跳ぶ） ----------
A = ["1:1 3:0.5 5:0.5 1':1", "7:1 5:0.5 2':0.5 7:1", "6:1 1':0.5 6:0.5 3:1", "3:1.5 4:0.5 5:1", "4:1 6:0.5 4:0.5 2:1", "1:1 3:0.5 5:0.5 1':1",
     "2':1 7:0.5 5:0.5 4:1", "3:2 2:1", "1:1 5:0.5 3:0.5 1':1", "6:1 4:0.5 2:0.5 6:1", "5:0.5 4:0.5 3:0.5 2:0.5 1:1", "7,:1 2:1 5:1",
     "1':1.5 7:0.5 6:1", "4:1 6:1 2':1", "7:1 5:1 2:1", "1:3"]
Bm = ["6:1 1':0.5 3':0.5 1':1", "5:1 7:0.5 2':0.5 7:1", "4:1 6:0.5 1':0.5 6:1", "5:2 1':1", "2':1 7:0.5 5:0.5 2:1", "6:1 5:0.5 4:0.5 3:1",
      "2:1 4:0.5 6:0.5 5:1", "5:3", "1':1 5:0.5 3:0.5 1:1", "4:1 6:0.5 1':0.5 4:1", "2:1 4:0.5 6:0.5 2':1", "5:1.5 6:0.5 7:1",
      "6:1 1':0.5 6:0.5 3:1", "4:1 6:1 1':1", "7:1 2':1 5:1", "1':3"]
for r in (1, 2):
    play_melody(c, f"{r}周目A", A + A, 4, "air", key=K, density=0.25 + 0.1 * r, seed=4500 + r)
    play_melody(c, f"{r}周目B", Bm + Bm, 4, "air", key=K, density=0.3 + 0.1 * r, seed=4510 + r)
s0 = c.s0["本を閉じる"]
c.FLUTE.at(s0 * B, "D5:3")

# ---------- チェンバロ ----------
ROOT = {"D": 38, "A": 45, "Bm": 47, "F#m": 42, "G": 43, "Em": 40}
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return sorted(54 + (p - 54) % 12 for p in (r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12))
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    tn = tri(ch)
    if n == "和音":
        for j, x in enumerate(tn): HC[j].at(round(b * B + 0.04 * j, 3), f"{nm(x)}:3")
        HL.at(b * B, f"{nm(r)}:3"); continue
    if n == "本を閉じる":                                              # 本を閉じる和音（ぱたん）
        if i == 0:
            for j, x in enumerate(tn): HC[j].at(b * B, f"{nm(x)}:3!")
            HL.at(b * B, f"{nm(r)}:3!")
        continue
    nxt = ROOT.get(S.chords[b + 1], r) if b + 1 < c.NB else r
    step = 1 if nxt > r else -1
    HL.bar(b, f"{nm(r)}:1 {nm(r + 7 if r + 7 <= 52 else r - 5)}:1, {nm(nxt - step * (1 if abs(nxt - r) > 2 else 0) if nxt != r else r + 12)}:1,")
    HR.bar(b, " ".join(f"{nm(tn[q])}:0.5{',' if q2 % 2 else ''}" for q2, q in enumerate((0, 1, 2, 1, 2, 1))))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の045（第3版）。塔の石段で、鐘守が若い祖父の日記を読み聞かせる。昔のお屋敷で捧げられた献呈の曲（プランクスティ）、宮廷的な2部形式。3/4・♩=88、D イオニア。笛は分散和音で跳ねて歌い、チェンバロは左手が4分で歩き、右手が8分の分散和音で、バロック風に和声が5度ずつ巡る。山は2回の B、最後は日記を閉じる和音。",
       harm_scenes=None, tail_scene="本を閉じる", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.22, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air045.json", "w"), ensure_ascii=False)
