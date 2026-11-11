"""人物の上を通る金色の光のつぶ・雪のつぶ（1〜2 コマで通りすぎる小さな明るい点）だけを消す（2026-11-11『白い息のリテイク』作り直し）。
  人間「ダメだこのままじゃ使えない。。。1番最初の動画で最初から調整し直した方がいいかも」
  前の作り方は、光がかぶった所を「ほかのコマの絵を曲げて持ってくる」大きな置きかえで直していたので、動かすと服や髪の模様がゆらいで見えた。
  ここでは、人物の絵はそのまま。前後 4 コマずつ（頭の動きぶんだけ ずらして重ねる）の中央値より はっきり明るい「点」の所だけを、その中央値に置きかえる。
  顔（目・口が動く所）にはさわらない。直した点の数（コマごと）と、顔にかぶった点の数を npy に書く（顔にかぶるコマは使わない判断に使う）。
  python3 dot_clean.py <コマのフォルダ> <人物の形 npy> <追跡 json> <出力フォルダ> <点の数 npy>
"""
import sys, os, json, cv2, numpy as np
SRC, PM, TRK, DST, OUT = sys.argv[1:6]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); K = len(P); trk = json.load(open(TRK))
dx = np.array([t[1] for t in trk], float); dy = np.array([t[2] for t in trk], float)
F = [cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in range(K)]
R = int(os.environ.get("DC_R", "4")); T = float(os.environ.get("DC_T", "14"))
FACE = (slice(190, 338), slice(530, 740))
stat = np.zeros((K, 2), int)
for k in range(K):
    nb = []
    for j in range(max(0, k - R), min(K, k + R + 1)):
        if j == k: continue
        M = np.float32([[1, 0, dx[k] - dx[j]], [0, 1, dy[k] - dy[j]]])
        nb.append(cv2.warpAffine(F[j], M, (F[j].shape[1], F[j].shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE))
    ref = np.median(np.stack(nb), 0).astype(np.float32); f = F[k].astype(np.float32)
    d = (f - ref).max(2)                                                   # 明るくなったぶん
    # ふちの動きで出る細い線ではなく「点」: 少しぼかした差も大きい所
    d = np.minimum(d, cv2.GaussianBlur(d, (0, 0), 1.0) * 1.6)
    near = cv2.dilate(P[k], cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(os.environ.get("DC_NEAR", "91")),) * 2)) > 100
    m = (d > T) & near
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    stat[k, 1] = int(m[FACE].sum()); m[FACE] = 0
    stat[k, 0] = int(m.sum())
    a = cv2.GaussianBlur(cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))).astype(np.float32), (0, 0), 1.2)[..., None]
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", np.clip(f * (1 - a) + ref * a, 0, 255).astype(np.uint8))
np.save(OUT, stat)
for a in range(0, K, 24): print(a, stat[a:a + 24:2, 0].tolist(), "顔", stat[a:a + 24:2, 1].tolist())
