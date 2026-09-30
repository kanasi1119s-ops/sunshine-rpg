import { painter } from "../../lib4.mjs";
export const name = "樽";
export const category = "object";
export const pal = { o: "#26140c", h: "#e4b47c", T: "#c48c54", t: "#9c6838", d: "#744826", u: "#4a2c18", i: "#5a6478", I: "#98a4bc", j: "#3a4054", S: "#282220" };
const p = painter();
for (let y = 10; y <= 27; y++) { const hw = 7.5 + 1.6 * Math.sin(Math.PI * (y - 9) / 19); const x0 = Math.round(16 - hw), x1 = Math.round(15 + hw); for (let x = x0; x <= x1; x++) { const rel = (x - x0) / (x1 - x0); let c = rel < 0.18 ? "h" : rel < 0.45 ? "T" : rel < 0.75 ? "t" : "d"; if ((x - x0) % 4 === 3 && rel > 0.2) c = "u"; p.put(x, y, c); } }
// 上のふた
p.ell(15.5, 10, 8, 3.6, "d"); p.ell(15.5, 10, 7, 2.9, "T"); p.ell(15, 9.6, 5.5, 2, "h");
p.pts([[9, 11], [10, 12], [21, 11], [22, 10]], "t");
for (let x = 10; x <= 21; x += 4) p.pts([[x, 9], [x + 1, 10]], "t");
// たが（鉄の輪）
for (const y of [14, 22]) for (let x = 8; x <= 23; x++) { const hw = 7.5 + 1.6 * Math.sin(Math.PI * (y - 9) / 19); if (Math.abs(x - 15.5) <= hw + 0.3) { p.put(x, y, x < 12 ? "I" : x > 19 ? "j" : "i"); p.put(x, y + 1, x < 20 ? "i" : "j"); } }
p.pts([[10, 14], [11, 22]], "I");
p.rect(9, 27, 22, 27, "u");
p.outline("o");
p.shadow(19, 28, 10, 2, "S");
export const rows = p.rows();
