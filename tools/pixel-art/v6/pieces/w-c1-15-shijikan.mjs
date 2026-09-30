import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 写字官（碑文の下働き）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "写字官（碑文の下働き）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#5e3024","#84482e","#a86a40"],"cloth":["#48485a","#6c6c80","#9494a6"],"trim":"#ece6d4","accent":"#e0b048","accent2":"#565666","pants":["#6e5a3c","#a8946a"],"boots":["#2a2224","#6e5a3c"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["glasses"]});
export const rows = sheetRows(frames);
