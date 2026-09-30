import { charBase, overrides, sym, rect, hline, vline, dress } from "../../lib4.mjs";
export const name = "お年寄りの女"; export const category = "character";
// 白髪のおだんご・めがね・むらさきのショール・花かごを持つ。
export const pal = {
  p: "#6a6a7e", "1": "#8a8a9e", "2": "#aeaec2", "3": "#d0d0e0", "4": "#f2f2fa", q: "#7a4444", a: "#c88a76", b: "#eab094", c: "#f8d0b4",
  r: "#2a1a44", J: "#523a86", j: "#7a5cb8", k: "#9c82d8", K: "#c4b2f0", g: "#3a6a4a", G: "#6aa070", P: "#2a3a3a", o: "#8a5a30", O: "#c89a58", y: "#d8c89a",
};
export const rows = overrides(charBase({ hair: 5, sideHair: 10 }), [
  ...hline(14, 17, 0, "p"), ...hline(13, 18, 1, "3"), [12, 1, "p"], [19, 1, "p"], [18, 0, "A"], [19, 0, "A"], [14, 1, "4"], [15, 1, "4"],
  ...dress(22, 28, 7, 8, { edge: "P", l: "G", m: "g", d: "P", hem: "y" }),
  ...dress(13, 18, 8, 7, {}), ...hline(12, 19, 12, "q"),
  ...vline(10, 6, 10, "m"), ...vline(14, 7, 10, "m"), ...vline(17, 7, 10, "m"), ...vline(21, 6, 10, "m"), ...hline(10, 14, 10, "m"), ...hline(17, 21, 10, "m"), ...hline(10, 14, 6, "m"), ...hline(17, 21, 6, "m"), [15, 8, "m"], [16, 8, "m"],
  ...rect(23, 22, 29, 26, "o"), ...hline(23, 29, 22, "O"), ...hline(23, 29, 26, "P"), [25, 21, "o"], [26, 20, "o"], [27, 20, "o"], [28, 21, "o"], [29, 22, "o"],
  [24, 23, "T"], [25, 23, "t"], [26, 23, "T"], [27, 24, "u"], [28, 24, "U"],
]);
