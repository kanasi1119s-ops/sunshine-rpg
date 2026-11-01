# ケルト・フルート100曲「銀の笛と百の夜」055 湖底の鐘 The Bell Beneath the Lake — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 雨がやむと、湖の底から鐘の音が聞こえる。昔、湖に沈んだ村の鐘だという。エイラが舟から身を乗りだすと、
#   笛の音は水の中へ沈んでいき、反対に、水の底にあった低い響きは水面へと上がってくる。上と下が入れかわる。
# 調べ: 悲しみ。形: 水面の上と下が入れかわる二層（笛は高い所から沈み、弦は低い所から水面へ上がる。中ほどで交差する）。
# 拍子・速さ: 6/8・付点4分＝35（書き方は1拍＝付点8分の ♪.＝70、1小節＝4拍。8分は 2/3 拍）。旋法: C エオリア（G の和音だけ B♮）。
# 主役は笛（高い → 沈む）。伴奏の主役: 弦（コントラバス・チェロ → ビオラ → バイオリン。低い所から高い水面へ）と、湖底の鐘。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 「沈む」場面で、笛は1小節に1音の長い音で、G5 から C4 まで音階を1段ずつ沈んでいく（その間、弦は1段ずつ上がる）。
#   051（湖への道）は同じ節が回ごとに下がるが、こちらは笛と弦が逆向きに動いて入れかわる。
# 始まり: 低い弦と湖底の鐘 → 終わり: 高い弦だけ（水面の光）。
# 山: 中盤に深い1つ（交差したところ）。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 70                     # 作曲ソフトの速さは 40 以上なので、1拍＝付点8分（♪.＝70）、1小節＝4拍で書く（付点4分＝35 と同じ）
S = Song("C100", "055-the-bell-beneath-the-lake", "湖底の鐘", "The Bell Beneath the Lake", BPM, 4, "C", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("C", "minor", 4)
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 1.5, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Cm", "Bb", "Ab", "Cm", "Fm", "Cm", "Bb", "Cm"]
CB = ["Ab", "Eb", "Fm", "Bb", "Cm", "Fm", "G", "Cm"]
CS = ["Cm", "Bb", "Ab", "G", "Cm", "Bb", "Ab", "G", "Fm", "Cm", "G", "Cm", "Cm", "Ab", "G", "Cm"]
SC = [("湖底", 4, "intro", ["Cm"] * 4), ("水面の上", 16, "verse", CA * 2), ("沈む", 16, "verse", CS), ("深い所", 16, "chorus", CA + CB),
      ("水面の下", 16, "verse", CB + CA), ("高い弦だけ", 6, "outro", ["Cm", "Ab", "Cm", "Cm", "Cm", "Cm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("湖底", 0, 0.66), ("水面の上", 0, 0.68), ("沈む", 0, 0.72), ("深い所", 0, 0.82), ("深い所", 10, 0.88), ("水面の下", 0, 0.74), ("高い弦だけ", 0, 0.7),
          ("高い弦だけ", 5, 0.64)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="湖底", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 長い音の大きさ（004・046・047 で測った値）: チェロ 0.02・gainDb 2、ビオラ 0.017 は笛の約5dB 下、バイオリン 0.03・gainDb 4 は約4dB 下。
#   低い弦だけの始まりは、始まり用のコントラバス（0.07・gainDb 8）とチェロ（0.03・gainDb 8）で（047）
mk = lambda name, patch, v, gd, pan: S.track(name, "strings", patch=patch, volume=v, gainDb=gd, pan=pan, reverb=0.75, release=0.8, barGain=[round(x * 1.3, 3) for x in G])
CB_ = mk("コントラバス", "contrabass", 0.03, 2, -0.1)
VC = [mk(f"チェロ{j + 1}", "cello", 0.02, 2, -0.25 + 0.1 * j) for j in range(2)]
VA = mk("ビオラ", "viola", 0.017, 1, 0.1)
VN = [mk(f"バイオリン{j + 1}", "violin", 0.03, 4, 0.25 + 0.1 * j) for j in range(2)]
CBI = S.track("コントラバス（始まり）", "strings", patch="contrabass", volume=0.07, gainDb=8, pan=-0.1, reverb=0.75, release=1.2)
VCI = S.track("チェロ（始まり）", "strings", patch="cello", volume=0.03, gainDb=8, pan=-0.2, reverb=0.75, release=1.2)
BELL = S.track("湖底の鐘", "bell", volume=0.1, pan=-0.05, reverb=0.95, barGain=[1.0] * c.NB)

def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12

# ---------- 笛 ----------
A = ["5:3 4:2 3:1", "4:3 2:3", "3:2 4:1 5:2 6:1", "5:6", "6:3 5:2 4:1", "3:2 2:1 1:3", "2:2 3:1 4:2 2:1", "1:6"]
Bm = ["1':3 7:2 6:1", "5:6", "6:2 5:1 4:2 3:1", "4:6", "3:3 4:2 5:1", "6:2 5:1 4:3", "3:2 2:1 2:3", "1:6"]
play_melody(c, "水面の上", e2b(A + A), 5, "air", key=K, density=0.2, seed=5501)            # 1=C5：水面の上の高い笛
SINK = ["5':6", "4':6", "3':6", "2':6", "1':6", "7:6", "6:6", "5:6", "4:6", "3:6", "2:6", "1:6", "1:3 2:3", "3:6", "2:3 1:3", "1:6"]
play_melody(c, "沈む", e2b(SINK), 4, "air", key=K, density=0.08, seed=5502)               # G5 から C4 へ、1小節に1段ずつ
play_melody(c, "深い所", e2b(A + Bm), 4, "air", key=K, density=0.2, seed=5503)             # 1=C4：沈んだ笛
play_melody(c, "水面の下", e2b(Bm + A), 4, "air", key=K, density=0.12, seed=5504)

# ---------- 弦（低い所から水面へ。場面ごとに受け持ちの音域が上がる） ----------
# 各場面で使う声: (トラック, 何の音か, 下限)
LAYER = {
    "水面の上": [(CB_, "r", 31), (VC[0], "f", 43), (VC[1], "t", 48)],
    "深い所":   [(VC[0], "r", 48), (VA, "f", 60), (VN[0], "t", 67), (VN[1], "r", 72)],
    "水面の下": [(VA, "f", 67), (VN[0], "t", 74), (VN[1], "r", 79)],
}
def pc_of(kind, ch):
    r, th, fi = tri(ch); return {"r": r, "t": th, "f": fi}[kind]
for sc, voices in LAYER.items():
    s0 = c.s0[sc]
    for q in range(0, 16, 2):
        ch = S.chords[s0 + q]
        for j, (tr, kd, lo) in enumerate(voices):
            tr.at(round((s0 + q) * B + 0.05 * j, 3), f"{nm(near(pc_of(kd, ch), lo))}:{round(2 * B - 0.05 * j + 0.2, 3)}{',' if q % 4 else ''}")
# 沈む：笛が1段下りるたびに、弦が1段上がる（チェロ C3 → C4、ビオラ G3 → G4 あたりへ）
s0 = c.s0["沈む"]
UP = [48, 50, 51, 53, 55, 56, 58, 60, 60, 62, 63, 65, 67, 67, 67, 67]
for q in range(16):
    ch = S.chords[s0 + q]; r, th, fi = tri(ch)
    base = UP[q]
    v1 = near(r, base - 5); v2 = near(fi, v1 + 1); v3 = near(th, base)
    VC[q % 2].at(round((s0 + q) * B, 3), f"{nm(v1)}:{2 * B + 0.15}{',' if q % 2 else ''}")
    VA.at(round((s0 + q) * B + 0.05, 3), f"{nm(v2)}:{2 * B + 0.1},")
    if q >= 8: VN[q % 2].at(round((s0 + q) * B + 0.1, 3), f"{nm(v3)}:{2 * B + 0.05},")
    if q < 6: CB_.at(round((s0 + q) * B, 3), f"{nm(near(r, 31))}:{2 * B + 0.1},")      # コントラバスは最初だけ。だんだん底から離れる

# ---------- 湖底（始まり）と、高い弦だけ（終わり） ----------
CBI.at(0, "C2:17.2"); VCI.at(0.05, "G2:8.3,"); VCI.at(8.05, "C3:9,")
s0 = c.s0["高い弦だけ"]
VN[0].at(s0 * B, "C6:24.4"); VN[1].at(round(s0 * B + 0.1, 3), "G6:24.2,"); VA.at(round(s0 * B + 0.2, 3), "Eb5:16,")

# ---------- 湖底の鐘（沈むほど近く。深い所でいちばん大きく、水面の下では遠く） ----------
for b, v in ((0, ""), (2, ","), (c.s0["水面の上"] + 6, ","), (c.s0["水面の上"] + 14, ","), (c.s0["沈む"] + 4, ""), (c.s0["沈む"] + 8, ""), (c.s0["沈む"] + 12, ""),
             (c.s0["深い所"], "!"), (c.s0["深い所"] + 8, "!"), (c.s0["水面の下"], ","), (c.s0["水面の下"] + 8, ","), (c.s0["高い弦だけ"], ",")):
    BELL.at(b * B, f"C4:12{v}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.4 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の055（第3版）。雨がやむと、湖の底から沈んだ村の鐘が聞こえる。6/8・付点4分＝35、C エオリア。はじめ笛は水面の上の高い所で歌い、弦は湖底の低い所（コントラバスとチェロ）にいる。「沈む」場面で笛は1小節に1音ずつ G5 から C4 まで沈み、その間に弦は1段ずつ水面へ上がる。中ほどで上と下が入れかわり（深い山）、最後は高い弦だけが水面の光のように残る。",
       harm_scenes=None, tail_scene="高い弦だけ", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 150, "lp": 3200, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2600, "rt": 4.6}}}
json.dump(air, open("/tmp/cel/w/air055.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
