import { painter } from "../../lib4.mjs";
export const name = "墓石";
export const category = "object";
export const pal = { o: "#1c1c28", h: "#dcdce4", l: "#b8b8c8", m: "#8e8ea4", d: "#666680", e: "#484860", g: "#4c7a3c", G: "#7cae54", n: "#3a5a2c", B: "#6a4c38", b: "#8a6a50", f: "#f4e4f8", y: "#f0d060", S: "#22262a" };
const p = painter();
// 土もり
p.blob(16, 25, 12, 4, ["n", "g", "G"]); p.rect(5, 25, 26, 26, "g"); p.rect(22, 26, 27, 26, "n"); p.ell(16, 26, 11, 2.5, "B"); p.pts([[8, 25], [10, 26], [13, 26]], "b");
p.blob(16, 24, 11, 3.3, ["n", "g", "G"]);
p.pts([[8, 23], [10, 22], [21, 23], [23, 23]], "G");
// 石碑
p.rect(10, 9, 21, 24, "l"); p.ell(15.5, 9, 6, 5.5, "l"); p.rect(10, 9, 12, 24, "h"); p.rect(19, 12, 21, 24, "m"); p.rect(21, 12, 21, 24, "d");
for (let y = 6; y <= 12; y++) for (let x = 10; x <= 21; x++) if (p.get(x, y) !== ".") p.put(x, y, x < 13 ? "h" : x > 18 ? "m" : "l");
p.rect(9, 24, 22, 25, "d"); p.rect(9, 24, 22, 24, "m");
// 十字のほり
p.rect(15, 10, 16, 18, "e"); p.rect(12, 12, 19, 13, "e"); p.rect(15, 10, 15, 18, "d"); p.rect(12, 12, 19, 12, "d");
// ひび・こけ
p.pts([[18, 16], [19, 17], [19, 18], [20, 19]], "d"); p.pts([[11, 21], [12, 22], [11, 23], [13, 23]], "g"); p.pts([[12, 22]], "G");
// 花
p.pts([[7, 24], [24, 24]], "f"); p.pts([[7, 25], [24, 25]], "y");
p.outline("o");
p.shadow(21, 28, 10, 1.6, "S");
export const rows = p.rows();
