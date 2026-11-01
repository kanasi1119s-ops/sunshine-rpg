# ケルト・フルート100曲「銀の笛と百の夜」097 朝の鐘 The Morning Bell — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 日がのぼり、ついに鐘が鳴る。古い伝説では、竪琴弾きは3つの調べ（泣かせる調べ・笑わせる調べ・眠らせる調べ）を持つという。
#   鐘の音は、祖父が止めた悲しみの調べから始まり、喜びの踊り、眠りの子守歌を通って、最後に島じゅうを目覚めさせる鐘になる。
# 調べ: 喜び（3つの調べを1曲で通る：悲しみ → 喜び → 眠り → 目覚め）。
# 拍子・速さ: 悲しみ 4/4・♩=56 → 喜び 6/8・付点4分＝100 → 眠り 3/4・♩=56 → 目覚め 4/4・♩=96。
#   （作曲ソフトの小節は 4/4 のまま。6/8 は1小節＝3拍、3/4 は1小節＝3拍として、拍の位置で書く）
# 旋法: D エオリア（悲しみ）→ D イオニア（喜び・眠り・目覚め）。
# 主役は笛（吹き方が3つに変わる：長く泣く笛 → 跳ねる笛 → ささやく笛 → 高らかな笛）。
# 伴奏の主役: 鐘（パイプオルガンの低い和音）と全員。悲しみ＝チェロとビオラ、喜び＝ボーランとギター、眠り＝竪琴、目覚め＝全員と鐘。
# この曲だけ: 竪琴の神話の3つの調べを、1曲の中で順に通る。
# 始まり: オルガンの低い和音 → 終わり: 鐘と全員の和音。
# 山: 3つの場面ごと（目覚めがいちばん大きい）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "097-the-morning-bell", "朝の鐘", "The Morning Bell", 96, 4, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
KM, KJ = Key("D", "minor", 4), Key("D", "major", 4)
SC = [("オルガン", 2, "intro", ["Dm", "Dm"]), ("悲しみ", 16, "verse", ["Dm", "Bb", "Gm", "A"] * 4), ("喜び", 30, "chorus", ["D", "G", "A", "D", "D", "G", "A", "D"] * 3 + ["D"] * 6),
      ("眠り", 12, "verse", ["D", "G", "D", "A", "D", "G", "A", "D", "D", "G", "A", "D"]), ("目覚め", 24, "chorus", ["D", "G", "A", "D", "Bm", "G", "A", "D"] * 3),
      ("鐘と全員", 3, "outro", ["D"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("オルガン", 0, 0.72), ("悲しみ", 0, 0.72), ("悲しみ", 12, 0.82), ("喜び", 0, 0.82), ("喜び", 26, 0.9), ("眠り", 0, 0.68), ("目覚め", 0, 0.86), ("目覚め", 23, 0.98),
          ("鐘と全員", 0, 0.96)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="オルガン", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 56}, {"bar": s["喜び"] + 1, "bpm": 150}, {"bar": s["眠り"] + 1, "bpm": 56}, {"bar": s["目覚め"] + 1, "bpm": 96, "ramp": 2}]
B = S.beats
G = c.g()
ORG = [S.track(f"鐘（パイプオルガン{j + 1}）", "pad", patch="churchOrgan", volume=0.05, gainDb=6, pan=-0.15 + 0.15 * j, reverb=0.75, barGain=G) for j in range(3)]      # 試し書き出し: 0.05 の3音で笛より約13dB 小さい → gainDb 6
BELL = S.track("鐘", "bell", volume=0.12, pan=0.1, reverb=0.9, barGain=[1.1] * c.NB)
VC = S.track("チェロ", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.25, reverb=0.65, release=0.7, barGain=G)
VA = S.track("ビオラ", "strings", patch="viola", volume=0.017, pan=0.1, reverb=0.65, release=0.7, barGain=G)
VN = S.track("バイオリン", "strings", patch="violin", volume=0.024, gainDb=3, pan=0.3, reverb=0.7, release=0.7, barGain=G)
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=0.25 - 0.08 * i, reverb=0.3, barGain=G) for i in range(5)]
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.05 + 0.1 * j, reverb=0.25, barGain=G) for j in range(2)]
HP = [S.track(f"竪琴{j + 1}", "harp", patch="folkHarp", volume=0.07, pan=-0.2 + 0.2 * j, reverb=0.55, sustain=1.6, barGain=G) for j in range(2)]

def put(key, bars, start_beat, bar_len, kind, dens, seed):
    ev = []
    for j, s_ in enumerate(bars): ev += mel_events(key, s_, 4, start_beat + j * bar_len)
    play(c.FLUTE, ornament([[round(t, 4), L, m] for t, L, m in ev], key, 96, kind, bar_len, density=dens, seed=seed))
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12

# ---------- オルガンの低い和音（始まり） ----------
for j, m in enumerate(("D2", "A2", "D3")): ORG[j].at(0.05 * j, f"{m}:8{',' if j else ''}")

# ---------- 悲しみ（4/4・D エオリア。長く泣く笛。チェロとビオラとオルガン） ----------
SAD = ["5:2 4:1 3:1", "2:2 1:2", "3:1 4:1 5:2", "4:4", "6:2 5:1 4:1", "3:2 2:2", "1:1 2:1 3:1 2:1", "1:4",
       "1':2 7:1 6:1", "5:2 4:2", "3:1 4:1 5:1 3:1", "2:4", "4:2 3:1 2:1", "1:2 7,:2", "1:1 2:1 7,:1 2:1", "1:4"]
put(KM, SAD, s["悲しみ"] * B, 4, "air", 0.2, 9701)
for b in range(s["悲しみ"], s["喜び"], 2):
    ch = S.chords[b]; r, th, fi = tri(ch)
    VC.at(b * B, f"{nm(near(r, 38))}:8.2"); VA.at(round(b * B + 0.05, 3), f"{nm(near(th, 53))}:8.1,")
    for j, m in enumerate((near(r, 38), near(fi, 45), near(r, 50))): ORG[j].at(round(b * B + 0.04 * j, 3), f"{nm(m)}:8.1,")

# ---------- 喜び（6/8＝1小節3拍・D イオニア。跳ねる笛。ボーランとギター） ----------
JA = ["1:1 3:0.5 5:1 3:0.5", "4:1 6:0.5 5:1 3:0.5", "1:1 3:0.5 5:1 1':0.5", "7:1 5:0.5 6:1.5", "1:1 3:0.5 5:1 3:0.5", "4:1 6:0.5 5:1 3:0.5", "2:1 4:0.5 3:1 7,:0.5", "1:1.5 1:1.5"]
JB = ["1':1 7:0.5 1':1 5:0.5", "6:1 5:0.5 6:1 2':0.5", "1':1 7:0.5 1':1 3':0.5", "2':1.5 1':1.5", "1':1 7:0.5 1':1 5:0.5", "6:1 1':0.5 5:1 3:0.5", "4:1 6:0.5 3:1 7,:0.5", "1:1.5 1:1.5"]
JIG = JA + JA + JB + JB + JA                                               # 40小節 × 3拍 = 120拍 = 30小節（4/4）
j0 = s["喜び"] * B
put(KJ, JIG, j0, 3, "jig", 0.45, 9702)
JCH = ["D", "G", "D", "A", "D", "G", "A", "D"] * 2 + ["D", "G", "D", "A", "D", "G", "A", "D"] * 2 + ["D", "G", "D", "A", "D", "G", "A", "D"]
for q in range(40):
    t = j0 + 3 * q; ch = JCH[q]
    DR[q % 2].at(round(t, 3), "C3:1!"); DR[q % 2].at(round(t + 1, 3), "E3:0.5,"); DR[q % 2].at(round(t + 1.5, 3), "C3:1"); DR[q % 2].at(round(t + 2.5, 3), "E3:0.5,")
    for i, m in enumerate(open_chord(ch)):
        if i < 5: GT[i].at(round(t + 0.02 * i, 3), f"{nm(m)}:1.4{'' if i == 0 else ','}"); GT[i].at(round(t + 1.5 + 0.02 * i, 3), f"{nm(m)}:1.4,")

# ---------- 眠り（3/4＝1小節3拍・D イオニア。ささやく笛。竪琴） ----------
LUL = ["3:2 2:1", "1:3", "2:1 3:1 4:1", "3:3", "5:2 4:1", "3:2 2:1", "2:1 3:1 2:1", "1:3", "3:2 2:1", "1:3", "2:1 3:1 2:1", "1:3", "5:2 4:1", "3:2 2:1", "2:1 3:1 2:1", "1:3"]
l0 = s["眠り"] * B
put(KJ, LUL, l0, 3, "air", 0.1, 9703)
LCH = ["D", "D", "G", "D", "G", "D", "A", "D"] * 2
for q in range(16):
    t = l0 + 3 * q; r, th, fi = tri(LCH[q])
    for k, m in enumerate((near(r, 38), near(fi, 45), near(th, 54))): HP[k % 2].at(round(t + k, 3), f"{nm(m)}:2{'' if k == 0 else ','}")

# ---------- 目覚め（4/4・D イオニア。高らかな笛。全員と鐘） ----------
WAKE = ["1':2 5:2", "6:1 7:1 1':2", "2':2 1':1 7:1", "1':4", "5:1 6:1 7:1 1':1", "2':2 3':2", "2':1 1':1 7:1 6:1", "5:4"]
put(KJ, WAKE * 3, s["目覚め"] * B, 4, "march", 0.4, 9704)
for b in range(s["目覚め"], s["鐘と全員"]):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    strum(GT, b, B, ch, [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 1, "d", ",")])
    DR[b % 2].bar(b, "C3:1! E3:0.5, E3:0.5, C3:1 E3:0.5, C3:0.5,")
    if i % 2 == 0:
        VC.at(b * B, f"{nm(near(r, 38))}:8.2"); VA.at(round(b * B + 0.05, 3), f"{nm(near(th, 55))}:8.1,"); VN.at(round(b * B + 0.1, 3), f"{nm(near(fi, 67))}:8,")
        for j, m in enumerate((near(r, 38), near(fi, 45), near(r, 50))): ORG[j].at(round(b * B + 0.04 * j, 3), f"{nm(m)}:8.1,")
    if i % 4 == 0: BELL.at(b * B, f"{nm(near(r, 62))}:6")
s0 = s["鐘と全員"]
c.FLUTE.at(s0 * B, "D6:10")
for j, m in enumerate(("D2", "A2", "D3")): ORG[j].at(round(s0 * B + 0.04 * j, 3), f"{m}:11")
VC.at(s0 * B, "D2:11"); VA.at(s0 * B, "A3:11,"); VN.at(s0 * B, "F#5:11,"); BELL.at(s0 * B, "D5:8!"); BELL.at(s0 * B + 2, "A4:8,")
strum(GT, s0, B, "D", [(0, 10, "d", "!")]); DR[0].at(s0 * B, "C3:1!")
for k, m in enumerate((38, 45, 50, 54, 57, 62, 66, 69)): HP[k % 2].at(round(s0 * B + 0.15 * k, 3), f"{nm(m)}:10,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の097（第3版）。日がのぼり、ついに鐘が鳴る。伝説の竪琴弾きの3つの調べ（泣かせる・笑わせる・眠らせる）を、1曲の中で順に通る。パイプオルガンの低い和音（鐘）で始まり、悲しみ（4/4・♩=56、D エオリア。長く泣く笛とチェロ・ビオラ）→ 喜び（6/8・付点4分＝100、D の長調。跳ねる笛とボーラン・ギター）→ 眠り（3/4・♩=56。ささやく笛と竪琴）→ 目覚め（4/4・♩=96。高らかな笛と全員、鐘）。最後は鐘と全員の和音。",
       harm_scenes=None, tail_scene="鐘と全員", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 3000, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air097.json", "w"), ensure_ascii=False)
