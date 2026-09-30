import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 鍛冶屋（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "鍛冶屋"; export const category = "map-character";
export const pal = palFrom({"skin":["#6a3a30","#8c5240","#c05850"],"hair":["#1e2030","#343850","#4c5270"],"cloth":["#5a3220","#8a5230","#b47c48"],"trim":"#e8dcc0","accent":"#ffc040","accent2":"#6e4226","pants":["#3a3450","#5c5470"],"boots":["#1c161c","#3a3450"]});
export const frames = makeSheet({"hair":"bald","outfit":"apron","acc":["band"]});
export const rows = sheetRows(frames);
