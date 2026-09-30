import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 砂嵐の歪み（渦を巻く砂）。うずまく砂の体の上に、空洞の白い仮面が浮かぶ。完全オリジナル。
export const name = "砂嵐の歪み";
export const category = "boss";
export const pal = { p: "#2a1a10", "1": "#5a3a20", "2": "#8a6234", "3": "#b88a4c", "4": "#e8c078", "5": "#fcecb8", b: "#ece4d0", B: "#a8a090", d: "#6a6258", e: "#14061e", v: "#a030ff", V: "#e0a0ff", w: "#ffffff", D: "#2a1a18" };
const c = cv(); const SAND = "p1234", MASK = "dBbb";
ground(c, 16, 29, 9, 2, "D");
// 渦（上が広く下が細い。帯をずらして重ねる）
for (let k = 0; k < 7; k++) { const cy = 10 + k * 3.1, rx = 14 - k * 1.8, cx = 16 + Math.round(Math.sin(k * 1.1) * 2); ell(c, cx, cy, rx, 3.4, SAND); }
// 渦の明るい筋
for (const [a, b, d, e2] of [[4, 15, 8, 17], [23, 14, 27, 15], [7, 21, 11, 23], [20, 22, 24, 21]]) bline(c, a, b, d, e2, "5");
// 舞う砂と小石
for (const [x, y] of [[2, 6], [4, 3], [28, 5], [29, 9], [1, 12], [30, 16], [3, 22], [27, 24], [8, 2], [24, 3]]) { c.put(x, y, "3"); c.put(x + 1, y, "2"); }
// 仮面
ell(c, 16, 8, 6, 7, MASK); fillEll(c, 16, 15, 3, 1, "B");
// 目（空洞に紫の光）と口
for (const x of [12, 19]) { fillEll(c, x, 8, 2, 2.5, "e"); c.put(x, 8, "v"); c.put(x, 9, "v"); c.put(x + 1, 9, "V"); }
c.put(11, 7, "w"); c.put(18, 7, "w");
for (let y = 12; y <= 14; y++) for (let x = 14; x <= 17; x++) c.put(x, y, y === 12 ? "e" : (x === 14 || x === 17) && y === 13 ? "e" : "e");
c.put(15, 12, "v"); c.put(16, 12, "v");
// ひび
bline(c, 16, 2, 15, 4, "d"); bline(c, 20, 5, 22, 7, "d");
export const rows = c.rows();
