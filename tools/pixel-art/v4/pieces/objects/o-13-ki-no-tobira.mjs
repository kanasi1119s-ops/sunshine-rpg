import { painter } from "../../lib4.mjs";
export const name = "木の扉";
export const category = "object";
export const pal = { o: "#221a18", h: "#e0d8c8", l: "#b8b0a0", m: "#8a8478", d: "#625c5c", t: "#8a5834", T: "#b47c48", U: "#d8a468", u: "#4e2e1e", i: "#3c4054", I: "#6c7290", y: "#f0c850", g: "#4a7a3c", G: "#7caa50", S: "#282a2a" };
const p = painter();
// 壁の一部
p.rect(3, 6, 28, 27, "m"); p.rect(3, 6, 6, 27, "l"); p.rect(25, 6, 28, 27, "d"); p.rect(3, 6, 28, 7, "h");
for (const y of [11, 16, 21]) for (let x = 3; x <= 28; x++) if ((x + y * 3) % 7 !== 0) p.put(x, y, "d");
p.rect(3, 26, 28, 27, "d");
// 石の枠（アーチ）
p.rect(8, 8, 23, 27, "l"); p.rect(8, 8, 23, 9, "h"); p.rect(8, 8, 9, 27, "h"); p.rect(22, 9, 23, 27, "m");
for (let x = 10; x < 22; x += 2) p.put(x, 8, "m");
// 扉
p.rect(10, 11, 21, 27, "t");
p.rect(10, 11, 21, 11, "T");
for (const x of [10, 13, 16, 19]) { p.rect(x, 12, x, 27, "T"); p.rect(x + 2, 12, x + 2, 27, "u"); }
p.rect(11, 12, 20, 12, "u"); p.rect(10, 12, 10, 27, "U");
// 鉄の帯・蝶番
p.rect(10, 14, 21, 15, "i"); p.rect(10, 14, 21, 14, "I"); p.rect(10, 23, 21, 24, "i"); p.rect(10, 23, 21, 23, "I");
p.pts([[11, 14], [11, 23], [20, 15], [20, 24]], "y");
p.rect(18, 18, 19, 21, "i"); p.pts([[18, 18]], "I"); p.pts([[18, 20]], "y");
// 石の段
p.rect(6, 27, 25, 28, "l"); p.rect(6, 27, 25, 27, "h"); p.rect(25, 28, 25, 28, "d");
// つた
p.pts([[4, 9], [4, 10], [5, 11], [4, 12], [5, 13], [6, 13], [3, 8], [4, 14], [26, 8], [27, 9], [26, 10], [27, 11], [26, 12]], "g"); p.pts([[4, 9], [26, 9], [5, 12]], "G");
p.outline("o");
p.shadow(20, 30, 11, 1, "S");
export const rows = p.rows();
