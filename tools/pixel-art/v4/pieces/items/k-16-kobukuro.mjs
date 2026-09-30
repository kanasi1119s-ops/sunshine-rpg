import { kNew, kEll, kRect, kPoly, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
export const name = "小袋（灯貨）";
export const category = "item";
export const pal = { o: "#2a1a10", H: "#e0bc80", L: "#c09458", M: "#94683a", D: "#68441e", r: "#c8403c", R: "#8c2224", A: "#ffd850", a: "#d09a28", b: "#8c5c14", w: "#ffffff", f: "#fff4b8" };
const g = kNew();
// 口のひだ
kPoly(g, [[10, 5], [12, 8], [14, 5], [16, 8], [18, 5], [20, 8], [22, 5], [23, 13], [9, 13]], "L");
kRect(g, 9, 9, 12, 12, "H"); kRect(g, 20, 9, 23, 12, "M");
for (const x of [12, 16, 20]) kRect(g, x, 8, x, 12, "M");
// 袋の本体
kEll(g, 16, 21, 11.5, 9, ["H", "L", "L", "M", "D"]);
kRect(g, 10, 13, 22, 16, "L"); kRect(g, 10, 13, 12, 16, "H"); kRect(g, 21, 13, 22, 16, "M");
// ひも
kRect(g, 9, 13, 23, 14, "r"); kRect(g, 9, 13, 23, 13, "r"); kRect(g, 9, 14, 23, 14, "R");
kRect(g, 15, 14, 17, 15, "r");
kLine(g, 14, 14, 11, 19, "r"); kLine(g, 18, 14, 22, 19, "R"); kRect(g, 10, 19, 12, 20, "r"); kRect(g, 21, 19, 23, 20, "R");
// 金の灯マーク
kEll(g, 16, 23, 3.2, 3.6, ["f", "A", "a"]); kPoly(g, [[16, 17], [18, 21], [14, 21]], "A");
kPut(g, 16, 18, "f"); kPut(g, 15, 21, "f");
kRect(g, 14, 27, 18, 27, "b");
const r0 = kOutline(g, { H: "D", L: "D", M: "D", D: "D", r: "R", R: "R" }, "o");
for (const [x, y, c] of [[9, 20, "w"], [8, 22, "H"], [9, 15, "w"], [8, 24, "H"], [25, 14, "."], [16, 25, "a"], [16, 24, "A"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
