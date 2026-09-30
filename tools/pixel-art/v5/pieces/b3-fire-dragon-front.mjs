import { Cv, ramp } from "../lib5.mjs";
// 火竜（正面）（ボス 256×256）: 正面向きで翼を高く広げた赤い竜。腹と首の下に明るい横板、口の奥に小さな炎、尻尾は右後ろで巻き上がる。足元は溶岩の割れ目がある岩場。
export const name = "火竜（正面）"; export const category = "boss"; export const size = 256;
export const pal = {
  ...ramp("abcde", "#220610", "#ee5a28", "#a81a1c"),
  ...ramp("fghi", "#9a5a22", "#fff0b0", "#e8a040"),
  ...ramp("jklm", "#b8683a", "#ffe8b8", "#eeae68"),
  n: "#0c0810", o: "#4a3c46", q: "#2a1410", r: "#6a3a26", t: "#fff060", u: "#ff9a1c",
  v: "#c8300e", w: "#ff8a1c", x: "#ffe484", y: "#1c141c", z: "#3a2c34", A: "#60484c", O: "#140608",
};
const c = new Cv(256);
const W = 256;
const bez = (a, b, ctl, n = 10) => { const o = []; for (let i = 1; i <= n; i++) { const t = i / n; o.push([(1 - t) ** 2 * a[0] + 2 * (1 - t) * t * ctl[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * ctl[1] + t * t * b[1]]); } return o; };
const claw = (x, y, dx, dy, len, wid, bend = 0) => { const px = -dy, py = dx; const m = c.poly([[x + px * wid, y + py * wid], [x + dx * len * 0.55 + px * (wid * 0.6 + bend), y + dy * len * 0.55 + py * (wid * 0.6 + bend)], [x + dx * len + px * bend * 1.6, y + dy * len + py * bend * 1.6], [x + dx * len * 0.5 - px * wid * 0.3 + px * bend * 0.4, y + dy * len * 0.5 - py * wid * 0.3 + py * bend * 0.4], [x - px * wid, y - py * wid]]); c.fill(m, "n"); c.rim(m, { n: "o" }); return m; };
const scales = (m, ox = 0, oy = 0, step = 6) => { const dk = { e: "c", d: "c", c: "b", b: "a" }; const w0 = []; for (let y = 4; y < 252; y += step) for (let x = ((y / step) & 1) * (step / 2) + ox; x < 252; x += step) { const X = x, Y = y + oy; if (!m[Y * W + X] || !m[(Y + 3) * W + X + 3] || !m[(Y - 1) * W + X - 2]) continue; const g = c.get(X, Y); if (dk[g]) w0.push([X, Y, g]); } for (const [X, Y, g] of w0) { const d = dk[g]; c.put(X - 1, Y + 1, d); c.put(X, Y + 2, d); c.put(X + 1, Y + 2, d); c.put(X + 2, Y + 1, d); if (g === "c" || g === "d") c.put(X, Y, "e"); } };

// ---- 岩場 ----
const rock = c.poly([[0, 243], [10, 232], [26, 236], [38, 228], [56, 234], [76, 226], [100, 232], [128, 228], [158, 233], [180, 226], [202, 234], [224, 228], [240, 235], [256, 240], [256, 256], [0, 256]]);
c.paint(rock, "yzA", { round: 14, dither: true, flat: 0.1, bias: 0.05 });
// 大きな岩の面（割れ目で区切られた岩）
const slabs = [[[0, 244], [14, 238], [44, 240], [52, 256], [0, 256]], [[58, 256], [66, 240], [104, 238], [118, 256]], [[124, 256], [128, 242], [168, 240], [184, 256]], [[190, 256], [200, 241], [236, 240], [256, 246], [256, 256]]];
for (const pts of slabs) { const m = c.inter(c.poly(pts), rock); c.paint(m, "yzA", { round: 6, bias: 0.04 }); c.rim(m, { y: "z", z: "A" }); c.edge(m, "y", "lower"); }
const cr = rng0(7);
function rng0(sd) { let s = sd; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
const crack = (x, y, dx, n) => { let X = x, Y = y; for (let i = 0; i < n; i++) { const nx = X + dx * (3 + cr() * 4), ny = Y + (cr() - 0.5) * 5; const a = c.inter(c.limb(X, Y, nx, ny, 2.2, 2.2), rock); c.fill(a, "v"); c.fill(c.inter(c.limb(X, Y, nx, ny, 1.1, 1.1), rock), "w"); X = nx; Y = ny; } };
crack(2, 246, 1, 14); crack(54, 254, 1, 10); crack(120, 256, -1, 9); crack(130, 240, 1, 14); crack(222, 240, 1, 9); crack(186, 256, 1, 9); crack(30, 252, 1, 7); crack(100, 244, 1, 6);
for (const [x, y, rx, ry] of [[60, 247, 7, 2.5], [176, 249, 8, 3], [108, 251, 6, 2.5], [236, 247, 6, 2.5]]) { const g = c.inter(c.ell(x, y, rx, ry), rock); c.fill(g, "v"); c.fill(c.inter(c.ell(x, y, rx - 2, ry - 1), rock), "w"); }
for (const [x, y] of [[30, 242], [100, 240], [176, 244], [240, 248], [60, 252]]) { c.put(x, y, "x"); c.put(x + 1, y, "x"); }
for (const [pts, ] of [[[[0, 240], [4, 218], [16, 212], [30, 222], [40, 232], [40, 244], [0, 250]]], [[[216, 236], [226, 224], [238, 214], [250, 216], [256, 226], [256, 246], [216, 246]]]]) { const m = c.poly(pts); c.paint(m, "yzA", { round: 9, bias: 0.04, flat: 0.1 }); c.rim(m, { y: "z", z: "A" }); c.edge(m, "y", "lower"); c.strokeIn(m, pts[1][0] + 6, pts[1][1] + 6, pts[1][0] + 12, pts[1][1] + 18, "y"); }
// ---- 翼（左=-1, 右=+1 少し違う形） ----
function wing(sg, P) {
  const f = (p) => [sg < 0 ? p[0] : 255 - p[0], p[1]];
  const [S, E, Wr, T1, T2, T3, T4, th] = P.map(f);
  const tips = [T1, T2, T3, T4];
  const poly = [Wr, T1];
  const dips = [];
  for (let i = 0; i < 3; i++) { const a = tips[i], b = tips[i + 1], mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]; const ctl = [mid[0], mid[1] + 2]; const pts = bez(a, b, ctl, 16).map((q, k, ar) => { const t = (k + 1) / ar.length; return [q[0], q[1] + 4 * Math.sin(t * Math.PI * 3) * (t * (1 - t) * 4)]; }); dips.push(pts[8]); poly.push(...pts); }
  poly.push(f([108, 132]), S, E);
  const mem = c.poly(poly);
  c.paint(mem, "jklm", { round: 18, flat: 0.35, bias: 0.12, light: [-0.3, -0.85] });
  // 膜のひだ（骨の間に筋）
  for (let i = 0; i < 3; i++) { const a = dips[i]; const s = [Wr[0] + (S[0] - Wr[0]) * (0.35 + i * 0.12), Wr[1] + (S[1] - Wr[1]) * (0.35 + i * 0.12) + 14 + i * 6]; c.strokeIn(mem, s[0], s[1], a[0], a[1], "k"); c.strokeIn(mem, s[0] + 1, s[1], a[0] + 1, a[1], "j"); }
  c.edge(mem, "j", "lower");
  // 骨
  const bones = [];
  const bn = (pts) => { const m = c.strip(pts); bones.push(m); c.paint(m, "abcde", { round: 3, flat: 0.1 }); c.edge(m, "a", "lower"); return m; };
  const bendTo = (A, B, k) => { const mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2, dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy); return [mx - (dy / L) * k, my + (dx / L) * k]; };
  for (let i = 0; i < 4; i++) { const T = tips[i], mid = bendTo(Wr, T, (sg < 0 ? 1 : -1) * (i === 0 ? -7 : 6 - i)); bn([[Wr[0], Wr[1], 3.6 - i * 0.2], [mid[0], mid[1], 2.4], [T[0], T[1], 1.1]]); }
  bn([[S[0], S[1], 7], [E[0], E[1], 5], [Wr[0], Wr[1], 4.2]]);
  // 関節のこぶ
  c.paint(c.ell(Wr[0], Wr[1], 6, 6), "abcde", { round: 4 }); c.edge(c.ell(Wr[0], Wr[1], 6, 6), "a", "lower");
  // 鉤爪: 手首の親指、先端
  claw(Wr[0], Wr[1] - 3, (th[0] - Wr[0]) / Math.hypot(th[0] - Wr[0], th[1] - Wr[1]), (th[1] - Wr[1]) / Math.hypot(th[0] - Wr[0], th[1] - Wr[1]), 24, 4.2, sg * 4);
  claw(T1[0], T1[1] - 2, sg * -0.25, 1, 11, 2.2, sg * 2);
  for (const T of [T2, T3, T4]) claw(T[0], T[1] - 1, 0, 1, 7, 1.7, sg * 1);
}
wing(-1, [[100, 118], [76, 66], [34, 42], [3, 110], [26, 168], [62, 184], [96, 160], [24, 18]]);
wing(+1, [[100, 118], [72, 72], [40, 48], [8, 118], [32, 162], [64, 176], [94, 152], [32, 20]]);

// ---- 尻尾（体の右後ろへ長く巻き上がる） ----
const tailPts = [[148, 196, 11], [176, 216, 10], [208, 220, 8], [235, 202, 7.5], [245, 172, 6], [241, 146, 4], [231, 126, 1.8]];
const tail = c.strip(tailPts);
c.paint(tail, "abcde", { round: 6 });
scales(tail, 0, 0, 5);
c.rim(tail, { b: "c", c: "d", d: "e" });
// 背びれ（尻尾の外側）
for (const [i, L] of [[1, 11], [2, 11], [3, 11], [4, 10], [5, 8]]) { const p = tailPts[i], q = tailPts[i + 1]; const dx = q[0] - p[0], dy = q[1] - p[1], ln = Math.hypot(dx, dy); const fl = i >= 3 ? -1 : 1; const nx = fl * dy / ln, ny = -fl * dx / ln; const sx = p[0] + nx * p[2] * 0.7 - dx / ln * 3, sy = p[1] + ny * p[2] * 0.7 - dy / ln * 3; const sp = c.poly([[sx, sy], [sx + nx * L - dx / ln * 2, sy + ny * L - dy / ln * 2], [sx + dx / ln * 8, sy + dy / ln * 8]]); c.fill(sp, "r"); c.rim(sp, { r: "u" }); c.edge(sp, "q", "lower"); }
// 尻尾の先の炎
const flame = (cx, cy, h, w) => { const m = c.poly([[cx - w, cy], [cx - w * 0.6, cy - h * 0.45], [cx - w * 0.15, cy - h * 0.6], [cx - w * 0.25, cy - h], [cx + w * 0.35, cy - h * 0.6], [cx + w * 0.7, cy - h * 0.4], [cx + w, cy]]); c.fill(m, "v"); const m2 = c.poly([[cx - w * 0.6, cy], [cx - w * 0.3, cy - h * 0.4], [cx, cy - h * 0.7], [cx + w * 0.3, cy - h * 0.4], [cx + w * 0.6, cy]]); c.fill(m2, "w"); c.fill(c.poly([[cx - w * 0.3, cy], [cx, cy - h * 0.4], [cx + w * 0.3, cy]]), "x"); };
flame(231, 126, 26, 7); c.put(226, 98, "w"); c.put(238, 108, "x");

// ---- 後ろ足（太ももと足） ----
function hind(sg) {
  const X = (x) => (sg < 0 ? x : 255 - x);
  const th = c.union(c.ell(X(84), 186, 24, 28), c.limb(X(82), 200, X(76), 226, 14, 9));
  c.paint(th, "abcde", { round: 12, bias: -0.06 }); scales(th, 1, 0, 6); c.rim(th, { c: "d", d: "e", b: "c" }); c.edge(th, "a", "lower");
  const ft = c.union(c.ell(X(72), 228, 18, 7));
  c.paint(ft, "abcde", { round: 5, bias: -0.1 }); c.edge(ft, "a", "lower");
  for (const dx of [-14, -5, 4, 13]) { const t = c.ell(X(72 + dx), 229, 4, 3.6); c.paint(t, "abcde", { round: 3, bias: -0.1 }); c.edge(t, "a", "lower"); }
  for (const [dx, bx] of [[-14, -0.3], [-5, -0.1], [4, 0.1], [13, 0.3]]) claw(X(72 + dx), 230, (sg < 0 ? 1 : -1) * bx, 1, 13, 3.3, sg * bx * 4);
}
hind(-1); hind(+1);

// ---- 胴 ----
const torso = c.union(c.ell(128, 152, 38, 46), c.ell(128, 122, 34, 22));
c.paint(torso, "abcde", { round: 26, bias: -0.1 }); scales(torso, 0, 0, 6); c.rim(torso, { b: "c", c: "d", d: "e" });
// 首（太く、頭へ）
const neck = c.strip([[128, 122, 19], [128, 100, 15], [128, 84, 14]]);
c.paint(neck, "abcde", { round: 10 }); c.rim(neck, { c: "d", d: "e" });
// 胸〜腹の横板（首の下から腹まで、少し湾曲）
const plates = []; let py = 90;
for (let i = 0; py < 198; i++) { const t = (py - 90) / 108; const hw = 9 + Math.sin(Math.min(1, t * 1.3) * Math.PI * 0.68) * 17 + (t > 0.8 ? -(t - 0.8) * 55 : 0); const hh = 4 + Math.round(t * 6); plates.push([py, hh, hw]); py += hh + 2; }
for (const [y0, h, hw] of plates) {
  const band = c.poly([[128 - hw, y0 - 2], [128 - hw * 0.5, y0 - 3.4], [128, y0 - 3.8], [128 + hw * 0.5, y0 - 3.4], [128 + hw, y0 - 2], [128 + hw - 1, y0 + h - 1], [128 + hw * 0.5, y0 + h + 1.2], [128, y0 + h + 1.8], [128 - hw * 0.5, y0 + h + 1.2], [128 - hw + 1, y0 + h - 1]]);
  c.paint(band, "fghi", { round: 4, bias: 0.0, light: [-0.3, -0.9], dither: false });
  c.rim(band, { g: "h", h: "i" }); c.edge(band, "f", "lower"); c.edge(band, "f", "upper");
}
// ---- 前足（太く、少し外へ） ----
function fore(sg) {
  const X = (x) => (sg < 0 ? x : 255 - x);
  const sh = c.ell(X(101), 136, 16, 16);
  const arm = c.union(c.limb(X(99), 140, X(82), 172, 14, 11), c.limb(X(82), 172, X(90), 206, 11, 9));
  const all = c.union(sh, arm);
  c.paint(all, "abcde", { round: 9, bias: -0.14 }); scales(all, 2, 0, 6); c.rim(all, { c: "d", d: "e", b: "c" }); c.edge(all, "a", "all");
  
  // ひじのとげ
  c.fill(c.poly([[X(70), 166], [X(60), 162], [X(68), 176]]), "r"); c.edge(c.poly([[X(70), 166], [X(60), 162], [X(68), 176]]), "q", "lower");
  const paw = c.ell(X(91), 212, 15, 7); c.paint(paw, "abcde", { round: 5, bias: -0.1 }); c.edge(paw, "a", "lower");
  for (const dx of [-11, -3.5, 4, 11]) { const t = c.ell(X(91 + dx), 215, 4.2, 4); c.paint(t, "abcde", { round: 3, bias: -0.1 }); c.edge(t, "a", "lower"); }
  for (const [dx, bx] of [[-11, -0.35], [-3.5, -0.1], [4, 0.1], [11, 0.35]]) claw(X(91 + dx), 216, (sg < 0 ? 1 : -1) * bx, 1, 16, 3.6, sg * bx * 4);
}
fore(-1); fore(+1);
// ---- 頭 ----
// ひれ（頬・あご）
for (const sg of [-1, 1]) {
  const X = (x) => (sg < 0 ? x : 255 - x);
  const fin = c.poly([[X(108), 62], [X(92), 54], [X(96), 62], [X(86), 66], [X(98), 70], [X(92), 78], [X(108), 76]]);
  c.paint(fin, "abcde", { round: 3, bias: 0.05 }); c.edge(fin, "a", "lower");
  const fin2 = c.poly([[X(116), 94], [X(104), 98], [X(110), 102], [X(108), 108], [X(118), 102]]);
  c.paint(fin2, "abcde", { round: 2 }); c.edge(fin2, "a", "lower");
  // 角
  const horn = c.strip([[X(112), 46, 5.5], [X(107), 34, 4.6], [X(100), 23, 3.6], [X(94), 12, 2.4], [X(92), 3, 1]]);
  c.paint(horn, "abcde", { round: 4 });
  const hornTip = c.strip([[X(99), 21, 3.4], [X(92), 3, 1]]);
  c.paint(c.inter(horn, c.union(hornTip, c.limb(X(99), 21, X(92), 3, 4, 1))), "qrr", { round: 2, dither: false });
  c.edge(horn, "a", "lower");
  for (const y of [38, 30]) c.strokeIn(horn, X(108), y + 2, X(101), y - 1, "a");
}
const skull = c.union(c.ell(128, 60, 26, 22), c.ell(128, 72, 20, 16));
c.paint(skull, "abcde", { round: 14, bias: 0.04 }); c.rim(skull, { c: "d", d: "e", b: "c" });
// 額のとさか
const crest = c.poly([[122, 44], [128, 28], [134, 44]]); c.paint(crest, "abcde", { round: 3 }); c.edge(crest, "a", "lower"); c.fill(c.poly([[127, 34], [128, 30], [129, 34]]), "r");
// 鼻先（下向きに突き出す）
const snout = c.union(c.ell(128, 80, 16, 12)); c.paint(snout, "abcde", { round: 9, bias: 0.1 }); c.edge(snout, "a", "lower"); c.rim(snout, { c: "d", d: "e" });
c.put(122, 77, "a"); c.put(123, 77, "a"); c.put(133, 77, "a"); c.put(134, 77, "a");
// 口の中（開口）と炎
const mouth = c.poly([[113, 86], [122, 84], [128, 85], [134, 84], [143, 86], [141, 99], [128, 104], [115, 99]]);
c.fill(mouth, "O"); c.fill(c.poly([[117, 98], [120, 90], [123, 94], [126, 86], [128, 92], [131, 86], [134, 94], [137, 90], [140, 98], [128, 103]]), "v"); c.fill(c.poly([[122, 99], [124, 93], [126, 96], [128, 89], [130, 96], [132, 93], [134, 99], [128, 102]]), "w"); c.fill(c.poly([[126, 100], [128, 94], [130, 100], [128, 102]]), "x");
// 下あご
const jaw = c.poly([[112, 94], [116, 103], [128, 106], [140, 103], [144, 94], [141, 110], [128, 114], [115, 110]]);
c.paint(jaw, "abcde", { round: 4, bias: -0.08 }); c.edge(jaw, "a", "lower");
// 牙
for (const x of [116, 121, 135, 140]) c.fill(c.poly([[x - 1.6, 86], [x + 1.6, 86], [x, 92 + (x % 2)]]), "i");
for (const x of [118, 138]) c.fill(c.poly([[x - 1.4, 104], [x + 1.4, 104], [x, 98]]), "h");
// 目（鋭く吊り上がる）
for (const sg of [-1, 1]) {
  const X = (x) => (sg < 0 ? x : 255 - x);
  c.fill(c.poly([[X(108), 54], [X(118), 58], [X(122), 62], [X(113), 63], [X(108), 59]]), "O");
  c.fill(c.poly([[X(110), 57], [X(118), 60], [X(119), 62], [X(113), 62]]), "u");
  c.fill(c.poly([[X(113), 59], [X(117), 61], [X(116), 62], [X(113), 61]]), "t");
  c.fill(c.poly([[X(106), 51], [X(120), 56], [X(120), 54], [X(108), 48]]), "a"); // 眉
}
// ---- 輪郭 ----
const om = { a: "O", b: "a", c: "a", d: "b", e: "c", f: "a", g: "a", h: "f", i: "g", j: "f", k: "f", l: "g", m: "g", n: "O", o: "n", q: "O", r: "q", y: "O", z: "y", A: "z", v: "a", w: "v", x: "w" };
c.outline("O", om);
c.despeckle("txuwi");
// ---- 火の粉 ----
for (const [x, y, k] of [[178, 214, "w"], [196, 196, "x"], [150, 222, "w"], [60, 222, "w"], [40, 200, "x"], [110, 214, "u"], [240, 222, "w"], [18, 214, "x"], [202, 238, "x"], [226, 106, "w"], [212, 96, "x"], [66, 210, "w"], [174, 232, "x"], [88, 240, "w"], [232, 122, "x"], [152, 240, "w"], [14, 190, "w"], [250, 196, "x"]]) { c.put(x, y, k); }
export const rows = c.rows();
