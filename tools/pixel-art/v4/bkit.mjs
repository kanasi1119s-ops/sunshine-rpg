import { blank, toRows, W } from "./lib4.mjs";
// ---- ボス・大きな絵用の描画部品（担当B追記）。ramp は「暗→明」の文字列（先頭が縁の色）。光は左上。 ----
/** 描画用のキャンバス。 */
export function cv() { const g = blank(); const put = (x, y, c) => { x = Math.round(x); y = Math.round(y); if (x >= 0 && x < W && y >= 0 && y < W) g[y][x] = c; }; const get = (x, y) => (x >= 0 && x < W && y >= 0 && y < W ? g[y][x] : "."); return { g, put, get, rows: (keep = "w") => toRows(despeckle(g, keep)) }; }
/** 立体的に陰影をつけた楕円（左上から光）。o.top/o.bot: 上半分・下半分だけ描く。o.flat: 陰影を弱める。 */
export function ell(c, cx, cy, rx, ry, ramp, o = {}) {
  const n = ramp.length; const ins = (x, y) => { const dx = (x - cx) / (rx + 0.5), dy = (y - cy) / (ry + 0.5); return dx * dx + dy * dy <= 1 && (!o.top || y <= cy) && (!o.bot || y >= cy); };
  for (let y = Math.floor(cy - ry - 1); y <= Math.ceil(cy + ry + 1); y++) for (let x = Math.floor(cx - rx - 1); x <= Math.ceil(cx + rx + 1); x++) {
    if (!ins(x, y)) continue; const dx = (x - cx) / (rx + 0.5), dy = (y - cy) / (ry + 0.5); const d = dx * dx + dy * dy; const nz = Math.sqrt(Math.max(0, 1 - d));
    const edge = !ins(x - 1, y) || !ins(x + 1, y) || !ins(x, y - 1) || !ins(x, y + 1);
    const s = (dx * -0.5 + dy * -0.62 + nz * 0.6) / 0.98;
    if (edge) { c.put(x, y, s > 0.35 && (!ins(x - 1, y) || !ins(x, y - 1)) ? ramp[Math.min(1, n - 1)] : ramp[0]); continue; }
    const k = Math.max(0, Math.min(0.999, (s + 0.3) / 1.2)); c.put(x, y, ramp[1 + Math.floor(k * (n - 1))]);
  }
}
/** 陰影つきの四角。左・上が明るく、右・下が暗い。 */
export function box(c, x0, y0, x1, y1, ramp) {
  const n = ramp.length; const mid = ramp[Math.min(2, n - 1)], hi = ramp[Math.min(3, n - 1)], lo = ramp[1], top = ramp[n - 1];
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
    let ch = mid; if (x === x0 || x === x1 || y === y0 || y === y1) ch = ramp[0];
    else if (y === y0 + 1 || x === x0 + 1) ch = hi; else if (x === x1 - 1 || y === y1 - 1) ch = lo;
    if (y === y0 + 1 && x === x0 + 1 && n > 4) ch = top; c.put(x, y, ch);
  }
}
/** 多角形（点は [x,y]）。縁は暗く、左上の縁は明るく、右下の内側は影。 */
export function poly(c, pts, ramp) {
  const n = ramp.length; const inside = (x, y) => { let r = false; for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) { const [xi, yi] = pts[i], [xj, yj] = pts[j]; if ((yi > y + 0.01) !== (yj > y + 0.01) && x < ((xj - xi) * (y + 0.01 - yi)) / (yj - yi) + xi) r = !r; } return r; };
  const ys = pts.map((p) => p[1]), xs = pts.map((p) => p[0]); const S = new Set();
  for (let y = Math.floor(Math.min(...ys)); y <= Math.ceil(Math.max(...ys)); y++) for (let x = Math.floor(Math.min(...xs)); x <= Math.ceil(Math.max(...xs)); x++) if (inside(x + 0.5, y + 0.5)) S.add(x + "," + y);
  const has = (x, y) => S.has(x + "," + y);
  for (const k of S) { const [x, y] = k.split(",").map(Number); let ch = ramp[Math.min(2, n - 1)];
    const outL = !has(x - 1, y), outT = !has(x, y - 1), outR = !has(x + 1, y), outB = !has(x, y + 1);
    if (outR || outB) ch = ramp[0]; else if (outL || outT) ch = ramp[Math.min(3, n - 1)]; else if (!has(x + 2, y) || !has(x, y + 2)) ch = ramp[1]; else if (!has(x - 2, y) || !has(x, y - 2)) ch = ramp[Math.min(3, n - 1)];
    if ((outL || outT) && (outR || outB)) ch = ramp[0]; c.put(x, y, ch); }
}
/** 線（ブレゼンハム）。 */
export function bline(c, x0, y0, x1, y1, ch) { x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1); const dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1; let e = dx + dy; for (;;) { c.put(x0, y0, ch); if (x0 === x1 && y0 === y1) break; const e2 = 2 * e; if (e2 >= dy) { e += dy; x0 += sx; } if (e2 <= dx) { e += dx; y0 += sy; } } }
/** 楕円を単色で塗る（o.onlyEmpty: 空きだけ）。 */
export function fillEll(c, cx, cy, rx, ry, ch, o = {}) { for (let y = Math.floor(cy - ry - 1); y <= Math.ceil(cy + ry + 1); y++) for (let x = Math.floor(cx - rx - 1); x <= Math.ceil(cx + rx + 1); x++) { const dx = (x - cx) / (rx + 0.5), dy = (y - cy) / (ry + 0.5); if (dx * dx + dy * dy <= 1 && (!o.onlyEmpty || c.get(x, y) === ".")) c.put(x, y, ch); } }
/** 楕円の穴（透明にする）。 */
export const hole = (c, cx, cy, rx, ry) => fillEll(c, cx, cy, rx, ry, ".");
/** 地面の影。 */
export const ground = (c, cx, cy, rx, ry, ch) => fillEll(c, cx, cy, rx, ry, ch);
/** 目（外側 out・白目 sc・虹彩 ir・瞳 pu・ハイライト w）。中心 cx,cy、横 rx・縦 ry。 */
export function eye(c, cx, cy, rx, ry, out, sc, ir, pu, w) { fillEll(c, cx, cy, rx, ry, out); fillEll(c, cx, cy, rx - 1, ry - 1, sc); const r2 = Math.max(1, Math.min(rx, ry) - 1); fillEll(c, cx, cy + 0.3, r2 - 0.5, ry - 1, ir); c.put(cx, cy, pu); c.put(cx, cy + 1, pu); if (rx > 2) c.put(cx + 1, cy, pu); c.put(cx - 1, cy - 1, w); }

/** 孤立した1ドット（同じ色の上下左右が無い点）を、まわりの多い色にそろえてざらつきを減らす。keep の文字（ハイライトなど）は残す。 */
export function despeckle(g, keep = "w") {
  const get = (x, y) => (x >= 0 && x < W && y >= 0 && y < W ? g[y][x] : ".");
  for (let pass = 0; pass < 2; pass++) { const chg = []; for (let y = 0; y < W; y++) for (let x = 0; x < W; x++) { const ch = g[y][x]; if (ch === "." || keep.includes(ch)) continue; const nb = [get(x - 1, y), get(x + 1, y), get(x, y - 1), get(x, y + 1)]; if (nb.includes(ch)) continue; const op = nb.filter((k) => k !== "."); if (op.length < 2) continue; const cnt = {}; for (const k of op) cnt[k] = (cnt[k] || 0) + 1; const best = Object.entries(cnt).sort((a, b) => b[1] - a[1] || nb.indexOf(a[0]) - nb.indexOf(b[0]))[0][0]; chg.push([x, y, best]); } for (const [x, y, k] of chg) g[y][x] = k; }
  return g;
}
