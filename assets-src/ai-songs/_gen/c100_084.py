# ケルト・フルート100曲「銀の笛と百の夜」084 孤独の稜線 The Lonely Ridge — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 北の峰へ続く細い稜線を、エイラはひとりで歩く。左も右も深い谷。遠くの谷底から、誰かが吹くバグパイプの持続音が
#   かすかに聞こえる気がする。エイラは古いスコットランドふうのゆっくりした歌を、ひとりで吹く。
# 調べ: 悲しみ。形: スロー・エア（A・B 各8小節。A B → A B' → A と半分。前半の B が山）。
# 拍子・速さ: 4/4・♩=48。旋法: B ドリア（G♯ がやわらかい）。
# 主役は笛（鋭くない短‐長の笛。E4〜B5）。伴奏の主役: 遠いバグパイプふうのドローン（B と F♯。004 と同じく、録音のバグパイプは
#   すぐ消えるので、遠いチェロとビオラの長い音で、2小節ごとに交互に弓を返す）。竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 遅いテンポのまま、スコッチ・スナップ（短‐長。8分3連の1つ分と2つ分）が、句の頭ごとに残る。鋭くせず、やわらかく。
# 始まり: ドローン → 終わり: ドローンだけ。
# 山: 前半（1回目の B）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "084-the-lonely-ridge", "孤独の稜線", "The Lonely Ridge", 48, 4, "B", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("B", "dorian", 4)
SC = [("ドローン", 3, "intro", ["Bm"] * 3), ("歌1", 16, "chorus", ["Bm"] * 16), ("歌2", 16, "verse", ["Bm"] * 16), ("歌3", 12, "verse", ["Bm"] * 12),
      ("ドローンだけ", 3, "outro", ["Bm"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ドローン", 0, 0.7), ("歌1", 0, 0.72), ("歌1", 12, 0.88), ("歌2", 0, 0.74), ("歌2", 15, 0.7), ("歌3", 0, 0.68), ("ドローンだけ", 0, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ドローン", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 遠いドローン（004: チェロ 0.02・gainDb 2、ビオラ 0.017 で笛の約5dB 下）。ドローンだけの所は始まり用のコントラバスとチェロ（047）
DV = [S.track(f"遠いドローン（{x}）", "strings", patch=p, volume=v, gainDb=gd, pan=pn, reverb=0.88, release=0.8, barGain=[round(y * 1.4, 3) for y in G])
      for x, p, v, gd, pn in (("チェロ B2", "cello", 0.02, 2, -0.3), ("ビオラ F♯3", "viola", 0.017, 0, 0.3), ("チェロ B2・弓返し", "cello", 0.02, 2, -0.3),
                              ("ビオラ F♯3・弓返し", "viola", 0.017, 0, 0.3))]
DI = [S.track("ドローン（始まりと終わりのコントラバス）", "strings", patch="contrabass", volume=0.07, gainDb=8, pan=-0.1, reverb=0.85, release=1.2),
      S.track("ドローン（始まりと終わりのチェロ）", "strings", patch="cello", volume=0.03, gainDb=8, pan=0.15, reverb=0.85, release=1.2)]

# ---------- スロー・エア（1=B4。句の頭にやわらかいスナップ：0.33 と 0.67） ----------
A = ["5,:0.33 1:0.67 1:1 2:1 3:1", "4:2 3:1 2:1", "1:0.33 3:0.67 3:1 5:2", "4:4",
     "3:0.33 5:0.67 5:1 6:1 5:1", "4:1 3:1 2:2", "1:0.33 2:0.67 3:1 2:1 7,:1", "1:4"]
Bm = ["5:0.33 1':0.67 1':2 7:1", "6:2 5:2", "6:0.33 1':0.67 7:1 6:1 5:1", "4:4",
      "3:0.33 5:0.67 6:2 5:1", "4:1 3:1 2:1 1:1", "2:0.33 3:0.67 2:1 7,:1 5,:1", "1:4"]
B2 = Bm[:4] + ["3:0.33 4:0.67 5:2 4:1", "3:1 2:1 1:2", "2:0.33 1:0.67 7,:2 5,:1", "1:4"]          # 2回目の B は低くしずかに
play_melody(c, "歌1", A + Bm, 4, "air", key=K, density=0.2, seed=8401)
play_melody(c, "歌2", A + B2, 4, "air", key=K, density=0.15, seed=8402)
play_melody(c, "歌3", A + ["3:0.33 5:0.67 6:2 5:1", "4:1 3:1 2:2", "1:0.33 2:0.67 7,:2 5,:1", "1:4"], 4, "air", key=K, density=0.1, seed=8403)

# ---------- 遠いドローン（2小節ごとに、2組が交互に弓を返す） ----------
DI[0].at(0, "B1:12.6"); DI[1].at(0.05, "F#2:12.5,")
k = 0
for b in range(3, c.s0["ドローンだけ"], 2):
    L = min(8.3, (c.s0["ドローンだけ"] - b) * B + 0.3)
    DV[2 * (k % 2)].at(b * B, f"B2:{L}{',' if k else ''}"); DV[1 + 2 * (k % 2)].at(round(b * B + 0.06, 3), f"F#3:{L - 0.06},")
    k += 1
s0 = c.s0["ドローンだけ"]
DI[0].at(s0 * B, "B1:12"); DI[1].at(round(s0 * B + 0.05, 3), "F#2:11.9,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の084（第3版）。北の峰へ続く細い稜線を、ひとりで歩く。スコットランドふうのスロー・エア（4/4・♩=48）、B ドリア。遠い谷底のバグパイプのような、B と F♯ の低い持続（遠いチェロとビオラが2小節ごとに交互に弓を返す）の上で、笛がゆっくり歌う。遅いテンポのまま、句の頭ごとにやわらかいスコッチ・スナップ（短‐長）が残る。山は前半の B。最後はドローンだけが残る。",
       harm_scenes=None, tail_scene="ドローンだけ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -44, "hp": 160, "lp": 3400, "wide": 0.014, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -25, "delay": 0.36, "lp": 2600, "rt": 4.6}}}
json.dump(air, open("/tmp/cel/w/air084.json", "w"), ensure_ascii=False)
