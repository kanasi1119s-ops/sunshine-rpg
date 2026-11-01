# ケルト・フルート100曲「銀の笛と百の夜」040 暁の森 Dawn in the Old Wood — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第4章の終わり。森の主に認められたエイラは、夜明けの森を出ていく。暗い森で低く吹いていた夜の節が、
#   日が差すと同じ音のまま、拍の中で細かく踊りだし、朝のジグになる。森の木々（弦）が目覚め、村のギターが迎え、
#   最後は急な崖の上に出て、ひらけた景色の前で全員が「ジャン」と鳴らす。
# 調べ: 喜び。形: 夜の旋律 → 朝の踊り（エアからジグへ）。
# 拍子・速さ: 6/8。夜は付点4分＝40（拍を感じさせない）→ 目覚めで 60 → 朝は 110。1拍＝付点4分、1小節＝2拍で書く。旋法: F イオニア。
# 主役は笛（夜は低く、朝は明るく）。伴奏の主役: 弦（ビオラとチェロ。森の目覚め）→ ナイロン弦ギター。竪琴・ピアノ・パッド・打楽器は使わない。
# この曲だけ: 拍の中の音の数だけを変えて（1拍に1音 → 1拍に3音）、夜の節がそのまま朝の踊りになる。
# 始まり: 笛ひとりの夜の節 → 終わり: 全員でジャン。
# 山: 平原（朝の踊りがしばらく同じ強さで続く）→ 急な崖（最後の16小節で一気に）。
import sys, json, re
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia
import c100_v2 as _v2
_oc = _v2.open_chord
_v2.open_chord = lambda ch, lo=52, hi=76: _oc(ch, lo, hi)

S = Song("C100", "040-dawn-in-the-old-wood", "暁の森", "Dawn in the Old Wood", 110, 2, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("F", "major", 4)
T3 = 1 / 3
CH16 = ["F", "Bb", "F", "C", "Dm", "Bb", "C", "F", "Bb", "F", "Bb", "C", "F", "Dm", "C", "F"]
SC = [("夜", 16, "intro", CH16), ("目覚め", 16, "verse", CH16), ("朝1", 32, "verse", CH16 * 2), ("朝2", 32, "verse", CH16 * 2),
      ("平原", 48, "verse", CH16 * 3), ("崖", 48, "chorus", CH16 * 3), ("ジャン", 2, "outro", ["F", "F"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("夜", 0, 0.66), ("目覚め", 0, 0.7), ("朝1", 0, 0.76), ("朝2", 0, 0.78), ("平原", 0, 0.78), ("平原", 47, 0.78),
          ("崖", 0, 0.9), ("崖", 47, 0.96), ("ジャン", 0, 0.96)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="夜", passing=True, tension=False)
S.fix_avoid = lambda t: 0
S.tempo = [{"bar": 1, "bpm": 40}, {"bar": c.s0["目覚め"] + 1, "bpm": 60, "ramp": 16}, {"bar": c.s0["朝1"] + 1, "bpm": 110}]
S.extra.update({"rubato": 0.3})
B = S.beats
G = c.g()
# 試し書き出し: ギター1本（0.016）でも笛より約8dB 大きい（5本重なる）→ 0.008。ビオラは笛と同じくらい
VA = S.track("ビオラ（森の目覚め）", "strings", patch="viola", volume=0.022, pan=0.25, reverb=0.65, release=0.4, barGain=[round(x * 1.4, 3) for x in G])
VC = S.track("チェロ（森の目覚め）", "strings", patch="cello", volume=0.014, gainDb=1, pan=-0.2, reverb=0.65, release=0.5, barGain=[round(x * 1.4, 3) for x in G])
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=0.3 + 0.05 * i, reverb=0.3, barGain=G) for i in range(5)]

# ---------- 夜の節（1拍に1音。F イオニア。1=F4） ----------
NIGHT = ["5:1 3:1", "2:1 1:1", "3:1 4:1", "5:2", "6:1 5:1", "4:1 3:1", "2:1 3:1", "1:2",
         "1':1 7:1", "6:1 5:1", "4:1 6:1", "5:2", "3:1 4:1", "5:1 3:1", "2:1 7,:1", "1:2"]
def dance(ev, key):
    """1拍に1音 → 1拍に3音。1回目（6.96）はどの拍も「その音・上・その音」で機械的だったので、拍ごとに形を変える：
    1拍目＝その音・上・その音／2拍目以降＝長短（その音 2/3・下 1/3）／句の終わり（2拍の音）＝その音を付点4分でのばす"""
    out = []
    for t, L, m in ev:
        n = int(round(L))
        for k in range(n):
            tt = t + k
            if n >= 2 and k == n - 1: seq = [(m, 1.0)]
            elif k == 0: seq = [(m, T3), (_dia(key, m, 1), T3), (m, T3)]
            else: seq = [(m, 2 * T3), (_dia(key, m, -1), T3)]
            q0 = 0.0
            for x, Lq in seq:
                out.append([round(tt + q0, 4), round(Lq, 4), x]); q0 += Lq
    return out
def night_ev(sc, oct_=4, rep=1):
    ev = []
    for r in range(rep):
        for j, s_ in enumerate(NIGHT):
            ev += mel_events(K, s_, oct_, (c.s0[sc] + 16 * r + j) * B)
    return [[round(t, 4), L, m] for t, L, m in ev]
play(c.FLUTE, ornament(night_ev("夜", 4), K, 40, "air", B, density=0.25, seed=4001))          # 夜：1拍に1音、低く
play(c.FLUTE, ornament(night_ev("目覚め", 4), K, 50, "air", B, density=0.3, seed=4002))       # 目覚め：同じ節、少しずつ速く
for sc, rep, d in (("朝1", 2, 0.1), ("朝2", 2, 0.15), ("平原", 3, 0.15), ("崖", 3, 0.22)):    # 朝：同じ節が、1拍に3音のジグに
    ev = dance(night_ev(sc, 5 if sc in ("朝2", "崖") else 4, rep), K)
    ev = [[t, L, m if m <= 84 else m - 12] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 110, "jig", B, density=d, seed=4003 + len(sc)))
s0 = c.s0["ジャン"]
c.FLUTE.at(s0 * B, "F5:1!")

# ---------- 森の目覚め（弦）とギター ----------
ROOT = {"F": 41, "Bb": 46, "C": 48, "Dm": 50}
JIG = [(0, 2 * T3, "d", "!"), (2 * T3, T3, "u", ","), (1, 2 * T3, "d", ""), (1 + 2 * T3, T3, "u", ",")]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    th = r + (3 if ch.endswith("m") else 4)
    if n == "目覚め" or (n in ("朝1", "崖") and i % 2 == 0):
        VC.at(b * B, f"{nm(r + 12 if r + 12 <= 55 else r)}:{2 if n == '目覚め' else 4},")
        VA.at(round(b * B + 0.05, 3), f"{nm(th + 12 if th + 12 <= 69 else th)}:{2 if n == '目覚め' else 4},")
    if n in ("朝1", "朝2", "平原", "崖"):
        strum(GT, b, B, ch, JIG if not (n == "朝1" and i < 8) else [(0, 2, "d", ",")])
    if n == "ジャン" and i == 0:
        strum(GT, b, B, ch, [(0, 1, "d", "!")]); VC.at(b * B, "F3:1!"); VA.at(b * B, "A4:1!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の040（第3版）。第4章の終わり、夜明けの森を出ていく。笛ひとりの夜の節（1拍に1音、付点4分＝40）が、日が差すと同じ音のまま1拍に3音になり、朝のジグ（6/8・付点4分＝110）に変わる。F イオニア。弦（ビオラとチェロ）の森が目覚め、ナイロン弦ギターが迎える。朝の踊りがしばらく同じ強さで続いたあと、最後の崖で一気に強くなり、全員で「ジャン」と鳴らす。",
       harm_scenes=None, tail_scene="ジャン", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.22, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air040.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
