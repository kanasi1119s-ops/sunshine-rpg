// 256×256 のボス3体。ボスは「歪み」（歪んだ灯り石が生んだ巨体）で、章ごとに形と色を変えてある。
// 立体感は「楕円体の法線と光の向き（左上）の内積」で決めるので、丸みのある塊が自然に陰影づく。
// 既存作品のモンスターの姿・名前は参考にしていない（CLAUDE.md 1-1）。
import { hash, makeGrid, putNative } from "./lib.mjs";

const W = 256;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const px = (g, r, c, k) => putNative(g, Math.round(r), Math.round(c), k);
const LV = (() => { const v = [-0.55, -0.6, 0.58]; const n = Math.hypot(...v); return v.map((x) => x / n); })();
/** 楕円体の表面の明るさ（-1〜1）。 */
const lumOf = (nx, ny, d) => nx * LV[0] + ny * LV[1] + Math.sqrt(Math.max(0, 1 - d)) * LV[2];
/** 明るさから階調番号（0〜len-1）を決める。少しだけ揺らぎを混ぜる。 */
function toneIdx(len, lum, c, r, jit = 0.1) {
  let t = Math.floor(clamp((lum + 0.45) / 1.35 * len, 0, len - 0.001));
  if (hash(c, r) < jit) t += hash(r, c) < 0.5 ? -1 : 1;
  return clamp(t, 0, len - 1);
}
/** 楕円体を描く。fn(r,c,nx,ny,d,lum) が色番号か null（描かない）を返す。 */
function ell(g, cx, cy, rx, ry, fn) {
  for (let r = Math.floor(cy - ry); r <= Math.ceil(cy + ry); r++) for (let c = Math.floor(cx - rx); c <= Math.ceil(cx + rx); c++) {
    const nx = (c - cx) / rx, ny = (r - cy) / ry, d = nx * nx + ny * ny;
    if (d > 1) continue;
    const k = fn(r, c, nx, ny, d, lumOf(nx, ny, d));
    if (k !== null && k !== undefined) px(g, r, c, k);
  }
}
/** 回り込まない距離ノイズ（ひび割れ・セル模様用）。 */
function worley(x, y, cell, seed = 0) {
  const cx = Math.floor(x / cell), cy = Math.floor(y / cell);
  let d1 = 9, d2 = 9;
  for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
    const gx = cx + i, gy = cy + j;
    const ppx = (gx + hash(gx + seed, gy) * 0.8 + 0.1) * cell, ppy = (gy + hash(gy + 50 + seed, gx) * 0.8 + 0.1) * cell;
    const d = Math.hypot(ppx - x, ppy - y) / cell;
    if (d < d1) { d2 = d1; d1 = d; } else if (d < d2) d2 = d;
  }
  return [d1, d2];
}
/** 太さのある管（曲線に沿って円柱の陰影をつける）。 */
function tube(g, pts, rad, ramp, jit = 0.06) {
  for (let s = 0; s < pts.length - 1; s++) {
    const [x0, y0] = pts[s], [x1, y1] = pts[s + 1], n = Math.ceil(Math.hypot(x1 - x0, y1 - y0));
    for (let i = 0; i <= n; i++) {
      const cx = x0 + (x1 - x0) * i / n, cy = y0 + (y1 - y0) * i / n;
      ell(g, cx, cy, rad, rad, (r, c, nx, ny, d, lum) => (d > 0.86 ? 0 : ramp[toneIdx(ramp.length, lum, c, r, jit)]));
    }
  }
}
function curve(p0, p1, p2, steps = 24) { return Array.from({ length: steps + 1 }, (_, i) => { const t = i / steps; return [(1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]]; }); }
/** 歪みの結晶（ひし形の破片）。 */
function shard(g, cx, cy, w, h, ramp, edge) {
  for (let r = -h; r <= h; r++) for (let c = -w; c <= w; c++) {
    const d = Math.abs(c) / w + Math.abs(r) / h; if (d > 1) continue;
    let k = c < 0 ? (r < 0 ? ramp[2] : ramp[1]) : (r < 0 ? ramp[1] : ramp[0]);
    if (d > 0.86) k = edge; else if (c < 0 && r < 0 && d < 0.5) k = ramp[2];
    px(g, cy + r, cx + c, k);
  }
}
const shadowUnder = (g, cx, cy, rx, ry, k) => ell(g, cx, cy, rx, ry, (r, c, nx, ny, d) => (d < 0.55 || hash(c, r) < 0.75 ? k : null));

// ======== 1. 水涸れの歪み（第1章）: 干からびた粘土の巨体、割れ目に水がにじみ、逆流する渦がまとわりつく ========
// pal: 0縁 1-5粘土(暗→明) 6割れ目の暗 7-10水(暗→明) 11水の光 12-14歪み紫(暗中明) 15影 16目の光
const boss1 = () => {
  const g = makeGrid();
  const CL = [1, 2, 3, 4, 5], WT = [7, 8, 9, 10];
  shadowUnder(g, 128, 240, 100, 11, 15);
  const clay = (r, c, nx, ny, d, lum) => {
    const [d1, d2] = worley(c, r * 1.1, 24, 3);
    const edge = d2 - d1;
    if (edge < 0.05) return hash(c, r) < 0.85 ? 9 : 11;              // 割れ目の奥に水が光る
    if (edge < 0.10) return 6;                                        // 割れ目の縁は暗く
    let t = toneIdx(5, lum, c, r, 0.13);
    if (d1 > 0.62) t = Math.max(0, t - 1);                             // 乾いた板の中心は少し暗く
    if (hash(c >> 2, r >> 2) < 0.12) t = clamp(t + 1, 0, 4);
    return CL[t];
  };
  // 腕（後ろ）→ 胴 → 肩 → 頭
  ell(g, 36, 168, 27, 56, clay); ell(g, 220, 168, 27, 56, clay);
  ell(g, 30, 226, 24, 20, clay); ell(g, 226, 226, 24, 20, clay);
  ell(g, 128, 152, 86, 88, clay);
  ell(g, 54, 118, 36, 32, clay); ell(g, 202, 118, 36, 32, clay);
  ell(g, 128, 80, 46, 42, clay);
  // 逆流する水の渦（胴にまとわりつく螺旋）
  for (let r = 60; r < 240; r++) for (let c = 30; c < 226; c++) {
    const dx = c - 128, dy = (r - 158) * 1.05, rad = Math.hypot(dx, dy); if (rad > 84 || rad < 10) continue;
    const ang = Math.atan2(dy, dx), s = Math.sin(ang * 2 - rad * 0.11);
    if (s < 0.78) continue;
    const nx = dx / 90, ny = dy / 90, lum = lumOf(nx, ny, nx * nx + ny * ny);
    const t = s > 0.95 ? 3 : toneIdx(4, lum, c, r, 0.08);
    if (r < 230 && Math.hypot(c - 128, r - 152) <= 86.5) px(g, r, c, s > 0.97 ? 11 : WT[t]);
  }
  // 目と口（洞のような暗い穴に、水色の光）
  for (const ex of [111, 145]) { ell(g, ex, 80, 11, 8, (r, c, nx, ny, d) => (d > 0.5 ? 0 : 6)); ell(g, ex, 81, 6, 4, (r, c, nx, ny, d) => (d > 0.45 ? 10 : 16)); }
  for (let c = 104; c <= 152; c++) { const r = 104 + Math.round(Math.sin(c * 0.9) * 2.4); px(g, r, c, 0); px(g, r + 1, c, c % 3 === 0 ? 16 : 6); if (c % 5 === 0) { px(g, r + 2, c, 0); px(g, r + 3, c, 0); } }
  // したたる水（腕・手から）
  for (const [x, y0] of [[22, 244], [34, 246], [214, 244], [232, 246], [70, 230], [186, 232], [110, 236], [146, 236]]) for (let i = 0; i < 12; i++) px(g, y0 + i * 0.6, x, i > 9 ? 11 : WT[Math.min(3, 1 + (i > 4 ? 1 : 0) + (i > 8 ? 1 : 0))]);
  // 歪みの結晶（紫）が宙に浮かぶ
  for (const [x, y, w, h] of [[14, 58, 8, 16], [242, 64, 9, 18], [26, 22, 6, 12], [232, 26, 6, 12], [128, 10, 7, 14], [92, 30, 5, 9], [166, 32, 5, 9], [12, 130, 5, 10]]) shard(g, x, y, w, h, [12, 13, 14], 0);
  // 外周の縁取り
  const has = (r, c) => r >= 0 && r < W && c >= 0 && c < W && g[r][c] !== -1 && g[r][c] !== 15;
  const add = []; for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) if ((g[r][c] === -1 || g[r][c] === 15) && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(r + a, c + b))) add.push([r, c]);
  for (const [r, c] of add) g[r][c] = 0;
  return g;
};
const pal1 = [["縁", "#150c0e"], ["粘土1", "#4a2a1c"], ["粘土2", "#6e4128"], ["粘土3", "#95603a"], ["粘土4", "#bd8853"], ["粘土5", "#e2b47a"], ["割れ目", "#241009"], ["水1", "#0a3352"], ["水2", "#115a7a"], ["水3", "#2792a8"], ["水4", "#5cc8c8"], ["水の光", "#c4f4ee"], ["歪み暗", "#2a1450"], ["歪み", "#5b2fa0"], ["歪み明", "#a884f0"], ["影", "#1d2a1c"], ["目の光", "#f0fffa"]];

// ======== 2. 積荷の歪み（第2章）: 木箱と灯り石が崩れて混ざった巨体 ========
// pal: 0縁 1-5木(暗→明) 6金具暗 7金具明 8-11灯り石(暗→明) 12-14歪み紫(暗中明) 15影 16縄
const boss2 = () => {
  const g = makeGrid();
  const WD = [1, 2, 3, 4, 5], AM = [8, 9, 10, 11];
  shadowUnder(g, 128, 242, 104, 10, 15);
  function crate(x, y, w, h, seed, broken = false) {
    for (let r = y; r < y + h; r++) for (let c = x; c < x + w; c++) {
      const u = (c - x) / w, v = (r - y) / h;
      const plank = Math.floor((r - y) / 11), inP = (r - y) % 11;
      const lum = (-(u - 0.5) * 0.9 - (v - 0.5) * 0.9) * 0.6 + 0.1;
      let t = toneIdx(5, lum, c, r, 0.05);
      if (inP === 0) t = Math.max(0, t - 2); else if (inP === 10) t = Math.max(0, t - 1); else if (inP === 1) t = Math.min(4, t + 1);
      if (hash(plank + seed, 7) < 0.3) t = clamp(t - 1, 0, 4);                     // 板ごとの色の違い
      if (hash(Math.floor((c + plank * 13) / 9), plank + seed) < 0.05 && inP > 1) t = Math.max(0, t - 1);
      if ((c - x) < 5 || (c - x) >= w - 5 || (r - y) < 5 || (r - y) >= h - 5) t = clamp(((c - x) < 5 || (r - y) < 5 ? 4 : 1), 0, 4); // 枠
      px(g, r, c, WD[t]);
    }
    for (const [cx0, cy0] of [[x + 2, y + 2], [x + w - 4, y + 2], [x + 2, y + h - 4], [x + w - 4, y + h - 4]]) for (let i = 0; i < 9; i++) for (let j = 0; j < 9; j++) if (i < 3 || j < 3 || (i + j) < 2) px(g, cy0 + (cy0 === y + 2 ? j : -j + 2), cx0 + (cx0 === x + 2 ? i : -i + 2), i === 0 || j === 0 ? 7 : 6);
    for (const [nx2, ny2] of [[x + 8, y + 8], [x + w - 9, y + 8], [x + 8, y + h - 9], [x + w - 9, y + h - 9]]) { px(g, ny2, nx2, 7); px(g, ny2 + 1, nx2, 6); }
    // 縁取り
    for (let c = x; c < x + w; c++) { px(g, y, c, 0); px(g, y + h - 1, c, 0); }
    for (let r = y; r < y + h; r++) { px(g, r, x, 0); px(g, r, x + w - 1, 0); }
    if (broken) { // 板が割れて灯り石が見える
      const bx = x + w * 0.3, by = y + h * 0.35;
      for (let r = 0; r < h * 0.4; r++) for (let c = 0; c < w * 0.4; c++) { const dd = (c - w * 0.2) ** 2 / (w * 0.2) ** 2 + (r - h * 0.2) ** 2 / (h * 0.2) ** 2; if (dd < 1) px(g, by + r, bx + c, dd < 0.25 ? 11 : dd < 0.55 ? 10 : 9); }
    }
  }
  // 灯り石の結晶（六角の柱。琥珀色に光る）
  function stone(cx, cy, w, h) {
    for (let r = -h; r <= h; r++) for (let c = -w; c <= w; c++) {
      const top = r < -h * 0.4, edge = Math.abs(c) / w;
      const inside = top ? Math.abs(c) <= w * (1 - (-h * 0.4 - r) / (h * 0.6) * 0.6) : true; if (!inside) continue;
      let k = c < -w * 0.3 ? 10 : c < w * 0.35 ? 11 : 9; if (top) k = r < -h * 0.85 ? 11 : 10; if (edge > 0.88 || r === h) k = 8; if (hash(c, r) < 0.05) k = 11;
      px(g, cy + r, cx + c, k);
    }
  }
  // 後ろの箱 → 前の箱（下から積み上がる）
  crate(6, 118, 44, 100, 1); crate(206, 112, 44, 106, 2, true);                       // 腕の箱
  crate(30, 168, 92, 76, 3); crate(120, 172, 100, 72, 4, true); crate(88, 150, 84, 46, 5);   // 下段
  crate(48, 100, 82, 70, 6, true); crate(128, 94, 84, 74, 7);                                 // 中段
  crate(88, 26, 80, 72, 8);                                                                   // 頭の箱
  // 隙間からもれる灯り石
  for (const [x, y, w, h] of [[80, 140, 9, 15], [170, 150, 8, 14], [128, 168, 10, 18], [58, 206, 8, 12], [196, 210, 9, 13], [128, 90, 7, 11]]) stone(x, y, w, h);
  // 目（灯り石）と口（割れた板）
  for (const ex of [108, 148]) { for (let r = 46; r < 60; r++) for (let c = ex - 9; c < ex + 9; c++) { const dd = (c - ex) ** 2 / 81 + (r - 53) ** 2 / 49; if (dd < 1) px(g, r, c, dd < 0.2 ? 11 : dd < 0.5 ? 10 : dd < 0.8 ? 9 : 0); } }
  for (let c = 102; c <= 156; c++) { const r = 76 + Math.round(Math.abs(Math.sin((c - 102) * 0.5)) * 5); px(g, r, c, 0); px(g, r + 1, c, c % 4 === 0 ? 11 : 8); px(g, r + 2, c, 0); }
  // 縄と鎖（斜めに巻く）
  for (let i = 0; i < 200; i++) { const c = 36 + i * 0.86, r = 110 + i * 0.5 + Math.sin(i / 6) * 2; px(g, r, c, 16); px(g, r + 1, c, i % 6 < 3 ? 16 : 1); }
  // 歪みのもや（外周の紫）と結晶
  const has = (r, c) => r >= 0 && r < W && c >= 0 && c < W && g[r][c] !== -1 && g[r][c] !== 15;
  const haze = []; for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) { if (g[r][c] === -1 || g[r][c] === 15) { for (let d = 1; d <= 7; d++) { if ([[d, 0], [-d, 0], [0, d], [0, -d]].some(([a, b]) => has(r + a, c + b))) { if (hash(c, r) < 0.42 - d * 0.05) haze.push([r, c, d < 3 ? 13 : 12]); break; } } } }
  for (const [r, c, k] of haze) g[r][c] = k;
  for (const [x, y, w, h] of [[16, 40, 7, 15], [238, 44, 8, 17], [30, 82, 5, 10], [226, 90, 5, 10], [128, 8, 6, 12]]) shard(g, x, y, w, h, [12, 13, 14], 0);
  const add = []; for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) if ((g[r][c] === -1 || g[r][c] === 15) && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => { const rr = r + a, cc = c + b; return rr >= 0 && rr < W && cc >= 0 && cc < W && g[rr][cc] !== -1 && g[rr][cc] !== 15 && g[rr][cc] !== 12 && g[rr][cc] !== 13; })) add.push([r, c]);
  for (const [r, c] of add) g[r][c] = 0;
  return g;
};
const pal2 = [["縁", "#160c08"], ["木1", "#3a2210"], ["木2", "#5e3a1c"], ["木3", "#855628"], ["木4", "#ab7a3c"], ["木5", "#d2a05a"], ["金具暗", "#3a3a44"], ["金具明", "#9a9aa8"], ["灯り石1", "#8a4a10"], ["灯り石2", "#d88a1c"], ["灯り石3", "#ffc94a"], ["灯り石4", "#fff4b0"], ["歪み暗", "#2a1450"], ["歪み", "#5b2fa0"], ["歪み明", "#a884f0"], ["影", "#1d2a1c"], ["縄", "#c8b078"]];

// ======== 3. 実験の歪み（第3章）: 実験装置が暴走した機械の巨体。中心の灯り石の核が光る ========
// pal: 0縁 1-6鋼(暗→明) 7-10真鍮(暗→明) 11-15光(暗→白) 16-18歪み紫 19影 20蒸気
const boss3 = () => {
  const g = makeGrid();
  const ST = [1, 2, 3, 4, 5, 6], BR = [7, 8, 9, 10], GL = [11, 12, 13, 14, 15];
  shadowUnder(g, 128, 244, 108, 9, 19);
  // 土台（重い板と脚）
  const plate = (x, y, w, h) => { for (let r = y; r < y + h; r++) for (let c = x; c < x + w; c++) { const lum = -((c - x) / w - 0.5) * 0.6 - ((r - y) / h - 0.5) * 1.2 + 0.1; let t = toneIdx(6, lum, c, r, 0.05); if (r === y) t = 5; if (r === y + h - 1) t = 0; px(g, r, c, ST[t]); } for (let i = 0; i < w / 14; i++) { px(g, y + 5, x + 8 + i * 14, 5); px(g, y + 6, x + 8 + i * 14, 1); } };
  plate(24, 216, 208, 26); plate(52, 200, 152, 18);
  // 脚（ピストン）
  for (const x of [58, 198]) { tube(g, [[x, 150], [x, 205]], 11, ST); for (let r = 158; r < 200; r += 8) for (let c = x - 12; c <= x + 12; c++) px(g, r, c, c < x - 4 ? 6 : c < x + 4 ? 4 : 2); }
  // 歯車（左右と上）
  function gear(cx, cy, R, teeth, spin) {
    for (let r = Math.floor(cy - R * 1.15); r <= cy + R * 1.15; r++) for (let c = Math.floor(cx - R * 1.15); c <= cx + R * 1.15; c++) {
      const dx = c - cx, dy = r - cy, rad = Math.hypot(dx, dy), ang = Math.atan2(dy, dx) + spin;
      const outer = R * (Math.sin(teeth * ang) > 0.1 ? 1.0 : 0.86); if (rad > outer) continue;
      const lum = (-dx * 0.55 - dy * 0.65) / R * 0.7 + 0.15;
      let t = toneIdx(6, lum, c, r, 0.05);
      if (rad > outer - 3) t = Math.max(0, t - 2);                                     // 歯の縁
      else if (Math.abs(rad - R * 0.62) < 2) t = Math.max(0, t - 2);                   // 溝
      else if (rad < R * 0.28) t = clamp(t + (rad < R * 0.12 ? -2 : 1), 0, 5);         // 軸
      else if (rad < R * 0.62 && Math.sin(6 * ang) > 0.55) t = 0;                       // 肉抜きの穴
      px(g, r, c, ST[t]);
    }
  }
  gear(46, 118, 46, 12, 0.1); gear(210, 118, 46, 12, 0.35); gear(128, 46, 34, 10, 0.2);
  // 管（歯車と核をつなぐ）
  tube(g, curve([70, 150], [80, 200], [110, 196]), 7, BR);
  tube(g, curve([186, 150], [176, 200], [146, 196]), 7, BR);
  tube(g, curve([70, 84], [96, 66], [104, 96]), 6, ST);
  tube(g, curve([186, 84], [160, 66], [152, 96]), 6, ST);
  // 排気口と蒸気
  for (const x of [98, 158]) { for (let r = 172; r < 186; r++) for (let c = x - 9; c <= x + 9; c++) px(g, r, c, ST[c < x - 3 ? 4 : c < x + 3 ? 3 : 1]); for (let i = 0; i < 26; i++) { const ex = x + Math.sin(i * 0.7) * 5 + (x < 128 ? -1 : 1) * i * 0.3, ey = 170 - i * 3.6; ell(g, ex, ey, 6 + i * 0.35, 4 + i * 0.25, (r, c, nx, ny, d) => (hash(c, r) < 0.5 - d * 0.35 ? 20 : null)); } }
  // 核を囲む輪（後ろ半分）
  function ring(cx, cy, rx, ry, thick, front) {
    for (let a = 0; a < 6.283; a += 0.004) { const isFront = Math.sin(a) > 0; if (isFront !== front) continue; for (let t2 = -thick; t2 <= thick; t2 += 0.6) { const c = cx + (rx + t2) * Math.cos(a), r = cy + (ry + t2 * ry / rx) * Math.sin(a); const lum = -Math.cos(a) * 0.4 - Math.sin(a) * 0.3 - Math.abs(t2) / thick * 0.5 + 0.5; px(g, r, c, BR[clamp(Math.floor(lum * 4), 0, 3)]); } }
  }
  ring(128, 128, 62, 24, 5, false);
  // 核（灯り石。中心ほど白く光る）
  ell(g, 128, 128, 46, 46, (r, c, nx, ny, d, lum) => { if (d > 0.93) return 0; const t = d < 0.06 ? 4 : d < 0.22 ? 3 : d < 0.45 ? 2 : d < 0.7 ? 1 : 0; const tt = clamp(t + (hash(c, r) < 0.1 ? 1 : 0), 0, 4); return GL[tt]; });
  // 核を囲むかご（縦の枠）
  for (const a of [-0.9, -0.3, 0.3, 0.9]) for (let t = -1; t <= 1; t += 0.004) { const ang = t * 1.2; const x = 128 + Math.sin(a * 2.2) * 46 * Math.cos(ang) * 0 + Math.sin(ang) * 48 * Math.cos(a), y = 128 - Math.cos(ang) * 48; px(g, y, x, ST[a < 0 ? 4 : 2]); px(g, y, x + 1, ST[a < 0 ? 3 : 1]); }
  ring(128, 128, 62, 24, 5, true);
  // 稲妻状の歪み（紫）が核から走る
  for (const [ax, ay, bx, by] of [[128, 96, 168, 30], [128, 96, 90, 22], [170, 120, 240, 80], [86, 122, 14, 70], [128, 160, 200, 244], [128, 160, 54, 246]]) { let x = ax, y = ay; const n = 34; for (let i = 0; i < n; i++) { x += (bx - x) / (n - i) + (hash(i, ax) - 0.5) * 8; y += (by - y) / (n - i) + (hash(i, ay) - 0.5) * 5; px(g, y, x, 17); px(g, y, x + 1, 18); if (i % 4 === 0) px(g, y - 1, x - 1, 16); } }
  for (const [x, y, w, h] of [[14, 40, 7, 15], [240, 40, 8, 16], [14, 190, 6, 12], [242, 190, 7, 13]]) shard(g, x, y, w, h, [16, 17, 18], 0);
  const has = (r, c) => r >= 0 && r < W && c >= 0 && c < W && g[r][c] !== -1 && g[r][c] !== 19 && g[r][c] !== 20;
  const add = []; for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) if ((g[r][c] === -1 || g[r][c] === 19) && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(r + a, c + b))) add.push([r, c]);
  for (const [r, c] of add) g[r][c] = 0;
  return g;
};
const pal3 = [["縁", "#0c1018"], ["鋼1", "#1e2632"], ["鋼2", "#323f52"], ["鋼3", "#4c5e78"], ["鋼4", "#6f86a4"], ["鋼5", "#9db4ce"], ["鋼6", "#d0e0f0"], ["真鍮1", "#5a3c12"], ["真鍮2", "#8a5f1c"], ["真鍮3", "#c08a2c"], ["真鍮4", "#f0c452"], ["光1", "#a04a10"], ["光2", "#e88a20"], ["光3", "#ffc84a"], ["光4", "#fff0a0"], ["光5", "#ffffff"], ["歪み暗", "#2a1450"], ["歪み", "#7a3fd0"], ["歪み明", "#c0a0ff"], ["影", "#1d2a1c"], ["蒸気", "#dfe8f0"]];

export const PIECES = [
  { name: "B1-水涸れの歪み", pal: pal1, build: boss1 },
  { name: "B2-積荷の歪み", pal: pal2, build: boss2 },
  { name: "B3-実験の歪み", pal: pal3, build: boss3 },
];
