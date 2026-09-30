import { Cv, ramp } from "../lib5.mjs";
// 岩殻ゴロ（中型 96×96）: 背中に苔むした岩の殻を背負った、四つ足のずんぐりした獣。斜め前（左向き）から見た姿。
export const name = "岩殻ゴロ"; export const category = "monster"; export const size = 96;
export const pal = {
  ...ramp("abcde", "#3a2a2c", "#d8a878", "#94623e"),   // 獣の皮
  ...ramp("fghijk", "#2a2c3a", "#c4c0b4", "#726c72"),   // 岩
  ...ramp("lmn", "#1e3a24", "#88c458"),                 // 苔
  ...ramp("pqr", "#3a1e7a", "#c8f4ff", "#4aa0d8"),      // 結晶
  s: "#14121c", o: "#0e0c14", t: "#f0e4c0", u: "#a89468", E: "#1a0e10", y: "#ffd23a", w: "#ffffff", z: "#231a30", x: "#4a2a3a",
};
const c = new Cv(96);
const G = c.rect(0, 0, 95, 88); // 地面より上だけ
const rockR = { f: "s", g: "f", h: "g", i: "h", j: "i", k: "j" };
// 落ち影
c.shadow(50, 88, 40, 4.5, "z");
// ---- 奥の脚（右奥・殻の下） ----
const legBR = c.union(c.limb(76, 62, 80, 80, 8, 7), c.ell(80, 82, 8, 4.5));
c.paint(c.sub(legBR, c.rect(0, 89, 95, 95)), "abcde", { round: 6, bias: -0.18 });
const legBR2 = c.union(c.limb(62, 64, 62, 80, 7, 6.5), c.ell(62, 82, 8, 4.5));
c.paint(legBR2, "abcde", { round: 6, bias: -0.1 });
// ---- 胴（殻の下からのぞく） ----
const belly = c.ell(46, 66, 26, 13);
c.paint(belly, "abcde", { round: 11, bias: -0.3 });
// ---- 殻（大きな岩の甲羅） ----
const shellAll = c.sub(c.union(c.ell(56, 36, 34, 27), c.ell(40, 42, 22, 20), c.rect(28, 40, 86, 56)), c.rect(0, 58, 95, 95));
const chips = [c.poly([[12, 26], [22, 20], [12, 34]]), c.poly([[36, 4], [44, 4], [38, 10]]), c.poly([[88, 20], [96, 20], [96, 30], [92, 26]]), c.poly([[92, 52], [96, 52], [96, 58], [90, 58]]), c.poly([[14, 52], [20, 56], [12, 58]])];
const shell = c.sub(shellAll, ...chips);
// 板に分ける（面）
const plates = [
  [[14, 30], [34, 8], [52, 6], [46, 30], [30, 44], [14, 46]],
  [[52, 6], [74, 10], [70, 32], [46, 30]],
  [[74, 10], [92, 26], [92, 46], [74, 46], [70, 32]],
  [[14, 46], [30, 44], [46, 30], [56, 46], [50, 62], [14, 62]],
  [[46, 30], [70, 32], [74, 46], [92, 46], [92, 62], [50, 62], [56, 46]],
];
const bias = [0.12, 0.28, -0.12, 0.02, -0.26];
plates.forEach((pl, i) => {
  const m = c.inter(shell, c.poly(pl));
  c.paint(m, "fghijk", { round: 5, bias: bias[i], dither: true, flat: 0.1 });
  c.edge(m, "f", "lower");
});
// 面のふち（板の上と左は明るい）
plates.forEach((pl) => { const m = c.inter(shell, c.poly(pl)); c.rim(m, { f: "g", g: "h", h: "i", i: "j", j: "k" }); });
// 割れ目
const cr = [[34, 8, 30, 22], [30, 22, 36, 30], [36, 30, 30, 40], [52, 6, 50, 18], [50, 18, 56, 26], [56, 26, 52, 34], [70, 32, 78, 38], [78, 38, 84, 36], [24, 50, 34, 54], [64, 46, 60, 56], [82, 20, 78, 28]];
for (const [a, b, d, e] of cr) c.strokeIn(shell, a, b, d, e, "s");
for (const [a, b, d, e] of [[35, 9, 31, 22], [51, 7, 51, 18], [83, 21, 79, 28]]) c.strokeIn(shell, a + 1, b, d + 1, e, "g");
// 岩の質感（点描）
c.speckle(shell, "g", 0.05, 11); c.speckle(shell, "i", 0.05, 5);
// 光の縁
c.rim(shell, { f: "g", g: "h", h: "j", i: "k", j: "k", k: "k" });
// ---- 苔 ----
const moss = c.union(c.ell(38, 12, 9, 4), c.ell(76, 16, 8, 4), c.ell(22, 34, 5, 5), c.ell(88, 44, 4, 5), c.ell(58, 54, 9, 3), c.ell(60, 8, 6, 2.5));
const mossM = c.inter(moss, shell);
c.paint(mossM, "lmn", { round: 3, dither: true }); c.edge(mossM, "l", "lower");
c.speckle(mossM, "n", 0.1, 4);
for (const [x, y] of [[36, 17], [40, 16], [74, 21], [79, 20], [22, 40], [55, 57], [63, 57], [88, 50]]) if (shell[y * 96 + x]) c.put(x, y, "m");
// ---- 結晶（殻から生える） ----
const cry = (pts, o = {}) => { const m = c.poly(pts); c.paint(m, "pqr", { round: 3, dither: false, bias: 0.22, ...o }); c.edge(m, "q", "lower"); return m; };
cry([[62, 20], [64, 6], [68, 2], [72, 8], [72, 20]]); c.line(65, 17, 67, 6, "r"); c.put(68, 4, "q");
cry([[72, 20], [76, 10], [80, 12], [80, 22]], { bias: -0.1 });
cry([[52, 24], [50, 14], [54, 10], [58, 14], [58, 24]]);
cry([[20, 30], [16, 20], [20, 16], [25, 22], [26, 32]], { bias: 0.05 });
cry([[84, 34], [88, 24], [92, 28], [90, 38]], { bias: -0.15 });
// ---- 頭（小さく、鋭い目、短いきば） ----
const neck = c.limb(24, 64, 34, 62, 9, 10);
const head = c.union(c.ell(20, 66, 13, 10), c.ell(12, 71, 9, 6), neck);
c.paint(head, "abcde", { round: 7, bias: 0.03 });
c.edge(c.ell(20, 66, 13, 10), "b", "lower");
// 額のプレート（岩）
const brow = c.poly([[10, 58], [20, 55], [30, 58], [28, 62], [14, 62]]);
c.paint(c.inter(brow, head), "fghij", { round: 3 }); c.edge(c.inter(brow, head), "f", "lower");
c.rim(c.inter(brow, head), { f: "g", g: "h", h: "i", i: "j" });
// 耳（小さく）
const ear = c.poly([[26, 58], [30, 52], [34, 58]]); c.paint(ear, "abcd", { round: 2, dither: false }); c.edge(ear, "a", "lower");
// 目（つり上がり）
c.fill(c.poly([[13, 65], [19, 64], [20, 67], [13, 67]]), "E");
c.put(17, 65, "y"); c.put(18, 65, "y"); c.put(18, 66, "y"); c.put(19, 66, "y"); c.put(15, 66, "y"); c.put(17, 65, "w");
c.line(12, 64, 20, 62, "a");
c.put(27, 65, "E"); c.put(28, 65, "E"); c.put(27, 66, "y");
// 鼻と口
c.put(6, 70, "a"); c.put(7, 69, "a"); c.put(6, 71, "E");
c.line(6, 74, 16, 75, "a"); c.line(16, 75, 20, 73, "a");
c.fill(c.poly([[8, 74], [10, 74], [9, 79]]), "t"); c.fill(c.poly([[13, 75], [15, 75], [14, 80]]), "t");
c.put(9, 78, "u"); c.put(14, 79, "u");
c.put(11, 77, "s");
// ---- 手前の脚（太く、大きな爪） ----
const legs = [[36, 68, 32, 82, 9, 8.5, 32, 84], [56, 68, 54, 82, 9, 8.5, 54, 84]];
for (const [x0, y0, x1, y1, r0, r1, fx, fy] of legs) {
  const l = c.union(c.limb(x0, y0, x1, y1, r0, r1), c.ell(fx, fy, 10, 5));
  c.paint(c.inter(l, G), "abcde", { round: 7, bias: 0.02 });
  c.edge(c.inter(l, G), "b", "lower");
  // 肩の岩プレート
  const sh = c.ell(x0 + 1, y0 - 2, 8, 5); const shm = c.inter(sh, c.sub(l, c.rect(0, 0, 0, 0)));
  c.paint(shm, "fghij", { round: 3 }); c.edge(shm, "f", "lower"); c.rim(shm, { f: "g", g: "h", h: "i", i: "j" });
  // 爪
  for (let k = -1; k <= 1; k++) { const cx = fx + k * 5 - 1, cy = fy + 4; c.fill(c.poly([[cx - 2, cy - 1], [cx + 2, cy - 1], [cx + (k < 0 ? -1 : k > 0 ? 1 : 0), cy + 5]]), "t"); c.put(cx - 1, cy, "w"); c.put(cx + 1, cy + 2, "u"); }
}
// 皮のしわ・すね毛の筋、足の指の分かれ目
for (const [x, y] of [[30, 72], [36, 76], [52, 72], [58, 76], [70, 70], [76, 74], [80, 70]]) { c.line(x, y, x + 2, y + 3, "b"); }
for (const fx of [32, 54]) { c.line(fx - 4, 80, fx - 4, 83, "a"); c.line(fx + 3, 80, fx + 3, 83, "a"); }
for (const x of [46, 64]) c.line(x, 66, x + 1, 72, "a");
// 奥の脚の爪
for (const fx of [62, 80]) for (let k = -1; k <= 1; k++) { const cx = fx + k * 5 - 1, cy = fy2(fx); c.fill(c.poly([[cx - 2, cy - 2], [cx + 2, cy - 2], [cx, cy + 3]]), "u"); c.put(cx - 1, cy - 1, "t"); }
function fy2() { return 84; }
// 岩の尻尾は省略、殻の下縁の影
for (let x = 14; x < 92; x++) { for (let y = 56; y < 66; y++) if (shell[y * 96 + x] && !shell[(y + 1) * 96 + x]) { c.put(x, y + 1, "s"); if (x % 2) c.put(x, y + 2, "s"); } }
c.outline("o", { a: "o", b: "a", c: "a", d: "b", e: "c", f: "s", g: "f", h: "f", i: "g", j: "h", k: "h", l: "s", m: "l", n: "m", p: "s", q: "p", r: "p", t: "u", u: "o", s: "o", z: "z" });
c.despeckle("wyEtuqr");
export const rows = c.rows();
