"""全身が必ず絵に入るようにするための「置き場所の下書き」（2026-10-04、人間の指示「全身が入るように」）。

AIに文字だけで頼むと、体が端で切れたアップの絵になりやすい（神・悪魔・キメラなどの最初の下絵は、15枚中14枚が切れていた）。
そこで、白い背景のまん中に、ぼかした影絵（体のおおまかな形・色・左上からの光）を置いた絵を作り、それを元に
画像生成AIに描かせる（img2img。generate.py の "layout"）。AIは影絵の位置と大きさを守るので、まわりに余白が残り、全身が入る。

形（shape）:
  ground  4本足で地面に立つ獣・虫（頭は右）
  float   宙に浮かぶもの（霊・目玉・くらげ）
  tall    2本足で立つもの（人型・鎧・木の怪物・悪魔）
  long    低く長いもの（蛇・ミミズ・とかげ・ワニ）
  winged  羽を広げたもの（鳥・こうもり・竜・羽虫）
  big     大きなかたまり（ゴーレム・機械・ボスの巨体。絵の7割ほど）
色（tone）: 体のおおまかな色 [r,g,b]。暗すぎ・鮮やかすぎにしない（AIがその色をそのまま平らに塗ってしまう）。
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BG = (244, 242, 238)
SHAPES = ("ground", "float", "tall", "long", "winged", "big", "ring")


def _mask(shape, rng):
    m = Image.new("L", (512, 512), 0)
    d = ImageDraw.Draw(m)
    j = lambda v: v + int(rng.integers(-12, 13))  # 毎回少しずつ形を変える
    if shape == "ground":
        d.ellipse((j(140), j(200), j(360), j(350)), 255)            # 胴
        d.ellipse((j(305), j(150), j(400), j(250)), 255)            # 頭（右）
        for x in (170, 215, 280, 320):
            d.rectangle((j(x), 320, j(x) + 24, j(395)), 255)       # 足
        d.polygon([(150, 260), (95, 300), (110, 320), (160, 300)], 255)  # しっぽ
    elif shape == "float":   # 浮く: 丸い板・顔・コインになりやすかったので、体＋左右のふくらみ＋下へ細くなる尾にする（2026-10-05）
        d.ellipse((j(180), j(120), j(350), j(285)), 255)
        d.ellipse((j(130), j(185), j(210), j(250)), 255); d.ellipse((j(320), j(175), j(395), j(240)), 255)
        sw = int(rng.integers(-40, 41))
        d.polygon([(200, 250), (330, 250), (j(290) + sw, 350), (j(250) + sw * 2, 420), (j(240) + sw, 340)], 255)
    elif shape == "tall":
        d.ellipse((j(215), j(70), j(305), j(165)), 255)             # 頭
        d.rounded_rectangle((j(185), 150, j(335), j(330)), 40, 255) # 胴
        d.rectangle((j(150), 170, j(185), j(300)), 255); d.rectangle((j(328), 170, j(368), j(300)), 255)  # 腕
        for x in (200, 275):
            d.rectangle((j(x), 320, j(x) + 42, j(435)), 255)       # 足
    elif shape == "long":   # 細長い: 細く平らな絵になりやすかったので、太い体の前を持ち上げ、脚をつける（2026-10-05）
        pts = [(90, 340), (160, 320), (240, 330), (310, 300), (360, 240), (390, 190)]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            d.line((j(x0), j(y0), j(x1), j(y1)), 255, width=84)
        d.ellipse((j(350), j(130), j(450), j(225)), 255)            # 頭（右上）
        for x in (130, 190, 250, 300):
            d.line((x, 350, x - 15, j(410)), 255, width=14)          # 脚
    elif shape == "winged":
        d.ellipse((j(205), j(200), j(325), j(330)), 255)            # 胴
        d.ellipse((j(300), j(160), j(370), j(230)), 255)            # 頭（右）
        d.polygon([(250, 230), (j(80), j(110)), (j(120), j(250)), (240, 290)], 255)    # 羽
        d.polygon([(290, 230), (j(430), j(100)), (j(410), j(240)), (300, 290)], 255)
        d.rectangle((j(235), 320, j(255), j(380)), 255); d.rectangle((j(280), 320, j(300), j(380)), 255)
    elif shape == "big":
        d.rounded_rectangle((j(120), j(130), j(395), j(395)), 70, 255)
        d.ellipse((j(305), j(90), j(415), j(200)), 255)
        for x in (145, 315):
            d.rectangle((j(x), 380, j(x) + 55, j(445)), 255)
    elif shape == "ring":   # 浮かぶ輪（全環など）。輪の真ん中に丸い芯（目）
        r0 = 170 + int(rng.integers(-8, 9)); r1 = r0 - 46
        d.ellipse((256 - r0, 250 - r0, 256 + r0, 250 + r0), 255); d.ellipse((256 - r1, 250 - r1, 256 + r1, 250 + r1), 0)
        d.ellipse((j(216), j(210), j(296), j(290)), 255)
    else:
        raise ValueError(f"形は {SHAPES} のどれか: {shape}")
    return m


def make_layout(shape="ground", tone=(110, 100, 95), seed=0):
    """白い背景＋左上から光の当たった、ぼかした影絵（512×512 RGB）"""
    rng = np.random.default_rng(seed)
    m = _mask(shape, rng)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(5))).astype(np.float32)[:, :, None] / 255
    yy, xx = np.mgrid[0:512, 0:512].astype(np.float32)
    light = 1.18 - 0.55 * ((xx + yy) / 1024)                          # 左上が明るく、右下が暗い
    body = np.clip(np.asarray(tone, np.float32)[None, None, :] * light[:, :, None], 0, 255)
    body += rng.normal(0, 16, body.shape)                              # 少しざらつかせる（平らな塗りを防ぐ）
    bg = np.asarray(BG, np.float32)[None, None, :] * np.ones((512, 512, 1), np.float32)
    shadow = np.zeros((512, 512), np.float32)
    ys = np.nonzero(np.asarray(m))[0]
    if len(ys) and shape not in ("float", "ring"):
        bottom = ys.max()
        shadow = np.exp(-(((yy - bottom) / 10) ** 2) - (((xx - 256) / 150) ** 2)) * 0.18
    elif len(ys):
        shadow = np.exp(-(((yy - 430) / 8) ** 2) - (((xx - 256) / 90) ** 2)) * 0.12
    bg = bg * (1 - shadow[:, :, None])
    out = bg * (1 - a) + body * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))


if __name__ == "__main__":
    import sys
    tiles = [make_layout(s, seed=1).resize((200, 200)) for s in SHAPES]
    sheet = Image.new("RGB", (200 * len(tiles), 200), "white")
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * 200, 0))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else "layouts.png")
    print("形の見本:", ", ".join(SHAPES))
