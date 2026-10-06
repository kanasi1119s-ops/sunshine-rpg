"""歩くモンスター（4本足など、立たせない）の2頭身ドット絵を、3つの型（16×16／16×32＋32×16／16×32）で書き出す共通の道具。
2026-10-07、人間の指示「このパターン記録しよう。ほかのモンスターでもやってみて」で、苔岩の子竜（koke-iwa-ryu/make.py）から取り出した。
使い方: 各モンスターの make.py で PAL（記号→色）と各向きの行を決め、save(HERE, フォルダ名, グループ, PAL) を呼ぶ。"""
import json
from PIL import Image

ORDER = ["down", "up", "left", "right"]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def mirror(half_rows):
    darker = {"D": "C", "E": "D", "H": "G"}
    return [r + "".join(darker.get(c, c) for c in r[::-1]) for r in half_rows]


LEG_L = ["AA.", "DCC", "CBB", "NNA"]           # 左の足（上から 付け根・足・足・爪）。体の縁に重ねて付ける
LEG_R = [".AA", "BCB", "BBB", "ANN"]           # 右の足（右半分なので1段暗い）


def put_leg(g, y0, left, spr=None, x0=None):
    """足の部品を置く。spr と x0 を渡すと、その形と位置で置く（後ろ向きの小さな足など）"""
    if spr is None:
        spr = LEG_L if left else LEG_R
    if x0 is None:
        x0 = 1 if left else 12
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


def save(HERE, folder, groups, PAL):
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
    json.dump(walker, open(out / f"{HERE.name}.walker.json", "w"), ensure_ascii=False)
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


