"""家財（家の中の家具）に、樽と同じ「実物感」の仕上げをかける（2026-10-06、人間の指示「家屋も樽みたいにリアルにしよう」→「家財も同じように使用」）。
樽（props3d_a.py の barrel）の実物感は、次の3つから来ている。それを、できあがった家具の絵に、あとからかける。
  1. つや: 見る向きと光の向きのあいだの向きで、面がやわらかく光る。木の家具はニスのつや。
     左上から右下へななめにかかる、やわらかいつやの帯（帯の中は少し明るく、ふちは市松でぼかす）
  2. するどい光の点: 金具（真ちゅう・鉄）・陶器・ガラスの、いちばん明るい所の左上に、白に近い光の点
  3. ふちの暗さ: 形の右下のふちのすぐ内がわは、光がまわりこまず、少し暗い
色の数がエディタの記号の数（62）をこえたら、近い色をまとめる（restyle.py の merge_colors）。
使い方: python3 gloss.py 名前...（../r20-props/<名前>.txt を上書き。restyle.py --apply のあとに1回だけ）"""
import colorsys
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from restyle import merge_colors, hx, to_hex, luma

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")


def hls(c):
    return colorsys.rgb_to_hls(*hx(c))


def kind(c):
    """色から材質をおおまかに決める: wood（茶色）・metal（真ちゅうの黄・鉄の灰）・shiny（陶器・ガラス・白い布より明るい所）・other。"""
    h, l, s = hls(c)
    if 0.03 <= h <= 0.13 and s > 0.25 and 0.12 < l < 0.75:
        return "wood"
    if 0.11 <= h <= 0.17 and s > 0.55 and l > 0.45:
        return "metal"                                        # 真ちゅう・金
    if s < 0.18 and 0.25 < l < 0.6:
        return "metal"                                        # 鉄
    if l > 0.72:
        return "shiny"                                        # 陶器・ガラス・紙の明るい所
    return "other"


def lighter(c, dl):
    h, l, s = hls(c)
    if dl > 0:
        h = h + (0.13 - h) * 0.1 if s > 0.15 else h          # 光の側は少し黄色寄り
    return to_hex(colorsys.hls_to_rgb(h % 1.0, max(0.02, min(0.97, l + dl)), s))


def gloss(img):
    H, W = len(img), len(img[0])
    solid = lambda x, y: 0 <= x < W and 0 <= y < H and img[y][x] and len(img[y][x]) == 7
    pts = [(x, y) for y in range(H) for x in range(W) if solid(x, y)]
    if not pts:
        return img
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    out = [r[:] for r in img]
    for x, y in pts:
        c = img[y][x]
        k = kind(c)
        fx = (x - x0) / max(1, x1 - x0)
        fy = (y - y0) / max(1, y1 - y0)
        edge_rb = not solid(x + 1, y) or not solid(x, y + 1)
        # 3) ふちの暗さ（右下のふちのすぐ内がわ。りんかくそのものはさわらない）
        inner_rb = not edge_rb and (not solid(x + 2, y) or not solid(x, y + 2))
        if inner_rb and luma(hx(c)) > 0.2 and k != "shiny":
            out[y][x] = lighter(c, -0.05)
            continue
        if edge_rb:
            continue
        # 1) 木のニスのつやの帯
        if k == "wood":
            d = abs((fx - 0.3) + (fy - 0.5) * 0.45)
            if d < 0.06 or (d < 0.1 and (x + y) % 2 == 0):
                out[y][x] = lighter(c, 0.07)
        # 2) 金具・陶器・ガラスの、するどい光の点（明るい所で、左上がそれより暗いか、すき間のとき）
        elif k in ("metal", "shiny"):
            l = hls(c)[1]
            up = img[y - 1][x] if y > 0 else ""
            lf = img[y][x - 1] if x > 0 else ""
            dark = lambda n: not n or len(n) != 7 or hls(n)[1] < l - 0.05
            # 明るい所の、左上のすみだけ（左も上も暗い）。目地のような細長い明るい線は光らせない
            if l > 0.55 and dark(up) and dark(lf):
                out[y][x] = "#fbf8ee" if k == "shiny" else lighter(c, 0.22)
    return out


def run(name):
    rows = [l for l in open(os.path.join(R20, name + ".txt")).read().split("\n") if l]
    pal = json.load(open(os.path.join(R20, "pal-" + name + ".json")))
    img = [[pal[ch] if ch != "." else "" for ch in r] for r in rows]
    img = merge_colors(gloss(img))
    cols = sorted({c for r in img for c in r if c})
    syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    cmap = {c: syms[i] for i, c in enumerate(cols)}
    open(os.path.join(R20, name + ".txt"), "w").write("\n".join("".join(cmap[c] if c else "." for c in r) for r in img) + "\n")
    json.dump({cmap[c]: c for c in cols}, open(os.path.join(R20, "pal-" + name + ".json"), "w"))
    print(name, len(cols), "colors")


if __name__ == "__main__":
    for n in sys.argv[1:]:
        run(n)
