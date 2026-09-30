// v2: 地形タイル7点（128x128、上下左右に回り込んでつながる）。自作のみ。既存の terrain.mjs・ぴぽやには依存しない。
// ノイズはすべて128周期（wrap）。端が反対側とつながる。
import { hash, clamp, smoothstep } from "./lib2.mjs";
const N = 128;
const grid = (v = 0) => Array.from({ length: N }, () => Array(N).fill(v));
const wr = (v) => ((v % N) + N) % N;
const H3 = (a, b, s) => hash(a * 31 + s * 977, b * 17 + s * 131);
/** 回り込む値ノイズ。格子の大きさは横cx・縦cy（128の約数）。 */
function pn(x, y, cx, cy, s) {
  const nx = N / cx, ny = N / cy, fx = x / cx, fy = y / cy;
  const ix = Math.floor(fx), iy = Math.floor(fy), tx = smoothstep(0, 1, fx - ix), ty = smoothstep(0, 1, fy - iy);
  const v = (i, j) => H3(((i % nx) + nx) % nx, ((j % ny) + ny) % ny, s);
  const a = v(ix, iy) * (1 - tx) + v(ix + 1, iy) * tx, b = v(ix, iy + 1) * (1 - tx) + v(ix + 1, iy + 1) * tx;
  return a * (1 - ty) + b * ty;
}
/** 角ばった粒のノイズ（cドットの粒）。位置を波打たせて格子のクセを消す。 */
function grain(x, y, c, s, warp = 3) {
  const wx = (pn(x, y, 16, 16, s + 50) - 0.5) * 2 * warp, wy = (pn(x, y, 16, 16, s + 60) - 0.5) * 2 * warp;
  const n = N / c;
  return H3(Math.floor(wr(x + wx) / c) % n, Math.floor(wr(y + wy) / c) % n, s);
}
/** 値を順位で段に分ける（fracs = 各段の割合、暗→明）。色の使用量を狙い通りにする。 */
function quantize(vals, fracs) {
  const flat = vals.flat().slice().sort((a, b) => a - b), tot = fracs.reduce((a, b) => a + b, 0);
  let acc = 0; const th = fracs.slice(0, -1).map((f) => { acc += f; return flat[Math.min(flat.length - 1, Math.floor((acc / tot) * flat.length))]; });
  return vals.map((row) => row.map((v) => { let k = 0; while (k < th.length && v >= th[k]) k++; return k; }));
}
const field = (f) => Array.from({ length: N }, (_, y) => Array.from({ length: N }, (_, x) => f(x, y)));
const put = (g, x, y, k) => { g[wr(y)][wr(x)] = k; };
/** 孤立ドット（上下左右に同じ色なし）を、多い隣の色に置き換える（回り込み対応）。 */
function despeckle(g, passes = 2) {
  for (let p = 0; p < passes; p++) {
    const src = g.map((r) => r.slice());
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const k = src[y][x], nb = [src[wr(y - 1)][x], src[wr(y + 1)][x], src[y][wr(x - 1)], src[y][wr(x + 1)]];
      if (nb.includes(k)) continue;
      const cnt = {}; nb.forEach((c) => (cnt[c] = (cnt[c] || 0) + 1));
      g[y][x] = +Object.entries(cnt).sort((a, b) => b[1] - a[1])[0][0];
    }
  }
  return g;
}
const scatter = (n, s, minD = 9) => { // 回り込む距離で離した点
  const pts = []; let i = 0;
  while (pts.length < n && i < 4000) {
    const x = Math.floor(H3(i, 1, s) * N), y = Math.floor(H3(i, 2, s) * N); i++;
    if (pts.every(([a, b]) => { const dx = Math.min(Math.abs(a - x), N - Math.abs(a - x)), dy = Math.min(Math.abs(b - y), N - Math.abs(b - y)); return dx * dx + dy * dy >= minD * minD; })) pts.push([x, y]);
  }
  return pts;
};

// ---- 草 ----
const GRASS_PAL = [["草1", "#3f6132"], ["草2", "#4a7137"], ["草3", "#578040"], ["草4", "#658e49"], ["草5", "#76a054"], ["草の影", "#365329"]];
function grassBase(s) {
  const v = field((x, y) => 0.14 * pn(x, y, 64, 64, s) + 0.26 * pn(x, y, 16, 16, s + 1) + 0.2 * pn(x, y, 8, 8, s + 3) + 0.4 * grain(x, y, 4, s + 2, 4));
  const g = quantize(v, [14, 34, 30, 16, 6]);
  // 草の房（V字の小さな明るい葉）
  for (const [x, y] of scatter(70, s + 7, 7)) {
    put(g, x, y, 3); put(g, x + 2, y, 3); put(g, x + 1, y + 1, 4); put(g, x + 1, y + 2, 5);
  }
  return g;
}
function grassA() { return despeckle(grassBase(11)); }
function grassB() {
  const g = despeckle(grassBase(11));
  // 花（小さな十字。白と黄）
  scatter(16, 21, 17).forEach(([x, y], i) => {
    const pet = i % 3 === 2 ? 7 : 6;
    put(g, x, y, 8); put(g, x - 1, y, pet); put(g, x + 1, y, pet); put(g, x, y - 1, pet); put(g, x, y + 1, pet);
  });
  // 小石（灰色の楕円。下が暗い）
  scatter(9, 33, 14).forEach(([x, y]) => {
    put(g, x, y, 9); put(g, x + 1, y, 9); put(g, x + 2, y, 9); put(g, x - 1, y + 1, 10); put(g, x, y + 1, 9); put(g, x + 1, y + 1, 10); put(g, x + 2, y + 1, 10); put(g, x + 3, y + 1, 10);
  });
  return g;
}
const GRASS_B_PAL = [...GRASS_PAL, ["花の白", "#e8e4d2"], ["花の薄桃", "#d68f9c"], ["花の芯", "#e2b93a"], ["石", "#948f86"], ["石の影", "#6a655f"]];
// put番号: 6=白 7=薄桃 8=芯 9=石 10=石の影

// ---- 土の道 ----
const DIRT_PAL = [["土1", "#6b5238"], ["土2", "#7a5e42"], ["土3", "#896d4d"], ["土4", "#987c58"], ["土5", "#a88b64"], ["土の影", "#5a4530"], ["土の石", "#a19684"], ["石の影", "#75695c"]];
function dirt() {
  const v = field((x, y) => 0.3 * pn(x, y, 64, 64, 41) + 0.32 * pn(x, y, 16, 16, 42) + 0.38 * grain(x, y, 4, 43, 4));
  const g = quantize(v, [10, 28, 32, 22, 8]);
  // 轍のような横長のかすれ（暗い筋）
  scatter(12, 47, 16).forEach(([x, y]) => { const l = 5 + Math.floor(H3(x, y, 3) * 6); for (let i = 0; i < l; i++) put(g, x + i, y + (i > l / 2 ? 1 : 0), 5); });
  scatter(12, 51, 16).forEach(([x, y]) => { for (let i = 0; i < 4; i++) put(g, x + i, y, 4); });
  scatter(6, 55, 20).forEach(([x, y]) => { put(g, x, y, 6); put(g, x + 1, y, 6); put(g, x, y + 1, 7); put(g, x + 1, y + 1, 7); put(g, x + 2, y + 1, 7); });
  return despeckle(g);
}

// ---- 水面 ----
const WATER_PAL = [["水1", "#2f5c7c"], ["水2", "#396c8c"], ["水3", "#467c9a"], ["水の光", "#7fb0c4"], ["水の白", "#a9cfdb"]];
function water() {
  const v = field((x, y) => 0.5 * pn(x, y, 32, 8, 61) + 0.35 * pn(x, y, 16, 4, 62) + 0.15 * pn(x, y, 32, 32, 63));
  const g = quantize(v, [30, 42, 28]);
  // 横長の光の線（2〜3本ずつ、少しずらして）
  for (const [x, y] of scatter(34, 71, 9)) { const l = 5 + Math.floor(H3(x, y, 9) * 8); for (let i = 0; i < l; i++) put(g, x + i, y, 3); if (H3(x, y, 4) > 0.5) for (let i = 2; i < l - 1; i++) put(g, x + i, y - 2, 3); }
  for (const [x, y] of scatter(12, 81, 14)) { const l = 3 + Math.floor(H3(x, y, 9) * 4); for (let i = 0; i < l; i++) put(g, x + i, y, 4); }
  const out = despeckle(g, 3);
  return out;
}

// ---- 深い森 ----
const FOREST_PAL = [["森の闇", "#2b3a1a"], ["森1", "#3a4a1c"], ["森2", "#4a5c22"], ["森3", "#5c6e2a"], ["森4", "#6f8232"], ["森5", "#849a3c"]];
function forest() {
  // 塊の中心（回り込むジッタ格子 8x8）。左上から光。
  const M = 6, C = N / M, pts = [];
  for (let j = 0; j < M; j++) for (let i = 0; i < M; i++) pts.push([(i + 0.5 + (H3(i, j, 91) - 0.5) * 0.55) * C, (j + 0.5 + (H3(i, j, 92) - 0.5) * 0.55) * C, 0.75 + H3(i, j, 93) * 0.6]);
  const v = field((x, y) => {
    let best = 9, second = 9, bd = null;
    for (const [px, py, sz] of pts) {
      let dx = Math.abs(px - x); dx = Math.min(dx, N - dx); let dy = Math.abs(py - y); dy = Math.min(dy, N - dy);
      if (dx > 36 || dy > 36) continue;
      const d = Math.hypot(dx, dy) / (15 * sz);
      if (d < best) { second = best; best = d; bd = [px - x, py - y]; } else if (d < second) second = d;
    }
    const inside = clamp(1 - best, 0, 1), lit = bd ? clamp(0.5 + (bd[0] + bd[1]) / 40, 0, 1) : 0.5; // 中心が左上側にあるほど明るい→ここでは点が右下にあると光が当たる
    const seam = clamp((second - best) * 2.2, 0, 1); // 塊の境は暗く
    return 0.18 + 0.4 * inside * (0.35 + 0.65 * (1 - lit)) + 0.1 * seam + 0.2 * grain(x, y, 3, 95, 3) + 0.16 * pn(x, y, 32, 32, 96) - 0.1;
  });
  const g = quantize(v, [10, 22, 28, 22, 13, 5]);
  return despeckle(g, 3);
}

// ---- 崖の壁 ----
const CLIFF_PAL = [["崖の影", "#4a3c44"], ["崖1", "#5f4e4b"], ["崖2", "#725f56"], ["崖3", "#85715f"], ["崖の明", "#a08a70"], ["割れ目", "#3b2f38"], ["崖の苔", "#5e6a45"]];
function cliff() {
  const g = grid(2);
  const bandH = [24, 30, 18, 26, 20, 10]; // 合計128
  let y0 = 0;
  bandH.forEach((bh, bi) => {
    // ブロックの幅（合計128）
    const ws = []; let sum = 0, i = 0;
    while (sum < N) { let w = 15 + Math.floor(H3(bi, i, 101) * 22); if (N - sum - w < 12) w = N - sum; ws.push(w); sum += w; i++; }
    const off = Math.floor(H3(bi, 7, 102) * N);
    let x0 = off;
    ws.forEach((bw, wi) => {
      const shade = Math.floor(H3(bi * 9 + wi, 3, 103) * 3); // 0..2 で塊ごとに明るさを少し変える
      const bseed = bi * 50 + wi;
      for (let yy = 0; yy < bh; yy++) for (let xx = 0; xx < bw; xx++) {
        const X = x0 + xx, Y = y0 + yy;
        let k = shade === 0 ? 1 : 2;
        const gr = grain(X, Y, 3, 110 + bseed, 2) + 0.5 * pn(X, Y, 16, 16, 120 + bseed);
        k = gr > 1.12 ? k + 1 : gr < 0.5 ? k - 1 : k;
        // 縦の傷（岩肌の縦筋）
        if (pn(X, Y, 4, 32, 130 + bseed) > 0.72) k -= 1;
        if (yy < 2) k = 4; else if (yy === 2) k = Math.max(k, 3); // 上縁：明るい
        if (yy >= bh - 2) k = 0; else if (yy === bh - 3) k = Math.min(k, 1); // 下縁：暗い
        if (xx === 0) k = 5; else if (xx === 1) k = Math.min(k, 1); // 左の割れ目
        if (xx === bw - 1) k = Math.max(0, Math.min(k, 1));
        put(g, X, Y, clamp(k, 0, 4) === k || k === 5 ? k : clamp(k, 0, 4));
      }
      x0 += bw;
    });
    y0 += bh;
  });
  // 苔を少し
  scatter(5, 141, 22).forEach(([x, y]) => { if (g[wr(y)][wr(x)] >= 2 && g[wr(y)][wr(x)] <= 3) { put(g, x, y, 6); put(g, x + 1, y, 6); put(g, x + 2, y, 6); put(g, x, y + 1, 6); put(g, x + 1, y + 1, 6); } });
  return despeckle(g);
}

// ---- 岸辺（上が草、下が水。境に湿った土。水の下側にも草の縁を作り、上下も回り込む）----
const SHORE_PAL = [
  ["草1", "#3f6132"], ["草2", "#4a7137"], ["草3", "#578040"], ["草4", "#658e49"], ["草の影", "#365329"],
  ["湿土1", "#4f4030"], ["湿土2", "#615039"], ["湿土3", "#75634a"],
  ["水1", "#2f5c7c"], ["水2", "#396c8c"], ["水3", "#467c9a"], ["水の光", "#7fb0c4"],
];
function shore() {
  const edge1 = (x) => 62 + (pn(x, 0, 32, 32, 151) - 0.5) * 16 + (pn(x, 0, 8, 8, 152) - 0.5) * 5; // 草と湿土の境
  const edge2 = (x) => 66 + (pn(x, 0, 32, 32, 153) - 0.5) * 14; // 湿土と水の境（岸の下）
  const lower = (x) => 112 + (pn(x, 0, 32, 32, 154) - 0.5) * 8; // 水と下の湿土の境
  const gv = field((x, y) => 0.4 * pn(x, y, 32, 32, 11) + 0.28 * pn(x, y, 16, 16, 12) + 0.32 * grain(x, y, 4, 13, 4));
  const gq = quantize(gv, [20, 35, 30, 15]);
  const wv = field((x, y) => 0.5 * pn(x, y, 32, 8, 161) + 0.35 * pn(x, y, 16, 4, 162) + 0.15 * pn(x, y, 32, 32, 163));
  const wq = quantize(wv, [34, 44, 22]);
  const wl = field((x, y) => pn(x, y, 32, 8, 171) * 0.7 + pn(x, y, 16, 4, 172) * 0.3);
  const wlq = quantize(wl, [92, 8]);
  const g = grid(0);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const e1 = edge1(x), e2 = e1 + 9 + (pn(x, 0, 16, 16, 155) - 0.5) * 5, e3 = lower(x), e4 = e3 + 8;
    let k;
    if (y < e1 - 0) k = gq[y][x]; // 上の草
    else if (y < e2) { const d = y - e1; k = (d < 2 ? 5 : d < 6 ? 6 : 7); if (grain(x, y, 3, 181, 2) > 0.8 && d < 6) k = 7; }
    else if (y < e3) { k = 8 + wq[y][x]; if (y - e2 < 3 && k !== 11) k = 8; }
    else if (y < e4) { const d = y - e3; k = d < 3 ? 7 : d < 6 ? 6 : 5; }
    else k = gq[y][x];
    g[y][x] = k;
  }
  // 湿土の縁に草の房を少し、草の房
  scatter(30, 197, 8).forEach(([x, y]) => { if ((y < 56 || y > 120 || y < 4) && g[wr(y)][x] <= 4) { put(g, x, y, 3); put(g, x + 2, y, 3); put(g, x + 1, y + 1, 3); put(g, x + 1, y + 2, 4); } });
  scatter(14, 88, 12).forEach(([x, y]) => { if (y > 80 && y < 106) { const l = 5 + Math.floor(H3(x, y, 9) * 6); for (let i = 0; i < l; i++) put(g, x + i, y, 11); } });
  return despeckle(g, 3);
}

export const PIECES = [
  { name: "T1-草地A", pal: GRASS_PAL, build: grassA },
  { name: "T7-草地B", pal: GRASS_B_PAL, build: grassB },
  { name: "T2-土の道", pal: DIRT_PAL, build: dirt },
  { name: "T3-水面", pal: WATER_PAL, build: water },
  { name: "T5-深い森", pal: FOREST_PAL, build: forest },
  { name: "T4-崖の壁", pal: CLIFF_PAL, build: cliff },
  { name: "T6-岸辺", pal: SHORE_PAL, build: shore },
];
