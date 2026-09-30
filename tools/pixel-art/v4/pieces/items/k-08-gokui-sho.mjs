import { kNew, kEll, kRect, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
// 極意書: 横に広げた巻物。両端の軸と、赤いひもと印。
export const name = "極意書";
export const category = "item";
export const pal = { o: "#2c1a1a", P: "#f8eccc", p: "#e4d0a0", q: "#c0a874", k: "#b0865a", K: "#6c4426", L: "#d8b078", t: "#c0303c", T: "#f07a80", d: "#8a1c2c", i: "#5a4030", w: "#ffffff" };
const g = kNew();
// 紙
kRect(g, 8, 9, 23, 24, "P"); kRect(g, 8, 21, 23, 24, "p"); kRect(g, 21, 9, 23, 24, "p"); kRect(g, 8, 24, 23, 24, "q");
// 軸（上と下）
kRect(g, 4, 5, 27, 8, "L"); kRect(g, 4, 8, 27, 8, "k"); kRect(g, 4, 7, 27, 7, "L");
kRect(g, 4, 25, 27, 28, "L"); kRect(g, 4, 28, 27, 28, "k"); kRect(g, 4, 27, 27, 27, "L");
kRect(g, 2, 4, 3, 9, "k"); kRect(g, 28, 4, 29, 9, "K"); kRect(g, 2, 24, 3, 29, "k"); kRect(g, 28, 24, 29, 29, "K");
kRect(g, 4, 5, 27, 5, "P");
// 文字っぽい線（読めない模様）
for (const [y, x0, x1] of [[12, 11, 20], [15, 11, 18], [18, 11, 20], [21, 11, 16]]) { kRect(g, x0, y, x1, y, "i"); kRect(g, x0 + 1, y + 1, x1 - 2, y + 1, "q"); }
// 赤い印
kRect(g, 18, 18, 22, 22, "t"); kRect(g, 22, 18, 22, 22, "d"); kRect(g, 18, 22, 22, 22, "d"); kRect(g, 18, 18, 19, 18, "T");
kRect(g, 20, 19, 20, 21, "T");
const r0 = kOutline(g, { P: "q", p: "q", q: "K", L: "K", k: "K", K: "K", t: "d" }, "o");
for (const [x, y, c] of [[5, 6, "w"], [6, 6, "w"], [9, 10, "w"], [9, 11, "w"], [5, 26, "w"]]) kPut(r0, x, y, c);
// ひも
kRect(r0, 15, 5, 16, 8, "t"); kRect(r0, 15, 5, 15, 8, "T");
export const rows = kRows(r0);
