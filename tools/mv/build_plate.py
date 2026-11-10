"""人物も雪もない背景の絵（1枚）を作る（2026-11-11『白い息のリテイク』。人間「テト周辺の背景がボロボロだね」）。
  はじめの作り方は「人物に隠れていないコマの中央値」だったが、人物のすぐそばは見えているコマが少なく、
  そこに白い息・光のつぶが重なったコマが多いので、もやのかけらが背景に焼きついていた。
    ・雪・白い息・光のつぶはどれも「明るくなる」ものなので、中央値ではなく、暗いほうから 30% の値を使う
    ・見えているコマが少ない所（人物のそば・後ろ）は信用せず、左右の信用できる背景から横につないでうめる
      （この場面の後ろは、駅の屋根・ホーム・雪の地面と、横に長いものがぼけて写っている）。そのあと縦に少しぼかしてなじませる
  python3 build_plate.py <コマのフォルダ（カメラを止めたもの）> <人物の形 npy> <出力 png>
"""
import sys, os, cv2, numpy as np
SRC, PM, OUT = sys.argv[1:4]
P = np.load(PM); K = len(P); ks = list(range(0, K, 2)); H, W = P.shape[1:]
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
fr = np.stack([cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in ks])
DIL = int(os.environ.get("PLATE_DIL", "17")); MINC = int(os.environ.get("PLATE_MIN", "10"))
# 2026-11-11 人間「肩周りの背景がぼやけてるから、もっと他の部分の背景と違和感ないように」: はじめは人物から 20px はなれ、半分以上のコマで
#   見えている所だけを本物の背景として使い、残り（画面の 22%）を横につないでうめていたので、肩のまわりが広くぼけていた。
#   人物から 8px はなれていて、10 コマ以上見えていれば本物の背景を使う（もやは「暗いほうから 30%」で除ける）。うめるのは本当に隠れた所だけ
vis = np.stack([cv2.dilate(P[k], EL(DIL)) < 20 for k in ks])
cnt = vis.sum(0); plate = np.zeros((H, W, 3), np.float32)
for y0 in range(0, H, 40):
    f = fr[:, y0:y0 + 40].astype(np.float32); f[~vis[:, y0:y0 + 40]] = np.nan
    with np.errstate(all="ignore"):
        p30 = np.nan_to_num(np.nanpercentile(f, 30, axis=0)); p15 = np.nan_to_num(np.nanpercentile(f, 15, axis=0))
    few = (cnt[y0:y0 + 40] < len(ks) * 0.5)[..., None]             # 見えているコマが少ない所（人物の際）は、もやが残りやすいので、もっと暗いほうの値
    plate[y0:y0 + 40] = np.where(few, p15, p30)
# 2026-11-11 人間「もっと際まで完全に」: 人物の際は見えているコマが少なく、白い点（もや・髪の先）が線のように残っていた。
#   際の帯だけ、小さな点を取りのぞく（5px の中央値）。ほかの所はそのまま（ぼかさない）
band = ((cnt >= MINC) & (cnt < len(ks) * 0.5))
md = cv2.medianBlur(np.clip(plate, 0, 255).astype(np.uint8), 5).astype(np.float32)
plate = np.where(band[..., None], md, plate)
good = cnt >= MINC
hole = ~good
cv2.imwrite(OUT + ".raw.png", np.clip(plate, 0, 255).astype(np.uint8)); cv2.imwrite(OUT + ".hole.png", hole.astype(np.uint8) * 255)   # lama_fill.py 用
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
hm = (cv2.GaussianBlur(hole.astype(np.float32), (0, 0), 4) * hole)[..., None]      # 穴の外（本物の背景）はぼかさない
bl = cv2.GaussianBlur(out, (0, 0), sigmaX=2, sigmaY=5)
out = out * (1 - hm) + bl * hm
# 2026-11-11 人間「肩周りの背景がぼやけてる」: 横につないだだけだと、うめた所だけ のっぺりして、となりの本物の背景（窓・柱・屋根の線）と
#   細かさがちがって見える。人物の後ろのいちばん大きい穴は、左右の本物の背景を「鏡うつし」にして持ってくる
#   （境目のすぐ内側が、すぐ外側と同じ細かさ・同じ明るさになる）。まん中（いつも人物に隠れている）で左右をまぜる
from scipy.ndimage import minimum_filter1d, maximum_filter1d, gaussian_filter1d
A = np.full(H, -1.0); B = np.full(H, -1.0)
for y in range(H):
    xs = np.where(hole[y])[0]
    if len(xs) < 30: continue
    segs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1); sg = max(segs, key=len)
    if len(sg) >= 30: A[y], B[y] = sg[0], sg[-1]
ys = np.where(A >= 0)[0]
if len(ys):
    y0, y1 = ys[0], ys[-1]; a = A[y0:y1 + 1].copy(); b = B[y0:y1 + 1].copy()
    bad = a < 0; a[bad] = np.interp(np.where(bad)[0], np.where(~bad)[0], a[~bad]); b[bad] = np.interp(np.where(bad)[0], np.where(~bad)[0], b[~bad])
    ax_l = gaussian_filter1d(minimum_filter1d(a, 31), 12) - 2          # 鏡の軸（なめらかな線。穴の外側＝本物の背景の上に置く）
    ax_r = gaussian_filter1d(maximum_filter1d(b, 31), 12) + 2
    base = out.copy(); xx = np.arange(W, dtype=np.float32)
    for i, y in enumerate(range(y0, y1 + 1)):
        if bad[i]: continue
        xa, xb = int(A[y]), int(B[y]); x = xx[xa:xb + 1]
        sl = np.clip(2 * ax_l[i] - x, 0, W - 1).astype(np.float32); sr = np.clip(2 * ax_r[i] - x, 0, W - 1).astype(np.float32)
        rowf = base[y][None].astype(np.float32)
        ml = cv2.remap(rowf, sl[None], np.zeros((1, len(x)), np.float32), cv2.INTER_LINEAR)[0]
        mr = cv2.remap(rowf, sr[None], np.zeros((1, len(x)), np.float32), cv2.INTER_LINEAR)[0]
        t = ((x - xa + 1) / (xb - xa + 2))[:, None]; t = np.clip((t - 0.3) / 0.4, 0, 1); t = t * t * (3 - 2 * t)
        mir = ml * (1 - t) + mr * t
        # 鏡うつしは境目から 45px まで（そこから 70px までで、横につないだ絵へもどす）。遠くの物（街灯の柱など）まで うつしこまない
        d = np.minimum(x - ax_l[i], ax_r[i] - x); lim = 34 if y < 300 else 70                                   # 頭の高さは街灯の柱が近いので、浅くする
        m = np.clip((lim - d) / 20, 0, 1)[:, None]; m = m * m * (3 - 2 * m)
        out[y, xa:xb + 1] = mir * m + base[y, xa:xb + 1] * (1 - m)
cv2.imwrite(OUT, np.clip(out, 0, 255).astype(np.uint8)); print("うめた広さ %.1f%%" % (100 * hole.mean()), "→", OUT)
