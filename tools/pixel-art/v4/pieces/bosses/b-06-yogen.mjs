import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 予言の歪み（石板の翼の天使）。文字を刻んだ石板を翼にして宙に浮く、石の天使。完全オリジナル。
export const name = "予言の歪み";
export const category = "boss";
export const pal = { p: "#14141e", "1": "#34344c", "2": "#5a5a78", "3": "#8888a8", "4": "#bcbcd8", g: "#7a5c18", G: "#d8b038", h: "#fff0a0", c: "#28b8d8", C: "#b0f4ff", e: "#2a0a20", i: "#ffc040", w: "#ffffff", D: "#1a1a2c" };
const c = cv(); const ST = "p1234", GD = "pgGhh";
const M = (pts) => pts.map(([x, y]) => [32 - x, y]);
ground(c, 16, 30, 6, 1, "D");
// 翼（石板）：上の大板と下の小板
const wu = [[0.5, 5], [11, 9], [11, 20], [2, 17]], wl = [[3, 19], [11, 21], [12, 28], [6, 26]];
poly(c, wu, ST); poly(c, M(wu), ST); poly(c, wl, ST); poly(c, M(wl), ST);
// 刻まれた文字（水色の光）
const glyph = (x, y, mx) => { const p = [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [1, 3]]; for (const [a, b] of p) { c.put(x + a, y + b, "c"); c.put(31 - (x + a), y + b, "c"); } };
glyph(4, 9); glyph(7, 12); glyph(3, 13); glyph(7, 16); c.put(5, 12, "C"); c.put(26, 12, "C"); c.put(4, 10, "C"); c.put(27, 10, "C");
for (const [x, y] of [[5, 21], [8, 23], [7, 25]]) { c.put(x, y, "c"); c.put(31 - x, y, "c"); }
// 光輪
ell(c, 16, 3, 6, 2, GD); hole(c, 16, 3, 4, 1);
// 頭（石の顔）と目
ell(c, 16, 9, 4, 4, ST); fillEll(c, 14, 9, 1, 0.6, "e"); fillEll(c, 18, 9, 1, 0.6, "e");
c.put(14, 9, "i"); c.put(18, 9, "i"); c.put(13, 8, "w"); c.put(17, 8, "w");
// 胴（ローブ）
poly(c, [[12, 13], [20, 13], [22, 24], [19, 29], [13, 29], [10, 24]], ST);
// 胸の紋（金）
poly(c, [[16, 15], [18, 18], [16, 21], [14, 18]], GD); c.put(16, 18, "h");
// ローブの裾のひだ
for (const x of [13, 16, 19]) bline(c, x, 23, x, 28, "1");
// 肩の飾り（金）
box(c, 10, 12, 13, 14, GD); box(c, 19, 12, 22, 14, GD);
export const rows = c.rows();
