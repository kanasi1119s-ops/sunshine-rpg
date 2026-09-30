import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 神官（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "神官"; export const category = "map-character";
export const pal = palFrom({"skin":["#c07a76","#eaa88e","#f2969a"],"hair":["#8a88a8","#b4b2cc","#dcdaea"],"cloth":["#9c94cc","#d4d0ee","#f0eefc"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#aaa6be","pants":["#4a3a3a","#6e5646"],"boots":["#6a4a3a","#4a3a3a"]});
export const frames = makeSheet({"hair":"short","outfit":"robe","acc":[]});
export const rows = sheetRows(frames);
