import { charBase, overrides, sym, rect, hline, vline, dress, line } from "../../lib4.mjs";
export const name = "薬屋"; export const category = "character";
// 白衣の下は緑の服。丸めがね・七三分けの髪。青いくすり瓶を持ち、肩かけかばんをさげる。
export const pal = {
  p: "#1c2a2a", "1": "#2a3a3e", "2": "#44585a", "3": "#6a8484", "4": "#94aeae", q: "#7a4a3a", a: "#c48870", b: "#e8b090", c: "#f8d4b6",
  r: "#1a3a2a", J: "#2e6a4a", j: "#4a9a68", k: "#78c890", K: "#b8e8b8", M: "#fafaff", m: "#a8a4c0", C: "#e4e0f0", y: "#c8c0d8",
  o: "#8a5a30", O: "#d8a058", P: "#4a4a5a", Q: "#6a6a7a", S: "#3a70d8", W: "#a8d4ff",
};
export const rows = overrides(charBase({ hair: 5, fringe: "side" }), [
  ...vline(10, 7, 10, "m"), ...vline(14, 7, 10, "m"), ...vline(17, 7, 10, "m"), ...vline(21, 7, 10, "m"), ...hline(10, 14, 10, "m"), ...hline(17, 21, 10, "m"), [15, 8, "m"], [16, 8, "m"],
  ...vline(10, 14, 21, "m"), ...rect(11, 14, 12, 21, "M"), ...rect(19, 14, 20, 21, "C"), ...vline(21, 14, 21, "m"), [9, 14, "m"], [9, 15, "m"], [22, 14, "m"], [22, 15, "m"],
  ...vline(7, 14, 19, "m"), ...vline(8, 14, 19, "M"), ...vline(23, 14, 19, "C"), ...vline(24, 14, 19, "m"),
  ...dress(22, 28, 6, 8, { edge: "m", l: "M", m: "M", d: "C", hem: "y" }), ...vline(15, 22, 28, "y"),
  ...line(12, 13, 8, 20, "o"), ...rect(3, 21, 8, 26, "o"), ...hline(3, 8, 21, "O"), ...hline(3, 8, 26, "P"), [5, 23, "A"], [3, 22, "O"],
  ...rect(25, 17, 27, 21, "S"), ...vline(25, 17, 21, "W"), ...rect(26, 14, 26, 16, "W"), [26, 13, "o"], [27, 18, "W"],
]);
