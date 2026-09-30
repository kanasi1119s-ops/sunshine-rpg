import { charBase, overrides, sym, rect } from "../lib4.mjs";
export const name = "ミナ（2.5頭身）"; export const category = "character";
export const pal = { p: "#4a2e1a", "1": "#7a5028", "2": "#b07c3a", "3": "#d8a850", "4": "#f4d888", J: "#2e5a30", j: "#4a8a48", k: "#78b868", K: "#b8e090", r: "#1c3a20", i: "#5aa0d0", B: "#f09aa0" };
export const rows = overrides(charBase({ hair: 5, sideHair: 12, skirt: true }), [
  ...rect(7, 8, 8, 20, "2"), ...rect(23, 8, 24, 20, "2"), ...rect(6, 9, 6, 19, "p"), ...rect(25, 9, 25, 19, "p"),
  [9, 4, "S"], [10, 4, "S"],
]);
