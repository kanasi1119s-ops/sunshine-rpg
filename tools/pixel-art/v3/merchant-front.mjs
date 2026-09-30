import { overrides } from "./sprite.mjs";
import { rows as yuri } from "./yuri-front.mjs";
// 旅の行商人（各地の町を回る町の人）。ユーリの骨組みをもとに、大きなターバン・口ひげ・大きな荷袋を背負った姿にした。目にはハイライトを入れる。
export const pal = { p: "#3a1a1a", "1": "#a82a3a", "2": "#d8485a", "3": "#f07888", "4": "#ffb0b8", J: "#2a6a5a", j: "#3a9a80", k: "#68c8a8", K: "#a8ecd0", r: "#0e2e28", C: "#f8f0dc", y: "#c8b890", S: "#e0a820", W: "#ffe070", a: "#a8683c", b: "#d09060", c: "#e8b080", d: "#f8d0a8", n: "#7a4028", q: "#2a1810", B: "#7a5030", G: "#a87840" };
const L = [];
// ターバン: 頭全体を布で巻く（y0〜11）
for (let y = 0; y <= 11; y++) for (let x = 7; x <= 24; x++) { const dx = (x - 15.5) / 9, dy = (y - 7) / 6.5; if (dx * dx + dy * dy < 1) L.push([x, y, (x + y) % 5 === 0 ? "1" : y < 4 ? "3" : y < 8 ? "2" : "1"]); }
L.push([15, 6, "S"], [16, 6, "S"], [15, 7, "W"], [16, 7, "S"]);   // 宝石の飾り
for (let x = 8; x <= 23; x++) L.push([x, 11, "1"], [x, 12, "1"]);
for (const x0 of [9, 20]) { L.push([x0, 14, "e"], [x0 + 1, 14, "e"], [x0 + 2, 14, "e"], [x0, 15, "w"], [x0 + 1, 15, "i"], [x0 + 2, 15, "e"], [x0, 16, "c"], [x0 + 1, 16, "c"], [x0 + 2, 16, "c"]); }
// 口ひげ
for (let x = 11; x <= 20; x++) L.push([x, 17, "q"]); for (const x of [10, 11, 20, 21]) L.push([x, 18, "q"]); L.push([15, 19, "n"], [16, 19, "n"]);
// 荷袋（背中から左右にはみ出す大きな袋）
for (let y = 20; y <= 30; y++) for (const [x0, dir] of [[3, 1], [28, -1]]) { const w = y < 22 ? 2 : 4; for (let i = 0; i < w; i++) L.push([x0 - dir * i * -1 * -1 + (dir > 0 ? i : -i) - (dir > 0 ? 0 : 0), y, i === 0 ? "B" : "G"]); }
for (const [x, y] of [[4, 21], [27, 21]]) L.push([x, y, "S"]);
L.push([24, 27, "b"], [25, 27, "b"]);
export const rows = overrides(yuri, L);
