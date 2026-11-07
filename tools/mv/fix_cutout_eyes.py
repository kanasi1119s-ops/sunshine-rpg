# テトの切り抜きの顔の中にあいた穴（目のまわりが透明になっている所）を埋める（2026-11-07 人間「映像のテトの目かけてるよ」「素材を直して」）。
# 原因: 白い背景を切り抜くとき、白目・目の光の一部が背景と判定され、240コマ中160コマで目のまわりに透明の穴があいていた。
# 使い方: python3 fix_cutout_eyes.py <切り抜きのフォルダ> <出力フォルダ>（元の大きさ 720×1280 でも、舞台用 0.66倍でもよい）
# 顔の肌の色の領域を「穴埋め」した範囲の内側にある、透明な小さい穴だけを、まわりの色で埋めて不透明にする。
import sys, glob, numpy as np
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1], sys.argv[2]
tot = 0
for f in sorted(glob.glob(src + '/*.png')):
    im = np.array(Image.open(f)); a = im[:, :, 3]; rgb = im[:, :, :3].astype(int)
    H = im.shape[0]; k = H / 844.0          # 舞台用（高さ 844）を基準に、元の大きさ（1280）でも同じ割合で
    skin = (rgb[:, :, 0] > 190) & (rgb[:, :, 1] > 150) & (rgb[:, :, 2] > 120) & (rgb[:, :, 0] - rgb[:, :, 2] < 90) & (a > 200)
    skin[int(H * 0.35):] = False                       # 頭のあたりだけ
    lab, n = ndimage.label(skin)
    if n == 0: Image.fromarray(im).save(f.replace(src, dst)); continue
    big = 1 + int(np.argmax(ndimage.sum(skin, lab, range(1, n + 1))))
    face = ndimage.binary_fill_holes(ndimage.binary_closing(lab == big, iterations=max(2, round(6 * k))))
    hole = (a < 250) & face
    hl, hn = ndimage.label(hole)
    mask = np.zeros(a.shape, np.uint8)
    for i in range(1, hn + 1):
        m = hl == i
        if m.sum() <= 400 * k * k: mask[m] = 255
    if mask.any():
        # 埋める色: 元の動画は白い背景なので、穴の所の本当の色は「切り抜いた色を、その透けぐあいのまま白の上に重ねた色」。
        #   白目・目の光は白に、まつげや輪郭の線のふちは線の色と白が混ざった色に戻る（まわりの色でぼかして埋めると、白目が灰色っぽくなる）
        al = a.astype(float)[..., None] / 255.0
        onwhite = im[:, :, :3].astype(float) * al + 255.0 * (1 - al)
        sel = mask > 0
        im[:, :, :3][sel] = np.clip(onwhite[sel], 0, 255).astype(np.uint8)
        im[:, :, 3][sel] = 255
        tot += 1
    Image.fromarray(im).save(f.replace(src, dst))
print('穴を埋めたコマ', tot)
