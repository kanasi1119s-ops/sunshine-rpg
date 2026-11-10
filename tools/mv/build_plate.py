"""人物も雪もない背景の絵（1枚）を作る（2026-11-11『白い息のリテイク』。人間「テト周辺の背景がボロボロだね」）。
  はじめの作り方は「人物に隠れていないコマの中央値」だったが、人物のすぐそばは見えているコマが少なく、
  そこに白い息・光のつぶが重なったコマが多いので、もやのかけらが背景に焼きついていた。
    ・雪・白い息・光のつぶはどれも「明るくなる」ものなので、中央値ではなく、暗いほうから 30% の値を使う
    ・見えているコマが少ない所（人物のそば・後ろ）は信用せず、左右の信用できる背景から横につないでうめる
      （この場面の後ろは、駅の屋根・ホーム・雪の地面と、横に長いものがぼけて写っている）。そのあと縦に少しぼかしてなじませる
  python3 build_plate.py <コマのフォルダ（カメラを止めたもの）> <人物の形 npy> <出力 png>
"""
import sys, cv2, numpy as np
SRC, PM, OUT = sys.argv[1:4]
P = np.load(PM); K = len(P); ks = list(range(0, K, 2)); H, W = P.shape[1:]
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
fr = np.stack([cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in ks])
vis = np.stack([cv2.dilate(P[k], EL(41)) < 20 for k in ks])        # 人物から 20px 以上はなれた所だけ使う（もや・髪の先をよける）
cnt = vis.sum(0); plate = np.zeros((H, W, 3), np.float32)
for y0 in range(0, H, 40):
    f = fr[:, y0:y0 + 40].astype(np.float32); f[~vis[:, y0:y0 + 40]] = np.nan
    with np.errstate(all="ignore"): plate[y0:y0 + 40] = np.nan_to_num(np.nanpercentile(f, 30, axis=0))
good = cnt >= len(ks) * 0.5                                       # 半分以上のコマで見えている所だけ信用する
hole = ~good
# 横につないでうめる（行ごとに、穴の左右の信用できる色を直線でつなぐ。端の色は 9px の平均）
out = plate.copy()
for y in range(H):
    row = hole[y]
    if not row.any(): continue
    xs = np.where(row)[0]; segs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1)
    for sg in segs:
        a, b = sg[0], sg[-1]
        L = plate[y, max(0, a - 9):a][good[y, max(0, a - 9):a]]; R = plate[y, b + 1:b + 10][good[y, b + 1:b + 10]]
        if len(L) == 0 and len(R) == 0: continue
        cl = L.mean(0) if len(L) else R.mean(0); cr = R.mean(0) if len(R) else cl
        t = ((np.arange(a, b + 1) - a + 1) / (b - a + 2))[:, None]
        t = t * t * (3 - 2 * t)                                    # なめらかに
        out[y, a:b + 1] = cl * (1 - t) + cr * t
# 穴の中だけ、縦に少しぼかして行ごとのすじを消す。境目もなじませる
hm = cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 4)[..., None]
bl = cv2.GaussianBlur(out, (0, 0), sigmaX=2, sigmaY=5)
out = out * (1 - hm) + bl * hm
cv2.imwrite(OUT, np.clip(out, 0, 255).astype(np.uint8)); print("うめた広さ %.1f%%" % (100 * hole.mean()), "→", OUT)
