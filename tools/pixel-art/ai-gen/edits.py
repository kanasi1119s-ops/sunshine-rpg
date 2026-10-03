"""手直し: 文字グリッドに点を打ち直す。使い方: python3 edits.py 名前 編集.json  → 名前_fix.{txt,json,png}
編集.json: {"palette": {"U": "#ff6a1a"}, "pixels": [[行, 列, "記号"], ...], "rects": [[行0, 列0, 行1, 列1, "記号"]]}"""
import sys, json
from PIL import Image
n, ef = sys.argv[1], sys.argv[2]
rows = [list(r) for r in open(f"{n}.txt").read().split("\n") if r]
pal = json.load(open(f"{n}.json")); e = json.load(open(ef))
pal.update(e.get("palette", {}))
for r0, c0, r1, c1, ch in e.get("rects", []):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1): rows[r][c] = ch
for r, c, ch in e.get("pixels", []): rows[r][c] = ch
for r0, c0, r1, c1, syms in e.get("erase", []):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if rows[r][c] in syms: rows[r][c] = "."
used = {ch for r in rows for ch in r} - {"."}
pal = {k: v for k, v in pal.items() if k in used}
open(f"{n}_fix.txt", "w").write("\n".join("".join(r) for r in rows) + "\n")
json.dump(pal, open(f"{n}_fix.json", "w"))
im = Image.new("RGBA", (len(rows[0]), len(rows)))
for y, r in enumerate(rows):
    for x, ch in enumerate(r):
        if ch != ".": im.putpixel((x, y), tuple(int(pal[ch][i:i+2], 16) for i in (1, 3, 5)) + (255,))
im.save(f"{n}_fix.png"); print(n, len(pal), "色")
