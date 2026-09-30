import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 密輸組織の元締め（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "密輸組織の元締め"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#8a6c3c","#b8985a","#dcc080"],"cloth":["#1a3a38","#2c5a52","#448a78"],"trim":"#f0e8d0","accent":"#ffb830","accent2":"#234842","pants":["#2c221e","#4a3a34"],"boots":["#241a18","#2c221e"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["beard"]});
export const rows = sheetRows(frames);
