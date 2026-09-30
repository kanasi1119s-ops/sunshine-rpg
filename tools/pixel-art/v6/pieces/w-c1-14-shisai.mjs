import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 霧断崖の司祭（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "霧断崖の司祭"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#7a8ea8","#a6bad0","#cadbea"],"cloth":["#222c46","#34425e","#4c5e80"],"trim":"#f6f8fc","accent":"#e0b048","accent2":"#2a354b","pants":["#4a3a3a","#6e5646"],"boots":["#1c2030","#4a3a3a"]});
export const frames = makeSheet({"hair":"short","outfit":"robe","acc":[]});
export const rows = sheetRows(frames);
