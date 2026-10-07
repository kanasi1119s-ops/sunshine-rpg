"""芯環塔から外を見る景色（2026-10-06、人間の指示「塔から外が見れる場所とかもほしいかも。それを塔の中のイベントに入れて」）。
400×225（ゲームの画面いっぱい）。イベントの会話のうしろに出す。

  vista-clouds.txt  風の回廊: 石のアーチ窓から見る、雷雲の下の嵐（雷雲の底・稲妻・雨・荒れる海と、陥没のふちから落ちる輪の大滝・しぶき）
  vista-summit.txt  頂の見晴らし: てっぺんもまだ雷雲の下。雷雲の裂け目から夜明けの空と欠けた光の環の跡がのぞき、
                    見おろすと、荒れる海と塔をぐるりと囲む輪の大滝・しぶき、稲妻と雨
  （2026-10-07、人間の指示「外から見えるのは嵐の様子だね。雲の下の」で、晴れた雲海・静かな海から、嵐の景色に描きかえた）

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
BRIGHTEN: dict = {}


def lightning(cv, x0, y0, length, seed, inside=lambda x, y: True):
    """稲妻: 芯は白、まわり1ドットに青白い光。ジグザグに下へのび、ときどき枝わかれ。まわりの雲を少し明るく照らす。"""
    rnd = random.Random(seed)
    pts = []

    def walk(x, y, n, depth):
        for _ in range(n):
            pts.append((x, y))
            x += rnd.choice([-1, -1, 0, 1, 1]) + (rnd.random() - 0.5) * 0.6
            y += 1
            if depth < 2 and rnd.random() < 0.06:
                walk(x, y, n // 3, depth + 1)

    walk(x0, y0, length, 0)
    # まわりの雲の照り返し: 稲妻から3ドット以内を、1段明るく（2ドットより外は市松で半分だけ）
    lit = set()
    for (x, y) in pts:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                d = abs(dx) + abs(dy)
                gx, gy = int(x) + dx, int(y) + dy
                if d <= 3 and (gx, gy) not in lit and inside(gx, gy) and 0 <= gx < W and 0 <= gy < H:
                    if d <= 2 or (gx + gy) % 2 == 0:
                        lit.add((gx, gy))
    for (gx, gy) in lit:
        c = cv.px[gy][gx]
        if c in BRIGHTEN:
            cv.put(gx, gy, BRIGHTEN[c])
    for (x, y) in pts:
        if not inside(int(x), int(y)):
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if inside(int(x) + dx, int(y) + dy):
                cv.put(int(x) + dx, int(y) + dy, "#a8b8f0")
    for (x, y) in pts:
        if inside(int(x), int(y)):
            cv.put(int(x), int(y), "#ffffff")
    return pts


def thunder_ceiling(cv, shift=0):
    """雷雲の底（画面の上の4割）。下面のこぶは、下（稲妻・海の照り返し）側がわずかに明るく、こぶとこぶの重なりの奥は暗い。"""
    cloud = ["#0c0e16", "#141826", "#1c2232", "#262e42", "#343e54", "#4a5670", "#6a7690", "#9aa4bc"]
    for y in range(0, 70 + shift):
        for x in range(W):
            cv.ramp(x, y, cloud, 0.18 + 0.1 * math.sin(x * 0.05 + y * 0.09))
    rnd = random.Random(5)
    for row, (yb, rmin, rmax) in enumerate([(30 + shift, 10, 18), (48 + shift, 12, 22), (64 + shift, 14, 26)]):
        x = -20 + rnd.uniform(0, 10)
        while x < W + 20:
            r = rnd.uniform(rmin, rmax)
            px, py = x, yb + rnd.uniform(-4, 4)
            for y in range(int(py - r), int(py + r * 0.9)):
                for xx in range(int(px - r), int(px + r)):
                    ddx, ddy = (xx - px) / r, (y - py) / (r * 0.9)
                    d2 = ddx * ddx + ddy * ddy
                    if d2 > 1 or not (0 <= y < H and 0 <= xx < W):
                        continue
                    nz = math.sqrt(1 - d2)
                    lam = max(0.0, 0.85 * ddy + 0.1 * ddx + 0.4 * nz)   # 下からの光
                    v = 0.14 + lam * 0.38 + row * 0.04
                    if d2 > 0.84 and ddy > 0.35:
                        v = 0.6 + row * 0.04   # 下ふち（照り返しの線）
                    cv.ramp(xx, y, cloud, v)
            x += r * rnd.uniform(1.1, 1.6)
    return cloud


# ───── フィールドの大滝・雷雲と同じ色・描き方（2026-10-07、人間の指示「実際のフィールドの滝雷雲のドットに近づけて」）─────
FIELD = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
# 大滝の色（assets-src/pixel-practice/r29-falls/falls.py と同じ）
FA, FB, FC, FD, FE, FF, FG = "#163a66", "#245a92", "#3a7cb8", "#62a2d8", "#9cccf0", "#d4ecfc", "#ffffff"
MIST_L, MIST_D = "#b8c8dc", "#8494ae"
ABYSS = ["#08090f", "#10131e", "#1a2032", "#28304a"]
SEA = ["#14345c", "#1e4a7c", "#2c64a0", "#46849e"]
BOLT_CORE, BOLT_GLOW, BOLT_EDGE = "#ffffff", "#8cc4ff", "#4a78c8"
RAIN = ["#cad8e6", "#8898b0"]


def field_cloud(colors=30):
    """フィールドの雷雲の絵（src/assets/falls/cloud.png の1コマ目、440×256）を、色数をへらして読みこむ。"""
    from PIL import Image
    im = Image.open(os.path.join(FIELD, "cloud.png")).convert("RGBA").crop((0, 0, 440, 256))
    alpha = im.getchannel("A")
    q = im.convert("RGB").quantize(colors=colors, dither=Image.Dither.NONE).convert("RGB")
    px = []
    for y in range(256):
        row = []
        for x in range(440):
            if alpha.getpixel((x, y)) < 128:
                row.append(None)
            else:
                r, g, b = q.getpixel((x, y))
                row.append("#%02x%02x%02x" % (r, g, b))
        px.append(row)
    return px


def stamp_cloud(cv, sprite, ox, oy, flip=False):
    for y, row in enumerate(sprite):
        for x, c in enumerate(row):
            xx = (439 - x if flip else x) + ox
            if c and 0 <= xx < W and 0 <= y + oy < H:
                cv.put(xx, y + oy, c)


def field_ceiling(cv, bottom=100, colors=30):
    """雷雲の天井: フィールドの雷雲の絵を2つ（1つは左右反転）ならべ、雲の底（紺の帯・中で光る金色）が bottom の高さに来るようにする。"""
    sprite = field_cloud(colors)
    for y in range(0, bottom - 40):
        for x in range(W):
            cv.ramp(x, y, ["#3a3842", "#48464e", "#5a5860"], 0.3 + 0.4 * math.sin(x * 0.05 + y * 0.11) ** 2)
    oy = bottom - 246
    stamp_cloud(cv, sprite, -70, oy - 30, flip=True)
    stamp_cloud(cv, sprite, 150, oy - 18)
    stamp_cloud(cv, sprite, -230, oy + 6)
    stamp_cloud(cv, sprite, 260, oy + 2, flip=True)


def field_bolt(cv, x0, y0, length, seed, inside=lambda x, y: True):
    """フィールドの稲妻と同じ: 1ドットの白い芯、青白い光、ふちに青。細くジグザグ。"""
    rnd = random.Random(seed)
    x, pts = float(x0), []
    for i in range(length):
        pts.append((int(x), y0 + i))
        if i % 3 == 0:
            x += rnd.choice([-2, -1, 1, 2])
        if rnd.random() < 0.05:
            bx = x
            for k in range(rnd.randrange(5, 10)):
                bx += rnd.choice([-1, 1, 2]) * (1 if rnd.random() < 0.5 else -1)
                pts.append((int(bx), y0 + i + k))
    for (px_, py) in pts:
        for dx in (-1, 1):
            if inside(px_ + dx, py):
                cv.put(px_ + dx, py, BOLT_GLOW)
    for (px_, py) in pts:
        if inside(px_, py):
            cv.put(px_, py, BOLT_CORE)


def field_falls(cv, rim, bottom_of, inside_x=lambda x: True, seed=3):
    """フィールドの大滝と同じ描き方: 水の帯（帯ごとに明るさがちがい、帯の境は暗い）・帯の上を流れる白いすじ・
    落ち口の白い泡・足もとの水しぶきと霧。rim(x)=落ち口の高さ、bottom_of(x)=滝の下の高さ。"""
    ribbons = [(2, FB), (3, FC), (2, FD), (3, FE), (2, FD), (2, FC), (2, FB)]
    seq = []
    for w_, c in ribbons:
        seq += [c] * w_
        seq.append(FA)
    rnd = random.Random(seed)
    for x in range(W):
        if not inside_x(x):
            continue
        top, bot = int(rim(x)), int(bottom_of(x))
        col = seq[x % len(seq)]
        for y in range(top, bot):
            c = col
            if (y * 7 + x * 13 + seed) % 23 < 3 and col != FA:
                c = FG if col in (FE, FD) else FF   # 下へ流れる白いすじ
            cv.put(x, y, c)
        # 落ち口の泡（上の2〜3ドット）と、ふちの水の光
        cv.put(x, top - 1, FE)
        cv.put(x, top, FG)
        cv.put(x, top + 1, FF if x % 3 else FG)
        if x % 2 == 0:
            cv.put(x, top + 2, FF)
        # 足もとの水しぶき・霧（もこもこのかたまり。フィールドと同じ明暗2色と白）
        for k in range(rnd.randrange(3, 7)):
            yy = bot - rnd.randrange(0, 9)
            cv.put(x, yy, [MIST_L, MIST_D, FF, MIST_L][k % 4])


def field_rain(cv, n, y0, seed):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.randrange(W), rnd.randrange(y0, H)
        cv.put(x, y, RAIN[0])
        cv.put(x - 1, y + 1, RAIN[0])
        cv.put(x - 1, y + 2, RAIN[1])


def vista_clouds():
    """風の回廊の窓から見る、雷雲の下の嵐（人間の指示「外から見えるのは嵐の様子だね。雲の下の」「滝も見えるよね」「雷雲の下だよ」
    「実際のフィールドの滝雷雲のドットに近づけて」）。雷雲はフィールドの雷雲の絵そのもの、滝・稲妻・雨はフィールドと同じ色と描き方。
      上: 雷雲の底（紺の帯と、中で光る金色）
      まん中: 荒れる紺の海と、陥没のふちから落ちる輪の大滝（向こう岸の弧）
      下: 滝つぼの暗い穴と、白い水しぶき"""
    cv = Canvas()
    for y in range(H):
        for x in range(W):
            cv.ramp(x, y, ABYSS, 0.35 + 0.3 * math.exp(-((y - 96) / 12) ** 2))
    # 荒れる海（地平から落ち口まで）
    for y in range(92, 132):
        for x in range(W):
            wave = 0.12 * math.sin(x * 0.45 + y * 1.7) + 0.06 * math.sin(x * 0.13 - y * 0.6)
            cv.ramp(x, y, SEA, 0.2 + (y - 92) / 40 * 0.5 + wave)
            if math.sin(x * 0.45 + y * 1.7) > 0.97 and (x * 7 + y * 3) % 9 == 0:
                cv.put(x, y, FE)
    rim = lambda x: 112 + 22 * ((x - 200) / 230) ** 2
    # 穴の底（暗い紺）と、白いしぶきのかたまり
    rnd = random.Random(7)
    for x in range(W):
        for y in range(int(rim(x)), H):
            cv.ramp(x, y, ABYSS, 0.2 - (y - rim(x)) / 200)
    field_falls(cv, rim, lambda x: rim(x) + 58 + 6 * math.sin(x * 0.05))
    for _ in range(60):
        cx_, cy_, r = rnd.randrange(W), rnd.randrange(176, 200), rnd.uniform(3, 8)
        for y in range(int(cy_ - r), int(cy_ + r)):
            for x in range(int(cx_ - r), int(cx_ + r)):
                d = math.hypot(x - cx_, (y - cy_) * 1.6) / r + 0.35 * math.sin(x * 1.9 + y * 2.3 + cx_)
                if d < 1 and 0 <= x < W and 0 <= y < H:
                    cv.put(x, y, FF if d < 0.35 else (MIST_L if d < 0.7 else MIST_D))
    field_ceiling(cv, bottom=96)
    for (lx, ly, n, sd) in [(128, 70, 60, 1), (292, 74, 52, 2)]:
        field_bolt(cv, lx, ly, n, sd, lambda x, y: 0 <= x < W and 0 <= y < 150)
    field_rain(cv, 130, 40, 17)
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
    """頂の見晴らし（人間の指示「雷雲の下だよ？で嵐滝も見える」「実際のフィールドの滝雷雲のドットに近づけて」）。頂もまだ雷雲の下。
      上: フィールドの雷雲の絵。その裂け目から、夜明けの空と、欠けた光の環の跡がのぞく
      下: 見おろす紺の海と、塔をぐるりと囲む輪の大滝（フィールドと同じ描き方）、穴の底のしぶき
      全体: 稲妻と雨。手前は石の欄干"""
    cv = Canvas()
    for y in range(H):
        for x in range(W):
            cv.ramp(x, y, ABYSS, 0.35 + 0.3 * math.exp(-((y - 86) / 10) ** 2))
    for y in range(84, H):
        for x in range(W):
            wave = 0.12 * math.sin(x * 0.4 + y * 1.5) + 0.06 * math.sin(x * 0.12 - y * 0.5)
            cv.ramp(x, y, SEA, 0.15 + (y - 84) / 60 * 0.45 + wave)
            if math.sin(x * 0.4 + y * 1.5) > 0.97 and (x * 7 + y * 3) % 9 == 0:
                cv.put(x, y, FE)
    bx, by, brx, bry = 200, 206, 250, 78
    inx = lambda x: abs((x - bx) / brx) < 1
    rim = lambda x: by - bry * math.sqrt(max(0.0, 1 - ((x - bx) / brx) ** 2))
    for x in range(W):
        if inx(x):
            for y in range(int(rim(x)), H):
                cv.ramp(x, y, ABYSS, 0.25 - (y - rim(x)) / 160)
    field_falls(cv, rim, lambda x: rim(x) + 34, inx, seed=5)
    rnd = random.Random(11)
    for _ in range(40):
        cx_, cy_, r = rnd.randrange(W), rnd.randrange(170, 200), rnd.uniform(3, 7)
        for y in range(int(cy_ - r), int(cy_ + r)):
            for x in range(int(cx_ - r), int(cx_ + r)):
                d = math.hypot(x - cx_, (y - cy_) * 1.6) / r + 0.35 * math.sin(x * 1.9 + y * 2.3 + cx_)
                if d < 1 and 0 <= x < W and 0 <= y < H and inx(x) and y > rim(x) + 20:
                    cv.put(x, y, FF if d < 0.35 else (MIST_L if d < 0.7 else MIST_D))
    field_ceiling(cv, bottom=84, colors=18)   # 夜明けの空の色があるぶん、雷雲の色をへらす（エディタの色の数の上限）
    # 雷雲の裂け目（夜明けの空と、欠けた光の環の跡）
    rcx, rcy, rrx, rry = 236, 26, 80, 14
    sky = ["#1e2048", "#2c2a5c", "#46366c", "#6a4474", "#984e6e", "#c8645e", "#e8865a", "#f6b070"]
    rift_n = noise(61)
    rift = lambda x, y: ((x - rcx) / rrx) ** 2 + ((y - rcy) / rry) ** 2 + rift_n(x * 3, y * 3) * 0.9 + 0.25 * math.sin(x * 0.21) < 1.0
    for y in range(0, 50):
        for x in range(W):
            if rift(x, y):
                cv.ramp(x, y, sky, (y - (rcy - rry)) / (2 * rry) * 0.9 + 0.05)
    for i in range(2400):
        t = math.pi + i / 2400 * math.pi
        x, y = 200 + 300 * math.cos(t), 150 + 140 * math.sin(t)
        for o, c in [(-1, "#c8c0ff"), (0, "#fff8e0"), (1, "#d8b8f0")]:
            if rift(int(x), int(y) + o):
                cv.put(int(x), int(y) + o, c)
    for y in range(0, 52):
        for x in range(W):
            if not rift(x, y) and any(rift(x + dx, y + dy) for dx, dy in ((0, -1), (0, -2), (-1, 0), (1, 0))):
                cv.put(x, y, "#e8b088" if rift(x, y - 1) else "#b8806c")
    for (lx, ly, n, sd) in [(96, 66, 70, 4), (318, 70, 60, 5)]:
        field_bolt(cv, lx, ly, n, sd, lambda x, y: 0 <= x < W and 0 <= y < 160)
    field_rain(cv, 120, 40, 19)
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
