import { painter } from "../../lib4.mjs";
export const name = "灯台";
export const category = "object";
export const pal = { o: "#1c2030", w: "#f0ece0", d: "#c0bcb4", k: "#8c8890", r: "#c8443c", R: "#e8746c", z: "#8a2c34", y: "#ffe888", Y: "#fff8d0", i: "#4a5068", I: "#7a8098", s: "#6c6470", c: "#8e8696", e: "#443e50", S: "#22262c", b: "#3a6a98" };
const p = painter();
// 岩の土台
p.blob(16, 26, 13, 4, ["e", "s", "c", "d"]); p.rect(3, 26, 29, 27, "s"); p.pts([[5, 25], [6, 25], [10, 24], [24, 25]], "c");
// 塔の本体
for (let y = 12; y <= 25; y++) { const f = (y - 12) / 13; const x0 = Math.round(12 - 3 * f), x1 = Math.round(20 + 3 * f); const band = Math.floor((y - 12) / 4) % 2 === 0; for (let x = x0; x < x1; x++) { const rel = (x - x0) / (x1 - x0); let c = band ? (rel < 0.3 ? "R" : rel < 0.7 ? "r" : "z") : (rel < 0.3 ? "w" : rel < 0.7 ? "d" : "k"); p.put(x, y, c); } }
p.rect(14, 22, 17, 25, "i"); p.rect(14, 22, 14, 25, "I"); p.pts([[16, 24]], "y");
p.rect(15, 15, 16, 17, "b"); p.pts([[15, 15]], "R");
// 回廊
p.rect(8, 11, 24, 12, "i"); p.rect(8, 11, 24, 11, "I"); p.pts([[8, 10], [10, 10], [12, 10], [20, 10], [22, 10], [24, 10]], "i");
// 灯室
p.rect(11, 5, 21, 10, "y"); p.rect(12, 6, 15, 9, "Y"); p.rect(19, 6, 20, 9, "y");
for (const x of [11, 16, 21]) p.rect(x, 5, x, 10, "i");
p.rect(11, 8, 21, 8, "i");
p.pts([[13, 6], [14, 6], [13, 7]], "w");
// 屋根
p.poly([[16, 1], [10, 5], [22, 5]], "z"); p.poly([[16, 1], [10, 5], [15, 5]], "r"); p.rect(10, 5, 22, 5, "e"); p.pts([[16, 0]], "I");
p.outline("o");
p.pts([[5, 8], [6, 8], [7, 8], [25, 8], [26, 8], [27, 8], [4, 5], [28, 5], [5, 11], [27, 11]], "y");
p.shadow(20, 29, 12, 1.6, "S");
export const rows = p.rows();
