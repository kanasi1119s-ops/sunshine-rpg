import { painter } from "../../lib4.mjs";
export const name = "浮島の岩";
export const category = "object";
export const pal = { o: "#241c28", g: "#4c8a3c", G: "#84c454", H: "#c0e88c", n: "#2e5a30", d: "#5a4650", e: "#3a2e40", m: "#7e6a70", l: "#a8949a", h: "#d4c4c4", r: "#8a6a3c", w: "#8cd4f0", W: "#e8faff", S: "#2a3a40", t: "#6a4428" };
const p = painter();
// 下の岩（逆さの円すい）
for (let y = 13; y <= 26; y++) { const f = (y - 13) / 13; const hw = 13 * (1 - f ** 1.2) * (1 + 0.15 * Math.sin(y * 2.1)) + 0.5; const x0 = Math.round(16 - hw), x1 = Math.round(16 + hw); for (let x = x0; x <= x1; x++) { const rel = (x - x0) / Math.max(x1 - x0, 1); let c = rel < 0.25 ? "l" : rel < 0.55 ? "m" : rel < 0.85 ? "d" : "e"; if ((x * 3 + y * 5) % 11 === 0 && rel > 0.3) c = "e"; p.put(x, y, c); } }
p.pts([[9, 15], [10, 16], [11, 18], [10, 19], [12, 21], [13, 23], [8, 14]], "h"); p.pts([[21, 16], [20, 19], [19, 22]], "e");
// 垂れ下がる根・しずく
p.pts([[10, 14], [10, 15], [9, 16], [22, 14], [23, 15], [23, 16], [23, 17]], "r"); p.pts([[15, 27], [16, 28], [15, 29]], "w"); p.pts([[15, 27]], "W");
// 上の草地
p.blob(16, 12, 14, 4.2, ["n", "g", "G", "H"]); p.rect(3, 12, 28, 14, "g"); p.rect(3, 14, 28, 14, "n");
for (let x = 3; x <= 28; x++) { const c = p.get(x, 13); if (c === "g" && x < 14) p.put(x, 13, "G"); }
p.blob(16, 11, 12, 3.4, ["g", "G", "H"]);
// 小さな木
p.rect(16, 7, 17, 11, "t"); p.blob(16.5, 5.5, 5, 4, ["n", "g", "G", "H"]);
p.pts([[7, 10], [24, 11], [10, 9]], "H");
// 小さな浮き石
p.blob(5, 22, 2, 1.6, ["e", "m", "l"]); p.blob(27, 20, 2.2, 1.8, ["e", "m", "l"]); p.blob(23, 27, 1.5, 1.2, ["e", "m", "l"]);
p.despeckle();
p.outline("o", true);
p.shadow(21, 30, 6, 1.1, "S");
export const rows = p.rows();
