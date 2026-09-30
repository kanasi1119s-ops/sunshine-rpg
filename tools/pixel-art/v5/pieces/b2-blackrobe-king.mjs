import { Cv, ramp, rng } from "../lib5.mjs";
// 黒衣の王（裏ボス級 256×256）: 宙に浮かぶ痩せた亡霊の王。足は無く、ちぎれた黒紫のマントが煙のように下へ広がる。
export const name = "黒衣の王"; export const category = "boss"; export const size = 256;
export const pal = {
  ...ramp("abcdef", "#0d0916", "#6a4c9c", "#2e1f52"), // マント（暗→明）
  ...ramp("ghijk", "#3a2208", "#fff0a0", "#d09a2c"), // 金
  ...ramp("lmnL", "#4a4560", "#f6f2e2", "#b4acc0"), // 骨
  ...ramp("pqrs", "#16307c", "#e6fbff", "#4aa8f0"), // 青白い炎
  o: "#06040c", v: "#24130a", w: "#ffffff", t: "#3a2a48", u: "#7a608c", y: "#1b1030",
};
const c = new Cv(256);
const R = rng(11);
const CL = "abcdef";

// ---- 落ち影（宙に浮いているので離して薄く） ----
c.shadow(128, 251, 64, 3.5, "y");

// ---- 杖（マントの奥から）----
const staff = c.limb(207, 40, 200, 232, 2.6, 2.2);

// ---- 後ろの高い襟 ----
const collarL = c.poly([[104, 96], [66, 112], [60, 84], [72, 60], [70, 44], [86, 62], [92, 76], [104, 84]]);
const collarR = c.poly([[152, 96], [190, 112], [196, 84], [184, 60], [186, 44], [170, 62], [164, 76], [152, 84]]);
c.paint(collarL, CL, { round: 7, bias: 0.05 }); c.paint(collarR, CL, { round: 7, bias: -0.08 });

// ---- マント本体（煙のようにちぎれた裾）----
const edgeL = [], edgeR = [];
for (let y = 96; y <= 192; y += 8) { const t = (y - 96) / 96, hw = 30 + 52 * Math.sin(Math.min(1, t * 1.1) * Math.PI / 2) + Math.sin(t * 6) * 3; edgeL.push([128 - hw, y]); edgeR.push([128 + hw, y]); }
const cloakBase = c.poly([...edgeR, ...edgeL.reverse()]);
const tips = [];
for (let i = 0; i < 21; i++) { const t = i / 20, x = 50 + t * 156, sx = Math.abs(t - 0.5) * 2, y0 = 192 - sx * 10, len = 14 + R() * R() * 34 + 10 * (1 - sx) - sx * 4, dx = (R() - 0.5) * 30 + (t < 0.5 ? -1 : 1) * sx * 8; tips.push(c.strip([[x, y0 - 6, 8], [x + dx * 0.4, y0 + len * 0.45, 5.4], [x + dx, y0 + len, 0.8]])); }
const cloak = c.sub(c.union(cloakBase, ...tips), c.rect(0, 250, 255, 255));
c.paint(cloak, CL, { round: 28, bias: 0.04 });
// 千切れて漂うマントの切れ端
const shreds = [[44, 214, 9, 4, -0.5], [212, 208, 10, 4, 0.4], [76, 236, 8, 3, -0.3], [176, 240, 9, 3, 0.3], [124, 250, 7, 3, 0]].map(([x, y, l, w, k]) => c.strip([[x - l, y - 2 * k * l, 0.8], [x, y, w], [x + l, y + 2 * k * l + 3, 0.8]]));
const shredM = c.union(...shreds);
c.paint(shredM, CL, { round: 3, bias: -0.1 });
const wispM = shredM;
const cloakAll = cloak;

// マントの折れ目（左に明るい面、右に暗い影の線）
const foldMask = c.sub(cloak, c.rect(0, 0, 255, 118));
const folds = [[112, 116, 70, 232], [124, 116, 108, 240], [136, 116, 130, 236], [146, 116, 168, 240], [92, 126, 44, 220], [160, 126, 210, 224], [102, 150, 90, 236], [156, 150, 176, 236], [120, 170, 118, 246]];
for (const [x0, y0, x1, y1] of folds) {
  const n = 6;
  for (let i = 0; i < n; i++) {
    const ax = x0 + (x1 - x0) * (i / n), ay = y0 + (y1 - y0) * (i / n) + 0, bx = x0 + (x1 - x0) * ((i + 1) / n), by = y0 + (y1 - y0) * ((i + 1) / n);
    const wob = Math.sin(i * 1.7 + x0) * 2.2;
    c.strokeIn(foldMask, ax + wob, ay, bx + wob, by, "a");
    c.strokeIn(foldMask, ax + wob - 1, ay, bx + wob - 1, by, "e");
    c.strokeIn(foldMask, ax + wob - 2, ay + 1, bx + wob - 2, by + 1, "c");
  }
}
// 裾の破れ目に縁の光
c.rim(cloak, { a: "b", b: "c", c: "d", d: "e" });
// 裾の穴（ぼろの穴）

for (const [x, y, rx, ry] of [[66, 184, 3, 6], [100, 190, 2.5, 8], [156, 186, 3, 7], [188, 180, 2.5, 6], [128, 200, 2, 7]]) c.fill(c.inter(c.ell(x, y, rx, ry), cloak), "a");

// ---- 胴（マントの前の暗い胸元）----
const chest = c.poly([[104, 92], [152, 92], [150, 140], [134, 190], [122, 190], [106, 140]]);
c.paint(chest, "aabbc", { round: 9, bias: -0.1 });
c.edge(chest, "a"); c.line(128, 100, 127, 186, "a"); c.line(129, 100, 128, 186, "c");
// あばら骨のような細い筋（痩せた体）
for (let i = 0; i < 4; i++) { const y = 112 + i * 9; c.line(114, y, 126, y + 3, "c"); c.line(130, y + 3, 142, y, "b"); }

// ---- 首と肩 ----
const shoulderL = c.ell(92, 106, 22, 9), shoulderR = c.ell(164, 106, 22, 9);
c.paint(shoulderL, CL, { round: 8, bias: 0.05 }); c.paint(shoulderR, CL, { round: 8, bias: -0.05 });
c.edge(shoulderL, "b", "upper"); c.edge(shoulderR, "b", "upper");

// ---- 頭（フードの影）----
const hood = c.union(c.ell(128, 62, 24, 28), c.ell(128, 84, 20, 16));
c.paint(hood, "abcbcd", { round: 14, bias: -0.15 });
c.edge(hood, "d", "upper");
// 顔の闇
const void_ = c.ell(128, 70, 15, 19);
c.fill(void_, "o");
c.fill(c.ell(128, 70, 13, 17), "a");
c.fill(c.ell(128, 72, 11, 15), "o");

// 光る目
const eye = (x, y, dir) => {
  c.fill(c.poly([[x - 6, y + 1], [x + 6, y - 1 * dir], [x + 5, y + 3], [x - 4, y + 4]]), "q");
  c.fill(c.poly([[x - 5, y + 1.5], [x + 5, y - 0.5 * dir], [x + 4, y + 2.5], [x - 3, y + 3]]), "r");
  c.fill(c.rect(x - 2, y + 1, x + 1, y + 2), "w");
};
eye(120, 66, -1); eye(137, 66, 1);
for (const [x, y] of [[113, 68], [144, 68]]) c.put(x, y, "q");

// 骨のような顎
const jaw = c.poly([[120, 85], [136, 85], [134, 92], [131, 100], [128, 103], [125, 100], [122, 92]]);
c.paint(jaw, "lmnL", { round: 5, bias: 0.0 });
c.edge(jaw, "l", "lower");
// 歯の線と頬骨
for (const x of [122, 125, 128, 131, 134]) c.line(x, 89, x, 93, "l");
c.line(121, 88, 135, 88, "m");
c.line(112, 80, 118, 84, "n"); c.line(144, 80, 138, 84, "m");
c.put(124, 96, "l"); c.put(132, 96, "l");

// ---- 冠（古い金・折れたとげ）----
const band = c.poly([[104, 46], [152, 46], [154, 56], [152, 58], [104, 58], [102, 56]]);
const spikes = c.union(
  c.poly([[104, 46], [110, 46], [108, 24], [106, 34]]),
  c.poly([[112, 46], [120, 46], [119, 18], [115, 30]]),
  c.poly([[124, 46], [132, 46], [128, 12], [126, 30]]),
  c.poly([[136, 46], [143, 46], [142, 30], [143, 22], [138, 32]]),
  c.poly([[145, 46], [152, 46], [150, 40], [147, 38]])
);
const crown = c.union(band, spikes);
c.paint(crown, "ghijk", { round: 6, bias: 0.05 });
c.edge(band, "h", "lower");
// 帯の飾り（宝石と刻み）
c.fill(c.ell(128, 52, 3, 3), "p"); c.fill(c.ell(127, 51, 1.5, 1.5), "s"); c.put(126, 50, "w");
c.fill(c.ell(113, 52, 1.5, 1.5), "q"); c.fill(c.ell(143, 52, 1.5, 1.5), "q");
for (const x of [107, 120, 135, 148]) c.line(x, 49, x, 55, "h");
c.rim(crown, { g: "h", h: "i", i: "j", j: "k" });
c.line(106, 47, 108, 27, "k"); c.line(114, 47, 116, 24, "k"); c.line(125, 47, 127, 16, "k"); c.line(137, 47, 141, 26, "k");
// 欠けた断面
c.put(143, 22, "h"); c.put(142, 24, "h");
c.put(115, 55, "w"); c.put(106, 50, "w"); c.put(126, 24, "w");
for (const [x, y] of [[104, 57], [107, 57], [148, 57]]) c.put(x, y, "g");

// ---- 高い襟の内側の光の縁 ----
c.rim(collarL, { a: "b", b: "c", c: "d", d: "e" }); c.rim(collarR, { a: "b", b: "c", c: "d" });

for (const [x0, y0, x1, y1] of [[76, 100, 72, 60], [84, 104, 80, 70], [90, 100, 86, 80]]) { c.strokeIn(collarL, x0, y0, x1, y1, "a"); c.strokeIn(collarL, x0 - 1, y0, x1 - 1, y1, "d"); }
for (const [x0, y0, x1, y1] of [[180, 100, 184, 60], [172, 104, 176, 70], [166, 100, 170, 80]]) { c.strokeIn(collarR, x0, y0, x1, y1, "a"); c.strokeIn(collarR, x0 - 1, y0, x1 - 1, y1, "c"); }
// ---- 杖を持つ側の腕（画面右）----
const armR = c.strip([[164, 108, 9], [180, 128, 9], [192, 150, 8]]);
const sleeveR = c.poly([[168, 116], [186, 118], [200, 150], [200, 176], [194, 186], [190, 176], [184, 190], [178, 178], [172, 184], [170, 150]]);
c.paint(c.union(armR, sleeveR), CL, { round: 9, bias: 0.02 });
c.edge(sleeveR, "b", "upper");
c.strokeIn(sleeveR, 178, 122, 190, 176, "a"); c.strokeIn(sleeveR, 177, 122, 189, 176, "d");
c.rim(sleeveR, { a: "b", b: "c", c: "d" });
// 杖（手前）
c.paint(staff, "tu", { round: 2.5, dither: false });
c.line(205, 40, 199, 228, "u");
// 骨の手（杖を握る）
const gripPalm = c.ell(202, 150, 7, 7);
c.paint(gripPalm, "lmnL", { round: 4 });
for (let i = 0; i < 4; i++) { const f = c.limb(195, 143 + i * 4.2, 208, 144 + i * 4.2, 2, 1.8); c.paint(f, "lmnL", { round: 2, flat: 0.4, bias: 0.0 }); c.edge(f, "l", "lower"); c.put(205, 143 + i * 4.2, "n"); }
c.fill(c.ell(196, 150, 2, 7), "m"); c.line(195, 144, 195, 156, "o");
for (let i = 0; i < 5; i++) c.line(196, 141 + i * 4.2, 209, 142 + i * 4.2, "o");
c.limb(208, 141, 214, 150, 1.6, 1.4); c.paint(c.limb(208, 141, 213, 148, 1.8, 1.4), "lmnL", { round: 2, dither: false });
// 杖の飾り環
c.fill(c.rect(201, 120, 209, 123), "i"); c.line(201, 120, 209, 120, "k"); c.line(201, 123, 209, 123, "h");
c.fill(c.rect(197, 190, 205, 193), "i"); c.line(197, 190, 205, 190, "k"); c.line(197, 193, 205, 193, "h");
// 杖頭の爪と宝玉
const claws = c.union(c.strip([[207, 52, 2.4], [198, 46, 2], [193, 34, 1.8], [196, 26, 1]]), c.strip([[207, 52, 2.4], [216, 46, 2], [221, 34, 1.8], [218, 26, 1]]), c.strip([[207, 52, 2.4], [207, 44, 2], [207, 40, 2]]));
c.paint(claws, "ghijk", { round: 2, dither: false });
c.rim(claws, { g: "h", h: "i", i: "j" });
const orb = c.ell(207, 32, 12.5, 12.5);
c.paint(orb, "pqrs", { round: 11, bias: 0.05 });
c.fill(c.ell(207, 33, 7, 7), "r"); c.fill(c.ell(206, 32, 4.5, 4.5), "s"); c.fill(c.ell(205, 31, 2.5, 2.5), "w");
c.fill(c.ell(200, 25, 2, 1.4), "w"); c.put(203, 22, "w");
c.edge(orb, "p", "lower");
c.put(212, 37, "q"); c.put(210, 39, "q");
c.line(213, 30, 214, 34, "r");
// 爪の先が宝玉の前に回る
c.fill(c.ell(198, 40, 2.4, 3), "j"); c.put(197, 38, "k"); c.fill(c.ell(217, 40, 2.4, 3), "i"); c.put(216, 38, "j");

// ---- 前へ広げた手（画面左）----
const armL = c.strip([[94, 110, 10], [76, 130, 10], [62, 152, 8]]);
const sleeveL = c.poly([[92, 112], [70, 118], [50, 146], [46, 176], [56, 184], [66, 176], [76, 182], [84, 160], [90, 140]]);
c.paint(c.union(armL, sleeveL), CL, { round: 10, bias: 0.12 });
c.edge(sleeveL, "c", "upper");
c.rim(sleeveL, { a: "b", b: "c", c: "d", d: "e" });
c.strokeIn(sleeveL, 84, 122, 66, 180, "a"); c.strokeIn(sleeveL, 83, 122, 65, 180, "d");
c.strokeIn(sleeveL, 70, 124, 54, 176, "a"); c.strokeIn(sleeveL, 69, 124, 53, 176, "d");
// 骨ばった前腕（袖口から出る）
const fore = c.limb(62, 172, 52, 156, 3.4, 3);
c.paint(fore, "lmnL", { round: 3, bias: 0.15 }); c.edge(fore, "l", "lower"); c.line(60, 170, 52, 157, "m");
// 手のひらと長い指
const palm = c.poly([[38, 150], [56, 144], [66, 154], [62, 168], [48, 170], [38, 162]]);
c.paint(palm, "lmnL", { round: 7, bias: 0.05 });
c.edge(palm, "l", "lower");
const fingers = [
  [[40, 152], [28, 138], [22, 120], [22, 104]],
  [[47, 148], [40, 128], [37, 108], [38, 92]],
  [[54, 146], [52, 126], [54, 106], [58, 92]],
  [[62, 149], [66, 132], [72, 118], [80, 108]],
  [[64, 158], [76, 152], [86, 148], [94, 148]],
];
const allF = [];
for (const f of fingers) {
  const m = c.strip([[f[0][0], f[0][1], 3.4], [f[1][0], f[1][1], 3], [f[2][0], f[2][1], 2.5], [f[3][0], f[3][1], 1.2]]);
  c.paint(m, "lmnL", { round: 3, flat: 0.2, dither: false, bias: 0.05 }); c.edge(m, "l", "lower"); allF.push(m);
  for (const k of [1, 2]) { c.line(f[k][0] - 3, f[k][1], f[k][0] + 3, f[k][1], "l"); c.put(f[k][0] - 1, f[k][1] - 1, "o"); }
  c.put(f[3][0], f[3][1] - 1, "m");
}
c.rim(c.union(palm, ...allF), { l: "m", m: "n", n: "L" });
c.line(44, 156, 58, 160, "m"); c.line(42, 162, 56, 166, "n");
c.put(48, 152, "o"); c.put(56, 150, "o");

// ---- アウトライン ----
c.outline("o", { a: "o", b: "a", c: "a", d: "b", e: "c", f: "d", g: "v", h: "v", i: "v", j: "h", k: "i", l: "o", m: "l", n: "l", L: "m", p: "p", q: "p", r: "q", s: "q", t: "o", u: "t", w: "o" });

// ---- 魂の火 ----
const flame = (x, y, s) => {
  const body = c.union(c.ell(x, y, 2.2 * s, 2.4 * s), c.poly([[x - 2 * s, y - 0.5 * s], [x + 2 * s, y - 0.5 * s], [x + 0.4 * s, y - 6 * s], [x - 0.4 * s, y - 5 * s]]));
  const tail = c.strip([[x, y + 1 * s, 1.8 * s], [x + 1.5 * s, y + 5 * s, 0.7 * s]]);
  const all = c.union(body, tail);
  const halo = c.grow(all, 1);
  for (let yy = 0; yy < 256; yy++) for (let xx = 0; xx < 256; xx++) if (halo[yy * 256 + xx] && c.g[yy][xx] === "." && ((xx + yy) & 1) === 0) c.g[yy][xx] = "p";
  c.paint(all, "pqrs", { round: 2 * s, dither: false, bias: 0.1 });
  c.put(Math.round(x), Math.round(y), "w"); c.put(Math.round(x), Math.round(y + 1), "s");
};
for (const [x, y, s] of [[207, 15, 1.7], [26, 84, 1.6], [232, 100, 1.5], [40, 220, 1.3], [222, 200, 1.4], [14, 172, 1.1], [246, 156, 1.0], [86, 30, 1.2], [166, 22, 1.0], [56, 60, 1.0], [242, 58, 1.2], [20, 40, 0.9]]) flame(x, y, s);

// 宝玉のにじむ光
for (let yy = 0; yy < 256; yy++) for (let xx = 0; xx < 256; xx++) if (c.g[yy][xx] === ".") { const d = Math.hypot(xx - 207, yy - 32); if (d < 19 && d > 13 && ((xx + yy) & 1) === 0) c.g[yy][xx] = "p"; }

c.despeckle("wpqrs");
export const rows = c.rows();
