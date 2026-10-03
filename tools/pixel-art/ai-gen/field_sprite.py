"""フィールド（マップ）用キャラ 16×32・4方向×3コマを作る（AIのデザイン画 → 色 → 型）。

考え方: 16×32 は小さすぎて、AIの絵をそのまま縮めると形がつぶれる。そこで2段にする。
  1. AIの「正面の全身デザイン画」から、髪・肌・上着・ズボン・靴・目印の色だけを取り出す（色の設計図）
  2. 手描きの型（field_templates.py。2頭身・暗い外周・3段の陰影・4方向×3コマの歩き）に色を当てはめる
体の形と歩きは型が受け持つので、どのキャラも同じ質で歩く。顔・髪型・服の形は型の組み合わせで選ぶ。

使い方:
  python3 tools/pixel-art/ai-gen/field_sprite.py デザイン.png 出力フォルダ 名前 --style spiky --outfit tunic [--deco sword,shield,helmet] [--beard] [--rembg]
  python3 tools/pixel-art/ai-gen/field_sprite.py - 出力フォルダ 名前 --style long --outfit dress --set hair=#c8642a --set top=#2a70c8 ...
     （デザイン画を使わず、色を全部手で決めるときは、デザイン画に - を渡し、--set で6色すべてを指定する）
  --set 部位=#rrggbb で、取り出した色を上書きできる（hair/skin/top/bottom/boot/acc）。--eye #rrggbb で目の色。
出力（出力フォルダ/名前.*）:
  .colors.json  使った色（手で直して --colors で読み直せる）
  .walker.json  ゲームの形式（src/game/sprite/walker-data.generated.ts の WalkerData: palette と frames）
  .sheet.txt / .sheet.json  12コマを1枚に並べた文字グリッド（横: コマ0〜2、縦: 下・上・左・右。48×128）とパレット。ドット絵エディタで描く用
  .sheet.png  12コマの一覧（8倍）、.compare.png  デザイン画と並べた比べ
"""
import argparse, colorsys, json, os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import field_templates as FT  # noqa: E402

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
DIRS = ("down", "up", "left", "right")
OUTLINE = "#1a1018"


def hexc(c):
    return "#%02x%02x%02x" % tuple(int(max(0, min(255, round(v)))) for v in c)


def ramp(base):
    """1色から（影・地・光）の3段を作る。影は少し暗く・少し青み、光は少し明るく・少し黄み。"""
    r, g, b = [v / 255 for v in base]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    def mk(h2, l2, s2):
        return hexc([v * 255 for v in colorsys.hls_to_rgb(h2 % 1, max(0, min(1, l2)), max(0, min(1, s2)))])
    hue_dark = h + (0.02 if 0.08 < h < 0.6 else -0.02)
    light = mk(h - 0.01, l + (1 - l) * 0.32, s * 0.95) if l >= 0.15 else mk(h, l + 0.16, s * 0.5)  # 黒に近い色の光は、色みを抑える
    if 0.02 < h < 0.12 and s > 0.35 and l > 0.6:   # 肌: 影がオレンジに寄りすぎないよう、彩度を抑える
        return (mk(h, l * 0.8, s * 0.7), mk(h, l, s), light)
    return (mk(hue_dark, l * 0.62, s * 1.05), mk(h, l, s), light)


def dominant(pix, k=3):
    """画素の中で一番多い色（Lab で k-means）。"""
    from sklearn.cluster import KMeans
    from skimage import color as skc
    if len(pix) < 4:
        return None
    lab = skc.rgb2lab(pix.reshape(-1, 1, 3) / 255.0).reshape(-1, 3)
    k = min(k, len(pix))
    km = KMeans(k, n_init=3, random_state=0).fit(lab)
    big = np.bincount(km.labels_).argmax()
    c = skc.lab2rgb(km.cluster_centers_[big].reshape(1, 1, 3)).reshape(3) * 255
    return c, km, lab


def extract(design, use_rembg):
    im = Image.open(design)
    if use_rembg:
        from pixelize import remove_bg_ai
        im = remove_bg_ai(im)
    else:
        from pixelize import remove_bg
        im = remove_bg(im)
    a = np.asarray(im)
    m = a[:, :, 3] >= 128
    ys, xs = np.nonzero(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    H, W = y1 - y0, x1 - x0
    rgb = a[:, :, :3].astype(float)

    def band(t0, t1, w=1.0):
        cx = (x0 + x1) / 2
        sel = np.zeros_like(m)
        sel[int(y0 + t0 * H):int(y0 + t1 * H), int(cx - w * W / 2):int(cx + w * W / 2)] = True
        return rgb[sel & m]

    out = {}
    for key, (t0, t1, w) in dict(hair=(0.0, 0.07, 1.0), skin=(0.09, 0.15, 0.3), top=(0.25, 0.45, 0.5),
                                 bottom=(0.62, 0.82, 0.5), boot=(0.93, 1.0, 1.0)).items():
        d = dominant(band(t0, t1, w))
        out[key] = d[0] if d else np.array([128, 128, 128])
    # 目印の色: 胴のあたりで、上着の色と違う、いちばん鮮やかな色
    pix = band(0.18, 0.6, 0.8)
    acc = None
    d = dominant(pix, 5)
    if d:
        from skimage import color as skc
        _, km, lab = d
        top_lab = skc.rgb2lab(out["top"].reshape(1, 1, 3) / 255.0).reshape(3)
        best = -1
        for c in km.cluster_centers_:
            if np.linalg.norm(c - top_lab) < 20:
                continue
            chroma = np.hypot(c[1], c[2])
            if chroma > best:
                best = chroma
                acc = skc.lab2rgb(c.reshape(1, 1, 3)).reshape(3) * 255
    if acc is None:
        r, g, b = out["top"] / 255
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        acc = np.array(colorsys.hls_to_rgb((h + 0.5) % 1, 0.5, 0.7)) * 255
    out["acc"] = acc
    return out, im.crop((x0, y0, x1, y1))



def palette_for(cols, eye=None):
    """型の文字 → 色。部位ごとに（影・地・光）。"""
    P = {"O": OUTLINE, "W": "#ffffff", "G": "#e8c048", "g": "#9a6a1c",
         "M": "#a8b0c0", "m": "#5a6070", "N": "#e4ecf4", "D": "#9a6a34", "d": "#5e3c1c", "Q": "#70d8ff"}
    for key, (base, dark, light) in dict(hair=("H", "h", "L"), skin=("S", "s", None), top=("T", "t", "U"),
                                          acc=("A", "a", None), bottom=("B", "b", None), boot=("K", "k", "Y")).items():
        d, m, l = ramp(cols[key])
        P[base], P[dark] = m, d
        if light: P[light] = l
    # 細部の色: 瞳（目の色と、その明るい色）、ほお、口、ひざの光
    e = eye or "#3a3050"
    er, eg, eb = [int(e[i:i + 2], 16) for i in (1, 3, 5)]
    P["E"] = e   # 目は縦2ドットの点（目の色）
    P["I"] = e
    P["J"] = hexc([v + (255 - v) * 0.45 for v in (er, eg, eb)])
    sr, sg, sb = cols["skin"]
    P["P"] = hexc([sr * 0.95 + 12, sg * 0.72, sb * 0.72])
    P["X"] = hexc([sr * 0.62, sg * 0.4, sb * 0.4])
    P["V"] = ramp(cols["bottom"])[2]
    if "orb" in cols:
        P["Q"] = hexc(cols["orb"])
    return P


def build(style, outfit, P, beard=False, decos=(), hair_sway=True):
    frames_raw = FT.all_frames(style, outfit, beard, decos, hair_sway)
    frames, pal, idx = {}, [], {}
    for key, rows in frames_raw.items():
        out = []
        for row in rows:
            s = ""
            for ch in row:
                if ch == ".":
                    s += "."; continue
                col = P.get(ch, P["O"]) if ch != "E" else P.get("E", P["O"])
                if col not in idx:
                    idx[col] = len(pal); pal.append(col)
                s += LETTERS[idx[col]]
            out.append(s)
        frames[key] = out
    return {"palette": pal, "frames": frames}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("design"); ap.add_argument("outdir"); ap.add_argument("name")
    ap.add_argument("--style", default="spiky", choices=list(FT.HAIR))
    ap.add_argument("--outfit", default="tunic", choices=["tunic", "coat", "dress", "robe"])
    ap.add_argument("--set", action="append", default=[], help="部位=#rrggbb（hair/skin/top/bottom/boot/acc、杖の玉・腕輪の光は orb）")
    ap.add_argument("--deco", default="", help="飾り（カンマ区切り）: band はちまき・cape マント・backsword 背中の剣・sword 手に剣・shield 盾・helmet 兜・staff 杖・scarf マフラー・goggles ゴーグル・twintails ふたつ結び")
    ap.add_argument("--beard", action="store_true", help="ひげをつける（髪の色）")
    ap.add_argument("--still-hair", action="store_true", help="歩くときに髪を揺らさない（男性の人物。人間の指示 2026-10-04）")
    ap.add_argument("--eye", help="目の色（省略すると外周と同じ暗い色）")
    ap.add_argument("--colors", help="手で直した .colors.json から作り直す")
    ap.add_argument("--rembg", action="store_true", help="デザイン画の背景をAIで切り抜く")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    base = os.path.join(a.outdir, a.name)
    crop = None
    if a.colors:
        cols = {k: np.array([int(v[i:i + 2], 16) for i in (1, 3, 5)]) for k, v in json.load(open(a.colors)).items() if k != "eye"}
    elif a.design == "-":
        cols = {}
    else:
        cols, crop = extract(a.design, a.rembg)
    for kv in a.set:
        k, v = kv.split("=")
        cols[k] = np.array([int(v[i:i + 2], 16) for i in (1, 3, 5)])
    missing = [k for k in ("hair", "skin", "top", "bottom", "boot", "acc") if k not in cols]
    if missing:
        sys.exit("色が足りません: " + ", ".join(missing) + "（--set で指定してください）")
    json.dump({**{k: hexc(v) for k, v in cols.items()}, **({"eye": a.eye} if a.eye else {})}, open(base + ".colors.json", "w"), ensure_ascii=False, indent=1)
    P = palette_for(cols, a.eye)
    data = build(a.style, a.outfit, P, a.beard, tuple(filter(None, a.deco.split(','))), not a.still_hair)
    json.dump(data, open(base + ".walker.json", "w"), ensure_ascii=False)
    sheet_rows = []
    for dr in DIRS:
        for y in range(32):
            sheet_rows.append("".join(data["frames"][f"{dr}{f}"][y] for f in range(3)))
    open(base + ".sheet.txt", "w").write("\n".join(sheet_rows) + "\n")
    json.dump({LETTERS[i]: c for i, c in enumerate(data["palette"])}, open(base + ".sheet.json", "w"))
    Z = 8
    img = Image.new("RGBA", (48 * Z, 128 * Z), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(sheet_rows):
        for x, ch in enumerate(row):
            if ch == ".": continue
            c = data["palette"][LETTERS.index(ch)]
            col = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
            for dy in range(Z):
                for dx in range(Z): px[x * Z + dx, y * Z + dy] = col
    bg = Image.new("RGB", img.size, (88, 136, 88)); bg.paste(img, (0, 0), img); bg.save(base + ".sheet.png")
    if crop is not None:
        c2 = crop.copy(); c2.thumbnail((384, 1024))
        cmp = Image.new("RGB", (c2.width + bg.width + 20, max(c2.height, bg.height)), (88, 136, 88))
        cmp.paste(c2, (0, 0), c2); cmp.paste(bg, (c2.width + 20, 0)); cmp.save(base + ".compare.png")
    print(a.name, len(data["palette"]), "色", base + ".sheet.png")


if __name__ == "__main__":
    main()
