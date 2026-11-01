# ケルト・フルート100曲「銀の笛と百の夜」077 涙の雨 Rain of Tears — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 灯台の部屋で、エイラは祖父の最後の手紙を見つけ、声をあげて泣く。灯台守の老婆がフィドルを手に取り、エイラの笛に答えるように弾く。
#   ふたりは交互に泣くように、ひとふしずつ受け渡す。受け渡しは少しずつ短くなり、一度だけ大きな叫びがあって、
#   最後に初めて、ふたりの節が3度で重なる。
# 調べ: 悲しみ。形: 交互の嘆き（笛4小節 ↔ フィドル4小節 → 2小節ずつ → 叫び → 1小節ずつ → 3度で重なる）。
# 拍子・速さ: 6/8・付点4分＝56（はじめの笛ひとりは 48 でゆれを大きく）。旋法: D エオリア。
# 主役は笛（泣く笛）。伴奏の主役: フィドル（老婆の嘆き。笛と交互に別の節を弾く）。脇: 竪琴の弱奏（2小節ずつの所から）。
#   ギター・ピアノ・パッド・打楽器・ほかの弦・2本目の笛は使わない。
# この曲だけ: 交互に泣き、最後に初めて重なる（それまで笛とフィドルは一度も同時に旋律を弾かない。叫びだけ、少しだけ重なりかける）。
# 始まり: 笛ひとり → 終わり: ふたりが3度で重なる。
# 山: 叫びで1つ。
import sys, json, re
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia

S = Song("C100", "077-rain-of-tears", "涙の雨", "Rain of Tears", 56, 2, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.25})
K = Key("D", "minor", 4)
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CH4 = ["Dm", "C", "Am", "Dm"]; CH4B = ["Bb", "Gm", "C", "Am"]
SC = [("笛ひとり", 8, "intro", CH4 + CH4B), ("4小節ずつ", 32, "verse", (CH4 + CH4B) * 4), ("2小節ずつ", 32, "verse", (CH4 + CH4B) * 4),
      ("叫び", 8, "chorus", ["Dm", "Bb", "Gm", "A", "Dm", "Bb", "C", "A"]), ("1小節ずつ", 16, "verse", (CH4 + CH4B) * 2), ("重なる", 16, "verse", (CH4 + CH4B) * 2),
      ("終わり", 2, "outro", ["Dm", "Dm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("笛ひとり", 0, 0.72), ("4小節ずつ", 0, 0.72), ("2小節ずつ", 0, 0.76), ("叫び", 0, 0.9), ("叫び", 7, 0.84), ("1小節ずつ", 0, 0.76), ("重なる", 0, 0.78),
          ("終わり", 0, 0.7)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="笛ひとり", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 48}, {"bar": s["4小節ずつ"] + 1, "bpm": 56, "ramp": 2}]
B = S.beats
G = c.g()
# 1回目（7.49）: フィドルだけの答えが本編より約22dB 小さく、穴があいた → gainDb 3 → 13、強さ ×1.4
FD = S.track("フィドル（老婆の嘆き）", "strings", patch="violin", volume=0.035, gainDb=13, pan=0.3, reverb=0.55, release=0.5, barGain=[round(x * (0.8 if S.scene_of(b)[0] in ("重なる", "叫び", "終わり") else 1.4), 3) for b, x in enumerate(G)])
HP = [S.track(f"竪琴（弱奏{j + 1}）", "harp", patch="folkHarp", volume=0.05, pan=-0.25 + 0.15 * j, reverb=0.65, sustain=1.6, barGain=G) for j in range(2)]

# ---------- 2つの嘆き（8分＝1、1小節＝6。1=D4） ----------
F = ["5:3 4:2 3:1", "4:3 2:3", "3:2 2:1 1:2 7,:1", "1:6", "1':3 7:2 6:1", "5:3 4:3", "3:2 4:1 5:2 3:1", "2:6"]        # 笛の嘆き
V = ["3:3 2:2 1:1", "7,:3 5,:3", "6,:2 7,:1 1:2 2:1", "1:6", "5:3 6:2 5:1", "4:3 3:3", "2:2 3:1 4:2 2:1", "1:6"]       # フィドルの嘆き（低く）
def put(track, bars, b0, dens=0.2, seed=0, flute=True, shift=0):
    ev = []
    for j, s_ in enumerate(e2b(bars)): ev += mel_events(K, s_, 4, (b0 + j) * B)
    ev = [[round(t, 4), L, (_dia(K, m, shift) if shift else m)] for t, L, m in ev]
    if flute: play(track, ornament(ev, K, 56, "air", B, density=dens, seed=seed))
    else: play(track, [(t, L, m, "" if L >= 1 else ",") for t, L, m in ev])
    return ev
put(c.FLUTE, F, s["笛ひとり"], 0.25, 7701)
for q in range(4):                                                  # 4小節ずつ
    b0 = s["4小節ずつ"] + 8 * q
    put(c.FLUTE, F[4 * (q % 2):4 * (q % 2) + 4], b0, 0.2, 7710 + q)
    put(FD, V[4 * (q % 2):4 * (q % 2) + 4], b0 + 4, flute=False)
for q in range(8):                                                  # 2小節ずつ
    b0 = s["2小節ずつ"] + 4 * q; h = (q % 4) * 2
    put(c.FLUTE, F[h:h + 2], b0, 0.25, 7720 + q)
    put(FD, V[h:h + 2], b0 + 2, flute=False)
CRY = ["5':6", "4':3 3':3", "2':3 1':3", "7:6", "1':3 7:3", "6:2 5:1 4:3", "3:3 2:3", "1:6"]
put(c.FLUTE, CRY, s["叫び"], 0.3, 7730)
put(FD, ["R:6", "5:6", "4:3 3:3", "2:3 1:3", "R:6", "6:3 5:3", "4:3 3:3", "2:6"], s["叫び"], flute=False)       # 叫び：少しだけ重なりかける
for q in range(16):                                                 # 1小節ずつ
    b0 = s["1小節ずつ"] + q; h = q % 8
    if q % 2 == 0: put(c.FLUTE, [F[h]], b0, 0.2, 7740 + q)
    else: put(FD, [V[h]], b0, flute=False)
put(c.FLUTE, F + F, s["重なる"], 0.15, 7750)                         # 初めて重なる：フィドルは笛と同じ節を3度下で
put(FD, F + F, s["重なる"], flute=False, shift=-2)
c.FLUTE.at(s["終わり"] * B, "F4:4"); FD.at(s["終わり"] * B, "D4:4,")

# ---------- 竪琴の弱奏（2小節ずつの所から） ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(s["2小節ずつ"], c.NB):
    ch = S.chords[b]; r, th, fi = tri(ch)
    for q, m in enumerate((near(r, 38), near(fi, 45), near(th, 52), near(r, 57), near(th, 52), near(fi, 45))):
        HP[q % 2].at(round(b * B + q / 3, 4), f"{nm(m)}:{round(2 / 3, 4)}{'' if q == 0 else ','}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.32 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の077（第3版）。灯台の部屋で祖父の最後の手紙を見つけ、エイラが泣く。6/8、D エオリア。笛ひとり（付点4分＝48、ゆれを大きく）で始まり、灯台守の老婆のフィドルが別の節で答える。ふたりは交互に泣くように、4小節ずつ → 2小節ずつ → 1小節ずつと受け渡しを短くし、そのあいだに一度だけ大きな叫び（山）。最後に初めて、フィドルが笛と同じ節を3度下で重ねる。下に竪琴の弱奏。",
       harm_scenes=None, tail_scene="終わり", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2600, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air077.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
