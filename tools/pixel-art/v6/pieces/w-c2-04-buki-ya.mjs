import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 武器屋の主（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "武器屋の主"; export const category = "map-character";
export const pal = palFrom({"skin":["#b0685a","#dc9878","#e87c74"],"hair":["#4a2a24","#70402c","#9a6238"],"cloth":["#4a2e2a","#7a4e3a","#a87850"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#623e2e","pants":["#3e3a52","#5c566e"],"boots":["#1e1a24","#3e3a52"]});
export const frames = makeSheet({"hair":"short","outfit":"apron","acc":["beard"]});
export const rows = sheetRows(frames);
