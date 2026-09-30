import { painter } from "../../lib4.mjs";
export const name = "井戸";
export const category = "object";
export const pal = { o: "#241c28", s: "#8a8494", c: "#b0aab8", h: "#d8d4dc", d: "#5e586c", e: "#3e3850", W: "#2a5a88", V: "#4a90c0", t: "#7a4c2c", T: "#a87040", u: "#4a2c1c", r: "#2c7a72", R: "#4ca898", q: "#88d4c0", y: "#c8b078", S: "#28282a" };
const p = painter();
// 石の囲い
p.rect(5, 19, 26, 27, "s"); p.ell(16, 20, 11, 6, "c"); p.ell(16, 21, 8.5, 4, "e"); p.ell(16, 22, 7.5, 3, "W"); p.pts([[12, 21], [13, 21], [18, 22], [19, 22]], "V");
p.rect(5, 20, 26, 27, "s"); p.ell(16, 20, 11, 6, "c"); p.rect(5, 21, 26, 26, "s"); p.ell(16, 21, 8.5, 4, "e"); p.ell(16, 22, 7.5, 3, "W"); p.pts([[12, 21], [13, 21], [18, 22], [19, 22]], "V");
p.rect(5, 24, 26, 27, "s"); p.rect(20, 24, 26, 27, "d"); p.rect(23, 21, 26, 24, "d");
for (let x = 6; x < 26; x += 5) for (const y of [25]) p.rect(x, y, x, y + 2, "d");
p.rect(5, 27, 26, 27, "d");
p.pts([[7, 22], [8, 22], [6, 23], [14, 17], [15, 17], [9, 18]], "h");
// 柱と屋根
p.rect(7, 9, 8, 20, "t"); p.rect(7, 9, 7, 20, "T"); p.rect(24, 9, 25, 20, "t"); p.rect(25, 9, 25, 20, "u"); p.rect(24, 9, 24, 20, "t");
p.poly([[16, 2], [3, 10], [29, 10]], "r");
for (let y = 2; y < 10; y++) { const w = Math.round(13 * (y - 1) / 8); for (let x = 16 - w; x < 16 + w; x++) p.put(x, y, (x - 16) / Math.max(w, 1) < -0.2 ? "R" : (y % 3 === 0 ? "u" : "r")); }
p.pts([[16, 2], [15, 3], [14, 5], [12, 7]], "q"); p.rect(3, 10, 28, 10, "u");
// 綱と桶
p.rect(16, 11, 16, 16, "y"); p.rect(14, 12, 18, 12, "T"); p.rect(14, 12, 14, 12, "T");
p.rect(14, 17, 18, 19, "t"); p.rect(14, 17, 18, 17, "T"); p.rect(14, 19, 18, 19, "u"); p.pts([[15, 18], [17, 18]], "s");
p.outline("o");
p.shadow(20, 29, 12, 1.6, "S");
export const rows = p.rows();
