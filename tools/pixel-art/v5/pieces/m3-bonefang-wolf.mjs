import { Cv, ramp } from "../lib5.mjs";
// 骨牙狼（中型 128×128）: 肋骨と背骨がむき出しの痩せた大オオカミ。灰茶の毛が少し残る。青白く光る目で唸る。
export const name = "骨牙狼"; export const category = "monster"; export const size = 128;
export const pal = {
  ...ramp("abcde", "#3a2a1c", "#f4ecc0", "#b39a62"), // 骨（暗→明）
  ...ramp("fghi", "#2a2420", "#8a7a68"), // 毛
  ...ramp("jk", "#4a1a1c", "#8a3a34"), // 肉
  o: "#120c0c", z: "#07050a", s: "#1a1616",
  w: "#fffbe0", // きば・ハイライト
  ...ramp("lmn", "#2a6a9a", "#e8fbff", "#7ad0f0"), // 目の光
  t: "#5a4a38", // 爪
};
const c = new Cv(128);
const G = 116;
c.shadow(66, G + 2, 54, 5, "s");

// ---- 奥側の脚（暗め） ----
const farFront = c.union(c.limb(52, 72, 50, 92, 5, 3.5), c.limb(50, 92, 56, 106, 3.5, 3), c.ell(58, 111, 7, 3.5));
const farHind = c.union(c.limb(96, 68, 100, 88, 7, 4), c.limb(100, 88, 92, 104, 4, 3), c.ell(93, 111, 8, 3.5));
c.paint(farFront, "abcd", { round: 3, bias: -0.22 });
c.paint(farHind, "abcd", { round: 3, bias: -0.22 });

// ---- しっぽ（骨の連なり） ----
const tailPts = [[110, 54], [116, 48], [120, 40], [120, 31], [115, 24], [109, 21]];
for (let i = 0; i < tailPts.length; i++) {
  const [x, y] = tailPts[i], r = 4.2 - i * 0.5;
  const v = c.ell(x, y, r + 0.6, r);
  c.paint(v, "abcde", { round: 2.5 });
  c.edge(v, "a", "lower");
  if (i + 1 < tailPts.length) { const [X, Y] = tailPts[i + 1]; c.line(x, y, X, Y, "b", 1); }
}
const tailTip = c.poly([[106, 19], [112, 18], [108, 24]]); c.fill(tailTip, "c");

// ---- 胴（肉と毛の薄い被膜）と肋骨 ----
const torso = c.union(c.poly([[42, 52], [70, 46], [104, 52], [104, 66], [94, 72], [78, 74], [66, 79], [52, 84], [43, 78], [40, 64]]), c.ell(50, 66, 9, 16));
c.paint(torso, "fghi", { round: 8, bias: -0.08 });
// 胸の空洞
const cavity = c.union(c.ell(66, 64, 22, 12), c.ell(70, 66, 18, 13));
c.fill(cavity, "z");
c.fill(c.shrink(cavity, 1), "o");
// 肋骨（左のほうが手前で太い）
for (let i = 0; i < 7; i++) {
  const x0 = 50 + i * 6.2, y0 = 52 + (i > 4 ? i - 4 : 0) * 1.2, x1 = x0 - 5 + i * 0.5, y1 = 80 - i * 0.9;
  const rib = c.strip([[x0, y0, 1.6], [x0 + 2, y0 + 8, 1.9], [x1 + 3, y1 - 6, 1.7], [x1, y1, 1.2]]);
  c.paint(rib, "cde", { round: 1.6, dither: false });
  c.edge(rib, "b", "lower");
}
// 胸骨と、つづく肋のすきまの暗がり
c.fill(c.strip([[47, 60, 1.2], [46, 72, 1.6], [50, 80, 1.2]]), "d");
// 毛のまだら（腹側・背中側）
const furPatchA = c.union(c.ell(88, 72, 9, 3), c.ell(60, 78, 8, 2.5));
c.paint(c.inter(furPatchA, c.ell(70, 64, 32, 24)), "fghi", { round: 3 });
c.speckle(c.ell(66, 80, 22, 3), "h", 0.25, 5);
// むき出しの肉の傷
c.fill(c.ell(80, 50, 4, 2.2), "k"); c.fill(c.ell(79, 49.5, 2, 1), "j");
c.fill(c.ell(90, 74, 3, 2), "j"); c.put(91, 74, "k");

// ---- 背骨（背中のライン）と骨のとげ ----
const spine = c.strip([[44, 47, 3.4], [60, 44, 3], [78, 45, 3], [96, 49, 3.2], [106, 54, 3.4]]);
c.paint(spine, "abcde", { round: 2.5, dither: false });
c.edge(spine, "b", "lower");
for (let i = 0; i < 9; i++) {
  const x = 48 + i * 6.6, y = 46 - Math.sin(i / 8 * Math.PI) * 1.5 + (i > 5 ? (i - 5) * 1.6 : 0), hgt = 11 - Math.abs(i - 3) * 0.9;
  const sp = c.poly([[x - 2.6, y + 1], [x + 1.4, y - hgt], [x + 2.8, y + 1]]);
  c.paint(sp, "cde", { round: 2, dither: false });
  c.edge(sp, "b", "lower");
}
// 腰の骨（骨盤）
const pelvis = c.union(c.ell(100, 60, 8, 8), c.poly([[94, 52], [108, 52], [110, 62], [102, 68]]));
c.paint(pelvis, "abcde", { round: 5 });
c.edge(pelvis, "a", "lower");
// 肩甲骨
const scap = c.poly([[42, 48], [60, 46], [58, 58], [46, 66]]);
c.paint(scap, "bcde", { round: 4 });
c.edge(scap, "a", "lower");

// ---- 手前の後ろ脚（太ももに毛と肉が残る） ----
const thigh = c.union(c.ell(102, 72, 11, 13), c.limb(104, 78, 112, 92, 6, 4));
c.paint(thigh, "fghi", { round: 8, bias: -0.02 });
c.speckle(c.inter(thigh, c.ell(102, 72, 9, 9)), "h", 0.2, 9);
const hindLower = c.union(c.limb(112, 90, 106, 102, 3.6, 3.2), c.limb(106, 102, 100, 112, 3.2, 3), c.ell(99, 112, 9, 3.6));
c.paint(hindLower, "bcde", { round: 3 });
c.edge(hindLower, "a", "lower");
c.fill(c.ell(112, 91, 3, 3), "d"); c.put(111, 90, "e");
// ---- 手前の前脚 ----
const foreUpper = c.union(c.limb(52, 70, 47, 90, 7, 4.5), c.ell(50, 74, 7, 8));
c.paint(foreUpper, "fghi", { round: 5 });
c.speckle(foreUpper, "h", 0.15, 12);
const foreLower = c.union(c.limb(47, 90, 40, 104, 3.8, 3.4), c.limb(40, 104, 34, 112, 3.4, 3.2), c.ell(35, 112, 9, 3.8));
c.paint(foreLower, "bcde", { round: 3 });
c.edge(foreLower, "a", "lower");
c.fill(c.ell(47, 91, 3, 3), "d"); c.put(46, 90, "e");

// ---- 爪（踏ん張って地面をつかむ） ----
for (const [cx, cy] of [[35, 113], [58, 112], [99, 113], [93, 112]]) {
  for (let i = 0; i < 4; i++) { const x = cx - 10 + i * 2.6; c.line(x, cy, x - 1.5, cy + 4, "e"); c.put(x, cy, "c"); }
}
// 首まわりの毛のふさ
for (const [x, y, hh] of [[38, 44, 7], [42, 42, 8], [46, 44, 6], [50, 84, 5], [56, 85, 4], [64, 82, 4]]) {
  const f = c.poly([[x - 2, y + 4], [x + 0.5, y - hh + (y > 60 ? 8 : 0) * 0], [x + 3, y + 4]]);
  if (y < 60) c.paint(f, "fghi", { round: 2, dither: false }); else c.fill(c.poly([[x - 2, y - 2], [x, y + hh], [x + 3, y - 2]]), "g");
}
// ---- 頭（正面寄り、3/4） ----
const ear1 = c.poly([[18, 44], [14, 26], [27, 38]]);
const ear2 = c.poly([[34, 40], [38, 24], [43, 44]]);
c.paint(ear2, "fghi", { round: 3, bias: -0.15 });
c.paint(ear1, "fghi", { round: 3 });
c.fill(c.poly([[18, 41], [16, 32], [23, 38]]), "k");
c.fill(c.poly([[36, 40], [38, 31], [40, 41]]), "j");
c.speckle(ear1, "a", 0.0, 1);
// 首（背骨がつづく）
const neck = c.union(c.ell(42, 56, 11, 11), c.limb(46, 50, 38, 58, 8, 11));
c.paint(neck, "fghi", { round: 8 });
c.speckle(neck, "h", 0.2, 21);
const skull = c.union(c.ell(28, 52, 15, 13), c.limb(24, 58, 8, 68, 10, 5.2));
c.paint(skull, "abcde", { round: 9, bias: -0.14 });
// 額・頬の毛
const furHead = c.union(c.ell(38, 46, 9, 6), c.ell(40, 58, 6, 5));
c.paint(c.inter(furHead, skull), "fghi", { round: 3 });
c.speckle(c.inter(furHead, skull), "i", 0.25, 4);
// 鼻すじの骨の割れ
c.strokeIn(skull, 20, 54, 12, 63, "b");
c.strokeIn(skull, 14, 62, 10, 65, "a");
// 口の中（暗い）→ 下あご（暗めの骨）→ 舌 → きば
const mouth = c.poly([[7, 68], [30, 63], [32, 76], [16, 88], [8, 84]]);
c.fill(mouth, "z");
const jaw = c.union(c.limb(32, 77, 13, 90, 4.6, 3.2), c.limb(33, 68, 30, 78, 5, 4.5));
c.paint(jaw, "abcde", { round: 3.5, bias: -0.3 });
c.edge(jaw, "a", "lower");
c.fill(c.ell(21, 74, 6, 2.2), "k"); c.fill(c.ell(20, 73.5, 3.5, 1), "j");
c.line(7, 67, 30, 62, "a"); c.line(8, 68, 30, 63, "b");
// 上のきば（長く曲がる）
c.fill(c.poly([[8, 68], [4, 83], [13, 69]]), "w"); c.edge(c.poly([[8, 68], [4, 83], [13, 69]]), "d", "lower");
c.fill(c.poly([[16, 67], [14, 80], [21, 66]]), "w"); c.put(15, 79, "e");
c.fill(c.poly([[23, 65], [23, 73], [28, 64]]), "e");
// 下のきば
c.fill(c.poly([[12, 87], [11, 79], [16, 84]]), "e");
c.fill(c.poly([[20, 82], [20, 76], [24, 79]]), "d");

// 鼻先
c.fill(c.ell(7, 65, 3, 2.2), "z"); c.put(6, 64, "d");
// 目のくぼみ（手前の大きな眼窩と、奥の小さな眼窩）
c.fill(c.ell(21, 50, 6.6, 5.6), "z"); c.fill(c.ell(21, 49, 5.4, 4.2), "o");
c.fill(c.ell(36, 48, 5, 4.4), "z");
c.fill(c.ell(21, 51, 3.4, 2.8), "m"); c.fill(c.ell(21, 51, 2.2, 1.8), "n"); c.put(20, 49, "w"); c.put(21, 49, "w");
c.fill(c.ell(36, 48.6, 2.6, 2.2), "m"); c.fill(c.ell(36, 48.6, 1.6, 1.3), "n"); c.put(35, 48, "w");
// 眉の骨のはり出し（にらむ）
c.line(15, 46, 26, 48, "b"); c.line(30, 43, 40, 46, "b");
c.line(15, 45, 25, 47, "e"); c.line(30, 42, 39, 45, "d");
// 鼻孔の上の骨の陰
c.put(11, 62, "a"); c.put(12, 62, "a");

// 目の光のにじみ（外側）
for (const [x, y] of [[15, 50], [27, 50], [30, 46], [40, 48]]) if (c.get(x, y) !== "z" && c.get(x, y) !== ".") { /* 何もしない */ }

c.outline("o", { a: "o", b: "a", c: "b", d: "b", e: "c", f: "o", g: "o", h: "g", i: "g", j: "o", k: "j", t: "o", w: "c" });
c.despeckle("wlmnt");
export const rows = c.rows();
