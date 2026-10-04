import { drawPixelLogo, drawPixelLogoReveal } from "./logo-pixel";
import { OPENING_HIT_MS, REVEAL, STORY_LINE_HEIGHT, STORY_LINES, STORY_SPEED, type BootOpeningState } from "../game/title/boot-opening";

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

/** 集中線の光。なめらかな色のグラデーションではなく、1ドットずつ、3段階の色と市松のディザで描く。 */
function drawRays(ctx: Ctx, cx: number, cy: number, ms: number, strength: number): void {
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


  const logoY = h * 0.42;
  if (state.phase === "story") {
    // 曲のはじまりの一撃（0.9秒）で、星空が光る
    const sinceHit = ms - OPENING_HIT_MS;
    if (sinceHit > -80 && sinceHit < 900) {
      const a = sinceHit < 0 ? 0.3 : Math.max(0, 1 - sinceHit / 900);
      const g = ctx.createRadialGradient(w / 2, h * 0.45, 4, w / 2, h * 0.45, w * 0.55);
      g.addColorStop(0, `rgba(255, 236, 170, ${0.55 * a})`);
      g.addColorStop(1, "rgba(255, 236, 170, 0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);
      drawSparkles(ctx, w / 2, h * 0.45, Math.max(0, sinceHit));
    }
    // あらすじ: 下から上へ流れる
    const scroll = (ms / 1000) * STORY_SPEED;
    ctx.font = "11px monospace";
    const top = 20;
    STORY_LINES.forEach((line, i) => {
      const y = h - scroll + i * STORY_LINE_HEIGHT;
      if (y < top - 12 || y > h + 4) return;
      // 上と下で、すうっと消える
      const alpha = Math.max(0, Math.min(1, (y - top) / 36)) * Math.max(0, Math.min(1, (h - y) / 26));
      ctx.fillStyle = `rgba(0,0,0,${0.8 * alpha})`;
      ctx.fillText(line, w / 2 + 1, y + 1);
      ctx.fillStyle = `rgba(250, 240, 210, ${alpha})`;
      ctx.fillText(line, w / 2, y);
    });
  } else if (state.phase === "reveal") {
    // 光の筋は、文字が現れてから強まる
    const after = ms - REVEAL.gatherEnd;
    drawRays(ctx, w / 2, logoY, ms, Math.max(0, Math.min(1, after / 700)));
    drawPixelLogoReveal(ctx, title, w / 2, logoY, 2, ms, REVEAL);
    if (after > 0) drawSparkles(ctx, w / 2, logoY, after);
  } else {
    // hold: ロゴを見せたまま、ボタンが押されるまで、ずっと流れつづける
    drawRays(ctx, w / 2, logoY, ms + 3000, 1);
    drawSparkles(ctx, w / 2, logoY, ms);
    drawPixelLogo(ctx, title, w / 2, logoY, 2, (ms % 4200) / 1100, ms + 5000);
    const blink = 0.5 + 0.5 * Math.sin(performance.now() / 380);
    ctx.globalAlpha = 0.35 + 0.65 * blink;
    ctx.font = "11px monospace";
    ctx.fillStyle = "#f2c14e";
    ctx.fillText("決定ボタン（Enter）で スタート", w / 2, h - 28);
    ctx.globalAlpha = 1;
  }
  if (state.phase !== "hold") {
    ctx.font = "9px monospace";
    ctx.textAlign = "right";
    ctx.textBaseline = "top";
    ctx.fillStyle = "rgba(200, 200, 224, 0.7)";
    ctx.fillText("決定で つぎへ", w - 6, 3);
  }
  ctx.textAlign = "left";
}
