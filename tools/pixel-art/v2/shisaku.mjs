// 試作機の歪み（第6章のボス・v2）: 雪原の戦跡の施設にあった、人造の歪み発生装置。凍りついた装甲、露出した歯車と割れた結晶の核、重戦車のような脚。
import { createPalette, makeGrid, heightField, paintField, ellipsoid, limb, bezier, outline, despeckle, groundShadow, eye, hash, put, clamp, smoothstep, W, toPieceFile } from "./lib2.mjs";

const LW = (() => { const v = [-0.55, -0.83]; const n = Math.hypot(...v); return v.map((x) => x / n); })();

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#090b14"), RIM = pal.rgb("縁明", "#2a3a58"), SHD = pal.rgb("影", "#111522");
  const STEEL = pal.ramp("鋼", 214, 0.2, 5, 0.09, 0.68);
  const ICE = pal.ramp("氷", 192, 0.55, 4, 0.3, 0.9);
  const BRASS = pal.ramp("真鍮", 34, 0.55, 4, 0.14, 0.62);
  const CORE = pal.ramp("結晶", 306, 0.8, 4, 0.3, 0.82);
  const g = makeGrid();
  const inSteel = (k) => STEEL.includes(k);

  // 面取りした板の高さ場（cut は角を斜めに落とす大きさ、b は縁の幅）
  const plate = (x0, y0, x1, y1, b = 4, cut = 0) => (x, y) => {
    if (x < x0 || x > x1 || y < y0 || y > y1) return 0;
    let d = Math.min(x - x0, x1 - x, y - y0, y1 - y);
    if (cut) { d = Math.min(d, (x - x0 + y - y0 - cut) * 0.7, (x1 - x + y - y0 - cut) * 0.7, (x - x0 + y1 - y - cut) * 0.7, (x1 - x + y1 - y - cut) * 0.7); }
    return d < 0 ? 0 : Math.max(0.03, Math.min(1, d / b));
  };
  const steelTex = (y0, y1, seam = 0) => (x, y) => -((y - y0) / (y1 - y0)) * 0.16 + (hash(x >> 1, y >> 1) - 0.5) * 0.1 + (seam && (x % seam === 0) ? -0.3 : 0);
  const paintPlate = (x0, y0, x1, y1, b = 4, cut = 0, o = {}) => paintField(g, plate(x0, y0, x1, y1, b, cut), STEEL, { ambient: 0.22, gain: 0.9, box: [x0 - 1, y0 - 1, x1 + 2, y1 + 2], tex: steelTex(y0, y1, o.seam || 0), ...o });

  // ---- 歯車 ----
  function gear(cx, cy, R, teeth, ramp, rot = 0, clip = null) {
    const n = ramp.length;
    for (let y = Math.floor(cy - R - 2); y <= cy + R + 2; y++) for (let x = Math.floor(cx - R - 2); x <= cx + R + 2; x++) {
      if (clip && !clip(x, y)) continue;
      const dx = x - cx, dy = y - cy, r = Math.hypot(dx, dy), a = Math.atan2(dy, dx) + rot;
      const tw = (((a * teeth) / (2 * Math.PI)) % 1 + 1) % 1, Ro = tw < 0.5 ? R : R * 0.84; if (r > Ro) continue;
      const sp = (((a * 5) / (2 * Math.PI)) % 1 + 1) % 1; if (r > R * 0.36 && r < R * 0.66 && sp > 0.14 && sp < 0.86) continue;
      let lum;
      if (r < R * 0.16) lum = 0.08;
      else if (r < R * 0.24) lum = 0.5 + 0.4 * clamp(-(dx * LW[0] + dy * LW[1]) / r, -1, 1) * -1;
      else if (Math.abs(r - R * 0.7) < 1.1) lum = 0.1;
      else { const rim = smoothstep(Ro - 3, Ro, r); lum = 0.5 + 0.45 * rim * clamp(-(dx * LW[0] + dy * LW[1]) / Math.max(1, r), -1, 1) + (hash(x >> 1, y >> 1) - 0.5) * 0.1; if (r > Ro - 1.2 && (dx * LW[0] + dy * LW[1]) > 0) lum = 0.12; }
      put(g, y, x, ramp[clamp(Math.floor(lum * n), 0, n - 1)]);
    }
  }
  // 氷の結晶（先のとがった柱）
  function shard(x, y, h, w, lean = 0) {
    for (let j = 0; j < h; j++) {
      const t = j / h, half = w * (1 - t) * 0.5 + (j === h - 1 ? 0 : 0.5), cxx = x + lean * t;
      for (let i = -Math.ceil(half); i <= Math.ceil(half); i++) {
        if (Math.abs(i) > half) continue;
        const left = i < -half * 0.15, idx = left ? (j < h * 0.4 ? 3 : 2) : i > half * 0.5 ? 0 : 1;
        put(g, y - j, cxx + i, ICE[idx]);
      }
    }
  }

  groundShadow(g, 128, 245, 108, 9, SHD);

  // ---- 脚（重戦車のような履帯の足）----
  const leg = (mx) => {
    const X = (x) => (mx ? 256 - x : x);
    const bx = (x0, x1) => (mx ? [256 - x1, 256 - x0] : [x0, x1]);
    // 上の太い柱
    { const [a, b] = bx(32, 90); paintPlate(a, 146, b, 214, 5, 12, { seam: 0 }); }
    // 履帯の足
    const [t0, t1] = bx(10, 100);
    paintField(g, heightField(Array.from({ length: 8 }, (_, i) => ({ cx: t0 + 14 + i * ((t1 - t0 - 28) / 7), cy: 222, rx: 16, ry: 17 })), 5), STEEL, { ambient: 0.16, gain: 0.8, box: [t0 - 2, 200, t1 + 3, 245], tex: (x, y) => -0.1 + (hash(x >> 1, y >> 1) - 0.5) * 0.08 });
    // 履帯の継ぎ目（上下の縁）
    for (let x = t0; x <= t1; x++) {
      let top = -1, bot = -1; for (let y = 200; y < 244; y++) if (inSteel(g[y][x])) { if (top < 0) top = y; bot = y; }
      if (top < 0) continue;
      if (x % 4 < 2) for (let k = 0; k < 4; k++) { if (inSteel(g[top + k][x])) put(g, top + k, x, STEEL[k < 1 ? 4 : 0]); if (inSteel(g[bot - k][x])) put(g, bot - k, x, STEEL[0]); }
    }
    // 転輪
    for (let i = 0; i < 4; i++) { const wx = t0 + 20 + i * ((t1 - t0 - 40) / 3); ellipsoid(g, wx, 224, 10, 10, STEEL, { ambient: 0.2, gain: 1.1 }); ellipsoid(g, wx, 224, 4, 4, BRASS, { ambient: 0.3 }); for (let a = 0; a < 6.28; a += 0.13) put(g, 224 + Math.sin(a) * 10.5, wx + Math.cos(a) * 10.5, STEEL[0]); }
    // 膝の歯車
    gear(X(60), 190, 13, 10, BRASS, mx ? 0.3 : 0);
  };
  leg(false); leg(true);

  // ---- 胴（重ねた装甲板）----
  paintPlate(46, 88, 210, 182, 5, 16, { seam: 0 });
  paintPlate(70, 62, 186, 96, 4, 12);
  // 肩の丸い装甲
  paintField(g, heightField([{ cx: 44, cy: 112, rx: 28, ry: 32 }], 5), STEEL, { ambient: 0.22, box: [12, 76, 76, 148], tex: steelTex(80, 144) });
  paintField(g, heightField([{ cx: 212, cy: 112, rx: 28, ry: 32 }], 5), STEEL, { ambient: 0.22, box: [180, 76, 244, 148], tex: steelTex(80, 144) });
  // 頭（操縦室）と排気筒
  paintPlate(102, 34, 154, 76, 4, 10);
  paintPlate(78, 26, 94, 70, 3, 3); paintPlate(162, 26, 178, 70, 3, 3);
  for (const px of [86, 170]) { for (let x = px - 7; x <= px + 7; x++) for (let y = 22; y <= 30; y++) { const d = ((x - px) / 7.5) ** 2 + ((y - 26) / 3.4) ** 2; if (d < 1) put(g, y, x, d < 0.6 ? OUT : STEEL[1]); } }
  // 排気の冷たい煙
  for (const [px, s] of [[86, 1], [170, 2]]) paintField(g, heightField([{ cx: px - 4, cy: 14, rx: 10, ry: 8 }, { cx: px + 6, cy: 6, rx: 12, ry: 6 }, { cx: px - 10, cy: 4, rx: 7, ry: 4 }], 4), STEEL.slice(1, 4), { ambient: 0.4, box: [px - 24, 0, px + 24, 24], tex: (x, y) => (hash((x >> 1) + s, y >> 1) - 0.5) * 0.4 });

  // ---- 開いた胸（歯車と割れた結晶の核）----
  const CX = 128, CY = 132, RX = 48, RY = 42;
  const cav = (x, y) => ((x - CX) / (RX - 2)) ** 2 + ((y - CY) / (RY - 2)) ** 2 <= 1;
  for (let y = CY - RY - 6; y <= CY + RY + 6; y++) for (let x = CX - RX - 6; x <= CX + RX + 6; x++) {
    const dx = x - CX, dy = y - CY, d = (dx / RX) ** 2 + (dy / RY) ** 2;
    if (d <= 1) put(g, y, x, d < 0.8 ? SHD : STEEL[0]);
    else if (d < 1.3) {
      const r = Math.hypot(dx, dy), rr = (Math.sqrt(d) - 1) / 0.14, nr = (0.5 - Math.abs(rr - 0.5)) * 2 * (rr < 0.5 ? -1 : 1);
      const lum = 0.5 + 0.45 * clamp(-(dx / r * LW[0] + dy / r * LW[1]) * (rr < 0.5 ? 1 : -0.6) * 1.0, -1, 1);
      put(g, y, x, STEEL[clamp(Math.floor(lum * 5), 0, 4)]);
    }
  }
  const dark = BRASS.slice(0, 3);
  gear(CX, CY - 4, 36, 18, [STEEL[0], STEEL[1], STEEL[2]], 0.1, cav);
  gear(CX - 30, CY + 16, 21, 12, BRASS, 0.2, cav);
  gear(CX + 32, CY + 12, 17, 10, dark, 0.05, cav);
  gear(CX + 28, CY - 30, 11, 8, BRASS, 0.4, cav);
  // 結晶（面ごとに光を変えた六角の柱）
  {
    const V = [[128, 96], [149, 112], [147, 148], [128, 166], [109, 148], [107, 112]];
    const C = [128, 132];
    const inTri = (px, py, a, b, c) => { const s = (p, q, r) => (p[0] - r[0]) * (q[1] - r[1]) - (q[0] - r[0]) * (p[1] - r[1]); const P = [px, py], d1 = s(P, a, b), d2 = s(P, b, c), d3 = s(P, c, a); return !((d1 < 0 || d2 < 0 || d3 < 0) && (d1 > 0 || d2 > 0 || d3 > 0)); };
    for (let y = 94; y <= 168; y++) for (let x = 104; x <= 152; x++) {
      for (let i = 0; i < 6; i++) {
        const a = V[i], b = V[(i + 1) % 6]; if (!inTri(x, y, a, b, C)) continue;
        const ex = b[0] - a[0], ey = b[1] - a[1], ln = Math.hypot(ex, ey), nx = ey / ln, ny = -ex / ln; // 外向き法線
        const lum = 0.5 + 0.5 * clamp(nx * LW[0] + ny * LW[1], -1, 1);
        const dist = Math.hypot(x - C[0], y - C[1]);
        let idx = clamp(Math.floor(lum * 3.6 + (1 - dist / 40) * 0.6), 0, 3);
        put(g, y, x, CORE[idx]); break;
      }
    }
    // 面の稜線（明るい線）
    for (let i = 0; i < 6; i++) { const a = V[i]; for (let t = 0; t <= 1; t += 0.02) { put(g, C[1] + (a[1] - C[1]) * t, C[0] + (a[0] - C[0]) * t, i < 2 || i === 5 ? CORE[3] : CORE[1]); } }
    for (let i = 0; i < 6; i++) { const a = V[i], b = V[(i + 1) % 6]; for (let t = 0; t <= 1; t += 0.02) put(g, a[1] + (b[1] - a[1]) * t, a[0] + (b[0] - a[0]) * t, (i === 5 || i === 0) ? CORE[3] : OUT); }
    // 割れ目（暗い亀裂＋欠け）
    let x = 122, y = 100; for (let i = 0; i < 64; i++) { x += hash(i, 31) < 0.45 ? 1 : hash(i, 32) < 0.5 ? -1 : 0; y += 1; put(g, y, x, OUT); put(g, y, x + 1, CORE[0]); }
    for (let yy = 138; yy < 152; yy++) for (let xx = 130; xx < 130 + (yy - 138) * 1.1; xx++) if (xx < 146) put(g, yy, xx, OUT);
    for (let i = 0; i < 12; i++) put(g, 138 + i, 130 + Math.round(i * 1.1), CORE[3]);
    // 割れて浮く結晶片
    for (const [sx, sy, w, h] of [[160, 106, 4, 8], [96, 160, 3, 6]]) for (let j = -h; j <= h; j++) for (let i = -w; i <= w; i++) { const d = Math.abs(i) / w + Math.abs(j) / h; if (d <= 1 && cav(sx + i, sy + j)) put(g, sy + j, sx + i, i < 0 ? CORE[j < 0 ? 3 : 2] : CORE[1]); }
  }
  // 結晶の光（暗がりに市松のにじみ）
  for (let y = 84; y <= 180; y++) for (let x = 84; x <= 172; x++) { if (g[y][x] !== SHD && g[y][x] !== STEEL[1]) continue; const d = Math.hypot((x - 128) / 26, (y - 132) / 38); if (d > 1 && d < 1.45 && (x + y) % 2 === 0 && cav(x, y)) put(g, y, x, CORE[d < 1.2 ? 1 : 0]); }

  // ---- 装甲の細部 ----
  // 警告の縞（下の帯）
  for (let y = 168; y <= 178; y++) for (let x = 62; x <= 194; x++) if (inSteel(g[y][x]) && !cav(x, y)) put(g, y, x, ((x + y) >> 2) % 2 ? BRASS[2] : OUT);
  // 継ぎ目とリベット
  for (const sx of [70, 186]) for (let y = 98; y <= 166; y++) if (inSteel(g[y][sx]) && !cav(sx, y)) { put(g, y, sx, STEEL[0]); put(g, y, sx + 1, STEEL[3]); }
  for (let x = 52; x <= 204; x++) if (inSteel(g[100][x]) && !cav(x, 100)) { put(g, 100, x, STEEL[0]); put(g, 101, x, STEEL[3]); }
  for (const [rx, ry] of [[56, 96], [56, 174], [200, 96], [200, 174], [78, 108], [178, 108], [78, 160], [178, 160], [110, 44], [146, 44], [110, 68], [146, 68], [86, 78], [170, 78], [44, 100], [44, 126], [212, 100], [212, 126]]) if (inSteel(g[ry][rx])) { put(g, ry, rx, STEEL[4]); put(g, ry, rx + 1, STEEL[0]); put(g, ry + 1, rx + 1, STEEL[0]); }
  // 頭の視線（割れた光る目）
  for (let y = 48; y <= 62; y++) for (let x = 108; x <= 148; x++) { const d = ((x - 128) / 19) ** 2 + ((y - 55) / 6) ** 2; if (d < 1 && inSteel(g[y][x])) put(g, y, x, d > 0.7 ? STEEL[0] : OUT); }
  eye(g, 128, 55, 13, 5, [CORE[1], CORE[2], CORE[3]], OUT, 0);
  // 装甲の亀裂（結晶の光が漏れる）
  const crack = (sx, sy, dx, dy, n, sd) => { let x = sx, y = sy; for (let i = 0; i < n; i++) { x += dx * (hash(i, sd) < 0.55 ? 1 : 0); y += dy * (hash(i, sd + 1) < 0.7 ? 1 : 0) + (dy === 0 ? (hash(i, sd + 2) < 0.5 ? 1 : -1) * (hash(i, sd + 3) < 0.4 ? 1 : 0) : 0); if (inSteel(g[Math.round(y)]?.[Math.round(x)])) { put(g, y, x, CORE[2]); put(g, y + 1, x, OUT); } } };
  crack(76, 132, -1, 0, 28, 3); crack(182, 128, 1, 0, 26, 7); crack(112, 172, 0, 1, 10, 11); crack(158, 94, 1, -1, 12, 13);
  // 露出した太い配管・ケーブル
  for (const [x1, y1, x2, y2, bend] of [[74, 150, 52, 204, -18], [182, 150, 204, 204, 18]]) limb(g, bezier([x1, y1], [x1 + bend, (y1 + y2) / 2], [x2, y2]), 3, 2.5, BRASS, { ambient: 0.25 });
  // 胴の落とす影（脚の上）と、肩の継ぎ目
  for (let y = 183; y <= 194; y++) for (let x = 40; x <= 216; x++) { const k = g[y][x], i = STEEL.indexOf(k); if (i > 0 && (y < 190 || (x + y) % 2 === 0)) put(g, y, x, STEEL[Math.max(0, i - (y < 189 ? 2 : 1))]); }
  for (const pcx of [44, 212]) for (let a = 0; a < 6.283; a += 0.01) for (const [rr, kk] of [[0.62, 0], [0.66, 3]]) { const x = pcx + Math.cos(a) * 28 * rr, y = 112 + Math.sin(a) * 32 * rr; if (inSteel(g[Math.round(y)]?.[Math.round(x)]) && (Math.cos(a) * (pcx < 128 ? 1 : -1) < 0.55)) put(g, y, x, STEEL[kk]); }
  for (const [bx, by] of [[44, 112], [212, 112]]) ellipsoid(g, bx, by, 6, 6, BRASS, { ambient: 0.3 });

  // ---- 霜・雪と氷柱 ----
  const snap = g.map((r) => r.slice());
  for (let x = 0; x < W; x++) for (let y = 1; y < W - 1; y++) {
    if (!inSteel(snap[y][x]) || cav(x, y)) continue;
    const above = snap[y - 1][x]; if (above >= 0 && inSteel(above)) continue;
    const t = 2 + Math.floor(hash(x >> 1, y >> 2) * 3.4);
    for (let k = 0; k < t; k++) if (inSteel(snap[y + k]?.[x])) put(g, y + k, x, ICE[k === 0 ? 3 : k === 1 ? (hash(x, y) < 0.5 ? 3 : 2) : 1]);
  }
  for (let x = 6; x < W - 6; x++) for (let y = 1; y < W - 8; y++) {
    if (!inSteel(snap[y][x]) || cav(x, y) || snap[y + 1][x] >= 0 || (x % 5 !== Math.floor(hash(x, 5) * 5) % 5)) continue;
    const len = 3 + Math.floor(hash(x, y) * 9); if (hash(x >> 2, y) > 0.62) continue;
    for (let k = 1; k <= len; k++) { put(g, y + k, x, ICE[k < len * 0.6 ? 2 : 3]); if (k < len * 0.45) put(g, y + k, x + 1, ICE[1]); }
    break;
  }
  // 肩・頭の氷の結晶
  shard(30, 88, 26, 9, -4); shard(42, 84, 34, 10, -2); shard(54, 90, 20, 8, 3); shard(206, 86, 30, 10, 3); shard(220, 92, 22, 8, 4); shard(190, 68, 16, 7, 2); shard(112, 36, 14, 6, -2); shard(24, 148, 12, 6, -3); shard(236, 150, 14, 6, 3);

  despeckle(g);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M6-試作機の歪み", g)]; })();
