import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 町の男の子（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "町の男の子"; export const category = "map-character";
export const pal = palFrom({"skin":["#cc8462","#f0aa84","#f08a8a"],"hair":["#7a4a1a","#b0742a","#d8a040"],"cloth":["#c05820","#e88a30","#f8b04a"],"trim":"#efe3c8","accent":"#ffb830","accent2":"#ba6e26","pants":["#3a4a7a","#5670a8"],"boots":["#221a1a","#3a4a7a"]});
export const frames = makeSheet({"hair":"spiky","outfit":"tunic","acc":[]});
export const rows = sheetRows(frames);
