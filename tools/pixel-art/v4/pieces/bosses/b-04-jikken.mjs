import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 実験の歪み（鉄の檻の実験装置）。鉄の檻の胴の中で青緑の核が脈打つ。完全オリジナル。
export const name = "実験の歪み";
export const category = "boss";
export const pal = { p: "#0a1216", "1": "#22323a", "2": "#3e5460", "3": "#6a8896", "4": "#a8c4d0", c: "#0e5a5a", C: "#20c0b0", X: "#d0fff0", e: "#2a0a20", i: "#ff4a6a", w: "#ffffff", r: "#6a3a22", R: "#c07038", y: "#e0b040", D: "#141826", v: "#5a2a9a", V: "#b070f0" };
const c = cv(); const IRON = "p1234", CORE = "pcCXX";
ground(c, 16, 29, 13, 2, "D");
// 頭の鉄仮面（一つ目のレンズ）
ell(c, 16, 6, 6, 4, IRON); box(c, 10, 6, 21, 8, IRON); fillEll(c, 16, 6, 4, 2, "e"); fillEll(c, 16, 6, 3, 1.5, "i"); c.put(16, 6, "e"); c.put(14, 5, "w");
// 首の管
box(c, 13, 9, 18, 11, IRON);
// 胴の檻の骨組み
box(c, 5, 11, 26, 26, IRON);
for (let y = 13; y <= 24; y++) for (let x = 7; x <= 24; x++) c.put(x, y, "p");
// 檻の中の核（脈打つ青緑の光）
ell(c, 16, 18, 6, 5, CORE); c.put(14, 16, "w");
for (const [x, y] of [[12, 15], [11, 19], [20, 21]]) c.put(x, y, "X");
// 檻の格子（縦）
for (const x of [9, 13, 18, 22]) for (let y = 12; y <= 25; y++) c.put(x, y, x < 16 ? (y % 7 === 0 ? "4" : "3") : "2");
// 横の帯（リベット）
for (const y of [12, 25]) for (let x = 6; x <= 25; x++) c.put(x, y, x % 3 === 0 ? "4" : "2");
// 腕（つながった管とはさみ）
poly(c, [[1, 13], [5, 13], [5, 22], [2, 22]], IRON); poly(c, [[26, 13], [30, 13], [29, 22], [26, 22]], IRON);
for (const x of [2, 28]) { c.put(x, 23, "R"); c.put(x, 24, "r"); c.put(x + 1, 23, "R"); c.put(x + 1, 24, "R"); c.put(x, 25, "p"); }
// 下の脚
box(c, 8, 26, 13, 29, IRON); box(c, 18, 26, 23, 29, IRON);
// 漏れる電気の火花
for (const [x, y] of [[3, 9], [28, 9], [2, 27], [29, 27]]) { c.put(x, y, "X"); c.put(x + 1, y - 1, "C"); c.put(x - 1, y + 1, "C"); }
export const rows = c.rows();
