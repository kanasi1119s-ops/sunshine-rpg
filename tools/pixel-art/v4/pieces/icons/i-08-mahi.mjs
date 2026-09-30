import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// まひ のアイコン。黄色いいなずまと火花。完全オリジナル。
export const name = "まひ";
export const category = "icon";
export const pal = { p: "#3a2408", "1": "#a06a10", "2": "#e8b020", "3": "#ffe050", "4": "#fffbb8", b: "#5a8af0", B: "#b8d8ff", D: "#20102a" };
const c = cv();
fillEll(c, 16, 29, 8, 1, "D");
poly(c, [[15, 2], [26, 2], [19, 12], [25, 12], [11, 30], [14, 17], [7, 17]], "p1234");
bline(c, 22, 4, 17, 11, "4"); bline(c, 15, 4, 10, 15, "3");
// 火花
for (const [x, y] of [[4, 6], [27, 22], [4, 24], [27, 8]]) { c.put(x, y, "B"); c.put(x - 1, y, "b"); c.put(x + 1, y, "b"); c.put(x, y - 1, "b"); c.put(x, y + 1, "b"); }
export const rows = c.rows();
