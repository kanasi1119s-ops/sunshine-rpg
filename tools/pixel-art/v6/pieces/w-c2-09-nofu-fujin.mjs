import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 農婦（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "農婦"; export const category = "map-character";
export const pal = palFrom({"skin":["#bc7a5c","#e4a884","#f0847e"],"hair":["#62341e","#8e5028","#b8783c"],"cloth":["#6a2c48","#a84a66","#d47490"],"trim":"#f6efdc","accent":"#c8983a","accent2":"#863b52","pants":["#4a3a3a","#6e5646"],"boots":["#221a1a","#4a3a3a"]});
export const frames = makeSheet({"hair":"bun","outfit":"dress","acc":["band"]});
export const rows = sheetRows(frames);
