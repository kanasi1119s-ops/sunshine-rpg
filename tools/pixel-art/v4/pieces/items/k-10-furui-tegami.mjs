import { kNew, kPoly, kRect, kPut, kOutline, kRows, kLine, kEll } from "../../lib4.mjs";
// 古い手紙: 封筒。ふたの三角と、ろうの封。すみが少しやぶれている。
export const name = "古い手紙";
export const category = "item";
export const pal = { o: "#2c2030", P: "#f0e4c8", p: "#d8c8a0", q: "#b0a078", Q: "#8c7c58", t: "#9a2c48", T: "#e0708c", d: "#601a34", w: "#ffffff", s: "#8878a0" };
const g = kNew();
kRect(g, 3, 8, 28, 25, "P");
kRect(g, 3, 23, 28, 25, "p"); kRect(g, 27, 8, 28, 25, "p");
// ふた（三角）
kPoly(g, [[3, 8], [28, 8], [16, 19]], "p");
kPoly(g, [[5, 9], [26, 9], [16, 17]], "P");
// 下の折り目
kLine(g, 3, 25, 12, 17, "q"); kLine(g, 28, 25, 19, 17, "q");
kLine(g, 3, 8, 16, 19, "q"); kLine(g, 28, 8, 16, 19, "q");
// しみ
for (const [x, y] of [[7, 21], [8, 21], [8, 22], [22, 22], [23, 22], [24, 21]]) kPut(g, x, y, "q");
// やぶれた角
kRect(g, 26, 24, 28, 25, "."); kPut(g, 25, 25, "."); kPut(g, 28, 23, ".");
const r0 = kOutline(g, { P: "Q", p: "Q", q: "Q" }, "o");
// 封ろう
kRect(r0, 14, 16, 18, 20, "t"); kRect(r0, 13, 17, 19, 19, "t"); kRect(r0, 18, 17, 19, 20, "d"); kRect(r0, 14, 20, 18, 20, "d");
kPut(r0, 14, 16, "T"); kPut(r0, 13, 17, "T"); kPut(r0, 14, 17, "T");
kPut(r0, 16, 18, "T"); kPut(r0, 15, 18, "T");
for (const [x, y, c] of [[5, 10, "w"], [6, 10, "w"], [4, 11, "w"], [8, 12, "P"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
