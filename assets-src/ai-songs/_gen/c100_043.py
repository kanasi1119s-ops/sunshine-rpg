# ケルト・フルート100曲「銀の笛と百の夜」043 塔の鐘守 The Bell Tower Keeper（2026-10-29）
# イメージ: 石の輪の向こうに、崩れかけた塔。昔ここに、年老いた鐘守が住んでいた。エイラが笛で問いかけると、
#   塔の石に残った鐘守の記憶が、低い声（チェロ）で答える。問いと答えはだんだん近づき、ふたりで一緒に歌う思い出の山。
#   そして鐘守の声は、静かに石の中へ帰っていく。
# 形: 笛（エイラ）とチェロ（鐘守の声）の対話。2小節ずつ→1小節ずつ→ふたりで一緒に→チェロが静かに去る。6/8・付点4分＝43。A エオリア。前半〜中盤に山→静けさ。
# ただひとつ: 笛以外で旋律を歌うのは、この曲のチェロだけ（低い音域なので笛の主役はゆずらない）。遠い鐘の録音ではじまり、鐘の余韻で終わる。
# 編曲の表:
#   遠い鐘  : 鐘の録音（遠く）＋弦の和音＋竪琴（はじまりから厚く）
#   対話1   : 笛が2小節問い、チェロが2小節答える。竪琴の分散和音・コントラバス
#   対話2   : 1小節ずつ、問いと答えが近づく。弦が3声に
#   思い出  : 笛とチェロが一緒に（チェロは対旋律）。弦の全和音・ホルン（山）
#   石へ    : 山のあと。チェロの声がだんだん低く、短くなっていく。笛はやさしく見送る
#   鐘の余韻: 鐘の録音と、弦の和音
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 129   # 8分音符＝129（付点4分＝43）
S = Song("C100", "043-the-bell-tower-keeper", "塔の鐘守", "The Bell Tower Keeper", BPM, 6, "A", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
Q8 = ["Am", "Am", "G", "G", "F", "F", "E", "E"]
R8 = ["Am", "Dm", "G", "C", "F", "Dm", "E", "Am"]
S.scene("遠い鐘", 4, "intro", ["Am", "Am", "Am", "Am"])
S.scene("対話1", 24, "verse", Q8 * 3)
S.scene("対話2", 16, "verse", R8 * 2)
S.scene("思い出", 16, "chorus", ["F", "G", "Am", "Am", "Dm", "G", "C", "E", "F", "G", "Am", "F", "Dm", "E", "Am", "Am"])
S.scene("石へ", 24, "verse", Q8 * 3)
S.scene("鐘の余韻", 6, "outro", ["Am", "F", "Am", "Am", "Am", "Am"])
NAMES = ["遠い鐘", "対話1", "対話2", "思い出", "石へ", "鐘の余韻"]

c = make(S, NAMES,
         [("遠い鐘", 0, 0.62), ("対話1", 0, 0.64), ("対話2", 0, 0.7), ("思い出", 0, 0.8), ("思い出", 10, 0.92), ("思い出", 15, 0.8),
          ("石へ", 0, 0.7), ("石へ", 23, 0.6), ("鐘の余韻", 0, 0.62), ("鐘の余韻", 5, 0.45)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="遠い鐘", passing=True, tension=False)
KEEP = S.track("鐘守の声（チェロ）", "strings", patch="cello", volume=0.15, pan=0.22, reverb=0.5, barGain=c.g())
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.09, pan=0.0, reverb=0.45, barGain=c.g())
HORN = [S.track(f"ホルン{i + 1}", "brass", patch="horn", volume=[0.05, 0.042][i], pan=[-0.3, -0.12][i], reverb=0.6, breath=False,
                attack=0.35, release=1.0, bright=-0.5, barGain=c.g()) for i in range(2)]

# 笛の問い（2小節）とチェロの答え（2小節）。6/8 は8分音符が1拍
ASK = [["5:3 4:2 3:1", "2:6"], ["3:2 4:1 5:3", "7:3 6:3"], ["1':3 7:2 6:1", "5:6"], ["4:2 5:1 6:3", "5:3 3:3"],
       ["5:3 6:2 7:1", "1':6"], ["7:2 6:1 5:3", "4:3 2:3"]]
ANS = [["1:3 2:2 3:1", "5,:6"], ["3:2 2:1 1:3", "7,:6"], ["6,:3 7,:2 1:1", "2:6"], ["3:2 2:1 1:3", "1:6"],
       ["5:3 4:2 3:1", "2:6"], ["1:2 7,:1 6,:3", "5,:6"]]
fl1, ce1 = [], []
for k in range(6): fl1 += ASK[k] + ["R:6", "R:6"]; ce1 += ["R:6", "R:6"] + ANS[k]
# 対話2：1小節ずつ
A1 = ["5:2 6:1 7:3", "1':3 7:3", "6:2 5:1 4:3", "5:6", "3:2 4:1 5:3", "6:3 5:3", "4:2 3:1 2:3", "1:6"]
C1 = ["3:3 2:3", "1:6", "4,:3 5,:3", "1:6", "1:3 7,:3", "6,:6", "5,:3 6,:3", "5,:6"]
fl2, ce2 = [], []
for k in range(16): fl2.append(A1[k % 8] if k % 2 == 0 else "R:6"); ce2.append("R:6" if k % 2 == 0 else C1[k % 8])
# 思い出：ふたりで一緒に（チェロは対旋律）
MEM = ["1':3 7:2 6:1", "5:6", "3:2 4:1 5:3", "6:3 5:3", "4:2 5:1 6:3", "7:6", "1':3 2':3", "7:6",
       "1':3 7:2 6:1", "5:3 6:3", "7:2 1':1 2':3", "1':6", "6:3 5:2 4:1", "3:3 2:3", "1:3 2:3", "1:6"]
MEMC = ["1:6", "7,:6", "1:3 2:3", "3:6", "2:6", "5,:6", "3:3 4:3", "5:6", "1:6", "7,:6", "1:3 5,:3", "1:6", "2:6", "7,:3 5,:3", "1:6", "1:6"]
# 石へ：笛はやさしく見送り、チェロの声は低く・短くなっていく
GO = ["5:6", "4:3 3:3", "2:6", "1:6", "3:6", "2:3 1:3", "7,:6", "1:6"]
GOC = [["1:3 7,:3", "6,:6"], ["5,:3", "R:3"], ["4,:3", "R:3"]]
fl4, ce4 = [], []
for k in range(24):
    fl4.append(GO[k % 8] if k % 4 != 3 else "R:6")
    blk = GOC[min(2, k // 8)]
    ce4.append(blk[k % 2] if k % 4 in (1, 2) else "R:6")
play_melody(c, "対話1", fl1, 4, "air", density=0.6, seed=4301)
play_melody(c, "対話1", ce1, 3, "air", density=0.0, track=KEEP)
play_melody(c, "対話2", fl2, 4, "air", density=0.7, seed=4302)
play_melody(c, "対話2", ce2, 3, "air", density=0.0, track=KEEP)
play_melody(c, "思い出", MEM, 4, "air", density=0.9, seed=4303)
play_melody(c, "思い出", MEMC, 3, "air", density=0.0, track=KEEP)
play_melody(c, "石へ", fl4, 4, "air", density=0.5, seed=4304)
play_melody(c, "石へ", ce4, 3, "air", density=0.0, track=KEEP)

B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "A3", "A5")
    if not (n == "鐘の余韻" and i >= 5): CB.bar(b, f"{nm(r - 12 if r - 12 >= 28 else r)}:6")
    nv = 2 if n in ("遠い鐘", "対話1") else 3
    if not (n == "鐘の余韻" and i >= 5):
        v = voice(ch, 57 if n != "思い出" else 60, nv, spread=True)
        for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n in ("遠い鐘", "対話1", "対話2", "石へ") or (n == "鐘の余韻" and i < 4):
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[3 % len(t)], t[2], t[1])))
    if n == "思い出":
        c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4 % len(t)], t[5 % len(t)], t[4 % len(t)], t[2]) * 2))
        hv = voice(ch, 52, 2, spread=False)
        for j in range(2): HORN[j].bar(b, f"{nm(hv[j])}:6")
rich(c, choir_scenes=["思い出"], pulse_scenes=["対話2", "思い出"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.35 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の043。崩れた塔の、年老いた鐘守の記憶。6/8・付点4分＝43、A エオリア。笛（エイラ）が問い、チェロ（鐘守の声）が答える対話。2小節ずつ→1小節ずつ→ふたりで一緒に歌う思い出の山→鐘守の声が静かに石の中へ帰っていく。遠い鐘ではじまり、鐘の余韻で終わる。",
       harm_scenes=None, tail_scene="鐘の余韻", fill=False, pads=True, pad_scenes=["対話1", "対話2", "思い出", "石へ", "鐘の余韻"], floor=True)
BAR = 6 * 60 / BPM
ev = [{"t": 0.3, "file": "0135", "db": -24, "len": 9.0, "pan": 0.35, "seek": 0.0, "hp": 200, "lp": 5000},
      {"t": round(c.s0["鐘の余韻"] * BAR + 0.5, 2), "file": "0135", "db": -25, "len": 10.0, "pan": 0.3, "seek": 0.0, "hp": 200, "lp": 5000}]
air = {"pre": 1.0, "tail": 8.0, "layers": [{"file": "0595", "db": -36, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8}], "events": ev,
       "fx": {"shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -24, "delay": 0.3, "lp": 2600, "rt": 5.0}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air043.json", "w"), ensure_ascii=False)
