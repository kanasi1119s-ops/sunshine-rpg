import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// お年寄りの女（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "お年寄りの女"; export const category = "map-character";
export const pal = palFrom({"skin":["#c88a76","#eab094","#f08a8a"],"hair":["#8a8a9e","#aeaec2","#d0d0e0"],"cloth":["#523a86","#7a5cb8","#9c82d8"],"trim":"#efe3c8","accent":"#ffb830","accent2":"#624a93","pants":["#2a3a3a","#6e5646"],"boots":["#221a1a","#2a3a3a"]});
export const frames = makeSheet({"hair":"bun","outfit":"dress","acc":[]});
export const rows = sheetRows(frames);
