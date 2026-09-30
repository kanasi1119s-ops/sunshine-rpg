import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 修道女（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "修道女"; export const category = "map-character";
export const pal = palFrom({"skin":["#c8867a","#f0b09a","#f4988e"],"hair":["#3c2a20","#8a5a38","#b88050"],"cloth":["#302c5c","#4c4888","#7470b4"],"trim":"#f8f4ec","accent":"#ffc040","accent2":"#3d3a6d","pants":["#4a3a3a","#6e5646"],"boots":["#2a2030","#4a3a3a"]});
export const frames = makeSheet({"hair":"bun","outfit":"robe","acc":["hood"]});
export const rows = sheetRows(frames);
