import { painter } from "../../lib4.mjs";
export const name = "帆走車";
export const category = "object";
export const pal = { o: "#2c1c14", w: "#f4ecd4", c: "#d8cca8", a: "#38b8b0", A: "#68e0d0", z: "#1e7a80", t: "#8a5632", T: "#b47a44", h: "#e0a868", u: "#4c2e1c", i: "#4a4a5a", I: "#8a8a9c", k: "#2a2a34", y: "#e8c050", r: "#c8443c", S: "#3a3020" };
const p = painter();
// 帆柱
p.rect(15, 3, 16, 20, "u"); p.rect(15, 3, 15, 20, "t");
// 三角の帆（縞）
p.poly([[14, 4], [14, 18], [2, 18]], "w"); p.poly([[17, 5], [29, 18], [17, 18]], "w");
for (let y = 4; y <= 18; y++) { for (let x = 1; x <= 30; x++) if (p.get(x, y) === "w") { const band = Math.floor((y - 4) / 3) % 2 === 0; const left = x < 15; p.put(x, y, band ? (left ? "A" : "a") : (left ? "w" : "c")); } }
p.line(15, 4, 3, 18, "z"); p.line(17, 5, 29, 18, "z");
p.line(3, 18, 14, 18, "z"); p.line(17, 18, 28, 18, "z");
p.pts([[16, 2], [17, 2], [18, 3]], "r"); p.rect(15, 2, 15, 3, "r");
// 車体
p.rect(5, 19, 26, 21, "t"); p.rect(5, 19, 26, 19, "h"); p.rect(5, 21, 26, 21, "u"); p.rect(3, 22, 28, 23, "T"); p.rect(3, 22, 28, 22, "h"); p.rect(3, 23, 28, 23, "t");
p.rect(11, 20, 12, 20, "y"); p.rect(19, 20, 20, 20, "y");
p.line(4, 21, 1, 19, "u"); p.pts([[1, 19], [2, 19]], "T");
// 車輪
const wheel = (cx, cy, r) => { p.ell(cx, cy, r, r, "k"); p.ell(cx, cy, r - 1.5, r - 1.5, "i"); p.ell(cx, cy, 1.5, 1.5, "I"); p.line(cx - r + 1, cy, cx + r - 1, cy, "I"); p.line(cx, cy - r + 1, cx, cy + r - 1, "I"); p.line(cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2, "k"); p.line(cx + r - 2, cy - r + 2, cx - r + 2, cy + r - 2, "k"); p.pts([[cx - r + 1, cy - 2], [cx - 2, cy - r + 1]], "I"); };
wheel(9, 26, 4); wheel(23, 26, 4); p.rect(14, 24, 18, 25, "u"); p.ell(16, 26, 2, 2, "i");
p.despeckle();
p.outline("o", true);
p.shadow(18, 29, 14, 1.6, "S");
export const rows = p.rows();
