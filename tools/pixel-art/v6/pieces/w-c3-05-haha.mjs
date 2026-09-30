import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 赤ん坊を抱く母（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "赤ん坊を抱く母"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47a64","#e6a488","#f08a8a"],"hair":["#6a4020","#986030","#c48a44"],"cloth":["#8a3a2a","#b85a3a","#d8805a"],"trim":"#f6f0dc","accent":"#ffb830","accent2":"#93482e","pants":["#2a3a4a","#6e5646"],"boots":["#221a1a","#2a3a4a"]});
export const frames = makeSheet({"hair":"bun","outfit":"dress","acc":[]});
export const rows = sheetRows(frames);
