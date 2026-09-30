import { kNew, kEll, kRect, kPoly, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
// 金貨: 大きな金貨。ふちに刻みがあり、星のしるしがある。うしろに1まいかさなる。
export const name = "金貨";
export const category = "item";
export const pal = { o: "#3a2408", X: "#fff6b8", A: "#ffd84c", a: "#e0a628", b: "#b07418", d: "#7a4a10", w: "#ffffff", c: "#c88c20", e: "#8a5c14" };
const g = kNew();
// うしろの金貨
kEll(g, 20, 14, 10.5, 10.5, ["A", "a", "a", "b", "d"]);
kEll(g, 20, 14, 8, 8, ["a", "a", "b"]);
// 手前の金貨
kEll(g, 13, 19, 11.5, 11.5, ["X", "A", "A", "a", "b"]);
// うち側のふちの線
for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) { const d = Math.hypot(x - 13, y - 19); if (d >= 8.2 && d < 9.4 && g[y][x] !== ".") g[y][x] = x + y < 32 ? "b" : "d"; }
for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) { const d = Math.hypot(x - 13, y - 19); if (d < 8.2 && d >= 0) g[y][x] = (x + y < 30 ? "A" : "a"); }
for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) { const d = Math.hypot(x - 13, y - 19); if (d < 8.2 && x + y > 36) g[y][x] = "c"; }
// 星（四方）
const S = [[13, 13], [13, 14], [13, 15], [13, 16], [13, 22], [13, 23], [13, 24], [13, 25], [7, 19], [8, 19], [9, 19], [10, 19], [16, 19], [17, 19], [18, 19], [19, 19]];
kPoly(g, [[13, 12], [15, 17], [20, 19], [15, 21], [13, 26], [11, 21], [6, 19], [11, 17]], "e");
kPoly(g, [[13, 13], [14.5, 17.5], [18, 19], [14.5, 20.5], [13, 25], [11.5, 20.5], [8, 19], [11.5, 17.5]], "X");
const r0 = kOutline(g, { X: "b", A: "d", a: "d", b: "d", c: "d", d: "d", e: "d" }, "o");
for (const [x, y, c] of [[6, 13, "w"], [7, 12, "w"], [8, 11, "X"], [5, 15, "X"], [13, 18, "w"], [13, 19, "w"], [24, 8, "X"], [25, 9, "X"], [23, 8, "w"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
