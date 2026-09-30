import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 画家（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "画家"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47c64","#e8a888","#f08a8a"],"hair":["#5a3818","#8a5a28","#b88440"],"cloth":["#b8a488","#e0d0b0","#f4e8cc"],"trim":"#efe3c8","accent":"#ffb830","accent2":"#b3a68d","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["cap"]});
export const rows = sheetRows(frames);
