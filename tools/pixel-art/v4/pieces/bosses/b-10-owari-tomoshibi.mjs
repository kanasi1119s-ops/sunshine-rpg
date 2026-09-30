import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 終わりの灯（最終ボス第1形態）。砕けた灯の環をまとう、夜のような外套の巨影。完全オリジナル。
export const name = "終わりの灯";
export const category = "boss";
export const pal = { p: "#0a0818", "1": "#1c1840", "2": "#342c6a", "3": "#5a4ca0", "4": "#8a7ad0", g: "#7a5a18", G: "#d8a832", h: "#fff0a0", H: "#ffffff", e: "#1a0410", i: "#ff2a4a", I: "#ff9a9a", w: "#ffffff", v: "#e8e0ff", D: "#100c20" };
const c = cv(); const CL = "p1234", RING = "pgGhH";
ground(c, 16, 30, 11, 1.5, "D");
// 砕けた灯の環（うしろ）。ところどころ欠ける
const seg = (a) => { const k = Math.floor(((a + Math.PI) / (Math.PI * 2)) * 14); return ![2, 5, 9, 12].includes(k); };
for (let t = 0; t < 360; t += 2) { const a = (t / 180) * Math.PI - Math.PI; if (!seg(a)) continue; const ang = a; for (const r of [13.6, 12.6]) { const x = 15.5 + r * Math.cos(ang), y = 15 + r * 0.98 * Math.sin(ang); const lit = -Math.cos(ang) * 0.6 - Math.sin(ang) * 0.75 > 0.2; c.put(x, y, r > 13 ? (lit ? "h" : "G") : (lit ? "G" : "g")); } }
// 環のかけら（浮く）
for (const [x, y] of [[2, 4], [3, 3], [29, 5], [28, 4], [1, 26], [2, 27], [30, 27]]) { c.put(x, y, "G"); c.put(x + 1, y, "h"); c.put(x, y + 1, "g"); }
// 外套（大きな影）
poly(c, [[9, 9], [23, 9], [27, 20], [29, 29], [3, 29], [5, 20]], CL);
// 外套のひだ
for (const [a, b, d, e2] of [[11, 14, 8, 27], [16, 14, 16, 28], [21, 14, 24, 27], [13, 18, 12, 28], [19, 18, 20, 28]]) bline(c, a, b, d, e2, "1");
// 肩と頭巾
ell(c, 16, 8, 7, 6, CL);
// 顔の闇
fillEll(c, 16, 9, 4.5, 4, "e");
// 目（赤い光・ハイライト）
for (const x of [14, 18]) { c.put(x, 9, "i"); c.put(x + 1, 9, "i"); c.put(x, 8, "I"); c.put(x, 10, "i"); }
c.put(13, 8, "w"); c.put(17, 8, "w");
// 胸の灯（消えかけた核）
ell(c, 16, 19, 3, 3, "pgGhH"); c.put(15, 18, "w"); c.put(16, 19, "H");
// ひび割れて漏れる光
for (const [a, b, d, e2] of [[16, 22, 15, 26], [13, 22, 11, 25], [19, 22, 21, 25]]) bline(c, a, b, d, e2, "G");
// 手（骨ばった白）
for (const x of [7, 24]) { c.put(x, 24, "v"); c.put(x + 1, 24, "v"); c.put(x, 25, "4"); c.put(x + 1, 25, "3"); }
export const rows = c.rows();
