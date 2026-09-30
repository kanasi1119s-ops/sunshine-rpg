// v5: 64×64〜256×256の大きな敵・ボスを描くための道具（2026-09-30）。
// 考え方: 「形（マスク）」を作り → 「立体の陰影つきで塗り」 → 「輪郭・縁の光・質感」を足す。左上から光が当たる。
// 1つの絵 = 1つのモジュール（.mjs）。export: name, category("monster"|"boss"), size, pal（文字→色）, rows（size行×size文字）。色は26色まで。
export const rng = (seed) => { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };
const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const toHex = (a) => "#" + a.map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, "0")).join("");
/** 色の並び（暗→明）を作る。chars の各文字に、から〜までを等分した色を割り当てる。mid を渡すと3点補間。 */
export function ramp(chars, from, to, mid) { const n = chars.length, a = hex(from), b = hex(to), m = mid && hex(mid), o = {}; for (let i = 0; i < n; i++) { const t = n === 1 ? 0 : i / (n - 1); let c; if (m) c = t < 0.5 ? a.map((v, k) => v + (m[k] - v) * (t * 2)) : m.map((v, k) => v + (b[k] - v) * ((t - 0.5) * 2)); else c = a.map((v, k) => v + (b[k] - v) * t); o[chars[i]] = toHex(c); } return o; }

export class Cv {
  constructor(n, m = n) { this.w = n; this.h = m; this.g = Array.from({ length: m }, () => Array(n).fill(".")); }
  inb(x, y) { return x >= 0 && y >= 0 && x < this.w && y < this.h; }
  put(x, y, c) { x = Math.round(x); y = Math.round(y); if (this.inb(x, y)) this.g[y][x] = c; return this; }
  get(x, y) { return this.inb(x, y) ? this.g[y][x] : "."; }
  rows() { return this.g.map((r) => r.join("")); }
  // ---- マスク（形）: Uint8Array(w*h) ----
  M() { return new Uint8Array(this.w * this.h); }
  ell(cx, cy, rx, ry) { const m = this.M(); for (let y = Math.floor(cy - ry - 1); y <= Math.ceil(cy + ry + 1); y++) for (let x = Math.floor(cx - rx - 1); x <= Math.ceil(cx + rx + 1); x++) if (this.inb(x, y) && ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1) m[y * this.w + x] = 1; return m; }
  poly(pts) { const m = this.M(), ys = pts.map((p) => p[1]); for (let y = Math.max(0, Math.floor(Math.min(...ys))); y <= Math.min(this.h - 1, Math.ceil(Math.max(...ys))); y++) { const yy = y + 0.5, xs = []; for (let i = 0; i < pts.length; i++) { const [ax, ay] = pts[i], [bx, by] = pts[(i + 1) % pts.length]; if ((ay <= yy && by > yy) || (by <= yy && ay > yy)) xs.push(ax + ((yy - ay) / (by - ay)) * (bx - ax)); } xs.sort((a, b) => a - b); for (let i = 0; i + 1 < xs.length; i += 2) for (let x = Math.round(xs[i]); x < Math.round(xs[i + 1]); x++) if (this.inb(x, y)) m[y * this.w + x] = 1; } return m; }
  rect(x0, y0, x1, y1) { const m = this.M(); for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) if (this.inb(x, y)) m[y * this.w + x] = 1; return m; }
  /** 太さが変わる線（丸い筆）。r0→r1 は半径。腕・尾・首・足に使う。 */
  limb(x0, y0, x1, y1, r0, r1 = r0) { const m = this.M(), n = Math.ceil(Math.hypot(x1 - x0, y1 - y0) * 2) + 1; for (let i = 0; i <= n; i++) { const t = i / n, cx = x0 + (x1 - x0) * t, cy = y0 + (y1 - y0) * t, r = r0 + (r1 - r0) * t; const e = this.ell(cx, cy, Math.max(0.6, r), Math.max(0.6, r)); for (let k = 0; k < m.length; k++) if (e[k]) m[k] = 1; } return m; }
  /** 曲がった帯（点の列を通る太さ可変の線）。しっぽ・蛇・触手に。pts=[[x,y,r],...] */
  strip(pts) { const m = this.M(); for (let i = 0; i + 1 < pts.length; i++) { const a = pts[i], b = pts[i + 1], s = this.limb(a[0], a[1], b[0], b[1], a[2], b[2]); for (let k = 0; k < m.length; k++) if (s[k]) m[k] = 1; } return m; }
  union(...ms) { const m = this.M(); for (const a of ms) for (let k = 0; k < m.length; k++) if (a[k]) m[k] = 1; return m; }
  sub(a, ...bs) { const m = Uint8Array.from(a); for (const b of bs) for (let k = 0; k < m.length; k++) if (b[k]) m[k] = 0; return m; }
  inter(a, b) { const m = this.M(); for (let k = 0; k < m.length; k++) if (a[k] && b[k]) m[k] = 1; return m; }
  /** 左右反転（絵の中心 (w-1)/2 を軸に）。左半分だけ作って hmirror して union すれば左右対称。 */
  hmirror(a) { const m = this.M(); for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) if (a[y * this.w + x]) m[y * this.w + (this.w - 1 - x)] = 1; return m; }
  sym(a) { return this.union(a, this.hmirror(a)); }
  shift(a, dx, dy) { const m = this.M(); for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) if (a[y * this.w + x]) { const X = x + dx, Y = y + dy; if (this.inb(X, Y)) m[Y * this.w + X] = 1; } return m; }
  /** 1ドット太らせる／細らせる。 */
  grow(a, n = 1) { let m = a; for (let i = 0; i < n; i++) { const o = Uint8Array.from(m); for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) if (m[y * this.w + x]) for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const X = x + dx, Y = y + dy; if (this.inb(X, Y)) o[Y * this.w + X] = 1; } m = o; } return m; }
  shrink(a, n = 1) { let m = a; for (let i = 0; i < n; i++) { const o = Uint8Array.from(m); for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) if (m[y * this.w + x]) for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const X = x + dx, Y = y + dy; if (!this.inb(X, Y) || !m[Y * this.w + X]) { o[y * this.w + x] = 0; break; } } m = o; } return m; }
  // ---- 塗り ----
  /** 距離（縁からの近さ）から丸みの高さを作る。 */
  _height(m, R) { const w = this.w, h = this.h, d = new Float32Array(w * h).fill(1e9), q = []; for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = y * w + x; if (!m[i]) { d[i] = 0; continue; } for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const X = x + dx, Y = y + dy; if (!this.inb(X, Y) || !m[Y * w + X]) { d[i] = 1; q.push(i); break; } } }
    for (let qi = 0; qi < q.length; qi++) { const i = q[qi], x = i % w, y = (i / w) | 0; for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const X = x + dx, Y = y + dy; if (!this.inb(X, Y)) continue; const j = Y * w + X; if (m[j] && d[j] > d[i] + 1) { d[j] = d[i] + 1; q.push(j); } } }
    const H = new Float32Array(w * h); for (let i = 0; i < H.length; i++) if (m[i]) { const t = Math.min(1, d[i] / R); H[i] = 1 - (1 - t) * (1 - t); } return H; }
  /**
   * マスクを、立体の陰影をつけて塗る。ramp は暗→明の文字の並び。
   * opts: round(丸みの半径・既定は形の大きさから)、bias(全体を明るく＋／暗く−)、light([lx,ly]・既定は左上)、dither(段の境目をまだらにする・既定 true)、flat(陰影を弱める 0〜1)
   */
  paint(m, ramp, o = {}) { const w = this.w, h = this.h; let x0 = w, x1 = 0, y0 = h, y1 = 0; for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (m[y * w + x]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; } if (x1 < x0) return this;
    const R = o.round ?? Math.max(2, Math.min(x1 - x0, y1 - y0) / 2.2), H = this._height(m, R), L = o.light ?? [-0.55, -0.75], k = 2.6, n = ramp.length, flat = o.flat ?? 0, dith = o.dither ?? true, bias = o.bias ?? 0;
    const hh = (x, y) => (this.inb(x, y) ? H[y * w + x] : 0), bay = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]];
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) if (m[y * w + x]) { const gx = (hh(x + 1, y) - hh(x - 1, y)) * k, gy = (hh(x, y + 1) - hh(x, y - 1)) * k; let nz = 1, nx = -gx, ny = -gy; const len = Math.hypot(nx, ny, nz); nx /= len; ny /= len; nz /= len; const lz = 0.7, ll = Math.hypot(L[0], L[1], lz); let s = (nx * L[0] + ny * L[1] + nz * lz) / ll; s = (s - 0.55) * 1.7 + 0.5 + bias; s = 0.5 + (s - 0.5) * (1 - flat); s += (hh(x, y) - 0.5) * 0.12; let f = Math.max(0, Math.min(0.9999, s)) * n; let idx = Math.floor(f); if (dith) { const fr = f - idx; if (fr > 0.62 + (bay[y & 3][x & 3] / 16 - 0.5) * 0.5 && idx < n - 1) idx++; } this.g[y][x] = ramp[Math.max(0, Math.min(n - 1, idx))]; } return this; }
  /** 平らに1色で塗る。 */
  fill(m, c) { for (let i = 0; i < m.length; i++) if (m[i]) this.g[(i / this.w) | 0][i % this.w] = c; return this; }
  /** 形の縁（内側の1ドット）を1色でなぞる。重なった部品どうしを分ける線に。side: "all"|"lower"(下と右の縁だけ)|"upper"(上と左) */
  edge(m, c, side = "all") { const w = this.w; for (let y = 0; y < this.h; y++) for (let x = 0; x < w; x++) if (m[y * w + x]) { const e = (dx, dy) => { const X = x + dx, Y = y + dy; return !this.inb(X, Y) || !m[Y * w + X]; }; const hit = side === "all" ? e(1, 0) || e(-1, 0) || e(0, 1) || e(0, -1) : side === "lower" ? e(1, 0) || e(0, 1) : e(-1, 0) || e(0, -1); if (hit) this.g[y][x] = c; } return this; }
  /** 上と左が空いているドット（光が当たる縁）を、map で明るい文字に置き換える。 */
  rim(m, map) { const w = this.w; for (let y = 0; y < this.h; y++) for (let x = 0; x < w; x++) if (m[y * w + x]) { const up = this.inb(x, y - 1) && m[(y - 1) * w + x], lf = this.inb(x - 1, y) && m[y * w + x - 1]; if (!up || !lf) { const c = this.g[y][x]; if (map[c]) this.g[y][x] = map[c]; } } return this; }
  /** ざらつき（点描）。density は 0〜1。 */
  speckle(m, c, density, seed = 1) { const r = rng(seed); for (let i = 0; i < m.length; i++) if (m[i] && r() < density) this.g[(i / this.w) | 0][i % this.w] = c; return this; }
  /** 質感の線（毛並み・岩の割れ目など）。mask の中にだけ引く。 */
  strokeIn(m, x0, y0, x1, y1, c) { let dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1, e = dx + dy, X = Math.round(x0), Y = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1); for (let i = 0; i < 4096; i++) { if (this.inb(X, Y) && m[Y * this.w + X]) this.g[Y][X] = c; if (X === x1 && Y === y1) break; const e2 = 2 * e; if (e2 >= dy) { e += dy; X += sx; } if (e2 <= dx) { e += dx; Y += sy; } } return this; }
  line(x0, y0, x1, y1, c, t = 1) { const n = Math.ceil(Math.hypot(x1 - x0, y1 - y0)) + 1; for (let i = 0; i <= n; i++) { const p = i / n, X = x0 + (x1 - x0) * p, Y = y0 + (y1 - y0) * p; if (t <= 1) this.put(X, Y, c); else this.fill(this.ell(X, Y, t / 2, t / 2), c); } return this; }
  /** すでに描いた物の外側に輪郭を付ける。map は「隣の色→輪郭の色」（無ければ def）。 */
  outline(def, map = {}, diag = false) { const l = [], D = diag ? [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]] : [[1, 0], [-1, 0], [0, 1], [0, -1]]; for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) if (this.g[y][x] === ".") { let c = null; for (const [dx, dy] of D) { const n = this.get(x + dx, y + dy); if (n !== ".") { c = map[n] ?? def; break; } } if (c) l.push([x, y, c]); } for (const [x, y, c] of l) this.g[y][x] = c; return this; }
  /** 空いているところだけに、落ち影の楕円。 */
  shadow(cx, cy, rx, ry, c, dither = true) { for (let y = Math.floor(cy - ry); y <= Math.ceil(cy + ry); y++) for (let x = Math.floor(cx - rx); x <= Math.ceil(cx + rx); x++) if (this.inb(x, y) && this.g[y][x] === "." && ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 && (!dither || ((x + y) & 1) === 0 || ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 0.5)) this.g[y][x] = c; return this; }
  /** 目や光の点など、小さな塊を置く。 */
  dot(x, y, c, r = 0) { return r ? this.fill(this.ell(x, y, r, r), c) : this.put(x, y, c); }
  /** 孤立した1ドットを、まわりでいちばん多い色にそろえる（keep は残す）。 */
  despeckle(keep = "") { const ch = []; for (let y = 1; y < this.h - 1; y++) for (let x = 1; x < this.w - 1; x++) { const c = this.g[y][x]; if (c === "." || keep.includes(c)) continue; const nb = [this.g[y - 1][x], this.g[y + 1][x], this.g[y][x - 1], this.g[y][x + 1]]; if (nb.includes(c)) continue; const cnt = {}; for (const k of nb) if (k !== ".") cnt[k] = (cnt[k] || 0) + 1; const b = Object.entries(cnt).sort((a, z) => z[1] - a[1])[0]; if (b && b[1] >= 2) ch.push([x, y, b[0]]); } for (const [x, y, k] of ch) this.g[y][x] = k; return this; }
  /** 左半分を、右半分へ写す（完全な左右対称にしたいとき）。 */
  mirrorLeft() { for (let y = 0; y < this.h; y++) for (let x = 0; x < Math.floor(this.w / 2); x++) this.g[y][this.w - 1 - x] = this.g[y][x]; return this; }
}
/** 色の文字の一覧と使用数を返す（確認用）。 */
export const colorsOf = (rows) => { const c = {}; for (const r of rows) for (const k of r) if (k !== ".") c[k] = (c[k] || 0) + 1; return c; };
