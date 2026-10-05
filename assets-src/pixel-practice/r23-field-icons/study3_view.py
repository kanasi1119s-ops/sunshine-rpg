"""3回目の勉強のプレビュー用の道具: ゲームの本物の地形テクスチャ（assets-src/field/terrain/w-*.png）の上に置く。"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
TERRAIN = os.path.join(HERE, "..", "..", "field", "terrain")
_cache = {}


def tex(kind):
    if kind not in _cache:
        _cache[kind] = Image.open(os.path.join(TERRAIN, f"w-{kind}.png")).convert("RGBA")
    return _cache[kind]


def terrain(kind, w, h, ox=0, oy=0):
    t = tex(kind)
    bg = Image.new("RGBA", (w, h))
    for y in range(-(oy % 128), h, 128):
        for x in range(-(ox % 128), w, 128):
            bg.paste(t, (x, y))
    return bg


SHADOW = {"grass": (10, 30, 10, 90), "snow": (40, 60, 100, 70), "sand": (60, 40, 10, 80), "sea": (0, 10, 40, 70),
          "lake": (0, 10, 40, 70), "cloud": (60, 70, 110, 60), "ash": (0, 0, 0, 80), "forest": (0, 20, 0, 90)}


def shadow_layer(im, kind):
    """足もとの半透明のだ円（ゲームではコードで敷く予定）。絵の横はばに合わせる"""
    w, h = im.size
    bbox = im.split()[3].getbbox() or (0, 0, w, h)
    x0, x1 = bbox[0], bbox[2]
    sh = Image.new("RGBA", (w, h))
    ImageDraw.Draw(sh).ellipse((x0 + (x1 - x0) * 0.08, h - 9, x1 - (x1 - x0) * 0.02, h - 1), fill=SHADOW.get(kind, (0, 0, 0, 80)))
    return sh


def on_terrain(im, kind, shadow=True):
    bg = terrain(kind, im.width, im.height)
    if shadow:
        bg.alpha_composite(shadow_layer(im, kind))
    bg.alpha_composite(im)
    return bg


# ===================================================================== 比べる表（study3-preview.png）
import json
import re

PX = os.path.join(HERE, "..")


def load_icon(d, n):
    rows = [l for l in open(os.path.join(PX, d, f"{n}.txt")).read().split("\n") if l]
    pal = json.load(open(os.path.join(PX, d, f"pal-{n}.json")))
    w, h = max(len(r) for r in rows), len(rows)
    im = Image.new("RGBA", (w, h))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c in pal:
                im.putpixel((x, y), tuple(int(pal[c][k:k + 2], 16) for k in (1, 3, 5)) + (255,))
    return im


# 練習の絵 → (今のゲームのアイコン, ふさわしい地面, 影を敷くか)
PAIRS = [
    ("castle3", ("r17-polish", "icon-castle"), "grass", True),
    ("spire3", ("r22-vehicles", "spire"), "sea", True),
    ("town3", ("r17-polish", "icon-snowtown"), "snow", True),
    ("cave3", ("r17-polish", "icon-cave"), "grass", True),
    ("mine3", ("r17-polish", "icon-mine"), "grass", True),
    ("port3", ("r17-polish", "icon-port"), "grass", True),
    ("village3", ("r17-polish", "icon-village"), "grass", True),
    ("lake3", ("r17-polish", "icon-lake"), "grass", True),
    ("temple3", ("r17-polish", "icon-temple"), "grass", True),
    ("ruin3", ("r17-polish", "icon-ruin"), "grass", True),
    ("stones3", ("r17-polish", "icon-stones"), "grass", True),
    ("bigtree3", ("r17-polish", "icon-bigtree"), "grass", True),
    ("shrine3", ("r17-polish", "icon-shrine"), "forest", True),
    ("volcano3", ("r17-polish", "icon-volcano"), "ash", True),
    ("vortex3", ("r17-polish", "icon-vortex"), "sea", False),
    ("dive3", ("r17-polish", "icon-dive"), "sea", False),
    ("tents3", ("r17-polish", "icon-tents"), "sand", True),
    ("sky3", ("r17-polish", "icon-sky"), "cloud", True),
    ("palace3", ("r17-polish", "icon-palace"), "waste", True),
    ("islet-fort3", ("r22-vehicles", "islet-fort"), "sea", False),
    ("islet-shrine3", ("r22-vehicles", "islet-shrine"), "sea", False),
    ("islet-cave3", ("r22-vehicles", "islet-cave"), "sea", False),
    ("islet-ruin3", ("r22-vehicles", "islet-ruin"), "sea", False),
]


def preview(path, Z=3):
    cells = []
    for name, old, kind, sh in PAIRS:
        new = load_icon("r23-field-icons", name)
        cur = load_icon(*old)
        a = on_terrain(new, kind, sh)
        b = on_terrain(cur, kind, False)
        pair = Image.new("RGBA", (a.width + b.width + 4, max(a.height, b.height)), (40, 40, 48, 255))
        pair.paste(a, (0, pair.height - a.height)); pair.paste(b, (a.width + 4, pair.height - b.height))
        cells.append((f"{name} | now: {old[1]} ({kind})", pair))
    maxw = 1560
    x, y, rowh, placed = 12, 12, 0, []
    for label, im in cells:
        w, h = im.width * Z, im.height * Z
        if x + w > maxw:
            x, y, rowh = 12, y + rowh + 22, 0
        placed.append((label, im, x, y)); x += w + 14; rowh = max(rowh, h)
    H1 = y + rowh + 40
    # 下の帯: ゲームと同じ大きさ（1倍）を2倍に広げて見せる。草の地面に足もとをそろえる
    names = [p[0] for p in PAIRS]
    ims = [load_icon("r23-field-icons", n) for n in names]
    sw = sum(i.width + 3 for i in ims) + 6
    strip = terrain("grass", sw, 118)
    xx = 4
    for n, im in zip(names, ims):
        lay = Image.new("RGBA", (sw, 118))
        lay.alpha_composite(shadow_layer(im, "grass"), (xx, 116 - im.height))
        lay.alpha_composite(im, (xx, 116 - im.height))
        strip.alpha_composite(lay); xx += im.width + 3
    k = max(1, min(2, maxw // sw))
    strip = strip.resize((strip.width * k, strip.height * k), Image.NEAREST)
    sheet = Image.new("RGBA", (max(maxw, strip.width), H1 + strip.height + 4), (40, 40, 48, 255))
    dr = ImageDraw.Draw(sheet)
    for label, im, px, py in placed:
        sheet.paste(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (px, py))
        dr.text((px, py + im.height * Z + 3), label, fill=(255, 255, 255))
    sheet.paste(strip, (0, H1))
    dr.text((6, H1 - 14), f"game scale x{k} (all practice pieces on grass)", fill=(255, 255, 255))
    sheet.save(path)


def grounds(path, Z=2):
    """全部の練習の絵を、草・雪・砂の3つの地面に置いて、地面で見え方が変わるかを確かめる"""
    names = [p[0] for p in PAIRS]
    kinds = ["grass", "snow", "sand"]
    ims = [load_icon("r23-field-icons", n) for n in names]
    cw = 64 * Z + 8
    rows = [names[i:i + 12] for i in range(0, len(names), 12)]
    H = 0
    blocks = []
    for r in rows:
        bh = max(load_icon("r23-field-icons", n).height for n in r) * Z
        blocks.append((r, bh)); H += 3 * (bh + 8) + 20
    sheet = Image.new("RGBA", (12 * cw + 70, H + 10), (40, 40, 48, 255))
    dr = ImageDraw.Draw(sheet)
    y = 6
    for r, bh in blocks:
        for kd in kinds:
            dr.text((4, y + bh // 2), kd, fill=(255, 255, 255))
            for i, n in enumerate(r):
                im = load_icon("r23-field-icons", n)
                t = on_terrain(im, kd, True).resize((im.width * Z, im.height * Z), Image.NEAREST)
                sheet.paste(t, (60 + i * cw, y + bh - t.height))
            y += bh + 8
        y += 20
    sheet.save(path)


# ===================================================================== 世界地図に置いた見本（study3-world.png）
GLYPH_TEX = {"O": "sea", "P": "grass", "F": "forest", "T": "snowforest", "M": "mountain", "D": "sand", "S": "snow", "R": "road",
             "H": "hills", "L": "lake", "C": "cloud", "W": "waste", "A": "ash", "Z": "lava", "V": "sea", "Q": "sea", "X": "chasm", "N": "pyramids"}


def world_rows():
    src = open(os.path.join(HERE, "..", "..", "..", "src", "game", "map", "world", "world-map.generated.ts")).read()
    a = src.index("WORLD_ROWS")
    b = src.index("];", a)
    return re.findall(r'"([A-Z]+)"', src[a:b])


def world_panel(rows, x0, y0, tw, th, icons, title):
    """本物の地形（1マス16ドット、テクスチャは世界の座標でつながる）を描き、アイコンを足もとの位置に置く"""
    W, H = tw * 16, th * 16
    img = Image.new("RGBA", (W, H))
    for ty in range(th):
        for tx in range(tw):
            gx, gy = x0 + tx, y0 + ty
            gl = rows[gy][gx] if 0 <= gy < len(rows) and 0 <= gx < len(rows[gy]) else "O"
            t = tex(GLYPH_TEX.get(gl, "grass"))
            sx, sy = (gx * 16) % 128, (gy * 16) % 128
            img.paste(t.crop((sx, sy, sx + 16, sy + 16)), (tx * 16, ty * 16))
    for (name, gx, gy, kind) in sorted(icons, key=lambda i: i[2]):
        im = load_icon("r23-field-icons", name)
        px = (gx - x0) * 16 + 8 - im.width // 2
        py = (gy - y0 + 1) * 16 - im.height
        if kind:
            img.alpha_composite(shadow_layer(im, kind), (px, py))
        img.alpha_composite(im, (px, py))
    ImageDraw.Draw(img).text((4, 2), title, fill=(255, 255, 255))
    return img
