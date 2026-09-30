import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 共鳴術士（水紋）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "共鳴術士（水紋）"; export const category = "map-character";
export const pal = palFrom({"skin":["#d08a78","#f0b498","#f08a8a"],"hair":["#16327a","#2a56b0","#4a80d8"],"cloth":["#5a86c8","#98c8ec","#c8ecfa"],"trim":"#efe3c8","accent":"#ffb830","accent2":"#7aa0bd","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"long","outfit":"dress","acc":[]});
export const rows = sheetRows(frames);
