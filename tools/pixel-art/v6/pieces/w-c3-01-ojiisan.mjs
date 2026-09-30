import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// お年寄りの男（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "お年寄りの男"; export const category = "map-character";
export const pal = palFrom({"skin":["#b8806c","#dca88a","#e8907a"],"hair":["#4a2a22","#7a4632","#c8c8dc"],"cloth":["#5a3a3a","#7e5a3c","#a07a4a"],"trim":"#e8dcc0","accent":"#ffb830","accent2":"#654830","pants":["#3a3a4e","#585870"],"boots":["#221a1a","#3a3a4e"]});
export const frames = makeSheet({"hair":"bald","outfit":"tunic","acc":["beard"]});
export const rows = sheetRows(frames);
