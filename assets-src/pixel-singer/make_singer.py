"""オリジナルのドット絵の歌い手（Sunshine Pixel Sound 用）。32×32 と 64×64。口の形 6 つ＋まばたき。ドット絵エディタで開ける JSON と、確認用の PNG・GIF を出す。"""
import json, sys
from PIL import Image
PAL = [(".", "透明", None), ("o", "ふち", "#1b2233"), ("H", "髪", "#1f8a8a"), ("h", "髪の影", "#14605f"), ("L", "髪の光", "#5fd0c4"),
       ("S", "肌", "#ffe0c4"), ("s", "肌の影", "#f2b79a"), ("E", "目", "#c9741a"), ("e", "目の上", "#5a2d0c"), ("W", "白", "#ffffff"),
       ("P", "ほお", "#ff9aa2"), ("M", "口の中", "#a8323e"), ("T", "舌", "#ff7b86"), ("C", "パーカー", "#fff3d6"), ("c", "パーカーの影", "#e6d2a8"),
       ("O", "だいだい", "#ff8a1f"), ("N", "ズボン", "#2b3a67"), ("G", "マイク", "#9aa3b2"), ("g", "マイクの頭", "#4a5263"), ("Y", "髪かざり", "#ffd23f")]
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
    # 体
    put(rect(12, 27.5, 15, 30), "S"); put(rect(17, 27.5, 20, 30), "S")          # 足
    put(rect(11.5, 30, 15.2, 31), "O"); put(rect(16.8, 30, 20.5, 31), "O")      # くつ
    put(rect(11, 25, 21, 28), "N")                                              # ズボン
    put(rect(10.5, 18.5, 21.5, 25.6), "C"); put(rect(10.5, 22.3, 21.5, 23.4), "O"); put(rect(10.5, 24.6, 21.5, 25.6), "c")
    put(rect(8.3, 19, 10.6, 25), "C"); put(rect(8.3, 24, 10.6, 25), "c"); put(ell(9.4, 25.6, 1.2, 1.1), "S")          # 左うで（下げる）
    put(rect(21.4, 19, 23.7, 23.2), "C"); put(rect(21.4, 22.2, 23.7, 23.2), "c")                                      # 右うで（ひじを曲げて、胸の前でマイクを持つ）
    put(rect(14.3, 17.6, 17.7, 19.2), "s")                                      # 首
    # 頭
    put(ell(16, 10.6, 9.4, 8.9), "H")                                            # 髪（うしろ）
    put(rect(6.8, 10, 9.6, 18.6), "H"); put(rect(22.4, 10, 25.2, 18.6), "H")     # 横の髪（あごの下まで）
    put(rect(6.8, 17.4, 9.6, 18.6), "h"); put(rect(22.4, 17.4, 25.2, 18.6), "h")
    put(ell(16, 12.6, 7.1, 6.6), "S")                                            # 顔
    put(both(ell(16, 12.6, 7.1, 6.6), rect(0, 17.6, 32, 20)), "s")
    put(lambda x, y: ell(16, 9.2, 8.2, 5.2)(x, y) and y < 10.4 + 1.1 * (abs(((x - 9) % 3.5) - 1.75) / 1.75), "H")      # 前髪（ぎざぎざ）
    put(lambda x, y: ell(16, 6.4, 6.5, 2.2)(x, y) and y < 6.2, "L")              # 髪の光
    put(lambda x, y: ell(16, 10.6, 9.4, 8.9)(x, y) and y > 14 and not ell(16, 12.6, 7.1, 6.6)(x, y) and (x < 8 or x > 24), "h")
    # ヘッドホン
    put(lambda x, y: ell(16, 10.4, 10.6, 9.9)(x, y) and not ell(16, 10.6, 9.7, 9.0)(x, y) and y < 9, "W")
    put(ell(6.2, 12.6, 2.2, 2.9), "O"); put(ell(25.8, 12.6, 2.2, 2.9), "O"); put(ell(6.2, 12.6, 1.0, 1.6), "W"); put(ell(25.8, 12.6, 1.0, 1.6), "W")
    # 髪かざり（小さなお日さま）
    put(ell(21.2, 6.3, 1.5, 1.5), "Y"); put(ell(21.2, 6.3, 0.7, 0.7), "O")
    # 目
    for cx in (12.6, 19.4):
        if blink: put(rect(cx - 1.5, 13.4, cx + 1.5, 14.0), "e")
        else:
            put(ell(cx, 13.2, 1.45, 1.9), "E"); put(both(ell(cx, 13.2, 1.45, 1.9), rect(0, 0, 32, 12.05)), "e")
            put(rect(cx - 1.0, 12.4, cx - 0.2, 13.3) if R >= 64 else rect(cx - 1.0, 12.0, cx, 13.0), "W")
    put(ell(10.4, 15.6, 1.3, 0.7), "P"); put(ell(21.6, 15.6, 1.3, 0.7), "P")      # ほお
    # マイク（頭を描いたあとに、胸の前へ）
    put(rect(18.4, 21.6, 22.6, 23.4), "C"); put(ell(18.9, 21.6, 1.25, 1.2), "S")
    put(rect(18.4, 19.6, 19.5, 21.0), "G"); put(ell(18.95, 18.9, 1.3, 1.3), "g")
    # 口
    if mouth == "closed": put(rect(15.0, 16.3, 17.0, 16.8), "M")
    elif mouth == "a": put(ell(16, 16.7, 1.7, 1.5), "M"); put(both(ell(16, 16.7, 1.7, 1.5), rect(0, 17.2, 32, 32)), "T")
    elif mouth == "i": put(rect(14.2, 16.2, 17.8, 17.2), "M"); put(rect(14.6, 16.2, 17.4, 16.7), "W")
    elif mouth == "u": put(ell(16, 16.6, 0.8, 0.9), "M")
    elif mouth == "e": put(ell(16, 16.7, 1.9, 1.0), "M"); put(both(ell(16, 16.7, 1.9, 1.0), rect(0, 0, 32, 16.5)), "W")
    elif mouth == "o": put(ell(16, 16.8, 1.1, 1.5), "M")
    # ふち（外がわを1ドット、こい紺でかこむ）
    out = [r[:] for r in g]
    for y in range(R):
        for x in range(R):
            if g[y][x] == "." and any(0 <= y + dy < R and 0 <= x + dx < R and g[y + dy][x + dx] != "." for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): out[y][x] = "o"
    return ["".join(r) for r in out]

FR = [("closed", False, 400), ("a", False, 200), ("i", False, 200), ("u", False, 200), ("e", False, 200), ("o", False, 200), ("closed", True, 150)]
NAMES = ["とじる", "あ", "い", "う", "え", "お", "まばたき"]
def img(rows, z):
    R = len(rows); im = Image.new("RGBA", (R, R), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if COL[ch]: c = COL[ch]; im.putpixel((x, y), (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), 255))
    return im.resize((R * z, R * z), Image.NEAREST)
OUT = sys.argv[1]
for R in (64, 32):
    cels = [draw(R, m, b) for m, b, _ in FR]
    json.dump({"format": "sunshine-pixel", "version": 2, "width": R, "height": R, "symbols": [{"sym": s, "label": l, "color": c} for s, l, c in PAL if c],
               "layers": [{"name": "歌い手", "visible": True, "opacity": 1}], "frames": [{"dur": d} for _, _, d in FR], "cels": [cels], "layer": 0, "frame": 0},
              open(f"{OUT}/歌い手_{R}.sunshine-pixel.json", "w", encoding="utf-8"), ensure_ascii=False)
    z = 512 // R; sheet = Image.new("RGBA", (R * z * 7, R * z), (40, 44, 60, 255))
    for i, c in enumerate(cels): sheet.alpha_composite(img(c, z), (i * R * z, 0))
    sheet.save(f"{OUT}/歌い手_{R}_確認用（口の形7コマ）.png")
    raw = Image.new("RGBA", (R * 7, R), (0, 0, 0, 0))
    for i, c in enumerate(cels): raw.alpha_composite(img(c, 1), (i * R, 0))
    raw.save(f"{OUT}/歌い手_{R}_シート（等倍・透明）.png")
print("ok")
