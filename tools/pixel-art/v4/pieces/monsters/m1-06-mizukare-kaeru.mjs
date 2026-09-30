import { Cv, R } from "../../lib4.mjs";
// 水涸れの蛙: 干上がった池で育った、ひび割れた肌のカエル。
export const name = "水涸れの蛙"; export const category = "monster";
export const pal = { ...R("abcde", "#2a2a14", "#c8c078", "#7a8a3a"), ...R("fgh", "#8a7a48", "#f0e6b0"), z: "#1e1a10", w: "#ffffff", e: "#1a1208", y: "#e8b030", n: "#5a2a1a" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
c.ell(6, 25, 4, 4, "abcde"); c.ell(26, 25, 4, 4, "abcde");                        // 後ろ足
c.ell(16, 21, 10, 7, "abcde", { dither: true });                                   // 体
c.ell(16, 25, 6, 3, "fgh", { outline: false });                                    // おなか
c.ell(10, 27, 3, 2, "abcd"); c.ell(22, 27, 3, 2, "abcd");                          // 前足
for (const x of [10, 22]) { c.ell(x, 13, 3, 3, "abcde"); c.ell(x, 13, 2, 2, "hhhh", { outline: false }); c.box(x - 1, 12, x, 14, "yyyy", { outline: false }); c.px(x - 1, 12, "w"); c.px(x, 14, "e"); c.px(x - 1, 13, "e"); }
c.line(7, 22, 25, 22, "a"); c.line(8, 23, 9, 23, "a"); c.line(23, 23, 24, 23, "a");    // 口
c.list([[12, 19, "n"], [13, 20, "n"], [14, 20, "n"], [19, 17, "n"], [20, 18, "n"], [20, 19, "n"], [21, 20, "n"], [9, 25, "a"], [10, 26, "a"], [14, 24, "n"]]);
c.list([[14, 17, "e"], [17, 17, "e"], [16, 15, "d"], [15, 16, "d"]]);
c.list([[12, 15, "d"], [13, 16, "d"], [18, 16, "d"], [19, 15, "d"]]);
export const rows = c.rows();
