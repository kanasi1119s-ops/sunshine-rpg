# ケルト・フルート100曲「銀の笛と百の夜」054 水面を叩く雨 Rain on Still Water（2026-10-29。第6章 霧の湖）
# イメージ: 灯を過ぎたあたりで、霧が小雨に変わる。鏡のような湖に、ぽつ、ぽつと輪が広がる。エイラは舟の上で笛を吹く。
#   雨粒が落ちるたびに、笛の音がひとつ生まれるようで、雨と笛がいっしょに歌っている。雨はしだいに強くなり、やがて上がる。最後の一粒。
# 形: 数粒の雨 → 雨の中の歌（2回）→ 雨が強まる（終盤の山）→ 雨が上がる → 最後の一粒。4/4・♩=58・E エオリア。
# ただひとつ: 雨粒（グロッケン・竪琴の高い音・ピチカートの高い音）がふぞろいに落ち、笛の音の頭は、かならず雨粒と同じ時に鳴る
#   （雨粒が笛の音を生む）。雨粒の数で、雨の強さ（場面）を表す。
# 編曲の表:
#   数粒    : 雨粒がまばらに、低い弦とチェロ、ナイロンギターの低い音
#   雨の歌1 : 笛。ピアノの左手の和音、ギターの指弾き
#   雨の歌2 : ＋弦3声・内声の動き。雨粒が少し増える
#   強まる  : 笛の2つ目の節（上の音域）。雨粒が多く、笛の和声。ピアノは両手
#   上がる  : 最初の節の前半。雨粒が減っていく
#   最後の一粒: 弦の和音と、雨粒ひとつ
import sys, json, random
from c100_common import *
from c100_v2 import *

BPM = 58
S = Song("C100", "054-rain-on-still-water", "水面を叩く雨", "Rain on Still Water", BPM, 4, "E", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
P = ["Em", "C", "G", "D", "Am", "Em", "C", "Bm", "Em", "C", "G", "D", "C", "Am", "Bm", "Em"]
S.scene("数粒", 4, "intro", ["Em", "C", "Em", "D"])
S.scene("雨の歌1", 16, "verse", P)
S.scene("雨の歌2", 16, "verse", P)
S.scene("強まる", 12, "chorus", ["C", "D", "Bm", "Em", "C", "D", "G", "G", "Am", "C", "D", "Em"])
S.scene("上がる", 8, "verse", P[:8])
S.scene("最後の一粒", 4, "outro", ["C", "Am", "Em", "Em"])
NAMES = ["数粒", "雨の歌1", "雨の歌2", "強まる", "上がる", "最後の一粒"]

c = make(S, NAMES,
         [("数粒", 0, 0.6), ("雨の歌1", 0, 0.64), ("雨の歌2", 0, 0.68), ("強まる", 0, 0.74), ("強まる", 8, 0.86), ("強まる", 11, 0.78),
          ("上がる", 0, 0.68), ("最後の一粒", 0, 0.62), ("最後の一粒", 3, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="数粒", passing=True, tension=False)
GLOCK = S.track("雨粒（グロッケン）", "bell", patch="glockenspiel", volume=0.03, pan=0.35, reverb=0.65, barGain=c.g())
DROPH = S.track("雨粒（竪琴）", "harp", patch="folkHarp", volume=0.06, pan=-0.4, reverb=0.6, barGain=c.g())
DROPP = S.track("雨粒（ピチカート）", "strings", patch="pizzicato", volume=0.05, pan=0.05, reverb=0.5, barGain=c.g())
PL = S.track("ピアノ（左手）", "piano", volume=0.85, pan=-0.2, reverb=0.5, barGain=c.g())
PR = S.track("ピアノ（右手）", "piano", volume=0.7, pan=-0.1, reverb=0.5, barGain=c.g())
GTR = S.track("ナイロンギター", "guitar", patch="nylonGuitar", volume=0.065, pan=0.3, reverb=0.4, barGain=c.g())
CELLO = S.track("チェロ（湖の底）", "strings", patch="cello", volume=0.08, pan=0.1, reverb=0.5, barGain=c.g())

M = ["5:1.5 4:0.5 5:1 1':1", "7:2 6:1 5:1", "5:1 3:1 2:1 3:1", "4:3 R:1",
     "4:1.5 5:0.5 6:1 1':1", "7:1 6:1 5:2", "6:1 5:1 3:1 6:1", "5:3 R:1",
     "5:1.5 4:0.5 5:1 2':1", "1':2 7:1 6:1", "7:1 5:1 3:1 5:1", "6:1 5:1 4:2",
     "3:1 4:1 5:1 6:1", "1':2 7:1 6:1", "5:1.5 4:0.5 2:2", "1:4"]
N = ["3':2 2':1 1':1", "2':2 1':1 7:1", "1':1 7:1 5:2", "5:4",
     "3':2 4':1 3':1", "2':1 1':1 2':2", "3':3 2':1", "1':4",
     "1':1.5 7:0.5 6:2", "5:1 6:1 1':2", "7:2 6:1 4:1", "5:4"]
notes = []
notes += play_melody(c, "雨の歌1", M, 4, "air", density=0.45, seed=5401)
notes += play_melody(c, "雨の歌2", M, 4, "air", density=0.6, seed=5402)
notes += play_melody(c, "強まる", N, 4, "air", density=0.8, seed=5403)
notes += play_melody(c, "上がる", M[:7] + ["5:4"], 4, "air", density=0.35, seed=5404)
notes += play_melody(c, "最後の一粒", ["1:4", "R:4", "R:4", "R:4"], 4, "air", density=0.0, seed=5405)

# ---------- 雨粒 ----------
B = S.beats
rg = random.Random(54)
RAIN = {"数粒": 2.5, "雨の歌1": 3, "雨の歌2": 4, "強まる": 6.5, "上がる": 2.5, "最後の一粒": 0}
# 1) 笛の音の頭（装飾音を除く、長さ 0.4 拍以上）には、かならず雨粒
onsets = sorted({round(t, 3) for t, L, m, mk in notes if L >= 0.4})
drops = [(t, None) for t in onsets]
# 2) あいだに、ふぞろいの雨粒（16分の格子の上で。場面の強さで数を変える）
for b in range(c.NB):
    n = c.scene_of_bar[b]; k = RAIN[n]
    if n == "上がる": k = max(1.0, k * (1 - S.scene_of(b)[1] / 10))
    cnt = int(k) + (1 if rg.random() < k - int(k) else 0)
    for _ in range(cnt): drops.append((b * B + rg.randrange(16) * 0.25, None))
drops.append((c.s0["最後の一粒"] * B + 3 * B + 1.0, "last"))
EP = [p for p in range(76, 92) if p % 12 in (4, 7, 9, 11, 2)]   # 高い所の E マイナー・ペンタトニック
last = {}
for t, tag in sorted(drops):
    if t >= c.NB * B: continue
    b = int(t // B); ch = S.chords[b].split("|")[0]
    pcs = chord_pcs(ch)
    cand = [p for p in EP if p % 12 in pcs] or EP
    p = rg.choice(cand)
    tr = rg.choice((GLOCK, DROPH, DROPH, DROPP)) if tag is None else GLOCK
    if tr is DROPP: p -= 12
    if tr is GLOCK: p += 0 if p >= 79 else 12
    if last.get(id(tr), -9) > t - 0.24: continue        # 同じ楽器で詰まりすぎない
    last[id(tr)] = t
    tr.at(round(t, 3), f"{nm(p)}:{1.5 if tr is not DROPP else 0.5}{',' if rg.random() < 0.5 else ''}")

# ---------- 伴奏 ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "E3", "E5")
    CELLO.bar(b, f"{nm(r)}:4")
    nv = 3 if n in ("雨の歌2", "強まる", "最後の一粒") else 2
    v = voice(ch, 50 if n in ("数粒", "雨の歌1") else 55, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "数粒": GTR.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2"); continue
    if n == "最後の一粒": continue
    PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if n != "強まる" else f"{nm(r)}:1 {nm(r + 7)}:1 {nm(r + 12)}:2")
    GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 2, 3, 2, 4, 2)) if n != "上がる" else f"{nm(t[0])}:1 {nm(t[2])}:1 {nm(t[4 % len(t)])}:2")
    if n == "強まる":
        hi = tones(ch, "B4", "B5"); PR.bar(b, f"{nm(hi[0])}:2 {nm(hi[1])}:2")
rich(c, choir_scenes=["強まる"], pulse_scenes=["雨の歌2", "強まる"], guitar=False, pizz=False, inner=True)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の054。静かな湖に小雨が落ちる。4/4・♩=58、E エオリア。雨粒（グロッケン・竪琴・ピチカートの高い音）がふぞろいに落ち、笛の音の頭はかならず雨粒と同じ時に鳴る。雨は強まり（終盤の山）、やがて上がって、最後の一粒で終わる。",
       harm_scenes=None, tail_scene="最後の一粒", fill=False, pads=True, pad_scenes=["雨の歌1", "雨の歌2", "強まる", "上がる", "最後の一粒"], floor=True)
air = {"pre": 0.6, "tail": 7.0, "layers": [{"file": "1019", "db": -40, "hp": 200, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -29, "rt": 7.0}, "far": {"db": -25, "delay": 0.25, "lp": 2800, "rt": 4.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air054.json", "w"), ensure_ascii=False)
