"""販売ページ用の紹介画像（10枚・JPEG）を作る（2026-10-07、人間の指示「画像を10枚ほどピックアップして、紹介で使うから売り文句も2枚ぐらいにつけて」）。
DLsite の推奨形式に合わせて JPEG（1280×960）。絵は販売用パック（build_monster_pack.py の出力）の 1倍の PNG を、整数倍で拡大して置く（にじみ無し）。
使い方: python3 tools/sales/make_promo.py パックのフォルダ 出力フォルダ
"""
import os, sys, csv
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FD = "/usr/share/fonts/opentype/noto/"
SERIF = FD + "NotoSerifCJK-Black.ttc"
SANS_B = FD + "NotoSansCJK-Bold.ttc"
SANS_BL = FD + "NotoSansCJK-Black.ttc"
W, H = 1280, 960
GOLD = (246, 214, 128); WHITE = (244, 242, 236); DIM = (176, 170, 190)


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def backdrop(top=(28, 22, 44), bottom=(10, 8, 18), glow=None):
    """暗い縦グラデーション＋まん中の淡い光"""
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    if glow:
        g = Image.new("L", (W, H), 0)
        ImageDraw.Draw(g).ellipse((W / 2 - 420, H / 2 - 360, W / 2 + 420, H / 2 + 300), fill=120)
        g = g.filter(ImageFilter.GaussianBlur(120))
        bg = Image.composite(Image.new("RGB", (W, H), glow), bg, g)
    return bg


def sprite(pack, kind, no, k):
    sub = "雑魚_96px" if kind == "mob" else "ボス_256px"
    im = Image.open(os.path.join(pack, sub, "1倍", f"{no}.png")).convert("RGBA")
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def shadow_paste(bg, im, x, y):
    """足もとに薄い影を落として貼る"""
    a = im.split()[3]
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: 90 if v else 0))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    bg.paste(sh, (x + 6, y + 10), sh)
    bg.paste(im, (x, y), im)


def text_c(d, xy, s, f, fill, stroke=0, stroke_fill=(0, 0, 0)):
    w = d.textlength(s, font=f)
    d.text((xy[0] - w / 2, xy[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def frame(d):
    d.rectangle((14, 14, W - 15, H - 15), outline=(120, 96, 52), width=2)
    d.rectangle((22, 22, W - 23, H - 23), outline=(70, 56, 34), width=1)


def names(pack):
    with open(os.path.join(pack, "一覧.csv"), encoding="utf-8-sig") as fp:
        return {r["番号"]: r["参考名"] for r in csv.DictReader(fp)}


def label(d, x, y, no, name, w):
    f1 = font(SANS_B, 15); f2 = font(SANS_B, 20)
    text_c(d, (x + w / 2, y), no, f1, DIM)
    text_c(d, (x + w / 2, y + 20), name, f2, WHITE)


def main():
    pack, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    N = names(pack)
    files = []

    # 01 売り文句つき（メイン）: 千手の光輪を中央に、左右にボス、下に雑魚の列
    bg = backdrop(glow=(70, 52, 30)); d = ImageDraw.Draw(bg)
    shadow_paste(bg, sprite(pack, "boss", "boss_13", 1), 40, 300)
    shadow_paste(bg, sprite(pack, "boss", "boss_15", 1), W - 296, 300)
    shadow_paste(bg, sprite(pack, "boss", "boss_24", 2), (W - 512) // 2, 190)
    row = ["mob_019", "mob_075", "mob_040", "mob_121", "mob_028", "mob_088", "mob_171", "mob_191", "mob_137", "mob_001"]
    for n, m in enumerate(row):
        shadow_paste(bg, sprite(pack, "mob", m, 1), 24 + n * 124, 760)
    text_c(d, (W / 2, 40), "敵キャラ、まるごと224体。", font(SERIF, 72), GOLD, 4, (30, 18, 8))
    text_c(d, (W / 2, 132), "雑魚200体 ＋ ボス24体　RPGモンスタードット絵パック", font(SANS_BL, 30), WHITE, 3, (10, 8, 16))
    text_c(d, (W / 2, 906), "※画像生成AIの下絵をもとに、ドット絵に変換・手直しして仕上げた作品です（AI生成作品）", font(SANS_B, 17), DIM)
    frame(d); files.append(("01_メイン.jpg", bg))

    # 02 売り文句つき（使いやすさ）: 戦闘画面のイメージ＋仕様
    bg = backdrop(top=(36, 52, 70), bottom=(14, 20, 30)); d = ImageDraw.Draw(bg)
    d.rectangle((60, 470, W - 60, 478), fill=(60, 80, 96))  # 地面の線
    for n, m in enumerate(["mob_023", "mob_016", "mob_123"]):
        shadow_paste(bg, sprite(pack, "mob", m, 2), 200 + n * 300, 280)
    text_c(d, (W / 2, 50), "戦闘画面に、そのまま置ける。", font(SERIF, 66), GOLD, 4, (12, 16, 24))
    d.text((150, 175), "雑魚は 96×96（2倍で192×192）。上の3体はゲーム画面に並べたイメージです。", font=font(SANS_B, 22), fill=DIM)
    bullets = ["背景が透明な PNG", "等倍・2倍・4倍を同梱（拡大はにじみ無し）", "雑魚 96×96・26色以内 ／ ボス 256×256・62色以内",
               "全部 右向きの1枚絵（左右反転して左向きにも）", "商用OK・加工OK・クレジット表記不要", "番号つき一覧（CSV・PDF）つき"]
    for n, b in enumerate(bullets):
        y = 540 + n * 58
        d.ellipse((150, y + 12, 166, y + 28), fill=GOLD)
        d.text((184, y), b, font=font(SANS_BL, 32), fill=WHITE)
    frame(d); files.append(("02_使いやすさ.jpg", bg))

    # 03〜06 ボス2体ずつ（2倍）
    pairs = [("boss_13", "boss_10"), ("boss_15", "boss_21"), ("boss_03", "boss_11"), ("boss_16", "boss_14")]
    for k, (a, b) in enumerate(pairs):
        bg = backdrop(glow=(46, 36, 70)); d = ImageDraw.Draw(bg)
        text_c(d, (W / 2, 40), "ボス 256×256（2倍で表示）", font(SANS_BL, 30), GOLD)
        for n, no in enumerate((a, b)):
            x = 96 + n * 576
            shadow_paste(bg, sprite(pack, "boss", no, 2), x, 110)
            label(d, x, 650, no, N[no], 512)
        frame(d); files.append((f"{k + 3:02d}_ボス_{N[a]}・{N[b]}.jpg", bg))

    # 07 千手の光輪（3倍）
    bg = backdrop(glow=(80, 60, 26)); d = ImageDraw.Draw(bg)
    shadow_paste(bg, sprite(pack, "boss", "boss_24", 3), (W - 768) // 2, 60)
    label(d, 0, 846, "boss_24", N["boss_24"], W)
    frame(d); files.append(("07_ボス_千手の光輪.jpg", bg))

    # 08〜10 雑魚（2倍・15体ずつ、テーマ別）
    themes = [("獣・虫", ["mob_001", "mob_016", "mob_019", "mob_021", "mob_023", "mob_075", "mob_121", "mob_123", "mob_140", "mob_153", "mob_170", "mob_171", "mob_179", "mob_183", "mob_013"]),
              ("精霊・結晶", ["mob_007", "mob_028", "mob_040", "mob_054", "mob_064", "mob_073", "mob_092", "mob_107", "mob_111", "mob_124", "mob_126", "mob_154", "mob_173", "mob_180", "mob_191"]),
              ("機械・亡霊", ["mob_022", "mob_039", "mob_044", "mob_049", "mob_055", "mob_063", "mob_076", "mob_088", "mob_117", "mob_131", "mob_137", "mob_150", "mob_177", "mob_184", "mob_196"])]
    for k, (title, ids) in enumerate(themes):
        bg = backdrop(); d = ImageDraw.Draw(bg)
        text_c(d, (W / 2, 32), f"雑魚 96×96（2倍で表示）　{title}", font(SANS_BL, 30), GOLD)
        for n, no in enumerate(ids):
            cx = 40 + (n % 5) * 240; cy = 92 + (n // 5) * 284
            shadow_paste(bg, sprite(pack, "mob", no, 2), cx + 24, cy)
            label(d, cx, cy + 198, no, N[no], 240)
        frame(d); files.append((f"{k + 8:02d}_雑魚_{title}.jpg", bg))

    # 11 まとめた小さい画像（PNG・560×420。一覧・サムネイル用。2026-10-07、人間の指示「まとめた小さい画像をPNGで」）
    SW, SH = 560, 420
    sm = backdrop(glow=(70, 52, 30)).resize((SW, SH), Image.LANCZOS); d = ImageDraw.Draw(sm)
    sm.paste(sprite(pack, "boss", "boss_24", 1), ((SW - 256) // 2, 82), sprite(pack, "boss", "boss_24", 1))
    for n, m in enumerate(["mob_075", "mob_019"]):
        im = sprite(pack, "mob", m, 1); sm.paste(im, (14, 96 + n * 112), im)
    for n, m in enumerate(["mob_040", "mob_179"]):
        im = sprite(pack, "mob", m, 1); sm.paste(im, (SW - 110, 96 + n * 112), im)
    text_c(d, (SW / 2, 12), "モンスタードット絵 224体", font(SERIF, 36), GOLD, 2, (30, 18, 8))
    text_c(d, (SW / 2, 352), "雑魚200体 ＋ ボス24体", font(SANS_BL, 24), WHITE, 2, (10, 8, 16))
    text_c(d, (SW / 2, 386), "透明PNG ・ 等倍/2倍/4倍 ・ 商用OK", font(SANS_B, 16), DIM)
    d.rectangle((4, 4, SW - 5, SH - 5), outline=(120, 96, 52), width=2)
    sm.save(os.path.join(out, "11_まとめ_560x420.png"), optimize=True)

    for name, im in files:
        im.save(os.path.join(out, name), quality=94)
    print(len(files), "枚 →", out)


if __name__ == "__main__":
    main()
