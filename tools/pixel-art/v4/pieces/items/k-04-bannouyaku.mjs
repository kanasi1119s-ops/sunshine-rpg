import { kNew, kEll, kRect, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
// 万能薬: ひょうたん型の緑のびん。ひもと葉のふだ。
export const name = "万能薬";
export const category = "item";
export const pal = { o: "#12281c", W: "#e6f8e4", G: "#bce4b0", g: "#76b47c", l: "#a4ee7a", L: "#4cb04c", D: "#26783a", d: "#14502c", c: "#d0a860", C: "#8c6432", w: "#ffffff", r: "#b06a3c", R: "#7a4222", y: "#f4e4b8", Y: "#b09c68" };
const g = kNew();
kEll(g, 16, 22, 9, 7.5, ["W", "G", "G", "g"]);
kEll(g, 16, 13.5, 6, 5.5, ["W", "G", "G", "g"]);
kRect(g, 13, 9, 18, 11, "G");
kEll(g, 16, 22.5, 7.5, 6.2, ["l", "L", "L", "D"]);
kEll(g, 16, 14.5, 4.4, 3.8, ["l", "L", "L", "D"]);
kRect(g, 14, 10, 17, 11, "g");
kRect(g, 11, 17, 20, 17, "G"); // くびれ
kRect(g, 13, 3, 18, 8, "c"); kRect(g, 18, 3, 18, 8, "C"); kRect(g, 13, 8, 18, 8, "C");
// ひも
kRect(g, 12, 9, 19, 9, "r"); kRect(g, 19, 9, 19, 9, "R");
// 葉のふだ
kRect(g, 22, 15, 26, 21, "y"); kRect(g, 26, 15, 26, 21, "Y"); kRect(g, 22, 21, 26, 21, "Y");
kLine(g, 19, 10, 22, 15, "r");
const r0 = kOutline(g, { c: "C", C: "C", r: "R", R: "R", y: "Y", Y: "Y" }, "o");
kPut(r0, 24, 16, "L"); kPut(r0, 23, 17, "L"); kPut(r0, 24, 17, "L"); kPut(r0, 25, 17, "D"); kPut(r0, 24, 18, "L"); kPut(r0, 24, 19, "D");
for (const [x, y, c] of [[9, 20, "w"], [9, 21, "w"], [10, 18, "W"], [13, 12, "w"], [13, 13, "w"], [14, 3, "y"], [15, 3, "y"], [20, 26, "D"], [12, 26, "l"], [17, 21, "l"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
