import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// どく のアイコン。緑の毒のしずくにドクロ。完全オリジナル。
export const name = "どく";
export const category = "icon";
export const pal = { p: "#1a0830", "1": "#3a1a6a", "2": "#5a9a2a", "3": "#8ad03c", "4": "#d0ff80", v: "#9a40d8", V: "#d090ff", w: "#f4f0e0", e: "#1a0830", D: "#20102a" };
const c = cv(); const G = "p1234".replace("1", "1");
fillEll(c, 16, 29, 8, 1, "D");
const R = "p" + "2" + "2" + "3" + "4";
poly(c, [[16, 3], [21, 11], [24, 17], [8, 17], [11, 11]], "p2334");
ell(c, 16, 19, 9, 8, "p2334");
// ドクロ
ell(c, 16, 18, 4, 4, "1wwww"); box(c, 14, 21, 18, 24, "1wwww");
c.put(14, 18, "e"); c.put(15, 18, "e"); c.put(14, 19, "e"); c.put(17, 18, "e"); c.put(18, 18, "e"); c.put(18, 19, "e"); c.put(16, 20, "1");
for (const x of [15, 17]) c.put(x, 23, "1");
// あわ
ell(c, 25, 9, 2, 2, "pvVVV"); ell(c, 7, 8, 1.5, 1.5, "pvVVV"); ell(c, 26, 22, 1.5, 1.5, "pvVVV");
c.put(12, 13, "4"); c.put(11, 15, "4");
export const rows = c.rows();
