"""金色の光の帯・白い息が濃くかぶったマフラーの右上〜右の巻き髪の先を、かぶっていないコマの同じ所で置きかえる
（2026-11-11『白い息のリテイク』。人間「全部が自然になるように。変な違和感あるぼやけ方をしない用にして」）。
  光のつぶを 1 つずつ消す（clean_person_dots.py）・白をひく（dehaze_person.py）では、濃くかぶったコマ（1.9〜3.2秒、4.8〜5.8秒、
  7.5〜8.9秒あたり）に、にじみ・オレンジ色のしみ・ちぎれたかけらが残っていた。マフラーは体と一緒に動くだけなので、
  時間のいちばん近い「かぶっていないコマ」のマフラーを、位置を合わせて持ってくる（patch_curl.py と同じ考え方）。
    ・かぶり具合 = 元のコマ（消す前）の、その場所の金色の明るい点の数。少しずつ濃くなる・うすくなるのに合わせて、なめらかに切りかえる
    ・位置合わせ: マフラー全体の編み目を目じるしに、たて・よこのずれを測る
    ・顔（あご・口）には手を加えない
  python3 patch_scarf.py <コマのフォルダ> <人物の形 npy> <元のコマ（消す前）のフォルダ> <出力コマのフォルダ> <出力の形 npy>
"""
import sys, os, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_util as PU
SRC, PM, RAW, DST, PMOUT = sys.argv[1:6]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); K = len(P); H, W = P.shape[1:]
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
F = [cv2.imread(f"{SRC}/{k + 1:03d}.png") for k in range(K)]
m = np.zeros(K)
for k in range(K):
    f = cv2.imread(f"{RAW}/{k + 1:03d}.png"); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, EL(9)); b, gr, r = [f[..., i].astype(int) for i in range(3)]
    m[k] = ((th > 30) & (gr > 140) & (r > 170) & (gr - b > 15))[270:430, 600:810].sum()
d = np.clip((m - 70) / 50.0, 0, 1)
d = np.convolve(np.pad(d, 3, mode="edge"), np.ones(7) / 7, "valid")          # 切りかえを 7 コマかけてなめらかに
d = np.maximum(d, np.clip((m - 70) / 50.0, 0, 1))
clean = m < 62
win = np.zeros((H, W), np.float32); win[332:432, 598:812] = 1; win[268:332, 706:812] = 1; win[304:332, 686:812] = 1   # マフラーの右上・右肩・右の巻き髪の先（あご・口はふくまない）
win = cv2.GaussianBlur(win, (0, 0), 6)
TY0, TY1, TX0, TX1 = 340, 412, 558, 702                                      # 位置合わせの目じるし（マフラー）
out_P = P.copy(); n = 0; scs = []
for k in range(K):
    if d[k] < 0.03: cv2.imwrite(f"{DST}/{k + 1:03d}.png", F[k]); continue
    cand = np.where(clean)[0]; r = int(cand[np.argmin(np.abs(cand - k))])
    tpl = cv2.cvtColor(F[r][TY0:TY1, TX0:TX1], cv2.COLOR_BGR2GRAY); S = 16
    area = cv2.cvtColor(F[k][TY0 - S:TY1 + S, TX0 - S:TX1 + S], cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(area, tpl, cv2.TM_CCOEFF_NORMED); _, sc, _, loc = cv2.minMaxLoc(res)
    dx, dy = loc[0] - S, loc[1] - S; scs.append(sc)
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    rf = cv2.warpAffine(F[r], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    ra = cv2.warpAffine(P[r], M, (W, H), flags=cv2.INTER_LINEAR).astype(np.float32)
    sl = (slice(230, 470), slice(560, 850)); rfc, rac = PU.fit(F[k][sl], rf[sl].astype(np.uint8), ra[sl], sigma=6.0); rf[sl] = rfc; ra[sl] = rac          # 2026-11-11「肩とか…変だよ？」: 肩の線が二重にならないよう、細かい動きを測って曲げて合わせる
    z = win * float(d[k]); w = z[..., None]
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", np.clip(F[k] * (1 - w) + rf * w, 0, 255).astype(np.uint8))
    out_P[k] = np.clip(P[k] * (1 - z) + ra * z, 0, 255).astype(np.uint8); n += 1
np.save(PMOUT, out_P)
print("置きかえたコマ", n, "・位置合わせの合い具合 平均 %.2f 最小 %.2f" % (np.mean(scs), np.min(scs)))
