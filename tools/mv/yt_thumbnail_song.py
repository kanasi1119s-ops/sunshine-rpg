"""HUMMING RELAY の1曲ぶんの YouTube サムネイル（1280×720）。アルバムのサムネ（yt_thumbnail_humming_relay.py）と同じ形: 舞台の絵・左の歌詞ボードに文字・右の台にテト。
  python3 yt_thumbnail_song.py <曲番号> <songs.tsv> <1行の紹介（日本語）> <出力.jpg>
テトは、目の穴を埋めた切り抜き（/tmp/yt2/tm。tools/mv/fix_cutout_eyes.py を通したもの）の 052 コマを使う。"""
import sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
NO, TSV, TAG, OUT = sys.argv[1:5]
rows = {r[0]: r for r in (l.rstrip("\n").split("\t") for l in open(TSV, encoding="utf-8")) if r and r[0]}
_, TJ, TE = rows[NO][:3]
FJ = "/home/claude/wt-mix/tools/mv/fonts/DotGothic16-Regular.ttf"; FE = "/home/claude/wt-mix/tools/mv/fonts/Orbitron.ttf"
W, H = 1920, 1080
bg = Image.open("/tmp/yt2/stage.png").convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
a = np.asarray(bg).astype(np.float32); gx0, gy0, gx1, gy1 = 118, 132, 918, 948
a[gy0:gy1, gx0:gx1] *= 0.4; bg = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
def txt(im, xy, t, f, col, glow=None, stroke=0):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text(xy, t, font=f, fill=glow, stroke_width=stroke + 4, stroke_fill=glow)
        lay = Image.alpha_composite(lay, g.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(lay).text(xy, t, font=f, fill=col, stroke_width=stroke, stroke_fill=(10, 5, 10, 255))
    return Image.alpha_composite(im, lay)
def fitf(path, t, size, maxw):
    while ImageFont.truetype(path, size).getbbox(t)[2] > maxw: size -= 2
    return ImageFont.truetype(path, size)
X = 150
rng = np.random.default_rng(int(NO))
gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(gl)
hs = (np.abs(np.sin(np.linspace(0.3, 7, 30) + int(NO))) * 0.6 + rng.random(30) * 0.3)
for b_ in range(30):
    x = int(140 + b_ * 25.2); h = int(hs[b_] * 330)
    for yy in range(930 - h, 930, 7): dg.rectangle((x, yy, x + 18, yy + 4), fill=(220, 50, 100, 95))
bg = Image.alpha_composite(bg, gl)
bg = txt(bg, (X, 165), f"HUMMING RELAY   {NO} / 25", fitf(FE, f"HUMMING RELAY   {NO} / 25", 36, 740), (255, 150, 180, 255), stroke=2)
# 曲名（日本語）: 長ければ「、」や助詞のあとで2行に分ける
def split(t):
    if ImageFont.truetype(FJ, 96).getbbox(t)[2] <= 740: return [t]
    for sep in ("、", "の中は", "は", "の"):
        if sep in t:
            i = t.index(sep) + len(sep); return [t[:i].rstrip("、"), t[i:]]
    return [t[:len(t) // 2], t[len(t) // 2:]]
ls = split(TJ); size = min(110, min(fitf(FJ, l, 110, 740).size for l in ls)); y = 250 if len(ls) == 2 else 320
for k, l in enumerate(ls):
    bg = txt(bg, (X - 2, y), l, ImageFont.truetype(FJ, size), (255, 255, 255, 255) if k == 0 else (255, 120, 160, 255), glow=(255, 40, 110, 230), stroke=3); y += size + 26
y += 14
bg = txt(bg, (X, y), TE, fitf(FE, TE, 44, 740), (240, 230, 240, 255), stroke=2); y += 86
bg = txt(bg, (X, y), TAG, fitf(FJ, TAG, 36, 740), (255, 200, 215, 255), stroke=2)
bg = txt(bg, (X, 778), "歌：重音テト  /  Vocal: Kasane Teto", ImageFont.truetype(FJ, 38), (255, 150, 180, 255), stroke=3)
bg = txt(bg, (X, 840), "歌詞つき（日本語・英語） / JP & EN Lyrics", fitf(FJ, "歌詞つき（日本語・英語） / JP & EN Lyrics", 34, 740), (240, 230, 240, 255), stroke=3)
t = cv2.imread("/tmp/yt2/tm/052.png", cv2.IMREAD_UNCHANGED); t = cv2.cvtColor(t, cv2.COLOR_BGRA2RGBA)
ti = Image.fromarray(t); s = 0.98; ti = ti.resize((int(ti.width * s), int(ti.height * s)), Image.LANCZOS)
al = np.asarray(ti)[..., 3]; ys = np.where(al.max(1) > 128)[0]; xs = np.where(al.max(0) > 128)[0]
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((1434 - 150, 845, 1434 + 150, 885), fill=(0, 0, 0, 130))
bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(10)))
bg.alpha_composite(ti, (1434 - (xs.min() + xs.max()) // 2, 868 - ys.max()))
bg.convert("RGB").resize((1280, 720), Image.LANCZOS).save(OUT, quality=93)
# テトの顔のあたりを大きく切り出して、目が欠けていないか見るための絵も出す
x0 = 1434 - (xs.min() + xs.max()) // 2; y0 = 868 - ys.max()
bg.convert("RGB").crop((x0 + int(ti.width * 0.2), y0 + ys.min(), x0 + int(ti.width * 0.8), y0 + ys.min() + int(ti.height * 0.3))).resize((1200, int(1200 * ti.height * 0.3 / (ti.width * 0.6))), Image.LANCZOS).save(OUT.replace(".jpg", ".face.png"))
print("ok", OUT)
