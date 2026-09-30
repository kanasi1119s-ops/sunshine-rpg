import { kNew, kPoly, kRect, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
// 回復薬（大）: 四角ばったずんぐり大びん。赤いろうの封と、ラベル。
export const name = "回復薬（大）";
export const category = "item";
export const pal = { o: "#241028", W: "#e8f4f4", G: "#b8d8dc", g: "#7aa4b4", l: "#ff8c9c", L: "#e03050", D: "#98183a", d: "#6a1030", c: "#c89858", C: "#845430", w: "#ffffff", y: "#f4ead0", Y: "#c8b888", t: "#a82838", T: "#e06070" };
const g = kNew();
kPoly(g, [[9, 12], [22, 12], [25, 15], [26, 18], [26, 27], [24, 29], [8, 29], [6, 27], [6, 18], [7, 15]], "G");
kRect(g, 12, 5, 19, 12, "G");
kRect(g, 8, 17, 24, 28, "L"); kRect(g, 8, 17, 9, 28, "l"); kRect(g, 22, 17, 24, 28, "D"); kRect(g, 10, 17, 10, 28, "L");
kRect(g, 8, 27, 24, 28, "D"); kRect(g, 12, 15, 19, 16, "L");
kRect(g, 8, 16, 24, 16, "W");
kRect(g, 12, 13, 19, 14, "W");
// ラベル
kRect(g, 11, 20, 20, 25, "y"); kRect(g, 20, 20, 20, 25, "Y"); kRect(g, 11, 25, 20, 25, "Y");
kRect(g, 15, 21, 16, 24, "t"); kRect(g, 13, 22, 18, 23, "t");
// コルク
kRect(g, 13, 2, 18, 5, "c"); kRect(g, 18, 2, 18, 5, "C"); kRect(g, 13, 5, 18, 5, "C");
kRect(g, 12, 6, 19, 8, "t"); kRect(g, 19, 6, 19, 8, "d"); kRect(g, 12, 6, 13, 6, "T");
const r0 = kOutline(g, { c: "C", C: "C", t: "d", d: "d" }, "o");
for (const [x, y, c] of [[8, 20, "w"], [8, 21, "w"], [9, 18, "w"], [13, 12, "w"], [7, 17, "w"], [22, 25, "l"], [21, 22, "l"], [14, 3, "y"], [15, 3, "y"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
