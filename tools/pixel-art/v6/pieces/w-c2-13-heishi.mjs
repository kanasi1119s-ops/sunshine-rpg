import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 兵士（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "兵士"; export const category = "map-character";
export const pal = palFrom({"skin":["#c4786a","#eca88a","#f28a86"],"hair":["#4a5070","#7480a0","#a8b4d0"],"cloth":["#7a2030","#b03848","#d86068"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#8d2d3a","pants":["#3e3a52","#5e5874"],"boots":["#1c1820","#3e3a52"]});
export const frames = makeSheet({"hair":"short","outfit":"armor","acc":["cap"]});
export const rows = sheetRows(frames);
