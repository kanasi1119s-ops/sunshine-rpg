import { kNew, kPoly, kRect, kPut, kOutline, kRows, kLine, kClean } from "../../lib4.mjs";
// 干し肉: 骨つきの干し肉を、ひもで吊るしたところ。白いあぶらの筋。
export const name = "干し肉";
export const category = "item";
export const pal = { o: "#2a1014", H: "#cc6c5c", R: "#a84840", M: "#7c2c2c", D: "#54181e", f: "#f6dcc8", F: "#dcaa98", s: "#e6cc94", S: "#9c7c40", w: "#ffffff", e: "#f4ecd8", E: "#c8b898" };
const g = kNew();
// 骨（右下へつき出す）
kLine(g, 20, 22, 27, 27, "e"); kLine(g, 20, 23, 27, 28, "E"); kLine(g, 19, 21, 26, 26, "e");
kRect(g, 26, 25, 29, 26, "e"); kRect(g, 27, 28, 29, 29, "E"); kRect(g, 28, 26, 29, 27, "e"); kRect(g, 26, 29, 27, 29, "E");
// 肉の本体（ななめのかたまり）
kPoly(g, [[6, 12], [12, 8], [19, 8], [24, 12], [25, 18], [22, 24], [15, 27], [9, 25], [5, 19]], "R");
kPoly(g, [[6, 12], [12, 8], [19, 8], [15, 15], [10, 20], [5, 19]], "H");
kPoly(g, [[24, 12], [25, 18], [22, 24], [15, 27], [17, 20]], "M");
kPoly(g, [[22, 24], [15, 27], [17, 24]], "D");
// あぶらの筋
for (const [x, y] of [[10, 12], [11, 13], [12, 14], [13, 15], [14, 16], [15, 17]]) { kPut(g, x, y, "f"); kPut(g, x, y + 1, "F"); }
for (const [x, y] of [[17, 21], [18, 22], [19, 23]]) kPut(g, x, y, "F");
for (const [x, y] of [[9, 21], [10, 22], [11, 22]]) kPut(g, x, y, "F");
for (const [x, y] of [[19, 12], [20, 13], [21, 14]]) kPut(g, x, y, "F");
// ひもの輪と、しばり
for (let x = 5; x <= 15; x++) for (let y = 0; y < 12; y++) { const d = ((x - 10) / 5) ** 2 + ((y - 5) / 5) ** 2; if (d <= 1 && d >= 0.42 && y < 10) kPut(g, x, y, x < 10 ? "s" : "S"); }
kRect(g, 20, 17, 21, 24, "s"); kRect(g, 22, 17, 22, 24, "S");
const r0 = kOutline(g, { H: "D", R: "D", M: "D", D: "D", s: "S", S: "S", e: "E", E: "E" }, "o");
for (const [x, y, c] of [[9, 11, "w"], [8, 12, "F"], [10, 10, "F"], [7, 15, "F"], [27, 26, "w"]]) kPut(r0, x, y, c);
export const rows = kClean(kRows(r0));
