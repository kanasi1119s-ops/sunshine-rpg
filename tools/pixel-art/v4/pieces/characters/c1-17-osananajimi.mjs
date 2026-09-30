import { charBase, overrides } from "../../lib4.mjs";
import { hs, st, face, mass, rs, finish } from "../../c1-kit.mjs";
// ミナの幼なじみ（歪みに巻き込まれた少年）。もじゃもじゃの栗色の髪・麦色のシャツと茶色のベスト・右手をこちらへのばして助けを求める。足もとから体がとけて、ずれ、紫のかけらになって消えかかっている。
export const name = "ミナの幼なじみ（歪みの少年）"; export const category = "character";
export const pal = {
  p: "#4a3220", "1": "#6e4a2c", "2": "#966a3c", "3": "#c09050", "4": "#e8c078",
  r: "#4a3820", J: "#7a5a30", j: "#a07c40", k: "#d0a858", K: "#f4d888", C: "#fff4d0", y: "#e0c890", Q: "#6a5a70", P: "#48405a",
  u: "#5a2ea0", U: "#c8a8ff", i: "#5aa0d8", s: "#3a2a44", B: "#f09aa0", n: "#8a3a3a", W: "#f0e8ff",
};
const base = overrides(charBase({ hair: 0 }), [
  // 髪（もじゃもじゃ）
  ...mass(1, rs("11-20", "9-22", "8-23", "8-23", "8-23", "8-23"), "43221", { out: "p", outB: "1", strand: [1, 3] }),
  ...st(0, ["10|pp", "13|p", "17|pp", "21|p"]), ...st(1, ["9|p"]), ...st(1, ["22|p"]),
  ...st(6, ["10|c", "12|c 2", "14|c", "18|c", "21|c"]), ...st(7, ["8|p2", "8|p1", "8|p"]), ...st(7, ["23|p"]),
  // 左腕（下げる）
  ...mass(14, rs("8-9", "7-9", "7-9", "7-9", "7-9", "7-9"), "CyJr", { out: "r" }),
  // 右腕（こちらへのばす）
  ...mass(10, rs("26-28", "25-27", "24-26", "23-25", "22-25", "22-24"), "CyyJ", { out: "r", noTop: false }), ...st(8, ["27|qcc", "27|qcb", "27|qbb"]),
  // シャツとベスト
  ...mass(13, rs("10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "9-22", "9-22"), "KkjJ", { out: "r", strand: [1, 6], folds: [[12, 16, 22]] }),
  ...st(13, ["14|Cc", "14|CCCC", "15|CC"]),
  ...mass(15, rs("10-13", "10-13", "10-13", "10-13", "10-13", "10-13", "10-13"), "JJrr", { out: "r" }), ...mass(15, rs("18-21", "18-21", "18-21", "18-21", "18-21", "18-21", "18-21"), "JJrr", { out: "r" }),
  ...st(20, ["10|rrrrrrrrrrrr"]),
  // ズボン（そで口だけ）
  ...st(22, ["11|QQQP", "11|QQQP", "11|QQQP"]), ...st(22, ["17|QPPP", "17|QPPP", "17|QPPP"]),
  ...face({ eye: "big", brow: "1", mouth: "open", ic: "i" }),
]);
// ゆがみ: 下から行をずらし、細かく欠けさせ、紫のかけらをちらす
const g = base.map((r) => [...r]);
const shift = { 23: 1, 25: -1, 27: 2 };
for (const [ys, d] of Object.entries(shift)) { const y = Number(ys); const row = g[y].slice(); for (let x = 0; x < 32; x++) { const sx = x - d; g[y][x] = sx >= 0 && sx < 32 ? row[sx] : "."; } }
for (let y = 22; y <= 30; y++) for (let x = 0; x < 32; x++) { const t = (y - 21) * 10; const h = (x * 37 + y * 101 + (x ^ y) * 13) % 100; if (g[y][x] !== "." && h < t) g[y][x] = h < t / 3 ? "." : (h % 2 ? "u" : "U"); }
for (const [x, y, c] of [[6, 22, "u"], [7, 24, "U"], [24, 23, "U"], [25, 26, "u"], [9, 28, "U"], [22, 29, "u"], [13, 30, "U"], [5, 26, "u"], [26, 21, "u"], [27, 25, "U"]]) g[y][x] = c;
export const rows = finish(g.map((r) => r.join("")), pal, { target: 36 });
