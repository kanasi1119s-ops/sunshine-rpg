import { painter } from "../../lib4.mjs";
export const name = "テント";
export const category = "object";
export const pal = { o: "#2c1c18", h: "#f6e6b8", l: "#e4c888", m: "#c8a462", d: "#9c7444", e: "#6c4a30", r: "#c8483c", R: "#e8786a", z: "#8a2c2c", k: "#2a1c20", K: "#4a3438", t: "#7a4c2c", y: "#d8c8a0", S: "#2a2a22" };
const p = painter();
// 杭
p.rect(1, 26, 2, 28, "t"); p.rect(29, 26, 30, 28, "t"); p.put(1, 26, "m");
// 幕（前の三角）
for (let y = 5; y <= 26; y++) { const w = 14 * (y - 4) / 22; for (let x = Math.round(16 - w); x < Math.round(16 + w); x++) { const rel = (x - 16) / Math.max(w, 1); let c = rel < -0.45 ? "h" : rel < 0.05 ? "l" : rel < 0.55 ? "m" : "d"; if (y >= 21 && y <= 23) c = rel < 0 ? "R" : rel < 0.5 ? "r" : "z"; p.put(x, y, c); } }
for (let y = 5; y <= 26; y++) { const w = 14 * (y - 4) / 22; p.put(Math.round(16 - w), y, "R"); p.put(Math.round(16 + w) - 1, y, "z"); }
p.rect(2, 25, 29, 26, "e"); p.rect(2, 25, 12, 25, "d");
// 入口
p.poly([[16, 11], [22, 25], [10, 25]], "k"); p.poly([[16, 11], [19, 25], [13, 25]], "K");
p.line(16, 10, 9, 24, "d"); p.line(16, 10, 23, 24, "e");
p.line(15, 11, 10, 22, "l");
// 先端の棒と小旗
p.rect(16, 1, 16, 4, "t"); p.poly([[17, 1], [21, 2.5], [17, 4]], "r");
p.outline("o");
p.shadow(19, 29, 13, 1.6, "S");
export const rows = p.rows();
