# ケルト・フルート100曲「銀の笛と百の夜」098 島の目覚め The Island Awakes — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 鐘の音で、島じゅうの人が目をさます。教会の前に集まった人たちが、079 と同じように、先唱者（エイラの笛）に続いて、
#   古い歌を少しずつずれながら歌いはじめる。ずれはだんだんそろい、速くなり、気づけば全員が速いリールを弾いて踊っている。
# 調べ: 喜び。形: 詩篇唱のずれ（4行）→ そろいながら速くなる → リール（AABB×2 → AA）。
# 拍子・速さ: 4/4。詩篇唱は ♩=44 → 4小節で ♩=112 のリールへ。旋法: G ミクソリディア（F♮）。
# 主役は笛（先唱の笛 → 速い笛）。伴奏: フィドル・アコーディオン（詩篇唱ではずれて重なる声、リールでは伴奏）・ギター・ボーラン（全員）。
#   竪琴・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: ずれた重なりがだんだんそろって、気づけば全員がリールを弾いている（リールの節は、詩篇の節を速く細かくしたもの）。
# 始まり: 笛ひとりの1行 → 終わり: 全員で切る。
# 山: 最後。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "098-the-island-awakes", "島の目覚め", "The Island Awakes", 112, 4, "G", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
K = Key("G", "mixolydian", 4)
CA = ["G", "C", "F", "G", "G", "C", "F", "G"]; CB = ["G", "F", "F", "Dm", "G", "F", "F", "G"]
T = CA * 2 + CB * 2
SC = [("先唱", 2, "intro", ["G", "G"]), ("詩篇", 10, "verse", ["G"] * 10), ("そろう", 4, "verse", ["G", "C", "F", "G"]), ("リール1", 32, "verse", T),
      ("リール2", 32, "chorus", T), ("リール3", 16, "chorus", CA * 2), ("切る", 1, "outro", ["G"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("先唱", 0, 0.86), ("詩篇", 0, 0.9), ("詩篇", 9, 0.9), ("そろう", 0, 0.86), ("リール1", 0, 0.84), ("リール2", 0, 0.88), ("リール3", 0, 0.92), ("リール3", 15, 0.98),
          ("切る", 0, 0.98)],
         {}, flute_gain={n: (1.5 if n in ("先唱", "詩篇") else 1.3 if n == "そろう" else 1.15) for n in NAMES}, intro="先唱", passing=True, tension=False)
S.fix_avoid = lambda t: 0
# 1回目（7.64）: 詩篇の所（はじめの約78秒）が −31dB で、リール（−17dB）より14dB 小さかった → 詩篇の場面の大きさ・笛・アコーディオンを上げる
s = c.s0
S.tempo = [{"bar": 1, "bpm": 44}, {"bar": s["そろう"] + 1, "bpm": 112, "ramp": 4}]
B = S.beats
G = c.g()
FD = S.track("フィドル", "strings", patch="violin", volume=0.03, gainDb=3, pan=0.3, reverb=0.4, barGain=G)
ACG = {"先唱": 0.65, "詩篇": 0.65, "そろう": 0.7}
AC = [S.track(f"アコーディオン{j + 1}", "accordion", volume=0.05, pan=0.15 + 0.07 * j, reverb=0.35,
              barGain=[round(x * ACG.get(S.scene_of(b)[0], 1.0), 3) for b, x in enumerate(G)]) for j in range(3)]
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=-0.3 - 0.05 * i, reverb=0.3, barGain=G) for i in range(5)]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]

# ---------- 詩篇の4行（1行＝2小節）。先唱の笛 → 全員が少しずつずれて ----------
L = ["1:2 3:2 5:2 4:1 3:1", "5:2 6:2 7:2 5:2", "1':2 7:1 6:1 5:2 4:2", "3:2 2:2 1:4"]
rng = random.Random(9801)
def line(li, b0, lag, lead=True):
    ev = [[round(t, 4), Ln, m] for t, Ln, m in mel_events(K, L[li], 4, b0 * B)]
    play(c.FLUTE, ornament(ev, K, 44, "air", B, density=0.15, seed=9800 + b0))
    if lead: return
    for tr, d, sh in ((FD, 0.5, -12), (AC[0], 0.25, -12), (AC[1], 0.7, 0)):
        delay = lag * d * rng.uniform(0.7, 1.2)
        play(tr, [(round(t + delay + lag * rng.uniform(0, 0.08), 4), max(0.3, round(Ln - 0.1, 4)), m + sh, ",") for t, Ln, m in ev])
line(0, s["先唱"], 0, lead=True)
for q, (li, lag) in enumerate(((0, 0.9), (1, 0.75), (2, 0.6), (3, 0.45), (1, 0.3))):
    line(li, s["詩篇"] + 2 * q, lag, lead=False)

# ---------- そろって速くなり、リールへ（リールの節は詩篇の節を速く細かくしたもの。1=G4） ----------
A = ["1:0.5 2:0.5 3:0.5 1:0.5 5:0.5 3:0.5 5:0.5 4:0.5", "3:0.5 5:0.5 6:0.5 5:0.5 7:0.5 6:0.5 5:0.5 4:0.5",
     "1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 5:0.5 6:0.5 4:0.5", "3:0.5 2:0.5 1:0.5 7,:0.5 1:1 1:1",
     "1:0.5 2:0.5 3:0.5 1:0.5 5:0.5 3:0.5 5:0.5 4:0.5", "3:0.5 5:0.5 6:0.5 5:0.5 7:0.5 6:0.5 5:0.5 4:0.5",
     "3:0.5 4:0.5 5:0.5 3:0.5 2:0.5 3:0.5 7,:0.5 2:0.5", "1:2 1:2"]
Bm = ["5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5 1':0.5", "7:0.5 6:0.5 5:0.5 6:0.5 7:0.5 5:0.5 4:0.5 5:0.5",
      "6:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5", "6:0.5 5:0.5 4:0.5 3:0.5 2:1 5:1",
      "5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5 1':0.5", "7:0.5 6:0.5 5:0.5 6:0.5 7:0.5 5:0.5 4:0.5 5:0.5",
      "3:0.5 4:0.5 5:0.5 3:0.5 2:0.5 3:0.5 7,:0.5 2:0.5", "1:2 1:2"]
play_melody(c, "そろう", ["1:1 3:1 5:1 4:1", "5:1 6:1 7:1 5:1", "1':1 7:1 6:1 4:1", "3:1 2:1 1:1 7,:1"], 4, "reel", key=K, density=0.1)
for q in range(4): FD.bar(s["そろう"] + q, ["G3:1 B3:1 D4:1 C4:1", "D4:1 E4:1 F4:1 D4:1", "G4:1 F4:1 E4:1 C4:1", "B3:1 A3:1 G3:1 F3:1"][q].replace("F3", "G3"))
for k, (sc, bars) in enumerate((("リール1", A + A + Bm + Bm), ("リール2", A + A + Bm + Bm), ("リール3", A + A))):
    s0 = s[sc]; ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), Ln, m] for t, Ln, m in ev]
    play(c.FLUTE, ornament(ev, K, 112, "reel", B, density=(0.45, 0.55, 0.6)[k], seed=9810 + k))
    play(FD, [(t, Ln, (m - 12 if m - 12 >= 55 else m), ("!" if abs(t % 2) < 1e-6 else ",")) for t, Ln, m in ev])
c.FLUTE.at(s["切る"] * B, "G5:0.6!"); FD.at(s["切る"] * B, "G4:0.6!")

# ---------- 全員の伴奏（リール） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
REEL = [(0, 0.5, "d", "!"), (0.5, 0.5, "u", ","), (1, 0.5, "d", ""), (1.5, 0.5, "u", ","), (2, 0.5, "d", "!"), (2.5, 0.5, "u", ","), (3, 0.5, "d", ""), (3.5, 0.5, "u", ",")]
for b in range(s["リール1"], c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    voice = [near(r, 57), near(th, 57), near(fi, 57)]
    if n == "切る":
        strum(GT, b, B, ch, [(0, 0.6, "d", "!")]); DR[0].at(b * B, "C3:0.6!")
        for j, m in enumerate(voice): AC[j].at(round(b * B + 0.02 * j, 3), f"{nm(m)}:0.6!")
        continue
    strum(GT, b, B, ch, REEL)
    for j, m in enumerate(voice):
        AC[j].bar(b, f"R:0.5 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.2")
    fill = (i % 8 == 7)
    DR[b % 2].bar(b, "C3:0.5! E3:0.5, C3:0.5, E3:0.5 C3:0.5! E3:0.5, C3:0.5, E3:0.5" if not fill else "C3:0.5! E3:0.5, C3:0.5! E3:0.5, C3:0.25! C3:0.25! C3:0.5! C3:0.5! C3:0.5!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の098（第3版）。鐘の音で島じゅうの人が目をさます。G ミクソリディア。笛ひとりが先唱の1行（♩=44）を歌い、フィドルとアコーディオンが同じ行を少しずつずれながら重ねる（079 と同じ詩篇唱）。ずれはだんだん小さくなり、4小節でそろいながら ♩=112 に速くなって、気づけば全員（フィドル・アコーディオン・ギター・ボーラン）がリールを弾いている。リールの節は、詩篇の節を速く細かくしたもの。最後がいちばん大きく、全員で切る。",
       harm_scenes=None, tail_scene="切る", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.15, "lp": 3000, "rt": 1.8}}}
json.dump(air, open("/tmp/cel/w/air098.json", "w"), ensure_ascii=False)
