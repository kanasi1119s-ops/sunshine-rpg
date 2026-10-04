import { LOGO_LAND_MS, logoDrop, STORY_LINE_HEIGHT, STORY_LINES, STORY_SPEED, type BootOpeningState } from "../game/title/boot-opening";

type Ctx = CanvasRenderingContext2D;

const SS = 3; // ロゴを、論理の3倍の細かさで作っておく
const LOGO_W = 300;
const LOGO_H = 84;

function hash(n: number): number {
  let h = (Math.floor(n) * 374761393) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

let logoCanvas: HTMLCanvasElement | null = null;
let scratch: HTMLCanvasElement | null = null;

/** ロゴの絵（金色の文字・黒いふちどり）を、一度だけ作る。 */
function getLogo(title: string): HTMLCanvasElement | null {
  if (typeof document === "undefined") return null;
  if (logoCanvas) return logoCanvas;
  const c = document.createElement("canvas");
  c.width = LOGO_W * SS;
  c.height = LOGO_H * SS;
  const g = c.getContext("2d");
  if (!g) return null;
  g.scale(SS, SS);
  g.textAlign = "center";
  g.textBaseline = "middle";
  g.lineJoin = "round";
  const main = title.replace(/（.*?）/g, "").replace(/RPG/g, "");
  // 影
  g.font = "bold 40px 'Hiragino Sans','Yu Gothic','Noto Sans JP',sans-serif";
  g.fillStyle = "rgba(0,0,0,0.55)";
  g.fillText(main, LOGO_W / 2 + 2, 30 + 3);
  // ふちどり
  g.strokeStyle = "#2a1204";
  g.lineWidth = 7;
  g.strokeText(main, LOGO_W / 2, 30);
  g.strokeStyle = "#8a5a18";
  g.lineWidth = 3.5;
  g.strokeText(main, LOGO_W / 2, 30);
  // 金のグラデーション
  const grad = g.createLinearGradient(0, 8, 0, 54);
  grad.addColorStop(0, "#fffbe0");
  grad.addColorStop(0.45, "#ffd45c");
  grad.addColorStop(0.55, "#e8a020");
  grad.addColorStop(1, "#a8601a");
  g.fillStyle = grad;
  g.fillText(main, LOGO_W / 2, 30);
  // RPG（小さな飾り枠つき）
  g.font = "bold 22px 'Hiragino Sans','Yu Gothic','Noto Sans JP',sans-serif";
  g.strokeStyle = "#2a1204";
  g.lineWidth = 5;
  g.strokeText("R P G", LOGO_W / 2, 66);
  const grad2 = g.createLinearGradient(0, 54, 0, 78);
  grad2.addColorStop(0, "#ffffff");
  grad2.addColorStop(1, "#9ad8ff");
  g.fillStyle = grad2;
  g.fillText("R P G", LOGO_W / 2, 66);
  // 左右の飾り線
  g.fillStyle = "#ffd45c";
  g.fillRect(LOGO_W / 2 - 100, 66, 56, 1.5);
  g.fillRect(LOGO_W / 2 + 44, 66, 56, 1.5);
  logoCanvas = c;
  return c;
}

/** ロゴに、斜めの光の帯を走らせたもの（ロゴの形の中だけに光る）。 */
function logoWithShine(logo: HTMLCanvasElement, progress: number): HTMLCanvasElement {
  if (!scratch) {
    scratch = document.createElement("canvas");
    scratch.width = logo.width;
    scratch.height = logo.height;
  }
  const g = scratch.getContext("2d")!;
  g.clearRect(0, 0, scratch.width, scratch.height);
  g.drawImage(logo, 0, 0);
  g.save();
  g.globalCompositeOperation = "source-atop";
  const x = (-0.3 + progress * 1.6) * scratch.width;
  const band = g.createLinearGradient(x - 60 * SS, 0, x + 60 * SS, 0);
  band.addColorStop(0, "rgba(255,255,255,0)");
  band.addColorStop(0.5, "rgba(255,255,255,0.9)");
  band.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = band;
  g.fillRect(0, 0, scratch.width, scratch.height);
  g.restore();
  return scratch;
}

function drawStarfield(ctx: Ctx, w: number, h: number, ms: number): void {
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, "#03030c");
  grad.addColorStop(0.65, "#0e0e2a");
  grad.addColorStop(1, "#2a1a3a");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);
  for (let i = 0; i < 110; i++) {
    const x = Math.round(hash(i * 5) * w);
    const y = Math.round(hash(i * 5 + 1) * h);
    ctx.globalAlpha = 0.2 + 0.8 * Math.abs(Math.sin(ms / 800 + i * 2.3));
    ctx.fillStyle = i % 8 === 0 ? "#ffe9a0" : "#dfe8ff";
    ctx.fillRect(x, y, i % 13 === 0 ? 2 : 1, i % 13 === 0 ? 2 : 1);
  }
  ctx.globalAlpha = 1;
}

function drawRays(ctx: Ctx, cx: number, cy: number, ms: number, strength: number): void {
  if (strength <= 0) return;
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2 + ms / 7000;
    const spread = 0.06;
    const grad = ctx.createRadialGradient(cx, cy, 4, cx, cy, 240);
    grad.addColorStop(0, `rgba(255, 220, 140, ${0.28 * strength})`);
    grad.addColorStop(1, "rgba(255, 220, 140, 0)");
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(a - spread) * 300, cy + Math.sin(a - spread) * 300);
    ctx.lineTo(cx + Math.cos(a + spread) * 300, cy + Math.sin(a + spread) * 300);
    ctx.closePath();
    ctx.fill();
  }
  ctx.restore();
}

function drawSparkles(ctx: Ctx, cx: number, cy: number, ms: number): void {
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < 26; i++) {
    const t = ((ms / 1400 + hash(i * 3)) % 1);
    const ang = hash(i * 3 + 1) * Math.PI * 2;
    const r = 20 + t * 130;
    ctx.globalAlpha = (1 - t) * 0.9;
    ctx.fillStyle = i % 3 === 0 ? "#ffffff" : "#ffd45c";
    ctx.fillRect(Math.round(cx + Math.cos(ang) * r * 1.5), Math.round(cy + Math.sin(ang) * r * 0.7), 2, 2);
  }
  ctx.restore();
}

/** 起動のオープニング。 */
export function renderBootOpening(ctx: Ctx, state: BootOpeningState, w: number, h: number, title: string): void {
  if (!state.open) return;
  const ms = state.ms;
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, w, h);
  drawStarfield(ctx, w, h, performance.now());
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";

  if (state.phase === "splash") {
    const fade = Math.min(1, performance.now() / 1200);
    ctx.globalAlpha = fade;
    ctx.font = "12px monospace";
    ctx.fillStyle = "#c8c8e0";
    ctx.fillText("サンシャインソフトウェア  presents", w / 2, h / 2 - 8);
    const blink = 0.5 + 0.5 * Math.sin(performance.now() / 380);
    ctx.globalAlpha = fade * (0.35 + 0.65 * blink);
    ctx.font = "10px monospace";
    ctx.fillStyle = "#f2c14e";
    ctx.fillText("決定ボタン（Enter）で スタート", w / 2, h / 2 + 22);
    ctx.globalAlpha = 1;
    return;
  }

  const logo = getLogo(title);
  const restY = h * 0.4;
  let logoY: number;
  let logoScale = 1;
  let storyMs = 0;
  if (state.phase === "logo") {
    const drop = logoDrop(ms);
    logoY = -LOGO_H + (restY + LOGO_H) * drop;
    // 着地の光とゆれ
    const landed = ms - LOGO_LAND_MS;
    if (landed > 0) {
      drawRays(ctx, w / 2, restY, ms, Math.min(1, landed / 600) * (landed < 3200 ? 1 : Math.max(0, 1 - (landed - 3200) / 600)));
      if (landed < 700) {
        ctx.fillStyle = `rgba(255, 255, 255, ${0.8 * (1 - landed / 700)})`;
        ctx.fillRect(0, 0, w, h);
      }
      drawSparkles(ctx, w / 2, restY, landed);
    }
    // 画面のゆれ（着地の直後）
    if (landed > 0 && landed < 500) {
      const amp = 4 * (1 - landed / 500);
      ctx.save();
      ctx.translate(Math.round((hash(landed / 30) - 0.5) * 2 * amp), Math.round((hash(landed / 30 + 9) - 0.5) * 2 * amp));
      drawLogoAt(ctx, logo, w / 2, logoY, ms - LOGO_LAND_MS - 400, logoScale);
      ctx.restore();
    } else {
      drawLogoAt(ctx, logo, w / 2, logoY, ms - LOGO_LAND_MS - 400, logoScale);
    }
    ctx.font = "9px monospace";
    ctx.fillStyle = `rgba(200, 200, 224, ${landedAlpha(ms)})`;
    ctx.fillText("サンシャインソフトウェア", w / 2, restY + LOGO_H / 2 + 14);
  } else {
    // あらすじ: ロゴが上へ上がって小さくなり、文字が下から上へ流れる
    storyMs = ms;
    const up = Math.min(1, ms / 1200);
    const ease = 1 - (1 - up) ** 3;
    logoScale = 1 - 0.4 * ease;
    logoY = restY + (28 - restY) * ease;
    drawLogoAt(ctx, logo, w / 2, logoY, 99999, logoScale);
    const scroll = (storyMs / 1000) * STORY_SPEED;
    ctx.font = "11px monospace";
    const top = 62;
    STORY_LINES.forEach((line, i) => {
      const y = h - scroll + i * STORY_LINE_HEIGHT;
      if (y < top - 12 || y > h + 4) return;
      // 上と下で、すうっと消える
      const alpha = Math.max(0, Math.min(1, (y - top) / 28)) * Math.max(0, Math.min(1, (h - y) / 22));
      ctx.fillStyle = `rgba(0,0,0,${0.8 * alpha})`;
      ctx.fillText(line, w / 2 + 1, y + 1);
      ctx.fillStyle = `rgba(250, 240, 210, ${alpha})`;
      ctx.fillText(line, w / 2, y);
    });
  }
  ctx.font = "9px monospace";
  ctx.textAlign = "right";
  ctx.textBaseline = "top";
  ctx.fillStyle = "rgba(200, 200, 224, 0.7)";
  ctx.fillText("決定で つぎへ", w - 6, 3);
  ctx.textAlign = "left";
}

function landedAlpha(ms: number): number {
  return Math.max(0, Math.min(1, (ms - LOGO_LAND_MS - 900) / 700));
}

function drawLogoAt(ctx: Ctx, logo: HTMLCanvasElement | null, cx: number, y: number, shineMs: number, scale: number): void {
  if (!logo) return;
  const shineProgress = shineMs < 0 ? -1 : (shineMs % 3600) / 1100;
  const src = shineProgress >= 0 && shineProgress <= 1 ? logoWithShine(logo, shineProgress) : logo;
  const dw = LOGO_W * scale;
  const dh = LOGO_H * scale;
  ctx.save();
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
  ctx.drawImage(src, cx - dw / 2, y - dh / 2, dw, dh);
  ctx.restore();
}
