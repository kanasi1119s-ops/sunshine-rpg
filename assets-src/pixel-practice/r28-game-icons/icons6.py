"""ゲームに入れるフィールドのアイコン・6回目（細かく・少し大きく・リアルに。2026-10-05）。

人間の指示「さらに細かく、少し大きく、リアルな感じで作って」「ドット絵はすべてこだわって」
  - 5回目（r26-game-icons/icons.py）と同じ12点・同じ名前。考え方も同じ:
      町・村 = 4回目の「地形になじむ」作り方（黒い縁なし・地面の色のすそ・地形から取った色・見つける目じるし1つ）
      お城・宮殿 = 3回目の作り方（黒に近い縁・家族のパレット・中庭の見える見下ろし）。**影はまったくつけない**
  - 枠は 64×64。絵の横はばは 52〜60 ドット、足もとは枠の下にそろえる。
  - 細かさ: 瓦の列のある屋根（切妻・寄棟・妻入りの3種類）、窓（ガラス・明かり・下の棚）と扉のある壁、えんとつ、
    小さな通り、いくつかの房でできた木、舟のつながる桟橋、市場の日よけ……を、小さくても本当らしい大きさで。
  - こだわり（どの絵も）: 1ドットの点をまかない（形は「かたまり」で）、光はいつも左上、縁はなめらかに、
    ハッシュや乱数で「ざらざらの模様」を作らない（乱数は置き場所を決めるときだけ）。
    最後に「同じ色のとなりがない1ドット」を数えて表示し、灯・金などのわざと置いた点のほかは 0 に近づける。
  - 1枚 24 色まで。
出力: この folder の <名前>.txt / pal-<名前>.json、preview.png（5回目と並べる）、preview-world.png（本物の地図の上、1倍と2倍）
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PX = os.path.join(HERE, "..")
R23 = os.path.join(PX, "r23-field-icons")
R26 = os.path.join(PX, "r26-game-icons")
TER = os.path.join(PX, "..", "field", "terrain")
sys.path.insert(0, R23)

W = H = 64

# ===================================================================== 色（地形の絵から取った色が中心。暗→明）
GRASS = ["#3e8a2c", "#4e9c34", "#58a83a", "#62b240", "#86cc52"]
GSH = ["#2f6e24", "#3a7a2a"]                                              # 草の上の影（濃い・うすい）
FOREST = ["#0c2a10", "#1c5a22", "#28742a", "#3a9034", "#62b04a"]
STONE = ["#383842", "#5c5c64", "#727280", "#9696a2", "#babac4", "#e2e2e8"]
DIRT = ["#7a4c26", "#946032", "#a8703c", "#b8844c", "#cc9a60"]
SAND = ["#b39a62", "#cdb47c", "#e6d29a", "#f6e8bc"]
SNOW = ["#3a5a7a", "#8ab0cc", "#b4cce2", "#d4e2f0", "#e8f0f8", "#ffffff"]
SEA = ["#163c78", "#1c4890", "#2456a4", "#5a8ad0", "#a8d0f4"]
LAKE = ["#1e5498", "#2660b0", "#3070c4", "#7ab0ea", "#a8d0f4"]
ROOF = ["#5a2a20", "#7e3a2a", "#a24e36", "#c06a48", "#d88c62"]
SLATE = ["#2c3a52", "#3a4e6c", "#4e688c", "#6c88aa", "#94acc8"]
THATCH = ["#6e5228", "#8a6a36", "#a8864a", "#c4a260", "#dcc07c"]
WALL = ["#8c7c64", "#b4a282", "#d6c8a6", "#ece2c6"]
TIMBER = ["#4a2e1c", "#6a4428", "#946032"]
GLASS = "#2c3a52"                                                         # 暗い窓
LIGHT = "#ffd878"
LAMP = "#f0a040"
FIRE = ["#c2401c", "#ff8a2c", LIGHT]
GLOW = ["#3a8aa8", "#7ad0e0", "#d8f8ff"]
GOLD = ["#b0802a", "#e0b850"]
SMOKE = ["#8a8a96", "#a8a8b4", "#c8c8d2", "#e2e2e8"]
MIST = ["#9eb4cc", "#b8c8dc", "#cad8e8", "#dce6f2"]
MIST_SNOW = ["#7e96b2", "#94aac4", "#a8bcd2", "#bccbdd"]                 # 雪の上の霧（雪の白より2段暗い青みの灰。白いと雪にとけて見えなかった）
ACCENT = {LIGHT, LAMP, *FIRE, *GLOW, *GOLD}                               # わざと1ドットで置く色（点の検査から外す）


def hx(c):
    return "#%02x%02x%02x" % c[:3]


_tex = {}


def texture(kind):
    if kind not in _tex:
        _tex[kind] = Image.open(os.path.join(TER, f"w-{kind}.png")).convert("RGB")
    return _tex[kind]


def ground_cols(kind):
    return {hx(c) for n, c in texture(kind).getcolors(65536)}


GROUND_KINDS = ("grass", "snow", "sand", "cloud", "waste", "hills")


def pure_colors():
    out = set()
    for k in GROUND_KINDS:
        out |= ground_cols(k)
    return out


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return 116 * y ** (1 / 3) - 16 if y > 0.008856 else 903.3 * y


def cdist(a, b):
    """色の近さ（明るさの差を重く。色みの差も見る）"""
    ra, ga, ba = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    rb, gb, bb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    la, lb = lum(a), lum(b)
    return (la - lb) ** 2 * 6 + ((ra - ga) - (rb - gb)) ** 2 * 0.25 + (((ra + ga) / 2 - ba) - ((rb + gb) / 2 - bb)) ** 2 * 0.25


# ===================================================================== 1枚ずつのパレット（24色まで。ここに無い色は、いちばん近い色へ）
_G = ["#58a83a", "#3a7a2a", "#2f6e24"]                                  # 草（すそ・影）
_T = ["#3a9034", "#62b04a"]                                            # 木（暗い所は影の色を共有）
_R = ["#7e3a2a", "#a24e36", "#c06a48", "#d88c62"]
_WD = ["#4a2e1c", "#6a4428", "#946032", "#a8703c"]
_WL = ["#b4a282", "#d6c8a6", "#ece2c6"]
PALETTES = {
    "icon-port": _G + _T + _R + _WD + _WL + ["#2c3a52", "#2456a4", "#5a8ad0", "#1c4890", "#cc9a60", "#9696a2", "#ffd878", "#fff4c8"],
    "icon-village": _G + _T + ["#8a6a36", "#a8864a", "#c4a260", "#dcc07c", "#f0dca0"] + _R[:3] + _WD + _WL + ["#3070c4", "#7ab0ea", "#2c3a52", "#ffd878"],
    "icon-village-mist": ["#e8f0f8", "#ffffff", "#d4e2f0", "#bccbdd", "#a8bcd2", "#94aac4", "#7e96b2", "#2e4a64", "#3a5a7a", "#6a8eac", "#c8d8ea",
                          "#2c3a52", "#4e688c", "#6c88aa", "#4a2e1c", "#6a4428", "#946032", "#b8844c", "#383842", "#5c5c64", "#9696a2",
                          "#babac4", "#ffd878", "#f0a040"],
    "icon-lake": ["#58a83a", "#2f6e24"] + _T + ["#3070c4", "#7ab0ea", "#e6d29a", "#727280", "#9696a2", "#babac4"] + _WL + _R[:3]
                 + ["#4a2e1c", "#a8703c", "#2c3a52", "#6c88aa", "#3a8aa8", "#7ad0e0", "#d8f8ff", "#ffd878"],
    "icon-mine": _G + _T + ["#383842", "#5c5c64", "#727280", "#9696a2", "#babac4"] + _WD + _R[:3] + ["#2c3a52", "#4e688c", "#6c88aa"]
                 + ["#b4a282", "#d6c8a6", "#ff8a2c", "#ffd878"],
    "icon-tents": ["#e6d29a", "#cdb47c", "#f6e8bc", "#b89058", "#d4ae72", "#e8c88a"] + _R + ["#ece2c6", "#b4a282"]
                  + ["#1c5a22", "#2f6e24", "#3a9034", "#62b04a"] + ["#4a2e1c", "#6a4428", "#946032"] + ["#9696a2", "#2456a4", "#ffd878", "#e0b850"],
    "icon-tents-grass": _G + _T + _R + ["#b4a282", "#d6c8a6", "#ece2c6", "#f8f2de"] + ["#3070c4", "#7ab0ea", "#e6d29a"]
                        + ["#4a2e1c", "#6a4428", "#946032"] + ["#9696a2", "#babac4", "#ff8a2c", "#ffd878"],
    "icon-temple": _G + ["#62b240"] + ["#383842", "#5c5c64", "#727280", "#9696a2", "#babac4"] + ["#2c3a52", "#3a4e6c", "#4e688c", "#6c88aa"]
                   + _WL + ["#b8c8dc", "#cad8e8", "#dce6f2"] + ["#4a2e1c", "#6a4428", "#a8703c"] + ["#e0b850", "#ffd878"],
    "icon-snowtown": ["#e8f0f8", "#ffffff", "#d4e2f0", "#b4cce2", "#94aac4", "#2e4a64", "#3a5a7a", "#6a8eac", "#5c5c64", "#727280", "#9696a2", "#babac4",
                      "#7e3a2a", "#a24e36", "#c06a48", "#2c3a52", "#4e688c", "#6c88aa", "#4a2e1c", "#6a4428", "#946032", "#b8844c",
                      "#ff8a2c", "#ffd878"],
    "icon-sky": ["#2f6e24", "#3a9034", "#62b04a", "#86cc52", "#383842", "#5c5c64", "#727280", "#9696a2"] + _R + _WL
                + ["#3a4e6c", "#6c88aa", "#2c3a52", "#4a2e1c", "#6a4428", "#946032", "#ffd878"],
}
MERGE = {
    # 港町は青い石板の屋根を灰色の石板にする（青は海の色とまざるため）
    "icon-port": {"#6c88aa": "#9696a2", "#4e688c": "#727280", "#94acc8": "#babac4", "#3a4e6c": "#2c3a52"},
}


# ===================================================================== キャンバス
class Canvas:
    def __init__(self, w=W, h=H, xlim=(2, 61)):
        self.w, self.h = w, h
        self.xlim = xlim                                        # 絵の横はばは 60 ドットまで（左右2ドットはあける）
        self.c = [[None] * w for _ in range(h)]
        self.m = [[None] * w for _ in range(h)]

    def put(self, x, y, col, mat=None):
        x, y = int(math.floor(x)), int(math.floor(y))
        if self.xlim[0] <= x <= self.xlim[1] and 0 <= y < self.h:
            self.c[y][x] = col
            self.m[y][x] = mat

    def get(self, x, y):
        return self.c[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    def rect(self, x0, y0, x1, y1, col, mat=None):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, col, mat)

    def shadow_edges(self):
        """（町）透明に面した右・下のふちだけ、その素材のいちばん暗い色に。左・上はそのまま（縁どりなし）"""
        out = [r[:] for r in self.c]
        for y in range(self.h):
            for x in range(self.w):
                mat = self.m[y][x]
                if self.c[y][x] is None or not mat or isinstance(mat, str):
                    continue
                if (self.get(x + 1, y) is None or self.get(x, y + 1) is None) and \
                        self.get(x - 1, y) is not None and self.get(x, y - 1) is not None:
                    out[y][x] = mat[0]                          # 上や左も空いている先っぽ（光の側）は暗くしない
        self.c = out

    def outline(self, out_col):
        """（お城・宮殿）3回目の縁: 透明に面した右・下は共通の縁の色、左・上は素材の1段暗い色"""
        res = [r[:] for r in self.c]
        for y in range(self.h):
            for x in range(self.w):
                col = self.c[y][x]
                if col is None:
                    continue
                shade = self.get(x + 1, y) is None or self.get(x, y + 1) is None
                lit = self.get(x - 1, y) is None or self.get(x, y - 1) is None
                mat = self.m[y][x]
                if shade:
                    res[y][x] = out_col
                elif lit and mat and col in mat:
                    res[y][x] = mat[max(0, mat.index(col) - 1)]
        self.c = res

    def orphans(self, skip=ACCENT):
        """同じ色のとなり（上下左右）がない1ドットの数（わざと置く色はのぞく）"""
        n = []
        for y in range(self.h):
            for x in range(self.w):
                v = self.c[y][x]
                if v is None or v in skip:
                    continue
                if self.m[y][x] == "ground":
                    continue                                    # 地形と同じ色のすそ（地図の上では見えない）
                if all(self.get(x + dx, y + dy) != v for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))):
                    n.append((x, y))                            # ななめにつながる同じ色があれば「線」なので点ではない（櫂・綱・稜線）
        return n

    def speckles(self, skip=ACCENT):
        """面の中のぽつんとした1ドット（上下左右がすべて塗られていて、同じ色が1つもない）＝ざらつきのもと"""
        return [(x, y) for (x, y) in self.orphans(skip)
                if all(self.get(x + dx, y + dy) is not None for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]

    def clean_soft(self, mats, passes=2):
        """岩・葉の中だけ: ぽつんとした1ドットを、となりの2つ以上が同じ色ならその色に（房のふちのくずを取る）"""
        for _ in range(passes):
            out = [r[:] for r in self.c]
            for (x, y) in self.orphans():
                if not any(self.m[y][x] is m for m in mats):
                    continue
                nb = [self.get(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                nb = [v for v in nb if v is not None and v in self.m[y][x]]
                if nb:
                    best = max(set(nb), key=nb.count)
                    if nb.count(best) >= 2:
                        out[y][x] = best
            self.c = out

    def despeckle(self, skip=ACCENT, passes=2):
        """ぽつんと1つだけの色で、まわり3方以上が同じ色なら、その色にそろえる（線や角はこわさない）"""
        for _ in range(passes):
            out = [r[:] for r in self.c]
            for (x, y) in self.orphans(skip):
                nb = [self.get(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                nb = [v for v in nb if v is not None]
                best = max(set(nb), key=nb.count) if nb else None
                if best is not None and nb.count(best) >= 3:
                    out[y][x] = best
            self.c = out

    def trim_ground(self, keep=1):
        """地形と同じ色だけのすそは、建物などから keep ドットより遠い所をけずる（地図の上では見えない）"""
        core = {(x, y) for y in range(self.h) for x in range(self.w) if self.c[y][x] and self.m[y][x] != "ground"}
        near = set(core)
        for _ in range(keep):
            near |= {(x + dx, y + dy) for (x, y) in near for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
        for y in range(self.h):
            for x in range(self.w):
                if self.m[y][x] == "ground" and (x, y) not in near:
                    self.c[y][x] = None
        for _ in range(3):                                      # すそのとげ（3方が空いた1ドット）もけずる
            for y in range(self.h):
                for x in range(self.w):
                    if self.m[y][x] == "ground" and self.c[y][x] and \
                            sum(self.get(x + dx, y + dy) is None for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 3:
                        self.c[y][x] = None

    def count(self):
        cnt = {}
        for r in self.c:
            for v in r:
                if v:
                    cnt[v] = cnt.get(v, 0) + 1
        return cnt

    def reduce(self, limit=24, prot=()):
        """色が多すぎるときは、近い2色を、よく使われるほうへまとめる。まず地面の粒の色どうし"""
        pure = pure_colors()
        prot = set(prot) | ACCENT
        base = {self.c[y][x] for y in range(self.h) for x in range(self.w) if self.m[y][x] == "ground"}
        self.merges = []

        def lab(h):
            r, g, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
            return (0.3 * r + 0.59 * g + 0.11 * b, r - g, (r + g) / 2 - b)
        while True:
            cnt = self.count()
            if len(cnt) <= limit:
                return
            cols = list(cnt)
            pc = [c for c in cols if c in pure]
            if len(pc) > 3:
                cols = pc
            best = None
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    if cols[i] in prot and cols[j] in prot:
                        continue
                    if cols[i] in base or cols[j] in base:
                        continue
                    a, b = lab(cols[i]), lab(cols[j])
                    d = (a[0] - b[0]) ** 2 * 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
                    if best is None or d < best[0]:
                        best = (d, cols[i], cols[j])
            _, a, b = best
            keep, drop = (a, b) if cnt[a] >= cnt[b] else (b, a)
            if drop in prot:
                keep, drop = drop, keep
            self.merges.append(f"{drop}->{keep}")
            self.c = [[keep if v == drop else v for v in r] for r in self.c]

    def save(self, name, trim=True, limit=24, merge=None):
        """merge: {まとめる色: 残す色}。色数を減らすときは、どの色をどれにまとめるかを1枚ずつ決める（自動ではなく、わざと）。
        PALETTES[name] があれば、それ以外の色は、そのパレットのいちばん近い色に置きかえる（置きかえた組は表示して確かめる）"""
        self.clean_soft(SOFT_MATS)
        if trim:
            self.trim_ground()
        merge = dict(merge or {})
        merge.update(MERGE.get(name, {}))
        for a, b in merge.items():
            self.c = [[b if v == a else v for v in r] for r in self.c]
        pal = PALETTES.get(name)
        if pal and not os.environ.get("R28_RAW"):
            assert len(set(pal)) <= limit, (name, len(set(pal)))
            mp = {}
            for col in self.count():
                if col not in pal:
                    mp[col] = min(pal, key=lambda p: cdist(col, p))
            if os.environ.get("R28_SHOWMAP"):
                print("  ", name, " ".join(f"{a}->{b}" for a, b in mp.items()))
            self.c = [[mp.get(v, v) for v in r] for r in self.c]
        self.merges = []
        if not os.environ.get("R28_RAW"):
            self.reduce(limit)
        if self.merges:
            print("  !! 自動でまとめた色:", " ".join(self.merges))
        self.despeckle()
        ys = [y for y in range(self.h) for x in range(self.w) if self.c[y][x]]
        dy = self.h - 1 - max(ys)                               # 足もとを枠のいちばん下にそろえる
        if dy > 0:
            self.c = [[None] * self.w for _ in range(dy)] + self.c[:self.h - dy]
        used = sorted(self.count(), key=lambda h: sum(int(h[i:i + 2], 16) for i in (1, 3, 5)))
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        mp = {c: letters[i] for i, c in enumerate(used)}
        with open(os.path.join(HERE, f"{name}.txt"), "w") as f:
            f.write("\n".join("".join(mp[v] if v else "." for v in r) for r in self.c) + "\n")
        with open(os.path.join(HERE, f"pal-{name}.json"), "w") as f:
            json.dump({mp[c]: c for c in used}, f)
        return name, len(used), len(self.orphans()), len(self.speckles())


# ===================================================================== 地面（すそ・影・草のふさ）
GROUND = {
    "grass": dict(tex="grass", sh=GSH, tuft=[GRASS[4], GRASS[3]]),
    "hills": dict(tex="grass", sh=GSH, tuft=[GRASS[4], GRASS[3]]),
    "snow": dict(tex="snow", sh=["#a6bfd8", "#c4d6ea"], tuft=["#ffffff", "#e8f0f8"]),
    "sand": dict(tex="sand", sh=["#b39a62", "#cdb47c"], tuft=["#f6e8bc", "#e6d29a"]),
    "cloud": dict(tex="cloud", sh=["#a2bcdc", "#b6cce6"], tuft=["#ffffff", "#eef4fc"]),
    "waste": dict(tex="waste", sh=["#382c40", "#4c4056"], tuft=["#6a5c74", "#5c4e66"]),
}


def skirt(c, cx, cy, rx, ry, kind):
    """町の下の地面（いちばん多い地形の色1色だけ。地形の粒はずれるので描かない）。けずった後は、すき間だけに残る"""
    base = sorted(texture(GROUND[kind]["tex"]).getcolors(65536), reverse=True)[0][1]
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                c.put(x, y, hx(base), "ground")


def cast(c, x0, x1, ytop, ybot, kind, dx=2, dy=2):
    """建物の影: 左上からの光で、右と下へ dx・dy ずれた形。建物のすぐ下の1行だけ濃い色、あとはうすい色（市松にしない）"""
    sh = GROUND[kind]["sh"]
    for y in range(ytop + dy, ybot + dy + 1):
        for x in range(x0 + dx, x1 + dx + 1):
            if not (x0 <= x <= x1 and ytop <= y <= ybot):
                c.put(x, y, sh[0] if (y == ybot + 1 and x <= x1 + 1) or (x == x1 + 1 and y <= ybot + 1) else sh[1])


def ell_shadow(c, cx, cy, rx, ry, kind):
    sh = GROUND[kind]["sh"]
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                c.put(x, y, sh[1])


def tuft(c, x, y, kind, h=2):
    """草のふさ（はば2〜3の小さな山形。点ではなく、かたまり）"""
    t = GROUND[kind]["tuft"]
    if h >= 2:
        c.put(x + 1, y - 1, t[0])
    c.put(x, y, t[1]); c.put(x + 1, y, t[0]); c.put(x + 2, y, t[1])


# ===================================================================== 家（3種類の屋根・窓・扉・えんとつ）
def house(c, x0, yb, w, kind="side", roof=ROOF, wall=WALL, rh=None, wh=5, door=None, wins=(), lit=(),
          chimney=None, snow=False, timber=False, ground="grass", shadow=True):
    """1軒の家。x0..x0+w-1 が屋根のはば（壁は左右1ドット内がわ）。yb は壁のいちばん下の行。
    kind: side（棟が横の切妻）/ hip（寄棟）/ front（妻がこちらを向く）
    roof・wall は暗→明の色の並び。wins は窓の左はしの x（家の左はしからの距離）、lit はそのうち明かりのつく窓の番号"""
    x1 = x0 + w - 1
    rh = rh or max(5, w // 2)
    yw0 = yb - wh + 1
    yr0 = yw0 - rh
    wx0, wx1 = x0 + 1, x1 - 1
    if shadow:
        cast(c, x0, x1, yr0, yb, ground, dx=2, dy=1)
    # 壁
    for y in range(yw0, yb + 1):
        for x in range(wx0, wx1 + 1):
            col = wall[2]
            if x == wx1:
                col = wall[1]
            if y == yw0:
                col = wall[1] if x < wx1 else wall[0]           # 軒の下の影
            c.put(x, y, col, wall)
    if timber:
        for y in range(yw0 + 1, yb + 1):
            c.put(wx0, y, TIMBER[1], TIMBER); c.put(wx1, y, TIMBER[0], TIMBER)
        for x in range(wx0, wx1 + 1):
            c.put(x, yw0, TIMBER[0], TIMBER)
    # 窓（はば2・高さ2。下に明るい棚）
    for i, wxo in enumerate(wins):
        wx = x0 + wxo
        on = i in lit
        for dy in range(2):
            c.put(wx, yw0 + 1 + dy, (LIGHT if dy == 0 else LAMP) if on else GLASS, wall)
            c.put(wx + 1, yw0 + 1 + dy, LAMP if on else GLASS, wall)
        if yw0 + 3 < yb or not door:
            c.put(wx, yw0 + 3, wall[3], wall); c.put(wx + 1, yw0 + 3, wall[3], wall)
    # 扉（はば2・高さ3）
    if door is not None:
        dx = x0 + door
        for y in range(yb - 2, yb + 1):
            c.put(dx, y, TIMBER[1], TIMBER); c.put(dx + 1, y, TIMBER[0], TIMBER)   # 扉: 左の板は1段明るい（2本の縦の面）
    # 屋根
    if kind == "front":
        front_roof(c, x0, x1, yr0, yw0, roof, wall)
    elif kind == "hip":
        hip_roof(c, x0, x1, yr0, yw0 - 1, roof)
    else:
        side_roof(c, x0, x1, yr0, yw0 - 1, roof)
    if chimney is not None:
        cx = x0 + chimney
        cy = yr0 + 1
        for y in range(cy - 3, cy + 1):
            c.put(cx, y, STONE[4], STONE); c.put(cx + 1, y, STONE[2], STONE)
        c.put(cx, cy - 4, STONE[1], STONE); c.put(cx + 1, cy - 4, STONE[1], STONE)
    if snow:
        snow_cap(c, x0, x1, yr0, rh)
    return yr0


def side_roof(c, x0, x1, y0, y1, pal):
    """棟が横の切妻: 上の行が棟（明るい）、2行ごとに瓦の列（明・中）、軒は暗い。左のはしは1段明るく、右のはしは1段暗く"""
    for y in range(y0, y1 + 1):
        k = y - y0
        for x in range(x0, x1 + 1):
            if k == 0 and x in (x0, x1):
                continue                                        # 棟の両はしを丸める
            if k == 0:
                i = 4
            elif y == y1:
                i = 1
            else:
                per = 3 if y1 - y0 >= 6 else 2                  # 高い屋根は「明・明・影」の3行で1列の瓦
                i = 2 if (k % per == 0) else 3
            if x == x1 and k > 0:
                i = max(0, i - 1)
            elif x == x0 and 0 < k and y < y1:
                i = min(4, i + 1)
            c.put(x, y, pal[i], pal)


def hip_roof(c, x0, x1, y0, y1, pal):
    """寄棟: いちばん近い軒で面を分ける（左＝明るい、手前＝中、右＝暗い）。瓦の列は面ごとに軒と平行。棟と左の稜は明るい線"""
    rh = y1 - y0 + 1
    for y in range(y0, y1 + 1):
        k = y - y0
        df = y1 - y
        for x in range(x0, x1 + 1):
            dl, dr = x - x0, x1 - x
            if min(dl, dr) < (rh - 1 - k) * 0.9 - 0.5 and k < rh - 1:
                if min(dl, dr) < rh - 1 - k - 1:
                    continue
            m = min(df, dl, dr)
            if y == y1:
                i = 1
            elif dl == m and dl <= df:
                i = 4 if dl == df else 3                      # 左の面は1色（稜だけ明るい線）。細い縦じまは点に見えた
            elif dr == m and dr <= df:
                i = 2 if dr == df else 1                      # 右の面も1色
            else:
                i = 3 if df % 2 == 1 else 2                   # 手前の面
            if k == 0:
                i = 4
            c.put(x, y, pal[i], pal)


def front_roof(c, x0, x1, y0, yw0, pal, wall):
    """妻がこちらを向く家: 棟は縦。左の斜面は明るく、右は暗い。手前のふちは「へ」の字の破風（暗い板）、その下に三角の壁"""
    cx = (x0 + x1) / 2
    half = (x1 - x0) / 2
    gh = max(2, int(half * 0.6))                              # 三角の壁の高さ
    for y in range(y0, yw0):
        for x in range(x0, x1 + 1):
            t = abs(x + 0.5 - (cx + 0.5)) / (half + 0.5)
            ybot = yw0 - 1 - int(round((1 - t) * gh))
            if y > ybot:
                if y >= ybot + 1 and x0 < x < x1:
                    c.put(x, y, wall[3] if x < cx else wall[2], wall)   # 三角の壁
                continue
            if y == ybot:
                c.put(x, y, TIMBER[0], TIMBER)                   # 破風の板
                continue
            left = x + 0.5 < cx + 0.5
            k = y - y0
            if abs(x + 0.5 - (cx + 0.5)) < 0.6:
                i = 4 if k == 0 or True else 3                  # 棟
                i = 4
            elif left:
                i = 3 if (x - x0) % 2 == 0 else 4 if (x - x0) % 4 == 1 else 3
                i = 3
            else:
                i = 2 if x < x1 else 1
            c.put(x, y, pal[i], pal)
    gx = int(cx)
    c.put(gx, yw0 - gh + 1, GLASS, wall)                          # 妻の小窓


def snow_cap(c, x0, x1, y0, rh):
    """屋根の雪: 上の 2〜3 行に、はば5の丸いこぶ。右の3ドットは青白（影）"""
    for x in range(x0, x1 + 1):
        ph = (x - x0) % 5
        dep = 3 if ph in (1, 2, 3) else 2
        if x in (x0, x1):
            dep = 2
        for y in range(y0, y0 + dep):
            if c.get(x, y) is not None:
                col = SNOW[5] if x < x1 - 2 else SNOW[3]
                c.put(x, y, col, SNOW)


# ===================================================================== 木（いくつかの房でできた葉）
def tree(c, cx, cy, r=5.0, pal=FOREST, ground="grass", trunk=2, shadow=True):
    """葉は5つの房。房ごとに左上が明るく、右下は暗い。いちばん明るい色は房の中の左上だけ（ふちには出さない。
    草より明るいふちは草にとけて形がくずれた）。幹は下に2ドット"""
    if shadow:
        ell_shadow(c, cx + 2.5, cy + r * 0.8, r * 0.95, r * 0.45, ground)
    for y in range(int(cy + r * 0.55), int(cy + r * 0.55) + trunk + 1):
        c.put(cx - 1, y, TIMBER[2], TIMBER); c.put(cx, y, TIMBER[0], TIMBER)
    lobes = [(0.0, -0.42, 0.56), (-0.45, -0.02, 0.55), (0.45, -0.04, 0.55), (0.0, 0.0, 0.62), (-0.1, 0.36, 0.56), (0.38, 0.34, 0.5)]
    mat = soft(pal[1:])
    for (lx, ly, lr) in lobes:
        px_, py_, rr = cx + lx * r, cy + ly * r, lr * r
        for y in range(int(py_ - rr) - 1, int(py_ + rr) + 2):
            for x in range(int(px_ - rr) - 1, int(px_ + rr) + 2):
                u, v = (x + 0.5 - px_) / rr, (y + 0.5 - py_) / rr
                d = u * u + v * v
                if d > 1:
                    continue
                s = u * 0.62 + v * 0.78
                if s < -0.35:
                    col = pal[4] if (d < 0.62 and s < -0.42) else pal[3]
                elif s < 0.3:
                    col = pal[3] if s < -0.05 else pal[2]
                else:
                    col = pal[2] if s < 0.62 else pal[1]
                c.put(x, y, col, mat)


# 針葉樹は手で1ドットずつ決めた形（雪の森の地形と同じ色）。W=雪 w=雪の影 G=葉の明るい面 g=葉 d=葉の暗いふち t=幹
PINE_L = [
    ".....W.....",
    "....WWg....",
    "...WWGgd...",
    "..WWGGggd..",
    "....WWgg...",
    "...WWGGgd..",
    "..WWGGgggd.",
    ".wWGGGgggd.",
    "...WWWGgg..",
    "..WWGGGggd.",
    ".WWGGGGgggd",
    "wwGGGgggggd",
    ".....td....",
]
PINE_S = [
    "...W...",
    "..WWg..",
    ".WWGgd.",
    "..WWgd.",
    ".WWGggd",
    "wWGGggd",
    "...td..",
]


def pine(c, cx, yb, h=12, pal=None):
    """針葉樹（手描きの形を置く）。h が 10 以上なら大きい形。足もとに雪の上の影"""
    pal = pal or ["#2e4a64", "#3a5a7a", "#6a8eac", "#c8d8ea", "#ffffff"]          # 雪の森の地形（かきなおし後）の色
    sp = PINE_L if h >= 10 else PINE_S
    mp = {"W": pal[4], "w": pal[3], "G": pal[2], "g": pal[1], "d": pal[0], "t": TIMBER[0]}
    x0 = int(cx) - len(sp[0]) // 2
    y0 = int(yb) - len(sp) + 1
    sh = GROUND["snow"]["sh"][1]
    for k in range(len(sp[0]) - 2):                               # 足もとの影（右へ）
        c.put(x0 + 3 + k, yb + 1, sh)
    for j, row in enumerate(sp):
        for i, ch in enumerate(row):
            if ch != ".":
                c.put(x0 + i, y0 + j, mp[ch], [pal[0]] + pal)


# ===================================================================== 水・道・小物
def water_ell(c, cx, cy, rx, ry, pal, rim=None, rim_w=1.6, clip=None):
    """水面: まん中の色1色＋岸ぞいに1段明るい帯（浅瀬）。rim は岸の砂の色の並び（明→暗の2色）"""
    for y in range(int(cy - ry - 3), int(cy + ry + 3)):
        for x in range(int(cx - rx - 3), int(cx + rx + 3)):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            d = math.sqrt(u * u + v * v)
            if clip and not clip(x, y):
                continue
            if d <= 1:
                inner = d < 1 - 1.4 / min(rx, ry)
                c.put(x, y, pal[2] if inner else pal[3])
            elif rim and d <= 1 + rim_w / min(rx, ry):
                c.put(x, y, rim[0] if v < 0.2 else rim[1])


def wave_dash(c, x, y, n, col):
    for k in range(n):
        c.put(x + k, y, col)


def path(c, pts, w=3, pal=DIRT):
    """土の道: まん中の色、左上のふちは1段明るく、右下のふちは1段暗い"""
    cells = set()
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = int(max(abs(xb - xa), abs(yb - ya), 1) * 2)
        for k in range(n + 1):
            x = xa + (xb - xa) * k / n
            y = ya + (yb - ya) * k / n
            for dx in range(w):
                for dy in range(w):
                    if (dx - (w - 1) / 2) ** 2 + (dy - (w - 1) / 2) ** 2 <= ((w) / 2) ** 2 + 0.1:
                        cells.add((int(x + dx - (w - 1) / 2), int(y + dy - (w - 1) / 2)))
    for (x, y) in cells:
        c.put(x, y, pal[2])                                     # 地形の道と同じ、平らな1色（ふちの線を引くと管に見えた）
    return cells


def puff(c, cx, cy, r, pal=SMOKE):
    """けむり・雲・霧の丸いかたまり（左上が明るく、右下は1段暗い）"""
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u, v = (x + 0.5 - cx) / r, (y + 0.5 - cy) / (r * 0.8)
            d = u * u + v * v
            if d <= 1:
                s = u * 0.6 + v
                c.put(x, y, pal[3] if s < -0.35 else pal[2] if s < 0.45 else pal[1], pal)


def awning(c, x0, x1, y, cols=(ROOF[3], WALL[3]), dark=(ROOF[1], WALL[1]), goods=True):
    """市場の日よけ: 布の上の面2行（はば2のしま）＋前のふち1行（暗い）、下に柱と台の上の品物"""
    for x in range(x0, x1 + 1):
        st = ((x - x0) // 2) % 2 == 0
        c.put(x, y, cols[0] if st else cols[1], ROOF)
        c.put(x, y + 1, cols[0] if st else cols[1], ROOF)
        c.put(x, y + 2, dark[0] if st else dark[1], ROOF)
    for x in (x0, x1):
        c.put(x, y + 3, TIMBER[0], TIMBER); c.put(x, y + 4, TIMBER[0], TIMBER)
    for x in range(x0 + 1, x1):
        c.put(x, y + 3, TIMBER[1], TIMBER)
        if goods:
            c.put(x, y + 4, [THATCH[4], ROOF[3], GRASS[4], THATCH[3]][((x - x0 - 1) // 2) % 4], TIMBER)


def boat(c, x0, y, n=8, sail=None):
    """小舟: 上のふち（明るい木）・船体（暗い木）・下の水の影。sail は帆の高さ（白い三角、左が明るい）"""
    for x in range(x0, x0 + n):
        c.put(x, y, TIMBER[2] if x < x0 + n - 1 else TIMBER[1], TIMBER)
    for x in range(x0 + 1, x0 + n - 1):
        c.put(x, y + 1, TIMBER[0], TIMBER)
    for x in range(x0 + 1, x0 + n):
        c.put(x, y + 2, SEA[1])
    if sail:
        mx = x0 + n // 2 - 1
        for k in range(sail):
            yy = y - 1 - k
            c.put(mx, yy, TIMBER[0], TIMBER)
            wdt = int((sail - k) * 0.55) + 1
            for x in range(mx + 1, mx + 1 + wdt):
                c.put(x, yy, WALL[3] if x < mx + wdt else WALL[1], WALL)
        c.put(mx, y - sail - 1, ROOF[3], ROOF)


# ===================================================================== 1) 港町（灯里・波音の浜）
def lighthouse(c, cx, ybase, h=24):
    """灯台: 岩の台・下が太い白い塔（赤い帯2本）・回廊・灯室（黄色い灯）・暗い丸屋根"""
    top = ybase - h
    for y in range(top + 6, ybase + 1):
        t = (y - top - 6) / max(1, h - 6)
        half = 2.2 + t * 1.8
        for x in range(int(cx - half - 1), int(cx + half + 2)):
            u = (x + 0.5 - cx) / half
            if abs(u) > 1:
                continue
            band = (y - top) in (11, 12, 13, 18, 19, 20)
            pal = ROOF if band else WALL
            i = 3 if u < -0.2 else 2 if u < 0.5 else 1
            if band:
                i = 3 if u < -0.2 else 2 if u < 0.5 else 1
            c.put(x, y, pal[i], pal)
    for (wy, wx) in ((top + 9, cx), (top + 16, cx - 1)):
        c.put(wx, wy, GLASS, WALL); c.put(wx, wy + 1, GLASS, WALL)
    c.put(cx - 1, ybase, TIMBER[0], WALL); c.put(cx, ybase, TIMBER[0], WALL)
    c.put(cx - 1, ybase - 1, TIMBER[1], WALL); c.put(cx, ybase - 1, TIMBER[0], WALL)
    for x in range(int(cx) - 4, int(cx) + 5):                     # 回廊
        c.put(x, top + 6, SLATE[3] if x < cx + 2 else SLATE[1], SLATE)
        c.put(x, top + 5, SLATE[1] if x in (cx - 4, cx + 4) else None, SLATE) if x in (cx - 4, cx + 4) else None
    for y in range(top + 2, top + 6):                             # 灯室
        for x in range(int(cx) - 2, int(cx) + 3):
            col = LIGHT if x < cx + 1 else LAMP
            if x == cx - 2 or x == cx + 2:
                col = SLATE[1]
            c.put(x, y, col, SLATE)
    for x in range(int(cx) - 3, int(cx) + 4):                     # 丸屋根
        c.put(x, top + 1, SLATE[2] if x < cx else SLATE[1], SLATE)
    for x in range(int(cx) - 2, int(cx) + 3):
        c.put(x, top, SLATE[3] if x < cx else SLATE[2], SLATE)
    c.put(cx, top - 1, SLATE[3], SLATE)


def rocks_base(c, cx, cy, rx, ry, pal=STONE):
    """岩の台（いくつかの丸い岩。左上が明るい）"""
    for (dx, dy, r) in ((-0.55, -0.15, 0.5), (0.45, -0.25, 0.5), (0.0, 0.2, 0.6), (-0.6, 0.35, 0.4), (0.62, 0.3, 0.42)):
        px_, py_ = cx + dx * rx, cy + dy * ry
        rr = r * rx
        for y in range(int(py_ - rr) - 1, int(py_ + rr) + 2):
            for x in range(int(px_ - rr) - 1, int(px_ + rr) + 2):
                u, v = (x + 0.5 - px_) / rr, (y + 0.5 - py_) / (rr * 0.75)
                d = u * u + v * v
                if d <= 1:
                    s = u * 0.6 + v * 0.8
                    c.put(x, y, pal[4] if s < -0.45 else pal[3] if s < 0.15 else pal[2] if s < 0.6 else pal[1], pal)


def icon_port():
    c = Canvas()
    g = "grass"
    skirt(c, 30, 36, 30, 27, g)
    # 入り江（右下）: 砂浜の帯・浅瀬・深い水
    water_ell(c, 44, 57, 17, 7.5, SEA, rim=(SAND[3], SAND[2]), rim_w=2.4)
    for (x, y, n) in ((51, 54, 3), (38, 61, 3)):
        wave_dash(c, x, y, n, SEA[3])
    tree(c, 41, 8, 4.4)
    tree(c, 8, 9, 4.4)
    # 灯台（岩の台の上。目じるし）
    rocks_base(c, 53, 44, 6, 3.5)
    lighthouse7(c, 53, 41, 28)
    # 桟橋と舟
    pier(c, 29, 46, 61, w=4)
    stamp(c, 34, 40, "sailboat", TIMBER)
    stamp(c, 46, 55, "rowboat", TIMBER)
    # 通り（桟橋から町へ）
    path(c, [(30, 45), (28, 38), (22, 31), (12, 29)], w=3)
    # 家（赤茶の瓦と灰色の石板。窓と扉と明かり）
    house(c, 3, 23, 15, "side", ROOF, door=10, wins=(2, 6), lit=(0,), chimney=11)
    house(c, 20, 20, 12, "hip", SLATE, door=7, wins=(2,), lit=())
    house(c, 33, 25, 11, "front", ROOF, door=5, wins=(2,), lit=(0,))
    house(c, 2, 40, 13, "hip", ROOF, door=8, wins=(2,), lit=(0,))
    house(c, 16, 43, 11, "front", SLATE, door=6, wins=(2,))
    # 港の倉庫（長い切妻）と市場の日よけ
    house(c, 3, 58, 18, "side", SLATE, wh=6, door=12, wins=(2, 6), lit=(1,), chimney=4)
    awning(c, 20, 27, 47)
    c.shadow_edges()
    return c.save("icon-port")


# ===================================================================== 2) 村（麦香野ほか）
def icon_village():
    c = Canvas()
    g = "grass"
    skirt(c, 32, 36, 30, 27, g)
    # 麦畑（右上）: 実った麦（つやの帯）と、刈ったあとの畑（麦の束）
    wheat_field(c, 36, 8, 24, 11, ripe=True)
    wheat_field(c, 36, 21, 24, 6, ripe=False)
    for (sx, sy) in ((38, 21), (44, 22), (50, 21), (56, 22)):
        stamp(c, sx, sy, "stook", THATCH)
    fence(c, 37, 59, 28)
    # 水路（左から、橋の下を通って水車の水路へ。そのあと右下へ）
    pts = [(2, 40), (12, 41), (24, 45), (30, 48)]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        for x in range(xa, xb + 1):
            y = round(ya + (yb - ya) * (x - xa) / max(1, xb - xa))
            c.put(x, y - 1, DIRT[3]); c.put(x, y, LAKE[3]); c.put(x, y + 1, LAKE[2]); c.put(x, y + 2, LAKE[2])
            c.put(x, y + 3, LAKE[1]); c.put(x, y + 4, DIRT[1])
    pts = [(50, 48), (61, 53)]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        for x in range(xa, xb + 1):
            y = round(ya + (yb - ya) * (x - xa) / max(1, xb - xa))
            c.put(x, y - 1, DIRT[3]); c.put(x, y, LAKE[3]); c.put(x, y + 1, LAKE[2]); c.put(x, y + 2, LAKE[2])
            c.put(x, y + 3, LAKE[1]); c.put(x, y + 4, DIRT[1])
    # 橋
    for x in range(14, 19):
        for y in range(38, 46):
            c.put(x, y, DIRT[4] if (y - 38) % 2 == 0 else DIRT[3], DIRT)
    for y in range(38, 46):
        c.put(19, y, DIRT[1], DIRT)
    path(c, [(16, 63), (16, 46)], w=3)
    path(c, [(16, 37), (18, 30), (28, 26)], w=3)
    # 水車小屋と水車（目じるし: 水路にはまった木の輪、はねる水しぶき）
    house(c, 20, 44, 14, "side", THATCH, door=4, wins=(8,), lit=(0,), chimney=2)
    for y in range(39, 48):                                       # 水車の後ろの壁（輪の腕が明るい壁の前で読めるように）
        for x in range(34, 47):
            c.put(x, y, WALL[2] if x < 45 else WALL[1], WALL)
    for x in range(34, 47):
        c.put(x, 39, WALL[3] if x < 45 else WALL[2], WALL); c.put(x, 38, TIMBER[0], TIMBER)
    stamp(c, 34, 37, "wheel", TIMBER)
    millrace(c, 30, 50, 47)
    for x in range(36, 46):                                       # 輪の下は水の中（水路の水を手前に重ねる）
        if c.get(x, 49) is not None:
            c.put(x, 49, LAKE[2]); c.put(x, 48, LAKE[3] if x % 3 else LAKE[2])
    for (x, y, col) in ((46, 47, WALL[3]), (47, 47, WALL[3]), (47, 46, LAKE[3]), (48, 47, LAKE[3]), (46, 48, WALL[3]),
                        (47, 48, LAKE[3]), (45, 46, WALL[3]), (49, 48, WALL[3])):
        c.put(x, y, col)                                          # 水しぶき（下流がわ）
    # わら屋根の家・赤い屋根の家
    house(c, 4, 26, 13, "hip", THATCH, door=8, wins=(2,), lit=(0,))
    house(c, 19, 19, 12, "front", ROOF, door=6, wins=(2,), lit=())
    house(c, 2, 60, 12, "side", THATCH, door=7, wins=(2,), chimney=8)
    house(c, 38, 62, 13, "hip", ROOF, door=8, wins=(2,), lit=(0,))
    tree(c, 9, 10, 5)
    tree(c, 54, 39, 4.4)
    tree(c, 28, 57, 4)
    c.shadow_edges()
    return c.save("icon-village")


def wheel(c, cx, cy, r=5):
    """水車: 木の輪（左上が明るい）と8本の羽根板"""
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d = math.hypot(dx, dy)
            if r - 1.3 <= d <= r + 0.2:
                c.put(x, y, TIMBER[2] if dx + dy < -1 else TIMBER[1] if dx + dy < 2 else TIMBER[0], TIMBER)
            elif d < r - 1.3:
                a = math.degrees(math.atan2(dy, dx)) % 45
                if a < 9 or a > 36:
                    c.put(x, y, TIMBER[0], TIMBER)
    c.put(cx, cy, TIMBER[2], TIMBER)


# ===================================================================== 岩・崖・小物（3〜10で使う）
SOFT_MATS = []


def soft(pal):
    """岩・葉の素材の色の並び（clean_soft の対象にするため、別のリストとして登録する）"""
    m = list(pal)
    SOFT_MATS.append(m)
    return m


def rock_mass(c, inside, box, pal=STONE, cell=6, seed=1, gap=None, tall=False):
    """山の地形と同じ「丸い岩の房」で、inside(x, y) の中をうめる。岩は格子を少しずらして置き、1つずつ左上が明るい。
    すき間はいちばん暗い色（山の地形と同じ）。乱数は岩の置き場所と大きさだけに使う"""
    import random
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    gap = gap or pal[1]                                         # すき間は暗い灰（いちばん暗い色だと、崖が黒っぽく重くなった）
    pal = soft(pal)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if inside(x, y):
                c.put(x, y, gap, pal)
    rocks = []
    row = 0
    for gy in range(y0 - 2, y1 + 3, int(cell * (1.15 if tall else 0.8))):
        off = (cell // 2) if row % 2 else 0
        for gx in range(x0 - 2 + off, x1 + 3, cell):
            rx, ry = cell * rnd.uniform(0.5, 0.62), cell * rnd.uniform(0.42, 0.52)
            if tall:
                rx, ry = rx * 0.78, ry * 1.5                    # 縦に長い岩（断崖の高さが出る）
            rocks.append((gx + rnd.uniform(-1.2, 1.2), gy + rnd.uniform(-1, 1), rx, ry))
        row += 1
    for (px_, py_, rx, ry) in sorted(rocks, key=lambda r: r[1]):
        # 山の地形（2026-10-05 にかきなおされた w-mountain）と同じ「角ばった岩」: 頂から左の面は明るく、右の面は暗い。
        # 左のふちは1段明るい線、すそは暗いすき間に消える
        h = ry * 2.0
        top = py_ - ry
        for y in range(int(top), int(py_ + ry) + 2):
            t = (y + 0.5 - top) / h
            if t <= 0 or t > 1:
                continue
            half = rx * t * 1.15
            for x in range(int(px_ - half) - 1, int(px_ + half) + 2):
                if not inside(x, y):
                    continue
                dx = x + 0.5 - px_
                if abs(dx) > half:
                    continue
                if dx < 0:
                    col = pal[4] if dx < -half + 1.2 and t < 0.85 else pal[3]
                else:
                    col = pal[2]
                if t > 0.86:
                    col = pal[1] if dx >= 0 else pal[2]
                c.put(x, y, col, pal)


def fence(c, x0, x1, y, pal=TIMBER):
    """柵: 横木1本と、3ドットごとの杭（杭は横木より1ドット高い）"""
    for x in range(x0, x1 + 1):
        c.put(x, y, pal[2], pal)
    for x in range(x0, x1 + 1, 3):
        c.put(x, y - 1, pal[2], pal); c.put(x, y + 1, pal[0], pal)


def reeds(c, x, y, pal=FOREST):
    """葦のかたまり: 高さのちがう3本（2〜4ドット）。先は明るい"""
    for (dx, h) in ((0, 3), (1, 4), (2, 2)):
        for k in range(h):
            c.put(x + dx, y - k, pal[3] if k == h - 1 else pal[2] if dx < 2 else pal[1], pal)


def well(c, x, y):
    """井戸: 石の丸いふち（上の面が見える）と、中の暗い水"""
    for (dx, dy, col) in ((1, 0, STONE[4]), (2, 0, STONE[4]), (0, 1, STONE[4]), (3, 1, STONE[3]), (0, 2, STONE[3]), (3, 2, STONE[2]),
                          (1, 3, STONE[2]), (2, 3, STONE[2]), (1, 1, SEA[1]), (2, 1, SEA[1]), (1, 2, SEA[2]), (2, 2, SEA[1])):
        c.put(x + dx, y + dy, col, STONE)
    for dx in range(4):
        c.put(x + dx, y + 4, STONE[1], STONE)


def flat_house(c, x0, yb, w, wh, depth, pal, door=None, wins=(), lit=(), ground="sand", parapet=True):
    """平屋根の土の家（上から見える屋上＋手前の壁）。屋上は明るく、ふちの低い手すり壁は1段明るい線、手前の壁はまん中、右は暗い"""
    x1 = x0 + w - 1
    yt = yb - wh - depth + 1
    cast(c, x0, x1, yt, yb, ground, dx=2, dy=1)
    for y in range(yt, yt + depth):
        for x in range(x0, x1 + 1):
            col = pal[3]
            if parapet and (y == yt or x == x0):
                col = pal[4]
            if x == x1:
                col = pal[2]
            c.put(x, y, col, pal)
    for y in range(yt + depth, yb + 1):
        for x in range(x0, x1 + 1):
            col = pal[2] if x < x1 else pal[1]
            if y == yt + depth:
                col = pal[1]                                    # 屋上のふちの下の影
            c.put(x, y, col, pal)
    for i, wx in enumerate(wins):
        on = i in lit
        c.put(x0 + wx, yt + depth + 2, LIGHT if on else pal[0], pal)
        c.put(x0 + wx, yt + depth + 3, LAMP if on else pal[0], pal)
    if door is not None:
        dx = x0 + door
        c.put(dx, yb - 2, pal[0], pal)
        for y in range(yb - 1, yb + 1):
            c.put(dx - 1, y, pal[0], pal); c.put(dx, y, pal[0], pal)


def dome(c, cx, yb, rx, ry, pal, mat=None):
    """丸屋根（左上が明るい。いちばん明るい色は左上の小さな光だけ）"""
    for y in range(int(yb - ry) - 1, yb + 1):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - yb) / ry
            d = u * u + v * v
            if d > 1:
                continue
            s = u * 0.7 + v * 0.6
            col = pal[4] if (s < -0.62 and d < 0.75) else pal[3] if s < -0.1 else pal[2] if s < 0.45 else pal[1]
            c.put(x, y, col, mat or pal)


def palm(c, x0, ytop, ybot, pal=FOREST):
    """やし: 少し曲がった幹（ふしの明るい線）と、5枚の葉（上は明るく、下は暗い）"""
    for y in range(ytop, ybot + 1):
        t = (y - ytop) / max(1, ybot - ytop)
        x = x0 - round((1 - t) ** 2 * 2)
        c.put(x, y, TIMBER[2] if (y - ytop) % 3 else DIRT[4], TIMBER); c.put(x + 1, y, TIMBER[1], TIMBER)
    for (ang, ln) in ((-2.9, 7), (-2.3, 6), (-0.8, 6), (-0.2, 7), (-1.6, 4)):
        for k in range(1, ln + 1):
            x = x0 - 1.5 + 0.5 + math.cos(ang) * k
            y = ytop - 1 + math.sin(ang) * k * 0.6 + (k / ln) ** 2 * 3.5
            c.put(x, y, pal[3] if k < ln * 0.6 else pal[2], pal[1:])
            c.put(x, y + 1, pal[2] if k < ln * 0.6 else pal[1], pal[1:])
    c.put(x0 - 1, ytop - 1, pal[4], pal[1:]); c.put(x0, ytop - 1, pal[3], pal[1:])


def smoke(c, x, y):
    """えんとつのけむり: 上へ小さくなる3つの丸いかたまり（右へ流れる）"""
    puff(c, x + 0.5, y - 1.5, 2.0)
    puff(c, x + 2.5, y - 5, 2.4)
    puff(c, x + 5.5, y - 8.5, 2.0)


# ===================================================================== 3) 霧間の集落（雪原の山あい・霧）
SLATE_SNOW = SLATE
TIMBER_WALL = [TIMBER[0], TIMBER[1], TIMBER[2], DIRT[3]]


def icon_village_mist():
    c = Canvas()
    g = "snow"
    skirt(c, 32, 38, 30, 25, g)
    # 奥の岩の尾根（山の地形と同じ岩の房。上に雪）
    rtop = lambda x: min(5 + 0.085 * (x - 17) ** 2, 8 + 0.085 * (x - 46) ** 2, 24)   # 2つの峰と、そのあいだの鞍部（霧間）
    ridge = lambda x, y: y >= rtop(x) and y <= 26 and 4 <= x <= 60
    rock_mass(c, ridge, (4, 4, 60, 26), cell=6, seed=4)
    for x in range(4, 61):                                         # 峰の雪（上ほど厚い）
        t = int(math.ceil(rtop(x)))
        dep = 4 if t < 9 else 2 if t < 15 else 1
        for k in range(dep):
            if c.get(x, t + k) is not None:
                c.put(x, t + k, SNOW[5] if k < dep - 1 or dep == 1 else SNOW[3], SNOW)
    # 踏まれた雪の道
    path(c, [(30, 63), (30, 50), (24, 42), (34, 34)], w=3, pal=[None, SNOW[2], SNOW[3], None])
    # 針葉樹（雪の森と同じ）
    for (x, yb, h) in ((8, 36, 13), (55, 34, 14), (7, 56, 11), (56, 57, 12), (47, 46, 10)):
        pine(c, x, yb, h)
    # 家（木の壁・青い石板の屋根に雪・灯）
    house(c, 11, 34, 13, "side", SLATE, TIMBER_WALL, door=9, wins=(2,), lit=(0,), chimney=3, snow=True, ground=g)
    house(c, 35, 32, 12, "front", SLATE, TIMBER_WALL, door=6, wins=(2,), lit=(0,), snow=True, ground=g)
    house(c, 15, 52, 13, "hip", SLATE, TIMBER_WALL, door=8, wins=(2,), lit=(0,), snow=True, ground=g)
    house(c, 36, 58, 11, "side", SLATE, TIMBER_WALL, door=6, wins=(2,), snow=True, ground=g)
    smoke(c, 14, 17)
    # 霧の帯（家のあいだを横に流れる、青みの灰色の丸いかたまり。雪の白とは別の色）
    for (x, y, r) in ((5, 41, 2.6), (9, 42, 3.0), (13, 41.5, 2.4), (48, 39, 2.6), (52, 40, 3.0), (57, 39.5, 2.6),
                      (27, 62, 2.4), (31, 61.5, 2.8)):
        puff(c, x, y, r, MIST_SNOW)
    c.shadow_edges()
    return c.save("icon-village-mist")


# ===================================================================== 4) 硝子湖（湖にうかぶ交易の町）
def isle_stone(c, cx, cy, rx, ry, depth=2):
    """石を積んだ島: 上の面（明るい石・まわりは1段暗いふち石）＋手前の石垣（depth 行）"""
    for y in range(int(cy - ry) - 1, int(cy + ry) + depth + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            u = (x + 0.5 - cx) / rx
            v = (y + 0.5 - cy) / ry
            vb = (y - depth + 0.5 - cy) / ry
            if u * u + v * v <= 1:
                d = u * u + v * v
                c.put(x, y, STONE[3] if d > 0.72 else STONE[4], STONE)
            elif u * u + vb * vb <= 1 and y > cy:
                c.put(x, y, STONE[2] if u < 0.45 else STONE[1], STONE)


def glass_dome(c, cx, yb, r):
    """ガラスの丸屋根: 3段の水色。左上に白い光、骨組みの線（縦2本）"""
    for y in range(int(yb - r), yb + 1):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u, v = (x + 0.5 - cx) / r, (y + 0.5 - yb) / r
            d = u * u + v * v
            if d > 1:
                continue
            s = u * 0.7 + v * 0.5
            col = GLOW[2] if (s < -0.55 and d < 0.7) else GLOW[1] if s < 0.2 else GLOW[0]
            if abs(x + 0.5 - cx) < 0.6 and y < yb - 1:
                col = GLOW[0] if s > 0 else SLATE[1]
            c.put(x, y, col, GLOW)
    for x in range(int(cx - r), int(cx + r) + 1):
        c.put(x, yb + 1, WALL[1] if x < cx + r - 1 else WALL[0], WALL)


def icon_lake():
    c = Canvas()
    g = "grass"
    skirt(c, 32, 40, 29, 24, g)
    water_ell(c, 32, 45, 27, 16, LAKE, rim=(SAND[2], SAND[1]), rim_w=1.8)
    for (x, y, n) in ((11, 48, 3), (48, 36, 4), (52, 55, 3), (26, 57, 4)):
        wave_dash(c, x, y, n, LAKE[3])
    for (x, y) in ((6, 40), (52, 36), (51, 47)):
        stamp(c, x, y, "reeds", FOREST)
    # 島と橋
    isle_stone(c, 21, 40, 13, 7, 3)
    isle_stone(c, 45, 47, 10, 6, 3)
    for x in range(33, 37):                                       # 島と島の橋
        for y in (44, 45):
            c.put(x, y, DIRT[4] if y == 44 else DIRT[2], DIRT)
        c.put(x, 46, TIMBER[0], TIMBER)
    for y in range(49, 62):                                       # 岸への橋（南の門へ）
        for x in (20, 21, 22):
            c.put(x, y, DIRT[4] if x < 22 else DIRT[2], DIRT)
        c.put(23, y, TIMBER[0], TIMBER)
    # 交易の塔（細く高い。石板の寄棟、明かりの窓）
    for y in range(20, 40):
        for x in range(23, 28):
            c.put(x, y, WALL[3] if x < 25 else WALL[2] if x < 27 else WALL[1], WALL)
    for y in (24, 25, 30, 31):
        c.put(25, y, LIGHT if y < 26 else GLASS, WALL)
    hip_roof(c, 22, 28, 15, 19, SLATE)
    c.put(25, 14, GOLD[1])
    house(c, 10, 41, 12, "hip", ROOF, door=8, wins=(2,), lit=(0,), shadow=False)
    house(c, 29, 40, 7, "side", ROOF, door=None, wins=(2,), wh=4, shadow=False)
    # ガラスの丸屋根（目じるし）
    stamp(c, 38, 38, "glassdome", GLOW)
    house(c, 50, 50, 6, "side", ROOF, wh=4, door=2, shadow=False)
    boat(c, 9, 55, 6)
    boat(c, 50, 36, 6, sail=5)
    tree(c, 10, 23, 5)
    tree(c, 54, 24, 4.6)
    c.shadow_edges()
    return c.save("icon-lake")


# ===================================================================== 5) 鉄鏈鉱山（山の斜面の段々の町）
def terrace(c, x0, x1, y, h=3):
    """段々の石垣: 上のふち1行（明るい）＋手前の石の面。石は大きな塊を少し（目地は横の線だけ。レンガにしない）"""
    for x in range(x0, x1 + 1):
        c.put(x, y, STONE[4] if x < x1 else STONE[3], STONE)
    for y2 in range(y + 1, y + h + 1):
        for x in range(x0, x1 + 1):
            col = STONE[3] if x < x1 else STONE[1]
            if y2 == y + h:
                col = STONE[2] if x < x1 else STONE[1]
            c.put(x, y2, col, STONE)
    for x in range(x0 + 3, x1 - 1, 7):                            # 大きな石の継ぎ目（短い縦線をまばらに）
        c.put(x, y + 1 + (x // 7) % max(1, h - 1), STONE[2], STONE)


def rails(c, pts):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = max(abs(xb - xa), abs(yb - ya))
        for k in range(n + 1):
            x = round(xa + (xb - xa) * k / n)
            y = round(ya + (yb - ya) * k / n)
            c.put(x, y, STONE[1], STONE)
            c.put(x, y + 1, TIMBER[1], TIMBER)
            c.put(x, y + 2, STONE[1], STONE)


def icon_mine():
    c = Canvas()
    g = "grass"
    skirt(c, 30, 38, 30, 26, g)
    # 右上の岩山（山の地形と同じ角ばった岩）
    slope = lambda x, y: y >= max(1, 26 - (x - 22) * 0.9) and y <= 20 and x <= 60
    rock_mass(c, slope, (20, 0, 60, 20), cell=7, seed=9)
    # 坑口（木の枠: 2本の柱とはり。中は奥ほど暗い）
    for y in range(9, 21):
        for x in range(44, 52):
            c.put(x, y, STONE[0] if y > 11 else STONE[1], STONE)
    for y in range(8, 21):
        c.put(43, y, TIMBER[2], TIMBER); c.put(44, y, TIMBER[1], TIMBER)
        c.put(51, y, TIMBER[1], TIMBER); c.put(52, y, TIMBER[0], TIMBER)
    for x in range(42, 54):
        c.put(x, 7, DIRT[4] if x < 52 else TIMBER[1], TIMBER); c.put(x, 8, TIMBER[1], TIMBER)
    c.put(41, 10, LIGHT); c.put(41, 11, LAMP)                      # ランプ
    # 段々（右上→左下）
    terrace(c, 22, 60, 28, h=3)
    terrace(c, 8, 40, 41, h=3)
    terrace(c, 1, 22, 55, h=3)
    # レール（坑口から手前へ。遠近）と、坑口から出てくるトロッコ
    track(c, 48, 12, 27, 2, 8)
    stamp(c, 43, 15, "minecart", STONE)
    # 上の段: かじ場（開いた口の火）とえんとつ＋けむり
    house(c, 24, 22, 14, "side", SLATE, door=None, wins=(), wh=5, chimney=10)
    for (x, y, col) in ((29, 20, FIRE[0]), (30, 20, FIRE[1]), (31, 20, FIRE[0]), (29, 21, FIRE[1]), (30, 21, LIGHT), (31, 21, FIRE[1]),
                        (28, 20, TIMBER[0]), (28, 21, TIMBER[0]), (32, 20, TIMBER[0]), (32, 21, TIMBER[0]), (29, 22, FIRE[0]), (30, 22, FIRE[0]), (31, 22, FIRE[0])):
        c.put(x, y, col, WALL)
    smoke(c, 35, 8)
    # 中の段: 家とかじ場
    house(c, 10, 39, 12, "hip", ROOF, door=8, wins=(2,), lit=(0,))
    house(c, 24, 39, 13, "side", SLATE, door=9, wins=(2,), lit=(), chimney=3)
    for (x, y, col) in ((31, 37, FIRE[1]), (32, 37, LIGHT), (31, 38, FIRE[0]), (32, 38, FIRE[1])):
        c.put(x, y, col, WALL)
    # 下の段: 長屋
    house(c, 2, 53, 18, "side", ROOF, door=13, wins=(2, 6, 9), lit=(1,), chimney=5)
    path(c, [(22, 63), (20, 59)], w=3)
    path(c, [(40, 45), (42, 54), (36, 60)], w=3)
    tree(c, 52, 50, 5)
    tree(c, 7, 33, 4.4)
    c.shadow_edges()
    return c.save("icon-mine")


# ===================================================================== 6) 砂音（砂漠の隊商都市）
ADOBE = ["#6e5228", "#8a6a36", "#b89058", "#d4ae72", "#e8c88a"]


def icon_tents():
    c = Canvas()
    g = "sand"
    skirt(c, 32, 38, 30, 25, g)
    for (x0, yb, w, wh, dp, door, wins, lit) in ((3, 27, 13, 6, 5, 8, (3,), ()), (16, 22, 10, 7, 4, 5, (2,), (0,)),
                                                (40, 22, 11, 7, 5, 6, (2,), ()), (50, 30, 10, 6, 4, 3, (7,), ()),
                                                (3, 45, 12, 6, 5, 7, (3,), ()), (48, 47, 12, 6, 5, 3, (8,), (0,))):
        adobe_house(c, x0, yb, w, wh, dp, door=door, wins=wins, lit=lit)
    # まん中の隊商宿（目じるし: 赤茶の丸屋根）: 段の手すり壁・アーチの門と窓・丸屋根の下の窓のある胴・金のてっぺん
    cast(c, 19, 45, 25, 45, g, dx=2, dy=1)
    for y in range(31, 46):
        for x in range(19, 46):
            col = ADOBE[3] if x < 45 else ADOBE[2]
            if y == 31:
                col = ADOBE[4] if x < 45 else ADOBE[3]             # 屋上のふち
            elif y == 32:
                col = ADOBE[2] if x < 45 else ADOBE[1]
            c.put(x, y, col, ADOBE)
    for x in range(19, 46, 4):                                     # 段になった手すり壁の飾り（2ドットの山）
        c.put(x, 30, ADOBE[4], ADOBE); c.put(x + 1, 30, ADOBE[3], ADOBE)
    for x in range(20, 45, 3):                                     # 梁の先
        c.put(x, 33, TIMBER[2], TIMBER); c.put(x, 34, ADOBE[1], ADOBE)
    for y in range(26, 31):                                        # 丸屋根の下の胴（小さな窓）
        for x in range(25, 40):
            c.put(x, y, ADOBE[3] if x < 38 else ADOBE[2], ADOBE)
    for x in (27, 30, 34, 37):
        c.put(x, 28, ADOBE[0], ADOBE); c.put(x, 29, ADOBE[0], ADOBE)
    dome(c, 32, 26, 9, 9, ROOF)
    c.put(32, 16, GOLD[1]); c.put(32, 15, GOLD[1]); c.put(31, 17, GOLD[0]); c.put(33, 17, GOLD[0])
    stamp(c, 29, 38, "archgate", ADOBE)
    for wx in (22, 40):
        stamp(c, wx, 37, "archwin", ADOBE)
    # 手前の市（しまの日よけ）と井戸、やし
    awning(c, 14, 24, 53)
    awning(c, 36, 46, 55, cols=(SLATE[3], WALL[3]), dark=(SLATE[1], WALL[1]))
    well(c, 28, 54)
    palm(c, 56, 51, 62)
    palm(c, 10, 51, 61)
    c.shadow_edges()
    return c.save("icon-tents")


# ===================================================================== 7) 草の上の野営地（砂守のいずみ・荒野の市）
CREAM = [WALL[0], WALL[1], WALL[2], WALL[3], "#f8f2de"]


def dome_tent(c, cx, yb, rx, ry, cloth, ground="grass"):
    ell_shadow(c, cx + 2, yb + 1, rx + 1, 2.2, ground)
    dome(c, cx, yb, rx, ry, cloth)
    for side in (-1, 1):                                          # 縫い目（左右に1本ずつ、丸屋根の弧にそう）
        for y in range(int(yb - ry) + 2, yb + 1):
            t = (y + 0.5 - (yb - ry)) / ry
            x = cx + side * rx * 0.55 * math.sqrt(max(0.0, t * (2 - t)))
            cur = c.get(int(x), y)
            if cur in cloth:
                c.put(x, y, cloth[max(1, cloth.index(cur) - 1)], cloth)
    for x in range(int(cx - rx) + 1, int(cx + rx)):                # すその帯（地面に近い1行、1段暗い）
        cur = c.get(x, yb - 1)
        if cur in cloth:
            c.put(x, yb - 1, cloth[max(1, cloth.index(cur) - 1)], cloth)
    for y in range(yb - 3, yb + 1):                                # 入口のたれ幕（暗いすき間）
        c.put(cx, y, TIMBER[0], cloth)
        c.put(cx + 1, y, TIMBER[0] if y > yb - 3 else cloth[1], cloth)
    c.put(cx - 1, yb, cloth[3], cloth)
    c.put(cx, int(yb - ry) - 1, TIMBER[1], cloth); c.put(cx, int(yb - ry) - 2, ROOF[3], cloth)


def icon_tents_grass():
    c = Canvas()
    g = "grass"
    skirt(c, 32, 40, 30, 22, g)
    water_ell(c, 46, 52, 11, 6, LAKE, rim=(SAND[2], SAND[1]), rim_w=1.5)
    wave_dash(c, 42, 51, 3, LAKE[3])
    reeds(c, 55, 50); reeds(c, 36, 55)
    dome_tent(c, 18, 38, 12, 11, ROOF)
    dome_tent(c, 38, 32, 8, 8, CREAM)
    dome_tent(c, 50, 38, 6, 6, ROOF)
    awning(c, 4, 15, 50)
    awning(c, 19, 30, 54, cols=(SLATE[3], WALL[3]), dark=(SLATE[1], WALL[1]))
    # たき火（石の輪・まき・火）とけむり
    for (x, y, col) in ((31, 45, STONE[3]), (34, 45, STONE[2]), (32, 46, TIMBER[1]), (33, 46, TIMBER[0]),
                        (32, 44, FIRE[1]), (33, 44, FIRE[0]), (32, 43, LIGHT), (33, 45, FIRE[0]), (32, 45, FIRE[1])):
        c.put(x, y, col, STONE)
    puff(c, 33.5, 39.5, 2.3); puff(c, 35.5, 35.0, 2.7)            # けむりは火のま上から、2つのかたまりだけ
    palm(c, 56, 22, 36)
    tree(c, 8, 24, 4.6)
    c.shadow_edges()
    return c.save("icon-tents-grass")


# ===================================================================== 8) 霧断崖（断崖にはりつく古い宗教都市）
WHITE = [WALL[0], WALL[1], WALL[2], WALL[3]]


def cliff(c, x0, x1, ytop_fn, ybot, ledges, seed=3):
    """断崖: 上のふちは岩の房、面は「岩だな（明るい上の面1〜2行）」と「縦の面（縦の割れ目）」の段。
    段ごとに少しずつ奥へ下がる。割れ目は決まった間かくより少しずらした場所に、2〜5ドットの縦線で"""
    import random
    rnd = random.Random(seed)
    for x in range(x0, x1 + 1):
        top = int(ytop_fn(x))
        for y in range(top, ybot + 1):
            col = STONE[3] if x < x1 - 1 else STONE[1]
            c.put(x, y, col, STONE)
    for (ly, lx0, lx1) in ledges:                                  # 岩だな
        for x in range(lx0, lx1 + 1):
            c.put(x, ly, STONE[5] if x < lx1 else STONE[4], STONE)
            c.put(x, ly + 1, STONE[4] if x < lx1 else STONE[3], STONE)
            c.put(x, ly - 1, STONE[1], STONE)                     # たなの上の面の奥の影
    ys = sorted([int(ytop_fn(x)) for x in range(x0, x1 + 1)])
    x = x0 + 3
    while x < x1 - 2:                                              # 縦の割れ目（左どなりを1段明るく）
        y0 = int(ytop_fn(x)) + rnd.randint(3, 6)
        n = rnd.randint(3, 6)
        for y in range(y0, min(ybot, y0 + n)):
            if c.get(x, y) == STONE[3]:
                c.put(x, y, STONE[2], STONE)
                if c.get(x - 1, y) == STONE[3]:
                    c.put(x - 1, y, STONE[4], STONE)
        x += rnd.randint(5, 8)
    for x in range(x0, x1 + 1):                                    # 上のふち（雪のように明るい岩のへり）
        top = int(ytop_fn(x))
        c.put(x, top, STONE[4] if x < x1 - 1 else STONE[3], STONE)


def icon_temple():
    """横に長い断崖（縦に長い岩の房で高さを出す）。岩だなに白い家、崖の上に環のしるしの堂、すそに霧と家"""
    c = Canvas()
    g = "grass"
    skirt(c, 32, 40, 30, 24, g)
    top = lambda x: 13 + 2.0 * math.sin(x / 4.0) + (0 if 20 <= x <= 44 else 3) + (2 if x < 6 or x > 57 else 0)
    face = lambda x, y: top(x) <= y <= 45 - (2 if x < 5 or x > 58 else 0) and 2 <= x <= 61
    rock_mass(c, face, (2, 8, 61, 45), cell=6, seed=12, tall=True)
    for x in range(2, 62):                                         # 崖の上のへり（草）
        t = int(math.ceil(top(x)))
        if c.get(x, t) is not None:
            c.put(x, t, GRASS[3], GRASS); c.put(x, t + 1, GRASS[1], GRASS)
    for (ly, lx0, lx1) in [(23, 3, 18), (29, 41, 60), (35, 15, 34), (41, 3, 22)]:   # 岩だな（上の面2行・下に影1行）
        for x in range(lx0, lx1 + 1):
            c.put(x, ly - 1, STONE[4] if x < lx1 else STONE[3], STONE)
            c.put(x, ly, STONE[3] if x < lx1 else STONE[2], STONE)
            c.put(x, ly + 1, STONE[0], STONE)
    house(c, 4, 21, 11, "side", SLATE, WHITE, door=7, wins=(2,), lit=(0,), wh=4, shadow=False)
    house(c, 44, 27, 12, "hip", SLATE, WHITE, door=8, wins=(2,), wh=4, shadow=False)
    house(c, 18, 33, 11, "front", SLATE, WHITE, door=6, wins=(2,), lit=(0,), wh=4, shadow=False)
    house(c, 6, 39, 10, "side", SLATE, WHITE, door=6, wins=(2,), wh=4, shadow=False)
    # 崖の上の堂（白い壁・石板の寄棟・金の環のしるし）
    house(c, 24, 13, 16, "hip", SLATE, WHITE, door=7, wins=(2, 11), lit=(0, 1), rh=6, wh=4, shadow=False)
    ring = [".oo.", "o..o", "o..o", ".oo."]
    for j, r in enumerate(ring):
        for i, ch in enumerate(r):
            if ch == "o":
                c.put(30 + i, j, GOLD[1] if i + j < 4 else GOLD[0])
    # つづら折りの石段（崖の上からすそまで）
    stair = [(40, 10, 40, 22), (40, 22, 36, 26), (36, 26, 36, 33), (36, 37, 40, 40), (40, 40, 40, 45)]
    for (xa, ya, xb, yb) in stair:
        n = max(abs(xb - xa), abs(yb - ya))
        for k in range(n + 1):
            x = round(xa + (xb - xa) * k / n); y = round(ya + (yb - ya) * k / n)
            c.put(x, y, STONE[5], STONE); c.put(x + 1, y, STONE[4], STONE)
    # すその家と霧
    house(c, 44, 57, 13, "side", SLATE, WHITE, door=9, wins=(2,), lit=(0,))
    house(c, 14, 59, 12, "hip", SLATE, WHITE, door=8, wins=(2,))
    path(c, [(40, 46), (36, 53), (32, 63)], w=3)
    for (x, y, r) in ((5, 47, 2.6), (10, 48, 3.0), (15, 47, 2.4), (20, 48, 2.6), (49, 46, 2.6), (54, 47, 3.0), (59, 46.5, 2.6)):
        puff(c, x, y, r, MIST)
    c.shadow_edges()
    return c.save("icon-temple")


# ===================================================================== 9) 雪の町（霜原・雪待ちの小屋町）
def icon_snowtown():
    c = Canvas()
    g = "snow"
    skirt(c, 32, 38, 30, 25, g)
    path(c, [(32, 63), (32, 46), (26, 38), (30, 30)], w=4, pal=[None, SNOW[2], SNOW[3], None])
    # 見張りの塔（古戦場のなごり。石の塔、上の段の胸壁、かがり火＝目じるし）
    for y in range(11, 37):
        for x in range(28, 36):
            col = STONE[4] if x < 30 else STONE[3] if x < 34 else STONE[2]
            if x == 35:
                col = STONE[1]
            c.put(x, y, col, STONE)
    for y in (16, 22, 28):                                         # 段の線（3段だけ）
        for x in range(28, 36):
            c.put(x, y, STONE[2] if x < 34 else STONE[1], STONE)
    for (y, x) in ((19, 31), (25, 32)):
        c.put(x, y, GLASS, STONE); c.put(x, y + 1, GLASS, STONE)
    c.put(31, 31, LIGHT, STONE); c.put(31, 32, LAMP, STONE)
    for y in range(33, 37):
        c.put(32, y, TIMBER[0], STONE); c.put(33, y, TIMBER[0], STONE)
    for x in range(26, 38):                                        # 張り出した上の段と胸壁
        c.put(x, 9, STONE[4] if x < 36 else STONE[3], STONE)
        c.put(x, 10, STONE[2] if x < 36 else STONE[1], STONE)
        if (x - 26) % 3 == 0:
            c.put(x, 8, STONE[4], STONE); c.put(x + 1, 8, STONE[3], STONE)
    for (x, y, col) in ((31, 7, FIRE[0]), (32, 7, FIRE[0]), (33, 7, FIRE[0]), (31, 6, FIRE[1]), (32, 6, LIGHT), (33, 6, FIRE[1]),
                        (32, 5, FIRE[1]), (32, 4, LIGHT), (31, 5, FIRE[0])):
        c.put(x, y, col)
    # 家（木の壁・雪の屋根・明かり・えんとつ）
    house(c, 4, 22, 14, "side", ROOF, TIMBER_WALL, door=10, wins=(2,), lit=(0,), chimney=4, snow=True, ground=g)
    house(c, 41, 21, 13, "front", SLATE, TIMBER_WALL, door=7, wins=(2,), lit=(0,), snow=True, ground=g)
    house(c, 4, 42, 13, "hip", SLATE, TIMBER_WALL, door=8, wins=(2,), snow=True, ground=g)
    house(c, 41, 42, 15, "side", ROOF, TIMBER_WALL, door=10, wins=(2, 6), lit=(1,), chimney=10, snow=True, ground=g)
    house(c, 17, 59, 12, "front", ROOF, TIMBER_WALL, door=6, wins=(2,), lit=(0,), snow=True, ground=g)
    smoke(c, 7, 9)
    for (x, yb, h) in ((56, 32, 13), (22, 30, 10), (56, 61, 12), (7, 59, 11), (39, 61, 9)):
        pine(c, x, yb, h)
    c.shadow_edges()
    return c.save("icon-snowtown")


# ===================================================================== 10) 浮嶼（雲の上の浮島群）
def floating_isle(c, cx, cy, rx, depth, seed=1):
    """浮島: 草の上の面（だ円）＋下へ細くなる岩の底（地層の段2本、左が明るい）"""
    ry = rx * 0.36
    for y in range(int(cy), int(cy + depth) + 1):
        t = (y - cy) / depth
        half = rx * (1 - t ** 1.3) * (1 - 0.2 * t)
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            u = (x + 0.5 - cx) / max(0.7, half)
            if abs(u) > 1:
                continue
            col = STONE[3] if u < -0.35 else STONE[2] if u < 0.45 else STONE[1]
            if int(y - cy) % 5 == 4 and abs(u) < 0.9:                 # 地層の段（横の線）
                col = STONE[2] if u < -0.35 else STONE[1] if u < 0.45 else STONE[0]
            c.put(x, y, col, STONE)
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            d = u * u + v * v
            if d <= 1:
                col = GRASS[3]
                if v > 0.55 or (d > 0.75 and u > 0.3):
                    col = GRASS[1]
                elif d > 0.72 and u < -0.2 and v < 0.3:
                    col = GRASS[4]
                c.put(x, y, col, GRASS)
    for x in range(int(cx - rx) + 1, int(cx + rx)):                # 草のへりの下の土
        y = int(cy + ry * math.sqrt(max(0, 1 - ((x + 0.5 - cx) / rx) ** 2))) + 1
        if c.get(x, y) in STONE:
            c.put(x, y, DIRT[1], STONE)


def icon_sky():
    c = Canvas()
    floating_isle(c, 20, 26, 17, 24, seed=3)
    floating_isle(c, 48, 18, 12, 18, seed=5)
    floating_isle(c, 45, 44, 10, 14, seed=7)
    house(c, 9, 27, 14, "side", ROOF, door=9, wins=(2,), lit=(0,), chimney=3, shadow=False)
    house(c, 22, 26, 9, "front", ROOF, door=4, wins=(), shadow=False)
    house(c, 41, 18, 12, "hip", ROOF, door=8, wins=(2,), lit=(0,), shadow=False)
    # 見張りの小塔
    for y in range(31, 45):
        for x in range(43, 48):
            c.put(x, y, WALL[3] if x < 45 else WALL[2] if x < 47 else WALL[1], WALL)
    c.put(45, 35, LIGHT, WALL); c.put(45, 36, LAMP, WALL)
    hip_roof(c, 42, 48, 27, 30, SLATE)
    # つり橋（2つの島のあいだ。たるむ板と綱）
    for x in range(34, 40):
        t = (x - 34) / 5
        y = 24 + int(round(math.sin(t * math.pi) * 1.6))
        c.put(x, y, DIRT[4] if x % 2 else DIRT[2], DIRT); c.put(x, y + 1, TIMBER[0], TIMBER)
        c.put(x, y - 2, TIMBER[1], TIMBER) if x in (34, 39) else None
    tree(c, 28, 20, 4.4, shadow=False)
    tree(c, 55, 13, 3.8, shadow=False)
    c.shadow_edges()
    return c.save("icon-sky", trim=False)


# ===================================================================== 11・12) お城と宮殿（3回目の作り方: 家族のパレット・黒に近い縁。影はまったくつけない）
from study3 import MASTER as M                                         # noqa: E402  3回目の家族のパレット

OUT = M["o"]
HOLE = M["k"]
CS = [OUT, M["a"], M["b"], M["c"], M["d"]]                           # 石（あたたかい灰）
CT = [OUT, M["A"], M["B"], M["C"], M["D"]]                           # 青緑の屋根
CL = [OUT, M["I"], M["J"], M["K"], M["N"]]                           # 葉
CR = [OUT, M["E"], M["F"], M["G"], M["H"]]                           # 赤い布
CD = [OUT, M["p"], M["q"], M["r"], M["s"]]                           # 暗いむらさきの石
CG = [M["g"], M["h"]]                                                # 金
CLT = [M["L"], M["M"]]                                               # 灯
CV = [M["W"], M["Y"]]                                                # むらさきの光


def face(c, x0, x1, y0, y1, pal, v=3, course=3, quoin=True, right_dark=True):
    """手前の石の面: 1色の面に、3行ごとの横の目地（1段暗い）だけ。縦の目地は入れない（レンガに見える）。
    左右の角だけ、段ごとに互いちがいの大きな角石（左は明るく、右は暗く）"""
    for y in range(y0, y1 + 1):
        r = y - y0
        for x in range(x0, x1 + 1):
            col = pal[v]
            if r % course == course - 1:
                col = pal[v - 1]
            if quoin and r % course != course - 1:
                blk = (r // course) % 2
                if x < x0 + 2 + blk:
                    col = pal[min(4, v + 1)]
                if right_dark and x > x1 - 2 - blk:
                    col = pal[v - 1]
            c.put(x, y, col, pal)


def top(c, x0, x1, y0, y1, pal, v=4):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c.put(x, y, pal[v] if x < x1 - (x1 - x0) // 5 else pal[v - 1], pal)


def crenel(c, x0, x1, y, pal, period=4):
    """胸壁の歯: 2ドットの歯（上の面は明るく、手前は中）と2ドットのすき間"""
    for x in range(x0, x1 + 1):
        if (x - x0) % period < period // 2:
            c.put(x, y - 2, pal[4], pal); c.put(x, y - 1, pal[3], pal)


def round_tower(c, cx, r, ytop, ybot, pal, slits=()):
    """丸い塔の胴: 左が明るく右が暗い（4段）。下のふちは だ円の弧。3行ごとの横の目地は弧にそって下がる"""
    ry = r * 0.36
    for y in range(int(ytop), int(ybot + ry) + 1):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u = (x + 0.5 - cx) / r
            if abs(u) > 1:
                continue
            bow = ry * math.sqrt(1 - u * u)
            if y + 0.5 > ybot + bow:
                continue
            i = 4 if u < -0.55 else 3 if u < 0.15 else 2 if u < 0.65 else 1
            if int(y - bow - ytop) % 3 == 2 and i > 1:
                i -= 1
            c.put(x, y, pal[i], pal)
    for (sy) in slits:
        c.put(cx - 1, sy, HOLE, pal); c.put(cx - 1, sy + 1, HOLE, pal); c.put(cx - 1, sy + 2, HOLE, pal)


def cone_roof(c, cx, ybase, r, h, pal):
    """とんがり屋根: 左が明るく右が暗い。すそは だ円の弧。3行ごとに瓦の段（1段暗い）。軒は暗い"""
    ry = r * 0.36
    for y in range(int(ybase - h), int(ybase + ry) + 1):
        t = (y + 0.5 - (ybase - h)) / h
        rr = r * min(1.0, t)
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            if rr < 0.5:
                if abs(x + 0.5 - cx) < 0.6:
                    c.put(x, y, pal[3], pal)
                continue
            u = (x + 0.5 - cx) / rr
            if abs(u) > 1:
                continue
            bow = ry * math.sqrt(1 - u * u) * min(1.0, t)
            if y + 0.5 > ybase + bow:
                continue
            i = 4 if u < -0.45 else 3 if u < 0.2 else 2 if u < 0.7 else 1
            if t > 0.3 and int(y - bow) % 3 == 0 and i > 1:
                i -= 1
            if y + 1.5 > ybase + bow:
                i = 1
            c.put(x, y, pal[i], pal)


def flat_top(c, cx, cy, r, pal):
    """平らな屋上（だ円）と、まわりの胸壁の歯。中の床は奥の影で暗い"""
    ry = r * 0.36
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u, v = (x + 0.5 - cx) / r, (y + 0.5 - cy) / ry
            d = u * u + v * v
            if d > 1:
                continue
            c.put(x, y, pal[4] if d > 0.45 and u < 0.4 else pal[3] if d > 0.45 else pal[2], pal)
    for k in range(-2, 3):
        x = cx + k * r * 0.42
        y = cy + ry * 0.9 * math.sqrt(max(0, 1 - (k * 0.42) ** 2))
        c.put(x - 0.5, y - 1, pal[4] if k < 1 else pal[3], pal); c.put(x + 0.5, y - 1, pal[4] if k < 0 else pal[3], pal)
        c.put(x - 0.5, y, pal[3] if k < 1 else pal[2], pal); c.put(x + 0.5, y, pal[2], pal)


def banner(c, x, y0, n, pal=CR):
    for y in range(y0, y0 + n):
        c.put(x, y, pal[3], pal); c.put(x + 1, y, pal[2], pal)
    c.put(x, y0 + n, pal[2], pal)
    c.put(x, y0 + 2, CG[1], pal)


def flag(c, x, ytop, pal=CR):
    for y in range(ytop, ytop + 4):
        c.put(x, y, M["w"], CS)
    for (dx, dy, i) in ((1, 0, 3), (2, 0, 3), (3, 0, 2), (1, 1, 3), (2, 1, 2), (3, 1, 2), (4, 1, 1)):
        c.put(x + dx, ytop + dy, pal[i], pal)


def icon_castle():
    c = Canvas()
    # 奥の壁（上の面＋胸壁＋中庭がわの面）
    top(c, 9, 54, 13, 14, CS)
    crenel(c, 9, 54, 13, CS)
    face(c, 9, 54, 15, 17, CS, v=2, quoin=False)
    # 中庭（石だたみは2色の大きな区画だけ。天守への道は明るい）
    for y in range(18, 44):
        for x in range(10, 54):
            c.put(x, y, CS[2] if y < 20 else CS[3], CS)
    for y in range(26, 44):
        for x in range(28, 36):
            c.put(x, y, CS[4] if x < 34 else CS[3], CS)
    for (tx, ty) in ((16, 35), (47, 35)):
        tree(c, tx, ty, 3.6, pal=CL, shadow=False, trunk=1)
    # 壁ぞいの長屋（兵舎と馬屋。青緑の片流れ屋根）と井戸
    for (bx0, bx1) in ((10, 17), (46, 53)):
        for y in range(19, 24):
            for x in range(bx0, bx1 + 1):
                c.put(x, y, CT[3] if (y - 19) % 2 == 0 else CT[2], CT)
        for x in range(bx0, bx1 + 1):
            c.put(x, 24, CT[1], CT)
        for y in range(25, 29):
            for x in range(bx0, bx1 + 1):
                c.put(x, y, CS[3] if x < bx1 else CS[2], CS)
        for x in range(bx0, bx1 + 1):
            c.put(x, 25, CS[2], CS)
        for x in (bx0 + 2, bx0 + 5):
            c.put(x, 26, HOLE, CS); c.put(x, 27, HOLE, CS)
    for (dx, dy, col) in ((0, 0, CS[4]), (1, 0, CS[4]), (2, 0, CS[3]), (0, 1, CS[3]), (1, 1, M["Q"]), (2, 1, CS[2]), (0, 2, CS[2]), (1, 2, CS[2]), (2, 2, CS[1])):
        c.put(43 + dx, 39 + dy, col, CS)
    # 天守（青緑の寄棟・手前の壁・窓・垂れ幕・入口・環のしるし）
    hip_roof(c, 18, 45, 2, 13, CT)
    face(c, 19, 44, 14, 26, CS, v=3)
    for y in range(14, 27):
        c.put(19, y, CS[4], CS)
    for (wx, lit) in ((22, False), (26, True), (37, True), (41, False)):
        for y in (17, 18, 19):
            c.put(wx, y, HOLE if not (lit and y > 17) else CLT[0], CS)
        c.put(wx, 20, CS[4], CS)
    for y in range(19, 27):
        for x in range(29, 35):
            if y > 20 or 30 <= x <= 33:
                c.put(x, y, HOLE if x < 34 else CS[1], CS)
    for (dx, dy) in ((0, -2), (1, -2), (-1, -1), (2, -1), (-1, 0), (2, 0), (0, 1), (1, 1)):
        c.put(31 + dx, 16 + dy, CG[1] if dx + dy < 1 else CG[0], CS)
    banner(c, 24, 14, 6); banner(c, 39, 14, 6)
    for x in range(36, 40):                                         # 天守の右の影（中庭の上）
        for y in range(18, 28):
            if c.get(x, y) in (CS[3], CS[2]) and x > 44:
                c.put(x, y, CS[2], CS)
    for y in range(14, 28):
        for x in range(45, 48):
            if c.get(x, y) in (CS[3], CS[2]):
                c.put(x, y, CS[2] if x > 45 else CS[1], CS)
    # 左右の壁の上の面
    top(c, 6, 9, 13, 44, CS); top(c, 54, 57, 13, 44, CS, v=3)
    # 奥の角の塔（とんがり屋根・旗）
    for tx in (8, 55):
        round_tower(c, tx, 5.5, 9, 17, CS, slits=(11,))
        cone_roof(c, tx, 9, 6.3, 11, CT)
    flag(c, 8, 0); flag(c, 55, 0)
    # 手前の壁（低い）
    top(c, 9, 54, 42, 43, CS)
    crenel(c, 9, 54, 42, CS)
    face(c, 9, 54, 44, 50, CS, v=3)
    for x in (14, 19, 44, 49):                                     # 手前の壁の矢狭間（縦長の細い穴）
        c.put(x, 46, HOLE, CS); c.put(x, 47, HOLE, CS); c.put(x, 48, CS[4], CS)
    # 手前の角の塔（平らな屋上）
    for tx in (8, 55):
        round_tower(c, tx, 6.0, 39, 52, CS, slits=(44,))
        flat_top(c, tx, 39, 6.4, CS)
    # 門の建物（張り出した上の面・胸壁・アーチの門・落とし格子）
    top(c, 24, 39, 38, 40, CS)
    crenel(c, 24, 39, 38, CS)
    face(c, 24, 39, 41, 55, CS, v=3)
    for y in range(45, 56):
        for x in range(28, 36):
            if y > 46 or 29 <= x <= 34:
                if y == 45 and not (30 <= x <= 33):
                    continue
                c.put(x, y, HOLE if (x - 28) % 2 == 0 or y > 53 else M["w"], CS)
    for x in range(28, 36):
        c.put(x, 44, CS[4], CS)
    for y in (43,):
        c.put(31, y, CG[1], CS); c.put(32, y, CG[0], CS)
    # 門前の道（下へ広がる）
    for y in range(56, 64):
        k = (y - 56) // 2
        for x in range(28 - k, 36 + k):
            c.put(x, y, CS[4] if x < 34 + k else CS[3], CS)
    c.outline(OUT)
    return c.save("icon-castle", trim=False)


def icon_palace():
    c = Canvas()
    # いちばん下の段（上の面＋石の面）と、まん中の大階段
    top(c, 2, 61, 46, 48, CS)
    face(c, 2, 61, 49, 55, CS, v=3)
    for y in range(46, 64):
        k = (y - 46) // 3
        for x in range(25 - k, 39 + k):
            c.put(x, y, CS[4] if (y - 46) % 2 == 0 else CS[2], CS)
        c.put(25 - k, y, CS[3], CS); c.put(38 + k, y, CS[1], CS)
    # 中の段（列柱の回廊: 柱は2ドット、柱のあいだは深い影）
    top(c, 7, 56, 36, 38, CS)
    for x in range(7, 57):
        c.put(x, 39, CS[2], CS)
    for y in range(40, 46):
        for x in range(7, 57):
            k = (x - 7) % 4
            c.put(x, y, CS[4] if k == 0 else CS[3] if k == 1 else HOLE if y > 40 else CS[1], CS)
    # 左右の丸屋根（暗いむらさきの石。金のてっぺん）
    for cx in (14, 49):
        for y in range(30, 36):
            for x in range(cx - 5, cx + 6):
                c.put(x, y, CS[3] if x < cx + 3 else CS[2], CS)
        for x in (cx - 3, cx, cx + 3):
            c.put(x, 32, CV[0], CS); c.put(x, 33, CV[0], CS)
        dome(c, cx, 29, 6, 6, CD)
        c.put(cx, 22, CG[1], CD); c.put(cx, 23, CG[0], CD)
    # 上の広間（暗い寄棟の屋根＋手前の壁、入口、むらさきの灯の窓）
    hip_roof(c, 18, 45, 18, 27, CD)
    face(c, 19, 44, 28, 35, CS, v=3)
    for y in range(30, 36):
        for x in range(29, 35):
            if y > 30 or 30 <= x <= 33:
                c.put(x, y, HOLE, CS)
    for wx in (22, 25, 38, 41):
        c.put(wx, 30, CV[1], CS); c.put(wx, 31, CV[0], CS)
    # まん中の「からっぽの灯」の塔: 4本の柱の枠、中は暗いからっぽ、ふちにだけむらさきの光
    for y in range(4, 19):
        for x in range(25, 39):
            if x in (25, 26, 37, 38):
                col = CD[4] if x == 25 else CD[3] if x == 26 else CD[2] if x == 37 else CD[1]
            else:
                col = HOLE
            c.put(x, y, col, CD)
    for y in (4, 11, 18):
        for x in range(24, 40):
            c.put(x, y, CD[4] if x < 37 else CD[2], CD)
            c.put(x, y + 1, CD[2] if x < 37 else CD[1], CD)
    for y in (6, 13):
        for x in range(27, 37):
            c.put(x, y, CV[0], CD)                                  # 枠の内がわのふちの光（上）
    for y in list(range(6, 11)) + list(range(13, 18)):
        c.put(27, y, CV[1] if y in (7, 8, 14, 15) else CV[0], CD); c.put(36, y, CV[0], CD)
    hip_roof(c, 24, 39, 0, 3, CD)
    c.put(31, 0, CG[1], CD); c.put(32, 0, CG[0], CD)
    c.outline(OUT)
    return c.save("icon-palace", trim=False)


# ===================================================================== 7回目: 手で1ドットずつ決めた部品（テンプレート）
# 文字1つ＝1ドット。'.' は透明。凡例（legend）は 文字 → 色（または (色, 素材)）。
# 7回目の指示「これらドット絵もっとこだわって。リアルな感じで」: 港・村・湖・鉱山・砂漠・野営地・霧断崖・雪の町・お城の部品を、
# 計算で作った形（ぼやける）ではなく、大事なドットを手で置いた形にした。光はいつも左上。
TPL = {}


def stamp(c, x0, y0, name, mat=None, flip=False):
    rows, leg = TPL[name]
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch == ".":
                continue
            v = leg[ch]
            col, m = (v if isinstance(v, tuple) else (v, mat))
            xx = x0 + (len(r) - 1 - i if flip else i)
            c.put(xx, y0 + j, col, m)


SEA_D = "#1c4890"
PALE = "#fff4c8"                                                         # 灯のまわりの光（灯台の光の筋・たき火の照り返し）

# --- 帆船: 船体は弓なり（へさきが上がる）、帆柱、前の綱（ななめの1本）。帆は、帆柱ぎわが少し暗く（風で張って奥へ曲がる）、
#     まん中の「ふくらみ」がいちばん明るく、後ろのふち（右）と下のふちが影。帆柱のてっぺんに赤い小旗
TPL["sailboat"] = ([
    "......f......",
    "......mff....",
    "......mS.....",
    ".....rmsS....",
    ".....rmsSS...",
    "....r.msSSs..",
    "....r.msSSSt.",
    "...r..msSSSst",
    "...r..msSSSst",
    "..r...msSSsst",
    "..r...mssssst",
    ".r....bbbbbbb",
    "ww....m......",
    "Hwwwwwwwwwwww",
    ".HHHHHHHHHHHh",
    "..hhhhhhhhhh.",
    "...~vvvvvvv~.",
], {"f": ROOF[3], "m": TIMBER[0], "S": WALL[3], "s": WALL[2], "t": WALL[1], "r": TIMBER[1], "b": TIMBER[1],
    "w": DIRT[4], "H": TIMBER[2], "h": TIMBER[0], "~": SEA[3], "v": SEA_D})

# --- 小舟: へさきとともがとがった細長い形。中は暗く、腰かけ板2枚。奥の櫂は上へ、手前の櫂は水の中へ（水かきのまわりに波紋）
TPL["rowboat"] = ([
    "O..............",
    ".o.............",
    "..o.wwwwwww....",
    "..wwdbdddbdw...",
    ".wddbdddbddddw.",
    "..wHHHHHHHHHw..",
    "...hhhhhhhhho..",
    "....~vvvvv~..o~",
    ".............OO",
], {"O": DIRT[3], "o": TIMBER[1], "w": DIRT[4], "d": TIMBER[0], "b": DIRT[3], "H": TIMBER[2], "h": TIMBER[0],
    "v": SEA_D, "~": SEA[3]})

# --- 灯台の上: 金のてっぺん、暗い丸屋根、ガラスの灯室（白い芯・まわりは黄・暗い枠）、手すりの回廊（手すりと細い柱）、
#     左右へ短い光の筋（水平に4ドット、ななめに2ドットずつ。ばらまかない）
TPL["lamp"] = ([
    "........g........",
    ".......DDd.......",
    "......DDDdd......",
    ".p....kLLLk....p.",
    "..p...kLMLk...p..",
    "PPL..kLMMLLk..LPP",
    "..p...kLLLk...p..",
    ".p...rrrrrrr...p.",
    ".....r.r.r.r.....",
    ".....RRRRRRR.....",
], {"g": GOLD[1], "D": SLATE[2], "d": SLATE[0], "k": SLATE[0], "L": LIGHT, "M": PALE, "P": PALE, "p": PALE,
    "r": SLATE[3], "R": SLATE[1]})


def lighthouse7(c, cx, ybase, h=28):
    """灯台（7回目）: 上は手描きの灯室（TPL lamp）。塔は下が太い円柱で、赤と白の帯（4行ずつ）。
    どの帯も左の2列が明るく、右の1列が影。白い帯に小窓、足もとに扉と石段"""
    top = ybase - h
    stamp(c, cx - 8, top, "lamp", WALL)
    for y in range(top + 10, ybase + 1):
        t = (y - top - 10) / max(1, ybase - top - 10)
        half = 3.0 + t * 1.6
        band = ((y - top - 10) // 4) % 2 == 0
        pal = ROOF if band else WALL
        for x in range(int(cx - half), int(cx + half) + 1):
            u = (x + 0.5 - (cx + 0.5)) / (half + 0.5)
            if abs(u) > 1:
                continue
            i = 3 if u < -0.35 else 2 if u < 0.45 else 1
            c.put(x, y, pal[i], pal)
    for wy in (top + 15, top + 23):
        c.put(cx, wy, GLASS, WALL); c.put(cx, wy + 1, GLASS, WALL)
    for y in range(ybase - 2, ybase + 1):
        c.put(cx - 1, y, TIMBER[1], WALL); c.put(cx, y, TIMBER[0], WALL)


def pier(c, x0, y0, y1, w=4):
    """桟橋: 横にわたした板（上の行は明るく、下の行は1段暗い）と、2枚ごとのすき間（下の水が暗く見える）。
    右のふちは影の梁。左右の杭は6行ごとで、水の上の杭には明るい波紋（杭の左右と下に1ドットずつ）"""
    water = set(SEA)
    for y in range(y0, y1 + 1):
        k = (y - y0) % 3
        on_water = c.get(x0 + 1, y) in water or c.get(x0 + 1, y) == SEA_D
        for x in range(x0, x0 + w):
            if k == 2:
                col = SEA_D if on_water else TIMBER[0]
            else:
                col = DIRT[4] if k == 0 else DIRT[3]
            if x == x0 + w - 1:
                col = TIMBER[1] if k != 2 else TIMBER[0]
            c.put(x, y, col, DIRT)
    for y in range(y0 + 3, y1, 6):
        for px in (x0 - 1, x0 + w):
            wet = c.get(px, y + 1) in water
            c.put(px, y, TIMBER[0], TIMBER); c.put(px, y + 1, TIMBER[0], TIMBER)
            if wet:
                side = -1 if px < x0 else 1
                c.put(px + side, y + 1, SEA[3]); c.put(px, y + 2, SEA[3])


# --- 水車（正面から）: 左上が明るい木の輪・8本の腕・軸・輪の外の板（羽根）。中のすき間は透明（うしろの壁や水が見える）
TPL["wheel"] = ([
    ".....PPP.....",
    "..P.RRRRR.P..",
    ".PRR..S..rrP.",
    "..RS..S..Sr..",
    ".R..S.S.S..r.",
    "PR...SSS...rp",
    "PRSSSSHSSSSrp",
    "PR...SSS...rp",
    ".R..S.S.S..r.",
    "..rS..S..Sr..",
    ".prr..S..rrp.",
    "..p.rrrrr.p..",
    ".....ppp.....",
], {"P": DIRT[2], "p": TIMBER[0], "R": DIRT[3], "r": TIMBER[0], "S": TIMBER[1], "H": DIRT[4]})

# --- 刈った麦を立てて束ねた「麦の束」（3×4。左が明るく、右が影、足もとに短い影）
TPL["stook"] = ([
    ".a.",
    "aAb",
    "aAb",
    "Abb",
], {"a": THATCH[4], "A": THATCH[3], "b": THATCH[1]})

SHEEN = "#f0dca0"


def wheat_field(c, x0, y0, w, h, ripe=True):
    """麦畑: 3行で1つのうね（穂の明るい行・穂のまん中の行・うねのあいだの影）。左上から右下へ、つやの帯（穂がいちばん明るい色）。
    手前のふち2行は、立っている麦の横の面（1段暗い）。刈ったあとの畑（ripe=False）は、うすい刈り株のうねに麦の束"""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            k = (y - y0) % 3
            if ripe:
                band = abs((x - x0) - (y - y0) * 1.6 - w * 0.35) < 3.2      # つやの帯（ななめ）
                if y >= y0 + h - 2:
                    col = THATCH[2] if y == y0 + h - 2 else THATCH[1]       # 手前の横の面
                elif k == 0:
                    col = SHEEN if band else THATCH[4]
                elif k == 1:
                    col = THATCH[4] if band else THATCH[3]
                else:
                    col = THATCH[2]
            else:
                col = THATCH[3] if k == 0 else THATCH[2] if k == 1 else DIRT[3]
            c.put(x, y, col)


def millrace(c, x0, x1, y):
    """水車の水路（木の板で囲んだ、まっすぐな流れ）: 上のふちの板・水3行（明るい波の行・水・深い所）・下のふちの板"""
    for x in range(x0, x1 + 1):
        c.put(x, y, DIRT[2], DIRT)
        c.put(x, y + 1, LAKE[3] if (x - x0) % 5 in (1, 2) else LAKE[2])
        c.put(x, y + 2, LAKE[2])
        c.put(x, y + 3, LAKE[1])
        c.put(x, y + 4, TIMBER[0], TIMBER)


# --- ガラスの丸屋根: 鉄の骨（まん中の1本と横の輪1本、輪の下は窓わくの縦の骨2本）。左上に、丸みにそった白い映りこみ。右下は暗いガラス
TPL["glassdome"] = ([
    ".....FFFFF.....",
    "...FHHGFGggF...",
    "..FHHHGFGGggF..",
    ".FHHGGGFGGGggF.",
    "FFFFFFFFFFFFFFF",
    "FHGGFGGFGGFggF.",
    "FHGGFGGFGGFgggF",
    "FGGGFGGFGgFgggF",
    "BBBBBBBBBBBBBbb",
], {"F": SLATE[3], "H": GLOW[2], "G": GLOW[1], "g": GLOW[0], "B": WALL[2], "b": WALL[1]})

# --- 葦（あし）とがま: 細い茎4本（左は明るく右は暗い）、ななめの葉2枚、2本の先に茶色のがまの穂（2ドット）。根もとに水の輪
TPL["reeds"] = ([
    "..h....",
    "..h..h.",
    "h.s..h.",
    "h.s.lS.",
    "s.sl.S.",
    "sl.s.S.",
    ".sssSS.",
    ".~~~~~.",
], {"h": TIMBER[0], "s": FOREST[3], "S": FOREST[2], "l": FOREST[4], "~": LAKE[3]})


# --- トロッコ（前から少し見下ろす）: 上に山盛りの鉱石（明るい石・暗い石・金色に光る灯り石1つ）、木の箱に鉄の帯（上下のふちと、まん中）、
#     下に2つずつの車輪
TPL["minecart"] = ([
    "..oOgOo..",
    ".oOOoOOo.",
    "SSSSSSSSs",
    "SDDDSDDDs",
    "SdddSddds",
    "sssssssss",
    ".kk...kk.",
], {"o": STONE[1], "O": STONE[4], "g": LIGHT, "S": STONE[3], "s": STONE[1], "D": TIMBER[2], "d": TIMBER[1], "k": STONE[0]})


def track(c, cx, y0, y1, g0=3, g1=8):
    """坑口から手前へ出てくるレール（遠近: 奥ほどせまく、手前ほど広い）。
    まくら木は2行ごとの横の板（レールより1ドット外まで）、レールのあいだは砕石。レールは「光る上の面（明るい）＋右の影（暗い）」の2ドット。
    坑口の暗がりの中のレールは、光らない暗い色"""
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        gauge = round(g0 + (g1 - g0) * t)
        L = cx - gauge // 2
        R = L + gauge
        dark = c.get(cx, y) == STONE[0]
        for x in range(L + 2, R):
            if not dark:
                c.put(x, y, STONE[2], STONE)                      # 砕石
        if (y - y0) % 2 == 1:
            for x in range(L - 1, R + 3):
                c.put(x, y, TIMBER[0] if dark else (TIMBER[2] if x == L - 1 else TIMBER[1]), TIMBER)   # まくら木
        for x in (L, R):
            c.put(x, y, STONE[2] if dark else STONE[4], STONE)
            c.put(x + 1, y, STONE[1] if dark else STONE[1], STONE)


def adobe_house(c, x0, yb, w, wh, depth, door=None, wins=(), lit=(), ground="sand"):
    """土の家（7回目）: 屋上のまわりの低い手すり壁（左と奥と手前のふちは明るい線、右は影）。屋上の面は1段へこんで、
    奥の手すり壁の影が1行落ちる。手前の壁の上には、梁の先（ビガ: 木の明るい1ドット＋その下の壁の影）が3ドットごと。
    入口は影の中（暗い穴・左の柱は明るい・上に木のまぐさ）"""
    P = ADOBE
    x1 = x0 + w - 1
    yt = yb - wh - depth + 1
    cast(c, x0, x1, yt, yb, ground, dx=2, dy=1)
    for y in range(yt, yt + depth):
        for x in range(x0, x1 + 1):
            if y == yt or y == yt + depth - 1 or x == x0:
                col = P[4]                                         # 手すり壁の上
            elif x == x1:
                col = P[2]
            elif y == yt + 1:
                col = P[2]                                         # 奥の手すり壁の影
            else:
                col = P[3]                                         # 屋上の面
            if x == x1 and (y == yt or y == yt + depth - 1):
                col = P[3]
            c.put(x, y, col, P)
    yw = yt + depth
    for y in range(yw, yb + 1):
        for x in range(x0, x1 + 1):
            col = P[3] if x < x1 else P[2]
            if y == yw:
                col = P[2] if x < x1 else P[1]                     # 手すり壁の下の影
            c.put(x, y, col, P)
    for x in range(x0 + 1, x1 - 1, 3):                             # 梁の先（ビガ）
        c.put(x, yw + 1, TIMBER[2], TIMBER); c.put(x, yw + 2, P[1], P)
    for i, wx in enumerate(wins):                                  # 小さな窓（1×2。下に明るい棚）
        on = i in lit
        c.put(x0 + wx, yw + 3, LIGHT if on else P[0], P); c.put(x0 + wx, yw + 4, LAMP if on else P[0], P)
    if door is not None:
        dx = x0 + door
        for x in range(dx - 1, dx + 3):
            c.put(x, yb - 3, TIMBER[1], TIMBER)                    # まぐさ
        for y in range(yb - 2, yb + 1):
            c.put(dx - 1, y, P[4], P)                              # 左の柱（光が当たる）
            c.put(dx, y, P[0], P); c.put(dx + 1, y, P[0], P)


# --- 隊商宿のアーチの門: 明るい縁どり（左と上）、影の縁（右）、中は深い影。奥に半分あいた木の扉
TPL["archgate"] = ([
    "..TTT..",
    ".TkkkT.",
    "TkkkkkU",
    "TkkkkkU",
    "TkkkdkU",
    "TkkkddU",
    "TkkkddU",
    "TkkkddU",
], {"T": ADOBE[4], "U": ADOBE[2], "k": ADOBE[0], "d": TIMBER[1]})

# --- 小さなアーチの窓（3×4）
TPL["archwin"] = ([
    ".T.",
    "TkU",
    "TkU",
    "TTU",
], {"T": ADOBE[4], "U": ADOBE[2], "k": ADOBE[0]})


# ===================================================================== 見本
TERRAIN = {"icon-port": "grass", "icon-village": "grass", "icon-village-mist": "snow", "icon-lake": "grass", "icon-mine": "grass",
           "icon-tents": "sand", "icon-tents-grass": "grass", "icon-temple": "grass", "icon-snowtown": "snow", "icon-sky": "cloud",
           "icon-castle": "hills", "icon-palace": "waste"}
NAMES = list(TERRAIN)


def load_icon(d, n):
    rows = [l for l in open(os.path.join(d, f"{n}.txt")).read().split("\n") if l]
    pal = json.load(open(os.path.join(d, f"pal-{n}.json")))
    im = Image.new("RGBA", (max(len(r) for r in rows), len(rows)))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in pal:
                im.putpixel((x, y), tuple(int(pal[ch][k:k + 2], 16) for k in (1, 3, 5)) + (255,))
    return im


def terrain(kind, w, h):
    t = texture(kind).convert("RGBA")
    bg = Image.new("RGBA", (w, h))
    for y in range(0, h, 128):
        for x in range(0, w, 128):
            bg.paste(t, (x, y))
    return bg


def show(names, Z=6, out=None):
    """（作業用）1点ずつ地形の上に大きく"""
    ims = []
    for n in names:
        im = load_icon(HERE, n)
        bg = terrain(TERRAIN[n], 72, 72)
        bg.alpha_composite(im, (4, 8 - 0))
        ims.append(bg.resize((72 * Z, 72 * Z), Image.NEAREST))
    sheet = Image.new("RGBA", (sum(i.width + 6 for i in ims), 72 * Z), (40, 40, 48, 255))
    x = 0
    for i in ims:
        sheet.paste(i, (x, 0)); x += i.width + 6
    sheet.save(out or "/tmp/r28.png")


# ===================================================================== 見本の画像
PLACES = [  # (名前, アイコン, マスx, マスy)  本物の地図の位置（r26 と同じ。world-map.ts の TOWN_ICON・VILLAGE_ICON）
    ("touri", "icon-port", 26, 153), ("namioto", "icon-port", 47, 137), ("mugikano", "icon-village", 57, 161),
    ("kazami", "icon-village", 68, 102), ("tomoshimori", "icon-village", 111, 167), ("minori", "icon-village", 214, 242),
    ("kirima", "icon-village-mist", 231, 43), ("garasuko", "icon-lake", 88, 142), ("tetsukusari", "icon-mine", 122, 113),
    ("sanone", "icon-tents", 102, 195), ("samori", "icon-tents-grass", 122, 185), ("arano", "icon-tents-grass", 269, 217),
    ("kiri", "icon-temple", 212, 62), ("shimohara", "icon-snowtown", 269, 31), ("yukimachi", "icon-snowtown", 245, 27),
    ("fushima", "icon-sky", 320, 130), ("toushin (castle)", "icon-castle", 238, 198), ("kyotoukyu (palace)", "icon-palace", 300, 212),
]
GLYPH_TEX = {"O": "sea", "P": "grass", "F": "forest", "T": "snowforest", "M": "mountain", "D": "sand", "S": "snow", "R": "road",
             "H": "hills", "L": "lake", "C": "cloud", "W": "waste", "A": "ash", "Z": "lava", "V": "sea", "Q": "sea", "X": "chasm", "N": "pyramids"}


def world_rows():
    import re
    src = open(os.path.join(PX, "..", "..", "src", "game", "map", "world", "world-map.generated.ts")).read()
    a = src.index("WORLD_ROWS")
    return re.findall(r'"([A-Z]+)"', src[a:src.index("];", a)])


def world_panel(rows, gx, gy, icon_dir, icon, tw=14, th=10):
    x0, y0 = gx - tw // 2, gy - th + 3
    img = Image.new("RGBA", (tw * 16, th * 16))
    for ty in range(th):
        for tx in range(tw):
            X, Y = x0 + tx, y0 + ty
            gl = rows[Y][X] if 0 <= Y < len(rows) and 0 <= X < len(rows[Y]) else "O"
            t = texture(GLYPH_TEX.get(gl, "grass")).convert("RGBA")
            sx, sy = (X * 16) % 128, (Y * 16) % 128
            img.paste(t.crop((sx, sy, sx + 16, sy + 16)), (tx * 16, ty * 16))
    im = load_icon(icon_dir, icon)
    img.alpha_composite(im, ((gx - x0) * 16 + 8 - im.width // 2, (gy - y0 + 1) * 16 - im.height))   # 足もとをマスの下にそろえる
    return img


def world_preview(path, path1x):
    """本物の地図の地形・本物の位置。どの場所も「左が5回目（48）、右が6回目（64）」。1マス16ドット。影は描かない"""
    rows = world_rows()
    panels = []
    for (label, icon, gx, gy) in PLACES:
        a = world_panel(rows, gx, gy, R26, icon)
        b = world_panel(rows, gx, gy, HERE, icon)
        p = Image.new("RGBA", (a.width * 2 + 2, a.height + 12), (20, 20, 24, 255))
        p.paste(a, (0, 12)); p.paste(b, (a.width + 2, 12))
        ImageDraw.Draw(p).text((2, 0), f"{label}: {icon}   r26 | r28", fill=(255, 255, 255))
        panels.append(p)
    cols = 3
    pw, ph = panels[0].size
    sheet = Image.new("RGBA", (cols * (pw + 6), ((len(panels) + cols - 1) // cols) * (ph + 6)), (20, 20, 24, 255))
    for i, p in enumerate(panels):
        sheet.paste(p, ((i % cols) * (pw + 6), (i // cols) * (ph + 6)))
    sheet.save(path1x)
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(path)


def preview(path, Z=5):
    """1点ずつ大きく: 左が5回目（r26、48×48）、右が6回目（r28、64×64）。どちらも置く地面の上、同じ倍率"""
    cells = []
    for n in NAMES:
        old = load_icon(R26, n)
        new = load_icon(HERE, n)
        bg = terrain(TERRAIN[n], 48 + 64 + 12, 64)
        bg.alpha_composite(old, (2, 64 - old.height))
        bg.alpha_composite(new, (48 + 8, 0))
        im = bg.resize((bg.width * Z, bg.height * Z), Image.NEAREST)
        g, lm = landmark(n)
        cells.append((f"{n} ({TERRAIN[n]})   left: r26 48px / right: r28 64px   colors {len(palette_of(n))}   mark dL {lm[0][2] if lm else '-'}", im))
    cols = 2
    w, h = cells[0][1].width + 16, cells[0][1].height + 22
    sheet = Image.new("RGBA", (cols * w + 10, ((len(cells) + cols - 1) // cols) * h + 10), (40, 40, 48, 255))
    dr = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(cells):
        x, y = 10 + (i % cols) * w, 10 + (i // cols) * h
        sheet.paste(im, (x, y + 18))
        dr.text((x, y + 3), label, fill=(255, 255, 255))
    sheet.save(path)


def palette_of(n):
    return json.load(open(os.path.join(HERE, f"pal-{n}.json")))


def ground_l(kind):
    t = texture(kind)
    cols = t.getcolors(65536)
    tot = sum(k for k, _ in cols)
    return sum(k * lum(hx(cc)) for k, cc in cols) / tot


def landmark(name):
    """見つける目じるし: 地面の色でない色のうち 4 ドット以上ある色で、地面の平均との明るさの差が 25〜35 のもの（多い順に3つ）"""
    rows = [l for l in open(os.path.join(HERE, f"{name}.txt")).read().split("\n") if l]
    pal = palette_of(name)
    g = ground_l(TERRAIN[name])
    pure = ground_cols(TERRAIN[name] if TERRAIN[name] != "hills" else "grass")
    cnt = {}
    for r in rows:
        for ch in r:
            if ch != "." and pal[ch] not in pure:
                cnt[pal[ch]] = cnt.get(pal[ch], 0) + 1
    ok = [(k, col, round(abs(lum(col) - g), 1)) for col, k in cnt.items() if k >= 4 and 25 <= abs(lum(col) - g) <= 35]
    ok.sort(reverse=True)
    return round(g, 1), ok[:3]


def size_of(name):
    rows = [l for l in open(os.path.join(HERE, f"{name}.txt")).read().split("\n") if l]
    xs = [x for r in rows for x, ch in enumerate(r) if ch != "."]
    ys = [y for y, r in enumerate(rows) for ch in r if ch != "."]
    return min(xs), max(xs), max(xs) - min(xs) + 1, min(ys), max(ys)


def colors(name_fn):
    """（作業用）まとめる前の色と、その数"""
    import builtins
    c = None
    orig = Canvas.save

    def grab(self, *a, **k):
        nonlocal c
        c = self
        self.trim_ground()
        return None
    Canvas.save = grab
    try:
        name_fn()
    finally:
        Canvas.save = orig
    cnt = c.count()
    for col, n in sorted(cnt.items(), key=lambda t: -t[1]):
        print(f"  {col} {n}")
    print("  合計", len(cnt))


PIECES = [icon_port, icon_village, icon_village_mist, icon_lake, icon_mine, icon_tents, icon_tents_grass, icon_temple, icon_snowtown, icon_sky, icon_castle, icon_palace]

if __name__ == "__main__":
    only = sys.argv[1:]
    for f in PIECES:
        n = f.__name__.replace("_", "-")
        if only and n not in only:
            continue
        print(*f())
    if not only:
        for n in NAMES:
            print(n, "左右・はば・上下", size_of(n), "地面の明るさ / 目じるし", landmark(n))
        preview(os.path.join(HERE, "preview.png"))
        world_preview(os.path.join(HERE, "preview-world.png"), os.path.join(HERE, "preview-world-1x.png"))
