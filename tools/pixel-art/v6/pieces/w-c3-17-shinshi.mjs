import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 貴族の紳士（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "貴族の紳士"; export const category = "map-character";
export const pal = palFrom({"skin":["#c47c64","#e8a888","#f08a8a"],"hair":["#3a2a2e","#5a4448","#8a7478"],"cloth":["#1e2848","#34406e","#54649a"],"trim":"#f6f2ff","accent":"#ffc040","accent2":"#2a3358","pants":["#3a3a4a","#5a5a6e"],"boots":["#141018","#3a3a4a"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["hat"]});
export const rows = sheetRows(frames);
