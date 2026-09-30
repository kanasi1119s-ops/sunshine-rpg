import { kNew, kRect, kPoly, kPut, kOutline, kRows, kEll, kLine } from "../../lib4.mjs";
// 羅針盤: 真鍮のふたなしコンパス。ガラスの下で赤い針が北をさす。
export const name = "羅針盤";
export const category = "item";
export const pal = { o: "#241408", X: "#fff0a8", A: "#eec250", a: "#c08c2c", b: "#8a5a1c", d: "#5c3a14", F: "#f2ecd8", f: "#d4ccb0", g: "#a8a48c", k: "#38304c", r: "#dc3c3c", R: "#8c1c24", w: "#ffffff", B: "#9cc4e0" };
const g = kNew();
// 上の輪とつまみ
for (let x = 11; x <= 20; x++) for (let y = 0; y < 8; y++) { const d = ((x - 15.5) / 4.8) ** 2 + ((y - 3.6) / 3.6) ** 2; if (d <= 1 && d >= 0.35) kPut(g, x, y, x < 16 ? "A" : "a"); }
kRect(g, 13, 6, 18, 8, "a"); kRect(g, 13, 6, 14, 8, "A"); kRect(g, 18, 6, 18, 8, "b");
// 外わく
kEll(g, 16, 19, 13, 12, ["X", "A", "A", "a", "b"]);
// 盤面
kEll(g, 16, 19, 10.3, 9.4, ["F", "F", "f", "g"]);
// 目もり
for (const [x, y] of [[16, 10], [16, 11], [16, 27], [16, 28], [6, 19], [7, 19], [25, 19], [26, 19]]) kPut(g, x, y, "k");
for (const [x, y] of [[9, 13], [23, 13], [9, 25], [23, 25]]) kPut(g, x, y, "g");
// 針（北へ赤・南へ白）
kPoly(g, [[16, 11], [19, 19], [16, 20], [13, 19]], "r");
kPoly(g, [[16, 11], [16, 20], [13, 19]], "R");
kPoly(g, [[16, 27], [19, 19], [16, 20], [13, 19]], "g");
kPoly(g, [[16, 27], [19, 19], [16, 20]], "k");
kPut(g, 16, 19, "k"); kPut(g, 16, 20, "A");
const r0 = kOutline(g, { X: "d", A: "d", a: "d", b: "d" }, "o");
// ガラスの照り
for (const [x, y, c] of [[9, 14, "w"], [10, 13, "w"], [11, 12, "w"], [8, 16, "B"], [9, 17, "B"], [16, 11, "R"], [16, 12, "r"], [15, 3, "X"], [14, 4, "X"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
