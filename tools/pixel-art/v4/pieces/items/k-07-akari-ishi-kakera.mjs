import { kNew, kPoly, kPut, kOutline, kRows } from "../../lib4.mjs";
// 灯り石のかけら: 欠けた小さな青い石が、ころがっている。
export const name = "灯り石のかけら";
export const category = "item";
export const pal = { o: "#141c4c", W: "#f0ffff", h: "#b0ecff", b: "#5cc0ec", B: "#3884d8", d: "#2450b0", D: "#1a3084", s: "#fff8c0", z: "#8ca0e8", w: "#ffffff" };
const g = kNew();
kPoly(g, [[10, 12], [17, 10], [23, 14], [22, 21], [16, 24], [9, 20]], "b");
kPoly(g, [[10, 12], [17, 10], [16, 24], [9, 20]], "h");
kPoly(g, [[17, 10], [23, 14], [22, 21], [16, 24]], "B");
kPoly(g, [[22, 21], [16, 24], [18, 19]], "d");
// 小さなかけら
kPoly(g, [[6, 24], [9, 22], [11, 25], [8, 28]], "B"); kPoly(g, [[6, 24], [9, 22], [8, 28]], "b");
kPoly(g, [[23, 24], [26, 23], [27, 26], [24, 27]], "d"); kPoly(g, [[23, 24], [26, 23], [24, 27]], "B");
const r0 = kOutline(g, { h: "z", b: "D", B: "D", d: "D" }, "o");
for (const [x, y, c] of [[12, 13, "w"], [12, 14, "W"], [13, 12, "W"], [7, 24, "h"], [24, 24, "b"], [18, 17, "s"], [18, 16, "w"], [18, 18, "w"], [17, 17, "w"], [19, 17, "w"], [11, 19, "b"], [20, 13, "b"], [15, 19, "B"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
