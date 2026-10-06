"""芯環塔から外を見る景色（2026-10-06、人間の指示「塔から外が見れる場所とかもほしいかも。それを塔の中のイベントに入れて」）。
400×225（ゲームの画面いっぱい）。イベントの会話のうしろに出す。

  vista-clouds.txt  風の回廊（昼）: 石のアーチ窓の向こうに、雲海と、遠い大陸・浮嶼の島々
  vista-summit.txt  頂の見晴らし（夜明け）: 石の欄干の向こうに、朝焼けの空・海・大陸の町の灯り、空にかかる欠けた光の環の跡

ドット絵の決まり（CLAUDE.md）: 光は左上。面の向きで明るさを変え、くぼみ・重なりの奥は暗く。石は目地・欠け・こけ。
市松（ディザ）は、となりあう2つの色の段のあいだだけに使う（4×4のベイヤー）。手前の石には、地面になじむ柔らかい影。
既存作の景色・塔のデザインはまねしない（CLAUDE.md 1-1）。

確認: ドット絵エディタは256マスまでなので、左右の半分（*-left.txt / *-right.txt、200×225）に分けて読みこみ、
4枚とも「文字グリッドとの食い違い 0 マス」（2026-10-06）。"""
import json, math, os, random
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 400, 225
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
SYMS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@$%&*+=?"


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


class Canvas:
    def __init__(self):
        self.px = [[None] * W for _ in range(H)]

    def put(self, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            self.px[y][x] = c

    def ramp(self, x, y, ramp, v):
        """v（0〜1）を、色の段（ramp）に当てはめる。段と段のあいだだけ、ベイヤーの市松でまぜる。"""
        v = min(max(v, 0.0), 0.9999) * (len(ramp) - 1)
        i = int(v)
        f = v - i
        t = (BAYER[y & 3][x & 3] + 0.5) / 16
        self.put(x, y, ramp[min(i + (1 if f > t else 0), len(ramp) - 1)])

    def save(self, name):
        used = sorted({c for row in self.px for c in row if c})
        assert len(used) <= len(SYMS), len(used)
        sym = {c: SYMS[i] for i, c in enumerate(used)}
        txt = "\n".join("".join(sym[c] if c else "." for c in row) for row in self.px) + "\n"
        open(os.path.join(HERE, f"{name}.txt"), "w").write(txt)
        json.dump({sym[c]: c for c in used}, open(os.path.join(HERE, f"{name}-pal.json"), "w"))
        try:
            from PIL import Image
            im = Image.new("RGB", (W, H))
            im.putdata([hexrgb(c or "#000000") for row in self.px for c in row])
            im.save(os.path.join(HERE, f"{name}.png"))
        except ImportError:
            pass
        print(name, len(used), "colors")


def noise(seed):
    rnd = random.Random(seed)
    pts = [(rnd.random() * 6.28, rnd.random() * 6.28, rnd.uniform(0.6, 1.4)) for _ in range(6)]

    def f(x, y):
        return sum(math.sin(x * 0.045 * k + a) * math.cos(y * 0.06 * k + b) / k for a, b, k in pts) / 3

    return f


# ───────────────────────── 共通の部品 ─────────────────────────
def puff_clouds(cv, y0, y1, ramp, seed, rmin, rmax, rows=3):
    """雲海を、もこもこの雲のかたまり（いくつもの丸の寄せ集め・底は平ら）として描く。奥の段から手前へ重ねる。
    丸の面の向きで明るさを決め（光は左上）、かたまりの下・重なりの奥は暗い。すきまは、下に敷いた暗めの雲の層でうめる。"""
    rnd = random.Random(seed)
    # 下に敷く層（かたまりのすきまに見える、奥の雲）
    for y in range(int(y0 + (y1 - y0) * 0.35), min(H, y1 + 20)):
        for x in range(W):
            cv.ramp(x, y, ramp, 0.3 + 0.06 * math.sin(x * 0.11 + y * 0.3))
    puffs = []
    for r_i in range(rows):
        base = y0 + (y1 - y0) * (r_i + 1) / rows
        x = -rmax * 2 + rnd.uniform(0, rmax)
        while x < W + rmax * 2:
            size = rnd.uniform(rmin, rmax)
            # 1つのかたまり: 底の大きな丸2〜3つと、上に小さな丸
            for k in range(rnd.randint(3, 5)):
                ox = rnd.uniform(-1.3, 1.3) * size
                rr = size * rnd.uniform(0.55, 0.9) * (1 - abs(ox) / (2.2 * size))
                up = (1 - abs(ox) / (1.6 * size)) * size * rnd.uniform(0.3, 0.8)
                puffs.append((x + ox, base - rr * 0.4 - up, rr, base))
            x += size * rnd.uniform(2.0, 2.8)
    puffs.sort(key=lambda p: (p[3], p[1]))
    L = (-0.5, -0.7, 0.5)
    for (cx, cy, r, base) in puffs:
        for y in range(int(cy - r), min(H, int(base) + 2)):
            for x in range(int(cx - r), int(cx + r) + 1):
                dx, dy = (x - cx) / r, (y - cy) / r
                d2 = dx * dx + dy * dy
                if d2 > 1 and not (y > cy and abs(dx) < 0.95):
                    continue  # 丸の外（ただし、丸の下は底まで四角くのばして平らな底にする）
                d2 = min(d2, 0.999)
                nz = math.sqrt(1 - d2)
                lam = max(0.0, dx * L[0] + dy * L[1] + nz * L[2])
                v = 0.38 + lam * 0.7
                if y > cy:
                    v -= (y - cy) / max(1, base - cy) * 0.28  # 底に近いほど影
                if d2 > 0.82 and dy < -0.25 and dx < 0.35:
                    v = 1.0  # 光の当たるふち
                cv.ramp(x, y, ramp, v)


def clouds_band(cv, y0, y1, ramp, seed, scale=1.0, top_light=True, thresh=0.0):
    """雲海: もこもこの上ふちを持つ帯。上（空に面した側）が明るく、下ほど・奥ほど暗い。"""
    n = noise(seed)
    for x in range(W):
        # 上ふちの高さ（丸いこぶの連なり）
        bump = 0
        for k, (p, a) in enumerate([(37, 5), (23, 3), (11, 1.6)]):
            bump += a * scale * (0.5 + 0.5 * math.sin(x / p * 6.28 / 2 + seed * (k + 1)))
        top = y0 + 6 * scale - bump
        for y in range(int(top), y1):
            d = (y - top) / max(1, (y1 - top))
            # こぶの左上が光る: 横の傾きで明るさを足す
            slope = math.cos(x / 37 * 3.14 + seed) * 0.12
            v = 0.95 - d * 0.9 + slope + n(x, y) * 0.15 + thresh
            if y - top < 1.2:
                v = 1.0  # ふちの光
            cv.ramp(x, y, ramp, v)


# ───────────────────────── 風の回廊（昼）─────────────────────────
def vista_clouds():
    cv = Canvas()
    sky = ["#2c5a9c", "#3a6eb2", "#4c84c4", "#6a9ed2", "#8cb8de", "#b4d2ea"]
    for y in range(H):
        for x in range(W):
            cv.ramp(x, y, sky, 0.05 + y / 150)
    # 太陽（左上）と、そのまわりのにじみ
    sx, sy = 150, 56
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - sx, y - sy)
            if d < 9:
                cv.put(x, y, "#fffbe8" if d < 7 else "#fff0c0")
            elif d < 44:
                base_v = 0.05 + y / 150
                glow = (1 - (d - 9) / 35) ** 2
                cv.ramp(x, y, sky + ["#dceaf2"], base_v + glow * 0.75)
    # 遠い大陸（かすんだ青）。高さの傾きで面の向きを出す: 右へ上る面（左上を向く）は明るく、右へ下る面は暗い
    mount = ["#5a7aa8", "#6a8cb8", "#86a6cc", "#a0bcd8"]
    hx = lambda x: 20 + 11 * math.sin(x / 41 + 1) + 7 * abs(math.sin(x / 17 + 2)) + 3 * math.sin(x / 6.1)
    for x in range(W):
        h = hx(x)
        slope = h - hx(x - 1.0)
        top = 116 - h
        for y in range(int(top), 130):
            v = 0.5 + max(-0.35, min(0.35, slope * 0.35)) - (y - top) / 70
            if y - int(top) < 1:
                v = 0.98 if slope > -0.2 else 0.7
            cv.ramp(x, y, mount, v)
    # 浮嶼の島々（空に浮かぶ岩の島。上に草、下は岩のつらら）
    for (cx, cy, r) in [(300, 70, 13), (338, 88, 7), (262, 92, 5)]:
        for y in range(cy - r, cy + int(r * 1.6)):
            for x in range(cx - r - 2, cx + r + 2):
                if y < cy:
                    if (x - cx) ** 2 / (r + 1.5) ** 2 + (y - cy) ** 2 / (r * 0.45) ** 2 <= 1:
                        lit = (x - cx) / r < -0.2 or y < cy - r * 0.3
                        cv.put(x, y, "#7aa070" if lit else "#5a8060")
                        if y <= cy - int(r * 0.45) + 1:
                            cv.put(x, y, "#9ac088")
                else:
                    w = r * (1 - (y - cy) / (r * 1.6)) + 0.5 * math.sin(x * 1.7)
                    if abs(x - cx) <= w:
                        cv.ramp(x, y, ["#4a5878", "#5e6c8a", "#7a88a2"], 0.75 - (x - cx + w) / (2 * w + 1) * 0.6 - (y - cy) / (r * 3))
    # 雲海（奥 → 手前の3段）
    far = ["#a8c0dc", "#c0d4e8", "#d8e6f2", "#eef4fa"]
    mid = ["#8ea8cc", "#aac0dc", "#cad8ea", "#e8f0f8", "#ffffff"]
    near = ["#7890b8", "#94acd0", "#b6c8e2", "#d6e2f0", "#f4f8fc", "#ffffff"]
    puff_clouds(cv, 112, 136, far, 3, 6, 10, rows=2)
    puff_clouds(cv, 132, 166, mid, 7, 10, 16, rows=2)
    puff_clouds(cv, 160, H + 6, near, 11, 16, 26, rows=2)
    # 小さな飛空艇のかげ（遠く、右の雲の上）
    for dx, row in enumerate(["..AA..", ".AAAA.", "AAAAAA", ".A..A."]):
        pass
    ship = [" ### ", "#####", " # # "]
    for j, row in enumerate(ship):
        for i, ch in enumerate(row):
            if ch == "#":
                cv.put(218 + i, 104 + j, "#4a5878")
    stone_arch(cv)
    cv.save("vista-clouds")


def stone_arch(cv):
    """手前の石のアーチ窓（光は左上: 窓のふちの右側・下側の面が明るく、左上のふちの奥は暗い）。"""
    stone = ["#2a2430", "#3c3442", "#504656", "#685c6c", "#827486", "#9c8ea0"]
    moss = ["#3a4a34", "#4e6040", "#647a50"]
    cx, top, half = W // 2, 18, 168
    rnd = random.Random(5)

    def inside(x, y):
        # アーチの開口: 上は半円、下はまっすぐ
        if abs(x - cx) > half:
            return False
        if y >= top + half * 0.55:
            return y < H - 30
        return (x - cx) ** 2 / half ** 2 + (y - (top + half * 0.55)) ** 2 / (half * 0.55) ** 2 <= 1

    for y in range(H):
        for x in range(W):
            if inside(x, y):
                continue
            # 開口までの近さ（ふちの面取り）
            near = 99
            for d in range(1, 7):
                if inside(x + d, y) or inside(x - d, y) or inside(x, y + d) or inside(x, y - d):
                    near = d
                    break
            # 石積み: 1段 12 ドット、石の幅 26 ドット（段ごとに半分ずらす）。石ごとに少し色を変え、左上のふちに光、右下のふちに影（面取り）
            row = y // 12
            off = (row % 2) * 13
            col = (x + off) // 26
            lx, ly = (x + off) % 26, y % 12
            tone = random.Random(row * 131 + col * 17).uniform(-0.07, 0.07)
            v = 0.42 + tone - ly * 0.006
            if lx == 0 or ly == 0:
                v = 0.12  # 目地
            elif lx == 1 or ly == 1:
                v = 0.62 + tone  # 左上のふち（光）
            elif lx == 25 or ly == 11:
                v = 0.26 + tone  # 右下のふち（影）
            if rnd.random() < 0.02 and v > 0.3:
                v -= 0.12  # 欠け・よごれ
            if near <= 6:
                # 開口のふち（厚みの面）: 左上を向いた面は明るい、右下を向いた面は暗い
                face_lit = inside(x + near, y) or inside(x, y + near)
                v = 0.78 - near * 0.05 if face_lit else 0.16 + near * 0.025
                if near == 1:
                    v = 0.97 if face_lit else 0.06
            cv.ramp(x, y, stone, v)
            jx = lx == 0
            jy = ly == 0
            # こけ（下のほうの、目地ぞい）
            if y > H - 70 and near > 6 and (jy or jx) and rnd.random() < 0.45:
                cv.put(x, y, moss[rnd.randrange(3)])
    # 窓台（手前の石の台）: 上の面は空の光を受けて明るく、前の面は石を1つずつ面取り。台の上ふちの手前に光の線
    for y in range(H - 30, H):
        for x in range(cx - half - 4, cx + half + 5):
            if y < H - 25:
                v = 0.95 if y == H - 30 else 0.84 - (y - (H - 30)) * 0.05 + 0.03 * math.sin(x * 0.6)
            elif y == H - 25:
                v = 0.08  # 上の面と前の面のさかいの影
            else:
                ly, lx = y - (H - 24), (x + (5 if (y - (H - 24)) // 12 else 0)) % 34
                tone = random.Random(x // 34 * 7 + 3).uniform(-0.05, 0.05)
                v = 0.4 + tone
                if lx == 0 or ly % 12 == 0:
                    v = 0.12
                elif lx == 1 or ly % 12 == 1:
                    v = 0.58 + tone
                elif lx == 33:
                    v = 0.25
            cv.ramp(x, y, stone, v)


# ───────────────────────── 頂の見晴らし（夜明け）─────────────────────────
def vista_summit():
    cv = Canvas()
    sky = ["#141632", "#1e2048", "#2c2a5c", "#46366c", "#6a4474", "#984e6e", "#c8645e", "#e8865a", "#f6b070", "#fcd896"]
    horizon = 132
    for y in range(H):
        for x in range(W):
            cv.ramp(x, y, sky, (y / horizon) ** 1.4)
    # のこっている星（上のほうだけ。色は2段）
    rnd = random.Random(9)
    for _ in range(70):
        x, y = rnd.randrange(W), rnd.randrange(60)
        cv.put(x, y, "#e8e8ff" if rnd.random() < 0.3 else "#9a9ad0")
    # 空にかかる、欠けた光の環の跡（大きな楕円の弧。ところどころ途切れる）
    rcx, rcy, ra, rb = 200, 150, 230, 120
    for i in range(2400):
        t = math.pi + i / 2400 * math.pi
        if any(a < t < b for a, b in [(3.7, 3.82), (4.6, 4.75), (5.5, 5.58)]):
            continue  # 欠けたところ
        x = rcx + ra * math.cos(t)
        y = rcy + rb * math.sin(t)
        for o, c in [(-1, "#c8c0ff"), (0, "#fff8e0"), (1, "#d8b8f0")]:
            cv.put(int(x), int(y) + o, c)
        if i % 3 == 0:
            cv.put(int(x), int(y) - 2, "#7a70b8")
    # 太陽（地平線から顔を出したところ）と、海への光の道
    sx = 128
    for y in range(horizon - 10, horizon + 1):
        for x in range(sx - 14, sx + 15):
            if math.hypot(x - sx, y - horizon) < 12:
                cv.put(x, y, "#fff6d8" if math.hypot(x - sx, y - horizon) < 10 else "#ffe2a0")
    # 遠い大陸（右）。夜明けの逆光で、左（太陽側）の稜線だけ明るい
    land = ["#1e1a34", "#2a2440", "#3a3050", "#57406a"]
    for x in range(150, W):
        h = 10 + 8 * math.sin(x / 33) + 4 * math.sin(x / 11 + 1) + 2 * math.sin(x / 4.1)
        h *= min(1, (x - 150) / 40)
        top = horizon - h
        for y in range(int(top), horizon + 4):
            v = 0.35 - (y - top) / 50
            if y - top < 1:
                v = 0.98
            cv.ramp(x, y, land, v)
    # 海（夜明けの空を映す。太陽の下に、光の道）
    sea = ["#1a1c3c", "#262a52", "#3a3a66", "#5a4a78", "#8a5a78", "#c87a70", "#f0b080", "#fff0c8"]
    for y in range(horizon + 1, H):
        for x in range(W):
            d = (y - horizon) / (H - horizon)
            road = math.exp(-((x - sx) / (8 + d * 50)) ** 2)
            wave = 0.06 * math.sin(x * 0.35 + y * 1.3) * (1 if (y % 3) else 0)
            cv.ramp(x, y, sea, 0.55 - d * 0.5 + road * 0.55 + wave)
    # 大陸の町の灯り（旅してきた町々。小さな橙の点と、そのにじみ）
    for (x, y) in [(176, 134), (214, 133), (252, 135), (300, 131), (338, 134), (372, 132)]:
        cv.put(x, y, "#ffd890")
        cv.put(x + 1, y, "#f0a050")
        cv.put(x, y - 1, "#f0a050")
        cv.put(x - 1, y, "#c87a70")
        cv.put(x, y + 1, "#c87a70")
    # 薄い雲のすじ（太陽側が明るい）
    for (y0, x0, x1) in [(96, 20, 150), (104, 230, 390), (118, 60, 170)]:
        for x in range(x0, x1):
            k = 1 - abs((x - x0) / (x1 - x0) * 2 - 1)
            th = 1 + int(2 * k)
            for y in range(y0, y0 + th):
                cv.put(x, y, "#f6b8a0" if x < sx + 60 else "#c8889a")
            cv.put(x, y0 + th, "#8a5a7a")
    balustrade(cv)
    cv.save("vista-summit")


def balustrade(cv):
    """手前の石の欄干（逆光: 太陽のある左の上ふちだけ明るく、手前の面は暗い）。柱は丸く、左上に照り。"""
    stone = ["#16141e", "#211d2a", "#2e2838", "#3e3648", "#5a4c5c", "#8a6e6e", "#d0a080"]
    rail_top, base = H - 46, H - 14
    # 上の手すり
    for y in range(rail_top, rail_top + 8):
        for x in range(W):
            v = 0.95 if y == rail_top else (0.62 if y == rail_top + 1 else 0.36 - (y - rail_top) * 0.02)
            cv.ramp(x, y, stone, v + 0.03 * math.sin(x * 0.5))
    cv_y = rail_top + 8
    for x in range(W):
        cv.put(x, cv_y, stone[0])  # 手すりの下の影
    # 柱（丸い形: 左から光が回りこむ）
    for px in range(14, W, 32):
        for y in range(cv_y + 1, base):
            # ふくらみ（壺の形）
            t = (y - cv_y) / (base - cv_y)
            w = 5 + 3 * math.sin(t * math.pi) - (1.5 if 0.1 < t < 0.2 else 0)
            for x in range(int(px - w), int(px + w) + 1):
                u = (x - px) / w  # -1（左）〜 1（右）
                v = 0.55 - u * 0.25 - abs(u) ** 3 * 0.25
                if u < -0.85:
                    v = 0.9  # 左ふちの照り
                cv.ramp(x, y, stone, v)
    # 台座（上の面だけ明るい）と、床
    for y in range(base, H):
        for x in range(W):
            v = 0.82 if y == base else 0.3 - (y - base) * 0.015
            cv.ramp(x, y, stone, v + 0.02 * math.sin(x * 0.8))


if __name__ == "__main__":
    vista_clouds()
    vista_summit()
