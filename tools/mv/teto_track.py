#!/usr/bin/env python3
"""テトの動画のコマから、口の位置（顔の動き）と口の開き具合を測る（teto_mv.py・teto_matte.py・stage_mv.py が使う）。
使い方: python3 teto_track.py <コマのフォルダ（001.png…）> <出力 json> [口の位置 x y（1コマ目。既定 342 291）]
出力: [[コマ番号, dx, dy, 合い具合(0〜1), 口の中の面積], ...]  dx, dy は1コマ目の口の位置からのずれ
※ 2026-10-27 時点では「たたき台」。今回の動画で使った追跡（track_teto_a.json）とは、上下で最大25ピクセルずれる。
  新しい動画で使うときは、口の位置に四角を描いた確認の絵を作って、口に合っているか必ず目で確かめてから使う。
しくみ: 1コマ目の「目から鼻」のあたり（口の上）を型にして、各コマでいちばん合う所を探す（OpenCV のテンプレート一致）。
        口の中の面積は、口のまわりでピンク〜赤（緑が暗く赤が明るい）の点の数"""
import sys, json, glob, os, cv2, numpy as np
FR, OUT = sys.argv[1], sys.argv[2]
MX0, MY0 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (342, 291)
files = sorted(glob.glob(os.path.join(FR, "[0-9][0-9][0-9].png")))
g0 = cv2.cvtColor(cv2.imread(files[0]), cv2.COLOR_BGR2GRAY)
tpl = g0[MY0 - 120:MY0 - 25, MX0 - 110:MX0 + 110]            # 目〜鼻（口は入れない。口が動いても合うように）
out = []
for k, f in enumerate(files):
    im = cv2.imread(f); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    x0, y0 = MX0 - 110 - 40, MY0 - 120 - 40
    win = g[y0:y0 + tpl.shape[0] + 80, x0:x0 + tpl.shape[1] + 80]
    r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED); _, conf, _, loc = cv2.minMaxLoc(r)
    dx, dy = loc[0] - 40, loc[1] - 40
    mx, my = MX0 + dx, MY0 + dy
    m = im[my - 30:my + 30, mx - 40:mx + 40].astype(int)
    area = int(((m[..., 1] < 170) & (m[..., 2] > 120)).sum())
    out.append([k, int(dx), int(dy), round(float(conf), 3), area])
json.dump(out, open(OUT, "w"))
print("ok", OUT, len(out), "コマ")
