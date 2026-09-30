import { cv, ell, box, poly, bline, fillEll, hole, ground, eye } from "../../bkit.mjs";
// 試作機の歪み（凍った重機械）。霜とつららに覆われた、履帯の足の重い機械。完全オリジナル。
export const name = "試作機の歪み";
export const category = "boss";
export const pal = { p: "#0c1420", "1": "#28384c", "2": "#4a6480", "3": "#7a9ab8", "4": "#b8d4ec", "5": "#f0faff", y: "#a88420", Y: "#f0d060", P: "#a030a0", q: "#f890f8", e: "#2a0a20", i: "#ff5a7a", w: "#ffffff", D: "#101828" };
const c = cv(); const STL = "p1234", ICE = "2345Z".replace("Z", "5");
ground(c, 16, 29, 14, 2, "D");
// 履帯
box(c, 2, 22, 29, 28, STL); for (let x = 4; x <= 27; x += 3) { c.put(x, 25, "1"); c.put(x, 24, "1"); c.put(x, 26, "1"); }
for (const x of [6, 15, 24]) { ell(c, x, 25, 2, 2, STL); }
for (let x = 3; x <= 28; x++) if (x % 2) c.put(x, 23, "4");
// 車体
box(c, 5, 12, 26, 22, STL); for (let x = 6; x <= 25; x += 4) c.put(x, 13, "4");
// 黄色の警告帯
for (let x = 7; x <= 24; x++) if ((x >> 1) % 2 === 0) { c.put(x, 20, "Y"); c.put(x, 21, "y"); }
// 砲塔（ドーム）と一つ目のレンズ
ell(c, 15, 10, 8, 6, STL, { top: true }); box(c, 8, 10, 22, 12, STL);
fillEll(c, 15, 8, 3, 2.3, "e"); fillEll(c, 15, 8, 2, 1.6, "i"); c.put(15, 8, "e"); c.put(14, 7, "w");
// 砲身（左）
box(c, 0, 13, 7, 17, STL); c.put(1, 15, "e"); c.put(0, 15, "e");
// 右の腕（アーム）
poly(c, [[26, 13], [30, 15], [30, 22], [27, 22]], STL); bline(c, 29, 16, 29, 20, "1");
// 漏れるエネルギー管
for (const y of [15, 18]) { for (let x = 17; x <= 23; x++) c.put(x, y, x % 3 === 0 ? "q" : "P"); }
// 霜とつらら（明るい氷色）
for (const [x, y, h] of [[6, 12, 4], [11, 6, 3], [20, 6, 3], [25, 12, 5], [10, 22, 3], [22, 22, 3], [3, 22, 3]]) poly(c, [[x - 1, y], [x + 1, y], [x, y + h]], "p345" + "5");
for (const [x, y] of [[8, 4], [12, 3], [17, 2], [21, 4], [4, 11], [27, 11], [14, 14], [9, 18]]) { c.put(x, y, "5"); c.put(x + 1, y, "4"); }
// 霜の氷塊（肩）
poly(c, [[3, 12], [7, 8], [9, 12]], "p2455"); poly(c, [[22, 12], [24, 7], [28, 12]], "p2455");
export const rows = c.rows();
