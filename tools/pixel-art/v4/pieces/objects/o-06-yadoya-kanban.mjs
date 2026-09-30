import { painter } from "../../lib4.mjs";
export const name = "宿屋の看板";
export const category = "object";
export const pal = { o: "#2a1a14", t: "#7a4c2c", T: "#a87040", h: "#d49c60", u: "#4a2c1c", i: "#4a4a58", I: "#7c7c8c", w: "#f4f0e4", b: "#3a64b0", B: "#6e9ae0", y: "#f8d860", s: "#8a8478", c: "#a8a294", S: "#2a2a24" };
const p = painter();
// 支柱と腕
p.rect(7, 6, 10, 26, "t"); p.rect(7, 6, 8, 26, "T"); p.rect(10, 6, 10, 26, "u"); p.rect(7, 6, 10, 6, "h");
p.rect(11, 6, 27, 8, "t"); p.rect(11, 6, 27, 6, "T"); p.rect(11, 8, 27, 8, "u"); p.line(11, 14, 18, 8, "u"); p.line(11, 13, 17, 8, "t");
// 鎖
for (const x of [14, 25]) { p.pts([[x, 9], [x, 11]], "I"); p.pts([[x, 10], [x, 12]], "i"); }
// 看板
p.rect(11, 12, 28, 23, "t"); p.rect(12, 13, 27, 22, "T"); p.rect(12, 13, 27, 13, "h"); p.rect(12, 22, 27, 22, "t"); p.rect(27, 13, 27, 22, "t");
p.rect(12, 14, 12, 21, "h");
// 寝台の絵
p.rect(14, 16, 15, 20, "u"); p.rect(14, 19, 25, 20, "u"); p.rect(25, 17, 25, 20, "u");
p.rect(16, 16, 18, 18, "w"); p.rect(16, 16, 16, 17, "w"); p.rect(19, 17, 24, 18, "b"); p.rect(19, 17, 24, 17, "B"); p.rect(16, 18, 18, 18, "c");
p.pts([[21, 14], [22, 14]], "y");
// 足元の石
p.rect(5, 26, 12, 28, "s"); p.rect(5, 26, 12, 26, "c"); p.rect(12, 27, 12, 28, "i");
p.outline("o");
p.shadow(16, 29, 12, 1.6, "S");
export const rows = p.rows();
