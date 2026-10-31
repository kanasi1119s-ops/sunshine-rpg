# ケルト・フルート100曲「銀の笛と百の夜」024 川辺の蛙たち The Frogs by the Brook — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 夕方の川辺。蛙たちが低い声で拍をきざみはじめる。エイラが笛で歌いだすと、水車小屋の子どもが2人、
#   木の笛を持って走ってきて、同じ歌を4小節ずつおくれて追いかける（輪唱）。3人で何周も回ったあと、
#   夕飯に呼ばれて1人ずつ帰っていき、最後は蛙の拍だけが残る。
# 調べ: 喜び（のどか）。形: 輪唱（3本の笛が同じ12小節の歌を、4小節ずつおくれて入る）。
# 拍子・速さ: 4/4・♩=58。旋法: G ドリア（4小節の和音 Gm・C・F・Gm を何度も回す。どの4小節も、ほかの4小節と重ねて響くように書いた）。
# 主役は笛（1本目＝エイラ）。脇: 2本目・3本目の笛（子どもたち。左右に。少し小さく）。
# 伴奏の主役: 低い弦のピチカート（蛙の拍）とマリンバ（小さな蛙の声）。竪琴・ギター・ピアノ・長い弦・パッド・打楽器は使わない。
# この曲だけ: 3本の笛が同じ節を追いかける輪唱。最後は入った順に1本ずつ帰る。
# 始まり: 蛙の拍 → 終わり: 笛が1本ずつ帰り、蛙の拍だけ。
# 山: 中盤に1つ（3周目。3本とも装飾が増え、マリンバが細かくなる）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "024-the-frogs-by-the-brook", "川辺の蛙たち", "The Frogs by the Brook", 58, 4, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("G", "dorian", 4)
CH4 = ["Gm", "C", "F", "Gm"]
SC = [("蛙の拍", 4, "intro"), ("1周目", 12, "verse"), ("2周目", 12, "verse"), ("3周目", 12, "chorus"), ("4周目", 12, "verse"),
      ("帰る", 8, "verse"), ("蛙だけ", 2, "outro")]
for n, L, kd in SC: S.scene(n, L, kd, (CH4 * 4)[:L])
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("蛙の拍", 0, 0.64), ("1周目", 0, 0.68), ("2周目", 0, 0.76), ("3周目", 0, 0.84), ("3周目", 8, 0.9), ("4周目", 0, 0.8),
          ("帰る", 0, 0.72), ("蛙だけ", 0, 0.66), ("蛙だけ", 1, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="蛙の拍", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 2本目の笛（0.16）はエイラの笛より約3dB 大きい → 0.11・0.1（子どもの笛は少し小さく）。ピチカートとマリンバは笛より少し小さい（丁度よい）
F2 = S.track("2本目の笛（子ども・左）", "panflute", patch="flute", volume=0.11, bright=-0.3, pan=-0.4, reverb=0.45, breath=False, barGain=G)
F3 = S.track("3本目の笛（子ども・右）", "panflute", patch="flute", volume=0.1, bright=-0.4, pan=0.45, reverb=0.5, breath=False, barGain=G)
VP = S.track("チェロ（蛙の拍・ピチカート）", "strings", patch="pizzicato", volume=0.12, gainDb=6, pan=-0.1, reverb=0.35, barGain=G)
CB = S.track("コントラバス（ピチカート）", "strings", patch="contrabass", volume=0.08, gainDb=0, pan=0.05, reverb=0.3, sustain=0.5, barGain=G)
MR = S.track("マリンバ（小さな蛙）", "strings", patch="marimba", volume=0.1, pan=0.25, reverb=0.4, barGain=G)

# ---------- 輪唱の歌（G ドリア。1=G4。12小節＝4小節×3。どの4小節も Gm・C・F・Gm の上） ----------
P1 = ["1:1 2:0.5 3:0.5 4:1 5:1", "6:1.5 5:0.5 4:1 3:1", "2:1 4:1 6:1 4:1", "5:2 1:2"]
P2 = ["5:1 7:1 1':2", "1':1 7:1 6:1 5:1", "4:2 6:1 4:1", "5:4"]
P3 = ["3:0.5 3:0.5 3:1 1:2", "6,:0.5 6,:0.5 6,:1 1:2", "2:0.5 2:0.5 2:1 4:1 2:1", "1:2 5,:2"]      # ゲコ・ゲコ・ゲー（蛙のまね）
TUNE = P1 + P2 + P3

def sing(track, start_bar, cycles, dens_of, seed, last_bars=None):
    """start_bar から TUNE を cycles 周。dens_of(周) で装飾の量。last_bars があれば、最後の周はそこまで"""
    for cy in range(cycles):
        bars = TUNE if (cy < cycles - 1 or last_bars is None) else TUNE[:last_bars]
        ev = []
        for j, s_ in enumerate(bars):
            ev += mel_events(K, s_, 4, (start_bar + 12 * cy + j) * B)
        ev = [[round(t, 4), L, m] for t, L, m in ev]
        play(track, ornament(ev, K, 58, "air", B, density=dens_of(cy), seed=seed + cy))

s1 = c.s0["1周目"]
DENS = lambda cy: [0.15, 0.25, 0.45, 0.3][min(cy, 3)]
sing(c.FLUTE, s1, 4, DENS, 2401)                                  # エイラ：4周（帰るの手前まで）
sing(F2, s1 + 4, 4, DENS, 2411)                                   # 子ども1：4小節おくれて入り、4小節おくれて帰る
sing(F3, s1 + 8, 4, DENS, 2421)                                   # 子ども2：8小節おくれて入り、最後に帰る（入った順に1本ずつ帰る）

# ---------- 蛙の拍（ピチカート）とマリンバ ----------
ROOT = {"Gm": 43, "C": 36, "F": 41}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    th = r + (3 if ch.endswith("m") else 4); fi = r + 7
    CB.bar(b, f"{nm(r)}:1 R:1 {nm(r)}:1, R:1")
    VP.bar(b, f"R:0.5 {nm(fi)}:0.5, R:1 R:0.5 {nm(fi)}:0.5, {nm(th)}:0.5, R:0.5")
    if n in ("蛙の拍", "蛙だけ"):
        if i % 2 == 1: MR.bar(b, f"R:3 {nm(fi + 24)}:0.25 {nm(fi + 24)}:0.25 R:0.5")
    elif n == "3周目":                                            # 山：マリンバが細かく
        MR.bar(b, " ".join(f"{nm(x)}:0.5{',' if q % 2 else ''}" for q, x in enumerate((r + 24, th + 24, fi + 24, th + 24, r + 36, fi + 24, th + 24, fi + 24))))
    else:
        MR.bar(b, f"R:1 {nm(fi + 24)}:0.25 {nm(fi + 24)}:0.25 R:0.5 R:1 {nm(th + 24)}:0.5 R:0.5")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の024（第3版）。夕方の川辺で蛙が拍をきざむ。エイラの笛と、水車小屋の子どもたちの2本の笛が、同じ12小節の歌を4小節ずつおくれて追いかける輪唱。4/4・♩=58、G ドリア。伴奏は低い弦のピチカート（蛙の拍）とマリンバ（小さな蛙）。山は3周目、最後は1本ずつ帰って、蛙の拍だけが残る。",
       harm_scenes=None, tail_scene="蛙だけ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.5, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.24, "lp": 3000, "rt": 2.8}}}
json.dump(air, open("/tmp/cel/w/air024.json", "w"), ensure_ascii=False)
