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


def vista_clouds():
    """風の回廊の窓から見る、雷雲の下の嵐（2026-10-07、人間の指示「外から見えるのは嵐の様子だね。雲の下の」「滝も見えるよね」「雷雲の下だよ」）。
    塔は、海が陥没した大穴の中に立ち、まわりは輪のような大滝（`world-map.ts` の大滝）。
      上: 低くたれこめる雷雲の底。下面のもこもこが、稲妻の光で下から照らされる（光は稲妻の側）
      まん中: 荒れる海と、陥没のふちから流れ落ちる大滝の白いカーテン（向こう岸の弧）
      下: 滝の落ちる穴の底からわき上がる、しぶきと霧
      全体: 稲妻（雷雲から海・滝へ）と、ななめの雨のすじ"""
    cv = Canvas()
    # 空気（雷雲の下の、暗い灰青）
    air = ["#141824", "#1c2230", "#262e3e", "#323c4e", "#424e62"]
    for y in range(H):
        for x in range(W):
            cv.ramp(x, y, air, 0.15 + 0.35 * (y / H) + 0.45 * math.exp(-((y - 88) / 10) ** 2))   # 地平のあたりは、雲の切れ間の光で少し明るい
    cloud = thunder_ceiling(cv)
    # 向こうの荒れた海（地平の少し下まで）
    horizon = 92
    sea = ["#0e1a22", "#14242e", "#1c3240", "#284454", "#3a5a6a", "#5a7c8a"]
    for y in range(horizon, 128):
        for x in range(W):
            d = (y - horizon) / 36
            wave = 0.1 * math.sin(x * 0.45 + y * 1.7) + 0.06 * math.sin(x * 0.13 - y * 0.6)
            cv.ramp(x, y, sea, 0.25 + d * 0.3 + wave)
            if math.sin(x * 0.45 + y * 1.7) > 0.93 and (x * 7 + y * 3) % 5 == 0:
                cv.put(x, y, "#8aa6b2")   # 白波
    # 大滝: 向こう岸の陥没のふち（ゆるい弧）から、海が白いカーテンになって落ちる
    def rim_y(x):
        return 108 + 22 * ((x - 200) / 230) ** 2   # 向こう岸のふち（まん中が奥で高く、両はしは手前に回りこんで低い）
    fall = ["#1e2c36", "#2c3e4a", "#3e5664", "#587482", "#7e9aa6", "#b4c8d0", "#e8f2f4"]
    srnd = random.Random(29)
    raw = [srnd.random() for _ in range(W + 4)]
    strands = [(raw[i] + raw[i + 1] * 2 + raw[i + 2]) / 4 for i in range(W)]   # 列ごとの水の量（となりとなじませる）
    for x in range(W):
        top = int(rim_y(x))
        cv.put(x, top - 1, "#cfe2e8")   # ふちで盛り上がる水の光
        cv.put(x, top, "#ffffff")
        length = H - top
        strand = strands[x]   # 水のすじの濃い・うすい
        for y in range(top + 1, H):
            t = (y - top) / length
            v = 0.62 - t * 0.42 + (strand - 0.5) * 0.45
            if t < 0.08:
                v += 0.18   # 落ちはじめは、白く泡立つ
            if (x * 5 + y * 3 + int(strand * 40)) % 17 == 0 and t < 0.6:
                v += 0.15   # 落ちる水のつぶ
            cv.ramp(x, y, fall, v)
    # 滝つぼからわき上がる、しぶきと霧（下の帯。もこもこの霧のかたまり）
    mist = ["#3e4c58", "#56646e", "#717e88", "#919ca4", "#b6c0c6", "#d4dade"]
    plume = noise(19)
    for y in range(140, H):
        for x in range(W):
            # 下ほど濃く、上へ向かって、ゆらぐ柱のように立ちのぼる
            rise = (y - 140) / (H - 140)
            col = 0.5 + 0.5 * math.sin(x * 0.09 + 1.3) * math.sin(x * 0.031)
            v = rise * 1.4 + col * 0.3 + plume(x, y) * 0.45 - 0.5
            if v > 0.02:
                cv.ramp(x, y, mist, min(0.95, 0.1 + v * 0.75))
    # 稲妻（雷雲から海と滝へ）と、まわりの照り返し
    BRIGHTEN.clear()
    BRIGHTEN.update({c: cloud[min(len(cloud) - 1, i + 2)] for i, c in enumerate(cloud)})
    BRIGHTEN.update({c: air[min(len(air) - 1, i + 2)] for i, c in enumerate(air)})
    BRIGHTEN.update({c: sea[min(len(sea) - 1, i + 2)] for i, c in enumerate(sea)})
    for (lx, ly, n, sd) in [(132, 60, 60, 1), (286, 66, 50, 2), (220, 70, 26, 3)]:
        lightning(cv, lx, ly, n, sd, lambda x, y: 0 <= x < W and 0 <= y < 140)
    # 雨のすじ（ななめ。手前ほど長い。2段の色）
    rnd = random.Random(17)
    for _ in range(420):
        x, y = rnd.randrange(W), rnd.randrange(40, H)
        n = 3 + int(y / 60)
        for k in range(n):
            xx, yy = x - k, y + k * 2
            if 0 <= xx < W and yy < H:
                cv.put(xx, yy, "#6e7c90" if k % 2 else "#4e5a6e")
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
    """頂の見晴らし（2026-10-07、人間の指示「雷雲の下だよ？で嵐滝も見える」）。塔のてっぺんも、まだ雷雲の下。
      上: 雷雲の底。その裂け目から、夜明けの空と、欠けた光の環の跡が、少しだけのぞく（裂け目のふちの雲は朝日に染まる）
      下: 高いところから見おろす、荒れる海と、塔をぐるりと囲む輪の大滝（向こう側の弧）、滝つぼのしぶき
      全体: 稲妻と雨。手前は石の欄干"""
    cv = Canvas()
    air = ["#141824", "#1c2230", "#262e3e", "#323c4e", "#424e62"]
    for y in range(H):
        for x in range(W):
            cv.ramp(x, y, air, 0.15 + 0.3 * (y / H) + 0.4 * math.exp(-((y - 84) / 9) ** 2))
    cloud = thunder_ceiling(cv, shift=4)
    # 雷雲の裂け目（夜明けの空がのぞく）
    rcx, rcy, rrx, rry = 236, 30, 84, 16
    sky = ["#1e2048", "#2c2a5c", "#46366c", "#6a4474", "#984e6e", "#c8645e", "#e8865a", "#f6b070"]
    rift_n = noise(61)
    rift = lambda x, y: ((x - rcx) / rrx) ** 2 + ((y - rcy) / rry) ** 2 + rift_n(x * 3, y * 3) * 0.9 + 0.25 * math.sin(x * 0.21) < 1.0
    for y in range(0, 60):
        for x in range(W):
            if rift(x, y):
                cv.ramp(x, y, sky, (y - (rcy - rry)) / (2 * rry) * 0.9 + 0.05)
    rnd = random.Random(9)
    for _ in range(18):
        x, y = rnd.randrange(rcx - rrx, rcx + rrx), rnd.randrange(rcy - rry, rcy)
        if rift(x, y):
            cv.put(x, y, "#e8e8ff")
    # 欠けた光の環の跡（裂け目の中だけ見える）
    for i in range(2400):
        t = math.pi + i / 2400 * math.pi
        if 4.6 < t < 4.75:
            continue
        x, y = 200 + 300 * math.cos(t), 150 + 140 * math.sin(t)
        for o, c in [(-1, "#c8c0ff"), (0, "#fff8e0"), (1, "#d8b8f0")]:
            if rift(int(x), int(y) + o):
                cv.put(int(x), int(y) + o, c)
    # 裂け目のふちの雲は、朝日に染まる（ふちから2ドット）
    edge = []
    for y in range(0, 62):
        for x in range(W):
            if not rift(x, y) and any(rift(x + dx, y + dy) for dx, dy in ((0, -1), (0, -2), (-1, 0), (1, 0))):
                edge.append((x, y))
    for (x, y) in edge:
        cv.put(x, y, "#e89a78" if rift(x, y - 1) else "#b86e6c")
    # 荒れる海（見おろす）
    horizon = 90
    sea = ["#0e1a22", "#14242e", "#1c3240", "#284454", "#3a5a6a", "#5a7c8a"]
    for y in range(horizon, H):
        for x in range(W):
            d = (y - horizon) / (H - horizon)
            wave = 0.1 * math.sin(x * 0.4 + y * 1.5) + 0.06 * math.sin(x * 0.12 - y * 0.5)
            cv.ramp(x, y, sea, 0.2 + d * 0.35 + wave)
            if math.sin(x * 0.4 + y * 1.5) > 0.93 and (x * 7 + y * 3) % 5 == 0:
                cv.put(x, y, "#8aa6b2")
    # 塔のまわりの陥没（だ円）と、ふちから落ちる輪の大滝
    bx, by, brx, bry = 200, 200, 240, 74
    fall = ["#1e2c36", "#2c3e4a", "#3e5664", "#587482", "#7e9aa6", "#b4c8d0", "#e8f2f4"]
    mist = ["#3e4c58", "#56646e", "#717e88", "#919ca4", "#b6c0c6", "#d4dade"]
    srnd = random.Random(31)
    raw = [srnd.random() for _ in range(W + 4)]
    strands = [(raw[i] + raw[i + 1] * 2 + raw[i + 2]) / 4 for i in range(W)]
    plume = noise(67)
    for x in range(W):
        u = (x - bx) / brx
        if abs(u) >= 1:
            continue
        top = by - bry * math.sqrt(1 - u * u)   # 向こう側のふち
        cv.put(x, int(top) - 1, "#cfe2e8")
        cv.put(x, int(top), "#ffffff")
        abyss = ["#05070c", "#0a0e16", "#121822", "#1c2430"]
        for y in range(int(top) + 1, H):
            t = (y - top) / 34
            if t < 1:
                v = 0.62 - t * 0.42 + (strands[x] - 0.5) * 0.45
                if t < 0.08:
                    v += 0.18
                cv.ramp(x, y, fall, v)
            else:
                cv.ramp(x, y, abyss, 0.6 - (t - 1) * 0.5)   # 穴の深み（下ほど暗い）
            # 滝の足もとから立ちのぼる、しぶき（滝のすぐ下の帯だけ）
            m = 1 - abs(t - 1.0) * 2.2 + plume(x, y) * 0.5 + 0.15 * math.sin(x * 0.09) - 0.35
            if m > 0.05:
                cv.ramp(x, y, mist, min(0.9, 0.05 + m * 0.7))
    # 稲妻（雷雲から海・滝へ）
    BRIGHTEN.clear()
    BRIGHTEN.update({c: cloud[min(len(cloud) - 1, i + 2)] for i, c in enumerate(cloud)})
    BRIGHTEN.update({c: air[min(len(air) - 1, i + 2)] for i, c in enumerate(air)})
    BRIGHTEN.update({c: sea[min(len(sea) - 1, i + 2)] for i, c in enumerate(sea)})
    for (lx, ly, n, sd) in [(96, 62, 64, 4), (318, 66, 56, 5)]:
        lightning(cv, lx, ly, n, sd, lambda x, y: 0 <= x < W and 0 <= y < 150)
    # 雨
    rnd = random.Random(19)
    for _ in range(380):
        x, y = rnd.randrange(W), rnd.randrange(50, H)
        for k in range(3 + int(y / 70)):
            xx, yy = x - k, y + k * 2
            if 0 <= xx < W and yy < H:
                cv.put(xx, yy, "#6e7c90" if k % 2 else "#4e5a6e")
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
