import { coverMs, isCoverPhase, REVEAL_MS, type BattleTransition } from "../game/battle/battle-transition";

type Ctx = CanvasRenderingContext2D;

function clamp01(v: number): number {
  return Math.max(0, Math.min(1, v));
}

/** 画面全体を黒でうめ、中心に円の穴をあける（穴の半径 r。0なら真っ暗）。 */
function drawIris(ctx: Ctx, w: number, h: number, r: number, ring: boolean): void {
  const cx = w / 2;
  const cy = h / 2;
  ctx.save();
  ctx.fillStyle = "#000";
  ctx.beginPath();
  ctx.rect(0, 0, w, h);
  if (r > 0.5) {
    ctx.arc(cx, cy, r, 0, Math.PI * 2, true);
  }
  ctx.fill("evenodd");
  if (ring && r > 1) {
    ctx.strokeStyle = "rgba(255, 255, 255, 0.85)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.stroke();
    // うずまき（回る光の筋）
    ctx.strokeStyle = "rgba(200, 180, 255, 0.55)";
    ctx.lineWidth = 1;
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2 + r * 0.05;
      ctx.beginPath();
      ctx.arc(cx, cy, r + 6 + i * 2, a, a + 0.6);
      ctx.stroke();
    }
  }
  ctx.restore();
}

function maxRadius(w: number, h: number): number {
  return Math.hypot(w, h) / 2 + 4;
}

/** 前半: フィールドの絵の上に重ねる演出。 */
export function renderTransitionCover(ctx: Ctx, t: BattleTransition, w: number, h: number): void {
  const cover = coverMs(t);
  if (!t.boss) {
    // ひらめき → うずまくように暗くなる
    const flash = clamp01(1 - t.ms / 140);
    const closing = clamp01((t.ms - 100) / (cover - 100));
    drawIris(ctx, w, h, maxRadius(w, h) * (1 - closing) ** 1.6, true);
    if (flash > 0) {
      ctx.fillStyle = `rgba(255, 255, 255, ${0.85 * flash})`;
      ctx.fillRect(0, 0, w, h);
    }
    return;
  }
  // ボス登場
  const ms = t.ms;
  // 赤い警告の脈打ち（最初の1.2秒）
  if (ms < 1500) {
    const pulse = Math.abs(Math.sin(ms / 130)) * clamp01(1 - ms / 1500);
    ctx.fillStyle = `rgba(200, 0, 30, ${0.38 * pulse})`;
    ctx.fillRect(0, 0, w, h);
  }
  // 画面が暗く沈む
  const dark = clamp01((ms - 200) / 900) * 0.62;
  ctx.fillStyle = `rgba(6, 0, 18, ${dark})`;
  ctx.fillRect(0, 0, w, h);
  // 周りをふちどる暗がり
  const vig = ctx.createRadialGradient(w / 2, h / 2, h * 0.3, w / 2, h / 2, w * 0.7);
  vig.addColorStop(0, "rgba(0,0,0,0)");
  vig.addColorStop(1, `rgba(0,0,0,${0.75 * clamp01(ms / 700)})`);
  ctx.fillStyle = vig;
  ctx.fillRect(0, 0, w, h);
  // 黒い帯（映画のように、上下から入る）
  const bar = Math.round(34 * clamp01((ms - 250) / 500));
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, w, bar);
  ctx.fillRect(0, h - bar, w, bar);
  // 走る光の筋
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < 7; i++) {
    const x = ((ms * (0.25 + i * 0.07) + i * 97) % (w + 120)) - 60;
    ctx.fillStyle = `rgba(160, 120, 255, ${0.10 + 0.05 * (i % 3)})`;
    ctx.fillRect(Math.round(x), bar, 2, h - bar * 2);
  }
  ctx.restore();
  // 名前
  const nameIn = clamp01((ms - 800) / 500);
  const nameOut = clamp01((ms - 2250) / 250);
  const alpha = nameIn * (1 - nameOut);
  if (alpha > 0) {
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "bold 22px monospace";
    ctx.shadowColor = "#a060ff";
    ctx.shadowBlur = 12;
    ctx.fillStyle = "#000";
    ctx.fillText(`― ${t.name} ―`, w / 2 + 1, h / 2 - 8 + 1);
    ctx.fillStyle = "#f4ecff";
    ctx.fillText(`― ${t.name} ―`, w / 2, h / 2 - 8);
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = alpha * clamp01((ms - 1300) / 400);
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "11px monospace";
    ctx.fillStyle = "#e8d8ff";
    ctx.fillText("強大な歪みが　立ちはだかる！", w / 2, h / 2 + 18);
    ctx.restore();
  }
  // 最後に白くひらめいて、うずまきで戦闘へ
  const close = clamp01((ms - 2300) / (cover - 2300));
  if (close > 0) {
    drawIris(ctx, w, h, maxRadius(w, h) * (1 - close) ** 1.4, true);
    ctx.fillStyle = `rgba(255, 255, 255, ${0.9 * Math.sin(Math.PI * clamp01((ms - 2300) / 300))})`;
    ctx.fillRect(0, 0, w, h);
  }
}

/** 後半: 戦闘画面の上に重ねる（暗いところから、うずまくようにひらく）。 */
export function renderTransitionReveal(ctx: Ctx, t: BattleTransition, w: number, h: number): void {
  const revealMs = t.boss ? REVEAL_MS.boss : REVEAL_MS.normal;
  const open = clamp01((t.ms - coverMs(t)) / revealMs);
  drawIris(ctx, w, h, maxRadius(w, h) * open ** 0.8, open < 0.98);
  if (t.boss && open < 0.5) {
    ctx.fillStyle = `rgba(255, 255, 255, ${0.5 * (1 - open * 2)})`;
    ctx.fillRect(0, 0, w, h);
  }
}

export { isCoverPhase };
