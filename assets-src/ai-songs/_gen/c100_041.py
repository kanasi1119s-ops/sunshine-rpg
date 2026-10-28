# ケルト・フルート100曲「銀の笛と百の夜」041 立つ石 The Standing Stones — 第2版の作り方で新しく（2026-10-29）
# イメージ: 第5章「石の輪と塔」のはじまり。丘の上に、背の高い石が輪になって立っている。何千年も前の人が、ここで歌った。
#   朝の光が、石と石のすき間をまっすぐ通る瞬間がある。そのとき、古い響きが初めて「長調の明るさ」を持つ。
# 形: 古い歌（5度を中心にした響き）が石の間で鳴り、光が通る瞬間に開き、また古い響きに戻る。4/4・♩=48。D ミクソリディア。中盤〜終盤に大きな山1つ。
# ただひとつ: 3度のない「5度だけの和音」で進み（古い時代の響き）、光が通る山で初めて3度（長調・短調の色）が鳴る。
#   古い歌2では、笛の下に4度下の笛が平行に重なる（中世のオルガヌムの重ね方）。
# 編曲の表:
#   石の影  : 弦の5度のドローン、チェロの D、竪琴の空5度（はじまりから厚く）
#   古い歌1 : 笛＋5度のドローン＋竪琴の空5度の分散和音＋チェロ
#   古い歌2 : ＋4度下の平行の笛（オルガヌム）＋ホルンの低い5度
#   光      : 3度が初めて鳴る。弦の全和音・ホルン・竪琴の分散和音・ティンパニのやわらかいロール。笛は高い所で
#   石に戻る: 5度の響きに戻る。笛のかけら、ドローン
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 48
S = Song("C100", "041-the-standing-stones", "立つ石", "The Standing Stones", BPM, 4, "D", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
F8 = ["D5", "C5", "D5", "G5", "D5", "A5", "C5", "D5"]
S.scene("石の影", 3, "intro", ["D5", "D5", "D5"])
S.scene("古い歌1", 16, "verse", F8 * 2)
S.scene("古い歌2", 16, "verse", F8 * 2)
S.scene("光", 12, "chorus", ["D", "G", "Bm", "G", "D", "A", "G", "Em", "G", "D", "A", "D"])
S.scene("石に戻る", 8, "outro", ["D5", "C5", "D5", "G5", "D5", "D5", "D5", "D5"])
NAMES = ["石の影", "古い歌1", "古い歌2", "光", "石に戻る"]

c = make(S, NAMES,
         [("石の影", 0, 0.64), ("古い歌1", 0, 0.64), ("古い歌1", 15, 0.68), ("古い歌2", 0, 0.7), ("古い歌2", 15, 0.76),
          ("光", 0, 0.84), ("光", 6, 0.95), ("光", 11, 0.86), ("石に戻る", 0, 0.7), ("石に戻る", 7, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="石の影", passing=True, tension=False)
ORG = S.track("4度下の笛（オルガヌム）", "panflute", patch="flute", volume=0.2, bright=-0.85, pan=0.35, reverb=0.6, breath=False,
              noRestrike=True, mono=True, sustain=1.12, phrase=16, barGain=c.g())
HORN = [S.track(f"ホルン{i + 1}", "brass", patch="horn", volume=[0.06, 0.05, 0.045][i], pan=[-0.3, -0.15, 0.0][i], reverb=0.6, breath=False,
                attack=0.35, release=1.0, bright=-0.5, barGain=c.g()) for i in range(3)]
TIMP = S.track("ティンパニ（光）", "strings", patch="timpani", volume=0.07, pan=0.1, reverb=0.6, gainDb=-5, barGain=c.g())
DR = [S.track(f"5度のドローン{i + 1}", "strings", patch="slowStrings", volume=0.085, pan=[-0.45, 0.45][i], reverb=0.6, barGain=c.g()) for i in range(2)]

A = ["1:2 2:1 4:1", "5:3 4:1", "2:2 1:2", "4:4", "5:1 7:1 1':2", "7:2 5:1 4:1", "2:2 4:1 2:1", "1:4"]
Bm = ["5:2 7:1 1':1", "2':3 1':1", "7:2 5:2", "4:4", "5:1 4:1 2:2", "4:2 5:2", "7,:1 1:1 2:2", "1:4"]
L = ["5:2 1':2", "2':2 3':2", "2':3 1':1", "7:4", "1':2 7:1 6:1", "5:2 3:2", "4:2 5:2", "6:4", "5:1 6:1 7:2", "1':3 7:1", "6:2 5:2", "5:4"]
play_melody(c, "古い歌1", A + Bm, 4, "air", density=0.5, seed=4101)
play_melody(c, "古い歌2", Bm + A, 4, "air", density=0.7, seed=4102)
play_melody(c, "光", L, 4, "air", density=0.9, seed=4103)
play_melody(c, "石に戻る", ["1:2 2:1 4:1", "5:4", "4:2 2:2", "1:4", "5:2 4:2", "2:4", "1:4", "R:4"], 4, "air", density=0.4, seed=4104)

B = S.beats
# 古い歌2：笛の下に、完全4度下の笛が平行に重なる（オルガヌム）
a2, z2 = c.s0["古い歌2"] * B, (c.s0["古い歌2"] + 16) * B
for st, Ln, x in list(c.FLUTE.ev):
    p = midi_of(x)
    if p is None or not (a2 <= st < z2) or Ln < 0.4: continue
    if p - 5 >= 60: ORG.at(st + 0.03, f"{nm(p - 5)}:{x.split(':', 1)[1]}")

for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    fifth = n != "光"
    drone(DR, b, B, 50 if n != "光" else 50)                       # D と A の古いドローン（全体を通して）
    c.LOW.bar(b, f"{nm(r)}:4" if not (n == "石に戻る" and i >= 7) else "R:4")
    if fifth:
        # 3度のない響き：根音・5度・オクターブだけ
        v = [r + 12, r + 19, r + 24]
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if n == "石の影" or n == "古い歌1" or (n == "石に戻る" and i < 6):
            c.HARP.bar(b, f"{nm(r + 12)}:1 {nm(r + 19)}:1 {nm(r + 24)}:1 {nm(r + 19)}:1")
        if n == "古い歌2":
            c.HARP.bar(b, f"{nm(r + 12)}:0.5 {nm(r + 19)}:0.5 {nm(r + 24)}:0.5 {nm(r + 31)}:0.5 {nm(r + 24)}:1 {nm(r + 19)}:1")
            for j, m in enumerate((r, r + 7)): HORN[j].bar(b, f"{nm(m + 12 if m < 45 else m)}:4")
        if n == "石の影": c.HARP2.bar(b, f"R:2 {nm(r + 31)}:2")
    else:
        # 光：初めて3度が鳴る。弦の全和音（広い並べ方）・ホルン・竪琴の分散和音
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        hv = voice(ch, 50, 3, spread=False)
        for j in range(3): HORN[j].bar(b, f"{nm(hv[j])}:4")
        t = tones(ch, "D3", "D6")
        c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4 % len(t)], t[5 % len(t)], t[6 % len(t)], t[4 % len(t)], t[2], t[1])))
        if i == 0: TIMP.bar(b, " ".join("D2:0.25" for _ in range(8)) + " D2:2")
        if i == 6: TIMP.bar(b, "D2:4")
rich(c, choir_scenes=["光"], pulse_scenes=["光"], guitar=False, pizz=False, inner=True, choir_vol=0.11)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の041。丘の上の石の輪に、朝の光が通る。4/4・♩=48、D ミクソリディア。3度のない5度だけの古い響き（笛の下に4度下の笛が平行に重なるオルガヌム）で進み、光が石のすき間を通る山で初めて3度が鳴る。最後は5度の響きに戻る。",
       harm_scenes=None, tail_scene="石に戻る", fill=False, pads=True, pad_scenes=["古い歌1", "古い歌2", "光", "石に戻る"], floor=True)
air = {"pre": 1.0, "tail": 7.0, "layers": [{"file": "0595", "db": -34, "hp": 120, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -27, "rt": 8.0}, "far": {"db": -24, "delay": 0.3, "lp": 2600, "rt": 5.0}, "haze": {"db": -27, "rt": 8.0}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air041.json", "w"), ensure_ascii=False)
