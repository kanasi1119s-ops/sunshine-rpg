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
SUMMIT = 4                        # 塔の頂（いちばん高い岩の柱の上のはし。絵の上から。積乱雲の上に出るよう、高くした）
# 積乱雲（r30-cumulonimbus の reshape5、440×256 の絵。2026-10-06 に採用。前は reshape3）を置く所: 雲の絵の (x, y) は、この絵の (x + CLOUD_DX, y + CLOUD_DY)。
# 雲そのものはこの絵には描かず、ゲームで上に重ねる（雲の中の雷のコマがあるので）。塔の上のほう（SPIRE_TOP_Y より上）は、
# 雲のさらに上に重ねる別の絵（spire-top.png）にする（塔が雲を突き抜けて見える）。
CLOUD_DX, CLOUD_DY = -55, -71
SPIRE_TOP_Y = 66
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
        return 168 + (vnoise(x, 9, 40, 402) - 0.5) * 10

    lobes = []
    # 本体: 外形の中に、ばらばらに散らす（大きい玉から置き、小さい玉ほど多く）
    tries = 0
    while len(lobes) < 240 and tries < 40000:
        tries += 1
        x = rnd.uniform(LEFT, RIGHT)
        tp, bt = top_at(x), bottom(x)
        y = rnd.uniform(tp, bt)
        edge = min(x - LEFT, RIGHT - x, y - tp) / 40     # ふちに近いほど 0
        rmax = 5 + 15 * max(0.0, min(1.0, edge))
        r = rnd.uniform(4, rmax) if rnd.random() < 0.65 else rnd.uniform(4, 8)
        # 玉が外形から大きくはみ出さない（上へは少し出てよい＝もくもくの頭）
        if y - r < tp - r * 0.55 or x - r < LEFT - 6 or x + r > RIGHT + 6 or y + r > bt + 1:
            continue
        lobes.append((x, y, r, 0.0))
    # はしと上のふちを、小さなもくもくでうめる（すき間の穴を作らない）
    for i in range(110):
        x = LEFT + 8 + (RIGHT - LEFT - 16) * (i + rnd.random()) / 110
        tp = top_at(x)
        r = rnd.uniform(4, 9)
        lobes.append((x, tp + r * rnd.uniform(0.35, 0.8), r, 0.0))
    # 雲の底: 底にそって、丸いもくもくを並べる（底は丸いふくらみの連なりで終わり、とがらない）
    x = LEFT + 10.0
    while x < RIGHT - 10:
        r = rnd.uniform(7, 13)
        lobes.append((x, bottom(x) - r + 1, r, 0.0))
        x += r * rnd.uniform(1.0, 1.4)
    # ちぎれ雲（本体からはなれた、小さなかけら）
    for (x, y) in ((26, 152), (296, 110), (300, 160), (44, 104)):
        for k in range(3):
            lobes.append((x + rnd.uniform(-8, 8), y + rnd.uniform(-3, 3), rnd.uniform(4, 7), 0.0))
    # 塔が雲を突き抜ける所: 塔の両わきに、まとわりつく小さなもくもく
    lobes.append((CX - 13, top_at(CX) + 3, 8, 5.0))
    lobes.append((CX + 14, top_at(CX) + 5, 7, 5.0))
    # 絵のはしで切れないよう、はしにかかるもくもくはのぞく（まわりの透けるうす雲のぶんも、あける）
    lobes = [l for l in lobes if l[0] - l[2] >= 14 and l[0] + l[2] <= W - 15]
    return lobes, bottom


LIGHT = (-0.5, -0.66, 0.56)                # 左上・手前からの光


def cloud_layer():
    """もくもくの雲（どのコマも同じ）。1ドットずつこだわって塗る（2026-10-05、人間の指示「自然な感じだけど、ドットはもっとこだわって」）。
    - もくもくは、中心も半径も整数にそろえ、きれいなドットの円にする（ふちのがたつきを出さない）。
    - 1つのもくもくの中は1色（平らな面）。上の方のもくもくほど明るく、底の方ほど暗い（玉ごとに色を決めるので、
      玉をまたいだ横のしま模様が出ない）。左ほど少し明るい（光は左上から）。
    - 光: もくもくの左上のふちに、1ドットの明るい弧。雲のいちばん上のふちは、さらに明るい光の弧（日の当たる頭）。
    - 重なりの影: 手前のもくもくの上のふちのすぐ外（奥のもくもくの上）に、1ドットの暗い弧。明るい弧と暗い弧が
      となり合い、もくもくの重なりがくっきり見える。
    - 雲の底のふちは、いちばん暗い色の1ドットの線。
    - 弧は、L字の角のドットをのぞいて、ななめにつながる1ドットの線にする。ぽつんと残ったドットはまわりの色にする。
    戻り値: (雲の色 {(x,y):色}, もくもくの持ち主 {(x,y):番号})"""
    lobes, bottom = cloud_lobes()
    snapped = []
    for (lx, ly, r, _z) in lobes:
        snapped.append((int(round(lx)), int(round(ly)), max(3, int(round(r)))))
    order = sorted(range(len(snapped)), key=lambda i: snapped[i][1] + snapped[i][2])   # 奥（下のはしが上）から手前へ
    owner = {}
    rank = {}
    for k, i in enumerate(order):
        cx, cy, r = snapped[i]
        rank[i] = k
        r2 = r * r + r * 0.8
        for y in range(cy - r - 1, cy + r + 2):
            for x in range(cx - r - 1, cx + r + 2):
                if 0 <= x < W and 0 <= y < H and (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                    owner[(x, y)] = i
    # 雲の中の小さな穴（外とつながらないすき間）は、となりのもくもくでうめる
    from collections import deque
    outside = set()
    dq = deque((x, y) for x in range(W) for y in (0, H - 1))
    while dq:
        q = dq.popleft()
        if q in outside or q in owner or not (0 <= q[0] < W and 0 <= q[1] < H):
            continue
        outside.add(q)
        x, y = q
        dq.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    ys = [y for (_, y) in owner]
    holes = [(x, y) for y in range(min(ys), max(ys) + 1) for x in range(W) if (x, y) not in owner and (x, y) not in outside]
    for _ in range(20):
        rest = []
        for (x, y) in holes:
            nb = [owner[q] for q in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)) if q in owner]
            if nb:
                owner[(x, y)] = nb[0]
            else:
                rest.append((x, y))
        holes = rest
        if not holes:
            break
    # もくもくを、近いものどうし「かたまり」にまとめる（2026-10-05、人間の指示「今度は丸みが多すぎる」）。
    # 陰は、1つ1つの丸ではなく、かたまりのふちの形に沿ってつける。丸いでこぼこは、かたまりの外のふちにだけ見え、
    # かたまりの中に、小さな丸の線がたくさん並ばない。
    n = len(CLOUD) - 1
    seeds = []
    clus = {}
    for i in sorted(range(len(snapped)), key=lambda i: -snapped[i][2]):
        cx, cy, r = snapped[i]
        best, bd = None, 1e9
        for si, (sx, sy) in enumerate(seeds):
            d = math.hypot(cx - sx, (cy - sy) * 1.3)
            if d < bd:
                best, bd = si, d
        if best is None or bd > 24:
            seeds.append((cx, cy))
            best = len(seeds) - 1
        clus[i] = best
    cown = {q: clus[i] for q, i in owner.items()}
    body = {}
    for si, (sx, sy) in enumerate(seeds):
        tp, bt = 60.0, bottom(sx)
        t = max(0.0, min(1.0, (sy - tp) / (bt - tp)))
        body[si] = max(1, min(n - 2, int(round(6.7 - t * 4.4 - (sx - 40) / 300))))
    pbody = {i: body[clus[i]] for i in clus}

    def outside(q, c):
        return cown.get(q) != c

    idx = {}
    for (x, y), c in cown.items():
        k = body[c]
        if owner.get((x, y - 1)) is None:
            k = min(n, k + 2)                                     # 雲のいちばん上のふち（日の当たる頭）
        elif outside((x - 1, y - 1), c) and outside((x - 1, y - 2), c):
            k = min(n, k + 2)                                     # かたまりの左上のふち（光の線）
        elif outside((x - 3, y - 4), c):
            k = min(n, k + 1)                                     # 左上を向いた面（光の面）
        elif outside((x + 3, y + 3), c) or outside((x + 1, y + 4), c):
            k = max(0, k - 1)                                     # 右下を向いた面（影）
        if owner.get((x, y + 1)) is None and y >= bottom(x) - 16:
            k = 0                                                 # 雲の底のふち
        idx[(x, y)] = k
    body = pbody
    # いちばん上のふちの光の線は、L 字の角をとって、ななめにつながる1ドットの線に（変える前の状態を見て決める）
    snap = dict(idx)
    rim = {q for q in owner if owner.get((q[0], q[1] - 1)) is None}
    for (x, y) in rim:
        same = lambda q: q in rim
        if (same((x - 1, y)) or same((x + 1, y))) and (same((x, y + 1)) and not same((x, y - 1))):
            if same((x - 1, y + 1)) or same((x + 1, y + 1)):
                continue
            idx[(x, y)] = snap[(x, y + 1)]
    # ぽつんと残ったドット（4つのとなりが、すべて別の色）は、まわりの多い色に
    for _ in range(2):
        for (x, y), k in list(idx.items()):
            nb = [idx.get(q) for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))]
            if None in nb:
                continue
            if all(b != k for b in nb):
                idx[(x, y)] = max(set(nb), key=nb.count)
    # とがった先（影の三日月の角・光の面の細い先）を丸める: 同じ色のとなりが1つ以下のドットを、その玉の地の色にもどす（3回）
    for _ in range(3):
        snap2 = dict(idx)
        for (x, y), k in snap2.items():
            i = owner[(x, y)]
            if k == body[i] or owner.get((x, y - 1)) is None or (owner.get((x, y + 1)) is None and k == 0):
                continue
            same = sum(1 for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)) if snap2.get(q) == k and owner.get(q) == i)
            if same <= 1:
                idx[(x, y)] = body[i]
    # 小さなかけら（同じ色でつながる5ドット以下の面）は、まわりにいちばん多く接する色にする（細い三角のくずをなくす）
    seen = set()
    for q0 in list(idx):
        if q0 in seen:
            continue
        k = idx[q0]
        comp, st = [], [q0]
        seen.add(q0)
        while st:
            q = st.pop()
            comp.append(q)
            x, y = q
            for nq in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if nq in idx and nq not in seen and idx[nq] == k:
                    seen.add(nq)
                    st.append(nq)
        if len(comp) <= 3 and owner.get((q0[0], q0[1] - 1)) is not None:
            cnt = {}
            cs = set(comp)
            for (x, y) in comp:
                for nq in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if nq in idx and nq not in cs:
                        cnt[idx[nq]] = cnt.get(idx[nq], 0) + 1
            if cnt:
                best = max(cnt, key=cnt.get)
                for q in comp:
                    idx[q] = best
    layer = {q: CLOUD[k] for q, k in idx.items()}
    return layer, owner


# 積乱雲（2026-10-05、人間が見せた写真「こんな感じの雲のがいいかも、試しにやってみて」）。
# 上へ高くもり上がる、きのこの形の雷雲。中は、雷と夕日で、あたたかい金色に光る。ふちは白っぽい灰色、底と右下は青い灰色の影。
WARM = [(64, 46, 44), (104, 70, 52), (150, 100, 60), (196, 140, 72), (232, 184, 104), (250, 220, 150), (255, 242, 200)]
MID = [(48, 46, 56), (80, 74, 82), (116, 106, 108), (156, 142, 134), (196, 182, 166), (228, 220, 206)]


def cb_half_width(y):
    """積乱雲の外形（高さ y での左右の広がり。左, 右）。上はかさのように広く、まん中は少しくびれ、底はまた広がる。左右ふぞろい。"""
    if y < 44 or y > 176:
        return None
    if y < 108:                                    # かさ（上の大きなドーム）
        t = (y - 44) / 64
        hw = 10 + 112 * math.sin(t * math.pi / 2) ** 1.05
        return (hw * 1.0, hw * 0.94)
    if y < 140:                                    # くびれ
        t = (y - 108) / 32
        hw = 122 - 40 * math.sin(t * math.pi * 0.5)
        return (hw, hw * 0.9 + 4)
    t = (y - 140) / 36                             # 底（左に低い棚のように張り出す）
    return (82 + 46 * t, 78 + 18 * t)


def cumulonimbus():
    """積乱雲をドット絵で描く。
    - もくもく: 大きなもくもく（半径 12〜22）を外形の中に重ね、その上を向いた面に、小さなもくもく（半径 4〜9）をさらに重ねる
      （カリフラワーのように、大きな山の上に小さな山）。高さの場（いちばん高い玉の面）から、面の向きを出す。
    - 光は2つ: 空からの光（左上）でふちが白く光る。雲の中の光（雷と夕日。まん中の少し下）で、手前を向いた面が金色に光る。
      中の光は、雲の奥ほど届かない（ふちと底は青い灰色のまま）。
    - くぼみ（もくもくとの境）は1段暗く。底は暗く重い。
    - 色は、冷たい灰色（CLOUD）・中間（MID）・あたたかい金色（WARM）の3つの段の表から選ぶ（色を混ぜてにごらせない）。
      段の境だけ、2×2 の市松もようで1ドットずつまぜ、なめらかにする。"""
    import random
    rnd = random.Random(2026)
    inside = lambda x, y: (lambda hw: hw is not None and CX - hw[0] <= x <= CX + hw[1])(cb_half_width(y))
    lobes = []
    # 外形のふちにそって大きなもくもく（ふちのでこぼこ）
    for y in range(46, 176, 3):
        hw = cb_half_width(y)
        for side, sx in ((-1, CX - hw[0]), (1, CX + hw[1])):
            r = rnd.uniform(10, 18)
            lobes.append((sx - side * r * 0.55, y, r, 0.0))
    x = CX - 40
    while x < CX + 40:                              # かさのてっぺん
        r = rnd.uniform(12, 20)
        lobes.append((x, 46 + r * 0.7, r, 0.0))
        x += r * 0.9
    # 中身の大きなもくもく
    for _ in range(170):
        x, y = rnd.uniform(CX - 130, CX + 130), rnd.uniform(48, 172)
        if inside(x, y):
            lobes.append((x, y, rnd.uniform(12, 22), rnd.uniform(-4, 2)))
    height = {}

    def stamp(lx, ly, r, z):
        for yy in range(int(ly - r) - 1, int(ly + r) + 2):
            for xx in range(int(lx - r) - 1, int(lx + r) + 2):
                if not (0 <= xx < W and 0 <= yy < H) or yy > 176 + 3 * math.sin(xx / 11.0):
                    continue
                d2 = (xx + 0.5 - lx) ** 2 + (yy + 0.5 - ly) ** 2
                if d2 <= r * r:
                    h = z + math.sqrt(r * r - d2)
                    if h > height.get((xx, yy), -1e9):
                        height[(xx, yy)] = h
    for l in lobes:
        stamp(*l)
    # 小さなもくもく: 上を向いた面（上のふち、もくもくのてっぺん）に重ねる
    big = list(height.items())
    rnd.shuffle(big)
    placed = 0
    for (x, y), h in big:
        if placed > 420:
            break
        up = height.get((x, y - 3))
        if up is None or (h - up > 1.6 and rnd.random() < 0.5):
            r = rnd.uniform(4, 9)
            stamp(x + rnd.uniform(-1, 1), y + r * 0.45, r, h - r * 0.55)
            placed += 1
    # 面の向きと光
    L = (-0.55, -0.65, 0.52)
    ln = math.sqrt(sum(c * c for c in L))
    L = [c / ln for c in L]
    GX, GY = CX - 6, 120                            # 雲の中の光のまん中
    blur = {}
    for (x, y) in height:
        acc, cnt = 0.0, 0
        for dy in (-3, 0, 3):
            for dx in (-3, 0, 3):
                v = height.get((x + dx, y + dy))
                if v is not None:
                    acc += v
                    cnt += 1
        blur[(x, y)] = acc / cnt
    BAYER = [[0, 2], [3, 1]]
    layer = {}
    for (x, y), h in height.items():
        hl = height.get((x - 1, y), h - 2)
        hr = height.get((x + 1, y), h - 2)
        hu = height.get((x, y - 1), h - 2)
        hd = height.get((x, y + 1), h - 2)
        nx, ny, nz = -(hr - hl) / 2, -(hd - hu) / 2, 1.3
        nn = math.sqrt(nx * nx + ny * ny + nz * nz)
        nx, ny, nz = nx / nn, ny / nn, nz / nn
        sky = max(0.0, nx * L[0] + ny * L[1] + nz * L[2])
        v = 0.2 + sky * 0.82
        v += max(0.0, (100 - y) / 60) * 0.12                       # 上ほど明るい
        v -= max(0.0, (y - 146) / 30) * 0.42                       # 底は暗く重い
        crease = blur[(x, y)] - h
        if crease > 1.0:
            v -= min(0.22, crease * 0.06)                          # もくもくの境のくぼみ
        # 雲の中の光（手前を向いた面ほど、まん中に近いほど）
        d = math.hypot((x - GX) / 120, (y - GY) / 64)
        glow = max(0.0, 1 - d) ** 1.2 * (0.3 + 0.7 * nz) * 1.25
        glow += (vnoise(x, y, 14, 501) - 0.5) * 0.25
        v += glow * 0.16
        # 3つの表のどれを使うか（市松でまぜる）
        g = glow * 2.3
        bi = BAYER[y % 2][x % 2] / 4 + 0.125
        zone = int(g + (bi - 0.5) * 0.5)
        ramp = CLOUD[1:] if zone <= 0 else (MID if zone == 1 else WARM)
        n = len(ramp) - 1
        f = max(0.0, min(1.0, v)) * n
        k = int(f)
        if f - k > 0.62 and bi > 0.5:
            k += 1
        elif f - k > 0.88:
            k += 1
        layer[(x, y)] = ramp[max(0, min(n, k))]
    # 外のふち: 上と左上は、いちばん明るい光の線（冷たい色）。底のふちは、いちばん暗い線
    for (x, y) in list(layer):
        if (x, y - 1) not in height and (x - 1, y) not in height:
            layer[(x, y)] = CLOUD[-1]
        elif (x, y - 1) not in height:
            layer[(x, y)] = CLOUD[-2]
        elif (x, y + 1) not in height and y > 150:
            layer[(x, y)] = CLOUD[0]
    # ぽつんと1ドットの色（4つのとなりがすべて別の色、しかも市松でない）を、まわりの多い色に
    for (x, y), c in list(layer.items()):
        nb = [layer.get(q) for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))]
        if None in nb or any(b == c for b in nb):
            continue
        diag = [layer.get(q) for q in ((x + 1, y + 1), (x - 1, y - 1))]
        if c in diag:
            continue
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
    # 2026-10-05: 雲は、写真をトレースした積乱雲（r30-cumulonimbus）に差しかえた。雲はゲームで上に重ねるので、ここでは描かない
    clouds = {}
    tower = tower_pixels(*load_spire())
    # 雲の底（列ごと）。雨はこれより下だけ
    base = [168] * W
    crows = [l for l in open(os.path.join(HERE, "..", "r30-cumulonimbus", "reshape5.txt")).read().split("\n") if l]
    for cy_, r in enumerate(crows):
        for cx_, ch in enumerate(r):
            x = cx_ + CLOUD_DX
            if ch != "." and 0 <= x < W:
                base[x] = max(base[x], cy_ + CLOUD_DY)
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
        # 4. 雲（塔が雲のてっぺんを突き抜ける所は、塔を前に出す。下のふちは、ゆるく波うつ）
        for (x, y), c in clouds.items():
            if (x, y) in tower and y < 60 + 3 * math.sin(x / 2.3):
                continue
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
    # 塔の上のほう（雲のさらに上に重ねる）。下のはしは、ゆるく波うつ
    top = {(x, y): c for (x, y), c in tower.items() if 0 <= y < SPIRE_TOP_Y + 3 * math.sin(x / 2.3)}
    th = SPIRE_TOP_Y + 4
    tcols = sorted(set(top.values()))
    tkey = {c: pool[i] for i, c in enumerate(tcols)}
    trows = ["".join(tkey[top[(x, y)]] if (x, y) in top else "." for x in range(W)) for y in range(th)]
    with open(os.path.join(HERE, "spire-top.txt"), "w") as f:
        f.write("\n".join(trows) + "\n")
    with open(os.path.join(HERE, "pal-spire-top.json"), "w") as f:
        json.dump({tkey[c]: "#%02x%02x%02x" % c for c in tcols}, f)
    tim = Image.new("RGBA", (W, th), (0, 0, 0, 0))
    for (x, y), c in top.items():
        tim.putpixel((x, y), c + (255,))
    tim.save(os.path.join(OUT, "spire-top.png"))
    print("ok", len(colors))


if __name__ == "__main__":
    build()
