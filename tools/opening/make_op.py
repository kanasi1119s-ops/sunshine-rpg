# リングライト・クロニクルのオープニング映像（1280×720・30fps・84秒）。曲『ひのわのそらへ』（BPM160＝1小節1.5秒）の拍に合わせてカットを切る。
# 素材: ゲームの戦闘の背景（src/assets/battle-bg）、ドット絵帳の仲間の全身・ボス・神、歩く絵、町の画面。
# 使い方: python3 make_op.py <出力.mp4> [--audio 曲.wav] [--from 秒 --to 秒] [--still 秒 --png 出力.png]
import sys, json, math, random, subprocess, argparse, glob, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--audio", default=""); ap.add_argument("--from", dest="t0", type=float, default=0)
ap.add_argument("--to", dest="t1", type=float, default=88.0); ap.add_argument("--still", type=float, default=-1); ap.add_argument("--png", default="")
a = ap.parse_args()

W, H, FPS = 1280, 720, 30
BAR = 2.0; BEAT = BAR / 4   # 『ひのわのそらへ』ジグ版: BPM120（付点4分）、1小節 2 秒
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
SHEET_NAME = ["ユーリ", "レト", "ミナ", "ガイド", "オルカ", "アヤメ"]
FIG = [(0.28, 0.69), (0.30, 0.71), (0.28, 0.69), (0.28, 0.69), (0.28, 0.69), (0.28, 0.69)]          # 全身が入る縦の帯（横の割合）
FACE = [(0.716, 0.016, 0.98, 0.82), (0.04, 0.016, 0.275, 0.82), (0.716, 0.47, 0.95, 0.935), (0.716, 0.006, 0.99, 0.855),
        (0.716, 0.006, 0.985, 0.875), (0.716, 0.006, 0.98, 0.875)]                                    # 顔の大写しの枠の内側
CENTER = [0.47, 0.50, 0.53, 0.48, 0.47, 0.45]
SHEET = [Image.open(f"{HERE}/chars/{n}.jpg").convert("RGBA") for n in SHEET_NAME]
def fr(im, box): return im.crop((int(box[0] * im.width), int(box[1] * im.height), int(box[2] * im.width), int(box[3] * im.height)))
FIGS = [fr(SHEET[k], (FIG[k][0], 0, FIG[k][1], 1)) for k in range(6)]
FACES = [fr(SHEET[k], FACE[k]) for k in range(6)]
BLUR = [cover(SHEET[k].filter(ImageFilter.GaussianBlur(SHEET[k].width / 300)), W, H, 1.1) for k in range(6)]
def fit_h(im, h): return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
FIGH = [fit_h(f, 700) for f in FIGS]
FACEH = [fit_h(f, 400) for f in FACES]
STRIP = [fit_h(fr(SHEET[k], (CENTER[k] - 0.1, 0.02, CENTER[k] + 0.1, 1.0)), 620) for k in range(6)]
LOGO = Image.open(f"{HERE}/logo-native.png").convert("RGBA")
LOGO5 = LOGO.resize((LOGO.width * 5, LOGO.height * 5), Image.NEAREST)
# ボス（人間の指示 2026-10-16「ボスも神も予言の歪みだけ」）: 手直しと動き（歩く16コマ・攻撃3種類）のある「予言の歪み」1体だけを使う。
# 絵は monster-fullbody ブランチの assets-src/monsters/kiri-yugami/anim.json から書き出したコマ（yogen/frames/）。
YDIR = os.path.join(HERE, "yogen")
_yms = json.load(open(f"{YDIR}/ms.json"))
YOGEN = {n: [(load(f"{YDIR}/frames/{n}_{i:02d}.png"), ms) for i, ms in enumerate(_yms[n])] for n in _yms}
def yogen(name, tl, loop=True):
    """動き name の、始まりから tl 秒のコマ（と何コマ目か）。"""
    fr = YOGEN[name]; tot = sum(ms for _, ms in fr) / 1000
    if loop: tl %= tot
    tl = max(0.0, min(tl, tot - 1e-6)); acc = 0.0
    for i, (im, ms) in enumerate(fr):
        acc += ms / 1000
        if tl < acc: return im, i
    return fr[-1][0], len(fr) - 1
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
LYR = [(12, 14, "星降る港　霧の向こうで"), (14, 16, "誰かが歌う　遠く"), (16, 18, "夢の地図には　星のしるしが"), (18, 20, "明日へ招く　さあ"),
       (20, 22, "目覚めの鐘　精霊の声"), (22, 24, "魔法の空へ"),
       (24, 26, "さあ駆け出そうよ　星屑の海を"), (26, 28, "灯の環の空まで　行こう"), (28, 30, "古の歌　翼に乗せ"), (30, 32, "運んでいくよ"),
       (32, 34, "どこまでも行こう　夢のその先へ"), (34, 36, "この手に輝く　ほら"), (36, 39, "リングライト・クロニクル")]
def lyrics(canvas, t):
    b = t / BAR
    for b0, b1, s in LYR:
        if b0 - 0.06 <= b < b1:
            al = min(1, (b - (b0 - 0.06)) / 0.12) * min(1, (b1 - b) / 0.1)
            im = T(s, 34, "j", fill=(255, 255, 255), stroke=3, sc=(30, 20, 60))
            put(canvas, im, W - im.width - 48, H - im.height - 30, al)

def party_run(canvas, t, ybase, x0=-120, speed=260, k=3, spacing=58, order=(0, 1, 2, 3, 4, 5), row=3):
    for j, i in enumerate(order):
        fr_ = [0, 1, 2, 1][int(t * 9 + j) % 4]
        im = scale(WF[i][row][fr_], k)
        x = x0 + speed * t - j * spacing
        bob = abs(math.sin(t * 9 + j)) * 3
        put(canvas, im, x, ybase - im.height - bob)

def boss_glow(c, im, cx, cy, beat_on, alpha=1.0):
    dark = Image.new("RGBA", im.size, (0, 0, 0, 0)); dark.paste((60, 10, 40, 255), (0, 0), im.getchannel("A"))
    put_c(c, Image.blend(dark, im, 0.5 + 0.5 * beat_on), cx, cy, alpha)

# ---------- 場面（1小節＝2秒・44小節） ----------
def frame(t):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    b = t / BAR; beat = t / BEAT; bi = int(b); fb = b - bi
    onbeat = 1 - min(1, (beat - int(beat)) * 3)
    if b < 4:   # 前奏: 夜空に光の環 → 夜明けの草原（笛がゆっくり歌う）
        if b < 2.2:
            sky(c, t, dawn=0.0); moons(c, t, alpha=ease(b / 0.8))
            ring(c, 640, 300, 330, 92, prog=ease((b - 0.3) / 1.4), alpha=1.0, glow=0.8)
            sparkles(c, t, 50, area=(0, 120, W, 520), alpha=ease((b - 0.5) / 1))
            s1 = T("かつて空を渡った光の環は　砕けて大地となった", 30, "j", fill=(240, 230, 255))
            put_c(c, s1, W / 2, 560, ease((b - 0.5) / 0.5) * (1 - ease((b - 1.8) / 0.35)))
            overlay(c, (255, 255, 255), ease((b - 2.0) / 0.2))
        else:
            u = (b - 2.2) / 1.8; dawn = ease(u * 1.3)
            bg_pan(c, BGC["meadow"], u, dx=0.6, dy=0.2)
            overlay(c, (20, 14, 50), 0.5 * (1 - dawn)); overlay(c, (255, 170, 90), 0.12 * dawn)
            ring(c, 640, 150 - 30 * u, 300, 70, alpha=0.75)
            party_run(c, (b - 2.2) * BAR * 0.6, H - 120, x0=-60, speed=200, k=3)
            s1 = T("統暦412年　港町・灯里", 30, "j"); put(c, s1, 60, 60, ease((b - 2.4) / 0.4) * (1 - ease((b - 3.6) / 0.3)))
            overlay(c, (255, 255, 255), max(1 - (b - 2.2) / 0.25, 0) + ease((b - 3.8) / 0.2))
    elif b < 12:   # ジグ A: 1小節ごとに土地をめぐる
        k = bi - 4
        scenes = [("ph", "02-first-town", "灯里"), ("ph", "03-lake-town", "硝子湖"), ("bg", "highland", "麦香野"), ("bg", "sea1", "海をこえて"),
                  ("ph", "19-now-town-desert", "砂音"), ("ph", "04-snow-town", "霜原"), ("map", None, "アルテシア"), ("bg", "void1", "")]
        kind, name, label = scenes[k]
        if kind == "ph": bg_pan(c, PH[name], fb, dx=0.7 * (1 if k % 2 else -1), dy=0.3)
        elif kind == "bg": bg_pan(c, BGC[name], fb, dx=0.9 * (1 if k % 2 else -1), dy=0.2)
        else: bg_pan(c, WMAP, fb, dx=1.0, dy=0.6)
        if k == 2: party_run(c, fb * BAR, H - 70, x0=-80, speed=700, k=4)
        if label:
            im = T(label, 64, "j", stroke=4, sc=(20, 10, 40)); put(c, im, 70 + 40 * (1 - eout(fb * 3)), H - 180, eout(fb * 4) * (1 - ease((fb - 0.85) / 0.15)))
        if k == 7:
            overlay(c, (0, 0, 0), 0.3)
            ring(c, 640, 360, 260 + 400 * ease(fb), 80 + 140 * ease(fb), alpha=1 - ease((fb - 0.6) / 0.4), glow=1.2)
            overlay(c, (255, 255, 255), ease((fb - 0.8) / 0.2))
        overlay(c, (255, 255, 255), 0.3 * onbeat * (1 if (beat % 4) < 1 else 0))
    elif b < 20:   # Aメロ: 仲間の紹介（元のイラスト）
        if bi == 19:   # 6人そろう（縦の帯を並べる）
            overlay(c, (16, 12, 30), 1.0)
            for j in range(6):
                im = STRIP[j]; x = j * (W / 6) + (W / 6 - im.width) / 2
                d = eout(fb * 4 - j * 0.15)
                put(c, im, x, 50 + 40 * (1 - d), d)
                ImageDraw.Draw(c).line([(j * W / 6, 0), (j * W / 6, H)], fill=(255, 210, 122, 120), width=3)
            sparkles(c, t, 40, alpha=0.8)
        else:
            idx = 0 if bi < 14 else bi - 13
            nm_, en, _, role, col = PARTY[idx]
            u = (b - (12 if idx == 0 else bi)) / (2 if idx == 0 else 1)
            bgimg = BLUR[idx]; bg_pan(c, bgimg, u, dx=0.4)
            overlay(c, (12, 8, 24), 0.45)
            side = -1 if idx % 2 else 1
            fig = FIGH[idx]
            fx = (W * 0.30 if side > 0 else W * 0.70) - fig.width / 2 - side * 220 * (1 - eout(u * 2.5))
            put(c, fig, fx, H - fig.height + 10, eout(u * 3))
            face = FACEH[idx]
            ax = (W * 0.74 if side > 0 else W * 0.26) - face.width / 2 + side * 160 * (1 - eout(u * 2.2 - 0.25))
            ay = 70
            al = eout(u * 2.2 - 0.25) * (1 - ease((u - 0.92) / 0.08))
            put(c, face, ax, ay, al)
            ImageDraw.Draw(c).rectangle((ax - 3, ay - 3, ax + face.width + 2, ay + face.height + 2), outline=tuple(int(v) for v in col) + (int(230 * al),), width=4)
            tx = ax; ty = ay + face.height + 16
            nmI = T(nm_, 72, "j", fill=(255, 255, 255), stroke=4, sc=tuple(int(v * 0.5) for v in col))
            enI = T(en.upper(), 28, "e", fill=tuple(int(v) for v in col), shadow=False)
            roI = T(role, 26, "j", fill=(240, 236, 248))
            put(c, nmI, tx, ty, al); put(c, enI, tx + nmI.width + 10, ty + 34, al); put(c, roI, tx + 4, ty + 92, al)
        if bi == 12 and fb < 0.15: overlay(c, (255, 255, 255), 1 - fb / 0.15)
        lyrics(c, t)
    elif b < 24:   # Bメロ: 霧の奥から「予言の歪み」が現れる（謎のことばが半小節ずつ）
        u = (b - 20) / 4
        bg_pan(c, BGC["prophecy"], u, dx=0.5)
        overlay(c, (10, 0, 20), 0.55 - 0.2 * ease((b - 21.8) / 0.4))
        if b < 22:   # 霧の中の影が歩いて近づく
            im, _ = yogen("walk", b * BAR - 40)
            im = scale(im, 1.5 + 0.7 * ease((b - 20) / 2))
            boss_glow(c, im, W / 2, H / 2 + 40, 0.15 * onbeat, ease((b - 20) / 0.8))
            overlay(c, (150, 140, 170), 0.25 * (1 - ease((b - 21) / 1)))
        elif b < 23:   # 姿を見せて、両手で打つ
            im, i = yogen("attack3", (b - 22) * BAR, loop=False)
            put_c(c, scale(im, 2.2), W / 2, H / 2 + 40)
            if i in (6, 7): overlay(c, (220, 250, 255), 0.55)
        else:
            im, _ = yogen("walk", (b - 23) * BAR)
            put_c(c, scale(im, 2.2), W / 2, H / 2 + 40)
        k = int((b - 20) * 2); sub = (b - 20) * 2 - k
        if k < 6 and sub < 0.9:
            words = ["歪み", "静まりの年", "消えた祖父", "霧の予言", "砕けた環", "真実へ"]
            im2 = T(words[k], 60, "j", fill=(220, 240, 255), stroke=3, sc=(10, 30, 60))
            put(c, im2, 80 if k % 2 == 0 else W - im2.width - 80, 90, eout(sub * 3))
        if b >= 23:
            ring(c, 640, 360, 300, 90, alpha=1.0, glow=1.4, crack=ease((b - 23) / 0.7), rot=t)
            overlay(c, (255, 255, 255), ease((b - 23.6) / 0.4))
        overlay(c, (0, 40, 80), 0.2 * onbeat)
        lyrics(c, t)
    elif b < 40:   # サビ
        k = bi - 24
        if k < 4:   # 草原を駆ける
            u = (b - 24) / 4
            bg_pan(c, BGC["meadow"], u, dx=1.0)
            ring(c, 640, 120, 360, 70, alpha=0.9, glow=1.2, rot=t * 0.2)
            party_run(c, (b - 24) * BAR, H - 60, x0=W + 60 - 1500, speed=200, k=5, spacing=84)
            sparkles(c, t, 60, alpha=0.9)
            if k == 0 and fb < 0.2: overlay(c, (255, 255, 255), 1 - fb / 0.2)
        elif k < 8:   # 戦い: 予言の歪みと4小節
            u = (b - 28) / 4
            bg_pan(c, BGC["prophecy"], u, dx=0.6)
            bx, by = 400, H / 2 + 20
            seq = ["walk", "attack", "walk", "attack2"][k - 4]
            im, i = yogen(seq, fb * BAR, loop=(seq == "walk"))
            hit = seq != "walk" and i in (6, 7)
            pshake = 10 * (1 if hit else 0) * (1 if int(t * 30) % 2 else -1)
            dead = ease((b - 31.55) / 0.4)
            if dead > 0:   # 最後に光に包まれて消える
                wim = Image.new("RGBA", im.size, (255, 255, 255, 0)); wim.putalpha(im.getchannel("A"))
                im = Image.blend(im, wim, min(1, dead * 1.5))
            put_c(c, scale(im, 2.1), bx, by, 1 - ease((b - 31.8) / 0.2))
            for j in range(6):
                sp = scale(WF[j][2][int(t * 6 + j) % 3], 4)
                put(c, sp, 900 + (j % 2) * 70 + (j // 2) * 60 + pshake, 300 + (j // 2) * 90 + (j % 2) * 30)
            if hit: overlay(c, (200, 240, 255), 0.5)
            if seq == "walk":   # 仲間の番: 拍ごとに光の環が当たる
                ring(c, bx, by, 180 + 200 * (beat % 1), 60 + 70 * (beat % 1), alpha=0.8 * (1 - beat % 1), glow=1.3)
                overlay(c, (255, 240, 200), 0.3 * onbeat)
            if k == 7: overlay(c, (255, 255, 255), ease((b - 31.6) / 0.3) * 0.9)
        elif k < 12:   # 仲間の顔（元のイラスト、半小節ずつ）→ 6人そろう
            j = min(7, int((b - 32) * 2)); sub = (b - 32) * 2 - j
            if j < 6:
                bg_pan(c, BLUR[j], sub, dx=0.4); overlay(c, (12, 8, 24), 0.35)
                face = FACEH[j]; side = 1 if j % 2 == 0 else -1
                fx = W / 2 + side * 170 - face.width / 2 - side * 120 * (1 - eout(sub * 3))
                fa = eout(sub * 6 + 0.15)
                put(c, face, fx, (H - face.height) / 2 - 20, fa)
                col = PARTY[j][4]
                ImageDraw.Draw(c).rectangle((fx - 3, (H - face.height) / 2 - 23, fx + face.width + 2, (H + face.height) / 2 - 18), outline=col + (int(230 * fa),), width=4)
                if sub < 0.08: overlay(c, (255, 255, 255), 0.4 * (1 - sub / 0.08))
            else:
                overlay(c, (16, 12, 30), 1.0)
                ring(c, 640, 70, 420, 50, alpha=0.9, glow=1.2, rot=t * 0.3)
                for q in range(6):
                    im = STRIP[q]; x = q * (W / 6) + (W / 6 - im.width) / 2
                    d = eout((b - 35) * 4 - q * 0.15)
                    put(c, im, x, 90 + 40 * (1 - d), d)
                sparkles(c, t, 50, alpha=0.9)
                overlay(c, (255, 255, 255), ease((b - 35.8) / 0.2))
        elif k < 14:   # 船で海へ
            u = (b - 36) / 2
            bg_pan(c, BGC["ship2"], u, dx=0.3, dy=0.0)
            for j in range(6):
                sp = scale(WF[j][1][1], 5); put(c, sp, 300 + j * 85, 520 + (j % 2) * 18)
        else:   # 朝日の海と大きな光の環
            u = (b - 38) / 2
            bg_pan(c, BGC["sea2"], u, dx=0.5)
            overlay(c, (255, 170, 90), 0.18)
            ring(c, 640, 230, 420, 110, alpha=1.0, glow=1.5, rot=t * 0.3)
            sparkles(c, t, 70, alpha=1.0)
            overlay(c, (255, 255, 255), ease((b - 39.75) / 0.25))
        lyrics(c, t)
    else:   # ジグ B: タイトル（ゲームのロゴ）
        u = b - 40
        sky(c, t, dawn=0.35); moons(c, t, 0.8)
        tmp = Image.new("RGBA", (W, H)); bg_pan(tmp, BGC["meadow"], 0.5, dx=0.2)
        tmp.putalpha(Image.linear_gradient("L").resize((W, H)).point(lambda v: min(255, max(0, (v - 90) * 2))))
        c.alpha_composite(tmp)
        sparkles(c, t, 80, alpha=1.0)
        al = ease(u / 0.6)
        zoom = 1 + 0.08 * (1 - eout(u / 1.5))
        lg = LOGO5 if abs(zoom - 1) < 0.004 else LOGO5.resize((round(LOGO5.width * zoom), round(LOGO5.height * zoom)), Image.NEAREST)
        glow = lg.filter(ImageFilter.GaussianBlur(14)); put_c(c, glow, W / 2, 300, 0.7 * al * (0.6 + 0.4 * math.sin(t * 3)))
        put_c(c, lg, W / 2, 300, al)
        jp = T("リングライト・クロニクル", 40, "j", fill=(255, 255, 255), stroke=3, sc=(40, 30, 70))
        put_c(c, jp, W / 2, 470, ease((u - 0.8) / 0.6))
        if u < 0.2: overlay(c, (255, 255, 255), 1 - u / 0.2)
        if u >= 3:   # 全員で一発（最後の小節の頭）
            overlay(c, (255, 255, 255), max(0, 1 - (u - 3) / 0.35))
            cr = T("© 2026 サンシャインソフトウェア", 22, "s", fill=(230, 230, 240)); put_c(c, cr, W / 2, H - 40, ease((u - 3.2) / 0.4))
        overlay(c, (0, 0, 0), ease((u - 3.6) / 0.4))
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
