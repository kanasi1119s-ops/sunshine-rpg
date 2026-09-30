import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 吟遊詩人（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "吟遊詩人"; export const category = "map-character";
export const pal = palFrom({"skin":["#c88a86","#f0b8a4","#f4929a"],"hair":["#8a5a24","#c08a3a","#e6bc5c"],"cloth":["#3e2c8c","#6a4ac4","#9678ec"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#553b9d","pants":["#1e5a3a","#38904e"],"boots":["#4a2a1a","#1e5a3a"]});
export const frames = makeSheet({"hair":"pony","outfit":"coat","acc":["hat"]});
export const rows = sheetRows(frames);
