// 予言の歪み（第5章のボス・v2）: 霧の断崖の神殿の予言碑が歪んだ怪物。文字を刻んだ石板の翼、無数の目、宙に浮く石の天使。
import { createPalette, makeGrid, heightField, paintField, bezier, limb, outline, despeckle, eye, hash, put, clamp, W, toPieceFile } from "./lib2.mjs";

const LW = (() => { const v = [-0.55, -0.83]; const n = Math.hypot(...v); return v.map((x) => x / n); })();

export function build() {
  const pal = createPalette();
  const OUT = pal.rgb("縁", "#0a0912"), RIM = pal.rgb("縁明", "#2c3550"), SHD = pal.rgb("影", "#141826");
  const STONE = pal.ramp("石", 226, 0.2, 5, 0.1, 0.7);
  const ROBE = pal.ramp("外套", 262, 0.3, 4, 0.08, 0.4);
  const GOLD = pal.ramp("金", 44, 0.85, 4, 0.3, 0.84);
  const CYAN = pal.ramp("刻印", 176, 0.75, 3, 0.34, 0.76);
  const FOG = pal.ramp("霧", 250, 0.22, 3, 0.2, 0.5);
  const EG = [GOLD[1], GOLD[2], GOLD[3]];
  const g = makeGrid();

  // ---- 石板（斜めの直方体。押し出しの厚み・縁のハイライト・刻印・ひび）----
  function slab(o) {
    const { x0, y0, deg, L, w, taper = 12, tipK = 0.6, ramp = STONE, seed = 1, runes = "wing", glowP = 0.4, cracks = 1, broken = false, ext = 4 } = o;
    const th = (deg * Math.PI) / 180, c = Math.cos(th), s = Math.sin(th);
    const lx = LW[0] * c + LW[1] * s, ly = -LW[0] * s + LW[1] * c;
    const hw = (u) => (w / 2) * (1 - tipK * clamp((u - (L - taper)) / taper, 0, 1));
    const loc = (x, y) => { const dx = x - x0, dy = y - y0; return [dx * c + dy * s, -dx * s + dy * c]; };
    const inside = (x, y) => {
      const [u, v] = loc(x, y); if (u < 0 || u > L || Math.abs(v) > hw(u)) return false;
      if (broken && u > L - 18 && hash(Math.floor(u / 3) + seed, Math.floor((v + 40) / 3)) < 0.55 * (u - (L - 18)) / 18 + (v > 0 ? 0.15 : -0.1)) return false;
      return true;
    };
    const R = L + w, bx0 = Math.max(0, Math.floor(x0 - R)), bx1 = Math.min(W - 1, Math.ceil(x0 + R)), by0 = Math.max(0, Math.floor(y0 - R)), by1 = Math.min(W - 1, Math.ceil(y0 + R));
    // 厚み（右下へ押し出した側面）
    for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
      if (inside(x, y)) continue;
      for (let t = 1; t <= ext; t++) if (inside(x - t, y - t)) { put(g, y, x, t === 1 ? ramp[1] : ramp[0]); break; }
    }
    // ひび
    const cr = Array.from({ length: cracks }, (_, i) => ({ v0: (hash(seed, i + 3) - 0.5) * w * 0.7, ua: hash(seed, i + 9) * L * 0.5, ub: L * (0.5 + hash(seed, i + 5) * 0.5), ph: hash(seed, i + 1) * 6 }));
    for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
      if (!inside(x, y)) continue;
      const [u, v] = loc(x, y), hwu = hw(u);
      // 縁のハイライト（光は左上）
      const cand = [[u, -1, 0], [L - u, 1, 0], [v + hwu, 0, -1], [hwu - v, 0, 1]];
      let best = cand[0]; for (const q of cand) if (q[0] < best[0]) best = q;
      let idx;
      const nd = best[1] * lx + best[2] * ly;
      if (best[0] < 2) idx = nd > 0.25 ? (best[0] < 1 ? 4 : 3) : nd < -0.25 ? (best[0] < 1 ? 0 : 1) : 2;
      else {
        const pos = (x - x0) * LW[0] + (y - y0) * LW[1];
        idx = Math.floor(2.25 + clamp(pos / (w * 1.3), -0.7, 0.7) * 1.3 + (hash(x >> 1, y >> 1) - 0.5) * 0.7);
        idx = clamp(idx, 1, 3);
      }
      for (const k of cr) if (u > k.ua && u < k.ub && Math.abs(v - (k.v0 + Math.sin(u * 0.28 + k.ph) * 2.2 + (u - k.ua) * 0.06)) < 0.55) idx = -1;
      put(g, y, x, idx < 0 ? ramp[0] : ramp[idx]);
    }
    // 刻印
    const glyph = (gu, sd) => {
      const bits = new Set(); const h = (n) => hash(gu * 7 + sd, n);
      const c1 = Math.floor(h(1) * 3), ra = Math.floor(h(2) * 2), rb = 3 + Math.floor(h(3) * 2);
      for (let r = ra; r <= rb; r++) bits.add(c1 * 5 + r);
      const r2 = Math.floor(h(4) * 5), ca = Math.floor(h(5) * 2), cb = 1 + Math.floor(h(6) * 2);
      for (let cc = Math.min(ca, cb); cc <= Math.max(ca, cb); cc++) bits.add(cc * 5 + r2);
      if (h(7) < 0.5) { const c3 = (c1 + 2) % 3; for (let r = 1; r <= 3; r++) bits.add(c3 * 5 + r); }
      return bits;
    };
    if (runes) for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
      if (!inside(x, y)) continue;
      const [u, v] = loc(x, y), hwu = hw(u); if (hwu - Math.abs(v) < 3) continue;
      let cu, fu, row, col;
      if (runes === "wing") {
        if (u < 7 || hwu < 6.5 || Math.abs(v) >= 5) continue;
        const q = u - 5; cu = Math.floor(q / 9); fu = q - cu * 9; if (fu >= 6) continue; col = Math.floor(fu / 2); row = Math.floor((v + 5) / 2);
      } else {
        const p = -v + 13.5; if (u < 10 || p < 0 || p >= 27 || hwu < 17) continue;
        const pc = Math.floor(p / 9), fp = p - pc * 9; if (fp >= 6) continue;
        const q = u - 10, qc = Math.floor(q / 14), fq = q - qc * 14; if (fq >= 10) continue;
        cu = qc * 3 + pc; col = Math.floor(fp / 2); row = Math.floor(fq / 2);
      }
      if (hash(cu, seed + 11) < 0.14) continue;
      if (!glyph(cu, seed).has(col * 5 + row)) continue;
      const glow = hash(cu, seed + 7) < glowP;
      put(g, y, x, glow ? CYAN[col === 0 ? 2 : 1] : ramp[0]);
    }
    return { pt: (u, v = 0) => [x0 + c * u - s * v, y0 + s * u + c * v] };
  }
  const E = (x, y, rx = 4, ry = 3, tilt = 0) => {
    x = Math.round(x); y = Math.round(y);
    if (rx >= 5) return eye(g, x, y, rx, ry, EG, OUT, tilt);
    for (let j = -ry - 1; j <= ry + 1; j++) for (let i = -rx - 1; i <= rx + 1; i++) {
      const d = (i / (rx + 1.2)) ** 2 + (j / (ry + 1.2)) ** 2; if (d > 1) continue;
      const dd = (i / rx) ** 2 + (j / ry) ** 2; put(g, y + j, x + i, dd > 1 ? OUT : dd < 0.25 ? EG[2] : EG[1]);
    }
    put(g, y, x, OUT); put(g, y - 1, x - 1, EG[2]);
  };

  // ---- 霧（足もと）----
  const fogParts = [];
  for (let i = 0; i < 14; i++) fogParts.push({ cx: 10 + i * 18 + (hash(i, 4) - 0.5) * 12, cy: 240 + (hash(i, 8) - 0.5) * 10 - (i % 3 === 0 ? 6 : 0), rx: 18 + hash(i, 2) * 16, ry: 9 + hash(i, 6) * 12 });
  paintField(g, heightField(fogParts, 4), FOG, { ambient: 0.45, gain: 0.7, thr: 0.05, box: [0, 214, W, 256], tex: (x, y) => (hash(x >> 1, y >> 1) - 0.5) * 0.14 });
  // 霧の上に漂う細い雲筋
  for (const [sx, sy, len] of [[20, 222, 26], [190, 226, 30], [96, 218, 18]]) for (let i = 0; i < len; i++) { put(g, sy + Math.round(Math.sin(i * 0.3) * 1.5), sx + i, FOG[2]); put(g, sy + 1 + Math.round(Math.sin(i * 0.3) * 1.5), sx + i, FOG[1]); }

  // ---- 光の輪（欠けた金の環）----
  {
    const cx = 128, cy = 58, r0 = 41, r1 = 50, LZ = 0.6, Ln = Math.hypot(0.5, 0.62, LZ);
    const gaps = [[0.25, 0.6], [2.4, 2.8], [-2.3, -2.15], [-0.75, -0.6], [1.2,1.35]];
    for (let y = cy - r1 - 1; y <= cy + r1 + 1; y++) for (let x = cx - r1 - 1; x <= cx + r1 + 1; x++) {
      const dx = x - cx, dy = y - cy, r = Math.hypot(dx, dy); if (r < r0 || r > r1) continue;
      const a = Math.atan2(dy, dx); if (gaps.some(([lo, hi]) => a > lo && a < hi)) continue;
      const p = (r - r0) / (r1 - r0), nr = (p - 0.5) * 2, nxr = (dx / r) * nr * 0.8, nyr = (dy / r) * nr * 0.8, nz = Math.sqrt(Math.max(0.05, 1 - nxr * nxr - nyr * nyr));
      let lum = (-nxr * 0.5 - nyr * 0.62 + nz * LZ) / Ln; lum = 0.28 + 0.72 * clamp(lum, 0, 1);
      let k = GOLD[clamp(Math.floor(lum * 4), 0, 3)];
      if (Math.round(a * 12) !== Math.round((a + 0.02) * 12) && r > r0 + 2 && r < r1 - 2) k = GOLD[0];
      put(g, y, x, k);
    }
  }

  // ---- 翼（左右6枚＋小さな板）----
  const degs = [232, 214, 198, 182, 166, 150], Ls = [64, 84, 90, 86, 74, 56];
  const wingSide = (mir, S) => {
    degs.forEach((d, i) => {
      const dd = mir ? 180 - d : d, r = (dd * Math.PI) / 180;
      const o = slab({ x0: S[0] + Math.cos(r) * 8, y0: S[1] + Math.sin(r) * 8, deg: dd, L: Ls[i], w: 22, taper: 14, tipK: 0.55, seed: 10 + i + (mir ? 20 : 0), glowP: 0.4, cracks: 2, broken: i % 2 === 0 });
      if (i === 1 || i === 3 || i === 5) { const [ex, ey] = o.pt(Ls[i] * 0.72); E(ex, ey, 5, 3, 0); }
    });
    [225, 205, 187, 168].forEach((d, i) => {
      const dd = mir ? 180 - d : d, r = (dd * Math.PI) / 180;
      const o = slab({ x0: S[0] + Math.cos(r) * 4, y0: S[1] + Math.sin(r) * 4, deg: dd, L: 40 - i * 3, w: 17, taper: 9, tipK: 0.5, seed: 50 + i + (mir ? 20 : 0), glowP: 0.5, cracks: 1 });
      if (i === 1) { const [ex, ey] = o.pt(26); E(ex, ey, 4, 3, 0); }
    });
  };
  wingSide(false, [98, 94]);
  wingSide(true, [158, 94]);
  // 浮かぶ欠片
  for (const [x, y, d, l, w] of [[16, 30, 200, 22, 10], [232, 32, 340, 22, 10], [8, 132, 168, 20, 9], [244, 134, 12, 20, 9], [34, 168, 130, 18, 9], [214, 172, 50, 18, 9], [70, 12, 250, 16, 8], [188, 14, 290, 16, 8]]) slab({ x0: x, y0: y, deg: d, L: l, w, taper: 8, tipK: 0.6, seed: Math.floor(x), runes: l > 18 ? "wing" : null, glowP: 0.5, cracks: 1, ext: 3 });

  // ---- 垂れる根（有機物）と鎖 ----
  for (const [x1, y1, bend, r0] of [[80, 232, -30, 9], [104, 246, -10, 8], [152, 246, 10, 8], [178, 232, 30, 9]]) {
    limb(g, bezier([128 + (x1 - 128) * 0.3, 190], [x1 + bend, 222], [x1, y1]), r0, 3, ROBE, { ambient: 0.22 });
    E(x1, y1 - 2, 3, 2);
  }
  for (const [sx, sy, dx] of [[62, 108, -1], [194, 108, 1]]) { const path = bezier([sx, sy], [sx + dx * 14, sy + 40], [sx + dx * 6, sy + 84], 14); path.forEach(([x, y], i) => { const h = i % 2 === 0; for (let a = -2; a <= 2; a++) for (let b = -1; b <= 1; b++) { const ring = h ? Math.abs(a) === 2 || Math.abs(b) === 1 : Math.abs(a) === 1 || Math.abs(b) === 1 && false; if (h ? (Math.abs(a) === 2 || Math.abs(b) === 1) : (Math.abs(b) === 1 && Math.abs(a) <= 1) || Math.abs(a) === 2 && false) put(g, y + b * 2, x + a, STONE[h ? 3 : 2]); } put(g, y, x, STONE[1]); }); }
  // ---- 外套の胴（後ろの暗い布）----
  paintField(g, heightField([{ cx: 128, cy: 108, rx: 54, ry: 28 }, { cx: 128, cy: 140, rx: 38, ry: 48 }, { cx: 128, cy: 176, rx: 26, ry: 44 }, { cx: 128, cy: 202, rx: 13, ry: 34 }], 5), ROBE, { ambient: 0.28, box: [60, 80, 200, 240], tex: (x, y) => Math.sin(x * 0.55 + Math.sin(y * 0.05) * 3) * 0.13 + (hash(x >> 1, y >> 1) - 0.5) * 0.08 });

  // ---- 髪のように垂れる板（頭の左右）----
  slab({ x0: 106, y0: 44, deg: 112, L: 52, w: 15, taper: 12, tipK: 0.7, seed: 71, runes: "wing", glowP: 0.6, cracks: 1 });
  slab({ x0: 150, y0: 44, deg: 68, L: 52, w: 15, taper: 12, tipK: 0.7, seed: 72, runes: "wing", glowP: 0.6, cracks: 1 });

  // ---- 頭（石の仮面）----
  paintField(g, heightField([{ cx: 128, cy: 62, rx: 24, ry: 28 }, { cx: 128, cy: 82, rx: 17, ry: 14 }], 5), STONE, { ambient: 0.3, box: [96, 28, 160, 102], tex: (x, y) => (hash(x >> 1, y >> 1) - 0.5) * 0.16 });
  // 眼窩と三つの目、額の目
  for (let y = 56; y <= 74; y++) for (let x = 105; x <= 151; x++) { const d = ((x - 128) / 26) ** 2 + ((y - 65) / 10) ** 2; if (d < 1 && g[y][x] >= 0) put(g, y, x, d > 0.8 ? STONE[0] : OUT); }
  E(128, 65, 10, 6); E(109, 68, 4, 3, 0); E(147, 68, 4, 3, 0); E(128, 45, 3, 4);
  // 口のような縦の刻み
  for (let y = 80; y < 92; y++) { put(g, y, 128, OUT); if (y % 3 === 0) { put(g, y, 127, STONE[0]); put(g, y, 129, STONE[0]); } }

  // ---- 肩の板と胸の予言碑 ----
  slab({ x0: 72, y0: 101, deg: 0, L: 56, w: 26, taper: 16, tipK: 0.4, seed: 81, runes: "wing", glowP: 0.35, cracks: 2, ext: 5 });
  slab({ x0: 184, y0: 101, deg: 180, L: 56, w: 26, taper: 16, tipK: 0.4, seed: 82, runes: "wing", glowP: 0.35, cracks: 2, ext: 5 });
  slab({ x0: 128, y0: 88, deg: 90, L: 126, w: 42, taper: 48, tipK: 0.86, seed: 91, runes: "stele", glowP: 0.62, cracks: 3, ext: 5, broken: false });
  for (let x = 112; x <= 144; x++) { put(g, 96, x, STONE[0]); put(g, 97, x, STONE[3]); put(g, 106, x, STONE[0]); put(g, 107, x, STONE[3]); }
  // 胸の目
  E(128, 118, 5, 4); E(113, 148, 4, 3); E(143, 156, 4, 3);
  // 外套の目（袖のあたり）
  E(82, 132, 5, 3); E(174, 130, 5, 3); E(96, 160, 4, 3); E(160, 158, 4, 3); E(112, 190, 3, 2); E(146, 194, 3, 2);

  // ---- 金の亀裂 ----
  const crack = (sx, sy, dx, n, sd) => { let x = sx, y = sy; for (let i = 0; i < n; i++) { x += dx * (hash(i, sd) < 0.6 ? 1 : 0); y += 1; const k = g[Math.round(y)]?.[Math.round(x)]; if (k >= 0 && (STONE.includes(k) || ROBE.includes(k))) { put(g, y, x, GOLD[2]); put(g, y, x - 1, GOLD[0]); } } };
  crack(116, 34, -1, 20, 3); crack(140, 40, 1, 24, 5);

  despeckle(g);
  outline(g, OUT, RIM);
  return { pal, g };
}
export const PIECES = (() => { const { pal, g } = build(); return [toPieceFile(pal, "M5-予言の歪み", g)]; })();
