import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 共鳴術士（火照）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "共鳴術士（火照）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47c64","#e8aa8a","#f08a8a"],"hair":["#a02818","#d84a20","#f88030"],"cloth":["#8a1e28","#c03a30","#e8663a"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#9a2e26","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"spiky","outfit":"tunic","acc":["scarf"]});
export const rows = sheetRows(frames);
