# ケルト・フルート100曲「銀の笛と百の夜」025 飛び石 Stepping Stones — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 小川の浅瀬に、平たい石が向こう岸まで並んでいる。エイラは笛を吹きながら、ぴょん、ぴょん、と石を渡っていく。
#   途中で1つ、ぐらつく石に乗ってよろけ（8小節だけ短調）、また跳びだす。向こう岸に近づくほど足どりは軽くなり、
#   最後の石から岸へ、全員でぴょんと跳んで止まる。
# 調べ: 喜び。形: ポルカ2曲のセット（1曲目 C → 8小節よろける → 1曲目 → 2曲目 F → 2曲目を D で）。
# 拍子・速さ: 2/4・♩=130。調: C → F → D（一段ずつ上がる）。
# 主役は笛（跳ねる笛・スタッカート）。伴奏の主役: アコーディオン（左手の「ブン・チャ」）と、ボーン（骨の拍子木。木の打音で）。
#   竪琴・ギター・ピアノ・弦・パッド・ボーランは使わない。
# この曲だけ: 途中で8小節だけ短調によろけ（長い音でぐらつく）、また跳びだす。
# 始まり: ひと跳び（笛の1音と骨の1打）→ 終わり: 全員でぴょんと止まる。
# 山: 階段（調が上がるたびに一段ずつ強く。よろける所で一度だけ下がる）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "025-stepping-stones", "飛び石", "Stepping Stones", 130, 2, "C", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
KC, KCm, KF, KD = Key("C", "major", 4), Key("C", "minor", 4), Key("F", "major", 4), Key("D", "major", 4)
A_CH = ["I", "V", "I", "I", "V", "IV", "V", "I"]
B_CH = ["I", "I", "V", "I", "IV", "I", "V", "I"]
M_CH = ["i", "v", "VI", "i", "iv", "i", "v", "V"]
def chords(root, seq, minor=False):
    r = PC[root]; out = []
    for d in seq:
        off = {"I": 0, "i": 0, "IV": 5, "iv": 5, "V": 7, "v": 7, "VI": 8}[d]
        nmx = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"][(r + off) % 12]
        out.append(nmx + ("m" if d in ("i", "iv", "v") else ""))
    return out
AB_C = chords("C", A_CH) * 2 + chords("C", B_CH) * 2
SC = [("ひと跳び", 2, "intro", ["C", "C"]), ("1曲目", 96, "verse", AB_C * 3), ("よろける", 8, "verse", chords("C", M_CH)),
      ("1曲目ふたたび", 32, "verse", AB_C), ("2曲目", 64, "chorus", (chords("F", A_CH) * 2 + chords("F", B_CH) * 2) * 2),
      ("向こう岸", 64, "chorus", (chords("D", A_CH) * 2 + chords("D", B_CH) * 2) * 2), ("ぴょん", 2, "outro", ["D", "D"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("ひと跳び", 0, 0.66), ("1曲目", 0, 0.7), ("1曲目", 95, 0.76), ("よろける", 0, 0.62), ("1曲目ふたたび", 0, 0.78),
          ("2曲目", 0, 0.84), ("2曲目", 63, 0.86), ("向こう岸", 0, 0.9), ("向こう岸", 63, 0.95), ("ぴょん", 0, 0.95)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ひと跳び", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 左手の低音・和音1音・骨の1打は、どれも短く切った笛とほぼ同じ大きさ → 笛が主役になるよう、それぞれ下げた（和音は3音重なるので大きく下げる）
AB = S.track("アコーディオン（左手のブン）", "accordion", volume=0.06, pan=-0.2, reverb=0.3, attack=0.03, release=0.2, barGain=G)
AC = [S.track(f"アコーディオン（左手のチャ{j + 1}）", "accordion", volume=0.025, pan=-0.15 + 0.05 * j, reverb=0.3, attack=0.03, release=0.15, barGain=G) for j in range(3)]
BN = S.track("ボーン（骨の拍子木）", "guitar", patch="surgeWoody", volume=0.045, pan=0.25, reverb=0.25, barGain=G)

def stac(bars):
    """跳ねる笛：0.5拍以下の音は短く切って、あとを休みに"""
    out = []
    for s_ in bars:
        tk = []
        for t in s_.split():
            n, L = t.split(":"); L = float(L)
            if n != "R" and L <= 0.5: tk += [f"{n}:{round(L * 0.55, 4)}", f"R:{round(L * 0.45, 4)}"]
            else: tk.append(t)
        out.append(" ".join(tk))
    return out

# ---------- 1曲目（C）・2曲目（F → D） ----------
A1 = ["5:0.5 3:0.5", "4:0.5 2:0.5", "3:0.25 4:0.25 5:0.25 6:0.25", "5:0.5 1':0.5", "7:0.5 2':0.5", "1':0.5 6:0.5", "5:0.25 4:0.25 3:0.25 2:0.25", "1:0.5 R:0.5"]
B1 = ["1':0.5 5:0.5", "6:0.25 7:0.25 1':0.5", "2':0.5 7:0.5", "1':0.5 5:0.5", "4:0.5 6:0.5", "5:0.25 4:0.25 3:0.25 2:0.25", "3:0.5 7,:0.5", "1:0.5 R:0.5"]
A2 = ["1:0.75 2:0.25", "3:0.5 1:0.5", "5:0.75 4:0.25", "3:0.5 2:0.5", "4:0.75 5:0.25", "6:0.5 4:0.5", "3:0.25 2:0.25 1:0.25 7,:0.25", "1:0.5 R:0.5"]
B2 = ["5:0.25 6:0.25 5:0.25 4:0.25", "3:0.5 5:0.5", "6:0.25 7:0.25 6:0.25 5:0.25", "4:0.5 6:0.5", "5:0.25 6:0.25 7:0.25 1':0.25", "2':0.5 7:0.5", "1':0.25 6:0.25 5:0.25 3:0.25", "1:0.5 R:0.5"]
MN = ["3:1", "2:0.5 1:0.5", "7,:1", "1:0.5 R:0.5", "6,:0.75 7,:0.25", "1:0.5 3:0.5", "2:1", "5,:0.5 R:0.5"]   # よろける（短調。長い音でぐらつく）
T1 = stac(A1 + A1 + B1 + B1); T2 = stac(A2 + A2 + B2 + B2)
play_melody(c, "ひと跳び", ["5:0.25 R:0.75", "R:1"], 4, "march", key=KC, density=0.0)
play_melody(c, "1曲目", T1 * 3, 4, "march", key=KC, density=0.25, seed=2501)
play_melody(c, "よろける", MN, 4, "air", key=KCm, density=0.35, seed=2502)
play_melody(c, "1曲目ふたたび", T1, 4, "march", key=KC, density=0.35, seed=2503)
play_melody(c, "2曲目", T2 * 2, 4, "march", key=KF, density=0.35, seed=2504)
play_melody(c, "向こう岸", T2 * 2, 4, "march", key=KD, density=0.45, seed=2505)
play_melody(c, "ぴょん", ["1':0.25! R:0.75", "R:1"], 4, "march", key=KD, density=0.0)

# ---------- アコーディオンの「ブン・チャ」と骨 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, sorted(60 + (p - 60) % 12 for p in (r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12))
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r, tones = tri(ch)
    lo = 41 + (r - 41) % 12                                       # 左手の低音（F2〜E3）
    if n == "ひと跳び":
        if i == 0: BN.bar(b, "A4:0.25! R:1.75")
        continue
    if n == "ぴょん":
        if i == 0:
            AB.bar(b, f"{nm(lo)}:0.25! R:1.75"); BN.bar(b, "A4:0.25! R:1.75")
            for j, t in enumerate(tones): AC[j].bar(b, f"{nm(t)}:0.25! R:1.75")
        continue
    if n == "よろける":                                         # よろける：長い和音で、ぐらっと
        AB.bar(b, f"{nm(lo)}:2,")
        for j, t in enumerate(tones): AC[j].bar(b, f"{nm(t)}:2,")
        continue
    AB.bar(b, f"{nm(lo)}:0.5 R:0.5 {nm(lo + 7 if lo + 7 <= 55 else lo - 5)}:0.5 R:0.5")
    for j, t in enumerate(tones): AC[j].bar(b, f"R:0.5 {nm(t)}:0.3, R:0.2 R:0.5 {nm(t)}:0.3, R:0.2")
    if n == "1曲目" and i < 16: continue                          # 骨は1曲目の2周目から
    pat = "A4:0.25! A4:0.25, R:0.5 A4:0.25 A4:0.25, R:0.5" if n != "向こう岸" else "A4:0.25! A4:0.25, E4:0.25, A4:0.25 A4:0.25! A4:0.25, E4:0.25, A4:0.25"
    BN.bar(b, pat)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.2 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の025（第3版）。小川の浅瀬の飛び石を、笛を吹きながらぴょんぴょん渡る。ポルカ2曲のセット（2/4・♩=130）。1曲目は C、途中で1つぐらつく石に乗って8小節だけ短調によろけ、また跳びだす。2曲目は F、最後は D に上がって、向こう岸へ全員でぴょんと跳んで止まる。伴奏はアコーディオンの「ブン・チャ」と、骨の拍子木。",
       harm_scenes=None, tail_scene="ぴょん", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.5, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.18, "lp": 3000, "rt": 2.2}}}
json.dump(air, open("/tmp/cel/w/air025.json", "w"), ensure_ascii=False)
