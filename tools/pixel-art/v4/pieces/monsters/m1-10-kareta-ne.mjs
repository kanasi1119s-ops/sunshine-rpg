import { Cv, R } from "../../lib4.mjs";
// 枯れた根: 引き抜かれた古い根が絡まって動き出したもの。うろの目がにぶく光る。
export const name = "枯れた根"; export const category = "monster";
export const pal = { ...R("abcde", "#1a1008", "#a08058", "#5a3a20"), ...R("fgh", "#a03a10", "#ffc050"), z: "#140c06", w: "#ffffff", e: "#0c0604", g: "#7a8a3a" };
const c = new Cv();
c.shadow(16, 30, 13, "z");
const root = (pts, th = 2) => { for (let i = 0; i < pts.length - 1; i++) { c.line(...pts[i], ...pts[i + 1], "b", th); c.line(pts[i][0], pts[i][1] - 1, pts[i + 1][0], pts[i + 1][1] - 1, "d", 1); } };
root([[10, 22], [5, 25], [2, 29]]); root([[13, 24], [11, 28], [7, 29]]); root([[19, 24], [21, 28], [25, 29]]); root([[22, 22], [27, 25], [30, 29]]); root([[16, 25], [16, 29]]);
root([[8, 14], [3, 12], [2, 7]]); root([[24, 14], [29, 11], [29, 6]]);
c.ell(16, 16, 7, 9, "abcde", { dither: true });
root([[13, 8], [11, 3], [8, 1]], 1); root([[18, 8], [20, 3], [24, 2]], 1); root([[16, 7], [16, 2]], 1); c.px(8, 1, "g"); c.px(24, 2, "g"); c.px(16, 1, "g");
c.ell(12, 14, 2, 3, "eeee", { outline: false }); c.ell(20, 14, 2, 3, "eeee", { outline: false });
c.px(12, 13, "w"); c.px(20, 13, "w"); c.px(12, 15, "g"); c.px(13, 15, "g"); c.px(20, 15, "g"); c.px(19, 15, "g");
c.box(13, 20, 19, 21, "eeee", { outline: false }); for (const x of [14, 16, 18]) c.px(x, 20, "d");
c.list([[10, 10, "e"], [10, 11, "e"], [22, 19, "e"], [11, 24, "e"], [21, 11, "d"], [12, 11, "d"]]);
export const rows = c.rows();
