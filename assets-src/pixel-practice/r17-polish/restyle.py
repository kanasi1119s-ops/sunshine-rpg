"""今ある町の飾りに、新しい木（tree2d.py）の「ドットの感じ」を当てはめる試し（2026-10-06、人間の指示
「この木の感じのドットの感じいいですね。このような雰囲気を既存で作ったオブジェクトに試しに当てはめてみてください」）。

新しい木の感じ（docs/design/tree-notes.md）を、次の5つの手順にして、立体の模型から描いた今の絵に重ねる。
  1. 色相のずれ: 明るい色ほど黄色寄り（あたたかい光）、暗い色ほど青寄り（空の光がまわる影）に。灰色にも、少しだけ色味をつける。
     まんなかの明るさの色はあざやかに、いちばん明るい・暗い色は少しおさえる。明暗の差（強弱）も少しだけ強く。
  2. りんかくは右下だけ: 左上（光の側）のふちの黒い線は消して、内がわの色にする。右下のふちは、真っ黒でなく、こい青みの色に。
  3. 光のふち: 左上のふちのすぐ内がわを、1段明るく（ところどころ）。
  4. 面をすっきり: まわりと色がちがう1ドットだけの点（ノイズ）は、まわりの色にそろえる。
  5. 接地の影（うすく透ける色）は、そのまま。
書き出し: ../r29-restyle-trial/<名前>.txt と pal-<名前>.json（試し。ゲームには読み込まれない）。
2026-10-06 人間の指示「これ全部共有ね」で採用。`--apply` をつけると、もとの絵（r17-polish・r20-props）を、この感じの絵で上書きする。
使い方: python3 restyle.py            … 試しを作る
        python3 restyle.py --apply    … ゲームの絵にする（模型から描きなおした絵に、1回だけかける。2回かけると強くなりすぎる）"""
import colorsys
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PP = os.path.join(HERE, "..")
OUT = os.path.join(PP, "r29-restyle-trial")
TARGETS = [
    ("r17-polish", n, n) for n in ("rock2", "bush2", "tree-snow", "tree-pine", "tree-dead", "rock-snow", "bush-snow", "palm", "cactus",
                                    "barrel", "lamp", "well", "signpost", "crates", "flowerbed")
] + [
    ("r20-props", n, n) for n in ("bench", "stall", "cart", "noticeboard", "brazier", "shrine", "statue-traveler", "statue-soldier",
                                   "statue-winged", "fountain", "haystack", "grave-cross")
]
WARM, COOL = 0.13, 0.62          # 光の色相（黄色寄り）、影の色相（青寄り）


def hx(c):
    return tuple(int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))


def to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(v * 255))):02x}" for v in rgb)


def luma(rgb):
    return 0.3 * rgb[0] + 0.59 * rgb[1] + 0.11 * rgb[2]


def toward(h, target, t):
    d = ((target - h + 0.5) % 1.0) - 0.5
    return (h + d * t) % 1.0


def shift(c):
    """手順1: 色相のずれ・あざやかさ・強弱。"""
    r, g, b = hx(c)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    y = luma((r, g, b))
    k = (y - 0.45) * 2                                      # -1（暗）〜 1（明）くらい
    if s < 0.12:                                            # 灰色: ほんの少し色味（光はあたたかく、影はつめたく）
        if s < 0.04 or abs(k) > 0.3:
            h = WARM if k > 0 else COOL                         # ほぼ無彩色のときだけ、色相を決める（青灰色の鉄などは、そのまま）
        s = s + 0.03 * min(1, abs(k))
    else:
        h = toward(h, WARM if k > 0 else COOL, min(0.22, abs(k) * 0.16))
        s = min(s, s * (1.08 - 0.25 * abs(k) ** 2)) if s > 0.55 else s * (1.08 - 0.25 * abs(k) ** 2)   # もとからあざやかな色は、それ以上あざやかにしない
    l = 0.5 + (l - 0.5) * 1.08                              # 強弱を少し強く
    return to_hex(colorsys.hls_to_rgb(h, max(0.03, min(0.97, l)), max(0, min(1, s))))


def darker(c, f=0.55):
    r, g, b = hx(c)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = toward(h, COOL, 0.3)
    return to_hex(colorsys.hls_to_rgb(h, l * f, min(1, s * 0.9 + 0.08)))


def restyle(rows, pal, grad=True):
    H, W = len(rows), len(rows[0])
    col = [[pal[ch] if ch != "." else "" for ch in r] for r in rows]
    solid = lambda x, y: 0 <= x < W and 0 <= y < H and len(col[y][x]) == 7
    # 1) 色相のずれ
    cache = {}
    for y in range(H):
        for x in range(W):
            c = col[y][x]
            if len(c) == 7:
                cache.setdefault(c, shift(c))
                col[y][x] = cache[c]
    # 1.5) 物全体を1つのかたまりとして、左上を少し明るく・右下を少し暗く（木の「樹冠全体を1つの球として光を決める」と同じ考え）
    pts = [(x, y) for y in range(H) for x in range(W) if solid(x, y)]
    if pts and grad:
        x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        cx, cy, hw, hh = (x0 + x1) / 2, (y0 + y1) / 2, max(1, (x1 - x0) / 2), max(1, (y1 - y0) / 2)
        for x, y in pts:
            g = -((x - cx) / hw * 0.6 + (y - cy) / hh * 0.4)          # -1（右下）〜 1（左上）
            g += 0.12 if (x + y) % 2 else -0.12                         # 段の境目は、市松でまぜる（段の線を作らない）
            g = 1 if g > 0.5 else (-1 if g < -0.5 else 0)              # 3段にまとめる（色をふやしすぎない）
            r, gg, b = hx(col[y][x])
            h, l, s = colorsys.rgb_to_hls(r, gg, b)
            col[y][x] = to_hex(colorsys.hls_to_rgb(h, max(0.02, min(0.97, l + 0.045 * g)), s))
    out = [r[:] for r in col]
    # 4) 1ドットだけの点をそろえる（りんかくをさわる前に）
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not solid(x, y):
                continue
            nb = [col[y + dy][x + dx] for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))]
            if all(len(n) == 7 for n in nb) and col[y][x] not in nb:
                best = max(set(nb), key=nb.count)
                if nb.count(best) >= 3 and abs(luma(hx(best)) - luma(hx(col[y][x]))) < 0.07:   # 目地・鋲などの、わざと置いた細部は残す
                    out[y][x] = best
    col = out
    out = [r[:] for r in col]
    # 2) りんかく: 左上は消す、右下はこい青みの色に。3) 左上のふちの光
    for y in range(H):
        for x in range(W):
            if not solid(x, y):
                continue
            c = col[y][x]
            open_l, open_u = not solid(x - 1, y), not solid(x, y - 1)
            open_r, open_d = not solid(x + 1, y), not solid(x, y + 1)
            if not (open_l or open_u or open_r or open_d):
                continue
            # りんかく＝まわり（内がわ）よりはっきり暗い、ふちの点。鉄の街灯のように、物そのものが暗い色のときは、りんかくとみなさない
            inner = [col[y + dy][x + dx] for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)) if solid(x + dx, y + dy)]
            dark = luma(hx(c)) < 0.2 and bool(inner) and max(luma(hx(n)) for n in inner) - luma(hx(c)) > 0.14
            if dark and (open_l or open_u) and not (open_r or open_d):
                # 内がわ（右下）の色で置きかえる＝左上のりんかくをなくす
                ix, iy = x + (1 if open_l else 0), y + (1 if open_u else 0)
                if solid(ix, iy) and luma(hx(col[iy][ix])) >= 0.2:
                    out[y][x] = col[iy][ix]
                    continue
            if dark and (open_r or open_d):
                ix, iy = x - (1 if open_r else 0), y - (1 if open_d else 0)
                if solid(ix, iy) and luma(hx(col[iy][ix])) >= 0.2:
                    out[y][x] = darker(col[iy][ix], 0.45)
                continue
            if not dark and (open_l or open_u):
                r, g, b = hx(c)
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                out[y][x] = to_hex(colorsys.hls_to_rgb(toward(h, WARM, 0.1) if s > 0.15 else h, min(0.95, l + 0.07), s))
    # 左上のりんかくをなくしたあとの、すぐ内がわにも光のふち
    return out


def merge_colors(img, limit=62):
    """色が limit をこえたら、いちばん近い2色を1つにまとめていく（エディタの記号は英字と数字の62個まで）。"""
    def rgb(c):
        return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
    while True:
        cnt = {}
        for r in img:
            for c in r:
                if c:
                    cnt[c] = cnt.get(c, 0) + 1
        if len(cnt) <= limit:
            return img
        solid = [c for c in cnt if len(c) == 7]
        best = None
        for i, a in enumerate(solid):
            for b in solid[i + 1:]:
                d = sum((p - q) ** 2 for p, q in zip(rgb(a), rgb(b)))
                if best is None or d < best[0]:
                    best = (d, a, b)
        _, a, b = best
        keep, drop = (a, b) if cnt[a] >= cnt[b] else (b, a)
        img = [[keep if c == drop else c for c in r] for r in img]


def save(img, name):
    img = merge_colors(img)
    cols = sorted({c for r in img for c in r if c})
    syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    if len(cols) > len(syms):
        raise SystemExit(f"{name}: 色が多すぎる {len(cols)}")
    cmap = {c: syms[i] for i, c in enumerate(cols)}
    open(os.path.join(OUT, name + ".txt"), "w").write("\n".join("".join(cmap[c] if c else "." for c in r) for r in img) + "\n")
    json.dump({cmap[c]: c for c in cols}, open(os.path.join(OUT, "pal-" + name + ".json"), "w"))
    return len(cols)


if __name__ == "__main__":
    import sys
    apply = "--apply" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    only = [a for a in sys.argv[1:] if not a.startswith("--")]                # 名前をならべると、その絵だけ
    targets = TARGETS + [("r20-props", n, n) for n in ("fountain-1", "fountain-2", "fountain-3")]
    targets += [("r20-props", n, n) for n in only if n not in {t[1] for t in targets}]   # 名前で指定した、ほかの r20-props の絵（階段など）
    for d, name, pname in targets:
        if only and name not in only:
            continue
        if not only and name.startswith("fountain-") and not apply:
            continue
        rows = [l for l in open(os.path.join(PP, d, name + ".txt")).read().split("\n") if l]
        pal = json.load(open(os.path.join(PP, d, "pal-" + pname + ".json")))
        img = restyle(rows, pal)
        if len({c for r in img for c in r if c}) > 90:
            img = restyle(rows, pal, grad=False)                  # 色が多すぎる絵は、全体の明暗をつけない
        print(name, save(img, name), "colors")
        if apply:
            import shutil
            shutil.copy(os.path.join(OUT, name + ".txt"), os.path.join(PP, d, name + ".txt"))
            shutil.copy(os.path.join(OUT, "pal-" + name + ".json"), os.path.join(PP, d, "pal-" + pname + ".json"))
