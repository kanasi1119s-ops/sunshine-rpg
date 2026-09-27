import type { TileMapData } from "./types";

const FLOOR = 6;
const WALL = 7;
const DOOR = 5;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#8a7458",
  [WALL]: "#332e2a",
  [DOOR]: "#6b4a2b",
};

/**
 * エンジンの動作確認用の仮の室内マップ（単色タイル）。
 * 原っぱマップ（sample-map.ts）の扉から入れる、小さな1部屋。
 */
export function createSampleRoomData(): TileMapData {
  const width = 8;
  const height = 6;
  const ground: number[] = new Array(width * height).fill(FLOOR);
  const collision: number[] = new Array(width * height).fill(0);

  const set = (x: number, y: number, tile: number, walkable: boolean): void => {
    ground[y * width + x] = tile;
    collision[y * width + x] = walkable ? 0 : 1;
  };

  for (let x = 0; x < width; x++) {
    set(x, 0, WALL, false);
    set(x, height - 1, WALL, false);
  }
  for (let y = 0; y < height; y++) {
    set(0, y, WALL, false);
    set(width - 1, y, WALL, false);
  }

  const doorX = Math.floor(width / 2);
  set(doorX, height - 1, DOOR, true);

  return {
    width,
    height,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    collision,
    exits: [
      {
        tileX: doorX,
        tileY: height - 1,
        targetMapId: "sample-field",
        targetTileX: Math.floor(20 / 2),
        targetTileY: 1,
      },
    ],
  };
}

export const SAMPLE_ROOM_ENTRY = { tileX: Math.floor(8 / 2), tileY: 4 };
