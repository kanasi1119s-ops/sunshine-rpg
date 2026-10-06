"""苔岩の子竜（2頭身の歩くモンスター）を、3つの大きさで作って見比べる。
2026-10-07、人間の指示「モンスターも1体作ってみて」「却下、32×16よ」「無理なら16×16でも検討して。もしくは16×32か」
「16×32と32×16をうまく使うのもありだね」「とりあえずこのパターン全部やってみて」。
最初に作った 32×32 の待機絵は old-32x32/ に残した（採用しない）。

3つのパターン（どれも 4方向×3コマの歩き。右向きは左向きの左右反転）:
- v16x32/ … 16×32 だけ。下・上は体が奥へのびる長い竜、横は 16×16 の竜を下にそろえて置く
- v16x16/ … 16×16。小さな4本足の竜（頭が全体の半分より大きい）
- mix/    … 下・上は 16×32（体が奥へのびる）、横は 32×16（イメージ画像どおり、4本足で低く歩く形）
立たせない（2026-10-07、人間の指示「立たせないで」）。どれも4本足で歩く。

イメージ画像（ref.png, Stable Diffusion 1.5）から残した特ちょう: 苔の緑の体と模様／頭の上の灰色の石のとげ（冠のように並ぶ）／
黒いアーモンド形の大きな目と石のまゆ／灰色の羽（とげつき）／しっぽと灰色の爪。
下・上は左半分を描いて左右反転でつなぐ（右半分の明るい色は1段暗くして、光を左上にする）。
使い方: python3 make.py → 各フォルダに walker.json・sheet.txt/json（エディタ用）・sheet.png・sheet_x8.png・walk.gif"""
import json
import pathlib
from PIL import Image

HERE = pathlib.Path(__file__).parent
ORDER = ["down", "up", "left", "right"]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

PAL = {
    "A": "#1a2014",  # 縁取り（こい緑の黒）
    "a": "#2e3e1c",  # 中の縁取り
    "B": "#40601e",  # 苔の暗
    "C": "#6e922c",  # 苔の地
    "D": "#9cbc42",  # 苔の明
    "E": "#cfe070",  # 苔のいちばん明るい所
    "F": "#3a3a42",  # 石の暗
    "G": "#6c6c76",  # 石の地
    "H": "#a2a2ae",  # 石の明
    "J": "#0e0e14",  # 目
    "K": "#ffffff",  # 目の光
    "L": "#2a1c14",  # 口・鼻の穴
    "M": "#b8cc6a",  # おなか・口のまわり
    "N": "#24242a",  # 爪
}


def mirror(half_rows):
    darker = {"D": "C", "E": "D", "H": "G"}
    return [r + "".join(darker.get(c, c) for c in r[::-1]) for r in half_rows]


# 4本足の竜（2026-10-07、人間の指示「立たせないで」）。見下ろしのRPGなので、
# 下・上向きは「体が奥へ長くのびる」形を 16×32 に、横向きは「低く長い」形を 32×16 に描くと、長い竜をそのまま描ける。

LEG_L = ["AA.", "DCC", "CBB", "NNA"]           # 左の足（上から 付け根・足・足・爪）。体の縁に重ねて付ける
LEG_R = [".AA", "BCB", "BBB", "ANN"]           # 右の足（右半分なので1段暗い）


def put_leg(g, y0, left):
    spr, x0 = (LEG_L, 1) if left else (LEG_R, 12)
    for i, r in enumerate(spr):
        y = y0 + i
        if 0 <= y < len(g):
            row = list(g[y])
            for j, c in enumerate(r):
                if c != ".":
                    row[x0 + j] = c
            g[y] = "".join(row)


def sway(g, rows, dx):
    """しっぽの行を左右に1ドットずらす"""
    for y in rows:
        r = g[y]
        g[y] = (r[1:] + ".") if dx < 0 else ("." + r[:-1])


# =============== 16×32（下・上。体が奥へのびる長い竜） ===============
L_DOWN = mirror([
    "......AA",   # 0  しっぽの先（いちばん奥）
    "......AC",
    "......AC",
    ".....ABC",
    ".....ABC",
    "....ABCC",   # 5  背中
    "...ABCCG",   # 6  背中の石のとげ
    "..A.ABCF",   # 7  たたんだ羽（背中の左右）
    ".AHAABCG",
    ".AGHABCF",
    "AGHGABCG",
    "AFGHAaCF",
    "AFFGHABC",
    ".AFFGABC",
    "..AAAaBC",
    "...ABCCC",   # 15
    "...ABCCC",
    "....AAGF",   # 17 首・頭の石の冠
    "...AGFGF",
    "..AGFGFG",
    "..ADGFGG",
    "..ADCCDC",
    "..ACFFFC",   # 22 まゆの石
    "..AHJJJC",   # 23 目
    "..AJKJJC",
    "..ACHHHC",
    "..ABCCML",   # 26 鼻の穴
    "..ABCMMM",
    "...ABLLL",   # 28 口
    "....AMMM",
    ".....AAA",
])
L_UP = mirror([
    "....A..A",   # 0  頭の石のとげ（後ろから）
    "...AHAAH",
    "..AGFGFG",
    "..ADGGFG",
    "..ADCCGF",
    "..ACCBFG",
    "..ACCCGF",
    "..ABCCCF",
    "...ABCCG",
    "....ABCF",   # 9  首
    "...ABCCG",
    "..A.ABCF",   # 11 たたんだ羽
    ".AHAABCG",
    ".AGHABCF",
    "AGHGABCG",
    "AFGHAaCF",
    "AFFGHABC",
    ".AFFGABC",
    "..AAAaBC",
    "...ABCCC",
    "...ABBCC",
    "....ABCC",
    "....ABCC",
    ".....ABC",   # 23 しっぽ（手前へ）
    ".....ABC",
    "......AC",
    "......AC",
    "......AC",
    "......AA",
])


def long_frames():
    fr = {}
    for f in range(3):
        g = list(L_DOWN) + ["." * 16]
        a, b = {0: (27, 27), 1: (28, 26), 2: (26, 28)}[f]      # 前足（頭の左右）を交互に
        put_leg(g, a, True); put_leg(g, b, False)
        a, b = {0: (15, 15), 1: (14, 16), 2: (16, 14)}[f]      # 後ろ足は前足と逆
        put_leg(g, a, True); put_leg(g, b, False)
        if f:
            sway(g, range(0, 5), -1 if f == 1 else 1)          # しっぽの先がゆれる
        fr[f"down{f}"] = g
        g = list(L_UP) + ["." * 16] * 3
        a, b = {0: (6, 6), 1: (5, 7), 2: (7, 5)}[f]            # 前足（首の左右）
        put_leg(g, a, True); put_leg(g, b, False)
        a, b = {0: (18, 18), 1: (19, 17), 2: (17, 19)}[f]      # 後ろ足
        put_leg(g, a, True); put_leg(g, b, False)
        if f:
            sway(g, range(24, 29), -1 if f == 1 else 1)
        fr[f"up{f}"] = g
    return fr


# =============== 16×16（小さな4本足の竜） ===============
S_DOWN = mirror([
    "....A..A",   # 0  石のとげ
    "...AHAAH",
    ".A.AGFGF",   # 2  羽の先（頭の後ろからのぞく）
    "AHAGFGFG",
    "AGADGGFG",
    "AFADCCDC",
    ".AACFFFC",   # 6  まゆ
    "..AHJJJC",   # 7  目
    "..AJKJJC",
    "..ACHHHC",
    "..ABCCML",   # 10 鼻
    "..ABCMMM",
    "...ABLLL",   # 12 口
    "....AMMM",
    ".....AAA",
])
S_UP = mirror([
    "....A..A",
    "...AHAAH",
    "..AGFGFG",
    ".AADGGFG",
    "AHAACCGF",   # 4  羽
    "AGHABCFG",
    "AFGHABCG",
    ".AFGABCF",
    "..AAABCC",
    "...ABCCC",
    "....ABCC",
    ".....ABC",   # 11 しっぽ
    "......AC",
    "......AC",
    "......AA",
])
S_SIDE = [
    "...A.A.A........",   # 0  石のとげ
    "..AHAHAHA..A....",
    ".AGFGFGFGAAHA...",   # 2  羽の先
    ".ADGGFGFGAGHA...",
    "ACFFFCCGAGHGA...",   # 4  まゆ・羽
    "AHJJHCCCBAGFA...",   # 5  目
    "AJKJCCCCCBAA....",
    "MCHHCCCCCCCBAA.A",   # 7  鼻先・しっぽ
    "LMCCCCCBCCCCBADA",
    "AMMCCCMMMMMCCCBA",
    "ALLLMMMMMMMMABA.",   # 10 口・おなか
    ".AMMMAAAAAAAAA..",
]
S_SIDE_LEGS = {0: ["..ACBA..ACBA....", ".ANNBA.ANNBA....", ".AAAAA.AAAAA...."],
               1: [".ACBA....ABBA...", "ANNBA...ANNBA...", "AAAAA...AAAAA..."],
               2: ["...ABBA.ACBA....", "..ANNBAANNBA....", "..AAAAAAAAAA...."]}


def small_frames():
    fr = {}
    for f in range(3):
        g = list(S_DOWN) + ["." * 16]
        a, b = {0: (11, 11), 1: (12, 10), 2: (10, 12)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        fr[f"down{f}"] = g
        g = list(S_UP) + ["." * 16]
        a, b = {0: (8, 8), 1: (9, 7), 2: (7, 9)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        if f:
            sway(g, range(11, 15), -1 if f == 1 else 1)
        fr[f"up{f}"] = g
        fr[f"left{f}"] = S_SIDE + S_SIDE_LEGS[f]
    return fr


# =============== 32×16（横向き・4本足で低く歩く形。mix で使う） ===============
W_SIDE = [
    "....A.A.A.....A.................",   # 0  頭の石のとげ・羽の先
    "...AHAHAHA...AHA...A............",
    "..AGFGFGFGA..AGHA.AHA...........",   # 2  羽（背中から上へ、とげ3本）
    "..AGFGFGFGGAAGFGHAGHA.A.........",
    ".ADGGFGFGFGAAFGFGHGHAHA.........",
    ".ADCFFFFCCGAaFFFGFGHGHA.........",   # 5  まゆの石
    "ACHJJJHCCCBAaaFFFFFGFA..........",   # 6  目
    "ACJKJJCCCCCBBCaAAAAAAA..........",
    "AMHHHCCCCBCCDCDCCCBCCCAA.......A",   # 8  鼻先・背中・しっぽの先
    "LMMCCCCBCCCDCCCCCBCCCCCBAA...AEA",
    "AMMMCCCCCCMMMMMMMMMCCCCCCBAAAADA",
    "ALLLLMCCCAMMMMMMMMMMACCCBBBBBBA.",   # 11 口・おなか
    ".AMMMMMCAAMMMMMMMMMMAABBAAAAAA..",
    "..AAAAAA",                             # 13 以降は足
]
W_LEGS = {  # 13〜15行め。前足（x=7〜10）と後ろ足（x=19〜22）を交互に出す
    0: ["........ACCBA.......ACCBA.......", ".......ANNNCA......ANNNCA.......", ".......AAAAAA......AAAAAA......."],
    1: [".......ACCBA..........ABBA......", "......ANNNCA.........ANNNA......", "......AAAAAA.........AAAAA......"],
    2: ["........ABBA.......ACCBA........", "........ANNNA.....ANNNCA........", "........AAAAA.....AAAAAA........"],
}


def wide_side_frames():
    fr = {}
    for f in range(3):
        top = [r.ljust(32, ".") for r in W_SIDE[:13]]
        fr[f"left{f}"] = top + W_LEGS[f]
    return fr


# =============== 書き出し ===============
def finish(fr, fw, fh):
    out = {}
    for k, g in fr.items():
        g = [r.ljust(fw, ".")[:fw] for r in g]
        g += ["." * fw] * (fh - len(g))
        out[k] = g[:fh]
    for f in range(3):
        if f"left{f}" in out:
            out[f"right{f}"] = [r[::-1] for r in out[f"left{f}"]]
    return out


def to_img(rows, palette, k=1):
    im = Image.new("RGBA", (len(rows[0]), len(rows)))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != ".":
                h = palette[LETTERS.index(c)].lstrip("#")
                im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def save(folder, groups):
    """groups: [(名前, frames, 1コマの幅, 高さ, 向きの並び)]。1つのフォルダに、グループごとのシートを書く"""
    out = HERE / folder
    out.mkdir(exist_ok=True)
    allf = {}
    for _, fr, _, _, _ in groups:
        allf.update(fr)
    used = sorted({c for g in allf.values() for r in g for c in r} - {"."})
    remap = {c: LETTERS[i] for i, c in enumerate(used)}
    palette = [PAL[c] for c in used]
    walker = {"palette": palette, "frames": {}}
    gif = []
    for name, fr, fw, fh, dirs in groups:
        frames = {k: ["".join(remap.get(c, c) for c in r) for r in g] for k, g in fr.items()}
        walker["frames"].update(frames)
        sheet = [""] * (fh * len(dirs))
        for ri, d in enumerate(dirs):
            for f in range(3):
                for y, row in enumerate(frames[f"{d}{f}"]):
                    sheet[ri * fh + y] += row
        suffix = "" if len(groups) == 1 else "-" + name
        (out / f"sheet{suffix}.txt").write_text("\n".join(sheet) + "\n")
        json.dump({LETTERS[i]: v for i, v in enumerate(palette)}, open(out / f"sheet{suffix}.json", "w"))
        to_img(sheet, palette).save(out / f"sheet{suffix}.png")
        big = Image.new("RGBA", (fw * 3 * 8, fh * len(dirs) * 8), (52, 60, 72, 255))
        big.alpha_composite(to_img(sheet, palette, 8))
        big.save(out / f"sheet{suffix}_x8.png")
    json.dump(walker, open(out / "koke-iwa-ryu.walker.json", "w"), ensure_ascii=False)
    # 動きのGIF（下・上・左・右の順に、1→0→2→0 で2回ずつ）。大きさのちがうコマは、下をそろえて同じ台に置く
    allframes = walker["frames"]
    cw = max(len(g[0]) for g in allframes.values()) * 6
    ch = max(len(g) for g in allframes.values()) * 6
    for d in ORDER:
        for _ in range(2):
            for f in (1, 0, 2, 0):
                g = allframes[f"{d}{f}"]
                im = Image.new("RGBA", (cw, ch), (52, 60, 72, 255))
                sp = to_img(g, palette, 6)
                im.alpha_composite(sp, ((cw - sp.width) // 2, ch - sp.height))
                gif.append(im.convert("P", palette=Image.ADAPTIVE))
    gif[0].save(out / "walk.gif", save_all=True, append_images=gif[1:], duration=200, loop=0)
    print(folder, "色数", len(used))


def main():
    long = finish(long_frames(), 16, 32)
    small = finish(small_frames(), 16, 16)
    wide = finish(wide_side_frames(), 32, 16)
    # 16×32 だけで作るとき: 下・上は長い竜、横は 16×16 の竜を 16×32 の下にそろえて置く
    tall_side = {k: ["." * 16] * 16 + v for k, v in small.items() if k[:-1] in ("left", "right")}
    save("v16x32", [("all", {**{k: v for k, v in long.items() if k[:-1] in ("down", "up")}, **tall_side}, 16, 32, ORDER)])
    save("v16x16", [("all", small, 16, 16, ORDER)])
    save("mix", [("down-up", {k: v for k, v in long.items() if k[:-1] in ("down", "up")}, 16, 32, ["down", "up"]),
                 ("side", wide, 32, 16, ["left", "right"])])


if __name__ == "__main__":
    main()
