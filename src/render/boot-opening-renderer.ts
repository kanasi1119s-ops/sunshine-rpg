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
    if (sinceHit > -80 && sinceHit < 900) {
      const a = sinceHit < 0 ? 0.3 : Math.max(0, 1 - sinceHit / 900);
      // 中心から外へ、はっきりした輪の段（5段）で光る
      for (let k = 5; k >= 1; k--) {
        const rx = (w * 0.55 * k) / 5;
        const ry = (h * 0.7 * k) / 5;
        ctx.fillStyle = `rgba(255, 236, 170, ${(0.12 * a * (6 - k)) / 2})`;
        ctx.beginPath();
        ctx.ellipse(Math.round(w / 2), Math.round(h * 0.45), Math.round(rx), Math.round(ry), 0, 0, Math.PI * 2);
        ctx.fill();
      }
      drawSparkles(ctx, w / 2, h * 0.45, Math.max(0, sinceHit));
    }
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
    drawPixelLogoReveal(ctx, title, w / 2, logoY, 2, ms, REVEAL);
    if (after > 0) drawSparkles(ctx, w / 2, logoY, after);
  } else {
    // hold: ロゴを見せたまま、ボタンが押されるまで、ずっと流れつづける
    drawRays(ctx, w / 2, logoY, ms + 3000, 1);
    drawSparkles(ctx, w / 2, logoY, ms);
    drawPixelLogo(ctx, title, w / 2, logoY, 2, (ms % 4200) / 1100, ms + 5000);
    const blink = 0.5 + 0.5 * Math.sin(performance.now() / 380);
    drawPixelText(ctx, "決定ボタン（Enter）で スタート", w / 2, h - 34, "center", 0.35 + 0.65 * blink, { color: "#f2c14e" });
  }
  if (state.phase !== "hold") {
    drawPixelText(ctx, "決定で つぎへ", w - 6, 3, "right", 0.8, { size: 10, color: "#c8c8e0" });
  }
  ctx.textAlign = "left";
}
