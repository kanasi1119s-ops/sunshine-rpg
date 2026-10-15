# リングライト・クロニクルのオープニング映像（1280×720・30fps・84秒）。曲『ひのわのそらへ』（BPM160＝1小節1.5秒）の拍に合わせてカットを切る。
# 素材: ゲームの戦闘の背景（src/assets/battle-bg）、ドット絵帳の仲間の全身・ボス・神、歩く絵、町の画面。
# 使い方: python3 make_op.py <出力.mp4> [--audio 曲.wav] [--from 秒 --to 秒] [--still 秒 --png 出力.png]
import sys, math, random, subprocess, argparse, glob, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--audio", default=""); ap.add_argument("--from", dest="t0", type=float, default=0)
ap.add_argument("--to", dest="t1", type=float, default=84.0); ap.add_argument("--still", type=float, default=-1); ap.add_argument("--png", default="")
a = ap.parse_args()

W, H, FPS = 1280, 720, 30
BAR = 1.5; BEAT = BAR / 4
HERE = os.path.dirname(os.path.abspath(__file__))
GAME = "/home/claude/wt-dirac/src/assets"
ART = os.path.join(HERE, "art")
PHOTO = os.path.join(HERE, "..", "note", "photos")
WALK = os.path.join(HERE, "..", "header")
FJ = os.path.join(HERE, "fonts/fontsource-shippori-mincho-b1-5.3.0/files/shippori-mincho-b1-japanese-800-normal.woff")
FE = os.path.join(HERE, "fonts/fontsource-cinzel-5.3.0/files/cinzel-latin-700-normal.woff")
FS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def font(p, s): return ImageFont.truetype(p, s)

def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eout(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3

# ---------- 素材 ----------
def load(p): return Image.open(p).convert("RGBA")
def cover(img, w, h, scale=1.0):
    """img を w×h を覆う大きさに（ドット絵はくっきり NEAREST）。scale>1 で余白を作る（パン用）"""
    k = max(w / img.width, h / img.height) * scale
    return img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))), Image.NEAREST)
BG = {n: load(f"{GAME}/battle-bg/{n}.png") for n in ["meadow", "highland", "sea1", "sea2", "ship1", "ship2", "snow1", "snow2", "volcano1", "void1", "void2", "prophecy", "warp1", "warp2", "forest-shrine1", "cave"]}
BGC = {n: cover(im, W, H, 1.18) for n, im in BG.items()}
def photo(name, crop_top=34):
    im = load(glob.glob(f"{PHOTO}/{name}.*")[0]); im = im.crop((0, crop_top, im.width, im.height - (0 if crop_top < 40 else 0)))
    return cover(im, W, H, 1.12)
PH = {k: photo(k) for k in ["02-first-town", "03-lake-town", "04-snow-town", "18-now-village", "19-now-town-desert"]}
WMAP = cover(load(glob.glob(f"{PHOTO}/10-world-map.*")[0]), W, H, 1.35)
def art(prefix): return load(glob.glob(f"{ART}/{prefix}_*.png")[0])
PARTY = [("ユーリ", "Yuri", "000", "灯りの相談所の新人調査員", (255, 160, 70)), ("レト", "Reto", "002", "皮肉屋の先輩調査員", (200, 70, 70)),
         ("ミナ", "Mina", "004", "水紋の術をつかう村の娘", (110, 190, 240)), ("コハク", "Kohaku", "006", "湖の町の交易商人の娘", (240, 200, 90)),
         ("オルカ", "Orca", "008", "鉱山で働いてきた力持ち", (230, 130, 60)), ("アヤメ", "Ayame", "010", "霜原の静かな案内人", (190, 150, 240))]
FULL = [art(p[2]) for p in PARTY]
BOSS = [art(f"{i:03d}") for i in range(220, 229)]
GODS = [art(f"{i:03d}") for i in range(230, 238)]
WALKS = [load(f"{WALK}/walk-c{i}.png") for i in range(6)]
def walk_frame(i, row, fr):
    sh = WALKS[i]; f = sh.crop((fr * 16, row * 32, fr * 16 + 16, row * 32 + 32))
    bg = sh.getpixel((0, 0))[:3]
    px = np.array(f); m = (px[..., 0] == bg[0]) & (px[..., 1] == bg[1]) & (px[..., 2] == bg[2]); px[m, 3] = 0
    return Image.fromarray(px)
WF = [[[walk_frame(i, r, f) for f in range(3)] for r in range(4)] for i in range(6)]

# ---------- 文字（先に描いておく） ----------
def text_img(s, f, fill=(255, 255, 255), stroke=0, sc=(0, 0, 0), shadow=True, spacing=0):
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    bb = d0.textbbox((0, 0), s, font=f, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 12, bb[3] - bb[1] + 12
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((6 - bb[0] + 3, 6 - bb[1] + 3), s, font=f, fill=(0, 0, 0, 170), stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(3))); d = ImageDraw.Draw(im)
    d.text((6 - bb[0], 6 - bb[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sc)
    return im
_tc = {}
def T(s, size, kind="j", **kw):
    key = (s, size, kind, tuple(sorted(kw.items())))
    if key not in _tc: _tc[key] = text_img(s, font({"j": FJ, "e": FE, "s": FS}[kind], size), **kw)
    return _tc[key]

def put(canvas, im, x, y, alpha=1.0):
    if alpha <= 0.003: return
    if alpha < 0.999:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(im, (int(round(x)), int(round(y))))
def put_c(canvas, im, cx, cy, alpha=1.0): put(canvas, im, cx - im.width / 2, cy - im.height / 2, alpha)
def scale(im, k): return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.NEAREST)

def bg_pan(canvas, big, u, dx=1.0, dy=0.3, tint=None):
    """big（W×H より大きい）を u（0〜1）でパンして貼る"""
    mx, my = big.width - W, big.height - H
    x = int(mx * (0.5 + (u - 0.5) * dx)) if dx >= 0 else int(mx * (0.5 - (u - 0.5) * -dx))
    y = int(my * (0.5 + (u - 0.5) * dy))
    x = max(0, min(mx, x)); y = max(0, min(my, y))
    crop = big.crop((x, y, x + W, y + H))
    if tint: crop = Image.blend(crop, Image.new("RGBA", (W, H), tint + (255,)), tint_amt(tint))
    canvas.alpha_composite(crop)
def tint_amt(t): return 0.0
def overlay(canvas, color, alpha):
    if alpha > 0.003: canvas.alpha_composite(Image.new("RGBA", (W, H), color + (int(255 * min(1, alpha)),)))

VIG = Image.new("L", (W, H), 0)
_v = np.zeros((H, W), np.float32); yy, xx = np.mgrid[0:H, 0:W]
_v = np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2, 0, 1) ** 1.6
VIGNETTE = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), (_v * 200).astype(np.uint8)]), "RGBA")

# ---------- 空・月・光の環（手で描く） ----------
STARS = [(random.Random(i).random() * W, random.Random(i + 999).random() * H * 0.7, random.Random(i + 77).random()) for i in range(260)]
def sky(canvas, t, dawn=0.0):
    top = np.array([12, 10, 34]) * (1 - dawn) + np.array([60, 80, 150]) * dawn
    bot = np.array([40, 26, 80]) * (1 - dawn) + np.array([250, 170, 110]) * dawn
    g = np.linspace(0, 1, H)[:, None]
    col = (top[None, :] * (1 - g) + bot[None, :] * g).astype(np.uint8)
    canvas.alpha_composite(Image.fromarray(np.repeat(col[:, None, :], W, axis=1)).convert("RGBA"))
    d = ImageDraw.Draw(canvas)
    for x, y, b in STARS:
        tw = 0.6 + 0.4 * math.sin(t * 3 + b * 20)
        v = int(255 * b * tw * (1 - dawn * 0.9))
        if v > 30: d.point((x, y), fill=(v, v, min(255, v + 30), 255))
def moons(canvas, t, alpha=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (cx, cy, r, col) in [(1010, 140, 46, (240, 240, 255)), (1090, 210, 16, (230, 80, 80))]:
        for k in range(6, 0, -1): d.ellipse((cx - r - k * 6, cy - r - k * 6, cx + r + k * 6, cy + r + k * 6), fill=col + (int(10 * k * alpha),))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (int(255 * alpha),))
    canvas.alpha_composite(lay)
def ring(canvas, cx, cy, rx, ry, prog=1.0, alpha=1.0, glow=1.0, crack=0.0, rot=0.0):
    """光の環。prog で描き始めから一周まで、crack で割れ目"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    n = 220; pts = []
    for i in range(int(n * prog) + 1):
        th = -math.pi / 2 + rot + 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(th), cy + ry * math.sin(th)))
    if len(pts) > 1:
        for wdt, col, al in [(26, (255, 170, 60), 40), (14, (255, 200, 100), 80), (7, (255, 225, 150), 200), (3, (255, 250, 230), 255)]:
            segs = pts if crack <= 0 else [p for j, p in enumerate(pts) if not (int(j / n * 9) % 3 == 1 and crack > (j % 7) / 7)]
            d.line(segs, fill=col + (int(al * alpha * glow if wdt > 7 else al * alpha),), width=wdt, joint="curve")
    lay = lay.filter(ImageFilter.GaussianBlur(1.2))
    canvas.alpha_composite(lay)
def sparkles(canvas, t, n=40, seed=3, area=(0, 0, W, H), col=(255, 230, 160), speed=30, alpha=1.0):
    d = ImageDraw.Draw(canvas); r = random.Random(seed)
    for i in range(n):
        x0, y0 = area[0] + r.random() * (area[2] - area[0]), area[1] + r.random() * (area[3] - area[1])
        ph = r.random() * 10; y = (y0 - t * speed * (0.5 + r.random())) % (area[3] - area[1]) + area[1]
        b = (0.5 + 0.5 * math.sin(t * 4 + ph)) * alpha
        s = 1 + int(2 * r.random())
        d.ellipse((x0 - s, y - s, x0 + s, y + s), fill=col + (int(220 * b),))

# ---------- 歌詞（小節 → 行） ----------
LYR = [(16, 18, "朝の港　風が呼んだ"), (18, 20, "地図の向こう　遠い空"), (20, 22, "鞄ひとつ　胸が踊る"), (22, 24, "明日へ行こう"),
       (24, 26, "光の環を追え"), (26, 28, "目覚めた石が導く"), (28, 30, "その先"), (30, 32, "まだ見ぬ明日"),
       (32, 34, "駆け出そう　風より"), (34, 36, "灯の環の空"), (36, 38, "めぐりあう仲間と"), (38, 40, "紡いでくよ"),
       (40, 42, "どこまでも　遠くへ"), (42, 44, "光の先"), (44, 47, "リングライト・クロニクル")]
def lyrics(canvas, t):
    b = t / BAR
    for b0, b1, s in LYR:
        if b0 - 0.08 <= b < b1:
            al = min(1, (b - (b0 - 0.08)) / 0.15) * min(1, (b1 - b) / 0.12)
            im = T(s, 34, "j", fill=(255, 255, 255), stroke=3, sc=(30, 20, 60))
            put(canvas, im, W - im.width - 48, H - im.height - 30, al)

def party_run(canvas, t, ybase, x0=-120, speed=260, k=3, spacing=58, order=(0, 1, 2, 3, 4, 5), row=3):
    for j, i in enumerate(order):
        fr = int(t * 9 + j) % 3; fr = [0, 1, 2, 1][int(t * 9 + j) % 4] if True else fr
        im = scale(WF[i][row][fr], k)
        x = x0 + speed * t - j * spacing
        bob = abs(math.sin(t * 9 + j)) * 3
        put(canvas, im, x, ybase - im.height - bob)

# ---------- 場面 ----------
def frame(t):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    b = t / BAR; beat = t / BEAT; bi = int(b); fb = b - bi
    onbeat = 1 - min(1, (beat - int(beat)) * 3)   # 拍の頭で 1、すぐ 0 へ
    if b < 8:   # 前奏: 夜空に光の環が生まれる → 夜明けの草原
        if b < 4:
            sky(c, t, dawn=0.0); moons(c, t, alpha=ease(b / 1.5))
            ring(c, 640, 300, 330, 92, prog=ease((b - 0.8) / 2.6), alpha=1.0, glow=0.8)
            sparkles(c, t, 50, area=(0, 120, W, 520), alpha=ease((b - 1) / 2))
            s1 = T("かつて空を渡った光の環は　砕けて大地となった", 30, "j", fill=(240, 230, 255))
            put_c(c, s1, W / 2, 560, ease((b - 1.2) / 0.8) * (1 - ease((b - 3.4) / 0.5)))
        else:
            u = (b - 4) / 4
            dawn = ease(u * 1.4)
            bg_pan(c, BGC["meadow"], u, dx=0.6, dy=0.2)
            overlay(c, (20, 14, 50), 0.55 * (1 - dawn)); overlay(c, (255, 170, 90), 0.12 * dawn)
            ring(c, 640, 150 - 30 * u, 300, 70, alpha=0.75)
            party_run(c, (b - 4) * BAR * 0.55, H - 120, x0=-60, speed=200, k=3)
            s1 = T("統暦412年　港町・灯里", 30, "j"); put(c, s1, 60, 60, ease((b - 4.3) / 0.6) * (1 - ease((b - 7.3) / 0.5)))
            if b > 7.5: overlay(c, (255, 255, 255), ease((b - 7.5) / 0.5))
    elif b < 16:   # リフ: 拍に合わせた土地のモンタージュ
        k = bi - 8
        scenes = [("ph", "02-first-town", "灯里"), ("ph", "03-lake-town", "硝子湖"), ("bg", "highland", "麦香野"), ("bg", "sea1", "海をこえて"),
                  ("ph", "19-now-town-desert", "砂音"), ("ph", "04-snow-town", "霜原"), ("map", None, "アルテシア"), ("bg", "void1", "")]
        kind, name, label = scenes[k]
        if kind == "ph": bg_pan(c, PH[name], fb, dx=0.7 * (1 if k % 2 else -1), dy=0.3)
        elif kind == "bg": bg_pan(c, BGC[name], fb, dx=0.9 * (1 if k % 2 else -1), dy=0.2)
        else: bg_pan(c, WMAP, fb, dx=1.0, dy=0.6)
        if k == 2: party_run(c, fb * BAR, H - 70, x0=-80, speed=900, k=4)
        if k == 3: put(c, scale(BOSS[0], 0), 0, 0, 0) if False else None
        if label:
            im = T(label, 64, "j", stroke=4, sc=(20, 10, 40)); put(c, im, 70 + 40 * (1 - eout(fb * 3)), H - 180, eout(fb * 4) * (1 - ease((fb - 0.85) / 0.15)))
        if k == 7:   # ゆがみの気配 → 白くはじける
            overlay(c, (0, 0, 0), 0.3)
            ring(c, 640, 360, 260 + 400 * ease(fb), 80 + 140 * ease(fb), alpha=1 - ease((fb - 0.6) / 0.4), glow=1.2)
            overlay(c, (255, 255, 255), ease((fb - 0.75) / 0.25))
        overlay(c, (255, 255, 255), 0.35 * onbeat * (1 if (beat % 4) < 1 else 0))
    elif b < 24:   # Aメロ: 仲間の紹介
        k = min(6, max(0, bi - 17)) if bi >= 17 else 0
        if bi == 23:   # 6人そろう
            bg_pan(c, BGC["meadow"], fb, dx=0.3)
            overlay(c, (20, 20, 40), 0.25)
            for j in range(6):
                im = scale(FULL[j], 0.9)
                x = 120 + j * 185; y = H - im.height - 20 + 30 * (1 - eout((fb * 4) - j * 0.18))
                put(c, im, x - 40, y, eout(fb * 4 - j * 0.18))
            sparkles(c, t, 40, area=(0, 0, W, H), alpha=0.8)
        else:
            idx = 0 if bi < 18 else bi - 17
            nm_, en, _, role, col = PARTY[idx]
            u = (b - (16 if idx == 0 else bi)) / (2 if idx == 0 else 1)
            g = np.linspace(0, 1, W)[None, :]
            c1 = np.array(col) * 0.35; c2 = np.array([20, 16, 40])
            grad = (c1[None, None, :] * (1 - g[..., None]) + c2[None, None, :] * g[..., None]).astype(np.uint8)
            c.alpha_composite(Image.fromarray(np.repeat(grad, H, axis=0)).convert("RGBA"))
            d = ImageDraw.Draw(c)
            for s in range(14):   # 斜めの光の帯
                x = (s * 160 + t * 220) % (W + 400) - 200
                d.polygon([(x, 0), (x + 40, 0), (x - 260, H), (x - 300, H)], fill=tuple(int(v) for v in col) + (18,))
            im = scale(FULL[idx], 2.4)
            side = -1 if idx % 2 else 1
            cx = (W * 0.68 if side > 0 else W * 0.32) + side * 260 * (1 - eout(u * 2.5)) - side * 30 * u
            put_c(c, im, cx, H / 2 + 40, eout(u * 3))
            tx = 90 if side > 0 else W - 520
            nmI = T(nm_, 96, "j", fill=(255, 255, 255), stroke=4, sc=tuple(int(v * 0.5) for v in col))
            enI = T(en.upper(), 34, "e", fill=tuple(int(v) for v in col), shadow=False)
            roI = T(role, 30, "j", fill=(235, 235, 245))
            al = eout(u * 3) * (1 - ease((u - 0.9) / 0.1))
            put(c, enI, tx + 40 * (1 - eout(u * 3)), 190, al); put(c, nmI, tx, 230, al); put(c, roI, tx + 6, 360, al)
            d.line([(tx + 6, 350), (tx + 6 + 380 * eout(u * 2.5), 350)], fill=tuple(int(v) for v in col) + (int(255 * al),), width=4)
        if bi == 16 and fb < 0.2: overlay(c, (255, 255, 255), 1 - fb / 0.2)
        lyrics(c, t)
    elif b < 32:   # Bメロ: ゆがみの影（謎の気配）
        k = bi - 24
        bgs = ["prophecy", "cave", "forest-shrine1", "volcano1", "warp1", "void2", "warp2", "void1"]
        bg_pan(c, BGC[bgs[k]], fb, dx=0.6 * (1 if k % 2 else -1))
        overlay(c, (10, 0, 20), 0.45)
        boss = BOSS[min(len(BOSS) - 1, k)]
        im = scale(boss, 2.2 + 0.25 * fb)
        dark = Image.new("RGBA", im.size, (0, 0, 0, 0)); dark.paste((60, 10, 40, 255), (0, 0), im.getchannel("A"))
        show = Image.blend(dark, im, 0.5 + 0.5 * onbeat)   # 拍のたびに赤く光って姿が浮かぶ
        put_c(c, show, W / 2 + (k % 2 * 2 - 1) * 180, H / 2 + 20, eout(fb * 3))
        if k < 6:
            words = ["歪み", "静まりの年", "消えた祖父", "灯芯都の影", "砕けた環", "真実へ"]
            im2 = T(words[k], 60, "j", fill=(255, 210, 220), stroke=3, sc=(80, 0, 30))
            put(c, im2, 80 if k % 2 == 0 else W - im2.width - 80, 90, eout(fb * 3) * (1 - ease((fb - 0.8) / 0.2)))
        if k >= 6:
            ring(c, 640, 360, 300, 90, alpha=1.0, glow=1.4, crack=ease((b - 30) / 1.5), rot=t)
            overlay(c, (255, 255, 255), ease((b - 31.4) / 0.6))
        overlay(c, (120, 0, 30), 0.25 * onbeat)
        lyrics(c, t)
    elif b < 48:   # サビ
        k = bi - 32
        if k < 4:   # 草原を駆ける
            u = (b - 32) / 4
            bg_pan(c, BGC["meadow"], u, dx=1.0)
            ring(c, 640, 120, 360, 70, alpha=0.9, glow=1.2, rot=t * 0.2)
            party_run(c, (b - 32) * BAR, H - 60, x0=W + 60 - 1400, speed=230, k=5, spacing=84)
            sparkles(c, t, 60, alpha=0.9)
            if k == 0 and fb < 0.25: overlay(c, (255, 255, 255), 1 - fb / 0.25)
        elif k < 8:   # 戦い
            boss = BOSS[[0, 2, 4, 6][k - 4]]; bgn = ["meadow", "snow1", "volcano1", "sea2"][k - 4]
            bg_pan(c, BGC[bgn], fb, dx=0.8 * (1 if k % 2 else -1))
            im = scale(boss, 2.0); shake = 8 * onbeat
            put_c(c, im, 400 + shake, H / 2 + 10)
            for j in range(6):
                sp = scale(WF[j][2][int(t * 6 + j) % 3], 4)   # 左を向いて構える
                put(c, sp, 900 + (j % 2) * 70 + (j // 2) * 60, 300 + (j // 2) * 90 + (j % 2) * 30)
            overlay(c, (255, 240, 200), 0.5 * onbeat * (1 if int(beat) % 2 == 0 else 0))
            ring(c, 400, H / 2 + 10, 180 + 200 * fb, 60 + 70 * fb, alpha=0.8 * (1 - fb), glow=1.3)
        elif k < 12:   # 8つの神（半小節ずつ）
            j = min(7, int((b - 40) * 2))
            bg_pan(c, BGC["void2" if j % 2 else "void1"], (b - 40) / 4, dx=0.5)
            g = GODS[j]; im = scale(g, 2.3)
            sub = (b - 40) * 2 - j
            put_c(c, im, W / 2 + (j % 2 * 2 - 1) * 200, H / 2, eout(sub * 4) * (1 - ease((sub - 0.85) / 0.15)))
            overlay(c, (255, 255, 255), 0.6 * max(0, 1 - sub * 6))
        elif k < 14:   # 船で海へ
            u = (b - 44) / 2
            bg_pan(c, BGC["ship2"], u, dx=0.3, dy=0.0)
            for j in range(6):   # 甲板の上に並んで、前（海のほう）を見る
                sp = scale(WF[j][1][1], 5); put(c, sp, 300 + j * 85, 520 + (j % 2) * 18)
        else:   # 朝日の海と大きな光の環
            u = (b - 46) / 2
            bg_pan(c, BGC["sea2"], u, dx=0.5)
            overlay(c, (255, 170, 90), 0.18)
            ring(c, 640, 230, 420, 110, alpha=1.0, glow=1.5, rot=t * 0.3)
            sparkles(c, t, 70, alpha=1.0)
        lyrics(c, t)
    else:   # 後奏: タイトル
        u = (b - 48)
        sky(c, t, dawn=0.35); moons(c, t, 0.8)
        bg = BGC["meadow"]; tmp = Image.new("RGBA", (W, H)); bg_pan(tmp, bg, 0.5, dx=0.2)
        tmp.putalpha(Image.linear_gradient("L").resize((W, H)).point(lambda v: min(255, max(0, (v - 90) * 2))))
        c.alpha_composite(tmp)
        ring(c, 640, 300, 400, 110, prog=ease(u / 2.5), alpha=1.0, glow=1.4, rot=0)
        sparkles(c, t, 80, alpha=1.0)
        en = T("Ringlight Chronicle", 96, "e", fill=(255, 236, 190), stroke=2, sc=(90, 50, 10))
        jp = T("リングライト・クロニクル", 44, "j", fill=(255, 255, 255), stroke=3, sc=(40, 30, 70))
        al = ease((u - 1.8) / 1.0)
        zoom = 1 + 0.06 * (1 - eout((u - 1.8) / 1.5))
        put_c(c, scale(en, zoom) if zoom != 1 else en, W / 2, 300, al)
        put_c(c, jp, W / 2, 395, ease((u - 2.6) / 0.8))
        if u >= 4:   # 全員で一発
            overlay(c, (255, 255, 255), max(0, 1 - (u - 4) / 0.4))
            cr = T("© 2026 サンシャインソフトウェア", 22, "s", fill=(230, 230, 240)); put_c(c, cr, W / 2, H - 40, ease((u - 4.6) / 0.6))
        overlay(c, (0, 0, 0), ease((u - 7.2) / 0.8))
    c.alpha_composite(VIGNETTE)
    return c.convert("RGB")

if a.still >= 0:
    frame(a.still).save(a.png or a.out); sys.exit(0)
cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
if a.audio: cmd += ["-ss", str(a.t0), "-t", str(a.t1 - a.t0), "-i", a.audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
n0, n1 = int(a.t0 * FPS), int(a.t1 * FPS)
for n in range(n0, n1):
    p.stdin.write(frame(n / FPS).tobytes())
    if n % 150 == 0: print(f"{n / FPS:.1f}秒", flush=True)
p.stdin.close(); p.wait()
print("書き出し:", a.out)
