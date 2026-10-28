# ケルト・フルート100曲「銀の笛と百の夜」001 銀の笛 The Silver Flute — 第2版（2026-10-28）
# イメージ: 夕暮れの灯台の部屋。少女エイラが祖父の古い箱を開け、銀の笛を取り出す。口に当てる前の、ひとつの息。
#   はじめて吹く節は、問いかけのように「1・3・4」と上がって止まる。2回目は少し慣れて、3回目（B）で窓の外の海へ伸びていく。
#   最後は竪琴が1音だけ、箱のふたを閉じるように鳴る。山なし・ごく静か（静の型、点数 7.2 以上をめざす）。
# 形（台帳）: スロー・エア AABA（テンポのゆれ）→2周目は短く ABA。4/4・♩=54。E ドリア。
# 編曲の表:
#   前置き : 息の音（空気の層で作る）→竪琴の根音1つ
#   1周目  : 笛＋竪琴の根音のドローン（1小節に1〜2回）＋弦とチェロのうすいドローン（E と B）。空間で上下を満たす
#   2周目  : 竪琴がゆっくりした分散和音に、チェロが笛と反対向きの対旋律、B ではホルンの長い和音が遠くで温める
#   余韻   : 竪琴の E の1音だけ
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "001-silver-flute", "銀の笛", "The Silver Flute", 54, 4, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"rubato": 0.4, "human": 0.45})
A1c = ["Em", "Em", "D", "D", "Em", "A", "D", "Em"]
A2c = ["Em", "Em", "D", "D", "Em", "A", "D", "Em"]
Bc = ["G", "D", "Em", "A", "G", "D", "Bm", "Em"]
S.scene("前置き", 2, "intro", ["Em", "Em"])
S.scene("1周目", 32, "verse", A1c + A2c + Bc + A2c)
S.scene("2周目", 24, "verse", A1c + Bc + A2c)
S.scene("余韻", 3, "outro", ["Em", "Em", "Em"])
NAMES = ["前置き", "1周目", "2周目", "余韻"]

c = make(S, NAMES,
         [("前置き", 0, 0.6), ("1周目", 0, 0.62), ("1周目", 20, 0.7), ("1周目", 31, 0.62), ("2周目", 0, 0.66), ("2周目", 12, 0.78), ("2周目", 23, 0.62),
          ("余韻", 0, 0.5), ("余韻", 2, 0.35)],
         {}, flute_gain={n: 1.25 for n in NAMES}, intro="前置き", passing=True, tension=False)
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.09, pan=0.2, reverb=0.5, barGain=c.g())
DR = [S.track(f"ドローン（弦）{i + 1}", "strings", patch="slowStrings", volume=0.05, pan=[-0.5, 0.5][i], reverb=0.65, barGain=c.g()) for i in range(2)]
HORN = S.track("ホルン（遠く）", "brass", patch="horn", volume=0.05, pan=-0.3, reverb=0.7, breath=False, attack=0.4, release=1.0, bright=-0.6, barGain=c.g())

# ---------- 旋律（E ドリア・4/4。問いの動機「1・3・4」） ----------
A1 = ["R:1 1:1 3:1.5 4:0.5", "5:3 4:0.5 3:0.5", "2:1.5 3:0.5 4:1 2:1", "5,:3.5 R:0.5",
      "R:1 1:1 3:1.5 4:0.5", "5:2 7:1.5 6:0.5", "5:1 4:1 3:1 2:1", "1:3.5 R:0.5"]
A2 = ["R:1 1:1 3:1.5 4:0.5", "5:3 4:0.5 3:0.5", "2:1.5 3:0.5 4:1 2:1", "5,:3.5 R:0.5",
      "R:1 1:1 3:1.5 4:0.5", "5:1 6:1 7:1 1':1", "7:1.5 5:0.5 4:1 2:1", "1:4"]
BL = ["3:1 5:1 7:1.5 1':0.5", "2':3 1':0.5 7:0.5", "6:1.5 7:0.5 1':1 5:1", "6:3.5 R:0.5",
      "7:1 1':1 2':1.5 3':0.5", "2':2 1':1 7:1", "5:1 4:1 3:1 2:1", "1:3.5 R:0.5"]
play_melody(c, "1周目", A1 + A2 + BL + A2, 4, "air", density=0.8, seed=101)
play_melody(c, "2周目", A1 + BL + A2[:7] + ["1:4"], 4, "air", density=1.0, seed=102)

# ---------- 伴奏 ----------
B = S.beats; prev = 52
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    t = tones(ch, "E3", "E5"); r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "前置き":
        if i == 1: c.HARP.bar(b, "R:2 E3:2")
        DR[0].bar(b, "E3:4")
        continue
    if n in ("1周目", "2周目"):
        drone(DR, b, B, 52); CELLO.bar(b, "E2:4") if n == "1周目" else None
    if n == "1周目":
        c.HARP.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if i % 2 == 0 else f"{nm(r)}:4")
    elif n == "2周目":
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2])))
        cand = [m for m in range(40, 57) if m % 12 in chord_pcs(ch)]
        a = min(cand, key=lambda m: abs(m - prev)); z = min([m for m in cand if m != a], key=lambda m: abs(m - a))
        CELLO.bar(b, f"{nm(a)}:2 {nm(z)}:2"); prev = z
        if 8 <= i < 16: HORN.bar(b, f"{nm(tones(ch, 'G3', 'D4')[0])}:4")
        if i % 8 == 7: c.HARP2.bar(b, f"R:2 {nm(tones(ch, 'E5', 'E6')[0])}:2")
    elif n == "余韻":
        drone(DR, b, B, 52)
        if i == 0: c.HARP.bar(b, "E4:4")       # 箱のふたを閉じるように、竪琴の1音

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の001（第2版）。夕暮れ、祖父の箱から銀の笛を取り出す。E ドリア・4/4・♩=54、テンポのゆれ。息の音→問いの動機「1・3・4」のスロー・エア AABA→2周目は竪琴とチェロが答える→竪琴の1音。",
       harm_scenes=None, tail_scene="余韻", fill=False, pads=True, pad_scenes=["2周目"])
