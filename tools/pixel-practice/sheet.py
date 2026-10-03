"""トレース結果の一覧画像。使い方: python3 sheet.py トレースフォルダ 出力.png 名前... （各絵を8倍に拡大して並べる）"""
import sys
from PIL import Image
d, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
Z = 8; ims = []
for n in names:
    im = Image.open(f"{d}/{n}.png").convert("RGBA"); bg = Image.new("RGBA", im.size, (61, 49, 96, 255)); bg.alpha_composite(im)
    ims.append(bg.resize((im.width * Z, im.height * Z), Image.NEAREST).convert("RGB"))
cols = 4; W = max(i.width for i in ims) + 8; H = max(i.height for i in ims) + 8
rows = (len(ims) + cols - 1) // cols
c = Image.new("RGB", (cols * W, rows * H), (30, 24, 48))
for k, im in enumerate(ims): c.paste(im, ((k % cols) * W + 4, (k // cols) * H + 4))
c.save(out)
