import { overrides } from "./sprite.mjs";
import { rows as yuri } from "./yuri-front.mjs";
// 村長（麦香野の村長。年配で、水争いに頭を悩ませる）。ユーリの骨組みをもとに、白髪・白いひげ・麦わら色の上着にした（町の人）。目にはハイライトを入れる。
export const pal = { p: "#5a5a64", "1": "#8a8a96", "2": "#b8b8c4", "3": "#dcdce6", "4": "#f8f8ff", J: "#7a5a24", j: "#b48c3c", k: "#dcb85c", K: "#f4e090", r: "#3a2a0c", C: "#f4ecd8", S: "#4a7a48", W: "#88b880", a: "#c08a70", b: "#e2a88c", c: "#f2ccb0", d: "#fde8d0", n: "#9a5a5a", P: "#4a4034", Q: "#6a5e4c" };
const L = [];
for (let y = 10; y <= 14; y++) for (const x of [6, 7, 24, 25]) L.push([x, y, "2"]);   // 白髪の横髪
for (const x0 of [9, 20]) { L.push([x0, 13, "3"], [x0 + 1, 13, "3"], [x0 + 2, 13, "3"], [x0, 14, "e"], [x0 + 1, 14, "e"], [x0 + 2, 14, "e"], [x0, 15, "w"], [x0 + 1, 15, "i"], [x0 + 2, 15, "e"], [x0, 16, "c"], [x0 + 1, 16, "c"], [x0 + 2, 16, "c"]); }   // 白い眉と目
// 白いひげ（口・あごを覆う）
for (let y = 17; y <= 23; y++) { const w = y < 19 ? 11 : y < 21 ? 9 : 6 - (y - 21); for (let x = 16 - Math.floor(w / 2); x < 16 + Math.ceil(w / 2); x++) L.push([x, y, (x + y) % 3 === 0 ? "2" : "3"]); }
L.push([15, 18, "n"], [16, 18, "n"]);
L.push([24, 27, "b"], [25, 27, "b"]);
export const rows = overrides(yuri, L);
