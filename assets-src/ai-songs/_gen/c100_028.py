# ケルト・フルート100曲「銀の笛と百の夜」028 夕もやの川 The River in Evening Mist — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 鴨の親子と別れた夕方。川から白いもやが立ちのぼり、向こう岸の木も、水車小屋の灯も、少しずつ輪郭がぼやけていく。
#   エイラの笛も、もやの中に溶けて、最後はどこで鳴っているのか分からない響きだけが残る。
# 調べ: 眠り。形: スロー・エア（12小節の節を4回。音がだんだんぼやけていく）→ 響き。
# 拍子・速さ: 4/4・♩=52。旋法: A ドリア。
# 主役は笛（輪郭がだんだん柔らかく。前半ははっきりした笛、後半は響きの多い柔らかい笛に持ちかえる）。
# 伴奏の主役: ピアノの分散和音（8分のまま、音の長さだけが場面ごとに倍になる＝ペダルで重なっていく）。
#   竪琴・ギター・弦・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: ピアノの音の長さが場面ごとに倍（0.5 → 1 → 2 → 4 → 8拍）になり、輪郭が霞んでいく。分散和音の速さは変えない。
# 始まり: はっきりしたピアノ（短く切った8分）→ 終わり: 響きだけが残る（ピアノの重なった響きと、遠い笛の1音）。
# 山: なし（平ら。響きが重なるぶん、後半ほど少し厚くなる）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "028-the-river-in-evening-mist", "夕もやの川", "The River in Evening Mist", 52, 4, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
K = Key("A", "dorian", 4)
CH = ["Am", "D", "Am", "G", "D", "Am", "Em", "Am", "C", "D", "G", "Am"]
SC = [("はっきり", 12, "verse", CH), ("もや1", 12, "verse", CH), ("もや2", 12, "verse", CH), ("もや3", 12, "verse", CH), ("響き", 6, "outro", ["Am", "D", "Am", "Am", "Am", "Am"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("はっきり", 0, 0.68), ("もや1", 0, 0.68), ("もや2", 0, 0.7), ("もや3", 0, 0.7), ("響き", 0, 0.68), ("響き", 5, 0.62)],
         {}, flute_gain={"はっきり": 1.15, "もや1": 1.15, "もや2": 0.0, "もや3": 0.0, "響き": 0.0}, intro="はっきり", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
LEN = {"はっきり": 0.5, "もや1": 1, "もや2": 2, "もや3": 4, "響き": 8}
# 柔らかい笛（もや2から持ちかえる。響きを多く、明るさを落とす）
FS = S.track("柔らかい笛（もやの中）", "panflute", patch="flute", volume=0.3, bright=-0.8, pan=0.05, reverb=0.8, breath=True,
             barGain=[round(x * (1.15 if b >= c.s0["もや2"] else 0), 3) for b, x in enumerate(G)])
# ピアノ：和音の4つの音それぞれに、重なりのぶんだけパートを分ける（同じ音が2拍ごとに鳴り直すので、8拍の長さには4本ずつ要る）
# 試し書き出し: 短い8分の分散和音（4音）で笛とほぼ同じ大きさ → 0.13→0.075。音が長く重なるほど厚くなるので、場面ごとに少しずつ下げる
PSC = {"はっきり": 1.3, "もや1": 1.15, "もや2": 1.0, "もや3": 0.9, "響き": 0.9}
PN = [[S.track(f"ピアノ（{v + 1}つ目の音・{j + 1}）", "piano", volume=0.075, pan=-0.25 + 0.15 * v, reverb=0.5, sustain=1.6,
               barGain=[round(x * PSC[S.scene_of(b)[0]], 3) for b, x in enumerate(G)])
       for j in range(4)] for v in range(4)]

# ---------- 旋律（A ドリア。1=A4。12小節） ----------
M = ["5:2 4:1 3:1", "2:3 1:1", "3:2 5:2", "4:4", "6:2 5:1 4:1", "5:3 3:1", "2:2 1:1 7,:1", "1:4",
     "3:1 4:1 5:2", "6:2 1':2", "7:2 6:1 5:1", "5:4"]
play_melody(c, "はっきり", M, 4, "air", key=K, density=0.35, seed=2801)
play_melody(c, "もや1", M, 4, "air", key=K, density=0.25, seed=2802)
play_melody(c, "もや2", M, 4, "air", key=K, density=0.12, seed=2803, track=FS)
play_melody(c, "もや3", M, 4, "air", key=K, density=0.05, seed=2804, track=FS)
play_melody(c, "響き", ["5:4", "3:4", "1:4", "R:4", "R:4", "R:4"], 4, "air", key=K, density=0.0, track=FS)

# ---------- ピアノの分散和音（8分のまま。音の長さだけが倍になっていく） ----------
ROOT = {"Am": 45, "D": 50, "G": 43, "Em": 40, "C": 48}
def voicing(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = ROOT[ch]
    th = (3 if m.group(2) else 4)
    return [r, r + 7, r + 12 + th, r + 19 + (0 if r + 19 <= 72 else -12)]     # 根音・5度・上の3度・上の5度（9度は使わずに澄ませる）
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    v = voicing(ch); L = LEN[n]
    if n == "響き" and i >= 3:                                         # 響きの最後：もう鳴らさず、重なった響きだけ
        continue
    for q in range(8):                                                  # 8分で、根音 → 5度 → 3度 → 5度 と上がっていく（同じ音は2拍ごと）
        vi = q % 4
        track = PN[vi][(b * 2 + q // 4) % 4]
        mk = "!" if q == 0 and n == "はっきり" else ("," if q % 2 else "")
        track.at(round(b * B + 0.5 * q, 3), f"{nm(v[vi])}:{L}{mk}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の028（第3版）。夕方、川から白いもやが立ちのぼり、景色の輪郭が少しずつぼやけていく。スロー・エア（4/4・♩=52）、A ドリア。ピアノの分散和音は8分のまま、音の長さだけが場面ごとに倍（0.5→1→2→4→8拍）になってペダルのように重なり、笛も後半は響きの多い柔らかい笛に持ちかえる。最後は、重なったピアノの響きと遠い笛の1音だけが残る。",
       harm_scenes=None, tail_scene="響き", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 7.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air028.json", "w"), ensure_ascii=False)
