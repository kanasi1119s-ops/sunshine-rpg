import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 積荷の歪み（木箱の化け物）。積み上がった木箱がひとつの巨体になり、大口を開ける。完全オリジナル。
export const name = "積荷の歪み";
export const category = "boss";
export const pal = { p: "#180c08", "1": "#3c2214", "2": "#6a4224", "3": "#946038", "4": "#c48c50", m: "#3a3a52", M: "#8a8aa8", N: "#c0c0dc", e: "#ffe070", E: "#3a2a08", w: "#ffffff", r: "#701828", R: "#c03048", t: "#e8e0c8", T: "#a8a088", v: "#5a2a9a", V: "#b070f0", D: "#1a1028" };
const c = cv(); const WOOD = "p1234", IR = "pmMN";
ground(c, 16, 29, 14, 2, "D");
// 上の小さな箱（頭）
box(c, 9, 2, 22, 10, WOOD); for (let x = 10; x <= 21; x++) c.put(x, 6, "2");
box(c, 9, 2, 12, 10, IR); box(c, 19, 2, 22, 10, IR);
// 大きな胴の箱（口）
box(c, 3, 11, 28, 27, WOOD);
for (const x of [3, 4, 5, 6]) for (let y = 11; y <= 27; y++) c.put(x, y, y === 11 || y === 27 || x === 3 ? "p" : (x === 4 ? "N" : x === 5 ? "M" : "m"));
for (const x of [25, 26, 27, 28]) for (let y = 11; y <= 27; y++) c.put(x, y, y === 11 || y === 27 || x === 28 ? "p" : (x === 25 ? "M" : x === 26 ? "m" : "m"));
// 板のすじ
for (const y of [15, 25]) for (let x = 7; x <= 24; x++) c.put(x, y, "1");
// 口（大きく開く）
for (let y = 17; y <= 23; y++) for (let x = 8; x <= 23; x++) c.put(x, y, y === 17 ? "p" : y > 21 ? "r" : "p");
for (let x = 9; x <= 22; x++) c.put(x, 22, "R"); for (let x = 11; x <= 20; x++) c.put(x, 23, "R");
for (const x of [9, 12, 15, 18, 21]) { c.put(x, 18, "T"); c.put(x, 19, "t"); c.put(x + 1, 18, "t"); c.put(x, 20, "T"); }
for (const x of [10, 13, 16, 19]) { c.put(x, 22, "t"); c.put(x, 21, "T"); }
// 目（3つ）
eye(c, 12, 6, 2, 2, "E", "e", "e", "E", "w"); eye(c, 19, 6, 2, 2, "E", "e", "e", "E", "w");
c.put(12, 6, "E"); c.put(19, 6, "E");
// 胴の割れ目から光る目
for (const [x, y] of [[9, 13], [22, 13]]) { c.put(x, y, "e"); c.put(x + 1, y, "e"); c.put(x, y - 1, "w"); }
// 足になる小箱
box(c, 5, 27, 12, 30, WOOD); box(c, 19, 27, 26, 30, WOOD);
// はみ出す歪み
for (const [x, y] of [[2, 6], [1, 9], [29, 5], [30, 9], [7, 1], [24, 1]]) { c.put(x, y, "V"); c.put(x, y + 1, "v"); }
export const rows = c.rows();
