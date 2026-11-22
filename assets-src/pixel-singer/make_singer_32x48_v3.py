"""もらった絵のキャラクター（赤い縦ロール）の歌い手 32×48・第3版。
お手本のドット絵を観察して決めたこと: 頭を小さめにして約3頭身／目は小さく、こい上まぶた＋白＋ひとみ色／かみは5〜6段の色を小さなかたまりで置く／
ふち取りは真っ黒一色にせず、かみはかみのいちばん暗い色でふち取る／服は小さな光の点で質感を出す。
頭と体は1ドットずつ手で打った表（ROWS）、縦ロールは巻きの形を計算で描く。"""
import json, sys
from PIL import Image
OUT = sys.argv[1]; W, H = 32, 48
C = {"#": "#120a14", "1": "#5a0a1c", "2": "#8f1024", "3": "#c21a2a", "4": "#e83a3c", "5": "#ff7a6e", "6": "#ffc0b0",
     "a": "#fff0e2", "b": "#ffd9c0", "c": "#e8a886", "d": "#b86a58", "p": "#ffb0a8",
     "e": "#0c3f4c", "f": "#1b9c9c", "g": "#6fe8d8", "w": "#ffffff", "v": "#dcd6e6", "u": "#a79cb8",
     "n": "#101a36", "N": "#223260", "M": "#3a5494", "L": "#6f8fd0", "k": "#1c1420", "K": "#3a2c40", "J": "#5e4c66",
     "y": "#f0c040", "m": "#6a1420", "t": "#ff8a94"}
ROWS = {  # 行番号: (始まりの列, ドット)。"." はすきま
 0: (15, "45"), 1: (14, "3..4"), 2: (16, "32...Nw.wN"),
 3: (12, "34554332NwNnNwN"), 4: (10, "3456655443wNwnwNw"), 5: (9, "345666554433Nw2wN"),
 6: (8, "3456665456654332"), 7: (8, "2345654345654322"), 8: (8, "2344543234543321"), 9: (8, "2334432123443221"),
 10: (8, "23432c32cc32c321"), 11: (8, "233c###ab###c321"), 12: (8, "232#weeabeew#231"), 13: (8, "132bffeabeffc221"),
 14: (8, "122bggfaafggc221"), 15: (8, ".21bppaaaappc12."), 16: (8, ".21cbaaddabbc12."), 17: (8, ".1..cbbbbbcc..1."),
 18: (8, ".....cccccd....."), 19: (8, "......dccd......"),
 20: (8, ".NMMwvwvwvwvNNn."), 21: (8, "NMLMNN43243NNNNn"), 22: (8, "NMMnMNN33NNNnNNn"), 23: (8, "NMNnMNNyNNNNnNNn"),
 24: (8, "NMNnMNNNNNNnnNNn"), 25: (8, "vwvnMNNyNNNnnvwv"), 26: (8, ".bcwvwvwvwvwubc."),
 27: (10, "345443343322"), 28: (9, "34544334332221"), 29: (8, "3454433433433221"), 30: (7, "345443343343322211"),
 31: (7, "kKJKkKJKkKJKkKJKkk"), 32: (7, "234543343343322211"), 33: (6, "23454334334334322211"), 34: (6, "23454334334334322211"),
 35: (5, "kKJKkKJKkKJKkKJKkKJKkk"), 36: (5, "wvw.wvw.wvw.wvw.wvw.wv"),
 37: (12, "vuu..vuu"), 38: (12, "wvu..wvu"), 39: (12, "wvu..wvu"), 40: (12, "wvu..wvu"), 41: (12, "wvu..wvu"), 42: (12, "wvu..wvu"),
 43: (11, "KJKk..KJKk"), 44: (11, "kKkk..kKkk")}
MOUTH = {"closed": {}, "a": {15: (15, "mm"), 16: (14, "mttm"), 17: (15, "mm")}, "i": {16: (14, "mwwm")}, "u": {16: (15, "mm")},
         "e": {16: (14, "mwwm"), 17: (15, "tt")}, "o": {15: (15, "mm"), 16: (15, "mm"), 17: (15, "mm")}}
BLINK = {11: (11, "cbbbabbbbc"), 12: (11, "bbbbabbbbb"), 13: (11, "####ab####"), 14: (11, "bbbbaabbbc")}
def build(mouth, blink):
    g = [[None] * W for _ in range(H)]
    # 縦ロール: ななめの暗い線で区切った帯を、上から 明→中→暗 とぬる
    for cx, mir in ((4, False), (27, True)):
        for y in range(8, 39):
            k = (y - 8) // 4; hw = 2 if k <= 5 else 1 if k == 6 else 0
            if y == 8: hw = 1
            if y == 38: hw = 0
            for x in range(cx - hw, cx + hw + 1):
                r = x - (cx - hw); r = (2 * hw - r) if mir else r; r7 = r if hw == 3 else r + (3 - hw)
                line = 3 - min(r7, 5) // 2 if r7 < 6 else 0
                d = (y - 8 - line) % 4; tone = (2, 5, 4, 3)[d]
                if r in (0, 2 * hw) and hw: tone = max(1, tone - 1)
                if d == 1 and r7 in (2, 3) and not mir: tone = 6
                if mir and d >= 2: tone = max(2, tone - 1)
                g[y][x] = str(tone)
    def stamp(tbl):
        for y, (x0, s) in tbl.items():
            for i, ch in enumerate(s):
                if ch != ".": g[y][x0 + i] = ch
    stamp(ROWS); stamp(MOUTH[mouth])
    if blink: stamp(BLINK)
    # ふち取り: かみのとなりはかみの暗い色、ほかは黒に近い色
    add = []
    for y in range(H):
        for x in range(W):
            if g[y][x] is None:
                nb = [g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W and 0 <= y + dy < H and g[y + dy][x + dx]]
                if nb: add.append((x, y, "1" if all(c in "23456" for c in nb) and y < 30 else "#"))
    for x, y, c in add: g[y][x] = c
    return g
FR = [("closed", False, 400), ("a", False, 200), ("i", False, 200), ("u", False, 200), ("e", False, 200), ("o", False, 200), ("closed", True, 150)]
grids = [build(m, b) for m, b, _ in FR]
used = sorted({c for g in grids for r in g for c in r if c})
SY = {c: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"[i] for i, c in enumerate(used)}   # エディタでは "." がすきまなので記号を付けかえる
cels = [["".join(SY[c] if c else "." for c in r) for r in g] for g in grids]
name = "縦ロールの歌い手_32x48_v3"
json.dump({"format": "sunshine-pixel", "version": 2, "width": W, "height": H, "symbols": [{"sym": SY[c], "label": "色", "color": C[c]} for c in used],
           "layers": [{"name": "歌い手", "visible": True, "opacity": 1}], "frames": [{"dur": d} for *_, d in FR], "cels": [cels], "layer": 0, "frame": 0},
          open(f"{OUT}/{name}.sunshine-pixel.json", "w", encoding="utf-8"), ensure_ascii=False)
def img(g, z):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            if g[y][x]: h = C[g[y][x]]; im.putpixel((x, y), (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255))
    return im.resize((W * z, H * z), Image.NEAREST)
z = 10; BG = (104, 100, 92, 255); sheet = Image.new("RGBA", (W * z * 7, H * z), BG); raw = Image.new("RGBA", (W * 7, H), (0, 0, 0, 0)); fs = []
for i, g in enumerate(grids):
    sheet.alpha_composite(img(g, z), (i * W * z, 0)); raw.alpha_composite(img(g, 1), (i * W, 0))
    f = Image.new("RGBA", (W * z, H * z), BG); f.alpha_composite(img(g, z)); fs.append(f.convert("P", palette=Image.ADAPTIVE))
sheet.save(f"{OUT}/{name}_確認用（口の形7コマ）.png"); raw.save(f"{OUT}/{name}_シート（等倍・透明）.png")
seq = [0, 1, 0, 3, 5, 1, 2, 4, 1, 0, 6, 0, 5, 3, 1, 0]
fs[0].save(f"{OUT}/{name}_歌っている見本.gif", save_all=True, append_images=[fs[i] for i in seq[1:]], duration=[120 if i == 6 else 180 for i in seq], loop=0)
print(len(used), "色")
