import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 旅の剣士（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "旅の剣士"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47c64","#e6a688","#f08a8a"],"hair":["#3a2e40","#5e4438","#8a6448"],"cloth":["#22307a","#3a56b0","#5c82d8"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#2e458d","pants":["#3a3448","#584e68"],"boots":["#1e1620","#3a3448"]});
export const frames = makeSheet({"hair":"short","outfit":"armor","acc":["scarf"]});
export const rows = sheetRows(frames);
