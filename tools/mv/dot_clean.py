"""人物の上を通る金色の光のつぶ・雪のつぶ（1〜2 コマで通りすぎる小さな明るい点）だけを消す（2026-11-11『白い息のリテイク』作り直し）。
  人間「ダメだこのままじゃ使えない。。。1番最初の動画で最初から調整し直した方がいいかも」
  前の作り方は、光がかぶった所を「ほかのコマの絵を曲げて持ってくる」大きな置きかえで直していたので、動かすと服や髪の模様がゆらいで見えた。
  ここでは、人物の絵はそのまま。前後 4 コマずつ（頭の動きぶんだけ ずらして重ねる）の中央値より はっきり明るい「点」の所だけを、その中央値に置きかえる。
  顔（目・口が動く所）にはさわらない。直した点の数（コマごと）と、金色のつぶとして直した画素の数を npy に書く。
  python3 dot_clean.py <コマのフォルダ> <人物の形 npy> <追跡 json> <出力フォルダ> <点の数 npy>
"""
import sys, os, json, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_util as PU
SRC, PM, TRK, DST, OUT = sys.argv[1:6]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); K = len(P); trk = json.load(open(TRK))
dx = np.array([t[1] for t in trk], float); dy = np.array([t[2] for t in trk], float)
F = [cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in range(K)]
R = int(os.environ.get("DC_R", "4")); T = float(os.environ.get("DC_T", "14"))
FACE = (slice(190, 338), slice(530, 740))
HEAVY = set(range(44, 82)) | set(range(104, 146)) | set(range(176, 214))   # 光の帯が人物にかかるコマ
stat = np.zeros((K, 2), int)
for k in range(K):
    nb = []
    RR = R * 2 if k in HEAVY else R                                        # 光の帯のコマは、つぶが同じ所に長く居るので、前後 8 コマずつ見る
    for j in range(max(0, k - RR), min(K, k + RR + 1)):
        if j == k: continue
        M = np.float32([[1, 0, dx[k] - dx[j]], [0, 1, dy[k] - dy[j]]])
        nb.append((abs(j - k), cv2.warpAffine(F[j], M, (F[j].shape[1], F[j].shape[0]), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)))
    ref = np.median(np.stack([x[1] for x in nb]), 0).astype(np.float32); f = F[k].astype(np.float32)
    # うめる色: 中央値そのもの（何コマも まぜた色）は ぼけるので、「中央値に近い色をしている、いちばん近いコマ」の色をそのまま使う
    fill = ref.copy(); done = np.zeros(ref.shape[:2], bool)
    for _, im in sorted(nb, key=lambda x: x[0]):
        ok = (np.abs(im.astype(np.float32) - ref).max(2) < T * 0.5) & ~done
        fill[ok] = im[ok]; done |= ok
    dd = f - ref; d = dd.max(2)                                            # 明るくなったぶん
    dmin = dd.min(2)                                                       # 光・雪は白〜金色なので、赤・緑・青のどれも明るくなる（腕の「04」・目・服のふちの動きは、どれかの色が変わらない）
    # ふちの動きで出る細い線ではなく「点」: 少しぼかした差も大きい所
    d = np.minimum(d, cv2.GaussianBlur(d, (0, 0), 1.0) * 1.6)
    near = cv2.dilate(P[k], cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(os.environ.get("DC_NEAR", "91")),) * 2)) > 100
    m = (d > T) & (dmin > T * 0.4) & near
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    if k in HEAVY:
        # 光の帯が人物にかかるコマ: つぶが重なって大きなかたまりになるので、「小さな点だけ」「どの色も明るい」の決まりでは残る。
        # ここだけは、明るくなった所をすべて直す
        # ただし、光が通る場所（手・胸の前／あごの右とマフラー）の中だけ。腕は頭とちがう動きをするので、前後のコマと重ねると「04」やふちがにじむ
        zone = np.zeros(d.shape, np.uint8)
        if 104 <= k < 146: zone[330:570, 480:715] = 1; zone[290:400, 480:770] = 1
        else: zone[240:400, 590:820] = 1; zone[400:440, 590:735] = 1
        m = np.where(zone > 0, ((d > T) & near), PU.blobs(m) > 0).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    else:
        m = PU.blobs(m)                                                    # 小さな点だけ。体や手が動いてできる細長い差（ふち）は直さない（直すと ふちが遅れて見える）
    m[FACE] = 0
    m[396:486, 724:822] = 0                                                # 腕の「04」のまわりは直さない（腕は頭とちがう動きをするので、前後のコマの文字がずれて重なり、にじむ）
    stat[k, 0] = int(m.sum())
    a = cv2.GaussianBlur(cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))).astype(np.float32), (0, 0), 1.2)[..., None]
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", np.clip(f * (1 - a) + fill * a, 0, 255).astype(np.uint8))
np.save(OUT, stat)
for a in range(0, K, 24): print(a, stat[a:a + 24:2, 0].tolist(), "金色", stat[a:a + 24:2, 1].tolist())
