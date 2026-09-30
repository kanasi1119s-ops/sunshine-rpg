import { painter } from "../../lib4.mjs";
export const name = "宝箱（開）";
export const category = "object";
export const pal = { o: "#241008", h: "#e8b078", T: "#c08048", t: "#8e5630", d: "#6a3a22", u: "#3e2014", g: "#e8b830", G: "#fff0a0", n: "#a07818", L: "#a03038", l: "#c85860", z: "#6a1c28", S: "#282422", w: "#ffffff", b: "#5a8ad0", r: "#e05060" };
const p = painter();
// 開いたふた（奥に立つ・内側が見える）
p.rect(5, 2, 26, 11, "t"); p.rect(5, 2, 26, 2, "T"); p.rect(5, 2, 6, 11, "T"); p.rect(25, 3, 26, 11, "d");
p.rect(8, 4, 23, 10, "L"); p.rect(8, 4, 23, 5, "z"); p.rect(8, 4, 8, 10, "z"); for (let x = 10; x < 23; x += 3) p.rect(x, 6, x, 10, "l");
p.rect(8, 10, 23, 10, "z");
// 箱の口（宝の山）
p.poly([[6, 11], [25, 11], [27, 17], [4, 17]], "u");
p.blob(16, 14, 9, 3.4, ["n", "g", "G"]);
p.pts([[11, 12], [14, 11], [18, 12], [21, 12], [9, 14], [23, 14], [16, 13]], "G"); p.pts([[12, 14], [19, 14], [15, 15], [22, 15]], "n");
p.rect(19, 12, 20, 13, "b"); p.put(19, 12, "w"); p.rect(10, 12, 11, 13, "r"); p.put(10, 12, "w");
// 前面
p.rect(4, 17, 27, 27, "d"); p.rect(4, 17, 5, 27, "t"); p.rect(26, 17, 27, 27, "u"); p.rect(4, 17, 27, 18, "t"); p.rect(4, 26, 27, 27, "u");
for (const y of [21, 24]) for (let x = 6; x < 26; x++) if ((x + y) % 6 === 0) p.put(x, y, "u");
for (const x0 of [7, 22]) { p.rect(x0, 17, x0 + 2, 27, "g"); p.rect(x0, 17, x0, 27, "G"); p.rect(x0 + 2, 18, x0 + 2, 27, "n"); }
p.rect(4, 26, 27, 27, "u"); for (const [x, y] of [[4, 18], [27, 18], [4, 26], [27, 26]]) p.put(x, y, "g");
p.rect(13, 18, 18, 22, "g"); p.rect(13, 18, 18, 18, "G"); p.rect(18, 19, 18, 22, "n"); p.rect(15, 20, 16, 21, "u");
p.outline("o");
p.pts([[2, 12], [29, 8], [16, 1]], "G");
p.shadow(19, 29, 12, 1.6, "S");
export const rows = p.rows();
