/**
 * タイトル画面の絵。黄昏から夜へ向かう空、月、遠くの雪山、灯りをともす塔（虚灯宮）、丘の上に並ぶ主要キャラクター5人。
 * 画像は使わず、一度だけ描いて使い回す。
 */
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import { getSpriteCanvas } from "../game/art/sprite";

function hash(a: number, b: number): number {
  let h = (Math.floor(a) * 374761393 + Math.floor(b) * 668265263) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
function px(ctx: CanvasRenderingContext2D, x: number, y: number, c: string, w = 1, h = 1): void {
  ctx.fillStyle = c;
  ctx.fillRect(Math.round(x), Math.round(y), w, h);
}

function skyBands(ctx: CanvasRenderingContext2D, w: number, h: number): void {
  const colors = ["#0a0c2a", "#0e1236", "#141844", "#1c1c52", "#26225e", "#34286a", "#483076", "#5e3a80", "#7a468a", "#9a5694", "#c0689a", "#e88a9a", "#f8b4a0"];
  const bh = h * 0.72 / colors.length;
  colors.forEach((c, i) => {
    const y0 = Math.round(i * bh), y1 = Math.round((i + 1) * bh);
    px(ctx, 0, y0, c, w, y1 - y0);
    if (i + 1 < colors.length) {
      for (let x = 0; x < w; x++) if ((x + y1) % 2 === 0) px(ctx, x, y1 - 1, colors[i + 1]);
    }
  });
}

function mountains(ctx: CanvasRenderingContext2D, w: number, base: number, amp: number, seed: number, body: string, snow: string, shade: string): void {
  for (let x = 0; x < w; x++) {
    const peak = Math.abs(Math.sin(x * 0.03 + seed)) * amp + Math.abs(Math.sin(x * 0.011 + seed * 3)) * amp * 0.8;
    const top = Math.round(base - peak);
    px(ctx, x, top, body, 1, 300);
    if (peak > amp * 0.9) px(ctx, x, top, snow, 1, Math.round((peak - amp * 0.9) * 0.9));
    if (((x * 7 + seed * 13) | 0) % 5 < 2) px(ctx, x, top + 4, shade, 1, 5);
  }
}

function tower(ctx: CanvasRenderingContext2D, cx: number, base: number): void {
  const body = "#1a1632", edge = "#3a3060", glow = "#ffe6a0";
  // 本体（下が太く、上へ細くなる）
  for (let y = 0; y < 84; y++) {
    const half = 10 - y * 0.05 + (y < 6 ? 0 : 0);
    const tapered = y > 60 ? (84 - y) * 0.45 : half;
    px(ctx, cx - tapered, base - y, body, tapered * 2, 1);
    px(ctx, cx - tapered, base - y, edge, 1, 1);
  }
  // 窓の灯り
  for (let k = 0; k < 7; k++) {
    const y = base - 10 - k * 9;
    px(ctx, cx - 5, y, glow, 2, 3); px(ctx, cx + 3, y, glow, 2, 3);
    if (k % 2 === 0) px(ctx, cx - 1, y - 2, glow, 2, 3);
  }
  // 頂の灯り（大きく光る）と光の筋
  for (let r = 18; r > 0; r -= 2) {
    ctx.fillStyle = `rgba(255, 224, 150, ${0.035 * (19 - r) / 2})`;
    ctx.beginPath(); ctx.arc(cx, base - 92, r, 0, Math.PI * 2); ctx.fill();
  }
  px(ctx, cx - 2, base - 94, "#fffbe0", 4, 5); px(ctx, cx - 3, base - 92, glow, 6, 1);
  // 両脇の小塔
  for (const dx of [-16, 16]) {
    for (let y = 0; y < 30; y++) px(ctx, cx + dx - 3, base - y, body, 6, 1);
    px(ctx, cx + dx - 1, base - 20, glow, 2, 3);
    for (let y = 0; y < 6; y++) px(ctx, cx + dx - 3 + y * 0.5, base - 30 - y, body, 6 - y, 1);
  }
}

function pine(ctx: CanvasRenderingContext2D, x: number, y: number, s: number): void {
  for (let k = 0; k < 4; k++) {
    const wd = (3 + k * 2.6) * s, yy = y - 20 * s + k * 5 * s;
    for (let xx = -wd; xx <= wd; xx++) px(ctx, x + xx, yy + Math.abs(xx) * 0.35, xx < -wd * 0.1 ? "#1c3a3a" : "#0e2428", 1, 5 * s);
  }
  px(ctx, x - 1, y, "#1a1018", 2, 4 * s);
}

let cached: HTMLCanvasElement | null = null;
let cachedKey = "";

/** タイトルの背景の絵（キャッシュ）。ブラウザ以外では null。 */
export function getTitleArt(w: number, h: number): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  const key = `${w}x${h}`;
  if (cached && cachedKey === key) {
    return cached;
  }
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return null;
  }
  ctx.imageSmoothingEnabled = false;
  skyBands(ctx, w, h);
  // 星
  for (let i = 0; i < 120; i++) {
    const y = hash(i, 2) * h * 0.45;
    const a = 1 - y / (h * 0.5);
    ctx.fillStyle = `rgba(255, 250, 230, ${0.35 + 0.65 * a * hash(i, 3)})`;
    ctx.fillRect(Math.floor(hash(i, 1) * w), Math.floor(y), 1, 1);
  }
  // 月（右上）
  const mx = w * 0.82, my = h * 0.2;
  for (let r = 26; r > 12; r -= 2) { ctx.fillStyle = `rgba(255, 244, 210, ${0.02 * (27 - r)})`; ctx.beginPath(); ctx.arc(mx, my, r, 0, Math.PI * 2); ctx.fill(); }
  for (let y = -12; y <= 12; y++) for (let x = -12; x <= 12; x++) {
    const d = x * x + y * y;
    if (d <= 144) px(ctx, mx + x, my + y, x + y < -5 ? "#fffbe8" : d > 100 ? "#e6d8b0" : "#f6ecc8");
  }
  for (const [dx, dy] of [[3, -2], [-4, 3], [5, 5]]) px(ctx, mx + dx, my + dy, "#d4c498", 2, 2);
  // 遠景の山々
  mountains(ctx, w, h * 0.66, 26, 1.3, "#2a2458", "#8a82c0", "#1c1844");
  mountains(ctx, w, h * 0.72, 18, 4.4, "#1e1a40", "#6a62a0", "#140f30");
  tower(ctx, w * 0.3, h * 0.68);
  // 霧
  for (let i = 0; i < 4; i++) {
    ctx.fillStyle = `rgba(160, 130, 200, ${0.05 + i * 0.02})`;
    ctx.fillRect(0, h * 0.62 + i * 6, w, 8);
  }
  // 手前の丘（左から右へ）と木
  for (let x = 0; x < w; x++) {
    const y = h * 0.8 + Math.sin(x * 0.02 + 1) * 5 + Math.sin(x * 0.07) * 1.6;
    px(ctx, x, y, "#12102a", 1, h);
    px(ctx, x, y, "#2e2858");
    if ((x + 3) % 4 === 0) px(ctx, x, y + 2, "#1c1840");
  }
  for (const [x, s] of [[14, 1.3], [38, 1], [w - 20, 1.4], [w - 48, 1.1], [w - 74, 0.9]] as Array<[number, number]>) pine(ctx, x, h * 0.84, s);
  for (let i = 0; i < 90; i++) { const x = hash(i, 8) * w, y = h * 0.84 + hash(i, 9) * (h * 0.16); px(ctx, x, y, "#2a2450"); px(ctx, x + 1, y - 1, "#3a3064"); }
  // 主要キャラクター5人（丘の上、小さく並ぶ）
  const party: Array<[string, number]> = [["ミナ", 0.2], ["レト", 0.36], ["ユーリ", 0.52], ["ガイド", 0.68], ["オルカ", 0.84]];
  party.forEach(([name, fx], i) => {
    const sprite = getSpriteCanvas(`char:${name}`, SPRITE_DATA);
    if (!sprite) return;
    const size = Math.round(sprite.width * 0.66);
    const x = Math.round(w * fx - size / 2);
    const y = Math.round(h * 0.93 - size + (i === 2 ? -4 : 0));
    ctx.fillStyle = "rgba(10, 8, 24, 0.55)";
    ctx.beginPath(); ctx.ellipse(x + size / 2, y + size - 2, size * 0.28, 2.5, 0, 0, Math.PI * 2); ctx.fill();
    ctx.drawImage(sprite, x, y, size, size);
    ctx.fillStyle = "rgba(60, 40, 120, 0.22)";      // 夜の青みをのせる
    ctx.globalCompositeOperation = "source-atop";
    ctx.globalCompositeOperation = "source-over";
  });
  cached = canvas;
  cachedKey = key;
  return canvas;
}
