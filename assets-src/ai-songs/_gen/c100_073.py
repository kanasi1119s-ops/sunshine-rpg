# ケルト・フルート100曲「銀の笛と百の夜」073 荒れる海 The Raging Sea — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 岬の先で嵐になる。風が強くなるたびに、波は高く、空は暗くなる。エイラは風に負けないよう、力いっぱい笛を吹く。
#   いちばん激しくなったとき、ふいに風がやみ、笛の長い1音だけが残る。
# 調べ: あいだ。形: 嵐のリールのセット（同じリールを、調を上げながら3回: E ドリア AABB+AA → F♯ ドリア AABB → A ミクソリディア AABB+AA）。
# 拍子・速さ: 4/4・♩=116 → 120 → 124。
# 主役は笛（風に負けない笛）。伴奏の主役: 弦の速い刻み（バイオリンとビオラの16分）とボーラン。脇: フィドル2本（笛の1オクターブ下と、同じ高さでごく小さく）・コントラバス。
#   竪琴・ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 調が上がるたびに風が強くなる（速さが上がり、弦の刻みが厚くなり、ボーランが詰まる）。
# 始まり: いきなり全員 → 終わり: 急に止まり、笛の長い1音。
# 山: 階段（回ごとに一段ずつ強く）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "073-the-raging-sea", "荒れる海", "The Raging Sea", 120, 4, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
KEYS = [Key("E", "dorian", 4), Key("F#", "dorian", 4), Key("A", "mixolydian", 4)]
NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def chords(root, mixo, seq):
    """度数（i・VII・IV）から和音名を作る"""
    out = []
    for d in seq:
        if d == "i": out.append(NOTE[root] + ("" if mixo else "m"))
        elif d == "VII": out.append(NOTE[(root + 10) % 12])
        else: out.append(NOTE[(root + 5) % 12])
    return out
DA = ["i", "VII", "i", "i", "i", "VII", "IV", "i"]; DB = ["i", "VII", "i", "IV", "i", "VII", "IV", "i"]
C1 = chords(4, False, DA * 2 + DB * 2 + DA * 2); C2 = chords(6, False, DA * 2 + DB * 2); C3 = chords(9, True, DA * 2 + DB * 2 + DA * 2)
SC = [("E の風", 48, "verse", C1), ("F♯ の風", 32, "verse", C2), ("A の風", 48, "chorus", C3), ("風がやむ", 4, "outro", ["A"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("E の風", 0, 0.78), ("E の風", 47, 0.82), ("F♯ の風", 0, 0.84), ("F♯ の風", 31, 0.88), ("A の風", 0, 0.9), ("A の風", 47, 0.98), ("風がやむ", 0, 0.8)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="E の風", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 116}, {"bar": s["F♯ の風"] + 1, "bpm": 120}, {"bar": s["A の風"] + 1, "bpm": 124}, {"bar": s["風がやむ"] + 1, "bpm": 124}]
B = S.beats
G = c.g()
FL = S.track("フィドル（低い・1オクターブ下）", "strings", patch="violin", volume=0.026, pan=-0.3, reverb=0.3, barGain=G)
FH = S.track("フィドル（高い・同じ高さ）", "strings", patch="violin", volume=0.01, pan=0.3, reverb=0.3, barGain=G)
TR = [S.track(f"弦の刻み（{x}）", "strings", patch=p, volume=v, pan=pn, reverb=0.35, barGain=G) for x, p, v, pn in (("バイオリン", "violin", 0.011, 0.4), ("ビオラ", "viola", 0.009, -0.4))]
CB_ = S.track("コントラバス", "strings", patch="contrabass", volume=0.03, gainDb=3, pan=-0.1, reverb=0.35, release=0.25, barGain=G)
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]

# ---------- リール（8分＝0.5。同じ節を、調を上げて） ----------
A = ["1:0.5 3:0.5 5:0.5 3:0.5 1:0.5 3:0.5 5:0.5 1':0.5", "7:0.5 5:0.5 4:0.5 5:0.5 7,:0.5 4:0.5 2:0.5 4:0.5",
     "1:0.5 3:0.5 5:0.5 3:0.5 1:0.5 3:0.5 5:0.5 6:0.5", "7:0.5 5:0.5 4:0.5 2:0.5 3:0.5 1:0.5 1:1",
     "1:0.5 3:0.5 5:0.5 3:0.5 1:0.5 3:0.5 5:0.5 1':0.5", "7:0.5 5:0.5 4:0.5 5:0.5 7,:0.5 4:0.5 2:0.5 4:0.5",
     "1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 2:0.5 7,:0.5 2:0.5", "3:0.5 1:0.5 2:0.5 7,:0.5 1:2"]
Bm = ["5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5 1':0.5", "7:0.5 5:0.5 5:0.5 4:0.5 5:0.5 6:0.5 7:0.5 5:0.5",
      "5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5 2':0.5", "1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 2:0.5 7,:0.5 2:0.5",
      "5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5 1':0.5", "7:0.5 5:0.5 5:0.5 4:0.5 5:0.5 6:0.5 7:0.5 5:0.5", A[6], A[7]]
B3 = [x.replace("3':", "1':") for x in Bm]                       # A の調では C♯6 が高すぎるので、いちばん上を A5 に
PLAN = [("E の風", A + A + Bm + Bm + A + A, 0), ("F♯ の風", A + A + Bm + Bm, 1), ("A の風", A + A + B3 + B3 + A + A, 2)]
for k, (sc, bars, ki) in enumerate(PLAN):
    K = KEYS[ki]; s0 = s[sc]; ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 120, "reel", B, density=(0.4, 0.5, 0.6)[k], seed=7300 + k))
    play(FL, [(t, L, (m - 12 if m - 12 >= 55 else m), ("!" if abs(t % 2) < 1e-6 else ",")) for t, L, m in ev])
    if k >= 1: play(FH, [(t, L, m, ",") for t, L, m in ev])
s0 = s["風がやむ"]
c.FLUTE.at(s0 * B, "E5:15")                                      # 風がやみ、笛の長い1音だけ

# ---------- 弦の刻み・コントラバス・ボーラン（調が上がるほど厚く） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(s["風がやむ"]):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lvl = NAMES.index(n)                                         # 0・1・2：風の強さ
    # 弦の刻み：16分。E では1拍おき、F♯ では毎拍、A では2声とも毎拍
    for j, tr in enumerate(TR):
        if j == 1 and lvl == 0: continue
        m = near(th if j == 0 else fi, 62 if j == 0 else 55)
        beats = [0, 2] if lvl == 0 else [0, 1, 2, 3]
        for q in beats:
            for x in range(4):
                tr.at(round(b * B + q + 0.25 * x, 3), f"{nm(m)}:0.25{'' if x == 0 else ','}")
    lo = near(r, 40)
    CB_.bar(b, f"{nm(lo)}:0.5! R:0.5 {nm(lo + 7 if lo + 7 <= 52 else lo - 5)}:0.5, R:0.5 {nm(lo)}:0.5 R:0.5 {nm(lo + 12 if lo + 12 <= 52 else lo)}:0.5, R:0.5")
    d = DR[b % 2]
    fill = (i % 8 == 7)
    if lvl == 0 and not fill:
        d.bar(b, "C3:0.5! E3:0.5, C3:0.5, E3:0.5 C3:0.5! E3:0.5, C3:0.5, E3:0.5")
    elif fill or lvl == 2:
        d.bar(b, " ".join(["C3:0.25! E3:0.25, C3:0.25, E3:0.25,"] * 3 + ["C3:0.25! C3:0.25! C3:0.25! C3:0.25!" if fill else "C3:0.25! E3:0.25, C3:0.25, E3:0.25,"]))
    else:
        d.bar(b, "C3:0.5! E3:0.25, E3:0.25, C3:0.5 E3:0.5, C3:0.5! E3:0.25, E3:0.25, C3:0.5 E3:0.5,")
# 急に止まる：最後の小節の頭だけ全員
s0 = s["風がやむ"]
CB_.at(s0 * B, "A1:0.5!"); DR[0].at(s0 * B, "C3:0.5!"); FL.at(s0 * B, "A3:0.5!"); TR[0].at(s0 * B, "C#5:0.5!"); TR[1].at(s0 * B, "E4:0.5!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の073（第3版）。岬の先で嵐になる。嵐のリールのセット（4/4）。同じリールを、E ドリア（♩=116）→ F♯ ドリア（120）→ A ミクソリディア（124）と調を上げながら3回。調が上がるたびに風が強くなり、弦の16分の刻みが厚くなって、ボーランが詰まる。フィドル2本が笛の下と同じ高さで一緒に弾き、コントラバスが支える。いちばん激しくなったところで急に止まり、笛の長い1音だけが残る。",
       harm_scenes=None, tail_scene="風がやむ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air073.json", "w"), ensure_ascii=False)
