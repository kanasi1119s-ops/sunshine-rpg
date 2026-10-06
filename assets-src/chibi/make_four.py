"""2頭身の4体（エルフの弓使い・天使・悪魔・魔王）を作る（2026-10-07、人間の指示「なんか4人作って」）。
体は仲間の2頭身の型（女性はアヤメ、男性はレトの体）。髪は heads.py で1から描いた新しい髪型にした（仲間の髪型を使わない）。
使い方: python3 make_four.py → 各フォルダに walker.json・sheet.txt/json（エディタ用）・sheet.png・sheet_x8.png・walk.gif"""
import pathlib
from chibi_parts import Chibi, L, stamp, wing_masks
from heads import ELF, ANGEL, DEMON, LORD

HERE = pathlib.Path(__file__).parent


def apply_head(c, head, hair="BCD", extra=None):
    """head の行で頭を描きかえる。h/H/d は髪（hair の3文字: 地・明・暗）、c/g などは extra の色"""
    m = {"h": hair[0], "H": hair[1], "d": hair[2]}
    m.update(extra or {})
    for k, g in c.frames.items():
        d = k[:-1]
        rows = head.get(d) if d != "right" else {y: r[::-1] for y, r in head["left"].items()}
        for y, r in rows.items():
            g[y] = [m.get(ch, ch) for ch in r]


def clear(c, letters, from_row=0):
    for g in c.frames.values():
        for y in range(from_row, 32):
            g[y] = ["." if ch in letters else ch for ch in g[y]]


def build(name, folder, c):
    out = HERE / folder
    out.mkdir(exist_ok=True)
    n = c.save(out, folder)
    print(name, folder, "色数", n)


# 1. エルフの弓使い（女性）
c = Chibi("アヤメ")
clear(c, "JL")                                   # 杖を外す
for ch, v in zip("BCD", ("#9fd08a", "#e2f6c8", "#4f8a4a")): c.color(ch, v)
c.color("K", "#3a8a4a")
for ch, v in zip("PQRHTSUV", ("#5a8a3a", "#3f6a2a", "#8ab860", "#a8d080", "#2e4f20", "#a8743a", "#6a4020", "#3a2410")): c.color(ch, v)
cc, cg = c.new("#3c7a2c"), c.new("#ffd36b")
apply_head(c, ELF, extra={"c": cc, "g": cg})
bw, bs = c.new("#8a5a2a"), c.new("#e8e0c8")      # 背中の長弓（木と弦）
for k, g in c.frames.items():
    if k.startswith(("down", "left", "right")):
        continue
    for y in range(9, 27):                       # 後ろ向き: 背中に斜めにかけた弓
        x = 3 + (y - 9) * 10 // 17
        if g[y][x] != ".": g[y][x] = bw
for k, g in c.frames.items():
    if k.startswith("left") or k.startswith("right"):
        s = 1 if k.startswith("left") else -1
        for y in range(12, 27):                  # 横向き: 背中から上下に出る弓の先
            x = 13 if s == 1 else 2
            if g[y][x] == ".": g[y][x] = bw
build("エルフの弓使い", "elf-archer", c)

# 2. 天使（男性）
c = Chibi("レト")
for ch, v in zip("BCD", ("#f0c050", "#fff2a8", "#b07a1c")): c.color(ch, v)
c.color("F", "#3a8ad8")
for ch, v in zip("JKLMOPQRSVW", ("#f4f2ea", "#c8b67a", "#ffffff", "#e8e6f0", "#b8b4c8", "#b8a070", "#e8e0c8", "#fff8e8", "#c8b890", "#d8c8a0", "#9a8a60")): c.color(ch, v)
apply_head(c, ANGEL)
c.halo(c.new("#ffe680"), c.new("#c89a2a"), gap=3)
stamp(c, wing_masks(c.new("#f0c860"), c.new("#fff0a0"), c.new("#c8962a"), c.new("#7a5a1a")), over_keys=("up",))   # イメージ画像どおり金の羽
build("天使", "angel", c)

# 3. 悪魔（女性）
c = Chibi("アヤメ")
clear(c, "JL")
for ch, v in zip("BCD", ("#b02a3a", "#e0505a", "#5a1020")): c.color(ch, v)
c.color("K", "#e8b020")
for ch, v in zip("PQRHT", ("#2a1a24", "#160c14", "#5a1a2a", "#3a2030", "#401020")): c.color(ch, v)
for g in c.frames.values():                      # アヤメの長い後ろ髪は使わない（ポニーテールにした）
    for y in range(19, 32):
        g[y] = ["." if ch in "BC" else ("A" if ch == "D" else ch) for ch in g[y]]
apply_head(c, DEMON)
hn, hl = c.new("#2a2028"), c.new("#8a7a94")
stamp(c, {"down": [(4, 3, hn), (3, 3, hn), (2, 2, hl), (4, 12, hn), (3, 12, hn), (2, 13, hl)],
          "up": [(4, 3, hn), (3, 3, hn), (2, 2, hl), (4, 12, hn), (3, 12, hn), (2, 13, hl)],
          "left": [(4, 5, hn), (3, 5, hn), (2, 4, hl), (4, 10, hn), (3, 11, hn), (2, 11, hl)]})
stamp(c, wing_masks(c.new("#b0202a"), c.new("#e04a4a"), c.new("#6a0a14"), "A", bat=True), over_keys=("up",))   # イメージ画像どおり赤い羽
c.tail(c.new("#3a1a3a"), c.new("#e0505a"))
build("悪魔", "demon", c)

# 4. 魔王（男性）
c = Chibi("レト")
for ch, v in zip("BCD", ("#2a2238", "#4e3e66", "#120c18")): c.color(ch, v)
c.color("F", "#ff3030")
for ch, v in zip("JKLMOPQRSVW", ("#9a1a22", "#5a0a12", "#4a4a58", "#2a2a34", "#16161c", "#3a3040", "#2a2232", "#4a3e58", "#1e1824", "#2e2638", "#140e18")): c.color(ch, v)
apply_head(c, LORD)
c.cape(c.new("#8a1420"), c.new("#5a0a14"), "A", start=17, end=29)
kn, kl, kg = c.new("#241a2e"), c.new("#9a88b4"), c.new("#ff3a3a")
L_HORN = [(6, 2), (5, 2), (4, 2), (3, 2), (2, 3), (1, 3), (0, 4)]   # イメージ画像のような、大きく反った2本の角
crown = [(y, x, kl if y == 0 else kn) for y, x in L_HORN] + [(y, 15 - x, kl if y == 0 else kn) for y, x in L_HORN]
stamp(c, {"down": crown, "up": crown,
          "left": [(5, 4, kn), (4, 4, kn), (3, 4, kn), (2, 5, kn), (1, 5, kn), (0, 6, kl), (5, 12, kn), (4, 12, kn), (3, 12, kn), (2, 11, kn), (1, 11, kl)]},
      over_keys=())
for k, g in c.frames.items():                     # 冠のまん中の赤い石は、頭の上にのせる
    if k[:-1] in ("down", "up"):
        g[3][7] = g[3][8] = kg
build("魔王", "demon-lord", c)
