"""大滝のまわりの海の渦潮（48×48・8コマ）。2026-10-05、人間の指示「その周りには渦潮」。
らせんの腕（白い泡のすじ）が、まん中へ向かって巻きこみながら回る。まん中は、深くくぼんだ暗い目。外のふちは海へ溶ける（ところどころ透かす）。
光は左上から（目の左上のふちが暗く、右下のふちが明るい＝くぼみ）。8コマで1回り（1コマ45°）。
出力: whirl-0..7.txt / pal-whirl-*.json と、src/assets/falls/whirl.png（横に8コマ）。"""
import json
import math
import os

from PIL import Image

from basin import PAL, hsh, mix, nearest, vnoise, water

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
S = 48
FR = 8


def pixel(x, y, fr):
    px, py = x + 0.5 - S / 2, y + 0.5 - S / 2
    r = math.hypot(px, py)
    R = S / 2 - 1
    if r > R:
        return None
    out = r / R
    if out > 0.8 and hsh(x, y, 21 + fr) < (out - 0.8) / 0.2:
        return None
    th = math.atan2(py, px)
    spin = fr * (2 * math.pi / FR) / 2           # 2本の腕なので、半回りで元の形＝8コマで1周に見える
    arm = math.sin(2 * (th + spin) + math.log(r + 1.5) * 4.2)   # 対数らせん
    rough = vnoise(th * 8 + fr * 0.0, r, 3, 22) - 0.5
    if r < 3.2:
        return PAL["a"] if r < 2 else PAL["b"]      # 渦の目（深い）
    if r < 6.5:
        # 目のまわりのくぼみ: 左上が暗く、右下が明るい
        lit = (px + py) / r
        v = 0.15 + lit * 0.18 + (1 - r / 6.5) * -0.1
        if arm > 0.6:
            return PAL["h"]
        return water(v)
    v = 0.4 + arm * 0.18 + rough * 0.25 - out * 0.1
    foam = arm * 0.75 + rough * 0.6 - out * 0.5 + 0.1
    if foam > 0.72:
        return PAL["k"] if foam > 0.95 else PAL["j"]
    if foam > 0.5:
        return PAL["i"]
    return water(v)


if __name__ == "__main__":
    sheet = Image.new("RGBA", (S * FR, S), (0, 0, 0, 0))
    for fr in range(FR):
        rows = []
        for y in range(S):
            line = ""
            for x in range(S):
                rgb = pixel(x, y, fr)
                line += "." if rgb is None else nearest(rgb)
            rows.append(line)
        used = sorted(set("".join(rows)) - {"."})
        with open(os.path.join(HERE, f"whirl-{fr}.txt"), "w") as f:
            f.write("\n".join(rows) + "\n")
        with open(os.path.join(HERE, f"pal-whirl-{fr}.json"), "w") as f:
            json.dump({k: "#%02x%02x%02x" % PAL[k] for k in used}, f)
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch != ".":
                    sheet.putpixel((fr * S + x, y), PAL[ch] + (255,))
    sheet.save(os.path.join(OUT, "whirl.png"))
    print("ok")
