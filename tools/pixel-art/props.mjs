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
  piece("P1-木", "r07-tree", "scratch1.txt", "pal-scratch1.json"),
  piece("P2-家", "r08-house", "scratch2.txt", "pal-scratch2.json"),
  // 家の色違い（屋根の5色だけ差し替え）
  piece("P3-家青", "r08-house", "scratch2.txt", "pal-scratch2.json", { R: "#4a78c8", r: "#3a60a8", Y: "#2c4a88", Z: "#1c2a58", H: "#78a4e8" }),
  piece("P4-家緑", "r08-house", "scratch2.txt", "pal-scratch2.json", { R: "#4a9a58", r: "#3a7a46", Y: "#2c5c38", Z: "#183a28", H: "#7ac888" }),
  piece("P5-岩", "r13-props", "rock.txt", "pal-rock.json"),
  piece("P6-茂み", "r13-props", "bush.txt", "pal-bush.json"),
];
