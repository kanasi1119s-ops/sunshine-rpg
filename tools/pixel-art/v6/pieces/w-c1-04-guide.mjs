import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// ガイド（商人の息子）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "ガイド（商人の息子）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#8a6c3c","#b8985a","#dcc080"],"cloth":["#7a5030","#a4743c","#c89a58"],"trim":"#f6ecd0","accent":"#ffb830","accent2":"#835d30","pants":["#3a4a48","#56706a"],"boots":["#3a2a2a","#3a4a48"]});
export const frames = makeSheet({"hair":"short","outfit":"tunic","acc":["band","bag"]});
export const rows = sheetRows(frames);
