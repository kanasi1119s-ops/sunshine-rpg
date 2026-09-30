import type { Npc } from "../game/npc";
import type { TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";
import { spriteSpecForNpc } from "../game/sprite/character-specs";
import { SPRITE_FEET_ROW } from "../game/sprite/overworld-sprite";
import { drawSprite } from "./sprite-renderer";

/** NPCの足元のy（ワールド座標）。プレイヤーとの前後（奥のものを先に描く）を決めるのに使う。 */
export function npcFeetY(npc: Npc, tileHeight: number): number {
  return npc.tileY * tileHeight + tileHeight;
}

/**
 * NPCのドット絵（16×32、正面向き）を、そのマスの足元にそろえて描く（頭は上のマスにはみ出す）。
 * 顔グラフィックのある人は、その色。名前の無い人は、IDから髪・肌・髪型を決めた色替え。
 * `filter` で、描くNPCを絞れる（プレイヤーより奥・手前に分けて描くため）。
 */
export function renderNpcs(
  ctx: CanvasRenderingContext2D,
  npcs: Npc[],
  map: TileMap,
  camera: Camera,
  filter: (npc: Npc) => boolean = () => true,
): void {
  const { tileWidth, tileHeight } = map.data;
  for (const npc of npcs) {
    if (!filter(npc)) {
      continue;
    }
    const x = npc.tileX * tileWidth - camera.x;
    const feetY = npcFeetY(npc, tileHeight) - camera.y;
    drawSprite(ctx, spriteSpecForNpc(npc), "down", 0, x + (tileWidth - 16) / 2, feetY - SPRITE_FEET_ROW - 1);
  }
}
