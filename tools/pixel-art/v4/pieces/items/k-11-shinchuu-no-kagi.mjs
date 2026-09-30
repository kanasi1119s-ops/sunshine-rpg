import { kNew, kEll, kRect, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
// 真鍮の鍵: 三つ葉の飾りの持ち手と、ななめの軸。
export const name = "真鍮の鍵";
export const category = "item";
export const pal = { o: "#2c1c10", X: "#fff4b0", A: "#f0cc50", a: "#c8942c", b: "#8c5c1c", d: "#5c3a14", w: "#ffffff" };
const g = kNew();
const R = ["X", "A", "A", "a", "b"];
kEll(g, 9.5, 9.5, 7, 7, R);
kEll(g, 16.5, 4.5, 3.6, 3.6, R); kEll(g, 4.5, 16.5, 3.6, 3.6, R);
// 穴
for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) if ((x - 9.5) ** 2 + (y - 9.5) ** 2 <= 9) g[y][x] = ".";
// 軸
for (const [ox, oy, c] of [[-1, 0, "A"], [0, 0, "A"], [1, 0, "a"], [0, 1, "a"], [0, -1, "X"]]) kLine(g, 14 + ox, 14 + oy, 26 + ox, 26 + oy, c);
kLine(g, 13, 15, 25, 27, "b");
// つば（軸の飾りの輪）
kRect(g, 16, 16, 19, 19, "a"); kRect(g, 16, 16, 17, 17, "X"); kRect(g, 18, 18, 19, 19, "b"); kPut(g, 17, 18, "A"); kPut(g, 18, 17, "A");
// ひげ（歯）
kRect(g, 20, 24, 22, 26, "a"); kRect(g, 19, 27, 21, 29, "a"); kRect(g, 23, 25, 24, 27, "b"); kRect(g, 20, 24, 21, 24, "A");
kRect(g, 25, 27, 28, 29, "a"); kRect(g, 25, 27, 26, 27, "A"); kRect(g, 27, 28, 28, 29, "b");
kPut(g, 21, 29, "b"); kPut(g, 20, 29, "b");
const r0 = kOutline(g, { X: "b", A: "d", a: "d", b: "d" }, "o");
for (const [x, y, c] of [[6, 5, "w"], [7, 4, "w"], [5, 6, "w"], [15, 3, "w"], [3, 15, "w"], [15, 15, "X"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
