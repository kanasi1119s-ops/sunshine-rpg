import { Cv, R } from "../../lib4.mjs";
// トロッコの機械兵: トロッコに上半身が組みこまれた古い鉱山の機械。ツルハシを構える。
export const name = "トロッコの機械兵"; export const category = "monster";
export const pal = { ...R("abcde", "#1a1c2a", "#c8d0e0", "#5a6688"), ...R("fgh", "#3a1a10", "#c87a4a"), ...R("ij", "#6a4a2a", "#d8b070"), z: "#12141e", w: "#ffffff", e: "#080a12", y: "#ffa030", r: "#a03a2a" };
const c = new Cv();
c.shadow(16, 30, 14, "z");
c.line(2, 29, 30, 29, "a");
c.box(12, 5, 19, 11, "abcde"); c.box(13, 7, 18, 9, "eeee", { outline: false }); c.px(13, 7, "w"); c.box(15, 8, 18, 9, "yyyy", { outline: false }); c.px(15, 8, "w");    // 頭とバイザー
c.line(15, 5, 15, 2, "b"); c.px(15, 1, "r");
c.box(10, 12, 21, 20, "abcde");                                                       // 胴
c.list([[12, 14, "e"], [13, 14, "e"], [18, 16, "e"], [19, 16, "e"], [15, 17, "y"], [16, 17, "y"]]);
c.box(6, 12, 9, 19, "abcde"); c.box(22, 12, 25, 19, "abcde");                         // 腕
c.line(27, 6, 25, 20, "j", 2); c.poly([[22, 5], [30, 4], [30, 7], [27, 7]], "abcde");  // ツルハシ
c.box(4, 20, 27, 27, "fgh"); c.box(4, 20, 27, 21, "abcde");                            // トロッコ
for (const x of [7, 12, 17, 22, 26]) c.px(x, 24, "e"); for (const x of [8, 14, 19, 24]) c.px(x, 22, "h");
c.list([[6, 26, "r"], [9, 25, "r"], [20, 26, "r"], [24, 25, "r"], [5, 22, "g"]]);
for (const x of [9, 23]) { c.ell(x, 27, 3, 3, "abcde"); c.px(x, 27, "e"); c.px(x - 1, 26, "d"); }
c.ell(9, 28, 0, 0, "a");
export const rows = c.rows();
