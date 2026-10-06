"""2頭身の4体（エルフの弓使い・天使・悪魔・魔王）を作る（2026-10-07、人間の指示「なんか4人作って」）。
体は仲間の2頭身の型（女性はアヤメ、男性はレトの体）。髪は heads.py で1から描いた新しい髪型にした（仲間の髪型を使わない）。
使い方: python3 make_four.py → 各フォルダに walker.json・sheet.txt/json（エディタ用）・sheet.png・sheet_x8.png・walk.gif"""
import pathlib
from chibi_parts import Chibi, L, stamp, wing_masks, swing_arms, swing_arms_ayame, swing_arms_side
from heads import ELF, ANGEL, DEMON, LORD_HELM

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
swing_arms_ayame(c)                              # 両手を交互に上下（魔王と同じ動き。人間の指示）
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
# 髪の動きをなめらかに（2026-10-07、人間の指示「前面と後面と横から見る髪の動きがなめらかじゃない」）。
# もとの型（アヤメ）の髪のすその動きは、エルフの新しい髪型と形が合わず、点がばらばらに動いていた。
# 歩きは 1→0→2→0 の順なので、コマ1と2を同じ「はずんだ形」、コマ0を「ふつうの形」にそろえ、
# 前・後ろは横髪のすそが1ドット上がり、横はうしろに流れる髪が1ドット後ろへふくらむ（毎歩同じ動きでゆれる）。
def set_cols(g, y, x0, s):
    for i, ch in enumerate(s):
        g[y][x0 + i] = ch


def mirror_s(s):
    return s[::-1]


HAIR_DOWN = {0: [".AB", ".AB", ".AB", ".AB", ".AD", ".AD", "..A"],
             1: [".AB", ".AB", ".AB", ".AD", ".AD", "..A", "..A"]}   # 15〜21行め（左のすそ。右は左右反転）
HAIR_UP = {0: [".AD", ".AD", ".AD", ".AD"], 1: [".AD", ".AD", ".AD", "..A"]}   # 18〜21行め
down0 = [list(r) for r in c.frames["down0"]]
up0 = [list(r) for r in c.frames["up0"]]
for f in range(3):
    k = 0 if f == 0 else 1
    g = c.frames[f"down{f}"]
    for y in range(15, 22):                       # 髪の両わき（x=0〜3, 12〜15）はコマ0にそろえてから、すそを上げる
        for x in list(range(0, 4)) + list(range(12, 16)):
            g[y][x] = down0[y][x]
    gu = c.frames[f"up{f}"]
    for y in range(18, 22):
        for x in list(range(0, 5)) + list(range(11, 16)):
            gu[y][x] = up0[y][x]
    for i, s in enumerate(HAIR_DOWN[k]):
        set_cols(g, 15 + i, 0, s); set_cols(g, 15 + i, 13, mirror_s(s))
    g = c.frames[f"up{f}"]
    for i, s in enumerate(HAIR_UP[k]):
        set_cols(g, 18 + i, 0, s); set_cols(g, 18 + i, 13, mirror_s(s))
side0 = [list(r) for r in c.frames["left0"]]
for f in (1, 2):
    g = c.frames[f"left{f}"]
    for y in range(13, 22):                       # うしろの髪（x=11より後ろ）は、まずコマ0にそろえる
        for x in range(11, 16):
            g[y][x] = side0[y][x]
    pass
# 横向きのうしろ髪のすそ（x=11〜15、17〜21行め）を、髪の色の形で描きなおす（人間の指示「横から見た髪の動きまだ違和感あります」）。
# ミナの横向きのように、すそは先ほど大きく後ろへはね、縁取りだけの棒にならないようにする。コマ1は大きく、コマ2は小さくはねる。
SIDE_TIP = {
    0: ["BBDA.", "BBDA.", "ADBA.", "ADDA.", "AAA.."],
    1: ["BBBDA", "BBBDA", "ADBBA", "ADDBA", "AAAA."],
    2: ["BBDA.", "BBDA.", "ADBBA", "ADDA.", "AAA.."],
}
for f in range(3):
    g = c.frames[f"left{f}"]
    for i, s in enumerate(SIDE_TIP[f]):
        set_cols(g, 17 + i, 11, s)
for f in range(3):
    c.frames[f"right{f}"] = [r[::-1] for r in c.frames[f"left{f}"]]
build("エルフの弓使い", "elf-archer", c)

# 2. 天使（男性）
c = Chibi("レト")
for ch, v in zip("BCD", ("#f0c050", "#fff2a8", "#b07a1c")): c.color(ch, v)
c.color("F", "#3a8ad8")
for ch, v in zip("JKLMOPQRSVW", ("#f4f2ea", "#c8b67a", "#ffffff", "#e8e6f0", "#b8b4c8", "#b8a070", "#e8e0c8", "#fff8e8", "#c8b890", "#d8c8a0", "#9a8a60")): c.color(ch, v)
apply_head(c, ANGEL)
swing_arms(c)                                    # 止まっていた手も、もう片方と同じように動かす（人間の指示）
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
swing_arms_ayame(c)                              # 両手を交互に上下（魔王と同じ動き。人間の指示）
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
for ch, v in zip("BCD", ("#26222e", "#5e5870", "#100c14")): c.color(ch, v)   # 黒いかぶと
apply_head(c, LORD_HELM, extra={"k": c.new("#1e1a24"), "l": c.new("#7a7488"),          # 角
                                "e": c.new("#ffe6c8"), "r": c.new("#ff3a2a"), "R": c.new("#a01820")})  # 赤く光る目と光の流れ
swing_arms(c)                                    # 止まっていた手も動かす（左右交互。人間の指示）
c.cape(c.new("#8a1420"), c.new("#5a0a14"), "A", start=17, end=29)
# 顔はイメージ画像どおり、黒いかぶとで全部おおい、まん中に赤く光る目を1つ（2026-10-07、人間の指示「魔王の顔はおおもとの画像を忠実に再現してほしい」）
build("魔王", "demon-lord", c)
