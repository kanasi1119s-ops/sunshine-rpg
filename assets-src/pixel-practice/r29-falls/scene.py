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
    """嵐の雲を、大小のもくもく（積乱雲のかたまり）を重ねて組む（2026-10-05、人間の指示「雲全体的にモクモクさせよう。
    上側が切れてる。もっとリアルな感じで、透ける感じも雲の周りに。今の雲は有機物な感じが強い」）。
    外形: まん中（塔の上）ほど高くもり上がるドーム。左右のはしは低く、丸く終わる（絵のはしで切れない）。底は平ら。
    もくもくの大きさは 6〜24 ドットとばらばらにし、外がわのふちほど小さいもくもく（カリフラワーのような頭）。"""
    lobes = []
    def top_at(x):                      # 雲の上のふち（ドーム）
        t = (x - CX) / 138
        return 74 + t * t * 70
    BOTTOM = 172                        # 雲の底（平ら）
    k = 0
    # 中身（大きなもくもく。うしろの方）
    for i in range(16):
        x = 40 + i * 16 + (hsh(i, 1, 300) - 0.5) * 10
        if abs(x - CX) > 132:
            continue
        y = (top_at(x) + BOTTOM) / 2 + (hsh(i, 2, 300) - 0.5) * 10
        lobes.append((x, y, 22 + hsh(i, 3, 300) * 6, 0.0))
        lobes.append((x + 8, top_at(x + 8) + 22, 16 + hsh(i, 9, 300) * 4, 1.0))     # 上のふちのすぐ下（すき間を作らない）
    # 上のふちのもくもく（小〜中。ふちに沿って並び、少し外へ出る）
    x = 26.0
    while x < W - 26:
        t = abs(x - CX) / 140
        r = 9 + hsh(int(x), 4, 300) * 10 * (1 - t * 0.45)
        y = top_at(x) + r * 0.6 + (hsh(int(x), 5, 300) - 0.5) * 6
        lobes.append((x, y, r, 3.0))
        # その上に、ときどき小さなもくもくの頭
        if hsh(int(x), 6, 300) > 0.55:
            lobes.append((x + (hsh(int(x), 7, 300) - 0.5) * r, y - r * 0.75, r * 0.6, 4.0))
        x += r * 1.05
    # 下の段（手前）: 底にそって、中くらいのもくもく
    x = 30.0
    while x < W - 30:
        t = abs(x - CX) / 140
        r = 11 + hsh(int(x), 8, 300) * 7
        y = BOTTOM - r * 0.45 + t * t * 6
        lobes.append((x, y, r, 5.0))
        x += r * 1.3
    # 塔が雲を突き抜ける所: 塔の両わきに、まとわりつく小さなもくもく
    lobes.append((CX - 13, top_at(CX) + 4, 8, 12.0))
    lobes.append((CX + 14, top_at(CX) + 6, 7, 12.0))
    return lobes, BOTTOM


LIGHT = (-0.5, -0.66, 0.56)                # 左上・手前からの光


def cloud_layer():
    """もくもくの雲（どのコマも同じ）。もくもくを、高さの場（それぞれの玉の高さのいちばん高い所）としてまとめ、
    その傾きで陰をつける。玉と玉は、境でなめらかにつながり、くぼみ（谷）だけが暗い線になる（つぶつぶの玉に見えない）。
    色は 9 段の平らな面にそろえ、1ドットのちらばりは置かない。外のふちの左上は銀色に光る。
    戻り値: (雲の色 {(x,y):色}, 雲のマスの集まり)"""
    lobes, BOTTOM = cloud_lobes()
    height = {}
    for (lx, ly, r, z) in lobes:
        for y in range(int(ly - r) - 1, int(ly + r) + 2):
            for x in range(int(lx - r) - 1, int(lx + r) + 2):
                if not (0 <= x < W and 0 <= y < H) or y > BOTTOM + 3 * math.sin(x / 9.0) + 2 * math.sin(x / 23.0 + 1):
                    continue                    # 雲の底は、ゆるく波うつ
                d2 = (x + 0.5 - lx) ** 2 + (y + 0.5 - ly) ** 2
                if d2 <= r * r:
                    h = z + math.sqrt(r * r - d2)
                    if h > height.get((x, y), -1e9):
                        height[(x, y)] = h
    # 高さの場を少しぼかす（玉と玉の境が角ばった岩の面にならず、ふんわりつながる）
    raw = height
    height = {}
    for (x, y) in raw:
        acc, cnt = 0.0, 0
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                hv = raw.get((x + dx, y + dy))
                if hv is not None:
                    acc += hv
                    cnt += 1
        height[(x, y)] = acc / cnt
    ln = math.sqrt(sum(c * c for c in LIGHT))
    L = [c / ln for c in LIGHT]
    layer = {}
    n = len(CLOUD) - 1
    for (x, y), h in height.items():
        hl = height.get((x - 1, y), h - 1.5)
        hr = height.get((x + 1, y), h - 1.5)
        hu = height.get((x, y - 1), h - 1.5)
        hd = height.get((x, y + 1), h - 1.5)
        gx, gy = (hr - hl) / 2, (hd - hu) / 2
        nx, ny, nz = -gx, -gy, 1.6
        nl = math.sqrt(nx * nx + ny * ny + nz * nz)
        lam = max(0.0, (nx * L[0] + ny * L[1] + nz * L[2]) / nl)
        v = 0.12 + lam * 0.62
        v += max(0.0, (130 - y) / 70) * 0.22                    # 上ほど光を受けて明るい（積乱雲の頭）
        v -= max(0.0, (y - (BOTTOM - 30)) / 30) * 0.3           # 雲の底は暗く重い
        # くぼみ（となりより、まわりが高い所＝もくもくとの境の谷）は暗く
        if (hl + hr + hu + hd) / 4 - h > 0.6:
            v -= 0.12
        # 外のふち: 左上は銀色、右下は暗く
        out_l, out_u = (x - 1, y) not in height, (x, y - 1) not in height
        if out_l or out_u:
            v += 0.2 if (out_l and out_u) or v > 0.42 else 0.0
        k = max(0, min(n, int(round(v * n))))
        col = CLOUD[k]
        layer[(x, y)] = col
    # ちぎれた1ドット（まわりの4つのうち3つ以上が別の色）を、まわりの多い色に
    for _ in range(2):
        for (x, y), c in list(layer.items()):
            nb = [layer.get(q) for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))]
            nb = [b for b in nb if b is not None]
            if len(nb) == 4 and sum(b != c for b in nb) >= 3:
                layer[(x, y)] = max(set(nb), key=nb.count)
    return layer, height


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
