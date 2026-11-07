"""生成AIが勝手に入れた文字（白い息のリテイクの元の動画 15〜111 コマの「静にの使って…」）を消す（2026-11-08）。
人間「途中でスカートとか乱れるグラフィックどうにかして」: 1回目は帯ごと別のコマで埋め、2回目はまわりから塗りのばしたので、スカートがゆがんだ／にじんだ。
  ・消すのは、文字の線（白い線と影）だけ（glyphmask: 文字のあるコマの中央値と、ないコマの中央値の「細い明るい線」の差）
  ・埋めるのは、文字のないコマの中から、文字のすぐ上と下の帯がいちばん合うコマを、少しずらして合わせたもの（スカートのひだがつながる）
  ・前のコマで選んだ埋め元の「次のコマ」が十分合っていれば、それを使い続ける（コマごとに埋め元が変わってちらつかないように）
  python3 remove_burned_text.py <元のコマ> <出力のコマ> <glyphmask.npy>"""
import sys, shutil, cv2, numpy as np
SRC, DST, MASK = sys.argv[1:4]
def load(k): return cv2.imread(f'{SRC}/{k+1:03d}.png').astype(np.float32)
y0, y1, x0, x1 = 615, 680, 455, 845
m = np.load(MASK).astype(np.uint8)
mm = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=3).astype(np.float32)
a = np.clip(cv2.GaussianBlur(mm, (0, 0), 2.5) * 1.5, 0, 1)[..., None]
clean = list(range(0, 13)) + list(range(113, 240)); CL = {c: load(c) for c in clean}
def err(A, c, dx, dy):
    C = CL[c]; Cs = C[y0 - 22 - dy:y1 + 22 - dy, x0 - dx:x1 - dx]
    ref = np.concatenate([A[y0 - 22:y0 - 2, x0:x1], A[y1 + 2:y1 + 22, x0:x1]])
    return ((np.concatenate([Cs[:20], Cs[-20:]]) - ref) ** 2).mean()
for k in range(240):
    if not (13 <= k <= 112): shutil.copy(f'{SRC}/{k+1:03d}.png', f'{DST}/{k+1:03d}.png')
prev = None; fade = []
for k in range(13, 113):
    A = load(k); best = None
    for c in clean:
        for dy in range(-6, 7, 2):
            for dx in (-4, 0, 4):
                e = err(A, c, dx, dy)
                if best is None or e < best[0]: best = (e, c, dx, dy)
    if prev is not None:
        c2 = prev[1] + 1
        if c2 in CL:
            e2 = min(((err(A, c2, dx, dy), c2, dx, dy) for dy in range(-6, 7, 2) for dx in (-4, 0, 4)))
            if e2[0] < best[0] * 3.0: best = e2
    switched = prev is not None and best[1] != prev[1] + 1
    oldc = (prev[1] + 1, prev[2], prev[3]) if switched and prev[1] + 1 in CL else None
    prev = best; e, c, dx, dy = best
    Cs = cv2.warpAffine(CL[c], np.float32([[1, 0, dx], [0, 1, dy]]), (1280, 720), borderMode=cv2.BORDER_REPLICATE)
    if oldc: fade = [(oldc, 0.75), (None, 0)]   # 埋め元が変わる所は、前の埋め元の続きと重ねて切りかえる
    if 'fade' in dir() and fade and fade[0][0]:
        (oc, odx, ody), w = fade[0][0], fade[0][1]
        Co = cv2.warpAffine(CL[oc], np.float32([[1, 0, odx], [0, 1, ody]]), (1280, 720), borderMode=cv2.BORDER_REPLICATE)
        Cs = Cs * (1 - w) + Co * w
        fade = [((oc + 1, odx, ody), w - 0.25)] if w - 0.25 > 0 and oc + 1 in CL else []
    S = A[y0:y1, x0:x1]; S[:] = S * (1 - a) + Cs[y0:y1, x0:x1] * a
    cv2.imwrite(f'{DST}/{k+1:03d}.png', A.astype(np.uint8))
print("ok")
# 仕上げ: 埋めた所だけ、前後のコマと 1:2:1 でならす（埋め元が変わる所のちらつきを消す。もとの動きはゆっくりなので、ならしても形は崩れない）
F = {k: cv2.imread(f'{DST}/{k+1:03d}.png').astype(np.float32) for k in range(11, 115)}
for _ in range(2):
    G = {}
    for k in range(13, 113):
        sm = 0.25 * F[k - 1] + 0.5 * F[k] + 0.25 * F[k + 1]
        G[k] = F[k].copy(); S = G[k][y0:y1, x0:x1]; S[:] = S * (1 - a) + sm[y0:y1, x0:x1] * a
    F.update(G)
for k in range(13, 113): cv2.imwrite(f'{DST}/{k+1:03d}.png', F[k].astype(np.uint8))
print("ならした")
