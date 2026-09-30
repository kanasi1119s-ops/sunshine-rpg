import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 麦香野の村長（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "麦香野の村長"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#a8802c","#d0a848","#ecc860"],"cloth":["#5e7028","#88983c","#b0c060"],"trim":"#fbf8ee","accent":"#e8b838","accent2":"#6d7a30","pants":["#5a3a22","#8a5a34"],"boots":["#3a2a1e","#5a3a22"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["beard"]});
export const rows = sheetRows(frames);
