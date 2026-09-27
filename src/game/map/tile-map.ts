import type { TileMapData } from "./types";

export interface TileMap {
  data: TileMapData;
  widthPx: number;
  heightPx: number;
}

export function createTileMap(data: TileMapData): TileMap {
  return {
    data,
    widthPx: data.width * data.tileWidth,
    heightPx: data.height * data.tileHeight,
  };
}

function isInBounds(map: TileMap, tileX: number, tileY: number): boolean {
  return (
    tileX >= 0 && tileY >= 0 && tileX < map.data.width && tileY < map.data.height
  );
}

export function getTileId(
  map: TileMap,
  layerIndex: number,
  tileX: number,
  tileY: number,
): number {
  if (!isInBounds(map, tileX, tileY)) {
    return 0;
  }
  const layer = map.data.layers[layerIndex];
  if (!layer) {
    return 0;
  }
  return layer.data[tileY * map.data.width + tileX] ?? 0;
}

/** マップ外、または通行判定レイヤーで塞がれているタイルは通れない。 */
export function isWalkable(map: TileMap, tileX: number, tileY: number): boolean {
  if (!isInBounds(map, tileX, tileY)) {
    return false;
  }
  const collision = map.data.collision;
  if (!collision) {
    return true;
  }
  return collision[tileY * map.data.width + tileX] !== 1;
}
