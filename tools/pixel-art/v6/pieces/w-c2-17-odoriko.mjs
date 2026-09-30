import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 踊り子（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "踊り子"; export const category = "map-character";
export const pal = palFrom({"skin":["#7a4030","#a86040","#e0687a"],"hair":["#282848","#403c68","#5c58a0"],"cloth":["#a02c78","#d04a98","#f078bc"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#a63b7a","pants":["#4a3a3a","#6e5646"],"boots":["#6a4030","#4a3a3a"]});
export const frames = makeSheet({"hair":"pony","outfit":"dress","acc":["band"]});
export const rows = sheetRows(frames);
