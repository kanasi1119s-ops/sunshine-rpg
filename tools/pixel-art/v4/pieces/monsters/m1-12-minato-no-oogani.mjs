import { Cv, R } from "../../lib4.mjs";
// 港の大蟹: 港の岩場にすむ、殻のかたい大きな蟹。大きなはさみを振りかざす。
export const name = "港の大蟹"; export const category = "monster";
export const pal = { ...R("abcde", "#3a0e18", "#ff9a5a", "#c03a2a"), ...R("fgh", "#f0d8b0", "#ffffff"), z: "#1c1018", w: "#ffffff", e: "#160a10", y: "#e8c060" };
const c = new Cv();
c.shadow(16, 30, 13, "z");
for (const s of [0, 1]) { const X = (x) => (s ? 31 - x : x);
  c.line(X(9), 22, X(3), 24, "b"); c.line(X(3), 24, X(2), 29, "b"); c.line(X(10), 24, X(6), 27, "b"); c.line(X(6), 27, X(6), 29, "b"); c.line(X(12), 26, X(10), 29, "b"); c.line(X(9), 21, X(3), 24, "c");
  c.line(X(9), 18, X(7), 12, "c", 2);                                                  // うで
  c.ell(X(6), 9, 4, 4, "abcde"); c.poly([[X(3), 6], [X(1), 1], [X(6), 5]], "abcde"); c.poly([[X(9), 6], [X(11), 1], [X(7), 5]], "abcde");
  c.line(X(6), 8, X(6), 5, "a"); c.px(X(4), 8, "e");
  c.line(X(13), 15, X(13), 12, "f"); c.eye(X(13) - (s ? 1 : 0), 10, "e");  }
c.ell(16, 21, 10, 6, "abcde", { dither: true });
c.line(9, 19, 23, 19, "b"); c.list([[12, 22, "y"], [13, 23, "y"], [19, 21, "y"], [20, 22, "y"], [16, 24, "b"], [11, 17, "d"], [12, 17, "e"]]);
c.px(15, 26, "f"); c.line(14, 25, 18, 25, "e");
export const rows = c.rows();
