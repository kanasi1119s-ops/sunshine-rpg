import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// エドレア（合議会代表）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "エドレア（合議会代表）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#e8a0b0"],"hair":["#7a80a0","#a8b0ce","#d4daee"],"cloth":["#2c1a66","#46309a","#6a52c0"],"trim":"#efe8f8","accent":"#e0a830","accent2":"#38267b","pants":["#4a3a3a","#6e5646"],"boots":["#241a3a","#4a3a3a"]});
export const frames = makeSheet({"hair":"long","outfit":"robe","acc":[]});
export const rows = sheetRows(frames);
