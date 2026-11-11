"""白い息の雲にかくれた左の巻き髪の先を、雲のないコマの同じ巻き髪で置きかえる
（2026-11-11『白い息のリテイク』。人間「全部が自然になるように。変な違和感あるぼやけ方をしない用にして」）。
  dehaze_person.py は、うすくかすんだ所の色はもどせるが、濃い雲の下の巻き髪は色が残っていないので もどせない。
  巻き髪は頭と一緒に動くだけで形は変わらないので、時間のいちばん近い「雲のないコマ」から同じ巻き髪を持ってくる:
    ・位置合わせ: 巻き髪の上半分（雲がかからない）を目じるしに、たて・よこのずれを測る
    ・置きかえるのは、雲がかかっている所（雲の濃さに合わせて、なめらかに切りかえる）だけ。形（切り抜き）も一緒に置きかえる
  python3 patch_curl.py <コマのフォルダ> <人物の形 npy（もやを外したもの）> <背景 png> <出力コマのフォルダ> <出力の形 npy>
"""
import sys, os, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_util as PU
SRC, PM, PLATE, DST, PMOUT = sys.argv[1:6]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); K = len(P); plate = cv2.imread(PLATE).astype(np.float32); pmin = plate.min(2)
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
F = [cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in range(K)]
Y0, Y1, X0, X1 = 250, 392, 425, 568                    # 置きかえる範囲（左の巻き髪の下半分）
TY0, TY1, TX0, TX1 = 150, 292, 445, 575                # 位置合わせの目じるし（巻き髪の上半分）
H, W = P.shape[1:]
win = np.zeros((H, W), np.float32); win[Y0:Y1, X0:X1] = 1; win = cv2.GaussianBlur(win, (0, 0), 7)
zones = []; clouds = []; amount = np.zeros(K)
for k in range(K):
    f = F[k].astype(np.float32)
    cloud = np.clip((f.min(2) - pmin - 22) / 110.0, 0, 1) * (P[k] < 40)
    cloud = cv2.morphologyEx(cloud, cv2.MORPH_OPEN, EL(11))
    z = np.clip(cv2.GaussianBlur(cv2.dilate(cloud, EL(45)), (0, 0), 10) * 1.8, 0, 1) * win
    zones.append(z); clouds.append(cloud); amount[k] = float(cloud[Y0 - 20:Y1 + 30, X0 - 30:X1 + 20].sum())
clean = amount < 40
print("雲のないコマ", int(clean.sum()), "/", K)
# 2026-11-11「肩とか髪の毛とか変だよ？」: 雲の形に合わせて半分だけ切りかえていたので、巻き髪の下半分が すけて見えたり、
#   元の先と持ってきた先が 2 本に見えたりしていた。雲が少しでもかかるコマは、下半分をまるごと持ってきた絵にする
#   （切りかえは時間の方向にだけ、なめらかに）。持ってきた絵は、細かい動きを測って いまのコマの形に曲げて合わせる
tw = np.clip((amount - 15) / 40.0, 0, 1)
tw = np.maximum(tw, np.convolve(np.pad(tw, 3, mode="edge"), np.ones(7) / 7, "valid"))
out_P = P.copy(); n = 0; shifts = []
for k in range(K):
    if tw[k] < 0.03: cv2.imwrite(f"{DST}/{k + 1:03d}.png", F[k]); continue
    cand = np.where(clean)[0]; r = int(cand[np.argmin(np.abs(cand - k))])
    tpl = cv2.cvtColor(F[r][TY0:TY1, TX0:TX1], cv2.COLOR_BGR2GRAY); S = 16
    area = cv2.cvtColor(F[k][TY0 - S:TY1 + S, TX0 - S:TX1 + S], cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(area, tpl, cv2.TM_CCOEFF_NORMED); _, sc, _, loc = cv2.minMaxLoc(res)
    dx, dy = loc[0] - S, loc[1] - S; shifts.append((k, r, dx, dy, round(sc, 2)))
    M = np.float32([[1, 0, dx], [0, 1, dy]]); sl = (slice(Y0 - 110, Y1 + 40), slice(X0 - 40, X1 + 40))
    rf = cv2.warpAffine(F[r], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    ra = cv2.warpAffine(P[r], M, (W, H), flags=cv2.INTER_LINEAR)
    conf = 1 - np.clip(cv2.GaussianBlur(cv2.dilate(clouds[k], EL(15)), (0, 0), 4) * 2.5, 0, 1)
    rfc, rac = PU.fit(F[k][sl], rf[sl], ra[sl], conf=conf[sl])
    z = (win * tw[k])[sl]; a = rac / 255.0 * z; pk = P[k][sl].astype(np.float32) / 255.0
    A = a + pk * (1 - a)                               # 持ってきた巻き髪を、いまのコマの上に重ねる（形ごと）
    col = (rfc * a[..., None] + F[k][sl].astype(np.float32) * (pk * (1 - a))[..., None]) / np.maximum(A, 1e-3)[..., None]
    col = np.where(A[..., None] > 0.004, col, rfc * z[..., None] + F[k][sl] * (1 - z[..., None]))   # 人物の外（背景）もふつうに切りかえる
    o = F[k].copy(); o[sl] = np.clip(col, 0, 255).astype(np.uint8)
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", o)
    out_P[k][sl] = np.clip(A * 255, 0, 255).astype(np.uint8); n += 1
np.save(PMOUT, out_P)
sc = [s[4] for s in shifts]
print("置きかえたコマ", n, "・位置合わせの合い具合 平均 %.2f 最小 %.2f・ずれ 最大 %d px" % (np.mean(sc), np.min(sc), max(max(abs(s[2]), abs(s[3])) for s in shifts)))
