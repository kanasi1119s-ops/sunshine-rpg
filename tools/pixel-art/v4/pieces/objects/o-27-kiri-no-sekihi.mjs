import { painter } from "../../lib4.mjs";
export const name = "霧の石碑";
export const category = "object";
export const pal = { o: "#1c2034", h: "#b4c0d8", l: "#8c9ab8", m: "#65729a", d: "#454f78", e: "#2c3458", g: "#c8a8ff", G: "#f0e4ff", z: "#8a5cd0", f: "#e4eaf6", F: "#b8c4dc", M: "#8e9cc0", S: "#2a3048" };
const p = painter();
// 石碑（上がとがる）
p.poly([[16, 2], [22, 6], [23, 24], [9, 24], [10, 6]], "m");
p.poly([[16, 2], [10, 6], [9, 24], [13, 24], [13, 7]], "l"); p.poly([[16, 2], [13, 5], [11, 7], [16, 4]], "h"); p.rect(9, 8, 10, 24, "h");
p.poly([[16, 2], [22, 6], [23, 24], [19, 24], [19, 6]], "d"); p.rect(22, 8, 23, 24, "e");
p.rect(9, 23, 23, 24, "e"); p.rect(9, 23, 12, 23, "d");
// 光る文様
p.rect(15, 8, 16, 9, "g"); p.rect(13, 11, 18, 11, "g"); p.rect(15, 11, 16, 17, "g"); p.rect(13, 14, 14, 14, "z"); p.rect(17, 14, 18, 14, "z"); p.rect(14, 17, 17, 17, "g"); p.rect(15, 19, 16, 20, "z");
p.pts([[15, 8], [15, 11], [15, 12]], "G");
p.pts([[13, 9], [18, 9], [12, 13], [19, 13]], "z");
// ひび
p.pts([[11, 18], [12, 19], [12, 20]], "d");
p.outline("o");
// 霧のもや
const mist = (cx, cy, rx, ry) => { for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) if (((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1) { const t = (y - cy) / ry; p.put(x, y, t < -0.3 ? "f" : t < 0.4 ? "F" : "M"); } };
mist(7, 26, 6, 2.6); mist(23, 27, 7, 2.6); mist(15, 28, 7, 2); mist(27, 22, 3, 1.8); mist(3, 22, 3, 1.8); mist(16, 25, 6, 1.8);
p.pts([[2, 19], [29, 18]], "F");
export const rows = p.rows();
