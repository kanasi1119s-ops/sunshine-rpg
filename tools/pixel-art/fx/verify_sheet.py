"""エディタが書き出したシート（PNG）が、エフェクトのコマと1マスもちがわないか確かめる。
使い方: python3 verify_sheet.py エフェクト.json シート.png"""
import json, sys, numpy as np
from PIL import Image
fx = json.load(open(sys.argv[1])); sh = np.array(Image.open(sys.argv[2]).convert("RGBA"))
W, H = fx["w"], fx["h"]; bad = 0
for k, f in enumerate(fx["frames"]):
    exp = np.zeros((H, W, 4), np.uint8)
    layers = ([(f["back"], f["bx"], f["by"])] if f.get("back") else []) + [(f["rows"], f["x"], f["y"])]
    for rows, ox, oy in layers:     # うしろ → 手前の順に重ねる
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c != ".":
                    v = fx["palette"][c]; exp[oy + y, ox + x] = [int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16), 255]
    got = sh[:, k * W:(k + 1) * W]
    m = (exp[..., 3] > 0) != (got[..., 3] > 0)
    m |= (exp[..., 3] > 0) & (np.abs(exp[..., :3].astype(int) - got[..., :3]).sum(2) > 6)
    bad += int(m.sum())
print(fx["name"], "食い違い", bad, "マス")
