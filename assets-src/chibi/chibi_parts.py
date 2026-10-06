"""2頭身の歩くキャラ（16×32・4方向×3コマ）に、羽・角・光輪・耳・しっぽ・マントを描き足す道具（2026-10-07）。
もとの体は仲間の2頭身の絵（assets-src/characters/walk-2head/*.json）。色を塗り替えたうえで、ここの部品を「透明な所だけ」に描き足す。"""
import json, pathlib
from PIL import Image

L = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
WALK = pathlib.Path(__file__).resolve().parents[1] / "characters" / "walk-2head"
ORDER = ["down", "up", "left", "right"]


class Chibi:
    def __init__(self, base):
        d = json.load(open(WALK / f"{base}.json"))
        self.pal = list(d["palette"])
        self.frames = {k: [list(r) for r in v] for k, v in d["frames"].items()
                       if k[:-1] in ORDER and k[-1] in "012"}

    def color(self, ch, hexv):
        self.pal[L.index(ch)] = hexv

    def new(self, hexv):
        self.pal.append(hexv)
        return L[len(self.pal) - 1]

    def put(self, g, y, x, c, over=False):
        if 0 <= y < 32 and 0 <= x < 16 and (over or g[y][x] == "."):
            g[y][x] = c

    def head_top(self, g):
        return next(y for y, r in enumerate(g) if any(c != "." for c in r))

    def head_center(self, g):
        y = self.head_top(g)
        y2 = y + 2
        xs = [x for x, c in enumerate(g[y2]) if c != "."]
        return y, (min(xs) + max(xs)) / 2

    def edges(self, g, y):
        xs = [x for x, c in enumerate(g[y]) if c != "."]
        return (min(xs), max(xs)) if xs else (None, None)

    # --- 部品 ---
    def wings(self, rows, inner, light, outline, widths):
        """体の左右（透明な所）に羽。rows は始まりの行（頭の上からのずれ）、widths は行ごとの幅"""
        for k, g in self.frames.items():
            top = self.head_top(g)
            for i, w in enumerate(widths):
                y = top + rows + i
                if y >= 32:
                    break
                l, r = self.edges(g, y)
                if l is None:
                    continue
                sides = [(-1, l), (1, r)] if not k.startswith(("left", "right")) else ([(1, r)] if k.startswith("left") else [(-1, l)])
                for s, e in sides:
                    for j in range(1, w + 1):
                        c = outline if j == w else (light if (i + j) % 3 == 0 else inner)
                        self.put(g, y, e + s * j, c)

    def halo(self, color, dark, gap=4):
        for g in self.frames.values():
            top, cx = self.head_center(g)
            y = max(0, top - gap)
            for dx in range(-3, 3):
                x = int(cx + 0.5 + dx)
                self.put(g, y, x, color if -2 <= dx <= 1 else dark)

    def horns(self, color, light, spread=3, height=2, extra=()):
        for g in self.frames.values():
            top, cx = self.head_center(g)
            for dx in (-spread, spread - 1, *extra):
                x = int(cx + 0.5 + dx)
                for h in range(1, height + 1):
                    self.put(g, top - h, x, light if h == height else color)
                self.put(g, top, x, color, over=True)

    def ears(self, skin, row_from_top=8):
        for k, g in self.frames.items():
            if k.startswith("up"):
                continue
            top = self.head_top(g)
            y = top + row_from_top
            l, r = self.edges(g, y)
            if l is None:
                continue
            if not k.startswith("right"):
                self.put(g, y, l - 1, skin); self.put(g, y - 1, l - 1, skin)
            if not k.startswith("left"):
                self.put(g, y, r + 1, skin); self.put(g, y - 1, r + 1, skin)

    def tail(self, color, tip):
        for k, g in self.frames.items():
            y0 = 23
            l, r = self.edges(g, y0)
            if l is None:
                continue
            s, e = (1, r) if not k.startswith("right") else (-1, l)
            pts = [(y0, e + s), (y0 + 1, e + 2 * s), (y0 + 2, e + 2 * s), (y0 + 3, e + 3 * s)]
            for y, x in pts:
                self.put(g, y, x, color)
            self.put(g, y0 + 4, e + 3 * s, tip); self.put(g, y0 + 4, e + 4 * s, tip)

    def cape(self, inner, dark, outline, start=18, end=29):
        for k, g in self.frames.items():
            for y in range(start, end):
                l, r = self.edges(g, y)
                if l is None:
                    continue
                w = 1 + (y - start) // 4
                sides = [(-1, l), (1, r)]
                if k.startswith("left"):
                    sides = [(1, r)]
                if k.startswith("right"):
                    sides = [(-1, l)]
                for s, e in sides:
                    for j in range(1, w + 1):
                        self.put(g, y, e + s * j, outline if j == w else (dark if j > 1 else inner))
            if k.startswith("up"):   # 後ろ向き: 背中いっぱいのマント
                for y in range(start, end):
                    l, r = self.edges(g, y)
                    for x in range(l + 1, r):
                        if g[y][x] not in ".A":
                            g[y][x] = dark if (x + y) % 5 == 0 else inner

    # --- 書き出し ---
    def save(self, out, name):
        out = pathlib.Path(out)
        frames = {k: ["".join(r) for r in g] for k, g in self.frames.items()}
        json.dump({"palette": self.pal, "frames": frames}, open(out / f"{name}.walker.json", "w"), ensure_ascii=False)
        sheet = [""] * 128
        for ri, d in enumerate(ORDER):
            for f in range(3):
                for y, row in enumerate(frames[f"{d}{f}"]):
                    sheet[ri * 32 + y] += row
        open(out / "sheet.txt", "w").write("\n".join(sheet) + "\n")
        json.dump({c: self.pal[i] for i, c in enumerate(L[:len(self.pal)])}, open(out / "sheet.json", "w"))

        def img(rows, k=1):
            im = Image.new("RGBA", (len(rows[0]), len(rows)))
            for y, r in enumerate(rows):
                for x, c in enumerate(r):
                    if c != ".":
                        h = self.pal[L.index(c)].lstrip("#")
                        im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
            return im.resize((im.width * k, im.height * k), Image.NEAREST)
        img(sheet).save(out / "sheet.png")
        big = Image.new("RGBA", (48 * 8, 128 * 8), (52, 60, 72, 255)); big.alpha_composite(img(sheet, 8)); big.save(out / "sheet_x8.png")
        gif = []
        for d in ORDER:
            for _ in range(2):
                for f in (1, 0, 1, 2):
                    fr = Image.new("RGBA", (128, 256), (70, 96, 70, 255)); fr.alpha_composite(img(frames[f"{d}{f}"], 8)); gif.append(fr.convert("RGB"))
        gif[0].save(out / "walk.gif", save_all=True, append_images=gif[1:], duration=200, loop=0)
        return len(self.pal)


def stamp(c, masks, over_keys=()):
    """向きごとの点の一覧で描く。masks = {"down": [(y, x, 色記号), ...], "up": [...], "left": [...]}。
    right は left の左右反転。over_keys に入っている向きは、体の上にも描く（後ろ向きの背中の羽など）"""
    for k, g in c.frames.items():
        d = k[:-1]
        pts = masks.get(d) if d != "right" else [(y, 15 - x, col) for y, x, col in masks.get("left", [])]
        for y, x, col in pts or []:
            c.put(g, y, x, col, over=d in over_keys)


def wing_masks(inner, light, dark, outline, bat=False):
    """羽（白い鳥の羽 / こうもりの羽）の形。16×32の絵の、頭の外側と背中に出る所だけ"""
    def row(y, xs, edge):
        return [(y, x, outline if x == edge else (light if (x + y) % 3 == 0 else (dark if bat and x % 2 else inner))) for x in xs]
    front = []
    for y, xs in {17: [0], 18: [0], 19: [0]}.items():   # 頭の上の左右の羽の先は描かない（2026-10-07、人間の指示「頭の上の左右の黄色いのと赤いのいらないかも」）
        front += row(y, xs, 0)
        front += row(y, [15 - x for x in xs], 15)
    side = []
    for y, xs in {12: [13], 13: [13, 14], 14: [12, 13, 14, 15], 15: [12, 13, 14, 15], 16: [12, 13, 14, 15], 17: [12, 13, 14],
                  18: [12, 13, 14], 19: [12, 13], 20: [12, 13], 21: [12]}.items():
        side += row(y, xs, max(xs))
    if bat:
        side += [(11, 14, outline), (13, 15, outline), (17, 15, outline)]
    back = []
    for y, (a, b) in {16: (2, 6), 17: (1, 6), 18: (1, 6), 19: (1, 6), 20: (2, 6), 21: (2, 5), 22: (3, 5), 23: (3, 4)}.items():
        back += row(y, range(a, b + 1), a)
        back += row(y, [15 - x for x in range(a, b + 1)], 15 - a)
    return {"down": front, "up": back, "left": side}
