# ケルト・フルート100曲「銀の笛と百の夜」052 舟を押す Pushing Off — 明るく速めの曲（2026-10-29。第6章 霧の湖）
# イメージ: 湖のほとりに、古い小舟がつないである。エイラは浅瀬に入り、「せーの」で舟を押す。三度目で舟が水に乗り、
#   ふわりと浮く。乗りこんで漕ぎ出すと、岸がうしろへ遠ざかる。水をかく櫂のリズムが、だんだん軽くなる。
# 形: スリップ・ジグ（9/8。ゆれる3つの組）2曲のセット。最初に全員の3回の打ち（ストップタイム）で舟を押し、
#   舟が浮いた所から1曲目が流れだす。岸を離れる所で調が一音上がり（D→E）、2曲目へ。最後は、櫂の3回の打ちで止まる（始まりと鏡）。
#   9/8・8分＝300（付点4分＝100）。2周目と最後に山。
# ただひとつ: 「せーの」の3回の全員の打ちで始まり、岸を離れる瞬間に調が一音上がる。
# 編曲の表:
#   押す   : 全員の打ち（ボーラン・ギターの和音・低い弦・チェロ）×3。打ちのあいだは弦がふくらむ（押す力）
#   浮く   : 竪琴が下から上へ駆けあがり、笛の弱起
#   1曲目-1: 笛＋ボーラン（軽く）＋ギター＋竪琴のローヴィング・サム＋チェロ。B から弦
#   1曲目-2: 全員。竪琴の3音オスティナート、ピチカート、笛の和声（B）
#   岸を離れる: 2小節。B の和音（E の属和音）で弦がふくらみ、E へ
#   2曲目-1: E。ボーラン＋ギター＋竪琴＋チェロ＋弦、グロッケンが要所を光らせる
#   2曲目-2: 山。全員＋笛の和声
#   漕ぐ   : 櫂の3回の打ち×2 → 和音をのばして終わる
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 300   # 8分音符＝300（付点4分＝100）
S = Song("C100", "052-pushing-off", "舟を押す", "Pushing Off", BPM, 9, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
A1 = ["D", "G", "D", "A", "D", "G", "A", "D"]
B1 = ["D", "A", "G", "A", "D", "G", "A", "D"]
C2 = ["E", "E", "A", "B", "E", "A", "B", "E"]
D2 = ["E", "B", "A", "E", "E", "A", "B", "E"]
S.scene("押す", 3, "intro", ["D", "D", "A"])
S.scene("浮く", 1, "break", ["A"])
S.scene("1曲目-1", 32, "verse", A1 * 2 + B1 * 2)
S.scene("1曲目-2", 32, "verse", A1 * 2 + B1 * 2)
S.scene("岸を離れる", 2, "break", ["D", "B"])
S.scene("2曲目-1", 32, "chorus", C2 * 2 + D2 * 2)
S.scene("2曲目-2", 32, "chorus", C2 * 2 + D2 * 2)
S.scene("漕ぐ", 4, "outro", ["E", "E", "E", "E"])
NAMES = ["押す", "浮く", "1曲目-1", "1曲目-2", "岸を離れる", "2曲目-1", "2曲目-2", "漕ぐ"]

c = make(S, NAMES,
         [("押す", 0, 0.72), ("押す", 2, 0.82), ("浮く", 0, 0.7), ("1曲目-1", 0, 0.7), ("1曲目-1", 31, 0.74), ("1曲目-2", 0, 0.8), ("1曲目-2", 31, 0.86),
          ("岸を離れる", 0, 0.78), ("2曲目-1", 0, 0.82), ("2曲目-1", 31, 0.86), ("2曲目-2", 0, 0.9), ("2曲目-2", 31, 0.96), ("漕ぐ", 0, 0.9), ("漕ぐ", 3, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="押す", passing=True, tension=False)
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.06, pan=-0.4, reverb=0.35, barGain=c.g())
GLOCK = S.track("グロッケン", "bell", patch="glockenspiel", volume=0.028, pan=0.3, reverb=0.6, barGain=c.g())

# ---------- 旋律（度数・8分＝1。スリップ・ジグ：3つの組 2+1） ----------
T1A = ["1:2 3:1 5:2 3:1 6:2 5:1", "4:2 6:1 5:2 3:1 2:3",
       "1:2 3:1 5:2 1':1 7:2 6:1", "5:1 6:1 5:1 4:2 3:1 2:3",
       "1:2 3:1 5:2 3:1 6:2 1':1", "2':2 1':1 7:2 6:1 5:3",
       "6:1 5:1 4:1 3:2 4:1 5:1 3:1 2:1", "1:6 5,:1 6,:1 7,:1"]
T1B = ["1':2 2':1 3':2 1':1 2':2 7:1", "1':2 6:1 5:2 3:1 5:3",
       "6:2 7:1 1':2 6:1 7:2 5:1", "6:1 7:1 6:1 5:2 3:1 2:3",
       "1':2 2':1 3':2 5':1 4':2 2':1", "3':2 1':1 2':2 7:1 1':3",
       "6:1 5:1 4:1 3:2 4:1 5:1 3:1 2:1", "1:6 5,:1 6,:1 7,:1"]
T2C = ["5:2 1':1 7:2 5:1 6:2 4:1", "5:2 3:1 1:2 3:1 2:3",
       "5:2 1':1 7:2 2':1 1':2 6:1", "7:1 1':1 7:1 6:2 5:1 5:3",
       "5:2 1':1 7:2 5:1 6:2 1':1", "2':1 3':1 2':1 1':2 6:1 7:3",
       "1':1 7:1 6:1 5:2 4:1 3:1 2:1 7,:1", "1:6 5,:1 6,:1 7,:1"]
T2D = ["3:2 5:1 1':2 5:1 3':2 1':1", "2':2 7:1 5:2 7:1 2':3",
       "1':2 6:1 4:2 6:1 1':2 6:1", "5:1 6:1 5:1 3:2 1:1 2:3",
       "3:2 5:1 1':2 5:1 3':2 5':1", "4':2 2':1 7:2 5:1 6:3",
       "4:1 5:1 6:1 5:2 3:1 2:1 7,:1 2:1", "1:6 5,:1 6,:1 7,:1"]
KE = S.key.up(2)   # D→E（岸を離れる）
play_melody(c, "浮く", ["R:6 5,:1 6,:1 7,:1"], 4, "jig", density=0)
play_melody(c, "1曲目-1", T1A + T1A + T1B + T1B, 4, "jig", density=0.6, seed=5201)
play_melody(c, "1曲目-2", T1A + T1A + T1B + T1B, 4, "jig", density=1.0, seed=5202)
play_melody(c, "岸を離れる", ["1:9", "R:6 5,:1 6,:1 7,:1"], 4, "jig", key=KE, density=0)
play_melody(c, "2曲目-1", T2C + T2C + T2D + T2D, 4, "jig", key=KE, density=0.8, seed=5203)
play_melody(c, "2曲目-2", T2C + T2C + T2D + T2D[:7] + ["1:9"], 4, "jig", key=KE, density=1.1, seed=5204)
play_melody(c, "漕ぐ", ["5:3 5:3 5:3", "1':3 1':3 1':3", "1':9", "R:9"], 4, "jig", key=KE, density=0)

# ---------- 伴奏 ----------
drive(c, ["1曲目-1", "1曲目-2", "2曲目-1", "2曲目-2"], kind="slipjig", soft_scenes=["1曲目-1"])
B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "押す":   # 「せーの」の打ち：全員で1拍目、あとは弦がふくらむ
        c.DRUM.bar(b, "D3:3! R:6"); strum(c.GTR, b, B, ch, [(0, 3, "d", "!")])
        c.LOW.bar(b, f"{nm(r)}:3 R:6")
        v = voice(ch, 50, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
        c.HARP.bar(b, f"{nm(r + 12)}:3 R:6")
        continue
    if n == "浮く":
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "A2", "A5")[:9]))
        v = voice(ch, 52, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
        c.LOW.bar(b, f"{nm(r)}:9")
        continue
    if n == "岸を離れる":
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
        c.LOW.bar(b, f"{nm(r)}:9"); strum(c.GTR, b, B, ch, [(0, 9, "d", ",")])
        c.DRUM.bar(b, "D3:3, R:6" if i == 0 else "R:6 D3:1, D3:1, A3:1")
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "B2", "B5")[:9]))
        continue
    if n == "漕ぐ":   # 櫂の3回の打ち（始まりと鏡）→ 和音をのばす
        if i < 2:
            c.DRUM.bar(b, "D3:3! D3:3 D3:3!"); strum(c.GTR, b, B, ch, [(0, 2.5, "d", "!"), (3, 2.5, "d", ""), (6, 2.5, "d", "!")])
            c.LOW.bar(b, f"{nm(r)}:3 {nm(r)}:3 {nm(r)}:3")
        else:
            if i == 2: strum(c.GTR, b, B, ch, [(0, 9, "d", "!")]); c.DRUM.bar(b, "D3:9!")
            c.LOW.bar(b, f"{nm(r)}:9")
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
        if i == 3: c.HARP.bar(b, f"{nm(tones(ch, 'E5', 'E6')[0])}:9")
        continue
    c.LOW.bar(b, f"{nm(r)}:6 {nm(r + 7)}:3")
    if n == "1曲目-1":
        roving_thumb(c.HARP, b, B, ch, up=(i % 2 == 0))
        if i >= 16:
            v = voice(ch, 54, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
    else:
        harp_ostinato(c.HARP, b, B, tones(ch, "D4" if n.startswith("1") else "E4", "E5")[:3])
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:9")
        if n in ("1曲目-2", "2曲目-2"): PIZZ.bar(b, f"{nm(r + 12)}:1 R:2 {nm(r + 19)}:1 R:2 {nm(r + 12)}:1 R:2")
        if n.startswith("2") and i % 4 == 0: GLOCK.bar(b, f"{nm(tones(ch, 'C6', 'C7')[0])}:3 R:6")
rich(c, choir_scenes=["1曲目-2", "2曲目-2"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
thick(c); sparkle(c)   # 2026-10-29: 速い曲の厚さ（023 7.27→7.53・025 7.26→7.66）＋高いきらめき
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の052（明るく速めの曲）。湖のほとりで舟を押し、漕ぎ出す。9/8 のスリップ・ジグ2曲のセット（付点4分＝100）。全員の「せーの」の3回の打ちで舟を押し、舟が浮いた所から1曲目が流れだす。岸を離れる所で調が D→E へ上がり、最後は櫂の3回の打ちで止まる。",
       harm_scenes=None, tail_scene="漕ぐ", fill=False, pads=False, floor=True)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0823", "db": -38, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.45, "fade": 5}],
       "fx": {"shimmer": {"db": -30, "rt": 5.0}, "far": {"db": -27, "delay": 0.18, "lp": 3200, "rt": 3.0}}, "intro_db": 4.0}
json.dump(air, open("/tmp/cel/w/air052.json", "w"), ensure_ascii=False)
