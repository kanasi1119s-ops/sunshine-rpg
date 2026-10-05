"""採用した積乱雲の形を、自然なまま変える（2026-10-05、人間の指示「採用した雲、自然な形で形を変えて」）。
前の試し（shape.py、段ごとにのばす・ちぢめる）は、ゆがんで不自然だったので使わない。ここでは:
- 写真の雲の一部分を、そのままの縦横の比（ゆがめない）で切り出し、重ねて、新しい形の雲を組む。
  1) 本体: 写真の雲ぜんぶ（下に置く）。
  2) 立ち上がる頭: 写真の雲の上のもくもく（白く光る所）を少し小さくして、本体のうしろ・左寄りに置く。
     本体の上から、もう一段、高くもり上がる（雲が上へのびていく途中の形）。うしろに置くので、つなぎめは本体のもくもくでかくれる。
  3) 右の張り出しは少しけずって、左右の形を変える。
- 重ねた絵（composite.png、空は写真の空の色）を、wide.py と同じやり方でドットにする（reshape.py）。"""
from PIL import Image, ImageFilter

photo = Image.open("ref-photo.png").convert("RGB")
crop = photo.crop((28, 0, 412, 262))
SKY = (32, 62, 120)
CW, CH = 384, 384


def alpha_of(img, top_rows=0):
    """雲らしさ（空は0、雲は255）。写真の色の『青さ』から。ふちはなめらか。"""
    a = Image.new("L", img.size)
    src = img.load()
    out = a.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = src[x, y]
            v = (78 - (b - r)) / 34
            if y < top_rows and b - r > 28:
                v = 0                                # 上のほうの青い所は空（写真のすみの暗い空と、右上のうすいかすみ）
            if r + g + b < 30:
                v = 0
            out[x, y] = int(max(0.0, min(1.0, v)) * 255)
    return a.filter(ImageFilter.GaussianBlur(0.6))


canvas = Image.new("RGB", (CW, CH), SKY)
# 2) 立ち上がる頭（うしろ）: 写真の雲の上のもくもく
head = crop.crop((50, 18, 290, 128))
k = 0.82
head = head.resize((int(head.width * k), int(head.height * k)), Image.LANCZOS)
ha = alpha_of(head, 999)
# 頭の下のほうは、だんだん消す（本体のうしろへ入っていく）
hm = ha.load()
import math
for y in range(head.height):
    for x in range(head.width):
        # だ円の形でふちを消す（切り出した四角のはしが見えないように）。下は本体のうしろへ入る
        u = (x + 0.5 - head.width / 2) / (head.width / 2)
        v = (y + 0.5 - head.height * 0.35) / (head.height * 0.65)
        d = math.sqrt(u * u + max(0.0, v) ** 2 * 1.0)
        f = max(0.0, min(1.0, (1.0 - d) / 0.3))
        hm[x, y] = int(hm[x, y] * f)
canvas.paste(head, (44, 96), ha)
# 1) 本体（まえ）
body = crop.copy()
ba = alpha_of(body, 110)
# 3) 右の張り出しを少しけずる（右はしを、上から下へななめに消す）
bm = ba.load()
for y in range(body.height):
    cut = body.width - 18 - int(max(0, 120 - y) * 0.35)
    for x in range(cut, body.width):
        bm[x, y] = int(bm[x, y] * max(0.0, 1 - (x - cut) / 14))
canvas.paste(body, (0, CH - body.height), ba)
canvas.save("composite.png")
print("ok")
