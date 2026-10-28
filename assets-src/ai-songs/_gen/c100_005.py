# ケルト・フルート100曲「銀の笛と百の夜」005 小舟の鈴 The Little Boat Bell — 第2版（2026-10-28）
# イメージ: 夕方の港。波にゆれる小舟の舳先で、小さな鈴が鳴る。鈴が呼ぶと笛が答え、こんどは笛が呼んで鈴が答える。
#   やがて二人は一緒に歌い、舟が沖へ出ていくと鈴は遠くなる。最後は笛が鈴の音をまねて、ぽつり、ぽつりと消えていく。
# 形（台帳）: 掛け合い（笛と本物の鈴の録音。鈴は和音の音に高さを合わせる）。6/8・付点4分＝46（舟のゆれ）。G ミクソリディア。山なし。
# 編曲の表:
#   鈴     : 鈴だけ→竪琴の低い「付点4分・付点4分」とナイロンギターのゆれる分散和音（舟のゆれ）
#   呼ぶ1  : 4小節ごとに、1小節目で鈴が呼び、2〜4小節目で笛が答える
#   応える : 笛が3小節呼び、4小節目で鈴が答える
#   二人   : 笛はつながった長い旋律、鈴は2小節ごとに寄りそう。弦がうすく入る
#   呼ぶ2  : 呼ぶ1の形に戻る（チェロが低く支える）
#   遠ざかる: 鈴は小さく・暗く・間があいていく。笛もまばらに
#   終わり : 笛が鈴をまねた短い高い音を、ぽつり、ぽつりと
import sys, json, math
from c100_common import *
from c100_v2 import *

BPM = 129   # 8分音符＝129（付点4分＝43）
S = Song("C100", "005-little-boat-bell", "小舟の鈴", "The Little Boat Bell", BPM, 6, "G", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
P = ["G", "C", "G", "F", "G", "Am", "F", "G", "C", "G", "F", "C", "G", "F", "C", "G"]
S.scene("鈴", 4, "intro", ["G", "G", "F", "G"])
S.scene("呼ぶ1", 16, "verse", P)
S.scene("応える", 16, "verse", ["C", "G", "F", "G", "Am", "F", "G", "G", "C", "G", "Am", "F", "F", "C", "G", "G"])
S.scene("二人", 24, "chorus", P + ["C", "G", "F", "G", "F", "C", "G", "G"])
S.scene("呼ぶ2", 16, "verse", P)
S.scene("遠ざかる", 8, "verse", ["G", "F", "G", "C", "G", "F", "G", "G"])
S.scene("終わり", 4, "outro", ["C", "G", "G", "G"])
NAMES = ["鈴", "呼ぶ1", "応える", "二人", "呼ぶ2", "遠ざかる", "終わり"]

c = make(S, NAMES,
         [("鈴", 0, 0.6), ("呼ぶ1", 0, 0.62), ("応える", 0, 0.66), ("二人", 0, 0.7), ("二人", 16, 0.76), ("二人", 23, 0.68),
          ("呼ぶ2", 0, 0.64), ("遠ざかる", 0, 0.64), ("遠ざかる", 7, 0.58), ("終わり", 0, 0.56), ("終わり", 3, 0.42)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="鈴", passing=True, tension=False)
GT = S.track("ナイロンギター（舟のゆれ）", "guitar", patch="nylonGuitar", volume=0.11, pan=0.35, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.2, reverb=0.45, barGain=c.g())

p = [["R:3 2:1 3:2", "5:3 6:1 5:2", "3:2 2:1 1:3"], ["R:3 3:1 5:2", "6:2 7:1 1':3", "7:2 6:1 5:3"],
     ["R:3 5:1 6:2", "7:3 6:1 5:2", "4:2 3:1 2:3"], ["R:3 2:1 3:2", "5:2 3:1 2:2 7,:1", "1:6"]]
q = [["5:3 6:1 7:2", "1':3 7:1 6:2", "5:2 3:1 5:3"], ["6:3 5:1 4:2", "3:2 4:1 5:3", "2:2 1:1 2:3"],
     ["3:3 5:1 1':2", "7:2 6:1 5:3", "6:2 4:1 3:3"], ["2:3 3:1 4:2", "5:2 7,:1 2:3", "1:6"]]
call = sum([["R:6"] + x for x in p], [])
resp = sum([x + ["R:6"] for x in q], [])
both = sum([[x[0].replace("R:3", "1:3"), x[1], x[2]] + y for x, y in zip(p, q)], [])
play_melody(c, "呼ぶ1", call, 4, "air", density=0.7, seed=501)
play_melody(c, "応える", resp, 4, "air", density=0.8, seed=502)
play_melody(c, "二人", both, 4, "air", density=0.9, seed=503)
play_melody(c, "呼ぶ2", call, 4, "air", density=0.8, seed=504)
play_melody(c, "遠ざかる", ["5:3 3:3", "2:6", "3:3 4:3", "5:6", "5:3 6:3", "5:3 3:3", "2:3 1:3", "1:6"], 4, "air", density=0.5, seed=505)
play_melody(c, "終わり", ["1':1 R:2 5:1 R:2", "1':3 5:3", "1':6", "R:6"], 4, "air", density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5")
    if n == "鈴" and i < 2: continue
    if n not in ("終わり",) or i < 4:
        c.HARP.bar(b, f"{nm(r)}:3 {nm(r + 7)}:3")
        GT.bar(b, " ".join(f"{nm(t[x % len(t)])}:1" for x in (1, 2, 3, 4, 3, 2)))
    if n == "二人":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
    elif n != "鈴" and not (n == "終わり" and i >= 4):   # 空間の床：うすい弦（笛が休む小節で音が落ちすぎないように）
        v = voice(ch, 52, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n in ("呼ぶ2", "二人"): CELLO.bar(b, f"{nm(r)}:6")

rich(c, choir_scenes=["二人"], pulse_scenes=["応える", "二人", "呼ぶ2"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の005（第2版）。港の小舟の鈴と笛の掛け合い。6/8・付点4分＝46（舟のゆれ）。G ミクソリディア。鈴は本物の録音を和音の音に合わせ、呼ぶ→答える→一緒に→遠ざかる。最後は笛が鈴をまねて消える。",
       harm_scenes=None, tail_scene="終わり", fill=False, pads=True, pad_scenes=["呼ぶ1", "応える", "二人", "呼ぶ2", "遠ざかる", "終わり"], floor=True)

# ---------- 鈴（本物の録音 0292 を、和音の音に合わせて置く） ----------
BAR = B * 60 / BPM
F0 = 2716.0
HZ = {"G": 1568.0, "F": 1396.9, "C": 2093.0, "Am": 1760.0}
def bell(b, beat=0.0, db=-22, seek=0.0, ln=5.0, lp=9000, pan=0.35):
    h = HZ.get(S.chords[b].split("|")[0], 1568.0)
    return {"t": round(b * BAR + beat * 60 / BPM, 2), "file": "0292", "db": db, "len": ln, "pan": pan, "seek": seek,
            "semi": round(12 * math.log2(h / F0), 2), "hp": 200, "lp": lp}
ev = [bell(c.s0["鈴"], 0, -19), bell(c.s0["鈴"] + 1, 3, -21)]
for sc in ("呼ぶ1", "呼ぶ2"):
    ev += [bell(c.s0[sc] + j, 0, -20) for j in range(0, 16, 4)]
ev += [bell(c.s0["応える"] + j, 3, -22) for j in range(3, 16, 4)]
ev += [bell(c.s0["二人"] + j, 3, -25, pan=0.25) for j in range(1, 24, 2)]
for j, x in enumerate((0, 4, 8)):
    ev.append(bell(c.s0["遠ざかる"] + x, 0, -24 - 4 * j, lp=int(7000 - 2000 * j), pan=0.45 + 0.1 * j))
air = {"pre": 0.4, "tail": 6.0, "layers": [
    {"file": "1046", "db": -30, "hp": 90, "lp": 6000, "lfo": [round(2 * BAR, 1), 0.35], "wide": 0.012, "duck": 0.4, "fade": 6},
    {"file": "1059", "db": -38, "hp": 120, "lp": 4000, "lfo": [53, 0.4], "phase": 1.3, "wide": 0.016, "pan": 0.15, "duck": 0.4, "fade": 8}],
    "events": ev,
    "fx": {"glass": {"hz": [784.0, 1568.0, 2349.3], "db": -27, "rt": 6.0, "start": 4}, "shimmer": {"db": -27, "rt": 8.0},
           "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5}, "haze": {"db": -27, "rt": 8.0}, "band": {"db": -37, "hz": 6500, "per": 23}},
    "intro_db": 8.5}
json.dump(air, open("/tmp/cel/w/air005.json", "w"), ensure_ascii=False)
print("鈴の録音を置いた回数:", len(ev))
