import { Cv, ramp } from "../lib5.mjs";
// 火竜（大型・中ボス級 192×192）: 溶岩をまとった竜。左向きで首をS字にもたげ、左へ炎を吐く。
export const name = "火竜"; export const category = "monster"; export const size = 192;
export const pal = {
  ...ramp("abcde", "#20070b", "#e0642c", "#86261a"), // 体（赤茶→赤橙）
  ...ramp("fgh", "#1c1719", "#4f4347"), // 腹（炭色）
  ...ramp("ijk", "#0a0810", "#5a4f7c"), // 黒曜石の棘
  ...ramp("lmn", "#5a1218", "#ff7a2c", "#b82c1c"), // 翼の膜
  o: "#d83a10", p: "#ff8a1e", q: "#ffd23a", r: "#fff6c0", // 炎・溶岩
  z: "#140508", y: "#3a0c08", // 輪郭
  ...ramp("stu", "#1c1416", "#7a5644"), // 岩
};
const c = new Cv(192); const late = [];
const W = 192;
const OUT = { a: "z", b: "z", c: "a", d: "b", e: "c", f: "z", g: "z", h: "f", i: "z", j: "z", k: "i", l: "y", m: "y", n: "l", s: "z", t: "z", u: "s", o: "y", p: "o", q: "p", r: "q" };

// ---------- 地面（溶岩の岩場） ----------
const ground = c.union(c.poly([[14, 186], [20, 170], [40, 164], [60, 168], [80, 172], [104, 168], [126, 172], [150, 166], [172, 170], [186, 176], [188, 191], [14, 191]]), c.ell(60, 178, 44, 12), c.ell(150, 180, 40, 10));
const rocks = c.union(c.poly([[16, 176], [22, 160], [34, 156], [42, 168]]), c.poly([[150, 170], [158, 158], [170, 156], [180, 166], [186, 176]]), c.poly([[44, 174], [52, 164], [70, 162], [80, 172]]));
c.paint(c.union(ground, rocks), "stu", { round: 8 });
const lavaCrack = (pts) => { for (let i = 0; i + 1 < pts.length; i++) c.strokeIn(ground, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], "p"); };
lavaCrack([[22, 184], [36, 180], [48, 186], [64, 182]]); lavaCrack([[20, 172], [30, 176], [40, 172]]); lavaCrack([[52, 172], [62, 170], [70, 176]]); lavaCrack([[160, 174], [172, 168], [180, 172]]); lavaCrack([[96, 176], [110, 182], [128, 178], [146, 184]]); lavaCrack([[156, 174], [168, 180], [182, 178]]);
c.speckle(c.inter(ground, c.rect(0, 178, 191, 191)), "q", 0.05, 5);
c.speckle(ground, "o", 0.05, 11);

// ---------- 尾（太く長く、先が燃える） ----------
const tail = c.strip([[136, 128, 17], [154, 142, 14], [172, 148, 10], [184, 138, 7], [186, 122, 5], [182, 108, 3]]);
// ---------- 翼（骨組みは黒、膜は赤橙） ----------
const wrist = [122, 50], tips = [[146, 6], [176, 22], [189, 56], [182, 90]], sh0 = [106, 92], bp = [138, 106];
const wingPts = [sh0, wrist];
const seq = [...tips, bp];
for (let i = 0; i < seq.length; i++) { wingPts.push(seq[i]); if (i + 1 < seq.length) { const a = seq[i], b2 = seq[i + 1], mx = (a[0] + b2[0]) / 2, my = (a[1] + b2[1]) / 2; wingPts.push([mx + (wrist[0] - mx) * 0.3, my + (wrist[1] - my) * 0.3]); } }
const mem = c.poly(wingPts);
// 翼の膜は、骨のあいだを少しえぐる
const memCut = c.M();
const memM = c.sub(mem, memCut);
c.paint(memM, "lmn", { round: 16, bias: 0.12, dither: true });
// 骨組み
const bones = c.union(
  c.limb(106, 92, 122, 50, 2.8, 2.4), c.limb(122, 50, 146, 6, 2.4, 1.2), c.limb(122, 50, 176, 22, 2.2, 1.2),
  c.limb(122, 50, 189, 56, 2, 1.2), c.limb(122, 52, 182, 90, 2, 1.2), c.limb(112, 80, 138, 106, 1.6, 1.2), c.limb(112, 80, 160, 86, 1.2, 1));
const bonesM = c.inter(bones, c.grow(mem, 3));
c.paint(bonesM, "ijk", { round: 2, dither: false });
c.edge(c.limb(106, 92, 122, 50, 2.8, 2.4), "k", "upper");
// 翼の爪
c.fill(c.poly([[144, 8], [150, 0], [149, 10]]), "j"); c.fill(c.poly([[174, 24], [181, 20], [178, 28]]), "j");

// ---------- 胴・腰 ----------
const torso = c.union(c.ell(104, 116, 32, 27), c.ell(124, 126, 28, 26), c.limb(84, 104, 110, 120, 20, 24));
const bodyM = torso;
// 後ろ足（太もも→すね→足）
const thigh = c.ell(126, 138, 24, 26);
const shin = c.union(c.limb(122, 150, 118, 168, 12, 8), c.limb(118, 168, 108, 172, 8, 6));
const rfoot = c.union(c.poly([[122, 166], [98, 170], [92, 178], [96, 180], [124, 180]]));
// 前足（肩→ひじ→鉤爪で岩をつかむ）
const foreArm = c.union(c.limb(84, 118, 74, 142, 11, 8), c.limb(74, 142, 66, 160, 8, 6), c.ell(64, 162, 9, 6));

// 尾を先に塗る（胴の下）
c.paint(tail, "abcde", { round: 10 });
// 奥の腕と脚（暗め）
c.paint(c.union(shin, rfoot), "abcde", { round: 6, bias: -0.1 });
c.paint(bodyM, "abcde", { round: 24, bias: -0.06 });
c.paint(thigh, "abcde", { round: 14, bias: 0.05 });
c.edge(thigh, "a"); c.rim(thigh, { a: "c", b: "d", c: "d" });

// 腹（暗い炭色の板：胸から下へ縦に並ぶ）
const belly = c.sub(c.inter(c.strip([[88, 122, 6], [92, 134, 8], [102, 146, 9], [116, 154, 8], [130, 158, 6]]), bodyM), c.shrink(thigh, 3));
c.paint(belly, "fgh", { round: 5, dither: false });
for (let y = 122; y < 160; y += 4) for (let x = 80; x < 140; x++) if (belly[y * W + x]) c.put(x, y, "f");
c.edge(belly, "b", "upper");

// ---------- 首（大きくS字） ----------
const neck = c.strip([[78, 70, 11], [88, 70, 12], [94, 78, 13], [90, 90, 15], [82, 102, 18], [86, 114, 20]]);
c.paint(neck, "abcde", { round: 12 });
// 首の腹側の板
const neckBelly = c.inter(c.strip([[74, 78, 5], [86, 78, 6], [90, 86, 7], [84, 96, 8], [82, 108, 9]]), neck);
c.paint(neckBelly, "fgh", { round: 3, dither: false });
for (const [x0, y0, x1, y1] of [[78, 74, 80, 82], [84, 74, 86, 82], [90, 80, 92, 88], [86, 88, 90, 92], [84, 96, 88, 100], [82, 104, 86, 108]]) c.strokeIn(neckBelly, x0, y0, x1, y1, "f");

// ---------- 頭 ----------
const HX = 22; const h = new Cv(192);
const skull = h.union(h.ell(48, 56, 20, 16), h.ell(60, 60, 14, 14));
const snout = h.poly([[22, 54], [44, 42], [58, 46], [58, 66], [40, 70], [24, 64]]);
const headM = h.union(skull, snout);
const jaw = h.poly([[24, 64], [40, 68], [58, 68], [64, 78], [50, 82], [34, 76], [24, 70]]);
// 下あご（大きく開く）
h.paint(jaw, "abcde", { round: 6, bias: -0.12 });
h.paint(headM, "abcde", { round: 14, bias: 0.05 });
// 口の中（炎の光）
const mouth = h.poly([[24, 64], [38, 63], [56, 66], [50, 72], [36, 72], [26, 68]]);
h.fill(mouth, "y"); h.fill(h.shrink(mouth, 1), "o"); h.fill(h.shrink(mouth, 2), "p");
// 牙（上の牙と下の牙）
for (const [x, y, len] of [[27, 62, 5], [32, 62, 6], [38, 62, 5], [44, 64, 4]]) h.fill(h.poly([[x, y], [x + 4, y], [x + 2, y + len]]), "r");
for (const [x, y] of [[28, 70], [34, 71], [41, 71]]) h.fill(h.poly([[x, y], [x + 3, y], [x + 1.5, y - 5]]), "r");
h.edge(snout, "b", "upper");
// 鼻のあな
h.put(24, 55, "z"); h.put(25, 55, "z"); h.put(25, 56, "y");
// うろこの筋（頭）
h.strokeIn(headM, 30, 50, 44, 46, "b"); h.strokeIn(headM, 48, 60, 58, 56, "b"); h.strokeIn(headM, 42, 66, 54, 64, "a");
// 眉の張り出し
const brow = h.poly([[32, 46], [50, 40], [58, 44], [54, 50], [40, 52], [32, 50]]);
h.paint(brow, "abcde", { round: 3, bias: -0.15, dither: false });
h.edge(brow, "a", "lower");
// 目（黄色く光る・縦長の瞳）
const eye = h.ell(44, 53, 6, 4.2);
h.fill(h.grow(eye, 1), "y"); h.fill(eye, "q"); h.fill(h.shrink(eye, 1), "r");
h.fill(h.rect(44, 50, 45, 56), "z"); h.put(44, 49, "y"); h.put(45, 57, "y");
h.put(41, 52, "r");
// 角（後ろにそる、2本）
const horn1 = h.strip([[56, 46, 5], [66, 34, 4], [78, 28, 3], [88, 30, 1]]);
const horn2 = h.strip([[60, 54, 4], [72, 44, 3.2], [84, 42, 2.4], [92, 46, 1]]);
h.paint(horn2, "ijk", { round: 2, dither: false });
h.paint(horn1, "ijk", { round: 3, dither: false });
h.edge(horn1, "k", "upper");
// 頭の後ろのたてがみ状の棘
for (const [x, y, dx, dy] of [[66, 58, 12, -4], [70, 64, 14, -1]]) h.fill(h.poly([[x, y - 4], [x + dx, y + dy], [x, y + 4]]), "j");

const SC = 1.25, AX = 82, AY = 62;
const srcOf = (x, y) => [Math.floor(60 + (x - AX) / SC + 0.0001), Math.floor(60 + (y - AY) / SC + 0.0001)];
for (let y = 0; y < 192; y++) for (let x = 0; x < 192; x++) { const [sx, sy] = srcOf(x, y); if (sx >= 0 && sy >= 0 && sx < 192 && sy < 192 && h.g[sy][sx] !== ".") c.put(x, y, h.g[sy][sx]); }
const rsM = (m) => { const o = c.M(); for (let y = 0; y < 192; y++) for (let x = 0; x < 192; x++) { const [sx, sy] = srcOf(x, y); if (sx >= 0 && sy >= 0 && sx < 192 && sy < 192 && m[sy * 192 + sx]) o[y * 192 + x] = 1; } return o; };
const headMs = rsM(headM), jawS = rsM(jaw);

// ---------- 前足（手前） ----------
c.paint(foreArm, "abcde", { round: 8 });
c.edge(foreArm, "b", "lower");
// 前足の鉤爪
for (const [x, y] of [[54, 160], [58, 164], [63, 167], [69, 166]]) c.fill(c.poly([[x, y - 3], [x + 4, y - 3], [x - 1, y + 6]]), "r");
// 後ろ足の爪
for (const [x, y] of [[94, 172], [98, 175], [102, 176]]) c.fill(c.poly([[x, y - 3], [x + 4, y - 3], [x - 2, y + 5]]), "r");

// ---------- 背の棘（黒曜石） ----------
const spineTri = (x, y, h, tilt = 6) => c.poly([[x - 4, y], [x + 4, y + 1], [x + tilt, y - h]]);
const spikes = [[92, 96, 14, 5], [104, 92, 16, 6], [116, 92, 15, 6], [128, 100, 15, 7], [140, 108, 14, 7], [152, 120, 13, 6], [164, 130, 11, 6], [176, 130, 9, 5]];
for (const [x, y, h, t] of spikes) { const s = spineTri(x, y, h, t); c.paint(s, "ijk", { round: 3, dither: false }); c.edge(s, "k", "upper"); }
// 肩の棘（大）
for (const [x, y, h, t] of [[84, 98, 14, -4], [76, 92, 12, -2]]) { const s = spineTri(x, y, h, t); c.paint(s, "ijk", { round: 3, dither: false }); }
// 首すじの棘
for (const [x, y, h, t] of [[82, 70, 9, 5], [88, 82, 10, 6], [88, 94, 11, 6]]) { const s = spineTri(x, y, h, t); c.paint(s, "ijk", { round: 2, dither: false }); }
// 前足・後ろ足のひざの棘
c.fill(c.poly([[106, 146], [112, 152], [100, 156]]), "j");
c.fill(c.poly([[64, 134], [70, 138], [58, 146]]), "j");
// 尾の棘
for (const [x, y] of [[150, 128], [166, 136], [178, 128]]) c.fill(c.poly([[x - 3, y + 2], [x + 3, y + 3], [x + 3, y - 7]]), "j");

// ---------- うろこ（体のもよう） ----------
const scaleArea = c.union(bodyM, thigh, tail, foreArm, shin);
const scaleMask = c.sub(scaleArea, belly);
for (let y = 88; y < 176; y += 6) for (let x = 60; x < 186; x += 7) { const xx = x + ((y / 6) & 1) * 3; if (scaleMask[y * W + xx] && scaleMask[(y + 2) * W + xx]) { c.put(xx, y, "b"); c.put(xx + 1, y + 1, "b"); c.put(xx + 2, y, "b"); } }
// うろこの光の縁
c.rim(bodyM, { c: "d", d: "e", b: "c" });

// ---------- 溶岩の筋（体の内側の熱） ----------
const veins = [
  [[96, 100], [102, 108], [98, 116], [106, 124], [104, 134]],
  [[112, 104], [120, 110], [118, 120], [126, 126], [136, 124]],
  [[112, 136], [120, 144], [116, 152], [122, 160]],
  [[140, 116], [150, 122], [158, 136], [170, 144]],
  [[140, 138], [148, 142], [160, 148]],
  [[92, 126], [86, 134]],
  [[74, 148], [70, 156]],
  [[80, 74], [82, 84], [80, 92]],
  [[54, 60], [60, 66]], [[168, 148], [178, 142], [182, 130]],
];
for (const v of veins) for (let i = 0; i + 1 < v.length; i++) { c.strokeIn(scaleArea, v[i][0] - 1, v[i][1], v[i + 1][0] - 1, v[i + 1][1], "o"); c.strokeIn(scaleArea, v[i][0], v[i][1], v[i + 1][0], v[i + 1][1], "p"); if (i % 2 === 0) c.strokeIn(scaleArea, v[i][0] + 1, v[i][1], v[i + 1][0] + 1, v[i + 1][1], "q"); }
// 翼の膜の熱い脈
for (const [x0, y0, x1, y1] of [[132, 96, 152, 34], [140, 96, 176, 50], [150, 98, 180, 68]]) { c.strokeIn(memM, x0, y0, x1, y1, "n"); c.strokeIn(memM, x0 + 1, y0, x1 + 1, y1, "q"); }

// 胴の下側をひとつ暗く
const dk = { e: "d", d: "c", c: "b", b: "a" };
for (let y = 138; y < 176; y++) for (let x = 60; x < 192; x++) if (scaleMask[y * W + x] && (x + y) % 3 !== 0) { const g = c.get(x, y); if (dk[g]) c.put(x, y, dk[g]); }
// ---------- 輪郭 ----------
c.outline("z", OUT);
c.despeckle("rqpoy");

// ---------- 口から左へ長く伸びる炎 ----------
const fl = c.union(
  c.strip([[44, 72, 4], [34, 70, 8], [20, 65, 15], [7, 60, 14], [1, 56, 8]]),
  c.limb(30, 58, 4, 44, 5, 2), c.limb(28, 72, 3, 80, 5, 2), c.limb(18, 62, 0, 64, 6, 1.5),
  c.limb(20, 50, 8, 32, 5, 2.5), c.limb(18, 74, 10, 92, 5, 2.5), c.limb(36, 60, 24, 40, 4, 1.5), c.limb(34, 74, 26, 90, 4, 1.5),
  c.limb(10, 50, 0, 50, 4, 1));
const flF = c.sub(fl, c.union(headMs, jawS));
c.fill(flF, "y"); c.fill(c.shrink(flF, 1), "o"); c.fill(c.shrink(flF, 3), "p"); c.fill(c.shrink(flF, 5), "q"); c.fill(c.shrink(flF, 8), "r");
for (const [x, y, k] of [[6, 26, "q"], [16, 28, "p"], [2, 96, "p"], [10, 102, "q"], [30, 30, "p"], [28, 98, "o"], [40, 100, "p"], [2, 70, "q"], [24, 22, "q"], [44, 30, "p"], [3, 42, "p"], [12, 84, "q"]]) late.push([x, y, k]);

// あごの下の火の粉
for (const [x, y, k] of [[60, 90, "q"], [66, 96, "p"], [54, 100, "p"], [74, 94, "q"], [62, 108, "o"], [70, 114, "p"]]) late.push([x, y, k]);

// ---------- 尾の先の炎 ----------
const tf = c.union(c.strip([[184, 112, 5], [182, 100, 6], [184, 90, 4], [182, 80, 1.5]]), c.limb(180, 100, 174, 88, 3, 1), c.limb(186, 102, 190, 90, 3, 1));
const tfF = c.sub(tf, tail);
c.fill(tfF, "o"); c.fill(c.shrink(tfF, 1), "p"); c.fill(c.shrink(tfF, 3), "q"); c.put(183, 104, "r"); c.put(183, 100, "r");
c.outline("y", { o: "y" });

// ---------- 舞い上がる火の粉 ----------
const sparks = [[60, 20, "q"], [72, 12, "p"], [30, 24, "p"], [90, 10, "q"], [100, 30, "o"], [120, 8, "p"], [56, 96, "p"], [40, 120, "q"], [22, 110, "o"], [14, 128, "p"], [30, 140, "q"], [46, 148, "p"], [92, 150, "o"], [132, 70, "q"], [190, 40, "p"], [186, 14, "q"], [166, 60, "o"], [8, 100, "q"], [66, 6, "o"], [130, 150, "p"], [180, 160, "q"], [78, 150, "p"], [12, 150, "o"]];
for (const [x, y, k] of sparks) c.put(x, y, k);

// ---------- 足元の照り返し（下から橙の光） ----------
const glowBand = c.inter(c.union(shin, rfoot, foreArm, bodyM), c.rect(0, 150, 191, 182));
c.rim(glowBand, {});
for (let y = 150; y < 182; y++) for (let x = 0; x < W; x++) { if (!glowBand[y * W + x]) continue; const below = c.get(x, y + 1); if (below === "." || below === "z" || "stu".includes(below)) { const g = c.get(x, y); if (g === "a" || g === "b" || g === "c") c.put(x, y, "d"); else if (g === "d") c.put(x, y, "e"); } }
// 落ち影
c.shadow(96, 184, 60, 4, "z", true);

for (const [x, y, k] of late) c.put(x, y, k);
export const rows = c.rows();
