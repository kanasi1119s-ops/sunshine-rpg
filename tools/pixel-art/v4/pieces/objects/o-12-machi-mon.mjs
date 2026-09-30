import { painter } from "../../lib4.mjs";
export const name = "町の門";
export const category = "object";
export const pal = { o: "#241e2c", h: "#d8d0c0", l: "#b4ac9c", m: "#8e8678", d: "#665e64", e: "#463e4c", k: "#1e1a26", t: "#7a4c2c", T: "#a87040", u: "#4a2c1c", r: "#c04038", R: "#e8746c", y: "#f0c850", i: "#4a5068", f: "#a08a58", S: "#26262a" };
const p = painter();
// 左右の塔
const tower = (x0, x1) => { p.rect(x0, 8, x1, 27, "m"); p.rect(x0, 8, x0 + 2, 27, "l"); p.rect(x1 - 2, 8, x1, 27, "d"); p.rect(x0, 8, x1, 9, "h"); p.rect(x0, 10, x1, 10, "d");
  for (let x = x0; x <= x1; x += 3) p.rect(x, 5, Math.min(x + 1, x1), 7, "l"); p.rect(x0, 7, x1, 7, "m"); p.rect(x0, 6, x0, 7, "h");
  for (const y of [14, 19, 24]) for (let x = x0; x <= x1; x++) if ((x + y) % 5 !== 0) p.put(x, y, "d");
  p.rect((x0 + x1) / 2 | 0, 12, ((x0 + x1) / 2 | 0) + 1, 15, "k"); };
tower(2, 9); tower(22, 29);
// 旗
p.rect(5, 1, 5, 5, "u"); p.poly([[6, 1], [11, 2.5], [6, 4.5]], "r"); p.pts([[6, 2]], "R");
p.rect(26, 1, 26, 5, "u"); p.poly([[27, 1], [31, 2.5], [27, 4.5]], "r");
// 門の上の壁とアーチ
p.rect(10, 12, 21, 27, "l"); p.rect(10, 12, 21, 13, "h"); p.rect(10, 14, 21, 14, "d");
for (let x = 10; x <= 21; x += 3) p.rect(x, 10, x + 1, 11, "l");
p.rect(10, 11, 21, 11, "l");
p.ell(16, 21, 5.5, 7, "e"); p.rect(11, 21, 20, 27, "e");
for (let y = 15; y <= 27; y++) for (let x = 10; x <= 21; x++) if ((y > 21 && x >= 11 && x <= 20) || ((x - 16) / 5.5) ** 2 + ((y - 21) / 7) ** 2 <= 1) p.put(x, y, y > 24 ? "d" : "k");
p.rect(11, 27, 20, 27, "f"); p.rect(13, 26, 18, 26, "f");
// 開いた扉
p.rect(11, 17, 12, 27, "t"); p.rect(11, 17, 11, 27, "T"); p.rect(19, 17, 20, 27, "t"); p.rect(20, 17, 20, 27, "u");
p.pts([[12, 22], [19, 22]], "y");
// かなめ石
p.rect(15, 13, 16, 14, "y"); p.put(15, 13, "h");
p.outline("o");
p.shadow(20, 29, 13, 1.6, "S");
export const rows = p.rows();
