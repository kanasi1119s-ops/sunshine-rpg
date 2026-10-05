import { drawPixelText } from "./pixel-text";
import { drawPixelLogo, drawPixelLogoReveal } from "./logo-pixel";
import { OPENING_HIT_MS, REVEAL, STORY_LINE_HEIGHT, STORY_LINES, STORY_SPEED, type BootOpeningState } from "../game/title/boot-opening";

type Ctx = CanvasRenderingContext2D;

function hash(n: number): number {
  let h = (Math.floor(n) * 374761393) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

/** 夜空の背景。なめらかなグラデーションではなく、はっきりした色の帯（ドット絵らしい段）で描く。 */
export function drawBandedSky(ctx: Ctx, x: number, y: number, w: number, h: number): void {
  const stops: [number, [number, number, number]][] = [[0, [3, 3, 12]], [0.65, [14, 14, 42]], [1, [42, 26, 58]]];
  const bands = 14;
  for (let i = 0; i < bands; i++) {
    const t = (i + 0.5) / bands;
    const hi = stops.findIndex(([p]) => p >= t);
    const [p1, c1] = stops[Math.max(0, hi - 1)];
    const [p2, c2] = stops[hi < 0 ? stops.length - 1 : hi];
    const k = p2 === p1 ? 0 : Math.min(1, Math.max(0, (t - p1) / (p2 - p1)));
    const c = c1.map((v, j) => Math.round(v + (c2[j] - v) * k));
    ctx.fillStyle = `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
    ctx.fillRect(x, y + Math.floor((i * h) / bands), w, Math.ceil(h / bands) + 1);
  }
}

function drawStarfield(ctx: Ctx, w: number, h: number, ms: number): void {
  drawBandedSky(ctx, 0, 0, w, h);
  for (let i = 0; i < 110; i++) {
    const x = Math.round(hash(i * 5) * w);
    const y = Math.round(hash(i * 5 + 1) * h);
    ctx.globalAlpha = 0.2 + 0.8 * Math.abs(Math.sin(ms / 800 + i * 2.3));
    ctx.fillStyle = i % 8 === 0 ? "#ffe9a0" : "#dfe8ff";
    ctx.fillRect(x, y, i % 13 === 0 ? 2 : 1, i % 13 === 0 ? 2 : 1);
  }
  ctx.globalAlpha = 1;
}

/** 集中線の光。なめらかな色のグラデーションではなく、1ドットずつ、3段階の色と市松のディザで描く。 */
export function drawRays(ctx: Ctx, cx: number, cy: number, ms: number, strength: number): void {
  if (strength <= 0) return;
  ctx.save();
  const colors = ["#fff4c0", "#ffd45c", "#c8802a"];
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2 + ms / 9000;
    const cos = Math.cos(a);
    const sin = Math.sin(a);
    const len = (i % 2 === 0 ? 210 : 140) * strength;
    const half = i % 2 === 0 ? 5 : 3; // 根もとの太さ（ドット）
    for (let d = 14; d < len; d++) {
      const t = d / len;
      const width = Math.max(0, Math.round(half * (1 - t)));
      const level = t < 0.3 ? 0 : t < 0.65 ? 1 : 2;
      for (let o = -width; o <= width; o++) {
        const x = Math.round(cx + cos * d - sin * o);
        const y = Math.round(cy + sin * d + cos * o);
        // 先へいくほどまばらに（市松）。ふちは1つおき
        if (level === 2 && (x + y) % 2 !== 0) continue;
        if (level === 1 && Math.abs(o) === width && width > 0 && (x + y) % 2 !== 0) continue;
        ctx.fillStyle = colors[level];
        ctx.fillRect(x, y, 1, 1);
      }
    }
  }
  ctx.restore();
}

/** ドットの火花。半透明やにじみは使わず、1〜2ドットの十字を、色の段で描く（遠くなるほど暗い色、ところどころ消える）。 */
function drawSparkles(ctx: Ctx, cx: number, cy: number, ms: number): void {
  ctx.save();
  for (let i = 0; i < 26; i++) {
    const t = ((ms / 1400 + hash(i * 3)) % 1);
    if (hash(i * 7 + Math.floor(t * 8)) < t * 0.6) continue; // 終わりに近いほど、ちらついて消える
    const ang = hash(i * 3 + 1) * Math.PI * 2;
    const r = 20 + t * 130;
    const x = Math.round(cx + Math.cos(ang) * r * 1.5);
    const y = Math.round(cy + Math.sin(ang) * r * 0.7);
    ctx.fillStyle = t < 0.5 ? (i % 3 === 0 ? "#ffffff" : "#fff4c0") : t < 0.8 ? "#ffd45c" : "#c8802a";
    ctx.fillRect(x, y, 2, 2);
    if (i % 4 === 0 && t < 0.6) {
      ctx.fillRect(x - 2, y, 2, 2);
      ctx.fillRect(x + 2, y, 2, 2);
      ctx.fillRect(x, y - 2, 2, 2);
      ctx.fillRect(x, y + 2, 2, 2);
    }
  }
  ctx.restore();
}

/** ビッグバンが続く時間（ms。曲の一撃から）。 */
export const BIGBANG_MS = 2800;

const clamp01 = (x: number): number => Math.min(1, Math.max(0, x));
const easeOutCubic = (x: number): number => 1 - Math.pow(1 - clamp01(x), 3);
const BAYER4 = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];

/** 火の色の段（若い光ほど白く、年をとると赤・紫・暗い青へ）。 */
const FIRE = ["#ffffff", "#fff4c0", "#ffd45c", "#ff9a30", "#e8502a", "#a02a50", "#5a2a6a", "#2a2a6a"];
const fireColor = (age: number): string => FIRE[Math.min(FIRE.length - 1, Math.floor(clamp01(age) * FIRE.length))];

function px(ctx: Ctx, x: number, y: number, size: number, color: string): void {
  ctx.fillStyle = color;
  ctx.fillRect(Math.round(x), Math.round(y), size, size);
}

/** 円（だ円）のふちを、1〜2ドットの点でなぞる。fade が大きいほど、点が抜けていく（半透明は使わない）。 */
function pixelRing(ctx: Ctx, cx: number, cy: number, rx: number, ry: number, color: string, thick: number, fade: number, seed = 0): void {
  const n = Math.max(24, Math.round(((rx + ry) * Math.PI) / 1.6));
  for (let i = 0; i < n; i++) {
    if (hash(seed * 977 + i) < fade) continue;
    const a = (i / n) * Math.PI * 2;
    px(ctx, cx + Math.cos(a) * rx - thick / 2, cy + Math.sin(a) * ry - thick / 2, thick, color);
  }
}

/** 画面ぜんたいの白いひらめき。ベイヤー行列のディザで、白→透けていく（半透明ではない）。 */
function ditherFlash(ctx: Ctx, w: number, h: number, level: number, color: string): void {
  if (level <= 0) return;
  ctx.fillStyle = color;
  const cell = 2;
  const th = level * 16;
  for (let y = 0; y < h; y += cell) {
    for (let x = 0; x < w; x += cell) {
      if (BAYER4[((y / cell) % 4) * 4 + ((x / cell) % 4)] < th) ctx.fillRect(x, y, cell, cell);
    }
  }
}

/**
 * 曲のはじまりの一撃で起きる「ビッグバン」を、ドット絵で描く（全部ドット。半透明・ぼかしは使わない）。
 *  1. 画面全体が白くひらめき、ふるえる
 *  2. 白い核がふくらみ、火の色の段の球になる。十字の光の筋と、集中線がのびる
 *  3. 衝撃の輪が3つ、外へ広がる。火花（ふき出す粒）が、尾を引いて飛ぶ
 *  4. 球はしぼみ、金色の「灯の環」だけが残って、ゆっくり回る。やがて環はくだけ、かけらと火の粉になって消える
 */
function drawBigBang(ctx: Ctx, w: number, h: number, sinceHit: number, block = 1): void {
  if (block > 1 && typeof document !== "undefined") {
    const small = document.createElement("canvas");
    small.width = Math.ceil(w / block);
    small.height = Math.ceil(h / block);
    drawBigBang(small.getContext("2d")!, small.width, small.height, sinceHit, 1);
    ctx.save();
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(small, 0, 0, small.width * block, small.height * block);
    ctx.restore();
    return;
  }
  const cx = Math.round(w / 2), cy = Math.round(h * 0.45);
  const R0 = Math.min(w, h * 1.2) * 0.5;               // 基準の半径
  const aspect = w > h ? (h / w) * 1.24 : 1;           // 横長の画面はだ円、縦長は円
  const t = sinceHit;
  ctx.save();
  if (t < 0) {
    // 一撃の直前: 小さな白い点が、ふるえながら大きくなる
    const grow = Math.max(0, (t + 80) / 80);
    const r = 1 + Math.round(grow * 3);
    px(ctx, cx - r - 2, cy - r - 2, (r + 2) * 2 + 1, FIRE[3]);
    px(ctx, cx - r, cy - r, r * 2 + 1, FIRE[0]);
    ctx.restore();
    return;
  }
  // ふるえ（最初の0.45秒）
  if (t < 450) {
    const k = (1 - t / 450) * 3;
    ctx.translate(Math.round((hash(Math.floor(t / 33) * 3) - 0.5) * 2 * k), Math.round((hash(Math.floor(t / 33) * 3 + 1) - 0.5) * 2 * k));
  }

  // --- 核（火の色の段の球）: 0〜1100msでふくらみ、そのあとしぼむ ---
  const grow = easeOutCubic(t / 650);
  const shrink = t < 900 ? 1 : Math.max(0, 1 - (t - 900) / 700);
  const coreR = R0 * 0.62 * grow * (0.35 + 0.65 * shrink);
  if (coreR > 1) {
    const rings = FIRE.length - 2;
    for (let k = rings - 1; k >= 0; k--) {
      const frac = (k + 1) / rings;
      const rr = Math.round(coreR * frac);
      const fadingOut = t > 700 + (1 - frac) * 400;
      ctx.fillStyle = FIRE[k];
      for (let dy = -Math.round(rr * aspect); dy <= Math.round(rr * aspect); dy++) {
        const ry = Math.max(1, rr * aspect);
        const half = Math.round(rr * Math.sqrt(Math.max(0, 1 - (dy * dy) / (ry * ry))));
        if (half <= 0) continue;
        if (!fadingOut) ctx.fillRect(cx - half, cy + dy, half * 2 + 1, 1);
        else {
          for (let dx = -half; dx <= half; dx += 1) if (BAYER4[((cy + dy) & 3) * 4 + ((cx + dx) & 3)] < 9) ctx.fillRect(cx + dx, cy + dy, 1, 1);
        }
      }
    }
  }

  // --- 十字の光の筋（0〜900ms、先にいくほど細くなる）---
  const flare = t < 150 ? t / 150 : Math.max(0, 1 - (t - 150) / 750);
  if (flare > 0) {
    const len = R0 * 1.7 * flare;
    for (let step = 0; step < 3; step++) {
      const th = 3 - step;                               // 太さ 3→1
      const l = len * (1 - step * 0.28);
      const col = [FIRE[0], FIRE[1], FIRE[2]][step];
      ctx.fillStyle = col;
      ctx.fillRect(Math.round(cx - l), cy - Math.floor(th / 2), Math.round(l * 2), th);
      ctx.fillRect(cx - Math.floor(th / 2), Math.round(cy - l * aspect * 1.2), th, Math.round(l * aspect * 2.4));
    }
  }

  // --- 集中線 ---
  const ray = t < 200 ? t / 200 : Math.max(0, 1 - (t - 200) / 1100);
  drawRays(ctx, cx, cy, t * 3, ray);

  // --- 衝撃の輪（3つ）---
  for (let i = 0; i < 3; i++) {
    const t0 = i * 170;
    const u = (t - t0) / 1300;
    if (u <= 0 || u >= 1) continue;
    const rr = R0 * 1.55 * easeOutCubic(u);
    pixelRing(ctx, cx, cy, rr, rr * aspect, fireColor(u * 0.9), u < 0.4 ? 3 : 2, u * u, i + 1);
  }

  // --- 火花（ふき出す粒。尾を引く）---
  for (let i = 0; i < 64; i++) {
    const ang = hash(i * 11 + 2) * Math.PI * 2;
    const speed = 0.55 + hash(i * 11 + 3) * 1.1;
    const life = 900 + hash(i * 11 + 4) * 1100;
    const u = t / life;
    if (u >= 1) continue;
    const dist = R0 * speed * easeOutCubic(u) * 1.25;
    const x = cx + Math.cos(ang) * dist, y = cy + Math.sin(ang) * dist * aspect + u * u * R0 * 0.25;
    if (hash(i * 11 + 5 + Math.floor(t / 70)) < u * 0.55) continue;     // 終わりに近いほど、ちらつく
    const col = fireColor(u);
    px(ctx, x, y, u < 0.5 ? 2 : 1, col);
    // 尾
    for (let k = 1; k <= 3; k++) {
      const du = Math.max(0, u - k * 0.03);
      const d2 = R0 * speed * easeOutCubic(du) * 1.25;
      px(ctx, cx + Math.cos(ang) * d2, cy + Math.sin(ang) * d2 * aspect + du * du * R0 * 0.25, 1, fireColor(Math.min(1, u + k * 0.12)));
    }
  }

  // --- 灯の環（くだけてのこる、金色の輪）---
  if (t > 500) {
    const u = clamp01((t - 500) / 400);
    const ringR = R0 * 0.66 * easeOutCubic(u);
    const shatter = t > 1700 ? clamp01((t - 1700) / 1000) : 0;
    const spin = t / 900;
    const n = 90;
    for (let i = 0; i < n; i++) {
      const seg = Math.floor(i / 6);                       // 6点ずつが1つのかけら
      if (shatter > 0 && hash(seg * 31 + 7) < shatter * 1.1) {
        // かけらが、外へ飛んで消える
        const drift = shatter * R0 * (0.3 + hash(seg * 31 + 8) * 0.9);
        const a = (i / n) * Math.PI * 2;
        if (hash(i * 13 + Math.floor(t / 60)) < shatter) continue;
        px(ctx, cx + Math.cos(a) * (ringR + drift), cy + Math.sin(a) * (ringR + drift) * aspect, 2, fireColor(0.15 + shatter * 0.7));
        continue;
      }
      const a = (i / n) * Math.PI * 2;
      const glint = Math.cos(a - spin * 2) > 0.92;         // 回る光の点
      px(ctx, cx + Math.cos(a) * ringR - 1, cy + Math.sin(a) * ringR * aspect - 1, glint ? 3 : 2, glint ? FIRE[0] : i % 2 ? FIRE[2] : FIRE[3]);
    }
  }

  // --- 火の粉（ゆっくり落ちる）---
  if (t > 700) {
    for (let i = 0; i < 40; i++) {
      const born = 700 + hash(i * 17 + 1) * 900;
      const u = (t - born) / 1700;
      if (u <= 0 || u >= 1) continue;
      const x = cx + (hash(i * 17 + 2) - 0.5) * R0 * 2.2 + Math.sin(u * 6 + i) * 4;
      const y = cy + (hash(i * 17 + 3) - 0.5) * R0 * aspect * 1.2 + u * R0 * 0.8;
      if (hash(i * 17 + 4 + Math.floor(t / 90)) < u * 0.6) continue;
      px(ctx, x, y, 1, fireColor(0.1 + u * 0.8));
    }
  }

  // --- 最初のひらめき（画面ぜんたい）---
  if (t < 200) ditherFlash(ctx, w, h, 1 - t / 200, "#fff8e0");
  drawSparkles(ctx, cx, cy, t);
  ctx.restore();
}

/** 起動のオープニング。 */
export function renderBootOpening(ctx: Ctx, state: BootOpeningState, w: number, h: number, title: string, logoScale = 2, bangBlock = 1): void {
  if (!state.open) return;
  const ms = state.ms;
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, w, h);
  drawStarfield(ctx, w, h, performance.now());
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  if (state.phase === "splash") {
    // 英語だけの表記。ゆっくり現れ、「TAP」の案内がまたたく
    const fade = Math.min(1, performance.now() / 1400);
    drawPixelText(ctx, "SUNSHINE SOFTWARE", w / 2, h / 2 - 22, "center", fade, { size: 20, color: "#f2c14e", bold: true });
    drawPixelText(ctx, "PRESENTS", w / 2, h / 2 + 4, "center", fade, { size: 12, color: "#c8c8e0" });
    const blink = 0.5 + 0.5 * Math.sin(performance.now() / 380);
    drawPixelText(ctx, "TAP or PRESS ENTER", w / 2, h / 2 + 46, "center", fade * (0.3 + 0.7 * blink), { size: 10, color: "#f2c14e" });
    return;
  }


  const logoY = h * 0.42;
  if (state.phase === "story") {
    // 曲のはじまりの一撃（0.9秒）で、星空が光る
    const sinceHit = ms - OPENING_HIT_MS;
    if (sinceHit > -80 && sinceHit < BIGBANG_MS) drawBigBang(ctx, w, h, sinceHit, bangBlock);
    // あらすじ: 下から上へ流れる
    const scroll = (ms / 1000) * STORY_SPEED;
    const top = 20;
    STORY_LINES.forEach((line, i) => {
      const y = h - scroll + i * STORY_LINE_HEIGHT;
      if (y < top - 12 || y > h + 4) return;
      // 上と下で、すうっと消える
      const alpha = Math.max(0, Math.min(1, (y - top) / 36)) * Math.max(0, Math.min(1, (h - y) / 26));
      drawPixelText(ctx, line, w / 2, y - 6, "center", alpha, { size: 13 });
    });
  } else if (state.phase === "reveal") {
    // 光の筋は、文字が現れてから強まる
    const after = ms - REVEAL.gatherEnd;
    drawRays(ctx, w / 2, logoY, ms, Math.max(0, Math.min(1, after / 700)));
    drawPixelLogoReveal(ctx, title, w / 2, logoY, logoScale, ms, REVEAL);
    if (after > 0) drawSparkles(ctx, w / 2, logoY, after);
  } else {
    // hold: ロゴを見せたまま、ボタンが押されるまで、ずっと流れつづける
    drawRays(ctx, w / 2, logoY, ms + 3000, 1);
    drawSparkles(ctx, w / 2, logoY, ms);
    drawPixelLogo(ctx, title, w / 2, logoY, logoScale, (ms % 4200) / 1100, ms + 5000);
    const blink = 0.5 + 0.5 * Math.sin(performance.now() / 380);
    drawPixelText(ctx, "決定ボタン（Enter）で スタート", w / 2, h - 34, "center", 0.35 + 0.65 * blink, { color: "#f2c14e" });
  }
  if (state.phase !== "hold") {
    drawPixelText(ctx, "決定で つぎへ", w - 6, 3, "right", 0.8, { size: 10, color: "#c8c8e0" });
  }
  ctx.textAlign = "left";
}
