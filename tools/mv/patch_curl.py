"""白い息の雲にかくれた左の巻き髪の先を、雲のないコマの同じ巻き髪で置きかえる
（2026-11-11『白い息のリテイク』。人間「全部が自然になるように。変な違和感あるぼやけ方をしない用にして」）。
  dehaze_person.py は、うすくかすんだ所の色はもどせるが、濃い雲の下の巻き髪は色が残っていないので もどせない。
  巻き髪は頭と一緒に動くだけで形は変わらないので、時間のいちばん近い「雲のないコマ」から同じ巻き髪を持ってくる:
    ・位置合わせ: 巻き髪の上半分（雲がかからない）を目じるしに、たて・よこのずれを測る
    ・置きかえるのは、雲がかかっている所（雲の濃さに合わせて、なめらかに切りかえる）だけ。形（切り抜き）も一緒に置きかえる
  python3 patch_curl.py <コマのフォルダ> <人物の形 npy（もやを外したもの）> <背景 png> <出力コマのフォルダ> <出力の形 npy>
"""
import sys, os, cv2, numpy as np
SRC, PM, PLATE, DST, PMOUT = sys.argv[1:6]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); K = len(P); plate = cv2.imread(PLATE).astype(np.float32); pmin = plate.min(2)
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
F = [cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in range(K)]
Y0, Y1, X0, X1 = 250, 392, 425, 568                    # 置きかえる範囲（左の巻き髪の下半分）
TY0, TY1, TX0, TX1 = 150, 292, 445, 575                # 位置合わせの目じるし（巻き髪の上半分）
H, W = P.shape[1:]
win = np.zeros((H, W), np.float32); win[Y0:Y1, X0:X1] = 1; win = cv2.GaussianBlur(win, (0, 0), 7)
zones = []; amount = np.zeros(K)
for k in range(K):
    f = F[k].astype(np.float32)
    cloud = np.clip((f.min(2) - pmin - 22) / 110.0, 0, 1) * (P[k] < 40)
    cloud = cv2.morphologyEx(cloud, cv2.MORPH_OPEN, EL(11))
    z = np.clip(cv2.GaussianBlur(cv2.dilate(cloud, EL(45)), (0, 0), 10) * 1.8, 0, 1) * win
    zones.append(z); amount[k] = float(cloud[Y0 - 20:Y1 + 30, X0 - 30:X1 + 20].sum())
clean = amount < 40
print("雲のないコマ", int(clean.sum()), "/", K)
out_P = P.copy(); n = 0; shifts = []
for k in range(K):
    z = zones[k]
    if clean[k] or z.max() < 0.15: cv2.imwrite(f"{DST}/{k + 1:03d}.png", F[k]); continue
    cand = np.where(clean)[0]; r = int(cand[np.argmin(np.abs(cand - k))])
    tpl = cv2.cvtColor(F[r][TY0:TY1, TX0:TX1], cv2.COLOR_BGR2GRAY); S = 16
    area = cv2.cvtColor(F[k][TY0 - S:TY1 + S, TX0 - S:TX1 + S], cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(area, tpl, cv2.TM_CCOEFF_NORMED); _, sc, _, loc = cv2.minMaxLoc(res)
    dx, dy = loc[0] - S, loc[1] - S; shifts.append((k, r, dx, dy, round(sc, 2)))
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    rf = cv2.warpAffine(F[r], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    ra = cv2.warpAffine(P[r], M, (W, H), flags=cv2.INTER_LINEAR).astype(np.float32)
    w = z[..., None]
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", np.clip(F[k] * (1 - w) + rf * w, 0, 255).astype(np.uint8))
    out_P[k] = np.clip(P[k] * (1 - z) + ra * z, 0, 255).astype(np.uint8); n += 1
np.save(PMOUT, out_P)
sc = [s[4] for s in shifts]
print("置きかえたコマ", n, "・位置合わせの合い具合 平均 %.2f 最小 %.2f・ずれ 最大 %d px" % (np.mean(sc), np.min(sc), max(max(abs(s[2]), abs(s[3])) for s in shifts)))
