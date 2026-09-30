import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// HP（ハート）のアイコン。24×24ほどを中央に。完全オリジナル。
export const name = "HP（ハート）";
export const category = "icon";
export const pal = { p: "#3a0818", "1": "#801030", "2": "#c02048", "3": "#ee4a68", "4": "#ff9aa8", w: "#ffffff", D: "#20102a" };
const c = cv(); const R = "p1234";
fillEll(c, 16, 27, 8, 1, "D");
ell(c, 11, 12, 6, 6, R); ell(c, 21, 12, 6, 6, R);
poly(c, [[5.5, 14], [26.5, 14], [16, 27]], R);
// 谷のなじませ
for (let x = 13; x <= 19; x++) for (let y = 11; y <= 15; y++) if (c.get(x, y) === "p" && y >= 13) c.put(x, y, "2");
c.put(16, 10, "1"); c.put(15, 11, "1"); c.put(17, 11, "1");
// ハイライト
c.put(9, 9, "w"); c.put(10, 8, "w"); c.put(8, 10, "w"); c.put(9, 8, "4");
export const rows = c.rows();
