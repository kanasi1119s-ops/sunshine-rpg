import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 郵便配達（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "郵便配達"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47a64","#e8a688","#f08a8a"],"hair":["#3e2c22","#5e4434","#846448"],"cloth":["#1e3a7a","#2e5cb8","#5a8ae0"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#254a93","pants":["#2a3a6a","#4a5c9a"],"boots":["#1a1420","#2a3a6a"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["cap","bag"]});
export const rows = sheetRows(frames);
