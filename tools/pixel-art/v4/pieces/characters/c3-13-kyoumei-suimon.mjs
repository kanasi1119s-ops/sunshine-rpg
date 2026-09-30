import { charBase, overrides, sym, rect, hline, vline, disc, dress, despeckle } from "../../lib4.mjs";
export const name = "共鳴術士（水紋）"; export const category = "character";
// 波うつ長い水色の髪・ひたいの飾り・ひらひらの長い袖。右手の上に水の玉をうかべる。
export const pal = {
  p: "#0a1e4a", "1": "#16327a", "2": "#2a56b0", "3": "#4a80d8", "4": "#88b8f0", q: "#8a4a48", a: "#d08a78", b: "#f0b498", c: "#fcd8bc", i: "#3ab0c8",
  r: "#2a4a8a", J: "#5a86c8", j: "#98c8ec", k: "#c8ecfa", K: "#f4fcff", S: "#3a8ad8", W: "#a8e8ff", M: "#eef4ff", m: "#a0b4d8",
};
const lock = [];
for (let y = 13; y <= 24; y++) { const s = Math.floor(y / 2) % 2; lock.push([6 + s, y, "p"], [7 + s, y, "2"], [8 + s, y, "3"], [9 + s, y, y % 3 ? "2" : "1"]); }
export const rows = despeckle(overrides(charBase({ hair: 5, sideHair: 12 }), [
  ...sym(lock),
  ...hline(9, 22, 5, "M"), [15, 5, "S"], [16, 5, "S"], [15, 4, "W"],
  ...sym([...rect(5, 18, 7, 22, "j"), ...vline(4, 18, 23, "r"), ...vline(5, 18, 22, "k"), ...hline(5, 7, 23, "W"), [4, 24, "r"], [8, 18, "j"]]),
  ...dress(22, 28, 6, 9, { edge: "r", l: "k", m: "j", d: "J" }),
  ...[9, 13, 17, 21].flatMap((x) => [[x, 28, "W"], [x + 1, 28, "W"], [x + 2, 28, "K"], [x + 3, 28, "K"]]).filter(([x]) => x <= 22), ...hline(11, 12, 25, "W"), ...hline(19, 20, 26, "W"), ...hline(15, 16, 24, "W"),
  [5, 24, "c"], [6, 24, "c"], [25, 24, "c"], [26, 24, "c"],
  ...disc(27, 19, 2.6, "S"), ...disc(27, 19, 1.7, "W"), [26, 18, "w"], [27, 15, "K"], [27, 16, "W"], [28, 22, "S"],
]), "w");
