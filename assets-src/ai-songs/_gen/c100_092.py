# ケルト・フルート100曲「銀の笛と百の夜」092 帰り道の花 Flowers on the Way Home — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 山のふもとの村で、雪どけの道ばたに最初の花が咲いている。村の家からフィドルとピアノが聞こえ、エイラも加わる。
#   はじめは足をきちんとそろえる角ばった踊り（ストラスペイ）。気持ちがほどけると、同じ節がなめらかなリールになって流れだす。
# 調べ: 喜び。形: ストラスペイ（AABB）→ 同じ節のリール（AABB×2）。ケープ・ブレトン式（フィドルとピアノだけ。打楽器なし）。
# 拍子・速さ: 4/4・♩=72 → 112。旋法: A イオニア。
# 主役は笛（スナップのある笛 → 流れる笛）。伴奏の主役: フィドル（笛の1オクターブ下で同じ節）とピアノ（左手のオクターブと、裏で弾む右手の和音）。
#   竪琴・ギター・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 尖ったストラスペイ（拍ごとに付点の「長‐短」とスナップの「短‐長」）が、同じ節のまま丸いリール（まっすぐな8分）にほどける。
# 始まり: ピアノの左手 → 終わり: 全員で切る。
# 山: 階段（ストラスペイ → リール1 → リール2）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "092-flowers-on-the-way-home", "帰り道の花", "Flowers on the Way Home", 112, 4, "A", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("A", "major", 4)
CA = ["A", "D", "A", "E", "A", "E", "E", "A"]; CB = ["A", "E", "F#m", "A", "A", "E", "D", "A"]
T = CA * 2 + CB * 2
SC = [("ピアノの左手", 2, "intro", ["A", "A"]), ("ストラスペイ", 32, "verse", T), ("ほどける", 1, "verse", ["E"]), ("リール1", 32, "verse", T), ("リール2", 32, "chorus", T),
      ("切る", 1, "outro", ["A"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ピアノの左手", 0, 0.76), ("ストラスペイ", 0, 0.76), ("ストラスペイ", 31, 0.8), ("ほどける", 0, 0.78), ("リール1", 0, 0.84), ("リール2", 0, 0.9), ("リール2", 31, 0.96),
          ("切る", 0, 0.96)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ピアノの左手", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 72}, {"bar": s["ほどける"] + 1, "bpm": 112, "ramp": 1}]
B = S.beats
G = c.g()
FD = S.track("フィドル", "strings", patch="violin", volume=0.03, pan=0.3, reverb=0.3, barGain=G)
LH = [S.track(f"ピアノ（左手のオクターブ{j + 1}）", "piano", volume=0.2, pan=-0.2, reverb=0.3, sustain=0.6, barGain=[round(x * (1.4 if b < 2 else 1.0), 3) for b, x in enumerate(G)]) for j in range(2)]
RH = [S.track(f"ピアノ（右手の和音{j + 1}）", "piano", volume=0.07, pan=0.05 + 0.05 * j, reverb=0.3, sustain=0.4, barGain=G) for j in range(3)]

# ---------- 節（まっすぐな8分で書き、ストラスペイでは拍ごとに「長‐短」「短‐長」に尖らせる。1=A4） ----------
A = ["1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "4:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5 2:1",
     "1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 7:0.5 6:0.5 5:0.5", "6:0.5 5:0.5 4:0.5 2:0.5 1:1 1:1",
     "1:0.5 3:0.5 5:0.5 1':0.5 2':0.5 1':0.5 7:0.5 6:0.5", "5:0.5 6:0.5 5:0.5 3:0.5 2:1 4:1",
     "3:0.5 5:0.5 4:0.5 2:0.5 7,:0.5 2:0.5 1:0.5 7,:0.5", "1:1 5,:1 1:2"]
Bm = ["5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5", "2':0.5 7:0.5 7:0.5 6:0.5 7:0.5 1':0.5 2':0.5 7:0.5",
      "1':0.5 6:0.5 6:0.5 5:0.5 6:0.5 7:0.5 1':0.5 6:0.5", "5:0.5 3:0.5 2:0.5 3:0.5 5:1 5:1",
      "5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5", "2':0.5 7:0.5 7:0.5 6:0.5 7:0.5 1':0.5 2':0.5 7:0.5",
      "1':0.5 6:0.5 5:0.5 3:0.5 4:0.5 2:0.5 7,:0.5 2:0.5", "1:1 5,:1 1:2"]
def sharpen(bar):
    """8分の組を、1・3拍目は付点（0.75・0.25）、2・4拍目はスナップ（0.25・0.75）に"""
    toks = bar.split(); out = []; t = 0.0; i = 0
    while i < len(toks):
        d, L = toks[i].split(":"); L = float(L)
        if L == 0.5 and i + 1 < len(toks) and float(toks[i + 1].split(":")[1]) == 0.5 and abs(t % 1) < 1e-6:
            d2 = toks[i + 1].split(":")[0]
            a, b_ = (0.75, 0.25) if int(t) % 2 == 0 else (0.25, 0.75)
            out += [f"{d}:{a}", f"{d2}:{b_}"]; t += 1; i += 2
        else:
            out.append(toks[i]); t += L; i += 1
    return " ".join(out)
TUNE = A + A + Bm + Bm
def put(sc, bars, kind, dens, seed):
    s0 = c.s0[sc]; ev = []
    for j, s_ in enumerate(bars): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 112, kind, B, density=dens, seed=seed))
    play(FD, [(t, L, (m - 12 if m - 12 >= 55 else m), ("!" if abs(t % 2) < 1e-6 else ",")) for t, L, m in ev])
put("ストラスペイ", [sharpen(x) for x in TUNE], "march", 0.3, 9201)
put("リール1", TUNE, "reel", 0.45, 9202)
put("リール2", TUNE, "reel", 0.55, 9203)
play_melody(c, "ほどける", ["5:1 4:1 3:1 2:1"], 4, "reel", key=K, density=0.0)
c.FLUTE.at(s["切る"] * B, "A5:0.6!"); FD.at(s["切る"] * B, "A4:0.6!")

# ---------- ピアノ（ケープ・ブレトン式：左手のオクターブと、裏で弾む右手） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 33); f5 = lo + 7
    if n == "切る":
        LH[0].bar(b, f"{nm(lo)}:0.6! R:3.4"); LH[1].bar(b, f"{nm(lo + 12)}:0.6! R:3.4")
        for j, m in enumerate((near(r, 57), near(th, 57), near(fi, 57))): RH[j].bar(b, f"{nm(m)}:0.6! R:3.4")
        continue
    LH[0].bar(b, f"{nm(lo)}:0.5! R:1.5 {nm(f5 if i % 2 else lo)}:0.5 R:1.5"); LH[1].bar(b, f"{nm(lo + 12)}:0.5 R:1.5 {nm((f5 if i % 2 else lo) + 12)}:0.5, R:1.5")
    if n == "ピアノの左手": continue
    for j, m in enumerate((near(r, 57), near(th, 57), near(fi, 57))):
        if n == "ストラスペイ":
            RH[j].bar(b, f"R:1 {nm(m)}:0.25, R:0.5 {nm(m)}:0.25, R:1 {nm(m)}:0.25, R:0.75")
        else:
            RH[j].bar(b, f"R:0.5 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.2 R:0.5 {nm(m)}:0.3, R:0.7 {nm(m)}:0.3, R:0.2")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.18 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の092（第3版）。山のふもとの村、雪どけの道ばたの最初の花。ケープ・ブレトン式（フィドルとピアノだけ、打楽器なし）、A の長調。ピアノの左手で始まり、ストラスペイ（♩=72。拍ごとに付点の「長‐短」とスナップの「短‐長」の尖った踊り）を AABB。1小節でテンポが 112 に上がり、同じ節がまっすぐな8分の丸いリールにほどけて2回流れる。フィドルは笛の1オクターブ下で同じ節。最後は全員で切る。",
       harm_scenes=None, tail_scene="切る", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.15, "lp": 3000, "rt": 1.6}}}
json.dump(air, open("/tmp/cel/w/air092.json", "w"), ensure_ascii=False)
