import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 合議会の使者（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "合議会の使者"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#2c2a44","#44405e","#5e5a80"],"cloth":["#38286e","#54409a","#7862c4"],"trim":"#f4f0fa","accent":"#e0b048","accent2":"#43337b","pants":["#6e6a88","#a8a4bc"],"boots":["#2a2030","#6e6a88"]});
export const frames = makeSheet({"hair":"short","outfit":"robe","acc":[]});
export const rows = sheetRows(frames);
