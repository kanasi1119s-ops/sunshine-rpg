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
n = len(d["frames"]); z = 12; BG = (104, 100, 92, 255)
sheet = Image.new("RGBA", (W * z * n, H * z), BG); raw = Image.new("RGBA", (W * n, H), (0, 0, 0, 0)); fs = []
for i in range(n):
    sheet.alpha_composite(img(i, z), (i * W * z, 0)); raw.alpha_composite(img(i, 1), (i * W, 0))
    f = Image.new("RGBA", (W * z, H * z), BG); f.alpha_composite(img(i, z)); fs.append(f.convert("P", palette=Image.ADAPTIVE))
sheet.save(f"{OUT}/{name}_確認用（口の形{n}コマ）.png"); raw.save(f"{OUT}/{name}_シート（等倍・透明）.png")
seq = [0, 1, 0, 3, 5, 1, 2, 4, 1, 0, 6, 0, 5, 3, 1, 0]
fs[0].save(f"{OUT}/{name}_歌っている見本.gif", save_all=True, append_images=[fs[i] for i in seq[1:]], duration=[120 if i == 6 else 180 for i in seq], loop=0)
