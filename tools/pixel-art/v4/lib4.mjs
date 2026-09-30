// v4: 32×32のドット絵を「2.5頭身のキャラクター」を中心に、大量に作るための共通部品。
// 1つの絵 = 1つのモジュール（.mjs）。export するもの: name（日本語の名前）, category, pal（文字→色）, rows（32行×32文字）。
// 人物は charBase() で2.5頭身の骨組みを作り、髪・服・小物を上書きして描き分ける。目には必ず白いハイライト(w)を入れる。
export const W = 32;
export const blank = () => Array.from({ length: W }, () => Array(W).fill("."));
export const toRows = (g) => g.map((r) => r.join(""));
/** 左半分（16列）を鏡写しにして32列にする。 */
export function mirror(half) { return half.map((r, i) => { if (r.length !== 16) console.log(`左半分の長さが違う行 ${i}: ${r.length}`); const l = r.padEnd(16, ".").slice(0, 16); return l + [...l].reverse().join(""); }); }
/** [x, y, 文字] の一覧で上書きする。 */
export function overrides(rows, list) { const g = rows.map((r) => [...r]); for (const [x, y, ch] of list) if (x >= 0 && x < W && y >= 0 && y < W) g[y][x] = ch; return g.map((r) => r.join("")); }
/** 長方形・線などの上書き用の点を作る。 */
export const rect = (x0, y0, x1, y1, c) => { const o = []; for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) o.push([x, y, c]); return o; };
export const hline = (x0, x1, y, c) => rect(x0, y, x1, y, c);
export const vline = (x, y0, y1, c) => rect(x, y0, x, y1, c);
/** 左右対称に点を置く（x は左側の座標。右側は 31-x）。 */
export const sym = (list) => list.flatMap(([x, y, c]) => [[x, y, c], [31 - x, y, c]]);

/** 人物の標準の色（文字→色）。絵ごとに pal で上書きする。 */
export const DEFAULT_PAL = {
  p: "#3a2222", "1": "#4a2a22", "2": "#7a4632", "3": "#a8683e", "4": "#d49a5a",          // 髪（暗→明）と髪の輪郭 p
  q: "#7a3f3a", a: "#c87a66", b: "#eaa588", c: "#f8cfae", d: "#fff0dc",                    // 肌（輪郭 q・影 a・中 b・明 c・光 d）
  e: "#2a1e3a", i: "#5a86d0", w: "#ffffff", n: "#a04a4a", B: "#f08a8a",                   // 目（暗・瞳・ハイライト）・口・ほお
  r: "#14204a", J: "#1e2c66", j: "#2f4a9a", k: "#4c74c8", K: "#86aef0", C: "#efe3c8",     // 服（輪郭 r・影 J・中 j・明 k・光 K）・えり C
  P: "#4a3a3a", Q: "#6e5646", s: "#221a1a", D: "#20142a",                                  // ズボン（影 P・明 Q）・くつ s・地面の影 D
  A: "#ffb830", X: "#ffe89a", S: "#3a8ac8", W: "#8cc8f0", m: "#7a7a88", M: "#c4c4d4", y: "#bfae8e",   // 小物: 金 A・淡い金 X・青 S・水色 W・金属 m・明るい金属 M・生成り y
  g: "#4a8a3a", G: "#8ac860", u: "#7a30c0", U: "#c08cff", t: "#c03040", T: "#f07080", o: "#e07820", O: "#ffb060", // 緑 g・明るい緑 G・紫 u・明るい紫 U・赤 t・明るい赤 T・橙 o・明るい橙 O
};

/**
 * 2.5頭身の人物（正面）の骨組み。頭 y2〜12（11ドット）・胴 y13〜21・足 y22〜29 で、全体は約28ドット（頭÷全体≒0.4）。
 * opts.hair: 髪の高さの行数(既定5)  opts.sideHair: 横髪を y いくつまで伸ばすか(既定なし)  opts.fringe: "straight"|"spiky"|"side"
 * opts.skirt: true でズボンの代わりにスカート  opts.tall: 未使用
 */
export function charBase(o = {}) {
  const g = blank(); const put = (x, y, c) => { if (x >= 0 && x < W && y >= 0 && y < W) g[y][x] = c; };
  const hw = { 2: 5, 3: 7, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 7, 12: 5 };
  const hairTop = o.hair ?? 5;   // y2 から何行が髪か
  for (let y = 2; y <= 12; y++) for (let x = 16 - hw[y]; x <= 15 + hw[y]; x++) {
    const edge = x === 16 - hw[y] || x === 15 + hw[y] || y === 2 || y === 12;
    const inHair = y < 2 + hairTop || (o.sideHair && y <= o.sideHair && (x < 16 - hw[y] + 2 || x > 15 + hw[y] - 2));
    let c;
    if (inHair) c = edge ? "p" : y <= 3 ? (x >= 12 && x <= 19 ? "4" : "3") : y === 4 ? (x < 16 ? "3" : "3") : y === 5 ? "2" : "2";
    else c = edge ? (y === 12 ? "q" : "q") : (x >= 21 || y >= 11) ? "b" : "c";
    if (!edge && inHair && y === 2 + hairTop - 1) c = (x + y) % 2 ? "1" : "2";        // 前髪の下端のなじませ
    put(x, y, c);
  }
  // 前髪の形
  const fr = o.fringe ?? "straight";
  if (fr === "spiky") for (const x of [10, 13, 16, 19, 22]) { put(x, 2 + hairTop, "2"); put(x, 3 + hairTop - 0, "c"); }
  if (fr === "side") for (let x = 9; x <= 17; x++) put(x, 2 + hairTop, "2");
  // 目（左 x11〜13・右 x18〜20、y7〜9）。ハイライト w は左上
  for (const x0 of [11, 18]) {
    put(x0, 7, "e"); put(x0 + 1, 7, "e"); put(x0 + 2, 7, "e");
    put(x0, 8, "w"); put(x0 + 1, 8, "i"); put(x0 + 2, 8, "e");
    put(x0, 9, "i"); put(x0 + 1, 9, "i"); put(x0 + 2, 9, "e");
  }
  put(15, 11, "n"); put(16, 11, "n"); put(10, 10, "B"); put(21, 10, "B");
  // 胴
  const bw = { 13: 5, 14: 7, 15: 7, 16: 6, 17: 6, 18: 6, 19: 6, 20: 6, 21: 6 };
  for (let y = 13; y <= 21; y++) for (let x = 16 - bw[y]; x <= 15 + bw[y]; x++) {
    const edge = x === 16 - bw[y] || x === 15 + bw[y];
    put(x, y, edge ? "r" : (x >= 20 || y === 21) ? "J" : (x <= 12 && y <= 16) ? "k" : "j");
  }
  put(15, 13, "c"); put(16, 13, "c"); put(14, 13, "C"); put(17, 13, "C"); put(15, 14, "C"); put(16, 14, "C");    // えり（首・Vの襟）
  // 腕（胴の両脇）と手
  for (let y = 14; y <= 19; y++) for (const x of [8, 7, 23, 24]) put(x, y, (x === 7 || x === 24) ? "r" : x === 8 ? "j" : "J");
  for (const x of [7, 8, 23, 24]) { put(x, 20, "c"); put(x, 21, x === 7 || x === 24 ? "b" : "c"); }
  // 足
  for (let y = 22; y <= 27; y++) { for (const x of [11, 12, 13, 14]) put(x, y, x === 11 ? "Q" : "P"); for (const x of [17, 18, 19, 20]) put(x, y, x === 17 ? "Q" : "P"); }
  for (const x of [10, 11, 12, 13, 14]) { put(x, 28, "s"); put(x, 29, "s"); } for (const x of [17, 18, 19, 20, 21]) { put(x, 28, "s"); put(x, 29, "s"); }
  if (o.skirt) for (let y = 22; y <= 25; y++) for (let x = 9; x <= 22; x++) put(x, y, y === 22 ? "k" : y === 23 ? "j" : "J");
  for (let x = 9; x <= 22; x++) put(x, 30, "D");
  return toRows(g);
}

// ---- 小物（アイテム）用の描画部品（k- 系の絵が使う。追記のみ） ----
export const kNew = () => blank();
export const kPut = (g, x, y, c) => { if (x >= 0 && x < W && y >= 0 && y < W) g[y][x] = c; };
/** 長方形を塗る */
export const kRect = (g, x0, y0, x1, y1, c) => { for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) kPut(g, x, y, c); };
/** 線（1ドット幅） */
export function kLine(g, x0, y0, x1, y1, c) { const n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0), 1); for (let i = 0; i <= n; i++) kPut(g, Math.round(x0 + ((x1 - x0) * i) / n), Math.round(y0 + ((y1 - y0) * i) / n), c); }
/** 楕円を塗る。ramp は明→暗の色の並び（文字の配列）。光は左上。ramp が1つなら単色。 */
export function kEll(g, cx, cy, rx, ry, ramp) {
  const r = Array.isArray(ramp) ? ramp : [ramp];
  for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) {
    const dx = (x - cx) / rx, dy = (y - cy) / ry; if (dx * dx + dy * dy > 1) continue;
    const t = Math.max(0, Math.min(0.999, (dx * 0.55 + dy * 0.55 + 0.75) / 1.5)); kPut(g, x, y, r[Math.floor(t * r.length)]);
  }
}
/** 多角形（点 [x,y] の並び）を塗る */
export function kPoly(g, pts, c) {
  const ys = pts.map((p) => p[1]); const y0 = Math.ceil(Math.min(...ys)), y1 = Math.floor(Math.max(...ys));
  for (let y = y0; y <= y1; y++) { const xs = []; for (let i = 0; i < pts.length; i++) { const [ax, ay] = pts[i], [bx, by] = pts[(i + 1) % pts.length]; if ((ay <= y && by > y) || (by <= y && ay > y)) xs.push(ax + ((y + 0.5 - ay) * (bx - ax)) / (by - ay)); }
    xs.sort((a, b) => a - b); for (let i = 0; i + 1 < xs.length; i += 2) for (let x = Math.round(xs[i]); x < Math.round(xs[i + 1]); x++) kPut(g, x, y, c); }
}
/** 縁取り: 透明のマスで、上下左右のどれかが絵になっているものを、隣の色に応じた暗い色にする。map: {隣の文字: 縁の文字}, def: 既定 */
export function kOutline(g, map, def) {
  const o = g.map((r) => [...r]);
  for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) { if (g[y][x] !== ".") continue; let c = null;
    for (const [dx, dy] of [[0, 1], [1, 0], [-1, 0], [0, -1]]) { const nx = x + dx, ny = y + dy; if (nx < 0 || ny < 0 || nx >= W || ny >= W) continue; const n = g[ny][nx]; if (n !== "." && !c) c = map[n] ?? def; }
    if (c) o[y][x] = c; }
  return o;
}
export const kRows = (g) => g.map((r) => r.join(""));

// ---- 追記（担当C3）: 円・線・すそ広がりの服 ----
/** 中心(cx,cy)・半径rの塗りつぶした円（上書き用の点）。 */
export const disc = (cx, cy, r, c) => { const o = []; for (let y = Math.floor(cy - r); y <= Math.ceil(cy + r); y++) for (let x = Math.floor(cx - r); x <= Math.ceil(cx + r); x++) if ((x - cx) ** 2 + (y - cy) ** 2 <= r * r + 0.3) o.push([x, y, c]); return o; };
/** (x0,y0)から(x1,y1)への線（上書き用の点）。 */
export const line = (x0, y0, x1, y1, c) => { const o = []; const n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0)); for (let i = 0; i <= n; i++) o.push([Math.round(x0 + ((x1 - x0) * i) / (n || 1)), Math.round(y0 + ((y1 - y0) * i) / (n || 1)), c]); return o; };
/** 中央(15.5)から左右に広がる服（すそ）。y0の半幅w0からy1の半幅w1へ。edge=輪郭 l=明 m=中 d=影 hem=すその線（最下段）。 */
export const dress = (y0, y1, w0, w1, { edge = "r", l = "k", m = "j", d = "J", hem = null } = {}) => { const o = []; for (let y = y0; y <= y1; y++) { const w = Math.round(w0 + ((w1 - w0) * (y - y0)) / Math.max(1, y1 - y0)); for (let x = 16 - w; x <= 15 + w; x++) { const k = x - (16 - w), e = k === 0 || x === 15 + w; let c = e ? edge : k < Math.max(2, w * 0.5) ? l : k < w * 1.25 ? m : d; if (!e && hem && y === y1) c = hem; o.push([x, y, c]); } } return o; };

// ---- モンスター用の描画道具（M1 追記）。光は左上、面は暗→明の階調で塗る。 ----
const hx = (s) => [1, 3, 5].map((i) => parseInt(s.slice(i, i + 2), 16));
const toHex = (a) => "#" + a.map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
/** R("abcd", 暗色, 明色): 文字ごとに暗→明の色を割り当てた pal の断片を返す。 */
export function R(chars, dark, light, mid) { const a = hx(dark), b = hx(light), m = mid ? hx(mid) : null, n = chars.length; const o = {}; [...chars].forEach((c, i) => { const t = n === 1 ? 0 : i / (n - 1); if (m) { o[c] = t < 0.5 ? toHex(a.map((v, k) => v + (m[k] - v) * t * 2)) : toHex(m.map((v, k) => v + (b[k] - v) * (t - 0.5) * 2)); } else o[c] = toHex(a.map((v, k) => v + (b[k] - v) * t)); }); return o; }
export const rng = (seed) => { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; };
export class Cv {
  constructor() { this.g = blank(); }
  px(x, y, c) { x = Math.round(x); y = Math.round(y); if (x >= 0 && x < W && y >= 0 && y < W) this.g[y][x] = c; }
  list(l) { for (const [x, y, c] of l) this.px(x, y, c); return this; }
  /** pred(x,y) が真の場所を ramp（[0]=縁・[1..]=暗→明）で塗る。 */
  shape(pred, x0, y0, x1, y1, ramp, o = {}) {
    const inside = (x, y) => x >= x0 && x <= x1 && y >= y0 && y <= y1 && pred(x, y);
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, rx = (x1 - x0 + 1) / 2, ry = (y1 - y0 + 1) / 2, n = ramp.length - 1; const lx = o.lx ?? 0.4, ly = o.ly ?? 0.5;
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) { if (!inside(x, y)) continue;
      const edge = !inside(x - 1, y) || !inside(x + 1, y) || !inside(x, y - 1) || !inside(x, y + 1);
      if (edge && o.outline !== false) { this.px(x, y, ramp[0]); continue; }
      const t = 0.55 - lx * ((x - cx) / rx) - ly * ((y - cy) / ry) + (((x + y) & 1) && o.dither ? 0.07 : 0);
      this.px(x, y, ramp[1 + Math.max(0, Math.min(n - 1, Math.floor(t * n)))]); }
    return this; }
  ell(cx, cy, rx, ry, ramp, o = {}) { return this.shape((x, y) => ((x - cx) / (rx + 0.5)) ** 2 + ((y - cy) / (ry + 0.5)) ** 2 <= 1, Math.floor(cx - rx), Math.floor(cy - ry), Math.ceil(cx + rx), Math.ceil(cy + ry), ramp, o); }
  box(x0, y0, x1, y1, ramp, o = {}) { return this.shape(() => true, x0, y0, x1, y1, ramp, o); }
  poly(pts, ramp, o = {}) { const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]); const pred = (x, y) => { let c = false; for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) { const [xi, yi] = pts[i], [xj, yj] = pts[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };
    return this.shape(pred, Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys), ramp, o); }
  line(x0, y0, x1, y1, c, th = 1) { const n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0), 1); for (let i = 0; i <= n; i++) { const x = x0 + ((x1 - x0) * i) / n, y = y0 + ((y1 - y0) * i) / n; this.px(x, y, c); if (th > 1) { this.px(x + 1, y, c); } if (th > 2) this.px(x, y + 1, c); } return this; }
  /** 影（地面の暗い1行）。 */
  shadow(cx, y, hw, c) { for (let x = cx - hw; x <= cx + hw; x++) this.px(x, y, c); return this; }
  /** 目: (x,y) が左上。2×2 で左上が白いハイライト。 */
  eye(x, y, c, hi = "w") { this.px(x, y, hi); this.px(x + 1, y, c); this.px(x, y + 1, c); this.px(x + 1, y + 1, c); return this; }
  /** 何かが塗られた場所のすぐ外側（上下左右）を c で縁取る。 */
  outlineAround(c) { const o = []; for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) if (this.g[y][x] === "." && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => this.g[y + dy]?.[x + dx] && this.g[y + dy][x + dx] !== ".")) o.push([x, y]); for (const [x, y] of o) this.g[y][x] = c; return this; }
  /** 孤立した点（上下左右に同じ色が無い点）のうち、まわりに絵がある点をまわりの多数の色になじませる。w（ハイライト）は残す。 */
  despeckle(keep = "w") { const src = this.g.map((r) => [...r]); for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) { const ch = src[y][x]; if (ch === "." || keep.includes(ch)) continue; const nb = [[1, 0], [-1, 0], [0, 1], [0, -1]].map(([dx, dy]) => src[y + dy]?.[x + dx]).filter((v) => v && v !== "."); if (nb.includes(ch) || nb.length < 2) continue; const cnt = {}; for (const v of nb) cnt[v] = (cnt[v] ?? 0) + 1; this.g[y][x] = Object.entries(cnt).sort((a, b) => b[1] - a[1])[0][0]; } return this; }
  rows() { this.despeckle(); return toRows(this.g); }
}

/** ASCII の小さな絵を (x, y) から貼る。空白は「そのまま」、"." は透明、ほかの文字はその色。 */
export function patch(rows, x, y, lines) { const g = rows.map((r) => [...r]); lines.forEach((ln, dy) => [...ln].forEach((ch, dx) => { const X = x + dx, Y = y + dy; if (ch !== " " && X >= 0 && X < W && Y >= 0 && Y < W) g[Y][X] = ch; })); return g.map((r) => r.join("")); }

// ---- 追記（担当O: マップ上の物用の描画道具）----
/** 32×32の絵を「点・長方形・線・楕円・多角形・陰影つきの塊・輪郭・落ち影」で描くための道具。 */
export function painter() {
  const g = blank();
  const put = (x, y, c) => { x = Math.round(x); y = Math.round(y); if (x >= 0 && x < W && y >= 0 && y < W) g[y][x] = c; };
  const get = (x, y) => (x >= 0 && x < W && y >= 0 && y < W ? g[y][x] : ".");
  const rect = (x0, y0, x1, y1, c) => { for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) put(x, y, c); };
  const line = (x0, y0, x1, y1, c) => { let dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1, e = dx + dy; for (;;) { put(x0, y0, c); if (x0 === x1 && y0 === y1) break; const e2 = 2 * e; if (e2 >= dy) { e += dy; x0 += sx; } if (e2 <= dx) { e += dx; y0 += sy; } } };
  const ell = (cx, cy, rx, ry, c) => { for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) if (((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1) put(x, y, c); };
  /** 楕円の塊。tones は暗→明の文字の並び。光は左上。 */
  const blob = (cx, cy, rx, ry, tones, bias = 0) => { const n = tones.length; for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) if (((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1) { const t = ((x - cx) / rx) * 0.55 + ((y - cy) / ry) * 0.75; const l = 0.5 - t / 2.4 + bias; put(x, y, tones[Math.max(0, Math.min(n - 1, Math.floor(l * n)))]); } };
  const poly = (pts, c) => { const ys = pts.map((p) => p[1]); const y0 = Math.floor(Math.min(...ys)), y1 = Math.ceil(Math.max(...ys)); for (let y = y0; y <= y1; y++) { const yy = y + 0.5, xs = []; for (let i = 0; i < pts.length; i++) { const [ax, ay] = pts[i], [bx, by] = pts[(i + 1) % pts.length]; if ((ay <= yy && by > yy) || (by <= yy && ay > yy)) xs.push(ax + ((yy - ay) / (by - ay)) * (bx - ax)); } xs.sort((a, b) => a - b); for (let i = 0; i + 1 < xs.length; i += 2) for (let x = Math.round(xs[i]); x < Math.round(xs[i + 1]); x++) put(x, y, c); } };
  /** すでに描いた物の外側に1ドットの縁を付ける。 */
  const outline = (c, diag = false) => { const l = []; const D = diag ? [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]] : [[1, 0], [-1, 0], [0, 1], [0, -1]]; for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) if (g[y][x] === "." && D.some(([a, b]) => get(x + a, y + b) !== ".")) l.push([x, y]); for (const [x, y] of l) g[y][x] = c; };
  /** 空いている所だけに落ち影の楕円を置く（輪郭のあとに呼ぶ）。 */
  const shadow = (cx, cy, rx, ry, c) => { for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) if (((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 && get(x, y) === ".") put(x, y, c); };
  const pts = (list, c) => list.forEach(([x, y]) => put(x, y, c));
  /** 上下左右に同じ色が無い孤立ドットを、まわりに2つ以上ある色へなじませる（protect の色は残す）。 */
  const despeckle = (protect = "") => { const ch = []; for (let y = 1; y < W - 1; y++) for (let x = 1; x < W - 1; x++) { const c = g[y][x]; if (c === "." || protect.includes(c)) continue; const nb = [g[y - 1][x], g[y + 1][x], g[y][x - 1], g[y][x + 1]]; if (nb.includes(c)) continue; const cnt = {}; for (const k of nb) if (k !== ".") cnt[k] = (cnt[k] || 0) + 1; const best = Object.entries(cnt).sort((a, b) => b[1] - a[1])[0]; if (best && best[1] >= 2) ch.push([x, y, best[0]]); } for (const [x, y, k] of ch) g[y][x] = k; };
  return { g, put, get, rect, line, ell, blob, poly, outline, shadow, pts, despeckle, rows: () => toRows(g) };
}
/** 孤立した1点（上下左右に同じ色が無い）を、まわりでいちばん多い色にならす。keep の文字（きらめきの白など）は残す。 */
export function kClean(rows, keep = "wWXs") {
  const g = rows.map((r) => [...r]);
  for (let y = 1; y < 31; y++) for (let x = 1; x < 31; x++) { const c = rows[y][x]; if (c === "." || keep.includes(c)) continue;
    const ns = [rows[y - 1][x], rows[y + 1][x], rows[y][x - 1], rows[y][x + 1]]; if (ns.includes(c)) continue;
    const cnt = {}; for (const n of ns) if (n !== ".") cnt[n] = (cnt[n] ?? 0) + 1; const best = Object.entries(cnt).sort((a, b) => b[1] - a[1])[0]; if (best && best[1] >= 2) g[y][x] = best[0]; }
  return g.map((r) => r.join(""));
}
/** 色の文字を別の文字にまとめる（色数を減らす用）。例: remap(rows, { A: "O", t: "T" }） */
export const remap = (rows, m) => rows.map((r) => [...r].map((c) => m[c] ?? c).join(""));
/** 孤立した1ドット（上下左右に同じ色が無い点）を、まわりでいちばん多い色にそろえる。keep に入れた文字（目のハイライトなど）は残す。 */
export const despeckle = (rows, keep = "w") => { const g = rows.map((r) => [...r]); for (let y = 1; y < W - 1; y++) for (let x = 1; x < W - 1; x++) { const c = rows[y][x]; if (c === "." || keep.includes(c)) continue; const n = [rows[y - 1][x], rows[y + 1][x], rows[y][x - 1], rows[y][x + 1]]; if (n.includes(c)) continue; const cnt = {}; for (const k of n) if (k !== ".") cnt[k] = (cnt[k] || 0) + 1; const best = Object.entries(cnt).sort((a, b) => b[1] - a[1])[0]; if (best) g[y][x] = best[0]; } return g.map((r) => r.join("")); };

/**
 * 人物の胴（y13〜30）を、横にせまくする（人間の指示 2026-09-30「胴が横に大きいので、少し細く」）。
 * 各行の左右の端の間を、factor 倍に縮める（中心はそのまま。最近傍で取るので、色は増えない）。人物（category "character"）にだけ、読み込み時にかける。
 */
export function slimBody(rows, factor = 0.8, fromY = 13) {
  const out = rows.map((r) => r);
  for (let y = fromY; y < rows.length; y++) {
    const r = rows[y]; let lo = r.length, hi = -1;
    for (let x = 0; x < r.length; x++) if (r[x] !== ".") { if (x < lo) lo = x; hi = x; }
    if (hi < 0) continue;
    const seg = r.slice(lo, hi + 1), w = seg.length, nw = Math.max(4, Math.round(w * factor));
    if (nw >= w) continue;
    const center = (lo + hi) / 2, start = Math.round(center - (nw - 1) / 2);
    let line = ".".repeat(r.length).split(""); for (let i = 0; i < nw; i++) line[start + i] = seg[Math.min(w - 1, Math.floor(((i + 0.5) * w) / nw))];
    out[y] = line.join("");
  }
  return out;
}
/**
 * 頭身を変える（人間の指示 2026-09-30「人物を全部2頭身で作ろう」。もとは2.5頭身）。
 * 頭の部分（y0〜12）を縦に伸ばし、体の部分（y13〜29）を縮めて、頭÷全体を 1/heads にする。最近傍で取るので、色は増えない。
 */
export function chibiHeads(rows, heads = 2) {
  if (heads >= 2.5) return rows;
  const total = 28, headH = Math.round(total / heads), bodyH = total - headH;    // 例: 2頭身 → 頭14・体14
  const out = rows.map((r) => r), srcHead = 13, srcBody = 17;
  for (let j = 0; j < headH + bodyH; j++) out[j] = j < headH ? rows[Math.min(srcHead - 1, Math.floor(((j + 0.5) * srcHead) / headH))] : rows[13 + Math.min(srcBody - 1, Math.floor(((j - headH + 0.5) * srcBody) / bodyH))];
  out[headH + bodyH] = rows[30];                                                  // 地面の影は、足の下に
  for (let j = headH + bodyH + 1; j < rows.length; j++) out[j] = ".".repeat(rows[0].length);
  return out;
}
export const CHAR_HEADS = 2;
/** 絵のモジュールから、実際に使う rows を取り出す（人物は、頭身を変えて、胴を細くする）。 */
export function pieceRows(m) {
  if (m.category !== "character") return m.rows;
  const chibi = chibiHeads(m.rows, CHAR_HEADS);
  return slimBody(chibi, 0.8, chibi === m.rows ? 13 : Math.round(28 / CHAR_HEADS) + 2);
}

/**
 * 仕上げ: 色数を max 色以内にまとめ（似た色へ寄せる。目のハイライト w は守る）、孤立した点を iso 個以内に減らす。
 * 使い方: export const rows = finish(r, pal);  （pal は絵ごとの上書き。DEFAULT_PAL は中で合わせる）
 */
export function finish(rows, pal = {}, max = 26, iso = 34) {
  const P = { ...DEFAULT_PAL, ...pal }; const g = rows.map((r) => [...r]);
  const rgb = (c) => { const h = P[c]; return [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16)); };
  const dist = (a, b) => { const x = rgb(a), y = rgb(b); const rm = (x[0] + y[0]) / 2; return Math.sqrt((2 + rm / 256) * (x[0] - y[0]) ** 2 + 4 * (x[1] - y[1]) ** 2 + (2 + (255 - rm) / 256) * (x[2] - y[2]) ** 2); };
  const keep = new Set(["w"]);
  for (;;) {
    const cnt = {}; for (const r of g) for (const c of r) if (c !== ".") cnt[c] = (cnt[c] || 0) + 1; const cs = Object.keys(cnt); if (cs.length <= max) break;
    let best = null; for (const a of cs) { if (keep.has(a)) continue; for (const b of cs) { if (a === b) continue; const cost = cnt[a] * dist(a, b) + (a === "e" || a === "i" ? 9999 : 0); if (!best || cost < best.cost) best = { a, b, cost }; } }
    for (const r of g) for (let x = 0; x < W; x++) if (r[x] === best.a) r[x] = best.b;
  }
  const prot = new Set(["w", "e", "i", "n", "B", "A", "X"]);
  for (let pass = 0; pass < 6; pass++) {
    const list = []; for (let y = 1; y < 31; y++) for (let x = 1; x < 31; x++) { const c = g[y][x]; if (c === "." || g[y - 1][x] === c || g[y + 1][x] === c || g[y][x - 1] === c || g[y][x + 1] === c) continue; list.push([x, y, c]); }
    if (list.length <= iso) break;
    const cand = list.filter(([, , c]) => !prot.has(c)).map(([x, y, c]) => { const ns = [g[y - 1][x], g[y + 1][x], g[y][x - 1], g[y][x + 1]].filter((n) => n !== "."); const m = {}; ns.forEach((n) => (m[n] = (m[n] || 0) + 1)); const t = Object.keys(m).sort((a, b) => m[b] - m[a])[0]; return { x, y, t, d: t ? dist(c, t) : 1e9 }; }).filter((o) => o.t).sort((a, b) => a.d - b.d);
    for (const o of cand.slice(0, list.length - iso)) g[o.y][o.x] = o.t;
  }
  return g.map((r) => r.join(""));
}
