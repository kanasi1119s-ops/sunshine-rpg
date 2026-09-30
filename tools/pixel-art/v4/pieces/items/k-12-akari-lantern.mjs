import { kNew, kEll, kRect, kPoly, kPut, kOutline, kRows, kLine } from "../../lib4.mjs";
// 灯りのランタン: 鉄の枠とガラスの中で、炎がゆれる手さげランタン。
export const name = "灯りのランタン";
export const category = "item";
export const pal = { o: "#12121c", I: "#6a6c84", i: "#44465e", d: "#2a2a3e", Y: "#fff0a0", y: "#ffd25a", O: "#ff9a30", R: "#e2551e", g: "#c8a850", G: "#7a6428", w: "#ffffff", h: "#fffcd8" };
const g = kNew();
// 持ち手の輪
for (let x = 9; x <= 22; x++) for (let y = 0; y < 8; y++) { const d = ((x - 15.5) / 6.5) ** 2 + ((y - 6) / 5.4) ** 2; if (d <= 1 && d >= 0.45) kPut(g, x, y, x < 15 ? "I" : "i"); }
// ふた
kPoly(g, [[13, 7], [18, 7], [23, 11], [8, 11]], "I"); kRect(g, 8, 11, 23, 12, "i"); kRect(g, 8, 12, 23, 12, "d");
kRect(g, 14, 6, 17, 7, "I");
// ガラス
kRect(g, 9, 13, 22, 23, "y"); kRect(g, 9, 13, 22, 13, "Y");
kRect(g, 11, 14, 20, 22, "Y");
kEll(g, 15.5, 19, 4, 5, ["h", "Y", "y", "O"]);
kEll(g, 15.5, 19.5, 2.3, 3.3, ["Y", "y", "O", "R"]);
// 柱
kRect(g, 9, 13, 10, 23, "I"); kRect(g, 21, 13, 22, 23, "i"); kRect(g, 21, 13, 22, 23, "i");
// 台
kRect(g, 8, 24, 23, 25, "I"); kRect(g, 8, 25, 23, 25, "i"); kRect(g, 10, 26, 21, 28, "i"); kRect(g, 10, 28, 21, 28, "d");
kRect(g, 8, 24, 23, 24, "I");

const r0 = kOutline(g, { I: "d", i: "o", d: "o", Y: "d", y: "d" }, "o");
for (const [x, y, c] of [[15, 21, "R"], [16, 20, "O"], [15, 18, "h"], [15, 17, "w"], [13, 15, "w"], [12, 14, "h"], [12, 16, "h"], [14, 8, "Y"], [15, 8, "Y"]]) kPut(r0, x, y, c);
// 光のふち
for (const [x, y] of [[13, 27], [12, 27]]) kPut(r0, x, y, "I");
export const rows = kRows(r0);
