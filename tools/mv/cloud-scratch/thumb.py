import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FJ = "/home/claude/wt-mix/tools/mv/fonts/DotGothic16-Regular.ttf"; FE = "/home/claude/wt-mix/tools/mv/fonts/Orbitron.ttf"
W, H = 1920, 1080
bg = Image.open("/tmp/yt/stage.png").convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
a = np.asarray(bg).astype(np.float32); gx0, gy0, gx1, gy1 = 118, 132, 918, 948
a[gy0:gy1, gx0:gx1] *= 0.4; bg = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
def txt(im, xy, t, f, col, glow=None, stroke=0):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text(xy, t, font=f, fill=glow, stroke_width=stroke + 4, stroke_fill=glow)
        lay = Image.alpha_composite(lay, g.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(lay).text(xy, t, font=f, fill=col, stroke_width=stroke, stroke_fill=(10, 5, 10, 255))
    return Image.alpha_composite(im, lay)
X = 150
rng = np.random.default_rng(3)
gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(gl)
hs = (np.abs(np.sin(np.linspace(0.3, 7, 30))) * 0.6 + rng.random(30) * 0.3)
for b_ in range(30):
    x = int(140 + b_ * 25.2); h = int(hs[b_] * 330)
    for yy in range(930 - h, 930, 7): dg.rectangle((x, yy, x + 18, yy + 4), fill=(220, 50, 100, 95))
bg = Image.alpha_composite(bg, gl)
def fitf(path, t, size, maxw):
    while ImageFont.truetype(path, size).getbbox(t)[2] > maxw: size -= 2
    return ImageFont.truetype(path, size)
bg = txt(bg, (X, 165), "全25曲  /  25 Songs", ImageFont.truetype(FJ, 36), (255, 150, 180, 255), stroke=2)
bg = txt(bg, (X - 4, 250), "SCARLET", fitf(FE, "FREQUENCY", 120, 750), (255, 255, 255, 255), glow=(255, 40, 110, 230), stroke=3)
bg = txt(bg, (X - 4, 390), "FREQUENCY", fitf(FE, "FREQUENCY", 120, 750), (255, 80, 130, 255), glow=(255, 40, 110, 230), stroke=3)
bg = txt(bg, (X, 545), "スカーレット・フリークエンシー", fitf(FJ, "スカーレット・フリークエンシー", 50, 740), (240, 230, 240, 255), stroke=2)
bg = txt(bg, (X, 660), "歌：重音テト  /  Vocal: Kasane Teto", ImageFont.truetype(FJ, 38), (255, 150, 180, 255), stroke=3)
bg = txt(bg, (X, 722), "歌詞つき（日本語・英語）・約1時間49分", fitf(FJ, "歌詞つき（日本語・英語）・約1時間49分", 38, 740), (240, 230, 240, 255), stroke=3)
bg = txt(bg, (X, 778), "With Lyrics (Japanese & English) - 1h 49min", fitf(FJ, "With Lyrics (Japanese & English) - 1h 49min", 30, 740), (240, 230, 240, 255), stroke=3)
t = cv2.imread("/tmp/yt/tm/052.png", cv2.IMREAD_UNCHANGED); t = cv2.cvtColor(t, cv2.COLOR_BGRA2RGBA)
ti = Image.fromarray(t); s = 0.98; ti = ti.resize((int(ti.width * s), int(ti.height * s)), Image.LANCZOS)
al = np.asarray(ti)[..., 3]; ys = np.where(al.max(1) > 128)[0]; xs = np.where(al.max(0) > 128)[0]
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((1434 - 150, 845, 1434 + 150, 885), fill=(0, 0, 0, 130))
bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(10)))
bg.alpha_composite(ti, (1434 - (xs.min() + xs.max()) // 2, 868 - ys.max()))
out = bg.convert("RGB").resize((1280, 720), Image.LANCZOS); out.save("/tmp/yt/thumb/SCARLET FREQUENCY サムネイル.jpg", quality=93)
print(ys.min() + 868 - ys.max())
