import { painter } from "../../lib4.mjs";
export const name = "風車";
export const category = "object";
export const pal = { o: "#2a2018", w: "#ece0c4", v: "#c8b48c", b: "#9a8460", r: "#b04a3c", R: "#d87058", z: "#7c2e2c", t: "#7a4c2c", T: "#a87040", u: "#4a2c1c", c: "#f6f2e8", d: "#d8d0bc", B: "#5a8ad0", S: "#2a2c22" };
const p = painter();
// 塔（先細り）
p.poly([[11, 13], [21, 13], [25, 27], [7, 27]], "w");
for (let y = 13; y <= 27; y++) { const f = (y - 13) / 14; const x0 = Math.round(11 - 4 * f), x1 = Math.round(21 + 4 * f); for (let x = x0; x < x1; x++) p.put(x, y, x - x0 < (x1 - x0) * 0.28 ? "c" : x - x0 > (x1 - x0) * 0.68 ? "b" : "w"); if (y % 4 === 0) for (let x = x0; x < x1; x++) if ((x + y) % 2 === 0 && x - x0 > (x1 - x0) * 0.6) p.put(x, y, "v"); }
p.rect(7, 26, 24, 27, "b"); p.rect(7, 26, 12, 26, "v");
// 扉と窓
p.rect(14, 21, 18, 27, "t"); p.rect(14, 21, 14, 27, "u"); p.pts([[17, 25]], "T"); p.rect(15, 21, 17, 21, "u");
p.rect(15, 16, 17, 18, "B"); p.rect(16, 16, 16, 18, "t"); p.rect(15, 17, 17, 17, "t");
// 屋根
p.poly([[16, 4], [7, 13], [25, 13]], "r");
for (let y = 4; y < 13; y++) { const w = Math.round(9 * (y - 3) / 9); for (let x = 16 - w; x < 16 + w; x++) p.put(x, y, (x - 16) / Math.max(w, 1) < -0.3 ? "R" : (x - 16) / Math.max(w, 1) > 0.35 ? "z" : "r"); }
p.rect(7, 13, 25, 13, "z");
// 羽根（4枚）
const hub = [16, 10];
const arm = (dx, dy) => { const L = 12; const ex = hub[0] + dx * L, ey = hub[1] + dy * L; const px = -dy, py = dx; const s = 0.42; p.poly([[hub[0] + dx * 3, hub[1] + dy * 3], [ex, ey], [ex + px * 4.6, ey + py * 4.6], [hub[0] + dx * 3 + px * 3.4, hub[1] + dy * 3 + py * 3.4]], "c"); p.poly([[hub[0] + dx * 3 + px * 3.4, hub[1] + dy * 3 + py * 3.4], [ex + px * 4.6, ey + py * 4.6], [ex + px * 3.6, ey + py * 3.6], [hub[0] + dx * 3 + px * 2.4, hub[1] + dy * 3 + py * 2.4]], "d"); p.line(hub[0], hub[1], Math.round(ex), Math.round(ey), "t"); };
const k = Math.SQRT1_2; arm(-k, -k); arm(k, -k); arm(-k, k); arm(k, k);
p.rect(15, 9, 17, 11, "T"); p.put(16, 10, "u"); p.put(15, 9, "c");
p.outline("o");
p.shadow(20, 29, 12, 1.6, "S");
export const rows = p.rows();
