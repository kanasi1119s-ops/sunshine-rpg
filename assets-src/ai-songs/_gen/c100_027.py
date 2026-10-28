# ケルト・フルート100曲「銀の笛と百の夜」027 鴨の親子 Ducklings in a Row — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 川面を、母鴨のあとに子鴨たちが一列になってついていく。母が先に節を歌い、子どもたちが少しずつ遅れて、同じ節で追いかける。
#   子が1羽、2羽、3羽と増えていく。最後は巣に着いて、みんなでそろって止まる。
# 形（台帳）: 6/8 の行進・親の笛のあとを、子の声（小さな笛・グロッケン・ピチカート）が1拍ずつ遅れて追う。付点4分＝72。F イオニア。
#   始め：小さな足取り（ピチカート）／終わり：巣（みんなでそろって止まる）。山なし（にぎやかさが増えるだけ）。
# 編曲の表:
#   足取り : ピチカートの小さな足取り
#   親     : 母の笛（AABB）＋竪琴＋ギターの軽い打ち
#   子1    : ＋小さな笛（右）が付点4分1つ遅れて
#   子2    : ＋グロッケンが1小節遅れて（1オクターブ上）
#   子3    : ＋ピチカートが1小節半遅れて（低い所）
#   巣     : 全員がそろって同じ節を歌い、「付点4分・付点4分」で止まる
import sys
from c100_common import *
from c100_v2 import *

BPM = 216
S = Song("C100", "027-ducklings-in-a-row", "鴨の親子", "Ducklings in a Row", BPM, 6, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["F", "Bb", "F", "C", "F", "Bb", "C", "F"]
BC = ["C", "Bb", "F", "C", "C", "Bb", "C", "F"]
S.scene("足取り", 4, "intro", ["F", "F", "C", "F"])
for nm_ in ("親", "子1", "子2", "子3"): S.scene(nm_, 32, "verse", AC * 2 + BC * 2)
S.scene("巣", 8, "outro", AC)
NAMES = ["足取り", "親", "子1", "子2", "子3", "巣"]

c = make(S, NAMES,
         [("足取り", 0, 0.64), ("親", 0, 0.68), ("子1", 0, 0.72), ("子2", 0, 0.76), ("子3", 0, 0.8), ("巣", 0, 0.84), ("巣", 7, 0.6)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="足取り", passing=True, tension=False)
KID = S.track("子の笛（小さな笛）", "panflute", patch="flute", volume=0.26, bright=-0.7, pan=0.45, reverb=0.5, breath=False, noRestrike=True, mono=True, sustain=1.05, barGain=c.g())
GLOCK = S.track("子のグロッケン", "bell", patch="glockenspiel", volume=0.045, pan=-0.35, reverb=0.6, barGain=c.g())
PZ = S.track("子のピチカート", "strings", patch="pizzicato", volume=0.08, pan=-0.15, reverb=0.35, barGain=c.g())
DRUM = S.track("ボーラン（水かき）", "guitar", patch="frameDrum", volume=0.085, pan=-0.15, reverb=0.3, modulate=False, barGain=c.g())
GTR = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.045, pan=0.3 + 0.04 * i, reverb=0.3, barGain=c.g()) for i in range(4)]

A = ["1:2 3:1 5:2 3:1", "4:2 6:1 5:3", "3:2 5:1 1':2 5:1", "5:3 2:3", "1:2 3:1 5:2 3:1", "4:2 6:1 5:2 4:1", "3:2 2:1 7,:2 2:1", "1:6"]
Bm = ["5:2 6:1 7:2 1':1", "6:2 5:1 4:3", "3:2 4:1 5:2 6:1", "5:3 2:3", "5:2 6:1 7:2 1':1", "2':2 1':1 6:3", "5:2 4:1 3:2 2:1", "1:6"]
TUNE = A + A + Bm + Bm
for k, sc in enumerate(("親", "子1", "子2", "子3")):
    play_melody(c, sc, TUNE, 4, "jig", density=0.4 + 0.2 * k, seed=2700 + k)
play_melody(c, "巣", A[:7] + ["1:3 1:3"], 4, "jig", density=0.5, seed=2705)
B = S.beats
def follow(track, start_scene, delay, octs, stop_bar):
    ev = []
    for sc in NAMES[NAMES.index(start_scene):5]:
        ev += section_events(c, sc, TUNE, 4)
    for t, L, m in ev:
        t2 = t + delay
        if t2 >= stop_bar * B: break
        m2 = m + 12 * octs
        while m2 > 96: m2 -= 12
        track.at(round(t2, 3), f"{nm(m2)}:{L}")
nest = c.s0["巣"]
follow(KID, "子1", 3, 0, nest)
follow(GLOCK, "子2", 6, 1, nest)
follow(PZ, "子3", 9, -1, nest)
# 巣：全員がそろって同じ節（遅れなし）
for t, L, m in section_events(c, "巣", A[:7] + ["1:3 1:3"], 4):
    KID.at(round(t + 0.02, 3), f"{nm(m)}:{L}"); GLOCK.at(t, f"{nm(m + 12)}:{L}"); PZ.at(t, f"{nm(m - 12)}:{L}")
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "F3", "F5")
    if n == "足取り":
        PZ.bar(b, f"{nm(r + 12)}:1 R:2 {nm(r + 19)}:1 R:2" if i < 3 else f"{nm(r + 12)}:1 R:1 {nm(r + 12)}:1 {nm(r + 19)}:1 R:2")
        if i >= 1: strum(GTR, b, B, ch, [(0, 3, "d", ","), (3, 3, "d", ",")])
        if i >= 2: c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:1 {nm(t[4 % len(t)])}:2 {nm(t[2])}:1")
        c.LOW.bar(b, f"{nm(r)}:6")
        continue
    if n != "親": bodhran(DRUM, b, B, "jig", var=1 if i % 8 == 7 else 0, soft=(n == "子1"))
    c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:1 {nm(t[4 % len(t)])}:2 {nm(t[2])}:1")
    strum(GTR, b, B, ch, ([(0, 2, "d", ","), (3, 2, "d", ",")] if n == "親" else JIG_STRUM) if n != "巣" or i < 7 else [(0, 3, "d", "!"), (3, 3, "d", "!")])
    if n in ("子1", "子2", "子3", "巣"):
        v = voice(ch, 53 if n == "子1" else 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n in ("親", "子1"): c.LOW.bar(b, f"{nm(r)}:6")
    if n in ("子2", "子3", "巣"): c.LOW.bar(b, f"{nm(r)}:3 {nm(r + 7)}:3")
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.28 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の027（第2版・明るく速めの曲）。川面を行く鴨の親子。6/8・付点4分＝72、F イオニア。母の笛のあとを、子の声（小さな笛・グロッケン・ピチカート）が1拍・1小節・1小節半遅れて追いかけ、子が増えていく。最後は巣でみんなそろって止まる。",
       harm_scenes=None, tail_scene="巣", fill=False, pads=True, pad_scenes=["子1", "子2", "子3", "巣"], double=False)
