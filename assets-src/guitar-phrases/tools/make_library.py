# ギターとベースのフレーズのライブラリを作る（2026-10-22 人間「ギターとベースも1000通りぐらいおねがいしたい」）
#   python3 make_library.py [GuitarSet から取り出した型.json]
#   → assets-src/guitar-phrases/phrases.json・assets-src/bass-phrases/phrases.json
# 既存の曲のリフ・旋律・ベースラインは写さない（CLAUDE.md 1-1）。ここの型はすべて、一般的な技法（docs/sound/modern-loud-rock/vocabulary.md 3章・
# arrangement-detail.md 3〜4章・bassline-guide.md）から組み立てたもの。実演の型は GuitarSet（CC BY 4.0）の進行1・3だけ（guitarset_extract.py）。
# ふるい落としの規則は docs/sound/guitar-bass-phrase-library.md 3章（このファイルの keep_* と loud25_phrases.check）。
import sys, os, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "assets-src", "ai-songs", "_gen"))
import loud25_phrases as LP
from loud25_phrases import MODES, BAR, chug_ratio, check, signature

S16, E8, Q = 3, 6, 12
NEUTRAL = ["m", "m7", "M", "maj7", "7", "5", "sus"]
MINOR_MODES = ["aeolian", "aeolian", "phrygian", "dorian", "harmonic"]
MAJOR_MODES = ["mixolydian", "lydian", "ionian"]

def fam_of(mode): return ["M", "maj7", "7", "5"] if mode in MAJOR_MODES else ["m", "m7", "5"]

def ev(t, d, ivs, mk=""): return [int(t), int(d), list(ivs), mk]

# ═════════════════ ギター: リフ ═════════════════
POWER = [0, 7, 12]
def pc_degrees(mode):
    sc = MODES[mode]
    return [d for d in sc if (d + 7) % 12 in [x % 12 for x in sc]]

def mel_notes(mode, lo, hi):
    return [x + 12 * o for o in range(-1, 4) for x in MODES[mode] if lo <= x + 12 * o <= hi]

class RiffGen:
    def __init__(self, rng, mode):
        self.r, self.mode = rng, mode
        self.degs = pc_degrees(mode)
        self.mel = mel_notes(mode, 12, 24)
    def chord(self, deg=0, kind=None):
        kind = kind or self.r.choice(["power", "power", "5-9", "dyad"])
        base = {"power": POWER, "5-9": [0, 7, 14], "dyad": [0, 7]}[kind]
        return [deg + x for x in base]
    def walk(self, n, start=None, span=(12, 24)):
        mel = [m for m in self.mel if span[0] <= m <= span[1]]
        k = mel.index(start) if start in mel else self.r.randrange(len(mel))
        out = []
        dirn = self.r.choice([-1, 1])
        for i in range(n):
            out.append(mel[k])
            step = self.r.choice([1, 1, 1, 2]) * dirn
            if self.r.random() < 0.25: dirn = -dirn
            k2 = k + step
            if not 0 <= k2 < len(mel): dirn = -dirn; k2 = k - step
            k = max(0, min(len(mel) - 1, k2))
        return out
    # ── かたまり（区間 [t0, t0+span) に音を置く。返り値: (音の並び, 種類の集合)）──
    def pedal(self, t0, span, rate=None):
        rate = rate or self.r.choice([S16, S16, E8])
        out = []
        for k, t in enumerate(range(t0, t0 + span, rate)):
            if k > 0 and rate == S16 and self.r.random() < 0.18: continue
            out.append(ev(t, S16, [0], ("!'" if k == 0 else "'")))
        return out, {"開放弦ペダル", "刻み"}
    def sustain(self, t0, span):
        deg = self.r.choice([0, 0] + self.degs)
        return [ev(t0, span, self.chord(deg), "!")], {"伸ばす"}
    def stab(self, t0, span):
        d = self.r.choice([S16, E8])
        out = [ev(t0, d, self.chord(self.r.choice([0] + self.degs)), "!")]
        return out, ({"休み"} if span - d >= E8 else set())
    def octave(self, t0, span):
        step = self.r.choice([E8, E8, Q]) if span >= 12 else E8
        n = max(1, span // step)
        notes = self.walk(n, span=(12, 19))
        out = []; slid = False
        for k, x in enumerate(notes):
            mk = "!" if k == 0 else ""
            if k == 0 and self.r.random() < 0.45: mk += "//@0.1"; slid = True
            out.append(ev(t0 + k * step, step if k < n - 1 else span - k * step, [x, x + 12], mk))
        return out, {"オクターブ"} | ({"スライド"} if slid else set())
    def pedaltone(self, t0, span):
        notes = self.walk(span // E8 + 1, span=(12, 24))
        out = []
        for k, t in enumerate(range(t0, t0 + span, S16)):
            if k % 2 == 0: out.append(ev(t, S16, [0], "'"))
            else: out.append(ev(t, S16, [notes[k // 2]], ""))
        return out, {"ペダルトーン"}
    def rest(self, t0, span):
        return [], {"休み"}
    def dotted(self, t0, span):
        out = []; t = t0; k = 0
        style = self.r.choice(["hit", "hitchug"])
        degs = [0] + [self.r.choice(self.degs) for _ in range(3)]
        while t < t0 + span:
            d = min(9, t0 + span - t)
            if style == "hit" or d < 9:
                out.append(ev(t, d, self.chord(degs[k % len(degs)], "power"), "!"))
            else:
                out.append(ev(t, E8, self.chord(degs[k % len(degs)], "power"), "!")); out.append(ev(t + E8, S16, [0], "'"))
            t += 9; k += 1
        return out, {"付点"}
    def triplet2(self, t0, span):
        out = []
        degs = self.r.choice([[0, 10, 8], [0, 3, 5], [8, 10, 12], [0, 5, 3], [10, 8, 7], [0, 7, 5]])
        degs = [d if d in self.degs + [0, 12] else 0 for d in degs]
        for k in range(span // 8):
            out.append(ev(t0 + 8 * k, 8, [degs[k % 3] + x for x in POWER], "!" if k == 0 else ""))
        return out, {"2拍3連"}
    def dissonant(self, t0, span):
        v = self.r.choice([[0, 7, 13], [0, 6], [0, 1, 7], [0, 7, 8]])
        return [ev(t0, span, v, "!")], {"不協和", "伸ばす"}

BAR_SPLITS = [[24, 24], [12, 12, 24], [24, 12, 12], [18, 18, 12], [36, 12], [12, 36], [48], [18, 30], [30, 18], [12, 12, 12, 12], [6, 18, 24], [24, 18, 6]]
BLOCK_W = {  # 流派ごとの、かたまりの選ばれやすさ
    "混ぜる": dict(pedal=3, sustain=3, stab=2, octave=2, pedaltone=1, rest=2, dotted=1, triplet2=1, dissonant=0.3),
    "刻み→伸ばす": dict(pedal=5, sustain=5, stab=1, octave=1, pedaltone=0, rest=1, dotted=0.5, triplet2=0, dissonant=0),
    "ペダルトーン": dict(pedal=1, sustain=2, stab=1, octave=1, pedaltone=6, rest=1, dotted=0, triplet2=0, dissonant=0),
    "オクターブ": dict(pedal=1, sustain=2, stab=1, octave=6, pedaltone=1, rest=2, dotted=0, triplet2=0.5, dissonant=0),
    "付点": dict(pedal=1, sustain=2, stab=1, octave=1, pedaltone=0, rest=1, dotted=6, triplet2=0, dissonant=0),
    "2拍3連": dict(pedal=2, sustain=2, stab=1, octave=1, pedaltone=0, rest=1, dotted=0, triplet2=5, dissonant=0),
    "不協和": dict(pedal=2, sustain=1, stab=2, octave=0, pedaltone=0, rest=3, dotted=1, triplet2=0, dissonant=4),
}
def wchoice(r, w):
    ks = [k for k, v in w.items() if v > 0]; return r.choices(ks, [w[k] for k in ks])[0]

def fix_mute_after_sustain(evs):
    """伸ばした音（1拍以上）のすぐ後にミュートの刻みが来るときは、伸ばす音を8分短くして間を空ける（banned-sounds: 弾いている途中で急にミュートへ切りかえない）"""
    evs.sort(key=lambda e: e[0])
    for a, b in zip(evs, evs[1:]):
        if a[1] >= Q and "'" not in a[3] and "'" in b[3] and a[0] + a[1] >= b[0]:
            a[1] = max(E8, b[0] - a[0] - E8)
    return evs

def riff_bar(g, flavor, split=None):
    split = split or g.r.choice(BAR_SPLITS)
    out, kinds = [], set()
    t = 0
    for i, sp in enumerate(split):
        b = wchoice(g.r, BLOCK_W[flavor])
        if b == "triplet2" and (sp != 24 or t % 24): b = "sustain"
        if b in ("pedaltone",) and sp < 12: b = "pedal"
        if b == "rest" and (sp > 18 or i == 0): b = "stab"
        e, k = getattr(g, b)(t, sp)
        out += e; kinds |= k; t += sp
    return out, kinds

def tail(g, t0=24):
    c = g.r.choice(["ため", "伸ばす", "駆け上がりオクターブ", "2拍3連", "スライドの一撃"])
    if c == "ため": return [ev(t0, E8, g.chord(0), "!")], {"休み"}
    if c == "伸ばす": return [ev(t0, 24, g.chord(g.r.choice(g.degs)), "!")], {"伸ばす"}
    if c == "駆け上がりオクターブ":
        ns = sorted(g.walk(4, span=(12, 19)))
        return [ev(t0 + 6 * k, 6, [x, x + 12], "!" if k == 0 else "") for k, x in enumerate(ns)], {"オクターブ"}
    if c == "2拍3連": return g.triplet2(t0, 24)
    return [ev(t0 + 12, 12, g.chord(g.r.choice(g.degs)), "!//@0.1")], {"スライド", "休み"}

def shift(evs, dt): return [[e[0] + dt, e[1], list(e[2]), e[3]] for e in evs]

def gen_riff(r, idx):
    mode = r.choice(MINOR_MODES * 3 + MAJOR_MODES)
    g = RiffGen(r, mode)
    flavor = r.choice(list(BLOCK_W))
    nb = r.choices([1, 2, 4], [0.15, 0.5, 0.35])[0]
    odd = r.random() < 0.18 and flavor != "不協和"
    if odd:
        evs, kinds = odd_riff(g, nb if nb > 1 else 2)
        nb = nb if nb > 1 else 2
    else:
        A, kA = riff_bar(g, flavor)
        bars = [(A, kA)]
        if nb >= 2:
            if r.random() < 0.6:   # 2小節目は前半が同じで後半が違う
                B2, kB = riff_bar(g, flavor, [24, 24])
                B = [e for e in A if e[0] < 24 and e[0] + e[1] <= 24] + [e for e in B2 if e[0] >= 24]
            else:
                B, kB = riff_bar(g, flavor)
            bars.append((B, kB))
        if nb == 4:
            plan = r.choice(["AA'AT", "ABAB'", "AA'A''T"])
            if plan == "AA'AT":
                T, kT = tail(g); bars += [(A, kA), ([e for e in A if e[0] + e[1] <= 24] + T, kA | kT)]
            elif plan == "ABAB'":
                T, kT = tail(g); bars += [(A, kA), ([e for e in bars[1][0] if e[0] + e[1] <= 24] + T, bars[1][1] | kT)]
            else:
                C2, kC = riff_bar(g, flavor, [24, 24]); T, kT = tail(g)
                bars += [([e for e in A if e[0] + e[1] <= 24] + [e for e in C2 if e[0] >= 24], kA | kC), ([e for e in A if e[0] + e[1] <= 24] + T, kA | kT)]
        evs, kinds = [], set()
        for b, (e, k) in enumerate(bars):
            evs += shift(e, b * BAR); kinds |= k
    evs = fix_mute_after_sustain([e for e in evs if e[1] > 0])
    return mk_phrase("guitar", "リフ", "リフ（" + ("5・7のかたまり" if odd else flavor) + "）", nb, evs, kinds, fam_of(mode), mode, f"gr{idx}", pc=True)

def odd_riff(g, nb):
    L = g.r.choice([5, 5, 7, 7, 3])
    syms = {5: ["Hcc-c", "H-cOc", "Hc-cc", "H-O-c", "Hcbc-", "HccO-"], 7: ["Hcc-cOc", "Hc-Hc-c", "H-ccO-c", "Hcc-Hcb", "H--cOcc"], 3: ["Hcc", "H-c", "Hc-"]}[L]
    cell = g.r.choice(syms)
    oct_note = g.r.choice([12, 15 if g.mode not in MAJOR_MODES else 16, 10, 7 + 12])
    total16 = nb * 16 - 8     # 最後の2拍は「しっぽ」（伸ばして小節の頭にもどす）
    out = []; kinds = {f"{L}のかたまり" if L > 3 else "付点"}
    for s in range(total16):
        c = cell[s % L]
        t = s * S16
        if c == "H": out.append(ev(t, S16, g.chord(0, "power"), "!"))
        elif c == "c": out.append(ev(t, S16, [0], "'")); kinds |= {"開放弦ペダル", "刻み"}
        elif c == "O": out.append(ev(t, S16, [oct_note], "")); kinds.add("オクターブ" if oct_note % 12 == 0 else "高い音")
        elif c == "b": out.append(ev(t, S16, [1 if g.mode == "phrygian" else 13], "")); kinds.add("不協和" if g.mode != "phrygian" else "♭2")
        elif c == "-": kinds.add("休み")
    # 和音の打撃は次の音まで伸ばす
    for i, e in enumerate(out):
        if len(e[2]) > 1:
            nxt = out[i + 1][0] if i + 1 < len(out) else total16 * S16
            e[1] = max(S16, nxt - e[0])
    t0 = total16 * S16
    tl = g.r.choice(["伸ばす", "ため"])
    if tl == "伸ばす": out.append(ev(t0, 24, g.chord(g.r.choice(g.degs), "power"), "!")); kinds.add("伸ばす")
    else: out.append(ev(t0, E8, g.chord(0), "!")); out.append(ev(t0 + 18, E8, g.chord(g.r.choice(g.degs)), "!")); kinds.add("休み")
    return out, kinds

# ═════════════════ ギター: サビのバッキング ═════════════════
BACK_T = ["X=======", "X===X===", "X===x===", "X==X==x=", "X==x====", "X=====x=", "X===-x==", "X==-X===", "X=x=X===", "X=====-x",
          "X===X=-x", "X=x=X=x=", "xxxxxxxx", "X=xxX=xx", "X=-X=-X=", "X==X==X=", "X=====>", "X==X===>", "--X=====", "X=======", "X===X==>",
          "X.x.X.x.", "X=====--", "X==-x===", "x=x=xxx="]
def gen_backing(r, idx):
    mode = r.choice(MINOR_MODES + MAJOR_MODES)
    minor = mode not in MAJOR_MODES
    nb = r.choices([1, 2, 4], [0.1, 0.4, 0.5])[0]
    voic = r.choice(["power", "5-9", "5-9", "power+3", "top-move", "oct"])
    third = 15 if minor else 16
    tops_pool = {"power": [12], "5-9": [14], "power+3": [third], "oct": [12], "top-move": [12, 14, third, 14, 19, 12]}[voic]
    plan = r.choice(["AAAB", "ABAB", "AABC", "AAAA'", "ABAC"])[:nb] if nb > 1 else "A"
    pats = {}
    for c in set(plan.replace("'", "")):
        pats[c] = r.choice(BACK_T)
    seq = []
    for i, c in enumerate(plan.replace("'", "")[:nb]):
        p = pats[c]
        if i == nb - 1 and p.endswith(">"): p = p[:-1] + r.choice(["=", "-"])
        seq.append(p)
    if "'" in plan and nb == 4: seq[3] = seq[3][:4] + r.choice(["X===", "X=-x", "--x=", "X=X="])
    if nb == 4 and r.random() < 0.5: seq[3] = seq[3][:6] + "--"    # 区切りの前に息つぎ
    evs = []; tech = set(["伸ばす"])
    top_i = r.randrange(len(tops_pool))
    for b, p in enumerate(seq):
        p = p.ljust(8, "=")[:8]
        if b > 0 and seq[b - 1].endswith(">"): p = "=" + p[1:]
        top = tops_pool[(top_i + b * r.choice([1, 1, 2])) % len(tops_pool)] if voic == "top-move" else tops_pool[0]
        voicing = [0, 7] + ([top] if voic != "power" or True else [])
        for s, c in enumerate(p):
            t = b * BAR + s * E8
            if c in "Xx>":
                if c == ">": tech.add("食い（前のめり）")
                evs.append(ev(t, E8, voicing, "!" if c in "X>" else ""))
            elif c == "=" and evs and evs[-1][0] + evs[-1][1] == t:
                evs[-1][1] += E8
            elif c == "-": tech.add("休み")
            elif c == ".":   # 8分で短く切る（アクセントの伸ばしの間）
                pass
    if any(p.startswith("xxxx") or p.count("x") >= 3 for p in seq): tech.add("8分のストローク")
    fits = ["m", "m7", "5"] if (voic == "power+3" or (voic == "top-move")) and minor else (["M", "maj7", "7", "5"] if voic in ("power+3", "top-move") else NEUTRAL)
    if voic == "top-move" and 17 in tops_pool: tech.add("上の声が動く")
    return mk_phrase("guitar", "バッキング", f"バッキング（{voic}）", nb, evs, tech, fits, mode, f"gb{idx}", pc=False)

# ═════════════════ ギター: アルペジオ ═════════════════
POOLS = {"madd9": ([0, 7, 12, 14, 15, 19], ["m"]), "m7": ([0, 7, 10, 15, 19, 22], ["m7", "m"]), "m": ([0, 7, 12, 15, 19, 24], ["m"]),
         "add9": ([0, 7, 12, 14, 16, 19], ["M"]), "maj7": ([0, 7, 11, 16, 19, 23], ["maj7", "M"]), "sus2": ([0, 7, 12, 14, 19, 24], ["sus", "5", "m", "M"]),
         "6/9": ([0, 7, 9, 14, 16, 21], ["M"]), "m11": ([0, 7, 10, 15, 17, 22], ["m7", "m"])}
SHAPES = [  # 分散和音の形（和音の音の番号。となりか1つ飛ばしで動く＝弦をまたぎすぎない）
    [0, 1, 2, 3, 4, 3, 2, 1], [0, 2, 1, 3, 2, 4, 3, 2], [1, 4, 2, 4, 3, 4, 2, 4], [0, 1, 3, 2, 4, 3, 5, 4], [5, 4, 3, 2, 1, 2, 3, 4], [0, 2, 3, 4, 3, 2, 1, 2],
    [0, 1, 2, 4, 3, 4, 2, 3], [2, 3, 4, 5, 4, 3, 2, 1], [0, 2, 4, 3, 5, 4, 3, 2], [1, 2, 3, 1, 4, 3, 2, 3], [0, 1, 2, 3, 2, 4, 3, 5], [3, 4, 5, 4, 3, 2, 3, 1]]
RHY = [[6] * 8, [6, 6, 12, 6, 6, 12], [12, 6, 6, 12, 12], [9, 9, 6, 9, 9, 6], [6, 6, 6, 6, 12, 12], [3, 3, 6, 6, 6, 6, 6, 12], [6, 12, 6, 6, 12, 6],
       [18, 6, 6, 6, 12], [9, 9, 6, 6, 6, 12], [6, 6, 6, 6, 6, 6, 12], [3, 3, 3, 3, 6, 6, 12, 12]]
def gen_arp(r, idx):
    pk = r.choice(list(POOLS)); pool, fits = POOLS[pk]
    nb = r.choices([1, 2, 4], [0.15, 0.45, 0.4])[0]
    sh = r.sample(range(len(SHAPES)), 3)
    rh = r.sample(range(len(RHY)), 2)
    plan = r.choice(["ABAC", "ABCB", "AABC", "ABA'C"])
    evs = []; tech = {"アルペジオ"}
    for b in range(nb):
        c = plan[b] if b < len(plan) else "A"
        s = SHAPES[sh["ABC".index(c) if c in "ABC" else 0]]
        if b == 2 and "'" in plan: s = s[1:] + s[:1]
        rr = RHY[rh[0] if c != "C" else rh[1]]
        if b == nb - 1 and nb > 1:      # 最後の小節は長い音で終わる
            rr = r.choice([[6, 6, 6, 6, 24], [12, 12, 24], [6, 6, 12, 24], [6, 6, 36]])
        t = 0; k = 0
        for d in rr:
            if t + d > BAR: d = BAR - t
            if d <= 0: break
            iv = pool[s[k % len(s)]]
            mk = "_" if d <= 6 else ""
            if t == 0: mk = "!" + mk
            if r.random() < 0.06 and t > 0 and d <= 6:
                tech.add("休み"); t += d; k += 1; continue
            evs.append(ev(b * BAR + t, d, [iv], mk))
            t += d; k += 1
        if any(x in (9, 9) for x in rr): tech.add("付点")
    # 共通の高い音（ペダルの上の音）を使う形
    if 2 in sh: tech.add("上の音のペダル")
    mode = "aeolian" if "m" in fits[0] else "ionian"
    ph = mk_phrase("guitar", "アルペジオ", f"アルペジオ（{pk}）", nb, evs, tech, fits, None, f"ga{idx}", pc=False)
    ph["ref"] = "E3"
    return ph

# ═════════════════ ギター: リードの短い句（2小節・問いと答え）═════════════════
LEAD_Q = [[(2, 2), (4, 2), (6, 4), (10, 6)], [(0, 3), (3, 3), (6, 2), (8, 8)], [(2, 1), (3, 1), (4, 2), (6, 2), (8, 8)], [(4, 2), (6, 2), (8, 2), (10, 6)],
          [(1, 1), (2, 2), (4, 4), (8, 4), (12, 4)], [(0, 6), (6, 2), (8, 8)], [(2, 2), (4, 2), (6, 2), (8, 2), (10, 2), (12, 4)], [(3, 1), (4, 3), (7, 1), (8, 8)],
          [(2, 2), (4, 6), (10, 2), (12, 4)], [(0, 4), (4, 2), (6, 2), (8, 4), (12, 4)], [(2, 2), (4, 2), (6, 10)], [(6, 2), (8, 2), (10, 2), (12, 4)]]
LEAD_A = [[(0, 2), (2, 2), (4, 8)], [(0, 3), (3, 3), (6, 6)], [(2, 2), (4, 2), (6, 2), (8, 6)], [(0, 4), (4, 4), (8, 4)], [(0, 2), (2, 1), (3, 1), (4, 2), (6, 6)],
          [(0, 6), (6, 6)], [(2, 2), (4, 4), (8, 4)], [(0, 2), (2, 2), (4, 2), (6, 2), (8, 4)]]
TENSION_END = {"m": [2, 7, 10, 14, 19], "M": [2, 7, 9, 14, 19]}
STABLE_END = {"m": [0, 3, 7, 12, 15], "M": [0, 4, 7, 12, 16]}
CT = {"m": {0, 3, 7, 10}, "M": {0, 4, 7, 11}}
def gen_lead(r, idx):
    minor = r.random() < 0.65
    q = "m" if minor else "M"
    mode = r.choice(["aeolian", "dorian", "minpent", "minpent", "phrygian", "harmonic"] if minor else ["ionian", "mixolydian", "majpent", "majpent", "lydian"])
    sc = mel_notes(mode, -9, 12)
    Qr = r.choice(LEAD_Q); Ar = list(Qr) if r.random() < 0.45 else r.choice(LEAD_A)
    if Ar == Qr:   # 答えは同じリズムで、最後の音を短くして息つぎ
        last = Ar[-1]; Ar = Ar[:-1] + [(last[0], max(2, min(4, last[1])))]
    tech = {"問いと答え"}
    cur = r.choice([x for x in sc if 0 <= x <= 9])
    evs = []
    def pick_next(cur, strong, final=None):
        if final: return min(final, key=lambda x: (abs(x - cur), r.random()))
        k = min(range(len(sc)), key=lambda i: abs(sc[i] - cur))
        step = r.choice([1, 1, 1, -1, -1, 2, -2, 0])
        if r.random() < 0.12: step = r.choice([3, 4, -3])
        x = sc[max(0, min(len(sc) - 1, k + step))]
        if strong:
            cts = [y for y in sc if y % 12 in CT[q] and abs(y - x) <= 3]
            if cts: x = min(cts, key=lambda y: abs(y - x))
        return x
    for b, rh in enumerate([Qr, Ar]):
        for j, (s, d) in enumerate(rh):
            t = b * BAR + s * S16
            last = j == len(rh) - 1
            strong = s % 8 == 0 or d >= 4
            fin = None
            if last: fin = [x for x in sc if x % 12 in [y % 12 for y in (TENSION_END[q] if b == 0 else STABLE_END[q])]]
            nxt = pick_next(cur, strong, fin)
            evs.append(ev(t, d * S16, [nxt], "!" if j == 0 and s % 4 == 0 else ""))
            cur = nxt
    # 駆け上がり（問いの最後の1拍の前を、16分4つの上り順次に）
    if r.random() < 0.35:
        tgt = evs[len(Qr)][2][0] if len(evs) > len(Qr) else None
        if tgt is not None and Ar[0][0] == 0:
            ks = [x for x in sc if x < tgt][-4:]
            if len(ks) == 4 and ks[0] >= -7:
                evs = [e for e in evs if not (BAR - 12 <= e[0] < BAR)]
                for e in evs:
                    if e[0] < BAR - 12 < e[0] + e[1]: e[1] = BAR - 12 - e[0]
                evs += [ev(BAR - 12 + 3 * k, 3, [x], "") for k, x in enumerate(ks)]
                tech.add("駆け上がり")
    evs.sort(key=lambda e: e[0])
    # チョーキング（1句に1回まで。全音上げてコードの音に着く）
    if r.random() < 0.5:
        for e in sorted(evs, key=lambda e: -e[1]):
            x = e[2][0]
            if e[1] >= 6 and (x + 2) % 12 in CT[q] and x % 12 not in CT[q] and (x + 2) % 12 in [y % 12 for y in MODES["aeolian" if minor else "ionian"]] + [y % 12 for y in MODES[mode]]:
                e[3] += "^^"; tech.add("チョーキング"); break
            if e[1] >= 6 and (x + 1) % 12 in CT[q] and minor and x % 12 == 2:
                e[3] += "^"; tech.add("チョーキング"); break
    # スライド（音の中ですべって次の音へ）
    if r.random() < 0.25:
        for i in range(len(evs) - 1):
            a, b2 = evs[i], evs[i + 1]
            dlt = b2[2][0] - a[2][0]
            if a[1] >= 6 and 1 <= abs(dlt) <= 3 and "^" not in a[3] and a[0] + a[1] == b2[0]:
                a[3] += f">{dlt:+d}"; tech.add("スライド"); break
    if any(e[2][0] - p[2][0] >= 5 for p, e in zip(evs, evs[1:])): tech.add("跳躍")
    fits = ["m", "m7"] if minor else ["M", "maj7"] + (["7"] if mode == "mixolydian" or mode == "majpent" else [])
    ph = mk_phrase("guitar", "リード", f"リード（{mode}）", 2, evs, tech, fits, mode, f"gl{idx}", pc=False)
    ph["ref"] = "C4"   # 根音を C4〜B4 に置き、-9〜+12 半音（D#3〜B5）で歌う
    ph["rel"] = "first"; ph["snapct"] = True   # 1小節目の根音を基準にした線（和音が変わっても線がつながる）。強拍の長い音は鳴らすときに和音の音へ寄せる
    return ph

# ═════════════════ ベース ═════════════════
APPROACH = ["N-1", "N+1", "N-2", "N+2", "N-5"]
def bass_ph(role, kind, nb, evs, tech, fits, fam, **kw):
    ph = mk_phrase("bass", role, kind, nb, evs, tech, fits, None, fam, pc=False)
    ph["ref"] = "E1"; ph.update(kw)
    return ph

def slots_to_events(slots, nb, unit, sym_iv, art, r):
    """記号の列（1文字＝unit 刻み）→ 音。= は前の音を伸ばす、- は休み"""
    evs = []
    for i, c in enumerate(slots):
        t = i * unit
        if c == "=" and evs and evs[-1][0] + evs[-1][1] == t: evs[-1][1] += unit; continue
        if c in "-=.": continue
        iv, mk = sym_iv(c, i)
        evs.append(ev(t, unit, [iv], mk))
    if art == "short":
        for e in evs:
            if e[1] > unit and "!" not in e[3]: e[1] = max(unit, e[1] - unit)
    elif art == "mixed":
        for i, e in enumerate(evs):
            if e[0] % Q and e[1] > 3: e[1] = max(3, e[1] // 2)
    return evs

def root_bar_8(r):
    s = ["R"] + [r.choice(["R", "R", "R", "=", "8", "5", "-"]) for _ in range(7)]
    if r.random() < 0.35: s[7] = "A"
    return "".join(s)

DOTTED16 = ["X..x..x.X..x..x.", "X..x..x.x.x.X...", "X.....x.X..x..x.", "X..x..x.X.......", "X..x..X...x.x...", "X.x..x..X.x..x..", "X...x..x..x.X...", "X..x...xX..x....",
            "X..x..x...x.X.x.", "X.....X.....X...", "X..x..x.X..x.x..", "X..X..X.X..X..X.", "X......xX.......", "X...X..x..X.X..."]
SYNC16 = ["X...x.x...x.X.x.", "X..x...x..x.X...", "X.x...x.x...X.x.", "X...x.x.x...x.x.", "X..x.x...x..X...", "X...x..x.x..x...", "X.x.x...X...x.x.", "X.....x.x.....x."]

def gen_bass_root(r, idx):
    nb = r.choices([1, 2, 4], [0.15, 0.4, 0.45])[0]
    style = r.choice(["8分", "8分", "付点", "シンコペーション"])
    art = r.choice(["long", "long", "short", "mixed"])
    plan = r.choice(["AAAB", "ABAB", "AAAA'", "ABAC"])
    use7 = r.random() < 0.2
    pats = {}
    def newpat():
        if style == "8分": return root_bar_8(r)
        src = DOTTED16 if style == "付点" else SYNC16
        p = list(r.choice(src))
        out = []
        for i, c in enumerate(p):
            if c == "X": out.append("R")
            elif c == "x": out.append(r.choice(["R", "R", "8", "5"] + (["7"] if use7 else [])))
            else: out.append("=")
        if art != "long":   # 次の音の直前を1〜2か所だけ休みにして、音を切る（細切れにしない）
            hits = [i for i, c in enumerate(out) if c not in "=-"]
            for i in r.sample(hits[1:], min(len(hits) - 1, r.choice([1, 2]))):
                if i > 0 and out[i - 1] == "=": out[i - 1] = "-"
        if r.random() < 0.3:
            for i in range(15, 10, -1):
                if out[i] not in "=-": out[i] = "A"; break
        return "".join(out)
    unit = E8 if style == "8分" else S16
    seqs = []
    for b in range(nb):
        c = plan[b] if b < len(plan) else "A"
        key = c.replace("'", "")
        if key not in pats: pats[key] = newpat()
        p = pats[key]
        if c.endswith("'") or (b == nb - 1 and nb == 4 and r.random() < 0.6):
            p = p[:len(p) // 2] + newpat()[len(p) // 2:]
        seqs.append(p)
    ap = r.choice(APPROACH)
    def sym_iv(c, i):
        if c == "R": return 0, "!" if i % (len(seqs[0])) == 0 else ""
        if c == "8": return 12, ""
        if c == "5": return 7, ""
        if c == "7": return 10, ""
        if c == "A": return ap, ""
        return 0, ""
    evs = []
    for b, p in enumerate(seqs):
        evs += shift(slots_to_events(p, 1, unit, sym_iv, art, r), b * BAR)
    tech = {"根音", style}
    if any("A" in p for p in seqs): tech.add("アプローチ")
    if any("8" in p for p in seqs): tech.add("オクターブ")
    if any("-" in p for p in seqs): tech.add("休み")
    fits = ["m", "m7", "7", "5"] if use7 else ["m", "m7", "M", "maj7", "7", "5", "sus"]
    return bass_ph("根音", f"根音（{style}）", nb, evs, tech, fits, f"br{idx}")

BASS_RHY = [["X...x.x.X...x.x."], ["X.....x.X...x..."], ["X...x...X.x.x..."], ["X..x..x.X......."], ["X.x.x...X...x.x."], ["X.......X.x.x.x."], ["X...x.x.x...x..."],
            ["X..x..x.x...X..."], ["X...X...X...x.x."], ["X.....xxX...x.x."], ["X...x...x.x.X..."]]
def gen_bass_melodic(r, idx):
    minor = r.random() < 0.6
    q = "m" if minor else "M"
    third = 3 if minor else 4
    mode = r.choice(["aeolian", "dorian"] if minor else ["ionian", "mixolydian"])
    sc = [x for x in mel_notes(mode, -5, 16)]
    ct = [x for x in sc if x % 12 in ({0, third, 7} | ({10} if minor else set()))]
    nb = r.choice([2, 2, 4, 4, 1])
    rhy = [list(r.choice(BASS_RHY)[0]) for _ in range(2)]
    plan = r.choice(["ABAB'", "AA'BA", "ABAC", "AB"])
    evs = []; tech = {"旋律"}
    cur = 0
    for b in range(nb):
        c = plan[b] if b < len(plan) else "A"
        p = list(rhy[0] if c in "A" else rhy[1])
        if r.random() < 0.3:   # 休みを入れて歌わせる
            j = r.choice([6, 10, 12, 14]); p[j:j + 2] = ["-", "-"] if p[j] == "." else p[j:j + 2]
            for i in range(j, min(16, j + 3)):
                if p[i] == ".": p[i] = "-"
            tech.add("休み")
        hits = [i for i, ch in enumerate(p) if ch in "Xx"]
        bar_ev = []
        for n_, i in enumerate(hits):
            nxt = hits[n_ + 1] if n_ + 1 < len(hits) else 16
            stop = next((k for k in range(i + 1, nxt) if p[k] == "-"), nxt)
            d = (stop - i) * S16
            if i == 0: x = (0 if cur <= 8 else 12) if r.random() < 0.8 or b == 0 else min([third, 7, third + 12], key=lambda y: abs(y - cur))
            elif i == 8:
                near = [y for y in ct if 0 < abs(y - cur) <= 9]
                x = min(ct, key=lambda y: (abs(y - cur), r.random())) if r.random() < 0.6 or not near else r.choice(near)
            elif n_ == len(hits) - 1 and i >= 12 and r.random() < 0.5:
                # 次の小節の根音へ近づく（いまの音が高ければ、1オクターブ上の根音へ）
                if cur > 8: x = r.choice(["N+11", "N+13", "N+10"]); cur = 12
                else: x = r.choice(["N-1", "N+1", "N-2"]); cur = 0
                tech.add("アプローチ")
            else:
                k = min(range(len(sc)), key=lambda z: abs(sc[z] - cur))
                st = r.choice([1, -1, 1, 2, -2])
                if r.random() < 0.12 and cur <= 4: x = cur + 12; tech.add("オクターブ")
                else: x = sc[max(0, min(len(sc) - 1, k + st))]; tech.add("経過音")
            bar_ev.append(ev(b * BAR + i * S16, d, [x], "!" if i == 0 else ""))
            if isinstance(x, int): cur = x
        evs += bar_ev
    fits = ["m", "m7"] if minor else ["M", "maj7"]
    return bass_ph("旋律", f"旋律（{mode}）", nb, evs, tech, fits, f"bm{idx}")

def gen_bass_walk(r, idx):
    """4分音符で歩く。1拍目は根音（2小節目以降は3度・5度も）、2〜3拍目は和音と音階の音で順に動き、4拍目は次の根音へ近づく。
    いまの音が高ければ1オクターブ上の根音へ近づき、次の小節はそこから始める（跳びすぎない）"""
    q = r.choice(["m7", "7", "maj7", "m7", "7"])
    third = 3 if q == "m7" else 4
    sev = 10 if q in ("m7", "7") else 11
    LOW = [[0, 2, third, "A"], [0, third, 5, "A"], [0, third, 7, "A"], [0, 7, 5, "A"], [0, -2, -5, "A"], [0, 5, 7, "A"], [third, 5, 7, "A"], [7, 5, third, "A"], [0, 2, 0, "A"]]
    HIGH = [[12, sev, 7, "A"], [12, 7, 9, "A"], [7, 9, sev, "A"], [12, 14, 12, "A"], [0, third, 7, "A"], [7, sev, 12, "A"], [12, sev, 9, "A"]]
    nb = r.choice([2, 4, 4, 1])
    evs = []; tech = {"ウォーキング", "アプローチ"}
    hi = False
    for b in range(nb):
        line = list(r.choice(HIGH if hi else LOW))
        if b == 0 or (b % 2 == 0 and r.random() < 0.7): line[0] = 12 if hi else 0
        if line[0] not in (0, 12) and b == 0: line[0] = 0
        last = line[2]
        if last >= 7: line[3] = r.choice(["N+11", "N+13", "N+10", "N+7"]); hi = True
        else: line[3] = r.choice(["N-1", "N+1", "N-2", "N+2", "N-5"]); hi = False
        for k, x in enumerate(line):
            t = b * BAR + k * Q
            if k in (1, 3) and r.random() < 0.12:   # 3連のはね（2つ目は弱く）
                evs.append(ev(t, 8, [x], "")); evs.append(ev(t + 8, 4, [x], ","))
                tech.add("3連のはね")
            else:
                evs.append(ev(t, Q, [x], "!" if k == 0 else ""))
    fits = [q] + (["m"] if q == "m7" else ["M"] if q == "maj7" else [])
    return bass_ph("グルーヴ", f"ジャズのウォーキング（{q}）", nb, evs, tech, fits, f"bw{idx}", style="ジャズ")

FUNK16 = ["X..xo.x.X.g.x.o.", "X.gx..o.x.gX..x.", "X..g.xo..xg.X.o.", "X.x.go..X..xg.x.", "X...o.gxX.x..go.", "X.g.x.o.g.X.x..g", "Xg.x.oxg..x.X.g.", "X..xg.o.Xg..x.o."]
def gen_bass_funk(r, idx):
    use7 = r.random() < 0.5; use3 = r.random() < 0.3
    nb = r.choice([1, 2, 2, 4])
    pats = [list(r.choice(FUNK16)) for _ in range(2)]
    evs = []; tech = {"ファンク", "ゴースト", "オクターブ"}
    for b in range(nb):
        p = pats[0] if b % 2 == 0 or nb == 1 else pats[1]
        if b == nb - 1 and nb >= 2 and r.random() < 0.5: p = p[:8] + list(r.choice(FUNK16))[8:]
        hits = [i for i, c in enumerate(p) if c not in "."]
        for n_, i in enumerate(hits):
            c = p[i]; nxt = hits[n_ + 1] if n_ + 1 < len(hits) else 16
            d = min(nxt - i, 2) * S16
            if c == "X":
                mk = "!"
                if i == 0 and r.random() < 0.12: mk += "//@0.1"; tech.add("スライド")
                evs.append(ev(b * BAR + i * S16, d, [0], mk))
            elif c == "o": evs.append(ev(b * BAR + i * S16, S16, [12], ""))
            elif c == "g": evs.append(ev(b * BAR + i * S16, S16, ["x"], ",,"))
            else:
                x = r.choice([0, 7] + ([10] if use7 else []) + ([3] if use3 else []))
                evs.append(ev(b * BAR + i * S16, d, [x], ""))
    fits = (["m", "m7"] if use3 else (["m7", "7", "m"] if use7 else ["m", "m7", "M", "7", "5", "sus"]))
    return bass_ph("グルーヴ", "ファンク（16分）", nb, evs, tech, fits, f"bf{idx}", style="ファンク")

def bd_bar(r):
    kind = r.choice(["付点", "間", "非対称", "3連風", "ランダム"])
    if kind == "付点": hits = [0, 3, 6, 10, 12]
    elif kind == "間": hits = [0, 6] + ([10] if r.random() < 0.4 else [])
    elif kind == "非対称": hits = [0, 3, 6, 9, 12]
    elif kind == "3連風": hits = [0, 2, 4, 8, 10]
    else:
        hits = [0]
        while True:
            nx = hits[-1] + r.choice([2, 3, 3, 4, 5])
            if nx >= 14: break
            hits.append(nx)
    if r.random() < 0.3: hits = [h for h in hits if h != r.choice(hits[1:])] if len(hits) > 2 else hits
    return sorted(set(hits))

def gen_bass_breakdown(r, idx):
    nb = r.choice([2, 4, 4])
    bars = [bd_bar(r) for _ in range(2)]
    evs = []; kicks = []; tech = {"キックと一致", "休み"}
    diss = r.random() < 0.25
    for b in range(nb):
        hits = bars[b % 2] if not (b == nb - 1) else None
        if hits is None:   # 最後の小節: 前半だけ打って3〜4拍目は休み、4拍目の裏か無しで次へ
            hits = [h for h in bars[0] if h < 8]
            end_hit = r.choice([14, None, 12])
            if end_hit: hits = hits + [end_hit]
            tech.add("ため")
        k = ["."] * 16
        for n_, h in enumerate(hits):
            nxt = hits[n_ + 1] if n_ + 1 < len(hits) else (16 if b < nb - 1 or h >= 12 else 8)
            d = max(1, nxt - h - (1 if nxt - h >= 3 else 0)) * S16
            if b == nb - 1 and h < 8 and n_ == len([x for x in hits if x < 8]) - 1: d = min(d, (8 - h) * S16)
            x = 1 if (diss and h not in (0,) and n_ == 2 and b % 2 == 1) else 0
            if x == 1: tech.add("不協和")
            evs.append(ev(b * BAR + h * S16, d, [x], "!" if h in (0, 12, 14) else ""))
            k[h] = "X"
        kicks.append("".join(k))
    return bass_ph("ブレイクダウン", "ブレイクダウン（キックと一致）", nb, evs, tech, ["m", "m7", "M", "5", "sus", "7"], f"bd{idx}", kick=kicks, feelx="ハーフ")

PEDAL_T = ["X..x..x.X..x..x.", "X.x.X.x.X.x.X.x.", "X...x...X...x...", "X..x..x.x.x.x.x.", "X.x.x.x.X.x.x.xo", "X..x..x.X.x.x.o.", "X.......X...x.x.", "X..x..x...x.x.x.", "X.x.x...X.x.x...", "X...X..xX...X..o"]
def gen_bass_pedal(r, idx):
    """主音を保つベース（和音が変わっても低音は1小節目の根音のまま）。付点・オクターブ・休みで単調にしない"""
    nb = r.choice([2, 4, 4])
    pats = r.sample(PEDAL_T, 2)
    evs = []; tech = {"ペダル"}
    for b in range(nb):
        p = pats[0] if b % 2 == 0 else pats[1]
        if b == nb - 1 and r.random() < 0.5: p = p[:8] + r.choice(["X.......", "X...o...", "X..x..o.", "o.x.X..."])
        hits = [i for i, c in enumerate(p) if c != "."]
        for n_, i in enumerate(hits):
            nxt = hits[n_ + 1] if n_ + 1 < len(hits) else 16
            c = p[i]
            x = 12 if c == "o" else 0
            if c == "o": tech.add("オクターブ")
            evs.append(ev(b * BAR + i * S16, (nxt - i) * S16, [x], "!" if c == "X" else ""))
        if "X..x..x" in p: tech.add("付点")
    ph = bass_ph("ペダル", "ペダル（主音を保つ）", nb, evs, tech, NEUTRAL, f"bp{idx}")
    ph["rel"] = "first"
    return ph

# ═════════════════ 共通: 仕分け ═════════════════
def mk_phrase(inst, role, kind, nb, evs, tech, fits, mode, fam, pc=False):
    evs = sorted([e for e in evs if e[1] > 0], key=lambda e: e[0])
    return {"id": "", "inst": inst, "role": role, "kind": kind, "bars": nb, "rel": "bar", "ref": "low" if inst == "guitar" else "E1",
            "fits": fits, "scale": mode, "tech": sorted(tech), "pc": pc, "family": fam, "src": "gen", "ev": evs}

def stats(ph):
    beats = ph["bars"] * 4
    n = len(ph["ev"])
    acc = sum(1 for e in ph["ev"] if "!" in e[3]) / max(1, n)
    ivs = [x for e in ph["ev"] for x in e[2] if isinstance(x, int)]
    poly = sum(1 for e in ph["ev"] if len(e[2]) > 1) / max(1, n)
    sus = sum(e[1] for e in ph["ev"] if e[1] >= Q and "'" not in e[3]) / (beats * Q)
    rest = 1 - sum(e[1] for e in ph["ev"]) / (beats * Q)
    return dict(dens=n / beats, acc=acc, mean=(sum(ivs) / len(ivs)) if ivs else 0, poly=poly, sus=sus, rest=rest)

def classify(ph):
    s = stats(ph)
    ph["chug"] = chug_ratio(ph)
    ph["range"] = LP.iv_range(ph)
    role, tech = ph["role"], set(ph["tech"])
    raw = 0.45 * min(1, s["dens"] / 3.5) + 0.12 * s["acc"] + 0.2 * ph["chug"] + 0.1 * min(1, max(0, s["mean"]) / 24) + 0.13 * s["poly"] - 0.15 * s["rest"]
    if role == "バッキング": raw += 0.1 * s["sus"]
    ph["_raw"] = raw
    feel = "ふつう"
    if ph.get("feelx") == "ハーフ" or ("2拍3連" in tech and s["dens"] < 1.2) or (s["dens"] <= 0.6 and role in ("リフ",)): feel = "ハーフ"
    if s["dens"] >= 3.2: feel = "ダブル"
    ph.pop("feelx", None)
    ph["feel"] = feel
    first4 = any(is_ch for is_ch in (LP.is_chug(e) for e in ph["ev"] if e[0] < 48))
    sec = set()
    if role == "リフ":
        melodic = bool(tech & {"オクターブ", "ペダルトーン", "5のかたまり", "7のかたまり", "高い音"})
        kinds3 = len(tech & {"開放弦ペダル", "伸ばす", "オクターブ", "ペダルトーン", "スライド", "休み", "付点", "2拍3連", "5のかたまり", "7のかたまり", "不協和"}) >= 3
        if kinds3 and melodic and ph["chug"] <= 0.4: sec.add("看板リフ")
        if not first4 and ph["chug"] <= 0.15: sec.add("前奏")
        if ph["chug"] <= 0.7: sec.add("Aメロ")
        if "伸ばす" in tech and ph["chug"] <= 0.35: sec.add("Bメロ")
        if "不協和" in tech or "2拍3連" in tech or feel == "ハーフ": sec.add("ブリッジ" if ph["chug"] <= 0.3 else "ブレイクダウン")
        if ph["chug"] >= 0.25 and "休み" in tech: sec.add("ブレイクダウン")
        if ph["chug"] <= 0.15 and "伸ばす" in tech and s["sus"] >= 0.4: sec.add("サビ")
    elif role == "バッキング":
        sec |= {"サビ"}
        if s["sus"] >= 0.5: sec |= {"前奏", "Bメロ"}
        if s["dens"] <= 0.75: sec.add("ブリッジ")
        if "8分のストローク" in tech: sec.add("Aメロ")
    elif role == "アルペジオ":
        sec |= {"前奏", "Aメロ", "ブリッジ"}
        if s["dens"] >= 1.6: sec.add("Bメロ")
    elif role == "リード":
        sec |= {"前奏", "看板リフ", "サビ", "ブリッジ"}
    elif role == "根音":
        sec |= {"Aメロ", "Bメロ", "サビ"}
        if s["dens"] >= 2: sec.add("看板リフ")
    elif role == "ユニゾン":
        sec |= {"看板リフ", "Aメロ"}
        if ph.get("_g_intro"): sec.add("前奏")
        if "ブレイクダウン" in ph.get("_g_sec", []): sec.add("ブレイクダウン")
    elif role == "旋律":
        sec |= {"Aメロ", "Bメロ", "サビ", "ブリッジ"}
    elif role == "グルーヴ":
        sec |= {"Aメロ", "ブリッジ", "看板リフ"}
    elif role == "ブレイクダウン":
        sec |= {"ブレイクダウン"}
    elif role == "ペダル":
        sec |= {"Bメロ", "前奏", "ブリッジ"}
    if not sec: sec.add("Aメロ")
    ph["sections"] = sorted(sec, key=lambda x: ["前奏", "Aメロ", "Bメロ", "サビ", "看板リフ", "ブリッジ", "ブレイクダウン"].index(x))
    for k in ("_g_intro", "_g_sec"): ph.pop(k, None)

# ═════════════════ ふるい落とし（音楽として成り立たないもの）═════════════════
def melodic_line(ph):
    return [e for e in ph["ev"] if isinstance(e[2][0], int)]

def keep_musical(ph):
    """問題の理由（空なら残す）"""
    why = []
    evs = ph["ev"]
    if len(evs) < 2 and ph["role"] not in ("バッキング",): why.append("音が少なすぎる")
    line = [e[2][0] for e in melodic_line(ph)]
    durs = [e[1] for e in evs]
    if len(set(line)) <= 1 and ph["role"] not in ("ペダル", "ブレイクダウン", "根音", "バッキング", "ユニゾン") and not (ph["role"] == "リフ" and len({tuple(e[2]) for e in evs}) > 1):
        why.append("同じ音だけ")
    if len(set(line)) <= 1 and len(set(durs)) <= 1 and ph["role"] not in ("バッキング",):
        why.append("同じ音の連打だけ")
    if ph["role"] in ("リード", "旋律", "アルペジオ") and len(line) > 2:
        jumps = [abs(b - a) for a, b in zip(line, line[1:])]
        arp = ph["role"] == "アルペジオ"   # 分散和音は弦をまたぐので、跳躍の決まりを少しゆるめる（10度＝15半音まで・7半音以上が55%まで）
        if sum(1 for j in jumps if j >= 7) / len(jumps) > (0.55 if arp else 0.3): why.append("跳躍だらけ")
        if any(j > (15 if arp else 12) for j in jumps): why.append("オクターブより大きい跳躍")
        for a, b, c in zip(line, line[1:], line[2:]):
            if abs(b - a) >= 5 and abs(c - b) >= 5 and (b - a) * (c - b) > 0 and ph["role"] != "アルペジオ": why.append("同じ向きに2回跳ぶ"); break
    if ph["role"] in ("リード", "旋律"):
        # ピロピロ（トリル）: a-b-a-b を8分以下の短い音で
        es = melodic_line(ph)
        for w in zip(es, es[1:], es[2:], es[3:]):
            ps = [x[2][0] for x in w]
            if ps[0] == ps[2] and ps[1] == ps[3] and ps[0] != ps[1] and abs(ps[0] - ps[1]) <= 2 and all(x[1] <= 6 for x in w):
                why.append("ピロピロ（トリル）"); break
        if max(sum(1 for e in evs if b * BAR <= e[0] < (b + 1) * BAR) for b in range(ph["bars"])) > 12: why.append("音が多すぎる")
    if ph["role"] == "リード":
        rest = ph["bars"] * BAR - sum(durs)
        if rest < 6: why.append("息つぎがない")
        # 長い音（1拍以上）が強拍で和音にない（チョーキングは着いた音で見る）
        for e in evs:
            x = e[2][0]
            snd = x + (2 if "^^" in e[3] else 1 if "^" in e[3] else 0)
            if e[1] >= Q and e[0] % 24 == 0:
                q = "m" if any(f.startswith("m") for f in ph["fits"]) else "M"
                ok = {0, 3, 7, 10, 2, 5} if q == "m" else {0, 4, 7, 2, 9, 11}
                if snd % 12 not in ok: why.append("強拍の長い音が和音にない"); break
    if ph["role"] in ("リフ", "バッキング", "アルペジオ"):
        # 4小節で同じ1小節を4回そのまま
        if ph["bars"] == 4:
            bars = [json.dumps([[e[0] - b * BAR] + e[1:] for e in evs if b * BAR <= e[0] < (b + 1) * BAR]) for b in range(4)]
            if len(set(bars)) == 1: why.append("同じ小節を4回")
    if ph["role"] == "リフ":
        kinds = set(ph["tech"]) & {"開放弦ペダル", "伸ばす", "オクターブ", "ペダルトーン", "スライド", "休み", "付点", "2拍3連", "5のかたまり", "7のかたまり", "不協和", "高い音", "♭2"}
        if len(kinds) < 3: why.append("リフの素材が3種類未満")
        # 伸ばす音のすぐ後に刻み（間なし）
        for a, b in zip(evs, evs[1:]):
            if a[1] >= Q and "'" not in a[3] and LP.is_chug(b) and a[0] + a[1] == b[0]: why.append("伸ばした音をすぐミュート"); break
    if ph["inst"] == "bass":
        # 小節の頭（音があるとき）は根音（旋律・ペダル・ユニゾンは例外を少し認める）
        heads = [e for e in evs if e[0] % BAR == 0]
        if (ph["role"] in ("根音", "ブレイクダウン") or (ph["role"] == "グルーヴ" and "ウォーキング" not in ph["tech"])) and any(e[2][0] not in (0, 12, "x") for e in heads): why.append("小節の頭が根音でない")
        if ph["role"] == "旋律" and sum(1 for e in heads if e[2][0] in (0, 12)) < max(1, len(heads) // 2): why.append("根音に沿っていない")
    return why

def chord_fit_gs(ph, q):
    """実演の型: 音の長さの75%以上が和音と音階の音、強拍の長い音は和音の音か9度"""
    sc = {0, 2, 4, 5, 7, 9, 11, 10} if q == "maj" else {0, 2, 3, 5, 7, 8, 10, 9}
    ct = {0, 4, 7, 2, 9, 11} if q == "maj" else {0, 3, 7, 2, 10, 5}
    tot = sum(e[1] for e in ph["ev"]); good = sum(e[1] for e in ph["ev"] if all(x % 12 in sc for x in e[2]))
    if tot == 0 or good / tot < 0.75: return False
    for e in ph["ev"]:
        if e[1] >= Q and e[0] % 24 == 0 and e[2][-1] % 12 not in ct: return False
    return True

# ═════════════════ 実演（GuitarSet）→ ライブラリの形 ═════════════════
def from_guitarset(cells):
    gout, bout = [], []
    for c in cells:
        q = c["q"]
        fits = ["M", "maj7", "7"] if q == "maj" else ["m", "m7"]
        evs = [[e[0], e[1], e[2], e[3]] for e in c["ev"]]
        style = {"BN": "ボサノバ", "Funk": "ファンク", "Jazz": "ジャズ", "Rock": "ロック", "SS": "弾き語り"}[c["style"]]
        if c["gkind"] == "solo":
            role, kind = "リード", f"実演のリード（{style}）"
        else:
            mv = sum(len(e[2]) for e in evs) / max(1, len(evs))
            role, kind = ("バッキング", f"実演のバッキング（{style}）") if mv >= 2.2 else ("アルペジオ", f"実演のアルペジオ（{style}）")
        tech = {"実演"} | ({"3連"} if c["grid"] == 4 else set())
        if c["style"] == "Funk" and role == "バッキング": tech.add("カッティング")
        ph = mk_phrase("guitar", role, kind, c["bars"], evs, tech, fits, None, "gs:" + c["src"].split()[3] + c["gkind"])
        ph["ref"] = "E2"; ph["src"] = c["src"]; ph["style"] = style
        if role == "リード": ph["rel"] = "first"; ph["snapct"] = True
        if role == "リード":
            # 実演のリードは問いと答えの形ではないので、技だけ付ける
            line = [e[2][0] for e in evs]
            if any(b - a >= 5 for a, b in zip(line, line[1:])): ph["tech"] = sorted(set(ph["tech"]) | {"跳躍"})
        if chord_fit_gs(ph, q): gout.append(ph)
        # 低音（親指のベース）: いちばん低い音が根音・5度だけの型
        if c["gkind"] == "comp":
            low = [[e[0], e[1], [min(e[2])], e[3]] for e in evs]
            lows = [x[2][0] for x in low]
            if len(low) >= 2 and all(x % 12 in (0, 7) for x in lows) and low[0][0] == 0 and lows[0] % 12 == 0:
                for i in range(len(low) - 1): low[i][1] = low[i + 1][0] - low[i][0]
                low[-1][1] = c["bars"] * BAR - low[-1][0]
                # 同じ高さが続くものはつなぐ
                merged = []
                for e in low:
                    if merged and merged[-1][2] == e[2] and merged[-1][0] + merged[-1][1] == e[0] and e[0] % BAR != 0: merged[-1][1] += e[1]
                    else: merged.append(e)
                for e in merged:
                    e[2] = [e[2][0] - 12 if e[2][0] > 16 else e[2][0]]
                bph = mk_phrase("bass", "グルーヴ", f"実演の低音（{style}）", c["bars"], merged, {"実演", "根音と5度"}, ["m", "m7", "M", "maj7", "7", "5"], None, ph["family"])
                bph["ref"] = "E1"; bph["src"] = c["src"] + "（いちばん低い声部）"; bph["style"] = style
                if len(merged) >= 2: bout.append(bph)
    return gout, bout

# ═════════════════ まとめ ═════════════════
def build(gs_path=None, seed=20261022):
    r = random.Random(seed)
    rejected = collections.Counter()
    def run(gen, n, tries_mult=6):
        out = []
        for i in range(n * tries_mult):
            if len(out) >= n: break
            ph = gen(random.Random(r.randrange(10 ** 9)), i)
            out.append(ph)
        return out
    G = run(gen_riff, 900) + run(gen_backing, 420) + run(gen_arp, 380) + run(gen_lead, 460)
    B = run(gen_bass_root, 420) + run(gen_bass_melodic, 380) + run(gen_bass_walk, 200) + run(gen_bass_funk, 200) + run(gen_bass_breakdown, 170) + run(gen_bass_pedal, 120)
    gsG, gsB = [], []
    if gs_path and os.path.exists(gs_path):
        gsG, gsB = from_guitarset(json.load(open(gs_path)))
    def filt(lst, inst):
        seen = set(); out = []
        for ph in lst:
            classify(ph)
            why = check(ph, inst) + keep_musical(ph)
            if why:
                for w in set(why): rejected[(inst, ph["src"][:9], w)] += 1
                continue
            sg = signature(ph)
            if sg in seen: rejected[(inst, ph["src"][:9], "重複")] += 1; continue
            seen.add(sg); out.append(ph)
        return out
    G = filt(G, "guitar"); gsG = filt(gsG, "guitar")
    # ユニゾンのベース（できあがったギターのリフから）
    uni = []
    for g in G:
        if g["role"] != "リフ": continue
        u = LP.unison_bass(g)
        if len(u["ev"]) < 3: continue
        u.update({"id": "", "kind": "ユニゾン（ギターのリフと同じリズム）", "src": "gen", "unison_of": None, "_gid": g, "pc": False, "scale": g.get("scale"), "family": g["family"]})
        u["tech"] = sorted({"ユニゾン"} | ({"休み"} if "休み" in g["tech"] else set()) | ({"オクターブ"} if any(e[2][0] == 12 for e in u["ev"]) else set()))
        u["_g_intro"] = "前奏" in g["sections"]; u["_g_sec"] = g["sections"]
        uni.append(u)
    B = filt(B, "bass"); gsB = filt(gsB, "bass")
    uni_kept = []
    seen_u = set()
    for u in uni:
        g = u.pop("_gid")
        classify(u)
        why = check(u, "bass") + keep_musical(u)
        sg = signature(u)
        if why or sg in seen_u:
            for w in set(why or ["重複"]): rejected[("bass", "unison", w)] += 1
            continue
        seen_u.add(sg); u["_g"] = g; uni_kept.append(u)
    # 刻み中心（刻み 0.5 以上）の型は、ギター全体の15%以下に
    allG = G + gsG
    heavy = [p for p in allG if p["chug"] >= 0.5]
    limit = int(0.15 * len(allG))
    if len(heavy) > limit:
        drop = set(id(p) for p in heavy[limit:])
        rejected[("guitar", "gen", "刻み中心が多すぎる（15%まで）")] += len(drop)
        G = [p for p in G if id(p) not in drop]
    # 強さ（0〜1）: 役割ごとの順位
    def energy(lst):
        by = collections.defaultdict(list)
        for p in lst: by[p["role"]].append(p)
        for role, ps in by.items():
            ps.sort(key=lambda p: p["_raw"])
            for i, p in enumerate(ps):
                p["energy"] = round(i / max(1, len(ps) - 1), 3)
        for p in lst: p.pop("_raw", None)
    allG = G + gsG
    allB = B + uni_kept + gsB
    energy(allG); energy(allB)
    # id
    pref = {"リフ": "gr", "バッキング": "gb", "アルペジオ": "ga", "リード": "gl", "根音": "br", "ユニゾン": "bu", "旋律": "bm", "グルーヴ": "bg", "ブレイクダウン": "bd", "ペダル": "bp"}
    cnt = collections.Counter()
    for p in allG + allB:
        k = pref[p["role"]] + ("x" if p["src"].startswith("GuitarSet") else "")
        cnt[k] += 1; p["id"] = f"{k}{cnt[k]:04d}"
    for u in uni_kept:
        u["unison_of"] = u.pop("_g")["id"]
    order = ["id", "inst", "role", "kind", "sections", "energy", "feel", "chug", "bars", "fits", "scale", "range", "ref", "rel", "snapct", "tech", "pc", "style", "kick", "unison_of", "family", "src", "ev"]
    def tidy(p): return {k: p[k] for k in order if k in p and p[k] is not None}
    return [tidy(p) for p in allG], [tidy(p) for p in allB], rejected

def summary(lst):
    out = {}
    out["数"] = len(lst)
    out["出典"] = dict(collections.Counter("GuitarSet" if p["src"].startswith("GuitarSet") else "自作" for p in lst))
    out["役割"] = dict(collections.Counter(p["role"] for p in lst))
    out["区間"] = dict(collections.Counter(s for p in lst for s in p["sections"]))
    out["ノリ"] = dict(collections.Counter(p["feel"] for p in lst))
    out["小節"] = dict(collections.Counter(p["bars"] for p in lst))
    out["和音"] = dict(collections.Counter(f for p in lst for f in p["fits"]))
    out["技"] = dict(collections.Counter(t for p in lst for t in p["tech"]).most_common(25))
    ch = [p["chug"] for p in lst]
    out["刻み"] = {"0": sum(1 for c in ch if c == 0), "0〜0.25": sum(1 for c in ch if 0 < c <= 0.25), "0.25〜0.5": sum(1 for c in ch if 0.25 < c < 0.5), "0.5以上（刻み中心）": sum(1 for c in ch if c >= 0.5)}
    out["強さ"] = {f"{a/10:.1f}〜": sum(1 for p in lst if a / 10 <= p["energy"] < (a + 1) / 10 or (a == 9 and p["energy"] == 1)) for a in range(10)}
    return out

if __name__ == "__main__":
    gs = sys.argv[1] if len(sys.argv) > 1 else None
    G, B, rej = build(gs)
    meta = lambda inst: {"説明": "度数（根音からの半音）で書いたフレーズの型。読み方・使い方は docs/sound/guitar-bass-phrase-library.md と assets-src/ai-songs/_gen/loud25_phrases.py",
                         "時間": "1拍＝12刻み・1小節＝48刻み。ev＝[始まり, 長さ, 音（根音からの半音の並び）, 印]",
                         "出典": "自作（一般的な技法から生成。make_library.py）と GuitarSet（CC BY 4.0、Xi ほか 2018、https://zenodo.org/records/3371780。進行1・3のみ、根音からの半音とリズムだけ）",
                         "作成": "2026-10-22"}
    gp = os.path.join(ROOT, "assets-src", "guitar-phrases", "phrases.json")
    bp = os.path.join(ROOT, "assets-src", "bass-phrases", "phrases.json")
    os.makedirs(os.path.dirname(bp), exist_ok=True)
    def dump(path, inst, lst):
        with open(path, "w") as f:
            f.write("{\n" + ",\n".join(f' "{k}": {json.dumps(v, ensure_ascii=False)}' for k, v in meta(inst).items()) + ',\n "phrases": [\n')
            f.write(",\n".join("  " + json.dumps(p, ensure_ascii=False, separators=(",", ":")) for p in lst))
            f.write("\n ]\n}\n")
    dump(gp, "guitar", G); dump(bp, "bass", B)
    rep = {"ギター": summary(G), "ベース": summary(B), "ふるい落とし": {f"{k[0]}/{k[1]}/{k[2]}": v for k, v in sorted(rej.items(), key=lambda x: -x[1])}}
    json.dump(rep, open(os.path.join(HERE, "summary.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
