"""『白い息のリテイク』作り直し（2026-11-11）: コマごとの「テトと白い息のある場所」の形を作る。
  新しい作り方（mv_compose.py の frames_wb2）は、人物を切り抜かない。画面のほとんどは元の動画をふつうの速さで流し、
  テトと白い息のまわりだけを、口を歌詞に合わせたコマに入れかえる。その「入れかえる場所」がこの形。
  ふちは人物の輪郭から 20px ほど外の、動かない背景の上に来るので、切り抜きのまちがいが絵に出ない。
    形 = 人物（切り抜き AI の形を 20px 広げる）＋ 白い息（背景の 1 枚より ぼんやり明るく、前後のコマでも続いている所）
  python3 wb2_region.py <コマのフォルダ> <人物の形 npy> <背景 png> <出力 npy（半分の大きさ・0/255）>
"""
import sys, cv2, numpy as np
SRC, PM, PLATE, OUT = sys.argv[1:5]
P = np.load(PM); K = len(P); pg = cv2.cvtColor(cv2.imread(PLATE), cv2.COLOR_BGR2GRAY).astype(np.float32)
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
ex = []
for k in range(K):
    g = cv2.cvtColor(cv2.imread(f"{SRC}/{k + 1:03d}.png"), cv2.COLOR_BGR2GRAY).astype(np.float32)
    ex.append(cv2.GaussianBlur(g - pg, (0, 0), 5))
ex = np.stack(ex); R = np.zeros((K, 360, 640), np.uint8); nb = []
for k in range(K):
    e = ex[max(0, k - 2):k + 3].min(0)                           # 雪は 1〜2 コマで通りすぎるので、前後でも明るい所だけ
    b = (e > 6).astype(np.uint8); b[:140] = 0; b[430:] = 0; b[:, :380] = 0; b[:, 900:] = 0
    b[cv2.dilate(P[k], EL(5)) > 100] = 0
    # 人物にくっついているかたまりだけ（はなれた明かりのゆらぎは入れない）
    per = (cv2.dilate(P[k], EL(41)) > 100).astype(np.uint8)
    n, lab = cv2.connectedComponents(np.maximum(b, per))
    keep = lab == lab[360, 640]
    br = cv2.dilate((keep & (b > 0)).astype(np.uint8), EL(31))
    m = np.maximum(per, br)
    R[k] = cv2.resize(m * 255, (640, 360), interpolation=cv2.INTER_AREA); nb.append(int(br.sum()))
np.save(OUT, R); print("白い息の広さ（10コマごと）", nb[::10])
