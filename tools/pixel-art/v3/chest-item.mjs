// 宝箱（ふたを閉じた正面）。長方形と曲線を1ドットずつ組んだ、オリジナルの絵。
export const pal = { p: "#1c0e08", "1": "#4a2a18", "2": "#6a4024", "3": "#946038", "4": "#c08a50", m: "#7a7a88", M: "#c4c4d4", g: "#d8a020", G: "#f8dc60", s: "#2a1a3a", k: "#3a2a1a" };
const g = Array.from({ length: 32 }, () => Array(32).fill("."));
const put = (x, y, c) => { if (x >= 0 && x < 32 && y >= 0 && y < 32) g[y][x] = c; };
const rect = (x0, y0, x1, y1, c) => { for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) put(x, y, c); };
// 本体（箱）
rect(4, 16, 27, 27, "2"); rect(4, 16, 27, 17, "3"); rect(4, 26, 27, 27, "1"); rect(5, 18, 8, 25, "3"); rect(23, 18, 26, 25, "1");
for (let y = 18; y <= 25; y += 2) for (let x = 9; x <= 22; x++) if ((x + y) % 4 === 0) put(x, y, "1");   // 板の継ぎ目
// ふた（丸み）
for (let y = 8; y <= 15; y++) { const inset = y < 10 ? 4 - (y - 8) * 1.5 | 0 : y < 12 ? 1 : 0; for (let x = 4 + inset; x <= 27 - inset; x++) put(x, y, y < 10 ? "4" : y < 13 ? "3" : "2"); }
rect(6, 8, 25, 8, "4"); for (let x = 5; x <= 26; x++) put(x, 15, "1");
// 金具（帯・角・鍵）
for (const x0 of [6, 23]) { rect(x0, 8, x0 + 2, 27, "m"); rect(x0, 8, x0, 27, "M"); }
rect(13, 14, 18, 20, "g"); rect(13, 14, 18, 14, "G"); rect(15, 16, 16, 18, "k"); put(15, 16, "s");
for (const [x, y] of [[4, 16], [27, 16], [4, 27], [27, 27]]) { put(x, y, "M"); }
// 輪郭
const has = (x, y) => y >= 0 && y < 32 && x >= 0 && x < 32 && g[y][x] !== ".";
const edge = []; for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) if (g[y][x] === "." && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(x + a, y + b))) edge.push([x, y]);
for (const [x, y] of edge) g[y][x] = "p";
for (let x = 3; x <= 28; x++) if (g[29][x] === ".") g[29][x] = "s";
export const rows = g.map((r) => r.join(""));
