import type { PlayerState } from "../game/player";
import type { Camera } from "./camera";
import { PORTRAITS } from "../game/portrait/portraits";
import { OVERWORLD_CELL_SIZE, renderPortrait } from "./portrait-renderer";

const HERO_SPEC = PORTRAITS["ユーリ"];

/** 歩行アニメーション1コマの長さ（ms）。2コマを交互に切り替え、簡単な足踏みに見せる。 */
const BOB_PERIOD_MS = 300;

/** 動いている間だけ、1コマおきに1px浮かせて足踏みのように見せる（当たり判定には影響しない）。 */
function walkBobOffset(player: PlayerState): number {
  if (!player.moving) {
    return 0;
  }
  const phase = (player.animationMs % BOB_PERIOD_MS) / BOB_PERIOD_MS;
  return phase < 0.5 ? 0 : -1;
}

/**
 * 主人公ユーリのドット絵（`game/portrait/portraits.ts`のグリッドを、
 * 当たり判定サイズ（12×14）に合わせて等倍で描く）。向いている方向が
 * 分かるよう、進行方向側に小さな三角形を重ねて表示し、歩いている間は
 * 簡単な足踏みアニメーションを付ける。
 */
export function renderPlayer(
  ctx: CanvasRenderingContext2D,
  player: PlayerState,
  camera: Camera,
): void {
  const screenX = player.x - camera.x;
  const drawY = player.y - camera.y + walkBobOffset(player);

  renderPortrait(ctx, HERO_SPEC, screenX, drawY, OVERWORLD_CELL_SIZE);

  const cx = screenX + player.width / 2;
  const cy = drawY + player.height / 2;
  ctx.fillStyle = "#f2c14e";
  ctx.beginPath();
  switch (player.direction) {
    case "up":
      ctx.moveTo(cx - 3, drawY + 3);
      ctx.lineTo(cx + 3, drawY + 3);
      ctx.lineTo(cx, drawY - 2);
      break;
    case "down":
      ctx.moveTo(cx - 3, drawY + player.height - 3);
      ctx.lineTo(cx + 3, drawY + player.height - 3);
      ctx.lineTo(cx, drawY + player.height + 2);
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
