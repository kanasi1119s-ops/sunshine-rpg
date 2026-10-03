// マップの飾り（木・家）。練習（docs/design/pixel-practice-log.md 第7・8回）で一から描いた絵（assets-src/pixel-practice/）を、
// 48×48の枠の下そろえで置いて書き出す。参考素材の絵は写していない（自作）。
import fs from "fs";
const ROOT = new URL("../../assets-src/pixel-practice/", import.meta.url);
function piece(name, dir, grid, palFile, recolor = {}) {
  const rows = fs.readFileSync(new URL(`${dir}/${grid}`, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const pal = { ...JSON.parse(fs.readFileSync(new URL(`${dir}/${palFile}`, ROOT), "utf8")), ...recolor };
  const keys = Object.keys(pal);
  const h = rows.length, w = Math.max(...rows.map((r) => r.length));
  return {
    name,
    pal: keys.map((k) => [k, pal[k]]),
    build() {
      const g = Array.from({ length: 48 }, () => Array(48).fill(-1));
      const ox = Math.floor((48 - w) / 2), oy = 48 - h;   // 横は中央、縦は下そろえ
      rows.forEach((r, y) => [...r].forEach((ch, x) => { const k = keys.indexOf(ch); if (k >= 0) g[oy + y][ox + x] = k; }));
      return g;
    },
  };
}
export const PIECES = [
  // 磨き直した版（assets-src/pixel-practice/r17-polish/。生成の元は tree.py・house.py・smallprops.py）
  piece("P1-木", "r17-polish", "tree4.txt", "pal-tree.json"),
  piece("P2-家", "r17-polish", "house2.txt", "pal-house.json"),
  piece("P3-家青", "r17-polish", "house2.txt", "pal-house-blue.json"),
  piece("P4-家緑", "r17-polish", "house2.txt", "pal-house-green.json"),
  piece("P5-岩", "r17-polish", "rock2.txt", "pal-rock2.json"),
  piece("P6-茂み", "r17-polish", "bush2.txt", "pal-bush2.json"),
];
