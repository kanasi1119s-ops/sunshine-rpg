import { OPENING_FADE_MS, OPENING_SCENES, sceneDurationMs, visibleChars, type OpeningScene, type OpeningState } from "../game/title/opening";
import { getNamedBackdrop, type NamedBackdrop } from "./battle-backdrop-images";
import { PORTRAITS } from "../game/portrait/portraits";
import { frameAt } from "../game/sprite/overworld-sprite";
import { spriteSpecFromPortrait } from "../game/sprite/character-specs";
import { drawSprite } from "./sprite-renderer";
import { drawPixelLogo } from "./logo-pixel";

const BAR_TOP = 14;
const BAR_BOTTOM = 52;
const PARTY = ["ユーリ", "レト", "ミナ", "ガイド", "オルカ", "アヤメ"];
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
  const grad = ctx.createLinearGradient(0, a.y, 0, a.y + a.h);
  grad.addColorStop(0, "#04040e");
  grad.addColorStop(0.7, "#10102c");
  grad.addColorStop(1, "#241838");
  ctx.fillStyle = grad;
  ctx.fillRect(a.x, a.y, a.w, a.h);
  for (let i = 0; i < 90; i++) {
    const x = Math.round(hash(i * 5) * a.w);
    const y = Math.round(a.y + hash(i * 5 + 1) * a.h * 0.9);
    ctx.globalAlpha = 0.25 + 0.75 * Math.abs(Math.sin(ms / 700 + i * 2.1));
    ctx.fillStyle = i % 7 === 0 ? "#ffe9a0" : "#dfe8ff";
    ctx.fillRect(x, y, i % 11 === 0 ? 2 : 1, i % 11 === 0 ? 2 : 1);
  }
  ctx.globalAlpha = 1;
}

/** 「灯の環」。光の輪が、ゆっくり回りながら脈打つ。 */
function drawRing(ctx: Ctx, a: Area, ms: number, strength: number): void {
  const cx = a.x + a.w / 2;
  const cy = a.y + a.h * 0.42;
  const pulse = 1 + 0.03 * Math.sin(ms / 600);
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (let k = 0; k < 6; k++) {
    const rx = (74 + k * 3) * pulse;
    const ry = (22 + k * 1.2) * pulse;
    ctx.strokeStyle = `rgba(255, 214, 120, ${(0.55 - k * 0.07) * strength})`;
    ctx.lineWidth = 5 - k * 0.6;
    ctx.beginPath();
    ctx.ellipse(cx, cy, rx, ry, -0.18, 0, Math.PI * 2);
    ctx.stroke();
  }
  // 環にそって流れる光の粒
  for (let i = 0; i < 28; i++) {
    const ang = (i / 28) * Math.PI * 2 + ms / 2500;
    const x = cx + Math.cos(ang) * 74 * pulse;
    const y = cy + Math.sin(ang) * 22 * pulse;
    ctx.fillStyle = `rgba(255, 244, 200, ${0.85 * strength})`;
    ctx.fillRect(Math.round(x), Math.round(y), 2, 2);
  }
  // 環の中心から広がるやわらかい光
  const glow = ctx.createRadialGradient(cx, cy, 4, cx, cy, 120);
  glow.addColorStop(0, `rgba(255, 220, 140, ${0.22 * strength})`);
  glow.addColorStop(1, "rgba(255, 220, 140, 0)");
  ctx.fillStyle = glow;
  ctx.fillRect(a.x, a.y, a.w, a.h);
  ctx.restore();
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
  ctx.fillStyle = `rgba(220, 200, 255, ${0.5 * fade})`;
  ctx.fillRect(a.x, a.y, a.w, a.h);
  ctx.strokeStyle = `rgba(255, 255, 255, ${fade})`;
  ctx.lineWidth = 2;
  ctx.beginPath();
  let x = a.x + a.w * (0.2 + hash(slot) * 0.6);
  let y = a.y;
  ctx.moveTo(x, y);
  for (let i = 0; i < 9; i++) {
    x += (hash(slot * 13 + i) - 0.5) * 36;
    y += a.h / 8;
    ctx.lineTo(Math.round(x), Math.round(y));
  }
  ctx.stroke();
}

/** 中心から広がる光の筋（タイトルの場面）。 */
function drawRays(ctx: Ctx, a: Area, ms: number): void {
  const cx = a.x + a.w / 2;
  const cy = a.y + a.h * 0.5;
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  const n = 14;
  for (let i = 0; i < n; i++) {
    const ang = (i / n) * Math.PI * 2 + ms / 6000;
    const spread = 0.07;
    const grad = ctx.createRadialGradient(cx, cy, 6, cx, cy, 260);
    grad.addColorStop(0, "rgba(255, 224, 150, 0.32)");
    grad.addColorStop(1, "rgba(255, 224, 150, 0)");
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(ang - spread) * 300, cy + Math.sin(ang - spread) * 300);
    ctx.lineTo(cx + Math.cos(ang + spread) * 300, cy + Math.sin(ang + spread) * 300);
    ctx.closePath();
    ctx.fill();
  }
  ctx.restore();
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
  ctx.font = "12px monospace";
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  let remaining = visible;
  lines.forEach((line, i) => {
    const shown = line.slice(0, Math.max(0, remaining));
    remaining -= line.length;
    ctx.fillStyle = "#000000";
    ctx.fillText(shown, x + 1, y + i * 15 + 1);
    ctx.fillStyle = "#f4f0e0";
    ctx.fillText(shown, x, y + i * 15);
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
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.font = "bold 20px monospace";
  ctx.fillStyle = "#000";
  ctx.fillText(text, a.x + a.w / 2 + 1, a.y + a.h * 0.42 + 1);
  ctx.fillStyle = "#ffe9a0";
  ctx.fillText(text, a.x + a.w / 2, a.y + a.h * 0.42);
  ctx.restore();
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
  ctx.imageSmoothingEnabled = true;
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
    ctx.fillStyle = `rgba(255, 255, 255, ${1 - ms / scene.flashMs})`;
    ctx.fillRect(a.x, a.y, a.w, a.h);
  }
  // 場面の頭は暗い状態から現れ、終わりぎわは暗くなる（ひらめく場面は暗くしない）
  const fadeIn = scene.flashMs > 0 ? 0 : Math.max(0, 1 - ms / OPENING_FADE_MS);
  const fadeOut = Math.max(0, 1 - (duration - ms) / SCENE_FADE_OUT_MS);
  const dark = Math.max(fadeIn, fadeOut);
  if (dark > 0) {
    ctx.fillStyle = `rgba(0, 0, 0, ${dark})`;
    ctx.fillRect(a.x, a.y, a.w, a.h);
  }
  // 周辺を暗くして、画面に重みを出す
  const vignette = ctx.createRadialGradient(screenWidth / 2, a.y + a.h / 2, a.h * 0.45, screenWidth / 2, a.y + a.h / 2, screenWidth * 0.62);
  vignette.addColorStop(0, "rgba(0, 0, 0, 0)");
  vignette.addColorStop(1, "rgba(0, 0, 0, 0.55)");
  ctx.fillStyle = vignette;
  ctx.fillRect(a.x, a.y, a.w, a.h);

  drawText(ctx, scene.lines, visibleChars(scene, ms), 16, screenHeight - BAR_BOTTOM + 8);
  ctx.font = "9px monospace";
  ctx.fillStyle = "rgba(200, 200, 224, 0.75)";
  ctx.textAlign = "right";
  ctx.textBaseline = "top";
  ctx.fillText("決定: つぎへ　x・Esc: とばす", screenWidth - 6, 2);
  ctx.textAlign = "left";
}
