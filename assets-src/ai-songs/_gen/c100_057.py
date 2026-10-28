# ケルト・フルート100曲「銀の笛と百の夜」057 二つの笛 Two Flutes, One Breath（2026-10-29。第6章 霧の湖）
# イメージ: 祖父の影は消えたのに、エイラが笛を吹くと、どこからかもう一本の笛が、少し遅れて同じ節を吹く。
#   はじめは1小節遅れ、次は1拍遅れ。だんだん息が近づいて、最後はふたりが同じ息で、和音で吹く。そして、ふたり同時に止める。
# 形: ピチカート → ひとり → 1小節ずれ → 1拍ずれ → 同じ息（山）→ 一斉に止める。3/4・♩=54・G ドリア。
# ただひとつ: 二本の笛のずれが「1小節 → 1拍 → 同時（3度の和音）」と回るたびに縮んでいく。
#   どのずれでもぶつからないように、旋律は G のマイナー・ペンタトニック（G B♭ C D F）だけで書く。
# 編曲の表:
#   ピチカート: 弦のピチカートだけで歩きだす（＋うすい弦の和音とチェロの床）
#   ひとり   : 笛ひとり。ピチカートと竪琴
#   1小節ずれ: 幻の笛（右・遠い響き）が1小節遅れで追う。弦2声
#   1拍ずれ  : 幻の笛が1拍遅れ。弦3声・内声
#   同じ息   : ふたりが同時に、幻の笛は3度下で和音に。山。竪琴の分散和音が細かく
#   止める   : ふたり同時の終止。全員の和音で止め、弦と竪琴の響きが残る
import sys, json
from c100_common import *
from c100_v2 import *
from c100_common import _dia

BPM = 54
S = Song("C100", "057-two-flutes-one-breath", "二つの笛", "Two Flutes, One Breath", BPM, 3, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.18})
P = ["Gm", "Gm", "F", "C", "Gm", "F", "C", "Bb", "Gm", "C", "F", "Gm", "Bb", "F", "C", "Gm"]
S.scene("ピチカート", 4, "intro", ["Gm", "F", "C", "Gm"])
S.scene("ひとり", 16, "verse", P)
S.scene("1小節ずれ", 16, "verse", P)
S.scene("1拍ずれ", 16, "verse", P)
S.scene("同じ息", 16, "chorus", P)
S.scene("止める", 4, "outro", ["Bb", "Gm", "Gm", "Gm"])
NAMES = ["ピチカート", "ひとり", "1小節ずれ", "1拍ずれ", "同じ息", "止める"]

c = make(S, NAMES,
         [("ピチカート", 0, 0.6), ("ひとり", 0, 0.64), ("1小節ずれ", 0, 0.66), ("1拍ずれ", 0, 0.7), ("同じ息", 0, 0.78), ("同じ息", 12, 0.88),
          ("止める", 0, 0.84), ("止める", 3, 0.56)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="ピチカート", passing=True, tension=False)
GHOST = S.track("幻の笛", "panflute", patch="flute", volume=0.3, bright=-0.8, pan=0.5, reverb=0.75, breath=False,
                noRestrike=True, mono=True, sustain=1.12, phrase=16, gainDb=2, barGain=c.g())
PZ = S.track("ピチカート（歩み）", "strings", patch="pizzicato", volume=0.075, pan=-0.35, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.12, reverb=0.5, barGain=c.g())

T = ["1:1 3:1 4:1", "5:2 4:1", "7:2 5:1", "4:3",
     "5:1 7:1 1':1", "7:2 5:1", "4:1 3:1 1:1", "3:3",
     "1':1.5 7:0.5 5:1", "4:2 5:1", "7:1 5:1 4:1", "5:3",
     "3:1 4:1 5:1", "7:1 5:1 4:1", "3:1 4:1 3:1", "1:3"]
play_melody(c, "ひとり", T, 4, "air", density=0.45, seed=5701)
play_melody(c, "1小節ずれ", T, 4, "air", density=0.55, seed=5702)
play_melody(c, "1拍ずれ", T, 4, "air", density=0.6, seed=5703)
lead = play_melody(c, "同じ息", T, 4, "air", density=0.6, seed=5704)
play_melody(c, "止める", ["7:1 5:1 4:1", "1:2 R:1", "R:3", "R:3"], 4, "air", density=0.0)
B = S.beats
# 幻の笛：1小節ずれ（1小節目は待つ）→ 1拍ずれ → 同じ息（3度下）
play_melody(c, "1小節ずれ", ["R:3"] + T[:15], 4, "air", density=0.3, seed=5711, track=GHOST)
gh = play_melody(c, "1拍ずれ", T, 4, "air", density=0.3, seed=5712, track=GHOST)
GHOST.ev = [(st + 1.0 if c.s0["1拍ずれ"] * B <= st < (c.s0["1拍ずれ"] + 16) * B else st, L, x) for st, L, x in GHOST.ev]
for t, L, m, mk in lead:
    if L < 0.4: continue
    pcs = chord_pcs(S.chords[int(t // B)])
    h = next((q for q in (_dia(S, m, -2), _dia(S, m, -3), _dia(S, m, -4)) if q % 12 in pcs), _dia(S, m, -2))
    if h >= 60: GHOST.at(round(t, 3), f"{nm(h)}:{round(L, 3)}{mk}")
GHOST.bar(c.s0["止める"], "D5:1 Bb4:1 A4:1"); GHOST.bar(c.s0["止める"] + 1, "Bb4:2 R:1")

for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "G3", "G5")
    CELLO.bar(b, f"{nm(r)}:3")
    if n == "止める":
        v = voice(ch, 55, 3, spread=True)
        if i == 1:
            PZ.bar(b, f"{nm(r + 12)}:1 R:2"); c.HARP.bar(b, " ".join(f"{nm(x)}:0.25" for x in t[:4]) + " R:2")
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
        if i >= 2: c.HARP2.bar(b, f"{nm(tones(ch, 'G5', 'G6')[i - 2])}:3")
        continue
    PZ.bar(b, f"{nm(r + 12)}:1 {nm(t[2])}:1 {nm(t[1])}:1" if i % 2 == 0 else f"{nm(r + 7)}:1 {nm(t[3 % len(t)])}:1 {nm(t[2])}:1")
    nv = 2 if n in ("ピチカート", "ひとり", "1小節ずれ") else 3
    v = voice(ch, 52 if nv == 2 else 55, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:3")
    if n in ("ひとり", "1小節ずれ", "1拍ずれ"): c.HARP.bar(b, f"{nm(t[0])}:1.5 {nm(t[2])}:1.5")
    if n == "同じ息": c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4 % len(t)], t[5 % len(t)], t[4 % len(t)], t[2])))
rich(c, choir_scenes=[], pulse_scenes=["1拍ずれ", "同じ息"], guitar=False, pizz=False, inner=True)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の057。消えた祖父の笛と、同じ息で吹く。3/4・♩=54、G ドリア（旋律は G のマイナー・ペンタトニックだけ）。もう一本の幻の笛が、はじめは1小節遅れ、次は1拍遅れで追い、最後はふたりが同時に3度の和音で吹いて、一斉に止める。",
       harm_scenes=None, tail_scene="止める", fill=False, pads=True, pad_scenes=["ひとり", "1小節ずれ", "1拍ずれ", "同じ息", "止める"], floor=True)
air = {"pre": 0.6, "tail": 7.0, "layers": [{"file": "0691", "db": -39, "hp": 150, "lp": 5000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -29, "rt": 7.0}, "far": {"db": -25, "delay": 0.25, "lp": 2800, "rt": 4.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air057.json", "w"), ensure_ascii=False)
