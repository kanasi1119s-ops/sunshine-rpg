"""芯環塔のまわりの大滝（1枚の絵・8コマ）。2026-10-05、人間の指示「滝もっとリアルに」「ドット絵はすべてこだわって」。
マスごとに描くと、ふちが階段になり、滝がブロックに見えたので、穴のまわり全体を1枚の絵として、1ドットずつ描く。
- 穴のふちは、なめらかな円。ふちの外（円の帯）は、海の水が穴へ向かって走る水面。ふちに近いほど白い泡が多い。
- 奥の崖（見下ろすと見える、穴の向こう側の壁）を、水がひとつながりのカーテンになって、穴の底まで流れ落ちる。
  光は左上から。崖の正面は明るく、左右のはしは崖が向こうへ回りこむので暗く細く見える。白い筋が下へ流れる。
- 底は、水しぶきの霧の帯。その下は、深い闇。手前のふちは、水が向こうへ越えていく白い泡と、のぼる水しぶき。
- 色は、計算した色を、手で選んだ水・泡・霧・闇の色の表にそろえる（1ドットごと）。16コマで1周（模様は流れの向きにくり返すので、ずらすだけで切れ目なく1周する）。
出力: basin-0..15.txt / pal-basin-*.json（288×288。まん中が塔のマスのまん中）と、src/assets/falls/basin.png（横に16コマ）。"""
import json
import math
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
S = 288
C = S / 2
T = 16.0
PIT_R = 6.6 * T          # 穴のふち（world-map.ts の BASIN_PIT_R と同じ）
RIM_R = 8.4 * T          # 水面の帯の外がわ（BASIN_RIM_R）
DEPTH = 6.2 * T          # 穴の深さ（見下ろしたとき、底の円が下へずれる量）
FRAMES = 16

PAL = {
    "a": (8, 9, 16), "b": (16, 19, 30), "c": (26, 32, 50),                     # 闇
    "d": (20, 52, 92), "e": (30, 74, 124), "f": (44, 100, 158), "g": (70, 132, 190),   # 水
    "h": (108, 168, 220), "i": (156, 204, 240), "j": (208, 234, 252), "k": (255, 255, 255),   # 水の光・泡
    "l": (120, 136, 160), "m": (168, 184, 204), "n": (204, 216, 230),          # 霧
    "o": (40, 48, 66), "p": (64, 74, 96),                                       # 崖の岩（水のすき間に見える）
}
KEYS = list(PAL)


def hsh(x, y, k=0):
    h = (int(x) * 374761393 + int(y) * 668265263 + k * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFFFF) / 4294967296


def vnoise(x, y, s, k=0):
    gx, gy = x / s, y / s
    x0, y0 = math.floor(gx), math.floor(gy)
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = hsh(x0, y0, k); b = hsh(x0 + 1, y0, k); c = hsh(x0, y0 + 1, k); d = hsh(x0 + 1, y0 + 1, k)
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def vnoise_py(x, y, sx, sy, k, period):
    """たて（流れの向き）に、period ドットでくり返す雑音。流れをずらしても、1周でぴったり元にもどる。"""
    gx, gy = x / sx, y / sy
    ny = max(1, round(period / sy))
    x0, y0 = math.floor(gx), math.floor(gy)
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    ya, yb = y0 % ny, (y0 + 1) % ny
    a = hsh(x0, ya, k); b = hsh(x0 + 1, ya, k); c = hsh(x0, yb, k); d = hsh(x0 + 1, yb, k)
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def vn2(x, y, sx, sy, k=0):
    """のびた雑音（横 sx・たて sy の大きさのちがう格子）。流れに沿った長い筋を作る。"""
    return vnoise(x / sx * 8, y / sy * 8, 8, k)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def nearest(rgb):
    best, bk = 1e18, "a"
    for k in KEYS:
        c = PAL[k]
        d = (c[0] - rgb[0]) ** 2 * 0.3 + (c[1] - rgb[1]) ** 2 * 0.59 + (c[2] - rgb[2]) ** 2 * 0.11
        if d < best:
            best, bk = d, k
    return bk


def water(v):
    """0〜1の明るさを、水の色の帯（暗い水→光る水）へ。"""
    ramp = [PAL["d"], PAL["e"], PAL["f"], PAL["g"], PAL["h"], PAL["i"], PAL["j"]]
    v = max(0.0, min(0.999, v)) * (len(ramp) - 1)
    i = int(v)
    return mix(ramp[i], ramp[i + 1], v - i)


def loop(fn, fr, step):
    """流れる模様を、コマごとに step ドットずつ本当にずらす（模様は流れの向きにくり返すので、1周で切れ目なくもどる）。"""
    return fn(fr * step)


def pixel(x, y, fr):
    px, py = x + 0.5 - C, y + 0.5 - C
    r = math.hypot(px, py)
    # ---------- 水面の帯（ふちの外）: 穴へ向かって荒々しく走る水。白い波がしら・泡のかたまり。外のふちは海へ溶ける
    if PIT_R < r <= RIM_R:
        out = (r - PIT_R) / (RIM_R - PIT_R)          # 0=ふち、1=外
        if out > 0.82 and hsh(x, y, 3) < (out - 0.82) / 0.18:
            return None
        ang = math.atan2(py, px)
        lane = ang * PIT_R
        streak = loop(lambda f: vnoise_py(lane, r + f, 2.2, 16, 1, 32) * 0.7 + vnoise_py(lane, r + f, 1.2, 8, 3, 32) * 0.3, fr, 2)
        chop = loop(lambda f: vnoise_py(lane, r + f, 1.0, 4, 2, 32), fr, 2)       # 波がしら（細かく荒い）
        v = 0.3 + (streak - 0.5) * 0.65 + (1 - out) * 0.25
        foam = (1 - out) ** 2.0 * 1.25 + (chop - 0.5) * 0.9
        if foam > 0.78:
            return PAL["k"] if foam > 1.02 else PAL["j"]
        if foam > 0.58 or chop > 0.8:
            return PAL["i"]
        if streak > 0.7:
            v += 0.25
        if streak < 0.28:
            v -= 0.18                                # 深くえぐれた波の谷
        return water(v)
    if r > RIM_R:
        return None
    # ---------- 穴の中
    floor_top = DEPTH - math.sqrt(max(0.0, PIT_R ** 2 - px ** 2))
    lip_y = -math.sqrt(max(0.0, PIT_R ** 2 - px ** 2))
    front_lip = math.sqrt(max(0.0, PIT_R ** 2 - px ** 2))
    if py < floor_top:
        # 奥の崖を流れ落ちる水のカーテン（荒々しく: 太い白い筋・ちぎれる水のかたまり・崖の段で白くはじける帯）
        u = px / PIT_R
        fall = (py - lip_y) / max(1.0, floor_top - lip_y)
        col = math.asin(max(-1.0, min(1.0, u))) * 60
        streak = loop(lambda f: vnoise_py(col, py - f, 1.6, 16, 5, 64) * 0.6 + vnoise_py(col, py - f, 0.9, 8, 6, 64) * 0.4, fr, 4)
        clump = loop(lambda f: vnoise_py(col, py - f, 2.4, 4, 12, 64), fr, 4)
        side = math.sqrt(max(0.0, 1 - u * u))
        light = 0.25 + side * 0.45 - u * 0.18
        v = light + (streak - 0.5) * 0.8 - fall * 0.1
        # 落ち口: ふくらんで、ところどころ盛り上がって越える（高さが場所と時間で変わる）
        surge = 0.04 + vnoise_py(col * 0.5, fr * 2, 3, 8, 13, 32) * 0.06      # 落ち口の盛り上がり（16コマで1周）
        if fall < surge:
            return PAL["k"] if (x + fr) % 3 else PAL["j"]
        # 崖の段で、水が白くはじける帯
        for step_at in (0.34, 0.58):
            d = abs(fall - step_at - (vnoise(col, 0, 6, 14) - 0.5) * 0.05)
            if d < 0.025 + clump * 0.035 and vnoise(col + step_at * 50, 0, 9, 18) > 0.42:   # 段は、ところどころだけ
                return PAL["k"] if clump > 0.55 else PAL["j"]
        if streak > 0.7 and fall < 0.85:
            return PAL["k"] if streak > 0.86 else (PAL["j"] if streak > 0.78 else PAL["i"])
        if clump > 0.82:
            return PAL["j"]                          # ちぎれて落ちる水のかたまり
        if streak < 0.22:
            v -= 0.2                                 # 水の薄いところ（暗い）
        rgb = water(v)
        # 底から立ちのぼる、強い水しぶき（ふくらんで、上へ高くのびる）
        puff = loop(lambda f: vnoise_py(px * 0.9, py + f, 9, 8, 7, 32) * 0.6 + vnoise_py(px, py + f, 4, 4, 15, 32) * 0.4, fr, -2)   # 霧は上へわき上がる
        mist = (fall - 0.42) / 0.58 * 1.25 + (puff - 0.5) * 1.1
        if mist > 0.5:
            return PAL["k"] if mist > 1.25 else (PAL["n"] if mist > 0.95 else (PAL["m"] if mist > 0.72 else PAL["l"]))
        # 水しぶきの粒（霧の上に、はね上がる白い粒）
        if fall > 0.35 and hsh(x, (y + fr * 2) % 32 // 2 + y // 32 * 100, 16) > 0.985:
            return PAL["k"]
        return rgb
    # 手前のふち: 水が向こうへ越えていく泡と、強くのぼる水しぶき
    if py > front_lip - 16:
        k = (front_lip - py) / 16
        spray = loop(lambda f: vnoise_py(px, py + f, 3, 4, 8, 32), fr, -2)
        if spray > 0.3 + k * 0.55:
            return PAL["k"] if k < 0.35 else (PAL["j"] if k < 0.6 else PAL["n"])
        if hsh(x, (y + fr * 2) % 32 // 2 + y // 32 * 100, 17) > 0.96:
            return PAL["k"]
        return PAL["i"] if k < 0.18 else PAL["c"]
    deep = 1 - (py - floor_top) / max(1.0, front_lip - floor_top)
    wisp = vnoise_py(py, px + fr * 2, 4, 16, 9, 32)                          # 底の霧は、横へゆっくり流れる（16コマで1周）
    if wisp > 0.72 and deep > 0.35:
        return PAL["o"] if wisp < 0.82 else PAL["p"]
    return mix(PAL["a"], PAL["c"], deep * 0.6)


def frame(fr):
    rows = []
    for y in range(S):
        line = []
        for x in range(S):
            rgb = pixel(x, y, fr)
            line.append("." if rgb is None else nearest(rgb))
        rows.append("".join(line))
    return rows


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.new("RGBA", (S * FRAMES, S), (0, 0, 0, 0))
    for fr in range(FRAMES):
        rows = frame(fr)
        used = sorted(set("".join(rows)) - {"."})
        with open(os.path.join(HERE, f"basin-{fr}.txt"), "w") as f:
            f.write("\n".join(rows) + "\n")
        with open(os.path.join(HERE, f"pal-basin-{fr}.json"), "w") as f:
            json.dump({k: "#%02x%02x%02x" % PAL[k] for k in used}, f)
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch != ".":
                    sheet.putpixel((fr * S + x, y), PAL[ch] + (255,))
    sheet.save(os.path.join(OUT, "basin.png"))
    print("ok")
