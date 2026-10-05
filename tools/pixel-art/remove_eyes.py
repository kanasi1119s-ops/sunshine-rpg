#!/usr/bin/env python3
"""雑魚（enemy:*）の絵から、光る目を取りのぞく（人間の指示 2026-10-05「雑魚モンスターに無理に目がついてるけど、なくてもいい」）。

使い方: python3 tools/pixel-art/remove_eyes.py [--write] [--sheet 出力.png]
  enemy-art.json の enemy:* を読み、「まわりより明るく色の濃い、小さなかたまり」（光る目）を、
  まわりの色（パレットの中でいちばん近い色）で塗りつぶす。大きな目（レンズなど）・歯・口・体の模様は、そのまま。
  --write をつけたときだけ enemy-art.json を書きかえる。そのあと node tools/pixel-art/export-game-data.mjs でゲームに入れる。
"""
import json, os, sys
import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "enemy-art.json")


def decode(entry):
    size, pal, rle = entry["size"], entry["palette"], entry["rle"]
    cells = []
    if rle.startswith("~"):
        for tok in rle[1:].split(","):
            v, n = tok.split(":")
            cells += [int(v)] * int(n)
    else:
        i = 0
        while i < len(rle):
            ch = rle[i]; i += 1
            j = i
            while j < len(rle) and (rle[j].isdigit() or rle[j].islower()):
                j += 1
            n = int(rle[i:j], 36) if j > i else 1
            i = j
            cells += [-1 if ch == "_" else ord(ch) - 65] * n
    return np.array(cells[: size * size]).reshape(size, size)


def encode(g, wide):
    flat = [int(v) for v in g.flatten()]
    if wide:
        toks, prev, n = [], None, 0
        for v in flat:
            if v == prev: n += 1
            else:
                if prev is not None: toks.append(f"{prev}:{n}")
                prev, n = v, 1
        toks.append(f"{prev}:{n}")
        return "~" + ",".join(toks)
    s, prev, n = "", None, 0
    for v in flat:
        ch = "_" if v < 0 else chr(65 + v)
        if ch == prev: n += 1
        else:
            if prev is not None: s += prev + (np.base_repr(n, 36).lower() if n > 1 else "")
            prev, n = ch, 1
    s += prev + (np.base_repr(n, 36).lower() if n > 1 else "")
    return s


def hex2rgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def remove_eyes(idx, pal, maxsize=40, topfrac=0.62):
    h, w = idx.shape
    alpha = idx >= 0
    if not alpha.any(): return idx, 0
    rgb_pal = np.array([hex2rgb(c) for c in pal], float)
    rgb = np.zeros((h, w, 3)); rgb[alpha] = rgb_pal[idx[alpha]]
    ys, xs = np.where(alpha)
    top_limit = ys.min() + (ys.max() - ys.min()) * topfrac
    mx = rgb.max(axis=2); mn = rgb.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    glow = alpha & (mx > 175) & (sat > 0.42)
    inner = ndi.binary_erosion(alpha, iterations=2)
    lab, n = ndi.label(glow & inner, structure=np.ones((3, 3)))
    out = idx.copy(); total = 0
    for i in range(1, n + 1):
        pts = np.argwhere(lab == i)
        if len(pts) > maxsize: continue
        if pts[:, 0].max() - pts[:, 0].min() + 1 > 10 or pts[:, 1].max() - pts[:, 1].min() + 1 > 10: continue
        if pts[:, 0].mean() > top_limit: continue
        mask = np.zeros((h, w), bool); mask[tuple(pts.T)] = True
        mask = ndi.binary_dilation(mask, iterations=2) & alpha
        ring = ndi.binary_dilation(mask, iterations=2) & alpha & ~mask & ~(glow)
        if ring.sum() < 4: continue
        med = np.median(rgb[ring], axis=0)
        near = int(np.argmin(((rgb_pal - med) ** 2).sum(axis=1)))
        out[mask] = near; total += len(pts)
    return out, total


def main():
    write = "--write" in sys.argv
    sheet = sys.argv[sys.argv.index("--sheet") + 1] if "--sheet" in sys.argv else None
    data = json.load(open(PATH))
    report, pairs = [], []
    for key, e in data.items():
        if not key.startswith("enemy:"): continue
        idx = decode(e)
        new, t = remove_eyes(idx, e["palette"])
        if t:
            report.append((key, t))
            pairs.append((key, e, idx, new))
            if write: e["rle"] = encode(new, len(e["palette"]) > 26)
    print(f"{len(report)} 体で目を消した:", ", ".join(f"{k[6:]}({t})" for k, t in report))
    if write:
        json.dump(data, open(PATH, "w"), ensure_ascii=False)
        print("enemy-art.json を書きかえた")
    if sheet:
        from PIL import Image
        cols = 8; W = 192
        rows = (len(pairs) * 2 + cols - 1) // cols
        im = Image.new("RGB", (cols * W, rows * W), (40, 40, 60))
        for n, (key, e, a, b) in enumerate(pairs):
            pal = np.array([hex2rgb(c) for c in e["palette"]], np.uint8)
            for k, g in enumerate((a, b)):
                arr = np.zeros((g.shape[0], g.shape[1], 4), np.uint8)
                m = g >= 0; arr[m, :3] = pal[g[m]]; arr[m, 3] = 255
                I = Image.fromarray(arr).resize((W, W), Image.NEAREST)
                pos = ((n * 2 + k) % cols * W, (n * 2 + k) // cols * W)
                im.paste(I, pos, I)
        im.save(sheet)


if __name__ == "__main__":
    main()
