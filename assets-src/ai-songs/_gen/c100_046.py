# ケルト・フルート100曲「銀の笛と百の夜」046 朽ちた礼拝堂 The Roofless Chapel（2026-10-29）
# イメージ: 塔のそばの、屋根の落ちた小さな礼拝堂。壁と柱だけが残り、上はまるごと空。
#   祈りの歌は、はじめ石の壁の中で小さく響いているが、だんだん上へ上へと広がり、最後は屋根のない空いっぱいに開いていく。
# 形: 弦の祈りの和音（コラール）の上で、笛が祈りの節。和音の並べ方が「狭い→広い」へ開いていき、最後は空へ。3/4・♩=50。F イオニア。終盤に静かな山。
# ただひとつ: 弦4声の和音の並べ方が、場面ごとに広がる（はじめは1オクターブの中に集まり、最後は4オクターブに開く）。
# 編曲の表:
#   石の床  : 弦4声の狭い和音＋チェロ（はじまりから厚く）
#   祈り1   : 笛の祈りの節。弦は狭いまま。竪琴がときどき
#   祈り2   : 和音が少し広がる。竪琴の分散和音
#   光の柱  : さらに広がる。笛の和声・内声
#   空へ    : いちばん広い（4オクターブ）。笛が高い所で。山
#   青空    : 高い和音がのびて消える
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 50
S = Song("C100", "046-the-roofless-chapel", "朽ちた礼拝堂", "The Roofless Chapel", BPM, 3, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
CC = ["F", "C", "Bb", "F", "Gm", "Bb", "C", "F", "Am", "Dm", "Bb", "C", "Bb", "Gm", "C", "F"]
S.scene("石の床", 3, "intro", ["F", "Bb", "F"])
S.scene("祈り1", 16, "verse", CC)
S.scene("祈り2", 16, "verse", CC)
S.scene("光の柱", 12, "verse", CC[:12])
S.scene("空へ", 16, "chorus", CC)
S.scene("青空", 5, "outro", ["Bb", "C", "F", "F", "F"])
NAMES = ["石の床", "祈り1", "祈り2", "光の柱", "空へ", "青空"]
WIDTH = {"石の床": 0, "祈り1": 0, "祈り2": 1, "光の柱": 2, "空へ": 3, "青空": 3}

c = make(S, NAMES,
         [("石の床", 0, 0.62), ("祈り1", 0, 0.64), ("祈り2", 0, 0.68), ("光の柱", 0, 0.72), ("空へ", 0, 0.8), ("空へ", 11, 0.9), ("空へ", 15, 0.82),
          ("青空", 0, 0.72), ("青空", 4, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="石の床", passing=True, tension=False)
STR4 = S.track("弦の持続（4声目）", "strings", patch="slowStrings", recipe="celtic-strings", volume=0.03, pan=-0.3, reverb=0.55, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.15, reverb=0.45, barGain=c.g())
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.07, pan=0.0, reverb=0.5, barGain=c.g())

M1 = ["5:2 6:1", "5:2 3:1", "4:2 5:1", "3:3", "2:2 3:1", "4:2 6:1", "5:2 4:1", "3:3",
      "1':2 7:1", "6:2 5:1", "4:1 5:1 6:1", "5:3", "4:2 3:1", "2:2 3:1", "2:2 7,:1", "1:3"]
M2 = ["1':2 2':1", "3':3", "2':2 1':1", "7:3", "1':2 6:1", "5:2 6:1", "1':2 2':1", "1':3",
      "3':2 2':1", "1':2 7:1", "6:1 7:1 1':1", "2':3", "1':2 6:1", "5:2 4:1", "2:2 7,:1", "1:3"]
play_melody(c, "祈り1", M1, 4, "air", density=0.5, seed=4601)
play_melody(c, "祈り2", M1, 4, "air", density=0.7, seed=4602)
play_melody(c, "光の柱", M2[:12], 4, "air", density=0.7, seed=4603)
play_melody(c, "空へ", M2, 4, "air", density=0.9, seed=4604)
play_melody(c, "青空", ["5:3", "6:2 7:1", "1':3", "1':3", "R:3"], 4, "air", density=0.2, seed=4605)

def chorale(ch, w):
    """4声の和音。w=0: 1オクターブの中に集める／w=3: 4オクターブに開く"""
    r = low(ch, "C2"); pcs = sorted(chord_pcs(ch), key=lambda p: (p - r) % 12)
    third = [p for p in pcs if (p - r) % 12 in (3, 4)][0]; fifth = [p for p in pcs if (p - r) % 12 == 7][0]
    def at(pc, lo): return next(m for m in range(lo, lo + 12) if m % 12 == pc)
    if w == 0: base = 55; return sorted([at(r % 12, base), at(third, base), at(fifth, base), at(r % 12, base + 7)])
    if w == 1: return [at(r % 12, 48), at(fifth, 55), at(third, 62), at(r % 12, 67)]
    if w == 2: return [at(r % 12, 43), at(fifth, 55), at(third, 64), at(fifth, 72)]
    return [at(r % 12, 38), at(fifth, 53), at(third, 66), at(r % 12, 79)]

B = S.beats
tracks4 = c.STR + [STR4]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "青空" and i == 4: continue
    v = chorale(ch, WIDTH[n])
    for j in range(4): tracks4[j].bar(b, f"{nm(v[j])}:3")
    CELLO.bar(b, f"{nm(r)}:3")
    if WIDTH[n] >= 2: CB.bar(b, f"{nm(r - 12 if r - 12 >= 28 else r)}:3")
    t = tones(ch, "F3", "F6")
    if n == "祈り1" and i % 4 == 3: c.HARP.bar(b, " ".join(f"{nm(x)}:{0.2 if j < 3 else 2.4}" for j, x in enumerate(t[:4])))
    if n in ("祈り2", "光の柱", "空へ"):
        lo = {"祈り2": 0, "光の柱": 2, "空へ": 3}[n]
        c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[lo], t[lo + 2], t[lo + 4], t[lo + 5], t[lo + 4], t[lo + 2])))
rich(c, choir_scenes=["光の柱", "空へ"], pulse_scenes=["祈り2", "光の柱", "空へ"], guitar=False, pizz=False, inner=True, choir_vol=0.11)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の046。屋根の落ちた礼拝堂の祈り。3/4・♩=50、F イオニア。弦4声の祈りの和音の上で、笛が祈りの節。和音の並べ方が場面ごとに広がり（1オクターブ→4オクターブ）、最後は屋根のない空いっぱいに開いていく。",
       harm_scenes=None, tail_scene="青空", fill=False, pads=True, pad_scenes=["祈り1", "祈り2", "光の柱", "空へ", "青空"], floor=True)
air = {"pre": 0.8, "tail": 8.0, "layers": [{"file": "0595", "db": -37, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8},
                                           {"file": "0222", "db": -40, "hp": 400, "lp": 9000, "wide": 0.012, "pan": 0.25, "duck": 0.35, "start": 150, "fade": 20}],
       "fx": {"shimmer": {"db": -27, "rt": 9.0}, "far": {"db": -24, "delay": 0.3, "lp": 2600, "rt": 5.0}, "haze": {"db": -27, "rt": 9.0}}, "intro_db": 5.0}
json.dump(air, open("/tmp/cel/w/air046.json", "w"), ensure_ascii=False)
