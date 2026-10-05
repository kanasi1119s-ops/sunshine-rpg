"""芯環塔のまわりの大滝のドット絵（2026-10-05、人間の指示「滝は特別なドット絵でリアルな感じで仕上げて」「ドット絵はすべてこだわって」）。
- curtain-0..3（16×96）: 崖を流れ落ちる水のカーテン。上は落ち口の白い泡、たてに何本もの水の帯（帯ごとに明るさがちがい、帯の境は暗い）、
  帯の上を白い筋が下へ流れる（1コマ6ドット、4コマで1周）。下は水しぶきと霧になって消える。
- surface-0..3（16×16）: ふちの上を、落ち口（下）へ走る水面。流れの筋が下へ動き、下のはしは落ち口の白い泡。向きは描くときに回す。
1文字=1色、'.'=透明。tools/pixel-practice/editor-draw.mjs で1コマずつ確かめ、src/assets/falls/*.png（横に4コマ）に書き出す。"""
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
PAL = {
    "A": "#163a66",  # 深い水（帯の境・影）
    "B": "#245a92",  # 水（暗）
    "C": "#3a7cb8",  # 水
    "D": "#62a2d8",  # 水（明）
    "E": "#9cccf0",  # 水（光）
    "F": "#d4ecfc",  # 泡
    "G": "#ffffff",  # いちばん白い泡・光
    "H": "#b8c8dc",  # 霧（明）
    "I": "#8494ae",  # 霧（暗）
}


def hsh(x, y, k=0):
    h = (x * 374761393 + y * 668265263 + k * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFFFF) / 4294967296


# 水の帯（左から: はば・明るさ）。はしの帯は暗く、まん中が明るい（落ちる水の厚み）
RIBBONS = [(2, "B"), (3, "C"), (2, "D"), (3, "E"), (2, "D"), (2, "C"), (2, "B")]
P = 24          # 白い筋のくり返しの長さ（1コマ6ドットで4コマ＝1周）


def curtain(frame):
    W, H = 16, 96
    g = [["."] * W for _ in range(H)]
    x0 = 0
    for ri, (w, tone) in enumerate(RIBBONS):
        for dx in range(w):
            x = x0 + dx
            for y in range(H):
                c = tone
                if dx == 0 and ri > 0:
                    c = "A" if tone in "BC" else "B"                       # 帯の境の影
                # 白い筋（帯ごとに2本、長さ4〜8。下へ流れる）
                for k in range(2):
                    start = (int(hsh(ri, k, 1) * P) + frame * 6) % P
                    ln = 4 + int(hsh(ri, k, 2) * 5)
                    yy = (y - start) % P
                    if yy < ln and dx > 0:
                        c = "G" if (yy < 2 and tone in "DE") else ("F" if tone in "DE" else "E")
                g[y][x] = c
        x0 += w
    # 落ち口（上の3行）: ふくらんだ白い泡のふち
    for x in range(W):
        g[0][x] = "F" if x % 5 else "E"
        g[1][x] = "G" if (x + frame) % 3 else "F"
        g[2][x] = "F" if (x + frame * 2) % 4 else "E"
    # 下: 水の帯がほどけて細い糸になり（1列おき）、白い水しぶきの雲に消える
    x0 = 0
    ends = []
    for ri, (w, tone) in enumerate(RIBBONS):
        end = 64 + int(hsh(ri, 5, 9) * 12) + (frame + ri) % 2      # 帯ごとに、ほどける高さがちがう
        for dx in range(w):
            x = x0 + dx
            for y in range(end - 3, H):
                if y >= end or (y >= end - 3 and dx not in (w // 2,)):
                    g[y][x] = "."                                    # ほどける手前は、帯のまん中の1本の糸だけ
        x0 += w
    # 水しぶきの雲（横いっぱいの、ふくらんだ1つのかたまり。上が明るく、下が暗い。少しずつふくらんで、ゆれる）
    puffs = [(2 + frame % 2, 80, 4.2), (7, 78 - frame % 2, 4.8), (12 - frame % 2, 80, 4.4), (4, 86, 4.0), (10, 85 + frame % 2, 4.2), (7, 90, 3.2)]
    for y in range(70, H):
        for x in range(W):
            best = None
            for (cx, cy, rr) in puffs:
                d = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5 / rr
                if d <= 1 and (best is None or d < best[0]):
                    best = (d, cx, cy)
            if best is None:
                continue
            d, cx, cy = best
            lit = (y + 0.5 - cy) < -0.5 and d < 0.85
            g[y][x] = "G" if lit and d < 0.45 else ("F" if lit else ("H" if d < 0.8 else "I"))
    # 雲の中にぽつんと残った暗い点は、まわりの色に（ちらつく1ドットをなくす）
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if g[y][x] == "I" and all(g[y + dy][x + dx] not in ("I", ".") for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = "H"
    return g


def surface(frame):
    W, H = 16, 16
    g = [["C"] * W for _ in range(H)]
    for x in range(W):
        for y in range(H):
            # 流れの筋（たて長の明るい線が下へ動く）
            lane = x // 3
            start = (int(hsh(lane, 1, 11) * 16) + frame * 4) % 16
            ln = 3 + int(hsh(lane, 2, 11) * 4)
            yy = (y - start) % 16
            c = "C" if (x + lane) % 3 else "B"
            if yy < ln and x % 3 != 0:
                c = "E" if yy < 1 else "D"
            g[y][x] = c
    # 下のはし: 落ち口の泡（ふちを越える水）
    for x in range(W):
        g[13][x] = "E" if (x + frame) % 3 else "D"
        g[14][x] = "F" if (x + frame) % 4 else "G"
        g[15][x] = "G" if (x * 3 + frame) % 5 else "F"
    return g


def save(name, g):
    rows = ["".join(r) for r in g]
    used = sorted(set("".join(rows)) - {"."})
    with open(os.path.join(HERE, f"{name}.txt"), "w") as f:
        f.write("\n".join(rows) + "\n")
    with open(os.path.join(HERE, f"pal-{name}.json"), "w") as f:
        json.dump({k: PAL[k] for k in used}, f)
    return rows


def sheet(name, frames, w, h):
    im = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    for i, rows in enumerate(frames):
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c in PAL:
                    v = PAL[c]
                    im.putpixel((i * w + x, y), (int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16), 255))
    os.makedirs(OUT, exist_ok=True)
    im.save(os.path.join(OUT, f"{name}.png"))


if __name__ == "__main__":
    cs = [save(f"curtain-{k}", curtain(k)) for k in range(4)]
    ss = [save(f"surface-{k}", surface(k)) for k in range(4)]
    sheet("curtain", cs, 16, 96)
    sheet("surface", ss, 16, 16)
    print("ok")
