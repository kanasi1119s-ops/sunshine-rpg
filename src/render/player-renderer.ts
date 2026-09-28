import type { PlayerState } from "../game/player";
import type { Camera } from "./camera";
import { PORTRAITS } from "../game/portrait/portraits";
import { OVERWORLD_CELL_SIZE, renderPortrait } from "./portrait-renderer";

const HERO_SPEC = PORTRAITS["ユーリ"];

/**
 * 主人公ユーリのドット絵（`game/portrait/portraits.ts`のグリッドを、
 * 当たり判定サイズ（12×14）に合わせて等倍で描く）。向いている方向が
 * 分かるよう、進行方向側に小さな三角形を重ねて表示する。
 */
export function renderPlayer(
  ctx: CanvasRenderingContext2D,
  player: PlayerState,
  camera: Camera,
): void {
  const screenX = player.x - camera.x;
  const screenY = player.y - camera.y;

  renderPortrait(ctx, HERO_SPEC, screenX, screenY, OVERWORLD_CELL_SIZE);

  const cx = screenX + player.width / 2;
  const cy = screenY + player.height / 2;
  ctx.fillStyle = "#f2c14e";
  ctx.beginPath();
  switch (player.direction) {
    case "up":
      ctx.moveTo(cx - 3, screenY + 3);
      ctx.lineTo(cx + 3, screenY + 3);
      ctx.lineTo(cx, screenY - 2);
      break;
    case "down":
      ctx.moveTo(cx - 3, screenY + player.height - 3);
      ctx.lineTo(cx + 3, screenY + player.height - 3);
      ctx.lineTo(cx, screenY + player.height + 2);
      break;
    case "left":
      ctx.moveTo(screenX + 3, cy - 3);
      ctx.lineTo(screenX + 3, cy + 3);
      ctx.lineTo(screenX - 2, cy);
      break;
    case "right":
      ctx.moveTo(screenX + player.width - 3, cy - 3);
      ctx.lineTo(screenX + player.width - 3, cy + 3);
      ctx.lineTo(screenX + player.width + 2, cy);
      break;
  }
  ctx.closePath();
  ctx.fill();
}
