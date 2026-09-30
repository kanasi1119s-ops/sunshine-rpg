import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 霜原の番所の守り（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "霜原の番所の守り"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87868","#e89a86","#ee7c88"],"hair":["#6a7488","#9aa4b8","#c8d0e0"],"cloth":["#2e4468","#4a6a96","#7a9ac0"],"trim":"#f2f6fa","accent":"#ffb830","accent2":"#3b5578","pants":["#3a2e34","#5a4a48"],"boots":["#2a2430","#3a2e34"]});
export const frames = makeSheet({"hair":"short","outfit":"armor","acc":["cap"]});
export const rows = sheetRows(frames);
