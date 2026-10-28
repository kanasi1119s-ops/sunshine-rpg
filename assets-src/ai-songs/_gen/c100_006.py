# ケルト・フルート100曲「銀の笛と百の夜」006 夜の灯台守 The Keeper of the Night Light — 第2版（2026-10-28）
# イメージ: 日が落ちた岬。灯台守が灯りを一つずつともしていく。灯りがひとつ増えるたびに、音もひとつ増え、少しずつ高い所が光る。
#   すべての灯りがともると、光は海の遠くまで届く（竪琴の上昇アルペジオと、いちばん高いベル）。
# 形（台帳）: 主題と変奏。同じ16小節の節を5回。回ごとに楽器が1つ増え、音域が上がる。3/4・♩=56。B ドリア（3回目だけ D ドリアへ上がる）。
#   始め：低い弦／終わり：高いベルと竪琴の上昇アルペジオ。中盤（3回目）に山。
# 編曲の表（灯りの数＝楽器の数）:
#   暗い海  : 低い弦とチェロだけ
#   灯り0   : ＋笛（主題をそのまま）
#   灯り1   : ＋竪琴（ゆっくりした分散和音）。笛に装飾
#   灯り2   : ＋ピチカート。笛は8分で飾った変奏
#   灯り3   : D ドリアへ上がる。＋グロッケン＋笛の和声＋高い弦（山）
#   灯り4   : B に戻る。竪琴が上昇アルペジオ、グロッケンが高い所で光る。笛は主題のかけら
#   光      : いちばん高いベルと竪琴の上昇アルペジオ
import sys
from c100_common import *
from c100_v2 import *
from lm25_lib import tr_chord

S = Song("C100", "006-night-light-keeper", "夜の灯台守", "The Keeper of the Night Light", 56, 3, "B", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
TC = ["Bm", "E", "Bm", "F#m", "A", "E", "G", "Bm", "D", "A", "Bm", "E", "Bm", "D", "E", "Bm"]
S.scene("暗い海", 4, "intro", ["Bm", "Bm", "A", "Bm"])
S.scene("灯り0", 16, "verse", TC)
S.scene("灯り1", 16, "verse", TC)
S.scene("灯り2", 16, "verse", TC)
S.scene("灯り3", 16, "chorus", [tr_chord(x, 3) for x in TC])
S.scene("灯り4", 16, "verse", TC)
S.scene("光", 4, "outro", ["Bm", "A", "Bm", "Bm"])
NAMES = ["暗い海", "灯り0", "灯り1", "灯り2", "灯り3", "灯り4", "光"]

c = make(S, NAMES,
         [("暗い海", 0, 0.6), ("灯り0", 0, 0.6), ("灯り1", 0, 0.64), ("灯り2", 0, 0.7), ("灯り3", 0, 0.78), ("灯り3", 10, 0.9), ("灯り3", 15, 0.76),
          ("灯り4", 0, 0.7), ("灯り4", 15, 0.62), ("光", 0, 0.6), ("光", 3, 0.42)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="暗い海", passing=True, tension=False)
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.09, pan=0.15, reverb=0.45, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.055, pan=-0.35, reverb=0.4, barGain=c.g())
BELL = S.track("灯りのベル", "bell", patch="glockenspiel", volume=0.03, pan=0.35, reverb=0.7, barGain=c.g())

TH = ["5,:2 1:1", "2:1.5 3:0.5 4:1", "5:2 4:1", "3:3", "2:2 3:1", "4:1 3:1 2:1", "1:2 7,:1", "1:3",
      "3:2 4:1", "5:1.5 6:0.5 7:1", "1':2 7:1", "6:3", "5:2 4:1", "3:1 4:1 5:1", "4:2 2:1", "1:3"]
DIM = ["5,:1 7,:0.5 1:0.5 2:1", "2:0.5 3:0.5 4:0.5 3:0.5 4:1", "5:1 6:0.5 5:0.5 4:1", "3:2 2:0.5 3:0.5", "2:1 1:0.5 2:0.5 3:1", "4:0.5 5:0.5 4:0.5 3:0.5 2:1", "1:1 2:0.5 1:0.5 7,:1", "1:3",
       "3:1 2:0.5 3:0.5 4:1", "5:0.5 4:0.5 5:0.5 6:0.5 7:1", "1':1 2':0.5 1':0.5 7:1", "6:2 5:0.5 6:0.5", "5:1 6:0.5 5:0.5 4:1", "3:0.5 2:0.5 3:0.5 4:0.5 5:1", "4:1 3:0.5 4:0.5 2:1", "1:3"]
FRAG = ["5,:2 1:1", "2:3", "R:3", "R:3", "3:2 4:1", "5:3", "R:3", "R:3", "1':2 7:1", "6:3", "R:3", "R:3", "5:2 4:1", "3:3", "2:3", "1:3"]
play_melody(c, "灯り0", TH, 4, "air", density=0.3, seed=601)
play_melody(c, "灯り1", TH, 4, "air", density=0.9, seed=602)
play_melody(c, "灯り2", DIM, 4, "air", density=0.5, seed=603)
play_melody(c, "灯り3", TH, 4, "air", density=1.0, seed=604, lift=3)
play_melody(c, "灯り4", FRAG, 4, "air", density=0.7, seed=605)

B = S.beats; ORDER = NAMES
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lv = ORDER.index(n)          # 灯りの数
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D6")
    # 低い弦とチェロは、ずっと（灯台の土台）。回ごとに少しずつ高く開く
    v = voice(ch, 50 + 2 * min(lv, 5), 3, spread=True)
    for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
    CELLO.bar(b, f"{nm(r)}:3")
    if lv >= 2 and n != "光": c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)])) if n != "灯り4" else " ".join(f"{nm(x)}:0.5" for x in t[:6]))
    if lv >= 3 and n != "光" and i % 2 == 0: PIZZ.bar(b, f"R:1 {nm(t[1])}:1 {nm(t[2])}:1")
    if n == "灯り3":
        if i % 2 == 0: BELL.bar(b, f"{nm(tones(ch, 'C6', 'C7')[0])}:3")
        c.HARP2.bar(b, f"R:1 {nm(tones(ch, 'C5', 'C6')[0])}:2")
    if n == "灯り4" and i % 4 == 3: BELL.bar(b, f"R:1 {nm(tones(ch, 'C6', 'C7')[1])}:2")
    if n == "光":
        c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "B3", "B6")[2 * i:2 * i + 6]))   # 上昇アルペジオ（小節ごとに高く）
        if i >= 2: BELL.bar(b, f"{nm(tones(ch, 'C6', 'C7')[-1])}:3")
# 笛の和声は灯り3だけ
rich(c, choir_scenes=["灯り3"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.4 --side-hpf 160",
       "ケルト・フルート100曲の006（第2版）。灯台守が灯りを一つずつともす。3/4・♩=56、B ドリア。主題と変奏：同じ節を5回、回ごとに楽器が1つ増え、音域が上がる（3回目は D ドリアへ）。最後は竪琴の上昇アルペジオといちばん高いベル。",
       harm_scenes=None, tail_scene="光", fill=False, pads=True, pad_scenes=["灯り2", "灯り3", "灯り4", "光"])
