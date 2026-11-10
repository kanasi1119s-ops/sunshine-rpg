"""元の動画の「白い息の雲」が、巻き髪・マフラーの上にかぶって白くかすんでいる所を、もとの色にもどす
（2026-11-11『白い息のリテイク』。人間「全部が自然になるように。変な違和感あるぼやけ方をしない用にして」）。
  元の動画は、息をはくたびに大きな白い雲が顔の左に出る（1.5〜3秒、3.7〜4.7秒、6.2〜7.1秒あたり）。人物だけを切り抜くと、
  雲のうち髪・マフラーに重なった分だけが残り、巻き髪の先が白っぽくぼけて、形がくずれて見えていた。
  白い息は wb_layers.py で出し直しているので、人物に重なった分は取りのぞく。
    ・雲のある場所 = 人物の外で、背景の絵（人物も雪もない 1 枚）より白く明るい、大きなかたまり
    ・雲の近くの「赤いもの」（髪・マフラー）だけを直す。赤いものは、もともと緑・青がとても低いので、
      緑・青がどれだけ持ち上がっているかで、かぶっている雲の濃さが分かる → その分の白を引く
    ・肌・目・服・手袋には手を加えない
  python3 dehaze_person.py <コマのフォルダ> <人物の形 npy> <背景 png> <出力フォルダ>
"""
import sys, os, cv2, numpy as np
SRC, PM, PLATE, DST = sys.argv[1:5]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); plate = cv2.imread(PLATE).astype(np.float32); pmin = plate.min(2)
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
WHITE = np.array([228, 226, 224], np.float32)          # 雲の色（BGR）
B0 = 42.0                                              # 赤い髪・マフラーの、もとの緑・青の低いほうの目安
n_fix = 0
for k in range(len(P)):
    f = cv2.imread(f"{SRC}/{k + 1:03d}.png").astype(np.float32)
    out_p = P[k] < 40
    cloud = np.clip((f.min(2) - pmin - 22) / 110.0, 0, 1) * out_p
    cloud = cv2.morphologyEx(cloud, cv2.MORPH_OPEN, EL(11))            # 雪・光のつぶ（小さい点）は雲ではない
    if cloud.sum() < 300: cv2.imwrite(f"{DST}/{k + 1:03d}.png", f.astype(np.uint8)); continue
    zone = cv2.GaussianBlur(cv2.dilate(cloud, EL(61)), (0, 0), 14)    # 雲のまわり 30px ほどまで
    zone = np.clip(zone * 1.6, 0, 1)
    b, g, r = f[..., 0], f[..., 1], f[..., 2]; lo = np.minimum(b, g)
    reddish = (r - lo > 28) & (r > 90) & (P[k] > 30)                   # 赤いもの（かすんでピンクになった所もふくむ）
    skin = (g > 150) & (r > 215) & (r - g < 75) & (b > 120) & (cv2.medianBlur(f.astype(np.uint8), 9)[..., 1] > 150)   # 肌（広い明るい面）は除く
    m = np.clip((lo - B0) / (WHITE[:2].mean() - B0), 0, 0.88) * zone * (reddish & ~skin)
    m = cv2.GaussianBlur(m, (0, 0), 1.0)[..., None]
    fixed = (f - m * WHITE) / np.maximum(1 - m, 0.12)
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", np.clip(fixed, 0, 255).astype(np.uint8)); n_fix += 1
print("直したコマ", n_fix, "→", DST)
