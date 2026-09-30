import { kNew, kEll, kRect, kPut, kOutline, kRows, kLine, kPoly } from "../../lib4.mjs";
// 目覚めの香: 小さな香炉にお香を3本。先が赤くともり、けむりがゆれる。
export const name = "目覚めの香";
export const category = "item";
export const pal = { o: "#2a1a24", A: "#f0c060", a: "#c08838", b: "#845020", d: "#4c2c18", s: "#e8e0f0", S: "#b8a8d0", v: "#8878a8", t: "#e04a2c", T: "#ffb060", n: "#b0824a", N: "#6a4a2a", w: "#ffffff", e: "#7ab068" };
const g = kNew();
// けむり
for (const [x, y] of [[13, 4], [14, 5], [15, 6], [15, 7], [14, 8], [13, 9], [13, 10]]) { kPut(g, x, y, "s"); kPut(g, x + 1, y, "S"); }
for (const [x, y] of [[20, 2], [19, 3], [19, 4], [20, 5], [21, 6], [21, 7], [20, 8], [20, 9]]) { kPut(g, x, y, "s"); kPut(g, x + 1, y, "v"); }
for (const [x, y] of [[9, 6], [10, 7], [10, 8], [9, 9], [9, 10]]) { kPut(g, x, y, "s"); kPut(g, x + 1, y, "S"); }
// お香
kLine(g, 9, 11, 11, 22, "n"); kLine(g, 10, 11, 12, 22, "N");
kLine(g, 14, 11, 15, 22, "n"); kLine(g, 15, 11, 16, 22, "N");
kLine(g, 20, 10, 19, 22, "n"); kLine(g, 21, 10, 20, 22, "N");
// 香炉（お椀）
kEll(g, 16, 22.5, 11, 7.5, ["A", "A", "a", "b"]);
for (let y = 15; y < 22; y++) for (let x = 3; x < 30; x++) if (g[y][x] !== "." && y < 22 && !"nN".includes(g[y][x]) ) { if (y < 22 && (g[y][x] === "A" || g[y][x] === "a" || g[y][x] === "b")) g[y][x] = "."; }
kRect(g, 5, 22, 27, 23, "A"); kRect(g, 5, 22, 27, 22, "A");
kRect(g, 12, 28, 20, 29, "d"); kRect(g, 10, 26, 22, 27, "b");
// 灰
kRect(g, 7, 21, 25, 21, "S"); kRect(g, 7, 21, 9, 21, "s");
const r0 = kOutline(g, { A: "b", a: "d", b: "d", n: "N", N: "N", s: "v", S: "v", v: "v" }, "o");
// 灰の上のお香の根もと
for (const [x, y, c] of [[9, 10, "T"], [10, 10, "t"], [14, 10, "T"], [15, 10, "t"], [20, 9, "T"], [21, 9, "t"], [8, 22, "w"], [9, 23, "w"], [24, 25, "a"], [16, 24, "e"], [15, 25, "e"], [17, 25, "e"], [16, 23, "e"]]) kPut(r0, x, y, c);
export const rows = kRows(r0);
