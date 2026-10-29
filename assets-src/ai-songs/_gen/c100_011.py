# ケルト・フルート100曲「銀の笛と百の夜」011 草を渡る風 Wind Through the Grass — 第2版（2026-10-28）
# イメージ: 一面の草原を、風がなでていく。草がいっせいになびいて、また起き上がる。その「なびき」を、何本もの笛の息で描く。
#   風が強まると和音がふくらみ、弱まると1本の笛だけが残る。山はなく、風の強弱だけがある。
# 形（台帳）: 笛だけの合唱（コラール）。主の笛の下に、和音の笛が2〜3本。4/4・♩=60。D ドリア。
#   強さは8小節＝32秒の周期で「風のうねり」をつくり、環境音の風も同じ周期で動かす。
# 編曲の表:
#   風      : 風の音→笛の和音だけがふくらんで、しぼむ（旋律なし）
#   草原1   : 主の笛＋和音の笛2本。うすい弦とチェロの低い D が地面
#   草原2   : ＋低い笛（3本目）＋竪琴がときどき1音（草の露）
#   風の道  : 旋律なし。笛の和音だけが大きくうねる（強い風が通り抜ける）
#   草原3   : 主の笛がいちばん高い所まで。和音の笛3本
#   風      : 笛の和音がしぼみ、風の音に戻る
import sys, math
from c100_common import *
from c100_v2 import *

S = Song("C100", "011-wind-through-the-grass", "草を渡る風", "Wind Through the Grass", 60, 4, "D", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
G1c = ["Dm", "Dm", "C", "G", "Dm", "C", "Am", "Am"]
G2c = ["F", "C", "Am", "G", "Dm", "C", "G", "Dm"]
G3c = ["Am", "Am", "F", "G", "Dm", "G", "C", "Am"]
G4c = ["G", "C", "G", "Dm", "Am", "C", "G", "Dm"]
S.scene("風", 4, "intro", ["Dm", "C", "Dm", "Dm"])
S.scene("草原1", 16, "verse", G1c + G2c)
S.scene("草原2", 16, "verse", G3c + G4c)
S.scene("風の道", 8, "break", ["Dm", "C", "F", "G", "Dm", "C", "G", "Dm"])
S.scene("草原3", 16, "chorus", G3c + G2c)
S.scene("風に還る", 8, "outro", ["Dm", "C", "Dm", "Dm", "Dm", "Dm", "Dm", "Dm"])
NAMES = ["風", "草原1", "草原2", "風の道", "草原3", "風に還る"]

c = make(S, NAMES,
         [("風", 0, 0.58), ("草原1", 0, 0.64), ("草原2", 0, 0.68), ("風の道", 0, 0.72), ("草原3", 0, 0.72), ("風に還る", 0, 0.6), ("風に還る", 7, 0.32)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="風", passing=True, tension=False)
WIND = [0.86 + 0.14 * math.sin(2 * math.pi * (b - 2) / 8) for b in range(c.NB)]
def wg(): return [round(g * WIND[b], 3) for b, g in enumerate(c.g())]
CH = [S.track(f"和音の笛{i + 1}", "panflute", patch="flute", volume=[0.17, 0.15, 0.13][i], bright=-0.9, pan=[-0.4, 0.4, -0.15][i], reverb=0.65,
              breath=(i == 0), noRestrike=True, mono=True, sustain=1.12, phrase=16, barGain=wg()) for i in range(3)]
CELLO = S.track("チェロ（地面）", "strings", patch="cello", volume=0.07, pan=0.1, reverb=0.5, barGain=c.g())
c.FLUTE.spec["barGain"] = [round(x * WIND[b], 3) for b, x in enumerate(c.FLUTE.spec["barGain"])]

G1 = ["R:2 5:2", "6:3 5:1", "4:2 3:2", "2:4", "R:2 3:2", "4:3 5:1", "6:2 7:1 6:1", "5:4"]
G2 = ["R:2 5:2", "7:3 6:1", "5:2 6:2", "4:4", "R:2 3:2", "5:3 4:1", "3:2 2:1 1:1", "1:4"]
G3 = ["R:2 5:2", "7:3 6:1", "5:2 7:2", "6:4", "R:2 4:2", "6:3 5:1", "4:2 3:1 2:1", "3:4"]
G4 = ["R:2 2:2", "4:3 3:1", "2:2 7,:2", "1:4", "R:2 5,:2", "7,:3 1:1", "2:2 3:2", "1:4"]
mel = {}
mel["草原1"] = play_melody(c, "草原1", G1 + G2, 5, "air", density=0.6, seed=1101)
mel["草原2"] = play_melody(c, "草原2", G3 + G4, 5, "air", density=0.7, seed=1102)
mel["草原3"] = play_melody(c, "草原3", G3 + G2, 5, "air", density=0.8, seed=1103)

B = S.beats
# 旋律のある所：主の笛の音ごとに、その下の和音の音を和音の笛が吹く（コラール）
for sc, notes in mel.items():
    nv = 2 if sc == "草原1" else 3
    for t, L, m, mk in notes:
        if L < 0.9: continue
        bar = int(t // B); pcs = chord_pcs(S.chords[bar])
        below = [x for x in range(m - 14, m - 1) if x % 12 in pcs]
        below = sorted(below, reverse=True)[:nv]
        for j, x in enumerate(below): CH[j].at(round(t + 0.02 * (j + 1), 3), f"{nm(x)}:{L}")
# 旋律のない所：和音の笛がふくらんで、しぼむ
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    if n in ("風", "風の道") or (n == "風に還る" and i < 6):
        v = voice(ch, 62, 3, spread=False)
        for j in range(3): CH[j].bar(b, f"{nm(v[j])}:4")
    if not (n == "風に還る" and i >= 7):
        CELLO.bar(b, "D2:4")
        v = voice(ch, 50, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    # 草のなびき：竪琴がゆっくり上り下りする（風の周期に合わせて強弱）
    if n in ("草原1", "草原2", "草原3", "風の道"):
        roving_thumb(c.HARP2, b, B, ch, up=(b % 2 == 0))
    if n in ("草原2", "草原3") and i % 4 == 1: c.HARP.bar(b, f"R:2 {nm(tones(ch, 'D5', 'D6')[1])}:2")

for tr in (c.HARP2,): tr.spec["barGain"] = wg()
rich(c, choir_scenes=[], pulse_scenes=["草原2", "草原3"], guitar=True, pizz=False, inner=True)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の011（第2版）。一面の草原を風がなでる。4/4・♩=60、D ドリア。笛だけの合唱（主の笛の下に和音の笛が2〜3本）。強さは8小節周期の風のうねり。山はなく、風の強弱だけ。",
       harm_scenes=None, tail_scene="風に還る", fill=False, pads=True, pad_scenes=["草原1", "草原2", "風の道", "草原3", "風に還る"], floor=True)
