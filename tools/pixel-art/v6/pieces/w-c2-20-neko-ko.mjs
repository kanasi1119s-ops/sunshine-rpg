import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 猫を抱いた子ども（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "猫を抱いた子ども"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47c68","#f0a890","#f68a8a"],"hair":["#4a3226","#7a5236","#a87a4c"],"cloth":["#6a4e98","#9a80cc","#c0a8ec"],"trim":"#fff8ec","accent":"#ffb830","accent2":"#7b66a3","pants":["#5e4a3c","#806858"],"boots":["#3a2418","#5e4a3c"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":[]});
export const rows = sheetRows(frames);
