"""木・茂み・草むらの緑を、町の草地の色（オリーブがかった落ちついた緑）になじませる
（2026-10-06、人間の指示「木も草も作り直し町になじんでない」）。
立体の模型から描いた木（props3d_c.py）・草むら（canopy3d.py）の緑は、あざやかすぎ、りんかくも黒くて、
町の草地（terrain:grass-a/b。#496d36〜#6a8f48 の、彩度の低い緑）から浮いていた。
ここでは、パレットの「緑の色」だけを、明るさの順を保ったまま、町の草地と同じ色合いの段へ置きかえる。
りんかく（ほとんど黒）は、こい緑がかった色に。幹・花・実・雪など、緑でない色はそのまま。
使い方: python3 recolor_foliage.py（props3d_c.py・canopy3d.py を作りなおしたあとに、もう一度）。"""
import colorsys
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# 町の草地に合わせた、葉の色の段（暗→明）。草地のいちばん明るい所より、すこし明るい所まで
OLIVE = ["#1a2a14", "#223619", "#2c441f", "#375226", "#42602d", "#4e6e34", "#5a7c3c", "#668a44", "#73974d", "#82a458", "#93b266"]
OUTLINE = "#16220f"
TARGETS = [("tree-pine", "tree-pine", 0, 6), ("bush2", "bush2", 1, 9)]   # （名前, パレット, 使う段のはじめ, おわり）。針葉樹は暗めに   # 草むら（canopy3d.py）は、そちらの色の段を同じ色にした


def hx(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def lum(c):
    r, g, b = hx(c)
    return 0.3 * r + 0.59 * g + 0.11 * b


def is_green(c):
    r, g, b = hx(c)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return 0.17 < h < 0.45 and s > 0.15 and g >= r and g >= b


for name, palname, k0, k1 in TARGETS:
    path = os.path.join(HERE, "pal-" + palname + ".json")
    pal = json.load(open(path))
    greens = sorted({v for v in pal.values() if len(v) == 7 and is_green(v)}, key=lum)
    if not greens:
        continue
    lo, hi = lum(greens[0]), lum(greens[-1])
    new = {}
    for k, v in pal.items():
        if len(v) == 7 and is_green(v):
            t = (lum(v) - lo) / max(1, hi - lo)
            new[k] = OLIVE[k0 + int(round(t * (k1 - k0)))]
        elif len(v) == 7 and lum(v) < 30:
            new[k] = OUTLINE                                     # 黒いりんかく → こい緑
        else:
            new[k] = v
    json.dump(new, open(path, "w"))
    print(name, "greens", len(greens))
