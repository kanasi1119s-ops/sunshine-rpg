"""芯環塔（世界地図のまんなかの塔）。2026-10-05、人間の指示「自然にできたような感じで、もっと高く高く。上の方は雲で見えなく」。
人が積んだ塔ではなく、陥没した穴の底から生えた、ねじれた岩の柱。層になった岩・自然にできた岩の棚（環のように塔をめぐる）・
ほのかに光る石の筋・根のように広がる足もと・洞窟のような入口。上は嵐の雲にのまれて見えない。
88×240（下そろえ）。光は左上。既存作品の塔の絵は写していない。"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 88, 240
PAL = {
    "0": "#14111a", "1": "#221d28", "2": "#332b36", "3": "#4a3f4a", "4": "#655760", "5": "#86767a",   # 岩: 暗→明
    "v": "#2aa6bc", "V": "#9af0f8",                                                                   # 光る筋
    "c": "#2c3042", "C": "#454a60", "d": "#646a84", "D": "#8c92aa", "E": "#b4b8cc",                    # 雲: 暗→明
    "Y": "#ffd27a", "y": "#c07a3a",                                                                   # 入口の灯
}
ROCK = "012345"


def hsh(x, y, k=0):
    h = (x * 374761393 + y * 668265263 + k * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFFFF) / 4294967296


def cx_at(y):
    return 44 + 3.2 * math.sin(y / 37.0) + 1.5 * math.sin(y / 13.0)


def hw_at(y):
    if y < 200:
        return 6 + max(0, y - 20) / 180 * 16 + 1.2 * math.sin(y / 9.0)
    t = (y - 200) / 38
    return 22 + 1.2 * math.sin(y / 9.0) + t * t * 21


def tone(v):
    v = max(0.0, min(0.999, v))
    return ROCK[int(v * len(ROCK))]


def build():
    g = [["."] * W for _ in range(H)]

    def put(x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < W and 0 <= y < H:
            g[y][x] = c

    # 岩の面（たてに長い、大きさのそろわない面の集まり。面ごとに明るさがちがい、すき間は暗い）
    seeds = []
    k = 0
    for y0 in range(0, H, 9):
        for i in range(7):
            k += 1
            seeds.append((cx_at(y0) + (hsh(k, 1, 3) - 0.5) * 2.2 * hw_at(y0), y0 + hsh(k, 2, 3) * 9, (hsh(k, 3, 3) - 0.5) * 0.3))
    for y in range(0, H - 2):
        c = cx_at(y)
        hw = hw_at(y)
        # ふちのでこぼこ（高さごとに、左右の出っぱりがちがう）
        jl = 1 + 2.5 * hsh(y // 4, 1, 1)
        jr = 1 + 2.5 * hsh(y // 4, 2, 1)
        for x in range(W):
            dx = x + 0.5 - c
            if dx < -hw - jl + 2 or dx > hw + jr - 2:
                continue
            u = max(-1.0, min(1.0, dx / hw))
            near = sorted(((x + 0.5 - sx) ** 2 + ((y + 0.5 - sy) * 0.55) ** 2, sv) for sx, sy, sv in seeds if abs(sy - y) < 18)
            d0, sv = near[0]
            d1 = near[1][0] if len(near) > 1 else d0 + 99
            nz = math.sqrt(max(0.0, 1 - u * u))
            light = 0.5 - u * 0.42 + nz * 0.1 + sv
            if math.sqrt(d1) - math.sqrt(d0) < 0.7:
                light = min(light, 0.2) if u > -0.6 else light - 0.25          # 面のすき間
            if y > 205:
                light -= (y - 205) / 55
            put(x, y, tone(light))
    # ---- 光る石の筋（柱をのぼる、ジグザグの細い筋）
    x = cx_at(232) - 6
    for y in range(230, 70, -1):
        x += math.sin(y / 5.0) * 0.6 + (0.4 if y % 23 < 11 else -0.4)
        xi = int(round(x))
        if g[y][xi] in ROCK:
            put(xi, y, "V" if y % 17 == 0 else "v")
    for (yy, xx) in ((150, 2), (96, -4), (188, 5)):
        x0 = int(cx_at(yy) + xx)
        for k in range(5):
            if g[yy - k][x0 + k // 2] in ROCK:
                put(x0 + k // 2, yy - k, "v")
    # ---- 入口（根もとの洞窟。奥にあたたかい灯）
    ex = int(cx_at(224))
    for y in range(212, 236):
        for x in range(ex - 7, ex + 8):
            rr = 7
            yy = y - 219
            if (yy >= 0 and abs(x + 0.5 - ex) <= rr) or math.hypot(x + 0.5 - ex, yy) <= rr:
                put(x, y, "0" if abs(x + 0.5 - ex) > 3 or y < 226 else ("Y" if y > 231 else "y"))
    for y in range(213, 236):
        put(ex - 8, y, "5"); put(ex + 8, y, "1")
    # ---- 足もとのがれき
    for (rx_, ry_) in ((8, 234), (16, 237), (70, 235), (79, 237), (25, 238), (62, 238)):
        for dy in range(3):
            for dx in range(4):
                put(rx_ + dx, ry_ + dy, tone(0.6 - dx * 0.12 - dy * 0.15))
    # ---- 嵐の雲（上の方をのみこむ。下のふちはちぎれた雲）
    puffs = []
    for k in range(14):
        px = 4 + k * 6.3 + (hsh(k, 1, 9) - 0.5) * 6
        py = 40 + (hsh(k, 2, 9) - 0.5) * 22
        pr = 13 + hsh(k, 3, 9) * 10
        puffs.append((px, py, pr))
    puffs += [(44, 18, 26), (20, 22, 18), (68, 20, 20), (44, 58, 15), (30, 64, 10), (58, 66, 11)]
    for y in range(0, 82):
        for x in range(W):
            best = None
            for (px, py, pr) in puffs:
                d = math.hypot(x + 0.5 - px, (y + 0.5 - py) * 1.25) / pr
                if d <= 1 and (best is None or d < best[0]):
                    best = (d, px, py, pr)
            if best is None:
                continue
            d, px, py, pr = best
            # 雲のかたまり: 左上が明るく、下が暗い
            l = 0.55 - (x + 0.5 - px) / pr * 0.25 - (y + 0.5 - py) / pr * 0.45
            if d > 0.86:
                l -= 0.25
            l -= max(0, y - 50) / 60
            c = "cCdDE"[max(0, min(4, int(l * 5)))]
            put(x, y, c)
    # ちぎれた雲のすそ（点々と、柱の上にかかる）
    for y in range(66, 92):
        for x in range(W):
            if hsh(x, y, 13) > 0.86 + (y - 66) / 40 and g[y][x] in ROCK + ".":
                put(x, y, "c" if g[y][x] != "." else "C")
    rows = ["".join(r) for r in g]
    used = set("".join(rows)) - {"."}
    assert len(used) <= 16, len(used)
    with open(os.path.join(HERE, "spire-natural.txt"), "w") as f:
        f.write("\n".join(rows) + "\n")
    with open(os.path.join(HERE, "pal-spire-natural.json"), "w") as f:
        json.dump({k: v for k, v in PAL.items() if k in used}, f, ensure_ascii=False)
    print("色数", len(used))


if __name__ == "__main__":
    build()
