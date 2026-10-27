# BARジャズ50曲の動画用サムネ（SCARLETと同じ作り: 左に文字・グロー、題名は英語＋日本語、曲数・内容の行）
# 使い方: python3 tools/mv/yt_thumbnail_barjazz.py <背景画像> <出力jpg> [曲数] [時間の文字]
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FJ = "/home/claude/wt-mix/tools/mv/fonts/DotGothic16-Regular.ttf"; FE = "/home/claude/wt-mix/tools/mv/fonts/Orbitron.ttf"
src, dst = sys.argv[1], sys.argv[2]; n = sys.argv[3] if len(sys.argv) > 3 else "50"; dur = sys.argv[4] if len(sys.argv) > 4 else "約4時間"
W, H = 1920, 1080
bg = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
a = np.asarray(bg).astype(np.float32)
x = np.linspace(0, 1, W)[None, :, None]
a *= (1 - 0.72 * np.clip(1 - x / 0.40, 0, 1) ** 0.8)       # 左だけ暗くして文字を読みやすく（ボトルにはかからない）
bg = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
def txt(im, xy, t, f, col, glow=None, stroke=0):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text(xy, t, font=f, fill=glow, stroke_width=stroke + 4, stroke_fill=glow)
        lay = Image.alpha_composite(lay, g.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(lay).text(xy, t, font=f, fill=col, stroke_width=stroke, stroke_fill=(20, 8, 0, 255))
    return Image.alpha_composite(im, lay)
def fitf(path, t, size, maxw):
    while ImageFont.truetype(path, size).getbbox(t)[2] > maxw: size -= 2
    return ImageFont.truetype(path, size)
X, MW = 100, 490
AMB = (255, 176, 74, 255); GL = (255, 120, 20, 230); CR = (255, 240, 220, 255)
bg = txt(bg, (X, 175), f"全{n}曲  /  {n} Songs", ImageFont.truetype(FJ, 40), AMB, stroke=3)
bg = txt(bg, (X - 4, 262), "AMBER", fitf(FE, "BAR JAZZ", 130, MW), (255, 255, 255, 255), glow=GL, stroke=3)
bg = txt(bg, (X - 4, 392), "BAR JAZZ", fitf(FE, "BAR JAZZ", 130, MW), AMB, glow=GL, stroke=3)
bg = txt(bg, (X, 540), "琥珀色のバー・ジャズ", fitf(FJ, "琥珀色のバー・ジャズ", 64, MW), CR, stroke=3)
bg = txt(bg, (X, 672), "本物の楽器の録音音源・オリジナル曲", fitf(FJ, "本物の楽器の録音音源・オリジナル曲", 36, MW), AMB, stroke=3)
bg = txt(bg, (X, 730), f"作業用・BGM・{dur}", fitf(FJ, f"作業用・BGM・{dur}", 38, MW), CR, stroke=3)
bg = txt(bg, (X, 790), "Real Instruments - All Original", fitf(FJ, "Real Instruments - All Original", 30, MW), CR, stroke=3)
bg.convert("RGB").resize((1280, 720), Image.LANCZOS).save(dst, quality=93)
