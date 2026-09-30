import { charBase, overrides, sym, rect, hline, vline } from "../../lib4.mjs";
export const name = "お年寄りの男"; export const category = "character";
// 白いひげ・はげ頭に白髪の房・つえ。茶色の長いうわぎ。
export const pal = {
  p: "#6a6a7e", "3": "#c8c8dc", "4": "#f2f2fa", q: "#6a3a3a", a: "#b8806c", b: "#dca88a", c: "#efc4a2", d: "#fff0dc",
  r: "#2a1a26", J: "#5a3a3a", j: "#7e5a3c", k: "#a07a4a", K: "#c8a870", C: "#e8dcc0", P: "#3a3a4e", Q: "#585870",
  o: "#7a4a24", O: "#c8903a", B: "#e8907a",
};
export const rows = overrides(charBase({ hair: 0 }), [
  ...sym([[8, 5, "p"], [8, 6, "p"], [8, 7, "p"], [8, 8, "p"], [9, 5, "3"], [9, 6, "3"], [9, 7, "3"], [9, 8, "3"], [10, 6, "4"], [10, 7, "3"], [9, 9, "3"]]),
  ...hline(11, 13, 6, "4"), ...hline(18, 20, 6, "4"),
  ...hline(11, 20, 10, "4"), ...sym([[10, 11, "3"], [11, 11, "4"], [12, 11, "4"]]),
  ...hline(11, 20, 12, "3"), ...hline(12, 19, 13, "4"), ...hline(12, 19, 14, "3"), ...hline(13, 18, 15, "3"), ...hline(14, 17, 16, "p"),
  [15, 11, "n"], [16, 11, "n"],
  ...vline(25, 14, 29, "o"), ...hline(25, 27, 13, "O"), [27, 14, "O"],
  ...rect(13, 17, 14, 18, "y"), ...hline(11, 20, 21, "P"),
]);
