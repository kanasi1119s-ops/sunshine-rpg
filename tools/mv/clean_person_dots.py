"""人物（マフラー・服・手袋）の上に重なった、金色の光のつぶと雪のつぶを消す
（2026-11-11『白い息のリテイク』。人間「動画色々細かく調整してスムーズにして…他のエフェクトも」）。
  remove_sparkle.py は人物の外だけを直したので、光の帯がマフラーの前を通るコマでは、つぶがマフラーの上に残っていた。
  また、元の動画の雪は人物の上にも焼きこまれていて、口を合わせるために人物の速さを変えると、その雪だけ一緒に速くなる。
  雪は wb_layers.py で降らせ直すので、人物の上の小さな明るい点は消しておく。
    ・あごより下（マフラー・服・手袋）だけ。顔・目・髪・白いリボンには手を加えない
    ・肌（腕と「04」の字）と、そのすぐそばは守る
    ・消すのは「まわりより明るい小さな点」（白〜黄色）だけ。まわりの色でうめる
  python3 clean_person_dots.py <コマのフォルダ> <人物の形 npy> <出力フォルダ>
"""
import sys, os, cv2, numpy as np
SRC, PM, DST = sys.argv[1:4]; os.makedirs(DST, exist_ok=True)
P = np.load(PM); EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
tot = 0
for k in range(len(P)):
    f = cv2.imread(f"{SRC}/{k + 1:03d}.png"); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    b, gr, r = [f[..., i].astype(np.int16) for i in range(3)]
    th = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, EL(11))
    med = cv2.medianBlur(f, 21)                                   # まわりの色。肌（明るい）の所と、そのそばは守る
    skin = cv2.dilate(((med[..., 1] > 120) & (P[k] > 100)).astype(np.uint8), EL(7))
    m = (th > 32) & (gr > 135) & (r > 150) & (P[k] > 100) & (skin == 0)
    m[:250] = False; m[250:322, 540:735] = False                  # 顔（真ん中）は守る。横の巻き髪の上のつぶは消す
    # 金色（黄色っぽい）の明るい点は、肌のそば（あごの下のマフラーなど）でも消す。肌そのものは黄色みが弱いので当たらない
    gold = (cv2.morphologyEx(g, cv2.MORPH_TOPHAT, EL(9)) > 38) & (gr > 150) & (r > 170) & (gr - b > 25) & (P[k] > 100)
    gold[:300] = False; gold[430:] = False; gold[:, :520] = False; gold[:, 735:] = False   # あごの下のマフラーだけ（腕の「04」は守る）
    m = m | gold
    m = cv2.dilate(m.astype(np.uint8), EL(7)); tot += int(m.sum())
    cv2.imwrite(f"{DST}/{k + 1:03d}.png", cv2.inpaint(f, m * 255, 4, cv2.INPAINT_TELEA) if m.any() else f)
print("消した点の広さ（1コマ平均 px）", tot // len(P), "→", DST)
