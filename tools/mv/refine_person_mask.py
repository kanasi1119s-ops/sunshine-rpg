"""人物の切り抜きの形から、まわりにくっついた白いもや（元の動画の白い息のかけら）を外す
（2026-11-11『白い息のリテイク』。人間「テト周辺の背景がボロボロだね」）。
  切り抜きの AI は、髪や肩のすぐ外にただよう白い息まで「人物」に入れることがあり、そのかけらがコマごとに形を変えて、
  人物のまわりがちぎれたように見えた。白い息は wb_layers.py で出し直すので、元のもやは外す。
    ・もや = 色がうすく（彩度が低い）、明るさが中くらいの所。髪・マフラー（赤）、肌、白いリボン、暗い手袋はちがう
    ・人物の「しん」（もやを除いた形）のうち、いちばん大きいひとかたまりだけを残し、中の穴はうめる
      → 髪に重なったもやは残る（穴をあけない）。外へはみ出したかけらだけが消える
    ・ふちは少しだけやわらかくする
  python3 refine_person_mask.py <コマのフォルダ> <人物の形 npy> <出力 npy>
"""
import sys, cv2, numpy as np
SRC, PM, OUT = sys.argv[1:4]
P = np.load(PM); EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n)); out = P.copy(); cut = 0
for k in range(len(P)):
    f = cv2.imread(f"{SRC}/{k + 1:03d}.png"); h = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    # 顔の横（巻き髪のあたり）にある人物は「赤い髪」と白いリボンだけ。赤くない所（白いもや）は人物から外す。
    #   髪に重なったもやはピンク色（赤みが残る）なので残り、髪の外へはみ出したもやだけが消える
    b_, g_, r_ = [f[..., i].astype(np.int16) for i in range(3)]
    red = (r_ - np.maximum(g_, b_) > 18)
    side = np.zeros(P[k].shape, bool); side[120:380, :565] = True; side[120:380, 715:] = True
    side[300:380, 565:605] = True; side[300:380, 680:715] = True   # ほおの下〜マフラーの横（目より下。肌・マフラーは赤みがあるので残る）
    side[:260, 670:800] = False                                # 白いリボンは守る
    core = ((P[k] > 128) & (red | ~side)).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_OPEN, EL(3))
    n, lab, st, _ = cv2.connectedComponentsWithStats(core, 8)
    if n > 1: core = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, EL(5))
    ff = core.copy(); m2 = np.zeros((ff.shape[0] + 2, ff.shape[1] + 2), np.uint8); cv2.floodFill(ff, m2, (0, 0), 2)
    core = (ff != 2).astype(np.uint8)                        # 外とつながっていない所（中の穴）はうめる
    keep = cv2.GaussianBlur(cv2.dilate(core, EL(3)).astype(np.float32), (0, 0), 1.0)
    a = P[k].astype(np.float32) * keep
    cut += int((P[k] > 128).sum() - (a > 128).sum()); out[k] = np.clip(a, 0, 255).astype(np.uint8)
np.save(OUT, out); print("外した広さ（1コマ平均 px）", cut // len(P), "→", OUT)
