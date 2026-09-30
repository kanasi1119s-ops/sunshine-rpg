import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 鉱夫（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "鉱夫"; export const category = "map-character";
export const pal = palFrom({"skin":["#a4685a","#d49676","#dc7a70"],"hair":["#4a3a24","#7a6238","#a88a4c"],"cloth":["#404a62","#6a7690","#98a4bc"],"trim":"#efe3c8","accent":"#f0b828","accent2":"#555e73","pants":["#4a4034","#6e6250"],"boots":["#1e1a18","#4a4034"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["band"]});
export const rows = sheetRows(frames);
