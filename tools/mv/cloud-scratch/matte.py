# 元の動画のコマ（白い背景）からテトを切り抜き、縮めた RGBA にする
import sys, cv2, numpy as np, os
SRC, OUT, SC = sys.argv[1], sys.argv[2], float(sys.argv[3]); os.makedirs(OUT, exist_ok=True)
ks = [int(a) for a in sys.argv[4:]] or range(240)
for k in ks:
    im = cv2.imread(f"{SRC}/{k+1:03d}.png")
    h, w = im.shape[:2]
    mn = im.min(2).astype(np.int16); sat = (im.max(2).astype(np.int16) - mn)
    white = ((mn > 232) & (sat < 14)).astype(np.uint8)
    # 外側の白（ふちにつながっている白）だけを背景にする
    ff = white.copy(); mask = np.zeros((h + 2, w + 2), np.uint8)
    for (x, y) in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if ff[y, x] == 1: cv2.floodFill(ff, mask, (x, y), 2)
    bg = (ff == 2).astype(np.uint8)
    # 体の内側に残った大きな白（腕と体のすきまなど）も背景に
    # 体の内側に残った白（髪の巻きのすきま・腕と体のすきまなど）も背景に。ただしリボン（頭の右上）は残す
    import json as _j
    TR = _j.load(open("/home/claude/wt-mix/tools/mv/track_teto_a.json"))
    mx, my = 342 + TR[k][1], 291 + TR[k][2]                       # 口の位置（追跡）。リボンはここから右上
    rib = np.zeros((h, w), np.uint8); rib[max(0, my - 205):my - 75, mx + 70:mx + 185] = 1
    rib[max(0, my - 100):my - 25, max(0, mx - 88):mx + 88] = 1     # 目（白目）も残す
    whitish = ((mn > 200) & (sat < 30)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(whitish * (1 - bg))
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    hair = (((hsv[..., 0] < 12) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 90) & (hsv[..., 2] > 50)).astype(np.uint8)
    for i in range(1, n):
        x, y, w_, h_, area = st[i]
        comp = lab[max(0, y - 6):y + h_ + 6, max(0, x - 6):x + w_ + 6] == i
        if rib[max(0, y - 6):y + h_ + 6, max(0, x - 6):x + w_ + 6][comp].mean() > 0.3: continue      # リボンは残す
        if area > 900: bg[lab == i] = 1; continue
        m = comp.astype(np.uint8)
        ring = cv2.dilate(m, np.ones((7, 7), np.uint8)) - m
        hr = hair[max(0, y - 6):y + h_ + 6, max(0, x - 6):x + w_ + 6][ring > 0]
        if len(hr) and hr.mean() > 0.3: bg[lab == i] = 1          # まわりが髪 → 髪のすきまの白（背景）
    # 背景のとなりの、白に近いにじみ（明るくて色の薄い所）も背景に（リボンの所はのぞく）
    pale = ((mn > 205) & (sat < 30)).astype(np.uint8) * (1 - rib)
    for _ in range(2):
        bg = np.maximum(bg, pale * cv2.dilate(bg, np.ones((3, 3), np.uint8)))
    fg = 1 - bg
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    a = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 1.0)
    # 縁の白いにじみを取る: 縁の色を、少し内側の色に寄せる
    a = np.clip((a - 0.3) / 0.6, 0, 1)
    inner = cv2.erode(fg, np.ones((5, 5), np.uint8))
    col = im.astype(np.float32)
    blur = cv2.blur(col * inner[..., None], (9, 9)); wgt = cv2.blur(inner.astype(np.float32), (9, 9))[..., None]
    fill = np.where(wgt > 0.05, blur / np.maximum(wgt, 1e-3), col)
    edge = ((a > 0) & (inner == 0))[..., None]
    col = np.where(edge, fill, col)
    rgba = np.dstack([col, a * 255]).clip(0, 255).astype(np.uint8)
    rgba = cv2.resize(rgba, (int(w * SC), int(h * SC)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"{OUT}/{k:03d}.png", rgba)
