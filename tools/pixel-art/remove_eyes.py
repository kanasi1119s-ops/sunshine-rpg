#!/usr/bin/env python3
"""雑魚（enemy:*）の絵から、「顔ではない場所の目」を取りのぞく（人間の指示 2026-10-05「雑魚モンスターに無理に目がついてる」「顔じゃないとこに目があるのがおかしい」）。

顔のある生き物（こうもり・ねずみ・鳥・人型など）の目は残す。しずく・石・箱・盾など、顔のない物に付いた目だけを、TARGETS で選んで消す。

使い方: python3 tools/pixel-art/remove_eyes.py [--write] [--sheet 出力.png]
  TARGETS の各敵について、目の場所（96×96の絵の中の x, y と、探す半径）の近くの「まわりとちがう点」を、
  近くの別の場所の絵（毛・石・水の質感）を写してうめる。--write をつけたときだけ enemy-art.json を書きかえる。
  そのあと node tools/pixel-art/export-game-data.mjs でゲームに入れる。
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


def local_median(rgb, alpha, win=9):
    h, w = alpha.shape; r = win // 2
    med = np.zeros_like(rgb)
    for y in range(h):
        for x in range(w):
            if not alpha[y, x]: continue
            sl = (slice(max(0, y - r), y + r + 1), slice(max(0, x - r), x + r + 1))
            med[y, x] = np.median(rgb[sl][alpha[sl]], axis=0)
    return med


def patch_fill(idx, rgb_pal, mask, avoid, alpha):
    """マスクの場所を、近くの「ちがう場所の絵」を写してうめる（毛・うろこ・石の質感がそのまま続く）。
    まわりのふち（マスクの外がわ2マス）が、いちばんよくなじむ向きとずれを探す。見つからなければ、まわりの色で塗る。"""
    h, w = idx.shape
    ring = ndi.binary_dilation(mask, iterations=2) & alpha & ~mask
    ry, rx = np.where(ring); my, mx_ = np.where(mask)
    rgb = np.zeros((h, w, 3)); rgb[alpha] = rgb_pal[idx[alpha]]
    best, best_cost = None, 1e18
    for dy in range(-18, 19):
        for dx in range(-18, 19):
            if abs(dx) + abs(dy) < 6: continue
            sy, sx = my + dy, mx_ + dx
            qy, qx = ry + dy, rx + dx
            if sy.min() < 0 or qy.min() < 0 or sx.min() < 0 or qx.min() < 0 or sy.max() >= h or qy.max() >= h or sx.max() >= w or qx.max() >= w: continue
            if not alpha[sy, sx].all() or not alpha[qy, qx].all(): continue
            if avoid[sy, sx].any() or avoid[qy, qx].any(): continue
            cost = ((rgb[ry, rx] - rgb[qy, qx]) ** 2).sum(axis=1).mean()
            if cost < best_cost: best_cost, best = cost, (dy, dx)
    out = idx.copy()
    # まわりがなめらか（水・光など）なときは、写すより、まわりの色をなだらかにつなぐほうが自然
    if ring.any() and rgb[ry, rx].std(axis=0).mean() < 60:
        known = alpha & ~mask
        work = rgb.copy(); filled = known.copy()
        todo = set(zip(my.tolist(), mx_.tolist()))
        while todo:
            stepped = []
            for (y, x) in todo:
                nb = [(y + a, x + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a or b) and 0 <= y + a < h and 0 <= x + b < w and filled[y + a, x + b]]
                if nb: stepped.append(((y, x), np.mean([work[q] for q in nb], axis=0)))
            if not stepped: break
            for (q, c) in stepped:
                work[q] = c; filled[q] = True; todo.discard(q)
        for (y, x) in zip(my, mx_):
            out[y, x] = int(np.argmin(((rgb_pal - work[y, x]) ** 2).sum(axis=1)))
        return out
    if best is not None and best_cost < 2500:
        dy, dx = best
        out[my, mx_] = idx[my + dy, mx_ + dx]
    else:
        med = np.median(rgb[ring], axis=0) if ring.any() else rgb[mask].mean(axis=0)
        out[mask] = int(np.argmin(((rgb_pal - med) ** 2).sum(axis=1)))
    return out


def remove_eyes(idx, pal, maxsize=60, topfrac=0.62):
    h, w = idx.shape
    alpha = idx >= 0
    if not alpha.any(): return idx, 0
    rgb_pal = np.array([hex2rgb(c) for c in pal], float)
    rgb = np.zeros((h, w, 3)); rgb[alpha] = rgb_pal[idx[alpha]]
    ys, xs = np.where(alpha)
    top_limit = ys.min() + (ys.max() - ys.min()) * topfrac
    med = local_median(rgb, alpha)
    dist = np.sqrt(((rgb - med) ** 2).sum(axis=2))
    mxc = rgb.max(axis=2); mnc = rgb.min(axis=2)
    sat = np.where(mxc > 0, (mxc - mnc) / np.maximum(mxc, 1), 0)
    teeth = (mxc > 195) & (sat < 0.3)                      # 歯・ひげ・白い毛の光は、目と見なさない
    outlier = alpha & (dist > 85) & ~teeth
    inner = ndi.binary_erosion(alpha, iterations=2)
    lab, n = ndi.label(ndi.binary_dilation(outlier & inner, iterations=1) & alpha, structure=np.ones((3, 3)))
    clusters = []
    for i in range(1, n + 1):
        pts = np.argwhere(lab == i)
        if len(pts) > maxsize: continue
        if pts[:, 0].max() - pts[:, 0].min() + 1 > 11 or pts[:, 1].max() - pts[:, 1].min() + 1 > 11: continue
        if pts[:, 0].mean() > top_limit: continue
        m = np.zeros((h, w), bool); m[tuple(pts.T)] = True
        clusters.append(m)
    if not clusters: return idx, 0
    allmask = np.zeros((h, w), bool)
    for m in clusters: allmask |= ndi.binary_dilation(m, iterations=1) & alpha
    out = idx.copy(); total = 0
    for m in clusters:
        mm = ndi.binary_dilation(m, iterations=1) & alpha
        out = patch_fill(out, rgb_pal, mm, allmask & ~mm, alpha)
        total += int(m.sum())
    return out, total


# 顔のない物についた目（敵のID → [(x, y, 半径), ...]）。絵を見て決めた。
TARGETS = {
    "enemy:enc-mugikano-water-source-0": [(50, 32, 9)],            # 水のしずく影: しずくの真ん中の目
    "enemy:enc-mugikano-water-source-5": [(27, 10, 6), (66, 10, 6)],  # 井戸の石: 石のアーチの目
    "enemy:enc-tetsukusari-mine-4": [(50, 38, 7)],                  # 落盤の石: 岩の山の赤い目
    "enemy:enc-sanone-camp-3": [(36, 46, 7), (58, 46, 7)],          # 日照りのしずく: しずくの目
    "enemy:enc-fushima-base-3": [(41, 34, 6), (53, 34, 6)],         # 浮き石: 岩の緑の目
    "enemy:enc-deep-1-3": [(52, 40, 7)],                            # 錆びた盾のかけら: 盾の目
    "enemy:enc-deep-1-5": [(39, 46, 6), (56, 46, 6)],               # 凍った涙: しずく形の目
    "enemy:enc-deep-2-3": [(62, 36, 6), (74, 36, 6)],               # 印章の石: 石の箱の目
    "enemy:enc-deep-2-5": [(51, 30, 7), (61, 30, 7)],               # 黄金のしずく: しずくの目
    "enemy:enc-deep-3-0": [(46, 44, 7)],                            # 歪みの断片: 水晶の目
    "enemy:enc-fushima-base-1": [(47, 38, 7), (57, 38, 7)],         # 配線の歪み: 電線のかたまりの赤い目（先の火花は残す）
}


def remove_spots(idx, pal, spots, reach=18):
    """目は、パレットの最後のほうの、ほとんど使われていない色（暗い瞳・光・白い反射）で描かれている。
    spots の近く（reach ドット以内）にある、その色の点を、まわりの1マスぶんの輪ごと、近くの別の場所の絵でうめる。"""
    h, w = idx.shape
    alpha = idx >= 0
    rgb_pal = np.array([hex2rgb(c) for c in pal], float)
    cnt = np.bincount(idx[alpha].flatten(), minlength=len(pal))
    eye_idx = [i for i in range(max(0, len(pal) - 6), len(pal)) if 0 < cnt[i] <= 48]
    yy, xx = np.mgrid[0:h, 0:w]
    out = idx.copy(); n = 0
    for (x, y, _r) in spots:
        near = ((xx - x) ** 2 + (yy - y) ** 2 <= reach * reach)
        eye = near & np.isin(idx, eye_idx)
        # 1つのかたまりごとに（左右の目を別々に）うめる
        lab, k = ndi.label(ndi.binary_dilation(eye, iterations=2) & eye | eye, structure=np.ones((3, 3)))
        for i in range(1, k + 1):
            m = ndi.binary_dilation(lab == i, iterations=3) & alpha
            allmask = np.isin(out, eye_idx) & near
            out = patch_fill(out, rgb_pal, m, allmask & ~m, alpha)
            n += 1
    return out, n


def main():
    write = "--write" in sys.argv
    sheet = sys.argv[sys.argv.index("--sheet") + 1] if "--sheet" in sys.argv else None
    data = json.load(open(PATH))
    report, pairs = [], []
    for key, spots in TARGETS.items():
        e = data[key]
        idx = decode(e)
        new, t = remove_spots(idx, e["palette"], spots)
        report.append((key, t))
        pairs.append((key, e, idx, new))
        if write: e["rle"] = encode(new, len(e["palette"]) > 26)
    print(f"{len(report)} 体で目を消した:", ", ".join(f"{k[6:]}({t}か所)" for k, t in report))
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
