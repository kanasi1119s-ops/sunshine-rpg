import { painter } from "../../lib4.mjs";
export const name = "宝箱（閉）";
export const category = "object";
export const pal = { o: "#241008", h: "#e8b078", T: "#c08048", t: "#8e5630", d: "#6a3a22", u: "#3e2014", g: "#e8b830", G: "#fff0a0", n: "#a07818", b: "#2a1a3a", S: "#282422" };
const p = painter();
// ふたの上面
p.poly([[8, 8], [23, 8], [27, 12], [4, 12]], "T"); p.poly([[8, 8], [15, 8], [11, 10], [6, 11]], "h");
for (const x of [9, 13, 18, 22]) p.pts([[x, 9]], "t");
// ふたの前面
p.rect(4, 12, 27, 17, "t"); p.rect(4, 12, 27, 12, "T"); p.rect(4, 12, 5, 17, "T"); p.rect(26, 13, 27, 17, "d"); p.rect(4, 17, 27, 17, "u");
for (const x of [10, 15, 20]) p.rect(x, 13, x, 16, "d");
// 箱本体
p.rect(4, 18, 27, 27, "d"); p.rect(4, 18, 5, 27, "t"); p.rect(26, 18, 27, 27, "u"); p.rect(4, 18, 27, 18, "t"); p.rect(4, 26, 27, 27, "u");
for (const y of [21, 24]) for (let x = 6; x < 26; x++) if ((x + y) % 6 === 0) p.put(x, y, "u");
// 金の帯・角
for (const x0 of [7, 22]) { p.rect(x0, 8, x0 + 2, 27, "g"); p.rect(x0, 8, x0, 27, "G"); p.rect(x0 + 2, 9, x0 + 2, 27, "n"); }
p.rect(4, 26, 27, 27, "u"); for (const [x, y] of [[4, 18], [27, 18], [4, 26], [27, 26]]) p.put(x, y, "g");
p.rect(4, 18, 27, 18, "n");
// 錠前
p.rect(13, 15, 18, 21, "g"); p.rect(13, 15, 18, 15, "G"); p.rect(13, 15, 13, 21, "G"); p.rect(18, 16, 18, 21, "n"); p.rect(15, 17, 16, 19, "b"); p.put(15, 20, "b");
p.outline("o");
p.shadow(19, 29, 12, 1.6, "S");
export const rows = p.rows();
