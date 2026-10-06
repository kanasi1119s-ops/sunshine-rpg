"""モンスタードット絵の販売用パックを組み立てる（2026-10-07、人間の指示「モンスタードット絵をまとめて販売できるように。DLsiteで、全部を1パックに、等倍＋2倍＋4倍」）。

公開・価格設定・ストアへの登録はしない（CLAUDE.md 1-2。人間の承認が要る）。ここでは、売るファイルを作るだけ。
- 絵は各敵の final.txt / final.json（ドット絵エディタで描いた最終版）から、背景が透明な PNG を作る（拡大は最近傍で、にじみ無し）
- ボスの名前は、物語の謎とつながらないよう、販売用の名前（boss_names.json）にする
使い方: python3 tools/sales/build_monster_pack.py 出力フォルダ
"""
import csv, json, os, shutil, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ART = os.path.join(ROOT, "assets-src", "monsters")
ROSTER = json.load(open(os.path.join(ROOT, "tools", "pixel-art", "ai-gen", "monster-roster.json")))
BOSS_NAMES = json.load(open(os.path.join(os.path.dirname(__file__), "boss_names.json")))
TITLE = "モンスタードット絵224体"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def render(i):
    rows = [r for r in open(f"{ART}/{i}/final.txt").read().split("\n") if r.strip()]
    pal = json.load(open(f"{ART}/{i}/final.json"))
    im = Image.new("RGBA", (len(rows[0]), len(rows)))
    px = im.load()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != ".":
                h = pal[c].lstrip("#")
                px[x, y] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
    return im, len(pal)


def sheet(items, cell, cols, path, title):
    f = ImageFont.truetype(FONT, 14); ft = ImageFont.truetype(FONT, 22)
    rows = (len(items) + cols - 1) // cols
    W = cols * (cell + 8) + 8; H = rows * (cell + 44) + 50
    s = Image.new("RGB", (W, H), (36, 34, 46))
    d = ImageDraw.Draw(s)
    d.text((10, 10), title, font=ft, fill=(255, 226, 140))
    for n, (no, name, im) in enumerate(items):
        x = 8 + (n % cols) * (cell + 8); y = 50 + (n // cols) * (cell + 44)
        k = max(1, cell // max(im.size))
        big = im.resize((im.width * k, im.height * k), Image.NEAREST)
        s.paste(big, (x + (cell - big.width) // 2, y + (cell - big.height) // 2), big)
        d.text((x, y + cell + 2), no, font=f, fill=(160, 160, 180))
        while name and d.textlength(name, font=f) > cell + 6:
            name = name[:-1]
        d.text((x, y + cell + 20), name, font=f, fill=(230, 230, 240))
    s.save(path)


def main():
    out = sys.argv[1]
    top = os.path.join(out, TITLE)
    if os.path.exists(top):
        shutil.rmtree(top)
    mobs = [e for e in ROSTER if e["kind"] == "mob" and e["status"] == "done"]
    bosses = [e for e in ROSTER if e["kind"] == "boss" and e["status"] == "done"]
    cat = []
    groups = (("雑魚", "mob", mobs, 3, lambda e: e["name"]), ("ボス", "boss", bosses, 2, lambda e: BOSS_NAMES[e["id"]]))
    sheets = {}
    for label, pre, items, width, namef in groups:
        sheets[label] = []
        for n, e in enumerate(items, 1):
            no = f"{pre}_{n:0{width}d}"
            im, ncol = render(e["id"])
            for k in (1, 2, 4):
                d = os.path.join(top, f"{label}_{im.width}px", f"{k}倍"); os.makedirs(d, exist_ok=True)
                im.resize((im.width * k, im.height * k), Image.NEAREST).save(os.path.join(d, f"{no}.png"), optimize=True)
            cat.append([no, label, namef(e), f"{im.width}×{im.height}", ncol])
            sheets[label].append((no, namef(e), im))
    d = os.path.join(top, "一覧"); os.makedirs(d, exist_ok=True)
    m = sheets["雑魚"]
    for p in range(0, len(m), 50):
        sheet(m[p:p + 50], 112, 10, os.path.join(d, f"雑魚一覧_{p // 50 + 1}.png"), f"雑魚 {p + 1}〜{min(p + 50, len(m))}（96×96 を 1倍で表示）")
    sheet(sheets["ボス"], 256, 6, os.path.join(d, "ボス一覧.png"), "ボス 24体（256×256・等倍）")
    with open(os.path.join(top, "一覧.csv"), "w", newline="", encoding="utf-8-sig") as fp:
        w = csv.writer(fp); w.writerow(["番号", "種類", "参考名", "大きさ（等倍）", "色数"]); w.writerows(cat)
    shutil.copy(os.path.join(os.path.dirname(__file__), "monster-pack-README.txt"), os.path.join(top, "はじめにお読みください.txt"))
    print("雑魚", len(mobs), "ボス", len(bosses), "→", top)


if __name__ == "__main__":
    main()
