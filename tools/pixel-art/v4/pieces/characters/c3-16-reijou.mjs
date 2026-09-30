import { charBase, overrides, sym, rect, hline, vline, disc, dress, remap, despeckle } from "../../lib4.mjs";
export const name = "貴族の令嬢"; export const category = "character";
// 金色の縦ロール・小さなかんむり・ふんわり大きく広がるピンクのドレス。右手に扇。
export const pal = {
  p: "#8a5a10", "1": "#b88418", "2": "#e0b030", "3": "#f8d858", "4": "#fff4a0", q: "#8a4a48", a: "#d8988a", b: "#f8c4ac", c: "#fde6d4", d: "#fff6ec", i: "#7a4ad0",
  r: "#5a2a5a", J: "#a04a96", j: "#d878c0", k: "#f4a4dc", K: "#ffd4f0", M: "#fbf8ff", A: "#ffc040", t: "#e03060", T: "#ff88a8", u: "#8a3ab8", U: "#e0b0ff", C: "#f4ecd8",
};
const curl = (y) => [...disc(4.5, y, 2.7, "p"), ...disc(4.5, y, 1.7, "3"), [4, y - 1, "4"], [5, y + 1, "2"]];
export const rows = despeckle(remap(overrides(charBase({ hair: 5, sideHair: 12 }), [
  ...sym([...curl(14), ...curl(18), ...curl(22), [7, 13, "p"], [7, 12, "2"], [8, 11, "p"]]),
  ...hline(11, 20, 4, "A"), [12, 3, "A"], [15, 3, "A"], [16, 3, "A"], [19, 3, "A"], [15, 4, "t"], [16, 4, "t"], [11, 4, "X"],
  ...dress(20, 29, 7, 13, { edge: "r", l: "k", m: "j", d: "J" }),
  ...[3, 7, 11, 15, 19, 23, 27].flatMap((x) => [[x, 29, "M"], [x + 1, 29, "M"], [x + 2, 29, "C"], [x + 3, 29, "C"]]).filter(([x]) => x <= 28),
  ...[7, 12, 20, 25].flatMap((x) => [[x, 25, "K"], [x + 1, 25, "K"]]), ...vline(15, 21, 28, "J"), ...vline(16, 21, 28, "r"),
  [15, 15, "t"], [16, 15, "t"], [14, 16, "T"], [17, 16, "T"], ...hline(11, 20, 19, "K"), ...hline(10, 21, 20, "r"),
  ...rect(7, 20, 8, 21, "M"), ...rect(23, 20, 24, 21, "M"),
  ...disc(27, 14, 3.2, "U"), ...vline(27, 12, 15, "u"), [26, 13, "u"], [28, 13, "u"], [25, 15, "u"], [29, 15, "u"], [25, 19, "A"], [26, 18, "A"], [26, 17, "A"], [27, 17, "A"], [26, 16, "A"],
]), {"X": "A", "B": "T"}), "w");
