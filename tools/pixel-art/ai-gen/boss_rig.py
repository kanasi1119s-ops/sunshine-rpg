"""ボスの絵を「部品」に描き分けて動かす（2026-10-04、人間の依頼「腕を別の部品として描き分けて、もっと大きく動かす」）。

1枚の絵の腕を、そのまま切り取って回すと、腕の付け根に穴があき、腕の範囲に胴や足が入り、大きく回すと形が崩れた。
そこで、切り絵のアニメーションの作り方（docs/design/pixel-animation-study.md 3節）どおりに、部品を描き分ける。
  胴（いちばん下のレイヤー）: 腕を取り去り、腕に隠れていた胴の横を、近くの胴の色で描き足す
  腕（まん中のレイヤー）: 肩から爪まで。肩の付け根は丸い関節（円）にして、回しても付け根にすき間ができないようにする
  肩当て（いちばん上のレイヤー）: 肩の上の部分。腕の付け根を上からかくす
回すときは RotSprite のやり方（2倍拡大を2回 → 回す → 元の大きさにもどす。4×4のかたまりで多い色を選ぶ）で、ぎざぎざや穴を減らす。

使い方: python3 boss_rig.py 絵.txt パレット.json 部品.json 出力.json
  部品.json: {"arm": {"poly": [[行,列],...], "pivot": [行,列], "lower_from": 行, "joint_r": 半径},
              "shoulder": {"poly": [[行,列],...]}, "hip": 行, "split": 列, "glow": ["記号"]}
  出力.json: {"layers": ["胴","右腕","肩当て"], "walk": [{"胴": 行の並び, "右腕": ..., "肩当て": ...}, ...], "attack": [...],
              "walk_ms": [...], "attack_ms": [...], "flat_walk": [...], "flat_attack": [...], "palette": {...}}
"""
import json
import os
import math
import sys

import numpy as np
from scipy import ndimage

DOT = "."
ROT_MIN = int(os.environ.get("ROT_MIN", "5"))  # 4×4の16票のうち、いくつ以上で点を置くか


def poly_mask(poly, H, W):
    from PIL import Image, ImageDraw
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([(c, r) for r, c in poly], fill=255)
    return np.asarray(im) > 0


def scale2x(g):
    """Scale2x（EPX）: ドット絵の形を保ったまま2倍にする"""
    H, W = g.shape
    P = np.pad(g, 1, mode="edge")
    B, D, F, Hh = P[:-2, 1:-1], P[1:-1, :-2], P[1:-1, 2:], P[2:, 1:-1]
    E = g
    out = np.empty((H * 2, W * 2), dtype=g.dtype)
    c = (B != Hh) & (D != F)
    out[0::2, 0::2] = np.where(c & (D == B), D, E)
    out[0::2, 1::2] = np.where(c & (B == F), F, E)
    out[1::2, 0::2] = np.where(c & (D == Hh), D, E)
    out[1::2, 1::2] = np.where(c & (Hh == F), F, E)
    return out


def rotsprite(part, pivot, ang, scale, H, W, offset=(0, 0)):
    """部品（記号の配列、透明は '.'）を pivot 中心に ang 度（下向きの腕が画面の左へ向く回りが正）・scale 倍にして、
    offset だけずらした H×W の配列を返す。4倍に拡大して回し、4×4ごとに多い記号を選んで元にもどす"""
    big = scale2x(scale2x(part))
    K = 4
    py, px = pivot[0] * K + K / 2, pivot[1] * K + K / 2
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    ys, xs = np.nonzero(big != DOT)
    out = np.full((H, W), DOT, dtype=part.dtype)
    if not len(ys):
        return out
    # 出力の範囲
    vy, vx = (ys - py) * scale, (xs - px) * scale
    ty, tx = py + vx * sa + vy * ca, px + vx * ca - vy * sa
    r0, r1 = int(ty.min() / K) - 1 + offset[0], int(ty.max() / K) + 2 + offset[0]
    c0, c1 = int(tx.min() / K) - 1 + offset[1], int(tx.max() / K) + 2 + offset[1]
    for y in range(max(0, r0), min(H, r1)):
        for x in range(max(0, c0), min(W, c1)):
            votes = {}
            for sy in range(K):
                for sx in range(K):
                    Y = (y - offset[0]) * K + sy + 0.5 - py
                    X = (x - offset[1]) * K + sx + 0.5 - px
                    Y, X = Y / scale, X / scale
                    oy, ox = py + ca * Y - sa * X, px + sa * Y + ca * X
                    iy, ix = int(oy), int(ox)
                    if 0 <= iy < big.shape[0] and 0 <= ix < big.shape[1]:
                        s = big[iy, ix]
                        votes[s] = votes.get(s, 0) + 1
            filled = sum(v for k, v in votes.items() if k != DOT)
            if filled >= ROT_MIN:
                out[y, x] = max((k for k in votes if k != DOT), key=votes.get)
    return out


class Rig:
    def __init__(self, g, pal, parts):
        self.g, self.pal, self.p = g, pal, parts
        H, W = g.shape; self.H, self.W = H, W
        fg = g != DOT
        # 腕（部品）は1本または2本（"arm" ＝右腕、"arm_l" ＝左腕。両手の攻撃に使う）
        cfgs = [("右腕", "肩当て" if "arm_l" not in parts else "右肩当て", parts["arm"], parts["shoulder"])]
        if "arm_l" in parts:
            cfgs.append(("左腕", "左肩当て", parts["arm_l"], parts["shoulder_l"]))
        self.limbs = {}
        cut = np.zeros_like(fg)
        for aname, sname, A, S in cfgs:
            m = poly_mask(A["poly"], H, W) & fg
            lf = A.get("lower_from")
            if lf is not None:   # 手の高さでは、外側のいちばん端のかたまり（手・爪）だけ（太ももが入らないように）
                right = A["pivot"][1] > W / 2
                for y in range(lf, H):
                    xs = np.nonzero(m[y])[0]
                    if not len(xs): continue
                    runs = np.split(xs, np.nonzero(np.diff(xs) > 1)[0] + 1)
                    keep = runs[-1] if right else runs[0]
                    m[y] = False; m[y, keep] = True
            # 指先・爪の足し分（人間の指摘「指先が切れている」）: 外側のかたまりだけを残す決まりだと、
            # 内側へ曲がった指や、はなれた爪が腕から外れて、攻撃のとき胴の側に置き去りになった。
            # rig.json の "extra"（多角形のならび）に入る絵の点は、腕の部品にもどす
            for ep in A.get("extra", []):
                m |= poly_mask(ep, H, W) & fg
            sm = poly_mask(S["poly"], H, W) & fg
            # 腕: 切り取った腕＋付け根の丸い関節（肩の玉）。人間の指摘「攻撃のとき腕が切れている」:
            # 腕の上の端がまっすぐな切り口のままだと、回したときにその切り口とすき間が見えた。
            # 付け根に大きな玉（半径 joint_r）を付け、腕の模様（近くの腕の色）で塗る。玉の上の半分は肩当ての下にかくれる
            arm = np.full_like(g, DOT); arm[m] = g[m]
            jr = A.get("joint_r", 12); py, px = A["pivot"]
            ball = np.zeros_like(fg)
            for y in range(py - jr, py + jr + 1):
                for x in range(px - jr, px + jr + 1):
                    if (y - py) ** 2 + (x - px) ** 2 <= jr * jr and 0 <= y < H and 0 <= x < W:
                        ball[y, x] = True
            fillb = ball & ~m
            if fillb.any():
                _, (iy, ix) = ndimage.distance_transform_edt(~m, return_indices=True)
                arm[fillb] = g[iy[fillb], ix[fillb]]
                # 玉の外側の縁は、腕の色を暗くした色（縁取り）にして形をはっきりさせる
                edge = ball & ~ndimage.binary_erosion(ball) & fillb
                darkest = sorted(set(arm[ball & (arm != DOT)]), key=lambda c: sum(int(pal[c][i:i + 2], 16) for i in (1, 3, 5)))
                if darkest:
                    arm[edge] = darkest[0]
            m = m | ball
            sh = np.full_like(g, DOT); sh[sm] = g[sm]
            self.limbs[aname] = dict(arm=arm, pivot=A["pivot"], mask=m, shoulder=sh, smask=sm, sname=sname)
            cut |= m | sm
        r = self.limbs["右腕"]
        self.arm, self.pivot, self.shoulder = r["arm"], r["pivot"], r["shoulder"]
        m = np.zeros_like(fg); sm = np.zeros_like(fg)
        for L in self.limbs.values():
            m |= L["mask"]; sm |= L["smask"]
        names = ["胴"] + [a for a in ("左腕", "右腕") if a in self.limbs] + [self.limbs[a]["sname"] for a in ("左腕", "右腕") if a in self.limbs]
        self.layers = names
        # 胴（部品）: 腕と肩当てを取り去り、胴の重なっていた所（左右どちらにも近くに胴がある所）を近くの胴の色で描き足す
        body = g.copy(); body[m] = DOT; body[sm] = DOT
        for _ in range(4):
            b = body != DOT
            hole = cut & ~b
            left = np.zeros_like(b); right = np.zeros_like(b)
            for k in range(1, 15):
                left[:, k:] |= b[:, :-k]; right[:, :-k] |= b[:, k:]
            fill = hole & left & right
            if not fill.any(): break
            _, (iy, ix) = ndimage.distance_transform_edt(~b, return_indices=True)
            body[fill] = body[iy[fill], ix[fill]]
        # 肩当ての下（腕の付け根のまわり）も胴で埋めておく（肩当てが動いても穴が見えないように）
        # 肩当ての下は、肩当てが作る影として暗い色で塗る（近くの色を引きのばすと、すじ模様になった）
        b = body != DOT
        under = sm & ~b
        if under.any():
            def lum(c): v = pal[c]; return 0.299 * int(v[1:3], 16) + 0.587 * int(v[3:5], 16) + 0.114 * int(v[5:7], 16)
            used = [c for c in np.unique(g[fg]) if c in pal]
            dark = sorted(used, key=lum)[min(2, len(used) - 1)]
            body[under] = dark
        self.body = body
        ys = np.nonzero(fg)[0]
        self.top, self.foot = int(ys.min()), int(ys.max())
        self.hip = parts.get("hip", int(self.top + (self.foot - self.top) * 0.7))
        self.split = parts.get("split", W // 2)

    def tilt_at(self, y, tilt):
        """上半身の傾き: 足の付け根では0、いちばん上で tilt ドット横へ"""
        return tilt * max(0, self.hip - y) / max(1, self.hip - self.top)

    def warp_body(self, src, dy, sway, lift_l, lift_r, squash=0, tilt=0):
        H, W, hip, foot = self.H, self.W, self.hip, self.foot
        ht = max(1, hip - self.top)
        out = np.full_like(src, DOT)
        for y in range(H):
            for x in range(W):
                if y < hip:
                    d = y - dy
                    sy = hip + (d - hip) * ht / max(1, ht - squash); sx = x - sway - self.tilt_at(y, tilt)
                else:
                    t = min(1.0, (y - hip) / max(1, foot - hip))
                    up = lift_l if x < self.split else lift_r
                    sy, sx = y - (dy * (1 - t) - up * t), x - sway * (1 - t)
                iy, ix = int(round(sy)), int(round(sx))
                if 0 <= iy < H and 0 <= ix < W:
                    out[y, x] = src[iy, ix]
        return out

    def frame(self, dy=0, sway=0, lift_l=0, lift_r=0, squash=0, arm_ang=0.0, arm_scale=1.0, arm_lift=0, tilt=0,
              l_ang=None, l_scale=1.0, l_lift=0):
        """arm_*: 右腕。l_*: 左腕（角度は「下ろした腕が画面の左へ向く回り」が正なので、左腕を体の内側へ回すのはマイナス）。
        l_ang を指定しないときは、右腕と同じ角度（＝歩きで左右の腕が反対に振れる）"""
        out = {"胴": self.warp_body(self.body, dy, sway, lift_l, lift_r, squash, tilt)}
        poses = {"右腕": (arm_ang, arm_scale, arm_lift), "左腕": (arm_ang if l_ang is None else l_ang, l_scale, l_lift)}
        for aname, L in self.limbs.items():
            ang, sc, lift = poses[aname]
            # 腕と肩当ても、上半身の傾きについていく（肩の高さでのずれ）
            tp = int(round(self.tilt_at(L["pivot"][0], tilt)))
            out[aname] = rotsprite(L["arm"], L["pivot"], ang, sc, self.H, self.W, (dy + lift, sway + tp))
            sh = np.full_like(self.g, DOT)
            ys, xs = np.nonzero(L["shoulder"] != DOT)
            for y, x in zip(ys, xs):
                yy, xx = y + dy + min(0, int(lift) // 2), x + sway + int(round(self.tilt_at(y, tilt)))
                if 0 <= yy < self.H and 0 <= xx < self.W:
                    sh[yy, xx] = L["shoulder"][y, x]
            out[L["sname"]] = sh
        return out

    def hand(self, ang, scale=1.0, dy=0, sway=0, lift=0, limb="右腕"):
        L = self.limbs[limb]
        ys, xs = np.nonzero(L["arm"] != DOT); py, px = L["pivot"]
        k = np.argmax((ys - py) ** 2 + (xs - px) ** 2)
        vy, vx = (ys[k] - py) * scale, (xs[k] - px) * scale
        a = math.radians(ang)
        return py + vx * math.sin(a) + vy * math.cos(a) + dy + lift, px + vx * math.cos(a) - vy * math.sin(a) + sway, math.hypot(vy, vx)


def flatten(fr, order=None):
    order = order or [k for k in ("胴", "左腕", "右腕", "左肩当て", "右肩当て", "肩当て") if k in fr]
    out = fr[order[0]].copy()
    for k in order[1:]:
        m = fr[k] != DOT; out[m] = fr[k][m]
    return out


def smear(layer, pivot, a0, a1, radius, dy, cols, H, W, width=16):
    """振りの残像: 肩を中心に、手の通り道の円弧（a0→a1）を帯で描く（外側ほど明るい）"""
    py, px = pivot
    lo, hi = min(a0, a1), max(a0, a1)
    for y in range(H):
        for x in range(W):
            vy, vx = y - dy - py, x - px
            r = math.hypot(vy, vx)
            if radius - width <= r <= radius + 3:
                ang = math.degrees(math.atan2(-vx, vy))
                if lo <= ang <= hi:
                    k = (r - (radius - width)) / (width + 3)
                    # 円弧の両端ほど細く（先端は消えていく）
                    t = (ang - lo) / max(1e-6, hi - lo)
                    if k < 0.25 + 0.6 * abs(t - 0.6):
                        continue
                    layer[y, x] = cols[min(len(cols) - 1, int(k * len(cols)))]
    return layer


def sparks(layer, cy, cx, cols, size, H, W):
    for k in range(8):
        a = k * math.pi / 4 + 0.2
        L = size if k % 2 == 0 else size * 0.6
        for t in range(int(L)):
            y, x = int(round(cy + t * math.sin(a))), int(round(cx + t * math.cos(a)))
            if 0 <= y < H and 0 <= x < W:
                layer[y, x] = cols[0] if t < L * 0.5 else cols[1]
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if abs(dy) + abs(dx) <= 4 and 0 <= cy + dy < H and 0 <= cx + dx < W:
                layer[int(cy + dy), int(cx + dx)] = cols[0]
    return layer


def shift(a, dy, dx):
    out = np.full_like(a, DOT); H, W = a.shape
    out[max(0, dy):H + min(0, dy), max(0, dx):W + min(0, dx)] = a[max(0, -dy):H - max(0, dy), max(0, -dx):W - max(0, dx)]
    return out


DEFAULT = dict(dy=0, sway=0, lift_l=0, lift_r=0, squash=0, arm_ang=0.0, arm_scale=1.0, arm_lift=0)


def lerp(a, b, t):
    """2つの形のあいだのコマ（中割り）。ずらす量は整数に丸める"""
    a = {**DEFAULT, **a}; b = {**DEFAULT, **b}
    out = {}
    for k in DEFAULT:
        v = a[k] + (b[k] - a[k]) * t
        out[k] = v if k in ("arm_ang", "arm_scale") else int(round(v))
    return out


def inbetween(keys, ms, n, skip=()):
    """keys の各あいだに n-1 枚の中割りを入れる。skip のあいだ（例: 振りの一瞬）は入れない。長さは割って配る"""
    out, out_ms, src = [], [], []
    for i, k in enumerate(keys):
        nxt = keys[(i + 1) % len(keys)]
        steps = 1 if i in skip else n
        for j in range(steps):
            out.append(lerp(k, nxt, j / steps)); out_ms.append(max(40, round(ms[i] / steps))); src.append(i if j == 0 else None)
    return out, out_ms, src


def build(g, pal, parts):
    rig = Rig(g, pal, parts)
    H, W = rig.H, rig.W
    spare = [c for c in "0123456789!#$%&" if c not in pal]
    fx = {}
    for k, v in (("a", "#e8fbff"), ("b", "#9ee8ff"), ("c", "#4fb7d8")):
        s = spare.pop(0); fx[k] = s; pal[s] = v
    glow = {}
    for s in parts.get("glow", []):
        c = pal[s]; v = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
        t = spare.pop(0); glow[s] = t; pal[t] = "#%02x%02x%02x" % tuple(min(255, int(x + (255 - x) * 0.6)) for x in v)

    KEYS = ("dy", "sway", "lift_l", "lift_r", "squash", "arm_ang", "arm_scale", "arm_lift", "tilt", "l_ang", "l_scale", "l_lift")
    DEF = dict(dy=0, sway=0, lift_l=0, lift_r=0, squash=0, arm_ang=0.0, arm_scale=1.0, arm_lift=0, tilt=0, l_ang=None, l_scale=1.0, l_lift=0)

    def mix(a, b, t):
        a = {**DEF, **a}; b = {**DEF, **b}
        out = {}
        for k in KEYS:
            if k == "l_ang":   # 左腕の角度を決めていないときは、右腕と同じ角度として混ぜる
                va = a["arm_ang"] if a["l_ang"] is None else a["l_ang"]
                vb = b["arm_ang"] if b["l_ang"] is None else b["l_ang"]
                out[k] = None if (a["l_ang"] is None and b["l_ang"] is None) else va + (vb - va) * t
                continue
            v = a[k] + (b[k] - a[k]) * t
            out[k] = v if k in ("arm_ang", "arm_scale", "l_scale") else int(round(v))
        return out

    def ease(t, kind):
        if kind == "in": return t * t                 # ゆっくり始まる（ため）
        if kind == "out": return 1 - (1 - t) ** 2     # ゆっくり終わる（戻り）
        if kind == "inout": return t * t * (3 - 2 * t)
        return t

    # 歩く（16コマ）: 決めの8ポーズ（接地・沈みこみ・通過・伸び上がり×左右）のあいだに中割りを1コマずつ。
    # 上下が中心・左右は1ドットまで・腕は足と反対（docs/design/pixel-animation-study.md）
    WK = [dict(dy=3), dict(dy=7, sway=1, squash=2, arm_ang=-4),
          dict(dy=1, sway=1, lift_l=18, arm_ang=10, arm_scale=1.04), dict(dy=-3, lift_l=7, arm_ang=6),
          dict(dy=3), dict(dy=7, sway=-1, squash=2, arm_ang=4),
          dict(dy=1, sway=-1, lift_r=18, arm_ang=-10, arm_scale=0.97), dict(dy=-3, lift_r=7, arm_ang=-6)]
    WKMS = [170, 230, 150, 150, 170, 230, 150, 150]
    wpose, walk_ms = [], []
    for k in range(len(WK)):
        a, b = WK[k], WK[(k + 1) % len(WK)]
        wpose.append(mix(a, {}, 0) if False else {**DEF, **a}); walk_ms.append(WKMS[k] // 2 + 10)
        wpose.append(mix(a, b, 0.5)); walk_ms.append(WKMS[k] // 2)
    walk = [rig.frame(**w) for w in wpose]

    # 攻撃: 決めのポーズ（構え→ため→振り上げ→当たり→振り抜け→戻りすぎ→構え）と中割り。
    # ためと戻りはゆっくり（中割り多め）、振り下ろしは速く（残像2コマだけ）、当たりは長めに止める
    def make_attack(REST, UP1, UP2, HIT, FOL, OVR):
        # 片手の攻撃では、左腕は構えのまま（決めていない左腕は右腕と同じ角度になるため、0度にしておく）
        REST, UP1, UP2, HIT, FOL, OVR = [{"l_ang": 0.0, **d} for d in (REST, UP1, UP2, HIT, FOL, OVR)]
        seq = []   # (ポーズ, ミリ秒, 印)
        for t in (0.35, 0.7):            seq.append((mix(REST, UP1, ease(t, "in")), 70, ""))
        seq.append(({**DEF, **UP1}, 90, ""))
        for t in (0.4, 0.75):            seq.append((mix(UP1, UP2, ease(t, "out")), 70, ""))
        seq.append(({**DEF, **UP2}, 330, "hold"))                 # ため: 頭の上で止める
        seq.append((mix(UP2, HIT, 0.25), 45, "smear1"))          # 振り下ろし（残像）
        seq.append((mix(UP2, HIT, 0.62), 45, "smear2"))
        seq.append(({**DEF, **HIT}, 230, "hit"))                  # 当たり
        seq.append(({**DEF, **FOL}, 110, ""))
        for t in (0.5,):                 seq.append((mix(FOL, OVR, ease(t, "out")), 90, ""))
        seq.append(({**DEF, **OVR}, 100, ""))
        for t in (0.5,):                 seq.append((mix(OVR, REST, ease(t, "inout")), 100, ""))
        seq.append(({**DEF, **REST}, 200, ""))
        attack = [rig.frame(**p0) for p0, _, _ in seq]
        attack_ms = [ms for _, ms, _ in seq]
        _, _, rad = rig.hand(150, 0.95)
        for idx, (p0, _, tag) in enumerate(seq):
            if tag == "smear1":
                tp = int(round(rig.tilt_at(rig.pivot[0], p0["tilt"])))
                attack[idx]["右腕"] = smear(attack[idx]["右腕"], (rig.pivot[0], rig.pivot[1] + p0["sway"] + tp), p0["arm_ang"], 150, rad * 1.02, p0["dy"] + p0["arm_lift"], [fx["c"], fx["b"], fx["a"]], H, W)
            if tag == "smear2":
                tp = int(round(rig.tilt_at(rig.pivot[0], p0["tilt"])))
                attack[idx]["右腕"] = smear(attack[idx]["右腕"], (rig.pivot[0], rig.pivot[1] + p0["sway"] + tp), p0["arm_ang"], 130, rad * 1.1, p0["dy"] + p0["arm_lift"], [fx["c"], fx["b"], fx["a"]], H, W)
            if tag == "hit":
                tp = int(round(rig.tilt_at(rig.pivot[0], p0["tilt"])))
                attack[idx]["右腕"] = smear(attack[idx]["右腕"], (rig.pivot[0], rig.pivot[1] + p0["sway"] + tp), p0["arm_ang"], 80, rad * 1.22, p0["dy"] + p0["arm_lift"], [fx["c"], fx["b"]], H, W, 12)
                hy, hx, _ = rig.hand(p0["arm_ang"], p0["arm_scale"], p0["dy"], p0["sway"] + tp, p0["arm_lift"])
                for k in attack[idx]:
                    for s0, t0 in glow.items():
                        attack[idx][k][attack[idx][k] == s0] = t0
                attack[idx]["右腕"] = sparks(attack[idx]["右腕"], int(hy), int(hx), [fx["a"], fx["b"]], 26, H, W)
                for k in attack[idx]:
                    attack[idx][k] = shift(attack[idx][k], 3, 0)
        return attack, attack_ms

    # 攻撃A（腕だけ）: 胴はほとんど動かさない
    attack, attack_ms = make_attack(dict(dy=0), dict(dy=1, arm_ang=60, arm_lift=-2),
                                    dict(dy=-2, sway=1, arm_ang=150, arm_scale=0.95, arm_lift=-4),
                                    dict(dy=7, sway=-2, squash=2, arm_ang=22, arm_scale=1.28, arm_lift=6),
                                    dict(dy=6, sway=-2, squash=1, arm_ang=14, arm_scale=1.2, arm_lift=6), dict(dy=0, arm_ang=-8))
    # 攻撃B（体ごと）: ためで上半身を腕の側へ反らして伸び上がり、左足を上げて踏みこむ準備。
    # 当たりで上半身を打つ向き（体のまん中）へ大きく倒し、沈んで縮む。左足を踏みこむ。振り抜けたあと少し戻りすぎる
    attack2, attack2_ms = make_attack(dict(dy=0),
                                      dict(dy=0, arm_ang=60, arm_lift=-2, tilt=6, lift_l=4),
                                      dict(dy=-5, sway=2, squash=-3, arm_ang=150, arm_scale=0.95, arm_lift=-4, tilt=12, lift_l=12),
                                      dict(dy=10, sway=-4, squash=4, arm_ang=22, arm_scale=1.3, arm_lift=6, tilt=-14),
                                      dict(dy=8, sway=-4, squash=3, arm_ang=14, arm_scale=1.22, arm_lift=6, tilt=-16),
                                      dict(dy=-1, sway=1, arm_ang=-8, tilt=4))
    # 攻撃C（両手）: 両腕を頭の上へ振り上げ（体は伸び上がって反る）→ 両手を体の前へたたきつける（沈んで縮む・大きく揺れる）
    attack3, attack3_ms = [], []
    if "左腕" in rig.limbs:
        R0 = dict(dy=0)
        U1 = dict(dy=0, squash=-1, arm_ang=60, l_ang=-60, arm_lift=-2, l_lift=-2)
        U2 = dict(dy=-6, squash=-4, arm_ang=155, l_ang=-155, arm_scale=0.95, l_scale=0.95, arm_lift=-5, l_lift=-5)
        HT = dict(dy=11, squash=5, arm_ang=18, l_ang=-18, arm_scale=1.3, l_scale=1.3, arm_lift=8, l_lift=8)
        FL = dict(dy=9, squash=4, arm_ang=10, l_ang=-10, arm_scale=1.22, l_scale=1.22, arm_lift=8, l_lift=8)
        OV = dict(dy=-1, arm_ang=-6, l_ang=6)
        seq = []
        for t in (0.35, 0.7): seq.append((mix(R0, U1, ease(t, "in")), 70, ""))
        seq.append(({**DEF, **U1}, 90, ""))
        for t in (0.4, 0.75): seq.append((mix(U1, U2, ease(t, "out")), 70, ""))
        seq.append(({**DEF, **U2}, 380, ""))
        seq.append((mix(U2, HT, 0.25), 45, "smear"))
        seq.append((mix(U2, HT, 0.62), 45, "smear"))
        seq.append(({**DEF, **HT}, 260, "hit"))
        seq.append(({**DEF, **FL}, 120, ""))
        seq.append((mix(FL, OV, ease(0.5, "out")), 90, ""))
        seq.append(({**DEF, **OV}, 100, ""))
        seq.append((mix(OV, R0, ease(0.5, "inout")), 100, ""))
        seq.append(({**DEF, **R0}, 200, ""))
        for p0, ms, tag in seq:
            fr = rig.frame(**p0)
            for limb, ang, sc, lift in (("右腕", p0["arm_ang"], p0["arm_scale"], p0["arm_lift"]), ("左腕", p0["l_ang"], p0["l_scale"], p0["l_lift"])):
                L = rig.limbs[limb]; piv = L["pivot"]
                _, _, rad = rig.hand(155 if limb == "右腕" else -155, 0.95, limb=limb)
                if tag == "smear":
                    hi = 150 if limb == "右腕" else -150
                    fr[limb] = smear(fr[limb], piv, ang, hi, rad * 1.05, p0["dy"] + lift, [fx["c"], fx["b"], fx["a"]], H, W)
                if tag == "hit":
                    fr[limb] = smear(fr[limb], piv, ang, 80 if limb == "右腕" else -80, rad * 1.24, p0["dy"] + lift, [fx["c"], fx["b"]], H, W, 12)
                    hy, hx, _ = rig.hand(ang, sc, p0["dy"], p0["sway"], lift, limb=limb)
                    fr[limb] = sparks(fr[limb], int(hy), int(hx), [fx["a"], fx["b"]], 28, H, W)
            if tag == "hit":
                for k in fr:
                    for s0, t0 in glow.items():
                        fr[k][fr[k] == s0] = t0
                    fr[k] = shift(fr[k], 4, 0)
            attack3.append(fr); attack3_ms.append(ms)
    return rig, walk, walk_ms, attack, attack_ms, attack2, attack2_ms, attack3, attack3_ms, pal


if __name__ == "__main__":
    txt, palp, partp, out = sys.argv[1:5]
    g = np.array([list(r) for r in open(txt).read().split("\n") if r])
    pal = json.load(open(palp)); parts = json.load(open(partp))
    rig, walk, walk_ms, attack, attack_ms, attack2, attack2_ms, attack3, attack3_ms, pal = build(g, pal, parts)
    rows = lambda a: ["".join(r) for r in a]
    lay = lambda fs: [{k: rows(v) for k, v in f.items()} for f in fs]
    partrows = {"胴": rows(rig.body)}
    for aname, L in rig.limbs.items():
        partrows[aname] = rows(L["arm"]); partrows[L["sname"]] = rows(L["shoulder"])
    json.dump({"layers": rig.layers, "parts": partrows,
               "attack3": lay(attack3), "attack3_ms": attack3_ms, "flat_attack3": [rows(flatten(f)) for f in attack3],
               "walk": lay(walk), "attack": lay(attack), "walk_ms": walk_ms, "attack_ms": attack_ms,
               "attack2": lay(attack2), "attack2_ms": attack2_ms, "flat_attack2": [rows(flatten(f)) for f in attack2],
               "flat_walk": [rows(flatten(f)) for f in walk], "flat_attack": [rows(flatten(f)) for f in attack], "palette": pal},
              open(out, "w"), ensure_ascii=False)
    print("部品:", "・".join(rig.layers), "/ 歩く", len(walk), "コマ・攻撃", len(attack), "コマ・体ごと", len(attack2), "コマ・両手", len(attack3), "コマ →", out)
