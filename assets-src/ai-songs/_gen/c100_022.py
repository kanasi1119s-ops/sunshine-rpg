# ケルト・フルート100曲「銀の笛と百の夜」022 止まった水車 The Stilled Mill-Wheel — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 小川をたどると、古い水車小屋がある。水車は苔むして、何年も止まったまま。エイラが笛で語りかけると、
#   車軸がぎい、と鳴り、羽根がひとつ、またひとつ水をつかみはじめる。回るほどに軽くなり、最後は勢いよく回り続ける。
# 調べ: あいだ。形: 拍のない前奏（語りかけ）→ 回りだす3拍子。
# 拍子・速さ: 前奏は ♩=40 で大きくゆれる → 3/4・♩=40 から 60 へ、曲全体で少しずつ上がる（テンポそのものが物語）。旋法: D エオリア。
# 主役は笛（語りかける笛）。伴奏の主役: チェロとコントラバスのきしみ（ピチカートの3拍子）。前奏だけ、チェロの低い長い音。
#   竪琴・ギター・ピアノ・パッド・打楽器・高い弦は使わない。
# この曲だけ: テンポが 40 から 60 へ少しずつ上がる（水車が回りだす）。ピチカートは、最初は1拍目だけ（ぎい…）→ 1・2・3拍 → 8分で回る。
# 始まり: 低い持続ときしみ → 終わり: 勢いよく回り続けたまま、最後のきしみ1つ。
# 山: 終盤に1つ（勢いよく）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "022-the-stilled-mill-wheel", "止まった水車", "The Stilled Mill-Wheel", 40, 3, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("D", "minor", 4)
CA = ["Dm", "Dm", "C", "Dm", "Dm", "Bb", "C", "Dm"]
CB = ["F", "C", "Dm", "Am", "Bb", "F", "C", "Dm"]
SC = [("止まった", 6, "intro", ["Dm"] * 6), ("動きだす", 16, "verse", CA + CB), ("回る1", 16, "verse", CA + CB),
      ("回る2", 16, "verse", CA + CB), ("勢いよく", 16, "chorus", CA + CB), ("回り続ける", 6, "outro", ["Dm", "C", "Dm", "C", "Dm", "Dm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("止まった", 0, 0.64), ("動きだす", 0, 0.66), ("回る1", 0, 0.72), ("回る2", 0, 0.78), ("勢いよく", 0, 0.84), ("勢いよく", 12, 0.92),
          ("回り続ける", 0, 0.86), ("回り続ける", 5, 0.82)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="止まった", passing=True, tension=False)
B = S.beats
s = c.s0
S.tempo = [{"bar": 1, "bpm": 40}, {"bar": s["動きだす"] + 1, "bpm": 40},
           {"bar": s["回る1"] + 1, "bpm": 45, "ramp": 16}, {"bar": s["回る2"] + 1, "bpm": 50, "ramp": 16},
           {"bar": s["勢いよく"] + 1, "bpm": 55, "ramp": 16}, {"bar": s["回り続ける"] + 1, "bpm": 60, "ramp": 16}]
S.extra.update({"rubato": 0.5})
G = c.g()
# 試し書き出し: 長いチェロ（gainDb 8）は笛より少し大きい → 5。ピチカート（gainDb 6）は笛と同じくらい。コントラバスの1打目は笛より大きい → gainDb 0
# 長いチェロは D3 より下で小さく、立ち上がりも遅い（007 で測った）→ D3 で、gainDb 8
VCL = S.track("チェロ（止まった車軸の低い音）", "strings", patch="cello", volume=0.1, gainDb=5, pan=-0.1, reverb=0.55, barGain=[round(x * 1.5, 3) for x in G])
# ピチカートは笛より約10dB 小さい（014 で測った）→ gainDb 6
VCP = S.track("チェロ（ピチカートのきしみ）", "strings", patch="pizzicato", volume=0.12, gainDb=6, pan=-0.25, reverb=0.4, barGain=G)
VCP2 = S.track("チェロ（ピチカートの裏）", "strings", patch="pizzicato", volume=0.1, gainDb=6, pan=-0.35, reverb=0.4, barGain=G)
CBP = S.track("コントラバス（ピチカート）", "strings", patch="contrabass", volume=0.09, gainDb=0, pan=0.15, reverb=0.35, sustain=0.5, barGain=G)

# ---------- 旋律（D エオリア。1=D4） ----------
A = ["1:2 3:1", "4:1 5:1 3:1", "2:2 1:1", "7,:3", "1:1 3:1 5:1", "6:2 5:1", "4:1 3:1 2:1", "1:3"]
Bm = ["5:2 6:1", "7:1 1':1 6:1", "5:2 4:1", "3:3", "4:1 5:1 6:1", "5:1 4:1 3:1", "2:1 7,:1 2:1", "1:3"]
TALK = ["R:1 1:2", "3:2 2:1", "1:1 7,:1 6,:1", "7,:3", "R:1 3:1 4:1", "5:3"]              # 語りかけ（拍を感じさせない）
play_melody(c, "止まった", TALK, 4, "air", key=K, density=0.2, seed=2201)
play_melody(c, "動きだす", A + Bm, 4, "air", key=K, density=0.15, seed=2202)
play_melody(c, "回る1", A + Bm, 4, "march", key=K, density=0.25, seed=2203)
play_melody(c, "回る2", [x for x in Bm] + A, 4, "march", key=K, density=0.35, seed=2204)
UP = ["5:1 1':1 3':1", "4':1 5':1 3':1", "2':2 1':1", "7:3", "1':1 3':1 5:1", "6:2 5:1", "4:1 3:1 2:1", "1:3"]   # 勢いよく：A を1オクターブ上から
play_melody(c, "勢いよく", UP + Bm, 4, "march", key=K, density=0.45, seed=2205)
play_melody(c, "回り続ける", ["1:1 3:1 5:1", "4:1 3:1 2:1", "1:1 3:1 5:1", "4:1 3:1 2:1", "1:3", "R:3"], 4, "march", key=K, density=0.3, seed=2206)

# ---------- きしみと回転 ----------
ROOT = {"Dm": 38, "C": 36, "Bb": 34, "F": 41, "Am": 45}
CREAK = ["R:1.3 A2:0.5, R:1.2", "D3:0.6 R:2.4", "R:2.2 E3:0.4, R:0.4", "R:0.5 A2:0.4, R:0.6 D3:0.5, R:1", "D3:0.6 R:2.4", "R:1.5 A2:0.5, D3:0.5,  R:0.5"]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    th = (r + (3 if ch.endswith("m") else 4)); fi = r + 7
    if n == "止まった":
        VCL.bar(b, "D3:3")                                    # 止まった車軸の低い音
        VCP.bar(b, CREAK[i])                                   # ぎい…（拍のないきしみ）
        continue
    if n == "動きだす":                                        # 1拍目だけ（ぎい…ごとん）
        CBP.bar(b, f"{nm(r)}:1 R:2")
        if i % 2 == 1: VCP.bar(b, f"R:2 {nm(fi)}:1,")
        continue
    if n == "回る1":                                            # 1・2・3拍
        CBP.bar(b, f"{nm(r)}:1 R:2")
        VCP.bar(b, f"R:1 {nm(th + 12)}:1, {nm(fi + 12)}:1,")
        continue
    if n in ("回る2", "勢いよく", "回り続ける"):                  # 8分で回る（勢いよくは上の音も）
        if n == "回り続ける" and i == 5:
            CBP.bar(b, f"{nm(38)}:1 R:2"); VCP.bar(b, "R:1.5 A2:0.5, R:1"); continue    # 最後のきしみ1つ
        CBP.bar(b, f"{nm(r)}:1 {nm(fi)}:1, {nm(r)}:1,")
        VCP.bar(b, " ".join(f"{nm(x + 12)}:0.5{',' if q % 2 else ''}" for q, x in enumerate((r, fi, th, fi, r + 12, fi))))
        if n != "回る2":
            VCP2.bar(b, " ".join(f"{nm(x + 12)}:0.5," for x in (fi, th + 12, fi, th + 12, fi, r + 12)))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.28 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の022（第3版）。苔むして何年も止まっていた水車に、エイラが笛で語りかける。拍のない語りかけのあと、3/4 の回転が ♩=40 から 60 へ曲全体で少しずつ速くなる。D エオリア。伴奏はチェロとコントラバスのピチカートのきしみで、最初は1拍目だけ、次に3拍、最後は8分で勢いよく回る。最後は回り続けたまま、きしみ1つで終わる。",
       harm_scenes=None, tail_scene="回り続ける", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 4.5, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.26, "lp": 3000, "rt": 2.8}}}
json.dump(air, open("/tmp/cel/w/air022.json", "w"), ensure_ascii=False)
