import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 浮嶼の主（空に浮かぶ島の主）。宙に浮く島そのものが、苔むした石の獣の体。完全オリジナル。
export const name = "浮嶼の主";
export const category = "boss";
export const pal = { p: "#14181c", "1": "#2c3a3c", "2": "#4a5e54", "3": "#748a70", "4": "#a4bc94", g: "#1c4a24", G: "#3c8a3c", h: "#8ad060", c: "#28d0a0", C: "#c8fff0", e: "#062a20", w: "#ffffff", r: "#5a3a22", R: "#9a6a3a", x: "#c8c0a8", D: "#1c2030" };
const c = cv(); const ROCK = "p1234", GRS = "pgGhh", HORN = "rRxxx".slice(0, 5);
// 島の下側（逆さ円錐の岩）
poly(c, [[3, 19], [29, 19], [24, 24], [19, 29], [15, 31], [12, 28], [7, 24]], ROCK);
for (const [a, b, d, e2] of [[9, 21, 12, 25], [20, 21, 18, 26], [15, 22, 15, 28], [24, 21, 22, 23]]) bline(c, a, b, d, e2, "1");
// 垂れる根と滝
for (const [x, y] of [[6, 22], [26, 22], [11, 27], [21, 27]]) { c.put(x, y, "r"); c.put(x, y + 1, "R"); c.put(x, y + 2, "r"); }
// 落ちる水
for (let y = 24; y <= 30; y++) { c.put(9, y, y % 3 ? "C" : "c"); }
// 島の草地の縁
ell(c, 16, 18, 14, 3, GRS);
// 上に立つ石の獣（胴と頭）
ell(c, 16, 12, 8, 6, ROCK);
// 苔
for (const [x, y] of [[9, 11], [10, 10], [11, 9], [12, 8], [21, 9], [22, 11], [20, 8]]) { c.put(x, y, "G"); c.put(x + 1, y, "g"); }
// 肩の岩と結晶
ell(c, 6, 14, 3, 3, ROCK); ell(c, 26, 14, 3, 3, ROCK);
for (const [x, y] of [[6, 10], [26, 10], [4, 12], [28, 12]]) { poly(c, [[x - 1, y + 2], [x + 1, y + 2], [x, y - 2]], "pcCCC"); }
// 角（左右）
poly(c, [[9, 9], [12, 8], [8, 1], [4, 2]], HORN); poly(c, [[23, 9], [20, 8], [24, 1], [28, 2]], HORN);
// 顔（大きな一つ目）
eye(c, 16, 11, 4, 3, "e", "C", "c", "e", "w");
// 牙と口
bline(c, 12, 15, 20, 15, "p"); for (const x of [13, 16, 19]) { c.put(x, 15, "x"); c.put(x, 16, "x"); }
// 島の上の小さな草木
for (const x of [4, 27]) { c.put(x, 16, "h"); c.put(x, 15, "G"); c.put(x - 1, 16, "G"); }
// 下の影（小さく）
ground(c, 16, 31, 6, 0.5, "D");
export const rows = c.rows();
