"""全体フィールドの山の「高低差」の絵（2026-10-05、人間の指示「山って高低差あるはずなんだよね。それを考えてリアルな山作ってほしいな」
「ドット絵はすべてこだわって」）。

山のマスの上に、ゲームが1マスに1つずつ「山の絵」を重ねて描く（src/render/mountain-relief.ts）。山脈のふちからの距離（＋ゆるい
ゆらぎ）で、ふもとの小山 → 中腹の山 → 高い山 → 雪をいただく峰、の4段を選び、奥の列から手前の列へ重ねる。峰の右下には影を落とす。

このスクリプトが作るもの
  - assets-src/field/relief/<名前>.txt と <名前>.json（ドット絵エディタで確かめる元の絵）、<名前>.png（確認用）
  - src/game/art/relief-sprites.generated.ts（ゲームが読みこむデータ。sprite-data.generated.ts と同じ形式）

絵の種類（どれも 72×72 の枠。山のすそのまん中が (26, 56)）
  - 3つの系統: gray（ふつうの灰色の岩山）・snow（雪の地方。雪におおわれ、岩は青みの灰）・volc（火山のまわり。暗くあたたかい岩、雪なし）
  - 4つの高さ: foot（ふもと）・slope（中腹）・high（高い山）・peak（峰。gray と snow は雪をいただく）
  - 2つの向き: l（頂が左寄り。右へ長くのびる尾根）・r（頂が右寄り）。それぞれ2つの形（a・b）
  - 影の絵（<名前>-sh）: 山の形を、光と反対の右下へ倒した形。ゲームが半透明で重ねる
  - 谷の地面（valley-<系統>、128×128、つながる）: 山と山のすき間に見える、いちばん低い所

描き方のきまり
  - 光は左上。稜線（頂からすそへの線）の左が光の面、右が影の面。光の面のふちは明るく、影の側のふちだけ暗い縁
  - 面の中のひだ（谷すじ）は、決まった本数の1ドットの線。1ドットの点はまかない
  - 雪は頂から、谷すじにそって下へのびる（下のふちはぎざぎざだが、2〜3ドットのかたまり）
使い方: python3 mountain_relief.py [リポジトリのルート]
"""
import json
import math
import os
import random
import sys

from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "..")
OUT = os.path.join(ROOT, "assets-src", "field", "relief")
TS = os.path.join(ROOT, "src", "game", "art", "relief-sprites.generated.ts")
SZ = 72
AX, AY = 26, 56                      # 山のすそのまん中

# 系統ごとの色（暗→明）: 縁・影の暗・影・光・光の明・稜線の光 / 雪の影・雪・雪の光
FAMILY = {
    "gray": dict(rock=["#2e2e3a", "#4c4c58", "#646474", "#8a8a9a", "#a8a8b8", "#c8c8d4"], snow=["#aebcd2", "#dfe7f2", "#ffffff"],
                 valley=["#3e3e4a", "#4a4a56", "#565664", "#686876"]),
    "snow": dict(rock=["#3a4a64", "#566a86", "#7088a6", "#94a8c2", "#b4c4d8", "#d0dcea"], snow=["#b8cadf", "#e6eef7", "#ffffff"],
                 valley=["#b4c6da", "#c6d6e8", "#d4e2f0", "#e8f0f8"]),
    "volc": dict(rock=["#221c1a", "#3a322e", "#4e4640", "#665c54", "#80746a", "#9a8e80"], snow=None,
                 valley=["#2a2220", "#342a26", "#3e342e", "#4a3e36"]),
}
TIERS = {   # はば（すその半はば）と高さ
    "foot": dict(hw=(9.0, 11.0), h=(8, 11)),
    "slope": dict(hw=(12.5, 14.5), h=(15, 19)),
    "high": dict(hw=(16.0, 18.0), h=(23, 28)),
    "peak": dict(hw=(19.0, 21.0), h=(31, 37)),
}


class Grid:
    def __init__(self, w=SZ, h=SZ):
        self.w, self.h = w, h
        self.c = [[None] * w for _ in range(h)]

    def put(self, x, y, col):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = col

    def get(self, x, y):
        return self.c[y][x] if 0 <= x < self.w and 0 <= y < self.h else None


def mountain(fam, tier, lean, seed):
    """山ひとつ。lean=-1 は頂が左寄り、+1 は右寄り"""
    rng = random.Random(seed)
    F = FAMILY[fam]
    R = F["rock"]
    T = TIERS[tier]
    hw = rng.uniform(*T["hw"])
    h = rng.randint(*T["h"])
    g = Grid()
    sx = AX + lean * hw * rng.uniform(0.18, 0.3)          # 頂のx
    sy = AY - h
    # 斜面の形: すそから頂へ、2つの折れ点（左と右で別々）。少しふくらんだ斜面
    def profile():
        a = rng.uniform(0.35, 0.5); b = rng.uniform(0.65, 0.8)
        return [(0.0, 0.0), (a, a * rng.uniform(1.05, 1.3)), (b, b * rng.uniform(0.95, 1.12)), (1.0, 1.0)]
    PL, PR = profile(), profile()

    def interp(P, t):
        for (a0, b0), (a1, b1) in zip(P, P[1:]):
            if a0 <= t <= a1:
                return b0 + (b1 - b0) * (t - a0) / max(1e-6, a1 - a0)
        return 1.0

    xl, xr = AX - hw, AX + hw

    def top(x):
        if x <= sx:
            t = (x - xl) / max(1e-6, sx - xl)               # 0=すそ … 1=頂
            return AY - h * interp(PL, max(0.0, t))
        t = (xr - x) / max(1e-6, xr - sx)
        return AY - h * interp(PR, max(0.0, t))
    cells = {}
    for x in range(int(math.floor(xl)), int(math.ceil(xr)) + 1):
        ty = top(x + 0.5)
        if x + 0.5 < xl or x + 0.5 > xr:
            continue
        for y in range(int(math.ceil(ty)), AY + 1):
            cells[(x, y)] = ty
    # 稜線: 頂から、すその少し右（尾根の向き）へ。ゆるく曲がる
    foot_x = AX + lean * hw * 0.35 + rng.uniform(-1.5, 1.5)
    bend = rng.uniform(-2.0, 2.0)

    def ridge(y):
        f = (y - sy) / max(1, h)
        return sx + (foot_x - sx) * f + bend * math.sin(f * math.pi)
    # 面のひだ（光の面に1〜2本、影の面に1本）: (始まりの高さの割合, 横のずれ, 向き)
    gullies = []
    for _ in range(1 if tier == "foot" else 2):
        gullies.append(("lit", rng.uniform(0.25, 0.45), rng.uniform(0.35, 0.65)))
    if tier != "foot":
        gullies.append(("shade", rng.uniform(0.2, 0.4), rng.uniform(0.3, 0.6)))
    for (x, y), ty in cells.items():
        f = (y - sy) / max(1, h)                              # 0=頂 … 1=すそ
        xm = ridge(y)
        if x + 0.5 < xm:                                      # 光の面: 上の方ほど明るい。稜線のすぐ左は稜線の光
            c = R[4] if f < 0.55 else R[3]
            if xm - (x + 0.5) < 1.2 and f < 0.9:
                c = R[5]
            if f > 0.88:
                c = R[2]                                      # すそは少し暗い
        else:                                                 # 影の面: 稜線ぎわは影、はなれると暗い影
            c = R[2] if (x + 0.5) - xm < 2.5 else R[1]
            if f > 0.85:
                c = R[1]
        g.put(x, y, c)
    # ひだ: 光の面は、稜線から左下へ下りる谷すじ（暗い1ドットの線の右に、明るい1ドット）
    for kind, f0, off in gullies:
        y0 = int(sy + f0 * h)
        if kind == "lit":
            x0 = ridge(y0) - off * (ridge(y0) - (xl + (sx - xl) * (1 - f0)))
            x, y = x0, y0
            for k in range(int(h * 0.45)):
                xi, yi = int(x), int(y)
                if (xi, yi) in cells and g.get(xi, yi) in (R[3], R[4], R[5]):
                    g.put(xi, yi, R[2])
                    if (xi + 1, yi) in cells and g.get(xi + 1, yi) in (R[3], R[4]):
                        g.put(xi + 1, yi, R[5] if k < 3 else R[4])
                x -= 0.55; y += 1
        else:                                                 # 影の面: 右下へ下りる、明るめの尾根すじ
            x0 = ridge(y0) + off * ((xr - (xr - sx) * (1 - f0)) - ridge(y0))
            x, y = x0, y0
            for k in range(int(h * 0.4)):
                xi, yi = int(x), int(y)
                if (xi, yi) in cells and g.get(xi, yi) in (R[1], R[2]):
                    g.put(xi, yi, R[2] if g.get(xi, yi) == R[1] else R[3])
                x += 0.6; y += 1
    # 雪: 峰（gray・snow）と、雪の地方の高い山。頂から下へ、谷すじにそってのびる
    snowy = F["snow"] and (tier == "peak" or (fam == "snow" and tier in ("high", "slope")))
    if snowy:
        S = F["snow"]
        depth = {"peak": 0.42, "high": 0.38, "slope": 0.3}[tier] * h
        if fam == "snow" and tier == "peak":
            depth = 0.62 * h
        for (x, y), ty in cells.items():
            # 下のふち: 3ドットはばのかたまりごとに、1〜3ドット上下（決まった並び）
            jag = [0, 2, 1, 3, 0, 1][(x // 3) % 6]
            if y - sy <= depth - jag:
                xm = ridge(y)
                if x + 0.5 < xm:
                    g.put(x, y, S[2] if (xm - (x + 0.5) < 1.2 or y - ty < 1) else S[1])
                else:
                    g.put(x, y, S[0])
    # 雪の地方: 中腹・ふもとの光の面にも、雪のかたまり（2〜4ドットの横長）を決まった間かくで
    if fam == "snow" and tier in ("foot", "slope"):
        S = F["snow"]
        for (x, y), ty in cells.items():
            if x + 0.5 < ridge(y) and y - ty < 2:
                g.put(x, y, S[1])                             # 光の面の上のふちに雪
        for k in range(3 if tier == "slope" else 2):
            yy = int(sy + h * (0.35 + 0.22 * k))
            xx = int(ridge(yy) - 3 - k * 2)
            for d in range(3):
                if (xx - d, yy) in cells:
                    g.put(xx - d, yy, S[1])
    # 縁: 影の側（右のふち）だけ、いちばん暗い色。光の側のふちは、明るいまま
    for (x, y), ty in list(cells.items()):
        if (x + 1, y) not in cells and x + 0.5 >= ridge(y) - 0.5 and y > sy + 1:
            g.put(x, y, R[0])
    # すその1行: 地面にとける（右半分だけ、影の暗）
    for x in range(int(xl), int(xr) + 1):
        if (x, AY) in cells and x + 0.5 > ridge(AY):
            g.put(x, AY, R[1])
    g.put(sx, sy, R[5] if not snowy else F["snow"][2])
    return g, cells


def shadow_of(cells, g):
    """影: 山の各列の高さを、光と反対の右下へ倒した形（右へ 0.55、下へ 0.22 の割合）。山そのものの所はのぞく。
    列ごとに、すそから倒した先までの線を引き、行ごとのすき間をうめる"""
    sh = Grid()
    tops = {}
    for (x, y) in cells:
        tops[x] = min(tops.get(x, AY), y)
    for x, ty in tops.items():
        hgt = AY - ty
        steps = max(1, int(hgt * 0.6))
        for k in range(steps + 1):
            f = k / steps
            sh.put(x + hgt * 0.55 * f, AY + hgt * 0.22 * f, "#101828")
    for y in range(SZ):
        row = [x for x in range(SZ) if sh.get(x, y)]
        if row:
            for x in range(min(row), max(row) + 1):
                sh.put(x, y, "#101828")
    for (x, y) in cells:
        sh.c[y][x] = None
    return sh


def valley(fam):
    """谷の地面（128×128・つながる）: 地の色に、3〜5ドットの暗いくぼみと、2ドットの明るい小石（右下に影）"""
    V = FAMILY[fam]["valley"]
    rng = random.Random({"gray": 61, "snow": 62, "volc": 63}[fam])
    g = Grid(128, 128)
    for y in range(128):
        for x in range(128):
            g.c[y][x] = V[1]
    for _ in range(70):                                       # くぼみ（横長の楕円、暗い）
        cx, cy = rng.randrange(128), rng.randrange(128)
        w, hh = rng.uniform(2.5, 4.5), rng.uniform(1.2, 2.0)
        for yy in range(-2, 3):
            for xx in range(-5, 6):
                if (xx / w) ** 2 + (yy / hh) ** 2 <= 1:
                    g.c[(cy + yy) % 128][(cx + xx) % 128] = V[0]
    for _ in range(60):                                       # 小石（上が明るく、右下に影）
        x, y = rng.randrange(128), rng.randrange(128)
        g.c[y][x] = V[3]; g.c[y][(x + 1) % 128] = V[2]
        g.c[(y + 1) % 128][x] = V[2]; g.c[(y + 1) % 128][(x + 1) % 128] = V[0]
    return g


LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def save(g, name, store):
    cols = sorted({v for r in g.c for v in r if v})
    pal = {LET[i]: c for i, c in enumerate(cols)}
    inv = {c: k for k, c in pal.items()}
    rows = ["".join(inv[v] if v else "." for v in r) for r in g.c]
    open(os.path.join(OUT, f"{name}.txt"), "w").write("\n".join(rows) + "\n")
    json.dump(pal, open(os.path.join(OUT, f"{name}.json"), "w"))
    im = Image.new("RGBA", (g.w, g.h))
    for y, r in enumerate(g.c):
        for x, v in enumerate(r):
            if v:
                im.putpixel((x, y), tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(os.path.join(OUT, f"{name}.png"))
    # ゲーム用（sprite.ts の RLE: 色番号 A〜Z、透明は _、続く個数は36進の小文字）
    flat = [inv[v] if v else "_" for r in g.c for v in r]
    s, prev, n = "", None, 0
    for ch in flat + [None]:
        if ch == prev:
            n += 1
            continue
        if prev is not None:
            s += prev + (base36(n) if n > 1 else "")
        prev, n = ch, 1
    store[f"relief:{name}"] = dict(size=g.w, palette=cols, rle=s)


def base36(n):
    d = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while n:
        out = d[n % 36] + out
        n //= 36
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    store = {}
    names = []
    for fam in FAMILY:
        for tier in TIERS:
            for lean, ln in ((-1, "l"), (1, "r")):
                for vi, v in enumerate("ab"):
                    name = f"{fam}-{tier}-{ln}{v}"
                    seed = (list(FAMILY).index(fam) * 100 + list(TIERS).index(tier) * 10 + (0 if ln == "l" else 5) + vi) * 7919 + 13
                    g, cells = mountain(fam, tier, lean, seed)
                    save(g, name, store)
                    save(shadow_of(cells, g), name + "-sh", store)
                    names.append(name)
        save(valley(fam), f"valley-{fam}", store)
    body = "\n".join(f'  {json.dumps(k)}: {{ size: {v["size"]}, palette: {json.dumps(v["palette"])}, rle: {json.dumps(v["rle"])} }},' for k, v in store.items())
    open(TS, "w").write(
        "// 自動生成: tools/pixel-art/ai-gen/mountain_relief.py（手で編集しない）。全体フィールドの山の高低差の絵（src/render/mountain-relief.ts が使う）。\n"
        'import type { SpriteData } from "./sprite";\n\n'
        "export const RELIEF_SPRITES: Record<string, SpriteData> = {\n" + body + "\n};\n")
    print(len(store), "点")


if __name__ == "__main__":
    main()
