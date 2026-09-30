import { Cv, R } from "../../lib4.mjs";
// 硝子の魚: 体が透きとおった硝子のような魚。中の骨が見える。
export const name = "硝子の魚"; export const category = "monster";
export const pal = { ...R("abcde", "#24507a", "#f4ffff", "#8ad4ec"), ...R("fgh", "#2a4a6a", "#8ac0e0"), z: "#10202e", w: "#ffffff", e: "#0c1a2a", r: "#f05a6a", y: "#ffe070" };
const c = new Cv();
c.shadow(16, 30, 11, "z");
c.poly([[24, 18], [31, 9], [30, 18], [31, 27]], "abcde", { lx: 0.2 });                // 尾びれ
c.poly([[12, 11], [16, 5], [22, 11]], "abcde"); c.poly([[14, 25], [17, 29], [21, 24]], "abcde");    // 背びれ・腹びれ
c.ell(14, 18, 12, 7, "abcde", { dither: true });                                      // 体
c.line(11, 18, 24, 18, "g"); for (let x = 13; x <= 22; x += 3) { c.line(x, 18, x + 1, 14, "g"); c.line(x, 18, x + 1, 22, "g"); }   // 中の骨
c.list([[9, 21, "g"], [10, 22, "g"], [8, 23, "b"]]);
c.poly([[14, 19], [20, 22], [16, 24]], "fghhh", { lx: 0.2 });                        // むなびれ
c.ell(8, 16, 3, 3, "hhhh"); c.ell(8, 16, 3, 3, "fghhh", { outline: true }); c.eye(7, 15, "r"); c.px(9, 17, "e");
c.line(2, 19, 4, 20, "e"); c.line(3, 18, 3, 18, "g");
c.list([[27, 5, "h"], [28, 3, "w"], [3, 8, "h"], [4, 5, "w"], [5, 10, "w"]]);
c.list([[10, 13, "w"], [11, 12, "w"], [12, 12, "w"], [16, 14, "y"]]);
export const rows = c.rows();
