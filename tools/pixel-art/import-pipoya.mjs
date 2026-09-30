// ぴぽや倉庫「フィールドマップセット１」（無料素材。規約: docs/assets-credits.md）の32×32チップから、
// 128×128の地形テクスチャ（色番号26色以内）を作る。元ファイルは assets-src/pipoya/。
// 同じ絵の繰り返しが目立たないよう、32×32を16マス並べるとき、回転・反転を混ぜる。
import path from "path";
import { readPng } from "./png-read.mjs";

const ROOT = new URL("../../assets-src/pipoya/", import.meta.url).pathname;
const AT = (name) => path.join(ROOT, "pipo-map001/640x480/pipo-map001_at-" + name + ".png");
const SHEET = path.join(ROOT, "pipo-map001/640x480/pipo-map001.png");

/** 画像から32×32のチップを切り出す。透明は alpha=0 のまま。 */
function chip(png, x0, y0) {
  const out = [];
  for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) {
    const i = ((y0 + y) * png.width + x0 + x) * 4;
    out.push([png.pixels[i], png.pixels[i + 1], png.pixels[i + 2], png.pixels[i + 3]]);
  }
  return out;
}
const transforms = [
  (x, y) => [x, y], (x, y) => [31 - x, y], (x, y) => [x, 31 - y], (x, y) => [31 - x, 31 - y],
  (x, y) => [y, x], (x, y) => [31 - y, x], (x, y) => [y, 31 - x], (x, y) => [31 - y, 31 - x],
];
function rng(seed) { let s = seed >>> 0; return () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296); }

/** チップ（透明があれば下地チップの上に重ねる）を4×4枚、向きを変えながら並べる。 */
function tile128(base, chipPx, seed, kinds = 8) {
  const r = rng(seed), grid = [];
  for (let ty = 0; ty < 4; ty++) for (let tx = 0; tx < 4; tx++) {
    const t = transforms[Math.floor(r() * kinds)];
    for (let y = 0; y < 32; y++) for (let x = 0; x < 32; x++) {
      const [sx, sy] = t(x, y), k = sy * 32 + sx;
      const px = chipPx[k][3] >= 128 ? chipPx[k] : base[k];
      grid[(ty * 32 + y) * 128 + tx * 32 + x] = px;
    }
  }
  return grid;
}

/** 色を最大 n 色にまとめる（頻度順に代表色を決め、近い色を寄せる。単純だが決まった結果になる）。 */
function quantize(grid, n) {
  const key = (p) => (p[0] << 16) | (p[1] << 8) | p[2];
  const count = new Map();
  for (const p of grid) count.set(key(p), (count.get(key(p)) || 0) + 1);
  let colors = [...count.entries()].sort((a, b) => b[1] - a[1]).map(([k]) => k);
  if (colors.length > n) {
    // 最も近い色同士を、頻度の少ない方から多い方へ寄せていく
    const dist = (a, b) => { const d = [16, 8, 0].map((s) => ((a >> s) & 255) - ((b >> s) & 255)); return d[0] * d[0] * 0.3 + d[1] * d[1] * 0.59 + d[2] * d[2] * 0.11; };
    const weight = new Map(count);
    const alive = new Set(colors);
    const merged = new Map();
    while (alive.size > n) {
      let best = null;
      const arr = [...alive];
      for (let i = 0; i < arr.length; i++) for (let j = i + 1; j < arr.length; j++) {
        const d = dist(arr[i], arr[j]) * Math.min(weight.get(arr[i]), weight.get(arr[j]));
        if (!best || d < best[0]) best = [d, arr[i], arr[j]];
      }
      const [, a, b] = best;
      const [lo, hi] = weight.get(a) < weight.get(b) ? [a, b] : [b, a];
      weight.set(hi, weight.get(hi) + weight.get(lo));
      alive.delete(lo); merged.set(lo, hi);
    }
    const resolve = (c) => { while (merged.has(c)) c = merged.get(c); return c; };
    colors = [...alive].sort((a, b) => weight.get(b) - weight.get(a));
    const idx = new Map(colors.map((c, i) => [c, i]));
    const cells = grid.map((p) => idx.get(resolve(key(p))));
    return { palette: colors.map((c) => "#" + c.toString(16).padStart(6, "0")), cells };
  }
  const idx = new Map(colors.map((c, i) => [c, i]));
  return { palette: colors.map((c) => "#" + c.toString(16).padStart(6, "0")), cells: grid.map((p) => idx.get(key(p))) };
}

export function buildPipoyaTextures() {
  const sheet = readPng(SHEET);
  const grass = chip(sheet, 0, 0);
  const at = (n) => chip(readPng(AT(n)), 0, 128); // 下の段の中身が詰まったチップ
  const src = { dirt: at("tuti"), water: at("umi"), forest: at("mori") };
  const list = {
    "terrain:grass-a": tile128(grass, grass, 11),
    "terrain:grass-b": tile128(grass, grass, 29),
    "terrain:dirt": tile128(grass, src.dirt, 3),
    "terrain:water": tile128(grass, src.water, 5, 4), // 波の向きがあるので、縦横の入れ替えはしない
    "terrain:forest": tile128(grass, src.forest, 7),
  };
  const out = {};
  for (const [k, grid] of Object.entries(list)) {
    const { palette, cells } = quantize(grid, 26);
    out[k] = { size: 128, palette, cells };
  }
  return out;
}
