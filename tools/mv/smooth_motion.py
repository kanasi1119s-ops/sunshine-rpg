#!/usr/bin/env python3
"""テトの動きを、なめらかにする（2026-10-29 人間「なめらかにならない」）。

これまでの問題（並び *.seq.json を数えた結果。01番の曲）:
  ・1秒に約1.7回、動きの向きが急に反対になる（行って戻る）。3コマしか同じ向きに進まない所もある → カクッと見える
  ・離れたコマへ飛ぶ所が約150回 → 姿がポンと入れかわって見える
  ・24コマ/秒のまま、同じコマが2回続く所もある → 動きが止まって見える

このしくみ:
  1. 並び（24コマ/秒の整数のコマ番号）を、飛ぶ所で区切る
  2. 区切りの中では、コマ番号の流れを、ガウスでならした「なめらかな位置」（小数）にする
     → 向きが変わる所は、ぴたっと止まらず、ゆっくり減速して、ゆっくり戻る（振り子のように）
  3. 書き出しのコマ数を 48 コマ/秒にして、各コマの位置（小数）を、なめらかな位置から読む
  4. 小数の位置の絵は、となりの2コマのあいだを「動きの流れ（オプティカルフロー）」で補間して作る（ただ重ねると二重に見えるので、絵を動かして合わせる）
  5. 飛ぶ所は、4コマ（約0.08秒）かけて、前の絵から次の絵へ溶かすように切りかえる
"""
import numpy as np, cv2

import os
SIGMA = float(os.environ.get("MV_SIGMA", "2.5"))   # 2026-10-29: 1.6→2.5（加速度のぶれが約2割へる）
FADE = int(os.environ.get("MV_FADE", "6"))          # 飛ぶ所の切りかえのコマ数（48コマ/秒で約0.12秒）

def smooth_positions(seq, fps_in=24, fps_out=48, sigma=None, jump=3):
    sigma = SIGMA if sigma is None else sigma
    """seq: 24コマ/秒の整数のコマ番号 → 48コマ/秒の [(位置, 区切りの番号)]"""
    s = np.asarray(seq, float); n = len(s)
    cut = [0] + [i + 1 for i in range(n - 1) if abs(s[i + 1] - s[i]) >= jump] + [n]
    smooth = np.zeros(n); seg = np.zeros(n, int)
    for g, (a, b) in enumerate(zip(cut[:-1], cut[1:])):
        x = s[a:b]
        if len(x) >= 3:
            r = int(3 * sigma) + 1; k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); k /= k.sum()
            xp = np.pad(x, r, mode="edge"); y = np.convolve(xp, k, mode="valid")
        else:
            y = x
        smooth[a:b] = y; seg[a:b] = g
    m = int(round(n * fps_out / fps_in)); out = []
    for j in range(m):
        t = j * fps_in / fps_out; i = min(int(t), n - 1); f = t - i
        if i + 1 < n and seg[i + 1] == seg[i]: p = smooth[i] * (1 - f) + smooth[i + 1] * f
        else: p = smooth[i]
        out.append((float(p), int(seg[i])))
    return out


class Interp:
    """となりの2コマのあいだを、オプティカルフローで補間する（RGBA。色は α をかけた形で扱う）"""
    def __init__(self, load, cache=64):
        self.load = load; self.flows = {}; self.order = []; self.cache = cache
        self.dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)

    def _gray(self, im):
        a = im[..., 3:4].astype(np.float32) / 255
        g = cv2.cvtColor((im[..., :3].astype(np.float32) * a).astype(np.uint8), cv2.COLOR_BGR2GRAY)
        return g

    def flow(self, k0, k1):
        key = (k0, k1)
        if key not in self.flows:
            self.flows[key] = self.dis.calc(self._gray(self.load(k0)), self._gray(self.load(k1)), None)
            self.order.append(key)
            if len(self.order) > self.cache: self.flows.pop(self.order.pop(0), None)
        return self.flows[key]

    @staticmethod
    def _warp(im, fl, t):
        h, w = fl.shape[:2]
        gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
        mx = gx + fl[..., 0] * t; my = gy + fl[..., 1] * t
        return cv2.remap(im, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    def morph(self, A, B, t):
        """離れた2つの絵のあいだを、動きの流れで形を寄せながら切りかえる（ただ重ねると二重に見えるので）"""
        A = A.astype(np.float32); B = B.astype(np.float32)
        def pm(x): x = x.copy(); x[..., :3] *= x[..., 3:4] / 255; return x
        gA = self._gray(A.astype(np.uint8)); gB = self._gray(B.astype(np.uint8))
        fab = self.dis.calc(gB, gA, None); fba = self.dis.calc(gA, gB, None)
        # 流れが大きすぎる所（読みちがい）は弱める
        for fl in (fab, fba):
            m = np.linalg.norm(fl, axis=2, keepdims=True); fl *= np.minimum(1, 40 / np.maximum(m, 1e-3))
        e = t * t * (3 - 2 * t)                       # 始めと終わりをゆっくり
        Aw = self._warp(pm(A), fba, -e); Bw = self._warp(pm(B), fab, -(1 - e))
        C = Aw * (1 - e) + Bw * e; a = C[..., 3:4]
        C[..., :3] = np.where(a > 0.5, C[..., :3] * 255 / np.maximum(a, 1e-3), 0)
        return np.clip(C, 0, 255).astype(np.uint8)

    def at(self, p, kmax):
        """位置 p（小数）の絵（BGRA・uint8）"""
        k = int(np.floor(p)); f = p - k
        k = max(0, min(kmax, k))
        if f < 0.03 or k + 1 > kmax: return self.load(k)
        if f > 0.97: return self.load(k + 1)
        A = self.load(k).astype(np.float32); B = self.load(k + 1).astype(np.float32)
        # α をかけた色にしてから動かす（縁が黒や白にならない）
        def pm(x): x = x.copy(); x[..., :3] *= x[..., 3:4] / 255; return x
        A, B = pm(A), pm(B)
        fab = self.flow(k + 1, k)     # B の各点が A のどこから来たか（逆向きに引く）
        fba = self.flow(k, k + 1)
        Aw = self._warp(A, fba, -f)         # 時刻 f の点 x は、A では x − f·v（v＝A→B の流れ）にあった
        Bw = self._warp(B, fab, -(1 - f))   # B では x − (1−f)·u（u＝B→A の流れ）にあった
        C = Aw * (1 - f) + Bw * f
        a = C[..., 3:4]
        C[..., :3] = np.where(a > 0.5, C[..., :3] * 255 / np.maximum(a, 1e-3), 0)
        return np.clip(C, 0, 255).astype(np.uint8)


def crossfade(A, B, t):
    """飛ぶ所の切りかえ（α をかけた形で混ぜる）"""
    A = A.astype(np.float32); B = B.astype(np.float32)
    pa = A.copy(); pa[..., :3] *= A[..., 3:4] / 255
    pb = B.copy(); pb[..., :3] *= B[..., 3:4] / 255
    C = pa * (1 - t) + pb * t; a = C[..., 3:4]
    C[..., :3] = np.where(a > 0.5, C[..., :3] * 255 / np.maximum(a, 1e-3), 0)
    return np.clip(C, 0, 255).astype(np.uint8)


def frame_plan(seq, fps_in=24, fps_out=48, fade=None):
    fade = FADE if fade is None else fade
    """書き出しの各コマで、どの位置の絵を（必要なら2つを混ぜて）出すか: [(p1, p2 または None, 混ぜる割合)]"""
    pos = smooth_positions(seq, fps_in, fps_out)
    plan = [(p, None, 0.0) for p, g in pos]
    for j in range(1, len(pos)):
        if pos[j][1] != pos[j - 1][1]:                       # 飛ぶ所
            pa = pos[j - 1][0]; pb = pos[j][0]
            for q in range(fade):
                jj = j - fade // 2 + q
                if 0 <= jj < len(pos):
                    plan[jj] = (pa, pb, (q + 0.5) / fade)
    return plan
