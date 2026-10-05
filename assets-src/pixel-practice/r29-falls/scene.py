"""芯環塔と大滝をひとつにした絵（320×360・16コマ）。2026-10-05、人間の指示「滝と塔をくっつけて、ドットで滝が流れていて、周りが大雨・嵐になって、雷まであるドットの動きを出して」。
重ねる順（奥から）:
  1. 穴と大滝（basin.py の16コマ。水面が穴へ走り、奥の崖を水が底まで落ちる）
  2. 塔（r27-spire の岩の柱。穴の底のさらに下から伸びる）
  3. 塔の足もとを包む、滝つぼの霧と水しぶき（塔の前を、わき上がって流れる）→ 塔と滝が、ひとつの景色になる
  4. 嵐の雲（横いっぱいの、ひとつながりの雲のかたまり。上と左右のふちは、まわりの嵐の暗がりへ溶ける）
  5. 大雨（ななめに降る雨の粒の筋。16コマで切れ目なく降りつづける。ふちほど少なく、まわりの嵐の雨（コード）とつながる）
雷は bolt.py（別の絵）を、ときどき重ねる。
絵のまん中（160, 200）が、塔のマスのまん中。1文字=1色（色は絵ごとに、使う色から記号を割り当てる）。エディタで1コマを4つ（160×180）に分けて確かめる。"""
import json
import math
import os

from PIL import Image

import basin

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
SPIRE = os.path.join(HERE, "..", "r27-spire")
W, H = 320, 360
CX, CY = 160, 200                 # 塔のマスのまん中
FRAMES = basin.FRAMES
TOWER_FEET = 72                   # 塔の絵の足もと（塔のマスのまん中から下へ。world-map の「4マス下」と同じ）

RAIN = [(150, 170, 196), (196, 212, 232), (226, 236, 248)]
MIST = [(120, 136, 160), (168, 184, 204), (204, 216, 230), (236, 242, 250)]
CLOUD = [(16, 17, 26), (26, 28, 40), (40, 43, 58), (58, 62, 82), (82, 87, 110), (110, 115, 138), (142, 147, 168), (176, 180, 198), (206, 210, 226)]
GLOW = (150, 186, 232)


def hsh(x, y, k=0):
    return basin.hsh(x, y, k)


def vnoise(x, y, s, k=0):
    return basin.vnoise(x, y, s, k)


def mix(a, b, t):
    return basin.mix(a, b, t)


def near(rgb, ramp):
    best, bk = 1e18, ramp[0]
    for c in ramp:
        d = sum((c[i] - rgb[i]) ** 2 for i in range(3))
        if d < best:
            best, bk = d, c
    return bk


def load_spire():
    rows = [l for l in open(os.path.join(SPIRE, "spire-natural.txt")).read().split("\n") if l]
    pal = json.load(open(os.path.join(SPIRE, "pal-spire-natural.json")))
    rgb = {k: (int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16)) for k, v in pal.items()}
    return rows, rgb


def cloud_layer():
    """横いっぱいの嵐の雲（どのコマも同じ）。濃さの場の傾きで面の向きを出し、左上の光で陰。下はどっしり、ふちは銀、塔の上で稲光がほのかに光る。"""
    layer = {}
    puffs = []
    for k in range(110):
        px = -16 + (k * 53) % 352 + (hsh(k, 1, 80) - 0.5) * 14
        py = 4 + (k * 37) % 96 + (hsh(k, 2, 80) - 0.5) * 10
        pr = 15 + hsh(k, 3, 80) * 16
        puffs.append((px, py, pr))
    for (dx, py, pr) in ((-14, 92, 20), (12, 96, 19), (0, 104, 16), (-30, 88, 17), (30, 90, 17)):
        puffs.append((CX + dx, py, pr))

    def dens(x, y):
        d = 0.0
        for (px, py, pr) in puffs:
            q = ((x - px) ** 2 + ((y - py) * 1.3) ** 2) ** 0.5 / pr
            if q < 1:
                d = max(d, 1 - q * q)
        d += (vnoise(x * 1.1, y * 1.4, 12, 81) * 0.6 + vnoise(x, y, 5, 82) * 0.4 - 0.5) * 0.5
        bottom = 104 + (vnoise(x, 3, 14, 83) - 0.5) * 26
        d -= max(0.0, (y - bottom) / 8)
        edge = min(x, W - 1 - x) / 40                      # 左右のふちで薄く
        d -= max(0.0, 1 - edge) * 0.6
        if abs(x - CX) < 64 and y < 96:
            d = max(d, 0.5 + (vnoise(x, y, 7, 79) - 0.5) * 0.3)   # 塔の上は、必ず厚い雲（もこもこのまま）
        return d

    TH = 0.3
    for y in range(0, 136):
        for x in range(W):
            d = dens(x + 0.5, y + 0.5)
            if d < TH:
                continue
            if d < TH + 0.06 and hsh(x, y, 84) < 0.5:
                continue                                   # ふちは、ちぎれて溶ける
            if y > 60 and abs(x - CX) > 130 and d < 0.45:
                continue                                   # 下のはしの、はなれた小さなかたまりは描かない
            gx = dens(x + 1.5, y + 0.5) - dens(x - 0.5, y + 0.5)
            gy = dens(x + 0.5, y + 1.5) - dens(x + 0.5, y - 0.5)
            lit = (gx * 0.6 + gy * 0.8) * 2.0
            v = 0.4 + lit - (y / 136) * 0.22 + (vnoise(x * 2, y * 2, 4, 85) - 0.5) * 0.1
            if d < TH + 0.08 and lit > 0.05:
                v += 0.22
            if d > 0.8:
                v -= 0.08
            col = mix(CLOUD[0], CLOUD[-1], max(0.0, min(1.0, v)))
            glow = max(0.0, 1 - (((x - CX) / 60) ** 2 + ((y - 70) / 30) ** 2))
            col = mix(col, GLOW, glow * 0.4)
            layer[(x, y)] = near(col, CLOUD + [GLOW])
    # ちぎれた雲の筋（塔のまわりに、すそからたれる）
    for k in range(16):
        sx = int(CX + (hsh(k, 4, 86) - 0.5) * 120)
        ln = 8 + int(hsh(k, 5, 86) * 18)
        for j in range(ln):
            y = 106 + j
            x = sx + int(math.sin(j / 3.0 + k) * 1.5)
            if 0 <= x < W:
                layer[(x, y)] = CLOUD[3] if j < ln * 0.6 else CLOUD[2]
    return layer


def front_mist(x, y, fr):
    """塔の足もとを包む、滝つぼの霧（塔の前）。横へ流れながら、上へわき上がる。16コマで1周。"""
    px, py = x - CX, y - CY
    # 霧の帯: 塔の足もと（穴の底のあたり）に、横長に
    band = 1 - abs(py - 36) / 34
    if band <= 0 or abs(px) > 100:
        return None
    side = 1 - abs(px) / 100
    n = basin.vnoise_py(px + fr * 2, py, 10, 8, 87, 32) * 0.55 + basin.vnoise_py(py, px + fr * 2, 5, 8, 88, 32) * 0.45
    v = band * 0.9 + side * 0.35 + (n - 0.5) * 1.1 - 0.55
    if v < 0.18:
        return None
    if v < 0.28 and hsh(x, y + fr, 89) < 0.5:
        return None
    return MIST[min(3, int(v * 4))]


def rain(x, y, fr):
    """大雨: ななめ（右上から左下）に降る、長さ5〜8の雨の筋。コマごとに12ドット落ちる（16コマで192ドット＝1周）。ふちほど少ない。"""
    L = FRAMES * 12
    # 雨の筋は、左下へ傾く（3ドット下がるごとに1ドット左）
    lane = x + y // 3
    if hsh(lane, 0, 90) > 0.30:
        return None
    phase = int(hsh(lane, 1, 91) * L)
    length = 5 + int(hsh(lane, 2, 92) * 4)
    t = (y - fr * 12 - phase) % L
    # 1本の筋につき、くり返しの中に2つ（間をあける）
    t2 = t % (L // 2)
    if t2 >= length:
        return None
    edge = min(x, W - 1 - x, y, H - 1 - y) / 50
    if hsh(lane, t // (L // 2), 93) > min(1.0, edge + 0.15):
        return None
    return RAIN[2] if t2 == length - 1 else (RAIN[1] if t2 > length // 2 else RAIN[0])


def build():
    spire_rows, spire_rgb = load_spire()
    clouds = cloud_layer()
    sw, sh = len(spire_rows[0]), len(spire_rows)
    sx0 = CX - sw // 2
    sy0 = CY + TOWER_FEET - sh
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.new("RGBA", (W * FRAMES, H), (0, 0, 0, 0))
    pool = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    for fr in range(FRAMES):
        # 1. 穴と大滝
        brows = [l for l in open(os.path.join(HERE, f"basin-{fr}.txt")).read().split("\n") if l]
        bpal = json.load(open(os.path.join(HERE, f"pal-basin-{fr}.json")))
        img = [[None] * W for _ in range(H)]
        bx0, by0 = CX - 144, CY - 144
        for y, r in enumerate(brows):
            for x, ch in enumerate(r):
                if ch != ".":
                    v = bpal[ch]
                    img[by0 + y][bx0 + x] = (int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16))
        # 2. 塔
        for y, r in enumerate(spire_rows):
            for x, ch in enumerate(r):
                if ch != "." and 0 <= sy0 + y < H:
                    img[sy0 + y][sx0 + x] = spire_rgb[ch]
        # 3. 塔の足もとの霧
        for y in range(H):
            for x in range(W):
                m = front_mist(x, y, fr)
                if m is not None:
                    img[y][x] = m
        # 4. 雲
        for (x, y), c in clouds.items():
            img[y][x] = c
        # 5. 大雨
        for y in range(H):
            for x in range(W):
                d = rain(x, y, fr)
                if d is not None:
                    img[y][x] = d
        # 書き出し（色ごとに記号を割り当てる）
        colors = sorted({c for row in img for c in row if c is not None})
        assert len(colors) <= len(pool), len(colors)
        key = {c: pool[i] for i, c in enumerate(colors)}
        rows = ["".join("." if c is None else key[c] for c in row) for row in img]
        with open(os.path.join(HERE, f"scene-{fr}.txt"), "w") as f:
            f.write("\n".join(rows) + "\n")
        with open(os.path.join(HERE, f"pal-scene-{fr}.json"), "w") as f:
            json.dump({key[c]: "#%02x%02x%02x" % c for c in colors}, f)
        for y in range(H):
            for x in range(W):
                if img[y][x] is not None:
                    sheet.putpixel((fr * W + x, y), img[y][x] + (255,))
    sheet.save(os.path.join(OUT, "scene.png"))
    print("ok", len(colors))


if __name__ == "__main__":
    build()
