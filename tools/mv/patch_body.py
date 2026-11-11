"""金色の光のつぶが体（左の肩・うで・胸など）にかぶったコマを、かぶっていないコマの同じ所で置きかえる
（2026-11-11『白い息のリテイク』。人間「肩とか髪の毛とか変だよ？」）。
  patch_scarf.py はマフラーの右上だけを見ていた。光の帯は体の前も通るので、左の肩や胸に、つぶを消したあとの
  にじみ・オレンジ色のしみ・白っぽいむらが残り、肩がすけたように見えるコマがあった。
    ・かぶっている所 = 元のコマ（消す前）で、人物の上にある金色の明るい点のまわり
    ・その場所がきれいな、時間のいちばん近いコマを持ってきて、細かい動きを測って いまのコマの形に曲げて合わせる（patch_util.py）
    ・顔（口・目は歌に合わせて動く）と、ほかの道具で直した所（マフラーの右上・左の巻き髪の先）にはさわらない
  python3 patch_body.py <コマのフォルダ> <人物の形 npy> <元のコマ（消す前）のフォルダ> <出力コマのフォルダ> <出力の形 npy>
"""
import sys, os, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_util as PU
SRC, PM, RAW, DST, PMOUT = sys.argv[1:6]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); K = len(P); H, W = P.shape[1:]
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
F = [cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in range(K)]
skip = np.zeros((H, W), bool); skip[190:338, 530:740] = True          # 顔
skip[332:432, 598:812] = True; skip[268:332, 686:812] = True           # マフラーの右上（patch_scarf.py）
skip[140:392, 425:568] = True                                          # 左の巻き髪（patch_curl.py）
dots = []
for k in range(K):
    f = cv2.imread(f"{RAW}/{k + 1:03d}.png"); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, EL(15)); b, gr, r = [f[..., i].astype(int) for i in range(3)]
    d = (th > 25) & (r > 150) & (gr - b > 25) & (cv2.dilate(P[k], EL(41)) > 128) & ~skip   # 人物の近くの背景のつぶも数える（肌の上の大きくぼけた光は、点としては見つけにくい）
    dots.append(cv2.morphologyEx(d.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)))
dots = np.stack(dots); cnt = dots.reshape(K, -1).sum(1)
out_P = P.copy(); n = 0; far = []
for k in range(K):
    near = dots[max(0, k - 2):k + 3].max(0)                             # 前後のコマのぶんも（にじみは つぶより少し長く残る）
    if near.sum() < 6: cv2.imwrite(f"{DST}/{k + 1:03d}.png", F[k]); continue
    zb = cv2.dilate(near, EL(45)); z = cv2.GaussianBlur(zb.astype(np.float32), (0, 0), 6) * (~skip)
    z = cv2.GaussianBlur(z, (0, 0), 2)
    inz = (dots * zb[None]).reshape(K, -1).sum(1)                       # その場所に つぶがあるコマは持ってこない
    wide = np.array([inz[max(0, j - 2):j + 3].max() for j in range(K)])
    cand = np.where(wide <= 2)[0]
    if len(cand) == 0: cv2.imwrite(f"{DST}/{k + 1:03d}.png", F[k]); continue
    r = int(cand[np.argmin(np.abs(cand - k))]); far.append(abs(r - k))
    ys, xs = np.where(zb > 0); sl = (slice(max(0, ys.min() - 50), min(H, ys.max() + 50)), slice(max(0, xs.min() - 50), min(W, xs.max() + 50)))
    rfc, rac = PU.fit(F[k][sl], F[r][sl], P[r][sl], conf=1 - cv2.GaussianBlur(zb.astype(np.float32), (0, 0), 3)[sl], sigma=8.0)
    w = z[sl][..., None]; o = F[k].copy()
    o[sl] = np.clip(F[k][sl] * (1 - w) + rfc * w, 0, 255).astype(np.uint8)
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", o)
    out_P[k][sl] = np.clip(P[k][sl] * (1 - z[sl]) + rac * z[sl], 0, 255).astype(np.uint8); n += 1
# 体の内側で、切り抜きに穴があいている・半分すけている所（灰色の服の胸を、切り抜きの AI が背景とまちがえていた。
#   そこから背景の窓の明かりがすけて、肩のあたりが変に見えていた）をうめる。
#   まわりを人物にかこまれた穴のうち、色が背景の絵とちがうもの（＝服）だけ。巻き髪と顔のあいだのすき間（色が背景と同じ）は残す
plate = cv2.imread(sys.argv[6]).astype(np.float32) if len(sys.argv) > 6 else None; filled = 0
for k in range(K):
    if plate is not None:
        img = cv2.imread(f"{DST}/{k + 1:03d}.png").astype(np.float32); diff = np.abs(img - plate).max(2)
        nb, lab, st, _ = cv2.connectedComponentsWithStats((out_P[k] < 200).astype(np.uint8), connectivity=8)
        for i in range(1, nb):
            x, y, w, h, ar = st[i]
            if x == 0 or y == 0 or x + w >= W or y + h >= H or ar < 6: continue
            if np.median(diff[lab == i]) > 22:
                out_P[k][cv2.dilate((lab == i).astype(np.uint8), EL(9)) > 0] = 255; filled += 1
    inner = cv2.erode((out_P[k] > 40).astype(np.uint8), EL(15)) > 0
    out_P[k][inner] = 255
print("うめた穴", filled)
np.save(PMOUT, out_P)
print("置きかえたコマ", n, "・持ってきたコマまでの はなれ 平均 %.1f 最大 %d コマ" % (np.mean(far or [0]), np.max(far or [0])))
