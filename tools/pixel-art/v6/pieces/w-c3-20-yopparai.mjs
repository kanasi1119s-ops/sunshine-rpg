import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 酔っぱらい（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "酔っぱらい"; export const category = "map-character";
export const pal = palFrom({"skin":["#c86a58","#e88a70","#e84e50"],"hair":["#6a5648","#8e7a66","#b0a08a"],"cloth":["#6a4a30","#8a6a44","#b08c5a"],"trim":"#f0ecdc","accent":"#ffb830","accent2":"#6e5536","pants":["#5a4a3a","#7a6a54"],"boots":["#2a2018","#5a4a3a"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":[]});
export const rows = sheetRows(frames);
