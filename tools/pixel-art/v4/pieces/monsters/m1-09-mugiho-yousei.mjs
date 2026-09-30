import { Cv, R } from "../../lib4.mjs";
// 麦穂の妖精: 麦の穂を冠にしたいたずら好きの小さな妖精。舌を出している。
export const name = "麦穂の妖精"; export const category = "monster";
export const pal = { ...R("abcde", "#6a3a10", "#fff0a0", "#e0a020"), ...R("fghi", "#3a6a2a", "#b8e070"), ...R("jklm", "#5a80b0", "#f0fcff"), ...R("nop", "#a06040", "#ffe0c0"), z: "#1a1a10", w: "#ffffff", e: "#2a1a20", t: "#f0506a" };
const c = new Cv();
c.shadow(16, 30, 5, "z");
c.poly([[12, 18], [3, 10], [1, 17], [5, 24], [12, 23]], "jklm", { lx: 0.5 }); c.poly([[20, 18], [29, 10], [31, 17], [27, 24], [20, 23]], "jklm", { lx: 0.5 });
c.line(12, 19, 4, 12, "k"); c.line(20, 19, 28, 12, "k");
c.ell(16, 22, 4, 5, "fghi");                                                        // 服
c.line(14, 27, 13, 29, "n"); c.line(18, 27, 19, 29, "n"); c.px(12, 29, "o"); c.px(20, 29, "o");
c.ell(16, 13, 5, 5, "nop");                                                         // 頭
for (const [x, y, s] of [[16, 3, 0], [12, 5, 0], [20, 5, 0], [9, 8, 1], [23, 8, 1]]) { c.ell(x, y + 1, 1, 2, "abcde"); c.line(x, y + 3, 16, 9, "g"); }  // 麦穂の冠
c.eye(12, 12, "f"); c.eye(18, 12, "f"); c.px(11, 11, "e"); c.px(20, 11, "e");
c.line(13, 16, 18, 16, "e"); c.px(17, 17, "t"); c.px(18, 17, "t"); c.px(18, 18, "t");
c.px(10, 15, "o"); c.px(22, 15, "o");
c.line(9, 20, 6, 24, "n"); c.line(23, 20, 26, 22, "n"); c.line(26, 22, 26, 17, "g"); c.ell(26, 15, 1, 2, "abcde");
export const rows = c.rows();
