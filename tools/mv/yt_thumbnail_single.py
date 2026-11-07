"""1曲ぶんの YouTube サムネイル（1280×720）。2026-11-08 白い息のリテイク・ハニー・サワー。
  python3 yt_thumbnail_single.py whitebreath|honeysour <出力.jpg>"""
import sys, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lyrics_data as LD
NAME, OUT = sys.argv[1:3]
NF = "/usr/share/fonts/opentype/noto/"; GF = "/usr/share/fonts/truetype/google-fonts/"
W, H = 1920, 1080
def txt(im, xy, t, f, col, stroke_col, stroke=0, glow=None):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text(xy, t, font=f, fill=glow, stroke_width=stroke + 6, stroke_fill=glow)
        lay = Image.alpha_composite(lay, g.filter(ImageFilter.GaussianBlur(14)))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((xy[0] + 4, xy[1] + 6), t, font=f, fill=(0, 0, 0, 160), stroke_width=stroke + 2, stroke_fill=(0, 0, 0, 160))
    lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(lay).text(xy, t, font=f, fill=col, stroke_width=stroke, stroke_fill=stroke_col)
    return Image.alpha_composite(im, lay)
def fit(path, t, size, maxw, index=0):
    while ImageFont.truetype(path, size, index=index).getlength(t) > maxw: size -= 2
    return ImageFont.truetype(path, size, index=index)
if NAME == "whitebreath":
    D = LD.WHITEBREATH
    im = cv2.imread("/tmp/ab/wbmv/fr/169.png")[..., ::-1]                        # 口を開けて歌うコマ
    bg = Image.fromarray(cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4)).convert("RGBA")
    a = np.asarray(bg).astype(np.float32); x = np.linspace(1, 0, W)[None, :, None]
    a[..., :3] *= (1 - 0.55 * np.clip(x * 1.6 - 0.5, 0, 1)); bg = Image.fromarray(a.astype(np.uint8))
    X = 70; JF = NF + "NotoSerifCJK-SemiBold.ttc"
    bg = txt(bg, (X, 300), "白い息の", fit(JF, "白い息の", 150, 640), (245, 248, 255), (16, 24, 52), 4, (120, 170, 255, 170))
    bg = txt(bg, (X, 470), "リテイク", fit(JF, "リテイク", 150, 640), (255, 228, 180), (16, 24, 52), 4, (255, 170, 90, 150))
    bg = txt(bg, (X + 6, 660), D["title_en"], fit(GF + "Lora-Italic-Variable.ttf", D["title_en"], 64, 620), (255, 205, 150), (16, 24, 52), 2)
    bg = txt(bg, (X + 6, 770), "歌：重音テト / Vocal: Kasane Teto", fit(NF + "NotoSansCJK-Bold.ttc", "歌：重音テト / Vocal: Kasane Teto", 40, 620), (235, 240, 250), (16, 24, 52), 3)
    bg = txt(bg, (X + 6, 830), "歌詞つき（日本語・英語） / JP & EN Lyrics", fit(NF + "NotoSansCJK-Bold.ttc", "歌詞つき（日本語・英語） / JP & EN Lyrics", 34, 620), (210, 220, 240), (16, 24, 52), 3)
else:
    D = LD.HONEYSOUR
    cap = cv2.VideoCapture("/mnt/user-data/attachments/945c1fd5-bcd9-525d-8abc-22b5d22e1041/aa5ffe71-gemini_generated_video_69FBA302.mp4")
    cap.set(cv2.CAP_PROP_POS_MSEC, 5700); _, f = cap.read(); f = f[..., ::-1]           # レモンのアップ
    # 背景: はちみつ色からソーダのピンクへのグラデーションに、はじける泡
    yy, xx = np.mgrid[0:H, 0:W]; g = np.clip((xx / W) * 0.7 + (yy / H) * 0.3, 0, 1)[..., None]
    a = (np.array([255, 196, 60]) * (1 - g) + np.array([255, 120, 170]) * g).astype(np.uint8)
    bg = Image.fromarray(a).convert("RGBA"); bl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); db = ImageDraw.Draw(bl)
    rng = np.random.default_rng(7)
    for _ in range(70):
        x, y, r = rng.integers(0, W), rng.integers(0, H), rng.integers(6, 40)
        db.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, 150), width=3); db.ellipse((x - r * 0.5, y - r * 0.6, x - r * 0.2, y - r * 0.3), fill=(255, 255, 255, 170))
    bg = Image.alpha_composite(bg, bl)
    fg = Image.fromarray(cv2.resize(f, (int(H * f.shape[1] / f.shape[0]), H), interpolation=cv2.INTER_LANCZOS4)).convert("RGBA")
    bg.alpha_composite(fg, (W - fg.width - 90, 0))
    X = 70; JF = NF + "NotoSansCJK-Black.ttc"; PK = (150, 40, 110)
    bg = txt(bg, (X, 230), "ハニー・", fit(JF, "ハニー・", 170, 900), (255, 255, 255), PK, 10)
    bg = txt(bg, (X, 430), "サワー", fit(JF, "サワー", 190, 900), (255, 206, 60), PK, 10)
    bg = txt(bg, (X + 10, 660), D["title_en"], fit(GF + "Poppins-Bold.ttf", D["title_en"], 80, 700), (255, 255, 255), PK, 5)
    bg = txt(bg, (X + 10, 790), "歌：重音テト（女声×男性ボイス）", fit(NF + "NotoSansCJK-Bold.ttc", "歌：重音テト（女声×男性ボイス）", 44, 860), (255, 255, 255), PK, 4)
    bg = txt(bg, (X + 10, 860), "Kasane Teto Duet / JP & EN Lyrics", fit(GF + "Poppins-Bold.ttf", "Kasane Teto Duet / JP & EN Lyrics", 40, 860), (255, 235, 245), PK, 3)
bg.convert("RGB").resize((1280, 720), Image.LANCZOS).save(OUT, quality=93)
print("ok", OUT)
