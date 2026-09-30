import { kNew, kEll, kRect, kPoly, kPut, kOutline, kRows, kLine, kClean } from "../../lib4.mjs";
// パン: 焼きたての丸いパン。切れ目が3本。
export const name = "パン";
export const category = "item";
export const pal = { o: "#2e1608", H: "#f8c878", L: "#e09c4c", M: "#bc7430", D: "#8a4c1e", d: "#5e3014", c: "#fff0cc", C: "#f0d8a0", w: "#ffffff", f: "#fbe8c0" };
const g = kNew();
kEll(g, 16, 18, 13, 10, ["H", "L", "L", "M", "D"]);
kEll(g, 16, 25, 10, 3, ["M", "D"]);
kRect(g, 6, 22, 26, 27, "D");
// パンの形を整える（下をふくらませる）
kEll(g, 16, 20, 13, 8.5, ["L", "M", "M", "D"]);
kEll(g, 16, 16.5, 12, 8, ["H", "L", "L", "M", "D"]);
// 切れ目
for (const [x0, y0] of [[9, 12], [15, 10], [21, 12]]) { kLine(g, x0, y0 + 2, x0 + 3, y0, "c"); kLine(g, x0, y0 + 3, x0 + 3, y0 + 1, "C"); kLine(g, x0 + 1, y0 + 4, x0 + 4, y0 + 2, "M"); }
// こんがり色のなじませ
for (const [x, y] of [[8, 16], [12, 18], [18, 19], [23, 17], [14, 14], [20, 15], [10, 20], [22, 21]]) kPut(g, x, y, "M");
for (const [x, y] of [[8, 14], [11, 17], [24, 15]]) kPut(g, x, y, "L");
// 粉
for (const [x, y] of [[13, 8], [19, 9]]) kPut(g, x, y, "f");
const r0 = kOutline(g, { H: "D", L: "d", M: "d", D: "d" }, "o");
for (const [x, y, c] of [[9, 9, "w"], [10, 8, "w"], [8, 10, "H"], [11, 8, "H"]]) kPut(r0, x, y, c);
export const rows = kClean(kRows(r0));
