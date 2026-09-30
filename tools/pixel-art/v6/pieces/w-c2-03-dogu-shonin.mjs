import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 道具屋の商人（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "道具屋の商人"; export const category = "map-character";
export const pal = palFrom({"skin":["#8c5038","#b87a52","#e07868"],"hair":["#2c2a3e","#4a4460","#6a6488"],"cloth":["#a04a1c","#d07030","#f0a050"],"trim":"#f4ecd8","accent":"#ffc040","accent2":"#a65a26","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"short","outfit":"apron","acc":["bag"]});
export const rows = sheetRows(frames);
