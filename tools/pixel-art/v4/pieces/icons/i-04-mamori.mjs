import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// まもり（盾）のアイコン。青い盾に金のふち。完全オリジナル。
export const name = "まもり（盾）";
export const category = "icon";
export const pal = { p: "#1a1030", "1": "#1c2c78", "2": "#3050c0", "3": "#5c86f0", "4": "#a4c4ff", g: "#7a5010", G: "#c89028", h: "#ffd860", H: "#fff4b0", w: "#ffffff", D: "#20102a" };
const c = cv();
fillEll(c, 16, 29, 8, 1, "D");
poly(c, [[5, 4], [27, 4], [27, 16], [23, 23], [16, 28], [9, 23], [5, 16]], "pgGhH");
poly(c, [[8, 7], [24, 7], [24, 15], [21, 21], [16, 25], [11, 21], [8, 15]], "p1234");
// 中の紋（金の星の十字）
for (let y = 9; y <= 22; y++) { c.put(16, y, "G"); c.put(15, y, "h"); }
for (let x = 10; x <= 22; x++) { c.put(x, 14, "G"); c.put(x, 13, "h"); }
c.put(15, 13, "H"); c.put(16, 14, "g");
for (const x of [10, 22]) c.put(x, 14, "1");
c.put(9, 8, "w"); c.put(10, 8, "w"); c.put(9, 9, "4");
export const rows = c.rows();
