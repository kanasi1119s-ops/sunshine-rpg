"""参考画像を拡大して見る・小さな絵を表示用に拡大する。使い方: python3 zoom.py 入力.png 出力.png [倍率] [クロップ x,y,w,h]"""
import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
z = int(sys.argv[3]) if len(sys.argv) > 3 else 8
im = Image.open(src).convert("RGBA")
if len(sys.argv) > 4:
    x, y, w, h = map(int, sys.argv[4].split(","))
    im = im.crop((x, y, x + w, y + h))
bg = Image.new("RGBA", im.size, (61, 49, 96, 255)); bg.alpha_composite(im)
bg.resize((im.width * z, im.height * z), Image.NEAREST).convert("RGB").save(out)
print(im.size)
