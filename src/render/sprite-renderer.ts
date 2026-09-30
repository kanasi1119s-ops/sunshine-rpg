import { buildSpritePixels, SPRITE_HEIGHT, SPRITE_WIDTH, spriteRuns, type SpriteDir, type SpriteFrame, type SpriteRun, type SpriteSpec } from "../game/sprite/overworld-sprite";

const cache = new Map<string, SpriteRun[]>();

function runsFor(spec: SpriteSpec, dir: SpriteDir, frame: SpriteFrame): SpriteRun[] {
  const key = `${spec.skin}|${spec.hair}|${spec.top}|${spec.bottom}|${spec.accent}|${spec.hairStyle}|${spec.headband ? 1 : 0}|${dir}|${frame}`;
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
