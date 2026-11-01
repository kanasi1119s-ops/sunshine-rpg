# ケルト・フルート100曲「銀の笛と百の夜」030 水車の夜明け Dawn at the Mill — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第3章の終わり。夜明け前、回りだした水車の中で、大きな歯車と小さな歯車がかみ合わずに空回りしている。
#   低い歯車（ピアノの3拍の音型）は4拍子の小屋の時計とずれたまま回り、エイラの笛は時計の4拍子でリールを吹く。
#   3小節ごとに一瞬だけ歯がそろう。夜が明けるころ、ついに全部の歯車がかみ合い、全員が同じ音型でそろって回る。
# 調べ: 喜び。形: リール（4/4）の上で、3拍の音型を回す（3拍の音型は3小節で1周して、4拍子の頭に戻る）。
# 拍子・速さ: 4/4・♩=108。旋法: G イオニア。
# 主役は笛（明るい笛。4拍子のリール）。伴奏の主役: ピアノ（左手の低い3拍の音型＝歯車。歯車2から右手の裏拍）と、ボーラン（小さい太鼓の高い音＝トップエンド）。
#   竪琴・ギター・弦・パッドは使わない。
# この曲だけ: 3拍の音型が4拍子の上でずれて回り、3小節で一周して戻る。最後は全員がその音型にそろう（歯車がかみ合う）。
# 始まり: 暗い低い音（ピアノの低い3拍の音型だけ）→ 終わり: 歯車がかみ合って全員で回り、最後の頭でそろって止まる。
# 山: 終盤に1つ（かみ合う）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "030-dawn-at-the-mill", "水車の夜明け", "Dawn at the Mill", 108, 4, "G", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("G", "major", 4)
CA = ["G", "C", "G", "D", "G", "C", "D", "G"]
CB = ["C", "G", "C", "D", "C", "G", "D", "G"]
SC = [("暗い歯車", 9, "intro", ["G"] * 9), ("歯車1", 24, "verse", (CA + CA + CB)), ("歯車2", 30, "verse", (CA + CB + CB + CA)[:30]),
      ("静か", 12, "verse", (CA + CB)[:12]), ("かみ合う", 36, "chorus", (CA + CA + CB + CB + CA)[:36]), ("止まる", 2, "outro", ["G", "G"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("暗い歯車", 0, 0.66), ("歯車1", 0, 0.72), ("歯車2", 0, 0.78), ("静か", 0, 0.68), ("かみ合う", 0, 0.84), ("かみ合う", 30, 0.94),
          ("止まる", 0, 0.94)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="暗い歯車", passing=True, tension=False)
B = S.beats
G = c.g()
# ピアノの音源は小さい（×1.4 で笛とほぼ同じ。016 で測った）。前奏（ピアノだけ）は別のパートで大きく（016・015 の教え）
LH = S.track("ピアノ（低い歯車＝3拍の音型）", "piano", volume=0.3, pan=-0.15, reverb=0.35, sustain=1.0, barGain=G)
LHI = S.track("ピアノ（前奏の歯車）", "piano", volume=0.3, gainDb=1,   # 1回目（7.80）は gainDb 10 で前奏が本編より約10dB 大きかった
            pan=-0.15, reverb=0.4, sustain=1.0, barGain=[round(x * 1.45, 3) for x in G])   # 2回目（7.82）は ×2 で本編より約6dB 大きく、3回目（7.84）は ×1 で約12dB 小さかった（強さが音量に比例しない）→ ×1.45
RH = [S.track(f"ピアノ（右手の裏拍{j + 1}）", "piano", volume=0.08, pan=0.08 + 0.06 * j, reverb=0.35, sustain=0.8, barGain=G) for j in range(3)]
LH8 = S.track("ピアノ（かみ合う・右手の音型）", "piano", volume=0.18, pan=0.15, reverb=0.35, sustain=0.9, barGain=G)
DR = [S.track(f"ボーラン（トップエンド{j + 1}）", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=0.1 + 0.08 * j, reverb=0.3, barGain=G) for j in range(2)]

# ---------- 3拍の音型（歯車）：8分6つ。4拍子の上で、3小節で1周 ----------
GEAR = [43, 50, 55, 59, 57, 50]                          # G2 D3 G3 B3 A3 D3
def gear(track, b0, b1, shift=0, mark_first=True, vel=""):
    """b0〜b1 小節に、3拍の音型を切れ目なく回す。音型の頭（3拍ごと）を強く"""
    t = b0 * B; q = 0
    while t < b1 * B - 1e-6:
        m = GEAR[q % 6] + shift
        mk = "!" if (q % 6 == 0 and mark_first) else ("," if q % 2 else vel)
        track.at(round(t, 3), f"{nm(m)}:0.5{mk}")
        t += 0.5; q += 1
gear(LHI, c.s0["暗い歯車"], c.s0["歯車1"])
gear(LH, c.s0["歯車1"], c.s0["かみ合う"])
gear(LH, c.s0["かみ合う"], c.s0["止まる"])
gear(LH8, c.s0["かみ合う"] + 24, c.s0["止まる"], shift=24)            # かみ合う後半：右手も2オクターブ上で同じ音型

# ---------- 笛（4拍子のリール。G イオニア。1=G4） ----------
A = ["5:0.5 5:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:0.5", "1:0.5 2:0.5 3:0.5 1:0.5 6,:1 5,:1",
     "5:0.5 5:0.5 3:0.5 5:0.5 1':0.5 7:0.5 6:0.5 5:0.5", "4:0.5 6:0.5 5:0.5 3:0.5 2:1 R:1",
     "5:0.5 5:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:0.5", "1:0.5 3:0.5 5:0.5 1':0.5 7:1 6:1",
     "5:0.5 4:0.5 3:0.5 2:0.5 3:0.5 1:0.5 7,:0.5 2:0.5", "1:2 R:2"]
Bm = ["1':1 7:0.5 6:0.5 5:1 3:1", "4:0.5 5:0.5 6:0.5 4:0.5 5:2", "1':1 7:0.5 1':0.5 2':1 1':1", "7:0.5 6:0.5 5:0.5 4:0.5 3:2",
      "3:0.5 4:0.5 5:0.5 3:0.5 6:0.5 5:0.5 4:0.5 6:0.5", "5:0.5 6:0.5 7:0.5 5:0.5 1':2", "2':0.5 1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5", "1:2 R:2"]
play_melody(c, "歯車1", A + A + Bm, 4, "reel", key=K, density=0.35, seed=3001)
play_melody(c, "歯車2", (A + Bm + Bm + A)[:30], 4, "reel", key=K, density=0.45, seed=3002)
play_melody(c, "静か", ["5:4", "3:2 2:2", "1:4", "6,:2 7,:2", "1:4", "3:4", "2:2 3:2", "5:4", "6:2 5:2", "4:2 3:2", "2:4", "1:2 R:2"], 4, "air", key=K, density=0.2, seed=3003)
play_melody(c, "かみ合う", (A + A + Bm)[:24], 4, "reel", key=K, density=0.5, seed=3004)
# かみ合う後半の12小節：笛も歯車の音型（1オクターブ上＋2オクターブ上の間）を4周 → 全員がそろう
s1 = c.s0["かみ合う"] + 24
t = s1 * B; q = 0
while t < c.s0["止まる"] * B - 1e-6:
    m = GEAR[q % 6] + 24
    c.FLUTE.at(round(t, 3), f"{nm(m if m <= 83 else m - 12)}:0.5{'!' if q % 6 == 0 else ''}")
    t += 0.5; q += 1
s0 = c.s0["止まる"]
c.FLUTE.at(s0 * B, "G5:2!"); LH.at(s0 * B, "G2:2!"); LH8.at(s0 * B, "G4:2!"); DR[0].at(s0 * B, "C3:1!")

# ---------- 右手の裏拍（歯車2から）とボーラン（歯車の頭を高い音で） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return sorted(60 + (p - 60) % 12 for p in (r, (r + 4) % 12, (r + 7) % 12))
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    if n in ("歯車2", "かみ合う"):
        for j, x in enumerate(tri(ch)): RH[j].bar(b, " ".join([f"R:0.5 {nm(x)}:0.5,"] * 4))
    if n == "歯車2" or (n == "かみ合う" and i < 24):
        # 3拍の音型の頭（3拍ごと）を小さい太鼓の高い音で。小節の頭とずれて回る
        for beat in range(4):
            g = b * B + beat
            if abs((g - c.s0["歯車1"] * B) % 3) < 1e-6: DR[b % 2].at(round(g, 3), "E3:0.5!")
            else: DR[b % 2].at(round(g, 3), "C3:0.5,")
    elif n == "かみ合う":
        DR[b % 2].bar(b, "C3:0.5! E3:0.5, C3:0.5, E3:0.5 C3:0.5! E3:0.5, C3:0.5, E3:0.5")
    elif n == "静か" and i % 3 == 0:
        DR[b % 2].bar(b, "E3:1, R:3")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の030（第3版）。第3章の終わり、夜明けの水車。リール（4/4・♩=108）、G イオニア。ピアノの低い歯車（3拍の音型）は4拍子の時計とずれたまま回り、3小節ごとに一瞬だけそろう。笛は4拍子でリールを吹き、ボーランが歯車の頭を高い音でたたく。夜明けに全部の歯車がかみ合い、笛もピアノもその音型でそろって回り、最後の頭でそろって止まる。",
       harm_scenes=None, tail_scene="止まる", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.4}}}
json.dump(air, open("/tmp/cel/w/air030.json", "w"), ensure_ascii=False)
