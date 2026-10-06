"""下絵から、布や羽を削らずに切り抜く（2026-10-06、人間の指示「ドットのトレースを細かく丁寧に」「マントとかも削ってる」）。

AIの切り抜き（rembg）は、白いマント・白い羽・白いドレス（白い背景のとき）や、暗い背景にとけた羽（暗い背景のとき）を、
背景といっしょに消すことがある（無神・女神のマントが欠けた原因）。
ここでは、rembg の切り抜きに、「四すみの背景の色と外側からつながっていない所」をすべて足す（削らないことを優先）。
ただし次は足さない: 足もとの床の影（いちばん下の帯の色の薄い所）・絵のふちに届く所（額縁など）・外側の背景のにじみ（2マス）。
rembg とくらべて大きすぎる（背景まで残った）ときは使わない。
使い方: python3 cutout.py 下絵.png 出力.png   （成功なら出力に透明つきPNGを書いて ok と出す。だめなら ng と出して 1 で終わる）
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage


def flood_cut(src, r):
    """r: rembg の切り抜き（True=体）。None なら rembg なしで試す（見た目の確認用）"""
    a = np.asarray(Image.open(src).convert("RGB")).astype(float)
    bgv = np.median(np.concatenate([a[:8, :8].reshape(-1, 3), a[:8, -8:].reshape(-1, 3)]), 0)
    sat = a.max(2) - a.min(2)
    if bgv.min() >= 200:
        bgc = np.abs(a - bgv).max(2) <= 5                      # 白い背景: 背景の色とほぼ同じ所だけ
    else:
        bgc = (np.abs(a - bgv).max(2) <= 30) & (sat < 30)      # 暗い背景: 明るさにむらがあるので、ゆるめに
    lab, _ = ndimage.label(bgc)
    if r is not None:      # 背景の種: rembg の体から25マス以上はなれた背景色の所（額縁の内側の背景も拾える）
        seeds = set(np.unique(lab[bgc & ~ndimage.binary_dilation(r, iterations=25)]))
    else:
        seeds = set(lab[0]) | set(lab[-1]) | set(lab[:, 0]) | set(lab[:, -1])
    seeds.discard(0)
    m = ~np.isin(lab, list(seeds))
    if bgv.min() < 200:    # 暗い背景: 背景より十分に明るい所か、色のこい所だけ足す（背景の光のもやは足さない）
        lum = a.mean(2)
        m &= (lum >= bgv.mean() + 45) | (sat >= 60)
    rr = r if r is not None else np.zeros_like(m)
    ry = np.where(rr.any(1))[0]
    if not len(ry):
        ry = np.where(m.any(1))[0]
    if not len(ry):
        return a, None
    top, bot = ry.min(), ry.max()
    add = m & ~rr
    # 足もとの床の影
    g = a.mean(2); mu = ndimage.uniform_filter(g, 7); sd = np.sqrt(np.maximum(ndimage.uniform_filter(g * g, 7) - mu * mu, 0))
    floor = np.zeros_like(add)
    band = int(bot - (bot - top) * 0.12)
    floor[band:] = True
    floor &= (sd < 4) & (sat < 30)
    band2 = int(bot - (bot - top) * 0.07)                      # いちばん下の帯は、色の薄い所をすべて床とみなす
    floor[band2:] |= (sat[band2:] < 30) & (a[band2:].min(2) >= 150)
    add &= ~floor
    add = ndimage.binary_opening(add, iterations=1)
    # 体のすき間から見える背景（背景と同じ色で、まわりがほとんど rembg の体）は足さない
    if r is not None:
        gap = add & (np.abs(a - bgv).max(2) <= 6)
        gl, gn = ndimage.label(gap)
        for k in range(1, gn + 1):
            comp = gl == k
            ring = ndimage.binary_dilation(comp, iterations=1) & ~comp
            if ring.sum() and (rr[ring].mean() >= 0.6 or (rr | ~add)[ring].mean() >= 0.85 and rr[ring].mean() >= 0.3):
                add &= ~comp
    # 絵のふちに届く所（額縁など）は足さない
    al, an = ndimage.label(add)
    edge = set(al[0]) | set(al[-1]) | set(al[:, 0]) | set(al[:, -1]); edge.discard(0)
    add &= ~np.isin(al, list(edge))
    # 外側の背景のにじみ（2マス）を落とす
    add &= ndimage.binary_erosion(rr | add, iterations=2) | ndimage.binary_dilation(rr, iterations=2)
    out = rr | add
    lab, n = ndimage.label(out)
    if n == 0:
        return a, None
    sz = ndimage.sum(out, lab, range(1, n + 1))
    out = np.isin(lab, 1 + np.where(sz >= max(150, sz.max() * 0.01))[0])
    return a, out


def main():
    src, out = sys.argv[1], sys.argv[2]
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from pixelize import remove_bg_ai
    r = np.asarray(remove_bg_ai(Image.open(src)))[..., 3] > 0
    a, m = flood_cut(src, r)
    if m is None:
        print("ng: 何も残らない"); return 1
    ratio = m.sum() / max(1, r.sum())
    if ratio > 2.2 or (m & r).sum() < r.sum() * 0.9:
        print(f"ng: rembg と大きくちがう（{ratio:.2f}倍）"); return 1
    Image.fromarray(np.dstack([a, m * 255]).astype(np.uint8), "RGBA").save(out)
    print(f"ok: rembg の {ratio:.2f} 倍")
    return 0


if __name__ == "__main__":
    sys.exit(main())
