# ケルト・フルート100曲「銀の笛と百の夜」025 飛び石 Stepping Stones — 第2版（明るく速めの曲）（2026-10-28）
# イメージ: 小川にならんだ飛び石を、ぴょん、ぴょんと渡っていく。跳ぶたびに足もとで水がはねる。途中でちょっとよろけて（短調の8小節）、
#   また元気に跳んでいく。最後は対岸に着いて、みんなで「ぴょん」と止まる。
# 形（台帳）: ポルカ（2/4・スタッカートの軽い跳び）。2曲のセット（C のポルカ → F のポルカ → C のポルカを全音上の D で）。
#   2/4・♩=88。始め：ひと跳び／終わり：対岸（全員でぴょんと止まる）。終盤に山。
# 編曲の表:
#   ひと跳び : 笛のひと跳び（3音）と水のはね
#   ポルカ1-1: 笛＋ギターの裏拍（ズン・チャ）＋ピチカートの低音
#   ポルカ1-2: ＋竪琴。笛は装飾つき
#   よろけ  : 短調（Am）の8小節。ピチカートだけ、水の音
#   ポルカ2-1: F のポルカ。チェロ
#   ポルカ2-2: ＋弦
#   ポルカ1-3: D へ上がって最初のポルカが戻る（山）
#   対岸    : 全員で「ぴょん」と止まる
import sys, json
from c100_common import *
from c100_v2 import *
from lm25_lib import tr_chord

BPM = 88
S = Song("C100", "025-stepping-stones", "飛び石", "Stepping Stones", BPM, 2, "C", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
P1A = ["C", "C", "F", "C", "G", "C", "G", "C"]; P1B = ["F", "F", "C", "F", "C", "G", "G", "C"]
P2A = ["F", "C", "Bb", "F", "F", "C", "Bb", "F"]; P2B = ["Bb", "Bb", "F", "F", "Bb", "Gm", "C", "F"]
S.scene("ひと跳び", 2, "intro", ["C", "C"])
S.scene("ポルカ1-1", 32, "verse", P1A * 2 + P1B * 2)
S.scene("ポルカ1-2", 32, "verse", P1A * 2 + P1B * 2)
S.scene("よろけ", 8, "break", ["Am", "Am", "Dm", "Am", "F", "G", "C", "C"])
S.scene("ポルカ2-1", 32, "verse", P2A * 2 + P2B * 2)
S.scene("ポルカ2-2", 32, "chorus", P2A * 2 + P2B * 2)
S.scene("ポルカ1-3", 32, "chorus", [tr_chord(x, 2) for x in P1A * 2 + P1B * 2])
S.scene("対岸", 4, "outro", ["D", "D", "D", "D"])
NAMES = ["ひと跳び", "ポルカ1-1", "ポルカ1-2", "よろけ", "ポルカ2-1", "ポルカ2-2", "ポルカ1-3", "対岸"]

c = make(S, NAMES,
         [("ひと跳び", 0, 0.66), ("ポルカ1-1", 0, 0.68), ("ポルカ1-2", 0, 0.74), ("よろけ", 0, 0.62), ("ポルカ2-1", 0, 0.74), ("ポルカ2-2", 0, 0.8),
          ("ポルカ1-3", 0, 0.86), ("ポルカ1-3", 28, 0.95), ("対岸", 0, 0.9), ("対岸", 3, 0.5)],
         {}, flute_gain={n: 1.05 for n in NAMES}, intro="ひと跳び", passing=True, tension=False)
GT = S.track("ギター（裏拍）", "guitar", patch="nylonGuitar", volume=0.085, pan=0.35, reverb=0.3, barGain=c.g())
GT2 = S.track("ギター（裏拍2）", "guitar", patch="nylonGuitar", volume=0.07, pan=0.42, reverb=0.3, barGain=c.g())
PIZZ = S.track("ピチカート（低音）", "strings", patch="pizzicato", volume=0.075, pan=-0.2, reverb=0.3, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.15, reverb=0.35, barGain=c.g())
DRUM = S.track("枠太鼓", "guitar", patch="frameDrum", volume=0.1, pan=-0.1, reverb=0.3, modulate=False, barGain=c.g())

def st(bars): return [" ".join(t + ("'" if float(t.split(":")[1]) <= 0.5 and not t.startswith("R") else "") for t in s.split()) for s in bars]
A1 = ["5:0.5 3:0.5 5:0.5 3:0.5", "1':1 5:1", "4:0.5 6:0.5 4:0.5 6:0.5", "5:1 3:1", "2:0.5 4:0.5 6:0.5 4:0.5", "3:0.5 5:0.5 1':1", "7:0.5 6:0.5 5:0.5 4:0.5", "3:1 1:1"]
B1 = ["1':0.5 7:0.5 6:0.5 7:0.5", "1':1 6:1", "5:0.5 6:0.5 7:0.5 5:0.5", "6:1 4:1", "3:0.5 4:0.5 5:0.5 6:0.5", "7:0.5 6:0.5 5:1", "4:0.5 2:0.5 7,:0.5 2:0.5", "1:1 R:1"]
A2 = ["1:0.5 3:0.5 5:0.5 1':0.5", "7:1 5:1", "6:0.5 5:0.5 4:0.5 6:0.5", "5:1 2:1", "3:0.5 5:0.5 1':0.5 3':0.5", "2':1 7:1", "1':0.5 6:0.5 4:0.5 2:0.5", "1:1 5,:1"]
B2 = ["4:0.5 4:0.5 6:0.5 1':0.5", "6:1 4:1", "3:0.5 3:0.5 5:0.5 1':0.5", "5:1 3:1", "2:0.5 4:0.5 6:0.5 2':0.5", "1':1 6:1", "5:0.5 4:0.5 3:0.5 2:0.5", "1:1 R:1"]
P1 = st(A1 + A1 + B1 + B1); P2 = st(A2 + A2 + B2 + B2)
KF = S.key.__class__("F", "major", 4)
play_melody(c, "ひと跳び", ["R:1 5:0.5' 1':0.5'", "R:2"], 5, "air", density=0)
play_melody(c, "ポルカ1-1", P1, 5, "reel", density=0.4, seed=2501)
play_melody(c, "ポルカ1-2", P1, 5, "reel", density=0.9, seed=2502)
play_melody(c, "よろけ", ["3:1 2:1", "1:2", "4:1 3:1", "2:2", "R:2", "R:1 5:0.5 7:0.5", "1':1 R:1", "R:2"], 5, "air", density=0.3, seed=2503,
            key=S.key.__class__("C", "major", 5))
play_melody(c, "ポルカ2-1", P2, 4, "reel", key=KF, density=0.6, seed=2504)
play_melody(c, "ポルカ2-2", P2, 4, "reel", key=KF, density=1.0, seed=2505)
play_melody(c, "ポルカ1-3", P1, 5, "reel", density=1.0, seed=2506, lift=2)
play_melody(c, "対岸", ["1:0.5' R:0.5 5,:0.5' R:0.5", "1:0.5! R:1.5", "R:2", "R:2"], 5, "air", density=0, lift=2)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "E3", "E5")
    if n == "ひと跳び":
        if i == 1: PIZZ.bar(b, f"{nm(r)}:0.5 R:0.5 {nm(r + 7)}:0.5 R:0.5"); GT.bar(b, f"R:0.5 {nm(t[1])}:0.5' R:0.5 {nm(t[1])}:0.5'"); DRUM.bar(b, "D3:0.5, R:0.5 D3:0.5, A3:0.5,")
        continue
    if n == "よろけ":
        PIZZ.bar(b, f"{nm(r)}:1 R:1" if i % 2 == 0 else f"R:1 {nm(t[2])}:1")
        v = voice(ch, 55, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:2")
        continue
    if n == "対岸":
        if i == 0:
            PIZZ.bar(b, f"{nm(r)}:0.5 R:0.5 {nm(r + 7)}:0.5 R:0.5"); GT.bar(b, f"R:0.5 {nm(t[1])}:0.5 R:0.5 {nm(t[1])}:0.5")
        if i == 1:   # ぴょん：全員で1拍目
            PIZZ.bar(b, f"{nm(r)}:0.5! R:1.5"); GT.bar(b, f"{nm(t[1])}:0.5! R:1.5"); GT2.bar(b, f"{nm(t[2])}:0.5! R:1.5"); DRUM.bar(b, "D3:0.5! R:1.5")
            c.HARP.bar(b, f"{nm(r + 12)}:2"); CELLO.bar(b, f"{nm(r)}:0.5 R:1.5")
        continue
    PIZZ.bar(b, f"{nm(r)}:0.5 R:0.5 {nm(r + 7)}:0.5 R:0.5")
    GT.bar(b, f"R:0.5 {nm(t[1])}:0.5' R:0.5 {nm(t[1])}:0.5'"); GT2.bar(b, f"R:0.5 {nm(t[2])}:0.5' R:0.5 {nm(t[2])}:0.5'")
    DRUM.bar(b, "D3:0.5! A3:0.5, D3:0.5 A3:0.5," if n != "ポルカ1-1" or i >= 16 else "D3:0.5, R:0.5 D3:0.5, R:0.5")   # 跳ぶ足どり
    if n in ("ポルカ1-1", "ポルカ2-1"): c.HARP2.bar(b, f"R:1 {nm(t[2] + 12)}:0.5 {nm(t[1] + 12)}:0.5")   # 水のはね
    if n in ("ポルカ1-2", "ポルカ2-1"):
        v = voice(ch, 53, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:2")
    if n == "ポルカ1-2": CELLO.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1")
    if n in ("ポルカ1-2", "ポルカ2-2", "ポルカ1-3"): c.HARP.bar(b, f"{nm(t[0] + 12)}:0.5 {nm(t[2] + 12)}:0.5 {nm(t[1] + 12)}:0.5 {nm(t[2] + 12)}:0.5")
    if n in ("ポルカ2-1", "ポルカ2-2", "ポルカ1-3"): CELLO.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1")
    if n in ("ポルカ2-2", "ポルカ1-3"):
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:2")
rich(c, choir_scenes=["ポルカ2-2", "ポルカ1-3"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.26 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の025（第2版・明るく速めの曲）。小川の飛び石を、ぴょんぴょん渡る。ポルカ（2/4・♩=88）のセット：C のポルカ→よろける短調の8小節→F のポルカ→D へ上がって最初のポルカ。最後は対岸で全員がぴょんと止まる。",
       harm_scenes=None, tail_scene="対岸", fill=False, pads=True, pad_scenes=["ポルカ1-2", "ポルカ2-1", "ポルカ2-2", "ポルカ1-3"])
# 空気：跳ぶたびの水のはね（小川の録音を短く切って、よろけの所と所々に）
BAR = 2 * 60 / BPM
ev = [{"t": round((c.s0["ひと跳び"] + 1) * BAR, 2), "file": "0864", "db": -20, "len": 0.8, "pan": 0.2, "seek": 3.0, "hp": 300, "lp": 9000}]
for j in range(0, 8, 2): ev.append({"t": round((c.s0["よろけ"] + j) * BAR + 0.3, 2), "file": "0864", "db": -22, "len": 0.9, "pan": [-0.3, 0.3][j % 4 // 2], "seek": 5.0 + j, "hp": 300, "lp": 9000})
for sc in ("ポルカ1-1", "ポルカ2-1"):
    for j in range(7, 32, 8): ev.append({"t": round((c.s0[sc] + j) * BAR + 0.5, 2), "file": "0864", "db": -27, "len": 0.7, "pan": 0.35, "seek": 9.0 + j, "hp": 300, "lp": 9000})
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0213", "db": -36, "hp": 200, "lp": 8000, "wide": 0.014, "duck": 0.45, "fade": 6}], "events": ev,
       "fx": {"glass": {"hz": [523.3, 1046.5, 1568.0], "db": -31, "rt": 5.0, "start": 4}, "shimmer": {"db": -30, "rt": 6.0},
              "far": {"db": -27, "delay": 0.2, "lp": 3000, "rt": 3.0}, "haze": {"db": -30, "rt": 6.0}}, "intro_db": 8.5}
json.dump(air, open("/tmp/cel/w/air025.json", "w"), ensure_ascii=False)
