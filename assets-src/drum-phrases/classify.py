# ドラムのフレーズ（16分の格子の8小節）の仕分け（2026-10-22）。extract_gmd.py と make_loud.py が使う。
# 付けるもの: energy（強さ 0〜1）・feel（normal／half／double／shuffle）・fills（フィルの位置と種類）・ghost（ゴーストの量）・
#            cymbals（使うシンバル）・uses_ride・uses_toms・density（1小節あたりの音数）
import collections

TOMS = "1234ABCD"
def tom_n(ch): return "1234".index(ch) if ch in "1234" else "ABCD".index(ch)
STRONG = {"X": 1.0, "x": 0.72, "o": 0.32, "O": 0.9}
CYMV = lambda ch: 1.0 if ch.isupper() else 0.75

def hits(bar):
    return sum(1 for k in "kshtc" for ch in bar[k] if ch != ".")

def timekeeper(bar, a, b):
    """[a,b) のマスで、時を刻む手の音（ハイハットの x X O・ライド・クラッシュで刻む小節のクラッシュ）がいくつ鳴るか。
    o（弱いハット）はペダルの足のことが多いので数えない"""
    ride_crash = sum(1 for ch in bar["c"] if ch in "cCgGnN") >= 3
    return sum(1 for i in range(a, b) if bar["h"][i] in "xXO" or bar["c"][i] in "rRuU" or (ride_crash and bar["c"][i] in "cCgGnN"))

def _cnt(bar, k, a, b, chars): return sum(1 for i in range(a, b) if bar[k][i] in chars)

def groove_profile(bars):
    """拍ごとの、ふだんの音数（8小節の中央値）。グルーヴの一部のタム・スネアをフィルとまちがえないため"""
    import statistics
    prof = []
    for j in range(4):
        a, b = j * 4, j * 4 + 4
        prof.append(dict(t=statistics.median(_cnt(x, "t", a, b, TOMS) for x in bars),
                         s=statistics.median(_cnt(x, "s", a, b, "xX") for x in bars),
                         k=statistics.median(_cnt(x, "k", a, b, "xXo") for x in bars),
                         tk=statistics.median(timekeeper(x, a, b) for x in bars)))
    return prof

def fill_beats(bars, bi, prof):
    """bi 小節目の拍ごとに「フィルらしさ」を見る。prof＝groove_profile（拍ごとのふだんの音数）"""
    bar = bars[bi]; out = []
    for j in range(4):
        a, b = j * 4, j * 4 + 4; g = prof[j]
        tk = timekeeper(bar, a, b)
        tom = _cnt(bar, "t", a, b, TOMS); sn = _cnt(bar, "s", a, b, "xX"); kc = _cnt(bar, "k", a, b, "xXo")
        allh = sum(1 for k in "kshtc" for i in range(a, b) if bar[k][i] != ".")
        drop = g["tk"] >= 1 and tk == 0          # ふだん刻んでいる手が止まった
        f = None
        if tom - g["t"] >= 2 or (tom > g["t"] and drop): f = "tom"
        elif drop:
            if sn - g["s"] >= 2: f = "snare"
            elif kc - g["k"] >= 2: f = "kick"
            elif allh == 0: f = "gap"
            elif any(bar["c"][i] in "cCgGnNsS" for i in range(a, b)): f = "hit"
            elif sn + kc >= 1: f = "break"
        elif sn - g["s"] >= 3: f = "snare"
        out.append(f)
    return out

def fill_kind(bars, bi, beats, swing_trip):
    """フィルの拍の並びから種類を決める（いちばん目立つもの）"""
    bar = bars[bi]; a = beats[0] * 4; b = beats[-1] * 4 + 4
    seg = {k: bar[k][a:b] for k in "kshtc"}
    toms = [tom_n(c) for c in seg["t"] if c in TOMS]
    kinds = []
    if len(toms) >= 3:
        down = sum(1 for x, y in zip(toms, toms[1:]) if y >= x); up = sum(1 for x, y in zip(toms, toms[1:]) if y < x)
        kinds.append("タム下り" if down >= up * 2 else ("タム上り" if up > down * 2 else "タム回し"))
    elif len(toms) >= 1: kinds.append("タム一打")
    run = mx = 0
    for c in seg["s"]:
        run = run + 1 if c != "." else 0; mx = max(mx, run)
    if mx >= 4 or sum(1 for c in seg["s"] if c != ".") >= 6: kinds.append("スネア連打")
    run = mxk = 0
    for c in seg["k"]:
        run = run + 1 if c != "." else 0; mxk = max(mxk, run)
    if mxk >= 3: kinds.append("キック連打")
    if swing_trip: kinds.append("3連")
    if any(c in "cCgGnNsS" for c in seg["c"]) and sum(1 for c in seg["s"] + seg["k"] if c != ".") <= 6 and not toms: kinds.append("一撃")
    empty = 0; mxe = 0
    for i in range(a, b):
        if all(bar[k][i] == "." for k in "kshtc"): empty += 1; mxe = max(mxe, empty)
        else: empty = 0
    if mxe >= 3: kinds.append("間")
    if not kinds:
        if sum(1 for c in seg["s"] if c == "o") >= 2: kinds.append("ゴースト")
        else: kinds.append("変化")
    return kinds

def classify(ph):
    bars = ph["bars"]; n = len(bars)
    # 拍ごとに、ハイハット・ライドで時を刻んでいる小節の割合
    prof = groove_profile(bars)
    trip_bars = set(ph.get("trip_bars", []))
    fills = []
    for bi in range(n):
        fb = fill_beats(bars, bi, prof)
        # 小節の終わりから続くフィルの拍（途中の1拍だけのものも記録）
        j = 3; run = []
        while j >= 0 and fb[j]: run.insert(0, j); j -= 1
        if not run:
            # 小節の途中のタム（フィルではなくグルーヴの一部の場合もある）
            continue
        if len(run) == 4 and bi > 0 and all(f == "gap" for f in fb): kinds = ["間"]
        else: kinds = fill_kind(bars, bi, run, bi in trip_bars)
        fills.append(dict(bar=bi + 1, beats=len(run), kind=kinds[0], kinds=kinds))
    # 強さ: ベロシティの段の平均（打ったマスの強さ）と音数
    vs = []; dens = 0
    for b in bars:
        for k in "ksh":
            for ch in b[k]:
                if ch != ".": vs.append(STRONG.get(ch, 0.72))
        for ch in b["t"]:
            if ch != ".": vs.append(1.0 if ch in "ABCD" else 0.72)
        for ch in b["c"]:
            if ch != ".": vs.append(CYMV(ch))
        dens += hits(b)
    dens /= n; mv = sum(vs) / max(1, len(vs))
    # テンポも少し足す（同じ音数でも速いほど激しい）
    bpm = ph.get("bpm", 120)
    e = 0.45 * min(1, max(0, (mv - 0.45) / 0.45)) + 0.4 * min(1, dens / 36) + 0.15 * min(1, max(0, (bpm - 70) / 130))
    crash = sum(1 for b in bars for ch in b["c"] if ch in "cCgGnNsS")
    e = min(1.0, e + 0.02 * min(5, crash))
    e = min(1.0, max(0.0, (e - 0.15) / 0.6))   # GMD 全体で 0〜1 に広がるように伸ばす
    # ノリ
    s4 = s8 = soff = 0; nb = 0
    fill_bars = {f["bar"] for f in fills if f["beats"] >= 2}
    for bi, b in enumerate(bars):
        if bi + 1 in fill_bars: continue
        nb += 1; s = b["s"]
        s4 += (s[4] in "xX") + (s[12] in "xX"); s8 += s[8] in "xX"
        soff += sum(1 for i in (2, 6, 10, 14) if s[i] in "xX")
    nb = max(1, nb)
    feel = "normal"
    if ph.get("swing", 0.5) >= 0.6: feel = "shuffle"
    elif soff / nb >= 2.5 and s4 / nb < 1: feel = "double"          # 裏拍ごとのスネア（2ビート・スカンク）
    elif s8 / nb >= 0.6 and s4 / nb <= 0.5: feel = "half"
    elif sum(1 for b in bars for i in (0, 4, 8, 12) if b["s"][i] in "xX") / nb >= 3.5: feel = "double"   # 毎拍スネア（4つ打ちのスネア）
    ghost = sum(1 for b in bars for ch in b["s"] if ch == "o") / n
    cy = collections.Counter()
    for b in bars:
        if any(c in "xXoO" for c in b["h"]): cy["hihat"] += 1
        if "O" in b["h"]: cy["open"] += 1
        for ch in b["c"]:
            if ch in "rR": cy["ride"] += 1
            elif ch in "uU": cy["bell"] += 1
            elif ch in "cCgG": cy["crash"] += 1
            elif ch in "nN": cy["china"] += 1
            elif ch in "sS": cy["splash"] += 1
    main = [k for k in ("hihat", "ride", "bell", "crash", "china", "splash") if cy[k] >= (2 if k in ("hihat", "ride") else 1)]
    if cy["open"]: main.append("open")
    toms = sum(1 for b in bars for ch in b["t"] if ch != ".")
    ph.update(energy=round(e, 3), feel=feel, fills=fills, ghost=round(ghost, 2), cymbals=main,
              uses_ride=cy["ride"] + cy["bell"] >= 4, uses_toms=toms >= 2, toms=toms, density=round(dens, 1))
    ph.pop("trip_bars", None)
    return ph
