// 積荷の歪み（第2章のボス・v2）: 密輸倉庫の木箱と縄と荷車の車輪が寄り集まって蜘蛛の形になった怪物。箱の口から、灯り石の目がいくつも覗く。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, outline, despeckle, groundShadow, eye, hash, put, clamp, smoothstep, W, toPieceFile } from "./lib2.mjs";

const idx = (ramp, t) => ramp[clamp(Math.floor(t * ramp.length), 0, ramp.length - 1)];
const LX = -0.6, LY = -0.8; // 光の向き（左上へ向かう）

/** 木箱。前の面・上の面・右の面。ang は傾き（ラジアン）。 */
function crate(g, cx, cy, w, h, d, ang, WOOD, IRON, seed = 1, brace = true, dim = 0, straps = []) {
  const c = Math.cos(ang), s = Math.sin(ang), R = Math.hypot(w / 2 + d * 1.2, h / 2 + d) + 3;
  const nb = Math.max(2, Math.round(h / 8));
  for (let y = Math.floor(cy - R); y <= cy + R; y++) for (let x = Math.floor(cx - R); x <= cx + R; x++) {
    const dx = x - cx, dy = y - cy, u = dx * c + dy * s, v = -dx * s + dy * c;
    let tone = -1;
    if (Math.abs(u) <= w / 2 && Math.abs(v) <= h / 2) {
      const v01 = (v + h / 2) / h, pid = Math.min(nb - 1, Math.floor(v01 * nb)), pv = (v01 * nb) % 1, pw = h / nb;
      tone = 0.44 + (hash(pid, seed) - 0.5) * 0.22 + 0.16 * (1 - v01) - 0.14 * (u / w + 0.5);
      tone += (hash(Math.floor((u + 300) / 5), pid + seed * 7) - 0.5) * 0.1; // 木目
      if (pv * pw < 1.1) tone = 0.08; // 板の継ぎ目
      const su = hash(pid, seed + 5) * 0.6 + 0.2; if (Math.abs((u + w / 2) / w - su) < 0.6 / w && pv * pw > 1.1) tone = 0.1; // 板の継ぎ目（縦）
      const eu = u + w / 2, ev = v + h / 2, ex = w - eu, ey = h - ev, m = Math.min(eu, ev, ex, ey);
      if (m < 4.2) { // 枠板
        tone = 0.56 + (hash(seed, Math.floor(u / 6)) - 0.5) * 0.12;
        if (Math.min(eu, ev) < 1.2) tone = 0.82; else if (Math.min(ex, ey) < 1.2) tone = 0.1; else if (m > 3.2) tone = 0.16;
        else if (Math.min(eu, ev) < Math.min(ex, ey)) tone += 0.12; else tone -= 0.14;
      }
      if (brace) {
        const dg = Math.abs(u / w + v / h);
        if (dg < 0.075 && m > 3.2) { tone = dg < 0.012 || dg > 0.062 ? 0.12 : 0.62 + (hash(Math.floor(u / 4), seed) - 0.5) * 0.14; if (dg > 0.03 && dg < 0.062 && u < v) tone -= 0.06; }
      }
      let strapped = false;
      for (const sv of straps) { const dv = v - sv * h / 2; if (Math.abs(dv) < 3.6 && m > 1.2) { strapped = true; const rv = Math.abs(((u + 300) % 13) - 6.5) < 1.2 && Math.abs(dv) < 1.2; put(g, y, x, rv ? IRON[2] : dv < -2 ? IRON[2] : dv > 2 ? IRON[0] : IRON[1]); } }
      if (strapped) continue;
      // 釘
      for (const [nu, nv] of [[5.4, 5.4], [w - 5.4, 5.4], [5.4, h - 5.4], [w - 5.4, h - 5.4]]) { const q = Math.hypot(eu - nu, ev - nv); if (q < 1.3) { put(g, y, x, IRON[eu < w / 2 && ev < h / 2 ? 2 : eu < w / 2 || ev < h / 2 ? 1 : 0]); tone = -2; } }
      if (tone !== -2) put(g, y, x, idx(WOOD, tone - dim));
      continue;
    }
    const t = -h / 2 - v;
    if (t > 0 && t <= d && u >= -w / 2 + t * 0.8 && u <= w / 2 + t * 0.8) { // 上の面
      const uu = u - t * 0.8, edge = t > d - 1.2 || uu < -w / 2 + 1.2 || t < 1.2;
      let tt = 0.82 + (hash(Math.floor((uu + 300) / 4), Math.floor(t / 4) + seed) - 0.5) * 0.14; if (edge) tt = t < 1.2 ? 0.14 : 0.94; put(g, y, x, idx(WOOD, tt - dim * 0.8)); continue;
    }
    if (u > w / 2 && u <= w / 2 + d * 0.8) { // 右の面
      const t2 = (u - w / 2) / 0.8; if (v >= -h / 2 - t2 && v <= h / 2 - t2) { const vv = v + t2 + h / 2, pl = Math.floor(vv / (h / nb)); put(g, y, x, idx(WOOD, (vv % (h / nb) < 1.1 ? 0.02 : 0.24 + (hash(pl, seed + 9) - 0.5) * 0.12) + (u - w / 2 < 1.2 ? -0.08 : 0))); }
    }
  }
}
/** 線分にそった太い板（脚）。taper で先を細く。 */
function plank(g, x0, y0, x1, y1, w, WOOD, seed = 1, taper = 0) {
  const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy), ux = dx / len, uy = dy / len, nx = -uy, ny = ux;
  const sg = nx * LX + ny * LY, m = w / 2 + 2;
  for (let y = Math.floor(Math.min(y0, y1) - m); y <= Math.max(y0, y1) + m; y++) for (let x = Math.floor(Math.min(x0, x1) - m); x <= Math.max(x0, x1) + m; x++) {
    const px = x - x0, py = y - y0, a = px * ux + py * uy, b = px * nx + py * ny, t = a / len;
    if (a < 0 || a > len) continue;
    const hw = (w / 2) * (1 - taper * t); if (Math.abs(b) > hw) continue;
    const sn = b / hw; // -1..1
    let tone = 0.5 - sg * sn * 0.36 + (hash(Math.floor(b + 50), Math.floor(a / 9) + seed) - 0.5) * 0.14;
    if (Math.abs(sn) > 0.8) tone += (sn * sg < 0 ? 0.16 : -0.22);
    if (Math.abs((a % 22) - 11) < 0.7 && Math.abs(sn) < 0.8) tone -= 0.3; // 板の継ぎ目・割れ
    if (a < 1.2 || (taper && a > len - 1.2)) tone = 0.12;
    put(g, y, x, idx(WOOD, tone));
  }
}
/** 荷車の車輪。輪・鉄の帯・ハブ・スポーク（抜けた所は透ける）。 */
function wheel(g, cx, cy, r, ry, spokes, WOOD, IRON, missing = [], rot = 0, rw = 0.2) {
  const k = ry / r;
  for (let y = Math.floor(cy - ry - 2); y <= cy + ry + 2; y++) for (let x = Math.floor(cx - r - 2); x <= cx + r + 2; x++) {
    const px = (x - cx), py = (y - cy) / k, d = Math.hypot(px, py); if (d > r) continue;
    const lit = -(px * LX + py * LY) / (d + 0.001); // 左上ほど正
    if (d > r - 1.6) { put(g, y, x, IRON[lit > 0.2 ? 2 : lit > -0.4 ? 1 : 0]); continue; } // 鉄の帯
    if (d > r * (1 - rw)) { const q = (d - r * (1 - rw)) / (r * rw); put(g, y, x, idx(WOOD, 0.46 + lit * 0.3 * (q > 0.5 ? 0.6 : 1) + (hash(x >> 1, y >> 1) - 0.5) * 0.1 - (q < 0.15 ? 0.3 : 0))); continue; }
    if (d < r * 0.2) { put(g, y, x, d < r * 0.09 ? IRON[0] : IRON[lit > 0.1 ? 2 : 1]); continue; }
    // スポーク
    for (let i = 0; i < spokes; i++) {
      if (missing.includes(i)) continue;
      const a = rot + i * 6.2832 / spokes, sx = Math.cos(a), sy = Math.sin(a), along = px * sx + py * sy, across = -px * sy + py * sx;
      if (along > 0 && Math.abs(across) < 2.1 - along / r * 0.5) { const sn = across / 2.2; put(g, y, x, idx(WOOD, 0.5 - (sx * LX * 0 + (-sy * LX + sx * LY)) * 0 - sn * (-sy * LX + sx * LY) * 0.5 + (Math.abs(sn) > 0.7 ? -0.14 : 0.06))); break; }
    }
  }
}
function rope(g, pts, r, ROPE, ph = 0) {
  // 縄。ななめのよりの模様
  const path = []; for (let i = 0; i < pts.length - 1; i++) for (let s = 0; s < 16; s++) path.push([pts[i][0] + (pts[i + 1][0] - pts[i][0]) * s / 16, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * s / 16]);
  const parts = path.map(([x, y]) => ({ cx: x, cy: y, rx: r, ry: r }));
  const xs = path.map((p) => p[0]), ys = path.map((p) => p[1]);
  paintField(g, heightField(parts, 4), ROPE, { ambient: 0.3, gain: 0.8, tex: (x, y) => (((x + y + ph) % 4) < 2 ? 0.14 : -0.12), box: [Math.floor(Math.min(...xs) - r - 2), Math.floor(Math.min(...ys) - r - 2), Math.ceil(Math.max(...xs) + r + 2), Math.ceil(Math.max(...ys) + r + 2)] });
}
function knot(g, x, y, r, ROPE) { paintField(g, heightField([{ cx: x, cy: y, rx: r, ry: r * 0.85 }], 5), ROPE, { ambient: 0.3, gain: 0.8, tex: (px, py) => (((px - py) % 4) < 2 ? 0.14 : -0.1), box: [Math.floor(x - r - 2), Math.floor(y - r - 2), Math.ceil(x + r + 2), Math.ceil(y + r + 2)] }); }

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0c0810"), RIM = pal.rgb("縁明", "#382a2c"), SHD = pal.rgb("影", "#161018");
  const WOOD = pal.ramp("木", 26, 0.42, 6, 0.07, 0.6, 30);
  const IRON = pal.ramp("鉄", 225, 0.14, 3, 0.12, 0.58);
  const ROPE = pal.ramp("縄", 42, 0.36, 4, 0.2, 0.68);
  const CLOTH = pal.ramp("幌", 352, 0.36, 4, 0.1, 0.44);
  const GLOW = pal.ramp("灯", 42, 0.95, 4, 0.3, 0.9, 20);
  const g = makeGrid();
  groundShadow(g, 128, 246, 116, 8, SHD);

  // --- 背後の大きな壊れ車輪（光背のように）---
  wheel(g, 128, 92, 84, 84, 10, WOOD, IRON, [2, 5, 6], 0.3, 0.15);

  // --- 脚（左右4本ずつ。板を縄でつなぐ）---
  const legs = [
    // [根元, ひざ, 足先, 足の種類]
    [[100, 108], [56, 50], [22, 92], "spike"], [[96, 124], [30, 104], [12, 168], "wheel"], [[100, 138], [26, 150], [20, 224], "spike"], [[108, 150], [56, 182], [50, 240], "wheel"],
    [[156, 108], [202, 44], [236, 88], "spike"], [[160, 124], [226, 100], [244, 160], "spike"], [[156, 138], [232, 146], [238, 222], "wheel"], [[148, 150], [200, 180], [210, 240], "spike"],
  ];
  legs.forEach(([a, k, f, kind], i) => {
    plank(g, a[0], a[1], k[0], k[1], 18, WOOD, 10 + i, 0.15);
    const tip = kind === "spike";
    plank(g, k[0], k[1], f[0], f[1], tip ? 15 : 12, WOOD, 30 + i, tip ? 0.85 : 0.2);
  });
  legs.forEach(([a, k, f, kind], i) => {
    if (kind === "wheel") { const wr = i === 1 ? 20 : i === 3 ? 19 : 20; wheel(g, f[0], f[1] - (i === 2 ? 0 : 0), wr, wr * 0.92, 8, WOOD, IRON, i % 2 ? [3] : [1, 6], i, 0.2); }
  });
  // 関節：縄の結び目と鉄の当て板
  legs.forEach(([a, k, f], i) => {
    const dx = f[0] - k[0], dy = f[1] - k[1], l = Math.hypot(dx, dy);
    rope(g, [[k[0] - 8 * (dy / l), k[1] + 8 * (dx / l) * 0 - 4], [k[0] + 8 * (dy / l), k[1] + 4]], 3, ROPE, i);
    knot(g, k[0], k[1], 10, ROPE);
    ellipsoid(g, k[0] + 1, k[1] - 1, 3, 3, IRON, { ambient: 0.3 });
    // 縄の垂れ
    const sx = a[0] < 128 ? -1 : 1;
    rope(g, [[k[0], k[1] + 6], [k[0] + sx * 2, k[1] + 16], [k[0] + sx * 5, k[1] + 24 + (i % 3) * 4]], 1.8, ROPE, i);
    // 縄の巻き（脚の途中）
    const mx = (a[0] + k[0]) / 2, my = (a[1] + k[1]) / 2;
    for (let q = -1; q <= 1; q += 2) rope(g, [[mx - 8, my - 2 + q * 3], [mx + 8, my + 4 + q * 3]], 1.6, ROPE, q);
  });

  // --- 胴：うしろの積み荷（腹部）---
  crate(g, 96, 80, 46, 40, 12, -0.12, WOOD, IRON, 3, true, 0.1, [0.5]);
  crate(g, 160, 76, 50, 46, 12, 0.1, WOOD, IRON, 4, true, 0.1, [-0.55]);
  crate(g, 128, 44, 56, 30, 10, 0.02, WOOD, IRON, 5, false, 0.12, [0.4]);
  // 幌（破れた布）: 上の箱からかぶさって垂れ、すそはぎざぎざ
  paintField(g, heightField([{ cx: 166, cy: 56, rx: 26, ry: 14, h: 0.9 }, { cx: 178, cy: 76, rx: 14, ry: 26, h: 0.8 }], 5), CLOTH, { ambient: 0.3, gain: 0.7, tex: (x, y) => Math.sin(x * 0.6) * 0.2 + (hash(x >> 2, y >> 2) < 0.05 ? -0.1 : 0), box: [140, 40, 200, 116] });
  for (let x = 150; x < 200; x++) { const cut = 90 + ((x * 7) % 11) + Math.floor((x % 9) / 3) * 4; for (let y = cut; y < 120; y++) if (CLOTH.includes(g[y][x])) g[y][x] = -1; }
  // 箱のすき間から漏れる灯
  for (const [x0, y0, x1, y1] of [[80, 92, 108, 90], [150, 96, 178, 98], [112, 32, 132, 34], [70, 70, 72, 84]]) for (let t = 0; t <= 1; t += 0.03) { const px = x0 + (x1 - x0) * t, py = y0 + (y1 - y0) * t; put(g, py, px, GLOW[t > 0.3 && t < 0.7 ? 2 : 1]); put(g, py + 1, px, GLOW[0]); }

  // --- 頭の箱（大きな口を開ける）---
  const hx = 128, hy = 144;
  crate(g, hx, hy, 104, 78, 14, 0, WOOD, IRON, 6, false, 0, [-0.86, 0.86]);
  // 口：ぎざぎざの歯（割れた板）と暗い口の中
  const mL = 84, mR = 172, mT = 121, mB = 171;
  for (let y = mT - 8; y <= mB + 8; y++) for (let x = mL - 2; x <= mR + 2; x++) { const u = Math.abs((x - 128) / 45); if (u > 1) continue; if (y >= mT + u * u * 14 - 1 && y <= mB - u * u * 12 + 1) put(g, y, x, OUT); }
  // 上の歯と下の歯（板の破片）
  for (let i = 0; i < 9; i++) { const x = mL + 4 + i * 9, u = Math.abs((x - 128) / 44), len = 12 + (i % 3) * 3 - u * 4, y0 = mT + u * u * 14 - 2; plank(g, x, y0, x + (i % 2 ? 1 : -1), y0 + len, 8, WOOD, 60 + i, 0.95); }
  for (let i = 0; i < 8; i++) { const x = mL + 8 + i * 9, u = Math.abs((x - 128) / 44), len = 10 + ((i + 1) % 3) * 4 - u * 4, y0 = mB - u * u * 12 + 2; plank(g, x, y0, x + (i % 2 ? -1 : 1), y0 - len, 8, WOOD, 80 + i, 0.95); }
  // 口の闇：歯のあいだの空きを黒く
  // 目（灯り石）
  const E3 = [GLOW[1], GLOW[2], GLOW[3]];
  eye(g, 128, 144, 9, 12, E3, OUT, 0);
  eye(g, 106, 149, 6, 8, E3, OUT, 0.12);
  eye(g, 151, 149, 6, 8, E3, OUT, -0.12);
  eye(g, 116, 162, 3, 4, E3, OUT, 0);
  eye(g, 141, 162, 3, 4, E3, OUT, 0);
  eye(g, 94, 142, 3, 3, E3, OUT, 0); eye(g, 162, 141, 3, 3, E3, OUT, 0);
  // 光のにじみ（歯の縁がほんのり暖色）
  for (let y = mT - 6; y < mB + 8; y++) for (let x = mL; x < mR; x++) { const k = g[y][x]; if (k < 0 || !WOOD.includes(k)) continue; const d = Math.hypot(x - 128, (y - 148) * 1.2); if (d < 30) { const i = WOOD.indexOf(k); if (hash(x, y) < 0.5 * (1 - d / 30) && i < 4) put(g, y, x, WOOD[Math.min(5, i + 2)]); } }

  // --- 胴の下：荷車の台と車軸 ---
  crate(g, 128, 198, 64, 28, 8, 0, WOOD, IRON, 7, true, 0.05, [0.0]);
  plank(g, 62, 206, 194, 206, 7, WOOD, 90, 0);
  // 胴をしばる縄
  rope(g, [[84, 112], [104, 170], [128, 178]], 2.4, ROPE, 0); rope(g, [[172, 112], [152, 170], [128, 178]], 2.4, ROPE, 2);
  rope(g, [[80, 150], [128, 176], [176, 150]], 2.2, ROPE, 1);
  knot(g, 128, 178, 6, ROPE);
  // 垂れる縄の端と、はみ出した荷
  for (const [x, y, l] of [[100, 208, 22], [116, 210, 16], [146, 210, 20], [160, 208, 14]]) rope(g, [[x, y], [x + 1, y + l * 0.5], [x - 2, y + l]], 1.7, ROPE, x);
  // 足元の散らばり（割れた箱・板）
  crate(g, 82, 240, 20, 14, 5, 0.3, WOOD, IRON, 11, false);
  crate(g, 176, 242, 24, 12, 5, -0.2, WOOD, IRON, 12, false);

  // 光は左上。右下ほど木を1段暗く（市松でなじませる）。目のまわりだけ暖色に明るく残す
  for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) {
    const k = g[y][x], i = WOOD.indexOf(k); if (i < 2) continue;
    const q = smoothstep(-30, 150, (x - 128) * 0.7 + (y - 130) * 0.9) * 1.5 + (hash(x, y) - 0.5) * 0.5 - (Math.hypot(x - 128, (y - 148) * 1.2) < 34 ? 0.5 : 0);
    if (q > 0.85) g[y][x] = WOOD[i - 1 - (q > 1.4 && i > 2 ? 1 : 0)];
  }
  despeckle(g, 2);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M2-積荷の歪み", g)]; })();
