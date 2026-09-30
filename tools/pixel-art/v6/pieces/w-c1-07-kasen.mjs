import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// カセン（灯里支部長）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "カセン（灯里支部長）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#66463c","#8e6a56","#b8a090"],"cloth":["#661a30","#922a44","#bc4a5c"],"trim":"#f6ecdc","accent":"#e0a830","accent2":"#752236","pants":["#4a3a4a","#6a5468"],"boots":["#2a1e26","#4a3a4a"]});
export const frames = makeSheet({"hair":"bob","outfit":"coat","acc":[]});
export const rows = sheetRows(frames);
