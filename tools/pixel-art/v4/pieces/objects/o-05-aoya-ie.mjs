import { painter } from "../../lib4.mjs";
export const name = "青い屋根の家";
export const category = "object";
export const pal = { o: "#141c34", e: "#1e2c58", d: "#2c4a8c", m: "#4272bc", l: "#68a0e0", h: "#a8d4f8", s: "#8a8a98", c: "#a8a8b4", k: "#68687a", z: "#4a4a5c", t: "#6a4428", u: "#402618", Y: "#f8dc70", A: "#c89838", S: "#262a30" };
const p = painter();
// 切妻の屋根（正面に三角）
p.poly([[16, 2], [2, 15], [30, 15]], "m");
for (let y = 2; y < 15; y++) { const w = Math.round(14 * (y - 1) / 13); for (let x = 16 - w; x < 16 + w; x++) { const rel = (x - 16) / Math.max(w, 1); let c = rel < -0.3 ? "l" : rel < 0.3 ? "m" : "d"; if ((y - 2) % 4 === 3) c = rel < 0 ? "d" : "e"; p.put(x, y, c); } }
p.pts([[16, 2], [15, 3], [16, 3], [14, 5]], "h");
p.rect(2, 15, 29, 16, "e"); p.rect(2, 15, 12, 15, "d");
// 壁（石積み）
p.rect(5, 17, 26, 27, "s"); p.rect(23, 17, 26, 27, "c"); p.rect(5, 17, 8, 27, "c");
p.rect(23, 17, 26, 27, "k");
for (let y = 19; y <= 25; y += 3) for (let x = 5; x <= 26; x++) p.put(x, y, "k");
for (let y = 17; y <= 27; y++) { const off = ((y - 17) / 3 | 0) % 2 ? 3 : 0; for (let x = 9 + off; x < 23; x += 6) if ((y - 17) % 3 !== 2) p.put(x, y, "k"); }
p.rect(5, 27, 26, 27, "z");
// 屋根裏の丸窓
p.ell(16, 10, 2.4, 2.4, "t"); p.ell(16, 10, 1.6, 1.6, "Y"); p.pts([[15, 9]], "h"); p.pts([[17, 11]], "A");
// アーチの扉
p.rect(13, 21, 18, 27, "t"); p.pts([[13, 21], [18, 21]], "s"); p.rect(14, 20, 17, 20, "t"); p.rect(13, 21, 13, 27, "u"); p.rect(18, 21, 18, 27, "u"); p.pts([[17, 25]], "Y");
// 窓
p.rect(7, 20, 10, 23, "t"); p.rect(8, 21, 9, 22, "Y"); p.rect(21, 20, 24, 23, "t"); p.rect(22, 21, 23, 22, "Y");
p.outline("o");
p.shadow(19, 29, 12, 1.6, "S");
export const rows = p.rows();
