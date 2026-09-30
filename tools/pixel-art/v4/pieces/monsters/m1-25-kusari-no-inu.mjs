import { Cv, R } from "../../lib4.mjs";
// 鎖につながれた犬: 首輪の鎖を引きずる、痩せた黒い犬。横向きでうなっている。
export const name = "鎖につながれた犬"; export const category = "monster";
export const pal = { ...R("abcde", "#100c14", "#9a8a90", "#4a3a44"), ...R("fgh", "#4a4a5a", "#d0d0e0"), z: "#0e0a12", w: "#ffffff", e: "#08060c", r: "#e0402a", t: "#c03a4a" };
const c = new Cv();
c.shadow(16, 30, 13, "z");
c.poly([[24, 16], [30, 9], [28, 19]], "abcde");                                          // しっぽ
c.box(22, 23, 24, 29, "abcd"); c.box(19, 23, 21, 29, "abcd"); c.box(8, 23, 10, 29, "abcd"); c.box(12, 23, 14, 29, "abcd");   // 足
c.ell(16, 19, 9, 5, "abcde", { dither: true });                                          // 胴
c.line(12, 17, 12, 21, "b"); c.line(15, 17, 15, 21, "b"); c.line(18, 17, 18, 21, "b");   // あばら
c.ell(8, 14, 4, 4, "abcde"); c.poly([[6, 15], [1, 17], [1, 20], [6, 20]], "abcde"); c.poly([[8, 11], [7, 6], [11, 10]], "abcde"); c.poly([[12, 12], [13, 7], [15, 12]], "abcde");   // 頭・鼻づら・耳
c.line(2, 19, 6, 19, "e"); for (const x of [2, 4]) c.px(x, 20, "w"); c.px(6, 20, "w"); c.px(1, 17, "e");
c.eye(7, 12, "r"); c.line(6, 11, 9, 12, "e");
c.box(6, 16, 12, 17, "fgh", { outline: false }); c.px(6, 17, "g");                       // 首輪
c.line(7, 18, 5, 24, "g"); for (const [x, y] of [[6, 19], [5, 22], [5, 25]]) c.box(x, y, x + 1, y + 1, "fgh"); for (let x = 6; x <= 26; x += 3) c.box(x, 28, x + 1, 29, "fgh"); c.ell(28, 28, 2, 2, "fgh"); c.px(28, 28, "e");
c.list([[13, 15, "c"], [16, 15, "c"], [19, 16, "d"], [22, 17, "b"], [12, 25, "a"]]);
export const rows = c.rows();
