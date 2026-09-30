import { painter } from "../../lib4.mjs";
export const name = "灯り石の柱";
export const category = "object";
export const pal = { o: "#141a30", h: "#a8b4d4", l: "#7c8ab4", m: "#56628e", d: "#3a4470", e: "#262c50", c: "#8cf4ec", C: "#e4fff8", g: "#3cc8c4", z: "#1c8c9c", S: "#1c2030", p: "#bce8ff" };
const p = painter();
// 台座（2段）
p.rect(5, 25, 26, 27, "m"); p.rect(5, 25, 26, 25, "h"); p.rect(5, 25, 7, 27, "l"); p.rect(23, 26, 26, 27, "d");
p.rect(8, 22, 23, 24, "l"); p.rect(8, 22, 23, 22, "h"); p.rect(21, 23, 23, 24, "m");
// 柱
p.rect(11, 9, 20, 21, "m"); p.rect(11, 9, 13, 21, "l"); p.rect(18, 9, 20, 21, "d"); p.rect(11, 9, 12, 21, "h"); p.rect(19, 9, 20, 21, "e");
// 光る刻み
p.rect(15, 11, 16, 20, "g"); p.rect(15, 11, 15, 20, "c"); p.rect(16, 14, 16, 18, "z");
p.pts([[14, 13], [17, 13], [14, 17], [17, 17]], "g"); p.pts([[13, 15], [18, 15]], "z");
p.rect(11, 8, 20, 8, "h"); p.rect(10, 7, 21, 8, "l"); p.rect(10, 7, 21, 7, "h"); p.rect(19, 8, 21, 8, "m");
// 浮かぶ灯り石
p.poly([[16, 0], [20, 3], [16, 6], [12, 3]], "g"); p.poly([[16, 1], [13, 3], [16, 5]], "c"); p.poly([[16, 5], [20, 3], [16, 6]], "z"); p.pts([[15, 2], [14, 3]], "C");
p.outline("o");
p.pts([[10, 2], [22, 4], [9, 5], [23, 1]], "p");
p.shadow(20, 29, 12, 1.6, "S");
export const rows = p.rows();
