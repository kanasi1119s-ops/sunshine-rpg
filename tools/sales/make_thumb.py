"""販売ページのサムネイル（カッコいい1枚）を作る（2026-10-07、人間の指示「カッコいいサムネ画像も作ってください」）。
1120×840 で組み立て、ちょうど半分に縮めた 560×420 も作る（絵は偶数倍で置くので、半分にしてもドットがくずれない）。PNG。
使い方: python3 tools/sales/make_thumb.py パックのフォルダ 出力フォルダ
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FD = "/usr/share/fonts/opentype/noto/"
W, H = 1120, 840


def font(name, size):
    return ImageFont.truetype(FD + name, size, index=0)


def sprite(pack, kind, no, k):
    sub = "雑魚_96px" if kind == "mob" else "ボス_256px"
    im = Image.open(os.path.join(pack, sub, "1倍", f"{no}.png")).convert("RGBA")
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def glow_of(im, color, blur, strength=1.0):
    """まわりに余白をとってからぼかす（四角い跡が出ないように）。左上が -blur*3 ずれた画像を返す"""
    p = blur * 3
    a = Image.new("L", (im.width + 2 * p, im.height + 2 * p), 0); a.paste(im.split()[3], (p, p))
    a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: min(255, int(v * strength)))
    g = Image.new("RGBA", a.size, color + (0,)); g.putalpha(a)
    return g


def put_glow(bg, im, color, blur, strength, x, y):
    g = glow_of(im, color, blur, strength)
    bg.alpha_composite(g, (x - blur * 3, y - blur * 3)) if x - blur * 3 >= 0 and y - blur * 3 >= 0 else bg.paste(g, (x - blur * 3, y - blur * 3), g)


def darken(im, k):
    r, g, b, a = im.split()
    f = lambda v: int(v * k)
    return Image.merge("RGBA", (r.point(f), g.point(f), b.point(f), a))


def main():
    pack, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rnd = random.Random(3)
    # 背景: 中心が赤金に燃える、黒い放射グラデーション
    bg = Image.new("RGB", (W, H), (8, 4, 10))
    px = bg.load()
    cx, cy = W / 2, 330
    for y in range(H):
        for x in range(0, W):
            d = math.hypot(x - cx, (y - cy) * 1.15) / 620
            t = max(0.0, 1 - d)
            px[x, y] = (int(8 + 120 * t ** 1.6), int(4 + 52 * t ** 2.2), int(10 + 20 * t ** 2.5))
    bg = bg.convert("RGBA")
    # 光の筋（中心から放射）
    rays = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(rays)
    for k in range(28):
        a0 = k * 2 * math.pi / 28 + 0.05
        a1 = a0 + 0.06
        R = 1400
        dr.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=38 if k % 2 else 22)
    rays = rays.filter(ImageFilter.GaussianBlur(6))
    bg = Image.composite(Image.new("RGBA", (W, H), (255, 190, 90, 255)), bg, rays)
    # 奥: 悪夢の蝗神（2倍）と後光
    ring = sprite(pack, "boss", "boss_14", 2)   # 奥の主役（千手の光輪は使わない。2026-10-07、人間の指示）
    rx, ry = (W - ring.width) // 2, 70
    put_glow(bg, ring, (255, 200, 90), 30, 1.6, rx, ry)
    bg.alpha_composite(ring, (rx, ry))
    # 前: 左に鬼神、右に光の獅子（2倍・少し暗くして奥行き）、手前の影
    oni = sprite(pack, "boss", "boss_15", 2)
    witch = sprite(pack, "boss", "boss_10", 2)
    put_glow(bg, oni, (255, 90, 30), 18, 1.2, -150, 300)
    bg.paste(darken(oni, 0.92), (-150, 300), darken(oni, 0.92))
    put_glow(bg, witch, (140, 110, 255), 18, 1.3, W - 400, 250)
    bg.paste(witch, (W - 400, 250), witch)
    # 火の粉
    sp = ImageDraw.Draw(bg)
    for _ in range(140):
        x, y = rnd.randrange(W), rnd.randrange(H)
        s = rnd.choice((2, 2, 2, 4))
        c = rnd.choice(((255, 196, 96, 220), (255, 120, 50, 200), (255, 236, 170, 230)))
        sp.rectangle((x - x % 2, y - y % 2, x - x % 2 + s - 1, y - y % 2 + s - 1), fill=c)
    # 下の帯（文字の土台）: 下から黒くなるグラデーション
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    for y in range(520, H):
        t = (y - 520) / (H - 520)
        bd.line([(0, y), (W, y)], fill=(4, 2, 6, int(235 * min(1, t * 1.6))))
    bg.alpha_composite(band)
    # 雑魚の列（2倍）を帯の上に
    row = ["mob_075", "mob_088", "mob_191"]
    for n, m in enumerate(row):
        im = sprite(pack, "mob", m, 2)
        x = 270 + n * 196
        put_glow(bg, im, (0, 0, 0), 6, 1.4, x + 6, 470 + 8)
        bg.alpha_composite(im, (x, 470))
    # 文字: 「224」を大きく、金の縦グラデーション＋黒いふち
    d = ImageDraw.Draw(bg)
    def gold_text(xy, s, f, stroke):
        mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).text(xy, s, font=f, fill=255)
        grad = Image.new("RGBA", (W, H))
        gd = ImageDraw.Draw(grad)
        bb = ImageDraw.Draw(mask).textbbox(xy, s, font=f)
        for y in range(bb[1], bb[3] + 1):
            t = (y - bb[1]) / max(1, bb[3] - bb[1])
            c = (int(255 - 40 * t), int(240 - 110 * t), int(170 - 140 * t), 255)
            gd.line([(bb[0], y), (bb[2], y)], fill=c)
        d.text(xy, s, font=f, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(20, 8, 4))
        bg.paste(grad, (0, 0), mask)
    f_big = font("NotoSerifCJK-Black.ttc", 150)
    f_ttl = font("NotoSerifCJK-Black.ttc", 66)
    s1, s2 = "224", "体"
    w1 = d.textlength(s1, font=f_big); w2 = d.textlength(s2, font=f_ttl)
    tl = d.textlength("モンスタードット絵", font=f_ttl)
    total = tl + 18 + w1 + 6 + w2
    x0 = (W - total) / 2
    gold_text((x0, 662), "モンスタードット絵", f_ttl, 6)
    gold_text((x0 + tl + 18, 590), s1, f_big, 8)
    gold_text((x0 + tl + 18 + w1 + 6, 662), s2, f_ttl, 6)
    sub = "雑魚 200体 ＋ ボス 24体 ／ 透明PNG・商用OK"
    f_sub = font("NotoSansCJK-Black.ttc", 28)
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 772), sub, font=f_sub, fill=(236, 230, 220), stroke_width=3, stroke_fill=(6, 4, 8))
    # 枠
    d.rectangle((6, 6, W - 7, H - 7), outline=(214, 170, 80), width=4)
    d.rectangle((16, 16, W - 17, H - 17), outline=(110, 80, 34), width=2)
    big = bg.convert("RGB")
    big.save(os.path.join(out, "サムネイル_1120x840.png"), optimize=True)
    big.resize((W // 2, H // 2), Image.BOX).save(os.path.join(out, "サムネイル_560x420.png"), optimize=True)
    print("→", out)


if __name__ == "__main__":
    main()
