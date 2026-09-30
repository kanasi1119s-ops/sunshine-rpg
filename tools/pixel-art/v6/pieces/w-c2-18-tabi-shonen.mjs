import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 旅の少年（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "旅の少年"; export const category = "map-character";
export const pal = palFrom({"skin":["#cc7c62","#f2ac88","#f4867e"],"hair":["#8a4a1c","#c07a2c","#e8a840"],"cloth":["#2c5c3a","#4a8a50","#78b868"],"trim":"#f4ecd0","accent":"#ffc040","accent2":"#3b6e40","pants":["#6a4a30","#8e6a44"],"boots":["#3a2418","#6a4a30"]});
export const frames = makeSheet({"hair":"spiky","outfit":"tunic","acc":["bag"]});
export const rows = sheetRows(frames);
