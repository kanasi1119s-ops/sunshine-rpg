import { Cv, R, rng } from "../../lib4.mjs";
// 歪みの小塊: 歪んだ灯り石からにじみ出た黒紫の塊。ひとつ目。
export const name = "歪みの小塊"; export const category = "monster";
export const pal = { ...R("abcde", "#100820", "#7a3a9a"), ...R("fgh", "#a01a6a", "#ff7ac0"), z: "#0c0616", w: "#ffffff", e: "#2a0a3a", v: "#f0e0ff" };
const c = new Cv(); const r = rng(7);
c.shadow(16, 30, 11, "z");
c.ell(16, 22, 10, 7, "abcde", { dither: true }); c.ell(9, 24, 5, 4, "abcde"); c.ell(23, 23, 5, 5, "abcde");
c.poly([[9, 18], [11, 9], [14, 17]], "abcde"); c.poly([[19, 16], [23, 8], [24, 18]], "abcde"); c.poly([[14, 16], [16, 11], [18, 16]], "abcde");
c.ell(16, 21, 4, 4, "vvvvv", { outline: false }); c.ell(16, 21, 4, 4, "eeeee", { outline: false });
c.ell(16, 21, 3, 3, "vvvvv", { outline: false }); c.px(15, 22, "g"); c.px(16, 22, "g"); c.px(15, 21, "f"); c.px(16, 20, "e"); c.px(17, 22, "f"); c.px(15, 23, "h");
c.px(14, 19, "w"); c.px(15, 19, "w");
c.line(10, 24, 12, 26, "f"); c.line(21, 25, 23, 27, "f"); c.line(11, 17, 12, 20, "g"); c.line(21, 19, 22, 17, "g");
for (const x of [7, 12, 19, 25]) { c.px(x, 28, "a"); c.px(x, 29, "a"); }
c.line(5, 26, 4, 28, "b");
export const rows = c.rows();
