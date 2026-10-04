import { drawPixelLogo, LOGO_NATIVE_H } from "./logo-pixel";
import { LOGO_LAND_MS, logoDrop, STORY_LINE_HEIGHT, STORY_LINES, STORY_SPEED, type BootOpeningState } from "../game/title/boot-opening";

type Ctx = CanvasRenderingContext2D;

function hash(n: number): number {
  let h = (Math.floor(n) * 374761393) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
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

  const restY = h * 0.4;
  let logoY: number;
  let storyMs = 0;
  if (state.phase === "logo") {
    const drop = logoDrop(ms);
    logoY = -LOGO_NATIVE_H * 2 + (restY + LOGO_NATIVE_H * 2) * drop;
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
      drawLogoAt(ctx, title, w / 2, logoY, ms - LOGO_LAND_MS - 400, 2, ms);
      ctx.restore();
    } else {
      drawLogoAt(ctx, title, w / 2, logoY, ms - LOGO_LAND_MS - 400, 2, ms);
    }
    ctx.font = "9px monospace";
    ctx.fillStyle = `rgba(200, 200, 224, ${landedAlpha(ms)})`;
    ctx.fillText("サンシャインソフトウェア", w / 2, restY + LOGO_NATIVE_H * 2 / 2 + 14);
  } else {
    // あらすじ: ロゴが上へ上がって小さくなり、文字が下から上へ流れる
    storyMs = ms;
    const up = Math.min(1, ms / 1200);
    const ease = 1 - (1 - up) ** 3;
    logoY = restY + (28 - restY) * ease;
    drawLogoAt(ctx, title, w / 2, logoY, 99999, 1, performance.now());
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

function drawLogoAt(ctx: Ctx, title: string, cx: number, y: number, shineMs: number, scale: number, ms: number): void {
  // ドット絵のロゴ。整数倍（2倍、あらすじの間は1倍）で、にじまないように描く
  const shine = shineMs < 0 ? -1 : (shineMs % 3600) / 1100;
  drawPixelLogo(ctx, title, cx, y, scale, shine, ms);
}
