import { kNew, kEll, kRect, kPoly, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
// 水筒: 革でできた平たい丸い水筒。コルクせんとかけひも。
export const name = "水筒";
export const category = "item";
export const pal = { o: "#221408", H: "#d89a5c", L: "#b8743c", M: "#8e5228", D: "#5e3418", s: "#f4dca0", c: "#d8b070", C: "#8e6a38", b: "#3a6a9c", B: "#7ab0d8", w: "#ffffff", t: "#e8c888" };
const g = kNew();
// かけひも（本体の後ろのわっか）
for (let x = 3; x <= 31; x++) for (let y = 0; y < 22; y++) { const d = ((x - 16.5) / 12.5) ** 2 + ((y - 13) / 11) ** 2; if (d <= 1 && d >= 0.62) kPut(g, x, y, x < 16 ? "t" : "C"); }
// 本体
kEll(g, 17, 20, 11.5, 10.5, ["H", "L", "L", "M", "D"]);
kEll(g, 17, 20, 8.5, 7.5, ["L", "L", "M", "M", "D"]);
// 波のしるし
for (const [x, y, k] of [[13, 19, "B"], [14, 18, "B"], [15, 19, "b"], [16, 18, "B"], [17, 19, "b"], [18, 18, "B"], [19, 19, "b"], [20, 18, "B"]]) kPut(g, x, y, k);
for (const [x, y, k] of [[14, 22, "B"], [15, 21, "B"], [16, 22, "b"], [17, 21, "B"], [18, 22, "b"], [19, 21, "B"], [20, 22, "b"]]) kPut(g, x, y, k);
// ぬい目
for (let a = 0; a < 24; a++) { const t = (a / 24) * Math.PI * 2; if (a % 2) kPut(g, Math.round(17 + Math.cos(t) * 10), Math.round(20 + Math.sin(t) * 9), "s"); }
// 口とコルク
kRect(g, 14, 7, 19, 10, "M"); kRect(g, 14, 7, 15, 10, "L"); kRect(g, 19, 7, 19, 10, "D");
kRect(g, 14, 3, 19, 6, "c"); kRect(g, 19, 3, 19, 6, "C"); kRect(g, 14, 6, 19, 6, "C"); kRect(g, 14, 3, 15, 3, "s");
const r0 = kOutline(g, { c: "C", C: "C", t: "C", H: "D", L: "D", M: "D", D: "D" }, "o");
for (const [x, y, c] of [[9, 17, "s"], [10, 15, "s"], [11, 14, "s"], [9, 18, "H"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
