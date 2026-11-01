# ケルト・フルート100曲「銀の笛と百の夜」053 霧の中の灯 A Lamp in the Mist — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 舟が湖の真ん中に出ると、深い霧に包まれる。前も後ろも見えない。ただ一つ、小さな灯が水の上でゆらめいている。
#   エイラは灯を見失わないよう、そのまわりを小さく回りながら笛を吹く。霧はゆっくり薄れ、最後は灯だけが残る。
# 調べ: あいだ。形: 灯のまわりを回る旋律（中心の音のまわりを、上下の隣の音で回る句）。
# 拍子・速さ: 6/8・付点4分＝37（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。旋法: A ドリア（F♯ が明るく浮く）。
# 主役は笛（小さく回る笛）。伴奏の主役: ピアノの高い2音のゆらぎ（トレモロ。灯の炎）。脇: 低い弦の霧（チェロとビオラ。だんだん薄れる）。
#   竪琴・ギター・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: ピアノのトレモロが灯の炎で、笛はそのまわりを回る（笛の句の中心の音＝トレモロの2音のどちらか）。
# 始まり: 低い弦の霧 → 終わり: 灯（ピアノのトレモロ）だけが残る。
# 山: 中盤に1つ（灯に近づく）。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

BPM = 37
S = Song("C100", "053-a-lamp-in-the-mist", "霧の中の灯", "A Lamp in the Mist", BPM, 2, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("A", "dorian", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Am", "D", "Am", "Am", "D", "C", "G", "Am"]
CB = ["Am", "G", "D", "Am", "Em", "C", "D", "Em"]
SC = [("霧", 4, "intro", ["Am"] * 4), ("灯がともる", 4, "verse", ["Am", "D", "Am", "Am"]), ("回る1", 16, "verse", CA * 2), ("回る2", 16, "verse", CA + CB),
      ("近づく", 16, "chorus", CB * 2), ("回る3", 16, "verse", CA * 2), ("灯だけ", 8, "outro", ["Am", "D", "Am", "Am", "Am", "D", "Am", "Am"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("霧", 0, 0.66), ("灯がともる", 0, 0.68), ("回る1", 0, 0.7), ("回る2", 0, 0.74), ("近づく", 0, 0.8), ("近づく", 12, 0.88), ("回る3", 0, 0.74),
          ("灯だけ", 0, 0.7), ("灯だけ", 7, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="霧", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 長い音のチェロ（0.02・gainDb 2）・ビオラ（0.017）は笛の約5dB 下（004）。霧は場面ごとに薄れる。霧だけの始まりは別のパートで大きく（049 の直し）
MIST = {"霧": 0.0, "灯がともる": 1.6, "回る1": 1.4, "回る2": 1.2, "近づく": 1.3, "回る3": 0.8, "灯だけ": 0.0}
VC = S.track("チェロ（霧）", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.2, reverb=0.7, release=0.7, barGain=[round(x * MIST[S.scene_of(b)[0]], 3) for b, x in enumerate(G)])
VA = S.track("ビオラ（霧）", "strings", patch="viola", volume=0.017, pan=0.15, reverb=0.7, release=0.7, barGain=[round(x * MIST[S.scene_of(b)[0]], 3) for b, x in enumerate(G)])
VCI = S.track("チェロ（始まりの霧）", "strings", patch="cello", volume=0.05, gainDb=6, pan=-0.2, reverb=0.7, release=0.9)
VAI = S.track("ビオラ（始まりの霧）", "strings", patch="viola", volume=0.04, gainDb=4, pan=0.15, reverb=0.7, release=0.9)
# ピアノ1音は ×1.4 で笛とほぼ同じ（016）。トレモロは音が多いので小さく
PT = [S.track(f"ピアノ（灯の炎{j + 1}）", "piano", volume=0.11, pan=0.18 + 0.08 * j, reverb=0.55, sustain=1.0,
              barGain=[round(x * (1.3 if S.scene_of(b)[0] == "灯だけ" else 1.0), 3) for b, x in enumerate(G)]) for j in range(2)]

def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12

# ---------- 霧（低い弦。2小節ごとに、チェロとビオラが少しずらして弓を返す） ----------
ROOT = {"Am": 45, "D": 50, "G": 43, "C": 48, "Em": 52}
for b in range(0, c.s0["灯だけ"], 2):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r = ROOT[ch]; _, th, fi = tri(ch)
    vc, va = (VCI, VAI) if n == "霧" else (VC, VA)
    lo_c, lo_a = (48, 57) if n == "近づく" else (43, 52)       # 近づく所だけ、霧が少し上へ持ち上がる
    vc.at(b * B, f"{nm(near(r % 12, lo_c))}:{2 * B + 0.3},")
    va.at(round(b * B + 0.15, 3), f"{nm(near(fi if n != '近づく' else th, lo_a))}:{2 * B + 0.15},")

# ---------- ピアノの灯（高い2音のトレモロ。16分＝1/6拍。ゆらぎは強さの揺れで） ----------
rng = random.Random(5301)
s_on = c.s0["灯がともる"]
for b in range(s_on, c.NB):
    ch = S.chords[b]; r, th, fi = tri(ch)
    hi, lo = near(fi, 81), near(th if ch != "D" else r, 76)
    if hi - lo < 3: lo -= 12 if lo > 76 else 0
    t0 = b * B
    for q in range(12):
        tr = PT[q % 2]; m = hi if q % 2 else lo
        mk = rng.choice(["", ",", ",", ","]) if q % 6 else ("!" if b % 2 == 0 and q == 0 else "")
        if b == s_on and q < 6: mk = ","                       # ともる瞬間はそっと
        tr.at(round(t0 + q / 6, 4), f"{nm(m)}:{round(1 / 6, 4)}{mk}")

# ---------- 笛（灯のまわりを回る句。1=A4） ----------
A = ["5:3 6:2 5:1", "4:2 5:1 6:2 5:1", "5:3 3:2 4:1", "5:6", "6:2 5:1 4:2 3:1", "4:2 5:1 3:3", "2:2 3:1 4:2 2:1", "1:6"]
Bm = ["1':3 2':2 1':1", "7:2 1':1 2':2 1':1", "1':3 6:2 7:1", "1':6", "2':2 1':1 7:2 6:1", "5:2 6:1 7:3", "6:2 5:1 4:2 6:1", "5:6"]
play_melody(c, "灯がともる", e2b(["R:6", "R:6", "5:3 6:2 5:1", "5:6"]), 4, "air", key=K, density=0.0)
play_melody(c, "回る1", e2b(A + A), 4, "air", key=K, density=0.15, seed=5301)
play_melody(c, "回る2", e2b(A + Bm), 4, "air", key=K, density=0.2, seed=5302)
play_melody(c, "近づく", e2b(Bm + Bm), 4, "air", key=K, density=0.3, seed=5303)
play_melody(c, "回る3", e2b(A + A), 4, "air", key=K, density=0.15, seed=5304)
play_melody(c, "灯だけ", e2b(["5:3 6:2 5:1", "5:6", "R:6", "R:6", "R:6", "R:6", "R:6", "R:6"]), 4, "air", key=K, density=0.0)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の053（第3版）。湖の真ん中で深い霧に包まれ、水の上に小さな灯だけがゆらめく。6/8・付点4分＝37、A ドリア。ピアノの高い2音のトレモロが灯の炎で、笛はその音を中心に、上下の隣の音で小さく回る。低い弦の霧（チェロとビオラ）はだんだん薄れ、中盤に灯へ近づく山が1つ。最後は笛も霧も消え、灯だけが残る。",
       harm_scenes=None, tail_scene="灯だけ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -44, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2600, "rt": 4.2}}}
json.dump(air, open("/tmp/cel/w/air053.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
