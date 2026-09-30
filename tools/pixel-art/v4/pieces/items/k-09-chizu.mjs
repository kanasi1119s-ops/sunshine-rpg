import { kNew, kPoly, kRect, kPut, kOutline, kRows, kLine, kEll } from "../../lib4.mjs";
// 地図: 4つに折りたたんだ古い地図を、ななめに広げたところ。海・陸・道・赤い×印。
export const name = "地図";
export const category = "item";
export const pal = { o: "#3a2418", P: "#f4e4b4", p: "#dcc890", q: "#b89c64", u: "#7ec0d0", U: "#4c94b0", g: "#8cb060", G: "#5a8440", r: "#a86a3c", x: "#d02c34", X: "#ff7a6c", i: "#6a4a2c", w: "#ffffff" };
const g = kNew();
kRect(g, 4, 6, 27, 27, "P");
// 折り目
kRect(g, 15, 6, 15, 27, "p"); kRect(g, 4, 16, 27, 16, "p");
kRect(g, 4, 26, 27, 27, "q"); kRect(g, 26, 6, 27, 27, "q");
// 海
kRect(g, 6, 8, 12, 14, "u"); kRect(g, 6, 8, 12, 8, "U"); kRect(g, 20, 20, 25, 25, "u"); kRect(g, 20, 25, 25, 25, "U");
// 陸
kEll(g, 17, 14, 7, 5, "g"); kEll(g, 13, 21, 5, 4, "g");
kRect(g, 12, 16, 14, 17, "g");
for (const [x, y] of [[20, 13], [21, 14], [19, 15], [17, 17], [15, 18]]) kPut(g, x, y, "G");
for (const [x, y] of [[15, 11], [16, 10], [17, 11], [16, 12], [13, 20], [14, 21]]) kPut(g, x, y, "G");
// 道（点線）
for (const [x, y] of [[9, 24], [11, 23], [13, 24], [15, 22], [17, 20], [19, 18], [21, 17]]) kPut(g, x, y, "r");
// ×印
kLine(g, 21, 8, 24, 11, "x"); kLine(g, 24, 8, 21, 11, "x"); kPut(g, 21, 8, "X");
const r0 = kOutline(g, { P: "q", p: "q", q: "i", u: "i", U: "i" }, "o");
for (const [x, y, c] of [[5, 7, "w"], [6, 7, "w"], [5, 8, "w"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
