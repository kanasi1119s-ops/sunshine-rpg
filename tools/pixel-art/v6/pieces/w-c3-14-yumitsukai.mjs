import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 弓使い（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "弓使い"; export const category = "map-character";
export const pal = palFrom({"skin":["#c48068","#e8aa88","#f08a8a"],"hair":["#5a3818","#8a5a28","#b88440"],"cloth":["#2e6a34","#4a9a48","#78c060"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#3b7b3a","pants":["#4a3a30","#6e5a44"],"boots":["#3a2416","#4a3a30"]});
export const frames = makeSheet({"hair":"pony","outfit":"tunic","acc":["band"]});
export const rows = sheetRows(frames);
