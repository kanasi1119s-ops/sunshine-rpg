import { charBase, overrides, sym, rect, hline, vline, dress, remap } from "../../lib4.mjs";
export const name = "図書館員"; export const category = "character";
// まっすぐな前髪のボブ・赤いふちの大きなめがね・青緑のカーディガン。本を高く積んで両手でかかえる。
export const pal = {
  p: "#1e1a2e", "1": "#2e2842", "2": "#463c62", "3": "#66588a", "4": "#8e80b4", q: "#7a4a44", a: "#c48a76", b: "#e8b094", c: "#f8d4b8",
  r: "#1a3a3a", J: "#2e6a66", j: "#4a9a90", k: "#7ac4b4", K: "#b0e8d8", P: "#2a3050", Q: "#44507a", s: "#181420",
  t: "#c02838", T: "#f06a6a", S: "#3a70c0", W: "#a0c8f0", g: "#3a8a4a", G: "#88d078", o: "#8a5a30", O: "#e0b060", M: "#f8f4ec", A: "#ffc040",
};
const book = (y, x0, x1, c, hi) => [...rect(x0, y, x1, y + 1, c), ...hline(x0, x1, y, hi), ...vline(x1, y, y + 1, "s"), [x0 + 1, y + 1, "M"]];
export const rows = remap(overrides(charBase({ hair: 5, sideHair: 12 }), [
  ...hline(9, 22, 5, "2"),
  ...vline(10, 6, 10, "t"), ...vline(14, 7, 10, "t"), ...vline(17, 7, 10, "t"), ...vline(21, 6, 10, "t"), ...hline(10, 14, 10, "t"), ...hline(17, 21, 10, "t"), ...hline(10, 14, 6, "t"), ...hline(17, 21, 6, "t"), [15, 8, "t"], [16, 8, "t"],
  ...dress(22, 28, 7, 7, { edge: "s", l: "Q", m: "P", d: "s" }),
  ...book(15, 11, 20, "t", "T"), ...book(17, 12, 21, "S", "W"), ...book(19, 11, 20, "g", "G"), ...book(21, 12, 20, "o", "O"),
  ...rect(10, 21, 11, 22, "c"), ...rect(21, 21, 22, 22, "b"), [16, 23, "t"], [16, 24, "t"],
]), {"1": "2", "n": "q", "C": "M", "k": "K", "G": "g", "W": "S"});
