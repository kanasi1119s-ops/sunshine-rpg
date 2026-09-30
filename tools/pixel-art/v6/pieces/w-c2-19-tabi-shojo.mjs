import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 旅の少女（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "旅の少女"; export const category = "map-character";
export const pal = palFrom({"skin":["#bc786e","#e8a68e","#f68a90"],"hair":["#242c58","#3c4a86","#5c72b8"],"cloth":["#9a5a18","#dc9424","#f8c848"],"trim":"#fcf6e6","accent":"#ffc040","accent2":"#b0761d","pants":["#5a4a6c","#847496"],"boots":["#2a1c20","#5a4a6c"]});
export const frames = makeSheet({"hair":"twin","outfit":"tunic","acc":["bag"]});
export const rows = sheetRows(frames);
