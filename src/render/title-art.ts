/**
 * タイトル画面の絵。夜明け前の青い空、メニューをかこむ大きな光の輪、遠くの山と塔（虚灯宮）、丘の上に並ぶ仲間6人（全身のドット絵）。
 * 背景は一度だけ描いて使い回す。キャラクターの全身の絵は、読みこみが終わったら描きなおす。
 */
import yuri from "../assets/title/yuri.png";
import reto from "../assets/title/reto.png";
import mina from "../assets/title/mina.png";
import guide from "../assets/title/guide.png";
import orca from "../assets/title/orca.png";
import ayame from "../assets/title/ayame.png";

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
  const colors = ["#050818", "#070c20", "#0a1228", "#0d1a34", "#10223f", "#142c4a", "#1a3856", "#214660", "#2a5568", "#38666e", "#4d7a72", "#6e8e72", "#a09a70", "#d8aa6e", "#f2c07a"];
  const bh = h * 0.78 / colors.length;
  colors.forEach((c, i) => {
    const y0 = Math.round(i * bh), y1 = Math.round((i + 1) * bh);
    px(ctx, 0, y0, c, w, y1 - y0);
    if (i + 1 < colors.length) {
      for (let x = 0; x < w; x++) if ((x + y1) % 2 === 0) px(ctx, x, y1 - 1, colors[i + 1]);
    }
  });
}

function mountains(ctx: CanvasRenderingContext2D, w: number, base: number, amp: number, seed: number, body: string, rim: string): void {
  for (let x = 0; x < w; x++) {
    const peak = Math.abs(Math.sin(x * 0.028 + seed)) * amp + Math.abs(Math.sin(x * 0.012 + seed * 3)) * amp * 0.7;
    const top = Math.round(base - peak);
    px(ctx, x, top, body, 1, 300);
    px(ctx, x, top, rim, 1, 1);
  }
}

/** 光の輪: 金色の細い輪（外側に向かってぼやけ、内側は夜明けの色にほんのり明るい）。 */
function lightRing(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number): void {
  const inner = ctx.createRadialGradient(cx, cy, 4, cx, cy, r);
  inner.addColorStop(0, "rgba(255, 214, 140, 0.0)");
  inner.addColorStop(0.7, "rgba(255, 200, 120, 0.08)");
  inner.addColorStop(1, "rgba(255, 210, 130, 0.22)");
  ctx.fillStyle = inner;
  ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
  for (let k = 7; k >= 1; k--) {
    ctx.strokeStyle = `rgba(255, 196, 96, ${0.04 * (8 - k)})`;
    ctx.lineWidth = 1 + k * 1.3;
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
  }
  ctx.lineWidth = 3; ctx.strokeStyle = "#f0a840";
  ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
  ctx.lineWidth = 1; ctx.strokeStyle = "#fff0b8";
  ctx.beginPath(); ctx.arc(cx, cy, r - 0.5, 0, Math.PI * 2); ctx.stroke();
  // 輪にそって走る、小さな光の粒
  for (let i = 0; i < 28; i++) {
    const a = hash(i, 11) * Math.PI * 2;
    const rr = r + (hash(i, 12) - 0.5) * 10;
    px(ctx, cx + Math.cos(a) * rr, cy + Math.sin(a) * rr, i % 3 === 0 ? "#fff6d0" : "#ffcf70");
  }
}

function tower(ctx: CanvasRenderingContext2D, cx: number, base: number): void {
  const body = "#0b1424", edge = "#34506a", glow = "#ffe6a0";
  for (let y = 0; y < 84; y++) {
    const tapered = y > 60 ? (84 - y) * 0.45 : 10 - y * 0.05;
    px(ctx, cx - tapered, base - y, body, tapered * 2, 1);
    px(ctx, cx - tapered, base - y, edge, 1, 1);
  }
  for (let k = 0; k < 7; k++) {
    const y = base - 10 - k * 9;
    px(ctx, cx - 5, y, glow, 2, 3); px(ctx, cx + 3, y, glow, 2, 3);
    if (k % 2 === 0) px(ctx, cx - 1, y - 2, glow, 2, 3);
  }
  for (let r = 18; r > 0; r -= 2) {
    ctx.fillStyle = `rgba(255, 224, 150, ${0.035 * (19 - r) / 2})`;
    ctx.beginPath(); ctx.arc(cx, base - 92, r, 0, Math.PI * 2); ctx.fill();
  }
  px(ctx, cx - 2, base - 94, "#fffbe0", 4, 5); px(ctx, cx - 3, base - 92, glow, 6, 1);
  for (const dx of [-16, 16]) {
    for (let y = 0; y < 30; y++) px(ctx, cx + dx - 3, base - y, body, 6, 1);
    px(ctx, cx + dx - 1, base - 20, glow, 2, 3);
    for (let y = 0; y < 6; y++) px(ctx, cx + dx - 3 + y * 0.5, base - 30 - y, body, 6 - y, 1);
  }
}

function pine(ctx: CanvasRenderingContext2D, x: number, y: number, s: number): void {
  for (let k = 0; k < 4; k++) {
    const wd = (3 + k * 2.6) * s, yy = y - 20 * s + k * 5 * s;
    for (let xx = -wd; xx <= wd; xx++) px(ctx, x + xx, yy + Math.abs(xx) * 0.35, xx < -wd * 0.1 ? "#12303a" : "#08181f", 1, 5 * s);
  }
  px(ctx, x - 1, y, "#0c0a10", 2, 4 * s);
}

/** 仲間6人の全身の絵（左から、ふくろの奥→手前）。x は画面の幅に対する位置、size は絵の高さ（画面の高さに対する割合）、depth は奥ほど上げる量。 */
const PARTY: Array<{ img: HTMLImageElement | null; src: string; fx: number; scale: number; depth: number }> = [
  { img: null, src: orca, fx: 0.16, scale: 0.4, depth: 5 },
  { img: null, src: guide, fx: 0.255, scale: 0.42, depth: 3 },
  { img: null, src: ayame, fx: 0.85, scale: 0.4, depth: 5 },
  { img: null, src: mina, fx: 0.75, scale: 0.42, depth: 3 },
  { img: null, src: reto, fx: 0.65, scale: 0.44, depth: 1 },
  { img: null, src: yuri, fx: 0.35, scale: 0.52, depth: 0 },
];
let cached: HTMLCanvasElement | null = null;
let cachedKey = "";
let loading = false;

function loadParty(): void {
  if (loading || typeof Image === "undefined") return;
  loading = true;
  for (const m of PARTY) {
    const img = new Image();
    img.onload = () => {
      m.img = img;
      cached = null;       // 読みこめたら、背景を描きなおす
    };
    img.src = m.src;
  }
}

/** タイトルの背景の絵（キャッシュ）。k は画面の拡大率（描く細かさ）。ブラウザ以外では null。 */
export function getTitleArt(w: number, h: number, k = 1): HTMLCanvasElement | null {
  if (typeof document === "undefined") {
    return null;
  }
  loadParty();
  const key = `${w}x${h}x${k}`;
  if (cached && cachedKey === key) {
    return cached;
  }
  const canvas = document.createElement("canvas");
  // 画面の拡大率 k ぶん、細かく描く（キャラクターの絵を、ぼかさず細部まで出すため）。ドットの背景は、論理座標のまま拡大して描く
  canvas.width = w * k;
  canvas.height = h * k;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return null;
  }
  ctx.scale(k, k);
  ctx.imageSmoothingEnabled = false;
  skyBands(ctx, w, h);
  // 星
  for (let i = 0; i < 140; i++) {
    const y = hash(i, 2) * h * 0.5;
    const a = 1 - y / (h * 0.55);
    ctx.fillStyle = `rgba(235, 244, 255, ${0.3 + 0.7 * a * hash(i, 3)})`;
    ctx.fillRect(Math.floor(hash(i, 1) * w), Math.floor(y), 1, 1);
  }
  // 光の輪（メニューをかこむ）
  lightRing(ctx, w * 0.5, h * 0.66, h * 0.4);
  // 地平線の夜明けのあかり
  const dawn = ctx.createRadialGradient(w * 0.5, h * 0.74, 4, w * 0.5, h * 0.74, w * 0.55);
  dawn.addColorStop(0, "rgba(255, 190, 110, 0.38)");
  dawn.addColorStop(1, "rgba(255, 190, 110, 0)");
  ctx.fillStyle = dawn;
  ctx.fillRect(0, h * 0.4, w, h * 0.4);
  // 遠景の山々
  mountains(ctx, w, h * 0.7, 24, 1.7, "#12304a", "#4a7a8a");
  ctx.save();
  ctx.translate(w * 0.5, h * 0.74);
  ctx.scale(0.46, 0.46);
  tower(ctx, 0, 0);
  ctx.restore();
  mountains(ctx, w, h * 0.77, 16, 5.2, "#0c2236", "#2e5a6a");
  // 霧
  for (let i = 0; i < 4; i++) {
    ctx.fillStyle = `rgba(150, 190, 200, ${0.05 + i * 0.02})`;
    ctx.fillRect(0, h * 0.7 + i * 6, w, 8);
  }
  // 手前の丘と木
  for (let x = 0; x < w; x++) {
    const y = h * 0.82 + Math.sin(x * 0.022 + 1) * 4 + Math.sin(x * 0.07) * 1.4;
    px(ctx, x, y, "#08141f", 1, h);
    px(ctx, x, y, "#2c5a58");
    if ((x + 3) % 4 === 0) px(ctx, x, y + 2, "#12303a");
  }
  for (const [x, s] of [[12, 1.3], [34, 1], [w - 16, 1.4], [w - 40, 1.0]] as Array<[number, number]>) pine(ctx, x, h * 0.86, s);
  for (let i = 0; i < 110; i++) { const x = hash(i, 8) * w, y = h * 0.84 + hash(i, 9) * (h * 0.16); px(ctx, x, y, "#143a3c"); px(ctx, x + 1, y - 1, "#235a54"); }
  // 仲間6人（奥から手前の順）
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
  for (const m of PARTY) {
    if (!m.img) continue;
    const size = Math.round(h * m.scale);       // 絵（256角）の一辺。人は、そのほぼ全高
    const x = Math.round(w * m.fx - size / 2);
    const y = Math.round(h * 0.965 - size - m.depth);
    ctx.fillStyle = "rgba(4, 8, 16, 0.5)";
    ctx.beginPath(); ctx.ellipse(x + size / 2, y + size - 1, size * 0.2, 2.5, 0, 0, Math.PI * 2); ctx.fill();
    ctx.drawImage(m.img, x, y, size, size);
  }
  ctx.imageSmoothingEnabled = false;
  cached = canvas;
  cachedKey = key;
  return canvas;
}
