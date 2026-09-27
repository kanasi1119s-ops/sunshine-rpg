import type { PlayerState } from "../game/player";
import type { Camera } from "./camera";

/**
 * ドット絵ができるまでの仮表示。向いている方向が分かるよう、
 * 進行方向側に小さな三角形を付けた色付き四角で表す。
 */
export function renderPlayer(
  ctx: CanvasRenderingContext2D,
  player: PlayerState,
  camera: Camera,
): void {
  const screenX = player.x - camera.x;
  const screenY = player.y - camera.y;

  ctx.fillStyle = "#f2c14e";
  ctx.fillRect(screenX, screenY, player.width, player.height);

  const cx = screenX + player.width / 2;
  const cy = screenY + player.height / 2;
  ctx.fillStyle = "#8a5a1e";
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
