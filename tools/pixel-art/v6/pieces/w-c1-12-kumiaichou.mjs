import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 鉄鏈の組合長（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "鉄鏈の組合長"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#6e3c26","#9a5a34","#c48046"],"cloth":["#303a50","#465268","#66748c"],"trim":"#d8d4c4","accent":"#e8b030","accent2":"#384253","pants":["#3e3244","#5c4c62"],"boots":["#2a2028","#3e3244"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["beard"]});
export const rows = sheetRows(frames);
