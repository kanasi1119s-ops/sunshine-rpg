import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 宿屋の女将（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "宿屋の女将"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47468","#eea48a","#f27c84"],"hair":["#7a3c22","#a85a30","#d08040"],"cloth":["#2c5658","#4a8a86","#7ac0b0"],"trim":"#f8f0e0","accent":"#ffb830","accent2":"#3b6e6b","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"bun","outfit":"apron","acc":[]});
export const rows = sheetRows(frames);
