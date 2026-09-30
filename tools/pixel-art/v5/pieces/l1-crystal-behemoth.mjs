import { Cv, ramp } from "../lib5.mjs";
// 紫晶の巨獣（大型・中ボス級 160×160）: 肩と背中から紫の水晶が突き出た、青灰色の筋肉質の巨大な獣人。右拳を前に突き出す。
export const name = "紫晶の巨獣"; export const category = "monster"; export const size = 160;
export const pal = {
  ...ramp("abcdef", "#171c2c", "#b4c2da", "#56698f"), // 皮膚（暗→明）
  ...ramp("ghijk", "#2a1248", "#e6c8ff", "#8a46c8"), // 水晶
  l: "#4a2038", m: "#7a3a5c", // 割れた皮膚
  r: "#e02020", y: "#ffe070", // 目
  n: "#5a4a3a", o: "#c8b48a", // 角
  s: "#c8a0a8", // 傷あと
  O: "#0c0e18", P: "#12082a", S: "#0a0c16", w: "#ffffff", t: "#2a2438", u: "#4a4058", // 影・輪郭・腰布
};
const c = new Cv(160);
const SK = "abcdef";
const part = (m, o = {}, edge = "b", ramp_ = SK) => { c.paint(m, ramp_, { dither: false, ...o }); if (edge) c.edge(m, edge, edge === "a" ? "all" : "lower"); return m; };
c.shadow(80, 151, 62, 6, "S");
// ---- 背中の水晶（体の後ろ） ----
const crystal = (bx, by, tx, ty, w, lean = 0, ov = {}) => {
  const dx = tx - bx, dy = ty - by, L = Math.hypot(dx, dy), px = -dy / L * w, py = dx / L * w;
  const A = [bx - px, by - py], B = [bx + px, by + py], T = [tx, ty], M = [bx + dx * 0.0, by];
  const Lm = c.poly([A, T, [bx, by]]), Rm = c.poly([B, T, [bx, by]]);
  const all = c.union(Lm, Rm);
  c.paint(Lm, "ijk", { round: 3, dither: false, ...ov }); c.paint(Rm, "ghi", { round: 3, dither: false, ...ov });
  c.line(Math.round(bx), Math.round(by), tx, ty, "h");
  c.edge(all, "h", "lower");
  c.line(Math.round(bx - px * 0.5 + dx * 0.15), Math.round(by - py * 0.5 + dy * 0.15), Math.round(tx - px * 0.1 - dx * 0.02), Math.round(ty - py * 0.1 - dy * 0.02), "k"); c.put(Math.round(bx - px * 0.4 + dx * 0.4), Math.round(by - py * 0.4 + dy * 0.4), "w");
  return all;
};
const back = [
  crystal(60, 36, 40, -2, 10), crystal(72, 30, 58, -8, 8), crystal(90, 30, 108, -6, 9), crystal(104, 36, 134, 2, 10),
  crystal(46, 42, 12, 10, 10), crystal(112, 40, 150, 26, 8),
];
// ---- 脚 ----
const legL = c.union(c.ell(56, 116, 20, 22), c.limb(54, 128, 51, 143, 15, 13));
const legR = c.union(c.ell(102, 116, 19, 22), c.limb(104, 128, 108, 143, 14, 13));
const footL = c.union(c.ell(50, 146, 17, 6), c.rect(38, 142, 62, 148));
const footR = c.union(c.ell(110, 146, 17, 6), c.rect(98, 142, 122, 148));
part(c.sub(footR, legR), { round: 5 }, "a"); part(legR, { round: 12 }, "a");
part(c.sub(footL, legL), { round: 5 }, "a"); part(legL, { round: 12 }, "a");
// 膝・すね
c.fill(c.ell(58, 128, 8, 5), "c"); c.fill(c.ell(56, 127, 5, 2.5), "d"); c.put(54, 126, "e");
c.fill(c.ell(101, 127, 8, 5), "c"); c.fill(c.ell(99, 126, 5, 2.5), "d");
c.line(57, 136, 55, 141, "b"); c.line(103, 136, 105, 141, "b");
// 爪
for (const x of [38, 42, 46]) c.fill(c.poly([[x, 146], [x + 3, 146], [x + 1, 151]]), "o");
for (const x of [112, 116, 120]) c.fill(c.poly([[x, 146], [x + 3, 146], [x + 2, 151]]), "o");
// ---- 腰布と骨盤 ----
const pelvis = c.union(c.ell(79, 100, 27, 12), c.poly([[54, 98], [104, 98], [100, 120], [79, 126], [58, 120]]));
part(pelvis, { round: 8 }, "b");
const cloth = c.poly([[58, 98], [102, 98], [98, 118], [90, 124], [79, 118], [68, 125], [61, 118]]);
part(cloth, { round: 6 }, "S", "Stu"); c.fill(c.rect(56, 97, 103, 100), "u");
c.line(60, 99, 100, 99, "t");
// ---- 胴体 ----
const torso = c.poly([[44, 44], [116, 42], [112, 70], [104, 88], [98, 100], [60, 100], [54, 88], [46, 68]]);
part(torso, { round: 14 }, "a");
// 大胸筋
const pecL = c.ell(62, 62, 19, 14), pecR = c.ell(98, 61, 19, 14);
part(pecR, { round: 9 }, "a"); part(pecL, { round: 9, bias: 0.05 }, "a");
c.line(79, 50, 79, 75, "a"); c.line(80, 50, 80, 75, "b");
c.line(50, 72, 68, 76, "a"); c.line(92, 76, 110, 72, "a");
// 腹筋（2列×3段）
const abs = [];
for (let r = 0; r < 3; r++) for (const cx of [70, 89]) { const a = c.ell(cx - (cx < 80 ? 0 : 0), 82 + r * 7.5, 8, 4); abs.push(a); part(a, { round: 3.5 }, "a"); }
c.line(79, 76, 79, 98, "a");
// わき腹の割れ目
c.line(52, 84, 58, 96, "b"); c.line(106, 84, 102, 96, "b");
// ---- 首・僧帽筋 ----
const trap = c.poly([[58, 46], [70, 34], [90, 34], [104, 44], [96, 50], [64, 50]]);
part(trap, { round: 6, bias: -0.05 }, "b");
// ---- 頭（小さめ・角ばる） ----
const head = c.poly([[68, 24], [72, 12], [90, 12], [94, 24], [92, 36], [86, 42], [76, 42], [70, 36]]);
part(head, { round: 7, bias: 0.12 }, "a");
// 眉間とほお
c.fill(c.poly([[69, 21], [93, 21], [91, 25], [71, 25]]), "a"); c.fill(c.poly([[72, 28], [79, 28], [79, 33], [73, 33]]), "d"); c.fill(c.poly([[83, 28], [90, 28], [89, 33], [83, 33]]), "c");
c.fill(c.poly([[71, 29], [76, 29], [77, 34], [72, 34]]), "b");
// 目（赤く光る）
c.fill(c.poly([[72, 24], [78, 26], [78, 28], [72, 27]]), "r"); c.fill(c.poly([[90, 24], [84, 26], [84, 28], [90, 27]]), "r");
c.put(76, 26, "y"); c.put(77, 27, "y"); c.put(86, 26, "y"); c.put(85, 27, "y"); c.put(75, 26, "y"); c.put(87, 26, "y");
// 口・きば
c.fill(c.rect(75, 36, 87, 38), "O"); c.fill(c.rect(76, 36, 78, 37), "w"); c.fill(c.rect(84, 36, 86, 37), "w");
c.put(77, 38, "w"); c.put(85, 38, "w");
// 鼻
c.put(80, 31, "a"); c.put(82, 31, "a");
// 角
const hornL = c.poly([[70, 16], [63, 14], [58, 6], [68, 11], [73, 12]]), hornR = c.poly([[91, 12], [96, 8], [104, 4], [98, 15], [93, 19]]);
c.paint(hornL, "no", { round: 2, dither: false }); c.paint(hornR, "no", { round: 2, dither: false });
c.edge(hornL, "b", "lower"); c.edge(hornR, "b", "lower");
// ---- 左腕（体の左＝画面左・下に垂らす）と肩 ----
const shL = c.ell(35, 48, 21, 18);
const armL = c.union(c.limb(34, 56, 26, 88, 14, 12), c.limb(26, 88, 30, 108, 12, 13));
part(armL, { round: 10 }, "a");
c.fill(c.ell(28, 82, 8, 5), "c"); c.line(20, 90, 26, 93, "b");
const fistL = c.ell(30, 118, 15, 14);
part(fistL, { round: 10 }, "a");
for (const y of [111, 117, 123]) c.line(19, y, 41, y + 1, "a"); for (const y of [113, 119]) { c.line(21, y, 26, y, "e"); }
c.line(34, 106, 32, 112, "b");
part(shL, { round: 12 }, "a");
// ---- 右腕（画面右・拳を前へ突き出す。手前に大きく） ----
const shR = c.ell(125, 46, 21, 18);
const armR = c.union(c.limb(122, 54, 130, 72, 15, 16), c.limb(130, 72, 122, 86, 17, 19));
part(armR, { round: 12 }, "a");
c.fill(c.ell(132, 72, 8, 5), "c"); c.fill(c.ell(130, 70, 4, 2), "d");
part(shR, { round: 12 }, "a");
const wrap = c.inter(armR, c.rect(108, 79, 140, 83)); c.fill(wrap, "u"); c.edge(wrap, "t", "lower");
const palm = c.ell(118, 108, 23, 14);
part(palm, { round: 10, bias: -0.05 }, "a");
const fingers = [];
for (let i = 0; i < 4; i++) { const f = c.union(c.ell(100 + i * 11, 96, 6.5, 9), c.rect(94 + i * 11, 96, 106 + i * 11, 104)); fingers.push(f); }
for (let i = 3; i >= 0; i--) { part(fingers[i], { round: 5, bias: 0.05 }, "a"); c.fill(c.ell(98 + i * 11, 91, 2.5, 1.5), "e"); c.put(97 + i * 11, 90, "f"); }
const thumb = c.union(c.ell(101, 112, 10, 7), c.limb(100, 112, 112, 116, 6, 6));
part(thumb, { round: 5, bias: 0.1 }, "a"); c.line(96, 108, 106, 110, "b");
const fistR = c.union(palm, ...fingers, thumb);
// 傷
c.line(120, 104, 128, 110, "s");
// ---- 前の水晶（肩と背中から） ----
const fr = [
  crystal(26, 42, 4, 12, 11), crystal(40, 34, 34, 6, 9), crystal(28, 38, 6, 34, 7), crystal(20, 50, 2, 54, 5),
  crystal(118, 34, 122, 0, 10), crystal(134, 40, 156, 10, 10), crystal(138, 50, 158, 42, 7), crystal(112, 36, 100, 14, 6),
];
// 割れた皮膚（水晶のまわり）
const crackAt = (cx, cy, r) => { r *= 0.7; const m = c.inter(c.ell(cx, cy, r, r * 0.8), c.union(torso, shL, shR, trap)); c.fill(m, "l"); c.speckle(m, "m", 0.12, cx * 3 + cy); c.edge(m, "m"); return m; };
for (const [x, y, r] of [[26, 44, 7], [36, 38, 6], [122, 38, 7], [134, 42, 6], [62, 44, 5], [96, 42, 5]]) crackAt(x, y, r);
for (const [x, y] of [[24, 46], [30, 41], [38, 44], [120, 42], [126, 36], [132, 46]]) c.put(x, y, "m");
// 胸・腹の傷あと
c.line(56, 54, 66, 68, "s"); c.line(58, 54, 68, 68, "b"); for (const [x, y] of [[59, 58], [61, 61], [63, 64]]) c.line(x - 2, y + 1, x + 2, y - 1, "s");
c.line(100, 50, 92, 66, "s"); c.line(84, 90, 92, 98, "s");
// 胸に小さな水晶の破片
crystal(88, 52, 90, 44, 3); crystal(72, 46, 70, 40, 2);
// 光の縁
for (const m of [torso, shL, shR, pecL, pecR, head, fistR, fistL, armL, armR, legL, legR]) c.rim(m, { a: "b", b: "c", c: "d", d: "e", e: "f" });
c.outline("O", { g: "P", h: "P", i: "P", j: "P", k: "P", n: "O", o: "n", u: "O", t: "O" });
c.despeckle("wyrsm");
export const rows = c.rows();
