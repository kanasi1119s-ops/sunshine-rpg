import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 灯里の歪み（序章のボス）。歪んだ灯り石に呑まれた、割れた大きな古い角灯。ひとつ目が中でにらむ。完全オリジナル。
export const name = "灯里の歪み";
export const category = "boss";
export const pal = { p: "#0e0a18", "1": "#2a2840", "2": "#464462", "3": "#6c6a8c", "4": "#9896b8", G: "#4a2c14", g: "#8a5a24", h: "#d08a30", A: "#ffb838", X: "#fff0a8", e: "#3a0a20", i: "#ff3a6a", w: "#ffffff", v: "#5a2a9a", V: "#a060e8", U: "#e0c0ff", D: "#1a1030" };
const c = cv(); const IRON = "p1234", AMB = "GghAX", VIO = "pvvVV";
ground(c, 16, 29, 12, 2, "D");
// 歪みのもや（紫の炎）を背に
for (const [x, y, rx, ry] of [[5, 15, 2, 5], [26, 13, 2, 6], [7, 8, 2, 3], [25, 6, 2, 3], [4, 22, 2, 3], [27, 22, 2, 4]]) ell(c, x, y, rx, ry, VIO);
// 取っ手の輪
ell(c, 16, 4, 6, 4, IRON); hole(c, 16, 4, 3, 2);
// ふた（屋根）
poly(c, [[15, 7], [17, 7], [24, 11], [8, 11]], IRON); box(c, 6, 11, 25, 13, IRON);
// 本体（ガラスの胴。ふくらんだ形）
ell(c, 16, 19, 10, 7, IRON); ell(c, 16, 19, 8, 6, AMB);
// 縦の枠
for (const x of [11, 21]) for (let y = 13; y <= 25; y++) c.put(x, y, y % 5 === 0 ? "3" : "2");
for (const x of [10, 20]) for (let y = 14; y <= 24; y++) if (c.get(x, y) !== "p") c.put(x, y, "1");
// ひとつ目
eye(c, 16, 19, 4, 3, "e", "X", "i", "e", "w");
c.put(15, 19, "i"); c.put(17, 19, "i");
// 割れ目と紫の漏れ
for (const [a, b, d, e2] of [[13, 13, 15, 16], [19, 14, 17, 16], [12, 24, 14, 22], [22, 24, 20, 22]]) bline(c, a, b, d, e2, "e");
for (const [x, y] of [[13, 12], [19, 12], [9, 21], [23, 17], [24, 21]]) { c.put(x, y, "V"); c.put(x, y + 1, "v"); }
// 台座と足
box(c, 7, 25, 24, 27, IRON);
poly(c, [[8, 27], [13, 27], [12, 30], [7, 30]], IRON); poly(c, [[19, 27], [24, 27], [25, 30], [19, 30]], IRON);
// 鋲
for (const x of [10, 16, 22]) c.put(x, 12, "4");
export const rows = c.rows();
