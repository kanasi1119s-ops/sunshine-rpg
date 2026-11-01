# ケルト・フルート100曲「銀の笛と百の夜」060 対岸 The Far Shore — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第6章の終わり。霧の中、エイラは向こう岸を目ざして、ゆっくり笛を吹きながら舟を進める。
#   ふいに霧が晴れ、対岸の村の灯と人影が見える。同じ節が、うれしさで踊りだす。岸に着いて、3歩、地面を踏みしめる。
# 調べ: 喜び。形: ゆっくりの節がポルカで踊りだす（同じ16小節の節を、霧の中では ♩=48 で長く、晴れると ♩=116 のポルカで）。
# 拍子・速さ: 2/4・♩=48 → 116。旋法: E ミクソリディア（D♮）。
# 主役は笛（霧では長く、晴れると跳ねる）。伴奏の主役: アコーディオン（霧では長い和音、ポルカでは裏拍の「チャッ」）と、
#   ナイロン弦ギター（ポルカの低音の「ズン」）、ピチカート（低音の補強）。打楽器は枠太鼓（ポルカの拍と、最後の3歩）。
#   竪琴・ピアノ・パッド・2本目の笛は使わない。
# 中ほど（ポルカ2 と 3 のあいだ）に、伴奏が2小節に1回だけ打つ「止まり打ち」の16小節（笛だけが走り続ける）。
# この曲だけ: 同じ節が、霧の中ではゆっくり、晴れると踊りだす（テンポが ♩=48 から 116 へ、4小節で上がる）。
# 始まり: 笛ひとり → 終わり: 枠太鼓の3歩（足音）。
# 山: 終盤（最後の A）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "060-the-far-shore", "対岸", "The Far Shore", 116, 2, "E", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("E", "mixolydian", 4)
CA = ["E", "D", "E", "A", "E", "D", "Bm", "E"]
CB = ["E", "A", "D", "E", "E", "A", "D", "E"]
T = CA * 2 + CB * 2
SC = [("笛ひとり", 16, "intro", CA * 2), ("霧の中", 16, "verse", CB * 2), ("晴れる", 4, "verse", ["B", "B", "E", "E"]),
      ("ポルカ1", 32, "verse", T), ("ポルカ2", 32, "verse", T), ("止まり打ち", 16, "verse", CB * 2), ("ポルカ3", 32, "chorus", T), ("ポルカ4", 32, "verse", T),
      ("最後のA", 16, "chorus", CA * 2), ("3歩", 3, "outro", ["E"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("笛ひとり", 0, 0.7), ("霧の中", 0, 0.72), ("晴れる", 0, 0.74), ("ポルカ1", 0, 0.78), ("ポルカ2", 0, 0.8), ("ポルカ3", 0, 0.84), ("ポルカ4", 0, 0.82),
          ("最後のA", 0, 0.9), ("最後のA", 15, 0.96), ("3歩", 0, 0.92)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="笛ひとり", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 48}, {"bar": s["晴れる"] + 1, "bpm": 116, "ramp": 4}]
B = S.beats
G = c.g()
# 試し書き出し: アコーディオン（0.05）の長い1音は笛より約3dB 大きく、裏拍の短い2音は約5dB 小さい → 長い和音の所（霧の中・晴れる）は強さを弱く
ACG = {"霧の中": 0.45, "晴れる": 0.6}
AC = [S.track(f"アコーディオン{j + 1}", "accordion", volume=0.05, pan=0.2 + 0.08 * j, reverb=0.35, barGain=[round(x * ACG.get(S.scene_of(b)[0], 1.0), 3) for b, x in enumerate(G)]) for j in range(3)]
GT = S.track("ギター（低音のズン）", "guitar", patch="nylonGuitar", volume=0.018, pan=-0.25, reverb=0.3, barGain=G)
PZ = S.track("ピチカート（低音）", "strings", patch="pizzicato", volume=0.1, gainDb=5, pan=-0.1, reverb=0.3, barGain=G)
DR = S.track("枠太鼓", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=0.05, reverb=0.25, barGain=G)

# ---------- 節（16小節。1=E4。8分＝0.5） ----------
A = ["5:0.5 6:0.25 5:0.25 3:0.5 1:0.5", "2:0.5 3:0.5 4:1", "5:0.5 6:0.25 5:0.25 3:0.5 5:0.5", "6:1 5:1",
     "5:0.5 6:0.25 5:0.25 3:0.5 1:0.5", "2:0.5 3:0.5 4:0.5 2:0.5", "7,:0.5 2:0.5 5:0.5 4:0.5", "1:1 5,:1"]
Bm = ["1':0.5 7:0.5 1':0.5 5:0.5", "6:0.5 5:0.5 4:1", "7:0.5 6:0.5 7:0.5 4:0.5", "5:1 3:1",
      "1':0.5 7:0.5 1':0.5 2':0.5", "1':0.5 7:0.5 6:0.5 5:0.5", "4:0.5 2:0.5 7,:0.5 2:0.5", "1:1 R:1"]
play_melody(c, "笛ひとり", A + A, 4, "air", key=K, density=0.15, seed=6001)               # 霧：同じ節を、ゆっくり長く
play_melody(c, "霧の中", Bm + Bm, 4, "air", key=K, density=0.2, seed=6002)
play_melody(c, "晴れる", ["5:2", "6:1 7:1", "1':1 R:1", "R:1 5,:1"], 4, "air", key=K, density=0.0)
for k, sc in enumerate(("ポルカ1", "ポルカ2", "ポルカ3", "ポルカ4")):
    play_melody(c, sc, A + A + Bm + Bm, 4, "reel", key=K, density=(0.3, 0.4, 0.5, 0.45)[k], seed=6010 + k)
play_melody(c, "止まり打ち", Bm + Bm, 4, "reel", key=K, density=0.35, seed=6015)
play_melody(c, "最後のA", A + A, 4, "reel", key=K, density=0.55, seed=6020)
s0 = c.s0["3歩"]
c.FLUTE.at(s0 * B, "E5:1!")

# ---------- 伴奏 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 40); hi5 = near(fi, lo + 1)
    voice = [near(r, 57), near(th, 57), near(fi, 57)]
    if n == "笛ひとり":
        continue
    if n == "霧の中":                                         # 霧：アコーディオンの長い和音（2小節ごと）とピチカートの根音
        if i % 2 == 0:
            for j, m in enumerate(voice): AC[j].at(round(b * B + 0.04 * j, 3), f"{nm(m)}:{4 - 0.1}{',' if j else ''}")
            PZ.at(b * B, f"{nm(lo)}:1,")
        continue
    if n == "晴れる":
        for j, m in enumerate(voice): AC[j].at(round(b * B + 0.03 * j, 3), f"{nm(m)}:1.9{',' if j else '!'}")
        GT.at(b * B, f"{nm(lo)}:1"); DR.bar(b, "C3:1! E3:0.5, E3:0.5," if i >= 2 else "R:2")
        continue
    if n == "3歩":                                            # 岸に着いて、3歩
        DR.bar(b, "C3:1! R:1")
        if i == 0:
            for j, m in enumerate(voice): AC[j].at(round(b * B + 0.03 * j, 3), f"{nm(m)}:1.5!")
            GT.at(b * B, f"{nm(lo)}:1.5!"); PZ.at(b * B, f"{nm(lo)}:1!")
        continue
    if n == "止まり打ち":                                     # 村が見えて、みんなが一瞬だけ手を止める：2小節に1回だけ全員で打つ（笛は走り続ける）
        if i % 2 == 0:
            for j, m in enumerate(voice): AC[j].at(round(b * B + 0.02 * j, 3), f"{nm(m)}:0.4!")
            GT.at(b * B, f"{nm(lo)}:0.5!"); PZ.at(b * B, f"{nm(lo)}:0.5!"); DR.at(b * B, "C3:0.5!")
        if i >= 14: DR.bar(b, "C3:0.5! E3:0.5, C3:0.5! E3:0.5!")
        continue
    # ポルカ：低音の「ズン」（1拍目は根音、2拍目は5度）と、アコーディオンの裏拍の「チャッ」
    GT.bar(b, f"{nm(lo)}:0.5! R:0.5 {nm(hi5 if hi5 - lo <= 9 else hi5 - 12)}:0.5 R:0.5")
    PZ.bar(b, f"{nm(lo)}:0.5 R:1.5" if n != "ポルカ1" or i >= 16 else "R:2")
    for j, m in enumerate(voice):
        AC[j].bar(b, f"R:0.5 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.2" if n != "ポルカ3" or i % 8 != 7 else f"R:0.5 {nm(m)}:0.3, R:0.2 {nm(m)}:0.25, {nm(m)}:0.25, {nm(m)}:0.5,")
    if n == "ポルカ1" and i < 16:
        DR.bar(b, "C3:1, R:1")
    elif n in ("ポルカ3", "最後のA"):
        DR.bar(b, "C3:0.5! E3:0.5, C3:0.5 E3:0.5," if i % 8 != 7 else "C3:0.5! E3:0.25, E3:0.25, C3:0.5! C3:0.5!")
    else:
        DR.bar(b, "C3:0.5! E3:0.5, C3:0.5, E3:0.5,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の060（第3版）。第6章の終わり、霧の湖を渡って対岸へ。2/4、E ミクソリディア。霧の中では、笛が同じ16小節の節を ♩=48 でゆっくり長く吹き（はじめは笛ひとり、次にアコーディオンの長い和音）、霧が晴れると4小節でテンポが 116 に上がって、同じ節がポルカで踊りだす。伴奏はギターの低音の「ズン」、アコーディオンの裏拍の「チャッ」、ピチカートと枠太鼓。山は最後の A。岸に着いて、枠太鼓の3歩で終わる。",
       harm_scenes=None, tail_scene="3歩", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.2}}}
json.dump(air, open("/tmp/cel/w/air060.json", "w"), ensure_ascii=False)
