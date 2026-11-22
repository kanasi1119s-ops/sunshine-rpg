"""もらった絵のキャラクター（赤い縦ロール）の歌い手 32×48。口の形 6 つ＋まばたきの 7 コマ。
形を部品ごとに置き、かげ・光・ふち取りを付けて、ドット絵エディタ用の JSON とシート画像を書き出す。"""
import json, sys, math
from PIL import Image
OUT = sys.argv[1]; W, H = 32, 48
C = dict(O="#1a1018", hD="#8f1024", hM="#b8172a", hB="#dd1f2a", hL="#f56a72", hH="#ffc2bd", sB="#ffdcc8", sD="#eba98c", bl="#ff9d9d",
         eD="#0f5f6a", eB="#1b9c9c", eL="#5fe0d0", wB="#f6f2f6", wD="#c9bfd4", nB="#283762", nD="#18213f", nL="#3f5796",
         rB="#c7202c", rD="#7e1126", rL="#e8505a", kB="#2a1c27", kL="#4a3a4c", go="#e9b93c", mD="#7a1a2a", to="#ff8a94")
def build(mouth, blink):
    col = [[None] * W for _ in range(H)]; part = [[None] * W for _ in range(H)]
    def p(x, y, c, pt=None):
        if 0 <= x < W and 0 <= y < H:
            col[y][x] = c
            if pt: part[y][x] = pt
    # 縦ロール（うしろ）
    for side, cx in ((1, 4), (-1, 27)):
        for y in range(12, 40):
            hw = 3 if y <= 28 else 2 if y <= 33 else 1 if y <= 37 else 0
            for x in range(cx - hw, cx + hw + 1):
                if (y - 12) % 4 == 3 and x == cx - hw * side and hw > 0: continue      # 外がわのくびれ
                t = (y - 12 + (x - cx) * side) % 4
                p(x, y, ("hL", "hB", "hM", "hD")[t], "drill")
    # 足・くつ
    for x0 in (11, 17):
        for y in range(41, 45):
            for x in range(x0, x0 + 4): p(x, y, "wD" if x == x0 + 3 else "wB", "leg")
    for x0 in (10, 17):
        for y in (45, 46):
            for x in range(x0, x0 + 5): p(x, y, "kB", "leg")
    p(11, 45, "kL"); p(18, 45, "kL")
    # うで・手
    for xs in ((7, 8, 9), (22, 23, 24)):
        for y in range(26, 33):
            for x in xs: p(x, y, "wB" if y == 32 else ("nL" if x == 7 else "nD" if x == 24 else "nB"), "arm")
    for x in (7, 8, 23, 24):
        for y in (33, 34): p(x, y, "sD" if y == 34 else "sB", "arm")
    # スカート
    hw = {33: 6.5, 34: 7.5, 35: 8, 36: 8.5, 37: 9, 38: 9.5, 39: 10, 40: 10}
    for y, h in hw.items():
        for x in range(W):
            if abs(x - 15.5) <= h:
                c = "rB"
                if y == 39: c = "kB"
                elif y == 40:
                    if x % 3 == 0: continue
                    c = "wB"
                elif x in (10, 14, 17, 21) and y >= 35: c = "rD"
                elif x in (8, 12) and 34 <= y <= 37 or (y == 33 and x < 15): c = "rL"
                elif x >= 23: c = "rD"
                p(x, y, c, "skirt")
    # 上着
    for y in range(25, 33):
        for x in range(10, 22):
            c = "nB"
            if x == 10: c = "nL"
            if x == 21 or y == 31: c = "nD"
            if y == 32: c = "wB" if x % 2 else "wD"
            p(x, y, c, "body")
    for x in range(12, 20): p(x, 25, "wB" if x % 2 == 0 else "wD")
    for x, y, c in ((14, 26, "rB"), (15, 26, "rD"), (16, 26, "rD"), (17, 26, "rB"), (13, 26, "rL"), (18, 26, "rB"), (14, 27, "rB"), (17, 27, "rD"),
                    (15, 27, "rL"), (16, 27, "rB"), (15, 28, "rD"), (16, 28, "rD"), (15, 30, "go"), (16, 30, "go")): p(x, y, c)
    for x in (14, 15, 16, 17): p(x, 24, "sD", "neck")
    # 頭（かみ）と顔
    for y in range(3, 23):
        for x in range(W):
            if ((x - 15.5) / 10.2) ** 2 + ((y - 12.5) / 10) ** 2 <= 1: p(x, y, "hB", "head")
    for x, yb in ((6, 18), (7, 20), (8, 21), (25, 18), (24, 20), (23, 21)):
        for y in range(12, yb + 1): p(x, y, "hD" if y == yb else "hM" if x >= 23 else "hB", "head")
    fr = {9: 16, 10: 14, 11: 13, 12: 14, 13: 14, 14: 13, 15: 12, 16: 13, 17: 14, 18: 13, 19: 13, 20: 14, 21: 14, 22: 16}
    for y in range(12, 24):
        for x in range(9, 23):
            if ((x - 15.5) / 7.4) ** 2 + ((y - 16) / 7.6) ** 2 <= 1 and y > fr[x]:
                p(x, y, "sD" if y == fr[x] + 1 or (x == 22) else "sB", "head")
    for x in range(W):                                             # かみの右はしのかげ
        for y in range(3, 23):
            if col[y][x] in ("hB", "hM") and part[y][x] == "head":
                e = [k for k in (1, 2, 3) if x + k >= W or part[y][x + k] != "head"]
                if e and y > 5: col[y][x] = "hD" if e[0] == 1 else "hM"
    for x, y in [(x, 6) for x in (9, 10, 11, 12, 13, 17, 18, 19, 20)] + [(8, 7), (9, 7), (10, 7), (20, 7), (21, 7), (11, 5), (12, 5)]: p(x, y, "hL")
    for x, y in ((10, 5), (11, 6), (12, 6)): p(x, y, "hH")
    for x, y in ((13, 11), (13, 12), (13, 13), (18, 10), (18, 11), (18, 12), (10, 12), (10, 13), (21, 12), (21, 13), (15, 4), (15, 5), (16, 6), (16, 7)): p(x, y, "hD")
    # あほ毛
    for x, y, c in ((15, 2, "hB"), (14, 1, "hB"), (13, 1, "hL"), (12, 2, "hB"), (16, 2, "hD")): p(x, y, c, "head")
    # しまのリボン
    for x, y, c in ((20, 2, "nB"), (21, 2, "wB"), (22, 3, "nB"), (21, 3, "nB"), (20, 3, "wB"), (23, 2, "wB"), (24, 2, "nB"), (23, 3, "wB"), (24, 3, "wB"), (25, 3, "nB"),
                    (21, 4, "wB"), (22, 4, "nD"), (23, 4, "nB"), (24, 4, "wB"), (25, 4, "nB"), (22, 5, "nB"), (24, 5, "nB"), (25, 5, "wD"), (20, 4, "nB")): p(x, y, c, "ribbon")
    # 目
    for x0 in (10, 19):
        if blink:
            for x in range(x0, x0 + 3): p(x, 18, "O")
            p(x0 - 1 if x0 == 10 else x0 + 3, 17, "O")
        else:
            for x in range(x0, x0 + 3): p(x, 15, "O"); p(x, 16, "eD"); p(x, 17, "eD"); p(x, 18, "eB"); p(x, 19, "eL")
            p(x0, 16, "wB"); p(x0 + 1, 17, "eB"); p(x0 + 2, 18, "eL"); p(x0 - 1 if x0 == 10 else x0 + 3, 16, "O")
    for x in (10, 11, 20, 21): p(x, 21, "bl")
    # 口
    M = {"closed": [(15, 21, "mD"), (16, 21, "mD"), (14, 20, "sD"), (17, 20, "sD")],
         "a": [(x, 20, "mD") for x in (14, 15, 16, 17)] + [(14, 21, "mD"), (15, 21, "to"), (16, 21, "to"), (17, 21, "mD"), (15, 22, "mD"), (16, 22, "mD")],
         "i": [(13, 20, "mD"), (18, 20, "mD")] + [(x, 20, "wB") for x in (14, 15, 16, 17)] + [(x, 21, "mD") for x in (14, 15, 16, 17)],
         "u": [(15, 20, "mD"), (16, 20, "mD"), (15, 21, "mD"), (16, 21, "mD")],
         "e": [(14, 20, "mD"), (15, 20, "wB"), (16, 20, "wB"), (17, 20, "mD"), (14, 21, "mD"), (15, 21, "to"), (16, 21, "to"), (17, 21, "mD")],
         "o": [(15, 20, "mD"), (16, 20, "mD"), (14, 21, "mD"), (15, 21, "mD"), (16, 21, "mD"), (17, 21, "mD"), (15, 22, "to"), (16, 22, "to")]}
    for x, y, c in M[mouth]: p(x, y, c)
    # 部品のさかい目と、まわりのふち取り
    n4 = ((1, 0), (-1, 0), (0, 1), (0, -1)); add = []
    for y in range(H):
        for x in range(W):
            for dx, dy in n4:
                X, Y = x + dx, y + dy
                if not (0 <= X < W and 0 <= Y < H): continue
                if part[y][x] == "drill" and part[Y][X] not in (None, "drill"): add.append((x, y, "O"))
                if part[y][x] == "arm" and part[Y][X] == "body" and col[y][x] != "wB": add.append((x, y, "nD"))
                if col[y][x] is None and col[Y][X] is not None: add.append((x, y, "O"))
    for x, y, c in add: col[y][x] = c
    return col
FR = [("closed", False, 400), ("a", False, 200), ("i", False, 200), ("u", False, 200), ("e", False, 200), ("o", False, 200), ("closed", True, 150)]
grids = [build(m, b) for m, b, _ in FR]
keys = sorted({c for g in grids for r in g for c in r if c}); S = {k: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"[i] for i, k in enumerate(keys)}
cels = [["".join(S[c] if c else "." for c in r) for r in g] for g in grids]
name = "縦ロールの歌い手_32x48"
json.dump({"format": "sunshine-pixel", "version": 2, "width": W, "height": H, "symbols": [{"sym": S[k], "label": k, "color": C[k]} for k in keys],
           "layers": [{"name": "歌い手", "visible": True, "opacity": 1}], "frames": [{"dur": d} for *_, d in FR], "cels": [cels], "layer": 0, "frame": 0},
          open(f"{OUT}/{name}.sunshine-pixel.json", "w", encoding="utf-8"), ensure_ascii=False)
def img(g, z):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            if g[y][x]: h = C[g[y][x]]; im.putpixel((x, y), (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255))
    return im.resize((W * z, H * z), Image.NEAREST)
z = 10; sheet = Image.new("RGBA", (W * z * 7, H * z), (88, 94, 108, 255)); raw = Image.new("RGBA", (W * 7, H), (0, 0, 0, 0)); fs = []
for i, g in enumerate(grids):
    sheet.alpha_composite(img(g, z), (i * W * z, 0)); raw.alpha_composite(img(g, 1), (i * W, 0))
    f = Image.new("RGBA", (W * z, H * z), (88, 94, 108, 255)); f.alpha_composite(img(g, z)); fs.append(f.convert("P", palette=Image.ADAPTIVE))
sheet.save(f"{OUT}/{name}_確認用（口の形7コマ）.png"); raw.save(f"{OUT}/{name}_シート（等倍・透明）.png")
seq = [0, 1, 0, 3, 5, 1, 2, 4, 1, 0, 6, 0, 5, 3, 1, 0]
fs[0].save(f"{OUT}/{name}_歌っている見本.gif", save_all=True, append_images=[fs[i] for i in seq[1:]], duration=[120 if i == 6 else 180 for i in seq], loop=0)
print(len(keys), "色")
