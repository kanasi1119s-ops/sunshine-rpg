import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// MP（星の雫）のアイコン。青いしずくの中に星がひとつ。完全オリジナル。
export const name = "MP（星の雫）";
export const category = "icon";
export const pal = { p: "#0a1440", "1": "#1c3a90", "2": "#3070d8", "3": "#60a8f8", "4": "#b0e4ff", w: "#ffffff", y: "#fff0a0", D: "#20102a" };
const c = cv(); const R = "p1234";
fillEll(c, 16, 28, 7, 1, "D");
poly(c, [[16, 3], [21, 12], [23, 17], [8.5, 17], [11, 12]], R);
ell(c, 16, 19, 8, 8, R);
// 星
const star = [[16, 12], [16, 13], [16, 14], [16, 15], [16, 16], [16, 17], [16, 18], [16, 19], [16, 20], [16, 21], [14, 17], [15, 17], [17, 17], [18, 17], [13, 17], [19, 17], [15, 16], [17, 16], [15, 18], [17, 18]];
for (const [x, y] of star) c.put(x, y + 1, "y"); c.put(16, 18, "w"); c.put(15, 18, "w"); c.put(16, 17, "w");
// ハイライト
c.put(11, 17, "w"); c.put(11, 18, "4"); c.put(12, 15, "4"); c.put(14, 8, "4"); c.put(13, 10, "w");
// きらめき
c.put(25, 7, "y"); c.put(24, 7, "4"); c.put(26, 7, "4"); c.put(25, 6, "4"); c.put(25, 8, "4");
c.put(6, 22, "y"); c.put(5, 22, "4"); c.put(7, 22, "4"); c.put(6, 21, "4"); c.put(6, 23, "4");
export const rows = c.rows();
