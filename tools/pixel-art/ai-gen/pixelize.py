"""AIが描いた「ドット絵風」の画像を、本物のドット絵に仕上げる（背景の除去・マス目合わせ・減色・半透明の除去）。

使い方:
  python3 pixelize.py raw/*.png                       # 48px・12色・かんたんな背景除去
  python3 pixelize.py --size 64 --colors 16 --rembg raw/*.png   # 戦闘の敵向け（64px・16色・AIで背景除去）

--rembg: 背景が白一色でない（景色や地面が描かれた）下絵のときに使う。
  rembg（MITライセンス）と isnet-general-use モデル（Apache-2.0）を使う。
  入れ方: pip install --break-system-packages rembg onnxruntime（初回にモデル約180MBを自動で取得）
"""
import argparse
import os
import numpy as np
from PIL import Image
from scipy import ndimage

_SESSION = None


def _keep_main(mask):
    """一番大きなかたまりと、それに近い大きさのものだけ残す（ちり・地面のかけらを消す）。"""
    lab, n = ndimage.label(mask)
    if n > 1:
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s >= sizes.max() * 0.03]
        mask = np.isin(lab, keep)
    return mask


def remove_bg(im, tol=40):
    """四すみの色を背景とみなし、外側からつながっている近い色を消す。"""
    a = np.asarray(im.convert('RGB')).astype(int)
    corners = np.array([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]])
    bg = np.median(corners, axis=0)
    near = (np.abs(a - bg).sum(2) < tol)
    lab, n = ndimage.label(near)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    mask = ~np.isin(lab, list(edge))
    mask = ndimage.binary_opening(mask, iterations=2)
    mask = _keep_main(mask)
    return Image.fromarray(np.dstack([a, mask * 255]).astype(np.uint8), 'RGBA')


def remove_bg_ai(im):
    """AIの切り抜き（rembg）で背景を消す。景色が描かれた下絵向け。"""
    global _SESSION
    from rembg import remove, new_session
    if _SESSION is None:
        _SESSION = new_session("isnet-general-use")
    out = np.asarray(remove(im.convert('RGB'), session=_SESSION)).copy()
    mask = _keep_main(ndimage.binary_opening(out[:, :, 3] >= 128, iterations=1))
    out[:, :, 3] = mask * 255
    return Image.fromarray(out, 'RGBA')


def pixelize(src, size=48, colors=12, ai_bg=False):
    im = Image.open(src)
    im = remove_bg_ai(im) if ai_bg else remove_bg(im)
    im = im.crop(im.getbbox())
    w, h = im.size
    s = (size - 2) / max(w, h)          # 外周に1ドットの余白を残す
    tw, th = max(1, round(w * s)), max(1, round(h * s))
    # マス目合わせ: 1マスの中の平均（BOX）で縮める。透明度は半分を境に、ある／なしにする
    small = np.asarray(im.resize((tw, th), Image.BOX)).copy()
    alpha = small[:, :, 3] >= 128
    # 減色は「見える画素」だけで色を選ぶ（背景の色でパレットをむだにしない）
    vis = small[:, :, :3][alpha].reshape(1, -1, 3)
    pal_img = Image.fromarray(vis.astype(np.uint8)).quantize(colors=colors, method=Image.Quantize.MEDIANCUT, kmeans=3)
    q = np.asarray(Image.fromarray(small[:, :, :3]).quantize(palette=pal_img, dither=Image.Dither.NONE).convert('RGB'))
    out = np.dstack([q, alpha * 255]).astype(np.uint8)
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    canvas.paste(Image.fromarray(out, 'RGBA'), ((size - tw) // 2, size - 1 - th))
    return canvas


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('--size', type=int, default=48)
    ap.add_argument('--colors', type=int, default=12)
    ap.add_argument('--rembg', action='store_true', help='AIで背景を消す（景色のある下絵向け）')
    ap.add_argument('--out', default='px')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for f in a.files:
        n = os.path.splitext(os.path.basename(f))[0]
        p = pixelize(f, a.size, a.colors, a.rembg)
        p.save(f'{a.out}/{n}.png')
        cols = len({c for c in p.getdata() if c[3]})
        print(n, cols, '色')
