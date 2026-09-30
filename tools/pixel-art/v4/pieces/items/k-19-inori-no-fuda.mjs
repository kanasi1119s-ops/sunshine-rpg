import { kNew, kRect, kPoly, kPut, kOutline, kRows, kEll, kLine } from "../../lib4.mjs";
// 祈りの札: 細長い紙のお札。藍の縁と赤い円のしるし、房とひも。
export const name = "祈りの札";
export const category = "item";
export const pal = { o: "#28203c", P: "#fbf2dc", p: "#e4d4ae", q: "#bea87a", i: "#3a4c96", I: "#6c82c8", D: "#242f6e", r: "#d0383c", R: "#8c1c2c", A: "#ffd050", a: "#c8902c", w: "#ffffff", s: "#d8a870" };
const g = kNew();
// 紙（すそがV字）
kPoly(g, [[9, 6], [22, 6], [22, 29], [16, 25], [9, 29]], "P");
kRect(g, 20, 6, 22, 27, "p"); kPoly(g, [[19, 26], [22, 29], [22, 24]], "p");
// 藍の縁
kRect(g, 9, 6, 22, 8, "i"); kRect(g, 9, 6, 22, 6, "I"); kRect(g, 9, 8, 22, 8, "D");
kRect(g, 9, 21, 9, 27, "P");
// 赤い円としるし
kEll(g, 15.5, 15.5, 4.7, 4.7, ["r", "r", "R"]);
kPoly(g, [[15, 11], [17, 15], [20, 16], [17, 17], [15, 21], [14, 17], [11, 16], [14, 15]], "A");
kPut(g, 15, 15, "P");
// 文字っぽい線
for (const y of [22, 24]) { kRect(g, 12, y, 14, y, "q"); kRect(g, 17, y, 19, y, "q"); }
kRect(g, 11, 11, 11, 13, "q"); kRect(g, 20, 11, 20, 13, "q"); kRect(g, 11, 18, 11, 19, "q"); kRect(g, 20, 18, 20, 19, "q");
// 房とひも
for (let x = 13; x <= 18; x++) for (let y = 0; y < 4; y++) { const d = ((x - 15.5) / 3) ** 2 + ((y - 3) / 3) ** 2; if (d <= 1 && d >= 0.35) kPut(g, x, y, x < 16 ? "s" : "a"); }
kRect(g, 15, 3, 16, 5, "r");
const r0 = kOutline(g, { P: "q", p: "q", q: "q", i: "D", I: "D", D: "D", s: "a", a: "a", r: "R", R: "R" }, "o");
for (const [x, y, c] of [[10, 10, "w"], [10, 11, "P"], [13, 13, "w"], [14, 12, "w"], [10, 9, "P"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
