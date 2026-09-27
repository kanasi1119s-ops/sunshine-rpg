import type { Npc } from "../game/npc";
import type { TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";

/** ドット絵ができるまでの仮表示。タイルより一回り小さい色付き四角で表す。 */
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
    ctx.fillStyle = npc.color;
    ctx.fillRect(x + 2, y + 2, tileWidth - 4, tileHeight - 4);
  }
}
