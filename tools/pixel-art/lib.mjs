// ドット絵の部品づくりの共通関数。64×64のグリッド（色番号の配列）を組み立てる。
/** 解像度の倍率（環境変数 SCALE=2 で128×128）。部品の設計は64×64の座標で書き、倍率ぶんだけ細かく描く。 */
export const S = Number(process.env.SCALE || 1);
export const N = 64 * S;
export function hash(a, b) {
  let h = (Math.floor(a) * 374761393 + Math.floor(b) * 668265263) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
export function makeGrid() {
  return Array.from({ length: N }, () => Array(N).fill(-1));
}
/** 設計座標（64基準）の1マスを、倍率ぶんのドットで塗る。 */
export function put(g, r, c, k) {
  r = Math.round(r); c = Math.round(c);
  for (let dr = 0; dr < S; dr++) for (let dc = 0; dc < S; dc++) putNative(g, r * S + dr, c * S + dc, k);
}
export function putNative(g, r, c, k) {
  if (r >= 0 && r < N && c >= 0 && c < N) g[r][c] = k;
}
/** 設計座標で色番号を読む。 */
export function get(g, r, c) {
  return g[Math.round(r) * S]?.[Math.round(c) * S] ?? -1;
}
export function rect(g, r0, c0, r1, c1, k) {
  for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) put(g, r, c, k);
}
/** 楕円（超楕円にもできる）。fn(r,c,nx,ny,d,light) が色番号かnullを返す。lightは左上が明るい向き(-1〜1)。 */
export function ellipse(g, cx, cy, rx, ry, fn, power = 2) {
  for (let r = Math.floor((cy - ry) * S); r <= Math.ceil((cy + ry) * S); r++) {
    for (let c = Math.floor((cx - rx) * S); c <= Math.ceil((cx + rx) * S); c++) {
      const dc = (c + 0.5) / S, dr = (r + 0.5) / S;
      const nx = (dc - cx) / rx, ny = (dr - cy) / ry;
      const d = Math.pow(Math.abs(nx), power) + Math.pow(Math.abs(ny), power);
      if (d > 1) continue;
      const light = -nx * 0.6 - ny * 0.8;
      const k = fn(Math.floor(dr), Math.floor(dc), nx, ny, d, light);
      if (k !== null && k !== undefined) putNative(g, r, c, k);
    }
  }
}
/** 5階調の色（ramp[0]=暗〜ramp[4]=明）で光と影をつける標準の塗り分け。 */
export function toneOf(ramp, light, d, noise = 0.12, seed = [0, 0]) {
  let t = light > 0.5 ? 4 : light > 0.12 ? 3 : light > -0.3 ? 2 : 1;
  if (d > 0.78 && light < 0) t = 1;
  if (d > 0.92) t = Math.max(0, t - 1);
  if (hash(seed[0], seed[1]) < noise) t = Math.max(0, Math.min(4, t + (hash(seed[1], seed[0]) < 0.5 ? -1 : 1)));
  return ramp[t];
}
/** 外周に縁取り色を付ける（skip の色は縁取りの対象にしない＝落ち影など）。細かい解像度では1ドットの細い縁になる。 */
export function outline(g, edge, skip = []) {
  const has = (r, c) => r >= 0 && r < N && c >= 0 && c < N && g[r][c] !== -1 && !skip.includes(g[r][c]);
  const add = [];
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) {
    if (g[r][c] === -1 || skip.includes(g[r][c])) {
      if ([[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => has(r + a, c + b))) add.push([r, c]);
    }
  }
  for (const [r, c] of add) g[r][c] = edge;
}
/**
 * 仕上げ（倍率2以上のとき）: 同じ系統の色（ramp）どうしの境目を市松のディザでなじませ、
 * さらに1ドット単位の細かい揺らぎを足して、べた塗りの面を減らす。
 */
export function refine(g, ramps) {
  if (S < 2) return;
  const pos = new Map();
  ramps.forEach((ramp) => ramp.forEach((k, i) => pos.set(k, { ramp, i })));
  const copy = g.map((row) => row.slice());
  for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) {
    const k = copy[r][c]; const info = pos.get(k); if (!info) continue;
    const { ramp, i } = info;
    for (const [dr, dc] of [[0, 2], [2, 0], [0, -2], [-2, 0]]) {
      const n = copy[r + dr]?.[c + dc]; const ni = pos.get(n);
      if (ni && ni.ramp === ramp && Math.abs(ni.i - i) === 1 && (r + c) % 2 === 0 && hash(c * 3 + 1, r * 5 + 2) < 0.6) { g[r][c] = n; break; }
    }
    if (hash(c + 977, r + 131) < 0.07) { const ni = Math.max(0, Math.min(ramp.length - 1, i + (hash(r, c) < 0.5 ? -1 : 1))); g[r][c] = ramp[ni]; }
  }
}
/** 地面の落ち影（楕円のディザ）。 */
export function shadow(g, cx, cy, rx, ry, k) {
  ellipse(g, cx, cy, rx, ry, (r, c, nx, ny, d) => (d < 0.6 || hash(c, r) < 0.7 ? k : null));
}
