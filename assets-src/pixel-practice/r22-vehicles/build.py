"""r22-vehicles の全部を作り直す。使い方: python3 build.py
→ <名前>.txt, pal-<名前>.json, preview.png。色数・文字・大きさを自動確認する（失敗したら終了コード1）。"""
import json, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from lib import PAL
import ships

# 名前: (幅, 高さ, 足元y（枠の上から。None=確認しない）)
SPEC = {
    "ship-right": (32, 32, 26), "ship-left": (32, 32, 26), "ship-down": (32, 32, 27), "ship-up": (32, 32, 27),
    "ship-docked": (48, 48, 42),
}
for d in ("right", "left", "down", "up"):
    for f in (0, 1):
        SPEC[f"airship-{d}-{f}"] = (40, 40, None)
SPEC["airship-shadow"] = (24, 10, None)
SPEC["airship-landed"] = (48, 48, 44)
SPEC["spire"] = (64, 112, 111)
for n in ("ruin", "cave", "shrine", "fort"):
    SPEC[f"islet-{n}"] = (48, 48, None)
SPEC["whirlpool-ring"] = (48, 48, None)


def collect():
    items = {}
    items.update(ships.make())
    try:
        import airships; items.update(airships.make())
    except ImportError:
        pass
    try:
        import spire; items.update(spire.make())
    except ImportError:
        pass
    try:
        import islets; items.update(islets.make())
    except ImportError:
        pass
    return items


def main():
    items = collect()
    errs = []
    sheet = {}
    for name, cv in items.items():
        rows = cv.rows()
        w, h, foot = SPEC[name]
        if len(rows) != h or any(len(r) != w for r in rows):
            errs.append(f"{name}: 大きさが {w}x{h} ではない")
        used = sorted({ch for r in rows for ch in r if ch != "."})
        miss = [ch for ch in used if ch not in PAL]
        if miss:
            errs.append(f"{name}: パレットにない文字 {miss}")
        if len(used) > 16:
            errs.append(f"{name}: 色が {len(used)} 色（16色まで）")
        ys = [y for y, r in enumerate(rows) if any(ch != "." for ch in r)]
        if not ys:
            errs.append(f"{name}: 空っぽ")
            continue
        # 足元＝泡（C/c）・水（L/l）を除いた最下行（縁取りを含む）。目安±1に収める
        solid = [y for y, r in enumerate(rows) if any(ch not in ".CcLl" for ch in r)]
        if foot is not None and abs(max(solid) - foot) > 1:
            errs.append(f"{name}: 足元がずれている（泡を除く最下行 y={max(solid)}、目安 {foot}）")
        open(f"{name}.txt", "w").write("\n".join(rows) + "\n")
        json.dump({k: PAL[k] for k in used if k in PAL}, open(f"pal-{name}.json", "w"))
        sheet[name] = (cv, len(used), max(ys))
        print(f"{name:18s} {w}x{h} 色={len(used):2d} 最下行={max(ys)}")
    preview(sheet)
    if errs:
        print("\n".join("NG " + e for e in errs)); sys.exit(1)
    print("OK:", len(sheet), "枚")


def render(cv, scale=4):
    im = Image.new("RGBA", (cv.w, cv.h), (0, 0, 0, 0))
    for y, r in enumerate(cv.g):
        for x, ch in enumerate(r):
            if ch != ".":
                hx = PAL[ch].lstrip("#")
                im.putpixel((x, y), (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 255))
    return im.resize((cv.w * scale, cv.h * scale), Image.NEAREST)


def preview(sheet, scale=4, bg=(46, 98, 150)):
    order = [n for n in sheet if n != "spire"] + (["spire"] if "spire" in sheet else [])
    groups = []
    cur, wsum = [], 0
    maxw = 1500
    for n in order:
        cv = sheet[n][0]
        if cur and (wsum + cv.w * scale + 8 > maxw):
            groups.append(cur); cur, wsum = [], 0
        cur.append(n); wsum += cv.w * scale + 8
    if cur: groups.append(cur)
    H = sum(max(sheet[n][0].h for n in g) * scale + 22 for g in groups) + 8
    im = Image.new("RGB", (maxw + 8, H), bg)
    d = ImageDraw.Draw(im)
    y = 4
    for g in groups:
        x = 4
        rh = max(sheet[n][0].h for n in g) * scale
        for n in g:
            cv = sheet[n][0]
            r = render(cv, scale)
            im.paste(r, (x, y + rh - r.height + 14), r)
            d.text((x, y), n, fill=(255, 255, 255))
            x += cv.w * scale + 8
        y += rh + 22
    im.save("preview.png")


if __name__ == "__main__":
    main()
