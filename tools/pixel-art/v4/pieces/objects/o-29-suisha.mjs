import { painter } from "../../lib4.mjs";
export const name = "水車";
export const category = "object";
export const pal = { o: "#241a14", h: "#d8a468", T: "#b47c44", t: "#8a5632", d: "#623c22", u: "#3e2416", s: "#8e8898", c: "#bab4c0", e: "#5c566a", W: "#3a72b0", V: "#6cb0e0", D: "#264c80", q: "#d8f0ff", i: "#4a4a5a", S: "#1c2c44" };
const p = painter();
// 池
p.ell(16, 27, 14, 3.4, "W"); p.rect(3, 27, 28, 28, "W"); p.ell(16, 28, 11, 2, "D"); p.pts([[6, 27], [7, 27], [24, 28], [25, 28], [12, 29], [19, 26]], "V");
// 石の支え
p.rect(1, 20, 6, 27, "s"); p.rect(1, 20, 6, 20, "c"); p.rect(1, 20, 2, 27, "c"); p.rect(5, 21, 6, 27, "e");
p.rect(25, 20, 30, 27, "s"); p.rect(25, 20, 30, 20, "c"); p.rect(25, 20, 26, 27, "c"); p.rect(29, 21, 30, 27, "e");
// 水車の輪
const cx = 16, cy = 15;
p.ell(cx, cy, 11, 11, "t"); p.ell(cx, cy, 8.6, 8.6, "d");
for (let a = 0; a < 12; a++) { const t = (a / 12) * Math.PI * 2 + 0.26; const x = cx + Math.cos(t) * 11, y = cy + Math.sin(t) * 11; p.rect(Math.round(x) - 1, Math.round(y) - 1, Math.round(x), Math.round(y), "h"); p.put(Math.round(x) + 1, Math.round(y) + 1, "u"); }
p.ell(cx, cy, 8.4, 8.4, "d");
for (let a = 0; a < 8; a++) { const t = (a / 8) * Math.PI * 2 + 0.39; p.line(cx, cy, Math.round(cx + Math.cos(t) * 9), Math.round(cy + Math.sin(t) * 9), a % 2 ? "T" : "h"); }
p.ell(cx, cy, 8.4, 8.4, "d"); 
for (let a = 0; a < 8; a++) { const t = (a / 8) * Math.PI * 2 + 0.39; p.line(cx, cy, Math.round(cx + Math.cos(t) * 8), Math.round(cy + Math.sin(t) * 8), a % 4 < 2 ? "T" : "t"); }
p.ell(cx, cy, 2.4, 2.4, "i"); p.ell(cx, cy, 1.2, 1.2, "c");
p.pts([[6, 8], [7, 6], [9, 4]], "h");
// 樋（上から水）
p.rect(14, 0, 28, 2, "t"); p.rect(14, 0, 28, 0, "h"); p.rect(14, 2, 28, 2, "u"); p.rect(15, 1, 27, 1, "V");
p.rect(24, 2, 26, 8, "V"); p.rect(24, 2, 24, 8, "q"); p.rect(26, 3, 26, 8, "W"); p.pts([[27, 9], [23, 10]], "V");
p.despeckle();
p.outline("o");
p.pts([[25, 5], [25, 7]], "q");
p.shadow(20, 30, 10, 1, "S");
export const rows = p.rows();
