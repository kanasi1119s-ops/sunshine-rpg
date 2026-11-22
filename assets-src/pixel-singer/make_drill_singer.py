"""もらった絵のキャラクター（赤い髪・長い縦ロールのツインテール・紺の上着・赤いフリルのスカート）のドット絵。32×32 と 64×64。口の形 6 つ＋まばたき。
ドット絵エディタで開ける JSON と、確認用の PNG・動画用のシートを出す。"""
import json, sys, math
from PIL import Image
PAL = [(".", "透明", None), ("o", "ふち", "#2a1420"), ("H", "髪", "#e3222c"), ("h", "髪の影", "#a8121f"), ("L", "髪の光", "#ff6f61"),
       ("S", "肌", "#ffe4d0"), ("s", "肌の影", "#f4bfa6"), ("E", "目", "#2fb8b2"), ("e", "目の上", "#14505c"), ("W", "白", "#ffffff"),
       ("P", "ほお", "#ff9aa2"), ("M", "口の中", "#a8323e"), ("T", "舌", "#ff7b86"), ("N", "上着（紺）", "#27365f"), ("n", "上着の影", "#19233f"),
       ("R", "スカート（赤）", "#c9212d"), ("r", "スカートの影", "#8e1420"), ("K", "黒いフリル", "#2e1b25"), ("F", "レース", "#f3e7e2"), ("B", "リボン（赤）", "#e8323a")]
COL = {s: c for s, _, c in PAL}

def draw(R, mouth="closed", blink=False):
    k = R / 32.0; g = [["."] * R for _ in range(R)]
    def put(fn, sym):
        for y in range(R):
            for x in range(R):
                if fn((x + 0.5) / k, (y + 0.5) / k): g[y][x] = sym
    ell = lambda cx, cy, rx, ry: (lambda x, y: ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1)
    rect = lambda x0, y0, x1, y1: (lambda x, y: x0 <= x < x1 and y0 <= y < y1)
    both = lambda a, b: (lambda x, y: a(x, y) and b(x, y))
    # 縦ロールのツインテール（うしろ。上から下へ、少しずつ細く。1巻きごとに明るい・暗いを交互に）
    for side in (-1, 1):
        for j in range(8):
            cy = 8.2 + j * 2.35; cx = 16 + side * (9.6 + 0.5 * math.sin(j * 1.3)); rx = 2.75 - j * 0.13; ry = 1.55
            put(ell(cx, cy, rx, ry), "H" if j % 2 == 0 else "h")
            put(both(ell(cx, cy, rx, ry), lambda x, y, cx=cx, cy=cy, side=side: y < cy - 0.5 and (x - cx) * side < 0.6), "L" if j % 2 == 0 else "H")
        put(ell(16 + side * 9.9, 27.3, 1.1, 0.9), "h")
    # 足・くつ
    put(rect(13.0, 25.5, 15.3, 29.6), "W"); put(rect(16.7, 25.5, 19.0, 29.6), "W"); put(rect(13.0, 28.8, 15.3, 29.6), "F"); put(rect(16.7, 28.8, 19.0, 29.6), "F")
    put(rect(12.4, 29.6, 15.6, 31), "K"); put(rect(16.4, 29.6, 19.6, 31), "K")
    # スカート（赤・黒いフリル・赤・白いレース）
    sk = lambda y0, y1: (lambda x, y: y0 <= y < y1 and abs(x - 16) <= 3.6 + (y - 19.5) * 0.62)
    put(sk(19.5, 26.2), "R"); put(sk(21.6, 22.6), "K"); put(sk(23.9, 24.9), "K"); put(sk(24.9, 25.6), "r"); put(sk(25.6, 26.4), "F")
    put(lambda x, y: sk(19.5, 26.4)(x, y) and abs(x - 16) > 2.2 + (y - 19.5) * 0.62 and g[min(R - 1, int(y * k))][min(R - 1, int(x * k))] == "R", "r")
    # 上着（紺）・白いフリルの前・赤いリボン
    put(rect(12.0, 16.0, 20.0, 20.4), "N"); put(rect(14.6, 16.6, 17.4, 20.4), "W"); put(rect(15.6, 17.4, 16.4, 20.4), "F")
    put(rect(12.0, 19.5, 20.0, 20.4), "n")
    put(lambda x, y: 10.2 <= x < 12.3 and 16.3 <= y < 20.6, "N"); put(lambda x, y: 19.7 <= x < 21.8 and 16.3 <= y < 20.6, "N")     # そで
    put(lambda x, y: 11.6 <= x < 20.4 and 19.6 <= y < 21.2 and abs(x - 16) > 1.6, "N")                                             # 前で手を組む
    put(rect(11.4, 20.9, 14.6, 21.5), "F"); put(rect(17.4, 20.9, 20.6, 21.5), "F")
    put(ell(16, 20.9, 1.7, 1.0), "S")
    put(rect(14.4, 15.5, 17.6, 16.6), "s")                                       # 首
    put(ell(14.9, 16.7, 1.2, 0.8), "B"); put(ell(17.1, 16.7, 1.2, 0.8), "B"); put(rect(15.6, 16.3, 16.4, 17.5), "r")
    # 頭
    put(ell(16, 8.9, 7.5, 7.1), "H")
    put(ell(16, 10.6, 5.7, 5.2), "S"); put(both(ell(16, 10.6, 5.7, 5.2), rect(0, 14.8, 32, 17)), "s")
    put(lambda x, y: ell(16, 7.6, 6.8, 4.6)(x, y) and y < 8.0 + 1.0 * (abs(((x - 9.6) % 3.2) - 1.6) / 1.6), "H")                  # 前髪
    put(lambda x, y: ell(16, 8.9, 7.5, 7.1)(x, y) and not ell(16, 10.6, 5.7, 5.2)(x, y) and y > 9.5 and abs(x - 16) < 7.2 and abs(x - 16) > 5.2, "h")   # 顔の横の髪
    put(lambda x, y: ell(16, 4.6, 5.0, 1.7)(x, y) and y < 4.5, "L")
    put(lambda x, y: (x - 15.2) ** 2 + (y - 1.9) ** 2 <= 1.5 ** 2 and (x - 14.6) ** 2 + (y - 2.4) ** 2 > 1.1 ** 2, "H")           # あほ毛
    # 頭のリボン（紺と白のしま）
    put(ell(21.6, 4.2, 2.1, 1.7), "N"); put(lambda x, y: ell(21.6, 4.2, 2.1, 1.7)(x, y) and int((x + y) * (1.2 if R >= 64 else 0.8)) % 2 == 0, "W"); put(ell(21.0, 4.6, 0.7, 0.7), "n")
    # 目
    for cx in (13.3, 18.7):
        if blink: put(rect(cx - 1.4, 11.6, cx + 1.4, 12.2) if R >= 64 else rect(cx - 1.3, 11.0, cx + 1.3, 12.0), "e")
        else:
            if R >= 64:
                put(ell(cx, 11.4, 1.35, 1.75), "E"); put(both(ell(cx, 11.4, 1.35, 1.75), rect(0, 0, 32, 10.55)), "e"); put(rect(cx - 0.9, 10.6, cx - 0.1, 11.5), "W")
            else:                                                                # 32×32: 目は横2・縦3ドット（上の1段がまつげ、左上に光を1ドット）
                x0 = round(cx - 1.0); put(rect(x0, 10, x0 + 2, 13), "E"); put(rect(x0, 10, x0 + 2, 11), "e"); put(rect(x0, 11, x0 + 1, 12), "W")
    put(ell(11.6, 13.6, 1.1, 0.6), "P"); put(ell(20.4, 13.6, 1.1, 0.6), "P")
    # 口
    my = 14.3
    if mouth == "closed": put(rect(15.1, my - 0.2, 16.9, my + 0.3), "M")
    elif mouth == "a": put(ell(16, my + 0.2, 1.5, 1.3), "M"); put(both(ell(16, my + 0.2, 1.5, 1.3), rect(0, my + 0.7, 32, 32)), "T")
    elif mouth == "i": put(rect(14.4, my - 0.3, 17.6, my + 0.6), "M"); put(rect(14.8, my - 0.3, 17.2, my + 0.15), "W")
    elif mouth == "u": put(ell(16, my + 0.1, 0.75, 0.8), "M")
    elif mouth == "e": put(ell(16, my + 0.2, 1.7, 0.9), "M"); put(both(ell(16, my + 0.2, 1.7, 0.9), rect(0, 0, 32, my)), "W")
    elif mouth == "o": put(ell(16, my + 0.3, 1.0, 1.3), "M")
    out = [r[:] for r in g]
    for y in range(R):
        for x in range(R):
            if g[y][x] == "." and any(0 <= y + dy < R and 0 <= x + dx < R and g[y + dy][x + dx] != "." for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y][x] = "o"
    return ["".join(r) for r in out]

FR = [("closed", False, 400), ("a", False, 200), ("i", False, 200), ("u", False, 200), ("e", False, 200), ("o", False, 200), ("closed", True, 150)]
def img(rows, z):
    R = len(rows); im = Image.new("RGBA", (R, R), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if COL[ch]: c = COL[ch]; im.putpixel((x, y), (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255))
    return im.resize((R * z, R * z), Image.NEAREST)
OUT = sys.argv[1]; NAME = "縦ロールの歌い手"
for R in (64, 32):
    cels = [draw(R, m, b) for m, b, _ in FR]
    json.dump({"format": "sunshine-pixel", "version": 2, "width": R, "height": R, "symbols": [{"sym": s, "label": l, "color": c} for s, l, c in PAL if c],
               "layers": [{"name": "歌い手", "visible": True, "opacity": 1}], "frames": [{"dur": d} for _, _, d in FR], "cels": [cels], "layer": 0, "frame": 0},
              open(f"{OUT}/{NAME}_{R}.sunshine-pixel.json", "w", encoding="utf-8"), ensure_ascii=False)
    z = 512 // R; sheet = Image.new("RGBA", (R * z * 7, R * z), (236, 236, 240, 255))
    for i, c in enumerate(cels): sheet.alpha_composite(img(c, z), (i * R * z, 0))
    sheet.save(f"{OUT}/{NAME}_{R}_確認用（口の形7コマ）.png")
    raw = Image.new("RGBA", (R * 7, R), (0, 0, 0, 0))
    for i, c in enumerate(cels): raw.alpha_composite(img(c, 1), (i * R, 0))
    raw.save(f"{OUT}/{NAME}_{R}_シート（等倍・透明）.png")
print("ok")
