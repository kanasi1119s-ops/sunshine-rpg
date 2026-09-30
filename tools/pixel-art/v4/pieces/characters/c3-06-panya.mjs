import { charBase, overrides, sym, rect, hline, vline, disc, line } from "../../lib4.mjs";
export const name = "パン屋"; export const category = "character";
// 白い高いぼうし・ちょびひげ・ふくよかな体。右手にフランスパン、左手に丸パン。
export const pal = {
  p: "#4a2a1a", "1": "#5a3420", "2": "#8a5a30", "3": "#b88448", "4": "#dcae68", q: "#8a4238", a: "#d08470", b: "#f2ac90", c: "#fcd4b4", B: "#f47a80",
  r: "#4a2a1a", J: "#8a5a3a", j: "#b08050", k: "#d0a870", K: "#ecd098", P: "#5a4a5a", Q: "#7a6a78",
  M: "#f8f4fc", m: "#bdb4d0", C: "#e6def0", o: "#a8641c", O: "#e8a848",
};
export const rows = overrides(charBase({ hair: 5 }), [
  ...hline(12, 19, 0, "m"), ...rect(9, 1, 22, 3, "M"), ...vline(9, 1, 3, "m"), ...vline(22, 1, 3, "m"), ...rect(20, 1, 21, 3, "C"), ...hline(8, 23, 4, "C"), [8, 4, "m"], [23, 4, "m"], ...hline(9, 22, 4, "m"),
  ...hline(9, 22, 4, "C"), ...hline(8, 23, 5, "m"),
  [12, 1, "M"], [14, 0, "M"],
  ...vline(9, 15, 21, "j"), ...vline(22, 15, 21, "J"), ...rect(10, 16, 21, 21, "M"), ...rect(19, 16, 21, 21, "C"), ...hline(10, 21, 21, "m"), ...rect(13, 17, 18, 18, "C"),
  [13, 10, "1"], [14, 10, "1"], [17, 10, "1"], [18, 10, "1"], [9, 9, "B"], [9, 10, "B"], [22, 9, "B"], [22, 10, "B"],
  ...line(24, 21, 29, 12, "O"), ...line(25, 21, 30, 12, "o"), ...line(26, 21, 30, 13, "o"), [27, 16, "O"], [28, 14, "O"],
  ...disc(5, 21, 2.5, "o"), ...disc(5, 20.5, 1.8, "O"), [4, 19, "K"], [5, 22, "o"],
]);
