"""4方向のドット絵を描くための道具: 素材ごとの色の段（暗い→明るい）と、形（行ごとのはば）から陰影とふちを付ける。"""
import sys, math, random
sys.path.insert(0, '/home/claude/wt-mix/assets-src/pixel-singer')
import art_blonde_trace_v1 as A
W, H = A.W, A.H
FRONT = [list(r) for r in A.ROWS]
PAL = {s: c for s, _, c in A.PAL}
RAMP = {
 "hair": list("DIMUXaflouvz"), "skin": list("Dchknpswy0"), "white": list("Ebjmrtx23"), "red": list("DIMPYg"),
 "denim": list("BGKNRWZe"), "brown": list("CFHLOSVi"), "sock": list("ETrt2"), "dark": list("A"),
}
OUT = {"hair": "D", "skin": "D", "white": "E", "red": "D", "denim": "B", "brown": "C", "sock": "E"}
def blank(): return [["."] * W for _ in range(H)]
def spans(keys):
    """keys: [(y, xl, xr), ...] → {y: (xl, xr)}（あいだは直線でつなぐ）"""
    out = {}
    for (y0, a0, b0), (y1, a1, b1) in zip(keys, keys[1:]):
        for y in range(y0, y1 + 1):
            t = 0 if y1 == y0 else (y - y0) / (y1 - y0)
            out[y] = (round(a0 + (a1 - a0) * t), round(b0 + (b1 - b0) * t))
    return out
def mask_from_spans(sp):
    return {(x, y) for y, (a, b) in sp.items() for x in range(a, b + 1)}
def shade(mask, mat, peak=0.3, lo=1, hi=None, vgrad=0.25, rim=True, noise=0.0, seed=1, bias=0.0):
    """円柱のような陰影: 行ごとに左から peak の所がいちばん明るく、右はしが暗い。上から下へ少し暗く。"""
    R = RAMP[mat]; hi = len(R) - 1 if hi is None else hi; rnd = random.Random(seed)
    rows = {}
    for x, y in mask: rows.setdefault(y, []).append(x)
    ys = sorted(rows); y0, y1 = ys[0], ys[-1]; out = {}
    for y in ys:
        xs = sorted(rows[y]); a, b = xs[0], xs[-1]
        for x in xs:
            t = 0.5 if b == a else (x - a) / (b - a)
            l = 1 - abs(t - peak) * (1.5 if t > peak else 1.1)
            l -= vgrad * ((y - y0) / max(1, y1 - y0)) - bias
            if noise: l += rnd.uniform(-noise, noise)
            l = max(0, min(1, l))
            i = lo + round(l * (hi - lo))
            if rim and ((x + 1, y) not in mask): i = max(lo, min(i, lo + 1))
            out[(x, y)] = R[i]
    return out
def put(g, cells):
    for (x, y), ch in cells.items():
        if 0 <= x < W and 0 <= y < H: g[y][x] = ch
def outline(g, color_of=None):
    """外がわのふち: 絵のはしの内がわ1マスを、となりの素材のふちの色にする（正面の絵と同じく、ふちは絵の内がわ）"""
    add = []
    for y in range(H):
        for x in range(W):
            if g[y][x] == ".": continue
            if any(not (0 <= x + a < W and 0 <= y + b < H) or g[y + b][x + a] == "." for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                add.append((x, y))
    for x, y in add: g[y][x] = color_of(g[y][x]) if color_of else "A"
def mat_of(ch):
    for m, R in RAMP.items():
        if ch in R: return m
    return None
def darker(ch, n=1):
    m = mat_of(ch)
    if not m: return ch
    R = RAMP[m]; return R[max(0, R.index(ch) - n)]
def lighter(ch, n=1):
    m = mat_of(ch)
    if not m: return ch
    R = RAMP[m]; return R[min(len(R) - 1, R.index(ch) + n)]
def save_png(grids, path, z=6, gap=4):
    from PIL import Image
    rgb = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in PAL.items()}
    im = Image.new('RGB', ((W + gap) * z * len(grids), H * z), (104, 100, 92))
    for k, g in enumerate(grids):
        for y in range(H):
            for x in range(W):
                if g[y][x] != ".": im.paste(rgb[g[y][x]], ((W + gap) * z * k + x * z, y * z, (W + gap) * z * k + x * z + z, y * z + z))
    im.save(path)
