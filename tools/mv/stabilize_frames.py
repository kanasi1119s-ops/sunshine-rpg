"""元の動画のカメラのゆっくりした寄り・横ずれを止めて、どのコマも同じカメラ位置にそろえる
（2026-11-08『白い息のリテイク』。人間「まだ動き変な部分ある」）。
  元の動画（10秒）はカメラが少しずつ寄って（約1.5%）、横に 12 ピクセルほど流れる。離れたコマどうしをつなぐと、
  そのたびに背景と体が「くっ」と寄ったり戻ったりして見えた。背景（人物の外）の点を合わせてカメラの動きを測り、
  なめらかな線に直してから、全部のコマを平均のカメラ位置に戻す（はみ出しが見えないよう 2.2% だけ寄せる）。
  python3 stabilize_frames.py <入力コマのフォルダ> <出力フォルダ> [コマ数]
"""
import sys, os, cv2, numpy as np
SRC, DST = sys.argv[1:3]; K = int(sys.argv[3]) if len(sys.argv) > 3 else 240
os.makedirs(DST, exist_ok=True)
def gray(k): return cv2.cvtColor(cv2.imread(f"{SRC}/{k + 1:03d}.png"), cv2.COLOR_BGR2GRAY)
H, W = gray(0).shape
mask = np.full((H, W), 255, np.uint8); mask[int(H * 0.11):, int(W * 0.33):int(W * 0.69)] = 0   # 人物（真ん中）はよける
orb = cv2.ORB_create(4000); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
ref_k, ref_d = orb.detectAndCompute(cv2.GaussianBlur(gray(0), (0, 0), 1.5), mask)
P = []
for k in range(K):
    if k == 0: P.append((1.0, 0.0, 0.0, 0.0)); continue
    kk, dd = orb.detectAndCompute(cv2.GaussianBlur(gray(k), (0, 0), 1.5), mask)
    m = bf.match(ref_d, dd)
    p0 = np.float32([ref_k[x.queryIdx].pt for x in m]); p1 = np.float32([kk[x.trainIdx].pt for x in m])
    M, inl = cv2.estimateAffinePartial2D(p1, p0, ransacReprojThreshold=2.0)
    s = float(np.hypot(M[0, 0], M[1, 0])); r = float(np.arctan2(M[1, 0], M[0, 0]))
    P.append((s, r, float(M[0, 2]), float(M[1, 2])))
P = np.array(P); t = np.arange(K)
# カメラの動きはゆっくりなので、3 次の曲線でならす（測りまちがいのコマに引っぱられない）
S = np.polyval(np.polyfit(t, P[:, 0], 3), t); R = np.polyval(np.polyfit(t, P[:, 1], 3), t)
TX = np.polyval(np.polyfit(t, P[:, 2], 3), t); TY = np.polyval(np.polyfit(t, P[:, 3], 3), t)
print("カメラ: 倍率 %.4f〜%.4f・横 %.1f〜%.1f・縦 %.1f〜%.1f" % (S.min(), S.max(), TX.min(), TX.max(), TY.min(), TY.max()))
def A(s, r, tx, ty): return np.array([[s * np.cos(r), -s * np.sin(r), tx], [s * np.sin(r), s * np.cos(r), ty], [0, 0, 1]])
mean = np.linalg.inv(A(S.mean(), R.mean(), TX.mean(), TY.mean()))
Z = float(os.environ.get("STAB_ZOOM", "1.022")); cx, cy = W / 2, H / 2
ZM = np.array([[Z, 0, cx * (1 - Z)], [0, Z, cy * (1 - Z)], [0, 0, 1]])
for k in range(K):
    M = ZM @ mean @ A(S[k], R[k], TX[k], TY[k])
    img = cv2.imread(f"{SRC}/{k + 1:03d}.png")
    out = cv2.warpAffine(img, M[:2], (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", out)
print("ok", DST)
