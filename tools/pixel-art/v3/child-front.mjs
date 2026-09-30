import { overrides } from "./sprite.mjs";
import { rows as yuri } from "./yuri-front.mjs";
// 町の子ども（元気な男の子）。ユーリの骨組みをもとに、短い金茶の髪・大きな目・黄色いシャツ・短いズボン・小さな体にした。目にはハイライトを入れる。
export const pal = { p: "#4a3018", "1": "#7a5028", "2": "#b07c38", "3": "#dca850", "4": "#fce090", J: "#c89a20", j: "#f0c840", k: "#fce070", K: "#fff4b0", r: "#7a5a10", C: "#fff8e0", S: "#e04a3a", W: "#f88070", a: "#c88068", b: "#eaa88c", c: "#f8d0b4", d: "#fff0e0", n: "#b05858", P: "#3a5a8a", Q: "#5a84b8" };
const L = [];
// 大きな目（3×4）
for (const x0 of [9, 20]) { for (let y = 14; y <= 17; y++) for (let dx = 0; dx < 3; dx++) L.push([x0 + dx, y, "e"]); L.push([x0, 14, "w"], [x0, 15, "w"], [x0 + 1, 16, "i"], [x0 + 2, 16, "i"], [x0 + 1, 17, "i"], [x0 + 2, 17, "i"]); }
L.push([14, 19, "n"], [15, 19, "n"], [16, 19, "n"], [17, 19, "n"], [13, 18, "n"], [18, 18, "n"]);   // 元気な口
L.push([12, 17, "W"], [19, 17, "W"], [11, 18, "W"], [20, 18, "W"]);   // 赤いほお
// 短いズボン
for (let y = 28; y <= 29; y++) for (let x = 10; x <= 21; x++) L.push([x, y, y === 28 ? "Q" : "P"]);
// 首かざり（赤いスカーフ）
for (let x = 12; x <= 19; x++) L.push([x, 22, "S"]); L.push([15, 23, "W"], [16, 23, "S"]);
L.push([24, 27, "b"], [25, 27, "b"]);
export const rows = overrides(yuri, L);
