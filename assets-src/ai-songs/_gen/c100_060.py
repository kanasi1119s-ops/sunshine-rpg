# ケルト・フルート100曲「銀の笛と百の夜」060 対岸 The Far Shore — 明るく速めの曲（2026-10-29。第6章 霧の湖）
# イメージ: 夜が明け、霧が晴れる。目の前に、対岸の岸辺と、その向こうの村の屋根。エイラは舟をこぎ寄せ、
#   霧の中で口ずさんでいた節が、いつのまにか踊りの節になっている。舟が岸に着き、乾いた地面を3歩、踏みしめる。
# 形: 霧（ポルカの節を倍の長さでゆっくり、笛ひとり）→ 晴れる → ポルカ AABB ×3（つなぎをはさむ。3周目にもう一度 A）→ 足音。
#   2/4・♩=116・E ミクソリディア。終盤に安堵の山。
# ただひとつ: 霧の中ではゆっくり歌っていた節が、霧が晴れると、同じ節のまま踊りだす。最後は音楽が止まり、枠太鼓の3歩（地面を踏む足音）で終わる。
# 編曲の表:
#   霧    : 笛ひとり（倍の長さ）。うすい弦とチェロ、竪琴がときどき
#   晴れる: ボーランの弱起
#   ポルカ1: 笛＋ボーラン（軽く）＋ギター＋チェロ。B から弦と竪琴
#   ポルカ2: 全員。竪琴の3音オスティナート、ピチカート
#   つなぎ: 弦のドローンとギター。笛は休み、竪琴の分散和音
#   ポルカ3: 山。笛の和声、グロッケン、内声
#   足音  : 全員の和音で止め、弦の響きの中で、枠太鼓の3歩
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 116
S = Song("C100", "060-the-far-shore", "対岸", "The Far Shore", BPM, 2, "E", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["E", "A", "A", "D", "E", "D", "E", "E", "E", "A", "E", "Bm", "A", "E", "E", "E"]
BC = ["E", "A", "D", "D", "E", "A", "E", "E", "E", "A", "D", "D", "E", "A", "E", "E"]
TA = ["1:0.5 3:0.5 5:0.5 3:0.5", "4:0.5 6:0.5 5:1", "1':0.5 7:0.5 6:0.5 5:0.5", "6:0.5 4:0.5 2:1",
      "1:0.5 3:0.5 5:0.5 1':0.5", "7:0.5 6:0.5 5:0.5 4:0.5", "3:0.5 2:0.5 3:0.5 7,:0.5", "1:1 1:1",
      "1:0.5 3:0.5 5:0.5 3:0.5", "4:0.5 6:0.5 5:1", "1':0.5 2':0.5 3':0.5 1':0.5", "2':0.5 7:0.5 5:1",
      "6:0.5 7:0.5 1':0.5 6:0.5", "5:0.5 4:0.5 3:0.5 2:0.5", "3:0.5 5:0.5 2:0.5 7,:0.5", "1:1 R:1"]
TB = ["5:0.5 6:0.5 5:0.5 3:0.5", "5:0.5 1':0.5 1':1", "7:0.5 1':0.5 2':0.5 7:0.5", "6:0.5 4:0.5 4:1",
      "5:0.5 6:0.5 5:0.5 3:0.5", "2:0.5 3:0.5 4:1", "5:0.5 4:0.5 3:0.5 2:0.5", "3:1 R:1",
      "5:0.5 6:0.5 5:0.5 3:0.5", "5:0.5 1':0.5 1':1", "7:0.5 1':0.5 2':0.5 7:0.5", "6:0.5 4:0.5 4:1",
      "3':0.5 2':0.5 1':0.5 7:0.5", "6:0.5 5:0.5 4:0.5 6:0.5", "5:0.5 3:0.5 2:0.5 7,:0.5", "1:1 R:1"]
def half(bars, beats=2):
    """同じ節を倍の長さで（1小節が2小節に）"""
    out = []
    for s in bars:
        a, b_, acc = [], [], 0.0
        for tok in s.split():
            d, L = tok.split(":"); L2 = float(L) * 2
            if acc + L2 <= beats + 1e-6: a.append(f"{d}:{L2:g}"); acc += L2
            elif acc < beats - 1e-6: a.append(f"{d}:{beats - acc:g}"); b_.append(f"{d}:{L2 - (beats - acc):g}"); acc = beats
            else: b_.append(f"{d}:{L2:g}")
        out += [" ".join(a), " ".join(b_) or f"R:{beats}"]
    return out
MIST = half(TA[:8])
MC = [x for ch in AC[:8] for x in (ch, ch)]
S.scene("霧", 16, "intro", MC)
S.scene("晴れる", 2, "break", ["B", "B"])
S.scene("ポルカ1", 64, "verse", AC * 2 + BC * 2)
S.scene("ポルカ2", 64, "verse", AC * 2 + BC * 2)
S.scene("つなぎ", 8, "break", ["A", "A", "D", "D", "A", "A", "B", "B"])
S.scene("ポルカ3", 80, "chorus", AC * 2 + BC * 2 + AC)
S.scene("足音", 4, "outro", ["E", "E", "E", "E"])
NAMES = ["霧", "晴れる", "ポルカ1", "ポルカ2", "つなぎ", "ポルカ3", "足音"]

c = make(S, NAMES,
         [("霧", 0, 0.62), ("霧", 15, 0.66), ("晴れる", 0, 0.66), ("ポルカ1", 0, 0.72), ("ポルカ1", 63, 0.78), ("ポルカ2", 0, 0.82), ("ポルカ2", 63, 0.86),
          ("つなぎ", 0, 0.72), ("ポルカ3", 0, 0.86), ("ポルカ3", 60, 0.96), ("ポルカ3", 79, 0.92), ("足音", 0, 0.86), ("足音", 3, 0.64)],
         {}, flute_gain={n: 1.12 for n in NAMES}, intro="霧", passing=True, tension=False)
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.06, pan=-0.4, reverb=0.35, barGain=c.g())
GLOCK = S.track("グロッケン", "bell", patch="glockenspiel", volume=0.028, pan=0.3, reverb=0.6, barGain=c.g())
STEP = S.track("足音（枠太鼓）", "guitar", patch="frameDrum", volume=0.14, pan=0.0, reverb=0.4, modulate=False)

play_melody(c, "霧", MIST, 4, "air", density=0.4, seed=6001)
play_melody(c, "晴れる", ["R:2", "R:1 5,:0.5 7,:0.5"], 4, "reel", density=0)
play_melody(c, "ポルカ1", TA + TA + TB + TB, 4, "reel", density=0.5, seed=6002)
play_melody(c, "ポルカ2", TA + TA + TB + TB, 4, "reel", density=0.9, seed=6003)
play_melody(c, "つなぎ", ["R:2"] * 6 + ["R:2", "R:1 5,:0.5 7,:0.5"], 4, "reel", density=0)
play_melody(c, "ポルカ3", TA + TA + TB + TB + TA[:15] + ["1:2"], 4, "reel", density=1.1, seed=6004)
play_melody(c, "足音", ["1:1 R:1", "R:2", "R:2", "R:2"], 4, "reel", density=0)

drive(c, ["ポルカ1", "ポルカ2", "ポルカ3"], kind="polka", soft_scenes=["ポルカ1"])
B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "霧":
        v = voice(ch, 52, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:2")
        c.LOW.bar(b, f"{nm(r)}:2")
        if i % 2 == 0: c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "E3", "E5")[:4]))
        continue
    if n == "晴れる":
        c.DRUM.bar(b, "R:2" if i == 0 else "R:1 D3:0.25, D3:0.25, A3:0.5")
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:2")
        c.LOW.bar(b, f"{nm(r)}:2")
        continue
    if n == "つなぎ":
        drone(c.STR[:2], b, B, 57 if ch == "A" else 50 if ch == "D" else 59)
        strum(c.GTR, b, B, ch, [(0, 2, "d", ",")] if i % 2 == 0 else [(0, 1, "d", ","), (1, 1, "u", ",")])
        c.LOW.bar(b, f"{nm(r)}:2")
        c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "A3", "A5")[i % 2 * 2: i % 2 * 2 + 4]))
        continue
    if n == "足音":   # 全員の和音で止め、響きの中で3歩
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:2")
        if i == 0:
            strum(c.GTR, b, B, ch, [(0, 1, "d", "!")]); c.DRUM.bar(b, "D3:1! R:1"); c.LOW.bar(b, f"{nm(r)}:2")
            c.HARP.bar(b, " ".join(f"{nm(x)}:0.125" for x in tones(ch, "E3", "E6")[:8]) + " R:1")
        else:
            STEP.bar(b, "D3:1 R:1" if i < 3 else "D3:2")
            c.LOW.bar(b, f"{nm(r)}:2")
        continue
    c.LOW.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1")
    part_b = (i // 16) % 4 >= 2 if i < 64 else False
    if n == "ポルカ1":
        if part_b:
            v = voice(ch, 55, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:2")
            c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "E4", "E5")[:4]))
        else:
            v = voice(ch, 52, 2, spread=True)
            for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:2")
    else:
        harp_ostinato(c.HARP, b, B, tones(ch, "E4", "E5")[:3])
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:2")
        PIZZ.bar(b, f"{nm(r + 12)}:0.5 R:0.5 {nm(r + 19)}:0.5 R:0.5")
        if n == "ポルカ3" and i % 8 == 0: GLOCK.bar(b, f"{nm(tones(ch, 'C6', 'C7')[0])}:1 R:1")
rich(c, choir_scenes=["ポルカ3"], pulse_scenes=[], guitar=False, pizz=False, inner=False)
thick(c); sparkle(c)   # 2026-10-29: 速い曲の厚さ（023 7.27→7.53・025 7.26→7.66）＋高いきらめき
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の060（明るく速めの曲）。霧が晴れ、対岸の岸に舟が着く。2/4・♩=116、E ミクソリディア。霧の中では笛ひとりでゆっくり歌っていた節が、霧が晴れると同じ節のままポルカで踊りだす（AABB ×3）。最後は音楽が止まり、枠太鼓の3歩（地面を踏む足音）で終わる。",
       harm_scenes=None, tail_scene="足音", fill=False, pads=False, floor=True)
air = {"pre": 0.4, "tail": 5.0, "layers": [{"file": "0691", "db": -39, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.45, "fade": 5}],
       "fx": {"shimmer": {"db": -30, "rt": 5.0}, "far": {"db": -27, "delay": 0.18, "lp": 3200, "rt": 3.0}}, "intro_db": 5.0}
json.dump(air, open("/tmp/cel/w/air060.json", "w"), ensure_ascii=False)
