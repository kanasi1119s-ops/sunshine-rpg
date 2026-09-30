import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 貴族の令嬢（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "貴族の令嬢"; export const category = "map-character";
export const pal = palFrom({"skin":["#d8988a","#f8c4ac","#f08a8a"],"hair":["#b88418","#e0b030","#f8d858"],"cloth":["#a04a96","#d878c0","#f4a4dc"],"trim":"#f4ecd8","accent":"#ffc040","accent2":"#ad609a","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"long","outfit":"dress","acc":[]});
export const rows = sheetRows(frames);
