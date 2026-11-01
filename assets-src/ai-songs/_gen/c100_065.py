# ケルト・フルート100曲「銀の笛と百の夜」065 老いた羊飼いの話 The Old Shepherd's Tale — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 村の集まり（ケーリー）の夜。年老いた羊飼いが、若いころに祖父と山で過ごした話をする。みんなで順番に出し物をする習わしで、
#   まずエイラが笛ひとりで話の始まりを語り、次に竪琴弾きの娘が続きを語る（笛は休んで聴く）。3番目は全員で。
#   話が終わると、みんなは静かな和音で羊飼いに応える。
# 調べ: 悲しみ。形: ケーリーの出し物の順番（笛ひとりの語り → 竪琴の番 → 全員 → 笛と竪琴の名残 → 全員の静かな和音）。
# 拍子・速さ: 6/8・付点4分＝50（語り。ゆれを大きく）→ 付点4分＝70。旋法: E ドリア（C♯ がやわらかい）。
# 主役は笛（語る笛）。伴奏の主役: 竪琴（ソロの番がある）。全員の所でチェロとビオラの長い和音。ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 主役が順番に交代する（笛が一度まるごと休んで、竪琴が節を語る）。
# 始まり: 笛ひとりの語り → 終わり: 全員の静かな和音。
# 山: 3番目の出し物（全員）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "065-the-old-shepherds-tale", "老いた羊飼いの話", "The Old Shepherd's Tale", 70, 2, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.25})
K = Key("E", "dorian", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Em", "A", "Em", "Em", "G", "Bm", "D", "Em"]; CB = ["A", "Bm", "D", "A", "Em", "G", "D", "Em"]
SC = [("笛の語り", 24, "intro", CA + CB + CA), ("竪琴の番", 24, "verse", CA + CB + CA), ("全員", 64, "chorus", (CA + CB) * 4),
      ("名残", 16, "verse", CA + CB), ("静かな和音", 4, "outro", ["Em"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("笛の語り", 0, 0.72), ("竪琴の番", 0, 0.72), ("全員", 0, 0.78), ("全員", 48, 0.9), ("名残", 0, 0.72), ("静かな和音", 0, 0.68)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="笛の語り", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 50}, {"bar": s["竪琴の番"] + 1, "bpm": 70}]
B = S.beats
G = c.g()
HM = S.track("竪琴（語る右手）", "harp", patch="folkHarp", volume=0.12, pan=0.2, reverb=0.55, sustain=1.6, barGain=G)
HA = [S.track(f"竪琴（左手の分散和音{j + 1}）", "harp", patch="folkHarp", volume=0.065, pan=-0.1 + 0.15 * j, reverb=0.55, sustain=1.6, barGain=G) for j in range(2)]
VC = S.track("チェロ（全員の和音）", "strings", patch="cello", volume=0.02, gainDb=2, pan=-0.25, reverb=0.7, release=0.7, barGain=G)
VA = S.track("ビオラ（全員の和音）", "strings", patch="viola", volume=0.017, pan=0.1, reverb=0.7, release=0.7, barGain=G)

# ---------- 節（8分＝1、1小節＝6。1=E4） ----------
A = ["5:3 4:2 3:1", "4:2 5:1 6:3", "5:2 4:1 3:2 2:1", "1:6", "3:2 4:1 5:2 6:1", "7:3 6:2 5:1", "4:2 3:1 2:2 7,:1", "1:6"]
Bm = ["1':3 7:2 6:1", "5:2 6:1 7:3", "1':2 2':1 1':2 7:1", "6:6", "5:2 6:1 5:2 4:1", "3:2 4:1 5:3", "4:2 3:1 2:2 1:1", "1:6"]
play_melody(c, "笛の語り", e2b(A + Bm + A), 4, "air", key=K, density=0.3, seed=6501)          # 笛ひとり
play_melody(c, "全員", e2b((A + Bm) * 4), 4, "air", key=K, density=0.35, seed=6502)
play_melody(c, "名残", e2b(A + Bm), 4, "air", key=K, density=0.2, seed=6503)
s0 = s["静かな和音"]
c.FLUTE.at(s0 * B, "B4:7")
# 竪琴の番：竪琴が節を語る（笛は休む）。1オクターブ上で
ev = []
for j, s_ in enumerate(e2b(A + Bm + A)): ev += mel_events(K, s_, 5, (s["竪琴の番"] + j) * B)
play(HM, [(round(t, 4), L, m, "" if L >= 1 else ",") for t, L, m in ev])

# ---------- 竪琴の左手（1拍に8分3つ）と、全員の弦 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
for b in range(s["竪琴の番"], s["静かな和音"]):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r, th, fi = tri(ch)
    lo = near(r, 40)
    seq = (lo, lo + 7, near(th, lo + 12)) if n != "全員" else (lo, near(fi, lo + 1), near(th, lo + 12))
    for q in range(2):
        for k, m in enumerate(seq if q == 0 else (lo + 12, near(fi, lo + 12), seq[2])):
            HA[k % 2].at(round(b * B + q + k * T3, 4), f"{nm(m)}:{round(2 * T3, 4)}{'' if (q == 0 and k == 0) else ','}")
    if n == "全員" and b % 2 == 0:
        VC.at(b * B, f"{nm(near(r, 40))}:{2 * B + 0.15}{',' if b % 4 else ''}"); VA.at(round(b * B + 0.05, 3), f"{nm(near(th, 55))}:{2 * B + 0.1},")
# 静かな和音（E・B・D・F♯・G）
for k, (tr, m) in enumerate(((VC, "E2"), (VA, "B3"), (HA[0], "E3"), (HA[1], "D4"), (HM, "F#4"), (HA[0], "G4"))):
    tr.at(round(s0 * B + 0.15 * k, 3), f"{m}:{round(7.5 - 0.15 * k, 2)}{'' if k == 0 else ','}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の065（第3版）。村の集まり（ケーリー）で、年老いた羊飼いが若いころの祖父の話をする。6/8、E ドリア。出し物の順番どおり、まず笛ひとりの語り（付点4分＝50、ゆれを大きく）、次に竪琴の番（付点4分＝70。笛は休み、竪琴が同じ節を語る）、3番目は全員（笛・竪琴・チェロとビオラ）で、ここが山。笛と竪琴の名残のあと、全員の静かな和音で羊飼いに応える。",
       harm_scenes=None, tail_scene="静かな和音", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.2}}}
json.dump(air, open("/tmp/cel/w/air065.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
