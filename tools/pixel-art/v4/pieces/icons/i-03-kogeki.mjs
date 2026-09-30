import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// こうげき（剣）のアイコン。斜めの剣。完全オリジナル。
export const name = "こうげき（剣）";
export const category = "icon";
export const pal = { p: "#141826", "1": "#4a5470", "2": "#8490b0", "3": "#c4ccdc", "4": "#f4f8ff", g: "#6a4a12", G: "#c8902c", h: "#ffd860", r: "#6a2a20", R: "#a4483a", D: "#20102a" };
const c = cv(); const ST = "p1234", GD = "pgGhh";
fillEll(c, 16, 29, 9, 1, "D");
// 刃（左下から右上へ）
poly(c, [[9.5, 21], [12, 23.5], [26.5, 8.5], [27, 4.5], [23, 5]], ST);
bline(c, 12, 20, 24, 8, "4"); bline(c, 13, 20, 25, 8, "4"); bline(c, 12, 21, 25, 8, "3"); bline(c, 13, 21, 26, 8, "3");
// つば（刃と直角）
for (const [a, b, d, e2, ch] of [[6, 18, 13, 25, "p"], [7, 18, 14, 25, "G"], [6, 19, 13, 26, "g"]]) { bline(c, a, b, d, e2, ch); bline(c, a + 1, b, d + 1, e2, ch); }
for (const [x, y] of [[8, 20], [10, 22], [12, 24]]) c.put(x, y, "h");
// つか
bline(c, 9, 25, 5, 29, "R"); bline(c, 10, 25, 6, 29, "r"); bline(c, 8, 25, 4, 29, "p"); bline(c, 9, 26, 5, 30, "r"); bline(c, 8, 26, 4, 30, "p");
ell(c, 4, 29, 1.2, 1.2, GD);
c.put(24, 6, "4"); c.put(26, 5, "4");
export const rows = c.rows();
