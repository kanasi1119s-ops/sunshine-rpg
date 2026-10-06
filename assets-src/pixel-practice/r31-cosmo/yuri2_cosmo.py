"""試し: 2頭身のユーリ（16×32、左向き＝戦闘の向き）が「コスモリングライト」をまとった絵（2026-10-06、人間の依頼）。
白と金の鎧・胸の環の核・光る籠手・背の光の環・背から流れる羽の板・まわりに浮かぶ6基の追尾砲台（砲口は敵のいる左）。
既存作のロボットのデザイン（V字の角・青い刃の翼・赤青白の配色など）はまねしない（CLAUDE.md 1-1）。
頭（髪・顔）は assets-src/characters/walk-2head/ユーリ.json の left0 をそのまま使う。光は左上。"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "characters", "walk-2head")
src = json.load(open(os.path.join(ROOT, "ユーリ.json"), encoding="utf-8"))
LET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
pal = {LET[i]: c for i, c in enumerate(src["palette"])}
NEW = {
    "1": "#f6f8fc", "2": "#d2d9e6", "3": "#9ca6bc", "4": "#5a6480",     # 鎧（明→暗）
    "5": "#ffe27a", "6": "#d8a030", "7": "#8a5a14",                     # 金
    "8": "#7ae4ff", "9": "#2aa8e0", "0": "#16588c", "v": "#ffffff",     # 光（核・砲口）
    "r": "#3a7cc0",                                                      # 光の環（奥の暗い側）
}
pal.update(NEW)
W, H, OX, OY = 40, 40, 12, 5
G = [["."] * W for _ in range(H)]
def put(x, y, c):
    if 0 <= x < W and 0 <= y < H: G[y][x] = c
def outline(mask_chars):
    pts = [(x, y) for y in range(H) for x in range(W) if G[y][x] in mask_chars]
    for x, y in pts:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x+dx < W and 0 <= y+dy < H and G[y+dy][x+dx] == ".": G[y+dy][x+dx] = "A"

# 1) 背の光の環（いちばん奥）。左上が明るく、右下は暗い。6つの金の節
RCX, RCY, RR = 21.5, 20.5, 10.5
for y in range(H):
    for x in range(W):
        d = math.hypot(x+.5-RCX, y+.5-RCY)
        if abs(d-RR) < 0.62:
            a = math.atan2(y+.5-RCY, x+.5-RCX)
            put(x, y, "8" if math.cos(a+2.35) > 0.35 else ("9" if math.cos(a+2.35) > -0.5 else "r"))
for k in range(6):
    a = k*math.pi/3 + math.pi/6
    x, y = int(RCX+RR*math.cos(a)), int(RCY+RR*math.sin(a))
    put(x, y, "5")

# 2) 羽の板（背＝右側から、右へ流れる3枚。上の板ほど明るい）
ROOTX, ROOTY = 24, 24
for i, (deg, ln) in enumerate(((-52, 10), (-14, 12), (24, 9))):
    a = math.radians(deg); ux, uy = math.cos(a), math.sin(a); px, py = -uy, ux
    body = "2" if i < 2 else "3"
    for t in range(ln):
        w = 1.0 if t < ln-4 else 1.0*(ln-t)/4
        x, y = ROOTX+ux*t, ROOTY+uy*t
        for s in (-1, 0, 1):
            if abs(s) <= w: put(int(round(x+px*s*0.9)), int(round(y+py*s*0.9)), body)
        put(int(round(x-px*0.9)), int(round(y-py*0.9)), "1" if i < 2 else "2")     # 上のふち（光）
        if t % 3 == 1 and 2 < t < ln-2: put(int(round(x)), int(round(y)), "8")      # 光のすじ
    put(int(round(ROOTX+ux*(ln-1))), int(round(ROOTY+uy*(ln-1))), "5")             # 先の金
outline(set("123458"))

# 3) 6基の追尾砲台（左向き。砲口の光・砲身・白い胴・後ろの推進の光）
POD = [
    "..AAAA..",
    "AA1112A.",
    "vA42223A9",
    "AA3334A.",
    "..AAAA..",
]
for (px, py) in ((2, 2), (0, 15), (2, 31), (28, 0), (31, 12), (29, 32)):
    for j, row in enumerate(POD):
        for i, ch in enumerate(row):
            if ch != ".": put(px+i, py+j, ch)
    put(px-1, py+2, "8")      # 砲口の先の光
    put(px+4, py+1, "6")      # 金の帯
    put(px+4, py+3, "7")

# 4) ユーリ（頭は元の絵、体は鎧）
head = src["frames"]["left0"]
BODY = [  # 18〜30行目（左向き）。1〜4=鎧、5〜7=金、8/9/v=光
    "....A566665AA...",
    "...A1112223A3A..",
    "..A11A2v823A33A.",
    "..A21A2898A3A3A.",
    "..A32A22223AA.A.",
    "..A43A5667A.....",
    "..A9AA1223A.....",
    "..A8A21223A.....",
    "...AA31A23A.....",
    "....A12A12A.....",
    "....A23A23A.....",
    "...A556A556A....",
    "...AAAAAAAAA....",
]
for y in range(32):
    row = head[y] if y < 18 else (BODY[y-18] if y-18 < len(BODY) else "." * 16)
    for x, ch in enumerate(row):
        if ch == ".": continue
        put(OX+x, OY+y, ch)
# 兜（2026-10-06 人間の指示「兜もつけよう」）。白い丸い鉢・金の額の帯・目の上のひさし・後ろへ流れる1枚のひれ・
# 首の後ろを守るしころ。前（左）に環の飾り。髪は、ひさしの下の前髪と、しころの下の後ろ髪だけ見せる。
# 記号: "_"=元の絵のまま、"."=消す、ほかは色。V字の角はつけない（CLAUDE.md 1-1）。
HELM = [
    "____________AA__",   # 0  ひれの先
    "__________AA56A_",   # 1
    "________AA5566A_",   # 2
    ".....AAA55566A..",   # 3  ひれの根もと
    "....A11112223A..",   # 4
    "...A111122222A..",   # 5
    "..A11112222233A.",   # 6
    "..A11122222333A.",   # 7
    "..A11222222334A.",   # 8
    "..A12222222344A.",   # 9
    "..A55555555566A.",   # 10 額の帯
    "..AA4AAA12A334A_",   # 11 ひさし・耳当て・しころ
    "___A____A12A44A_",   # 12
    "________A2vA4A__",   # 13 耳当ての環の飾り
    "_________AAA____",   # 14
]
for y, row in enumerate(HELM):
    for x, ch in enumerate(row):
        if ch == "_": continue
        if ch == ".":
            if G[OY+y][OX+x] in LET: put(OX+x, OY+y, ".")    # 元の絵（髪）だけ消す。後ろの光の環は残す
        else:
            put(OX+x, OY+y, ch)
# 額の帯の前（左）に、小さな環の飾り
for (x, y, c) in ((OX+1, OY+9, "A"), (OX+0, OY+10, "A"), (OX+1, OY+10, "v"), (OX+1, OY+11, "A"), (OX+2, OY+10, "5"), (OX+2, OY+9, "A")):
    put(x, y, c)

used = sorted(set(ch for row in G for ch in row if ch != "."))
out_pal = {k: pal[k] for k in used}
open(os.path.join(HERE, "yuri2-cosmo.txt"), "w").write("\n".join("".join(r) for r in G) + "\n")
json.dump(out_pal, open(os.path.join(HERE, "pal-yuri2-cosmo.json"), "w"))
print(len(out_pal), "colors")
