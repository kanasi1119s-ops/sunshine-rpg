// マップの飾り（木・家）。練習（docs/design/pixel-practice-log.md 第7・8回）で一から描いた絵（assets-src/pixel-practice/）を、
// 48×48の枠の下そろえで置いて書き出す。参考素材の絵は写していない（自作）。
import fs from "fs";
const ROOT = new URL("../../assets-src/pixel-practice/", import.meta.url);
function piece(name, dir, grid, palFile, recolor = {}, frame = 48) {
  const rows = fs.readFileSync(new URL(`${dir}/${grid}`, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const pal = { ...JSON.parse(fs.readFileSync(new URL(`${dir}/${palFile}`, ROOT), "utf8")), ...recolor };
  const keys = Object.keys(pal);
  const h = rows.length, w = Math.max(...rows.map((r) => r.length));
  return {
    name,
    pal: keys.map((k) => [k, pal[k]]),
    build() {
      const g = Array.from({ length: frame }, () => Array(frame).fill(-1));
      const ox = Math.floor((frame - w) / 2), oy = frame - h;   // 横は中央、縦は下そろえ
      rows.forEach((r, y) => [...r].forEach((ch, x) => { const k = keys.indexOf(ch); if (k >= 0) g[oy + y][ox + x] = k; }));
      return g;
    },
  };
}
export const PIECES = [
  // 磨き直した版（assets-src/pixel-practice/r17-polish/。生成の元は tree.py・house3d.py・smallprops.py）
  piece("P1-木", "r17-polish", "tree4.txt", "pal-tree.json"),
  piece("P2-家", "r17-polish", "cottage.txt", "pal-cottage.json", {}, 64),
  piece("P3-家青", "r17-polish", "cottage.txt", "pal-cottage-blue.json", {}, 64),
  piece("P4-家緑", "r17-polish", "cottage.txt", "pal-cottage-green.json", {}, 64),
  piece("P5-岩", "r17-polish", "rock2.txt", "pal-rock2.json"),
  piece("P6-茂み", "r17-polish", "bush2.txt", "pal-bush2.json"),
  piece("P7-屋敷", "r17-polish", "manor4.txt", "pal-manor4.json", {}, 80),
  piece("P8-屋敷青", "r17-polish", "manor4.txt", "pal-manor4-blue.json", {}, 80),
  piece("P9-屋敷緑", "r17-polish", "manor4.txt", "pal-manor4-green.json", {}, 80),
  // 雪の地方の飾り（r17-polish/snow.py で、既存の木・岩・茂みを雪化／枯れ木は一から）
  piece("P10-雪の木", "r17-polish", "tree-snow.txt", "pal-tree-snow.json"),
  piece("P11-枯れ木", "r17-polish", "tree-dead.txt", "pal-tree-dead.json"),
  piece("P12-雪の岩", "r17-polish", "rock-snow.txt", "pal-rock-snow.json"),
  piece("P13-雪の茂み", "r17-polish", "bush-snow.txt", "pal-bush-snow.json"),
  // 砂漠の飾り（r17-polish/desert.py で一から）
  piece("P14-ヤシ", "r17-polish", "palm.txt", "pal-palm.json"),
  piece("P15-サボテン", "r17-polish", "cactus.txt", "pal-cactus.json"),
];
