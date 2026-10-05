"""全体フィールドの山の置き方を整える（2026-10-05、人間の指示「地形、結構山とか岩山がぐちゃぐちゃに置かれてるから整えて」）。

apply_field_trace.py のあとに実行する（何度実行しても同じ結果になる）。world-map.generated.ts の WORLD_ROWS だけを書きかえる。

やること（どれも決まった順番・決まったきまりで、乱数は使わない）
  1. 山のかたまりのふちをなめらかにする: 山（M・N）のマスを、まわり3×3の多数決でならす（2と合わせて、変わらなくなるまで）
  2. ぽつんと1マスだけの山は消し、山にかこまれた1マスのくぼみ・穴はうめる
  3. 小さな谷（X）のかけら（6マス以下）は山にする（どちらも通れないので、歩ける所は変わらない）
  4. とがった山（N）は、大きな山脈のまん中だけ: 山のふちから3マス以上内がわで、山のかたまりが60マス以上のときだけ N、ほかは M
     （火山のまわり・溶岩から8マス以内の N は、火山の本体なのでそのまま）
  5. 丘（H）: 山にとなる草原（P）のうち、山に2マス以上ふれる所を丘にして、山と草原のあいだをやわらげる

まもること（スクリプトの最後で確かめ、守れていなければ書きかえずに止まる）
  - 変えてよいのは M・N・H・X（小さなかけら）と、それにとなる陸（P・F・D・S・T・W・A）だけ。海・湖・道・雲・溶岩・渦の輪（O L R C Z V Q）は変えない
  - 町・村・名所・環灯台・小島・船着き場・船・飛空艇・塔・渦の通り道（WORLD_CHANNEL）のまわり2マスは変えない
  - 町のまわり12マスは変えない（ダンジョンの入口は、町から歩いて3〜9マスの所に、通れるマスを数えて決まるため）
  - 塔の陥没（WORLD_TOWER から22マス以内）と、渦の輪（V・Q）から3マス以内は変えない
  - 道のとなりのマスを山にしない
  - 歩いて行ける所のつながりを変えない: 前もあとも通れるマスどうしの「つながりの組」が、まったく同じであること
使い方: python3 tools/world-map/tidy_mountains.py [リポジトリのルート]
"""
import re
import sys
from collections import Counter, deque

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
GEN = f"{ROOT}/src/game/map/world/world-map.generated.ts"
MOUNT = set("MN")
BLOCKED = set("OMLVQNXZ")                  # world-map.ts の BLOCKED（海・山・湖・渦・とがった山・谷・溶岩）
LAND_OK = set("PFDSTWAH")                  # 山のとなりで変えてよい陸
FIXED = set("OLRCZVQ")
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy]


def load():
    src = open(GEN).read()
    i = src.index("WORLD_ROWS"); j = src.index("];", i)
    rows = re.findall(r'"([A-Z]+)"', src[i:j])
    return src, i, j, [list(r) for r in rows]


def protected_mask(src, g):
    H, W = len(g), len(g[0])
    prot = [[False] * W for _ in range(H)]

    def mark(cx, cy, r):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < W and 0 <= y < H:
                    prot[y][x] = True
    for a, b in re.findall(r"\{ x: (\d+), y: (\d+)", src):
        mark(int(a), int(b), 2)
    for a, b in re.findall(r"\[(\d+), (\d+)\]", src[src.index("WORLD_CHANNEL"):]):
        mark(int(a), int(b), 2)
    towns = src[src.index("WORLD_TOWNS"):src.index("WORLD_BEACONS")]
    for a, b in re.findall(r"x: (\d+), y: (\d+)", towns):
        mark(int(a), int(b), 12)
    tw = re.search(r"WORLD_TOWER = \{ x: (\d+), y: (\d+)", src)
    mark(int(tw.group(1)), int(tw.group(2)), 22)
    for y in range(H):
        for x in range(W):
            if g[y][x] in "VQ":
                mark(x, y, 3)
            if g[y][x] == "Z":
                mark(x, y, 8)
            if x < 8 or y < 8 or x >= W - 8 or y >= H - 8:
                prot[y][x] = True
    return prot


def components(g):
    """歩ける（BLOCKED でない）マスの4方向のつながりの組。地図は左右・上下でつながる（wrap）"""
    H, W = len(g), len(g[0])
    lab = [[-1] * W for _ in range(H)]
    n = 0
    for y in range(H):
        for x in range(W):
            if lab[y][x] >= 0 or g[y][x] in BLOCKED:
                continue
            dq = deque([(x, y)]); lab[y][x] = n
            while dq:
                cx, cy = dq.popleft()
                for dx, dy in N4:
                    nx, ny = (cx + dx) % W, (cy + dy) % H
                    if lab[ny][nx] < 0 and g[ny][nx] not in BLOCKED:
                        lab[ny][nx] = n; dq.append((nx, ny))
            n += 1
    return lab


def same_partition(g0, g1):
    """前もあとも歩けるマスについて、つながりの組の分け方が同じか"""
    a, b = components(g0), components(g1)
    fw, bw = {}, {}
    H, W = len(g0), len(g0[0])
    for y in range(H):
        for x in range(W):
            if a[y][x] >= 0 and b[y][x] >= 0:
                if fw.setdefault(a[y][x], b[y][x]) != b[y][x] or bw.setdefault(b[y][x], a[y][x]) != a[y][x]:
                    return False, (x, y)
    return True, None


class Tidy:
    def __init__(self, g, prot):
        self.g = g
        self.prot = prot
        self.H, self.W = len(g), len(g[0])
        self.lab = components(g)
        self.orig = [r[:] for r in g]
        self.lab0 = [r[:] for r in self.lab]                   # もとのつながりの組（もと歩けたマスだけ >= 0）

    def at(self, x, y):
        return self.g[y][x] if 0 <= x < self.W and 0 <= y < self.H else "O"

    def changeable(self, x, y):
        if self.prot[y][x]:
            return False
        c = self.g[y][x]
        if c in MOUNT or c == "H":
            return True
        if c in LAND_OK:
            return any(self.at(x + dx, y + dy) in MOUNT for dx, dy in N8)
        return False

    def near_road(self, x, y):
        return any(self.at(x + dx, y + dy) == "R" for dx, dy in N4)

    def can_open(self, x, y):
        """山を陸にしてよいか: となりの歩けるマスが、もともと同じつながりの組（新しい近道ができない）"""
        labs = {self.lab[y + dy][x + dx] for dx, dy in N4 if 0 <= x + dx < self.W and 0 <= y + dy < self.H and self.g[y + dy][x + dx] not in BLOCKED}
        if self.lab0[y][x] >= 0:
            labs.add(self.lab0[y][x])                          # もと歩けたマスにもどすときは、もとの組にしかつながらないこと
        return len(labs) <= 1

    def can_fill(self, x, y):
        """陸を山にしてよいか: 道のとなりでない、そのマスを山にしても、まわりの歩けるマスどうしが 9×9 の中でつながったまま"""
        if self.near_road(x, y):
            return False
        if self.g[y][x] in BLOCKED:
            return True
        nbs = [(x + dx, y + dy) for dx, dy in N4 if self.at(x + dx, y + dy) not in BLOCKED]
        if len(nbs) <= 1:
            return True
        r = 4
        seen = {nbs[0]}
        dq = deque([nbs[0]])
        while dq:
            cx, cy = dq.popleft()
            for dx, dy in N4:
                nx, ny = cx + dx, cy + dy
                if abs(nx - x) > r or abs(ny - y) > r or (nx, ny) == (x, y) or (nx, ny) in seen:
                    continue
                if self.at(nx, ny) in BLOCKED:
                    continue
                seen.add((nx, ny)); dq.append((nx, ny))
        return all(p in seen for p in nbs)

    def land_for(self, x, y):
        """山を陸にするときの地面: まわりでいちばん多い陸（山・道・水はのぞく）。なければ草原"""
        c = Counter(self.at(x + dx, y + dy) for dx, dy in N8)
        for k in list(c):
            if k not in LAND_OK:
                del c[k]
        if not c:
            return "P"
        top = max(sorted(c), key=lambda k: c[k])
        return "P" if top == "H" else top

    def open(self, x, y):
        if self.orig[y][x] == "X":
            return False                                       # もとが谷のマスは、山にはしても陸にはしない
        if self.can_open(x, y):
            labs = [self.lab[y + dy][x + dx] for dx, dy in N4 if self.at(x + dx, y + dy) not in BLOCKED]
            self.g[y][x] = self.land_for(x, y)
            self.lab[y][x] = self.lab0[y][x] if self.lab0[y][x] >= 0 else (labs[0] if labs else -2)
            return True
        return False

    def fill(self, x, y, glyph="M"):
        if self.can_fill(x, y):
            self.g[y][x] = glyph
            self.lab[y][x] = -1
            return True
        return False

    def mcount8(self, x, y):
        return sum(self.at(x + dx, y + dy) in MOUNT for dx, dy in N8)

    def mcount4(self, x, y):
        return sum(self.at(x + dx, y + dy) in MOUNT for dx, dy in N4)

    # ---------------------------------------------------------------- 1) ふちをならす
    def smooth(self, rounds=2):
        for _ in range(rounds):
            plan = []
            for y in range(self.H):
                for x in range(self.W):
                    if not self.changeable(x, y):
                        continue
                    m = self.mcount8(x, y)
                    is_m = self.g[y][x] in MOUNT
                    if is_m and m <= 2:
                        plan.append(("open", x, y))
                    elif not is_m and m >= 6:
                        plan.append(("fill", x, y))
            for op, x, y in plan:
                (self.open if op == "open" else self.fill)(x, y)

    # ---------------------------------------------------------------- 2) ぽつんと1マス・1マスのくぼみ
    def singles(self):
        for y in range(self.H):
            for x in range(self.W):
                if not self.changeable(x, y):
                    continue
                if self.g[y][x] in MOUNT and self.mcount4(x, y) == 0:
                    self.open(x, y)
                elif self.g[y][x] not in MOUNT and self.mcount4(x, y) >= 3:
                    self.fill(x, y)

    # ---------------------------------------------------------------- 3) 小さな谷のかけら
    def small_chasms(self, maxn=6):
        seen = set()
        for y in range(self.H):
            for x in range(self.W):
                if self.g[y][x] != "X" or (x, y) in seen:
                    continue
                comp, dq = [], deque([(x, y)]); seen.add((x, y))
                while dq:
                    cx, cy = dq.popleft(); comp.append((cx, cy))
                    for dx, dy in N4:
                        p = (cx + dx, cy + dy)
                        if p not in seen and self.at(*p) == "X":
                            seen.add(p); dq.append(p)
                if len(comp) <= maxn and not any(self.prot[cy][cx] for cx, cy in comp):
                    for cx, cy in comp:
                        self.g[cy][cx] = "M"                      # 通れない → 通れない

    # ---------------------------------------------------------------- 4) とがった山は大きな山脈のまん中だけ
    def peaks(self, core=3, minsize=60):
        H, W = self.H, self.W
        dist = [[0] * W for _ in range(H)]
        dq = deque()
        for y in range(H):
            for x in range(W):
                if self.g[y][x] in MOUNT:
                    if any(self.at(x + dx, y + dy) not in MOUNT for dx, dy in N8):
                        dist[y][x] = 1; dq.append((x, y))
                    else:
                        dist[y][x] = 0
        while dq:
            x, y = dq.popleft()
            for dx, dy in N8:
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and self.g[ny][nx] in MOUNT and dist[ny][nx] == 0:
                    dist[ny][nx] = dist[y][x] + 1; dq.append((nx, ny))
        size = [[0] * W for _ in range(H)]
        seen = set()
        for y in range(H):
            for x in range(W):
                if self.g[y][x] in MOUNT and (x, y) not in seen:
                    comp, q2 = [], deque([(x, y)]); seen.add((x, y))
                    while q2:
                        cx, cy = q2.popleft(); comp.append((cx, cy))
                        for dx, dy in N4:
                            p = (cx + dx, cy + dy)
                            if p not in seen and self.at(*p) in MOUNT:
                                seen.add(p); q2.append(p)
                    for cx, cy in comp:
                        size[cy][cx] = len(comp)
        for y in range(H):
            for x in range(W):
                if self.g[y][x] not in MOUNT or self.prot[y][x]:
                    continue
                want = "N" if (dist[y][x] >= core and size[y][x] >= minsize) else "M"
                self.g[y][x] = want                                # M と N はどちらも通れない

    # ---------------------------------------------------------------- 5) 丘の帯
    def hills(self):
        for y in range(self.H):
            for x in range(self.W):
                if self.prot[y][x] or self.g[y][x] != "P":
                    continue
                if self.mcount8(x, y) >= 2:
                    self.g[y][x] = "H"                             # 通れる → 通れる


def main():
    src, i, j, g0 = load()
    prot = protected_mask(src, g0)
    g1 = [r[:] for r in g0]
    lab0 = components(g0)
    for _round in range(6):                                     # 全部の手順を、変わらなくなるまでくり返す（何度実行しても同じ結果にするため）
        t = Tidy([r[:] for r in g1], prot)
        t.orig = g0
        t.lab0 = lab0
        # 今のつながりの組を、もとの組の番号に読みかえる（もとは歩けなかった所だけの組は、それぞれ別の負の番号）
        cur, mp, k = t.lab, {}, -10
        for yy in range(len(g0)):
            for xx in range(len(g0[0])):
                c = cur[yy][xx]
                if c >= 0 and lab0[yy][xx] >= 0:
                    mp.setdefault(c, lab0[yy][xx])
        for yy in range(len(g0)):
            for xx in range(len(g0[0])):
                c = cur[yy][xx]
                if c >= 0 and c not in mp:
                    mp[c] = k; k -= 1
        t.lab = [[mp[c] if c >= 0 else c for c in row] for row in cur]
        t.small_chasms()
        for _ in range(8):
            before = ["".join(r) for r in t.g]
            t.smooth(1)
            t.singles()
            if ["".join(r) for r in t.g] == before:
                break
        t.peaks()
        t.hills()
        if t.g == g1:
            break
        g1 = t.g
    H, W = len(g0), len(g0[0])
    # ---- 確かめ ----
    bad = []
    for y in range(H):
        for x in range(W):
            a, b = g0[y][x], g1[y][x]
            if a == b:
                continue
            if prot[y][x]:
                bad.append(("まもる所が変わった", x, y, a, b))
            if a in FIXED or b in FIXED:
                bad.append(("変えてはいけない地形", x, y, a, b))
            if a == "X" and b != "M":
                bad.append(("谷は山にだけ", x, y, a, b))
    ok, where = same_partition(g0, g1)
    if not ok:
        bad.append(("歩けるつながりが変わった", where))
    if bad:
        print("止めました（書きかえていません）:", bad[:10])
        sys.exit(1)
    out = ["".join(r) for r in g1]
    changed = sum(a != b for r0, r1 in zip(g0, g1) for a, b in zip(r0, r1))
    body = "\n".join(f'  "{r}",' for r in out)
    new_src = src[:i] + "WORLD_ROWS: string[] = [\n" + body + "\n" + src[j:]
    head = "// 自動生成: tools/world-map/gen_world.py → apply_field_trace.py → tidy_mountains.py（手で編集しない）。"
    new_src = re.sub(r"^// 自動生成: [^\n]*?（手で編集しない）。", head, new_src, count=1)
    open(GEN, "w").write(new_src)
    print("書きかえたマス:", changed, "/", W * H)
    print("前:", sorted(Counter(c for r in g0 for c in r if c in "MNHX").items()), "あと:", sorted(Counter(c for r in g1 for c in r if c in "MNHX").items()))


if __name__ == "__main__":
    main()
