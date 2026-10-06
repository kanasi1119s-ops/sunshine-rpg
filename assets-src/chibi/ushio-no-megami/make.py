"""潮と月の女神（2頭身・16×32・4方向×3コマ）。2026-10-07、人間の指示「神に変えましょうか作るの」「64は細かすぎる 32×16で」。
イメージ画像（ref.png、Stable Diffusion 1.5 で描いた、ふつうの頭身の女神）を見て、2頭身の歩くキャラの体（仲間の長い髪の型）に、
銀の髪・深い青のローブ・真珠のふち・三日月の光輪・真珠の杖を描いた。実在の宗教の像に寄せないよう、手は合わせず、光輪は三日月にした。
"""
import json, pathlib
from PIL import Image
HERE = pathlib.Path(__file__).parent
base = json.load(open(HERE / "../../characters/walk-2head/ミナ.json"))
L = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
pal = list(base["palette"])
def setc(ch, hexv): pal[L.index(ch)] = hexv
# 髪: 銀
setc("B", "#d6dbe8"); setc("C", "#f5f7fc"); setc("D", "#8d95ad")
# 目: 深い青、髪かざり: 真珠
setc("I", "#2c4bb0"); setc("E", "#e9eefc"); setc("F", "#ffffff")
# 杖: 真珠と銀
setc("H", "#c9d1e3"); setc("J", "#7d86a0")
# 上のローブ: 深い青、金のふち → 真珠
setc("N", "#2f4fa8"); setc("O", "#1d3a80"); setc("P", "#4a6cc8"); setc("Q", "#6f8fe0"); setc("R", "#f1ecdc")
# 潮の玉の色（b）は元の明るい水色を使う
# 下のローブ: 深い青に波の明かり
setc("T", "#2a4898"); setc("U", "#1b3170"); setc("V", "#15275a"); setc("W", "#203c86"); setc("X", "#86a6ee")
# 三日月の光輪（新しい色）
pal += ["#fff3b8", "#e6c25a"]
HALO, HALO2 = L[len(pal) - 2], L[len(pal) - 1]
CRESCENT = [(0, -2), (0, 3), (1, -2), (1, -1), (1, 2), (1, 3), (2, -1), (2, 0), (2, 1), (2, 2)]   # 上が開いた三日月（中心からのずれ）
frames = {}
for k, rows in base["frames"].items():
    if k[-1] not in "012" or not k[:-1] in ("down", "up", "left", "right"):
        continue
    g = [list(r) for r in rows]
    top = next(y for y, r in enumerate(g) if any(c != "." for c in r))
    xs = [x for x, c in enumerate(g[top]) if c != "."]
    cx = (min(xs) + max(xs)) // 2
    y0 = max(0, top - 4)
    for dy, dx in CRESCENT:
        y, x = y0 + dy, cx + dx
        if 0 <= x < 16 and g[y][x] == ".":
            g[y][x] = HALO if dy < 2 else HALO2
    # 真珠のふち: ローブのすその1行上に、1つおきに真珠の点
    hem = max(y for y, r in enumerate(g) if any(c in "TX" for c in r))
    for x in range(16):
        if g[hem][x] in "TX" and x % 2 == 0:
            g[hem][x] = "R"
    # 正面: 胸の前に、光る潮の玉（2×2、まわりに暗い縁）を両手で持つ
    if k.startswith("down"):
        oy = 20 + (1 if any(c != "." for c in g[4]) and top > 4 else 0) + (top - 4)
        for (dy, dx), c in {(0, 0): "F", (0, 1): "b", (1, 0): "b", (1, 1): "E"}.items():
            g[oy + dy][7 + dx] = c
    frames[k] = ["".join(r) for r in g]
json.dump({"palette": pal, "frames": frames}, open(HERE / "ushio-no-megami.walker.json", "w"), ensure_ascii=False)
order = ["down", "up", "left", "right"]
sheet = [""] * 128
for r, d in enumerate(order):
    for f in range(3):
        for y, row in enumerate(frames[f"{d}{f}"]):
            sheet[r * 32 + y] += row
open(HERE / "sheet.txt", "w").write("\n".join(sheet) + "\n")
json.dump({c: pal[i] for i, c in enumerate(L[:len(pal)])}, open(HERE / "sheet.json", "w"))
def img(rows, k=1):
    im = Image.new("RGBA", (len(rows[0]), len(rows)))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != ".":
                h = pal[L.index(c)].lstrip("#"); im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im.resize((im.width * k, im.height * k), Image.NEAREST)
img(sheet).save(HERE / "sheet.png")
big = Image.new("RGBA", (48 * 8, 128 * 8), (52, 60, 72, 255)); big.alpha_composite(img(sheet, 8)); big.save(HERE / "sheet_x8.png")
gif = []
for d in order:
    for _ in range(2):
        for f in (1, 0, 1, 2):
            fr = Image.new("RGBA", (16 * 8, 32 * 8), (70, 96, 70, 255)); fr.alpha_composite(img(frames[f"{d}{f}"], 8)); gif.append(fr.convert("RGB"))
gif[0].save(HERE / "walk.gif", save_all=True, append_images=gif[1:], duration=200, loop=0)
print("colors", len(pal))
