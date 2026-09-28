import type { Npc } from "../game/npc";
import type { TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";
import { PORTRAITS, PORTRAIT_GRID_HEIGHT, PORTRAIT_GRID_WIDTH } from "../game/portrait/portraits";
import { OVERWORLD_CELL_SIZE, renderPortrait } from "./portrait-renderer";

/**
 * `spriteName`が`PORTRAITS`に登録されているNPCは、そのドット絵をタイル中央に
 * 描く。登録が無いNPC（名前の無い町の人など）は、これまで通りの色付き四角で
 * 表す（ドット絵ができるまでの仮表示）。
 */
export function renderNpcs(
  ctx: CanvasRenderingContext2D,
  npcs: Npc[],
  map: TileMap,
  camera: Camera,
): void {
  const { tileWidth, tileHeight } = map.data;
  for (const npc of npcs) {
    const x = npc.tileX * tileWidth - camera.x;
    const y = npc.tileY * tileHeight - camera.y;
    const spec = npc.spriteName ? PORTRAITS[npc.spriteName] : undefined;
    if (spec) {
      const offsetX = Math.floor((tileWidth - PORTRAIT_GRID_WIDTH) / 2);
      const offsetY = Math.floor((tileHeight - PORTRAIT_GRID_HEIGHT) / 2);
      renderPortrait(ctx, spec, x + offsetX, y + offsetY, OVERWORLD_CELL_SIZE);
      continue;
    }
    ctx.fillStyle = npc.color;
    ctx.fillRect(x + 2, y + 2, tileWidth - 4, tileHeight - 4);
  }
}
