"""芯環塔（3回目の作り直し）。2026-10-05、人間の指示「入口はいらない。もっとリアルに、遠近感を感じ、陥没した更に下から伸びているように。
塔は円柱を意識して」「リアルにリアルに細かいドット絵を作って」。
- 円柱: 1列ずつ、柱の丸みに沿った光（左上から）と、右のふちの、稲光の青い照り返し。
- 岩: 自然の岩。層の線は、見下ろしているので、柱の丸みに沿って下へ弓なりに曲がる。細かな割れ目、縦の溝（風と水で削られた）、ほのかに光る石の筋。
- 遠近: 上ほど細く、かすんで青白く（遠い）。下は陥没の底のさらに下へ消え、闇と霧に溶ける（足もとは見えない）。
- 上は嵐の雲にのまれる。入口はない。
色は、1ドットごとに光と色を計算してから、手で選んだ色の表（下の PAL）のいちばん近い色にそろえる。96×256（下そろえ）。既存作品の塔の絵は写していない。"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 96, 256

PAL_RGB = {
    # 岩（暗→明。少しむらさきがかった灰）
    "a": (12, 10, 16), "b": (22, 19, 28), "c": (33, 29, 40), "d": (46, 41, 54), "e": (62, 56, 70),
    "f": (80, 73, 88), "g": (100, 92, 106), "h": (124, 115, 126), "i": (150, 141, 148), "j": (178, 170, 172),
    # かすみ（遠い上のほう）
    "k": (88, 94, 116), "l": (112, 118, 140), "m": (140, 146, 166),
    # 青い照り返し（稲光）
    "n": (70, 92, 140), "o": (120, 150, 200),
    # 光る石の筋
    "p": (40, 150, 170), "q": (130, 230, 240),
    # 雲（暗→明）
    "1": (16, 17, 26), "r": (26, 28, 40), "s": (40, 43, 58), "t": (58, 62, 82), "u": (82, 87, 110), "v": (110, 115, 138), "w": (142, 147, 168), "x": (176, 180, 198),
    "2": (206, 210, 226), "3": (150, 186, 232),
    # 底の霧
    "y": (60, 70, 92), "z": (90, 102, 124),
}
KEYS = list(PAL_RGB)


def nearest(rgb, allowed=None):
    best, bk = 1e9, None
    for k in (allowed or KEYS):
        c = PAL_RGB[k]
        d = (c[0] - rgb[0]) ** 2 * 0.3 + (c[1] - rgb[1]) ** 2 * 0.59 + (c[2] - rgb[2]) ** 2 * 0.11
        if d < best:
            best, bk = d, k
    return bk


def hsh(x, y, k=0):
    h = (x * 374761393 + y * 668265263 + k * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFFFF) / 4294967296


def vnoise(x, y, s, k=0):
    """なめらかな雑音（格子の値を補間）。"""
    gx, gy = x / s, y / s
    x0, y0 = math.floor(gx), math.floor(gy)
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = hsh(x0, y0, k); b = hsh(x0 + 1, y0, k); c = hsh(x0, y0 + 1, k); d = hsh(x0 + 1, y0 + 1, k)
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def fbm(x, y, k=0):
    return vnoise(x, y, 12, k) * 0.5 + vnoise(x, y, 6, k + 1) * 0.3 + vnoise(x, y, 3, k + 2) * 0.2


CLOUD_BOTTOM = 74     # 雲のすそ（これより上は雲）
ABYSS = 228           # これより下は陥没の底の闇へ


def cx_at(y):
    return 48 + 1.6 * math.sin(y / 41.0)


def hw_at(y):
    # 上ほど細い（遠い）。下へ向かってゆっくり太り、底では闇に消える
    t = (y - 20) / (H - 20)
    return 11 + 12 * t + 0.8 * math.sin(y / 7.3)


def mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def rock_rgb(x, y):
    """自然の岩の柱（柱状の岩の束）。柱の丸みに沿って、たての岩の柱が並ぶ（ふちへ行くほど細く見える＝円柱に見える）。"""
    c = cx_at(y)
    hw = hw_at(y)
    u = (x + 0.5 - c) / hw
    if abs(u) > 1:
        return None
    a = math.asin(max(-1.0, min(1.0, u)))                 # 柱のまわりの角度（-90°〜90°）
    twist = y / 160.0 + vnoise(0, y, 40, 3) * 0.25           # ゆるいねじれ
    colw = 0.23
    q = (a + twist) / colw
    col = math.floor(q)
    f = q - col
    # ふちのでこぼこ: 一番外の岩の柱は、高さごとに少し欠ける
    if abs(u) > 0.93 and hsh(col, int(y // 5), 9) > 0.55:
        return None
    # 岩の柱1本の面: 柱の中で少し角ばった面（左の面・正面・右の面）
    facet = -0.35 if f < 0.33 else (0.0 if f < 0.7 else 0.35)
    theta = a + facet
    lam = max(0.0, math.cos(theta + 0.85)) * 0.95
    tone = (hsh(col, 1, 5) - 0.5) * 0.2                       # 柱ごとの色のちがい
    v = 0.08 + lam * 0.72 + tone + (fbm(x * 1.6, y * 0.6, 11) - 0.5) * 0.16
    if f < 0.08 or f > 0.95:
        v -= 0.3                                               # 柱と柱のすき間（深い影）
    # 横の節目（柱ごとに、ばらばらの高さ）。節の上は影、すぐ下は光
    seg = 24 + int(hsh(col, 2, 6) * 30)
    off = int(hsh(col, 3, 6) * seg)
    sy = int(y + math.cos(a) * 3.5) + off                      # 見下ろしているので、節は丸みに沿って下へ弓なり
    m = sy % seg
    if m == 0 and 0.12 < f < 0.9:
        v -= 0.3
    elif m == 1 and 0.12 < f < 0.9:
        v += 0.08
    base = mix(PAL_RGB["a"], PAL_RGB["j"], max(0.0, min(1.0, v)))
    # 右のふちの、稲光の青い照り返し
    if u > 0.55:
        base = mix(base, PAL_RGB["o"], min(0.5, (u - 0.55) * 1.3))
    # 遠近: 上ほど少しかすむ
    haze = max(0.0, min(0.5, (140 - y) / 130))
    base = mix(base, PAL_RGB["k"], haze)
    # 下は陥没の底の闇へ
    if y > ABYSS - 44:
        dark = min(1.0, (y - (ABYSS - 44)) / 74)
        base = mix(base, PAL_RGB["a"], dark * 0.94)
    return base


def build():
    g = [["."] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            rgb = rock_rgb(x, y)
            if rgb is not None:
                g[y][x] = nearest(rgb, list("abcdefghijklmno"))
    # 光る石の筋: 柱をらせん状にのぼる細い筋（手前の半分だけ見える）。まわりにかすかな光
    for k in range(3):
        for y in range(CLOUD_BOTTOM + 4, ABYSS - 6):
            ph = y / 23.0 + k * 2.1
            u = math.sin(ph)
            if math.cos(ph) < 0:                 # 裏がわ
                continue
            x = int(round(cx_at(y) + u * hw_at(y) * 0.92))
            if 0 <= x < W and g[y][x] != ".":
                g[y][x] = "q" if (y + k) % 9 == 0 else "p"
                for dx in (-1, 1):
                    if 0 <= x + dx < W and g[y][x + dx] in "abcdef":
                        g[y][x + dx] = "e" if g[y][x + dx] in "abcd" else "n"
    # 陥没の底の霧（下のほうに、横にたなびく帯。柱の上にかかる）
    for y in range(ABYSS - 30, H):
        for x in range(W):
            band = math.sin(y / 5.5 + vnoise(x, y, 14, 21) * 3)
            amt = (y - (ABYSS - 30)) / 60
            if band > 0.62 - amt * 0.4 and vnoise(x, y, 9, 22) > 0.45:
                g[y][x] = "z" if band > 0.85 else "y"
    # 嵐の雲（上をのみこむ）: 雲の濃さの場を作り、その傾きから面の向きを出して、左上の光で陰をつける（かたまりは、ひとつながり）。
    # 下はどっしり暗く、上のふちは銀色に光り、雲の中に稲光のほのかな光。すそからは、ちぎれた雲の筋が塔にまとわりつく。
    puffs = []
    for k in range(44):
        px = (k * 41) % 108 - 6 + (hsh(k, 1, 50) - 0.5) * 10
        py = 4 + (k * 29 % 62) + (hsh(k, 2, 50) - 0.5) * 8
        pr = 11 + hsh(k, 3, 50) * 13
        puffs.append((px, py, pr))
    # 塔の上をおおう、大きなかたまり（いちばん手前・下）
    for (dx, py, pr) in ((-10, 56, 17), (9, 60, 16), (0, 66, 14), (-4, 46, 18), (12, 48, 15)):
        puffs.append((cx_at(py) + dx, py, pr))

    def dens(x, y):
        d = 0.0
        for (px, py, pr) in puffs:
            q = ((x - px) ** 2 + ((y - py) * 1.35) ** 2) ** 0.5 / pr
            if q < 1:
                d = max(d, (1 - q * q))
        d += (fbm(x * 1.2, y * 1.6, 61) - 0.5) * 0.45
        d -= max(0.0, (y - (CLOUD_BOTTOM - 8 + (fbm(x * 1.5, 3, 65) - 0.5) * 18)) / 9)   # すそで薄くなる（すそのふちは、ちぎれてでこぼこ）
        return d

    TH = 0.28
    for y in range(0, CLOUD_BOTTOM + 12):
        for x in range(W):
            d = dens(x + 0.5, y + 0.5)
            if d < TH:
                continue
            gx = dens(x + 1.5, y + 0.5) - dens(x - 0.5, y + 0.5)
            gy = dens(x + 0.5, y + 1.5) - dens(x + 0.5, y - 0.5)
            # 面の向き: 濃さが増す向きの反対が外向き。左上（-0.6, -0.8）からの光
            lit = (gx * 0.6 + gy * 0.8) * 2.2
            v = 0.42 + lit - (y / CLOUD_BOTTOM) * 0.22 + (fbm(x * 2, y * 2, 63) - 0.5) * 0.12
            edge = d < TH + 0.07
            if edge and lit > 0.05:
                v += 0.25                                    # 銀のふち
            if d > 0.75:
                v -= 0.08                                    # 奥まった、濃いところ
            col = mix(PAL_RGB["1"], PAL_RGB["2"], max(0.0, min(1.0, v)))
            # 雲の中の稲光のほのかな光（塔の上のあたり）
            glow = max(0.0, 1 - (((x - 52) / 22) ** 2 + ((y - 34) / 16) ** 2))
            if glow > 0:
                col = mix(col, PAL_RGB["3"], glow * 0.45)
            g[y][x] = nearest(col, list("1rstuvwx23"))
    # ちぎれた雲の筋（すそから下へたれて、塔にまとわりつく）
    for k in range(9):
        sx = int(cx_at(CLOUD_BOTTOM) + (hsh(k, 4, 64) - 0.5) * (hw_at(CLOUD_BOTTOM) * 2 + 18))
        ln = 6 + int(hsh(k, 5, 64) * 14)
        for j in range(ln):
            y = CLOUD_BOTTOM + 2 + j
            x = sx + int(math.sin(j / 3.0 + k) * 1.5)
            if 0 <= x < W and y < H:
                g[y][x] = "t" if j < ln * 0.6 else "s"
                if j < ln * 0.4 and 0 <= x + 1 < W:
                    g[y][x + 1] = "u"
    rows = ["".join(r) for r in g]
    used = sorted(set("".join(rows)) - {"."})
    pal = {k: "#%02x%02x%02x" % PAL_RGB[k] for k in used}
    with open(os.path.join(HERE, "spire-natural.txt"), "w") as f:
        f.write("\n".join(rows) + "\n")
    with open(os.path.join(HERE, "pal-spire-natural.json"), "w") as f:
        json.dump(pal, f, ensure_ascii=False)
    print("色数", len(used))


if __name__ == "__main__":
    build()
