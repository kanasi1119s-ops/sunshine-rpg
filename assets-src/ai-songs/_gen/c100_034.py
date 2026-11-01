# ケルト・フルート100曲「銀の笛と百の夜」034 苔の絨毯 The Moss Carpet — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 梟と別れた夜ふけ。森の奥に、ふかふかの苔が一面に広がる場所がある。エイラは横になり、笛で子守歌を吹く。
#   吹くたびに体は苔に沈みこみ、歌も1回ごとに低く沈んでいく。最後は、笛とコントラバスのいちばん低い音で眠りに落ちる。
# 調べ: 眠り。形: 沈みこむ子守歌（16小節の歌を4回。1回ごとに全体が3度ずつ下がる）。
# 拍子・速さ: 3/4・♩=54 → 最後で 48。調: E♭ → C → A♭ → F（3度ずつ下がる）。
# 主役は笛（低い所へ沈む。1回目 B♭4〜B♭5 → 4回目 C4〜C5）。伴奏の主役: チェロ（ゆりかごの根音と5度）。3回目からコントラバス。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 1周ごとに全体が3度ずつ下がっていく（つなぎの2小節で、チェロが先に3度下へ沈む）。
# 始まり: 低い音（チェロのゆりかご）→ 終わり: 笛とコントラバスのいちばん低い音（笛 C4・コントラバス F1）。
# 山: 前半に1つ（2回目）。最初が大きく、だんだん小さくなる形にはしない（始まりはチェロ1本）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "034-the-moss-carpet", "苔の絨毯", "The Moss Carpet", 54, 3, "Eb", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
KEYS = [("Eb", 5), ("C", 5), ("Ab", 4), ("F", 4)]              # 調と、笛の1度のオクターブ
DEG = ["I", "I", "IV", "V", "I", "I", "V", "I", "I", "IV", "IV", "I", "V", "I", "V", "I"]
def chord_names(root):
    r = PC[root]; nmz = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    return [nmz[(r + {"I": 0, "IV": 5, "V": 7}[d]) % 12] for d in DEG]
SC = [("ゆりかご", 2, "intro", ["Eb", "Eb"])]
for k, (rt, o) in enumerate(KEYS):
    SC.append((f"{k + 1}回目", 16, "chorus" if k == 1 else "verse", chord_names(rt)))
    if k < 3: SC.append((f"沈む{k + 1}", 2, "verse", [KEYS[k + 1][0]] * 2))
SC.append(("眠り", 4, "outro", ["F"] * 4))
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ゆりかご", 0, 0.66), ("1回目", 0, 0.72), ("2回目", 0, 0.8), ("2回目", 8, 0.86), ("3回目", 0, 0.74), ("4回目", 0, 0.7),
          ("眠り", 0, 0.66), ("眠り", 3, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ゆりかご", passing=True, tension=False)
S.fix_avoid = lambda t: 0
S.tempo = [{"bar": 1, "bpm": 54}, {"bar": c.s0["4回目"] + 1, "bpm": 51, "ramp": 8}, {"bar": c.s0["眠り"] + 1, "bpm": 48, "ramp": 4}]
B = S.beats
G = c.g()
# 試し書き出し: チェロ E♭3 は笛より約3dB 小さく、F2（強さ 1.1）は笛と同じくらい → gainDb 3→1。コントラバス F1 は笛より約5dB 小さい
# チェロは D3 より下で小さくなる（007 で測った）→ 沈むほど強く
SINK = {"ゆりかご": 1.0, "1回目": 1.0, "沈む1": 1.1, "2回目": 1.15, "沈む2": 1.25, "3回目": 1.35, "沈む3": 1.45, "4回目": 1.55, "眠り": 1.6}
VC = [S.track(f"チェロ（ゆりかご{j + 1}）", "strings", patch="cello", volume=0.03, gainDb=1, pan=-0.15, reverb=0.6, release=0.5,
              barGain=[round(x * SINK[S.scene_of(b)[0]], 3) for b, x in enumerate(G)]) for j in range(2)]
CB = S.track("コントラバス（3回目から）", "strings", patch="contrabass", volume=0.06, gainDb=2, pan=0.1, reverb=0.55, release=0.6,
             barGain=[round(x * 1.4, 3) for x in G])

# ---------- 歌（16小節。調ごとに同じ度数で） ----------
T = ["3:2 2:1", "1:2 5,:1", "6,:1 7,:1 1:1", "2:3", "3:2 4:1", "5:2 3:1", "2:1 3:1 2:1", "1:3",
     "5:2 6:1", "5:1 4:1 3:1", "4:2 2:1", "3:3", "2:1 3:1 4:1", "3:1 2:1 1:1", "7,:2 2:1", "1:3"]
for k, (rt, o) in enumerate(KEYS):
    K = Key(rt, "major", o)
    play_melody(c, f"{k + 1}回目", T, o, "air", key=K, density=[0.25, 0.4, 0.2, 0.1][k], seed=3400 + k)
    if k < 3: play_melody(c, f"沈む{k + 1}", ["1:3", "1:2 R:1"], o, "air", key=K, density=0.0)
play_melody(c, "眠り", ["5,:3", "5,:3", "5,:3", "R:3"], 4, "air", key=Key("F", "major", 4), density=0.0)    # 最後：笛のいちばん低い C4

# ---------- チェロのゆりかご（根音2拍・5度1拍）とコントラバス ----------
LOWROOT = {"Eb": 51, "Ab": 44, "Bb": 46, "C": 48, "F": 41, "G": 43, "Db": 49}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = LOWROOT.get(ch, 48)
    if n.endswith("回目") and n[0] in "34": r = r if r < 46 else r - 12
    if r < 36: r += 12                                            # チェロの最低音 C2 より下にしない
    if n == "眠り":
        if i == 0: VC[0].at(b * B, f"{nm(41)}:{3 * B},"); CB.at(b * B, "F1:9")
        continue
    if n.startswith("沈む"):                                        # つなぎ：チェロが先に3度下へ沈む
        nxt = LOWROOT[S.chords[b]]
        VC[b % 2].bar(b, f"{nm(r)}:3,")
        continue
    VC[b % 2].bar(b, f"{nm(r)}:2 {nm(r + 7)}:1,")
    if n in ("3回目", "4回目") and i % 2 == 0:
        CB.at(b * B, f"{nm(r - 12 if r - 12 >= 28 else r)}:{2 * B},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.32 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の034（第3版）。森の奥の苔の上で眠りにつく子守歌。3/4・♩=54 → 48。同じ16小節の歌を4回、1回ごとに全体が3度ずつ下がる（E♭ → C → A♭ → F）。伴奏はチェロのゆりかご（根音と5度）、3回目からコントラバス。山は2回目、最後は笛とコントラバスのいちばん低い音で眠りに落ちる。",
       harm_scenes=None, tail_scene="眠り", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2600, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air034.json", "w"), ensure_ascii=False)
