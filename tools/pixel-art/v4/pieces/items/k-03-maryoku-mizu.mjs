import { kNew, kPoly, kRect, kPut, kOutline, kRows } from "../../lib4.mjs";
// 魔力の水: 三角フラスコに青く光る水と、きらめき。
export const name = "魔力の水";
export const category = "item";
export const pal = { o: "#101838", W: "#e8fcff", G: "#a8e4f4", g: "#5ab4dc", b: "#4c8cf0", B: "#2c58c0", d: "#1c3488", h: "#9cd0ff", c: "#a0a8c8", C: "#666c98", w: "#ffffff", s: "#fff6b0" };
const g = kNew();
kRect(g, 13, 8, 18, 15, "G"); kRect(g, 18, 8, 18, 15, "g");
kPoly(g, [[13, 15], [19, 15], [26, 27], [24, 29], [8, 29], [6, 27]], "G");
kPoly(g, [[11, 22], [21, 22], [25, 27], [24, 28], [8, 28], [7, 27]], "b");
kRect(g, 8, 26, 24, 28, "B"); kRect(g, 19, 22, 24, 28, "B"); kRect(g, 21, 26, 24, 28, "d");
kRect(g, 10, 24, 12, 25, "h"); kRect(g, 11, 22, 16, 22, "h"); kRect(g, 13, 23, 15, 23, "h");
kRect(g, 12, 3, 19, 6, "c"); kRect(g, 19, 3, 19, 6, "C"); kRect(g, 13, 7, 18, 7, "C"); kRect(g, 12, 3, 14, 3, "W");
const r0 = kOutline(g, { c: "C", C: "C" }, "o");
for (const [x, y, c] of [[13, 10, "w"], [13, 12, "w"], [12, 17, "w"], [11, 19, "w"], [10, 26, "w"], [16, 25, "W"], [19, 24, "h"], [17, 16, "g"],
  // きらめき
  [26, 8, "s"], [26, 7, "w"], [26, 9, "w"], [25, 8, "w"], [27, 8, "w"], [5, 14, "s"], [5, 13, "w"], [5, 15, "w"], [4, 14, "w"], [6, 14, "w"], [23, 16, "s"], [16, 27, "b"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
