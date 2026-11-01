# ケルト・フルート100曲「銀の笛と百の夜」072 雨の始まり When the Rain Began — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 岬に着くと、冷たい雨が降りだす。灰色の雲の下、音はすぐに雨に吸いこまれて、響かない。
#   エイラは岩かげで笛を吹き続ける。やがて雲が切れ、光が海に差しこむと、同じ節が長調になって、響きが一気に広がる。
# 調べ: あいだ。形: 雨のエア（C エオリア。16小節×2 → 8小節）→ 雲が切れる2小節 → 同じ節が C の長調で広がる（28小節）。
# 拍子・速さ: 4/4・♩=66（雨の所はゆれを大きく）。旋法: C エオリア → C イオニア。
# 主役は笛（乾いた笛 → 広がる笛）。伴奏の主役: 竪琴（雨では乾いた雨粒の分散和音、晴れると大きく広がる）。脇: 弦の弱奏（チェロとビオラ。晴れるとバイオリンも）。
#   ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 雨の部分は響きを短く乾かし（どのパートも残響をほとんどなし）、雲が切れた瞬間に、同じ楽器の「響きの長いパート」に入れかわって響きが開く。
# 始まり: 乾いた雨の音楽 → 終わり: 響きが一気に広がる。
# 山: 最後。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "072-when-the-rain-began", "雨の始まり", "When the Rain Began", 66, 4, "C", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
KM, KJ = Key("C", "minor", 4), Key("C", "major", 4)
CR = ["Cm", "Bb", "Cm", "Bb", "Cm", "Fm", "Bb", "Cm", "Fm", "Cm", "Bb", "Cm", "Ab", "Eb", "Gm", "Cm"]
CRB = ["Cm", "Bb", "Ab", "Fm", "Ab", "Cm", "Fm", "G"]
MAJ = {"Cm": "C", "Bb": "G", "Fm": "F", "Ab": "Am", "Eb": "Em", "Gm": "G"}
CO = [MAJ[x] for x in CR] + [MAJ[x] for x in CR[:8]] + ["F", "G", "C", "C"]
SC = [("雨", 32, "verse", CR * 2), ("強い雨", 8, "verse", CRB), ("雲が切れる", 2, "verse", ["G", "G"]), ("光", 28, "chorus", CO)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("雨", 0, 0.7), ("強い雨", 0, 0.76), ("雲が切れる", 0, 0.72), ("光", 0, 0.84), ("光", 24, 0.94), ("光", 27, 0.86)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="雨", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
DRY = {n: (n in ("雨", "強い雨")) for n in NAMES}
c.FLUTE.spec["reverb"] = 0.03                                    # 雨の笛：響きをほとんどなしに
FLW = S.track("フルート（雲が切れた後）", "panflute", **dict(c.FLUTE.spec, reverb=0.95))
HPD = [S.track(f"竪琴（乾いた雨粒{j + 1}）", "harp", patch="folkHarp", volume=0.075, pan=-0.2 + 0.4 * j, reverb=0.02, sustain=0.5, barGain=G) for j in range(2)]
HPW = [S.track(f"竪琴（広がる{j + 1}）", "harp", patch="folkHarp", volume=0.075, pan=-0.35 + 0.35 * j, reverb=0.95, sustain=2.2, barGain=G) for j in range(3)]
mk = lambda name, patch, v, gd, pan, rv: S.track(name, "strings", patch=patch, volume=v, gainDb=gd, pan=pan, reverb=rv, release=(0.2 if rv < 0.1 else 1.0), barGain=G)
VCD, VAD = mk("チェロ（乾いた弱奏）", "cello", 0.02, 2, -0.25, 0.03), mk("ビオラ（乾いた弱奏）", "viola", 0.017, 0, 0.15, 0.03)
VCW, VAW, VNW = mk("チェロ（広がる）", "cello", 0.02, 2, -0.3, 0.95), mk("ビオラ（広がる）", "viola", 0.017, 0, 0.1, 0.95), mk("バイオリン（広がる）", "violin", 0.03, 4, 0.35, 0.95)

# ---------- 笛（同じ節：雨は C エオリア、光は C の長調） ----------
R = ["5:2 4:1 3:1", "4:2 2:2", "3:1 2:1 1:2", "2:3 R:1", "5:2 6:1 5:1", "4:2 3:2", "2:1 3:1 4:1 2:1", "1:3 R:1",
     "6:2 5:1 4:1", "5:2 3:2", "4:1 3:1 2:2", "3:3 R:1", "1':2 7:1 6:1", "5:2 4:2", "3:1 2:1 3:1 2:1", "1:4"]
RB = ["5:4", "4:4", "3:4", "2:4", "3:2 4:2", "5:4", "6:2 5:2", "5:4"]
def put(track, key, bars, oct_, b0, dens, seed):
    ev = []
    for j, s_ in enumerate(bars): ev += mel_events(key, s_, oct_, (b0 + j) * B)
    play(track, ornament([[round(t, 4), L, m] for t, L, m in ev], key, 66, "air", B, density=dens, seed=seed))
put(c.FLUTE, KM, R + R, 4, c.s0["雨"], 0.2, 7201)
put(c.FLUTE, KM, RB, 4, c.s0["強い雨"], 0.15, 7202)
c.FLUTE.at(c.s0["雲が切れる"] * B, "D5:4"); FLW.at(c.s0["雲が切れる"] * B + 4, "B4:4,")
put(FLW, KJ, R, 4, c.s0["光"], 0.25, 7203)
put(FLW, KJ, R[:8], 5, c.s0["光"] + 16, 0.3, 7204)
put(FLW, KJ, ["3:4", "2:4", "1:4", "1:4"], 5, c.s0["光"] + 24, 0.0, 7205)

# ---------- 竪琴と弦 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 48)
    if DRY[n]:                                                     # 雨：乾いた8分の雨粒（短く）
        notes = [lo, lo + 7, near(th, lo + 12), lo + 12, near(fi, lo + 12), near(th, lo + 12), lo + 7, lo + 12]
        for q, m in enumerate(notes):
            HPD[q % 2].at(round(b * B + 0.5 * q, 3), f"{nm(m)}:0.35{'' if q == 0 else ','}")
        if b % 2 == 0:
            VCD.at(b * B, f"{nm(near(r, 36))}:{2 * B - 0.1},"); VAD.at(round(b * B + 0.05, 3), f"{nm(near(th, 55))}:{2 * B - 0.15},")
    elif n == "雲が切れる":
        if i == 0:
            VCW.at(b * B, "G2:8"); VAW.at(b * B + 0.05, "D4:7.9,"); VNW.at(b * B + 4, "B4:4,")
            for q, m in enumerate((43, 50, 55, 59, 62, 67, 71, 74)): HPW[q % 3].at(round(b * B + 4 + 0.25 * q, 3), f"{nm(m)}:4,")
    else:                                                          # 光：広い分散和音（2オクターブ）と、響きの長い弦
        notes = [near(r, 36), near(fi, 43), near(r, 48), near(th, 52), near(fi, 55), near(r, 60), near(th, 64), near(fi, 67)]
        for q, m in enumerate(notes):
            HPW[q % 3].at(round(b * B + 0.5 * q, 3), f"{nm(m)}:1.5{'' if q == 0 else ','}")
        if b % 2 == 0:
            VCW.at(b * B, f"{nm(near(r, 36))}:{2 * B + 0.3}"); VAW.at(round(b * B + 0.05, 3), f"{nm(near(th, 55))}:{2 * B + 0.25},")
            VNW.at(round(b * B + 0.1, 3), f"{nm(near(fi, 67))}:{2 * B + 0.2},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.12 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の072（第3版）。岬に着くと冷たい雨が降りだし、音は雨に吸いこまれて響かない。4/4・♩=66。C エオリアの雨のエアは、笛も竪琴（乾いた8分の雨粒）も弦の弱奏も、響きをほとんどなくした乾いた音。2小節で雲が切れると、同じ節が C の長調になり、同じ楽器の響きの長いパートに入れかわって、響きが一気に広がる（竪琴は2オクターブに開き、バイオリンも加わる）。最後が山。",
       harm_scenes=None, tail_scene="光", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 6.0, "layers": [{"file": "0595", "db": -46, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -28, "delay": 0.3, "lp": 2800, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air072.json", "w"), ensure_ascii=False)
