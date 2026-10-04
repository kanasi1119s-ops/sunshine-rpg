"""手直しの目を足す edits.py 用の 編集.json を作る（目を光らせる）。
使い方: python3 eyes.py 出力.json 暗い色 明るい色 光の色 行,列,半径 [行,列,半径 ...]
  例: python3 eyes.py edit.json "#5a2a00" "#ffb030" "#fff2c0" 100,110,3 100,124,3 120,90,1.5
目は 外側=暗い色の縁、中=明るい色、左上に光の点（半径2以上のとき）。記号は x/y/z を使う（無ければ）。"""
import json, sys
out, dark, mid, hi = sys.argv[1:5]
pix = []
for spec in sys.argv[5:]:
    r, c, rad = (float(v) for v in spec.split(","))
    R = int(rad) + 2
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            d = (dy * dy + dx * dx) ** 0.5
            if d <= rad + 0.6:
                pix.append([int(r) + dy, int(c) + dx, "y" if d <= rad - 0.4 or rad < 1.5 else "x"])
    if rad >= 2:
        pix.append([int(r) - 1, int(c) - 1, "z"])
    elif rad >= 1:
        pix.append([int(r), int(c), "z"])
json.dump({"palette": {"x": dark, "y": mid, "z": hi}, "pixels": pix}, open(out, "w"))
print(out, len(pix), "点")
