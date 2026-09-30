import { Cv, ramp } from "../lib5.mjs";
// 針翅ムシ（小型 64×64）: 甲虫とスズメバチの中間の、空を飛ぶ虫の魔物。背に針のとげ、ガラスのような翅、光る複眼。
export const name = "針翅ムシ"; export const category = "monster"; export const size = 64;
export const pal = {
  ...ramp("abcde", "#241018", "#f08a34", "#8a3428"), // 甲殻（暗→明）
  ...ramp("fgh", "#4c7cb0", "#e4fbff", "#9cd0e8"), // 翅
  v: "#3c6a8c", V: "#2a4868",
  ...ramp("ijk", "#c02818", "#ffe070"), // 複眼
  w: "#ffffff",
  ...ramp("lmn", "#5a4030", "#f4e8c0"), // とげ
  p: "#3a1a30", q: "#5a2a48", // 足
  o: "#120810", s: "#20303c", t: "#2c2448",
};
const c = new Cv(64);
const CX = 32;
// 落ち影（空中なので離して薄く）
// ---- 翅（左右、奥） ----
const wingL = c.union(c.poly([[22, 26], [12, 12], [3, 9], [1, 16], [4, 26], [12, 34], [21, 36]]), c.poly([[22, 34], [10, 38], [6, 46], [12, 50], [20, 44]]));
const wingR = c.hmirror(wingL);
for (const wm of [wingL, wingR]) {
  c.paint(wm, "fgh", { round: 7, dither: false, bias: 0.05, flat: 0.25 });
}
// 翅脈
const veinL = [[21, 29, 5, 12], [15, 20, 8, 24], [12, 17, 5, 22], [18, 24, 9, 17], [20, 36, 8, 42], [14, 39, 8, 46]];
for (const [x0, y0, x1, y1] of veinL) { c.strokeIn(wingL, x0, y0, x1, y1, "v"); c.strokeIn(wingR, 63 - x0, y0, 63 - x1, y1, "v"); }
c.edge(wingL, "v", "lower"); c.edge(wingR, "v", "lower");
// 翅のきらめき
c.put(6, 13, "w"); c.put(7, 13, "w"); c.put(9, 12, "w"); c.put(57, 13, "w"); c.put(56, 13, "w"); c.put(9, 44, "w");
// ---- 背のとげ（奥） ----
const spines = [
  c.poly([[20, 24], [11, 13], [24, 20]]), c.poly([[24, 20], [19, 5], [28, 17]]),
  c.poly([[28, 17], [27, 2], [33, 15]]),
  c.poly([[33, 15], [37, 1], [38, 17]]),
  c.poly([[37, 18], [46, 6], [41, 21]]),
];
for (const s of spines) { c.paint(s, "lmn", { round: 2, dither: false }); }
// ---- 足（細く曲がる、体の奥・手前） ----
const legs = [
  [[22, 40], [13, 44], [9, 55]], [[22, 44], [15, 51], [16, 58]],
  [[42, 40], [51, 44], [55, 55]], [[42, 44], [49, 51], [48, 58]],
];
for (const l of legs) { const m = c.strip([[l[0][0], l[0][1], 1.6], [l[1][0], l[1][1], 1.1], [l[2][0], l[2][1], 0.7]]); c.paint(m, "pq", { round: 1.2, dither: false }); c.put(l[2][0], l[2][1] + 1, "p"); }
// ---- 胴（丸い甲殻） ----
const body = c.union(c.ell(CX, 32, 14, 14), c.ell(CX, 42, 11, 9));
c.paint(body, "abcde", { round: 12, bias: 0.22, flat: 0.15, light: [-0.35, -0.85] });
// 腹の縞（暗い帯）
for (const y of [33, 37, 41]) { const band = c.inter(body, c.sub(c.ell(CX, y + 6, 15, 10), c.ell(CX, y + 8, 15, 10))); c.fill(band, "c"); c.edge(band, "a", "lower"); }
// 背中の甲羅の割れ目とつや
c.strokeIn(body, 32, 20, 32, 30, "b");
c.rim(body, { c: "d", d: "e", b: "c" });
c.fill(c.ell(25, 24, 3.5, 2.4), "d"); c.fill(c.ell(24, 23, 1.8, 1), "e");
c.put(28, 21, "e");
// ---- 頭 ----
const head = c.union(c.ell(CX, 46, 9, 7));
c.paint(head, "bcde", { round: 6 });
c.edge(head, "a", "lower"); c.rim(head, { c: "d", d: "e" });
// 複眼
for (const ex of [26, 38]) {
  c.fill(c.ell(ex, 45, 4.5, 5), "o");
  c.paint(c.ell(ex, 45, 3.6, 4.2), "ijk", { round: 3, dither: false, bias: 0.1 });
  c.put(ex - 1, 44, "w"); c.put(ex - 1, 43, "k");
}
// 触角
c.line(28, 40, 22, 33, "p"); c.line(22, 33, 19, 32, "p"); c.line(36, 40, 42, 33, "p"); c.line(42, 33, 45, 32, "p");
// 大あご
c.line(29, 51, 27, 55, "n", 1); c.line(27, 55, 30, 55, "n"); c.line(35, 51, 37, 55, "n"); c.line(37, 55, 34, 55, "n");
c.outline("o", { a: "o", b: "a", c: "a", f: "V", g: "v", h: "v", l: "p", m: "p", n: "p", p: "o", q: "p" });
c.despeckle("wkeE");
c.shadow(32, 61, 14, 2, "t");
export const rows = c.rows();
