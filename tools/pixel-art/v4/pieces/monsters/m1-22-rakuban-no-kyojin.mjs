import { Cv, R } from "../../lib4.mjs";
// 落盤の巨人（小型）: 崩れた坑道の岩が寄り集まって立ち上がった小さな巨人。
export const name = "落盤の巨人"; export const category = "monster";
export const pal = { ...R("abcde", "#1e1c26", "#c0b8b0", "#6a6470"), ...R("fgh", "#5a4a20", "#d8c070"), z: "#14121a", w: "#ffffff", e: "#08060c", y: "#ff9a30", g: "#7a9a5a" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
c.ell(11, 26, 3, 3, "abcde"); c.ell(21, 26, 3, 3, "abcde"); c.box(9, 22, 13, 26, "abcde"); c.box(19, 22, 23, 26, "abcde");     // 足
c.box(4, 15, 8, 22, "abcde"); c.box(24, 15, 28, 22, "abcde");                                                              // 腕
c.ell(6, 24, 4, 4, "abcde", { dither: true }); c.ell(26, 24, 4, 4, "abcde", { dither: true });                            // こぶし
c.ell(16, 17, 8, 7, "abcde", { dither: true });                                                                           // 胴
c.ell(7, 13, 4, 3, "abcde"); c.ell(25, 13, 4, 3, "abcde");                                                                // 肩
c.ell(16, 8, 5, 4, "abcde"); c.poly([[12, 5], [14, 1], [16, 5]], "abcde"); c.poly([[17, 5], [20, 2], [21, 6]], "abcde");
c.box(12, 7, 14, 8, "eeee", { outline: false }); c.box(18, 7, 20, 8, "eeee", { outline: false }); c.px(12, 7, "w"); c.px(18, 7, "w"); c.px(13, 8, "y"); c.px(19, 8, "y"); c.px(14, 8, "y"); c.px(20, 8, "y");
c.line(13, 11, 19, 11, "e"); c.line(14, 12, 18, 12, "d");
c.list([[12, 14, "e"], [13, 15, "e"], [14, 16, "e"], [19, 18, "e"], [16, 21, "e"], [6, 22, "e"], [26, 22, "e"]]);
c.list([[10, 15, "g"], [11, 15, "g"], [22, 13, "g"], [9, 12, "g"]]);
c.list([[3, 28, "b"], [4, 29, "c"], [28, 28, "b"], [29, 29, "c"], [1, 27, "c"], [30, 26, "c"]]);
export const rows = c.rows();
