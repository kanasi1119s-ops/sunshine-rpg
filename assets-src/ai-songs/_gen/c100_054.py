# ケルト・フルート100曲「銀の笛と百の夜」054 水面を叩く雨 Rain on the Water — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 霧が雨に変わる。舟の上で、エイラは祖父のことを思い出して泣く。雨粒が湖を叩く音に合わせて、笛がゆっくり歌う。
#   雨はいったん強くなり、やがて小降りになって、最後の一粒が水面に落ちる。
# 調べ: 悲しみ。形: 雨粒の上の歌（16小節の歌を、雨の強さを変えて4回。最後は小雨と、最後の一粒）。
# 拍子・速さ: 4/4・♩=58。旋法: E エオリア。
# 主役は笛（雨粒と同時に鳴る笛）。伴奏の主役: グロッケンと竪琴の雨粒（高い短い音。16分の格子の上に、ばらばらに落ちる）。
#   脇: ピアノの低い和音（そっと）。ギター・パッド・弦・打楽器・2本目の笛は使わない。
# この曲だけ: 笛の音の頭は、かならず雨粒と同じ時に鳴る（笛の音が始まるところには、必ず1粒落ちる）。
# 始まり: 雨粒だけ（とピアノの低い E）→ 終わり: 最後の一粒（グロッケン1音）。
# 山: 終盤に1つ（強い雨）。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "054-rain-on-the-water", "水面を叩く雨", "Rain on the Water", 58, 4, "E", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.15})
K = Key("E", "minor", 4)
CA = ["Em", "Bm", "C", "Em", "Am", "Em", "D", "Em"]
CB = ["Am", "G", "Am", "D", "C", "G", "D", "Em"]
SC = [("雨粒", 4, "intro", ["Em"] * 4), ("歌1", 16, "verse", CA + CB), ("歌2", 16, "verse", CA + CB), ("強い雨", 16, "chorus", CB + CB),
      ("小雨", 8, "verse", CA), ("最後の一粒", 2, "outro", ["Em", "Em"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("雨粒", 0, 0.66), ("歌1", 0, 0.68), ("歌2", 0, 0.72), ("強い雨", 0, 0.8), ("強い雨", 12, 0.88), ("小雨", 0, 0.72), ("最後の一粒", 0, 0.64)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="雨粒", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
RAIN = {"雨粒": 1.6, "歌1": 1.0, "歌2": 1.1, "強い雨": 1.3, "小雨": 1.0, "最後の一粒": 1.6}
HP = [S.track(f"竪琴（雨粒{j + 1}）", "harp", patch="folkHarp", volume=0.06, pan=-0.35 + 0.25 * j, reverb=0.7, sustain=1.4,
              barGain=[round(x * RAIN[S.scene_of(b)[0]], 3) for b, x in enumerate(G)]) for j in range(2)]
GL = [S.track(f"グロッケン（雨粒{j + 1}）", "bell", patch="glockenspiel", volume=0.028, pan=0.2 + 0.2 * j, reverb=0.75,
              barGain=[round(x * RAIN[S.scene_of(b)[0]], 3) for b, x in enumerate(G)]) for j in range(2)]
# ピアノ1音は ×1.4 で笛とほぼ同じ、和音の音は 0.08 前後（016）。ここはそっと
PB = S.track("ピアノ（低い音）", "piano", volume=0.16, pan=-0.15, reverb=0.55, sustain=1.6, barGain=G)
PC2 = [S.track(f"ピアノ（低い和音{j + 1}）", "piano", volume=0.06, pan=-0.05 + 0.08 * j, reverb=0.55, sustain=1.6, barGain=G) for j in range(2)]
PBI = S.track("ピアノ（始まりの低い E）", "piano", volume=0.3, gainDb=6, pan=-0.15, reverb=0.6, sustain=2.0)

def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return [r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12]
def near(pc, lo):
    return lo + (pc - lo) % 12

# ---------- 笛（1=E4。歌は16小節） ----------
A = ["5:2 4:1 3:1", "2:3 1:1", "3:1 4:1 5:1 6:1", "5:4", "6:2 5:1 4:1", "3:2 2:1 1:1", "2:1 3:1 4:1 2:1", "1:4"]
Bm = ["1':2 7:1 6:1", "5:3 3:1", "4:1 5:1 6:1 1':1", "7:4", "1':2 2':1 1':1", "7:2 6:1 5:1", "4:2 3:1 2:1", "1:3 R:1"]
B2 = Bm[:7] + ["1:4"]
PLAN = [("歌1", A + Bm, 0.1), ("歌2", A + Bm, 0.15), ("強い雨", Bm + B2, 0.2), ("小雨", A, 0.08)]
onsets = []
for sc, bars, dens in PLAN:
    s0 = c.s0[sc]; ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    onsets += [(t, m) for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 58, "air", B, density=dens, seed=5400 + len(onsets)))
s0 = c.s0["最後の一粒"]
c.FLUTE.at(s0 * B, "E4:6"); onsets.append((s0 * B, 64))

# ---------- 雨粒（笛の音の頭には必ず1粒。ほかは16分の格子に、ばらばらに） ----------
rng = random.Random(5401)
k = 0
taken = set()
for t, m in onsets:
    x = m + 12 if k % 2 == 0 else m + 24
    while x > 93: x -= 12
    (HP if k % 2 == 0 else GL)[(k // 2) % 2].at(t, f"{nm(x)}:0.5{',' if k % 3 else ''}")
    taken.add(round(t * 4)); k += 1
DENS = {"雨粒": 0.4, "歌1": 0.07, "歌2": 0.11, "強い雨": 0.26, "小雨": 0.05}
for b in range(c.s0["最後の一粒"]):
    n = S.scene_of(b)[0]; pcs = tri(S.chords[b])
    for q in range(16):
        g = b * 16 + q
        if g in taken or rng.random() > DENS[n]: continue
        x = near(rng.choice(pcs), rng.choice((72, 76, 81, 84)))
        tr = rng.choice(HP + GL)
        tr.at(round(g / 4, 3), f"{nm(x if tr in HP else min(x + 12, 96))}:0.5,")
s0 = c.s0["最後の一粒"]
GL[0].at(round((s0 + 1) * B + 1.5, 3), "B6:2")                    # 最後の一粒

# ---------- ピアノの低い和音（2拍ごと、そっと） ----------
# 1回目（8.05）: 雨粒だけの始まりが −46〜−69dB（ピアノの E2 は数秒で消え、雨粒もまばら）→ 雨粒を増やし、ピアノを小節ごとに打ちなおす
for b in range(4):
    PBI.at(b * B, f"E2:4{'' if b == 0 else ','}"); PC2[b % 2].at(round(b * B + 0.05, 3), "B2:3.9,")
for b in range(c.s0["歌1"], c.NB):
    ch = S.chords[b]; r, th, fi = tri(ch)
    if S.scene_of(b)[0] == "最後の一粒":
        if b == c.s0["最後の一粒"]: PB.at(b * B, "E2:8,"); PC2[0].at(b * B + 0.05, "B2:7.9,"); PC2[1].at(b * B + 0.1, "G3:7.8,")
        continue
    PB.at(b * B, f"{nm(near(r, 40))}:4,")
    PC2[0].at(round(b * B + 0.04, 3), f"{nm(near(fi, 47))}:3.9,"); PC2[1].at(round(b * B + 2.04, 3), f"{nm(near(th, 52))}:1.9,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の054（第3版）。霧が雨に変わり、舟の上でエイラが祖父を思って泣く。4/4・♩=58、E エオリア。グロッケンと竪琴の高い短い音が雨粒として、16分の格子の上にばらばらに落ち、笛の音の頭には必ず1粒が重なる（笛は雨粒と同時に鳴る）。ピアノの低い和音がそっと支える。16小節の歌を、雨の強さを変えて4回歌い、終盤に強い雨の山。最後は小雨になり、最後の一粒が水面に落ちる。",
       harm_scenes=None, tail_scene="最後の一粒", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air054.json", "w"), ensure_ascii=False)
