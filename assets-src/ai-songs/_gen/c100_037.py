# ケルト・フルート100曲「銀の笛と百の夜」037 森の主 The Lord of the Wood — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 迷った末にたどり着いた森のいちばん奥。年老いた大鹿（森の主）が横たわり、静かに息を引きとろうとしている。
#   エイラは笛でアイルランドの哀歌（キーニング）を唱える。同じ音を何度も唱えて呼びかけ、嘆き、こらえきれずに上へ叫び、
#   下へ崩れ落ちる。最後に1音だけを置くと、森の主は目を閉じ、エイラを森の者として認める。
# 調べ: 悲しみ。形: 3部の哀歌（呼びかけ → 嘆き → 叫び）。
# 拍子・速さ: 自由（唱える速さ。4/4・♩=56 前後で大きくゆれる）。旋法: D エオリア。
# 主役は笛（唱える笛 → 叫ぶ笛。叫びも硬くせず、柔らかく）。伴奏の主役: 低いホルンと低い弦（コントラバスの D、チェロ）。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 同じ音（A）を何度も唱え、上へ叫んで（C6 まで）、下へ崩れる（半音ずつ D4 まで）。
# 始まり: 低い弦 → 終わり: 1音（D4）を置いて終わる。
# 山: 叫びで1つ。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "037-the-lord-of-the-wood", "森の主", "The Lord of the Wood", 56, 4, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.5})
K = Key("D", "minor", 4)
SC = [("低い弦", 2, "intro", ["Dm", "Dm"]), ("呼びかけ", 20, "verse", (["Dm", "Dm", "Bb", "Dm", "C", "Dm", "Am", "Dm"] * 3)[:20]),
      ("嘆き", 20, "verse", (["Dm", "Bb", "F", "C", "Dm", "Gm", "Am", "Dm"] * 3)[:20]), ("叫び", 13, "chorus", ["Gm", "Bb", "C", "Dm", "F", "Bb", "C", "Dm", "Bb", "Gm", "A", "A", "Dm"]),
      ("1音", 4, "outro", ["Dm"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("低い弦", 0, 0.66), ("呼びかけ", 0, 0.68), ("呼びかけ", 19, 0.72), ("嘆き", 0, 0.74), ("嘆き", 19, 0.78), ("叫び", 0, 0.82), ("叫び", 6, 0.86),
          ("叫び", 12, 0.78), ("1音", 0, 0.68), ("1音", 3, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="低い弦", passing=False, tension=False)
S.fix_avoid = lambda t: 0
S.tempo = [{"bar": 1, "bpm": 52}, {"bar": c.s0["嘆き"] + 1, "bpm": 56, "ramp": 4}, {"bar": c.s0["叫び"] + 1, "bpm": 60, "ramp": 4},
           {"bar": c.s0["叫び"] + 8, "bpm": 50, "ramp": 6}, {"bar": c.s0["1音"] + 1, "bpm": 46}]
B = S.beats
G = c.g()
# 試し書き出し: ホルン（0.06）は笛より約18dB 小さい → 0.15・gainDb 6。コントラバスの D は笛と同じくらい（ずっと鳴るので 0.05→0.03）。チェロは約5dB 小さい
HN = S.track("低いホルン", "brass", patch="horn", volume=0.15, gainDb=6, pan=-0.25, reverb=0.75, barGain=G)
CBS = [S.track(f"コントラバス（D{j + 1}）", "strings", patch="contrabass", volume=0.03, pan=0.05, reverb=0.65, release=0.6, barGain=[round(x * 1.3, 3) for x in G]) for j in range(2)]
VC = S.track("チェロ（嘆き）", "strings", patch="cello", volume=0.014, gainDb=1, pan=0.25, reverb=0.65, release=0.5, barGain=[round(x * 1.4, 3) for x in G])

# ---------- 笛（D エオリア。1=D4。A＝5） ----------
CALL = ["5:1 5:1 5:2", "5:0.5 6:0.5 5:1 5:2", "5:1 5:1 4:1 5:1", "5:4",                 # 呼びかけ：同じ A を何度も唱える
        "5:1 5:0.5 5:0.5 5:2", "6:1 5:1 5:2", "5:1 4:0.5 3:0.5 5:2", "5:4",
        "5:1 5:1 5:1 6:1", "5:2 5:2", "5:0.5 4:0.5 5:1 5:2", "5:4",
        "1':1 7:1 5:2", "5:1 5:1 5:2", "6:1 5:1 4:1 5:1", "5:4",
        "5:1 5:1 5:2", "4:1 5:1 5:2", "5:2 5:2", "5:4"]
LAMENT = ["5:1 4:1 3:2", "2:1 3:1 4:2", "3:1 2:1 1:2", "7,:4",                              # 嘆き：A から下へ、少しずつ
          "1:1 2:1 3:1 4:1", "5:2 4:1 3:1", "2:2 1:1 7,:1", "1:4",
          "3:1 4:1 5:2", "6:1 5:1 4:2", "3:1 2:1 3:2", "4:4",
          "5:1 6:1 7:2", "6:1 5:1 4:2", "3:1 4:1 2:2", "1:4",
          "5:1 5:1 4:1 3:1", "2:2 3:2", "1:2 7,:2", "1:4"]
CRY = ["5:1 6:1 7:2", "1':2 2':2", "3':1 2':1 3':2", "4':2 3':2",                           # 叫び：上へ（B♭5 まで。硬くしないよう、長い音で）
       "5':2 4':1 3':1", "5':4", "6':4",       # 1回目（6.96）は C6 まで上げて叫びが硬かった → B♭5 まで
       "6':1 5':1 4':1 3':1", "2':1 1':1 7:1 6:1", "5:1 4:1 3:1 2:1", "1:2 7,:2", "1:4", "R:4"]   # 下へ崩れる
play_melody(c, "呼びかけ", CALL, 4, "air", key=K, density=0.3, seed=3701)
play_melody(c, "嘆き", LAMENT, 4, "air", key=K, density=0.3, seed=3702)
play_melody(c, "叫び", CRY, 4, "air", key=K, density=0.2, seed=3703)
play_melody(c, "1音", ["R:2 1:2", "1:4", "1:4", "R:4"], 4, "air", key=K, density=0.0)    # 1音を置く（D4）

# ---------- 低い弦とホルン ----------
ROOT = {"Dm": 38, "Bb": 46, "C": 48, "Am": 45, "F": 41, "Gm": 43, "A": 45}
end = (c.s0["1音"] + 3) * B
st, k = 0.0, 0
while st < end - 0.01:                                                 # コントラバスの D（2小節ごとに交互に弓を返す）
    en = min(end, st + 8.2)
    CBS[k % 2].at(round(st, 3), f"D2:{round(en - st, 3)}{',' if st else ''}")
    st += 8; k += 1
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    th = r + (3 if ch.endswith("m") else 4)
    if n == "呼びかけ" and i % 4 == 3:                                  # 唱える句の終わりに、ホルンが低く答える
        HN.at(b * B, f"{nm(th if th >= 50 else th + 12)}:4,")
    if n == "嘆き":
        VC.at(b * B, f"{nm(th if th >= 48 else th + 12)}:4,")
        if i % 2 == 0: HN.at(b * B, f"{nm(r + 12 if r + 12 <= 62 else r)}:{2 * B},")
    if n == "叫び" and i < 11:
        VC.at(b * B, f"{nm(th if th >= 48 else th + 12)}:4")
        HN.at(b * B, f"{nm(r + 12 if r + 12 <= 62 else r)}:4{'!' if i == 6 else ''}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の037（第3版）。森のいちばん奥で、年老いた森の主（大鹿）が息を引きとろうとしている。アイルランドの哀歌（キーニング）のように、笛が同じ音（A）を何度も唱えて呼びかけ、嘆き、上へ叫んで（C6 まで）、下へ崩れ落ちる。自由な速さ、D エオリア。伴奏は低いホルンと低い弦（コントラバスの D とチェロ）。最後に1音（D）を置いて終わる。",
       harm_scenes=None, tail_scene="1音", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.32, "lp": 2600, "rt": 4.2}}}
json.dump(air, open("/tmp/cel/w/air037.json", "w"), ensure_ascii=False)
