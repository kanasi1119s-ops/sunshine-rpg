# ケルト・フルート100曲「銀の笛と百の夜」051 湖への道 The Road Down to the Lake — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第6章のはじまり。塔をあとにしたエイラは、霧の湖へ下る長い坂道を歩く。坂を一つ下りるたびに、空が少しずつ広く見えてくる。
# 調べ: あいだ。形: 坂を下る旋律（16小節の同じ節を4回。回るたびに一段低く：音階で3度ずつ下がり、最後は1オクターブ下）。
# 拍子・速さ: 3/4・♩=52。旋法: D エオリア。
# 主役は笛（下りていく笛）。伴奏の主役: ナイロン弦ギターのローヴィング・サム（親指の低音が拍ごとに歩き、ほかの指が裏で和音をつまむ）。
#   脇: 3回目から高い弦（バイオリン・ビオラ。開いた5度）。竪琴・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 旋律が下りるほど、伴奏が上へ開く（ギターの指の音は回るたびに高く、3回目から高い弦が加わる）。
#   和音も旋律といっしょに音階の上で下がる（Dm → B♭ → Gm → ふたたび Dm）。
# 始まり: ギターの歩みだけ → 終わり: 低い笛と、上に開いた高い弦。
# 山: なし。
import sys, json, re
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia

S = Song("C100", "051-the-road-down-to-the-lake", "湖への道", "The Road Down to the Lake", 52, 3, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.15})
K = Key("D", "minor", 4)
BASE = ["Dm", "C", "Bb", "C", "Dm", "Am", "Bb", "Dm"]
SHIFT = [0, -2, -4, -7]                                 # 回ごとの下がり方（音階の段）
LOWER = {0: BASE, -2: ["Bb", "Am", "Gm", "Am", "Bb", "F", "Gm", "Bb"], -4: ["Gm", "F", "Eb", "F", "Gm", "Dm", "Eb", "Gm"], -7: BASE}
SC = [("ギターの歩み", 4, "intro", ["Dm", "Dm", "C", "Dm"])] + [(f"坂{r + 1}", 16, ("chorus" if r == 3 else "verse"), LOWER[SHIFT[r]] * 2) for r in range(4)] + \
     [("岸", 6, "outro", ["Dm"] * 6)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ギターの歩み", 0, 0.68), ("坂1", 0, 0.7), ("坂2", 0, 0.72), ("坂3", 0, 0.74), ("坂4", 0, 0.76), ("岸", 0, 0.74), ("岸", 5, 0.68)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ギターの歩み", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 親指（0.014）と指（0.01）を合わせると笛より約3dB 小さいだけ（指の音が大きい）→ 指を 0.007 に。始まりはギターだけなので、始まり用のパートを別に（大きく）
GT = S.track("ギター（親指の低音）", "guitar", patch="nylonGuitar", volume=0.014, pan=-0.15, reverb=0.35, barGain=G)
GF = [S.track(f"ギター（指の和音{j + 1}）", "guitar", patch="nylonGuitar", volume=0.007, pan=-0.3 + 0.15 * j, reverb=0.35, barGain=G) for j in range(2)]
GTI = S.track("ギター（始まりの歩み）", "guitar", patch="nylonGuitar", volume=0.026, pan=-0.2, reverb=0.35)
VN = [S.track(f"バイオリン（上に開く{j + 1}）", "strings", patch="violin", volume=0.03, gainDb=4, pan=0.25 + 0.1 * j, reverb=0.7, release=0.8, barGain=G) for j in range(2)]
VA = S.track("ビオラ（上に開く）", "strings", patch="viola", volume=0.014, pan=0.15, reverb=0.7, release=0.8, barGain=G)

# ---------- 和音の音 ----------
def triad(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12

# ---------- ギターのローヴィング・サム（1小節＝8分6つ。親指は拍に、指は裏に） ----------
def guitar_bar(b, ch, nxt, f_lo, intro=False):
    r, th, fi = triad(ch); nr = triad(nxt)[0]
    bass = near(r, 38)                                   # D2〜C♯3
    fifth = near(fi, bass + 1)
    if fifth - bass > 9: fifth -= 12
    walk = near(nr, 38)                                  # 次の和音へ歩く音（下か上から半音・全音で）
    app = walk - 2 if walk - 2 > bass else walk + 2
    if app < 36: app += 12
    t0 = b * B
    tr = GTI if intro else GT
    for k, m in enumerate((bass, fifth, app)):
        tr.at(round(t0 + k, 3), f"{nm(m)}:{1.0 if k < 2 else 0.9}{'' if k == 0 else ','}")
    up = [near(th, f_lo), near(fi, f_lo), near(r, f_lo + 5)]
    for k in range(3):
        trf = GTI if intro else GF[k % 2]
        trf.at(round(t0 + k + 0.5, 3), f"{nm(up[k])}:0.5,")

for b in range(c.NB):
    n = S.scene_of(b)[0]
    if n == "岸": continue
    nxt = S.chords[b + 1] if b + 1 < c.NB else "Dm"
    f_lo = {"ギターの歩み": 55, "坂1": 55, "坂2": 59, "坂3": 64, "坂4": 69}[n]       # 指の音は、回るたびに高く
    guitar_bar(b, S.chords[b], nxt, f_lo, intro=(n == "ギターの歩み"))

# ---------- 笛（16小節の同じ節。1=D4。基本は D5 のまわり） ----------
M = ["5':1.5 4':0.5 3':1", "2':2 1':1", "2':1 3':1 4':1", "5':3",
     "6':1.5 5':0.5 4':1", "3':1 2':1 1':1", "7:1 1':1 2':1", "1':3",
     "3':1.5 2':0.5 1':1", "7:2 1':1", "7:1 1':1 2':1", "3':3",
     "4':1 3':1 2':1", "1':1 7:1 1':1", "2':1 3':1 7:1", "1':3"]
for r in range(4):
    s0 = c.s0[f"坂{r + 1}"]; ev = []
    for j, s_ in enumerate(M): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, _dia(K, m, SHIFT[r])] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 52, "air", B, density=(0.2 if r < 3 else 0.12), seed=5100 + r))

# ---------- 高い弦（3回目から。開いた5度で上へ） ----------
for sc, lo in (("坂3", 74), ("坂4", 79)):
    s0 = c.s0[sc]
    for q in range(0, 16, 2):
        r, th, fi = triad(S.chords[s0 + q])
        a = near(r, lo); f = a + 7
        VN[0].at(round((s0 + q) * B, 3), f"{nm(a)}:{2 * B - 0.1}{',' if q % 4 else ''}")
        VN[1].at(round((s0 + q) * B + 0.05, 3), f"{nm(f)}:{2 * B - 0.15},")
        if sc == "坂4": VA.at(round((s0 + q) * B + 0.1, 3), f"{nm(near(th, 64))}:{2 * B - 0.2},")

# ---------- 岸：低い笛と、上に開いた高い弦 ----------
s0 = c.s0["岸"]
c.FLUTE.at(s0 * B, "A4:3"); c.FLUTE.at((s0 + 1) * B, "F4:3"); c.FLUTE.at((s0 + 2) * B, "D4:11")
VN[0].at(s0 * B, "D6:17"); VN[1].at(round(s0 * B + 0.1, 3), "A5:16.9,"); VA.at(round(s0 * B + 0.2, 3), "D5:16.8,")
GT.at(s0 * B, "D2:6,"); GF[0].at(round(s0 * B + 0.5, 3), "A3:5,"); GF[1].at(round(s0 * B + 1.0, 3), "F4:4.5,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の051（第3版）。霧の湖へ下る長い坂道。3/4・♩=52、D エオリア。ナイロン弦ギターのローヴィング・サム（親指の低音が拍ごとに歩き、指が裏で和音をつまむ）の上で、笛が16小節の同じ節を4回吹く。回るたびに節は一段低く（音階で3度ずつ、最後は1オクターブ下）、和音もいっしょに下がる。反対に、ギターの指の音は回るたびに高くなり、3回目から高い弦が開いた5度で加わる。最後は低い笛と、上に開いた高い弦。",
       harm_scenes=None, tail_scene="岸", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air051.json", "w"), ensure_ascii=False)
