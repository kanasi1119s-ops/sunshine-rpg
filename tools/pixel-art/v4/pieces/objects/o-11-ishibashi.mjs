import { painter } from "../../lib4.mjs";
export const name = "石橋";
export const category = "object";
export const pal = { o: "#20242c", h: "#dcd8cc", l: "#bcb8ac", m: "#98948c", d: "#706c70", e: "#4c4858", W: "#3a6ea8", V: "#5a9cd0", D: "#264a7c", q: "#b8e0f4", g: "#5a8a48", S: "#1c2c44" };
const p = painter();
// 橋の腹（正面の壁）
p.poly([[3, 25], [3, 17], [7, 14], [25, 14], [29, 17], [29, 25]], "m");
// 天板（通路）
p.poly([[3, 17], [7, 9], [25, 9], [29, 17], [25, 14], [7, 14]], "l");
p.poly([[7, 9], [25, 9], [23, 11], [9, 11]], "h");
// 手すり（奥）と手前の縁
p.rect(7, 8, 24, 9, "d"); p.rect(7, 8, 24, 8, "m"); for (const x of [8, 15, 23]) p.rect(x, 6, x + 1, 8, "m");
for (const x of [8, 15, 23]) p.put(x, 6, "h");
p.rect(3, 15, 28, 16, "h"); p.rect(4, 17, 27, 17, "d");
p.rect(3, 17, 4, 25, "l"); p.rect(27, 17, 28, 25, "d");
// 石の目地
for (const y of [19, 22]) for (let x = 5; x < 27; x++) p.put(x, y, "d");
for (const [x, y] of [[8, 18], [13, 18], [20, 18], [24, 18], [6, 20], [11, 20], [22, 20], [26, 20], [8, 23], [24, 23]]) p.rect(x, y, x, y + 1, "d");
// アーチ
for (let y = 15; y <= 25; y++) for (let x = 8; x <= 24; x++) if (((x - 16) / 7.5) ** 2 + ((y - 25) / 9) ** 2 <= 1) p.put(x, y, y < 20 ? "e" : y < 23 ? "D" : "W");
p.pts([[13, 24], [14, 24], [19, 23]], "V");
for (let a = 0; a < 11; a++) { const t = Math.PI * (a + 0.3) / 10.6; p.put(16 - Math.cos(t) * 8.8, 25 - Math.sin(t) * 10.2, a < 5 ? "h" : "l"); }
p.pts([[16, 15], [15, 15], [17, 15]], "h"); p.pts([[5, 18], [26, 17]], "g");
p.outline("o");
// 川
for (let y = 26; y <= 29; y++) for (let x = 0; x < 32; x++) if (p.get(x, y) === "." || p.get(x, y) === "o") p.put(x, y, y === 26 ? "D" : "W");
p.pts([[3, 27], [4, 27], [5, 28], [24, 28], [25, 28], [26, 28], [28, 27], [10, 29], [17, 27]], "V"); p.pts([[4, 27], [25, 29]], "q");
p.rect(0, 30, 31, 30, "S");
export const rows = p.rows();
