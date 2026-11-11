"""ほかのコマから持ってきた絵（巻き髪・マフラー）を、いまのコマの形にぴったり合わせる（2026-11-11『白い息のリテイク』。
人間「肩とか髪の毛とか変だよ？」）。
  patch_curl.py・patch_scarf.py は、持ってきた絵を「たて・よこにずらすだけ」で重ねていた。巻き髪の先や肩は、頭やマフラーと
  少しちがう動きをするので、切りかえの途中で元の絵と持ってきた絵がずれて、先が 2 本に見えたり、肩の線が二重になったりしていた。
  ここでは、いまのコマと持ってきた絵のあいだの細かい動き（ピクセルごとのずれ）を測り、持ってきた絵のほうを曲げて合わせる。
  雲で見えない所はずれを測れないので、見えている所のずれを、なめらかに広げて使う（conf: 見えている度合い 0〜1）。
"""
import cv2, numpy as np
_dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
_dis.setFinestScale(0); _dis.setPatchSize(12); _dis.setPatchStride(3); _dis.setGradientDescentIterations(40)
def fit(cur, ref, ref_alpha, conf=None, sigma=10.0):
    """cur（いまのコマ BGR uint8）に合うよう ref（持ってきた絵 BGR）と ref_alpha（その形）を曲げて返す（float32）"""
    gc = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY); gr = cv2.cvtColor(np.clip(ref, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    fl = _dis.calc(gc, gr, None)
    c = np.ones(gc.shape, np.float32) if conf is None else np.clip(conf, 0.02, 1).astype(np.float32)
    den = cv2.GaussianBlur(c, (0, 0), sigma)
    fl = np.dstack([cv2.GaussianBlur(fl[..., i] * c, (0, 0), sigma) / den for i in range(2)])
    fl = np.clip(fl, -10, 10)                          # 大きくはずれた測りまちがいは使わない
    h, w = gc.shape; gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    mx, my = gx + fl[..., 0], gy + fl[..., 1]
    return (cv2.remap(ref.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE),
            cv2.remap(ref_alpha.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE))
