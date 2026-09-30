import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 船頭（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "船頭"; export const category = "map-character";
export const pal = palFrom({"skin":["#b0705a","#d8946c","#e4806c"],"hair":["#5c5c74","#8c8ca6","#bcbcd0"],"cloth":["#22346a","#3a5aa0","#5e86cc"],"trim":"#f4f0e4","accent":"#ffc040","accent2":"#2e4880","pants":["#4a4658","#6c6680"],"boots":["#221c1c","#4a4658"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["cap"]});
export const rows = sheetRows(frames);
