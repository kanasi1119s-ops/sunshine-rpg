import { cv, ell, box, poly, bline, fillEll, hole } from "../../bkit.mjs";
// すばやさ（羽）のアイコン。ななめの白い羽。完全オリジナル。
export const name = "すばやさ（羽）";
export const category = "icon";
export const pal = { p: "#284060", "1": "#4a7098", "2": "#8ab4d8", "3": "#c8e4f8", "4": "#ffffff", q: "#c8a848", Q: "#f0dc90", D: "#20102a" };
const c = cv();
fillEll(c, 16, 29, 8, 1, "D");
poly(c, [[5, 27], [7, 19], [12, 11], [19, 6], [27, 4], [26, 12], [22, 19], [15, 24], [9, 27]], "p1234");
// 羽ぺんの軸
bline(c, 5, 27, 24, 6, "q"); bline(c, 6, 27, 25, 7, "Q");
// 羽根の筋（切れ込み）
for (const [a, b, d, e2] of [[10, 22, 8, 17], [13, 19, 11, 14], [16, 16, 15, 11], [19, 13, 19, 9], [12, 24, 16, 22], [16, 21, 20, 19], [20, 17, 23, 14]]) bline(c, a, b, d, e2, "1");
for (const [x, y] of [[8, 20], [12, 15], [17, 11], [22, 8]]) c.put(x, y, "4");
export const rows = c.rows();
