import { Cv, R } from "../../lib4.mjs";
// 錆の蟲: 鉱山の錆をまとった甲虫。横向きで、大きな角と赤茶けた殻を持つ。
export const name = "錆の蟲"; export const category = "monster";
export const pal = { ...R("abcde", "#2a0e08", "#f0904a", "#a83a1a"), ...R("fgh", "#3a3038", "#8a7a88"), z: "#1a0e0a", w: "#ffffff", e: "#0e0604", y: "#ffe860", g: "#5a8a50" };
const c = new Cv();
c.shadow(16, 30, 12, "z");
for (const [x0, x1] of [[10, 7], [15, 14], [21, 24]]) { c.line(x0, 24, x1, 27, "f", 1); c.line(x1, 27, x1 - 1, 29, "f"); }
c.ell(17, 20, 11, 8, "abcde", { dither: true });                                         // 殻
c.line(17, 12, 17, 27, "a"); c.line(17, 12, 22, 13, "a");
c.list([[12, 16, "b"], [13, 17, "a"], [21, 20, "a"], [22, 21, "b"], [24, 24, "a"], [10, 21, "a"], [11, 22, "a"], [14, 25, "b"]]);
c.list([[9, 18, "g"], [10, 18, "g"], [20, 15, "g"], [23, 19, "g"], [18, 26, "g"]]);
c.ell(6, 21, 4, 4, "fghh");                                                              // 頭
c.poly([[3, 19], [0, 12], [5, 17]], "fghh"); c.poly([[5, 16], [4, 10], [8, 16]], "fghh");    // 角
c.poly([[3, 24], [0, 27], [5, 26]], "fghh");
c.eye(5, 20, "y"); c.px(7, 22, "e");
c.list([[16, 13, "d"], [15, 13, "d"], [14, 14, "d"], [9, 24, "e"]]);
export const rows = c.rows();
