import { RELIEF_SPRITES } from "../game/art/relief-sprites.generated";
import { getSpriteCanvas } from "../game/art/sprite";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { hashCell } from "../game/color-utils";
import type { Camera } from "./camera";
import type { TileMap } from "../game/map/tile-map";
import type { TileMapData } from "../game/map/types";

/**
 * 全体フィールドの山の高低差（2026-10-05、人間の指示「山って高低差あるはずなんだよね。それを考えてリアルな山作ってほしいな」）。
 *
 * 山のマス（tileArt が mountain / peaks）の上に、1マスに1つずつ「山の絵」を重ねて描く。見た目だけで、通れる・通れない
 * （collision）や地図のマスは変えない。
 *  - 高さ: 山脈のふちからの距離（4方向）の平方根の2倍＋ゆるいゆらぎ（5マスくらいの大きさ）。とがった山（peaks）のマスは少し高い。
 *    ふち＝ふもとの小山（foot）、内がわ＝中腹（slope）・高い山（high）。峰（peak、雪をいただく）は「まわり2マスの中でいちばん高い」
 *    所だけ。ゆらぎで、峰と峰のあいだに低い所（谷・峠）ができる。内がわの中腹・高い山は、5つに1つほど描かず、谷の地面をのぞかせる。
 *  - 向き: 右どなりのほうが高ければ頂が右寄り（r）、そうでなければ左寄り（l）。尾根が高い方へのぼっていくように見える。形は3つ（a〜c）。
 *  - 系統: 雪原・雪の森から4マス以内は雪の山（snow）、溶岩・灰の大地から8マス以内は火山の岩（volc）、ほかは灰色（gray）。
 *  - 地面: ふちから2マスまでは、となりの陸の地面（草・森・雪など）を敷いてから山を置く（山と草原の境目が四角い段にならない）。
 *    それより内がわは、谷の地面（いちばん低い所）を敷く。
 *  - 重ね方: 奥の列から手前の列へ。列を描き終えるごとに、その列の峰の影（右下へ倒した形）を半透明で重ねる
 *    （同じ列の右の山と、うしろの地面に影が落ちる。手前の列は、あとから上に描かれる）。
 *  - 重さ: 16×16マスずつ、1枚のキャンバスにまとめて覚えておき、毎フレームはそれを数枚描くだけ。
 * 絵は tools/pixel-art/ai-gen/mountain_relief.py が作る `relief-sprites.generated.ts`（72×72、山のすそのまん中が (26, 56)）。
 */

export type ReliefFamily = "gray" | "snow" | "volc";
export type ReliefTier = "foot" | "slope" | "high" | "peak";

export interface ReliefField {
  width: number;
  height: number;
  /** ふちからの距離（山でないマスは 0）。 */
  dist: Uint16Array;
  /** 高さ（山でないマスは 0）。 */
  elev: Float32Array;
  /** 0=gray 1=snow 2=volc */
  family: Uint8Array;
  /** 絵の段（0=foot 1=slope 2=high 3=peak。山でないマスは 0） */
  tier: Uint8Array;
}

export const TIERS: ReliefTier[] = ["foot", "slope", "high", "peak"];

const FAMILIES: ReliefFamily[] = ["gray", "snow", "volc"];
const ANCHOR_X = 26;
const ANCHOR_Y = 56;
const TEX = 128;
const ART = 16;

/** なめらかなゆらぎ（-1〜1）。5マスくらいの大きさで、決まった値（毎回同じ）。 */
export function reliefNoise(x: number, y: number): number {
  const s = 5;
  const x0 = Math.floor(x / s);
  const y0 = Math.floor(y / s);
  const fx = x / s - x0;
  const fy = y / s - y0;
  const v = (a: number, b: number): number => (hashCell(a * 7 + 3, b * 13 + 5) % 1000) / 500 - 1;
  const sm = (t: number): number => t * t * (3 - 2 * t);
  const top = v(x0, y0) + (v(x0 + 1, y0) - v(x0, y0)) * sm(fx);
  const bottom = v(x0, y0 + 1) + (v(x0 + 1, y0 + 1) - v(x0, y0 + 1)) * sm(fx);
  return top + (bottom - top) * sm(fy);
}

/**
 * 高さの場を作る（純粋な関数。テストしやすいよう、地図の形式から切りはなしている）。
 * isMount: 山のマスか。isPeak: とがった山のマスか。familyHint: そのマスのまわりの地面の系統（0=ふつう 1=雪 2=火山）。
 */
export function computeReliefField(
  width: number,
  height: number,
  isMount: (x: number, y: number) => boolean,
  isPeak: (x: number, y: number) => boolean,
  familyHint: (x: number, y: number) => number,
): ReliefField {
  const n = width * height;
  const dist = new Uint16Array(n);
  const elev = new Float32Array(n);
  const family = new Uint8Array(n);
  const queue: number[] = [];
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (!isMount(x, y)) continue;
      const i = y * width + x;
      const edge = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => {
        const nx = x + dx, ny = y + dy;
        return nx < 0 || ny < 0 || nx >= width || ny >= height || !isMount(nx, ny);
      });
      if (edge) {
        dist[i] = 1;
        queue.push(i);
      }
    }
  }
  for (let q = 0; q < queue.length; q++) {
    const i = queue[q];
    const x = i % width, y = Math.floor(i / width);
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, ny = y + dy;
      if (nx < 0 || ny < 0 || nx >= width || ny >= height) continue;
      const j = ny * width + nx;
      if (dist[j] === 0 && isMount(nx, ny)) {
        dist[j] = dist[i] + 1;
        queue.push(j);
      }
    }
  }
  // 高さ: 内がわほど高いが、だんだんゆるやかに（平らな峰の台地にならないよう、距離の平方根）。ゆらぎで谷と峠ができる
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const i = y * width + x;
      if (!dist[i]) continue;
      elev[i] = 2 * Math.sqrt(dist[i]) + reliefNoise(x, y) * 1.3 + (isPeak(x, y) ? 0.6 : 0);
      family[i] = familyHint(x, y);
    }
  }
  // 段: ふち＝ふもと。峰（雪）は「まわり2マスの中でいちばん高い」所だけ。それより低い所は高い山・中腹
  const tier = new Uint8Array(n);
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const i = y * width + x;
      if (!dist[i]) continue;
      let top = true;
      for (let dy = -2; dy <= 2 && top; dy++) {
        for (let dx = -2; dx <= 2; dx++) {
          const nx = x + dx, ny = y + dy;
          if ((dx || dy) && nx >= 0 && ny >= 0 && nx < width && ny < height && elev[ny * width + nx] > elev[i]) {
            top = false;
            break;
          }
        }
      }
      tier[i] = reliefTierOf(dist[i], elev[i], top);
    }
  }
  return { width, height, dist, elev, family, tier };
}

/** 段の決め方（0=foot 1=slope 2=high 3=peak）。 */
export function reliefTierOf(dist: number, elev: number, localTop: boolean): number {
  if (dist <= 1) return 0;
  if (localTop && elev >= 3.8) return 3;
  if (elev >= 3.4) return 2;
  return 1;
}

const fieldCache = new WeakMap<TileMapData, ReliefField>();

function artOf(map: TileMap, x: number, y: number): string {
  if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height) return "";
  const id = map.data.layers[0]?.data[y * map.data.width + x] ?? 0;
  return map.data.tileArt?.[id] ?? "";
}

function textureOf(map: TileMap, x: number, y: number): string {
  if (x < 0 || y < 0 || x >= map.data.width || y >= map.data.height) return "";
  const id = map.data.layers[0]?.data[y * map.data.width + x] ?? 0;
  return map.data.tileTexture?.[id] ?? "";
}

function isMountArt(art: string): boolean {
  return art === "mountain" || art === "peaks";
}

/** 地図の高さの場（地図ごとに1回だけ作る）。 */
export function reliefFieldFor(map: TileMap): ReliefField {
  const cached = fieldCache.get(map.data);
  if (cached) return cached;
  const { width, height } = map.data;
  // 雪・火山の地面の近さを、先にまとめて数える（マスごとに周りを見ると重いので、ぼかしの代わりに広げる）
  const near = (want: (tex: string) => boolean, r: number): Uint8Array => {
    const hit = new Uint8Array(width * height);
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        if (!want(textureOf(map, x, y))) continue;
        for (let yy = Math.max(0, y - r); yy <= Math.min(height - 1, y + r); yy++) {
          for (let xx = Math.max(0, x - r); xx <= Math.min(width - 1, x + r); xx++) hit[yy * width + xx] = 1;
        }
      }
    }
    return hit;
  };
  const snowy = near((t) => t === "terrain:w-snow" || t === "terrain:w-snowforest", 4);
  const volcanic = near((t) => t === "terrain:w-lava" || t === "terrain:w-ash", 8);
  const field = computeReliefField(
    width,
    height,
    (x, y) => isMountArt(artOf(map, x, y)),
    (x, y) => artOf(map, x, y) === "peaks",
    (x, y) => (volcanic[y * width + x] ? 2 : snowy[y * width + x] ? 1 : 0),
  );
  fieldCache.set(map.data, field);
  return field;
}

function drawWindow(ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement, tx: number, ty: number, sx: number, sy: number): void {
  const ox = (((tx * ART) % TEX) + TEX) % TEX;
  const oy = (((ty * ART) % TEX) + TEX) % TEX;
  ctx.drawImage(canvas, ox, oy, ART, ART, sx, sy, ART, ART);
}

/** となりの陸の地面（草・雪・砂・丘・道・森など）のテクスチャ。水と山しかなければ null。 */
function landBeside(map: TileMap, x: number, y: number): string | null {
  const counts = new Map<string, number>();
  for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]) {
    const art = artOf(map, x + dx, y + dy);
    if (art && art !== "water" && !isMountArt(art)) {
      const tex = textureOf(map, x + dx, y + dy);
      if (tex) counts.set(tex, (counts.get(tex) ?? 0) + (Math.abs(dx) + Math.abs(dy) === 1 ? 2 : 1));
    }
  }
  let best: string | null = null;
  let bestN = 0;
  for (const [k, v] of counts) {
    if (v > bestN || (v === bestN && best !== null && k < best)) {
      best = k;
      bestN = v;
    }
  }
  return best;
}

interface ReliefPlan {
  /** マスごとの山の絵の番号（-1 は山でない）。keys[番号] が絵のキー。 */
  sprite: Int16Array;
  /** マスごとの地面の番号（-1 は描かない）。bases[番号] がテクスチャのキー（"T:" は地形、"R:" は谷の地面）。 */
  base: Int16Array;
  /** 絵の置き場所のずれ（x は -2〜2、y は -1〜1） */
  jx: Int8Array;
  jy: Int8Array;
  keys: string[];
  bases: string[];
}

const planCache = new WeakMap<TileMapData, ReliefPlan>();

/** マスごとの絵・地面・ずれを、地図ごとに1回だけ決めておく（毎フレーム決めると重い）。 */
function reliefPlanFor(map: TileMap): ReliefPlan {
  const cached = planCache.get(map.data);
  if (cached) return cached;
  const field = reliefFieldFor(map);
  const { width, height } = map.data;
  const n = width * height;
  const sprite = new Int16Array(n).fill(-1);
  const base = new Int16Array(n).fill(-1);
  const jx = new Int8Array(n);
  const jy = new Int8Array(n);
  const keys: string[] = [];
  const bases: string[] = [];
  const keyIndex = new Map<string, number>();
  const baseIndex = new Map<string, number>();
  const idx = (m: Map<string, number>, list: string[], k: string): number => {
    let v = m.get(k);
    if (v === undefined) {
      v = list.length;
      list.push(k);
      m.set(k, v);
    }
    return v;
  };
  for (let ty = 0; ty < height; ty++) {
    for (let tx = 0; tx < width; tx++) {
      const i = ty * width + tx;
      if (!field.dist[i]) continue;
      const fam = FAMILIES[field.family[i]];
      const tier = TIERS[field.tier[i]];
      const left = tx > 0 ? field.elev[i - 1] : 0;
      const right = tx < width - 1 ? field.elev[i + 1] : 0;
      const lean = right > left ? "r" : "l";
      const h = hashCell(tx * 17 + 5, ty * 31 + 7);
      const variant = "abc"[h % 3];
      // 内がわの中腹・高い山は、ところどころ描かない（谷の地面がのぞき、峰と峰のあいだに谷ができる）
      const gap = field.dist[i] >= 3 && tier !== "peak" && (h >> 7) % 5 === 0;
      if (!gap) sprite[i] = idx(keyIndex, keys, `relief:${fam}-${tier}-${lean}${variant}`);
      jx[i] = ((h >> 3) % 5) - 2;
      jy[i] = ((h >> 5) % 3) - 1;
      // ふち（ななめにも陸がとなる所までふくむ）は、となりの陸の地面。山のすそのすき間から、四角い谷の地面が見えないように
      const land = field.dist[i] <= 2 ? landBeside(map, tx, ty) : null;
      base[i] = land ? idx(baseIndex, bases, `T:${land}`) : idx(baseIndex, bases, `R:relief:valley-${fam}`);
    }
  }
  const plan = { sprite, base, jx, jy, keys, bases };
  planCache.set(map.data, plan);
  return plan;
}

const CHUNK = 16;   // 16×16 マスずつ、絵を1枚のキャンバスにまとめて覚えておく（毎フレーム数百枚の絵を重ねると重いので）
const chunkCache = new WeakMap<ReliefPlan, Map<number, HTMLCanvasElement | null>>();

function drawChunk(map: TileMap, plan: ReliefPlan, cx: number, cy: number): HTMLCanvasElement | null {
  const { width, height } = map.data;
  const x0 = cx * CHUNK, y0 = cy * CHUNK;
  const canvas = document.createElement("canvas");
  canvas.width = CHUNK * ART;
  canvas.height = CHUNK * ART;
  const ctx = canvas.getContext("2d");
  if (!ctx) return null;
  ctx.imageSmoothingEnabled = false;
  const ox = x0 * ART, oy = y0 * ART;
  const baseCanvas = plan.bases.map((b) => (b.startsWith("T:") ? getSpriteCanvas(b.slice(2), SPRITE_DATA) : getSpriteCanvas(b.slice(2), RELIEF_SPRITES)));
  const art = plan.keys.map((k) => getSpriteCanvas(k, RELIEF_SPRITES));
  const shade = plan.keys.map((k) => getSpriteCanvas(`${k}-sh`, RELIEF_SPRITES));
  let drew = false;
  // 1) 地面
  for (let ty = y0; ty < Math.min(height, y0 + CHUNK); ty++) {
    for (let tx = x0; tx < Math.min(width, x0 + CHUNK); tx++) {
      const b = plan.base[ty * width + tx];
      if (b < 0 || !baseCanvas[b]) continue;
      drawWindow(ctx, baseCanvas[b]!, tx, ty, tx * ART - ox, ty * ART - oy);
      drew = true;
    }
  }
  // 2) 山と影（この区画にかかる、まわりのマスの山もふくめて、奥の列から）
  const sx0 = Math.max(0, x0 - 3), sx1 = Math.min(width - 1, x0 + CHUNK + 3);
  const sy0 = Math.max(0, y0 - 2), sy1 = Math.min(height - 1, y0 + CHUNK + 4);
  for (let ty = sy0; ty <= sy1; ty++) {
    for (let pass = 0; pass < 2; pass++) {
      ctx.globalAlpha = pass === 0 ? 1 : 0.26;
      for (let tx = sx0; tx <= sx1; tx++) {
        const i = ty * width + tx;
        const k = plan.sprite[i];
        const img = k < 0 ? null : pass === 0 ? art[k] : shade[k];
        if (!img) continue;
        ctx.drawImage(img, tx * ART + ART / 2 - ANCHOR_X + plan.jx[i] - ox, ty * ART + ART - 2 - ANCHOR_Y + plan.jy[i] - oy);
        drew = true;
      }
    }
  }
  ctx.globalAlpha = 1;
  return drew ? canvas : null;
}

export function renderMountainRelief(ctx: CanvasRenderingContext2D, map: TileMap, camera: Camera): void {
  if (!map.data.tileTexture || map.data.tileWidth !== ART || map.data.tileHeight !== ART) return;
  if (typeof document === "undefined") return;
  const plan = reliefPlanFor(map);
  let cache = chunkCache.get(plan);
  if (!cache) {
    cache = new Map();
    chunkCache.set(plan, cache);
  }
  const size = CHUNK * ART;
  const cols = Math.ceil(map.data.width / CHUNK);
  const c0 = Math.max(0, Math.floor(camera.x / size)), c1 = Math.floor((camera.x + camera.viewportWidth) / size);
  const r0 = Math.max(0, Math.floor(camera.y / size)), r1 = Math.floor((camera.y + camera.viewportHeight) / size);
  ctx.imageSmoothingEnabled = false;
  for (let cy = r0; cy <= r1; cy++) {
    for (let cx = c0; cx <= Math.min(cols - 1, c1); cx++) {
      const key = cy * cols + cx;
      let chunk = cache.get(key);
      if (chunk === undefined) {
        chunk = drawChunk(map, plan, cx, cy);
        cache.set(key, chunk);
      }
      if (chunk) ctx.drawImage(chunk, Math.round(cx * size - camera.x), Math.round(cy * size - camera.y));
    }
  }
}
