import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 薬屋（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "薬屋"; export const category = "map-character";
export const pal = palFrom({"skin":["#c48870","#e8b090","#f08a8a"],"hair":["#3a2e42","#5a4a5c","#7e6c7c"],"cloth":["#2e6a4a","#4a9a68","#78c890"],"trim":"#e4e0f0","accent":"#ffb830","accent2":"#3b7b53","pants":["#4a4a5a","#6a6a7a"],"boots":["#221a1a","#4a4a5a"]});
export const frames = makeSheet({"hair":"bob","outfit":"apron","acc":["bag"]});
export const rows = sheetRows(frames);
