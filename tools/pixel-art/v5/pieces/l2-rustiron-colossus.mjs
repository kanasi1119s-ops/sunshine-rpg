import { Cv, ramp, rng } from "../lib5.mjs";
// 錆鉄の巨兵（大型・中ボス級 176×176）: 古い時代の錆びた鉄の巨大な人型兵器。胸の割れた動力窓から橙の光が漏れ、兜の細い目が緑に光る。
export const name = "錆鉄の巨兵"; export const category = "monster"; export const size = 176;
// 鉄 a〜f（暗→明）、錆 g〜j、動力の光 k l m、緑の目 n p q、輪郭 o、錆の輪郭 r、影 s、隙間の闇 t、白 w
export const pal = { ...ramp("abcdef", "#141a28", "#b4c6d6", "#465a7c"), ...ramp("ghij", "#4a2214", "#e08838", "#a4501e"), ...ramp("klm", "#e05a10", "#fff2a0", "#ffa830"), ...ramp("npq", "#0a5a3a", "#d8ffd0", "#3ce88a"), o: "#0a0e18", r: "#22100c", y: "#fff8c8", s: "#1a1830", t: "#05070c", w: "#ffffff" };
const c = new Cv(176);
// 値ノイズ（錆のまだら用）
const noise = (seed, sc) => { const R = rng(seed), G = 64, t = Array.from({ length: G * G }, () => R()); const f = (x, y) => { x /= sc; y /= sc; const xi = Math.floor(x), yi = Math.floor(y), fx = x - xi, fy = y - yi, s = (u) => u * u * (3 - 2 * u); const v = (a, b) => t[((b % G + G) % G) * G + ((a % G + G) % G)]; return (v(xi, yi) * (1 - s(fx)) + v(xi + 1, yi) * s(fx)) * (1 - s(fy)) + (v(xi, yi + 1) * (1 - s(fx)) + v(xi + 1, yi + 1) * s(fx)) * s(fy); }; return f; };
const n1 = noise(11, 9), n2 = noise(5, 4);
/** 錆のまだらを部品の上に載せる */
const rust = (m, th = 0.6, seedOff = 0) => { th += 0.07; for (let y = 0; y < 176; y++) for (let x = 0; x < 176; x++) if (m[y * 176 + x]) { const v = n1(x + seedOff, y + seedOff * 2) * 0.7 + n2(x, y + seedOff) * 0.3; if (v > th) { const d = v - th; const cur = c.g[y][x]; const lit = "def".includes(cur) ? 1 : 0; c.g[y][x] = d > 0.13 ? (lit ? "i" : "h") : d > 0.06 ? (lit ? "i" : "h") : "g"; if (d > 0.2 && lit) c.g[y][x] = "j"; if (d > 0.03 && ((x * 7 + y * 3 + seedOff) % 23 === 0)) for (let k = 1; k < 3 + (x % 4); k++) if (m[(y + k) * 176 + x]) c.g[y + k][x] = "h"; } } };
const rivet = (x, y) => { c.put(x, y, "f"); c.put(x + 1, y, "d"); c.put(x, y + 1, "c"); c.put(x + 1, y + 1, "b"); };
const seam = (m, x0, y0, x1, y1) => { c.strokeIn(m, x0, y0, x1, y1, "a"); c.strokeIn(m, x0 - 1, y0 - 1, x1 - 1, y1 - 1, "e"); };

// ---- 落ち影 ----
c.shadow(88, 168, 74, 6, "s");

// ---- 奥の部品から順に ----
// 脚（太い柱2本＋膝・すね当て）
const legL = c.union(c.rect(54, 120, 82, 156), c.poly([[50, 156], [84, 156], [86, 166], [46, 166]]));
const legR = c.union(c.rect(94, 120, 122, 156), c.poly([[92, 156], [126, 156], [130, 166], [90, 166]]));
c.paint(legL, "abcde", { round: 12 }); c.paint(legR, "abcde", { round: 12 });
// 腰
const hip = c.union(c.rect(54, 108, 122, 122), c.poly([[54, 122], [122, 122], [114, 130], [62, 130]]));
c.paint(hip, "abcde", { round: 8 });
// 胴（胸板：台形で肩が広い）
const torso = c.poly([[46, 58], [130, 58], [126, 88], [118, 112], [58, 112], [50, 88]]);
c.paint(torso, "abcde", { round: 16 });
// 首
const neck = c.rect(78, 44, 98, 62); c.paint(neck, "abcd", { round: 8 });
// 頭（兜）
const head = c.union(c.poly([[68, 46], [70, 26], [78, 14], [98, 14], [106, 26], [108, 46]]), c.rect(72, 40, 104, 52));
c.paint(head, "abcdef", { round: 14 });
const crest = c.poly([[86, 4], [90, 4], [92, 16], [84, 16]]); // 兜の飾り（折れた角）
c.paint(crest, "abcde", { round: 3 });
// 兜の額当てと顎
const brow = c.rect(70, 28, 106, 32); c.paint(brow, "abcd", { round: 3, flat: 0.3 });
const jaw = c.poly([[74, 46], [102, 46], [98, 54], [78, 54]]); c.paint(jaw, "abcd", { round: 4 });
// 目の穴（細い横長）
const eyeL = c.rect(74, 35, 85, 38), eyeR = c.rect(91, 35, 102, 38);
c.fill(c.union(eyeL, eyeR), "t");
c.fill(c.rect(75, 36, 84, 37), "p"); c.fill(c.rect(92, 36, 101, 37), "p");
c.fill(c.rect(77, 36, 82, 36), "q"); c.fill(c.rect(94, 36, 99, 36), "q"); c.put(79, 36, "w"); c.put(96, 36, "w");
// 兜の縦の通気口
for (let x = 80; x <= 96; x += 4) c.fill(c.rect(x, 43, x + 1, 50), "a");
c.fill(c.rect(87, 20, 88, 34), "b"); // 鼻筋の継ぎ目

// 腕（円筒）
const armL = c.union(c.limb(30, 78, 30, 122, 14, 12), c.rect(18, 92, 44, 116));
const armR = c.union(c.limb(146, 78, 146, 122, 14, 12), c.rect(132, 92, 158, 116));
c.paint(armL, "abcde", { round: 12 }); c.paint(armR, "abcde", { round: 12, light: [-0.3, -0.75] });
// 腕の輪（肘・手首の帯）
for (const [cx] of [[30], [146]]) { const b1 = c.rect(cx - 15, 98, cx + 15, 103), b2 = c.rect(cx - 13, 118, cx + 13, 122); c.paint(c.inter(b1, cx < 88 ? armL : armR), "bcdef", { round: 3, flat: 0.2 }); c.paint(c.inter(b2, cx < 88 ? armL : armR), "bcdef", { round: 3, flat: 0.2 }); }
// 手（ごつい拳）
const handL = c.union(c.ell(30, 136, 17, 15), c.rect(16, 124, 44, 138)), handR = c.union(c.ell(146, 136, 17, 15), c.rect(132, 124, 160, 138));
c.paint(handL, "abcdef", { round: 10 }); c.paint(handR, "abcdef", { round: 10 });
for (const [hx, hm] of [[30, handL], [146, handR]]) { for (const dx of [-8, 0, 8]) c.strokeIn(hm, hx + dx, 134, hx + dx, 149, "a"); c.edge(c.inter(hm, c.rect(hx - 20, 127, hx + 20, 128)), "a"); }

// 肩当て（左は無傷、右は欠け）
const shL = c.union(c.ell(30, 68, 26, 20), c.rect(6, 66, 54, 84));
const shLm = c.sub(shL, c.rect(0, 86, 60, 100), c.poly([[0, 0], [10, 0], [0, 50]]));
const shR0 = c.union(c.ell(146, 68, 26, 20), c.rect(122, 66, 170, 84));
const bite = c.poly([[176, 40], [176, 84], [166, 78], [162, 68], [156, 68], [152, 58], [146, 58], [143, 48], [136, 44], [136, 36]]);
const shRm = c.sub(shR0, c.rect(0, 86, 176, 100), bite, c.poly([[150, 84], [170, 84], [162, 76], [156, 80]]), c.poly([[122, 70], [128, 66], [130, 74]]));
c.paint(shLm, "abcdef", { round: 16 }); c.paint(shRm, "abcdef", { round: 16 }); c.edge(shLm, "a", "lower"); c.edge(shRm, "a", "lower");
// 肩当ての段（重ねた板）
for (const [m, x0, x1] of [[shLm, 8, 54], [shRm, 122, 168]]) { for (const y of [72, 79]) { c.strokeIn(m, x0, y, x1, y + 2, "a"); c.strokeIn(m, x0, y - 1, x1, y + 1, "e"); } }
// 肩と胴の間の暗いすき間
c.fill(c.inter(c.rect(52, 62, 56, 86), torso), "a");

// 胸の板と動力窓
const chestPlate = c.poly([[62, 66], [114, 66], [110, 108], [66, 108]]);
c.paint(chestPlate, "abcde", { round: 10, flat: 0.15 });
c.edge(chestPlate, "a", "lower"); c.edge(chestPlate, "e", "upper");
const win = c.ell(88, 86, 17, 17), winIn = c.ell(88, 86, 14, 14);
c.fill(win, "a"); c.paint(win, "abcdef", { round: 3, flat: 0.1 });
c.fill(winIn, "t");
// 光（中心ほど明るい）
for (let y = 68; y < 106; y++) for (let x = 70; x < 106; x++) if (winIn[y * 176 + x]) { const d = Math.hypot(x - 88, y - 86); c.g[y][x] = d < 3 ? "y" : d < 6 ? "m" : d < 9.5 ? "l" : d < 12 ? "k" : "g"; }
c.fill(c.inter(winIn, c.poly([[70, 100], [106, 100], [106, 106], [70, 106]])), "t");
// 割れ目（窓を斜めに走る亀裂と、欠け）
c.line(78, 76, 84, 84, "t"); c.line(84, 84, 82, 92, "t"); c.line(82, 92, 88, 100, "t"); c.line(93, 72, 91, 79, "t");
c.fill(c.poly([[89, 70], [96, 74], [92, 78]]), "t");
// 窓の光が周りの鉄にうつる
for (let y = 66; y < 108; y++) for (let x = 64; x < 114; x++) { const d = Math.hypot(x - 88, y - 86); if (d > 17 && d < 22 && chestPlate[y * 176 + x] && "abcde".includes(c.g[y][x]) && ((x + y) & 1) === 0) c.g[y][x] = d < 19.5 ? "i" : "h"; }
// 窓の光のにじみ（外へ）
for (const [x, y] of [[88, 66], [70, 84], [106, 92], [76, 100], [102, 104]]) c.put(x, y, "j");
// 割れた窓の縁の欠け
c.put(74, 74, "t"); c.put(75, 73, "t");

// 腹の板と腰帯
const belt = c.rect(58, 108, 118, 118); c.paint(belt, "bcde", { round: 4, flat: 0.2 }); c.edge(belt, "a", "lower");
const buckle = c.rect(80, 108, 96, 120); c.paint(buckle, "cdef", { round: 4 }); c.edge(buckle, "a");

// 膝当て
const kneeL = c.ell(70, 141, 15, 9), kneeR = c.ell(106, 141, 15, 9);
c.paint(kneeL, "bcdef", { round: 6 }); c.paint(kneeR, "bcdef", { round: 6 });
c.edge(kneeL, "a", "lower"); c.edge(kneeR, "a", "lower");
// 足の甲の板
for (const [x0, x1] of [[50, 86], [90, 126]]) { const f = c.rect(x0, 156, x1, 164); c.paint(c.inter(f, c.union(legL, legR)), "bcde", { round: 3, flat: 0.3 }); c.strokeIn(c.rect(0, 0, 175, 175), x0 + 4, 160, x1 - 4, 160, "a"); }
// 脚の間の暗い隙間
c.fill(c.rect(83, 130, 93, 156), "a"); c.fill(c.rect(85, 132, 91, 156), "t");

// ---- 質感 ----
const bodyAll = c.union(legL, legR, hip, torso, neck, head, armL, armR, handL, handR, shLm, shRm, kneeL, kneeR, chestPlate, belt, buckle, jaw, brow);
// 鉄板のつなぎ目
seam(torso, 47, 60, 62, 66); seam(torso, 129, 60, 114, 66);
seam(hip, 58, 120, 118, 120);
seam(legL, 58, 146, 84, 146); seam(legR, 92, 146, 118, 146);
seam(armL, 18, 108, 44, 108); seam(armR, 132, 108, 158, 108);
seam(head, 72, 44, 104, 44);
// 板の継ぎ目（縦）
seam(chestPlate, 64, 90, 64, 108); seam(chestPlate, 112, 90, 112, 108);
seam(torso, 88, 108, 88, 112);
// 錆
rust(c.union(legL, legR, hip), 0.56, 3); rust(c.sub(torso, c.grow(win, 3)), 0.52, 9); rust(c.union(armL, armR), 0.5, 17); rust(c.union(shLm, shRm), 0.48, 23);
rust(c.union(handL, handR), 0.5, 31); rust(c.sub(head, c.rect(70, 33, 106, 40)), 0.6, 41); rust(c.union(kneeL, kneeR, belt), 0.5, 47);
// リベット
for (const [x, y] of [[66, 70], [110, 70], [66, 104], [110, 104], [58, 112], [116, 112], [12, 74], [22, 82], [42, 74], [50, 82], [132, 74], [142, 82], [160, 76], [72, 130], [104, 130], [61, 150], [82, 150], [95, 150], [116, 150], [22, 100], [38, 100], [136, 100], [152, 100], [22, 120], [38, 120], [136, 120], [152, 120], [76, 30], [98, 30], [80, 46], [94, 46]]) rivet(x, y);
// 窓の枠のリベット
for (let a = 0; a < 8; a++) { const t = a * Math.PI / 4; rivet(Math.round(88 + Math.cos(t) * 15.5) - 1, Math.round(86 + Math.sin(t) * 15.5) - 1); }
// 縁の光
c.rim(shLm, { a: "b", b: "d", c: "e", d: "f", e: "f", g: "i", h: "i" }); c.rim(shRm, { a: "b", b: "d", c: "e", d: "f", e: "f", g: "i", h: "i" });
c.rim(head, { a: "c", b: "d", c: "e", d: "f", e: "f" }); c.rim(torso, { b: "d", c: "e", d: "f" });
c.rim(c.union(armL, handL), { b: "d", c: "e", d: "f", e: "f" }); c.rim(c.union(armR, handR), { b: "d", c: "e", d: "f", e: "f" });
// 強い反射（金属の照り）
for (const [x, y, w, h] of [[14, 62, 3, 8], [34, 58, 8, 2], [64, 62, 10, 2], [72, 20, 5, 2], [24, 92, 2, 14], [60, 128, 2, 20], [96, 128, 2, 20], [124, 62, 4, 2]]) c.fill(c.rect(x, y, x + w - 1, y + h - 1), "f");
c.fill(c.rect(21, 98, 24, 98), "f"); c.fill(c.rect(69, 138, 72, 138), "f"); c.fill(c.rect(78, 18, 81, 18), "f");
// 欠けた縁に見える錆の断面（右肩）
const cutE = c.inter(shRm, c.grow(bite, 1)); c.fill(cutE, "i"); c.fill(c.inter(cutE, c.shift(cutE, 0, -1)), "h"); for (let y = 40; y < 90; y++) for (let x = 130; x < 176; x++) if (cutE[y * 176 + x] && (x + y) % 5 === 0) c.g[y][x] = "j";
c.strokeIn(shRm, 150, 84, 156, 80, "h");

// 垂れた鎖（左肩の下から腰へ、右の欠け目からも）
const chain = (x0, y0, x1, y1, sag) => { const n = 20; const pts = []; for (let i = 0; i <= n; i++) { const t = i / n; pts.push([x0 + (x1 - x0) * t + Math.sin(t * Math.PI) * 2, y0 + (y1 - y0) * t + Math.sin(t * Math.PI) * sag]); } pts.forEach(([x, y], i) => { const m = (i % 2 === 0); if (m) { c.fill(c.ell(x, y, 2.6, 3.2), "b"); c.fill(c.ell(x, y, 1.2, 1.8), "t"); c.put(x - 1, y - 2, "e"); } else { c.fill(c.ell(x, y, 1.4, 3.0), "c"); c.put(x, y - 2, "f"); } }); };
chain(56, 84, 62, 122, -6);
chain(150, 82, 158, 126, 4);
// 瓦礫（足元）
const rub = (cx, cy, rx, ry, rot) => { const m = c.poly([[cx - rx, cy + ry], [cx - rx * 0.7, cy - ry], [cx + rx * 0.3, cy - ry * 1.1], [cx + rx, cy + ry * 0.2], [cx + rx * 0.8, cy + ry]]); c.paint(m, "abcde", { round: 3 }); c.edge(m, "a", "lower"); c.rim(m, { b: "d", c: "e", d: "f" }); return m; };
const rubs = [rub(30, 162, 9, 5), rub(14, 166, 6, 3), rub(150, 163, 10, 5), rub(166, 167, 6, 3), rub(44, 169, 5, 2), rub(134, 169, 6, 3), rub(72, 172, 4, 2), rub(104, 172, 5, 2)];
for (const m of rubs) rust(m, 0.55, 5);
// 瓦礫の砂の粒
c.speckle(c.rect(6, 168, 168, 172), "b", 0.03, 8);

// ---- 輪郭 ----
c.outline("o", { a: "o", b: "a", c: "a", d: "b", e: "b", f: "c", g: "r", h: "r", i: "g", j: "h", t: "o", p: "a", q: "a", k: "g", l: "g", m: "h", s: ".", w: "c" });
c.despeckle("wfmlqpkj");
// 光のにじみ（輪郭の外、窓のまわりは胸の中なので内側のみ）
export const rows = c.rows();
