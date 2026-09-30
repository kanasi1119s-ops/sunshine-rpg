import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 漁師（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "漁師"; export const category = "map-character";
export const pal = palFrom({"skin":["#9c5a44","#c4805a","#d86a5a"],"hair":["#4a4a5e","#787a90","#a8aabc"],"cloth":["#2a4478","#4a72b0","#e8f0f8"],"trim":"#dce8f0","accent":"#e8a838","accent2":"#3b5b8d","pants":["#3a5a4a","#587a64"],"boots":["#2a2018","#3a5a4a"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["cap"]});
export const rows = sheetRows(frames);
