import { charBase, overrides, sym, rect, hline, vline, dress, despeckle } from "../../lib4.mjs";
export const name = "赤ん坊を抱く母"; export const category = "character";
// 三つ編みを肩にたらし、毛布にくるんだ赤ん坊を抱く。長い青緑のスカート。
export const pal = {
  p: "#4a2e1a", "1": "#6a4020", "2": "#986030", "3": "#c48a44", "4": "#eab868", q: "#7a4238", a: "#c47a64", b: "#e6a488", c: "#f6ccac",
  r: "#4a1e1a", J: "#8a3a2a", j: "#b85a3a", k: "#d8805a", K: "#f0a880", S: "#2a5a7a", W: "#5a9ab8", P: "#2a3a4a", C: "#f6f0dc", y: "#d0c29a", M: "#ffffff", t: "#e05a70",
};
export const rows = despeckle(overrides(charBase({ hair: 5, sideHair: 7 }), [
  ...dress(22, 28, 7, 8, { edge: "P", l: "W", m: "S", d: "P", hem: "W" }),
  ...[12, 13, 14, 15, 16, 17, 18, 19, 20].flatMap((y) => [[10, y, y % 2 ? "3" : "2"], [11, y, y % 2 ? "2" : "3"]]), [10, 21, "t"], [11, 21, "t"], [9, 12, "p"], [9, 13, "p"],
  ...rect(13, 16, 22, 23, "C"), ...hline(13, 22, 23, "y"), ...vline(22, 17, 22, "y"), ...hline(14, 21, 21, "y"), [13, 16, "y"], [14, 16, "M"], [15, 17, "M"],
  ...rect(17, 13, 21, 17, "c"), ...hline(17, 21, 13, "3"), [18, 14, "3"], [20, 14, "3"], [18, 15, "e"], [20, 15, "e"], [19, 16, "n"], [17, 16, "B"], [21, 16, "B"], ...vline(16, 14, 17, "q"),
  ...rect(10, 20, 13, 21, "j"), ...hline(14, 15, 21, "c"), [23, 20, "c"], [22, 21, "c"],
]), "wBein");
