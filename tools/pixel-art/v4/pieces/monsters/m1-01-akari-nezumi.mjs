import { Cv, R } from "../../lib4.mjs";
// 灯り鼠: 尻尾の先に小さな灯り石をぶら下げた、痩せたネズミ。横向き。
export const name = "灯り鼠"; export const category = "monster";
export const pal = { ...R("abcde", "#1e1420", "#a08a86"), ...R("fghi", "#5a2a3a", "#e8a89a"), ...R("jklm", "#a04a10", "#fff2a0"), z: "#160e1c", w: "#ffffff", r: "#e04030", t: "#3a2a30" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
c.line(24, 22, 28, 18, "t", 2); c.line(28, 18, 27, 12, "t", 2); // 尻尾
c.ell(27, 10, 2, 2, "jklm"); c.px(26, 9, "m"); c.px(27, 10, "l");                // 灯り石
c.ell(9, 16, 2, 3, "abcde"); c.px(9, 16, "g");                                    // 耳
c.ell(16, 22, 8, 5, "abcde", { dither: true });                                   // 胴
c.ell(20, 27, 2, 2, "abcd"); c.ell(12, 27, 2, 2, "abcd"); c.ell(8, 28, 1, 1, "abcd"); // 足
c.ell(9, 21, 4, 4, "abcde");                                                      // 頭
c.poly([[6, 20], [1, 25], [7, 25]], "abcde");                                     // 鼻づら
c.px(2, 24, "r"); c.px(3, 24, "h");                                               // 鼻
c.eye(8, 19, "r"); c.line(6, 26, 9, 26, "w");                                     // 目と歯
c.list([[14, 20, "c"], [15, 19, "d"], [18, 21, "b"], [17, 25, "b"], [13, 24, "b"], [22, 24, "a"]]);
c.line(12, 18, 12, 18, "d");
export const rows = c.rows();
