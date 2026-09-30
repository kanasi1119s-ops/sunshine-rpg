import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 静滅教団の信者（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "静滅教団の信者"; export const category = "map-character";
export const pal = palFrom({"skin":["#d8b8a0","#f0d4bc","#f08a8a"],"hair":["#161222","#241c38","#362a52"],"cloth":["#221a3c","#32285a","#56478e"],"trim":"#cfc8e0","accent":"#ffb830","accent2":"#282048","pants":["#4a3a3a","#6e5646"],"boots":["#0e0a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"short","outfit":"robe","acc":["hood"]});
export const rows = sheetRows(frames);
