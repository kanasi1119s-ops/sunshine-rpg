import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const SHELF = 3;
const TABLE = 4;
const DOOR = 5;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#8a8578",
  [WALL]: "#4a4c54",
  [SHELF]: "#6a4c34",
  [TABLE]: "#7a6248",
  [DOOR]: "#6a5a4a",
};

const NON_WALKABLE = new Set([WALL, SHELF, TABLE]);

const WIDTH = 20;
const HEIGHT = 14;

const SOUTH_DOOR = { x: 9, y: HEIGHT - 1 };
/** 奥の閲覧机（3x2）。改ざんされた記録が広げられている。 */
const TABLE_ORIGIN = { x: 8, y: 3 };

/**
 * 第5章の事件現場、断崖の岩壁を掘った記録の間（古文書庫）。
 * 環信仰の古い記録が納められ、その一部が書き換えられている。
 */
export function createKiriArchiveData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(FLOOR);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, WALL);
    set(x, HEIGHT - 1, x === SOUTH_DOOR.x ? DOOR : WALL);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL);
    set(WIDTH - 1, y, WALL);
  }

  // 左右の壁ぎわの書架。
  for (let y = 2; y < 10; y++) {
    set(2, y, SHELF);
    set(WIDTH - 3, y, SHELF);
  }
  // 奥の閲覧机。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(TABLE_ORIGIN.x + dx, TABLE_ORIGIN.y + dy, TABLE);
    }
  }

  return {
    width: WIDTH,
    height: HEIGHT,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    collision,
    exits: [
      {
        // 南の戸口から、霧断崖の町へ。
        tileX: SOUTH_DOOR.x,
        tileY: SOUTH_DOOR.y,
        targetMapId: "kiri-town",
        targetTileX: 12,
        targetTileY: 2,
      },
    ],
  };
}

/** 町から入ってきたときの立ち位置。 */
export const KIRI_ARCHIVE_ENTRY = { tileX: SOUTH_DOOR.x, tileY: SOUTH_DOOR.y - 2 };

/** 記録の間のNPC・仕掛けを置く座標（イベントデータ側で使う）。 */
export const KIRI_ARCHIVE_LANDMARKS = {
  record: { tileX: TABLE_ORIGIN.x + 1, tileY: TABLE_ORIGIN.y + 2 },
  margin: { tileX: 4, tileY: 5 },
  ledger: { tileX: 15, tileY: 5 },
  keeper: { tileX: 7, tileY: 7 },
};
