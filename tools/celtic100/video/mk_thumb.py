# 「銀の笛と百の夜」全100曲の動画のサムネイル（1280x720）。いつもの形（Dream Island・ケルト異世界ファンタジーと同じ）:
#   左下に、大きな英語のタイトル → 英語の副題（色つき） → 日本語のタイトルと曲数 → 長さと曲数（枠なし）。右下に Sunshine Pixel Sound。
#   この絵は左に少女がいるので、文字は左下の草花の上に置き、下と左を少し暗くする。
# 使い方: python3 mk_thumb.py <背景の1コマ.png（1920x1080）> <出力.jpg> <長さの文字（例: 7h 12m）>
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out, dur = sys.argv[1:4]
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
F = lambda s: ImageFont.truetype(SERIF, s)
im = Image.open(src).convert("RGB").resize((1280, 720), Image.LANCZOS).convert("RGBA")
h = np.linspace(0, 1, 720)[:, None]; w = np.linspace(0, 1, 1280)[None, :]
a = np.clip((h - 0.42) / 0.58, 0, 1) ** 1.1 * 215 * np.clip(1.35 - w, 0, 1)
shade = Image.new("RGBA", (1280, 720), (12, 10, 34, 0)); shade.putalpha(Image.fromarray(a.astype(np.uint8))); im = Image.alpha_composite(im, shade)
SUB_C = (255, 214, 150); BOX_C = (190, 225, 255)
L = [("Silver Flute", F(100), (250, 250, 255), 400), ("A Hundred Nights · Celtic Fantasy Flute", F(34), SUB_C, 530), ("銀の笛と百の夜　ケルト幻想の笛　全100曲", F(32), (255, 255, 255), 578)]
sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
for t, f, c, y in L: d.text((60, y), t, font=f, fill=(0, 0, 0, 220), stroke_width=6, stroke_fill=(0, 0, 0, 220))
sh = sh.filter(ImageFilter.GaussianBlur(6)); im = Image.alpha_composite(im, sh); d = ImageDraw.Draw(im)
for t, f, c, y in L: d.text((60, y), t, font=f, fill=c + (255,), stroke_width=1, stroke_fill=(10, 14, 30, 255))
bt = f"{dur} · 100 songs"; bf = F(28); bb = d.textbbox((0, 0), bt, font=bf)
d.text((62, 650 - bb[1]), bt, font=bf, fill=BOX_C + (255,), stroke_width=3, stroke_fill=(0, 0, 0, 170))
cf = F(24); cb = d.textbbox((0, 0), "Sunshine Pixel Sound", font=cf)
d.text((1280 - 32 - (cb[2] - cb[0]), 720 - 26 - (cb[3] - cb[1]) - cb[1]), "Sunshine Pixel Sound", font=cf, fill=(240, 240, 250, 235), stroke_width=2, stroke_fill=(0, 0, 0, 160))
im.convert("RGB").save(out, quality=92)
