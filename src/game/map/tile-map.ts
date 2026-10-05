import type { MapExit, TileMapData } from "./types";

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

/** つながる地図なら、座標を地図の中に折りかえす。 */
function wrapTile(map: TileMap, tileX: number, tileY: number): [number, number] {
  if (!map.data.wrap) return [tileX, tileY];
  const w = map.data.width, h = map.data.height;
  return [((tileX % w) + w) % w, ((tileY % h) + h) % h];
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
  [tileX, tileY] = wrapTile(map, tileX, tileY);
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
  [tileX, tileY] = wrapTile(map, tileX, tileY);
  if (!isInBounds(map, tileX, tileY)) {
    return false;
  }
  const collision = map.data.collision;
  if (!collision) {
    return true;
  }
  return collision[tileY * map.data.width + tileX] !== 1;
}

export function findExitAt(map: TileMap, tileX: number, tileY: number): MapExit | undefined {
  return map.data.exits?.find((exit) => exit.tileX === tileX && exit.tileY === tileY);
}
