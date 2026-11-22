"""エディタで保存した作品（JSON）から、確認用の絵・等倍シート・見本GIFを作る。使い方: python3 render.py <作品.json> <出力フォルダ> <名前>"""
import json, sys
from PIL import Image
d = json.load(open(sys.argv[1], encoding="utf-8")); OUT, name = sys.argv[2], sys.argv[3]; W, H = d["width"], d["height"]
col = {s["sym"]: tuple(int(s["color"][i:i + 2], 16) for i in (1, 3, 5)) + (255,) for s in d["symbols"]}
def img(fi, z):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for layer in reversed(d["cels"]) if False else d["cels"]:
        for y, r in enumerate(layer[fi]):
            for x, ch in enumerate(r):
                if ch in col: im.putpixel((x, y), col[ch])
    return im.resize((W * z, H * z), Image.NEAREST)
n = len(d["frames"]); z = 8; BG = (104, 100, 92, 255); cols = int(sys.argv[4]) if len(sys.argv) > 4 else n; rows = n // cols
sheet = Image.new("RGBA", (W * z * cols, H * z * rows), BG); raw = Image.new("RGBA", (W * cols, H * rows), (0, 0, 0, 0)); fs = []
for i in range(n):
    cx, cy = i % cols, i // cols
    sheet.alpha_composite(img(i, z), (cx * W * z, cy * H * z)); raw.alpha_composite(img(i, 1), (cx * W, cy * H))
    f = Image.new("RGBA", (W * 12, H * 12), BG); f.alpha_composite(img(i, 12)); fs.append(f.convert("P", palette=Image.ADAPTIVE))
sheet.save(f"{OUT}/{name}_確認用（{n}コマ）.png"); raw.save(f"{OUT}/{name}_シート（等倍・透明）.png")
mouth = [0, 1, 0, 3, 5, 1, 2, 4, 1, 0, 6, 0, 5, 3, 1, 0]
seq = [((t // 2) % rows) * cols + mouth[t % len(mouth)] if rows > 1 else mouth[t % len(mouth)] for t in range(32 if rows > 1 else 16)]
fs[seq[0]].save(f"{OUT}/{name}_歌っている見本.gif", save_all=True, append_images=[fs[i] for i in seq[1:]], duration=170, loop=0)
