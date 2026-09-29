// v2: モンスター・ボスを「一から」描くための共通部品（旧 lib.mjs・bosses.mjs は使わない）。
// 方針は docs/design/pixel-art-notes.md（光は左上・色相シフト・外周は暗い縁取り・孤立ドットを消す・26色以内）。
export const W = 256;
export const hash = (a, b) => { let h = (Math.floor(a) * 374761393 + Math.floor(b) * 668265263) >>> 0; h = ((h ^ (h >>> 13)) * 1274126177) >>> 0; return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
export const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
export const smoothstep = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };

// ---- 色 ----
function hsl2hex(h, s, l) {
  h = ((h % 360) + 360) % 360; s = clamp(s, 0, 1); l = clamp(l, 0, 1);
  const a = s * Math.min(l, 1 - l), f = (n) => { const k = (n + h / 30) % 12; return l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)); };
  return "#" + [f(0), f(8), f(4)].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");
}
/** パレット。ramp() で「暗→明」の色の並びを作る。影は青紫側、光は黄側へ色相をずらし、彩度は中間が最大。 */
export function createPalette() {
  const colors = []; const names = [];
  const add = (name, hex) => { const i = colors.indexOf(hex); if (i >= 0) return i; if (colors.length >= 26) throw new Error("色が26色を超えました: " + name); colors.push(hex); names.push(name); return colors.length - 1; };
  return {
    colors, names, add,
    /** hue: 中間色の色相, steps: 段数, sat: 中間の彩度, lo/hi: 明るさの範囲 */
    ramp(name, hue, sat, steps = 4, lo = 0.12, hi = 0.72, shift = 26) {
      return Array.from({ length: steps }, (_, i) => {
        const t = i / (steps - 1), mid = 1 - Math.abs(t - 0.55) * 1.4;
        // 影側は 250°（青紫）へ、光側は 55°（黄）へ近づける
        const toward = (from, to, k) => { let d = ((to - from + 540) % 360) - 180; return from + d * k; };
        const hh = t < 0.5 ? toward(hue, 250, (0.5 - t) * shift / 60) : toward(hue, 55, (t - 0.5) * shift / 90);
        return add(`${name}${i + 1}`, hsl2hex(hh, sat * (0.55 + 0.45 * clamp(mid, 0, 1)), lo + (hi - lo) * t));
      });
    },
    rgb(name, hex) { return add(name, hex); },
  };
}

// ---- グリッド ----
export const makeGrid = () => Array.from({ length: W }, () => Array(W).fill(-1));
export const put = (g, r, c, k) => { r = Math.round(r); c = Math.round(c); if (r >= 0 && r < W && c >= 0 && c < W) g[r][c] = k; };

// ---- 立体（高さ場）----
/** 高さ場: 楕円体を滑らかに合成して丸みのある塊を作る。parts=[{cx,cy,rx,ry,h}] */
export function heightField(parts, k = 6) {
  return (x, y) => {
    let s = 0;
    for (const p of parts) {
      const nx = (x - p.cx) / p.rx, ny = (y - p.cy) / p.ry, d = nx * nx + ny * ny;
      if (d < 1) s += Math.exp(k * Math.sqrt(1 - d) * (p.h ?? 1)) - 1;
    }
    return s <= 0 ? 0 : Math.log(1 + s) / k;
  };
}
const L = (() => { const v = [-0.5, -0.62, 0.6]; const n = Math.hypot(...v); return v.map((x) => x / n); })();
/** 高さ場を色に塗る。ramp は暗→明。tex(x,y)で明るさを±補正（質感）。しきい値 thr 以上を「中身」とする。 */
export function paintField(g, hf, ramp, { thr = 0.02, gain = 1.0, tex = null, ambient = 0.25, box = [0, 0, W, W] } = {}) {
  const [x0, y0, x1, y1] = box, e = 0.6;
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
    const h = hf(x, y); if (h < thr) continue;
    const dx = (hf(x + e, y) - hf(x - e, y)) / (2 * e), dy = (hf(x, y + e) - hf(x, y - e)) / (2 * e);
    const nz = 1 / Math.hypot(dx * 14 * gain, dy * 14 * gain, 1), nx = -dx * 14 * gain * nz, ny = -dy * 14 * gain * nz;
    let lum = nx * L[0] + ny * L[1] + nz * L[2]; lum = ambient + (1 - ambient) * clamp(lum, 0, 1);
    if (tex) lum += tex(x, y, lum);
    put(g, y, x, ramp[clamp(Math.floor(lum * ramp.length), 0, ramp.length - 1)]);
  }
}
/** 単純な楕円体を描く。 */
export function ellipsoid(g, cx, cy, rx, ry, ramp, opts = {}) {
  paintField(g, heightField([{ cx, cy, rx, ry }]), ramp, { ...opts, box: [Math.floor(cx - rx) - 1, Math.floor(cy - ry) - 1, Math.ceil(cx + rx) + 2, Math.ceil(cy + ry) + 2] });
}
/** 曲線に沿った先細りの管（触手・角・腕）。 */
export function limb(g, pts, r0, r1, ramp, opts = {}) {
  const parts = []; const n = pts.length;
  pts.forEach(([x, y], i) => { const t = i / (n - 1), r = r0 + (r1 - r0) * t; parts.push({ cx: x, cy: y, rx: r, ry: r }); });
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]), m = Math.max(r0, r1) + 3;
  paintField(g, heightField(parts, 5), ramp, { ...opts, box: [Math.floor(Math.min(...xs) - m), Math.floor(Math.min(...ys) - m), Math.ceil(Math.max(...xs) + m), Math.ceil(Math.max(...ys) + m)] });
}
export function bezier(p0, p1, p2, n = 24) { return Array.from({ length: n + 1 }, (_, i) => { const t = i / n; return [(1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]]; }); }

// ---- 仕上げ ----
/** 孤立ドット（上下左右に同じ色が無い）を、最も多い隣の色に置き換える。 */
export function despeckle(g, passes = 2) {
  for (let p = 0; p < passes; p++) for (let r = 1; r < W - 1; r++) for (let c = 1; c < W - 1; c++) {
    const k = g[r][c]; if (k < 0) continue;
    const n = [g[r - 1][c], g[r + 1][c], g[r][c - 1], g[r][c + 1]];
    if (n.includes(k)) continue;
    const cnt = new Map(); for (const v of n) if (v >= 0) cnt.set(v, (cnt.get(v) || 0) + 1);
    let best = k, bc = 0; for (const [v, m] of cnt) if (m > bc) { best = v; bc = m; }
    if (bc >= 2) g[r][c] = best;
  }
}
/** 外周に1ドットの縁取り。edge は暗い色。左上側（光の当たる側）は rim（明るめの暗色）を使う。 */
export function outline(g, edge, rim = edge) {
  const has = (r, c) => r >= 0 && r < W && c >= 0 && c < W && g[r][c] >= 0;
  const add = [];
  for (let r = 0; r < W; r++) for (let c = 0; c < W; c++) if (g[r][c] < 0 && [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(r + a, c + b))) add.push([r, c, has(r + 1, c) || has(r, c + 1) ? rim : edge]);
  for (const [r, c, k] of add) g[r][c] = k;
}
/** 落ち影（楕円）。 */
export function groundShadow(g, cx, cy, rx, ry, k) {
  for (let y = Math.floor(cy - ry); y <= cy + ry; y++) for (let x = Math.floor(cx - rx); x <= cx + rx; x++) { const d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2; if (d < 1 && g[y]?.[x] === -1 && (d < 0.55 || (x + y) % 2 === 0)) put(g, y, x, k); }
}
/** 光る目（縦長の瞳）。glow は暗→明の3色。 */
export function eye(g, cx, cy, rx, ry, glow, dark, tilt = 0) {
  for (let y = -ry - 2; y <= ry + 2; y++) for (let x = -rx - 2; x <= rx + 2; x++) {
    const d = (x / (rx + 1.6)) ** 2 + (y / (ry + 1.6)) ** 2; if (d > 1) continue;
    const dd = (x / rx) ** 2 + (y / ry) ** 2; let k = dark;
    if (dd <= 1) k = glow[dd < 0.3 ? 2 : dd < 0.65 ? 1 : 0];
    put(g, cy + y, cx + x + Math.round(y * tilt), k);
  }
  for (let y = -ry; y <= ry; y++) { const w = Math.round((1 - Math.abs(y) / ry) * rx * 0.3); for (let x = -w; x <= w; x++) put(g, cy + y, cx + x + Math.round(y * tilt), dark); }
  put(g, cy - Math.round(ry * 0.45), cx - Math.round(rx * 0.4), glow[2]);
}
export function toPieceFile(pal, name, g) { return { name, pal: pal.colors.map((h, i) => [pal.names[i], h]), build: () => g }; }
