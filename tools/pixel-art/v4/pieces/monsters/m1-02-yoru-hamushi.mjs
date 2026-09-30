import { Cv, R } from "../../lib4.mjs";
// 夜の羽虫: 大きな翅に光る目玉もようを持つ、夜の虫。正面。
export const name = "夜の羽虫"; export const category = "monster";
export const pal = { ...R("abcde", "#140c2c", "#8a78d8"), ...R("fghi", "#2a2050", "#c8b8f8"), ...R("jkl", "#c06a10", "#fff090"), z: "#120a22", w: "#ffffff", r: "#f04a5a", v: "#0c0618" };
const c = new Cv();
c.shadow(16, 30, 7, "z");
const wing = (s) => { const X = (x) => (s ? 31 - x : x); return [[X(12), 11], [X(3), 3], [X(1), 12], [X(3), 21], [X(9), 25], [X(13), 21]]; };
for (const s of [0, 1]) { c.poly(wing(s), "abcde", { lx: 0.5 }); const X = (x) => (s ? 31 - x : x);
  c.ell(X(6), 13, 2, 3, "jkl"); c.px(X(5), 11, "w"); c.px(X(6), 13, "v");           // 目玉もよう
  c.line(X(12), 12, X(4), 5, "b"); c.line(X(12), 15, X(3), 14, "b"); c.line(X(12), 19, X(6), 23, "b"); }
c.ell(16, 19, 3, 7, "fghi");                                                        // 胴
for (let y = 16; y <= 24; y += 3) c.line(14, y, 18, y, "f");
c.ell(16, 10, 4, 4, "fghi");                                                        // 頭
c.line(14, 7, 10, 2, "f"); c.line(18, 7, 22, 2, "f"); c.px(10, 2, "l"); c.px(22, 2, "l");
c.eye(13, 9, "r"); c.eye(17, 9, "r"); c.px(15, 13, "w"); c.px(17, 13, "w");
c.line(14, 27, 12, 29, "f"); c.line(18, 27, 20, 29, "f");
export const rows = c.rows();
