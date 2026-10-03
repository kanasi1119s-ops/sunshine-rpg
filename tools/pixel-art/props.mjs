// マップの飾り（木・家）。練習（docs/design/pixel-practice-log.md 第7・8回）で一から描いた絵（assets-src/pixel-practice/）を、
// 48×48の枠の下そろえで置いて書き出す。参考素材の絵は写していない（自作）。
import fs from "fs";
const ROOT = new URL("../../assets-src/pixel-practice/", import.meta.url);
function piece(name, dir, grid, palFile) {
  const rows = fs.readFileSync(new URL(`${dir}/${grid}`, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const pal = JSON.parse(fs.readFileSync(new URL(`${dir}/${palFile}`, ROOT), "utf8"));
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
  piece("P1-木", "r07-tree", "scratch1.txt", "pal-scratch1.json"),
  piece("P2-家", "r08-house", "scratch2.txt", "pal-scratch2.json"),
];
