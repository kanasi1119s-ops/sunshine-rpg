import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 占い師（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "占い師"; export const category = "map-character";
export const pal = palFrom({"skin":["#c48a76","#e6ac90","#f08a8a"],"hair":["#3a2a5a","#563a86","#7a56b0"],"cloth":["#3a2a7a","#5a44a8","#7a66c8"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#483686","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"long","outfit":"robe","acc":["hood"]});
export const rows = sheetRows(frames);
