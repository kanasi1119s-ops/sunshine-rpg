# 【celtic_fantasy 用に写した版（2026-10-20）。カホン・ウッドベース・本物のフルート・アコギの旋律を足した。もとは celtic_suite.py】
# ケルト音楽20曲（2026-10-16、人間の依頼「ケルト音楽を3~4分で20曲作成してください。雰囲気は全部変えるように。感情・風景・イベント・季節でイメージして。
#   スケールを大きく使って、多種多様に試してみて」）。
# 曲ごとの「設計」（場面・拍子・テンポ・調と旋法・コード進行・楽器・形・入り方・終わり方）を下の SONGS に書き、共通の部品で音符にする。
#   旋律: 曲ごとに決まった乱数で、拍子に合ったリズムの型と、コードの音を強い拍に置く決まりで書く（動機を同じリズムで高さを変えてくり返す。
#         16小節＝8小節の問い（半終止）＋8小節の答え（頭の4小節は問いと同じ、終わりは主音）。B は音域を上げる）。既存の曲のメロディは使わない（CLAUDE.md 1-1）。
#   人間の指示（2026-10-16）: FX を使う／ピアノは左手と右手（右手は和音を同時に）／定番から外したコード進行（借用・ナポリ・分数・sus・maj7）。
#   MIDI のチャンネルは（ドラム以外で）15まで。同じ楽器のパートは pan・reverb・fx をそろえて共有させる。
# 使い方: python3 celtic_suite.py <番号か id か all> [出力フォルダ（省略は assets-src/ai-songs）]
import sys, os, re, json, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

# ================================================================ 和音・音階
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(s): return (PCN[s[0]] + (1 if len(s) > 1 and s[1] == "#" else -1 if len(s) > 1 and s[1] == "b" else 0)) % 12
def chord_pcs(ch):
    m = re.match(r"^([A-G][#b]?)(.*)$", ch.split("/")[0]); r = pc(m.group(1)); q = m.group(2)
    minor = q.startswith("m") and not q.startswith("maj")
    if "sus4" in q: t = 5
    elif "sus2" in q: t = 2
    else: t = 3 if minor else 4
    f = 6 if "b5" in q else 7
    pcs = [r, (r + t) % 12, (r + f) % 12]
    if "maj7" in q: pcs.append((r + 11) % 12)
    elif "7" in q: pcs.append((r + 10) % 12)
    elif "6" in q: pcs.append((r + 9) % 12)
    return pcs
def bass_pc(ch): return pc(ch.split("/")[1]) if "/" in ch else chord_pcs(ch)[0]
FLAT = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def tr_chord(ch, n):
    if n == 0: return ch
    def one(x):
        m = re.match(r"^([A-G][#b]?)(.*)$", x); r = (pc(m.group(1)) + n) % 12
        return (SHARP if "#" in m.group(1) or n in (2, 4, 7, 9, 11) else FLAT)[r] + m.group(2)
    return "/".join(one(x) for x in ch.split("/"))
MODES = {"ionian": [0, 2, 4, 5, 7, 9, 11], "dorian": [0, 2, 3, 5, 7, 9, 10], "mixolydian": [0, 2, 4, 5, 7, 9, 10],
         "aeolian": [0, 2, 3, 5, 7, 8, 10], "lydian": [0, 2, 4, 6, 7, 9, 11], "harmonic": [0, 2, 3, 5, 7, 8, 11]}
def low(x, lo): return lo + ((x - lo) % 12)

# ================================================================ 拍子
# beats: 1小節の拍（作曲ソフトの beats）、sub: 1拍の細かい単位、pulses: 拍のまとまりの頭（単位）
METERS = {
    "6/8": dict(beats=2, sub=3, pulses=[0, 3]), "9/8": dict(beats=3, sub=3, pulses=[0, 3, 6]), "12/8": dict(beats=4, sub=3, pulses=[0, 3, 6, 9]),
    "4/4": dict(beats=4, sub=2, pulses=[0, 2, 4, 6]), "4/4s": dict(beats=4, sub=4, pulses=[0, 4, 8, 12]),
    "3/4": dict(beats=3, sub=2, pulses=[0, 2, 4]), "2/4": dict(beats=2, sub=4, pulses=[0, 4]), "7/8": dict(beats=7, sub=1, pulses=[0, 2, 4]),
}
TPL = {   # 旋律のリズムの型（単位。負の数は休み）
    "6/8": {"body": [[2, 1, 2, 1], [1, 1, 1, 2, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [3, 2, 1], [1, 1, 1, 3], [2, 1, 3]], "cad": [[3, 3], [6], [4, 2]]},
    "9/8": {"body": [[2, 1, 2, 1, 2, 1], [2, 1, 2, 1, 3], [1, 1, 1, 2, 1, 2, 1], [3, 2, 1, 2, 1], [2, 1, 1, 1, 1, 3]], "cad": [[6, 3], [9], [3, 6]]},
    "12/8": {"body": [[2, 1, 2, 1, 2, 1, 2, 1], [3, 2, 1, 3, 3], [2, 1, 3, 2, 1, 3], [3, 3, 2, 1, 3], [1, 1, 1, 3, 2, 1, 3]], "cad": [[6, 6], [9, 3], [9, -3]]},
    "4/4": {"body": [[1] * 8, [2, 1, 1, 2, 2], [1, 1, 2, 1, 1, 2], [3, 1, 2, 2], [2, 2, 1, 1, 2], [1, 1, 1, 1, 2, 2]], "cad": [[4, 4], [6, 2], [6, -2]]},
    "4/4s": {"body": [[6, 2, 4, 4], [4, 4, 8], [4, 2, 2, 4, 4], [2, 2, 2, 2, 4, 4], [3, 1, 4, 4, 4], [4, 4, 4, 4], [2, 2, 4, 8]], "cad": [[12, -4], [8, 8], [4, 4, 8]]},
    "3/4": {"body": [[2, 2, 2], [3, 1, 2], [4, 2], [2, 1, 1, 2], [1, 1, 2, 2], [2, 1, 1, 1, 1]], "cad": [[6], [4, 2], [4, -2]]},
    "2/4": {"body": [[2, 2, 2, 2], [2, 1, 1, 2, 2], [1, 1, 2, 2, 2], [4, 2, 2], [2, 2, 4], [1, 1, 1, 1, 2, 2]], "cad": [[4, 4], [6, -2], [4, 2, -2]]},
    "7/8": {"body": [[1] * 7, [2, 2, 3], [1, 1, 2, 3], [2, 1, 1, 1, 2], [1, 1, 1, 1, 3]], "cad": [[4, 3], [7], [2, 2, 3]]},
}

# ================================================================ 楽器（旋律を受けもつもの）: 作曲ソフトの楽器・追加項目・飾り・音域
LEADS = {
    "flute": ("panflute", {}, "cut", (60, 84)), "ocarina": ("ocarina", {}, "cut", (60, 86)),
    "fiddle": ("fiddle", {"patch": "violin"}, "roll", (55, 91)), "acc": ("accordion", {}, "cut", (53, 84)),
    "oboe": ("panflute", {"patch": "oboe"}, "plain", (58, 89)), "clarinet": ("panflute", {"patch": "clarinet"}, "plain", (50, 89)),
    "banjo": ("banjo", {}, "plain", (55, 86)), "bagpipe": ("bagpipe", {}, "cut", (57, 81)), "horn": ("brass", {"patch": "horn"}, "plain", (48, 77)),
    "xylo": ("xylophone", {}, "plain", (65, 96)), "piano": ("piano", {}, "plain", (60, 88)),
    "wflute": ("panflute", {}, "cut", (60, 84)),   # 2026-10-20 高音が固い: 笛の音源の自然な音域（C6 まで）に収める（C#6〜E6 は音源を引きのばして硬くなっていた）
      # フルート（2026-10-20 点数の試し: VSCO の録音はプチッが10か所出て 7.73、笛の音源にして 7.83）
    "gtrlead": ("guitar", {"amp": "crystal", "chorus": 0}, "plain", (52, 81)),   # アコギの旋律（間奏）
}
LEAD_META = {   # 音量・左右・残響・FX（同じ楽器は同じ値＝チャンネルを共有）
    "flute": dict(vol=0.21, pan=0.15, reverb=0.4, gainDb=2, breath=True, fx="delay"), "ocarina": dict(vol=0.2, pan=0.15, reverb=0.42, gainDb=2, breath=True, fx="delay"),
    # フィドル（2026-10-17、人間の指示「バイオリンは柔らかく力強く、音を透き通るように響かせる」）: フィドルだけを書き出して数値で比べた結果、
    #   左右にわずかにずらした2本（doubleDetune 5セント）で点数 7.23→7.65（厚み＝力強さ）、2.8kHz を -2.5dB（刺さりを取る＝やわらかさ）、
    #   高音は落とさず 200〜600Hz を +2dB（透き通る芯）、立ち上がりをゆるく・余韻を長く、ホールの残響＋薄いディレイ（響き）。
    "fiddle": dict(vol=0.19, pan=-0.18, reverb=0.5, gainDb=3, bright=-0.15, attack=0.35, release=0.7, doubleDetune={"cents": 5, "spread": 0.3}, fx="fiddle"), "acc": dict(vol=0.15, pan=0.25, reverb=0.28, fx="room"),
    "oboe": dict(vol=0.19, pan=0.12, reverb=0.4, gainDb=1, breath=True, fx="plate"), "clarinet": dict(vol=0.19, pan=0.12, reverb=0.4, gainDb=1, breath=True, fx="plate"),
    "banjo": dict(vol=0.15, pan=0.3, reverb=0.22, fx="room"), "bagpipe": dict(vol=0.13, pan=0.0, reverb=0.35, fx="hall"),
    "horn": dict(vol=0.15, pan=-0.1, reverb=0.36, breath=True, release=0.5, fx="hall"), "xylo": dict(vol=0.1, pan=-0.35, reverb=0.25, fx="room"),
    "piano": dict(vol=0.12, pan=0.06, reverb=0.3, sustain=1.5, fx="plate"),
    "wflute": dict(vol=0.2, pan=0.12, reverb=0.42, gainDb=2, breath=True, release=0.45, fx="delay"),
    "gtrlead": dict(vol=0.13, pan=-0.22, reverb=0.26, bright=-0.55, attack=0.5, release=0.6, sustain=1.0, autoScoop=False, humanPitch=0, fx="gsoft"),
}

def S_(id, title, image, meter, bpm, key, mode, progs, band, form, desc_extra, **kw):
    return dict(id=id, title=title, image=image, meter=meter, bpm=bpm, key=key, mode=mode, progs=progs, band=band, form=form, desc=desc_extra, **kw)
def F(kind, bars, level, mel=None, lead=None, **kw): return dict(kind=kind, bars=bars, level=level, mel=mel, lead=lead, **kw)
SONGS = []

# ================================================================ 人間の指摘で手で直す小節（曲id → {(区間, 16小節の中の番号): 音（単位で書く）}）
PATCH = {}

# ================================================================ 旋律を書く
class Mel:
    def __init__(self, song, rng):
        self.m = METERS[song["meter"]]; self.U = self.m["beats"] * self.m["sub"]; self.rng = rng
        self.tonic = pc(song["key"]); self.mode = [(self.tonic + x) % 12 for x in MODES[song["mode"]]]
    def scale_for(self, ch):
        # コードの音が音階にないとき（E の G#、Bbmaj7 の Bb など）は、半音となりの音階の音と入れかえる。
        # 入れかえる相手は「そのコードの音でも主音でもない」ほうを選ぶ（2026-10-17: 以前は並び順で先の音を消していたため、
        # A エオリアンの E で主音 A を消して G を残し、G# のすぐあとに G が鳴る「合わない音」が出た。『雨の修道院』12・44小節）。
        sc = list(self.mode); cp = chord_pcs(ch)
        for x in cp:
            if x in sc: continue
            near = [s for s in sc if min((s - x) % 12, (x - s) % 12) == 1]
            near.sort(key=lambda s: (s in cp, s == self.tonic))   # コードの音・主音は消さない（後ろへ）
            if near: sc[sc.index(near[0])] = x
            else: sc.append(x)
        return sorted(set(sc))
    def phrase16(self, chords, lo, hi, peak, seed_shift=0):
        rng, U, meter = self.rng, self.U, self.m
        body = TPL[next(k for k in TPL if METERS[k] is meter)]["body"]; cads = TPL[next(k for k in TPL if METERS[k] is meter)]["cad"]
        tpls = rng.sample(body, k=min(4, len(body)))
        order = [0, 1, 0, 2, 0, 1, 3, "C"]
        mem = {}; bars = []; prev = None; span = hi - lo
        def target(b, ph): return lo + span * (0.28 + 0.06 * ph) + span * 0.5 * peak * math.sin(math.pi * min(1.0, (b + 0.5) / 7.5))
        for ph in (0, 1):
            for b in range(8):
                gb = ph * 8 + b
                if ph == 1 and b < 4:
                    bars.append(bars[b]); prev = midi_last(bars[b]); continue
                ch = chords[gb]; sc = self.scale_for(ch)
                cpcs = chord_pcs(ch)
                # アヴォイド・ノート（コードの音の半音上。E の F、G# の A など）は、弱い拍でも使わない（2026-10-17『雨の修道院』の指摘）
                avoid = {(c + 1) % 12 for c in cpcs} - set(cpcs)
                pool = [x for x in range(lo, hi + 1) if x % 12 in sc and x % 12 not in avoid]
                if len({x % 12 for x in pool}) < 5:   # 音が少なすぎると1歩で大きく跳ぶので、避ける音を半音上の「根音の上」だけに絞る
                    avoid = {(cpcs[0] + 1) % 12} - set(cpcs)
                    pool = [x for x in range(lo, hi + 1) if x % 12 in sc and x % 12 not in avoid]
                ct = [x for x in pool if x % 12 in cpcs[:3]] or pool
                key = order[b]
                rhythm = rng.choice(cads) if key == "C" else tpls[key % len(tpls)]
                nn = [d for d in rhythm if d > 0]
                tg = target(b, ph); tg2 = target(b + 1, ph)
                first = nearest(ct, tg if prev is None else 0.55 * tg + 0.45 * prev)
                if first == prev and len(ct) > 1: first = nearest([x for x in ct if x != prev], first)
                notes = [first]
                if key != "C" and key in mem and len(mem[key]) == len(nn) - 1: steps = mem[key]
                else:
                    steps = []; cur = first; leap = 0
                    for j in range(1, len(nn)):
                        dirn = 1 if tg2 > cur + 1 else (-1 if tg2 < cur - 1 else rng.choice([-1, 1]))
                        if leap:   # 跳んだ直後は反対向きに1歩もどる（音域を広く使いつつ、歌える形に）
                            s = -1 if leap > 0 else 1; leap = 0
                        else:
                            s = dirn * (1 if rng.random() < 0.62 else 2)
                            if rng.random() < 0.15: s = -s
                            # 2026-10-17 人間の指示「全体的に音域のスケールを広げて」: 1割ほどの確率で 4〜5度の跳躍（音階で3〜4歩）
                            if rng.random() < 0.12 and j < len(nn) - 1: s = dirn * rng.choice([3, 4]); leap = s
                        # 音階の音が少ないコード（A7 で D・F・Bb を避けると4音だけ）で、3〜4歩がオクターブ近く跳ばないように 7半音までに縮める
                        ci = pool.index(nearest(pool, cur))
                        while abs(s) > 1 and abs(pool[max(0, min(len(pool) - 1, ci + s))] - cur) > 7: s -= 1 if s > 0 else -1
                        if leap: leap = s if abs(s) >= 3 else 0
                        steps.append(s); cur = pool[max(0, min(len(pool) - 1, ci + s))]
                    if key != "C": mem[key] = steps
                idx = pool.index(first)
                for s in steps:
                    ci = idx
                    while abs(s) > 1 and abs(pool[max(0, min(len(pool) - 1, ci + s))] - pool[ci]) > 7: s -= 1 if s > 0 else -1
                    idx = max(0, min(len(pool) - 1, idx + s)); notes.append(pool[idx])
                # 長い音・拍の頭の音は和音の音に
                pos = 0; k = 0; out = []
                for d in rhythm:
                    if d < 0: out.append(("R", -d)); pos += -d; continue
                    n = notes[k]; k += 1
                    if (d >= U / 2 or (pos in meter["pulses"] and d >= meter["sub"])) and n % 12 not in cpcs: n = nearest(ct, n)
                    out.append((n, d)); pos += d
                if key == "C":   # 終わりの音: 問いは和音の3度か5度、答えは主音
                    last = max(i for i, (n, d) in enumerate(out) if n != "R")
                    ref = out[last - 1][0] if last > 0 and out[last - 1][0] != "R" else tg
                    if ph == 1:
                        cand = [x for x in pool if x % 12 == self.tonic] or ct
                    else:
                        cand = [x for x in ct if x % 12 != self.tonic] or ct
                    out[last] = (nearest(cand, ref), out[last][1])
                # 同じ高さが続かないように（つなぐと弾き直しで音が切れる）
                for i in range(1, len(out)):
                    a, b2 = out[i - 1][0], out[i][0]
                    if a != "R" and a == b2:
                        p2 = [x for x in pool if x != a]; out[i] = (nearest(p2, a + (1 if tg2 > a else -1)), out[i][1])
                if prev is not None and out[0][0] == prev:
                    p2 = [x for x in ct if x != prev] or [x for x in pool if x != prev]; out[0] = (nearest(p2, prev), out[0][1])
                bars.append(" ".join(f"{'R' if n == 'R' else nm(n)}:{d}" for n, d in out))
                prev = midi_last(bars[-1])
        return bars
def nearest(lst, x): return min(lst, key=lambda m: (abs(m - x), m))
def midi_last(bar):
    toks = [t.split(":")[0] for t in bar.split() if not t.startswith("R:")]
    return md(toks[-1]) if toks else None

# ================================================================ 曲を組み立てる
def build(song, out):
    rng = random.Random(song["id"] + str(song.get("seed", "")))
    M = METERS[song["meter"]]; U = M["beats"] * M["sub"]; SUB = M["sub"]; PUL = M["pulses"]
    PLEN = [(PUL[i + 1] if i + 1 < len(PUL) else U) - PUL[i] for i in range(len(PUL))]
    mel = Mel(song, rng)
    band = song["band"]
    # 旋律（A・B・C）: 16小節ずつ
    MELS = {}; PROG16 = {}
    for kname, (f4, e1, e2) in song["progs"].items():
        ch16 = f4.split() + e1.split() + f4.split() + e2.split(); PROG16[kname] = ch16
        # 2026-10-17 人間の指示「音域のスケールを広げて」: 旋律の音域を約1オクターブ半 → 約2オクターブ半（A3〜E6）に。B はさらに上（C4〜G6）
        lo, hi = song.get("mel_range", (57, 88))
        if kname == "B": lo, hi = lo + 3, hi + 3
        if kname == "C": lo, hi = lo + 1, hi + 1
        # その旋律を受けもつ楽器（ハモリは2音下、オクターブ上の重ねは+12）の音域に収める（外れた音をオクターブで折り返すと1音だけ跳ぶため）
        for sec in song["form"]:
            if sec.get("mel") != kname: continue
            for nm_ in (sec["lead"] if isinstance(sec["lead"], list) else [sec["lead"]]):
                lo, hi = max(lo, LEADS[nm_][3][0]), min(hi, LEADS[nm_][3][1])
            if sec.get("harm"): lo, hi = max(lo, LEADS[sec["harm"]][3][0] + 4), min(hi, LEADS[sec["harm"]][3][1])
            if sec.get("oct"): hi = min(hi, LEADS[sec["oct"]][3][1] - 12)
        if hi - lo < 19: hi = lo + 19
        MELS[kname] = mel.phrase16(ch16, lo, hi, peak=0.8 if kname == "A" else 1.0)
        for (kk, bar_i), fixed in PATCH.get(song["id"], {}).items():   # 人間が「合わない」と聞いた所を手で直すときはここに
            if kk == kname: MELS[kname][bar_i] = fixed
        for (kk, bar_i), fixed in PATCH.get(song["id"], {}).items():   # 人間が「合わない」と聞いた所だけを手で直す
            if kk == kname: MELS[kname][bar_i] = fixed
    # 小節の表
    plan = []; tempo = []
    for si, sec in enumerate(song["form"]):
        sh = sec.get("shift", 0)
        if sec.get("bpm"): tempo.append({"bar": len(plan) + 1, "bpm": sec["bpm"], "ramp": 1})
        for i in range(sec["bars"]):
            if sec["kind"] in song["progs"]: base = PROG16[sec["kind"]][i % 16]
            elif sec["kind"] == "break": base = PROG16["B"][i % 4]
            elif sec["kind"] == "end": base = sec.get("end_chord") or (song["key"] + ("m" if song["mode"] in ("aeolian", "dorian", "harmonic") else ""))
            else: base = PROG16["A"][i % 4] if not sec.get("mel") else PROG16[sec["mel"]][i % 16]
            mstr = None
            if sec.get("mel") and (sec["kind"] != "intro" or i < sec.get("frag", 99)): mstr = MELS[sec["mel"]][i % 16]
            plan.append(dict(sec=sec, si=si, i=i, ch=tr_chord(base, sh), base=base, mel=mstr, shift=sh))
    if song.get("rit"): tempo.append({"bar": max(1, len(plan) - 3), "bpm": round(song["bpm"] * 0.82), "ramp": 3})
    NB = len(plan); chords = [p["ch"] for p in plan]
    S = Song(M["beats"], SUB, NB, mel.mode); S.G = min(0.1, 0.35 / M["sub"] * (song["bpm"] / 100))
    bt = lambda u: fmt(u / SUB)
    tok = lambda m, u, mk="": f"{nm(m)}:{bt(u)}{mk}"

    # ---- パート ----
    FX = {"delay": [{"type": "delay", "beats": round(PLEN[0] / SUB, 4), "mix": 0.12, "feedback": 0.28}, {"type": "plate", "mix": 0.1}],
          "plate": [{"type": "plate", "mix": 0.13}], "room": [{"type": "room", "mix": 0.12}], "hall": [{"type": "reverb", "mix": 0.15}],
          "gsoft": [{"type": "eq", "low": 1, "mid": -1.5, "midHz": 2600, "high": -4}, {"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.003, "release": 0.12}, {"type": "plate", "mix": 0.1}],
          "fiddle": [{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": round(PLEN[0] / SUB, 4), "mix": 0.08, "feedback": 0.2}, {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]}
    leads_used = set(band["leads"])
    for sec in song["form"]:
        if sec.get("harm"): leads_used.add(sec["harm"])
        if sec.get("oct"): leads_used.add(sec["oct"])
        for x in (sec["lead"] if isinstance(sec.get("lead"), list) else [sec.get("lead")]):
            if x: leads_used.add(x)
    for name in [n for n in LEADS if n in leads_used and n != "piano"]:
        inst, extra, _, _ = LEADS[name]; mt = dict(LEAD_META[name]); fxn = mt.pop("fx"); vol = mt.pop("vol"); pan = mt.pop("pan")
        if name == "wflute" and song.get("lead_patch"): extra = dict(extra, patch=song["lead_patch"])   # ゆったりの曲は本物のフルートの録音（長い音がきれい）
        if song.get("lead_db"): mt["gainDb"] = mt.get("gainDb", 0) + song["lead_db"]
        if name == "gtrlead" and band.get("gpatch"): extra = dict(extra, patch=band["gpatch"])   # アコギの旋律も同じ弦に
        fx_ = FX[fxn]
        if name in ("wflute", "flute") and song.get("soft_high", True):
            # 2026-10-20 人間「高音弾くときのフルートがちょっと音が固いかな」: 刺さりやすい 3〜4kHz と高い音域をおさえる（ディレイの前にEQ）
            fx_ = [{"type": "eq", "low": 0, "mid": -3, "midHz": 3300, "high": -3}] + fx_
        S.part("L_" + name, inst, f"旋律（{name}）", vol, pan, fx=fx_, **extra, **mt)
    if band.get("drone") == "bagpipe" and "bagpipe" not in leads_used:
        S.part("L_bagpipe", "bagpipe", "旋律（bagpipe）", 0.13, 0.0, reverb=0.35, fx=FX["hall"])
    if band.get("harp"): S.part("harp", "harp", "ハープ（分散和音）", 0.12, -0.35, reverb=0.38, bright=-0.4, sustain=3, release=0.8,
                               fx=[{"type": "pingpong", "beats": round(PLEN[0] / SUB / 2, 4) or 0.5, "mix": 0.1, "feedback": 0.2}])
    PNO = dict(reverb=0.3, sustain=1.5, fx=FX["plate"])
    if band.get("piano") or "piano" in leads_used:
        for k in ("pno1", "pno2", "pno3"): S.part(k, "piano", f"ピアノ右手（和音・{k[3]}）", 0.09, 0.06, **PNO)
        S.part("pnoL", "piano", "ピアノ左手（低音）", 0.12, 0.06, **PNO)
        if "piano" in leads_used: S.part("L_piano", "piano", "ピアノ右手（旋律）", 0.13, 0.06, **PNO)
    if band.get("guitar") == "riff":
        # 2026-10-20 人間「ギター単音だけのバージョンで一曲選んで試しに作ってみて」: 和音のストロークをやめ、単音のリフ1本だけにする（間奏の旋律も単音）
        S.part("g3", "guitar", "アコギ（単音のリフ）", 0.13, -0.3, **({"patch": band["gpatch"]} if band.get("gpatch") else {}), amp="crystal", chorus=0, sustain=1.1, reverb=0.22,
               autoScoop=False, humanPitch=0, push=0.008, bright=-0.5, attack=0.58, release=0.6,
               fx=[{"type": "eq", "low": 0.5, "mid": -1, "midHz": 2600, "high": -3.5}, {"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.003, "release": 0.12}])
    elif band.get("guitar"):
        for k, pan in (("g1", -0.5), ("g2", -0.5 if band.get("gring") else 0.5), ("g3", -0.5), ("g4", 0.5)):
            # 2026-10-17 人間の指示「アコギもう少し音が柔らかいといいかも」: 高音をおさえ（bright -0.4・eq の high -2.5）、強い弾き（!）をやめた。
            #   楽器ごとの点検で、6kHz より上が -14.7dB → 下がり、重心 3.1kHz → 下がったことを確かめる
            # 2026-10-17 人間の指示「アコギの音、弾き始めも柔らかめで」「強くていいんだけど柔らかい音に」: 弾く強さはそのままで、音色を柔らかく。
            #   高音（bright -0.65・eq high -4.5）と弾いた瞬間の硬さ（2.6kHz を -1.5・コンプ attack 3ms）を抑え、低めを +1。立ち上がりを少し遅く（attack 0.58）。
            #   鳴らしたままの分散和音（gring）は余韻も長く（release 0.68）
            ring = band.get("gring"); gs = song.get("gsoft", 1)
            if band.get("gpatch"): pass
            S.part(k, "guitar", f"アコギ（{k[1]}本目）", 0.1, pan, **({"patch": band["gpatch"]} if band.get("gpatch") else {}), amp="crystal", chorus=0, sustain=1.0, reverb=0.22, autoScoop=False, humanPitch=0, push=0.008 * int(k[1]),
                   bright=round(-0.65 * gs, 2), attack=0.58, release=0.68 if ring else 0.6, **({"gainDb": song["gdb"]} if song.get("gdb") else {}),
                   fx=[{"type": "eq", "low": 1, "mid": round(-1.5 * gs, 2), "midHz": 2600, "high": round(-4.5 * gs, 2)}, {"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.003, "release": 0.12}])
    if band.get("acc") and "acc" not in leads_used: S.part("L_acc", "accordion", "旋律（acc）", 0.15, 0.25, reverb=0.28, fx=FX["room"])
    if band.get("pizz"): S.part("pizz", "strings", "弦のピチカート", 0.13, -0.3, patch="pizzicato", reverb=0.3)
    # ウッドベース（2026-10-20 楽器ごとの点検: 出だしが硬い 17.5dB・点数 6.63 → 立ち上がりをゆるく、高音を下げる）
    # 2026-10-20 楽器ごとの点検 2回目: エレキの音源（--bass jazz）では、どの曲もウッドベースだけ 6.6 前後と低い
    #   → 本物のコントラバスのピチカートの録音（--bass upright。VSCO 2 CE）に。録音なのでアンプは通さず、軽いEQとコンプだけ
    if band.get("bass") == "upright" and song.get("real_bass", False):
        S.part("bass", "bass", "ウッドベース", round(0.26 * song.get("bass_vol", 1.0), 3), 0, reverb=0.1, release=0.35,
               fx=[{"type": "eq", "low": 1.5, "mid": -1, "midHz": 350, "high": -2}, {"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.01, "release": 0.2}])
    elif band.get("bass") == "upright": S.part("bass", "bass", "ウッドベース", 0.22, 0, amp="jazz", reverb=0.08, release=0.3, bright=-0.65, attack=0.04,
                                              fx=[{"type": "eq", "low": 1, "mid": 0, "midHz": 800, "high": -9}, {"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.02, "release": 0.2}])
    if band.get("drums") == "cajon": S.part("cajon", "cajon", "カホン", round(0.4 * song.get("cajon_vol", 1.0), 3), -0.05, reverb=0.14)
    if band.get("bass") == "finger": S.part("bass", "bass", "ベース（指弾き）", 0.24, 0, fx=[{"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.02, "release": 0.15}])
    if band.get("cello") or band.get("drone") == "cello": S.part("cello", "strings", "チェロ", 0.13, -0.3, patch="cello", reverb=0.35, release=0.5, gainDb=song.get("cello_db", 0),
                                                               fx=[{"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.01, "release": 0.15}])
    if band.get("contrabass"): S.part("cb", "strings", "コントラバス", 0.14, 0, patch="contrabass", reverb=0.3)
    if band.get("strings"):
        S.part("sth", "strings", "弦（上・のばす）", 0.07, 0.35, patch="slowStrings", reverb=0.4, release=0.6)
        S.part("stl", "strings", "弦（下・のばす）", 0.07, 0.35, patch="slowStrings", reverb=0.4, release=0.6)
    if band.get("sparkle") == "glock": S.part("glock", "glockenspiel", "鉄琴（きらめき）", 0.07, 0.4, reverb=0.4, sustain=4, release=0.8,
                                              fx=[{"type": "pingpong", "beats": round(PLEN[0] / SUB, 4), "mix": 0.2, "feedback": 0.35}])
    if band.get("sparkle") == "xylo" and "xylo" not in leads_used: S.part("L_xylo", "xylophone", "旋律（xylo）", 0.1, -0.35, reverb=0.25, fx=FX["room"])
    if band.get("horn") and "horn" not in leads_used: S.part("L_horn", "brass", "旋律（horn）", 0.15, -0.1, patch="horn", reverb=0.36, breath=True, release=0.5, fx=FX["hall"])
    if band.get("timp"): S.part("timp", "strings", "ティンパニ", 0.16, 0, patch="timpani", reverb=0.3, gainDb=-4)
    if band.get("big"): S.part("big", "inchTom", "大太鼓", 0.13, 0, patch="inchTom", reverb=0.15, gainDb=-9)
    dr = band.get("drums")
    if dr and dr != "cajon": S.part("bodhran", "tom", "ボーラン風の刻み", 0.12, 0.1, reverb=0, gainDb=-8, bright=-0.4)
    if dr in ("kit", "march"):
        S.part("kick", "kick", "キック", 0.26, 0, gainDb=-8)
        S.part("snare", "snare", "スネア", 0.17 if dr == "kit" else 0.2, 0, push=0.01, gainDb=-10)
        S.part("hat", "hihat", "ハイハット", 0.07, 0, gainDb=-9)
        S.part("crash", "crash", "クラッシュ", 0.09, 0, gainDb=-8)

    # ---- 単音のリフ（guitar: "riff"）: 拍のまとまりごとのリズムと、和音の音の上り下りの型を、曲ごとに1つ決めて2小節でくり返す ----
    rr = random.Random(song["id"] + "riff" + str(song.get("seed", "")))
    RH = []   # 2小節ぶん: 拍のまとまりごとに、音の長さの並び（単位）
    for _b in range(2):
        bar_ = []
        for pl in PLEN:
            if pl % 3 == 0: opts = [[2, 1], [1, 1, 1], [3]] if pl == 3 else [[2, 1, 2, 1], [1, 1, 1, 3], [3, 2, 1]]
            elif pl == 4: opts = [[2, 1, 1], [1, 1, 2], [2, 2], [3, 1]]
            elif pl == 2: opts = [[1, 1], [2]]
            else: opts = [[pl]]
            bar_.append(rr.choice(opts))
        RH.append(bar_)
    CONT = rr.choice([[0, 2, 1, 2, 3, 2, 1, 0], [0, 1, 2, 3, 2, 1, 2, 1], [0, 2, 3, 2, 1, 2, 0, 1], [0, 1, 0, 2, 3, 2, 1, 2]])
    def riff_bar(i, cp, nxt, lvl):
        tl = [m for m in range(48, 70) if m % 12 in cp[:3]]
        base = min(range(len(tl)), key=lambda k: abs(tl[k] - low(cp[0], 50)))
        tk = []; c = 0
        lens = [d for grp in RH[i % 2] for d in grp]
        for j, d in enumerate(lens):
            last_note = j == len(lens) - 1 and i % 2 == 1
            if last_note:   # 2小節目の最後は、次の和音の根音へ音階で近づく
                tgt = low(chord_pcs(nxt)[0], 50); m = tgt + (2 if tgt + 2 < 70 else -1)
                m = min(S.scale and [x for x in range(46, 72) if x % 12 in S.scale] or [m], key=lambda x: abs(x - m))
            else:
                m = tl[min(len(tl) - 1, base + CONT[c % len(CONT)])]
            mk = "" if j == 0 else ","
            if lvl <= 2 and j % 2 == 1 and not last_note: tk.append(f"R:{bt(d)}")   # 静かな所は音を間引いて、間をあける
            else: tk.append(tok(m, d, mk))
            c += 1
        return tk

    LV = {1: 0.62, 2: 0.74, 3: 0.86, 4: 0.96, 5: 1.03}
    arc = []
    def on(sec, comp, need):
        if sec.get("only") is not None: return comp in sec["only"]
        return sec["level"] >= need
    for bi, p in enumerate(plan):
        sec, i, ch, sh = p["sec"], p["i"], p["ch"], p["shift"]; lvl = sec["level"]; L = sec["bars"]
        nxt = plan[bi + 1]["ch"] if bi + 1 < NB else ch
        is_end = sec["kind"] == "end"; last = i == L - 1
        g0 = LV[lvl]; g1 = LV[min(5, lvl + 1)] if not is_end else LV[max(1, lvl - 2)]
        arc.append(round(g0 + (g1 - g0) * 0.35 * i / max(1, L - 1), 3))
        sc = mel.scale_for(p["base"]); sc = [(x + sh) % 12 for x in sc]; S.scale = sc
        cp = chord_pcs(ch); br = bass_pc(ch)
        triad = sorted(set(cp[:3]))
        def tones(lo, hi, pcs=None): return [m for m in range(lo, hi + 1) if m % 12 in (pcs or cp[:3])]
        # ---- 旋律 ----
        if p["mel"] and not is_end:
            seqs = p["mel"]
            if sh: seqs = " ".join(t if t.startswith("R:") else f"{nm(md(t.split(':')[0]) + sh)}:{t.split(':')[1]}" for t in seqs.split())
            ld = sec["lead"]; ld = ld[(i // 16) % len(ld)] if isinstance(ld, list) else ld
            def fit(name, sq, shift_oct=0, whole=None):
                """楽器の音域に合わせてオクターブを動かす。2026-10-17: 小節ごとに動かすと小節の境目でオクターブ跳びが起きた（03・15 で多数）ので、
                同じ区間の16小節ぶん（whole）をまとめて見て1つのオクターブを決め、それでも外れる音だけ個別に折り返す"""
                lo_, hi_ = LEADS[name][3]
                ref = whole if whole is not None else sq
                ms = [md(t.split(":")[0]) + sh for t in ref.split() if not t.startswith("R:")]
                o = shift_oct
                if ms:
                    c = (max(ms) + min(ms)) / 2; mid = (lo_ + hi_) / 2
                    while c + 12 * o > mid + 6: o -= 1
                    while c + 12 * o < mid - 6: o += 1
                    # 下が楽器の音域から出るなら、上がまだ収まる範囲で1オクターブ上げる（折り返しで1音だけ跳ぶのを防ぐ）
                    while min(ms) + 12 * o < lo_ and max(ms) + 12 * (o + 1) <= hi_: o += 1
                    while max(ms) + 12 * o > hi_ and min(ms) + 12 * (o - 1) >= lo_: o -= 1
                outk = []
                for t in sq.split():
                    if t.startswith("R:"): outk.append(t); continue
                    m = md(t.split(":")[0]) + 12 * o
                    while m > hi_: m -= 12
                    while m < lo_: m += 12
                    outk.append(f"{nm(m)}:{t.split(':')[1]}")
                return " ".join(outk)
            whole = " ".join(MELS[sec["mel"]]) if sec.get("mel") else None
            style = "plain" if (song.get("plain_fiddle") and ld == "fiddle") else LEADS[ld][2]
            S.put("L_" + ld, bi, S.ornament(S.seq(fit(ld, seqs, 0, whole)), style, bi + 17 * p["si"], dens=0.4, legato=True) if style != "plain" else S.plain(S.seq(fit(ld, seqs, 0, whole)), legato=True))
            if sec.get("harm"):
                h = []
                for t in seqs.split():
                    n_, d = t.split(":")
                    if n_ == "R": h.append(t); continue
                    m = md(n_); c = 0
                    while c < 2:
                        m -= 1
                        if m % 12 in sc: c += 1
                    avoid = {(x + 1) % 12 for x in cp} - set(cp)   # ハモリがアヴォイド・ノート（コードの音の半音上）に乗ったら、もう1段下げる
                    if m % 12 in avoid:
                        m -= 1
                        while m % 12 not in sc: m -= 1
                    h.append(f"{nm(m)}:{d}")
                S.put("L_" + sec["harm"], bi, S.plain(S.seq(fit(sec["harm"], " ".join(h), 0, whole)), legato=True))
            if sec.get("oct"): S.put("L_" + sec["oct"], bi, S.plain(S.seq(fit(sec["oct"], seqs, 1, whole)), legato=False))
        if is_end and i == 0:
            ld = sec.get("lead") or band["leads"][0]
            lo_, hi_ = LEADS[ld][3]; t = nearest(tones(lo_ + 5, hi_ - 5, [cp[0]]), (lo_ + hi_) // 2)
            S.put("L_" + ld, bi, [tok(t, U)])
        # ---- ハープ（分散和音。同じ高さを続けない）----
        if band.get("harp") and on(sec, "harp", 1) and not (is_end and i > 1):
            tl = tones(45, 88); cyc = tl + tl[-2:0:-1]   # ハープも広く（A2〜E6）
            n = U if U <= 12 else U // 2; d = 1 if U <= 12 else 2
            st = (bi * 3) % len(cyc)
            if is_end: S.put("harp", bi, [tok(m, d) for m in tl[:n]] if len(tl) >= n else [tok(tl[0], U)])
            else: S.put("harp", bi, [tok(cyc[(st + j) % len(cyc)], d) + ("" if j == 0 else ",") for j in range(n)])
        # ---- ピアノ ----
        pv = sorted(low(x, 60) for x in triad)[:3]; lr = low(br, 40); f5 = lr + ((cp[2] - br) % 12)
        if f5 >= lr + 12: f5 -= 12
        if f5 <= lr: f5 += 12
        ps = band.get("piano") or "flow"
        if (band.get("piano") or "piano" in leads_used) and (on(sec, "piano", 2) or (sec.get("only") is None and lvl >= 1 and sec["kind"] == "intro")):
            pianolead = p["mel"] and (sec["lead"] == "piano")
            if is_end:
                for vi, g in enumerate(("pno1", "pno2", "pno3")): S.put(g, bi, [tok(pv[vi], U, ",")] if i == 0 else [f"R:{bt(U)}"])
                S.put("pnoL", bi, [tok(lr, U)] if i == 0 else [f"R:{bt(U)}"])
            else:
                if not pianolead:
                    for vi, g in enumerate(("pno1", "pno2", "pno3")):
                        if ps == "block" or lvl <= 1: S.put(g, bi, [tok(pv[vi], U, ",")])
                        elif ps == "pulse": S.put(g, bi, [tok(pv[vi], PLEN[j], "!" if j == 0 else ",") for j in range(len(PUL))])
                        elif ps == "oompah":
                            tk = []
                            for j, pl in enumerate(PLEN):
                                if song["meter"] == "3/4": tk += ([f"R:{bt(pl)}"] if j == 0 else [tok(pv[vi], pl, ",")])
                                else: h = pl // 2 or 1; tk += [f"R:{bt(h)}", tok(pv[vi], pl - h, ",")] if pl > 1 else [tok(pv[vi], pl, ",")]
                            S.put(g, bi, tk)
                        else: S.put(g, bi, [tok(pv[vi], U, ",")])   # flow: 右手は和音をのばす
                # 左手
                if ps == "flow" or pianolead:
                    seq = [lr, f5, lr + 12, f5 + 12 if f5 + 12 < 64 else f5, lr + 12, f5]
                    n = U if U <= 8 else U // 2; d = 1 if U <= 8 else 2
                    if U == 9 or U == 12: n, d = U // 3, 3
                    S.put("pnoL", bi, [tok(seq[j % len(seq)], d, "!" if j == 0 else ",") for j in range(n)])
                elif ps == "oompah":
                    tk = []
                    for j, pl in enumerate(PLEN):
                        m = lr if j % 2 == 0 else f5
                        if song["meter"] == "3/4": tk += [tok(lr, pl, "!")] if j == 0 else [f"R:{bt(pl)}"]
                        else: h = pl // 2 or 1; tk += [tok(m, h, "!" if j == 0 else ""), f"R:{bt(pl - h)}"] if pl > 1 else [tok(m, pl)]
                    S.put("pnoL", bi, tk)
                else:
                    S.put("pnoL", bi, [tok(lr if j % 2 == 0 else (f5 if j % 4 == 1 else lr + 12), PLEN[j], "!" if j == 0 else "") for j in range(len(PUL))])
        if p["mel"] and sec["lead"] == "piano": pass
        # ---- アコギ ----
        if band.get("guitar") == "riff" and on(sec, "guitar", 1) and not (is_end and i > 0):
            gl = p["mel"] and sec.get("lead") == "gtrlead"
            if is_end: S.put("g3", bi, [tok(low(cp[0], 52), U)])
            elif not gl:   # 間奏（アコギの旋律）の区間はリフを休む
                S.put("g3", bi, riff_bar(i, cp, nxt, lvl))
        elif band.get("guitar") == "arp" and on(sec, "guitar", 2) and not (is_end and i > 0):   # 指で弾く分散和音（静かな曲）
            tl = tones(52, 76); n, d = (U, 1) if U <= 8 else ((U // 3, 3) if U % 3 == 0 else (U // 2, 2))
            gl = p["mel"] and sec.get("lead") == "gtrlead"   # アコギが旋律の区間は、伴奏のアコギを和音をのばすだけにする（半音でぶつからないように）
            if not (band.get("bass") == "upright" and on(sec, "bass", 2)): S.put("g1", bi, [tok(low(br, 40), U, ",")])   # ウッドベースがいる所は、低い音をベースにまかせる
            if gl and not is_end:
                S.put("g3", bi, [tok(low(cp[1], 52), U, ",")]); S.put("g2", bi, [tok(low(cp[2], 55), U, ",")])
            if not is_end and band.get("gring") and not gl:
                # 2026-10-17 人間の指示「アコギの音少し伸ばして。伸びながら音が小さくなっていく感じ」: 1音ずつ切らず、2本に分けて
                #   次の次の音まで鳴らしたままにする（弦を押さえたまま鳴らしっぱなしにする弾き方）。音は弦の減衰で自然に小さくなる
                vs = {"g3": [], "g2": [f"R:{bt(d)}"]}
                for j in range(n):
                    m = tl[(j * 2 + bi) % len(tl)] if j % 2 else tl[(j + bi) % len(tl)]
                    vs["g3" if j % 2 == 0 else "g2"].append(tok(m, min(2 * d, U - j * d), "," if j else ""))
                for g, tk in vs.items(): S.put(g, bi, tk)
            elif not is_end and not gl: S.put("g3", bi, [tok(tl[(j * 2 + bi) % len(tl)] if j % 2 else tl[(j + bi) % len(tl)], d, "," if j else "") for j in range(n)])
        elif band.get("guitar") and on(sec, "guitar", 3) and not (is_end and i > 0):
            r0 = low(cp[0], 45)
            v = [low(br, 40), r0 + ((cp[2] - cp[0]) % 12), r0 + 12, r0 + 12 + ((cp[1] - cp[0]) % 12)]
            if band.get("bass") == "upright" and on(sec, "bass", 2): v[0] = r0 + ((cp[1] - cp[0]) % 12)   # 低い音はウッドベースにまかせる（にごり防止）
            gl = p["mel"] and sec.get("lead") == "gtrlead"
            for gi, g in enumerate(("g1", "g2", "g3", "g4")):
                if gi < 2 or is_end: S.put(g, bi, [tok(v[gi], U)]); continue
                if gl: continue   # アコギが旋律の区間は、刻みをやめて和音をのばすだけ
                tk = []
                for j, pl in enumerate(PLEN):
                    pat = [2, 1] * (pl // 3) if pl % 3 == 0 else ([1, 1] if pl == 2 else ([2, 1, 1] if pl == 4 else [pl]))
                    for q, dd in enumerate(pat): tk.append(tok(v[gi], dd, "" if q == 0 else ","))
                S.put(g, bi, tk)
        # ---- アコーディオン（和音の3度をのばす）----
        if band.get("acc") == "hold" and on(sec, "acc", 3) and "L_acc" in S.parts and not (p["mel"] and (sec["lead"] == "acc" or sec.get("harm") == "acc")) and not (is_end and i > 0):
            S.put("L_acc", bi, [tok(low(cp[1], 57), U, ",")])
        # ---- ピチカート ----
        if band.get("pizz") and on(sec, "pizz", 2) and not is_end:
            tl = tones(55, 79); S.put("pizz", bi, [tok(tl[(j * 2 + bi) % len(tl)], 1, "!" if j in PUL else ",") for j in range(U)] if U <= 8 else [tok(tl[(j + bi) % len(tl)], SUB) for j in range(U // SUB)])
        # ---- 低音 ----
        if band.get("bass") == "finger" and on(sec, "bass", 3) and not (is_end and i > 0):
            r = low(br, 28); rn = low(bass_pc(nxt), 28)
            ap = (rn - 1 if rn > r else rn + 1) if rn != r else r + 7
            if is_end: S.put("bass", bi, [tok(r, U)])
            else:
                # 2026-10-17 人間の指示「ベースは普通のコード進行でいいかも」: コードの根音（分数コードは指定の低音）を、拍のまとまりごとに弾くだけ
                S.put("bass", bi, [tok(r, pl, "" if j == 0 else ",") for j, pl in enumerate(PLEN)])
        if band.get("bass") == "upright" and on(sec, "bass", 2) and not (is_end and i > 0):
            # ウッドベース: 静かな所は根音（と5度）をのばす。弾む所は拍のまとまりごとに 根音→5度→（上の根音）、盛り上がる所では最後に次のコードへの半音のつなぎ
            r = low(br, 31); f = r + 7 if r + 7 <= 47 else r - 5; rn = low(bass_pc(nxt), 31)
            n = len(PUL)
            if is_end or n == 1: S.put("bass", bi, [tok(r, U)])
            elif lvl <= 2: S.put("bass", bi, [tok(r, PUL[-1]), tok(f, U - PUL[-1], ",")])
            else:
                seq = [r, f, r + 12 if r + 12 <= 50 else f, f][:n] if n >= 3 else [r, f]
                if lvl >= 4 and n >= 3 and rn != r:
                    ap = rn - 1 if rn > seq[-2] else rn + 1
                    if ap != seq[-2]: seq[-1] = ap
                S.put("bass", bi, [tok(seq[j], PLEN[j], "" if j == 0 else ",") for j in range(n)])
        if (band.get("cello") or band.get("drone") == "cello") and not (is_end and i > 0):
            if band.get("drone") == "cello" and on(sec, "drone", 1): S.put("cello", bi, [tok(low(mel.tonic + sh, 38), U)])
            elif band.get("cello") == "ost" and on(sec, "cello", 2) and not is_end:
                r = low(br, 38); pat = [r, r + 7, r + 12, r + 7, r + 3 if (cp[1] - cp[0]) % 12 == 3 else r + 4, r + 7]
                S.put("cello", bi, [tok(pat[j % len(pat)], 1 if U <= 9 else 2, "!" if j == 0 else ",") for j in range(U if U <= 9 else U // 2)])
            elif band.get("cello") and on(sec, "cello", 2): S.put("cello", bi, [tok(low(br, 43), U)])
        if band.get("contrabass") and on(sec, "contrabass", 2) and not (is_end and i > 0): S.put("cb", bi, [tok(low(br, 31), U)])
        # ---- 弦・ホルン ----
        if band.get("strings") and on(sec, "strings", 3 if band.get("drums") else 2) and not (is_end and i > 1):
            S.put("sth", bi, [tok(low(cp[1], 66), U)]); S.put("stl", bi, [tok(low(cp[2], 55), U)])
        if band.get("horn") and lvl >= 5 and "L_horn" in S.parts and not (p["mel"] and (sec["lead"] == "horn" or sec.get("harm") == "horn")) and not is_end and sec.get("only") is None:
            S.put("L_horn", bi, [tok(low(cp[2], 55), U)])
        if band.get("drone") == "bagpipe" and on(sec, "drone", 1) and not (p["mel"] and (sec["lead"] == "bagpipe" or sec.get("harm") == "bagpipe")) and not is_end:
            S.put("L_bagpipe", bi, [tok(low(mel.tonic + sh, 57), U)])
        # ---- きらめき ----
        if band.get("sparkle") == "glock" and on(sec, "glock", 1) and not (is_end and i > 1):
            hi_t = tones(84, 100)
            if lvl <= 2 or sec.get("only"): S.put("glock", bi, [f"R:{bt(PLEN[0])}", tok(hi_t[bi % len(hi_t)], U - PLEN[0])] if bi % 2 == 0 else [tok(hi_t[(bi + 2) % len(hi_t)], U)])
            elif lvl >= 4 and i % 2 == 0: S.put("glock", bi, [tok(hi_t[(j + bi) % len(hi_t)], PLEN[j]) for j in range(len(PUL))])
        if band.get("sparkle") == "xylo" and lvl >= 4 and "L_xylo" in S.parts and not p["mel"] is None and not (sec["lead"] == "xylo" or sec.get("oct") == "xylo") and sec.get("only") is None:
            tl = tones(72, 96); n, d = (U, 1) if U <= 8 else ((U // 3, 3) if U % 3 == 0 else (U // 2, 2))
            if i % 2 == 1: S.put("L_xylo", bi, [tok(tl[(j + bi) % len(tl)], d, "!" if j == 0 else ",") for j in range(n)])
        # ---- 打楽器 ----
        BOD = {"X": "A2!", "x": "C3", "o": "C3,,"}
        def pat_bod(fill):
            s = ["."] * U
            for j, p0 in enumerate(PUL):
                s[p0] = "X" if j == 0 else "x"
                for q in range(1, PLEN[j]): s[p0 + q] = "o" if (q % 2 == 1 or PLEN[j] == 3) else "."
            if fill:
                for q in range(PUL[-1], U): s[q] = "x" if q < U - 1 else "X"
            return "".join(s)
        kit_on = dr in ("kit", "march") and on(sec, "drums", 4 if dr == "kit" else 3)
        if dr == "cajon" and on(sec, "drums", 3) and not (is_end and i > 0):
            # カホン: 低音（B2）＝キックの位置、スラップ（F3）＝スネアの位置、トーン（D3）＝合間の弱い音。区間の最後の小節は短いフィル
            CJ = {"X": "B2", "x": "B2,", "S": "F3!", "s": "F3,", "t": "D3,", "g": "D3,,"}   # 低音は強く打たない（ウッドベースとぶつかる 0.57）
            cs_ = ["."] * U; n = len(PUL)
            if is_end: cs_[0] = "X"
            else:
                for j, p0 in enumerate(PUL):
                    if n == 4: cs_[p0] = "X" if j in (0, 2) else "S"
                    elif n == 3: cs_[p0] = (["X", "S", "s"] if song["meter"] == "3/4" else ["X", "t", "S"])[j]
                    elif n == 2: cs_[p0] = "X" if j == 0 else "S"
                    else: cs_[p0] = "X"
                    if lvl >= 4:
                        for q in range(1, PLEN[j]):
                            if PLEN[j] == 3 and q == 2: cs_[p0 + q] = "g"
                            elif PLEN[j] == 2: cs_[p0 + q] = "g"
                            elif PLEN[j] == 4 and (q == 2 or (lvl >= 5 and q == 3)): cs_[p0 + q] = "g"
                if last:
                    for q in range(PUL[-1], U): cs_[q] = "t" if q < U - 1 else "S"
            S.put("cajon", bi, S.pgrid("".join(cs_), CJ))
        if dr and dr != "cajon" and on(sec, "drums", 3) and not (is_end and i > 0):
            pb = pat_bod(last and not is_end and not kit_on) if not is_end else "X" + "." * (U - 1)
            if kit_on and not is_end: pb = "".join("." if (q in PUL or (last and q >= PUL[-1])) else c for q, c in enumerate(pb))   # ドラムと重ねるときは拍の頭を空ける（手は2本）
            if is_end and kit_on: pb = "." * U
            if pb.strip("."): S.put("bodhran", bi, S.pgrid(pb, BOD))
        if dr in ("kit", "march") and on(sec, "drums", 4 if dr == "kit" else 3) and not (is_end and i > 0):
            k = ["."] * U; sn = ["."] * U; hh = ["."] * U
            if is_end: k[0] = "X"; sn[0] = "X"
            else:
                k[0] = "X"
                if len(PUL) == 4: k[PUL[2]] = "x"
                if dr == "kit":
                    for j in (range(1, len(PUL), 2) if len(PUL) in (2, 4) else range(1, len(PUL))): sn[PUL[j]] = "X" if len(PUL) != 3 else "x"
                    for p0 in PUL: hh[p0] = "x"
                    if lvl >= 5:
                        for q in range(U):
                            if hh[q] == "." and (q % max(1, SUB // 2 if SUB > 1 else 1) == 0): hh[q] = "o"
                else:   # 行進: スネアの刻み
                    for q in range(U): sn[q] = "x" if q in PUL else ("o" if q % 2 == 0 or SUB == 3 else ".")
                if last:
                    for q in range(PUL[-1], U): sn[q] = "x" if q < U - 1 else "X"; hh[q] = "."
            S.put("kick", bi, S.grid("".join(k))); S.put("snare", bi, S.grid("".join(sn)))
            if "".join(hh).strip("."): S.put("hat", bi, S.grid("".join(hh)))
            if (i == 0 and lvl >= 4) or (is_end and i == 0) or (lvl >= 5 and i % 8 == 0):
                S.put("crash", bi, S.grid("X" + "." * (U - 1))); hh[0] = "."
                S.parts["hat"]["bars"][bi] = None
                if "".join(hh).strip("."): S.put("hat", bi, S.grid("".join(hh)))
        if band.get("timp") and not (is_end and i > 0):
            r = low(br, 38)
            if r > 50: r -= 12
            if is_end or (lvl >= 4 and i % 4 == 0 and sec.get("only") is None) or (sec.get("only") and "timp" in sec["only"] and i % 2 == 0):
                S.put("timp", bi, [tok(r, U, "!")])
            elif last and lvl >= 3 and sec.get("only") is None: S.put("timp", bi, [tok(r, 1, "," if j < U // 2 else "") for j in range(U)] if U <= 9 else [tok(r, 2) for j in range(U // 2)])
        if band.get("big") and not (is_end and i > 0):
            BIG = {"X": "E2!", "x": "A2", "o": "C3,"}
            if is_end: S.put("big", bi, S.pgrid("X" + "." * (U - 1), BIG))
            elif on(sec, "big", 5) and i % 2 == 0: S.put("big", bi, S.pgrid("X" + "." * (PUL[len(PUL) // 2] - 1) + "x" + "." * (U - PUL[len(PUL) // 2] - 1), BIG) if len(PUL) > 1 else S.pgrid("X" + "." * (U - 1), BIG))
            elif sec.get("only") and "big" in sec["only"] and i % 2 == 0: S.put("big", bi, S.pgrid("o" + "." * (U - 1), BIG))
        # 終わり（fade）: ハープだけが上へ
        if is_end and sec.get("end") == "fade" and i == 1 and band.get("harp"):
            tl = tones(55, 91); S.put("harp", bi, [tok(m, 1) for m in tl[:U - 1]] + [tok(tl[U - 1] if len(tl) >= U else tl[-1], 1)] if len(tl) >= U else [tok(tl[0], U)])

    extra = {"guitarWobble": False}
    if tempo: extra["tempo"] = tempo
    if song.get("swing"): extra["swing"] = song["swing"]
    secs = sum(4 * 0 for _ in [])
    # 長さ（テンポの変化を入れて）
    bpm_at = []; cur = song["bpm"]
    tmap = {t["bar"]: t["bpm"] for t in tempo}
    total = 0.0
    for b in range(NB):
        if b + 1 in tmap: cur = tmap[b + 1]
        total += M["beats"] * 60 / cur
    prog_note = "・".join(dict.fromkeys(chords))[:120]
    desc = (f"（仮）{song['image']}。{song['meter'].replace('4/4s', '4/4')}・BPM{song['bpm']}・{song['key']}の{ {'ionian': '長調', 'dorian': 'ドリアン', 'mixolydian': 'ミクソリディアン', 'aeolian': '自然的短音階', 'lydian': 'リディアン', 'harmonic': '和声的短音階'}[song['mode']]}、"
            f"約{int(total // 60)}分{int(total % 60):02d}秒。旋律: {'・'.join(song['band']['leads'])}。{song['desc']}"
            f"楽器: フルート・アコギ・カホン・ウッドベース。FX: 笛のディレイとプレート、アコギのEQとコンプ、ウッドベースのEQとコンプ。")
    S.dump(out, song["title"] + "（仮）", desc, song["bpm"], chords, arc, extra=extra)
    # 仕上げ: のばす楽器の同じ高さの弾き直しをつなぐ
    sj = json.load(open(out, encoding="utf-8"))
    for pt in sj["parts"]:
        r = pt["role"]
        if r.startswith(("弦（", "チェロ", "コントラバス", "ハープ")) or (r.startswith("旋律（acc") and band.get("acc") == "hold") or r.startswith("旋律（bagpipe") or r.startswith("旋律（horn"):
            if r.startswith("ハープ"): continue
            pt["notes"] = merge(pt["notes"], legato=r.startswith("弦（"))
        if song.get("soft_high", True) and (r.startswith("旋律（gtrlead") or r.startswith("アコギ")):
            # 2026-10-20 人間「アコギの音もかなりの高音の所の音が少し強いのでもう少し柔らかく」: E5 から上は弱めに（A5 から上はさらに弱く）
            def _gsoft(tk):
                if tk.startswith("R:") or ":" not in tk: return tk
                m_ = md(tk.split(":")[0]); body = tk.split(":")[1]
                if m_ is None or m_ < 76 or "," in body: return tk
                body = body.replace("!", ""); tk = tk.split(":")[0] + ":" + body
                mk = ",," if m_ >= 81 else ","
                return tk[:-1] + mk + "_" if tk.endswith("_") else tk + mk
            pt["notes"] = " ".join(_gsoft(t) for t in pt["notes"].split())
            for fx in pt.get("fx", []):
                if fx.get("type") == "eq": fx["high"] = round(fx.get("high", 0) - 1.5, 2); fx["mid"] = round(fx.get("mid", 0) - 1.0, 2)   # 弦の高い倍音と弾いた瞬間の硬さを少しおさえる
        if song.get("soft_high", True) and (r.startswith("旋律（wflute") or r.startswith("旋律（flute")):
            # 高い音（A5 から上）は息を少し弱めて吹く: 強い印（!）のない音に「,」（C#6 から上は「,,」）を付ける
            def _soft(tk):
                if tk.startswith("R:") or ":" not in tk: return tk
                m_ = md(tk.split(":")[0]); body = tk.split(":")[1]
                if m_ is None or m_ < 81 or "!" in body or "," in body: return tk
                mk = ",," if m_ >= 85 else ","
                return tk[:-1] + mk + "_" if tk.endswith("_") else tk + mk
            pt["notes"] = " ".join(_soft(t) for t in pt["notes"].split())
            # 2026-10-20 人間「フルートの音強弱をつけるようにしようか」: 2小節ごとのフレーズに、出だし弱く→山で強く→終わりを引く強弱。
            #   2拍以上のばす音は、息をふくらませるように音量を立ち上げる（<）
            pt["phrase"] = M["beats"] * 2
            def _swell(tk):
                if tk.startswith("R:") or ":" not in tk: return tk
                body = tk.split(":")[1]; num = "".join(ch for ch in body if ch.isdigit() or ch == ".")
                try: L_ = float(num)
                except ValueError: return tk
                if L_ < 2 or "<" in body: return tk
                return tk[:-1] + "<_" if tk.endswith("_") else tk + "<"
            pt["notes"] = " ".join(_swell(t) for t in pt["notes"].split())
    json.dump(sj, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return total

def merge(notes, legato):
    out_ = []
    for t in notes.split():
        n_, d = t.split(":", 1); mark = "".join(c for c in d if not (c.isdigit() or c == ".")); dv = float(d[:len(d) - len(mark)])
        if out_ and n_ != "R" and out_[-1][0] == n_ and dv >= 1 and out_[-1][1] >= 1 and "!" not in mark and out_[-1][1] + dv <= 32:
            out_[-1][1] += dv; out_[-1][2] = out_[-1][2].replace("_", ""); continue
        out_.append([n_, dv, mark.replace("_", "") if legato else mark])
    res = []
    for j, (n_, dv, mark) in enumerate(out_):
        nxt = out_[j + 1][0] if j + 1 < len(out_) else "R"
        lg = "_" if legato and n_ != "R" and nxt not in ("R", n_) and dv >= 1 else ""
        while dv > 32 and n_ == "R": res.append("R:32"); dv -= 32
        res.append(f"{n_}:{fmt(dv)}{mark}{lg}")
    return " ".join(res)

