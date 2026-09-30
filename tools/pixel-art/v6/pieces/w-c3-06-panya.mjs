import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// パン屋（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "パン屋"; export const category = "map-character";
export const pal = palFrom({"skin":["#d08470","#f2ac90","#f47a80"],"hair":["#5a3420","#8a5a30","#b88448"],"cloth":["#8a5a3a","#b08050","#d0a870"],"trim":"#e6def0","accent":"#ffb830","accent2":"#8d6640","pants":["#5a4a5a","#7a6a78"],"boots":["#221a1a","#5a4a5a"]});
export const frames = makeSheet({"hair":"short","outfit":"apron","acc":["cap"]});
export const rows = sheetRows(frames);
