import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 学者（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "学者"; export const category = "map-character";
export const pal = palFrom({"skin":["#c88a7c","#f0b8a0","#f4a09c"],"hair":["#5c2c38","#8a4448","#b8645a"],"cloth":["#3e6458","#6a9a84","#9cc8ae"],"trim":"#fbf6ea","accent":"#e0a838","accent2":"#557b6a","pants":["#4a3e50","#6a5e70"],"boots":["#2a2030","#4a3e50"]});
export const frames = makeSheet({"hair":"short","outfit":"robe","acc":["glasses"]});
export const rows = sheetRows(frames);
