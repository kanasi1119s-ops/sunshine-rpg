# ケルト・フルート100曲「銀の笛と百の夜」005 小舟の鈴 The Little Boat Bell（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 港で、小舟の鈴が鳴る。呼ぶ（本物の小さな鈴の録音）→笛が応える→こんどは笛が呼ぶ→鈴が応える→遠ざかり、笛が鈴の音を真似て消える。
# 型: 鈴の音程（曲の和音の音に合わせて高さを変えた録音）に、笛が寄り添う。始め：きらめくチャイム／終わり：笛が鈴を真似て消える。山なし。
# 強さ: 鈴(pp)→呼ぶ1(p)→応える(p→mp)→呼ぶ2(mp)→遠ざかる(p→ppp)→終わり(ppp)
import sys, json
from c100_common import *

BPM = 66
S = Song("C100", "005-little-boat-bell", "小舟の鈴", "The Little Boat Bell", BPM, 4, "G", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("鈴", 4, "intro", ["G", "F", "C", "G"])
S.scene("呼ぶ1", 16, "verse", ["G", "F", "C", "G", "Am", "F", "C", "G", "Em", "F", "C", "G", "G", "F", "Dm", "G"])
S.scene("応える", 16, "verse", ["C", "G", "Am", "F", "C", "G", "Dm", "G", "Em", "F", "C", "G", "Am", "F", "Dm", "G"])
S.scene("呼ぶ2", 16, "chorus", ["G", "F", "C", "G", "Am", "G", "F", "C", "Em", "F", "C", "G", "F", "C", "Dm", "G"])
S.scene("遠ざかる", 14, "verse", ["Em", "F", "C", "G", "Am", "F", "C", "G", "Em", "F", "C", "G", "Dm", "G"])
S.scene("終わり", 8, "outro", ["G", "G", "G", "G", "G", "G", "G", "G"])
NAMES = ["鈴", "呼ぶ1", "応える", "呼ぶ2", "遠ざかる", "終わり"]

c = make(S, NAMES,
         [("鈴", 0, 0.72), ("呼ぶ1", 0, 0.66), ("応える", 0, 0.72), ("応える", 15, 0.78), ("呼ぶ2", 0, 0.8), ("呼ぶ2", 12, 0.86),
          ("遠ざかる", 0, 0.6), ("遠ざかる", 13, 0.4), ("終わり", 0, 0.4), ("終わり", 7, 0.28)],
         {"呼ぶ1": 0.58, "応える": 0.58, "呼ぶ2": 0.6, "遠ざかる": 0.7, "終わり": 0.8},
         flute_gain={"呼ぶ1": 1.4, "応える": 1.3, "呼ぶ2": 1.25, "遠ざかる": 1.2}, intro="鈴", passing=True)
CHIME = S.track("チャイム", "bell", patch="glockenspiel", volume=0.04, pan=0.3, reverb=0.7, barGain=c.g())

# ---------- 旋律（G ミクソリディア） ----------
put_melody(c, "呼ぶ1", [
    ["R:1 1:2 2:1", "3:3 R:1", "R:1 2:1 1:1 7,:1", "1:3 R:1"],
    ["R:1 3:2 4:1", "3:2 2:2", "R:1 1:1 2:1 3:1", "2:3 R:1"],
    ["R:1 5,:1 6,:1 7,:1", "1:3 R:1", "R:1 7,:1 6,:1 5,:1", "6,:3 R:1"],
    ["R:1 1:2 3:1", "2:2 1:2", "R:1 7,:1 1:1 2:1", "1:3 R:1"]], 5)
put_melody(c, "応える", [
    ["1:2 2:1 3:1", "4:2 3:2", "2:1 3:1 4:1 3:1", "2:3 R:1"],
    ["3:2 4:1 3:1", "2:2 1:2", "7,:1 1:1 2:1 3:1", "1:3 R:1"],
    ["5,:2 6,:1 7,:1", "1:2 2:2", "3:1 2:1 1:1 7,:1", "6,:3 R:1"],
    ["7,:1 1:1 2:2", "3:3 2:1", "1:2 7,:1 6,:1", "5,:4"]], 5)
put_melody(c, "呼ぶ2", [
    ["1:1 2:1 3:2", "4:2 3:1 2:1", "3:2 4:1 3:1", "2:3 R:1"],
    ["R:1 3:1 4:1 3:1", "2:2 1:2", "1:1 2:1 3:1 4:1", "3:3 R:1"],
    ["4:2 3:2", "2:1 3:1 2:1 1:1", "7,:2 1:2", "1:3 R:1"],
    ["3:2 2:2", "1:2 7,:2", "6,:2 7,:2", "1:4"]], 5)
put_bars(c, "遠ざかる", ["1:2 R:2", "R:4", "3:2 R:2", "R:4", "2:2 R:2", "R:4", "1:4", "R:4", "3:4", "R:4", "1:4", "R:4", "1:4", "R:4"], 5)
put_bars(c, "終わり", ["R:4", "1:4", "R:4", "R:4", "3:4", "R:4", "R:4", "R:4"], 5)

# ---------- 伴奏 ----------
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6")
    if n == "鈴":
        c.HARP.bar(b, f"{nm(t[0])}:4" if i % 2 == 0 else f"{nm(t[2])}:2 R:2")
        CHIME.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C6", "C7")[:4]) if i % 2 == 1 else f"R:2 {nm(tones(ch, 'C6', 'C7')[1])}:2")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    elif n in ("呼ぶ1", "応える", "呼ぶ2"):
        c.HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 2)) if n != "呼ぶ2" else " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 6, 4, 2, 4, 2)))
        if i % 4 == 3: c.HARP2.bar(b, f"R:2 {nm(t[-2])}:2")
        if n != "呼ぶ1" or i >= 4: c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        if n != "呼ぶ1" or i >= 8:
            v = voice(ch, 62, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if n == "呼ぶ2" and i % 2 == 1: CHIME.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C6", "C7")[:4]))
    elif n == "遠ざかる":
        c.HARP.bar(b, f"{nm(t[0])}:4" if i % 2 == 0 else f"{nm(t[2])}:2 R:2")
        if i % 4 == 3: c.HARP2.bar(b, f"R:2 {nm(t[-2])}:2")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4") if i < 8 else None
    elif n == "終わり":
        if i in (0, 3): c.HARP.bar(b, f"{nm(t[0])}:4")
        if i < 7:
            v = voice(ch, 62, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i == 5: CHIME.bar(b, f"{nm(tones(ch, 'C6', 'C7')[2])}:4")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の005。港で小舟の鈴が鳴る。G ミクソリディア・66。本物の小さな鈴の録音（曲の和音に合わせて高さを変えたもの）と笛が、呼び合う。",
       harm_scenes=["応える", "呼ぶ2"], tail_scene="終わり", tail_keep=7)

# ---------- 空気の指定：本物の鈴の録音を、曲の和音の音に高さを合わせて置く ----------
import math
BAR = 4 * 60 / BPM
F0 = 2716.0                                  # 録音(0292)のおよその高さ(Hz)
def semi(hz): return round(12 * math.log2(hz / F0), 2)
HZ = {"G": 1568.0, "F": 1396.9, "C": 2093.0, "D": 2349.3, "A": 1760.0, "E": 1318.5, "B": 1975.5}
def root(ch): return ch[0]
events = []
def bell(b, beat=0.0, db=-24, hz=None, seek=0.0, ln=5.0):
    ch = S.chords[b].split("|")[0]
    h = hz or {"G": 1568.0, "F": 1396.9, "C": 2093.0, "Dm": 2349.3, "Am": 1760.0, "Em": 1975.5}.get(ch, 1568.0)
    events.append({"t": round(b * BAR + beat * 60 / BPM, 2), "file": "0292", "db": db, "len": ln, "pan": 0.35, "seek": seek, "semi": semi(h), "hp": 200, "lp": 9000})
for sc, lvl in (("呼ぶ1", -22), ("呼ぶ2", -21)):                 # 笛が応える前に、鈴が呼ぶ（各フレーズの頭）
    for i, b in enumerate(S.sc(sc)):
        if i % 4 == 0: bell(b, 0.0, lvl)
for i, b in enumerate(S.sc("応える")):                         # 応える：笛のあとに、鈴が返す（各フレーズの最後の小節の3拍目）
    if i % 4 == 3: bell(b, 2.0, -24)
for i, b in enumerate(S.sc("遠ざかる")):                       # 遠ざかる：だんだん小さく、間があく
    if i in (0, 4, 8, 12): bell(b, 0.0, -24 - i * 0.9)
bell(S.sc("終わり")[5], 0.0, -32)
air = {"pre": 1.2, "tail": 5.0, "layers": [
    {"file": "1046", "db": -27, "hp": 90, "lp": 7500, "lfo": [37, 0.3], "wide": 0.011, "duck": 0.5, "fade": 5},
    {"file": "1059", "db": -35, "hp": 120, "lp": 4500, "lfo": [53, 0.5], "phase": 1.3, "wide": 0.017, "pan": 0.15, "duck": 0.45, "fade": 6}],
    "events": events,
    "fx": {"glass": {"hz": [784.0, 1568.0, 2349.3], "db": -26, "rt": 5.0, "start": 4}, "shimmer": {"db": -29, "rt": 6.0}, "far": {"db": -27, "delay": 0.2, "lp": 2800, "rt": 3.5}},
    "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air005.json", "w"), ensure_ascii=False)
print("鈴の録音を置いた回数:", len(events))
