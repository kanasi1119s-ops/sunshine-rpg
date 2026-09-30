import { cv, ell, box, poly, bline, fillEll, hole, ground } from "../../bkit.mjs";
// 水涸れの歪み（干上がった川底の主）。ひび割れた泥と骨でできた、巨大な魚のような主。完全オリジナル。
export const name = "水涸れの歪み";
export const category = "boss";
export const pal = { p: "#1c120c", "1": "#3c2a1c", "2": "#5e4630", "3": "#866644", "4": "#b0905e", b: "#d8c8a0", B: "#f4ecd0", t: "#2a3c50", T: "#4a90b8", W: "#a8e4f8", e: "#2a0a20", i: "#ffd040", w: "#ffffff", v: "#5a2a9a", V: "#b070f0", D: "#1a1028" };
const c = cv(); const MUD = "p1234", BONE = "1bBB", WAT = "tTW";
ground(c, 16, 29, 13, 2, "D");
// ひびわれた地面のふち
for (const [a, b] of [[2, 28], [6, 30], [24, 30], [28, 28]]) bline(c, a, b, a + 2, b - 1, "1");
// 背びれ（骨のとげ）
for (const [x, h] of [[9, 5], [12, 8], [15, 10], [18, 10], [21, 8]]) poly(c, [[x - 2, 13], [x + 2, 13], [x, 13 - h]], "p1bBB");
// 胴（大きな魚の体。泥）
ell(c, 15, 19, 12, 8, MUD);
// 尾
poly(c, [[25, 17], [30, 11], [30, 26], [25, 21]], MUD); bline(c, 26, 18, 29, 14, "2"); bline(c, 26, 20, 29, 24, "2");
// ひび
for (const [a, b, d, e2] of [[8, 16, 11, 20], [11, 20, 9, 24], [17, 14, 19, 18], [19, 18, 22, 19], [14, 25, 16, 22]]) bline(c, a, b, d, e2, "p");
// 頭側の大きな口（あご骨）
poly(c, [[2, 19], [10, 17], [10, 24], [4, 25]], "p1bBB");
for (const x of [4, 6, 8]) { c.put(x, 20, "B"); c.put(x, 21, "b"); c.put(x, 22, "B"); }
// 口の中に残った水
fillEll(c, 6, 23, 3, 1, "T"); c.put(5, 23, "W");
// 目（黄色い光、ハイライト）
fillEll(c, 10, 14, 3, 2.5, "e"); fillEll(c, 10, 14, 2, 1.5, "i"); c.put(10, 14, "e"); c.put(9, 13, "w");
// あばら骨
for (const x of [14, 17, 20]) { for (let y = 21; y <= 26; y++) c.put(x + (y > 24 ? 1 : 0), y, y < 25 ? "B" : "b"); }
// ひれ（下）
poly(c, [[10, 26], [16, 26], [14, 30], [9, 30]], MUD);
// 漏れる歪み
for (const [x, y] of [[4, 12], [3, 15], [27, 9], [28, 12]]) { c.put(x, y, "V"); c.put(x, y + 1, "v"); }
export const rows = c.rows();
