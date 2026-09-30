import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// ドルン（暗躍する仲介人）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "ドルン（暗躍する仲介人）"; export const category = "map-character";
export const pal = palFrom({"skin":["#b8907c","#dcb49e","#f08a8a"],"hair":["#26263a","#3a3a54","#54547a"],"cloth":["#181828","#2a2a40","#3e3e5a"],"trim":"#f0ecf4","accent":"#e0b848","accent2":"#222233","pants":["#22222e","#34344a"],"boots":["#221a1a","#22222e"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["hat"]});
export const rows = sheetRows(frames);
