import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// ミナの幼なじみ（歪みの少年）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "ミナの幼なじみ（歪みの少年）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f09aa0"],"hair":["#6e4a2c","#966a3c","#c09050"],"cloth":["#7a5a30","#a07c40","#d0a858"],"trim":"#fff4d0","accent":"#ffb830","accent2":"#806333","pants":["#48405a","#6a5a70"],"boots":["#3a2a44","#48405a"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":[]});
export const rows = sheetRows(frames);
