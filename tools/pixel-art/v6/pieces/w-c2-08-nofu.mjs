import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 農夫（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "農夫"; export const category = "map-character";
export const pal = palFrom({"skin":["#b06a4c","#dc9a68","#e07a6a"],"hair":["#5a4030","#886040","#b08850"],"cloth":["#8a2c34","#c04448","#e0787a"],"trim":"#efe0bc","accent":"#a88a3a","accent2":"#9a363a","pants":["#2a4a86","#4a76b8"],"boots":["#3a2418","#2a4a86"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["hat"]});
export const rows = sheetRows(frames);
