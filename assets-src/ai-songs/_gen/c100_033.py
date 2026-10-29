# ケルト・フルート100曲「銀の笛と百の夜」033 梟の問い The Owl's Question — 第2版（2026-10-28）
# イメージ: 夜の森。高い枝の梟が「ほう」と問いかける。エイラは笛で、梟と同じ高さの音（F♯）から答える。
#   やがて笛が問い、梟が答える。言葉は通じないのに、二人の問答は少しずつ打ちとけていく。最後は梟の声だけが残る。
# 形（台帳）: 掛け合い（笛と本物の梟の録音 0936。梟の声の高さ＝約370Hz＝F♯4。だから B エオリアにして、梟の声を属音 F♯ にした）。
#   4/4・♩=48。始め：梟／終わり：梟。山なし。
# 編曲の表:
#   夜     : 夜の森の空気、低い弦のドローン
#   問答1  : 4小節ごとに、1小節目で梟が問い、2〜4小節目で笛が F♯ から答える
#   問答2  : 笛が3小節問い、4小節目で梟が答える
#   二人   : 笛の長い節。梟が2小節ごとに寄りそう。竪琴の倍音
#   梟     : 梟の声とドローンだけ
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 48
S = Song("C100", "033-the-owls-question", "梟の問い", "The Owl's Question", BPM, 4, "B", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
QC = ["Bm", "Em", "Bm", "F#m", "G", "D", "Em", "Bm", "Bm", "G", "A", "Bm", "Em", "G", "F#m", "Bm"]
S.scene("夜", 2, "intro", ["Bm", "Bm"])
S.scene("問答1", 16, "verse", QC)
S.scene("問答2", 16, "verse", QC)
S.scene("二人", 16, "chorus", QC)
S.scene("梟", 4, "outro", ["Bm"] * 4)
NAMES = ["夜", "問答1", "問答2", "二人", "梟"]

c = make(S, NAMES,
         [("夜", 0, 0.6), ("問答1", 0, 0.62), ("問答2", 0, 0.66), ("二人", 0, 0.7), ("二人", 15, 0.66), ("梟", 0, 0.56), ("梟", 3, 0.36)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="夜", passing=True, tension=False)
DR = [S.track(f"ドローン{i + 1}", "strings", patch="slowStrings", volume=0.1, pan=[-0.4, 0.4][i], reverb=0.6, barGain=c.g()) for i in range(2)]
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.1, reverb=0.5, barGain=c.g())

# 笛の答え：梟の高さ（F♯＝5度）から始める
ANS = [["5:1.5 4:0.5 3:2", "2:1 3:1 1:2", "7,:3 R:1"], ["5:2 6:1 5:1", "4:1 3:1 2:2", "3:3 R:1"],
       ["5:1 6:1 7:2", "6:1 5:1 4:2", "5:3 R:1"], ["5:1.5 3:0.5 2:2", "1:1 7,:1 1:2", "1:3 R:1"]]
ASK = [["3:1 4:1 5:2", "6:2 5:2", "4:3 R:1"], ["1':1 7:1 6:2", "5:2 4:1 3:1", "2:3 R:1"],
       ["3:1 5:1 7:2", "1':2 7:1 6:1", "5:3 R:1"], ["4:1 3:1 2:2", "3:1 2:1 7,:2", "1:3 R:1"]]
play_melody(c, "問答1", sum([["R:4"] + a for a in ANS], []), 4, "air", density=0.6, seed=3301)
play_melody(c, "問答2", sum([a + ["R:4"] for a in ASK], []), 4, "air", density=0.7, seed=3302)
play_melody(c, "二人", ["5:2 6:1 7:1", "1':3 7:1", "6:2 5:2", "4:4", "5:1 4:1 3:2", "4:2 6:2", "5:4", "R:4",
                       "5:2 7:1 6:1", "5:2 4:1 3:1", "2:2 3:2", "4:4", "3:1 2:1 1:2", "7,:2 2:2", "1:4", "R:4"], 4, "air", density=0.9, seed=3303)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    drone(DR, b, B, 47)
    if n in ("夜", "問答1", "問答2", "二人") or (n == "梟" and i < 3):
        CELLO.bar(b, f"{nm(r)}:4")
        v = voice(ch, 55 if n != "夜" else 50, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    # 梟が鳴く小節（笛が休む）：竪琴がそっと和音をなでて、森の奥行きを残す
    if (n == "問答1" and i % 4 == 0) or (n == "問答2" and i % 4 == 3):
        t = tones(ch, "B3", "B5"); c.HARP.bar(b, "R:1.5 " + " ".join(f"{nm(x)}:{0.25 if j < 3 else 1.75}" for j, x in enumerate(t[:4])))
    if n == "二人" and i % 2 == 1: c.HARP2.bar(b, f"R:2 {nm(tones(ch, 'B5', 'B6')[0])}:2")
    if n == "梟" and i == 3: DR[0].bar(b, "R:4"); DR[1].bar(b, "R:4")
rich(c, choir_scenes=["二人"], pulse_scenes=["問答2", "二人"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の033（第2版）。夜の森で、梟と笛の問答。4/4・♩=48、B エオリア。本物の梟の声（約370Hz＝F♯）に、笛が同じ高さから答える。やがて笛が問い、梟が答え、打ちとけていく。最後は梟の声だけ。",
       harm_scenes=None, tail_scene="梟", fill=False, pads=True, pad_scenes=["問答1", "問答2", "二人", "梟"])
BAR = 4 * 60 / BPM
SEEK = [0.3, 3.4, 6.2, 8.8, 11.5, 14.2, 17.1, 19.7, 22.6]
ev = []; q = 0
def owl(b, beat=0.0, db=-20, pan=0.35):
    global q
    ev.append({"t": round(b * BAR + beat * 60 / BPM, 2), "file": "0936", "db": db, "len": 1.2, "pan": pan, "seek": SEEK[q % len(SEEK)], "hp": 200, "lp": 3000}); q += 1
owl(c.s0["夜"] + 1, 0)
for j in range(0, 16, 4): owl(c.s0["問答1"] + j, 0.5)
for j in range(3, 16, 4): owl(c.s0["問答2"] + j, 0.5, -21, 0.4)
for j in range(1, 16, 2): owl(c.s0["二人"] + j, 2.5, -24, 0.45)
owl(c.s0["梟"], 0.5, -20, 0.35); owl(c.s0["梟"] + 2, 0.5, -23, 0.5)
air = {"pre": 1.5, "tail": 8.0, "layers": [{"file": "0621", "db": -33, "hp": 120, "lp": 6000, "wide": 0.014, "duck": 0.3, "fade": 6},
                                           {"file": "0425", "db": -40, "hp": 1500, "lp": 9000, "wide": 0.012, "pan": -0.25, "duck": 0.3, "fade": 8}],
       "events": ev,
       "fx": {"glass": {"hz": [370.0, 740.0, 1109.7], "db": -28, "rt": 7.0, "start": 4}, "shimmer": {"db": -27, "rt": 9.0}, "far": {"db": -24, "delay": 0.3, "lp": 2400, "rt": 5.0},
              "haze": {"db": -26, "rt": 9.0}, "band": {"db": -38, "hz": 6000, "per": 29}}, "intro_db": 8.5}
json.dump(air, open("/tmp/cel/w/air033.json", "w"), ensure_ascii=False)
print("梟:", len(ev))
