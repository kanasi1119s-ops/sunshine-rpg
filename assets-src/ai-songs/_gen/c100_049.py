# ケルト・フルート100曲「銀の笛と百の夜」049 蔦の窓 The Ivy Window — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 扉の奥は、蔦におおわれた小さな部屋だった。窓は蔦でふさがれて暗い。エイラが笛を吹きながら、蔦を少しずつ払っていくと、
#   光が足もとから壁へ、壁から天井へと上がっていき、最後に窓のいちばん上から、一筋の光がまっすぐ射しこむ。
# 調べ: 眠り（静かな驚き）。形: 一筋の光が射しこむ（旋律の高さが、場面ごとにゆっくり上がる）。
# 拍子・速さ: 3/4・♩=60。旋法: A リディア（D♯ がやわらかく浮く）。
# 主役は笛（最後に一番高い長い音）。伴奏の主役: マリンバの柔らかい3音のくり返し（C♯・E・D♯）。脇: 低い弦の影（チェロとビオラ。光が上がるほど薄くなる）。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 笛のいちばん高い長い音（A5）が、最後に1本だけ（それまで笛は E5 より上に行かない）。
# 始まり: 低い弦の影 → 終わり: 高い一筋の光（笛の A5 を長く）。
# 山: 最後だけ。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "049-the-ivy-window", "蔦の窓", "The Ivy Window", 60, 3, "A", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("A", "lydian", 4)
CH8 = ["A", "B", "A", "E", "F#m", "B", "E", "A"]
SC = [("影", 8, "intro", ["A"] * 8), ("足もと", 24, "verse", CH8 * 3), ("壁", 24, "verse", CH8 * 3), ("天井", 24, "verse", CH8 * 3),
      ("一筋", 10, "chorus", ["A"] * 10)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("影", 0, 0.66), ("足もと", 0, 0.66), ("壁", 0, 0.68), ("天井", 0, 0.7), ("天井", 23, 0.72), ("一筋", 0, 0.8), ("一筋", 9, 0.74)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="影", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: マリンバ（0.05）は笛より約5dB 小さい。チェロ・ビオラ（強さ 1.4）は笛と同じくらい（影は場面ごとに弱める）
SHADE = {"影": 2.0, "足もと": 1.4, "壁": 1.1, "天井": 0.8, "一筋": 0.6}            # 低い弦の影は、光が上がるほど薄く
VC = S.track("チェロ（影）", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.2, reverb=0.65, release=0.6, barGain=[round(x * SHADE[S.scene_of(b)[0]], 3) for b, x in enumerate(G)])
VA = S.track("ビオラ（影）", "strings", patch="viola", volume=0.017, pan=0.15, reverb=0.65, release=0.6, barGain=[round(x * SHADE[S.scene_of(b)[0]], 3) for b, x in enumerate(G)])
# 1回目（7.52）: 影（約24秒）が本編より約12dB 小さかった → 影の8小節だけ、別の弦のパートを大きく
VCI = S.track("チェロ（始まりの影）", "strings", patch="cello", volume=0.05, gainDb=6, pan=-0.2, reverb=0.65, release=0.6)
VAI = S.track("ビオラ（始まりの影）", "strings", patch="viola", volume=0.04, gainDb=4, pan=0.15, reverb=0.65, release=0.6)
MR = [S.track(f"マリンバ（光の3音{j + 1}）", "strings", patch="marimba", volume=0.05, pan=-0.2 + 0.4 * j, reverb=0.55, barGain=G) for j in range(2)]

# ---------- 笛（A リディア。1=A4。場面ごとに高さが上がる。E5 より上には行かない、最後だけ A5） ----------
LOW = ["5,:3", "6,:2 7,:1", "1:3", "7,:2 6,:1", "5,:3", "6,:1 7,:1 1:1", "2:3", "1:3"]          # 足もと：E4〜B4
MID = ["1:2 2:1", "3:3", "4:2 3:1", "2:3", "3:2 4:1", "5:3", "4:1 3:1 2:1", "3:3"]               # 壁：A4〜E5
HIGH = ["3:2 4:1", "5:3", "4:2 5:1", "5:3", "3:1 4:1 5:1", "5:2 4:1", "3:2 4:1", "5:3"]          # 天井：C♯5〜E5（E5 にとどまる）
play_melody(c, "足もと", LOW * 3, 4, "air", key=K, density=0.15, seed=4901)
play_melody(c, "壁", MID * 3, 4, "air", key=K, density=0.2, seed=4902)
play_melody(c, "天井", HIGH * 3, 4, "air", key=K, density=0.2, seed=4903)
play_melody(c, "一筋", ["5:3", "6:3", "7:3"], 4, "air", key=K, density=0.0)
c.FLUTE.at((c.s0["一筋"] + 3) * B, "A5:18")                 # 一番高い A5 を、切らずに1本だけ

# ---------- マリンバの3音（C♯5・E5・D♯5 のくり返し）と、低い弦の影 ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b)
    MR[b % 2].bar(b, "C#5:1, E5:1, D#5:1," if n != "一筋" else "C#6:1, E6:1, D#6:1,")
ROOT = {"A": 45, "B": 47, "E": 40, "F#m": 42}
for b in range(0, c.NB, 2):
    ch = S.chords[b]; r = ROOT[ch]
    vc, va = (VCI, VAI) if b < 8 else (VC, VA)
    vc.at(b * B, f"{nm(r + 12 if r + 12 <= 52 else r)}:6,"); va.at(round(b * B + 0.05, 3), f"{nm(r + 19 if r + 19 <= 64 else r + 7)}:5.95,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の049（第3版）。蔦におおわれた暗い部屋で、蔦を払うと光が射しこむ。3/4・♩=60、A リディア。マリンバの柔らかい3音（C♯・E・D♯）がくり返し、低い弦の影は光が上がるほど薄くなる。笛の旋律は、足もと → 壁 → 天井と場面ごとに高くなるが E5 より上には行かず、最後にいちばん高い A5 の長い音が、一筋の光として1本だけ射しこむ。",
       harm_scenes=None, tail_scene="一筋", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air049.json", "w"), ensure_ascii=False)
