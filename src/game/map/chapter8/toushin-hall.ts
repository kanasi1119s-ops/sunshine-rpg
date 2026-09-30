import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const DAIS = 3;
const SEAT = 4;
const DOOR = 5;
const CARPET = 6;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#a49a8a",
  [WALL]: "#3e3e4e",
  [DAIS]: "#6a5a7a",
  [SEAT]: "#5a4a3a",
  [DOOR]: "#4a5a86",
  [CARPET]: "#8a3a4a",
};

const NON_WALKABLE = new Set([WALL, DAIS, SEAT]);

const WIDTH = 22;
const HEIGHT = 15;

const SOUTH_DOOR = { x: 10, y: HEIGHT - 1 };
/** 奥の議長席の壇（6x2）。 */
const DAIS_ORIGIN = { x: 8, y: 2 };

/**
 * 第8章の事件現場、灯芯都の合議会堂。
 * 中央に赤い絨毯が敷かれた議場で、奥に議長席、両側に議員席が並ぶ。
 */
export function createToushinHallData(): TileMapData {
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

  // 中央の絨毯。
  for (let y = 4; y < HEIGHT - 1; y++) {
    set(10, y, CARPET);
    set(11, y, CARPET);
  }
  // 奥の壇。
  for (let dx = 0; dx < 6; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(DAIS_ORIGIN.x + dx, DAIS_ORIGIN.y + dy, DAIS);
    }
  }
  // 両側の議員席。
  for (let y = 5; y < 11; y += 2) {
    for (const x of [3, 4, 6, 15, 17, 18]) {
      set(x, y, SEAT);
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
        // 南の扉から、灯芯都の広場へ。
        tileX: SOUTH_DOOR.x,
        tileY: SOUTH_DOOR.y,
        targetMapId: "toushin-town",
        targetTileX: 13,
        targetTileY: 2,
      },
    ],
  };
}

/** 広場から入ってきたときの立ち位置。 */
export const TOUSHIN_HALL_ENTRY = { tileX: SOUTH_DOOR.x, tileY: SOUTH_DOOR.y - 2 };

/** 議場内のNPC・仕掛けを置く座標（イベントデータ側で使う）。 */
export const TOUSHIN_HALL_LANDMARKS = {
  chair: { tileX: DAIS_ORIGIN.x + 2, tileY: DAIS_ORIGIN.y + 2 },
  edrea: { tileX: DAIS_ORIGIN.x + 4, tileY: DAIS_ORIGIN.y + 2 },
  clerk: { tileX: 6, tileY: 8 },
  witness: { tileX: 16, tileY: 8 },
};
