import type { PlayerState } from "../game/player";
import type { Camera } from "./camera";
import { HERO_SPRITE } from "../game/sprite/character-specs";
import { frameAt, SPRITE_FEET_ROW, SPRITE_WIDTH } from "../game/sprite/overworld-sprite";
import { drawSprite } from "./sprite-renderer";

/**
 * 主人公ユーリのドット絵（16×32、4方向×3コマの歩き）。当たり判定（12×14）は変えず、判定の足元の中央に、
 * 絵の足元をそろえて描く（頭は上のマスにはみ出す）。
 */
export function renderPlayer(ctx: CanvasRenderingContext2D, player: PlayerState, camera: Camera): void {
  const feetX = player.x + player.width / 2 - camera.x;
  const feetY = player.y + player.height - camera.y;
  drawSprite(
    ctx,
    HERO_SPRITE,
    player.direction,
    frameAt(player.moving, player.animationMs),
    feetX - SPRITE_WIDTH / 2,
    feetY - SPRITE_FEET_ROW - 1,
  );
}
