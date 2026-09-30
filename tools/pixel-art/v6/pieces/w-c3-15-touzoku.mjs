import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 盗賊（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "盗賊"; export const category = "map-character";
export const pal = palFrom({"skin":["#b87860","#dca486","#f08a8a"],"hair":["#1e2440","#2e3660","#46508a"],"cloth":["#2a2a3c","#44445c","#62628a"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#36364a","pants":["#2a2a3a","#46465c"],"boots":["#141018","#2a2a3a"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["hood"]});
export const rows = sheetRows(frames);
