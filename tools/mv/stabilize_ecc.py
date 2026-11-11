"""元の動画のカメラのゆれを、コマごとに背景へぴったり合わせて止める（2026-11-11『白い息のリテイク』作り直し。人間「違和感あるね。ぼやけたり、ズレたり」）。
  stabilize_frames.py は、カメラの動きを「なめらかな 3 次の曲線」とみなして直していたが、本当のカメラは 2〜4 秒の周期で ±1.4px ゆれていて、
  直したあとも背景が 3px ほど行き来していた。テトのまわりだけ別のコマに入れかえる今の作り方では、そのずれが輪郭のまわりの「ズレ」に見える。
  ここでは、コマごとに背景（人物の外・雪は小さな中央値で消す）を、見本の背景 1 枚に合わせる変形（平行移動・倍率・回転・ゆがみ）を測る（ECC）。
  測った値は前後 5 コマでならし（測りまちがいで細かくふるえないように）、元のコマから 1 回だけ、するどい補間（Lanczos）で作る（ぼけを足さない）。
  python3 stabilize_ecc.py <元のコマのフォルダ> <見本の背景 png> <人物の形 npy（だいたいでよい）> <出力フォルダ>
"""
import sys, os, cv2, numpy as np
SRC, PLATE, PM, DST = sys.argv[1:5]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); K = len(P)
prep = lambda g: cv2.GaussianBlur(cv2.medianBlur(g, 5), (0, 0), 1.5).astype(np.float32)
ref = prep(cv2.cvtColor(cv2.imread(PLATE), cv2.COLOR_BGR2GRAY)); H, W = ref.shape
crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 120, 1e-6)
Ws = []; ccs = []; Wp = np.eye(2, 3, dtype=np.float32)
for k in range(K):
    g = prep(cv2.cvtColor(cv2.imread(f"{SRC}/{k + 1:03d}.png"), cv2.COLOR_BGR2GRAY))
    m = (cv2.dilate(P[k], np.ones((101, 101), np.uint8)) < 50).astype(np.uint8); m[:24] = 0; m[-24:] = 0; m[:, :24] = 0; m[:, -24:] = 0
    m[600:] = 0                                             # 下は生成AIの文字が出るコマがある
    Wk = Wp.copy()
    if k == 0:                                              # はじめは粗い絵から（元のコマは 12px ほどずれている）
        s = 0.25; rs = cv2.resize(ref, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); gs = cv2.resize(g, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        ms = cv2.resize(m, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)
        _, w0 = cv2.findTransformECC(rs, gs, np.eye(2, 3, dtype=np.float32), cv2.MOTION_AFFINE, crit, ms, 3)
        Wk = w0.copy(); Wk[:, 2] /= s
    cc, Wk = cv2.findTransformECC(ref, g, Wk, cv2.MOTION_AFFINE, crit, m, 5)
    Ws.append(Wk.copy()); ccs.append(cc); Wp = Wk
Ws = np.array(Ws)
ker = np.array([1, 2, 3, 2, 1], np.float32); ker /= ker.sum()
Wsm = np.stack([np.convolve(np.pad(Ws[:, i, j], 2, mode="edge"), ker, mode="valid") for i in range(2) for j in range(3)], 1).reshape(K, 2, 3)
print("合った度合い 最小 %.3f・ならす前後の差 最大 %.2fpx" % (min(ccs), np.abs(Ws[:, :, 2] - Wsm[:, :, 2]).max()))
for k in range(K):
    img = cv2.imread(f"{SRC}/{k + 1:03d}.png")
    out = cv2.warpAffine(img, Wsm[k].astype(np.float32), (W, H), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", out)
np.save(DST + ".warp.npy", Wsm); print("ok", DST)
