# ケルト・フルート100曲「銀の笛と百の夜」067 祭りの前夜 The Eve of the Festival — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 明日は村の祭り。広場では前の晩から、手をつないだ輪の踊りが始まる。はじめは力強く、途中で一度ゆるやかな「休みの踊り」になり、
#   夜がふけるほど速く、熱くなる。いちばん速くなったところで、全員がぴたりと止まる。
# 調べ: 喜び。形: ガヴォット型の組曲（踊り ♩=120 → ゆるむ「バル」♩=90 → もっと速く ♩=132 へ）。
# 拍子・速さ: 4/4・♩=120 → 90 → 132。旋法: D エオリア。
# 主役は笛（熱い笛）。伴奏の主役: フィドル（笛の1オクターブ下で一緒に。バルでは長い音）とアコーディオン（裏拍の「チャッ」、バルでは長い和音）。
#   打楽器はボーラン。竪琴・ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 組曲の真ん中で一度ゆるめて（谷）、また燃える。最後は速さの頂点で止まる。
# 始まり: 太鼓だけ → 終わり: 速さの頂点で止まる。
# 山: 中心に谷（バル）。最後が頂点。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "067-the-eve-of-the-festival", "祭りの前夜", "The Eve of the Festival", 120, 4, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("D", "minor", 4)
CA = ["Dm", "Gm", "F", "Dm", "Dm", "Gm", "C", "Dm"]; CB = ["Dm", "F", "C", "Bb", "Dm", "F", "C", "Dm"]
SC = [("太鼓", 2, "intro", ["Dm", "Dm"]), ("踊り", 48, "verse", (CA * 2 + CB * 2) + CA + CB), ("バル", 24, "verse", CA + CB + CA),
      ("もっと速く", 48, "chorus", (CA * 2 + CB * 2) + CA * 2), ("止まる", 1, "outro", ["Dm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("太鼓", 0, 0.8), ("踊り", 0, 0.8), ("踊り", 47, 0.86), ("バル", 0, 0.66), ("バル", 23, 0.7), ("もっと速く", 0, 0.82), ("もっと速く", 47, 0.98), ("止まる", 0, 0.98)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="太鼓", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 120}, {"bar": s["バル"] + 1, "bpm": 90, "ramp": 2}, {"bar": s["もっと速く"] + 1, "bpm": 132, "ramp": 24}]
B = S.beats
G = c.g()
# フィドル（短い音は大きい。044: 0.04 で旋律を一緒に）→ 1オクターブ下で 0.028。アコーディオン（060: 裏拍の短い音は笛の約5dB 下、長い和音は ×0.45）
FD = S.track("フィドル", "strings", patch="violin", volume=0.028, pan=-0.3, reverb=0.3, barGain=G)
ACG = {"バル": 0.45}
AC = [S.track(f"アコーディオン{j + 1}", "accordion", volume=0.05, pan=0.2 + 0.08 * j, reverb=0.3, barGain=[round(x * ACG.get(S.scene_of(b)[0], 1.0), 3) for b, x in enumerate(G)]) for j in range(3)]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25,
              barGain=[round(x * (1.5 if S.scene_of(b)[0] == "太鼓" else 1.0), 3) for b, x in enumerate(G)]) for j in range(2)]

# ---------- 節（8分＝0.5。1=D4） ----------
A = ["1:0.5 2:0.5 3:0.5 4:0.5 5:1 5:1", "6:0.5 5:0.5 4:0.5 3:0.5 4:1 2:1", "3:0.5 4:0.5 5:0.5 1':0.5 7:1 5:1", "4:0.5 3:0.5 2:0.5 3:0.5 1:2",
     "1:0.5 2:0.5 3:0.5 4:0.5 5:1 5:1", "6:0.5 5:0.5 4:0.5 3:0.5 4:0.5 5:0.5 6:1", "5:0.5 4:0.5 3:0.5 2:0.5 3:0.5 2:0.5 7,:1", "1:1 5,:1 1:2"]
Bm = ["5:1 1':1 1':0.5 7:0.5 6:1", "7:0.5 6:0.5 5:0.5 4:0.5 5:2", "6:1 2':1 2':0.5 1':0.5 7:1", "1':0.5 7:0.5 6:0.5 5:0.5 6:2",
      "5:1 1':1 1':0.5 7:0.5 6:1", "7:0.5 6:0.5 5:0.5 4:0.5 3:0.5 4:0.5 5:1", "4:0.5 3:0.5 2:0.5 3:0.5 2:0.5 1:0.5 7,:1", "1:1 5,:1 1:2"]
PLAN = [("踊り", A + A + Bm + Bm + A + Bm, "reel", 0.4), ("バル", A + Bm + A, "air", 0.2), ("もっと速く", A + A + Bm + Bm + A + A, "reel", 0.55)]
for k, (sc, bars, kind, dens) in enumerate(PLAN):
    s0 = s[sc]; ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 120, kind, B, density=dens, seed=6700 + k))
    if sc != "バル":
        play(FD, [(t, L, (m - 12 if m - 12 >= 55 else m), ("!" if abs(t % B) < 1e-6 else ",")) for t, L, m in ev])
s0 = s["止まる"]
c.FLUTE.at(s0 * B, "D5:0.6!"); FD.at(s0 * B, "D4:0.6!")

# ---------- 伴奏 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    voice = [near(r, 57), near(th, 57), near(fi, 57)]
    d = DR[b % 2]
    if n == "太鼓":
        d.bar(b, "C3:1! E3:0.5, E3:0.5, C3:1 E3:0.5, C3:0.5,"); continue
    if n == "止まる":
        d.bar(b, "C3:0.6! R:3.4")
        for j, m in enumerate(voice): AC[j].at(round(b * B + 0.02 * j, 3), f"{nm(m)}:0.6!")
        continue
    if n == "バル":                                            # ゆるむ：アコーディオンの長い和音、フィドルの長い音、太鼓は1小節に2打だけ
        if i % 2 == 0:
            for j, m in enumerate(voice): AC[j].at(round(b * B + 0.04 * j, 3), f"{nm(m)}:{2 * B - 0.1}{',' if j else ''}")
            FD.at(round(b * B + 0.1, 3), f"{nm(near(fi, 62))}:{2 * B - 0.2},")
        d.bar(b, "C3:1, R:1 E3:1, R:1")
        continue
    fill = (i % 16 == 15)
    for j, m in enumerate(voice):
        AC[j].bar(b, f"R:0.5 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.2")
    if fill:
        d.bar(b, "C3:0.5! E3:0.5, C3:0.5! E3:0.5, C3:0.25! C3:0.25! C3:0.5! C3:0.5! C3:0.5!")
    else:
        d.bar(b, "C3:1! E3:0.5, E3:0.5, C3:1 E3:0.5, C3:0.5," if n == "踊り" else "C3:0.5! E3:0.5, C3:0.5 E3:0.5, C3:0.5! E3:0.5, C3:0.5 E3:0.5,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.2 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の067（第3版）。祭りの前の晩、広場の輪の踊り。4/4、D エオリア。ボーランだけで始まり、ガヴォット型の組曲として、力強い踊り（♩=120）→ 真ん中で一度ゆるむ「バル」（♩=90。アコーディオンとフィドルの長い音、太鼓は1小節に2打）→ だんだん速く熱く（♩=132 へ）。笛の下でフィドルが1オクターブ下を一緒に弾き、アコーディオンが裏拍を刻む。速さの頂点で、全員がぴたりと止まる。",
       harm_scenes=None, tail_scene="止まる", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.15, "lp": 3000, "rt": 1.8}}}
json.dump(air, open("/tmp/cel/w/air067.json", "w"), ensure_ascii=False)
