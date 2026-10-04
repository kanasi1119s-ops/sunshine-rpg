import { buildSpritePixels, SPRITE_HEIGHT, SPRITE_WIDTH, spriteRuns, type SpriteDir, type SpriteFrame, type SpriteRun, type SpriteSpec } from "../game/sprite/overworld-sprite";

const cache = new Map<string, SpriteRun[]>();

function runsFor(spec: SpriteSpec, dir: SpriteDir, frame: SpriteFrame): SpriteRun[] {
  const key = `${spec.handKey ?? ""}|${spec.mobTemplate ?? ""}|${spec.skin}|${spec.hair}|${spec.top}|${spec.bottom}|${spec.accent}|${spec.hairStyle}|${spec.headband ? 1 : 0}|${dir}|${frame}`;
  let runs = cache.get(key);
  if (!runs) {
    runs = spriteRuns(buildSpritePixels(spec, dir, frame));
    cache.set(key, runs);
  }
  return runs;
}

/** マップ用のキャラクターの絵（16×32）を、左上が(x, y)になるように描く。 */
export function drawSprite(ctx: CanvasRenderingContext2D, spec: SpriteSpec, dir: SpriteDir, frame: SpriteFrame, x: number, y: number): void {
  const left = Math.round(x);
  const top = Math.round(y);
  for (const run of runsFor(spec, dir, frame)) {
    ctx.fillStyle = run.color;
    ctx.fillRect(left + run.x, top + run.y, run.w, 1);
  }
}

export { SPRITE_HEIGHT, SPRITE_WIDTH };

let scratch: HTMLCanvasElement | null = null;

/** 縮小して描く（世界地図では、主人公・仲間を小さく見せる）。ドットがにじまないよう、いったん別の小さなキャンバスに描いてから、補間なしで縮める。 */
export function drawSpriteScaled(ctx: CanvasRenderingContext2D, spec: SpriteSpec, dir: SpriteDir, frame: SpriteFrame, feetX: number, feetY: number, scale: number): void {
  if (scale >= 1 || typeof document === "undefined") {
    drawSprite(ctx, spec, dir, frame, feetX - SPRITE_WIDTH / 2, feetY - SPRITE_HEIGHT + 1);
    return;
  }
  if (!scratch) {
    scratch = document.createElement("canvas");
    scratch.width = SPRITE_WIDTH;
    scratch.height = SPRITE_HEIGHT;
  }
  const c = scratch.getContext("2d");
  if (!c) {
    return;
  }
  c.clearRect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT);
  drawSprite(c, spec, dir, frame, 0, 0);
  ctx.imageSmoothingEnabled = false;
  const w = Math.round(SPRITE_WIDTH * scale);
  const h = Math.round(SPRITE_HEIGHT * scale);
  ctx.drawImage(scratch, 0, 0, SPRITE_WIDTH, SPRITE_HEIGHT, Math.round(feetX - w / 2), Math.round(feetY - h + 1), w, h);
}
