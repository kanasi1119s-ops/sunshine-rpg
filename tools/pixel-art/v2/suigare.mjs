// 水涸れの歪み（第1章のボス・v2）: 干上がった川底の主。ひび割れた泥の皮膚の魚竜の骸がとぐろを巻き、あばら骨の奥から黒い水が滴る。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, bezier, smoothstep, outline, despeckle, groundShadow, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

// ---- この絵だけで使う部品 ----
function catmull(pts, n = 10) {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let s = 0; s < n; s++) {
      const t = s / n, t2 = t * t, t3 = t2 * t;
      out.push(p0.map((_, k) => 0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3)));
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
}
/** 太さが変わる管。pts=[[x,y,r]...] */
function tube(g, pts, ramp, opts = {}) {
  const path = catmull(pts, 12), parts = [];
  let last = null;
  for (const [x, y, r] of path) { if (last && Math.hypot(x - last[0], y - last[1]) < r * 0.35) continue; parts.push({ cx: x, cy: y, rx: r, ry: r }); last = [x, y]; }
  const m = Math.max(...pts.map((p) => p[2])) + 3;
  const box = [Math.floor(Math.min(...pts.map((p) => p[0])) - m), Math.floor(Math.min(...pts.map((p) => p[1])) - m), Math.ceil(Math.max(...pts.map((p) => p[0])) + m), Math.ceil(Math.max(...pts.map((p) => p[1])) + m)];
  paintField(g, heightField(parts, 5), ramp, { ...opts, box });
  return path;
}
function vor(x, y, S) {
  const gx = Math.floor(x / S), gy = Math.floor(y / S); let d1 = 1e9, d2 = 1e9, id = 0;
  for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
    const fx = (gx + i + hash(gx + i, gy + j)) * S, fy = (gy + j + hash(gx + i + 977, gy + j + 31)) * S, d = Math.hypot(x - fx, y - fy);
    if (d < d1) { d2 = d1; d1 = d; id = (gx + i) * 131 + gy + j; } else if (d < d2) d2 = d;
  }
  return { e: d2 - d1, id };
}
/** ひび割れ泥の質感。ひびは最暗色、板は縁がわずかに反る。 */
const mudTex = (S, crackW = 1.5) => (x, y) => {
  const v = vor(x, y, S); if (v.e < crackW) return -0.95;
  const v2 = vor(x + 40, y + 17, S * 0.45); // 細かい二次のひび（板の中の細い割れ）
  if (v2.e < 0.7 && hash(v.id, 5) < 0.5) return -0.5;
  const grime = -0.16 * smoothstep(140, 235, y) - 0.08 * smoothstep(190, 250, x) + 0.07 * smoothstep(120, 30, x + y * 0.4 - 60) ;
  return (hash(v.id, 7) - 0.5) * 0.17 + (Math.min(v.e, 7) / 7 - 0.5) * 0.15 + grime + (hash(x >> 1, y >> 1) < 0.05 ? -0.06 : 0);
};
function spike(g, x0, y0, x1, y1, r0, ramp) { const n = 14; const pts = Array.from({ length: n + 1 }, (_, i) => [x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n]); paintField(g, heightField(pts.map(([x, y], i) => ({ cx: x, cy: y, rx: r0 * (1 - i / (n + 0.6)) + 0.6, ry: r0 * (1 - i / (n + 0.6)) + 0.6 })), 5), ramp, { ambient: 0.25, box: [Math.floor(Math.min(x0, x1) - r0 - 2), Math.floor(Math.min(y0, y1) - r0 - 2), Math.ceil(Math.max(x0, x1) + r0 + 2), Math.ceil(Math.max(y0, y1) + r0 + 2)] }); }

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0d0a12"), RIM = pal.rgb("縁明", "#3a2c36"), SHD = pal.rgb("影", "#17111b");
  const MUD = pal.ramp("泥", 28, 0.3, 6, 0.06, 0.5, 34);
  const BONE = pal.ramp("骨", 46, 0.26, 4, 0.16, 0.78, 26);
  const WAT = pal.ramp("黒水", 222, 0.5, 4, 0.04, 0.34, 10);
  const CORE = pal.ramp("核", 172, 0.85, 4, 0.3, 0.82, 12);
  const g = makeGrid();

  groundShadow(g, 128, 247, 112, 8, SHD);

  // --- とぐろの胴（尾の先 → 深い底 → 首）。手前は大きく重く ---
  const body = [[214, 56, 3], [234, 70, 11], [243, 112, 19], [236, 160, 25], [204, 196, 28], [150, 208, 29], [90, 205, 28], [44, 184, 26], [22, 140, 22], [30, 96, 19], [66, 62, 16], [104, 54, 15]];
  tube(g, body, MUD, { ambient: 0.22, gain: 1.0, tex: mudTex(15) });
  // 内側のもうひとつのとぐろ（奥、暗い）。胴の内側に段を作る
  tube(g, [[56, 150, 12], [84, 124, 14], [128, 116, 15], [172, 124, 14], [200, 146, 12]], MUD, { ambient: 0.12, gain: 1.1, tex: (x, y, l) => mudTex(13)(x, y) - 0.12 });

  // --- 背びれ（骨の棘）。外周にそって並ぶ ---
  const ridge = [[250, 90, 14], [250, 130, 12], [246, 172, 12], [9, 118, 14], [8, 150, 12], [14, 176, 12], [18, 82, 13], [42, 60, 12], [200, 50, 9], [226, 44, 9]];
  for (const [ex, ey, len] of [[244, 74, 18], [254, 112, 16], [250, 150, 15], [232, 186, 14], [12, 112, 16], [4, 146, 15], [10, 178, 14], [16, 76, 16], [40, 52, 16], [74, 44, 15], [214, 46, 12]]) {
    const cxp = 128, cyp = 140, ang = Math.atan2(ey - cyp, ex - cxp);
    spike(g, ex - Math.cos(ang) * 8, ey - Math.sin(ang) * 8, ex + Math.cos(ang) * 10 - (ex > 128 ? -2 : 2), ey + Math.sin(ang) * 10 - 10, 5, BONE);
  }

  // --- 尾びれ（裂けた膜と骨の筋）---
  for (let i = 0; i < 6; i++) {
    const a = -2.55 + i * 0.36, len = 30 + (i % 2) * 8, x0 = 214, y0 = 56;
    const x1 = x0 + Math.cos(a) * len + 8, y1 = y0 + Math.sin(a) * len - 4;
    if (i < 5) { const a2 = a + 0.36, len2 = 30 + ((i + 1) % 2) * 8, x2 = x0 + Math.cos(a2) * len2 + 8, y2 = y0 + Math.sin(a2) * len2 - 4;
      for (let t = 0.25; t <= 1; t += 0.012) { const ax = x0 + (x1 - x0) * t, ay = y0 + (y1 - y0) * t, bx = x0 + (x2 - x0) * t, by = y0 + (y2 - y0) * t; if (t > 0.9 && i % 2 === 0) continue; for (let u = 0; u <= 1; u += 0.05) put(g, ay + (by - ay) * u, ax + (bx - ax) * u, MUD[t > 0.7 ? 1 : 2]); } }
    spike(g, x0, y0, x1, y1, 3.6, BONE);
  }

  // --- 皮が裂けて骨が覗く所（胴の右・左）---
  const tear = (tx, ty, rx, ry, n, ang) => {
    for (let y = ty - ry - 2; y <= ty + ry + 2; y++) for (let x = tx - rx - 2; x <= tx + rx + 2; x++) {
      const d = ((x - tx) / rx) ** 2 + ((y - ty) / ry) ** 2 + (hash(x >> 1, y >> 1) - 0.5) * 0.2;
      if (d < 1) put(g, y, x, WAT[d > 0.7 || x + y < tx + ty - 6 ? 0 : 1]);
      else if (d < 1.25 && g[y]?.[x] >= 0) put(g, y, x, MUD[x + y < tx + ty ? 3 : 1]);
    }
    for (let i = 0; i < n; i++) { const yy = ty - ry + 3 + (i + 0.5) * (2 * ry - 6) / n; tube(g, [[tx - rx + 3, yy - 3 * ang, 2.6], [tx, yy + 2, 3], [tx + rx - 3, yy - 3 * ang + 1, 2.4]], BONE, { ambient: 0.2 }); }
  };
  tear(236, 128, 9, 22, 4, 0.3); tear(28, 118, 7, 18, 3, -0.3);
  // 胸に近いひびが、うっすら核の色に光る
  for (let y = 120; y < 240; y++) for (let x = 40; x < 220; x++) { const k = g[y][x]; if (k !== MUD[0]) continue; const d = Math.hypot(x - 128, (y - 194) * 1.15); if (d < 78 && hash(x, y) < 0.9 * (1 - d / 78)) put(g, y, x, CORE[d < 40 ? 1 : 0]); }

  // --- 胸のあばら骨の空洞（黒い水と核）---
  const cx = 128, cy = 192;
  for (let y = 160; y < 226; y++) for (let x = 56; x < 202; x++) {
    const n = ((x - cx) / 64) ** 2 + ((y - cy) / 29) ** 2;
    if (n > 1) continue;
    put(g, y, x, WAT[n > 0.8 || y > cy + 20 ? 0 : (x + y * 0.6 < cx + cy * 0.6 - 14 && n < 0.62 ? 1 : 0)]);
  }
  for (let y = 156; y < 230; y++) for (let x = 54; x < 204; x++) {
    const n = ((x - cx) / 64) ** 2 + ((y - cy) / 29) ** 2;
    if (n > 1 && n < 1.2 && g[y][x] >= 0) put(g, y, x, MUD[y < cy - 8 || x < cx - 24 ? 3 : n < 1.1 ? 1 : 0]);
  }
  // 核（黒い水の底で光る。小さめ、ひびわれた宝玉）
  paintField(g, heightField([{ cx: 128, cy: 196, rx: 12, ry: 11, h: 1 }], 6), CORE, { ambient: 0.35, gain: 0.9, tex: (x, y) => (Math.abs((x - 128) * 0.7 + (y - 196)) < 0.7 ? -0.35 : 0) });
  for (let a = 0; a < 6.283; a += 0.03) for (const rr of [14, 15.5]) { const x = Math.round(128 + Math.cos(a) * rr), y = Math.round(196 + Math.sin(a) * rr * 0.92); if (g[y]?.[x] >= 0 && WAT.includes(g[y][x])) put(g, y, x, WAT[rr === 14 ? 2 : 1]); }
  // 背骨（湾曲した胴の上端を走る骨の節）とあばら骨
  const spineY = (x) => 151 + 12 * Math.sin((x - 56) / 146 * Math.PI);
  const ribs = [[70, -8, 46], [84, -5, 52], [99, -3, 40], [114, -1, 50], [143, 1, 48], [158, 3, 40], [172, 5, 52], [187, 8, 44]];
  for (const [rx, lean, len] of ribs) {
    const ry = spineY(rx);
    tube(g, [[rx, ry, 4.4], [rx + lean * 0.5, ry + len * 0.35, 4.2], [rx + lean * 1.3, ry + len * 0.7, 3], [rx + lean * 1.7, ry + len, 1.4]], BONE, { ambient: 0.2, tex: (x, y) => (hash(x >> 1, y >> 1) < 0.09 ? -0.1 : 0) });
  }
  for (let x = 58; x <= 198; x += 7.5) ellipsoid(g, x, spineY(x), 4.9, 4.2, BONE, { ambient: 0.22 });
  for (let x = 62; x <= 194; x += 7.5) { put(g, spineY(x) + 5, x, BONE[0]); put(g, spineY(x) + 5, x + 1, BONE[0]); }

  // --- 黒い水の滴り（あばらの隙間から足元へ）---
  for (const [dx, top, len, wd] of [[76, 212, 26, 2], [92, 218, 22, 1], [108, 222, 14, 1], [122, 224, 16, 3], [137, 224, 14, 1], [151, 222, 16, 3], [166, 222, 16, 1], [180, 218, 22, 2], [194, 212, 24, 1]]) {
    for (let y = top; y < top + len; y++) { const w = wd * (y < top + len - 5 ? 1 : 0.5); for (let x = -w; x <= w; x += 1) { const px = Math.round(dx + x + Math.sin(y * 0.2 + dx) * 0.6); put(g, y, px, x < 0 ? WAT[3] : x > 0 ? WAT[0] : WAT[wd > 1 ? 2 : 1]); } }
    if (len > 14) ellipsoid(g, dx, top + len + 3, 2.6 + wd * 0.4, 3.2, WAT, { ambient: 0.35 });
  }
  // 足元の黒い水たまり
  paintField(g, heightField([{ cx: 128, cy: 241, rx: 92, ry: 8 }, { cx: 78, cy: 244, rx: 40, ry: 7 }, { cx: 180, cy: 240, rx: 44, ry: 7 }, { cx: 128, cy: 247, rx: 50, ry: 5 }], 4), WAT, { ambient: 0.4, gain: 0.3, tex: (x, y) => (hash(x >> 2, y >> 1) < 0.12 ? -0.15 : 0) });
  for (const [px, py, w] of [[70, 238, 12], [100, 241, 10], [150, 239, 14], [184, 242, 10], [126, 245, 16]]) for (let x = -w; x <= w; x++) put(g, py, px + x, WAT[3]);
  for (const [px, py] of [[92, 239], [138, 243], [170, 237]]) for (let d = 0; d < 4; d++) put(g, py, px + d, CORE[2]);

  // --- 頭（骨と泥のまだらな頭蓋、開いた顎）---
  const sk = heightField([{ cx: 118, cy: 52, rx: 24, ry: 21, h: 1 }, { cx: 148, cy: 58, rx: 32, ry: 13, h: 0.9 }, { cx: 178, cy: 62, rx: 22, ry: 9, h: 0.9 }], 5);
  // 下あご（開いて垂れる）
  tube(g, [[122, 76, 9], [146, 92, 8], [172, 100, 6], [196, 98, 3.4]], BONE, { ambient: 0.2, tex: (x, y) => (hash(x >> 1, y >> 1) < 0.07 ? -0.1 : 0) });
  // 口の闇（黒い水が満ちる）
  for (let y = 62; y < 98; y++) for (let x = 128; x < 202; x++) { const top = 66 + (x - 128) * 0.02, bot = 72 + (x - 128) * 0.34 - (x - 128) * (x - 128) * 0.0009; if (y > top && y < bot && x < 200 - (y - 62) * 0.15) put(g, y, x, WAT[y < top + 3 ? 0 : (x + y) % 11 === 0 ? 2 : 1]); }
  paintField(g, sk, BONE, { ambient: 0.22, tex: (x, y, l) => { const v = vor(x, y, 11); return (v.e < 1.1 ? -0.5 : 0) + (hash(v.id, 3) < 0.35 ? -0.12 : 0) + (hash(x >> 1, y >> 1) < 0.05 ? -0.08 : 0); } });
  // 頭のうえの泥のこびりつき（骨にひび割れた泥が残る）
  paintField(g, heightField([{ cx: 108, cy: 40, rx: 14, ry: 10, h: 1 }, { cx: 128, cy: 46, rx: 10, ry: 8 }], 5), MUD, { ambient: 0.25, tex: mudTex(8, 1.2), box: [90, 26, 150, 66] });
  // 牙（上）
  for (let i = 0; i < 8; i++) { const x = 152 + i * 6, yb = 68 + i * 0.5; spike(g, x, yb - 1, x - 1, yb + 7 + (i % 2) * 3, 2.3, BONE); }
  // 牙（下）
  for (let i = 0; i < 6; i++) { const x = 140 + i * 9, yb = 91 + i * 1.8 - (i > 3 ? 4 : 0) + 5; spike(g, x, yb + 3, x + 1, yb - 8 - (i % 2) * 3, 2.3, BONE); }
  // 眼窩（黒い穴に核と同じ光）
  ellipsoid(g, 130, 47, 9.5, 8, WAT, { ambient: 0.1 });
  ellipsoid(g, 130, 48, 5.6, 4.6, CORE, { ambient: 0.55, gain: 0.7 });
  put(g, 46, 128, CORE[3]); put(g, 46, 129, CORE[3]); put(g, 47, 128, CORE[3]);
  // 鼻孔
  for (const [x, y] of [[192, 58], [193, 58]]) put(g, y, x, WAT[0]);
  // 口からこぼれる黒い水
  for (let y = 98; y < 120; y++) for (let x = -1; x <= 1; x++) put(g, y, 176 + x + Math.round(Math.sin(y * 0.3)), x < 0 ? WAT[2] : WAT[1]);
  ellipsoid(g, 176, 123, 3, 3.5, WAT, { ambient: 0.3 });

  despeckle(g, 2);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M1-水涸れの歪み", g)]; })();
