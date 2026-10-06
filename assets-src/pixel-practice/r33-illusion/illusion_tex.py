"""幻想の禁域（まぼろしの回廊）の地面の模様（2026-10-06、人間の指示「禁域幻想空間的なダンジョンも追加しよう。作るときドット絵にこだわりを持ってね」）。
128×128（ゲームのマス 16×16 が 8×8 ならぶ大きさ）。上下左右がつながる（はしで切れ目が出ない）ように、模様は 128 で割り切れる周期で作る。

  illusion-void.txt    虚空: 星の海に、うすい星雲。ところどころ明るい星に十字の光
  illusion-floor.txt   床: 星の海に浮かぶ水晶の板（1マスに1枚）。板と板のすきまから虚空がのぞく
  illusion-wall.txt    壁: 縦にのびる水晶の柱の束（面の向きで明るさを変える）
  illusion-rune.txt    光の道: 水晶の板に、光るルーンの円
  illusion-hidden.txt  見えない道: 虚空に見えるが、板のかどに、かすかな星がならぶ（謎解き用。歩ける）

ドット絵の決まり（CLAUDE.md）: 光は左上。板は面取り（左上のふちが明るく、右下のふちが暗い）、板の下に虚空への影。
水晶は、面の向きで明るさを変え、稜線に光の線。市松（ディザ）は、となりあう2つの色の段のあいだだけ（4×4のベイヤー）。"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
N = 128
T = 16
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
SYMS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class Tex:
    def __init__(self):
        self.px = [["#000000"] * N for _ in range(N)]

    def put(self, x, y, c):
        self.px[y % N][x % N] = c

    def get(self, x, y):
        return self.px[y % N][x % N]

    def ramp(self, x, y, ramp, v):
        v = min(max(v, 0.0), 0.9999) * (len(ramp) - 1)
        i = int(v)
        f = v - i
        t = (BAYER[y & 3][x & 3] + 0.5) / 16
        self.put(x, y, ramp[min(i + (1 if f > t else 0), len(ramp) - 1)])

    def save(self, name):
        used = sorted({c for row in self.px for c in row})
        sym = {c: SYMS[i] for i, c in enumerate(used)}
        open(os.path.join(HERE, f"{name}.txt"), "w").write("\n".join("".join(sym[c] for c in row) for row in self.px) + "\n")
        json.dump({sym[c]: c for c in used}, open(os.path.join(HERE, f"{name}-pal.json"), "w"))
        try:
            from PIL import Image
            im = Image.new("RGB", (N, N))
            im.putdata([tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for row in self.px for c in row])
            im.save(os.path.join(HERE, f"{name}.png"))
            # 3×3にならべた見本（つなぎ目が見えないか確かめる）
            big = Image.new("RGB", (N * 3, N * 3))
            for i in range(3):
                for j in range(3):
                    big.paste(im, (i * N, j * N))
            big.resize((N * 6, N * 6), Image.NEAREST).save(os.path.join(HERE, f"{name}-tiled.png"))
        except ImportError:
            pass
        print(name, len(used), "colors")


def periodic(seed, terms=5):
    """128 で割り切れる周期の波を重ねた、つながる雲模様（0〜1）。"""
    rnd = random.Random(seed)
    waves = [(rnd.choice([1, 2, 3, 4]), rnd.choice([1, 2, 3, 4]), rnd.random() * 6.28, rnd.uniform(0.5, 1)) for _ in range(terms)]

    def f(x, y):
        s = sum(a * math.sin(2 * math.pi * (kx * x + ky * y) / N + p) for kx, ky, p, a in waves)
        tot = sum(a for *_, a in waves)
        return 0.5 + 0.5 * s / tot

    return f


VOID = ["#05051a", "#0b0a26", "#151238", "#211a4c", "#2f2262", "#433078"]
STAR = ["#4a4a8a", "#8a8ad0", "#d8d8ff", "#ffffff"]


def paint_void(t, seed=1, faint=False):
    neb = periodic(seed)
    neb2 = periodic(seed + 7, 4)
    for y in range(N):
        for x in range(N):
            v = 0.12 + 0.55 * neb(x, y) ** 2 + 0.25 * neb2(x, y) ** 3
            t.ramp(x, y, VOID, v * (0.7 if faint else 1))
    rnd = random.Random(seed * 13)
    for _ in range(90):
        x, y = rnd.randrange(N), rnd.randrange(N)
        t.put(x, y, STAR[rnd.choice([0, 0, 0, 1, 1, 2])])
    for _ in range(7):
        x, y = rnd.randrange(N), rnd.randrange(N)
        t.put(x, y, STAR[3])
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            t.put(x + dx, y + dy, STAR[1])


SLAB = ["#26285a", "#343a7a", "#46509a", "#5e6cba", "#8494d6", "#b8c8f0", "#eef4ff"]
GLOW = ["#2a6a90", "#40a8c8", "#70e0f0", "#c8fcff"]


def slab(t, ox, oy, rnd, rune=None):
    """1マス（16×16）の水晶の板。まわり1ドットは虚空（板が浮いて見える）。上の面（13×11）と、手前の厚みの面（2ドット）。
    上の面は左上が明るく、左上にひし形の照り（水晶の中の面）。右と下のふちは暗く、厚みの面の下に、虚空へ落ちるうすい影。"""
    tone = rnd.uniform(-0.05, 0.05)
    top_y0, top_y1 = 1, 11   # 上の面
    for y in range(1, T - 1):
        for x in range(1, T - 1):
            gx, gy = ox + x, oy + y
            if y <= top_y1:
                v = 0.6 + tone - (x + y) / (2 * T) * 0.25
                # 左上のひし形の照り（水晶の中の面）
                if abs(x - 5) + abs(y - 4) <= 3:
                    v += 0.13
                if abs(x - 5) + abs(y - 4) == 3 and x <= 5:
                    v += 0.08
                # 右下の深い面（ひし形の反対側）
                if abs(x - 10) + abs(y - 8) <= 2:
                    v -= 0.08
                if y == top_y0 or x == 1:
                    v = 0.9            # 上・左のふち（光）
                if x == T - 2:
                    v = 0.3 + tone     # 右のふち（影）
                if y == top_y1:
                    v = 0.78           # 上の面と厚みの面のさかい（光の線）
            else:
                # 手前の厚みの面（暗め。左ほど少し明るい）
                v = 0.32 + tone - x / T * 0.12 - (y - top_y1 - 1) * 0.08
            t.ramp(gx, gy, SLAB, v)
    # 板の下の虚空に、うすい影（虚空の色を一段暗く）
    for x in range(2, T):
        c = t.get(ox + x, oy + T - 1)
        if c in VOID[1:]:
            t.put(ox + x, oy + T - 1, VOID[VOID.index(c) - 1])
    # ときどき、ひびと、そこからもれる光
    if rnd.random() < 0.25 and rune is None:
        x, y = rnd.randrange(6, 11), rnd.randrange(5, 9)
        for k in range(rnd.randrange(3, 5)):
            t.put(ox + x, oy + y, GLOW[1] if k % 2 else SLAB[1])
            x += rnd.choice([1, 1, 0])
            y += rnd.choice([0, 1])
    # 光の粒（ひし形の照りの中）
    if rnd.random() < 0.6:
        t.put(ox + 4, oy + 3, SLAB[6])
    if rune is not None:
        draw_rune(t, ox, oy, rune)


def draw_rune(t, ox, oy, kind):
    """板の中心に、光るルーンの円と、まん中の印（種類ごとに形をかえる）。"""
    cx, cy, r = ox + 7.5, oy + 6.0, 4.4
    for a in range(64):
        th = a / 64 * 2 * math.pi
        x, y = cx + r * math.cos(th), cy + r * math.sin(th)
        t.put(int(round(x)), int(round(y)), GLOW[2] if math.cos(th + 2.3) > 0 else GLOW[1])
    marks = [
        [(0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (-1, 0), (1, 0)],
        [(-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2), (2, -2), (1, -1), (-1, 1), (-2, 2)],
        [(-1, -2), (0, -2), (1, -2), (0, -1), (0, 0), (0, 1), (-1, 2), (0, 2), (1, 2)],
        [(0, -2), (-1, -1), (1, -1), (-2, 0), (2, 0), (-1, 1), (1, 1), (0, 2)],
    ][kind % 4]
    for dx, dy in marks:
        t.put(int(cx + 0.5) + dx, int(cy + 0.5) + dy, GLOW[3])
    # 円のまわりに、ほのかな光（板の色を一段明るく）
    for y in range(oy + 1, oy + 11):
        for x in range(ox + 2, ox + T - 2):
            d = math.hypot(x - cx, y - cy)
            if 4.9 < d < 5.8 and t.get(x, y) in SLAB[:4]:
                t.put(x, y, SLAB[SLAB.index(t.get(x, y)) + 1])


def floor(rune=False, name="illusion-floor"):
    t = Tex()
    paint_void(t, seed=3)
    rnd = random.Random(21 if not rune else 34)
    for ty in range(N // T):
        for tx in range(N // T):
            slab(t, tx * T, ty * T, rnd, rune=(tx + ty * 3) if rune else None)
    t.save(name)


CRYS = ["#140f2e", "#1e1642", "#2c2160", "#40318a", "#5c48b0", "#8270d4", "#b4a6f0", "#ece6ff"]


def wall():
    """水晶の柱の束（六角の柱を横から見た形）。柱ごとに、光の面（左）・正面（中）・影の面（右）の3つに分け、
    面と面のさかいの稜線に光の線。柱と柱のすきまは奥の暗がり。縦につながるよう、柱は上下にのび、ところどころ成長のすじ。"""
    t = Tex()
    rnd = random.Random(8)
    widths = []
    while sum(widths) < N:
        widths.append(rnd.choice([10, 12, 13, 14, 16]))
    widths[-1] -= sum(widths) - N
    x0 = 0
    for w in widths:
        tone = rnd.uniform(-0.05, 0.05)
        a, b = x0 + max(2, w // 4), x0 + w - max(2, w // 4)   # 光の面 | 正面 | 影の面
        seam = rnd.randrange(N)
        for y in range(N):
            for x in range(x0, x0 + w):
                if x == x0:
                    v = 0.05  # すきま
                elif x < a:
                    v = 0.78 + tone
                elif x < b:
                    v = 0.55 + tone - (x - a) / max(1, b - a) * 0.1
                else:
                    v = 0.3 + tone
                if x == a or x == b:
                    v = 0.92 if x == a else 0.45  # 稜線（光の側は明るい線、影の側はひかえめ）
                ys = (y - seam) % 32
                if ys == 0 and x != x0:
                    v -= 0.22   # 成長のすじ（細い暗い線）
                elif ys == 1 and x != x0:
                    v += 0.1    # すじの下の照り返し
                t.ramp(x, y, CRYS, v)
        x0 += w
    # 中にとじこめた光の粒（正面の中だけ）
    for _ in range(26):
        x, y = rnd.randrange(N), rnd.randrange(N)
        if t.get(x, y) in CRYS[3:6]:
            t.put(x, y, CRYS[7] if rnd.random() < 0.3 else CRYS[6])
    t.save("illusion-wall")


def hidden():
    """見えない道: 虚空と同じに見えるが、マスのかど（16ドットおき）に、かすかな星が規則正しくならぶ。"""
    t = Tex()
    paint_void(t, seed=3)
    for ty in range(0, N, T):
        for tx in range(0, N, T):
            for (dx, dy) in ((2, 2), (13, 2), (2, 13), (13, 13)):
                t.put(tx + dx, ty + dy, STAR[1])
    t.save("illusion-hidden")


def void_only():
    t = Tex()
    paint_void(t, seed=3)
    t.save("illusion-void")


if __name__ == "__main__":
    void_only()
    floor()
    floor(rune=True, name="illusion-rune")
    wall()
    hidden()
