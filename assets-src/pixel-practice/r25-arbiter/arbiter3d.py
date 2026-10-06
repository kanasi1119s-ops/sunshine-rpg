"""隠しボス「機械の悪神巨人兵」の戦闘の絵（256×256・40色以内。2026-10-06、人間の指示）。
機械の体なので、AIの下絵ではなく、立体の模型（../r17-polish/sdf3d.py のきょり関数）から1ドットずつ描く。
  - 体: 黒鉄の重い鎧（板の継ぎ目・すみの暗さ）に、金のふち飾り。胸に紫に光る核。
  - 頭: 角のある兜と、赤く光る目のすき間。
  - 手: 片手に巨大な刃（前へ斜めに下ろす）。
  - 背: 光の輪（世界の「灯の環」を思わせる輪）と、輪の上の8つの光の珠（8神の数）。
戦闘では敵は左にいて右を向くので、模型を35度まわして、右前を向かせる。光は左上前から。
出力: arbiter.txt / pal-arbiter.json（ゲームの boss:arbiter）。"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "r17-polish"))
import sdf3d  # noqa: E402
from sdf3d import Model, rbox, sphere, ellipsoid, capsule, cyl_y, diff, box, length, render, save  # noqa: E402

YAW = math.radians(35)


SCALE = 0.9


class RotModel(Model):
    """模型ぜんたいを、たての軸のまわりにまわし（前を右へ向ける）、少し小さくして絵に収める。"""
    def _r(self, p):
        c, s = math.cos(YAW), math.sin(YAW)
        x, y, z = p[..., 0], p[..., 1], p[..., 2]
        return np.stack([c * x - s * z, y, s * x + c * z], -1) / SCALE

    def sdf(self, p):
        return super().sdf(self._r(p)) * SCALE

    def material(self, p):
        return super().material(self._r(p))


def torus_z(c, R, r):
    """正面を向いた輪（xy の面にある輪）。"""
    c = np.array(c, float)

    def f(p):
        q = p - c
        return np.sqrt((np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2) - R) ** 2 + q[..., 2] ** 2) - r
    return f


def blade(a, b, w, t, side=(1.0, 0.0, 0.0)):
    """平たい刃: a（柄の根もと）から b（切っ先）へ。w＝幅の半分、t＝厚みの半分。先へ行くほど細くなる。"""
    a = np.array(a, float); b = np.array(b, float)
    u = b - a; Lb = np.linalg.norm(u); u /= Lb
    v = np.array(side, float); v -= u * (v @ u); v /= np.linalg.norm(v)
    n = np.cross(u, v)

    def f(p):
        q = p - a
        x = q @ u; y = q @ v; z = q @ n
        k = np.clip(x / Lb, 0, 1)
        ww = w * (1 - 0.85 * k ** 1.6) + 0.5
        dx = np.maximum(np.maximum(-x, x - Lb), 0)
        return np.sqrt(dx ** 2 + np.maximum(np.abs(y) - ww, 0) ** 2 + np.maximum(np.abs(z) - t, 0) ** 2) + np.minimum(np.maximum(np.maximum(-x, x - Lb), np.maximum(np.abs(y) - ww, np.abs(z) - t)), 0)
    return f


RAMPS = {
    "iron": ["#0e0c14", "#1a1724", "#272336", "#373149", "#4a435e", "#605874", "#7a7090", "#958cab"],
    "gold": ["#3a2408", "#6a4410", "#9a6a1c", "#c8952e", "#e8bf4a", "#fbe58a"],
    "core": ["#2a0a40", "#6a1aa0", "#a040e0", "#d890ff", "#f4e0ff", "#ffffff"],
    "eye": ["#5a0808", "#c01818", "#ff5040", "#ffd0b0"],
    "blade": ["#1c2230", "#34405a", "#56688a", "#8299bc", "#b6c8e2", "#eaf2ff"],
    "joint": ["#08070c", "#141220", "#221e30", "#302a42"],
    "glow": ["#2a0a40", "#6a1aa0", "#a040e0", "#d890ff", "#f4e0ff", "#ffffff"],
}


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return n ^ (n >> 15)


def shade(m, p, n, lum, x, y):
    if m == "core":
        return 0.22 + 0.62 * max(0.0, n[2] * 0.5 + 0.5) ** 2 + 0.14 * lum, m   # 自分で光る（まん中ほど白く、ふちは紫）
    if m == "glow":
        return 0.5 + 0.35 * lum, "core"                               # 光のすじ（鎧の上を走る）
    if m == "eye":
        return 0.6 + 0.4 * lum, m
    if m == "iron":
        # 鎧の板の継ぎ目（体の高さ方向に、ところどころ横のすじ）
        if abs((p[1] + 3) % 14 - 7) < 0.55 and abs(n[1]) < 0.7:
            lum -= 0.16
        lum += ((hn(int(p[0] // 6), int(p[1] // 6), int(p[2] // 6)) % 5) - 2) * 0.012
    if m == "blade":
        lum = 0.15 + 0.85 * lum                                        # 刃は鋼（光を受ける面は白く光る）
        if lum > 0.62:
            lum = min(0.99, lum + 0.2)
    return lum, m


def build():
    m = RotModel()
    for sx in (-1, 1):
        m.add(rbox((sx * 22, 7, 6), (14, 7, 21), 3), "iron")                       # 足
        m.add(rbox((sx * 22, 36, 0), (11, 24, 12), 3), "iron")                     # すね
        m.add(rbox((sx * 22, 30, 11), (9, 14, 3), 2), "gold")                      # すねの金の板
        m.add(sphere((sx * 22, 61, 6), 11), "gold")                                 # ひざ
        m.add(rbox((sx * 20, 82, 0), (13, 19, 13), 4), "iron")                     # もも
        m.add(ellipsoid((sx * 54, 160, 0), (21, 16, 21)), "iron")                  # 肩
        m.add(diff(ellipsoid((sx * 54, 162, 0), (22.5, 15, 22.5)), box((sx * 54, 150, 0), (30, 12, 30))), "gold")   # 肩の金のふち
        m.add(capsule((sx * 60, 172, 0), (sx * 74, 198, -6), 4.5, 1.0), "gold")     # 肩のとげ
        m.add(capsule((sx * 58, 146, 0), (sx * 62, 120, 4), 10.5), "iron")         # 上の腕
        m.add(sphere((sx * 62, 117, 4), 10), "joint")                               # ひじ
        m.add(capsule((sx * 62, 114, 5), (sx * 64, 88, 17), 13), "iron")           # 前の腕（こて）
        m.add(sphere((sx * 64, 81, 21), 11), "iron")                                # こぶし
        m.add(capsule((sx * 9, 194, 0), (sx * 24, 224, -10), 4.2, 1.0), "gold")     # 角
    m.add(rbox((0, 101, 0), (31, 12, 18), 4), "iron")                              # 腰
    m.add(rbox((0, 92, 17), (14, 12, 3), 2), "gold")                               # 前垂れ
    m.add(cyl_y(0, 0, 20, 110, 124), "joint")                                       # 胴のつなぎ
    m.add(rbox((0, 146, 0), (42, 26, 24), 8), "iron")                              # 胸
    for sx in (-1, 1):
        m.add(rbox((sx * 21, 151, 19), (17, 16, 6), 4), "iron")                    # 胸の板
    m.add(diff(rbox((0, 149, 24), (13, 13, 3), 3), sphere((0, 149, 27), 10)), "gold")   # 核の金の枠
    m.add(sphere((0, 149, 25), 9), "core")                                          # 光る核
    m.add(cyl_y(0, 0, 10, 168, 180), "joint")                                       # 首
    m.add(rbox((0, 188, 3), (12, 11, 12), 4), "iron")                              # 頭（兜）
    m.add(rbox((0, 196, 6), (9, 3, 10), 2), "gold")                                 # 兜の金のひたい
    m.add(box((0, 187, 15.2), (9, 1.6, 0.8)), "eye")                               # 目のすき間（赤く光る）
    m.add(blade((-64, 84, 30), (-60, 6, 92), 9, 1.6, side=(1, 0, 0)), "blade")     # 巨大な刃（前へ斜めに下ろす）
    m.add(rbox((-64, 82, 24), (5, 5, 8), 2), "gold")                                # 刃のつば
    # ---- 細かい部品 ----
    for sx in (-1, 1):
        for yy in (98, 106):
            m.add(capsule((sx * 61, yy, 9), (sx * 63, yy - 1, 13), 13.6), "gold") if yy == 98 else None   # こての金の帯
        m.add(rbox((sx * 22, 46, 12.5), (6, 1.2, 0.8), 0.5), "glow")              # すねの光のすじ
        m.add(rbox((sx * 20, 84, 13.4), (1.2, 12, 0.8), 0.5), "glow")             # ももの光のすじ
        m.add(rbox((sx * 30, 94, 15), (8, 10, 2.5), 1.5), "iron")                  # 腰の板（左右）
        m.add(capsule((sx * 30, 170, -22), (sx * 44, 206, -30), 5, 2), "iron")     # 背の排気の筒
        m.add(sphere((sx * 44, 206, -30), 3.5), "core")                            # 筒の先の光
    for k in range(3):
        m.add(rbox((-14 + k * 14, 128, 23.5), (4.5, 1.4, 1.2), 0.6), "joint")     # 胸の下の通気口
    m.add(rbox((0, 136, 25.5), (1.2, 9, 0.8), 0.4), "glow")                       # 核から下へ走る光
    m.add(rbox((16, 152, 25.5), (9, 1.2, 0.8), 0.4), "glow")                      # 核から横へ走る光
    m.add(rbox((-16, 152, 25.5), (9, 1.2, 0.8), 0.4), "glow")
    m.add(rbox((0, 178, 10), (11, 5, 6), 2.5), "iron")                            # あごの守り
    m.add(capsule((0, 200, 4), (0, 206, -8), 3.2, 1.2), "gold")                   # 兜のとさか
    m.add(sphere((64, 84, 33), 9.5), "core")                                       # 左手の光の珠（流星を呼ぶ）
    m.add(torus_z((0, 168, -34), 74, 3.2), "gold")                                  # 背の光の輪
    for k in range(8):
        a = k / 8 * 2 * math.pi + math.pi / 8
        m.add(sphere((74 * math.cos(a), 168 + 74 * math.sin(a), -34), 6.2), "core")    # 輪の上の8つの光
    return m


if __name__ == "__main__":
    img = render(build(), 256, 256, 128, 238, RAMPS, shade_fn=shade, outline="#0a0810", ambient=0.2, front_tilt=12, z0=140.0, max_dist=320.0)
    n = save(img, os.path.join(HERE, "arbiter.txt"), os.path.join(HERE, "pal-arbiter.json"))
    print("arbiter", n, "colors")
