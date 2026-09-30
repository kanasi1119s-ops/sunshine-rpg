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


/** 先が細くなる管（触手・角・爪）。r0が根もと、r1が先の半径。 */
function taper(g, pts, r0, r1, ramp, edge = 0) {
  const n = pts.length - 1;
  for (let s = 0; s < n; s++) {
    const [x0, y0] = pts[s], [x1, y1] = pts[s + 1], m = Math.max(2, Math.ceil(Math.hypot(x1 - x0, y1 - y0)));
    for (let i = 0; i <= m; i++) {
      const t = (s + i / m) / n, rad = r0 + (r1 - r0) * t, cx = x0 + (x1 - x0) * i / m, cy = y0 + (y1 - y0) * i / m;
      ell(g, cx, cy, rad, rad, (r, c, nx, ny, d, lum) => (d > 0.8 ? edge : ramp[toneIdx(ramp.length, lum, c, r, 0.05)]));
    }
  }
}
/** 牙（下向き dir=1 / 上向き dir=-1 の三角）。 */
function fang(g, x, y, w, h, dir, ramp, edge = 0) {
  for (let i = 0; i <= h; i++) { const half = w * (1 - i / h) / 2; for (let c = -Math.ceil(half); c <= Math.ceil(half); c++) { const r = y + dir * i; const k = i === h || Math.abs(c) > half - 0.6 ? edge : c < 0 ? ramp[2] : ramp[1]; px(g, r, x + c, i < 2 && Math.abs(c) < half - 1 ? ramp[3] : k); } }
}
/** 縦に細い瞳孔の目（不気味な光る目）。 */
function eye(g, cx, cy, rx, ry, glow, tilt = 0) {
  ell(g, cx, cy, rx + 2, ry + 2, (r, c, nx, ny, d) => (d > 0.6 ? 0 : 1));
  ell(g, cx, cy, rx, ry, (r, c, nx, ny, d, lum) => { const t = d < 0.25 ? 3 : d < 0.55 ? 2 : d < 0.85 ? 1 : 0; return glow[Math.min(glow.length - 1, t + (lum > 0.4 ? 1 : 0))]; });
  for (let r = -ry; r <= ry; r++) { const w = Math.max(0, Math.round((1 - Math.abs(r) / ry) * rx * 0.28)); for (let c = -w; c <= w; c++) px(g, cy + r, cx + c + Math.round(r * tilt), 0); }
  px(g, cy - ry * 0.4, cx - rx * 0.4, 15);                       // 目の照り返し
}
/** 外周に、ゆらめく毒気（歪みのもや）を散らす。 */
function miasma(g, ramp, reach, density, skip) {
  const has = (r, c) => r >= 0 && r < W && c >= 0 && c < W && g[r][c] !== -1 && !skip.includes(g[r][c]);
  const put = [];
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) {
    if (g[r][c] !== -1 && !skip.includes(g[r][c])) continue;
    for (let d = 1; d <= reach; d++) {
      if ([[d, 0], [-d, 0], [0, d], [0, -d], [d, d], [-d, d], [d, -d], [-d, -d]].some(([a, b]) => has(r + a, c + b))) {
        const wisp = hash(Math.floor(c / 3), Math.floor((r + d * 2) / 3));
        if (hash(c, r) < density * (1 - d / (reach + 1)) * (0.4 + wisp)) put.push([r, c, d < reach / 3 ? ramp[2] : d < reach * 0.66 ? ramp[1] : ramp[0]]);
        break;
      }
    }
  }
  for (const [r, c, k] of put) g[r][c] = k;
}
function outlineAll(g, skip) {
  const has = (r, c) => r >= 0 && r < W && c >= 0 && c < W && g[r][c] !== -1 && !skip.includes(g[r][c]);
  const add = []; for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) if ((g[r][c] === -1 || skip.includes(g[r][c])) && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(r + a, c + b))) add.push([r, c]);
  for (const [r, c] of add) g[r][c] = 0;
}

/** 背後の禍々しい光輪（暗い環に、とげと呪印の刻み）。 */
function halo(g, cx, cy, R, ramp) {
  for (let a = 0; a < 6.2832; a += 0.003) for (let t = -3; t <= 3; t += 0.7) { const rr = R + t; px(g, cy + Math.sin(a) * rr, cx + Math.cos(a) * rr, Math.abs(t) > 2 ? ramp[0] : ramp[1]); }
  for (let i = 0; i < 24; i++) { const a = i / 24 * 6.2832 + 0.1; const long = i % 3 === 0; const len = long ? 18 : 8; for (let k = 4; k < len; k++) { const rr = R + k, w = Math.max(0, (long ? 3.2 : 2) * (1 - k / len)); for (let d = -w; d <= w; d += 0.6) px(g, cy + Math.sin(a) * rr + Math.cos(a) * d, cx + Math.cos(a) * rr - Math.sin(a) * d, ramp[k < len * 0.5 ? 1 : 0]); } }
  for (let i = 0; i < 36; i++) { const a = i / 36 * 6.2832; const rr = R - 9; for (let k = 0; k < 4; k++) px(g, cy + Math.sin(a) * (rr - k), cx + Math.cos(a) * (rr - k), i % 2 ? ramp[1] : ramp[2]); }      // 呪印の刻み
}
/** 小さな目の群れ（気味悪さ）。 */
function eyeCluster(g, cx, cy, n, spread, glow, seed) {
  for (let i = 0; i < n; i++) { const a = hash(seed, i) * 6.2832, d = Math.sqrt(hash(seed + 9, i)) * spread; const x = cx + Math.cos(a) * d, y = cy + Math.sin(a) * d * 0.8, rr = 3 + Math.floor(hash(seed + 3, i) * 3); eye(g, Math.round(x), Math.round(y), rr, rr - 1, glow, (hash(seed, i + 40) - 0.5) * 0.6); }
}
/** 右・下の縁を明るくして、背後の光に照らされたように見せる。 */
function rimLight(g, skip, col, bright) {
  const bg = (r, c) => r < 0 || r >= W || c < 0 || c >= W || g[r][c] === -1 || skip.includes(g[r][c]);
  const put = [];
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) { const k = g[r][c]; if (k === -1 || k === 0 || skip.includes(k)) continue; if (bg(r, c + 2) || bg(r, c + 1)) put.push([r, c, hash(c, r) < 0.85 ? col : bright]); else if (bg(r + 2, c + 1) && hash(c, r) < 0.5) put.push([r, c, col]); }
  for (const [r, c, k] of put) g[r][c] = k;
}
/** 牙と牙のあいだに垂れるよだれの糸。 */
function slime(g, xs, y0, y1, col) { for (const x of xs) for (let r = y0; r < y1; r++) if ((r + x) % 5 !== 0) px(g, r, x, col); }

// ======== 1. 水涸れの歪み（第1章）: 干からびた骸（むくろ）の巨体。胸は空洞で、暗い水が逆流する ========
// pal: 0縁 1-5灰の粘土(暗→明) 6割れ目の暗 7-9紫の光(暗→明) 10-13骨(暗→明) 14洞の闇 15白 16-18目の赤紫(暗→明) 19黒い水 20黒い水の光 21影 22毒気暗 23毒気
const boss1 = () => {
  const g = makeGrid();
  const CL = [1, 2, 3, 4, 5], BN = [10, 11, 12, 13], EYE = [16, 17, 18];
  shadowUnder(g, 128, 241, 104, 11, 21);
  halo(g, 128, 112, 112, [22, 24, 25]);
  // 黒い水の触手（地面から）
  for (const [x0, x1, y1, cx] of [[40, 8, 150, 4], [216, 250, 156, 254], [86, 66, 190, 40], [170, 192, 190, 226]]) taper(g, curve([x0, 244], [cx, 205], [x1, y1]), 9, 2, [19, 19, 20], 0);
  const clay = (r, c, nx, ny, d, lum) => {
    const [d1, d2] = worley(c, r * 1.1, 20, 3); const edge = d2 - d1;
    if (edge < 0.05) return hash(c, r) < 0.7 ? 8 : 9;                  // 割れ目から漏れる紫の光
    if (edge < 0.11) return 6;
    let t = toneIdx(5, lum - 0.12, c, r, 0.14); if (d1 > 0.6) t = Math.max(0, t - 1);
    return CL[t];
  };
  // 腕: 右（向かって左）は巨大で長い爪、左は細く垂れる
  // 左腕は高く振り上げ、鉤爪を開く（力強い輪郭）。右腕は重く垂れる
  for (const [x, y] of curve([58, 136], [10, 118], [24, 62], 40)) { const rad = 28 - 11 * (136 - y) / 74 * 0 - (136 - y) / 74 * 11; ell(g, x, y, rad, rad, clay); }
  ell(g, 26, 52, 22, 20, clay);
  for (const [x, dx] of [[8, -6], [18, -2], [30, 3], [42, 8]]) taper(g, curve([x + 2, 42], [x + dx, 22], [x + dx * 1.6 + 2, 2]), 5, 1, BN, 0);
  ell(g, 232, 160, 22, 56, clay);
  for (const [x, dx] of [[222, 1], [232, 3], [242, 5]]) taper(g, curve([x, 208], [x + dx, 226], [x + dx * 2, 244]), 4, 1, BN, 0);
  // 胴（空洞の胸: 肋骨と、暗い洞、脈動する紫の核）
  ell(g, 128, 156, 82, 84, clay);
  ell(g, 128, 150, 46, 56, (r, c, nx, ny, d) => (d > 0.9 ? 0 : d > 0.7 ? 6 : 14));
  for (let i = 0; i < 5; i++) { const y = 118 + i * 17; for (let c = 92; c <= 164; c++) { const nx = (c - 128) / 38, yy = y + Math.round((nx * nx) * 12 - 10); const lum = -nx * 0.4 + 0.3; px(g, yy, c, BN[toneIdx(4, lum, c, yy, 0.05)]); px(g, yy + 1, c, BN[toneIdx(4, lum - 0.3, c, yy, 0.05)]); px(g, yy + 2, c, 0); } }
  ell(g, 128, 160, 17, 20, (r, c, nx, ny, d) => (d > 0.85 ? 8 : d > 0.5 ? 9 : 15));
  // 胸の洞から黒い水の触手が這い出す（先端に目）
  for (const [pts, ex, ey] of [[curve([112, 176], [80, 212], [44, 196]), 44, 196], [curve([146, 178], [186, 222], [214, 198]), 214, 198], [curve([128, 190], [124, 226], [100, 240]), 100, 240]]) { taper(g, pts, 8, 3, [19, 19, 20]); eye(g, ex, ey, 5, 4, EYE, 0); }
  // 肩のとげ・背中のとげ
  for (const [x, y, w, h, dir] of [[60, 96, 16, 34, -1], [90, 80, 12, 30, -1], [196, 96, 16, 34, -1], [166, 80, 12, 30, -1]]) fang(g, x, y, w, h, dir, BN);
  // 頭（髑髏）: 大きく裂けた口と二重の牙、空洞の眼窩に赤紫の目
  ell(g, 128, 68, 46, 44, clay);
  ell(g, 128, 108, 32, 18, (r, c, nx, ny, d, lum) => (ny < 0 ? null : (d > 0.8 ? 0 : CL[toneIdx(5, lum, c, r, 0.1)])));
  for (const ex of [108, 148]) { ell(g, ex, 66, 15, 14, (r, c, nx, ny, d) => (d > 0.8 ? 0 : 14)); }
  eyeCluster(g, 62, 168, 7, 24, EYE, 11); eyeCluster(g, 194, 176, 6, 22, EYE, 12);
  eye(g, 108, 67, 9, 8, EYE, -0.2); eye(g, 148, 67, 9, 8, EYE, 0.2); eye(g, 128, 46, 6, 6, EYE, 0);          // 額にも第三の目
  ell(g, 128, 94, 30, 12, (r, c, nx, ny, d) => (d > 0.75 ? 0 : 14));                                          // 口の闇
  for (let i = 0; i < 9; i++) { const x = 100 + i * 7; fang(g, x, 84, 6, 10 + (i % 2) * 5, 1, BN); fang(g, x + 3, 104, 6, 9 + (i % 2) * 4, -1, BN); }
  slime(g, [102, 112, 122, 134, 144, 154], 96, 105, 13);
  // 角（曲がった骨）
  taper(g, curve([94, 44], [76, 20], [88, 4]), 7, 1, BN); taper(g, curve([162, 44], [182, 20], [170, 4]), 7, 1, BN);
  // したたる黒い水
  for (const [x, y] of [[100, 112], [128, 116], [156, 112], [40, 236], [230, 216], [120, 230], [150, 236]]) for (let i = 0; i < 16; i++) px(g, y + i, x, i > 12 ? 20 : 19);
  // 歪みの結晶（紫）
  for (const [x, y, w, h] of [[16, 60, 8, 18], [242, 70, 8, 18], [30, 20, 6, 12], [224, 24, 6, 13], [128, 12, 6, 12]]) shard(g, x, y, w, h, [7, 8, 9], 0);
  outlineAll(g, [21, 22, 23, 24, 25]);
  rimLight(g, [21, 22, 23, 24, 25], 9, 15);
  miasma(g, [22, 22, 23], 12, 0.75, [21, 22, 23, 24, 25]);
  return g;
};
const pal1 = [["縁", "#0a0610"], ["粘土1", "#241c26"], ["粘土2", "#3c3040"], ["粘土3", "#584a5c"], ["粘土4", "#7a6a78"], ["粘土5", "#a09096"], ["割れ目", "#160a20"], ["紫光1", "#4a1a80"], ["紫光2", "#8a3ad8"], ["紫光3", "#d8a4ff"], ["骨1", "#3a3026"], ["骨2", "#66584a"], ["骨3", "#a49480"], ["骨4", "#dcccb0"], ["洞の闇", "#0a0410"], ["白", "#ffffff"], ["目1", "#7a0a3a"], ["目2", "#e0206a"], ["目3", "#ff9ac0"], ["黒水", "#0a0e1c"], ["黒水光", "#3a4a80"], ["影", "#1a1424"], ["毒気1", "#2a1450"], ["毒気2", "#5b2fa0"], ["光輪暗", "#6a0c26"], ["光輪明", "#c8285a"]];

// ======== 2. 積荷の歪み（第2章）: 大口を開けた木箱の化け物。牙は割れた板、舌は縄、目は灯り石 ========
// pal: 0縁 1-5暗い木(暗→明) 6金具暗 7金具明 8-11血の赤〜琥珀(暗→明) 12洞の闇 13-15牙の板(暗→明) 16縄 17黒い染み 18-20目(暗→明) 21影 22毒気暗 23毒気
const boss2 = () => {
  const g = makeGrid();
  const WD = [1, 2, 3, 4, 5], GL = [8, 9, 10, 11], TH = [13, 14, 15], EY = [18, 19, 20];
  shadowUnder(g, 128, 242, 106, 10, 21);
  halo(g, 128, 118, 118, [22, 24, 25]);
  function crate(x, y, w, h, seed) {
    for (let r = y; r < y + h; r++) for (let c = x; c < x + w; c++) {
      const u = (c - x) / w, v = (r - y) / h, plank = Math.floor((r - y) / 11), inP = (r - y) % 11;
      const lum = (-(u - 0.5) * 0.9 - (v - 0.5) * 0.9) * 0.6 - 0.05; let t = toneIdx(5, lum, c, r, 0.06);
      if (inP === 0) t = Math.max(0, t - 2); else if (inP === 10) t = Math.max(0, t - 1);
      if (hash(plank + seed, 7) < 0.35) t = clamp(t - 1, 0, 4);
      if (hash(Math.floor((c + plank * 13) / 9), plank + seed) < 0.06 && inP > 1) t = 0;                      // 腐った黒ずみ
      if ((c - x) < 4 || (c - x) >= w - 4 || (r - y) < 4 || (r - y) >= h - 4) t = clamp(((c - x) < 4 || (r - y) < 4 ? 3 : 1), 0, 4);
      px(g, r, c, WD[t]);
    }
    for (let c = x; c < x + w; c++) { px(g, y, c, 0); px(g, y + h - 1, c, 0); } for (let r = y; r < y + h; r++) { px(g, r, x, 0); px(g, r, x + w - 1, 0); }
    for (const [ax, ay] of [[x + 6, y + 6], [x + w - 8, y + 6], [x + 6, y + h - 8], [x + w - 8, y + h - 8]]) { px(g, ay, ax, 7); px(g, ay + 1, ax, 6); px(g, ay, ax + 1, 6); }
  }
  // 腕: 割れた板でできた長い爪
  crate(4, 120, 46, 96, 1); crate(206, 112, 46, 104, 2);
  for (const [x, y] of [[8, 214], [20, 216], [32, 214], [44, 212]]) taper(g, curve([x, y], [x - 2, y + 14], [x - 6, y + 30]), 4, 1, TH);
  for (const [x, y] of [[212, 214], [224, 216], [236, 214], [248, 212]]) taper(g, curve([x, y], [x + 2, y + 14], [x + 6, y + 30]), 4, 1, TH);
  // 胴の箱
  crate(28, 168, 94, 78, 3); crate(122, 172, 102, 74, 4); crate(86, 138, 84, 56, 5);
  crate(46, 96, 84, 66, 6); crate(126, 92, 86, 70, 7);
  // 頭の箱: 巨大な口
  crate(84, 18, 92, 82, 8);
  ell(g, 130, 66, 40, 22, (r, c, nx, ny, d) => (d > 0.86 ? 0 : d > 0.55 ? 8 : 12));
  for (let i = 0; i < 9; i++) { const x = 96 + i * 8; fang(g, x, 50, 7, 13 + (i % 3) * 3, 1, TH); fang(g, x + 4, 82, 7, 11 + (i % 2) * 4, -1, TH); }
  slime(g, [98, 108, 118, 138, 148, 158], 63, 82, 15);
  eyeCluster(g, 34, 176, 6, 20, EY, 21); eyeCluster(g, 222, 172, 6, 20, EY, 22); eyeCluster(g, 128, 226, 5, 24, EY, 23);
  // 舌（縄）が垂れ、よだれ
  taper(g, curve([128, 70], [150, 108], [122, 138]), 6, 3, [16, 16, 5]);
  for (const [x, y] of [[104, 84], [156, 84], [122, 92]]) for (let i = 0; i < 14; i++) px(g, y + i, x, i > 10 ? 10 : 17);
  // 目（灯り石）をあちこちに
  eye(g, 106, 34, 8, 7, EY, -0.2); eye(g, 154, 34, 8, 7, EY, 0.2);
  eye(g, 68, 132, 6, 5, EY, 0); eye(g, 186, 128, 7, 6, EY, 0.1); eye(g, 90, 206, 6, 5, EY, 0); eye(g, 178, 210, 6, 5, EY, -0.1);
  // 割れ目から漏れる血色の灯り
  for (const [x, y, w, h] of [[80, 158, 8, 14], [170, 162, 7, 13], [126, 186, 9, 16], [52, 224, 7, 12], [200, 228, 8, 12]]) for (let r = -h; r <= h; r++) for (let c = -w; c <= w; c++) { const d = (c / w) ** 2 + (r / h) ** 2; if (d < 1) px(g, y + r, x + c, d < 0.2 ? 11 : d < 0.5 ? 10 : d < 0.8 ? 9 : 8); }
  // 縄・鎖の触手が暴れる
  taper(g, curve([60, 176], [12, 150], [4, 100]), 4, 1.5, [16, 16, 5]); taper(g, curve([196, 176], [246, 150], [252, 96]), 4, 1.5, [16, 16, 5]);
  taper(g, curve([90, 244], [40, 246], [10, 226]), 4, 1.5, [17, 17, 6]);
  // 歪みの結晶
  for (const [x, y, w, h] of [[16, 60, 7, 16], [240, 52, 8, 17], [30, 22, 5, 11], [224, 20, 5, 12]]) shard(g, x, y, w, h, [22, 22, 23], 0);
  outlineAll(g, [21, 22, 23, 24, 25]);
  rimLight(g, [21, 22, 23, 24, 25], 10, 11);
  miasma(g, [22, 22, 23], 12, 0.7, [21, 22, 23, 24, 25]);
  return g;
};
const pal2 = [["縁", "#0a0606"], ["木1", "#1e1410"], ["木2", "#382418"], ["木3", "#563820"], ["木4", "#7a5230"], ["木5", "#a07444"], ["金具暗", "#2a2a32"], ["金具明", "#7a7a88"], ["赤1", "#5a0a10"], ["赤2", "#b01a20"], ["赤3", "#ff5a20"], ["琥珀", "#ffc040"], ["洞の闇", "#100404"], ["牙1", "#5a5040"], ["牙2", "#b0a488"], ["牙3", "#f0e8cc"], ["縄", "#8a7448"], ["黒い染み", "#0c0808"], ["目1", "#7a1000"], ["目2", "#ff4010"], ["目3", "#ffe080"], ["影", "#1a1418"], ["毒気1", "#2a1450"], ["毒気2", "#5b2fa0"], ["光輪暗", "#6a0c26"], ["光輪明", "#c8285a"]];

// ======== 3. 実験の歪み（第3章）: 実験装置が生き物のように蠢く。巨大な一つ目、歯車の顎、血管のような管 ========
// pal: 0縁 1-6錆びた鋼(暗→明) 7-9錆(暗→明) 10-13目の白目〜赤(暗→明) 14-16虹彩(暗→明) 17歯の鋼 18血管の赤 19-21紫の脈(暗→明) 22影 23毒気暗 24毒気
const boss3 = () => {
  const g = makeGrid();
  const ST = [1, 2, 3, 4, 5, 6], RS = [7, 8, 9], IR = [14, 15, 16];
  shadowUnder(g, 128, 244, 108, 9, 22);
  halo(g, 128, 112, 116, [23, 25, 24]);
  // 鎖（上から垂れる）
  for (const x0 of [50, 206]) for (let i = 0; i < 44; i++) { const y = 6 + i * 3.6, x = x0 + Math.sin(i * 0.5) * 3; ell(g, x, y, 2.6, 3.4, (r, c, nx, ny, d) => (d > 0.6 ? 2 : i % 2 ? 4 : 3)); }
  // 土台と脚
  const plate = (x, y, w, h) => { for (let r = y; r < y + h; r++) for (let c = x; c < x + w; c++) { const lum = -((c - x) / w - 0.5) * 0.6 - ((r - y) / h - 0.5) * 1.2 - 0.1; let t = toneIdx(6, lum, c, r, 0.08); if (r === y) t = 4; if (r === y + h - 1) t = 0; if (hash(c >> 1, r >> 1) < 0.1) t = 0; px(g, r, c, ST[t]); if (hash(c, r) < 0.06) px(g, r, c, RS[1]); } };
  plate(20, 218, 216, 26); plate(48, 202, 160, 18);
  for (let i = 0; i < 12; i++) fang(g, 26 + i * 18, 218, 10, 12, -1, [1, 2, 3, 4]);           // 土台のとげ
  // 血管のような管（触手）: 紫の脈が光る
  const vein = (pts, r0, r1) => { taper(g, pts, r0, r1, ST); const n = pts.length; for (let i = 3; i < n - 2; i += 3) { const [x, y] = pts[i]; px(g, y, x, 21); px(g, y + 1, x, 20); px(g, y, x + 1, 20); } };
  vein(curve([60, 200], [8, 190], [12, 120], 32), 10, 3); vein(curve([196, 200], [248, 190], [244, 116], 32), 10, 3);
  vein(curve([70, 100], [20, 96], [16, 40], 30), 8, 3); vein(curve([186, 100], [236, 96], [240, 36], 30), 8, 3);
  vein(curve([100, 214], [60, 246], [24, 236], 26), 7, 2); vein(curve([156, 214], [196, 246], [232, 236], 26), 7, 2);
  // 歯車の顎（下の口）: 大きな歯車の上半分が、牙のように上を向く
  ell(g, 128, 186, 78, 40, (r, c, nx, ny, d) => (d > 0.85 ? 0 : 14));                       // 口の闇（赤黒い）
  for (let i = 0; i < 12; i++) { const x = 66 + i * 11.6, hh = 20 + (i % 2) * 6; fang(g, x, 218 - 30, 10, hh, -1, [2, 3, 4, 5]); }
  for (let i = 0; i < 11; i++) { const x = 72 + i * 11.6, hh = 14 + (i % 2) * 5; fang(g, x, 150, 9, hh, 1, [2, 3, 4, 5]); }
  // 頭部の装甲と巨大な一つ目
  ell(g, 128, 112, 68, 66, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : ST[toneIdx(6, lum - 0.2, c, r, 0.12)]));
  for (let i = 0; i < 14; i++) { const a = i / 14 * 6.283; px(g, 112 + Math.sin(a) * 62, 128 + Math.cos(a) * 62, 6); px(g, 112 + Math.sin(a) * 62 + 1, 128 + Math.cos(a) * 62, 1); }   // リベット
  ell(g, 128, 112, 46, 44, (r, c, nx, ny, d, lum) => { if (d > 0.9) return 0; let t = d < 0.5 ? 3 : d < 0.8 ? 2 : 1; if (lum > 0.5) t += 0; return 10 + Math.min(3, t); });      // 白目（濁った黄と赤）
  for (let n = 0; n < 14; n++) { let a = hash(n, 5) * 6.283, rr = 44; for (let i = 0; i < 26; i++) { rr -= 1.2; a += (hash(n, i + 9) - 0.5) * 0.28; px(g, 112 + Math.sin(a) * rr, 128 + Math.cos(a) * rr, 18); } }    // 充血した血管
  ell(g, 128, 114, 26, 26, (r, c, nx, ny, d, lum) => (d > 0.9 ? 0 : IR[toneIdx(3, lum + 0.2 - d * 0.5, c, r, 0.1)]));    // 虹彩
  for (let r = 96; r <= 132; r++) { const w = Math.round((1 - Math.abs(r - 114) / 19) * 6); for (let c = -w; c <= w; c++) px(g, r, 128 + c, 0); }     // 縦の瞳孔
  px(g, 104, 118, 15); px(g, 105, 118, 15); px(g, 104, 119, 15);
  // まぶた（金属の板）
  ell(g, 128, 70, 60, 26, (r, c, nx, ny, d, lum) => (ny > 0.35 ? null : d > 0.88 ? 0 : ST[toneIdx(6, lum - 0.15, c, r, 0.1)]));
  ell(g, 128, 158, 52, 16, (r, c, nx, ny, d, lum) => (ny < -0.2 ? null : d > 0.85 ? 0 : ST[toneIdx(6, lum - 0.25, c, r, 0.1)]));
  // 上の歯車と横の歯車（回転する刃）
  function gear(cx, cy, R, teeth, spin) {
    for (let r = Math.floor(cy - R * 1.15); r <= cy + R * 1.15; r++) for (let c = Math.floor(cx - R * 1.15); c <= cx + R * 1.15; c++) {
      const dx = c - cx, dy = r - cy, rad = Math.hypot(dx, dy), ang = Math.atan2(dy, dx) + spin;
      const tooth = Math.max(0, Math.sin(teeth * ang)); const outer = R * (0.82 + 0.26 * Math.pow(tooth, 0.6)); if (rad > outer) continue;      // 鋭い刃の歯
      const lum = (-dx * 0.55 - dy * 0.65) / R * 0.7 - 0.05; let t = toneIdx(6, lum, c, r, 0.08);
      if (rad > outer - 3) t = 0; else if (Math.abs(rad - R * 0.6) < 2) t = 0; else if (rad < R * 0.24) t = clamp(t + (rad < R * 0.1 ? -2 : 1), 0, 5); else if (rad < R * 0.6 && Math.sin(5 * ang) > 0.6) t = 0;
      if (hash(c, r) < 0.05) { px(g, r, c, RS[1]); continue; } px(g, r, c, ST[t]);
    }
  }
  // 怒った眉のような装甲板（目を斜めにいからせる）
  for (const sg of [-1, 1]) for (let i = 0; i < 46; i++) { const x = 128 + sg * (12 + i), y = 74 - i * 0.28 * -1 + (i > 30 ? (i - 30) * -1.2 : 0) - 6; for (let t = -5; t <= 5; t++) px(g, y + t + (sg > 0 ? 0 : 0), x, t < -3 ? 5 : t < 1 ? 3 : t < 4 ? 2 : 0); }
  for (let i = 0; i < 7; i++) fang(g, 74 + i * 18, 44, 9, 18 + (i % 2) * 8, -1, [2, 3, 4, 5]);     // 頭上の冠のとげ
  gear(128, 34, 30, 12, 0.2);
  slime(g, [72, 88, 104, 120, 136, 152, 168, 184], 156, 176, 17);
  // 紫の稲妻
  for (const [ax, ay, bx, by] of [[128, 112, 24, 60], [128, 112, 236, 70], [128, 190, 8, 240], [128, 190, 248, 236]]) { let x = ax, y = ay; const n = 30; for (let i = 0; i < n; i++) { x += (bx - x) / (n - i) + (hash(i, ax) - 0.5) * 9; y += (by - y) / (n - i) + (hash(i, ay) - 0.5) * 6; px(g, y, x, 20); px(g, y, x + 1, 19); if (i % 3 === 0) px(g, y - 1, x - 1, 21); } }
  for (const [x, y, w, h] of [[14, 60, 7, 16], [242, 56, 8, 17], [30, 22, 5, 11], [224, 24, 5, 12]]) shard(g, x, y, w, h, [19, 20, 21], 0);
  outlineAll(g, [22, 23, 24, 25]);
  rimLight(g, [22, 23, 24, 25], 21, 6);
  miasma(g, [23, 23, 24], 12, 0.7, [22, 23, 24, 25]);
  return g;
};
const pal3 = [["縁", "#080810"], ["鋼1", "#16161c"], ["鋼2", "#26262e"], ["鋼3", "#3c3c48"], ["鋼4", "#585868"], ["鋼5", "#7c7c8c"], ["鋼6", "#a8a8b8"], ["錆1", "#3a1a0a"], ["錆2", "#6a3010"], ["錆3", "#a05a20"], ["白目1", "#3a2a1a"], ["白目2", "#6a5024"], ["白目3", "#a08a42"], ["白目4", "#d4c470"], ["虹彩1", "#5a0a10"], ["虹彩2", "#d02010"], ["虹彩3", "#ff7a18"], ["歯", "#c8c8d0"], ["血管", "#9a1020"], ["紫1", "#3a1070"], ["紫2", "#8a3ad8"], ["紫3", "#d8a8ff"], ["影", "#14101a"], ["毒気1", "#2a1450"], ["毒気2", "#5b2fa0"], ["光輪赤", "#a01a40"]];

// ======== 4. 砂嵐の歪み（第4章）: 渦を巻く砂の巨体。大きく裂けた口、砂に埋もれた荷車の骨組み、無数の目 ========
// pal: 0縁 1-5砂(暗→明) 6-8渦の影(暗→明) 9口の闇 10-12牙(暗→明) 13-15目(暗→明) 16琥珀の光 17影 18毒気暗 19毒気 20光輪暗 21光輪明 22白
const boss4 = () => {
  const g = makeGrid();
  const SD = [1, 2, 3, 4, 5], TH = [10, 11, 12], EY = [13, 14, 15];
  shadowUnder(g, 128, 242, 104, 10, 17);
  halo(g, 128, 118, 114, [18, 20, 21]);
  // 渦の帯（砂が巻き上がる）
  for (let k = 0; k < 5; k++) {
    const y0 = 60 + k * 36;
    for (let c = 6; c < 250; c++) {
      const u = (c - 6) / 244, y = y0 + Math.sin(u * 6.283 * 1.5 + k) * 12 + (u - 0.5) * (k % 2 ? 18 : -18), th = 6 + 4 * Math.sin(u * 3.14);
      for (let t = -th; t <= th; t += 0.7) { const lum = -t / th * 0.7 - 0.05; px(g, y + t, c, t > th - 1.2 || t < -th + 1 ? 6 : SD[toneIdx(5, lum, c, y + t, 0.14)]); }
    }
  }
  // 胴（砂の塊）
  const sand = (r, c, nx, ny, d, lum) => { const [d1] = worley(c, r, 14, 5); let t = toneIdx(5, lum - 0.1, c, r, 0.16); if (d1 < 0.16) t = Math.max(0, t - 1); return SD[t]; };
  ell(g, 128, 156, 92, 84, sand);
  ell(g, 128, 190, 108, 42, sand);
  // 荷車の骨組み（砂に埋もれた車輪）
  for (const [wx, wy, wr] of [[52, 196, 30], [204, 200, 28]]) {
    for (let a = 0; a < 6.283; a += 0.01) for (let t = -2; t <= 2; t += 0.7) px(g, wy + Math.sin(a) * (wr + t), wx + Math.cos(a) * (wr + t), t < 0 ? 4 : 2);
    for (let i = 0; i < 8; i++) { const a = i / 8 * 6.283; for (let k = 0; k < wr; k++) px(g, wy + Math.sin(a) * k, wx + Math.cos(a) * k, k % 2 ? 2 : 3); }
  }
  // 頭: 大きく裂けた口
  ell(g, 128, 78, 62, 56, sand);
  ell(g, 128, 96, 42, 30, (r, c, nx, ny, d) => (d > 0.85 ? 0 : d > 0.6 ? 6 : 9));
  for (let i = 0; i < 10; i++) { const x = 96 + i * 7; fang(g, x, 76, 6, 12 + (i % 3) * 3, 1, TH); if (i % 2 === 0) fang(g, x + 3, 116, 6, 10, -1, TH); }
  slime(g, [100, 112, 126, 140, 154], 90, 108, 16);
  eye(g, 100, 54, 10, 9, EY, -0.2); eye(g, 156, 54, 10, 9, EY, 0.2); eye(g, 128, 34, 6, 6, EY, 0);
  eyeCluster(g, 40, 140, 6, 22, EY, 41); eyeCluster(g, 216, 146, 6, 22, EY, 42); eyeCluster(g, 128, 210, 5, 30, EY, 43);
  // 砂の腕（鉤爪）
  for (const [sx, ex] of [[44, 8], [212, 248]]) { taper(g, curve([sx, 130], [(sx + ex) / 2, 90], [ex, 96]), 16, 4, SD); for (const d of [-8, 0, 8]) taper(g, curve([ex, 96], [ex + d, 76], [ex + d * 1.5, 60]), 4, 1, TH); }
  // 琥珀の割れ目の光
  for (const [x, y, w, h] of [[80, 170, 6, 12], [178, 176, 6, 12], [128, 220, 8, 10]]) for (let r = -h; r <= h; r++) for (let c = -w; c <= w; c++) { const d = (c / w) ** 2 + (r / h) ** 2; if (d < 1) px(g, y + r, x + c, d < 0.4 ? 22 : 16); }
  for (const [x, y, w, h] of [[16, 60, 7, 16], [242, 54, 8, 17], [30, 22, 5, 11], [224, 22, 5, 12]]) shard(g, x, y, w, h, [18, 19, 19], 0);
  outlineAll(g, [17, 18, 19, 20, 21]);
  rimLight(g, [17, 18, 19, 20, 21], 5, 22);
  miasma(g, [18, 18, 19], 12, 0.7, [17, 18, 19, 20, 21]);
  return g;
};
const pal4 = [["縁", "#0e0a06"], ["砂1", "#4a3620"], ["砂2", "#7a5c34"], ["砂3", "#a88448"], ["砂4", "#d0aa62"], ["砂5", "#f0d488"], ["渦1", "#2c1e12"], ["渦2", "#5a4224"], ["渦3", "#8a6a3a"], ["口の闇", "#120806"], ["牙1", "#5a4e3e"], ["牙2", "#b8ac90"], ["牙3", "#f4ecd4"], ["目1", "#6a1a08"], ["目2", "#f05a18"], ["目3", "#ffe488"], ["琥珀", "#ffb838"], ["影", "#1a1410"], ["毒気1", "#2a1450"], ["毒気2", "#5b2fa0"], ["光輪暗", "#6a0c26"], ["光輪明", "#c8285a"], ["白", "#fff8e0"]];

// ======== 5. 予言の歪み（第5章）: 巨大な石碑。刻まれた文字は書き換えられ、紙片の帯が巻きつき、目が開く ========
// pal: 0縁 1-5石(暗→明) 6文字の暗 7-9青白い文字光(暗→明) 10-12紙(暗→明) 13-15目(暗→明) 16割れ目 17影 18毒気暗 19毒気 20光輪暗 21光輪明 22白
const boss5 = () => {
  const g = makeGrid();
  const ST = [1, 2, 3, 4, 5], PP = [10, 11, 12], EY = [13, 14, 15];
  shadowUnder(g, 128, 244, 100, 9, 17);
  halo(g, 128, 112, 116, [18, 20, 21]);
  // 石碑本体（縦長の板。上は欠けている）
  for (let r = 28; r < 240; r++) for (let c = 58; c < 198; c++) {
    const top = 28 + Math.round(10 * Math.sin(c * 0.21) + 8 * hash(c >> 2, 3));
    if (r < top) continue;
    const u = (c - 58) / 140, v = (r - 28) / 212, lum = -(u - 0.5) * 0.8 - (v - 0.5) * 0.5;
    let t = toneIdx(5, lum, c, r, 0.12); const [d1, d2] = worley(c, r, 26, 8); if (d2 - d1 < 0.06) t = 0;
    if (c < 62 || c > 193) t = c < 62 ? 4 : 0; px(g, r, c, ST[t]);
  }
  // 刻まれた文字（一部だけ青白く光る＝書き換えられた欄）
  for (let row = 0; row < 8; row++) for (let col = 0; col < 7; col++) {
    const x = 74 + col * 17, y = 110 + row * 15; if (hash(row, col + 60) < 0.2) continue;
    const lit = row === 3 && col > 1 && col < 6;
    for (let i = 0; i < 9; i++) { px(g, y + i, x + (hash(row + i, col) < 0.5 ? 0 : 6), lit ? 8 : 6); px(g, y + (i % 4) * 2, x + i % 7, lit ? 9 : 6); }
  }
  // 巻きつく紙片の帯
  for (const [y0, dy] of [[70, 40], [150, -30], [206, 20]]) for (let c = 30; c < 226; c++) { const u = (c - 30) / 196, y = y0 + dy * Math.sin(u * 3.14 * 1.2), w = 8; for (let t = -w; t <= w; t++) px(g, y + t, c, t < -w + 1 || t > w - 1 ? 0 : PP[toneIdx(3, -t / w * 0.7, c, y + t, 0.1)]); }
  // 大きな目と、無数の小さな目
  ell(g, 128, 74, 36, 26, (r, c, nx, ny, d) => (d > 0.85 ? 0 : d > 0.6 ? 6 : 14));
  eye(g, 128, 74, 22, 20, EY, 0);
  eyeCluster(g, 128, 170, 8, 40, EY, 51); eyeCluster(g, 40, 130, 5, 20, EY, 52); eyeCluster(g, 216, 140, 5, 20, EY, 53);
  // 割れ目と欠けた破片
  for (let i = 0; i < 3; i++) { let x = 110 + i * 20, y = 120; for (let k = 0; k < 90; k++) { x += (hash(k, i) - 0.5) * 6; y += 1.8; px(g, y, x, 16); px(g, y, x + 1, 0); } }
  for (const [x, y, w, h] of [[30, 90, 8, 18], [226, 100, 8, 18], [40, 30, 6, 12], [214, 26, 6, 13]]) shard(g, x, y, w, h, [7, 8, 9], 0);
  for (const x0 of [30, 226]) taper(g, curve([x0, 240], [x0 + (x0 < 100 ? -20 : 20), 190], [x0 + (x0 < 100 ? -8 : 8), 150]), 9, 2, ST);
  outlineAll(g, [17, 18, 19, 20, 21]);
  rimLight(g, [17, 18, 19, 20, 21], 9, 22);
  miasma(g, [18, 18, 19], 12, 0.7, [17, 18, 19, 20, 21]);
  return g;
};
const pal5 = [["縁", "#080a10"], ["石1", "#1c2028"], ["石2", "#343a46"], ["石3", "#505868"], ["石4", "#727c8e"], ["石5", "#9aa4b6"], ["文字暗", "#0a0c14"], ["文字1", "#1a4a80"], ["文字2", "#5ab0f0"], ["文字3", "#d0f0ff"], ["紙1", "#5a4e38"], ["紙2", "#b0a482"], ["紙3", "#f0e8cc"], ["目1", "#5a0a30"], ["目2", "#e0206a"], ["目3", "#ffc0d8"], ["割れ目", "#04060a"], ["影", "#141822"], ["毒気1", "#2a1450"], ["毒気2", "#5b2fa0"], ["光輪暗", "#6a0c26"], ["光輪明", "#c8285a"], ["白", "#ffffff"]];

// ======== 6. 試作機の歪み（第6章）: 雪と氷に覆われた古い機械。氷の結晶のとげ、凍った歯車、赤く光る核 ========
// pal: 0縁 1-5鋼(暗→明) 6-8氷(暗→明) 9核の光(暗) 10核の光 11核の白 12-14目(暗→明) 15雪 16歯の氷 17影 18毒気暗 19毒気 20光輪暗 21光輪明 22白
const boss6 = () => {
  const g = makeGrid();
  const ST = [1, 2, 3, 4, 5], IC = [6, 7, 8], EY = [12, 13, 14];
  shadowUnder(g, 128, 244, 108, 9, 17);
  halo(g, 128, 112, 116, [18, 20, 21]);
  // 氷のとげ（背後）
  for (let i = 0; i < 9; i++) { const x = 20 + i * 27, h = 60 + (i % 3) * 30; fang(g, x, 130 - h * 0.2, 16, h, -1, [6, 7, 8, 16], 0); }
  // 機械の胴
  const steel = (r, c, nx, ny, d, lum) => { let t = toneIdx(5, lum - 0.1, c, r, 0.1); if ((r >> 3) % 4 === 0 && (c >> 4) % 2 === 0) t = Math.max(0, t - 1); return ST[t]; };
  ell(g, 128, 168, 100, 72, steel);
  ell(g, 128, 96, 68, 58, steel);
  for (let i = 0; i < 16; i++) { const a = i / 16 * 6.283; px(g, 96 + Math.sin(a) * 62, 128 + Math.cos(a) * 62, 5); px(g, 96 + Math.sin(a) * 62 + 1, 128 + Math.cos(a) * 62, 0); }
  // 凍った歯車の顎
  ell(g, 128, 150, 58, 26, (r, c, nx, ny, d) => (d > 0.85 ? 0 : 9));
  for (let i = 0; i < 10; i++) { const x = 82 + i * 10; fang(g, x, 130, 9, 14 + (i % 2) * 6, 1, [6, 7, 8, 16]); fang(g, x + 5, 172, 9, 12 + (i % 2) * 5, -1, [6, 7, 8, 16]); }
  // 核（胸で赤く光る）
  ell(g, 128, 208, 26, 22, (r, c, nx, ny, d) => (d > 0.85 ? 0 : d > 0.55 ? 9 : d > 0.25 ? 10 : 11));
  // 目
  eye(g, 104, 82, 10, 9, EY, -0.2); eye(g, 152, 82, 10, 9, EY, 0.2); eye(g, 128, 56, 6, 6, EY, 0);
  eyeCluster(g, 36, 176, 5, 18, EY, 61); eyeCluster(g, 220, 180, 5, 18, EY, 62);
  // パイプの触手（霜つき）
  for (const [pts] of [[curve([50, 190], [8, 170], [10, 110], 30)], [curve([206, 190], [248, 170], [246, 106], 30)], [curve([80, 236], [40, 250], [16, 232], 24)], [curve([176, 236], [216, 250], [240, 232], 24)]]) taper(g, pts, 9, 3, ST);
  // 雪の積もり（上向きの面に白）
  for (let c = 0; c < W; c++) for (let r = 1; r < W; r++) if (g[r][c] !== -1 && g[r][c] >= 1 && g[r][c] <= 5 && (g[r - 1][c] === -1) && hash(c, r) < 0.85) { for (let k = 0; k < 3; k++) if (g[r + k]?.[c] >= 1 && g[r + k][c] <= 5) g[r + k][c] = k === 2 ? 8 : 15; }
  for (const [x, y, w, h] of [[16, 60, 7, 16], [242, 56, 8, 17], [30, 22, 5, 11], [224, 24, 5, 12]]) shard(g, x, y, w, h, [6, 7, 8], 0);
  outlineAll(g, [17, 18, 19, 20, 21]);
  rimLight(g, [17, 18, 19, 20, 21], 8, 22);
  miasma(g, [18, 18, 19], 12, 0.7, [17, 18, 19, 20, 21]);
  return g;
};
const pal6 = [["縁", "#060a10"], ["鋼1", "#141a24"], ["鋼2", "#28323e"], ["鋼3", "#42505e"], ["鋼4", "#647684"], ["鋼5", "#8ea0b0"], ["氷1", "#1a4a78"], ["氷2", "#4a9ad0"], ["氷3", "#b0e4ff"], ["核暗", "#6a0a10"], ["核", "#ff4a20"], ["核白", "#ffe8c0"], ["目1", "#0a3a5a"], ["目2", "#30c0f0"], ["目3", "#e0fbff"], ["雪", "#eef6ff"], ["氷歯", "#d8f0ff"], ["影", "#101620"], ["毒気1", "#2a1450"], ["毒気2", "#5b2fa0"], ["光輪暗", "#6a0c26"], ["光輪明", "#c8285a"], ["白", "#ffffff"]];

export const PIECES = [
  { name: "B1-水涸れの歪み", pal: pal1, build: boss1 },
  { name: "B2-積荷の歪み", pal: pal2, build: boss2 },
  { name: "B3-実験の歪み", pal: pal3, build: boss3 },
  { name: "B4-砂嵐の歪み", pal: pal4, build: boss4 },
  { name: "B5-予言の歪み", pal: pal5, build: boss5 },
  { name: "B6-試作機の歪み", pal: pal6, build: boss6 },
];
