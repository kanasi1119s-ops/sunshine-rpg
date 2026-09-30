import { Cv, R } from "../../lib4.mjs";
// 鉱石の蜘蛛: 背に紫の鉱石の結晶を生やした蜘蛛。八本の脚で坑道の壁も歩く。
export const name = "鉱石の蜘蛛"; export const category = "monster";
export const pal = { ...R("abcde", "#16101e", "#8a7a98", "#4a3a5a"), ...R("fghij", "#3a1a7a", "#f0d8ff", "#9a4ae0"), z: "#100a18", w: "#ffffff", e: "#08040c", r: "#ff4a5a" };
const c = new Cv();
c.shadow(16, 30, 13, "z");
for (const s of [0, 1]) { const X = (x) => (s ? 31 - x : x);
  c.line(X(12), 18, X(6), 12, "b", 2); c.line(X(6), 12, X(2), 22, "b", 2); c.line(X(2), 22, X(2), 29, "b");
  c.line(X(12), 20, X(5), 21, "b", 2); c.line(X(5), 21, X(4), 29, "b");
  c.line(X(13), 22, X(8), 26, "b", 2); c.line(X(8), 26, X(8), 29, "b");
  c.line(X(14), 15, X(10), 8, "b"); c.line(X(10), 8, X(7), 5, "b"); c.px(X(12), 12, "c"); c.px(X(6), 12, "c"); }
c.ell(16, 20, 8, 6, "abcde", { dither: true });
for (const [pts] of [[[[10, 17], [11, 8], [15, 15]]], [[[17, 15], [21, 7], [23, 16]]], [[[14, 15], [16, 4], [18, 15]]], [[[20, 19], [26, 14], [23, 22]]], [[[12, 20], [7, 15], [9, 22]]]]) c.poly(pts, "fghij", { lx: 0.5 });
c.line(16, 6, 16, 14, "j"); c.line(11, 10, 12, 14, "j"); c.line(21, 9, 21, 14, "h");
c.ell(16, 24, 5, 3, "abcde"); c.px(13, 24, "c");                                                    // 頭
c.eye(12, 23, "r"); c.eye(18, 23, "r"); c.px(15, 22, "r"); c.px(16, 22, "r"); c.px(14, 27, "w"); c.px(18, 27, "w");
c.list([[8, 19, "d"], [9, 18, "d"], [11, 21, "c"], [22, 21, "a"]]);
export const rows = c.rows();
