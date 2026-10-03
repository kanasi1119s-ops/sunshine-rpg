"""全体フィールドの地形を、人間が用意した見本の絵（assets-src/field/reference-field.png）から読み取って置きかえる（2026-10-04）。

gen_world.py が作った world-map.generated.ts の WORLD_ROWS だけを書きかえる（町・村・塔・船などの座標はそのまま）。
gen_world.py を実行し直したときは、続けてこのスクリプトも実行する。

読み取り方:
  - 絵の飾りの縁を除き、地図の 356×267 マスに重ねる（1マス ≒ 2.8×2.8 ドット）。
  - マスの中のドットを色で分け（海・草・森・灰色の岩・茶色の山・砂・雪・雪の森）、いちばん多いものをそのマスの地形にする。
  - 青は、地図の外周から海でつながっていれば海（O）、陸に囲まれていれば湖・川（L）。
  - 道（R）・雲の島（C）・荒れ地（W）・谷（X）・溶岩（Z）・灰（A）・渦の輪（V・Q）は、元の地図のまま残す（道は町どうしを結ぶため）。
  - 町・村・小島・名所・環灯台・塔・船着き場・飛空艇のまわり（半径2マス）と、地図のふち8マスは元のまま。
"""
import colorsys
import re
import sys
from collections import Counter, deque

from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
GEN = f"{ROOT}/src/game/map/world/world-map.generated.ts"
REF = f"{ROOT}/assets-src/field/reference-field.png"
BORDER = 11          # 見本の絵の飾りの縁（ドット）
KEEP = set("RCWXZAVQ")


def classify(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    h *= 360
    if v > 0.80 and s < 0.16:
        return "S"                                  # 雪（白）
    if 180 <= h <= 235 and s >= 0.35:
        return "B"                                  # 水（青）
    if 180 <= h <= 225 and 0.12 <= s < 0.35 and v > 0.45:
        return "T"                                  # 雪の森（青みがかった灰）
    if s < 0.15 and v < 0.85:
        return "M"                                  # 灰色の岩山
    if 70 <= h <= 150 and s >= 0.25:
        return "F" if v < 0.48 else "P"             # 森（暗い緑）・草原
    if 20 <= h < 70 and v > 0.72 and s < 0.55:
        return "D"                                  # 砂
    if 15 <= h < 70 and s >= 0.2:
        return "N"                                  # 茶色のとがった山
    return None


def main():
    src = open(GEN).read()
    i = src.index("WORLD_ROWS"); j = src.index("];", i)
    rows = re.findall(r'"([A-Z]+)"', src[i:j])
    H, W = len(rows), len(rows[0])
    orig = [list(r) for r in rows]
    im = Image.open(REF).convert("RGB")
    im = im.crop((BORDER, BORDER, im.width - BORDER, im.height - BORDER))
    px = im.load(); sx, sy = im.width / W, im.height / H

    new = [r[:] for r in orig]
    for y in range(H):
        for x in range(W):
            if orig[y][x] in KEEP:
                continue
            votes = Counter()
            for py in range(int(y * sy), max(int(y * sy) + 1, int((y + 1) * sy))):
                for qx in range(int(x * sx), max(int(x * sx) + 1, int((x + 1) * sx))):
                    c = classify(*px[min(qx, im.width - 1), min(py, im.height - 1)])
                    if c:
                        votes[c] += 2 if c == "F" else 1   # 森は明るい葉先が草原に読まれやすいので、暗い緑を重く数える
            if votes:
                new[y][x] = votes.most_common(1)[0][0]

    # 道の茶色が「茶色の山」に読まれたもの: 元の道のとなり2マス以内の茶色の山は、草原にする
    for y in range(H):
        for x in range(W):
            if new[y][x] == "N" and any(orig[yy][xx] == "R" for yy in range(max(0, y - 2), min(H, y + 3)) for xx in range(max(0, x - 2), min(W, x + 3))):
                new[y][x] = "P"

    # 雑音を減らす: 読み取ったマスを、まわり3×3でいちばん多い地形に（元のままのマスは数えない）
    sm = [r[:] for r in new]
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if orig[y][x] in KEEP:
                continue
            c = Counter(new[yy][xx] for yy in range(y - 1, y + 2) for xx in range(x - 1, x + 2) if new[yy][xx] not in KEEP)
            top, n = c.most_common(1)[0]
            if n >= 5:
                sm[y][x] = top
    new = sm

    # 雪の森は、雪原の近く（5マス以内）だけ。海岸の浅瀬の水色が雪の森に読まれたものは、元の地形（海・湖なら水、陸なら草原）にする
    for y in range(H):
        for x in range(W):
            if new[y][x] == "T" and orig[y][x] not in "ST" and not any(new[yy][xx] == "S" for yy in range(max(0, y - 5), min(H, y + 6)) for xx in range(max(0, x - 5), min(W, x + 6))):
                new[y][x] = "B" if orig[y][x] in "OL" else "P"

    # 青: 外周から海でつながる所は海（O）、それ以外は湖・川（L）
    sea = [[False] * W for _ in range(H)]
    dq = deque()
    for y in range(H):
        for x in range(W):
            if (x in (0, W - 1) or y in (0, H - 1)) and new[y][x] in "BO":
                sea[y][x] = True; dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and not sea[ny][nx] and new[ny][nx] in "BOVQ":
                sea[ny][nx] = True; dq.append((nx, ny))
    for y in range(H):
        for x in range(W):
            if new[y][x] == "B":
                # 元の地図で湖・川だったところは湖・川、海だったところは海（船の通れる所を変えない）
                new[y][x] = "L" if orig[y][x] == "L" else "O" if orig[y][x] == "O" else ("O" if sea[y][x] else "L")

    # 絵の中のアイコン（船など）が海の上の小さな陸として読まれたものを消す: 元は海で、小さな陸のかたまり
    seen = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if seen[y][x] or new[y][x] in "OL":
                continue
            comp, dq2 = [], deque([(x, y)]); seen[y][x] = True
            while dq2:
                cx, cy = dq2.popleft(); comp.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and new[ny][nx] not in "OL":
                        seen[ny][nx] = True; dq2.append((nx, ny))
            if len(comp) < 40 and all(orig[cy][cx] == "O" for cx, cy in comp):
                for cx, cy in comp:
                    new[cy][cx] = "O"

    # 元のままにする所: ふち8マス・町など大事な場所のまわり
    for y in range(H):
        for x in range(W):
            if x < 8 or y < 8 or x >= W - 8 or y >= H - 8:
                new[y][x] = orig[y][x]
    pts = [(int(a), int(b)) for a, b in re.findall(r"\{ x: (\d+), y: (\d+)", src)]
    pts += [(int(a), int(b)) for a, b in re.findall(r'"x": (\d+), "y": (\d+)', src)]
    for (px_, py_) in pts:
        for y in range(py_ - 2, py_ + 3):
            for x in range(px_ - 2, px_ + 3):
                if 0 <= x < W and 0 <= y < H:
                    new[y][x] = orig[y][x]
    # 道のとなりが水や山でふさがれないよう、道の両どなりで水・山になったマスは元に戻す
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if orig[y][x] == "R":
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if new[y + dy][x + dx] in "OLMN" and orig[y + dy][x + dx] not in "OLMN":
                        new[y + dy][x + dx] = orig[y + dy][x + dx]

    out = ["".join(r) for r in new]
    changed = sum(a != b for r0, r1 in zip(rows, out) for a, b in zip(r0, r1))
    body = "\n".join(f'  "{r}",' for r in out)
    src = src[:i] + "WORLD_ROWS: string[] = [\n" + body + "\n" + src[j:]
    open(GEN, "w").write(src)
    print("書きかえたマス:", changed, "/", W * H, Counter("".join(out)).most_common())


if __name__ == "__main__":
    main()
