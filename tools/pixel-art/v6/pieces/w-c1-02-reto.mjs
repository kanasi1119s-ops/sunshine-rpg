import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// レト（先輩調査員）（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "レト（先輩調査員）"; export const category = "map-character";
export const pal = palFrom({"skin":["#c87a66","#eaa588","#f08a8a"],"hair":["#3e4a68","#62729a","#8fa0c4"],"cloth":["#1e5a5e","#2e8888","#54b4a8"],"trim":"#efe3c8","accent":"#ffb830","accent2":"#256d6d","pants":["#343e52","#4a5a6a"],"boots":["#241c26","#343e52"]});
export const frames = makeSheet({"hair":"short","outfit":"coat","acc":["scarf"]});
export const rows = sheetRows(frames);
