import re
# ケルト・フルート100曲「銀の笛と百の夜」001 銀の笛 The Silver Flute（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 祖父の箱から銀の笛を出す夕暮れ。笛に最初のひと息を吹き込む。3音の問いが、少しずつ伸びて、やがて答えが返り、また静かになる。
# 強さ: 息(pp)→問い(pp)→伸びる(p)→答え(mp→mf。いちばん大きい)→1拍の無音→余韻(pp)→終わり(ppp)
# 空気: 夕暮れの小さな波と遠い風（c100_air.py で本物の録音を下に敷く）
import sys
from vb25_lib import *

S = Song("C100", "001-silver-flute", "銀の笛", "The Silver Flute", 54, 4, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("息", 4, "intro", ["Em", "Em", "Em/G", "Em"])
S.scene("問い", 12, "verse", ["Em", "D/E", "Em7", "Cmaj7", "Am7", "Em/G", "D", "Em", "Cmaj7", "D", "Am7", "Em"])
S.scene("伸びる", 12, "verse", ["Em", "G", "D", "Em", "Cmaj7", "Am7", "Em/G", "D", "C", "G/B", "Am7", "Em"])
S.scene("答え", 12, "chorus", ["Cmaj7", "D", "Em", "Em/G", "Am7", "D", "G", "Em", "Cmaj7", "D/F#", "Am7", "Em"])
S.scene("余韻", 12, "break", ["Em", "D/E", "Em7", "Cmaj7", "Am7", "Em", "Em", "D", "Cmaj7", "Em/G", "Am7", "Em"])
S.scene("終わり", 8, "outro", ["Em", "Em", "Em", "Em", "Em", "Em", "Em", "Em"])
K = S.key
NB = S.nb

def curve(points):
    out = []
    pts = sorted(points)
    for b in range(NB):
        for (b0, v0), (b1, v1) in zip(pts, pts[1:]):
            if b0 <= b <= b1:
                out.append(round(v0 + (v1 - v0) * (b - b0) / max(1, b1 - b0), 3)); break
        else: out.append(pts[-1][1])
    return out
s0 = {n: S.sc(n)[0] for n in ("息", "問い", "伸びる", "答え", "余韻", "終わり")}
DYN = curve([(0, 0.72), (s0["問い"], 0.68), (s0["伸びる"], 0.72), (s0["答え"], 0.82), (s0["答え"] + 6, 1.0), (s0["余韻"] - 1, 0.9),
             (s0["余韻"], 0.45), (s0["終わり"], 0.4), (NB - 1, 0.3)])
# 伴奏は、答えの山でフルートを埋めないように 0.72 倍に抑える（フルートが小さい件。2026-10-28）
ACC = [0.4 if s0["答え"] + 7 <= b < s0["余韻"] else 0.72 if s0["答え"] <= b < s0["余韻"] else (0.5 if s0["問い"] <= b < s0["答え"] else 1.0) for b in range(NB)]
def g(extra=None):
    return [round(d * ACC[b] * (extra[b] if extra else 1), 3) for b, d in enumerate(DYN)]

FLUTE = S.track("フルート", "panflute", patch="flute", volume=0.42, pan=-0.05, reverb=0.5, breath=True, barGain=[round(max(d, 0.82) * (1.18 if s0["答え"] <= b < s0["余韻"] else (1.4 if s0["問い"] <= b < s0["答え"] else 1.0)), 3) for b, d in enumerate(DYN)])
HARP = S.track("ハープ", "harp", patch="folkHarp", recipe="celtic-harp", volume=0.105, pan=-0.1, reverb=0.45, barGain=g())
HARP2 = S.track("ハープ（高い響き）", "harp", patch="folkHarp", volume=0.055, pan=0.4, reverb=0.6, barGain=g())
STR = [S.track(f"弦の持続{i}", "strings", patch="slowStrings", recipe="celtic-strings", volume=0.05, pan=[-0.7, 0.7, 0][i], reverb=0.55, barGain=g()) for i in range(3)]
LOW = S.track("チェロ", "strings", patch="cello", recipe="celtic-low", volume=0.07, pan=-0.15, reverb=0.35, barGain=g())
BELL = S.track("ベル", "bell", patch="glockenspiel", volume=0.045, pan=0.35, reverb=0.7, barGain=g())
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
SIL = Silence(S)

# ---------- 旋律（E ドリアン。3音の問い：1 3 4） ----------
Q = [
 ["R:1 1:1 3:1.5 R:0.5", "4:3 R:1", "R:2 3:1 1:1", "2:3 R:1"],
 ["1:1 3:1 4:1 6:1", "5:3 R:1", "4:1 3:1 2:1 1:1", "7,:3 R:1"],
 ["1:1 3:1 5:1 7:1", "1':3 R:1", "7:1 6:1 5:1 4:1", "3:3 R:1"],
]
E = [
 ["3:1 5:1 6:1 1':1", "2':2 1':1 7:1", "6:1.5 5:0.5 4:1 3:1", "2:3 R:1"],
 ["1:0.5 2:0.5 3:1 5:1 6:1", "7:1 1':1 2':2", "3':2 2':1 1':1", "7:3 R:1"],
 ["6:1 5:1 4:1 3:1", "2:1 3:1 4:2", "5:1 4:1 3:1 2:1", "1:4"],
]
A = [
 ["1':1 7:0.5 6:0.5 5:1 3:1", "4:1.5 5:0.5 6:2", "7:1 6:1 5:1 4:1", "3:3 R:1"],
 ["5:1 6:1 1':1 3':1", "2':2 1':1 7:1", "6:1 7:1 1':1 5:1", "6:4"],
 ["3':1 2':1 1':1 7:1", "6:1 5:1 4:1 3:1", "2:1 3:1 4:1 2:1", "1:4"],
]
T = ["1:2 3:2", "4:4", "R:4", "3:2 1:2", "2:3 R:1", "R:4", "1:2 3:2", "4:2 3:2", "2:4", "R:4", "1:4", "R:4"]
_N = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
def _midi(tok):
    m = re.match(r"^([A-G])([#b]?)(-?\d+):", tok)
    if not m: return None
    return (int(m.group(3)) + 1) * 12 + _N[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0)
def shift(txt, d):
    out = []
    for tok in txt.split():
        m = re.match(r"^([A-G][#b]?)(-?\d+)(:.*)$", tok)
        out.append(f"{m.group(1)}{int(m.group(2)) + d}{m.group(3)}" if m else tok)
    return " ".join(out)
def fold_phrase(bars_txt, hi=84):
    """パンフルートの音域（〜C6）より高い音が1つでもあるフレーズは、まるごと1オクターブ下げる（旋律の形を保つ。高い音は小さくしか鳴らないため。2026-10-28）"""
    ps = [_midi(t) for txt in bars_txt for t in txt.split()]
    ps = [p for p in ps if p is not None]
    if ps and max(ps) > hi and min(ps) - 12 >= 60: return [shift(t, -1) for t in bars_txt]
    return bars_txt
def put(scene, phr, oct_):
    bars = S.sc(scene)
    for p, ph in enumerate(phr):
        txt = [K.mel(x, oct=oct_) for x in ph]   # 実測：笛は高い音（〜F#6）のほうが大きく鳴る。下げると小さくなる（2026-10-28）
        for j, t in enumerate(txt): FLUTE.bar(bars[p * 4 + j], t)
put("問い", Q, 5); put("伸びる", E, 5); put("答え", A, 5)
for i, b in enumerate(S.sc("余韻")): FLUTE.bar(b, K.mel(T[i], oct=4 if i < 6 else 5))
for i, b in enumerate(S.sc("終わり")):
    if i == 1: FLUTE.bar(b, K.mel("1:4", oct=5))
    if i == 2: FLUTE.bar(b, K.mel("R:4", oct=5))

# 笛の低い音（E4〜A4あたり）は、同じ強さで鳴らしても小さく聞こえる。小節ごとの平均の高さで音量を足す（2026-10-28。答えの後半・余韻が小さかった）
def _lowboost():
    import collections
    pb = collections.defaultdict(list)
    for st, L, x in FLUTE.ev:
        p = _midi(x if ":" in x else x + ":1")
        if p is not None: pb[int(st // 4)].append(p)
    bg = FLUTE.spec["barGain"]
    for b, ps in pb.items():
        if not (s0["答え"] + 7 <= b < s0["余韻"]): continue   # 測って小さかった所（答えの後半）だけ
        m = sum(ps) / len(ps)
        k = min(1.0, max(0.35, (72 - m) / 8))
        bg[b] = round(bg[b] * (1 + 1.6 * k), 3)

# ---------- 伴奏 ----------
for b in range(NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6")
    if n == "息":
        if i in (0, 2): HARP.bar(b, f"{nm(t[0])}:4")
        if i in (1, 3): HARP2.bar(b, f"{nm(t[-3])}:4")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")
    elif n == "問い":
        HARP.bar(b, f"{nm(t[0])}:4" if i % 2 == 0 else f"{nm(t[2])}:2 R:2")
        if i % 4 == 3: HARP2.bar(b, f"R:2 {nm(t[-2])}:2")
        if i >= 8: LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
    elif n == "伸びる":
        HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 3)))
        LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        if i >= 4:
            v = voice(ch, 62, 3, spread=True)
            for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")
    elif n == "答え":
        if i < 8:
            HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 6, 7, 6, 4, 2)))
            HARP2.bar(b, " ".join(f"{nm(x)}:0.5" for x in [t[-1], t[-2], t[-3], t[-2]] * 2) if i % 2 == 0 else f"{nm(t[-1])}:4")
        else:   # 答えの終わりの4小節：笛が下りてくるので、竪琴は細かく動かず、ゆっくりにする（笛が埋もれていた。2026-10-28）
            HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2")
            if i % 2 == 0: HARP2.bar(b, f"{nm(t[-1])}:4")
        LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")
        if i % 2 == 1 and i < 8: BELL.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C6", "C7")[:4]))
    elif n == "余韻":
        if i % 2 == 0: HARP2.bar(b, f"{nm(t[-1])}:2 {nm(t[-3])}:2")
        if i < 8: HARP.bar(b, f"{nm(t[0])}:4")
        if i in (4, 5, 6, 7, 8, 9):
            v = voice(ch, 64, 2)
            for j in range(2): STR[j].bar(b, f"{nm(v[j])}:4")
    elif n == "終わり":
        if i == 0: HARP.bar(b, f"{nm(t[0])}:4")
        if i == 3: HARP2.bar(b, f"{nm(t[-3])}:4")
        if i == 5: BELL.bar(b, f"{nm(tones(ch, 'C6', 'C7')[2])}:4")
cym_swell(CYM, s0["答え"] + 4, 4, "E4")
CYM.bar(NB - 3, "B4:12")
SIL.add(s0["余韻"] - 1, 3, 4)
SIL.apply()
S.fade_out = 0
S.flags = "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0"
S.desc = "ケルト・フルート100曲の001。祖父の箱から銀の笛を出す夕暮れ。E ドリアン・54。3音の問いが少しずつ伸びて、答えが返り、静けさに戻る。"
vwrite(S)
