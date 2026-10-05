"""ドット絵エディタで書き出した術のシート（assets-src/effects/spells/<属性>/editor/<種類>.sheet.png）を、ゲームに入れる（2026-10-05）。

使い方: python3 tools/pixel-art/fx/export-spell-sheets.py
出力:
  src/assets/spell-fx/<属性>-<種類>.png … シート（色の数が少ないので、色番号つきPNGにして小さくする。1ドットも変えない）
  src/game/art/spell-fx.generated.ts   … コマの大きさ・足もとの点・長さ・光・揺れ
シートとコマのJSONが1マスでもちがうときは、止まる（先に verify_sheet.py で0マスにしておく）。
"""
import json
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC = os.path.join(ROOT, "assets-src", "effects", "spells")
OUT_IMG = os.path.join(ROOT, "src", "assets", "spell-fx")
OUT_TS = os.path.join(ROOT, "src", "game", "art", "spell-fx.generated.ts")


def expected(fx, k):
    W, H = fx["w"], fx["h"]
    f = fx["frames"][k]
    exp = np.zeros((H, W, 4), np.uint8)
    for y, r in enumerate(f["rows"]):
        for x, c in enumerate(r):
            if c != ".":
                v = fx["palette"][c]
                exp[f["y"] + y, f["x"] + x] = [int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16), 255]
    return exp


def main():
    os.makedirs(OUT_IMG, exist_ok=True)
    meta = {}
    total = 0
    for el in sorted(os.listdir(SRC)):
        d = os.path.join(SRC, el)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".json"):
                continue
            kind = name[:-5]
            fx = json.load(open(os.path.join(d, name)))
            sheet_path = os.path.join(d, "editor", f"{kind}.sheet.png")
            if not os.path.exists(sheet_path):
                print("× シートが無い:", sheet_path)
                sys.exit(1)
            sh = np.array(Image.open(sheet_path).convert("RGBA"))
            W, H, n = fx["w"], fx["h"], len(fx["frames"])
            for k in range(n):
                got = sh[:, k * W:(k + 1) * W]
                exp = expected(fx, k)
                bad = ((exp[..., 3] > 0) != (got[..., 3] > 0)) | ((exp[..., 3] > 0) & (np.abs(exp[..., :3].astype(int) - got[..., :3]).sum(2) > 6))
                if bad.any():
                    print(f"× {el}/{kind} の {k} コマ目が、エディタのシートと {int(bad.sum())} マスちがう")
                    sys.exit(1)
            # 透明（アルファ0）を1色にまとめて、色番号つきPNGに
            img = sh[:, : W * n].copy()
            img[img[..., 3] == 0] = 0
            pil = Image.fromarray(img, "RGBA")
            q = pil.quantize(colors=min(256, len(fx["palette"]) + 1), method=Image.Quantize.FASTOCTREE)
            back = np.array(q.convert("RGBA"))
            if not np.array_equal((back[..., 3] > 0), (img[..., 3] > 0)) or np.abs(back[..., :3].astype(int) - img[..., :3])[img[..., 3] > 0].max(initial=0) > 0:
                q = pil   # 色が変わるなら、そのままのPNGで
            out = os.path.join(OUT_IMG, f"{el}-{kind}.png")
            q.save(out, optimize=True)
            total += os.path.getsize(out)
            meta[f"{el}/{kind}"] = {
                "w": W, "h": H, "ax": fx["anchor"][0], "ay": fx["anchor"][1],
                "flashColor": fx["frames"][0].get("flash_color", "#ffffff"),
                "frames": [[f["ms"], f.get("flash", 0), f.get("shake", 0)] for f in fx["frames"]],
            }
    with open(OUT_TS, "w") as fp:
        fp.write("// 自動生成（tools/pixel-art/fx/export-spell-sheets.py）。手で書きかえない。\n")
        fp.write("// 術のエフェクトのコマ（ドット絵エディタで書き出したシート src/assets/spell-fx/<属性>-<種類>.png）の、大きさ・足もとの点・コマごとの [長さms, 光, 揺れ]。\n")
        fp.write("export interface SpellFxSheet { w: number; h: number; ax: number; ay: number; flashColor: string; frames: [number, number, number][] }\n")
        fp.write("export const SPELL_FX: Record<string, SpellFxSheet> = ")
        fp.write(json.dumps(meta, ensure_ascii=False, separators=(",", ":")))
        fp.write(";\n")
    print(len(meta), "組", round(total / 1024), "KiB")


if __name__ == "__main__":
    main()
