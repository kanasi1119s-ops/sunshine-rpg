import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 砂音の隊商長（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "砂音の隊商長"; export const category = "map-character";
export const pal = palFrom({"skin":["#98603e","#c4865c","#d88a6a"],"hair":["#a88a5c","#d0b484","#ecdcae"],"cloth":["#8a4a26","#c07a30","#e0a848"],"trim":"#fbf6e6","accent":"#e8b030","accent2":"#9a6226","pants":["#4a3a2a","#7a5a3a"],"boots":["#3a2a20","#4a3a2a"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["scarf"]});
export const rows = sheetRows(frames);
