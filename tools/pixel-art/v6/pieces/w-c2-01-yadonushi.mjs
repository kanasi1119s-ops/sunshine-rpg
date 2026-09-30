import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 宿屋の主人（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "宿屋の主人"; export const category = "map-character";
export const pal = palFrom({"skin":["#b8686a","#e0987a","#e87878"],"hair":["#5a4a52","#8a7c82","#b8aeb0"],"cloth":["#5c3428","#8c5a3c","#b88054"],"trim":"#f4ecdc","accent":"#ffc040","accent2":"#704830","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"bald","outfit":"apron","acc":["beard"]});
export const rows = sheetRows(frames);
