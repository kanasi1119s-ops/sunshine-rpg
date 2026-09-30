import { Cv, ramp } from "../lib5.mjs";
// 灯守りの竜（章ボス 256×256）: 深い藍色と鈍い金色の竜。胸に古いランタンの灯りが燃え、まわりのうろこを照らす。
export const name = "灯守りの竜"; export const category = "boss"; export const size = 256;
export const pal = {
  ...ramp("abcde", "#050820", "#5a78bc", "#1e2e72"),   // 体（藍）
  ...ramp("fgh", "#0c1236", "#3c4a9c", "#1c2258"),                // 翼の膜
  ...ramp("ijkl", "#3e2e14", "#f2d676", "#b58a34"),    // 鈍い金
  ...ramp("mno", "#3e2436", "#e88c44", "#a04c34"),     // 灯りに照らされた体
  ...ramp("pqrs", "#c23c18", "#fff2b0", "#ffb42c"),    // 炎
  X: "#04061a", z: "#3a0c16", t: "#eadcc0", u: "#080a1e", w: "#ffffff",
};
const c = new Cv(256);
const LX = 128, LY = 150; // 灯りの中心
const mir = (pts) => pts.map(([x, y, r]) => (r === undefined ? [255 - x, y] : [255 - x, y, r]));

// ---------- 翼 ----------
function wing(side) {
  const P = (x, y) => (side < 0 ? [x, y] : [255 - x, y]);
  const memPts = side < 0
    ? [[106, 104], [28, 40], [3, 76], [30, 92], [8, 138], [38, 150], [40, 190], [72, 166], [100, 190], [114, 150]]
    : [[106, 106], [28, 46], [4, 84], [32, 98], [10, 146], [40, 156], [44, 194], [74, 170], [100, 190], [114, 150]];
  const mp = memPts.map(([x, y]) => P(x, y));
  let mem = c.poly(mp);
  const holes = side < 0
    ? [[[18, 100], [32, 108], [22, 122]], [[46, 132], [60, 120], [58, 146]], [[12, 62], [24, 70], [14, 74]]]
    : [[[22, 118], [36, 126], [26, 138]], [[58, 90], [70, 96], [60, 108]], [[44, 160], [56, 152], [56, 172]]];
  for (const h of holes) mem = c.sub(mem, c.poly(h.map(([x, y]) => P(x, y))));
  c.paint(mem, "fgh", { round: 14, bias: -0.08 });
  // 骨組み
  const bx = side < 0
    ? [[104, 106, 8, 68, 62, 6], [68, 62, 6, 28, 40, 4], [28, 40, 4, 4, 76, 2.5], [28, 40, 4, 8, 138, 2.5], [28, 40, 4, 40, 190, 2.5], [104, 106, 6, 100, 190, 2]]
    : [[104, 108, 8, 68, 68, 6], [68, 68, 6, 28, 46, 4], [28, 46, 4, 4, 84, 2.5], [28, 46, 4, 10, 146, 2.5], [28, 46, 4, 44, 194, 2.5], [104, 108, 6, 100, 190, 2]];
  const bones = bx.map(([x0, y0, r0, x1, y1, r1]) => { const [a, b] = P(x0, y0), [d, e] = P(x1, y1); return c.limb(a, b, d, e, r0, r1); });
  const bm = c.union(...bones);
  c.paint(bm, "abcd", { round: 4 });
  c.edge(bm, "a", "lower");
  // 膜の陰（骨の下側）
  // 爪（翼の先）
  const [wx, wy] = P(28, side < 0 ? 40 : 46);
  c.fill(c.poly([[wx - 3, wy - 2], [wx + 3 * -side * -1, wy - 12], [wx + 4, wy]].map(([x, y]) => [x, y])), "k");
  return { mem, bm };
}
const wl = wing(-1), wr = wing(1);
const wingAll = c.union(wl.mem, wl.bm, wr.mem, wr.bm);
// 翼の縁の光（左上）
c.rim(wl.mem, { f: "g", g: "h" }); c.rim(wr.mem, { f: "g", g: "h" });

// ---------- 尾 ----------
const tail = c.strip([[140, 192, 17], [162, 208, 14], [188, 216, 11], [210, 208, 8], [226, 192, 5], [236, 176, 2.5]]);
c.paint(tail, "abcde", { round: 8, bias: -0.14 });
const spade = c.poly([[236, 164], [246, 178], [238, 192], [230, 178]]);
c.paint(spade, "ijkl", { round: 4, dither: false }); c.edge(spade, "i", "lower");
c.edge(tail, "a", "lower");
for (const [x, y, s] of [[156, 196, 6], [176, 202, 6], [196, 200, 5], [214, 190, 4]]) c.fill(c.poly([[x - 3, y + 2], [x + 1, y - s - 2], [x + 4, y + 1]]), "k");

// ---------- 胴 ----------
const torso = c.union(c.ell(128, 148, 35, 47), c.ell(128, 186, 29, 24), c.limb(128, 112, 128, 72, 24, 16));
c.paint(torso, "abcde", { round: 20, bias: -0.05 });
// 肩
const shL = c.poly([[78, 110], [98, 96], [122, 104], [120, 126], [90, 130]]), shR = c.hmirror(shL);
c.paint(shL, "abcde", { round: 8, bias: -0.15 }); c.paint(shR, "abcde", { round: 8, bias: -0.15 }); c.edge(shL, "a", "lower"); c.edge(shR, "a", "lower");
for (const sx of [-1, 1]) { const px = (x) => (sx < 0 ? x : 255 - x); c.fill(c.poly([[px(88), 104], [px(76), 84], [px(102), 98]]), "k"); c.fill(c.poly([[px(76), 84], [px(84), 98], [px(94), 98]]), "l"); c.fill(c.poly([[px(76), 84], [px(80), 92], [px(85), 94]]), "j"); }
// 腹の板（金）
const belly = c.ell(128, 190, 17, 34);
const bellyM = c.inter(belly, c.rect(0, 178, 255, 218));
c.paint(bellyM, "ijkl", { round: 8, dither: false });
for (let y = 182; y < 216; y += 6) c.strokeIn(bellyM, 108, y + 2, 148, y + 2, "i");
// 胸の筋・面の分け（明暗）
c.strokeIn(torso, 96, 130, 100, 168, "b"); c.strokeIn(torso, 160, 130, 156, 168, "a");

// ---------- 脚 ----------
function leg(cx, flip) {
  const P = (x) => (flip ? 255 - x : x);
  const thigh = c.ell(P(cx), 192, 19, 26);
  const shin = c.limb(P(cx - 2), 200, P(cx - 6), 226, 12, 9);
  const foot = c.union(c.ell(P(cx - 8), 232, 17, 8), c.ell(P(cx - 2), 233, 12, 7));
  const m = c.union(thigh, shin, foot);
  c.paint(m, "abcde", { round: 12, bias: -0.14 });
  c.edge(c.union(thigh), "a", "lower");
  // 爪
  const cl = [];
  for (const dx of [-20, -8, 5]) { const x = P(cx - 8 + dx), dir = flip ? -1 : 1; cl.push(c.poly([[x - 3, 236], [x + 3, 236], [x + dir * 1, 246]])); }
  const cm = c.union(...cl); c.paint(cm, "ijkl", { round: 2, dither: false });
  return c.union(m, cm);
}
const legs = c.union(leg(90, false), leg(90, true));

// ---------- 灯り（胸）----------
const cage = c.ell(LX, LY, 17, 20), inner = c.ell(LX, LY, 12, 15);
c.paint(cage, "ijkl", { round: 6, dither: false });
c.edge(cage, "X", "all");
const rnd = (x, y) => [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]][y & 3][x & 3] / 16;
for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) if (inner[y * 256 + x]) {
  const d = Math.hypot((x - LX) / 12, (y - LY - 1) / 15), t = d + (rnd(x, y) - 0.5) * 0.18;
  c.put(x, y, t < 0.3 ? "s" : t < 0.56 ? "r" : t < 0.82 ? "q" : "p");
}
// 炎のゆらめき（上に伸びる）と格子
c.fill(c.poly([[LX - 5, LY - 6], [LX - 1, LY - 20], [LX + 1, LY - 12], [LX + 5, LY - 6]]), "r");
c.fill(c.poly([[LX - 2, LY - 6], [LX, LY - 15], [LX + 2, LY - 6]]), "s");
for (const dx of [-7, 7]) c.line(LX + dx, LY - 13, LX + dx, LY + 13, "j", 1);
c.line(LX - 12, LY - 1, LX + 12, LY - 1, "j", 1);
c.fill(c.rect(LX - 8, LY - 24, LX + 8, LY - 21), "k"); c.fill(c.rect(LX - 6, LY - 27, LX + 6, LY - 25), "l"); c.line(LX - 6, LY - 24, LX + 6, LY - 24, "i");
c.fill(c.rect(LX - 8, LY + 21, LX + 8, LY + 24), "k"); c.line(LX - 8, LY + 24, LX + 8, LY + 24, "i");
c.put(LX - 2, LY + 4, "w"); c.put(LX - 1, LY + 4, "w"); c.put(LX, LY + 3, "w");

// ---------- 頭 ----------
const K = 1.22, tx = (x) => 128 + (x - 128) * K, ty = (y) => 88 + (y - 76) * K, TP = (pts) => pts.map(([x, y]) => [tx(x), ty(y)]);
const skull = c.ell(tx(128), ty(56), 26 * K, 21 * K), brow = c.poly(TP([[100, 50], [128, 40], [156, 50], [152, 60], [104, 60]]));
const snout = c.union(c.ell(tx(128), ty(76), 18 * K, 13 * K), c.ell(tx(128), ty(70), 14 * K, 12 * K));
const jaw = c.ell(tx(128), ty(91), 14 * K, 7 * K);
const frillL = c.poly(TP([[103, 64], [88, 68], [95, 74], [86, 82], [104, 78]])), frillR = c.hmirror(frillL);
c.paint(frillL, "ijkl", { round: 4, dither: false }); c.paint(frillR, "ijkl", { round: 4, dither: false });
c.paint(jaw, "abcde", { round: 6, bias: -0.25 }); c.edge(jaw, "a", "lower");
const upper = c.union(skull, brow, snout);
c.paint(upper, "abcde", { round: 16, bias: -0.1 }); c.edge(upper, "a", "lower");
// 口
const my = ty(84);
c.fill(c.poly([[tx(111), my - 2], [tx(145), my - 2], [tx(141), my + 5], [tx(115), my + 5]]), "z");
c.fill(c.rect(tx(114), my - 2, tx(142), my - 2), "X");
for (const x of [115, 123, 133, 141]) c.fill(c.poly([[tx(x) - 2, my - 2], [tx(x) + 2, my - 2], [tx(x), my + 6]]), "t");
for (const x of [120, 136]) c.fill(c.poly([[tx(x) - 2, my + 5], [tx(x) + 2, my + 5], [tx(x), my - 1]]), "t");
for (const x of [122, 133]) { c.put(tx(x), ty(72), "X"); c.put(tx(x) + 1, ty(72), "X"); }
// 額の稜線と眉
c.strokeIn(skull, 128, ty(42), 128, ty(52), "b");
c.fill(c.poly(TP([[102, 46], [124, 54], [124, 58], [101, 54]])), "a"); c.fill(c.poly(TP([[154, 46], [132, 54], [132, 58], [155, 54]])), "a");
// 目
for (const s of [-1, 1]) { const P = (x) => (s < 0 ? tx(x) : 255 - tx(x)), Y = (y) => ty(y);
  c.fill(c.poly([[P(103), Y(58)], [P(122), Y(55)], [P(124), Y(63)], [P(109), Y(65)]]), "X");
  c.fill(c.poly([[P(106), Y(58.5)], [P(120), Y(56.5)], [P(122), Y(62)], [P(110), Y(63)]]), "r");
  c.fill(c.poly([[P(112), Y(59)], [P(120), Y(58)], [P(121), Y(61.5)], [P(114), Y(62)]]), "s");
  c.put(P(119), Y(59), "w"); c.put(P(118), Y(59), "w"); }
// 角
const hornL = c.strip([[tx(110), ty(48), 10], [tx(94), ty(44), 8.5], [tx(80), ty(36), 7], [tx(72), ty(22), 5], [tx(74), ty(10), 3.4], [tx(82), ty(3), 1]]);
const hornR = c.hmirror(hornL);
for (const h of [hornL, hornR]) { c.paint(h, "ijkl", { round: 6, dither: false }); c.edge(h, "i", "lower"); }
for (const [x0, y0, x1, y1] of [[100, 46, 102, 40], [88, 42, 91, 36], [78, 32, 82, 28], [72, 22, 76, 20]]) { c.strokeIn(hornL, tx(x0), ty(y0), tx(x1), ty(y1), "i"); c.strokeIn(hornR, 255 - tx(x0), ty(y0), 255 - tx(x1), ty(y1), "i"); }
c.fill(c.poly(TP([[123, 38], [128, 24], [133, 38]])), "k"); c.fill(c.poly(TP([[126, 38], [128, 28], [130, 38]])), "l");

// ---------- 灯りの照り返し（うろこが明るくなる）----------
const M1 = { a: "m", b: "n", c: "n", d: "o", e: "o", f: "m", g: "n", h: "o", i: "k", j: "l", k: "l" };
const M2 = { a: "a", b: "m", c: "m", d: "n", e: "n", f: "f", g: "m", h: "n", i: "j", j: "k", k: "l" };
const M3 = { a: "a", b: "b", c: "c", d: "m", e: "m", f: "f", g: "g", h: "m", i: "i", j: "j", k: "k" };
for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) { const ch = c.g[y][x]; if (ch === "." || !M2[ch] || !"abcdefghijk".includes(ch)) continue;
  const d = Math.hypot(x - LX, (y - LY) * 1.1); if (d < 16 || d > 66) continue;
  const t = 1 - (d - 16) / 50, th = t * 0.85 + (rnd(x, y) - 0.5) * 0.3;
  const m = th > 0.7 ? M1 : th > 0.46 ? M2 : th > 0.25 ? M3 : null; if (m) c.g[y][x] = m[ch]; }
c.outline("X", { i: "i", j: "i", k: "j", l: "k", t: "z" });
c.despeckle("wsrpq");
// 落ち影
c.shadow(128, 247, 96, 7, "u");
export const rows = c.rows();
