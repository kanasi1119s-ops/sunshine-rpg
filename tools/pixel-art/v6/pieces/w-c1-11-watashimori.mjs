import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 硝子湖の渡し守（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "硝子湖の渡し守"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#5c5456","#847a7a","#aca4a0"],"cloth":["#2c5462","#4a8090","#78b0b8"],"trim":"#f0eee0","accent":"#e8b030","accent2":"#3b6673","pants":["#6a4a30","#9a7248"],"boots":["#3a2a24","#6a4a30"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["hat"]});
export const rows = sheetRows(frames);
