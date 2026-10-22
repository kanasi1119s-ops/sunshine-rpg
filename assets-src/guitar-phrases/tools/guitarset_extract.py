# GuitarSet（CC BY 4.0。Q. Xi, R. Bittner, J. Pauwels, X. Ye, J. P. Bello, ISMIR 2018。https://zenodo.org/records/3371780）の
# 注釈（annotation.zip の .jams）から、4/4 の1〜2小節の「実演の型」を取り出す。
#   使う: 進行1（12小節のブルース形式。どの曲でもない一般的な形）と進行3（I-V-vi-iii-IV-I-IV-V。300年以上前のカノンと同じ一般的な並び）
#   使わない: 進行2（ii-V-I-IV-viiø-III-vi。既存のスタンダード曲のコード進行に基づくため、CLAUDE.md 1-1 に照らして外す）
#   取り出すのは「根音からの半音の数」と「リズム」だけ（音そのもの・録音は使わない）。
# 使い方: python3 -I guitarset_extract.py <annotationを展開したフォルダ> <出力.json>
import json, glob, os, sys, statistics

TPB = 12
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def at_least(pc, low): return low + ((pc - low) % 12)

def chord_root(label):
    label = label.split("/")[0]
    r, q = label.split(":") if ":" in label else (label, "maj")
    return NAMES.index(r), q

def load(path):
    d = json.load(open(path))
    notes = []
    for a in d["annotations"]:
        if a["namespace"] == "note_midi":
            for x in a["data"]:
                notes.append((x["time"], x["duration"], int(round(x["value"]))))
    beats = [(x["time"], x["value"]["position"]) for a in d["annotations"] if a["namespace"] == "beat_position" for x in a["data"]]
    chords = [(x["time"], x["duration"], x["value"]) for a in d["annotations"] if a["namespace"] == "chord" and a["annotation_metadata"].get("data_source", "").startswith("Semi") for x in a["data"]]
    if not chords:
        chords = [(x["time"], x["duration"], x["value"]) for a in d["annotations"] if a["namespace"] == "chord" for x in a["data"]]
    return sorted(notes), sorted(beats), chords

def to_tick(t, bt):
    """時刻 → 刻み（拍の時刻の間を直線でつなぐ）"""
    if t <= bt[0]: return (t - bt[0]) / (bt[1] - bt[0]) * TPB
    for i in range(len(bt) - 1):
        if bt[i] <= t < bt[i + 1]:
            return (i + (t - bt[i]) / (bt[i + 1] - bt[i])) * TPB
    return (len(bt) - 1 + (t - bt[-1]) / (bt[-1] - bt[-2])) * TPB

def cluster(notes, gap=0.06):
    """ほぼ同時の音（かき鳴らしの時間差）をまとめる"""
    out = []
    for n in notes:
        if out and n[0] - out[-1][0][0] < gap: out[-1].append(n)
        else: out.append([n])
    return out

def extract(path):
    base = os.path.basename(path)[:-5]
    style = base.split("_")[1].split("-")[0]
    prog = style[-1]; style = style[:-1]
    if prog == "2": return []
    kind = base.split("_")[-1]   # comp / solo
    notes, beats, chords = load(path)
    bt = [b[0] for b in beats]
    pos = [b[1] for b in beats]
    if len(bt) < 8: return []
    first_down = next(i for i, p in enumerate(pos) if p == 1)
    groups = cluster(notes)
    raw = []
    for g in groups:
        t0 = g[0][0]
        tk = to_tick(t0, bt) - first_down * TPB
        ends = [to_tick(n[0] + n[1], bt) - first_down * TPB for n in g]
        raw.append((tk, max(ends), sorted({n[2] for n in g})))
    # 格子: 16分（3刻み）と3連（4刻み）のどちらに近いか
    def err(step): return statistics.mean(abs(r[0] - round(r[0] / step) * step) for r in raw) / step
    grid = 4 if err(4) < 0.7 * err(3) else 3
    ev = []
    for tk, end, ps in raw:
        q = int(round(tk / grid) * grid)
        if q < 0: continue
        if ev and ev[-1][0] == q:
            ev[-1][2] = sorted(set(ev[-1][2]) | set(ps)) if kind == "comp" else ps
            continue
        d = max(grid, int(round((end - tk) / grid) * grid))
        ev.append([q, d, ps])
    for i in range(len(ev) - 1):
        ev[i][1] = min(ev[i][1], ev[i + 1][0] - ev[i][0])
    nbars = int(ev[-1][0] // 48) + 1 if ev else 0
    # 小節頭の和音
    bar_t = [bt[first_down + 4 * b] if first_down + 4 * b < len(bt) else None for b in range(nbars + 1)]
    def chord_at(t):
        for c0, cd, lab in chords:
            if c0 - 0.05 <= t < c0 + cd - 0.05: return lab
        return chords[-1][2]
    cells = []
    for b in range(nbars):
        if bar_t[b] is None: continue
        lab = chord_at(bar_t[b] + 0.02)
        root, q = chord_root(lab)
        if q not in ("maj", "min"): continue
        span = [e for e in ev if b * 48 <= e[0] < (b + 1) * 48]
        if not span: continue
        cells.append({"bar": b, "root": root, "q": q, "ev": span, "lab": lab})
    out = []
    for c in cells:
        out.append(make_phrase(base, style, kind, grid, [c]))
        nxt = next((x for x in cells if x["bar"] == c["bar"] + 1), None)
        if nxt and nxt["root"] == c["root"] and nxt["q"] == c["q"]:
            out.append(make_phrase(base, style, kind, grid, [c, nxt]))
    return [p for p in out if p]

def make_phrase(base, style, kind, grid, cs):
    root = cs[0]["root"]; ref = at_least(root, 40)   # E2 以上でいちばん低い根音
    b0 = cs[0]["bar"]
    ev = []
    for c in cs:
        for t, d, ps in c["ev"]:
            T = t - b0 * 48
            D = min(d, len(cs) * 48 - T)
            if kind == "comp" and len(ps) > 4: ps = [ps[0]] + ps[-3:]
            if kind == "solo": ps = [ps[-1]]   # 単音（重なったら上の音）
            ev.append([T, D, [p - ref for p in ps], "!" if T % 48 == 0 else ""])
    return {"src": f"GuitarSet(CC BY 4.0) {base} 小節{b0 + 1}" + (f"〜{b0 + len(cs)}" if len(cs) > 1 else ""), "style": style, "gkind": kind, "grid": grid,
            "q": cs[0]["q"], "bars": len(cs), "ev": ev}

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    allp = []
    for f in sorted(glob.glob(os.path.join(src, "*.jams"))):
        try: allp += extract(f)
        except Exception as e: print("飛ばす", f, e)
    json.dump(allp, open(dst, "w"), ensure_ascii=False)
    print(len(allp), "個の型（ふるい落とし前）")
