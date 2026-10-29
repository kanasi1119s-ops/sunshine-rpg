# ケルト・フルート100曲「銀の笛と百の夜」048 鐘の秘密 The Secret of the Bell（2026-10-29）
# イメージ: 塔の床の石の一枚だけが、たたくと鐘のように鳴る。その下に、秘密の入口がある。
#   エイラの笛は、はじめ「どこ？」と問いかけるように上がっては止まる。鐘の音が鳴ると、その響きの中の音を弦が引き継ぎ、
#   問いはだんだん「ここだ」と下りて閉じる答えに変わっていく。最後に、石の扉が開く（長調の和音）。
# 形: 問いの旋律（上がって止まる）→鐘→問いと答えが交互に→答え（下りて閉じる）が勝つ→扉が開く。6/8・付点4分＝44。D ドリア→D 長調。終盤に1つの山。
# ただひとつ: 鐘の録音の響き（主音と、短3度上の倍音）を、弦がそのまま和音として引き継ぐ。最後に短3度が長3度に変わって扉が開く。
# 編曲の表:
#   問い    : 竪琴が上がって止まる問い＋弦＋チェロ（はじまりから厚く）
#   探す1   : 笛の問い（2小節ずつ、上がって止まる）。竪琴・チェロ・弦
#   鐘の音  : 鐘の録音。弦が鐘の響き（D と F）を引き継いで、高い所でのばす
#   探す2   : 問いと答えが交互に。弦3声・内声の動き
#   扉      : 答えが続く（下りて閉じる）。ホルン・笛の和声。山
#   開く    : D の長三和音。高い弦と笛
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 132   # 8分音符＝132（付点4分＝44）
S = Song("C100", "048-the-secret-of-the-bell", "鐘の秘密", "The Secret of the Bell", BPM, 6, "D", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
QC = ["Dm", "G", "F", "C", "Am", "Em", "Dm", "G"]
S.scene("問い", 4, "intro", ["Dm", "G", "Dm", "G"])
S.scene("探す1", 24, "verse", QC * 3)
S.scene("鐘の音", 4, "break", ["Dm", "Dm", "Dm", "Dm"])
S.scene("探す2", 32, "verse", ["Dm", "G", "G", "Dm", "F", "C", "Am", "Dm"] * 4)
S.scene("扉", 16, "chorus", ["F", "C", "G", "Dm", "F", "C", "G", "A", "C", "F", "C", "G", "F", "Gm", "A", "A"])
S.scene("開く", 10, "outro", ["D", "G", "D", "A", "D", "G", "D", "D", "D", "D"])
NAMES = ["問い", "探す1", "鐘の音", "探す2", "扉", "開く"]

c = make(S, NAMES,
         [("問い", 0, 0.62), ("探す1", 0, 0.64), ("鐘の音", 0, 0.62), ("探す2", 0, 0.68), ("扉", 0, 0.78), ("扉", 12, 0.92), ("開く", 0, 0.86), ("開く", 9, 0.55)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="問い", passing=True, tension=False)
HORN = [S.track(f"ホルン{i + 1}", "brass", patch="horn", volume=[0.055, 0.045, 0.04][i], pan=[-0.3, -0.12, 0.05][i], reverb=0.6, breath=False,
                attack=0.35, release=1.0, bright=-0.5, barGain=c.g()) for i in range(3)]
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.12, reverb=0.45, barGain=c.g())
BELLSTR = [S.track(f"鐘の響きを引き継ぐ弦{i + 1}", "strings", patch="slowStrings", volume=0.05, pan=[0.5, -0.5][i], reverb=0.7, barGain=c.g()) for i in range(2)]

Q = [["1:2 2:1 3:3", "4:2 5:1 6:3"], ["3:2 4:1 5:3", "6:3 7:3"], ["5:2 6:1 7:3", "1':3 2':3"], ["2:2 3:1 4:3", "5:6"]]
A = [["6:2 5:1 4:3", "3:3 1:3"], ["5:2 4:1 3:3", "2:3 1:3"], ["4:2 3:1 2:3", "1:6"], ["2':2 1':1 7:3", "6:3 5:3"]]
s1 = sum([Q[k % 4] for k in range(12)], [])
s2 = sum([Q[k % 4] if k % 2 == 0 else A[k % 4] for k in range(16)], [])
DOOR = ["1':3 7:2 6:1", "5:3 4:3", "3:2 2:1 1:3", "2:6", "1':3 7:2 6:1", "5:3 3:3", "4:2 5:1 6:3", "#7:6",
        "2':3 1':2 7:1", "6:3 5:3", "4:2 3:1 2:3", "3:6", "6:3 5:2 4:1", "3:3 2:3", "#1:3 2:3", "#3:6"]
play_melody(c, "探す1", s1, 4, "air", density=0.5, seed=4801)
play_melody(c, "鐘の音", ["R:6", "R:6", "5:6", "4:3 3:3"], 4, "air", density=0.0)
play_melody(c, "探す2", s2, 4, "air", density=0.7, seed=4802)
play_melody(c, "扉", DOOR, 4, "air", density=0.9, seed=4803)
play_melody(c, "開く", ["5:3 6:3", "7:3 1':3", "1':6", "7:6", "3':3 2':3", "1':3 7:3", "1':6", "1':6", "R:6", "R:6"], 4, "air",
            key=S.key.__class__("D", "major", 4), density=0.4, seed=4804)

B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D6")
    if n == "開く" and i >= 9: continue
    CELLO.bar(b, f"{nm(r)}:6")
    nv = 2 if n in ("問い", "探す1") else 3
    v = voice(ch, 55 if n not in ("扉", "開く") else 59, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n in ("問い", "探す1"):   # 竪琴の問い：上がって、止まる
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4], t[5])) + " R:2" if i % 2 == 0 else f"{nm(t[1])}:3 {nm(t[3])}:3")
    if n in ("鐘の音", "探す2", "扉"):
        # 鐘の響き（D と、短3度上の F）を、高い弦が引き継いでのばす。扉の最後で F が F♯（長3度）へ
        top = 77 if not (n == "扉" and i >= 14) else 78
        BELLSTR[0].bar(b, f"D6:6"); BELLSTR[1].bar(b, f"{nm(top)}:6")
    if n in ("探す2", "扉"):
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4], t[6 % len(t)], t[4], t[2])))
    if n in ("扉", "開く"):
        hv = voice(ch, 50, 3, spread=False)
        for j in range(3): HORN[j].bar(b, f"{nm(hv[j])}:6")
    if n == "開く":
        c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4], t[6 % len(t)], t[7 % len(t)], t[9 % len(t)]) * 2))
rich(c, choir_scenes=["扉", "開く"], pulse_scenes=["探す2", "扉"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の048。塔の床下の、秘密の入口。6/8・付点4分＝44、D ドリア→D 長調。笛の問い（上がって止まる）が、鐘の音をきっかけに、答え（下りて閉じる）に変わっていく。鐘の響き（D と短3度上の F）を高い弦が引き継ぎ、扉が開く所で長3度に変わる。",
       harm_scenes=None, tail_scene="開く", fill=False, pads=True, pad_scenes=["探す1", "鐘の音", "探す2", "扉", "開く"], floor=True)
BAR = 6 * 60 / BPM
ev = [{"t": round(c.s0["鐘の音"] * BAR + 0.2, 2), "file": "0135", "db": -22, "len": 10.0, "pan": 0.2, "seek": 0.0, "hp": 150, "lp": 7000}]
air = {"pre": 0.8, "tail": 8.0, "layers": [{"file": "0595", "db": -37, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8}], "events": ev,
       "fx": {"shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -24, "delay": 0.3, "lp": 2600, "rt": 5.0}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air048.json", "w"), ensure_ascii=False)
