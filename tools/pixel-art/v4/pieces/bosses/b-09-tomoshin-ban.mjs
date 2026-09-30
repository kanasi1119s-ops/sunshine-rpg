import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 灯芯都の番人（都を守る巨大な機械の番人）。青銅と鉄の巨体。胸の灯が都を照らす。完全オリジナル。
export const name = "灯芯都の番人";
export const category = "boss";
export const pal = { p: "#12121c", "1": "#2c3040", "2": "#4a5468", "3": "#7484a0", "4": "#a8b8d0", g: "#5a3a12", G: "#b07a24", h: "#f0c048", H: "#fff0b0", A: "#ffa020", X: "#fff4c0", e: "#2a0810", i: "#ff3a3a", w: "#ffffff", s: "#6a5a4a", D: "#181828" };
const c = cv(); const ST = "p1234", BR = "pgGhH";
ground(c, 16, 30, 14, 1.5, "D");
// 脚
box(c, 9, 21, 15, 28, ST); box(c, 17, 21, 23, 28, ST); box(c, 8, 27, 16, 30, BR); box(c, 16, 27, 24, 30, BR);
// 胴
box(c, 9, 9, 22, 22, ST);
for (const y of [12, 19]) for (let x = 10; x <= 21; x++) c.put(x, y, "1");
// 胸の灯（丸窓）
ell(c, 16, 16, 4, 4, BR); ell(c, 16, 16, 3, 3, "gAAXX"); c.put(15, 15, "w");
for (const [x, y] of [[13, 13], [19, 13], [13, 19], [19, 19]]) c.put(x, y, "H");
// 肩（大きな青銅の肩当て）
ell(c, 5, 12, 5, 4, BR); ell(c, 27, 12, 5, 4, BR);
for (const [x, y] of [[3, 10], [4, 9], [5, 9]]) c.put(x, y, "H");
for (const [x, y] of [[25, 10], [26, 9]]) c.put(x, y, "h");
// 腕と拳
box(c, 2, 15, 7, 24, ST); box(c, 24, 15, 29, 24, ST);
box(c, 1, 23, 8, 28, BR); box(c, 23, 23, 30, 28, BR);
for (const y of [17, 20]) for (const x of [3, 4, 5, 25, 26, 27]) c.put(x, y, "1");
// 頭（兜）
box(c, 11, 2, 20, 9, ST); poly(c, [[13, 2], [16, 0], [19, 2]], BR);
for (let x = 12; x <= 19; x++) c.put(x, 5, "e");
for (let x = 13; x <= 18; x++) c.put(x, 6, x % 2 ? "i" : "e"); c.put(13, 5, "w"); c.put(18, 6, "i");
c.put(14, 6, "i"); c.put(15, 6, "i"); c.put(16, 6, "i"); c.put(17, 6, "i");
// 首と蒸気口
box(c, 13, 9, 18, 10, "p1123");
for (const [x, y] of [[11, 3], [1, 11], [30, 11]]) c.put(x, y, "4");
export const rows = c.rows();
