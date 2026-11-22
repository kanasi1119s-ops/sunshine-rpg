"""もらった絵のキャラクターを、フィールド用キャラの型（field_sprite.py）をもとに 24×32 の歌い手にする。
型の正面の立ち絵（16×32）を 24×32 のまん中に置き、縦ロール・リボン・あほ毛・服の飾りを描き足し、口の形 6 つとまばたきのコマを作る。"""
import json, sys
from PIL import Image
OUT = sys.argv[1]
rows = open("/tmp/px5/base.sheet.txt").read().split("\n"); pal = json.load(open("/tmp/px5/base.sheet.json"))
base = [list("...." + r[:16] + "....") for r in rows[:32]]
inv = {v.lower(): k for k, v in pal.items()}
def sym(color):
    c = color.lower()
    if c not in inv:
        s = next(ch for ch in "abcdefghijklmnopqrstuvwxyz0123456789" if ch not in pal); pal[s] = c; inv[c] = s
    return inv[c]
A, B, C, D, G = "A", sym("#dd1f2a"), None, None, sym("#ffdcc8")
C = [k for k, v in pal.items() if k in "C"][0]; D = "D"
TEAL, TEAL2, WHITE, WSH, NAVY, RED, RDK, BLK = sym("#1b8c92"), sym("#35c9c0"), sym("#f2eef2"), sym("#a086a4"), sym("#283762"), sym("#c7202c"), sym("#7e1126"), sym("#2a1c27")
MD, TONGUE, HL = sym("#7a1a2a"), sym("#ff8a94"), sym("#ffb3a0")
def put(g, x, y, s):
    if 0 <= x < 24 and 0 <= y < 32: g[y][x] = s
def stamp(g, x, y, lines):
    for j, l in enumerate(lines):
        for i, ch in enumerate(l):
            if ch != " ": put(g, x + i, y + j, {"A": A, "B": B, "C": C, "D": D, "H": HL, "W": WHITE, "w": WSH, "N": NAVY, "R": RED, "r": RDK, "K": BLK}[ch])
def common(g):
    # 縦ロール（左右）。3段で1巻き: 上が明るく、下が暗い。下へ行くほど少し外へ、最後は細く
    for j in range(5):
        y = 10 + j * 3
        if j < 2: stamp(g, 0, y, ["ACCBA", "ABBDA", "ABDDA"]); stamp(g, 19, y, ["ABCCA", "ADBBA", "ADDBA"])
        elif j < 4: stamp(g, 0, y, [" ACBA", " ABDA", " ADDA"]); stamp(g, 19, y, ["ABCA ", "ADBA ", "ADDA "])
        else: stamp(g, 2, y, ["ACA", "ADA", " A "]); stamp(g, 19, y, ["ACA", "ADA", " A "])
    for x in (1, 2, 3, 20, 21, 22): put(g, x, 9, A)
    # 白いくつ下と黒いくつ
    stamp(g, 7, 29, ["AWWAAAAWWA", "AKKA  AKKA", "AAAA  AAAA"])
    # あほ毛
    stamp(g, 10, 1, [" AA ", "ABBA", " ABA"]); 
    # 頭のリボン（紺と白のしま）
    stamp(g, 15, 3, [" AAA", "ANWA", "AWNA", " AA "])
    # 首もとの赤いリボン、スカートの黒いフリルと白いレース
    for x in (11, 12): put(g, x, 19, RED)
    put(g, 10, 19, RDK); put(g, 13, 19, RDK)
    for x in range(6, 18):
        if g[25][x] not in (A, "."): put(g, x, 25, BLK)
        if g[28][x] not in (A, "."): put(g, x, 28, WHITE)
    # 目: 上がこい青緑、下が明るい青緑
    for x in (9, 14):
        put(g, x, 14, TEAL); put(g, x, 15, TEAL2)
def face(g, mouth, blink):
    for x in (10, 11, 12, 13): put(g, x, 16, G if x in (11, 12) else g[16][x]); 
    put(g, 11, 17, G); put(g, 12, 17, G)
    if mouth == "closed": put(g, 11, 17, MD); put(g, 12, 17, MD)
    elif mouth == "a": [put(g, x, 16, MD) for x in (10, 11, 12, 13)]; put(g, 11, 17, TONGUE); put(g, 12, 17, TONGUE)
    elif mouth == "i": put(g, 10, 17, MD); put(g, 11, 17, WHITE); put(g, 12, 17, WHITE); put(g, 13, 17, MD)
    elif mouth == "u": put(g, 11, 17, MD)
    elif mouth == "e": put(g, 10, 16, MD); put(g, 11, 16, WHITE); put(g, 12, 16, WHITE); put(g, 13, 16, MD); put(g, 11, 17, TONGUE); put(g, 12, 17, TONGUE)
    elif mouth == "o": put(g, 11, 16, MD); put(g, 12, 16, MD); put(g, 11, 17, MD); put(g, 12, 17, MD)
    if blink:
        for x0 in (8, 13):
            put(g, x0 + 1, 14, G)
            for x in (x0, x0 + 1, x0 + 2): put(g, x, 15, TEAL)
FR = [("closed", False, 400), ("a", False, 200), ("i", False, 200), ("u", False, 200), ("e", False, 200), ("o", False, 200), ("closed", True, 150)]
cels = []
for m, bl, _ in FR:
    g = [r[:] for r in base]; common(g); face(g, m, bl); cels.append(["".join(r) for r in g])
# 口のまわりの元の色を確かめるための出力
used = sorted({ch for c in cels for r in c for ch in r if ch != "."})
json.dump({"format": "sunshine-pixel", "version": 2, "width": 24, "height": 32, "symbols": [{"sym": s, "label": "色", "color": pal[s]} for s in used],
           "layers": [{"name": "歌い手", "visible": True, "opacity": 1}], "frames": [{"dur": d} for _, _, d in FR], "cels": [cels], "layer": 0, "frame": 0},
          open(f"{OUT}/縦ロールの歌い手_24x32.sunshine-pixel.json", "w", encoding="utf-8"), ensure_ascii=False)
def img(c, z):
    im = Image.new("RGBA", (24, 32), (0, 0, 0, 0))
    for y, r in enumerate(c):
        for x, ch in enumerate(r):
            if ch != ".": h = pal[ch]; im.putpixel((x, y), (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255))
    return im.resize((24 * z, 32 * z), Image.NEAREST)
z = 12; sheet = Image.new("RGBA", (24 * z * 7, 32 * z), (88, 94, 108, 255)); raw = Image.new("RGBA", (24 * 7, 32), (0, 0, 0, 0))
for i, c in enumerate(cels): sheet.alpha_composite(img(c, z), (i * 24 * z, 0)); raw.alpha_composite(img(c, 1), (i * 24, 0))
sheet.save(f"{OUT}/縦ロールの歌い手_24x32_確認用（口の形7コマ）.png"); raw.save(f"{OUT}/縦ロールの歌い手_24x32_シート（等倍・透明）.png"); print(len(used), "色")
for r in cels[0]: print(r)
