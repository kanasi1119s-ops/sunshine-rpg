"""苔岩の子竜（2頭身のモンスター・32×32・右向き・待機3コマ）を作る。
2026-10-07、人間の指示「モンスターも1体作ってみて」。イメージ画像は ref.png（Stable Diffusion 1.5）。
イメージ画像から拾った特ちょう: 苔の緑の体／頭の上と後ろの、灰色の石のとげ（冠のように並ぶ）／大きな黒い目と白っぽい目のふち／
灰色のこうもりのような小さな羽（とげが3本）／長いしっぽ／太い前足と灰色の爪。
2頭身にするため、頭を全体の半分近くまで大きくし、体と足を短くした。
部品（しっぽ・後ろ足・羽・体・前足・頭）を後ろから順に置き、縁取りと陰影（光は左上）をつけてから、目・口・石のとげを1ドットずつ描く。
使い方: python3 make.py → sheet.txt・sheet.json（エディタ用、96×32 = 3コマ）・sheet.png・sheet_x8.png・idle.gif"""
import json
import pathlib
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
W = H = 32

# 色（16色）
PAL = {
    ".": None,
    "A": "#1a2014",  # 外の縁取り（黒ではなく、こい緑の黒）
    "a": "#2e3e1c",  # 中の縁取り（部品の重なり）
    "B": "#40601e",  # 苔の暗
    "C": "#6e922c",  # 苔の地
    "D": "#9cbc42",  # 苔の明
    "E": "#cfe070",  # 苔のいちばん明るい所
    "F": "#3a3a42",  # 石の暗
    "G": "#6c6c76",  # 石の地
    "H": "#a2a2ae",  # 石の明
    "I": "#d8d8e0",  # 目のふち・光
    "J": "#0e0e14",  # 目
    "K": "#ffffff",  # 目の光
    "L": "#2a1c14",  # 口
    "M": "#b8cc6a",  # おなか
    "N": "#24242a",  # 爪
}
# 部品ごとの 明・地・暗
TONES = {"moss": ("D", "C", "B"), "stone": ("H", "G", "F"), "wing": ("G", "F", "F"), "belly": ("M", "M", "C")}


def parts(bob=0, wing_up=0):
    """部品を後ろから順に、(名前, 色の種類, マスク) で返す"""
    out = []

    def mask(draw_fn):
        im = Image.new("L", (W, H), 0)
        draw_fn(ImageDraw.Draw(im))
        return im

    b = bob
    # しっぽ（体の左下から左へのび、先が少し上がる）
    out.append(("tail", "moss", mask(lambda d: (d.line([(9, 23 + b), (5, 25 + b), (2, 26 + b)], fill=255, width=3),
                                               d.line([(2, 26 + b), (1, 24 + b)], fill=255, width=2)))))
    # 後ろ足（地面に着いているので、上下しない）
    out.append(("leg_b", "moss", mask(lambda d: (d.rectangle([7, 23, 11, 28], fill=255), d.rectangle([6, 28, 12, 29], fill=255)))))
    # 羽（背中から左上へ、石の色のとげ3本）
    w = wing_up
    wing_rows = {3: "..#...........", 4: "..##..........", 5: "...###........", 6: "...#####......",
                 7: "....#######...", 8: "....#########.", 9: "...###########", 10: "..############",
                 11: "..##.###.#####", 12: "..#...#...####", 13: "...........###", 14: "............##"}

    def draw_wing(d):
        for y, r in wing_rows.items():
            dy = b - (wing_up if y <= 8 else (wing_up // 2 if y <= 11 else 0))   # 羽を上げるときは、先ほど大きく動く
            for x, c in enumerate(r):
                if c == "#":
                    d.point((x, y + dy), fill=255)
                    if wing_up and y <= 8:
                        d.point((x, y + dy + 1), fill=255)
    out.append(("wing", "wing", mask(draw_wing)))
    # 体
    out.append(("body", "moss", mask(lambda d: d.ellipse([5, 15 + b, 21, 27 + b], fill=255))))
    # 前足
    out.append(("leg_f", "moss", mask(lambda d: (d.rectangle([17, 21 + b, 21, 28], fill=255), d.rectangle([16, 28, 23, 29], fill=255)))))
    # 頭（大きく丸く）と鼻先
    out.append(("head", "moss", mask(lambda d: (d.ellipse([11, 4 + b, 28, 20 + b], fill=255), d.ellipse([21, 9 + b, 30, 18 + b], fill=255)))))
    return out


def render(bob=0, wing_up=0):
    g = [["."] * W for _ in range(H)]
    owner = [[-1] * W for _ in range(H)]
    ps = parts(bob, wing_up)
    for i, (name, tone, m) in enumerate(ps):
        lt, mid, dk = TONES[tone]
        px = m.load()
        inside = lambda x, y: 0 <= x < W and 0 <= y < H and px[x, y] > 0
        for y in range(H):
            for x in range(W):
                if not inside(x, y):
                    continue
                if not inside(x - 1, y) or not inside(x, y - 1):
                    c = lt
                elif not inside(x + 1, y) or not inside(x, y + 1) or not inside(x + 1, y + 1):
                    c = dk
                else:
                    c = mid
                g[y][x] = c
                owner[y][x] = i
        # 前の部品の縁: 後ろの部品と接する所に中の縁取り
        for y in range(H):
            for x in range(W):
                if owner[y][x] != i:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < H and 0 <= owner[yy][xx] < i and not inside(xx, yy):
                        g[y][x] = "a"
                        break
    # 苔の模様（まばらに暗い点と明るい点）
    for y in range(H):
        for x in range(W):
            if g[y][x] == "C":
                if (x * 7 + y * 3) % 11 == 0:
                    g[y][x] = "B"
                elif (x * 5 + y * 9) % 13 == 0:
                    g[y][x] = "D"
    # おなか（体の下の方を明るく）
    for y in range(20 + bob, 27 + bob):
        for x in range(7, 20):
            if 0 <= y < H and owner[y][x] == 3 and g[y][x] in "CBD" and ((x - 14) / 6.5) ** 2 + ((y - bob - 25.5) / 3.6) ** 2 < 1:
                g[y][x] = "M"
    # 外の縁取り
    filled = [[g[y][x] != "." for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            if filled[y][x]:
                continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and filled[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = "A"

    def put(y, x, c):
        if 0 <= y < H and 0 <= x < W:
            g[y][x] = c
    b = bob
    # 頭の石のとげ（冠のように、頭の上と後ろに並ぶ）
    for (x, y, h) in ((13, 6, 2), (15, 4, 3), (18, 3, 3), (21, 3, 3), (24, 4, 2), (12, 9, 2)):
        for k in range(h):
            put(y + b - k, x, "G" if k else "F")
            put(y + b - k, x + 1, "H" if k == h - 1 else "G")
        put(y + b - h, x, "A"); put(y + b - h, x + 1, "A")
        put(y + b - h + 1, x - 1, "A") if g[y + b - h + 1][x - 1] == "." else None
        put(y + b - h + 1, x + 2, "A") if g[y + b - h + 1][x + 2] == "." else None
    for (x, y) in ((14, 7), (16, 6), (19, 6), (22, 6), (25, 7), (17, 8), (20, 8), (13, 11)):   # 頭の上の石のつぶ
        put(y + b, x, "G"); put(y + b, x + 1, "F")
    # 羽の骨（3本のとげの先から肩へ、明るい石の線）
    wu = wing_up
    for (x, y) in ((3, 4), (4, 5), (5, 5), (6, 6), (7, 6), (8, 7), (9, 7), (10, 8), (11, 8), (12, 9), (13, 10), (7, 8), (6, 9), (5, 10), (4, 11), (3, 12), (9, 9), (8, 10), (7, 11), (6, 12)):
        yy = y + b - (wu if y <= 8 else (wu // 2 if y <= 11 else 0))
        if 0 <= yy < H and g[yy][x] in "FG":
            put(yy, x, "H")
    # 背中の小さな石のとげ
    for (x, y) in ((8, 15), (6, 17)):
        put(y + b, x, "G"); put(y + b - 1, x, "H"); put(y + b - 2, x, "A"); put(y + b - 1, x - 1, "A"); put(y + b - 1, x + 1, "A")
    # 目（イメージ画像どおり、黒いアーモンド形の大きな目に、灰色のふちと、石のまゆ）
    for x in range(19, 27):
        put(7 + b, x, "G")                       # まゆの石（上）
        put(8 + b, x, "F")                       # まゆの石（影）
    put(7 + b, 19, "H"); put(7 + b, 20, "H")
    for (x, y) in ((20, 9), (25, 9), (19, 10), (26, 10), (20, 11), (25, 11), (21, 12), (22, 12), (23, 12), (24, 12)):
        put(y + b, x, "H")                       # 目のふち
    for (x, y) in ((21, 9), (22, 9), (23, 9), (24, 9), (20, 10), (21, 10), (22, 10), (23, 10), (24, 10), (25, 10), (21, 11), (22, 11), (23, 11), (24, 11)):
        put(y + b, x, "J")
    put(9 + b, 22, "K"); put(10 + b, 21, "I")   # 目の光
    # 鼻の穴と口
    put(12 + b, 28, "L")
    for x in range(23, 30):
        put(15 + b, x, "L")
    put(14 + b, 23, "L")
    # 爪
    for x in (17, 19, 21, 23):                   # 前足の爪（地面に広がる）
        put(30, x, "N")
    put(29, 24, "N"); put(30, 24, "A")
    for x in (6, 8, 10, 12):                     # 後ろ足の爪
        put(30, x, "N")
    return g


def main():
    frames = [render(0, 0), render(1, 0), render(0, 2)]   # 0 ふつう / 1 体が1ドット下がる / 2 羽が上がる
    used = sorted({c for f in frames for r in f for c in r} - {"."})
    sheet = ["".join("".join(f[y]) for f in frames) for y in range(H)]
    (HERE / "sheet.txt").write_text("\n".join(sheet) + "\n")
    json.dump({c: PAL[c] for c in used}, open(HERE / "sheet.json", "w"))

    def img(rows, k=1):
        im = Image.new("RGBA", (len(rows[0]), len(rows)))
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c != ".":
                    h = PAL[c].lstrip("#")
                    im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
        return im.resize((im.width * k, im.height * k), Image.NEAREST)
    img(sheet).save(HERE / "sheet.png")
    big = Image.new("RGBA", (96 * 8, 32 * 8), (52, 60, 72, 255)); big.alpha_composite(img(sheet, 8)); big.save(HERE / "sheet_x8.png")
    gif = []
    for f in (0, 1, 0, 2):
        fr = Image.new("RGBA", (32 * 6, 32 * 6), (52, 60, 72, 255))
        fr.alpha_composite(img(["".join(r) for r in frames[f]], 6))
        gif.append(fr.convert("P", palette=Image.ADAPTIVE))
    gif[0].save(HERE / "idle.gif", save_all=True, append_images=gif[1:], duration=300, loop=0)
    print("色数", len(used))


if __name__ == "__main__":
    main()
