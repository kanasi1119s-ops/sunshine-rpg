import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// ミナ（麦香野の少女）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "ミナ（麦香野の少女）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f09aa0"],"hair":["#8a6028","#b8862e","#e0b048"],"cloth":["#3e7a3c","#5ea450","#88cc70"],"trim":"#fbf3dc","accent":"#ffb830","accent2":"#4b8340","pants":["#8a6a48","#c0a070"],"boots":["#5a3a2a","#8a6a48"]});
export const frames = makeSheet({"hair":"twin","outfit":"dress","acc":[]});
export const rows = sheetRows(frames);
