import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// ユーリ（16歳の新人調査員）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "ユーリ（16歳の新人調査員）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#5a3122","#8a4a2a","#b06a38"],"cloth":["#232a6a","#34489a","#5670c8"],"trim":"#efe3c8","accent":"#d08a28","accent2":"#2a3a7b","pants":["#544a5c","#7a6a62"],"boots":["#2a1c24","#544a5c"]});
export const frames = makeSheet({"hair":"spiky","outfit":"tunic","acc":["bag"]});
export const rows = sheetRows(frames);
