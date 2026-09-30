import { makeSheet, palFrom, sheetRows } from "../lib6.mjs";
// 図書館員（マップ用 16×24・4方向×3コマ）。色は v4 の同名の絵から。
export const name = "図書館員"; export const category = "map-character";
export const pal = palFrom({"skin":["#c48a76","#e8b094","#f08a8a"],"hair":["#2e2842","#463c62","#66588a"],"cloth":["#2e6a66","#4a9a90","#7ac4b4"],"trim":"#efe3c8","accent":"#ffc040","accent2":"#3b7b73","pants":["#2a3050","#44507a"],"boots":["#181420","#2a3050"]});
export const frames = makeSheet({"hair":"bob","outfit":"coat","acc":["glasses"]});
export const rows = sheetRows(frames);
