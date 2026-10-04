/**
 * タイトル画面の絵。戦闘の背景に使っている草原のドット絵（`battle-bg/meadow.png`）を、夜の色にそめたもの。
 * 空は暗い青にして星と月を足し、草の上に蛍の光を少しちらす。一度だけ描いて使い回す（画面の拡大率ごと）。
 */
import meadow from "../assets/battle-bg/meadow.png";

function hash(a: number, b: number): number {
  let h = (Math.floor(a) * 374761393 + Math.floor(b) * 668265263) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}
function px(ctx: CanvasRenderingContext2D, x: number, y: number, c: string, w = 1, h = 1): void {
  ctx.fillStyle = c;
  ctx.fillRect(Math.round(x), Math.round(y), w, h);
}

let image: HTMLImageElement | null = null;
let loading = false;
let cached: HTMLCanvasElement | null = null;
let cachedKey = "";

function loadImage(): void {
  if (loading || typeof Image === "undefined") return;
  loading = true;
  const img = new Image();
  img.onload = () => {
    image = img;
    cached = null;       // 読みこめたら、描きなおす
  };
  img.src = meadow;
}

/** 草原の絵の色を、夜の色（暗い青）にする。空（明るい青）は、とくに暗くする。星を置く場所（空）を isSky に記録。 */
function nightGrade(src: HTMLImageElement): { canvas: HTMLCanvasElement; isSky: Uint8Array } | null {
  const w = src.width, h = src.height;
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const g = c.getContext("2d", { willReadFrequently: true });
  if (!g) return null;
  g.drawImage(src, 0, 0);
  const img = g.getImageData(0, 0, w, h);
  const d = img.data;
  const isSky = new Uint8Array(w * h);
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      const r = d[i], gg = d[i + 1], b = d[i + 2];
      const sky = y < h * 0.45 && b > r + 25 && b > gg && r + gg + b > 330;
      if (sky) isSky[y * w + x] = 1;
      const lum = (r * 0.3 + gg * 0.59 + b * 0.11) / 255;
      if (sky) {
        // 空: 上ほど暗い紺、地平線に近いほどほんのり明るい青
        const t = y / (h * 0.45);
        d[i] = 10 + t * 26;
        d[i + 1] = 18 + t * 40;
        d[i + 2] = 48 + t * 62;
      } else {
        // 草・木・山: 暗くして、青緑にかたむける（月あかり）。明るい所（雪）は、青白く残す
        d[i] = Math.round(r * 0.2 + 6 + lum * 14);
        d[i + 1] = Math.round(gg * 0.3 + 14 + lum * 16);
        d[i + 2] = Math.round(b * 0.5 + 34 + lum * 30);
      }
    }
  }
  g.putImageData(img, 0, 0);
  return { canvas: c, isSky };
}

/** タイトルの背景の絵（キャッシュ）。k は画面の拡大率（描く細かさ）。ブラウザ以外では null。 */
export function getTitleArt(w: number, h: number, k = 1): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  loadImage();
  const key = `${w}x${h}x${k}`;
  if (cached && cachedKey === key) {
    return cached;
  }
  const canvas = document.createElement("canvas");
  canvas.width = w * k;
  canvas.height = h * k;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return null;
  }
  ctx.scale(k, k);
  ctx.imageSmoothingEnabled = false;
  // 空（草原の絵の上にのびる分）: 上は暗い紺、絵の空につながる色まで
  const graded = image ? nightGrade(image) : null;
  const imgH = image ? image.height : 169;
  const top = h - imgH;                       // 絵の上のへり
  const sky = ctx.createLinearGradient(0, 0, 0, Math.max(1, top));
  sky.addColorStop(0, "#04061a");
  sky.addColorStop(1, "#0a1230");
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, w, h);
  if (graded && image) {
    ctx.drawImage(graded.canvas, Math.round((w - image.width) / 2), top);
    const ox = Math.round((w - image.width) / 2);
    // 星（空の部分だけ）
    for (let i = 0; i < 170; i++) {
      const x = Math.floor(hash(i, 1) * w);
      const y = Math.floor(hash(i, 2) * (top + imgH * 0.42));
      const ix = x - ox, iy = y - top;
      const inSky = iy < 0 || (ix >= 0 && ix < image.width && iy < imgH && graded.isSky[iy * image.width + ix] === 1);
      if (!inSky) continue;
      const a = 0.35 + 0.65 * hash(i, 3);
      ctx.fillStyle = `rgba(235, 244, 255, ${a})`;
      ctx.fillRect(x, y, 1, 1);
      if (i % 17 === 0) { ctx.fillRect(x - 1, y, 3, 1); ctx.fillRect(x, y - 1, 1, 3); }
    }
    // 月（右上）: ほんのり光る輪と、欠けた丸
    const mx = Math.round(w * 0.82), my = Math.round(h * 0.17);
    for (let r = 30; r > 12; r -= 2) { ctx.fillStyle = `rgba(200, 220, 255, ${0.02 * (31 - r) / 1.5})`; ctx.beginPath(); ctx.arc(mx, my, r, 0, Math.PI * 2); ctx.fill(); }
    for (let y = -12; y <= 12; y++) for (let x = -12; x <= 12; x++) {
      const d = x * x + y * y;
      if (d <= 144) px(ctx, mx + x, my + y, x + y < -5 ? "#f4f8ff" : d > 100 ? "#b8c8e0" : "#dce6f6");
    }
    for (const [dx, dy] of [[3, -2], [-4, 3], [5, 5]]) px(ctx, mx + dx, my + dy, "#a8b8d0", 2, 2);
    // 蛍（草の上のちいさな光）
    for (let i = 0; i < 26; i++) {
      const x = hash(i, 21) * w;
      const y = top + imgH * 0.55 + hash(i, 22) * imgH * 0.42;
      ctx.fillStyle = "rgba(210, 255, 150, 0.18)";
      ctx.beginPath(); ctx.arc(x + 0.5, y + 0.5, 3, 0, Math.PI * 2); ctx.fill();
      px(ctx, x, y, i % 3 === 0 ? "#fffbd0" : "#d8ff88");
    }
    // 画面の四すみを少し暗く（文字を読みやすく）
    const vg = ctx.createRadialGradient(w / 2, h * 0.55, h * 0.3, w / 2, h * 0.55, w * 0.62);
    vg.addColorStop(0, "rgba(2, 6, 20, 0)");
    vg.addColorStop(1, "rgba(2, 6, 20, 0.45)");
    ctx.fillStyle = vg;
    ctx.fillRect(0, 0, w, h);
  }
  cached = canvas;
  cachedKey = key;
  return canvas;
}
