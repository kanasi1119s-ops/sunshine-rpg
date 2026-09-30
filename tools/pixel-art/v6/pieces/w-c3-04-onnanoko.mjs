import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 町の女の子（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "町の女の子"; export const category = "map-character";
export const pal = palFrom({"skin":["#c88a76","#eab094","#f08a8a"],"hair":["#5a3a6a","#8a5a3a","#b8843c"],"cloth":["#a83a70","#d8609a","#f090b8"],"trim":"#f4ecd8","accent":"#ffb830","accent2":"#ad4d7b","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"twin","outfit":"dress","acc":[]});
export const rows = sheetRows(frames);
