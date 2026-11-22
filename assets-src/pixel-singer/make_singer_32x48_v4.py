"""もらった絵のキャラクター（赤い縦ロール）の歌い手 32×48・第3版。
お手本のドット絵を観察して決めたこと: 頭を小さめにして約3頭身／目は小さく、こい上まぶた＋白＋ひとみ色／かみは5〜6段の色を小さなかたまりで置く／
ふち取りは真っ黒一色にせず、かみはかみのいちばん暗い色でふち取る／服は小さな光の点で質感を出す。
頭と体は1ドットずつ手で打った表（ROWS）、縦ロールは巻きの形を計算で描く。"""
import json, sys
from PIL import Image
OUT = sys.argv[1]; W, H = 32, 48
C = {"#": "#0c0612", "1": "#4a0a1a", "2": "#7a1022", "3": "#b01c2a", "4": "#d93a38", "5": "#f47460", "6": "#ffbe9e",
     "a": "#fff0e2", "b": "#ffd9c0", "c": "#e0a080", "d": "#a85c4c", "p": "#ffb0a8",
     "e": "#0c3f4c", "f": "#22a8a4", "w": "#ffffff", "v": "#d8d2e2", "u": "#9a8fae",
     "n": "#0c1430", "N": "#1e2c58", "M": "#34508c", "L": "#6c8ccc", "k": "#181018", "K": "#362a3c", "J": "#5c4c64",
     "y": "#f0c040", "m": "#5a1018", "t": "#ff8a94"}
OY = 4
HEAD = ["......45......", ".....3..4..Nw.", "....345542.wNn", "..345665443Nwn", ".34566655443N2", "34566665544332", "34565543456432", "23454432345432",
        "23432c32c32321", "233c##cc##c221", "232bvebbevb221", "132bwfaafwc221", "122bpaaaapc221", "122cbaccabc121", ".21.cbbbbc.12.", ".1...dccd...1.",
        ".NMwvwvwvwvNn.", ".MLNN4324NNNn.", ".MMnMN33NNnNn.", ".MNnMNyNNNnNn.", ".MNnMNNNNNnNn.", ".vwnMNyNNnnwv.", ".bcwvwvwvwubc."]
RIB = {1: "wN", 2: "NwN", 3: "wN", 4: "N"}
LOW = {23: (10, "345433433221"), 24: (9, "34544334332211"), 25: (8, "3454433433433221"), 26: (8, "kKJKkKJKkKJKkKkk"),
       27: (7, "234543343343322211"), 28: (6, "23454334334334322211"), 29: (6, "12343223223223221111"), 30: (5, "kKJKkKJKkKJKkKJKkKJKkk"),
       31: (5, "vw.wv.wvw.vw.wvw.vw.wv"), 32: (12, "vuu..vuu"), 33: (12, "wvu..wvu"), 34: (12, "wvu..wvu"), 35: (12, "wvu..wvu"), 36: (12, "wvu..wvu"),
       37: (12, "wvu..wvu"), 38: (11, "KJKk..KJKk"), 39: (11, "kKkk..kKkk")}
LA = ["..35542..", ".3566432.", ".2454321.", "..23211.."]; LB = ["...35542.", "..3566432", "..2454321", "...23211."]
RA = ["..24432..", ".2455321.", ".1343211.", "..12211.."]; RB = [".24432...", "2455321..", "1343211..", ".12211..."]
LD = LA + LB + LA + LB + LA + ["...3542..", "..25431..", "...231...", "...342...", "....21...", "....1...."]
RD = RA + RB + RA + RB + RA + ["..2432...", "..14321..", "...121...", "...232...", "....11...", "....1...."]
MOUTH = {"closed": {}, "a": {12: (15, "mm"), 13: (14, "mttm")}, "i": {13: (14, "mwwm")}, "u": {13: (15, "mm")},
         "e": {13: (14, "mwwm"), 14: (15, "mm")}, "o": {12: (15, "mm"), 13: (15, "mm")}}
BLINK = {9: (13, "cccccc"), 10: (13, "bbbbbb"), 11: (13, "##aa##")}
def build(mouth, blink):
    g = [[None] * W for _ in range(H)]
    def stamp(tbl):
        for y, (x0, s) in tbl.items():
            for i, ch in enumerate(s):
                if ch != ".": g[y + OY][x0 + i] = ch
    stamp({6 + i: (0, r) for i, r in enumerate(LD)}); stamp({6 + i: (23, r) for i, r in enumerate(RD)})
    stamp({i: (9, r) for i, r in enumerate(HEAD)}); stamp({y: (23, r) for y, r in RIB.items()}); stamp(LOW); stamp(MOUTH[mouth])
    if blink: stamp(BLINK)
    add = []
    for y in range(H):
        for x in range(W):
            if g[y][x] is None:
                nb = [g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W and 0 <= y + dy < H and g[y + dy][x + dx]]
                if nb: add.append((x, y, "1" if all(c in "123456" for c in nb) and y < OY + 12 else "#"))
    for x, y, c in add: g[y][x] = c
    return g
FR = [("closed", False, 400), ("a", False, 200), ("i", False, 200), ("u", False, 200), ("e", False, 200), ("o", False, 200), ("closed", True, 150)]
grids = [build(m, b) for m, b, _ in FR]
used = sorted({c for g in grids for r in g for c in r if c})
SY = {c: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"[i] for i, c in enumerate(used)}   # エディタでは "." がすきまなので記号を付けかえる
cels = [["".join(SY[c] if c else "." for c in r) for r in g] for g in grids]
name = "縦ロールの歌い手_32x48_v4"
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
