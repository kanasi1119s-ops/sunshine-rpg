import { painter } from "../../lib4.mjs";
export const name = "砂漠のサボテン";
export const category = "object";
export const pal = { o: "#1c3020", d: "#2a5a3c", m: "#3e8a54", l: "#66b26a", h: "#a4dc8c", p: "#f0a0c0", P: "#ff6890", y: "#fff0a0", s: "#e8d094", a: "#c8a466", b: "#9c7a46", k: "#78604a", c: "#b4a488", S: "#8a6e44" };
const p = painter();
// 砂の盛り
p.blob(16, 27, 14, 3.6, ["b", "a", "s"]); p.pts([[5, 26], [7, 25], [25, 26], [27, 27]], "s");
p.ell(6, 27, 2.2, 1.6, "c"); p.pts([[5, 26]], "s"); p.put(7, 28, "k");
// 幹（縦の筋）
const col = (x0, x1, y0, y1) => { for (let x = x0; x <= x1; x++) for (let y = y0; y <= y1; y++) { const rel = (x - x0) / (x1 - x0); p.put(x, y, rel < 0.25 ? "h" : rel < 0.5 ? "l" : rel < 0.8 ? "m" : "d"); } p.ell((x0 + x1) / 2, y0, (x1 - x0) / 2 + 0.5, 2, "m"); for (let y = y0 - 2; y <= y0 + 1; y++) for (let x = x0; x <= x1; x++) if (((x - (x0 + x1) / 2) / ((x1 - x0) / 2 + 0.5)) ** 2 + ((y - y0) / 2.4) ** 2 <= 1) { const rel = (x - x0) / (x1 - x0); p.put(x, y, rel < 0.25 ? "h" : rel < 0.5 ? "l" : rel < 0.8 ? "m" : "d"); } };
col(13, 19, 6, 26);
for (const x of [15, 17]) for (let y = 8; y <= 26; y++) p.put(x, y, x === 15 ? "m" : "d");
// 左の腕
col(5, 8, 11, 17); p.rect(5, 16, 13, 19, "m"); p.rect(5, 16, 13, 16, "l"); p.rect(5, 19, 13, 19, "d"); p.rect(6, 12, 6, 16, "h");
// 右の腕
col(24, 27, 14, 20); p.rect(19, 19, 27, 22, "m"); p.rect(19, 19, 27, 19, "l"); p.rect(19, 22, 27, 22, "d"); p.rect(25, 15, 25, 19, "d");
// とげ・花
p.pts([[12, 10], [20, 12], [12, 20], [20, 24], [4, 13], [28, 16], [14, 24]], "y");
p.pts([[15, 4], [16, 4], [17, 4]], "p"); p.pts([[16, 3]], "P"); p.pts([[16, 5]], "P"); p.pts([[26, 11], [26, 12]], "p"); p.pts([[25, 12]], "P");
p.outline("o");
export const rows = p.rows();
