import { Cv, R } from "../../lib4.mjs";
// 迷い火: 道に迷わせるゆらめく炎。うつろな顔がある。
export const name = "迷い火"; export const category = "monster";
export const pal = { ...R("abcdef", "#5a1020", "#fff4b0", "#e8602a"), ...R("ghij", "#1a1040", "#5a4aa0"), z: "#1c1236", w: "#ffffff", e: "#2a0a10", n: "#ff8a4a" };
const c = new Cv();
c.ell(16, 30, 9, 0, "gg", { outline: false }); c.shadow(16, 30, 8, "h");
c.poly([[16, 2], [11, 12], [9, 19], [23, 19], [21, 12]], "abcdef", { lx: 0.2 });
c.ell(16, 21, 8, 7, "abcdef", { lx: 0.3, dither: true });
c.poly([[16, 10], [13, 16], [12, 21], [20, 21], [19, 16]], "bcdef", { outline: false, lx: 0.2, ly: 0.3 });
c.poly([[6, 12], [4, 20], [8, 20]], "abcdef"); c.poly([[26, 9], [24, 19], [28, 19]], "abcdef");
c.box(11, 17, 13, 22, "eeee", { outline: false }); c.box(18, 17, 20, 22, "eeee", { outline: false });
c.px(11, 17, "w"); c.px(18, 17, "w"); c.px(12, 21, "n"); c.px(19, 21, "n");
c.line(14, 25, 17, 25, "e"); c.px(13, 24, "e"); c.px(18, 24, "e");
export const rows = c.rows();
