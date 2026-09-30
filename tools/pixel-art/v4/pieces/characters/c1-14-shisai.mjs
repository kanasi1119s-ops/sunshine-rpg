import { charBase, overrides } from "../../lib4.mjs";
import { hs, st, face, mass, rs, finish } from "../../c1-kit.mjs";
// 霧断崖の司祭。とがった白い司祭ぼうし（金のふち）・霧のような淡い青の長い髪・黒に近い紺の長衣の上に白いレースのすそのうわぎ・灯りの模様の細い肩かけ・開いた本を胸の前に持つ。
export const name = "霧断崖の司祭"; export const category = "character";
export const pal = {
  p: "#4a5a72", "1": "#7a8ea8", "2": "#a6bad0", "3": "#cadbea", "4": "#eef6fc",
  r: "#141a2c", J: "#222c46", j: "#34425e", k: "#4c5e80", K: "#7a8eb0", C: "#f6f8fc", y: "#d8e0ea", 
  A: "#e0b048", X: "#fff0b0", T: "#8ad0d8", t: "#3a8a98", o: "#1c5462", W: "#e8ecf4", m: "#9aa8bc", i: "#5a8ab0", s: "#1c2030", g: "#f4ecd0", G: "#c8b890",
};
const raw = overrides(charBase({ hair: 0 }), [
  // 長い髪（うしろ）
  ...mass(7, rs(...Array(16).fill("6-9"), "6-9", "7-9", "7-9", "8-9"), "3221", { out: "p", strand: [1, 5] }), ...mass(7, rs(...Array(16).fill("22-25"), "22-25", "22-24", "22-24", "22-23"), "1111", { out: "p", strand: [1, 5] }),
  // 腕（広めの袖）
  ...mass(14, rs("8-9", "6-9", "6-9", "6-9", "6-9", "6-9", "6-9", "6-9"), "KkjJ", { out: "r", folds: [[7, 17, 20]] }), ...mass(14, rs("22-23", "22-25", "22-25", "22-25", "22-25", "22-25", "22-25", "22-25"), "kjJJ", { out: "r" }),
  ...st(22, ["6|WyWyW"]), ...st(22, ["23|WyWyW"]),
  // 紺の長衣
  ...mass(13, rs("10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "10-21", "9-22", "9-22", "9-22", "9-22", "9-22", "9-22", "9-22", "8-23", "8-23"), "KkjJ", { out: "r", strand: [1, 7], folds: [[13, 16, 28], [18, 16, 28]] }),
  // 白いレースのすそのうわぎ（短め）
  ...mass(17, rs("9-22", "9-22", "9-22", "9-22", "9-22", "9-22"), "WCyy", { out: "y", strand: [1, 6] }),
  ...st(23, ["9|WyWyWyWyWyWyWy"]), ...st(23, ["23|W"]),
  ...st(13, ["14|Cc", "14|CCCC", "15|CC"]), ...st(14, ["17|CC"]),
  // 灯りの模様の肩かけ（縦）
  ...mass(14, rs("14-17", "14-17", "14-17", "14-17"), "Tttо".replace("о", "o"), { out: "o" }),
  ...st(17, ["15|XA", "15|AX"]),
  // 開いた本
  ...st(19, ["11|GggggggggGg".replace(/g/g, "g")]),
  ...st(19, ["11|GgggGgggggG", "11|GgWWGWWWggG", "11|GgggGgggggG", "12|GGGGGGGGGG"]),
  ...st(21, ["9|qc", "9|qb"]), ...st(21, ["22|cq", "22|bq"]),
  // 足もと
  ...st(29, ["9|ssssss", "17|ssssss"]),
  // 司祭ぼうし
  ...mass(0, rs("14-17", "13-18", "12-19", "11-20", "10-21", "9-22"), "WCyy", { out: "y", strand: [1, 4] }),
  ...st(4, ["9|AAAAAAAAAAAAAAAA"]), ...st(1, ["15|AA"]), ...st(2, ["15|XX"]),
  // 髪の前がわ
  ...hs(5, ["9|p3 2 1 2 1 1", "9|p2 1", "8|p2", "8|p2", "8|p1", "8|p1"]),
  ...face({ eye: "narrow", brow: "2", mouth: "small", ic: "i" }),
]);
export const rows = finish(raw, pal);
