import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 料理人（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "料理人"; export const category = "map-character";
export const pal = palFrom({"skin":["#b87458","#dc9c78","#e88070"],"hair":["#2a1e22","#3e2c30","#5a4448"],"cloth":["#2e5a3a","#4a8a50","#78b070"],"trim":"#f0ecf4","accent":"#ffb830","accent2":"#3b6e40","pants":["#3a3a4a","#585868"],"boots":["#1a1418","#3a3a4a"]});
export const frames = makeSheet({"hair":"bald","outfit":"apron","acc":["cap"]});
export const rows = sheetRows(frames);
