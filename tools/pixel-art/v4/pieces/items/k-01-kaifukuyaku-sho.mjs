import { kNew, kEll, kRect, kPut, kOutline, kRows } from "../../lib4.mjs";
// 回復薬（小）: まるいフラスコに赤い薬。コルクせん。
export const name = "回復薬（小）";
export const category = "item";
export const pal = { o: "#2a1230", W: "#e4f6fb", G: "#b4dcec", g: "#7cb0cc", l: "#f88a98", L: "#d83048", D: "#8c1a34", c: "#d09a58", C: "#8c5a32", w: "#ffffff", y: "#efe0a8", Y: "#b89c60" };
const g = kNew();
kRect(g, 13, 11, 18, 16, "G"); kRect(g, 18, 11, 18, 16, "g");
kEll(g, 16, 21.5, 9, 8, ["W", "G", "G", "g"]);
kEll(g, 16, 22.5, 7.4, 6.4, ["l", "L", "L", "D"]);
for (let y = 14; y < 20; y++) for (let x = 6; x < 26; x++) if (g[y][x] === "l" || g[y][x] === "L" || g[y][x] === "D") g[y][x] = "W";
for (let x = 10; x <= 22; x++) if (g[19][x] === "W") g[19][x] = "l";
kRect(g, 13, 7, 18, 10, "c"); kRect(g, 18, 7, 18, 10, "C"); kRect(g, 13, 10, 18, 10, "C");
kRect(g, 12, 15, 19, 15, "y"); kRect(g, 19, 15, 19, 15, "Y");
let r = kOutline(g, { c: "C", C: "C", y: "Y" }, "o");
for (const [x, y, c] of [[9, 20, "w"], [9, 21, "w"], [10, 18, "w"], [14, 13, "w"], [14, 14, "w"], [12, 25, "l"], [20, 26, "D"], [19, 28, "D"], [15, 8, "y"], [16, 8, "y"]]) kPut(r, x, y, c);
export const rows = kRows(r);
