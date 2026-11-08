"""元の動画で、テトのまわりを「ぐるっと回る金色の光のつぶ（光の帯）」を消す
（2026-11-08『白い息のリテイク』。人間「ぐるっと光源が動く部分が違和感しかない」）。
  生成AIが入れた演出で、3〜6秒と8〜10秒に、光のつぶが帯になって人物のまわりを回る。
  しくみ:
    1. 人物の形を切り抜きの AI（rembg の isnet-anime）で取り、人物の外だけを直す（人物には手を加えない）
    2. 光のつぶ = 金色（赤が青よりずっと強い）で、まわりより明るい小さな点。街灯・窓の明かりのように動かない明かりは、
       光のない場面の背景（中央値）にも出ているので除く
    3. 光のつぶのまわり（帯ごと、ぼんやりした光も）を、光のない場面のコマの背景で置きかえる。
       置きかえる元のコマも時間どおり前へ進めるので、その中の雪も下へ降り続ける。境目は大きくぼかす
    4. 置きかえる場所は前後のコマとならして、ちらつかないようにする
  python3 remove_sparkle.py <コマのフォルダ（カメラを止めたもの）> <人物の形 npy> <出力フォルダ>
"""
import sys, os, cv2, numpy as np
SRC, PM, DST = sys.argv[1:4]; os.makedirs(DST, exist_ok=True)
P = np.load(PM).astype(np.float32) / 255.0; K = len(P)
F = lambda k: cv2.imread(f"{SRC}/{k + 1:03d}.png")
POOL = list(range(15, 53)) + list(range(148, 189))          # 光のつぶがない（ほぼない）コマ
med = np.median(np.stack([F(k) for k in POOL[::3]]), 0).astype(np.float32)
mw = med[..., 2] - med[..., 0]
raw = []
for k in range(K):
    f = F(k).astype(np.float32); warm = f[..., 2] - f[..., 0]
    th = cv2.morphologyEx(cv2.cvtColor(F(k), cv2.COLOR_BGR2GRAY), cv2.MORPH_TOPHAT, np.ones((11, 11), np.uint8))
    m = ((warm > 40) & (warm - mw > 25) & (th > 15) & (P[k] < 0.25)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    # つぶが集まっている所だけを帯とみなす（ばらばらの 1 点は雪の色ゆれ）
    dens = cv2.blur(m.astype(np.float32), (61, 61))
    raw.append(np.clip(dens * 120, 0, 1))
raw = np.stack(raw)
out_n = 0
for k in range(K):
    a = raw[max(0, k - 4):k + 5].max(0)                      # 前後とならす
    a = cv2.GaussianBlur(a, (0, 0), 18); a = np.clip(a * 1.6, 0, 1)
    img = F(k).astype(np.float32)
    # 人物には手を加えない（切り抜きが髪の先を取りこぼすことがあるので、少し広げ、赤い髪・マフラーの色も守る）
    prot = cv2.dilate(P[k], np.ones((13, 13), np.uint8))
    red = ((img[..., 2] - np.maximum(img[..., 1], img[..., 0])) > 45).astype(np.uint8)
    red = cv2.dilate(cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), np.ones((9, 9), np.uint8)).astype(np.float32)
    a = a * (1 - cv2.GaussianBlur(np.maximum(prot, red), (0, 0), 3))
    if a.max() < 0.02: cv2.imwrite(f"{DST}/{k + 1:03d}.png", img.astype(np.uint8)); continue
    c = POOL[k % len(POOL)]
    fill = F(c).astype(np.float32)
    pc = cv2.GaussianBlur(P[c], (0, 0), 3)[..., None]       # 置きかえ元のコマの人物の所は、背景の中央値で
    fill = fill * (1 - pc) + med * pc
    out = img * (1 - a[..., None]) + fill * a[..., None]
    # 人物（マフラーなど）の上に重なった金色のつぶは、小さな点だけを周りの色でうめる（光の帯がある場面だけ）
    near = cv2.dilate((raw[max(0, k - 4):k + 5].max(0) > 0.05).astype(np.uint8), np.ones((81, 81), np.uint8))
    g8 = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(g8, cv2.MORPH_TOPHAT, np.ones((7, 7), np.uint8))
    dot = ((out[..., 1] - out[..., 0]) > 45) & (out[..., 1] > 110) & (th > 20) & (P[k] > 0.5) & (near > 0)
    dot = cv2.dilate(dot.astype(np.uint8), np.ones((5, 5), np.uint8))
    if dot.sum(): out = cv2.inpaint(np.clip(out, 0, 255).astype(np.uint8), dot * 255, 3, cv2.INPAINT_TELEA).astype(np.float32)
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", np.clip(out, 0, 255).astype(np.uint8)); out_n += 1
print("直したコマ", out_n, "→", DST)
