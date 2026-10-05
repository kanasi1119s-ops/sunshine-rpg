import { drawPixelText } from "./pixel-text";
import { drawBandedSky, drawRays as drawPixelRays } from "./boot-opening-renderer";
import { OPENING_FADE_MS, OPENING_SCENES, sceneDurationMs, visibleChars, type OpeningScene, type OpeningState } from "../game/title/opening";
import { getNamedBackdrop, type NamedBackdrop } from "./battle-backdrop-images";
import { PORTRAITS } from "../game/portrait/portraits";
import { frameAt } from "../game/sprite/overworld-sprite";
import { spriteSpecFromPortrait } from "../game/sprite/character-specs";
import { drawSprite } from "./sprite-renderer";
import { drawPixelLogo } from "./logo-pixel";

const BAR_TOP = 14;
const BAR_BOTTOM = 52;
const PARTY = ["ユーリ", "レト", "ミナ", "コハク", "オルカ", "アヤメ"];
const SCENE_FADE_OUT_MS = 600;

function hash(n: number): number {
  let h = (Math.floor(n) * 374761393) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

type Ctx = CanvasRenderingContext2D;
interface Area { x: number; y: number; w: number; h: number }

/** 星空（夜の背景）。まばらな星がゆっくりまたたく。 */
function drawStarfield(ctx: Ctx, a: Area, ms: number): void {
  drawBandedSky(ctx, a.x, a.y, a.w, a.h);
  for (let i = 0; i < 90; i++) {
    const x = Math.round(hash(i * 5) * a.w);
    const y = Math.round(a.y + hash(i * 5 + 1) * a.h * 0.9);
    ctx.globalAlpha = 0.25 + 0.75 * Math.abs(Math.sin(ms / 700 + i * 2.1));
    ctx.fillStyle = i % 7 === 0 ? "#ffe9a0" : "#dfe8ff";
    ctx.fillRect(x, y, i % 11 === 0 ? 2 : 1, i % 11 === 0 ? 2 : 1);
  }
  ctx.globalAlpha = 1;
}

/** 「灯の環」。1ドットずつ描いた光の輪（中心が白く、外へ金・だいだい、まわりにディザの光）。1回だけ描いてためておく。 */
let ringCache: HTMLCanvasElement | null = null;
function getPixelRing(): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  if (ringCache) return ringCache;
  const rx = 78;
  const ry = 24;
  const tilt = -0.18;
  const W = 2 * (rx + 22);
  const H = 2 * (ry + 22);
  const c = document.createElement("canvas");
  c.width = W;
  c.height = H;
  const g = c.getContext("2d");
  if (!g) return null;
  const cx = W / 2;
  const cy = H / 2;
  const cos = Math.cos(-tilt);
  const sin = Math.sin(-tilt);
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const dx = x + 0.5 - cx;
      const dy = y + 0.5 - cy;
      const lx = dx * cos - dy * sin;
      const ly = dx * sin + dy * cos;
      const d = Math.abs(Math.hypot(lx / rx, ly / ry) - 1) * Math.min(rx, ry);
      const thick = 1.0 + 0.5 * Math.abs(ly / ry);
      let col: string | null = null;
      if (d < thick * 0.7) col = "#ffffff";
      else if (d < thick * 1.5) col = "#ffe070";
      else if (d < thick * 2.5) col = "#f0a020";
      else if (d < thick * 3.8 && (x + y) % 2 === 0) col = "rgba(255, 208, 96, 0.8)";
      else if (d < thick * 5.5 && x % 2 === 0 && y % 2 === 0) col = "rgba(255, 208, 96, 0.45)";
      if (col) {
        g.fillStyle = col;
        g.fillRect(x, y, 1, 1);
      }
    }
  }
  ringCache = c;
  return c;
}

function drawRing(ctx: Ctx, a: Area, ms: number, strength: number): void {
  const cx = Math.round(a.x + a.w / 2);
  const cy = Math.round(a.y + a.h * 0.42);
  const ring = getPixelRing();
  if (ring) {
    const prevSmooth = ctx.imageSmoothingEnabled;
    ctx.imageSmoothingEnabled = false;
    // 脈打ち: ゆっくり、3段階の明るさで
    const beat = Math.floor(2.99 * (0.5 + 0.5 * Math.sin(ms / 600)));
    ctx.globalAlpha = (0.7 + 0.15 * beat) * Math.min(1, strength + 0.15);
    ctx.drawImage(ring, cx - ring.width / 2, cy - ring.height / 2);
    ctx.globalAlpha = 1;
    ctx.imageSmoothingEnabled = prevSmooth;
  }
  // 環にそって流れる光の粒（ドット）
  const cos = Math.cos(-0.18);
  const sin = Math.sin(-0.18);
  for (let i = 0; i < 28; i++) {
    const ang = (i / 28) * Math.PI * 2 + ms / 2500;
    const lx = Math.cos(ang) * 78;
    const ly = Math.sin(ang) * 24;
    const x = cx + lx * cos + ly * sin;
    const y = cy - lx * sin + ly * cos;
    ctx.fillStyle = `rgba(255, 244, 200, ${0.9 * strength})`;
    ctx.fillRect(Math.round(x), Math.round(y), 2, 2);
  }
}

/** 環が砕けて、光のかけらが四方へ飛び散る。 */
function drawShatter(ctx: Ctx, a: Area, ms: number): void {
  const cx = a.x + a.w / 2;
  const cy = a.y + a.h * 0.42;
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < 90; i++) {
    const ang = hash(i * 3) * Math.PI * 2;
    const speed = 30 + hash(i * 3 + 1) * 120;
    const t = ms / 1000;
    const dist = (t * speed) % 260;
    const x = cx + Math.cos(ang) * dist * 1.6;
    const y = cy + Math.sin(ang) * dist * 0.9 + t * t * 14;
    const size = 2 + Math.floor(hash(i * 3 + 2) * 3);
    ctx.fillStyle = i % 3 === 0 ? "#fff4c8" : i % 3 === 1 ? "#ffd070" : "#8ad8ff";
    ctx.globalAlpha = Math.max(0, 1 - dist / 260);
    ctx.fillRect(Math.round(x), Math.round(y), size, size);
    // 尾
    for (let k = 1; k <= 3; k++) {
      ctx.globalAlpha *= 0.6;
      ctx.fillRect(Math.round(x - Math.cos(ang) * k * 3 * 1.6), Math.round(y - Math.sin(ang) * k * 3 * 0.9), size, size);
    }
  }
  ctx.restore();
}

/** 流星（ななめに落ちる光の筋）。 */
function drawMeteors(ctx: Ctx, a: Area, ms: number): void {
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < 12; i++) {
    const period = 1800 + hash(i) * 2400;
    const t = ((ms + hash(i + 40) * period) % period) / period;
    const x = a.x + hash(i + 80) * a.w * 1.2 - a.w * 0.1 + t * 120;
    const y = a.y - 20 + t * (a.h + 40);
    for (let k = 0; k < 14; k++) {
      ctx.globalAlpha = (1 - k / 14) * 0.9 * Math.sin(Math.PI * t);
      ctx.fillStyle = k < 2 ? "#ffffff" : "#ffd98a";
      ctx.fillRect(Math.round(x - k * 3), Math.round(y - k * 3.4), k < 3 ? 2 : 1, k < 3 ? 2 : 1);
    }
  }
  ctx.restore();
}

/** 稲妻（ときどき画面がひらめき、ぎざぎざの線が走る）。 */
function drawLightning(ctx: Ctx, a: Area, ms: number): void {
  const slot = Math.floor(ms / 900);
  const within = ms - slot * 900;
  if (hash(slot * 7) < 0.45 || within > 260) return;
  const fade = 1 - within / 260;
  ctx.fillStyle = `rgba(220, 200, 255, ${0.5 * Math.ceil(fade * 3) / 3})`;
  ctx.fillRect(a.x, a.y, a.w, a.h);
  // ぎざぎざの線を、1ドットずつ
  ctx.fillStyle = "#ffffff";
  let x = a.x + a.w * (0.2 + hash(slot) * 0.6);
  let y = a.y;
  for (let i = 0; i < 9; i++) {
    const nx = x + (hash(slot * 13 + i) - 0.5) * 36;
    const ny = y + a.h / 8;
    const steps = Math.ceil(Math.max(Math.abs(nx - x), Math.abs(ny - y)));
    for (let k = 0; k <= steps; k++) {
      const px = Math.round(x + ((nx - x) * k) / steps);
      const py = Math.round(y + ((ny - y) * k) / steps);
      ctx.fillRect(px, py, 2, 1);
    }
    x = nx;
    y = ny;
  }
}

/** 中心から広がる光の筋（タイトルの場面）。ドットの集中線。 */
function drawRays(ctx: Ctx, a: Area, ms: number): void {
  drawPixelRays(ctx, a.x + a.w / 2, a.y + a.h * 0.5, ms, 1);
}

/** 空をただよう光の粒（ドット）。場面の色で、ゆっくり上へ昇る。 */
function drawSparkles(ctx: Ctx, color: string, a: Area, ms: number): void {
  ctx.fillStyle = color;
  for (let i = 0; i < 36; i++) {
    const speed = 6 + hash(i * 3 + 1) * 14;
    const x = Math.round(hash(i * 3) * a.w + Math.sin(ms / 900 + i) * 4);
    const y = Math.round(a.y + a.h - ((ms / 1000) * speed + hash(i * 3 + 2) * a.h) % a.h);
    ctx.globalAlpha = 0.35 + 0.65 * Math.abs(Math.sin(ms / 500 + i * 1.7));
    const size = i % 5 === 0 ? 2 : 1;
    ctx.fillRect(x, y, size, size);
  }
  ctx.globalAlpha = 1;
}

function drawText(ctx: Ctx, lines: string[], visible: number, x: number, y: number): void {
  let remaining = visible;
  lines.forEach((line, i) => {
    const shown = line.slice(0, Math.max(0, remaining));
    remaining -= line.length;
    // 下の帯（52ドット）に3行が収まるように、行の間は14ドット
    drawPixelText(ctx, shown, x, y + i * 14, "left", 1, { size: 13 });
  });
}

/** 絵の前を、右へ歩く仮のドット絵（2倍）。 */
function drawWalkers(ctx: Ctx, names: string[], w: number, feetY: number, ms: number): void {
  const scale = 2;
  names.forEach((name, i) => {
    const portrait = PORTRAITS[name];
    if (!portrait) return;
    const spec = spriteSpecFromPortrait(portrait, name);
    const x = (((ms / 1000) * 18 - i * 26 + w * 0.15 + 400) % (w + 80)) - 40;
    ctx.save();
    ctx.translate(Math.round(x), Math.round(feetY - 32 * scale));
    ctx.scale(scale, scale);
    drawSprite(ctx, spec, "right", frameAt(true, ms + i * 120), 0, 0);
    ctx.restore();
  });
}

function drawCaption(ctx: Ctx, text: string, a: Area, ms: number, duration: number): void {
  const t = ms / duration;
  const alpha = Math.min(1, Math.max(0, (t - 0.08) / 0.12)) * Math.min(1, Math.max(0, (0.7 - t) / 0.12));
  if (alpha <= 0) return;
  drawPixelText(ctx, text, a.x + a.w / 2, a.y + a.h * 0.42 - 12, "center", Math.round(alpha * 4) / 4, { size: 22, color: "#ffe9a0", bold: true });
}

function drawArt(ctx: Ctx, scene: OpeningScene, a: Area, ms: number, duration: number): void {
  const t = Math.min(1, ms / duration);
  if (scene.art === "stars") {
    drawStarfield(ctx, a, ms);
    return;
  }
  if (scene.art === "title") {
    drawStarfield(ctx, a, ms);
    return;
  }
  const img = getNamedBackdrop(scene.art as NamedBackdrop);
  if (!img) return;
  const zoom = scene.zoom[0] + (scene.zoom[1] - scene.zoom[0]) * t;
  const dw = a.w * zoom;
  const dh = a.h * zoom;
  const pan = scene.pan[0] + (scene.pan[1] - scene.pan[0]) * t;
  ctx.imageSmoothingEnabled = false; // ドット絵の背景は、なめらかに引きのばさない
  ctx.drawImage(img, a.x + (a.w - dw) / 2 + pan, a.y + (a.h - dh) * 0.7, dw, dh);
}

/** オープニング（絵が動き、光の環・流星・稲妻が重なり、下に文字が出る）。 */
export function renderOpening(ctx: Ctx, state: OpeningState, screenWidth: number, screenHeight: number, gameTitle: string): void {
  if (!state.open) return;
  const scene = OPENING_SCENES[state.scene];
  const ms = state.elapsedMs;
  const duration = sceneDurationMs(scene);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, screenWidth, screenHeight);

  const a: Area = { x: 0, y: BAR_TOP, w: screenWidth, h: screenHeight - BAR_TOP - BAR_BOTTOM };
  ctx.save();
  ctx.beginPath();
  ctx.rect(a.x, a.y, a.w, a.h);
  ctx.clip();
  if (scene.shake > 0) {
    ctx.translate(Math.round((hash(ms / 40) - 0.5) * 2 * scene.shake), Math.round((hash(ms / 40 + 99) - 0.5) * 2 * scene.shake));
  }
  drawArt(ctx, scene, a, ms, duration);
  if (scene.tint) {
    ctx.fillStyle = scene.tint;
    ctx.fillRect(a.x - 4, a.y - 4, a.w + 8, a.h + 8);
  }
  switch (scene.overlay) {
    case "ring":
      drawRing(ctx, a, ms, scene.caption ? 0.45 : 1);
      break;
    case "shatter":
      drawShatter(ctx, a, ms);
      break;
    case "meteors":
      drawMeteors(ctx, a, ms);
      break;
    case "lightning":
      drawLightning(ctx, a, ms);
      break;
    case "rays":
      drawRays(ctx, a, ms);
      break;
    default:
      break;
  }
  drawSparkles(ctx, scene.sparkle, a, ms);
  if (scene.sprites === "party") {
    drawWalkers(ctx, PARTY, screenWidth, a.y + a.h - 6, ms);
  } else if (scene.sprites === "hero") {
    drawWalkers(ctx, ["ユーリ"], screenWidth, a.y + a.h - 6, ms);
  }
  if (scene.caption) {
    drawCaption(ctx, scene.caption, a, ms, duration);
  }
  if (scene.art === "title") {
    // 最後は、ドット絵のロゴがふわっと現れる
    const reveal = Math.min(1, Math.max(0, (ms - 500) / 1200));
    ctx.save();
    ctx.globalAlpha = reveal;
    drawPixelLogo(ctx, gameTitle, screenWidth / 2, a.y + a.h / 2, 2, -1, ms);
    ctx.restore();
  }
  ctx.restore();

  // 場面の頭の白いひらめき
  if (scene.flashMs > 0 && ms < scene.flashMs) {
    ctx.fillStyle = `rgba(255, 255, 255, ${Math.ceil((1 - ms / scene.flashMs) * 5) / 5})`;
    ctx.fillRect(a.x, a.y, a.w, a.h);
  }
  // 場面の頭は暗い状態から現れ、終わりぎわは暗くなる（ひらめく場面は暗くしない）
  const fadeIn = scene.flashMs > 0 ? 0 : Math.max(0, 1 - ms / OPENING_FADE_MS);
  const fadeOut = Math.max(0, 1 - (duration - ms) / SCENE_FADE_OUT_MS);
  const dark = Math.max(fadeIn, fadeOut);
  if (dark > 0) {
    ctx.fillStyle = `rgba(0, 0, 0, ${Math.ceil(dark * 8) / 8})`;
    ctx.fillRect(a.x, a.y, a.w, a.h);
  }
  // 周辺を暗くして、画面に重みを出す
  // 周辺を暗くして、画面に重みを出す（はっきりした4段のふち。外ほど重なって濃くなる）
  ctx.fillStyle = "rgba(0, 0, 0, 0.09)";
  for (let k = 1; k <= 4; k++) {
    const t = k * 7;
    ctx.fillRect(a.x, a.y, a.w, t);
    ctx.fillRect(a.x, a.y + a.h - t, a.w, t);
    ctx.fillRect(a.x, a.y + t, t, a.h - t * 2);
    ctx.fillRect(a.x + a.w - t, a.y + t, t, a.h - t * 2);
  }

  drawText(ctx, scene.lines, visibleChars(scene, ms), 16, screenHeight - BAR_BOTTOM + 5);
  drawPixelText(ctx, "決定: つぎへ　x・Esc: とばす", screenWidth - 6, 2, "right", 0.85, { size: 10, color: "#c8c8e0" });
  ctx.textAlign = "left";
}
