import { getTileId, type TileMap } from "../game/map/tile-map";
import type { Camera } from "./camera";

/** カメラに映る範囲のタイルだけを描画する。 */
export function renderTileMap(
  ctx: CanvasRenderingContext2D,
  map: TileMap,
  camera: Camera,
): void {
  const { tileWidth, tileHeight } = map.data;

  const startX = Math.max(0, Math.floor(camera.x / tileWidth));
  const startY = Math.max(0, Math.floor(camera.y / tileHeight));
  const endX = Math.min(
    map.data.width - 1,
    Math.floor((camera.x + camera.viewportWidth) / tileWidth),
  );
  const endY = Math.min(
    map.data.height - 1,
    Math.floor((camera.y + camera.viewportHeight) / tileHeight),
  );

  for (let layerIndex = 0; layerIndex < map.data.layers.length; layerIndex++) {
    for (let tileY = startY; tileY <= endY; tileY++) {
      for (let tileX = startX; tileX <= endX; tileX++) {
        const tileId = getTileId(map, layerIndex, tileX, tileY);
        if (tileId === 0) {
          continue;
        }
        const color = map.data.tileColors[tileId];
        if (!color) {
          continue;
        }
        ctx.fillStyle = color;
        ctx.fillRect(
          tileX * tileWidth - camera.x,
          tileY * tileHeight - camera.y,
          tileWidth,
          tileHeight,
        );
      }
    }
  }
}
