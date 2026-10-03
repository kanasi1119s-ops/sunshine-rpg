import { getSpriteCanvas } from "../game/art/sprite";
import { SPRITE_DATA } from "../game/art/sprite-data.generated";
import type { Direction } from "../input/direction";

/**
 * 船・飛空艇の絵。専用のドット絵（`prop:ship-<向き>` `prop:airship-<向き>-<コマ>`）があればそれを、なければ簡易な絵を描く。
 * (x, y) は足元の中央（画面の座標）。
 */
function spriteOr(key: string): HTMLCanvasElement | null {
  return getSpriteCanvas(key, SPRITE_DATA) ?? null;
}

function shipFallback(ctx: CanvasRenderingContext2D, x: number, y: number, dir: Direction): void {
  const flip = dir === "left" ? -1 : 1;
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(flip, 1);
  ctx.fillStyle = "rgba(255,255,255,0.7)";
  ctx.fillRect(-18, 1, 8, 2);
  ctx.fillStyle = "#2a1a10";
  ctx.fillRect(-12, -7, 26, 9);
  ctx.fillStyle = "#8a5a2c";
  ctx.fillRect(-11, -6, 24, 7);
  ctx.fillStyle = "#6a4220";
  ctx.fillRect(-2, -6, 15, 7);
  ctx.fillStyle = "#e8dcc0";
  ctx.fillRect(-1, -22, 1, 16);
  ctx.fillStyle = "#f4f0e0";
  ctx.fillRect(0, -21, 9, 13);
  ctx.fillStyle = "#c8c0a8";
  ctx.fillRect(5, -19, 4, 11);
  ctx.restore();
}

function airshipFallback(ctx: CanvasRenderingContext2D, x: number, y: number, dir: Direction, frame: number): void {
  ctx.fillStyle = "rgba(0,0,0,0.25)";
  ctx.fillRect(x - 10, y + 4, 20, 4);
  ctx.fillStyle = "#2a2430";
  ctx.fillRect(x - 14, y - 18, 28, 12);
  ctx.fillStyle = "#c8553c";
  ctx.fillRect(x - 13, y - 17, 26, 10);
  ctx.fillStyle = "#8a3a2c";
  ctx.fillRect(x + 2, y - 17, 11, 10);
  ctx.fillStyle = "#e8dcc0";
  ctx.fillRect(x - 6, y - 8, 12, 5);
  const wing = frame % 2 === 0 ? 0 : 2;
  ctx.fillStyle = "#586070";
  ctx.fillRect(x - 20, y - 14 + wing, 7, 3);
  ctx.fillRect(x + 13, y - 14 + wing, 7, 3);
  void dir;
}

export function drawShip(ctx: CanvasRenderingContext2D, x: number, y: number, dir: Direction, docked = false): void {
  const sprite = (docked ? spriteOr("prop:ship-docked") : null) ?? spriteOr(`prop:ship-${dir}`);
  if (sprite) {
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(sprite, Math.round(x - sprite.width / 2), Math.round(y - sprite.height + 6));
    return;
  }
  shipFallback(ctx, Math.round(x), Math.round(y), dir);
}

export function drawAirship(ctx: CanvasRenderingContext2D, x: number, y: number, dir: Direction, nowMs: number, flying: boolean): void {
  const frame = Math.floor(nowMs / 160) % 2;
  const sprite = (flying ? null : spriteOr("prop:airship-landed")) ?? spriteOr(`prop:airship-${dir}-${frame}`) ?? spriteOr("prop:airship-down-0");
  const bob = flying ? Math.round(Math.sin(nowMs / 260) * 1.5) : 0;
  if (flying) {
    const shadow = spriteOr("prop:airship-shadow");
    if (shadow) {
      ctx.drawImage(shadow, Math.round(x - shadow.width / 2), Math.round(y + 6));
    }
  }
  if (sprite) {
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(sprite, Math.round(x - sprite.width / 2), Math.round(y - sprite.height + 6 + bob - (flying ? 8 : 0)));
    return;
  }
  airshipFallback(ctx, Math.round(x), Math.round(y - (flying ? 8 : 0) + bob), dir, frame);
}
