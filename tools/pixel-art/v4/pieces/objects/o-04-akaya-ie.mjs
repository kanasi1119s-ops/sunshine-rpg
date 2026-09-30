import { painter } from "../../lib4.mjs";
export const name = "赤い屋根の家";
export const category = "object";
export const pal = { o: "#2c1a18", r: "#9c3a34", R: "#c85448", q: "#e07a5c", H: "#f4a684", z: "#6a2426", w: "#e8d8b4", v: "#c4b088", b: "#8e7a5c", t: "#6a4428", u: "#402618", B: "#5a8ad0", W: "#a8d0f0", s: "#7a7688", K: "#4a4458", S: "#2c2a26" };
const p = painter();
// 煙突
p.rect(21, 2, 25, 8, "s"); p.rect(21, 2, 25, 3, "K"); p.rect(24, 4, 25, 8, "K"); p.pts([[21, 4], [22, 6]], "w");
// 屋根（斜め上から見た台形）
p.poly([[9, 4], [23, 4], [30, 16], [2, 16]], "R");
for (let y = 4; y < 16; y++) { const f = (y - 4) / 12; const x0 = Math.round(9 - 7 * f), x1 = Math.round(23 + 7 * f); for (let x = x0; x < x1; x++) { let c = (y % 3 === 0) ? "z" : (y % 3 === 1 ? "R" : "r"); if (y % 3 === 1 && (x + y) % 6 === 0) c = "q"; if (x - x0 < (x1 - x0) * 0.2 && y % 3 === 1) c = "q"; if (x - x0 > (x1 - x0) * 0.8 && y % 3 !== 0) c = "r"; p.put(x, y, c); } }
p.rect(9, 4, 22, 4, "H");
// 壁
p.rect(4, 16, 27, 27, "w"); p.rect(4, 17, 27, 18, "v"); p.rect(24, 19, 27, 27, "v"); p.rect(4, 26, 27, 27, "b");
for (let x = 6; x < 26; x += 4) p.pts([[x, 27]], "o");
// 窓
p.rect(6, 20, 11, 24, "t"); p.rect(7, 21, 10, 23, "B"); p.pts([[7, 21], [8, 21]], "W"); p.rect(8, 21, 8, 23, "W"); p.rect(7, 22, 10, 22, "t");
p.rect(20, 20, 24, 24, "t"); p.rect(21, 21, 23, 23, "B"); p.pts([[21, 21], [21, 22]], "W"); p.rect(22, 21, 22, 23, "t");
// 扉
p.rect(14, 20, 18, 27, "t"); p.rect(14, 20, 14, 27, "u"); p.rect(18, 20, 18, 27, "u"); p.pts([[17, 24]], "H");
p.outline("o");
p.shadow(20, 29, 12, 1.6, "S");
export const rows = p.rows();
