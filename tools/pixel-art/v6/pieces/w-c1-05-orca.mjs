import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// オルカ（元鉱夫）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "オルカ（元鉱夫）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#5a5458","#8a8488","#c0bcc0"],"cloth":["#402a20","#5e3e2a","#7a5638"],"trim":"#efe3c8","accent":"#d8a840","accent2":"#4b3222","pants":["#4a4e5a","#6a7080"],"boots":["#2a2224","#4a4e5a"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["band"]});
export const rows = sheetRows(frames);
