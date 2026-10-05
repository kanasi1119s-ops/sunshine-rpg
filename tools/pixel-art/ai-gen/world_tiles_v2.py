"""全体フィールドの地形テクスチャ・描きなおし（2026-10-05、人間の指示「フィールドの1マスのドット絵もこだわりを持って、違和感がなくなるように作って」
「ドット絵はすべてこだわって」）。

world_tiles.py の TEXTURES のうち、山（w-mountain）・とがった山（w-pyramids）・丘（w-hills）・雪の森（w-snowforest）・道（w-road）・
荒れ地（w-waste）・灰の大地（w-ash）・谷（w-chasm）を、この描き方に置きかえる（world_tiles.py の最後で読みこむ）。
草・海・砂・雪・森・湖・雲・溶岩は、前のまま（粒の大きさの基準）。

描き方のきまり（どの地形も同じ）
  - 光は左上。上・左を向いた面が明るく、右・下を向いた面が暗い
  - 粒の大きさは草・海と同じ（2〜6ドットのかたまり）。1ドットだけの点はまかない
  - 縁どりは「影の側（右・下）だけ、その素材のいちばん暗い色」。光の側には黒い線を引かない
  - 同じ形のはんこを並べない: ひとつずつ大きさ・頂の位置・稜線の折れを変える
  - 128×128 で上下左右がつながる（描くときは座標を 128 で割ったあまりにする。距離も、つながった輪の上で測る）
  - 山（M）は、とがった山（N）と、となりあってつながる（同じ描き方、同じ光）。N は M より背が高く、色は暗くあたたかい（火山の本体にも使うので雪はない）
"""
import math
import random

from world_tiles import S, Tex, lattice, grass, snow

# ===================================================================== 共通
def torus_d(ax, ay, bx, by):
    dx = abs(ax - bx); dy = abs(ay - by)
    return math.hypot(min(dx, S - dx), min(dy, S - dy))


def jitter_lattice(rng, nx, ny, jit):
    """128 を割り切る、互いちがいの格子（つなぎ目ですき間・重なりが出ない）"""
    fx, fy = S / nx, S / ny
    pts = []
    for j in range(ny):
        for i in range(nx):
            x = i * fx + (fx / 2 if j % 2 else 0) + rng.uniform(-jit, jit)
            y = j * fy + rng.uniform(-jit, jit)
            pts.append((x % S, y % S))
    return pts


def crag(t, rng, cx, by, hw, h, cols, outline, snowcap=None, crevice=True):
    """岩山ひとつ。cx: すそのまん中、by: すその行、hw: すその半はば、h: 高さ。cols: 暗→明の4色。
    形: 頂は少しずらし、左の斜面はゆるく右の斜面は急（光の側を広く見せる）。半分ほどの山には、肩（低いもう1つの頂）がつく。
    塗り: 稜線（頂からすそへの線）の左が光の面（上ほど明るい2段）、右が影の面（稜線ぎわは中、はなれると暗い）。
    右のふちだけ、いちばん暗い色。下のふちは前の列の山にかくれるので線を引かない。"""
    sx = cx + rng.uniform(-0.2, 0.15) * hw
    sy = by - h
    kl, kr = rng.uniform(0.8, 1.0), rng.uniform(1.1, 1.35)        # 左はゆるく、右は急
    sh = None
    if rng.random() < 0.5:                                        # 肩（左の光の側だけ。右につけると、影の面のとなりに細い光の柱ができた）
        side = -1
        sh = (sx + side * hw * rng.uniform(0.45, 0.65), sy + h * rng.uniform(0.3, 0.45))
    wob = [rng.uniform(-0.8, 0.8) for _ in range(9)]

    def wobble(x):
        """斜面のゆるい折れ（となりの点と線でつなぐ。とびとびにすると、細い針のような柱ができた）"""
        u = min(7.999, max(0.0, (x - cx + hw) / (2 * hw + 1) * 8))
        i = int(u)
        return wob[i] + (wob[i + 1] - wob[i]) * (u - i)

    def top(x):
        d = x - sx
        y = sy + (abs(d) / hw) * h * (kl if d < 0 else kr)
        y += wobble(x) * (abs(d) / hw)
        if sh:
            y = min(y, sh[1] + abs(x - sh[0]) / hw * h * 1.1)
        return y
    cells = {}
    for x in range(int(math.floor(cx - hw)) - 1, int(math.ceil(cx + hw)) + 2):
        ty = top(x)
        if ty > by:
            continue
        for y in range(int(math.ceil(ty)), int(by) + 1):
            cells[(x, y)] = ty
    rng_r = rng.uniform(-0.4, 0.4)

    def main_top(x):
        d = x - sx
        return sy + (abs(d) / hw) * h * (kl if d < 0 else kr) + wobble(x) * (abs(d) / hw)

    def ridge(y, on_sh=False):
        if on_sh:                                              # 肩の稜線も、すそへ向かって少しかたむく
            return sh[0] + (cx - sh[0]) * max(0.0, (y - sh[1]) / max(1.0, by - sh[1])) * 0.5
        f = (y - sy) / max(1, h)
        return sx + (cx - sx) * f * 0.6 + rng_r * f * hw * 0.25
    for (x, y), ty in cells.items():
        on_sh = bool(sh) and ty < main_top(x) - 0.01            # この列のいちばん上が肩のとき、肩の稜線で塗りわける
        f = (y - (sh[1] if on_sh else sy)) / max(1, h)          # 0=頂 … 1=すそ
        xm = ridge(y, on_sh)
        if x < xm:                                                # 光の面（上の3わりは明るい段、ふちの1ドットも明るい）
            c = cols[3] if (f < 0.3 or (y - ty < 1 and f < 0.7)) else cols[2]
            if f > 0.85:
                c = cols[1]
        else:                                                     # 影の面（稜線ぎわは中、はなれると暗い）
            c = cols[1] if x - xm < 3 else cols[0]
        if (x + 1, y) not in cells and x >= xm and f > 0.12:
            c = outline                                           # 右のふち
        t.put(x, y, c)
    if crevice:                                                   # 光の面のひだ（左下へ、2〜3ドット）
        for _ in range(1 + int(hw / 7)):
            f0 = rng.uniform(0.35, 0.65)
            y0 = int(sy + f0 * h)
            x0 = int(ridge(y0)) - rng.randint(2, max(3, int(hw * 0.5)))   # 頂の稜線の左
            for k in range(rng.randint(2, 3)):
                if (x0 - k, y0 + k) in cells:
                    t.put(x0 - k, y0 + k, cols[1])
    if snowcap:                                                   # 頂の雪（下のふちは、ぎざぎざ）
        depth = max(3, int(h * 0.3))
        for (x, y), ty in cells.items():
            lim = sy + depth - (2 if (x * 7) % 5 == 0 else 0) + (abs(x - sx) / hw) * h * 0.25
            if y <= lim and y - ty < depth:
                t.put(x, y, snowcap[1] if x < ridge(y) else snowcap[0])


class Clip:
    """描く行をえらぶ入れもの。mode="below": y >= 128（下のふちをこえて上へまわりこむ所）だけ、
    mode="body": 0 <= y < 128 だけ、mode="above": y < 0（上のふちをこえて下へまわりこむ所）だけ"""
    def __init__(self, t, mode):
        self.t, self.mode = t, mode

    def put(self, x, y, c):
        ok = (y >= S) if self.mode == "below" else (y < 0) if self.mode == "above" else (0 <= y < S)
        if ok:
            self.t.put(x, y, c)

    def get(self, x, y):
        return self.t.get(x, y)

    def col(self, c):
        return self.t.col(c)


def draw_rows(t, items, draw):
    """items を y の小さい順に描く（下にあるものが手前）。つなぎ目をこえる所は、手前・奥がくずれないよう3回に分ける:
    1) いちばん下の列が上へまわりこむ所（いちばん奥）→ 2) ふつうの所 → 3) いちばん上の列が下へまわりこむ所（いちばん手前）"""
    items = sorted(items, key=lambda p: p[1])
    for mode in ("below", "body", "above"):
        for it in items:
            draw(Clip(t, mode), it)


# ===================================================================== 1) 山（M）
def mountain():
    """灰色の岩山が、互いちがいの列でびっしり重なる。ひとつひとつ形がちがう（高さ 10〜15・すそのはば 18〜26）。
    すき間には暗い谷の色。どの方向にもつながるので、山の地形がいくつつながっても1つの山脈に見える"""
    rng = random.Random(41)
    t = Tex("#4a4a56")                                        # 山と山のあいだの谷（いちばん奥）
    cols = ["#5c5c64", "#727280", "#9696a2", "#babac4"]
    items = [(x, y, rng.randrange(1 << 30), rng.uniform(11, 15), rng.uniform(13, 19)) for (x, y) in jitter_lattice(rng, 7, 10, 3)]
    draw_rows(t, items, lambda tt, it: crag(tt, random.Random(it[2]), it[0], it[1], it[3], it[4], cols, "#383842"))
    return t


# ===================================================================== 2) とがった山（N・山脈のまん中の高い峰）
def pyramids():
    """とがった山（N）: 山脈のまん中の高い峰と、火山の本体の両方に使う。M と同じ形の描き方で、より大きく高い峰。
    色は M より暗く、少しあたたかい岩（火山にも合うよう、雪はかぶせない）。
    （前は茶色の三角がならぶ絵で、まわりの灰色の山となじまなかった。キーの名前は前のまま）"""
    rng = random.Random(42)
    t = Tex("#3c3632")
    cols = ["#4e4640", "#665c54", "#8a7e72", "#ada090"]
    items = [(x, y, rng.randrange(1 << 30), rng.uniform(12, 17), rng.uniform(18, 26)) for (x, y) in jitter_lattice(rng, 6, 8, 3)]
    draw_rows(t, items, lambda tt, it: crag(tt, random.Random(it[2]), it[0], it[1], it[3], it[4], cols, "#2a2420"))
    return t


# ===================================================================== 3) 丘（H）
def hills():
    """草の地面（w-grass と同じ）に、やわらかな丸い小山。上と左は明るい草、右下は1段暗い草、すその右下だけに細い影。
    （前は暗い線でかこんだ平たい小山が、はんこのように並んでいた）"""
    t = grass()
    rng = random.Random(43)
    items = [(x, y, rng.uniform(7, 10.5), rng.uniform(0.62, 0.75)) for (x, y) in jitter_lattice(rng, 5, 7, 4)]

    def hummock(tt, it):
        cx, cy, w, k = it
        h = w * k
        for yy in range(-int(h) - 1, 1):
            for xx in range(-int(w) - 1, int(w) + 2):
                u, v = xx / w, yy / h
                if u * u + v * v > 1:
                    continue
                # 丸い丘: 頂の左上に明るい草、右の斜面は1段暗い草、右下のすそはもう1段暗い
                if u < 0.15 and v < -0.45:
                    c = "#86cc52"
                elif u < 0.4:
                    c = "#62b240"
                elif v < -0.3 or u < 0.75:
                    c = "#4e9c34"
                else:
                    c = "#3e8a2c"
                tt.put(int(cx) + xx, int(cy) + yy, c)
        for xx in range(-int(w * 0.3), int(w) + 1):           # すその影（右寄り、1行）
            tt.put(int(cx) + xx, int(cy) + 1, "#3e8a2c" if -w * 0.1 < xx < w * 0.85 else "#4e9c34")
    draw_rows(t, items, hummock)
    return t


# ===================================================================== 4) 雪の森（T）
def snowforest():
    """雪原（w-snow）に、雪をかぶった針葉樹がびっしり。1本は3段の枝。枝の上の面は白い雪、右下は暗い青緑の葉。
    木ごとに高さと幅をかえる。（前は細かい点がちらついて、雪あらしのように見えた）"""
    t = snow()
    rng = random.Random(44)
    DARK, MID, LEAF, SNOWS, SNOWL = "#2e4a64", "#3a5a7a", "#6a8eac", "#d4e2f0", "#ffffff"
    items = [(int(x), int(y), rng.randint(10, 13), rng.uniform(4.0, 5.0)) for (x, y) in jitter_lattice(rng, 11, 12, 1.5)]

    def tree(tt, it):
        cx, cy, hgt, wid = it
        top = cy - hgt
        th = hgt / 3                                           # 3段の枝。段ごとに、上がとがった三角
        for tier in range(3):
            y0 = top + tier * th * 0.85
            tw = wid * (0.55 + 0.225 * tier)                   # 下の段ほど広い
            rows = int(round(th + 1))
            for r in range(rows):
                y = int(y0 + r)
                half = tw * (r + 1) / rows
                for xx in range(-int(half + 0.5), int(half + 0.5) + 1):
                    if abs(xx) > half + 0.25:
                        continue
                    if r == 0 or (r == 1 and xx < 0 and xx > -half * 0.7):
                        c = SNOWL if xx <= 0 else SNOWS            # 枝の上の雪（左は白、右は青白）。雪は段の上だけ
                    elif xx >= half - 0.75:
                        c = DARK                                   # 右のふち
                    else:
                        c = MID if xx > 0 else LEAF
                    tt.put(cx + xx, y, c)
        tt.put(cx + 1, cy + 1, "#c8d8ea")                       # 足もとの雪の影（右下）
        tt.put(cx + 2, cy + 1, "#c8d8ea")
    draw_rows(t, items, tree)
    return t


# ===================================================================== 5) 道（R）
def road():
    """ふみ固めた土の道: 地の色に、2〜3ドットの明るい土のかたまりと、暗い小石のかたまり（影は右下）。点はまかない"""
    rng = random.Random(45)
    t = Tex("#a8703c")
    for _ in range(140):                                       # 明るい土のかたまり（横長）
        x, y = rng.randrange(S), rng.randrange(S)
        w = rng.randint(2, 4)
        for k in range(w):
            t.put(x + k, y, "#b8844c")
        if w >= 3:
            t.put(x + 1, y - 1, "#b8844c")
    for _ in range(46):                                        # 小石: 上が明るく、右下に影
        x, y = rng.randrange(S), rng.randrange(S)
        t.put(x, y, "#cc9a60"); t.put(x + 1, y, "#b8844c")
        t.put(x, y + 1, "#946032"); t.put(x + 1, y + 1, "#7a4c26")
    for _ in range(90):                                        # 少し暗いくぼみ（2ドット）
        x, y = rng.randrange(S), rng.randrange(S)
        t.put(x, y, "#946032"); t.put(x + 1, y, "#946032")
    return t


# ===================================================================== 6) 荒れ地（W）
def waste():
    """ひび割れた、かわいた地面。ボロノイ（つながった輪の上で測る）のさかいがひび。ひびの左上どなりは1段明るい（ひびのふちに光）。
    板の中に、ところどころ小石のかたまり"""
    rng = random.Random(46)
    BASE, LIGHT, DARK, CRACK = "#5c4e66", "#6a5c74", "#4c4056", "#382c40"
    t = Tex(BASE)
    seeds = jitter_lattice(rng, 5, 6, 7)
    owner = {}
    for y in range(S):
        for x in range(S):
            ds = sorted((torus_d(x, y, sx, sy), i) for i, (sx, sy) in enumerate(seeds))
            owner[(x, y)] = (ds[0][1], ds[1][0] - ds[0][0])
    for y in range(S):
        for x in range(S):
            i, gap = owner[(x, y)]
            sx, sy = seeds[i]
            # 板ごとに、左上が少し明るい（板がわずかに盛り上がっている）
            ddx = ((x - sx + S / 2) % S) - S / 2
            ddy = ((y - sy + S / 2) % S) - S / 2
            # ひびは、板のさかいのうち、ところどころ（とちゅうで切れる）
            j = owner[(x, y)][0]
            broken = (math.sin(x * 2 * math.pi / 32 + j) + math.cos(y * 2 * math.pi * 3 / S + 2 * j)) > 1.2   # 128 で1回りする波（つなぎ目でずれない）
            if gap < 1.0 and not broken:
                t.put(x, y, CRACK)

    for y in range(S):                                        # ひびの左上どなりに光
        for x in range(S):
            if t.get(x, y) == t.col(CRACK):
                for (dx, dy) in ((-1, 0), (0, -1)):
                    if t.get(x + dx, y + dy) == t.col(BASE):
                        t.put(x + dx, y + dy, LIGHT)
    for _ in range(14):                                       # 小石のかたまり
        x, y = rng.randrange(S), rng.randrange(S)
        if owner[(x % S, y % S)][1] < 3:
            continue
        t.put(x, y, LIGHT); t.put(x + 1, y, DARK); t.put(x, y + 1, DARK); t.put(x + 1, y + 1, CRACK)
    return t


# ===================================================================== 7) 灰の大地（A）
def ash():
    """火山のまわりの、暗い紫の灰。灰は風にふかれて、ゆるい渦をえがく吹きだまりの線（明るい上のふち＋暗い下のふち）になる。
    線は流れの場にそってのびるので、はんこのくり返しにならない。ところどころ、まだ赤い燃えさしのかたまり。"""
    rng = random.Random(47)
    BASE, DEEP, DRIFT, DRIFTL, EMBER, EMBERL = "#2a1434", "#1e0c26", "#3c1e4a", "#5a3470", "#a8401c", "#f07a24"
    t = Tex(BASE)
    # 流れの場: つながった輪の上の、いくつかの渦の重ねあわせ
    vort = [(rng.uniform(0, S), rng.uniform(0, S), rng.choice((-1, 1)) * rng.uniform(0.6, 1.0)) for _ in range(5)]
    def flow(x, y):
        vx, vy = 1.0, 0.15
        for (cx, cy, s) in vort:
            dx = ((x - cx + S / 2) % S) - S / 2
            dy = ((y - cy + S / 2) % S) - S / 2
            r2 = dx * dx + dy * dy + 60
            vx += -dy * s * 40 / r2
            vy += dx * s * 40 / r2
        n = math.hypot(vx, vy)
        return vx / n, vy / n
    for _ in range(70):                                       # 吹きだまりの線（2ドットの厚み）
        x, y = rng.uniform(0, S), rng.uniform(0, S)
        ln = rng.randint(10, 22)
        for k in range(ln):
            vx, vy = flow(x, y)
            xi, yi = int(x), int(y)
            t.put(xi, yi, DRIFTL if 1 < k < ln - 2 else DRIFT)
            t.put(xi, yi + 1, DRIFTL if 2 < k < ln - 4 else DRIFT)
            t.put(xi, yi + 2, DRIFT)
            t.put(xi, yi + 3, DEEP)
            x += vx; y += vy
    for _ in range(9):                                        # 燃えさし（2×2 の芯と、まわり1ドット）
        x, y = rng.randrange(S), rng.randrange(S)
        t.put(x, y, EMBERL); t.put(x + 1, y, EMBER); t.put(x, y + 1, EMBER); t.put(x + 1, y + 1, EMBER)
    return t


# ===================================================================== 8) 谷（X）
def chasm():
    """深い裂け目をのぞきこんだ絵: 奥はいちばん暗く、岩だなの帯（上の面が明るく、下のふちに影）が、段になって奥へ落ちる。
    帯はゆるく波うち、とちゅうで切れる。"""
    rng = random.Random(48)
    ABYSS, DEEP, LEDGE, LEDGEL, RIM = "#120c14", "#1a121a", "#2a1e2a", "#3a2c3a", "#4c3c4c"
    t = Tex(DEEP)
    for y in range(S):                                        # 奥の暗がり（ゆるい横の帯）
        for x in range(S):
            if (y + int(3 * math.sin(x * 2 * math.pi / 64))) % 16 > 11:
                t.put(x, y, ABYSS)
    for j in range(8):                                        # 岩だな 8 段（16 ドットごと）
        y0 = j * 16 + rng.randint(0, 4)
        ph = rng.uniform(0, 2 * math.pi)
        amp = rng.uniform(1.0, 2.5)
        x = 0
        while x < S:
            seg = rng.randint(14, 34)
            gap = rng.randint(3, 8)
            for k in range(seg):
                xx = x + k
                y = y0 + int(round(amp * math.sin(xx * 2 * math.pi / 64 + ph)))
                end = k in (0, seg - 1)
                t.put(xx, y, RIM if not end else LEDGEL)
                t.put(xx, y + 1, LEDGEL)
                t.put(xx, y + 2, LEDGE)
                t.put(xx, y + 3, ABYSS)                       # 岩だなの下の影
            x += seg + gap
    return t


TEXTURES_V2 = {
    "w-mountain": mountain, "w-pyramids": pyramids, "w-hills": hills, "w-snowforest": snowforest,
    "w-road": road, "w-waste": waste, "w-ash": ash, "w-chasm": chasm,
}
