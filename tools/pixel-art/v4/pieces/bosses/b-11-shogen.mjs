import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 初源の歪み（裏ボス）。灯の環が砕けて最初に生まれた歪みの一滴。目をたくさん持つ巨大な闇のしずく。完全オリジナル。
export const name = "初源の歪み";
export const category = "boss";
export const pal = { p: "#0c0618", "1": "#2a1250", "2": "#4a2286", "3": "#7440c0", "4": "#a878f0", m: "#ff40b0", M: "#ffa0e0", c: "#20e0d0", C: "#c0fff8", g: "#c89a30", G: "#fff0a0", e: "#1a0420", w: "#ffffff", i: "#ff2050", D: "#140c24", x: "#eee0ff" };
const c = cv(); const VO = "p1234";
ground(c, 16, 30, 13, 1.5, "D");
// しずく型の巨体（上が細く、下がふくらむ）
poly(c, [[16, 0], [20, 6], [24, 14], [8, 14], [12, 6]], VO); ell(c, 16, 9, 6, 7, VO);
ell(c, 16, 19, 14, 10, VO);
// 下のたれ
for (const [x, w] of [[5, 3], [10, 2], [22, 2], [27, 3]]) poly(c, [[x - 1, 26], [x + w, 26], [x + w / 2, 31]], VO);
// 砕けた環のかけらが体に刺さっている
for (const [x, y] of [[6, 15], [7, 16], [26, 13], [25, 12], [9, 26], [22, 27]]) { c.put(x, y, "G"); c.put(x, y + 1, "g"); c.put(x + 1, y, "g"); }
// 大きな中央の目
fillEll(c, 16, 15, 6, 4.5, "e"); fillEll(c, 16, 15, 5, 3.5, "C"); fillEll(c, 16, 15.5, 3, 3.2, "m"); fillEll(c, 16, 15.5, 1.5, 2.4, "e"); c.put(14, 13, "w"); c.put(15, 13, "w"); c.put(14, 14, "M");
for (const x of [11, 21]) c.put(x, 15, "c");
// 小さな目たち
for (const [x, y] of [[9, 19], [23, 19], [13, 23], [19, 23], [7, 22], [25, 23], [12, 9], [20, 9]]) { c.put(x, y, "i"); c.put(x + 1, y, "i"); c.put(x, y - 1, "w"); c.put(x + 1, y - 1, "M"); }
// 口（下に裂ける）
bline(c, 10, 27, 22, 27, "e"); for (const x of [12, 15, 18, 21]) { c.put(x, 26, "x"); c.put(x, 27, "e"); }
// しずくの雫と光の粒
for (const [x, y] of [[3, 8], [28, 6], [2, 20], [29, 21], [16, 2]]) { c.put(x, y, "4"); c.put(x, y + 1, "3"); }
export const rows = c.rows();
