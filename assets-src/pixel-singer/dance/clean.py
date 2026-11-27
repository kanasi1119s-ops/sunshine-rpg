"""読み取ったマス目（build.py の出力 sheet.json）から、まわりの灰色のにじみを消す → sheet2.json（= 4方向の読み取り.json）。
にじみ: 白っぽい灰色（あざやかさ 0.22 未満・明るさ 0.42〜0.9）で、背景にとなり、反対がわ（内がわ）のとなりが白っぽくないマス。
  シャツやくつ下のふち（内がわも白っぽい）は消さない。3回くり返し、そのあと1マスだけ飛び出した点を消す。"""
import json, colorsys
d = json.load(open('/tmp/px5/sheet.json')); pal = d['pal']
rgb = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in pal.items()}
HL = {k: colorsys.rgb_to_hls(*(c / 255 for c in v)) for k, v in rgb.items()}
def greyish(ch): h, l, s = HL[ch]; return s < 0.22 and 0.42 < l < 0.9
def whiteish(ch): h, l, s = HL[ch]; return s < 0.25 and l > 0.55
out = []
for rows in d['grids']:
    G = [list(r) for r in rows]; H = len(G); W = len(G[0])
    for it in range(3):
        kill = []
        for y in range(H):
            for x in range(W):
                ch = G[y][x]
                if ch == "." or not greyish(ch): continue
                for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ox, oy = x + a, y + b
                    if not (0 <= ox < W and 0 <= oy < H) or G[oy][ox] == ".":
                        ix, iy = x - a, y - b
                        if 0 <= ix < W and 0 <= iy < H and G[iy][ix] != "." and not whiteish(G[iy][ix]): kill.append((x, y)); break
        for x, y in kill: G[y][x] = "."
    for y in range(H):
        for x in range(W):
            if G[y][x] != "." and sum(1 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < W and 0 <= y + b < H and G[y + b][x + a] != ".") <= 1: G[y][x] = "."
    out.append(["".join(r) for r in G])
d['grids'] = out; json.dump(d, open('/tmp/px5/sheet2.json', 'w'), ensure_ascii=False)
