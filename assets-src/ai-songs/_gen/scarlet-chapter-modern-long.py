# 『緋色の断章（現代版・6分）』（仮）: 「緋色の断章（空間版・6分）」の旋律・コード・構成（258小節・BPM172・嬰ハ短調）をそのままに、
# いまの作曲ソフトで、きれいで現代的な音に作り変えた版（2026-10-15、人間の指示「現代音楽版の音で作り変えて。長い方の曲で」）。
# 変えたこと:
#  - 旋律: Aメロ・Bメロ・ブリッジ・最後の空間部はグランドピアノ、サビ・ギターソロはリードギター（warm-lead-b。ビブラート・チョーキング・しゃくりなし）。
#    サビは FM ベルを重ねてきらめかせる。前の版の「半音ずつ上げるチョーキングの代わり」は使わない（banned-sounds 11・17）。
#  - 伴奏: 16分のピアノの分散和音、左右の歪みギター（刻み）、左右の弦、サビの厚いシンセ（unisonSaw）、空間部のパッド。
#  - タッピングの部分は、ピアノの速いソロに置きかえた（32分のギターは「ピロピロ」に近いため）。スラップのベースソロは指で弾くベースのソロに。
#  - ドラム: 生ドラム（--drums jpop）。セクションごとに型を変え、ライド・低いタム（E3・C3・A2）・ゴースト・フィル・止めを入れる。シンバルは鳴らしきる。
# 構成（258小節・6分）: イントロ8 → Aメロ8 → Bメロ8 → サビ8 → Aメロ8 → Bメロ8 → サビ8 → ギターソロ40 → ブリッジ16 →
#   ピアノソロ40 → ベースソロ32 → ドラムソロ16 → せり上げ8 → サビ8 → サビ8 → 空間16 → 消えていく16 → 終わり2
# 使い方: python3 scarlet-chapter-modern-long.py <出力.json>
# 書き出し: node tools/composer/song.mjs build assets-src/ai-songs/scarlet-chapter-modern-long.json --wav --edition modern
#   --drums jpop --bass pick --piano salamander --orchestra vsco --guitar emily --master-preset jpop-band
import json, sys

def fmt(x): return ("%.4f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
def md(n):
    i = 2 if len(n) > 2 and n[1] == "#" else 1
    return N.index(n[:i]) + 12 * (int(n[i:]) + 1)

NAT = {1, 3, 4, 6, 8, 9, 11}   # 嬰ハ短調（自然的）
HAR = {1, 3, 4, 6, 8, 9, 0}    # 和声的（G#7 の上）
def scale_for(ch): return HAR if ch == "G#7" else NAT
def step(m, k, pcs):
    d = 1 if k > 0 else -1
    for _ in range(abs(k)):
        m += d
        while m % 12 not in pcs: m += d
    return m
def snap(m, pcs):
    while m % 12 not in pcs: m -= 1
    return m

PROG = {"intro": "C#m C#m A B", "A": "C#m C#m A B C#m C#m F#m G#7", "B": "A B G#m E A B G#m G#7",
        "CH": "A B G#m F#m A B E G#7", "SOLO": "C#m A F#m G#7 C#m A B G#7", "BR": "F#m E G#m A F#m E B B"}
PLAN = [("intro", "intro", 2), ("A", "A", 1), ("B", "B", 1), ("CH", "CH", 1), ("A", "A", 1), ("B", "B", 1), ("CH", "CH", 1),
        ("gsolo", "SOLO", 5), ("bridge", "BR", 2), ("psolo", "SOLO", 5), ("bsolo", "SOLO", 4), ("dsolo", "intro", 4),
        ("build", "BR", 1), ("F1", "CH", 1), ("F2", "CH", 1), ("space", "CH", 2), ("fade", "intro", 4), ("end", None, 0)]
bars, occ = [], {}
for kind, prog, rep in PLAN:
    cs = PROG[prog].split() * rep if prog else ["C#m", "C#m"]
    k = occ.get(kind, 0); occ[kind] = k + 1
    for i, c in enumerate(cs): bars.append(dict(kind=kind, chord=c, i=i, n=len(cs), k=k))
NB = len(bars)
assert NB == 258, NB

TONES = {"C#m": ["C#4", "E4", "G#4"], "A": ["A3", "C#4", "E4"], "B": ["B3", "D#4", "F#4"], "G#m": ["G#3", "B3", "D#4"],
         "F#m": ["F#3", "A3", "C#4"], "E": ["E3", "G#3", "B3"], "G#7": ["G#3", "C4", "D#4"]}
PCS = {c: sorted({md(x) % 12 for x in t}) for c, t in TONES.items()}
FIFTH = {"C#m": "G#4", "A": "E5", "B": "F#5", "G#m": "D#5", "F#m": "C#5", "E": "B4", "G#7": "D#5"}
def root_in(ch, lo): return lo + ((md(TONES[ch][0]) - lo) % 12)
def tones_from(ch, lo):
    pcs = [md(x) % 12 for x in TONES[ch]]; r = pcs[0]; base = lo + ((r - lo) % 12)
    return sorted(base + o + ((p - r) % 12) for o in (0, 12) for p in pcs)
def voicing(ch, center):
    pcs = [md(x) % 12 for x in TONES[ch]]; best = None
    for inv in range(3):
        o = pcs[inv:] + pcs[:inv]; cur = center - 7; v = []
        for p in o:
            x = cur + ((p - cur) % 12); v.append(x); cur = x + 1
        sc = abs(sum(v) / 3 - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]

# ---- 旋律（もとの曲と同じ）----
LEAD = {
    "A": "G#5:1 E5:0.5 G#5:0.5 B5:1.5 A5:0.5 G#5:2 F#5:1 E5:1 E5:1 A5:1 C#6:1.5 B5:0.5 D#6:2 B5:1 F#5:1 G#5:1 E5:0.5 G#5:0.5 B5:1 C#6:1 B5:1.5 G#5:0.5 E5:2 F#5:1 A5:1 C#6:1 A5:1 F#5:1 D#5:1 B4:1 G#4:1",
    "B": "C#6:1 B5:0.5 A5:0.5 E5:2 D#6:1 C#6:0.5 B5:0.5 F#5:2 B5:1 G#5:1 D#6:2 E6:1.5 B5:0.5 G#5:2 A5:1 C#6:1 E6:2 D#6:1 B5:1 F#5:2 C#6:2 B5:1 C#6:1 B5:1 D#6:1 B5:1 G#5:1",
    "CH": "E6:2 C#6:1 E6:1 D#6:2 B5:1 F#5:1 B5:1.5 D#6:0.5 B5:1 G#5:1 A5:1 C#6:1 E6:2 E6:1 C#6:1 A5:2 F#5:1 B5:1 D#6:1 B5:1 G#5:1 B5:1 E6:2 D#6:1.5 B5:0.5 G#5:1 F#5:1",
}
def parse(s): return [(t.rsplit(":", 1)[0], float(t.rsplit(":", 1)[1])) for t in s.split()]
def mel_bar(which, i, shift=0):
    ev = parse(LEAD[which]); start, acc, out = (i % 8) * 4, 0.0, []
    for n, d in ev:
        lo, hi = max(acc, start), min(acc + d, start + 4)
        if hi > lo: out.append(f"{nm(md(n) + shift)}:{fmt(hi - lo)}")
        acc += d
    return out

# ---- 小節ごとに書く入れもの ----
PARTS = {}
ORDER = []
def part(key, inst, role, vol, pan, **kw):
    PARTS[key] = dict(meta=dict(instrument=inst, role=role, volume=vol, pan=pan, **kw), bars=[None] * NB); ORDER.append(key)
def put(key, bi, toks):
    if isinstance(toks, str): toks = toks.split()
    t = 0.0
    for x in toks:
        if x.startswith("g:"): assert len(x) == 18, x; t += 4; continue
        d = x.split(":")[1]; t += float("".join(c for c in d if c.isdigit() or c == "."))
    assert abs(t - 4) < 1e-6, (key, bi, bars[bi]["kind"], t, toks)
    PARTS[key]["bars"][bi] = " ".join(toks)

DR = -7   # ドラムは -7dB（『ネオンハートビート』の点数の試行で決めた値）
part("pmel", "piano", "旋律（ピアノ）", 0.22, -0.05, reverb=0.2, gainDb=2)
part("lead", "leadGuitar", "旋律・ソロ（リードギター）", 0.16, 0.08, gainDb=3, guitarTone="warm-lead-b", humanPitch=0, autoScoop=False)
part("bell", "fmBell", "きらめき（FMベル）", 0.07, 0.3, reverb=0.35)
part("parp", "piano", "ピアノ（分散和音）", 0.15, -0.3, reverb=0.15)
part("gl", "distGuitar", "ギター（左）", 0.07, -0.85, amp="hardrock", ampDrive=0.9, ampTone=-3, chorus=0, reverb=0.1)
part("gr", "distGuitar", "ギター（右）", 0.07, 0.85, amp="hardrock", ampDrive=0.9, ampTone=-3, chorus=0, reverb=0.1, push=0.008)
part("sth", "strings", "弦（上）", 0.09, 0.6, reverb=0.25)
part("stl", "strings", "弦（下）", 0.08, -0.6, reverb=0.25)
part("sawh", "unisonSaw", "厚いシンセ（上）", 0.06, 0.45, reverb=0.2, duck=0.25)
part("sawl", "unisonSaw", "厚いシンセ（下）", 0.06, -0.45, reverb=0.2, duck=0.25)
part("padh", "pad", "パッド（上）", 0.08, 0.35, reverb=0.4)
part("padl", "pad", "パッド（下）", 0.08, -0.35, reverb=0.4)
part("bass", "bass", "ベース", 0.32, 0)
part("bsolo", "bass", "ベースソロ", 0.3, 0, gainDb=2)
part("kick", "kick", "キック", 0.3, 0, gainDb=DR)
part("snare", "snare", "スネア", 0.26, 0, push=0.02, gainDb=DR)
part("hihat", "hihat", "ハイハット", 0.08, 0, push=-0.008, gainDb=DR)
part("crash", "crash", "クラッシュ", 0.1, 0, gainDb=DR)
part("ride", "crash", "ライド", 0.07, 0.2, gainDb=DR)
part("tom", "tom", "タム", 0.14, 0, reverb=0, gainDb=DR)

R4 = "R:4"
PAT16 = [0, 2, 1, 3, 4, 3, 2, 1, 0, 2, 1, 3, 4, 5, 4, 3]

# ---- リードギターのソロ（チョーキング・ビブラートなし。音階の流れ・分散和音・長い音で歌う）----
def fit4(ev):
    s = sum(d for _, d in ev)
    if s < 4: ev[-1] = (ev[-1][0], ev[-1][1] + 4 - s)
    elif s > 4:
        out, acc = [], 0.0
        for n, d in ev:
            if acc + d >= 4 - 1e-9: out.append((n, 4 - acc)); break
            out.append((n, d)); acc += d
        ev = out
    return [f"{nm(n)}:{fmt(d)}" for n, d in ev]

def run(start, count, direction, pcs, dur=0.25):
    out, m = [], start
    for _ in range(count): out.append((m, dur)); m = step(m, direction, pcs)
    return out

def solo_bar(b):
    c, i = b["chord"], b["i"]; pcs = scale_for(c); rnd = i // 8; m = i % 8
    t = [md(x) for x in TONES[c]]
    r, th, f5 = t[0] + 12, t[1] + 12, t[2] + 12          # C#5 付近
    if rnd == 0:     # 歌うように: 長い音と8分（中音域）
        if m % 2 == 0: ev = [(snap(f5, pcs), 1.5), (step(f5, -1, pcs), 0.5), (th, 1), (step(th, -1, pcs), 1)]
        else: ev = [(r, 0.5), (step(r, 1, pcs), 0.5), (th, 0.5), (f5, 0.5), (step(f5, 1, pcs), 2)]
    elif rnd == 1:   # 8分のフレーズ＋16分の飾り
        if m % 2 == 0: ev = [(f5 + 5 if (f5 + 5) % 12 in pcs else step(f5, 2, pcs), 1)] + run(step(f5, 1, pcs), 4, -1, pcs) + [(th, 1), (r, 1)]
        else: ev = [(r, 0.5), (th, 0.5), (f5, 0.5), (r + 12, 0.5)] + run(r + 12, 4, -1, pcs) + [(step(r + 12, -4, pcs), 1)]
    elif rnd == 2:   # 16分の音階（上がって下りる）
        lo = snap(r, pcs)
        ev = run(lo, 8, +1, pcs) + run(step(lo, 8, pcs), 8, -1, pcs) if m % 2 == 0 else run(snap(r + 12, pcs), 12, -1, pcs) + [(th, 1)]
    elif rnd == 3:   # 分散和音で2オクターブを駆け上がる（高音域）
        arp = [r, th, f5, r + 12, th + 12, f5 + 12, r + 24, f5 + 12]
        ev = [(x, 0.25) for x in arp] + ([(th + 12, 1), (f5 + 12, 1)] if m % 2 == 0 else [(r + 24, 2)])
    else:            # 山場: 高い音の呼びかけと応え → 最後は長い音で着地
        hi = snap(r + 24 if m < 6 else r + 19, pcs)
        if m < 6:
            st = step(hi, -2, pcs)
            while st % 12 not in PCS[c]: st -= 1      # 3拍目から下りる16分は、和音の音から始める
            ev = [(hi, 1.5), (step(hi, -1, pcs), 0.5)] + run(st, 8, -1, pcs)
        elif m == 6: ev = run(snap(r + 12, pcs), 8, +1, pcs) + [(snap(r + 24, pcs), 2)]
        else: ev = [(md("G#5"), 2), (md("C6"), 2)]     # G#7 の上で導音（C）→ 次のブリッジへ
    ev = [(x - 12 if x > 88 else x, d) for x, d in ev]   # リードギターの音域（〜E6）
    def ct(x):   # 0.5拍以上の音は和音の音へ寄せる（和音の半音上でぶつからないように）
        while x % 12 not in PCS[c]: x -= 1
        return x
    return fit4([(ct(x) if d >= 0.5 else x, d) for x, d in ev])

# ---- ピアノのソロ（もとのタッピングの音の流れを、16分のピアノに）----
def psolo_bar(b):
    c, i = b["chord"], b["i"]; pcs = scale_for(c)
    t = [md(x) + 12 for x in TONES[c]]; a, cc = t[0], t[2]
    tapped = snap(cc + 12 + (4 if i >= 20 else 0), pcs)
    if i < 16:   # 前半は8分で落ち着いて
        seq = [a, cc, tapped, cc, a, cc, step(tapped, 1, pcs), cc]
        return [f"{nm(x)}:0.5" for x in seq]
    out = []
    for beat in range(4):
        tp = step(tapped, ([0, 2, 1, 3] if i % 2 == 0 else [3, 1, 2, 0])[beat], pcs)
        for x in ([a, cc, tp, cc] if beat % 2 == 0 else [a, cc, step(tp, 1, pcs), cc]): out.append(f"{nm(x)}:0.25")
    return out

# ---- ベースソロ（指で弾くベース）----
def bass_solo_bar(b, nxt):
    c, idx = b["chord"], b["i"]; pcs = scale_for(c)
    lo = root_in(c, 28) + 12; f5 = lo + 7; nlo = root_in(nxt, 28) + 12
    m = idx % 8
    if m < 3: base = [lo, lo, lo + 12, lo, lo + 12, lo, f5, lo, lo, lo + 12, lo, lo, f5, lo + 12, lo, nlo - 1]; ev = [(x, 0.25) for x in base]
    elif m < 5:
        top = snap(lo + 14, pcs)
        ev = [(top, 0.75), (step(top, -1, pcs), 0.25), (step(top, -2, pcs), 0.5), (step(top, -3, pcs), 0.5),
              (step(top, -2, pcs), 0.5), (step(top, -4, pcs), 0.5), (lo + 12, 0.5), (nlo - 1, 0.5)]
    elif m < 7:
        up = [snap(lo, pcs)]
        for _ in range(7): up.append(step(up[-1], 1, pcs))
        ev = [(x, 0.25) for x in up + up[::-1][:-1] + [up[0]]]
    else:
        ev = [(lo + 12 + 7 - j, 0.25) for j in range(0, 8, 2)] + [(lo + 12, 0.5), (lo + 7, 0.5), (lo, 1), (nlo - 1, 1)]
    out = []
    for x, d in ev:
        while x > md("G3"): x -= 12
        out.append((x, d))
    return fit4(out)

# ---- ドラム（1文字＝16分）----
Z = "................"
CHO_K = ["X..xX..xX..xX..x", "X..xX...X..xX.x."]
def tomtok(tm, pit=("E3", "E3", "C3", "C3", "A2", "A2")):
    hits = [j for j, ch in enumerate(tm) if ch in "xX"]; toks = []; k = 0
    for ch in tm:
        if ch in "xX": toks.append(pit[min(len(pit) - 1, k * len(pit) // max(1, len(hits)))] + ":0.25" + ("!" if ch == "X" else "")); k += 1
        else: toks.append("R:0.25")
    return toks
FILL_SMALL = ("....X.......oxXX", None)
FILL_TOM = ("....X...........", "........xxXXxxXX")
FILL_BIG = ("....X...ooxxXXXX", "............xXXX")
FILL_LIFT = ("o.o.x.x.xxxxXXXX", "............XXXX")

def drums(b, nxtkind):
    kind, i, n, k = b["kind"], b["i"], b["n"], b["k"]; last = i == n - 1
    kk, sn, hh, ride, crash, fill = Z, Z, Z, False, False, None
    if kind == "intro":
        if i >= 4:
            kk = "X..x..X...x.X..."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.O."; crash = i == 4
        if i == 3: sn = "........o.o.xxXX"
    elif kind == "A":
        if k == 0: kk = "X.....X...X....." if i % 2 == 0 else "X.....X...X..x.."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."
        else: kk = "X..x..X...x.X..." if i % 2 == 0 else "X..x..X...X..x.."; sn = "....X..o....X..."; hh = "xxx.xxx.xxx.xxO."
        crash = i == 0
    elif kind == "B":
        kk = "X...X..xX...X..x"; sn = "....X..o....X..o"; hh = "x.x.x.x.x.x.x.x." if i < 4 else "xxxxxxxxxxxxxxxx"
        ride = k == 1 and i < 4
        if ride: hh = Z
        crash = i == 0
    elif kind in ("CH", "F1", "F2"):
        kk = CHO_K[i % 2]; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."; crash = i % 4 == 0
        if kind == "F2" and i in (1, 2, 5, 6): hh = Z; ride = True
    elif kind == "gsolo":
        blk = i // 8
        if blk == 0: kk = "X.......X.x....."; sn = "........X......."; ride = True
        elif blk == 1: kk = CHO_K[i % 2]; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."
        elif blk == 2: kk = "X...X...X...X..."; sn = "....X.......X..."; ride = True
        elif blk == 3: kk = "X.X.X.X.X.X.X.X."; sn = "....X.......X..."; hh = "xxxxxxxxxxxxxxxx"
        else: kk = CHO_K[i % 2]; sn = "....X.......X..."; hh = "x.O.x.O.x.O.x.O."
        crash = i % 8 == 0 or (blk == 4 and i % 2 == 0)
    elif kind == "bridge":
        if i < 8: kk = "X.......X......." if i % 2 == 0 else "X.......X..x...."; hh = "x...x...x...x..."
        else: kk = "X.......X.x....."; sn = "........X......."; ride = True
        crash = i in (0, 8)
    elif kind == "psolo":
        if i < 16: kk = "X.......X......."; sn = "....X.......X..."; hh = "x.x.x.x.x.x.x.x."
        elif i < 32: kk = CHO_K[i % 2]; sn = "....X.......X..."; hh = "xxx.xxx.xxx.xxO."
        else: kk = CHO_K[i % 2]; sn = "....X.......X..."; hh = Z; ride = True
        crash = i % 8 == 0
    elif kind == "bsolo":
        if i < 16: kk = "X......xX.x....."; sn = "....X..o.o..X..o"; hh = "x.x.x.x.x.x.x.x."
        else: kk = "X..x..X...x.X..."; sn = "....X..o....X..o"; ride = True
        crash = i % 8 == 0
    elif kind == "dsolo":
        sec, j = i // 4, i % 4
        if sec == 0:
            kk = "X.....x.x.x....."; sn = "o.o.X.o.o.o.X.o."; hh = "x.x.x.x.x.x.x.x."
            if j == 3: sn = "....X.....xxXXXX"
        elif sec == 1:
            kk = "xxxxxxxxxxxxxxxx"; kk = "X" + kk[1:]; sn = "....X.......X..."
            if j == 3: sn = "....X...xx......"
        elif sec == 2:
            kk = "X..x.x....x..x.."; sn = "....X..o...oX..x"; hh = "X.x.X.x.X.x.X.x."
        else:
            kk = "X...X...X...X..."; sn = "xxxxxxxxxxxxxxxx" if j < 2 else "xxxxxxxxXXXXXXXX"
        crash = j == 0
    elif kind == "build":
        if i < 4: kk = "X.......X......."; hh = "x...x...x...x..."
        elif i < 6: kk = "X...X...X...X..."; sn = "x.x.x.x.x.x.x.x."
        elif i == 6: kk = "X...X...X...X..."; sn = "xxxxxxxxxxxxxxxx"
        else: kk = "X...X...X...X..."; sn = "xxxxxxxxXXXXXXXX"
        crash = i == 0
    elif kind == "space":
        kk = "X.......X......." if i % 2 == 0 else "X..............."; sn = "........o......." if i >= 8 else Z
        ride = True; crash = i == 0
    elif kind == "fade":
        kk = "X..............." if i % 2 == 0 and i < 12 else Z
    elif kind == "end":
        kk = "X..............." if i == 0 else Z; crash = i == 0
    # フィル（4小節ごとに小さく、8小節ごとにタム、セクションの終わりは大きく）
    busy = kind not in ("intro", "dsolo", "build", "space", "fade", "end") and (kk != Z or sn != Z)
    if busy:
        if last:
            if kind == "F2": kk = "X..............."; sn = "X..............."; hh = Z; ride = False; fill = None   # 空間へ入る前は一発で止める
            elif nxtkind in ("dsolo",): fill = FILL_BIG
            elif kind in ("bridge",): fill = FILL_LIFT
            else: fill = FILL_BIG
        elif i % 8 == 7: fill = FILL_TOM
        elif i % 4 == 3: fill = FILL_SMALL
    tm = None
    if kind == "dsolo" and i % 4 == 3 and i // 4 == 0: tm = None
    if kind == "dsolo" and i // 4 == 1 and i % 4 == 3: tm = "........xxXXxxXX"
    if kind == "dsolo" and i // 4 == 3 and i % 4 >= 2: tm = "........xxxxXXXX"
    if kind == "build" and i == 7: tm = "............XXXX"
    if fill:
        fs, ft = fill
        sn = "".join(f if f != "." else sn[j] for j, f in enumerate(fs))
        if ft:
            tm = ft; first = ft.index(next(ch for ch in ft if ch in "xX")); hh = hh[:first] + "." * (16 - first); ride = False
            kk = kk[:8] + "".join("X" if j % 4 == 0 else "." for j in range(8))
        else: hh = hh[:12] + "...."
    if tm:   # タムと同時の音は外す（手は2本）
        first = next(j for j, ch in enumerate(tm) if ch in "xX")
        sn = sn[:first] + "".join("." if tm[first + j] in "xX" else c for j, c in enumerate(sn[first:]))
        hh = hh[:first] + "." * (16 - first)
    if crash: hh = "." + hh[1:]
    return kk, sn, hh, ride, crash, tm

ARC = []
for bi, b in enumerate(bars):
    kind, i, n, k = b["kind"], b["i"], b["n"], b["k"]; f = i / max(1, n - 1)
    g = {"intro": 0.75 + 0.1 * f, "A": 0.8 + 0.04 * k, "B": 0.88 + 0.07 * f, "CH": 1.0, "gsolo": 0.9 + 0.12 * f,
         "bridge": 0.72 + 0.08 * f, "psolo": 0.85 + 0.15 * f, "bsolo": 0.86, "dsolo": 0.95, "build": 0.8 + 0.2 * f,
         "F1": 1.02, "F2": 1.05, "space": 0.85 - 0.05 * f, "fade": 0.75 - 0.2 * f, "end": 0.55}[kind]
    ARC.append(round(min(1.05, g), 3))

for bi, b in enumerate(bars):
    kind, c, i, n, k = b["kind"], b["chord"], b["i"], b["n"], b["k"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < NB else c
    nxtkind = bars[bi + 1]["kind"] if bi + 1 < NB else None
    last = i == n - 1
    t = [md(x) for x in TONES[c]]
    # 旋律（ピアノ）
    if kind in ("A", "B"): put("pmel", bi, mel_bar(kind, i))
    elif kind == "bridge":
        f5 = md(FIFTH[c]); pcs = scale_for(c); th = t[1] + 12
        put("pmel", bi, [f"{nm(f5)}:1.5", f"{nm(step(f5, -1, pcs))}:0.5", f"{nm(th)}:2"] if i % 8 != 7 else [f"{nm(f5)}:4"])
    elif kind == "psolo": put("pmel", bi, psolo_bar(b))
    elif kind == "space": put("pmel", bi, mel_bar("CH", i, -12 if i >= 8 else 0))
    elif kind == "end": put("pmel", bi, ["C#4:4"] if i == 0 else [R4])
    else: put("pmel", bi, [R4])
    # リードギター
    if kind in ("CH", "F1", "F2"): put("lead", bi, mel_bar("CH", i, -12))   # サビはギターを1オクターブ下（太い中音域）、上の音はベルが受け持つ
    elif kind == "gsolo": put("lead", bi, solo_bar(b))
    elif kind == "build" and i >= 4:
        pcs = scale_for(c); m0 = snap(md("E5") + i - 4, pcs)
        put("lead", bi, [f"{nm(step(m0, q // 2, pcs))}:0.5" for q in range(8)])
    elif kind == "psolo" and i >= 32: put("lead", bi, [f"{nm(md(FIFTH[c]) + (12 if md(FIFTH[c]) < md('C5') else 0))}:4"])
    else: put("lead", bi, [R4])
    # FM ベル
    if kind == "intro" and i < 4: put("bell", bi, mel_bar("CH", i))
    elif kind in ("CH", "F1", "F2"): put("bell", bi, mel_bar("CH", i))
    elif kind in ("bridge", "space", "fade") or (kind == "end" and i == 0):
        x = md(TONES[c][2]) + 24
        put("bell", bi, [f"{nm(x if x <= md('C7') else x - 12)}:2", "R:2"])
    else: put("bell", bi, [R4])
    # ピアノの分散和音
    tt = tones_from(c, 55)
    if (kind == "intro" and i >= 4) or kind in ("A", "B", "CH", "F1", "F2"):
        if kind == "B" and last: put("parp", bi, [f"{nm(tt[0])}:0.25", f"{nm(tt[2])}:0.25", f"{nm(tt[4])}:0.5", f"{nm(tt[3])}:3"])
        else: put("parp", bi, [f"{nm(tt[j % len(tt)])}:0.25" for j in PAT16])
    elif kind in ("bridge", "space"): put("parp", bi, [f"{nm(tt[j % len(tt)])}:0.5" for j in (0, 2, 4, 2, 0, 2, 4, 2)])
    elif kind == "fade": put("parp", bi, [f"{nm(tt[j])}:1" for j in (0, 2, 4, 2)] if i < 12 else ([f"{nm(tt[0])}:4"] if i % 2 == 0 else [R4]))
    elif kind == "bsolo": put("parp", bi, [f"{nm(tt[j])}:1" for j in (0, 2, 4, 2)])
    else: put("parp", bi, [R4])
    # 歪みギター（左右）
    r = nm(root_in(c, 40))
    if kind in ("CH", "F1", "F2", "gsolo") or (kind == "intro" and i >= 4) or (kind == "psolo" and i >= 16) or (kind == "build" and i >= 4):
        g = [f"{r}:0.5"] * 8
        if kind == "gsolo" and i < 8: g = [f"{r}:2", f"{r}:2"]
    elif kind == "A" and k == 1: g = [f"{r}:2", f"{r}:2"]
    elif kind == "B": g = [f"{r}:1.5", f"{r}:0.5", f"{r}:1", f"{r}:1"] if not last else [f"{r}:4"]
    elif kind == "bridge" and i >= 8: g = [f"{r}:4"]
    elif kind == "dsolo" and i % 4 == 0: g = [f"{r}:4"]
    elif kind == "F2" and last: g = [f"{r}:4"]
    else: g = [R4]
    if kind == "F2" and last: g = [f"{r}:4"]
    put("gl", bi, g); put("gr", bi, g)
    # 弦・厚いシンセ・パッド
    STR = kind in ("B", "CH", "F1", "F2", "build", "space") or (kind == "gsolo" and i >= 16) or (kind == "bridge" and i >= 8) or (kind == "psolo" and i >= 16) or (kind == "fade" and i < 12)
    put("sth", bi, [f"{nm(voicing(c, 70)[2])}:4"] if STR else [R4])
    put("stl", bi, [f"{nm(voicing(c, 58)[0])}:4"] if STR else [R4])
    SAW = kind in ("CH", "F1", "F2") or (kind == "gsolo" and i >= 32) or (kind == "psolo" and i >= 32) or (kind == "build" and i >= 4)
    put("sawh", bi, [f"{nm(voicing(c, 66)[1])}:4"] if SAW else [R4])
    put("sawl", bi, [f"{nm(voicing(c, 62)[0])}:4"] if SAW else [R4])
    PAD = kind in ("intro", "bridge", "bsolo", "dsolo", "space", "fade", "end") or (kind == "A" and k == 0)
    put("padh", bi, [f"{nm(voicing(c, 64)[2])}:4"] if PAD and not (kind == "end" and i == 1) else [R4])
    put("padl", bi, [f"{nm(voicing(c, 56)[1])}:4"] if PAD and not (kind == "end" and i == 1) else [R4])
    # ベース
    lo = root_in(c, 28); a, o, f5 = nm(lo), nm(lo + 12), nm(lo + 7)
    rn = root_in(nxt, 28); ap = nm(rn - 1 if rn > lo else rn + 1) if rn != lo else f5
    if kind in ("CH", "F1", "F2", "gsolo", "psolo") or (kind == "intro" and i >= 4):
        if kind == "F2" and last: bs = [f"{a}:4"]
        elif kind == "gsolo" and i < 8: bs = [f"{a}:1.5", f"{a}:0.5", f"{o}:1", f"{ap}:1"]
        elif kind == "psolo" and i < 16: bs = [f"{a}:0.75", f"{a}:0.75", f"{o}:0.5", f"{a}:0.5", f"{f5}:0.5", f"{o}:0.5", f"{ap}:0.5"]
        elif i % 4 != 3: bs = [a + ":0.5", a + ":0.5", o + ":0.5", a + ":0.5", a + ":0.5", o + ":0.5", f5 + ":0.5", ap + ":0.5"]
        else: bs = [a + ":0.5", o + ":0.5", a + ":0.5", o + ":0.5", f5 + ":0.25", o + ":0.25", f5 + ":0.25", a + ":0.25", ap + ":1"]
    elif kind == "A": bs = [f"{a}:0.75", f"{a}:0.75", f"{o}:0.5", f"{a}:0.5", f"{f5}:0.5", f"{o}:0.5", f"{ap}:0.5"] if k == 1 else [f"{a}:1.5", f"{a}:0.5", f"{f5}:1", f"{ap}:1"]
    elif kind == "B": bs = [a + ":0.5"] * 6 + [o + ":0.5", ap + ":0.5"] if not last else [f"{a}:4"]
    elif kind == "bridge": bs = [f"{a}:4"] if i < 8 else [f"{a}:1.5", f"{a}:0.5", f"{o}:1", f"{ap}:1"]
    elif kind == "dsolo": bs = [f"{a}:4"] if i % 4 == 0 else [R4]
    elif kind == "build": bs = [f"{a}:2", f"{a}:2"] if i < 4 else [a + ":0.5"] * 8
    elif kind == "space": bs = [f"{a}:4"]
    elif kind == "fade": bs = [f"{a}:4"] if i % 2 == 0 and i < 12 else [R4]
    elif kind == "end": bs = [f"{nm(md('C#2'))}:4"] if i == 0 else [R4]
    else: bs = [R4]
    put("bass", bi, bs)
    put("bsolo", bi, bass_solo_bar(b, nxt) if kind == "bsolo" else [R4])
    # ドラム
    kk, sn, hh, ride, crash, tm = drums(b, nxtkind)
    put("kick", bi, ["g:" + kk]); put("snare", bi, ["g:" + sn]); put("hihat", bi, ["g:" + hh])
    put("crash", bi, ["g:X..............."] if crash else [R4])
    put("ride", bi, ["D2:0.5"] * 8 if ride else [R4])
    put("tom", bi, tomtok(tm) if tm else [R4])

parts = []
for key in ORDER:
    p = PARTS[key]; assert all(x is not None for x in p["bars"]), key
    d = dict(p["meta"]); d["notes"] = " ".join(p["bars"]); d["barGain"] = ARC; parts.append(d)

song = {"title": "緋色の断章（現代版・6分）",
        "description": "（仮）「緋色の断章（空間版・6分）」の旋律・コード・構成をそのままに、きれいで現代的な音に作り変えた版。BPM172・嬰ハ短調・258小節（6分）。"
                       "旋律は A・Bメロがピアノ、サビとギターソロがリードギター（ビブラート・チョーキングなし）、サビは FM ベルを重ねる。16分のピアノ・左右の歪みギター・左右の弦・サビの厚いシンセ・生ドラム。"
                       "タッピングはピアノの速いソロに、スラップのベースソロは指で弾くベースのソロにした。最後はピアノとパッドとベルの空間に溶けていく。"
                       "入り方: パッドと FM ベルだけでサビの動機を4小節。終わり方: 全員で一発止め → 空間 → 長い和音。",
        "bpm": 172, "beats": 4, "chords": " ".join(b["chord"] for b in bars), "barsPerChord": 1, "repeats": 1,
        "tone": "rock", "feel": "rock", "human": 0.25, "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False,
        "parts": parts}
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/scarlet-chapter-modern-long.json"
json.dump({"guitarWobble": False, **song}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(parts), "parts", NB, "bars", round(NB * 4 * 60 / 172), "sec")
