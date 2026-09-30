import { charBase, overrides, sym, rect, hline, vline, disc } from "../../lib4.mjs";
export const name = "町の男の子"; export const category = "character";
// 短パン・しましまシャツ・ボールを持つ元気な子。ドットを詰めて背を低くしてある。
export const pal = {
  p: "#4a2812", "1": "#7a4a1a", "2": "#b0742a", "3": "#d8a040", "4": "#f8d068", q: "#8a4a34", a: "#cc8462", b: "#f0aa84", c: "#fcd4b0",
  r: "#6a3010", J: "#c05820", j: "#e88a30", k: "#f8b04a", K: "#ffd98a", P: "#3a4a7a", Q: "#5670a8", t: "#c83a3a", T: "#ff8078",
};
const g = overrides(charBase({ hair: 4, fringe: "spiky" }), [
  [14, 1, "3"], [15, 0, "4"], [16, 1, "3"], [15, 1, "4"], ...sym([[9, 1, "p"], [10, 1, "3"]]),
  ...hline(11, 20, 16, "k"), ...hline(11, 20, 19, "k"),
  ...rect(7, 17, 8, 19, "b"), ...rect(23, 17, 24, 19, "a"), ...vline(7, 17, 19, "q"), ...vline(24, 17, 19, "q"),
  ...rect(11, 25, 14, 27, "c"), ...rect(17, 25, 20, 27, "b"), ...hline(11, 14, 27, "C"), ...hline(17, 20, 27, "C"),
  ...disc(26, 22, 2.5, "t"), [25, 21, "T"], [25, 22, "T"], ...vline(26, 20, 24, "T"),
  [12, 10, "a"], [19, 10, "a"], [19, 11, "a"],
]);
export const rows = [...Array(2).fill(".".repeat(32)), ...g.slice(0, 18), ...g.slice(20)];
