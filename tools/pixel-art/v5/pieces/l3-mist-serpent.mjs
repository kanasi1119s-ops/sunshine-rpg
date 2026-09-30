import { Cv, ramp } from "../lib5.mjs";
// 霧の大蛇（大型 192×192・中ボス級）: 大きなとぐろを巻き、鎌首を高くもたげた青緑〜白の大蛇。額に冠のようなひれ、金色の目、二又の舌。まわりにうっすら霧。
export const name = "霧の大蛇"; export const category = "monster"; export const size = 192;
export const pal = {
  ...ramp("abcdef", "#0c2c38", "#eafcf4", "#2f9c90"), // 体（青緑→白）
  ...ramp("ghij", "#a8863e", "#fff6c8", "#f0dc90"), // 腹（淡い黄色）
  ...ramp("klm", "#7a2c58", "#f6a8b8", "#d8587a"), // ひれ
  o: "#07161e", y: "#ffc820", Y: "#fff8b0", E: "#10141c",
  r: "#9c2a44", R: "#4a1024", t: "#f0506a", w: "#ffffff", W: "#b8ccd4",
  n: "#dcefff", m: "#8cbce4", s: "#0c2230",
};
const c = new Cv(192);
const B = "abcdef", BELLY = "ghij", FIN = "klm";
const rgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
// ---------- 道具（この絵の中だけ）----------
function chaikin(p, n = 2) { for (let k = 0; k < n; k++) { const o = [p[0]]; for (let i = 0; i + 1 < p.length; i++) { const a = p[i], b = p[i + 1]; o.push(a.map((v, j) => v * 0.75 + b[j] * 0.25), a.map((v, j) => v * 0.25 + b[j] * 0.75)); } o.push(p[p.length - 1]); p = o; } return p; }
function resample(p, step) { const o = [p[0]]; let acc = 0; for (let i = 0; i + 1 < p.length; i++) { const a = p[i], b = p[i + 1], L = Math.hypot(b[0] - a[0], b[1] - a[1]); let d = step - acc; while (d <= L) { const t = d / L; o.push(a.map((v, j) => v + (b[j] - v) * t)); d += step; } acc = L - (d - step); } return o; }
function frame(p, i) { const a = p[Math.max(0, i - 1)], b = p[Math.min(p.length - 1, i + 1)]; let tx = b[0] - a[0], ty = b[1] - a[1]; const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l; return { tx, ty, nx: -ty, ny: tx }; } // n = 進行方向の右手（背側）
const offs = (p, k) => p.map((q, i) => { const f = frame(p, i); return [q[0] + f.nx * q[2] * k, q[1] + f.ny * q[2] * k, q[2]]; });
function diamonds(cv, path, mask, gap, k, sx, sy, dark, light) { const s = resample(path, gap); s.forEach((q, i) => { const f = frame(s, i), cx = q[0] + f.nx * q[2] * k, cy = q[1] + f.ny * q[2] * k, a = sx * (q[2] / 10), b = sy * (q[2] / 10); const d = cv.poly([[cx + f.tx * a, cy + f.ty * a], [cx + f.nx * b, cy + f.ny * b], [cx - f.tx * a, cy - f.ty * a], [cx - f.nx * b, cy - f.ny * b]]); const dm = cv.inter(d, mask); cv.fill(dm, dark); cv.edge(dm, light, "upper"); }); }
function spikes(path, gap, h0, h1, w, lean = 0.5) { const s = resample(path, gap), out = []; s.forEach((q, i) => { const f = frame(s, i), t = i / (s.length - 1), h = h0 + (h1 - h0) * t, bx = q[0] + f.nx * q[2] * 0.7, by = q[1] + f.ny * q[2] * 0.7; out.push(c.poly([[bx - f.tx * w, by - f.ty * w], [bx + f.tx * w, by + f.ty * w], [q[0] + f.nx * (q[2] + h) - f.tx * h * lean, q[1] + f.ny * (q[2] + h) - f.ty * h * lean]])); }); return out; }
function ellPts(cx, cy, rx, ry, r, a0, a1, n = 48) { const p = []; for (let i = 0; i <= n; i++) { const a = a0 + (a1 - a0) * (i / n); p.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry, r]); } return p; }
// ---------- 落ち影 ----------
c.shadow(94, 181, 84, 6, "s");
// ---------- しっぽ（いちばん奥）----------
const tailP = chaikin([[146, 156, 9.5], [160, 160, 8.5], [174, 156, 7], [183, 146, 5.6], [184, 134, 4.2], [178, 124, 3], [170, 119, 2], [163, 121, 1.2]], 2);
const tailM = c.strip(tailP);
for (const sp of spikes(tailP.slice(8), 8, 5, 2, 2.4)) { c.paint(sp, FIN, { round: 2, flat: 0.3 }); c.edge(sp, "k"); }
c.paint(tailM, B, { round: 6, bias: -0.12 }); c.edge(tailM, "a", "lower");
diamonds(c, tailP.slice(0, 30), tailM, 9, -0.1, 3.4, 2.4, "b", "d");
// ---------- とぐろ ----------
function coil(cx, cy, rx, ry, r, bias, seed) {
  const back = c.strip(ellPts(cx, cy, rx, ry, r, 0, Math.PI * 2, 72));
  c.paint(back, B, { round: r + 1, bias: bias - 0.28 }); c.edge(back, "a");
  const fp = ellPts(cx, cy, rx, ry, r, 0.03 * Math.PI, 0.97 * Math.PI, 60), front = c.strip(fp);
  c.paint(front, B, { round: r + 1, bias });
  // 腹（下の縁に淡い黄色の帯＋横縞）
  const bp = ellPts(cx, cy + r * 0.85, rx - 1, ry, r * 0.55, 0.08 * Math.PI, 0.92 * Math.PI, 60), bm = c.inter(c.strip(bp), front);
  c.paint(bm, BELLY, { round: r * 0.5, bias: 0.1 });
  for (let y = cy; y < cy + ry + r + 2; y += 3) for (let x = 0; x < 192; x++) if (bm[y * 192 + x] && c.get(x, y) !== "g") c.put(x, y, c.get(x, y) === "j" ? "i" : c.get(x, y) === "i" ? "h" : "g");
  c.edge(bm, "g", "upper");
  // 背のうろこ模様（大きなひし形）
  const dp = ellPts(cx, cy - 1, rx, ry, r, 0.06 * Math.PI, 0.94 * Math.PI, 60);
  diamonds(c, dp, c.sub(front, bm), r * 1.15, 0.2, 5.6, 4.2, "b", "d");
  c.rim(front, { a: "b", b: "c", c: "d", d: "e" });
  c.edge(front, "a", "all");
  return { back, front };
}
const cA = coil(92, 158, 60, 10, 11, -0.3, 3);
const cB = coil(96, 135, 47, 9, 11, -0.2, 5);
// ---------- 首（三段目の奥→首→手前）----------
const cCback = c.strip(ellPts(90, 113, 34, 7, 10.5, 0, Math.PI * 2, 60));
c.paint(cCback, B, { round: 11, bias: -0.2 }); c.edge(cCback, "a");
const neckP = chaikin([[92, 112, 12], [98, 98, 11.5], [102, 84, 11], [100, 68, 10.2], [93, 53, 9.6], [84, 42, 9.6], [76, 36, 10]], 2);
for (const sp of spikes(neckP.slice(3), 8, 9, 6, 3.2, 0.7)) { c.paint(sp, FIN, { round: 3, flat: 0.2 }); c.edge(sp, "k"); }
const neckM = c.strip(neckP);
c.paint(neckM, B, { round: 11, bias: 0.12 });
const nb = c.inter(c.strip(offs(neckP, -0.55).map((q) => [q[0], q[1], q[2] * 0.5])), neckM);
c.paint(nb, BELLY, { round: 5, bias: 0.05 });
for (let y = 30; y < 118; y += 3) for (let x = 0; x < 192; x++) if (nb[y * 192 + x]) c.put(x, y, c.get(x, y) === "j" ? "i" : c.get(x, y) === "i" ? "h" : "g");
c.edge(nb, "g", "upper");
diamonds(c, neckP.slice(0, 24), c.sub(neckM, nb), 11, 0.32, 5, 3.6, "b", "e");
c.rim(neckM, { a: "b", b: "c", c: "d", d: "e" });
c.edge(neckM, "a", "all");
const cC = coil(90, 113, 34, 7, 10.5, -0.08, 9);
// ---------- 頭 ----------
const mouthIn = c.poly([[30, 34], [50, 34], [84, 36], [92, 44], [86, 53], [56, 55], [38, 59], [30, 50]]);
c.paint(mouthIn, "rRt", { round: 7, dither: false, bias: -0.1 });
c.fill(c.sub(mouthIn, c.rect(0, 0, 191, 41)), "R"); c.fill(c.sub(mouthIn, c.rect(0, 0, 191, 45), c.rect(0, 52, 191, 191)), "r");
const upper = c.poly([[88, 28], [82, 18], [68, 13], [50, 15], [38, 21], [27, 29], [22, 35], [29, 38], [42, 36], [56, 37], [70, 37], [84, 37], [92, 34]]);
c.paint(upper, B, { round: 9, bias: 0.14 });
const lower = c.poly([[88, 50], [72, 50], [56, 52], [42, 56], [30, 60], [27, 64], [42, 68], [62, 68], [80, 65], [92, 58]]);
c.paint(lower, BELLY, { round: 8, bias: -0.05 });
for (let y = 52; y < 70; y += 3) for (let x = 0; x < 192; x++) if (lower[y * 192 + x] && x > 44) c.put(x, y, c.get(x, y) === "j" ? "i" : c.get(x, y) === "i" ? "h" : "g");
c.edge(lower, "a", "all"); c.edge(upper, "a", "all");
c.rim(upper, { b: "d", c: "e", d: "f" });
c.fill(c.ell(30, 30, 1.8, 1.3), "a");
c.strokeIn(upper, 84, 30, 74, 36, "b"); c.strokeIn(upper, 78, 22, 70, 32, "c");
c.strokeIn(lower, 86, 56, 70, 64, "i"); c.strokeIn(lower, 78, 54, 62, 62, "h");
diamonds(c, [[76, 27, 9], [60, 26, 7], [46, 27, 5]], c.sub(upper, c.rect(0, 33, 191, 60)), 12, 0.35, 4, 2.6, "b", "e");
c.strokeIn(upper, 46, 20, 40, 30, "b"); c.strokeIn(upper, 34, 26, 32, 33, "b");
// 目（金色）と眉
const eyeM = c.poly([[54, 24], [60, 21], [69, 22], [73, 26], [64, 28]]);
c.fill(c.grow(eyeM), "o"); c.fill(eyeM, "y");
c.fill(c.rect(60, 22, 68, 23), "Y"); c.fill(c.rect(64, 22, 65, 27), "E"); c.put(63, 22, "w");
c.line(52, 23, 62, 18, "a"); c.line(62, 18, 76, 22, "a"); c.line(54, 21, 63, 16, "b");
// 牙（上は長く、下は短く）
const fu1 = c.poly([[38, 36], [47, 36], [41, 57]]), fu2 = c.poly([[56, 37], [63, 37], [59, 49]]), fl1 = c.poly([[34, 60], [41, 58], [36, 47]]), fl2 = c.poly([[52, 54], [57, 53], [55, 46]]);
for (const f of [fu1, fu2, fl1, fl2]) { c.fill(f, "w"); c.edge(f, "W", "lower"); c.edge(f, "W", "upper"); }
c.fill(c.poly([[41, 38], [43, 38], [42, 46]]), "w"); c.fill(c.poly([[57, 38], [59, 38], [58, 43]]), "w");
// 二又の舌
const tg = c.strip([[60, 47, 3.4], [44, 47, 2.8], [28, 47, 2.2], [17, 48, 1.8]]); c.fill(tg, "t"); c.edge(tg, "r", "lower");
c.line(17, 47, 6, 39, "t", 2); c.line(17, 49, 6, 57, "t", 2); c.put(5, 38, "t"); c.put(5, 58, "t"); c.put(4, 39, "t"); c.put(4, 57, "t");
// 額の冠のひれ
const crown = [];
const bases = [[66, 14], [73, 15], [80, 18], [86, 23], [91, 29]];
const tips = [[57, 0], [68, 0], [83, 1], [97, 9], [105, 22]];
bases.forEach((b, i) => { const t = tips[i], nx = -(t[1] - b[1]), ny = t[0] - b[0], l = Math.hypot(nx, ny), w = 4.4; crown.push(c.poly([[b[0] - nx / l * w, b[1] - ny / l * w], [t[0], t[1]], [b[0] + nx / l * w, b[1] + ny / l * w], [b[0] + 2, b[1] + 8]])); });
const crownM = c.union(...crown);
const under = c.sub(crownM, upper);
c.paint(under, FIN, { round: 5, flat: 0.05, bias: 0.3 }); c.edge(under, "k"); c.rim(under, { l: "m", k: "l" });
for (const t of tips) c.put(t[0], Math.max(1, t[1] + 1), "m");
// ---------- 輪郭 ----------
c.outline("o", { a: "o", b: "a", c: "a", d: "b", e: "b", f: "c", g: "a", h: "a", i: "b", j: "b", k: "o", l: "k", m: "l", r: "R", R: "o", t: "r", w: "W", W: "a", y: "o", Y: "y" });
c.despeckle("wYyWE");
// ---------- 霧（点描でぼかす）----------
const sil = c.M(); for (let y = 0; y < 192; y++) for (let x = 0; x < 192; x++) if (c.g[y][x] !== "." && c.g[y][x] !== "s") sil[y * 192 + x] = 1;
const bay = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]];
let cur = sil; const rings = [];
for (let k = 1; k <= 9; k++) { const g = c.grow(cur); const ring = c.M(); for (let i = 0; i < ring.length; i++) if (g[i] && !cur[i]) ring[i] = 1; rings.push(ring); cur = g; }
rings.forEach((ring, k) => { const dens = [0.5, 0.42, 0.34, 0.26, 0.2, 0.15, 0.1, 0.06, 0.03][k]; for (let y = 0; y < 192; y++) for (let x = 0; x < 192; x++) if (ring[y * 192 + x] && c.g[y][x] === "." && bay[y & 3][x & 3] / 16 < dens) c.g[y][x] = k < 4 ? "m" : "m"; });
// 地面をはう霧
for (let y = 170; y < 190; y++) for (let x = 0; x < 192; x++) { const d = ((x - 96) / 100) ** 2 + ((y - 182) / 10) ** 2; if (c.g[y][x] === "." && d < 1 && bay[(y * 3) & 3][(x + y) & 3] / 16 < 0.32 * (1 - d) + 0.04 && ((x >> 1) + (y >> 1)) % 3 !== 0) c.g[y][x] = (x + y) % 5 === 0 ? "n" : "m"; }
for (const [x, y] of [[20, 20], [12, 62], [8, 100], [176, 60], [182, 96], [40, 8], [110, 30], [124, 70], [24, 130], [168, 176]]) for (const [dx, dy] of [[0, 0], [2, 1], [-2, 1], [1, -2], [4, 0]]) if (c.get(x + dx, y + dy) === ".") c.put(x + dx, y + dy, "n");
export const rows = c.rows();
