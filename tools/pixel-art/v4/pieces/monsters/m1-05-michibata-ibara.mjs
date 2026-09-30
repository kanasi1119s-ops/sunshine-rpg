import { Cv, R } from "../../lib4.mjs";
// 道端の茨: トゲだらけのツルが絡まって動く。黄色い目が茂みの奥で光る。
export const name = "道端の茨"; export const category = "monster";
export const pal = { ...R("abcde", "#0e1a14", "#7ab848"), ...R("fgh", "#d8d0a0", "#fffbe8"), ...R("jk", "#7a1030", "#e84060"), z: "#0c1410", w: "#ffffff", y: "#ffd830", e: "#1a1408" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
const vine = (pts) => { for (let i = 0; i < pts.length - 1; i++) c.line(...pts[i], ...pts[i + 1], "a", 3); for (let i = 0; i < pts.length - 1; i++) c.line(pts[i][0] + 1, pts[i][1], pts[i + 1][0] + 1, pts[i + 1][1], "c"); };
vine([[15, 26], [8, 19], [6, 12], [10, 5]]); vine([[17, 26], [24, 18], [26, 10], [22, 4]]); vine([[16, 24], [14, 14], [16, 6]]);
vine([[12, 27], [4, 26], [2, 22]]); vine([[20, 27], [28, 26], [29, 21]]);
c.ell(16, 23, 9, 6, "abcde", { dither: true });
for (const [x, y] of [[6, 15], [7, 10], [9, 6], [10, 20], [25, 14], [26, 9], [23, 5], [24, 21], [14, 12], [15, 8], [3, 25], [29, 24]]) { c.px(x - 2, y - 1, "g"); c.px(x - 1, y, "f"); c.px(x + 3, y + 1, "g"); c.px(x + 2, y + 1, "f"); }
c.list([[9, 27, "g"], [23, 27, "g"], [13, 19, "g"], [19, 19, "g"]]);
c.box(11, 21, 14, 23, "eeee", { outline: false }); c.box(18, 21, 21, 23, "eeee", { outline: false });
c.eye(12, 21, "y"); c.eye(19, 21, "y"); c.line(13, 26, 19, 26, "e"); for (const x of [14, 16, 18]) c.px(x, 26, "h");
c.ell(24, 25, 1, 1, "jk"); c.ell(8, 25, 1, 1, "jk");
export const rows = c.rows();
