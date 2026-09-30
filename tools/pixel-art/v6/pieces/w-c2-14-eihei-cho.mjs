import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 衛兵長（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "衛兵長"; export const category = "map-character";
export const pal = palFrom({"skin":["#b8705e","#dc9c7c","#e48478"],"hair":["#62627c","#9494b0","#c4c4dc"],"cloth":["#7a1e30","#b03040","#dc5860"],"trim":"#efe3c8","accent":"#f0b030","accent2":"#8d2633","pants":["#3a3650","#5c5674"],"boots":["#1e1a24","#3a3650"]});
export const frames = makeSheet({"hair":"short","outfit":"armor","acc":["beard"]});
export const rows = sheetRows(frames);
