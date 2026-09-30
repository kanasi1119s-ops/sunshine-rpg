import { painter } from "../../lib4.mjs";
export const name = "掲示板";
export const category = "object";
export const pal = { o: "#241a14", h: "#c89c62", t: "#94683c", d: "#684424", u: "#40281a", w: "#f6f2e4", c: "#d4ceb8", y: "#f2d878", Y: "#c8a848", r: "#d85a50", b: "#5a86c8", p: "#8a2c34", k: "#4a4a58", S: "#282824" };
const p = painter();
// 脚
p.rect(7, 18, 9, 27, "t"); p.rect(7, 18, 7, 27, "h"); p.rect(9, 18, 9, 27, "d"); p.rect(22, 18, 24, 27, "t"); p.rect(22, 18, 22, 27, "h"); p.rect(24, 18, 24, 27, "d");
p.rect(5, 27, 11, 27, "u"); p.rect(20, 27, 26, 27, "u");
// 屋根板
p.poly([[4, 3], [27, 3], [29, 7], [2, 7]], "t"); p.poly([[4, 3], [27, 3], [26, 4], [5, 4]], "h"); p.rect(2, 7, 29, 8, "d");
// 板
p.rect(4, 8, 27, 19, "t"); p.rect(4, 8, 27, 9, "d"); p.rect(4, 8, 5, 19, "h"); p.rect(26, 9, 27, 19, "d"); p.rect(4, 18, 27, 19, "u"); p.rect(4, 17, 4, 17, "h");
p.rect(6, 10, 25, 17, "d"); p.rect(6, 10, 25, 10, "u");
// 貼り紙
p.rect(7, 11, 12, 16, "w"); p.rect(7, 11, 12, 11, "c"); for (const y of [13, 15]) p.rect(8, y, 11, y, "k");
p.rect(14, 11, 18, 14, "y"); p.rect(14, 11, 18, 11, "Y"); p.rect(15, 13, 17, 13, "Y");
p.rect(20, 11, 24, 16, "w"); p.rect(20, 11, 24, 11, "c"); p.rect(21, 13, 23, 13, "b"); p.rect(21, 15, 23, 15, "k");
p.rect(14, 15, 18, 16, "r"); p.rect(14, 15, 18, 15, "p");
p.pts([[9, 11], [16, 11], [22, 11], [16, 15]], "r");
p.pts([[9, 11], [22, 11]], "b");
p.outline("o");
p.shadow(20, 29, 11, 1.6, "S");
export const rows = p.rows();
