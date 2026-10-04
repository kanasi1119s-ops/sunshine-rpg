import { OPENING_FADE_MS, OPENING_SCENES, sceneDurationMs, visibleChars, type OpeningState } from "../game/title/opening";
import { getNamedBackdrop, type NamedBackdrop } from "./battle-backdrop-images";
import { PORTRAITS } from "../game/portrait/portraits";
import { frameAt } from "../game/sprite/overworld-sprite";
import { spriteSpecFromPortrait } from "../game/sprite/character-specs";
import { drawSprite } from "./sprite-renderer";

const BAR_TOP = 14;
const BAR_BOTTOM = 52;
const PARTY = ["ユーリ", "レト", "ミナ", "ガイド", "オルカ", "アヤメ"];
const SCENE_FADE_OUT_MS = 500;

function hash(n: number): number {
  let h = (Math.floor(n) * 374761393) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

/** 空をただよう光の粒（ドット）。場面の色で、ゆっくり上へ昇る。 */
function drawSparkles(ctx: CanvasRenderingContext2D, color: string, w: number, h: number, ms: number): void {
  ctx.fillStyle = color;
  for (let i = 0; i < 36; i++) {
    const speed = 6 + hash(i * 3 + 1) * 14;
    const x = Math.round(hash(i * 3) * w + Math.sin(ms / 900 + i) * 4);
    const y = Math.round(h - ((ms / 1000) * speed + hash(i * 3 + 2) * h) % h);
    const twinkle = 0.35 + 0.65 * Math.abs(Math.sin(ms / 500 + i * 1.7));
    ctx.globalAlpha = twinkle;
    const size = i % 5 === 0 ? 2 : 1;
    ctx.fillRect(x, y, size, size);
  }
  ctx.globalAlpha = 1;
}

function drawText(ctx: CanvasRenderingContext2D, lines: string[], visible: number, x: number, y: number): void {
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

/** 絵の前を、右へ歩く仮のドット絵（3倍）。 */
function drawWalkers(ctx: CanvasRenderingContext2D, names: string[], w: number, feetY: number, ms: number): void {
  const scale = 2;
  names.forEach((name, i) => {
    const portrait = PORTRAITS[name];
    if (!portrait) return;
    const spec = spriteSpecFromPortrait(portrait, name);
    const x = ((ms / 1000) * 18 - i * 26 + w * 0.15 + 400) % (w + 80) - 40;
    ctx.save();
    ctx.translate(Math.round(x), Math.round(feetY - 32 * scale));
    ctx.scale(scale, scale);
    drawSprite(ctx, spec, "right", frameAt(true, ms + i * 120), 0, 0);
    ctx.restore();
  });
}

/** オープニング（絵がゆっくり寄っていき、光の粒がただよい、下に文字が出る）。 */
export function renderOpening(ctx: CanvasRenderingContext2D, state: OpeningState, screenWidth: number, screenHeight: number, gameTitle: string): void {
  if (!state.open) return;
  const scene = OPENING_SCENES[state.scene];
  const ms = state.elapsedMs;
  const duration = sceneDurationMs(scene);
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, screenWidth, screenHeight);

  const areaY = BAR_TOP;
  const areaH = screenHeight - BAR_TOP - BAR_BOTTOM;
  ctx.save();
  ctx.beginPath();
  ctx.rect(0, areaY, screenWidth, areaH);
  ctx.clip();
  if (scene.art === "title") {
    const grad = ctx.createLinearGradient(0, areaY, 0, areaY + areaH);
    grad.addColorStop(0, "#0a0a22");
    grad.addColorStop(1, "#3a2a50");
    ctx.fillStyle = grad;
    ctx.fillRect(0, areaY, screenWidth, areaH);
  } else {
    const img = getNamedBackdrop(scene.art as NamedBackdrop);
    if (img) {
      // ゆっくり寄っていく（1.0倍→1.12倍）
      const t = Math.min(1, ms / duration);
      const zoom = 1 + 0.12 * t;
      const dw = screenWidth * zoom;
      const dh = areaH * zoom;
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(img, (screenWidth - dw) / 2, areaY + (areaH - dh) * 0.7, dw, dh);
    }
  }
  drawSparkles(ctx, scene.sparkle, screenWidth, areaH, ms);
  if (scene.sprites === "party") {
    drawWalkers(ctx, PARTY, screenWidth, areaY + areaH - 6, ms);
  } else if (scene.sprites === "hero") {
    drawWalkers(ctx, ["ユーリ"], screenWidth, areaY + areaH - 6, ms);
  }
  if (scene.art === "title") {
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "bold 22px monospace";
    ctx.fillStyle = "#000";
    ctx.fillText(gameTitle, screenWidth / 2 + 1, areaY + areaH / 2 + 1);
    ctx.fillStyle = "#f2c14e";
    ctx.fillText(gameTitle, screenWidth / 2, areaY + areaH / 2);
    ctx.textAlign = "left";
  }
  ctx.restore();

  // 場面の頭は暗い状態から現れ、終わりぎわは暗くなる
  const fadeIn = Math.max(0, 1 - ms / OPENING_FADE_MS);
  const fadeOut = Math.max(0, 1 - (duration - ms) / SCENE_FADE_OUT_MS);
  const dark = Math.max(fadeIn, fadeOut);
  if (dark > 0) {
    ctx.fillStyle = `rgba(0, 0, 0, ${dark})`;
    ctx.fillRect(0, areaY, screenWidth, areaH);
  }

  drawText(ctx, scene.lines, visibleChars(scene, ms), 16, screenHeight - BAR_BOTTOM + 8);
  ctx.font = "9px monospace";
  ctx.fillStyle = "rgba(200, 200, 224, 0.75)";
  ctx.textAlign = "right";
  ctx.textBaseline = "top";
  ctx.fillText("決定: つぎへ　x・Esc: とばす", screenWidth - 6, 2);
  ctx.textAlign = "left";
}
