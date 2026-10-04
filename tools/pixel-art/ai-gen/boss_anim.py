"""ボスの絵（256×256の文字グリッド）から、歩く動きと攻撃の動きのコマを作る（2026-10-04、人間の依頼）。

作り方（ドット絵アニメーションの基本に合わせる。docs/design/pixel-animation-study.md）:
  大きな絵は、腕・足を「部品」として切り分け、関節（肩・足の付け根）を中心に回したり動かしたりして重ねる（切り絵の動かし方）。
  回すときは最近傍で、ぼかさない。体（胴）は、上下に弾むだけ。
  歩く（8コマ）: 接地 → 沈みこみ（いちばん低い）→ 通過（片足を上げる）→ 伸び上がり（いちばん高い）を左右で。
               動きの中心は上下。左右のゆれは1ドットまで。腕は足と反対に振る。重いボスなのでゆっくり、沈みこみを長めに。
  攻撃（7コマ）: 構え → ため（腕を後ろ上へ大きく引き、体を少し沈める。長めに止める）→ 振りの途中（残像のコマ）
               → 当たり（腕を前へ振り抜き、手が手前に来るので少し大きく。光・火花・画面の揺れ。長めに止める）
               → 振り抜けたあと → 戻りすぎ（少しはね返る）→ 構えに戻る
使い方: python3 boss_anim.py 絵.txt パレット.json 部品.json 出力.json
  部品.json: {"right_arm": {"poly": [[行,列],...], "pivot": [行,列]}, "left_arm": {...}, "hip": 行, "split": 列,
              "glow": ["記号",...]（当たりで明るくする記号）, "attack_arm": "right_arm"}
  出力.json: {"walk": [コマ...], "attack": [...], "walk_ms": [...], "attack_ms": [...], "palette": {...}}
"""
import json
import math
import sys

import numpy as np


def poly_mask(poly, H, W):
    from PIL import Image, ImageDraw
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([(c, r) for r, c in poly], fill=255)
    return np.asarray(im) > 0


def sample(g, sy, sx):
    H, W = g.shape
    sy, sx = int(round(sy)), int(round(sx))
    return g[sy, sx] if 0 <= sy < H and 0 <= sx < W else "."


class Rig:
    def __init__(self, g, parts):
        self.g = g; self.H, self.W = g.shape; self.p = parts
        fg = g != "."
        self.arms = {}
        for name in ("left_arm", "right_arm"):
            if name in parts:
                m = poly_mask(parts[name]["poly"], self.H, self.W) & fg
                # 手の高さ（lower_from 行より下）では、外側のいちばん端のかたまり（手・爪）だけを腕にする。
                # 内側の太もも・腰が腕といっしょに動いてしまうのを防ぐ（人間の指摘「足の一部も攻撃モーションに巻き込まれてる」）
                lf = parts[name].get("lower_from")
                if lf is not None:
                    outer_right = parts[name]["pivot"][1] > self.W / 2
                    for y in range(lf, self.H):
                        xs = np.nonzero(m[y])[0]
                        if not len(xs): continue
                        runs = np.split(xs, np.nonzero(np.diff(xs) > 1)[0] + 1)
                        keep = runs[-1] if outer_right else runs[0]
                        m[y] = False; m[y, keep] = True
                self.arms[name] = (m, parts[name]["pivot"])
        self.body = g.copy()
        cut = np.zeros_like(fg)
        for m, _ in self.arms.values():
            self.body[m] = "."; cut |= m
        # 腕を切り取ったあとの穴: 左右どちらにも近く（12ドット以内）に胴があるマスは、胴の重なっていた所なので、近くの胴の色で埋める
        from scipy import ndimage
        for _ in range(3):
            b = self.body != "."
            hole = cut & ~b
            if not hole.any(): break
            left = np.zeros_like(b); right = np.zeros_like(b)
            for k in range(1, 13):
                left[:, k:] |= b[:, :-k]; right[:, :-k] |= b[:, k:]
            fill = hole & left & right
            if not fill.any(): break
            _, (iy, ix) = ndimage.distance_transform_edt(~b, return_indices=True)
            self.body[fill] = self.body[iy[fill], ix[fill]]
        ys = np.nonzero(fg)[0]
        self.foot = int(ys.max()); self.hip = parts.get("hip", int(ys.min() + (ys.max() - ys.min()) * 0.7))
        self.split = parts.get("split", self.W // 2)

    def body_frame(self, dy, sway, lift_l, lift_r, squash=0):
        """胴は dy だけ上下（下が正）。squash: 沈みこみで胴を少し縮める行数。足は付け根から足先へ、上げる量をなめらかに混ぜる"""
        H, W, hip, foot = self.H, self.W, self.hip, self.foot
        out = np.full_like(self.g, ".")
        top = int(np.nonzero(self.g != ".")[0].min())
        ht = max(1, hip - top)
        for y in range(H):
            for x in range(W):
                if y < hip:
                    # 胴: dy だけ上下し、squash 行ぶん縦に縮める（足の付け根の高さは保つ）
                    d = y - dy
                    sy = hip + (d - hip) * ht / max(1, ht - squash)
                    sx = x - sway
                else:
                    t = min(1.0, (y - hip) / max(1, foot - hip))
                    up = lift_l if x < self.split else lift_r
                    d = dy * (1 - t) - up * t
                    sy, sx = y - d, x - sway * (1 - t)
                out[y, x] = sample(self.body, sy, sx)
        return out

    def put_arm(self, frame, name, ang, scale=1.0, dy=0, sway=0, offset=(0, 0)):
        """腕を肩（pivot）中心に ang 度回し（画面で時計回りが正）、scale 倍にして、胴の動きに合わせて重ねる"""
        m, (py, px) = self.arms[name]
        H, W = self.H, self.W
        a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
        ys, xs = np.nonzero(m)
        # 出力の範囲（回したあとの外接四角）を求め、そこだけ逆にたどる
        corners = []
        for y, x in ((ys.min(), xs.min()), (ys.min(), xs.max()), (ys.max(), xs.min()), (ys.max(), xs.max())):
            vy, vx = (y - py) * scale, (x - px) * scale
            corners.append((py + vx * sa + vy * ca, px + vx * ca - vy * sa))
        r0 = int(min(c[0] for c in corners)) - 2; r1 = int(max(c[0] for c in corners)) + 3
        c0 = int(min(c[1] for c in corners)) - 2; c1 = int(max(c[1] for c in corners)) + 3
        for y in range(max(0, r0 + dy + offset[0]), min(H, r1 + dy + offset[0])):
            for x in range(max(0, c0 + sway + offset[1]), min(W, c1 + sway + offset[1])):
                vy, vx = (y - dy - offset[0] - py) / scale, (x - sway - offset[1] - px) / scale
                sy, sx = py + vx * -sa + vy * ca, px + vx * ca + vy * sa
                iy, ix = int(round(sy)), int(round(sx))
                if 0 <= iy < H and 0 <= ix < W and m[iy, ix]:
                    frame[y, x] = self.g[iy, ix]
        return frame

    def hand(self, name, ang, scale=1.0, dy=0, sway=0):
        """腕の先（肩からいちばん遠い点）が、回したあとどこに来るか"""
        m, (py, px) = self.arms[name]
        ys, xs = np.nonzero(m)
        k = np.argmax((ys - py) ** 2 + (xs - px) ** 2)
        vy, vx = (ys[k] - py) * scale, (xs[k] - px) * scale
        a = math.radians(ang)
        return py + vx * math.sin(a) + vy * math.cos(a) + dy, px + vx * math.cos(a) - vy * math.sin(a) + sway, math.hypot(vy, vx)


def smear(frame, rig, name, a0, a1, radius, dy, cols):
    """振りの残像: 肩を中心に、腕の長さの円弧を a0→a1 の向きに帯で描く（外側ほど明るい）"""
    _, (py, px) = rig.arms[name]
    H, W = frame.shape
    lo, hi = min(a0, a1), max(a0, a1)
    for y in range(H):
        for x in range(W):
            vy, vx = y - dy - py, x - px
            r = math.hypot(vy, vx)
            if radius - 14 <= r <= radius + 3:
                # 下向き（腕を下ろした向き）を0度、時計回りを正とした角度
                ang = math.degrees(math.atan2(-vx, vy))
                if lo <= ang <= hi:
                    k = (r - (radius - 14)) / 17
                    if frame[y, x] == "." or k > 0.45:
                        frame[y, x] = cols[min(len(cols) - 1, int(k * len(cols)))]
    return frame


def sparks(frame, cy, cx, cols, size=16):
    """当たりの火花: 中心から8方向に光の線"""
    H, W = frame.shape
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        L = size if k % 2 == 0 else size * 0.6
        for t in range(int(L)):
            y, x = int(round(cy + t * math.sin(a))), int(round(cx + t * math.cos(a)))
            if 0 <= y < H and 0 <= x < W:
                frame[y, x] = cols[0] if t < L * 0.5 else cols[1]
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if abs(dy) + abs(dx) <= 3 and 0 <= cy + dy < H and 0 <= cx + dx < W:
                frame[int(cy + dy), int(cx + dx)] = cols[0]
    return frame


def shift(frame, dy, dx):
    out = np.full_like(frame, ".")
    H, W = frame.shape
    out[max(0, dy):H + min(0, dy), max(0, dx):W + min(0, dx)] = frame[max(0, -dy):H - max(0, dy), max(0, -dx):W - max(0, dx)]
    return out


def build(g, pal, parts):
    rig = Rig(g, parts)
    L, R = "left_arm", "right_arm"
    have = lambda n: n in rig.arms

    def pose(dy, sway, lift_l, lift_r, arm_l=0.0, arm_r=0.0, squash=0):
        f = rig.body_frame(dy, sway, lift_l, lift_r, squash)
        if have(L): rig.put_arm(f, L, arm_l, 1.0, dy, sway)
        if have(R): rig.put_arm(f, R, arm_r, 1.0, dy, sway)
        return f

    # 歩く: (胴の上下, 左右ゆれ, 左足を上げる量, 右足を上げる量, 左腕の角度, 右腕の角度, 胴の縮み)
    # 左足を前に出す（上げる）ときは、右腕を前に振る（反対の腕）
    W8 = [(3, 0, 0, 0, 0, 0, 0),      # 接地
          (7, 1, 0, 0, 2, -2, 2),     # 沈みこみ（いちばん低い・胴を少し縮める）
          (1, 1, 18, 0, 5, -7, 0),    # 通過（左足を上げる。右腕を前へ）
          (-3, 0, 7, 0, 3, -4, 0),    # 伸び上がり（いちばん高い）
          (3, 0, 0, 0, 0, 0, 0),      # 接地
          (7, -1, 0, 0, -2, 2, 2),    # 沈みこみ
          (1, -1, 0, 18, 7, -5, 0),   # 通過（右足を上げる。左腕を前へ）
          (-3, 0, 0, 7, 4, -3, 0)]    # 伸び上がり
    walk = [pose(*w) for w in W8]
    walk_ms = [170, 230, 150, 150, 170, 230, 150, 150]

    A = parts.get("attack_arm", R)
    other = L if A == R else R
    sgn = -1 if A == R else 1          # 角度は「下ろした腕が画面の左へ向く回り」が正。右腕を外側・上へ上げるのはマイナス
    glow = {}
    spare = [c for c in "0123456789" if c not in pal]
    for s in parts.get("glow", []):
        c = pal[s]; v = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
        glow[s] = spare.pop(0); pal[glow[s]] = "#%02x%02x%02x" % tuple(min(255, int(x + (255 - x) * 0.6)) for x in v)
    fx = {"a": "#e8fbff", "b": "#9ee8ff", "c": "#4fb7d8"}
    fxs = {}
    for k, v in fx.items():
        s = spare.pop(0); fxs[k] = s; pal[s] = v

    def apose(dy, ang, scale=1.0, lean=0, other_ang=0.0, lift=0):
        """ang: 腕の角度（度）。lift: 肩ごと腕を上下にずらす量（上がマイナス）"""
        f = rig.body_frame(dy, lean, 0, 0)
        if have(other): rig.put_arm(f, other, other_ang, 1.0, dy, lean)
        rig.put_arm(f, A, ang, scale, dy, lean, (lift, 0))
        return f

    # 攻撃: 正面向きの大きなボスは、腕を頭の上へ回すと形が崩れ、胸の前を横切ると胸と同じ色で見えなくなる。
    # そこで「横へ引いて肩を上げる（ため）→ 爪を手前・下へ突き出す（手前に来るので大きく描く）」で見せる。
    out_ = sgn                                             # 外側へ開く向き（右腕ならマイナス）
    in_ = -sgn                                             # 体の内側へ向く向き
    a1 = apose(2, out_ * 28, 0.98, -in_ * 1, in_ * 3, -10)     # ため1: 腕を横へ引き、肩を上げる
    a2 = apose(4, out_ * 40, 0.94, -in_ * 2, in_ * 5, -16)     # ため2: いちばん引く（小さく＝奥へ）。長めに止める
    a3 = apose(3, in_ * 6, 1.10, in_ * 1, in_ * 2, -4)         # 突き出しの途中（残像）
    _, _, rad = rig.hand(A, out_ * 40, 0.94, 4 - 16)
    a3 = smear(a3, rig, A, min(out_ * 40, in_ * 6), max(out_ * 40, in_ * 6), rad, 4 - 16, [fxs["c"], fxs["b"], fxs["a"]])
    a4 = apose(6, in_ * 22, 1.32, in_ * 2, -in_ * 2, 8)        # 当たり: 爪を手前・下へ（大きく）。長めに止める
    hy, hx, _ = rig.hand(A, in_ * 22, 1.32, 6 + 8, in_ * 2)
    a4 = smear(a4, rig, A, min(in_ * 6, in_ * 22), max(in_ * 6, in_ * 22), rad * 1.25, 6 + 8, [fxs["c"], fxs["b"]])
    for s0, t0 in glow.items():
        a4[a4 == s0] = t0
    a4 = sparks(a4, int(hy), int(hx), [fxs["a"], fxs["b"]], 26)
    a4 = shift(a4, 3, 0)                                   # 画面の揺れ（下へ）
    a5 = apose(5, in_ * 26, 1.24, in_ * 2, -in_ * 1, 10)       # 振り抜けたあと
    a6 = apose(1, out_ * 6, 1.0, -in_ * 1, 0, -2)              # 戻りすぎ（少しはね返る）
    a7 = apose(0, 0, 1.0, 0, 0, 0)                             # 構え
    attack = [a1, a2, a3, a4, a5, a6, a7]
    attack_ms = [180, 360, 70, 240, 150, 120, 220]
    return walk, walk_ms, attack, attack_ms, pal


if __name__ == "__main__":
    txt, palp, partp, out = sys.argv[1:5]
    g = np.array([list(r) for r in open(txt).read().split("\n") if r])
    pal = json.load(open(palp)); parts = json.load(open(partp))
    walk, walk_ms, attack, attack_ms, pal = build(g, pal, parts)
    j = lambda fs: [["".join(r) for r in f] for f in fs]
    json.dump({"walk": j(walk), "attack": j(attack), "walk_ms": walk_ms, "attack_ms": attack_ms, "palette": pal}, open(out, "w"))
    print("歩く", len(walk), "コマ・攻撃", len(attack), "コマ →", out)
