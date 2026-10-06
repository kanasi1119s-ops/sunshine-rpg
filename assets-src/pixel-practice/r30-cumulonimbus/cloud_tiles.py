"""積乱雲の下のマス（2026-10-05、人間の指示「船が雲の上に動けちゃうからどうにかして」）。
雲の絵（reshape5.txt、440×256。2026-10-06 に採用。前は reshape3）は、ゲームで塔のマスのまん中から (-215, -351) の所に描く。
1マス（16×16）のうち 4割以上を雲がおおうマスを、塔のマスからのずれ (dx, dy) にして書き出す。
飛空艇は、このマスに入れない（嵐の雲の中）。船は入れる（雲のうしろを進む）。"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [l for l in open(os.path.join(HERE, "reshape5.txt")).read().split("\n") if l]
cnt = {}
for py, r in enumerate(rows):
    for px, c in enumerate(r):
        if c != ".":
            k = ((px - 215 + 8) // 16, (py - 351 + 8) // 16)
            cnt[k] = cnt.get(k, 0) + 1
cov = sorted((k for k, v in cnt.items() if v >= 0.4 * 256), key=lambda k: (k[1], k[0]))
out = os.path.join(HERE, "..", "..", "..", "src", "game", "map", "world", "tower-cloud.generated.ts")
with open(out, "w") as f:
    f.write("// 自動生成: assets-src/pixel-practice/r30-cumulonimbus/cloud_tiles.py（手で編集しない）。\n")
    f.write("// 芯環塔の上の積乱雲が、4割以上おおうマス（塔のマスからのずれ）。船と飛空艇は入れない。\n")
    f.write("export const TOWER_CLOUD_TILES: ReadonlyArray<readonly [number, number]> = [\n")
    for i in range(0, len(cov), 8):
        f.write("  " + " ".join(f"[{dx}, {dy}]," for dx, dy in cov[i:i + 8]) + "\n")
    f.write("];\n")
print("ok", len(cov))
