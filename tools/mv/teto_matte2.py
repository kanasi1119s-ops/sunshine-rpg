#!/usr/bin/env python3
"""テトの動画のコマを、白い背景から「なめらかな縁」で切り抜く（第2版。2026-10-29 人間「細かいところのトリミングができていない、なめらかにならない」）。

第1版（teto_matte.py）の問題:
  ・背景か体かを 0/1 で決めてから少しぼかしていたので、縁がギザギザ（階段）になる
  ・縁の色を内側の色でぬりつぶしていたので、絵の黒い線（輪郭線）が縁で消える。白いにじみも少し残る

第2版のしくみ（背景が真っ白とわかっている＝「既知の背景」の切り抜き）:
  1. 背景・体・リボン・白目の判定は第1版と同じ（どこが背景かの大まかな地図）
  2. その地図から、確かな体（内側）・確かな背景・あいまいな帯（縁の数ピクセル）を作る
  3. あいまいな帯の各ピクセルは「体の色 F と白 W を α の割合で混ぜた色」C = αF + (1−α)W と考える。
     体の色 F は内側から外へ広げて推定し、α = Σ(W−C) / Σ(W−F) で求める（輪郭線の黒は α≈1、白いにじみは α≈0 になる）
  4. 色は白を取り除いた本当の色に戻す（F = (C − (1−α)W) / α）→ 白いにじみが残らない
  5. 縮めるときは「α をかけた色」で縮めてから戻す（縁が黒ずんだり白くなったりしない）
使い方: python3 teto_matte2.py <コマのフォルダ> <出力フォルダ> <縮める倍率> [コマ番号...]
"""
import sys, os, json, cv2, numpy as np
SRC, OUT, SC = sys.argv[1], sys.argv[2], float(sys.argv[3]); os.makedirs(OUT, exist_ok=True)
ks = [int(a) for a in sys.argv[4:]] or range(240)
TR = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "track_teto_a.json")))
WHITE = 250.0


def rough_bg(im, k):
    """第1版と同じ考え方の、背景の大まかな地図（1＝背景）"""
    h, w = im.shape[:2]
    mn = im.min(2).astype(np.int16); sat = (im.max(2).astype(np.int16) - mn)
    white = ((mn > 232) & (sat < 14)).astype(np.uint8)
    # リボンの細い輪郭線にすきまがあると、外の背景がリボンの中まで流れこむ → リボンの枠の中だけ、線を1〜2ピクセル太らせて壁にする
    mx0, my0 = 342 + TR[k][1], 291 + TR[k][2]
    rbox = np.zeros((h, w), np.uint8); rbox[max(0, my0 - 260):my0 - 60, mx0 + 55:mx0 + 195] = 1
    wall = cv2.dilate(((mn < 205) & (rbox > 0)).astype(np.uint8), np.ones((5, 5), np.uint8))
    white = white * (1 - wall)
    ff = white.copy(); mask = np.zeros((h + 2, w + 2), np.uint8)
    for (x, y) in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]:
        if ff[y, x] == 1: cv2.floodFill(ff, mask, (x, y), 2)
    bg = (ff == 2).astype(np.uint8)
    mx, my = 342 + TR[k][1], 291 + TR[k][2]
    keep = np.zeros((h, w), np.uint8)                       # リボンと白目は残す
    keep[max(0, my - 260):my - 60, mx + 55:mx + 195] = 1
    keep[max(0, my - 100):my - 25, max(0, mx - 88):mx + 88] = 1
    keep[max(0, my - 22):my + 30, max(0, mx - 45):mx + 45] = 1          # 口（歯）も残す
    ribbon = np.zeros((h, w), np.uint8); ribbon[max(0, my - 260):my - 60, mx + 55:mx + 195] = 1
    whitish = ((mn > 200) & (sat < 30)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(whitish * (1 - bg))
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    hair = (((hsv[..., 0] < 12) | (hsv[..., 0] > 165)) & (hsv[..., 1] > 90) & (hsv[..., 2] > 50)).astype(np.uint8)
    for i in range(1, n):
        x, y, w_, h_, area = st[i]
        sl = (slice(max(0, y - 6), y + h_ + 6), slice(max(0, x - 6), x + w_ + 6))
        comp = lab[sl] == i
        if keep[sl][comp].mean() > 0.3: continue
        if area > 900: bg[lab == i] = 1; continue
        m = comp.astype(np.uint8)
        ring = cv2.dilate(m, np.ones((7, 7), np.uint8)) - m
        hr = hair[sl][ring > 0]
        if len(hr) and hr.mean() > 0.3: bg[lab == i] = 1
    # 2026-10-29 人間「白いところリボン以外に残ってる」: 腕と体のすきま・指のあいだ・リボンのまわりの、閉じこめられた白も背景にする
    #   ・真っ白で色のない小さなかたまりは、まわりが肌でなければ背景（爪や肌の光は、まわりが肌なので残る）
    #   ・リボンの枠の中は、いちばん大きい白（リボン本体）とそれに近い大きさのものだけを残し、小さな白のかけらは背景
    skin = (((hsv[..., 0] < 25) | (hsv[..., 0] > 170)) & (hsv[..., 1] > 25) & (hsv[..., 1] < 140) & (hsv[..., 2] > 150)).astype(np.uint8)
    redish = (((hsv[..., 0] < 14) | (hsv[..., 0] > 160)) & (hsv[..., 1] > 60)).astype(np.uint8)   # 髪の赤（暗い赤の線もふくむ）
    pure = ((mn > 215) & (sat < 26)).astype(np.uint8) * (1 - bg)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(pure)
    rib_sizes = [st2[i, 4] for i in range(1, n2) if ribbon[lab2 == i].mean() > 0.5] if n2 > 1 else []
    rib_max = max(rib_sizes) if rib_sizes else 0
    for i in range(1, n2):
        x, y, w_, h_, area = st2[i]
        sl = (slice(max(0, y - 4), y + h_ + 4), slice(max(0, x - 4), x + w_ + 4))
        comp = (lab2[sl] == i)
        in_rib = ribbon[sl][comp].mean() > 0.5
        if in_rib:
            m = comp.astype(np.uint8); ring = cv2.dilate(m, np.ones((5, 5), np.uint8)) - m
            hr = redish[sl][ring > 0]
            if area >= 0.35 * rib_max or not (len(hr) and hr.mean() > 0.5): continue   # リボン本体と、リボンの中の白
            bg[lab2 == i] = 1; continue                                   # 髪にかこまれた白＝髪とリボンのすきまの背景
        if keep[sl][comp].mean() > 0.5: continue                          # 白目・歯
        m = comp.astype(np.uint8); ring = cv2.dilate(m, np.ones((5, 5), np.uint8)) - m
        sk = skin[sl][ring > 0]
        if len(sk) and sk.mean() > 0.5 and area < 60: continue            # 肌の光（爪など）
        bg[lab2 == i] = 1
    # リボンの枠の中で、髪の縁にそって細く残った白（壁のせいで背景にならなかった白い線）は背景にする。
    # リボン本体は太いので、細い所（幅4ピクセルくらいまで）だけを取りのぞく（2026-10-29 人間「髪の毛の周りに白いの残ってる」）
    kw = (((mn > 200) & (sat < 30)) & (ribbon > 0) & (bg == 0)).astype(np.uint8)
    body = cv2.morphologyEx(kw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    for _ in range(3): body = cv2.dilate(body, np.ones((3, 3), np.uint8)) * kw     # 本体の縁をもとにもどす
    hull = np.zeros_like(body)
    cs, _ = cv2.findContours(body, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cs:
        if cv2.contourArea(cnt) > 30: cv2.fillPoly(hull, [cv2.convexHull(cnt)], 1)   # リボンの形の内側（模様の線のすきまの白は残す）
    bg[(kw > 0) & (body == 0) & (hull == 0)] = 1
    hull = cv2.erode(hull, np.ones((3, 3), np.uint8))
    inside = (hull > 0) & (mn > 150)
    bg[inside] = 0                                                         # リボンの形の内側は、背景にしない（穴をあけない）
    body = np.maximum(body, inside.astype(np.uint8))
    # 背景になった白のとなりの、白に近いにじみも背景へ（リボン本体のまわりはのぞく）
    pale2 = ((mn > 205) & (sat < 30)).astype(np.uint8) * (1 - (keep * (1 - ribbon)))
    pale2[body > 0] = 0
    for _ in range(2):
        bg = np.maximum(bg, pale2 * cv2.dilate(bg, np.ones((3, 3), np.uint8)))
    # リボンの影は少し青むらさき（背景の白は色がない）→ リボンの枠の中の青むらさきの明るい所は、背景にしない
    b_, g_, r_ = [im[..., j].astype(np.int16) for j in range(3)]
    lav = (ribbon > 0) & (b_ - g_ > 7) & (r_ - g_ > 7) & (mn > 120) & (sat < 60) & (redish == 0)   # むらさき＝緑がいちばん少ない
    lav = cv2.morphologyEx(lav.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)) > 0
    bg[lav] = 0; body = np.maximum(body, lav.astype(np.uint8))
    # ---- 最後の仕上げ（2026-10-29 人間「詰めが甘い。徹底して、リボン以外の白いところを取り除いて」）----
    # 色のない白（背景の白）は、リボン本体・白目・歯のほかは、どこにあっても背景にする。
    #   白目と歯は、目と口の枠の中にあり、まわり（輪）が髪の赤でないもの。肌の光は少し色があるので残る
    neutral = ((mn > 218) & (sat < 13)).astype(np.uint8)
    face = np.zeros((h, w), np.uint8)
    face[max(0, my - 100):my - 25, max(0, mx - 88):mx + 88] = 1
    face[max(0, my - 22):my + 30, max(0, mx - 45):mx + 45] = 1
    n3, lab3, st3, _ = cv2.connectedComponentsWithStats(neutral * (1 - body))
    for i in range(1, n3):
        x, y, w_, h_, area = st3[i]
        sl = (slice(max(0, y - 4), y + h_ + 4), slice(max(0, x - 4), x + w_ + 4))
        comp = lab3[sl] == i
        if face[sl][comp].mean() > 0.8:
            m = comp.astype(np.uint8); ring = cv2.dilate(m, np.ones((5, 5), np.uint8)) - m
            rr = redish[sl][ring > 0]
            if not (len(rr) and rr.mean() > 0.5): continue                 # 白目・歯（まわりが髪でない）
        bg[lab3 == i] = 1
    # 背景のとなりの、白に近い薄い色（にじみ）も背景へ。3回広げる（リボン本体はのぞく）
    pale3 = ((mn > 200) & (sat < 32)).astype(np.uint8) * (1 - body)
    for _ in range(3):
        bg = np.maximum(bg, pale3 * cv2.dilate(bg, np.ones((3, 3), np.uint8)))
    rough_bg.ribbon_body = body
    return bg, keep


def spread_color(col, known, iters=6):
    """内側（known）の色を、外側へ少しずつ広げる（あいまいな帯の「体の色」の推定）"""
    c = col * known[..., None]; w = known.astype(np.float32)
    out = col * known[..., None]; done = known.astype(bool)
    for r in (3, 5, 9, 15, 25)[:iters]:
        bc = cv2.blur(c, (r, r)); bw = cv2.blur(w, (r, r))
        new = (~done) & (bw > 0.02)
        out[new] = (bc / np.maximum(bw, 1e-4)[..., None])[new]
        done |= new
    return out


def matte(im, k):
    bg, keep = rough_bg(im, k)
    fg = 1 - bg
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    sure_fg = cv2.erode(fg, np.ones((3, 3), np.uint8))            # 確かな体（輪郭の黒い線が入るよう、けずりすぎない）
    sure_bg = cv2.erode(1 - fg, np.ones((5, 5), np.uint8))        # 確かな背景
    band = (1 - sure_fg) * (1 - sure_bg)                            # あいまいな帯（縁の数ピクセル）
    C = im.astype(np.float32)
    # 体の色の推定: 縁のすぐ内側（輪郭線）の色を、いちばん近い所から取る（遠くの服の色を使うと、輪郭線が灰色にうすまる）
    F = spread_color(C, sure_fg)
    dark = cv2.erode(np.where(sure_fg[..., None] > 0, C, 255).astype(np.float32), np.ones((7, 7), np.uint8))   # 3ピクセル以内のいちばん暗い色＝輪郭線
    F = np.where(((band > 0) & (dark.sum(2) < F.sum(2)))[..., None], dark, F)
    num = np.clip(WHITE - C, 0, None).sum(2)
    den = np.clip(WHITE - F, 0, None).sum(2)
    a_band = np.clip(num / np.maximum(den, 30.0), 0, 1)
    # 体の色そのものが白に近い所（リボン・白目・服の白い光）は、計算できないので地図の値をなめらかに使う
    pale_f = den < 60
    soft = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.8)
    a_band = np.where(pale_f, soft, a_band)
    alpha = np.where(sure_fg > 0, 1.0, np.where(sure_bg > 0, 0.0, a_band)).astype(np.float32)
    # 背景の白につながる、ごく薄いにじみは消す（α が小さすぎる所）
    alpha = np.where(alpha < 0.04, 0.0, alpha)
    rb = rough_bg.ribbon_body > 0                                          # リボン本体は、かならず不透明（穴をあけない）
    alpha[rb] = 1.0
    # 本当の色に戻す（白を取り除く）
    a3 = alpha[..., None]
    Fc = np.where(a3 > 0.08, (C - (1 - a3) * WHITE) / np.maximum(a3, 1e-3), F)
    Fc = np.clip(Fc, 0, 255)
    wgt = np.clip(alpha / 0.35, 0, 1)[..., None]                          # α が小さい所は、戻した色がぶれやすいので、推定した体の色に寄せる
    Fc = Fc * wgt + F * (1 - wgt)
    Fc = np.where((band > 0)[..., None], Fc, C)
    Fc[rb] = C[rb]
    return Fc, alpha


def shrink(F, alpha, sc):
    """α をかけた色で縮めてから戻す（縁が白くも黒くもならない）"""
    h, w = alpha.shape
    size = (int(w * sc), int(h * sc))
    pm = cv2.resize(F * alpha[..., None], size, interpolation=cv2.INTER_AREA)
    a = cv2.resize(alpha, size, interpolation=cv2.INTER_AREA)
    col = np.where(a[..., None] > 1e-3, pm / np.maximum(a[..., None], 1e-3), 0)
    return np.dstack([np.clip(col, 0, 255), np.clip(a * 255, 0, 255)]).astype(np.uint8)


if __name__ == "__main__":
    for k in ks:
        im = cv2.imread(f"{SRC}/{k + 1:03d}.png")
        F, a = matte(im, k)
        cv2.imwrite(f"{OUT}/{k:03d}.png", shrink(F, a, SC))
