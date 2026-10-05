"""芯環塔と大滝をひとつにした絵（320×360・16コマ）。2026-10-05、人間の指示「滝と塔をくっつけて、ドットで滝が流れていて、周りが大雨・嵐になって、雷まであるドットの動きを出して」。
重ねる順（奥から）:
  1. 穴と大滝（basin.py の16コマ。水面が穴へ走り、奥の崖を水が底まで落ちる）
  2. 塔（r27-spire の岩の柱。穴の底のさらに下から伸びる）
  3. 塔の足もとを包む、滝つぼの霧と水しぶき（塔の前を、わき上がって流れる）→ 塔と滝が、ひとつの景色になる
  4. 嵐の雲（横いっぱいの、ひとつながりの雲のかたまり。上と左右のふちは、まわりの嵐の暗がりへ溶ける）
  5. 大雨（ななめに降る雨の粒の筋。16コマで切れ目なく降りつづける。ふちほど少なく、まわりの嵐の雨（コード）とつながる）
雷は bolt.py（別の絵）を、ときどき重ねる。
2026-10-05 追加（人間の指示「雨は雲の下に欲しいね、あと塔は雲を突き抜けてもいいかもね」）:
  - 雨は、雲の底より下にだけ降る（雲の上や、雲の前には描かない）。
  - 塔は雲を突き抜け、雲の上に頂が出る。頂は、柱状の岩の柱が、1本ずつちがう高さで折れて終わる形（自然の岩）。
    そのため、絵を上へ80ドット広げた（雲の上のふちも、絵のはしで切れずに、丸くもり上がる）。
絵の (160, 280) が、塔のマスのまん中。1文字=1色（色は絵ごとに、使う色から記号を割り当てる）。エディタで1コマを4つ（160×180）に分けて確かめる。"""
import json
import math
import os

from PIL import Image

import basin
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r27-spire"))
import spire2

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
SPIRE = os.path.join(HERE, "..", "r27-spire")
W, H = 320, 440
CX, CY = 160, 280                 # 塔のマスのまん中
SUMMIT = 26                       # 塔の頂（いちばん高い岩の柱の上のはし。絵の上から）
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


def cloud_lobes():
    """嵐の雲を、大小のもくもくを重ねて組む。
    2026-10-05 人間の指示「雲全体的にモクモクさせよう…今の雲は有機物な感じが強い」のあと、「雲、自然な感じにして」で作り直し:
      - 外形は、きれいなドーム（きのこのかさ）にしない。上のふちの高さは、ゆるいゆらぎで左右ふぞろい（右側が少し高い）。
        左右のはしの長さもちがう。底は、ちぎれてでこぼこ（ところどころ、すそが垂れ下がる）。
      - もくもくは、決まった段に並べない。外形の中に、ばらばらに散らす（大きなもくもくは少なく、小さなもくもくが多い。
        ふちに近いほど小さい＝カリフラワーのような頭）。
      - 本体のまわりに、はなれた小さな雲のかけら（ちぎれ雲）をいくつか置く。
    戻り値: (もくもく [(x, y, 半径, 高さ)], 底の高さ bottom(x))"""
    import random
    rnd = random.Random(1005)
    LEFT, RIGHT = 18, 306

    def top_at(x):                      # 雲の上のふち（左右ふぞろい）
        t = (x - 168) / 150
        return 66 + t * t * 78 + (vnoise(x, 5, 46, 401) - 0.5) * 24 - max(0.0, (x - 170) / 150) * 10

    def bottom(x):                      # 雲の底（ちぎれてでこぼこ。ところどころ垂れ下がる）
        return 168 + (vnoise(x, 9, 18, 402) - 0.5) * 12 + max(0.0, vnoise(x, 2, 7, 403) - 0.62) * 34

    lobes = []
    # 本体: 外形の中に、ばらばらに散らす（大きい玉から置き、小さい玉ほど多く）
    tries = 0
    while len(lobes) < 120 and tries < 20000:
        tries += 1
        x = rnd.uniform(LEFT, RIGHT)
        tp, bt = top_at(x), bottom(x)
        y = rnd.uniform(tp, bt)
        edge = min(x - LEFT, RIGHT - x, y - tp) / 40     # ふちに近いほど 0
        rmax = 6 + 22 * max(0.0, min(1.0, edge))
        r = rnd.uniform(5, rmax) if rnd.random() < 0.7 else rnd.uniform(5, 9)
        # 玉が外形から大きくはみ出さない（上へは少し出てよい＝もくもくの頭）
        if y - r < tp - r * 0.55 or x - r < LEFT - 6 or x + r > RIGHT + 6:
            continue
        lobes.append((x, y, r, 0.0))
    # はしと上のふちを、小さなもくもくでうめる（すき間の穴を作らない）
    for i in range(70):
        x = LEFT + 8 + (RIGHT - LEFT - 16) * (i + rnd.random()) / 70
        tp = top_at(x)
        r = rnd.uniform(5, 11)
        lobes.append((x, tp + r * rnd.uniform(0.35, 0.8), r, 0.0))
    for i in range(40):
        x = LEFT + 10 + (RIGHT - LEFT - 20) * (i + rnd.random()) / 40
        y = (top_at(x) + bottom(x)) / 2
        lobes.append((x, y, rnd.uniform(14, 20), 0.0))
    # ちぎれ雲（本体からはなれた、小さなかけら）
    for (x, y) in ((8, 150), (300, 112), (330, 158), (40, 104)):
        for k in range(3):
            lobes.append((x + rnd.uniform(-8, 8), y + rnd.uniform(-3, 3), rnd.uniform(4, 7), 0.0))
    # 塔が雲を突き抜ける所: 塔の両わきに、まとわりつく小さなもくもく
    lobes.append((CX - 13, top_at(CX) + 3, 8, 5.0))
    lobes.append((CX + 14, top_at(CX) + 5, 7, 5.0))
    return lobes, bottom


LIGHT = (-0.5, -0.66, 0.56)                # 左上・手前からの光


def cloud_layer():
    """もくもくの雲（どのコマも同じ）。ドット絵の雲の描き方: 丸いもくもくを、奥（底が上にある玉）から手前へ重ねて塗る。
    - 玉の中の色は、雲全体の上下の位置で決まる平らな色（上ほど明るく、底は暗く重い。左ほど少し明るい）。
    - 玉の左上のふち（2〜3ドット）は1段明るく、右下のふち（内がわ）は1段暗い。手前の玉が奥の玉をかくすので、
      奥の玉のふちの弧だけが残り、もくもくの重なりに見える。
    - 1ドットのちらばりは置かない。
    戻り値: (雲の色 {(x,y):色}, 雲のマスの集まり)"""
    lobes, bottom = cloud_lobes()
    order = sorted(lobes, key=lambda l: l[1] + l[2])          # 玉の下のはしが上にあるものから（奥から）
    n = len(CLOUD) - 1
    tone = {}
    for (lx, ly, r, _z) in order:
        for y in range(int(ly - r) - 1, int(ly + r) + 2):
            for x in range(int(lx - r) - 1, int(lx + r) + 2):
                if not (0 <= x < W and 0 <= y < H) or y > bottom(x):
                    continue
                dx, dy = x + 0.5 - lx, y + 0.5 - ly
                d = math.sqrt(dx * dx + dy * dy)
                if d > r:
                    continue
                # 雲全体の上下・左右で決まる明るさ
                top = 60.0
                v = 0.92 - (y - top) / (bottom(x) - top + 1) * 0.66 - (x - 40) / 600
                # 玉のふち: 左上は明るく、右下（内がわ）は暗く
                rim = r - d
                ang = (dx * -0.6 + dy * -0.8) / (d + 1e-6)           # 左上を向く度合い
                if rim < 2.6 and ang > 0.25:
                    v += 0.14 if rim < 1.3 else 0.08
                elif rim < 2.2 and ang < -0.35:
                    v -= 0.1
                tone[(x, y)] = v
    layer = {}
    for (x, y), v in tone.items():
        k = max(0, min(n, int(round(v * n))))
        layer[(x, y)] = CLOUD[k]
    # 雲の中の小さな穴（外とつながっていないすき間）は、まわりの色でうめる
    from collections import deque
    outside = set()
    dq = deque((x, y) for x in range(W) for y in (0, H - 1))
    while dq:
        q = dq.popleft()
        if q in outside or q in layer or not (0 <= q[0] < W and 0 <= q[1] < H):
            continue
        outside.add(q)
        x, y = q
        dq.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    ys = [y for (_, y) in layer]
    holes = [(x, y) for y in range(min(ys), max(ys) + 1) for x in range(W) if (x, y) not in layer and (x, y) not in outside]
    while holes:
        rest = []
        for (x, y) in holes:
            nb = [layer.get(q) for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)) if q in layer]
            if nb:
                layer[(x, y)] = max(set(nb), key=nb.count)
                tone[(x, y)] = 0.5
            else:
                rest.append((x, y))
        if len(rest) == len(holes):
            break
        holes = rest
    # ちぎれた1ドット（まわりの4つのうち3つ以上が別の色）を、まわりの多い色に
    for _ in range(2):
        for (x, y), c in list(layer.items()):
            nb = [layer.get(q) for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))]
            nb = [b for b in nb if b is not None]
            if len(nb) == 4 and sum(b != c for b in nb) >= 3:
                layer[(x, y)] = max(set(nb), key=nb.count)
    return layer, tone


VEIL = [(150, 156, 178), (186, 190, 208)]


def cloud_veil(owner):
    """雲のまわりの、透けるうす雲（ゲームでは、半透明で重ねる）。もくもくのふちから外へ、横にたなびく筋になって消える。
    外がわほど少なく、筋は横長のゆらぎで決める（1ドットのちらばりは置かない）。"""
    from collections import deque
    dist = {}
    q = deque()
    for (x, y) in owner:
        dist[(x, y)] = 0
        q.append((x, y))
    R = 12
    while q:
        x, y = q.popleft()
        d = dist[(x, y)]
        if d >= R:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if 0 <= p[0] < W and 0 <= p[1] < H and p not in dist:
                dist[p] = d + 1
                q.append(p)
    veil = {}
    for (x, y), d in dist.items():
        if d == 0:
            continue
        wisp = vnoise(x * 0.35, y * 1.6, 9, 210)                 # 横にのびる筋
        s = (1 - d / (R + 1)) * (0.55 + wisp * 0.9)
        if y > 170:
            s -= (y - 170) / 8                                   # 雲の底の下には、ほとんど出さない（雨がある）
        if s > 0.5:
            veil[(x, y)] = VEIL[1] if s > 0.78 else VEIL[0]
    # ぽつんと1ドットだけ残った所は消す
    for p in list(veil):
        x, y = p
        if sum((x + dx, y + dy) in veil or (x + dx, y + dy) in owner for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) <= 1:
            del veil[p]
    return veil


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


def rain(x, y, fr, base):
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
    if y <= base[x]:
        return None                                    # 雨は雲の底より下だけ
    edge = min(x, W - 1 - x, H - 1 - y) / 50
    if hsh(lane, t // (L // 2), 93) > min(1.0, edge + 0.15):
        return None
    return RAIN[2] if t2 == length - 1 else (RAIN[1] if t2 > length // 2 else RAIN[0])


def crown_top(x, y):
    """塔の頂: 柱状の岩の柱ごとに、ちがう高さで折れて終わる（まん中ほど高く、ふちほど低い）。その柱の上のはし（絵のy）。"""
    sy = y - (CY + TOWER_FEET - 256)                       # 塔の絵の中のy
    c, hw = spire2.cx_at(sy), spire2.hw_at(sy)
    u = (x + 0.5 - c) / hw
    if abs(u) > 1:
        return None
    a = math.asin(max(-1.0, min(1.0, u)))
    twist = sy / 160.0 + spire2.vnoise(0, sy, 40, 3) * 0.25
    col = math.floor((a + 0.4 + twist) / 0.23)
    return SUMMIT + int(u * u * 6) + int(hsh(col, 7, 70) * 9)


def tower_pixels(spire_rows, spire_rgb):
    """塔（雲を突き抜けて、頂まで）。下の方（塔の絵の y>=100）は r27-spire の絵、上は同じ岩の式で、頂まで続ける。"""
    out = {}
    sy0 = CY + TOWER_FEET - len(spire_rows)
    for y, r in enumerate(spire_rows):
        if y < 100:
            continue
        for x, ch in enumerate(r):
            if ch != ".":
                out[(CX - len(r) // 2 + x, sy0 + y)] = spire_rgb[ch]
    rock_keys = list("abcdefghijklmno")
    orig_hw = spire2.hw_at
    spire2.hw_at = lambda yy: max(orig_hw(yy), 12.5)            # 雲の上も、太い柱のまま（細い針にしない）
    for y in range(0, sy0 + 100):
        for x in range(CX - 40, CX + 40):
            sx = x - (CX - 48)
            top = crown_top(sx, y)
            if top is None or y < top:
                continue
            rgb = spire2.rock_rgb(sx, y - sy0)
            if rgb is None:
                continue
            if y == top:
                rgb = mix(rgb, spire2.PAL_RGB["j"], 0.45)          # 折れた柱の上の面（光が当たる）
            elif y == top + 1:
                rgb = mix(rgb, spire2.PAL_RGB["a"], 0.25)          # その下のふち（影）
            out[(x, y)] = spire2.PAL_RGB[spire2.nearest(rgb, rock_keys)]
    spire2.hw_at = orig_hw
    return out


def build():
    spire_rows, spire_rgb = load_spire()
    clouds, owner = cloud_layer()
    veil = cloud_veil(owner)
    tower = tower_pixels(*load_spire())
    # 雲の底（列ごと）。雨はこれより下だけ
    base = [168] * W
    for (x, y) in clouds:
        base[x] = max(base[x], y)
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
        # 2. 塔（雲を突き抜けて、頂まで）
        for (x, y), c in tower.items():
            if 0 <= y < H:
                img[y][x] = c
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
                d = rain(x, y, fr, base)
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
    # 透けるうす雲（ゲームでは半透明で重ねる）
    vk = {c: k for c, k in zip(VEIL, "AB")}
    vrows = ["".join(vk[veil[(x, y)]] if (x, y) in veil else "." for x in range(W)) for y in range(H)]
    with open(os.path.join(HERE, "veil.txt"), "w") as f:
        f.write("\n".join(vrows) + "\n")
    with open(os.path.join(HERE, "pal-veil.json"), "w") as f:
        json.dump({k: "#%02x%02x%02x" % c for c, k in vk.items()}, f)
    vim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for (x, y), c in veil.items():
        vim.putpixel((x, y), c + (255,))
    vim.save(os.path.join(OUT, "veil.png"))
    print("ok", len(colors))


if __name__ == "__main__":
    build()
