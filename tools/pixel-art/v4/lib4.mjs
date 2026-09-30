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
  const ys = pts.map((p) => p[1]); const y0 = Math.min(...ys), y1 = Math.max(...ys);
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
