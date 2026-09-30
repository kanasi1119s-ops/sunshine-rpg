import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// アヤメ（霜原の案内人）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "アヤメ（霜原の案内人）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#161e3c","#242e56","#3a4880"],"cloth":["#2c4488","#4468b8","#6a90dc"],"trim":"#f4f0e8","accent":"#ffb830","accent2":"#365393","pants":["#4a3a3a","#6e5646"],"boots":["#2a2a44","#4a3a3a"]});
export const frames = makeSheet({"hair":"long","outfit":"coat","acc":[]});
export const rows = sheetRows(frames);
