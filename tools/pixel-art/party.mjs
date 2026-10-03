// 主要キャラクター5人の立ち絵（104×104の枠・下そろえ・横は中央）。元は assets-src/pixel-practice/r18-chars/ の
// 描画エンジン（chargen.py）で作った文字グリッド（1文字=1色）。色は50〜60色なので「長い色番号」形式で書き出す。
import fs from "fs";
const ROOT = new URL("../../assets-src/pixel-practice/r18-chars/", import.meta.url);
function piece(name, grid, palFile) {
  const rows = fs.readFileSync(new URL(grid, ROOT), "utf8").split("\n").filter((l) => l !== "");
  const pal = JSON.parse(fs.readFileSync(new URL(palFile, ROOT), "utf8"));
  const keys = Object.keys(pal);
  const frame = 104, h = rows.length, w = Math.max(...rows.map((r) => r.length));
  return {
    name,
    pal: keys.map((k) => [k, pal[k]]),
    build() {
      const g = Array.from({ length: frame }, () => Array(frame).fill(-1));
      const ox = Math.floor((frame - w) / 2), oy = frame - h;
      rows.forEach((r, y) => [...r].forEach((ch, x) => { const k = keys.indexOf(ch); if (k >= 0) g[oy + y][ox + x] = k; }));
      return g;
    },
  };
}
export const PIECES = [
  piece("C1-ユーリ", "yuri4.txt", "pal-yuri4.json"),
  piece("C2-レト", "reto1.txt", "pal-reto1.json"),
  piece("C3-ミナ", "mina2.txt", "pal-mina2.json"),
  piece("C4-ガイド", "guide2.txt", "pal-guide2.json"),
  piece("C5-オルカ", "orca2.txt", "pal-orca2.json"),
];
